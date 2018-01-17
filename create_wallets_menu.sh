#!/bin/bash

echo
<<<<<<< HEAD
echo "-----------------------------"
echo "| Electrum Wallet Generator |"
echo "|                           |"
echo "| by hmallen@github.com     |"
echo "-----------------------------"
echo
=======
echo "Electrum Wallet Generator by Hunter M. Allen"
echo

>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0
echo "Enter number of wallets to create:"
read wallet_num
echo

exec_string="python create_features.py"

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
<<<<<<< HEAD
            echo "Not creating overlays."
=======
            echo "Not creating overlays"
>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0
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
<<<<<<< HEAD
                echo "Not printing overlays."
=======
                echo "Not printing overlays"
>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0
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
<<<<<<< HEAD
echo
=======
>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0

DT=$(date "+%m%d%Y_%H%M%S")

for (( i=1; i<=$wallet_num; i++ ))
do
    exec="$exec_string --directory wallets/$DT/$i --number $i"
    mkdir -p wallets/$DT/$i
    ./electrum_modified create -w wallets/$DT/$i/$i
<<<<<<< HEAD
    echo    
=======
>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0
    echo "Creating info file and QR code."
    $exec
done

if [ $print_overlays = true ]; then
<<<<<<< HEAD
    echo
=======
>>>>>>> 56d187d56a0f4d2c8b0359da1d4d68aca49cf2f0
    echo "OVERLAY PRINTING TO BE IMPLEMENTED HERE..."
    sleep 3
fi

echo "Done!"

exit 0
