#!/bin/bash

PROGRAM_NAME="$1"

if [ -x "$PROGRAM_NAME" ]; then

    output=$("./flame_cp" "${@:2}" 2>&1)
    exit_code=$?

    if [ "$exit_code" -eq 0 ]; then
        echo "C program executed successfully :)"
	echo "output: $output"
    else
        case "$exit_code" in
            1)
                echo "Command line usage error :(" >&2
                ;;
            2)
                echo "Input or outfut file NULL :(" >&2
                ;;
	    3)
		echo "Error opening input file or setting permissions :(" >&2
		;;
	    4)
		echo "Error opening input file :(" >&2
		;;
	    5) 
		echo "Error getting file information :(" >&2
		;;
	    6)
		echo "Error allocating memory for input buffer :(" >&2
		;;
	    7)	
		echo "Error reading input file :(" >&2
		;;
	    8)
		echo "Error opening output file or setting permissions :(" >&2
		;;
	    9)
		echo "Error opening output file :(" >&2
		;;
	    10)
		echo "Error writing to output file :(" >&2
		;;
        esac
    fi
else 
    echo "Error: Compiled program not found"
fi
