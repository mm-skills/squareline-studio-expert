# Display Widgets

## Label
**Typical use case:** Displaying text on the screen.
**Size flags:** Size often uses `flags: 51` for content-fit instead of fixed dimensions.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "LABEL/Label", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "LABEL/Text", "strval": "Hello World", "InheritedType": 10
},
{
  "nid": 1030, "strtype": "LABEL/Long_mode", "strval": "WRAP", "InheritedType": 3
},
{
  "nid": 1040, "strtype": "LABEL/Recolor", "strval": "False", "InheritedType": 2
}
```
**Style parts:** `Style_main` (MAIN)

## Image
**Typical use case:** Displaying graphics, icons, or backgrounds.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "IMAGE/Image", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "IMAGE/Asset", "strval": "assets/logo.png", "InheritedType": 5
},
{
  "nid": 1030, "flags": 16, "strtype": "IMAGE/Pivot", "intarray": [0, 0], "InheritedType": 7
},
{
  "nid": 1040, "strtype": "IMAGE/Rotation", "integer": 0, "InheritedType": 6
},
{
  "nid": 1050, "strtype": "IMAGE/Scale", "integer": 256, "InheritedType": 6
}
```
**Style parts:** `Style_main` (MAIN)

## Arc
**Typical use case:** Displaying values in a circular gauge or meter.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "ARC/Arc", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "ARC/Value", "integer": 50, "InheritedType": 6
},
{
  "nid": 1030, "flags": 16, "strtype": "ARC/Range", "intarray": [0, 100], "InheritedType": 7
},
{
  "nid": 1040, "flags": 16, "strtype": "ARC/Bg_angles", "intarray": [135, 45], "InheritedType": 7
},
{
  "nid": 1050, "strtype": "ARC/Rotation", "integer": 0, "InheritedType": 6
},
{
  "nid": 1060, "strtype": "ARC/Mode", "strval": "NORMAL", "InheritedType": 3
}
```
**Style parts:** `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB)
**Arc Angles Explanation:** `Bg_angles` is `[start, end]`. 0° is at 3 o'clock. Angles increase clockwise. 135° to 45° creates a symmetrical gauge with the gap at the bottom.

## Bar
**Typical use case:** Displaying progress or a level, like a battery or loading bar.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "BAR/Bar", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "BAR/Value", "integer": 60, "InheritedType": 6
},
{
  "nid": 1030, "strtype": "BAR/Value_start", "integer": 0, "InheritedType": 6
},
{
  "nid": 1040, "flags": 16, "strtype": "BAR/Range", "intarray": [0, 100], "InheritedType": 7
},
{
  "nid": 1050, "strtype": "BAR/Mode", "strval": "NORMAL", "InheritedType": 3
}
```
**Style parts:** `Style_main` (MAIN), `Style_indicator` (INDICATOR)

## Spinner
**Typical use case:** Indeterminate loading animation.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "SPINNER/Spinner", "InheritedType": 1
}
```
**Style parts:** `Style_main` (MAIN), `Style_indicator` (INDICATOR)

## Chart
**Typical use case:** Plotting data series (Line, Bar, Scatter).
**Required properties:**
```json
{
  "nid": 1010, "strtype": "CHART/Chart", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "CHART/Chart_type", "strval": "LINE", "InheritedType": 3
},
{
  "nid": 1030, "strtype": "CHART/Number_of_points", "integer": 10, "InheritedType": 6
}
```
**Style parts:** `Style_bg` (MAIN), `Style_indicator` (INDICATOR), `Style_items` (ITEMS), `Style_scrollbar` (SCROLLBAR), `Style_ticks` (TICKS)

## Calendar
**Typical use case:** Selecting dates.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "CALENDAR/Date", "intarray": [1, 1, 2025], "InheritedType": 7
}
```
**Style parts:** `Style_main` (MAIN), `Style_items` (ITEMS)
