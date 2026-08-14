"""
Concept Scene Template - Core Explanation
Visual breakdown of key concepts
"""

from manim import *

class ConceptScene(Scene):
    """
    核心概念讲解场景
    Duration: ~40 seconds
    """

    def construct(self):
        # Voiceover: "The key ingredients are three components..."

        # ===== CONFIG =====
        PRIMARY_COLOR = "{{PRIMARY_COLOR}}"
        SECONDARY_COLOR = "{{SECONDARY_COLOR}}"
        ACCENT_COLOR = "{{ACCENT_COLOR}}"
        BG_COLOR = "{{BG_COLOR}}"

        config.background_color = BG_COLOR

        # ===== TITLE =====
        title = Text("Core Concepts", font_size=48)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait(1)

        # ===== THREE KEY CONCEPTS =====
        concept1 = Text("1. {{CONCEPT_1}}", font_size=32, color=PRIMARY_COLOR)
        concept2 = Text("2. {{CONCEPT_2}}", font_size=32, color=SECONDARY_COLOR)
        concept3 = Text("3. {{CONCEPT_3}}", font_size=32, color=ACCENT_COLOR)

        concepts = VGroup(concept1, concept2, concept3).arrange(
            DOWN, buff=0.6, aligned_edge=LEFT
        )
        concepts.next_to(title, DOWN, buff=1)

        # ===== SEQUENTIAL REVEAL =====
        for concept in concepts:
            self.play(FadeIn(concept, shift=RIGHT * 0.5))
            self.wait(1.5)

        self.wait(2)

        # ===== VISUAL DEMONSTRATION =====
        # Example: Show geometric representation
        demo_group = self.create_visual_demo()
        demo_group.scale(0.8).to_edge(DOWN, buff=1)

        self.play(
            concepts.animate.scale(0.7).to_edge(LEFT, buff=1),
            FadeIn(demo_group)
        )
        self.wait(3)

        # ===== CLEAR =====
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def create_visual_demo(self):
        """
        Create visual representation
        Override this method for specific topics
        """
        # Example: Three circles representing concepts
        circle1 = Circle(radius=0.5, color=PRIMARY_COLOR, fill_opacity=0.3)
        circle2 = Circle(radius=0.5, color=SECONDARY_COLOR, fill_opacity=0.3)
        circle3 = Circle(radius=0.5, color=ACCENT_COLOR, fill_opacity=0.3)

        circles = VGroup(circle1, circle2, circle3).arrange(RIGHT, buff=0.5)
        return circles

# Usage:
# manim -pqh concept_scene.py ConceptScene
