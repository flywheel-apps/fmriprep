# Parse config.json and return strings that can be passed back to the calling
# function.
#
import os
import json
import flywheel

# Parse config file
def generate_license(args):

    license_file = '/opt/freesurfer/license.txt'
    license_info = ''

    # If the config file does not exist then exit
    if not os.path.isfile(args.json_file):
        raise SystemExit('File does not exist: %s!' % args.json_file)

    # Read the config json file
    with open(args.json_file, 'r') as jsonfile:
        config = json.load(jsonfile)

    # OPTION 1: Parse config for license elements
    print('\tChecking for license in Gear Configuration (config.FREESURFER_LICENSE)...')
    if config['config'].get('FREESURFER_LICENSE'):
        license_info = ' '.join(config['config']['FREESURFER_LICENSE'].split()).replace(" ", "\n")
        print('\t-->Generating FREESURFER LICENSE file from Gear Configuration.')

    # OPTION 2: Parse config for license elements
    if not license_info:
        print('\tChecking for license in project info (project.info.FREESURFER_LICENSE)...')
        fw = flywheel.Flywheel(config['inputs']['api_key']['key'])
        project_id = fw.get_analysis(config['destination']['id']).parents.project
        project = fw.get_project(project_id)
        if project.info.get('FREESURFER_LICENSE'):
            license_info = ' '.join(project.info.get('FREESURFER_LICENSE').split()).replace(" ", "\n")
            print('\t-->Generating FREESURFER LICENSE file from Project Info.')

    # Write the license info to a file.
    if license_info:
        with open(license_file, 'w') as lf:
            lf.write(license_info)
        return 0
    else:
        return 1

if __name__ == '__main__':

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--json_file', type=str, default='/flywheel/v0/config.json', dest="json_file", help='Full path to the input json config file.')
    args = ap.parse_args()

    status = generate_license(args)
    os.sys.exit(status)
