#!/bin/bash

# Master script to run update_snapshot only if files have changed

# Define log file for tracking
LOG_FILE="update_snapshot_run.log"

echo "=== Snapshot run at $(date) ===" >> "$LOG_FILE"

# Call snapshot script
./update_snapshot.sh >> "$LOG_FILE" 2>&1


