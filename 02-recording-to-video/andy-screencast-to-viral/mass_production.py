#!/usr/bin/env python3
"""
批量生产系统 - 43个视频 × 6种Hook变体 = 258个爆款视频
自动化生产线，达到10万粉丝的规模化方案
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict
import sys
import os

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from complete_viral_system import CompleteViralSystem


class MassProductionSystem:
    """大规模生产系统"""

    def __init__(self):
        self.source_dir = Path("/Users/andy/Documents/Andy录屏素材库")
        self.output_dir = Path("/Users/andy/Documents/AICode/09 Andy-Video-SKill/mass_production_output")
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Hook模板（6种爆款公式）
        self.hook_templates = [
            "{keyword}只需3秒",           # 数字冲击
            "{keyword}太强了",            # 情绪爆发
            "终于发现{keyword}的秘密",    # 秘密揭露
            "{keyword}效果惊人",          # 结果展示
            "99%的人不知道的{keyword}",  # 稀缺性
            "用{keyword}做1000元效果"     # 价值对比
        ]

        # CTA模板
        self.cta_templates = [
            "关注我，每天分享AI神器",
            "点赞收藏，下次就找不到了",
            "评论区告诉我你想学什么"
        ]

        self.viral_system = CompleteViralSystem(str(self.output_dir / "temp"))

    def get_all_videos(self) -> List[Path]:
        """获取所有视频文件"""
        videos = []
        for ext in ["*.mp4", "*.mov", "*.MP4", "*.MOV"]:
            videos.extend(self.source_dir.glob(ext))
        return sorted(videos)

    def extract_keyword_from_filename(self, filename: str) -> str:
        """从文件名提取关键词"""
        # 简单处理：去除扩展名和日期时间
        name = Path(filename).stem

        # 常见关键词映射
        keyword_map = {
            "GPT": "AI壁纸",
            "录屏": "录屏技巧",
            "Display": "屏幕录制",
            "Retina": "高清录屏"
        }

        for key, value in keyword_map.items():
            if key in name:
                return value

        # 默认关键词
        return "AI工具"

    def generate_batch_variants(
        self,
        video_path: Path,
        num_variants: int = 6,
        duration: int = 30,
        platform: str = "douyin"
    ) -> List[str]:
        """为一个视频生成多个变体"""

        keyword = self.extract_keyword_from_filename(video_path.name)
        video_name = video_path.stem[:20]  # 取前20字符

        generated_files = []

        print(f"\n{'='*70}")
        print(f"📹 处理视频: {video_path.name}")
        print(f"🏷️  关键词: {keyword}")
        print(f"{'='*70}")

        for i, template in enumerate(self.hook_templates[:num_variants], 1):
            hook_text = template.format(keyword=keyword)
            cta_text = self.cta_templates[i % len(self.cta_templates)]

            output_name = f"{video_name}_v{i}.mp4"

            print(f"\n🎬 生成变体 {i}/{num_variants}: {hook_text}")

            try:
                output_path = self.viral_system.create_complete_viral_video(
                    input_video=str(video_path),
                    output_path=output_name,
                    hook_text=hook_text,
                    cta_text=cta_text,
                    account_name="AI工具猎人",
                    duration=duration,
                    platform=platform
                )

                generated_files.append(output_path)
                print(f"✅ 变体 {i} 完成")

            except Exception as e:
                print(f"❌ 变体 {i} 失败: {str(e)}")
                continue

        return generated_files

    def run_mass_production(
        self,
        max_videos: int = 10,
        variants_per_video: int = 3,
        duration: int = 30
    ):
        """
        大规模生产

        Args:
            max_videos: 处理多少个源视频（测试用10个，正式用43）
            variants_per_video: 每个视频生成几个变体（建议3-6个）
            duration: 每个视频时长
        """

        videos = self.get_all_videos()
        total_videos = min(max_videos, len(videos))

        print(f"\n{'='*70}")
        print(f"🏭 大规模生产系统启动")
        print(f"{'='*70}")
        print(f"📊 源视频数量: {len(videos)}")
        print(f"📊 计划处理: {total_videos} 个")
        print(f"📊 每个视频变体数: {variants_per_video}")
        print(f"📊 预计生成总数: {total_videos * variants_per_video} 个视频")
        print(f"{'='*70}\n")

        all_generated = []
        success_count = 0
        fail_count = 0

        for idx, video_path in enumerate(videos[:total_videos], 1):
            print(f"\n{'#'*70}")
            print(f"处理进度: {idx}/{total_videos}")
            print(f"{'#'*70}")

            try:
                generated = self.generate_batch_variants(
                    video_path=video_path,
                    num_variants=variants_per_video,
                    duration=duration
                )

                all_generated.extend(generated)
                success_count += len(generated)

            except Exception as e:
                print(f"❌ 视频处理失败: {video_path.name}")
                print(f"   错误: {str(e)}")
                fail_count += 1
                continue

        # 生成报告
        report_path = self.output_dir / "production_report.json"
        report = {
            "total_source_videos": len(videos),
            "processed_videos": total_videos,
            "variants_per_video": variants_per_video,
            "success_count": success_count,
            "fail_count": fail_count,
            "generated_files": all_generated
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*70}")
        print(f"🎉 大规模生产完成!")
        print(f"{'='*70}")
        print(f"✅ 成功生成: {success_count} 个视频")
        print(f"❌ 失败: {fail_count} 个")
        print(f"📊 成功率: {success_count/(success_count+fail_count)*100:.1f}%")
        print(f"📁 输出目录: {self.output_dir}")
        print(f"📄 详细报告: {report_path}")
        print(f"{'='*70}\n")

        return all_generated


if __name__ == "__main__":
    system = MassProductionSystem()

    # 先测试前5个视频，每个3个变体（共15个）
    print("🧪 测试模式：前5个视频 × 3个变体 = 15个视频")

    system.run_mass_production(
        max_videos=5,
        variants_per_video=3,
        duration=30
    )

    print("\n" + "="*70)
    print("✅ 测试完成！如果效果满意，修改参数运行全量生产：")
    print("   max_videos=43, variants_per_video=6")
    print("   将生成 258 个爆款视频")
    print("="*70)
