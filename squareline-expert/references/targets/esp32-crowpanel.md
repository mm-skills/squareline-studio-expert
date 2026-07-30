# ESP32 CrowPanel Configuration

Board-specific configuration for Elecrow CrowPanel displays with ESP32-S3.

## CrowPanel 1.28" Round (240×240)

| Parameter | Value |
|-----------|-------|
| **Board** | `"Arduino with TFT_eSPI"` |
| **Board Version** | `"v1.1.1"` |
| **Width** | `240` |
| **Height** | `240` |
| **Shape** | `"CIRCLE"` |
| **LVGL Version** | `"8.3.6"` |
| **LVGL Include** | `"lvgl.h"` |
| **Editor Version** | `"1.5.0"` (original) or `"1.6.1"` (current) |
| **Color Depth** | 16-bit (RGB565) |

### Script Command
```bash
python3 scripts/generate_project.py \
  --name "CrowPanel_128" \
  --width 240 --height 240 \
  --shape CIRCLE \
  --board "Arduino with TFT_eSPI" \
  --board-version "v1.1.1" \
  --lvgl-version "8.3.6" \
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

## CrowPanel 2.8" (320×240)

| Parameter | Value |
|-----------|-------|
| **Width** | `320` |
| **Height** | `240` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 3.5" (480×320)

| Parameter | Value |
|-----------|-------|
| **Width** | `480` |
| **Height** | `320` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 5.0" (800×480)

| Parameter | Value |
|-----------|-------|
| **Width** | `800` |
| **Height** | `480` |
| **Shape** | `"RECTANGLE"` |

## CrowPanel 7.0" (800×480)

| Parameter | Value |
|-----------|-------|
| **Width** | `800` |
| **Height** | `480` |
| **Shape** | `"RECTANGLE"` |

> [!NOTE]
> All CrowPanel models use ESP32-S3 with TFT_eSPI driver. The board string
> `"Arduino with TFT_eSPI"` works for all sizes. The 1.28" round model is the
> only one requiring `shape: "CIRCLE"`.
