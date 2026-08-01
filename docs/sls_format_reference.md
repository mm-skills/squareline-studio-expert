# SquareLine Studio Project File Format — Reference Documentation

> [!NOTE]
> Reverse-engineered from two real SLS projects (v1.5.0 and v1.6.1), cross-referenced with
> [official SLS documentation](https://docs.squareline.io/docs/squareline/) and community sources.
> **No official file format specification exists** — this is the first comprehensive attempt at one.
>
> **Source projects analysed:**
> - `research/crowpanel_1_28_reference/` — v1.5.0, CrowPanel 1.28" round (240×240), 5 screens, events, animations
> - `research/new01/` — v1.6.1, MaTouch 3.5" (480×320), all 23 widget types, 3 events, style states
>
> **Official documentation cross-references:**
> - [Widgets](https://docs.squareline.io/docs/squareline/widgets) — widget properties and inspector panels
> - [Events](https://docs.squareline.io/docs/squareline/events) — event triggers and action wiring
> - [Styles](https://docs.squareline.io/docs/squareline/styles) — style states, parts, and properties
> - [Screens](https://docs.squareline.io/docs/squareline/screens) — screen management and transitions
> - [Animations](https://docs.squareline.io/docs/squareline/animations) — animation editor
> - [Themes](https://docs.squareline.io/docs/squareline/themes) — theme definitions
> - [Fonts](https://docs.squareline.io/docs/squareline/fonts) — font management
> - [Assets](https://docs.squareline.io/docs/squareline/assets) — image asset management
> - [Components](https://docs.squareline.io/docs/squareline/components) — reusable component system
> - [Export](https://docs.squareline.io/docs/squareline/export) — code export settings
> - [Project Settings](https://docs.squareline.io/docs/squareline/project) — project configuration

---

## 1. File Inventory

A SquareLine Studio project is a **directory** containing these files:

| File | Format | Purpose | Required? |
|------|--------|---------|-----------| 
| `SquareLine_Project.spj` | JSON | Main project: widget tree, screens, events, animations | ✅ |
| `SquareLine_Project.sll` | JSON | Project metadata: resolution, board, LVGL version, paths | ✅ |
| `Themes.slt` | JSON | Theme definitions (colors, fonts per state) | ✅ |
| `project.info` | JSON | Editor metadata: user, timestamp, version (v1.6+) | ✅ (v1.6+) |
| `SquareLine_Project.slp` | JSON | Local user preferences: export paths, drive mappings | Optional |
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

## 3. `.sll` — Project Metadata [📖](https://docs.squareline.io/docs/squareline/project)

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
    "lvgl_version": "9.2.2",
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

## 4. `Themes.slt` — Theme Definitions [📖](https://docs.squareline.io/docs/squareline/themes)

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

---

## 6. InheritedType Enum

| IT | Data Type | Data Field | Examples |
|:---:|---|---|---|
| **1** | Section header | *(none)* | `OBJECT/Layout`, `OBJECT/Transform`, `OBJECT/Flags`, `SCREEN/Screen`, `LABEL/Label` |
| **2** | Boolean | `strval`: `"True"`/`"False"` | `OBJECT/Clickable`, `OBJECT/Hidden`, `LABEL/Recolor` |
| **3** | Enum/String constant | `strval` | `OBJECT/Align` → `"CENTER"`, `ARC/Mode` → `"NORMAL"` |
| **4** | Event handler (v1.5 only) | `childs`: event data | `_event/EventHandler` — replaced by IT=10 in v1.6+ |
| **5** | Asset path | `strval`: relative path | `IMAGE/Asset` → `"assets/foo.png"` |
| **6** | Integer | `integer` | `IMAGE/Scale` → `256`, `ARC/Value` → `50` |
| **7** | Integer array | `intarray` | `OBJECT/Position` → `[x, y]`, `_style/Bg_Color` → `[R, G, B, A]` |
| **8** | Animation reference | `strval`: name | `PLAY ANIMATION/Animation` → `"progress"` |
| **9** | Object reference (GUID) | `strval`: GUID or `"-"` | `CHANGE SCREEN/Screen_to`, `KEYBOARD/Target_textarea` |
| **10** | String | `strval` | `OBJECT/Name`, `LABEL/Text`, function names |
| **11** | Style container | `childs`: array | `BUTTON/Style_main`, `SCREEN/Style_scrollbar` |
| **12** | JSON-encoded string | `strval`: JSON string | `CHART/ChartData` — `"[{\"Axis\":0,\"Color\":[R,G,B,A],\"Series\":[...]}]"` |
| **13** | Layout type | `strval` + layout params | `OBJECT/Layout_type` → `"No_layout"` |
| **14** | Image set reference | `strval` | `PROPERTYANIMATION/ImageSet` |
| **15** | Child container ref | *(unknown)* | `TABVIEW/Children` |

### Layout_type extra fields (InheritedType 13)

The `strval` is always `"No_layout"` regardless of actual layout — the **real layout type is in the numeric `LayoutType` field**:

| `LayoutType` | Meaning |
|:---:|---|
| `0` | No layout |
| `1` | FLEX ✅ confirmed |
| `2` | GRID (assumed) |

Full property with FLEX enabled:
```json
{
  "Flow": 0,              // 0=ROW, 1=COLUMN (assumed)
  "Wrap": false,           // flex-wrap
  "Reversed": false,       // reverse direction
  "MainAlignment": 0,      // main-axis alignment (0=START, 1=CENTER, 2=END, 3=SPACE_EVENLY, etc.)
  "CrossAlignment": 0,     // cross-axis alignment
  "TrackAlignment": 0,     // multi-line track alignment
  "LayoutType": 1,         // ← this is the real layout selector
  "strval": "No_layout",   // ← misleading, always "No_layout"
  "InheritedType": 13
}
```

> [!WARNING]
> `strval` for Layout_type is always `"No_layout"` even when FLEX is active. The numeric `LayoutType` field is the source of truth.

### Size/Position flags

| `flags` value | Meaning |
|:---:|---|
| `17` | Fixed pixel sizing |
| `51` | Content-fit sizing (used on Labels) |
| `1048576` | Section header flag (on Flags, States, Scrolling sections) |

---

## 7. Universal Object Properties

Every widget has these (`OBJECT/` prefix):

| strtype | IT | Description |
|---------|:---:|---|
| `OBJECT/Name` | 10 | Widget name |
| `OBJECT/Layout` | 1 | Layout section header |
| `OBJECT/Layout_type` | 13 | `"No_layout"`, `"FLEX"`, `"GRID"` |
| `OBJECT/Transform` | 1 | Transform section header |
| `OBJECT/Position` | 7 | `[x, y]` with flags |
| `OBJECT/Size` | 7 | `[w, h]` with flags |
| `OBJECT/Align` | 3 | `"CENTER"`, `"TOP_LEFT"`, `"TOP_MID"`, `"TOP_RIGHT"`, `"BOTTOM_LEFT"`, etc. |
| `OBJECT/Extend_click_area` | 6 | Extended click area (v1.6+) |
| `OBJECT/Flags` | 1 | Flags section header |
| `OBJECT/Clickable` | 2 | Boolean |
| `OBJECT/Scrolling` | 1 | Scrolling section header (v1.6+) |
| `OBJECT/Scrollable` | 2 | Boolean |
| `OBJECT/Scroll_on_focus` | 2 | Boolean |
| `OBJECT/Scrollbar_mode` | 3 | `"AUTO"`, `"OFF"`, `"ON"`, `"ACTIVE"` |
| `OBJECT/Scroll_direction` | 3 | `"ALL"`, `"HOR"`, `"VER"`, `"NONE"` |
| `OBJECT/Scroll_snap_x` | 3 | `"NONE"`, `"START"`, `"END"`, `"CENTER"` (v1.6+) |
| `OBJECT/Scroll_snap_y` | 3 | `"NONE"`, `"START"`, `"END"`, `"CENTER"` (v1.6+) |
| `OBJECT/States` | 1 | States section header |
| `OBJECT/Hidden` | 2 | Boolean |
| `OBJECT/Adv_hittest` | 2 | Advanced hit testing |
| `OBJECT/Press_lock` | 2 | Press lock |

---

## 8. Complete Widget Catalog (24 Types) [📖](https://docs.squareline.io/docs/squareline/widgets)

All confirmed from `research/new01/` (v1.6.1) and SLS bundled examples.

> [!NOTE]
> CONTAINER is an LVGL 9.x alias for PANEL. COLORWHEEL was removed in LVGL 9.

### SCREEN [📖](https://docs.squareline.io/docs/squareline/widgets/screen)
| strtype | IT | Description |
|---------|:---:|---|
| `SCREEN/Screen` | 1 | Section header |
| `SCREEN/Temporary` | 2 | Temporary screen flag |
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

### PANEL [📖](https://docs.squareline.io/docs/squareline/widgets/panel)
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

### CONTAINER (LVGL 9.x) [📖](https://docs.squareline.io/docs/squareline/widgets/container)
| strtype | IT | Description |
|---------|:---:|---|
| `CONTAINER/Edited` | 2 | Edit flag |
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

> Functionally identical to PANEL. Uses standard `OBJECT/*` properties.
> Found heavily in SLS bundled examples (e.g., Coffee Machine: 218 instances).

### BUTTON [📖](https://docs.squareline.io/docs/squareline/widgets/button)
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN) |

### IMGBUTTON [📖](https://docs.squareline.io/docs/squareline/widgets/imgbutton)
| strtype | IT | Description |
|---------|:---:|---|
| `IMGBUTTON/Images` | 1 | Section header |
| `IMGBUTTON/Button_state` | 3 | `"RELEASED"` |
| `IMGBUTTON/Image_released` | 5 | Asset for released state |
| `IMGBUTTON/Image_pressed` | 5 | Asset for pressed state |
| `IMGBUTTON/Image_disabled` | 5 | Asset for disabled state |
| `IMGBUTTON/Image_checked_released` | 5 | Asset for checked+released |
| `IMGBUTTON/Image_checked_pressed` | 5 | Asset for checked+pressed |
| `IMGBUTTON/Image_checked_disabled` | 5 | Asset for checked+disabled |
| **Style parts:** | | `Style_main` (MAIN) |

### LABEL [📖](https://docs.squareline.io/docs/squareline/widgets/label)
| strtype | IT | Description |
|---------|:---:|---|
| `LABEL/Label` | 1 | Section header |
| `LABEL/Text` | 10 | Text content |
| `LABEL/Long_mode` | 3 | `"WRAP"`, `"SCROLL"`, `"DOT"`, `"CLIP"` |
| `LABEL/Recolor` | 2 | Enable recoloring syntax |
| **Style parts:** | | `Style_main` (MAIN) |

### IMAGE [📖](https://docs.squareline.io/docs/squareline/widgets/image)
| strtype | IT | Description |
|---------|:---:|---|
| `IMAGE/Image` | 1 | Section header |
| `IMAGE/Asset` | 5 | Asset path |
| `IMAGE/Pivot` | 7 | Rotation pivot `[x, y]` |
| `IMAGE/Rotation` | 6 | Rotation (0.1° units) |
| `IMAGE/Scale` | 6 | Scale (256 = 100%) |
| **Style parts:** | | `Style_main` (MAIN) |

### ARC [📖](https://docs.squareline.io/docs/squareline/widgets/arc)
| strtype | IT | Description |
|---------|:---:|---|
| `ARC/Arc` | 1 | Section header |
| `ARC/Value` | 6 | Current value |
| `ARC/Range` | 7 | `[min, max]` |
| `ARC/Bg_angles` | 7 | `[start_angle, end_angle]` |
| `ARC/Rotation` | 6 | Rotation offset |
| `ARC/Mode` | 3 | `"NORMAL"`, `"REVERSE"`, `"SYMMETRICAL"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### SLIDER [📖](https://docs.squareline.io/docs/squareline/widgets/slider)
| strtype | IT | Description |
|---------|:---:|---|
| `SLIDER/Slider` | 1 | Section header |
| `SLIDER/Value` | 6 | Current value |
| `SLIDER/Value_left` | 6 | Left value (range mode) |
| `SLIDER/Range` | 7 | `[min, max]` |
| `SLIDER/Mode` | 3 | `"NORMAL"`, `"SYMMETRICAL"`, `"RANGE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### BAR [📖](https://docs.squareline.io/docs/squareline/widgets/bar)
| strtype | IT | Description |
|---------|:---:|---|
| `BAR/Bar` | 1 | Section header |
| `BAR/Value` | 6 | Current value |
| `BAR/Value_start` | 6 | Start value (range mode) |
| `BAR/Range` | 7 | `[min, max]` |
| `BAR/Mode` | 3 | `"NORMAL"`, `"SYMMETRICAL"`, `"RANGE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR) |

### SWITCH [📖](https://docs.squareline.io/docs/squareline/widgets/switch)
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### CHECKBOX [📖](https://docs.squareline.io/docs/squareline/widgets/checkbox)
| strtype | IT | Description |
|---------|:---:|---|
| `CHECKBOX/Checkbox` | 1 | Section header |
| `CHECKBOX/Title` | 10 | Checkbox text label |
| **Style parts:** | | `Style_main` (MAIN), `Style_bullet` (INDICATOR) |

### DROPDOWN [📖](https://docs.squareline.io/docs/squareline/widgets/dropdown)
| strtype | IT | Description |
|---------|:---:|---|
| `DROPDOWN/Dropdown` | 1 | Section header |
| `DROPDOWN/Options` | 10 | Newline-separated options: `"Option 1\nOption 2\nOption 3"` |
| `DROPDOWN/Base_text` | 10 | Static text (overrides selected display) |
| `DROPDOWN/Show_selected` | 2 | Show selected option |
| `DROPDOWN/List_align` | 3 | `"BOTTOM"`, `"TOP"`, `"LEFT"`, `"RIGHT"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_list_main` (list MAIN), `Style_list_selected` (list SELECTED) |

### ROLLER [📖](https://docs.squareline.io/docs/squareline/widgets/roller)
| strtype | IT | Description |
|---------|:---:|---|
| `ROLLER/Roller` | 1 | Section header |
| `ROLLER/Options` | 10 | Newline-separated options |
| `ROLLER/Selected` | 6 | Selected index |
| `ROLLER/Mode` | 3 | `"NORMAL"`, `"INFINITE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_selected` (SELECTED) |

### TEXTAREA [📖](https://docs.squareline.io/docs/squareline/widgets/textarea)
| strtype | IT | Description |
|---------|:---:|---|
| `TEXTAREA/TextArea` | 1 | Section header |
| `TEXTAREA/Text` | 10 | Text content |
| `TEXTAREA/Placeholder` | 10 | Placeholder text |
| `TEXTAREA/Accepted_characters` | 10 | Character whitelist |
| `TEXTAREA/Max_text_length` | 6 | Max length (default 98989898) |
| `TEXTAREA/One_line_mode` | 2 | Single line mode |
| `TEXTAREA/Password_mode` | 2 | Password masking |
| **Style parts:** | | `Style_main` (MAIN), `Style_cursor` (CURSOR), `Style_placeholder` (PLACEHOLDER), `Style_selected` (SELECTED) |

### KEYBOARD [📖](https://docs.squareline.io/docs/squareline/widgets/keyboard)
| strtype | IT | Description |
|---------|:---:|---|
| `KEYBOARD/Mode` | 3 | `"TEXT_LOWER"`, `"TEXT_UPPER"`, `"SPECIAL"`, `"NUMBER"` |
| `KEYBOARD/Target_textarea` | 9 | GUID of linked textarea (or `"-"`) |
| **Style parts:** | | `Style_main` (MAIN), `Style_items` (ITEMS) |

### SPINNER [📖](https://docs.squareline.io/docs/squareline/widgets/spinner)
| strtype | IT | Description |
|---------|:---:|---|
| `SPINNER/Spinner` | 1 | Section header |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR) |

### SPINBOX [📖](https://docs.squareline.io/docs/squareline/widgets/spinbox)
| strtype | IT | Description |
|---------|:---:|---|
| `SPINBOX/Spinbox` | 1 | Section header |
| `SPINBOX/Value` | 6 | Current value |
| `SPINBOX/Range` | 7 | `[min, max, step]` (3 elements!) |
| `SPINBOX/Digit_format` | 7 | `[total_digits, decimal_digits]` |
| **Style parts:** | | `Style_main` (MAIN), `Style_cursor` (CURSOR) |

### CALENDAR [📖](https://docs.squareline.io/docs/squareline/widgets/calendar)
| strtype | IT | Description |
|---------|:---:|---|
| `CALENDAR/Date` | 7 | `[day, month, year]` |
| **Style parts:** | | `Style_main` (MAIN), `Style_items` (ITEMS) |

### CHART [📖](https://docs.squareline.io/docs/squareline/widgets/chart)
| strtype | IT | Description |
|---------|:---:|---|
| `CHART/Chart` | 1 | Section header |
| `CHART/Chart_type` | 3 | `"LINE"`, `"BAR"`, `"SCATTER"` |
| `CHART/Number_of_points` | 6 | Data point count |
| `CHART/Division_lines` | 7 | `[hor, ver]` |
| `CHART/Zoom` | 7 | `[x_zoom, y_zoom]` (256=100%) |
| `CHART/Primary_Y_range` | 7 | `[min, max]` |
| `CHART/Secondary_Y_range` | 7 | `[min, max]` |
| `CHART/ChartData` | 12 | JSON array of series objects |
| `CHART/Chart_data` | 1 | Section header for data |
| `CHART/Primary_Y_Axis` | 1 | Section header |
| `CHART/PrimaryYMajor` | 7 | `[count, length]` |
| `CHART/PrimaryYMinor` | 7 | `[count, length]` |
| `CHART/Labels_on_Primary_Y_axis` | 2 | Show labels |
| `CHART/Font_size_on_Primary_Y_axis` | 6 | Font size |
| `CHART/Secondary_Y_Axis` | 1 | Section header |
| `CHART/SecondaryYMajor` | 7 | `[count, length]` |
| `CHART/SecondaryYMinor` | 7 | `[count, length]` |
| `CHART/Labels_on_Secondary_Y_axis` | 2 | Show labels |
| `CHART/Font_size_on_Secondary_Y_axis` | 6 | Font size |
| `CHART/X_Axis` | 1 | Section header |
| `CHART/XMajor` | 7 | `[count, length]` |
| `CHART/XMinor` | 7 | `[count, length]` |
| `CHART/Labels_on_X_axis` | 2 | Show labels |
| `CHART/Font_size_on_X_axis` | 6 | Font size |
| **Style parts:** | | `Style_bg` (MAIN), `Style_indicator` (INDICATOR), `Style_items` (ITEMS), `Style_scrollbar` (SCROLLBAR), `Style_ticks` (TICKS) |

### COLORWHEEL
| strtype | IT | Description |
|---------|:---:|---|
| `COLORWHEEL/Mode` | 3 | `"HUE"`, `"SATURATION"`, `"VALUE"` |
| `COLORWHEEL/Fixed_mode` | 2 | Lock mode |
| **Style parts:** | | `Style_main` (MAIN), `Style_knob` (KNOB) |

### TABVIEW [📖](https://docs.squareline.io/docs/squareline/widgets/tabview)
| strtype | IT | Description |
|---------|:---:|---|
| `TABVIEW/Tabview` | 1 | Section header |
| `TABVIEW/Tab_position` | 3 | `"TOP"`, `"BOTTOM"`, `"LEFT"`, `"RIGHT"` |
| `TABVIEW/Tab_size` | 6 | Tab button height/width in px |
| `TABVIEW/Tabpages` | 1 | Section header |
| `TABVIEW/Children` | 15 | Child container reference |
| **Style parts:** | | `Style_main` (MAIN), `Style_buttons_main` (buttons MAIN), `Style_buttons_items` (buttons ITEMS) |

### TABPAGE (child of TABVIEW)
| strtype | IT | Description |
|---------|:---:|---|
| `TABPAGE/TabPage` | 1 | Section header |
| `TABPAGE/Title` | 10 | Tab title text |
| `TABPAGE/Name` | 10 | Widget name |
| **Note:** TABPAGE uses its own prefix for ALL properties (not OBJECT/) including Flags, States, Scrollable, etc. Full flag set: `Clickable`, `Click_focusable`, `Checkable`, `Checked`, `Disabled`, `Focused`, `Pressed`, `Hidden`, `Floating`, `Adv_hittest`, `Press_lock`, `Snappable`, `Event_bubble`, `Gesture_bubble`, `Scroll_elastic`, `Scroll_momentum`, `Scroll_one`, `Scroll_chain`, `Scroll_on_focus`, `Scroll_with_arrow`, `Ignore_layout`, `Overflow_visible`, `Flex_in_new_track`, `User_1..4` |
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

---

## 9. Events [📖](https://docs.squareline.io/docs/squareline/events)

### 9.1 Event Structure

Events are inline children of widget properties:

```json
{
  "disabled": false,
  "nid": 1000343,
  "strtype": "_event/EventHandler",
  "strval": "CLICKED",
  "InheritedType": 4,
  "childs": [
    { "strtype": "_custom/name", "strval": "Event1", "InheritedType": 10 },
    { "strtype": "_custom/condition_C", "strval": "", "InheritedType": 10 },
    { "strtype": "_custom/condition_P", "strval": "", "InheritedType": 10 },
    {
      "strtype": "_event/action",
      "strval": "CHANGE SCREEN",
      "InheritedType": 10,
      "childs": [ /* action parameters */ ]
    }
  ]
}
```

### 9.2 Event Trigger Types [📖](https://docs.squareline.io/docs/squareline/events/events)

| Trigger | Description | Confirmed |
|---------|-------------|:---:|
| `CLICKED` | Short press and release | ✅ |
| `PRESSED` | Immediately on press | ✅ |
| `RELEASED` | On release | ✅ |
| `PRESS_LOST` | Press followed by pointer leaving widget | ✅ |
| `LONG_PRESSED` | After long press threshold | LVGL |
| `LONG_PRESSED_REPEAT` | Repeated after long press | LVGL |
| `SHORT_CLICKED` | Short click detected | LVGL |
| `VALUE_CHANGED` | Widget value changed | ✅ |
| `CHECKED(VALUE_CHANGED)` | Checkbox/switch set to checked | ✅ |
| `UNCHECKED(VALUE_CHANGED)` | Checkbox/switch set to unchecked | ✅ |
| `SCREEN_LOADED` | Screen fully loaded | ✅ |
| `SCREEN_UNLOADED` | Screen fully unloaded | ✅ |
| `SCREEN_LOAD_START` | Screen load begins | ✅ |
| `SCREEN_UNLOAD_START` | Screen unload begins | ✅ |
| `GESTURE_LEFT(GESTURE)` | Left swipe gesture | ✅ |
| `GESTURE_RIGHT(GESTURE)` | Right swipe gesture | ✅ |
| `GESTURE_UP(GESTURE)` | Up swipe gesture | ✅ |
| `GESTURE_DOWN(GESTURE)` | Down swipe gesture | ✅ |
| `FOCUSED` | Widget gains focus | LVGL |
| `DEFOCUSED` | Widget loses focus | LVGL |
| `READY` | Process completed | LVGL |
| `CANCEL` | Process cancelled | LVGL |
| `KEY` | Key input received | elojb |
| `KEY_RIGHT(KEY)` | Right key pressed | elojb |
| `KEY_LEFT(KEY)` | Left key pressed | elojb |
| `KEY_UP(KEY)` | Up key pressed | elojb |
| `KEY_DOWN(KEY)` | Down key pressed | elojb |
| `KEY_NEXT(KEY)` | Next key (tab) | elojb |
| `KEY_PREV(KEY)` | Previous key (shift+tab) | elojb |
| `KEY_ENTER(KEY)` | Enter key pressed | elojb |
| `KEY_ESC(KEY)` | Escape key pressed | elojb |
| `EDITED` | Text content modified | elojb |
| `INSERT` | Text inserted | elojb |

> [!NOTE]
> ✅ = confirmed in SLS example projects. elojb = confirmed from decoded `.elojb` descriptors.
> Compound triggers like `CHECKED(VALUE_CHANGED)` and `KEY_RIGHT(KEY)` use SLS-specific
> naming. The parenthesized suffix indicates the underlying LVGL event type.

### 9.3 Event Action Types [📖](https://docs.squareline.io/docs/squareline/events/actions)

#### CHANGE SCREEN ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "CHANGE SCREEN",
  "childs": [
    { "strtype": "CHANGE SCREEN/Name", "strval": "CHANGE SCREEN" },
    { "strtype": "CHANGE SCREEN/Call", "strval": "ChangeScreen( <{Screen_to}>, lv.SCR_LOAD_ANIM.<{Fade_mode}>, <{Speed}>, <{Delay}>)" },
    { "strtype": "CHANGE SCREEN/CallC", "strval": "_ui_screen_change( &<{Screen_to}>, LV_SCR_LOAD_ANIM_<{Fade_mode}>, <{Speed}>, <{Delay}>, &<{Screen_to}>_screen_init);" },
    { "strtype": "CHANGE SCREEN/Screen_to", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "CHANGE SCREEN/Fade_mode", "strval": "MOVE_LEFT", "InheritedType": 3 },
    { "strtype": "CHANGE SCREEN/Speed", "strval": "500", "InheritedType": 6 },
    { "strtype": "CHANGE SCREEN/Delay", "InheritedType": 6 }
  ]
}
```

#### CALL FUNCTION ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "CALL FUNCTION",
  "childs": [
    { "strtype": "CALL FUNCTION/Name", "strval": "CALL FUNCTION" },
    { "strtype": "CALL FUNCTION/Call", "strval": "<{Function_name}>( event_struct )" },
    { "strtype": "CALL FUNCTION/CallC", "strval": "<{Function_name}>( e );" },
    { "strtype": "CALL FUNCTION/Function_name", "strval": "on_slide_changed", "InheritedType": 10 },
    { "strtype": "CALL FUNCTION/Dont_export_function", "strval": "False", "InheritedType": 2 }
  ]
}
```

#### PLAY ANIMATION ✅ confirmed (v1.5 project)
```json
{
  "strtype": "_event/action", "strval": "PLAY ANIMATION",
  "childs": [
    { "strtype": "PLAY ANIMATION/Name", "strval": "PLAY ANIMATION" },
    { "strtype": "PLAY ANIMATION/Call", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>)" },
    { "strtype": "PLAY ANIMATION/CallC", "strval": "<{FunctionName}>(<{Target}>, <{Delay}>);" },
    { "strtype": "PLAY ANIMATION/FunctionName", "strval": "progress_Animation" },
    { "strtype": "PLAY ANIMATION/Animation", "strval": "progress", "InheritedType": 8 },
    { "strtype": "PLAY ANIMATION/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "PLAY ANIMATION/Delay", "InheritedType": 6 }
  ]
}
```

#### LABEL_PROPERTY (Set Label Text) ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "LABEL_PROPERTY",
  "childs": [
    { "strtype": "LABEL_PROPERTY/Name", "strval": "LABEL_PROPERTY", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Call", "strval": "SetLabelProperty(<{Target}>, '<{Property}>', '<{Value}>')", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/CallC", "strval": "_ui_label_set_property(<{Target}>, _UI_LABEL_PROPERTY_<{Property}>, \"<{Value}>\");", "InheritedType": 10 },
    { "strtype": "LABEL_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "LABEL_PROPERTY/Property", "strval": "Text", "InheritedType": 3 },
    { "strtype": "LABEL_PROPERTY/Value", "strval": "Test", "InheritedType": 10 }
  ]
}
```

#### INCREMENT ARC ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT ARC",
  "childs": [
    { "strtype": "INCREMENT ARC/Name", "strval": "INCREMENT ARC", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/Call", "strval": "IncrementArc( <{Target}>, <{Value}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/CallC", "strval": "_ui_arc_increment( <{Target}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT ARC/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT ARC/Value", "integer": 30, "InheritedType": 6 }
  ]
}
```

#### INCREMENT BAR — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT BAR",
  "childs": [
    { "strtype": "INCREMENT BAR/Name", "strval": "INCREMENT BAR", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/Call", "strval": "IncrementBar( <{Target}>, <{Value}>, LV_ANIM_<{Animate}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/CallC", "strval": "_ui_bar_increment( <{Target}>, <{Value}>, LV_ANIM_<{Animate}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT BAR/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT BAR/Value", "integer": 1, "InheritedType": 6 },
    { "strtype": "INCREMENT BAR/Animate", "strval": "ON", "InheritedType": 3 }
  ]
}
```
Animate choices: `ON`, `OFF`

> [!NOTE]
> INCREMENT BAR and INCREMENT SLIDER have an `Animate` parameter that INCREMENT ARC does not.
> This controls whether the value change is animated (`LV_ANIM_ON`) or instant (`LV_ANIM_OFF`).

#### INCREMENT SLIDER — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "INCREMENT SLIDER",
  "childs": [
    { "strtype": "INCREMENT SLIDER/Name", "strval": "INCREMENT SLIDER", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/Call", "strval": "IncrementSlider( <{Target}>, <{Value}>, LV_ANIM_<{Animate}> )", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/CallC", "strval": "_ui_slider_increment( <{Target}>, <{Value}>, LV_ANIM_<{Animate}>);", "InheritedType": 10 },
    { "strtype": "INCREMENT SLIDER/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "INCREMENT SLIDER/Value", "integer": 1, "InheritedType": 6 },
    { "strtype": "INCREMENT SLIDER/Animate", "strval": "ON", "InheritedType": 3 }
  ]
}
```
Animate choices: `ON`, `OFF`

#### DELETE SCREEN — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "DELETE SCREEN",
  "childs": [
    { "strtype": "DELETE SCREEN/Name", "strval": "DELETE SCREEN" },
    { "strtype": "DELETE SCREEN/Call", "strval": "DeleteScreen(<{Screen}>)" },
    { "strtype": "DELETE SCREEN/CallC", "strval": "_ui_screen_delete( &<{Screen}>_screen_destroy);" },
    { "strtype": "DELETE SCREEN/Screen", "strval": "GUID...", "InheritedType": 9 }
  ]
}
```

#### MODIFY FLAG ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "MODIFY FLAG",
  "childs": [
    { "strtype": "MODIFY FLAG/Name", "strval": "MODIFY FLAG", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/Call", "strval": "ModifyFlag( <{Object}>, lv.obj.FLAG.<{Flag}>, \"<{Action}>\")", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/CallC", "strval": "_ui_flag_modify( <{Object}>, LV_OBJ_FLAG_<{Flag}>, _UI_MODIFY_FLAG_<{Action}>);", "InheritedType": 10 },
    { "strtype": "MODIFY FLAG/Object", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MODIFY FLAG/Flag", "strval": "HIDDEN", "InheritedType": 3 },
    { "strtype": "MODIFY FLAG/Action", "strval": "ADD", "InheritedType": 3 }
  ]
}
```
Flag choices: `HIDDEN`, `CLICKABLE`, `CHECKABLE`, `PRESS_LOCK`, `CLICK_FOCUSABLE`, `ADV_HITTEST`, `IGNORE_LAYOUT`, `FLOATING`, `EVENT_BUBBLE`, `GESTURE_BUBBLE`, `SNAPPABLE`, `SCROLLABLE`, `SCROLL_ELASTIC`, `SCROLL_MOMENTUM`, `SCROLL_ON_FOCUS`, `SCROLL_CHAIN`, `SCROLL_ONE`

Action choices: `ADD`, `REMOVE`, `TOGGLE`

#### MODIFY STATE ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "MODIFY STATE",
  "childs": [
    { "strtype": "MODIFY STATE/Name", "strval": "MODIFY STATE", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/Call", "strval": "ModifyState( <{Object}>, lv.STATE.<{State}>, \"<{Action}>\")", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/CallC", "strval": "_ui_state_modify( <{Object}>, LV_STATE_<{State}>, _UI_MODIFY_STATE_<{Action}>);", "InheritedType": 10 },
    { "strtype": "MODIFY STATE/Object", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MODIFY STATE/State", "strval": "CHECKED", "InheritedType": 3 },
    { "strtype": "MODIFY STATE/Action", "strval": "ADD", "InheritedType": 3 }
  ]
}
```
State choices: `CHECKED`, `DISABLED`, `PRESSED`, `FOCUSED`, `USER_1`, `USER_2`, `USER_3`, `USER_4`

Action choices: `ADD`, `REMOVE`, `TOGGLE`

#### SET OPACITY ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "SET OPACITY",
  "childs": [
    { "strtype": "SET OPACITY/Name", "strval": "SET OPACITY", "InheritedType": 10 },
    { "strtype": "SET OPACITY/Call", "strval": "set_opacity( <{Target}>, <{Value}>)", "InheritedType": 10 },
    { "strtype": "SET OPACITY/CallC", "strval": "_ui_opacity_set( <{Target}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "SET OPACITY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET OPACITY/Value", "strval": "100", "InheritedType": 6 }
  ]
}
```

#### SLIDER_PROPERTY ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "SLIDER_PROPERTY",
  "childs": [
    { "strtype": "SLIDER_PROPERTY/Name", "strval": "SLIDER_PROPERTY", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/Call", "strval": "SetSliderProperty(<{Target}>, '<{Property}>', <{Value}>)", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/CallC", "strval": "_ui_slider_set_property(<{Target}>, _UI_SLIDER_PROPERTY_<{Property}>, <{Value}>);", "InheritedType": 10 },
    { "strtype": "SLIDER_PROPERTY/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SLIDER_PROPERTY/Property", "strval": "Value_with_anim", "InheritedType": 3 },
    { "strtype": "SLIDER_PROPERTY/Value", "strval": "", "InheritedType": 10 }
  ]
}
```
Property choices: `Value_with_anim`, `Value`

#### KEYBOARD SET TARGET — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "KEYBOARD SET TARGET",
  "childs": [
    { "strtype": "KEYBOARD SET TARGET/Name", "strval": "KEYBOARD SET TARGET", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/Call", "strval": "KeyboardSetTarget( <{Keyboard}>,  <{TextArea}>)", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/CallC", "strval": "_ui_keyboard_set_target(<{Keyboard}>,  <{TextArea}>);", "InheritedType": 10 },
    { "strtype": "KEYBOARD SET TARGET/Keyboard", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "KEYBOARD SET TARGET/TextArea", "strval": "GUID...", "InheritedType": 9 }
  ]
}
```

#### MOVE CURSOR — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "MOVE CURSOR",
  "childs": [
    { "strtype": "MOVE CURSOR/Name", "strval": "MOVE CURSOR", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/Call", "strval": "TextAreaMoveCursor( <{Target}>, \"<{Direction}>\" )", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/CallC", "strval": "_ui_textarea_move_cursor( <{Target}>, UI_MOVE_CURSOR_<{Direction}>);", "InheritedType": 10 },
    { "strtype": "MOVE CURSOR/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "MOVE CURSOR/Direction", "strval": "RIGHT", "InheritedType": 3 }
  ]
}
```
Direction choices: `UP`, `RIGHT`, `DOWN`, `LEFT`

#### STEP SPINBOX — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "STEP SPINBOX",
  "childs": [
    { "strtype": "STEP SPINBOX/Name", "strval": "STEP SPINBOX", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/Call", "strval": "StepSpinbox( <{Target}>, <{Direction}> )", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/CallC", "strval": "_ui_spinbox_step( <{Target}>, <{Direction}>);", "InheritedType": 10 },
    { "strtype": "STEP SPINBOX/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "STEP SPINBOX/Direction", "strval": "1", "InheritedType": 3 }
  ]
}
```
Direction choices: `1(INCREMENT)`, `-1(DECREMENT)`

#### SWITCH THEME — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "SWITCH THEME",
  "childs": [
    { "strtype": "SWITCH THEME/Name", "strval": "SWITCH THEME", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/Call", "strval": "SwitchTheme( <{Theme}> )", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/CallC", "strval": "_ui_switch_theme( <{Theme}> );", "InheritedType": 10 },
    { "strtype": "SWITCH THEME/Theme", "strval": "", "InheritedType": 10 }
  ]
}
```

#### SET TEXT VALUE FROM ARC ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE FROM ARC",
  "childs": [
    { "strtype": "SET TEXT VALUE FROM ARC/Name", "strval": "SET TEXT VALUE FROM ARC", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Call", "strval": "SetTextValueArc( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/CallC", "strval": "_ui_arc_set_text_value( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE FROM ARC/Prefix", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM ARC/Postfix", "strval": "", "InheritedType": 10 }
  ]
}
```

> [!NOTE]
> The `target` in the Call/CallC template refers to the **event source widget** (the arc/slider/switch
> that triggered the event), not a separate parameter. `Target` is the label to update.

#### SET TEXT VALUE FROM SLIDER ✅ confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE FROM SLIDER",
  "childs": [
    { "strtype": "SET TEXT VALUE FROM SLIDER/Name", "strval": "SET TEXT VALUE FROM SLIDER", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Call", "strval": "SetTextValueSlider( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/CallC", "strval": "_ui_slider_set_text_value( <{Target}>, target, \"<{Prefix}>\", \"<{Postfix}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Prefix", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE FROM SLIDER/Postfix", "strval": "", "InheritedType": 10 }
  ]
}
```

#### SET TEXT VALUE WHEN CHECKED — elojb confirmed
```json
{
  "strtype": "_event/action", "strval": "SET TEXT VALUE WHEN CHECKED",
  "childs": [
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Name", "strval": "SET TEXT VALUE WHEN CHECKED", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Call", "strval": "SetTextValueChecked( <{Target}>, target, \"<{On_text}>\", \"<{Off_text}>\")", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/CallC", "strval": "_ui_checked_set_text_value( <{Target}>, target, \"<{On_text}>\", \"<{Off_text}>\");", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Target", "strval": "GUID...", "InheritedType": 9 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/On_text", "strval": "", "InheritedType": 10 },
    { "strtype": "SET TEXT VALUE WHEN CHECKED/Off_text", "strval": "", "InheritedType": 10 }
  ]
}
```

#### Property-Setting Actions

These follow the same pattern as LABEL_PROPERTY but for other widget types:

| Action | Widget | Sets |
|--------|--------|------|
| `BAR_PROPERTY` | BAR | Value |
| `BASIC_PROPERTY` | Any | Generic property |
| `DROPDOWN_PROPERTY` | DROPDOWN | Selected index, Options |
| `IMAGE_PROPERTY` | IMAGE | Asset, Rotation, Scale |
| `LABEL_PROPERTY` | LABEL | Text ✅ confirmed |
| `ROLLER_PROPERTY` | ROLLER | Selected index |
| `SLIDER_PROPERTY` | SLIDER | Value |

#### Complete Action Summary (24 user-facing actions)

| Category | Actions | Confirmed |
|----------|--------|:---:|
| Navigation | CHANGE SCREEN, DELETE SCREEN | ✅, — |
| Code | CALL FUNCTION | ✅ |
| Animation | PLAY ANIMATION, SET OPACITY | ✅, ✅ |
| Value Increment | INCREMENT ARC, INCREMENT BAR, INCREMENT SLIDER | ✅, —, — |
| Property Setting | LABEL_PROPERTY, SLIDER_PROPERTY, BAR_PROPERTY, DROPDOWN_PROPERTY, IMAGE_PROPERTY, ROLLER_PROPERTY, BASIC_PROPERTY | ✅, ✅, — |
| Text Display | SET TEXT VALUE FROM ARC, SET TEXT VALUE FROM SLIDER, SET TEXT VALUE WHEN CHECKED | ✅, ✅, ✅ |
| State/Flag | MODIFY FLAG, MODIFY STATE | ✅, ✅ |
| Keyboard | KEYBOARD SET TARGET, MOVE CURSOR | —, — |
| Other | STEP SPINBOX, SWITCH THEME | —, — |

### 9.4 Screen Transition Fade Modes

| Mode | Description |
|------|-------------|
| `NONE` | Instant switch |
| `FADE_ON` | New screen fades in ✅ confirmed |
| `FADE_OUT` | Current screen fades out |
| `MOVE_LEFT` | Both screens push left ✅ confirmed |
| `MOVE_RIGHT` | Both screens push right ✅ confirmed |
| `MOVE_TOP` | Both screens push up |
| `MOVE_BOTTOM` | Both screens push down |
| `OVER_LEFT` | New screen slides over from left |
| `OVER_RIGHT` | New screen slides over from right |
| `OVER_TOP` | New screen slides over from top |
| `OVER_BOTTOM` | New screen slides over from bottom |
| `OUT_LEFT` | Current screen slides out to left |
| `OUT_RIGHT` | Current screen slides out to right |
| `OUT_TOP` | Current screen slides out to top |
| `OUT_BOTTOM` | Current screen slides out to bottom |

---

## 10. Style States [📖](https://docs.squareline.io/docs/squareline/styles)

Styles are nested inside `Style_*` properties. Multiple states can coexist.

### 10.0 Confirmed Widget Style Parts

All confirmed from `new01` with style sections added to each widget.

> [!NOTE]
> All style parts accept the same 31 style properties (Section 10.4). However, SLS may show a
> **reduced subset** in the UI for non-MAIN parts — e.g., knob parts may not expose Text or
> Transform properties. When generating programmatically, any property can be set on any part
> and LVGL will apply it if relevant to the widget's drawing logic.

#### Style Part → Visual Mapping

| SLS Part Name | LVGL Part | What it controls |
|---|---|---|
| `Style_main` | `LV_PART_MAIN` | Widget background, border, outline, shadow, padding, text |
| `Style_indicator` | `LV_PART_INDICATOR` | Filled/active portion (slider track fill, arc progress) |
| `Style_knob` | `LV_PART_KNOB` | Draggable handle (slider handle, arc handle). Padding resizes it |
| `Style_items` | `LV_PART_ITEMS` | Repeated sub-elements (keyboard keys, chart series) |
| `Style_selected` | `LV_PART_SELECTED` | Currently selected item (roller highlight, textarea selection) |
| `Style_cursor` | `LV_PART_CURSOR` | Insertion cursor (textarea blinker) |
| `Style_bullet` | `LV_PART_INDICATOR` | Checkbox tick box (same LVGL part, SLS-specific name) |
| `Style_scrollbar` | `LV_PART_SCROLLBAR` | Scrollbar track/thumb |
| `Style_bg` | `LV_PART_MAIN` | Chart background (SLS-specific alias) |
| `Style_ticks` | `LV_PART_TICKS` | Chart axis tick marks and labels |

#### Per-Widget Style Parts

| Widget | Parts | Notes |
|--------|-------|-------|
| SCREEN | `main` | Background only |
| PANEL | `main`, `scrollbar` | Main has full 31 properties |
| BUTTON | `main` | Bg, border, shadow, padding |
| LABEL | `main` | Text color, font, decoration |
| IMAGE | `main` | Recolor, opacity, transform |
| SLIDER | `main`, `indicator`, `knob` | main=track bg, indicator=fill, knob=handle |
| ARC | `main`, `indicator`, `knob` | main=bg arc, indicator=value arc, knob=handle |
| BAR | `main`, `indicator` | Like slider without knob |
| SWITCH | `main`, `indicator`, `knob` | main=track, indicator=on-state, knob=toggle |
| CHECKBOX | `main`, `bullet` | main=text area, bullet=the tick box |
| DROPDOWN | `main`, `list_main`, `list_selected`, `list_scrollbar` | main=button, list_main=list bg, list_selected=highlighted option, list_scrollbar=scrollbar |
| ROLLER | `main`, `selected` | main=list bg, selected=highlighted row |
| TEXTAREA | `main`, `selected`, `cursor` | main=bg, selected=highlight, cursor=blinker |
| KEYBOARD | `main`, `items` | main=bg, items=individual keys |
| CHART | `bg`, `scrollbar`, `indicator`, `ticks` | bg=chart area, ticks=axis labels |
| SPINNER | `main`, `indicator` | main=bg track, indicator=spinning arc |
| TABVIEW | `main` | Tab bar container |
| TABPAGE | `main` | Individual tab content area |

### 10.1 Style State Structure ✅ confirmed

```json
{
  "strtype": "PANEL/Style_main",
  "childs": [
    {
      "strtype": "_style/StyleState",
      "strval": "DEFAULT",
      "InheritedType": 10,
      "childs": [
        { "strtype": "_style/Bg_Color", "flags": 4096, "intarray": [255, 0, 0, 255], "InheritedType": 7 }
      ]
    }
  ]
}
```

Multiple states can coexist — e.g., Checkbox with DEFAULT and CHECKED states:

```json
{
  "strtype": "CHECKBOX/Style_bullet",
  "childs": [
    {
      "strtype": "_style/StyleState", "strval": "DEFAULT",
      "childs": [
        { "strtype": "_style/Bg_Color", "flags": 4096, "intarray": [255, 255, 255, 255], "InheritedType": 7 }
      ]
    },
    {
      "strtype": "_style/StyleState", "strval": "CHECKED",
      "childs": [
        { "strtype": "_style/Bg_Color", "flags": 4096, "intarray": [255, 0, 0, 255], "InheritedType": 7 }
      ]
    }
  ]
}
```

### 10.2 Style States
`DEFAULT`, `PRESSED`, `CHECKED`, `FOCUSED`, `DISABLED`, `CHECKED|PRESSED`, etc.

### 10.3 The `flags` Field on IT=7 Properties ✅ confirmed

IT=7 properties use `intarray` instead of `strval`. The `flags` field indicates the array format:

| flags | intarray len | Format | Examples |
|:-----:|:---:|--------|----------|
| `4096` | 4 | `[R, G, B, A]` (RGBA color) | Bg_Color, Border_Color, Text_Color, Shadow_Color |
| `256` | 3 | `[R, G, B]` (RGB, no alpha) | Bg_gradiens_Color |
| `16` | 2 | `[val1, val2]` (parameter pair) | Padding_RowCol, Outline_params, Shadow_offset, Text_Spacing |

Other flags values (on non-style properties):
| `17` | 2 | Position/Size with default flags |
| `19` | 2 | Size with content-fit |
| `51` | 2 | Size with content-fit both axes |

### 10.4 Style Properties (Complete Catalog — 31 properties)

All confirmed from Panel1 with every attribute set.

#### Background
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Bg_Color` | 7 | `[R, G, B, A]` | Background color (0–255) |
| `_style/Bg_Radius` | 6 | Integer | Corner radius (px) |
| `_style/Bg_gradiens_Color` | 7 | `[R, G, B]` | Gradient end color (note: no alpha, typo in key name is real) |
| `_style/Bg_gradient_params` | 7 | `[start_opa, end_opa]` | Gradient opacity range |
| `_style/Gradient direction` | 3 | `"HOR"`, `"VER"` | Gradient direction (note: space in key name is real) |
| `_style/Clip_corner` | 2 | `"True"`/`"False"` | Clip content to rounded corners |
| `_style/Bg_Image` | 5 | Asset path | Background image |
| `_style/Bg_Image_opa` | 6 | 0–255 | Background image opacity |
| `_style/Bg_Image_Recolor` | 7 | `[R, G, B, A]` | Background image recolor tint |
| `_style/Bg_Image_Tiled` | 2 | `"True"`/`"False"` | Tile background image |

#### Border
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Border_Color` | 7 | `[R, G, B, A]` | Border color |
| `_style/Border width` | 6 | Integer (px) | Border width (space in key is real) |
| `_style/Border side` | 3 | `"FULL"`, `"BOTTOM"`, `"TOP"`, `"LEFT"`, `"RIGHT"`, `"NONE"` | Which sides get border |

#### Outline
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Outline_Color` | 7 | `[R, G, B, A]` | Outline color |
| `_style/Outline_params` | 7 | `[width, offset]` | Outline width and offset from edge |

#### Shadow
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Shadow_Color` | 7 | `[R, G, B, A]` | Shadow color |
| `_style/Shadow_params` | 7 | `[width, spread]` | Shadow blur width and spread |
| `_style/Shadow_offset` | 7 | `[x, y]` | Shadow offset |

#### Blending
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Blend mode` | 3 | `"NORMAL"`, `"ADDITIVE"`, `"SUBTRACTIVE"` | Blend mode (space in key is real) |
| `_style/Blend_opacity` | 6 | 0–255 | Overall opacity |

#### Padding
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Padding` | 7 | `[top, bottom, left, right]` | Content padding |
| `_style/Padding_RowCol` | 7 | `[row, column]` | Padding between flex/grid items |

#### Text
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Text_Color` | 7 | `[R, G, B, A]` | Text color |
| `_style/Text_Font` | 3 | Font name | e.g., `"montserrat_14"`, `"montserrat_10"` |
| `_style/Text_Align` | 3 | `"AUTO"`, `"CENTER"`, `"LEFT"`, `"RIGHT"` | Text alignment |
| `_style/Text_Spacing` | 7 | `[letter_spacing, line_spacing]` | Character and line spacing |
| `_style/Text_Decor` | 3 | `"NONE"`, `"UNDERLINE"`, `"STRIKETHROUGH"` | Text decoration |

#### Transform
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Transform_width` | 7 | `[value, max]` | Width transform |
| `_style/Transform_height` | 7 | `[value, max]` | Height transform |
| `_style/Transform_rotation` | 6 | Integer | Rotation (0.1° units) |
| `_style/Transform_scale` | 6 | Integer | Scale (256 = 100%) |
| `_style/Transform_pivot` | 7 | `[x, y]` | Transform pivot point |

#### Arc-specific (on ARC widget style parts)
| strtype | IT | Data | Description |
|---------|:---:|------|---|
| `_style/Arc_Image` | strval | Asset path | Arc track image |
| `_style/Arc_Rounded` | strval | `"True"`/`"False"` | Arc end caps |
| `_style/Arc_Width` | 6 | Integer | Arc track width (px) |

> [!WARNING]
> Several style property key names have inconsistent formatting — some use spaces (`"Border width"`, `"Blend mode"`, `"Gradient direction"`, `"Border side"`), others use underscores. One has a typo (`"Bg_gradiens_Color"` — note the 's'). These are the **actual key names** stored in the file; a generator must use them exactly as-is.

---

## 11. Animations (v1.5 project data) [📖](https://docs.squareline.io/docs/squareline/animations)

### PROPERTYANIMATION

| strtype | IT | Description |
|---------|:---:|---|
| `PROPERTYANIMATION/Name` | 10 | Display name |
| `PROPERTYANIMATION/VariableName` | 10 | Code variable name |
| `PROPERTYANIMATION/PropertyFunction` | 10 | Setter callback |
| `PROPERTYANIMATION/PropertyGetter` | 10 | Getter callback |
| `PROPERTYANIMATION/StartValue` | 6 | Start value |
| `PROPERTYANIMATION/EndValue` | 6 | End value |
| `PROPERTYANIMATION/Duration` | 6 | Duration (ms) |
| `PROPERTYANIMATION/Delay` | 6 | Start delay (ms) |
| `PROPERTYANIMATION/Path` | 3 | `"LINEAR"`, `"EASE_IN"`, `"EASE_OUT"`, `"EASE_IN_OUT"`, `"OVERSHOOT"`, `"BOUNCE"` |
| `PROPERTYANIMATION/LoopCount` | 6 | Loops (0=infinite) |
| `PROPERTYANIMATION/LoopInfinite` | 2 | Infinite loop flag |
| `PROPERTYANIMATION/LoopDelay` | 6 | Delay between loops |
| `PROPERTYANIMATION/PlaybackTime` | 6 | Reverse playback time |
| `PROPERTYANIMATION/PlaybackDelay` | 6 | Reverse delay |

### ELOANIMATION

Timeline wrapper for property animations:

| strtype | Description |
|---------|---|
| `ELOANIMATION/Name` | Animation name |
| `ELOANIMATION/FunctionName` | Generated function name |
| `ELOANIMATION/PlayType` | Play mode |
| `ELOANIMATION/Loop` | Loop setting |
| `ELOANIMATION/TestTarget` | Test target GUID |
| `ELOANIMATION/AnimationTargetObjectType` | `"BASIC"` |

---

## 12. Components (`.ecomp`) [📖](https://docs.squareline.io/docs/squareline/components)

Same JSON structure as a widget in `.spj`. Represents reusable widget templates.

---

## 13. `.slp` — Local Preferences

JSON file storing user-specific project preferences (not required for project generation):

```json
{
  "uiExportFolderPath": "",
  "projectExportFolderPath": "",
  "drive_stdio": "-",
  "drive_stdio_path": "",
  "drive_posix": "-",
  "drive_posix_path": "",
  "drive_win32": "-",
  "drive_win32_path": "",
  "drive_fatfs": "-",
  "drive_fatfs_path": ""
}
```

---

## 14. SLS Installation Structure

Useful paths inside the SquareLine Studio installation:

| Path | Contents |
|------|----------|
| `~/SquareLine/boards/<Group>/<board>/` | Downloaded board `.slb` definitions (JSON) |
| `<app>/Contents/boards/` | Bundled board definitions |
| `<app>/Contents/examples/` | 15 example projects (full `.spj`/`.sll`/`.slt`) |
| `<app>/Contents/lvgl/lvgl_v*/objects/` | Internal widget definitions |
| `<app>/Contents/lvgl/lvgl_v*/objects/functions/` | Internal event action definitions |
| `<app>/Contents/lvgl/extensions/` | Theme manager C/Python templates |
| `<app>/Contents/codeformat_c.cfg` | astyle config for generated C code |

### Bundled Example Projects

| Example | Resolution | Shape | Widgets | Events | Animations |
|---------|:----------:|:-----:|:-------:|:------:|:----------:|
| Caffee_Machnine_800x480 | 800×480 | RECT | 504 | 78 | 32 |
| SmartWatch_392x392 | 392×392 | CIRCLE | 290 | 47 | 12 |
| 3d_Printer_2_1024x600 | 1024×600 | RECT | 281 | 28 | 11 |
| EV_Charger_800x480 | 640×400 | RECT | 268 | 34 | 19 |
| Futuristic_Ebike_800x480 | 800×480 | RECT | 198 | 31 | 10 |
| Smart_Gadget_240x320 | 240×320 | RECT | 130 | 21 | 5 |
| POS_272x480 | 270×480 | RECT | 73 | 16 | 9 |
| Medical_272x480 | 272×480 | RECT | 73 | 6 | 3 |
| Thermostat_480x800 | 480×800 | RECT | 13 | 2 | 0 |

> These are located at `/Applications/SquareLine_Studio.app/Contents/examples/`
> and can be opened in SLS or parsed programmatically for reference patterns.

---

## 15. Remaining Gaps

| Gap | Priority | How to Fill |
|-----|----------|-------------|
| ~~New action Call/CallC templates~~ | ~~Medium~~ | Resolved — all 24 actions have full JSON blocks from decoded `.elojb` descriptors |
| GRID layout params | Low | Set a Panel to GRID layout in SLS, save, compare |
| Theme file with actual overrides | Low | Customise a theme in SLS, save |
| Multi-state style combos | Low | e.g., `"CHECKED|PRESSED"` compound states |
| ~~LVGL 9.x property differences~~ | ~~Low~~ | Addressed in `references/format/lvgl-version-guide.md` |

---

## 16. UX Design Guidelines

The skill includes advisory UX best-practice guidelines under `references/ux/`:

| Reference | Contents |
|-----------|----------|
| `design-guidelines.md` | Touch targets, typography, colour, contrast, layout principles, feedback states. Adapted from Material Design and iOS HIG. |
| `round-display-patterns.md` | Safe zone calculation, 7 layout patterns for circular displays (gauge, radial menu, value+controls, dashboard, indicator, list, clock) |
| `rectangular-display-patterns.md` | 8 layout patterns for rectangular displays (tab bar, dashboard grid, master-detail, cards, hero+controls, toolbar, form, carousel) |
| `screen-flow-patterns.md` | Navigation models (hub-and-spoke, tab, carousel, hierarchical, modal, wizard), transition best practices, rotary encoder navigation |
| `widget-recipes.md` | 10 ready-made widget compositions (thermostat, toggle row, sensor dashboard, nav bar, settings list, alert dialog, splash screen, chart view, input form, clock display) |

These guidelines are **advisory** — the agent should follow them by default, flag concerns
if the user overrides, but never refuse a user's request based on them.
