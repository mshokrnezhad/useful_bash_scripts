#!/bin/bash

# Check if input file exists
if [ ! -f "html_with_image_links.txt" ]; then
    echo "Error: html_with_image_links.txt not found!"
    exit 1
fi

# Create a directory for downloaded images if it doesn't exist
download_dir="downloaded_images"
mkdir -p "$download_dir"

# Extract links and download images
echo "Extracting links and downloading images..."
grep -o 'href="https://[^"]*\.png[^"]*"' html_with_image_links.txt | 
    sed 's/href="\([^"]*\.png\)[^"]*"/\1/' |
    while read -r url; do
        # Extract filename from URL
        filename=$(basename "$url")
        echo "Downloading $filename..."
        curl -s "$url" -o "$download_dir/$filename"
    done

echo "Download complete! Files are saved in $download_dir/" 