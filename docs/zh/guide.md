# 使用指南

## 选择合适的 Skill

根据任务选类目：

| 我想... | 选用类目 |
|---------|----------|
| 程序化生成数学/AI 动画 | 01 程序化动画 |
| 把录屏转成短视频 | 02 录屏转视频 |
| 把 React 代码或 HTML 页面渲染成 MP4 | 03 代码转视频 |
| 撰写或校验爆款脚本 | 04 脚本与策划 |
| 制作风格化手作解释视频 | 05 风格化效果 |

## 工作流

1. 浏览 [CATALOG](../../CATALOG.md) 选定 skill
2. 按 [INSTALLATION](../../INSTALLATION.md) 安装
3. 重启 Claude Code
4. 按 SKILL.md 调用

## 更新 Skill

源 skill 发布新版本时：

```bash
./scripts/update-skill.sh andy-manim-video
```

脚本会从源路径覆盖本地副本并更新 `CHANGELOG.md`。

## 新增 Skill

```bash
./scripts/new-skill.sh my-new-skill --category 01-programmatic-animation
```

在指定类目下创建脚手架目录，含占位 `SKILL.md`。填充内容后更新 `CATALOG.md`。