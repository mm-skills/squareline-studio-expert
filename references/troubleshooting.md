# Troubleshooting & Debugging

Guidance for diagnosing issues with SquareLine Studio projects and the
generated LVGL firmware code.

## 1. SLS Application Logs

### Via the UI (v1.5.0+)

Navigate to **File → Show log file** in the SLS top menu to view the live
application log. This shows engine errors, asset loading issues, and memory
diagnostics that the standard UI console filters out.

### Raw Log File Locations

SquareLine Studio is built on the Unity engine and writes detailed diagnostics
to `Player.log`. If SLS freezes or fails to launch, retrieve the log manually:

| OS | Path |
|---|---|
| **macOS** | `~/Library/Logs/unity3d/SquareLine Kft_/SquareLine_Studio/Player.log` |
| **Windows** | `C:\Users\<username>\AppData\LocalLow\SquareLine Kft_\SquareLine_Studio\Player.log` |
| **Linux** | `~/.config/unity3d/SquareLine Kft_/SquareLine_Studio/Player.log` |

> [!TIP]
> On Windows, `AppData` is hidden by default. Press **Win + R**, type `%appdata%`,
> and navigate one folder up to find `LocalLow`.

### What to Look For

| Symptom | Look for in `Player.log` |
|---------|-------------------------|
| Project won't open | JSON parse errors, missing file references |
| Widget missing after load | `saved_objtypeKey` mismatches, unknown widget type errors |
| Asset import crash | Image format errors, memory allocation failures |
| Code export failure | Template resolution errors, path permission issues |
| SLS freeze/hang | Memory spikes, infinite loop warnings |

## 2. LVGL Runtime Debugging

If UI components behave incorrectly at runtime (wrong animations, style
glitches, layout failures, memory issues), the problem usually stems from the
LVGL library layer rather than the SLS project files.

### Enable LVGL Logging

In your exported project's `lv_conf.h`:

```c
/* Enable LVGL internal logging */
#define LV_USE_LOG 1

/* Set log verbosity — choose one: */
#define LV_LOG_LEVEL LV_LOG_LEVEL_WARN    /* Warnings and errors only */
// #define LV_LOG_LEVEL LV_LOG_LEVEL_INFO  /* + informational messages */
// #define LV_LOG_LEVEL LV_LOG_LEVEL_TRACE /* Exhaustive — every operation logged */
```

> [!NOTE]
> `LV_LOG_LEVEL_TRACE` generates very high output volume and can slow down
> embedded targets. Use it for targeted debugging sessions, not production builds.

### Common LVGL Runtime Issues

| Symptom | Likely Cause | What to Check |
|---------|-------------|---------------|
| Widget not visible | Wrong parent, zero size, hidden flag | `LV_OBJ_FLAG_HIDDEN`, widget dimensions |
| Style not applied | Wrong part or state selector | Style part mapping in `references/format/styles-states.md` |
| Crash on screen change | Invalid screen GUID, missing `_screen_init` | Event `Screen_to` references valid screen |
| Memory allocation failure | Too many widgets or large assets | Reduce widget count, compress images, increase `LV_MEM_SIZE` |
| Font missing warning | Using non-built-in font size | Only even sizes 8–48 are built-in (see `references/format/fonts.md`) |
| Touch not responding | Input driver misconfigured | Check `lv_indev` setup matches LVGL version (v8 vs v9 API differs) |

### Serial Monitor Setup

For ESP32/Arduino targets, LVGL log output goes to the serial console:

```
Tools → Serial Monitor (115200 baud)
```

For PlatformIO:
```bash
pio device monitor -b 115200
```

## 3. Project File Debugging

When a generated `.spj` file won't open in SLS or widgets are missing:

1. **Validate first** — run `scripts/validate_project.py /path/to/project/`
2. **Check GUID uniqueness** — duplicate GUIDs cause silent widget drops
3. **Verify nidcnt** — must exceed the highest `nid` in the project
4. **Check `.sll` ↔ `.spj` info consistency** — version, resolution, board must match
5. **Inspect JSON syntax** — use `python3 -m json.tool < file.spj` to find parse errors

## 4. SLS Canvas-Edit Name Corruption

SLS regenerates `OBJECT/Name` values for widgets that are edited on the canvas
(moved, resized, restyled) when the project is saved. The regenerated name
**strips underscores** — e.g., `wsrIdle_temp` → `wsrIdletemp` — because SLS's
internal naming template concatenates tokens without separators
(`need_separator: false` in all widget descriptors).

| Symptom | Cause | Fix |
|---------|-------|-----|
| Firmware compile fails with undefined `ui_<name>` symbols after SLS Save | SLS stripped underscores from canvas-edited widget names | Run `scripts/check_names.py --baseline <file> --fix` to restore names |
| Widget names lost underscores after Save | SLS name regeneration on "dirty" widgets | Use camelCase naming to avoid the issue entirely |
| Some widgets on a screen lost underscores, others didn't | Only canvas-edited ("dirty") widgets are regenerated | Only manipulated widgets are affected |

**Prevention:** Use camelCase for all firmware-bound widget names. See
SKILL.md anti-pitfall rule #24.

**Detection & Recovery:** Use `scripts/check_names.py`:
```bash
# Save a baseline before opening in SLS
python3 scripts/check_names.py /path/to/project/ --save-baseline names.json

# After SLS Save, check for changes
python3 scripts/check_names.py /path/to/project/ --baseline names.json

# Restore stripped names
python3 scripts/check_names.py /path/to/project/ --baseline names.json --fix
```

## External References

- [SLS Troubleshooting Guide](http://docs.squareline.io/docs/miscellanos/troubleshooting/)
- [SLS Changelog (v1.5.0+ log viewer)](http://docs.squareline.io/docs/miscellanos/changelog/)
- [LVGL Debugging Guide](https://docs.lvgl.io/9.2/overview/debugging.html)
- [SLS Forum — Troubleshooting](https://forum.squareline.io/)
