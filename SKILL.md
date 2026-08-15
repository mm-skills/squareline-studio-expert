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

### 11. ALL text fields use literal \n, NOT real newlines
Text in `LABEL/Text`, `DROPDOWN/Options`, `ROLLER/Options`, `TEXTAREA/Text`,
`TEXTAREA/Placeholder`, `CHECKBOX/Title`, and `DROPDOWN/Base_text` must use the
**two-character sequence** `\n` (backslash + n) for line breaks, NOT actual newline
characters (0x0A). SLS's code generator passes `strval` directly into string literals.
A real newline breaks the JSON and/or produces `SyntaxError: invalid syntax` in the
generated Python code.
```
✅ "Line 1\\nLine 2"   ← correct (literal \n in JSON)
❌ "Line 1\nLine 2"     ← BREAKS JSON and SLS code generation
```

### 12. Free-tier projects have strict size limits
The Personal (free) license enforces hard limits: **max 10 screens, 150 widgets,
1 component, 5 global colors, 2 themes**. Exceeding these will cause SLS to refuse
to save the project. Always confirm the user's license tier before generating, and
default to free-tier limits unless told otherwise.
→ Read `references/licensing-limitations.md` for full details and budgeting strategies.

### 13. Only even Montserrat sizes 8–48 are built-in
SLS ships 21 built-in Montserrat font sizes: **8, 10, 12, 14, 16, 18, 20, 22, 24,
26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48** — even numbers only. Referencing
`montserrat_56` or `montserrat_13` will produce a "Font is missing" warning. Any
size outside this range requires a custom font — use `scripts/convert_font.py` to
generate one from a TTF source file using SLS's bundled `lv_font_conv` binary.
→ Read `references/format/fonts.md` for the complete font reference.

### 14. LVGL version determines widget availability and code output
SLS supports LVGL **v8.3.x** and **v9.x** (9.1, 9.2, 9.3, 9.5). The LVGL version is set
by the board's `supported_lvgl_version` field. Key differences:
- **COLORWHEEL** is v8 only — removed in LVGL 9
- **CONTAINER** is the LVGL 9 name for PANEL (both work in SLS)
- Most popular boards (Arduino TFT_eSPI, CrowPanel, MaTouch, M5Stack) now target **v9.5** (as of SLS 1.6.2)
- All 15 bundled SLS examples use **v9.2.2**
- Default to **v9** for new projects unless the user specifies a v8 board.
→ Read `references/format/lvgl-version-guide.md` for the full version guide.

### 15. Board string and version determine LVGL export generation
The `board` and `board_version` in `.sll` must match an installed `.slb` board
pack. An unrecognised board string causes SLS to show "Custom Board" and may
silently **fall back to v8 code generation** on export, even if `lvgl_version`
is set to v9. Many boards (e.g. `"Arduino with TFT_eSPI"`) have multiple
versions — v1.x supports v8 only, latest board versions target v9.5. Use `v2.3.0` for v9
projects. For projects without a hardware-specific board, use
`"CMake/Eclipse/VScode with SDL for development on PC"` (the board used by all
bundled SLS examples).

### 16. Only use recognised LVGL version strings
Valid `lvgl_version` values are: `"8.3.11"`, `"9.1.0"`, `"9.2.2"`, `"9.3"`, `"9.5"`.
Arbitrary strings like `"9.0.0"` are silently accepted by SLS but don't map to
any export template. Default to `"9.5"` for new v9 projects.

### 17. Alignment values have NO prefix
The `OBJECT/Align` property uses short-form values: `CENTER`, `TOP_LEFT`, `TOP_MID`,
`TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_MID`, `BOTTOM_RIGHT`, `LEFT_MID`, `RIGHT_MID`.
Never add an `ALIGN_` prefix — the code template adds `LV_ALIGN_` (C) or `lv.ALIGN.`
(Python) automatically. Using `ALIGN_CENTER` produces `LV_ALIGN_ALIGN_CENTER` which
doesn't exist in LVGL.

### 18. Theme color names must be valid C identifiers
Custom color names defined in `Themes.slt` become variable names in exported code.
Use only alphanumeric characters and underscores (e.g., `dark_blue`, not `dark-blue`).
Hyphens cause compilation errors. The default theme must be named `"Default"` — SLS
generates `UI_THEME_DEFAULT` from this name.

### 19. Widget visibility uses OBJECT/Hidden, not OBJ_FLAG_HIDDEN
To set a widget's initial visibility in the `.spj`, use `OBJECT/Hidden` with
`InheritedType: 2` and `strval: "True"` or `"False"`. Do NOT use `OBJ_FLAG_HIDDEN` —
that is an LVGL runtime constant, not an SLS project property. SLS's code generator
maps `Hidden: True` → `lv_obj_add_flag(obj, LV_OBJ_FLAG_HIDDEN)` in the export.
Exception: TABPAGE widgets use `TABPAGE/Hidden` instead of `OBJECT/Hidden`.

### 20. Every widget MUST include its Style_* part nodes
SLS requires every widget to have its type-specific `Style_*` properties — even if
no styles are customised. Missing Style_* nodes cause a NullReferenceException in SLS.
See the complete catalogue in `references/format/widget-catalog.md`. The
`widget_helpers.py` builder adds these automatically.

### 21. Clear .slp export paths when copying or scaffolding projects
The `.slp` file contains `uiExportFolderPath` and `projectExportFolderPath` which
store absolute filesystem paths from the last export. When copying or scaffolding a
project, these MUST be set to `""` (empty string) to prevent SLS from silently
exporting to the previous user's filesystem location. Even SLS's own shipped examples
have this bug (EV_Charger_1280x800 ships with a stale Windows path).

### 22. Project name must be set — don't leave it as "SquareLine_Project"
The project display name in SLS comes from `info.Name` in the `.spj` (and mirrors
in `.sll` `name` and `project.info` `project_name`). All 5 name fields must be
consistent and descriptive. The default `"SquareLine_Project"` makes all projects
indistinguishable in SLS's Recent Projects list and title bar.

### 23. Custom fonts need 3 files: `.c`, `.bin`, AND `.fcfg`
Every custom font requires three files in `assets/fonts/`:
- `ui_font_<Name>.c` — LVGL C source (for firmware compilation)
- `ui_font_<Name>.bin` — binary font (for SLS preview rendering)
- `ui_font_<Name>.fcfg` — JSON metadata (so SLS recognises the font)

Missing the `.bin` shows placeholder squares in SLS. Missing the `.fcfg` makes SLS
not recognise the font at all. Use `scripts/convert_font.py` to generate all three.
→ Read `references/format/fonts.md` for the full custom font workflow.

---

## Core Workflow

### Step 1: Understand Requirements
Before generating, establish:
- **License tier**: Personal (free), Small Business, Business, or Enterprise?
  Default to **Personal (free)** unless the user specifies otherwise.
- **Display**: Resolution (width × height), shape (RECTANGLE/CIRCLE), color depth
- **Board**: Target hardware (e.g., "ESP32S335D - MaTouch 3.5-inch")
- **LVGL version**: Determined by board selection. Default to **v9** for new projects.
  If the user mentions a specific board, check its `supported_lvgl_version`.
  → Read `references/format/lvgl-version-guide.md` if uncertain.
- **Screens**: How many screens, navigation flow between them
- **Widgets**: What UI elements on each screen
- **Interactions**: Touch events, value changes, screen transitions

If using the **free tier**, apply project size constraints from the start:
→ Read `references/licensing-limitations.md` for limits and widget budgeting.

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
**Preferred:** Use `scripts/widget_helpers.py` for programmatic widget construction:
```python
from widget_helpers import WidgetBuilder
wb = WidgetBuilder()
label = wb.label("title", text="Hello", font="montserrat_24", align="CENTER")
button = wb.button("save", text="Save", size=(120, 48),
                   on_click=wb.call_function("on_save"))
wb.add_children(screen, [label, button])
```
The helper handles GUID generation, nidcnt tracking, all 16 mandatory base
properties, style quirks, and event templates automatically.

**Manual alternative:** Build JSON by hand using the reference docs.
→ Read `references/format/widget-catalog.md` for widget properties and defaults.
→ Read `references/widgets/` for detailed widget-group guidance.

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
| Design a screen layout or choose a pattern | `references/ux/design-guidelines.md` |
| Layout patterns for round displays | `references/ux/round-display-patterns.md` |
| Layout patterns for rectangular displays | `references/ux/rectangular-display-patterns.md` |
| Plan screen navigation and flow | `references/ux/screen-flow-patterns.md` |
| Build a common UI component (thermostat, settings, etc.) | `references/ux/widget-recipes.md` |
| Check license tier limits and widget budgets | `references/licensing-limitations.md` |
| Check available fonts or add custom fonts | `references/format/fonts.md` |
| Find image assets for a project | `references/format/image-asset-sources.md` |
| Check LVGL version compatibility and migration | `references/format/lvgl-version-guide.md` |
| Build widgets programmatically with a helper API | `scripts/widget_helpers.py` |
| Convert a TTF font to SLS custom font files (.c, .bin, .fcfg) | `scripts/convert_font.py` |
| Debug SLS crashes, LVGL runtime errors, or project load failures | `references/troubleshooting.md` |
| Report a bug or defect in the skill | `references/issue-management.md` |
| Contribute a fix or propose an enhancement | `references/contribution-protocol.md` |

---

## UX Design Guidelines (Advisory)

When generating UI layouts, consult `references/ux/` for best-practice guidance drawn from
Material Design, iOS Human Interface Guidelines, and embedded display ergonomics.

**How to apply these guidelines:**
1. **Follow by default** — use recommended patterns, sizes, and layouts unless the user
   specifies otherwise. These patterns are drawn from mobile UI conventions that most
   users are already familiar with.
2. **Flag concerns, don't block** — if a user's request conflicts with a guideline,
   implement what they ask but note the concern:
   > ⚠️ **UX note:** The touch targets on this screen are 30×30px, below the
   > recommended 48×48px minimum for embedded displays. This may be difficult to
   > tap accurately. Let me know if you'd like me to adjust sizing.
3. **Never refuse** — these are guidelines, not rules. The user's intent always takes
   priority over best practice.
4. **Suggest improvements** — when generating from scratch, proactively apply best
   practices and briefly mention which guidelines informed your choices.
5. **Consider the input model** — if the device has a rotary encoder, prefer sequential
   navigation patterns and scroll-friendly layouts. If touch-only, prioritise clear
   tap targets and gesture affordances.

→ Read `references/ux/design-guidelines.md` for the full guideline catalog.

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
- [ ] Free tier: total screens ≤ 10
- [ ] Free tier: total widgets ≤ 150
- [ ] Free tier: components ≤ 1
- [ ] Free tier: global colors ≤ 5
- [ ] Free tier: themes ≤ 2

---

## Supported Widget Types

24 widget types available:

`SCREEN` · `PANEL` · `CONTAINER`* · `BUTTON` · `IMGBUTTON` · `LABEL` · `IMAGE` · `ARC` ·
`SLIDER` · `BAR` · `SWITCH` · `CHECKBOX` · `DROPDOWN` · `ROLLER` · `TEXTAREA` ·
`KEYBOARD` · `SPINNER` · `SPINBOX` · `CALENDAR` · `CHART` · `COLORWHEEL`† ·
`TABVIEW` · `TABPAGE`

\* CONTAINER = LVGL 9.x alias for PANEL (preferred name in v9 projects)  
† COLORWHEEL = v8 only, removed in LVGL 9 — do not use for v9 projects

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
