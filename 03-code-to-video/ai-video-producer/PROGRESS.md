# AI Video Producer - 开发进度

## ✅ 已完成（2026-04-14 22:40）

### 1. Skill 骨架搭建
- ✅ 创建目录结构：`~/.openclaw/workspace/skills/ai-video-producer/`
- ✅ 编写 `SKILL.md` 文档（完整的使用说明）
- ✅ 创建 `config.json` 配置文件

### 2. 核心模块实现
- ✅ `modules/1-topic-generator.mjs` - 选题生成模块
- ✅ `modules/2-ppt-generator.mjs` - React PPT 生成模块
- ✅ `modules/3-video-recorder.mjs` - 视频录制模块（**已整合 Codex 方案**）
- ✅ `index.mjs` - 主入口文件（交互式流程）

### 3. 技术方案确认
- **选题生成**：OpenClaw browser 工具 + GitHub Trending
- **PPT 生成**：基于 Andy 的实际项目模板（`.codex-react-video-job`）
- **视频录制**：✅ **已整合 Codex 固化方案**
  - 自动提取 `ScriptFooter` 配音文本
  - 使用 `edge-tts` 生成中文配音
  - Playwright 录制（根据音频时长自动控制每页停留时间）
  - FFmpeg 转码、加速、合成
  - 自动生成视频封面

### 4. Codex 方案学习完成 ✅
- ✅ 学习了 `/Users/andy/Desktop/02 AI+产品/AI知识视频生成工具/.claude/skills/react-video-generator/`
- ✅ 理解了完整的工作流程：
  1. 从 React 代码提取配音文本
  2. 使用 edge-tts 生成配音
  3. Playwright 录制（根据音频时长控制）
  4. FFmpeg 加速、合成、生成封面
- ✅ 已完整集成到 `modules/3-video-recorder.mjs`

---

## ⏳ 待完善

### 1. 选题生成模块
- [ ] 集成 OpenClaw browser 工具（目前是模拟数据）
- [ ] 实现 GitHub Trending 爬取逻辑
- [ ] 集成 feishu_create_doc 工具保存文档

### 2. PPT 生成模块
- [ ] 从 Andy 的项目复制完整模板到 `templates/react-ppt-template/`
- [ ] 优化场景组件生成逻辑（根据选题内容生成不同类型的场景）
- [ ] 支持更多场景类型（封面、痛点、架构、演示、金句、总结）

### 3. 依赖安装
- [ ] 自动检测并安装 `edge-tts`（Python 包）
- [ ] 自动检测并安装 `playwright`（Node.js 包）
- [ ] 自动检测 `ffmpeg` 是否安装

### 4. 测试与优化
- [ ] 端到端测试完整流程
- [ ] 错误处理优化
- [ ] 性能优化（并行处理、缓存）

---

## 📋 使用方式

```bash
# 进入 Skill 目录
cd ~/.openclaw/workspace/skills/ai-video-producer

# 一键启动
node index.mjs
```

---

## 🎯 核心优势（整合 Codex 方案后）

### 1. 自动配音
- 从 React 代码自动提取 `ScriptFooter` 文案
- 使用 `edge-tts` 生成高质量中文配音
- 支持自定义语速、音调、音量

### 2. 智能录制
- 根据音频时长自动控制每页停留时间
- 不需要手动设置场景时长
- 自动处理场景切换

### 3. 高质量输出
- 1536x2048 高清分辨率
- 支持视频加速（默认 1.2x）
- 自动生成视频封面
- 自动裁掉开头白屏

### 4. 完整自动化
- 从选题到成片全自动
- 只需人工确认选题
- 一键生成高质量视频

---

## 🎯 下一步行动

### Andy 提供
- ✅ 已提供 Codex 方案参考
- [ ] 确认模板文件是否需要调整
- [ ] 提供实际的选题示例（用于测试）

### 小天完成
- ✅ 已整合 Codex 视频录制方案
- [ ] 集成 OpenClaw 工具（browser、feishu_create_doc）
- [ ] 完善依赖检测和安装
- [ ] 端到端测试

### 联调测试
- [ ] 跑通完整流程
- [ ] 修复 bug
- [ ] 优化体验

---

**更新时间**：2026-04-14 22:40  
**当前状态**：视频录制模块已完成（整合 Codex 方案），选题和 PPT 生成待完善
