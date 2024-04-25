#!/usr/bin/bash

this_script="$(basename "$0")" # Name of this script when executaded
options= # Options passed to this script
args=("$@") # Arguments to the executable
tests_dir= # If args is a directory
out_dir= # Directory for the output directories

read_options(){
    for opt in "$@"; do
        if grep -E '\W-d(?:$|\W)' - <<< "$opt" &> /dev/null; then
            tests_dir=$(strip_tslash "$args")
            unset "args"
            if ! check_dir "$tests_dir"; then
                exit 1
            fi
        elif grep -E '\W-[d]*h[d]*(?:$|\W)|--help' - <<< "$opt" &> /dev/null; then
            print_help
            exit 0
        else
            printf "%s: is not a recognised option\n" "$opt" >&2
            printf "Run with -h option to see usage\n"
            exit 1
        fi
    done
}

main(){
    for idx in ${#args}; do
        if grep -E '\W-{1,2}\w' - <<< "$((idx))" &> /dev/null; then
            options="$options"" $((idx))"
            read_options "$$((idx))"
        else
            echo "$$((idx))"
        fi
    done
}

main "$@"
