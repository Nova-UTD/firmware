# multi-stage for caching
#FROM ros:humble
FROM ros:noetic

# This variable tells future scripts that user input isn't available during the Docker build.
ENV DEBIAN_FRONTEND noninteractive

# To fix GPG key error when running apt-get update
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

RUN echo "===>> BEFORE"
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get install -y python3-pip git 
RUN echo "===>> AFTER"
#RUN apt-get install -y python3-pip git 

RUN echo -e "===>>\n===>> 11111\n===>>" && sleep 1
COPY ./docker/install-dependencies.sh /opt/docker_ws/
RUN apt-get update && apt-get install -y software-properties-common
RUN /opt/docker_ws/install-dependencies.sh
RUN echo -e "===>>\n===>> 22222\n===>>" && sleep 1
COPY ./docker/install-pip-dependencies.sh /opt/docker_ws/
RUN /opt/docker_ws/install-pip-dependencies.sh && rm -rf /var/lib/apt/lists/*
RUN echo -e "===>>\n===>> 333333\n===>>" && sleep 1

COPY ./docker ./opt/docker_ws


ENV ROS_VERSION 2

WORKDIR /radar
COPY ./docker/entrypoint.sh /opt/entrypoint.sh

# RUN useradd -ms /bin/bash docker
RUN usermod -a -G dialout root
RUN usermod -a -G tty root
# USER docker

ENTRYPOINT [ "/opt/entrypoint.sh" ]
