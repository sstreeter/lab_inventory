#!/bin/bash

# Persistent snapshot with change detection and hard link deduplication
SNAPSHOT_DIR="scaffold_snapshots"
SOURCE_DIR="lab_inventory"
mkdir -p "$SNAPSHOT_DIR"

# Use timestamp for new snapshot
NOW=$(date +"%Y%m%d_%H%M%S")
NEW_SNAPSHOT="$SNAPSHOT_DIR/scaffold_$NOW"

# Use latest snapshot as reference (if it exists)
LATEST_LINK="$SNAPSHOT_DIR/latest"

if [ -d "$LATEST_LINK" ]; then
    # Use rsync with --link-dest to avoid copying unchanged files
    rsync -a --delete \
          --exclude='__pycache__' \
          --exclude='*.log' \
          --exclude='*.pyc' \
          --exclude='*.DS_Store' \
          --exclude='frontend/node_modules' \
          --link-dest="$(realpath $LATEST_LINK)" \
          "$SOURCE_DIR/" "$NEW_SNAPSHOT"
else
    # First snapshot (no reference yet)
    rsync -a --delete \
          --exclude='__pycache__' \
          --exclude='*.log' \
          --exclude='*.pyc' \
          --exclude='*.DS_Store' \
          --exclude='frontend/node_modules' \
          "$SOURCE_DIR/" "$NEW_SNAPSHOT"
fi

# Only keep the new snapshot if there are actual changes
if [ "$(find "$NEW_SNAPSHOT" -type f | wc -l)" -eq 0 ]; then
    echo "No changes detected. Snapshot not saved."
    rm -rf "$NEW_SNAPSHOT"
else
    # Update 'latest' symlink to point to the new snapshot
    rm -f "$LATEST_LINK"
    ln -s "$NEW_SNAPSHOT" "$LATEST_LINK"
    echo "Scaffold snapshot saved: $NEW_SNAPSHOT"
    echo "Symlink 'latest' now points to: $NEW_SNAPSHOT"
fi

