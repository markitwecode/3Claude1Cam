"""Chapter 6, scene 1: title, callback to the Hermite recursion, the notes' five-point curve. Clips c6.hook.1 – c6.hook.3."""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

PART = "Part 6 · Stationary points"

# The notes' §4.10 curve: y' = (x + 2)(x + 1/2)(x - 3/2)^2
X_MIN, X_MAX = -2.6, 2.5
PEAK_X, VALLEY_X, FLAT_X = -2.0, -0.5, 1.5
BEND1_X, BEND2_X = -1.4307777, 0.3057777          # roots of y'' besides 3/2


def curve_y(x):
    return x ** 5 / 5 - x ** 4 / 8 - 17 * x ** 3 / 12 + 21 * x ** 2 / 16 + 9 * x / 4


def open_card():
    """The chapter's title card exactly as it stands once settled (static VGroup at ORIGIN)."""
    card = title_card(PART)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


class NotesFigure(VGroup):
    """Faint axes + BLUE curve + five YELLOW dots, at their fixed full-size place.
    Parts: .axes .curve .dots (VGroup peak, valley, bend1, bend2, flat, in that order),
    .peak .valley .bend1 .bend2 .flat; .at_x(x) → the curve's point above x."""

    def __init__(self):
        super().__init__()
        self.axes = Axes(x_range=[-2.8, 2.7, 1], y_range=[-2.0, 6.6, 1],
                         x_length=11.4, y_length=4.9, tips=False,
                         axis_config={"include_ticks": False, "stroke_width": 2,
                                      "stroke_color": DIM, "stroke_opacity": 0.55})
        self.axes.move_to(0.15 * UP)
        self.curve = self.axes.plot(curve_y, x_range=[X_MIN, X_MAX, 0.01], color=BLUE, stroke_width=6)
        self.peak, self.valley, self.bend1, self.bend2, self.flat = [
            Dot(self.at_x(x), radius=0.11, color=YELLOW).set_z_index(2)
            for x in (PEAK_X, VALLEY_X, BEND1_X, BEND2_X, FLAT_X)]
        self.dots = VGroup(self.peak, self.valley, self.bend1, self.bend2, self.flat)
        self.add(self.axes, self.curve, self.dots)

    def at_x(self, x):
        return self.axes.c2p(x, curve_y(x))


def notes_figure():
    return NotesFigure()


# "?" offsets from each dot, in the order peak, valley, bend1, bend2, flat
Q_OFFSETS = [0.5 * UP, 0.5 * DOWN, 0.42 * RIGHT + 0.18 * UP, 0.42 * RIGHT + 0.32 * DOWN, 0.42 * RIGHT + 0.42 * DOWN]


def handover_shot():
    """Last frame: figure, "?"s, question on top, derivative row with odd/even at the bottom.
    Parts: .fig (NotesFigure) .qs (VGroup of 5 "?") .question .row (MathTex parts y', y'', y''', y^(4), cdots)
    .odd .even."""
    shot = VGroup()
    shot.fig = notes_figure()
    shot.qs = VGroup(*[T("?", 36, YELLOW).move_to(d.get_center() + off)
                       for d, off in zip(shot.fig.dots, Q_OFFSETS)])
    shot.question = T("How do derivatives tell these apart?", 42).move_to(3.2 * UP)
    shot.row = MathTex(r"y'", r"y''", r"y'''", r"y^{(4)}", r"\cdots", font_size=56, color=GREEN)
    shot.row.arrange(RIGHT, buff=1.1, aligned_edge=DOWN).move_to(2.7 * DOWN)
    shot.odd = T("odd", 30, FG).next_to(shot.row[2], DOWN, buff=0.22)
    shot.even = T("even", 30, FG).next_to(shot.row[3], DOWN, buff=0.22)
    shot.even.align_to(shot.odd, UP)
    shot.add(shot.fig, shot.qs, shot.question, shot.row, shot.odd, shot.even)
    return shot


def _recap():
    eq = MathTex(r"H_{n+1} = 2x\,H_n - 2n\,H_{n-1}", font_size=56)
    box = SurroundingRectangle(eq, color=YELLOW, buff=0.3, stroke_width=4)
    boxed = VGroup(eq, box).move_to(1.3 * UP)
    lines = VGroup(MathTex(r"H_0 = 1", font_size=44),
                   MathTex(r"H_1 = 2x", font_size=44),
                   MathTex(r"H_2 = 4x^2 - 2", font_size=44)).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.2, width=lines.width + 0.9, height=lines.height + 0.6,
                             stroke_color=BLUE, stroke_width=3)
    frame.move_to(lines)
    ladder = VGroup(frame, lines).move_to(1.5 * DOWN)
    return boxed, ladder


class HookScene(NarratedScene):
    def construct(self):
        shot = handover_shot()
        fig = shot.fig

        with self.say("c6.hook.1") as c:
            card = open_card()
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 1.0),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 1.0),
                      time_span(FadeIn(card.course), 0.3, 1.3),
                      time_span(FadeIn(card.part), 0.6, 1.6), run_time=1.6)
            c.wait_until("last")
            boxed, ladder = _recap()
            sweep_clear(self, time_span(FadeIn(boxed, shift=0.2 * DOWN), 0.45, 1.1), run_time=1.1)
            self.play(*appear(ladder), run_time=min(0.8, c.until()))

        with self.say("c6.hook.2") as c:
            sweep_clear(self, time_span(Create(fig.axes), 0.7, 1.6), run_time=1.6)
            self.play(Create(fig.curve), run_time=min(3.0, 0.8 * c.until("peak")), rate_func=linear)
            c.wait_until("peak")
            self.play(FadeIn(fig.peak, scale=0.4), run_time=min(0.7, c.until("valley")))
            c.wait_until("valley")
            self.play(FadeIn(fig.valley, scale=0.4), run_time=min(0.8, c.until("bends")))
            c.wait_until("bends")
            self.play(LaggedStart(FadeIn(fig.bend1, scale=0.4), FadeIn(fig.bend2, scale=0.4), lag_ratio=0.5),
                      run_time=min(1.4, c.until("flat")))
            c.wait_until("flat")
            self.play(FadeIn(fig.flat, scale=0.4), *flash([fig.flat]), run_time=min(1.2, c.until()))

        with self.say("c6.hook.3", gap=1.0) as c:
            self.play(*appear(shot.question), run_time=1.0)
            self.play(*appear(*shot.qs, shift=None, lag=0.15), run_time=min(1.4, c.until("derivs")))  # early: question marks
            c.wait_until("derivs")
            self.play(*appear(*shot.row, shift=None, lag=0.25), run_time=min(1.6, c.until("but two")))
            c.wait_until("zero")
            yy = shot.row[1]
            self.play(*recolor([yy], YELLOW), FlashAround(yy, time_width=1.5),
                      run_time=min(1.5, c.until("parity")))
            c.wait_until("parity")
            self.play(*recolor([yy], GREEN), run_time=min(1.0, c.until("odd")))
            c.wait_until("odd")
            self.play(*appear(shot.odd), run_time=min(0.6, c.until("even")))
            c.wait_until(own_word=shot.even)
            self.play(*appear(shot.even), run_time=min(0.8, c.until()))
        # handover: the shot stays on screen; ch6_s2_vocab opens on handover_shot()
