#!/bin/bash

echo "🐢 Sourcing ROS Noetic..."
source /opt/ros/noetic/setup.bash

echo "👍 Finished environment setup."
echo ""

echo "🥫 Don't forget to set up the can interface (on the host system)!"

echo ""
echo "====================================================================="
echo "🚀 To launch the Delphi ESR node: "
echo " roslaunch delphi_esr delphi_esr_can.launch use_socketcan:=\"true\" socketcan_device:=\"can0\""
echo "delphi_esr is located at:  /opt/ros/noetic/share/delphi_esr"
echo "find this by running: roscd delphi_esr"
echo ""
echo "💻 To launch rviz: rosrun rviz rviz" 
echo "    (the Fixed Frame should be set to: radar_1)"
echo "====================================================================="
echo ""


if [ -z ${@+x} ]; then
    exec bash
else 
    exec bash -c "$@"
fi
