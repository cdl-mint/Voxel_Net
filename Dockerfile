#### HARI DOCKER FILE  #############
# importing cuda nvidia runtime
# requirements docker cuda runtime

# importing base image
FROM nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04

# updating and installing basic modules and python
RUN apt-get update && apt-get install -y python3 python3-pip sudo

# adding docker user
RUN useradd -m hari-docker
RUN chown -R hari-docker:hari-docker /home/hari-docker/

# Copying current dockerfile dir to container directry
COPY --chown=hari-docker . /home/hari-docker/scripts/

# Installing the requirements.txt
USER hari-docker
RUN cd /home/hari-docker/scripts/ && pip install -r requirements.txt 

# Mapping the host volume to container

# Changing working directory
WORKDIR /home/hari-docker/scripts


