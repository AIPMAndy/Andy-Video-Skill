"""
Attention Mechanism Explained - Simplified (No LaTeX)
Topic: Scaled Dot-Product Attention (Core of Transformers)
Target: 8-12 minute explainer video
Style: Dark background, color-coded elements, progressive reveals
"""

from manim import *

# Color constants for consistency across all scenes
QUERY_COLOR = "#00FFFF"      # Cyan for Queries
KEY_COLOR = "#FF00FF"        # Magenta for Keys
VALUE_COLOR = "#FFFF00"      # Yellow for Values
BG_COLOR = "#171717"         # Dark background

class AttentionIntro(Scene):
    """Opening scene: Hook with the fundamental question"""
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title with 3Blue1Brown style (using system font)
        title = Text("But what is", font="Helvetica Neue", font_size=48, color=WHITE)
        attention = Text("Attention", font="Helvetica Neue", font_size=72, color=VALUE_COLOR, weight=BOLD)
        subtitle = Text("in AI?", font="Helvetica Neue", font_size=48, color=WHITE)

        title_group = VGroup(title, attention, subtitle).arrange(DOWN, buff=0.3)

        self.play(FadeIn(title, shift=UP))
        self.wait(0.5)
        self.play(Write(attention))
        self.wait(0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(2)

        # Transition: Show real-world context
        context = Text(
            "The mechanism behind ChatGPT, GPT-4,\nClaude, and every modern AI",
            font_size=32,
            color=GRAY
        )
        context.next_to(title_group, DOWN, buff=1)

        self.play(FadeIn(context))
        self.wait(2)
        self.play(FadeOut(title_group), FadeOut(context))


class AttentionBasics(Scene):
    """Explain the core problem attention solves"""
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Problem setup
        problem_title = Text("The Problem:", font_size=40, color=RED).to_edge(UP)
        self.play(Write(problem_title))

        # Sentence example
        sentence = Text(
            '"The animal didn\'t cross the street because it was too tired"',
            font_size=28,
            color=WHITE
        ).shift(UP)

        self.play(FadeIn(sentence))
        self.wait(1)

        # Highlight ambiguous word
        it_word = Text("it", font_size=28, color=VALUE_COLOR).move_to(sentence.get_center() + RIGHT * 2.8)
        question = Text("What does 'it' refer to?", font_size=32, color=QUERY_COLOR).next_to(sentence, DOWN, buff=0.8)

        self.play(
            it_word.animate.scale(1.5),
            FadeIn(question)
        )
        self.wait(2)

        # Show two candidates
        animal = Text("The animal", font_size=28, color=BLUE).shift(DOWN * 1.5 + LEFT * 3)
        street = Text("The street", font_size=28, color=GREEN).shift(DOWN * 1.5 + RIGHT * 3)

        self.play(FadeIn(animal), FadeIn(street))
        self.wait(1)

        # Attention mechanism solution
        solution = Text(
            "Attention: Dynamically focus on relevant context",
            font_size=32,
            color=VALUE_COLOR
        ).to_edge(DOWN)

        self.play(Write(solution))
        self.wait(2)

        self.play(
            FadeOut(problem_title),
            FadeOut(sentence),
            FadeOut(it_word),
            FadeOut(question),
            FadeOut(animal),
            FadeOut(street),
            FadeOut(solution)
        )


class AttentionMathSetup(Scene):
    """Introduce Q, K, V with color coding"""
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("Three Key Ingredients", font_size=40, color=WHITE).to_edge(UP)
        self.play(Write(title))

        # Query
        q_label = Text("Query (Q)", font_size=36, color=QUERY_COLOR).shift(UP * 1 + LEFT * 4)
        q_desc = Text('"What am I looking for?"', font_size=24, color=GRAY).next_to(q_label, DOWN, buff=0.3)
        q_vec = VGroup(
            Text("[", font_size=60, color=QUERY_COLOR),
            VGroup(
                Text("q1", font_size=24, color=QUERY_COLOR),
                Text("q2", font_size=24, color=QUERY_COLOR),
                Text("q3", font_size=24, color=QUERY_COLOR),
            ).arrange(DOWN, buff=0.3),
            Text("]", font_size=60, color=QUERY_COLOR)
        ).arrange(RIGHT, buff=0.2).next_to(q_desc, DOWN, buff=0.5)

        self.play(FadeIn(q_label))
        self.wait(0.5)
        self.play(Write(q_desc))
        self.wait(0.5)
        self.play(Create(q_vec))
        self.wait(1)

        # Key
        k_label = Text("Key (K)", font_size=36, color=KEY_COLOR).shift(UP * 1)
        k_desc = Text('"What do I contain?"', font_size=24, color=GRAY).next_to(k_label, DOWN, buff=0.3)
        k_vec = VGroup(
            Text("[", font_size=60, color=KEY_COLOR),
            VGroup(
                Text("k1", font_size=24, color=KEY_COLOR),
                Text("k2", font_size=24, color=KEY_COLOR),
                Text("k3", font_size=24, color=KEY_COLOR),
            ).arrange(DOWN, buff=0.3),
            Text("]", font_size=60, color=KEY_COLOR)
        ).arrange(RIGHT, buff=0.2).next_to(k_desc, DOWN, buff=0.5)

        self.play(FadeIn(k_label))
        self.wait(0.5)
        self.play(Write(k_desc))
        self.wait(0.5)
        self.play(Create(k_vec))
        self.wait(1)

        # Value
        v_label = Text("Value (V)", font_size=36, color=VALUE_COLOR).shift(UP * 1 + RIGHT * 4)
        v_desc = Text('"What do I communicate?"', font_size=24, color=GRAY).next_to(v_label, DOWN, buff=0.3)
        v_vec = VGroup(
            Text("[", font_size=60, color=VALUE_COLOR),
            VGroup(
                Text("v1", font_size=24, color=VALUE_COLOR),
                Text("v2", font_size=24, color=VALUE_COLOR),
                Text("v3", font_size=24, color=VALUE_COLOR),
            ).arrange(DOWN, buff=0.3),
            Text("]", font_size=60, color=VALUE_COLOR)
        ).arrange(RIGHT, buff=0.2).next_to(v_desc, DOWN, buff=0.5)

        self.play(FadeIn(v_label))
        self.wait(0.5)
        self.play(Write(v_desc))
        self.wait(0.5)
        self.play(Create(v_vec))
        self.wait(2)

        # Show the formula
        formula = Text(
            "Attention(Q,K,V) = softmax(QK^T / √d_k) V",
            font_size=28,
            color=WHITE
        ).to_edge(DOWN)

        formula_box = SurroundingRectangle(formula, color=VALUE_COLOR, buff=0.2)

        self.play(Write(formula))
        self.play(Create(formula_box))
        self.wait(3)

        self.play(*[FadeOut(mob) for mob in self.mobjects])


class AttentionConclusion(Scene):
    """Wrap up with key insights"""
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Title
        title = Text("Why Attention Changed Everything", font_size=40, color=VALUE_COLOR).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Key points
        points = VGroup(
            Text("1. Dynamic Context Selection", font_size=28, color=QUERY_COLOR),
            Text("   → Focus on what matters for each word", font_size=24, color=GRAY),
            Text("2. Parallelizable Computation", font_size=28, color=KEY_COLOR),
            Text("   → All attention scores computed simultaneously", font_size=24, color=GRAY),
            Text("3. Long-Range Dependencies", font_size=28, color=GREEN),
            Text("   → Connect words across entire sequences", font_size=24, color=GRAY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(DOWN * 0.5)

        for i, point in enumerate(points):
            self.play(FadeIn(point, shift=RIGHT * 0.5))
            self.wait(0.5 if i % 2 == 0 else 1)

        self.wait(2)

        # Final message
        self.play(FadeOut(points))

        final = VGroup(
            Text("Attention is all you need", font_size=48, color=VALUE_COLOR),
            Text("— Vaswani et al., 2017", font_size=32, color=GRAY, slant=ITALIC),
        ).arrange(DOWN, buff=0.5)

        self.play(Write(final[0]))
        self.wait(0.5)
        self.play(FadeIn(final[1]))
        self.wait(3)


# Main rendering config
if __name__ == "__main__":
    # To render all scenes:
    # manim -pqh attention_mechanism_simple.py
    pass
