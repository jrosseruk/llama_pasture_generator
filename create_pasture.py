#!/usr/bin/env python3
"""
Simple SVG Pasture Texture Generator
Creates a pasture scene with fences, grass areas, and llamas
"""

import sys
import random
import os
import argparse
import xml.etree.ElementTree as ET


def load_llama_svg(svg_path):
    """Load and extract the llama SVG content"""
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Extract the group content (skip the XML declaration and outer svg tag)
    llama_content = []
    for child in root:
        llama_content.append(ET.tostring(child, encoding='unicode'))

    return ''.join(llama_content)

def colorize_llama(llama_content, color):
    """Replace only the main body color with a custom color"""
    # The main body is the large path that starts with "M300.96,15.706"
    # Note: ET.tostring adds namespace prefixes like ns0:
    import re

    # Find and replace color only in the main body path (the one with M300.96)
    # Account for possible namespace prefix (ns0:path or path)
    pattern = r'(<(?:ns\d+:)?path style="fill:#DADBDC;" d="M300\.96,15\.706[^"]+"\s*/?>)'

    def replace_color(match):
        return match.group(0).replace('#DADBDC', color)

    colored = re.sub(pattern, replace_color, llama_content)
    return colored

def colorize_tree(tree_content, green_shades):
    """Replace tree greens with custom shades"""
    # Original greens in the tree: #00AD68, #7CDFA8, #218649
    colored = tree_content.replace('#00AD68', green_shades[0])
    colored = colored.replace('#7CDFA8', green_shades[1])
    colored = colored.replace('#218649', green_shades[2])
    return colored

def create_pasture_svg(width_inches, height_inches, num_llamas=100, dpi=138, placement='half'):
    """Generate an SVG pasture texture with llamas"""

    # Convert inches to pixels (dpi increased by 44% from 96 to 138)
    width = width_inches * dpi
    height = height_inches * dpi

    svg_parts = []

    # SVG header - use pixel dimensions for better rendering
    svg_parts.append(f'<svg width="{int(width)}" height="{int(height)}" '
                    f'viewBox="0 0 {width} {height}" '
                    f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">')

    # Load llama SVG template
    llama_svg_path = '/home/j/Documents/svgs/llama-svgrepo-com.svg'
    base_llama_content = None
    if os.path.exists(llama_svg_path):
        base_llama_content = load_llama_svg(llama_svg_path)

    # Load disco ball SVG
    disco_svg_path = '/home/j/Documents/svgs/disco-ball-disco-svgrepo-com.svg'
    disco_content = None
    if os.path.exists(disco_svg_path):
        disco_content = load_llama_svg(disco_svg_path)

    # Load tree SVG
    tree_svg_path = '/home/j/Documents/svgs/tree-svgrepo-com.svg'
    base_tree_content = None
    if os.path.exists(tree_svg_path):
        base_tree_content = load_llama_svg(tree_svg_path)

    # Load sheep SVG
    sheep_svg_path = '/home/j/Documents/svgs/sheep-free-svgrepo-com.svg'
    sheep_content = None
    if os.path.exists(sheep_svg_path):
        sheep_content = load_llama_svg(sheep_svg_path)

    # Load barn SVG
    barn_svg_path = '/home/j/Documents/svgs/barn-farm-svgrepo-com.svg'
    barn_content = None
    if os.path.exists(barn_svg_path):
        barn_content = load_llama_svg(barn_svg_path)

    # Load house SVG
    house_svg_path = '/home/j/Documents/svgs/house-svgrepo-com.svg'
    house_content = None
    if os.path.exists(house_svg_path):
        house_content = load_llama_svg(house_svg_path)

    # Background - sky
    svg_parts.append(f'  <rect width="{width}" height="{height}" fill="#87CEEB"/>')

    # Add fluffy white clouds of various sizes
    cloud_positions = [
        (width * 0.1, height * 0.08, 1.2),   # size multiplier
        (width * 0.25, height * 0.15, 0.8),
        (width * 0.45, height * 0.05, 1.5),
        (width * 0.6, height * 0.18, 0.9),
        (width * 0.75, height * 0.12, 1.3),
        (width * 0.88, height * 0.08, 1.0),
        (width * 0.35, height * 0.22, 0.7),
        (width * 0.92, height * 0.16, 1.1),
    ]

    for cx, cy, size in cloud_positions:
        # Each cloud is made of multiple overlapping circles
        svg_parts.append(f'  <g opacity="0.9">')
        svg_parts.append(f'    <ellipse cx="{cx}" cy="{cy}" rx="{40*size}" ry="{25*size}" fill="white"/>')
        svg_parts.append(f'    <ellipse cx="{cx-25*size}" cy="{cy+5*size}" rx="{30*size}" ry="{20*size}" fill="white"/>')
        svg_parts.append(f'    <ellipse cx="{cx+25*size}" cy="{cy+5*size}" rx="{35*size}" ry="{22*size}" fill="white"/>')
        svg_parts.append(f'    <ellipse cx="{cx+10*size}" cy="{cy-10*size}" rx="{25*size}" ry="{18*size}" fill="white"/>')
        svg_parts.append(f'  </g>')

    # Ground - pasture grass
    ground_height = height * 0.7
    ground_y = height - ground_height

    # Add rolling hills in the background - bigger and more numerous
    hill_y = ground_y + 150
    svg_parts.append(f'  <ellipse cx="{width * 0.15}" cy="{hill_y}" rx="550" ry="280" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * 0.4}" cy="{hill_y}" rx="600" ry="300" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * 0.65}" cy="{hill_y}" rx="650" ry="320" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * 0.88}" cy="{hill_y}" rx="500" ry="250" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * -0.05}" cy="{hill_y}" rx="450" ry="220" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * 1.05}" cy="{hill_y}" rx="450" ry="220" fill="#6BA83A" opacity="0.7"/>')
    svg_parts.append(f'  <ellipse cx="{width * 0.25}" cy="{hill_y + 50}" rx="400" ry="200" fill="#6BA83A" opacity="0.6"/>')
    svg_parts.append(f'  <ellipse cx="{width * 0.75}" cy="{hill_y + 40}" rx="480" ry="240" fill="#6BA83A" opacity="0.6"/>')

    svg_parts.append(f'  <rect y="{ground_y}" width="{width}" '
                    f'height="{ground_height}" fill="#7CB342"/>')

    # Lighter grass patches for texture
    random.seed(42)
    for _ in range(15):
        x = random.uniform(0, width)
        y = random.uniform(ground_y, height)
        w = random.uniform(30, 80)
        h = random.uniform(20, 50)
        svg_parts.append(f'  <ellipse cx="{x}" cy="{y}" rx="{w}" ry="{h}" '
                        f'fill="#8BC34A" opacity="0.6"/>')

    # Add wiggly river - positioned much lower in the pasture
    river_start_y = ground_y + 400
    river_width = 40
    river_path = f'M 0,{river_start_y} Q {width*0.15},{river_start_y-30} {width*0.25},{river_start_y+10} T {width*0.45},{river_start_y+40} Q {width*0.6},{river_start_y+60} {width*0.75},{river_start_y+45} T {width},{river_start_y+70} L {width},{river_start_y+70+river_width} Q {width*0.75},{river_start_y+45+river_width} {width*0.6},{river_start_y+60+river_width} T {width*0.45},{river_start_y+40+river_width} Q {width*0.25},{river_start_y+10+river_width} {width*0.15},{river_start_y-30+river_width} T 0,{river_start_y+river_width} Z'
    svg_parts.append(f'  <path d="{river_path}" fill="#4A90E2" opacity="0.7"/>')
    # River reflection highlights
    river_highlight_path = f'M {width*0.1},{river_start_y-10} Q {width*0.2},{river_start_y+5} {width*0.3},{river_start_y+15} T {width*0.5},{river_start_y+45} Q {width*0.65},{river_start_y+58} {width*0.8},{river_start_y+50}'
    svg_parts.append(f'  <path d="{river_highlight_path}" stroke="#87CEEB" stroke-width="8" fill="none" opacity="0.4"/>')

    # Track building positions for llama collision detection
    buildings = []

    # Add barns randomly scattered on the grass (below the river)
    if barn_content:
        num_barns = 3
        for _ in range(num_barns):
            bx = random.uniform(width * 0.05, width * 0.9)
            by = random.uniform(river_start_y + river_width + 50, height - 100)
            scale = random.uniform(0.1, 0.15)
            svg_parts.append(f'  <g transform="translate({bx}, {by}) scale({scale})">')
            svg_parts.append(barn_content)
            svg_parts.append(f'  </g>')
            # Store building position (approximate bounding box)
            buildings.append((bx, by, 60 * scale, 80 * scale))

    # Add houses randomly scattered on the grass (below the river)
    if house_content:
        num_houses = 3
        for _ in range(num_houses):
            hx = random.uniform(width * 0.05, width * 0.9)
            hy = random.uniform(river_start_y + river_width + 50, height - 100)
            scale = random.uniform(0.08, 0.12)
            svg_parts.append(f'  <g transform="translate({hx}, {hy}) scale({scale})">')
            svg_parts.append(house_content)
            svg_parts.append(f'  </g>')
            # Store building position (approximate bounding box)
            buildings.append((hx, hy, 50 * scale, 70 * scale))

    # Add ponds (water areas) with natural shapes - much bigger lakes
    ponds = []

    # Lake 1 - irregular curved shape (much bigger)
    lake1_x = width * 0.25
    lake1_y = height * 0.65
    scale1 = 3.0
    lake1_path = f'M {lake1_x-40*scale1},{lake1_y} Q {lake1_x-50*scale1},{lake1_y-35*scale1} {lake1_x-20*scale1},{lake1_y-45*scale1} T {lake1_x+30*scale1},{lake1_y-40*scale1} Q {lake1_x+60*scale1},{lake1_y-25*scale1} {lake1_x+65*scale1},{lake1_y+5*scale1} T {lake1_x+45*scale1},{lake1_y+35*scale1} Q {lake1_x+10*scale1},{lake1_y+42*scale1} {lake1_x-25*scale1},{lake1_y+38*scale1} T {lake1_x-40*scale1},{lake1_y} Z'
    svg_parts.append(f'  <path d="{lake1_path}" fill="#4A8FD8" opacity="0.85"/>')
    # Darker center instead of lighter
    svg_parts.append(f'  <ellipse cx="{lake1_x-15}" cy="{lake1_y-15}" rx="{35*scale1}" ry="{25*scale1}" fill="#2E6BA8" opacity="0.3"/>')
    ponds.append((lake1_x, lake1_y, 65*scale1, 45*scale1))

    # Lake 2 - kidney bean shape (much bigger)
    lake2_x = width * 0.7
    lake2_y = height * 0.75
    scale2 = 3.0
    lake2_path = f'M {lake2_x-50*scale2},{lake2_y} Q {lake2_x-60*scale2},{lake2_y-40*scale2} {lake2_x-10*scale2},{lake2_y-50*scale2} T {lake2_x+40*scale2},{lake2_y-35*scale2} Q {lake2_x+70*scale2},{lake2_y-10*scale2} {lake2_x+75*scale2},{lake2_y+15*scale2} Q {lake2_x+60*scale2},{lake2_y+45*scale2} {lake2_x+20*scale2},{lake2_y+50*scale2} Q {lake2_x-10*scale2},{lake2_y+52*scale2} {lake2_x-35*scale2},{lake2_y+40*scale2} Q {lake2_x-48*scale2},{lake2_y+25*scale2} {lake2_x-50*scale2},{lake2_y} Z'
    svg_parts.append(f'  <path d="{lake2_path}" fill="#4A8FD8" opacity="0.85"/>')
    # Darker center instead of lighter
    svg_parts.append(f'  <ellipse cx="{lake2_x-10}" cy="{lake2_y-10}" rx="{42*scale2}" ry="{28*scale2}" fill="#2E6BA8" opacity="0.3"/>')
    ponds.append((lake2_x, lake2_y, 75*scale2, 52*scale2))

    # Lake 3 - amoeba shape (much bigger)
    lake3_x = width * 0.5
    lake3_y = height * 0.85
    scale3 = 3.0
    lake3_path = f'M {lake3_x-35*scale3},{lake3_y} Q {lake3_x-45*scale3},{lake3_y-30*scale3} {lake3_x-15*scale3},{lake3_y-38*scale3} T {lake3_x+20*scale3},{lake3_y-32*scale3} Q {lake3_x+50*scale3},{lake3_y-20*scale3} {lake3_x+48*scale3},{lake3_y+10*scale3} Q {lake3_x+35*scale3},{lake3_y+35*scale3} {lake3_x},{lake3_y+37*scale3} Q {lake3_x-25*scale3},{lake3_y+32*scale3} {lake3_x-35*scale3},{lake3_y} Z'
    svg_parts.append(f'  <path d="{lake3_path}" fill="#4A8FD8" opacity="0.85"/>')
    # Darker center instead of lighter
    svg_parts.append(f'  <ellipse cx="{lake3_x-8}" cy="{lake3_y-10}" rx="{28*scale3}" ry="{20*scale3}" fill="#2E6BA8" opacity="0.3"/>')
    ponds.append((lake3_x, lake3_y, 50*scale3, 38*scale3))

    # Fence posts (vertical) - define fence position first
    fence_y = ground_y + 50
    post_spacing = 80
    post_height = 120
    num_posts = int(width / post_spacing) + 1

    # Add llamas randomly in the pasture (below the fence only!)
    if base_llama_content:
        # Define a palette of bright, light colors for llama bodies
        llama_colors = [
            '#FFD4B2',  # Bright peach
            '#FFDAB9',  # Bright tan
            '#FFF8DC',  # Bright cream
            '#F5DEB3',  # Wheat/bright brown
            '#FFE4C4',  # Bisque/bright beige
            '#B0E0FF',  # Bright light blue
            '#E6B3E6',  # Bright lavender
            '#FFD6E8',  # Bright pink
            '#C7F5D9',  # Bright mint
            '#FFFACD',  # Lemon chiffon/bright yellow
        ]

        # Helper function to check if point is in a pond
        def is_in_pond(x, y, ponds):
            for px, py, rx, ry in ponds:
                # Check if point is inside ellipse
                if ((x - px)**2 / rx**2 + (y - py)**2 / ry**2) <= 1:
                    return True
            return False

        # Helper function to check if point is in the river
        def is_in_river(x, y):
            # Approximate river position (between river_start_y and river_start_y + river_width)
            # Check if y coordinate is in river range (with some margin)
            if y < river_start_y - 10 or y > river_start_y + river_width + 50:
                return False
            # Simple check - if in the y range, assume it might be in river
            return True

        # Helper function to check if point overlaps with buildings
        def is_on_building(x, y, buildings):
            for bx, by, bw, bh in buildings:
                # Check if point is within building bounding box (with some margin)
                if (x >= bx - 10 and x <= bx + bw + 10 and
                    y >= by - 10 and y <= by + bh + 10):
                    return True
            return False

        # Llamas must be placed below the fence and not in ponds, river, or on buildings
        llama_area_start = fence_y + post_height + 10
        llama_count = 0
        attempts = 0
        max_attempts = num_llamas * 50  # Increased to ensure we get all llamas

        while llama_count < num_llamas and attempts < max_attempts:
            # Place llamas based on placement mode
            if placement == 'full':
                # Full width placement
                x = random.uniform(40, width - 40)
            else:
                # Half width placement (right side only)
                x = random.uniform(width * 0.5, width - 40)
            y = random.uniform(llama_area_start, height - 60)
            attempts += 1

            # Skip if in pond, river, or on building
            if is_in_pond(x, y, ponds) or is_in_river(x, y) or is_on_building(x, y, buildings):
                continue

            llama_count += 1
            scale = random.uniform(0.08, 0.15)
            # Random flip for variety
            flip = random.choice([1, -1])
            # Random color for this llama
            color = random.choice(llama_colors)
            transform = f'translate({x}, {y}) scale({flip * scale}, {scale})'

            # Create a colored version of the llama
            colored_llama = colorize_llama(base_llama_content, color)

            # Wrap in a group with transform
            svg_parts.append(f'  <g transform="{transform}">')
            svg_parts.append(colored_llama)
            svg_parts.append(f'  </g>')

        # Warn if we couldn't place all llamas
        if llama_count < num_llamas:
            print(f"Warning: Could only place {llama_count} out of {num_llamas} llamas due to space constraints.")

    # Draw fence posts
    for i in range(num_posts):
        x = i * post_spacing
        svg_parts.append(f'  <rect x="{x-3}" y="{fence_y}" width="6" '
                        f'height="{post_height}" fill="#5D4037"/>')

    # Horizontal fence rails
    rail_y1 = fence_y + 30
    rail_y2 = fence_y + 70
    svg_parts.append(f'  <rect x="0" y="{rail_y1}" width="{width}" '
                    f'height="4" fill="#6D4C41"/>')
    svg_parts.append(f'  <rect x="0" y="{rail_y2}" width="{width}" '
                    f'height="4" fill="#6D4C41"/>')

    # Grass tufts for detail
    for _ in range(25):
        x = random.uniform(0, width)
        y = random.uniform(fence_y + 130, height)
        svg_parts.append(f'  <line x1="{x}" y1="{y}" x2="{x}" y2="{y-10}" '
                        f'stroke="#558B2F" stroke-width="2"/>')

    # Add trees with different shades of green
    if base_tree_content:
        tree_color_variations = [
            ('#00AD68', '#7CDFA8', '#218649'),  # Original
            ('#00CC77', '#8FFFB8', '#2A9955'),  # Brighter
            ('#009955', '#6FD098', '#186638'),  # Darker
            ('#00E680', '#A0FFC8', '#30AA66'),  # Very bright
            ('#008844', '#5FC088', '#155528'),  # Deep green
        ]

        tree_positions = [
            (width * 0.15, height * 0.55, 0.12),
            (width * 0.35, height * 0.62, 0.1),
            (width * 0.82, height * 0.58, 0.14),
            (width * 0.65, height * 0.67, 0.11),
            (width * 0.9, height * 0.72, 0.13),
            (width * 0.08, height * 0.68, 0.09),
            (width * 0.45, height * 0.78, 0.1),
            (width * 0.22, height * 0.72, 0.11),
            (width * 0.55, height * 0.63, 0.13),
            (width * 0.75, height * 0.82, 0.09),
            (width * 0.42, height * 0.59, 0.12),
            (width * 0.12, height * 0.81, 0.1),
            (width * 0.88, height * 0.65, 0.11),
            (width * 0.68, height * 0.56, 0.13),
            (width * 0.95, height * 0.78, 0.08),
            (width * 0.28, height * 0.84, 0.1),
            (width * 0.62, height * 0.88, 0.09),
            (width * 0.05, height * 0.6, 0.11),
        ]

        for tx, ty, scale in tree_positions:
            # Pick random green shades
            shades = random.choice(tree_color_variations)
            colored_tree = colorize_tree(base_tree_content, shades)

            svg_parts.append(f'  <g transform="translate({tx}, {ty}) scale({scale})">')
            svg_parts.append(colored_tree)
            svg_parts.append(f'  </g>')

    # Add one sheep (the black sheep of the family!)
    if sheep_content:
        # Position sheep in a visible spot in the pasture
        sheep_x = width * 0.6
        sheep_y = height * 0.62
        sheep_scale = 0.096  # 20% smaller (0.12 * 0.8)
        svg_parts.append(f'  <g transform="translate({sheep_x}, {sheep_y}) scale({sheep_scale})">')
        svg_parts.append(sheep_content)
        svg_parts.append(f'  </g>')

    # Add disco ball hanging from the top center
    if disco_content:
        # Position disco ball at the top center, hanging down
        disco_x = width * 0.5
        disco_y = 0
        # Scale disco ball proportionally to image width
        # For reference: 10" = 1380px, 20" = 2760px at 138 dpi
        disco_scale = min(0.8, (width / 1380) * 0.2)

        # Disco ball
        svg_parts.append(f'  <g transform="translate({disco_x}, {disco_y}) scale({disco_scale})">')
        svg_parts.append(disco_content)
        svg_parts.append(f'  </g>')

    # Close SVG
    svg_parts.append('</svg>')

    return '\n'.join(svg_parts)


def main():
    parser = argparse.ArgumentParser(description='SVG Pasture Texture Generator')
    parser.add_argument('width', type=float, nargs='?', help='Width in inches')
    parser.add_argument('height', type=float, nargs='?', help='Height in inches')
    parser.add_argument('num_llamas', type=int, nargs='?', default=100, help='Number of llamas (default: 100)')
    parser.add_argument('--placement', choices=['half', 'full'], default='half',
                        help='Llama placement: "half" for right side only (default), "full" for entire width')

    args = parser.parse_args()

    # Get dimensions from user if not provided
    if args.width is None or args.height is None:
        print("SVG Pasture Texture Generator")
        print("=" * 40)
        width_inches = float(input("Enter width in inches: "))
        height_inches = float(input("Enter height in inches: "))
        llama_input = input("Enter number of llamas (default 100): ").strip()
        num_llamas = int(llama_input) if llama_input else 100
        placement_input = input("Enter placement mode (half/full, default half): ").strip().lower()
        placement = placement_input if placement_input in ['half', 'full'] else 'half'
    else:
        width_inches = args.width
        height_inches = args.height
        num_llamas = args.num_llamas
        placement = args.placement

    # Generate SVG
    svg_content = create_pasture_svg(width_inches, height_inches, num_llamas, placement=placement)

    # Save to SVG file
    output_file = f"pasture_{width_inches}x{height_inches}_{num_llamas}llamas.svg"
    with open(output_file, 'w') as f:
        f.write(svg_content)

    print(f"\nCreated: {output_file}")
    print(f"Dimensions: {width_inches}\" x {height_inches}\"")
    print(f"Llamas: {num_llamas}")


if __name__ == "__main__":
    main()
