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
    elif tags["react"]:
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
    if tags["recording"] or tags["localize"]:
        steps.insert(1, {"stage": "transcript", "operator": "whisperx", "action": "Optional word timestamps and speaker separation for existing speech.", "status": availability(ENGINES["whisperx"])})
    if primary not in ("bb-video", "moneyprinterturbo-video") and (tags["explainer"] or tags["short"]):
        steps.append({"stage": "voice", "operator": "edge-tts", "action": "Optional consented online TTS (text goes to a third-party service).", "status": availability(ENGINES["edge-tts"])})
    if tags["short"] or tags["recording"] or tags["localize"]:
        steps.append({"stage": "captions", "operator": "whisperx", "action": "Create, align and inspect subtitles; avoid hallucinated captions.", "status": availability(ENGINES["whisperx"])})
    steps.append({"stage": "quality", "operator": "agent + ffprobe", "action": "Verify duration, aspect ratio, codec, audio, black frames, safe area, citations and licensing.", "status": "planned"})
    e = ENGINES[primary]
    fallbacks = {
        "bb-video": ["react-video", "remotion-skills"],
        "moneyprinterturbo-video": ["bb-video", "ai-video-producer"],
        "remotion-skills": ["react-video", "bb-video"],
        "wan2.2": ["ltx-2", "comfyui", "bb-video"],
        "comfyui": ["wan2.2", "ltx-2", "bb-video"],
        "andy-screencast-to-viral": ["auto-editor", "moviepy"],
    }.get(primary, ["bb-video", "react-video"])
    return {
        "request": request, "selected": primary, "selected_repo": e["repo"],
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
                "chromium": "chromium", "nvidia-smi": "nvidia-smi", "uv": "uv"}
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
        subprocess.run(["git", "clone", "--quiet", "--depth", "1", url, str(src)], check=True)
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


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Andy Video Director: plan / doctor / bootstrap / scaffold")
    sub = p.add_subparsers(dest="command", required=True)
    a = sub.add_parser("plan", help="Select lead engine and a multi-tool production plan")
    a.add_argument("--request", required=True)
    a.add_argument("--gpu", action="store_true", help="GPU runtime available")
    a.add_argument("--offline", action="store_true")
    a.add_argument("--prefer", choices=sorted(ENGINES))
    sub.add_parser("doctor", help="Inspect command availability; no dependency installation")
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
        elif args.command == "bootstrap":
            answer = bootstrap(args.engine, args.dest, args.execute, args.force)
        else:
            answer = scaffold(args.request, args.project, args.style, args.execute, args.gpu)
        print(json.dumps(answer, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, RuntimeError, FileExistsError, OSError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"error": str(exc), "status": "failed"}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
