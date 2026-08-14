#!/usr/bin/env node
/**
 * 批量生成工具 - 一次生成多首诗的文字雨动效
 */

import * as fs from 'fs';
import * as path from 'path';
import { EXAMPLE_POEMS, PRESETS, recommendPreset, applyPreset } from './presets';

interface BatchTask {
  text: string;
  preset?: string;
  outputName: string;
}

interface BatchConfig {
  tasks: BatchTask[];
  baseOutputDir: string;
  generateImages: boolean; // 是否调用 ChatGPT 生成背景图
  parallelLimit: number; // 并发数限制
}

/**
 * 解析批量配置文件
 */
function parseBatchConfig(configPath: string): BatchConfig {
  if (!fs.existsSync(configPath)) {
    throw new Error(`配置文件不存在: ${configPath}`);
  }

  const content = fs.readFileSync(configPath, 'utf-8');
  return JSON.parse(content);
}

/**
 * 生成单个项目
 */
async function generateOne(task: BatchTask, baseOutputDir: string): Promise<void> {
  const { generateHTML, generateSketch, generateImageTask } = await import('./generate.js');

  const outputDir = path.join(baseOutputDir, task.outputName);

  // 构建配置
  let config: any = {
    text: task.text,
    output: outputDir,
    noPreview: true,
  };

  // 应用预设
  if (task.preset && PRESETS[task.preset]) {
    config = applyPreset(task.preset, config);
  } else {
    // 智能推荐
    const recommended = recommendPreset(task.text);
    config = applyPreset(recommended, config);
  }

  // 创建目录
  const assetsDir = path.join(outputDir, 'assets');
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(assetsDir, { recursive: true });

  // 生成文件
  fs.writeFileSync(path.join(outputDir, 'index.html'), generateHTML(config));
  fs.writeFileSync(path.join(outputDir, 'sketch.js'), generateSketch(config));

  // 生成 ChatGPT 任务包
  const taskPacket = generateImageTask(config);
  fs.writeFileSync(path.join(outputDir, 'image-task.json'), JSON.stringify(taskPacket, null, 2));

  // 生成简化版 README
  const readme = `# ${task.text.split(/[，。、]/)[0]}

生成时间: ${new Date().toLocaleString('zh-CN')}
预设: ${task.preset || '自动推荐'}

## 运行

\`\`\`bash
cd ${outputDir}
python3 -m http.server 8000
\`\`\`

访问: http://localhost:8000
`;
  fs.writeFileSync(path.join(outputDir, 'README.md'), readme);

  console.log(`   ✅ ${task.outputName}`);
}

/**
 * 批量生成
 */
async function batchGenerate(config: BatchConfig): Promise<void> {
  console.log('🎨 批量文字雨生成器\n');
  console.log(`📋 任务数: ${config.tasks.length}`);
  console.log(`📂 输出目录: ${config.baseOutputDir}`);
  console.log(`🔄 并发限制: ${config.parallelLimit}\n`);

  // 创建基础输出目录
  fs.mkdirSync(config.baseOutputDir, { recursive: true });

  // 分批执行（控制并发）
  const tasks = config.tasks;
  for (let i = 0; i < tasks.length; i += config.parallelLimit) {
    const batch = tasks.slice(i, i + config.parallelLimit);
    console.log(`\n批次 ${Math.floor(i / config.parallelLimit) + 1}:`);

    await Promise.all(batch.map(task => generateOne(task, config.baseOutputDir)));
  }

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log('✅ 批量生成完成！\n');

  // 生成索引页面
  generateIndexPage(config);
}

/**
 * 生成索引页面（方便预览所有项目）
 */
function generateIndexPage(config: BatchConfig): void {
  const indexPath = path.join(config.baseOutputDir, 'index.html');

  const items = config.tasks
    .map(
      task => `
    <div class="card">
      <h3>${task.text.split(/[，。、]/)[0]}</h3>
      <p class="excerpt">${task.text}</p>
      <p class="meta">预设: ${task.preset || '自动推荐'}</p>
      <a href="${task.outputName}/index.html" target="_blank">查看动效</a>
    </div>
  `
    )
    .join('');

  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>文字雨作品集</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 40px 20px;
    }
    .container {
      max-width: 1200px;
      margin: 0 auto;
    }
    h1 {
      color: white;
      text-align: center;
      margin-bottom: 10px;
      font-size: 2.5rem;
    }
    .subtitle {
      color: rgba(255, 255, 255, 0.9);
      text-align: center;
      margin-bottom: 40px;
      font-size: 1.1rem;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 24px;
    }
    .card {
      background: white;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
    }
    .card h3 {
      color: #333;
      margin-bottom: 12px;
      font-size: 1.3rem;
    }
    .excerpt {
      color: #666;
      line-height: 1.6;
      margin-bottom: 12px;
      font-size: 0.95rem;
    }
    .meta {
      color: #999;
      font-size: 0.85rem;
      margin-bottom: 16px;
    }
    .card a {
      display: inline-block;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 10px 20px;
      border-radius: 6px;
      text-decoration: none;
      font-weight: 500;
      transition: opacity 0.2s;
    }
    .card a:hover {
      opacity: 0.9;
    }
    footer {
      text-align: center;
      color: rgba(255, 255, 255, 0.8);
      margin-top: 60px;
      font-size: 0.9rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🌧️ 文字雨作品集</h1>
    <p class="subtitle">生成时间: ${new Date().toLocaleString('zh-CN')} | 共 ${
    config.tasks.length
  } 个作品</p>

    <div class="grid">
      ${items}
    </div>

    <footer>
      <p>由 text-rain-generator 批量生成</p>
      <p>启动本地服务器后访问此页面</p>
    </footer>
  </div>
</body>
</html>`;

  fs.writeFileSync(indexPath, html);
  console.log(`📄 索引页面: ${indexPath}\n`);
}

/**
 * 创建示例配置文件
 */
function createExampleConfig(): void {
  const exampleConfig: BatchConfig = {
    tasks: [
      {
        text: '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
        preset: 'jiangnan',
        outputName: 'jingye-si',
      },
      {
        text: '春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。',
        preset: 'jiangnan',
        outputName: 'chun-xiao',
      },
      {
        text: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。',
        preset: 'beijing',
        outputName: 'deng-guan-que-lou',
      },
      {
        text: '两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。',
        preset: 'jiangnan',
        outputName: 'jue-ju',
      },
      {
        text: '清明时节雨纷纷，路上行人欲断魂。',
        preset: 'jiangnan',
        outputName: 'qing-ming',
      },
    ],
    baseOutputDir: './batch-output',
    generateImages: false,
    parallelLimit: 3,
  };

  fs.writeFileSync('batch-config.example.json', JSON.stringify(exampleConfig, null, 2));
  console.log('✅ 示例配置文件已创建: batch-config.example.json\n');
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.includes('--init')) {
    createExampleConfig();
    console.log('📝 编辑配置文件后运行:');
    console.log('   node batch-generate.ts --config batch-config.json\n');
    process.exit(0);
  }

  let configPath = 'batch-config.json';
  const configIndex = args.indexOf('--config');
  if (configIndex !== -1 && args[configIndex + 1]) {
    configPath = args[configIndex + 1];
  }

  if (!fs.existsSync(configPath)) {
    console.error(`❌ 配置文件不存在: ${configPath}`);
    console.log('\n运行以下命令创建示例配置:');
    console.log('   node batch-generate.ts --init\n');
    process.exit(1);
  }

  const config = parseBatchConfig(configPath);
  batchGenerate(config).catch(error => {
    console.error('❌ 批量生成失败:', error.message);
    process.exit(1);
  });
}

export { batchGenerate, BatchConfig, BatchTask };
