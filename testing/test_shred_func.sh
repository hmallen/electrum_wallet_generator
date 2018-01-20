#!/bin/bash

secure_mode=true
DT=test_wallets
wallet_num=3

if [ $secure_mode = true ]; then
    echo
    echo "Shredding wallet files."
    for (( i=1; i<=$wallet_num; i++ ))
    do
        shred -u -z -v wallets/$DT/$i/* &&
        rm -r wallets/$DT/$i
    done
    shred -u -z -v wallets/$DT/tmp/*
    rm -r wallets/$DT/tmp
    shred -u -z -v wallets/$DT/* &&
    rm -r wallets/$DT
    echo
    echo "Restoring networking services."
    #sudo /etc/init.d/networking start &&
fi
