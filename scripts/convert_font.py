#!/usr/bin/env python3
"""
Helper script to wrap lv_font_conv and generate SquareLine Studio font files.

Generates the .c, .bin, and .fcfg files required for custom fonts in a single command.

Usage:
# Text font with ASCII range + extra symbols:
python3 convert_font.py \
  --font DMSans-Regular.ttf \
  --name dm_sans_text_14 \
  --size 14 \
  --range 0x20-0x7f \
  --symbols '°·×✕…—–€£' \
  --output ./assets/fonts/

# Numbers-only display font:
python3 convert_font.py \
  --font DMSans-Bold.ttf \
  --name dm_sans_hero_80 \
  --size 80 \
  --symbols '0123456789.°-:ABCDEFGHIJKLMNOPQRSTUVWXYZ✕' \
  --output ./assets/fonts/

# Icon font with specific code points:
python3 convert_font.py \
  --font lucide.ttf \
  --name lucide_24 \
  --size 24 \
  --range 0xE056 --range 0xE087 --range 0xE0B4 \
  --output ./assets/fonts/
"""
import argparse
import json
import os
import platform
import re
import subprocess
import sys


def find_converter(override_path=None):
    """Auto-detect the lv_font_conv binary based on platform."""
    if override_path and os.path.exists(override_path):
        return override_path

    system = platform.system()
    binary_name = ""
    search_paths = []

    if system == "Darwin":
        binary_name = "lv_font_conv-osx"
        search_paths = ["/Applications/SquareLine_Studio.app/Contents/MacOS/lvgl/"]
    elif system == "Linux":
        binary_name = "lv_font_conv-linux"
        search_paths = [
            "/opt/SquareLine_Studio/lvgl/",
            os.path.expanduser("~/SquareLine_Studio/lvgl/")
        ]
    elif system == "Windows":
        binary_name = "lv_font_conv.exe"
        search_paths = [
            "C:\\Program Files\\SquareLine_Studio\\lvgl\\",
            "C:\\Program Files (x86)\\SquareLine_Studio\\lvgl\\"
        ]
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

    for path in search_paths:
        full_path = os.path.join(path, binary_name)
        if os.path.exists(full_path):
            return full_path

    return None


def run_converter(converter, font_path, size, bpp, ranges, symbols, output_path, format, font_name):
    """Run the lv_font_conv binary."""
    cmd = [
        converter,
        "--bpp", str(bpp),
        "--size", str(size),
        "--font", font_path
    ]

    for r in ranges:
        cmd.extend(["-r", r])
    
    if symbols:
        cmd.extend(["--symbols", symbols])

    cmd.extend([
        "--no-compress",
        "--no-prefilter",
        "--format", format,
        "-o", output_path
    ])

    if format == "lvgl":
        cmd.extend(["--lv-font-name", f"ui_font_{font_name}"])

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running converter for format {format}:")
        print(e.stderr)
        return False


def generate_fcfg(name, ttf_path, assets_prefix, size, bpp, ranges, symbols, output_dir):
    """Generate the .fcfg JSON metadata file."""
    ttf_filename = os.path.basename(ttf_path)
    
    # Ensure prefix uses forward slashes and doesn't end with a slash
    prefix = assets_prefix.replace("\\", "/").rstrip("/")

    fcfg_data = {
        "codename": name,
        "ttf_path": f"{prefix}/{ttf_filename}",
        "bin_path": f"{prefix}/ui_font_{name}.bin",
        "c_path": f"{prefix}/ui_font_{name}.c",
        "cfg_path": f"{prefix}/ui_font_{name}.fcfg",
        "size": size,
        "bpp": bpp,
        "letters": 0,
        "ranges": ranges,
        "symbols": symbols,
        "customparams": "--no-compress --no-prefilter",
        "uploaded": False
    }

    fcfg_path = os.path.join(output_dir, f"ui_font_{name}.fcfg")
    with open(fcfg_path, "w") as f:
        json.dump(fcfg_data, f, indent=4)
    
    return fcfg_path


def main():
    parser = argparse.ArgumentParser(
        description="Generate SquareLine Studio font files using lv_font_conv",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__.split("Usage:\n")[-1] if "Usage:\n" in __doc__ else ""
    )
    
    parser.add_argument("--font", required=True, help="Path to source TTF file")
    parser.add_argument("--name", required=True, help="Font codename (e.g., dm_sans_text_14)")
    parser.add_argument("--size", required=True, type=int, help="Font size in pixels")
    parser.add_argument("--output", required=True, help="Output directory for generated files")
    parser.add_argument("--bpp", type=int, default=4, choices=[1, 2, 3, 4, 8], help="Bits per pixel (default: 4)")
    parser.add_argument("--range", action="append", default=[], help="Unicode range(s) to include (can be specified multiple times)")
    parser.add_argument("--symbols", default="", help="Individual characters to include")
    parser.add_argument("--converter-path", help="Override path to lv_font_conv binary")
    parser.add_argument("--assets-prefix", default="/assets/fonts", help="Project-relative prefix for paths in .fcfg (default: /assets/fonts)")

    args = parser.parse_args()

    # Validations
    if not os.path.exists(args.font):
        print(f"Error: Font file not found at {args.font}")
        sys.exit(1)

    if not args.range and not args.symbols:
        print("Error: At least one --range or --symbols must be specified.")
        sys.exit(1)

    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", args.name):
        print(f"Error: Invalid font name '{args.name}'. Must be a valid C identifier.")
        sys.exit(1)

    # Detect converter
    print("Detecting lv_font_conv binary...")
    converter = find_converter(args.converter_path)
    if not converter:
        print("Error: Could not find lv_font_conv binary. Please install SquareLine Studio or provide --converter-path.")
        sys.exit(1)
    print(f"Using converter: {converter}")

    # Setup output directory
    os.makedirs(args.output, exist_ok=True)
    c_out = os.path.join(args.output, f"ui_font_{args.name}.c")
    bin_out = os.path.join(args.output, f"ui_font_{args.name}.bin")

    # Generate C format
    print(f"Generating C file: {c_out}...")
    if not run_converter(converter, args.font, args.size, args.bpp, args.range, args.symbols, c_out, "lvgl", args.name):
        sys.exit(1)

    # Generate Bin format
    print(f"Generating BIN file: {bin_out}...")
    if not run_converter(converter, args.font, args.size, args.bpp, args.range, args.symbols, bin_out, "bin", args.name):
        sys.exit(1)

    # Generate FCFG metadata
    print("Generating .fcfg metadata file...")
    fcfg_out = generate_fcfg(args.name, args.font, args.assets_prefix, args.size, args.bpp, args.range, args.symbols, args.output)

    print("\n✅ Font conversion successful!")
    print(f"   C File   : {c_out}")
    print(f"   BIN File : {bin_out}")
    print(f"   FCFG File: {fcfg_out}")

if __name__ == "__main__":
    main()
