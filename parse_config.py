#! /usr/bin/env python2.7
#
# Parse config.json and return strings that can be passed back to the calling
# function.
#

# Parse config file
def parse_config(args):
    import json
    import os

    # If the config file does not exist then exit
    if not os.path.isfile(args.json_file):
        raise SystemExit('File does not exist: %s!' % args.json_file)

    if args.json_file.endswith('manifest.json'):
        manifest=True
    else:
        manifest=False

    # Read the config json file
    with open(args.json_file, 'r') as jsonfile:
        config = json.load(jsonfile)

    # Load defaults from manifest
    if manifest:
        default_config = config['config']
        config = {}
        config['config'] = {}
        for k in default_config.iterkeys():
            config['config'][k] = default_config[k]['default']

    # Parse config for license elements
    if args.l:
        if config['config']['license_key'] and config['config']['license_key'][0] == "*":
            license_key = config['config']['license_key']
        else:
            license_key = "*" + config['config']['license_key']
        print config['config']['license_email'] + "\\n" + config['config']['license_number'] + "\\n " + license_key + "\\n" + config['config']['license_reference'] + "\\n"

if __name__ == '__main__':

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--json_file', type=str, dest="json_file", help='Full path to the input json config file.')
    ap.add_argument('-l', action='store_true', help='Generate License File')
    args = ap.parse_args()

    parse_config(args)
