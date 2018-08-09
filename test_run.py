from pprint import pprint
import unittest
import os
import stat
import shutil

import run


class fmriprepTestCase(unittest.TestCase):

    def setUp(self):
        self.flywheel = 'flywheel/v0'
        os.makedirs(self.flywheel)
        run.FLYWHEEL_BASE = self.flywheel

        # Mock config.json
        self.config = {
            "config": {
                "freesurfer": True,
                "save_outputs": False,
                "save_intermediate_work": False,
                "intermediate_files": "ref_image_corrected_brain.nii.gz",
                "intermediate_folders": "",
                "ignore": "",
                "longitudinal": False,
                "t2s_coreg": False,
                "force_bbr": False,
                "force_no_bbr": False,
                "template": "MNI152NLin2009cAsym",
                "medial_surface_nan": False,
                "template_resampling_grid": "native",
                "bold2t1w_dof": 9,
                "output_space": "template fsaverage5"
            }
        }

    def tearDown(self):
        shutil.rmtree(self.flywheel)

    def test_get_flags(self):
        flags = run.get_flags(self.config)
        self.assertTrue('--longitudinal' == flags['longitudinal_FLAG'])
        self.assertTrue('' == flags['freesurfer_FLAG'])

    def test_recursive_chmod(self):
        file_dir = os.path.join(self.flywheel, 'files')
        os.mkdir(file_dir)

        file_path = os.path.join(self.flywheel, 'files', 'test.txt')
        with open(file_path, 'w') as fp:
            fp.write('Test string.')
        file_path_2 = os.path.join(self.flywheel, 'files', 'test2.txt')
        with open(file_path_2, 'w') as fp:
            fp.write('Second test string.')

        file_mode = os.stat(file_path).st_mode
        pre_file_perm = stat.S_IMODE(file_mode)
        file_mode = os.stat(file_path_2).st_mode
        pre_file_2_perm = stat.S_IMODE(file_mode)

        run.recursive_chmod(file_dir)

        file_mode = os.stat(file_path).st_mode
        post_file_perm = stat.S_IMODE(file_mode)
        file_mode = os.stat(file_path_2).st_mode
        post_file_2_perm = stat.S_IMODE(file_mode)

        self.assertTrue(post_file_perm == 777)
        self.assertTrue(post_file_perm != pre_file_perm)
        self.assertTrue(post_file_2_perm == 777)
        self.assertTrue(post_file_2_perm != pre_file_2_perm)

        shutil.rmtree(file_dir)

    def test_find_file(self):
        file_dir = os.path.join(self.flywheel, 'files')
        os.mkdir(file_dir)

        html_path = os.path.join(self.flywheel, 'files', 'test.html')
        with open(html_path, 'w') as fp:
            fp.write('Test string.')
        text_path = os.path.join(self.flywheel, 'files', 'test.txt')
        with open(text_path, 'w') as fp:
            fp.write('Second test string.')

        html_files = run.find_file('*.html', self.flywheel)
        self.assertTrue(len(html_files) == 1)
        self.assertTrue(html_files[0] == html_path)

        shutil.rmtree(file_dir)

    def test_find_dir(self):
        file_dir = os.path.join(self.flywheel, 'files')
        os.mkdir(file_dir)

        html_path = os.path.join(self.flywheel, 'files', 'test.html')
        with open(html_path, 'w') as fp:
            fp.write('Test string.')
        text_path = os.path.join(self.flywheel, 'files', 'test.txt')
        with open(text_path, 'w') as fp:
            fp.write('Second test string.')

        html_files = run.find_file('*.html', self.flywheel)
        self.assertTrue(len(html_files) == 1)
        self.assertTrue(html_files[0] == html_path)

        shutil.rmtree(file_dir)

    def test_get_freesurfer(self):
        freesurfer_dir = os.path.join(self.flywheel, 'input',
                                      'freesurfer_license')
        os.makedirs(freesurfer_dir)
        with open(os.path.join(freesurfer_dir, 'license.txt'), 'w') as license:
            license.write("My license")

        fs_license = run.get_freesurfer_license()
        expected_license_path = \
            'flywheel/v0/input/freesurfer_license/license.txt'
        self.assertTrue(fs_license == expected_license_path)

    def test_convert_index_to_archive(self):
        html_filename = 'out.html'
        sub_id = 'ex0000'
        analysis_id = '123456789009876543211234'
        gear_output = os.path.join(self.flywheel, 'output')
        fmriprep_output = os.path.join(gear_output, analysis_id)
        work_dir = fmriprep_output + '_work'
        html_filepath = os.path.join(fmriprep_output, 'fmriprep',
                                     html_filename)

        self.mock_fmriprep_output(fmriprep_output, sub_id, work_dir,
                                  html_filepath)

        run.convert_index_to_archive(html_filepath, sub_id, analysis_id,
                                     gear_output, work_dir)
        zip_file = run.find_file('*.html.zip', gear_output)[0]
        expected_zip_file = \
            'flywheel/v0/output/ex0000_123456789009876543211234.html.zip'
        self.assertEqual(zip_file, expected_zip_file)

    def mock_fmriprep_output(self, fmriprep_output, sub_id, work_dir,
                             html_filepath):

        os.makedirs(os.path.join(fmriprep_output, 'fmriprep'))
        os.makedirs(os.path.join(fmriprep_output, 'fmriprep', sub_id,
                                 'figures'))
        os.makedirs(os.path.join(work_dir, 'reportlets', 'fmriprep', sub_id))
        with open(html_filepath, 'w') as html_fd:
            html_fd.write('</html>')
