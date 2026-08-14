import { spawn, execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { chromium } from 'playwright';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载配置
const config = JSON.parse(
  readFileSync(join(__dirname, '../config.json'), 'utf-8')
);

/**
 * 等待指定时间
 */
function wait(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * 获取音频时长
 * @param {string} audioPath - 音频文件路径
 * @returns {number} 时长（秒）
 */
function getAudioDuration(audioPath) {
  const cmd = `ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "${audioPath}"`;
  const result = execSync(cmd, { encoding: 'utf-8' });
  return parseFloat(result.trim());
}

/**
 * 从 React 代码中提取配音文本
 * @param {string} appJsxPath - App.jsx 文件路径
 * @returns {string[]} 配音文本数组
 */
export function extractVoiceoverTexts(appJsxPath) {
  console.log('📝 提取配音文本...');
  
  const appContent = readFileSync(appJsxPath, 'utf-8');
  
  // 提取 ScriptFooter 中的 text
  const scriptTexts = [];
  const regex = /<ScriptFooter\s+text=\{?"([^"]+)"\}?\s*\/>/g;
  let match;
  
  while ((match = regex.exec(appContent)) !== null) {
    scriptTexts.push(match[1]);
  }
  
  if (scriptTexts.length === 0) {
    throw new Error('未找到 ScriptFooter 配音文本');
  }
  
  console.log(`✓ 找到 ${scriptTexts.length} 段配音文本\n`);
  return scriptTexts;
}

/**
 * 生成配音（使用 edge-tts）
 * @param {string[]} texts - 配音文本数组
 * @param {string} outputDir - 输出目录
 * @returns {Promise<string[]>} 音频文件路径数组
 */
export async function generateVoiceover(texts, outputDir) {
  console.log('🎤 生成配音...');
  
  mkdirSync(outputDir, { recursive: true });
  
  // 写入临时文本文件
  const textPath = join(outputDir, 'voiceover_texts.txt');
  writeFileSync(textPath, texts.join('\n---\n'));
  
  // 创建 Python 脚本
  const pythonScript = `
#!/usr/bin/env python3
import asyncio
import pathlib
import sys

try:
    import edge_tts
except ImportError:
    print('Installing edge-tts...', file=sys.stderr)
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'edge-tts'])
    import edge_tts

TEXT_PATH = pathlib.Path('${textPath}')
OUT_DIR = pathlib.Path('${outputDir}')
OUT_DIR.mkdir(parents=True, exist_ok=True)

segments = [part.strip() for part in TEXT_PATH.read_text(encoding='utf-8').split('\\n---\\n') if part.strip()]

async def synthesize(index: int, text: str):
    out = OUT_DIR / f'step-{index:02d}.mp3'
    communicate = edge_tts.Communicate(text, 'zh-CN-YunxiNeural', rate='-8%', pitch='-2Hz', volume='+8%')
    await communicate.save(str(out))
    print(f'saved {out}')

async def main():
    for idx, text in enumerate(segments):
        await synthesize(idx, text)

asyncio.run(main())
`;
  
  const scriptPath = join(outputDir, 'generate_voiceover.py');
  writeFileSync(scriptPath, pythonScript);
  
  // 执行 Python 脚本
  execSync(`python3 "${scriptPath}"`, { stdio: 'inherit' });
  
  // 返回生成的音频文件路径
  const audioPaths = texts.map((_, i) => 
    join(outputDir, `step-${String(i).padStart(2, '0')}.mp3`)
  );
  
  console.log('✅ 配音生成完成\n');
  return audioPaths;
}

/**
 * 启动开发服务器
 * @param {string} projectDir - 项目目录
 * @param {number} port - 端口号
 * @returns {Promise<Object>} 服务器信息
 */
export async function startDevServer(projectDir, port = 4173) {
  console.log(`🚀 启动开发服务器 (端口 ${port})...`);
  
  return new Promise((resolve, reject) => {
    const child = spawn(
      'npm',
      ['run', 'dev', '--', '--host', '127.0.0.1', '--port', String(port)],
      {
        cwd: projectDir,
        stdio: 'pipe',
        shell: true,
        env: { ...process.env, BROWSER: 'none' }
      }
    );
    
    let resolved = false;
    let serverUrl = `http://127.0.0.1:${port}`;
    
    const done = () => {
      if (!resolved) {
        resolved = true;
        resolve({ child, url: serverUrl });
      }
    };
    
    child.stdout.on('data', (buf) => {
      const text = buf.toString();
      process.stdout.write(text);
      const match = text.match(/http:\/\/127\.0\.0\.1:(\d+)/);
      if (match) {
        serverUrl = `http://127.0.0.1:${match[1]}`;
        done();
      }
    });
    
    child.stderr.on('data', (buf) => process.stderr.write(buf.toString()));
    child.on('error', reject);
    child.on('exit', (code) => {
      if (!resolved) {
        reject(new Error(`dev server exited early: ${code}`));
      }
    });
    
    setTimeout(done, 5000);
  });
}

/**
 * 使用 Playwright 录制视频（根据音频时长自动控制）
 * @param {string} serverUrl - 服务器 URL
 * @param {string[]} audioPaths - 音频文件路径数组
 * @param {string} outputDir - 输出目录
 * @param {Object} options - 录制选项
 * @returns {Promise<string>} 视频文件路径
 */
export async function recordWithPlaywright(serverUrl, audioPaths, outputDir, options = {}) {
  console.log('🎥 开始录制视频...');
  
  const {
    width = config.video.width,
    height = config.video.height
  } = options;
  
  mkdirSync(outputDir, { recursive: true });
  
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: 1,
    recordVideo: {
      dir: outputDir,
      size: { width, height }
    }
  });
  
  const page = await context.newPage();
  
  try {
    await page.goto(`${serverUrl}/?step=0`, { waitUntil: 'networkidle' });
    await wait(2000); // 等待首页动画完成
    
    for (let step = 0; step < audioPaths.length; step++) {
      const audioPath = audioPaths[step];
      const duration = getAudioDuration(audioPath);
      const waitTime = (duration + 0.5) * 1000; // 音频时长 + 0.5秒缓冲
      
      console.log(`  场景 ${step + 1}: 等待 ${(waitTime / 1000).toFixed(1)}s`);
      await wait(waitTime);
      
      if (step < audioPaths.length - 1) {
        await page.click('body');
        await wait(500);
      }
    }
    
    const video = page.video();
    await context.close();
    const webmPath = await video.path();
    
    console.log('✅ 视频录制完成\n');
    return webmPath;
    
  } finally {
    await browser.close();
  }
}

/**
 * 转码并合成最终视频
 * @param {string} webmPath - WebM 视频路径
 * @param {string[]} audioPaths - 音频文件路径数组
 * @param {string} outputPath - 输出路径
 * @param {Object} options - 转码选项
 * @returns {Promise<void>}
 */
export async function transcodeAndMerge(webmPath, audioPaths, outputPath, options = {}) {
  console.log('🎬 转码并合成视频...');
  
  const {
    speed = 1.2,
    trimStartSec = 3
  } = options;
  
  const tempDir = join(dirname(outputPath), 'tmp');
  mkdirSync(tempDir, { recursive: true });
  
  // 1. 加速视频并裁掉开头白屏
  const tempVideoPath = join(tempDir, `temp-video-${speed}x.mp4`);
  execSync(
    `ffmpeg -y -ss ${trimStartSec} -i "${webmPath}" -filter:v "setpts=PTS/${speed}" -c:v libx264 -preset medium -crf 18 -an "${tempVideoPath}"`,
    { stdio: 'pipe' }
  );
  
  // 2. 合并音频
  const concatContent = audioPaths.map((path, i) => 
    `file '${path}'`
  ).join('\n');
  const concatPath = join(tempDir, 'concat.txt');
  writeFileSync(concatPath, concatContent);
  
  const mergedAudioPath = join(tempDir, `audio-${speed}x.mp3`);
  execSync(
    `ffmpeg -y -f concat -safe 0 -i "${concatPath}" -filter:a "atempo=${speed}" "${mergedAudioPath}"`,
    { stdio: 'pipe' }
  );
  
  // 3. 合并视频和音频
  execSync(
    `ffmpeg -y -i "${tempVideoPath}" -i "${mergedAudioPath}" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "${outputPath}"`,
    { stdio: 'pipe' }
  );
  
  // 4. 生成封面
  const posterPath = join(dirname(outputPath), 'poster.jpg');
  execSync(
    `ffmpeg -y -i "${outputPath}" -ss 00:00:02 -vframes 1 -q:v 2 "${posterPath}"`,
    { stdio: 'pipe' }
  );
  
  console.log('✅ 视频合成完成\n');
}

/**
 * 主函数：执行视频录制流程（整合 Codex 方案）
 * @param {string} projectDir - React 项目目录
 * @param {string} outputPath - 输出视频路径
 * @param {Object} options - 录制选项
 */
export async function runVideoRecording(projectDir, outputPath, options = {}) {
  console.log('🚀 开始录制视频（Codex 方案）...\n');
  
  let server = null;
  
  try {
    const { speed = 1.2 } = options;
    
    // 1. 提取配音文本
    const appJsxPath = join(projectDir, 'src/App.jsx');
    const texts = extractVoiceoverTexts(appJsxPath);
    
    // 2. 生成配音
    const audioDir = join(projectDir, 'output/audio');
    const audioPaths = await generateVoiceover(texts, audioDir);
    
    // 3. 启动开发服务器
    const port = 4173;
    const serverInfo = await startDevServer(projectDir, port);
    server = serverInfo.child;
    
    await wait(2000); // 等待服务器就绪
    
    // 4. 录制视频
    const videoDir = join(projectDir, 'output/video');
    const webmPath = await recordWithPlaywright(
      serverInfo.url,
      audioPaths,
      videoDir,
      options
    );
    
    // 5. 转码并合成
    await transcodeAndMerge(webmPath, audioPaths, outputPath, { speed });
    
    console.log(`✅ 视频已生成: ${outputPath}`);
    console.log(`📐 分辨率: ${config.video.width}x${config.video.height}`);
    console.log(`⚡ 速度: ${speed}x\n`);
    
    return {
      success: true,
      videoPath: outputPath,
      posterPath: join(dirname(outputPath), 'poster.jpg')
    };
    
  } catch (error) {
    console.error('❌ 视频录制失败:', error);
    return {
      success: false,
      error: error.message
    };
  } finally {
    if (server) {
      server.kill('SIGTERM');
    }
  }
}
