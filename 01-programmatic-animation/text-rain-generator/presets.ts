/**
 * 文字雨预设配置
 * 常见场景和参数组合
 */

export interface Preset {
  name: string;
  description: string;
  scene: string;
  speed: number;
  tilt: number;
  color: string;
  fontSize: number;
  canvasWidth: number;
  canvasHeight: number;
}

export const PRESETS: Record<string, Preset> = {
  // 江南风格
  jiangnan: {
    name: '江南烟雨',
    description: '细雨绵绵，诗意江南',
    scene: '江南水乡老宅，青瓦白墙，斑驳墙面，竹叶投影',
    speed: 2.0,
    tilt: 8,
    color: '#c9b8a3',
    fontSize: 22,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 北方风格
  beijing: {
    name: '北京胡同',
    description: '四合院屋檐，雨落青石板',
    scene: '北京四合院灰瓦屋檐，红砖墙面，古朴门楼',
    speed: 3.0,
    tilt: 12,
    color: '#d4c5a9',
    fontSize: 24,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 古寺风格
  temple: {
    name: '古寺钟声',
    description: '禅意空灵，梵音悠远',
    scene: '古寺飞檐，琉璃瓦，木质斗拱，香炉烟雾',
    speed: 1.8,
    tilt: 5,
    color: '#b8a88a',
    fontSize: 26,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 现代风格
  modern: {
    name: '都市夜雨',
    description: '霓虹灯影，现代诗意',
    scene: '现代建筑屋檐，玻璃幕墙倒影，城市夜景',
    speed: 3.5,
    tilt: 15,
    color: '#e8e8e8',
    fontSize: 20,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 雪花效果
  snow: {
    name: '飘雪',
    description: '雪落无声，银装素裹',
    scene: '冬日老宅，积雪屋顶，冰凌挂檐',
    speed: 1.2,
    tilt: 25,
    color: '#f0f0f0',
    fontSize: 28,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 快雨
  storm: {
    name: '暴雨如注',
    description: '狂风骤雨，气势磅礴',
    scene: '暴雨中的老宅，瓦片反光，雨雾朦胧',
    speed: 5.0,
    tilt: 30,
    color: '#b0b0b0',
    fontSize: 20,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 横屏模式（适合视频网站）
  landscape: {
    name: '横屏观影',
    description: '16:9 横屏格式，适合 B站/YouTube',
    scene: '传统中式建筑屋檐，横向构图',
    speed: 2.5,
    tilt: 10,
    color: '#d4c5a9',
    fontSize: 24,
    canvasWidth: 1920,
    canvasHeight: 1080,
  },

  // 正方形（适合社交媒体）
  square: {
    name: '社交媒体',
    description: '1:1 方形，适合 Instagram/微信',
    scene: '中式屋檐特写，对称构图',
    speed: 2.5,
    tilt: 10,
    color: '#d4c5a9',
    fontSize: 22,
    canvasWidth: 1080,
    canvasHeight: 1080,
  },

  // 徽派建筑
  huizhou: {
    name: '徽派建筑',
    description: '安徽徽派，马头墙，黑瓦白墙',
    scene: '徽派建筑马头墙，黑瓦白墙，木质雕花窗棂',
    speed: 2.2,
    tilt: 9,
    color: '#bfb5a3',
    fontSize: 23,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 岭南风格
  lingnan: {
    name: '岭南骑楼',
    description: '广州骑楼，民国风情',
    scene: '广州岭南骑楼，民国时期建筑，斑驳的白墙灰瓦',
    speed: 2.8,
    tilt: 12,
    color: '#d0c4b0',
    fontSize: 22,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 窑洞
  yaodong: {
    name: '陕北窑洞',
    description: '黄土高原，窑洞人家',
    scene: '陕北黄土窑洞，拱形门洞，黄土墙面',
    speed: 1.8,
    tilt: 6,
    color: '#c8b89a',
    fontSize: 24,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 川西民居
  sichuan: {
    name: '川西民居',
    description: '四川藏式碉楼，彩绘梁柱',
    scene: '川西藏式民居，彩绘木梁，石砌墙体，经幡飘扬',
    speed: 2.0,
    tilt: 8,
    color: '#d5c3a8',
    fontSize: 23,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 福建土楼
  tulou: {
    name: '福建土楼',
    description: '客家土楼，圆形建筑',
    scene: '福建客家土楼，圆形土墙，木质窗棂，天井中庭',
    speed: 2.3,
    tilt: 10,
    color: '#c4b49a',
    fontSize: 22,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 蒙古包
  yurt: {
    name: '草原蒙古包',
    description: '草原毡房，游牧文化',
    scene: '内蒙古草原蒙古包，白色毡房，蓝天白云',
    speed: 1.5,
    tilt: 15,
    color: '#e0d5c5',
    fontSize: 24,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 赛博朋克
  cyberpunk: {
    name: '赛博雨夜',
    description: '霓虹灯光，未来都市',
    scene: '赛博朋克城市夜景，霓虹灯招牌，玻璃幕墙反光',
    speed: 4.0,
    tilt: 20,
    color: '#00ffcc',
    fontSize: 20,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 竹林
  bamboo: {
    name: '竹林深处',
    description: '翠竹摇曳，清风徐来',
    scene: '竹林密布，竹叶投影，阳光斑驳',
    speed: 1.2,
    tilt: 5,
    color: '#b8d4a8',
    fontSize: 26,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 樱花
  sakura: {
    name: '樱花纷飞',
    description: '粉色樱花瓣飘落',
    scene: '日式木屋屋檐，樱花树枝条，粉色花瓣',
    speed: 1.0,
    tilt: 20,
    color: '#ffb6c1',
    fontSize: 22,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 沙漠
  desert: {
    name: '大漠孤烟',
    description: '西域戈壁，驼队商旅',
    scene: '新疆戈壁沙漠，土坯房屋，风沙痕迹',
    speed: 2.5,
    tilt: 25,
    color: '#d4a76a',
    fontSize: 23,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 极简黑白
  minimal: {
    name: '极简黑白',
    description: '纯黑白，现代简约',
    scene: '极简主义建筑，纯白墙面，几何线条，高对比',
    speed: 3.0,
    tilt: 0,
    color: '#ffffff',
    fontSize: 28,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },

  // 水墨
  ink: {
    name: '水墨意境',
    description: '泼墨山水，虚实结合',
    scene: '中国水墨画风格，山水屋舍，留白写意，墨色渲染',
    speed: 1.8,
    tilt: 8,
    color: '#808080',
    fontSize: 26,
    canvasWidth: 1080,
    canvasHeight: 1920,
  },
};

/**
 * 经典诗句示例
 */
export const EXAMPLE_POEMS = [
  // 李白
  '床前明月光，疑是地上霜。举头望明月，低头思故乡。',
  '朝辞白帝彩云间，千里江陵一日还。两岸猿声啼不住，轻舟已过万重山。',
  '故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。',

  // 杜甫
  '两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。',
  '国破山河在，城春草木深。感时花溅泪，恨别鸟惊心。',
  '迟日江山丽，春风花草香。泥融飞燕子，沙暖睡鸳鸯。',

  // 王维
  '空山新雨后，天气晚来秋。明月松间照，清泉石上流。',
  '红豆生南国，春来发几枝。愿君多采撷，此物最相思。',

  // 孟浩然
  '春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。',

  // 王之涣
  '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。',

  // 陆游
  '山重水复疑无路，柳暗花明又一村。',

  // 陶渊明
  '采菊东篱下，悠然见南山。山气日夕佳，飞鸟相与还。',

  // 韩愈
  '天街小雨润如酥，草色遥看近却无。',

  // 杜牧
  '清明时节雨纷纷，路上行人欲断魂。借问酒家何处有，牧童遥指杏花村。',
  '远上寒山石径斜，白云生处有人家。停车坐爱枫林晚，霜叶红于二月花。',

  // 白居易
  '离离原上草，一岁一枯荣。野火烧不尽，春风吹又生。',

  // 王勃
  '海内存知己，天涯若比邻。',

  // 苏轼
  '横看成岭侧成峰，远近高低各不同。不识庐山真面目，只缘身在此山中。',
  '大江东去，浪淘尽，千古风流人物。',

  // 辛弃疾
  '青山遮不住，毕竟东流去。',

  // 现代诗句（适合横屏）
  '我们都在阴沟里，但仍有人仰望星空。',
  '世界以痛吻我，我要报之以歌。',
];

/**
 * 根据诗句内容推荐预设
 */
export function recommendPreset(poemText: string): string {
  const text = poemText.toLowerCase();

  if (text.includes('雪') || text.includes('霜') || text.includes('冰')) {
    return 'snow';
  }
  if (text.includes('雨') || text.includes('湿')) {
    return 'jiangnan';
  }
  if (text.includes('寺') || text.includes('禅') || text.includes('僧')) {
    return 'temple';
  }
  if (text.includes('暴') || text.includes('狂') || text.includes('骤')) {
    return 'storm';
  }
  if (text.includes('城') || text.includes('楼') || text.includes('市')) {
    return 'modern';
  }
  if (text.includes('胡同') || text.includes('北') || text.includes('京')) {
    return 'beijing';
  }

  // 默认江南风格
  return 'jiangnan';
}

/**
 * 应用预设到配置
 */
export function applyPreset(presetName: string, baseConfig: any): any {
  const preset = PRESETS[presetName];
  if (!preset) {
    console.warn(`⚠️  未找到预设 "${presetName}"，使用默认配置`);
    return baseConfig;
  }

  return {
    ...baseConfig,
    scene: preset.scene,
    speed: preset.speed,
    tilt: preset.tilt,
    color: preset.color,
    fontSize: preset.fontSize,
    canvasWidth: preset.canvasWidth,
    canvasHeight: preset.canvasHeight,
  };
}
