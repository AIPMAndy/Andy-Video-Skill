---
name: text-rain-generator
description: Generate artistic text rain animation with p5.js. Input poem/text + scene description, automatically generates background image via ChatGPT (through andy-relay), outputs complete runnable p5.js project with configurable rain physics (speed, tilt, collision).
---

# Text Rain Generator

将诗句/文字转换成艺术化的"文字雨"动效，参考景桐的 Vibe Coding 风格。

## 核心能力

1. **智能生图**：通过 `/andy-relay` 调度 ChatGPT 生成黑白老照片风格的背景图
2. **物理引擎**：p5.js 粒子系统模拟真实雨滴效果（重力、风、碰撞）
3. **参数化控制**：可调节雨速、倾斜、颜色、布局等
4. **即开即用**：输出完整 HTML 文件，浏览器直接运行

## 使用方式

### 基础模式（最快）
```
/text-rain-generator "床前明月光，疑是地上霜" --scene "江南老宅屋檐"
```

### 高级模式（精细调参）
```
/text-rain-generator "山重水复疑无路，柳暗花明又一村" \
  --scene "苏州园林青瓦屋檐，斑驳墙壁" \
  --speed 3 \
  --tilt 15 \
  --color "#e8d5b7" \
  --no-preview
```

## 参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--scene` | "中式老宅屋檐" | 背景场景描述，传递给 ChatGPT 生图 |
| `--speed` | 2.5 | 雨滴下落速度（1-5） |
| `--tilt` | 10 | 最大倾斜角度（度） |
| `--color` | "#d4c5a9" | 文字颜色（十六进制） |
| `--font-size` | 24 | 字体大小（px） |
| `--canvas-width` | 1080 | 画布宽度 |
| `--canvas-height` | 1920 | 画布高度（默认竖屏） |
| `--no-preview` | false | 不自动打开浏览器预览 |
| `--output` | `./text-rain-output/` | 输出目录 |

## 工作流程

### 第1步：解析输入
- 拆解诗句为字符数组
- 验证参数合法性
- 生成项目文件夹结构

### 第2步：生成背景图（通过 andy-relay）

调用 `/andy-relay` 发送任务到 ChatGPT：

```json
{
  "objective": "Generate background image for text rain animation",
  "deliverable": "One PNG image, 1080x1920, black and white old photo style",
  "context": {
    "scene": "{用户提供的场景描述}",
    "style": "monochrome, vintage, film grain, high contrast",
    "composition": "bottom 2/3 shows roof tiles/eaves, top 1/3 empty for rain"
  },
  "prompt": "Generate a black and white vintage photograph: {scene}. Composition: traditional Chinese roof tiles occupy bottom 60%, weathered texture with visible gaps between tiles. Top 40% is empty sky/wall for text overlay. High contrast, film grain, 1980s photo quality. Vertical format 1080x1920.",
  "acceptance": [
    "Image resolution exactly 1080x1920",
    "Monochrome (no color)",
    "Clear roof/eaves structure in bottom portion",
    "Sufficient empty space at top"
  ]
}
```

**重要**：
- 使用 ChatGPT 的 DALL-E 3 生图能力
- 下载生成的图片到项目 `assets/` 目录
- 验证图片尺寸和风格

### 第3步：生成 p5.js 代码

创建核心文件：

#### `index.html`
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Text Rain - {首句诗}</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.7.0/p5.min.js"></script>
  <script src="sketch.js"></script>
  <style>
    body {
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      background: #1a1a1a;
    }
    canvas {
      box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
  </style>
</head>
<body></body>
</html>
```

#### `sketch.js`
核心逻辑：

```javascript
// 全局变量
let particles = [];
let backgroundImg;
let poem = []; // 诗句字符数组
let config = {
  speed: {SPEED},
  tilt: {TILT},
  color: '{COLOR}',
  fontSize: {FONT_SIZE},
  canvasWidth: {CANVAS_WIDTH},
  canvasHeight: {CANVAS_HEIGHT}
};

// p5.js 生命周期
function preload() {
  backgroundImg = loadImage('assets/background.png');
}

function setup() {
  createCanvas(config.canvasWidth, config.canvasHeight);
  textFont('STKaiti'); // 楷体，适合中文诗词
  textSize(config.fontSize);
  textAlign(CENTER, CENTER);
  
  // 初始化粒子
  poem = '{POEM_TEXT}'.split('');
  for (let i = 0; i < poem.length * 3; i++) {
    particles.push(new RainDrop(random(poem)));
  }
}

function draw() {
  // 渲染背景
  image(backgroundImg, 0, 0, width, height);
  
  // 更新和渲染粒子
  for (let p of particles) {
    p.update();
    p.display();
    
    // 循环利用粒子
    if (p.y > height) {
      p.reset();
    }
  }
}

// 雨滴类
class RainDrop {
  constructor(char) {
    this.char = char;
    this.reset();
  }
  
  reset() {
    this.x = random(width * 0.1, width * 0.9); // 左右留白
    this.y = random(-500, -50);
    this.speed = random(config.speed * 0.8, config.speed * 1.2);
    this.rotation = random(-config.tilt, config.tilt);
    this.wobble = random(-0.5, 0.5); // 左右摆动
    this.alpha = random(150, 255);
  }
  
  update() {
    // 重力加速
    this.y += this.speed;
    this.x += sin(this.y * 0.01) * this.wobble;
    
    // 碰撞检测：屋檐区域（底部 60%）
    if (this.y > height * 0.4) {
      let imgColor = backgroundImg.get(this.x, this.y);
      let brightness = (imgColor[0] + imgColor[1] + imgColor[2]) / 3;
      
      // 碰到深色区域（瓦片）改变轨迹
      if (brightness < 100) {
        this.speed *= 0.95; // 减速
        this.x += random(-2, 2); // 随机溅开
        this.rotation += random(-5, 5);
      }
    }
  }
  
  display() {
    push();
    translate(this.x, this.y);
    rotate(radians(this.rotation));
    fill(config.color + hex(this.alpha, 2));
    noStroke();
    text(this.char, 0, 0);
    pop();
  }
}
```

### 第4步：输出和验证

生成文件结构：
```
text-rain-output/
├── index.html
├── sketch.js
├── assets/
│   └── background.png
├── README.md
└── preview.sh  # 快速启动脚本
```

#### `README.md`
```markdown
# 文字雨动效 - {诗句首句}

## 快速运行

### 方法1：直接打开
双击 `index.html` 在浏览器中打开

### 方法2：本地服务器（推荐）
```bash
# Python 3
python -m http.server 8000

# 或使用 Node.js
npx serve .
```

访问 http://localhost:8000

## 录屏导出

### macOS
⌘ + Shift + 5 选择录制区域

### Windows
Win + G 打开 Xbox Game Bar

### 通用方案
使用 OBS Studio 录制浏览器窗口

## 参数调整

编辑 `sketch.js` 中的 `config` 对象：

- `speed`: 雨速（1-5）
- `tilt`: 倾斜角度（0-30）
- `color`: 文字颜色
- `fontSize`: 字号

## 技术栈

- p5.js 1.7.0
- 纯前端，无需构建
```

#### `preview.sh`
```bash
#!/bin/bash
# 自动启动本地服务器并打开浏览器

echo "🌧️  启动文字雨预览..."

# 检测可用工具
if command -v python3 &> /dev/null; then
    echo "使用 Python 服务器 (http://localhost:8000)"
    python3 -m http.server 8000 &
    SERVER_PID=$!
    sleep 2
    open http://localhost:8000
elif command -v npx &> /dev/null; then
    echo "使用 Node.js serve"
    npx serve . -l 8000 &
    SERVER_PID=$!
    sleep 2
    open http://localhost:8000
else
    echo "⚠️  未找到 Python 或 Node.js，请手动打开 index.html"
    open index.html
    exit 0
fi

echo "✅ 预览已启动！按 Ctrl+C 停止服务器"
trap "kill $SERVER_PID" EXIT
wait $SERVER_PID
```

## 验证清单

自动执行以下检查：

- [ ] 背景图已下载且尺寸正确（1080x1920）
- [ ] 诗句文字已正确拆分
- [ ] `sketch.js` 语法无错误
- [ ] 浏览器控制台无报错
- [ ] 粒子系统正常运行（至少100帧无卡顿）
- [ ] 碰撞效果触发正常

如果 `--no-preview` 未设置，自动通过 WebBridge 打开预览。

## 故障排查

### 图片生成失败
- **原因**：ChatGPT 限流/登录过期
- **解决**：手动上传 1080x1920 黑白屋檐图到 `assets/background.png`

### 中文乱码
- **原因**：字体未加载
- **解决**：在 `setup()` 中指定系统字体或使用 Web Font

### 性能卡顿
- **原因**：粒子数过多
- **解决**：减少 `particles` 初始化数量（默认 `poem.length * 3`）

## 进阶扩展

### 添加音效
```javascript
let rainSound;
function preload() {
  backgroundImg = loadImage('assets/background.png');
  rainSound = loadSound('assets/rain.mp3');
}
function setup() {
  // ...
  rainSound.loop();
}
```

### 导出视频（Node.js）
使用 `p5.js` + `canvas` 库逐帧导出：
```bash
npm install canvas p5
node export-frames.js  # 生成帧序列
ffmpeg -i frame_%04d.png -c:v libx264 output.mp4
```

## Claude Code 执行流程

当用户调用 `/text-rain-generator` 时，按以下步骤执行：

### Step 1: 解析参数并生成项目

```bash
cd ~/.claude/skills/text-rain-generator
node cli.ts "{用户提供的诗句}" {其他参数}
```

CLI 会输出 JSON 格式的结果，包含：
- `outputDir`: 项目输出目录
- `taskPacketPath`: ChatGPT 任务包路径
- `backgroundPath`: 背景图目标路径
- `indexPath`: HTML 入口文件路径
- `config`: 完整配置对象

### Step 2: 调用 andy-relay 生成背景图

读取 `taskPacketPath` 中的任务包，通过 `/andy-relay` 调度 ChatGPT：

```javascript
// 伪代码示例
const taskPacket = JSON.parse(fs.readFileSync(taskPacketPath));

// 调用 andy-relay
await invokeSkill('andy-relay', {
  provider: 'chatgpt',
  task: taskPacket,
  downloadTo: backgroundPath,
});
```

**重要**: 
- 使用 WebBridge 工具与 ChatGPT 交互
- 等待图片生成完成（可能需要 10-30 秒）
- 从 ChatGPT 界面下载图片到 `backgroundPath`
- 验证图片尺寸和格式

### Step 3: 验证背景图

```bash
# 检查文件是否存在
ls -lh {backgroundPath}

# 验证图片尺寸（需要 ImageMagick 或用 Node.js）
identify {backgroundPath}  # 或用 sharp 库
```

确认：
- 文件存在且大小 > 100KB
- 尺寸符合配置（默认 1080×1920）
- 格式为 PNG 或 JPG

### Step 4: 启动预览（如果未设置 --no-preview）

```bash
cd {outputDir}
./preview.sh
```

或通过 WebBridge 打开：

```javascript
// 使用 mcp__webbridge__navigate
await webbridge.navigate({
  url: 'http://localhost:8000/index.html',
  session: 'text-rain-preview',
});

// 等待 2 秒让页面加载
await sleep(2000);

// 截图验证
await webbridge.screenshot({
  session: 'text-rain-preview',
  path: `{outputDir}/preview.png`,
});
```

### Step 5: 报告结果

向用户报告：
- ✅ 项目已生成到: `{outputDir}`
- ✅ 背景图已生成: `{backgroundPath}`
- ✅ 预览已启动: `http://localhost:8000`
- 📝 使用说明: 查看 `{outputDir}/README.md`

如果某步失败，提供清晰的错误信息和解决方案。

## 错误处理

### ChatGPT 生图失败
- **症状**: 任务包已发送，但 ChatGPT 返回错误或超时
- **解决**: 
  1. 检查 ChatGPT 账号是否有 DALL-E 3 权限
  2. 简化场景描述（去掉复杂细节）
  3. 让用户手动上传背景图到 `assets/background.png`

### 图片尺寸不匹配
- **症状**: 下载的图片尺寸与配置不符
- **解决**: 使用 ImageMagick 或 sharp 库调整尺寸
  ```bash
  convert {backgroundPath} -resize 1080x1920! {backgroundPath}
  ```

### WebBridge 连接失败
- **症状**: `mcp__webbridge__*` 工具报错
- **解决**: 
  1. 确认 Kimi WebBridge 服务运行中
  2. 运行 `~/.kimi-webbridge/bin/kimi-webbridge start`
  3. 如果仍失败，降级为手动打开浏览器

### 预览页面空白
- **症状**: 浏览器打开但只看到黑屏
- **解决**:
  1. 打开浏览器控制台查看错误
  2. 检查 `assets/background.png` 是否存在
  3. 验证 `sketch.js` 语法无错误
  4. 确认本地服务器正常运行（非直接打开 HTML）

## 灵感来源

- 景桐 Vibe Coding 文字雨案例
- p5.js 官方粒子系统示例
- 日本枯山水美学 + 中式诗词意境
