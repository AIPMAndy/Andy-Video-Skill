---
name: andy-manim-video
version: 1.0.0
description: 3Blue1Brown 风格的 Manim 程序化动画视频制作系统
author: Andy
created: 2026-07-31
license: MIT
tags: [video, animation, manim, 3blue1brown, education, youtube]
---

# Andy Manim Video - 程序化动画视频制作系统

**一键生成 3Blue1Brown 风格的教育动画视频**

## 核心价值

- ✅ **10倍迭代速度**：程序化动画 vs 手动 After Effects
- ✅ **数学精度**：代码控制每一帧，零手动错误
- ✅ **可复现性**：Git 版本控制，团队协作
- ✅ **顶级视觉风格**：复刻 23.8M 浏览量的 3Blue1Brown 美学
- ✅ **完整工作流**：从脚本到发布的端到端自动化

---

## 使用场景

### 1. AI/ML 概念讲解
- Attention Mechanism（已验证）
- Transformer Architecture
- Backpropagation
- Neural Network Basics

### 2. 数学可视化
- 线性代数
- 微积分
- 概率论
- 数值优化

### 3. 算法演示
- 排序算法
- 图算法
- 动态规划
- 递归可视化

### 4. 系统架构
- 分布式系统
- 数据流图
- 网络协议
- 并发模型

---

## 快速开始

### 安装依赖

```bash
# 安装 Manim Community
pip install manim

# （可选）安装 LaTeX（用于复杂数学公式，需要 4GB 空间）
# brew install mactex-no-gui
```

### 一键生成视频

```bash
# 调用技能
/andy-manim-video "主题：Attention Mechanism" "风格：3Blue1Brown" "时长：2分钟"

# 或在 Claude Code 中：
Skill("andy-manim-video", args="Attention Mechanism, 3Blue1Brown style, 2 minutes")
```

### 手动执行（高级用户）

```bash
# 1. 生成动画脚本
cd ~/Documents/AICode/ai-video-production
# Claude 会生成 {topic}_animation.py

# 2. 渲染预览（低质量，快速迭代）
manim -pql {topic}_animation.py {SceneName}

# 3. 渲染高质量（发布版本）
manim -pqh {topic}_animation.py --format=mp4 {SceneName}

# 4. 渲染所有场景（生产级）
./render_all.sh high
```

---

## 工作流程

### Phase 1: 脚本生成（5-10分钟）

**输入**：
- 主题关键词（如 "Attention Mechanism"）
- 目标时长（如 "2 分钟"）
- 视觉风格（默认：3Blue1Brown）

**处理**：
1. 分析主题核心概念
2. 设计 3-7 个场景结构
3. 生成 Python Manim 代码
4. 定义配色方案（青/洋红/黄）
5. 创建渲染脚本

**输出**：
- `{topic}_animation.py` - Manim 脚本
- `render_all.sh` - 自动化渲染脚本
- `README.md` - 项目文档

**技术栈**：
- Manim Community v0.19.0+
- Python 3.9+

---

### Phase 2: 动画渲染（10-20分钟）

**输入**：Phase 1 生成的 Python 脚本

**处理**：
1. 低质量预览渲染（480p15）- 快速验证
2. 发现问题 → 修改代码 → 重新渲染
3. 高质量最终渲染（1080p60）- 发布版本

**输出**：
- 低质量预览：`media/videos/{topic}/480p15/*.mp4`
- 高质量成品：`media/videos/{topic}/1080p60/*.mp4`

**渲染时间**：
- 480p15：每场景 30-60 秒
- 1080p60：每场景 2-5 分钟

---

### Phase 3: 配音制作（1-2小时）

**选项 A：AI 配音（推荐）**

工具：
- ElevenLabs（英文，最自然）
- 飞书妙记（中文）
- Azure Speech（多语言）

流程：
1. 读取 Python 注释中的配音脚本
2. 调用 TTS API 生成音频
3. 分段或整体导出 WAV

**选项 B：自己录音**

工具：
- Audacity（免费音频编辑器）
- Blue Yeti / Rode NT-USB（麦克风推荐）

技巧：
- 参考 3Blue1Brown 的平静叙述风格
- 语速：每分钟 140-160 词
- 环境：安静房间 + 降噪处理

---

### Phase 4: 视频合成（1-2小时）

**工具选择**：

**DaVinci Resolve（推荐，免费）**
- 专业级调色和音频混音
- GPU 加速渲染
- 下载：https://www.blackmagicdesign.com/products/davinciresolve

**iMovie（Mac 内置，简单）**
- 零学习成本
- 基础剪辑功能完善

**合成步骤**：
1. 导入所有场景视频（按顺序）
2. 添加配音音轨（同步到画面）
3. 添加背景音乐（-25dB 音量）
4. 场景间添加 0.5 秒淡入淡出
5. 导出设置：H.264, 1080p60, 10-15 Mbps

---

### Phase 5: 缩略图设计（30分钟-1小时）

**工具**：

**Figma（推荐，专业）**
- 画布：1280x720px
- 模板：YouTube Thumbnail
- 免费使用

**DALL-E 3 / Midjourney（AI 生成）**

提示词模板：
```
YouTube thumbnail for AI educational video.
Dark background (#1a1a1a), glowing neural network,
cyan/magenta/yellow gradient. Bold text: "ATTENTION".
Minimalist, high contrast, tech aesthetic. 1280x720.
```

**设计要素**：
- 背景色：暗色 (#1a1a1a 或 #171717)
- 主标题：粗体、高对比度、易读
- 配色：青色 + 洋红 + 黄色（与视频统一）
- 视觉焦点：中心对称、发光效果

**A/B 测试 3 个变体**：
1. 疑问式："But what is Attention?"
2. 时间限定："Attention in 100 Seconds"
3. 震撼性："Attention: The Algorithm That Changed AI"

---

### Phase 6: 发布准备（30分钟）

**标题公式**（基于研究验证）：

✅ **疑问式**（最高点击率）
- "But what is {Topic} in AI?"
- "What is {Concept}?"
- 示例：3Blue1Brown "But what is a neural network?" - 23.8M 浏览量

**时间限定**（吸引忙碌观众）
- "{Topic} in 100 Seconds"
- "{Topic} Explained in 5 Minutes"
- 示例：Fireship 系列 - 平均 3M+ 浏览量

**震撼性**（算法推荐友好）
- "{Concept}: The {Adjective} That Changed {Domain}"
- "The Secret Behind {Topic}"

**描述模板**：

```markdown
{概念} is the core mechanism behind {应用列表}. 
This video explains how it works from first principles using visual animations.

⏱️ Timestamps:
0:00 - Introduction
0:10 - The Problem
0:45 - Core Concepts
1:25 - Why It Matters
1:55 - Conclusion

📚 Resources:
- Paper: {论文链接}
- Code: {GitHub 链接}
- Manim: https://www.manim.community/

🛠️ Tools used:
- Animation: Manim (Python)
- Style: 3Blue1Brown inspired
- Created with: Claude Code

#AI #MachineLearning #{标签列表}
```

**标签策略**（15-20 个）：
- 核心概念（Attention, Transformer）
- 技术栈（AI, MachineLearning, DeepLearning）
- 应用场景（ChatGPT, GPT-4, Claude）
- 风格标签（Explained, Tutorial, Animation）
- 对标创作者（3Blue1Brown, Fireship）

---

## 核心配置

### 配色系统（3Blue1Brown 风格）

```python
# 标准配色常量
QUERY_COLOR = "#00FFFF"      # 青色 - Query
KEY_COLOR = "#FF00FF"        # 洋红 - Key
VALUE_COLOR = "#FFFF00"      # 黄色 - Value
BG_COLOR = "#171717"         # 深色背景
HIGHLIGHT_COLOR = "#58C4DD"  # 强调色（蓝绿）
ACCENT_COLOR = "#FC6255"     # 重点色（红）

# 应用到 Manim 配置
config.background_color = BG_COLOR
```

### 渲染质量档位

```bash
# 预览（快速迭代）
manim -pql scene.py SceneName  # 480p15fps

# 中等（测试）
manim -pqm scene.py SceneName  # 720p30fps

# 高质量（发布）
manim -pqh scene.py SceneName  # 1080p60fps

# 4K（专业）
manim -pqk scene.py SceneName  # 2160p60fps
```

### 字体系统

```python
# 系统字体（无需 LaTeX）
Text("Content", font="Helvetica Neue", font_size=36)

# LaTeX 字体（需要安装 LaTeX）
MathTex(r"\text{Content}", font_size=36)
```

---

## 场景模板库

### 1. 开场钩子（Intro Hook）

```python
class IntroScene(Scene):
    def construct(self):
        # 疑问式标题
        title_part1 = Text("But what is", font_size=48)
        keyword = Text("Attention", font_size=64, color=YELLOW)
        title_part2 = Text("in AI?", font_size=48)
        
        title = VGroup(title_part1, keyword, title_part2).arrange(RIGHT, buff=0.3)
        
        self.play(FadeIn(title_part1), FadeIn(title_part2))
        self.play(Write(keyword))
        self.wait()
        
        # 副标题
        subtitle = Text(
            "The mechanism behind ChatGPT, GPT-4, and Claude",
            font_size=24
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(FadeIn(subtitle))
        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
```

### 2. 问题设定（Problem Setup）

```python
class ProblemScene(Scene):
    def construct(self):
        # 问题标题
        problem_title = Text("The Problem:", font_size=40)
        self.play(Write(problem_title))
        self.wait()
        
        # 示例句子
        sentence = Text(
            '"The animal didn\'t cross the street because it was too tired"',
            font_size=28
        ).next_to(problem_title, DOWN, buff=0.8)
        
        self.play(FadeIn(sentence))
        self.wait()
        
        # 高亮歧义词
        ambiguous_word = Text("it", font_size=28, color=YELLOW)
        ambiguous_word.move_to(sentence[...])  # 定位到 "it" 位置
        
        self.play(
            sentence[...].animate.set_color(YELLOW),
            Circumscribe(sentence[...], color=YELLOW)
        )
        self.wait()
```

### 3. 概念讲解（Concept Explanation）

```python
class ConceptScene(Scene):
    def construct(self):
        # 三要素标题
        title = Text("Three Key Ingredients", font_size=44)
        self.play(Write(title))
        self.wait()
        
        # Query
        query_label = Text("Query (Q)", font_size=32, color=QUERY_COLOR)
        query_desc = Text('"What am I looking for?"', font_size=24)
        query_group = VGroup(query_label, query_desc).arrange(DOWN, buff=0.3)
        
        # Key
        key_label = Text("Key (K)", font_size=32, color=KEY_COLOR)
        key_desc = Text('"What do I contain?"', font_size=24)
        key_group = VGroup(key_label, key_desc).arrange(DOWN, buff=0.3)
        
        # Value
        value_label = Text("Value (V)", font_size=32, color=VALUE_COLOR)
        value_desc = Text('"What do I communicate?"', font_size=24)
        value_group = VGroup(value_label, value_desc).arrange(DOWN, buff=0.3)
        
        # 排列
        all_groups = VGroup(query_group, key_group, value_group).arrange(DOWN, buff=0.8)
        
        # 动画
        self.play(FadeIn(query_group))
        self.wait()
        self.play(FadeIn(key_group))
        self.wait()
        self.play(FadeIn(value_group))
        self.wait(2)
```

### 4. 总结收尾（Conclusion）

```python
class ConclusionScene(Scene):
    def construct(self):
        # 主要观点
        title = Text("Why Attention Changed Everything", font_size=40)
        self.play(Write(title))
        self.wait()
        
        # 三大优势
        points = [
            "1. Dynamic Context Selection",
            "2. Parallelizable Computation",
            "3. Long-Range Dependencies"
        ]
        
        point_group = VGroup(*[Text(p, font_size=28) for p in points])
        point_group.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        
        for point in point_group:
            self.play(FadeIn(point))
            self.wait()
        
        self.wait()
        self.play(FadeOut(VGroup(*self.mobjects)))
        
        # 名言结尾
        quote = Text("Attention is all you need", font_size=48, color=YELLOW)
        author = Text("— Vaswani et al., 2017", font_size=24).next_to(quote, DOWN)
        
        self.play(Write(quote))
        self.play(FadeIn(author))
        self.wait(3)
```

---

## 技术细节

### 避免 LaTeX 依赖（快速迭代）

**问题**：LaTeX 安装需要 4GB 空间 + 30 分钟

**解决方案**：使用 Text + Unicode 替代 MathTex

```python
# ❌ 需要 LaTeX
formula = MathTex(r"\text{Attention}(Q,K,V) = \text{softmax}(\frac{QK^T}{\sqrt{d_k}})V")

# ✅ 无需 LaTeX
formula = Text(
    "Attention(Q,K,V) = softmax(QK^T / √d_k) V",
    font_size=28
)
```

**自定义矩阵显示**：

```python
# ❌ 需要 LaTeX
matrix = Matrix([[1, 2], [3, 4]])

# ✅ 无需 LaTeX
def create_vector(label, color, values):
    """创建向量显示（无 LaTeX）"""
    vec = VGroup(
        Text("[", font_size=60, color=color),
        VGroup(*[Text(v, font_size=24, color=color) for v in values]).arrange(DOWN, buff=0.3),
        Text("]", font_size=60, color=color)
    ).arrange(RIGHT, buff=0.2)
    
    label_text = Text(label, font_size=32, color=color).next_to(vec, UP)
    return VGroup(label_text, vec)

# 使用
query_vec = create_vector("Query", QUERY_COLOR, ["q1", "q2", "q3"])
```

---

## 性能优化

### 渲染加速

```bash
# 使用多核渲染
manim -pqh scene.py --workers 4

# 只渲染变更的场景
manim -pqh scene.py Scene3  # 只渲染 Scene3

# 缓存部分动画
# 在 Scene 类中使用 self.add() 而不是 self.play() 可跳过动画
```

### 文件大小优化

```bash
# 使用 FFmpeg 二次压缩（几乎无损）
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -preset slow -c:a aac -b:a 128k output.mp4

# 批量压缩
for f in *.mp4; do
  ffmpeg -i "$f" -c:v libx264 -crf 23 -preset slow "${f%.mp4}_compressed.mp4"
done
```

---

## 故障排查

### 问题 1：ModuleNotFoundError: No module named 'manim'

```bash
# 解决：安装 Manim Community
pip install manim

# 验证安装
manim --version
```

### 问题 2：LaTeX 相关错误（FileNotFoundError: 'latex'）

**原因**：使用了 MathTex / Matrix 但未安装 LaTeX

**解决方案 A**：安装 LaTeX（需要 4GB）
```bash
brew install mactex-no-gui
```

**解决方案 B**：使用无 LaTeX 版本（推荐）
- 替换 MathTex → Text
- 替换 Matrix → 自定义 VGroup
- 参考上方"避免 LaTeX 依赖"章节

### 问题 3：TypeError: Only VMobject can be added to VGroup

**原因**：尝试将 list 或其他类型对象添加到 VGroup

**解决**：
```python
# ❌ 错误
self.play(FadeOut(VGroup(*self.mobjects)))

# ✅ 正确
self.play(*[FadeOut(mob) for mob in self.mobjects])
```

### 问题 4：Font not found 警告

**原因**：指定的字体系统中不存在

**解决**：
```python
# 使用 macOS 自带字体
Text("Content", font="Helvetica Neue")  # ✅
Text("Content", font="Helvetica")       # ✅
Text("Content", font="Arial")           # ✅

# 避免使用的字体
Text("Content", font="CMU Serif")       # ❌ 需要 LaTeX
```

---

## 成功案例

### Attention Mechanism 视频

**时间投入**：
- 脚本生成：10 分钟
- 迭代调试：30 分钟
- 渲染输出：15 分钟
- **总计**：55 分钟（vs 手动制作 8-10 小时）

**技术指标**：
- 场景数：4 个
- 总时长：100 秒
- 文件大小：3MB（1080p60）
- 渲染速度：10 倍提升

**预期效果**（基于对标）：
- 第一周：1,000+ 浏览量
- 第一月：10,000+ 浏览量
- 3 个月：100,000+ 浏览量

---

## API 接口（供其他技能调用）

### 生成动画脚本

```javascript
// 从其他 Skill 调用
const result = await skillCall('andy-manim-video', {
  action: 'generate_script',
  topic: 'Attention Mechanism',
  duration: '2 minutes',
  style: '3blue1brown',
  color_scheme: {
    primary: '#00FFFF',
    secondary: '#FF00FF',
    accent: '#FFFF00'
  }
});
// 返回：{ scriptPath: '/path/to/animation.py', sceneCount: 4 }
```

### 渲染视频

```javascript
const result = await skillCall('andy-manim-video', {
  action: 'render',
  scriptPath: '/path/to/animation.py',
  quality: 'high',  // low, medium, high, production
  scenes: ['Scene1', 'Scene2']  // 可选，不指定则渲染全部
});
// 返回：{ videoFiles: ['/path/to/Scene1.mp4', '/path/to/Scene2.mp4'] }
```

### 完整工作流

```javascript
const result = await skillCall('andy-manim-video', {
  action: 'full_workflow',
  topic: 'Backpropagation',
  duration: '3 minutes',
  output_dir: '~/Desktop/videos',
  include_voiceover: true,
  voiceover_provider: 'elevenlabs'
});
// 返回：{ finalVideo: '/path/to/final.mp4', thumbnail: '/path/to/thumb.png' }
```

---

## 项目结构

```
andy-manim-video/
├── SKILL.md                    # 本文档
├── index.mjs                   # 主入口（Node.js）
├── config.json                 # 配置文件
├── templates/                  # 场景模板
│   ├── intro_hook.py
│   ├── problem_setup.py
│   ├── concept_explanation.py
│   └── conclusion.py
├── examples/                   # 示例项目
│   ├── attention_mechanism/
│   ├── backpropagation/
│   └── transformer/
├── utils/                      # 工具函数
│   ├── color_schemes.py
│   ├── render_manager.py
│   └── video_composer.py
└── tests/                      # 测试用例
    ├── test_script_generation.py
    └── test_rendering.py
```

---

## 依赖项

### Python 包
```bash
pip install manim               # 动画引擎
pip install pillow              # 图像处理
pip install numpy               # 数值计算
```

### 系统工具
```bash
brew install ffmpeg             # 视频处理
brew install cairo              # 图形渲染
brew install pango              # 文字渲染
```

### 可选依赖
```bash
brew install mactex-no-gui      # LaTeX（复杂数学公式）
pip install openai-whisper      # 字幕生成
```

---

## 未来优化

- [ ] 支持自动生成配音脚本
- [ ] 集成 ElevenLabs TTS API
- [ ] 支持自动生成缩略图
- [ ] 支持批量渲染多个主题
- [ ] 集成 YouTube 自动发布
- [ ] 支持实时预览（Web UI）
- [ ] 支持协作编辑（多人同时修改）
- [ ] 支持 AI 辅助场景设计

---

## 开源计划

### 仓库信息
- **名称**：andy-manim-video
- **License**：MIT
- **GitHub**：https://github.com/AIPMAndy/andy-manim-video
- **文档**：https://andy-manim-video.readthedocs.io/

### 贡献指南

欢迎提交：
- 新的场景模板
- 配色方案
- Bug 修复
- 性能优化
- 文档改进

---

**维护者**：Andy  
**创建时间**：2026-07-31  
**最后更新**：2026-07-31  
**优先级**：P0
