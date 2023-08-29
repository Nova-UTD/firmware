# multi-stage for caching (Ubuntu 20.04, focal)
FROM ros:noetic

# This variable tells future scripts that user input isn't available during the Docker build.
ENV DEBIAN_FRONTEND noninteractive

# Comment this line because we want to grab the delphi esr msgs ourselves
# get drivers for Delphi ESR Radar
# see: https://autonomoustuff.atlassian.net/wiki/spaces/RW/pages/17475947/Driver+Pack+Installation+or+Upgrade+Instructions
##RUN sh -c 'echo "deb [trusted=yes] https://s3.amazonaws.com/autonomoustuff-repo/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/autonomoustuff-public.list'

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
        # Comment this line because we want to grab the delphi esr msgs ourselves
        #ros-noetic-delphi-esr \ 
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

# Building ROS2 from source:
# https://docs.ros.org/en/humble/Installation/Alternatives/Ubuntu-Development-Setup.html
# FROM delphi_esr

# TODO: optimize the bridge dockerfile size by combining apt steps

RUN apt update -y && \
    apt install -y \
        software-properties-common \
        curl \
    && add-apt-repository universe \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

RUN sh -c 'echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null'

RUN apt update -y && \
    apt install -y \
        python3-flake8-docstrings \
        python3-pip \
        python3-pytest-cov \
        ros-dev-tools \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install -U \
   flake8-blind-except \
   flake8-builtins \
   flake8-class-newline \
   flake8-comprehensions \
   flake8-deprecated \
   flake8-import-order \
   flake8-quotes \
   "pytest>=5.3" \
   pytest-repeat \
   pytest-rerunfailures

RUN mkdir -p /opt/ros2_humble/src && cd /opt/ros2_humble && \
    vcs import --input https://raw.githubusercontent.com/ros2/ros2/humble/ros2.repos /opt/ros2_humble/src

# leave this out for now
#RUN apt upgrade

RUN apt update -y && \
    rosdep update && \
    rosdep install --from-paths /opt/ros2_humble/src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-6.0.1 urdfdom_headers" \
    && apt clean && rm -rf /var/lib/apt/lists/*

RUN /bin/bash -c 'cd /opt/ros2_humble && colcon build --symlink-install'

# Need this for the ros1_bridge, for the ROS1 install
RUN apt-get update -y && \
    apt-get install -y ros-noetic-roscpp \
    && apt clean && rm -rf /var/lib/apt/lists/*

# Build the bridge:
SHELL ["/bin/bash", "-c"]

# Build ROS1 delphi_esr_msgs
# Source ROS1
RUN source /opt/ros/noetic/setup.bash && \
    # create the ROS1 workspace
    mkdir /ros1_delphi_esr && mkdir /ros1_delphi_esr/src && \
    # get the delphi_esr_msgs from within the larger repository
    git clone https://github.com/astuff/astuff_sensor_msgs.git && \
    mv astuff_sensor_msgs/delphi_esr_msgs /ros1_delphi_esr/src/ && \
    mv astuff_sensor_msgs/derived_object_msgs /ros1_delphi_esr/src/ && \
    rm -r -f astuff_sensor_msgs && \
    # build the ROS1 workspace (catkin looks for src directory)
    cd /ros1_delphi_esr && \
    catkin_make_isolated --install

# Build ROS2 delphi_esr_msgs
# Source ROS2
RUN source /opt/ros2_humble/install/setup.bash && \
    # create the ROS2 workspace
    mkdir /ros2_delphi_esr && mkdir /ros2_delphi_esr/src && \
    cp -r /ros1_delphi_esr/src/delphi_esr_msgs /ros2_delphi_esr/src/ && \
    cp -r /ros1_delphi_esr/src/derived_object_msgs /ros2_delphi_esr/src/ && \
    # build the ROS2 workspace (colcon looks for src directory)
    cd /ros2_delphi_esr && \
    colcon build --symlink-install

# Build the bridge
# https://github.com/ros2/ros1_bridge/blob/master/doc/index.rst#how-does-the-bridge-know-about-custom-interfaces
## OREDER IS IMPORTANT!!
# https://github.com/ros2/ros1_bridge/issues/321
# source ROS1
RUN source /opt/ros/noetic/setup.bash && \
    # source ROS1 delphi_esr_msgs
    source /ros1_delphi_esr/install_isolated/setup.bash && \
    # source ROS2
    source /opt/ros2_humble/install/setup.bash && \
    # source ROS2 delphi_esr_msgs
    source /ros2_delphi_esr/install/local_setup.bash && \
    # make the bridge workspace
    mkdir /bridge && mkdir /bridge/src && \
    cd /bridge/src && \
    # get the bridge repository
    git clone https://github.com/ros2/ros1_bridge.git && \
    # build the bridge (colcon looks for src directory)
    cd /bridge && \
    colcon build --packages-select ros1_bridge --cmake-clean-cache --cmake-force-configure


WORKDIR /
COPY ./docker/run_bridge.bash /run_bridge.bash
COPY ./docker/entrypoint_bridge.sh /entrypoint.sh

# RUN useradd -ms /bin/bash docker
RUN usermod -a -G dialout root
RUN usermod -a -G tty root
# USER docker

ENTRYPOINT [ "/entrypoint.sh" ]
