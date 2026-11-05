"""Chapter 3, scene 1: hook: (77) and (78) become a toolbox for two questions. Clips c3.hook.1 – c3.hook.2."""
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

EXPO = load_scene("ch2_s6_expo")

TOOL_SCALE = 0.66            # toolbox size relative to the full-size formulas (44 → 29)
TOOL_UL = np.array([-6.6, 3.55, 0])   # toolbox's top-left corner


# ---------------------------------------------------------------- shared: the toolbox (s2, s5 import it)

def tool_lines():
    """(77) and (78) at full size (font 44), tags DIM, the i of 1/2i PINK; not placed."""
    cf = EXPO.cos_formula()
    sf = EXPO.sin_formula()
    sf[2][-1].set_color(PINK)                      # the i in 1/(2i)
    t77 = MathTex("(77)", font_size=44, color=DIM).next_to(cf, RIGHT, buff=0.45)
    t78 = MathTex("(78)", font_size=44, color=DIM).next_to(sf, RIGHT, buff=0.45)
    cos_line, sin_line = VGroup(cf, t77), VGroup(sf, t78)
    VGroup(cos_line, sin_line).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    return VGroup(cos_line, sin_line)


def toolbox():
    """VGroup(cos_line, sin_line) = (77), (78), scaled and parked in the top-left corner."""
    tb = tool_lines()
    tb.scale(TOOL_SCALE)
    tb.move_to(TOOL_UL + np.array([tb.width / 2, -tb.height / 2, 0]))
    return tb


# ---------------------------------------------------------------- the ch2 s6 picture, small and live

PS = 0.78                                   # picture scale
PSH = np.array([-1.55, -0.2, 0])            # picture shift after scaling (about ORIGIN)


def place(m):
    return m.scale(PS, about_point=ORIGIN).shift(PSH)


def sum_parts(theta):
    cx, cy, u = EXPO.PIC["cx"], EXPO.PIC["cy"], EXPO.PIC["u"]
    e = np.exp(1j * theta)
    P = lambda z: EXPO.to_pt(z, cx, cy, u)  # noqa: E731
    gold = EXPO.arrow_between(P(0), P(e), GOLD)
    purple = EXPO.arrow_between(P(e), P(e + e.conjugate()), PURPLE)
    gl = MathTex(r"e^{i\theta}", font_size=44, color=GOLD)
    gl.move_to(EXPO.side_spot(P(0), P(e), gl, +1))
    pl = MathTex(r"e^{-i\theta}", font_size=44, color=PURPLE)
    pl.move_to(EXPO.side_spot(P(e), P(e + e.conjugate()), pl, +1))
    dot = Dot(P(2 * e.real), radius=0.09, color=BLUE)
    dl = MathTex(r"2\cos\theta", font_size=36, color=BLUE).next_to(dot, DOWN, buff=0.22)
    return place(VGroup(gold, purple, gl, pl, dot, dl))


def static_plane():
    p = EXPO.PIC
    cx, cy, u, ex, ey = p["cx"], p["cy"], p["u"], p["ex"], p["ey"]
    re = T("Re", 39, color=DIM).next_to(EXPO.to_pt(complex(ex, 0), cx, cy, u), RIGHT, buff=0.15)
    im = T("Im", 39, color=DIM).next_to(EXPO.to_pt(complex(0, ey), cx, cy, u), RIGHT, buff=0.15)
    return place(VGroup(EXPO.build_plane(cx, cy, u, ex, ey), re, im))


def card(w, h, center):
    return RoundedRectangle(corner_radius=0.2, width=w, height=h, stroke_color=DIM,
                            stroke_width=2, fill_color=BG, fill_opacity=0).move_to(center)


def badge(card_rect):
    b = MathTex(r"e^{i\theta}", font_size=40, color=GOLD)
    ring = RoundedRectangle(corner_radius=0.18, width=b.width + 0.4, height=b.height + 0.3,
                            stroke_color=GOLD, stroke_width=2.5, fill_color=BG, fill_opacity=1)
    g = VGroup(ring, b.move_to(ring))
    # seated just above the card's top-right corner: it never crosses the border
    g.next_to(card_rect.get_corner(UR), UP, buff=0.1).align_to(card_rect, RIGHT).shift(0.1 * LEFT)
    g.set_z_index(2)
    return g


# ---------------------------------------------------------------- scene

class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(2.0)   # let the two badged questions sit
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        # silent lead-in: the title card is built and read before the voice starts
        card_ = title_card("Part 3 · Powers and sums with exponentials")
        card_.title.scale_to_fit_width(12.4)
        self.play(FadeIn(card_.title, shift=0.3 * DOWN), GrowFromCenter(card_.rule), run_time=1.0)  # early: title card
        self.play(*appear(card_.course, card_.part, lag=0.3), run_time=1.0)  # early: title card
        self.wait(2.6)  # silent hold on the card before the first line (not a sync wait)
        with self.say("c3.hook.1") as c:
            c.wait_until("last")

            # {last}: ch2 s6's tip-to-tail picture, small, on the left
            plane = static_plane()
            th = ValueTracker(EXPO.TH0)
            live = always_redraw(lambda: sum_parts(th.get_value()))
            first = sum_parts(EXPO.TH0)
            sweep_clear(self, FadeIn(plane), FadeIn(first), run_time=1.6)
            self.remove(first)
            self.add(live)
            # the two arrows turn opposite ways; the sum stays on the real axis
            rt = min(3.0, c.until("cos", floor=1.0) - 0.1)
            self.play(th.animate.set_value(80 * DEGREES), run_time=rt / 2, rate_func=smooth)
            self.play(th.animate.set_value(EXPO.TH0), run_time=rt / 2, rate_func=smooth)
            c.wait_until("cos")

            big = tool_lines()
            big.move_to([3.75, 0.0, 0])
            cos_line, sin_line = big
            self.play(*appear(cos_line), run_time=min(1.2, c.until("sin", floor=0.6)))
            self.play(*flash([cos_line[0][4], cos_line[0][6]], run_time=1.5, time_width=1.5))
            c.wait_until("sin")
            self.play(*appear(sin_line), run_time=1.2)
            self.play(*flash([sin_line[0][2]], color=PINK, run_time=1.5, time_width=1.5))
            live.clear_updaters()
        self.plane, self.live, self.big = plane, live, big

    def clip2(self):
        with self.say("c3.hook.2") as c:
            # {today}: the formulas shrink into the toolbox; the picture leaves
            tb = toolbox()
            self.play(*during(disappear(self.plane, self.live), 0, 0.45),
                      *during([Transform(self.big[0], tb[0]), Transform(self.big[1], tb[1])], 0.2, 1),
                      run_time=min(1.8, c.until("q1")))
            self.remove(*self.big.get_family())
            self.add(tb)
            c.wait_until("q1")

            # {q1}: the left card
            lc = card(6.2, 3.4, [-3.4, -0.75, 0])
            q1 = MathTex(r"\int", r"\cos", r"^3", r"\;\theta\,d\theta", "=", r"\mathord{?}", font_size=50)
            q1[1].set_color(BLUE)
            q1[5].set_color(YELLOW)
            q1.move_to(lc.get_center() + 0.75 * UP)
            self.play(FadeIn(lc), *appear(q1), run_time=1.2)
            c.wait_until("easy")

            # {easy}: cos 3θ integrates in one line
            e1 = MathTex(r"\int", r"\cos 3\theta", r"\,d\theta", "=", r"\tfrac{1}{3}", r"\sin 3\theta", "+", "C",
                         font_size=40)
            e1[1].set_color(BLUE)
            e1[5].set_color(BLUE)
            e1.move_to(lc.get_center() + 0.75 * DOWN + 0.3 * LEFT)
            tick = check_mark().scale(0.9).next_to(e1, RIGHT, buff=0.3)
            self.play(*appear(e1), run_time=1.2)
            self.play(GrowFromCenter(tick), run_time=0.6)
            c.wait_until("power")

            # {power}: the cube is the trouble
            # small ring nudged up-right so it clears the s of cos (and the theta after it)
            h3 = q1[2].height
            ring = Circle(radius=0.68 * h3, color=RED, stroke_width=3).move_to(
                q1[2].get_center() + np.array([0.12 * h3, 0.08 * h3, 0]))
            self.play(GrowFromCenter(ring), q1[2].animate.set_color(RED), run_time=1.0)
            c.wait_until("q2")

            # {q2}: the right card, a sum of cosines, built in two lines
            rc = card(6.2, 3.4, [3.4, -0.75, 0])
            l1 = MathTex("1", "+", r"\cos\theta", "+", r"\cos 2\theta", "+", r"\cdots", font_size=44)
            l2 = MathTex("+", r"\cos(N-1)\theta", "=", r"\mathord{?}", font_size=44)
            for k in (2, 4):
                l1[k].set_color(BLUE)
            l2[1].set_color(BLUE)
            l2[3].set_color(YELLOW)
            VGroup(l1, l2).arrange(DOWN, buff=0.45).move_to(rc)
            l2.shift(0.6 * RIGHT)
            self.play(*during([FadeIn(rc)], 0, 0.5), *during(appear(l1), 0.35, 1), run_time=1.4)
            c.wait_until("up to the cosine")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("both")

            # {both}: a GOLD e^{iθ} badge lands on each card
            b1, b2 = badge(lc), badge(rc)
            self.play(*appear(b1, b2, lag=0.3, shift=0.4 * DOWN), run_time=1.4)
            self.play(*[VShowPassingFlash(b[0].copy().set_stroke(GOLD, 6), time_width=0.5) for b in (b1, b2)],
                      run_time=1.5)
