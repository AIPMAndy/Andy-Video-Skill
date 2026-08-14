#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def build_atempo_chain(speed_ratio: float) -> str:
    # Keep each atempo stage inside ffmpeg's most-compatible operating range.
    stages = []
    remaining = float(speed_ratio)
    while remaining > 2.0:
      stages.append("atempo=2.0")
      remaining /= 2.0
    while remaining < 0.5:
      stages.append("atempo=0.5")
      remaining /= 0.5
    stages.append(f"atempo={remaining:.6f}")
    return ",".join(stages)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))


SILENCE_START_RE = re.compile(r"silence_start:\s*(?P<value>-?\d+(?:\.\d+)?)")
SILENCE_END_RE = re.compile(r"silence_end:\s*(?P<value>-?\d+(?:\.\d+)?)")


def probe_duration(audio_path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return float(result.stdout.strip())


def detect_terminal_silence(
    audio_path: Path,
    noise_db: float = -40.0,
    min_silence_duration: float = 0.12,
    source_duration: float = None,
):
    duration = float(source_duration) if source_duration is not None else probe_duration(audio_path)
    result = subprocess.run(
        [
            "ffmpeg",
            "-i",
            str(audio_path),
            "-af",
            f"silencedetect=noise={noise_db:.1f}dB:d={min_silence_duration:.3f}",
            "-f",
            "null",
            "-",
        ],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    trim_start = 0.0
    trim_end = duration
    last_silence = None
    pending_start = None

    for line in result.stdout.splitlines():
        start_match = SILENCE_START_RE.search(line)
        if start_match:
            pending_start = float(start_match.group("value"))
            continue

        end_match = SILENCE_END_RE.search(line)
        if end_match and pending_start is not None:
            silence_end = float(end_match.group("value"))
            last_silence = (pending_start, silence_end)
            if pending_start <= 0.02:
                trim_start = max(trim_start, silence_end)
            pending_start = None

    if last_silence is not None:
        silence_start, silence_end = last_silence
        if duration - silence_end <= 0.05:
            trim_end = min(trim_end, silence_start)

    if trim_end - trim_start <= 0.02:
        return 0.0, duration
    return trim_start, trim_end


def compute_effective_slot_duration(
    content_duration: float,
    target_slot_duration: float,
    max_tail_padding: float,
    min_slot_duration: float,
    minimum_tail_padding: float,
) -> float:
    effective_slot_duration = float(target_slot_duration)
    minimum_tail_padding = max(0.0, float(minimum_tail_padding))
    if minimum_tail_padding > 0.0:
        minimum_scene_duration = max(
            min_slot_duration,
            content_duration + minimum_tail_padding,
        )
        if effective_slot_duration < minimum_scene_duration:
            return minimum_scene_duration

    if content_duration < target_slot_duration - max_tail_padding:
        effective_slot_duration = max(
            min_slot_duration,
            content_duration + max_tail_padding,
        )
    return max(min_slot_duration, effective_slot_duration)


def compute_reserved_tail_padding(
    content_duration: float,
    effective_slot_duration: float,
    preferred_tail_padding: float,
) -> float:
    preferred_tail_padding = max(0.0, float(preferred_tail_padding))
    if preferred_tail_padding <= 0.0:
        return 0.0
    if content_duration >= effective_slot_duration - preferred_tail_padding:
        return preferred_tail_padding
    return 0.0


def build_trim_filters(trim_start: float, trim_end: float, source_duration: float):
    if trim_start <= 0.001 and trim_end >= source_duration - 0.001:
        return []

    trim_args = []
    if trim_start > 0.001:
        trim_args.append(f"start={trim_start:.6f}")
    if trim_end < source_duration - 0.001:
        trim_args.append(f"end={trim_end:.6f}")
    return [f"atrim={':'.join(trim_args)}", "asetpts=PTS-STARTPTS"]


def main():
    parser = argparse.ArgumentParser(
        description="Build a single narration track from segmented clips and target slot durations."
    )
    parser.add_argument("--manifest", required=True, help="Manifest JSON produced by the segmented narration generator.")
    parser.add_argument("--slot-durations", required=True, help="JSON file with an array of slot durations in seconds.")
    parser.add_argument("--output", required=True, help="Output narration track path, usually .m4a")
    parser.add_argument(
        "--underflow-mode",
        choices=["pad-end", "pad-start", "stretch"],
        default="pad-end",
        help="How to handle narration that is shorter than its target scene slot. pad-end starts immediately and pads the scene tail.",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=48000,
        help="Output sample rate for each slot and the final narration track.",
    )
    parser.add_argument(
        "--gain",
        type=float,
        default=1.0,
        help="Linear volume gain applied to the final narration track.",
    )
    parser.add_argument(
        "--max-tail-padding",
        type=float,
        default=0.55,
        help="Maximum silence allowed at the end of a slot before the slot is shrunk to stay tight.",
    )
    parser.add_argument(
        "--minimum-tail-padding",
        type=float,
        default=0.55,
        help="Minimum breathing room to preserve after each narration segment by expanding crowded scene slots.",
    )
    parser.add_argument(
        "--min-slot-duration",
        type=float,
        default=0.0,
        help="Lower bound when shrinking slots to reduce dead air.",
    )
    parser.add_argument(
        "--preferred-tail-padding",
        type=float,
        default=0.0,
        help="Preferred end-of-scene breathing room added for crowded narration when possible.",
    )
    parser.add_argument(
        "--effective-slot-durations-output",
        help="Optional JSON path that receives the effective slot durations actually used after tightening.",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    slot_path = Path(args.slot_durations).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    tmp_dir = output_path.parent / f"{output_path.stem}-slots"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slot_durations = json.loads(slot_path.read_text(encoding="utf-8"))
    items = manifest["items"]
    if len(items) != len(slot_durations):
        raise SystemExit("The number of slot durations must match the number of voice segments.")

    concat_lines = []
    diagnostics = []
    effective_slot_durations = []
    max_tail_padding = max(0.0, float(args.max_tail_padding))
    min_slot_duration = max(0.0, float(args.min_slot_duration))
    preferred_tail_padding = max(0.0, float(args.preferred_tail_padding))
    minimum_tail_padding = max(0.0, float(args.minimum_tail_padding))

    for item, slot_duration in zip(items, slot_durations):
        target_slot_duration = float(slot_duration)
        source_duration = float(item["duration_sec"])
        slot_output = tmp_dir / f"slot-{item['index']:02d}.m4a"
        trim_start, trim_end = detect_terminal_silence(
            Path(item["audio_path"]),
            source_duration=source_duration,
        )
        content_duration = max(trim_end - trim_start, 0.0)
        if content_duration <= 0.02:
            trim_start = 0.0
            trim_end = source_duration
            content_duration = source_duration

        effective_slot_duration = compute_effective_slot_duration(
            content_duration=content_duration,
            target_slot_duration=target_slot_duration,
            max_tail_padding=max_tail_padding,
            min_slot_duration=min_slot_duration,
            minimum_tail_padding=minimum_tail_padding,
        )
        effective_slot_durations.append(round(effective_slot_duration, 6))

        reserved_tail_padding = compute_reserved_tail_padding(
            content_duration=content_duration,
            effective_slot_duration=effective_slot_duration,
            preferred_tail_padding=preferred_tail_padding,
        )
        spoken_slot_duration = max(
            effective_slot_duration - reserved_tail_padding,
            min_slot_duration,
        )
        speed_ratio = content_duration / spoken_slot_duration
        audio_filters = build_trim_filters(trim_start, trim_end, source_duration)
        if content_duration > spoken_slot_duration + 0.01:
            # Speed up overlong narration so it fits the scene timing.
            audio_filters.append(build_atempo_chain(speed_ratio))
            audio_filters.extend(["apad", f"atrim=0:{spoken_slot_duration:.3f}"])
        elif content_duration < spoken_slot_duration - 0.01:
            if args.underflow_mode == "stretch":
                audio_filters.append(build_atempo_chain(speed_ratio))
                audio_filters.extend(["apad", f"atrim=0:{spoken_slot_duration:.3f}"])
            elif args.underflow_mode == "pad-end":
                audio_filters.extend(["apad", f"atrim=0:{spoken_slot_duration:.3f}"])
            else:
                # Keep already-fast narration intact, but right-align it in the slot
                # so it lands close to the slide transition instead of leaving a
                # long dead-air tail.
                delay_ms = int(round((spoken_slot_duration - content_duration) * 1000))
                audio_filters.extend(
                    [
                        f"adelay={delay_ms}|{delay_ms}",
                        "apad",
                        f"atrim=0:{spoken_slot_duration:.3f}",
                    ]
                )
        else:
            audio_filters.extend(["apad", f"atrim=0:{spoken_slot_duration:.3f}"])
        if reserved_tail_padding > 0.0:
            tail_delay_ms = int(round(reserved_tail_padding * 1000))
            audio_filters.extend(
                [
                    f"apad=pad_dur={reserved_tail_padding:.3f}",
                    f"atrim=0:{effective_slot_duration:.3f}",
                ]
            )
        run(
            [
                "ffmpeg",
                "-y",
                "-i",
                item["audio_path"],
                "-af",
                ",".join(audio_filters),
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                str(args.sample_rate),
                str(slot_output),
            ]
        )
        concat_lines.append(f"file '{slot_output.as_posix()}'")
        diagnostics.append(
            {
                "index": item["index"],
                "source_duration_sec": round(source_duration, 6),
                "content_duration_sec": round(content_duration, 6),
                "target_slot_duration_sec": round(target_slot_duration, 6),
                "effective_slot_duration_sec": round(effective_slot_duration, 6),
                "spoken_slot_duration_sec": round(spoken_slot_duration, 6),
                "reserved_tail_padding_sec": round(reserved_tail_padding, 6),
                "source_tail_padding_sec": round(max(effective_slot_duration - source_duration, 0.0), 6),
                "tail_padding_sec": round(max(effective_slot_duration - spoken_slot_duration, 0.0), 6),
                "speed_ratio": round(speed_ratio, 6),
                "trim_start_sec": round(trim_start, 6),
                "trim_end_sec": round(trim_end, 6),
            }
        )

    concat_file = tmp_dir / "concat.txt"
    concat_file.write_text("\n".join(concat_lines), encoding="utf-8")
    diagnostics_path = output_path.parent / f"{output_path.stem}-diagnostics.json"
    diagnostics_path.write_text(
        json.dumps(
            {
                "underflow_mode": args.underflow_mode,
                "max_tail_padding": max_tail_padding,
                "minimum_tail_padding": minimum_tail_padding,
                "min_slot_duration": min_slot_duration,
                "preferred_tail_padding": preferred_tail_padding,
                "items": diagnostics,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    if args.effective_slot_durations_output:
        effective_slot_path = Path(args.effective_slot_durations_output).expanduser().resolve()
        effective_slot_path.parent.mkdir(parents=True, exist_ok=True)
        effective_slot_path.write_text(
            json.dumps(effective_slot_durations, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    run(
        [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-af",
            f"volume={args.gain:.4f}",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            str(args.sample_rate),
            "-movflags",
            "+faststart",
            str(output_path),
        ]
    )
    print(output_path)


if __name__ == "__main__":
    main()
