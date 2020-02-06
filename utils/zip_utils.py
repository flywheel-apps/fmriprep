"""
Module collection of zip utilities.
"""
from zipfile import ZipFile, ZIP_DEFLATED
import os, os.path as op
import logging
import json
import re

log = logging.getLogger(__name__)

def unzip_all(context, input_zip_filename, output_dir):
    """Unzip the contents of input_zip_filename relative to output_dir,
    All of the files extracted can be tracked with zip_list.
    
    :param context: The gear context with core functionality
    :type context: class: `flywheel.gear_context.GearContext`
    :param input_zip_filename: Zip file to extract relative to output_dir
    :type input_zip_filename: str
    :param output_dir: Root directory to extract input_zip_filename relative to
    :type output_dir: str
    """

    input_zip = ZipFile(input_zip_filename,'r')
    log.info(
        'Unzipping file, {}'.format(input_zip_filename)
    )
    if not context.gear_dict['dry-run']:
        input_zip.extractall(output_dir)

def unzip_config(context, input_zip_filename, output_dir, 
    search_str=r'*_config\.json'):
    """Unzips a filename matching search_str from input_zip_filename relative to the output_dir.
       Returns the contents of that file as a python dictionary. Raises a generic exception otherwise.
       Great for extracting the configuration of previous gears in a sequence. 
    
    :param context: The gear context with core functionality
    :type context: class: `flywheel.gear_context.GearContext`
    :param input_zip_filename: Zip file to search for a file with search_str in its name
    :type input_zip_filename: str
    :param output_dir: Absolute directory to unzip relative to
    :type output_dir: str
    :param search_str: Regular Expression string for the name of the config file
    :type search_str: regex str
    :return: config
    :rtype: dictionary
    """
    config = {}
    zf = ZipFile(input_zip_filename)
    for fl in zf.filelist:
        if not (fl.filename[-1]=='/'): # not (fl.is_dir()):
            # if search_str in filename
            if re.search(search_str, fl.filename):
                try: 
                    json_str = zf.read(fl.filename).decode()
                    config = json.loads(json_str)
                except Exception as e:
                    raise e

                # This corrects for leaving the initial "config" key out
                # of previous gear versions without error
                if 'config' not in config.keys():
                    config = {'config': config}
    
    if len(config) == 0:
        raise Exception(
            'Could not find a configuration within the ' + \
            'exported zip-file, {}.'.format(input_zip_filename)
        )
    return config

def zip_output(context, outputzipname, source_dir, root_dir=None, 
                exclude_files=None):            
    """Compresses the complete output of the gear as designated by root_dir 
    (root_dir defaults to /flywheel/v0/work) and places it in the output 
    directory to be catalogued by the application.
    
    :param context: The gear context with core functionality
    :type context: class: `flywheel.gear_context.GearContext`
    :param outputzipname: complete path of the resultant output zip file
    :type outputzipname: str
    :param source_dir: subdirectory (of <root_dir>) to zip
    :type source_dir: str
    :param root_dir: The root directory to zip relative to, defaults to 
    context.work_dir in the body of the function
    :type root_dir: str, optional
    :param exclude_files: files in /flywheel/v0/workdir/<source_dir> to exclude 
    from the zip file, defaults to None
    :type exclude_files: list, optional
    """

    if exclude_files:
        exclude_from_output = exclude_files
    else:
        exclude_from_output = []

    # if root_dir is not defined, set it to the working directory
    if not root_dir:
        root_dir = context.work_dir

    log.info('Zipping output file {}'.format(outputzipname))
    if not context.gear_dict['dry-run']:
        try:
            os.remove(outputzipname)
        except:
            pass

        os.chdir(root_dir)
        outzip = ZipFile(outputzipname, 'w', ZIP_DEFLATED)
        for root, _, files in os.walk(source_dir):
            for fl in files:
                fl_path = op.join(root,fl)
                # only if the file is not to be excluded from output
                if fl_path not in exclude_from_output:
                    outzip.write(fl_path)
        outzip.close()

def zip_list(zip_filename):
    """Opens the provided zip filename and returns a list of file paths without
    directories.
    
    :param zip_filename: absolute path of zip file
    :type zip_filename: str
    :return: list of relative-path file members
    :rtype: list
    """
    zip_file_list = []
    zf = ZipFile(zip_filename)
    for fl in zf.filelist:
        if not (fl.filename[-1]=='/'): #not (fl.is_dir()):
            zip_file_list.append(fl.filename)
    return zip_file_list