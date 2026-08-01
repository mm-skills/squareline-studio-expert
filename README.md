# SquareLine Studio Expert Skill

An AI skill for generating [SquareLine Studio](https://squareline.io/) project files programmatically. Produces valid `.spj`, `.sll`, and `.slt` files that open correctly in SLS v1.5+ and generate working LVGL UI code for embedded displays (ESP32, STM32, etc.).

## Features

- **Programmatic project generation** — scaffold complete SLS projects from the command line or via AI agent
- **Widget builder API** — Python helpers for constructing widgets with correct GUIDs, nid tracking, styles, and events
- **Validation** — automated checks for GUID uniqueness, nidcnt consistency, required properties, and free-tier limits
- **Reference library** — comprehensive docs on file format, widget catalog, events, styles, UX patterns, and board targets
- **Board support** — CrowPanel, MaTouch, and generic Arduino board configurations

## Installation

### As an Antigravity / Gemini skill (via git submodule)

Add this repo as a submodule in your project's skill directory:

```bash
git submodule add https://github.com/your-org/squareline-studio-skill.git .agents/skills/squareline-expert
```

To update to the latest version:

```bash
git submodule update --remote .agents/skills/squareline-expert
```

After cloning a project that includes this submodule:

```bash
git submodule init
git submodule update
```

### Manual installation

Copy or symlink this repo into your skill directory:

```bash
ln -s /path/to/squareline-studio-skill ~/.gemini/config/skills/squareline-expert
```

## Usage

Once installed, the skill is triggered by mentions of SquareLine Studio, SLS projects, LVGL UI, ESP32 displays, CrowPanel, or related terms. See [SKILL.md](SKILL.md) for full agent instructions.

### Standalone script usage

Generate a project scaffold:

```bash
python3 scripts/generate_project.py \
  --name "MyProject" \
  --width 480 --height 320 \
  --board "ESP32S335D - MaTouch 3.5-inch Parallel 480x320 TFT with Touch - Arduino-IDE" \
  --screens 3 \
  --output /path/to/output/
```

Validate a generated project:

```bash
python3 scripts/validate_project.py /path/to/project/
```

## Repository Structure

```
├── SKILL.md              # Agent-facing skill instructions
├── references/           # Format specs, widget docs, UX patterns, board configs
├── scripts/              # Python tools (generator, validator, widget helpers)
├── docs/                 # Additional reference documentation
└── README.md             # This file
```

## Contributing

See [references/contribution-protocol.md](references/contribution-protocol.md) for contribution guidelines and [references/issue-management.md](references/issue-management.md) for bug reporting.

## License

See project license file for details.
