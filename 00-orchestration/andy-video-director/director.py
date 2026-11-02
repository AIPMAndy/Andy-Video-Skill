#!/usr/bin/env python3
"""Andy Video Director: deterministic, auditable planner and opt-in installer.

No API keys required for planning. This utility does not hallucinate finished
videos or silently execute third-party software. An AI Agent reads SKILL.md
and implements the returned plan, invoking installed upstream Skills.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
REGISTRY = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
ENGINES = {e["id"]: e for e in REGISTRY["engines"]}
STYLES = {
    "whiteboard", "riso", "ink", "launch", "origami", "pop", "op",
    "cutout", "ascii", "shadow", "bauhaus", "pixel", "chat", "toy3d",
    "newsreel", "filmroom", "mystery", "isometric", "trailer", "dossier",
    "manga", "map", "swiss", "lumen", "blueprint", "collage", "grain",
    "storybook", "tapestry", "parable",
}
WORDS = {
    "recording": r"录屏|直播回放|长视频|视频切片|切条|剪辑现有|screencast|recording|repurpose",
    "avatar": r"数字人|口型|对口型|照片说话|lip.sync|talking.head|liveportrait|sadtalker",
    "generative": r"文生视频|图生视频|图片生成视频|电影级镜头|生成写实镜头|text.to.video|image.to.video|cinematic footage",
    "react": r"react|remotion|jsx|tsx|前端组件|网页转视频|程序化动效",
    "math": r"manim|数学动画|数学公式|公式推导|3blue1brown|几何证明",
    "product": r"网站宣传|产品宣传|app宣传|发布片|发布会|产品演示|软件介绍|launch|promo|saas",
    "short": r"口播|短视频|无露脸|批量生成|一键成片|自动找素材|faceless|stock footage|批量短视频",
    "explainer": r"科普|知识视频|解释|原理|讲解|冷知识|教程|explain|education|whiteboard",
    "localize": r"视频翻译|配音翻译|多语言配音|翻译视频|localiz|dub|translate",
    "edit": r"去停顿|去静音|自动剪辑|跳剪|silence|autocut|auto.edit",
    "blender": r"blender|三维建模|3d建模|3d 建模",
    "threejs": r"three\.js|threejs|webgl|网页三维",
    "motion_graphics": r"ui动效|界面动效|anime\.js|animejs|\bmotion\b|动画转场|微交互",
    "lottie": r"lottie|矢量动画|json动画|json 动画",
    "beat": r"音乐卡点|音乐节拍|自动卡点|跟着音乐|节奏同步|beat.sync|beat sync|music.sync",
    "voiceover": r"配音|旁白|tts|语音合成|voiceover|narration",
    "visual_fx": r"辉光|景深|\bbloom\b|postprocessing|后期特效",
    "captions_only": r"生成字幕|自动字幕|加字幕|字幕对齐|caption|subtitle",
}
STYLE_RE = re.compile(r"^[a-z][a-z0-9-]{1,35}$")


def detect(request: str) -> dict:
    q = request.casefold()
    return {k: bool(re.search(p, q)) for k, p in WORDS.items()}


def installed_path(e: dict, skill_home: Path | None = None) -> Path:
    home = skill_home or Path(os.environ.get("ANDY_VIDEO_SKILL_HOME", str(Path.home() / ".claude" / "skills")))
    if e["kind"] == "builtin-skill":
        return ROOT.parent.parent / e["skill_path"]
    return home / e["id"]


def availability(e: dict) -> str:
    if e["kind"] == "builtin-skill":
        return "bundled" if installed_path(e).exists() else "unavailable"
    if e["kind"] in ("agent-skill", "agent-skill-pack"):
        return "installed" if installed_path(e).exists() else "needs-bootstrap"
    return "external-engine; setup required"


def route(request: str, gpu: bool = False, prefer: str | None = None, offline: bool = False) -> dict:
    tags = detect(request)
    if prefer:
        if prefer not in ENGINES:
            raise ValueError("Unknown engine: " + prefer)
        primary = prefer
    elif tags["recording"]:
        primary = "andy-screencast-to-viral"
    elif tags["avatar"]:
        primary = "liveportrait"
    elif tags["localize"]:
        primary = "videolingo"
    elif tags["generative"]:
        primary = "wan2.2" if gpu else "comfyui"
    elif tags["math"]:
        primary = "andy-manim-video"
    elif tags["blender"]:
        primary = "blender-mcp"
    elif tags["threejs"]:
        primary = "threejs"
    elif tags["lottie"] and not tags["product"]:
        primary = "lottie-web"
    elif tags["react"] or tags["motion_graphics"] or tags["visual_fx"]:
        primary = "remotion-skills"
    elif tags["product"]:
        primary = "bb-video"
    elif tags["short"] and not tags["explainer"]:
        primary = "moneyprinterturbo-video"
    else:
        primary = "bb-video"
    if offline and primary == "moneyprinterturbo-video":
        primary = "bb-video"
    if not gpu and ENGINES[primary]["hardware"] == "gpu":
        reason = "GPU or managed inference endpoint is required; no generation was executed."
    else:
        reason = "Selected by deterministic intent rules; verify suitability before running."
    steps = [
        {"stage": "brief", "operator": "agent", "action": "Confirm source facts, rights, language, audience, duration, aspect and CTA.", "status": "planned"},
        {"stage": "storyboard", "operator": "agent", "action": "Write evidence-backed script, shots, title and visual information map.", "status": "planned"},
        {"stage": "production", "operator": primary, "action": "Read the selected Skill/engine's own instructions; set up dependencies and execute locally if available.", "status": availability(ENGINES[primary])},
    ]
    if tags["recording"] or tags["localize"] or tags["captions_only"]:
        steps.insert(1, {"stage": "transcript", "operator": "whisperx", "action": "When source speech exists, transcribe and align word timestamps.", "status": availability(ENGINES["whisperx"])})
    if tags["beat"]:
        steps.insert(-1, {"stage": "beat-analysis", "operator": "librosa", "action": "Analyze authorized user-supplied music before editing; actual timestamps require execution.", "status": availability(ENGINES["librosa"])})
    if tags["motion_graphics"]:
        motion_engine = "animejs" if re.search(r"anime\.js|animejs", request, re.IGNORECASE) else "motion"
        steps.append({"stage": "motion", "operator": motion_engine, "action": "Compose the library in a real browser/React video renderer. A UI animation library alone does not produce an MP4.", "status": availability(ENGINES[motion_engine])})
    if tags["visual_fx"]:
        steps.append({"stage": "effects", "operator": "postprocessing", "action": "Configure actual WebGL effects after checking GPU and renderer compatibility.", "status": availability(ENGINES["postprocessing"])})
    if tags["lottie"]:
        steps.append({"stage": "vector", "operator": "lottie-web", "action": "Render licensed Lottie JSON and capture it into a video composition.", "status": availability(ENGINES["lottie-web"])})
    chinese_voice = bool(re.search(r"中文|普通话|汉语|chinese|mandarin", request, re.IGNORECASE))
    if tags["voiceover"] or (chinese_voice and (tags["explainer"] or tags["short"])):
        steps.append({"stage": "voice", "operator": "cosyvoice", "action": "Optional local TTS; setup weights and compute, verify reference voice consent and audio output.", "status": availability(ENGINES["cosyvoice"])})
    elif primary not in ("bb-video", "moneyprinterturbo-video") and (tags["explainer"] or tags["short"]):
        steps.append({"stage": "voice", "operator": "edge-tts", "action": "Optional consented online TTS (text goes to a third-party service).", "status": availability(ENGINES["edge-tts"])})
    if tags["short"] or tags["recording"] or tags["localize"] or tags["captions_only"]:
        steps.append({"stage": "captions", "operator": "whisperx", "action": "Create, align and review subtitles; do not infer timings without audio.", "status": availability(ENGINES["whisperx"])})
    if primary in ("blender-mcp", "threejs", "lottie-web"):
        steps.append({"stage": "composition", "operator": "ffmpeg / compatible renderer", "action": "Render actual frames and compose a playable video, with rights and playback QA.", "status": "planned; renderer setup required"})
    steps.append({"stage": "quality", "operator": "agent + ffprobe", "action": "Verify duration, aspect ratio, codec, audio, black frames, safe area, citations and licensing.", "status": "planned"})
    e = ENGINES[primary]
    fallbacks = {
        "bb-video": ["react-video", "remotion-skills"],
        "moneyprinterturbo-video": ["bb-video", "ai-video-producer"],
        "remotion-skills": ["react-video", "bb-video"],
        "wan2.2": ["ltx-2", "comfyui", "bb-video"],
        "comfyui": ["wan2.2", "ltx-2", "bb-video"],
        "andy-screencast-to-viral": ["auto-editor", "moviepy"],
        "blender-mcp": ["threejs", "bb-video"],
        "threejs": ["blender-mcp", "remotion-skills"],
        "lottie-web": ["remotion-skills", "react-video"],
    }.get(primary, ["bb-video", "react-video"])
    skill_dir = installed_path(e) if e["kind"] in ("agent-skill", "agent-skill-pack", "builtin-skill") else None
    entrypoint = None
    if skill_dir is not None:
        if e["kind"] == "agent-skill-pack":
            entrypoint = skill_dir / "remotion-best-practices" / "SKILL.md"
        else:
            for candidate in ("SKILL.md", "skill.md"):
                if (skill_dir / candidate).is_file():
                    entrypoint = skill_dir / candidate
                    break
    return {
        "request": request, "pipeline_version": "0.3.0",
        "candidate_registry_count": len(ENGINES),
        "selected": primary, "selected_repo": e["repo"],
        "entrypoint": str(entrypoint) if entrypoint else None,
        "selected_kind": e["kind"], "status": availability(e), "reason": reason,
        "needs_gpu": e["hardware"] == "gpu", "offline_requested": offline,
        "stages": steps, "fallbacks": fallbacks,
        "execution": ("Agent must follow " + e.get("skill_path", "upstream documentation") +
                      "; the plan is not a finished video."),
        "gate": "Require rights/licensing review and actual runtime checks; never claim rendered or benchmarked without evidence."
    }


def doctor() -> dict:
    binaries = {"git": "git", "node": "node", "python3": "python3",
                "ffmpeg": "ffmpeg", "ffprobe": "ffprobe", "chrome": "google-chrome",
                "chromium": "chromium", "nvidia-smi": "nvidia-smi", "uv": "uv",
                "blender": "blender", "sox": "sox"}
    found = {k: shutil.which(cmd) for k, cmd in binaries.items()}
    chrome_env = os.environ.get("CHROME_PATH", "")
    if chrome_env and Path(chrome_env).is_file():
        found["chrome"] = chrome_env
    found["bb-video"] = str(installed_path(ENGINES["bb-video"])) if installed_path(ENGINES["bb-video"]).exists() else None
    found["moneyprinterturbo-video"] = str(installed_path(ENGINES["moneyprinterturbo-video"])) if installed_path(ENGINES["moneyprinterturbo-video"]).exists() else None
    found["remotion-skills"] = str(installed_path(ENGINES["remotion-skills"])) if installed_path(ENGINES["remotion-skills"]).exists() else None
    return {"available": found, "total_registry": len(ENGINES), "note": "Binary presence does not establish successful video rendering."}


def bootstrap(engine_id: str, destination: Path, execute: bool, force: bool) -> dict:
    if engine_id not in ENGINES:
        raise ValueError("Unknown engine: " + engine_id)
    e = ENGINES[engine_id]
    if e["kind"] not in ("agent-skill", "agent-skill-pack") or not e.get("ref"):
        raise ValueError("Only pinned, reviewed Agent Skill packages can be bootstrapped")
    if not STYLE_RE.fullmatch(engine_id):
        raise ValueError("Invalid engine id")
    target = (destination.expanduser() / engine_id).resolve()
    info = {"source": "https://github.com/" + e["repo"], "pinned_commit": e["ref"],
            "source_subdirectory": e["skill_path"], "target": str(target),
            "action": "download-and-copy Skill files ONLY (dependencies are NOT installed)"}
    if not execute:
        info["status"] = "dry-run; pass --execute to install"
        return info
    if target.exists() and not force:
        raise FileExistsError(f"{target} exists; use --force to replace")
    if not shutil.which("git"):
        raise RuntimeError("git is required")
    with tempfile.TemporaryDirectory(prefix="andy-video-upstream-") as temp:
        src = Path(temp) / "repo"
        url = "https://github.com/" + e["repo"] + ".git"
        subprocess.run(["git", "init", "-q", str(src)], check=True)
        subprocess.run(["git", "-C", str(src), "remote", "add", "origin", url], check=True)
        subprocess.run(["git", "-C", str(src), "fetch", "--quiet", "--depth", "1", "origin", e["ref"]], check=True)
        subprocess.run(["git", "-C", str(src), "checkout", "--quiet", "--detach", "FETCH_HEAD"], check=True)
        actual = subprocess.check_output(["git", "-C", str(src), "rev-parse", "HEAD"], text=True).strip()
        if actual != e["ref"]:
            raise RuntimeError("Upstream HEAD moved. Pinned commit mismatch; review and update registry intentionally.")
        original = (src / e["skill_path"]).resolve()
        if not original.is_relative_to(src.resolve()) or not original.is_dir():
            raise RuntimeError("Upstream Skill folder missing")
        expected = original / "SKILL.md"
        if e["kind"] == "agent-skill" and not expected.is_file():
            raise RuntimeError("Upstream SKILL.md missing")
        if e["kind"] == "agent-skill-pack" and not any(original.glob("*/SKILL.md")):
            raise RuntimeError("Upstream Skill pack missing")
        destination = destination.expanduser().resolve()
        destination.mkdir(parents=True, exist_ok=True)
        staged = Path(temp) / "stage"
        shutil.copytree(original, staged, symlinks=False)
        for licence in ("LICENSE", "LICENSE.txt"):
            if (src / licence).is_file():
                shutil.copy2(src / licence, staged / ("UPSTREAM_" + licence))
                break
        (staged / "ANDY_UPSTREAM.json").write_text(json.dumps(info, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if target.exists():
            if not target.is_dir() or target.is_symlink():
                raise RuntimeError("Refusing to replace non-directory or symlink")
            shutil.rmtree(target)
        shutil.copytree(staged, target)
    info["status"] = "installed; execution and dependencies untested"
    if e["kind"] == "agent-skill-pack":
        info["note"] = "The official Remotion pack is staged as one directory. Install its subskills into the Agent's skill path if required by that Agent."
    return info


def scaffold(request: str, project: Path, style: str, execute: bool, gpu: bool) -> dict:
    plan = route(request, gpu=gpu)
    if plan["selected"] != "bb-video":
        return {"status": "delegate", "plan": plan,
                "next": "Read the selected tool's own Skill/README and execute its prescribed workflow; never claim rendered."}
    if style not in STYLES:
        raise ValueError("Unsupported BB-Video style: " + style)
    folder = installed_path(ENGINES["bb-video"])
    if not folder.is_dir():
        return {"status": "missing-bb-video", "plan": plan,
                "next": "Run bootstrap bb-video --execute, then rerun scaffold."}
    mode = "promo" if detect(request)["product"] else "explainer"
    script = folder / mode / "scripts" / "new.mjs"
    if not script.is_file():
        raise RuntimeError("Upstream project generator not found: " + str(script))
    cmd = ["node", str(script), str(project.expanduser().resolve()), "--style", style]
    result = {"status": "dry-run", "mode": mode, "command": cmd, "note": "Scaffolding alone does not produce an MP4."}
    if execute:
        if not shutil.which("node"):
            raise RuntimeError("node not found")
        if project.expanduser().exists():
            raise FileExistsError("Refusing to overwrite existing project")
        subprocess.run(cmd, cwd=str(folder), check=True)
        result["status"] = "scaffolded; agent must write script/visuals, render and review"
    return result



def qa_video(filepath: Path, expected_aspect: str | None = None, require_audio: bool = False) -> dict:
    """Check actual container metadata; pass != aesthetic/factual quality proof."""
    path = filepath.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError("Video file not found: " + str(path))
    if not shutil.which("ffprobe"):
        raise RuntimeError("ffprobe is required for media QA")
    cp = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate",
         "-of", "json", str(path)],
        text=True, capture_output=True, check=True,
    )
    data = json.loads(cp.stdout)
    streams = data.get("streams") or []
    videos = [x for x in streams if x.get("codec_type") == "video"]
    audios = [x for x in streams if x.get("codec_type") == "audio"]
    failures = []
    if not videos:
        failures.append("Missing video stream")
    if require_audio and not audios:
        failures.append("Requested audio stream missing")
    duration = float((data.get("format") or {}).get("duration") or 0)
    if duration <= 0:
        failures.append("Invalid duration")
    w = int(videos[0].get("width") or 0) if videos else 0
    h = int(videos[0].get("height") or 0) if videos else 0
    if not w or not h:
        failures.append("Invalid frame dimensions")
    if expected_aspect:
        try:
            ax, ay = map(int, expected_aspect.split(":"))
            if ax <= 0 or ay <= 0:
                raise ValueError
        except ValueError as exc:
            raise ValueError("Aspect must be like 9:16 or 16:9") from exc
        if w and h and abs(w / h - ax / ay) > 0.015:
            failures.append("Actual frame aspect does not match requested aspect")
    return {"status": "passed" if not failures else "failed", "file": str(path),
            "duration_seconds": duration, "width": w, "height": h,
            "video_codec": videos[0].get("codec_name") if videos else None,
            "audio_streams": len(audios), "issues": failures,
            "limits": "Container metadata only: inspect content, captions, claims, cuts, and visual quality separately."}


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Andy Video Director: plan / doctor / bootstrap / scaffold")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("plan", help="Select lead engine and a multi-tool production plan")
    a.add_argument("--request", required=True)
    a.add_argument("--gpu", action="store_true", help="GPU runtime available")
    a.add_argument("--offline", action="store_true")
    a.add_argument("--prefer", choices=sorted(ENGINES))
    sub.add_parser("doctor", help="Inspect command availability; no dependency installation")
    q = sub.add_parser("qa", help="Inspect a rendered video using ffprobe metadata")
    q.add_argument("--file", type=Path, required=True)
    q.add_argument("--aspect", choices=["16:9", "9:16", "1:1", "4:3", "3:4"])
    q.add_argument("--require-audio", action="store_true")
    b = sub.add_parser("bootstrap", help="Pin and install a reviewed upstream Agent Skill")
    b.add_argument("engine", choices=sorted(x["id"] for x in REGISTRY["engines"] if x["kind"] in ("agent-skill", "agent-skill-pack")))
    b.add_argument("--dest", type=Path, default=Path.home() / ".claude" / "skills")
    b.add_argument("--execute", action="store_true")
    b.add_argument("--force", action="store_true")
    s = sub.add_parser("scaffold", help="Scaffold a BB-Video project (not full video)")
    s.add_argument("--request", required=True)
    s.add_argument("--project", required=True, type=Path)
    s.add_argument("--style", default="launch", choices=sorted(STYLES))
    s.add_argument("--gpu", action="store_true")
    s.add_argument("--execute", action="store_true")
    args = p.parse_args(argv)
    try:
        if args.command == "plan":
            answer = route(args.request, args.gpu, args.prefer, args.offline)
        elif args.command == "doctor":
            answer = doctor()
        elif args.command == "qa":
            answer = qa_video(args.file, args.aspect, args.require_audio)
        elif args.command == "bootstrap":
            answer = bootstrap(args.engine, args.dest, args.execute, args.force)
        else:
            answer = scaffold(args.request, args.project, args.style, args.execute, args.gpu)
        print(json.dumps(answer, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, FileExistsError, OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc), "status": "failed"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
