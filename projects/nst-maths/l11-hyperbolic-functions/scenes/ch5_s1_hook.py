"""Chapter 5, scene 1: hook: from ch4's lattice to Example 36, and why circles belong here. Clips c5.hook.1 – c5.hook.3.

Module-level builders (import with load_scene("ch5_s1_hook")):
- lattice_shot(): ch4 s6's Argand lattice, small: DIM axes, Re z FG / Im z PINK, ticks -4pi..4pi,
  GREEN crosses at 2pi m +- i ln(2+sqrt3) (m = -2..2), BLUE 2pi brace, TEAL height brace, and the
  answer z = 2pi m +- i ln(2+sqrt3) under it (2pi m BLUE, +- YELLOW, i PINK, ln TEAL).
  Attributes .plane .crosses .answer. Centred at ORIGIN.
- example36_eq(size=72): Example 36, white MathTex 2x^2 + 4x + y^2 - 6y + 7 = 0, centred. Parts:
  0 '2', 1 x^2, 2 +, 3 4x, 4 +, 5 y^2, 6 -, 7 6y, 8 +, 9 7, 10 =, 11 0.
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

XS = 0.36          # units per real unit on the lattice's real axis (2pi -> 2.26)
YS = 0.8           # units per unit on the imaginary axis
H = float(np.log(2 + np.sqrt(3)))


def _cross(p, size=0.22):
    d = size / 2
    return VGroup(Line(p + d * (UL), p + d * (DR)), Line(p + d * (UR), p + d * (DL))).set_stroke(GREEN, 5)


def lattice_shot():
    re_ax = Line(5.4 * LEFT, 5.4 * RIGHT).set_stroke(DIM, 2)
    im_ax = Line(1.75 * DOWN, 1.75 * UP).set_stroke(DIM, 2)
    re_lab = MathTex(r"\mathrm{Re}\,z", font_size=30, color=FG).next_to(re_ax, RIGHT, buff=0.15)
    im_lab = MathTex(r"\mathrm{Im}\,z", font_size=30, color=PINK).next_to(im_ax, UP, buff=0.12)
    ticks, tlabs = VGroup(), VGroup()
    for m, s in zip(range(-2, 3), [r"-4\pi", r"-2\pi", "0", r"2\pi", r"4\pi"]):
        x = 2 * PI * m * XS
        ticks.add(Line([x, -0.07, 0], [x, 0.07, 0]).set_stroke(DIM, 2))
        lab = MathTex(s, font_size=28, color=DIM).move_to([x + (0.22 if m == 0 else 0), -0.32, 0])
        tlabs.add(lab)
    crosses = VGroup(*[_cross(np.array([2 * PI * m * XS, sgn * H * YS, 0]))
                       for m in range(-2, 3) for sgn in (1, -1)])
    y_top = H * YS
    b2 = span_brace(np.array([0, y_top, 0]), np.array([2 * PI * XS, y_top, 0]), direction=UP, color=BLUE)
    b2_lab = MathTex(r"2\pi", font_size=30, color=BLUE).next_to(b2, UP, buff=0.08)
    bh = Brace(Line(ORIGIN, y_top * UP), direction=LEFT, buff=0.12, color=TEAL)
    bh_lab = MathTex(r"\ln\left(2 + \sqrt{3}\right)", font_size=28, color=TEAL).next_to(bh, LEFT, buff=0.08)
    bh_lab.shift(0.12 * UP)
    plane = VGroup(re_ax, im_ax, ticks, tlabs, re_lab, im_lab, crosses, b2, b2_lab, bh, bh_lab)
    answer = MathTex("z", "=", r"2\pi m", r"\pm", "i", r"\ln\left(2 + \sqrt{3}\right)", font_size=44)
    answer[2].set_color(BLUE)
    answer[3].set_color(YELLOW)
    answer[4].set_color(PINK)
    answer[5].set_color(TEAL)
    answer.next_to(plane, DOWN, buff=0.55)
    g = VGroup(plane, answer).move_to(ORIGIN)
    g.plane, g.crosses, g.answer = plane, crosses, answer
    return g


def example36_eq(size=72):
    return MathTex("2", "x^2", "+", "4x", "+", "y^2", "-", "6y", "+", "7", "=", "0",
                   font_size=size, color=FG).move_to(ORIGIN)


class HookScene(NarratedScene):
    def construct(self):
        # ---- c5.hook.1: title, last time's lattice, circles and ellipses
        with self.say("c5.hook.1") as c:
            card = title_card("Part 5 · Circles and ellipses")
            if card.title.width > 12.6:
                card.title.scale_to_fit_width(12.6)
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.6),
                      time_span(FadeIn(card.course), 0.15, 0.75),
                      time_span(FadeIn(card.part), 0.3, 0.9), run_time=0.9)
            c.wait_until("last")

            lat = lattice_shot()
            lat.shift(0.2 * UP)
            sweep_clear(self, *appear(lat.plane, shift=None), run_time=2.0)
            self.play(*appear(lat.answer), run_time=1.0)
            c.wait_until("turn")

            self.play(*set_alpha([lat], DIMMED), run_time=0.8)
            circ = Circle(radius=1.6).set_stroke(BLUE, 5).move_to(3.2 * LEFT)
            ell = Ellipse(width=5.0, height=2.6).set_stroke(BLUE, 5).move_to(3.0 * RIGHT)
            self.play(*during(disappear(lat), 0, 0.3),
                      *during([Create(circ), Create(ell)], 0.3, 1), run_time=2.4)
            c.wait_until("briskly")
            self.play(FadeOut(circ, scale=0.2), FadeOut(ell, scale=0.2), run_time=1.0)

        # ---- c5.hook.2: Example 36
        with self.say("c5.hook.2") as c:
            eq = example36_eq(72)
            self.play(*appear(eq), run_time=1.0)
            c.wait_until("xpart")
            box = token_box([eq[k] for k in range(0, 4)], eq, height=eq.height + 0.4)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("ypart")
            self.play(Transform(box, token_box([eq[k] for k in range(5, 10)], eq, pad=0.1, height=eq.height + 0.4)),
                      run_time=1.2)
            c.wait_until("ask")

            ax = VGroup(Line(1.9 * LEFT, 1.9 * RIGHT), Line(1.7 * DOWN, 1.7 * UP)).set_stroke(DIM, 2)
            ax.move_to([4.4, 0, 0])
            qm = MathTex("?", font_size=140, color=YELLOW).move_to(ax.get_center() + 0.6 * UR)
            self.play(FadeOut(box), eq.animate.scale(0.8).move_to([-2.6, 0.6, 0]), run_time=1.2)
            self.play(*appear(ax, shift=None), *appear(qm), run_time=1.0)
            c.wait_until("hint")

            hint = MathTex("x^2", "+", "y^2", "=", "r^2", font_size=56, color=BLUE).set_opacity(0.5)
            hint.next_to(eq, DOWN, buff=0.75)
            hint.shift((eq[10].get_x() - hint[3].get_x()) * RIGHT)       # line up the = signs
            self.play(*appear(hint), run_time=1.0)
            c.wait_until("two")
            self.play(FlashAround(eq[0], color=YELLOW, run_time=1.5, time_width=1.5),
                      *recolor([eq[0]], YELLOW), run_time=1.5)
            c.wait_until("only")
            one = MathTex("1", font_size=72 * 0.8, color=YELLOW).set_opacity(0.45)
            gapw = one.width + 0.16
            one.next_to(eq[4], RIGHT, buff=0.16).align_to(eq[0], DOWN)
            self.play(*[eq[k].animate.shift(gapw * RIGHT) for k in range(5, 12)],
                      time_span(FadeIn(one), 0.6, 1.4), run_time=1.4)

        # ---- c5.hook.3: why circles? the circle-hyperbola pair
        with self.say("c5.hook.3", gap=1.5) as c:
            self.play(*disappear(ax, qm, hint), run_time=1.0)
            c.wait_until("cs")
            pair = S1.circle_hyperbola_pair(unit=1.3)
            pair.shift(0.45 * DOWN + 0.2 * RIGHT)
            for m in (pair.h_axes, pair.right, pair.left):
                m.set_stroke(opacity=0.5)
            pair.h_eq.set_opacity(0.5)
            pair.hlabel.tex.set_opacity(0.6)
            theta = pair.theta
            self.add(theta)
            eq_grp = VGroup(eq, one)
            self.play(*during([eq_grp.animate.scale(0.55).to_corner(UL, buff=0.45)], 0, 0.55),
                      *during(appear(pair.circle_panel, VGroup(pair.cdot, pair.clabel), shift=None, lag=0.3),
                              0.45, 1), run_time=1.4)
            # one turn counter-clockwise, stopping just below the x-axis (theta = -0.9 mod 2pi), so the
            # last sweep can run theta upward through 0 on both curves
            self.play(theta.animate.set_value(TAU - 0.9), run_time=c.until("next", floor=1.0), rate_func=linear)
            c.wait_until("next")
            part6 = T("Part 6", 34, color=TEAL)
            part6.next_to(pair.h_axes, DOWN, buff=0.2)
            self.play(*appear(pair.hyper_panel, VGroup(pair.hdot, pair.hlabel), shift=None, lag=0.3),
                      *during(appear(part6), 0.3, 1), run_time=1.2)
            rest = c.until(floor=1.5) - 0.1
            self.play(theta.animate.set_value(TAU + 0.9), run_time=rest)   # theta increases: ccw, upward

        for m in (pair.cdot, pair.hdot, pair.clabel, pair.hlabel):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)], run_time=1.0)
        self.wait(0.15)
