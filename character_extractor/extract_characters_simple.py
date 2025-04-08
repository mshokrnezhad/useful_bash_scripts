#!/usr/bin/env python3
import os
import re
import base64
from PIL import Image, ImageDraw
import numpy as np
from collections import defaultdict
import sys


def extract_characters(svg_file, output_dir):
    """
    Extract individual pixel art characters from an SVG file and save each as a separate PNG file.
    This is a simpler approach that works with SVG files containing embedded images.

    Args:
        svg_file: Path to the input SVG file
        output_dir: Directory to save the extracted characters
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Read the SVG file
    with open(svg_file, 'r', encoding='utf-8', errors='ignore') as f:
        svg_content = f.read()

    # Look for embedded image data
    image_data_match = re.search(r'xlink:href="data:image/png;base64,([^"]+)"', svg_content)
    if not image_data_match:
        image_data_match = re.search(r'<image[^>]*href="data:image/png;base64,([^"]+)"', svg_content)

    if image_data_match:
        # Extract and decode the base64 image data
        base64_data = image_data_match.group(1)
        image_data = base64.b64decode(base64_data)

        # Save the decoded image temporarily
        temp_image_path = os.path.join(output_dir, "temp_image.png")
        with open(temp_image_path, 'wb') as f:
            f.write(image_data)

        # Open the image with PIL
        img = Image.open(temp_image_path)

        # Process the image to extract characters
        extract_characters_from_image(img, output_dir)

        # Clean up the temporary file
        os.remove(temp_image_path)
    else:
        print("No embedded image data found in the SVG file.")
        print("Trying to extract directly from SVG structure...")
        extract_from_svg_structure(svg_file, output_dir)


def extract_from_svg_structure(svg_file, output_dir):
    """
    Extract characters directly from the SVG structure by rendering it to a bitmap.
    """
    try:
        # Try to use cairosvg if available
        try:
            import cairosvg
            png_file = os.path.join(output_dir, "temp.png")
            cairosvg.svg2png(url=svg_file, write_to=png_file)
            img = Image.open(png_file)
            extract_characters_from_image(img, output_dir)
            os.remove(png_file)
            return
        except ImportError:
            print("cairosvg not available. Please install with: pip install cairosvg")
            print("Trying alternative method...")
        except OSError as e:
            print(f"Cairo library error: {e}")
            if sys.platform == 'darwin':  # macOS
                print("\nOn macOS, you need to install Cairo library with Homebrew:")
                print("  brew install cairo")
                print("  pip install cairosvg")
            print("\nFalling back to alternative method...")
    except Exception as e:
        print(f"Error using cairosvg: {e}")
        print("Falling back to alternative method...")

    # Alternative method: create a bitmap from the SVG rectangles
    create_bitmap_from_svg(svg_file, output_dir)


def create_bitmap_from_svg(svg_file, output_dir):
    """
    Create a bitmap from SVG rectangles and extract characters.
    """
    # Read the SVG file
    with open(svg_file, 'r', encoding='utf-8', errors='ignore') as f:
        svg_content = f.read()

    # Extract width and height
    width_match = re.search(r'width="([^"]+)"', svg_content)
    height_match = re.search(r'height="([^"]+)"', svg_content)

    if width_match and height_match:
        width = int(float(width_match.group(1).replace('px', '')))
        height = int(float(height_match.group(1).replace('px', '')))
    else:
        width = 6001  # Default from the file name
        height = 3240  # Default from the file name

    # Create a blank image
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Extract rect elements
    rect_pattern = r'<rect\s+([^>]+)>'
    rects_data = re.findall(rect_pattern, svg_content)

    # Draw each rectangle
    for rect_data in rects_data:
        # Extract attributes
        x_match = re.search(r'x="([^"]+)"', rect_data)
        y_match = re.search(r'y="([^"]+)"', rect_data)
        width_match = re.search(r'width="([^"]+)"', rect_data)
        height_match = re.search(r'height="([^"]+)"', rect_data)
        fill_match = re.search(r'fill="([^"]+)"', rect_data)

        if x_match and y_match and width_match and height_match:
            x = float(x_match.group(1))
            y = float(y_match.group(1))
            w = float(width_match.group(1))
            h = float(height_match.group(1))

            # Get fill color
            fill = '#000000'  # Default to black
            if fill_match:
                fill = fill_match.group(1)

            # Convert hex color to RGB
            if fill.startswith('#'):
                if len(fill) == 7:  # #RRGGBB
                    r = int(fill[1:3], 16)
                    g = int(fill[3:5], 16)
                    b = int(fill[5:7], 16)
                    color = (r, g, b, 255)
                elif len(fill) == 9:  # #RRGGBBAA
                    r = int(fill[1:3], 16)
                    g = int(fill[3:5], 16)
                    b = int(fill[5:7], 16)
                    a = int(fill[7:9], 16)
                    color = (r, g, b, a)
                else:
                    color = (0, 0, 0, 255)
            else:
                color = (0, 0, 0, 255)

            # Draw the rectangle
            draw.rectangle([x, y, x + w, y + h], fill=color)

    # Save the image temporarily
    temp_image_path = os.path.join(output_dir, "temp_bitmap.png")
    img.save(temp_image_path)

    # Extract characters from the image
    extract_characters_from_image(img, output_dir)

    # Clean up
    os.remove(temp_image_path)


def extract_characters_from_image(img, output_dir):
    """
    Extract individual characters from an image.

    Args:
        img: PIL Image object
        output_dir: Directory to save the extracted characters
    """
    # Convert to grayscale for processing
    gray_img = img.convert('L')

    # Threshold to create a binary image
    # We'll use a high threshold to keep only the darkest pixels
    binary = gray_img.point(lambda p: p < 200)

    # Convert to numpy array for easier processing
    binary_array = np.array(binary)

    # Find connected components (characters)
    labeled_array, num_features = label_connected_components(binary_array)

    print(f"Found {num_features} potential characters")

    # Extract each character
    for label in range(1, num_features + 1):
        # Get the coordinates of pixels with this label
        y_indices, x_indices = np.where(labeled_array == label)

        # Skip if too few pixels (likely noise)
        if len(x_indices) < 10:
            continue

        # Find the bounding box
        min_x, max_x = np.min(x_indices), np.max(x_indices)
        min_y, max_y = np.min(y_indices), np.max(y_indices)

        # Add padding
        padding = 2
        min_x = max(0, min_x - padding)
        min_y = max(0, min_y - padding)
        max_x = min(img.width - 1, max_x + padding)
        max_y = min(img.height - 1, max_y + padding)

        # Crop the character from the original image
        char_img = img.crop((min_x, min_y, max_x + 1, max_y + 1))

        # Save the character
        char_img.save(os.path.join(output_dir, f"character_{label}.png"))
        print(f"Saved character {label} to {os.path.join(output_dir, f'character_{label}.png')}")


def label_connected_components(binary_array):
    """
    Label connected components in a binary image.

    Args:
        binary_array: Numpy array of binary image

    Returns:
        labeled_array: Array where each connected component has a unique label
        num_features: Number of connected components found
    """
    # Initialize label array
    height, width = binary_array.shape
    labeled_array = np.zeros_like(binary_array, dtype=int)

    # Initialize variables
    current_label = 0
    visited = set()

    # Define directions for 8-connectivity
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # Process each pixel
    for y in range(height):
        for x in range(width):
            if binary_array[y, x] > 0 and (y, x) not in visited:
                # Found a new component
                current_label += 1

                # BFS to find all connected pixels
                queue = [(y, x)]
                visited.add((y, x))
                labeled_array[y, x] = current_label

                while queue:
                    cy, cx = queue.pop(0)

                    # Check all neighbors
                    for dy, dx in directions:
                        ny, nx = cy + dy, cx + dx

                        if (0 <= ny < height and 0 <= nx < width and
                                binary_array[ny, nx] > 0 and (ny, nx) not in visited):
                            visited.add((ny, nx))
                            labeled_array[ny, nx] = current_label
                            queue.append((ny, nx))

    return labeled_array, current_label


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_file = os.path.join(script_dir, "source_501743406.svg")
    output_dir = os.path.join(script_dir, "extracted_characters_simple")

    print(f"Extracting characters from {svg_file}")
    extract_characters(svg_file, output_dir)
    print("Done!")


if __name__ == "__main__":
    main()
