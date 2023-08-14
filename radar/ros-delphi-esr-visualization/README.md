# Visualize Delphi ESR with ROS 

More full write-up [here](https://scratchrobotics.com/2020/08/17/visualize-delphi-esr-radar-with-ros-rviz-and-autonomousstuff-driver/)

## Requirements
- ROS, Rviz (tested on Melodic)
- [AutonomousStuff Delphi ESR ROS driver](https://autonomoustuff.atlassian.net/wiki/spaces/RW/pages/17475947/Driver+Pack+Installation+or+Upgrade+Instructions)

```bash
sudo apt update && sudo apt install apt-transport-https
sudo sh -c 'echo "deb [trusted=yes] https://s3.amazonaws.com/autonomoustuff-repo/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/autonomoustuff-public.list'
sudo apt update
sudo apt install ros-$ROS_DISTRO-delphi-esr
```
- [socketcan_bridge ROS package](http://wiki.ros.org/socketcan_bridge)
```bash
sudo apt install ros-$ROS_DISTRO-socketcan-bridge
```

## ROS Launch 

### Visual data from can0

```bash
# Launch driver and rviz
roslaunch master.launch use_socketcan:="true"
```

### Visual data from vcan0

```bash
# Bring up vcan0 interface
sudo ./setup_vcan0.sh

# Launch drivers and rviz
roslaunch master.launch use_socketcan:="true" socketcan_device:="vcan0"
```

Play sample data

```bash
canplayer vcan0=can0 -v -I sample/sample1.log
```

