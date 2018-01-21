#!/bin/bash

sudo apt update &&
sudo apt install git python3 python3-virtualenv libcairo2 libffi-dev libmagickwand-dev libmagickcore-extra ghostscript -y &&

pip install git+https://github.com/spesmilo/electrum.git &&
pip install git+https://github.com/hmallen/DrawSVG.git &&
pip install -r requirements.txt
