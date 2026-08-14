# Changelog

All notable changes to the Text Rain Generator Skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-02

### 🎉 Initial Release

First stable release of Text Rain Generator, a Claude Code Skill that transforms Chinese classical poetry into artistic particle animations.

### ✨ Added

#### Core Features
- **Text rain animation generator** using p5.js particle system
- **20 curated presets** covering traditional Chinese architectural styles (jiangnan, beijing, huizhou, lingnan, yaodong, sichuan, tulou, yurt, temple, bamboo) and artistic styles (sakura, desert, modern, cyberpunk, minimal, ink, snow, storm, landscape, square)
- **Intelligent preset recommendation** based on poem content analysis
- **Physics-based simulation** with gravity, sine wave wobbling, rotation, and collision detection
- **Collision detection** using pixel brightness sampling from background images
- **23 example poems** from classical Chinese literature

#### AI Integration
- **ChatGPT + DALL-E 3 integration** via andy-relay Skill for automatic background image generation
- **Kimi WebBridge automation** for browser control and image downloading
- **Automatic scene description generation** from preset configurations

#### Advanced Tools
- **Video export** (`export-video.ts`) - frame-by-frame rendering using node-canvas, supports custom duration/FPS/quality
- **Batch generation** (`batch-generate.ts`) - concurrent processing with configurable parallelism, generates gallery index page
- **Audio enhancement** (`sound-effects.ts`) - adds atmospheric sound effects with fade-in and mute controls
- **Interactive quick-start** (`quick-start.sh`) - menu-driven demo script with 8 pre-selected poems

#### Developer Experience
- **TypeScript implementation** with full type safety
- **Comprehensive test suite** (`test.ts`) covering HTML generation, sketch generation, parameter embedding, file I/O, edge cases, and special characters
- **Modular architecture** - each tool can be used independently
- **CLI interface** (`cli.ts`) with JSON output for programmatic consumption
- **npm/bun scripts** for common workflows (test, demo, batch, export, presets)

#### Documentation
- **SKILL.md** - Claude Code execution workflow (5 steps: parse args → generate project → call andy-relay → verify image → preview)
- **USAGE.md** - comprehensive 300+ line user guide covering all features, troubleshooting, performance optimization
- **DEVELOPER.md** - architecture documentation, extension guide, testing guide, performance benchmarks
- **CHEATSHEET.md** - quick reference card with preset table, parameter reference, troubleshooting, performance tips
- **README.md** - project overview with feature highlights, quick start, roadmap
- **CHANGELOG.md** - version history (this file)

### 🎨 Presets

Each preset includes:
- Scene description for ChatGPT image generation
- Optimized speed and tilt parameters
- Custom color schemes
- Canvas dimensions (1080×1920 portrait, 1920×1080 landscape, 1080×1080 square)

Full list:
1. **jiangnan** (江南水乡) - Misty water towns, 2.0 speed, 5° tilt
2. **beijing** (北京胡同) - Siheyuan courtyards, 2.5 speed, 10° tilt
3. **huizhou** (徽派建筑) - Horsehead walls, 2.2 speed, 8° tilt
4. **lingnan** (岭南骑楼) - Arcade buildings, 2.3 speed, 12° tilt
5. **yaodong** (黄土窑洞) - Loess cave dwellings, 3.0 speed, 15° tilt
6. **sichuan** (川西民居) - Tibetan-style watchtowers, 2.8 speed, 10° tilt
7. **tulou** (客家土楼) - Hakka earthen buildings, 2.5 speed, 8° tilt
8. **yurt** (草原毡房) - Mongolian yurts, 3.5 speed, 20° tilt
9. **temple** (古刹寺庙) - Buddhist temples, 1.8 speed, 5° tilt
10. **bamboo** (竹林幽径) - Bamboo forests, 2.0 speed, 6° tilt
11. **sakura** (樱花季) - Cherry blossoms, 1.5 speed, 8° tilt
12. **desert** (大漠孤烟) - Desert landscapes, 4.0 speed, 25° tilt
13. **modern** (现代都市) - Urban skyscrapers, 3.0 speed, 15° tilt
14. **cyberpunk** (赛博朋克) - Neon-lit future, 3.5 speed, 20° tilt
15. **minimal** (极简主义) - Pure minimalism, 2.0 speed, 0° tilt
16. **ink** (水墨画) - Ink wash painting, 1.5 speed, 5° tilt
17. **snow** (雪景) - Snowy scenes, 1.0 speed, 3° tilt
18. **storm** (暴风雨) - Stormy weather, 5.0 speed, 35° tilt
19. **landscape** (横版山水) - Horizontal landscape, 2.0 speed, 8° tilt
20. **square** (方形构图) - Square format, 2.0 speed, 10° tilt

### 🔧 Technical Details

#### Architecture
- **Frontend**: p5.js 1.7.0 (particle system and canvas rendering)
- **Backend**: TypeScript with Bun runtime
- **AI**: ChatGPT + DALL-E 3 (via andy-relay Skill)
- **Browser automation**: Kimi WebBridge MCP server
- **Video rendering**: node-canvas + FFmpeg

#### Performance
- Generation speed: <1 second (excluding background image)
- Runtime: 60 FPS @ 72 particles, ~10-15% CPU, ~50MB memory
- Video export: 10 seconds @ 30fps ≈ 8 seconds rendering time

#### Physics Engine
```typescript
class RainDrop {
  - Gravity acceleration: this.speed += 0.05
  - Sine wave wobbling: this.x += sin(wobblePhase) * wobbleAmplitude
  - Rotation: this.rotation += rotationSpeed
  - Collision detection: brightness < 80 triggers splash effect
  - Particle density: calculated as poemLength * densityFactor
}
```

### 📦 Dependencies

```json
{
  "@types/node": "^20.10.0",
  "canvas": "^2.11.2",
  "typescript": "^5.3.3"
}
```

### 🎯 Usage

```bash
# Basic invocation in Claude Code
/text-rain-generator "床前明月光，疑是地上霜。举头望明月，低头思故乡。"

# With preset
/text-rain-generator "春眠不觉晓" --preset jiangnan

# Custom parameters
/text-rain-generator "大漠孤烟直" --speed 4.0 --tilt 25 --color "#e8a05d"
```

### 🧪 Testing

- 6 test cases covering all core functionality
- 100% test pass rate
- Edge case handling: empty text, special characters, Unicode
- Live demo verified: "床前明月光" with 1080×1920 background @ 60 FPS

### 📝 Known Limitations

1. **Background image generation** depends on ChatGPT availability and rate limits
2. **Image dimensions** may require manual adjustment (DALL-E 3 sometimes generates non-exact sizes)
3. **Audio effects** require manual integration (CDN-hosted sounds)
4. **Video export** requires FFmpeg installation
5. **Chinese fonts** may display incorrectly on Windows without proper font configuration

### 🚀 Future Roadmap

#### v1.1 (Short-term)
- Automatic background image resizing
- Built-in audio library (local files)
- Web Font support
- 30+ presets

#### v1.5 (Mid-term)
- Interactive parameter adjustment panel
- Real-time preview with Hot Reload
- Community preset sharing platform
- Mobile adaptation

#### v2.0 (Long-term)
- 3D text rain (Three.js)
- Physics engine integration (Matter.js)
- WebGL acceleration
- Cloud rendering service

### 🙏 Credits

- **景桐** - Original Vibe Coding inspiration
- **p5.js** - Elegant creative coding framework
- **OpenAI** - DALL-E 3 image generation
- **Kimi WebBridge** - Reliable browser automation

### 📄 License

MIT License

---

## [Unreleased]

### Planned
- Automatic image dimension correction
- Built-in sound effect library
- More architectural presets (30+ total)
- Performance optimization for high particle counts
- WebGL rendering backend option

---

**Maintained by**: Andy  
**Repository**: `~/.claude/skills/text-rain-generator/`  
**Documentation**: See README.md, USAGE.md, DEVELOPER.md, CHEATSHEET.md
