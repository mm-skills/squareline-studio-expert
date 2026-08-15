#!/usr/bin/env python3
"""
Detect and restore widget names stripped of underscores by SLS canvas-edit + Save.

Context:
SLS regenerates widget OBJECT/Name values when a user canvas-edits a widget and saves.
The regenerated name strips underscores (e.g., `wsrIdle_temp` → `wsrIdletemp`).
This breaks firmware C-symbol bindings. (See GitHub issue #11)
This script helps users detect and fix this after every SLS Save.
"""

import argparse
import copy
import json
import os
import shutil
import sys
from pathlib import Path

# ANSI colors
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_err(msg, quiet=False):
    if not quiet:
        print(f"{Colors.RED}❌ {msg}{Colors.RESET}")

def print_warn(msg, quiet=False):
    if not quiet:
        print(f"{Colors.YELLOW}⚠️  {msg}{Colors.RESET}")

def print_ok(msg, quiet=False):
    if not quiet:
        print(f"{Colors.GREEN}✅ {msg}{Colors.RESET}")

def print_info(msg, quiet=False):
    if not quiet:
        print(msg)


def find_spj_file(project_path):
    path = Path(project_path)
    if path.is_file() and path.suffix == '.spj':
        return path
    elif path.is_dir():
        spj_files = list(path.glob('*.spj'))
        if not spj_files:
            return None
        return spj_files[0]
    return None

def walk_tree(node, current_screen="root"):
    """
    Generator that yields (widget_node, name_property_node, parent_screen_name, guid).
    """
    if not isinstance(node, dict):
        return

    # Check if this node is a screen
    is_page = node.get("isPage", False)
    screen_name = current_screen
    
    guid = node.get("guid")

    # Find the name property
    name_prop = None
    for prop in node.get("properties", []):
        st = prop.get("strtype")
        if st in ("OBJECT/Name", "TABPAGE/Name"):
            name_prop = prop
            if is_page:
                screen_name = prop.get("strval", current_screen)
            break

    if name_prop and guid:
        yield (node, name_prop, screen_name, guid)

    for child in node.get("children", []):
        yield from walk_tree(child, screen_name)


def load_spj(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_spj(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)

def cmd_save_baseline(spj_data, baseline_file, quiet):
    baseline = {}
    root = spj_data.get("root", spj_data)
    for _, name_prop, _, guid in walk_tree(root):
        baseline[guid] = name_prop.get("strval", "")
    
    with open(baseline_file, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print_ok(f"Saved {len(baseline)} widget names to {baseline_file}", quiet)

def cmd_check_baseline(spj_path, spj_data, baseline_file, fix, quiet):
    try:
        with open(baseline_file, 'r') as f:
            baseline = json.load(f)
    except Exception as e:
        print_err(f"Failed to load baseline: {e}", quiet=False)
        sys.exit(1)

    root = spj_data.get("root", spj_data)
    changes = []
    
    for _, name_prop, screen_name, guid in walk_tree(root):
        if guid in baseline:
            old_name = baseline[guid]
            current_name = name_prop.get("strval", "")
            
            if old_name != current_name:
                changes.append({
                    "guid": guid,
                    "screen": screen_name,
                    "old_name": old_name,
                    "new_name": current_name,
                    "prop_ref": name_prop
                })

    if not changes:
        print_ok("No naming changes detected compared to baseline.", quiet)
        sys.exit(0)
    
    print_warn(f"Found {len(changes)} naming changes:", quiet=False)
    for c in changes:
        print_info(f"  {c['screen']} / {c['guid']}: {Colors.RED}{c['new_name']}{Colors.RESET} (was {Colors.GREEN}{c['old_name']}{Colors.RESET})", quiet=False)
    
    if fix:
        backup_path = f"{spj_path}.bak"
        shutil.copy2(spj_path, backup_path)
        print_info(f"Created backup at {backup_path}", quiet)
        
        for c in changes:
            c['prop_ref']['strval'] = c['old_name']
        
        save_spj(spj_path, spj_data)
        print_ok(f"Restored {len(changes)} names and saved to {spj_path}", quiet=False)
    else:
        sys.exit(1)


def cmd_convention_check(spj_data, quiet):
    root = spj_data.get("root", spj_data)
    warnings = 0
    
    for _, name_prop, screen_name, guid in walk_tree(root):
        name = name_prop.get("strval", "")
        if "_" in name:
            warnings += 1
            print_warn(f"{screen_name} / {name} ({guid}) contains underscores — may be rewritten by SLS on canvas-edit + Save. Consider using camelCase.", quiet=False)
            
    if warnings == 0:
        print_ok("All widget names pass convention check (no underscores found).", quiet)
    else:
        print_warn(f"Found {warnings} widget names with underscores.", quiet=False)
    
    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(description="Detect and restore widget names stripped of underscores by SLS canvas-edit + Save.")
    parser.add_argument("project_path", help="Path to SLS project directory or .spj file")
    parser.add_argument("--save-baseline", metavar="FILE", help="Save current widget names to a baseline JSON file")
    parser.add_argument("--baseline", metavar="FILE", help="Compare current names against a saved baseline")
    parser.add_argument("--fix", action="store_true", help="With --baseline, restore names from baseline in the .spj")
    parser.add_argument("--quiet", action="store_true", help="Only output if problems found")
    
    args = parser.parse_args()
    
    spj_path = find_spj_file(args.project_path)
    if not spj_path:
        print_err(f"No .spj file found in {args.project_path}", quiet=False)
        sys.exit(1)
        
    try:
        spj_data = load_spj(spj_path)
    except Exception as e:
        print_err(f"Failed to load {spj_path}: {e}", quiet=False)
        sys.exit(1)
        
    if args.save_baseline:
        cmd_save_baseline(spj_data, args.save_baseline, args.quiet)
    elif args.baseline:
        cmd_check_baseline(spj_path, spj_data, args.baseline, args.fix, args.quiet)
    else:
        cmd_convention_check(spj_data, args.quiet)

if __name__ == "__main__":
    main()
