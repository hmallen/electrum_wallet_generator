#!/bin/bash

sudo apt update &&
<<<<<<< HEAD
sudo apt install git python3 python3-dev libcairo2 libffi-dev libmagickwand-dev libmagickcore-extra ghostscript -y &&
sudo python3 -m pip install virtualenv &&

mkdir -p .virtualenvs &&

python3 -m virtualenv .virtualenvs/electrum_wallet_generator &&
#python3 -m virtualenv .virtualenvs/ewg_test &&
source .virtualenvs/electrum_wallet_generator/bin/activate &&
#source .virtualenvs/ewg_test/bin/activate &&

pip install git+https://github.com/spesmilo/electrum.git &&
pip install git+https://github.com/hmallen/DrawSVG.git &&
pip install -r requirements.txt &&

#sed -i "s/, check_www//g" ~/.virtualenvs/electrum_wallet_generator/

echo "Installation complete. Type 'source .virtualenvs/electrum_wallet_generator/bin/activate' to activate virtualenv."
=======
sudo apt install python36 -y &&
sudo python3 -m pip install virtualenv &&
mkdir ~/.virtualenvs &&
python3 -m virtualenv ~/.virtualenvs/electrum_wallet_generator &&
source ~/.virtualenvs/electrum_wallet_generator/bin/activate &&
pip install git+https://github.com/spesmilo/electrum.git &&
pip install git+https://github.com/hmallen/DrawSVG.git &&
pip install -r requirements.txt &&
#sed -i "s/check_www/\#check_www/g" ~/.virtualenvs/electrum_wallet_generator/
>>>>>>> ce66224d374c900b163c7753f2ddbd74903fd193
