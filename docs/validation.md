# SLS Format Validation Coverage

> **Purpose:** Document the provenance of every fact about SquareLine Studio's `.spj`
> file format used in this skill. All claims are traced back to either (a) the 15
> example projects shipped with SLS 1.6.2, or (b) our controlled test project for
> widget types absent from the shipped examples.
>
> **Method:** Clean-room investigation - all facts are verified by inspecting JSON project files shipped as sample projects with SLS or created with SLS's own GUI in the test_project for any widgets not covered in the samples.  NOTE: if inconstencies are discovered when loading SLS files, please file your observations for investigation as a github issue and include any console logs or errors.

---

## Validation Sources

| ID | Source | Path | Description |
|----|--------|------|-------------|
| **S1–S15** | SLS Shipped Examples | `/Applications/SquareLine_Studio.app/Contents/examples/*` | 15 example projects bundled with SLS 1.6.2 |
| **T1** | Coverage Test Project | `test_projects/coverage_test/` | Custom project for the 6 missing widget types |

### SLS Shipped Examples (S1–S15)

| ID | Project | Widget Types Used |
|----|---------|-------------------|
| S1 | `3d_Printer_2_1024x600` | BAR, BUTTON, IMAGE, LABEL, PANEL, SCREEN, SLIDER |
| S2 | `3d_Printer_800x480` | IMAGE, IMGBUTTON, LABEL, PANEL, ROLLER, SCREEN, SLIDER, SWITCH |
| S3 | `3d_printer_2_800x480` | BAR, BUTTON, IMAGE, LABEL, PANEL, SCREEN, SLIDER |
| S4 | `Audio_mixer_480x800` | ARC, IMAGE, IMGBUTTON, LABEL, PANEL, SCREEN, SLIDER |
| S5 | `Caffee_Machnine_800x480` | BUTTON, CONTAINER, IMAGE, LABEL, PANEL, ROLLER, SCREEN, SLIDER |
| S6 | `EV_Charger_1024x600` | BUTTON, CHART, IMAGE, LABEL, PANEL, SCREEN, SPINNER |
| S7 | `EV_Charger_1280x800` | BUTTON, CHART, IMAGE, LABEL, PANEL, SCREEN, SPINNER |
| S8 | `EV_Charger_800x480` | BUTTON, CHART, CONTAINER, IMAGE, LABEL, PANEL, SCREEN, SPINNER |
| S9 | `Futuristic_Ebike_480x272` | BUTTON, CHART, IMAGE, LABEL, PANEL, ROLLER, SCREEN, SLIDER |
| S10 | `Futuristic_Ebike_800x480` | BUTTON, CHART, CONTAINER, IMAGE, LABEL, PANEL, ROLLER, SCREEN, SLIDER |
| S11 | `Medical_272x480` | IMAGE, LABEL, PANEL, SCREEN, SLIDER, SWITCH |
| S12 | `POS_272x480` | IMAGE, KEYBOARD, LABEL, PANEL, SCREEN, TEXTAREA |
| S13 | `SmartWatch_392x392` | ARC, BUTTON, CHART, IMAGE, LABEL, PANEL, SCREEN, SPINNER |
| S14 | `Smart_Gadget_240x320` | IMAGE, LABEL, PANEL, SCREEN, SWITCH |
| S15 | `Thermostat_480x800` | ARC, LABEL, PANEL, SCREEN, SLIDER |

### Coverage Test Project (T1)

| Screen | Widget Types | Instances |
|--------|-------------|-----------|
| ScreenCalendarCheckbox | **CALENDAR**, **CHECKBOX** | 1 CALENDAR, 2 CHECKBOX |
| ScreenDropdownSpinbox | **DROPDOWN**, **SPINBOX** | 2 DROPDOWN, 2 SPINBOX |
| ScreenTabview | **TABVIEW**, **TABPAGE** | 1 TABVIEW (3 TABPAGEs) |

**Pre-SLS snapshot:** `CoverageTest.spj.before` (agent-generated, minimal properties only)

**Post-SLS snapshot:** `CoverageTest.spj` (after opening and saving in SLS — contains all normalised properties)

---

## Widget Type Coverage Matrix

| Widget Type | In Shipped Examples | Source(s) | In Coverage Test |
|-------------|--------------------:|-----------|:----------------:|
| ARC | ✅ 3 examples | S4, S13, S15 | — |
| BAR | ✅ 2 examples | S1, S3 | — |
| BUTTON | ✅ 8 examples | S1,S3,S5–S10,S13 | — |
| **CALENDAR** | ❌ | — | ✅ T1 |
| CHART | ✅ 6 examples | S6–S10, S13 | — |
| **CHECKBOX** | ❌ | — | ✅ T1 |
| CONTAINER | ✅ 3 examples | S5, S8, S10 | — |
| **DROPDOWN** | ❌ | — | ✅ T1 |
| IMAGE | ✅ 15 examples | S1–S15 | — |
| IMGBUTTON | ✅ 1 example | S2 | — |
| KEYBOARD | ✅ 1 example | S12 | — |
| LABEL | ✅ 15 examples | S1–S15 | — |
| PANEL | ✅ 15 examples | S1–S15 | — |
| ROLLER | ✅ 4 examples | S2, S5, S9, S10 | — |
| SCREEN | ✅ 15 examples | S1–S15 | — |
| SLIDER | ✅ 8 examples | S1–S5, S9–S11, S15 | — |
| **SPINBOX** | ❌ | — | ✅ T1 |
| SPINNER | ✅ 3 examples | S6–S8, S13 | — |
| SWITCH | ✅ 3 examples | S2, S11, S14 | — |
| **TABPAGE** | ❌ | — | ✅ T1 |
| **TABVIEW** | ❌ | — | ✅ T1 |
| TEXTAREA | ✅ 1 example | S12 | — |

**Result: 22/22 widget types covered** (16 from shipped examples + 6 from coverage test).

---

## Style Parts Coverage

### Confirmed from Shipped Examples (S1–S15)

Every widget instance in every shipped example includes its `Style_*` parts — even when no styles are customised. The parts are structural nodes that SLS requires.

| Widget | Style Parts | Source(s) |
|--------|------------|-----------|
| **ARC** | `Style_main`, `Style_indicator`, `Style_knob` | S4, S13, S15 |
| **BAR** | `Style_main`, `Style_indicator` | S1, S3 |
| **BUTTON** | `Style_main` | S1, S3, S5–S10, S13 |
| **CHART** | `Style_bg`, `Style_indicator`, `Style_items`, `Style_scrollbar`, `Style_ticks` | S6–S10, S13 |
| **CONTAINER** | `Style_main`, `Style_scrollbar` | S5, S8, S10 |
| **IMAGE** | `Style_main` | S1–S15 |
| **IMGBUTTON** | `Style_main` | S2 |
| **KEYBOARD** | `Style_main`, `Style_items` | S12 |
| **LABEL** | `Style_main` | S1–S15 |
| **PANEL** | `Style_main`, `Style_scrollbar` | S1–S15 |
| **ROLLER** | `Style_main`, `Style_selected` | S2, S5, S9, S10 |
| **SCREEN** | `Style_main`, `Style_scrollbar` | S1–S15 |
| **SLIDER** | `Style_main`, `Style_indicator`, `Style_knob` | S1–S5, S9–S11, S15 |
| **SPINNER** | `Style_main`, `Style_indicator` | S6–S8, S13 |
| **SWITCH** | `Style_main`, `Style_indicator`, `Style_knob` | S2, S11, S14 |
| **TEXTAREA** | `Style_main`, `Style_cursor`, `Style_placeholder`, `Style_selected` | S12 |

### ✅ Confirmed from Coverage Test (T1) — SLS 1.6.2 open+save on 2026-08-15

The user opened `CoverageTest.spj` in SLS 1.6.2 and saved. Diffing `.spj.before` vs `.spj` confirmed:

| Widget | Confirmed Style Parts | `part` value | `strval` (accepted style categories) |
|--------|----------------------|-------------|--------------------------------------|
| **CALENDAR** | `Style_main`, `Style_items` | `lv.PART.MAIN`, `lv.PART.ITEMS` | `Rectangle, Pad, Transform` / `Rectangle, Pad` |
| **CHECKBOX** | `Style_main`, `Style_bullet` | `lv.PART.MAIN`, `lv.PART.INDICATOR` | `Text, Transform` / `Rectangle, Pad` |
| **DROPDOWN** | `Style_main`, `Style_indicator`, `Style_list_main` ⚡, `Style_list_scrollbar` ⚡, `Style_list_selected` ⚡ | `MAIN`, `INDICATOR`, then sub-object `MAIN`/`SCROLLBAR`/`SELECTED` | See detail below |
| **SPINBOX** | `Style_main`, `Style_cursor` | `lv.PART.MAIN`, `lv.PART.CURSOR` | `Rectangle, Pad, Text, Transform` / `Rectangle, Text` |
| **TABVIEW** | `Style_main`, `Style_buttons_main` ⚡, `Style_buttons_items` ⚡ | `lv.PART.MAIN`, then sub-object `MAIN`/`ITEMS` | `Rectangle, Pad, Text, Transform` / see detail below |
| **TABPAGE** | `Style_main`, `Style_scrollbar` | `lv.PART.MAIN`, `lv.PART.SCROLLBAR` | `Rectangle, Pad, Text, Transform` / `Rectangle, Pad` |

> ⚡ = sub-object style. The `strval` encodes the accessor function:
> - DROPDOWN list styles: `{"python":"{0}.get_list()","c":"lv_dropdown_get_list({0})"}`
> - TABVIEW button styles: `{"python":"{0}.get_tab_bar()","c":"lv_tabview_get_tab_bar({0})"}`

#### Additional findings from coverage test

| Finding | Detail |
|---------|--------|
| **TABPAGE uses widget-type prefix for boolean flags** | SLS added 29 flags as `TABPAGE/Hidden`, `TABPAGE/Clickable`, etc. — NOT `OBJECT/Hidden`. This is unique to TABPAGE. |
| **`State_trickle` absent on SCREEN and TABPAGE** | SLS added `OBJECT/State_trickle` to CALENDAR, CHECKBOX, DROPDOWN, SPINBOX, TABVIEW — but NOT to SCREEN or TABPAGE widgets. |
| **SLS removed some properties we set** | `TABPAGE/Scroll_snap_x`, `TABPAGE/Scroll_snap_y`, `TABPAGE/Scrolling`, `TABPAGE/Transform` were removed by SLS. TABPAGEs do not support these. |
| **SLS added widget-specific properties** | CALENDAR got `Date`; DROPDOWN got `Base_text`, `List_align`, `Show_selected`; SPINBOX got `Digit_format`, `Range`, `Value`; TABVIEW got `Children`. |

---

## Issue-Specific Validation Evidence

### Issue #8 — `.slp` `uiExportFolderPath`

| Claim | Evidence | Source |
|-------|----------|--------|
| `.slp` contains `uiExportFolderPath` | Present in all 15 examples | S1–S15 |
| `.slp` contains `projectExportFolderPath` | Present in all 15 examples | S1–S15 |
| 14/15 ship empty, 1 has stale path | S7 has `D:/esp32/EXPORTTTEEESSZZTT/EV_Charger/./ui` | S7 |
| `.slp` has exactly 10 keys | Confirmed across all 15 | S1–S15 |

### Issue #6A — `\n` in text fields

| Claim | Evidence | Source |
|-------|----------|--------|
| SLS uses `\\n` (JSON-escaped) in LABEL/Text | 11/15 examples contain `\\n` in label text | S1–S12 |
| Same convention for ROLLER/Options | Found in S2, S5, S9, S10 | S2, S5, S9, S10 |
| `strval` stores the 2-char sequence `\n` | `repr()` confirms: `'MOVE\\nZ'` → two chars backslash+n | S2 |

### Issue #6B — Theme color names

| Claim | Evidence | Source |
|-------|----------|--------|
| No hyphens in shipped color names | **No examples define custom color names at all** — all `colors` arrays empty | S1–S15 |
| Theme definitions live in `Themes.slt` | All 15 have `Themes.slt` | S1–S15 |

> [!WARNING]
> This claim is validated by **absence of counter-evidence**, not by positive example. No shipped example exercises custom theme colour naming.

### Issue #6C — `deftheme` must be "Default"

| Claim | Evidence | Source |
|-------|----------|--------|
| All shipped examples use `deftheme.name = "Default"` | **15/15 confirmed** | S1–S15 |
| No example uses custom deftheme names | 0 counter-examples | S1–S15 |
| No example uses additional `themes[]` entries | All 15 have `themes: []` | S1–S15 |

### Issue #6D — Alignment values (no `ALIGN_` prefix)

| Claim | Evidence | Source |
|-------|----------|--------|
| All values use short form | Complete set found across 15 examples: `CENTER`, `TOP_LEFT`, `TOP_MID`, `TOP_RIGHT`, `BOTTOM_LEFT`, `BOTTOM_MID`, `BOTTOM_RIGHT`, `LEFT_MID`, `RIGHT_MID` | S1–S15 |
| No `ALIGN_` prefix found | 0 instances across all 15 examples | S1–S15 |

### Issue #6E — Style_* parts

See **Style Parts Coverage** section above. **All 22/22 types now confirmed** — 16 from shipped examples (S1–S15), 6 from coverage test T1.

### Issue #6F — `OBJECT/State_trickle`

| Claim | Evidence | Source |
|-------|----------|--------|
| Not present in shipped examples | 0/15 examples contain `OBJECT/State_trickle` — they target LVGL 9.2.2 | S1–S15 |
| Present on LVGL 9.5 widgets (except SCREEN and TABPAGE) | SLS added `State_trickle=False` to CALENDAR, CHECKBOX, DROPDOWN, SPINBOX, TABVIEW | T1 |
| Not present on SCREEN or TABPAGE | SLS did NOT add `State_trickle` to SCREENs or TABPAGEs | T1 |
| Default value is `"False"` | All instances have `strval: "False"` | T1 |

### Issue #4 — `OBJECT/Hidden`

| Claim | Evidence | Source |
|-------|----------|--------|
| SLS uses `OBJECT/Hidden` with `InheritedType: 2` | 12/15 examples contain it | S1, S3–S11, S13, S14 |
| Values are `"True"` and `"False"` (strings) | Both values confirmed | S1, S3–S11, S13, S14 |
| No `OBJ_FLAG_HIDDEN` in any `.spj` | 0 instances | S1–S15 |
| Present on hundreds of widgets (even when False) | S5 has 412 instances | S5 |

### Issue #7 — Custom font registration

| Claim | Evidence | Source |
|-------|----------|--------|
| Custom fonts need `.fcfg` + `.bin` + `.c` | 13/15 examples ship all three file types | S1–S4, S6–S14 |
| `.fcfg` JSON structure documented | Full schema extracted from S12 (`POS_272x480`) | S12 |
| Widget `Text_Font` uses codename (no `ui_font_` prefix) | All 15 examples use short codenames | S1–S15 |
| `lv_font_conv` tool shipped with SLS | Located at `/Applications/SquareLine_Studio.app/Contents/lvgl/lv_font_conv-osx` | SLS install |

---

## Post-SLS Validation Procedure

After the user opens the coverage test project in SLS and saves it:

1. **Diff the `.spj` files:**
   ```bash
   cd test_projects/coverage_test/
   python3 -c "
   import json
   before = json.load(open('CoverageTest.spj.before'))
   after = json.load(open('CoverageTest.spj'))
   # Compare widget properties to find SLS-added Style_* parts
   "
   ```

2. **Extract new Style_* parts** for each of the 6 widget types.

3. **Update this document** with confirmed Style_* parts and mark as ✅.

4. **Update `widget_helpers.py`** if any Style_* parts are missing or incorrect.

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-08-15 | Initial validation against S1–S15 shipped examples | Agent |
| 2026-08-15 | Created coverage test project T1 for 6 missing widget types | Agent |
| 2026-08-15 | ✅ SLS open+save of T1 completed. All 6 types confirmed. `State_trickle` behaviour on SCREEN/TABPAGE clarified. TABPAGE flag prefix convention discovered. | Agent + User (SLS save) |
| 2026-08-15 | Added anti-pitfalls #17–#22 to SKILL.md, 7 new checks to validate_project.py, .slp generation to generate_project.py. PR fix/issue-analysis-fixes. Closes #4, #5, #6, #7, #8, #9. | Agent |
