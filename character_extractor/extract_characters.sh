#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install numpy pillow

# Try to install cairosvg (optional but recommended)
pip3 install cairosvg || echo "cairosvg installation failed. Will use fallback method."

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Python script
echo "Running character extraction script..."
python3 "$SCRIPT_DIR/extract_characters.py"

echo "Character extraction complete!"
echo "Check the 'extracted_characters' directory for the results." 