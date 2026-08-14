# Text Rain Generator - 速查表

## 快速开始

```bash
# 1. 调用 Skill（在 Claude Code 中）
/text-rain-generator "床前明月光，疑是地上霜。举头望明月，低头思故乡。"

# 2. 使用预设
/text-rain-generator "春眠不觉晓" --preset jiangnan

# 3. 交互式菜单
cd ~/.claude/skills/text-rain-generator
./quick-start.sh
```

## 20 种预设速览

| 预设名 | 中文名 | 场景 | 速度 | 倾斜 | 适用诗词 |
|--------|--------|------|------|------|----------|
| **jiangnan** | 江南水乡 | 烟雨、水墨 | 2.0 | 5° | 春雨、江南 |
| **beijing** | 北京胡同 | 四合院、红墙 | 2.5 | 10° | 古都、秋 |
| **huizhou** | 徽派建筑 | 马头墙、青石 | 2.2 | 8° | 古村、徽州 |
| **lingnan** | 岭南骑楼 | 骑楼、西关 | 2.3 | 12° | 广东、夏 |
| **yaodong** | 黄土窑洞 | 黄土高原 | 3.0 | 15° | 黄河、陕北 |
| **sichuan** | 川西民居 | 碉楼、藏式 | 2.8 | 10° | 山水、川西 |
| **tulou** | 客家土楼 | 圆形土楼 | 2.5 | 8° | 客家、福建 |
| **yurt** | 草原毡房 | 蒙古包、草原 | 3.5 | 20° | 草原、游牧 |
| **temple** | 古刹寺庙 | 寺庙、佛光 | 1.8 | 5° | 禅意、佛教 |
| **bamboo** | 竹林幽径 | 竹林、青石 | 2.0 | 6° | 竹子、幽静 |
| **sakura** | 樱花季 | 樱花、粉色 | 1.5 | 8° | 春天、樱花 |
| **desert** | 大漠孤烟 | 沙漠、驼队 | 4.0 | 25° | 沙漠、边塞 |
| **modern** | 现代都市 | 摩天大楼、霓虹 | 3.0 | 15° | 都市、现代 |
| **cyberpunk** | 赛博朋克 | 霓虹、未来 | 3.5 | 20° | 科幻、未来 |
| **minimal** | 极简主义 | 纯色、留白 | 2.0 | 0° | 现代诗、简约 |
| **ink** | 水墨画 | 泼墨、留白 | 1.5 | 5° | 山水、禅意 |
| **snow** | 雪景 | 雪花、白色 | 1.0 | 3° | 冬天、雪 |
| **storm** | 暴风雨 | 闪电、乌云 | 5.0 | 35° | 风暴、激烈 |
| **landscape** | 横版山水 | 山水画 | 2.0 | 8° | 横屏显示 |
| **square** | 方形构图 | 正方形 | 2.0 | 10° | 社交媒体 |

## 常用命令

### 基础使用
```bash
# 最简调用（自动推荐预设）
/text-rain-generator "诗词内容"

# 指定预设
/text-rain-generator "诗词内容" --preset jiangnan

# 自定义参数
/text-rain-generator "诗词内容" --speed 3.0 --tilt 15 --color "#ff0000"
```

### 视频导出
```bash
cd ~/.claude/skills/text-rain-generator
bun run export-video.ts \
  --input ~/output/text-rain-20260802-123456/index.html \
  --output ~/Desktop/rain.mp4 \
  --duration 10 \
  --fps 30
```

### 批量生成
```bash
# 1. 创建配置文件 tasks.json
cat > tasks.json << 'EOF'
{
  "tasks": [
    {"poem": "春眠不觉晓", "preset": "jiangnan"},
    {"poem": "白日依山尽", "preset": "landscape"},
    {"poem": "大漠孤烟直", "preset": "desert"}
  ],
  "outputDir": "~/batch-output",
  "parallelLimit": 2
}
EOF

# 2. 运行批量生成
bun run batch-generate.ts tasks.json
```

### 音效增强
```bash
bun run sound-effects.ts \
  --input ~/output/text-rain-20260802-123456 \
  --sound-url "https://cdn.example.com/rain.mp3" \
  --volume 0.3
```

## 参数速查

### 核心参数
| 参数 | 说明 | 默认值 | 范围 |
|------|------|--------|------|
| `--speed` | 下落速度 | 2.5 | 1.0-10.0 |
| `--tilt` | 倾斜角度 | 10 | 0-45 |
| `--color` | 文字颜色 | #d4c5a9 | 十六进制 |
| `--fontSize` | 字号 | 24 | 12-72 |
| `--width` | 画布宽度 | 1080 | 320-3840 |
| `--height` | 画布高度 | 1920 | 568-2160 |

### 高级参数
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--density` | 粒子密度 | 0.04 |
| `--wobble` | 摆动幅度 | 1.5 |
| `--wobbleSpeed` | 摆动速度 | 0.1 |
| `--rotationSpeed` | 旋转速度 | 0.05 |
| `--collisionThreshold` | 碰撞阈值 | 80 |

### 场景参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--scene` | 背景场景描述 | "江南水乡，小桥流水" |
| `--style` | 艺术风格 | "水墨画风格" |
| `--time` | 时间氛围 | "黄昏时分" |
| `--weather` | 天气 | "细雨蒙蒙" |

## 预设推荐规则

| 诗词关键词 | 自动推荐预设 | 原因 |
|------------|--------------|------|
| 雪 | snow | 雪景主题 |
| 雨、江南、春 | jiangnan | 江南烟雨 |
| 竹、林 | bamboo | 竹林场景 |
| 沙漠、边塞 | desert | 大漠风光 |
| 寺、禅、佛 | temple | 禅意意境 |
| 故宫、京城 | beijing | 古都风貌 |
| 月、夜 | minimal | 极简夜色 |
| 山、水、峰 | landscape | 山水画 |
| 樱花、春 | sakura | 樱花季 |

## 故障排查

### 问题 1：背景图生成失败
```bash
# 原因：ChatGPT 未登录或限流
# 解决：手动提供背景图
cp my-background.png ~/output/text-rain-xxx/assets/background.png
```

### 问题 2：字体显示异常
```bash
# 原因：系统缺少中文字体
# 解决：在 sketch.js 中指定 Web Font
textFont('Noto Sans SC');
```

### 问题 3：性能卡顿
```bash
# 原因：粒子数过多
# 解决：降低密度
/text-rain-generator "诗词" --density 0.02
```

### 问题 4：视频导出失败
```bash
# 原因：未安装 FFmpeg
# 解决：
brew install ffmpeg  # macOS
sudo apt install ffmpeg  # Linux
```

## 性能优化技巧

1. **降低分辨率**：`--width 720 --height 1280`
2. **减少粒子**：`--density 0.02`
3. **关闭碰撞检测**：修改 `sketch.js` 注释掉 `detectCollision()`
4. **使用 JPG 背景**：更小的文件尺寸
5. **降低帧率**：视频导出时用 `--fps 24`

## 高级技巧

### 1. 双色渐变文字
修改 `sketch.js`：
```javascript
const gradient = drawingContext.createLinearGradient(0, 0, 0, height);
gradient.addColorStop(0, '#ff6b6b');
gradient.addColorStop(1, '#4ecdc4');
drawingContext.fillStyle = gradient;
```

### 2. 多层粒子系统
```javascript
const layers = [
  { speed: 2.0, opacity: 0.3 }, // 背景层
  { speed: 3.0, opacity: 0.7 }, // 中景层
  { speed: 5.0, opacity: 1.0 }, // 前景层
];
```

### 3. 鼠标交互
```javascript
function mouseMoved() {
  drops.forEach(drop => {
    const d = dist(mouseX, mouseY, drop.x, drop.y);
    if (d < 50) {
      drop.x += (drop.x - mouseX) * 0.1;
      drop.y += (drop.y - mouseY) * 0.1;
    }
  });
}
```

### 4. 音频可视化
```javascript
let fft = new p5.FFT();
function draw() {
  let spectrum = fft.analyze();
  let bass = fft.getEnergy("bass");
  drops.forEach(drop => {
    drop.speed = map(bass, 0, 255, 1, 5);
  });
}
```

## 资源链接

- **p5.js 文档**: https://p5js.org/reference/
- **音效资源**: https://freesound.org/
- **中文 Web Fonts**: https://fonts.google.com/?subset=chinese-simplified
- **FFmpeg 文档**: https://ffmpeg.org/documentation.html
- **Skill 源码**: `~/.claude/skills/text-rain-generator/`

## 快捷键（预览页面）

| 按键 | 功能 |
|------|------|
| 空格 | 暂停/继续 |
| R | 重新开始 |
| S | 截图 |
| M | 静音/取消静音（需音效） |
| F | 全屏 |
| + / - | 调整速度 |

## 示例诗词

```
床前明月光，疑是地上霜。举头望明月，低头思故乡。  # preset: minimal
春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。  # preset: jiangnan
大漠孤烟直，长河落日圆。萧关逢候骑，都护在燕然。  # preset: desert
千山鸟飞绝，万径人踪灭。孤舟蓑笠翁，独钓寒江雪。  # preset: snow
空山新雨后，天气晚来秋。明月松间照，清泉石上流。  # preset: bamboo
```

---

**版本**: 1.0.0  
**更新**: 2026-08-02  
**更多**: 参见 `USAGE.md` 完整教程
