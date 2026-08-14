// ============================================
// 可视化组件库 - 从样例代码中提炼
// ============================================

import React, { useState, useEffect } from 'react';
import { 
  Search, 
  Bot, 
  User, 
  ArrowRight, 
  TrendingDown,
  Sparkles,
  Crown,
  Brain
} from 'lucide-react';

// --- 1. 搜索迁徙可视化 (Search Shift Visualizer) ---
// 展示用户从传统搜索引擎迁移到 AI 搜索的过程
export const SearchShiftVisualizer = ({ isActive }) => {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    if (!isActive) { setPhase(0); return; }
    const interval = setInterval(() => {
      setPhase(p => (p < 3 ? p + 1 : 3));
    }, 2500);
    return () => clearInterval(interval);
  }, [isActive]);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center gap-6 p-6 relative bg-[#f8fafc] overflow-hidden">
      
      {/* 警告标签 */}
      <div className={`absolute top-6 flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-full text-[10px] font-bold border border-red-100 transition-opacity duration-500 ${phase >= 1 ? 'opacity-100 scale-100' : 'opacity-0 scale-90'}`}>
        <TrendingDown size={14} className="animate-pulse"/> 百度/谷歌首页排名流量骤减
      </div>

      <div className="flex flex-col items-center mt-4 w-full max-w-2xl relative h-64 justify-center">
        
        {/* 传统搜索引擎 */}
        <div className={`absolute w-80 bg-white border border-slate-200 rounded-2xl shadow-md p-4 transition-all duration-1000 ${phase === 0 ? 'opacity-100 scale-100 translate-y-0' : 'opacity-20 scale-90 -translate-y-10 blur-sm'}`}>
          <div className="flex items-center gap-2 mb-4">
            <Search size={16} className="text-blue-500"/>
            <div className="h-2 w-32 bg-slate-100 rounded"></div>
          </div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="flex flex-col gap-1">
                <div className="h-3 w-48 bg-blue-100 rounded"></div>
                <div className="h-1.5 w-64 bg-slate-100 rounded"></div>
              </div>
            ))}
          </div>
        </div>

        {/* 转移箭头 */}
        <div className={`absolute z-20 flex items-center justify-center bg-white/80 backdrop-blur px-4 py-2 rounded-full border border-slate-200 shadow-xl transition-all duration-700 ${phase >= 1 && phase < 3 ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`}>
          <span className="text-xs font-black text-slate-700 mr-2">用户习惯彻底转移</span>
          <ArrowRight size={16} className="text-indigo-500 animate-pulse"/>
        </div>

        {/* AI 搜索界面 */}
        <div className={`absolute w-80 bg-slate-900 border border-slate-700 rounded-3xl shadow-2xl p-4 transition-all duration-1000 ${phase >= 2 ? 'opacity-100 scale-100 translate-y-0' : 'opacity-0 scale-90 translate-y-10'}`}>
          <div className="flex items-center gap-2 mb-4 border-b border-slate-800 pb-3">
            <Sparkles size={16} className="text-indigo-400"/>
            <span className="text-white font-bold text-xs">ChatGPT / Gemini / Perplexity</span>
          </div>
          <div className="bg-slate-800 rounded-xl p-3 text-slate-300 text-[10px] leading-relaxed relative">
            <div className="flex items-start gap-2 mb-2">
              <User size={12} className="text-slate-500 mt-0.5"/>
              <span>"帮我推荐几款最好的产品..."</span>
            </div>
            <div className={`flex items-start gap-2 transition-all duration-700 delay-500 ${phase >= 3 ? 'opacity-100' : 'opacity-0'}`}>
              <Bot size={14} className="text-emerald-400 mt-0.5"/>
              <span>
                根据全网数据，我为您推荐以下 <span className="bg-indigo-500/20 text-indigo-300 px-1 rounded font-bold">3个顶级品牌</span>：
                <br/><br/>
                1. 品牌 A (高性价比)<br/>
                2. 品牌 B (技术领先)<br/>
                3. 品牌 C (大厂背书)
              </span>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

// --- 2. 漏斗压缩可视化 (Cruel Funnel Visualizer) ---
// 展示从海量信息到精选结果的筛选过程
export const CruelFunnelVisualizer = ({ isActive }) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!isActive) { setStep(0); return; }
    const sequence = async () => {
      await new Promise(r => setTimeout(r, 600));
      setStep(1); // Show thousands of links
      await new Promise(r => setTimeout(r, 1200));
      setStep(2); // Funnel compress
      await new Promise(r => setTimeout(r, 1200));
      setStep(3); // 3-5 slots remain
    };
    sequence();
  }, [isActive]);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-6 bg-white relative overflow-hidden">
      
      <div className="w-full max-w-2xl relative h-72 flex flex-col items-center justify-center gap-2">
        
        {/* 顶部：传统 SEO 海量结果 */}
        <div className={`w-full flex justify-center flex-wrap gap-1 px-10 transition-all duration-1000 ${step >= 1 ? 'opacity-30' : 'opacity-0'}`}>
          {[...Array(40)].map((_, i) => (
            <div key={i} className="w-8 h-2 bg-slate-200 rounded-sm"></div>
          ))}
        </div>
        <div className={`text-[9px] font-bold text-slate-400 mb-2 transition-all duration-500 ${step >= 1 ? 'opacity-100' : 'opacity-0'}`}>
          传统网页收录 (100,000+ 结果)
        </div>

        {/* 中间：AI 压缩漏斗 */}
        <div className={`relative flex items-center justify-center w-full transition-all duration-1000 ${step >= 2 ? 'h-24 opacity-100' : 'h-0 opacity-0'}`}>
          <svg className="absolute w-64 h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <polygon points="0,0 100,0 60,100 40,100" fill="url(#grad1)" opacity="0.1" />
            <defs>
              <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" style={{stopColor: '#6366f1', stopOpacity: 1}} />
                <stop offset="100%" style={{stopColor: '#a855f7', stopOpacity: 1}} />
              </linearGradient>
            </defs>
          </svg>
          <div className="z-10 bg-indigo-600 text-white px-4 py-1.5 rounded-full text-[10px] font-black shadow-lg flex items-center gap-1 animate-pulse">
            <Brain size={12}/> AI 大模型深度总结筛选
          </div>
        </div>

        {/* 底部：残酷结果 */}
        <div className={`text-[9px] font-bold text-indigo-500 mt-2 transition-all duration-500 ${step >= 3 ? 'opacity-100' : 'opacity-0'}`}>
          AI 直接推荐答案 (仅留 3-5 席)
        </div>
        <div className={`flex gap-3 mt-2 transition-all duration-1000 ease-[cubic-bezier(0.25,1,0.5,1)] ${step >= 3 ? 'opacity-100 translate-y-0 scale-100' : 'opacity-0 translate-y-10 scale-50'}`}>
          {[1, 2, 3].map((i) => (
            <div key={i} className="bg-slate-900 border border-slate-700 w-20 h-24 rounded-2xl flex flex-col items-center justify-center shadow-[0_0_20px_rgba(99,102,241,0.3)] relative group">
              <Crown size={20} className="text-amber-400 mb-2"/>
              <div className="text-[10px] font-black text-white">推荐位 {i}</div>
              <div className="absolute inset-0 rounded-2xl border-2 border-indigo-400/50 animate-ping opacity-50"></div>
            </div>
          ))}
        </div>

        {step >= 3 && (
          <div className="absolute bottom-2 bg-red-50 text-red-600 px-4 py-2 rounded-xl text-[10px] font-bold animate-fadeIn">
            不在名单里 = 从互联网出局
          </div>
        )}
      </div>
    </div>
  );
};

// --- 3. 雷达扫描可视化 (Radar Visualizer) ---
// 展示全平台监控、实时追踪的能力
export const RadarVisualizer = ({ isActive, platforms = [] }) => {
  const [scanAngle, setScanAngle] = useState(0);
  const [activePlatforms, setActivePlatforms] = useState([]);

  useEffect(() => {
    if (!isActive) {
      setScanAngle(0);
      setActivePlatforms([]);
      return;
    }

    // 雷达扫描动画
    const scanInterval = setInterval(() => {
      setScanAngle(prev => (prev + 2) % 360);
    }, 30);

    // 平台逐个点亮
    platforms.forEach((_, index) => {
      setTimeout(() => {
        setActivePlatforms(prev => [...prev, index]);
      }, index * 500);
    });

    return () => clearInterval(scanInterval);
  }, [isActive, platforms]);

  return (
    <div className="w-full h-full flex items-center justify-center p-6 bg-slate-900 relative overflow-hidden">
      
      {/* 雷达圆盘 */}
      <div className="relative w-64 h-64">
        {/* 背景圆环 */}
        {[1, 2, 3].map(i => (
          <div 
            key={i}
            className="absolute inset-0 rounded-full border border-indigo-500/20"
            style={{ 
              width: `${i * 33.33}%`, 
              height: `${i * 33.33}%`,
              top: `${(100 - i * 33.33) / 2}%`,
              left: `${(100 - i * 33.33) / 2}%`
            }}
          />
        ))}

        {/* 扫描线 */}
        <div 
          className="absolute top-1/2 left-1/2 w-32 h-0.5 bg-gradient-to-r from-indigo-500 to-transparent origin-left"
          style={{ transform: `translate(-50%, -50%) rotate(${scanAngle}deg)` }}
        />

        {/* 中心点 */}
        <div className="absolute top-1/2 left-1/2 w-4 h-4 bg-indigo-500 rounded-full -translate-x-1/2 -translate-y-1/2 animate-pulse" />

        {/* 平台图标（环绕分布） */}
        {platforms.map((platform, index) => {
          const angle = (index / platforms.length) * 360;
          const radius = 120;
          const x = Math.cos((angle * Math.PI) / 180) * radius;
          const y = Math.sin((angle * Math.PI) / 180) * radius;
          const isActive = activePlatforms.includes(index);

          return (
            <div
              key={index}
              className={`absolute top-1/2 left-1/2 w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-500 ${
                isActive 
                  ? 'bg-indigo-500 text-white scale-110 shadow-[0_0_20px_rgba(99,102,241,0.6)]' 
                  : 'bg-slate-800 text-slate-600 scale-90'
              }`}
              style={{ 
                transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px))` 
              }}
            >
              {platform.icon}
            </div>
          );
        })}
      </div>

      {/* 状态文字 */}
      <div className="absolute bottom-8 text-center">
        <div className="text-indigo-400 text-sm font-bold mb-1">全平台实时监控</div>
        <div className="text-slate-500 text-xs">
          已激活 {activePlatforms.length} / {platforms.length} 个平台
        </div>
      </div>
    </div>
  );
};

// --- 4. 对比展示 (Before/After Comparison) ---
// 传统方案 vs AI 方案的对比
export const BeforeAfterComparison = ({ before, after, isActive }) => {
  const [showAfter, setShowAfter] = useState(false);

  useEffect(() => {
    if (!isActive) {
      setShowAfter(false);
      return;
    }
    setTimeout(() => setShowAfter(true), 1000);
  }, [isActive]);

  return (
    <div className="w-full h-full flex items-center justify-center p-6 bg-[#f8fafc]">
      <div className="grid grid-cols-2 gap-6 w-full max-w-4xl">
        
        {/* 传统方式 */}
        <div className={`transition-all duration-700 ${showAfter ? 'opacity-40 scale-95' : 'opacity-100 scale-100'}`}>
          <div className="bg-white/70 backdrop-blur-xl rounded-3xl p-6 border border-slate-200">
            <div className="text-xs font-bold text-red-500 mb-4 flex items-center gap-2">
              <span className="w-2 h-2 bg-red-500 rounded-full"></span>
              传统方式
            </div>
            <div className="space-y-3">
              {before.map((item, i) => (
                <div key={i} className="flex items-start gap-2 text-sm text-slate-600">
                  <span className="text-red-400 mt-0.5">✗</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* AI 方案 */}
        <div className={`transition-all duration-700 delay-300 ${showAfter ? 'opacity-100 scale-100' : 'opacity-0 scale-90'}`}>
          <div className="bg-white/70 backdrop-blur-xl rounded-3xl p-6 border border-indigo-200 shadow-[0_0_30px_rgba(99,102,241,0.2)]">
            <div className="text-xs font-bold text-emerald-500 mb-4 flex items-center gap-2">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
              AI 方案
            </div>
            <div className="space-y-3">
              {after.map((item, i) => (
                <div key={i} className="flex items-start gap-2 text-sm text-slate-700">
                  <span className="text-emerald-500 mt-0.5">✓</span>
                  <span>{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

// --- 5. 数据流动可视化 (Data Flow Visualizer) ---
// 展示数据处理流程
export const DataFlowVisualizer = ({ steps, isActive }) => {
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    if (!isActive) {
      setCurrentStep(0);
      return;
    }

    const interval = setInterval(() => {
      setCurrentStep(prev => (prev < steps.length - 1 ? prev + 1 : prev));
    }, 1500);

    return () => clearInterval(interval);
  }, [isActive, steps]);

  return (
    <div className="w-full h-full flex items-center justify-center p-6 bg-white">
      <div className="flex items-center gap-4">
        {steps.map((step, index) => (
          <React.Fragment key={index}>
            {/* 步骤节点 */}
            <div className={`
              flex flex-col items-center gap-2 transition-all duration-500
              ${index <= currentStep ? 'opacity-100 scale-100' : 'opacity-30 scale-90'}
            `}>
              <div className={`
                w-16 h-16 rounded-2xl flex items-center justify-center
                ${index <= currentStep ? 'bg-indigo-500 text-white' : 'bg-slate-200 text-slate-400'}
                transition-all duration-500
              `}>
                {step.icon}
              </div>
              <div className="text-xs font-bold text-slate-700 text-center max-w-[80px]">
                {step.label}
              </div>
            </div>

            {/* 连接箭头 */}
            {index < steps.length - 1 && (
              <ArrowRight 
                size={24} 
                className={`
                  transition-all duration-500
                  ${index < currentStep ? 'text-indigo-500 opacity-100' : 'text-slate-300 opacity-30'}
                `}
              />
            )}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
