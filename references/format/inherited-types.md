# Inherited Types and Universal Properties

This document defines the `InheritedType` enum used in SquareLine Studio project files, detailing data types, layout fields, size/position flags, and universal object properties that apply to all widgets.

## InheritedType Enum

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

## Universal Object Properties

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
