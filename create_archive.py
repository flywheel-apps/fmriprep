import os
import json
import re
import pprint

import flywheel

from create_archive_funcs import get_flywheel_hierarchy, create_bids_hierarchy

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
container_id = str(config_contents['destination']['id'])
container_type = str(config_contents['destination']['type'])


## Create SDK client
print("Create SDK client")
fw = flywheel.Flywheel(api_key)

## Create flywheel hierarchy
print("Create Flywheel Hierarchy")
flywheel_hierarchy = get_flywheel_hierarchy(fw, container_id, container_type)
pprint.pprint(flywheel_hierarchy)

### Create bids hierarchy
print("Create BIDS Hierarchy")
bids_hierarchy, files_lookup = create_bids_hierarchy(flywheel_hierarchy)
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
