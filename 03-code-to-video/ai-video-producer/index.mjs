#!/usr/bin/env node

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import readline from 'readline';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载配置
const config = JSON.parse(
  readFileSync(join(__dirname, 'config.json'), 'utf-8')
);

// 导入模块
import { runTopicGeneration } from './modules/1-topic-generator.mjs';
import { runPPTGeneration } from './modules/2-ppt-generator.mjs';
import { runVideoRecording } from './modules/3-video-recorder.mjs';

/**
 * 等待用户确认
 * @param {string} message - 提示信息
 * @returns {Promise<string>} 用户输入
 */
function askUser(message) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise(resolve => {
    rl.question(message, answer => {
      rl.close();
      resolve(answer.trim().toLowerCase());
    });
  });
}

/**
 * 主流程
 */
async function main() {
  console.log('╔════════════════════════════════════════════════════════════╗');
  console.log('║                                                            ║');
  console.log('║          🎬 AI 知识视频自动化生产系统 v1.0                ║');
  console.log('║                                                            ║');
  console.log('╚════════════════════════════════════════════════════════════╝');
  console.log('');
  
  try {
    // ========== 第1步：生成选题 ==========
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('📋 第1步：生成选题');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    
    const topicResult = await runTopicGeneration();
    
    if (!topicResult.success) {
      console.error('❌ 选题生成失败，流程终止');
      process.exit(1);
    }
    
    console.log('✅ 选题生成完成！');
    console.log(`📄 文档链接: ${topicResult.docUrl}`);
    console.log(`📊 共生成 ${topicResult.projects.length} 个选题`);
    console.log('');
    
    // 如果不是自动确认模式，等待用户确认
    if (!config.autoConfirm) {
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('⏸️  请确认选题');
      console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
      console.log('');
      console.log('选项：');
      console.log('  y - 继续执行');
      console.log('  n - 重新生成选题');
      console.log('  e - 编辑选题后继续');
      console.log('  q - 退出');
      console.log('');
      
      const answer = await askUser('请输入选项 (y/n/e/q): ');
      
      if (answer === 'q') {
        console.log('👋 已退出');
        process.exit(0);
      }
      
      if (answer === 'n') {
        console.log('🔄 重新生成选题...');
        // TODO: 重新生成逻辑
        console.log('⚠️  暂未实现，请手动重新运行');
        process.exit(0);
      }
      
      if (answer === 'e') {
        console.log('✏️  请在飞书文档中编辑选题，完成后按回车继续...');
        await askUser('');
      }
    }
    
    // ========== 第2步：生成 React PPT ==========
    console.log('');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎨 第2步：生成 React PPT');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    
    const projectName = `ai-video-${Date.now()}`;
    const pptResult = await runPPTGeneration(topicResult.projects, projectName);
    
    if (!pptResult.success) {
      console.error('❌ PPT 生成失败，流程终止');
      process.exit(1);
    }
    
    console.log('✅ React PPT 生成完成！');
    console.log(`📁 项目目录: ${pptResult.projectDir}`);
    console.log('');
    
    // ========== 第3步：录制视频 ==========
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎥 第3步：录制视频');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    
    const videoPath = join(config.output.videoDir, `${projectName}.mp4`);
    const videoResult = await runVideoRecording(pptResult.projectDir, videoPath);
    
    if (!videoResult.success) {
      console.error('❌ 视频录制失败，流程终止');
      process.exit(1);
    }
    
    console.log('✅ 视频录制完成！');
    console.log(`🎬 视频路径: ${videoResult.videoPath}`);
    console.log('');
    
    // ========== 完成 ==========
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('🎉 全部完成！');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('');
    console.log('📋 流程摘要：');
    console.log(`  ✅ 选题文档: ${topicResult.docUrl}`);
    console.log(`  ✅ React 项目: ${pptResult.projectDir}`);
    console.log(`  ✅ 视频文件: ${videoResult.videoPath}`);
    console.log('');
    console.log('📌 下一步：');
    console.log('  1. 审核视频质量');
    console.log('  2. 发布到目标平台（抖音、B站、YouTube等）');
    console.log('');
    console.log('👋 感谢使用 AI 视频自动化生产系统！');
    console.log('');
    
  } catch (error) {
    console.error('');
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.error('❌ 发生错误');
    console.error('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.error('');
    console.error(error);
    console.error('');
    process.exit(1);
  }
}

// 运行主流程
main();
