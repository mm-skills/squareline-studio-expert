# Input Widgets

## Slider
**Typical use case:** Adjusting a numeric value within a specific range, such as brightness or volume.
**Default size recommendation:** 200x10 (horizontal) or 10x200 (vertical)
**Required properties:**
```json
{
  "nid": 1010, "strtype": "SLIDER/Slider", "InheritedType": 1
},
{
  "nid": 1020, "flags": 16, "strtype": "SLIDER/Range", "intarray": [0, 100], "InheritedType": 7
},
{
  "nid": 1030, "strtype": "SLIDER/Mode", "strval": "NORMAL", "InheritedType": 3
},
{
  "nid": 1040, "strtype": "SLIDER/Value", "integer": 50, "InheritedType": 6
}
```
**Style parts:**
- `Style_main` (MAIN): The background track.
- `Style_indicator` (INDICATOR): The filled part of the track representing the current value.
- `Style_knob` (KNOB): The draggable handle.
**Common gotchas:** `SLIDER/Value_left` is required if using RANGE mode.

## Switch
**Typical use case:** Toggling between on/off states.
**Default size recommendation:** 50x25
**Required properties:**
```json
{
  "nid": 1010, "strtype": "SWITCH/Switch", "InheritedType": 1
}
```
**Style parts:**
- `Style_main` (MAIN): The background track of the switch.
- `Style_indicator` (INDICATOR): The active state background.
- `Style_knob` (KNOB): The toggle circle.
**Common gotchas:** Switch doesn't have a built-in text label; you often need to pair it with a Label widget or place it inside a Panel.

## Checkbox
**Typical use case:** Toggling a single option with an integrated label.
**Default size recommendation:** 100x20 (often set to content-fit with flag 51 on Size).
**Required properties:**
```json
{
  "nid": 1010, "strtype": "CHECKBOX/Checkbox", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "CHECKBOX/Title", "strval": "Check me", "InheritedType": 10
}
```
**Style parts:**
- `Style_main` (MAIN): The text label.
- `Style_bullet` (INDICATOR): The checkbox itself.
**Common gotchas:** Style_bullet maps to `lv.PART.INDICATOR`. Size should generally be content-fit to avoid clipping the text.

## Dropdown
**Typical use case:** Selecting one option from a collapsible list.
**Default size recommendation:** 130x35
**Required properties:**
```json
{
  "nid": 1010, "strtype": "DROPDOWN/Dropdown", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "DROPDOWN/Options", "strval": "Option 1\\nOption 2\\nOption 3", "InheritedType": 10
},
{
  "nid": 1030, "strtype": "DROPDOWN/Base_text", "strval": "", "InheritedType": 10
},
{
  "nid": 1040, "strtype": "DROPDOWN/Show_selected", "strval": "True", "InheritedType": 2
},
{
  "nid": 1050, "strtype": "DROPDOWN/List_align", "strval": "BOTTOM", "InheritedType": 3
}
```
**Style parts:**
- `Style_main` (MAIN): The closed dropdown button.
- `Style_indicator` (INDICATOR): The drop-down arrow icon.
- `Style_list_main` (list MAIN): The background of the opened list.
- `Style_list_selected` (list SELECTED): The currently selected list item.
**Common gotchas:** Options MUST be separated by a literal `\n` string (e.g., `\\n` in JSON), NOT an actual newline character.

## Roller
**Typical use case:** Scrolling through a list of options (like a date picker or slot machine).
**Default size recommendation:** 100x120
**Required properties:**
```json
{
  "nid": 1010, "strtype": "ROLLER/Roller", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "ROLLER/Options", "strval": "Apples\\nOranges\\nBananas", "InheritedType": 10
},
{
  "nid": 1030, "strtype": "ROLLER/Selected", "integer": 0, "InheritedType": 6
},
{
  "nid": 1040, "strtype": "ROLLER/Mode", "strval": "NORMAL", "InheritedType": 3
}
```
**Style parts:**
- `Style_main` (MAIN): The unselected text and background.
- `Style_selected` (SELECTED): The highlighted middle section.
**Common gotchas:** Like Dropdown, options must use literal `\n`. Can be set to INFINITE mode for continuous scrolling.

## Spinbox
**Typical use case:** Precisely adjusting a numeric value digit-by-digit.
**Default size recommendation:** 100x40
**Required properties:**
```json
{
  "nid": 1010, "strtype": "SPINBOX/Spinbox", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "SPINBOX/Value", "integer": 0, "InheritedType": 6
},
{
  "nid": 1030, "flags": 16, "strtype": "SPINBOX/Range", "intarray": [0, 100, 1], "InheritedType": 7
},
{
  "nid": 1040, "flags": 16, "strtype": "SPINBOX/Digit_format", "intarray": [3, 0], "InheritedType": 7
}
```
**Style parts:**
- `Style_main` (MAIN): The text and background.
- `Style_cursor` (CURSOR): The cursor showing the active digit.
**Common gotchas:** `Range` requires exactly 3 array elements: `[min, max, step]`. `Digit_format` requires `[total_digits, decimal_digits]`.
