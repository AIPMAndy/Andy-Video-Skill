#!/usr/bin/env python3
"""
Render a knowledge video with voiceover using edge-tts.

Workflow:
1. Prepare project: sync template, generate App.jsx, install dependencies
2. Load JSON config
3. Extract script fields for voiceover
4. Generate voiceover segments using edge-tts
5. Align audio timeline to scene durations
6. Update App.jsx with effective scene durations
7. Render video using render-video.mjs
8. Merge video with aligned audio
"""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
TEMPLATE_DIR = SCRIPT_DIR.parent / "template"
GENERATE_VOICEOVER_SCRIPT = SCRIPT_DIR / "generate_edge_voiceover.py"
BUILD_TIMED_AUDIO_SCRIPT = SCRIPT_DIR / "build_timed_audio.py"

# Files/dirs to preserve when syncing template
PRESERVE = {"node_modules", "dist", "output", ".git", "package-lock.json"}


def sync_template(job_dir: Path) -> None:
    """
    Sync template directory to job directory, preserving certain files/dirs.

    Args:
        job_dir: Target job directory
    """
    print(f"📦 Syncing template to {job_dir}")

    # Create job_dir if it doesn't exist
    job_dir.mkdir(parents=True, exist_ok=True)

    # Copy all files from template, except preserved ones
    for item in TEMPLATE_DIR.iterdir():
        if item.name in PRESERVE:
            continue

        dest = job_dir / item.name

        if item.is_dir():
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
        else:
            shutil.copy2(item, dest)

    print(f"✅ Template synced")


def write_component(job_dir: Path, config_data: dict) -> None:
    """
    Generate App.jsx that imports KnowledgeVideoGenerator and passes config.

    Args:
        job_dir: Job directory containing the project
        config_data: Video configuration data
    """
    print("📝 Writing App.jsx")

    app_jsx = f"""import React from 'react';
import KnowledgeVideoGenerator from './knowledge-video-generator.jsx';

const config = {json.dumps(config_data, ensure_ascii=False, indent=2)};

export default function App() {{
  return <KnowledgeVideoGenerator config={{config}} />;
}}
"""

    app_path = job_dir / "src" / "App.jsx"
    app_path.write_text(app_jsx, encoding="utf-8")

    print(f"✅ App.jsx written to {app_path}")


def install_dependencies(job_dir: Path) -> None:
    """
    Install npm dependencies in the job directory.

    Args:
        job_dir: Job directory containing package.json
    """
    print("📦 Installing dependencies")

    result = subprocess.run(
        ["npm", "install"],
        cwd=job_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ npm install failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print("✅ Dependencies installed")


def generate_voiceover(script_segments: list[str], output_dir: Path) -> tuple[Path, Path, Path]:
    """
    Generate voiceover audio files for each script segment using edge-tts.

    Args:
        script_segments: List of script text segments
        output_dir: Directory to save audio files

    Returns:
        Tuple of (segments_file, manifest_file, segments_dir)
    """
    print(f"🎙️  Generating voiceover for {len(script_segments)} segments")

    output_dir.mkdir(parents=True, exist_ok=True)

    # Create segments file (text separated by \n---\n)
    segments_file = output_dir / "segments.txt"
    segments_text = "\n---\n".join(script_segments) + "\n"
    segments_file.write_text(segments_text, encoding="utf-8")

    # Set up output paths
    segments_dir = output_dir / "segments"
    manifest_file = output_dir / "manifest.json"

    # Call generate_edge_voiceover.py with correct parameters
    result = subprocess.run(
        [
            sys.executable,
            str(GENERATE_VOICEOVER_SCRIPT),
            "--segments-file", str(segments_file),
            "--output-dir", str(segments_dir),
            "--manifest", str(manifest_file),
            "--locale=zh-CN",
            "--rate=+10%",
            "--pitch=-2Hz",
            "--volume=+0%",
            "--voice=zh-CN-YunyangNeural",
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Failed to generate voiceover:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Generated voiceover segments")
    print(result.stdout)

    return segments_file, manifest_file, segments_dir


def align_audio_timeline(audio_files: list[Path], scene_durations_ms: list[int], output_dir: Path, manifest_path: Path) -> tuple[Path, list[int]]:
    """
    Align audio segments to scene durations using build_timed_audio.py.

    Args:
        audio_files: List of audio file paths
        scene_durations_ms: Target scene durations in milliseconds
        output_dir: Directory to save aligned audio
        manifest_path: Path to the audio manifest file

    Returns:
        Tuple of (aligned_audio_path, effective_scene_durations_ms)
    """
    print(f"⏱️  Aligning audio timeline")

    # Create slot durations JSON (in seconds)
    slot_durations_file = output_dir / "slot_durations.json"
    slot_durations_sec = [ms / 1000.0 for ms in scene_durations_ms]
    slot_durations_file.write_text(json.dumps(slot_durations_sec, indent=2), encoding="utf-8")

    aligned_audio = output_dir / "aligned_audio.m4a"
    effective_durations_file = output_dir / "effective_durations.json"

    # Call build_timed_audio.py
    result = subprocess.run(
        [
            sys.executable,
            str(BUILD_TIMED_AUDIO_SCRIPT),
            "--manifest", str(manifest_path),
            "--slot-durations", str(slot_durations_file),
            "--output", str(aligned_audio),
            "--effective-slot-durations-output", str(effective_durations_file),
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Failed to align audio timeline:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    # Read effective durations from output file (in seconds)
    with open(effective_durations_file, "r", encoding="utf-8") as f:
        effective_durations_sec = json.load(f)

    # Convert to milliseconds
    effective_durations = [int(sec * 1000) for sec in effective_durations_sec]

    print(f"✅ Audio aligned: {aligned_audio}")
    print(f"✅ Effective scene durations: {effective_durations}")

    return aligned_audio, effective_durations


def update_app_with_durations(job_dir: Path, effective_durations: list[int]) -> None:
    """
    Update App.jsx to include effective scene durations.

    Args:
        job_dir: Job directory
        effective_durations: List of effective scene durations in milliseconds
    """
    print("📝 Updating App.jsx with scene durations")

    app_path = job_dir / "src" / "App.jsx"
    app_content = app_path.read_text(encoding="utf-8")

    # Find the config object and add sceneDurationsMs
    # Simple approach: insert before the closing brace of config
    lines = app_content.splitlines()

    # Find the line with "const config = {"
    config_start = None
    for i, line in enumerate(lines):
        if "const config = " in line:
            config_start = i
            break

    if config_start is None:
        print("⚠️  Could not find config object in App.jsx", file=sys.stderr)
        return

    # Parse the config to add sceneDurationsMs
    # Extract the JSON part
    config_json_start = app_content.find("{", app_content.find("const config = "))
    config_json_end = app_content.find("};", config_json_start) + 1
    config_json = app_content[config_json_start:config_json_end]

    # Parse and update
    config_data = json.loads(config_json)
    config_data["sceneDurationsMs"] = effective_durations

    # Rebuild App.jsx
    new_config_json = json.dumps(config_data, ensure_ascii=False, indent=2)
    new_app_content = (
        app_content[:config_json_start] +
        new_config_json +
        app_content[config_json_end:]
    )

    app_path.write_text(new_app_content, encoding="utf-8")
    print(f"✅ App.jsx updated with scene durations")


def render_video(job_dir: Path, output_path: Path, width: int = 2400, height: int = 3200, audio_path: Path = None) -> Path:
    """
    Render video using render-video.mjs in the job directory.

    Args:
        job_dir: Job directory containing the project
        output_path: Path to save the rendered video
        width: Video width in pixels
        height: Video height in pixels
        audio_path: Optional path to audio file to merge during rendering

    Returns:
        Path to the rendered video file
    """
    print(f"🎬 Rendering video ({width}×{height})")

    # Use absolute paths to avoid path resolution issues
    job_dir_abs = job_dir.resolve()
    render_script = job_dir_abs / "scripts" / "render-video.mjs"

    if not render_script.exists():
        print(f"❌ Render script not found: {render_script}", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert output_path to absolute path as well
    output_path_abs = output_path.resolve()

    cmd = [
        "node",
        str(render_script),
        "--width", str(width),
        "--height", str(height),
        "--output", str(output_path_abs),
    ]

    # Add audio parameter if provided (use absolute path)
    if audio_path and audio_path.exists():
        audio_path_abs = audio_path.resolve()
        cmd.extend(["--audio", str(audio_path_abs)])
        print(f"🔊 Including audio: {audio_path_abs}")

    result = subprocess.run(
        cmd,
        cwd=job_dir,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Video rendering failed:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Video rendered: {output_path}")
    return output_path


def merge_video_audio(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    """
    Merge video and audio using ffmpeg.

    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Path to save merged video

    Returns:
        Path to the merged video file
    """
    print(f"🎵 Merging video and audio")

    result = subprocess.run(
        [
            "ffmpeg",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "-y",
            str(output_path),
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"❌ Failed to merge video and audio:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Video and audio merged: {output_path}")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Render knowledge video with voiceover")
    parser.add_argument("config", type=Path, help="Path to JSON config file")
    parser.add_argument("--output", type=Path, help="Output video path (default: work_dir/config_name_final.mp4)")
    parser.add_argument("--width", type=int, default=2400, help="Video width (default: 2400)")
    parser.add_argument("--height", type=int, default=3200, help="Video height (default: 3200)")
    parser.add_argument("--work-dir", type=Path, help="Working directory (default: temp dir next to config)")

    args = parser.parse_args()

    # Validate config file
    if not args.config.exists():
        print(f"❌ Config file not found: {args.config}", file=sys.stderr)
        sys.exit(1)

    # Load config
    print(f"📖 Loading config: {args.config}")
    with open(args.config, "r", encoding="utf-8") as f:
        config_data = json.load(f)

    # Set up paths
    config_name = args.config.stem
    work_dir = args.work_dir or args.config.parent / f"{config_name}_work"
    output_path = args.output or work_dir / f"{config_name}_final.mp4"

    print(f"📁 Working directory: {work_dir}")
    print(f"📁 Output path: {output_path}")

    # Step 1: Prepare project
    sync_template(work_dir)
    write_component(work_dir, config_data)
    install_dependencies(work_dir)

    # Step 2: Extract script segments
    script_segments = []
    for step in config_data.get("steps", []):
        script = step.get("script", "")
        script_segments.append(script)

    if not script_segments:
        print("⚠️  No script segments found in config", file=sys.stderr)
        sys.exit(1)

    print(f"📝 Found {len(script_segments)} script segments")

    # Step 3: Generate voiceover
    audio_dir = work_dir / "audio"
    segments_file, manifest_file, segments_dir = generate_voiceover(script_segments, audio_dir)

    # Read manifest to get audio file paths
    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    # Handle both 'segments' and 'items' keys for backward compatibility
    segments_key = "segments" if "segments" in manifest else "items"
    audio_files = [Path(segment["path"] if "path" in segment else segment["audio_path"])
                   for segment in manifest[segments_key]]
    print(f"📂 Audio files: {[f.name for f in audio_files]}")

    # Step 4: Align audio timeline
    # Use default scene durations if not specified
    default_duration = 15000  # 15 seconds
    scene_durations_ms = config_data.get("sceneDurationsMs", [default_duration] * len(script_segments))

    aligned_audio, effective_durations = align_audio_timeline(audio_files, scene_durations_ms, audio_dir, manifest_file)

    # Step 5: Update App.jsx with effective durations
    update_app_with_durations(work_dir, effective_durations)

    # Step 6: Render video with audio
    render_video(work_dir, output_path, args.width, args.height, audio_path=aligned_audio)

    print(f"\n🎉 Done! Video saved to: {output_path}")


if __name__ == "__main__":
    main()
