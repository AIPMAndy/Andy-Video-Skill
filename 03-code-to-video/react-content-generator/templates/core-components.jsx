// ============================================
// 核心组件库 - 从样例代码中提炼
// ============================================

import React from 'react';

// --- 1. Apple Style Glass Card ---
// 支持主题切换：light(默认), dark
export const GlassCard = ({ children, className = "", onClick, active = false, style={}, theme = 'light' }) => {
  const themeStyles = {
    light: {
      bg: 'bg-white/70',
      border: 'border-white/80',
      shadow: 'shadow-[0_10px_40px_rgba(0,0,0,0.04)]',
      shadowHover: 'hover:shadow-[0_20px_50px_rgba(79,70,229,0.08)]',
      activeRing: 'ring-indigo-500/30',
      gradient: 'from-indigo-50/50',
    },
    dark: {
      bg: 'bg-slate-900/80',
      border: 'border-slate-700/50',
      shadow: 'shadow-[0_10px_40px_rgba(0,0,0,0.3)]',
      shadowHover: 'hover:shadow-[0_20px_50px_rgba(0,0,0,0.5)]',
      activeRing: 'ring-blue-500/30',
      gradient: 'from-slate-800/50',
    },
  };

  const t = themeStyles[theme] || themeStyles.light;

  return (
    <div
      onClick={onClick}
      style={style}
      className={`
        relative overflow-hidden rounded-[2.5rem] ${t.bg} backdrop-blur-3xl
        border ${t.border}
        ${t.shadow}
        transition-[transform,box-shadow,opacity] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]
        ${active ? `scale-95 shadow-[inset_0_2px_10px_rgba(0,0,0,0.03)] ring-2 ${t.activeRing}` : `hover:-translate-y-1 ${t.shadowHover}`}
        ${className}
      `}
    >
      <div className="relative h-full z-10">{children}</div>
      <div className={`absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-white/90 to-transparent pointer-events-none opacity-90`}></div>
      <div className={`absolute bottom-0 right-0 w-2/3 h-2/3 bg-gradient-to-t ${t.gradient} to-transparent pointer-events-none rounded-[2.5rem]`}></div>
    </div>
  );
};

// --- 2. Script Footer (配音提词器) ---
// 支持三种主题风格：light(默认), dark, glass
export const ScriptFooter = ({ text, theme = 'light' }) => {
  const themeStyles = {
    light: {
      bg: 'bg-white/85',
      border: 'border-white/60',
      text: 'text-slate-800',
      rounded: 'rounded-2xl',
      shadow: 'shadow-[0_15px_40px_rgba(0,0,0,0.1)]',
    },
    dark: {
      bg: 'bg-slate-900/80',
      border: 'border-slate-700/50',
      text: 'text-slate-200',
      rounded: 'rounded-3xl',
      shadow: 'shadow-[0_20px_60px_rgba(0,0,0,0.4)]',
    },
    glass: {
      bg: 'bg-white/80',
      border: 'border-white/50',
      text: 'text-slate-800',
      rounded: 'rounded-full',
      shadow: 'shadow-[0_10px_40px_rgba(0,0,0,0.08)]',
    },
  };

  const style = themeStyles[theme] || themeStyles.light;

  return (
    <div className="absolute bottom-8 left-0 w-full flex justify-center z-50 pointer-events-none px-4">
      <div className={`${style.bg} backdrop-blur-2xl border ${style.border} px-6 py-4 md:px-8 md:py-5 ${style.rounded} ${style.shadow} max-w-4xl text-center w-full md:w-auto animate-slideInUp`}>
        <div className={`${style.text} text-sm md:text-base font-bold leading-relaxed text-center`}>
          {text}
        </div>
      </div>
    </div>
  );
};

// --- 3. Progress Bar (进度条) ---
export const ProgressBar = ({ current, total }) => (
  <div className="absolute top-6 left-6 right-6 md:top-8 md:left-1/2 md:-translate-x-1/2 md:w-64 h-1.5 bg-slate-200 rounded-full overflow-hidden z-50">
    <div 
      className="h-full bg-gradient-to-r from-indigo-400 via-purple-400 to-blue-400 rounded-full transition-all duration-500 ease-out"
      style={{ width: `${(current / total) * 100}%` }}
    />
  </div>
);

// --- 4. Badge (徽章/标签) ---
export const Badge = ({ children, variant = "default", className = "" }) => {
  const variants = {
    default: "bg-slate-100 text-slate-700 border-slate-200",
    success: "bg-emerald-50 text-emerald-600 border-emerald-100",
    warning: "bg-amber-50 text-amber-600 border-amber-100",
    error: "bg-red-50 text-red-600 border-red-100",
    info: "bg-blue-50 text-blue-600 border-blue-100",
    primary: "bg-indigo-50 text-indigo-600 border-indigo-100"
  };

  return (
    <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold border ${variants[variant]} ${className}`}>
      {children}
    </div>
  );
};

// --- 5. Stat Card (数据卡片) ---
export const StatCard = ({ value, label, icon: Icon, trend, className = "" }) => (
  <GlassCard className={`p-6 ${className}`}>
    <div className="flex items-start justify-between mb-2">
      {Icon && <Icon size={24} className="text-indigo-500" />}
      {trend && (
        <span className={`text-xs font-bold ${trend > 0 ? 'text-emerald-500' : 'text-red-500'}`}>
          {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}%
        </span>
      )}
    </div>
    <div className="text-3xl font-black text-slate-900 mb-1">{value}</div>
    <div className="text-sm text-slate-500 font-medium">{label}</div>
  </GlassCard>
);

// --- 6. Feature Card (功能卡片) ---
export const FeatureCard = ({ icon: Icon, title, description, className = "" }) => (
  <GlassCard className={`p-6 ${className}`}>
    <div className="flex flex-col items-center text-center gap-3">
      {Icon && (
        <div className="w-12 h-12 rounded-2xl bg-indigo-100 flex items-center justify-center">
          <Icon size={24} className="text-indigo-600" />
        </div>
      )}
      <h3 className="text-lg font-bold text-slate-900">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{description}</p>
    </div>
  </GlassCard>
);

// --- 7. Timeline Item (时间线项) ---
export const TimelineItem = ({ step, title, description, active = false, completed = false }) => (
  <div className="flex gap-4 items-start">
    <div className={`
      w-10 h-10 rounded-full flex items-center justify-center font-bold text-sm
      transition-all duration-300
      ${completed ? 'bg-emerald-500 text-white' : active ? 'bg-indigo-500 text-white' : 'bg-slate-200 text-slate-500'}
    `}>
      {completed ? '✓' : step}
    </div>
    <div className="flex-1">
      <h4 className={`font-bold mb-1 ${active ? 'text-indigo-600' : 'text-slate-700'}`}>{title}</h4>
      <p className="text-sm text-slate-500">{description}</p>
    </div>
  </div>
);

// --- 8. Comparison Card (对比卡片) ---
export const ComparisonCard = ({ before, after, className = "" }) => (
  <div className={`grid grid-cols-2 gap-4 ${className}`}>
    <GlassCard className="p-6 opacity-60">
      <div className="text-xs font-bold text-red-500 mb-3">传统方式</div>
      <div className="space-y-2">
        {before.map((item, i) => (
          <div key={i} className="flex items-start gap-2 text-sm text-slate-600">
            <span className="text-red-400">✗</span>
            <span>{item}</span>
          </div>
        ))}
      </div>
    </GlassCard>
    <GlassCard className="p-6">
      <div className="text-xs font-bold text-emerald-500 mb-3">AI 方案</div>
      <div className="space-y-2">
        {after.map((item, i) => (
          <div key={i} className="flex items-start gap-2 text-sm text-slate-700">
            <span className="text-emerald-500">✓</span>
            <span>{item}</span>
          </div>
        ))}
      </div>
    </GlassCard>
  </div>
);

// --- 9. Animated Counter (动画计数器) ---
export const AnimatedCounter = ({ value, duration = 2000, suffix = "" }) => {
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    let start = 0;
    const end = parseInt(value);
    const increment = end / (duration / 16);
    
    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setCount(end);
        clearInterval(timer);
      } else {
        setCount(Math.floor(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [value, duration]);

  return <span>{count.toLocaleString()}{suffix}</span>;
};

// --- 10. Pulse Dot (脉冲点) ---
export const PulseDot = ({ color = "indigo", size = "md" }) => {
  const sizes = {
    sm: "w-2 h-2",
    md: "w-3 h-3",
    lg: "w-4 h-4"
  };

  return (
    <div className="relative inline-flex">
      <div className={`${sizes[size]} bg-${color}-500 rounded-full`}></div>
      <div className={`absolute inset-0 ${sizes[size]} bg-${color}-400 rounded-full animate-ping opacity-75`}></div>
    </div>
  );
};
