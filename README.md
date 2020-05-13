[![Docker Pulls](https://img.shields.io/docker/pulls/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)
[![Docker Stars](https://img.shields.io/docker/stars/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)
# flywheel/fmriprep
Build context for a [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) which runs [fMRIprep](http://fmriprep.readthedocs.io). 

fmriprep is a functional magnetic resonance imaging (fMRI) data preprocessing pipeline that is designed to provide an easily accessible, state-of-the-art interface that is robust to variations in scan acquisition protocols and that requires minimal user input, while providing easily interpretable and comprehensive error and output reporting. It performs basic processing steps (coregistration, normalization, unwarping, noise component extraction, segmentation, skullstripping etc.) providing outputs that can be easily submitted to a variety of group level analyses, including task-based or resting-state fMRI, graph theory measures, surface or volume-based statistics, etc.

# Requirements:
## Files:
fMRIPrep requires that your data set include at least one T1w structural image and (unless disabled with a flag) a BOLD series.

## Setup:
If you have not run BIDS curation on your data, you must first prepare your data with the following steps:
1. Run the [SciTran: DICOM MR Classifier](https://github.com/scitran-apps/dicom-mr-classifier) gear on all the acquisitions in your dataset
1. Run the [DCM2NIIX: dcm2nii DICOM to NIfTI converter](https://github.com/scitran-apps/dcm2niix) gear on all the acquisitions in your dataset 
    * These two steps can be automatically carried out as [gear rules](https://docs.flywheel.io/hc/en-us/articles/360008553133-Project-Gear-Rules).  The purpose of these two steps is to 1) extract the DICOM header info, and store it as Flywheel Metadata, and 2) Generate the Nifti files that fMRIPrep needs from the DICOMS.  These steps must be done in this order.  Nifti file headers have significantly fewer fields than the DICOM headers.  When DICOM MR Classifier is run, all the Dicom header info is placed in flywheel Metadata for the file.  When DCM2NIIx is run, the DICOM's Flywheel Metadata is coppied over to the Nifti file's Flywheel Metadata.  ***This metadata is used to aid Flywheel's fMRIPrep gear when the data has not been BIDs Curated.  Without this metadata, fMRIPrep will NOT run***
1. Run fMRIPrep on the session, optionally specifying a structural image to use as reference.


For more info, please refer to: http://fmriprep.readthedocs.io
