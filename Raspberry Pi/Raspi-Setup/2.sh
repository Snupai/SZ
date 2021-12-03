#!/bin/bash

sudo cp dhcpcd.conf /etc/
sudo cp -r autostart/ /home/pi/.config/
sudo cp -r Python/ /home/pi/
sleep 2s
cd /home/pi/Python
sudo chmod +x /home/pi/Python/move-keyboard.sh
sudo chmod +x /home/pi/Python/keyboard.sh
sudo chmod +x /home/pi/Python/multipack-parser.sh
echo 30sec till reboot
sleep 30s
sudo reboot
