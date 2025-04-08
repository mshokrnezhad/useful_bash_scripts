# PNG Link Extractor and Downloader

A shell script that extracts PNG image links from HTML files and automatically downloads them. This tool is perfect for batch downloading image assets from web pages.

## Prerequisites

Before running the script, you need:

1. **Bash shell** (comes pre-installed on most Unix-based systems)
2. **curl** (for downloading files)
3. **grep** and **sed** (for text processing)

### Installation Steps

1. **macOS**:

   ```bash
   # curl comes pre-installed
   ```

2. **Ubuntu/Debian**:

   ```bash
   sudo apt-get install curl
   ```

3. **Windows**:
   - Use Windows Subsystem for Linux (WSL)
   - Or install Git Bash which includes these tools

## Usage

### Quick Start

1. Place your HTML file in the same directory as the script
2. Run the script:
   ```bash
   ./extract_png_links.sh
   ```

### How It Works

The script:

1. Looks for PNG image links in the specified HTML file
2. Creates a `downloaded_images` directory
3. Downloads each PNG image found
4. Saves them with their original filenames

### Default Configuration

- Input file: `abilities_04.txt`
- Output directory: `downloaded_images/`

## Features

- Extracts PNG image URLs from HTML content
- Automatically downloads all found images
- Creates organized directory for downloaded files
- Preserves original filenames
- Simple and efficient shell-based implementation

## Troubleshooting

1. **File Not Found Error**

   - Ensure the input file exists in the script directory
   - Check file permissions
   - Verify the file name matches `abilities_04.txt`

2. **Download Issues**

   - Check internet connection
   - Verify URLs are accessible
   - Ensure sufficient disk space

3. **Permission Issues**
   - Make the script executable:
     ```bash
     chmod +x extract_png_links.sh
     ```
   - Check directory write permissions

## Notes

- The script processes only PNG images
- All downloads are saved in the `downloaded_images` directory
- Original filenames are preserved
- The script creates the output directory if it doesn't exist
