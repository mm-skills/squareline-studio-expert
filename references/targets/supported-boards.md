# Supported Boards — Dynamic Discovery

SquareLine Studio supports boards from multiple manufacturers. Board definitions
are **not hardcoded** in this skill — instead, extract them dynamically from the
user's local SLS installation to ensure accuracy and freshness.

## How to Find Board Definitions

### Quick: Run the extraction script
```bash
python3 scripts/extract_boards.py                  # Uses cache, or extracts + caches
python3 scripts/extract_boards.py --refresh        # Force re-extract from .slb files
python3 scripts/extract_boards.py --group Elecrow  # Filter by manufacturer
python3 scripts/extract_boards.py --board "MaTouch" # Search by board name
python3 scripts/extract_boards.py --json           # Raw JSON output
```

The script caches results to `scripts/.board_cache.json` on first run.
Subsequent runs read from cache (no filesystem traversal, no permission prompts).
Use `--refresh` after installing new boards in SLS.

### Manual: Read .slb files directly
Board definitions are `.slb` files (JSON format) stored in two locations:

| Location | Contents |
|---|---|
| `~/SquareLine/boards/<Group>/<board_id>/` | Downloaded boards (most boards) |
| `/Applications/SquareLine_Studio.app/Contents/boards/` | Bundled boards (macOS) |

Each `.slb` file contains:
```json
{
    "version": "v2.3.0",
    "group": "Elecrow",
    "title": "DIS01728A-1 - ESP32-S3 2.8inch HMI Display ...",
    "width": 320,
    "height": 240,
    "shape": "rectangle",
    "color_depth": "16",
    "supported_lvgl_version": "9.3",
    "language": "C",
    "lvgl_export_path": "./components/ui/",
    "lvgl_include_path": "lvgl.h",
    "url": "https://github.com/...",
    "short_description": "...",
    "long_description": "..."
}
```

The `title` field is the exact string to use in the `.sll` `board` field.

## Manufacturer Groups

SLS v1.6.1 organises boards into these tabs:

| Group | Examples |
|---|---|
| **Arduino** | Arduino with TFT_eSPI, GIGA R1 WiFi |
| **Desktop** | SDL simulators for PC development |
| **Elecrow** | CrowPanel HMI displays (2.4"–7.0") |
| **Espressif** | ESP32-S2/S3 dev kits (Kaluga, EYE, BOX, WROVER) |
| **M5Stack** | Core2, Dial (round), Tab5 (1280×720), M5StickC |
| **Makerfabs** | MaTouch displays (1.9"–4.0", 2.1" Rotary) |
| **NXP** | i.MX RT1064/RT595 EVK boards |

## Circular Displays

Look for `"shape": "circle"` in the `.slb` file. Known circular boards include
M5Stack Dial (240×240), MaTouch 2.1" Rotary (480×480), and i.MX RT595 (392×392).
The generic Arduino TFT_eSPI board can also be set to circle manually.

## Key Fields for Project Generation

When generating a project for a specific board, copy these fields from the `.slb`
into the `.sll` and `.spj` info block:

| .slb field | Maps to .sll field |
|---|---|
| `title` | `board` |
| `version` | `board_version` |
| `width` | `width` |
| `height` | `height` |
| `shape` | `shape` (uppercase: `"RECTANGLE"` or `"CIRCLE"`) |
| `lvgl_include_path` | `lvgl_include_path` |
| `supported_lvgl_version` | Use to pick `lvgl_version` (e.g., `"9.3"` → `"9.3.0"`) |

> [!WARNING]
> The `board` string in `.sll` must **exactly match** the `title` field from the
> `.slb` file. A mismatch causes SLS to show "Custom Board" in project info and
> may cause SLS to **fall back to v8 code generation** on export, even if
> `lvgl_version` is set to a v9 version. Always verify the board string against
> the installed `.slb` board packs.

> [!NOTE]
> The `.slb` `shape` uses lowercase (`"rectangle"`, `"circle"`), but the `.sll`
> uses uppercase (`"RECTANGLE"`, `"CIRCLE"`). Transform on copy.
