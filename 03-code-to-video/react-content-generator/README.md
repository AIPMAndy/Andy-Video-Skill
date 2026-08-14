# React Content Generator

生成高质量 React 知识演示页面（Apple 风格 + 动画）

**可独立使用**，也可配合 `react-video-generator` 生成视频。

## 特点

- ✅ **Apple 风格设计**：毛玻璃卡片、大圆角、精致阴影
- ✅ **分步动画系统**：状态驱动、时序编排、流畅过渡
- ✅ **可视化组件库**：搜索迁徙、漏斗压缩、雷达扫描、对比展示
- ✅ **响应式设计**：适配桌面、平板、手机
- ✅ **独立使用**：可作为展示页面直接使用
- ✅ **视频集成**：可选配合 react-video-generator 生成视频

## 快速开始

### 1. 使用 skill

```bash
# 生成 React 页面
/react-content-generator "主题：AI 搜索革命" --pages=5

# 不需要配音文本（纯展示页面）
/react-content-generator "主题：AI 搜索革命" --no-script
```

### 2. 运行项目

```bash
cd output
npm install
npm run dev
```

### 3. （可选）生成视频

如果需要将页面转换为视频：

```bash
/react-video-generator
```

## 文件结构

```
react-content-generator/
├── SKILL.md                          # 主文档
├── templates/                        # 模板库
│   ├── core-components.jsx           # 核心组件（GlassCard、ScriptFooter 等）
│   ├── visualizer-components.jsx     # 可视化组件（搜索迁徙、漏斗压缩等）
│   ├── animation-presets.css         # 动画预设
│   ├── app-template.jsx              # 完整项目模板
│   ├── package.json                  # 依赖配置
│   ├── vite.config.js                # Vite 配置
│   ├── tailwind.config.js            # Tailwind 配置
│   └── postcss.config.js             # PostCSS 配置
├── examples/                         # 示例
│   └── usage-examples.md             # 使用示例
└── README.md                         # 本文档
```

## 核心组件

### GlassCard（毛玻璃卡片）
```jsx
<GlassCard className="p-6">
  <h3>标题</h3>
  <p>内容</p>
</GlassCard>
```

### ScriptFooter（配音提词器）
```jsx
<ScriptFooter text="这是配音文本，会被 react-video-generator 自动提取" />
```

### ProgressBar（进度条）
```jsx
<ProgressBar current={2} total={5} />
```

## 可视化组件

### SearchShiftVisualizer（搜索迁徙）
展示用户从传统搜索引擎迁移到 AI 搜索的过程。

```jsx
<SearchShiftVisualizer isActive={step === 1} />
```

### CruelFunnelVisualizer（漏斗压缩）
展示从海量信息到精选结果的筛选过程。

```jsx
<CruelFunnelVisualizer isActive={step === 2} />
```

### RadarVisualizer（雷达扫描）
展示全平台监控、实时追踪的能力。

```jsx
<RadarVisualizer 
  isActive={step === 3}
  platforms={[
    { icon: <Search size={20} />, name: "百度" },
    { icon: <Bot size={20} />, name: "ChatGPT" }
  ]}
/>
```

### BeforeAfterComparison（对比展示）
传统方案 vs AI 方案的对比。

```jsx
<BeforeAfterComparison
  isActive={step === 4}
  before={["人工客服", "成本高", "效率低"]}
  after={["AI 客服", "成本低", "效率高"]}
/>
```

## 动画预设

### 基础动画
- `animate-fadeInScale`：淡入放大
- `animate-slideInUp`：上滑进入
- `animate-slideInDown`：下滑进入
- `animate-slideInLeft`：左滑进入
- `animate-slideInRight`：右滑进入

### 特效动画
- `animate-float-badge`：浮动徽章
- `animate-pulse-glow`：脉冲发光
- `animate-rotate-slow`：缓慢旋转

### 延迟工具类
- `delay-100` ~ `delay-2000`：动画延迟（0.1s ~ 2s）

## 配色方案

### 主色调
- **Indigo/Purple**：科技感（#6366f1 + #a855f7）
- **Blue/Cyan**：商务感（#3b82f6 + #06b6d4）
- **Emerald/Teal**：活力感（#10b981 + #14b8a6）
- **Amber/Orange**：温暖感（#f59e0b + #f97316）

### 语义色
- **Success**：#10b981（emerald-500）
- **Warning**：#f59e0b（amber-500）
- **Error**：#ef4444（red-500）
- **Info**：#3b82f6（blue-500）

## 最佳实践

### 1. 页面数量
- 短视频（15-30 秒）：3-4 页
- 中视频（30-60 秒）：5-6 页
- 长视频（60-90 秒）：7-8 页

### 2. 配音文本
- 每页 50-150 字（对应 10-30 秒配音）
- 口语化、有节奏感
- 关键词加重语气

### 3. 动画节奏
- 开场动画：2-3 秒
- 主体展示：10-20 秒
- 结尾过渡：2-3 秒

### 4. 视觉层次
- 开场页：大标题 + 副标题 + 装饰元素
- 内容页：标题 + 可视化 + 关键信息
- 结尾页：总结 + CTA + 联系方式

## 与 react-video-generator 集成

### 1. 配音文本要求
- 每页必须有 `<ScriptFooter text="..." />`
- 文本长度：50-150 字
- 语气：口语化、有节奏感

### 2. 动画时长控制
- 每页总时长：15-30 秒
- 开场动画：2-3 秒
- 主体展示：10-20 秒
- 结尾过渡：2-3 秒

### 3. 视觉规范
- 分辨率：1200x1600（竖屏）
- 背景：浅色系（便于录制）
- 对比度：确保文字清晰可读

## 示例项目

查看 `examples/usage-examples.md` 了解完整示例：
- AI 搜索革命（5 页）
- Roblox AI Agent（5 页）
- 企业 AI 转型（4 页）
- 个人 IP 打造（5 页）

## 常见问题

### Q: 如何调整动画速度？
A: 修改 `setTimeout` 的延迟时间和 CSS `transition-duration`。

### Q: 如何自定义配色？
A: 修改 `tailwind.config.js` 中的 `theme.extend.colors`。

### Q: 如何添加新的可视化组件？
A: 参考 `templates/visualizer-components.jsx`，遵循相同的状态管理模式。

### Q: 生成的项目如何运行？
A: 
```bash
cd output
npm install
npm run dev
```

## 更新日志

### v1.0.0 (2026-04-25)
- 初始版本
- 基于 4 个成熟项目提炼设计系统
- 支持 Apple 风格 + 动画 + 配音文本
- 集成 react-video-generator 工作流

## 作者

Content (Andy 的 AI 内容与品牌负责人)

## 许可

MIT
