import flywheel
import fnmatch
import json
import logging
import os
import shutil
import sys
import zipfile

from subprocess import call
from flywheel_bids.supporting_files.utils import validate_bids

import create_archive

# Define Constants
FLYWHEEL_BASE = '.'
CONTAINER = '[flywheel/fmriprep]'

# Set up logger
logger = logging.getLogger(CONTAINER)


def recursive_chmod(path, perms=0o777):
    for root, dirs, files in os.walk(path):
        for d in dirs:
            os.chmod(os.path.join(root, d), perms)
        for f in files:
            os.chmod(os.path.join(root, f), perms)


def find_file(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def find_dir(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in dirs:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def zipdir(path, zip_handler):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip_handler.write(os.path.join(root, file))


def print_bids(bids_dir):
    for root, dirs, files in os.walk(bids_dir):
        level = root.replace(bids_dir, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def get_flags(config):
    """
    Parses the configurations and returns dictionary of flags based on the
    options
    """
    flags = {}
    # Surface Options
    config_freesurfer = config['config'].get('freesurfer')
    if config_freesurfer:
        freesurfer_flag = ''
    else:
        freesurfer_flag = '--fs-no-reconall'

    # Workflow Options
    config_ignore = config['config'].get('ignore')
    config_longitudinal = config['config'].get('longitudinal')
    config_t2s_coreg = config['config'].get('t2s_coreg')
    config_bold2t1w_dof = config['config'].get('bold2t1w_dof')
    config_output_space = config['config'].get('output_space')
    config_force_bbr = config['config'].get('force_bbr')
    config_force_no_bbr = config['config'].get('force_no_bbr')
    config_template = config['config'].get('template')
    config_template_resampling_grid = \
        config['config'].get('template_resampling_grid')
    config_medial_surface_nan = config['config'].get('medial_surface_nan')

    flags['template_FLAG'] = '--template={}'.format(config_template)
    flags['template_resampling_grid_FLAG'] = \
        '-template_resampling_grid={}'.format(config_template_resampling_grid)
    flags['bold2t1w_dof_FLAG'] = \
        '--bold2t1w-dof={}'.format(config_bold2t1w_dof)
    flags['output_space_FLAG'] = \
        '--output-space={}'.format(config_output_space)

    if config_ignore:
        flags['ignore_FLAG'] = ''
    else:
        flags['ignore_FLAG'] = '--ignore'

    if config_longitudinal:
        flags['longitudinal_FLAG'] = ''
    else:
        flags['longitudinal_FLAG'] = '--longitudinal'

    if config_t2s_coreg:
        flags['t2s_coreg_FLAG'] = ''
    else:
        flags['t2s_coreg_FLAG'] = '--t2s-coreg'

    if config_force_bbr:
        flags['force_bbr_FLAG'] = ''
    else:
        flags['force_bbr_FLAG'] = '--force-bbr'

    if config_force_no_bbr:
        flags['force_no_bbr_FLAG'] = ''
    else:
        flags['force_no_bbr_FLAG'] = '--force-no-bbr'

    if config_medial_surface_nan:
        flags['medial_surface_nan_FLAG'] = ''
    else:
        flags['medial_surface_nan_FLAG'] = '--medial-surface-nan'

    return flags


def get_freesurfer_license():
    freesurfer_license_dir = os.join(FLYWHEEL_BASE,
                                     'input', 'freesurfer_license')
    freesurfer_license = None
    if os.path.exists(freesurfer_license_dir):
        dir_contents = os.listdir(freesurfer_license_dir)
        if dir_contents:
            freesurfer_license = os.join(freesurfer_license_dir,
                                         dir_contents[0])
    return freesurfer_license


def download_and_validate_bids(bids_dir):
    # Download BIDS hierarchy
    logger.info('Downloading BIDS hierarchy')
    create_archive.main(FLYWHEEL_BASE, bids_dir)

    # Validate BIDS data
    logger.info('Validating BIDS hierarchy')
    validate_bids(bids_dir)


def exit_housekeeping(fmriprep_exit_status, fmriprep_output, sub_id,
                      analysis_id, gear_output, work_dir):
    if fmriprep_exit_status == 0:
        # Convert index file to standalone zip archive
        html_files = find_file('*.html',
                               os.path.join(fmriprep_output, 'fmriprep'))
        if html_files:
            html_file = html_files[0]
        else:
            html_file = None
        html_dir = os.path.dirname(html_file)
        sub_id = os.path.splitext(os.path.basename(html_file))
        if html_file:
            logger.info('Converting output html report...')
            zip_html_basename = '{}_{}.html.zip'.format(sub_id, analysis_id)
            output_html_file = os.path.join(gear_output, zip_html_basename)
            index_output_html = os.path.join(html_dir, 'index.html')
            shutil.copyfile(html_file, index_output_html)
            with zipfile.ZipFile(output_html_file, 'w') as output_zip:
                output_zip.write(index_output_html)
                output_zip.write(os.path.join(html_dir, sub_id, 'figures'))
                output_zip.write(os.path.join(work_dir, 'reportlets',
                                              'fmriprep', sub_id))
            os.remove(index_output_html)
            logger.info('HTML report converted.')
        else:
            logger.warn('no output html report found!')

        # Look for files/folders to preserve from working directory
        work_filename = 'fmriprep_work_selected_{}_{}.zip'.format(sub_id,
                                                                  analysis_id)
        work_file_zip = os.path.join(gear_output, work_filename)
        if config_intermediate_files:
            logger.info('Archiving selected intermediate files...')
            with zipfile.ZipFile(work_file_zip, 'a') as work_zip:
                for file_pattern in config_intermediate_files:
                    files = find_file(file_pattern, work_dir)
                    for f in files:
                        work_zip.write(f)

        if config_intermediate_folders:
            logger.info('Archiving selected intermediate folders...')
            with zipfile.ZipFile(work_file_zip, 'a') as work_zip:
                for dir_pattern in config_intermediate_files:
                    dirs = find_dir(dir_pattern, work_dir)
                    for d in dirs:
                        zipdir(work_zip)

        # Generate zipped output of fmriprep
        logger.info('generating zip archive from outputs...')
        zipped_output = os.join(gear_output,
                                'fmriprep_{}_{}'.format(sub_id, analysis_id))
        with zipfile.ZipFile(zipped_output) as output_zip:
            zipdir(fmriprep_output)

        if config_save_intermediate_work:
            logger.info('generating zip archive from intermediate work files')
            zipped_output = os.join(gear_output,
                                    'fmriprep_work_{}_{}'.format(sub_id,
                                                                 analysis_id))
            with zipfile.ZipFile(zipped_output) as output_zip:
                zipdir(work_dir)
        recursive_chmod(gear_output)
    elif config_save_outputs:
        logger.error('Config "save_outputs" set to true. Zipping up outputs.')
        zipped_output = os.join(gear_output,
                                'fmriprep_{}_{}'.format(sub_id, analysis_id))
        with zipfile.ZipFile(zipped_output) as output_zip:
            zipdir(fmriprep_output)
        zipped_output = os.join(gear_output,
                                'fmriprep_work_{}_{}'.format(sub_id,
                                                             analysis_id))
        with zipfile.ZipFile(zipped_output) as output_zip:
            zipdir(work_dir)
        recursive_chmod(gear_output)
    else:
        logger.error('Save outputs config not set. Cleaning up and exiting.')


def main():
    # Useful info
    gear_output = os.path.join(FLYWHEEL_BASE, 'output')

    # Display Dockerfile for build info
    logger.info('BEGIN FMRIPREP DOCKERFILE')
    with open('{}/Dockerfile'.format(FLYWHEEL_BASE), 'r') as dockerfile:
        print(dockerfile.read())
    logger.info('END FMRIPREP DOCKERFILE')

    # Configure Environment
    with open('docker-env.json') as fp:
        data = json.load(fp)
    os.environ.update(data)

    # Parse Configurations
    config_path = os.path.join(FLYWHEEL_BASE, 'config.json')
    with open(config_path) as config_fp:
        config = json.load(config_fp)

    analysis_id = config['destination']['id']

    config_save_outputs = config['config'].get('save_outputs')
    config_save_intermediate_work = \
        config['config'].get('save_intermediate_work')
    config_intermediate_files = config['config'].get('intermediate_files')
    config_intermediate_folders = config['config'].get('intermediate_folders')

    # Get Flags for the command
    flags = get_flags(config)

    # Check Freesurfer license
    freesurfer_license = get_freesurfer_license()
    if freesurfer_license:
        shutil.copyfile(freesurfer_license, '/opt/freesurfer/license.txt')
    else:
        logger.exception('A license is required to run!')
        sys.exit(1)

    # Download and Validate BIDS hierarchy
    download_and_validate_bids(os.path.join(FLYWHEEL_BASE,
                                            'input', 'bids_dataset'))
    print_bids(bids_dir)

    # Run fmriprep
    fmriprep_output = os.path.join(gear_output, analysis_id)
    work_dir = fmriprep_output + '_work'
    fmriprep_exit_status = check_call([
            'time',
            '/usr/local/miniconda/bin/fmriprep',
            bids_dir,
            fmriprep_output,
            'participant',
            '-w={}'.format(work_dir),
            flags['freesurfer_FLAG'],
            flags['ignore_FLAG'],
            flags['longitudinal_FLAG'],
            flags['t2s_coreg_FLAG'],
            flags['bold2t1w_dof_FLAG'],
            flags['output_space_FLAG'],
            flags['force_bbr_FLAG'],
            flags['force_no_bbr_FLAG'],
            flags['template_FLAG'],
            flags['template_resampling_grid_FLAG'],
            flags['medial_surface_nan_FLAG']
        ])

    # Cleanup Outputs
    exit_housekeeping(fmriprep_exit_status, fmriprep_output, sub_id,
                      analysis_id, gear_output, work_dir)


    # Clean up
    shutil.rmtree(work_dir)
    shutil.rmtree(fmriprep_output)

    logger.info('Wrote:\n\t{}'.format('\n\t'.join(os.listdir(gear_output))))

    sys.exit(fmriprep_exit_status)


if __name__ == '__main__':
    main()
