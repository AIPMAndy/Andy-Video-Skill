# Attention Mechanism Example

完整的注意力机制视频示例项目，演示 andy-manim-video 的完整工作流。

## 项目结构

```
attention_mechanism/
├── attention_mechanism.py    # 完整 Manim 脚本（4个场景）
├── render_all.sh             # 批量渲染脚本
├── README.md                 # 本文档
└── media/                    # 渲染输出（自动生成）
```

## 场景列表

1. **AttentionIntro** (~10s) - 开场钩子
   - "But what is Attention Mechanism?"
   
2. **AttentionBasics** (~20s) - 问题设定
   - 为什么需要注意力机制
   - 传统方法的局限性

3. **AttentionMathSetup** (~40s) - 核心概念
   - Query, Key, Value 三大要素
   - 矩阵表示和计算流程

4. **AttentionConclusion** (~30s) - 总结结尾
   - 三大要点回顾
   - 应用场景展望

**总时长**: ~100 秒（1分40秒）

## 快速开始

### 1. 预览单个场景

```bash
# 低质量快速预览
manim -pql attention_mechanism.py AttentionIntro

# 高质量渲染
manim -pqh attention_mechanism.py AttentionIntro
```

### 2. 渲染所有场景

```bash
# 低质量（快速迭代）
./render_all.sh low

# 高质量（发布版本，推荐）
./render_all.sh high

# 4K 生产级
./render_all.sh production
```

### 3. 查看输出

```bash
# 视频文件位置
ls -lh media/videos/attention_mechanism_simple/1080p60/

# 预期输出:
# AttentionIntro.mp4          (~330KB)
# AttentionBasics.mp4         (~510KB)
# AttentionMathSetup.mp4      (~1.0MB)
# AttentionConclusion.mp4     (~1.1MB)
```

## 配色方案

```python
QUERY_COLOR = "#00FFFF"    # 青色 (Cyan) - 查询向量
KEY_COLOR = "#FF00FF"      # 洋红 (Magenta) - 键向量
VALUE_COLOR = "#FFFF00"    # 黄色 (Yellow) - 值向量
BG_COLOR = "#171717"       # 深色背景
```

这套配色来自 3Blue1Brown，具有：
- ✅ 高对比度，视觉清晰
- ✅ 色彩区分度高，便于理解
- ✅ 符合数学教育视频审美

## 关键技术点

### 1. 无 LaTeX 依赖

使用 `Text` 对象代替 `MathTex`，避免 4GB LaTeX 安装：

```python
# ❌ 需要 LaTeX
matrix = Matrix([[1, 2], [3, 4]])

# ✅ 纯 Text 实现
custom_matrix = VGroup(
    Text("[", font_size=60),
    VGroup(
        Text("q1", font_size=24),
        Text("q2", font_size=24)
    ).arrange(DOWN),
    Text("]", font_size=60)
).arrange(RIGHT)
```

### 2. 出字动画效果

核心技巧 - 分阶段显示：

```python
# Stage 1: 基础框架
self.play(FadeIn(title_part1), FadeIn(title_part2))

# Stage 2: 关键词强调
self.play(Write(keyword))  # "Attention" 逐字显现

# Stage 3: 补充信息
self.play(FadeIn(subtitle))
```

**用户反馈**: "这个出字的效果还不错" ✨

### 3. 颜色语义化

用颜色传递概念关联：

```python
# Query 始终用青色
q_label = Text("Query", color=QUERY_COLOR)

# Key 始终用洋红
k_label = Text("Key", color=KEY_COLOR)

# 用户一看颜色就知道在讲什么概念
```

## 下一步工作

### Phase 1: 配音制作

```bash
# 工具推荐: macOS 原生
# say -v Samantha -o intro_vo.aiff "But what is attention mechanism?"

# AI 配音工具
# - ElevenLabs (推荐，最自然)
# - Azure TTS
# - Google Cloud TTS
```

### Phase 2: 音频合成

```bash
# 使用 ffmpeg 合成配音
ffmpeg -i AttentionIntro.mp4 -i intro_vo.mp3 \
  -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 \
  AttentionIntro_final.mp4
```

### Phase 3: 背景音乐

推荐音乐库：
- YouTube Audio Library（免费）
- Epidemic Sound（付费，高质量）
- Artlist（付费，专业级）

音量设置: **-25dB** (背景不抢戏)

### Phase 4: 视频合成

工具选择：
- **DaVinci Resolve** (免费，专业)
- **iMovie** (macOS，简单)
- **Final Cut Pro** (付费，高级)

合成顺序：
1. 导入所有场景视频
2. 按顺序排列到时间线
3. 添加转场效果（建议：Cross Dissolve 0.5s）
4. 添加背景音乐轨道
5. 调整音量平衡
6. 导出最终视频

### Phase 5: 缩略图设计

规格: **1280x720px, PNG**

设计要点：
- 高对比度文字（白色 + 描边）
- 关键概念可视化（Q/K/V 矩阵）
- 疑问式标题："什么是注意力机制？"
- 面部表情（可选，提升点击率）

工具:
- Figma (在线，免费)
- Canva (模板丰富)
- Photoshop (专业)

### Phase 6: YouTube 发布

**A/B 测试标题**:
1. "But what is Attention Mechanism? | Transformer 核心原理"
2. "注意力机制可视化讲解 | 3分钟看懂 Transformer"
3. "Attention 到底是什么？| 深度学习必知概念"

**描述模板**:
```
🎯 3分钟可视化讲解注意力机制（Attention Mechanism）

📌 时间轴:
0:00 - 开场引入
0:10 - 问题设定
0:30 - 核心概念
1:10 - 总结应用

🔗 相关资源:
- Attention Is All You Need 论文
- Transformer 代码实现
- 更多可视化教程

#Attention #Transformer #深度学习 #机器学习 #AI教程
```

**标签策略**:
- attention mechanism
- transformer explained
- deep learning visualization
- 3blue1brown style
- manim animation
- AI education
- 注意力机制
- 深度学习

## 性能数据

| 场景 | 渲染时间 (1080p60) | 文件大小 |
|------|-------------------|---------|
| Intro | ~15秒 | 332KB |
| Basics | ~20秒 | 509KB |
| MathSetup | ~45秒 | 1.0MB |
| Conclusion | ~30秒 | 1.1MB |
| **总计** | **~110秒** | **~3MB** |

**迭代效率**: 相比 After Effects 提升 **10倍**

## 学习资源

- [Manim Community 官方文档](https://docs.manim.community/)
- [3Blue1Brown 频道](https://www.youtube.com/c/3blue1brown)
- [Manim 示例库](https://docs.manim.community/en/stable/examples.html)

## 许可证

MIT License - 可自由修改和分发

---

**Created**: 2026-07-31  
**Tool**: andy-manim-video v1.0.0  
**Author**: Andy
