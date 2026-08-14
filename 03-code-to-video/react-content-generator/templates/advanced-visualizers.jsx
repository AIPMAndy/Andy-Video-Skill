// ============================================
// 高级可视化组件 - 基于三个案例提炼的新模式
// ============================================

import React, { useState, useEffect } from 'react';
import { ArrowRight, Zap, Brain, AlertTriangle, Factory } from 'lucide-react';

// --- 1. 对比崩溃模式 (Contrast Collapse Pattern) ---
// 适合展示痛点：正常状态 → 转折 → 崩溃+警示
// 参考：TensorFlow的LabToProductionPain、liteparse的TheBloodyTruth
export const ContrastCollapseVisualizer = ({
  isActive,
  leftContent,   // { icon, title, subtitle }
  rightContent,  // { icon, title, subtitle }
  transformIcon = Zap,
  overlayContent, // { icon, text }
  bottomAlert,    // { icon, text }
  theme = 'light' // 'light' | 'dark'
}) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!isActive) { setStep(0); return; }
    const timer1 = setTimeout(() => setStep(1), 1000);
    const timer2 = setTimeout(() => setStep(2), 2500);
    const timer3 = setTimeout(() => setStep(3), 4500);
    return () => { clearTimeout(timer1); clearTimeout(timer2); clearTimeout(timer3); };
  }, [isActive]);

  const isDark = theme === 'dark';
  const bgClass = isDark ? 'bg-slate-900' : 'bg-slate-50/50';
  const textClass = isDark ? 'text-slate-200' : 'text-slate-800';

  return (
    <div className={`w-full h-full flex flex-col items-center justify-center gap-6 p-6 relative ${bgClass} overflow-hidden ${textClass} rounded-3xl`}>

      <div className="w-full max-w-2xl flex items-center justify-between z-10 px-4 h-72 relative">

        {/* Left: Original State */}
        <div className={`flex flex-col items-center gap-3 transition-all duration-700 w-1/3 ${
          step >= 2 ? 'opacity-40 blur-[1px] scale-90' : 'opacity-100'
        }`}>
          <div className={`w-20 h-20 ${isDark ? 'bg-slate-800' : 'bg-slate-900'} rounded-2xl flex items-center justify-center shadow-lg border ${isDark ? 'border-slate-700' : 'border-slate-700'} relative`}>
            {leftContent.icon}
          </div>
          <div className="text-center">
            <span className="text-[12px] font-black block">{leftContent.title}</span>
            <span className={`text-[10px] leading-tight block mt-1 ${isDark ? 'text-slate-500' : 'text-slate-500'}`}>
              {leftContent.subtitle}
            </span>
          </div>
        </div>

        {/* Middle: Transformation */}
        <div className="flex-1 flex justify-center relative">
          {step === 1 && <ArrowRight size={28} className={isDark ? 'text-slate-600' : 'text-slate-300'} />}
          {step >= 2 && (
            <div className="flex flex-col items-center">
              {React.createElement(transformIcon, { size: 28, className: 'text-rose-500 animate-bounce' })}
              <span className="text-[10px] font-black text-rose-500 mt-2 bg-rose-50 px-2 py-0.5 rounded border border-rose-200">
                {overlayContent?.text || '转折点'}
              </span>
            </div>
          )}
        </div>

        {/* Right: Problem State with Overlay */}
        <div className={`flex flex-col items-center gap-3 transition-all duration-700 w-1/3 ${
          step >= 2 ? 'scale-105' : 'opacity-0 translate-x-8'
        }`}>
          <div className="w-20 h-20 bg-white rounded-2xl flex items-center justify-center shadow-xl border-2 border-orange-200 relative overflow-hidden">
            {step >= 2 && <div className="absolute inset-0 bg-orange-500/5 animate-pulse"></div>}
            {rightContent.icon}
            {step >= 3 && overlayContent && (
              <div className="absolute inset-0 flex items-center justify-center bg-white/80 backdrop-blur-sm">
                {React.createElement(overlayContent.icon, { size: 32, className: 'text-rose-500 animate-pulse' })}
              </div>
            )}
          </div>
          <div className="text-center">
            <span className="text-[12px] font-black block text-orange-600">{rightContent.title}</span>
            <span className="text-[10px] text-slate-500 leading-tight block mt-1">
              {rightContent.subtitle}
            </span>
          </div>
        </div>
      </div>

      {/* Bottom Alert */}
      {step >= 3 && bottomAlert && (
        <div className={`absolute bottom-4 ${isDark ? 'bg-slate-800' : 'bg-slate-900'} text-white px-6 py-3 rounded-full flex items-center gap-3 text-[12px] font-bold shadow-2xl animate-[slideInUp_0.5s_ease-out]`}>
          {React.createElement(bottomAlert.icon, { size: 16, className: 'text-orange-400 shrink-0' })}
          <span>{bottomAlert.text}</span>
        </div>
      )}
    </div>
  );
};

// --- 2. 流程引擎模式 (Flow Engine Pattern) ---
// 适合展示技术架构：输入 → 引擎处理 → 多个输出
// 参考：liteparse的SemanticParsingArch
export const FlowEngineVisualizer = ({
  isActive,
  inputNode,      // { icon, label }
  engineNode,     // { icon, label, gradient }
  outputNodes,    // [{ icon, label, color }]
  theme = 'light'
}) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!isActive) { setStep(0); return; }
    const timer1 = setTimeout(() => setStep(1), 800);
    const timer2 = setTimeout(() => setStep(2), 2000);
    const timer3 = setTimeout(() => setStep(3), 3200);
    return () => { clearTimeout(timer1); clearTimeout(timer2); clearTimeout(timer3); };
  }, [isActive]);

  const isDark = theme === 'dark';
  const bgClass = isDark ? 'bg-slate-900' : 'bg-slate-50';

  return (
    <div className={`w-full h-full flex items-center justify-center p-6 ${bgClass} relative overflow-hidden`}>

      <div className="flex items-center gap-8 w-full max-w-4xl">

        {/* Input Node */}
        <div className={`transition-all duration-700 ${step >= 1 ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-10'}`}>
          <div className={`w-24 h-24 rounded-2xl ${isDark ? 'bg-slate-800' : 'bg-white'} border ${isDark ? 'border-slate-700' : 'border-slate-200'} flex flex-col items-center justify-center shadow-lg`}>
            {inputNode.icon}
            <span className={`text-[10px] font-bold mt-2 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
              {inputNode.label}
            </span>
          </div>
        </div>

        {/* SVG Flow Line */}
        {step >= 2 && (
          <svg className="w-16 h-2" viewBox="0 0 100 10">
            <path
              d="M 0 5 L 100 5"
              fill="none"
              stroke={isDark ? '#3b82f6' : '#6366f1'}
              strokeWidth="2"
              strokeDasharray="6 6"
              className="animate-dash"
            />
          </svg>
        )}

        {/* Engine Node */}
        <div className={`relative transition-all duration-1000 ${step >= 1 ? 'opacity-100 scale-100' : 'opacity-0 scale-50'}`}>
          <div className={`w-32 h-32 rounded-3xl ${engineNode.gradient || 'bg-gradient-to-br from-blue-500 to-indigo-600'} flex flex-col items-center justify-center shadow-2xl relative overflow-hidden`}>
            {step >= 2 && (
              <div className="absolute inset-0">
                <div className="absolute inset-0 bg-white/10 animate-ping"></div>
              </div>
            )}
            <div className="relative z-10 flex flex-col items-center">
              {engineNode.icon}
              <span className="text-[11px] font-black text-white mt-2">{engineNode.label}</span>
            </div>
          </div>
        </div>

        {/* SVG Flow Lines to Outputs */}
        {step >= 2 && (
          <svg className="w-16 h-2" viewBox="0 0 100 10">
            <path
              d="M 0 5 L 100 5"
              fill="none"
              stroke={isDark ? '#3b82f6' : '#6366f1'}
              strokeWidth="2"
              strokeDasharray="6 6"
              className="animate-dash"
            />
          </svg>
        )}

        {/* Output Nodes */}
        <div className="flex flex-col gap-3">
          {outputNodes.map((node, index) => (
            <div
              key={index}
              className={`transition-all duration-700 ${
                step >= 3 ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-10'
              }`}
              style={{ transitionDelay: `${index * 100}ms` }}
            >
              <div className={`flex items-center gap-2 px-4 py-2 rounded-xl ${isDark ? 'bg-slate-800' : 'bg-white'} border-l-4 ${node.color || 'border-blue-500'} shadow-md`}>
                {node.icon}
                <span className={`text-[10px] font-bold ${isDark ? 'text-slate-200' : 'text-slate-700'}`}>
                  {node.label}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// --- 3. 卡片瀑布流模式 (Card Cascade Pattern) ---
// 适合展示特性列表：多个特性卡片依次出现
// 参考：social-auto-upload的AutoUploadFeatures
export const CardCascadeVisualizer = ({
  isActive,
  cards,    // [{ icon, title, description, color }]
  layout = 'grid', // 'grid' | 'vertical'
  theme = 'light'
}) => {
  const [visibleCards, setVisibleCards] = useState([]);

  useEffect(() => {
    if (!isActive) {
      setVisibleCards([]);
      return;
    }

    cards.forEach((_, index) => {
      setTimeout(() => {
        setVisibleCards(prev => [...prev, index]);
      }, 800 + index * 200);
    });
  }, [isActive, cards]);

  const isDark = theme === 'dark';
  const layoutClass = layout === 'grid' ? 'grid grid-cols-2 gap-4' : 'flex flex-col gap-3';

  return (
    <div className={`w-full h-full flex items-center justify-center p-6 ${isDark ? 'bg-slate-900' : 'bg-slate-50'}`}>
      <div className={`w-full max-w-2xl ${layoutClass}`}>
        {cards.map((card, index) => (
          <div
            key={index}
            className={`transition-all duration-700 ${
              visibleCards.includes(index)
                ? 'opacity-100 translate-y-0'
                : 'opacity-0 translate-y-10'
            }`}
          >
            <div className={`${isDark ? 'bg-slate-800/50' : 'bg-white/70'} backdrop-blur-xl rounded-2xl p-5 border ${isDark ? 'border-slate-700/50' : 'border-white/60'} shadow-lg hover:-translate-y-1.5 transition-all duration-300`}>
              <div className="flex items-start gap-3">
                <div className={`w-10 h-10 rounded-xl ${card.color || 'bg-blue-50'} flex items-center justify-center shrink-0`}>
                  {card.icon}
                </div>
                <div className="flex-1">
                  <h4 className={`text-sm font-black mb-1 ${isDark ? 'text-slate-200' : 'text-slate-800'}`}>
                    {card.title}
                  </h4>
                  <p className={`text-[11px] leading-relaxed ${isDark ? 'text-slate-400' : 'text-slate-600'}`}>
                    {card.description}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// --- 4. 金句组件标准模板 ---
// 适合展示Andy的身份背书和核心观点
// 参考：三个案例中的GoldenSentence组件
export const GoldenSentenceStandard = ({
  isActive,
  quote,      // { top, bottom, highlight }
  author = 'Andy',
  credentials = [],
  theme = 'light'
}) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!isActive) { setStep(0); return; }
    const timer1 = setTimeout(() => setStep(1), 800);
    const timer2 = setTimeout(() => setStep(2), 2000);
    return () => { clearTimeout(timer1); clearTimeout(timer2); };
  }, [isActive]);

  const isDark = theme === 'dark';

  return (
    <div className={`w-full h-full flex flex-col items-center justify-center p-8 ${isDark ? 'bg-slate-900' : 'bg-gradient-to-br from-slate-50 to-white'} relative overflow-hidden`}>

      {/* Quote Mark */}
      <div className={`text-8xl font-serif ${isDark ? 'text-slate-800/20' : 'text-slate-200/40'} absolute top-8 left-8`}>"</div>

      <div className="relative z-10 max-w-3xl text-center">

        {/* Top Quote */}
        <div className={`transition-all duration-1000 ${step >= 1 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <p className={`text-2xl md:text-3xl font-bold leading-relaxed mb-4 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
            {quote.top}
          </p>
        </div>

        {/* Bottom Quote with Highlight */}
        <div className={`transition-all duration-1000 delay-300 ${step >= 2 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <p className="text-2xl md:text-3xl font-black leading-relaxed bg-clip-text text-transparent bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500">
            {quote.bottom}
          </p>
        </div>

        {/* Author & Credentials */}
        {step >= 2 && (
          <div className={`mt-8 flex flex-col items-center gap-2 animate-fadeInScale`}>
            <div className={`text-lg font-black ${isDark ? 'text-slate-200' : 'text-slate-900'}`}>
              — {author}
            </div>
            <div className="flex flex-wrap gap-2 justify-center">
              {credentials.map((cred, index) => (
                <span
                  key={index}
                  className={`text-[10px] px-3 py-1 rounded-full ${isDark ? 'bg-slate-800 text-slate-400' : 'bg-slate-100 text-slate-600'} font-bold`}
                >
                  {cred}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
