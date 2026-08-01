# Widget Catalog

This document catalogs the 24 widget types available in SquareLine Studio, detailing their specific properties and style parts.

## Complete Widget Catalog (24 Types)

All confirmed from `research/new01/` (v1.6.1).

> [!NOTE]
> CONTAINER is an LVGL 9.x alias for PANEL. COLORWHEEL was removed in LVGL 9.

### SCREEN
| strtype | IT | Description |
|---------|:---:|---|
| `SCREEN/Screen` | 1 | Section header |
| `SCREEN/Temporary` | 2 | Temporary screen flag |
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

### PANEL
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

### CONTAINER (LVGL 9.x)
| strtype | IT | Description |
|---------|:---:|---|
| `CONTAINER/Edited` | 2 | Edit flag |
| **Style parts:** | | `Style_main` (MAIN), `Style_scrollbar` (SCROLLBAR) |

> Functionally identical to PANEL. Uses standard `OBJECT/*` properties.
> Found heavily in SLS bundled examples (e.g., Coffee Machine: 218 instances).

### BUTTON
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN) |

### IMGBUTTON
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

### LABEL
| strtype | IT | Description |
|---------|:---:|---|
| `LABEL/Label` | 1 | Section header |
| `LABEL/Text` | 10 | Text content |
| `LABEL/Long_mode` | 3 | `"WRAP"`, `"SCROLL"`, `"DOT"`, `"CLIP"` |
| `LABEL/Recolor` | 2 | Enable recoloring syntax |
| **Style parts:** | | `Style_main` (MAIN) |

### IMAGE
| strtype | IT | Description |
|---------|:---:|---|
| `IMAGE/Image` | 1 | Section header |
| `IMAGE/Asset` | 5 | Asset path |
| `IMAGE/Pivot` | 7 | Rotation pivot `[x, y]` |
| `IMAGE/Rotation` | 6 | Rotation (0.1° units) |
| `IMAGE/Scale` | 6 | Scale (256 = 100%) |
| **Style parts:** | | `Style_main` (MAIN) |

### ARC
| strtype | IT | Description |
|---------|:---:|---|
| `ARC/Arc` | 1 | Section header |
| `ARC/Value` | 6 | Current value |
| `ARC/Range` | 7 | `[min, max]` |
| `ARC/Bg_angles` | 7 | `[start_angle, end_angle]` |
| `ARC/Rotation` | 6 | Rotation offset |
| `ARC/Mode` | 3 | `"NORMAL"`, `"REVERSE"`, `"SYMMETRICAL"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### SLIDER
| strtype | IT | Description |
|---------|:---:|---|
| `SLIDER/Slider` | 1 | Section header |
| `SLIDER/Value` | 6 | Current value |
| `SLIDER/Value_left` | 6 | Left value (range mode) |
| `SLIDER/Range` | 7 | `[min, max]` |
| `SLIDER/Mode` | 3 | `"NORMAL"`, `"SYMMETRICAL"`, `"RANGE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### BAR
| strtype | IT | Description |
|---------|:---:|---|
| `BAR/Bar` | 1 | Section header |
| `BAR/Value` | 6 | Current value |
| `BAR/Value_start` | 6 | Start value (range mode) |
| `BAR/Range` | 7 | `[min, max]` |
| `BAR/Mode` | 3 | `"NORMAL"`, `"SYMMETRICAL"`, `"RANGE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR) |

### SWITCH
| strtype | IT | Description |
|---------|:---:|---|
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_knob` (KNOB) |

### CHECKBOX
| strtype | IT | Description |
|---------|:---:|---|
| `CHECKBOX/Checkbox` | 1 | Section header |
| `CHECKBOX/Title` | 10 | Checkbox text label |
| **Style parts:** | | `Style_main` (MAIN), `Style_bullet` (INDICATOR) |

### DROPDOWN
| strtype | IT | Description |
|---------|:---:|---|
| `DROPDOWN/Dropdown` | 1 | Section header |
| `DROPDOWN/Options` | 10 | Newline-separated options: `"Option 1\nOption 2\nOption 3"` |
| `DROPDOWN/Base_text` | 10 | Static text (overrides selected display) |
| `DROPDOWN/Show_selected` | 2 | Show selected option |
| `DROPDOWN/List_align` | 3 | `"BOTTOM"`, `"TOP"`, `"LEFT"`, `"RIGHT"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR), `Style_list_main` (list MAIN), `Style_list_selected` (list SELECTED) |

### ROLLER
| strtype | IT | Description |
|---------|:---:|---|
| `ROLLER/Roller` | 1 | Section header |
| `ROLLER/Options` | 10 | Newline-separated options |
| `ROLLER/Selected` | 6 | Selected index |
| `ROLLER/Mode` | 3 | `"NORMAL"`, `"INFINITE"` |
| **Style parts:** | | `Style_main` (MAIN), `Style_selected` (SELECTED) |

### TEXTAREA
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

### KEYBOARD
| strtype | IT | Description |
|---------|:---:|---|
| `KEYBOARD/Mode` | 3 | `"TEXT_LOWER"`, `"TEXT_UPPER"`, `"SPECIAL"`, `"NUMBER"` |
| `KEYBOARD/Target_textarea` | 9 | GUID of linked textarea (or `"-"`) |
| **Style parts:** | | `Style_main` (MAIN), `Style_items` (ITEMS) |

### SPINNER
| strtype | IT | Description |
|---------|:---:|---|
| `SPINNER/Spinner` | 1 | Section header |
| **Style parts:** | | `Style_main` (MAIN), `Style_indicator` (INDICATOR) |

### SPINBOX
| strtype | IT | Description |
|---------|:---:|---|
| `SPINBOX/Spinbox` | 1 | Section header |
| `SPINBOX/Value` | 6 | Current value |
| `SPINBOX/Range` | 7 | `[min, max, step]` (3 elements!) |
| `SPINBOX/Digit_format` | 7 | `[total_digits, decimal_digits]` |
| **Style parts:** | | `Style_main` (MAIN), `Style_cursor` (CURSOR) |

### CALENDAR
| strtype | IT | Description |
|---------|:---:|---|
| `CALENDAR/Date` | 7 | `[day, month, year]` |
| **Style parts:** | | `Style_main` (MAIN), `Style_items` (ITEMS) |

### CHART
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

> [!NOTE]
> COLORWHEEL was removed in LVGL 9 (v8 only).

| strtype | IT | Description |
|---------|:---:|---|
| `COLORWHEEL/Mode` | 3 | `"HUE"`, `"SATURATION"`, `"VALUE"` |
| `COLORWHEEL/Fixed_mode` | 2 | Lock mode |
| **Style parts:** | | `Style_main` (MAIN), `Style_knob` (KNOB) |

### TABVIEW
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

## IMAGE Asset Requirements

- Supported format: PNG with alpha channel is the standard (all SLS examples use PNG)
- Directory convention: All assets go in `assets/` at the project root, referenced by relative path (`assets/filename.png`)
- Naming convention: Lowercase, underscores, descriptive (e.g., `icon_battery.png`, `bg_main.png`)
- Recommended icon sizes: 16, 24, 32, 48px for common UI icons on embedded displays
- Recoloring: Monochrome/white icons can be tinted via LVGL style properties (`_style/Bg_Image_Recolor`) — use white source PNGs for maximum flexibility
- Flash/RAM cost: Each pixel costs 2–4 bytes depending on colour depth; a 48×48 RGBA icon ≈ 9 KB. Budget carefully on constrained devices
- IMAGE widget properties quick reference from the catalog above: `IMAGE/Asset` (path, IT=5), `IMAGE/Pivot` (rotation pivot [x,y], IT=7), `IMAGE/Rotation` (0.1° units, IT=6), `IMAGE/Scale` (256 = 100%, IT=6)
