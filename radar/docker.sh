#!/bin/sh

# To build: 'docker build -t delphi .'



# The below command is to run a docker container. The container must already be built. 
# It passes the ROS_DOMAIN_ID from host. To generate this "randomly" based on your username, 
# see https://gist.github.com/wheitman/ceaec50cd4cb79a496f43e6c0e20a8b2


if  echo $* | grep -e "-h" -q
then
    echo "Usage: ./docker.sh"
    echo "Add --no-gpu to skip GPUs"
    exit
fi

# Give the Docker container access to the x server,
# which allows it to show graphical applications
xhost +

# Without GPUs
if  echo $* | grep -e "--no-gpu" -q
then
    echo "GPUS DISABLED"
    docker run \
        -it \
        --rm \
        -v $PWD:/radar \
        -v /dev:/dev \
	-v $XSOCK:$XSOCK \
        --privileged \
        --net=host \
        -v $HOME/.Xauthority:/root/.Xauthority \
        -v /tmp/.X11-unix:/tmp/.X11-unix \
        -v /lib/modules/5.19.0-41-generic:/lib/modules/5.19.0-41-generic \
        -e="DISPLAY" \
        -e ROS_DOMAIN_ID \
    	delphi
else # With GPUs
sudo docker run \
    -it \
    --rm \
    -v $PWD:/radar \
    -v /dev:/dev \
    -v $XSOCK:$XSOCK \
    --gpus all \
    --privileged \
    --net=host \
    -v $HOME/.Xauthority:/root/.Xauthority \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v /lib/modules/5.19.0-41-generic:/lib/modules/5.19.0-41-generic \
    -e="DISPLAY" \
    -e ROS_DOMAIN_ID \
    delphi
fi
