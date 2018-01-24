#!/bin/bash

canvas="../resources/blank_canvas_gs.pdf"

echo
echo "Please input desired number of print jobs to queue:"
read print_count

for (( i=1; i<=$print_count; i++ ))
do
    echo "Queuing $i of $print_count."
    lp -o "InputSlot=MANUAL" $canvas
done

echo
echo "Begin inserting pages into manual feed slot..."
echo "If done before requested number of prints, jobs must be cancelled manually."
echo

exit 0
