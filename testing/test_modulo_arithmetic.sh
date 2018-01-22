#!/bin/bash

if [ "$1" != "" ]; then
    wallet_num=$1
else
    wallet_num=15
fi

echo
echo "Wallet number: $wallet_num"

if [ $(($wallet_num%3)) -gt 0 ]; then
    echo
    echo "Bill layout not full."
fi

if [ $(($wallet_num%8)) -gt 0 ]; then
    echo
    echo "Address layout not full."
fi

echo
echo "Done!"

exit 0
