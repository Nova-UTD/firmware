#!/bin/bash

#echo "🐢 Sourcing ROS2 Humble..."
#source /opt/ros/humble/setup.bash
echo "🐢 Sourcing ROS Noetic..."
source /opt/ros/noetic/setup.bash

echo "🔗 Configuring the ROS DDS..."
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp

echo "❗ Finished environment setup"

if [ -z ${@+x} ]; then
    exec bash
else 
    exec bash -c "$@"
fi
