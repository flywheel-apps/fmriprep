import pprint

from create_archive_funcs import create_bids_hierarchy


def run_print_test(description, flywheel_hierarchy, print_files_lookup=False):
    print("/////////////////////////////////////////")
    print(description)
    print("Flywheel Hierarchy")
    pprint.pprint(flywheel_hierarchy)
    bids_hierarchy, files_lookup = create_bids_hierarchy('dummy', flywheel_hierarchy, test_bool=True)
    print("BIDS Hierarchy")
    pprint.pprint(bids_hierarchy)

    if print_files_lookup:
        pprint.pprint(files_lookup)


## Test #1
description = "One subject, one session -- NOT BIDS"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd72348573476fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy)

## Test #2
description = 'one subject, multiple sessions -- NOT BIDS'
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "session1",
                "subject_code": "Jane Doe 1",
                "acquisitions": {
                    "623765726354fsd7263476s": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "48375jdfkjdsf983498234": {
                "label": "session2",
                "subject_code": "Jane Doe 1",
                "acquisitions": {
                    "623112765726354fsdfjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
                    }}
run_print_test(description, flywheel_hierarchy)



## Test #3
description = "multiple subjects, one session each (same session label)"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "session1",
                "subject_code": "s001",
                "acquisitions": {
                    "623765726354fsd7263476s": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "48375jdfkjdsf983498234": {
                "label": "session1",
                "subject_code": "s002",
                "acquisitions": {
                    "623112765726354fsdfjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}
                    }}
run_print_test(description, flywheel_hierarchy)



## Test #4
description = "multiple subjects, multiple sessions"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "123u3473485": {
                "label": "session1",
                "subject_code": "s001",
                "acquisitions": {
                    "623765476s": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "123445345435": {
                "label": "session2",
                "subject_code": "s001",
                "acquisitions": {
                    "62376ddddds": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62y6667777jh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "483222234": {
                "label": "session1",
                "subject_code": "s002",
                "acquisitions": {
                    "612312323423jh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62377sdkjfhaiueyr666764jh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "222880234": {
                "label": "session2",
                "subject_code": "s002",
                "acquisitions": {
                    "623112765726354fsdfjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy)


## Test #5
description = "multiple subjects, multiple sessions -- filenames ALREADY BIDS"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "123u3473485": {"label": "ses-001",
                "subject_code": "sub-001",
                "acquisitions": {
                    "623765476s": {
                        "label": "T1w",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "6237610s877763": {
                        "label": "task-balloontask",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "123445345435": {
                "label": "ses-002",
                "subject_code": "sub-001",
                "acquisitions": {
                    "623769990ds": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62y8767777jh": {
                        "label": "task-taskballoon",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "483222234": {
                "label": "ses-001",
                "subject_code": "sub-002",
                "acquisitions": {
                    "61231xx39485sjs23jh": {
                        "label": "T1w",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62377sdkxxjfhaiuex": {
                        "label": "task-taskballoon",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "222880234": {
                "label": "ses-002",
                "subject_code": "sub-002",
                "acquisitions": {
                    "6238743587fjh": {
                        "label": "T1w",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "6237italjsd843727": {
                        "label": "task-taskballoon",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }},
                    }}}
run_print_test(description, flywheel_hierarchy)

## Test #6
description = "multiple T1w images"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "123",
                "subject_code": "876",
                "acquisitions": {
                    "alksdfiuer932": {
                        "label": "T1 MPRAGE 1",
                        "created": "2017-09-19T10:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62asdfsafdh": {
                        "label": "T1 MPRAGE 2",
                        "created": "2017-09-19T14:10:09.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62skldfjuh": {
                        "label": "T1 MPRAGE 3",
                        "created": "2017-09-20T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "982734adsdf": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}

run_print_test(description, flywheel_hierarchy, print_files_lookup=True)
## Test #7
description = "multiple functional images"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "123",
                "subject_code": "876",
                "acquisitions": {
                    "alksdfiuer932": {
                        "label": "T1 MPRAGE 1",
                        "created": "2017-09-19T10:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62asdfsafdh": {
                        "label": "fMRI task",
                        "created": "2017-09-19T13:10:09.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "62skldfjuh": {
                        "label": "fMRI task",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "982734adsdf": {
                        "label": "fMRI task",
                        "created": "2017-09-25T08:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy, print_files_lookup=True)

## Test #8
description = "files with extension .nii"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy)
## Test #9
description = "no nifti files"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip'],
                        'measurements': ['functional', None],
                        'type': ['dicom']
                        }}}}}
run_print_test(description, flywheel_hierarchy)
## Test #10
description = "no 'measurements'"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': [None, None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': [None, None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy)
## Test #11
description = 'Different session ids but same session label'
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "session1",
                "subject_code": "JaneDoe",
                "acquisitions": {
                    "7823765726354fsd7263476s": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "6563765726354fsd7263476s876fjh": {
                        "label": "fMRI_task",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
        "48375jdfkjdsf983498234": {
                "label": "session1",
                "subject_code": "JaneDoe",
                "acquisitions": {
                    "123112765726354fsdfjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-20T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "343765726354fsd7263476s876fjh": {
                        "label": "fMRI_task",
                        "created": "2017-09-20T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}},
                    }}
run_print_test(description, flywheel_hierarchy, print_files_lookup=True)
## Test #12
description = 'Lower case measurements'
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd7263476s876fjh": {
                        "label": "fMRI task",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }}}}}
run_print_test(description, flywheel_hierarchy)

## Test #13
description = 'multiple niftis in an acquisition'
flywheel_hierarchy = {
    u'576be74e59b2b6346719ef83': {
        u'576be8b259b2b6346719efe4': {
            'label': u'amyg_s15_amyg_sess1_pcolA',
            'subject_code': u'amyg_s15',
            'acquisitions': {u'576d1faaa02c8621973ed0fa': {
                'created': u'2016-06-24T11:55:22.726Z',
                    'files': [u'8613_8_1_fmri.dcm.zip',
                              u'fmri.nii.gz',
                              u'8613_8_1_fmri_fMRI_Ret_bars_20150107173003_8.nii.gz'],
                    'label': u'fMRI_Ret_bars',
                    'measurements': [u'functional',
                                     u'functional',
                                     None],
                    'type': [u'dicom',
                             u'nifti',
                             u'nifti']}}}}}
run_print_test(description, flywheel_hierarchy, print_files_lookup=True)


## Test #14
description = 'empty session'
flywheel_hierarchy = {u'576be8b259b2b6346719efe4': {}}
run_print_test(description, flywheel_hierarchy, print_files_lookup=True)


## Test #15
description = 'empty acquisition'
flywheel_hierarchy = {u'576be8b259b2b6346719efe4': {u'29837498ualkjsdflksjfls': {}}}
run_print_test(description, flywheel_hierarchy, print_files_lookup=True)

## TODO: Test #16 -- CAN labels have underscores?!?!? is that BIDS compliant? - seems like no - no underscores allowed
description = 'Checking underscores'
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "ses-_2_3",
                "subject_code": "1_2_3rt",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1_MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd72348573476fjh": {
                        "label": "fMRI_task_thisisthetask_check_test",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }
                    }}}}
run_print_test(description, flywheel_hierarchy)


## Test #17 -- rest must be in the acquisition label to be found...
description = "Handling 'rest' task"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "1^53",
                "subject_code": "98001",
                "acquisitions": {
                    "623765726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "623765726354fsd72348573476fjh": {
                        "label": "fMRI task ",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "12654sadflkje87we87weradsf": {
                        "label": "rest fMRI task",
                        "created": "2017-09-19T10:39:58.721Z",
                        "files": ['fmri_dicom.zip', 'fmri.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    }}}}
run_print_test(description, flywheel_hierarchy)


## Test #18
description = "Handling 'sbref' files"
flywheel_hierarchy = {
    "8aa3d4574587asj": {
        "48375938745s76f6ds767sd6": {
                "label": "s001",
                "subject_code": "001",
                "acquisitions": {
                    "123726354fsd7263476s876fjh": {
                        "label": "T1 MPRAGE",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1_dicom.zip', 'T1.nii.gz'],
                        'measurements': ['anatomy_t1w', None],
                        'type': ['dicom', 'nifti']
                        },
                    "234526354fsd723485734fsrt": {
                        "label": "fMRI_REST_AP",
                        "created": "2017-09-19T14:39:58.721Z",
                        "files": ['rfMRI_REST_AP.zip', 'rfMRI_REST_AP.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "345sadflkje87we87weradsf": {
                        "label": "fMRi_REST_SBRef",
                        "created": "2017-09-19T10:39:58.721Z",
                        "files": ['sbref_dicom.zip', 'sbref.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "456756756756623432klj": {
                        "label": "fMRI_task_AP",
                        "created": "2017-09-19T15:39:58.721Z",
                        "files": ['rfMRI_task_AP.zip', 'rfMRI_task_AP.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        },
                    "5676663441265dsf": {
                        "label": "fMRi_task_AP_SBRef",
                        "created": "2017-09-19T15:39:58.721Z",
                        "files": ['task_sbref_dicom.zip', 'task_sbref.nii.gz'],
                        'measurements': ['functional', None],
                        'type': ['dicom', 'nifti']
                        }
                    }}}}
run_print_test(description, flywheel_hierarchy)

### Berkeley example
description = "Berkeley example"
flywheel_hierarchy = {
    "59c275f0f5187a001d725b84": {
        "59c1ba4bf5187a001d725b6f": {
                "label": "2017-09-19 14:35",
                "subject_code": "HERO_gka1",
                "acquisitions": {
                    "1": {
                        "label": "SpinEchoFieldMap_AP",
                        "created": "2017-09-19T14:39:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919393376149693793.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919393376149693793.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919393376149693793.0.0.0.json'
                            ],
                        'measurements': ['field_map', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "2": {
                        "label": "SpinEchoFieldMap_PA",
                        "created": "2017-09-19T14:40:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919401467612294451.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919401467612294451.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919401467612294451.0.0.0.json'
                            ],
                        'measurements': ['field_map', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "3": {
                        "label": "tfMRI_LFContrast_PA_run1_SBRef",
                        "created": "2017-09-19T14:42:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919421021234395122.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919421021234395122.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919421021234395122.0.0.0.json'
                            ],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "4": {
                        "label": "tfMRI_LFContrast_PA_run1",
                        "created": "2017-09-19T14:42:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919421231599295123.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919421231599295123.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919421231599295123.0.0.0.json',
                            '1_qa_report.png',
                            '1_mriqc.qa.html'
                            ],
                        'measurements': ['functional', None, None, None, 'functional'],
                        'type': ['dicom', 'nifti', 'source code', 'qa', 'qa']
                        },
                    "5": {
                        "label": "tfMRI_LFContrast_AP_run1_SBRef",
                        "created": "2017-09-19T14:50:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919493668688474262.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919493668688474262.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919493668688474262.0.0.0.json'
                            ],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "6": {
                        "label": "tfMRI_LFContrast_AP_run1",
                        "created": "2017-09-19T14:50:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919493882400374263.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919493882400374263.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919493882400374263.0.0.0.json',
                            '1_qa_report.png'],
                        'measurements': ['functional', None, None, None],
                        'type': ['dicom', 'nifti', 'source code', 'qa']
                        },
                    "7": {
                        "label": "tfMRI_LFContrast_PA_run2_SBRef",
                        "created": "2017-09-19T14:56:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919545114956153402.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919545114956153402.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919545114956153402.0.0.0.json'],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "8": {
                        "label": "tfMRI_LFContrast_PA_run2",
                        "created": "2017-09-19T14:56:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091919545332144453403.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091919545332144453403.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091919545332144453403.0.0.0.json',
                            '1_qa_report.png'],
                        'measurements': ['functional', None, None, None],
                        'type': ['dicom', 'nifti', 'source code', 'qa']
                        },
                    "9": {
                        "label": "tfMRI_LFContrast_AP_run2_SBRef",
                        "created": "2017-09-19T15:01:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920004535912132542.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920004535912132542.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920004535912132542.0.0.0.json'
                            ],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "10": {
                        "label": "tfMRI_LFContrast_AP_run2",
                        "created": "2017-09-19T15:01:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920004747015432543.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920004747015432543.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920004747015432543.0.0.0.json',
                            '1_qa_report.png'
                            ],
                        'measurements': ['functional', None, None, None],
                        'type': ['dicom', 'nifti', 'source code', 'qa']
                        },
                    "11": {
                        "label": "tfMRI_LFContrast_PA_run3_SBRef",
                        "created": "2017-09-19T15:09:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920083225750111682.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920083225750111682.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920083225750111682.0.0.0.json'	
                            ],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "12": {
                        "label": "tfMRI_LFContrast_PA_run3",
                        "created": "2017-09-19T15:09:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920083444350411683.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920083444350411683.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920083444350411683.0.0.0.json',
                            '1_qa_report.png'
                            ],
                        'measurements': ['functional', None, None, None],
                        'type': ['dicom', 'nifti', 'source code', 'qa']
                        },
                    "13": {
                        "label": "tfMRI_LFContrast_AP_run3_SBRef",
                        "created": "2017-09-19T15:14:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920134318597290822.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920134318597290822.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920134318597290822.0.0.0.json'
                            ],
                        'measurements': ['functional', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "14": {
                        "label": "tfMRI_LFContrast_AP_run3",
                        "created": "2017-09-19T15:14:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920134531766790823.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920134531766790823.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920134531766790823.0.0.0.json',
                            '1_qa_report.png'],
                        'measurements': ['functional', None, None, None],
                        'type': ['dicom', 'nifti', 'source code', 'qa']
                        },
                    "15": {
                        "label": "T1w_MPR",
                        "created": "2017-09-19T15:26:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920200439073969961.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920200439073969961.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920200439073969961.0.0.0.json'
                            ],
                        'measurements': ['anatomy_t1w', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        },
                    "16": {
                        "label": "T2w_SPC",
                        "created": "2017-09-19T15:32:00.000Z",
                        "files": [
                            '1.3.12.2.1107.5.2.43.66044.2017091920324580650270941.0.0.0.dicom.zip',
                            '1.3.12.2.1107.5.2.43.66044.2017091920324580650270941.0.0.0.nii.gz',
                            '1.3.12.2.1107.5.2.43.66044.2017091920324580650270941.0.0.0.json'
                            ],
                        'measurements': ['anatomy_t2w', None, None],
                        'type': ['dicom', 'nifti', 'source code']
                        }
                    }}}}
run_print_test(description, flywheel_hierarchy)
### UPenn example
description = "UPenn example"
#run_print_test(description, flywheel_hierarchy)
