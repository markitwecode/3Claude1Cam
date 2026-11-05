"""Chapter 8, scene 3: F16, two circles; when they coincide; the six roots of z^6 - 2z^3 + 2. Clips c8.f16.1 – c8.f16.5.

Shared piece for the recap (ch8_s8_end):
  recap_panel()  plane + dashed GOLD 2^{1/6} circle + GOLD triple (1 + i) + PURPLE triple (1 - i)
                 + the two angle formulas (m, 2πm TEAL), as at {mirror}.
                 Parts: .plane .circle .gold .purple .fa .fb
"""
# style: 2
import cmath
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

INTRO = load_scene("ch8_s1_intro")
argand_plane = load_scene("ch2_s2_theorem").argand_plane

LX = -6.3                                   # left column edge (clip 2)
RX = 0.9                                    # right column edge (clips 3-5)
# clip 2 plane (the two rings)
O2, U2, E2 = np.array([3.7, -0.3, 0.0]), 1.8, 2.6
# clips 3-5 plane (parallelogram, square, six roots)
O3, U3, E3 = np.array([-3.3, -0.6, 0.0]), 2.2, 2.75
R6 = 2 ** (1 / 6)
DOT_R = 0.11
GOLD_DEG = (15, 135, 255)
PURPLE_DEG = (345, 225, 105)

# illustrative values for the two rings (never spoken)
B_EX, C_EX, N_EX = 0.6 + 0.5j, -0.4 + 0.3j, 4
S_EX = cmath.sqrt(B_EX ** 2 - C_EX)
W1, W2 = B_EX + S_EX, B_EX - S_EX


def tex(*s, size=44, color=FG):
    return MathTex(*s, font_size=size, color=color)


def P(z, center=O3, unit=U3):
    return center + unit * np.array([z.real, z.imag, 0.0])


def polar(r, deg):
    return r * cmath.exp(1j * np.deg2rad(deg))


def ring_circle(r, center, unit):
    return DashedVMobject(Circle(radius=unit * r, color=GOLD, stroke_width=3).move_to(center), num_dashes=40)


def root_dots(degs, r, color, center=O3, unit=U3, first=None):
    return VGroup(*[Dot(P(polar(r, d), center, unit), radius=DOT_R,
                        color=first if (first and k == 0) else color).set_z_index(3)
                    for k, d in enumerate(degs)])


def angle_formula(sign):
    """'1 + i:  θ = π/12 + 2πm/3' (sign '+') or the 1 - i one; 1 ± i coloured, 2πm TEAL."""
    col = GOLD if sign == "+" else PURPLE
    pre = r"1 + i:" if sign == "+" else r"1 - i:"
    th = r"\ \ \theta = \pi/12 + " if sign == "+" else r"\ \ \theta = -\pi/12 + "
    m = tex(pre, th, r"2\pi m", r"/3", size=44)
    m[0].set_color(col)
    m[2].set_color(TEAL)
    return m


def place_left(m, y, x=RX):
    m.move_to([0, y, 0]).align_to([x, 0, 0], LEFT)
    return m


def recap_panel():
    plane = argand_plane(O3, U3, E3)
    circle = ring_circle(R6, O3, U3)
    gold = root_dots(GOLD_DEG, R6, GOLD)
    purple = root_dots(PURPLE_DEG, R6, PURPLE)
    fa = place_left(angle_formula("+"), 1.0)
    fb = place_left(angle_formula("-"), -0.2)
    g = VGroup(plane, circle, gold, purple, fa, fb)
    g.plane, g.circle, g.gold, g.purple, g.fa, g.fb = plane, circle, gold, purple, fa, fb
    return g


def boxed(m, color=YELLOW, buff=0.25):
    return SurroundingRectangle(m, color=color, buff=buff, corner_radius=0.12, stroke_width=3)


class F16(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ clip 1: the card
    def clip1(self):
        lines = [
            tex(r"\text{Show that the roots of }z^{2n} - 2bz^n + c = 0", size=44),
            tex(r"\text{lie on two circles in the Argand diagram.}", size=44),
            tex(r"\text{Give a condition on }b\text{ and }c\text{ such that the}", size=44),
            tex(r"\text{circles coincide. Find the largest value of}", size=44),
            tex(r"|z_1 - z_2|\text{ when }z_1\text{ and }z_2\text{ are roots of}", size=44),
            tex(r"z^6 - 2z^3 + 2 = 0.", size=44),
        ]
        q = INTRO.question_card("F16", lines)
        self.q = q
        row = INTRO.card_row()
        small = row.cards[1]
        with self.say("c8.f16.1") as c:
            self.play(FadeIn(row), run_time=1.0)
            others = [cd for i, cd in enumerate(row.cards) if i != 1]
            self.play(*disappear(*others, small.icon, small.tag), run_time=0.8)
            self.play(TransformFromCopy(small.box, q.box), *fly(small.label, q.label),
                      *during(disappear(small.label), 0, 0.3), run_time=1.5)
            self.remove(*small.get_family())
            self.play(*appear(*q.body, lag=0.15, shift=None), *appear(q.icon, shift=None),  # early: the question card is read whole
                      run_time=1.6)
            c.wait_until("chord")
            self.play(FlashUnder(VGroup(q.body[4], q.body[5]), color=YELLOW, run_time=2, time_width=1.5))
            c.wait_until("stop")
            self.play(FlashAround(q.icon, color=YELLOW, run_time=1.5, time_width=1.5))

    # ------------------------------------------------------------ clip 2: substitute, two rings
    def clip2(self):
        r0 = left_at(tex(r"w = z^n", size=48, color=YELLOW), 3.0)
        r1 = left_at(tex(r"z^{2n} - 2bz^n + c = 0", size=52), 1.9)
        r1w = tex(r"w", r"^2 - 2b", r"w", r" + c = 0", size=52)
        r1w[0].set_color(YELLOW)
        r1w[2].set_color(YELLOW)
        left_at(r1w, 1.9)
        r2a = left_at(tex(r"w = b \pm s,", size=44), 0.7)
        r2b = tex(r"s = \sqrt{b^2 - c}", size=44).next_to(r2a, RIGHT, buff=0.45)
        r2b.shift((r2a[0][0].get_y() - r2b[0][0].get_y()) * UP)
        r3 = left_at(tex(r"w_1 = b + s,\quad w_2 = b - s", size=44), -0.5)
        r4 = left_at(tex(r"\text{radius } |w|^{1/n}", size=44, color=GOLD), -1.6)
        r5 = left_at(tex(r"\text{same circle} \iff |w_1| = |w_2|", size=44), -2.8)
        self.r5 = r5

        plane = argand_plane(O2, U2, E2)
        cap = tex(r"\text{e.g. } n = 4,\ \ b = 0.6 + 0.5i,\ \ c = -0.4 + 0.3i", size=28, color=DIM)
        cap.move_to([O2[0], 3.15, 0])
        rings = []
        for w in (W1, W2):
            r = abs(w) ** (1 / N_EX)
            a0 = np.rad2deg(cmath.phase(w)) / N_EX
            degs = [a0 + 90 * k for k in range(N_EX)]
            circ = ring_circle(r, O2, U2)
            dots = root_dots(degs, r, TEAL, O2, U2, first=GREEN)
            rings.append((r, a0, circ, dots))
        lab1 = tex(r"1.11", size=32, color=GOLD)
        lab1.move_to(P(polar(rings[0][0] * U2 + 0.38, rings[0][1] + 315) / U2, O2, U2))
        lab2 = tex(r"0.76", size=32, color=GOLD)
        lab2.move_to(P(polar(rings[1][0] * U2 + 0.34, rings[1][1] + 225) / U2, O2, U2))
        for lab in (lab1, lab2):
            set_backstroke(lab)

        with self.say("c8.f16.2") as c:
            self.play(*disappear(self.q), run_time=0.8)
            self.play(*appear(r1, r0, lag=0.5), run_time=1.4)
            c.wait_until("w squared")
            self.play(*edit(r1, r1w), run_time=min(1.8, c.until("roots") - 0.3))
            c.wait_until("roots")
            self.play(*appear(r2a), run_time=1.0)
            c.wait_until("where")
            self.play(*appear(r2b), run_time=1.0)
            self.play(FadeIn(plane), *appear(cap, shift=None), run_time=1.0)
            c.wait_until("ring1")
            self.play(*appear(r3), run_time=1.0)
            c.wait_until("ring")
            circ1, dots1 = rings[0][2], rings[0][3]
            self.play(Create(circ1), *[GrowFromCenter(d) for d in dots1], run_time=1.4)
            c.wait_until("radius")
            self.play(*appear(r4), *appear(lab1, shift=None), run_time=1.0)
            circ2, dots2 = rings[1][2], rings[1][3]
            self.play(Create(circ2), *[GrowFromCenter(d) for d in dots2], *appear(lab2, shift=None), run_time=1.3)
            c.wait_until("two_circles")
            self.play(*[VShowPassingFlash(cc.copy().set_stroke(YELLOW, 6), time_width=0.6, run_time=1.6)
                        for cc in (circ1, circ2)])
            c.wait_until("coincide")
            self.play(*appear(r5), run_time=1.0)

    # ------------------------------------------------------------ clip 3: when do they coincide?
    def clip3(self):
        self.bl, self.ba = ValueTracker(1.25), ValueTracker(20)
        self.sl, self.sa = ValueTracker(0.9), ValueTracker(75)
        bz = lambda: polar(self.bl.get_value(), self.ba.get_value())  # noqa: E731
        sz = lambda: polar(self.sl.get_value(), self.sa.get_value())  # noqa: E731
        self.bz, self.sz = bz, sz
        akw = dict(buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.15, tip_length=0.26)
        self.plane = argand_plane(O3, U3, E3)
        self.b_arr = always_redraw(lambda: Arrow(O3, P(bz()), color=FG, **akw).set_z_index(2))
        self.s_arr = always_redraw(lambda: Arrow(O3, P(sz()), color=FG, **akw).set_z_index(2))
        self.side1 = always_redraw(lambda: DashedLine(P(bz()), P(bz() + sz()), color=DIM, stroke_width=3))
        self.side2 = always_redraw(lambda: DashedLine(P(sz()), P(bz() + sz()), color=DIM, stroke_width=3))
        self.dp = always_redraw(lambda: Line(O3, P(bz() + sz()), color=YELLOW, stroke_width=4))
        self.dm = always_redraw(lambda: Line(P(sz()), P(bz()), color=YELLOW, stroke_width=4))

        def tip_off(z, d=0.32):
            return P(z) + d * np.array([np.cos(cmath.phase(z)), np.sin(cmath.phase(z)), 0])

        self.b_lab = tex("b", size=40)
        self.b_lab.add_updater(lambda m: m.move_to(tip_off(bz())))
        self.s_lab = tex("s", size=40)
        self.s_lab.add_updater(lambda m: m.move_to(tip_off(sz())))
        self.dp_lab = tex("b + s", size=34, color=YELLOW)
        self.dp_lab.add_updater(lambda m: m.move_to(tip_off(bz() + sz(), 0.45)))

        def dm_pos(m):
            # upright, beside the b - s diagonal on the origin side, between the diagonals and b
            b, s = bz(), sz()
            p = b + 0.35 * (s - b)
            d = (s - b) / abs(s - b)
            n = d * 1j
            if (n * (b + s).conjugate()).real > 0:
                n = -n
            off = 0.5 * (m.width * abs(n.real) + m.height * abs(n.imag)) + 0.08
            m.move_to(P(p) + off * np.array([n.real, n.imag, 0]))

        self.dm_lab = tex("b - s", size=32, color=YELLOW)
        self.dm_lab.add_updater(dm_pos)
        for lab in (self.b_lab, self.s_lab, self.dp_lab, self.dm_lab):
            set_backstroke(lab)

        def length_row(sym, y, fn):
            lab = tex(sym, size=44, color=YELLOW)
            eq = tex(r"\approx", size=44)
            num = DecimalNumber(fn(), num_decimal_places=2, font_size=44, color=GOLD)
            g = VGroup(lab, eq, num).arrange(RIGHT, buff=0.22)
            place_left(g, y)
            num.add_updater(lambda m: m.set_value(fn()))
            return g

        self.len_p = length_row(r"|b + s|", 2.0, lambda: abs(bz() + sz()))
        self.len_m = length_row(r"|b - s|", 1.15, lambda: abs(bz() - sz()))

        def rmark():
            b, s = bz(), sz()
            ub, us = b / abs(b), s / abs(s)
            k = 0.28 / U3
            pts = [P(k * ub), P(k * (ub + us)), P(k * us)]
            return VMobject(stroke_color=FG, stroke_width=3).set_points_as_corners(pts)

        self.rmark = always_redraw(rmark)

        a1 = place_left(tex(r"s = itb,\quad t \text{ real}", size=44), 0.0)
        a2 = place_left(tex(r"s^2 = -t^2b^2 = b^2 - c", size=44), -0.9)
        a3 = place_left(tex(r"\Rightarrow\ c = b^2(1 + t^2)", size=44), -1.8)
        ans = tex(r"c/b^2\ \text{real and}\ \geq 1\ \ (\text{or } b = 0)", size=40, color=YELLOW)
        place_left(ans, -3.05, RX + 0.25)
        ans_box = boxed(ans)
        self.alg = [a1, a2, a3]
        self.ans, self.ans_box = ans, ans_box

        with self.say("c8.f16.3") as c:
            sweep_clear(self, self.r5.animate.move_to([0, 3.4, 0]), keep=[self.r5], run_time=1.4)
            c.wait_until("para")
            self.play(FadeIn(self.plane), run_time=0.8)
            self.play(GrowArrow(self.b_arr), GrowArrow(self.s_arr),
                      *appear(self.b_lab, self.s_lab, shift=None), run_time=1.2)
            c.wait_until("then b plus s")
            self.play(Create(self.side1), Create(self.side2), run_time=1.0)
            c.wait_until("diagonals")
            self.play(Create(self.dp), Create(self.dm), *appear(self.dp_lab, self.dm_lab, shift=None),
                      run_time=1.2)
            self.play(*appear(self.len_p, self.len_m, lag=0.4), run_time=1.2)
            c.wait_until("rect")
            self.play(self.sa.animate.set_value(110), run_time=2.0)
            c.wait_until("right angles")
            self.play(FadeIn(self.rmark), *flash([self.len_p[2], self.len_m[2]], color=GOLD, run_time=1.5,
                                                 time_width=1.5), run_time=1.5)
            c.wait_until("algebra")
            self.play(*appear(a1), run_time=1.0)
            c.wait_until("squaring")
            self.play(*appear(a2), run_time=1.0)
            c.wait_until("c equals")
            self.play(*appear(a3), run_time=1.0)
            c.wait_until("answer")
            self.play(*appear(ans, shift=None), FadeIn(ans_box), run_time=1.2)

    # ------------------------------------------------------------ clip 4: the example, a square
    def clip4(self):
        ex1 = place_left(tex(r"z^6 - 2z^3 + 2 = 0", size=44), 2.5)
        ex2 = place_left(tex(r"n = 3,\ \ b = 1,\ \ c = 2", size=44), 1.6)
        chk = place_left(tex(r"c/b^2 = 2", size=44), -0.6)
        tick = check_mark().next_to(chk, RIGHT, buff=0.35)
        m1 = place_left(tex(r"|1 \pm i| = \sqrt{2}\ \Rightarrow\ |z| = (\sqrt{2})^{1/3}", size=42, color=GOLD), -1.75)
        m2 = place_left(tex(r"= 2^{1/6} \approx 1.12", size=42, color=GOLD), -2.7, RX + 2.2)
        one = tex("1", size=40, color=BLUE).move_to(P(1 + 0j) + 0.32 * DOWN + 0.05 * RIGHT)
        eye = tex("i", size=40, color=PINK).move_to(P(1j) + 0.32 * LEFT)
        for m in (one, eye):
            set_backstroke(m)
        self.circle = ring_circle(R6, O3, U3)

        with self.say("c8.f16.4") as c:
            self.play(*disappear(self.len_p, self.len_m, *self.alg, self.r5, self.dp_lab, self.dm_lab),
                      run_time=0.8)
            self.play(self.ans.animate.move_to([self.ans.get_x(), 0.55, 0]),
                      self.ans_box.animate.move_to([self.ans_box.get_x(), 0.55, 0]),
                      *during(appear(ex1, ex2, lag=0.4), 0.3, 1), run_time=1.6)
            c.wait_until("c is two")
            self.play(*appear(chk), run_time=0.8)
            self.play(Create(tick), run_time=0.6)
            c.wait_until("square")
            for m in (self.b_lab, self.s_lab):
                m.clear_updaters()
            self.play(*disappear(self.b_lab, self.s_lab), run_time=0.6)
            self.play(self.bl.animate.set_value(1), self.ba.animate.set_value(0),
                      self.sl.animate.set_value(1), self.sa.animate.set_value(90), run_time=1.8)
            for m in (self.b_arr, self.s_arr, self.dm, self.side1, self.side2, self.dp, self.rmark):
                m.clear_updaters()
            c.wait_until("right angles")
            self.play(self.b_arr.animate.set_color(BLUE), self.s_arr.animate.set_color(PINK),
                      *appear(one, eye, shift=None), run_time=1.0)
            # the mirror square, b - s: its far corner is 1 - i
            akw = dict(buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.15, tip_length=0.26)
            ms = Arrow(O3, P(-1j), color=PINK, **akw).set_opacity(0.5)
            mside1 = DashedLine(P(1 + 0j), P(1 - 1j), color=DIM, stroke_width=3)
            mside2 = DashedLine(P(-1j), P(1 - 1j), color=DIM, stroke_width=3)
            dm2 = Line(O3, P(1 - 1j), color=YELLOW, stroke_width=4)
            self.play(FadeOut(self.dm), GrowArrow(ms), Create(mside1), Create(mside2), run_time=1.0)
            self.play(Create(dm2), run_time=0.8)
            self.wp = Dot(P(1 + 1j), radius=DOT_R, color=GOLD).set_z_index(3)
            self.wm = Dot(P(1 - 1j), radius=DOT_R, color=PURPLE).set_z_index(3)
            self.wp_lab = set_backstroke(tex(r"1 + i", size=36, color=GOLD).next_to(self.wp, UR, buff=0.08))
            self.wm_lab = set_backstroke(tex(r"1 - i", size=36, color=PURPLE).next_to(self.wm, RIGHT, buff=0.15))
            c.wait_until("mod")
            self.play(GrowFromCenter(self.wp), GrowFromCenter(self.wm),
                      *appear(self.wp_lab, self.wm_lab, shift=None), run_time=1.0)
            c.wait_until("modulus root two")
            self.play(*appear(m1), run_time=1.0)
            c.wait_until("every root")
            self.play(*appear(m2), Create(self.circle), run_time=1.4)
            self.square = [self.b_arr, self.s_arr, self.side1, self.side2, self.dp, self.rmark, one, eye,
                           ms, mside1, mside2, dm2]
            self.right4 = [ex1, ex2, chk, tick, self.ans, self.ans_box]
            self.mods = [m1, m2]

    # ------------------------------------------------------------ clip 5: the six roots, the longest chord
    def clip5(self):
        panel = recap_panel()
        gold, purple, fa, fb = panel.gold, panel.purple, panel.fa, panel.fb
        note1 = place_left(T("m counts turns", size=36, t2c={"m": TEAL}), 2.85)
        note2 = place_left(T("(n is the sheet’s power here)", size=28, color=DIM), 2.3)

        def deg_lab(d, color):
            lab = tex(rf"{d}^\circ", size=30, color=color)
            lab.move_to(P(polar(R6 + 0.36 / U3, d)))
            return set_backstroke(lab)

        glabs = [deg_lab(d, GOLD) for d in GOLD_DEG]
        plabs = [deg_lab(d, PURPLE) for d in PURPLE_DEG]
        z = lambda d: P(polar(R6, d))  # noqa: E731

        with self.say("c8.f16.5", gap=3.2) as c:
            self.play(*disappear(*self.square, *self.right4), run_time=1.0)
            self.play(*appear(note1, note2, lag=0.4), run_time=1.2)
            c.wait_until("one plus eye gives")
            self.play(*appear(fa, shift=None), run_time=1.2)
            for k, cue in enumerate(["fifteen", "a hundred and thirty-five", "two hundred and fifty-five"]):
                c.wait_until(cue)
                self.play(*fly(self.wp, gold[k]), *appear(glabs[k], shift=None), run_time=1.0 if k == 0 else 0.8)
            c.wait_until("mirror")
            ghosts = [d.copy() for d in gold]
            self.play(*[g.animate.move_to(p.get_center()).set_color(PURPLE) for g, p in zip(ghosts, purple)],
                      *during(appear(fb, shift=None), 0.3, 1), run_time=1.6)
            self.remove(*ghosts)
            self.add(*purple)
            self.play(*appear(*plabs, shift=None, lag=0.1), run_time=0.8)
            c.wait_until("none")
            dia = DashedLine(z(15), z(195), color=RED, stroke_width=4, dash_length=0.12)
            miss = cross_mark().scale(0.7).move_to(z(195))
            self.play(Create(dia), *disappear(*self.mods), run_time=0.9)
            self.play(GrowFromCenter(miss), run_time=0.5)
            c.wait_until("chord_long")
            chord = Line(z(15), z(225), color=YELLOW, stroke_width=6).set_z_index(1)
            radii = VGroup(Line(O3, z(15)), Line(O3, z(225))).set_stroke(YELLOW, 2.5, opacity=0.7)
            arc = Arc(radius=0.4, start_angle=np.deg2rad(225), angle=np.deg2rad(150), arc_center=O3,
                      color=YELLOW, stroke_width=4)
            alab = set_backstroke(tex(r"150^\circ", size=32, color=YELLOW).move_to(
                O3 + 0.95 * np.array([np.cos(np.deg2rad(300)), np.sin(np.deg2rad(300)), 0])))
            self.play(*disappear(dia, miss), Create(chord), run_time=1.0)
            self.play(Create(radii), Create(arc), *appear(alab, shift=None), run_time=1.0)
            others = [Line(z(105), z(255)), Line(z(135), z(345))]
            self.play(*[VShowPassingFlash(o.set_stroke(YELLOW, 6), time_width=1.0, run_time=1.5) for o in others])
            c.wait_until("len")
            l1 = tex(r"|z_1 - z_2| = 2 \cdot 2^{1/6} \sin 75^\circ", size=42)
            l2 = tex(r"= (1 + \sqrt{3})/\sqrt[3]{2} \approx 2.17", size=42)
            place_left(l1, -1.75, RX + 0.25)
            place_left(l2, -2.75, RX + 0.9)
            box = boxed(VGroup(l1, l2))
            self.play(*appear(l1, shift=None), FadeIn(box), run_time=1.2)
            c.wait_until("that's one plus")
            self.play(*appear(l2, shift=None), run_time=1.0)


def left_at(m, y):
    m.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
    return m
