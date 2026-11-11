"""Evidence-first 15-second product promo planning. No rendering or network calls.

Generate an inspectable shot list from a user-supplied brief and verify actual
assets and measured narration before handing the plan to a rendering engine.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil
import subprocess
import wave

ROLES = ("device", "interaction", "result")
TIMES = (3.0, 7.0, 5.0)
VISUALS = {
    "device": "Show the complete real device/browser UI before zooming; establish context.",
    "interaction": "Keep the SAME device on screen while showing one real user action.",
    "result": "Move to a legible close-up of the actual result; show proof and CTA.",
}
REQUIRED = ("product_name", "audience", "core_value", "pain_point", "cta", "platform", "aspect")


def _relative(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Asset paths must be nonempty relative paths")
    p = Path(value)
    if p.is_absolute() or ".." in p.parts or value.startswith("~"):
        raise ValueError("Only safe relative asset paths are permitted: " + value)
    return value


def _input(brief: dict) -> None:
    if not isinstance(brief, dict):
        raise ValueError("Brief must be a JSON object")
    for key in REQUIRED:
        if not isinstance(brief.get(key), str) or not brief[key].strip():
            raise ValueError("Brief requires nonempty string: " + key)
    if brief["aspect"] not in ("9:16", "16:9", "1:1", "4:3", "3:4"):
        raise ValueError("Unsupported aspect ratio")
    for field in ("source_ui", "on_screen", "voiceover", "voice_files"):
        value = brief.get(field, {})
        if not isinstance(value, dict):
            raise ValueError(field + " must be an object")
    sources = brief.get("source_ui", {})
    for role in ROLES:
        _relative(sources.get(role, ""))
    for role, value in brief.get("voice_files", {}).items():
        if role not in ROLES:
            raise ValueError("Unknown voice role: " + role)
        _relative(value)


def build_plan(brief: dict) -> dict:
    """Produce a deterministic plan, not a video, scene footage or approved claim."""
    _input(brief)
    offsets = (0.0, 3.0, 10.0)
    shots = []
    for role, start, duration in zip(ROLES, offsets, TIMES):
        shot = {
            "role": role, "start_seconds": start, "duration_seconds": duration,
            "end_seconds": start + duration,
            "device_id": brief.get("device_id", "primary-device"),
            "source_file": brief["source_ui"][role],
            "source_kind": "real-product-ui; must be visually verified",
            "visual_direction": VISUALS[role],
            "voiceover": brief.get("voiceover", {}).get(role, ""),
            "voice_file": brief.get("voice_files", {}).get(role, ""),
            "screen_text": brief.get("on_screen", {}).get(role, ""),
        }
        shots.append(shot)
    return {
        "schema_version": "1.0", "artifact_kind": "preproduction-shotlist-not-rendered",
        "status": "planned", "duration_seconds": 15.0,
        "product_name": brief["product_name"], "audience": brief["audience"],
        "core_value": brief["core_value"], "pain_point": brief["pain_point"],
        "platform": brief["platform"], "aspect": brief["aspect"], "cta": brief["cta"],
        "public_demo_data_confirmed": brief.get("public_demo_data_confirmed") is True,
        "claims": brief.get("claims", []), "shots": shots,
        "workflow": [
            "Verify real UI and a clean public demo data set; never fabricate results",
            "Measure real narration audio before adjusting the timeline",
            "Render a 15-second sample via an installed renderer (not this CLI)",
            "Review start/middle/end plus full playback; lock approved shots",
            "Expand only after the sample works; run director.py qa on the MP4",
        ],
        "handoff": {"locked_shots": [], "next_revision": "First 15s sample", "approved_voice": None},
    }


def init(brief_file: Path, out_dir: Path) -> dict:
    brief = json.loads(brief_file.read_text(encoding="utf-8"))
    plan = build_plan(brief)
    out = out_dir.expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    target = out / "product_promo_plan.json"
    if target.exists():
        raise FileExistsError("Plan exists; preserve prior approved shots: " + str(target))
    target.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    handoff = out / "HANDOFF.md"
    handoff.write_text(
        "# Product promo handoff (not rendered)\n\n"
        f"Product: {plan['product_name']}\nAudience: {plan['audience']}\n"
        f"One value: {plan['core_value']}\nCTA: {plan['cta']}\n\n"
        "## Next steps\n" + "".join(f"- {s}\n" for s in plan["workflow"]) +
        "\n## Revision log\n- Locked shots: none\n- Approved voice: pending\n",
        encoding="utf-8",
    )
    return {"status": "planned-not-rendered", "plan": str(target), "handoff": str(handoff),
            "next": "Provide real UI files and measured voice tracks; run promo-audit."}


def _asset(root: Path, name: str) -> Path:
    rel = _relative(name)
    path = (root / rel).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Asset resolves outside --assets-root: " + name)
    return path


def _audio_seconds(path: Path) -> float | None:
    if path.suffix.lower() == ".wav":
        with wave.open(str(path), "rb") as f:
            return f.getnframes() / f.getframerate()
    if not shutil.which("ffprobe"):
        return None
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                       text=True, capture_output=True, check=False)
    if p.returncode != 0:
        return None
    try:
        return float(p.stdout.strip())
    except ValueError:
        return None


def audit(plan_file: Path, assets_root: Path) -> dict:
    """Check source and voice readiness; not a substitute for visual/video QA."""
    plan = json.loads(plan_file.read_text(encoding="utf-8"))
    issues = []
    shots = plan.get("shots", [])
    if len(shots) != 3 or [s.get("role") for s in shots] != list(ROLES):
        issues.append("Expected device → interaction → result in that order")
    if len({s.get("device_id") for s in shots}) != 1:
        issues.append("Shot continuity broken: device_id must stay constant")
    elapsed = 0.0
    root = assets_root.expanduser().resolve()
    for shot in shots:
        role = shot.get("role", "unknown")
        start, seconds = shot.get("start_seconds"), shot.get("duration_seconds")
        if not isinstance(start, (int, float)) or not isinstance(seconds, (int, float)) or seconds <= 0:
            issues.append(role + ": invalid shot timing")
        elif abs(start - elapsed) > 0.01:
            issues.append(role + ": gap or overlapping shots")
        if isinstance(seconds, (int, float)):
            elapsed += seconds
        try:
            src = _asset(root, shot.get("source_file", ""))
            if not src.is_file() or src.stat().st_size == 0:
                issues.append(role + ": missing or empty real UI: " + str(src))
        except ValueError as e:
            issues.append(role + ": " + str(e))
        if len(shot.get("screen_text", "")) > 28:
            issues.append(role + ": screen text exceeds 28 characters; shorten for legibility")
        if shot.get("voiceover") and not shot.get("voice_file"):
            issues.append(role + ": narration text provided without a measured audio file")
        if shot.get("voice_file"):
            try:
                voice = _asset(root, shot["voice_file"])
                if not voice.is_file():
                    issues.append(role + ": missing voice audio: " + str(voice))
                else:
                    duration = _audio_seconds(voice)
                    if duration is None:
                        issues.append(role + ": audio duration cannot be measured (ffprobe needed)")
                    elif isinstance(seconds, (int, float)) and duration > seconds - 0.1:
                        issues.append(role + f": narration {duration:.2f}s exceeds {seconds:.2f}s shot")
            except (ValueError, wave.Error, ZeroDivisionError) as e:
                issues.append(role + ": cannot inspect voice: " + str(e))
    if abs(elapsed - 15) > 0.01:
        issues.append("Shot durations must sum to exactly 15 seconds")
    if plan.get("public_demo_data_confirmed") is not True:
        issues.append("Public/synthetic demo data has not been confirmed")
    for i, claim in enumerate(plan.get("claims", [])):
        if not isinstance(claim, dict) or not claim.get("text") or not claim.get("evidence_url"):
            issues.append(f"Claim {i+1} requires text and evidence_url")
    return {"status": "ready-for-render" if not issues else "blocked", "issues": issues,
            "checked_shots": len(shots), "limits": "Files and audio metadata only. Human review must verify UI authenticity, privacy, claims, visual quality and final playback. No video was rendered."}
