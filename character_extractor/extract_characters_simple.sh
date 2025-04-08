#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed."
    exit 1
fi

# Install required packages
echo "Installing required Python packages..."
pip3 install numpy pillow

# Check if running on macOS
if [[ "$(uname)" == "Darwin" ]]; then
    echo "Detected macOS system"
    echo "Note: For full functionality, you may need to install Cairo library with Homebrew:"
    echo "  brew install cairo"
    echo "  pip3 install cairosvg"
    echo ""
    echo "If you don't have Homebrew installed, you can get it from: https://brew.sh/"
    echo ""
    echo "Don't worry if you skip this step - the script will still work using fallback methods."
    echo ""
    
    # Try to install cairosvg (optional)
    echo "Attempting to install cairosvg (may fail if Cairo is not installed)..."
    pip3 install cairosvg || echo "cairosvg installation failed. Will use fallback method."
else
    # Try to install cairosvg (optional but recommended)
    echo "Attempting to install cairosvg..."
    pip3 install cairosvg || echo "cairosvg installation failed. Will use fallback method."
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Run the Python script
echo "Running simple character extraction script..."
python3 "$SCRIPT_DIR/extract_characters_simple.py"

echo "Character extraction complete!"
echo "Check the 'extracted_characters_simple' directory for the results."

# Provide additional guidance if on macOS
if [[ "$(uname)" == "Darwin" ]]; then
    echo ""
    echo "Note: If you saw Cairo library errors, this is normal on macOS without Cairo installed."
    echo "The script used a fallback method to extract characters."
    echo "For better results in the future, consider installing Cairo with:"
    echo "  brew install cairo"
    echo "  pip3 install cairosvg"
fi 