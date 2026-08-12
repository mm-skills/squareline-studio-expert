# LVGL Version Compatibility Guide

SquareLine Studio generates UI project files that target a specific LVGL version.
This guide covers the version-dependent aspects relevant to project generation
and provides pointers for firmware integration.

## Supported LVGL Versions in SLS v1.6.2

| Version | SLS Internal ID | Status |
|---------|----------------|--------|
| 8.3.11 | `lvgl_v8_3_11` | Legacy — still supported for older boards |
| 9.1.0 | `lvgl_v9_1_0` | Supported |
| 9.2.2 | `lvgl_v9_2_2` | Current default in bundled examples |
| 9.3 | `lvgl_v9_3` | Supported |
| 9.5 | `lvgl_v9_5` | Latest — added in SLS 1.6.2, 84 boards |

> [!TIP]
> All 15 bundled SLS example projects still use LVGL 9.2.2. However, 84 board packs now target LVGL 9.5 as of SLS v1.6.2.

## How the Version Is Determined

1. **Board definition** — Each `.slb` board file has a `supported_lvgl_version` field
   (e.g., `"9.3"`, `"8.3.*"`). When you select a board in SLS, it sets the project
   LVGL version automatically.
2. **Project metadata** — The `.sll` file stores the version in `"lvgl_version"`,
   and the `.spj` `info` block mirrors it. Both must be consistent.
3. **Code generation** — SLS uses version-specific internal templates to generate
   C and MicroPython code with the correct LVGL API calls.

## Board Version Distribution

| LVGL Version | Board Count | Notable Boards |
|---|---|---|
| 8.2.0 / 8.3.* | 11 | ESP32-S3-LCD-EV-BOARD, i.MX RT595 EVK, Eclipse SDL |
| 9.1.* | 8 | CrowPanel PICO 3.5", ESP WROVER KIT, ESP-BOX |
| 9.2.* | 3 | MaTouch 4" 480×480 |
| 9.3 | 11 | Arduino TFT_eSPI, MaTouch 3.5", M5Stack, CrowPanel displays |
| 9.5 | 84 | Arduino TFT_eSPI, CrowPanel (all sizes incl. 1.28"), MaTouch, M5Stack, Espressif, Renesas, Nuvoton, Raspberry Pi |

> [!IMPORTANT]
> As of SLS 1.6.2, the majority of board packs (84) now target **LVGL 9.5**. Default to **9.5** for new projects unless the user specifies a specific version.

## SPJ Format Differences (Minimal)

The `.spj` widget tree, event structures, and Call/CallC templates are **largely
identical** across LVGL v8 and v9. Note that v9.5 introduces a CHANGE SCREEN Call/CallC template change: `lv.SCR_LOAD_ANIM` → `lv.SCREEN_LOAD_ANIM` (Python) and `LV_SCR_LOAD_ANIM_` → `LV_SCREEN_LOAD_ANIM_` (C). Key differences:

### Widget Availability

| Widget | LVGL v8 | LVGL v9 | Notes |
|--------|:---:|:---:|---|
| COLORWHEEL | ✅ | ❌ | Removed in v9. Do not use for v9 projects. |
| CONTAINER | ✅ | ✅ | LVGL 9.x alias for PANEL. Preferred over PANEL in v9. |
| IMGBUTTON | ✅ | ✅ | Available in SLS for both, though underlying LVGL API deprecated in v9. |

### `.sll` Version String

The `lvgl_version` field must match the board's `supported_lvgl_version`:
```json
"lvgl_version": "9.2.2"     // v9 project
"lvgl_version": "8.3.11"    // v8 project
```

### Event Call/CallC Templates

All event action templates (CHANGE SCREEN, CALL FUNCTION, INCREMENT ARC, etc.)
are **identical** in the SPJ file regardless of LVGL version. SLS handles the
version-specific code generation internally when exporting. Note that LVGL 9.5 changes the CHANGE SCREEN Call/CallC templates from `SCR_LOAD_ANIM` to `SCREEN_LOAD_ANIM`. Other action templates are identical.

## Code Generation Differences (Awareness)

When SLS exports C or MicroPython code, the output uses version-specific LVGL
APIs. This matters when writing custom event handlers (`ui_events.c`) or
integrating the generated UI with firmware drivers.

### Key API Renames (v8 → v9)

| Category | LVGL v8 | LVGL v9 |
|----------|---------|--------|
| Widget creation | `lv_btn_create()`, `lv_img_create()` | `lv_button_create()`, `lv_image_create()` |
| Active screen | `lv_scr_act()` | `lv_screen_active()` |
| Screen load anim | `LV_SCR_LOAD_ANIM_*` | `LV_SCREEN_LOAD_ANIM_*` |
| Load screen | `lv_scr_load_anim()` | `lv_screen_load_anim()` |
| Event binding | `lv_obj_add_event_cb()` | `lv_obj_add_event()` |
| Clear flag | `lv_obj_clear_flag()` | `lv_obj_remove_flag()` |
| Clear state | `lv_obj_clear_state()` | `lv_obj_remove_state()` |
| Memory | `lv_mem_alloc()` | `lv_malloc()` |
| Style constants | `LV_STYLE_BG_IMG_RECOLOR` | `LV_STYLE_BG_IMAGE_RECOLOR` |
| Image format | `LV_IMG_CF_TRUE_COLOR_ALPHA` | `LV_COLOR_FORMAT_NATIVE_WITH_ALPHA` |
| Display driver | `lv_disp_drv_t` struct | `lv_display_create()` function |
| Coord type | `lv_coord_t` | `int32_t` (type removed) |

> [!NOTE]
> These API differences affect the **exported C code** and your **custom firmware**,
> not the `.spj`/`.sll`/`.slt` project files this skill generates. The skill
> focuses on producing correct project files that SLS can open.

### External References

For detailed LVGL API migration guidance:
- [LVGL v9 Migration Guide](https://docs.lvgl.io/9.2/intro/migration_guide.html)
- [LVGL v9.5 API Reference](https://docs.lvgl.io/9.5/)
- [LVGL v9 API Reference](https://docs.lvgl.io/9.2/)
- [LVGL v8 API Reference](https://docs.lvgl.io/8.4/)
- [SquareLine Studio v9 Support Announcement](https://squareline.io/blog)

## Choosing a Version

| Scenario | Recommended LVGL Version |
|----------|-------------------------|
| New project, no board selected yet | **9.5** (matches SLS examples) |
| Specific board selected | Use the board's `supported_lvgl_version` |
| Migrating an existing v8 project | Keep v8 unless re-exporting all code |
| Using COLORWHEEL widget | Must use **v8** |
| Using SDL desktop simulator | v9.5 (latest CMake/SDL board) |
| CrowPanel 1.28" round | **9.5** (CrowPanel-specific board available) |
