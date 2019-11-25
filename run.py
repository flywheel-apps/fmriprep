#!/usr/bin/env python3
import os, os.path as op
import json
import flywheel
import utils.common as cm
import logging
from collections import OrderedDict
import utils.fmriprep as fp
import shutil


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
    if op.exists(environ_json, log):

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
        bidsdir = op.join(flywheelv0, 'input', 'bids_dataset')

        if not op.exists(bidsdir):
            #   Use Python SDK to accomplish this task
            cmd = ['/usr/local/miniconda/bin/python', '{}/create_archive.py'.format(flywheelv0)]
            cm.exec_command(cmd)
        else:
            context.log.warning('Found Existing data in {}'.format(bidsdir))
    except:
        raise Exception('Unable to generate BIDS directory')

    return bidsdir





def main():
    """
    This function creates the flywheel gear context, and uses the provided input and config settings to:
    1) extract physio logs from a zipped dicom archive
    2) generate BIDS complient physio data
    3) clean up any undesired files

    """




    with flywheel.gear_context.GearContext() as context:
        try:

            # Start logging
            setup_logger(context)

            # Setup environment
            set_environment()

            # Create Custom Dict
            context.custom_dict = {}

            # First set up some directories:
            analysis_id = context.destination.get('id')

            # Designated locations for "fmriprep" output and working directory
            fmriprep_output = op.join(context.output_dir, '{}'.format(analysis_id))
            working_dir = op.join(context.output_dir, '{}_work'.format(analysis_id))

            # Store these values in our custom dict
            context.custom_dict['fmriprep_output'] = fmriprep_output
            # The working directory is actually past into the command
            context.config['w'] = working_dir

            # Generate the BIDS directory
            bidsdir = create_bids_directory(context)
            context.custom_dict['bidsdir'] = bidsdir

            # Generate Command Call
            command = fp.create_command(context)

            # Run the call
            fp.run_command(context, command)





        except Exception as e:
            context.log.exception(e)

        finally:

            shutil.copytree(fmriprep_output,os.path.join(context.output_dir,'fmriprep_output'))
            shutil.copytree(working_dir,os.path.join(context.output_dir,'working_dir'))
            shutil.copytree(bidsdir,os.path.join(context.output_dir,'bidsdir'))








