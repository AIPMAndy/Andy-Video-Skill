import { useEffect, useMemo, useState } from "react";
import { markVideoReady, setVideoDuration } from "./video-runtime";

export const DESIGN_WIDTH = 1200;
export const DESIGN_HEIGHT = 1600;

export function pace(ms, speedMultiplier = 1) {
  return Math.round(ms / speedMultiplier);
}

export function useStageScale() {
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const update = () => {
      setScale(
        Math.min(
          window.innerWidth / DESIGN_WIDTH,
          window.innerHeight / DESIGN_HEIGHT,
        ),
      );
    };

    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  return scale;
}

export function useAutoplayScenes(sceneDurationsMs, options = {}) {
  const {
    readyDelayMs = 650,
    speedMultiplier = 1,
  } = options;
  const [step, setStep] = useState(0);
  const [isReady, setIsReady] = useState(false);

  const pacedDurations = useMemo(
    () => sceneDurationsMs.map((value) => pace(value, speedMultiplier)),
    [sceneDurationsMs, speedMultiplier],
  );

  useEffect(() => {
    setVideoDuration(pacedDurations.reduce((sum, value) => sum + value, 0));
    const timer = window.setTimeout(() => {
      setIsReady(true);
      markVideoReady();
    }, pace(readyDelayMs, speedMultiplier));
    return () => window.clearTimeout(timer);
  }, [pacedDurations, readyDelayMs, speedMultiplier]);

  useEffect(() => {
    if (!isReady) {
      return;
    }
    let elapsed = 0;
    const timers = pacedDurations.slice(0, -1).map((duration, index) => {
      elapsed += duration;
      return window.setTimeout(() => {
        setStep(index + 1);
      }, elapsed);
    });

    return () => timers.forEach((timer) => window.clearTimeout(timer));
  }, [isReady, pacedDurations]);

  return {
    step,
    isReady,
    totalSteps: pacedDurations.length,
  };
}

export function GlassCard({ children, className = "", style = {} }) {
  return (
    <div
      style={style}
      className={`
        relative overflow-hidden rounded-[2.5rem] bg-white/74 backdrop-blur-3xl
        border border-white/70 shadow-[0_16px_52px_rgba(15,23,42,0.05)]
        transition-all duration-500 ease-[cubic-bezier(0.25,1,0.5,1)]
        ${className}
      `}
    >
      <div className="relative z-10 h-full">{children}</div>
      <div className="pointer-events-none absolute left-0 top-0 h-1/2 w-full bg-gradient-to-b from-white/95 to-transparent opacity-90" />
      <div className="pointer-events-none absolute bottom-0 right-0 h-2/3 w-2/3 rounded-[2.5rem] bg-gradient-to-t from-slate-50/50 to-transparent" />
    </div>
  );
}

export function ScriptFooter({ text }) {
  return (
    <div className="pointer-events-none absolute bottom-7 left-0 z-50 flex w-full justify-center px-6">
      <div className="w-[96%] max-w-[74rem] rounded-[2.95rem] border border-white/80 bg-white/90 px-[3.25rem] py-[1.9rem] text-center shadow-[0_18px_42px_rgba(15,23,42,0.11)] backdrop-blur-2xl animate-slideInUp">
        <div className="text-[1.62rem] font-bold leading-[1.54] tracking-[0.012em] text-slate-800">
          {text}
        </div>
      </div>
    </div>
  );
}
