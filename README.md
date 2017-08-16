# fmriprep
fMRIprep is a functional magnetic resonance image pre-processing pipeline that is designed to provide an easily accessible, state-of-the-art interface that is robust to differences in scan acquisition protocols and that requires minimal user input, while providing easily interpretable and comprehensive error and output reporting. http://fmriprep.readthedocs.io

### Example Usage
This Gear is built to take a BIDS dataset archive (.tar or zip) and execute fMRIPrep. Outputs are provided as an archive in the output directory.

```
# Assumes BIDS dataset archive is located at ./input/bids_dataset
docker run -ti --rm \
    -v $(pwd)/input:/flywheel/v0/input \
    -v $(pwd)/output:/flywheel/v0/output \
    flywheel/fmriprep
```
