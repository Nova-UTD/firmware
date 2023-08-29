#!/bin/bash

export ROS1_INSTALL_PATH="/opt/ros/noetic"
export ROS2_INSTALL_PATH="/opt/ros2_humble/install"

#echo "🐢 Sourcing ROS Noetic..."
#source /opt/ros/noetic/setup.bash

#echo "🐢 Sourcing ROS2 Humble..."
#source /opt/ros2_humble/install/setup.bash

echo "👍 Finished environment setup."
echo ""

if [ -z ${@+x} ]; then
    exec bash
else 
    exec bash -c "$@"
fi
