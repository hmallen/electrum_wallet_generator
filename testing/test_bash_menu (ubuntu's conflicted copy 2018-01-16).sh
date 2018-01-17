#!/bin/bash
# Bash Menu Script Example

echo
echo "Electrum Wallet Generator by Hunter M. Allen"
echo

echo "Enter number of wallets to create:"
read wallet_num
echo
echo "Creating $wallet_num wallet(s)."
echo

exec_string="python create_features.py "

echo "Create PNG overlays?"
PS3="Selection: "
options=("Yes" "No" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Yes")
            echo "Creating overlays."
            create_overlays=true
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

if [ $create_overlays = true ]
then
    echo "Send overlays to printer?"
    PS3="Selection: "
    options=("Yes" "No" "Quit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                echo "Printing overlays."
                print_overlays=1
                break
                ;;
            "No")
                echo "Not printing overlays"
                print_overlays=0
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
