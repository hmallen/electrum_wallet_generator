#!/bin/bash

./electrum_modified create -w wallet_1 &&
./electrum_modified daemon start &&
./electrum_modified daemon load_wallet -w wallet_1 &&
./electrum_modified listaddresses -w wallet_1 &&
./electrum_modified daemon close_wallet -w wallet_1 &&
./electrum_modified daemon stop &&
echo "Done!"
