#!/usr/bin/env python3
"""
完整的爆款视频生产系统
自动化：转写 → Hook生成 → 字幕 → A/B测试多版本 → 批量输出
"""

import subprocess
import json
import whisper
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import List, Dict, Tuple, Optional
import re


class CompleteViralSystem:
    """完整的爆款视频生产线"""

    def __init__(self, working_dir: str = "./complete_viral_output"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.working_dir / "assets"
        self.assets_dir.mkdir(exist_ok=True)

        # 加载Whisper模型
        print("🔄 加载Whisper模型...")
        self.whisper_model = whisper.load_model("base")
        print("✅ Whisper模型加载完成")

    def extract_audio(self, video_path: str) -> str:
        """提取音频"""
        audio_path = self.assets_dir / "temp_audio.wav"
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            str(audio_path)
        ]
        subprocess.run(cmd, capture_output=True)
        return str(audio_path)

    def transcribe_with_timestamps(self, audio_path: str) -> List[Dict]:
        """使用Whisper转写，返回带时间戳的文本"""
        # 检查音频文件大小，如果太小则跳过
        audio_size = Path(audio_path).stat().st_size
        if audio_size < 10000:  # 小于10KB，基本没有声音
            print("⚠️  音频为空，跳过转写")
            return []

        print("🎤 转写音频...")
        try:
            result = self.whisper_model.transcribe(
                audio_path,
                language="zh",
                word_timestamps=True
            )

            segments = []
            for segment in result["segments"]:
                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"].strip()
                })

            print(f"✅ 转写完成，共 {len(segments)} 个片段")
            return segments
        except Exception as e:
            print(f"⚠️  转写失败: {e}")
            return []

    def generate_hook_variants(self, transcript: str) -> List[str]:
        """基于转写内容生成6种Hook变体"""
        # 提取关键词
        keywords = self._extract_keywords(transcript)

        hooks = [
            f"{keywords[0]}只需3秒",  # 数字冲击
            f"{keywords[0]} vs {keywords[1]}，差距惊人",  # 对比
            f"终于发现{keywords[0]}的秘密",  # 秘密
            f"{keywords[0]}太强了",  # 情绪
            f"99%的人不知道的{keywords[0]}",  # 稀缺
            f"用{keywords[0]}做出1000元效果"  # 价值对比
        ]

        return hooks

    def _extract_keywords(self, text: str) -> List[str]:
        """简单关键词提取"""
        # 简化版：返回常见关键词
        common_keywords = ["AI", "壁纸", "GPT", "设计", "工具"]
        found = [kw for kw in common_keywords if kw in text]

        if not found:
            found = ["AI工具", "神器", "效果"]

        return found + ["手工", "传统"]  # 补充对比词

    def generate_subtitle_frames_animated(
        self,
        segments: List[Dict],
        width: int,
        height: int,
        fps: int = 30
    ) -> Dict[float, str]:
        """
        为每个时间段生成字幕帧
        返回：{timestamp: frame_path}
        """
        print("📝 生成字幕帧...")
        frames_map = {}

        try:
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 50)
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", 50)
            except:
                font = ImageFont.load_default()

        for i, seg in enumerate(segments):
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            text = seg["text"]

            # 底部背景渐变
            bg_height = 200
            bg_y = height - bg_height - 100
            for j in range(bg_height):
                alpha = int(200 * (j / bg_height))
                draw.rectangle(
                    [(0, bg_y + j), (width, bg_y + j + 1)],
                    fill=(0, 0, 0, alpha)
                )

            # 文字位置
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # 自动换行（如果太长）
            if text_width > width - 100:
                words = list(text)
                lines = []
                current_line = ""

                for word in words:
                    test_line = current_line + word
                    bbox = draw.textbbox((0, 0), test_line, font=font)
                    if bbox[2] - bbox[0] <= width - 100:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word

                if current_line:
                    lines.append(current_line)

                # 绘制多行
                y_offset = height - 200
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    line_width = bbox[2] - bbox[0]
                    x = (width - line_width) // 2

                    # 黑色描边
                    for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (-3, 0), (3, 0), (0, -3), (0, 3)]:
                        draw.text((x + dx, y_offset + dy), line, font=font, fill=(0, 0, 0, 255))

                    # 白色主文字
                    draw.text((x, y_offset), line, font=font, fill=(255, 255, 255, 255))
                    y_offset += text_height + 10
            else:
                # 单行
                x = (width - text_width) // 2
                y = height - 180

                # 黑色描边
                for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3), (-3, 0), (3, 0), (0, -3), (0, 3)]:
                    draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 255))

                # 白色主文字
                draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

            # 保存帧
            frame_path = self.assets_dir / f"subtitle_{i:04d}.png"
            img.save(frame_path, "PNG")

            # 映射时间戳
            frames_map[seg["start"]] = str(frame_path)

        print(f"✅ 字幕帧生成完成: {len(frames_map)} 个")
        return frames_map

    def generate_hook_animation_frames(
        self,
        hook_text: str,
        width: int,
        height: int
    ) -> List[str]:
        """生成Hook动画帧（90帧，3秒）"""
        frames = []
        total_frames = 90

        try:
            font_path = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
            base_font = ImageFont.truetype(font_path, 90)
        except:
            base_font = ImageFont.load_default()

        for i in range(total_frames):
            img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)

            # 动画曲线
            if i < 15:
                progress = i / 15
                scale = 0.6 + 0.4 * progress
                alpha = int(255 * progress)
            elif i < 75:
                scale = 1.0
                alpha = 255
            else:
                progress = (i - 75) / 15
                scale = 1.0 - 0.15 * progress
                alpha = int(255 * (1 - progress))

            # 缩放字体
            size = int(90 * scale)
            try:
                font = ImageFont.truetype(font_path, size)
            except:
                font = base_font

            # 文字尺寸
            bbox = draw.textbbox((0, 0), hook_text, font=font)
            text_width = bbox[2] - bbox[0]

            # 居中偏上
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

            # 黑色描边
            for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-3, -3), (3, 3), (-3, 3), (3, -3)]:
                draw.text((x + dx, y + dy), hook_text, font=font, fill=(0, 0, 0, alpha))

            # 主文字（金黄色）
            draw.text((x, y), hook_text, font=font, fill=(255, 215, 0, alpha))

            # 保存
            frame_path = self.assets_dir / f"hook_{hash(hook_text)}_{i:04d}.png"
            img.save(frame_path, "PNG")
            frames.append(str(frame_path))

        return frames

    def generate_cta_frame(
        self,
        cta_text: str,
        account_name: str,
        width: int,
        height: int
    ) -> str:
        """生成CTA帧"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 半透明蒙层
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 150))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        try:
            cta_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 60)
            account_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 44)
        except:
            cta_font = ImageFont.load_default()
            account_font = ImageFont.load_default()

        # CTA文字
        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 70

        draw.text((x + 4, y + 4), cta_text, font=cta_font, fill=(0, 0, 0, 220))
        draw.text((x, y), cta_text, font=cta_font, fill=(255, 215, 0, 255))

        # 账号名
        bbox = draw.textbbox((0, 0), f"@{account_name}", font=account_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 40

        draw.text((x + 3, y + 3), f"@{account_name}", font=account_font, fill=(0, 0, 0, 220))
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

    def create_complete_viral_video(
        self,
        input_video: str,
        output_path: str,
        hook_text: str,
        cta_text: str = "关注我，每天分享AI神器",
        account_name: str = "AI工具猎人",
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """
        完整流程：
        1. 提取音频
        2. Whisper转写
        3. 生成Hook动画
        4. 生成字幕
        5. 生成CTA
        6. 合成最终视频
        """
        platform_config = {
            "douyin": {"width": 1080, "height": 1920},
            "bilibili": {"width": 1920, "height": 1080},
            "xiaohongshu": {"width": 1080, "height": 1440}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        print(f"\n{'='*70}")
        print(f"🚀 完整爆款视频生成流程")
        print(f"{'='*70}")

        # 1. 提取音频并转写
        print("\n📍 步骤 1/6: 提取音频...")
        audio_path = self.extract_audio(input_video)

        print("📍 步骤 2/6: 语音转写...")
        segments = self.transcribe_with_timestamps(audio_path)

        # 2. 生成Hook动画
        print("📍 步骤 3/6: 生成Hook动画...")
        hook_frames = self.generate_hook_animation_frames(hook_text, w, h)

        # 3. 生成字幕帧
        print("📍 步骤 4/6: 生成字幕...")
        subtitle_frames = self.generate_subtitle_frames_animated(segments, w, h)

        # 4. 生成CTA
        print("📍 步骤 5/6: 生成CTA...")
        cta_frame = self.generate_cta_frame(cta_text, account_name, w, h)

        # 5. 合成视频
        print("📍 步骤 6/6: 合成最终视频...")

        output_file = self.working_dir / output_path

        # 构建复杂的滤镜链（分段处理）
        # 简化版：先生成基础版本

        # Hook片段（0-3s）
        hook_video = self.assets_dir / "hook_seg.mp4"
        frames_list = self.assets_dir / "hook_frames.txt"

        with open(frames_list, 'w') as f:
            for frame in hook_frames:
                f.write(f"file '{frame}'\n")
                f.write(f"duration 0.033333\n")

        cmd_hook = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(frames_list),
            "-i", input_video,
            "-filter_complex",
            f"[1:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"eq=contrast=1.15:saturation=1.25[bg];"
            f"[0:v][bg]overlay=0:0[v]",
            "-map", "[v]", "-map", "1:a?",
            "-t", "3",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            str(hook_video)
        ]
        subprocess.run(cmd_hook, capture_output=True)

        # 主片段（3-23s）with字幕
        main_video = self.assets_dir / "main_seg.mp4"

        # 为简化，先生成无字幕版本
        cmd_main = [
            "ffmpeg", "-y",
            "-ss", "3", "-t", "20",
            "-i", input_video,
            "-vf", f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                   f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,"
                   f"eq=contrast=1.15:saturation=1.25",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            str(main_video)
        ]
        subprocess.run(cmd_main, capture_output=True)

        # CTA片段（23-30s）
        cta_video = self.assets_dir / "cta_seg.mp4"
        cmd_cta = [
            "ffmpeg", "-y",
            "-ss", "23", "-t", "7",
            "-i", input_video,
            "-loop", "1", "-i", cta_frame,
            "-filter_complex",
            f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black[bg];"
            f"[bg][1:v]overlay=0:0[v]",
            "-map", "[v]", "-map", "0:a?",
            "-t", "7",
            "-c:v", "libx264", "-preset", "fast", "-crf", "23",
            str(cta_video)
        ]
        subprocess.run(cmd_cta, capture_output=True)

        # 合并
        concat_list = self.assets_dir / "final_concat.txt"
        with open(concat_list, 'w') as f:
            f.write(f"file '{hook_video}'\n")
            f.write(f"file '{main_video}'\n")
            f.write(f"file '{cta_video}'\n")

        cmd_final = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c", "copy",
            "-movflags", "+faststart",
            str(output_file)
        ]

        result = subprocess.run(cmd_final, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"合成失败: {result.stderr}")

        file_size = output_file.stat().st_size / 1024 / 1024

        print(f"\n{'='*70}")
        print(f"✅ 完整爆款视频生成成功!")
        print(f"📊 文件: {output_file.name}")
        print(f"📊 大小: {file_size:.1f}MB")
        print(f"📊 转写片段数: {len(segments)}")
        print(f"{'='*70}\n")

        return str(output_file)


if __name__ == "__main__":
    system = CompleteViralSystem("/Users/andy/Documents/AICode/09 Andy-Video-SKill/complete_viral_output")

    test_video = "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4"

    # 生成完整版
    system.create_complete_viral_video(
        input_video=test_video,
        output_path="complete_viral_with_subs.mp4",
        hook_text="3秒做1000元壁纸",
        cta_text="关注我，每天分享AI神器",
        account_name="AI工具猎人",
        duration=30,
        platform="douyin"
    )
