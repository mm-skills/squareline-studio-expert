# Font Documentation

This document covers font handling and requirements in SquareLine Studio.

## Built-in Montserrat Sizes

SquareLine Studio includes built-in support for the Montserrat font at specific even-numbered sizes. 
There are 21 sizes available in total: 8 to 48.

| Size | Font Name | LVGL Config |
|---|---|---|
| 8 | montserrat_8 | LV_FONT_MONTSERRAT_8 |
| 10 | montserrat_10 | LV_FONT_MONTSERRAT_10 |
| 12 | montserrat_12 | LV_FONT_MONTSERRAT_12 |
| 14 | montserrat_14 | LV_FONT_MONTSERRAT_14 |
| 16 | montserrat_16 | LV_FONT_MONTSERRAT_16 |
| 18 | montserrat_18 | LV_FONT_MONTSERRAT_18 |
| 20 | montserrat_20 | LV_FONT_MONTSERRAT_20 |
| 22 | montserrat_22 | LV_FONT_MONTSERRAT_22 |
| 24 | montserrat_24 | LV_FONT_MONTSERRAT_24 |
| 26 | montserrat_26 | LV_FONT_MONTSERRAT_26 |
| 28 | montserrat_28 | LV_FONT_MONTSERRAT_28 |
| 30 | montserrat_30 | LV_FONT_MONTSERRAT_30 |
| 32 | montserrat_32 | LV_FONT_MONTSERRAT_32 |
| 34 | montserrat_34 | LV_FONT_MONTSERRAT_34 |
| 36 | montserrat_36 | LV_FONT_MONTSERRAT_36 |
| 38 | montserrat_38 | LV_FONT_MONTSERRAT_38 |
| 40 | montserrat_40 | LV_FONT_MONTSERRAT_40 |
| 42 | montserrat_42 | LV_FONT_MONTSERRAT_42 |
| 44 | montserrat_44 | LV_FONT_MONTSERRAT_44 |
| 46 | montserrat_46 | LV_FONT_MONTSERRAT_46 |
| 48 | montserrat_48 | LV_FONT_MONTSERRAT_48 |

## Custom Fonts

Custom fonts can be added via the Font Manager in SquareLine Studio (TTF → generated font).
The naming convention for custom fonts is the `ui_font_<Name>` prefix.

## LVGL Dependency

Each built-in size used in a project requires its corresponding `LV_FONT_MONTSERRAT_XX` define to be enabled in `lv_conf.h` at firmware build time (e.g., `#define LV_FONT_MONTSERRAT_14 1`). Custom fonts must be declared using `LV_FONT_DECLARE(ui_font_<Name>)`.

## Common Gotchas

> [!WARNING]
> - **No odd sizes**: Do not use odd sizes for built-in Montserrat (e.g., `montserrat_15`).
> - **Max size**: Nothing above 48 without using the Font Manager for a custom font.
> - **Custom names**: Don't use the "montserrat" prefix for your custom fonts to avoid collisions and confusion.

## Font Properties in Widgets

In widget styles, fonts are represented by InheritedType 17 (`fontval`). 
They are referenced via `_style/Text_Font` (InheritedType 3) in the styles structure.
