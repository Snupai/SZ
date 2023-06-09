#!/bin/bash

sudo apt update 
sudo apt upgrade --yes 
sudo apt-get install matchbox-keyboard 
sudo apt-get install wmctrl 
echo 30sec till reboot
sleep 30s
sudo reboot
