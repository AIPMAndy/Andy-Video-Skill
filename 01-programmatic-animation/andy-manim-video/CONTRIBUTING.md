# Contributing to Andy Manim Video

感谢你考虑为 Andy Manim Video 做出贡献！

## 贡献方式

### 1. 报告 Bug

在 [GitHub Issues](https://github.com/AIPMAndy/andy-manim-video/issues) 提交问题时，请包含：

- **问题描述**: 清晰简洁的描述
- **重现步骤**: 详细的重现步骤
- **预期行为**: 你期望发生什么
- **实际行为**: 实际发生了什么
- **环境信息**: OS、Python 版本、Manim 版本
- **截图/日志**: 如果适用

### 2. 提交功能请求

描述你想要的功能，包括：
- 使用场景
- 预期效果
- 可能的实现方案

### 3. 提交代码

#### 开发环境设置

```bash
# 1. Fork 仓库
git clone https://github.com/YOUR_USERNAME/andy-manim-video.git
cd andy-manim-video

# 2. 安装依赖
npm install
pip install manim

# 3. 创建分支
git checkout -b feature/your-feature-name
```

#### 代码规范

- **Python**: 遵循 PEP 8
- **JavaScript**: 使用 ESLint
- **注释**: 英文注释，清晰简洁
- **提交信息**: 使用约定式提交

```bash
# 好的提交信息示例
feat: add cyberpunk color scheme
fix: resolve LaTeX dependency issue
docs: update installation guide
```

#### 测试

```bash
# 运行测试
npm test

# 测试新场景模板
cd examples/your-example
./render_all.sh low
```

#### 提交 Pull Request

1. 确保所有测试通过
2. 更新相关文档
3. 提交 PR，描述：
   - 改动内容
   - 解决的问题
   - 测试方法

### 4. 贡献场景模板

在 `templates/` 目录添加新模板：

```python
"""
Your Scene Template - Brief Description
"""

from manim import *

class YourScene(Scene):
    def construct(self):
        # Your implementation
        pass
```

附带：
- 使用示例
- 效果说明
- 参数文档

### 5. 贡献示例项目

在 `examples/` 目录添加完整示例：

```
examples/your-topic/
├── script.py
├── render_all.sh
└── README.md
```

## 行为准则

- 尊重所有贡献者
- 建设性反馈
- 包容不同观点
- 专注于项目目标

## 许可证

贡献的代码将遵循 MIT 许可证。

## 问题？

有任何问题，欢迎在 Issues 中讨论或发送邮件至 andy@example.com

---

再次感谢你的贡献！🎉
