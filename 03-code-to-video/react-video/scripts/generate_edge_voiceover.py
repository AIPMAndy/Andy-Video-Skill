#!/usr/bin/env python3
import argparse
import asyncio
import inspect
import json
import subprocess
from pathlib import Path

import edge_tts


DEFAULT_LOCALE = "zh-CN"
DEFAULT_VOICE = "zh-CN-YunyangNeural"
DEFAULT_RATE = "+10%"
DEFAULT_PITCH = "-2Hz"
DEFAULT_VOLUME = "+0%"


def probe_duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def load_segments(path: Path):
    text = path.read_text(encoding="utf-8").strip()
    return [segment.strip() for segment in text.split("\n---\n") if segment.strip()]


def choose_voice(requested_voice, requested_locale, voices=None):
    if requested_voice:
        return requested_voice

    if voices is None:
        voices = asyncio.run(edge_tts.list_voices())

    exact = next(
        (
            voice["ShortName"]
            for voice in voices
            if voice.get("Locale") == requested_locale
        ),
        None,
    )
    if exact:
        return exact

    language_prefix = requested_locale.split("-", 1)[0]
    language_match = next(
        (
            voice["ShortName"]
            for voice in voices
            if voice.get("Locale", "").startswith(f"{language_prefix}-")
        ),
        None,
    )
    if language_match:
        return language_match

    if voices:
        return voices[0]["ShortName"]
    raise SystemExit("edge-tts did not return any available voices.")


async def synthesize_segment(index, text, output_dir, voice, rate, pitch, volume):
    audio_path = output_dir / f"step-{index:02d}.mp3"
    kwargs = {
        "text": text,
        "voice": voice,
        "rate": rate,
        "pitch": pitch,
        "volume": volume,
    }
    supported = inspect.signature(edge_tts.Communicate).parameters
    communicate = edge_tts.Communicate(
        **{key: value for key, value in kwargs.items() if key in supported}
    )
    await communicate.save(str(audio_path))
    return {
        "index": index,
        "text": text,
        "audio_path": str(audio_path),
        "duration_sec": probe_duration(audio_path),
    }


async def run_generation(args):
    segments_file = Path(args.segments_file).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    manifest_path = Path(args.manifest).expanduser().resolve()

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    selected_voice = choose_voice(args.voice, args.locale)
    items = []
    for index, text in enumerate(load_segments(segments_file)):
        items.append(
            await synthesize_segment(
                index=index,
                text=text,
                output_dir=output_dir,
                voice=selected_voice,
                rate=args.rate,
                pitch=args.pitch,
                volume=args.volume,
            )
        )

    manifest_path.write_text(
        json.dumps(
            {
                "provider": "edge-tts",
                "voice": selected_voice,
                "locale": args.locale,
                "rate": args.rate,
                "pitch": args.pitch,
                "volume": args.volume,
                "items": items,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(manifest_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate per-scene edge-tts narration audio from a segmented subtitle file."
    )
    parser.add_argument("--segments-file", required=True, help="Subtitle file split by --- separators.")
    parser.add_argument("--output-dir", required=True, help="Directory for generated audio segments.")
    parser.add_argument("--manifest", required=True, help="Manifest JSON output path.")
    parser.add_argument("--voice", help="Exact edge-tts voice name, for example zh-CN-YunyangNeural.")
    parser.add_argument("--locale", default=DEFAULT_LOCALE, help="Preferred locale when auto-selecting a voice.")
    parser.add_argument("--rate", default=DEFAULT_RATE, help="edge-tts rate value, for example +10%%.")
    parser.add_argument("--pitch", default=DEFAULT_PITCH, help="edge-tts pitch value, for example -2Hz.")
    parser.add_argument("--volume", default=DEFAULT_VOLUME, help="edge-tts volume value, for example +0%%.")
    args = parser.parse_args()

    asyncio.run(run_generation(args))


if __name__ == "__main__":
    main()
