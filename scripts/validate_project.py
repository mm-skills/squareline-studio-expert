#!/usr/bin/env python3
"""
Validate a SquareLine Studio project directory.

Checks:
- Required files exist
- JSON is valid
- GUIDs are unique
- nidcnt is correct
- Widget structure is valid
- Event references resolve
- .sll and .spj info block are consistent

Usage:
    python3 validate_project.py /path/to/project/
"""
import json
import os
import sys


class Validator:
    BUILTIN_MONTSERRAT_SIZES = {str(i) for i in range(8, 50, 2)}
    VALID_ALIGNS = {
        'CENTER', 'TOP_LEFT', 'TOP_MID', 'TOP_RIGHT', 'BOTTOM_LEFT',
        'BOTTOM_MID', 'BOTTOM_RIGHT', 'LEFT_MID', 'RIGHT_MID'
    }
    NEWLINE_CHECK_TYPES = {
        'LABEL/Text', 'DROPDOWN/Options', 'DROPDOWN/Base_text', 'ROLLER/Options',
        'TEXTAREA/Text', 'TEXTAREA/Placeholder', 'CHECKBOX/Title'
    }
    REQUIRED_STYLE_PARTS = {
        'ARC': ['Style_main', 'Style_indicator', 'Style_knob'],
        'BAR': ['Style_main', 'Style_indicator'],
        'BUTTON': ['Style_main'],
        'CALENDAR': ['Style_main', 'Style_items'],
        'CHART': ['Style_bg', 'Style_indicator', 'Style_items', 'Style_scrollbar', 'Style_ticks'],
        'CHECKBOX': ['Style_main', 'Style_bullet'],
        'CONTAINER': ['Style_main', 'Style_scrollbar'],
        'DROPDOWN': ['Style_main', 'Style_indicator', 'Style_list_main', 'Style_list_scrollbar', 'Style_list_selected'],
        'IMAGE': ['Style_main'],
        'IMGBUTTON': ['Style_main'],
        'KEYBOARD': ['Style_main', 'Style_items'],
        'LABEL': ['Style_main'],
        'PANEL': ['Style_main', 'Style_scrollbar'],
        'ROLLER': ['Style_main', 'Style_selected'],
        'SCREEN': ['Style_main', 'Style_scrollbar'],
        'SLIDER': ['Style_main', 'Style_indicator', 'Style_knob'],
        'SPINBOX': ['Style_main', 'Style_cursor'],
        'SPINNER': ['Style_main', 'Style_indicator'],
        'SWITCH': ['Style_main', 'Style_indicator', 'Style_knob'],
        'TABVIEW': ['Style_main', 'Style_buttons_main', 'Style_buttons_items'],
        'TABPAGE': ['Style_main', 'Style_scrollbar'],
        'TEXTAREA': ['Style_main', 'Style_cursor', 'Style_placeholder', 'Style_selected'],
    }

    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.errors = []
        self.warnings = []
        self.guids = set()
        self.nids = set()
        self.max_nid = 0
        self.widget_names = set()
        self.screen_guids = set()
        self.fonts_checked = 0

    def error(self, msg):
        self.errors.append(f"❌ {msg}")

    def warn(self, msg):
        self.warnings.append(f"⚠️  {msg}")

    def ok(self, msg):
        print(f"  ✅ {msg}")

    def check_files_exist(self):
        """Check required files exist."""
        # Find .spj and .sll files
        spj_files = [f for f in os.listdir(self.project_dir) if f.endswith('.spj')]
        sll_files = [f for f in os.listdir(self.project_dir) if f.endswith('.sll')]

        if not spj_files:
            self.error("No .spj file found")
            return None, None
        if not sll_files:
            self.error("No .sll file found")
            return spj_files[0], None

        slt_path = os.path.join(self.project_dir, "Themes.slt")
        if not os.path.exists(slt_path):
            self.error("Themes.slt not found")
        else:
            self.ok("Themes.slt exists")

        self.ok(f"Project files: {spj_files[0]}, {sll_files[0]}")
        return spj_files[0], sll_files[0]

    def check_json_valid(self, filename):
        """Check a file contains valid JSON."""
        filepath = os.path.join(self.project_dir, filename)
        try:
            with open(filepath) as f:
                data = json.load(f)
            self.ok(f"{filename}: valid JSON")
            return data
        except json.JSONDecodeError as e:
            self.error(f"{filename}: invalid JSON - {e}")
            return None
        except FileNotFoundError:
            self.error(f"{filename}: file not found")
            return None

    def collect_guids_and_nids(self, obj, path="root"):
        """Recursively collect all GUIDs and nids."""
        if isinstance(obj, dict):
            guid = obj.get("guid")
            if guid:
                if guid in self.guids:
                    self.error(f"Duplicate GUID: {guid} at {path}")
                self.guids.add(guid)

                if obj.get("saved_objtypeKey") == "SCREEN":
                    self.screen_guids.add(guid)

            for prop in obj.get("properties", []):
                nid = prop.get("nid")
                if nid is not None:
                    if nid in self.nids:
                        # Only warn for small nids since widget defaults reuse them
                        if nid > 10000:
                            self.error(f"Duplicate nid {nid} at {path}")
                    self.nids.add(nid)
                    self.max_nid = max(self.max_nid, nid)

                name = None
                if prop.get("strtype") == "OBJECT/Name":
                    name = prop.get("strval", "")
                    if name in self.widget_names:
                        self.warn(f"Duplicate widget name: '{name}' at {path}")
                    self.widget_names.add(name)

            for i, child in enumerate(obj.get("children", [])):
                child_name = ""
                for p in child.get("properties", []):
                    if p.get("strtype") == "OBJECT/Name":
                        child_name = p.get("strval", "")
                self.collect_guids_and_nids(child, f"{path}/{child_name or i}")

    def check_widget_structure(self, obj, path="root"):
        """Check each widget has required fields."""
        if isinstance(obj, dict):
            objtype = obj.get("saved_objtypeKey")
            if objtype and objtype != "STARTEVENTS":
                has_name = False
                style_parts_found = set()
                
                for prop in obj.get("properties", []):
                    st = prop.get("strtype", "")
                    val = prop.get("strval", "")
                    
                    if st == "OBJECT/Name" or st == "TABPAGE/Name":
                        has_name = True

                    if "OBJ_FLAG_HIDDEN" in st:
                        self.error(f"Widget at {path} uses LVGL constant OBJ_FLAG_HIDDEN. Use OBJECT/Hidden instead.")

                    if st.endswith("/Align"):
                        if isinstance(val, str) and val.startswith("ALIGN_"):
                            self.error(f"Widget at {path} has invalid alignment '{val}' (starts with ALIGN_)")
                        elif val and val not in self.VALID_ALIGNS:
                            self.error(f"Widget at {path} has invalid alignment '{val}'")

                    if st in self.NEWLINE_CHECK_TYPES:
                        if isinstance(val, str) and '\n' in val:
                            self.error(f"Widget at {path} has unescaped newline in {st}. Should be literal \\\\n")

                    for part in self.REQUIRED_STYLE_PARTS.get(objtype, []):
                        if st.endswith(f"/{part}"):
                            style_parts_found.add(part)

                if not has_name:
                    self.error(f"Widget at {path} has no OBJECT/Name property")

                if objtype == "SCREEN" and not obj.get("isPage"):
                    self.warn(f"Screen at {path} missing isPage: true")
                    
                if objtype in self.REQUIRED_STYLE_PARTS:
                    for req_part in self.REQUIRED_STYLE_PARTS[objtype]:
                        if req_part not in style_parts_found:
                            self.error(f"Widget at {path} ({objtype}) is missing required style part '{req_part}'")

            for i, child in enumerate(obj.get("children", [])):
                child_name = ""
                for p in child.get("properties", []):
                    if p.get("strtype") == "OBJECT/Name":
                        child_name = p.get("strval", "")
                self.check_widget_structure(child, f"{path}/{child_name or i}")

    def check_event_refs(self, obj, path="root"):
        """Check event GUID references resolve to known GUIDs."""
        if isinstance(obj, dict):
            for prop in obj.get("properties", []):
                if prop.get("strtype") == "_event/EventHandler":
                    self._check_event_children(prop.get("childs", []), path)

            for child in obj.get("children", []):
                self.check_event_refs(child, path)

    def _check_event_children(self, childs, path):
        for child in childs:
            if child.get("strtype") == "_event/action":
                for param in child.get("childs", []):
                    if param.get("InheritedType") == 9:
                        ref = param.get("strval", "")
                        if ref and ref != "-" and ref not in self.guids:
                            self.error(
                                f"Event at {path}: reference to unknown GUID '{ref}' "
                                f"in {param.get('strtype')}"
                            )

    def check_fonts(self, obj, path="root"):
        """Check font references are valid."""
        if isinstance(obj, dict):
            for prop in obj.get("properties", []):
                self._check_font_prop(prop, path)

            for i, child in enumerate(obj.get("children", [])):
                child_name = ""
                for p in child.get("properties", []):
                    if p.get("strtype") == "OBJECT/Name" or p.get("strtype") == "TABPAGE/Name":
                        child_name = p.get("strval", "")
                self.check_fonts(child, f"{path}/{child_name or i}")

    def _check_font_prop(self, prop, path):
        if prop.get("strtype") == "_style/Text_Font" and prop.get("InheritedType") == 3:
            font_name = prop.get("strval", "")
            if font_name:
                self.fonts_checked += 1
                if font_name.startswith("montserrat_"):
                    size = font_name.split("_")[-1]
                    if size not in self.BUILTIN_MONTSERRAT_SIZES:
                        self.warn(f"Unknown built-in font size '{font_name}' at {path}")
                elif font_name.startswith("ui_font_"):
                    pass # Valid custom font
                else:
                    self.warn(f"Unrecognized font naming convention '{font_name}' at {path}")
        
        for child in prop.get("childs", []):
            self._check_font_prop(child, path)

    def check_consistency(self, spj_data, sll_data):
        """Check .spj info block matches .sll."""
        info = spj_data.get("info", {})
        if not info:
            self.warn(".spj has no info block (may be v1.5 format)")
            return

        for key in ["width", "height", "board", "editor_version", "lvgl_version"]:
            spj_val = info.get(key)
            sll_val = sll_data.get(key)
            if spj_val != sll_val:
                self.error(
                    f"Inconsistency: .spj info.{key}={spj_val!r} vs .sll {key}={sll_val!r}"
                )

    def check_nidcnt(self, sll_data):
        """Check nidcnt is greater than max nid used (v1.6+ only)."""
        nidcnt = sll_data.get("nidcnt", 0)
        # v1.5 uses large hash-based nids; only check for v1.6+ sequential nids
        if self.max_nid > 100000000:
            self.ok(f"nidcnt check skipped (v1.5 hash-based nids detected)")
            return
        if self.max_nid >= nidcnt:
            self.error(
                f"nidcnt ({nidcnt}) must be greater than max nid used ({self.max_nid})"
            )
        else:
            self.ok(f"nidcnt ({nidcnt}) > max nid ({self.max_nid})")

    def validate(self):
        """Run all validation checks."""
        print(f"\n🔍 Validating: {self.project_dir}\n")

        # Check files exist
        spj_name, sll_name = self.check_files_exist()
        if not spj_name:
            return False

        # Load and validate JSON
        spj_data = self.check_json_valid(spj_name)
        sll_data = self.check_json_valid(sll_name) if sll_name else None
        slt_data = self.check_json_valid("Themes.slt")

        if spj_data:
            if spj_data.get("info", {}).get("Name") == "SquareLine_Project":
                self.warn("Project Name is 'SquareLine_Project' (default)")

        if slt_data:
            deftheme = slt_data.get("deftheme", {})
            if deftheme.get("name") != "Default":
                self.warn(f"Themes.slt deftheme.name is '{deftheme.get('name')}', should be 'Default'")

        slp_files = [f for f in os.listdir(self.project_dir) if f.endswith('.slp')]
        if not slp_files:
            self.warn("No .slp file found (generate_project.py should create it)")
        else:
            slp_data = self.check_json_valid(slp_files[0])
            if slp_data:
                ui_path = slp_data.get("uiExportFolderPath", "")
                proj_path = slp_data.get("projectExportFolderPath", "")
                if ui_path or proj_path:
                    self.warn(f"{slp_files[0]} contains non-empty export paths which may be stale. uiExportFolderPath='{ui_path}', projectExportFolderPath='{proj_path}'")

        if not spj_data:
            return False

        # Check structure
        root = spj_data.get("root", spj_data)
        self.collect_guids_and_nids(root)
        self.ok(f"Found {len(self.guids)} unique GUIDs, {len(self.screen_guids)} screens")

        self.check_widget_structure(root)
        self.check_event_refs(root)
        self.check_fonts(root)
        self.ok(f"Checked {self.fonts_checked} font references")

        if sll_data:
            self.check_consistency(spj_data, sll_data)
            self.check_nidcnt(sll_data)

        # Report
        print()
        if self.warnings:
            for w in self.warnings:
                print(f"  {w}")
        if self.errors:
            for e in self.errors:
                print(f"  {e}")
            print(f"\n🔴 Validation FAILED: {len(self.errors)} error(s), {len(self.warnings)} warning(s)")
            return False
        else:
            print(f"\n🟢 Validation PASSED: {len(self.warnings)} warning(s)")
            return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_project.py <project_directory>")
        sys.exit(1)

    project_dir = sys.argv[1]
    if not os.path.isdir(project_dir):
        print(f"Error: '{project_dir}' is not a directory")
        sys.exit(1)

    validator = Validator(project_dir)
    success = validator.validate()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
