"""Chapter 7, scene 6: recap of the chapter, the lecture's two threads, and next time. Clips c7.recap.1 – c7.recap.3.

Recap grid: four panels built from s1/s2/s3/s4/s5's helpers (circuit + four laws, the turning
arrows with shadows, d/dt -> x iω with the quarter-turn pair, the boxed Z with its triangle).
Lecture picture: two threads (TEAL "the 2πn", GOLD "the turning arrow") with thumbnails strung
on them. ch2 s2's ray/theta_arc are imported; ch1 s5 / ch3 s3 (not built) and ch4/ch5/ch6
(in fix passes) are drawn here as small stand-ins in the course colours.
Ends on the end card (Lecture 11, cosh, Part 8 card), held ~8 s, then fades.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S2C = load_scene("ch7_s2_circuit")
S3 = load_scene("ch7_s3_amplitudes")
S4 = load_scene("ch7_s4_parts")
S5 = load_scene("ch7_s5_impedance")
CH2 = load_scene("ch2_s2_theorem")

tx = S5.tx
PHI0 = 25 * DEGREES


def _dir(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- recap panels
X_L, X_R = -3.55, 3.55
Y_T, Y_B = 2.1, -1.65            # picture centres
CAP_T, CAP_B = 0.5, -3.45        # caption centres


def caption(text, y, x):
    return T(text, 30).move_to(P(x, y))


def panel_r1():
    circ = S4.small_circuit(center=P(-5.15, Y_T), scale=0.38)
    laws = S3.law_lines().move_to(P(-1.55, Y_T))
    cap = T("four laws: two parts,\nthe current, the loop", 28).move_to(P(X_L, CAP_T + 0.12))
    return circ, laws, cap


def panel_r2(ph, ops):
    c = P(X_R, Y_T)
    plane = S5.amp_plane(c, 0.26, 1.45)
    arrows = S3.turning_arrows(ph, ops, center=c, unit=0.26)
    shadows = S3.arrow_shadows(ph, ops, center=c, unit=0.26)
    cap = caption("every quantity: a turning arrow", CAP_T, X_R)
    return plane, arrows, shadows, cap


def panel_r3():
    rule = S4.deriv_rule(44).move_to(P(-5.05, Y_B))
    pc = P(-1.75, Y_B)
    plane = S5.amp_plane(pc, 0.28, 1.45)
    pair = S4.quarter_pair(center=pc, unit=0.28, phase=S4.TH, i_len=1.5 * PI)
    cap = MathTex(r"\text{derivatives become }\times\,", "i", r"\omega", font_size=40)
    cap[1].set_color(PINK)
    cap.move_to(P(X_L, CAP_B))
    return rule, plane, pair, cap


def panel_r4():
    zb = tx("Z", "=", ("R", BLUE), "-", r"\frac{", ("i", PINK), "}{", r"\omega", ("C", PINK), "}",
            size=46).move_to(P(2.05, Y_B))
    box = SurroundingRectangle(zb, color=YELLOW, buff=0.2, stroke_width=3)
    o, u = P(4.0, Y_B + 0.65), 0.45
    tri = VGroup(S5.amp_arrows(0.0, center=o, unit=u, tip_to_tail=True, width=5, tip=0.2),
                 S5.right_angle(0.0, center=o, unit=u, s=0.18), S5.lag_arc(0.0, center=o, unit=u))
    cap = caption("one complex resistance", CAP_B, X_R)
    return zb, box, tri, cap


# ---------------------------------------------------------------- lecture thumbnails
TW, TH_ = 2.5, 2.0
ROW1_Y, ROW2_Y = 1.75, -1.95
ROW1_X = (-3.0, 0.0, 3.0)
ROW2_X = (-4.5, -1.5, 1.5, 4.5)


def frame(c, color):
    return RoundedRectangle(corner_radius=0.15, width=TW, height=TH_).set_stroke(color, 2).set_fill(BG, 1).move_to(c)


def axes(o, l, r, d, u, op=0.6):
    return VGroup(Line(o + l * LEFT, o + r * RIGHT), Line(o + d * DOWN, o + u * UP)).set_stroke(DIM, 1.5, opacity=op)


def thumb_ring(c):
    """ch1 s5: the five roots of 2i on the dashed GOLD circle r = 2^{1/5}, unit circle DIM."""
    r1, r = 0.6, 0.6 * 2 ** 0.2
    g = VGroup(axes(c, 0.95, 0.95, 0.85, 0.85),
               Circle(radius=r1, color=DIM, stroke_width=1.5).move_to(c),
               DashedVMobject(Circle(radius=r, color=GOLD, stroke_width=2).move_to(c), num_dashes=28))
    pts = [c + r * _dir(PI / 10 + TAU * m / 5) for m in range(5)]
    g.add(Polygon(*pts).set_stroke(TEAL, 1.5, opacity=0.45))
    for m, p in enumerate(pts):
        g.add(Dot(p, radius=0.075, color=GREEN if m == 0 else TEAL))
    return g


def thumb_ladder(c):
    """ch4 s4: the ladder of ln 2i (dashed GOLD line at Re w = ln 2, rungs 2πi apart)."""
    o = c + P(-0.55, -0.55)
    g = VGroup(axes(o, 0.35, 1.45, 0.4, 1.4))
    x = o[0] + 0.7
    g.add(DashedLine(P(x, c[1] - 0.9), P(x, c[1] + 0.9), dash_length=0.08,
                     color=GOLD, stroke_width=2))
    ys = {n: c[1] - 0.25 + 0.42 * n for n in (-1, 0, 1, 2)}
    for n, y in ys.items():
        g.add(Dot(P(x, y), radius=0.075 if n == 0 else 0.065, color=GREEN if n == 0 else TEAL))
    g.add(Dot(P(x, c[1] + 0.84), radius=0.05, color=TEAL, fill_opacity=0.5))
    br = Brace(Line(P(x, ys[0]), P(x, ys[1])), direction=RIGHT, buff=0.1, color=TEAL)
    g.add(br, MathTex(r"2\pi i", font_size=28, color=TEAL).next_to(br, RIGHT, buff=0.08))
    return g


def _spiral_pt(o, unit, n):
    w = complex(0.1, 0.03) * complex(np.log(2), PI / 2 + TAU * n)
    rr = unit * np.exp(w.real) ** 0.6
    return o + rr * _dir(w.imag)


def thumb_gallery(c):
    """ch5 s7: the gallery of four frames: 1 value, q values, dense circle, spiral."""
    g = VGroup()
    cs = [c + P(-0.58, 0.45), c + P(0.58, 0.45), c + P(-0.58, -0.45), c + P(0.58, -0.45)]
    for k in cs:
        g.add(Rectangle(width=1.05, height=0.8).set_stroke(DIM, 1.5).move_to(k))
    g.add(Dot(cs[0] + 0.2 * LEFT, radius=0.07, color=GREEN))
    for m in range(5):
        g.add(Dot(cs[1] + 0.27 * _dir(PI / 10 + TAU * m / 5), radius=0.05, color=GREEN if m == 0 else TEAL))
    g.add(Circle(radius=0.3, color=GOLD, stroke_width=1.5).move_to(cs[2]))
    for n in range(1, 70):
        g.add(Dot(cs[2] + 0.3 * _dir(np.sqrt(2) * (PI / 2 + TAU * n)), radius=0.018, color=TEAL))
    g.add(Dot(cs[2] + 0.3 * _dir(np.sqrt(2) * PI / 2), radius=0.05, color=GREEN))
    curve = VMobject().set_points_as_corners([_spiral_pt(cs[3], 0.19, t) for t in np.linspace(-5.3, 10.4, 300)])
    g.add(curve.set_stroke(TEAL, 1.5, opacity=0.4))
    for n in range(-5, 11):
        g.add(Dot(_spiral_pt(cs[3], 0.19, n), radius=0.04 if n else 0.05, color=GREEN if n == 0 else TEAL))
    return g


def thumb_powers(c):
    """ch2 s2: e^{iθ}, e^{2iθ}, e^{3iθ}, each a θ further (ch2's ray and θ-arc)."""
    o = c + P(-0.55, -0.6)
    u = 1.25
    g = VGroup(axes(o, 0.3, 1.5, 0.3, 1.45),
               Arc(radius=u, start_angle=0, angle=PI / 2, arc_center=o, color=DIM, stroke_width=1.5))
    for k in range(3):
        g.add(CH2.theta_arc(k, center=o, radius=0.3 + 0.12 * k))
    for k in range(3):
        g.add(CH2.ray(CH2.THETA * (k + 1), center=o, unit=u).set_opacity(1.0 if k == 2 else 0.4))
    return g


def thumb_chain(c):
    """ch3 s3: six unit arrows, each θ = π/6 further, curling up; S_N their shadow."""
    u = 0.42
    o = c + P(-0.45, -0.75)
    g = VGroup(axes(o, 0.5, 1.4, 0.15, 1.65))
    p = o.copy()
    for k in range(6):
        q = p + u * _dir(k * PI / 6)
        g.add(Arrow(p, q, buff=0, stroke_width=4, color=GOLD, tip_length=0.12,
                    max_tip_length_to_length_ratio=0.35))
        p = q
    foot = P(p[0], o[1])
    g.add(DashedLine(p, foot, color=DIM, stroke_width=2, dash_length=0.06))
    g.add(Line(o + 0.07 * DOWN, foot + 0.07 * DOWN, color=BLUE, stroke_width=5))
    g.add(Dot(foot, radius=0.07, color=BLUE), Dot(p, radius=0.08, color=YELLOW))
    return g


def thumb_phasor(c):
    """ch6 s3: the GOLD arrow on its circle, its BLUE shadow on the real axis."""
    o, r = c + P(-0.1, 0.05), 0.72
    a = -PI / 3
    tip = o + r * _dir(a)
    foot = P(tip[0], o[1])
    g = VGroup(axes(o, 0.95, 0.95, 0.85, 0.85),
               Circle(radius=r, color=GOLD, stroke_width=2).set_stroke(opacity=0.45).move_to(o),
               DashedLine(tip, foot, color=DIM, stroke_width=2, dash_length=0.06),
               Dot(foot, radius=0.08, color=BLUE),
               Arrow(o, tip, buff=0, stroke_width=5, color=GOLD, tip_length=0.18,
                     max_tip_length_to_length_ratio=0.3))
    return g


def thumb_four(c):
    """ch7 s3: the four amplitude arrows and their shadows."""
    o, u = c + P(-0.5, 0.15), 0.2
    g = VGroup(axes(o, 0.4, 1.35, 0.8, 0.6))
    arrows = S5.amp_arrows(PHI0, center=o, unit=u, width=4, tip=0.14)
    for key, r, off, col in (("v0", 5, -S5.LAG, FG), ("vr", 4, 0.0, BLUE), ("vc", 3, -PI / 2, PINK),
                             ("i0", 1, 0.0, GOLD)):
        sh = S3._shadow(o + r * u * _dir(PHI0 + off), col, o)
        sh[1].scale(0.7)
        g.add(sh)
    g.add(arrows)
    return g


def thumb(c, color, build):
    return VGroup(frame(c, color), build(c))


# ---------------------------------------------------------------- the scene
class Recap(NarratedScene):
    def construct(self):
        ph = ValueTracker(PHI0)
        ph.add_updater(lambda m, dt: m.increment_value(S3.OMEGA * dt))
        self.add(ph)
        self.ph = ph
        self.recap()
        self.lecture()
        self.next_time()

    # ------------------------------------------------------------ clip 1: the four panels
    def recap(self):
        circ, laws, cap1 = panel_r1()
        self.ops = {k: ValueTracker(0.0) for k in ("vr", "vc", "v0", "i0")}
        plane2, arrows2, shadows2, cap2 = panel_r2(lambda: self.ph.get_value(), self.ops)
        self.live = [arrows2, shadows2]
        rule3, plane3, pair3, cap3 = panel_r3()
        zb, box, tri, cap4 = panel_r4()
        rows = list(laws)

        with self.say("c7.recap.1", gap=1.2) as c:
            c.wait_until("r1")
            self.play(FadeIn(circ), run_time=1.0)
            c.wait_until("four laws")
            self.play(*appear(cap1), run_time=0.9)
            c.wait_until("one for each part")
            self.play(*appear(rows[0], rows[1], lag=0.35), run_time=1.3)
            c.wait_until("the current")
            self.play(*appear(rows[2]), run_time=0.9)
            c.wait_until("the loop")
            self.play(*appear(rows[3]), run_time=0.9)

            c.wait_until("r2")
            self.add(arrows2, shadows2)
            self.play(FadeIn(plane2), *[o.animate.set_value(1.0) for o in self.ops.values()],
                      *appear(cap2), run_time=1.2)
            c.wait_until("r3")
            self.play(*appear(rule3), *appear(cap3), run_time=1.1)
            c.wait_until("multiplication")
            self.play(FadeIn(plane3), GrowArrow(pair3.vc), GrowArrow(pair3.i0), FadeIn(pair3.mark),
                      run_time=1.3)
            c.wait_until("so the laws become algebra")
            self.play(FlashAround(laws, run_time=1.5, time_width=1.5, buff=0.15))

            c.wait_until("r4")
            self.play(FadeIn(tri), run_time=1.2)
            c.wait_until(own_word=cap4)
            self.play(*appear(cap4), run_time=0.9)
            c.wait_until("zed")
            self.play(*appear(zb), FadeIn(box), run_time=1.0)
            c.wait_until("minus eye over omega")
            self.play(FlashAround(box, run_time=1.5, time_width=1.5))

    # ------------------------------------------------------------ clip 2: two threads
    def lecture(self):
        th1 = Line(P(-6.6, ROW1_Y), P(6.6, ROW1_Y)).set_stroke(TEAL, 4, opacity=0.55).set_z_index(-2)
        th2 = Line(P(-6.6, ROW2_Y), P(6.6, ROW2_Y)).set_stroke(GOLD, 4, opacity=0.55).set_z_index(-2)
        h1 = T("the 2πn", 38, TEAL).move_to(P(0, 3.4)).align_to(P(-6.3, 0), LEFT)
        tag1 = T("Parts 1, 4, 5", 30, DIM).move_to(P(0, 3.4)).align_to(P(6.3, 0), RIGHT)
        h2 = T("the turning arrow", 38, GOLD).move_to(P(0, -0.3)).align_to(P(-6.3, 0), LEFT)
        tag2 = T("Parts 2, 3, 6, 7", 30, DIM).move_to(P(0, -0.3)).align_to(P(6.3, 0), RIGHT)
        row1 = [thumb(P(x, ROW1_Y), TEAL, b) for x, b in zip(ROW1_X, (thumb_ring, thumb_ladder, thumb_gallery))]
        row2 = [thumb(P(x, ROW2_Y), GOLD, b)
                for x, b in zip(ROW2_X, (thumb_powers, thumb_chain, thumb_phasor, thumb_four))]
        lab1 = [T(s, 28, DIM).next_to(t, DOWN, buff=0.15) for s, t in zip(("roots", "logarithms", "powers"), row1)]
        lab2 = [T(s, 28, DIM).next_to(t, DOWN, buff=0.15)
                for s, t in zip(("De Moivre", "cosine sums", "oscillations", "circuits"), row2)]

        with self.say("c7.recap.2", gap=1.5) as c:
            sweep_clear(self, *during([o.animate.set_value(0.0) for o in self.ops.values()], 0, 0.5),
                        time_span(Create(th1), 0.6, 1.6), time_span(Create(th2), 0.8, 1.8),
                        keep=[self.ph, *self.live, *self.ops.values()], run_time=1.8)
            self.remove(*self.live, *self.ops.values())
            c.wait_until("thread1")
            self.play(*appear(h1), run_time=0.8)
            self.play(*appear(tag1), run_time=0.7)  # early: the parts tag belongs with its thread's name
            for k, w in enumerate(("roots", "logarithms", "powers")):
                c.wait_until(w)
                nxt = ("logarithms", "powers", None)[k]
                self.play(*appear(row1[k], lab1[k], lag=0.2),
                          run_time=min(1.0, max(0.5, 0.9 * c.until(nxt)) if nxt else 1.0))
            c.wait_until("thread2")
            self.play(*appear(h2), run_time=0.8)
            self.play(*appear(tag2), run_time=0.7)  # early: the parts tag belongs with its thread's name
            cues = ("De Moivre's", "sums of cosines", "oscillations", "circuits")
            for k, w in enumerate(cues):
                c.wait_until(w)
                nxt = cues[k + 1] if k + 1 < len(cues) else None
                self.play(*appear(row2[k], lab2[k], lag=0.2),
                          run_time=min(1.0, max(0.5, 0.9 * c.until(nxt))) if nxt else 1.0)

    # ------------------------------------------------------------ clip 3: next time + end card
    def next_time(self):
        title = T("Lecture 11", 56).move_to(P(0, 2.7))
        line = MathTex(r"e^{i\theta}", r"\;\longrightarrow\;", r"e^{x}", font_size=60).move_to(P(0, 1.0))
        line[0].set_color(GOLD)
        line[2].set_color(GOLD)
        eq = MathTex(r"\tfrac{1}{2}\big(", "e^{x}", "+", "e^{-x}", r"\big)", "=", r"\cosh x", font_size=64)
        eq[1].set_color(GOLD)
        eq[3].set_color(PURPLE)
        eq.move_to(P(0, -0.65))
        card_t = T("Part 8 · Solutions (bonus): F12, F13, F15–F19", 32)
        card_b = RoundedRectangle(corner_radius=0.18, width=card_t.width + 0.7, height=card_t.height + 0.55)
        card_b.set_stroke(DIM, 2).set_fill(BG, 1)
        card = VGroup(card_b, card_t).move_to(P(0, -2.65))
        card_t.move_to(card_b)

        with self.say("c7.recap.3", gap=0.0) as c:
            sweep_clear(self, *appear(title), time_span(FadeIn(line[0]), 0.9, 1.6), run_time=1.8)
            c.wait_until("turns real")
            self.play(GrowFromPoint(line[1], line[0].get_right()), run_time=0.8)
            self.play(*appear(line[2], shift=None), run_time=min(1.0, c.until("cosh")))
            c.wait_until("cosh")
            self.play(*appear(eq), run_time=1.3)
            c.wait_until("hyperbolic cosine")
            self.play(FlashAround(eq[6], run_time=1.5, time_width=1.5), *recolor(eq[6], YELLOW))
            c.wait_until("bonus")
            self.play(FadeIn(card_b), *appear(card_t), run_time=1.2)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
