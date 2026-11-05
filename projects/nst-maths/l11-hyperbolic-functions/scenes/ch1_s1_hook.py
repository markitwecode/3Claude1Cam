"""Chapter 1, scene 1: hook: cos without the i, and the circle/hyperbola glimpse. Clips c1.hook.1 – c1.hook.4.

Series visuals defined here (import with load_scene("ch1_s1_hook")):
- cos_sin_pair(size=60): last time's  cos x = (e^{ix}+e^{-ix})/2  over  sin x = (e^{ix}-e^{-ix})/2i,
  cos/sin BLUE, e^{ix} GOLD, e^{-ix} PURPLE, every i PINK. VGroup(.cos, .sin), centred.
- circle_hyperbola_pair(unit=1.4, theta=0.0): BLUE unit circle with running (cos θ, sin θ) on the left,
  TEAL x² − y² = 1 (right branch solid, left DIM) with running (cosh θ, sinh θ) on the right.
  Drive both points with `pair.theta` (a ValueTracker; animate it, e.g. pair.theta.animate.set_value(1)).
  The group can be moved/scaled freely: the points read their origin and unit from the drawn curves.
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
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


# ---------------------------------------------------------------- series visuals

def _color_exp(parts, plus_idx, minus_idx, i_idx):
    """parts: a MathTex; colour e^{ix} pieces GOLD, e^{-ix} pieces PURPLE, i's PINK."""
    for k in plus_idx:
        parts[k].set_color(GOLD)
    for k in minus_idx:
        parts[k].set_color(PURPLE)
    for k in i_idx:
        parts[k].set_color(PINK)


def cos_sin_pair(size=60):
    """Last time's pair, centred. Part indices (both lines):
    0 name (BLUE), 1 x, 2 =, 4 'e', 5 i, 6 'x' (e^{ix}), 7 sign, 8 'e-', 9 i, 10 'x' (e^{-ix}),
    11 fraction bar + 2; the sine line has its denominator i at 12."""
    cos = MathTex(r"\cos", r"x", "=", r"\frac{", "e^{", "i", "x}", "+", "e^{-", "i", "x}", "}{2}",
                  font_size=size)
    sin = MathTex(r"\sin", r"x", "=", r"\frac{", "e^{", "i", "x}", "-", "e^{-", "i", "x}", "}{2", "i", "}",
                  font_size=size)
    for line in (cos, sin):
        line[0].set_color(BLUE)
    _color_exp(cos, (4, 6), (8, 10), (5, 9))
    _color_exp(sin, (4, 6), (8, 10), (5, 9, 12))
    pair = VGroup(cos, sin).arrange(DOWN, buff=0.8)
    sin.shift((cos[2].get_x() - sin[2].get_x()) * RIGHT)      # line up the = signs
    pair.move_to(ORIGIN)
    pair.cos, pair.sin = cos, sin
    return pair


def _wrap(t):
    return (t + PI) % TAU - PI


def circle_hyperbola_pair(unit=1.4, theta=0.0, t_max=1.25, gap=7.2, label_size=40):
    """The circle (left) and hyperbola (right), centred on ORIGIN. Attributes:
    .circle_panel (axes, circle, eq), .hyper_panel (axes, right, left, eq),
    .cdot/.clabel, .hdot/.hlabel (updaters attached; each label is VGroup(BG card, MathTex), MathTex
    at .tex), .theta (ValueTracker, not in the group)."""
    theta_t = ValueTracker(theta)

    # left: unit circle
    c_axes = VGroup(Line(2.0 * unit * LEFT * 0.95, 2.0 * unit * RIGHT * 0.95),
                    Line(1.55 * unit * DOWN, 1.55 * unit * UP)).set_stroke(DIM, 2)
    circle = Circle(radius=unit).set_stroke(BLUE, 4)
    c_eq = MathTex("x^2 + y^2 = 1", font_size=40, color=BLUE)
    circle_panel = VGroup(c_axes, circle, c_eq)

    # right: hyperbola x^2 - y^2 = 1
    h_axes = VGroup(Line(2.05 * unit * LEFT, 2.05 * unit * RIGHT),
                    Line(1.75 * unit * DOWN, 1.75 * unit * UP)).set_stroke(DIM, 2)
    h_origin = Dot(ORIGIN, radius=0.01).set_opacity(0)
    right = ParametricFunction(lambda t: unit * np.array([np.cosh(t), np.sinh(t), 0]),
                               t_range=[-t_max, t_max]).set_stroke(TEAL, 4)
    left = ParametricFunction(lambda t: unit * np.array([-np.cosh(t), np.sinh(t), 0]),
                              t_range=[-t_max, t_max]).set_stroke(DIM, 3)
    h_eq = MathTex("x^2 - y^2 = 1", font_size=40, color=TEAL)
    hyper_panel = VGroup(h_axes, h_origin, right, left, h_eq)

    circle_panel.shift(gap / 2 * LEFT)
    hyper_panel.shift(gap / 2 * RIGHT)
    top = unit * 1.75 + 0.45
    c_eq.move_to(circle.get_center() + top * UP)
    h_eq.move_to(h_origin.get_center() + top * UP)

    def u():
        return circle.width / 2

    def c_point():
        t = theta_t.get_value()
        return circle.get_center() + u() * np.array([np.cos(t), np.sin(t), 0])

    def h_point():
        t = float(np.clip(_wrap(theta_t.get_value()), -t_max, t_max))
        return h_origin.get_center() + u() * np.array([np.cosh(t), np.sinh(t), 0])

    cdot = Dot(c_point(), radius=0.09, color=YELLOW)
    hdot = Dot(h_point(), radius=0.09, color=YELLOW)
    def boxed(tex):       # BG card behind the label: it reads cleanly over the axes and the curves
        card = BackgroundRectangle(tex, color=BG, fill_opacity=1.0, buff=0.08)
        g = VGroup(card, tex)
        g.tex = tex
        return g

    clabel = boxed(MathTex(r"(\cos\theta,\ \sin\theta)", font_size=label_size, color=BLUE))
    hlabel = boxed(MathTex(r"(\cosh\theta,\ \sinh\theta)", font_size=label_size, color=TEAL))

    # Updaters act on the on-screen originals only. Mobject.copy() shares these functions, and a
    # Transform of the group (pair.animate.scale(...)) runs its start/target copies' updaters every
    # frame: they would chase the moving original and leave the dots a frame behind, off the curves.
    def follow_c(m):
        if m is cdot:
            m.move_to(c_point())

    def follow_h(m):
        if m is hdot:
            m.move_to(h_point())

    def place_c(m):       # outside the circle, on the radius through the point
        if m is clabel:
            t = theta_t.get_value()
            m.next_to(cdot, np.array([np.cos(t), np.sin(t), 0]), buff=0.12)

    def place_h(m):       # inside the branch, left of the point, above it (below it once sinh θ < 0):
        if m is hlabel:   # the branch bends away from the label on that side; the card covers the y-axis
            t = float(np.clip(_wrap(theta_t.get_value()), -t_max, t_max))
            m.next_to(hdot, LEFT, buff=0.12).shift(0.34 * np.tanh((t + 0.15) / 0.15) * UP)

    cdot.add_updater(follow_c)
    hdot.add_updater(follow_h)
    clabel.add_updater(place_c)
    hlabel.add_updater(place_h)
    place_c(clabel)
    place_h(hlabel)

    pair = VGroup(circle_panel, hyper_panel, cdot, clabel, hdot, hlabel)
    pair.circle_panel, pair.hyper_panel = circle_panel, hyper_panel
    pair.circle, pair.c_axes, pair.c_eq = circle, c_axes, c_eq
    pair.right, pair.left, pair.h_axes, pair.h_eq, pair.h_origin = right, left, h_axes, h_eq, h_origin
    pair.cdot, pair.clabel, pair.hdot, pair.hlabel = cdot, clabel, hdot, hlabel
    pair.theta = theta_t
    return pair


# ---------------------------------------------------------------- the scene

class HookScene(NarratedScene):
    def construct(self):
        # ---- c1.hook.1: title, then last time's pair
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Cosine without the i")
            if card.title.width > 12.6:
                card.title.scale_to_fit_width(12.6)
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.6),
                      time_span(FadeIn(card.course), 0.15, 0.75),
                      time_span(FadeIn(card.part), 0.3, 0.9), run_time=0.9)
            c.wait_until("in Lecture ten", nth=0)     # the card holds ~3.7 s; the pair is up by "cosine"

            pair = cos_sin_pair(60)
            cos, sin = pair.cos, pair.sin
            sweep_clear(self, *appear(cos, sin, lag=0.5), run_time=2.0)
            c.wait_until("E to the eye ex")
            self.play(*flash([VGroup(cos[4], cos[5], cos[6]), VGroup(sin[4], sin[5], sin[6])], color=GOLD,
                             run_time=1.5, time_width=1.5))
            c.wait_until("E to the minus eye ex")
            self.play(*flash([VGroup(cos[8], cos[9], cos[10]), VGroup(sin[8], sin[9], sin[10])], color=PURPLE,
                             run_time=1.5, time_width=1.5))

        # ---- c1.hook.2: lift out the i's
        with self.say("c1.hook.2") as c:
            self.play(*set_alpha([sin], DIMMED), FlashUnder(cos, color=BLUE, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("lift")
            self.play(*[p.animate.shift(0.9 * UP).set_opacity(0) for p in (cos[5], cos[9])],
                      run_time=min(1.6, c.until("left")))
            c.wait_until("left")

            new = MathTex("?", r"\,x", "=", r"\frac{1}{2}", r"\left(", "e^{", "x}", "+", "e^{-", "x}", r"\right)",
                          font_size=60)
            new[0].set_color(TEAL)
            for k in (5, 6):
                new[k].set_color(GOLD)
            for k in (8, 9):
                new[k].set_color(PURPLE)
            new.shift(cos[2].get_center() - new[2].get_center())
            self.play(*edit(cos, new), run_time=2.0)
            c.wait_until("new")
            q = new[0]
            self.play(FlashAround(q, color=TEAL, run_time=1.5, time_width=1.5),
                      q.animate(rate_func=there_and_back).scale(1.4), run_time=1.5)

        # ---- c1.hook.3: the circle and the hyperbola
        with self.say("c1.hook.3") as c:
            ch = circle_hyperbola_pair()
            ch.shift(0.35 * DOWN)
            theta = ch.theta
            self.add(theta)
            sweep_clear(self, *appear(ch.circle_panel, VGroup(ch.cdot, ch.clabel), lag=0.4), run_time=2.0)
            c.wait_until("On the left")
            self.play(theta.animate.set_value(TAU), run_time=c.until("hyper", floor=1.0) - 0.1, rate_func=linear)
            theta.set_value(0.0)
            c.wait_until("hyper")
            self.play(*appear(ch.hyper_panel, VGroup(ch.hdot, ch.hlabel), lag=0.4), run_time=1.5)
            rest = c.until(floor=2.0) - 0.2
            self.play(theta.animate.set_value(1.15), run_time=0.35 * rest)
            self.play(theta.animate.set_value(-1.0), run_time=0.4 * rest)
            self.play(theta.animate.set_value(0.7), run_time=0.25 * rest)

        # ---- c1.hook.4: three questions
        with self.say("c1.hook.4", gap=1.5) as c:
            self.play(ch.animate.scale(0.75).move_to(1.45 * UP), run_time=1.5)
            qs = [T("What are they?", size=34),
                  T("How are they tied to cosine and sine?", size=34),
                  T("Why ‘hyperbolic’?", size=34)]
            VGroup(*qs).arrange(DOWN, buff=0.36, aligned_edge=LEFT).move_to(1.0 * LEFT + 2.1 * DOWN)
            for qline, cue in zip(qs, ["What are these", "How are they", "why are they called"]):
                c.wait_until(cue)
                self.play(*appear(qline), run_time=1.0)
            c.wait_until("answer")
            tag_x = qs[1].get_right()[0] + 0.7
            tags = []
            for qline, (txt, col) in zip(qs, [("this chapter", GREEN), ("this chapter", GREEN),
                                             ("Parts 2 and 6", DIM)]):
                tg = T(txt, size=30, color=col)
                tg.next_to(qline, RIGHT).set_x(tag_x, direction=LEFT)
                tg.align_to(qline, DOWN)
                tags.append(tg)
            c.wait_until("this chapter")
            self.play(*appear(tags[0], tags[1], lag=0.3), run_time=1.2)
            c.wait_until("The third")
            self.play(*appear(tags[2]), run_time=1.0)

        for m in (ch.cdot, ch.hdot, ch.clabel, ch.hlabel):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)], run_time=1.0)
        self.remove(theta)
        self.wait(0.15)
