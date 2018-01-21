#!/bin/bash

print_user=`lpstat | awk '{print $2}'`
echo $print_user

while [ "`lpstat | awk '{print $2}'`" != "" ]
do
    echo `lpstat | awk '{print $2}'`
    sleep 1
done
