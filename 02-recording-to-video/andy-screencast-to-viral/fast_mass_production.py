#!/usr/bin/env python3
"""
快速批量生产系统 - 无Whisper版本
专为无声录屏优化，纯视觉Hook
"""

import subprocess
from pathlib import Path
from typing import List
from PIL import Image, ImageDraw, ImageFont


class FastViralProducer:
    """快速爆款视频生产（无字幕版）"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.output_dir / "assets"
        self.assets_dir.mkdir(exist_ok=True)

    def generate_hook_frames(self, hook_text: str, width: int, height: int) -> List[str]:
        """生成Hook动画帧（90帧 = 3秒）"""
        frames = []
        total_frames = 90

        try:
            font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
        except:
            font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"

        for i in range(total_frames):
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # 动画曲线
            if i < 15:  # 0-0.5s: 放大
                progress = i / 15
                scale = 0.6 + 0.4 * progress
                alpha = int(255 * progress)
            elif i < 75:  # 0.5-2.5s: 保持
                scale = 1.0
                alpha = 255
            else:  # 2.5-3s: 淡出
                progress = (i - 75) / 15
                scale = 1.0 - 0.15 * progress
                alpha = int(255 * (1 - progress))

            # 字体大小
            size = int(90 * scale)
            try:
                font = ImageFont.truetype(font_path, size)
            except:
                font = ImageFont.load_default()

            # 文字位置
            bbox = draw.textbbox((0, 0), hook_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = int(height * 0.35)

            # 多层阴影
            for offset in range(10, 0, -2):
                shadow_alpha = int(alpha * 0.25)
                draw.text(
                    (x + offset, y + offset),
                    hook_text,
                    font=font,
                    fill=(0, 0, 0, shadow_alpha)
                )

            # 黑色描边（8方向）
            for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
                draw.text((x + dx, y + dy), hook_text, font=font, fill=(0, 0, 0, alpha))

            # 黄色主文字
            draw.text((x, y), hook_text, font=font, fill=(255, 215, 0, alpha))

            # 保存帧
            frame_path = self.assets_dir / f"hook_{hash(hook_text)}_{i:03d}.png"
            img.save(frame_path, "PNG")
            frames.append(str(frame_path))

        return frames

    def generate_cta_frame(self, cta_text: str, account_name: str, width: int, height: int) -> str:
        """生成CTA帧"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 150))
        draw = ImageDraw.Draw(img)

        # CTA文字
        try:
            cta_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 70)
        except:
            cta_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 70)

        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 100

        # 黄色CTA
        draw.text((x + 3, y + 3), cta_text, font=cta_font, fill=(0, 0, 0, 255))
        draw.text((x, y), cta_text, font=cta_font, fill=(255, 215, 0, 255))

        # 账号名
        try:
            account_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
        except:
            account_font = cta_font

        bbox = draw.textbbox((0, 0), f"@{account_name}", font=account_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 40

        draw.text((x + 2, y + 2), f"@{account_name}", font=account_font, fill=(0, 0, 0, 255))
        draw.text((x, y), f"@{account_name}", font=account_font, fill=(255, 255, 255, 255))

        # 箭头
        arrow_text = "👇 点击关注"
        try:
            arrow_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
        except:
            arrow_font = account_font

        bbox = draw.textbbox((0, 0), arrow_text, font=arrow_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 140

        draw.text((x + 2, y + 2), arrow_text, font=arrow_font, fill=(0, 0, 0, 220))
        draw.text((x, y), arrow_text, font=arrow_font, fill=(255, 215, 0, 255))

        frame_path = self.assets_dir / f"cta_{hash(cta_text)}.png"
        img.save(frame_path, "PNG")
        return str(frame_path)

    def create_viral_video(
        self,
        input_video: str,
        output_path: str,
        hook_text: str,
        cta_text: str,
        account_name: str,
        width: int = 1080,
        height: int = 1920
    ) -> str:
        """
        快速生成爆款视频（无字幕版）
        结构：Hook(3s) + Main(20s) + CTA(7s) = 30s
        """
        print(f"🎬 生成: {hook_text}")

        # 1. 生成Hook帧
        hook_frames = self.generate_hook_frames(hook_text, width, height)

        # 2. 生成CTA帧
        cta_frame = self.generate_cta_frame(cta_text, account_name, width, height)

        # 3. Hook片段（0-3s）
        hook_video = self.assets_dir / f"hook_{hash(hook_text)}.mp4"
        frames_list = self.assets_dir / f"hook_frames_{hash(hook_text)}.txt"

        with open(frames_list, 'w') as f:
            for frame in hook_frames:
                f.write(f"file '{frame}'\n")
                f.write(f"duration 0.033333\n")

        cmd_hook = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(frames_list),
            "-i", input_video,
            "-filter_complex",
            f"[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"eq=contrast=1.15:saturation=1.25[bg];"
            f"[0:v][bg]overlay=0:0[v]",
            "-map", "[v]",
            "-t", "3",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-an",  # 无音频
            str(hook_video)
        ]
        subprocess.run(cmd_hook, capture_output=True)

        # 4. 主片段（3-23s）
        main_video = self.assets_dir / f"main_{hash(hook_text)}.mp4"
        cmd_main = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", "3", "-t", "20",
            "-i", input_video,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                   f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
                   f"eq=contrast=1.15:saturation=1.25",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-an",  # 无音频
            str(main_video)
        ]
        subprocess.run(cmd_main, capture_output=True)

        # 5. CTA片段（23-30s）
        cta_video = self.assets_dir / f"cta_{hash(hook_text)}.mp4"
        cmd_cta = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", "23", "-t", "7",
            "-i", input_video,
            "-loop", "1", "-i", cta_frame,
            "-filter_complex",
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black[bg];"
            f"[bg][1:v]overlay=0:0[v]",
            "-map", "[v]",
            "-t", "7",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-an",  # 无音频
            str(cta_video)
        ]
        subprocess.run(cmd_cta, capture_output=True)

        # 6. 合并
        concat_list = self.assets_dir / f"concat_{hash(hook_text)}.txt"
        with open(concat_list, 'w') as f:
            f.write(f"file '{hook_video}'\n")
            f.write(f"file '{main_video}'\n")
            f.write(f"file '{cta_video}'\n")

        output_file = self.output_dir / output_path
        cmd_final = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            "-movflags", "+faststart",
            str(output_file)
        ]

        result = subprocess.run(cmd_final, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"合成失败: {result.stderr}")

        print(f"  ✅ {output_path}")
        return str(output_file)


def main():
    """批量生产主函数"""
    source_dir = Path("/Users/andy/Documents/Andy录屏素材库")
    output_dir = Path("/Users/andy/Documents/AICode/09 Andy-Video-SKill/fast_production_output")

    producer = FastViralProducer(str(output_dir))

    # Hook模板
    hook_templates = [
        "{keyword}只需3秒",
        "{keyword}太强了",
        "终于发现{keyword}的秘密"
    ]

    # 获取所有视频
    videos = list(source_dir.glob("*.mp4"))[:5]  # 测试模式：前5个

    print(f"\n{'='*70}")
    print(f"🚀 快速批量生产系统")
    print(f"{'='*70}")
    print(f"📊 源视频数量: {len(videos)}")
    print(f"📊 每个视频变体数: {len(hook_templates)}")
    print(f"📊 预计生成总数: {len(videos) * len(hook_templates)}")
    print(f"{'='*70}\n")

    success_count = 0

    for idx, video_path in enumerate(videos, 1):
        # 提取关键词
        video_name = video_path.stem
        keyword = video_name[:10] if len(video_name) > 10 else video_name

        print(f"\n[{idx}/{len(videos)}] {video_name}")

        for i, template in enumerate(hook_templates, 1):
            hook_text = template.format(keyword=keyword)
            output_name = f"{video_name}_v{i}.mp4"

            try:
                producer.create_viral_video(
                    input_video=str(video_path),
                    output_path=output_name,
                    hook_text=hook_text,
                    cta_text="关注我，每天分享AI神器",
                    account_name="AI工具猎人"
                )
                success_count += 1
            except Exception as e:
                print(f"  ❌ 失败: {e}")
                continue

    print(f"\n{'='*70}")
    print(f"✅ 生产完成！")
    print(f"📊 成功: {success_count}/{len(videos) * len(hook_templates)}")
    print(f"📁 输出目录: {output_dir}")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
