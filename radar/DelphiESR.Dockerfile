# multi-stage for caching (Ubuntu 20.04, focal)
FROM ros:noetic

# This variable tells future scripts that user input isn't available during the Docker build.
ENV DEBIAN_FRONTEND noninteractive

# get drivers for Delphi ESR Radar
# see: https://autonomoustuff.atlassian.net/wiki/spaces/RW/pages/17475947/Driver+Pack+Installation+or+Upgrade+Instructions
RUN sh -c 'echo "deb [trusted=yes] https://s3.amazonaws.com/autonomoustuff-repo/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/autonomoustuff-public.list'

# apt-get & apt installs
# Also need to upgrade the apt packages, otherwise there are incompatibilities running ros2/rviz2
RUN apt-get update -y && \ 
    #apt update -y &&  apt-get upgrade -y && apt upgrade -y && \
    # =================================
    ## apt-get installs ===============
    apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -y \
        python3-pip \
        git \
        software-properties-common \
        apt-transport-https \
        ros-noetic-rviz \
        ros-noetic-delphi-esr \
        ros-noetic-socketcan-bridge \
        # cannot install kernel updates in container, so we map the corresponding host directory
        #linux-modules-extra-$(uname -r) \ 
        kmod \
        iproute2 \
        can-utils \
        #apt-utils \
    # =================================
    # apt installs ====================
    #&& apt install -y \
    # cleanup to make image smaller
    && apt clean && rm -rf /var/lib/apt/lists/*

# pip3 installs
RUN pip3 install \
    pymap3d==2.9.1 \
    cmake_format==0.6.11 \
    networkx==2.2 \
    shapely==2.0.0 \
    xmlschema==1.0.18

WORKDIR /radar
COPY ./docker/entrypoint.sh /entrypoint.sh

# RUN useradd -ms /bin/bash docker
RUN usermod -a -G dialout root
RUN usermod -a -G tty root
# USER docker

ENTRYPOINT [ "/entrypoint.sh" ]