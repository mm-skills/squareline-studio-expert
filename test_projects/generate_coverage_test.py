#!/usr/bin/env python3
"""
Generate a SquareLine Studio test project containing widget types NOT
present in the 15 shipped SLS example projects.

Purpose:
  The SLS examples collectively cover 16 widget types. This script creates
  a minimal project with the 6 MISSING types so that their Style_* parts,
  base properties, and export behaviour can be validated by opening/saving
  the project in SLS.

Missing widget types (not in any shipped example):
  1. CALENDAR
  2. CHECKBOX
  3. DROPDOWN
  4. SPINBOX
  5. TABVIEW (container)
  6. TABPAGE (child of TABVIEW)

Usage:
  python3 generate_coverage_test.py

  Then open the generated project in SquareLine Studio 1.6.2:
    File → Open → select test_projects/coverage_test/CoverageTest.spj

  SLS will normalise the project on save. After saving, run the companion
  diff analysis to extract the canonical Style_* parts for each widget type.

Output:
  test_projects/coverage_test/
    CoverageTest.spj
    CoverageTest.sll
    CoverageTest.slp
    Themes.slt
    project.info
    assets/
    components/
"""

import json
import os
import random
import sys
from datetime import datetime

# Add parent scripts/ to path so we can reuse generate_project's helpers
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, os.path.join(REPO_ROOT, "scripts"))

from generate_project import generate_guid


# ── Constants ──────────────────────────────────────────────────────────

PROJECT_NAME = "CoverageTest"
WIDTH = 480
HEIGHT = 480
SHAPE = "RECTANGLE"
BOARD = "Custom Board"
BOARD_VERSION = "v1.0.0"
EDITOR_VERSION = "1.6.2"
LVGL_VERSION = "9.5"

OUTPUT_DIR = os.path.join(SCRIPT_DIR, "coverage_test")


# ── Minimal widget constructors ────────────────────────────────────────
# These intentionally use ONLY the absolute minimum properties needed
# to create a widget that SLS will accept. We want SLS to fill in
# whatever it considers mandatory — that's the whole point of the test.

def _base_props(name, x=0, y=0, w=100, h=50, align="CENTER"):
    """16 mandatory OBJECT/* base properties."""
    return [
        {"nid": 10, "strtype": "OBJECT/Name", "strval": name, "InheritedType": 10},
        {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
        {
            "Flow": 0, "Wrap": False, "Reversed": False,
            "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
            "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
            "strval": "No_layout", "InheritedType": 13
        },
        {"nid": 40, "strtype": "OBJECT/Transform", "InheritedType": 1},
        {"nid": 50, "flags": 17, "strtype": "OBJECT/Position",
         "intarray": [x, y], "InheritedType": 7},
        {"nid": 60, "flags": 17, "strtype": "OBJECT/Size",
         "intarray": [w, h], "InheritedType": 7},
        {"nid": 70, "strtype": "OBJECT/Align", "strval": align,
         "InheritedType": 3},
        {"nid": 75, "strtype": "OBJECT/Extend_click_area", "InheritedType": 6},
        {"nid": 90, "flags": 1048576, "strtype": "OBJECT/Flags", "InheritedType": 1},
        {"nid": 225, "flags": 1048576, "strtype": "OBJECT/Scrolling", "InheritedType": 1},
        {"nid": 230, "strtype": "OBJECT/Scrollable", "strval": "False", "InheritedType": 2},
        {"nid": 300, "strtype": "OBJECT/Scrollbar_mode", "strval": "AUTO", "InheritedType": 3},
        {"nid": 310, "strtype": "OBJECT/Scroll_direction", "strval": "ALL", "InheritedType": 3},
        {"nid": 314, "strtype": "OBJECT/Scroll_snap_x", "strval": "NONE", "InheritedType": 3},
        {"nid": 315, "strtype": "OBJECT/Scroll_snap_y", "strval": "NONE", "InheritedType": 3},
        {"nid": 320, "flags": 1048576, "strtype": "OBJECT/States", "InheritedType": 1},
    ]


def make_calendar(name, x=0, y=0):
    """CALENDAR widget — minimal."""
    props = _base_props(name, x, y, 230, 230)
    props.append({"nid": 1010, "strtype": "CALENDAR/Calendar", "InheritedType": 1})
    return {
        "guid": generate_guid(), "children": [], "properties": props,
        "saved_objtypeKey": "CALENDAR",
    }


def make_checkbox(name, title="Check me", x=0, y=0):
    """CHECKBOX widget — minimal."""
    props = _base_props(name, x, y, 100, 20)
    props.extend([
        {"nid": 1010, "strtype": "CHECKBOX/Checkbox", "InheritedType": 1},
        {"nid": 1020, "strtype": "CHECKBOX/Title", "strval": title, "InheritedType": 10},
    ])
    return {
        "guid": generate_guid(), "children": [], "properties": props,
        "saved_objtypeKey": "CHECKBOX",
    }


def make_dropdown(name, options="Option 1\\nOption 2\\nOption 3", x=0, y=0):
    """DROPDOWN widget — minimal."""
    props = _base_props(name, x, y, 150, 35)
    props.extend([
        {"nid": 1010, "strtype": "DROPDOWN/Dropdown", "InheritedType": 1},
        {"nid": 1020, "strtype": "DROPDOWN/Options", "strval": options, "InheritedType": 10},
    ])
    return {
        "guid": generate_guid(), "children": [], "properties": props,
        "saved_objtypeKey": "DROPDOWN",
    }


def make_spinbox(name, x=0, y=0):
    """SPINBOX widget — minimal."""
    props = _base_props(name, x, y, 100, 40)
    props.append({"nid": 1010, "strtype": "SPINBOX/Spinbox", "InheritedType": 1})
    return {
        "guid": generate_guid(), "children": [], "properties": props,
        "saved_objtypeKey": "SPINBOX",
    }


def make_tabview_with_tabs(name, tab_names=None, x=0, y=0):
    """TABVIEW widget with TABPAGE children — minimal."""
    if tab_names is None:
        tab_names = ["Tab A", "Tab B", "Tab C"]

    props = _base_props(name, x, y, 400, 300)
    props.extend([
        {"nid": 1010, "strtype": "TABVIEW/Tabview", "InheritedType": 1},
        {"nid": 1020, "strtype": "TABVIEW/Tab_position", "strval": "TOP", "InheritedType": 3},
        {"nid": 1030, "strtype": "TABVIEW/Tab_size", "integer": 50, "InheritedType": 6},
        {"nid": 1040, "strtype": "TABVIEW/Tabpages", "InheritedType": 1},
    ])

    tabpages = []
    for tab_title in tab_names:
        tab_name = tab_title.replace(" ", "_")
        tp_props = [
            {"nid": 10, "strtype": "TABPAGE/Name", "strval": tab_name, "InheritedType": 10},
            {"nid": 20, "strtype": "TABPAGE/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "TABPAGE/Layout_type",
                "strval": "No_layout", "InheritedType": 13,
            },
            {"nid": 40, "strtype": "TABPAGE/Transform", "InheritedType": 1},
            {"nid": 90, "flags": 1048576, "strtype": "TABPAGE/Flags", "InheritedType": 1},
            {"nid": 225, "flags": 1048576, "strtype": "TABPAGE/Scrolling", "InheritedType": 1},
            {"nid": 230, "strtype": "TABPAGE/Scrollable", "strval": "False", "InheritedType": 2},
            {"nid": 300, "strtype": "TABPAGE/Scrollbar_mode", "strval": "AUTO", "InheritedType": 3},
            {"nid": 310, "strtype": "TABPAGE/Scroll_direction", "strval": "ALL", "InheritedType": 3},
            {"nid": 314, "strtype": "TABPAGE/Scroll_snap_x", "strval": "NONE", "InheritedType": 3},
            {"nid": 315, "strtype": "TABPAGE/Scroll_snap_y", "strval": "NONE", "InheritedType": 3},
            {"nid": 320, "flags": 1048576, "strtype": "TABPAGE/States", "InheritedType": 1},
            {"nid": 1010, "strtype": "TABPAGE/TabPage", "InheritedType": 1},
            {"nid": 1020, "strtype": "TABPAGE/Title", "strval": tab_title, "InheritedType": 10},
        ]
        tabpages.append({
            "guid": generate_guid(), "children": [], "properties": tp_props,
            "saved_objtypeKey": "TABPAGE",
        })

    return {
        "guid": generate_guid(), "children": tabpages, "properties": props,
        "saved_objtypeKey": "TABVIEW",
    }


def make_screen(name, children, editor_posy=-600):
    """Standard SCREEN with children."""
    return {
        "guid": generate_guid(),
        "children": children,
        "isPage": True,
        "editor_posx": 600,
        "editor_posy": editor_posy,
        "properties": [
            {"nid": 10, "strtype": "OBJECT/Name", "strval": name, "InheritedType": 10},
            {"nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1},
            {
                "Flow": 0, "Wrap": False, "Reversed": False,
                "MainAlignment": 0, "CrossAlignment": 0, "TrackAlignment": 0,
                "LayoutType": 0, "nid": 30, "strtype": "OBJECT/Layout_type",
                "strval": "No_layout", "InheritedType": 13,
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
                "strval": "lv.PART.MAIN, Rectangle, Pad, Text", "InheritedType": 11,
            },
            {
                "part": "lv.PART.SCROLLBAR", "childs": [],
                "nid": 1050, "strtype": "SCREEN/Style_scrollbar",
                "strval": "lv.PART.SCROLLBAR, Rectangle, Pad", "InheritedType": 11,
            },
        ],
        "saved_objtypeKey": "SCREEN",
    }


# ── Main generation ───────────────────────────────────────────────────

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "assets"), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "components"), exist_ok=True)

    # ── Screen 1: CALENDAR + CHECKBOX ──
    screen1_children = [
        make_calendar("TestCalendar", x=-110, y=-80),
        make_checkbox("TestCheckbox1", title="Accept terms", x=-110, y=100),
        make_checkbox("TestCheckbox2", title="Subscribe", x=110, y=100),
    ]
    screen1 = make_screen("ScreenCalendarCheckbox", screen1_children, editor_posy=-600)

    # ── Screen 2: DROPDOWN + SPINBOX ──
    screen2_children = [
        make_dropdown("TestDropdown1", "Red\\nGreen\\nBlue", x=0, y=-80),
        make_dropdown("TestDropdown2", "Small\\nMedium\\nLarge", x=0, y=-20),
        make_spinbox("TestSpinbox1", x=-80, y=60),
        make_spinbox("TestSpinbox2", x=80, y=60),
    ]
    screen2 = make_screen("ScreenDropdownSpinbox", screen2_children, editor_posy=-1200)

    # ── Screen 3: TABVIEW (with 3 TABPAGEs) ──
    tabview = make_tabview_with_tabs("TestTabview", ["Settings", "Status", "About"])
    screen3_children = [tabview]
    screen3 = make_screen("ScreenTabview", screen3_children, editor_posy=-1800)

    screens = [screen1, screen2, screen3]
    screen_guids = [s["guid"] for s in screens]

    nidcnt = 1000205

    # ── .spj ──
    spj = {
        "root": {
            "guid": generate_guid(),
            "children": screens,
            "properties": [
                {"nid": nidcnt, "strtype": "STARTEVENTS/Name",
                 "strval": "___initial_actions0", "InheritedType": 10}
            ],
            "saved_objtypeKey": "STARTEVENTS",
        },
        "animations": [],
        "selected_theme": "Default",
        "selected_screen": screen_guids[0],
        "info": {
            "name": f"{PROJECT_NAME}.spj",
            "depth": 1,
            "width": WIDTH,
            "height": HEIGHT,
            "rotation": 0,
            "offset_x": 0,
            "offset_y": 0,
            "shape": SHAPE,
            "multilang": "DISABLE",
            "description": "Coverage test project — contains widget types not in SLS shipped examples",
            "board": BOARD,
            "board_version": BOARD_VERSION,
            "editor_version": EDITOR_VERSION,
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
            "lvgl_version": LVGL_VERSION,
            "callfuncsexport": "C_FILE",
            "imageexport": "SOURCE",
            "lvgl_include_path": None,
            "naming": "Name",
            "naming_force_lowercase": False,
            "naming_add_subcomponent": False,
            "nidcnt": nidcnt + 1,
            "BitDepth": 16,
            "Name": PROJECT_NAME,
        },
    }

    # ── .sll ──
    sll = {
        "name": f"{PROJECT_NAME}.spj",
        "depth": 1,
        "width": WIDTH,
        "height": HEIGHT,
        "rotation": 0,
        "offset_x": 0,
        "offset_y": 0,
        "shape": SHAPE,
        "multilang": "DISABLE",
        "description": "",
        "board": BOARD,
        "board_version": BOARD_VERSION,
        "editor_version": EDITOR_VERSION,
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
        "lvgl_version": LVGL_VERSION,
        "callfuncsexport": "C_FILE",
        "imageexport": "SOURCE",
        "lvgl_include_path": "",
        "naming": "Name",
        "naming_force_lowercase": False,
        "naming_add_subcomponent": False,
        "nidcnt": nidcnt + 1,
    }

    # ── .slp ──
    slp = {
        "uiExportFolderPath": "",
        "projectExportFolderPath": "",
        "drive_stdio": "-",
        "drive_stdio_path": "",
        "drive_posix": "-",
        "drive_posix_path": "",
        "drive_win32": "-",
        "drive_win32_path": "",
        "drive_fatfs": "-",
        "drive_fatfs_path": "",
    }

    # ── Themes.slt ──
    slt = {
        "deftheme": {"name": "Default", "properties": []},
        "themes": [],
        "selected_theme": "Default",
    }

    # ── project.info ──
    info = {
        "project_name": f"{PROJECT_NAME}.spj",
        "datetime": datetime.now().astimezone().isoformat(),
        "editor_version": EDITOR_VERSION,
        "project_version": 1,
        "user": "",
    }

    # ── Write all files ──
    with open(os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.spj"), "w") as f:
        json.dump(spj, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.sll"), "w") as f:
        json.dump(sll, f, indent=4)

    with open(os.path.join(OUTPUT_DIR, f"{PROJECT_NAME}.slp"), "w") as f:
        json.dump(slp, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "Themes.slt"), "w") as f:
        json.dump(slt, f, indent=2)

    with open(os.path.join(OUTPUT_DIR, "project.info"), "w") as f:
        json.dump(info, f, indent=4)

    print(f"✅ Coverage test project generated at: {OUTPUT_DIR}")
    print()
    print("Project contents:")
    print(f"  Screen 1 (ScreenCalendarCheckbox): CALENDAR ×1, CHECKBOX ×2")
    print(f"  Screen 2 (ScreenDropdownSpinbox):   DROPDOWN ×2, SPINBOX ×2")
    print(f"  Screen 3 (ScreenTabview):           TABVIEW ×1 (3 TABPAGEs)")
    print()
    print("Next steps:")
    print(f"  1. Open in SLS:  File → Open → {OUTPUT_DIR}/{PROJECT_NAME}.spj")
    print(f"  2. SLS will normalise the project (add missing Style_* parts, etc.)")
    print(f"  3. Save:  File → Save (Ctrl+S)")
    print(f"  4. Tell the agent to diff the before/after to extract canonical properties")


if __name__ == "__main__":
    main()
