#!/usr/bin/env python3
"""
Screencast Analyzer - Phase 1 of Viral Pipeline
Extracts metadata, transcribes audio, identifies highlights
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import re

class ScreencastAnalyzer:
    def __init__(self, video_path: str, output_dir: str = "./analysis"):
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {video_path}")

    def extract_metadata(self) -> Dict:
        """Extract video metadata using ffprobe"""
        cmd = [
            'ffprobe',
            '-v', 'quiet',
            '-print_format', 'json',
            '-show_format',
            '-show_streams',
            str(self.video_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe failed: {result.stderr}")

        data = json.loads(result.stdout)

        # Extract key info
        video_stream = next((s for s in data['streams'] if s['codec_type'] == 'video'), None)
        audio_stream = next((s for s in data['streams'] if s['codec_type'] == 'audio'), None)

        metadata = {
            'filename': self.video_path.name,
            'duration': float(data['format']['duration']),
            'size_mb': float(data['format']['size']) / (1024 * 1024),
            'has_audio': audio_stream is not None,
        }

        if video_stream:
            metadata.update({
                'width': int(video_stream['width']),
                'height': int(video_stream['height']),
                'fps': eval(video_stream.get('r_frame_rate', '30/1')),
            })

        return metadata

    def extract_audio(self) -> Optional[Path]:
        """Extract audio track to MP3"""
        audio_path = self.output_dir / f"{self.video_path.stem}_audio.mp3"

        cmd = [
            'ffmpeg',
            '-y',
            '-i', str(self.video_path),
            '-vn',
            '-acodec', 'libmp3lame',
            '-q:a', '2',
            str(audio_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Audio extraction failed: {result.stderr}", file=sys.stderr)
            return None

        return audio_path

    def transcribe_audio(self, audio_path: Path) -> Dict:
        """Transcribe audio using Whisper"""
        print(f"🎤 Transcribing audio with Whisper...")

        # Check if whisper is available
        whisper_check = subprocess.run(['which', 'whisper'], capture_output=True)
        if whisper_check.returncode != 0:
            print("⚠️  Whisper not found. Install with: pip install openai-whisper")
            return {'text': '', 'language': 'unknown', 'segments': []}

        output_prefix = self.output_dir / self.video_path.stem

        cmd = [
            'whisper',
            str(audio_path),
            '--language', 'Chinese',
            '--model', 'medium',
            '--output_format', 'json',
            '--output_dir', str(self.output_dir)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️  Whisper failed: {result.stderr}", file=sys.stderr)
            return {'text': '', 'language': 'unknown', 'segments': []}

        # Read Whisper output
        json_path = output_prefix.with_suffix('.json')
        if json_path.exists():
            with open(json_path) as f:
                whisper_data = json.load(f)
            return whisper_data

        return {'text': '', 'language': 'unknown', 'segments': []}

    def extract_keyframes(self, fps: float = 0.5, max_frames: int = 50) -> Path:
        """Extract keyframes at specified fps"""
        frames_dir = self.output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)

        print(f"📸 Extracting keyframes at {fps} fps...")

        cmd = [
            'ffmpeg',
            '-y',
            '-i', str(self.video_path),
            '-vf', f'fps={fps}',
            str(frames_dir / 'frame_%04d.jpg')
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Frame extraction failed: {result.stderr}")

        return frames_dir

    def analyze_highlights(self, metadata: Dict, transcription: Dict) -> List[Dict]:
        """Identify potential highlight moments"""
        highlights = []
        duration = metadata['duration']

        # Strategy 1: High speech density (words per second)
        if transcription.get('segments'):
            for seg in transcription['segments']:
                start = seg['start']
                end = seg['end']
                text = seg['text']

                # Calculate word density
                words = len(text.split())
                seg_duration = end - start
                if seg_duration > 0:
                    wps = words / seg_duration

                    # High density = exciting moment
                    if wps > 3.0:  # > 3 words per second
                        highlights.append({
                            'start': start,
                            'end': end,
                            'score': min(wps / 5.0, 1.0),
                            'reason': 'High speech density',
                            'type': 'excited_speech',
                            'text': text.strip()
                        })

        # Strategy 2: Keywords detection
        excitement_keywords = ['哇', '太', '真的', '竟然', '没想到', '成功', '完成', '看', '效果']
        for seg in transcription.get('segments', []):
            text = seg['text'].lower()
            keyword_count = sum(1 for kw in excitement_keywords if kw in text)

            if keyword_count >= 2:
                highlights.append({
                    'start': seg['start'],
                    'end': seg['end'],
                    'score': min(keyword_count / 3.0, 1.0),
                    'reason': f'Contains {keyword_count} excitement keywords',
                    'type': 'keyword_match',
                    'text': seg['text'].strip()
                })

        # Strategy 3: Beginning and end (often have intro/result)
        if duration > 30:
            highlights.append({
                'start': 0,
                'end': min(15, duration),
                'score': 0.6,
                'reason': 'Intro segment',
                'type': 'intro'
            })

            highlights.append({
                'start': max(0, duration - 30),
                'end': duration,
                'score': 0.7,
                'reason': 'Ending segment (likely result)',
                'type': 'result'
            })

        # Sort by score
        highlights.sort(key=lambda x: x['score'], reverse=True)

        return highlights

    def recommend_cuts(self, metadata: Dict, highlights: List[Dict]) -> Dict:
        """Generate cutting recommendations for different durations"""
        duration = metadata['duration']

        recommendations = {}

        # Find best continuous segments
        if highlights:
            # 30s: Single best highlight
            best = highlights[0]
            start_30 = max(0, best['start'] - 5)
            end_30 = min(duration, start_30 + 30)
            recommendations['best_30s'] = {
                'start': round(start_30, 2),
                'end': round(end_30, 2),
                'reason': f"Centers on: {best.get('reason', 'top highlight')}"
            }

            # 60s: Extended version
            start_60 = max(0, best['start'] - 10)
            end_60 = min(duration, start_60 + 60)
            recommendations['best_60s'] = {
                'start': round(start_60, 2),
                'end': round(end_60, 2),
                'reason': 'Extended context around best highlight'
            }

            # 90s: Full story
            # Try to include intro + highlight + result
            intro_highlights = [h for h in highlights if h['type'] == 'intro']
            result_highlights = [h for h in highlights if h['type'] == 'result']

            if intro_highlights and result_highlights:
                start_90 = intro_highlights[0]['start']
                end_90 = min(duration, start_90 + 90)
                recommendations['best_90s'] = {
                    'start': round(start_90, 2),
                    'end': round(end_90, 2),
                    'reason': 'Full story: intro → highlights → result'
                }
            else:
                start_90 = max(0, best['start'] - 20)
                end_90 = min(duration, start_90 + 90)
                recommendations['best_90s'] = {
                    'start': round(start_90, 2),
                    'end': round(end_90, 2),
                    'reason': 'Extended segment with context'
                }
        else:
            # Fallback: use middle section
            mid = duration / 2
            recommendations = {
                'best_30s': {'start': max(0, mid - 15), 'end': min(duration, mid + 15)},
                'best_60s': {'start': max(0, mid - 30), 'end': min(duration, mid + 30)},
                'best_90s': {'start': max(0, mid - 45), 'end': min(duration, mid + 45)},
            }

        return recommendations

    def analyze(self, extract_frames: bool = True) -> Dict:
        """Run complete analysis pipeline"""
        print(f"🎬 Analyzing: {self.video_path.name}")
        print("=" * 60)

        # Step 1: Metadata
        print("📊 Extracting metadata...")
        metadata = self.extract_metadata()
        print(f"   Duration: {metadata['duration']:.1f}s")
        print(f"   Resolution: {metadata.get('width', '?')}x{metadata.get('height', '?')}")
        print(f"   Size: {metadata['size_mb']:.1f} MB")
        print(f"   Has audio: {metadata['has_audio']}")

        # Step 2: Audio extraction
        audio_path = None
        transcription = {'text': '', 'segments': []}

        if metadata['has_audio']:
            print("\n🎵 Extracting audio...")
            audio_path = self.extract_audio()

            if audio_path:
                # Step 3: Transcription
                transcription = self.transcribe_audio(audio_path)
                if transcription.get('text'):
                    print(f"   Transcribed {len(transcription['text'])} characters")
                    print(f"   Language: {transcription.get('language', 'unknown')}")

        # Step 4: Keyframes
        frames_dir = None
        if extract_frames:
            frames_dir = self.extract_keyframes()
            frame_count = len(list(frames_dir.glob('*.jpg')))
            print(f"   Extracted {frame_count} frames")

        # Step 5: Highlight analysis
        print("\n🔍 Analyzing highlights...")
        highlights = self.analyze_highlights(metadata, transcription)
        print(f"   Found {len(highlights)} potential highlights")

        # Step 6: Cutting recommendations
        print("\n✂️  Generating recommendations...")
        recommendations = self.recommend_cuts(metadata, highlights)

        for duration, cut in recommendations.items():
            print(f"   {duration}: {cut['start']:.1f}s - {cut['end']:.1f}s")

        # Compile results
        result = {
            'source': str(self.video_path),
            'metadata': metadata,
            'transcription': transcription.get('text', ''),
            'segments': transcription.get('segments', []),
            'highlights': highlights[:10],  # Top 10
            'recommendations': recommendations,
            'frames_dir': str(frames_dir) if frames_dir else None,
            'audio_file': str(audio_path) if audio_path else None
        }

        # Save to JSON
        output_path = self.output_dir / f"{self.video_path.stem}_analysis.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✅ Analysis complete: {output_path}")

        return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python analyzer.py <video_path> [output_dir]")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./analysis"

    analyzer = ScreencastAnalyzer(video_path, output_dir)
    result = analyzer.analyze()

    # Print summary
    print("\n" + "=" * 60)
    print("📋 ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Video: {result['metadata']['filename']}")
    print(f"Duration: {result['metadata']['duration']:.1f}s")
    print(f"Top Highlights:")
    for i, h in enumerate(result['highlights'][:5], 1):
        print(f"  {i}. {h['start']:.1f}s - {h['end']:.1f}s (score: {h['score']:.2f})")
        print(f"     {h['reason']}")
        if h.get('text'):
            print(f"     \"{h['text'][:60]}...\"")

    print(f"\n💡 Recommended cuts:")
    for duration, cut in result['recommendations'].items():
        print(f"  {duration}: {cut['start']:.1f}s → {cut['end']:.1f}s")


if __name__ == '__main__':
    main()
