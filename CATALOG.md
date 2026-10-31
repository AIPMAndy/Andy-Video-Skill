# Skill Catalog

13 local Skills across 6 categories. The [22-source video engine registry](./00-orchestration/andy-video-director/registry.json) is a router index, not 22 installed Skills.

## By Category

### 00 · Unified Video Orchestration (1 skill)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 13 | [andy-video-director](./00-orchestration/andy-video-director/) | Python stdlib / Agent Skill / multi-engine router | v0.2.0 | [SKILL.md](./00-orchestration/andy-video-director/SKILL.md) |

Upstream Agent Skill packs installable on demand: full BB-Video with 30 styles; MoneyPrinterTurbo; and Remotion Agent Skills. Heavy model engines remain external targets requiring setup.



### 01 · Programmatic Animation (4 skills)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 1 | [andy-manim-video](./01-programmatic-animation/andy-manim-video/) | Python / Manim | v1.0.0 | [SKILL.md](./01-programmatic-animation/andy-manim-video/SKILL.md) |
| 2 | [andy-p5js](./01-programmatic-animation/andy-p5js/) | p5.js | v1.0.0 | [skill.md](./01-programmatic-animation/andy-p5js/skill.md) |
| 3 | [andy-liquid](./01-programmatic-animation/andy-liquid/) | Three.js / React | v0.1.0 | [SKILL.md](./01-programmatic-animation/andy-liquid/SKILL.md) |
| 4 | [text-rain-generator](./01-programmatic-animation/text-rain-generator/) | Canvas / JS | v1.0.0 | [SKILL.md](./01-programmatic-animation/text-rain-generator/SKILL.md) |

### 02 · Recording-to-Video (1 skill)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 5 | [andy-screencast-to-viral](./02-recording-to-video/andy-screencast-to-viral/) | Python / FFmpeg | v1.0.0 | [SKILL.md](./02-recording-to-video/andy-screencast-to-viral/SKILL.md) |

### 03 · Code-to-Video (3 skills)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 6 | [react-video](./03-code-to-video/react-video/) | React / Playwright | v1.0.0 | [skill.md](./03-code-to-video/react-video/skill.md) |
| 7 | [react-content-generator](./03-code-to-video/react-content-generator/) | React / Tailwind | v2.0.0 | [SKILL.md](./03-code-to-video/react-content-generator/SKILL.md) |
| 8 | [ai-video-producer](./03-code-to-video/ai-video-producer/) | Node.js / Playwright | v0.1.0 | [SKILL.md](./03-code-to-video/ai-video-producer/SKILL.md) |

### 04 · Script & Planning (3 skills)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 9 | [dbs-script-flow](./04-script-and-planning/dbs-script-flow/) | Logic analyzer | v1.1.0 | [SKILL.md](./04-script-and-planning/dbs-script-flow/SKILL.md) |
| 10 | [duizhaochao-script-generator](./04-script-and-planning/duizhaochao-script-generator/) | Template | v1.0.0 | [SKILL.md](./04-script-and-planning/duizhaochao-script-generator/SKILL.md) |
| 11 | [mrbeast-skill](./04-script-and-planning/mrbeast-skill/) | Methodology | v1.0.0 | [SKILL.md](./04-script-and-planning/mrbeast-skill/SKILL.md) |

### 05 · Stylized Effects (1 skill)
| # | Skill | Tech Stack | Status | Source |
|---|-------|-----------|--------|--------|
| 12 | [andy-paper-collage-explainer](./05-stylized-effects/andy-paper-collage-explainer/) | Canvas / JS | v1.0.0 | [SKILL.md](./05-stylized-effects/andy-paper-collage-explainer/SKILL.md) |

## By Tech Stack

- **Python stdlib / Agent orchestration**: andy-video-director (routing, environment checks, pinned skill staging, actual Agent handoff)


- **Python / Manim**: andy-manim-video
- **p5.js**: andy-p5js
- **Three.js / React**: andy-liquid
- **Canvas / JS**: text-rain-generator, andy-paper-collage-explainer
- **React / Playwright / ffmpeg**: react-video
- **React / Tailwind**: react-content-generator
- **Node.js / Playwright**: ai-video-producer
- **Python / FFmpeg**: andy-screencast-to-viral
- **Logic analyzer / templates / methodology**: dbs-script-flow, duizhaochao-script-generator, mrbeast-skill
