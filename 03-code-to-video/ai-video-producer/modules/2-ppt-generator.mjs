import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载配置
const config = JSON.parse(
  readFileSync(join(__dirname, '../config.json'), 'utf-8')
);

/**
 * 加载 React 项目模板
 * @returns {Object} 模板文件内容
 */
export function loadTemplate() {
  console.log('📦 加载 React 项目模板...');
  
  const templateDir = join(__dirname, '../templates/react-ppt-template');
  
  // 从 Andy 的实际项目中复制模板
  const sourceDir = '/Users/andy/Desktop/公众号发布/.codex-react-video-job';
  
  return {
    packageJson: readFileSync(join(sourceDir, 'package.json'), 'utf-8'),
    viteConfig: readFileSync(join(sourceDir, 'vite.config.js'), 'utf-8'),
    tailwindConfig: readFileSync(join(sourceDir, 'tailwind.config.js'), 'utf-8'),
    postcssConfig: readFileSync(join(sourceDir, 'postcss.config.js'), 'utf-8'),
    indexHtml: readFileSync(join(sourceDir, 'index.html'), 'utf-8'),
    renderScript: readFileSync(join(sourceDir, 'scripts/render-video.mjs'), 'utf-8'),
    mainJsx: readFileSync(join(sourceDir, 'src/main.jsx'), 'utf-8'),
    videoRuntime: readFileSync(join(sourceDir, 'src/video-runtime.js'), 'utf-8'),
    socialVideoLayout: readFileSync(join(sourceDir, 'src/social-video-layout.jsx'), 'utf-8')
  };
}

/**
 * 生成场景组件代码
 * @param {Object} topic - 选题内容
 * @param {number} index - 场景索引
 * @returns {string} React 组件代码
 */
export function generateSceneComponent(topic, index) {
  // 基于选题内容生成场景组件
  // 这里是简化版，实际需要根据内容类型生成不同的场景
  
  return `
const Scene${index} = ({ isActive }) => {
  const [step, setStep] = useState(0);
  
  useEffect(() => {
    if (!isActive) {
      setStep(0);
      return;
    }
    const timer1 = setTimeout(() => setStep(1), 800);
    const timer2 = setTimeout(() => setStep(2), 2200);
    return () => {
      clearTimeout(timer1);
      clearTimeout(timer2);
    };
  }, [isActive]);
  
  return (
    <div className="relative flex h-full w-full flex-col items-center justify-center overflow-hidden bg-slate-50 p-10">
      <div className="mb-6 text-center">
        <h3 className="text-[2.12rem] font-black tracking-[-0.045em] text-slate-800">
          ${topic.title}
        </h3>
      </div>
      
      <div className="relative w-full max-w-[56rem]">
        <div className={\`transition-all duration-500 \${step >= 1 ? 'opacity-100' : 'opacity-0'}\`}>
          <p className="text-[1.3rem] font-medium leading-[1.74] text-slate-600">
            ${topic.hook}
          </p>
        </div>
      </div>
    </div>
  );
};
`;
}

/**
 * 生成主组件代码
 * @param {Array} topics - 选题列表
 * @returns {string} 主组件代码
 */
export function generateMainComponent(topics) {
  console.log('🎨 生成 React 组件代码...');
  
  const sceneDurations = topics.map(() => 10000).join(', ');
  const sceneComponents = topics.map((topic, index) => 
    generateSceneComponent(topic, index)
  ).join('\n\n');
  
  const sceneElements = topics.map((_, index) => `
    <React.Fragment key="scene${index}">
      <Scene${index} isActive={step === ${index}} />
      <ScriptFooter text="场景 ${index + 1} 的文案" />
    </React.Fragment>
  `).join(',\n');
  
  return `
import React, { useEffect, useState } from "react";
import { useAutoplayScenes, ScriptFooter } from "./social-video-layout";

const sceneDurationsMs = [${sceneDurations}];

${sceneComponents}

export default function VideoLesson() {
  const { step, totalSteps } = useAutoplayScenes(sceneDurationsMs, {
    readyDelayMs: 650,
  });

  const pageBaseClass = "col-start-1 row-start-1 flex h-full w-full flex-col items-center justify-center px-6 pb-32 pt-14 transition-all duration-700";

  const getPageStyle = (index) => {
    if (index === step) return "opacity-100 scale-100 z-10";
    if (index < step) return "opacity-0 scale-90 z-0";
    return "opacity-0 scale-110 z-20";
  };

  const scenes = [
    ${sceneElements}
  ];

  return (
    <div className="fixed inset-0 h-full w-full overflow-hidden bg-[#f5f5f7] font-sans text-slate-800">
      <div className="grid h-full w-full grid-cols-1 grid-rows-1">
        {scenes.map((content, index) => (
          <div key={index} className={\`\${pageBaseClass} \${getPageStyle(index)}\`}>
            {content}
          </div>
        ))}
      </div>
    </div>
  );
}
`;
}

/**
 * 写入 React 项目文件
 * @param {Object} template - 模板内容
 * @param {string} appCode - App.jsx 代码
 * @param {string} outputDir - 输出目录
 */
export function writeReactProject(template, appCode, outputDir) {
  console.log(`📁 写入 React 项目到: ${outputDir}...`);
  
  // 创建目录结构
  mkdirSync(join(outputDir, 'src'), { recursive: true });
  mkdirSync(join(outputDir, 'scripts'), { recursive: true });
  
  // 写入文件
  writeFileSync(join(outputDir, 'package.json'), template.packageJson);
  writeFileSync(join(outputDir, 'vite.config.js'), template.viteConfig);
  writeFileSync(join(outputDir, 'tailwind.config.js'), template.tailwindConfig);
  writeFileSync(join(outputDir, 'postcss.config.js'), template.postcssConfig);
  writeFileSync(join(outputDir, 'index.html'), template.indexHtml);
  writeFileSync(join(outputDir, 'scripts/render-video.mjs'), template.renderScript);
  writeFileSync(join(outputDir, 'src/main.jsx'), template.mainJsx);
  writeFileSync(join(outputDir, 'src/video-runtime.js'), template.videoRuntime);
  writeFileSync(join(outputDir, 'src/social-video-layout.jsx'), template.socialVideoLayout);
  writeFileSync(join(outputDir, 'src/App.jsx'), appCode);
  
  console.log('✅ React 项目文件已写入\n');
}

/**
 * 主函数：执行 PPT 生成流程
 * @param {Array} topics - 选题列表
 * @param {string} projectName - 项目名称
 */
export async function runPPTGeneration(topics, projectName) {
  console.log('🚀 开始生成 React PPT...\n');
  
  try {
    // 1. 加载模板
    const template = loadTemplate();
    
    // 2. 生成主组件代码
    const appCode = generateMainComponent(topics);
    
    // 3. 写入项目文件
    const outputDir = join(config.output.reactProjectDir, projectName);
    writeReactProject(template, appCode, outputDir);
    
    console.log(`✅ React PPT 已生成: ${outputDir}\n`);
    
    return {
      success: true,
      projectDir: outputDir
    };
  } catch (error) {
    console.error('❌ PPT 生成失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
