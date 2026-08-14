#!/usr/bin/env python3
"""
全球顶级AI知识博主 - 视频生产系统 V3.0
MrBeast级制作水准 × 科技美学 × 病毒式传播力
"""

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import List, Tuple
import colorsys


class PremiumViralProducer:
    """全球顶级视频生产系统"""

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.output_dir / "assets"
        self.assets_dir.mkdir(exist_ok=True)

        # 品牌配色
        self.colors = {
            "tech_blue": (14, 165, 233),      # #0EA5E9
            "energy_purple": (139, 92, 246),  # #8B5CF6
            "accent_red": (239, 68, 68),      # #EF4444
            "neutral_white": (248, 250, 252), # #F8FAFC
            "deep_black": (15, 23, 42),       # #0F172A
        }

    def ease_out_back(self, t: float) -> float:
        """回弹缓动函数（更有活力）"""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

    def ease_out_expo(self, t: float) -> float:
        """指数衰减（快速滑入）"""
        return 1 if t == 1 else 1 - pow(2, -10 * t)

    def ease_in_cubic(self, t: float) -> float:
        """三次方缓入（柔和加速）"""
        return t * t * t

    def create_gradient_background(self, width: int, height: int, color1: Tuple, color2: Tuple) -> Image.Image:
        """创建渐变背景（蓝→紫科技感）"""
        base = Image.new('RGB', (width, height), color1)
        gradient = Image.new('RGB', (width, height), color1)
        draw = ImageDraw.Draw(gradient)

        for y in range(height):
            ratio = y / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))

        return gradient

    def create_glow_particles(self, width: int, height: int, num_particles: int = 50) -> Image.Image:
        """创建粒子光效"""
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        np.random.seed(42)
        for _ in range(num_particles):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            size = np.random.randint(2, 8)
            alpha = np.random.randint(50, 150)

            # 蓝紫色粒子
            if np.random.random() > 0.5:
                color = (*self.colors["tech_blue"], alpha)
            else:
                color = (*self.colors["energy_purple"], alpha)

            draw.ellipse([x-size, y-size, x+size, y+size], fill=color)

        # 高斯模糊制造光晕
        img = img.filter(ImageFilter.GaussianBlur(radius=5))
        return img

    def create_premium_hook_frame(
        self,
        text: str,
        width: int,
        height: int,
        frame_number: int,
        total_frames: int = 90
    ) -> Image.Image:
        """
        创建顶级Hook帧（单帧）
        动画: 0-15帧放大 + 15-75帧保持 + 75-90帧缩小淡出
        """
        # 1. 渐变背景
        bg = self.create_gradient_background(
            width, height,
            self.colors["tech_blue"],
            self.colors["energy_purple"]
        )

        # 2. 粒子效果
        particles = self.create_glow_particles(width, height, num_particles=80)
        bg.paste(particles, (0, 0), particles)

        # 3. 计算动画参数
        if frame_number < 15:
            # 放大阶段 (0-0.5s)
            t = frame_number / 15
            eased_t = self.ease_out_back(t)
            scale = 0.5 + 0.5 * eased_t
            opacity = int(255 * self.ease_in_cubic(t))
        elif frame_number < 75:
            # 保持阶段 (0.5-2.5s)
            scale = 1.0
            opacity = 255
        else:
            # 缩小淡出 (2.5-3s)
            t = (frame_number - 75) / 15
            scale = 1.0 - 0.15 * t
            opacity = int(255 * (1 - t))

        # 4. 创建文字层
        text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(text_layer)

        # 加载字体
        try:
            # 中文：思源黑体 Bold
            font_path = "/System/Library/Fonts/PingFang.ttc"
            base_size = 100
            font_size = int(base_size * scale)
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # 文字位置（居中偏上）
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = int(height * 0.35 - text_height // 2)

        # 5. 多层阴影（深度感）
        for offset in [20, 15, 10, 5]:
            shadow_alpha = int(opacity * 0.15)
            shadow_color = (*self.colors["deep_black"], shadow_alpha)
            draw.text((x + offset, y + offset), text, font=font, fill=shadow_color)

        # 6. 描边（3层，制造立体感）
        stroke_width = 4
        for dx, dy in [(-stroke_width, 0), (stroke_width, 0), (0, -stroke_width), (0, stroke_width),
                       (-stroke_width, -stroke_width), (stroke_width, stroke_width),
                       (-stroke_width, stroke_width), (stroke_width, -stroke_width)]:
            outline_color = (30, 58, 138, opacity)  # 深蓝描边
            draw.text((x + dx, y + dy), text, font=font, fill=outline_color)

        # 7. 渐变文字（蓝→紫）
        # 因PIL不支持文字渐变，用纯色+高光模拟
        main_color = (255, 215, 0, opacity)  # 金色（高对比度）
        draw.text((x, y), text, font=font, fill=main_color)

        # 8. 顶部高光
        highlight_color = (255, 255, 255, int(opacity * 0.6))
        draw.text((x, y - 2), text, font=font, fill=highlight_color)

        # 9. 合成
        result = Image.alpha_composite(bg.convert('RGBA'), text_layer)
        return result

    def generate_premium_hook_sequence(
        self,
        text: str,
        width: int = 1080,
        height: int = 1920
    ) -> List[str]:
        """生成90帧Hook动画序列"""
        print(f"🎬 生成顶级Hook动画: {text}")
        frames = []

        for i in range(90):
            frame = self.create_premium_hook_frame(text, width, height, i, 90)
            frame_path = self.assets_dir / f"hook_{hash(text)}_{i:03d}.png"
            frame.save(frame_path, "PNG", optimize=True)
            frames.append(str(frame_path))

            if (i + 1) % 30 == 0:
                print(f"  进度: {i+1}/90 帧")

        print(f"  ✅ Hook动画完成")
        return frames

    def create_annotation_overlay(
        self,
        width: int,
        height: int,
        text: str,
        annotation_type: str = "arrow"
    ) -> Image.Image:
        """创建标注叠加层（箭头/高光圈/文字提示）"""
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        if annotation_type == "arrow":
            # 红色箭头指向关键区域
            arrow_color = (*self.colors["accent_red"], 200)
            # 简化：绘制文字提示
            try:
                font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 60)
            except:
                font = ImageFont.load_default()

            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = int(height * 0.15)

            # 半透明背景卡片
            padding = 30
            draw.rounded_rectangle(
                [x - padding, y - padding, x + text_width + padding, y + 80],
                radius=20,
                fill=(239, 68, 68, 220)
            )

            # 白色文字
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

        return overlay

    def create_premium_cta_frame(
        self,
        cta_text: str,
        account_name: str,
        width: int = 1080,
        height: int = 1920
    ) -> str:
        """创建顶级CTA帧"""
        # 渐变背景（半透明遮罩）
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        # 渐变遮罩（从透明到半透明黑）
        for y in range(height):
            ratio = y / height
            alpha = int(180 * ratio)
            draw = ImageDraw.Draw(img)
            draw.line([(0, y), (width, y)], fill=(15, 23, 42, alpha))

        draw = ImageDraw.Draw(img)

        # CTA主文字（渐变金色）
        try:
            cta_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 80)
        except:
            cta_font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 - 150

        # 阴影
        draw.text((x + 4, y + 4), cta_text, font=cta_font, fill=(0, 0, 0, 255))
        # 主文字（金色）
        draw.text((x, y), cta_text, font=cta_font, fill=(255, 215, 0, 255))

        # 账号名（带Logo样式）
        try:
            account_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 70)
        except:
            account_font = cta_font

        account_text = f"@{account_name}"
        bbox = draw.textbbox((0, 0), account_text, font=account_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2

        # 圆角背景卡片（品牌色）
        padding = 40
        draw.rounded_rectangle(
            [x - padding, y - 20, x + text_width + padding, y + 90],
            radius=50,
            fill=(14, 165, 233, 255)  # 科技蓝
        )

        # 白色账号名
        draw.text((x, y), account_text, font=account_font, fill=(255, 255, 255, 255))

        # 引导文字（带Emoji）
        guide_text = "👇 评论区说说你的需求"
        try:
            guide_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 50)
        except:
            guide_font = account_font

        bbox = draw.textbbox((0, 0), guide_text, font=guide_font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) // 2
        y = height // 2 + 180

        draw.text((x + 2, y + 2), guide_text, font=guide_font, fill=(0, 0, 0, 200))
        draw.text((x, y), guide_text, font=guide_font, fill=(248, 250, 252, 255))

        # 保存
        frame_path = self.assets_dir / f"cta_premium_{hash(cta_text)}.png"
        img.save(frame_path, "PNG")
        return str(frame_path)

    def create_premium_viral_video(
        self,
        input_video: str,
        output_path: str,
        hook_text: str,
        cta_text: str = "想学更多AI技巧？",
        account_name: str = "全球AI工具猎人",
        width: int = 1080,
        height: int = 1920
    ) -> str:
        """
        创建全球顶级质量爆款视频
        """
        print(f"\n{'='*70}")
        print(f"🌟 全球顶级视频生产系统 V3.0")
        print(f"{'='*70}")
        print(f"📹 源素材: {Path(input_video).name}")
        print(f"🎯 Hook: {hook_text}")
        print(f"{'='*70}\n")

        # 1. 生成Hook帧序列
        hook_frames = self.generate_premium_hook_sequence(hook_text, width, height)

        # 2. 生成CTA帧
        print("🎨 生成CTA帧...")
        cta_frame = self.create_premium_cta_frame(cta_text, account_name, width, height)
        print("  ✅ CTA完成")

        # 3. Hook片段（0-3s）- 纯Hook动画，不叠加原视频
        print("\n🎬 合成Hook片段...")
        hook_video = self.assets_dir / "hook_premium.mp4"
        frames_list = self.assets_dir / "hook_frames.txt"

        with open(frames_list, 'w') as f:
            for frame in hook_frames:
                f.write(f"file '{frame}'\n")
                f.write(f"duration 0.033333\n")

        cmd_hook = [
            "ffmpeg", "-y", "-loglevel", "warning",
            "-f", "concat", "-safe", "0", "-i", str(frames_list),
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(hook_video)
        ]
        subprocess.run(cmd_hook)
        print("  ✅ Hook片段完成")

        # 4. 主片段（3-23s）
        print("\n🎬 合成主内容片段...")
        main_video = self.assets_dir / "main_premium.mp4"
        cmd_main = [
            "ffmpeg", "-y", "-loglevel", "warning",
            "-ss", "3", "-t", "20",
            "-i", input_video,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                   f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
                   f"eq=contrast=1.2:saturation=1.3:brightness=0.05",
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            str(main_video)
        ]
        subprocess.run(cmd_main)
        print("  ✅ 主片段完成")

        # 5. CTA片段（23-30s）
        print("\n🎬 合成CTA片段...")
        cta_video = self.assets_dir / "cta_premium.mp4"
        cmd_cta = [
            "ffmpeg", "-y", "-loglevel", "warning",
            "-ss", "23", "-t", "7",
            "-i", input_video,
            "-loop", "1", "-i", cta_frame,
            "-filter_complex",
            f"[0:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black[bg];"
            f"[bg][1:v]overlay=0:0[v]",
            "-map", "[v]",
            "-t", "7",
            "-c:v", "libx264", "-preset", "slow", "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-an",
            str(cta_video)
        ]
        subprocess.run(cmd_cta)
        print("  ✅ CTA片段完成")

        # 6. 最终合成
        print("\n🎬 最终合成...")
        concat_list = self.assets_dir / "final_concat.txt"
        with open(concat_list, 'w') as f:
            f.write(f"file '{hook_video}'\n")
            f.write(f"file '{main_video}'\n")
            f.write(f"file '{cta_video}'\n")

        output_file = self.output_dir / output_path
        cmd_final = [
            "ffmpeg", "-y", "-loglevel", "warning",
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
        print(f"✅ 全球顶级视频生成成功！")
        print(f"📊 文件: {output_file.name}")
        print(f"📊 大小: {file_size:.1f}MB")
        print(f"📊 质量: 好莱坞级（CRF 18 + Slow Preset）")
        print(f"{'='*70}\n")

        return str(output_file)


if __name__ == "__main__":
    producer = PremiumViralProducer(
        "/Users/andy/Documents/AICode/09 Andy-Video-SKill/premium_output"
    )

    # 第一个样片：GPT做壁纸
    producer.create_premium_viral_video(
        input_video="/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4",
        output_path="GPT做壁纸_全球顶级版_v1.mp4",
        hook_text="3秒生成价值1000美元的壁纸",
        cta_text="想学更多AI赚钱技巧？",
        account_name="全球AI工具猎人"
    )
