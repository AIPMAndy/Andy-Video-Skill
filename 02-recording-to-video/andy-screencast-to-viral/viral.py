#!/usr/bin/env python3
"""
Main entry point for Screencast-to-Viral Pipeline
Usage: python viral.py <command> [options]
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

COMMANDS = {
    'analyze': {
        'script': 'analyzer.py',
        'description': 'Analyze a screen recording to find highlights',
        'usage': 'viral.py analyze <video_path> [output_dir]'
    },
    'generate': {
        'script': 'editor.py',
        'description': 'Generate viral clip from analyzed video',
        'usage': 'viral.py generate <video_path> <analysis_json> [duration] [platform]'
    },
    'batch': {
        'script': 'batch_processor.py',
        'description': 'Process entire directory of recordings',
        'usage': 'viral.py batch <input_dir> [options]'
    },
    'doctor': {
        'script': None,
        'description': 'Check if all dependencies are installed',
        'usage': 'viral.py doctor'
    }
}

def check_dependencies():
    """Check if required tools are installed"""
    print("🔍 Checking dependencies...\n")

    checks = {
        'ffmpeg': ['ffmpeg', '-version'],
        'ffprobe': ['ffprobe', '-version'],
        'python3': ['python3', '--version'],
    }

    optional_checks = {
        'whisper': ['whisper', '--help'],
        'imagemagick': ['convert', '-version'],
    }

    all_good = True

    for name, cmd in checks.items():
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ {name:15} {version[:60]}")
        else:
            print(f"❌ {name:15} NOT FOUND")
            all_good = False

    print()

    for name, cmd in optional_checks.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {name:15} (optional)")
            else:
                print(f"⚠️  {name:15} NOT FOUND (optional)")
        except FileNotFoundError:
            print(f"⚠️  {name:15} NOT FOUND (optional)")

    print()

    if all_good:
        print("✅ All required dependencies satisfied!")
    else:
        print("❌ Some required dependencies are missing")
        print("\nInstallation instructions:")
        print("  ffmpeg: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)")
        print("  whisper: pip install openai-whisper")

    return all_good

def show_help():
    """Show help message"""
    print("🎬 Screencast-to-Viral Pipeline")
    print("=" * 60)
    print("\nCommands:\n")

    for cmd, info in COMMANDS.items():
        print(f"  {cmd:12} {info['description']}")
        print(f"               Usage: {info['usage']}")
        print()

    print("\nExamples:")
    print('  # Analyze a video')
    print('  python viral.py analyze video.mp4')
    print()
    print('  # Generate 30s clip for Douyin')
    print('  python viral.py generate video.mp4 analysis.json 30 douyin')
    print()
    print('  # Batch process first 10 videos')
    print('  python viral.py batch "/path/to/recordings" --limit 10')
    print()
    print('  # Check dependencies')
    print('  python viral.py doctor')

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == 'help' or command == '--help' or command == '-h':
        show_help()
        sys.exit(0)

    if command == 'doctor':
        check_dependencies()
        sys.exit(0)

    if command not in COMMANDS:
        print(f"❌ Unknown command: {command}")
        print(f"\nAvailable commands: {', '.join(COMMANDS.keys())}")
        sys.exit(1)

    cmd_info = COMMANDS[command]
    script = SCRIPT_DIR / cmd_info['script']

    if not script.exists():
        print(f"❌ Script not found: {script}")
        sys.exit(1)

    # Pass remaining arguments to the script
    args = ['python3', str(script)] + sys.argv[2:]

    result = subprocess.run(args)
    sys.exit(result.returncode)

if __name__ == '__main__':
    main()
