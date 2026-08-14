import React, { useState, useEffect, useRef } from 'react';
import {
  Star, Globe, Users, Bot, Flame, Code2, Search, ShieldCheck,
  CheckCircle2, XCircle, Layers, Database, FileText, FileJson,
  Sparkles, Network, Terminal, User, Zap, Activity, Settings,
  ArrowRight, MessageSquare, BrainCircuit, AlertTriangle
} from 'lucide-react';
import { markVideoReady, setVideoDuration } from './video-runtime.js';

// Design canvas constants (fixed design dimensions)
const DESIGN_WIDTH = 1200;
const DESIGN_HEIGHT = 1600;

// Responsive scaling hook - scales fixed design canvas to fit viewport
const useStageScale = () => {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const updateScale = () => {
      const scaleX = window.innerWidth / DESIGN_WIDTH;
      const scaleY = window.innerHeight / DESIGN_HEIGHT;
      setScale(Math.min(scaleX, scaleY));
    };

    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, []);

  return scale;
};

// Icon mapping for dynamic icon selection
const ICON_MAP = {
  star: Star, globe: Globe, users: Users, bot: Bot, flame: Flame,
  code: Code2, search: Search, shield: ShieldCheck, check: CheckCircle2,
  x: XCircle, layers: Layers, database: Database, file: FileText,
  json: FileJson, sparkles: Sparkles, network: Network, terminal: Terminal,
  user: User, zap: Zap, activity: Activity, settings: Settings,
  arrow: ArrowRight, message: MessageSquare, brain: BrainCircuit,
  alert: AlertTriangle
};

// --- Core Components ---
const GlassCard = ({ children, className = "", onClick, active = false, style = {} }) => {
  return (
    <div
      onClick={onClick}
      style={style}
      className={`
        relative overflow-hidden rounded-[2.5rem] bg-white/70 backdrop-blur-3xl
        border border-white/80
        shadow-[0_10px_40px_rgba(0,0,0,0.04)]
        transition-[transform,box-shadow,opacity] duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]
        ${active ? 'scale-95 shadow-[inset_0_2px_10px_rgba(0,0,0,0.03)]' : 'hover:-translate-y-1 hover:shadow-[0_20px_50px_rgba(99,102,241,0.08)]'}
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
  <div className="absolute bottom-[3.25rem] left-0 w-full flex justify-center z-50 pointer-events-none px-[3.25rem]">
    <div className="rounded-full border border-white/80 bg-white/90 px-[3.25rem] py-[1.9rem] text-center shadow-[0_18px_42px_rgba(15,23,42,0.11)] backdrop-blur-2xl">
      <div className="text-[1.62rem] font-bold leading-[1.54] tracking-[0.012em] text-slate-800">
        {text}
      </div>
    </div>
  </div>
);

// --- Generic Visualizer Components ---
const PainPointVisualizer = ({ config, isActive }) => {
  const [phase, setPhase] = useState(0);

  useEffect(() => {
    if (!isActive) { setPhase(0); return; }
    const interval = setInterval(() => setPhase(p => (p + 1) % (config.items?.length || 4)), 2000);
    return () => clearInterval(interval);
  }, [isActive, config.items]);

  const Icon = ICON_MAP[config.icon] || AlertTriangle;

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-6 relative bg-[#f8fafc] overflow-hidden">
      <div className={`absolute top-6 flex items-center gap-2 bg-red-50 text-red-600 px-4 py-2 rounded-full text-[10px] font-bold border border-red-100 transition-opacity duration-500 ${phase >= 1 ? 'opacity-100' : 'opacity-0'}`}>
        <Icon size={14} className="animate-pulse"/> {config.badge || "常见痛点"}
      </div>

      <div className="w-full max-w-sm flex flex-col gap-3 relative z-10 mt-8">
        {config.items?.map((item, idx) => {
          const ItemIcon = ICON_MAP[item.icon] || XCircle;
          return (
            <div key={idx} className={`bg-white rounded-xl p-3 shadow-md flex items-center justify-between border border-slate-200 transition-all duration-700 ${phase >= idx + 1 ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'}`}>
              <div className="flex items-center gap-3">
                <div className={`bg-${item.color || 'red'}-50 p-2 rounded-lg text-${item.color || 'red'}-500`}>
                  <ItemIcon size={16}/>
                </div>
                <div className="flex flex-col">
                  <span className="font-bold text-slate-800" style={{ fontSize: '0.875rem' }}>{item.title}</span>
                  <span className="text-[9px] text-slate-500">{item.description}</span>
                </div>
              </div>
              <XCircle size={16} className="text-red-500"/>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const FeatureVisualizer = ({ config, isActive }) => {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!isActive) { setStep(0); return; }
    const sequence = async () => {
      for (let i = 1; i <= (config.steps?.length || 3); i++) {
        await new Promise(r => setTimeout(r, 1000));
        setStep(i);
      }
    };
    sequence();
  }, [isActive, config.steps]);

  return (
    <div className="w-full h-full flex flex-col items-center justify-center p-6 bg-white relative overflow-hidden">
      <div className="w-full max-w-sm flex flex-col items-center gap-3 relative z-10">
        {config.steps?.map((stepConfig, idx) => {
          const StepIcon = ICON_MAP[stepConfig.icon] || Sparkles;
          return (
            <div key={idx} className={`w-full bg-white border border-slate-200 p-3 rounded-xl flex items-center gap-3 shadow-sm transition-all duration-700 ${step >= idx + 1 ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
              <div className={`bg-${stepConfig.color || 'blue'}-100 p-2.5 rounded-xl text-${stepConfig.color || 'blue'}-600 shadow-sm`}>
                <StepIcon size={18}/>
              </div>
              <div className="flex flex-col">
                <span className="text-xs font-bold text-slate-800">{stepConfig.title}</span>
                <span className="text-[9px] text-slate-500">{stepConfig.description}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const GoldenSentence = ({ config }) => {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center relative overflow-hidden bg-white">
      <div className="absolute inset-0 bg-white rounded-[3rem] transform scale-95 origin-center shadow-[0_20px_60px_rgba(0,0,0,0.06)] border border-slate-100 flex flex-col items-center justify-center p-8">
        <div className="relative z-10 text-center w-full max-w-4xl">
          <div className={`text-${config.themeColor || 'indigo'}-600 font-bold tracking-[0.3em] mb-8 animate-slideInUp uppercase`} style={{ fontSize: '0.875rem' }}>
            {config.subtitle || "Philosophy"}
          </div>

          <h2 className="font-black text-slate-800 leading-tight mb-8 animate-fadeInScale tracking-tight" style={{ fontSize: '4.55rem', animationDelay: '0.2s' }}>
            {config.quote}
          </h2>

          <div className={`w-16 h-1 bg-${config.themeColor || 'indigo'}-500 mx-auto rounded-full mb-8 animate-scaleX`} style={{animationDelay: '0.4s'}}></div>

          <p className="text-slate-500 font-medium italic animate-fadeInScale max-w-2xl mx-auto leading-relaxed" style={{ fontSize: '1.86rem', animationDelay: '0.6s' }}>
            {config.explanation}
          </p>
        </div>
      </div>
    </div>
  );
};

// --- Main Generator Component ---
export default function KnowledgeVideoGenerator({ config }) {
  const [step, setStep] = useState(0);
  const [isReady, setIsReady] = useState(false);
  const mousePosRef = useRef({ x: 0, y: 0 });
  const [smoothMouse, setSmoothMouse] = useState({ x: 0, y: 0 });

  const themeColor = config.themeColor || 'indigo';
  const totalSteps = config.steps?.length || 7;

  // Video runtime integration
  useEffect(() => {
    // Support dynamic scene durations from config, fallback to 15s per scene
    const durations = config.sceneDurationsMs || config.steps.map(() => 15000);
    const totalDuration = durations.reduce((sum, d) => sum + d, 0);
    setVideoDuration(totalDuration);

    const timer = setTimeout(() => {
      setIsReady(true);
      markVideoReady();
    }, 1000);

    // Auto-advance through scenes with dynamic durations
    let currentStep = 0;
    const scheduleNext = () => {
      if (currentStep < totalSteps - 1) {
        setTimeout(() => {
          currentStep++;
          setStep(currentStep);
          scheduleNext();
        }, durations[currentStep]);
      }
    };
    scheduleNext();

    return () => {
      clearTimeout(timer);
    };
  }, [totalSteps]);

  useEffect(() => {
    const timer = setTimeout(() => setIsReady(true), 500);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    let frameId;
    const animate = () => {
      const target = mousePosRef.current;
      setSmoothMouse(prev => ({
        x: prev.x + (target.x - prev.x) * 0.05,
        y: prev.y + (target.y - prev.y) * 0.05
      }));
      frameId = requestAnimationFrame(animate);
    };
    const handleMouseMove = (e) => {
      const x = (e.clientX / window.innerWidth) * 2 - 1;
      const y = (e.clientY / window.innerHeight) * 2 - 1;
      mousePosRef.current = { x, y };
    };
    window.addEventListener('mousemove', handleMouseMove);
    animate();
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(frameId);
    };
  }, []);

  const nextStep = () => { if (isReady && step < totalSteps - 1) setStep(step + 1); };

  const gridContainerClass = "w-full h-full grid grid-cols-1 grid-rows-1 bg-[#f8fafc]";
  const pageBaseClass = "col-start-1 row-start-1 w-full h-full flex flex-col items-center justify-center transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)] pb-24 md:pb-40 px-6 md:px-12";

  const getPageStyle = (index) => {
    if (index === step) return "opacity-100 scale-100 z-10 blur-0 pointer-events-auto translate-y-0";
    if (index < step) return "opacity-0 scale-90 z-0 blur-md pointer-events-none -translate-y-10";
    return "opacity-0 scale-110 z-20 blur-sm pointer-events-none translate-y-10";
  };

  const renderStep = (stepConfig, index) => {
    const StepIcon = ICON_MAP[stepConfig.icon] || Star;

    switch (stepConfig.type) {
      case 'cover':
        return (
          <React.Fragment key={index}>
            {/* Floating Star Badge with enhanced animation */}
            <div className="absolute top-24 md:top-32 right-6 md:right-1/4 z-50 animate-fadeInScale" style={{animationDelay: '0.8s'}}>
              <div className={`bg-gradient-to-br from-white to-slate-50 text-slate-800 border-2 border-amber-200 px-5 py-2 md:px-6 md:py-3 rounded-full shadow-2xl flex items-center gap-2 transform -rotate-3 animate-float-badge backdrop-blur-xl relative overflow-hidden`}>
                <div className="absolute inset-0 bg-gradient-to-r from-amber-100/50 to-orange-100/50 animate-gradient"></div>
                <Star className="w-5 h-5 text-amber-500 fill-amber-500 relative z-10 drop-shadow-lg" />
                <span className="font-sans font-black tracking-wide relative z-10 bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent" style={{ fontSize: '1.5rem' }}>{stepConfig.badge}</span>
              </div>
            </div>

            {/* Enhanced Icon with glow and rotation */}
            <div className="mb-10 md:mb-14 relative animate-fadeInScale mx-auto" style={{animationDelay: '0.2s'}}>
              <div className={`w-40 h-40 md:w-56 md:h-56 bg-gradient-to-br from-white to-slate-50 rounded-[4rem] shadow-[0_30px_80px_-15px_rgba(99,102,241,0.4)] flex items-center justify-center relative overflow-hidden group border-2 border-${themeColor}-100 backdrop-blur-xl animate-pulse-glow`}>
                {/* Shimmer effect */}
                <div className="absolute inset-0 shimmer-effect"></div>

                {/* Rotating gradient background */}
                <div className={`absolute inset-0 bg-gradient-to-tr from-${themeColor}-100/60 via-blue-100/40 to-purple-100/60 opacity-70 animate-gradient`}></div>

                {/* Icon with rotation animation */}
                <div className="relative z-10 animate-rotate-icon">
                  <StepIcon className={`w-24 h-24 text-${themeColor}-600 drop-shadow-2xl`} />
                </div>

                {/* Decorative circles */}
                <div className={`absolute top-4 right-4 w-3 h-3 rounded-full bg-${themeColor}-400 animate-pulse`} style={{animationDuration: '2s'}}></div>
                <div className={`absolute bottom-6 left-6 w-2 h-2 rounded-full bg-blue-400 animate-pulse`} style={{animationDuration: '3s'}}></div>
              </div>
            </div>

            {/* Project Name with gradient and shadow */}
            <h1 className="font-black text-center mb-4 tracking-tighter leading-tight animate-slideInUp drop-shadow-2xl w-full relative" style={{ fontSize: '5.5rem', animationDelay: '0.3s' }}>
              <span className={`bg-gradient-to-r from-slate-800 via-slate-700 to-slate-800 bg-clip-text text-transparent animate-gradient`}>
                {config.project?.name || stepConfig.title}
              </span>
            </h1>

            {/* Subtitle with color accent */}
            {stepConfig.subtitle && (
              <p className={`text-center font-bold mb-10 animate-slideInUp bg-gradient-to-r from-${themeColor}-600 via-${themeColor}-500 to-blue-600 bg-clip-text text-transparent animate-gradient`} style={{ fontSize: '2.2rem', animationDelay: '0.4s' }}>
                {stepConfig.subtitle}
              </p>
            )}

            {/* Course badge with enhanced styling */}
            <div className="flex items-center gap-4 bg-gradient-to-r from-white/90 to-slate-50/90 px-8 py-4 rounded-full border-2 border-slate-200 mx-auto animate-fadeInScale backdrop-blur-xl shadow-2xl relative overflow-hidden" style={{animationDelay: '0.5s'}}>
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/50 to-transparent animate-shimmer"></div>
              <span className={`bg-gradient-to-r from-${themeColor}-600 to-${themeColor}-700 text-white px-4 py-2 rounded-full font-black shadow-lg relative z-10 animate-pulse`} style={{ fontSize: '1rem', animationDuration: '3s' }}>
                {stepConfig.courseNumber}
              </span>
              <span className="font-black text-slate-700 relative z-10" style={{ fontSize: '1.5rem' }}>{stepConfig.category}</span>
            </div>

            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'pain_point':
        return (
          <React.Fragment key={index}>
            <div className={`mb-8 px-5 py-2 rounded-full bg-red-50 text-red-600 border border-red-100 font-bold flex items-center gap-2 shadow-sm animate-fadeInScale mx-auto backdrop-blur-md`} style={{ fontSize: '1.125rem' }}>
              <StepIcon className="w-4 h-4" />
              <span>{stepConfig.badge}</span>
            </div>
            <h2 className="font-black text-center mb-10 text-slate-800 animate-fadeInScale w-full" style={{ fontSize: '4.55rem', animationDelay: '0.2s' }}>
              {stepConfig.title}
            </h2>

            <div className="w-full max-w-4xl px-4 mx-auto h-[400px]">
              <GlassCard className="w-full h-full p-0 overflow-hidden bg-white" onClick={(e) => e.stopPropagation()}>
                <PainPointVisualizer config={stepConfig.visualizer} isActive={step === index} />
              </GlassCard>
            </div>
            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'feature':
        return (
          <React.Fragment key={index}>
            <div className={`mb-8 px-5 py-2 rounded-full bg-${themeColor}-50 text-${themeColor}-600 border border-${themeColor}-100 font-bold flex items-center gap-2 shadow-sm animate-fadeInScale mx-auto backdrop-blur-md`} style={{ fontSize: '1.125rem' }}>
              <StepIcon className="w-4 h-4" />
              <span>{stepConfig.badge}</span>
            </div>
            <h2 className="font-black text-center mb-10 text-slate-800 animate-fadeInScale w-full" style={{ fontSize: '4.55rem', animationDelay: '0.2s' }}>
              {stepConfig.title}
            </h2>

            <div className="w-full max-w-4xl px-4 mx-auto h-[400px]">
              <GlassCard className="w-full h-full p-0 overflow-hidden bg-[#f8fafc]" onClick={(e) => e.stopPropagation()}>
                <FeatureVisualizer config={stepConfig.visualizer} isActive={step === index} />
              </GlassCard>
            </div>
            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'golden_sentence':
        return (
          <React.Fragment key={index}>
            <GoldenSentence config={{ ...stepConfig, themeColor }} />
            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'summary':
        return (
          <React.Fragment key={index}>
            <div className="bg-white/70 backdrop-blur-2xl p-8 md:p-12 rounded-[2.5rem] md:rounded-[3.5rem] shadow-[0_20px_60px_rgba(0,0,0,0.05)] border border-white/60 text-center max-w-sm md:max-w-3xl w-full mx-auto relative overflow-hidden animate-fadeInScale">
              <div className={`w-24 h-24 md:w-32 md:h-32 bg-${themeColor}-50 rounded-full flex items-center justify-center mx-auto mb-8 text-${themeColor}-600 shadow-[0_10px_30px_rgba(99,102,241,0.15)] border border-${themeColor}-100`}>
                <StepIcon className="w-10 h-10 md:w-14 md:h-14 animate-pulse" />
              </div>
              <h2 className="font-black text-slate-800 mb-8 leading-tight animate-fadeInScale" style={{ fontSize: '4.55rem', animationDelay: '0.2s' }}>
                {stepConfig.title}
              </h2>
              <ul className="text-slate-600 mb-10 font-medium leading-relaxed max-w-xl mx-auto text-left space-y-5 px-4" style={{ fontSize: '1.375rem' }}>
                {stepConfig.points?.map((point, idx) => {
                  const PointIcon = ICON_MAP[point.icon] || CheckCircle2;
                  return (
                    <li key={idx} className="flex items-start gap-4 animate-fadeInScale" style={{animationDelay: `${0.4 + idx * 0.2}s`}}>
                      <div className={`bg-${point.color || themeColor}-100 p-2 rounded-xl mt-0.5 shrink-0 text-${point.color || themeColor}-600 border border-${point.color || themeColor}-200`}>
                        <PointIcon size={18}/>
                      </div>
                      <span><strong className="text-slate-900">{point.title}：</strong>{point.description}</span>
                    </li>
                  );
                })}
              </ul>
              <div className="w-full h-px bg-slate-200 mb-10 scale-x-50"></div>
              <div className="flex flex-col items-center gap-5">
                <button className="px-8 py-3 rounded-full bg-slate-900 text-white font-bold shadow-xl border border-slate-700 flex items-center gap-3 animate-fadeInScale hover:scale-105 transition-transform active:scale-95 cursor-pointer" style={{ fontSize: '1.125rem' }}>
                  <User className="w-4 h-4" /> {stepConfig.author || "AI酋长Andy"}
                </button>
                <div className="mt-2 text-[10px] text-slate-500 font-mono tracking-widest uppercase">
                  {stepConfig.footer}
                </div>
              </div>
            </div>
            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      default:
        return null;
    }
  };

  const scale = useStageScale();

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-slate-950 flex items-center justify-center">
      <div
        onClick={nextStep}
        className="relative overflow-hidden cursor-pointer font-sans text-slate-800 bg-[#f8fafc] select-none"
        style={{
          width: `${DESIGN_WIDTH}px`,
          height: `${DESIGN_HEIGHT}px`,
          transform: `scale(${scale})`,
          transformOrigin: 'center center',
        }}
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
          @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-60px); }
            to { opacity: 1; transform: translateX(0); }
          }
          @keyframes slideInRight {
            from { opacity: 0; transform: translateX(60px); }
            to { opacity: 1; transform: translateX(0); }
          }
          @keyframes scaleX {
            from { transform: scaleX(0); }
            to { transform: scaleX(1); }
          }
          @keyframes float-badge {
            0%, 100% { transform: translateY(0) rotate(-3deg); }
            50% { transform: translateY(-10px) rotate(-3deg); }
          }
          @keyframes rotate-icon {
            0% { transform: rotate(0deg) scale(1); }
            50% { transform: rotate(5deg) scale(1.05); }
            100% { transform: rotate(0deg) scale(1); }
          }
          @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.3); }
            50% { box-shadow: 0 0 40px rgba(99, 102, 241, 0.6); }
          }
          @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
          }
          @keyframes particle-float {
            0%, 100% { transform: translateY(0) translateX(0); opacity: 0.3; }
            25% { transform: translateY(-20px) translateX(10px); opacity: 0.6; }
            50% { transform: translateY(-40px) translateX(-10px); opacity: 0.3; }
            75% { transform: translateY(-20px) translateX(5px); opacity: 0.6; }
          }
          @keyframes shimmer {
            0% { transform: translateX(-100%); }
            100% { transform: translateX(100%); }
          }
          .animate-fadeInScale { animation: fadeInScale 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
          .animate-slideInUp { animation: slideInUp 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
          .animate-slideInLeft { animation: slideInLeft 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
          .animate-slideInRight { animation: slideInRight 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
          .animate-scaleX { animation: scaleX 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
          .animate-float-badge { animation: float-badge 3s ease-in-out infinite; }
          .animate-rotate-icon { animation: rotate-icon 4s ease-in-out infinite; }
          .animate-pulse-glow { animation: pulse-glow 2s ease-in-out infinite; }
          .animate-gradient {
            background-size: 200% 200%;
            animation: gradient-shift 3s ease infinite;
          }
          .animate-particle { animation: particle-float 4s ease-in-out infinite; }
          .shimmer-effect::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
            animation: shimmer 2s infinite;
          }
          `}
        </style>

        {/* Enhanced Dynamic Background with Particles */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden bg-gradient-to-br from-slate-50 via-white to-slate-100">
          {/* Animated gradient blobs */}
          <div className={`absolute top-[-10%] right-[-10%] w-[80vw] h-[80vw] rounded-full bg-gradient-to-br from-${themeColor}-200/50 to-${themeColor}-100/30 blur-[150px] animate-pulse`}
               style={{ transform: `translate(${smoothMouse.x * -20}px, ${smoothMouse.y * 20}px)`, animationDuration: '4s' }} />
          <div className="absolute bottom-[-10%] left-[-10%] w-[80vw] h-[80vw] rounded-full bg-gradient-to-tr from-blue-200/40 to-purple-100/30 blur-[150px] animate-pulse"
               style={{ transform: `translate(${smoothMouse.x * 20}px, ${smoothMouse.y * -20}px)`, animationDuration: '5s' }} />
          <div className={`absolute top-[40%] left-[30%] w-[40vw] h-[40vw] rounded-full bg-gradient-to-r from-${themeColor}-100/40 to-white/60 blur-[120px] animate-pulse`}
               style={{ animationDuration: '6s' }} />

          {/* Floating particles */}
          {[...Array(12)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 rounded-full bg-gradient-to-br from-white to-slate-200 animate-particle"
              style={{
                left: `${(i * 8 + 10) % 90}%`,
                top: `${(i * 13 + 15) % 80}%`,
                animationDelay: `${i * 0.3}s`,
                animationDuration: `${4 + (i % 3)}s`
              }}
            />
          ))}
        </div>

        {/* Progress Bar */}
        <div className="absolute top-6 left-6 right-6 md:top-8 md:left-1/2 md:-translate-x-1/2 md:w-64 h-1.5 bg-slate-200/50 rounded-full overflow-hidden z-50 backdrop-blur-sm border border-slate-200/50">
          <div
            className={`h-full bg-gradient-to-r from-${themeColor}-500 to-blue-500 rounded-full transition-all duration-500 ease-out`}
            style={{ width: `${((step + 1) / totalSteps) * 100}%` }}
          />
        </div>

        {/* CSS Grid Stacking Context */}
        <div className={gridContainerClass}>
          {config.steps?.map((stepConfig, index) => (
            <div key={index} className={`${pageBaseClass} ${getPageStyle(index)}`}>
              {renderStep(stepConfig, index)}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
