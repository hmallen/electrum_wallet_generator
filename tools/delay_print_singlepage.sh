#!/bin/bash

path=$1

if [ "$path" = "" ]; then
    echo
    echo "No file path provided. Exiting."
    exit 1
fi

echo
echo "File for printing: $path"

pages=$(strings < $path | sed -n 's|.*/Count -\{0,1\}\([0-9]\{1,\}\).*|\1|p' | sort -rn | head -n 1)

if [ $pages -gt 1 ]; then
    echo
    echo "File has multiple pages, but program only handles single-page documents. Exiting."
    exit 0
fi

echo
echo "Please input number of copies to print:"
read print_count

echo
echo "Please input printer delay between prints (seconds):"
read print_delay

for (( i=1; i<=$print_count; i++ ))
do
    echo
    echo "Printing copy $i."
    lp $path
    
    echo "Waiting for print job to complete."
    while [ "`lpstat | awk '{print $2}'`" != "" ]
    do
        sleep 1
    done
    
    if [ $i -ne $print_count ]; then
        echo "Delaying $print_delay seconds before next print."
        sleep $print_delay
    fi
done

echo
echo "Done!"

exit 0
