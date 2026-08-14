import React, { useState, useEffect } from 'react';
import {
  Star, Shield, Key, Box, Eye, Search, Sparkles, RefreshCw,
  Layers, Cpu, BookOpen, CheckCircle2, XCircle, AlertTriangle,
  Code2, Globe, Users, Zap, Activity, Database, FileText
} from 'lucide-react';
import { markVideoReady, setVideoDuration } from './video-runtime.js';

// Design canvas constants
const DESIGN_WIDTH = 1200;
const DESIGN_HEIGHT = 1600;

// Responsive scaling
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

// Icon mapping
const ICON_MAP = {
  star: Star, shield: Shield, key: Key, box: Box, eye: Eye, search: Search,
  sparkles: Sparkles, refresh: RefreshCw, layers: Layers, cpu: Cpu,
  book: BookOpen, check: CheckCircle2, x: XCircle, alert: AlertTriangle,
  code: Code2, globe: Globe, users: Users, zap: Zap, activity: Activity,
  database: Database, file: FileText, 'alert-circle': AlertTriangle,
  'alert-triangle': AlertTriangle, 'x-circle': XCircle, 'check-circle': CheckCircle2,
  'mouse-pointer': Search, api: Database, brain: Sparkles, server: Database,
  'git-branch': Activity, package: Box, 'file-text': FileText, 'pen-tool': FileText,
  briefcase: Box, 'trending-up': Activity, rocket: Sparkles, 'arrow-right': RefreshCw,
  gem: Sparkles, target: Search, wand: Sparkles, download: RefreshCw, repeat: RefreshCw,
  link: Globe, filter: Search, layout: Layers, clock: Activity, settings: Cpu,
  'trending-up': Activity
};

// Glass Card Component
const GlassCard = ({ children, className = "" }) => (
  <div className={`rounded-[2.5rem] bg-white/70 backdrop-blur-3xl border border-white/60 shadow-[0_10px_40px_rgba(0,0,0,0.05)] ${className}`}>
    {children}
  </div>
);

// Script Footer
const ScriptFooter = ({ text }) => (
  <div className="absolute bottom-12 left-0 w-full flex justify-center z-50 px-12">
    <div className="rounded-full border border-white/80 bg-white/90 px-12 py-6 text-center shadow-[0_18px_42px_rgba(15,23,42,0.11)] backdrop-blur-2xl max-w-4xl">
      <div className="text-[1.5rem] font-medium leading-relaxed text-slate-700">
        {text}
      </div>
    </div>
  </div>
);

const KnowledgeVideoGenerator = ({ config }) => {
  const [step, setStep] = useState(0);
  const [smoothMouse, setSmoothMouse] = useState({ x: 0, y: 0 });

  const themeColor = config.themeColor || 'blue';
  const totalSteps = config.steps?.length || 1;

  useEffect(() => {
    const sceneDurations = config.sceneDurationsMs || [];
    if (sceneDurations.length === 0) return;

    let currentStep = 0;
    let elapsed = 0;

    const interval = setInterval(() => {
      elapsed += 100;
      const currentDuration = sceneDurations[currentStep] || 5000;

      if (elapsed >= currentDuration) {
        currentStep++;
        elapsed = 0;

        if (currentStep >= sceneDurations.length) {
          clearInterval(interval);
          const totalDuration = sceneDurations.reduce((a, b) => a + b, 0);
          setVideoDuration(totalDuration);
          markVideoReady();
        } else {
          setStep(currentStep);
        }
      }
    }, 100);

    return () => clearInterval(interval);
  }, [config.sceneDurationsMs]);

  const nextStep = () => {
    if (step < totalSteps - 1) {
      setStep(step + 1);
    }
  };

  const renderStep = (stepConfig, index) => {
    const StepIcon = ICON_MAP[stepConfig.icon] || Sparkles;

    switch (stepConfig.type) {
      case 'cover':
        return (
          <React.Fragment key={index}>
            {/* Header Badge */}
            <div className="text-center mb-8 animate-fadeInScale">
              <div className="inline-block bg-blue-100 text-blue-700 px-4 py-2 rounded-full text-xs font-black tracking-widest uppercase mb-6 shadow-sm border border-blue-200">
                {stepConfig.courseNumber} · {stepConfig.category}
              </div>

              {/* Project Name */}
              <h1 className="text-5xl md:text-6xl font-black tracking-tighter text-slate-900 mb-4 leading-tight">
                {config.project?.name || stepConfig.title}
              </h1>

              {/* Subtitle with gradient */}
              {stepConfig.subtitle && (
                <p className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-purple-600">
                  {stepConfig.subtitle}
                </p>
              )}
            </div>

            {/* Icon Card */}
            <GlassCard className="w-48 h-48 mx-auto mb-8 flex items-center justify-center animate-fadeInScale" style={{animationDelay: '0.2s'}}>
              <StepIcon className={`w-24 h-24 text-${themeColor}-600`} />
            </GlassCard>

            {/* Star Badge */}
            {stepConfig.badge && (
              <div className="flex justify-center mb-8 animate-fadeInScale" style={{animationDelay: '0.3s'}}>
                <div className="bg-white/80 backdrop-blur-xl border border-slate-200 px-6 py-3 rounded-full shadow-lg flex items-center gap-2">
                  <Star className="w-5 h-5 text-amber-500 fill-amber-500" />
                  <span className="font-bold text-slate-800">{stepConfig.badge}</span>
                </div>
              </div>
            )}

            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'pain_point':
        return (
          <React.Fragment key={index}>
            <div className="text-center mb-8">
              <div className="inline-block bg-red-100 text-red-700 px-4 py-2 rounded-full text-xs font-black tracking-widest uppercase mb-4">
                {stepConfig.badge || '痛点'}
              </div>
              <h2 className="text-4xl font-black text-slate-900">{stepConfig.title}</h2>
            </div>

            <div className="w-full max-w-3xl mx-auto grid gap-4">
              {stepConfig.visualizer?.items?.map((item, idx) => {
                const ItemIcon = ICON_MAP[item.icon] || AlertTriangle;
                return (
                  <GlassCard key={idx} className="p-6 animate-fadeInScale" style={{animationDelay: `${idx * 0.1}s`}}>
                    <div className="flex items-start gap-4">
                      <div className={`w-12 h-12 rounded-xl bg-${item.color}-50 text-${item.color}-600 flex items-center justify-center flex-shrink-0`}>
                        <ItemIcon size={24} />
                      </div>
                      <div>
                        <h4 className="font-bold text-slate-800 text-lg mb-1">{item.title}</h4>
                        <p className="text-sm text-slate-600">{item.description}</p>
                      </div>
                    </div>
                  </GlassCard>
                );
              })}
            </div>

            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'feature':
        return (
          <React.Fragment key={index}>
            <div className="text-center mb-8">
              <div className={`inline-block bg-${themeColor}-100 text-${themeColor}-700 px-4 py-2 rounded-full text-xs font-black tracking-widest uppercase mb-4`}>
                {stepConfig.badge || '核心功能'}
              </div>
              <h2 className="text-4xl font-black text-slate-900">{stepConfig.title}</h2>
            </div>

            <div className="w-full max-w-4xl mx-auto grid md:grid-cols-2 gap-4">
              {stepConfig.visualizer?.steps?.map((item, idx) => {
                const ItemIcon = ICON_MAP[item.icon] || Sparkles;
                return (
                  <GlassCard key={idx} className="p-6 animate-fadeInScale hover:-translate-y-2 transition-transform duration-300" style={{animationDelay: `${idx * 0.1}s`}}>
                    <div className={`w-12 h-12 rounded-xl bg-${item.color}-50 text-${item.color}-600 flex items-center justify-center mb-4`}>
                      <ItemIcon size={24} />
                    </div>
                    <h4 className="font-bold text-slate-800 text-lg mb-2">{item.title}</h4>
                    <p className="text-sm text-slate-600 leading-relaxed">{item.description}</p>
                  </GlassCard>
                );
              })}
            </div>

            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'golden_sentence':
        return (
          <React.Fragment key={index}>
            <div className="w-full max-w-3xl mx-auto">
              <GlassCard className="p-12 text-center animate-fadeInScale">
                <div className={`w-20 h-20 rounded-full bg-${themeColor}-50 text-${themeColor}-600 flex items-center justify-center mx-auto mb-6`}>
                  <StepIcon size={40} />
                </div>
                <h2 className="text-3xl font-black text-slate-900 mb-4">{stepConfig.title}</h2>
                <p className="text-xl text-slate-700 leading-relaxed font-medium">
                  {stepConfig.sentence || stepConfig.script}
                </p>
              </GlassCard>
            </div>

            <ScriptFooter text={stepConfig.script} />
          </React.Fragment>
        );

      case 'summary':
        return (
          <React.Fragment key={index}>
            <div className="w-full max-w-3xl mx-auto">
              <GlassCard className="p-12 text-center animate-fadeInScale">
                <div className={`w-20 h-20 rounded-full bg-${themeColor}-50 text-${themeColor}-600 flex items-center justify-center mx-auto mb-6`}>
                  <StepIcon size={40} />
                </div>
                <h2 className="text-3xl font-black text-slate-900 mb-8">{stepConfig.title}</h2>

                {stepConfig.points?.map((point, idx) => {
                  const PointIcon = ICON_MAP[point.icon] || CheckCircle2;
                  return (
                    <div key={idx} className="flex items-start gap-4 mb-4 text-left">
                      <div className={`w-10 h-10 rounded-lg bg-${point.color || themeColor}-50 text-${point.color || themeColor}-600 flex items-center justify-center flex-shrink-0`}>
                        <PointIcon size={20} />
                      </div>
                      <div>
                        <span className="font-bold text-slate-900">{point.title}：</span>
                        <span className="text-slate-700">{point.description}</span>
                      </div>
                    </div>
                  );
                })}
              </GlassCard>
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
        <style>{`
          @keyframes fadeInScale {
            from { opacity: 0; transform: translateY(10px) scale(0.98); }
            to { opacity: 1; transform: translateY(0) scale(1); }
          }
          .animate-fadeInScale {
            animation: fadeInScale 0.6s cubic-bezier(0.25, 1, 0.5, 1) both;
          }
        `}</style>

        {/* Background Blobs */}
        <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
          <div className="absolute top-[-10%] left-[-10%] w-[60vw] h-[60vw] rounded-full bg-blue-100/40 blur-[120px]" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[60vw] h-[60vw] rounded-full bg-purple-100/30 blur-[120px]" />
        </div>

        {/* Progress Bar */}
        <div className="absolute top-8 left-1/2 -translate-x-1/2 w-64 h-1.5 bg-slate-200/50 rounded-full overflow-hidden z-50 backdrop-blur-sm border border-slate-200/50">
          <div
            className={`h-full bg-gradient-to-r from-${themeColor}-500 to-blue-500 rounded-full transition-all duration-500 ease-out`}
            style={{ width: `${((step + 1) / totalSteps) * 100}%` }}
          />
        </div>

        {/* Content */}
        <div className="relative z-10 w-full h-full flex flex-col items-center justify-center p-12">
          {config.steps?.[step] && renderStep(config.steps[step], step)}
        </div>
      </div>
    </div>
  );
};

export default KnowledgeVideoGenerator;
