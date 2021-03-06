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
                if [ $wallet_num -gt 3 ]; then
                    echo
                    echo "Printer delay between pages (seconds):"
                    read printer_delay
                fi
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
    $exec_string --directory wallets/$DT --merge
    mv wallets/$DT/overlay.pdf wallets/$DT/tmp/overlay_orig.pdf
    echo
    echo "Formatting PDFs for printing."
    gs -sOutputFile=wallets/$DT/overlay.pdf -sDEVICE=pdfwrite -sPAPERSIZE=letter -dCompatibilityLevel=1.6 -dNOPAUSE -dBATCH -dPDFFitPage wallets/$DT/tmp/overlay_orig.pdf
fi

if [ $print_overlays = true ]; then
    if [ $create_pdfs = true ]; then
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
                #lp -P $i -H hold overlay.pdf
                lp -P $i wallets/$DT/overlay.pdf
                if [ $i -ne $page_count ]; then
                    echo "Delaying $printer_delay seconds before next print."
                    sleep $printer_delay
                fi
            done
        else
            echo
            echo "Printing overlay page."
            lp wallets/$DT/overlay.pdf
        fi
    else
        echo
        echo "PNG printing not yet implemented. Skipping."
    fi
fi

echo
echo "Done!"

exit 0
