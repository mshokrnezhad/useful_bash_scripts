# Pixel Character Extractor

This tool extracts individual pixel art characters from an SVG file containing multiple characters and saves each character as a separate SVG file.

## How It Works

The script uses a clustering algorithm to identify individual characters in the SVG file based on the proximity of pixels. It then extracts each character and saves it as a separate SVG file.

The process works as follows:

1. Parse the SVG file to extract all pixel rectangles
2. Group pixels that are close to each other to identify individual characters
3. For each character, create a new SVG file containing only the pixels for that character

## Requirements

- Python 3
- Required Python packages (installed automatically by the script):
  - numpy
  - pillow (PIL)
  - cairosvg (optional, for better SVG handling)

## Usage

### If You're Getting Black Pictures

If the original script produces black pictures, try the simpler alternative script:

```bash
./extract_characters_simple.sh
```

This alternative script:

1. Converts the SVG to a bitmap image
2. Uses image processing techniques to identify and extract individual characters
3. Saves each character as a PNG file in the `extracted_characters_simple` directory

### Using the Original Script

Run the shell script:

```bash
./extract_characters.sh
```

This will:

1. Install the required dependencies
2. Run the Python script to extract the characters
3. Save the extracted characters in the `extracted_characters` directory

### Using the Python Scripts Directly

If you prefer to run the Python scripts directly:

```bash
# Original script
python3 extract_characters.py

# Alternative script (if you get black pictures)
python3 extract_characters_simple.py
```

Make sure you have the required dependencies installed:

```bash
pip3 install numpy pillow cairosvg
```

## Output

The extracted characters will be saved in the output directory with filenames like:

- `character_0.svg` and `character_0.png` (original script)
- `character_1.png` (simple script)

## Customization

If you need to adjust the extraction parameters, you can modify the following variables in the Python script:

- `grid_size`: Controls the size of the grid cells used for clustering (default: 20)
- `padding`: Controls the amount of padding added around each character (default: 1)

## Troubleshooting

### Cairo Library Errors on macOS

If you see errors like:

```
OSError: no library called "cairo-2" was found
no library called "cairo" was found
```

This is because macOS doesn't come with the Cairo library pre-installed. The script will automatically fall back to an alternative method, but for better results, you can install Cairo:

1. Install Homebrew if you don't have it already:

   ```
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. Install Cairo using Homebrew:

   ```
   brew install cairo
   ```

3. Reinstall cairosvg:
   ```
   pip3 install cairosvg
   ```

After installing Cairo, the script should work without errors and may produce better results.

### Black Pictures

If you're getting black pictures, try the following:

1. Use the alternative script (`extract_characters_simple.sh`)
2. Adjust the threshold value in the script (look for `binary = gray_img.point(lambda p: p < 200)` and change 200 to a different value)
3. Make sure the SVG file contains colored rectangles and not just a single embedded image

### Other Issues

If the script fails to extract characters correctly, try the following:

1. Make sure the SVG file is properly formatted
2. Adjust the `grid_size` parameter to match the size of your characters
3. If using the bitmap approach, adjust the `threshold` parameter

If you encounter any issues with the cairosvg library, the script will fall back to using PIL directly, which may not work as well with SVG files.
