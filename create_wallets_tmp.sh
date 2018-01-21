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
options=("PDF" "PNG" "None" "Quit")
select opt in "${options[@]}"
do
    case $opt in
        "PDF")
            create_overlays=true
            create_pdfs=true
            exec_string="$exec_string --overlay --pdf"
            break
            ;;
        "PNG")
            create_overlays=true
            create_pdfs=false
            exec_string="$exec_string --overlay"
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

if [ "$create_overlays" = true ]; then
    echo
    echo "Send overlays to printer?"
    PS3="Selection: "
    options=("Yes" "No" "Quit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                print_overlays=true
                if [ $wallet_num -gt 3 ]; then
                    echo
                    echo "Printer delay between pages (seconds):"
                    read printer_delay
                fi
                break
                ;;
            "No")
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

if [ "$print_overlays" = true ]; then
    echo
    echo "Enable secure mode?"
    echo "--Networking will be disabled while program is running and wallet files will be shredded/overwritten after printing.--"
    PS3="Selection: "
    options=("Yes" "No" "Quit")
    select opt in "${options[@]}"
    do
        case $opt in
            "Yes")
                secure_mode=true
                break
                ;;
            "No")
                secure_mode=false
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

DT=$(date "+%m%d%Y_%H%M%S")

if [ "$secure_mode" = true ]; then
    echo
    echo "Secure mode enabled."
    echo "Disabling networking services."
    sudo /etc/init.d/networking stop &&
    sudo /etc/init.d/network-manager stop &&
    sleep 5
    DT="${DT}_secure"
fi

echo
if [ $wallet_num -eq 1 ]; then
    echo "Creating 1 wallet."
else
    echo "Creating $wallet_num wallets."
fi

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

if [ "$create_pdfs" = true ]; then
    echo
    echo "Merging PDFs into single document."
    $exec_string --directory wallets/$DT --merge
    mv wallets/$DT/overlay.pdf wallets/$DT/tmp/overlay_orig.pdf
    echo
    echo "Formatting PDFs for printing."
    gs -sOutputFile=wallets/$DT/overlay.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage wallets/$DT/tmp/overlay_orig.pdf
fi

if [ "$print_overlays" = true ]; then
    if [ "$create_pdfs" = true ]; then
        echo
        echo "Sending overlays to printer."
        if [ $wallet_num -gt 3 ]; then
            let page_count=$wallet_num/3
            let page_count_mod=$wallet_num%3
            if [ $page_count_mod -gt 0 ]; then
                let page_count++
            fi
            for (( i=1; i<=$page_count; i++ ))
            do
                echo
                echo "Printing overlay page $i."
                #lp -P $i wallets/$DT/overlay.pdf
                if [ $i -ne $page_count ]; then
                    echo "Delaying $printer_delay seconds before next print."
                    sleep $printer_delay
                fi
            done
        else
            echo
            echo "Printing overlay page."
            #lp wallets/$DT/overlay.pdf
        fi
    else
        echo
        echo "PNG printing not yet implemented. Skipping."
    fi
fi

if [ "$secure_mode" = true ]; then
    echo
    echo "Shredding wallet files."
    #for (( i=1; i<=$wallet_num; i++ ))
    #do
        #shred -u -z -v wallets/$DT/$i/* &&
        #rm -r wallets/$DT/$i
    #done
    #shred -u -z -v wallets/$DT/tmp/*
    #rm -r wallets/$DT/tmp
    #shred -u -z -v wallets/$DT/* &&
    #rm -r wallets/$DT
    echo
    echo "Restoring networking services."
    sudo /etc/init.d/networking start &&
    sudo /etc/init.d/network-manager start &&
    sleep 5
fi

echo
echo "Done!"

exit 0
