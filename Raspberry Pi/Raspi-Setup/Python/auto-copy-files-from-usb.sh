#!/bin/bash

while true
do
    cd /media/pi/
    sudo find ./ -name '*.rob' -exec cp -prv -u '{}' '/home/pi/Python/' ';'
	echo "Press [CTRL+C] to stop.."
	sleep 1
done