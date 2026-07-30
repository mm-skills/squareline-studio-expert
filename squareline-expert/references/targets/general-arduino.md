# General Arduino Board Configuration

Generic configuration for Arduino-based boards using LVGL with TFT displays.

## Common Board Strings

| Board | Typical Displays |
|-------|-----------------|
| `"Arduino with TFT_eSPI"` | Most ESP32 + TFT displays (ILI9341, ST7789, etc.) |
| `"Custom Board"` | Any board — requires manual driver setup |

## Default Configuration

| Parameter | Value |
|-----------|-------|
| **Board** | `"Custom Board"` |
| **Board Version** | `"v1.0.0"` |
| **Shape** | `"RECTANGLE"` |
| **LVGL Version** | `"8.3.11"` |
| **LVGL Include** | `"lvgl.h"` |
| **Editor Version** | `"1.6.1"` |
| **Color Depth** | 16-bit (RGB565) |

### Script Command
```bash
python3 scripts/generate_project.py \
  --name "MyProject" \
  --width 320 --height 240 \
  --board "Custom Board" \
  --lvgl-version "8.3.11" \
  --output ./my_project/
```

## Common Display Resolutions

| Display | Width | Height | Notes |
|---------|:-----:|:------:|-------|
| 1.28" round | 240 | 240 | Shape: CIRCLE |
| 1.3" TFT | 240 | 240 | ST7789 |
| 1.8" TFT | 160 | 128 | ST7735 |
| 2.0" TFT | 320 | 240 | ILI9225 |
| 2.4" TFT | 320 | 240 | ILI9341 |
| 2.8" TFT | 320 | 240 | ILI9341 |
| 3.2" TFT | 320 | 240 | ILI9341 |
| 3.5" TFT | 480 | 320 | ILI9488 |
| 4.3" TFT | 480 | 272 | Various |
| 5.0" TFT | 800 | 480 | Various |
| 7.0" TFT | 800 | 480 | Various |

## LVGL Version Compatibility

| SLS Version | Default LVGL | Notes |
|:-----------:|:------------:|-------|
| 1.5.x | 8.3.6 | Older nid format, no project.info |
| 1.6.x | 8.3.11 | Sequential nids, project.info, info block in .spj |

## Post-Export Integration Notes

After exporting from SLS, the generated code needs:

1. **Display driver init** — `lv_disp_drv_init()` with correct resolution and buffer
2. **Input driver** — touch controller registration via `lv_indev_drv_register()`
3. **Timer handler** — call `lv_timer_handler()` in your main loop (Arduino `loop()`)
4. **Memory** — LVGL needs at least 32KB heap; ESP32 typically has 320KB+ available
5. **Thread safety** — on dual-core ESP32, never touch LVGL objects from a non-LVGL
   task without taking the LVGL mutex

> [!WARNING]
> When using `"Custom Board"`, SLS exports generic code without board-specific
> display initialisation. You must provide your own display driver setup.
> Using `"Arduino with TFT_eSPI"` generates TFT_eSPI-compatible init code.
