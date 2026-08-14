# Text Rain Generator - 开发者文档

## 项目结构

```
text-rain-generator/
├── SKILL.md              # Skill 文档（给 Claude 的执行指令）
├── README.md             # 项目概述（开发者视角）
├── USAGE.md              # 用户使用指南（详细教程）
├── DEVELOPER.md          # 本文件（开发者文档）
├── package.json          # 依赖和脚本配置
├── tsconfig.json         # TypeScript 配置
├── cli.ts                # CLI 入口（主要接口）
├── generate.ts           # 核心生成逻辑
├── presets.ts            # 预设配置和诗句库
├── test.ts               # 测试套件
├── export-video.ts       # 视频导出工具
├── batch-generate.ts     # 批量生成工具
├── sound-effects.ts      # 音效增强模块
└── quick-start.sh        # 快速示例脚本
```

## 架构设计

### 核心流程

```
用户调用 /text-rain-generator
        ↓
    cli.ts (解析参数)
        ↓
    generate.ts (生成 HTML/JS)
        ↓
    andy-relay (调度 ChatGPT 生图)
        ↓
    WebBridge (下载图片)
        ↓
    验证 & 预览
```

### 模块职责

#### 1. cli.ts - CLI 接口层

**职责**:
- 解析命令行参数
- 应用预设配置
- 智能推荐预设
- 输出执行结果（JSON 格式）

**关键函数**:
```typescript
parseArgs(): CLIArgs
applyPreset(presetName: string, baseConfig: any): any
main(): Promise<void>
```

#### 2. generate.ts - 核心生成逻辑

**职责**:
- 生成 HTML 文件
- 生成 p5.js sketch.js
- 生成 ChatGPT 任务包
- 生成 README

**关键函数**:
```typescript
generateHTML(config: Config): string
generateSketch(config: Config): string
generateImageTask(config: Config): object
```

**设计决策**:
- 使用模板字符串而非模板引擎（减少依赖）
- 配置参数直接嵌入代码（无需运行时解析）
- sketch.js 完全自包含（无需构建步骤）

#### 3. presets.ts - 预设系统

**职责**:
- 定义 20 种预设配置
- 存储经典诗句库
- 智能推荐预设

**数据结构**:
```typescript
interface Preset {
  name: string;
  description: string;
  scene: string;
  speed: number;
  tilt: number;
  color: string;
  fontSize: number;
  canvasWidth: number;
  canvasHeight: number;
}
```

**推荐算法**:
```typescript
function recommendPreset(poemText: string): string {
  // 关键词匹配
  if (text.includes('雪')) return 'snow';
  if (text.includes('雨')) return 'jiangnan';
  // ... 更多规则
  return 'jiangnan'; // 默认
}
```

#### 4. export-video.ts - 视频导出

**职责**:
- 逐帧渲染动画
- 使用 node-canvas 离线渲染
- 生成帧序列（PNG/JPG）

**技术栈**:
- `canvas` - Node.js canvas 实现
- 直接移植 p5.js 粒子系统逻辑

**性能考虑**:
- 每帧独立渲染（无共享状态）
- 支持 JPG 压缩（减少磁盘占用）
- 进度显示（每 30 帧）

#### 5. batch-generate.ts - 批量生成

**职责**:
- 读取 JSON 配置
- 并发控制（避免资源耗尽）
- 生成索引页面

**并发策略**:
```typescript
for (let i = 0; i < tasks.length; i += parallelLimit) {
  const batch = tasks.slice(i, i + parallelLimit);
  await Promise.all(batch.map(task => generateOne(task)));
}
```

#### 6. sound-effects.ts - 音效系统

**职责**:
- 音效配置管理
- sketch.js 代码注入
- 推荐音效资源

**实现方式**:
- 字符串替换注入（无需 AST 解析）
- CDN 音效资源（无需下载）
- 渐进增强（可选功能）

## 关键技术决策

### 1. 为什么用 TypeScript？

**优势**:
- 类型安全（减少运行时错误）
- 更好的 IDE 支持
- 渐进式采用（可混用 JS）

**妥协**:
- 生成的代码仍是纯 JS（兼容性）

### 2. 为什么不用模板引擎？

**原因**:
- 减少依赖（npm 包大小）
- 模板简单（字符串拼接足够）
- 更容易调试（直接看到生成结果）

**代价**:
- 代码可读性略差
- 转义处理需手动

### 3. 为什么用 p5.js 而非原生 Canvas？

**原因**:
- p5.js 语义更清晰（setup/draw 范式）
- 内置数学函数（sin/random/map）
- 社区资源丰富

**代价**:
- CDN 依赖（~1MB）
- 性能略低于原生

### 4. 为什么背景图通过 ChatGPT 生成？

**原因**:
- 用户已登录（无需额外配置）
- DALL-E 3 质量高
- andy-relay 已封装好

**替代方案**:
- Midjourney API（需付费）
- Stable Diffusion（需本地部署）
- 用户手动上传

## 扩展开发指南

### 添加新预设

1. 编辑 `presets.ts`：

```typescript
export const PRESETS: Record<string, Preset> = {
  // ... 现有预设
  myPreset: {
    name: '我的预设',
    description: '预设描述',
    scene: '场景描述（传给 ChatGPT）',
    speed: 2.5,
    tilt: 10,
    color: '#d4c5a9',
    fontSize: 24,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },
};
```

2. （可选）添加推荐规则：

```typescript
function recommendPreset(poemText: string): string {
  // ...
  if (text.includes('关键词')) return 'myPreset';
  // ...
}
```

3. 测试：

```bash
bun run cli.ts "测试诗句" --preset myPreset
```

### 修改粒子物理

编辑 `generate.ts` 中的 `generateSketch()` 函数：

```typescript
update(width: number, height: number, config: any) {
  // 修改重力
  this.y += this.speed * 1.2; // 原值 1.0

  // 修改摆动幅度
  this.x += Math.sin(this.wobblePhase) * 2.0; // 原值 this.wobbleAmplitude

  // 修改碰撞阈值
  if (brightness < 120) { // 原值 80
    // ...
  }
}
```

### 添加新输出格式

1. 创建新的生成函数：

```typescript
function generateForNewFormat(config: Config): string {
  // 实现新格式逻辑
}
```

2. 在 `cli.ts` 中调用：

```typescript
if (config.format === 'new-format') {
  fs.writeFileSync(
    path.join(outputDir, 'output.ext'),
    generateForNewFormat(config)
  );
}
```

### 集成新的图片生成服务

1. 创建新的任务包生成器：

```typescript
function generateMidjourneyTask(config: Config): object {
  return {
    prompt: `${config.scene} --ar 9:16 --style raw`,
    // Midjourney 特定参数
  };
}
```

2. 修改 `SKILL.md` 添加新服务的调用逻辑

## 测试

### 运行测试套件

```bash
cd ~/.claude/skills/text-rain-generator
bun run test
```

### 测试覆盖

- ✅ HTML 生成
- ✅ Sketch 生成
- ✅ 配置参数嵌入
- ✅ 文件系统操作
- ✅ 边界情况（空文本、特殊字符）

### 手动测试清单

- [ ] 基础生成（默认参数）
- [ ] 所有预设（20 个）
- [ ] 自定义参数
- [ ] 批量生成
- [ ] 视频导出
- [ ] 浏览器兼容性（Chrome/Firefox/Safari）
- [ ] 不同屏幕尺寸

### 性能基准

**生成速度**:
- 单个项目：<1 秒（不含背景图）
- 批量 10 个：~3 秒（parallelLimit=3）

**视频导出**:
- 10 秒 @ 30fps = 300 帧
- 1080×1920 PNG：~15 秒
- 1080×1920 JPG（质量 90）：~8 秒

**运行时性能**:
- 60fps @ 72 粒子：~10-15% CPU
- 内存：~50MB（包含背景图）

## 已知限制

1. **背景图生成依赖 ChatGPT**
   - 限流时会失败
   - 尺寸可能不精确（需要调整）

2. **音效需手动集成**
   - CDN 音效质量参差不齐
   - 需要用户手动下载

3. **视频导出需要 FFmpeg**
   - 用户需自行安装
   - 帧序列可能占用大量磁盘空间

4. **中文字体兼容性**
   - Windows 上可能显示异常
   - Web Font 加载较慢

## 未来改进

### 短期（v1.1）
- [ ] 自动调整背景图尺寸
- [ ] 内置音效库（本地文件）
- [ ] Web Font 支持
- [ ] 更多预设（30+）

### 中期（v1.5）
- [ ] 交互式参数调节面板
- [ ] 实时预览（Hot Reload）
- [ ] 社区预设分享平台
- [ ] 移动端适配

### 长期（v2.0）
- [ ] 3D 文字雨（Three.js）
- [ ] 物理引擎集成（Matter.js）
- [ ] WebGL 加速
- [ ] 云渲染服务

## 贡献指南

### 代码风格

- TypeScript strict mode
- 2 空格缩进
- 单引号字符串
- 无分号（除必需场景）

### 提交流程

1. 修改代码
2. 运行测试：`bun run test`
3. 手动验证：生成一个示例项目
4. 更新文档（如需要）

### 文档维护

- `SKILL.md` - Claude 执行逻辑变更
- `USAGE.md` - 用户功能变更
- `DEVELOPER.md` - 架构/API 变更
- `README.md` - 项目概述变更

## 联系方式

- 项目位置：`~/.claude/skills/text-rain-generator/`
- 开发者：Andy
- 版本：1.0.0
- 最后更新：2026-08-02

---

Happy Coding! 🌧️
