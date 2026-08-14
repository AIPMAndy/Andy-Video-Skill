#!/usr/bin/env python3
"""
Batch Processor - Process multiple recordings into viral clips
"""

import json
import sys
from pathlib import Path
from typing import List, Dict
import subprocess
from datetime import datetime

class BatchProcessor:
    def __init__(self, input_dir: str, output_dir: str = "./batch_output"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.analyzer_script = Path(__file__).parent / "analyzer.py"
        self.editor_script = Path(__file__).parent / "editor.py"

        if not self.input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")

    def find_videos(self) -> List[Path]:
        """Find all video files in input directory"""
        extensions = ['.mp4', '.mov', '.avi', '.mkv']
        videos = []

        for ext in extensions:
            videos.extend(self.input_dir.glob(f'*{ext}'))

        return sorted(videos)

    def process_video(self, video_path: Path, durations: List[int] = [30, 60],
                     platforms: List[str] = ['douyin']) -> Dict:
        """Process single video through full pipeline"""

        video_name = video_path.stem
        print(f"\n{'='*80}")
        print(f"🎬 Processing: {video_name}")
        print(f"{'='*80}")

        # Create video-specific output directory
        video_output = self.output_dir / video_name
        video_output.mkdir(exist_ok=True)

        analysis_dir = video_output / "analysis"
        clips_dir = video_output / "clips"

        results = {
            'video': str(video_path),
            'status': 'pending',
            'analysis': None,
            'clips': [],
            'errors': []
        }

        try:
            # Step 1: Analyze
            print("\n📊 Step 1: Analyzing video...")
            analysis_result = subprocess.run([
                'python3', str(self.analyzer_script),
                str(video_path),
                str(analysis_dir)
            ], capture_output=True, text=True)

            if analysis_result.returncode != 0:
                raise RuntimeError(f"Analysis failed: {analysis_result.stderr}")

            analysis_json = analysis_dir / f"{video_name}_analysis.json"
            if not analysis_json.exists():
                raise FileNotFoundError("Analysis output not found")

            results['analysis'] = str(analysis_json)
            print(f"✅ Analysis complete: {analysis_json}")

            # Step 2: Generate clips for each duration × platform
            print(f"\n✂️  Step 2: Generating clips...")

            for duration in durations:
                for platform in platforms:
                    print(f"\n  → {duration}s clip for {platform}")

                    clip_output = clips_dir / f"{duration}s_{platform}"
                    clip_output.mkdir(parents=True, exist_ok=True)

                    edit_result = subprocess.run([
                        'python3', str(self.editor_script),
                        str(video_path),
                        str(analysis_json),
                        str(duration),
                        platform
                    ], capture_output=True, text=True, cwd=str(clip_output))

                    if edit_result.returncode != 0:
                        error = f"Failed to generate {duration}s {platform} clip: {edit_result.stderr}"
                        results['errors'].append(error)
                        print(f"❌ {error}")
                        continue

                    # Find generated clip
                    generated_clips = list(clip_output.glob(f"*{platform}.mp4"))
                    if generated_clips:
                        clip_path = generated_clips[0]
                        metadata_path = clip_path.with_name(f"{clip_path.stem}_metadata.json")

                        results['clips'].append({
                            'duration': duration,
                            'platform': platform,
                            'file': str(clip_path),
                            'metadata': str(metadata_path) if metadata_path.exists() else None
                        })

                        print(f"✅ Generated: {clip_path.name}")

            results['status'] = 'success' if results['clips'] else 'failed'

        except Exception as e:
            results['status'] = 'failed'
            results['errors'].append(str(e))
            print(f"\n❌ Error: {e}")

        return results

    def process_batch(self, limit: int = None,
                     durations: List[int] = [30, 60],
                     platforms: List[str] = ['douyin'],
                     skip_existing: bool = True) -> Dict:
        """Process multiple videos"""

        videos = self.find_videos()

        if not videos:
            print(f"❌ No videos found in {self.input_dir}")
            return {}

        if limit:
            videos = videos[:limit]

        print(f"\n🎯 Found {len(videos)} videos to process")
        print(f"⚙️  Settings:")
        print(f"   Durations: {durations}")
        print(f"   Platforms: {platforms}")
        print(f"   Output: {self.output_dir}")

        batch_results = {
            'timestamp': datetime.now().isoformat(),
            'input_dir': str(self.input_dir),
            'output_dir': str(self.output_dir),
            'total_videos': len(videos),
            'settings': {
                'durations': durations,
                'platforms': platforms
            },
            'results': []
        }

        for i, video in enumerate(videos, 1):
            print(f"\n{'='*80}")
            print(f"📹 Video {i}/{len(videos)}: {video.name}")
            print(f"{'='*80}")

            # Skip if already processed
            video_output = self.output_dir / video.stem
            if skip_existing and video_output.exists():
                existing_clips = list(video_output.glob("clips/**/*.mp4"))
                if existing_clips:
                    print(f"⏭️  Skipping (already processed, found {len(existing_clips)} clips)")
                    continue

            result = self.process_video(video, durations, platforms)
            batch_results['results'].append(result)

        # Summary
        successful = sum(1 for r in batch_results['results'] if r['status'] == 'success')
        failed = sum(1 for r in batch_results['results'] if r['status'] == 'failed')
        total_clips = sum(len(r['clips']) for r in batch_results['results'])

        batch_results['summary'] = {
            'successful': successful,
            'failed': failed,
            'total_clips': total_clips
        }

        # Save batch report
        report_path = self.output_dir / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(batch_results, f, ensure_ascii=False, indent=2)

        print(f"\n{'='*80}")
        print(f"🎉 BATCH PROCESSING COMPLETE")
        print(f"{'='*80}")
        print(f"✅ Successful: {successful}/{len(videos)}")
        print(f"❌ Failed: {failed}/{len(videos)}")
        print(f"🎬 Total clips generated: {total_clips}")
        print(f"📄 Report saved: {report_path}")

        return batch_results


def main():
    if len(sys.argv) < 2:
        print("Usage: python batch_processor.py <input_dir> [options]")
        print("\nOptions:")
        print("  --output <dir>      Output directory (default: ./batch_output)")
        print("  --limit <n>         Process only first N videos")
        print("  --durations <list>  Comma-separated durations (default: 30,60)")
        print("  --platforms <list>  Comma-separated platforms (default: douyin)")
        print("\nExample:")
        print('  python batch_processor.py "/Users/andy/Documents/Andy录屏素材库" --limit 10 --durations 30,60 --platforms douyin,bilibili')
        sys.exit(1)

    input_dir = sys.argv[1]
    output_dir = "./batch_output"
    limit = None
    durations = [30, 60]
    platforms = ['douyin']

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_dir = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--durations' and i + 1 < len(sys.argv):
            durations = [int(d) for d in sys.argv[i + 1].split(',')]
            i += 2
        elif sys.argv[i] == '--platforms' and i + 1 < len(sys.argv):
            platforms = sys.argv[i + 1].split(',')
            i += 2
        else:
            i += 1

    processor = BatchProcessor(input_dir, output_dir)
    processor.process_batch(limit=limit, durations=durations, platforms=platforms)


if __name__ == '__main__':
    main()
