# 更新日志

## v2.0.0 (2026-06-07)

### 🎨 新增功能

#### 1. 三种主题风格预设
基于 TensorFlow、liteparse、social-auto-upload 三个真实案例提炼：
- **暗黑科技风（dark-tech）**：深空黑背景 + 蓝紫渐变 + 光晕效果
  - 适合：技术产品、开发工具、开源项目
  - 参考：liteparse案例
- **温暖专业风（warm-professional）**：浅灰白背景 + 橙黄渐变 + 柔和阴影
  - 适合：企业级解决方案、B端产品、技术服务
  - 参考：TensorFlow案例
- **梦幻渐变风（dreamy-gradient）**：粉白基底 + 紫粉渐变 + 光晕效果
  - 适合：C端产品、社交工具、创意应用
  - 参考：social-auto-upload案例

#### 2. 高级可视化组件库
新增4种基于真实案例的可视化模式：

**ContrastCollapseVisualizer（对比崩溃模式）**
- 用途：展示痛点，从正常到崩溃的转变
- 结构：左侧正常 → 中间转折 → 右侧崩溃+overlay警示层
- 标准时序：1000ms → 2500ms → 4500ms

**FlowEngineVisualizer（流程引擎模式）**
- 用途：展示技术架构和数据流动
- 结构：输入 → 引擎处理（SVG流线动画）→ 多输出分支
- 标准时序：800ms → 2000ms → 3200ms

**CardCascadeVisualizer（卡片瀑布流模式）**
- 用途：展示特性列表、功能点
- 结构：2x2 grid或垂直列表，卡片依次出现
- 标准时序：首卡800ms，后续每张+200ms

**GoldenSentenceStandard（金句组件标准模板）**
- 用途：展示核心观点和身份背书
- 结构：引号水印 + 上半句 + 下半句（渐变强调）+ 作者credentials
- 标准时序：800ms → 2000ms

#### 3. 标准化动画时序系统
从案例中提炼的最佳实践：
- 初始延迟：800-1200ms（默认1000ms）
- 步骤间隔：1200-2000ms（默认1500ms）
- 高潮时刻：3500-4500ms（默认4000ms）
- 元素渐入：700ms
- 页面切换：1000ms

新增动画：
- `scaleIn`：从中心放大入场
- `fadeIn`：纯淡入
- `dash`：SVG流线动画（stroke-dashoffset）

#### 4. 主题切换支持
核心组件支持主题参数：
- **GlassCard**：自动适配 light/dark 背景、边框、阴影
- **ScriptFooter**：支持 light/dark/glass 三种风格
- 主题配置文件：`theme-presets.js`

### 🔧 改进优化

#### 组件增强
- GlassCard：增加主题参数，自动调整配色和阴影
- ScriptFooter：支持3种风格（light/dark/glass），自动匹配主题
- 所有动画：统一使用标准时序配置

#### 文档完善
- 新增主题风格使用指南
- 新增4种高级可视化组件文档
- 完善动画时序规范说明
- 增加适用场景和最佳实践

#### 模板文件
- `theme-presets.js`：主题配置、动画时序、命名规范
- `advanced-visualizers.jsx`：4种新增高级组件
- `animation-presets.css`：新增scaleIn、fadeIn、dash动画
- `core-components.jsx`：GlassCard和ScriptFooter支持主题

### 📦 技术栈
保持不变：
- React 18+
- Vite
- Tailwind CSS
- lucide-react

### 🔄 迁移说明
从 OpenClaw skill库 迁移到 Claude Code skill库：
- 位置：`~/.claude/skills/react-content-generator`
- 完整保留所有模板和文档
- 向后兼容 v1.0 的所有功能

### 🎯 使用方式
```bash
# 使用新主题
/react-content-generator "主题：开源LLM部署" --theme=dark-tech
/react-content-generator "主题：企业AI解决方案" --theme=warm-professional
/react-content-generator "主题：AI社交产品" --theme=dreamy-gradient

# 兼容旧版用法
/react-content-generator "主题：AI 搜索革命" --pages=5
```

---

## v1.0.0 (2026-04-25)

### 初始版本
- 基于 4 个成熟项目提炼设计系统
- Apple 风格 + 动画 + 配音文本
- 4种基础可视化组件
- 集成 react-video-generator 工作流
