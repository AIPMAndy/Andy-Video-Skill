# User Guide

## Picking the Right Skill

Match your task to a category:

| I want to... | Use category |
|--------------|--------------|
| Create math / AI animations programmatically | 01 Programmatic Animation |
| Convert screen recordings into short-form videos | 02 Recording-to-Video |
| Render React code or HTML pages as MP4 | 03 Code-to-Video |
| Write or validate a viral script | 04 Script & Planning |
| Produce a distinctive hand-crafted explainer | 05 Stylized Effects |

## Workflow

1. Browse the [CATALOG](../../CATALOG.md) to pick a skill
2. Follow [INSTALLATION](../../INSTALLATION.md) to install
3. Restart Claude Code
4. Invoke the skill per its SKILL.md instructions

## Updating a Skill

When a skill has a new release upstream:

```bash
./scripts/update-skill.sh andy-manim-video
```

The script overwrites the local copy from the source path and updates `CHANGELOG.md`.

## Adding a New Skill

```bash
./scripts/new-skill.sh my-new-skill --category 01-programmatic-animation
```

Creates a scaffolded directory under the chosen category with a placeholder `SKILL.md`.
Then populate it and update `CATALOG.md`.