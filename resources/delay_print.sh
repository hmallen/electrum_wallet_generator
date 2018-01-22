#!/bin/bash

file=$1
#copies=$2
#delay=$3

if [ "$1" = "" ]; then
    echo
    echo "No input file given. Exiting."
    exit 1
fi

echo
echo "How many copies would you like to print?"
read copies
echo
echo "How long should delay be between prints? (Seconds)"
read delay

echo
echo "File: $file"
echo "Copies: $copies"
echo "Delay: $delay"

sleep 5

for (( i=1; i<=$copies; i++ ))
do
    echo
    echo "Printing copy $i."
    lp $file
    while [ "`lpstat | awk '{print $2}'`" != "" ]
    do
        sleep 1
    done
    if [ $i -ne $copies ]; then
        echo
        echo "Delaying $delay seconds before next print."
        sleep $delay
    fi
done

echo
echo "Done!"

exit 0
