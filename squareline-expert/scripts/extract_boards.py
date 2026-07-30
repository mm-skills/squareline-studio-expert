#!/usr/bin/env python3
"""
Extract board definitions from the user's SquareLine Studio installation.

Reads .slb (JSON) board definition files from:
  1. ~/SquareLine/boards/          (downloaded boards)
  2. /Applications/SquareLine_Studio.app/Contents/boards/  (bundled boards, macOS)

Caches results to a local JSON file. Subsequent runs read from cache unless
--refresh is specified.

Usage:
    python3 extract_boards.py                  # Use cache or extract + cache
    python3 extract_boards.py --refresh        # Force re-extract from .slb files
    python3 extract_boards.py --group Elecrow  # Filter by group
    python3 extract_boards.py --json           # Output raw JSON
    python3 extract_boards.py --board "MaTouch" # Search for a board by name
"""
import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SCRIPT_DIR, ".board_cache.json")


def find_slb_files():
    """Find all .slb board definition files on the system."""
    search_paths = [
        os.path.expanduser("~/SquareLine/boards"),
        "/Applications/SquareLine_Studio.app/Contents/boards",
    ]

    slb_files = []
    for base in search_paths:
        if os.path.isdir(base):
            slb_files.extend(glob.glob(f"{base}/**/*.slb", recursive=True))

    return slb_files


def parse_boards(slb_files):
    """Parse .slb files, deduplicate by title (keep latest version)."""
    board_map = {}

    for path in slb_files:
        try:
            with open(path) as f:
                data = json.load(f)
            title = data.get("title", "")
            version = data.get("version", "v0.0.0")

            if title not in board_map or version > board_map[title]["version"]:
                # Keep only the fields we need
                board_map[title] = {
                    "title": title,
                    "group": data.get("group", "Other"),
                    "version": version,
                    "width": data.get("width", 0),
                    "height": data.get("height", 0),
                    "shape": data.get("shape", ""),
                    "color_depth": data.get("color_depth", "16"),
                    "supported_lvgl_version": data.get("supported_lvgl_version", ""),
                    "language": data.get("language", "C"),
                    "lvgl_include_path": data.get("lvgl_include_path", "lvgl.h"),
                    "lvgl_export_path": data.get("lvgl_export_path", ""),
                    "ui_export_path": data.get("ui_export_path", ""),
                    "flat_export": data.get("flat_export", True),
                    "short_description": data.get("short_description", ""),
                }
        except (json.JSONDecodeError, KeyError):
            continue

    return board_map


def write_cache(board_map):
    """Write board map to cache file."""
    cache = {
        "extracted_at": datetime.now().isoformat(),
        "board_count": len(board_map),
        "boards": board_map,
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)
    return cache


def read_cache():
    """Read board map from cache file. Returns None if no cache."""
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError):
        return None


def get_boards(refresh=False):
    """Get board map from cache or extract fresh."""
    if not refresh:
        cache = read_cache()
        if cache:
            extracted = cache.get("extracted_at", "unknown")
            count = cache.get("board_count", 0)
            print(f"Using cached data ({count} boards, extracted {extracted})")
            print(f"Run with --refresh to re-extract from .slb files\n")
            return cache["boards"]

    # Extract fresh
    slb_files = find_slb_files()
    if not slb_files:
        print("No .slb board files found.")
        print("Searched:")
        print("  ~/SquareLine/boards/")
        print("  /Applications/SquareLine_Studio.app/Contents/boards/")
        print("\nMake sure SquareLine Studio is installed and has downloaded boards.")
        sys.exit(1)

    board_map = parse_boards(slb_files)
    cache = write_cache(board_map)
    print(f"Extracted {len(slb_files)} .slb files → {len(board_map)} unique boards")
    print(f"Cached to {CACHE_FILE}\n")
    return board_map


def print_table(board_map, group_filter=None, search=None):
    """Print boards as a markdown table grouped by manufacturer."""
    groups = defaultdict(list)
    for title, data in board_map.items():
        group = data.get("group", "Other")
        if group_filter and group.lower() != group_filter.lower():
            continue
        if search and search.lower() not in title.lower():
            continue
        groups[group].append(data)

    total = 0
    for group in sorted(groups.keys()):
        boards = sorted(groups[group], key=lambda x: x["title"])
        total += len(boards)
        print(f"\n## {group} ({len(boards)} boards)\n")
        print("| Board String | Res | Color | LVGL | Ver | Shape |")
        print("|---|:---:|---|---|---|---|")
        for b in boards:
            shape = b.get("shape", "—") or "—"
            print(
                f'| `"{b["title"]}"` '
                f'| {b["width"]}×{b["height"]} '
                f'| {b.get("color_depth", "16")} '
                f'| {b.get("supported_lvgl_version", "?")} '
                f'| {b["version"]} '
                f'| {shape} |'
            )

    if total == 0 and (group_filter or search):
        print(f"\nNo boards found matching filter.")
    else:
        print(f"\n**Total: {total} unique boards**")


def print_json(board_map, group_filter=None, search=None):
    """Print boards as JSON."""
    output = []
    for title, data in sorted(board_map.items()):
        if group_filter and data.get("group", "").lower() != group_filter.lower():
            continue
        if search and search.lower() not in title.lower():
            continue
        output.append(data)
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Extract SLS board definitions")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--group", help="Filter by group name (e.g., Elecrow)")
    parser.add_argument("--board", help="Search board titles (e.g., 'MaTouch')")
    parser.add_argument("--refresh", action="store_true",
                        help="Force re-extract from .slb files (ignore cache)")
    args = parser.parse_args()

    board_map = get_boards(refresh=args.refresh)

    if args.json:
        print_json(board_map, args.group, args.board)
    else:
        print_table(board_map, args.group, args.board)


if __name__ == "__main__":
    main()
