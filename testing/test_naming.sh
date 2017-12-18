#!/bin/bash

echo "Bash version ${BASH_VERSION}"

NUM=$1

echo "Creating $NUM wallets."

./electrum_modified daemon start &&

for (( i=1; i<=$NUM; i++ ))
do
	echo "$i"
done

./electrum_modified daemon stop &&

exit 0
