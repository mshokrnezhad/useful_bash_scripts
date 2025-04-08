#!/usr/bin/env python3
import os
import re
import xml.etree.ElementTree as ET
from collections import defaultdict
import numpy as np
from PIL import Image, ImageDraw


def extract_characters_from_svg(svg_file, output_dir):
    """
    Extract individual pixel art characters from an SVG file and save each as a separate SVG file.

    Args:
        svg_file: Path to the input SVG file
        output_dir: Directory to save the extracted characters
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Parse the SVG file
    try:
        # First, try to parse as XML
        tree = ET.parse(svg_file)
        root = tree.getroot()

        # Get SVG dimensions
        width = float(root.get('width').replace('px', ''))
        height = float(root.get('height').replace('px', ''))

        # Find all rect elements (pixels)
        rects = root.findall('.//{http://www.w3.org/2000/svg}rect')

        if not rects:
            print("No rectangle elements found in the SVG. Trying alternative approach...")
            raise Exception("No rectangles found")

    except Exception as e:
        print(f"XML parsing failed: {e}")
        print("Trying to extract data using regex...")

        # Read the file as text
        with open(svg_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Extract width and height using regex
        width_match = re.search(r'width="([^"]+)"', content)
        height_match = re.search(r'height="([^"]+)"', content)

        if width_match and height_match:
            width = float(width_match.group(1).replace('px', ''))
            height = float(height_match.group(1).replace('px', ''))
        else:
            width = 6001.0  # Default from the file name
            height = 3240.0  # Default from the file name

        # Extract rect elements using regex
        rect_pattern = r'<rect\s+([^>]+)>'
        rects_data = re.findall(rect_pattern, content)

        # Create a list of dictionaries with rect attributes
        rects = []
        for rect_data in rects_data:
            attrs = {}
            for attr_match in re.finditer(r'(\w+)="([^"]+)"', rect_data):
                attrs[attr_match.group(1)] = attr_match.group(2)
            rects.append(attrs)

    # If we still don't have any rectangles, try a bitmap-based approach
    if not rects:
        print("No rectangle elements found. Using bitmap-based approach...")
        return extract_characters_from_bitmap(svg_file, output_dir)

    # Extract pixel positions
    pixels = []
    for rect in rects:
        try:
            x = float(rect.get('x', 0))
            y = float(rect.get('y', 0))
            w = float(rect.get('width', 1))
            h = float(rect.get('height', 1))
            fill = rect.get('fill', '#000000')

            # Ensure fill color is valid
            if not fill or fill == 'none':
                fill = '#000000'  # Default to black if no fill color

            pixels.append((x, y, w, h, fill))
        except (TypeError, ValueError) as e:
            print(f"Error processing rectangle: {rect}, {e}")

    if not pixels:
        print("No valid pixels found in the SVG.")
        return

    # Group pixels by their position to identify characters
    # We'll use a clustering approach to group pixels that are close to each other

    # First, convert pixel positions to a numpy array
    positions = np.array([(x, y) for x, y, _, _, _ in pixels])

    # If we have too few pixels, just save them all as one character
    if len(positions) < 10:
        save_character(pixels, 0, output_dir, width, height)
        return

    # Use a simple clustering approach based on pixel density
    # We'll create a grid and count pixels in each cell
    grid_size = 20  # Adjust based on character size
    grid = defaultdict(list)

    for i, (x, y, w, h, fill) in enumerate(pixels):
        grid_x = int(x / grid_size)
        grid_y = int(y / grid_size)
        grid[(grid_x, grid_y)].append(i)

    # Merge adjacent grid cells to form characters
    visited = set()
    characters = []

    for cell in grid:
        if cell in visited:
            continue

        # BFS to find connected cells
        queue = [cell]
        visited.add(cell)
        character_pixels = []

        while queue:
            current = queue.pop(0)
            character_pixels.extend(grid[current])

            # Check adjacent cells
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    neighbor = (current[0] + dx, current[1] + dy)
                    if neighbor in grid and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

        # Add the character if it has enough pixels
        if len(character_pixels) > 5:  # Minimum pixels for a character
            characters.append([pixels[i] for i in character_pixels])

    print(f"Found {len(characters)} characters")

    # Save each character as a separate SVG file
    for i, character_pixels in enumerate(characters):
        save_character(character_pixels, i, output_dir, width, height)
        # Also save as PNG for preview
        save_character_as_png(character_pixels, i, output_dir, width, height)


def extract_characters_from_bitmap(svg_file, output_dir):
    """
    Alternative approach: Convert SVG to bitmap, then identify characters
    """
    try:
        # Try to use cairosvg if available
        import cairosvg
        png_file = os.path.join(output_dir, "temp.png")
        cairosvg.svg2png(url=svg_file, write_to=png_file)
        img = Image.open(png_file)
    except ImportError:
        print("cairosvg not available. Please install with: pip install cairosvg")
        print("Trying to use PIL directly...")
        try:
            # Try to open directly with PIL (may not work well with SVG)
            img = Image.open(svg_file)
        except Exception as e:
            print(f"Failed to open SVG as image: {e}")
            return

    # Convert to grayscale and threshold to get binary image
    img = img.convert('L')
    threshold = 200
    binary = img.point(lambda p: p > threshold and 255)

    # Find connected components (characters)
    visited = set()
    characters = []

    for y in range(binary.height):
        for x in range(binary.width):
            if (x, y) in visited or binary.getpixel((x, y)) > 0:
                continue

            # BFS to find connected pixels
            queue = [(x, y)]
            visited.add((x, y))
            character_pixels = [(x, y)]

            while queue:
                cx, cy = queue.pop(0)

                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = cx + dx, cy + dy
                    if (0 <= nx < binary.width and 0 <= ny < binary.height and
                            (nx, ny) not in visited and binary.getpixel((nx, ny)) == 0):
                        visited.add((nx, ny))
                        queue.append((nx, ny))
                        character_pixels.append((nx, ny))

            # Add the character if it has enough pixels
            if len(character_pixels) > 10:  # Minimum pixels for a character
                characters.append(character_pixels)

    print(f"Found {len(characters)} characters using bitmap approach")

    # Save each character as a separate PNG file
    for i, character_pixels in enumerate(characters):
        # Find bounding box
        xs = [x for x, y in character_pixels]
        ys = [y for x, y in character_pixels]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Create a new image for this character
        char_width = max_x - min_x + 1
        char_height = max_y - min_y + 1
        char_img = Image.new('RGB', (char_width, char_height), color='white')
        draw = ImageDraw.Draw(char_img)

        # Draw the character
        for x, y in character_pixels:
            draw.point((x - min_x, y - min_y), fill='black')

        # Save the character
        char_img.save(os.path.join(output_dir, f"character_{i}.png"))


def save_character(pixels, index, output_dir, original_width, original_height):
    """
    Save a character as an SVG file

    Args:
        pixels: List of (x, y, width, height, fill) tuples
        index: Character index
        output_dir: Output directory
        original_width: Width of the original SVG
        original_height: Height of the original SVG
    """
    # Find the bounding box of the character
    min_x = min(x for x, y, w, h, _ in pixels)
    max_x = max(x + w for x, y, w, h, _ in pixels)
    min_y = min(y for x, y, w, h, _ in pixels)
    max_y = max(y + h for x, y, w, h, _ in pixels)

    # Add some padding
    padding = 1
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x = min(original_width, max_x + padding)
    max_y = min(original_height, max_y + padding)

    width = max_x - min_x
    height = max_y - min_y

    # Create SVG content
    svg_content = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{min_x} {min_y} {width} {height}">
'''

    # Add each pixel
    for x, y, w, h, fill in pixels:
        svg_content += f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" />\n'

    svg_content += '</svg>'

    # Save the SVG file
    output_file = os.path.join(output_dir, f"character_{index}.svg")
    with open(output_file, 'w') as f:
        f.write(svg_content)

    print(f"Saved character {index} to {output_file}")


def save_character_as_png(pixels, index, output_dir, original_width, original_height):
    """
    Save a character as a PNG file for preview

    Args:
        pixels: List of (x, y, width, height, fill) tuples
        index: Character index
        output_dir: Output directory
        original_width: Width of the original SVG
        original_height: Height of the original SVG
    """
    # Find the bounding box of the character
    min_x = min(x for x, y, w, h, _ in pixels)
    max_x = max(x + w for x, y, w, h, _ in pixels)
    min_y = min(y for x, y, w, h, _ in pixels)
    max_y = max(y + h for x, y, w, h, _ in pixels)

    # Add some padding
    padding = 1
    min_x = max(0, min_x - padding)
    min_y = max(0, min_y - padding)
    max_x = min(original_width, max_x + padding)
    max_y = min(original_height, max_y + padding)

    width = int(max_x - min_x)
    height = int(max_y - min_y)

    # Create a new image with transparent background
    img = Image.new('RGBA', (width, height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(img)

    # Draw each pixel
    for x, y, w, h, fill in pixels:
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
                color = (0, 0, 0, 255)  # Default to black
        else:
            # Handle named colors or other formats
            color = (0, 0, 0, 255)  # Default to black

        # Draw the rectangle
        rect_x = int(x - min_x)
        rect_y = int(y - min_y)
        rect_w = int(w)
        rect_h = int(h)
        draw.rectangle([rect_x, rect_y, rect_x + rect_w, rect_y + rect_h], fill=color)

    # Save the PNG file
    output_file = os.path.join(output_dir, f"character_{index}.png")
    img.save(output_file)
    print(f"Saved PNG preview of character {index} to {output_file}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_file = os.path.join(script_dir, "source_501743406.svg")
    output_dir = os.path.join(script_dir, "extracted_characters")

    print(f"Extracting characters from {svg_file}")
    extract_characters_from_svg(svg_file, output_dir)
    print("Done!")


if __name__ == "__main__":
    main()
