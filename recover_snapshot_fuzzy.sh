#!/bin/bash

SNAPSHOT_DIR="scaffold_snapshots"
RECOVER_DIR="recovered_files"

# Check if fzf is installed
if ! command -v fzf >/dev/null; then
    echo "Error: 'fzf' is required. Please install it first."
    exit 1
fi

# List snapshots
echo "Available Snapshots:"
snapshots=($(ls -d "$SNAPSHOT_DIR"/scaffold_* 2>/dev/null))
if [ ${#snapshots[@]} -eq 0 ]; then
    echo "No snapshots found."
    exit 1
fi

for i in "${!snapshots[@]}"; do
    snap_path="${snapshots[$i]}"
    snap_name=$(basename "$snap_path")
    echo "[$i] $snap_name"
done

read -p "Enter the number of the snapshot to recover from: " snap_index
selected_snapshot="${snapshots[$snap_index]}"
if [ -z "$selected_snapshot" ] || [ ! -d "$selected_snapshot" ]; then
    echo "Invalid snapshot selection."
    exit 1
fi

# Use fzf to select files or folders
echo "Loading file list for snapshot: $(basename "$selected_snapshot")"
file_list=$(cd "$selected_snapshot" && find . -type f -o -type d | sed 's|^\./||' | fzf --multi --preview "tree -C $selected_snapshot/{} || cat $selected_snapshot/{}")

# If nothing was selected
if [ -z "$file_list" ]; then
    echo "No files or folders selected."
    exit 1
fi

# Ask for destination directory
default_dest="$RECOVER_DIR/$(basename "$selected_snapshot")"
read -p "Enter destination directory (default: $default_dest): " dest_dir
dest_dir="${dest_dir:-$default_dest}"
mkdir -p "$dest_dir"

# Copy selected files/directories
echo "$file_list" | while IFS= read -r path; do
    src="$selected_snapshot/$path"
    dest="$dest_dir/$path"
    if [ -f "$src" ]; then
        mkdir -p "$(dirname "$dest")"
        cp "$src" "$dest"
        echo "Recovered file: $path"
    elif [ -d "$src" ]; then
        mkdir -p "$dest"
        cp -r "$src/" "$dest/"
        echo "Recovered folder: $path"
    else
        echo "Not found or unsupported type: $path"
    fi
done

echo "✅ Recovery complete. Files and folders copied to: $dest_dir"

