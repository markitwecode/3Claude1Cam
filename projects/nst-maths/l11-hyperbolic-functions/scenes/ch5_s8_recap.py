"""Chapter 5, scene 8: recap in six panels, then the + flips to - and the circle opens into the hyperbola (end card).
Clips c5.recap.1 – c5.recap.2.

Panels (3 x 2, DIM rounded frames as in the earlier recaps), each a miniature built with the builders
of the scene that taught it, on its mark, while the previous one dims to 0.4:
r1 s3's E2 circle + (x-1)^2 + y^2 = 1; r2 s3's case icons circle -> point -> empty set; r3 s4's wide
ellipse (a circle stretched) with its GOLD/GREEN braces; r4 s5's circle + ellipse driven by one theta
dial; r5 s6's Example 36 sketch beside 2(x+1)^2 - 2 (the GREEN -2); r6 s7's filled ellipse, A = pi a b.
Then all restored, the board clears to the unit circle x^2 + y^2 = 1, the + turns YELLOW and flips to
-, the circle opens out into ch1 s1's TEAL hyperbola with (cosh theta, sinh theta). End card ~8 s.
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

S1 = load_scene("ch1_s1_hook")
S3 = load_scene("ch5_s3_complete")
S4 = load_scene("ch5_s4_ellipse")
S5 = load_scene("ch5_s5_param")
S6 = load_scene("ch5_s6_example")
S7 = load_scene("ch5_s7_area")

# ---------------------------------------------------------------- the grid
PW, PH = 4.4, 3.5
XS = (-4.55, 0.0, 4.55)
YS = (1.85, -1.85)
CENTRES = [np.array([x, y, 0]) for y in YS for x in XS]
FADED = 0.4
CAP = 30
PIC_DY = 0.22                    # picture centre above the panel centre
PIC_W, PIC_H = PW - 0.3, PH - 0.95


def frame_at(k):
    return RoundedRectangle(corner_radius=0.15, width=PW, height=PH).set_stroke(DIM, 2).move_to(CENTRES[k])


def pic_centre(k):
    return CENTRES[k] + PIC_DY * UP


def caption(k, text, color=FG):
    t = T(text, CAP, color)
    t.move_to(CENTRES[k] + (-PH / 2 + 0.36) * UP)
    return t


def fit(m, k):
    if m.width > PIC_W or m.height > PIC_H:
        s = min(PIC_W / m.width, PIC_H / m.height)
        print(f"[recap] panel {k} scaled by {s:.2f}", file=sys.stderr)
        m.scale(s)
    m.move_to(pic_centre(k))
    return m


# ---------------------------------------------------------------- the end shot
HC = np.array([0.0, -0.4, 0.0])
HU = 1.6


def end_pieces():
    pair = S1.circle_hyperbola_pair(unit=HU, theta=0.6)
    hp = pair.hyper_panel
    hp.shift(HC - pair.h_origin.get_center())
    pair.hdot.update(0)
    pair.hlabel.update(0)
    circle = Circle(radius=HU).set_stroke(BLUE, 4).move_to(HC)
    eq = MathTex("x^2", "+", "y^2", "=", "1", font_size=52, color=BLUE)
    eq.move_to(pair.h_eq.get_center() + 0.05 * UP)
    minus = MathTex("-", font_size=52, color=YELLOW).move_to(eq[1])
    return pair, circle, eq, minus


class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.wait(8.0)                       # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    def dim_prev(self):
        return set_alpha(self.panels, FADED) if self.panels else []

    # ------------------------------------------------------------ c5.recap.1
    def clip1(self):
        frames = [frame_at(k) for k in range(6)]
        self.frames = frames
        with self.say("c5.recap.1") as c:
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.15),
                      run_time=min(1.0, c.until("r1")))
            c.wait_until("r1")

            # ---- r1: E2's circle
            eq = S3.e2_equation(36)
            fig = S3.e2_figure(origin=ORIGIN, u=0.55)
            fig[7].next_to(fig[3], DOWN, buff=0.12)      # (1, 0) below the circle, clear of its stroke
            fig[7].set_x(max(fig[7].get_x(), fig[0].c2p(0, 0)[0] + 0.14 + fig[7].width / 2))   # and of the y-axis
            pic = fit(VGroup(eq, fig).arrange(DOWN, buff=0.22), 0)
            cap = caption(0, "complete the square")
            self.play(*appear(eq, fig, lag=0.4), run_time=min(1.5, c.until("complete")))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
            self.panels.append(VGroup(pic, cap))
            c.wait_until("r2")

            # ---- r2: the sign decides
            circ, pt, empty = S3.case_icons()
            icons = [circ.copy(), pt.copy(), empty[0].copy()]
            rels = [">", "=", "<"]
            labs = [MathTex("r^2", rel, "0", font_size=32) for rel in rels]
            cols = []
            for icon, lab in zip(icons, labs):
                icon.move_to(ORIGIN)
                lab.next_to(ORIGIN, DOWN, buff=0.75)
                cols.append(VGroup(icon, lab))
            row = VGroup(*cols).arrange(RIGHT, buff=0.42)
            for col in cols[1:]:
                col[0].set_y(cols[0][0].get_y())
                col[1].set_y(cols[0][1].get_y())
            arrows = [MathTex(r"\to", font_size=36, color=DIM).move_to(
                [(cols[i][0].get_right()[0] + cols[i + 1][0].get_left()[0]) / 2, cols[0][0].get_y(), 0])
                for i in range(2)]
            pic2 = fit(VGroup(row, *arrows), 1)
            cap2 = caption(1, "the sign decides")
            c.wait_until(own_word=cap2)
            self.play(*self.dim_prev(), *appear(cap2), run_time=1.0)
            for cue, i in (("a circle", 0), ("single point", 1), ("nothing at all", 2)):
                c.wait_until(cue)
                extra = appear(arrows[i - 1], shift=None) if i else []
                self.play(*extra, *appear(icons[i], labs[i], lag=0.15), run_time=min(0.9, c.until("r3") if i == 2 else 0.9))
            self.panels.append(VGroup(pic2, cap2))
            c.wait_until("r3")

            # ---- r3: a stretched circle
            s = 0.34                     # small enough that 'semi-minor' clears the panel border
            we = S4.wide_ellipse()
            body = VGroup(we.ell, we.arm_x, we.arm_y, we.dot, we.brace_x, we.brace_y).scale(s)
            lab_x = T("semi-major", 28, GOLD).next_to(we.brace_x, DOWN, buff=0.08)
            lab_y = T("semi-minor", 28, GREEN).next_to(we.brace_y, RIGHT, buff=0.1)
            pic3 = VGroup(body, lab_x, lab_y)
            fit(pic3, 2)
            pic3.shift(0.1 * DOWN)
            start = Circle(radius=we.ell.height / 2).set_stroke(BLUE, 5).move_to(we.ell)
            cap3 = caption(2, "a stretched circle")
            self.play(*self.dim_prev(), *appear(start, we.dot, shift=None), run_time=min(1.0, c.until("stretched")))
            c.wait_until("stretched")
            self.play(ReplacementTransform(start, we.ell), *appear(cap3), run_time=min(1.5, c.until("semi-major")))
            c.wait_until("semi-major")
            self.play(GrowArrow(we.arm_x), GrowFromCenter(we.brace_x), *appear(lab_x),
                      run_time=min(1.0, c.until("semi-minor")))
            c.wait_until("semi-minor")
            self.play(GrowArrow(we.arm_y), GrowFromCenter(we.brace_y), *appear(lab_y),
                      run_time=min(1.0, c.until("r4")))
            self.panels.append(VGroup(pic3, cap3))
            c.wait_until("r4")

            # ---- r4: cosine and sine draw both
            g = S5.circle_ellipse_pair(theta=0.7, unit=0.6, eqs=False)
            k = 3
            P = pic_centre(k)
            top_y = P[1] + 0.55
            g.circle.move_to([P[0] - 1.325, top_y, 0])
            g.centre.move_to(g.circle)
            ell_grp = VGroup(g.ellipse, g.ecentre, g.ab)
            ell_grp.shift(np.array([P[0] + 0.725, top_y, 0]) - g.ellipse.get_center())
            ring, needle, hub, d_lab = g.dial
            VGroup(ring, hub).scale(0.7).move_to([P[0] - 0.25, P[1] - 0.85, 0])
            hub.move_to(ring)
            d_lab.next_to(ring, RIGHT, buff=0.15)
            for m in g.updated:
                m.update(0)
            pieces = [g.circle, g.centre, g.radius, g.cdot, g.ellipse, g.ecentre, *g.ab, g.edot,
                      ring, needle, hub, d_lab]
            cap4 = caption(k, "cos and sin draw both")
            self.play(*self.dim_prev(), *appear(*pieces, shift=None, lag=0.03), *appear(cap4),
                      run_time=min(1.2, c.until()))
            self.play(g.theta.animate.set_value(0.7 + TAU), rate_func=linear,
                      run_time=max(0.5, c.until() - 0.15))
            for m in g.updated:
                m.clear_updaters()
            self.panels.append(VGroup(*pieces, cap4))

    # ------------------------------------------------------------ c5.recap.2
    def clip2(self):
        with self.say("c5.recap.2") as c:
            # ---- r5: Example 36
            k = 4
            sk = S6.example36_sketch(unit=0.36)
            sketch = VGroup(sk.ax, sk.axis_labels, sk.dashes, sk.ellipse, sk.gold, sk.green, sk.centre,
                            sk.centre_label)
            expr = MathTex(r"2(x+1)^2", r"-2", font_size=40)
            expr[1].set_color(GREEN)
            expr.next_to(sketch, RIGHT, buff=0.2)
            pic5 = fit(VGroup(sketch, expr), k)
            cap5 = caption(k, "factor, complete, divide")
            self.play(*self.dim_prev(), *appear(sketch, shift=None), run_time=min(1.5, c.until("factor")))
            c.wait_until(own_word=cap5)
            self.play(*appear(expr, cap5, lag=0.5), run_time=min(1.4, c.until("complete the squares")))
            c.wait_until("complete the squares")
            self.play(FlashAround(expr[1], color=GREEN, time_width=1.5), run_time=min(1.5, c.until("r6")))
            self.panels.append(VGroup(pic5, cap5))
            c.wait_until("r6")

            # ---- r6: area pi a b
            k = 5
            shape = S7.ex36_ellipse(unit=0.5, centre=ORIGIN, label_size=32)
            shape = VGroup(*shape[:4], *shape[5:])        # drop the (-1, 3) label: too crowded at this size
            form = MathTex(r"A = \pi a b", font_size=48).next_to(shape, RIGHT, buff=0.7)
            pic6 = fit(VGroup(shape, form), k)
            cap6 = caption(k, "area πab")
            self.play(*self.dim_prev(), *appear(shape, form, shift=None, lag=0.4),
                      run_time=min(1.5, c.until("area")))
            c.wait_until(own_word=cap6)
            self.play(*appear(cap6), run_time=1.0)
            self.panels.append(VGroup(pic6, cap6))
            c.wait_until("times b")
            self.play(*set_alpha(self.panels[:-1], 1), run_time=1.0)
            c.wait_until("next")

            # ---- next: the + flips to -
            pair, circle, eq, minus = end_pieces()
            sweep_clear(self, FadeIn(pair.h_axes), FadeIn(circle), FadeIn(eq), run_time=1.6)
            c.wait_until("plus sign")
            self.play(eq[1].animate.set_color(YELLOW), FlashAround(eq[1], time_width=1.5),
                      run_time=min(1.2, c.until("minus")))
            c.wait_until("minus")
            self.play(*swap(eq[1], minus), run_time=min(1.2, c.until("hyper")))
            settle(self, eq, add=[minus], drop=[eq[1]])
            c.wait_until("hyper")

            # ---- hyper: the circle opens out into the hyperbola
            twin = circle.copy()
            self.add(twin)
            self.play(ReplacementTransform(circle, pair.right), ReplacementTransform(twin, pair.left),
                      *recolor(list(eq), TEAL), run_time=min(2.0, c.until("cosh")))
            c.wait_until("cosh")
            self.play(*appear(pair.hdot, pair.hlabel, shift=None, lag=0.3), run_time=min(1.2, c.until()))
