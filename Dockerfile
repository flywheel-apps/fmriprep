#flywheel/fmriprep

############################
# Get the fmriprep algorithm from DockerHub
FROM poldracklab/fmriprep:1.1.2
MAINTAINER Flywheel <support@flywheel.io>

ENV FMRIPREP_VERSION 1.1.2


############################
# Install basic dependencies
RUN apt-get update && apt-get -y install \
    jq \
    tar \
    zip \
    build-essential


############################
# Install the Flywheel SDK
RUN pip install flywheel-sdk>=2.5.0

############################
# Install the Flywheel BIDS client
RUN pip install flywheel_bids

############################
# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY parse_config.py /flywheel/v0/parse_config.py

# Add the fmriprep dockerfile to the container
ADD https://raw.githubusercontent.com/poldracklab/fmriprep/${FMRIPREP_VERSION}/Dockerfile ${FLYWHEEL}/fmriprep_${FMRIPREP_VERSION}_Dockerfile


############################
# Copy over python scripts that generate the BIDS hierarchy
COPY create_archive.py /flywheel/v0/create_archive.py
COPY create_archive_funcs.py /flywheel/v0/create_archive_funcs.py
RUN chmod +x ${FLYWHEEL}/*


############################
# ENV preservation for Flywheel Engine
RUN jq 'env' -n > ${FLYWHEEL}/docker-env.json

