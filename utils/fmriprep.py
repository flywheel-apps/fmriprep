#!/usr/bin/env python3

import utils.common as cm
import logging
from collections import OrderedDict

log = logging.getLogger(__name__)

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


valid_output_spaces=['MNI152Lin',
                     'MNI152NLin2009cAsym',
                     'MNI152NLin6Asym',
                     'MNI152NLin6Sym',
                     'MNIInfant',
                     'MNIPediatricAsym',
                     'NKI',
                     'OASIS30ANTs',
                     'PNC',
                     'WHS',
                     'fsLR',
                     'fsaverage',
                     'T1w',
                     'anat',
                     'fsnative',
                     'func',
                     'bold',
                     'run',
                     'boldref',
                     'sbref']


def str_2_num(string):

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


def validate_output_spaces(output_spaces):
    # Split output spaces by space
    spaces = output_spaces.split()
    
    # Loop though
    for space in spaces:
        # remove any cohort and res information
        template = space.split(':')[0]

        log.debug('space: {}'.format(space))
        log.debug('template: {}'.format(template))
        
        
        # Verify that the template is one that fmriprep will recognize
        # See valid_output_spaces defined above (Possibly a better way to get this list?)
        if template not in valid_output_spaces:
            log.debug('Template is invalid')
            raise Exception('Output space {} is not a valid space.'.format(template))
        
        log.debug('Template is valid')
        
def create_command(context):
    # Extract some input settings that are inputs
    try:
        cmd = ['/usr/local/miniconda/bin/fmriprep']
        paramlist = OrderedDict()
        for key in fmriprep_options:
            if key in context.config:
                log.debug('{}: {}'.format(key, context.config[key]))
                
                # If key is output spaces, we have to do some custom checks
                if key == 'output-spaces':
                    validate_output_spaces(context.config[key])
                
                if context.config[key] == "" or context.config[key] is None:
                    log.debug('Skipping {}\n'.format(key))
                    continue

                paramlist[key] = context.config[key]

        command = cm.build_command_list(cmd, paramlist)
        command.append('--fs-license-file={}'.format(context.get_input_path('freesurfer-license')))

        command.append(context.gear_dict['bids_path'])
        command.append(context.gear_dict['output_analysisid_dir'])
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



