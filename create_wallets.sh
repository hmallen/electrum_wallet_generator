#!/bin/bash

echo "Bash version ${BASH_VERSION}"

NUM=$1

echo "Creating $NUM wallet(s)."

DT=$(date "+%m%d%Y_%H%M%S")

for (( i=1; i<=$NUM; i++ ))
do
	mkdir -p wallets/$DT/$i
	./electrum_modified create -w wallets/$DT/$i/$i
	echo "Creating info file and QR code."
	python create_qr.py -d "wallets/$DT/$i/" -n "$i"
done

echo "Done!"

exit 0
