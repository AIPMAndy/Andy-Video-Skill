# React Video - Knowledge Video Generator

基于你提供的两个优秀案例（prompts.chat 和 Firecrawl），我已经优化了 `react-video` skill，添加了专业的知识视频生成功能。

## ✨ 新功能

### 知识视频模板生成器

通过简单的 JSON 配置文件，自动生成 Apple 风格的专业知识视频，包含：

- 🎨 **玻璃态设计** - Apple 风格的毛玻璃卡片效果
- 🎬 **多种场景类型** - 封面、痛点、功能、金句、总结
- 🎯 **智能动画** - 自动播放的流畅过渡动画
- 📱 **响应式布局** - 适配不同尺寸
- 🎨 **主题定制** - 支持多种配色方案

## 🚀 快速开始

### 方式 1：使用示例配置

```bash
/react-video --template knowledge --config template/knowledge-video-config.example.json
```

### 方式 2：创建自定义配置

1. 复制示例配置文件：
```bash
cp template/knowledge-video-config.example.json my-project-config.json
```

2. 编辑配置文件（参考下方结构）

3. 生成视频：
```bash
/react-video --template knowledge --config my-project-config.json --width 1920 --height 1080
```

## 📋 配置文件结构

```json
{
  "themeColor": "indigo",  // 主题色：indigo, orange, blue, emerald, purple, red
  "project": {
    "name": "项目名称",
    "stars": "162k+",
    "courseNumber": "第 340 课",
    "category": "分类标签"
  },
  "steps": [
    {
      "type": "cover",           // 封面页
      "title": "主标题",
      "subtitle": "副标题",
      "script": "底部解说词..."
    },
    {
      "type": "pain_point",      // 痛点展示
      "title": "问题描述",
      "visualizer": {
        "items": [...]           // 问题列表
      }
    },
    {
      "type": "feature",         // 功能特性
      "title": "解决方案",
      "visualizer": {
        "steps": [...]           // 步骤列表
      }
    },
    {
      "type": "golden_sentence", // 金句页
      "quote": "引用文字",
      "explanation": "解释说明"
    },
    {
      "type": "summary",         // 总结页
      "points": [...]            // 要点列表
    }
  ]
}
```

## 📚 示例配置

项目包含两个完整示例：

1. **prompts.chat** - `knowledge-video-config.example.json`
   - 主题色：indigo（靛蓝）
   - 展示社区平台类项目

2. **Firecrawl** - `knowledge-video-config-firecrawl.example.json`
   - 主题色：orange（橙色）
   - 展示技术工具类项目

## 🎨 支持的场景类型

### 1. Cover（封面）
- 项目介绍
- 星标展示
- 课程编号

### 2. Pain Point（痛点）
- 问题可视化
- 多个痛点展示
- 动画效果

### 3. Feature（功能）
- 解决方案展示
- 步骤流程
- 特性列表

### 4. Golden Sentence（金句）
- 哲学性总结
- 视觉冲击
- 品牌理念

### 5. Summary（总结）
- 要点回顾
- 行动号召
- 作者信息

## 🎯 使用场景

- ✅ 技术项目介绍视频
- ✅ 开源项目宣传
- ✅ 教程/课程内容
- ✅ 产品演示
- ✅ 技术分享
- ✅ 知识科普

## 📖 详细文档

查看 `KNOWLEDGE_VIDEO_GUIDE.md` 获取：
- 完整配置说明
- 图标列表
- 颜色方案
- 最佳实践
- 故障排除

## 🛠️ 技术栈

- **React** - UI 框架
- **Tailwind CSS** - 样式系统
- **Lucide React** - 图标库
- **Vite** - 构建工具
- **Playwright** - 浏览器录制
- **FFmpeg** - 视频转码

## 💡 设计灵感

基于以下优秀案例的设计模式：
- Apple 官网的玻璃态设计
- prompts.chat 知识视频
- Firecrawl 知识视频

## 🔧 自定义开发

如果需要添加自定义可视化组件：

1. 编辑 `template/src/knowledge-video-generator.jsx`
2. 在 `renderStep` 函数中添加新的 case
3. 创建对应的可视化组件
4. 在配置文件中使用新类型

## 📝 注意事项

- 确保已安装 ffmpeg：`brew install ffmpeg`（macOS）
- Node.js 版本 >= 16
- 首次运行会自动安装 Playwright
- 视频生成时间取决于总时长和复杂度

## 🎬 输出

默认输出路径：`.react-video-job/output/video/react-video.mp4`

可通过 `--output` 参数自定义输出路径。

## 🤝 贡献

欢迎提交 Issue 和 PR 来改进这个 skill！

---

**作者**: AI酋长Andy  
**更新时间**: 2026-05-29
