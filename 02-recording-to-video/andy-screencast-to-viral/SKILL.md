---
name: screencast-to-viral
description: Transform long screen recordings into viral short-form videos with AI-powered editing, subtitles, and packaging. Designed for 10x content production velocity.
tags: [video, editing, viral, automation, short-form]
version: 1.0.0
---

# Andy's Screencast-to-Viral Pipeline

## 🎯 Core Mission

Turn your 42+ screen recordings into 100+ viral short videos. Automated analysis → intelligent editing → viral packaging → batch publishing.

Target: **10万粉丝** through systematic content production.

## When to Use

- You have raw screen recordings (2-10 minutes)
- Want to generate short-form videos (30-90 seconds)
- Need batch processing for multiple files
- Targeting Douyin/Bilibili/Xiaohongshu

## Quick Start

```bash
# Analyze one recording to find highlights
/screencast-to-viral analyze --input "path/to/video.mp4"

# Generate short video (auto mode)
/screencast-to-viral generate --input "path/to/video.mp4"

# Batch process entire directory
/screencast-to-viral batch --input "/Users/andy/Documents/Andy录屏素材库"

# Preview without rendering
/screencast-to-viral preview --input "path/to/video.mp4"
```

## Pipeline Stages

### Stage 1: Analyze (智能分析)

**What it does:**
- Extract metadata (duration, resolution, audio)
- Transcribe speech with Whisper
- Extract key frames (0.5 fps)
- Identify "highlight moments"
- Generate cutting recommendations

**Output:**
```json
{
  "source": "video.mp4",
  "duration": 206.5,
  "transcription": "full text...",
  "highlights": [
    {
      "start": 15.2,
      "end": 45.8,
      "score": 0.92,
      "reason": "High visual change + excited speech",
      "type": "result_reveal"
    }
  ],
  "recommendations": {
    "best_30s": { "start": 15.2, "end": 45.2 },
    "best_60s": { "start": 10.0, "end": 70.0 },
    "best_90s": { "start": 5.0, "end": 95.0 }
  }
}
```

### Stage 2: Edit (智能剪辑)

**What it does:**
- Extract highlight segment
- Remove dead air and pauses
- Speed up non-critical parts (1.2-1.5x)
- Apply MrBeast "no dull moments" principle

**Rules:**
- Delete all silence >0.5s
- Delete all "um", "uh", "嗯", "啊"
- Speed up mouse movement/typing
- Keep all "wow moments"

### Stage 3: Package (爆款包装)

**What it does:**
- Add viral hook (first 3 seconds)
- Generate auto-subtitles
- Add BGM (120-140 BPM)
- Apply visual effects

**Hook Templates:**

```javascript
const hooks = {
  question: {
    text: "你见过{X秒}做出这个效果吗？",
    visual: "flash_final_result"
  },
  challenge: {
    text: "大家都说这个不可能...",
    visual: "show_difficulty"
  },
  result_first: {
    text: "直接看结果 →",
    visual: "show_result_immediately"
  }
}
```

### Stage 4: Design (标题+封面)

**What it does:**
- Generate 5 title variants (MrBeast formula)
- Extract best frame for thumbnail
- Add text overlay to thumbnail
- Create A/B test versions

**Title Templates:**

```python
templates = [
    "用AI{动作}{结果}，只用了{N}秒",
    "{之前}到{之后}，差距惊人",
    "终于发现{秘密}了...",
    "{N}个{工具}同时{动作}会怎样",
]
```

### Stage 5: Export (批量导出)

**What it does:**
- Export to platform-specific formats
- Generate metadata.json for each video
- Create thumbnail variants
- Prepare upload checklist

**Platform Specs:**

| Platform | Ratio | Duration | Bitrate |
|----------|-------|----------|---------|
| Douyin | 9:16 | 30-90s | 6000k |
| Bilibili | 16:9 | 60-180s | 8000k |
| Xiaohongshu | 3:4 | 30-60s | 5000k |

## Options Reference

```bash
--input <path>          # Input video file or directory
--output <path>         # Output directory (default: ./output)
--duration <seconds>    # Target duration: 30, 60, or 90
--platform <name>       # douyin, bilibili, xiaohongshu, or all
--style <template>      # tech, tutorial, vlog, showcase
--hook <type>           # question, challenge, result_first
--no-subtitle          # Skip subtitle generation
--no-music             # Skip background music
--speed <factor>        # Speed multiplier (1.0-2.0)
--preview              # Generate preview only
--batch                # Process entire directory
--force                # Overwrite existing outputs
```

## Configuration File

Create `viral-config.json` in your project:

```json
{
  "defaults": {
    "duration": 60,
    "platform": "douyin",
    "style": "tech",
    "hook": "question"
  },
  "audio": {
    "bgm_volume": 0.25,
    "voice_volume": 0.75,
    "bgm_library": "~/Music/BGM"
  },
  "subtitle": {
    "font": "PingFang SC",
    "size": 48,
    "color": "#FFFFFF",
    "outline": "#000000",
    "position": "bottom_center"
  },
  "quality": {
    "video_bitrate": "6000k",
    "audio_bitrate": "128k",
    "preset": "medium"
  }
}
```

## Dependencies

**Required:**
- ffmpeg >= 5.0
- ffprobe (bundled with ffmpeg)
- whisper (OpenAI) - `pip install openai-whisper`
- Python >= 3.9

**Optional:**
- yt-dlp (for reference video analysis)
- imagemagick (for thumbnail design)

## Installation Check

```bash
# Check if all tools are available
/screencast-to-viral doctor
```

Expected output:
```
✓ ffmpeg found (version 6.0)
✓ ffprobe found
✓ whisper found
✓ Python 3.11 found
⚠ imagemagick not found (optional)
✓ All required dependencies satisfied
```

## Workflow Example

### Single Video Processing

```bash
# Step 1: Analyze
/screencast-to-viral analyze --input "李子柒01.mp4"

# Review analysis.json, then:

# Step 2: Generate
/screencast-to-viral generate \
  --input "李子柒01.mp4" \
  --duration 60 \
  --platform douyin \
  --hook question

# Output:
# - output/李子柒01_viral_60s.mp4
# - output/李子柒01_thumbnail.jpg
# - output/李子柒01_titles.txt
# - output/李子柒01_metadata.json
```

### Batch Processing

```bash
# Process all recordings
/screencast-to-viral batch \
  --input "/Users/andy/Documents/Andy录屏素材库" \
  --output "./viral_output" \
  --duration 60 \
  --platform all

# Generates:
# - 42 source videos → 126 short videos (3 versions each)
# - Organized by platform
# - Ready-to-upload package
```

## Quality Checklist

Before publishing, verify:

- [ ] Video plays smoothly (no stutters)
- [ ] Subtitles are accurate and readable
- [ ] Audio levels balanced (BGM not too loud)
- [ ] Hook grabs attention in first 3 seconds
- [ ] No dead air or long pauses
- [ ] Thumbnail has visual contrast
- [ ] Title uses numbers and curiosity gap
- [ ] Ends with clear CTA or cliffhanger

## MrBeast Principles Applied

1. **CTR × AVD formula** - Every decision optimizes click-through or watch time
2. **No dull moments** - Delete everything boring
3. **Stair-stepping** - Content escalates continuously
4. **Simple concept × extreme execution** - Clear idea, flawless delivery
5. **First 30 seconds rule** - Hook, promise, action

## Success Metrics

Track these for every video:

```json
{
  "completion_rate": 0.65,  // >50% = viral potential
  "like_rate": 0.08,        // >5% = high value
  "comment_rate": 0.03,     // >2% = engaging
  "share_rate": 0.01,       // >1% = exceptional
  "follower_growth": 127    // per 10k views
}
```

## Troubleshooting

### Issue: Whisper transcription fails
**Solution:** Check audio track exists with `ffprobe -show_streams video.mp4`

### Issue: Subtitles out of sync
**Solution:** Use `--subtitle-offset <seconds>` to adjust timing

### Issue: Generated video too large
**Solution:** Lower bitrate with `--video-bitrate 4000k`

### Issue: Hook doesn't match content
**Solution:** Manually specify highlight with `--segment 15.2-45.8`

## Iteration Strategy

1. **Week 1**: Process 10 best recordings → 30 test videos
2. **Week 2**: Analyze metrics → identify winning patterns
3. **Week 3**: Process remaining 32 recordings with winning template
4. **Week 4**: Scale to daily publishing (2-3 videos/day)

## Output Structure

```
viral_output/
├── douyin/
│   ├── video_001/
│   │   ├── final.mp4
│   │   ├── thumbnail.jpg
│   │   ├── titles.txt
│   │   └── metadata.json
│   └── video_002/
├── bilibili/
└── xiaohongshu/
```

## Next Steps

After skill creation:
1. Test with 1 recording (李子柒01.mp4 or GPT做电脑壁纸.mp4)
2. Iterate on hook templates
3. Build title generation logic
4. Create batch processing script
5. Launch production pipeline

---

**Status**: 🚧 In Development
**Goal**: Transform 42 recordings → 100+ viral videos → 10万粉丝
**Deadline**: 3 months from start
