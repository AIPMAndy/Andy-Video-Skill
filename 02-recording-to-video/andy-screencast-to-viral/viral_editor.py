#!/usr/bin/env python3
"""
Viral Video Editor - 真正的爆款视频生成器
基于 MrBeast 方法论：Hook × Retention × CTA
"""

import subprocess
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from typing import List, Dict, Tuple


class ViralVideoEditor:
    """爆款视频编辑器"""

    def __init__(self, working_dir: str = "./viral_output"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.working_dir / "assets"
        self.assets_dir.mkdir(exist_ok=True)

    def generate_hook_frames(
        self,
        hook_text: str,
        width: int,
        height: int,
        style: str = "impact"
    ) -> List[str]:
        """
        生成Hook动画帧（0-3秒，90帧）
        动画：放大 → 停留 → 缩小淡出
        """
        frames = []
        fps = 30
        total_frames = 90  # 3秒

        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", 80)
        except:
            font = ImageFont.load_default()

        for i in range(total_frames):
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # 动画曲线
            if i < 15:  # 0-0.5s: 放大进入
                progress = i / 15
                scale = 0.5 + 0.5 * progress
                alpha = int(255 * progress)
            elif i < 75:  # 0.5-2.5s: 停留
                scale = 1.0
                alpha = 255
            else:  # 2.5-3s: 缩小淡出
                progress = (i - 75) / 15
                scale = 1.0 - 0.2 * progress
                alpha = int(255 * (1 - progress))

            # 计算文字尺寸
            bbox = draw.textbbox((0, 0), hook_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 缩放后的字体
            scaled_size = int(80 * scale)
            try:
                scaled_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Black.ttf", scaled_size)
            except:
                scaled_font = font

            # 重新计算尺寸
            bbox = draw.textbbox((0, 0), hook_text, font=scaled_font)
            text_width = bbox[2] - bbox[0]

            # 居中位置（偏上）
            x = (width - text_width) // 2
            y = height // 3

            # 绘制多层阴影（景深效果）
            for offset in range(8, 0, -2):
                shadow_alpha = int(alpha * 0.3)
                draw.text(
                    (x + offset, y + offset),
                    hook_text,
                    font=scaled_font,
                    fill=(0, 0, 0, shadow_alpha)
                )

            # 主文字（黄色高亮）
            draw.text((x, y), hook_text, font=scaled_font, fill=(255, 215, 0, alpha))

            # 描边效果
            for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                draw.text((x + dx, y + dy), hook_text, font=scaled_font, fill=(0, 0, 0, alpha))

            # 保存帧
            frame_path = self.assets_dir / f"hook_frame_{i:04d}.png"
            img.save(frame_path, "PNG")
            frames.append(str(frame_path))

        print(f"✅ Hook动画帧生成完成: {len(frames)} 帧")
        return frames

    def generate_subtitle_frame(
        self,
        text: str,
        width: int,
        height: int,
        highlight_words: List[str] = None
    ) -> str:
        """
        生成字幕帧（底部1/3，白字黑边，关键词高亮）
        """
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 48)
        except:
            font = ImageFont.load_default()

        # 底部半透明黑色背景
        bg_height = 180
        bg_y = height - bg_height
        for i in range(bg_height):
            alpha = int(180 * (i / bg_height))
            draw.rectangle([(0, bg_y + i), (width, bg_y + i + 1)], fill=(0, 0, 0, alpha))

        # 文字位置（底部1/3）
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height - 120

        # 黑色描边
        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (-3, 0), (3, 0), (0, -3), (0, 3)]:
            draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))

        # 主文字（白色）
        draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        # 关键词高亮（黄色）
        if highlight_words:
            for word in highlight_words:
                if word in text:
                    # 简化处理：整句高亮
                    draw.text((x, y), text, font=font, fill=(255, 215, 0, 255))
                    break

        frame_path = self.assets_dir / f"subtitle_{hash(text)}.png"
        img.save(frame_path, "PNG")
        return str(frame_path)

    def generate_cta_frame(
        self,
        cta_text: str,
        account_name: str,
        width: int,
        height: int
    ) -> str:
        """
        生成CTA引导帧（最后7秒）
        """
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 半透明黑色蒙层
        for y in range(height):
            alpha = int(120)
            draw.rectangle([(0, y), (width, y + 1)], fill=(0, 0, 0, alpha))

        try:
            cta_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 56)
            account_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 40)
        except:
            cta_font = ImageFont.load_default()
            account_font = ImageFont.load_default()

        # CTA文字
        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 50

        # 阴影
        draw.text((x + 3, y + 3), cta_text, font=cta_font, fill=(0, 0, 0, 200))
        # 主文字
        draw.text((x, y), cta_text, font=cta_font, fill=(255, 215, 0, 255))

        # 账号名
        bbox = draw.textbbox((0, 0), f"@{account_name}", font=account_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 50

        draw.text((x + 2, y + 2), f"@{account_name}", font=account_font, fill=(0, 0, 0, 200))
        draw.text((x, y), f"@{account_name}", font=account_font, fill=(255, 255, 255, 255))

        # 箭头提示
        arrow = "👇"
        bbox = draw.textbbox((0, 0), arrow, font=cta_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 130
        draw.text((x, y), arrow, font=cta_font, fill=(255, 215, 0, 255))

        frame_path = self.assets_dir / "cta_frame.png"
        img.save(frame_path, "PNG")
        print(f"✅ CTA帧生成完成")
        return str(frame_path)

    def create_viral_video(
        self,
        input_video: str,
        output_path: str,
        hook_text: str,
        subtitles: List[Tuple[float, float, str]],  # (start, end, text)
        cta_text: str,
        account_name: str,
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """
        生成爆款视频

        结构：
        - 0-3s: Hook动画
        - 3-23s: 主内容 + 字幕
        - 23-30s: CTA引导
        """
        platform_config = {
            "douyin": {"width": 1080, "height": 1920},
            "bilibili": {"width": 1920, "height": 1080},
            "xiaohongshu": {"width": 1080, "height": 1440}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        print(f"\n🚀 生成爆款视频...")

        # 1. 生成Hook动画帧
        print("📍 步骤 1/4: 生成Hook动画...")
        hook_frames = self.generate_hook_frames(hook_text, w, h)

        # 2. 生成CTA帧
        print("📍 步骤 2/4: 生成CTA引导...")
        cta_frame = self.generate_cta_frame(cta_text, account_name, w, h)

        # 3. 创建Hook视频片段（使用第一帧循环）
        print("📍 步骤 3/4: 合成Hook片段...")
        hook_video = self.assets_dir / "hook_segment.mp4"

        # 使用ffmpeg的concat将帧序列转换为视频
        frames_list = self.assets_dir / "hook_frames.txt"
        with open(frames_list, 'w') as f:
            for frame in hook_frames:
                f.write(f"file '{frame}'\n")
                f.write(f"duration 0.033333\n")  # 30fps

        cmd_hook = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(frames_list),
            "-i", input_video,
            "-filter_complex",
            f"[1:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black[bg];"
            f"[0:v][bg]overlay=0:0:shortest=1[v]",
            "-map", "[v]",
            "-map", "1:a?",
            "-t", "3",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            str(hook_video)
        ]

        subprocess.run(cmd_hook, capture_output=True)

        # 4. 创建主视频（3-23秒）+ CTA（23-30秒）
        print("📍 步骤 4/4: 合成最终视频...")

        main_video = self.assets_dir / "main_segment.mp4"
        cta_video = self.assets_dir / "cta_segment.mp4"

        # 主片段（简化版：不加字幕，直接处理视频）
        cmd_main = [
            "ffmpeg", "-y",
            "-ss", "3",
            "-t", "20",
            "-i", input_video,
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                   f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,"
                   f"eq=contrast=1.1:saturation=1.2",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-c:a", "aac",
            str(main_video)
        ]
        subprocess.run(cmd_main, capture_output=True)

        # CTA片段
        cmd_cta = [
            "ffmpeg", "-y",
            "-ss", "23",
            "-t", "7",
            "-i", input_video,
            "-loop", "1",
            "-i", cta_frame,
            "-filter_complex",
            f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black[bg];"
            f"[bg][1:v]overlay=0:0[v]",
            "-map", "[v]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "23",
            "-t", "7",
            str(cta_video)
        ]
        subprocess.run(cmd_cta, capture_output=True)

        # 5. 合并所有片段
        output_file = self.working_dir / output_path
        concat_list = self.assets_dir / "concat_list.txt"

        with open(concat_list, 'w') as f:
            f.write(f"file '{hook_video}'\n")
            f.write(f"file '{main_video}'\n")
            f.write(f"file '{cta_video}'\n")

        cmd_final = [
            "ffmpeg", "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            "-movflags", "+faststart",
            str(output_file)
        ]

        result = subprocess.run(cmd_final, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"ffmpeg failed: {result.stderr}")

        file_size = output_file.stat().st_size / 1024 / 1024
        print(f"✅ 爆款视频生成完成!")
        print(f"📊 文件: {output_file}")
        print(f"📊 大小: {file_size:.1f}MB")

        return str(output_file)


if __name__ == "__main__":
    editor = ViralVideoEditor("/Users/andy/Documents/AICode/09 Andy-Video-SKill/viral_output")

    test_video = "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4"

    # 测试：生成一个爆款版本
    editor.create_viral_video(
        input_video=test_video,
        output_path="viral_demo_v1.mp4",
        hook_text="3秒做1000元壁纸",
        subtitles=[],  # 简化版暂时不加字幕
        cta_text="关注我，每天分享AI神器",
        account_name="AI工具猎人",
        duration=30,
        platform="douyin"
    )
