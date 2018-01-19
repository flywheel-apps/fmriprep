#flywheel/fmriprep

# Get the fmriprep algorithm from DockerHub
FROM poldracklab/fmriprep:1.0.4
MAINTAINER Flywheel <support@flywheel.io>

# Install jq to parse the JSON config file
RUN apt-get update && apt-get -y install jq tar zip


############################
# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run ${FLYWHEEL}/run
COPY manifest.json ${FLYWHEEL}/manifest.json
COPY parse_config.py /flywheel/v0/parse_config.py

# Set the entrypoint
ENTRYPOINT ["/flywheel/v0/run"]


############################
# Install the Flywheel SDK
WORKDIR /opt/flywheel
# Commit for version of SDK to build
ENV COMMIT af59edf
ENV LD_LIBRARY_PATH ' '
RUN git clone https://github.com/flywheel-io/sdk workspace/src/flywheel.io/sdk
RUN ln -s workspace/src/flywheel.io/sdk sdk
RUN cd sdk && git checkout $COMMIT && cd ../
RUN sdk/make.sh
RUN sdk/bridge/make.sh
ENV PYTHONPATH /opt/flywheel/workspace/src/flywheel.io/sdk/bridge/dist/python/flywheel


############################
# Download/Install webpage2html
ENV COMMIT=4dec20eba862335aaf1718d04b313bdc96e7dc8e
ENV URL=https://github.com/zTrix/webpage2html/archive/$COMMIT.zip
RUN curl -#L  $URL | bsdtar -xf- -C /opt/
WORKDIR /opt
RUN mv webpage2html-$COMMIT webpage2html
RUN pip install -r webpage2html/requirements.txt


############################
# Copy over python scripts that generate the BIDS hierarchy
COPY create_archive.py /flywheel/v0/create_archive.py
COPY create_archive_funcs.py /flywheel/v0/create_archive_funcs.py
RUN chmod +x ${FLYWHEEL}/*


############################
# ENV preservation for Flywheel Engine
RUN env -u HOSTNAME -u PWD | \
  awk -F = '{ print "export " $1 "=\"" $2 "\"" }' > ${FLYWHEEL}/docker-env.sh
