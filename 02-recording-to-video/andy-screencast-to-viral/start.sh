#!/bin/bash
#
# 10万粉丝冲刺 - 一键启动脚本
# 整合所有系统：生产 → 追踪 → 发布
#

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="/Users/andy/Documents/AICode/09 Andy-Video-SKill"
SOURCE_DIR="/Users/andy/Documents/Andy录屏素材库"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "========================================================================"
echo "  🚀 10万粉丝冲刺系统 - Andy录屏素材转爆款视频"
echo "========================================================================"
echo -e "${NC}"

# 菜单
show_menu() {
    echo ""
    echo "请选择操作："
    echo ""
    echo "  ${GREEN}1${NC}. 🎬 批量生产视频（5个测试 / 43个全量）"
    echo "  ${GREEN}2${NC}. 📊 查看生产进度"
    echo "  ${GREEN}3${NC}. 📋 生成发布计划清单"
    echo "  ${GREEN}4${NC}. 📈 查看数据报告"
    echo "  ${GREEN}5${NC}. 🔍 单个视频测试"
    echo "  ${GREEN}6${NC}. 📚 查看完整文档"
    echo "  ${GREEN}0${NC}. 🚪 退出"
    echo ""
    echo -n "选择 [0-6]: "
}

# 1. 批量生产
batch_production() {
    echo ""
    echo -e "${YELLOW}选择生产模式:${NC}"
    echo "  1. 测试模式（5个视频 × 3变体 = 15个）"
    echo "  2. 全量生产（43个视频 × 6变体 = 258个）"
    echo -n "选择 [1-2]: "
    read mode

    cd "$SCRIPT_DIR"

    if [ "$mode" == "1" ]; then
        echo -e "${GREEN}启动测试模式...${NC}"
        python3 mass_production.py
    elif [ "$mode" == "2" ]; then
        echo -e "${RED}⚠️  全量生产将生成258个视频，预计需要2-4小时${NC}"
        echo -n "确认开始？[y/N]: "
        read confirm
        if [ "$confirm" == "y" ] || [ "$confirm" == "Y" ]; then
            # 修改参数运行全量
            python3 -c "
import sys
sys.path.insert(0, '.')
from mass_production import MassProductionSystem
system = MassProductionSystem()
system.run_mass_production(max_videos=43, variants_per_video=6, duration=30)
"
        else
            echo "已取消"
        fi
    else
        echo "无效选择"
    fi
}

# 2. 查看进度
check_progress() {
    echo ""
    echo -e "${BLUE}📊 生产进度检查${NC}"
    echo "========================================"

    # 统计生成的视频
    output_dirs=(
        "$PROJECT_DIR/premium_output"
        "$PROJECT_DIR/viral_output"
        "$PROJECT_DIR/complete_viral_output"
        "$PROJECT_DIR/mass_production_output"
    )

    total=0
    for dir in "${output_dirs[@]}"; do
        if [ -d "$dir" ]; then
            count=$(find "$dir" -name "*.mp4" -type f 2>/dev/null | wc -l | tr -d ' ')
            echo "  $dir: $count 个视频"
            total=$((total + count))
        fi
    done

    echo "========================================"
    echo -e "${GREEN}总计生成: $total 个视频${NC}"
    echo ""

    # 检查是否有进程在运行
    if ps aux | grep -v grep | grep "mass_production.py" > /dev/null; then
        echo -e "${YELLOW}⏳ 批量生产进程正在运行中...${NC}"
        echo "查看实时日志: tail -f /tmp/mass_production.log"
    else
        echo -e "${GREEN}✅ 没有生产任务在运行${NC}"
    fi
}

# 3. 生成发布计划
generate_publish_plan() {
    echo ""
    echo -e "${BLUE}📋 生成发布计划${NC}"
    echo ""

    cd "$SCRIPT_DIR"
    python3 -c "
from auto_publisher import AutoPublisher
from data_tracker import ViralDataTracker

videos_dir = '$PROJECT_DIR/mass_production_output/temp'
tracker = ViralDataTracker('$PROJECT_DIR/tracking_data')
publisher = AutoPublisher(videos_dir, tracker)

# 生成30天计划
publisher.create_publish_queue(days=30)
publisher.export_manual_publish_checklist()

print('')
print('✅ 发布计划已生成！')
print('📁 文件位置: $PROJECT_DIR/mass_production_output/temp/manual_publish_checklist.csv')
print('')
print('使用方法:')
print('  1. 用Excel打开清单文件')
print('  2. 每天按清单发布6-8个视频')
print('  3. 发布时间: 12:00, 18:00, 21:00')
print('  4. 发布后记录数据到追踪系统')
"
}

# 4. 查看数据报告
view_report() {
    echo ""
    echo -e "${BLUE}📈 数据报告${NC}"
    echo ""

    cd "$SCRIPT_DIR"
    python3 -c "
from data_tracker import ViralDataTracker

tracker = ViralDataTracker('$PROJECT_DIR/tracking_data')
print(tracker.generate_report())

# Hook类型分析
hook_stats = tracker.analyze_hook_performance()
if hook_stats:
    print('\n🎯 Hook类型表现分析:')
    print('='*70)
    for hook_type, stats in sorted(hook_stats.items(), key=lambda x: x[1].get('avg_views', 0), reverse=True):
        print(f'\n  {hook_type}:')
        print(f'    发布数量: {stats[\"count\"]}')
        print(f'    平均播放: {stats.get(\"avg_views\", 0):,.0f}')
        print(f'    平均涨粉: {stats.get(\"avg_followers\", 0):.0f}')
        print(f'    平均完播率: {stats[\"avg_completion\"]*100:.1f}%')
        print(f'    爆款率: {stats.get(\"viral_rate\", 0)*100:.1f}%')
"
}

# 5. 单个视频测试
single_video_test() {
    echo ""
    echo -e "${BLUE}🔍 单个视频测试${NC}"
    echo ""

    # 列出源视频
    echo "源视频列表:"
    ls -1 "$SOURCE_DIR" | grep -E "\.mp4|\.mov" | head -10 | nl

    echo ""
    echo -n "输入视频序号 [1-10]: "
    read num

    video=$(ls -1 "$SOURCE_DIR" | grep -E "\.mp4|\.mov" | head -10 | sed -n "${num}p")

    if [ -z "$video" ]; then
        echo "无效序号"
        return
    fi

    echo ""
    echo "选择风格:"
    echo "  1. 完整爆款版（Hook动画 + 增强画面 + CTA）"
    echo "  2. 科技极简风"
    echo "  3. 赛博霓虹风"
    echo "  4. Apple商业风"
    echo -n "选择 [1-4]: "
    read style

    cd "$SCRIPT_DIR"

    if [ "$style" == "1" ]; then
        python3 -c "
from complete_viral_system import CompleteViralSystem
system = CompleteViralSystem('$PROJECT_DIR/test_output')
system.create_complete_viral_video(
    input_video='$SOURCE_DIR/$video',
    output_path='test_complete.mp4',
    hook_text='AI工具只需3秒',
    duration=30
)
"
        echo -e "${GREEN}✅ 生成完成: $PROJECT_DIR/test_output/test_complete.mp4${NC}"
    else
        echo "其他风格请使用 premium_editor_v2.py"
    fi
}

# 6. 查看文档
view_docs() {
    echo ""
    echo -e "${BLUE}📚 项目文档${NC}"
    echo ""
    echo "核心文档:"
    echo "  1. 10万粉丝策略: $PROJECT_DIR/10W_FOLLOWERS_STRATEGY.md"
    echo "  2. 爆款公式V2: $PROJECT_DIR/VIRAL_FORMULA_V2.md"
    echo "  3. 原始计划: $PROJECT_DIR/SCREENCAST_TO_VIRAL_PLAN.md"
    echo ""
    echo "核心代码:"
    echo "  1. 完整系统: $SCRIPT_DIR/complete_viral_system.py"
    echo "  2. 批量生产: $SCRIPT_DIR/mass_production.py"
    echo "  3. 数据追踪: $SCRIPT_DIR/data_tracker.py"
    echo "  4. 自动发布: $SCRIPT_DIR/auto_publisher.py"
    echo ""
    echo -n "按回车继续..."
    read
}

# 主循环
while true; do
    show_menu
    read choice

    case $choice in
        1) batch_production ;;
        2) check_progress ;;
        3) generate_publish_plan ;;
        4) view_report ;;
        5) single_video_test ;;
        6) view_docs ;;
        0)
            echo ""
            echo -e "${GREEN}🎯 记住目标: 10万粉丝！${NC}"
            echo "加油！💪"
            echo ""
            exit 0
            ;;
        *)
            echo -e "${RED}无效选择${NC}"
            ;;
    esac

    echo ""
    echo -n "按回车继续..."
    read
done
