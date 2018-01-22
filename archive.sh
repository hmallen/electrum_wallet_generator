#!/bin/bash

path=$1

IFS_ORIG=$IFS
IFS=.
read -ra file_name <<< "$path"
IFS=$IFS_ORIG

prefix=${file_name[0]}
suffix=${file_name[1]}

DT=$(date "+%m%d%Y-%H%M")

archive_path="archive/${prefix}_$DT.$suffix"

echo
echo "Archiving: $archive_path"

mv $path $archive_path

echo
echo "Done!"

exit 0
