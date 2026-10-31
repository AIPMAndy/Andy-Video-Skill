<div align="center">

# Andy-Video-Skill

**One video request. 13 local Skills, unified routing across 22 verified video-related source entries.**

A curated catalog of 13 Skills for Claude Code that turn your AI agent into a video production studio — 3Blue1Brown animations, viral shorts, React-to-MP4, paper-collage explainers, and more.

[Live Showcase](https://AIPMAndy.github.io/Andy-Video-Skill/) · [Quick Start](#-quick-start-3-minutes) · [中文文档](./README.zh-CN.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/AIPMAndy/Andy-Video-SKill.svg)](https://github.com/AIPMAndy/Andy-Video-SKill/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/AIPMAndy/Andy-Video-SKill.svg)](https://github.com/AIPMAndy/Andy-Video-SKill/commits/main)
[![Skills](https://img.shields.io/badge/skills-13-blueviolet)](#-5-categories-12-skills-1-install)
[![Categories](https://img.shields.io/badge/categories-6-blue)](#-5-categories-12-skills-1-install)

![Hero — 13 Skills across 6 categories, one install command](./showcase/assets/images/hero.png)

</div>

---

## Why this exists

If you've tried to make videos with Claude Code, you already know the pain:

- **Manim** is powerful but ships with 80+ pages of docs and a steep curve
- **React Video** needs Playwright + FFmpeg wrangling on every change
- **Screencast-to-viral** means memorizing ffmpeg's filter graph
- **Paper-collage explainers** require hand-tuned Canvas math
- Each one is a week of trial and error before your first render

**Andy-Video-Skill puts 13 video workflows a single `cp -r` away.** Every Skill here was stress-tested in a real production video release — none of them are toy demos.

---

## 6 categories · 13 Skills · 1 install

| # | Category | Skills | What it unlocks |
|---|----------|:------:|-----------------|
| 00 | **Video Orchestration** | 1 | One natural-language request → dispatch to appropriate video engine; reviewed full BB-Video, Remotion and MoneyPrinterTurbo Skill packages on demand |
| 01 | **Programmatic Animation** | 4 | 3Blue1Brown math · p5.js generative · Three.js liquid metal · Matrix text rain |
| 02 | **Recording-to-Video** | 1 | Long recordings → 100+ platform-native viral shorts |
| 03 | **Code-to-Video** | 3 | React components → MP4 · Apple-style knowledge pages · AI producer |
| 04 | **Script & Planning** | 3 | Hook diagnosis · copy-and-learn templates · YouTube methodology |
| 05 | **Stylized Effects** | 1 | Hand-crafted paper-collage explainer style |

> **Featured: `andy-screencast-to-viral`** — turn a 2-hour screencast into 100+ ready-to-publish short videos with auto-generated captions, hook frames, and platform-specific cuts.

![Screencast-to-Viral detail](./showcase/assets/images/detail-screencast.png)

---

## 🚀 Quick Start (3 minutes)

**Featured: [andy-video-director](./00-orchestration/andy-video-director/)** — a unified Agent Skill router with executable preflight, reviewed/pinned upstream install and real engine handoff. It can stage BB-Video's full renderer and all **30 styles**, MoneyPrinterTurbo and 12 official Remotion Agent Skills. The 22-item source registry is **not** 22 preinstalled engines or proof that every backend was rendered successfully.

```bash
python3 00-orchestration/andy-video-director/director.py plan --request "Make a launch video for my AI product"
# Optional explicit upstream install: ./scripts/install-all.sh --with-upstreams
```


```bash
# 1. Clone the catalog
git clone https://github.com/AIPMAndy/Andy-Video-SKill.git
cd Andy-Video-SKill

# 2. Install ALL skills into Claude Code
./scripts/install-all.sh

# 3. Restart Claude Code, then ask:
#    "Use andy-manim-video to explain attention mechanism."
```

Want just one Skill?

```bash
cp -r 01-programmatic-animation/andy-manim-video ~/.claude/skills/
```

That's it. Restart Claude Code and the Skill is live.

---

## Killer Feature — real output, real production

One frame from `andy-manim-video` rendering "AI Redeem" — a real production we shipped:

![Manim output frame — Directors Cut](./showcase/assets/images/killer-feature-manim.png)

Same Skill, social-platform cut:

![Manim output frame — Social Cut](./showcase/assets/images/killer-feature-manim-social.png)

Every Skill in this catalog has been used to ship at least one public video. None of them are toy demos.

---

## Who this is for

- **AI builders** prototyping video features without rebuilding 12 workflows from scratch
- **Content creators** using Claude Code to script, render, and iterate in one loop
- **Educators** turning lectures into 3Blue1Brown-style explainers
- **Marketers / growth teams** chopping long demos into platform-native shorts
- **Indie devs** who want video in their product but don't want to learn Manim

---

## Installation — pick your mode

### A. Browse only (no install)

```bash
git clone https://github.com/AIPMAndy/Andy-Video-SKill.git
cd Andy-Video-SKill
```

Read any `SKILL.md` directly. No Claude Code required.

### B. Single Skill

```bash
cp -r 01-programmatic-animation/andy-manim-video ~/.claude/skills/
```

Restart Claude Code to load it.

### C. Bulk install (recommended)

```bash
./scripts/install-all.sh                                    # install all 13
./scripts/install-all.sh --exclude andy-liquid,react-video  # skip some
```

See [INSTALLATION.md](./INSTALLATION.md) for full details and verification.

---

## How a Skill works

Each Skill is a directory containing:

- `SKILL.md` — the workflow contract Claude Code reads
- Optional assets, helper scripts, references

Drop it into `~/.claude/skills/` and Claude Code picks it up on next launch. No runtime, no API key, no daemon.

Example — `andy-p5js` detail page:

![andy-p5js detail](./showcase/assets/images/detail-p5js.png)

Or the Manim Skill, which has been used to ship educational explainers:

![andy-manim-video detail](./showcase/assets/images/detail-manim.png)

Or `andy-paper-collage-explainer` for a distinctive hand-crafted style:

![andy-paper-collage-explainer detail](./showcase/assets/images/detail-collage.png)

---

## Architecture — what this catalog actually is

This is **not** an application. It is a **content library** — 13 local directories of Skill instructions that an AI agent reads. The unit of install is the Skill, not the app.

```
Andy-Video-SKill/
├── 01-programmatic-animation/   # 4 Skills
├── 02-recording-to-video/       # 1 Skill
├── 03-code-to-video/            # 3 Skills
├── 04-script-and-planning/      # 3 Skills
├── 05-stylized-effects/         # 1 Skill
├── showcase/                    # GitHub Pages site
├── scripts/                     # install-all.sh, verify.sh, …
├── CATALOG.md                   # full Skill catalog with tech stacks
├── INSTALLATION.md              # install modes + verification
├── CONTRIBUTING.md              # how to add a Skill
└── CHANGELOG.md
```

Browse the full Skill-by-Skill catalog: [CATALOG.md](./CATALOG.md).

---

## Repository Metadata (suggestions)

| Field | Value |
|-------|-------|
| **Description** | Curated catalog of 12 video-generation Skills for Claude Code — Manim, React Video, Screencast-to-Viral, and more. |
| **Topics** | `claude-code` · `claude-skills` · `video-generation` · `manim` · `p5js` · `react-video` · `screencast-to-viral` · `ai-video` · `content-creation` · `open-source` |
| **Website** | https://AIPMAndy.github.io/Andy-Video-SKill/ |
| **Social Preview** | Use `./showcase/assets/images/hero.png` as the OG card |

---

## Roadmap

- [x] 12 Skills across 5 categories
- [x] Bilingual docs (English + 中文)
- [x] GitHub Pages showcase site
- [x] One-command bulk installer
- [x] Verification script (`./scripts/verify.sh`)
- [ ] Voice-driven video editing Skill
- [ ] Homebrew tap for macOS users
- [ ] Public output gallery — one shipped video per Skill
- [ ] Cross-platform install (Linux path verified)

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). The catalog welcomes:

- **New Skills** — must be production-tested, not theoretical
- **Improvements** to existing Skills (bug fixes, clearer contracts)
- **Translation fixes** in EN / 中文 READMEs

Bug reports and PRs are enabled. Issue templates are in `.github/ISSUE_TEMPLATE/`.

---

## FAQ

**Q: Do I need Claude Code?**
A: No. You can read any `SKILL.md` directly. But Skills shine when loaded into an agent.

**Q: Are these Skills free?**
A: Yes — MIT License. Use commercially, fork, remix, ship.

**Q: Can I install just one Skill?**
A: Yes. Every Skill is standalone. Use the `cp -r` form in INSTALLATION.md.

**Q: Why not just write my own Skill?**
A: You can. But each Skill here is the output of one full production cycle. You're saving 6+ months of trial-and-error.

**Q: What does "battle-tested" mean?**
A: Each Skill has shipped at least one public video we can show. See `killer-feature-manim*.png` above for the Manim examples.

**Q: Is there a web UI?**
A: The static [showcase](https://AIPMAndy.github.io/Andy-Video-SKill/) lists all Skills. The Skills themselves run inside Claude Code — there is no separate app.

---

<!-- andy-author-card:start -->
## 作者 / About the author

**AI 酋长 Andy（Andy Liu，GitHub/X @AIPMAndy）**：前腾讯/百度 AI 产品专家，大模型独角兽前 VP，现专注 AI + 产品方法论创业。

微信 `AIPMAndy`（备注「Andy-Video-Skill」） · [X @AIPMAndy](https://x.com/AIPMAndy) · [Telegram @AIPMAndy](https://t.me/AIPMAndy) · [个人官网 metaver.vip](https://metaver.vip/)

*AI Chief Andy (Andy Liu, @AIPMAndy on GitHub and X) is a former Tencent and Baidu AI product expert and former VP at an LLM unicorn, now a serial entrepreneur focused on AI and product methodology.*

### 作者的其他项目

- [AndySoul](https://github.com/AIPMAndy/AndySoul)：CLAUDE.md / AGENTS.md 规则模板，让 Claude Code、Codex、Cursor 少犯错
- [DNA Memory](https://github.com/AIPMAndy/dna-memory)：Claude Code、Codex 共用的本地 AI Agent 记忆 MCP
- [SafeSkill](https://github.com/AIPMAndy/safeskill)：装 AI Skill 之前，先扫危险命令、提示注入和密钥泄露
- [OpenClaw Skills 中文精选](https://github.com/AIPMAndy/awesome-openclaw-skills-CN)：OpenClaw Skills 分类整理，附国产模型接入指南
- [Grok Bot 中文攻略](https://aipmandy.github.io/grok-bot-handbook/)：AI Agent 中文教程

<!-- andy-author-card:end -->

## License

MIT — see [LICENSE](./LICENSE).

## Credits

Existing Andy Skills are maintained by Andy. Third-party sources retain original authors and licenses (BB-Video © 2026 Dylan Deng, MIT). Each Skill retains its own LICENSE inside its directory. The `andy-p5js` and `andy-paper-collage-explainer` visual assets shown above were produced by their respective Skills in real production.

---

<div align="center">

**If this saved you from rebuilding a video pipeline, a ⭐ goes a long way.**

</div>