#!/bin/bash

source ../activate &&

python test_addr_overlay.py &&
gs -sOutputFile=test_address_gs.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage test_address.pdf &&

deactivate &&

echo
echo "Done!"

exit 0
