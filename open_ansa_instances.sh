#!/bin/bash

# Define the directory containing ANSA files
ANSA_FILES_DIR="/Shashank/Python/ansa_test/"

# Define the script that should be loaded inside ANSA
ANSA_SCRIPT="/Shashank/Python/run_script_in_ansa.py"
ANSA_FUNCTION="main"  # Function to execute inside the script

# Loop through all `.ansa` files in the directory
for file in "$ANSA_FILES_DIR"/*.ansa; do
    # Check if the file exists
    [ -e "$file" ] || continue

    # Open ANSA instance and execute the script inside it
    echo "Opening ANSA for: $file and executing script..."
    
    ansa2501 -i "$file" -execscript "$ANSA_SCRIPT|$ANSA_FUNCTION" &

    # Add a short delay to prevent system overload
    sleep 2
done

echo "All ANSA files are opened and scripts are executed."
