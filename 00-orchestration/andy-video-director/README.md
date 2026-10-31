# Andy Video Director | Unified video Skill orchestrator

One natural-language video request → route to the right upstream Skill, choose optional companions, set up reviewed pinned Skill files and execute through the actual producer.

This is an **Agent Skill with an executable deterministic planner**, not a turnkey hosted model. It keeps the 12 existing Andy Skills intact and contains an audited registry of 22 video-related repositories/skills. Installed upstream Skills currently supported by the installer: **BB-Video**, **MoneyPrinterTurbo**, **Remotion Agent Skills**. Compute-heavy model repositories are cataloged routing targets only until independently set up.

## Fast start

From the repository root (Python 3.9+, standard library only):

    python3 00-orchestration/andy-video-director/director.py plan --request "用开源方案做一个知识视频"
    python3 00-orchestration/andy-video-director/director.py doctor

Example: pin and stage the full BB-Video source, preserving its complete runtimes, guides and 30 styles.

    python3 00-orchestration/andy-video-director/director.py bootstrap bb-video
    python3 00-orchestration/andy-video-director/director.py bootstrap bb-video --execute
    python3 00-orchestration/andy-video-director/director.py scaffold --request "给我的 SaaS 做发布视频" --project ./videos/demo --style launch --execute

The last step **creates a source project only**. The AI Agent must read upstream promo/GUIDE.md, implement the storyboard/frame code and run its voice/render/review pipeline.

Other approved upstream packages:

    python3 00-orchestration/andy-video-director/director.py bootstrap moneyprinterturbo-video --execute
    python3 00-orchestration/andy-video-director/director.py bootstrap remotion-skills --execute

Use a secure GitHub connection and verify the pinned commit. Third-party dependencies, API keys, model downloads and any render steps are NOT performed by bootstrap. If a source cannot be downloaded or its reviewed version is unavailable, the command fails without installing a different revision.

## Selection examples

| Request | Lead engine |
|---|---|
| 科普/讲知识/白板动画/冷知识 | BB-Video |
| 软件发布/网页宣传片 | BB-Video promo |
| React 动画/动态地图 | Remotion Agent Skills |
| 给题材一键生成短视频 | MoneyPrinterTurbo |
| 2 小时录屏剪成多条 | Existing Andy screencast Skill |
| 数学推导 | Existing Andy Manim Skill |
| 文生视频/图生视频 | Wan / ComfyUI, only after GPU/model setup |
| 照片说话 | LivePortrait (rights + GPU required) |
| 视频翻译配音 | VideoLingo |

## Audit and security

- Registry: [registry.json](./registry.json) — provenance, use cases, hardware, implementation state, license caveats.
- Agent contract: [SKILL.md](./SKILL.md) — routing + actual-tool handoff + quality gates.
- Tests: [tests](./tests/) — no external services required.
- External code is not executed by merely planning or staging. Explicit execute flags exist for bootstrap and BB scaffolding.
- BB-Video © 2026 Dylan Deng, MIT. Its root LICENSE is preserved on installation.
- A video's third-party media, voice, model weights, trademarks and faces may carry restrictions beyond source code license.

## QA for actual rendered MP4

```bash
python3 00-orchestration/andy-video-director/director.py qa --file ./videos/final.mp4 --aspect 9:16 --require-audio
```

This checks ffprobe container metadata, streams and aspect. It cannot replace human review of caption timing, facts, scene continuity, black frames or style quality.
