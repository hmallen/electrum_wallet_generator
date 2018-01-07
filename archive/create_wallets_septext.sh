#!/bin/bash

echo "Bash version ${BASH_VERSION}"

NUM=$1

echo "Creating $NUM wallet(s)."

DT=$(date "+%m%d%Y_%H%M%S")

./electrum_modified daemon start &&

for (( i=1; i<=$NUM; i++ ))
do
	mkdir -p wallets/$DT/$i
	./electrum_modified create -w wallets/$DT/$i/$i > wallets/$DT/$i/$i_seed.txt
	echo -e "\r" >> wallets/$DT/$i/$i.txt
	./electrum_modified daemon load_wallet -w wallets/$DT/$i/$i
	./electrum_modified getunusedaddress -w wallets/$DT/$i/$i >> wallets/$DT/$i/$i_addr.txt
	./electrum_modified daemon close_wallet -w wallets/$DT/$i/$i
	cat wallets/$DT/$i/$i.txt
	echo "Creating QR code."
	python create_qr_septext.py -d "wallets/$DT/$i/"
done

./electrum_modified daemon stop &&

echo "Done!"

exit 0
