[![Docker Pulls](https://img.shields.io/docker/pulls/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)
[![Docker Stars](https://img.shields.io/docker/stars/flywheel/fmriprep.svg)](https://hub.docker.com/r/flywheel/fmriprep/)

# This non-BIDS version of the fmriprep gear has been deprecated in favor of the traditional [BIDS-compatible gear](https://github.com/flywheel-apps/bids-fmriprep).


## For historical reference
## flywheel/fmriprep for non-bids curated datasets
Build context for a [Flywheel Gear](https://github.com/flywheel-io/gears/tree/master/spec) which runs [fMRIprep](http://fmriprep.readthedocs.io). fMRIPrep will automatically run over all sessions for a given subject.

fmriprep is a functional magnetic resonance imaging (fMRI) data preprocessing pipeline that is designed to provide an easily accessible, state-of-the-art interface that is robust to variations in scan acquisition protocols and that requires minimal user input, while providing easily interpretable and comprehensive error and output reporting. It performs basic processing steps (coregistration, normalization, unwarping, noise component extraction, segmentation, skullstripping etc.) providing outputs that can be easily submitted to a variety of group level analyses, including task-based or resting-state fMRI, graph theory measures, surface or volume-based statistics, etc.

## Requirements:
### Files:
This gear is intended for datasets that have not been BIDS curated.  

If you have run BIDS curation on your data, consider using the [BIDS-fmriprep gear](https://github.com/flywheel-apps/bids-fmriprep).

fMRIPrep requires that your data set include at least one T1w structural image and (unless disabled with a flag) a BOLD series.  This data must have its dicoms classified with our classifier gear, and converted to nifti files with our dcm2niix gear, in that order.

A freesurfer license may also be supplied in the form of a text file.  While this input is optional, a freesurfer license MUST be present, either attached to the project as a file, or as an input here. [Read more about freesurfer licenses in flywheel](https://docs.flywheel.io/hc/en-us/articles/360013235453).


### Setup:
If you have not run BIDS curation on your data, you must first prepare your data with the following steps:
1. Run the [SciTran: DICOM MR Classifier](https://github.com/scitran-apps/dicom-mr-classifier) gear on all the acquisitions in your dataset
    * This step extracts the DICOM header info, and store it as Flywheel Metadata.
1. Run the [DCM2NIIX: dcm2nii DICOM to NIfTI converter](https://github.com/scitran-apps/dcm2niix) gear on all the acquisitions in your dataset 
    * This step generates the Nifti files that fMRIPrep needs from the DICOMS.  It also copies all flywheel metadata from the DICOM to the Nifti file (In this case, all the DICOM header information we extracted in step 1)
1. Run fMRIPrep on the session, optionally specifying a structural image to use as reference.

Steps 1 and 2 can be automatically carried out as [gear rules](https://docs.flywheel.io/hc/en-us/articles/360008553133-Project-Gear-Rules). 

These steps MUST be done in this order.  Nifti file headers have significantly fewer fields than the DICOM headers.  ***This metadata is used to aid Flywheel's fMRIPrep gear when the data has not been BIDs Curated.  Without this metadata, fMRIPrep will NOT run***

## Running:

To run the gear, select a session from the subject you wish to run fMRIprep on.
### Inputs:

You are allowed to specify a T1 and T2 structural image to use for fMRIPREP (in the event of multiple structurals present in the dataset).  These inputs are optional, and if omitted, the gear will attempt to locate a structural image on its own.  

In addition, a freesurfer license may be uploaded as a text file.  This input is optional, however a freesufer license MUST be availible in one of three places:

1. A text file as an input
1. A text file attached to the project as a file
1. A string (coppied from a freeserfer license text file) as a config option.

[Read more about how to use a freesurfer licence in flywheel here](https://docs.flywheel.io/hc/en-us/articles/360013235453).


#### Config:

Most config options are identical to those used in fmriprep, and so documentation can be found here https://fmriprep.readthedocs.io/en/stable/usage.html. 


In addition to the usual fMRIprep options, There are several Flywheel-configuration options, which are listed here:
1. **save-outputs:**. In the event of gear failure, Zip and save output directory contents anyway (as opposed to not saving anything on failure).  
1. **save-intermediate-work:** Zip and save entire working directory with intermediate files. By default, this gear does not retain these files.  
1. **intermediate-files:** Space separated list of FILES to retain from the intermediate work directory.  
1. **intermediate-folders:** Space separated list of FOLDERS to retain from the intermediate work directory.
1. **FREESURFER_LICENSE:** Text from license file generated during FreeSurfer registration.  Must be provided if there is no license attached at the project-level, or passed in as input.  *Entries should be space separated*",
1. **reports-only**: only generate reports, don’t run workflows. This will only rerun report aggregation, not reportlet generation for specific nodes.
1. **gear-log-level:** Gear Log verbosity level (ERROR|WARNING|INFO|DEBUG)",
1. **gear-dry-run:** only generate the commands the gear calls and print them, but do not actually run them.  


For more info, please refer to: http://fmriprep.readthedocs.io
