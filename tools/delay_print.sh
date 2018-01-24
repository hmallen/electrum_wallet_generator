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

echo "File has $pages pages."

if [ $pages -eq 1 ]; then
    echo
    echo "File only has 1 page. No delay required. Exiting."
    exit 0
fi

echo
echo "Please input printer delay between pages (seconds):"
read print_delay

for (( i=1; i<=$pages; i++ ))
do
    echo
    echo "Printing page $i."
    lp -P $i $path
    
    echo "Waiting for print job to complete."
    while [ "`lpstat | awk '{print $2}'`" != "" ]
    do
        sleep 1
    done
    
    if [ $i -ne $pages ]; then
        echo "Delaying $print_delay seconds before next print."
        sleep $print_delay
    fi
done

echo
echo "Done!"

exit 0
