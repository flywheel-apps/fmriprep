import os
import re
import sys

#from jsonschema import validate

from datetime import datetime


from pprint import pprint

#### Define functions
def merge_classification(dst, src):
    if src is None:
        return

    for key in src.keys():
        if key not in dst:
            dst[key] = []

        for val in src[key]:
            if val not in dst[key]:
                dst[key].append(val)

def has_classification_value(classification, aspect, value):
    return value in classification.get(aspect, [])

def get_anatomy_measurement(classification):
    if not has_classification_value(classification, 'Intent', 'Structural'):
        return None

    measurement = classification.get('Measurement', [])
    if 'T1' in measurement:
        return 'T1'
    if 'T2' in measurement:
        return 'T2'

    return None

def get_flywheel_hierarchy(fw, analysis_id):
    """
        Takes fw client, a container id and container_type as input

        analysis_id: the ID of the analysis

        Returns the flywheel tree

        example:

        {
        "<project_id>": {
           "<session_id>": {
                    "label": "ses11123",
                    "subject_code": "001",
                    "acquisitions": {
                        "<acquisition_id1>": {
                            "label": "T1 MPRAGE",
                            "created": datetime.datetime(2017, 09, 19, 14, 39, 58.721)
                            "files": ['T1.nii.gz',]
                            "classification": {
                                "Intent": ["Structural"],
                                "Measurement": ["T1"]
                            },
                            "type": ['nifti'],
                            "infos": [{}]
                    },
                        "<acquisition_id2>": {
                            "label": "task123123",
                            "created": datetime.datetime(2017, 09, 19, 14, 39, 58.721)
                            "files": ['fmri.nii.gz'],
                            "classification": {
                                "Intent": ["Functional"]
                            },
                            "type": ['nifti'],
                            "infos": [{'RepetitionTime': 2.3}]
                    }
                }
            }
        }
    }


    """
    # Get analysis
    analysis = fw.get_analysis(analysis_id)
    # Get container type and id from
    container_type = analysis.parent.type
    container_id = analysis.parent.id

    # Determine if ID is a project or a session ID
    if container_type == 'project':
        # Get list of sessions within project
        project_sessions = fw.get_project_sessions(container_id)
        project_id = container_id
    elif container_type == 'session':
        # If container type is a session, get the specific session
        session = fw.get_session(container_id)
        # Place the single session within a list to iterate over (mirrors project_sessions above)
        project_sessions = [session]
        project_id = session.get('project')
    else:
        print("Container ID %s is not associated with a project or a session" % container_id)
        raise Exception

    # Create dictionary to place flywheel hierarchy info
    flywheel_hierarchy = {project_id: {}}
    # Iterate over every session within project
    for p_ses in project_sessions:
        # Get session ID, session label and subject code to place in dictionary
        session_id = p_ses.get('_id')
        # If no subject code present, continue...
        if not ('code' in p_ses['subject'].keys()):
            print('Subject code is not present for session: %s' % session_id)
            print('Moving on')
            continue
        flywheel_hierarchy[project_id][session_id] = {'label': p_ses.get('label'),
                                                     'subject_code': p_ses['subject']['code'],
                                                     'acquisitions': {}
                                                     }
        # Get all acquisitions within session
        session_acqs = fw.get_session_acquisitions(session_id)
        # Iterate over all acquisitions within session
        for s_acq in session_acqs:
            # Get acquistiion ID and place in dictionary
            acq_id = s_acq.get('_id')
            # Get true acquisition in order to get meta information
            acq = fw.get_acquisition(acq_id)
            # Initiate acquisition information
            flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id] = {
                    'label': acq.get('label'),
                    'created': acq.get('created'),
                    'files': [],
                    'classification': {},
                    'infos': []
                    }
            # Iterate over all files within acquisition
            for f in acq['files']:
                filename = f['name']
                ## Sometimes classification is not present - if not, assign classification value to be None
                classification = f.get('classification')
                # Get type - we are only concerned with nifti files that contain the BIDS side car meta information
                ftype = f.get('type')
                # Get info from file
                info = f.get('info')
                if ftype == 'nifti' and classification:
                    flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['files'].append(filename)
                    merge_classification(flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['classification'], classification)
                    flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['infos'].append(info)

            # If no nifti files found for an acquisition, remove it
            if not flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['files']:
                del flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]

    return flywheel_hierarchy


def populate_bids_hierarchy(bids_filepath, bids_hierarchy):

    # split up path, participant, session, 'anat'/'func', filename
    participant, session, subdir, filename = bids_filepath.split('/')

    ## Populate bids_hierarchy
    if participant not in bids_hierarchy:
        bids_hierarchy[participant] = {}
    if session not in bids_hierarchy[participant]:
        bids_hierarchy[participant][session] = {}
    if subdir not in bids_hierarchy[participant][session]:
        bids_hierarchy[participant][session][subdir] = []

    bids_hierarchy[participant][session][subdir].append(filename)

    return bids_hierarchy


def make_bids_spec(desc, flywheel_val, label_type):
    """ Asserts if label already conforms to the BIDS spec, if not
    converts the 'flywheel_val' variable into a BIDS allowable string

    desc: string describing the type of label
            ex: sub-
                ses-
                acq-
                ce-
                task-
    flywheel_val: the value of the Flywheel string such as the subject code
            ex: amyg_s11_ses2_pcolA
                session4
                s004

    valtype: the label type, is either 'label' or 'index'
            label indicates only alphanumeric values are allowed
            index indicates only numeric values are allowed

    returns: the label within BIDS format
            ex: sub-control001
                ses-123
                acq-t1w

    """
    # If BIDS 'label', then any letter and number is allowed
    if label_type == 'label':
        # Define regex to check for BIDS compliance
        regex = '[0-9a-zA-Z]+$'
        # Extract BIDS compliant values, incase the flywheel_val is NOT BIDS
        extract_values = ''.join(ch for ch in flywheel_val if ch.isalnum())
    # if BIDS 'index', then any number is allowed
    if label_type == 'index':
        # Define regex to check for BIDS compliance
        regex = '[0-9]+$'
        # Extract BIDS compliant values, incase the flywheel_val is NOT BIDS
        extract_values = re.sub(r'\D+', '', flywheel_val)
    # Check if flywheel value already conforms to bids spec
    pattern = desc + regex
    already_bids = re.match(pattern, flywheel_val)
    if already_bids:
        label_bids = flywheel_val
    # Otherwise, grab all permissible values from subject_code and make that the participant
    else:
        label_bids = desc + extract_values
    return label_bids


def check_meta_info(f, b, info):
    """ Asserts all required

        f: Flywheel filename of nifti file (used for print errors/warnings)
        b: BIDS filename of nifti file
        info: meta info attached to nifti file in Flywheel system

    """
    # Dictionary of required meta information
    #   keys: character to search for in filename
    #   values: list of required values in info field
    json_reqs = {
        'T1w.nii': [], # No required info, but there are 'recommended' values
        'T2w.nii': [], # No required info, but there are 'recommended' values
        'bold.nii': ['RepetitionTime','TaskName'],
        'sbref.nii': [], # No required info
        'phasediff.nii': ['EchoTime1', 'EchoTime2'],
        'phase1.nii': ['EchoTime'],
        'phase2.nii': ['EchoTime'],
        'fieldmap.nii': ['Units'],
        'epi.nii':  ['PhaseEncodingDirection','TotalReadoutTime'],
        'magnitude.nii': [], # No required info
        'magnitude1.nii': [], # No required info
        'magnitude2.nii': [], # No required info
        }
    # Initiate variable
    reqvals_notpresent = False

    # Deterine the type of file by looking for string in BIDS filename
    found = [key for key in json_reqs.keys() if key in b]
    # If the type of file was found
    if found:
        # Get required values for JSON based on the filetype
        required_vals = json_reqs.get(found[0])
        # Iterate over the required_vals
        for req_val in required_vals:
            # If req_val not in the meta info
            if not (req_val in info):
                print("Required meta information (%s) not present for file: %s" % (req_val,f))
                reqvals_notpresent = True
    # Else print, I didn't recognize the file type...
    else:
        print("Could not identify file type")

    return reqvals_notpresent



def determine_fmap_intendedfor(flywheel_hierarchy):
    """ """
    # initialize dictionary
    fmaps_intendedfor = {}
    # Determine if fieldmaps are present within flywheel hierarchy
    # Participant Directory
    for project in flywheel_hierarchy.keys():
        fmaps_intendedfor[project] = {}
        # Session Directory
        for session_id in flywheel_hierarchy[project].keys():
            fmaps_intendedfor[project][session_id] = {}
            # initialize lists
            fmaps_time = {'i': [], 'j': [], 'k': [], 'i-': [], 'j-': [], 'k-': []}
            fmaps_filenames = {'i': [], 'j': [], 'k': [], 'i-': [], 'j-': [], 'k-': []}
            funcs = []

            # Iterate over acquisitions
            for acq_id in flywheel_hierarchy[project][session_id]['acquisitions'].keys():
                if has_classification_value(flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['classification'], 'Intent', 'Fieldmap'):
                    # Get PhaseEncodingDirection
                    pe_dir = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['infos'][-1].get('PhaseEncodingDirection')
                    if pe_dir:
                        fmaps_time[pe_dir].append(
                            flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['created'],
                        )
                        fmaps_filenames[pe_dir].append(
                            os.path.join(
                                acq_id,
                                flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['files'][-1]
                                )
                        )
                elif has_classification_value(flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['classification'], 'Intent', 'Functional'):
                    # Get PhaseEncodingDirection
                    pe_dir = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['infos'][-1].get('PhaseEncodingDirection')
                    if pe_dir:
                        # Flip the pe_dir so it indicates which pe the fieldmap should be for the functional image...
                        if '-' in pe_dir: pe_dir_flipped = pe_dir[0]
                        else: pe_dir_flipped = pe_dir + '-'

                        # Add timestamp, pathname, pe_dir_flipped
                        funcs.append(
                                [
                                    flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['created'],
                                    os.path.join(
                                        acq_id,
                                        flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['files'][-1]
                                        ),
                                    pe_dir_flipped
                                    ]
                                )
                else:
                    pass

            ###
            # Determine which fieldmaps go with which functional datasets
            if funcs:
                # Initialize a dictionary with empty lists
                all_fmap_filenames = [x for alist in fmaps_filenames.values() for x in alist]
                tmp = dict.fromkeys(all_fmap_filenames)
                for key in tmp.keys():
                    tmp[key] = []

                # Iterate over each functional image, determine which fmap timepoint it is closest to...
                for func_time, func_filename, func_pedir_flipped in funcs:
                    if fmaps_filenames[func_pedir_flipped]:
                        # Get the func time
                        FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
                        ft = check_time(func_time, FMT)
                        # Determing the fieldmap that the functional image is closest to...
                        fmap_time = min(fmaps_time[func_pedir_flipped], key=lambda x: abs(check_time(x, FMT)-ft))
                        fmap_idx = fmaps_time[func_pedir_flipped].index(fmap_time)
                        fmap_filename = fmaps_filenames[func_pedir_flipped][fmap_idx]
                        tmp[fmap_filename].append(func_filename)

                # add tmp to dictionary
                fmaps_intendedfor[project][session_id].update(tmp)

    return fmaps_intendedfor


def check_time(t, fmt):
    if isinstance(t, str):
        return datetime.strptime(func_time, fmt)
    else:
        return t

def create_bids_hierarchy(flywheel_hierarchy, fieldmap_intendedfor):
    """
    """

    # Keep track of what file within the Flywheel hierarchy goes with what file within BIDS hierarchy
    #    list of paired lists [['/flywheel/hierarchy/file.nii', '/bids/hierarchy/file.nii'], ... ]
    files_lookup = []
    ## Traverse over Flywheel hierarchy to generate BIDS hierarchy
    bids_hierarchy_tmp = {}
    # Participant Directory
    for project in flywheel_hierarchy.keys():
        # Session Directory
        for session_id in flywheel_hierarchy[project].keys():
            # Iterate over acquisitions
            for acq_id in flywheel_hierarchy[project][session_id]['acquisitions'].keys():

                # Get meta info for BIDS
                subject_code = flywheel_hierarchy[project][session_id]['subject_code']
                session_label = flywheel_hierarchy[project][session_id]['label']
                classification = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['classification']

                # Get nifti file
                # NOTE! If there are multiple nifti files within the one acquisition,
                #   take the last file in the list, under the assumption that it is the most recent
                nifti_filename = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['files'][-1]
                # Define the extension (.nii or .nii.gz)
                if '.nii.gz' in nifti_filename:
                    extension = '.nii.gz'
                else:
                    extension = '.nii'
                # Define the path of the desired nifti file within the flywheel hierarchy
                flywheel_filepath = os.path.join(project, session_id, acq_id, nifti_filename)

                ### Making BIDS
                # Generate the participant information (i.e. sub-001)
                participant_bids = make_bids_spec('sub-', subject_code, 'label')
                # Generate the session information (i.e. ses-1234)
                session_bids = make_bids_spec('ses-', session_label, 'label')
                # Get acquistion label
                acquisition_label = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['label']

                ### HANDLE T1w/T2w images
                anatomy_measurement = get_anatomy_measurement(classification)

                if anatomy_measurement:
                    # Define dirname
                    bids_dirname = 'anat'
                    # Create the new name of the file that conforms to bids spec
                    if anatomy_measurement == 'T1':
                        desc = 'T1w'
                    if anatomy_measurement == 'T2':
                        desc = 'T2w'
                    bids_filename = '%s_%s_%s%s' % (participant_bids, session_bids, desc, extension)

                ### HANDLE Functional images
                elif has_classification_value(classification, 'Intent', 'Functional'):
                    # Define dirname
                    bids_dirname = 'func'
                    # Use the acquistion label as the task name (i.e. task-balloontask or task-rest)
                    # If rest is in the acquisition label, will classify as resting state
                    if 'rest' in acquisition_label.lower():
                        taskname = 'task-rest'
                    # Otherwise, the taskname will take all permitted values from acquisition_label
                    else:
                        taskname = make_bids_spec('task-', acquisition_label, 'label')
                    # check if sbref is in the acquistion label, if so, use sbref as filename description
                    if 'sbref' in acquisition_label.lower():
                        bids_func_desc = 'sbref'
                        # remove sbref from taskname, if present
                        pattern = re.compile(bids_func_desc, re.IGNORECASE)
                        taskname = re.sub(pattern, '', taskname)
                    else:
                        bids_func_desc = 'bold'
                    # Create the new name of the file that conforms to bids spec
                    bids_filename = '%s_%s_%s_%s%s' % (participant_bids, session_bids, taskname, bids_func_desc, extension)

                ### HANDLE Fieldmap images
                elif has_classification_value(classification, 'Intent', 'Fieldmap'):
                    # Define dirname
                    bids_dirname = 'fmap'

                    #### Making BIDS
                    # determine type of fieldmap from acquisition label
                    #
                    # Possible field maps
                    # (1)  phasediff & magnitude (2 images)
                    #   _phasediff & _magnitude1/_magnitude2
                    # (2) 2 phase images & 2 magnitude images
                    #  _phase1/_phase2 & _magnitude1/_magnitude2
                    # (3) single real fieldmap NOTE!!! NOT HANDLING THIS CASE - not sure how!!
                    #  _magnitude & _fieldmap
                    # (4) multiple phase encoded directions
                    #  _dir-<dirlabel>_epi where dirlabel is AP/PA/LR/RL etc...
                    # NOTE: all files above need a sidecar json except for magnitude images
                    acquisition_label_lower = acquisition_label.lower()
                    # (1) If phasediff
                    if 'phasediff' in acquisition_label_lower:
                        bids_field_desc = 'phasediff'
                    # (2) if phase
                    elif 'phase' in acquisition_label_lower:
                        bids_field_desc = 'phase'
                    # (1&2) if magnitude
                    elif 'mag' in acquisition_label_lower:
                        bids_field_desc = 'magnitude'
                    # (4) If spin echo
                    elif 'spinecho' in acquisition_label_lower:
                        ## Determine dir_label
                        re_match = re.search('AP|PA|LR|RL', acquisition_label)
                        if re_match:
                            dir_label = acquisition_label[re_match.start():re_match.end()]
                        else:
                            dir_label = 'unknown'
                        bids_field_desc = 'dir-%s_epi' % dir_label
                    else:
                        print('WARNING: Cannot determine fieldmap type for file: %s' % flywheel_filepath)
                        print('Moving on...')
                        continue
                    # Create the new name of the file that conforms to bids spec
                    bids_filename = '%s_%s_%s%s' % (participant_bids, session_bids, bids_field_desc, extension)
                else:
                    continue

                # NOTE: If 'run%d' at the end of the acquisition label -- honor that number and change to BIDS format
                # 'task-foorun1' -> 'task-foo_run-1'
                bids_filename = re.sub(r'(run)(\d)(_)', r'_\1-\2\3', bids_filename)

                ### Now append directory
                # Define the path of the new nifti file within the bids hierarchy
                bids_filepath = os.path.join(participant_bids, session_bids, bids_dirname, bids_filename)
                # Append to file lookup
                files_lookup.append([flywheel_filepath, bids_filepath])
                # Populate bids hierarchy
                populate_bids_hierarchy(bids_filepath, bids_hierarchy_tmp)

    ### Iterate over files looking for duplicates and add run numbers if necessary
    for sub_dir in bids_hierarchy_tmp.keys():
        for ses_dir in bids_hierarchy_tmp[sub_dir].keys():
            for desc_dir in bids_hierarchy_tmp[sub_dir][ses_dir].keys():
                bids_files = bids_hierarchy_tmp[sub_dir][ses_dir][desc_dir]
                # Get a list of duplicate filenames that need to be renamed
                duplicates = [x for x in set(bids_files) if bids_files.count(x) > 1]
                #### Go through each duplicate, find the flywheel file and rename
                for duplicate in duplicates:
                    # Identify the corresponding flywheel files that have bids duplicates
                    flywheel_files = [item[0] for item in files_lookup \
                                  if os.path.basename(item[1]) == duplicate]
                    # Get timing information about the duplicate files in order to assign run-<index>
                    created = []
                    for ff in flywheel_files:
                        project_id, session_id, acq_id, filename = ff.split('/')
                        # list of tuples [(timestamp, flywheel_filename), ...]
                        created.append(
                                    (flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['created'], ff)
                                    )
                    # Sort list of files based on timestamp which is first item in tuple
                    created.sort(key=lambda x: x[0])
                    # Go through the created list and assign the run counts
                    for idx in range(len(created)):
                        # Get flywheel filename
                        fff = created[idx][1]
                        # Get corresponding bids filename
                        for idxx in range(len(files_lookup)):
                            if files_lookup[idxx][0] == fff:
                                bbb = files_lookup[idxx][1]
                                break
                        # Now rename bids filename (variable name: 'bbb')
                        # If duplicate _magnitude or _phase - add a number after description
                        #   _magnitude.nii.gz => _magnitude1.nii.gz
                        bbb_new = re.sub(r'(_)(magnitude|phase)(.nii)', r'\g<1>\g<2>%d\g<3>' % (idx+1), bbb)
                        # If duplicate T1w, T2w, bold, sbref, - add run number
                        #    sub-<label>_ses-<label>_T1w.nii.gz
                        #               =>
                        #        sub-<label>_ses-<label>_run-<index>_T1w.nii.gz
                        bbb_new = re.sub(r'(_)(bold|T1w|T2w)(.nii)', r'_run-%d\g<1>\g<2>\g<3>' % (idx+1), bbb_new)
                        # Update the files_lookup information
                        files_lookup[idxx][1] = bbb_new

    ### Create new bids_hierarchy with all unique filenames
    bids_hierarchy = {}
    for f,b  in files_lookup:
        populate_bids_hierarchy(b, bids_hierarchy)

    # Use the "info" field to create JSON file
    reqvals_notpresent = 0
    json_files = []
    ### Create JSON files
    for f,b in files_lookup:
        # Get meta information to create json file
        project_id, session_id, acq_id, filename = f.split('/')

        # Get meta info
        info = flywheel_hierarchy[project_id][session_id]['acquisitions'][acq_id]['infos'][-1]

        # If bold file, need to get taskname from filename, taskname is not in 'info'
        if '_bold.nii' in b:
            # Place TaskName into the file -- just using Acquisition Label
            #    NOTE: it is not clear within the bids spec if the Task Name can have any character
            #       it seems like there is a distinction between task NAME and task LABEL where
            #       task LABEL has restrictions but task NAME does not...
            # To be safe, I'll make it the TASK LABEL
            #NOT THIS:meta_info['TaskName'] = flywheel_hierarchy[project][session_id]['acquisitions'][acq_id]['label']
            # Pull task label out of bids filename
            find_taskname = re.search('task-[a-zA-Z0-9]+', b)
            taskname = b[find_taskname.start()+5:find_taskname.end()]
            info['TaskName'] = taskname

        # If a fieldmap, determine which files this fieldmap is intended for...
        if 'fmap' in b:
            if fieldmap_intendedfor:
                try:
                    # Get the flywheel names of all of the functional files that the fieldmap is intended for...
                    funcs_f = fieldmap_intendedfor[project_id][session_id]['%s/%s' % (acq_id,filename)]
                    # Now get the bids name of that flywheel file...
                    funcs_b = []
                    for ff in funcs_f:
                        # ff is actually the acq_id/flywheel_filename,make it so that it's the full flywheel pathname
                        fff = os.path.join(project_id, session_id, ff)
                        # Get bids filename
                        for flyfile, bidsfile in files_lookup:
                            if flyfile == fff:
                                part, ses, subdir, fname = bidsfile.split('/')
                                # Append filename to th elist
                                funcs_b.append(os.path.join(subdir,fname))
                    info['IntendedFor'] = funcs_b
                except KeyError:
                    pass

        ## Check required information from file 'info' based on BIDS filetype
        reqvals_notpresent += check_meta_info(f, b, info)
        # Save meta information to JSON file
        json_filename = re.sub(r'(.nii.gz|.nii)', r'.json', b)
        # If info present, add JSON info
        if info:
            # Add JSON blob and JSON filename to json_files
            json_files.append([info, json_filename])
            # Add json_filename to bids_hierarchy
            populate_bids_hierarchy(json_filename, bids_hierarchy)


    # If the required values are not present, can't run fmriprep
    if reqvals_notpresent:
        print('Required meta information is not present')
        print('Run the dcm2niix gear to generate meta info for nifti files')
        sys.exit(1)

    # Append json_files to files_lookup
    return bids_hierarchy, files_lookup + json_files


def validate_flywheel_hierarchy(flywheel_hierarchy):

    # TODO! Check if acquisitions were found -- this needs to be checked for every session...
    if not ('acquisitions' in flywheel_hierarchy[project][session_id]):
        print('No nifti files were found in session' % session_id)
        print('Nothing to do')
        sys.exit(0)


