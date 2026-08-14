/**
 * 音效增强模块
 * 为文字雨添加环境音效（雨声、风声、钟声等）
 */

export interface SoundConfig {
  enabled: boolean;
  rainSound?: string;
  ambientSound?: string;
  volume: number;
  fadeIn: boolean;
  fadeInDuration: number;
}

export const DEFAULT_SOUND_CONFIG: SoundConfig = {
  enabled: false,
  volume: 0.3,
  fadeIn: true,
  fadeInDuration: 2000,
};

/**
 * 预设音效资源（CDN）
 */
export const SOUND_PRESETS = {
  rain: {
    light: 'https://cdn.freesound.org/previews/416/416710_5121236-lq.mp3', // 轻雨
    medium: 'https://cdn.freesound.org/previews/393/393398_7277193-lq.mp3', // 中雨
    heavy: 'https://cdn.freesound.org/previews/465/465423_9336374-lq.mp3', // 暴雨
  },
  ambient: {
    nature: 'https://cdn.freesound.org/previews/406/406113_7255534-lq.mp3', // 自然环境
    temple: 'https://cdn.freesound.org/previews/244/244985_1015240-lq.mp3', // 寺庙钟声
    bamboo: 'https://cdn.freesound.org/previews/456/456966_9258921-lq.mp3', // 竹林风声
    snow: 'https://cdn.freesound.org/previews/391/391660_6849142-lq.mp3', // 雪地
  },
};

/**
 * 生成增强版 sketch.js（包含音效）
 */
export function generateSketchWithSound(
  baseSketch: string,
  soundConfig: SoundConfig
): string {
  if (!soundConfig.enabled) {
    return baseSketch;
  }

  // 在 preload 函数中添加音效加载
  const soundLoadCode = `
// 音效加载
let rainSound, ambientSound;

function preload() {
  backgroundImg = loadImage('assets/background.png');

  ${soundConfig.rainSound ? `rainSound = loadSound('${soundConfig.rainSound}');` : ''}
  ${soundConfig.ambientSound ? `ambientSound = loadSound('${soundConfig.ambientSound}');` : ''}
}
`;

  // 在 setup 函数中添加音效初始化
  const soundSetupCode = `
  // 音效初始化
  ${
    soundConfig.rainSound
      ? `
  if (rainSound) {
    rainSound.setVolume(${soundConfig.volume});
    rainSound.loop();
    ${
      soundConfig.fadeIn
        ? `
    rainSound.setVolume(0);
    setTimeout(() => {
      rainSound.fade(${soundConfig.volume}, ${soundConfig.fadeInDuration});
    }, 500);
    `
        : ''
    }
  }
  `
      : ''
  }

  ${
    soundConfig.ambientSound
      ? `
  if (ambientSound) {
    ambientSound.setVolume(${soundConfig.volume * 0.7});
    ambientSound.loop();
    ${
      soundConfig.fadeIn
        ? `
    ambientSound.setVolume(0);
    setTimeout(() => {
      ambientSound.fade(${soundConfig.volume * 0.7}, ${soundConfig.fadeInDuration});
    }, 1000);
    `
        : ''
    }
  }
  `
      : ''
  }
`;

  // 添加静音/取消静音控制
  const soundControlCode = `
// 音效控制
let isMuted = false;

function keyPressed() {
  // ... 原有键盘控制代码 ...

  // M 键静音/取消静音
  if (key === 'm' || key === 'M') {
    isMuted = !isMuted;
    if (isMuted) {
      if (rainSound) rainSound.setVolume(0);
      if (ambientSound) ambientSound.setVolume(0);
    } else {
      if (rainSound) rainSound.setVolume(${soundConfig.volume});
      if (ambientSound) ambientSound.setVolume(${soundConfig.volume * 0.7});
    }
  }
}
`;

  // 替换原有代码
  let enhanced = baseSketch
    .replace(/function preload\(\) \{[^}]+\}/, soundLoadCode.trim())
    .replace(/console\.log\(`✅ 初始化完成[^`]+`\);/, soundSetupCode.trim() + '\n\n  console.log(`✅ 初始化完成: ${particles.length} 个粒子`);');

  // 如果没有 keyPressed 函数，添加完整的
  if (!enhanced.includes('function keyPressed()')) {
    enhanced += '\n\n' + soundControlCode;
  } else {
    // 在现有 keyPressed 中添加静音控制
    enhanced = enhanced.replace(
      /if \(key === ' '\) \{[\s\S]*?\}/,
      match =>
        match +
        `

  // M 键静音/取消静音
  if (key === 'm' || key === 'M') {
    isMuted = !isMuted;
    if (isMuted) {
      if (rainSound) rainSound.setVolume(0);
      if (ambientSound) ambientSound.setVolume(0);
    } else {
      if (rainSound) rainSound.setVolume(${soundConfig.volume});
      if (ambientSound) ambientSound.setVolume(${soundConfig.volume * 0.7});
    }
  }
`
    );
  }

  return enhanced;
}

/**
 * 根据预设推荐音效
 */
export function recommendSound(presetName: string): SoundConfig {
  const recommendations: Record<string, SoundConfig> = {
    jiangnan: {
      enabled: true,
      rainSound: SOUND_PRESETS.rain.light,
      ambientSound: SOUND_PRESETS.ambient.nature,
      volume: 0.25,
      fadeIn: true,
      fadeInDuration: 3000,
    },
    storm: {
      enabled: true,
      rainSound: SOUND_PRESETS.rain.heavy,
      volume: 0.4,
      fadeIn: true,
      fadeInDuration: 2000,
    },
    temple: {
      enabled: true,
      rainSound: SOUND_PRESETS.rain.light,
      ambientSound: SOUND_PRESETS.ambient.temple,
      volume: 0.2,
      fadeIn: true,
      fadeInDuration: 4000,
    },
    bamboo: {
      enabled: true,
      rainSound: SOUND_PRESETS.rain.light,
      ambientSound: SOUND_PRESETS.ambient.bamboo,
      volume: 0.25,
      fadeIn: true,
      fadeInDuration: 3000,
    },
    snow: {
      enabled: true,
      ambientSound: SOUND_PRESETS.ambient.snow,
      volume: 0.15,
      fadeIn: true,
      fadeInDuration: 5000,
    },
  };

  return recommendations[presetName] || DEFAULT_SOUND_CONFIG;
}

/**
 * 下载音效文件到本地（可选）
 */
export async function downloadSounds(
  soundConfig: SoundConfig,
  outputDir: string
): Promise<SoundConfig> {
  // 注：实际下载需要使用 fetch 或其他 HTTP 库
  // 这里只返回配置，实际实现需要在 Node.js 环境中完成
  console.log('⚠️  音效下载功能需要在完整环境中实现');
  return soundConfig;
}
