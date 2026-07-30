---
name: squareline-expert
description: >
  Generate SquareLine Studio (SLS) project files programmatically for LVGL-based
  embedded UI development. Trigger on: "SquareLine Studio", "SLS project", "LVGL UI",
  "ESP32 display", "HMI touch screen", "CrowPanel", ".spj file", "generate UI layout",
  "create screens", "widget layout", "LVGL project files", "embedded UI design",
  "SLS layout", "round display UI", "rotary display", "touch screen UI project".
  Use when the user wants to create, scaffold, or modify SquareLine Studio project
  files (.spj, .sll, .slt) without using the visual editor, or when they want an
  AI-generated first-cut UI layout for embedded displays.
---

# SquareLine Studio Expert

Generate complete SquareLine Studio project files that open correctly in SLS v1.5+
and produce working LVGL UI code for embedded displays (ESP32, STM32, etc.).

## Quick Start

To generate a project, you need three files minimum:
- `SquareLine_Project.spj` — Widget tree, events, animations
- `SquareLine_Project.sll` — Project metadata (board, resolution, LVGL version)
- `Themes.slt` — Theme definitions

Use `scripts/generate_project.py` for scaffolding, or build the JSON manually
using the reference files below.

---

## ❌ Anti-Pitfall Checklist

These are the most common mistakes. Read BEFORE generating any project files.

### 1. Layout_type strval is ALWAYS "No_layout"
The `strval` field on `OBJECT/Layout_type` is misleading — it's always `"No_layout"`
even when FLEX is active. The **real** layout type is in the numeric `LayoutType` field:
- `0` = No layout
- `1` = FLEX
- `2` = GRID

### 2. Style key names are inconsistent
Some style property keys use spaces: `"Border width"`, `"Blend mode"`, `"Gradient direction"`,
`"Border side"`. One has a typo: `"Bg_gradiens_Color"` (note the 's'). You MUST use
these exact key names — SLS will silently ignore misspelled keys.

### 3. Unset references use "-" not empty string
When a GUID reference is not set (e.g., no target screen), the value is `"-"`, not `""`.

### 4. TABPAGE uses its own prefix
TABPAGE widgets use `TABPAGE/` prefix for ALL properties including flags and states,
unlike every other widget which uses `OBJECT/` for universal properties.

### 5. nidcnt must be tracked
The `nidcnt` field in `.sll` (and `.spj` info block) must be greater than the highest
`nid` value used in any property. Increment it for every new property you add.
Standard widget properties use small nids (10-1050). Events and animations use
nids starting from the current `nidcnt` value.

### 6. GUIDs must be globally unique
Every widget, screen, and root node needs a unique GUID in the format:
`GUID<digits>-<digits>S<digits>`. Generate unique random digits for each.

### 7. v1.6 .spj has an info block
In SLS v1.6+, the `.spj` file contains an `info` block that mirrors the `.sll` metadata.
Both must be consistent. The `.spj` also has `animations`, `selected_theme`, and
`selected_screen` at the top level.

### 8. Size flags encode sizing mode
- `flags: 17` = fixed pixel sizing
- `flags: 51` = content-fit sizing (used on Labels by default)
- `flags: 1048576` = section header flag (on Flags, States, Scrolling group headers)

### 9. Color arrays vary in length
- Background, border, text, shadow colors: `[R, G, B, A]` (4 values, 0-255)
- Gradient color: `[R, G, B]` (3 values, NO alpha)
- Always check the reference for the specific property

### 10. Events need Call and CallC templates
Every event action has `Call` (MicroPython template) and `CallC` (C template) fields
containing placeholder patterns like `<{Screen_to}>`. These are used for code generation
and must match the action type exactly. Copy the templates from the reference.

### 11. Dropdown/Roller options use literal \n, NOT real newlines
Options in `DROPDOWN/Options` and `ROLLER/Options` are separated by the **two-character
sequence** `\n` (backslash + n), NOT actual newline characters. SLS generates Python code
from these strings, and real newlines cause `SyntaxError: invalid syntax`.
```
✅ "Option 1\\nOption 2\\nOption 3"   ← correct (literal \n in JSON)
❌ "Option 1\nOption 2\nOption 3"     ← BREAKS SLS code generation
```

---

## Core Workflow

### Step 1: Understand Requirements
Before generating, establish:
- **Display**: Resolution (width × height), shape (RECTANGLE/CIRCLE), color depth
- **Board**: Target hardware (e.g., "ESP32S335D - MaTouch 3.5-inch")
- **Screens**: How many screens, navigation flow between them
- **Widgets**: What UI elements on each screen
- **Interactions**: Touch events, value changes, screen transitions

### Step 2: Load Target Board Config
→ Read `references/targets/` for board-specific settings.
If no specific board, use a generic Arduino config.

### Step 3: Generate Project Scaffold
Option A: Run `scripts/generate_project.py`:
```bash
python3 scripts/generate_project.py \
  --name "MyProject" \
  --width 480 --height 320 \
  --board "ESP32S335D - MaTouch 3.5-inch Parallel 480x320 TFT with Touch - Arduino-IDE" \
  --screens 3 \
  --output /path/to/output/
```

Option B: Build JSON manually using the structure reference.
→ Read `references/format/project-structure.md`

### Step 4: Add Widgets
For each screen, add the required widgets as children.
→ Read `references/format/widget-catalog.md` for widget properties and defaults.
→ Read `references/widgets/` for detailed widget-group guidance.

Every widget needs at minimum:
```json
{
  "guid": "GUID<unique>",
  "properties": [
    { "nid": 10, "strtype": "OBJECT/Name", "strval": "MyWidget", "InheritedType": 10 },
    { "nid": 20, "strtype": "OBJECT/Layout", "InheritedType": 1 },
    // ... layout_type, transform, position, size, align, flags, scrolling, states
    // ... widget-specific properties (e.g., SLIDER/Range, LABEL/Text)
    // ... style parts (e.g., BUTTON/Style_main)
  ],
  "saved_objtypeKey": "BUTTON"
}
```

### Step 5: Wire Events
Add event handlers to widget properties arrays.
→ Read `references/format/events-actions.md` for event structure and action templates.

### Step 6: Apply Custom Styles
Override default styles by adding child entries to Style_* properties.
→ Read `references/format/styles-states.md` for the complete style property catalog.

### Step 7: Validate
Run the validation script on your output:
```bash
python3 scripts/validate_project.py /path/to/output/
```

---

## Reference Lookup Table

| When you need to... | Read this reference |
|---|---|
| Understand file structure (.spj/.sll/.slt) | `references/format/project-structure.md` |
| Decode InheritedType or property data types | `references/format/inherited-types.md` |
| Add a specific widget type | `references/format/widget-catalog.md` |
| Wire an event or screen transition | `references/format/events-actions.md` |
| Style a widget or set state overrides | `references/format/styles-states.md` |
| Work with sliders, switches, dropdowns, etc. | `references/widgets/input-widgets.md` |
| Work with labels, images, arcs, charts, etc. | `references/widgets/display-widgets.md` |
| Work with panels, tabs, screens | `references/widgets/container-widgets.md` |
| Work with buttons, textareas, keyboards | `references/widgets/interactive-widgets.md` |
| Configure for CrowPanel boards | `references/targets/esp32-crowpanel.md` |
| Configure for generic Arduino boards | `references/targets/general-arduino.md` |
| Find board strings from user's SLS install | `references/targets/supported-boards.md` |

---

## Output Verification Checklist

Before delivering generated project files, verify:

- [ ] `.spj`, `.sll`, and `Themes.slt` all exist
- [ ] All GUIDs are unique across the project
- [ ] `nidcnt` in `.sll` exceeds the highest `nid` used
- [ ] Every widget has `saved_objtypeKey` set correctly
- [ ] Every widget has `OBJECT/Name` with a unique name
- [ ] Screen objects have `isPage: true`
- [ ] Event `Screen_to` values reference valid screen GUIDs
- [ ] Style property key names match EXACTLY (check spaces and typos)
- [ ] Color arrays have correct length (4 for RGBA, 3 for gradient)
- [ ] `.sll` `width`/`height` match the target display resolution
- [ ] v1.6+: `.spj` `info` block mirrors `.sll` metadata

---

## Supported Widget Types

24 widget types available:

`SCREEN` · `PANEL` · `CONTAINER`* · `BUTTON` · `IMGBUTTON` · `LABEL` · `IMAGE` · `ARC` ·
`SLIDER` · `BAR` · `SWITCH` · `CHECKBOX` · `DROPDOWN` · `ROLLER` · `TEXTAREA` ·
`KEYBOARD` · `SPINNER` · `SPINBOX` · `CALENDAR` · `CHART` · `COLORWHEEL`† ·
`TABVIEW` · `TABPAGE`

\* CONTAINER = LVGL 9.x alias for PANEL  
† COLORWHEEL = v8 only, removed in LVGL 9

→ See `references/format/widget-catalog.md` for full property tables.

---

## Supported Event Actions (24)

| Category | Actions |
|----------|--------|
| Navigation | CHANGE SCREEN, DELETE SCREEN |
| Code | CALL FUNCTION |
| Animation | PLAY ANIMATION, SET OPACITY |
| Value Increment | INCREMENT ARC, INCREMENT BAR, INCREMENT SLIDER |
| Property Setting | LABEL_PROPERTY, BAR_PROPERTY, DROPDOWN_PROPERTY, IMAGE_PROPERTY, ROLLER_PROPERTY, SLIDER_PROPERTY, BASIC_PROPERTY |
| Text Display | SET TEXT VALUE FROM ARC, SET TEXT VALUE FROM SLIDER, SET TEXT VALUE WHEN CHECKED |
| State/Flag | MODIFY FLAG, MODIFY STATE |
| Keyboard | KEYBOARD SET TARGET, MOVE CURSOR |
| Other | STEP SPINBOX, SWITCH THEME |

→ See `references/format/events-actions.md` for structures and templates.

---

## Example Projects

SLS ships with 15 example projects at:
`/Applications/SquareLine_Studio.app/Contents/examples/`

Use these as reference for real-world patterns. Notable examples:
- **SmartWatch_392x392** — circular display, 290 widgets, 9 screens
- **Caffee_Machnine_800x480** — most complex: 504 widgets, 78 events, 32 animations
- **Futuristic_Ebike_800x480** — heavy button/slider usage with animations
