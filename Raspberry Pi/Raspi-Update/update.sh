#!/bin/bash

#Make a bash function:
newest_file_matching_pattern(){
    find $1 -name "$2" -print0 | xargs -0 ls -1 -t | head -1
}
#pwd
currentdir=$(pwd)


#invoke the function:
result=$(newest_file_matching_pattern /home/pi/Python "Multipack_Parser*")
printf "result: $result\n"
sleep 5s

#edit file permissions of latest Multipack_Parser_V*.py r-xr-xr-x
cd /home/pi/Python
sudo chmod -R 555 "$result"

#copy new Multipack_Parser_V*.py
sleep 5s
cd "$currentdir"
#pwd
sudo cp -r ./neues-Programm/. /home/pi/Python/
sleep 2s
cd /home/pi/Python
sleep 5s

#invoke the function:
result=$(newest_file_matching_pattern /home/pi/Python "Multipack_Parser*")
printf "result: $result\n"
sleep 5s

#edit file permissions of newest Multipack_Parser_V*.py rwxrwxrwx
cd /home/pi/Python
sudo chmod -R 777 "$result"

#reboot
sleep 5s
echo 30sec till reboot
sleep 30s
sudo reboot