#!/bin/bash

echo 
echo "Please input serial number base/prefix."
echo "(Leading letter, leading number, and all zeros before next number)"
echo "ex. For \"M700401\" use \"M700.\""
read serial_prefix

echo
echo "Serial prefix: $serial_prefix"

echo
echo "Please input starting serial number in series."
echo "(Number following the prefix input above)"
echo "ex. For \"M700401\" use \"401.\""
read serial_start

echo
echo "Starting number: $serial_start"

for (( i=1; i<=10; i++ ))
do
    serial_current="$serial_prefix$serial_start"
    echo $serial_current
    ((serial_start++))
    echo "Serial start (new): $serial_start"
    sleep 1
done
