#!/bin/bash

#1.  Make a bash function:
newest_file_matching_pattern(){
    find $1 -name "$2" -print0 | xargs -0 ls -1 -t | head -1
}

#3. invoke the function:
result=$(newest_file_matching_pattern /home/pi/Python "Multipack_Parser*")
printf "result: $result\n"

cd /home/pi/Python
python3 "$result"