#!/usr/bin/env node

/**
 * Interactive Knowledge Video Config Generator
 *
 * This script helps you create a configuration file for knowledge videos
 * through an interactive CLI interface.
 */

import readline from 'readline';
import fs from 'fs';
import path from 'path';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, resolve);
  });
}

const THEME_COLORS = ['indigo', 'orange', 'blue', 'emerald', 'purple', 'red'];
const ICONS = ['star', 'globe', 'users', 'bot', 'flame', 'code', 'search', 'shield', 'layers', 'database', 'sparkles', 'network', 'terminal', 'message', 'brain', 'alert'];

async function main() {
  console.log('\n🎬 Knowledge Video Config Generator\n');
  console.log('This tool will help you create a configuration file for your knowledge video.\n');

  const config = {
    themeColor: 'indigo',
    project: {},
    steps: []
  };

  // Project Info
  console.log('📋 Project Information\n');
  config.project.name = await question('Project name: ');
  config.project.stars = await question('GitHub stars (e.g., 162k+): ');
  config.project.courseNumber = await question('Course number (e.g., 第 340 课): ');
  config.project.category = await question('Category (e.g., AI 基础设施): ');

  // Theme Color
  console.log('\n🎨 Theme Color\n');
  console.log('Available colors:', THEME_COLORS.join(', '));
  const themeColor = await question(`Choose theme color [${THEME_COLORS[0]}]: `);
  config.themeColor = themeColor || THEME_COLORS[0];

  // Cover Step
  console.log('\n📄 Cover Page\n');
  const cover = {
    type: 'cover',
    icon: await question('Icon name (e.g., message): ') || 'message',
    badge: await question('Badge text (e.g., 162k+ Stars): '),
    title: config.project.name,
    subtitle: await question('Subtitle: '),
    courseNumber: config.project.courseNumber,
    category: config.project.category,
    script: await question('Opening script/narration: ')
  };
  config.steps.push(cover);

  // Pain Points
  console.log('\n❌ Pain Points\n');
  const numPainPoints = parseInt(await question('How many pain point steps? [1]: ') || '1');

  for (let i = 0; i < numPainPoints; i++) {
    console.log(`\nPain Point ${i + 1}:`);
    const painPoint = {
      type: 'pain_point',
      icon: await question('Icon: ') || 'alert',
      badge: await question('Badge text: '),
      title: await question('Title: '),
      script: await question('Script: '),
      visualizer: {
        icon: await question('Visualizer icon: ') || 'alert',
        badge: await question('Visualizer badge: '),
        items: []
      }
    };

    const numItems = parseInt(await question('How many problem items? [3]: ') || '3');
    for (let j = 0; j < numItems; j++) {
      console.log(`  Item ${j + 1}:`);
      painPoint.visualizer.items.push({
        icon: await question('    Icon: ') || 'x',
        color: await question('    Color (red/amber/slate): ') || 'red',
        title: await question('    Title: '),
        description: await question('    Description: ')
      });
    }

    config.steps.push(painPoint);
  }

  // Features
  console.log('\n✨ Features\n');
  const numFeatures = parseInt(await question('How many feature steps? [2]: ') || '2');

  for (let i = 0; i < numFeatures; i++) {
    console.log(`\nFeature ${i + 1}:`);
    const feature = {
      type: 'feature',
      icon: await question('Icon: ') || 'sparkles',
      badge: await question('Badge text: '),
      title: await question('Title: '),
      script: await question('Script: '),
      visualizer: {
        steps: []
      }
    };

    const numSteps = parseInt(await question('How many feature steps? [3]: ') || '3');
    for (let j = 0; j < numSteps; j++) {
      console.log(`  Step ${j + 1}:`);
      feature.visualizer.steps.push({
        icon: await question('    Icon: ') || 'check',
        color: await question('    Color (blue/purple/emerald): ') || 'blue',
        title: await question('    Title: '),
        description: await question('    Description: ')
      });
    }

    config.steps.push(feature);
  }

  // Golden Sentence
  console.log('\n💎 Golden Sentence\n');
  const addGolden = await question('Add golden sentence page? [y/n]: ');
  if (addGolden.toLowerCase() === 'y') {
    const golden = {
      type: 'golden_sentence',
      subtitle: await question('Subtitle (e.g., Philosophy): '),
      quote: await question('Quote: '),
      explanation: await question('Explanation: '),
      script: await question('Script: ')
    };
    config.steps.push(golden);
  }

  // Summary
  console.log('\n📝 Summary\n');
  const summary = {
    type: 'summary',
    icon: await question('Icon: ') || 'message',
    title: await question('Title (e.g., 课程总结): ') || '课程总结',
    author: await question('Author name: ') || 'AI酋长Andy',
    footer: await question('Footer text (e.g., org/repo): '),
    script: await question('Closing script: '),
    points: []
  };

  const numPoints = parseInt(await question('How many summary points? [3]: ') || '3');
  for (let i = 0; i < numPoints; i++) {
    console.log(`\nPoint ${i + 1}:`);
    summary.points.push({
      icon: await question('  Icon: ') || 'check',
      color: await question('  Color: ') || config.themeColor,
      title: await question('  Title: '),
      description: await question('  Description: ')
    });
  }

  config.steps.push(summary);

  // Save Config
  console.log('\n💾 Saving Configuration\n');
  const filename = await question('Output filename [knowledge-video-config.json]: ') || 'knowledge-video-config.json';
  const outputPath = path.resolve(filename);

  fs.writeFileSync(outputPath, JSON.stringify(config, null, 2));
  console.log(`\n✅ Configuration saved to: ${outputPath}`);
  console.log('\nNext steps:');
  console.log(`  1. Review and edit: ${filename}`);
  console.log(`  2. Generate video: /react-video --template knowledge --config ${filename}`);
  console.log('\n');

  rl.close();
}

main().catch(console.error);
