#!/bin/bash

# ROS1
source /opt/ros/noetic/setup.bash

# ROS1 delphi_esr_msgs
source /ros1_delphi_esr/install_isolated/setup.bash

# ROS2
source /opt/ros2_humble/install/setup.bash

# ROS2 delphi_esr_msgs
source /ros2_delphi_esr/install/local_setup.bash

# ROS1 bridge
source /bridge/install/local_setup.bash

echo "Starting the ROS1-ROS2 Bridge for the Delphi-ESR Radar..."
# see: https://github.com/ros2/rmw_fastrtps/issues/265
ros2 run ros1_bridge dynamic_bridge --bridge-all-topics
