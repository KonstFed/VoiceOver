#!/bin/bash

# Define the source and destination folders
for source_folder in $(ls "$1")
do

    folder_name=$(basename $source_folder)
    destination_folder="${source_folder}/${folder_name}"

    # Create the destination folder if it does not exist
    if [ ! -d "$destination_folder" ]; then
    mkdir -p "$destination_folder"
    fi

    # # Copy files from source folder to destination folder
    mv "$1"/"$source_folder"/*.wav "$destination_folder"
done