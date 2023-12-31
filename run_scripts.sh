#!/usr/bin/bash

this_script="$(basename "$0")" # Name of this script when executaded
options= # Options passed to this script
exe_path= # Executable to run
args= # Arguments to the executable
tests_dir= # If args is a directory
out_dir= # Directory for the output directories

assign_vars(){
    if [[ $# -le 0 ]]; then
        print_help
        return 1
    fi

    if [[ "${1:0:1}" = "-" ]]; then
        if [[ ${#options} -eq 2 ]]; then
            options=$1
            shift 1
        else
            printf "%s: is not a recognised option\n" "$1" >&2
            printf "%s -h: to see usage\n" "$this_script" >&2
            return 1
        fi
    fi

    exe_path=$1
    if [[ $exe_path && ! -x "$exe_path" ]]; then
        printf "Cannot execute: %s\n" "$exe_path"
        return 1
    fi

    if [[ $2 ]]; then
        args=$2
    fi

    if [[ $3 ]]; then
        out_dir=$(strip_tslash "$3")
    fi
}

#Strip trailing slashes
strip_tslash(){
    if [[ "$1" = *"/" ]]; then
        echo "${1%/}"
    else
        echo "$1"
    fi
}

# Print help
print_help(){
    printf "%s - runs a script or an executable\n" "$this_script"
    printf "\nUSAGE:\n\t%s <executable> [arguments] [output_directory]\n" "$this_script"
    printf "\t%s <-hd>\n" "$this_script"
    printf "\nDESCRIPTION:\n\t-h\n\t  print this help and exit\n"
    printf "\t-d\n\t  treat [arguments] as a directory of test files\n"
    printf "\texecutable\n\t\tpath to executable\n"
    printf "\targuments\n\t\toptional arguments to the executable\n"
    printf "\toutput_directory\n\t\toptional directory to redirect output to\n"
}

# Confirm directories exist
check_dir(){
    if [[ $# -ge 1 ]]; then
        for dir in "$@"; do
            if [[ ! -d "$dir" ]]; then
                printf "Invalid directory: %s\n" "$dir" >&2
                return 1
            fi
        done
    else
        echo "Not enough arguments" >&2
        return 1
    fi

    return 0
}

if ! assign_vars "$@"; then
    exit 1
fi

if [[ $options ]]; then
    if [[ "$options" = "-d" ]]; then
        tests_dir=$(strip_tslash "$args")
        unset "args"
        if ! check_dir "$tests_dir"; then
            exit 1
        fi
    elif [[ "$options" = "-h" ]]; then
        print_help
        exit 0
    else
        printf "%s is not a recognised option\n" "$options" >&2
        printf "%s -h: to see usage\n" "$this_script" >&2
        exit 1
    fi
fi

if [[ $out_dir ]]; then
    if ! check_dir "$out_dir"; then
        exit 1
    elif [[ ! -w "$out_dir" ]]; then
        printf "%s: is not write-able\n" "$out_dir"
        exit 1
    fi
fi

if [[ $tests_dir ]]; then
    # Iterate through all files in tests_dir
    for file in "$tests_dir/"*; do
        if [[ $out_dir ]]; then
            out_file="$out_dir/out_$(basename "$file" ".*").txt"
            $exe_path "$file" > "$out_file"
        else
            $exe_path "$file"
        fi
    done
else
    if [[ $out_dir ]]; then
            out_file="$out_dir/out_$(basename "$exe_path" ".*").txt"
            $exe_path "$args" > "$out_file"
        else
            $exe_path "$args"
        fi
fi
