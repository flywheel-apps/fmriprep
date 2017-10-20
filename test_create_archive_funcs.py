from pprint import pprint
import unittest

import create_archive_funcs

class bidsTestCases(unittest.TestCase):

    def _compare_file_lookup(self, files_lookup, files_exp):
        # Iterate over lists and compare...
        for idx in range(len(files_lookup)):
            f,b = files_lookup[idx]
            f_exp, b_exp = files_exp[idx]
            # Assert filenames are equal
            self.assertEqual(f, f_exp)
            self.assertEqual(b, b_exp)



    ##### Testing function: 'check_meta_info'
    def test_check_meta_info_t1w_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_T1w.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_t1w_info(self):
        f = '123.nii.gz'
        b = 'sub-123_T1w.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_t2w_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_T2w.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_t2w_info(self):
        f = '123.nii.gz'
        b = 'sub-123_T2w.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_bold_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_bold.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_bold_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_bold.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_bold_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_bold.nii.gz'
        info = {'RepetitionTime': 'value1',
                'TaskName': 'value2',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_sbref_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_sbref.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_sbref_info(self):
        f = '123.nii.gz'
        b = 'sub-123_sbref.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_phasediff_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_phasediff.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phasediff_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_phasediff.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phasediff_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_phasediff.nii.gz'
        info = {'EchoTime1': 'value1',
                'EchoTime2': 'value2',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_phase1_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_phase1.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phase1_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_phase1.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phase1_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_phase1.nii.gz'
        info = {'EchoTime': 'value1',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_phase2_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_phase2.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phase2_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_phase2.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_phase2_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_phase2.nii.gz'
        info = {'EchoTime': 'value1',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_fieldmap_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_fieldmap.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_fieldmap_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_fieldmap.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_fieldmap_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_fieldmap.nii.gz'
        info = {'Units': 'value1',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_epi_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_epi.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_epi_info_invalid(self):
        f = '123.nii.gz'
        b = 'sub-123_epi.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertTrue(reqvals_notpresent)

    def test_check_meta_info_epi_info_valid(self):
        f = '123.nii.gz'
        b = 'sub-123_epi.nii.gz'
        info = {'PhaseEncodingDirection': 'value1',
                'TotalReadoutTime': 'value2',
                'Extra': 'extra'
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude_info(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude1_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude1.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude1_info(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude1.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude2_noinfo(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude2.nii.gz'
        info = {}
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    def test_check_meta_info_magnitude2_info(self):
        f = '123.nii.gz'
        b = 'sub-123_magnitude2.nii.gz'
        info = {'Test1': 'value1',
                'Test2': 'value2',
                }
        reqvals_notpresent = create_archive_funcs.check_meta_info(f, b, info)
        self.assertFalse(reqvals_notpresent)

    ##### Testing function: 'create_bids_hierarchy'
    def test_create_bids_hierarchy_one_sub_one_session_notbids(self):
        flywheel_hierarchy = {"11": {"22": {
                "label": "12^2", "subject_code": "98001",
                "acquisitions": {
                    "33": {
                        "label": "T1 MPRAGE", "created": "2017-09-19T14:39:58.721Z",
                        "files": ['T1.nii.gz'], 'measurements': ['anatomy_t1w'],
                        'types': ['nifti'], 'infos': [{}]
                        },
                    "44": {
                        "label": "fMRI task ", "created": "2017-09-19T14:39:58.721Z",
                        "files": ['fmri.nii.gz'], 'measurements': ['functional'],
                        'types': ['nifti'], 'infos': [{'RepetitionTime': 'val'}]
                        }
                    }}}}
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        # Assert files_lookup is as expected...
        files_exp = [
                ('11/22/33/T1.nii.gz', 'sub-98001/ses-122/anat/sub-98001_ses-122_T1w.nii.gz'),
                ('11/22/44/fmri.nii.gz', 'sub-98001/ses-122/func/sub-98001_ses-122_task-fMRItask_bold.nii.gz'),
                ({'RepetitionTime': 'val','TaskName':'fMRItask'}, 'sub-98001/ses-122/func/sub-98001_ses-122_task-fMRItask_bold.json')
                ]
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)


    def test_create_bids_hierarchy_1sub_2ses_notbids(self):
    # 'one subject, multiple sessions -- NOT BIDS'
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                    "label": "session1",
                    "subject_code": "Jane Doe 1",
                    "acquisitions": {
                        "623765726354fsd7263476s": {
                            "label": "T1 MPRAGE", "created": "2017-09-19T14:39:58.721Z",
                            "files": ['T1.nii.gz'], 'measurements': ['anatomy_t1w'],
                            'type': ['nifti'], 'infos': [{}]
                        },
                        "623765726354fsd7263476s876fjh": {
                            "label": "fMRI task ", "created": "2017-09-19T14:39:58.721Z",
                            "files": ['fmri.nii.gz'], 'measurements': ['functional'],
                            'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                        }}},
                "sesID2": {
                    "label": "session2",
                    "subject_code": "Jane Doe 1",
                    "acquisitions": {
                       "623112765726354fsdfjh": {
                            "label": "T1 MPRAGE", "created": "2017-09-19T14:39:58.721Z",
                            "files": ['T1.nii.gz'], 'measurements': ['anatomy_t1w'],
                            'type': ['nifti'], 'infos': [{}]
                        },
                        "623765726354fsd7263476s876fjh": {
                            "label": "fMRI task ", "created": "2017-09-19T14:39:58.721Z",
                            "files": ['fmri.nii.gz'], 'measurements': ['functional'],
                            'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                        }}},
                    }}

        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        files_exp = [
            ['projID/sesID1/623765726354fsd7263476s/T1.nii.gz',
                'sub-JaneDoe1/ses-session1/anat/sub-JaneDoe1_ses-session1_T1w.nii.gz'],
            ['projID/sesID1/623765726354fsd7263476s876fjh/fmri.nii.gz',
                'sub-JaneDoe1/ses-session1/func/sub-JaneDoe1_ses-session1_task-fMRItask_bold.nii.gz'],
            ['projID/sesID2/623112765726354fsdfjh/T1.nii.gz',
                'sub-JaneDoe1/ses-session2/anat/sub-JaneDoe1_ses-session2_T1w.nii.gz'],
            ['projID/sesID2/623765726354fsd7263476s876fjh/fmri.nii.gz',
                'sub-JaneDoe1/ses-session2/func/sub-JaneDoe1_ses-session2_task-fMRItask_bold.nii.gz'],
            [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                'sub-JaneDoe1/ses-session1/func/sub-JaneDoe1_ses-session1_task-fMRItask_bold.json'],
            [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                'sub-JaneDoe1/ses-session2/func/sub-JaneDoe1_ses-session2_task-fMRItask_bold.json']
            ]
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)


    def test_create_bids_hierarchy_samelabel(self):
        #multiple subjects, one session each (same session label: 'session1')
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "session1",
                        "subject_code": "s001",
                        "acquisitions": {
                            "623765726354fsd7263476s": {
                                "label": "T1 MPRAGE", "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'], 'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ", "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'], 'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID2": {
                        "label": "session1",
                        "subject_code": "s002",
                        "acquisitions": {
                            "623112765726354fsdfjh": {
                                "label": "T1 MPRAGE", "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'], 'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ", "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'], 'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}
                            }}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        files_exp = [
                ['projID/sesID1/623765726354fsd7263476s/T1.nii.gz',
                    'sub-s001/ses-session1/anat/sub-s001_ses-session1_T1w.nii.gz'],
                ['projID/sesID1/623765726354fsd7263476s876fjh/fmri.nii.gz',
                    'sub-s001/ses-session1/func/sub-s001_ses-session1_task-fMRItask_bold.nii.gz'],
                ['projID/sesID2/623112765726354fsdfjh/T1.nii.gz',
                    'sub-s002/ses-session1/anat/sub-s002_ses-session1_T1w.nii.gz'],
                ['projID/sesID2/623765726354fsd7263476s876fjh/fmri.nii.gz',
                    'sub-s002/ses-session1/func/sub-s002_ses-session1_task-fMRItask_bold.nii.gz'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s001/ses-session1/func/sub-s001_ses-session1_task-fMRItask_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s002/ses-session1/func/sub-s002_ses-session1_task-fMRItask_bold.json']]
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

    def test_create_bids_hierarchy_2sub_4ses_notbids(self):
        # multiple subjects, multiple sessions - NOT BIDS
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "session1",
                        "subject_code": "s001",
                        "acquisitions": {
                            "623765476s": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID2": {
                        "label": "session2",
                        "subject_code": "s001",
                        "acquisitions": {
                            "62376ddddds": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62y6667777jh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID3": {
                        "label": "session1",
                        "subject_code": "s002",
                        "acquisitions": {
                            "612312323423jh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62377sdkjfhaiueyr666764jh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID4": {
                        "label": "session2",
                        "subject_code": "s002",
                        "acquisitions": {
                            "623112765726354fsdfjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        files_exp = [
                ['projID/sesID1/623765476s/T1.nii.gz',
                    'sub-s001/ses-session1/anat/sub-s001_ses-session1_T1w.nii.gz'],
                ['projID/sesID1/623765726354fsd7263476s876fjh/fmri.nii.gz',
                    'sub-s001/ses-session1/func/sub-s001_ses-session1_task-fMRItask_bold.nii.gz'],
                ['projID/sesID2/62376ddddds/T1.nii.gz',
                    'sub-s001/ses-session2/anat/sub-s001_ses-session2_T1w.nii.gz'],
                ['projID/sesID2/62y6667777jh/fmri.nii.gz',
                    'sub-s001/ses-session2/func/sub-s001_ses-session2_task-fMRItask_bold.nii.gz'],
                ['projID/sesID3/612312323423jh/T1.nii.gz',
                    'sub-s002/ses-session1/anat/sub-s002_ses-session1_T1w.nii.gz'],
                ['projID/sesID3/62377sdkjfhaiueyr666764jh/fmri.nii.gz',
                    'sub-s002/ses-session1/func/sub-s002_ses-session1_task-fMRItask_bold.nii.gz'],
                ['projID/sesID4/623112765726354fsdfjh/T1.nii.gz',
                    'sub-s002/ses-session2/anat/sub-s002_ses-session2_T1w.nii.gz'],
                ['projID/sesID4/623765726354fsd7263476s876fjh/fmri.nii.gz',
                    'sub-s002/ses-session2/func/sub-s002_ses-session2_task-fMRItask_bold.nii.gz'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s001/ses-session1/func/sub-s001_ses-session1_task-fMRItask_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s001/ses-session2/func/sub-s001_ses-session2_task-fMRItask_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s002/ses-session1/func/sub-s002_ses-session1_task-fMRItask_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'fMRItask'},
                    'sub-s002/ses-session2/func/sub-s002_ses-session2_task-fMRItask_bold.json']]
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

    def test_create_bids_hierarchy_2sub_4ses_bids(self):
        # multiple subjects, multiple sessions -- filenames ALREADY BIDS
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {"label": "ses-001",
                        "subject_code": "sub-001",
                        "acquisitions": {
                            "623765476s": {
                                "label": "T1w",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "6237610s877763": {
                                "label": "task-balloontask",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID2": {
                        "label": "ses-002",
                        "subject_code": "sub-001",
                        "acquisitions": {
                            "623769990ds": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62y8767777jh": {
                                "label": "task-taskballoon",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID3": {
                        "label": "ses-001",
                        "subject_code": "sub-002",
                        "acquisitions": {
                            "61231xx39485sjs23jh": {
                                "label": "T1w",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62377sdkxxjfhaiuex": {
                                "label": "task-taskballoon",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID4": {
                        "label": "ses-002",
                        "subject_code": "sub-002",
                        "acquisitions": {
                            "6238743587fjh": {
                                "label": "T1w",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "6237italjsd843727": {
                                "label": "task-taskballoon",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }},
                            }}}

        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        



    def test_create_bids_hierarchy_multiple_T1w(self):
        #multiple T1w images
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "123",
                        "subject_code": "876",
                        "acquisitions": {
                            "alksdfiuer932": {
                                "label": "T1 MPRAGE 1",
                                "created": "2017-09-19T10:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62asdfsafdh": {
                                "label": "T1 MPRAGE 2",
                                "created": "2017-09-19T14:10:09.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62skldfjuh": {
                                "label": "T1 MPRAGE 3",
                                "created": "2017-09-20T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "982734adsdf": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)


    def test_create_bids_hierarchy_multiple_func_images(self):
        # Multiple functional images
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "123",
                        "subject_code": "876",
                        "acquisitions": {
                            "alksdfiuer932": {
                                "label": "T1 MPRAGE 1",
                                "created": "2017-09-19T10:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "62asdfsafdh": {
                                "label": "fMRI task",
                                "created": "2017-09-19T13:10:09.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "62skldfjuh": {
                                "label": "fMRI task",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "982734adsdf": {
                                "label": "fMRI task",
                                "created": "2017-09-25T08:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_extension_nii(self):
        # files with extension .nii
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        

    def test_create_bids_hierarchy_no_nifti_files(self):
        #"no nifti files"
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1_dicom.zip'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['dicom'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri_dicom.zip'],
                                'measurements': ['functional'],
                                'type': ['dicom'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_no_measurements(self):
        # "no 'measurements'"
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': [None],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': [None],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_diff_ids_same_label(self):
        #'Different session ids but same session label'
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "session1",
                        "subject_code": "JaneDoe",
                        "acquisitions": {
                            "7823765726354fsd7263476s": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "6563765726354fsd7263476s876fjh": {
                                "label": "fMRI_task",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                "sesID2": {
                        "label": "session1",
                        "subject_code": "JaneDoe",
                        "acquisitions": {
                            "123112765726354fsdfjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-20T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "343765726354fsd7263476s876fjh": {
                                "label": "fMRI_task",
                                "created": "2017-09-20T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}},
                            }}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_uppercase_measurements(self):
        #'uppercase measurements'
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['Anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['Functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_multiple_niftis(self):
        #'multiple niftis in an acquisition'
        flywheel_hierarchy = {
            u'576be74e59b2b6346719ef83': {
                u'576be8b259b2b6346719efe4': {
                    'label': u'amyg_s15_amyg_sess1_pcolA',
                    'subject_code': u'amyg_s15',
                    'acquisitions': {u'576d1faaa02c8621973ed0fa': {
                        'created': u'2016-06-24T11:55:22.726Z',
                            'files': [
                                      u'fmri.nii.gz',
                                      u'8613_8_1_fmri_fMRI_Ret_bars_20150107173003_8.nii.gz'
                                      ],
                            'label': u'fMRI_Ret_bars',
                            'measurements': [
                                             u'functional',
                                             u'functional'
                                             ],
                            'types': [
                                     u'nifti',
                                     u'nifti'
                                     ],
                            'infos': [
                                    {'RepetitionTime':'val'},
                                    {'RepetitionTime':'val'}
                                     ],
                            }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_underscores(self):
        # TODO: CAN labels have underscores?!?!? is that BIDS compliant? - seems like no - no underscores allowed
        #'Checking underscores'
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "ses-_2_3",
                        "subject_code": "1_2_3rt",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1_MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd72348573476fjh": {
                                "label": "fMRI_task_thisisthetask_check_test",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                }
                            }}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_rest(self):
        # NOTE: rest must be in the acquisition label to be found...
        #"Handling 'rest' task"
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd72348573476fjh": {
                                "label": "fMRI task ",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "12654sadflkje87we87weradsf": {
                                "label": "rest fMRI task",
                                "created": "2017-09-19T10:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            }}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_sbref(self):
        #"Handling 'sbref' files"
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "s001",
                        "subject_code": "001",
                        "acquisitions": {
                            "123726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "234526354fsd723485734fsrt": {
                                "label": "fMRI_REST_AP",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['rfMRI_REST_AP.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "345sadflkje87we87weradsf": {
                                "label": "fMRi_REST_SBRef",
                                "created": "2017-09-19T10:39:58.721Z",
                                "files": ['sbref.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "456756756756623432klj": {
                                "label": "fMRI_task_AP",
                                "created": "2017-09-19T15:39:58.721Z",
                                "files": ['rfMRI_task_AP.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{'RepetitionTime':'val'}]
                                },
                            "5676663441265dsf": {
                                "label": "fMRi_task_AP_SBRef",
                                "created": "2017-09-19T15:39:58.721Z",
                                "files": ['task_sbref.nii.gz'],
                                'measurements': ['functional'],
                                'type': ['nifti'], 'infos': [{}]
                                }
                            }}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_customer_example(self):
        # customer example
        flywheel_hierarchy = {'projID': {
            'sesID1': {
                'acquisitions': {
                    '59dd24192ff46855581e01b6': {
                        'created': '2017-10-10T19:48:35.833Z',
                        'files': ['ep2d_neuro_PA_Task_3mm.nii.gz'],
                        'label': 'ep2d_neuro_PA_Task_3mm',
                        'measurements': [None],
                        'type': ['nifti'], 'infos': [{}]},
                    '59dd24662ff46855581e01b7': {'created': '2017-10-10T19:49:48.621Z',
                        'files': ['ep2d_neuro_PA_Rest_3mm.nii.gz'],
                        'label': 'ep2d_neuro_PA_Rest_3mm',
                        'measurements': [None],
                        'type': ['nifti'], 'infos': [{}]},
                    '59dd24c62ff46855581e01b9': {'created': '2017-10-10T19:51:32.499Z',
                        'files': ['T1 MPRAGE.nii.gz'],
                        'label': 'T1 MPRAGE',
                        'measurements': [None],
                        'type': ['nifti'], 'infos': [{}]}
                    },
                    'label': '09/18/17 17:25 PM',
                    'subject_code': 'DistractWM_123'}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_customer_fieldmaps(self):
        # customer fieldmap example
        flywheel_hierarchy = {
                "projectID": {
                    "sessionID": {
                        "label": "session1",
                        "subject_code": "HERO_gka1",
                        "acquisitions": {
                    "1": {
                        "label": "SpinEchoFieldMap_AP", "created": "2017-09-19T14:39:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919393376149693793.0.0.0.nii.gz'],
                        'measurements': ['field_map'], 'type': ['nifti'],
                        'infos': [{'PhaseEncodingDirection': '1','TotalReadoutTime': '2'}]
                        },
                    "2": {
                        "label": "SpinEchoFieldMap_PA", "created": "2017-09-19T14:40:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919401467612294451.0.0.0.nii.gz'],
                        'measurements': ['field_map'], 'type': ['nifti'],
                        'infos': [{'PhaseEncodingDirection': '1','TotalReadoutTime': '2'}]
                        },
                    "3": {
                        "label": "tfMRI_LFContrast_PA_run1_SBRef", "created": "2017-09-19T14:42:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919421021234395122.0.0.0.nii.gz'],
                        'measurements': ['functional'], 'type': ['nifti'], 'infos': [{}]
                        },
                    "4": {
                        "label": "tfMRI_LFContrast_PA_run1","created": "2017-09-19T14:42:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919421231599295123.0.0.0.nii.gz'],
                        'measurements': ['functional'],'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "5": {
                        "label": "tfMRI_LFContrast_AP_run1_SBRef", "created": "2017-09-19T14:50:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919493668688474262.0.0.0.nii.gz'],
                        'measurements': ['functional'], 'type': ['nifti'], 'infos': [{}]
                        },
                    "6": {
                        "label": "tfMRI_LFContrast_AP_run1", "created": "2017-09-19T14:50:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919493882400374263.0.0.0.nii.gz'],
                        'measurements': ['functional'],'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "7": {"label": "tfMRI_LFContrast_PA_run2_SBRef", "created": "2017-09-19T14:56:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919545114956153402.0.0.0.nii.gz'],
                        'measurements': ['functional'],'type': ['nifti'], 'infos': [{}]
                        },
                    "8": {
                        "label": "tfMRI_LFContrast_PA_run2","created": "2017-09-19T14:56:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091919545332144453403.0.0.0.nii.gz'],
                        'measurements': ['functional'],'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "9": {
                        "label": "tfMRI_LFContrast_AP_run2_SBRef", "created": "2017-09-19T15:01:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920004535912132542.0.0.0.nii.gz',],
                        'measurements': ['functional'],'type': ['nifti'], 'infos': [{}]
                        },
                    "10": {
                        "label": "tfMRI_LFContrast_AP_run2","created": "2017-09-19T15:01:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920004747015432543.0.0.0.nii.gz',],
                        'measurements': ['functional'], 'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "11": {
                        "label": "tfMRI_LFContrast_PA_run3_SBRef","created": "2017-09-19T15:09:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920083225750111682.0.0.0.nii.gz',],
                        'measurements': ['functional'],'type': ['nifti'], 'infos': [{}]
                        },
                    "12": {
                        "label": "tfMRI_LFContrast_PA_run3", "created": "2017-09-19T15:09:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920083444350411683.0.0.0.nii.gz',],
                        'measurements': ['functional'], 'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "13": {
                        "label": "tfMRI_LFContrast_AP_run3_SBRef", "created": "2017-09-19T15:14:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920134318597290822.0.0.0.nii.gz',],
                        'measurements': ['functional'], 'type': ['nifti'], 'infos': [{}]
                        },
                    "14": {
                        "label": "tfMRI_LFContrast_AP_run3", "created": "2017-09-19T15:14:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920134531766790823.0.0.0.nii.gz',],
                        'measurements': ['functional'], 'type': ['nifti'],
                        'infos': [{'RepetitionTime':'val'}]
                        },
                    "15": {
                        "label": "T1w_MPR","created": "2017-09-19T15:26:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920200439073969961.0.0.0.nii.gz',],
                        'measurements': ['anatomy_t1w'], 'type': ['nifti'], 'infos': [{}]
                        },
                    "16": {
                        "label": "T2w_SPC","created": "2017-09-19T15:32:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.43.66044.2017091920324580650270941.0.0.0.nii.gz'],
                        'measurements': ['anatomy_t2w'], 'type': ['nifti'], 'infos': [{}]
                        }
                    }}}}
        # Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        # Assert files_lookup is as expected...
        files_exp = [
                ['projectID/sessionID/1/1.3.12.2.1107.5.2.43.66044.2017091919393376149693793.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/fmap/sub-HEROgka1_ses-session1_dir-AP_epi.nii.gz'],
                ['projectID/sessionID/2/1.3.12.2.1107.5.2.43.66044.2017091919401467612294451.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/fmap/sub-HEROgka1_ses-session1_dir-PA_epi.nii.gz'],
                ['projectID/sessionID/3/1.3.12.2.1107.5.2.43.66044.2017091919421021234395122.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_sbref.nii.gz'],
                ['projectID/sessionID/4/1.3.12.2.1107.5.2.43.66044.2017091919421231599295123.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_bold.nii.gz'], 
                ['projectID/sessionID/5/1.3.12.2.1107.5.2.43.66044.2017091919493668688474262.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_sbref.nii.gz'], 
                ['projectID/sessionID/6/1.3.12.2.1107.5.2.43.66044.2017091919493882400374263.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_bold.nii.gz'],
                ['projectID/sessionID/7/1.3.12.2.1107.5.2.43.66044.2017091919545114956153402.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_sbref.nii.gz'],
                ['projectID/sessionID/8/1.3.12.2.1107.5.2.43.66044.2017091919545332144453403.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_bold.nii.gz'], 
                ['projectID/sessionID/9/1.3.12.2.1107.5.2.43.66044.2017091920004535912132542.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_sbref.nii.gz'],
                ['projectID/sessionID/10/1.3.12.2.1107.5.2.43.66044.2017091920004747015432543.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_bold.nii.gz'],
                ['projectID/sessionID/11/1.3.12.2.1107.5.2.43.66044.2017091920083225750111682.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_sbref.nii.gz'],
                ['projectID/sessionID/12/1.3.12.2.1107.5.2.43.66044.2017091920083444350411683.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_bold.nii.gz'],
                ['projectID/sessionID/13/1.3.12.2.1107.5.2.43.66044.2017091920134318597290822.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_sbref.nii.gz'], 
                ['projectID/sessionID/14/1.3.12.2.1107.5.2.43.66044.2017091920134531766790823.0.0.0.nii.gz', 
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_bold.nii.gz'],
                ['projectID/sessionID/15/1.3.12.2.1107.5.2.43.66044.2017091920200439073969961.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/anat/sub-HEROgka1_ses-session1_T1w.nii.gz'],
                ['projectID/sessionID/16/1.3.12.2.1107.5.2.43.66044.2017091920324580650270941.0.0.0.nii.gz',
                    'sub-HEROgka1/ses-session1/anat/sub-HEROgka1_ses-session1_T2w.nii.gz'],

                [{'PhaseEncodingDirection': '1', 'TotalReadoutTime': '2'},
                    'sub-HEROgka1/ses-session1/fmap/sub-HEROgka1_ses-session1_dir-AP_epi.json'],
                [{'PhaseEncodingDirection': '1', 'TotalReadoutTime': '2'},
                    'sub-HEROgka1/ses-session1/fmap/sub-HEROgka1_ses-session1_dir-PA_epi.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastPA'},
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastAP'},
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastPA'},
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastAP'}, 
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastPA'},
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_bold.json'],
                [{'RepetitionTime': 'val', 'TaskName': 'tfMRILFContrastAP'},
                    'sub-HEROgka1/ses-session1/func/sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_bold.json'],
                ]
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

        # pretty print the bids_hierarchy
        bids_exp = {
            'sub-HEROgka1': {
                'ses-session1': {
                    'anat': [
                        'sub-HEROgka1_ses-session1_T1w.nii.gz',
                        'sub-HEROgka1_ses-session1_T2w.nii.gz'
                        ],
                    'fmap': [
                        'sub-HEROgka1_ses-session1_dir-AP_epi.nii.gz',
                        'sub-HEROgka1_ses-session1_dir-PA_epi.nii.gz',
                        'sub-HEROgka1_ses-session1_dir-AP_epi.json',
                        'sub-HEROgka1_ses-session1_dir-PA_epi.json'
                        ],
                    'func': [
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_sbref.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_bold.nii.gz',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-1_bold.json',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-1_bold.json',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-2_bold.json',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-2_bold.json',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastPA_run-3_bold.json',
                        'sub-HEROgka1_ses-session1_task-tfMRILFContrastAP_run-3_bold.json'
                        ]
                    }}}
        # Assert anat folder is the same
        self.assertEqual(
                 bids_hierarchy['sub-HEROgka1']['ses-session1']['anat'],
                 bids_exp['sub-HEROgka1']['ses-session1']['anat'],
            )
        # Assert fmap folder is the same
        self.assertEqual(
                bids_hierarchy['sub-HEROgka1']['ses-session1']['fmap'],
                bids_exp['sub-HEROgka1']['ses-session1']['fmap']
            )
        # Assert func folder is the same
        self.assertEqual(
                bids_hierarchy['sub-HEROgka1']['ses-session1']['func'],
                bids_exp['sub-HEROgka1']['ses-session1']['func']
            )

    def test_create_bids_hierarchy_no_info(self):
        # Assert error raised when no meta information is present
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "1^53",
                        "subject_code": "98001",
                        "acquisitions": {
                            "623765726354fsd7263476s876fjh": {
                                "label": "T1 MPRAGE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['T1.nii.gz'],
                                'measurements': ['Anatomy_t1w'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "623765726354fsd7263476s876fjh": {
                                "label": "fMRI task",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['fmri.nii.gz'],
                                'measurements': ['Functional'],
                                'type': ['nifti'], 'infos': [{}]
                                }}}}}
        ## Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

    def test_create_bids_hierarchy_case1(self):
        """ Case 1: phase difference image and at least one magnitude image

            Expected files:
                _phasediff.nii[.gz]
                _phasediff.json
                _magnitude1.nii[.gz]
                _magnitude2.nii[.gz]

        """
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "123",
                        "subject_code": "001",
                        "acquisitions": {
                            "12345": {
                                "label": "phaseDiff",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['phasediff.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'],
                                'infos': [{'EchoTime1': 0.006,
                                    'EchoTime2': 0.00746}]
                                },
                            "67": {
                                "label": "FieldmapMag",
                                "created": "2017-09-19T14:39:00.000Z",
                                "files": ['mag1.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "89": {
                                "label": "FieldmapMag",
                                "created": "2017-09-19T14:59:00.000Z",
                                "files": ['mag2.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'], 'infos': [{}]
                                }}}}}

        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        files_exp = [
                ['projID/sesID1/12345/phasediff.nii.gz',
                    'sub-001/ses-123/fmap/sub-001_ses-123_phasediff.nii.gz'],
                ['projID/sesID1/67/mag1.nii.gz',
                    'sub-001/ses-123/fmap/sub-001_ses-123_magnitude1.nii.gz'],
                ['projID/sesID1/89/mag2.nii.gz',
                    'sub-001/ses-123/fmap/sub-001_ses-123_magnitude2.nii.gz'],
                [{'EchoTime1': 0.006, 'EchoTime2': 0.00746},
                    'sub-001/ses-123/fmap/sub-001_ses-123_phasediff.json']
                ]
        bids_exp = {'sub-001': {'ses-123': {'fmap': ['sub-001_ses-123_phasediff.nii.gz',
                                  'sub-001_ses-123_magnitude1.nii.gz',
                                  'sub-001_ses-123_magnitude2.nii.gz',
                                  'sub-001_ses-123_phasediff.json']}}}
        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

        # Assert fmap folder is the same
        self.assertEqual(
                bids_hierarchy['sub-001']['ses-123']['fmap'],
                bids_exp['sub-001']['ses-123']['fmap']
                )

    def test_create_bids_hierarchy_case2(self):
        """ Case 2: two phase images and two magnitude images

            Expected files:
                _phase1.nii[.gz]
                _phase1.json
                _phase2.nii[.gz]
                _phase2.json
                _magnitude1.nii[.gz]
                _magnitude2.nii[.gz]

        """
        flywheel_hierarchy = {
            "projID": {
                "sesID1": {
                        "label": "123",
                        "subject_code": "001",
                        "acquisitions": {
                            "123": {
                                "label": "PHASE",
                                "created": "2017-09-19T14:39:58.721Z",
                                "files": ['phase1.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'],
                                'infos': [{'EchoTime': 0.006}]
                                },
                            "45": {
                                "label": "PHASE",
                                "created": "2017-09-19T14:44:58.721Z",
                                "files": ['phase2.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'],
                                'infos': [{'EchoTime': 0.00746}]
                                },
                            "67": {
                                "label": "FieldmapMag",
                                "created": "2017-09-19T14:39:00.000Z",
                                "files": ['mag1.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'], 'infos': [{}]
                                },
                            "89": {
                                "label": "FieldmapMag",
                                "created": "2017-09-19T14:59:00.000Z",
                                "files": ['mag2.nii.gz'],
                                'measurements': ['field_map'],
                                'type': ['nifti'], 'infos': [{}]
                                }}}}}
        # Call function
        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)
        files_exp = [['projID/sesID1/123/phase1.nii.gz',
            'sub-001/ses-123/fmap/sub-001_ses-123_phase1.nii.gz'],
            ['projID/sesID1/45/phase2.nii.gz',
                'sub-001/ses-123/fmap/sub-001_ses-123_phase2.nii.gz'],
            ['projID/sesID1/67/mag1.nii.gz',
                'sub-001/ses-123/fmap/sub-001_ses-123_magnitude1.nii.gz'],
            ['projID/sesID1/89/mag2.nii.gz',
                'sub-001/ses-123/fmap/sub-001_ses-123_magnitude2.nii.gz'],
            [{'EchoTime': 0.006},
                'sub-001/ses-123/fmap/sub-001_ses-123_phase1.json'],
            [{'EchoTime': 0.00746},
                'sub-001/ses-123/fmap/sub-001_ses-123_phase2.json']]
        bids_exp = {'sub-001': {'ses-123': {'fmap': ['sub-001_ses-123_phase1.nii.gz',
                                  'sub-001_ses-123_phase2.nii.gz',
                                  'sub-001_ses-123_magnitude1.nii.gz',
                                  'sub-001_ses-123_magnitude2.nii.gz',
                                  'sub-001_ses-123_phase1.json',
                                  'sub-001_ses-123_phase2.json']}}}

        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

        # Assert fmap folder is the same
        self.assertEqual(
                bids_hierarchy['sub-001']['ses-123']['fmap'],
                bids_exp['sub-001']['ses-123']['fmap']
                )

    def test_create_bids_hierarchy_case3(self):
        """ Case 3: single, real fieldmap image
            Expected files:
                _magnitude.nii[.gz]
                _fieldmap.nii[.gz]
                _fieldmap.json

        NOT IMPLEMENTED IN THE CODE

        """

    def test_create_bids_hierarchy_case4(self):
        """ Case 4: Multiple phase encoded directions
            Expected files:
                _epi.nii[.gz]
                _epi.json

        """
        flywheel_hierarchy = {
                "projectID": {
                    "sessionID": {
                        "label": "ses1",
                        "subject_code": "001",
                        "acquisitions": {
                    "1": {
                        "label": "SpinEchoFieldMap_AP", "created": "2017-09-19T14:39:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.4.nii.gz'],
                        'measurements': ['field_map'], 'type': ['nifti'],
                        'infos': [{'PhaseEncodingDirection': 'j-','TotalReadoutTime': 0.1}]
                        },
                    "2": {
                        "label": "SpinEchoFieldMap_PA", "created": "2017-09-19T14:40:00.000Z",
                        "files": ['1.3.12.2.1107.5.2.4000.nii.gz'],
                        'measurements': ['field_map'], 'type': ['nifti'],
                        'infos': [{'PhaseEncodingDirection': 'j','TotalReadoutTime': 0.35}]
                        }
                    }}}}

        bids_hierarchy, files_lookup = create_archive_funcs.create_bids_hierarchy(flywheel_hierarchy)

        files_exp = [
                ['projectID/sessionID/1/1.3.12.2.1107.5.2.4.nii.gz',
                    'sub-001/ses-ses1/fmap/sub-001_ses-ses1_dir-AP_epi.nii.gz'],
                ['projectID/sessionID/2/1.3.12.2.1107.5.2.4000.nii.gz',
                    'sub-001/ses-ses1/fmap/sub-001_ses-ses1_dir-PA_epi.nii.gz'],
                [{'PhaseEncodingDirection': 'j-', 'TotalReadoutTime': 0.1},
                    'sub-001/ses-ses1/fmap/sub-001_ses-ses1_dir-AP_epi.json'],
                [{'PhaseEncodingDirection': 'j', 'TotalReadoutTime': 0.35},
                    'sub-001/ses-ses1/fmap/sub-001_ses-ses1_dir-PA_epi.json']
                ]

        bids_exp = {'sub-001': {'ses-ses1': {'fmap': ['sub-001_ses-ses1_dir-AP_epi.nii.gz',
                                   'sub-001_ses-ses1_dir-PA_epi.nii.gz',
                                   'sub-001_ses-ses1_dir-AP_epi.json',
                                   'sub-001_ses-ses1_dir-PA_epi.json']}}}

        # Compare files
        self._compare_file_lookup(files_lookup, files_exp)

        # Assert fmap folder is the same
        self.assertEqual(
                bids_hierarchy['sub-001']['ses-ses1']['fmap'],
                bids_exp['sub-001']['ses-ses1']['fmap']
                )

if __name__ == "__main__":

    #suite = unittest.TestSuite()
    #suite.addTest(bidsTestCases('test_create_bids_hierarchy_case1'))
    #suite.addTest(bidsTestCases('test_create_bids_hierarchy_case2'))
    #suite.addTest(bidsTestCases('test_create_bids_hierarchy_case4'))
    #unittest.TextTestRunner().run(suite)

    unittest.main()
    run_module_suite()
