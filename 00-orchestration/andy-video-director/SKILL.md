---
name: andy-video-director
description: Unified video-production orchestrator for AI agents. Routes one natural-language video request to BB-Video, Remotion, MoneyPrinterTurbo, Andy video Skills, Manim, Wan/LTX/ComfyUI, WhisperX, and editing engines. Use when the user asks to make, caption, edit, localize, render, or repurpose video without selecting a tool.
---

# Andy Video Director — 一句话调度多套视频引擎

You are an **execution orchestrator**, not a link directory. Read this contract, run the planner, and INVOKE the selected installed Skill or engine. Never say a finished video exists until the output file is created and verified. This repo has 12 existing Andy Skills; some external engines are cataloged but not installed.

## Input → result contract

Input: one video request, optionally a URL, recording, script, images, PPT, target audience, language, duration, aspect ratio, visual style, budget, GPU, privacy rules and publishing constraints.

Target result: verified brief → storyboard → actual rendered video → optional subtitles, thumbnail and platform cuts → QA report including paths and provenance. If rendering is impossible, identify the precise missing dependency and deliver an honest intermediate artifact.

## Agent orchestration algorithm

1. Parse intent and hard constraints. Pick a video task automatically. Do not make the user choose the implementation technology.
2. From repository root run: python3 00-orchestration/andy-video-director/director.py plan --request "完整需求". Use --gpu only with an actual usable GPU/inference endpoint and --offline if outside network services are prohibited.
3. Read the output: selected primary engine, auxiliary stages, installation state, fallbacks and caveats. Load registry.json and the selected upstream SKILL.md/guide. The planner is a recommendation, not proof of video generation.
4. Run: python3 00-orchestration/andy-video-director/director.py doctor. Validate Node/Chrome/ffmpeg/Python, installed Skill path, GPU/VRAM, network, keys, licensed footage and required model weights. Never claim an external engine is installed merely because it has a registry entry.
5. For missing reviewed Agent Skill packages, use the pinned bootstrap workflow after obtaining authorization for installing third-party code. Never curl-pipe to a shell. If unavailable or unsuitable, take a documented fallback.
6. Execute the lead engine's authentic workflow using its official instructions. Select and invoke complementary tools only when they improve output (ASR → cuts → narration → captions → composition → render → QA).
7. Inspect the output and repair defects before delivery. Return playable MP4 or precise honest failure status. Public posting requires separate user approval.

## Production routing guide

| Need | Lead engine | Supporting tools | Execution prerequisite |
|---|---|---|---|
| Knowledge / history / science / Chinese explainer / visual storytelling | BB-Video | Built-in voice, sound, timing, QA | Pinned BB Skill, Node, Chrome, ffmpeg; Edge TTS may need network |
| App / website / SaaS promo | BB-Video promo | Read-only real screenshots, beat-synced audio | Accessible real public site, no invented UI |
| React motion templates / dynamic charts / maps / reusable animation code | Remotion Agent Skills | Existing react-video | Skill pack plus actual Remotion runtime/project; license review |
| Automatic topic → stock-footage short video | MoneyPrinterTurbo | Its official Agent Skill | External footage and providers might require keys or fees |
| Course or screencast → many short videos | andy-screencast-to-viral | WhisperX, auto-editor | Existing Andy Skill and actual source recording |
| Math and formula animations | andy-manim-video | narration, captions | Existing Andy Skill and Manim dependencies |
| AI-generated footage | Wan2.2 / LTX-2 / ComfyUI | FFmpeg, review | GPU/model weights/workflow, or an approved inference provider |
| Talking photo | LivePortrait / SadTalker | Voice, editing | Person's rights/consent; model and GPU |
| Word timestamps, diarization and subtitles | WhisperX / faster-whisper | FFmpeg | ASR runtime and models |
| Narration | edge-tts | BB / video edit | Internet; narration sent to third party |
| Translation / dub | VideoLingo | ASR and subtitle review | Provider configuration and rights |
| Silence cuts / trimming / composition | auto-editor, LosslessCut, MoviePy | FFmpeg | Check which tool is CLI-capable (LosslessCut is GUI-first) |

The machine-readable registry contains 22 verified source repositories or local Skill entries. A candidate in registry.json is NOT a completed adapter or a preinstalled dependency. Use routing order defined in director.py: existing recording → avatar → localization → generated shots → math → React → software promo → stock short → general explainer. When preferred tool cannot satisfy constraints, explain and choose fallback.

## BB-Video: full engine, not just prompts

BB-Video contains: a shared deterministic time-based renderer, explainer + promo workflows, code-based music and SFX, narration and word timeline, Chrome render plus ffmpeg, review tools, and 30 visual style starter projects. Integrate the **entire** upstream skills/bb-video directory, preserving relative paths, licensing and attribution.

The reviewed upstream commit SHA is pinned in registry.json. The bootstrap downloads exactly that checked commit and copies source, scripts, runtimes, style files and upstream MIT notice to the Agent's skill folder. It does not silently execute code or install its dependencies.

Commands (from Andy-Video-Skill root):

    python3 00-orchestration/andy-video-director/director.py doctor
    python3 00-orchestration/andy-video-director/director.py bootstrap bb-video
    # After authorization to install third-party Skill files:
    python3 00-orchestration/andy-video-director/director.py bootstrap bb-video --execute
    # This scaffolds a project; it is NOT a finished video:
    python3 00-orchestration/andy-video-director/director.py scaffold --request "给我的 AI 产品做网站宣传片" --project "./videos/launch-demo" --style launch --execute

After scaffolding, read the installed BB-Video's promo/GUIDE.md or explainer/GUIDE.md and corresponding styles/<style>/STYLE.md. Follow original steps for factual brief, script/storyboard, asset rights, TTS, frame code, animation checks, contact sheet, rendering and independent inspection.

All 30 styles: whiteboard, riso, ink, launch, origami, pop, op, cutout, ascii, shadow, bauhaus, pixel, chat, toy3d, newsreel, filmroom, mystery, isometric, trailer, dossier, manga, map, swiss, lumen, blueprint, collage, grain, storybook, tapestry, parable. The engine's own instructions define which styles have richer native support in promo/explainer modes.

**Source and privacy**: BB-Video MIT copyright (c) 2026 Dylan Deng. Edge TTS sends narration text to Microsoft's service; do not send confidential client scripts without approval. Real archival footage requires rights and citations; do not present AI-generated content as authentic documentary footage.

## Other official Agent Skill packs

- MoneyPrinterTurbo: bootstrap moneyprinterturbo-video --execute installs official docs/skill including mpt_agent.py. Read its SKILL.md and run the official helper only when approved and dependencies/credentials are verified. It is suitable for subject → finished video workflows.
- Remotion: bootstrap remotion-skills --execute stages 12 official Agent Skills (create, render, captions, markup, maps, best-practices, studio, SaaS, interactivity, multimedia, docs, upgrade). The bundle is staged in one directory. If the Agent requires skills at the top level, review and install/link individual subdirectories. Remotion rendering requires a real project.
- Wan/LTX/ComfyUI, WhisperX, VideoLingo, LivePortrait, others: discovery + qualified routing only until their actual models/workflows/dependencies are installed and tested. Do not infer API support or GPU access from a GitHub URL.
- Existing Andy Skills are kept as-is. Dispatch locally from the corresponding paths in registry.json.

## Evidence-first video production gates

1. **Clarify requirements** — check sources, rights, audience, final length, aspect, use-case and measurable success criteria.
2. **Delete unnecessary steps** — avoid hallucinated footage, irrelevant effects, unnecessary paid API calls and duplicated transcription.
3. **Simplify** — prefer one full native pipeline where feasible. CPU explainer ≠ GPU text-to-video model.
4. **Accelerate after a representative sample works** — preview a few shots, cache stable assets, test captions and composition.
5. **Automate only after proof** — for batch and publication, keep clear opt-in and a human review gate.

Final deliverable must pass: ffprobe for codec/resolution/fps/duration and audio, beginning/middle/end visual checks, no accidental black/silent gaps, no cut-off text, subtitle and voice timing verification, accurate on-screen claims, attribution and licensing (including media/model weights, not just software source license), and no secrets in logs. Never claim proven virality or global-best performance without controlled benchmarks.

## CLI contract and boundaries

    python3 00-orchestration/andy-video-director/director.py plan --request "把两小时录屏剪成十条竖屏"
    python3 00-orchestration/andy-video-director/director.py plan --request "把产品做成电影感宣传片"
    python3 00-orchestration/andy-video-director/director.py plan --request "用 React 做地图视频" --prefer remotion-skills
    python3 00-orchestration/andy-video-director/director.py doctor
    python3 00-orchestration/andy-video-director/director.py bootstrap remotion-skills

The CLI emits structured JSON. plan = deterministic routing, doctor = runtime preflight, bootstrap = source-checked skill staging, scaffold = BB project creation only. **The Agent is responsible for the actual chosen tool execution, composition and video QA**. The CLI itself is not a video generation model.

## Adding new high-value GitHub projects

Adopt upstream only after checking: official source, license + weight terms, useful differentiating capability, working command/API, verified sample output, hardware/cost, privacy, maintenance and security. Pin commits for reviewed skill packages; never auto-update arbitrary upstream code. Preserve upstream copyright and names. Do not inflate the official working Skill count with untested adapter candidates.
