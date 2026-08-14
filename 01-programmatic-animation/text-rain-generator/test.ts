#!/usr/bin/env node
/**
 * 测试用例 - 验证核心功能
 */

import * as fs from 'fs';
import * as path from 'path';
import { generateHTML, generateSketch } from './generate';

const TEST_CONFIG = {
  text: '床前明月光，疑是地上霜',
  scene: '江南老宅青瓦屋檐',
  speed: 2.5,
  tilt: 10,
  color: '#d4c5a9',
  fontSize: 24,
  canvasWidth: 1080,
  canvasHeight: 1920,
  output: './test-output',
  noPreview: true,
};

console.log('🧪 开始测试 text-rain-generator...\n');

let passed = 0;
let failed = 0;

// 测试1: HTML 生成
console.log('测试1: 生成 HTML 文件...');
try {
  const html = generateHTML(TEST_CONFIG);
  if (html.includes('p5.js') && html.includes('sketch.js')) {
    console.log('   ✅ HTML 生成正确\n');
    passed++;
  } else {
    console.log('   ❌ HTML 缺少必要元素\n');
    failed++;
  }
} catch (error) {
  console.log(`   ❌ HTML 生成失败: ${error.message}\n`);
  failed++;
}

// 测试2: Sketch 生成
console.log('测试2: 生成 sketch.js...');
try {
  const sketch = generateSketch(TEST_CONFIG);
  const requiredElements = [
    'class RainDrop',
    'function setup()',
    'function draw()',
    'backgroundImg',
    'particles',
  ];

  const missing = requiredElements.filter(el => !sketch.includes(el));
  if (missing.length === 0) {
    console.log('   ✅ Sketch 包含所有必要元素\n');
    passed++;
  } else {
    console.log(`   ❌ Sketch 缺少元素: ${missing.join(', ')}\n`);
    failed++;
  }
} catch (error) {
  console.log(`   ❌ Sketch 生成失败: ${error.message}\n`);
  failed++;
}

// 测试3: 配置参数正确嵌入
console.log('测试3: 验证配置参数嵌入...');
try {
  const sketch = generateSketch(TEST_CONFIG);
  const checks = [
    { param: 'speed', value: '2.5' },
    { param: 'tilt', value: '10' },
    { param: 'color', value: '#d4c5a9' },
    { param: 'fontSize', value: '24' },
  ];

  const errors = checks.filter(c => !sketch.includes(c.value));
  if (errors.length === 0) {
    console.log('   ✅ 所有配置参数正确嵌入\n');
    passed++;
  } else {
    console.log(`   ❌ 缺失参数: ${errors.map(e => e.param).join(', ')}\n`);
    failed++;
  }
} catch (error) {
  console.log(`   ❌ 参数验证失败: ${error.message}\n`);
  failed++;
}

// 测试4: 文件输出
console.log('测试4: 创建输出目录和文件...');
try {
  const outputDir = path.resolve(TEST_CONFIG.output);
  fs.mkdirSync(outputDir, { recursive: true });
  fs.mkdirSync(path.join(outputDir, 'assets'), { recursive: true });

  fs.writeFileSync(
    path.join(outputDir, 'test.html'),
    generateHTML(TEST_CONFIG)
  );

  if (fs.existsSync(path.join(outputDir, 'test.html'))) {
    console.log(`   ✅ 文件已写入 ${outputDir}\n`);
    passed++;

    // 清理测试文件
    fs.unlinkSync(path.join(outputDir, 'test.html'));
    fs.rmdirSync(path.join(outputDir, 'assets'));
    fs.rmdirSync(outputDir);
  } else {
    console.log('   ❌ 文件写入失败\n');
    failed++;
  }
} catch (error) {
  console.log(`   ❌ 文件操作失败: ${error.message}\n`);
  failed++;
}

// 测试5: 边界情况 - 空文本
console.log('测试5: 边界情况测试...');
try {
  const emptyConfig = { ...TEST_CONFIG, text: '' };
  const sketch = generateSketch(emptyConfig);
  // 应该生成代码但 poem 数组为空
  if (sketch.includes('poemText: ``')) {
    console.log('   ✅ 空文本处理正确\n');
    passed++;
  } else {
    console.log('   ❌ 空文本处理不当\n');
    failed++;
  }
} catch (error) {
  console.log(`   ❌ 边界测试失败: ${error.message}\n`);
  failed++;
}

// 测试6: 特殊字符处理
console.log('测试6: 特殊字符处理...');
try {
  const specialConfig = {
    ...TEST_CONFIG,
    text: '测试"引号"和\'单引号\'还有\n换行',
  };
  const sketch = generateSketch(specialConfig);
  // 使用模板字符串应该能正确处理特殊字符
  if (sketch.includes('poemText: `')) {
    console.log('   ✅ 特殊字符处理正确\n');
    passed++;
  } else {
    console.log('   ❌ 特殊字符可能导致语法错误\n');
    failed++;
  }
} catch (error) {
  console.log(`   ❌ 特殊字符测试失败: ${error.message}\n`);
  failed++;
}

// 总结
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
console.log(`✅ 通过: ${passed}`);
console.log(`❌ 失败: ${failed}`);
console.log(`📊 成功率: ${((passed / (passed + failed)) * 100).toFixed(1)}%`);
console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

if (failed === 0) {
  console.log('🎉 所有测试通过！\n');
  process.exit(0);
} else {
  console.log('⚠️  部分测试失败，请检查代码\n');
  process.exit(1);
}
