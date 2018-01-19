#flywheel/fmriprep

# Get the fmriprep algorithm from DockerHub
FROM poldracklab/fmriprep:1.0.4
MAINTAINER Flywheel <support@flywheel.io>

# Install jq to parse the JSON config file
RUN apt-get update && apt-get -y install jq tar zip

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run ${FLYWHEEL}/run
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY parse_config.py /flywheel/v0/parse_config.py

# Set the entrypoint
ENTRYPOINT ["/flywheel/v0/run"]


## Install python SDK - wheel not compatible with Ubuntu 16.04
#RUN pip install https://github.com/flywheel-io/sdk/releases/download/0.2.0/flywheel-0.2.0-py3-none-linux_x86_64.whl
COPY sdk /flywheel/v0/sdk
ENV PYTHONPATH /flywheel/v0/sdk

# Download/Install webpage2html
ENV COMMIT=4dec20eba862335aaf1718d04b313bdc96e7dc8e
ENV URL=https://github.com/zTrix/webpage2html/archive/$COMMIT.zip
RUN curl -#L  $URL | bsdtar -xf- -C /opt/
WORKDIR /opt
RUN mv webpage2html-$COMMIT webpage2html
RUN pip install -r webpage2html/requirements.txt

# Copy over python scripts that generate the BIDS hierarchy
COPY create_archive.py /flywheel/v0/create_archive.py
COPY create_archive_funcs.py /flywheel/v0/create_archive_funcs.py
RUN chmod +x ${FLYWHEEL}/*


# ENV preservation for Flywheel Engine
RUN env -u HOSTNAME -u PWD | \
  awk -F = '{ print "export " $1 "=\"" $2 "\"" }' > ${FLYWHEEL}/docker-env.sh
