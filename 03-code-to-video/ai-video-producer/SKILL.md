# AI Video Producer Skill

**一键生成 AI 知识视频的完整自动化流程**

## 功能概述

从 GitHub Trending 爬取最新开源项目 → 生成选题文档 → 生成 React PPT 代码 → 自动录制视频 → 输出成品

## 使用方法

### 一键启动（推荐）

```bash
cd ~/.openclaw/workspace/skills/ai-video-producer
node index.mjs
```

### 交互式确认

执行过程中会在选题生成后暂停，让你确认：
- 输入 `y` 继续执行
- 输入 `n` 重新生成选题
- 输入 `e` 编辑选题后继续

### 配置文件

编辑 `config.json` 自定义行为：

```json
{
  "github": {
    "trendingUrl": "https://github.com/trending",
    "languages": ["python", "typescript"],
    "minStars": 10000,
    "timeRange": "monthly"
  },
  "output": {
    "topicDocFolder": "AI专用知识库/素材/AI知识视频素材",
    "videoDir": "/Users/andy/Desktop/AI视频/",
    "reactProjectDir": "/Users/andy/Desktop/公众号发布/"
  },
  "video": {
    "width": 1536,
    "height": 2048,
    "fps": 30
  },
  "autoConfirm": false
}
```

## 工作流程

### 第1步：选题生成

**输入**：GitHub Trending 页面

**处理**：
1. 使用 OpenClaw 浏览器控制访问 GitHub Trending
2. 筛选符合条件的项目（真实可用、有影响力、较新）
3. 为每个项目生成：
   - 选题名称
   - 视频标题
   - 钩子文案
   - GitHub 星数
   - 项目描述
   - 使用场景
   - 核心价值

**输出**：飞书文档（存储在 AI 专用知识库/素材目录）

**状态**：✅ 已实现

---

### 第2步：React PPT 生成

**输入**：第1步的选题文档

**处理**：
1. 读取选题内容
2. 基于模板生成 React 组件代码
3. 使用 `social-video-layout.jsx` 提供的布局组件
4. 生成场景切换逻辑

**输出**：完整的 React 项目（包含 JSX、配置文件）

**技术栈**：
- React 19
- Vite
- TailwindCSS
- Lucide Icons

**状态**：⏳ 待实现

---

### 第3步：视频自动化录制

**输入**：第2步生成的 React 项目

**处理**：
1. 启动 Vite 开发服务器
2. 使用 Playwright 启动无头浏览器
3. 录制网页内容为 WebM 视频
4. 使用 FFmpeg 转码为 MP4
5. 可选：合成语音旁白

**技术方案**：
- Playwright（浏览器自动化）
- FFmpeg（视频转码）
- 可选：ElevenLabs TTS（语音合成）

**输出**：MP4 视频文件

**状态**：⏳ 待抽象化

---

### 第4步：人工发布

**输入**：第3步生成的视频文件

**处理**：Andy 人工审核并发布到目标平台

**状态**：✅ 流程明确

---

## 核心模块

### modules/1-topic-generator.mjs

负责从 GitHub Trending 生成选题文档

**主要函数**：
- `fetchTrending(languages, timeRange)` - 爬取 GitHub Trending
- `filterProjects(projects, minStars)` - 筛选项目
- `generateTopicDoc(projects)` - 生成选题文档
- `saveToFeishu(doc, folder)` - 保存到飞书知识库

---

### modules/2-ppt-generator.mjs

负责生成 React PPT 代码

**主要函数**：
- `loadTemplate()` - 加载 React 模板
- `generateScenes(topics)` - 生成场景组件
- `generateMainComponent(scenes)` - 生成主组件
- `writeReactProject(code, outputDir)` - 写入项目文件

---

### modules/3-video-recorder.mjs

负责录制视频

**主要函数**：
- `startDevServer(projectDir, port)` - 启动开发服务器
- `recordWithPlaywright(url, duration, outputPath)` - 录制视频
- `transcodeToMp4(webmPath, mp4Path, options)` - 转码视频
- `addVoiceover(videoPath, audioPath, outputPath)` - 合成语音

---

## 模板文件

### templates/react-ppt-template/

包含完整的 React 项目模板：

```
templates/react-ppt-template/
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── index.html
├── scripts/
│   └── render-video.mjs
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── video-runtime.js
    └── social-video-layout.jsx
```

**关键组件**：
- `useAutoplayScenes()` - 自动场景切换 Hook
- `ThreeFourCanvas` - 3:4 画布容器
- `ScriptFooter` - 底部文案组件
- `SceneBadge` - 场景标签组件
- `GlassCard` - 毛玻璃卡片组件

---

## 依赖项

### Node.js 包
- `playwright` - 浏览器自动化
- `vite` - 开发服务器
- `react` - UI 框架
- `tailwindcss` - 样式框架
- `lucide-react` - 图标库

### 系统工具
- `ffmpeg` - 视频处理（需要预装）

### OpenClaw 工具
- `browser` - 浏览器控制
- `feishu_create_doc` - 飞书文档创建

---

## 示例输出

### 选题文档示例

```markdown
# AI知识视频选题 - 2026-04-14

## 选题1：Microsoft MarkItDown
- **GitHub星数**：107,953
- **标题**：微软开源神器！一键把任何文档转成Markdown
- **钩子**：PDF、Word、PPT、Excel...你电脑里的各种文件格式...
- **使用场景**：文档转换、RAG知识库、内容提取
- **核心价值**：支持Office全家桶、本地运行、数据不出本地
```

### React 组件示例

```jsx
const MarkItDownScene = ({ isActive }) => {
  const [step, setStep] = useState(0);
  
  useEffect(() => {
    if (!isActive) return;
    const timer1 = setTimeout(() => setStep(1), 800);
    const timer2 = setTimeout(() => setStep(2), 2200);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [isActive]);
  
  return (
    <div className="flex h-full w-full items-center justify-center">
      {/* 场景内容 */}
    </div>
  );
};
```

---

## 故障排查

### 浏览器录制失败
- 检查 Playwright 是否正确安装：`npx playwright install chromium`
- 确认端口未被占用：`lsof -i :4173`

### FFmpeg 转码失败
- 确认 FFmpeg 已安装：`ffmpeg -version`
- 检查输入文件是否存在

### 飞书文档创建失败
- 确认飞书 OAuth 已授权
- 检查目标文件夹是否存在

---

## 未来优化

- [ ] 支持自动生成语音旁白
- [ ] 支持批量生成多个视频
- [ ] 支持自定义视频模板
- [ ] 支持自动发布到抖音/B站
- [ ] 支持视频质量检查

---

**创建时间**：2026-04-14  
**维护者**：Andy + 小天  
**优先级**：P0
