#!/bin/bash

sudo apt update &&
sudo apt install python36 -y &&
sudo python3 -m pip install virtualenv &&
mkdir ~/.virtualenvs &&
python3 -m virtualenv ~/.virtualenvs/electrum_wallet_generator &&
source ~/.virtualenvs/electrum_wallet_generator/bin/activate &&
pip install git+https://github.com/spesmilo/electrum.git &&
pip install git+https://github.com/hmallen/DrawSVG.git &&
pip install -r requirements.txt &&
#sed -i "s/check_www/\#check_www/g" ~/.virtualenvs/electrum_wallet_generator/
