"""Chapter 6, scene 1: hook: circle and ellipse, flip the plus, the curve-pair glimpse. Clips c6.hook.1 – c6.hook.2.

Series visuals defined here (import with load_scene("ch6_s1_hook")):
- why_label(size=36): the YELLOW "why hyperbolic?" label (ch6 s3 brings it back and turns it GREEN).
- glimpse_pair(): ch1 s1's circle_hyperbola_pair at unit 1.0, without its own equations, centred at
  (0, PAIR_Y); returns the pair with `.why` = why_label() placed over the TEAL branch.
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

S1 = load_scene("ch1_s1_hook")

PAIR_Y = -1.35
EQ_Y = 2.35


def why_label(size=36):
    return T("why hyperbolic?", size=size, color=YELLOW)


def glimpse_pair():
    pair = S1.circle_hyperbola_pair(unit=1.0, gap=6.2, label_size=32)
    pair.circle_panel.remove(pair.c_eq)
    pair.hyper_panel.remove(pair.h_eq)
    pair.shift(PAIR_Y * UP)
    why = why_label()
    o = pair.h_origin.get_center()
    why.move_to(o + np.array([1.0, 2.1, 0]))
    pair.why = why
    return pair


def circle_fig():
    """Last time's BLUE circle with x^2 + y^2 = r^2 above it (parts: x2, +, y2, =, r2)."""
    circ = Circle(radius=1.3).set_stroke(BLUE, 4)
    eq = MathTex("x^2", "+", "y^2", "=", "r^2", font_size=52, color=BLUE)
    eq.next_to(circ, UP, buff=0.45)
    g = VGroup(circ, eq)
    g.circ, g.eq = circ, eq
    return g


def ellipse_fig(u=0.6):
    """Example 36's tall ellipse: centre (-1, 3), semi-minor sqrt2 (GREEN), semi-major 2 (GOLD)."""
    O = ORIGIN

    def p(x, y):
        return O + u * np.array([x, y, 0])

    axes = VGroup(Line(p(-3.0, 0), p(1.2, 0)), Line(p(0, -0.4), p(0, 5.6))).set_stroke(DIM, 2)
    c = p(-1, 3)
    ell = Ellipse(width=2 * np.sqrt(2) * u, height=4 * u).move_to(c).set_stroke(BLUE, 4)
    dashes = VGroup(DashedLine(c, p(-1, 0), dash_length=0.08), DashedLine(c, p(0, 3), dash_length=0.08))
    dashes.set_stroke(DIM, 2)
    major = VGroup(Line(c, p(-1, 5)), Line(c, p(-1, 1))).set_stroke(GOLD, 4)
    minor = VGroup(Line(c, p(-1 - np.sqrt(2), 3)), Line(c, p(-1 + np.sqrt(2), 3))).set_stroke(GREEN, 4)
    dot = Dot(c, radius=0.08, color=YELLOW)
    lab = MathTex("(-1,\\ 3)", font_size=38, color=YELLOW)
    lab.next_to(ell, LEFT, buff=0.15).set_y(c[1])
    g = VGroup(axes, dashes, ell, major, minor, dot, lab)
    return g


def _aside(mob, pos, scale=0.75, op=0.4):
    t = mob.copy().scale(scale).move_to(pos)
    for m in t.get_family():
        if isinstance(m, VMobject):
            m.set_stroke(opacity=m.get_stroke_opacity() * op)
            m.set_fill(opacity=m.get_fill_opacity() * op)
    return t


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        for m in (self.pair.cdot, self.pair.hdot, self.pair.clabel, self.pair.hlabel):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)], run_time=1.0)
        self.remove(self.pair.theta)
        self.wait(0.15)

    # ------------------------------------------------------------ title, last time
    def clip1(self):
        with self.say("c6.hook.1") as c:
            card = title_card("Part 6 · Hyperbolas and the conic family")
            if card.title.width > 12.6:
                card.title.scale_to_fit_width(12.6)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      time_span(FadeIn(card.course), 0.3, 0.9),
                      time_span(FadeIn(card.part, shift=0.2 * DOWN), 0.5, 1.1),
                      run_time=1.1)
            c.wait_until("last")

            circ = circle_fig()
            circ.move_to(np.array([-3.3, -0.1, 0]))
            ell = ellipse_fig()
            ell.move_to(np.array([3.3, -0.1, 0]))
            self.circ, self.ell = circ, ell
            sweep_clear(self, *appear(circ, ell, lag=0.4), run_time=2.0)
            c.wait_until("circle")
            self.play(FlashAround(circ.eq[1], color=YELLOW, time_width=1.5),
                      circ.eq[1].animate(rate_func=there_and_back).scale(1.5), run_time=1.5)

    # ------------------------------------------------------------ flip the sign, the question
    def clip2(self):
        circ, ell = self.circ, self.ell
        eq = circ.eq
        with self.say("c6.hook.2") as c:
            # equation to the centre; circle and ellipse dim and slide aside
            circ.remove(eq)
            target = eq.copy().scale(72 / 52).set_color(FG).move_to(EQ_Y * UP)
            target[1].set_color(YELLOW)
            self.play(Transform(circ, _aside(circ, np.array([-5.4, -0.6, 0]))),
                      Transform(ell, _aside(ell, np.array([5.5, -0.6, 0]))),
                      Transform(eq, target), run_time=1.6)
            # the plus flips over and lands as a minus
            plus = eq[1]
            minus = MathTex("-", font_size=72, color=YELLOW).move_to(plus)
            self.play(Rotate(plus, PI / 2, axis=RIGHT, about_point=plus.get_center()),
                      run_time=0.55, rate_func=rush_into)
            eq.remove(plus)
            self.remove(plus)
            minus.rotate(-PI / 2, axis=RIGHT, about_point=minus.get_center())
            self.add(minus)
            self.play(Rotate(minus, PI / 2, axis=RIGHT, about_point=minus.get_center()),
                      run_time=0.55, rate_func=rush_from)

            # r^2 becomes s^2
            c.wait_until("S squared")
            new = MathTex("x^2", "-", "y^2", "=", "s^2", font_size=72, color=FG)
            new.shift(eq[0].get_center() - new[0].get_center())
            s2 = new[4]
            self.play(*swap(eq[3], s2), run_time=1.2)

            # the question
            c.wait_until("ask")
            q = T("?", size=96, color=GOLD).next_to(s2, RIGHT, buff=0.6)
            self.play(*appear(q, shift=None), run_time=1.0)

            # the leftover question: ch1 s1's glimpse
            c.wait_until("pair")
            pair = glimpse_pair()
            self.pair = pair
            theta = pair.theta
            self.add(theta)
            sweep_clear(self, *appear(pair.circle_panel, VGroup(pair.cdot, pair.clabel),
                                      pair.hyper_panel, VGroup(pair.hdot, pair.hlabel), lag=0.3),
                        keep=[eq, minus, s2, q], run_time=2.0)
            c.wait_until(own_word=pair.why, cue="called hyperbolic")
            self.play(*appear(pair.why), run_time=1.0)
            rest = max(2.0, c.until("promise") + 2.0)
            self.play(theta.animate.set_value(1.1), run_time=0.35 * rest)
            self.play(theta.animate.set_value(-0.9), run_time=0.4 * rest)
            self.play(theta.animate.set_value(0.6), run_time=0.25 * rest)
