// ============================================
// 完整项目模板 - App.jsx
// ============================================

import React, { useState, useEffect, useRef } from 'react';
import { 
  Brain, 
  Search, 
  MessageSquare, 
  TrendingDown, 
  Target, 
  Radar, 
  Globe, 
  CheckCircle2, 
  XCircle, 
  Zap, 
  ShieldCheck, 
  Box, 
  Eye, 
  BarChart3, 
  Bot, 
  Sparkles, 
  Database, 
  ArrowRight, 
  FolderOpen, 
  Cpu, 
  Layers, 
  Terminal, 
  Code2, 
  Check, 
  Star, 
  Trophy, 
  Building2, 
  MousePointerClick, 
  LineChart, 
  Link,
  Crown,
  SearchCode,
  User,
  History,
  Settings2,
  Workflow
} from 'lucide-react';

// --- 核心组件 ---
const GlassCard = ({ children, className = "", onClick, active = false, style={} }) => {
  return (
    <div
      onClick={onClick}
      style={style}
      className={`
        relative overflow-hidden rounded-[2.5rem] bg-white/70 backdrop-blur-3xl
        border border-white/80
        shadow-[0_10px_40px_rgba(0,0,0,0.04)]
        transition-[transform,box-shadow,opacity] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]
        ${active ? 'scale-95 shadow-[inset_0_2px_10px_rgba(0,0,0,0.03)] ring-2 ring-indigo-500/30' : 'hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(79,70,229,0.08)]'}
        ${className}
      `}
    >
      <div className="relative h-full z-10">{children}</div>
      <div className="absolute top-0 left-0 w-full h-1/2 bg-gradient-to-b from-white/90 to-transparent pointer-events-none opacity-90"></div>
      <div className="absolute bottom-0 right-0 w-2/3 h-2/3 bg-gradient-to-t from-indigo-50/50 to-transparent pointer-events-none rounded-[2.5rem]"></div>
    </div>
  );
};

const ScriptFooter = ({ text }) => (
  <div className="absolute bottom-8 left-0 w-full flex justify-center z-50 pointer-events-none px-4">
    <div className="bg-white/80 backdrop-blur-2xl border border-white/50 px-6 py-4 md:px-8 md:py-5 rounded-full shadow-[0_10px_40px_rgba(0,0,0,0.08)] max-w-4xl text-center w-full md:w-auto animate-slideInUp">
      <div className="text-slate-700 text-sm md:text-lg font-bold leading-relaxed text-center">
        {text}
      </div>
    </div>
  </div>
);

// --- 主应用 ---
export default function App() {
  const [step, setStep] = useState(0);
  const [smoothMouse, setSmoothMouse] = useState({ x: 0, y: 0 });

  // 鼠标跟踪（用于背景动画）
  useEffect(() => {
    const handleMouseMove = (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;
      setSmoothMouse({ x, y });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const nextStep = () => setStep(s => s + 1);

  const totalSteps = 5; // 根据实际页面数量调整

  const gridContainerClass = "absolute inset-0 grid grid-cols-1 grid-rows-1";
  const pageBaseClass = "col-start-1 row-start-1 w-full h-full flex flex-col items-center justify-center transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]";
  
  const getPageStyle = (index) => {
    if (index === step) return "opacity-100 scale-100 z-20 pointer-events-auto";
    if (index < step) return "opacity-0 scale-95 -translate-y-10 z-10 pointer-events-none";
    return "opacity-0 scale-105 translate-y-10 z-0 pointer-events-none";
  };

  const steps = [
    // --- 第 1 页：开场 ---
    (
      <>
        <div className="flex flex-col items-center gap-8 animate-fadeInScale">
          <div className="text-5xl md:text-7xl font-black text-slate-900 text-center leading-tight">
            AI 搜索革命
          </div>
          <div className="text-lg md:text-2xl text-slate-600 text-center max-w-2xl">
            传统 SEO 已死，AI 推荐时代来临
          </div>
          <div className="flex gap-4 mt-4">
            <GlassCard className="px-6 py-3">
              <div className="flex items-center gap-2">
                <Brain size={20} className="text-indigo-500"/>
                <span className="font-bold text-slate-700">智能推荐</span>
              </div>
            </GlassCard>
            <GlassCard className="px-6 py-3">
              <div className="flex items-center gap-2">
                <Target size={20} className="text-purple-500"/>
                <span className="font-bold text-slate-700">精准触达</span>
              </div>
            </GlassCard>
          </div>
        </div>
        <ScriptFooter text="今天我们来聊聊一个正在发生的巨变：AI 搜索革命。这不是未来，而是现在进行时。" />
      </>
    ),

    // --- 第 2 页：痛点 ---
    (
      <>
        <div className="w-full max-w-4xl">
          <div className="text-3xl md:text-5xl font-black text-slate-900 mb-8 text-center">
            用户习惯彻底改变
          </div>
          {/* 这里插入 SearchShiftVisualizer 组件 */}
          <div className="h-96 bg-white/50 backdrop-blur-xl rounded-3xl border border-slate-200 flex items-center justify-center">
            <div className="text-slate-400 text-sm">[ 搜索迁徙可视化 ]</div>
          </div>
        </div>
        <ScriptFooter text="过去，用户在百度、谷歌搜索，翻页找答案。现在，他们直接问 ChatGPT、Gemini，AI 直接给出 3-5 个推荐。" />
      </>
    ),

    // --- 第 3 页：残酷真相 ---
    (
      <>
        <div className="w-full max-w-4xl">
          <div className="text-3xl md:text-5xl font-black text-slate-900 mb-8 text-center">
            只留 3-5 个席位
          </div>
          {/* 这里插入 CruelFunnelVisualizer 组件 */}
          <div className="h-96 bg-white/50 backdrop-blur-xl rounded-3xl border border-slate-200 flex items-center justify-center">
            <div className="text-slate-400 text-sm">[ 漏斗压缩可视化 ]</div>
          </div>
        </div>
        <ScriptFooter text="AI 会从全网 10 万+ 结果中，深度总结筛选，最终只推荐 3-5 个品牌。不在名单里，就等于从互联网出局。" />
      </>
    ),

    // --- 第 4 页：解决方案 ---
    (
      <>
        <div className="w-full max-w-5xl">
          <div className="text-3xl md:text-5xl font-black text-slate-900 mb-12 text-center">
            如何进入 AI 推荐名单？
          </div>
          <div className="grid grid-cols-3 gap-6">
            {[
              { icon: Database, title: "全平台布局", desc: "覆盖所有 AI 训练数据源" },
              { icon: Star, title: "高质量内容", desc: "让 AI 认可你的专业度" },
              { icon: Crown, title: "持续优化", desc: "实时监控 AI 推荐排名" }
            ].map((item, i) => (
              <GlassCard key={i} className="p-6 animate-fadeInScale" style={{animationDelay: `${i * 0.2}s`}}>
                <div className="flex flex-col items-center text-center gap-3">
                  <div className="w-16 h-16 rounded-2xl bg-indigo-100 flex items-center justify-center">
                    <item.icon size={32} className="text-indigo-600"/>
                  </div>
                  <h3 className="text-lg font-bold text-slate-900">{item.title}</h3>
                  <p className="text-sm text-slate-600">{item.desc}</p>
                </div>
              </GlassCard>
            ))}
          </div>
        </div>
        <ScriptFooter text="三个关键动作：全平台布局、高质量内容、持续优化。缺一不可。" />
      </>
    ),

    // --- 第 5 页：结尾 ---
    (
      <>
        <div className="flex flex-col items-center gap-8">
          <div className="text-4xl md:text-6xl font-black text-slate-900 text-center leading-tight animate-fadeInScale">
            抓住 AI 时代的<br/>流量红利
          </div>
          <div className="w-px h-20 bg-slate-200 scale-x-50"></div>
          <div className="flex flex-col items-center gap-5">
            <div className="text-slate-500 text-sm md:text-lg font-bold text-center animate-fadeInScale" style={{animationDelay: '0.3s'}}>
              想了解更多？
            </div>
            <div className="px-10 py-3 rounded-full bg-slate-900 text-white font-mono text-sm md:text-lg font-bold shadow-lg flex items-center justify-center animate-fadeInScale" style={{animationDelay: '0.5s'}}>
              扫码咨询
            </div>
          </div>
        </div>
        <ScriptFooter text="AI 搜索革命已经开始，你准备好了吗？想了解更多，欢迎扫码咨询。下课！" />
      </>
    )
  ];

  return (
    <div 
      onClick={nextStep}
      className="fixed inset-0 w-full h-full overflow-hidden cursor-pointer font-sans text-slate-800 bg-[#f8fafc] select-none"
    >
      <style>
        {`
        @keyframes fadeInScale {
          from { opacity: 0; transform: translateY(40px) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes slideInUp {
          from { opacity: 0; transform: translateY(50px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeInScale { animation: fadeInScale 0.6s cubic-bezier(0.25, 1, 0.5, 1) both; }
        .animate-slideInUp { animation: slideInUp 0.5s cubic-bezier(0.25, 1, 0.5, 1) both; }
        `}
      </style>

      {/* 动态背景 */}
      <div className="absolute inset-0 pointer-events-none overflow-hidden bg-[#f8fafc]">
        <div className="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-indigo-100/40 blur-[120px]" 
             style={{ transform: `translate(${smoothMouse.x * -20}px, ${smoothMouse.y * 20}px)` }} />
        <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-purple-100/30 blur-[120px]"
             style={{ transform: `translate(${smoothMouse.x * 20}px, ${smoothMouse.y * -20}px)` }} />
      </div>

      {/* 进度条 */}
      <div className="absolute top-6 left-6 right-6 md:top-8 md:left-1/2 md:-translate-x-1/2 md:w-64 h-1.5 bg-slate-200 rounded-full overflow-hidden z-50">
        <div 
          className="h-full bg-gradient-to-r from-indigo-400 via-purple-400 to-blue-400 rounded-full transition-all duration-500 ease-out"
          style={{ width: `${((step + 1) / totalSteps) * 100}%` }}
        />
      </div>

      {/* 页面容器 */}
      <div className={gridContainerClass}>
        {steps.map((content, index) => (
          <div key={index} className={`${pageBaseClass} ${getPageStyle(index)}`}>
            {content}
          </div>
        ))}
      </div>

    </div>
  );
}
