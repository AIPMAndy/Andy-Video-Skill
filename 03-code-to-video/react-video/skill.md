---
name: react-video
description: Generate professional knowledge videos or custom React videos using Playwright and ffmpeg
trigger: When user wants to create educational videos, tech tutorials, or render React components as video
---

# React Video Renderer Skill

This skill helps you generate MP4 videos from React code. It supports two modes:

1. **Knowledge Video Generator** - Create professional educational videos from structured config (Apple-style design)
2. **Custom React Code** - Render any React component as video

## Usage

```
/react-video [options]
```

## Options

- `--width <number>` - Output video width (default: 2400)
- `--height <number>` - Output video height (default: 3200)
- `--duration <seconds>` - Video duration in seconds (auto-detected if not specified)
- `--output <path>` - Output file path (default: ./output/video/react-video.mp4)
- `--audio <path>` - Optional audio file to merge with video
- `--code <file>` - React component file to render (default: App.jsx)
- `--config <file>` - Knowledge video config file (JSON)
- `--template <name>` - Use built-in template: "knowledge" (default: custom)

## Mode 1: Knowledge Video Generator (NEW!)

Create professional educational videos with Apple-style design. Perfect for:
- Tech project introductions
- Tutorial videos
- Product demos
- Course content

### Quick Start

```bash
/react-video --template knowledge --config my-config.json
```

### Config Structure

```json
{
  "themeColor": "indigo",
  "project": {
    "name": "Project Name",
    "stars": "162k+",
    "courseNumber": "第 340 课",
    "category": "AI 基础设施"
  },
  "steps": [
    {
      "type": "cover",
      "title": "Main Title",
      "subtitle": "Subtitle",
      "script": "Narration text..."
    },
    {
      "type": "pain_point",
      "title": "Problem Statement",
      "visualizer": { ... }
    },
    {
      "type": "feature",
      "title": "Solution",
      "visualizer": { ... }
    },
    {
      "type": "golden_sentence",
      "quote": "Inspirational quote"
    },
    {
      "type": "summary",
      "points": [ ... ]
    }
  ]
}
```

### Step Types

- **cover** - Opening slide with project info
- **pain_point** - Highlight problems/challenges
- **feature** - Showcase solutions/features
- **golden_sentence** - Philosophical insight
- **summary** - Recap key points

### Examples

See `knowledge-video-config.example.json` and `knowledge-video-config-firecrawl.example.json` for complete examples.

## Mode 2: Custom React Code

Render any React component as video (original functionality).

```bash
/react-video --code MyComponent.jsx --width 1920 --height 1080
```

## How it works

1. Creates a temporary Vite project with your React code
2. Starts a dev server
3. Uses Playwright to record the browser rendering
4. Transcodes the recording to MP4 with ffmpeg
5. Optionally merges audio track

## Requirements

- Node.js and npm
- ffmpeg installed on system
- Playwright will be installed automatically

## Interactive Mode

Just run `/react-video` and the skill will guide you through:
1. Choosing between knowledge video or custom code
2. Providing necessary configuration
3. Generating the video
