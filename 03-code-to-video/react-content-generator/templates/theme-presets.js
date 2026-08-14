// ============================================
// 主题风格预设 - 基于三个成熟案例提炼
// ============================================

export const THEME_PRESETS = {
  // 暗黑科技风（liteparse风格）- 适合技术产品、开发工具
  'dark-tech': {
    name: '暗黑科技风',
    description: '深空黑背景 + 蓝紫渐变 + 光晕效果',
    colors: {
      primary: '#3b82f6',      // blue-500
      secondary: '#6366f1',    // indigo-500
      accent: '#06b6d4',       // cyan-500
      background: '#020617',   // 深空黑
      cardBg: 'rgba(15, 23, 42, 0.8)',  // slate-900/80
      cardBorder: 'rgba(71, 85, 105, 0.5)', // slate-700/50
      text: '#e2e8f0',         // slate-200
      textSecondary: '#94a3b8', // slate-400
      warning: '#ef4444',      // red-500
      warningBg: 'rgba(239, 68, 68, 0.1)',
      warningBorder: 'rgba(239, 68, 68, 0.2)',
      success: '#10b981',      // emerald-500
    },
    shadows: {
      card: '0_20px_60px_rgba(0,0,0,0.4)',
      cardHover: '0_30px_80px_rgba(0,0,0,0.6)',
      glow: '0_0_15px_rgba(59,130,246,0.8)',
      glowAccent: '0_0_30px_rgba(244,63,94,0.6)',
    },
    scriptFooter: {
      bg: 'bg-slate-900/80',
      border: 'border-slate-700/50',
      text: 'text-slate-200',
      rounded: 'rounded-3xl',
      shadow: 'shadow-[0_20px_60px_rgba(0,0,0,0.4)]',
    },
    glassCard: {
      bg: 'bg-slate-900/80',
      border: 'border-slate-700/50',
      blur: 'backdrop-blur-2xl',
    }
  },

  // 温暖专业风（TensorFlow风格）- 适合企业级解决方案、B端产品
  'warm-professional': {
    name: '温暖专业风',
    description: '浅灰白背景 + 橙黄渐变 + 柔和阴影',
    colors: {
      primary: '#f97316',      // orange-500
      secondary: '#f59e0b',    // amber-500
      accent: '#eab308',       // yellow-500
      background: '#f8fafc',   // slate-50
      cardBg: 'rgba(255, 255, 255, 0.85)',
      cardBorder: 'rgba(255, 255, 255, 0.6)',
      text: '#1e293b',         // slate-800
      textSecondary: '#64748b', // slate-500
      warning: '#dc2626',      // red-600
      warningBg: '#fef2f2',    // red-50
      warningBorder: '#fecaca', // red-200
      success: '#059669',      // emerald-600
    },
    shadows: {
      card: '0_10px_40px_rgba(0,0,0,0.04)',
      cardHover: '0_20px_50px_rgba(0,0,0,0.08)',
      glow: '0_15px_40px_rgba(249,115,22,0.3)',
      glowAccent: '0_0_20px_rgba(245,158,11,0.4)',
    },
    scriptFooter: {
      bg: 'bg-white/85',
      border: 'border-white/60',
      text: 'text-slate-800',
      rounded: 'rounded-2xl',
      shadow: 'shadow-[0_15px_40px_rgba(0,0,0,0.1)]',
    },
    glassCard: {
      bg: 'bg-white/85',
      border: 'border-white/60',
      blur: 'backdrop-blur-2xl',
    }
  },

  // 梦幻渐变风（social-auto-upload风格）- 适合C端产品、社交工具
  'dreamy-gradient': {
    name: '梦幻渐变风',
    description: '粉白基底 + 紫粉渐变 + 光晕效果',
    colors: {
      primary: '#d946ef',      // fuchsia-600
      secondary: '#6366f1',    // indigo-500
      accent: '#3b82f6',       // blue-500
      background: '#fdf2f8',   // 粉白基底
      cardBg: 'rgba(255, 255, 255, 0.7)',
      cardBorder: 'rgba(255, 255, 255, 0.6)',
      text: '#1e293b',         // slate-800
      textSecondary: '#64748b', // slate-500
      warning: '#f43f5e',      // rose-500
      warningBg: '#fef2f2',    // rose-50
      warningBorder: '#fecdd3', // rose-200
      success: '#10b981',      // emerald-500
    },
    shadows: {
      card: '0_10px_40px_rgba(0,0,0,0.04)',
      cardHover: '0_20px_50px_rgba(0,0,0,0.08)',
      glow: '0_0_30px_rgba(217,70,239,0.4)',
      glowAccent: '0_0_20px_rgba(99,102,241,0.3)',
    },
    scriptFooter: {
      bg: 'bg-white/80',
      border: 'border-white/50',
      text: 'text-slate-800',
      rounded: 'rounded-full',
      shadow: 'shadow-[0_10px_40px_rgba(0,0,0,0.08)]',
    },
    glassCard: {
      bg: 'bg-white/70',
      border: 'border-white/60',
      blur: 'backdrop-blur-3xl',
    }
  },
};

// 标准动画时序配置
export const ANIMATION_TIMING = {
  // 初始延迟（首次元素出现）
  initialDelay: {
    min: 800,
    max: 1200,
    default: 1000,
  },
  // 步骤间隔（状态切换）
  stepInterval: {
    min: 1200,
    max: 2000,
    default: 1500,
  },
  // 高潮时刻（最终警示/结论）
  climaxDelay: {
    min: 3500,
    max: 4500,
    default: 4000,
  },
  // 元素渐入时长
  elementDuration: 700,
  // 页面切换时长
  pageTransition: 1000,
};

// 组件命名规范
export const COMPONENT_NAMING = {
  pain: '{核心问题}Pain',           // 痛点组件
  arch: '{技术名}Arch',             // 方案/架构组件
  features: '{技术名}Features',     // 特性展示组件
  golden: 'GoldenSentence',         // 金句组件
  outro: 'AndyIdentity{Outro/CTA}', // 结尾组件
};

// 可视化组件模式
export const VISUALIZER_PATTERNS = {
  // 对比崩溃模式（左右对比 + 中间转折 + overlay警示层）
  'contrast-collapse': {
    description: '展示从正常到崩溃的转变，适合痛点展示',
    structure: 'left(past) → middle(transformation) → right(problem+overlay)',
    timing: 'step 0: 静态 → step 1: 左侧出现 → step 2: 右侧+转折 → step 3: overlay警示',
  },
  // 流程引擎模式（SVG流线 + 中心节点 + 分支输出）
  'flow-engine': {
    description: '展示技术架构和数据流动，适合方案展示',
    structure: 'input → [engine with SVG flow] → multiple outputs',
    timing: 'step 0: 输入 → step 1: 引擎激活 → step 2: SVG流线 → step 3: 输出分支',
  },
  // 漏斗压缩模式
  'funnel-compress': {
    description: '展示从海量到精选的筛选过程',
    structure: 'top(many items) → middle(funnel) → bottom(few winners)',
    timing: 'step 0: 顶部海量 → step 1: 漏斗压缩 → step 2: 底部精选',
  },
  // 雷达扫描模式
  'radar-scan': {
    description: '展示全平台监控/实时追踪',
    structure: 'center(radar) + surrounding(platforms)',
    timing: 'continuous: 雷达旋转 + platforms逐个点亮',
  },
};

// 圆角规范
export const BORDER_RADIUS = {
  sm: 'rounded-lg',           // 8px - 小元素
  md: 'rounded-xl',           // 12px - 按钮/badge
  lg: 'rounded-2xl',          // 16px - 小卡片
  xl: 'rounded-[2.5rem]',     // 40px - 大卡片（推荐）
  '2xl': 'rounded-3xl',       // 24px - 容器
  '3xl': 'rounded-[3rem]',    // 48px - 超大容器
  full: 'rounded-full',       // 圆形 - 按钮/badge
};

// 响应式断点
export const BREAKPOINTS = {
  sm: '640px',   // 手机横屏
  md: '768px',   // 平板
  lg: '1024px',  // 笔记本
  xl: '1280px',  // 桌面
};

// 图标尺寸规范
export const ICON_SIZES = {
  xs: 12,  // 标签、徽章
  sm: 16,  // 按钮、列表项
  md: 24,  // 卡片标题
  lg: 32,  // 页面副标题
  xl: 48,  // 页面主视觉
  '2xl': 64, // 超大主视觉
};
