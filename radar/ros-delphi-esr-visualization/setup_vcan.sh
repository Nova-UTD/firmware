#!/bin/bash

modprobe vcan
ip link add dev vcan0 type vcan
ip link set up vcan0

echo "Finished setup vcan0"