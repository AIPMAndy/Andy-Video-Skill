#!/usr/bin/env python3
"""
自动发布系统 - 定时发布到抖音/B站/小红书
集成数据追踪，自动记录发布信息
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import schedule
import time

from data_tracker import ViralDataTracker


class AutoPublisher:
    """自动发布系统"""

    def __init__(
        self,
        videos_dir: str,
        tracker: ViralDataTracker,
        schedule_config: str = None
    ):
        self.videos_dir = Path(videos_dir)
        self.tracker = tracker
        self.schedule_config = schedule_config or self._default_schedule()

        self.publish_queue = []
        self.published_videos = set()

    def _default_schedule(self) -> Dict:
        """默认发布时间表"""
        return {
            "douyin": [
                {"time": "12:00", "count": 2},  # 午间2条
                {"time": "18:00", "count": 2},  # 晚饭2条
                {"time": "21:00", "count": 2}   # 睡前2条
            ],
            "bilibili": [
                {"time": "20:00", "count": 1},
                {"time": "22:00", "count": 1}
            ],
            "xiaohongshu": [
                {"time": "10:00", "count": 1},
                {"time": "15:00", "count": 1},
                {"time": "20:00", "count": 1}
            ]
        }

    def scan_videos(self) -> List[Path]:
        """扫描待发布的视频"""
        videos = []
        for ext in ["*.mp4", "*.mov"]:
            videos.extend(self.videos_dir.glob(f"**/{ext}"))

        # 过滤已发布
        unpublished = [
            v for v in videos
            if str(v) not in self.published_videos
        ]

        return sorted(unpublished)

    def create_publish_queue(self, days: int = 30):
        """
        创建发布队列
        根据视频数量和发布频率，自动分配发布时间
        """
        videos = self.scan_videos()
        print(f"📊 扫描到 {len(videos)} 个待发布视频")

        queue = []
        video_idx = 0

        for day in range(days):
            publish_date = datetime.now() + timedelta(days=day)

            # 每天的发布计划
            for platform, slots in self.schedule_config.items():
                for slot in slots:
                    hour, minute = map(int, slot["time"].split(":"))
                    count = slot["count"]

                    for _ in range(count):
                        if video_idx >= len(videos):
                            break

                        publish_time = publish_date.replace(
                            hour=hour,
                            minute=minute,
                            second=0
                        )

                        queue.append({
                            "video_path": str(videos[video_idx]),
                            "platform": platform,
                            "scheduled_time": publish_time.isoformat(),
                            "status": "pending"
                        })

                        video_idx += 1

                    if video_idx >= len(videos):
                        break

                if video_idx >= len(videos):
                    break

            if video_idx >= len(videos):
                break

        self.publish_queue = queue

        # 保存队列
        queue_path = self.videos_dir / "publish_queue.json"
        with open(queue_path, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)

        print(f"✅ 发布队列已创建: {len(queue)} 个任务")
        print(f"📅 覆盖天数: {day + 1} 天")
        print(f"📁 队列文件: {queue_path}")

        return queue

    def publish_to_douyin(self, video_path: str, title: str, tags: List[str]) -> Dict:
        """
        发布到抖音
        注意：这是模拟代码，实际需要使用抖音开放平台API或自动化工具
        """
        print(f"📱 正在发布到抖音...")
        print(f"   视频: {Path(video_path).name}")
        print(f"   标题: {title}")
        print(f"   标签: {', '.join(tags)}")

        # TODO: 实际发布逻辑
        # 方案1: 使用抖音开放平台API（需要企业认证）
        # 方案2: 使用自动化工具（pyautogui + 截图识别）
        # 方案3: 手动发布（导出发布清单，人工上传）

        return {
            "success": True,
            "platform_url": f"https://www.douyin.com/video/{int(time.time())}",
            "message": "模拟发布成功（实际需要对接API）"
        }

    def generate_title_and_tags(self, video_path: str) -> tuple:
        """从视频文件名生成标题和标签"""
        filename = Path(video_path).stem

        # 提取Hook文本作为标题
        # 假设文件名格式: "原视频名_v1.mp4"
        # Hook信息需要从metadata或者数据库中获取

        title = filename[:30]  # 抖音标题限制

        # 默认标签
        tags = ["AI工具", "效率神器", "黑科技", "实用技巧"]

        return title, tags

    def publish_video(self, task: Dict) -> bool:
        """发布单个视频"""
        video_path = task["video_path"]
        platform = task["platform"]

        print(f"\n{'='*70}")
        print(f"🚀 开始发布")
        print(f"{'='*70}")
        print(f"📹 视频: {Path(video_path).name}")
        print(f"📱 平台: {platform}")
        print(f"⏰ 计划时间: {task['scheduled_time']}")

        title, tags = self.generate_title_and_tags(video_path)

        try:
            if platform == "douyin":
                result = self.publish_to_douyin(video_path, title, tags)
            elif platform == "bilibili":
                result = {"success": True, "platform_url": "https://bilibili.com/xxx"}
            elif platform == "xiaohongshu":
                result = {"success": True, "platform_url": "https://xiaohongshu.com/xxx"}
            else:
                result = {"success": False, "message": "未知平台"}

            if result["success"]:
                # 注册到数据追踪系统
                video_id = self.tracker.register_video(
                    video_path=video_path,
                    hook_type="自动识别",
                    hook_text=title,
                    platform=platform
                )

                self.tracker.mark_published(
                    video_id=video_id,
                    platform_url=result.get("platform_url", "")
                )

                self.published_videos.add(video_path)

                print(f"✅ 发布成功")
                print(f"🔗 链接: {result.get('platform_url', 'N/A')}")
                print(f"📊 已注册到数据追踪系统: {video_id}")

                return True
            else:
                print(f"❌ 发布失败: {result.get('message', '未知错误')}")
                return False

        except Exception as e:
            print(f"❌ 发布异常: {str(e)}")
            return False

    def export_manual_publish_checklist(self, output_path: str = None):
        """
        导出手动发布清单
        如果API不可用，可以导出Excel，人工按清单发布
        """
        if output_path is None:
            output_path = self.videos_dir / "manual_publish_checklist.csv"

        import csv

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=[
                "序号", "视频文件", "平台", "发布日期", "发布时间", "建议标题", "建议标签", "已发布"
            ])
            writer.writeheader()

            for i, task in enumerate(self.publish_queue, 1):
                video_name = Path(task["video_path"]).name
                dt = datetime.fromisoformat(task["scheduled_time"])
                title, tags = self.generate_title_and_tags(task["video_path"])

                writer.writerow({
                    "序号": i,
                    "视频文件": video_name,
                    "平台": task["platform"],
                    "发布日期": dt.strftime("%Y-%m-%d"),
                    "发布时间": dt.strftime("%H:%M"),
                    "建议标题": title,
                    "建议标签": ", ".join(tags),
                    "已发布": ""
                })

        print(f"✅ 手动发布清单已导出: {output_path}")
        print(f"📋 请使用Excel打开，按清单逐个发布视频")

    def run_scheduled_publisher(self):
        """
        运行定时发布器
        注意：这需要一直运行，建议用screen或tmux
        """
        print("🤖 自动发布器启动")
        print("⏰ 按队列定时发布视频...")

        # 检查是否有到期任务
        def check_and_publish():
            now = datetime.now()

            for task in self.publish_queue:
                if task["status"] != "pending":
                    continue

                scheduled_time = datetime.fromisoformat(task["scheduled_time"])

                # 如果到时间了（容差1分钟）
                if abs((now - scheduled_time).total_seconds()) < 60:
                    success = self.publish_video(task)
                    task["status"] = "published" if success else "failed"

        # 每分钟检查一次
        schedule.every(1).minutes.do(check_and_publish)

        print("✅ 定时器已设置，等待发布时间...")

        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == "__main__":
    print("="*70)
    print("自动发布系统 - 使用说明")
    print("="*70)
    print()
    print("🎯 功能:")
    print("  1. 扫描待发布视频")
    print("  2. 自动生成发布时间表")
    print("  3. 导出手动发布清单（推荐）")
    print("  4. 自动定时发布（需API对接）")
    print()
    print("📋 推荐流程:")
    print("  1. 运行此脚本生成发布清单")
    print("  2. 打开清单Excel文件")
    print("  3. 每天按清单手动发布6-8个视频")
    print("  4. 发布后在抖音后台查看数据")
    print("  5. 将数据手动填入data_tracker.py")
    print()
    print("="*70)

    # 示例使用
    videos_dir = "/Users/andy/Documents/AICode/09 Andy-Video-SKill/mass_production_output/temp"
    tracker = ViralDataTracker("/Users/andy/Documents/AICode/09 Andy-Video-SKill/tracking_data")

    publisher = AutoPublisher(videos_dir, tracker)

    # 生成30天发布计划
    publisher.create_publish_queue(days=30)

    # 导出手动发布清单
    publisher.export_manual_publish_checklist()

    print("\n✅ 发布计划已准备完成！")
    print("📁 查看文件: manual_publish_checklist.csv")
