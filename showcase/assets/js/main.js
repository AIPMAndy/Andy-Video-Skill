const SKILLS = [
  { name: 'andy-video-director', cat: '00 · Video Orchestration', desc: 'One request → route engines; stage complete BB-Video, Remotion and MoneyPrinterTurbo Skills' },
  { name: 'andy-manim-video', cat: '01 · Programmatic Animation', desc: '3Blue1Brown-style math & AI animations using Manim' },
  { name: 'andy-p5js', cat: '01 · Programmatic Animation', desc: 'Creative p5.js particle and generative art animations' },
  { name: 'andy-liquid', cat: '01 · Programmatic Animation', desc: 'Three.js liquid metal and 3D bloom cinematic effects' },
  { name: 'text-rain-generator', cat: '01 · Programmatic Animation', desc: 'Matrix-style text rain animation' },
  { name: 'andy-screencast-to-viral', cat: '02 · Recording-to-Video', desc: 'Long screen recordings → 100+ viral short videos' },
  { name: 'react-video', cat: '03 · Code-to-Video', desc: 'Render React components as MP4' },
  { name: 'react-content-generator', cat: '03 · Code-to-Video', desc: 'Apple-style React knowledge pages' },
  { name: 'ai-video-producer', cat: '03 · Code-to-Video', desc: 'AI-powered video production framework' },
  { name: 'dbs-script-flow', cat: '04 · Script & Planning', desc: 'Detect swipe-away risk in short-video scripts' },
  { name: 'duizhaochao-script-generator', cat: '04 · Script & Planning', desc: 'Generate viral copy-and-learn scripts' },
  { name: 'mrbeast-skill', cat: '04 · Script & Planning', desc: 'YouTube content creation via MrBeast methodology' },
  { name: 'andy-paper-collage-explainer', cat: '05 · Stylized Effects', desc: 'Paper-collage hand-crafted explainer style' },
];

const grid = document.getElementById('skill-grid');
SKILLS.forEach(s => {
  const card = document.createElement('a');
  card.href = `skills/${s.name}.html`;
  card.className = 'card';
  card.innerHTML = `
    <span class="category">${s.cat}</span>
    <h3>${s.name}</h3>
    <p>${s.desc}</p>
  `;
  grid.appendChild(card);
});