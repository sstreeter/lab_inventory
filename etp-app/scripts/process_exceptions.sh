#!/bin/bash

INPUT="exceptions.csv"
OUTPUT="exceptions_cleaned_final.csv"

# Output header
echo "Lab,ComputerName,Owner" > "$OUTPUT"

# Skip header and read each line
tail -n +2 "$INPUT" | while IFS=',' read -r lab sn bc cname _ _ _ location mac user owner _ hostname _; do
    # Convert all to uppercase safely
    lab_uc=$(echo "$lab" | tr '[:lower:]' '[:upper:]')
    sn_uc=$(echo "$sn" | tr '[:lower:]' '[:upper:]')
    bc_uc=$(echo "$bc" | tr '[:lower:]' '[:upper:]')
    cname_uc=$(echo "$cname" | tr '[:lower:]' '[:upper:]')
    host_uc=$(echo "$hostname" | tr '[:lower:]' '[:upper:]')
    user_uc=$(echo "$user" | tr '[:lower:]' '[:upper:]')
    owner_uc=$(echo "$owner" | tr '[:lower:]' '[:upper:]')
    loc_uc=$(echo "$location" | tr '[:lower:]' '[:upper:]')

    # Determine ComputerName value and its source
    if [[ -n "$cname_uc" ]]; then
        comp="CN:$cname_uc"
    elif [[ -n "$host_uc" ]]; then
        comp="HN:$host_uc"
    elif [[ -n "$sn_uc" ]]; then
        comp="SN:$sn_uc"
    elif [[ -n "$bc_uc" ]]; then
        comp="BC:$bc_uc"
    else
        comp="UNKNOWN"
    fi

    # Determine Owner value and its source
    if [[ -n "$owner_uc" ]]; then
        final_owner="OWN:$owner_uc"
    elif [[ -n "$user_uc" ]]; then
        final_owner="USR:$user_uc"
    elif [[ -n "$lab_uc" ]]; then
        final_owner="LAB:$lab_uc"
    elif [[ -n "$loc_uc" ]]; then
        final_owner="LOC:$loc_uc"
    else
        final_owner="UNKNOWN"
    fi

    # Output clean line
    echo "$lab_uc,$comp,$final_owner" >> "$OUTPUT"
done

