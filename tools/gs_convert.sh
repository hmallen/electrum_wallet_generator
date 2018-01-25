#!/bin/bash

path=$1

if [ "$path" = "" ]; then
    echo
    echo "No file path provided. Exiting."
    exit 1
fi

IFS_ORIG=$IFS
IFS=.
read -ra file_name <<< "$path"
IFS=$IFS_ORIG

prefix=${file_name[0]}
suffix=${file_name[1]}

path_gs="${prefix}_gs.${suffix}"

gs -sOutputFile=$path_gs -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage $path &&

echo
echo "Done!"
