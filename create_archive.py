import os
import json
import re
import pprint
import shutil

import flywheel

from create_archive_funcs import get_flywheel_hierarchy, determine_fmap_intendedfor, create_bids_hierarchy

### SETUP
# Define variables
flywheel_basedir = os.environ['FLYWHEEL']
rootdir = os.path.join(flywheel_basedir, 'input', 'bids_dataset')
if not os.path.exists(rootdir):
    os.makedirs(rootdir)

# Read in config file
config_file = os.path.join(flywheel_basedir, 'config.json')
if not os.path.exists(config_file):
    raise Exception('Config file (%s) does not exist' % config_file)
fp = open(config_file, 'r')
config_contents = json.loads(fp.read())
fp.close()
# Get apikey and session ID number from config file
api_key = str(config_contents['inputs']['api_key']['key'])
analysis_id = str(config_contents['destination']['id'])

## Create SDK client
print("Create SDK client")
fw = flywheel.Flywheel(api_key)

## Create flywheel hierarchy
print("Create Flywheel Hierarchy")
flywheel_hierarchy = get_flywheel_hierarchy(fw, analysis_id)
pprint.pprint(flywheel_hierarchy)

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
    os.mkdir(os.path.join(rootdir, sub_dir))
    for ses_dir in bids_hierarchy[sub_dir].keys():
        os.mkdir(os.path.join(rootdir, sub_dir, ses_dir))
        for desc_dir in bids_hierarchy[sub_dir][ses_dir].keys():
            os.mkdir(os.path.join(rootdir, sub_dir, ses_dir, desc_dir))

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

### Use manifest-defined anatomical files if they were provided
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
