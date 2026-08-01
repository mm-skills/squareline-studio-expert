# Image Asset Sources

This document catalogs where to find image assets for SquareLine Studio projects.

## 1. SLS Built-in Example Projects

The primary source for assets, installed with SquareLine Studio.
Path: `/Applications/SquareLine_Studio.app/Contents/examples/`

| Example Project | Asset Count | Best For |
|---|---|---|
| `Caffee_Machnine_800x480` | 85 | UI icons, buttons, backgrounds, decorative elements |
| `SmartWatch_392x392` | 49 | Clock hands, weather icons, health icons, circular UI |
| `3d_Printer_2_1024x600` | 41 | Status icons, backgrounds, settings icons |
| `Futuristic_Ebike_480x272` | 36 | Gauge elements, speed/battery icons, status indicators |
| `EV_Charger_800x480` | 33 | Charging icons, plug animations, status backgrounds |
| `3d_Printer_800x480` | 30 | Printer-specific icons plus general UI |
| `Audio_mixer_480x800` | 18 | Audio controls, sliders, mixer UI |
| `Smart_Gadget_240x320` | 18 | Weather icons, clock hands, album art |
| `Medical_272x480` | 12 | Medical device icons, circular display elements |
| `POS_272x480` | 10 | Arrow icons, crypto/payment icons, QR codes |

Common reusable icons across examples: `arrow.png`, `ok.png`, `icn_settings.png`, `phone.png`, `light.png`.

## 2. CrowPanel Reference Assets

The skill's research directory contains 353 CrowPanel-specific assets at `research/crowpanel_1_28_reference/assets/`:
- Device control icons, power indicators, status bars
- Light/brightness controls, appliance UI elements
- Available at multiple resolutions (@2x, @3x variants)

## 3. LVGL Built-in Demo Assets

LVGL's demo applications include icon sets in `lvgl/demos/`. Available when LVGL is installed via PlatformIO or the SLS export.

## 4. Generating Assets with Gemini

For project-specific icons:
- Request monochrome/white-on-transparent PNG icons at target resolution
- Describe purpose and style (e.g. "48×48 white outline flame icon on transparent background")
- Generated icons can be tinted at runtime via LVGL recoloring

## 5. Usage Guidance

- Copy assets into your project's `assets/` directory — don't reference from SLS install path
- Resize to target display requirements
- Prefer monochrome white-on-transparent PNGs for runtime tinting
- Full-colour PNGs for backgrounds and decorative elements
