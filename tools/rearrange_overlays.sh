#!/bin/bash

wallet_path=$1
config_path=$2

if [ "$wallet_path" = "" ]; then
    echo
    echo "No wallet directory provided. Exiting."
    exit 1
fi

#cd $wallet_path

if [ "`ls $wallet_path | grep overlay.pdf`" = "overlay.pdf" ] && [ "`ls $wallet_path | grep overlay_addr.pdf`" = "overlay_addr.pdf" ]; then
    echo
    echo "Wallet directory confirmed. Proceeding with rearrangement."
else
    echo
    echo "Incorrect path provided. Use path to directory containing sequence of wallet directories. Exiting."
    exit 1
fi

if [ "$config_path" = "" ]; then
    echo
    echo "No config directory provided. Exiting."
    exit 1
fi

if [ "`ls $config_path | grep bill.ini`" = "bill.ini" ] && [ "`ls $config_path | grep address.ini`" = "address.ini" ]; then
    echo
    echo "Config directory confirmed. Proceeding with rearrangement."
else
    echo
    echo "Incorrect path provided. Use path to directory containing \"bill.ini\" and \"address.ini.\" Exiting."
    exit 1
fi

exec_string="python rearrange_features.py --directory $wallet_path --config $config_path"

echo
echo "Call rearrange_features.py here!"

echo
echo "Merging PDFs into single document."
$exec_string --merge
mv $wallet_path/overlay.pdf $wallet_path/tmp/overlay_orig.pdf
mv $wallet_path/overlay_addr.pdf $wallet_path/tmp/overlay_addr_orig.pdf
echo
echo "Formatting PDFs for printing."
gs -sOutputFile=$wallet_path/overlay.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage $wallet_path/tmp/overlay_orig.pdf;
gs -sOutputFile=$wallet_path/overlay_addr.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage $wallet_path/tmp/overlay_addr_orig.pdf;

echo
echo "Done!"

exit 0
