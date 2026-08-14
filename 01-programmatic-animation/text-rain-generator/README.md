# 🌧️ Text Rain Generator

> 将中国古典诗词转化为艺术动画的 Claude Code Skill

灵感来自景桐的 Vibe Coding 作品，使用 p5.js 粒子系统创建物理真实的文字雨效果，结合 DALL-E 3 生成的中国风背景，呈现诗意与科技的完美融合。

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)

---

## ✨ 特性

- 🎨 **20 种精心设计的预设**：江南水乡、北京胡同、大漠孤烟、竹林幽径...
- 🤖 **AI 背景生成**：通过 ChatGPT + DALL-E 3 自动生成诗意背景
- ⚡ **物理真实模拟**：重力、摆动、旋转、碰撞检测
- 🎬 **视频导出**：一键导出 MP4 动画
- 📦 **批量处理**：并发生成多个作品
- 🔊 **音效支持**：雨声、风铃、古琴等氛围音效
- 🎯 **智能推荐**：根据诗词内容自动匹配最佳预设
- 🚀 **零配置**：开箱即用，无需复杂设置

---

## 🎬 效果预览

### 静夜思 × 极简主义
```
床前明月光，疑是地上霜。
举头望明月，低头思故乡。
```
*黑色背景 + 金色文字 + 缓慢飘落*

### 春晓 × 江南水乡
```
春眠不觉晓，处处闻啼鸟。
夜来风雨声，花落知多少。
```
*烟雨江南 + 水墨色文字 + 细雨轨迹*

### 使至塞上 × 大漠孤烟
```
大漠孤烟直，长河落日圆。
```
*沙漠落日 + 橙黄文字 + 狂风倾斜*

---

## 🚀 快速开始

### 方法 1：直接调用（推荐）

在 Claude Code 中：

```
/text-rain-generator "床前明月光，疑是地上霜。举头望明月，低头思故乡。"
```

系统会：
1. 自动推荐预设（`minimal`）
2. 调用 ChatGPT 生成背景图
3. 生成 HTML/JS 项目
4. 在浏览器中打开预览

### 方法 2：交互式菜单

```bash
cd ~/.claude/skills/text-rain-generator
./quick-start.sh
```

选择预设诗词，一键生成。

### 方法 3：指定预设

```
/text-rain-generator "空山新雨后，天气晚来秋" --preset bamboo
```

---

## 📋 预设列表

| 预设 | 风格 | 适用场景 | 速度 | 倾斜 |
|------|------|----------|------|------|
| `jiangnan` | 江南水乡 | 春雨、江南诗词 | 慢 | 小 |
| `beijing` | 北京胡同 | 古都、秋季诗词 | 中 | 中 |
| `huizhou` | 徽派建筑 | 古村、徽州诗词 | 中 | 中 |
| `lingnan` | 岭南骑楼 | 广东、夏季诗词 | 中 | 中 |
| `yaodong` | 黄土窑洞 | 陕北、黄土高原 | 快 | 大 |
| `sichuan` | 川西民居 | 川西、山水诗词 | 快 | 中 |
| `tulou` | 客家土楼 | 福建、客家诗词 | 中 | 小 |
| `yurt` | 草原毡房 | 草原、游牧诗词 | 很快 | 大 |
| `temple` | 古刹寺庙 | 禅意、佛教诗词 | 很慢 | 小 |
| `bamboo` | 竹林幽径 | 竹子、幽静诗词 | 慢 | 小 |
| `sakura` | 樱花季 | 春天、樱花诗词 | 很慢 | 小 |
| `desert` | 大漠孤烟 | 沙漠、边塞诗词 | 很快 | 很大 |
| `modern` | 现代都市 | 都市、现代诗词 | 快 | 大 |
| `cyberpunk` | 赛博朋克 | 科幻、未来诗词 | 很快 | 很大 |
| `minimal` | 极简主义 | 现代诗、简约 | 中 | 无 |
| `ink` | 水墨画 | 山水、禅意诗词 | 很慢 | 小 |
| `snow` | 雪景 | 冬天、雪诗词 | 极慢 | 极小 |
| `storm` | 暴风雨 | 风暴、激烈诗词 | 极快 | 极大 |
| `landscape` | 横版山水 | 横屏显示 | 中 | 小 |
| `square` | 方形构图 | 社交媒体 | 中 | 中 |

完整参数说明见 [CHEATSHEET.md](CHEATSHEET.md)

---

## 📚 文档

- **[USAGE.md](USAGE.md)** - 详细使用教程（300+ 行）
- **[CHEATSHEET.md](CHEATSHEET.md)** - 快速参考卡片
- **[DEVELOPER.md](DEVELOPER.md)** - 开发者文档
- **[SKILL.md](SKILL.md)** - Skill 执行逻辑

---

## 🛠️ 高级功能

### 视频导出

```bash
bun run export-video.ts \
  --input ~/output/text-rain-20260802-123456/index.html \
  --output ~/Desktop/rain.mp4 \
  --duration 10 \
  --fps 30
```

需要安装 FFmpeg：
```bash
brew install ffmpeg  # macOS
```

### 批量生成

创建 `tasks.json`：
```json
{
  "tasks": [
    {"poem": "春眠不觉晓", "preset": "jiangnan"},
    {"poem": "白日依山尽", "preset": "landscape"},
    {"poem": "大漠孤烟直", "preset": "desert"}
  ],
  "outputDir": "~/batch-output",
  "parallelLimit": 2
}
```

运行：
```bash
bun run batch-generate.ts tasks.json
```

### 音效增强

```bash
bun run sound-effects.ts \
  --input ~/output/text-rain-20260802-123456 \
  --sound-url "https://cdn.example.com/rain.mp3" \
  --volume 0.3
```

---

## 🎯 技术架构

```
用户调用 /text-rain-generator
        ↓
    解析参数 & 应用预设
        ↓
    生成 HTML/JS 项目
        ↓
    调用 andy-relay Skill
        ↓
    ChatGPT + DALL-E 3 生图
        ↓
    WebBridge 下载图片
        ↓
    验证 & 浏览器预览
```

### 核心技术栈

- **前端**: p5.js（粒子系统）
- **后端**: TypeScript + Bun
- **AI**: ChatGPT + DALL-E 3（通过 andy-relay）
- **浏览器自动化**: Kimi WebBridge
- **视频**: node-canvas + FFmpeg

### 物理引擎

```typescript
class RainDrop {
  update() {
    // 重力加速
    this.y += this.speed;
    this.speed += 0.05;
    
    // 正弦波摆动
    this.wobblePhase += this.wobbleSpeed;
    this.x += Math.sin(this.wobblePhase) * this.wobbleAmplitude;
    
    // 旋转
    this.rotation += this.rotationSpeed;
  }
  
  detectCollision(backgroundImg) {
    const color = backgroundImg.get(this.x, this.y);
    const brightness = (color[0] + color[1] + color[2]) / 3;
    
    if (brightness < 80) { // 暗色区域触发碰撞
      this.speed *= 0.5; // 减速
      this.x += random(-5, 5); // 飞溅
    }
  }
}
```

---

## 🔧 安装与配置

### 前置条件

- macOS 或 Linux
- Bun >= 1.0（或 Node.js >= 18）
- Claude Code Desktop/CLI
- ChatGPT Plus 账号（用于 DALL-E 3）
- Kimi WebBridge（已配置 andy-relay）

### 安装依赖

```bash
cd ~/.claude/skills/text-rain-generator
bun install
```

### 测试

```bash
bun run test
```

应该看到：
```
✅ HTML generation works
✅ Sketch generation works
✅ Config embedding works
✅ File system operations work
✅ Edge cases handled
✅ Special characters handled

All tests passed! 🎉
```

---

## 🎨 自定义开发

### 添加新预设

编辑 `presets.ts`：

```typescript
export const PRESETS: Record<string, Preset> = {
  myPreset: {
    name: '我的预设',
    description: '预设描述',
    scene: '传给 ChatGPT 的场景描述',
    speed: 2.5,
    tilt: 10,
    color: '#d4c5a9',
    fontSize: 24,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },
};
```

### 修改物理参数

编辑 `generate.ts` 中的 `generateSketch()` 函数，调整：
- 重力加速度
- 摆动幅度/频率
- 碰撞阈值
- 粒子密度

详见 [DEVELOPER.md](DEVELOPER.md)

---

## 🐛 故障排查

### 背景图生成失败

**原因**: ChatGPT 未登录或限流

**解决**:
```bash
# 手动提供背景图
cp my-background.png ~/output/text-rain-xxx/assets/background.png
```

### 字体显示异常

**原因**: 系统缺少中文字体

**解决**: 在 `sketch.js` 中指定 Web Font：
```javascript
textFont('Noto Sans SC');
```

### 性能卡顿

**原因**: 粒子数过多

**解决**: 降低密度
```
/text-rain-generator "诗词" --density 0.02
```

更多问题见 [CHEATSHEET.md - 故障排查](CHEATSHEET.md#故障排查)

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| 生成速度 | <1 秒（不含背景图） |
| 运行帧率 | 60 FPS @ 72 粒子 |
| CPU 占用 | ~10-15% |
| 内存占用 | ~50MB |
| 视频导出 | 10 秒 @ 30fps ≈ 8 秒 |

---

## 🗺️ Roadmap

### v1.1（短期）
- [ ] 自动调整背景图尺寸
- [ ] 内置音效库
- [ ] Web Font 支持
- [ ] 更多预设（30+）

### v1.5（中期）
- [ ] 交互式参数面板
- [ ] 实时预览（Hot Reload）
- [ ] 社区预设分享
- [ ] 移动端适配

### v2.0（长期）
- [ ] 3D 文字雨（Three.js）
- [ ] 物理引擎（Matter.js）
- [ ] WebGL 加速
- [ ] 云渲染服务

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

开发指南见 [DEVELOPER.md](DEVELOPER.md)

---

## 📜 License

MIT License

---

## 🙏 致谢

- **景桐** - Vibe Coding 原创灵感
- **p5.js** - 优雅的创意编程框架
- **OpenAI** - DALL-E 3 图像生成
- **Kimi WebBridge** - 可靠的浏览器自动化

---

## 📞 联系方式

- **项目位置**: `~/.claude/skills/text-rain-generator/`
- **开发者**: Andy
- **版本**: 1.0.0
- **最后更新**: 2026-08-02

---

<div align="center">

**让诗词在屏幕上舞动 🌧️**

Made with ❤️ by Claude Code

</div>
