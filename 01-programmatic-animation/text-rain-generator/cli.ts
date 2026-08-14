#!/usr/bin/env node
/**
 * CLI 入口 - 由 Claude Code 调用
 * 处理完整工作流：生成项目 → 调用 andy-relay → 预览
 */

import * as fs from 'fs';
import * as path from 'path';
import { PRESETS, recommendPreset, applyPreset } from './presets';

interface CLIArgs {
  text?: string;
  scene?: string;
  preset?: string;
  speed?: number;
  tilt?: number;
  color?: string;
  fontSize?: number;
  canvasWidth?: number;
  canvasHeight?: number;
  output?: string;
  noPreview?: boolean;
  listPresets?: boolean;
  help?: boolean;
}

function printHelp() {
  console.log(`
🌧️  Text Rain Generator

用法:
  text-rain-generator <诗句> [选项]

示例:
  text-rain-generator "床前明月光，疑是地上霜"
  text-rain-generator "山重水复疑无路" --preset jiangnan
  text-rain-generator "清明时节雨纷纷" --scene "江南水乡" --speed 3

选项:
  --preset <name>        使用预设配置 (见下方列表)
  --scene <desc>         背景场景描述
  --speed <num>          雨速 (1-5, 默认 2.5)
  --tilt <deg>           倾斜角度 (0-30, 默认 10)
  --color <hex>          文字颜色 (默认 #d4c5a9)
  --font-size <px>       字体大小 (默认 24)
  --canvas-width <px>    画布宽度 (默认 1080)
  --canvas-height <px>   画布高度 (默认 1920)
  --output <dir>         输出目录 (默认 ./text-rain-output)
  --no-preview           不自动打开预览
  --list-presets         列出所有预设配置
  --help                 显示此帮助

可用预设:
${Object.entries(PRESETS)
  .map(([key, preset]) => `  ${key.padEnd(12)} - ${preset.name}: ${preset.description}`)
  .join('\n')}
`);
}

function listPresets() {
  console.log('\n📚 可用预设配置:\n');
  Object.entries(PRESETS).forEach(([key, preset]) => {
    console.log(`━━━ ${preset.name} (${key}) ━━━`);
    console.log(`描述: ${preset.description}`);
    console.log(`场景: ${preset.scene}`);
    console.log(`参数: 速度=${preset.speed}, 倾斜=${preset.tilt}°, 颜色=${preset.color}`);
    console.log(`尺寸: ${preset.canvasWidth}×${preset.canvasHeight}\n`);
  });
}

function parseArgs(): CLIArgs {
  const args = process.argv.slice(2);
  const parsed: CLIArgs = {};

  // 帮助和列表命令优先
  if (args.includes('--help') || args.includes('-h')) {
    parsed.help = true;
    return parsed;
  }
  if (args.includes('--list-presets')) {
    parsed.listPresets = true;
    return parsed;
  }

  // 第一个非flag参数作为诗句
  const textIndex = args.findIndex(arg => !arg.startsWith('--'));
  if (textIndex !== -1) {
    parsed.text = args[textIndex];
  }

  // 解析选项
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (!arg.startsWith('--')) continue;

    const key = arg.slice(2);
    const value = args[i + 1];

    switch (key) {
      case 'preset':
        parsed.preset = value;
        i++;
        break;
      case 'scene':
        parsed.scene = value;
        i++;
        break;
      case 'speed':
        parsed.speed = parseFloat(value);
        i++;
        break;
      case 'tilt':
        parsed.tilt = parseFloat(value);
        i++;
        break;
      case 'color':
        parsed.color = value;
        i++;
        break;
      case 'font-size':
        parsed.fontSize = parseInt(value);
        i++;
        break;
      case 'canvas-width':
        parsed.canvasWidth = parseInt(value);
        i++;
        break;
      case 'canvas-height':
        parsed.canvasHeight = parseInt(value);
        i++;
        break;
      case 'output':
        parsed.output = value;
        i++;
        break;
      case 'no-preview':
        parsed.noPreview = true;
        break;
    }
  }

  return parsed;
}

async function main() {
  const args = parseArgs();

  if (args.help) {
    printHelp();
    return;
  }

  if (args.listPresets) {
    listPresets();
    return;
  }

  if (!args.text) {
    console.error('❌ 错误: 必须提供诗句文本\n');
    console.log('运行 text-rain-generator --help 查看用法');
    process.exit(1);
  }

  console.log('🌧️  文字雨生成器\n');

  // 构建配置
  let config: any = {
    text: args.text,
    output: args.output || './text-rain-output',
    noPreview: args.noPreview || false,
  };

  // 应用预设（如果指定）
  if (args.preset) {
    if (!PRESETS[args.preset]) {
      console.error(`❌ 未知预设: ${args.preset}`);
      console.log('\n运行 text-rain-generator --list-presets 查看所有预设\n');
      process.exit(1);
    }
    console.log(`📋 使用预设: ${PRESETS[args.preset].name}`);
    config = applyPreset(args.preset, config);
  } else {
    // 智能推荐预设
    const recommended = recommendPreset(args.text);
    console.log(`💡 推荐预设: ${PRESETS[recommended].name} (使用 --preset ${recommended} 应用)`);
    config = applyPreset(recommended, config);
  }

  // 命令行参数覆盖预设
  if (args.scene) config.scene = args.scene;
  if (args.speed !== undefined) config.speed = args.speed;
  if (args.tilt !== undefined) config.tilt = args.tilt;
  if (args.color) config.color = args.color;
  if (args.fontSize !== undefined) config.fontSize = args.fontSize;
  if (args.canvasWidth !== undefined) config.canvasWidth = args.canvasWidth;
  if (args.canvasHeight !== undefined) config.canvasHeight = args.canvasHeight;

  console.log('\n📋 配置信息:');
  console.log(`   诗句: ${config.text}`);
  console.log(`   场景: ${config.scene}`);
  console.log(`   参数: 速度=${config.speed}, 倾斜=${config.tilt}°, 颜色=${config.color}`);
  console.log(`   尺寸: ${config.canvasWidth}×${config.canvasHeight}`);
  console.log(`   输出: ${config.output}\n`);

  // 生成项目（调用主生成脚本）
  const { generateHTML, generateSketch, generateImageTask } = await import('./generate.js');

  const outputDir = path.resolve(config.output);
  const assetsDir = path.join(outputDir, 'assets');

  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(assetsDir, { recursive: true });

  console.log('📝 生成项目文件...');

  // 生成所有文件
  fs.writeFileSync(path.join(outputDir, 'index.html'), generateHTML(config));
  fs.writeFileSync(path.join(outputDir, 'sketch.js'), generateSketch(config));

  // 生成 README
  const readme = `# 文字雨 - ${config.text.split(/[，。、]/)[0]}

> 生成时间: ${new Date().toLocaleString('zh-CN')}

## 快速运行

\`\`\`bash
cd ${outputDir}
python3 -m http.server 8000
# 访问 http://localhost:8000
\`\`\`

或直接运行:
\`\`\`bash
./preview.sh
\`\`\`

## 配置信息

- 诗句: ${config.text}
- 场景: ${config.scene}
- 速度: ${config.speed}
- 倾斜: ${config.tilt}°
- 颜色: ${config.color}
- 字号: ${config.fontSize}px
- 尺寸: ${config.canvasWidth}×${config.canvasHeight}

## 交互控制

- 鼠标点击 / 空格: 暂停/继续
- R 键: 重置
- 刷新: 重新开始

详细说明见项目文档: ~/.claude/skills/text-rain-generator/README.md
`;
  fs.writeFileSync(path.join(outputDir, 'README.md'), readme);

  // 生成启动脚本
  const previewScript = `#!/bin/bash
echo "🌧️  启动文字雨预览..."

if command -v python3 &> /dev/null; then
    echo "✅ 使用 Python 服务器"
    python3 -m http.server 8000 &
    SERVER_PID=$!
    sleep 2
    [[ "$OSTYPE" == "darwin"* ]] && open http://localhost:8000
    [[ "$OSTYPE" == "linux-gnu"* ]] && xdg-open http://localhost:8000
elif command -v bun &> /dev/null; then
    echo "✅ 使用 Bun"
    bun --hot . &
    SERVER_PID=$!
else
    open index.html
    exit 0
fi

echo "✅ 服务器已启动！按 Ctrl+C 停止"
trap "kill $SERVER_PID 2>/dev/null" EXIT
wait $SERVER_PID
`;
  const scriptPath = path.join(outputDir, 'preview.sh');
  fs.writeFileSync(scriptPath, previewScript);
  fs.chmodSync(scriptPath, '755');

  // 生成 ChatGPT 任务包
  const taskPacket = generateImageTask(config);
  fs.writeFileSync(
    path.join(outputDir, 'image-task.json'),
    JSON.stringify(taskPacket, null, 2)
  );

  console.log('   ✅ index.html');
  console.log('   ✅ sketch.js');
  console.log('   ✅ README.md');
  console.log('   ✅ preview.sh');
  console.log('   ✅ image-task.json\n');

  // 输出后续步骤（给 Claude 看的）
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ 项目已生成！\n');
  console.log('📋 后续步骤 (由 Claude Code 自动执行):\n');
  console.log('1️⃣  调用 /andy-relay 生成背景图');
  console.log(`   任务包: ${path.join(outputDir, 'image-task.json')}`);
  console.log(`   目标路径: ${path.join(assetsDir, 'background.png')}\n`);
  console.log('2️⃣  下载并验证图片');
  console.log(`   验证尺寸: ${config.canvasWidth}×${config.canvasHeight}`);
  console.log('   验证格式: PNG/JPG\n');
  console.log('3️⃣  通过 WebBridge 打开预览');
  console.log(`   URL: http://localhost:8000/index.html\n`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  console.log(`📂 输出目录: ${outputDir}\n`);

  // 返回关键路径（JSON格式，方便 Claude 解析）
  const result = {
    success: true,
    outputDir,
    taskPacketPath: path.join(outputDir, 'image-task.json'),
    backgroundPath: path.join(assetsDir, 'background.png'),
    indexPath: path.join(outputDir, 'index.html'),
    config,
  };

  console.log('📊 执行结果 (JSON):');
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  main().catch(error => {
    console.error('❌ 错误:', error.message);
    console.error(error.stack);
    process.exit(1);
  });
}
