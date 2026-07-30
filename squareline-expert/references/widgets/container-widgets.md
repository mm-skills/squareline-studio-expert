# Container Widgets

## Screen
**Role in the widget hierarchy:** The absolute root for any visible UI. Everything must be placed on a Screen.
**Screen-specific characteristics:**
- In the JSON hierarchy, screens must have `"isPage": true`.
- They require specific properties: `SCREEN/Screen` and `SCREEN/Temporary` (usually `"False"`).
- Often used to define the dark background color of the UI using `Style_main`.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "SCREEN/Screen", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "SCREEN/Temporary", "strval": "False", "InheritedType": 2
}
```

## Panel
**Role in the widget hierarchy:** A generic container for grouping widgets, applying backgrounds/borders, and managing layouts.
**FLEX/GRID layout usage:**
To use FLEX layout, replace the standard `Layout_type` property with:
```json
{
  "Flow": 0, "Wrap": true, "Reversed": false,
  "MainAlignment": 0, "CrossAlignment": 1, "TrackAlignment": 0,
  "LayoutType": 1, "nid": 30, "strtype": "OBJECT/Layout_type",
  "strval": "No_layout", "InheritedType": 13
}
```
(LayoutType=1 is FLEX, LayoutType=2 is GRID).
**Spacing:** When using flex/grid, use `Padding_RowCol` in `Style_main` to define spacing between children.

## TabView
**Role in the widget hierarchy:** Manages multiple TabPages, displaying a tab bar for navigation.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "TABVIEW/Tabview", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "TABVIEW/Tab_position", "strval": "TOP", "InheritedType": 3
},
{
  "nid": 1030, "strtype": "TABVIEW/Tab_size", "integer": 50, "InheritedType": 6
}
```

## TabPage
**Role in the widget hierarchy:** A child container strictly belonging to a TabView.
**The TABPAGE/ Prefix Anomaly:**
Unlike almost every other widget that uses `OBJECT/` for base properties (like Size, Position, Flags, States, Scrollable), TabPage uses `TABPAGE/` for EVERYTHING.
Example: Instead of `OBJECT/Flags`, it uses `TABPAGE/Flags`. Instead of `OBJECT/Size`, it uses `TABPAGE/Size`.
**Required properties:**
```json
{
  "nid": 1010, "strtype": "TABPAGE/TabPage", "InheritedType": 1
},
{
  "nid": 1020, "strtype": "TABPAGE/Title", "strval": "Tab 1", "InheritedType": 10
},
{
  "nid": 1030, "strtype": "TABPAGE/Name", "strval": "Tab1Page", "InheritedType": 10
}
```
