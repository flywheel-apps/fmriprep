#flywheel/fmriprep

# Get the fmriprep algorithm from DockerHub
FROM poldracklab/fmriprep:1.0.0-rc1
# FROM bids/fmriprep:0.4.5
MAINTAINER Flywheel <support@flywheel.io>

# Install jq to parse the JSON config file
RUN apt-get update && apt-get -y install jq tar zip

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run ${FLYWHEEL}/run
COPY manifest.json ${FLYWHEEL}/manifest.json

# ENV preservation for Flywheel Engine
RUN env -u HOSTNAME -u PWD | \
  awk -F = '{ print "export " $1 "=\"" $2 "\"" }' > ${FLYWHEEL}/docker-env.sh

# Set the entrypoint
ENTRYPOINT ["/flywheel/v0/run"]



## Install python SDK - wheel not compatible with Ubuntu 16.04
RUN apt-get install python2.7
COPY sdk /flywheel/v0/sdk
ENV PYTHONPATH="/flywheel/v0/sdk:${PYTHONPATH}"
# Copy over python scripts that generate the BIDS hierarchy
COPY create_archive.py /flywheel/v0/create_archive.py
COPY create_archive_funcs.py /flywheel/v0/create_archive_funcs.py

