import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import wave

MODULE = Path(__file__).resolve().parents[1] / "promo_workflow.py"
spec = importlib.util.spec_from_file_location("andy_promo_workflow", MODULE)
promo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(promo)


def example():
    return {
        "product_name": "Example AI App", "audience": "independent makers",
        "core_value": "See one useful result fast", "pain_point": "Setup is too slow",
        "cta": "Try the live demo", "platform": "Reels", "aspect": "9:16",
        "source_ui": {"device": "assets/device.png", "interaction": "assets/click.mp4", "result": "assets/result.png"},
        "on_screen": {"device": "Slow setup?", "interaction": "One click", "result": "See the result"},
    }


class PromoWorkflowTests(unittest.TestCase):
    def test_three_shots_and_no_render_claim(self):
        plan = promo.build_plan(example())
        self.assertEqual([(s["role"], s["start_seconds"], s["duration_seconds"]) for s in plan["shots"]],
                         [("device", 0, 3), ("interaction", 3, 7), ("result", 10, 5)])
        self.assertEqual(plan["artifact_kind"], "preproduction-shotlist-not-rendered")

    def test_missing_assets_and_no_data_consent_blocked(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            planfile = folder / "plan.json"
            planfile.write_text(json.dumps(promo.build_plan(example())))
            result = promo.audit(planfile, folder)
            self.assertEqual(result["status"], "blocked")
            self.assertGreaterEqual(len(result["issues"]), 4)

    def test_real_assets_confirmed_ready_only_for_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            brief = example()
            brief["public_demo_data_confirmed"] = True
            for value in brief["source_ui"].values():
                path = folder / value
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"sample-nonempty")
            planfile = folder / "plan.json"
            planfile.write_text(json.dumps(promo.build_plan(brief)))
            self.assertEqual(promo.audit(planfile, folder)["status"], "ready-for-render")

    def test_voice_duration_requires_actual_audio(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            brief = example()
            brief["public_demo_data_confirmed"] = True
            brief["voiceover"] = {"device": "Some words"}
            brief["voice_files"] = {"device": "device.wav"}
            for value in brief["source_ui"].values():
                path = folder / value
                path.parent.mkdir(exist_ok=True)
                path.write_bytes(b"sample-nonempty")
            with wave.open(str(folder / "device.wav"), "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(8000)
                f.writeframes(b"\x00\x00" * 32000)  # 4s exceeds 3s first shot
            planfile = folder / "plan.json"
            planfile.write_text(json.dumps(promo.build_plan(brief)))
            result = promo.audit(planfile, folder)
            self.assertEqual(result["status"], "blocked")
            self.assertTrue(any("exceeds" in issue for issue in result["issues"]))

    def test_reject_path_traversal(self):
        brief = example()
        brief["source_ui"]["device"] = "../../secret.png"
        with self.assertRaises(ValueError):
            promo.build_plan(brief)

    def test_init_refuses_to_overwrite_reviewed_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            b = folder / "brief.json"
            b.write_text(json.dumps(example()))
            result = promo.init(b, folder / "out")
            self.assertIn("planned-not-rendered", result["status"])
            self.assertTrue((folder / "out" / "HANDOFF.md").exists())
            with self.assertRaises(FileExistsError):
                promo.init(b, folder / "out")


if __name__ == "__main__":
    unittest.main()
