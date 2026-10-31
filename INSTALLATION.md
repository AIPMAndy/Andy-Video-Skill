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

## Unified video orchestration

Installing this repo normally includes **13 local Skills**, including the Andy Video Director. The additional 22-source registry is **not** a claim that 22 engines are installed.

```bash
./scripts/install-all.sh
python3 00-orchestration/andy-video-director/director.py plan --request "为我的产品做视频"
python3 00-orchestration/andy-video-director/director.py doctor
```

To **explicitly opt in** to staging complete, reviewed and commit-pinned upstream Agent Skill packages (BB-Video's full renderer and 30 visual styles, MoneyPrinterTurbo and Remotion official Agent Skills):

```bash
./scripts/install-all.sh --with-upstreams
# Or install just BB-Video:
python3 00-orchestration/andy-video-director/director.py bootstrap bb-video --execute
```

Pinned bootstrap copies upstream source only. It does **not** install npm/Python dependencies, download model weights, configure providers or produce a finished video. Read upstream instructions, confirm cost/privacy/licenses and use the agent to run the selected runtime and QA.
