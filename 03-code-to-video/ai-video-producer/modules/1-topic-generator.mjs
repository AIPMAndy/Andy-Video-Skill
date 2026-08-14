import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载配置
const config = JSON.parse(
  readFileSync(join(__dirname, '../config.json'), 'utf-8')
);

/**
 * 从 GitHub Trending 爬取项目
 * @param {string[]} languages - 编程语言列表
 * @param {string} timeRange - 时间范围 (daily/weekly/monthly)
 * @returns {Promise<Array>} 项目列表
 */
export async function fetchTrending(languages, timeRange = 'monthly') {
  console.log(`📡 正在爬取 GitHub Trending (${timeRange})...`);
  
  // TODO: 使用 OpenClaw browser 工具爬取
  // 这里需要调用 OpenClaw 的 browser 工具
  // 暂时返回模拟数据
  
  return [];
}

/**
 * 筛选符合条件的项目
 * @param {Array} projects - 项目列表
 * @param {number} minStars - 最小星数
 * @returns {Array} 筛选后的项目
 */
export function filterProjects(projects, minStars) {
  console.log(`🔍 筛选项目（最小星数: ${minStars}）...`);
  
  return projects.filter(project => {
    // 筛选条件：
    // 1. 星数大于最小值
    // 2. 有实用价值
    // 3. 项目活跃
    return project.stars >= minStars;
  });
}

/**
 * 为项目生成选题内容
 * @param {Object} project - 项目信息
 * @returns {Object} 选题内容
 */
export function generateTopicContent(project) {
  // TODO: 这里可以调用 LLM 生成更好的标题和钩子文案
  
  return {
    name: project.name,
    stars: project.stars,
    title: `每天半小时AI知识｜${project.name}`,
    hook: `${project.description}`,
    description: project.description,
    useCase: '待补充',
    coreValue: '待补充'
  };
}

/**
 * 生成选题文档（Markdown 格式）
 * @param {Array} projects - 项目列表
 * @returns {string} Markdown 文档
 */
export function generateTopicDoc(projects) {
  console.log(`📝 生成选题文档...`);
  
  const date = new Date().toISOString().split('T')[0];
  let markdown = `# AI知识视频选题 - ${date}\n\n`;
  markdown += `> 从 GitHub Trending 自动生成的选题\n\n`;
  markdown += `---\n\n`;
  
  projects.forEach((project, index) => {
    const topic = generateTopicContent(project);
    markdown += `## 选题${index + 1}：${topic.name}\n\n`;
    markdown += `- **GitHub星数**：${topic.stars.toLocaleString()}\n`;
    markdown += `- **标题**：${topic.title}\n`;
    markdown += `- **钩子文案**：${topic.hook}\n`;
    markdown += `- **使用场景**：${topic.useCase}\n`;
    markdown += `- **核心价值**：${topic.coreValue}\n\n`;
    markdown += `---\n\n`;
  });
  
  return markdown;
}

/**
 * 保存选题文档到飞书
 * @param {string} markdown - Markdown 文档
 * @param {string} folder - 目标文件夹
 * @returns {Promise<Object>} 飞书文档信息
 */
export async function saveToFeishu(markdown, folder) {
  console.log(`💾 保存到飞书知识库: ${folder}...`);
  
  // TODO: 调用 OpenClaw 的 feishu_create_doc 工具
  // 暂时返回模拟数据
  
  return {
    doc_id: 'mock_doc_id',
    doc_url: 'https://feishu.cn/docx/mock_doc_id'
  };
}

/**
 * 主函数：执行选题生成流程
 */
export async function runTopicGeneration() {
  console.log('🚀 开始生成选题...\n');
  
  try {
    // 1. 爬取 GitHub Trending
    const projects = await fetchTrending(
      config.github.languages,
      config.github.timeRange
    );
    
    // 2. 筛选项目
    const filtered = filterProjects(projects, config.github.minStars);
    console.log(`✅ 筛选出 ${filtered.length} 个项目\n`);
    
    // 3. 生成选题文档
    const markdown = generateTopicDoc(filtered);
    
    // 4. 保存到飞书
    const result = await saveToFeishu(
      markdown,
      config.output.topicDocFolder
    );
    
    console.log(`\n✅ 选题文档已生成: ${result.doc_url}\n`);
    
    return {
      success: true,
      projects: filtered,
      markdown,
      docUrl: result.doc_url
    };
  } catch (error) {
    console.error('❌ 选题生成失败:', error);
    return {
      success: false,
      error: error.message
    };
  }
}
