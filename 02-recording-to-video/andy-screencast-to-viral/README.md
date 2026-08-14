# Andy's Screencast-to-Viral Pipeline

**目标**: 将42个录屏素材自动转化成100+爆款短视频，达到10万粉丝

## 🎯 现状

✅ **已完成**（2026-08-09）:
- 完整的技术方案设计
- 智能分析器（提取高光时刻）
- 智能剪辑器（生成30/60/90秒短视频）
- 批量处理系统
- 平台适配（抖音/B站/小红书）
- **已成功测试**：从120秒录屏生成30秒抖音短视频

✅ **测试结果**:
```
输入: GPT做电脑壁纸.mp4 (120.4秒, 45.4MB)
输出: 30秒抖音短视频 (1080×1920, 1.3MB)
      + 5个标题变体
      + Hook文案
      + 完整元数据
```

## 🚀 快速开始

### 1. 检查依赖

```bash
cd ~/.claude/skills/andy-screencast-to-viral
python3 viral.py doctor
```

需要安装:
- ✅ ffmpeg（已安装）
- ✅ ffprobe（已安装）
- ⚠️ whisper（推荐安装）: `pip install openai-whisper`

### 2. 处理单个视频

```bash
# 分析视频
python3 viral.py analyze "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4"

# 生成30秒抖音短视频
python3 viral.py generate \
  "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4" \
  "./analysis/GPT做电脑壁纸_analysis.json" \
  30 \
  douyin
```

### 3. 批量处理（推荐）

```bash
# 处理前10个视频（测试）
python3 viral.py batch \
  "/Users/andy/Documents/Andy录屏素材库" \
  --limit 10 \
  --durations 30,60 \
  --platforms douyin

# 处理全部42个视频
python3 viral.py batch \
  "/Users/andy/Documents/Andy录屏素材库" \
  --durations 30,60 \
  --platforms douyin,bilibili
```

## 📊 Pipeline工作流

```
录屏素材 (2-10分钟)
    ↓
[Stage 1: 分析]
- 提取元数据
- 语音转文字 (Whisper)
- 提取关键帧
- 识别高光时刻
    ↓
[Stage 2: 剪辑]
- 提取精华片段
- 删除冗余部分
- 智能变速
    ↓
[Stage 3: 包装]
- 添加开场Hook
- 生成字幕
- 混合背景音乐
    ↓
[Stage 4: 适配]
- 平台格式转换
- 生成标题变体
- 制作封面
    ↓
短视频 (30-90秒) + 元数据
```

## 🎬 输出结构

```
batch_output/
├── 视频01/
│   ├── analysis/
│   │   ├── 视频01_analysis.json
│   │   ├── 视频01_audio.mp3
│   │   └── frames/
│   └── clips/
│       ├── 30s_douyin/
│       │   ├── 视频01_30s_base_douyin.mp4
│       │   └── 视频01_30s_base_douyin_metadata.json
│       └── 60s_douyin/
│           └── ...
├── 视频02/
└── batch_report_20260809_215500.json
```

## 💡 核心功能

### 1. 智能高光识别

- **语音密度分析**: 识别激动时刻（>3词/秒）
- **关键词检测**: "哇"、"太"、"真的"、"成功"等
- **结构化片段**: 自动识别开场/过程/结果

### 2. MrBeast爆款原则

- ✅ **CTR优化**: 数字化标题 + 悬念感
- ✅ **AVD优化**: 前3秒Hook + 无废话剪辑
- ✅ **阶梯递进**: 持续升级，不能平

### 3. 多平台适配

| 平台 | 尺寸 | 时长 | 特点 |
|------|------|------|------|
| 抖音 | 1080×1920 (9:16) | 30-90s | 完播率优先 |
| B站 | 1920×1080 (16:9) | 60-180s | 信息密度高 |
| 小红书 | 1080×1440 (3:4) | 30-60s | 视觉吸引力 |

### 4. 标题生成（MrBeast公式）

```python
templates = [
    "用AI{动作}{结果}，只用了{N}秒",
    "{之前}到{之后}，差距惊人",
    "终于发现{秘密}了...",
    "{N}个{工具}同时{动作}会怎样",
]
```

## 📈 成功指标

### 短期目标（1个月）
- [ ] 处理完42个录屏素材
- [ ] 生成至少100条短视频
- [ ] 测试完3个平台
- [ ] 找到1-2个爆款模板（完播率>50%）

### 中期目标（3个月）
- [ ] 粉丝突破1万
- [ ] 单条播放量过10万
- [ ] 稳定日更（2-3条/天）
- [ ] 形成固定风格和IP

### 最终目标（6个月）
- [ ] **粉丝突破10万** ⭐
- [ ] 商业化（接广告/带货）
- [ ] 建立素材库和模板库
- [ ] 形成可复制的生产流程

## ⚙️ 配置选项

创建 `viral-config.json`:

```json
{
  "defaults": {
    "duration": 60,
    "platform": "douyin",
    "hook": "question"
  },
  "audio": {
    "bgm_volume": 0.25,
    "voice_volume": 0.75
  },
  "subtitle": {
    "font": "PingFang SC",
    "size": 48,
    "color": "#FFFFFF"
  },
  "quality": {
    "video_bitrate": "6000k",
    "audio_bitrate": "128k"
  }
}
```

## 🐛 故障排除

### 问题: Whisper未安装
```bash
pip install openai-whisper
```

### 问题: ffmpeg未找到
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### 问题: 生成的视频文件过大
```bash
# 在editor.py中降低码率
--video-bitrate 4000k
```

### 问题: 语音识别不准确
```bash
# 使用更大的Whisper模型
whisper audio.mp3 --model large
```

## 📝 下一步计划

### 立即执行（本周）
1. ✅ 完成核心pipeline开发
2. ✅ 测试单个视频处理
3. ⏳ 安装Whisper提升语音识别
4. ⏳ 批量处理10个最优质素材
5. ⏳ 发布到抖音测试反馈

### 本月计划
1. 优化标题生成算法
2. 添加自动字幕功能
3. 集成背景音乐库
4. 开发封面自动生成
5. 处理全部42个素材

### 长期规划
1. 建立爆款模板库
2. 添加A/B测试系统
3. 集成数据分析面板
4. 开发自动发布功能
5. 扩展到更多平台

## 🔗 相关资源

- **方案文档**: `/Users/andy/Documents/AICode/09 Andy-Video-SKill/SCREENCAST_TO_VIRAL_PLAN.md`
- **录屏素材库**: `/Users/andy/Documents/Andy录屏素材库` (42个文件, 5.7GB)
- **MrBeast方法论**: `~/.claude/skills/mrbeast-skill/`
- **视频分析技能**: `~/.claude/skills/video-content-analysis.md`

## 📞 使用支持

遇到问题？
1. 运行 `python3 viral.py doctor` 检查环境
2. 查看 `batch_report_*.json` 了解处理状态
3. 检查 `output/` 目录下的日志文件

---

**版本**: 1.0.0 (MVP)  
**创建日期**: 2026-08-09  
**状态**: ✅ 核心功能已验证，可投入生产使用  
**目标**: 10万粉丝
