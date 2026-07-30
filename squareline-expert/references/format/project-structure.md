# SquareLine Studio Project Structure

This document outlines the general file structure and metadata formats for a SquareLine Studio project, covering the file inventory, `project.info`, `.sll`, `.slt`, and `.spj` formats. Focus on these structures when scaffolding a new project.

## 1. File Inventory

A SquareLine Studio project is a **directory** containing these files:

| File | Format | Purpose | Required? |
|------|--------|---------|-----------| 
| `SquareLine_Project.spj` | JSON | Main project: widget tree, screens, events, animations | ✅ |
| `SquareLine_Project.sll` | JSON | Project metadata: resolution, board, LVGL version, paths | ✅ |
| `Themes.slt` | JSON | Theme definitions (colors, fonts per state) | ✅ |
| `project.info` | JSON | Editor metadata: user, timestamp, version (v1.6+) | ✅ (v1.6+) |
| `SquareLine_Project.slp` | Binary? | Unknown purpose (v1.6+, may be lock/state file) | Optional |
| `SquareLine_Project_events.py` | Python | MicroPython event callback stubs (if MicroPython target) | Optional |
| `components/*.ecomp` | JSON | Reusable component definitions (same structure as SPJ widgets) | Optional |
| `assets/*.png` | PNG | Image assets referenced by widgets | Optional |
| `autosave/` | Directory | Auto-saved SPJ backups (.zip) | Auto |
| `backup/` | Directory | Manual backups (.zip) | Auto |
| `cache/` | Directory | Editor thumbnail cache | Auto |

---

## 2. `project.info` (v1.6+)

```json
{
    "project_name": "SquareLine_Project.spj",
    "datetime": "2026-07-29T14:53:13.5018960+01:00",
    "editor_version": "1.6.1",
    "project_version": 1,
    "user": "McNeill Matt"
}
```

---

## 3. `.sll` — Project Metadata

Flat JSON object. Fields vary between versions.

### v1.5.0 fields
```json
{
    "name": "SquareLine_Project.spj",
    "depth": 1, "width": 240, "height": 240,
    "rotation": 0, "offset_x": 0, "offset_y": 0,
    "shape": "CIRCLE",
    "multilang": "DISABLE",
    "board": "Arduino with TFT_eSPI",
    "board_version": "v1.1.1",
    "editor_version": "1.5.0",
    "image": "/9j/4AAQ...",
    "export_temp_image": false, "force_export_images": false, "flat_export": true,
    "advanced_alpha": false, "pointfilter": false,
    "theme_simplified": false, "theme_dark": false,
    "theme_color1": 5, "theme_color2": 0,
    "uiExportFolderPath": "...",
    "projectExportFolderPath": "...",
    "custom_variable_prefix": "uic",
    "backup_cnt": 417, "autosave_cnt": 0,
    "lvgl_version": "8.3.6",
    "callfuncsexport": "C_FILE",
    "imageexport": "SOURCE",
    "lvgl_include_path": "lvgl.h",
    "naming": "", "naming_force_lowercase": false,
    "nidcnt": 1000355
}
```

### v1.6.1 additional/changed fields
```json
{
    "separate_screen_save": false,
    "hierarchy_state_save": false,
    "reverse_event_order": false,
    "group_color_cnt": 0,
    "imagebytearrayprefix": "",
    "naming": "Name",
    "naming_add_subcomponent": false
}
```

> [!IMPORTANT]
> The `shape` field is `"CIRCLE"` for round displays and `"RECTANGLE"` for standard ones. This affects masking in the editor.

---

## 4. `Themes.slt` — Theme Definitions

```json
{
  "deftheme": {
    "name": "Default",
    "properties": []
  },
  "themes": [],
  "selected_theme": "Default"
}
```

---

## 5. `.spj` — Main Project File

### 5.1 Top-Level Structure

#### v1.5.0
```json
{
  "root": { "guid": "...", "deepid": 0, "children": [...], "properties": [...] }
}
```

#### v1.6.1 (expanded)
```json
{
  "root": {
    "guid": "...",
    "children": [...],
    "properties": [...],
    "saved_objtypeKey": "STARTEVENTS"
  },
  "animations": [],
  "selected_theme": "Default",
  "selected_screen": "GUID...",
  "info": { /* duplicate of .sll metadata plus BitDepth, Name */ }
}
```

**Key v1.6 changes:**
- `deepid` field removed from objects
- `animations` array at top level (was inline in v1.5)
- `selected_theme`, `selected_screen` at top level
- `info` block embeds full project metadata (redundant with `.sll`)
- Root object has `saved_objtypeKey: "STARTEVENTS"`

### 5.2 GUID Format

```
GUID<digits>-<digits>S<digits>
```

Example: `"GUID53732461-168142S6514219"`

Cross-references: Events reference target widgets/screens by their GUID. Unset references use `"-"`.

### 5.3 Node IDs (`nid`)

Each property has a numeric `nid`. Pattern:
- **Standard widget properties**: sequential small integers (10, 20, 30, ... 1010, 1020, ...)
- **Event/animation properties**: from the global `nidcnt` counter in `.sll` (e.g., 1000343)

### 5.4 Widget Object Structure

Every widget follows this pattern:
```json
{
  "guid": "GUID...",
  "children": [],
  "isPage": true,           // only on SCREEN objects
  "editor_posx": 600,       // only on SCREEN objects
  "editor_posy": -600,      // only on SCREEN objects
  "properties": [
    // OBJECT/* properties (universal)
    // WIDGET/* properties (widget-specific)
    // _event/* properties (if events attached)
  ],
  "saved_objtypeKey": "BUTTON"
}
```
