# Andy-P5JS

<div align="center">

![Andy-P5JS Logo](./assets/logo.png)

**AI驱动的p5.js创意编码工作流 - 从灵感到动画一站式解决方案**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/andyai/andy-p5js/releases)
[![p5.js](https://img.shields.io/badge/p5.js-1.7.0+-red.svg)](https://p5js.org/)

[English](./README.md) | [中文](./README_CN.md)

</div>

## 🎯 What is Andy-P5JS?

Andy-P5JS is a complete AI-powered workflow for creative coding with p5.js, from inspiration discovery to final video output. It combines the best AI tools and platforms to streamline the entire creative process.

## ✨ Features

- 🔍 **Inspiration Discovery** - Search quality templates from OpenProcessing
- 🤖 **AI Code Generation** - Generate high-quality code using Gemini 3.1 Pro Canvas
- 👁️ **Live Preview** - Real-time preview and debugging in p5.js Web Editor
- ⚡ **Local Optimization** - Deploy locally and enhance visual effects
- 🎨 **Visual Validation** - Visual regression testing with testiv/snapstack
- 🎬 **Video Output** - Screen recording with Cap or video editing with ChatCut

## 🔄 Standard Workflow

```
Inspiration → AI Generation → Online Preview → Local Optimization → Visual Validation → Video Output
     ↓              ↓               ↓                  ↓                    ↓                ↓
OpenProcessing   Gemini      p5js.org         Local Server           MCP Tools       Cap/ChatCut
```

## 🚀 Quick Start

### Installation

1. **Install Claude Desktop** (with Andy-P5JS skill)

```bash
# Clone this repository
git clone https://github.com/andyai/andy-p5js.git
cd andy-p5js

# Copy skill to Claude skills directory
cp -r skill.md ~/.claude/skills/andy-p5js/
```

2. **Configure MCP Servers** (optional but recommended)

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "webbridge": {
      "command": "node",
      "args": ["/path/to/webbridge/server.mjs"],
      "env": {
        "KIMI_WEBBRIDGE_URL": "http://127.0.0.1:10086"
      }
    },
    "testiv": {
      "command": "npx",
      "args": ["-y", "@testiv/mcp"]
    },
    "snapstack": {
      "command": "npx",
      "args": ["-y", "snapstack-server"]
    }
  }
}
```

### Usage

**In Claude Desktop:**

```
/andy-p5js
```

Or with specific requirements:

```
/andy-p5js Create a 3D particle explosion effect
```

## 📖 Complete Workflow Guide

### Step 1: Inspiration Search (OpenProcessing)

Visit [OpenProcessing](https://openprocessing.org/) to search for quality templates.

**Search Tips:**
- Use English keywords (e.g., "particle system", "3D animation")
- Filter by likes/favorites
- Check the license before using
- Look for clear code structure

### Step 2: AI Code Generation (Gemini Canvas)

Use the **3-step prompt engineering method**:

**Step 1 - Generate Style Prompt:**
```
Generate a detailed visual style description for this p5.js animation:

Requirements: [Your requirements]

Output:
- Visual style (colors, lighting, atmosphere)
- Animation effects (particle count, motion, interaction)
- Technical details (3D/2D, physics, algorithms)
```

**Step 2 - Generate Code with Style:**
```
Generate complete p5.js animation code using this style:

[Prompt from Step 1]

Requirements:
- Complete HTML file (with p5.js CDN)
- Use WEBGL mode (if 3D)
- Parameterized config (CONFIG object)
- ES6 Class structure
- Responsive design
- Clear comments
```

**Step 3 - Verify and Optimize:**
- Preview directly in Gemini Canvas
- Adjust parameters until satisfied
- Copy complete code

### Step 3: Online Preview (p5.js Web Editor)

Visit [p5.js Web Editor](https://editor.p5js.org/) for real-time preview and debugging.

**Advantages:**
- No local setup required
- Real-time preview
- Built-in examples and docs
- Multi-file project support
- Easy sharing and embedding

### Step 4: Local Deployment & Optimization

Save code locally and start a dev server:

```bash
# Save the HTML file
# file: cosmic-dandelion.html

# Start local server
python3 -m http.server 8765

# Open in browser
open http://localhost:8765/cosmic-dandelion.html
```

**Optimization Checklist:**
- [ ] 3D effects smooth (use WEBGL)
- [ ] Colors harmonious (check color scheme)
- [ ] Animation natural (use easing and noise)
- [ ] Performance good (60fps target)
- [ ] Responsive works (windowResized)
- [ ] Parameters configurable (CONFIG object)

### Step 5: Visual Validation (MCP Tools)

Use visual tools for quality assurance:

```javascript
// testiv - Visual regression testing
testiv_capture("animation-baseline")
testiv_compare("animation-baseline", "animation-optimized")

// snapstack - Screenshot management
snapstack_capture("keyframe-1")
snapstack_timeline()

// photopea - Image post-processing
photopea_open("animation-screenshot.png")
```

### Step 6: Video Output

**Option A - Cap Screen Recording (Recommended):**
1. Open Cap app
2. Select browser window
3. Start recording
4. Stop and export

**Option B - ffmpeg:**
```bash
# Screen record on macOS
ffmpeg -f avfoundation -i "1" -t 30 -r 60 animation.mp4

# Compress
ffmpeg -i animation.mp4 -c:v libx264 -crf 23 animation-compressed.mp4
```

**Option C - ChatCut Video Editing:**
- Visit [ChatCut](https://app.chatcut.io/)
- Upload recorded video
- AI-assisted editing (subtitles, transitions, music)
- Export final version

## 🎨 Example Projects

### Cosmic Dandelion Animation

A beautiful 3D animation of birds flying away from a dandelion with particle effects.

**Features:**
- 500 birds with Fibonacci sphere distribution
- 600 twinkling stars background
- 100 atmospheric particles
- 15-frame trail system
- Multi-layer glow effects
- Perlin noise flight paths

**Files:**
- [`examples/cosmic-dandelion-3d.html`](./examples/cosmic-dandelion-3d.html) - Original version
- [`examples/cosmic-dandelion-enhanced.html`](./examples/cosmic-dandelion-enhanced.html) - Enhanced version
- [`examples/visual-test-suite.html`](./examples/visual-test-suite.html) - Side-by-side comparison

**Preview:**

![Cosmic Dandelion](./assets/cosmic-dandelion.png)

[🎬 Watch Video](./assets/cosmic-dandelion.mp4)

## 🛠️ Technical Highlights

### Fibonacci Sphere Distribution

```javascript
// Evenly distribute points on a sphere
const phi = acos(1 - 2 * (index + 0.5) / total);
const theta = PI * (1 + sqrt(5)) * (index + 0.5);

const position = createVector(
  sin(phi) * cos(theta),
  sin(phi) * sin(theta),
  cos(phi)
);
```

### Multi-Layer Glow Effects

```javascript
// Render 3-5 layers of gradient glow
for (let r = 5; r >= 1; r--) {
  let alpha = map(r, 5, 1, 20, 150);
  fill(glowColor + alpha.toString(16).padStart(2, '0'));
  sphere(radius * (1 + r * 0.15));
}
```

### Perlin Noise Natural Motion

```javascript
// Generate natural floating motion with noise
let noise = createVector(
  map(noise(pos.x * 0.01, time * 0.1), 0, 1, -0.5, 0.5),
  map(noise(pos.y * 0.01, time * 0.1), 0, 1, -0.5, 0.5),
  map(noise(pos.z * 0.01, time * 0.1), 0, 1, -0.5, 0.5)
);
velocity.add(noise);
```

### Trail System

```javascript
// Record position history
this.trail.push(this.pos.copy());
if (this.trail.length > CONFIG.trailLength) {
  this.trail.shift();
}

// Render fading trail
for (let i = 0; i < this.trail.length - 1; i++) {
  let alpha = map(i, 0, this.trail.length, 0, 100);
  stroke(color + alpha.toString(16).padStart(2, '0'));
  line(trail[i].x, trail[i].y, trail[i].z,
       trail[i+1].x, trail[i+1].y, trail[i+1].z);
}
```

## 📊 Quality Standards

### Visual Quality
- ✅ Cosmic-level beauty (depth, lighting, effects)
- ✅ Harmonious colors (theme-appropriate palette)
- ✅ Smooth animation (60fps, no stuttering)
- ✅ Rich details (particles, trails, glows)

### Code Quality
- ✅ Clear structure (Class-based architecture)
- ✅ Parameterized config (easy to adjust)
- ✅ Complete comments (key algorithms explained)
- ✅ Responsive design (adapts to screen size)

### Performance Standards
- ✅ Initial load < 2s
- ✅ Stable frame rate ≥ 60fps
- ✅ Memory usage < 200MB
- ✅ CPU usage < 50%

## 🔗 Resources

- **OpenProcessing**: https://openprocessing.org/
- **p5.js Web Editor**: https://editor.p5js.org/
- **Gemini Canvas**: https://gemini.google.com/app?hl=en_GB
- **ChatCut**: https://app.chatcut.io/
- **p5.js Documentation**: https://p5js.org/reference/
- **p5.js Examples**: https://p5js.org/examples/

## 💡 Best Practices

1. **Search First, Create Second** - Learn from excellent works
2. **AI-Assisted, Not Replaced** - Use AI for initial version, manually refine
3. **Online Debug, Local Deploy** - Use online tools for rapid iteration
4. **Parameterize Everything** - Centralize all adjustable parameters in CONFIG
5. **Performance First** - 60fps is the baseline
6. **Visual Validation Essential** - Screenshot comparison for quantifiable improvements

## 🐛 Troubleshooting

**Q: Gemini-generated code throws errors?**
A: Check p5.js version, ensure 1.7.0+, WEBGL mode requires full 3D API support.

**Q: Animation stuttering?**
A: Reduce particle count, lower draw complexity, use object pooling for memory optimization.

**Q: How to export high-quality video?**
A: Use Cap to record original video (60fps), then use ChatCut for lossless editing.

**Q: Can I use OpenProcessing code directly?**
A: Most can be used, but check the license. Recommended as reference for learning.

## 📈 Roadmap

- [ ] Support Three.js advanced 3D rendering
- [ ] Integrate Tone.js audio visualization
- [ ] Support WebGL Shader customization
- [ ] Integrate ml5.js machine learning interaction
- [ ] Support VR/AR output formats

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Andy AIPM**
- GitHub: [@andyai](https://github.com/andyai)
- Email: a61269592042@gmail.com

## 🙏 Acknowledgments

- [p5.js](https://p5js.org/) - The JavaScript library for creative coding
- [OpenProcessing](https://openprocessing.org/) - Creative coding community
- [Gemini](https://gemini.google.com/) - AI code generation
- [Claude](https://claude.ai/) - AI assistant platform
- [Kimi WebBridge](https://www.kimi.com/) - Browser automation

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by Andy AIPM

</div>
