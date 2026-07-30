#!/usr/bin/env python3
"""
Generate a minimal SquareLine Studio project scaffold.

Creates .spj, .sll, Themes.slt, and project.info files that open
correctly in SLS v1.6.x.

Usage:
    python3 generate_project.py --name MyProject --width 480 --height 320 \
        --board "ESP32S335D - MaTouch 3.5-inch Parallel 480x320 TFT with Touch - Arduino-IDE" \
        --screens 2 --output /path/to/output/
"""
import argparse
import json
import os
import random
import time
from datetime import datetime


def generate_guid():
    """Generate a unique GUID in SLS format: GUID<digits>-<digits>S<digits>"""
    a = random.randint(10000000, 99999999)
    b = random.randint(100000, 999999)
    c = random.randint(1000000, 9999999)
    return f"GUID{a}-{b}S{c}"


def make_screen(name, guid, nid_start, editor_posx=600, editor_posy=-600):
    """Create a SCREEN widget with standard default properties."""
    return {
        "guid": guid,
        "children": [],
        "isPage": True,
        "editor_posx": editor_posx,
        "editor_posy": editor_posy,
        "properties": [
            {"nid": 10, "strtype": "OBJECT/Name", "strval": name, "InheritedType": 10},
            {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0,
                "nid": 30, "strtype": "OBJECT/Layout_type",
                "strval": "No_layout", "InheritedType": 13
            },
            {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
            {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags", "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling", "InheritedType": 1},
            {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False", "InheritedType": 2},
            {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO", "InheritedType": 3},
            {"nid": 310, "strtype": "OBJECT/Scroll_direction", "strval": "ALL", "InheritedType": 3},
            {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE", "InheritedType": 3},
            {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE", "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States", "InheritedType": 1},
            {"nid": 1010, "strtype": "SCREEN/Screen", "InheritedType": 1},
            {"nid": 1020, "strtype": "SCREEN/Temporary", "strval": "False", "InheritedType": 2},
            {
                "part": "lv.PART.MAIN", "childs": [],
                "nid": 1040, "strtype": "SCREEN/Style_main",
                "strval": "lv.PART.MAIN, Rectangle, Pad, Text", "InheritedType": 11
            },
            {
                "part": "lv.PART.SCROLLBAR", "childs": [],
                "nid": 1050, "strtype": "SCREEN/Style_scrollbar",
                "strval": "lv.PART.SCROLLBAR, Rectangle, Pad", "InheritedType": 11
            },
        ],
        "saved_objtypeKey": "SCREEN"
    }


def generate_spj(screens, nidcnt, project_name, width, height, board,
                  board_version, editor_version, lvgl_version, shape):
    """Generate the main .spj project file."""
    root_guid = generate_guid()
    screen_guids = [generate_guid() for _ in range(len(screens))]

    screen_objects = []
    for i, (name, guid) in enumerate(zip(screens, screen_guids)):
        posy = -600 - (i * 400)
        screen_objects.append(make_screen(name, guid, 10, editor_posy=posy))

    spj = {
        "root": {
            "guid": root_guid,
            "children": screen_objects,
            "properties": [
                {
                    "nid": nidcnt,
                    "strtype": "STARTEVENTS/Name",
                    "strval": "___initial_actions0",
                    "InheritedType": 10
                }
            ],
            "saved_objtypeKey": "STARTEVENTS"
        },
        "animations": [],
        "selected_theme": "Default",
        "selected_screen": screen_guids[0] if screen_guids else "",
        "info": {
            "name": f"{project_name}.spj",
            "depth": 1,
            "width": width,
            "height": height,
            "rotation": 0,
            "offset_x": 0,
            "offset_y": 0,
            "shape": shape,
            "multilang": "DISABLE",
            "description": "",
            "board": board,
            "board_version": board_version,
            "editor_version": editor_version,
            "image": "",
            "export_temp_image": False,
            "force_export_images": False,
            "flat_export": True,
            "advanced_alpha": False,
            "pointfilter": False,
            "theme_simplified": False,
            "theme_dark": False,
            "theme_color1": 5,
            "theme_color2": 0,
            "custom_variable_prefix": "uic",
            "separate_screen_save": False,
            "hierarchy_state_save": False,
            "reverse_event_order": False,
            "backup_cnt": 0,
            "autosave_cnt": 0,
            "group_color_cnt": 0,
            "imagebytearrayprefix": None,
            "lvgl_version": lvgl_version,
            "callfuncsexport": "C_FILE",
            "imageexport": "SOURCE",
            "lvgl_include_path": None,
            "naming": "Name",
            "naming_force_lowercase": False,
            "naming_add_subcomponent": False,
            "nidcnt": nidcnt + 1,
            "BitDepth": 16,
            "Name": project_name
        }
    }
    return spj


def generate_sll(project_name, width, height, board, board_version,
                 editor_version, lvgl_version, shape, nidcnt):
    """Generate the .sll project metadata file."""
    return {
        "name": f"{project_name}.spj",
        "depth": 1,
        "width": width,
        "height": height,
        "rotation": 0,
        "offset_x": 0,
        "offset_y": 0,
        "shape": shape,
        "multilang": "DISABLE",
        "description": "",
        "board": board,
        "board_version": board_version,
        "editor_version": editor_version,
        "image": "",
        "export_temp_image": False,
        "force_export_images": False,
        "flat_export": True,
        "advanced_alpha": False,
        "pointfilter": False,
        "theme_simplified": False,
        "theme_dark": False,
        "theme_color1": 5,
        "theme_color2": 0,
        "custom_variable_prefix": "uic",
        "separate_screen_save": False,
        "hierarchy_state_save": False,
        "reverse_event_order": False,
        "backup_cnt": 0,
        "autosave_cnt": 0,
        "group_color_cnt": 0,
        "imagebytearrayprefix": "",
        "lvgl_version": lvgl_version,
        "callfuncsexport": "C_FILE",
        "imageexport": "SOURCE",
        "lvgl_include_path": "",
        "naming": "Name",
        "naming_force_lowercase": False,
        "naming_add_subcomponent": False,
        "nidcnt": nidcnt + 1
    }


def generate_slt():
    """Generate the Themes.slt file."""
    return {
        "deftheme": {"name": "Default", "properties": []},
        "themes": [],
        "selected_theme": "Default"
    }


def generate_project_info(project_name, editor_version):
    """Generate the project.info file (v1.6+)."""
    return {
        "project_name": f"{project_name}.spj",
        "datetime": datetime.now().astimezone().isoformat(),
        "editor_version": editor_version,
        "project_version": 1,
        "user": ""
    }


def main():
    parser = argparse.ArgumentParser(description="Generate SquareLine Studio project scaffold")
    parser.add_argument("--name", default="SquareLine_Project", help="Project name")
    parser.add_argument("--width", type=int, default=480, help="Display width")
    parser.add_argument("--height", type=int, default=320, help="Display height")
    parser.add_argument("--shape", default="RECTANGLE", choices=["RECTANGLE", "CIRCLE"],
                        help="Display shape")
    parser.add_argument("--board", default="Custom Board",
                        help="Board name string")
    parser.add_argument("--board-version", default="v1.0.0", help="Board version")
    parser.add_argument("--editor-version", default="1.6.1", help="SLS editor version")
    parser.add_argument("--lvgl-version", default="8.3.11", help="LVGL version")
    parser.add_argument("--screens", type=int, default=1, help="Number of screens")
    parser.add_argument("--screen-names", nargs="*", help="Screen names (default: Screen1, Screen2, ...)")
    parser.add_argument("--output", required=True, help="Output directory")

    args = parser.parse_args()

    # Generate screen names
    if args.screen_names:
        screen_names = args.screen_names
    else:
        screen_names = [f"Screen{i+1}" for i in range(args.screens)]

    nidcnt = 1000205  # Standard starting nidcnt

    os.makedirs(args.output, exist_ok=True)
    os.makedirs(os.path.join(args.output, "assets"), exist_ok=True)
    os.makedirs(os.path.join(args.output, "components"), exist_ok=True)

    # Generate files
    spj = generate_spj(screen_names, nidcnt, args.name, args.width, args.height,
                        args.board, args.board_version, args.editor_version,
                        args.lvgl_version, args.shape)
    sll = generate_sll(args.name, args.width, args.height, args.board,
                        args.board_version, args.editor_version, args.lvgl_version,
                        args.shape, nidcnt)
    slt = generate_slt()
    info = generate_project_info(args.name, args.editor_version)

    # Write files
    with open(os.path.join(args.output, f"{args.name}.spj"), "w") as f:
        json.dump(spj, f, indent=2)

    with open(os.path.join(args.output, f"{args.name}.sll"), "w") as f:
        json.dump(sll, f, indent=4)

    with open(os.path.join(args.output, "Themes.slt"), "w") as f:
        json.dump(slt, f, indent=2)

    with open(os.path.join(args.output, "project.info"), "w") as f:
        json.dump(info, f, indent=4)

    print(f"✅ Project generated at: {args.output}")
    print(f"   Screens: {', '.join(screen_names)}")
    print(f"   Display: {args.width}x{args.height} ({args.shape})")
    print(f"   Board: {args.board}")
    print(f"   Files: {args.name}.spj, {args.name}.sll, Themes.slt, project.info")


if __name__ == "__main__":
    main()
