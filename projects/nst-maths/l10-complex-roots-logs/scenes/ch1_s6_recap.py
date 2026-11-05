"""Chapter 1, scene 6: try F15 and F16, recap in four panels, then De Moivre next. Clips c1.recap.1 – c1.recap.4."""
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

POLAR = load_scene("ch1_s2_polar")
UNITY = load_scene("ch1_s3_unity")
METHOD = load_scene("ch1_s4_method")
THEO = load_scene("ch2_s2_theorem")

PLANE_XS = [-5.1, -1.7, 1.7, 5.1]   # F15's four small planes
PLANE_Y = -1.0
PU = 1.0                            # their unit
PEXT = 1.35

LX, RX = -3.5, 3.5                  # recap grid columns
TOP_Y, BOT_Y = 2.1, -1.45           # recap grid rows (picture centres)
RU, REXT = 0.9, 1.25                # recap planes' unit and half-extent
CAP = 30


def _dir(deg):
    a = np.deg2rad(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def small_plane(i):
    return THEO.argand_plane(center=np.array([PLANE_XS[i], PLANE_Y, 0]), unit=PU, extent=PEXT)


def f15_card():
    prose = VGroup(T("F15. Find all solutions of the following equations and indicate", 36),
                   T("their location on the Argand diagram:", 36)).arrange(DOWN, buff=0.22)
    prose.move_to([0, 2.75, 0])
    eqs = VGroup()
    for i, (tag, eq) in enumerate([("(a)", "z^3 = -1"), ("(b)", "z^4 = 1"), ("(c)", "z^2 = i"), ("(d)", "z^3 = -i")]):
        m = MathTex(r"\text{" + tag + r"}\;\;" + eq, font_size=42)
        m.move_to([PLANE_XS[i], 1.05, 0])
        eqs.add(m)
    return prose, eqs


def f16_card():
    lines = [
        [r"F16. Show that the roots of the equation ", r"$z^{2n} - 2bz^n + c = 0$", r" will, for"],
        [r"general complex values of $b$ and $c$ and positive integer values of $n$,"],
        [r"lie on two circles in the Argand diagram. Give a condition on $b$ and $c$"],
        [r"such that the circles coincide. Find the largest value of $|z_1 - z_2|$"],
        [r"when $z_1$ and $z_2$ are roots of $z^6 - 2z^3 + 2 = 0$."],
    ]
    card = VGroup(*[Tex(*ln, font_size=40) for ln in lines]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    card.move_to([0, 2.1, 0])
    return card


def panel_r1():
    c = np.array([LX, TOP_Y, 0])
    plane = POLAR.argand_plane(center=c, unit=RU, extent=REXT)
    z = POLAR.polar_z(center=c, unit=RU)
    cap = T("modulus, argument, + 2πn", CAP, t2c={"+ 2πn": TEAL})
    cap.next_to(VGroup(plane, z), DOWN, buff=0.25).set_x(LX)
    return plane, z, cap


def panel_r2():
    c = np.array([RX, TOP_Y, 0])
    plane = UNITY.argand_plane(center=c, unit=RU, extent=REXT)
    roots = UNITY.four_roots(center=c, unit=RU, labels=True, label_size=34)
    cap = VGroup(MathTex(r"z^4 = 1", font_size=38), T(": four roots", CAP)).arrange(RIGHT, buff=0.06,
                                                                                   aligned_edge=DOWN)
    cap.next_to(plane, DOWN, buff=0.25).set_x(RX)
    return plane, roots, cap


def panel_r3():
    rows = METHOD.condensed_steps(size=36)
    rows.move_to([LX, BOT_Y, 0])
    cap = T("polar form, keep the 2πn, match", CAP, t2c={"2πn": TEAL})
    return rows, cap


def panel_r4():
    c = np.array([RX, BOT_Y, 0])
    plane = METHOD.argand_plane(center=c, unit=RU, extent=REXT)
    k = RU / METHOD.U
    ring = METHOD.ring_circle().scale(k).move_to(c)
    dots = VGroup()
    for j in range(5):
        a = PI / 10 + 2 * PI * j / 5
        dots.add(Dot(c + RU * METHOD.R5 * np.array([np.cos(a), np.sin(a), 0]), radius=0.09,
                     color=GREEN if j == 0 else TEAL).set_z_index(2))
    cap = T("degree 5, five roots", CAP)
    cap.next_to(plane, DOWN, buff=0.25).set_x(RX)
    return plane, ring, dots, cap


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ── F15: four equations like ours ────────────────────────────────────────────────
    def clip1(self):
        prose, eqs = f15_card()
        planes = [small_plane(i) for i in range(4)]
        with self.say("c1.recap.1", gap=3.4) as c:
            c.wait_until("f15")
            self.play(*appear(prose), run_time=1.0)  # early: the exam card is shown whole, then read
            self.play(*appear(*[VGroup(e, p) for e, p in zip(eqs, planes)], lag=0.3),
                      run_time=min(1.8, c.until("use the same")))

            # {args}: −1 has argument π, −i has −π/2
            c.wait_until("args")
            ca = np.array([PLANE_XS[0], PLANE_Y, 0])
            dot_a = Dot(ca + PU * LEFT, radius=0.09, color=FG).set_z_index(2)
            arc_a = Arc(radius=0.4, start_angle=0, angle=PI, arc_center=ca, color=YELLOW, stroke_width=4)
            lab_a = MathTex(r"\pi", font_size=40, color=YELLOW).move_to(ca + np.array([-0.3, 0.66, 0]))
            set_backstroke(lab_a, width=6)
            self.play(FadeIn(dot_a, scale=0.5), Create(arc_a), *appear(lab_a, shift=None), run_time=1.5)

            c.wait_until("minus eye")
            cd = np.array([PLANE_XS[3], PLANE_Y, 0])
            dot_d = Dot(cd + PU * DOWN, radius=0.09, color=FG).set_z_index(2)
            arc_d = Arc(radius=0.4, start_angle=0, angle=-PI / 2, arc_center=cd, color=YELLOW, stroke_width=4)
            lab_d = MathTex(r"-\pi/2", font_size=36, color=YELLOW).move_to(cd + np.array([0.6, -0.72, 0]))
            set_backstroke(lab_d, width=6)
            self.play(FadeIn(dot_d, scale=0.5), Create(arc_d), *appear(lab_d, shift=None),
                      run_time=min(1.5, c.until("keep")))

            # {keep}: + 2πn on each
            c.wait_until("keep")
            keep_a = MathTex(r"+\,2\pi n", font_size=34, color=TEAL).next_to(lab_a, RIGHT, buff=0.08)
            keep_d = MathTex(r"+\,2\pi n", font_size=34, color=TEAL).next_to(lab_d, DOWN, buff=0.15)
            for k in (keep_a, keep_d):
                set_backstroke(k, width=6)
            self.play(*appear(keep_a, keep_d, lag=0.2), run_time=1.2)

            # {b}: (b) is the roots of unity from before
            c.wait_until("b")
            tag = T("roots of unity", 30, color=FG).next_to(planes[1], DOWN, buff=0.3)
            self.play(*appear(tag), FlashUnder(eqs[1], run_time=1.5, time_width=1.5), run_time=1.5)

    # ── F16: a quadratic in disguise ─────────────────────────────────────────────────
    def clip2(self):
        card = f16_card()
        hero = MathTex("z^{2n}", "-", "2b", "z^n", "+", "c", "=", "0", font_size=56).move_to([-3.2, -0.55, 0])
        brace = Brace(hero[3], DOWN, buff=0.12, color=YELLOW)
        wlab = MathTex("w", "=", "z^n", font_size=44, color=YELLOW).next_to(brace, DOWN, buff=0.12)
        quad = MathTex("w^2", "-", "2b", "w", "+", "c", "=", "0", font_size=56).move_to([-3.2, -2.5, 0])
        quad[0].set_color(YELLOW)
        quad[3].set_color(YELLOW)
        rc = np.array([3.0, -1.75, 0])
        inner = DashedVMobject(Circle(radius=0.7, color=GOLD, stroke_width=3).move_to(rc), num_dashes=20)
        outer = DashedVMobject(Circle(radius=1.4, color=GOLD, stroke_width=3).move_to(rc), num_dashes=40)
        lab_out = MathTex(r"|w_2|^{1/n}", font_size=34, color=GOLD).next_to(rc + 1.4 * _dir(30), RIGHT, buff=0.15)
        p_in = rc + 0.7 * _dir(-35)
        lab_in = MathTex(r"|w_1|^{1/n}", font_size=34, color=GOLD).move_to(rc + np.array([2.35, -1.55, 0]))
        lead = Line(p_in, lab_in.get_left() + 0.1 * LEFT, color=GOLD, stroke_width=2).set_opacity(0.7)
        origin = Dot(rc, radius=0.05, color=DIM)
        part8 = T("Full solutions: Part 8", 30, color=DIM).move_to([-3.2, -3.3, 0])

        with self.say("c1.recap.2", gap=4.5) as c:
            sweep_clear(self, run_time=1.0)
            self.play(*appear(*card, lag=0.15), run_time=1.5)  # early: the exam card is shown whole, then read
            c.wait_until("sub")
            self.play(FlashAround(card[0][1], run_time=1.5, time_width=1.5), *appear(hero), run_time=min(1.5, c.until("middle term")))
            c.wait_until("middle term")
            self.play(GrowFromCenter(brace), hero[3].animate.set_color(YELLOW), run_time=0.8)
            self.play(*appear(wlab), run_time=min(1.0, c.until("then the first")))
            c.wait_until("then the first")
            self.play(hero[0].animate.set_color(YELLOW), FlashAround(hero[0], run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("quadratic in w")
            self.play(*appear(quad), run_time=1.2)

            c.wait_until("rings")
            self.play(FadeIn(origin), Create(inner), Create(outer), run_time=1.5)
            self.play(*appear(lab_in, lab_out, lag=0.3), Create(lead), run_time=min(1.2, c.until("two circles")))
            c.wait_until("part8")
            self.play(*appear(part8), run_time=1.0)

    # ── the recap grid ───────────────────────────────────────────────────────────────
    def clip3(self):
        p1, z, cap1 = panel_r1()
        p2, roots, cap2 = panel_r2()
        rows, cap3 = panel_r3()
        p4, ring, dots, cap4 = panel_r4()
        cap3.next_to(rows, DOWN, buff=0.4).set_x(LX).set_y(cap4.get_y())
        with self.say("c1.recap.3", gap=3.6) as c:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # F16 leaves all at once
            c.wait_until("r1")
            self.play(FadeIn(p1), GrowArrow(z.arrow), FadeIn(z.dot), *appear(z.label, z.mod, shift=None),
                      run_time=1.5)
            c.wait_until("argument")
            self.play(Create(z.arc), *appear(z.theta, shift=None), run_time=1.0)
            c.wait_until("whole turns")
            self.play(Create(z.turn), *appear(z.turn_label, shift=None), run_time=1.5)
            self.play(*appear(cap1), run_time=min(1.0, c.until("r2")))

            c.wait_until("r2")
            self.play(FadeIn(p2), *appear(*roots.dots, lag=0.2, shift=None), run_time=1.3)
            self.play(*appear(*roots.labels, lag=0.1, shift=None), *appear(cap2),
                      run_time=min(1.2, c.until("r3")))

            c.wait_until("r3")
            c.wait_until("polar form")
            self.play(*appear(rows[0], rows[1], lag=0.5), run_time=1.8)
            c.wait_until("keep the two pi n")
            self.play(FlashAround(rows[1][1][0][10:14], color=TEAL, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("match lengths")
            self.play(*appear(rows[2]), run_time=1.2)
            self.play(*appear(cap3), run_time=min(1.0, c.until("r4")))

            c.wait_until("r4")
            self.play(FadeIn(p4), Create(ring), run_time=1.3)
            self.play(*appear(*dots, lag=0.2, shift=None), run_time=1.2)
            c.wait_until("degree five")
            self.play(*appear(cap4), run_time=1.0)

        self.grid = VGroup(p1, z, cap1, p2, roots, cap2, rows, cap3, p4, ring, dots, cap4)
        settle(self, self.grid)

    # ── next time: De Moivre ─────────────────────────────────────────────────────────
    def clip4(self):
        c0 = np.array([-3.2, -0.1, 0])
        plane = THEO.argand_plane(center=c0, unit=1.8, extent=2.6)
        steps = THEO.power_steps(n=4, center=c0, unit=1.8, dim=0.4)
        for a in steps.arrows:
            a.set_opacity(1)
        tip = steps.arrows[0].get_end()
        elab = MathTex(r"e^{i\theta}", font_size=40, color=GOLD).next_to(tip, RIGHT, buff=0.12)
        formula = MathTex(r"(\cos\theta + i\sin\theta)^n", font_size=56).move_to([3.3, 0.5, 0])
        part = T("Part 2 · De Moivre's theorem", 32, color=DIM).move_to([3.3, -0.7, 0])

        with self.say("c1.recap.4") as c:
            self.play(*set_alpha([self.grid], DIMMED), run_time=0.8)
            sweep_clear(self, FadeIn(plane), run_time=1.0)
            self.play(GrowArrow(steps.arrows[0]), Create(steps.arcs[0]),
                      *appear(steps.label, elab, shift=None), run_time=min(1.2, c.until("power")))
            for k in range(1, 4):
                self.play(GrowArrow(steps.arrows[k]), Create(steps.arcs[k]),
                          steps.arrows[k - 1].animate.set_opacity(0.4), run_time=0.9 if k == 1 else 0.6)
            c.wait_until("dm")
            self.play(*appear(formula, part, lag=0.5), run_time=1.5)

