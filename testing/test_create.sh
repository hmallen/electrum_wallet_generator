#!/bin/bash

echo "Bash version ${BASH_VERSION}"

NUM=$1

echo "Creating $NUM wallet(s)."

./electrum_modified daemon start &&

for (( i=1; i<=$NUM; i++ ))
do
	mkdir wallets/$i
	./electrum_modified create -w wallets/$i/$i > wallets/$i/$i.txt
	echo -e "\r" >> wallets/$i/$i.txt
	./electrum_modified daemon load_wallet -w wallets/$i/$i
	./electrum_modified getunusedaddress -w wallets/$i/$i >> wallets/$i/$i.txt
	./electrum_modified daemon close_wallet -w wallets/$i/$i
	cat wallets/$i/$i.txt
done

./electrum_modified daemon stop &&

exit 0
