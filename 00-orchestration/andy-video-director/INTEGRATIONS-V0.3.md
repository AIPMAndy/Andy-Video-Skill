# Andy Video Director V0.3 — Integration status

**Published: 2026-11-02.** This release upgrades the **catalog and deterministic multi-stage planner**, not hosted rendering. New third-party tools are **not bundled, installed, invoked, or proven to output video**.

## New upstream sources (repository existence verified)

| Engine | GitHub source | Purpose | Requirements |
|---|---|---|---|
| CosyVoice | [QwenAudio/CosyVoice](https://github.com/QwenAudio/CosyVoice) | Chinese narration | Local model weights, compute, approved voice |
| Motion | [motiondivision/motion](https://github.com/motiondivision/motion) | UI/React animations | Browser renderer |
| Anime.js | [juliangarnier/anime](https://github.com/juliangarnier/anime) | Timeline and SVG motion | Browser renderer |
| Blender MCP | [ahujasid/mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | 3D assets/scenes | Trusted MCP server, Blender, rendering |
| librosa | [librosa/librosa](https://github.com/librosa/librosa) | Music beat and tempo analysis | Licensed source audio; Python runtime |
| Lottie Web | [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | Vector animations | Real Lottie JSON and capture |
| postprocessing | [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing) | Browser bloom/DOF | WebGL and GPU |
| Three.js | [mrdoob/three.js](https://github.com/mrdoob/three.js) | Browser 3D scenes | WebGL and recording/capture |

## Planner demo (stdlib only)

Run from repository root:

```bash
python3 00-orchestration/andy-video-director/director.py plan --request "用 Blender MCP 做三维建模"
python3 00-orchestration/andy-video-director/director.py plan --request "给中文知识视频配音、生成字幕"
python3 00-orchestration/andy-video-director/director.py plan --request "用 Anime.js 做 UI 动效"
python3 00-orchestration/andy-video-director/director.py plan --request "把视频按音乐节拍自动卡点"
python3 00-orchestration/andy-video-director/director.py doctor
python3 -m unittest discover -s 00-orchestration/andy-video-director/tests -v
```

`plan` returns engine choice, stage sequence, availability and fallbacks. It does not install libraries, call an MCP server, run a speech model or render MP4. The `quality` stage is a *planned* check until an actual file exists.

## Acceptance gates before claiming executable integration

1. **Product promo**: original product screenshots, actual animation, exported MP4 and review of the real frames.
2. **Chinese explainer**: locally generated permitted speech, pronunciation review, aligned captions and actual video export.
3. **Short-form editing**: input recording, real ASR/beat metadata, exported vertical video, and timing/codec/playback QA.

For each engine, pin an audited version, establish licensing including model weights/assets, install approved dependencies, check CPU/GPU/resources, produce at least one reproducible output and run visual/audio quality checks. Do not silently install arbitrary code or MCP tools. Voice cloning requires rights and permission. Music and 3D assets must be appropriately licensed. No external source is represented as production-tested solely by catalog inclusion.
