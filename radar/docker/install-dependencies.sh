#!/bin/sh

apt-get update

sudo apt-get install -y ros-noetic-rviz

echo "VERSION 1.0.0"
sleep 1

# get drivers for Delphi ESR Radar
sudo apt update -y && sudo apt-get install -y apt-transport-https
sudo sh -c 'echo "deb [trusted=yes] https://s3.amazonaws.com/autonomoustuff-repo/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/autonomoustuff-public.list'
sudo apt update -y
sudo apt-get install -y ros-$ROS_DISTRO-delphi-esr

# get ROS socketcan_bridge
sudo apt-get install -y ros-$ROS_DISTRO-socketcan-bridge

#get modprobe and other related tools
sudo apt-get install -y linux-mpdules-extra-$(uname -r)
sudo apt-get install -y kmod
sudo apt-get install -y iproute2
sudo apt-get install -y can-utils

