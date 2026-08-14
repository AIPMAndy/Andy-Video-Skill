---
name: andy-p5js
version: 1.0.0
description: AI-powered p5.js creative coding workflow - from inspiration to animation
author: Andy
tags: [p5js, creative-coding, animation, visual-effects, generative-art]
dependencies: [webbridge]
---

# Andy-P5JS

AI驱动的p5.js创意编码工作流 - 从灵感到动画一站式解决方案。

## 🎯 核心能力

1. **灵感发现** - 从 OpenProcessing 搜索优质模板
2. **代码生成** - 使用 Gemini 3.1 Pro Canvas 生成高质量代码
3. **实时预览** - p5.js Web Editor 在线预览和调试
4. **本地优化** - 本地部署和视觉效果增强
5. **视觉验证** - 使用 testiv/snapstack 进行视觉回归测试
6. **视频输出** - Cap 录屏或 ChatCut 剪辑

## 🔄 标准工作流

```
灵感搜索 → AI生成 → 在线预览 → 本地优化 → 视觉验证 → 视频输出
   ↓           ↓          ↓          ↓          ↓          ↓
OpenProcessing  Gemini   p5js.org   本地服务器   MCP工具    Cap/ChatCut
```

## 📋 使用场景

- 创意动画快速原型
- 生成艺术作品
- 交互式可视化
- 教学演示动画
- 社交媒体视觉内容

## 🎨 示例项目

- 宇宙级蒲公英飞鸟动画
- 3D粒子效果系统
- Fibonacci球体分布算法
- 多层辉光渲染

## ⚙️ 配置要求

- webbridge MCP 服务器（必需）
- testiv/snapstack（可选，用于视觉测试）
- photopea（可选，用于图像后处理）
- rrweb-stack（可选，用于交互录制）
- Cap 或 ffmpeg（可选，用于视频录制）

## 🚀 快速开始

```bash
# 调用技能
/andy-p5js

# 或指定需求
/andy-p5js 创建一个3D粒子爆炸效果
```

---

## 实现步骤

### Step 1: 灵感搜索（OpenProcessing）

使用 webbridge 访问 https://openprocessing.org/ 搜索相关主题的优质模板。

**搜索策略：**
- 使用英文关键词（如 "particle system", "3D animation", "generative art"）
- 筛选高点赞数/收藏数的作品
- 优先选择有清晰代码结构的项目
- 注意查看开源协议

**webbridge 操作：**
```javascript
// 1. 访问 OpenProcessing
navigate("https://openprocessing.org/")

// 2. 搜索相关主题
fill("input[type='search']", "particle system 3D")
send_keys("Enter")

// 3. 截图保存灵感
screenshot("openprocessing-inspiration.png")
```

### Step 2: AI代码生成（Gemini Canvas）

**三步提示词工程法：**

**第一步 - 生成动画风格提示词：**
```
请为以下p5.js动画需求生成一个详细的视觉风格描述提示词：

需求：[用户需求]

输出格式：
- 视觉风格（色彩、光影、氛围）
- 动画效果（粒子数量、运动轨迹、交互方式）
- 技术要点（3D/2D、物理引擎、算法选择）
```

**第二步 - 使用生成的提示词生成代码：**
```
使用以下风格描述，生成完整的p5.js动画代码：

[第一步生成的提示词]

要求：
- 完整的HTML文件（包含p5.js CDN）
- 使用WEBGL模式（如果是3D）
- 参数化配置（CONFIG对象）
- ES6 Class结构
- 响应式设计
- 注释清晰
```

**第三步 - 验证和优化：**
- 在 Gemini Canvas 中直接预览生成的代码
- 调整参数直到满意
- 复制完整代码

**webbridge 操作：**
```javascript
// 访问 Gemini Canvas
navigate("https://gemini.google.com/app?hl=en_GB")

// 选择 Gemini 3.1 Pro
click("button[aria-label='Open mode picker']")
// 选择 Pro 模式

// 输入提示词
fill("textarea[aria-label='Enter a prompt']", promptText)
send_keys("Enter")

// 等待生成并截图
screenshot("gemini-generated-code.png")
```

### Step 3: 在线预览（p5.js Web Editor）

访问 https://editor.p5js.org/ 进行在线预览和快速迭代。

**优势：**
- 无需本地环境配置
- 实时预览和调试
- 内置示例和文档
- 支持多文件项目
- 可分享和嵌入

**webbridge 操作：**
```javascript
// 1. 访问 p5.js Editor
navigate("https://editor.p5js.org/")

// 2. 粘贴代码（需要拆分为 sketch.js）
// 注意：将HTML中的<script>部分提取到 sketch.js

// 3. 点击运行
click("button[aria-label='Play']")

// 4. 截图预览
screenshot("p5js-editor-preview.png")
```

### Step 4: 本地部署优化

将代码保存到本地并启动开发服务器。

**操作流程：**
```bash
# 1. 保存文件
# 使用 Write 工具保存为 .html

# 2. 启动本地服务器
python3 -m http.server 8765 &

# 3. 使用 webbridge 打开
navigate("http://localhost:8765/animation.html")

# 4. 视觉优化
# - 调整参数（粒子数量、颜色、速度）
# - 增强效果（多层辉光、拖尾、粒子系统）
# - 性能优化（降低复杂度或优化算法）
```

**优化检查清单：**
- [ ] 3D效果是否流畅（使用WEBGL）
- [ ] 色彩是否和谐（检查配色方案）
- [ ] 动画是否自然（使用缓动和噪声）
- [ ] 性能是否达标（60fps目标）
- [ ] 响应式是否正常（windowResized）
- [ ] 参数是否可配置（CONFIG对象）

### Step 5: 视觉验证（MCP工具）

使用视觉工具进行质量验证。

**testiv - 视觉回归测试：**
```javascript
// 建立基线
testiv_capture("animation-baseline")

// 修改后对比
testiv_compare("animation-baseline", "animation-optimized")
```

**snapstack - 截图管理：**
```javascript
// 捕获关键帧
snapstack_capture("keyframe-1")
snapstack_capture("keyframe-2")

// 生成时间轴
snapstack_timeline()
```

**photopea - 图像后处理：**
```javascript
// 增强截图效果
photopea_open("animation-screenshot.png")
// 手动调整后保存
```

### Step 6: 视频输出

**方案A - Cap录屏（推荐）：**
```bash
# 使用 Mac 上的 Cap 应用
# 1. 打开 Cap
# 2. 选择浏览器窗口
# 3. 开始录制
# 4. 停止并导出
```

**方案B - ffmpeg录屏：**
```bash
# macOS 屏幕录制
ffmpeg -f avfoundation -i "1" -t 30 -r 60 animation.mp4

# 压缩优化
ffmpeg -i animation.mp4 -c:v libx264 -crf 23 -preset medium animation-compressed.mp4
```

**方案C - rrweb-stack交互录制：**
```javascript
// 录制用户交互
rrweb_start_recording()

// 执行操作...

// 停止并保存
rrweb_stop_recording("animation-interactive.json")
```

**视频剪辑 - ChatCut：**
- 访问 https://app.chatcut.io/
- 上传录制的视频
- AI辅助剪辑（自动字幕、转场、配乐）
- 导出最终版本

## 📊 质量标准

### 视觉质量
- ✅ 宇宙级美感（多层次、深度感、光影效果）
- ✅ 色彩和谐（配色方案符合主题）
- ✅ 动画流畅（60fps，无卡顿）
- ✅ 细节丰富（粒子、拖尾、辉光）

### 代码质量
- ✅ 结构清晰（Class-based架构）
- ✅ 参数化配置（易于调整）
- ✅ 注释完整（关键算法说明）
- ✅ 响应式设计（适配不同屏幕）

### 性能标准
- ✅ 初始加载 < 2秒
- ✅ 帧率稳定 ≥ 60fps
- ✅ 内存占用 < 200MB
- ✅ CPU使用率 < 50%

## 🎓 技术要点

### Fibonacci球体分布算法
```javascript
// 在球面上均匀分布点
const phi = acos(1 - 2 * (index + 0.5) / total);
const theta = PI * (1 + sqrt(5)) * (index + 0.5);

const position = createVector(
  sin(phi) * cos(theta),
  sin(phi) * sin(theta),
  cos(phi)
);
```

### 多层辉光效果
```javascript
// 渲染3-5层渐变光晕
for (let r = 5; r >= 1; r--) {
  let alpha = map(r, 5, 1, 20, 150);
  fill(glowColor + alpha.toString(16).padStart(2, '0'));
  sphere(radius * (1 + r * 0.15));
}
```

### Perlin噪声自然运动
```javascript
// 使用噪声生成自然飘动
let noise = createVector(
  map(noise(pos.x * 0.01, time * 0.1), 0, 1, -0.5, 0.5),
  map(noise(pos.y * 0.01, time * 0.1), 0, 1, -0.5, 0.5),
  map(noise(pos.z * 0.01, time * 0.1), 0, 1, -0.5, 0.5)
);
velocity.add(noise);
```

### 轨迹拖尾系统
```javascript
// 记录历史位置
this.trail.push(this.pos.copy());
if (this.trail.length > CONFIG.trailLength) {
  this.trail.shift();
}

// 渲染渐变拖尾
for (let i = 0; i < this.trail.length - 1; i++) {
  let alpha = map(i, 0, this.trail.length, 0, 100);
  stroke(color + alpha.toString(16).padStart(2, '0'));
  line(trail[i].x, trail[i].y, trail[i].z,
       trail[i+1].x, trail[i+1].y, trail[i+1].z);
}
```

## 🔗 资源链接

- **OpenProcessing**: https://openprocessing.org/
- **p5.js Web Editor**: https://editor.p5js.org/
- **Gemini Canvas**: https://gemini.google.com/app?hl=en_GB
- **ChatCut**: https://app.chatcut.io/
- **p5.js 文档**: https://p5js.org/reference/
- **p5.js 示例**: https://p5js.org/examples/

## 💡 最佳实践

1. **先搜索后创造** - 站在巨人的肩膀上，从优秀作品中学习
2. **AI辅助而非替代** - 用AI生成初版，人工精调优化
3. **在线调试本地部署** - 利用在线工具快速迭代，本地环境深度优化
4. **参数化一切** - CONFIG对象集中管理所有可调参数
5. **性能优先** - 60fps是底线，牺牲细节保证流畅度
6. **视觉验证必不可少** - 截图对比，确保优化效果可量化

## 🐛 常见问题

**Q: Gemini生成的代码运行报错？**
A: 检查p5.js版本，确保使用1.7.0+，WEBGL模式需要完整的3D API支持。

**Q: 动画卡顿怎么办？**
A: 减少粒子数量、降低绘制复杂度、使用对象池优化内存分配。

**Q: 如何导出高质量视频？**
A: 使用Cap录制原始视频（60fps），然后用ChatCut进行无损剪辑。

**Q: OpenProcessing的代码能直接用吗？**
A: 大部分可以，但需要注意开源协议，建议作为参考学习而非直接复制。

## 📈 未来扩展

- [ ] 支持Three.js高级3D渲染
- [ ] 集成Tone.js音频可视化
- [ ] 支持WebGL Shader自定义
- [ ] 集成ml5.js机器学习交互
- [ ] 支持VR/AR输出格式

---

**License**: MIT  
**Repository**: https://github.com/andyai/andy-p5js (待创建)  
**Author**: Andy AIPM  
**Version**: 1.0.0
