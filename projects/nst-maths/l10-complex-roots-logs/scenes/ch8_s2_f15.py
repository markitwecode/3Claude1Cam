"""Chapter 8, scene 2: F15, four root equations solved by Part 1's three steps. Clips c8.f15.1 – c8.f15.5."""
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

S1 = load_scene("ch8_s1_intro")
CH2 = load_scene("ch2_s2_theorem")
CH1 = load_scene("ch1_s3_unity")

UNIT = 1.15
EXT = 1.45
XS = [0.6, 4.4]
YS = [1.55, -2.05]
CENTERS = {"a": (0, 0), "b": (1, 0), "c": (0, 1), "d": (1, 1)}
LX = -6.4                 # left edge of the working column
ROWS = [1.8, 0.0, -1.5]
FS = 52                   # working font size
DR = 0.09                 # root dot radius
LAB_FS = 32               # Cartesian labels

EQS = {"a": r"(a)\ \ z^3 = -1", "b": r"(b)\ \ z^4 = 1", "c": r"(c)\ \ z^2 = i", "d": r"(d)\ \ z^3 = -i"}


def ctr(p):
    i, j = CENTERS[p]
    return np.array([XS[i], YS[j], 0.0])


def pt(p, deg):
    a = np.deg2rad(deg)
    return ctr(p) + UNIT * np.array([np.cos(a), np.sin(a), 0])


def mark(*mobs):
    """Remember each part's opacities, so light() can dim and restore them."""
    for mob in mobs:
        for m in mob.family_members_with_points():
            m._base = (m.get_stroke_opacity(), m.get_fill_opacity())


def light(mobs, k):
    out = []
    for mob in mobs:
        for m in mob.family_members_with_points():
            bs, bf = getattr(m, "_base", (m.get_stroke_opacity(), m.get_fill_opacity()))
            out.append(m.animate.set_stroke(opacity=bs * k).set_fill(opacity=bf * k))
    return out


def row(tex, y, yellow=None, teal=None):
    m = MathTex(tex, font_size=FS)
    if yellow:
        m[0][yellow[0]:yellow[1]].set_color(YELLOW)
    if teal:
        m[0][teal[0]:teal[1]].set_color(TEAL)
    m.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
    return m


def nrow(vals, y):
    m = MathTex("n = " + ", ".join(str(v) for v in vals), font_size=FS)
    for k in range(len(vals)):
        m[0][2 + 2 * k].set_color(GREEN if k == 0 else TEAL)
    m.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
    return m


def root_dot(p, deg, k):
    return Dot(pt(p, deg), radius=DR, color=GREEN if k == 0 else TEAL).set_z_index(2)


def cart(tex, p, deg, k, side):
    lab = MathTex(tex, font_size=LAB_FS, color=GREEN if k == 0 else TEAL)
    if side is DR or side is DL:   # just below the dot, outward: clear of the Re labels and plane (c)
        d = pt(p, deg)
        lab.next_to(d, DOWN, buff=0.06 + DR)
        if side is DR:
            lab.align_to(d + 0.05 * RIGHT, LEFT)
        else:
            lab.align_to(d + 0.05 * LEFT, RIGHT)
    else:
        lab.next_to(pt(p, deg), side, buff=0.12 + DR)
    return set_backstroke(lab, width=5)


def outline(p, degs):
    pts = [pt(p, d) for d in degs]
    m = Polygon(*pts) if len(pts) > 2 else Line(*pts)
    return m.set_stroke(TEAL, 2.5, opacity=0.85).set_z_index(1)


class F15(NarratedScene):
    def construct(self):
        shot = S1.handover_shot()
        self.add(shot)
        self.row, self.steps0 = shot[0], shot[1]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ the card
    def clip1(self):
        cards = self.row.cards
        f15 = cards[0]
        self.eqs = {p: MathTex(EQS[p], font_size=44) for p in "abcd"}
        eq_row = VGroup(*self.eqs.values()).arrange(RIGHT, buff=0.85)
        q = S1.question_card("F15", ["Find all solutions of the following equations, and indicate",
                                     "their location on the Argand diagram:", eq_row], size=34)
        eq_row.set_x(q.box.get_x())
        self.q = q
        with self.say("c8.f15.1") as c:
            self.play(*disappear(*cards[1:], self.steps0, f15.icon, f15.tag, lag=0.04), run_time=0.8)
            self.play(TransformFromCopy(f15.box, q.box), *fly(f15.label, q.label),
                      *during([FadeOut(f15.box), FadeOut(f15.label)], 0, 0.3),
                      *during(appear(q.icon, shift=None), 0.6, 1),
                      run_time=min(1.3, c.until("Find all")))
            c.wait_until(own_word=q.body[0])
            self.play(*appear(q.body[0], q.body[1], lag=0.5), run_time=1.4)  # early: the question text, shown as one
            c.wait_until("eqs")
            self.play(*appear(self.eqs["a"]), run_time=0.8)
            for p, cue in (("b", "zed to the fourth"), ("c", "zed squared"), ("d", "and zed cubed")):
                c.wait_until(cue)
                self.play(*appear(self.eqs[p]), run_time=0.8)
            c.wait_until("stop")
            self.play(FlashAround(q.icon, color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until()

    # ------------------------------------------------------------------ four planes, the method
    def clip2(self):
        q = self.q
        self.planes = {p: CH2.argand_plane(center=ctr(p), unit=UNIT, extent=EXT) for p in "abcd"}
        self.cells = {p: [self.planes[p], self.eqs[p]] for p in "abcd"}
        st1 = T("polar form, + 2πn", size=36, t2c={"+ 2πn": TEAL})
        st2 = T("divide the argument", size=36)
        st3 = T("one root for each n", size=36)
        nums = [T(str(k), size=34, color=DIM) for k in (1, 2, 3)]
        self.method = VGroup()
        for k, (num, st) in enumerate(zip(nums, (st1, st2, st3))):
            st.move_to([0, 1.5 - 1.0 * k, 0]).align_to([LX + 0.55, 0, 0], LEFT)
            num.move_to([LX + 0.12, st.get_y(), 0])
            self.method.add(VGroup(num, st))
        unit_tag = MathTex(r"|z| = 1", font_size=52, color=GOLD).move_to([0, -1.9, 0]).align_to([LX, 0, 0], LEFT)
        self.unit_tag = unit_tag
        with self.say("c8.f15.2") as c:
            self.play(*disappear(q.box, q.label, q.icon, q.body[0], q.body[1], lag=0.05), run_time=0.7)
            moves = []
            for p in "abcd":
                eq = self.eqs[p]
                target = eq.copy().scale(34 / 44)
                target.next_to(self.planes[p], UP, buff=0.12).set_x(ctr(p)[0])
                moves.append(eq.animate.scale(34 / 44).move_to(target.get_center()))
            self.play(*during(moves, 0, 0.55), *during([FadeIn(self.planes[p]) for p in "abcd"], 0.6, 1),
                      run_time=min(1.5, c.until("all_unit") - 1.3))
            self.play(*appear(*self.method, lag=0.3), run_time=min(1.2, c.until("all_unit")))  # early: the three steps, listed whole
            c.wait_until("all_unit")
            circles = [self.planes[p].circle for p in "abcd"]
            self.play(*[ci.animate.set_stroke(FG, 3.5, opacity=1) for ci in circles],
                      *[VShowPassingFlash(ci.copy().set_stroke(GOLD, 6), time_width=0.4) for ci in circles],
                      *during(appear(unit_tag), 0.3, 1), run_time=1.6)
            for p in "abcd":
                mark(*self.cells[p])
            c.wait_until("args")
            self.play(FlashAround(st1[-4:], color=TEAL, run_time=1.5, time_width=1.5))
            c.wait_until()

    # ------------------------------------------------------------------ helpers for a part
    def focus(self, p, extra_out=(), run_time=1.0):
        anims = []
        for o in "abcd":
            anims += light(self.cells[o], 1.0 if o == p else DIMMED)
        if extra_out:
            anims += during(disappear(*extra_out), 0, 0.6)
        self.play(*anims, run_time=run_time)

    def add_to(self, p, *mobs):
        mark(*mobs)
        self.cells[p].extend(mobs)

    def rhs(self, c, p, deg, r1):
        dot = Dot(pt(p, deg), radius=0.1, color=YELLOW).set_z_index(3)
        self.play(*appear(r1, shift=None), GrowFromCenter(dot), run_time=1.0)
        return dot

    def roots(self, c, p, degs, cues, rhs_dot=None, nr=None, first_rt=1.0):
        dots = []
        for k, (deg, cue) in enumerate(zip(degs, cues)):
            c.wait_until(cue)
            d = root_dot(p, deg, k)
            anims = [GrowFromCenter(d)]
            if k == 0:
                if rhs_dot is not None:
                    anims.append(FadeOut(rhs_dot))
                if nr is not None:
                    anims += appear(nr, shift=None)
            self.play(*anims, run_time=first_rt if k == 0 else 0.6)
            dots.append(d)
        self.add_to(p, *dots)
        return dots

    def carts(self, c, p, specs, first_extra=()):
        labs = []
        for i, (tex, deg, k, side, cue) in enumerate(specs):
            lab = cart(tex, p, deg, k, side)
            c.wait_until(cue)
            self.play(*appear(lab, shift=0.15 * DOWN), *(first_extra if i == 0 else ()), run_time=0.8)
            labs.append(lab)
        self.add_to(p, *labs)
        return labs

    # ------------------------------------------------------------------ (a)
    def clip3(self):
        p = "a"
        r1 = row(r"-1 = e^{i(\pi + 2\pi n)}", ROWS[0], yellow=(0, 2), teal=(7, 11))
        r2 = row(r"z = e^{i(\pi/3 + 2\pi n/3)}", ROWS[1], teal=(8, 14))
        r3 = nrow([0, 1, 2], ROWS[2])
        with self.say("c8.f15.3") as c:
            self.focus(p, extra_out=[self.method, self.unit_tag])
            dot = self.rhs(c, p, 180, r1)
            c.wait_until("a_div")
            self.play(*appear(r2, shift=0.5 * DOWN), run_time=min(1.5, c.until("a_vals")))
            self.roots(c, p, [60, 180, 300], ["sixty", "a hundred and eighty", "three hundred"],
                       rhs_dot=dot, nr=r3)
            self.carts(c, p, [
                (r"\frac{1}{2} + \frac{\sqrt{3}}{2}i", 60, 0, RIGHT, "a_cart"),
                (r"-1", 180, 1, LEFT, "minus one, and"),
                (r"\frac{1}{2} - \frac{\sqrt{3}}{2}i", 300, 2, RIGHT, "a half minus"),
            ])
            c.wait_until("a_tri")
            tri = outline(p, [60, 180, 300])
            self.play(Create(tri), FlashAround(self.cells[p][3], color=TEAL, run_time=1.0), run_time=1.0)
            self.add_to(p, tri)
            self.work = [r1, r2, r3]
            c.wait_until()

    # ------------------------------------------------------------------ (b) and (c)
    def clip4(self):
        b1 = row(r"1 = e^{2\pi i n}", ROWS[0], yellow=(0, 1), teal=(3, 7))
        b2 = row(r"z = e^{i\pi n/2}", ROWS[1], teal=(3, 8))
        b3 = nrow([0, 1, 2, 3], ROWS[2])
        c1 = row(r"i = e^{i(\pi/2 + 2\pi n)}", ROWS[0], yellow=(0, 1), teal=(8, 12))
        c2 = row(r"z = e^{i(\pi/4 + \pi n)}", ROWS[1], teal=(8, 11))
        c3 = nrow([0, 1], ROWS[2])
        fr = CH1.four_roots(center=ctr("b"), unit=UNIT, labels=True, label_size=30)
        for d in fr.dots:
            d.scale(DR / (d.width / 2))
        for lab in fr.labels:
            set_backstroke(lab, width=5)
        with self.say("c8.f15.4") as c:
            self.focus("b", extra_out=self.work, run_time=0.6)
            self.play(*appear(b1, shift=None), run_time=0.6)
            self.play(*appear(b2, shift=0.5 * DOWN), run_time=1.0)
            c.wait_until("with roots")
            self.play(*appear(b3, shift=None),
                      *[GrowFromCenter(d) for d in fr.dots], run_time=0.9)
            self.play(*appear(*fr.labels, lag=0.4), run_time=min(1.6, c.until("a square")))
            c.wait_until("a square")
            sq = outline("b", [0, 90, 180, 270])
            self.play(Create(sq), run_time=0.6)
            self.add_to("b", *fr.dots, *fr.labels, sq)

            c.wait_until("c")
            self.focus("c", extra_out=[b1, b2, b3], run_time=0.9)
            dot = self.rhs(c, "c", 90, c1)
            c.wait_until("so the roots")
            self.play(*appear(c2, shift=0.5 * DOWN), run_time=min(1.2, c.until("sit at")))
            self.roots(c, "c", [45, 225], ["sit at", "five pi"], rhs_dot=dot, nr=c3, first_rt=0.8)
            diam = outline("c", [45, 225])
            self.carts(c, "c", [
                (r"\frac{1+i}{\sqrt{2}}", 45, 0, RIGHT, "c_cart"),
                (r"-\frac{1+i}{\sqrt{2}}", 225, 1, LEFT, "its negative"),
            ], first_extra=[Create(diam)])
            self.add_to("c", diam)
            self.work = [c1, c2, c3]
            c.wait_until()

    # ------------------------------------------------------------------ (d)
    def clip5(self):
        p = "d"
        r1 = row(r"-i = e^{i(-\pi/2 + 2\pi n)}", ROWS[0], yellow=(0, 2), teal=(10, 14))
        r2 = row(r"z = e^{i(-\pi/6 + 2\pi n/3)}", ROWS[1], teal=(9, 15))
        r3 = nrow([0, 1, 2], ROWS[2])
        with self.say("c8.f15.5") as c:
            self.focus(p, extra_out=self.work)
            dot = self.rhs(c, p, 270, r1)
            c.wait_until("d_div")
            self.play(*appear(r2, shift=0.5 * DOWN), run_time=min(1.5, c.until("minus thirty")))
            self.roots(c, p, [-30, 90, 210], ["minus thirty", "ninety", "two hundred"], rhs_dot=dot, nr=r3,
                       first_rt=0.8)
            self.carts(c, p, [
                (r"\frac{\sqrt{3} - i}{2}", -30, 0, DR, "d_cart"),
                (r"i", 90, 1, LEFT, "then eye"),
                (r"\frac{-\sqrt{3} - i}{2}", 210, 2, DL, "minus root three"),
            ])
            c.wait_until("d_tri")
            tri = outline(p, [-30, 90, 210])
            self.play(Create(tri), FlashAround(self.cells[p][3], color=TEAL, run_time=1.0), run_time=1.0)
            self.add_to(p, tri)
            anims = []
            for o in "abcd":
                anims += light(self.cells[o], 1.0)
            self.play(*anims, *during(disappear(r1, r2, r3), 0, 0.6), run_time=min(1.2, c.until()))
            c.wait_until()
        self.wait(1.5)
