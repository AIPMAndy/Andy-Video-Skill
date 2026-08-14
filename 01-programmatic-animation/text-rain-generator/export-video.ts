#!/usr/bin/env node
/**
 * 视频导出工具 - 逐帧渲染文字雨动画
 * 需要安装: npm install canvas @types/canvas
 */

import * as fs from 'fs';
import * as path from 'path';
import { createCanvas, loadImage, registerFont } from 'canvas';

interface ExportConfig {
  projectDir: string;
  outputDir: string;
  duration: number; // 秒
  fps: number;
  format: 'png' | 'jpg';
  quality: number; // 0-100 (仅对 jpg 有效)
}

const DEFAULT_CONFIG: ExportConfig = {
  projectDir: './text-rain-output',
  outputDir: './frames',
  duration: 10,
  fps: 30,
  format: 'png',
  quality: 90,
};

/**
 * 简化的粒子类（从 sketch.js 移植）
 */
class RainDrop {
  char: string;
  x: number;
  y: number;
  speed: number;
  rotation: number;
  rotationSpeed: number;
  wobblePhase: number;
  wobbleSpeed: number;
  wobbleAmplitude: number;
  alpha: number;
  scale: number;
  hasCollided: boolean;
  baseSpeed: number;

  constructor(char: string, width: number, height: number, config: any, initialSpread: boolean = false) {
    this.char = char;
    this.reset(width, height, config, initialSpread);
  }

  reset(width: number, height: number, config: any, initialSpread: boolean = false) {
    // 高斯分布横向位置
    const gaussian = () => {
      let u = 0, v = 0;
      while (u === 0) u = Math.random();
      while (v === 0) v = Math.random();
      return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
    };

    this.x = Math.max(
      width * 0.05,
      Math.min(width / 2 + gaussian() * width * 0.25, width * 0.95)
    );

    // 初始化时分散在整个屏幕，重置时在顶部
    if (initialSpread) {
      this.y = Math.random() * height;
    } else {
      this.y = Math.random() * -height;
    }

    this.baseSpeed = config.speed * (0.7 + Math.random() * 0.6);
    this.speed = this.baseSpeed;
    this.rotation = (Math.random() - 0.5) * config.tilt * 2;
    this.rotationSpeed = (Math.random() - 0.5) * 0.4;
    this.wobblePhase = Math.random() * Math.PI * 2;
    this.wobbleSpeed = 0.02 + Math.random() * 0.03;
    this.wobbleAmplitude = 0.3 + Math.random() * 0.5;
    this.alpha = 180 + Math.random() * 75;
    this.scale = 0.85 + Math.random() * 0.3;
    this.hasCollided = false;
  }

  update(width: number, height: number, config: any) {
    this.y += this.speed;
    this.wobblePhase += this.wobbleSpeed;
    this.x += Math.sin(this.wobblePhase) * this.wobbleAmplitude;
    this.rotation += this.rotationSpeed;

    // 轻微加速
    if (this.speed < config.speed * 2) {
      this.speed += 0.05;
    }

    // 循环
    if (this.y > height + 50) {
      this.reset(width, height, config);
    }
  }

  draw(ctx: any, config: any) {
    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.rotate((this.rotation * Math.PI) / 180);
    ctx.scale(this.scale, this.scale);

    // 解析颜色
    const hexToRgb = (hex: string) => {
      const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
      return result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
          }
        : { r: 212, g: 197, b: 169 };
    };

    const rgb = hexToRgb(config.color);
    ctx.fillStyle = `rgba(${rgb.r}, ${rgb.g}, ${rgb.b}, ${this.alpha / 255})`;
    ctx.font = `${config.fontSize}px "STKaiti", "KaiTi", serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(this.char, 0, 0);

    ctx.restore();
  }
}

/**
 * 渲染单帧
 */
async function renderFrame(
  frameNumber: number,
  particles: RainDrop[],
  backgroundImage: any,
  config: any,
  canvasConfig: any
): Promise<Buffer> {
  const canvas = createCanvas(canvasConfig.canvasWidth, canvasConfig.canvasHeight);
  const ctx = canvas.getContext('2d');

  // 绘制背景
  ctx.drawImage(backgroundImage, 0, 0, canvasConfig.canvasWidth, canvasConfig.canvasHeight);

  // 更新和绘制粒子
  particles.forEach(p => {
    p.update(canvasConfig.canvasWidth, canvasConfig.canvasHeight, config);
    p.draw(ctx, config);
  });

  // 导出
  if (canvasConfig.format === 'jpg') {
    return canvas.toBuffer('image/jpeg', { quality: canvasConfig.quality / 100 });
  } else {
    return canvas.toBuffer('image/png');
  }
}

/**
 * 主函数
 */
async function exportVideo(config: ExportConfig) {
  console.log('🎬 开始导出视频帧...\n');

  // 读取项目配置
  const sketchPath = path.join(config.projectDir, 'sketch.js');
  if (!fs.existsSync(sketchPath)) {
    throw new Error(`未找到项目文件: ${sketchPath}`);
  }

  const sketchCode = fs.readFileSync(sketchPath, 'utf-8');

  // 解析配置（简单正则提取）
  const extractConfig = (code: string) => {
    const speedMatch = code.match(/speed:\s*([\d.]+)/);
    const tiltMatch = code.match(/tilt:\s*([\d.]+)/);
    const colorMatch = code.match(/color:\s*'([^']+)'/);
    const fontSizeMatch = code.match(/fontSize:\s*([\d.]+)/);
    const widthMatch = code.match(/canvasWidth:\s*([\d.]+)/);
    const heightMatch = code.match(/canvasHeight:\s*([\d.]+)/);
    const textMatch = code.match(/poemText:\s*`([^`]+)`/);

    return {
      speed: speedMatch ? parseFloat(speedMatch[1]) : 2.5,
      tilt: tiltMatch ? parseFloat(tiltMatch[1]) : 10,
      color: colorMatch ? colorMatch[1] : '#d4c5a9',
      fontSize: fontSizeMatch ? parseInt(fontSizeMatch[1]) : 24,
      canvasWidth: widthMatch ? parseInt(widthMatch[1]) : 1080,
      canvasHeight: heightMatch ? parseInt(heightMatch[1]) : 1920,
      poemText: textMatch ? textMatch[1] : '床前明月光，疑是地上霜',
    };
  };

  const projectConfig = extractConfig(sketchCode);
  console.log('📋 项目配置:', projectConfig);

  // 加载背景图
  const backgroundPath = path.join(config.projectDir, 'assets/background.png');
  if (!fs.existsSync(backgroundPath)) {
    throw new Error(`未找到背景图: ${backgroundPath}`);
  }
  const backgroundImage = await loadImage(backgroundPath);
  console.log('✅ 背景图已加载\n');

  // 初始化粒子
  const poem = projectConfig.poemText.split('').filter(c => c.trim());
  const particleCount = Math.max(poem.length * 3, 50);
  const particles: RainDrop[] = [];

  for (let i = 0; i < particleCount; i++) {
    const char = poem[Math.floor(Math.random() * poem.length)];
    particles.push(
      new RainDrop(char, projectConfig.canvasWidth, projectConfig.canvasHeight, projectConfig, true)
    );
  }

  console.log(`🌧️  已初始化 ${particles.length} 个粒子\n`);

  // 创建输出目录
  fs.mkdirSync(config.outputDir, { recursive: true });

  // 渲染帧
  const totalFrames = config.duration * config.fps;
  console.log(`🎞️  开始渲染 ${totalFrames} 帧 (${config.duration}秒 @ ${config.fps}fps)\n`);

  for (let frame = 0; frame < totalFrames; frame++) {
    const buffer = await renderFrame(frame, particles, backgroundImage, projectConfig, {
      canvasWidth: projectConfig.canvasWidth,
      canvasHeight: projectConfig.canvasHeight,
      format: config.format,
      quality: config.quality,
    });

    const frameFile = path.join(
      config.outputDir,
      `frame_${frame.toString().padStart(5, '0')}.${config.format}`
    );
    fs.writeFileSync(frameFile, buffer);

    // 进度显示
    if ((frame + 1) % 30 === 0 || frame === totalFrames - 1) {
      const progress = ((frame + 1) / totalFrames) * 100;
      console.log(`   进度: ${progress.toFixed(1)}% (${frame + 1}/${totalFrames})`);
    }
  }

  console.log(`\n✅ 帧序列已导出到: ${config.outputDir}`);
  console.log('\n📹 使用 FFmpeg 合成视频:');
  console.log(
    `   ffmpeg -framerate ${config.fps} -i ${config.outputDir}/frame_%05d.${config.format} -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p output.mp4\n`
  );
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const config = { ...DEFAULT_CONFIG };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];

      switch (key) {
        case 'input':
        case 'project':
          config.projectDir = value;
          i++;
          break;
        case 'output':
          config.outputDir = value;
          i++;
          break;
        case 'duration':
          config.duration = parseInt(value);
          i++;
          break;
        case 'fps':
          config.fps = parseInt(value);
          i++;
          break;
        case 'format':
          config.format = value as 'png' | 'jpg';
          i++;
          break;
        case 'quality':
          config.quality = parseInt(value);
          i++;
          break;
      }
    }
  }

  exportVideo(config).catch(error => {
    console.error('❌ 导出失败:', error.message);
    process.exit(1);
  });
}

export { exportVideo, ExportConfig };
