# Installation

Three ways to use this catalog:

## A. Browse Only (No Install)

```bash
git clone https://github.com/AIPMAndy/Andy-Video-Skill.git
cd Andy-Video-Skill
```

Read `SKILL.md` files directly. No code runs.

## B. Install a Single Skill

```bash
# Pick a skill from CATALOG.md, then:
cp -r "Andy-Video-Skill/01-programmatic-animation/andy-manim-video" \
      ~/.claude/skills/
```

Restart Claude Code to load the skill.

## C. Bulk Install All Skills

```bash
cd Andy-Video-Skill
./scripts/install-all.sh
```

The script copies every category's skills into `~/.claude/skills/`. Skip any
skill by passing its directory name as an argument:

```bash
./scripts/install-all.sh --exclude andy-liquid,react-video
```

## Verify Installation

```bash
ls ~/.claude/skills/ | grep andy
```

You should see the installed skills.
