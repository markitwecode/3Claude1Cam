"""The chapter title card, identical in every chapter (layout taken from FoCS L3 ch1_s1_hook.py).

Title and course line come from the project's project.json ("title", "course_line").

    card = title_card("Part 2 · Pattern matching")
    self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
    self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)   # cue: "Foundations"/…
    self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

Ch1 then turns the word "Lists" into the chapter's first object (P5); do something similar
when it fits, and keep the subtitle lines up until the space is needed (STYLE.md screen time).
"""
from manim import DOWN, LEFT, ORIGIN, RIGHT, UP, Line, VGroup

from lib.paths import config
from lib.style import DIM, T


class TitleCard(VGroup):
    def __init__(self, part, **kw):
        super().__init__(**kw)
        self.title = T(config()["title"], size=96)
        self.rule = Line(LEFT * 2.8, RIGHT * 2.8, stroke_width=2, color=DIM)
        self.course = T(config()["course_line"], size=36, color=DIM)
        self.part = T(part, size=36)
        self.add(self.title, self.rule, self.course, self.part)
        self.arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.rule.shift(UP * 0.08)


def title_card(part):
    """part: e.g. "Part 2 · Pattern matching" (use the middle dot, as ch1 does)."""
    return TitleCard(part)
