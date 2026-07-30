# Styles, States, and Animations

This document covers style states, the complete 31-property style catalog, animation structures, and component definitions in SquareLine Studio. Note the warning regarding inconsistent key names in style properties.

## Style States

Styles are nested inside `Style_*` properties. Multiple states can coexist.

### Confirmed Widget Style Parts

All style parts accept the same 31 properties (see catalog below). SLS may show a
reduced subset in the UI for non-MAIN parts, but programmatically any property can
be set on any part.

#### Style Part → Visual Mapping

| SLS Part Name | LVGL Part | What it controls |
|---|---|---|
| `Style_main` | `LV_PART_MAIN` | Widget background, border, outline, shadow, padding, text |
| `Style_indicator` | `LV_PART_INDICATOR` | Filled/active portion (slider fill, arc progress) |
| `Style_knob` | `LV_PART_KNOB` | Draggable handle. Padding resizes it |
| `Style_items` | `LV_PART_ITEMS` | Repeated sub-elements (keyboard keys) |
| `Style_selected` | `LV_PART_SELECTED` | Selected item (roller highlight, textarea selection) |
| `Style_cursor` | `LV_PART_CURSOR` | Insertion cursor (textarea blinker) |
| `Style_bullet` | `LV_PART_INDICATOR` | Checkbox tick box (SLS-specific name) |
| `Style_scrollbar` | `LV_PART_SCROLLBAR` | Scrollbar track/thumb |
| `Style_bg` | `LV_PART_MAIN` | Chart background (SLS alias) |
| `Style_ticks` | `LV_PART_TICKS` | Chart axis tick marks and labels |

#### Per-Widget Style Parts

| Widget | Parts | Notes |
|--------|-------|-------|
| SCREEN | `main`, `scrollbar` | Background and scrollbar |
| PANEL | `main`, `scrollbar` | Main has full 31 properties |
| CONTAINER | `main`, `scrollbar` | Like PANEL |
| BUTTON | `main` | Bg, border, shadow, padding |
| IMGBUTTON | `main` | Image states |
| LABEL | `main` | Text color, font, decoration |
| IMAGE | `main` | Recolor, opacity, transform |
| SLIDER | `main`, `indicator`, `knob` | main=track bg, indicator=fill, knob=handle |
| ARC | `main`, `indicator`, `knob` | main=bg arc, indicator=value arc, knob=handle |
| BAR | `main`, `indicator` | Like slider without knob |
| SWITCH | `main`, `indicator`, `knob` | main=track, indicator=on-state, knob=toggle |
| CHECKBOX | `main`, `bullet` | main=text area, bullet=the tick box |
| DROPDOWN | `main`, `indicator`, `list_main`, `list_selected` | The button, arrow, list bg, highlighted item |
| ROLLER | `main`, `selected` | main=list bg, selected=highlighted row |
| TEXTAREA | `main`, `selected`, `cursor`, `placeholder` | bg, highlight, blinker, placeholder text |
| KEYBOARD | `main`, `items` | main=bg, items=individual keys |
| SPINBOX | `main`, `cursor` | Input field, cursor |
| CHART | `bg`, `scrollbar`, `indicator`, `items`, `ticks` | bg=chart area, items=data points, ticks=axis labels |
| CALENDAR | `main`, `items` | Background, day cells |
| SPINNER | `main`, `indicator` | main=bg track, indicator=spinning arc |
| TABVIEW | `main`, `buttons_main`, `buttons_items` | Tab bar container, tab buttons bg, individual tabs |
| TABPAGE | `main`, `scrollbar` | Content area, scrollbar |

### Style State Structure

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
      "strtype": "_style/StyleState",
      "strval": "DEFAULT",
      "childs": [
        { "strtype": "_style/Bg_Color", "flags": 4096, "intarray": [255, 255, 255, 255], "InheritedType": 7 }
      ]
    },
    {
      "strtype": "_style/StyleState",
      "strval": "CHECKED",
      "childs": [
        { "strtype": "_style/Bg_Color", "flags": 4096, "intarray": [255, 0, 0, 255], "InheritedType": 7 }
      ]
    }
  ]
}
```

### Style States
`DEFAULT`, `PRESSED`, `CHECKED`, `FOCUSED`, `DISABLED`, `CHECKED|PRESSED`, etc.

### The `flags` Field on IT=7 Properties

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

### Style Properties (Complete Catalog — 31 properties)

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

## Animations (v1.5 project data)

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

## Components (`.ecomp`)

Same JSON structure as a widget in `.spj`. Represents reusable widget templates.
