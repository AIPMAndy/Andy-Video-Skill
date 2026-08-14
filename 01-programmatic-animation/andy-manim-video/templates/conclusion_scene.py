"""
Conclusion Scene Template - Summary and Takeaways
Wrap up with key messages
"""

from manim import *

class ConclusionScene(Scene):
    """
    总结与结尾场景
    Duration: ~30 seconds
    """

    def construct(self):
        # Voiceover: "So why does this matter? Here are three key takeaways..."

        # ===== CONFIG =====
        ACCENT_COLOR = "{{ACCENT_COLOR}}"
        BG_COLOR = "{{BG_COLOR}}"

        config.background_color = BG_COLOR

        # ===== SECTION 1: WHY THIS MATTERS =====
        title = Text("Why This Matters", font_size=44)
        title.to_edge(UP, buff=1)
        self.play(Write(title))
        self.wait(1)

        # Three key takeaways
        point1 = Text("→ {{TAKEAWAY_1}}", font_size=28)
        point2 = Text("→ {{TAKEAWAY_2}}", font_size=28)
        point3 = Text("→ {{TAKEAWAY_3}}", font_size=28)

        points = VGroup(point1, point2, point3).arrange(
            DOWN, buff=0.5, aligned_edge=LEFT
        )
        points.next_to(title, DOWN, buff=1.2)

        for point in points:
            self.play(FadeIn(point, shift=RIGHT * 0.3))
            self.wait(1.2)

        self.wait(2)
        self.play(FadeOut(VGroup(*self.mobjects)))

        # ===== SECTION 2: CLOSING QUOTE =====
        quote = Text(
            "{{CLOSING_QUOTE}}",
            font_size=48,
            color=ACCENT_COLOR
        )
        quote.move_to(ORIGIN)

        self.play(Write(quote, run_time=2))
        self.wait(3)
        self.play(FadeOut(quote))

        # ===== SECTION 3: CALL TO ACTION (Optional) =====
        cta = VGroup(
            Text("Thanks for watching!", font_size=36),
            Text("Subscribe for more visual explanations", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.5)

        self.play(FadeIn(cta))
        self.wait(2)
        self.play(FadeOut(cta))

# Usage:
# manim -pqh conclusion_scene.py ConclusionScene
