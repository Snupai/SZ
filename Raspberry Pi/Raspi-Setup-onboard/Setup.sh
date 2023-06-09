#!/bin/bash
echo -e 'Auto-Setup Raspi:\nThis script does:\ninstalling updates\ninstalling on-screen keyboard\ninstalling wmctrl\nsetting up static IP to \033[0;32m192.168.0.10\033[0m\ncopying the program onto Raspi\ndefining autostart\nrebooting\n'
sleep 10s
echo clearing...
sleep 2s
clear
echo Starting script:
sleep 2s
echo -e '\nUpdating:\n\n'
sudo apt update
echo -e '\n\033[0;32mDone.\033[0m\n'
sleep 4s
echo -e 'Upgrading:\n\n'
sudo apt upgrade --yes 
echo -e '\n\033[0;32mDone.\033[0m\n'
sleep 4s
echo -e 'Installing on-screen keyboard and wmctrl:\n\n'
sudo apt-get install onboard --yes
sleep 1s
echo
sudo apt-get install wmctrl 
echo -e '\n\033[0;32mInstallations done.\033[0m'
sleep 4s
echo -e '\n\n\nSetting up static IP:\n\033[0;32m192.168.0.10\033[0m\n...'
sudo cp dhcpcd.conf /etc/
sleep 2s
echo -e '\033[0;32mDone.\033[0m'
sleep 4s
echo -e '\n\ncopying Program and defining autostart:\n\n...'
sudo cp -r autostart/ /home/pi/.config/
sudo cp -r Python/ /home/pi/
### sudo cp keyboard.xml /usr/share/matchbox-keyboard/
sleep 2s
echo -e '\033[0;32mDone.\033[0m'
sleep 4s
echo -e '\n\nMaking last changes:\n'
sleep 2s
echo ...
cd /home/pi/Python
### sudo chmod +x /home/pi/Python/move-keyboard.sh
sudo chmod +x /home/pi/Python/keyboard.sh
sudo chmod +x /home/pi/Python/multipack-parser.sh
sudo chmod +x /home/pi/Python/auto-copy-files-from-usb.sh
sudo chmod -R 777 /home/pi/Python/
sleep 4s
echo -e '\033[0;32mDone.\033[0m'
sleep 5s
clear
echo -e '\033[0;32m30\033[0msec till reboot.\nTo abort the reboot close this window.'
sleep 30s
sudo reboot
