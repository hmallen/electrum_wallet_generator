#!/bin/bash

source ../activate &&

python test_addr_overlay.py &&
gs -sOutputFile=test_address_gs.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage test_address.pdf &&
lp test_address_gs.pdf &&
while [ "`lpstat | awk '{print $2}'`" != "" ]
do
    sleep 1
done

deactivate &&

echo
echo "Done!"

exit 0
