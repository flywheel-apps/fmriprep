#!/usr/bin/env python3

import json
import os, os.path as op
import subprocess as sp
import sys
import shutil
import flywheel_bids
import flywheel
from utils import args
from utils.bids.download_bids import *
from utils.bids.validate_bids import *
from utils.fly.custom_log import *
from utils.fly.load_manifest_json import *
from utils.fly.make_file_name_safe import *
from utils.results.set_zip_name import set_zip_head
from utils.results.zip_htmls import zip_htmls
from utils.results.zip_output import zip_output
from utils.results.zip_intermediate import zip_all_intermediate_output
from utils.results.zip_intermediate import zip_intermediate_selected
from utils.results.zip_intermediate import zip_intermediate_selected
import utils.dry_run
import utils.fmriprep as fp
import utils.freesurfer as fs
from create_archive_funcs import get_flywheel_hierarchy, determine_fmap_intendedfor, create_bids_hierarchy

flywheelv0 = '/flywheel/v0'
environ_json = '/tmp/gear_environ.json'

def download_optional_inputs(flywheel_basedir, sub_dir, ses_dir, rootdir):
    """
    Use manifest-defined anatomical files if they were provided
    """
    print('Looking for manifest-defined anatomical files')
    t1_anat_dir = os.path.join(flywheel_basedir, 'input', 't1w_anatomy')
    if os.path.isdir(t1_anat_dir):
        t1_file = os.listdir(t1_anat_dir)
        if t1_file:
            t1_file = os.path.join(t1_anat_dir, t1_file[0])
            anat_dir = os.path.join(rootdir, sub_dir, ses_dir, 'anat')
            if not os.path.isdir(anat_dir):
                os.mkdir(anat_dir)
            dest_file = os.path.join(anat_dir, sub_dir + '_' + ses_dir + '_T1w.nii.gz')
            if os.path.exists(dest_file):
                print('Found downloaded T1 file - overwriting!')
                os.remove(dest_file)
                os.remove(dest_file.replace('.nii.gz', '.json'))
            shutil.copyfile(t1_file, dest_file)

    t2_anat_dir = os.path.join(flywheel_basedir, 'input', 't2w_anatomy')
    if os.path.isdir(t2_anat_dir):
        t2_file = os.listdir(t2_anat_dir)
        if t2_file:
            anat_dir = os.path.join(rootdir, sub_dir, ses_dir, 'anat')
            if not os.path.isdir(anat_dir):
                os.mkdir(anat_dir)
            t2_file = os.path.join(t2_anat_dir, t2_file[0])
            dest_file = os.path.join(anat_dir, sub_dir + '_' + ses_dir + '_T2w.nii.gz')
            if os.path.exists(dest_file):
                print('Found downloaded T2 file - overwriting!')
                os.remove(dest_file)
                os.remove(dest_file.replace('.nii.gz', '.json'))
            shutil.copyfile(t2_file, dest_file)

def setup_logger(gear_context):
    """
    This function simply sets up the gear logger to Flywheel SSE best practices
    :param gear_context: the gear context
    :type gear_context: class: `flywheel.gear_context.GearContext`
    """

    # Setup logging as per SSE best practices
    fmt = '%(asctime)s %(levelname)8s %(name)-8s %(funcName)s - %(message)s'
    logging.basicConfig(level=gear_context.config['gear-log-level'], format=fmt)
    gear_context.log = logging.getLogger('[flywheel/extract-cmrr-physio]')
    gear_context.log.info('log level is ' + gear_context.config['gear-log-level'])
    gear_context.log_config()  # not configuring the log but logging the config


def set_environment():

    log = logging.getLogger()
    # Let's ensure that we have our environment .json file and load it up
    if op.exists(environ_json):

        # If it exists, read the file in as a python dict with json.load
        with open(environ_json, 'r') as f:
            log.info('Loading gear environment')
            environ = json.load(f)

        # Now set the current environment using the keys.  This will automatically be used with any sp.run() calls,
        # without the need to pass in env=...  Passing env= will unset all these variables, so don't use it if you do it
        # this way.
        for key in environ.keys():
            os.environ[key] = environ[key]
    else:
        log.warning('No Environment file found!')
    # Pass back the environ dict in case the run.py program has need of it later on.
    return environ


# def create_bids_directory(context):
#
#     try:
#         bidsdir = op.join(context.work_dir, 'bids')
#         bidsdir = op.join('/flywheel/v0','input','bids_dataset')
#
#         if not op.exists(bidsdir):
#             #   Use Python SDK to accomplish this task
#             cmd = ['/usr/local/miniconda/bin/python', '{}/create_archive.py'.format(flywheelv0)]
#             cm.exec_command(context, cmd)
#         else:
#             context.log.warning('Found Existing data in {}'.format(bidsdir))
#     except:
#         raise Exception('Unable to generate BIDS directory')
#
#     return bidsdir


def cleanup(context):


    # Make archives for result *.html files for easy display on platform
    path = context.gear_dict['output_analysisid_dir'] + \
                             '/' + context.gear_dict['COMMAND']
    zip_htmls(context, path)

    zip_output(context)

    # possibly save ALL intermediate output
    if context.config['save-intermediate-work']:
        zip_all_intermediate_output(context)

    # possibly save intermediate files and folders
    zip_intermediate_selected(context)

    # clean up: remove output that was zipped
    if os.path.exists(context.gear_dict['output_analysisid_dir']):
        if not context.config['save-outputs']:

            shutil.rmtree(context.gear_dict['output_analysisid_dir'])
            log.debug('removing output directory "' +
                      context.gear_dict['output_analysisid_dir'] + '"')

        else:
            log.info('NOT removing output directory "' +
                      context.gear_dict['output_analysisid_dir'] + '"')

    else:
        log.info('Output directory does not exist so it cannot be removed')


    if len(context.gear_dict['warnings']) > 0 :
        msg = 'Previous warnings:\n'
        for err in context.gear_dict['warnings']:
            if str(type(err)).split("'")[1] == 'str':
                # show string
                msg += '  Warning: ' + str(err) + '\n'
            else:  # show type (of warning) and warning message
                msg += '  ' + str(type(err)).split("'")[1] + ': ' + str(err) + '\n'
        log.info(msg)

    if len(context.gear_dict['errors']) > 0 :
        msg = 'Previous errors:\n'
        for err in context.gear_dict['errors']:
            if str(type(err)).split("'")[1] == 'str':
                # show string
                msg += '  Error msg: ' + str(err) + '\n'
            else:  # show type (of error) and error message
                msg += '  ' + str(type(err)).split("'")[1] + ': ' + str(err) + '\n'
        log.info(msg)
        ret = 1

    log.info('BIDS App Gear is done.  Returning '+str(ret))
    os.sys.exit(ret)


def list_files(startpath):
    log=logging.getLogger()
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        log.info('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            log.info('{}{}'.format(subindent, f))




def initialize(context):
    # Add manifest.json as the manifest_json attribute
    setattr(context, 'manifest_json', load_manifest_json())

    log = custom_log(context)

    # Find Freesurfer License
    # fs.find_freesurfer_license(context, context.get_input_path('freesurfer-license'))

    context.gear_dict = {}
    context.log_config() # not configuring the log but logging the config

    # Instantiate custom gear dictionary to hold "gear global" info
    context.gear_dict = {}

    # The main command line command to be run:
    context.gear_dict['COMMAND'] = 'fmriprep'

    # Keep a list of errors and warning to print all in one place at end of log
    # Any errors will prevent the command from running and will cause exit(1)
    context.gear_dict['errors'] = []
    context.gear_dict['warnings'] = []

    # Get level of run from destination's parent: subject or session
    fw = context.client
    dest_container = fw.get(context.destination['id'])
    context.gear_dict['run_level'] = dest_container.parent.type

    project_id = dest_container.parents.project
    context.gear_dict['project_id'] = project_id
    if project_id:
        project = fw.get(project_id)
        context.gear_dict['project_label'] = project.label
        context.gear_dict['project_label_safe'] = \
            make_file_name_safe(project.label, '_')
    else:
        context.gear_dict['project_label'] = 'unknown_project'
        context.gear_dict['project_label_safe'] = 'unknown_project'
        log.warning('Project label is ' + context.gear_dict['project_label'])

    subject_id = dest_container.parents.subject
    context.gear_dict['subject_id'] = subject_id
    if subject_id:
        subject = fw.get(subject_id)
        context.gear_dict['subject_code'] = subject.code
        context.gear_dict['subject_code_safe'] = \
            make_file_name_safe(subject.code, '_')
    else:
        context.gear_dict['subject_code'] = 'unknown_subject'
        context.gear_dict['subject_code_safe'] = 'unknown_subject'
        log.warning('Subject code is ' + context.gear_dict['subject_code'])

    session_id = dest_container.parents.session
    context.gear_dict['session_id'] = session_id
    if session_id:
        session = fw.get(session_id)
        context.gear_dict['session_label'] = session.label
        context.gear_dict['session_label_safe'] = \
            make_file_name_safe(session.label, '_')
    else:
        context.gear_dict['session_label'] = 'unknown_session'
        context.gear_dict['session_label_safe'] = 'unknown_session'
        log.warning('Session label is ' + context.gear_dict['session_label'])

    # Set first part of result zip file names based on the above file safe names
    set_zip_head(context)

    # the usual BIDS path:
    bids_path = os.path.join(context.work_dir, 'bids')
    context.gear_dict['bids_path'] = bids_path

    # in the output/ directory, add extra analysis_id directory name for easy
    #  zipping of final outputs to return.
    context.gear_dict['output_analysisid_dir'] = \
        context.output_dir + '/' + context.destination['id']

    # grab environment for gear
    with open('/tmp/gear_environ.json', 'r') as f:
        environ = json.load(f)
        context.gear_dict['environ'] = environ

        # Add environment to log if debugging
        kv = ''
        for k, v in environ.items():
            kv += k + '=' + v + ' '
        log.debug('Environment: ' + kv)

    set_environment()

    return log


def create_command(context, log):

    # Create the command and validate the given arguments
    try:

        # Set the actual gear command:
        command = [context.gear_dict['COMMAND']]

        # 3 positional args: bids path, output dir, 'participant'
        # This should be done here in case there are nargs='*' arguments
        # These follow the BIDS Apps definition (https://github.com/BIDS-Apps)
        command.append(context.gear_dict['bids_path'])
        command.append(context.gear_dict['output_analysisid_dir'])
        command.append('participant')

        # Put command into gear_dict so arguments can be added in args.
        context.gear_dict['command'] = command

        # Generate Command Call
        log.info('generating fmriprep command call')
        command = fp.create_command(context,log)
        context.log.info('Done')
        context.gear_dict['command'] = command
        log.info(command)


    except Exception as e:
        context.gear_dict['errors'].append(e)
        log.critical(e)
        log.exception('Error in creating and validating command.',)

    pass


def create_and_download_bids(fw, rootdir, flywheel_basedir, analysis_id):
    log=logging.getLogger()
    ## Create flywheel hierarchy
    print("Create Flywheel Hierarchy")
    flywheel_hierarchy = get_flywheel_hierarchy(fw, analysis_id)
    log.debug(flywheel_hierarchy)
    #pprint.pprint(flywheel_hierarchy)

    # Determine what fieldmaps and functionals are connected...
    print("Determine fmap intendedfor")
    fmaps_intendedfor = determine_fmap_intendedfor(flywheel_hierarchy)
    print(fmaps_intendedfor)

    ### Create bids hierarchy
    print("Create BIDS Hierarchy")
    bids_hierarchy, files_lookup = create_bids_hierarchy(flywheel_hierarchy, fmaps_intendedfor)
    # Print out BIDS hierarchy (for logs)
    pprint.pprint(bids_hierarchy)

    ### Download flywheel files into the bids hierarchy within the ROOTDIR defined above
    # Make sure to create all directories within bids hierarchy
    print("Download files into BIDS hierarchy")
    for sub_dir in bids_hierarchy.keys():
        os.makedirs(os.path.join(rootdir, sub_dir))
        for ses_dir in bids_hierarchy[sub_dir].keys():
            os.makedirs(os.path.join(rootdir, sub_dir, ses_dir))
            for desc_dir in bids_hierarchy[sub_dir][ses_dir].keys():
                os.makedirs(os.path.join(rootdir, sub_dir, ses_dir, desc_dir))

    # Now iterate over all flywheel files and download to correct bids filename
    for flywheel_file, bids_file in files_lookup:
        # Create JSON file
        if type(flywheel_file) is dict:
            with open(os.path.join(rootdir, bids_file), 'w') as fp:
                json.dump(flywheel_file, fp)
        # OR Download flywheel file
        else:
            # Get flywheel info in order to download file
            project_id, session_id, acq_id, filename = flywheel_file.split('/')
            # Download file
            fw.download_file_from_acquisition(acq_id, filename, os.path.join(rootdir, bids_file))

    download_optional_inputs(flywheel_basedir, sub_dir, ses_dir, rootdir)


def set_up_data(context, log):
    # Set up and validate data to be used by command
    try:

        # Download bids for the current session
        # editme: add kwargs to limit what is downloaded
        # bool src_data: Whether or not to include src data (e.g. dicoms) default: False
        # list subjects: The list of subjects to include (via subject code) otherwise all subjects
        # list sessions: The list of sessions to include (via session label) otherwise all sessions
        # list folders: The list of folders to include (otherwise all folders) e.g. ['anat', 'func']
        # **kwargs: Additional arguments to pass to download_bids_dir

        #folders_to_load = ['anat', 'func', 'fmap']
        fw = context.client
        analysis_id = str(context.destination['id'])

        # Get analysis
        analysis = fw.get_analysis(analysis_id)
        # Get container type and id from
        container_type = analysis['parent']['type']
        container_id = analysis['parent']['id']



        folders_to_load = []  # leave empty to download all folders

        if context.gear_dict['run_level'] == 'project':

            log.info('Downloading BIDS for project "' +
                     context.gear_dict['project_label'] + '"')

            project = fw.get_project(container_id)
            BIDS_metadata = project.get('info', {}).get('BIDS')
            print(BIDS_metadata)
            try:
                # don't filter by subject or session, grab all
                download_bids(context, folders=folders_to_load)
            except flywheel_bids.supporting_files.errors.BIDSExportError:
                create_and_download_bids(fw, context.gear_dict['bids_path'], '/flywheel/v0', analysis_id)


        elif context.gear_dict['run_level'] == 'subject':

            log.info('Downloading BIDS for subject "' +
                     context.gear_dict['subject_code'] + '"')

            subject = fw.get_subject(container_id)
            session = fw.get_session(subject.session)
            project = fw.get_project(session.project)

            BIDS_metadata = subject.get('info', {}).get('BIDS')
            print(BIDS_metadata)

            try:
                # filter by subject
                download_bids(context,
                          subjects = [context.gear_dict['subject_code']],
                          folders=folders_to_load)

            except flywheel_bids.supporting_files.errors.BIDSExportError:
                create_and_download_bids(fw, context.gear_dict['bids_path'], '/flywheel/v0', analysis_id)


        elif context.gear_dict['run_level'] == 'session':

            log.info('Downloading BIDS for session "' +
                     context.gear_dict['session_label'] + '"')
            session = fw.get_session(container_id)
            project = fw.get_project(session.project)
            BIDS_metadata = session.get('info', {}).get('BIDS')
            # filter by session
            try:
                download_bids(context,
                          sessions = [context.gear_dict['session_label']],
                          folders=folders_to_load)

            except flywheel_bids.supporting_files.errors.BIDSExportError:
                create_and_download_bids(fw, context.gear_dict['bids_path'], '/flywheel/v0', analysis_id)

            download_optional_inputs('/flywheel/v0', "sub-{}".format(BIDS_metadata.get('Subject')),
                                     "ses-{}".format(BIDS_metadata.get('Label')), context.gear_dict['bids_path'])

        else:
            msg = 'This job is not being run at the project subject or session level'
            raise TypeError(msg)







        # Validate Bids file heirarchy
        # Bids validation on a phantom tree may be occuring soon
        validate_bids(context)

    except Exception as e:
        context.gear_dict['errors'].append(e)
        log.critical(e)
        log.exception('Error in BIDS download and validation.',)


def execute(context, log):
    try:

        log.info('Command: ' + ' '.join(context.gear_dict['command']))

        # Don't run if there were errors or if this is a dry run
        ok_to_run = True

        if len(context.gear_dict['errors']) > 0:
            ok_to_run = False
            result = sp.CompletedProcess
            result.returncode = 1
            log.info('Command was NOT run because of previous errors.')

        if context.config['gear-dry-run']:
            ok_to_run = False
            result = sp.CompletedProcess
            result.returncode = 0
            e = 'dry-run is set: Command was NOT run.'
            log.warning(e)
            context.gear_dict['warnings'].append(e)
            utils.dry_run.pretend_it_ran(context)

        if ok_to_run:
            # Run the actual command this gear was created for
            result = sp.run(context.gear_dict['command'],
                        env = context.gear_dict['environ'])
            log.debug(repr(result))

        log.info('Return code: ' + str(result.returncode))

        if result.returncode == 0:
            log.info('Command successfully executed!')

        else:
            log.info('Command failed.')

    except Exception as e:
        context.gear_dict['errors'].append(e)
        log.critical(e)
        log.exception('Unable to execute command.')

    finally:

        # Make archives for result *.html files for easy display on platform
        path = context.gear_dict['output_analysisid_dir'] + \
                                 '/' + context.gear_dict['COMMAND']
        zip_htmls(context, path)

        zip_output(context)

        # possibly save ALL intermediate output
        if context.config['save-intermediate-work']:
            zip_all_intermediate_output(context)

        # possibly save intermediate files and folders
        zip_intermediate_selected(context)

        # clean up: remove output that was zipped
        if os.path.exists(context.gear_dict['output_analysisid_dir']):
            if not context.config['save-outputs']:

                shutil.rmtree(context.gear_dict['output_analysisid_dir'])
                log.debug('removing output directory "' +
                          context.gear_dict['output_analysisid_dir'] + '"')

            else:
                log.info('NOT removing output directory "' +
                          context.gear_dict['output_analysisid_dir'] + '"')

        else:
            log.info('Output directory does not exist so it cannot be removed')

        ret = result.returncode

        if len(context.gear_dict['warnings']) > 0 :
            msg = 'Previous warnings:\n'
            for err in context.gear_dict['warnings']:
                if str(type(err)).split("'")[1] == 'str':
                    # show string
                    msg += '  Warning: ' + str(err) + '\n'
                else:  # show type (of warning) and warning message
                    msg += '  ' + str(type(err)).split("'")[1] + ': ' + str(err) + '\n'
            log.info(msg)

        if len(context.gear_dict['errors']) > 0 :
            msg = 'Previous errors:\n'
            for err in context.gear_dict['errors']:
                if str(type(err)).split("'")[1] == 'str':
                    # show string
                    msg += '  Error msg: ' + str(err) + '\n'
                else:  # show type (of error) and error message
                    msg += '  ' + str(type(err)).split("'")[1] + ': ' + str(err) + '\n'
            log.info(msg)
            ret = 1

        log.info('BIDS App Gear is done.  Returning '+str(ret))
        os.sys.exit(ret)




def main():
    """
    This function creates the flywheel gear context, and uses the provided input and config settings to:
    1) extract physio logs from a zipped dicom archive
    2) generate BIDS complient physio data
    3) clean up any undesired files

    """




    with flywheel.gear_context.GearContext() as context:
        try:

            log = initialize(context)

            create_command(context,log)

            set_up_data(context,log)

            execute(context,log)

            list_files('/flywheel/v0')
        except Exception as e:
            log.exception(e)
        log.info('BIDS App Gear is done.')



if __name__ == "__main__":
    main()