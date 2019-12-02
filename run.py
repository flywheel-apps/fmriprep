#!/usr/bin/env /usr/local/miniconda/bin/python3.7



import os, os.path as op
import json
import flywheel
import utils.common as cm
import logging
from collections import OrderedDict
import utils.fmriprep as fp
import shutil
import utils.freesurfer as fs
from utils.fly.custom_log import *
from utils.fly.load_manifest_json import *
from utils.fly.make_file_name_safe import *
from utils.results.set_zip_name import set_zip_head
from utils.results.zip_htmls import zip_htmls
from utils.results.zip_output import zip_output
from utils.results.zip_intermediate import zip_all_intermediate_output
from utils.results.zip_intermediate import zip_intermediate_selected
from utils.results.zip_intermediate import zip_intermediate_selected



flywheelv0 = '/flywheel/v0'
environ_json = '/tmp/gear_environ.json'


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


def create_bids_directory(context):

    try:
        bidsdir = op.join(context.work_dir, 'bids')
        bidsdir = op.join('/flywheel/v0','input','bids_dataset')

        if not op.exists(bidsdir):
            #   Use Python SDK to accomplish this task
            cmd = ['/usr/local/miniconda/bin/python', '{}/create_archive.py'.format(flywheelv0)]
            cm.exec_command(context, cmd)
        else:
            context.log.warning('Found Existing data in {}'.format(bidsdir))
    except:
        raise Exception('Unable to generate BIDS directory')

    return bidsdir


def cleanup(context):


    # Make archives for result *.html files for easy display on platform
    path = context.gear_dict['output_analysisid_dir'] + \
                             '/' + context.gear_dict['COMMAND']
    zip_htmls(context, path)

    zip_output(context)

    # possibly save ALL intermediate output
    if context.config['gear-save-intermediate-output']:
        zip_all_intermediate_output(context)

    # possibly save intermediate files and folders
    zip_intermediate_selected(context)

    # clean up: remove output that was zipped
    if os.path.exists(context.gear_dict['output_analysisid_dir']):
        if not context.config['gear-keep-output']:

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
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def main():
    """
    This function creates the flywheel gear context, and uses the provided input and config settings to:
    1) extract physio logs from a zipped dicom archive
    2) generate BIDS complient physio data
    3) clean up any undesired files

    """




    with flywheel.gear_context.GearContext() as context:
        try:

            list_files('/flywheel/v0')

            fw = context.client

            # Start logging
            setup_logger(context)
            log = context.log

            # Setup environment
            set_environment()

            context.log.info('Setting Gear Dict')
            context.gear_dict = {}

            # Find Freesurfer License
            fs.find_freesurfer_license(context, context.get_input_path('freesurfer-license'))

            # Create Custom Dict
            context.custom_dict = {}

            context.gear_dict['COMMAND'] = 'fmriprep'


            # First set up some directories:
            analysis_id = context.destination.get('id')
            context.log.info('Analysis_id: {}'.format(analysis_id))

            # Get the session run type
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


            # Designated locations for "fmriprep" output and working directory
            # fmriprep_output = context.gear_dict['output_analysisid_dir'] in bids_fmriprep

            fmriprep_output = op.join(context.output_dir, '{}'.format(analysis_id))
            working_dir = op.join(context.output_dir, '{}_work'.format(analysis_id))
            context.gear_dict['output_analysisid_dir'] = fmriprep_output

            # Store these values in our custom dict
            context.custom_dict['fmriprep_output'] = fmriprep_output
            # The working directory is actually past into the command
            context.config['w'] = working_dir
            context.gear_dict={'dry-run':False}


            # Generate the BIDS directory
            context.log.info('starting create_bids_dictionary')
            bidsdir = create_bids_directory(context)
            context.log.info('exiting create_bids_dictionary')
            context.custom_dict['bidsdir'] = bidsdir

            # Generate Command Call
            context.log.info('generating fmriprep command call')
            command = fp.create_command(context)
            context.log.info('Done')

            # Run the call
            context.log.info('Calling fmriprep command call')
            fp.run_command(context, command)





        except Exception as e:
            context.log.exception(e)

        finally:
            list_files('/flywheel/v0')
            set_zip_head(context)

            path = os.path.join(fmriprep_output, context.gear_dict['COMMAND'])

            zip_htmls(context, path)
            zip_output(context)
        # possibly save ALL intermediate output
        if context.config['save-intermediate-output']:
            zip_all_intermediate_output(context)

        # possibly save intermediate files and folders
        zip_intermediate_selected(context)

        # clean up: remove output that was zipped
        if os.path.exists(fmriprep_output):

            shutil.rmtree(fmriprep_output)
            log.debug('removing output directory "' +
                      context.gear_dict['output_analysisid_dir'] + '"')

        else:
            log.info('Output directory does not exist so it cannot be removed')



        log.info('BIDS App Gear is done.')









if __name__ == "__main__":
    main()