#!/usr/bin/env python3
"""
Video Editor - Phase 2 of Viral Pipeline
Intelligent cutting based on analysis results
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

class VideoEditor:
    def __init__(self, video_path: str, analysis_path: str, output_dir: str = "./output"):
        self.video_path = Path(video_path)
        self.analysis_path = Path(analysis_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

        if not self.analysis_path.exists():
            raise FileNotFoundError(f"Analysis not found: {analysis_path}")

        # Load analysis
        with open(self.analysis_path) as f:
            self.analysis = json.load(f)

    def cut_segment(self, start: float, end: float, output_name: str,
                   speed: float = 1.0, reencode: bool = True) -> Path:
        """Cut a segment from the video"""
        output_path = self.output_dir / output_name

        duration = end - start

        print(f"✂️  Cutting {start:.1f}s → {end:.1f}s (duration: {duration:.1f}s)")

        if speed != 1.0:
            print(f"   Speed: {speed}x")

        if reencode:
            # Re-encode for quality and speed adjustment
            cmd = [
                'ffmpeg',
                '-y',
                '-ss', str(start),
                '-i', str(self.video_path),
                '-t', str(duration),
            ]

            # Speed filter
            if speed != 1.0:
                cmd.extend([
                    '-filter:v', f'setpts={1/speed}*PTS',
                    '-filter:a', f'atempo={speed}',
                ])

            # Quality settings
            cmd.extend([
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                str(output_path)
            ])
        else:
            # Fast copy (no re-encode)
            cmd = [
                'ffmpeg',
                '-y',
                '-ss', str(start),
                '-i', str(self.video_path),
                '-t', str(duration),
                '-c', 'copy',
                str(output_path)
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffmpeg failed: {result.stderr}")

        return output_path

    def add_subtitles(self, video_path: Path, subtitle_text: str,
                     output_name: str) -> Path:
        """Add hardcoded subtitles to video"""
        output_path = self.output_dir / output_name

        # Create SRT file
        srt_path = self.output_dir / f"{video_path.stem}_temp.srt"
        with open(srt_path, 'w', encoding='utf-8') as f:
            f.write("1\n")
            f.write("00:00:00,000 --> 00:00:05,000\n")
            f.write(f"{subtitle_text}\n")

        cmd = [
            'ffmpeg',
            '-y',
            '-i', str(video_path),
            '-vf', f"subtitles={srt_path}:force_style='FontName=PingFang SC,FontSize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,Outline=2,Alignment=2'",
            '-c:a', 'copy',
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        srt_path.unlink()  # Clean up temp file

        if result.returncode != 0:
            print(f"⚠️  Subtitle embedding failed: {result.stderr}", file=sys.stderr)
            return video_path

        return output_path

    def add_background_music(self, video_path: Path, music_path: Optional[str],
                            music_volume: float = 0.2, output_name: str = None) -> Path:
        """Mix background music with video audio"""
        if not music_path or not Path(music_path).exists():
            print("⚠️  No background music provided, skipping")
            return video_path

        if output_name is None:
            output_name = f"{video_path.stem}_with_music.mp4"

        output_path = self.output_dir / output_name

        cmd = [
            'ffmpeg',
            '-y',
            '-i', str(video_path),
            '-i', music_path,
            '-filter_complex',
            f'[1:a]volume={music_volume}[a1];[0:a][a1]amix=inputs=2:duration=shortest',
            '-c:v', 'copy',
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Music mixing failed: {result.stderr}", file=sys.stderr)
            return video_path

        return output_path

    def generate_viral_clip(self, duration: int = 30,
                           platform: str = 'douyin',
                           add_hook: bool = True,
                           bgm_path: Optional[str] = None) -> Dict:
        """Generate a viral short clip"""

        print(f"\n🎬 Generating {duration}s clip for {platform}")
        print("=" * 60)

        # Get recommended segment
        rec_key = f'best_{duration}s'
        if rec_key not in self.analysis['recommendations']:
            raise ValueError(f"No recommendation for {duration}s duration")

        rec = self.analysis['recommendations'][rec_key]
        start = rec['start']
        end = rec['end']

        print(f"📍 Using segment: {start:.1f}s → {end:.1f}s")
        print(f"   Reason: {rec['reason']}")

        # Step 1: Cut base segment
        base_clip = self.cut_segment(
            start, end,
            f"{self.video_path.stem}_{duration}s_base.mp4",
            speed=1.0,
            reencode=True
        )

        current_clip = base_clip

        # Step 2: Add hook (if requested)
        if add_hook:
            print("\n🎣 Adding viral hook...")
            # For now, we'll add this as a subtitle overlay
            # In production, this would be a proper intro card
            hook_text = self.generate_hook_text(duration)
            print(f"   Hook: {hook_text}")
            # Note: Real implementation would add a 3-second intro card

        # Step 3: Add background music
        if bgm_path:
            print("\n🎵 Adding background music...")
            current_clip = self.add_background_music(
                current_clip, bgm_path,
                music_volume=0.25,
                output_name=f"{self.video_path.stem}_{duration}s_with_music.mp4"
            )

        # Step 4: Platform-specific adjustments
        final_clip = self.adjust_for_platform(current_clip, platform, duration)

        # Generate metadata
        metadata = {
            'source_video': str(self.video_path),
            'duration': duration,
            'platform': platform,
            'segment': {'start': start, 'end': end},
            'output_file': str(final_clip),
            'hook_text': hook_text if add_hook else None,
            'titles': self.generate_titles(),
        }

        # Save metadata
        meta_path = self.output_dir / f"{final_clip.stem}_metadata.json"
        with open(meta_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Generated: {final_clip}")
        print(f"📄 Metadata: {meta_path}")

        return metadata

    def generate_hook_text(self, duration: int) -> str:
        """Generate viral hook based on video content"""
        filename = self.video_path.stem

        # Extract topic from filename
        if 'GPT' in filename or 'AI' in filename:
            hooks = [
                f"用AI做这个只要{duration}秒？",
                "这效果是AI生成的？",
                "没想到AI能做到这个...",
            ]
        else:
            hooks = [
                f"{duration}秒看完整个过程",
                "这个操作太狠了",
                "最后的效果惊到我了",
            ]

        return hooks[0]

    def generate_titles(self) -> list:
        """Generate multiple title variants (MrBeast formula)"""
        filename = self.video_path.stem

        titles = [
            f"用AI做电脑壁纸，{30}秒搞定",
            "AI生成壁纸 vs 手工设计，差距惊人",
            "终于发现做壁纸的秘密了...",
            "GPT做壁纸效果太炸了",
            "这个AI工具改变了我的桌面",
        ]

        return titles

    def adjust_for_platform(self, video_path: Path, platform: str, duration: int) -> Path:
        """Adjust video for platform-specific requirements"""

        specs = {
            'douyin': {'width': 1080, 'height': 1920, 'ratio': '9:16'},
            'bilibili': {'width': 1920, 'height': 1080, 'ratio': '16:9'},
            'xiaohongshu': {'width': 1080, 'height': 1440, 'ratio': '3:4'},
        }

        if platform not in specs:
            print(f"⚠️  Unknown platform: {platform}, using original format")
            return video_path

        spec = specs[platform]
        output_name = f"{video_path.stem}_{platform}.mp4"
        output_path = self.output_dir / output_name

        print(f"\n📱 Adjusting for {platform} ({spec['ratio']})...")

        # Get source dimensions
        metadata = self.analysis['metadata']
        src_width = metadata['width']
        src_height = metadata['height']

        target_width = spec['width']
        target_height = spec['height']

        # Calculate scaling to fit within target with padding
        scale_w = target_width / src_width
        scale_h = target_height / src_height
        scale = min(scale_w, scale_h)

        new_width = int(src_width * scale)
        new_height = int(src_height * scale)

        # Center and add blur background
        vf = f"scale={new_width}:{new_height},pad={target_width}:{target_height}:(ow-iw)/2:(oh-ih)/2:black"

        cmd = [
            'ffmpeg',
            '-y',
            '-i', str(video_path),
            '-vf', vf,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'copy',
            str(output_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Platform adjustment failed: {result.stderr}", file=sys.stderr)
            return video_path

        return output_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python editor.py <video_path> <analysis_json> [duration] [platform]")
        print("\nExample:")
        print("  python editor.py video.mp4 analysis.json 30 douyin")
        sys.exit(1)

    video_path = sys.argv[1]
    analysis_path = sys.argv[2]
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    platform = sys.argv[4] if len(sys.argv) > 4 else 'douyin'

    editor = VideoEditor(video_path, analysis_path)

    metadata = editor.generate_viral_clip(
        duration=duration,
        platform=platform,
        add_hook=True,
        bgm_path=None  # Add BGM path if available
    )

    print("\n" + "=" * 60)
    print("🎉 VIRAL CLIP READY")
    print("=" * 60)
    print(f"📹 Output: {metadata['output_file']}")
    print(f"⏱️  Duration: {metadata['duration']}s")
    print(f"📱 Platform: {metadata['platform']}")
    print(f"\n💡 Suggested Titles:")
    for i, title in enumerate(metadata['titles'][:3], 1):
        print(f"  {i}. {title}")


if __name__ == '__main__':
    main()
