# ESP32 CrowPanel Configuration

Board-specific configuration for Elecrow CrowPanel displays with ESP32/ESP32-S3.

## CrowPanel 1.28" Round (240×240)

As of SLS 1.6.2, Elecrow provides **dedicated CrowPanel 1.28" board packs** — use
these instead of the generic `"Arduino with TFT_eSPI"` board.

| Parameter | Value (Arduino-IDE) | Value (ESP-IDF) |
|-----------|---|---|
| **Board** | `"CrowPanel 1.28" HMI ESP32-S3 Rotary Display 240x240 - Arduino-IDE"` | `"CrowPanel 1.28" HMI ESP32 Rotary Display - ESP-IDF"` |
| **Board Version** | `"v2.5.0"` | `"v2.5.0"` |
| **Width** | `240` | `240` |
| **Height** | `240` | `240` |
| **Shape** | `"CIRCLE"` | `"CIRCLE"` |
| **LVGL Version** | `"9.5"` | `"9.5"` |
| **LVGL Include** | `"lvgl.h"` | `"lvgl.h"` |
| **Editor Version** | `"1.6.2"` | `"1.6.2"` |
| **Color Depth** | 16-bit (RGB565) | 16-bit (RGB565) |

> [!TIP]
> The generic `"Arduino with TFT_eSPI"` board (v2.3.0+) still works but the
> dedicated CrowPanel boards include optimised export templates for the specific
> hardware. Prefer the dedicated board when available.

### Script Command
```bash
python3 scripts/generate_project.py \
  --name "CrowPanel_128" \
  --width 240 --height 240 \
  --shape CIRCLE \
  --board "CrowPanel 1.28\" HMI ESP32-S3 Rotary Display 240x240 - Arduino-IDE" \
  --board-version "v2.5.0" \
  --lvgl-version "9.5" \
  --output ./my_project/
```

### Design Considerations for Round Displays

1. **Usable area is circular** — corners of the 240×240 pixel area are not visible.
   The inscribed circle has a diameter of 240px, but practical UI should stay within
   ~200px diameter to avoid edge clipping.

2. **Center alignment** — use `"Align": "CENTER"` for most widgets to keep them
   within the visible circle.

3. **Widget placement zones** (relative to center):
   - **Safe zone**: ±85px from center (170px diameter) — fully visible
   - **Caution zone**: ±85–110px — partially visible depending on bezel
   - **Clip zone**: >±110px — will be clipped by the circular mask

4. **Arc widget is ideal** — the ARC widget follows the circular display shape
   naturally. Use `Bg_angles: [135, 45]` for a standard 270° sweep.

5. **Avoid wide horizontal elements** — sliders, bars, and text labels wider than
   ~170px will extend into the clip zone. Consider using vertical layouts or
   smaller widgets.

6. **Navigation** — with limited screen space, use screen transitions (CHANGE SCREEN)
   rather than trying to fit navigation buttons. Consider swipe gestures or
   rotary encoder input.

7. **Font size** — use `montserrat_14` or larger for readability on small displays.
   `montserrat_10` is too small for primary content.

## CrowPanel Pico 2.4" (320×240)

| Parameter | Value |
|-----------|-------|
| **Board** | `"DIS09024P - CrowPanel Pico 2.4inch Display - Arduino-IDE"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `320` |
| **Height** | `240` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 3.5" (480×320)

| Parameter | Value |
|-----------|-------|
| **Board** | `"DIS01135P - CrowPanel PICO HMI 3.5inch Display - Arduino-IDE"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `480` |
| **Height** | `320` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 5.0" (800×480)

| Parameter | Value |
|-----------|-------|
| **Board** | `"CrowPanel Advance 5.0 ESP32-P4 HMI - ESP-IDF"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `800` |
| **Height** | `480` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 7.0" (800×480)

| Parameter | Value |
|-----------|-------|
| **Board** | `"CrowPanel Advance 7.0 HMI - ESP-IDF"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `800` |
| **Height** | `480` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 1.46" Round (360×360)

| Parameter | Value |
|-----------|-------|
| **Board** | `"CrowPanel 1.46" HMI ESP32 Rotary Display - ESP-IDF"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `360` |
| **Height** | `360` |
| **Shape** | `"CIRCLE"` |

## CrowPanel 2.1" Round (480×480)

| Parameter | Value |
|-----------|-------|
| **Board** | `"CrowPanel 2.1" ESP32 Rotary Display - ESP-IDF"` |
| **Board Version** | `"v2.5.0"` (LVGL 9.5) |
| **Width** | `480` |
| **Height** | `480` |
| **Shape** | `"CIRCLE"` |

> [!NOTE]
> As of SLS 1.6.2, most CrowPanel models have dedicated board packs targeting
> LVGL 9.5. The generic `"Arduino with TFT_eSPI"` board still works as a
> fallback. Round displays (1.28", 1.46", 2.1") require `shape: "CIRCLE"`.

