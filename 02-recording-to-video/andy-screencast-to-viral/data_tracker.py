#!/usr/bin/env python3
"""
数据追踪系统 - 监控每个视频的表现，自动识别爆款
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import csv


class ViralDataTracker:
    """爆款数据追踪器"""

    def __init__(self, data_dir: str = "./tracking_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.data_dir / "videos_database.json"
        self.db = self._load_db()

    def _load_db(self) -> Dict:
        """加载数据库"""
        if self.db_path.exists():
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"videos": [], "summary": {}}

    def _save_db(self):
        """保存数据库"""
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(self.db, f, ensure_ascii=False, indent=2)

    def register_video(
        self,
        video_path: str,
        hook_type: str,
        hook_text: str,
        platform: str = "douyin",
        source_video: str = ""
    ) -> str:
        """注册一个新视频"""
        video_id = f"{Path(video_path).stem}"

        video_data = {
            "video_id": video_id,
            "file_path": video_path,
            "hook_type": hook_type,
            "hook_text": hook_text,
            "platform": platform,
            "source_video": source_video,
            "created_at": datetime.now().isoformat(),
            "published_at": None,
            "status": "generated",  # generated, published, viral, failed

            # 数据指标
            "views": 0,
            "likes": 0,
            "comments": 0,
            "shares": 0,
            "followers_gain": 0,

            # 算法指标
            "ctr": 0.0,
            "completion_rate": 0.0,
            "avg_watch_time": 0.0,
            "engagement_rate": 0.0,

            # 爆款得分
            "viral_score": 0.0,
            "viral_level": "unknown"  # unknown, failed, normal, good, viral, super_viral
        }

        self.db["videos"].append(video_data)
        self._save_db()

        return video_id

    def update_video_data(
        self,
        video_id: str,
        views: Optional[int] = None,
        likes: Optional[int] = None,
        comments: Optional[int] = None,
        shares: Optional[int] = None,
        followers_gain: Optional[int] = None,
        completion_rate: Optional[float] = None
    ):
        """更新视频数据"""
        for video in self.db["videos"]:
            if video["video_id"] == video_id:
                if views is not None:
                    video["views"] = views
                if likes is not None:
                    video["likes"] = likes
                if comments is not None:
                    video["comments"] = comments
                if shares is not None:
                    video["shares"] = shares
                if followers_gain is not None:
                    video["followers_gain"] = followers_gain
                if completion_rate is not None:
                    video["completion_rate"] = completion_rate

                # 计算派生指标
                if video["views"] > 0:
                    video["engagement_rate"] = (
                        (video["likes"] + video["comments"] + video["shares"])
                        / video["views"]
                    )

                # 计算爆款得分
                video["viral_score"] = self._calculate_viral_score(video)
                video["viral_level"] = self._classify_viral_level(video)

                self._save_db()
                return True

        return False

    def _calculate_viral_score(self, video: Dict) -> float:
        """
        计算爆款得分
        公式: (完播率 × 0.4) + (互动率 × 0.3) + (涨粉率 × 0.3)
        """
        if video["views"] == 0:
            return 0.0

        completion_score = video["completion_rate"] * 0.4
        engagement_score = video["engagement_rate"] * 0.3

        # 涨粉率（每1000播放涨粉数）
        follower_rate = (video["followers_gain"] / video["views"]) * 1000 if video["views"] > 0 else 0
        follower_score = min(follower_rate / 10, 1.0) * 0.3  # 标准化到0-1

        return completion_score + engagement_score + follower_score

    def _classify_viral_level(self, video: Dict) -> str:
        """分类爆款等级"""
        views = video["views"]
        completion_rate = video["completion_rate"]
        followers_gain = video["followers_gain"]

        # 超级爆款
        if views >= 1000000 and completion_rate >= 0.6 and followers_gain >= 1000:
            return "super_viral"

        # 爆款
        if views >= 100000 and completion_rate >= 0.45 and followers_gain >= 100:
            return "viral"

        # 优质
        if views >= 10000 and completion_rate >= 0.35:
            return "good"

        # 普通
        if views >= 1000 and completion_rate >= 0.25:
            return "normal"

        # 失败
        if views < 1000 or completion_rate < 0.25:
            return "failed"

        return "unknown"

    def mark_published(self, video_id: str, platform_url: str = ""):
        """标记视频已发布"""
        for video in self.db["videos"]:
            if video["video_id"] == video_id:
                video["status"] = "published"
                video["published_at"] = datetime.now().isoformat()
                video["platform_url"] = platform_url
                self._save_db()
                return True
        return False

    def get_top_performers(self, n: int = 10, metric: str = "viral_score") -> List[Dict]:
        """获取表现最好的N个视频"""
        published = [v for v in self.db["videos"] if v["status"] == "published"]
        sorted_videos = sorted(published, key=lambda x: x.get(metric, 0), reverse=True)
        return sorted_videos[:n]

    def get_viral_videos(self) -> List[Dict]:
        """获取所有爆款视频"""
        return [v for v in self.db["videos"] if v["viral_level"] in ["viral", "super_viral"]]

    def generate_report(self) -> str:
        """生成数据报告"""
        videos = self.db["videos"]
        published = [v for v in videos if v["status"] == "published"]

        if not published:
            return "❌ 暂无已发布视频数据"

        total_views = sum(v["views"] for v in published)
        total_followers = sum(v["followers_gain"] for v in published)
        avg_completion = sum(v["completion_rate"] for v in published) / len(published)

        # 统计各级别视频数量
        level_counts = {}
        for v in published:
            level = v["viral_level"]
            level_counts[level] = level_counts.get(level, 0) + 1

        report = f"""
{'='*70}
📊 视频数据报告
{'='*70}

📹 视频统计:
   总生成: {len(videos)} 个
   已发布: {len(published)} 个
   待发布: {len(videos) - len(published)} 个

📈 整体数据:
   总播放量: {total_views:,}
   总涨粉数: {total_followers:,}
   平均完播率: {avg_completion*100:.1f}%
   平均转粉率: {total_followers/total_views*100:.3f}% (每100播放涨粉数)

🏆 视频分级:
   🔥 超级爆款: {level_counts.get('super_viral', 0)} 个
   ✨ 爆款: {level_counts.get('viral', 0)} 个
   ✅ 优质: {level_counts.get('good', 0)} 个
   ⚠️  普通: {level_counts.get('normal', 0)} 个
   ❌ 失败: {level_counts.get('failed', 0)} 个

🎯 Top 5 表现最佳:
"""

        top_5 = self.get_top_performers(5)
        for i, v in enumerate(top_5, 1):
            report += f"""
   {i}. {v['hook_text']}
      播放: {v['views']:,} | 涨粉: {v['followers_gain']} | 完播率: {v['completion_rate']*100:.1f}%
      爆款得分: {v['viral_score']:.3f} | 等级: {v['viral_level']}
"""

        report += f"\n{'='*70}\n"

        # 保存报告
        report_path = self.data_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)

        return report

    def export_to_csv(self, output_path: str = None):
        """导出为CSV供Excel分析"""
        if output_path is None:
            output_path = self.data_dir / "videos_data.csv"

        with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
            if not self.db["videos"]:
                return

            writer = csv.DictWriter(f, fieldnames=self.db["videos"][0].keys())
            writer.writeheader()
            writer.writerows(self.db["videos"])

        print(f"✅ 数据已导出: {output_path}")

    def analyze_hook_performance(self) -> Dict:
        """分析不同Hook类型的表现"""
        hook_stats = {}

        for video in self.db["videos"]:
            if video["status"] != "published":
                continue

            hook_type = video["hook_type"]
            if hook_type not in hook_stats:
                hook_stats[hook_type] = {
                    "count": 0,
                    "total_views": 0,
                    "total_followers": 0,
                    "avg_completion": 0.0,
                    "viral_count": 0
                }

            stats = hook_stats[hook_type]
            stats["count"] += 1
            stats["total_views"] += video["views"]
            stats["total_followers"] += video["followers_gain"]
            stats["avg_completion"] += video["completion_rate"]

            if video["viral_level"] in ["viral", "super_viral"]:
                stats["viral_count"] += 1

        # 计算平均值
        for hook_type, stats in hook_stats.items():
            if stats["count"] > 0:
                stats["avg_completion"] /= stats["count"]
                stats["avg_views"] = stats["total_views"] / stats["count"]
                stats["avg_followers"] = stats["total_followers"] / stats["count"]
                stats["viral_rate"] = stats["viral_count"] / stats["count"]

        return hook_stats


if __name__ == "__main__":
    # 测试代码
    tracker = ViralDataTracker("/Users/andy/Documents/AICode/09 Andy-Video-SKill/tracking_data")

    # 示例：注册视频
    video_id = tracker.register_video(
        video_path="/path/to/video.mp4",
        hook_type="数字冲击",
        hook_text="3秒做1000元壁纸",
        platform="douyin"
    )

    print(f"✅ 视频已注册: {video_id}")

    # 示例：更新数据
    tracker.update_video_data(
        video_id=video_id,
        views=50000,
        likes=2500,
        comments=150,
        shares=80,
        followers_gain=250,
        completion_rate=0.55
    )

    # 生成报告
    print(tracker.generate_report())

    # 导出CSV
    tracker.export_to_csv()
