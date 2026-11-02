# Changelog

All notable changes to Andy-Video-Skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).

## [Unreleased]

### Added — 2026-11-02 (V0.3)
- Expanded verified upstream registry from 22 to 30 projects, preserving all 13 bundled Skills.
- Added deterministic multi-stage routing for Chinese TTS, UI motion, 3D, Lottie, audio beat detection and postprocessing.
- Added eight new routing tests and status-explicit integration documentation; external engines are not yet installed or render-tested.


### Added — 2026-10-31
- New **andy-video-director** unified video orchestration Skill with 22 verified source candidates, route selection, runtime doctor, pinned upstream bootstrap and BB-Video project scaffold.
- Complete pinned BB-Video source available on demand with 30 styles and original MIT notice; official MoneyPrinterTurbo and Remotion Skill packs can be staged on demand.
- Deterministic routing unit tests and CI. Existing 12 Skills are preserved.


## [1.0.0] - 2026-08-14

### Added
- Initial repository creation
- 12 skills aggregated across 5 categories:
  - **01-programmatic-animation**: andy-manim-video, andy-p5js, andy-liquid, text-rain-generator
  - **02-recording-to-video**: andy-screencast-to-viral
  - **03-code-to-video**: react-video, react-content-generator, ai-video-producer
  - **04-script-and-planning**: dbs-script-flow, duizhaochao-script-generator, mrbeast-skill
  - **05-stylized-effects**: andy-paper-collage-explainer
- Bilingual documentation (README, INSTALLATION, CONTRIBUTING, CATALOG)
- Static showcase site under `showcase/` for GitHub Pages
- Helper scripts: `install-all.sh`, `update-skill.sh`, `new-skill.sh`, `verify.sh`
- GitHub Actions: Pages deployment, weekly link check
- MIT License
