"""
Intro Scene Template - Opening Hook
3Blue1Brown style question-based opening
"""

from manim import *

class IntroScene(Scene):
    """
    开场钩子 - 疑问式标题
    Duration: ~10 seconds
    """

    def construct(self):
        # Voiceover: "But what is {TOPIC}? Let's explore this fascinating concept."

        # ===== CONFIG =====
        TOPIC = "{{TOPIC}}"  # Replace with actual topic
        PRIMARY_COLOR = "{{PRIMARY_COLOR}}"
        BG_COLOR = "{{BG_COLOR}}"

        config.background_color = BG_COLOR

        # ===== TITLE COMPONENTS =====
        title_part1 = Text("But what is", font_size=48)
        keyword = Text(TOPIC, font_size=64, color=PRIMARY_COLOR)
        title_part2 = Text("?", font_size=48)

        title = VGroup(title_part1, keyword, title_part2).arrange(RIGHT, buff=0.3)
        title.move_to(ORIGIN)

        # ===== ANIMATION =====
        # Step 1: Fade in question frame
        self.play(FadeIn(title_part1), FadeIn(title_part2))
        self.wait(0.5)

        # Step 2: Write keyword with emphasis
        self.play(Write(keyword, run_time=1.5))
        self.wait(1)

        # Step 3: Subtitle
        subtitle = Text(
            "Let's explore this concept visually",
            font_size=28,
            color=GRAY
        ).next_to(title, DOWN, buff=0.8)

        self.play(FadeIn(subtitle, shift=UP * 0.2))
        self.wait(2)

        # Step 4: Clear screen
        self.play(*[FadeOut(mob) for mob in self.mobjects])

# Usage:
# manim -pql intro_scene.py IntroScene
