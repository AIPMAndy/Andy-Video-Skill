#!/bin/bash
# 快速示例脚本 - 一键生成经典诗句文字雨

SKILL_DIR="$HOME/.claude/skills/text-rain-generator"

echo "🌧️  Text Rain Generator - 快速示例"
echo ""
echo "选择一个经典诗句："
echo ""
echo "1. 床前明月光，疑是地上霜 (李白《静夜思》)"
echo "2. 春眠不觉晓，处处闻啼鸟 (孟浩然《春晓》)"
echo "3. 白日依山尽，黄河入海流 (王之涣《登鹳雀楼》)"
echo "4. 两个黄鹂鸣翠柳，一行白鹭上青天 (杜甫《绝句》)"
echo "5. 清明时节雨纷纷，路上行人欲断魂 (杜牧《清明》)"
echo "6. 空山新雨后，天气晚来秋 (王维《山居秋暝》)"
echo "7. 山重水复疑无路，柳暗花明又一村 (陆游《游山西村》)"
echo "8. 采菊东篱下，悠然见南山 (陶渊明《饮酒》)"
echo ""
read -p "请输入数字 (1-8): " choice

case $choice in
  1)
    POEM="床前明月光，疑是地上霜。举头望明月，低头思故乡。"
    PRESET="jiangnan"
    NAME="jingye-si"
    ;;
  2)
    POEM="春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。"
    PRESET="jiangnan"
    NAME="chun-xiao"
    ;;
  3)
    POEM="白日依山尽，黄河入海流。欲穷千里目，更上一层楼。"
    PRESET="beijing"
    NAME="deng-guan-que-lou"
    ;;
  4)
    POEM="两个黄鹂鸣翠柳，一行白鹭上青天。窗含西岭千秋雪，门泊东吴万里船。"
    PRESET="jiangnan"
    NAME="jue-ju"
    ;;
  5)
    POEM="清明时节雨纷纷，路上行人欲断魂。借问酒家何处有，牧童遥指杏花村。"
    PRESET="jiangnan"
    NAME="qing-ming"
    ;;
  6)
    POEM="空山新雨后，天气晚来秋。明月松间照，清泉石上流。"
    PRESET="bamboo"
    NAME="shan-ju-qiu-ming"
    ;;
  7)
    POEM="山重水复疑无路，柳暗花明又一村。"
    PRESET="jiangnan"
    NAME="you-shan-xi-cun"
    ;;
  8)
    POEM="采菊东篱下，悠然见南山。山气日夕佳，飞鸟相与还。"
    PRESET="jiangnan"
    NAME="yin-jiu"
    ;;
  *)
    echo "❌ 无效选择"
    exit 1
    ;;
esac

echo ""
echo "📝 生成项目: $NAME"
echo "🎨 预设: $PRESET"
echo ""

# 生成项目
cd "$SKILL_DIR" || exit 1
bun run cli.ts "$POEM" --preset "$PRESET" --output "$HOME/Documents/AICode/text-rain-examples/$NAME"

echo ""
echo "✅ 生成完成！"
echo ""
echo "⚠️  注意: 背景图需要通过 ChatGPT 生成"
echo "   任务包已保存到: image-task.json"
echo ""
echo "🚀 启动预览:"
echo "   cd $HOME/Documents/AICode/text-rain-examples/$NAME"
echo "   python3 -m http.server 8000"
echo "   open http://localhost:8000"
echo ""
