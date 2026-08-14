#!/usr/bin/env python3
"""
Premium Video Editor V2 - 使用图片叠加实现高级感
不依赖 drawtext，用 PIL 生成标题图片后叠加
"""

import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


class PremiumVideoEditorV2:
    """专业级视频编辑器 - 图片叠加方案"""

    def __init__(self, working_dir: str = "./premium_output"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)
        self.assets_dir = self.working_dir / "assets"
        self.assets_dir.mkdir(exist_ok=True)

    def create_title_overlay(
        self,
        title: str,
        subtitle: str,
        width: int,
        height: int,
        style: str = "tech_minimal"
    ) -> str:
        """生成透明背景的标题图片"""

        # 创建透明画布
        img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 加载系统字体
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 56)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 32)
            hint_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            hint_font = ImageFont.load_default()

        if style == "tech_minimal":
            # 科技极简风格
            # 顶部渐变装饰
            for i in range(200):
                alpha = int(153 * (1 - i/200))  # 0.6 -> 0
                draw.rectangle([(0, i), (width, i+1)], fill=(26, 26, 26, alpha))

            # 标题装饰线
            draw.rectangle([(width//2-400, 80), (width//2+400, 83)], fill=(255, 255, 255, 204))

            # 标题文字（带阴影）
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            # 阴影
            draw.text((title_x+2, 122), title, font=title_font, fill=(0, 0, 0, 153))
            # 主文字
            draw.text((title_x, 120), title, font=title_font, fill=(255, 255, 255, 255))

            # 副标题
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x+1, 201), subtitle, font=subtitle_font, fill=(0, 0, 0, 102))
            draw.text((subtitle_x, 200), subtitle, font=subtitle_font, fill=(204, 204, 204, 255))

            # 底部装饰
            for i in range(200):
                alpha = int(153 * (i/200))
                draw.rectangle([(0, height-200+i), (width, height-200+i+1)], fill=(26, 26, 26, alpha))

            # 底部提示条
            draw.rectangle([(width//2-3, height-120), (width//2+3, height-60)], fill=(74, 158, 255, 230))

            # 提示文字
            hint_text = "向上滑动查看更多"
            hint_bbox = draw.textbbox((0, 0), hint_text, font=hint_font)
            hint_width = hint_bbox[2] - hint_bbox[0]
            hint_x = (width - hint_width) // 2
            draw.text((hint_x, height-80), hint_text, font=hint_font, fill=(170, 170, 170, 255))

        elif style == "cyberpunk":
            # 赛博霓虹风格
            # 顶部霓虹线
            draw.rectangle([(0, 100), (width, 104)], fill=(0, 255, 255, 153))
            draw.rectangle([(0, 104), (width, 106)], fill=(255, 0, 255, 102))

            # 标题（霓虹效果 - 多层叠加）
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2

            # 外发光
            draw.text((title_x+3, 143), title, font=title_font, fill=(255, 0, 255, 204))
            # 主体
            draw.text((title_x, 140), title, font=title_font, fill=(0, 255, 255, 255))

            # 副标题
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x+2, 232), subtitle, font=subtitle_font, fill=(0, 255, 255, 153))
            draw.text((subtitle_x, 230), subtitle, font=subtitle_font, fill=(255, 0, 255, 255))

            # 底部霓虹线
            draw.rectangle([(0, height-106), (width, height-102)], fill=(0, 255, 255, 153))
            draw.rectangle([(0, height-102), (width, height-98)], fill=(255, 0, 255, 102))

            # 底部装饰
            draw.rectangle([(40, height-140), (160, height-136)], fill=(0, 255, 255, 230))
            draw.rectangle([(40, height-136), (160, height-134)], fill=(255, 0, 255, 179))
            hint_text = "SWIPE UP"
            draw.text((170, height-130), hint_text, font=hint_font, fill=(0, 255, 255, 255))

        elif style == "apple_business":
            # Apple商业风格
            # 顶部装饰线
            draw.rectangle([(width//2-200, 160), (width//2+200, 161)], fill=(29, 29, 31, 51))

            # 标题
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            title_width = title_bbox[2] - title_bbox[0]
            title_x = (width - title_width) // 2
            draw.text((title_x, 200), title, font=title_font, fill=(29, 29, 31, 255))

            # 副标题
            subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
            subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
            subtitle_x = (width - subtitle_width) // 2
            draw.text((subtitle_x, 280), subtitle, font=subtitle_font, fill=(110, 110, 115, 255))

            # 底部装饰条
            draw.rectangle([(width//2-25, height-60), (width//2+25, height-56)], fill=(29, 29, 31, 77))

        # 保存
        output_path = self.assets_dir / f"title_overlay_{style}.png"
        img.save(output_path, "PNG")
        print(f"✅ 标题图层已生成: {output_path}")
        return str(output_path)

    def create_background(self, width: int, height: int, style: str = "tech_minimal") -> str:
        """生成背景图片"""
        img = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(img)

        if style == "tech_minimal":
            # 深色渐变背景
            for y in range(height):
                # 从深灰到黑色的微妙渐变
                gray = int(10 + (26 - 10) * (1 - y / height))
                draw.rectangle([(0, y), (width, y+1)], fill=(gray, gray, gray))

        elif style == "cyberpunk":
            # 深色背景带微妙的蓝紫渐变
            for y in range(height):
                r = int(13)
                g = int(17 + 10 * (y / height))
                b = int(23 + 15 * (y / height))
                draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))

        elif style == "apple_business":
            # 纯净浅灰背景
            img = Image.new('RGB', (width, height), (245, 245, 247))

        output_path = self.assets_dir / f"background_{style}.png"
        img.save(output_path, "PNG")
        print(f"✅ 背景图层已生成: {output_path}")
        return str(output_path)

    def create_premium_video(
        self,
        input_video: str,
        output_path: str,
        title: str,
        subtitle: str,
        style: str = "tech_minimal",
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """生成高级感视频"""

        platform_config = {
            "douyin": {"width": 1080, "height": 1920},
            "bilibili": {"width": 1920, "height": 1080},
            "xiaohongshu": {"width": 1080, "height": 1440}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        # 生成图层
        print(f"\n🎨 生成 {style} 风格视频...")
        bg_path = self.create_background(w, h, style)
        title_path = self.create_title_overlay(title, subtitle, w, h, style)

        output_file = self.working_dir / output_path

        # 构建滤镜链
        if style == "apple_business":
            # Apple风格：视频缩小留白
            video_scale = 0.92
            filter_complex = f"""
            [0:v]scale=iw*min({w}/iw\\,{h}/ih)*{video_scale}:ih*min({w}/iw\\,{h}/ih)*{video_scale},
            eq=contrast=1.05:brightness=0.03:saturation=1.08[scaled];

            [1:v][scaled]overlay=(W-w)/2:(H-h)/2+40[with_video];
            [with_video][2:v]overlay=0:0:format=auto,
            fade=in:st=0:d=1:alpha=1,
            fade=out:st={duration-1.5}:d=1.5:alpha=1[final]
            """
        else:
            # 其他风格：视频居中
            filter_complex = f"""
            [0:v]scale=iw*min({w}/iw\\,{h}/ih):ih*min({w}/iw\\,{h}/ih),
            eq=contrast=1.1:brightness=0.02:saturation=1.15[scaled];

            [1:v][scaled]overlay=(W-w)/2:(H-h)/2[with_video];
            [with_video][2:v]overlay=0:0:format=auto,
            fade=in:st=0:d=1:alpha=1,
            fade=out:st={duration-1.5}:d=1.5:alpha=1[final]
            """

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-loop", "1", "-i", bg_path,
            "-i", title_path,
            "-filter_complex", filter_complex,
            "-map", "[final]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-movflags", "+faststart",
            str(output_file)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"ffmpeg failed: {result.stderr}")

        file_size = output_file.stat().st_size / 1024 / 1024
        print(f"✅ 视频生成完成: {output_file}")
        print(f"📊 文件大小: {file_size:.1f}MB")

        return str(output_file)


if __name__ == "__main__":
    editor = PremiumVideoEditorV2("/Users/andy/Documents/AICode/09 Andy-Video-SKill/premium_output")

    test_video = "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4"

    styles = [
        ("tech_minimal", "用AI做电脑壁纸", "30秒搞定专业级壁纸"),
        ("cyberpunk", "AI壁纸生成", "未来已来"),
        ("apple_business", "AI创作壁纸", "简单 强大 优雅")
    ]

    for style_name, title, subtitle in styles:
        print(f"\n{'='*70}")
        print(f"🎬 生成风格: {style_name.upper()}")
        print(f"{'='*70}")

        output = f"premium_{style_name}_douyin.mp4"
        editor.create_premium_video(
            input_video=test_video,
            output_path=output,
            title=title,
            subtitle=subtitle,
            style=style_name,
            duration=30,
            platform="douyin"
        )
