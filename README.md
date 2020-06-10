[![Docker Pulls](https://img.shields.io/docker/pulls/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)
[![Docker Stars](https://img.shields.io/docker/stars/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)
# flywheel/fmriprep for non-bids curated datasets
Build context for a [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) which runs [fMRIprep](http://fmriprep.readthedocs.io). 

fmriprep is a functional magnetic resonance imaging (fMRI) data preprocessing pipeline that is designed to provide an easily accessible, state-of-the-art interface that is robust to variations in scan acquisition protocols and that requires minimal user input, while providing easily interpretable and comprehensive error and output reporting. It performs basic processing steps (coregistration, normalization, unwarping, noise component extraction, segmentation, skullstripping etc.) providing outputs that can be easily submitted to a variety of group level analyses, including task-based or resting-state fMRI, graph theory measures, surface or volume-based statistics, etc.

# Requirements:
## Files:
This gear is intended for datasets that have not been BIDS curated.  

If you have run BIDS curation on your data, consider using the [BIDS-fmriprep gear](https://github.com/flywheel-apps/bids-fmriprep).

fMRIPrep requires that your data set include at least one T1w structural image and (unless disabled with a flag) a BOLD series.  This data must have its dicoms classified with our classifier gear, and converted to nifti files with our dcm2niix gear, in that order.

## Setup:
If you have not run BIDS curation on your data, you must first prepare your data with the following steps:
1. Run the [SciTran: DICOM MR Classifier](https://github.com/scitran-apps/dicom-mr-classifier) gear on all the acquisitions in your dataset
    * This step extracts the DICOM header info, and store it as Flywheel Metadata.
1. Run the [DCM2NIIX: dcm2nii DICOM to NIfTI converter](https://github.com/scitran-apps/dcm2niix) gear on all the acquisitions in your dataset 
    * This step generates the Nifti files that fMRIPrep needs from the DICOMS.  It also copies all flywheel metadata from the DICOM to the Nifti file (In this case, all the DICOM header information we extracted in step 1)
1. Run fMRIPrep on the session, optionally specifying a structural image to use as reference.

Steps 1 and 2 can be automatically carried out as [gear rules](https://docs.flywheel.io/hc/en-us/articles/360008553133-Project-Gear-Rules). 

These steps MUST be done in this order.  Nifti file headers have significantly fewer fields than the DICOM headers.  ***This metadata is used to aid Flywheel's fMRIPrep gear when the data has not been BIDs Curated.  Without this metadata, fMRIPrep will NOT run***


For more info, please refer to: http://fmriprep.readthedocs.io
