#!/bin/bash

echo
echo "Electrum Wallet Generator by Hunter M. Allen"
echo

echo "Enter number of wallets to create:"
read wallet_num
echo

exec_string="python ../create_features.py"

echo "Create PNG overlays?"
PS3="Selection: "
options=("Yes" "No" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Yes")
            echo "Creating overlays."
            create_overlays=true
            exec_string="$exec_string --overlay"
            break
            ;;
        "No")
            echo "Not creating overlays"
            create_overlays=false
            break
            ;;
        "Quit")
            echo "Exiting program."
            exit
            ;;
        *) echo invalid option;;
    esac
done

echo

if [ $create_overlays = true ]; then
    echo "Send overlays to printer?"
    PS3="Selection: "
    options=("Yes" "No" "Quit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                echo "Printing overlays."
                print_overlays=true
                break
                ;;
            "No")
                echo "Not printing overlays"
                print_overlays=false
                break
                ;;
            "Quit")
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
    exec="$exec_string --directory wallet/$DT/$i --number $i"
    mkdir -p wallets/$DT/$i
    ./electrum_modified_osx create -w wallets/$DT/$i/$i
    echo "Creating info file and QR code."
    $exec
done

if [ $print_overlays = true ]; then

echo "Done!"

exit 0
