#!/usr/bin/env python3
import os, os.path as op
import json
import flywheel
import utils.common as cm
import logging
from collections import OrderedDict
import glob
import utils.zip_utils as zp
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

container = '[flywheel/fmriprep]'

fmriprep_options = OrderedDict({"h": bool,
                                "version": bool,
                                "skip_bids_validation": bool,
                                "participant_label": str,
                                "t": str,
                                "echoidx": str,
                                "nthreads": int,
                                "omp-nthreads": int,
                                "mem-mb": float,
                                "low-mem": bool,
                                "use-plugin": bool,
                                "anat-only": bool,
                                "boilerplate": bool,
                                "error-on-aroma-warnings": bool,
                                "v": bool,
                                "ignore": ['fieldmaps', 'slicetiming', 'sbref'],
                                "longitudinal": bool,
                                "t2s-coreg": bool,
                                "output-spaces": str,
                                "bold2t1w-dof": [6, 9, 12],
                                "force-bbr": bool,
                                "force-no-bbr": bool,
                                "medial-surface-nan": bool,
                                "dummyscans": int,
                                "aroma-melodic-dimensionality": int,
                                "return-all-components": bool,
                                "fd-spike-threshold": [float, int],
                                "dvars-spike-threshold": [float, int],
                                "skull-strip-template": str,
                                "skull-strip-fixed-seed": str,
                                "fmap-bspline": bool,
                                "fmap-no-demean": bool,
                                "use-syn-sdc": bool,
                                "force-syn": bool,
                                "fs-license-file": str,
                                "no-submm-recon": bool,
                                "cifti-output": bool,
                                "fs-no-reconall": bool,
                                "w": str,
                                "resource-monitor": bool,
                                "reports-only": bool,
                                "run-uuid": str,
                                "write-graph": bool,
                                "stop-on-first-crash": bool,
                                "notrack": bool,
                                "sloppy": bool})


def str_2_num(string):
    log = logging.getLogger()

    try:
        if string.find('.'):
            num = float(string)
        else:
            num = int(string)
    except:
        log.warning('UNABLE TO CONVERT {} TO TYPE INT OR FLOAT'.format(string))
        num = string

    return num


def check_type(val, expected):
    log = logging.getLogger()

    # if the expected value is a type (int, bool, etc)
    if type(expected) == type:

        # and the value does not match that type
        if not isinstance(val, expected):

            # if the expected value is a string
            if expected == str:

                # Warn the user that we're typecasting
                log.warning('VALUE {} IS EXPECTED TO BE OF TYPE {}, BUT IS TYPE {}.  CONVERTING.').format(val, expected,
                                                                                                          type(val))

                # And try to typecast, but don't fail if it doesn't work.  Pass it out and see what happens:
                try:
                    val = '{}'.format(val)
                except:
                    log.warning('WARNING, TYPCASTING {} to {} FAILED'.format(val, expected))

            # If the expected value is a bool
            elif expected == bool:

                # If the input value is a string
                if isinstance(val, str):

                    # If it's the string "true"
                    if val.lower() == 'true':
                        # set it to true
                        val = True
                    # if it's the string "false"
                    elif val.lower() == 'false':
                        # set it to false
                        val = False

                # If it's a number, try to bool it
                else:
                    try:
                        val = bool(val)
                    except:
                        log.warning('NO BOOL EQUIVALENT FOR {}'.format(val))

            # If we're expecting type int or type float:
            elif expected == int or expected == float:

                # Try to convert it
                val = str_2_num(val)

                # We're only really concerned if a type "int" is a "float":
                if expected == int and isinstance(val, float):
                    log.warning('VALUE {} IS {} WHEN EXPECTED {}'.format(val, float, int))

            else:
                log.warning('UNKNOWN TYPE {} WITH VAL'.format(expected, val))

        # Otherwise we're comparing a value, not a type
        else:
            if type(expected):
                pass


def validate(context):
    # log = context.log
    # for key in fmriprep_options:
    #     expected = fmriprep_options[key]
    #     if key in context.config:
    #         if isinstance(key,list):
    #
    #         if type(key) == type:
    #             if not isinstance(context.config[key],expected):
    #                 if key == str:
    #                     try:
    #                         log.warning('Config option {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))
    #                         log.info('Attempting to convert')
    #                         context.config[key]='{}'.format(context.config[key])
    #                     except:
    #                         raise Exception('Unable to convert {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))')
    #
    #                 elif key == bool:
    #                     try:
    #                         log.warning('Config option {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))
    #                         log.info('Attempting to convert')
    #                         if context.config[key]=='true':
    #                             context.config[key] == True
    #                         elif context.config[key]=='false':
    #                             context.config[key] == False
    #                     except:
    #                         raise Exception('Unable to convert {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))')
    #
    #                 elif key == int:
    #                     try:
    #                         log.warning('Config option {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))
    #                         log.info('Attempting to convert')
    #                         context.config[key] = int(context.config[key])
    #
    #                     except:
    #                         raise Exception('Unable to convert {}: {} needs to be type {}'.format(key,context.config[key],fmriprep_options['key']))')
    #
    #                 elif key == int:
    #                     try:
    #                         log.warning('Config option {}: {} needs to be type {}'.format(key, context.config[key],
    #                                                                                       fmriprep_options['key']))
    #                         log.info('Attempting to convert')
    #                         context.config[key] = int(context.config[key])
    #
    #                     except:
    #                         raise Exception(
    #                             'Unable to convert {}: {} needs to be type {}'.format(key, context.config[key],
    #                                                                                   fmriprep_options['key']))

    pass


def create_command(context):
    # Extract some input settings that are inputs
    try:
        cmd = ['/usr/local/miniconda/bin/fmriprep']
        paramlist = OrderedDict()
        for key in fmriprep_options:
            if key in context.config:
                context.log.info('{}: == str: {}'.format(key, context.config[key]==str))
                context.log.info('{}: {}'.format(key, context.config[key]))
                context.log.info('{} == "": {}'.format(key, context.config[key] == ""))
                context.log.info('{} is None: {}\n'.format(key, context.config[key] is None))

                if context.config[key] == "" or context.config[key] is None:
                    context.log.info('Skipping {}\n'.format(key))
                    continue

                paramlist[key] = context.config[key]

        command = cm.build_command_list(cmd, paramlist)
        command.append('--fs-license-file={}'.format(context.get_input_path('freesurfer-license')))

        command.append(context.custom_dict['bidsdir'])
        command.append(context.custom_dict['fmriprep_output'])
        command.append('participant')
    except:
        raise Exception('Unable to generate command list')

    return command


def run_command(context, command):
    try:
        cm.exec_command(context, command)
    except:
        raise Exception('Unable to run command')

    pass


def cleanup_output(context):
    pass
#     log = logging.getLogger()
#
#     # Look for the output html file
#     html_file = glob.glob(op.join(context.custom_dict['fmriprep_output'],'fmriprep','sub-*.html'))
#
#     # If it's not there, error out
#     if len(html_file)==0:
#         log.error('NO FMRIPREP OUTPUT FOUND')
#         raise Exception('No fmriprep output found')
#
#     # Otherwise take the file and extract the subject ID
#     html_file = html_file[0]
#     html_dir, html_base = os.path.split(html_file)
#     sub_id = os.path.splitext(html_base)[0]
#     analysis_id = context.destination.get('id')
#
#     # Get the html report and zip the folder
#     log.info("{}  Converting output html report...".format(container))
#     output_html_file = os.path.join(context.output_dir,'{}_{}.html.zip'.format(sub_id,analysis_id))
#     figure_dir = os.path.join(html_dir,sub_id,'figures')
#
#     index = os.path.join(html_dir,'index.html')
#     shutil.copy(html_file, index)
#     outzip = ZipFile(output_html_file, 'w', ZIP_DEFLATED)
#     # for root, _, files in os.walk(figure_dir):
#     #     for fl in files:
#     #         fl_path = op.join(root, fl)
#     #         # only if the file is not to be excluded from output
#     #         if fl_path not in exclude_from_output:
#     #             outzip.write(fl_path)
#     outzip.write(index)
#     outzip.write(figure_dir)
#     outzip.close()
#
#     log.info("{}  HTML report converted.".format(container))
#
#
#     # Look for files/folders to preserve from the working DIRECTORY
#     work_file_zip = os.path.join(context.output_dir,'fmriprep_work_selected_{}_{}.zip'.format(sub_id,analysis_id))
#
#     if context.config['intermediate-files']:
#         log.info("{}  Archiving selected intermediate files...".format(container))
#
#         outzip = ZipFile(work_file_zip,'w', ZIP_DEFLATED)
#         int_files = context.config['intermediate-files'].split()
#         for file in int_files:
#             path = os.path.join(context.config['w'],file)
#             if os.path.exists(path):
#                 outzip.write(path)
#
# zip $work_file_zip
# `find. - type
# f - name
# "$f"
# `
# done
# fi
#
# if [[-n "$config_intermediate_folders"]]; then
# echo
# "$CONTAINER  Archiving selected intermediate folders..."
# cd
# "$WORKING_DIR"
# for f in $config_intermediate_folders; do
# zip $work_file_zip
# `find. - type
# d - name
# "$f"
# `
# done
# fi
#
# # Generate zipped output of fmriprep
# cd
# "$GEAR_OUTPUT_DIR"
# echo
# "$CONTAINER  generating zip archive from outputs..."
# time
# zip - q - r
# "$GEAR_OUTPUT_DIR" / fmriprep_
# "$SUB_ID"
# _
# "$ANALYSIS_ID" $(basename "$FMRIPREP_OUTPUT_DIR")
#
# if [[ $config_save_intermediate_work == 'true']]; then
# echo
# "$CONTAINER  generating zip archive from intermediate work files..."
# cd
# "$GEAR_OUTPUT_DIR"
# time
# zip - q - r
# "$GEAR_OUTPUT_DIR" / fmriprep_work_
# "$SUB_ID"
# _
# "$ANALYSIS_ID" $(basename "$WORKING_DIR")
# fi
# chmod - R
# 777 $GEAR_OUTPUT_DIR
#
# elif [[ $config_save_outputs == 'true']]; then
# echo
# "$CONTAINER  Error occurred. Config 'save_outputs' set to true. Zipping up outputs."
# cd
# "$GEAR_OUTPUT_DIR"
# time
# zip - q - r
# "$GEAR_OUTPUT_DIR" / debug_fmriprep_
# "$ANALYSIS_ID"  $(basename "$FMRIPREP_OUTPUT_DIR")
# time
# zip - q - r
# "$GEAR_OUTPUT_DIR" / debug_fmriprep_work_
# "$ANALYSIS_ID" $(basename "$WORKING_DIR")
# chmod - R
# 777 $GEAR_OUTPUT_DIR
#
# else
# echo
# "$CONTAINER  Errors encountered during execution. Save outputs config not set. Cleaning up and exiting."
# fi
#
# # Clean up
# rm - rf
# "$WORKING_DIR"
# rm - rf
# "$FMRIPREP_OUTPUT_DIR"
#
# echo - e
# "Wrote: `ls -lh $GEAR_OUTPUT_DIR`"
#
# exit $FMRIPREP_EXITSTATUS
