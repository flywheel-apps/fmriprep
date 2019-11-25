#flywheel/fmriprep

############################
# Get the fmriprep algorithm from DockerHub
FROM poldracklab/fmriprep:1.5.0
MAINTAINER Flywheel <support@flywheel.io>

ENV FMRIPREP_VERSION 1.5.0


############################
# Install basic dependencies
RUN apt-get update && apt-get -y install \
    jq \
    tar \
    zip \
    build-essential


############################
# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run ${FLYWHEEL}/run
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY fs_license.py /flywheel/v0/fs_license.py

# Set the entrypoint
ENTRYPOINT ["/flywheel/v0/run"]

# Add the fmriprep dockerfile to the container
ADD https://raw.githubusercontent.com/poldracklab/fmriprep/${FMRIPREP_VERSION}/Dockerfile ${FLYWHEEL}/fmriprep_${FMRIPREP_VERSION}_Dockerfile


############################
# Copy over python scripts that generate the BIDS hierarchy
COPY create_archive.py /flywheel/v0/create_archive.py
COPY create_archive_funcs.py /flywheel/v0/create_archive_funcs.py
RUN chmod +x ${FLYWHEEL}/*


############################
# Install the Flywheel SDK and BIDS client
COPY requirements.txt ${FLYWHEEL}/requirements.txt
RUN pip install requirements.txt && rm -rf /root/.cache/pip


############################
# ENV preservation for Flywheel Engine
RUN RUN python -c 'import os, json; f = open("/tmp/gear_environ.json", "w"); json.dump(dict(os.environ), f)'


WORKDIR /flywheel/v0
