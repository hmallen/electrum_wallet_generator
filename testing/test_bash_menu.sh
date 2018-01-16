#!/bin/bash
# Bash Menu Script Example

echo
echo "Electrum Wallet Generator by Hunter M. Allen"
echo

echo "How many wallets would you like to create?"
read wallet_num
echo
echo "Creating $wallet_num wallet(s)."
echo

PS3='Create PNG overlays? Choice: '
options=("Yes" "No" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "Yes")
            echo "Creating overlays."
            create_overlays=1
            break
            ;;
        "No")
            echo "Not creating overlays"
            create_overlays=0
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

if [ $create_overlays -eq 1 ]
then
    PS3='Print overlays? Choice: '
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
