#!/usr/bin/env python3
"""
Premium Video Editor - 高级感视频包装
使用 ffmpeg 复杂滤镜实现专业级视觉效果
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Optional


class PremiumVideoEditor:
    """专业级视频编辑器 - 真正的高级感"""

    def __init__(self, working_dir: str = "./premium_output"):
        self.working_dir = Path(working_dir)
        self.working_dir.mkdir(parents=True, exist_ok=True)

    def create_tech_minimal_style(
        self,
        input_video: str,
        output_path: str,
        title: str,
        subtitle: str,
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """
        科技极简风格
        - 渐变背景（深色）
        - 优雅字幕动画
        - 边缘柔光
        - 流畅转场
        """

        # 平台尺寸配置
        platform_config = {
            "douyin": {"width": 1080, "height": 1920, "aspect": "9:16"},
            "bilibili": {"width": 1920, "height": 1080, "aspect": "16:9"},
            "xiaohongshu": {"width": 1080, "height": 1440, "aspect": "3:4"}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        output_file = self.working_dir / output_path

        # 复杂滤镜链 - 打造高级感
        filter_complex = f"""
        [0:v]scale=iw*min({w}/iw\,{h}/ih):ih*min({w}/iw\,{h}/ih),
        gblur=sigma=0:steps=1,
        eq=contrast=1.1:brightness=0.02:saturation=1.15,
        unsharp=5:5:1.0:5:5:0.0[scaled];

        color=c=#0a0a0a:s={w}x{h}:d={duration}[bg];

        [bg]drawbox=x=0:y=0:w={w}:h={h}:color=#1a1a1a@0.3:t=fill,
        drawbox=x=0:y=0:w={w}:h=200:color=black@0.6:t=fill,
        drawbox=x=0:y={h-200}:w={w}:h=200:color=black@0.6:t=fill[bg_gradient];

        [bg_gradient][scaled]overlay=(W-w)/2:(H-h)/2:format=auto[composed];

        [composed]drawbox=x={w//2-400}:y=80:w=800:h=3:color=#ffffff@0.8:t=fill,
        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial\\ Bold.ttf:
        text='{title}':fontcolor=white:fontsize=56:
        x=(w-text_w)/2:y=120:
        alpha='if(lt(t,1),t,if(lt(t,{duration-1.5}),1,({duration}-t)/1.5))':
        shadowcolor=black@0.6:shadowx=2:shadowy=2,

        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:
        text='{subtitle}':fontcolor=#cccccc:fontsize=32:
        x=(w-text_w)/2:y=200:
        alpha='if(lt(t,1.2),0,if(lt(t,2.2),(t-1.2),if(lt(t,{duration-1.5}),1,({duration}-t)/1.5)))':
        shadowcolor=black@0.4:shadowx=1:shadowy=1[with_titles];

        [with_titles]drawbox=x={w//2-3}:y={h-120}:w=6:h=60:color=#4a9eff@0.9:t=fill,
        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:
        text='向上滑动查看更多':fontcolor=#aaaaaa:fontsize=28:
        x=(w-text_w)/2:y={h-80}:
        alpha='sin(2*PI*t/2)*0.3+0.7'[final]
        """

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
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

        print(f"🎨 生成科技极简风格...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"ffmpeg failed: {result.stderr}")

        print(f"✅ 已生成: {output_file}")
        print(f"📊 文件大小: {output_file.stat().st_size / 1024 / 1024:.1f}MB")

        return str(output_file)

    def create_cyberpunk_neon_style(
        self,
        input_video: str,
        output_path: str,
        title: str,
        subtitle: str,
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """
        赛博霓虹风格
        - 霓虹色背景
        - 发光字幕
        - RGB色彩分离
        - 故障效果
        """

        platform_config = {
            "douyin": {"width": 1080, "height": 1920},
            "bilibili": {"width": 1920, "height": 1080},
            "xiaohongshu": {"width": 1080, "height": 1440}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        output_file = self.working_dir / output_path

        filter_complex = f"""
        [0:v]scale=iw*min({w}/iw\,{h}/ih):ih*min({w}/iw\,{h}/ih),
        eq=contrast=1.2:saturation=1.4,
        curves=preset=lighter[scaled];

        color=c=#0d1117:s={w}x{h}:d={duration}[bg];

        [bg]drawbox=x=0:y=100:w={w}:h=4:color=#00ffff@0.6:t=fill,
        drawbox=x=0:y=104:w={w}:h=2:color=#ff00ff@0.4:t=fill,
        drawbox=x=0:y={h-106}:w={w}:h=4:color=#00ffff@0.6:t=fill,
        drawbox=x=0:y={h-102}:w={w}:h=2:color=#ff00ff@0.4:t=fill[bg_neon];

        [bg_neon][scaled]overlay=(W-w)/2:(H-h)/2[composed];

        [composed]drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial\\ Bold.ttf:
        text='{title}':fontcolor=#00ffff:fontsize=64:
        x=(w-text_w)/2:y=140:
        alpha='if(lt(t,0.8),t/0.8,if(lt(t,{duration-1}),1,({duration}-t)))':
        shadowcolor=#ff00ff@0.8:shadowx=3:shadowy=3,

        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:
        text='{subtitle}':fontcolor=#ff00ff:fontsize=36:
        x=(w-text_w)/2:y=230:
        alpha='if(lt(t,1.5),0,if(lt(t,2.5),(t-1.5),if(lt(t,{duration-1}),1,({duration}-t))))':
        shadowcolor=#00ffff@0.6:shadowx=2:shadowy=2[with_glow];

        [with_glow]drawbox=x=40:y={h-140}:w=120:h=4:color=#00ffff@0.9:t=fill,
        drawbox=x=40:y={h-136}:w=120:h=2:color=#ff00ff@0.7:t=fill,
        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:
        text='SWIPE UP':fontcolor=#00ffff:fontsize=24:
        x=170:y={h-130}:
        alpha='sin(2*PI*t/1.5)*0.4+0.6'[final]
        """

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
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

        print(f"🌃 生成赛博霓虹风格...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"ffmpeg failed: {result.stderr}")

        print(f"✅ 已生成: {output_file}")
        print(f"📊 文件大小: {output_file.stat().st_size / 1024 / 1024:.1f}MB")

        return str(output_file)

    def create_apple_business_style(
        self,
        input_video: str,
        output_path: str,
        title: str,
        subtitle: str,
        duration: int = 30,
        platform: str = "douyin"
    ) -> str:
        """
        Apple商业风格
        - 纯净背景
        - 精致字体
        - 大量留白
        - 优雅动画
        """

        platform_config = {
            "douyin": {"width": 1080, "height": 1920},
            "bilibili": {"width": 1920, "height": 1080},
            "xiaohongshu": {"width": 1080, "height": 1440}
        }

        config = platform_config.get(platform, platform_config["douyin"])
        w, h = config["width"], config["height"]

        output_file = self.working_dir / output_path

        filter_complex = f"""
        [0:v]scale=iw*min({w}/iw\,{h}/ih)*0.92:ih*min({w}/iw\,{h}/ih)*0.92,
        gblur=sigma=0,
        eq=contrast=1.05:brightness=0.03:saturation=1.08[scaled];

        color=c=#f5f5f7:s={w}x{h}:d={duration}[bg];

        [bg][scaled]overlay=(W-w)/2:(H-h)/2+40[composed];

        [composed]drawbox=x={w//2-200}:y=160:w=400:h=1:color=#1d1d1f@0.2:t=fill,
        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial\\ Bold.ttf:
        text='{title}':fontcolor=#1d1d1f:fontsize=52:
        x=(w-text_w)/2:y=200:
        alpha='if(lt(t,1),t,if(lt(t,{duration-2}),1,({duration}-t)/2))',

        drawtext=fontfile=/System/Library/Fonts/Supplemental/Arial.ttf:
        text='{subtitle}':fontcolor=#6e6e73:fontsize=30:
        x=(w-text_w)/2:y=280:
        alpha='if(lt(t,1.5),0,if(lt(t,2.5),(t-1.5),if(lt(t,{duration-2}),1,({duration}-t)/2)))'[with_text];

        [with_text]drawbox=x=0:y={h-2}:w={w}:h=2:color=#d2d2d7@0.5:t=fill,
        drawbox=x={w//2-25}:y={h-60}:w=50:h=4:color=#1d1d1f@0.3:t=fill:
        enable='between(t,0,{duration})'[final]
        """

        cmd = [
            "ffmpeg", "-y",
            "-i", input_video,
            "-filter_complex", filter_complex,
            "-map", "[final]",
            "-map", "0:a?",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "21",
            "-c:a", "aac",
            "-b:a", "192k",
            "-t", str(duration),
            "-movflags", "+faststart",
            str(output_file)
        ]

        print(f"🍎 生成Apple商业风格...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"ffmpeg failed: {result.stderr}")

        print(f"✅ 已生成: {output_file}")
        print(f"📊 文件大小: {output_file.stat().st_size / 1024 / 1024:.1f}MB")

        return str(output_file)


if __name__ == "__main__":
    # 测试代码
    editor = PremiumVideoEditor("/Users/andy/Documents/AICode/09 Andy-Video-SKill/premium_output")

    test_video = "/Users/andy/Documents/Andy录屏素材库/GPT做电脑壁纸.mp4"

    # 生成3种风格
    styles = [
        ("tech_minimal", "用AI做电脑壁纸", "30秒搞定专业级壁纸"),
        ("cyberpunk", "AI壁纸生成", "未来已来"),
        ("apple_business", "AI创作壁纸", "简单 强大 优雅")
    ]

    for style_name, title, subtitle in styles:
        output = f"demo_{style_name}_douyin.mp4"
        print(f"\n{'='*60}")
        print(f"生成风格: {style_name}")
        print(f"{'='*60}")

        if style_name == "tech_minimal":
            editor.create_tech_minimal_style(
                test_video, output, title, subtitle, duration=30, platform="douyin"
            )
        elif style_name == "cyberpunk":
            editor.create_cyberpunk_neon_style(
                test_video, output, title, subtitle, duration=30, platform="douyin"
            )
        else:
            editor.create_apple_business_style(
                test_video, output, title, subtitle, duration=30, platform="douyin"
            )
