# Text Rain Generator - 完整使用指南

生成景桐风格的"文字雨"动效，通过 AI 辅助完成从生图到动画的全流程。

## 📦 快速开始

### 基础用法

```bash
/text-rain-generator "床前明月光，疑是地上霜"
```

Claude Code 会自动：
1. 生成完整的 p5.js 项目
2. 通过 ChatGPT 生成背景图
3. 启动本地预览

### 使用预设

```bash
/text-rain-generator "清明时节雨纷纷" --preset jiangnan
```

### 自定义参数

```bash
/text-rain-generator "山重水复疑无路" \
  --scene "苏州园林青瓦屋檐" \
  --speed 3 \
  --tilt 15 \
  --color "#e8d5b7"
```

## 🎨 可用预设（20种）

### 地域风格
- `jiangnan` - 江南烟雨：细雨绵绵，诗意江南
- `beijing` - 北京胡同：四合院屋檐，雨落青石板
- `huizhou` - 徽派建筑：马头墙，黑瓦白墙
- `lingnan` - 岭南骑楼：广州民国风情
- `sichuan` - 川西民居：藏式碉楼，彩绘梁柱
- `tulou` - 福建土楼：客家圆楼
- `yaodong` - 陕北窑洞：黄土高原
- `yurt` - 草原蒙古包：游牧文化

### 特殊场景
- `temple` - 古寺钟声：禅意空灵
- `bamboo` - 竹林深处：翠竹摇曳
- `sakura` - 樱花纷飞：粉色花瓣
- `desert` - 大漠孤烟：西域戈壁

### 艺术风格
- `modern` - 都市夜雨：霓虹灯光
- `cyberpunk` - 赛博雨夜：未来都市
- `minimal` - 极简黑白：现代简约
- `ink` - 水墨意境：泼墨山水

### 天气效果
- `snow` - 飘雪：白色雪花效果
- `storm` - 暴雨如注：狂风骤雨

### 格式特化
- `landscape` - 横屏观影：16:9，适合视频网站
- `square` - 社交媒体：1:1，适合 Instagram/微信

## 🛠️ 命令行参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--preset <name>` | 自动推荐 | 使用预设配置 |
| `--scene <desc>` | 根据预设 | 背景场景描述（传递给 ChatGPT） |
| `--speed <num>` | 2.5 | 雨滴下落速度（1-5） |
| `--tilt <deg>` | 10 | 最大倾斜角度（0-30度） |
| `--color <hex>` | #d4c5a9 | 文字颜色（十六进制） |
| `--font-size <px>` | 24 | 字体大小 |
| `--canvas-width <px>` | 1080 | 画布宽度 |
| `--canvas-height <px>` | 1920 | 画布高度（默认竖屏） |
| `--output <dir>` | ./text-rain-output | 输出目录 |
| `--no-preview` | false | 不自动打开预览 |
| `--list-presets` | - | 列出所有预设 |

## 📹 高级功能

### 1. 导出视频（逐帧渲染）

```bash
cd ~/.claude/skills/text-rain-generator

# 安装依赖
npm install canvas @types/canvas

# 导出帧序列
node export-video.ts \
  --project ~/Documents/AICode/text-rain-demo \
  --output ./frames \
  --duration 10 \
  --fps 30

# 使用 FFmpeg 合成视频
ffmpeg -framerate 30 -i frames/frame_%05d.png \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p \
  output.mp4
```

**参数说明**:
- `--project`: 项目目录路径
- `--output`: 帧序列输出目录
- `--duration`: 视频时长（秒）
- `--fps`: 帧率（30/60）
- `--format`: 帧格式（png/jpg）
- `--quality`: JPG 质量（0-100）

### 2. 批量生成

```bash
cd ~/.claude/skills/text-rain-generator

# 创建示例配置
node batch-generate.ts --init

# 编辑 batch-config.json
vim batch-config.json

# 批量生成
node batch-generate.ts --config batch-config.json
```

**配置文件示例**:
```json
{
  "tasks": [
    {
      "text": "床前明月光，疑是地上霜",
      "preset": "jiangnan",
      "outputName": "jingye-si"
    },
    {
      "text": "春眠不觉晓，处处闻啼鸟",
      "preset": "jiangnan",
      "outputName": "chun-xiao"
    }
  ],
  "baseOutputDir": "./batch-output",
  "generateImages": false,
  "parallelLimit": 3
}
```

批量生成会创建：
- 每个诗句的独立项目文件夹
- 一个索引页面（`index.html`）统一预览

### 3. 添加音效

在生成的项目中手动添加音效：

1. 编辑 `sketch.js`，在 `preload()` 中添加：
```javascript
let rainSound;
function preload() {
  backgroundImg = loadImage('assets/background.png');
  rainSound = loadSound('assets/rain.mp3'); // 添加音效文件
}
```

2. 在 `setup()` 中初始化：
```javascript
rainSound.loop();
rainSound.setVolume(0.3);
```

3. 添加控制（在 `keyPressed()` 中）：
```javascript
if (key === 'm' || key === 'M') {
  if (rainSound.isPlaying()) {
    rainSound.pause();
  } else {
    rainSound.loop();
  }
}
```

**推荐音效资源**:
- [Freesound](https://freesound.org/) - 免费音效库
- [OpenGameArt](https://opengameart.org/) - 游戏音效
- [Zapsplat](https://www.zapsplat.com/) - 高质量音效

## 🎮 交互控制

运行时的键盘和鼠标控制：

| 操作 | 功能 |
|------|------|
| 鼠标点击 / 空格 | 暂停/继续动画 |
| R 键 | 重置所有粒子 |
| M 键 | 静音/取消静音（需添加音效） |
| 刷新页面 | 重新开始 |

## 🐛 故障排查

### 问题：背景图未生成

**原因**: ChatGPT 限流或登录过期

**解决方案**:
1. 手动登录 ChatGPT 网页版
2. 重新运行 `/text-rain-generator`
3. 或手动上传 1080×1920 的黑白背景图到 `assets/background.png`

**手动生成背景图**:
1. 使用 Midjourney/Stable Diffusion 生成
2. 提示词参考 `image-task.json` 中的 prompt
3. 调整尺寸为 1080×1920（使用 `sips -z 1920 1080 image.png`）

### 问题：预览页面空白

**症状**: 浏览器打开但只看到黑屏

**排查步骤**:
1. 打开浏览器控制台（F12）查看错误
2. 检查 `assets/background.png` 是否存在
3. 确认使用本地服务器（不是直接打开 HTML）
4. 验证 `sketch.js` 语法无错误

**常见错误**:
- `Failed to load resource: net::ERR_FILE_NOT_FOUND` → 背景图不存在
- `CORS policy` → 需要使用本地服务器
- `p5.js is not defined` → CDN 加载失败，检查网络

### 问题：中文字符显示为方块

**原因**: 系统缺少中文字体

**解决方案**:
1. 确保系统已安装楷体/宋体
2. 编辑 `sketch.js` 第 23 行：
```javascript
textFont('Arial, sans-serif'); // 使用通用字体
```

3. 或使用 Web Font（Google Fonts 的 Noto Sans SC）

### 问题：动画卡顿

**原因**: 粒子数过多或设备性能不足

**解决方案**:
1. 减少粒子数：编辑 `sketch.js` 第 29 行
```javascript
const particleCount = Math.max(poem.length * 2, 50); // 改为 *2
```

2. 降低画布分辨率：`--canvas-width 720 --canvas-height 1280`

3. 关闭其他占用 GPU 的程序

### 问题：图片尺寸不匹配

**症状**: 下载的图片不是 1080×1920

**解决方案**:
```bash
# macOS/Linux (使用 sips)
sips -z 1920 1080 assets/background.png

# 或使用 ImageMagick
convert assets/background.png -resize 1080x1920! assets/background.png
```

## 📊 性能优化

### 优化粒子数

根据诗句长度动态调整：
```javascript
// 短诗（<20字）: ×3
// 中诗（20-50字）: ×2
// 长诗（>50字）: ×1.5
const particleCount = poem.length < 20 
  ? poem.length * 3 
  : poem.length * 2;
```

### 优化渲染

1. **降低帧率**（适合录屏）:
```javascript
function setup() {
  // ...
  frameRate(30); // 默认 60
}
```

2. **使用离屏渲染**（大量粒子时）:
```javascript
let pg; // 离屏 canvas
function setup() {
  pg = createGraphics(width, height);
}
```

### 浏览器选择

推荐性能：
1. Chrome/Edge（最佳）
2. Firefox
3. Safari（macOS 上硬件加速更好）

## 🎓 技术细节

### p5.js 粒子系统

**核心概念**:
- 每个字符是一个独立的 `RainDrop` 对象
- 物理模拟：重力、正弦波摆动、旋转、碰撞检测
- 粒子循环利用（而非创建/销毁）

**关键参数**:
```javascript
class RainDrop {
  speed: number;      // 下落速度
  rotation: number;   // 当前旋转角
  wobblePhase: number; // 摆动相位
  alpha: number;      // 透明度
  scale: number;      // 缩放比例
}
```

### 碰撞检测算法

```javascript
detectCollision() {
  // 采样背景像素亮度
  const imgColor = backgroundImg.get(this.x, this.y);
  const brightness = (imgColor[0] + imgColor[1] + imgColor[2]) / 3;

  // 深色区域触发碰撞
  if (brightness < 80) {
    this.speed *= 0.5;  // 减速
    this.x += random(-5, 5); // 溅射
  }
}
```

**阈值调整**:
- `brightness < 60`: 敏感（更多碰撞）
- `brightness < 100`: 宽松（更少碰撞）

### 性能分析

**内存占用**:
- 基础项目：~5MB
- 100 个粒子：+2MB
- 背景图（1080×1920）：~2-3MB

**CPU 占用**:
- 60fps @ 72 粒子：~10-15%（现代 CPU）
- 瓶颈：碰撞检测（像素采样）

## 📚 参考资料

- [p5.js 官方文档](https://p5js.org/reference/)
- [粒子系统教程 - The Coding Train](https://thecodingtrain.com/particles)
- [景桐 Vibe Coding 案例](https://twitter.com/jingtonic)
- [WebBridge 使用文档](https://www.kimi.com/zh-cn/features/webbridge)

## 🤝 贡献

发现 bug 或有功能建议？
- 位置：`~/.claude/skills/text-rain-generator/`
- 编辑相应文件并测试
- 运行测试：`bun run test.ts`

## 📄 许可证

MIT License - 自由使用和修改

---

生成工具版本: 1.0.0  
最后更新: 2026-08-02
