#!/bin/bash

echo
echo "-----------------------------"
echo "| Electrum Wallet Generator |"
echo "|                           |"
echo "| by hmallen@github.com     |"
echo "-----------------------------"
echo

echo "Enter number of wallets to create:"
read wallet_num
echo

exec_string="python create_features.py"

echo "Create overlays?"
PS3="Selection: "
options=("PNG" "PDF" "None" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "PNG")
            create_overlays=true
            create_pdfs=false
            exec_string="$exec_string --overlay"
            break
            ;;
        "PDF")
            create_overlays=true
            create_pdfs=true
            exec_string="$exec_string --overlay --pdf"
            break
            ;;
        "None")
            create_overlays=false
            break
            ;;
        "Quit")
            echo
            echo "Exiting program."
            exit
            ;;
        *) echo invalid option;;
    esac
done

if [ $create_overlays = true ]; then
    echo
    echo "Send overlays to printer?"
    PS3="Selection: "
    options=("Yes" "No" "Quit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                #echo "Printing overlays."
                print_overlays=true
                break
                ;;
            "No")
                #echo "Not printing overlays."
                print_overlays=false
                break
                ;;
            "Quit")
                echo
                echo "Exiting program."
                exit
                ;;
            *) echo invalid option;;
        esac
    done
fi

echo

if [ $wallet_num -eq 1 ]; then
    echo "Creating 1 wallet."
else
    echo "Creating $wallet_num wallets."
fi

DT=$(date "+%m%d%Y_%H%M%S")

for (( i=1; i<=$wallet_num; i++ ))
do
    exec="$exec_string --directory wallets/$DT/$i --number $i"
    mkdir -p wallets/$DT/$i
    echo
    ./electrum_modified create -w wallets/$DT/$i/$i
    echo
    echo "Creating info file and QR code."
    $exec
done

if [ $create_pdfs = true ]; then
    echo
    echo "Merging PDFs into single document."
    python combine_pdfs.py -d wallets/$DT
fi

if [ $print_overlays = true ]; then
    echo
    echo "OVERLAY PRINTING TO BE IMPLEMENTED HERE..."
    # EXAMPLE: lp wallets/$DT/overlay_1.png
fi

echo "Done!"

exit 0
