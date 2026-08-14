---
name: react-content-generator
description: 生成高质量 React 知识演示页面（Apple 风格 + 动画），支持3种主题风格，可独立使用或配合 react-video-generator 生成视频
version: 2.0.0
---

# React 内容生成器

专门用于生成高质量的 React 知识演示页面（可独立使用，也可配合 `react-video-generator` 生成视频）。

## 核心特点

基于 **7 个成熟案例项目**的代码模式，提炼出的设计系统：

### 1. 三种主题风格预设（NEW v2.0）
- **暗黑科技风（dark-tech）**：深空黑背景 + 蓝紫渐变 + 光晕效果，适合技术产品/开发工具
- **温暖专业风（warm-professional）**：浅灰白背景 + 橙黄渐变 + 柔和阴影，适合企业级解决方案/B端产品
- **梦幻渐变风（dreamy-gradient）**：粉白基底 + 紫粉渐变 + 光晕效果，适合C端产品/社交工具

### 2. Apple 风格设计语言
- **毛玻璃卡片（GlassCard）**：支持主题切换，自动适配浅色/深色背景
- **圆角系统**：`rounded-[2.5rem]`（大圆角）→ `rounded-3xl`（超大容器）
- **阴影层次**：根据主题自动调整阴影深度
- **渐变背景**：多层渐变叠加，营造空间感

### 3. 标准化动画时序系统（NEW v2.0）
- **状态驱动**：通过 `step` 状态控制动画流程
- **标准时序**：初始延迟 800-1200ms，步骤间隔 1200-2000ms，高潮时刻 3500-4500ms
- **过渡效果**：`transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]`
- **新增动画**：scaleIn、fadeIn、dash（SVG流线动画）

### 4. 配音文本集成（可选）
- **ScriptFooter 组件**：支持三种主题风格（light/dark/glass）
- **响应式显示**：`text-sm md:text-base font-bold`
- **视频生成支持**：`react-video-generator` 会自动提取配音文本

### 5. 高级可视化组件库（NEW v2.0）
基于真实案例提炼的4种核心模式：
- **对比崩溃模式**（ContrastCollapseVisualizer）：展示痛点，左侧正常→中间转折→右侧崩溃+警示层
- **流程引擎模式**（FlowEngineVisualizer）：展示技术架构，输入→引擎处理→多输出+SVG流线动画
- **卡片瀑布流模式**（CardCascadeVisualizer）：展示特性列表，卡片依次出现
- **金句组件标准模板**（GoldenSentenceStandard）：展示Andy身份背书+核心观点

传统可视化组件（保留）：
- **搜索迁徙可视化**（SearchShiftVisualizer）：展示用户行为变化
- **漏斗压缩可视化**（CruelFunnelVisualizer）：展示筛选过程
- **雷达扫描可视化**（RadarVisualizer）：展示全平台监控
- **对比展示**（BeforeAfterComparison）：传统 vs AI 方案

## 使用方法

```bash
# 基础用法
/react-content-generator "主题：AI 搜索革命"

# 指定主题风格（NEW v2.0）
/react-content-generator "主题：AI 搜索革命" --theme=dark-tech
/react-content-generator "主题：AI 搜索革命" --theme=warm-professional
/react-content-generator "主题：AI 搜索革命" --theme=dreamy-gradient

# 指定页数
/react-content-generator "主题：AI 搜索革命" --pages=5

# 不需要配音文本（纯展示页面）
/react-content-generator "主题：AI 搜索革命" --no-script

# 组合使用
/react-content-generator "主题：开源LLM部署" --theme=dark-tech --pages=6
```

## 工作流程

1. **需求分析**
   - 提取主题、目标受众、核心观点
   - 确定页面数量（默认 3-5 页）

2. **内容结构设计**
   - 开场页：标题 + 副标题 + 核心观点
   - 痛点页：问题可视化 + 数据支撑
   - 方案页：解决方案 + 优势展示
   - 案例页：实际效果 + 对比
   - 结尾页：总结 + CTA

3. **代码生成**
   - 基于模板库生成完整 React 项目
   - 自动配置 Vite + Tailwind CSS
   - 集成 lucide-react 图标库

4. **配音文本生成**
   - 为每页生成对应的配音文本
   - 自动嵌入 `<ScriptFooter text="..." />`

## 项目结构

生成的项目结构：
```
output/
├── src/
│   ├── App.jsx          # 主组件（包含所有页面）
│   └── main.jsx         # 入口文件
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## 核心组件模板

### GlassCard（毛玻璃卡片）
```jsx
const GlassCard = ({ children, className = "", onClick, active = false }) => {
  return (
    <div
      onClick={onClick}
      className={`
        relative overflow-hidden rounded-[2.5rem] bg-white/70 backdrop-blur-3xl
        border border-white/80
        shadow-[0_10px_40px_rgba(0,0,0,0.04)]
        transition-[transform,box-shadow,opacity] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]
        ${active ? 'scale-95 shadow-[inset_0_2px_10px_rgba(0,0,0,0.03)]' : 'hover:-translate-y-1'}
        ${className}
      `}
    >
      <div className="relative h-full z-10">{children}</div>
      <div className="absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-white/90 to-transparent pointer-events-none opacity-90"></div>
    </div>
  );
};
```

### ScriptFooter（配音提词器）
```jsx
const ScriptFooter = ({ text }) => (
  <div className="absolute bottom-8 left-0 w-full flex justify-center z-50 pointer-events-none px-4">
    <div className="bg-white/80 backdrop-blur-2xl border border-white/50 px-6 py-4 md:px-8 md:py-5 rounded-full shadow-[0_10px_40px_rgba(0,0,0,0.08)] max-w-4xl text-center">
      <div className="text-slate-700 text-sm md:text-lg font-bold leading-relaxed">
        {text}
      </div>
    </div>
  </div>
);
```

## 动画预设

### fadeInScale（淡入放大）
```css
@keyframes fadeInScale {
  from { opacity: 0; transform: translateY(40px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
.animate-fadeInScale { 
  animation: fadeInScale 0.6s cubic-bezier(0.25, 1, 0.5, 1) both; 
}
```

### slideInUp（上滑进入）
```css
@keyframes slideInUp {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-slideInUp { 
  animation: slideInUp 0.5s cubic-bezier(0.25, 1, 0.5, 1) both; 
}
```

## 可视化组件库

### 新增高级组件（v2.0）

#### 1. 对比崩溃模式（ContrastCollapseVisualizer）
展示痛点：正常状态 → 转折 → 崩溃+警示层

**适用场景：**
- 技术债务累积导致系统崩溃
- 传统方案遭遇瓶颈
- 用户流失/体验下降

**核心元素：**
- 左侧：过去的正常状态（逐渐淡化）
- 中间：转折点图标（箭头→闪电）
- 右侧：问题状态 + overlay警示层
- 底部：权威背书/警示文案

**标准时序：** step 0 静态 → step 1 左侧出现(1000ms) → step 2 右侧+转折(2500ms) → step 3 overlay警示(4500ms)

#### 2. 流程引擎模式（FlowEngineVisualizer）
展示技术架构：输入 → 引擎处理 → 多个输出

**适用场景：**
- AI/数据处理管道
- 微服务架构
- 自动化工作流

**核心元素：**
- 输入节点：原始数据/请求
- 引擎节点：渐变背景 + ping动画 + SVG流线
- 输出节点：3-4个分支，带渐变色左边框
- SVG动画：stroke-dasharray实现流动效果

**标准时序：** step 0 静态 → step 1 输入+引擎(800ms) → step 2 SVG流线(2000ms) → step 3 输出分支(3200ms)

#### 3. 卡片瀑布流模式（CardCascadeVisualizer）
展示特性列表：多个特性卡片依次出现

**适用场景：**
- 产品功能点展示
- 技术优势罗列
- 团队能力说明

**核心元素：**
- 2x2 grid或垂直列表
- 每个卡片：图标+标题+描述
- 延迟动画：每项delay递增200ms
- hover效果：上浮1.5px

**标准时序：** 首卡800ms，后续每张+200ms

#### 4. 金句组件标准模板（GoldenSentenceStandard）
展示Andy身份背书+核心观点

**适用场景：**
- 结尾总结
- 核心观点强调
- 个人IP打造

**核心元素：**
- 大引号水印（背景）
- 上半句：普通文字
- 下半句：渐变色强调
- 底部：作者名 + credentials徽章

**标准时序：** step 0 静态 → step 1 上半句(800ms) → step 2 下半句+作者(2000ms)

### 传统组件（保留）

#### 5. 搜索迁徙可视化（SearchShiftVisualizer）
展示用户从传统搜索引擎迁移到 AI 搜索的过程。

**适用场景：**
- 用户行为变化
- 市场趋势转移
- 技术迭代

**核心元素：**
- 传统搜索界面（逐渐模糊）
- 转移箭头 + 文字说明
- AI 搜索界面（逐渐清晰）

### 6. 漏斗压缩可视化（CruelFunnelVisualizer）
展示从海量信息到精选结果的筛选过程。

**适用场景：**
- 信息过滤
- 竞争淘汰
- 精准推荐

**核心元素：**
- 顶部：大量小方块（代表海量信息）
- 中间：SVG 漏斗 + 压缩动画
- 底部：3-5 个高亮卡片（最终结果）

### 7. 雷达扫描可视化（RadarVisualizer）
展示全平台监控、实时追踪的能力。

**适用场景：**
- 多平台监控
- 实时数据追踪
- 全局视角

**核心元素：**
- 中心雷达圆盘 + 扫描线
- 周围平台图标（逐个点亮）
- 数据流动效果

### 8. 对比展示（BeforeAfterComparison）
传统方案 vs AI 方案的对比。

**适用场景：**
- 新旧对比
- 优劣分析
- 升级说明

**核心元素：**
- 左右分屏或上下分屏
- 对比项逐条展示
- 优势项高亮标注

## 配色方案

### 主色调（Indigo/Purple）
```css
/* 主色 */
--primary: #6366f1;      /* indigo-500 */
--primary-light: #818cf8; /* indigo-400 */
--primary-dark: #4f46e5;  /* indigo-600 */

/* 辅助色 */
--secondary: #a855f7;     /* purple-500 */
--accent: #06b6d4;        /* cyan-500 */

/* 背景 */
--bg-base: #f8fafc;       /* slate-50 */
--bg-card: rgba(255,255,255,0.7); /* white/70 */
```

### 语义色
```css
/* 成功 */
--success: #10b981;       /* emerald-500 */

/* 警告 */
--warning: #f59e0b;       /* amber-500 */

/* 错误 */
--error: #ef4444;         /* red-500 */

/* 信息 */
--info: #3b82f6;          /* blue-500 */
```

## 图标使用规范

使用 `lucide-react` 图标库：

```jsx
import { 
  Brain,        // AI/智能
  Search,       // 搜索
  Sparkles,     // 亮点/特色
  Target,       // 目标/精准
  Zap,          // 快速/效率
  Crown,        // 顶级/推荐
  TrendingDown, // 下降趋势
  ArrowRight,   // 流程/转移
  CheckCircle2, // 成功/完成
  XCircle       // 失败/问题
} from 'lucide-react';
```

**图标尺寸规范：**
- 小图标：`size={12}` - 用于标签、徽章
- 中图标：`size={16}` - 用于按钮、列表项
- 大图标：`size={24}` - 用于卡片标题
- 超大图标：`size={48}` - 用于页面主视觉

## 响应式设计

### 断点系统
```css
/* Tailwind 默认断点 */
sm: 640px   /* 手机横屏 */
md: 768px   /* 平板 */
lg: 1024px  /* 笔记本 */
xl: 1280px  /* 桌面 */
```

### 字号响应
```jsx
// 标题
className="text-2xl md:text-4xl lg:text-5xl"

// 正文
className="text-sm md:text-base lg:text-lg"

// 小字
className="text-xs md:text-sm"
```

## 性能优化

### 1. 动画性能
- 优先使用 `transform` 和 `opacity`（GPU 加速）
- 避免动画 `width`、`height`、`top`、`left`
- 使用 `will-change` 提示浏览器优化

### 2. 图标优化
- 使用 `lucide-react` 的 tree-shaking
- 只导入需要的图标

### 3. 状态管理
- 使用 `useState` 管理页面状态
- 使用 `useEffect` 控制动画时序
- 避免不必要的重渲染

## 与 react-video-generator 集成（可选）

如果你需要将生成的 React 页面转换为视频，可以配合 `react-video-generator` 使用。

### 1. 配音文本要求
- 每页必须有 `<ScriptFooter text="..." />`
- 文本长度：50-150 字（对应 10-30 秒配音）
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

### 4. 工作流程
```bash
# 步骤 1：生成 React 项目
/react-content-generator "主题：AI 搜索革命" --pages=5

# 步骤 2：运行项目
cd output
npm install
npm run dev

# 步骤 3：生成视频
/react-video-generator
```

**注意：**
- 如果不需要生成视频，可以省略步骤 3
- 如果只需要展示页面，可以使用 `--no-script` 参数省略配音文本

## 常见问题

### Q: 如何调整动画速度？
A: 修改 `setTimeout` 的延迟时间和 CSS `transition-duration`。

### Q: 如何添加新的可视化组件？
A: 参考 `templates/` 目录下的示例，遵循相同的状态管理模式。

### Q: 如何自定义配色？
A: 修改 `tailwind.config.js` 中的 `theme.extend.colors`。

### Q: 生成的项目如何运行？
A: 
```bash
cd output
npm install
npm run dev
```

## 最佳实践

### 1. 内容设计
- **一页一个核心观点**：不要在一页塞太多信息
- **视觉优先**：用可视化代替文字描述
- **节奏控制**：快慢结合，避免单调

### 2. 动画设计
- **入场动画**：统一使用 `fadeInScale` 或 `slideInUp`
- **交互反馈**：hover 状态要明显
- **时序编排**：重要元素延迟出现（`animationDelay`）

### 3. 配音文本
- **口语化**：写成"说话"的样子，不是"写作"的样子
- **有停顿**：用标点符号控制节奏
- **有重点**：关键词用"加重语气"的方式表达

## 示例项目

### 示例 1：AI 搜索革命
主题：传统 SEO 失效，AI 搜索崛起

**页面结构：**
1. 开场：标题 + 核心观点
2. 痛点：搜索迁徙可视化
3. 真相：漏斗压缩可视化
4. 方案：产品介绍 + 功能展示
5. 结尾：总结 + CTA

### 示例 2：Roblox AI Agent
主题：游戏中的 AI 助手

**页面结构：**
1. 开场：标题 + 场景描述
2. 问题：传统游戏开发痛点
3. 方案：AI Agent 能力展示
4. 案例：实际应用场景
5. 结尾：未来展望

## 更新日志

### v1.0.0 (2026-04-25)
- 初始版本
- 基于 4 个成熟项目提炼设计系统
- 支持 Apple 风格 + 动画 + 配音文本
- 集成 react-video-generator 工作流

---

**作者：** Content (Andy 的 AI 内容与品牌负责人)  
**最后更新：** 2026-04-25
