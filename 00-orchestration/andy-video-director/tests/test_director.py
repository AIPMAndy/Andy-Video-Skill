import importlib.util
from pathlib import Path
import unittest

MODULE = Path(__file__).resolve().parents[1] / "director.py"
spec = importlib.util.spec_from_file_location("andy_video_director", MODULE)
director = importlib.util.module_from_spec(spec)
spec.loader.exec_module(director)


class DirectorTests(unittest.TestCase):
    def test_registry_and_styles(self):
        self.assertGreaterEqual(len(director.ENGINES), 20)
        self.assertEqual(len(director.STYLES), 30)
        for engine in director.ENGINES.values():
            self.assertTrue(engine["repo"])
            self.assertTrue(engine["kind"])
        self.assertEqual(len(director.ENGINES["bb-video"]["ref"]), 40)

    def test_general_explainer(self):
        p = director.route("帮我做一期讲解视频，讲 AI Agent 的原理")
        self.assertEqual(p["selected"], "bb-video")
        self.assertIn("stages", p)
        self.assertEqual(p["stages"][-1]["stage"], "quality")

    def test_recording(self):
        self.assertEqual(director.route("把两小时录屏剪成10条短视频")["selected"],
                         "andy-screencast-to-viral")

    def test_math(self):
        self.assertEqual(director.route("做数学公式推导 Manim 动画")["selected"],
                         "andy-manim-video")

    def test_react(self):
        self.assertEqual(director.route("用 React 动画做一段地图视频")["selected"],
                         "remotion-skills")

    def test_promo(self):
        self.assertEqual(director.route("给我做一个网站宣传片")["selected"], "bb-video")

    def test_short(self):
        self.assertEqual(director.route("一键成片的批量短视频")["selected"],
                         "moneyprinterturbo-video")

    def test_offline_fallback(self):
        self.assertEqual(director.route("一键成片的批量短视频", offline=True)["selected"],
                         "bb-video")

    def test_video_generation_requires_gpu(self):
        p = director.route("我想文生视频，电影级镜头", gpu=False)
        self.assertTrue(p["needs_gpu"])
        self.assertIn("GPU", p["reason"])

    def test_preference_override(self):
        self.assertEqual(director.route("做教程", prefer="react-video")["selected"], "react-video")
        with self.assertRaises(ValueError):
            director.route("做教程", prefer="not-a-real-engine")

    def test_v03_registry(self):
        self.assertEqual(director.REGISTRY["version"], "0.3.0")
        self.assertEqual(len(director.ENGINES), 30)
        self.assertEqual(director.ENGINES["blender-mcp"]["repo"], "ahujasid/mcp-for-blender")
        for name in ("cosyvoice", "motion", "animejs", "blender-mcp", "librosa", "lottie-web", "postprocessing", "threejs"):
            self.assertEqual(director.availability(director.ENGINES[name]), "external-engine; setup required")

    def test_v03_multistage_routing(self):
        cases = [
            ("给中文知识视频配音、生成字幕", "bb-video", {"cosyvoice", "whisperx"}),
            ("用 Anime.js 做 UI 动效", "remotion-skills", {"animejs"}),
            ("用 Motion 做界面动效", "remotion-skills", {"motion"}),
            ("用 Blender MCP 做三维建模", "blender-mcp", {"ffmpeg / compatible renderer"}),
            ("把视频按音乐节拍自动卡点", "bb-video", {"librosa"}),
            ("用 three.js 做网页三维", "threejs", {"ffmpeg / compatible renderer"}),
            ("用 Lottie 做矢量动画", "lottie-web", {"lottie-web"}),
            ("给 React 动画加 bloom 辉光", "remotion-skills", {"postprocessing"}),
        ]
        for req, primary, ops in cases:
            with self.subTest(request=req):
                result = director.route(req)
                self.assertEqual(result["selected"], primary)
                self.assertEqual(result["pipeline_version"], "0.3.0")
                self.assertEqual(result["stages"][-1]["stage"], "quality")
                self.assertTrue(ops.issubset({step["operator"] for step in result["stages"]}))

    def test_v03_not_automatically_installed(self):
        result = director.route("用 Blender MCP 做三维建模")
        self.assertTrue(result["needs_gpu"])
        self.assertIn("GPU", result["reason"])
        self.assertIn("setup required", result["status"])
        with self.assertRaises(ValueError):
            director.bootstrap("cosyvoice", Path("/tmp"), False, False)

    def test_bootstrap_is_dry_run(self):
        x = director.bootstrap("bb-video", Path("/tmp/andy-video-tests-destination"), False, False)
        self.assertIn("dry-run", x["status"])
        self.assertEqual(x["pinned_commit"], director.ENGINES["bb-video"]["ref"])

    def test_reject_engine_not_installable(self):
        with self.assertRaises(ValueError):
            director.bootstrap("wan2.2", Path("/tmp"), False, False)

    def test_scaffold_is_not_a_video(self):
        x = director.scaffold("给 App 做发布会宣传片", Path("/tmp/andy-video-not-created"), "launch", False, False)
        self.assertIn(x["status"], {"dry-run", "missing-bb-video"})
        with self.assertRaises(ValueError):
            director.scaffold("科普", Path("/tmp/x"), "evil-style", False, False)


if __name__ == "__main__":
    unittest.main()
