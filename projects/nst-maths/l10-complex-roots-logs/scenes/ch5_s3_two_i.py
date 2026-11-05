"""Chapter 5, scene 3: 2^i, the principal value on the unit circle, then the whole ray of values. Clips c5.two.1 – c5.two.4.

Shared: `two_i_ray(...)` (module level) draws the log-scale strip of the values of 2^i laid along
the ray at angle ln 2 (TEAL dots, GREEN n = 0). s4 (horizontal, i^i), s7 and s8 reuse it.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

LN2 = float(np.log(2))
U = 1.85                         # screen units per plane unit
O = np.array([2.0, -1.3, 0])     # plane origin on screen


def P(x, y):
    return O + U * np.array([x, y, 0])


def argand_plane(xr=(-0.9, 2.1), yr=(-0.9, 2.4)):
    """Re/Im axes, faint grid, DIM unit circle (same construction as ch2_s1_hook.argand_plane)."""
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(P(x, yr[0]), P(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(P(xr[0], y), P(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0), P(xr[1], 0) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0]), P(0, yr[1]) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    re = T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    unit = Circle(radius=U, color=DIM, stroke_width=2).move_to(O)
    return VGroup(grid, xax, yax, re, im, unit)


def two_i_ray(step=1.45, angle=LN2, center=ORIGIN, n_max=2, size=32, tick_tex=None, n_tex=None,
              dot_r=0.11, with_many=True):
    """The values of 2^i on a log-scale strip along the ray at `angle` (radians from +x).

    One equal step per factor e^{2pi}; the n = 0 value (modulus 1) sits at `center`, n > 0 inward
    (towards -direction), n < 0 outward. Ticks labelled on the clockwise side, n labels on the other.
    `tick_tex` / `n_tex`: lists of TeX strings ordered n = n_max ... -n_max (default: e^{-2pi n}, n = ...).
    `angle=0` gives a horizontal strip (outward = right). Returns a VGroup with attributes
    .line .ticks .tick_labels .dots .n_labels .many (VGroup of the two ellipses; empty if not with_many)
    and .ns (the n of each dot / tick, same order); .dot_of(n) → that dot.
    """
    d = np.array([np.cos(angle), np.sin(angle), 0.0])
    nrm = np.array([-np.sin(angle), np.cos(angle), 0.0])
    ns = list(range(n_max, -n_max - 1, -1))
    if tick_tex is None:
        tick_tex = []
        for n in ns:
            if n == 0:
                tick_tex.append("1")
            elif n == 1:
                tick_tex.append(r"e^{-2\pi}")
            elif n == -1:
                tick_tex.append(r"e^{2\pi}")
            else:
                tick_tex.append(rf"e^{{{-2 * n}\pi}}")
    if n_tex is None:
        n_tex = [rf"n={n}" for n in ns]

    def pos(n):
        return np.array(center) - n * step * d

    half = (n_max + 0.6) * step
    line = Line(np.array(center) - half * d, np.array(center) + half * d, color=GOLD, stroke_width=4)
    ticks, tlabs, dots, nlabs = VGroup(), VGroup(), VGroup(), VGroup()
    for n, tt, nt in zip(ns, tick_tex, n_tex):
        p = pos(n)
        ticks.add(Line(p - 0.17 * nrm, p + 0.17 * nrm, color=GOLD, stroke_width=3))
        tl = MathTex(tt, font_size=size, color=GOLD)
        tl.move_to(p - nrm * (0.3 + 0.5 * (abs(nrm[0]) * tl.width + abs(nrm[1]) * tl.height)))
        tlabs.add(tl)
        dots.add(Dot(p, radius=dot_r, color=GREEN if n == 0 else TEAL))
        nl = MathTex(nt, font_size=size, color=GREEN if n == 0 else TEAL)
        nl.move_to(p + nrm * (0.3 + 0.5 * (abs(nrm[0]) * nl.width + abs(nrm[1]) * nl.height)))
        nlabs.add(nl)
    many = VGroup()
    if with_many:
        for sgn in (-1, 1):
            many.add(VGroup(*[Dot(np.array(center) + sgn * (n_max + 0.8 + 0.18 * k) * step * d,
                                  radius=0.045, color=DIM) for k in range(3)]))
    g = VGroup(line, ticks, tlabs, dots, nlabs, many)
    g.line, g.ticks, g.tick_labels, g.dots, g.n_labels, g.many, g.ns = line, ticks, tlabs, dots, nlabs, many, ns
    g.dot_of = lambda n: dots[ns.index(n)]
    return g


def mt(*parts, size=48, color=FG):
    return MathTex(*parts, font_size=size, color=color)


class TwoToTheI(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c5.two.1
    def clip1(self):
        with self.say("c5.two.1") as c:
            self.heading = T("Example 31: Complex logarithms", size=46).move_to(UP * 3.25)
            task = MathTex(r"\text{Use complex logarithms to evaluate }", r"2^{i}", r"\text{ and }", r"i^{i}",
                           r"\text{ in the form }", r"x+iy", r"\text{.}", font_size=38)
            task[1][1].set_color(PINK)
            task[3].set_color(PINK)
            task[5][2].set_color(PINK)
            task.move_to(UP * 2.3)
            self.task = task
            self.play(*appear(self.heading), run_time=1.0)  # early: heading of the worked example
            self.play(*appear(task), run_time=1.2)  # early: the task, read as it is spoken
            c.wait_until("def")

            r1 = mt("z", "=", r"2^{i}", size=52)
            r1[2][1].set_color(PINK)
            r2 = mt(r"\Rightarrow", r"\ln z", "=", r"\ln 2^{i}", "=", r"i\ln 2", size=52)
            r2[3][3].set_color(PINK)
            r2[5][0].set_color(PINK)
            r3 = mt(r"\Rightarrow", "z", "=", r"e^{i\ln 2}", size=52)
            r3[3][1].set_color(PINK)
            r4 = mt("=", r"\cos(\ln 2)", "+", r"i\sin(\ln 2)", size=52)
            r4[1].set_color(BLUE)
            r4[3].set_color(PINK)
            route = VGroup(r1, r2, r3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
            r4.next_to(r3, DOWN, buff=0.55)
            r4.shift((r3[2].get_x() - r4[0].get_x()) * RIGHT)
            route.add(r4)
            route.move_to(DOWN * 0.75 + LEFT * 0.9)
            self.r = (r1, r2, r3, r4)
            self.route = route
            self.play(*appear(r1), run_time=1.0)
            c.wait_until("two to the power eye is")
            self.play(*appear(r2), run_time=min(1.2, c.until("quick")))
            c.wait_until("quick")

            tag = T("(principal value)", size=36, color=GREEN).next_to(r2, RIGHT, buff=0.4)
            self.ptag = tag
            self.play(FlashUnder(r2[5], color=GREEN, run_time=1.4, time_width=1.5), *appear(tag), run_time=1.4)
            c.wait_until("euler")
            self.play(*appear(r3), run_time=1.0)
            c.wait_until("cosine of log two")
            self.play(*appear(r4), run_time=1.2)

    # ------------------------------------------------------------------ c5.two.2
    def clip2(self):
        r1, r2, r3, r4 = self.r
        with self.say("c5.two.2") as c:
            plane = argand_plane()
            self.plane = plane
            left_block = VGroup(self.route, self.ptag)
            self.play(*during(disappear(self.task), 0, 0.4),
                      *during([self.heading.animate.scale(0.85).to_edge(LEFT, buff=0.5),
                              left_block.animate.scale(0.82).to_edge(LEFT, buff=0.5).align_to(UP * 2.35, UP)],
                             0.2, 0.75),
                      *during([FadeIn(plane)], 0.5, 1), run_time=min(2.0, c.until("circle")))
            c.wait_until("circle")

            arrow = Arrow(O, P(1, 0), buff=0, color=GOLD, stroke_width=6, max_tip_length_to_length_ratio=0.15)
            self.arrow = arrow
            self.play(*flash([plane[5]], color=DIM, run_time=1.4), GrowArrow(arrow), run_time=1.4)
            c.wait_until("angle")

            arc = Arc(radius=0.62, start_angle=0, angle=LN2, arc_center=O, color=YELLOW, stroke_width=4)
            self.arc = arc
            self.play(Rotate(arrow, angle=LN2, about_point=O), Create(arc), run_time=1.6)
            alab = mt(r"\ln 2\approx 0.69\ \text{rad}\approx 40^\circ", size=34, color=YELLOW)
            alab.next_to(O, DOWN, buff=0.3).align_to(O + 0.15 * RIGHT, LEFT)
            set_backstroke(alab, width=8)
            self.alab = alab
            self.play(*appear(alab), run_time=1.0)
            c.wait_until("numbers")

            dot = Dot(P(np.cos(LN2), np.sin(LN2)), radius=0.12, color=GREEN)
            dlab = mt(r"0.769+0.639\,i", size=36)
            dlab[0][-1].set_color(PINK)
            dlab.move_to(dot.get_center() + np.array([0.0, -0.22, 0]), aligned_edge=LEFT).set_x(4.0, LEFT)
            set_backstroke(dlab, width=8)
            self.dot, self.dlab = dot, dlab
            self.play(GrowFromCenter(dot), run_time=0.8)
            self.play(*appear(dlab), run_time=1.0)
            c.wait_until("tag")

            ptag2 = T("principal value", size=30, color=GREEN).next_to(dlab, DOWN, buff=0.22, aligned_edge=LEFT)
            set_backstroke(ptag2, width=8)
            self.ptag2 = ptag2
            self.play(*appear(ptag2), *flash([dot], color=GREEN, run_time=1.2), run_time=1.2)

    # ------------------------------------------------------------------ c5.two.3
    def clip3(self):
        r1, r2, r3, r4 = self.r
        with self.say("c5.two.3") as c:
            left_block = VGroup(self.route, self.ptag)
            self.play(*during(disappear(self.ptag), 0, 0.4),
                      *during([self.route.animate.scale(0.62 / 0.82).to_edge(LEFT, buff=0.5)
                               .align_to(UP * 2.55, UP).set_opacity(0.45)], 0.25, 1), run_time=1.4)
            c.wait_until("ladder")

            ladder = mt(r"\ln 2", r"\;\to\;", r"\ln 2", "+", r"2\pi i n", r",\quad n\in\mathbb{Z}")
            ladder[4].set_color(TEAL)
            ladder[4][2].set_color(PINK)
            ladder.to_edge(LEFT, buff=0.5).set_y(-0.45)
            self.play(*appear(ladder), run_time=1.2)
            c.wait_until("two pi eye times n")
            self.play(*flash([ladder[4]], color=TEAL, run_time=1.4), run_time=1.4)
            c.wait_until("sub")

            p1 = mt(r"2^{i}", "=", r"e^{i(", r"\ln 2", "+", r"2\pi i n", r")}")
            p1[0][1].set_color(PINK)
            p1[2][1].set_color(PINK)
            p1[5].set_color(TEAL)
            p1[5][2].set_color(PINK)
            p1.to_edge(LEFT, buff=0.5).set_y(-0.45)
            self.play(*edit(ladder, p1), run_time=min(1.8, c.until("square")))
            c.wait_until("square")

            self.play(*flash([p1[2][1], p1[5][2]], color=PINK, run_time=1.4), run_time=1.4)
            note = mt(r"i\cdot 2\pi i n=-2\pi n", size=38)
            note[0][0].set_color(PINK)
            note[0][4].set_color(PINK)
            note[0][-4:].set_color(GOLD)
            note.next_to(p1, RIGHT, buff=0.45)
            self.note = note
            self.play(*appear(note), run_time=1.0)
            c.wait_until("result")

            p2 = mt("=", r"e^{-2\pi n}", r"\,e^{i\ln 2}")
            p2[1].set_color(GOLD)
            p2[2][1].set_color(PINK)
            p2.next_to(p1, DOWN, buff=0.6)
            p2.shift((p1[1].get_x() - p2[0].get_x()) * RIGHT)
            self.play(*appear(p2), run_time=1.4)
            p3 = mt("=", r"e^{-2\pi n}", r"(\cos\ln 2", "+", r"i\sin\ln 2)")
            p3[1].set_color(GOLD)
            p3[2][1:].set_color(BLUE)
            p3[4][:-1].set_color(PINK)
            p3.next_to(p2, DOWN, buff=0.6)
            p3.shift((p1[1].get_x() - p3[0].get_x()) * RIGHT)
            self.p = (p1, p2, p3)
            c.wait_until("times E to the eye log two")
            self.play(*appear(p3), run_time=min(1.4, max(1.0, c.remaining - 0.1)))

    # ------------------------------------------------------------------ c5.two.4
    def clip4(self):
        p1, p2, p3 = self.p
        with self.say("c5.two.4", gap=3.3) as c:
            n0 = mt(r"n=0", size=36, color=GREEN)
            n0.move_to(self.dot.get_center() + np.array([-0.9, 0.12, 0]))
            set_backstroke(n0, width=8)
            self.play(*disappear(self.note), run_time=0.8)
            self.play(*appear(n0), *flash([self.dot], color=GREEN, run_time=1.2), run_time=1.2)
            c.wait_until("modulus")

            end = O + 6.0 * np.array([np.cos(LN2), np.sin(LN2), 0])
            ray = Arrow(O, end, buff=0, color=GOLD, stroke_width=6, max_tip_length_to_length_ratio=0.04)
            self.play(ReplacementTransform(self.arrow, ray), run_time=1.8)
            self.add(self.dot)
            c.wait_until("n1")

            d1 = Dot(O + U * np.exp(-2 * PI) * np.array([np.cos(LN2), np.sin(LN2), 0]), radius=0.1, color=TEAL)
            # outside the unit circle, left of it, with a leader line in to the dot at the origin
            l1 = VGroup(mt(r"n=1", size=34, color=TEAL),
                        mt(r"e^{-2\pi}\approx 0.0019", size=34, color=TEAL)).arrange(DOWN, buff=0.15)
            l1.move_to(np.array([-0.15, -0.75, 0]), aligned_edge=RIGHT)
            set_backstroke(l1, width=8)
            a1 = Arrow(l1.get_right() + 0.1 * RIGHT, O + 0.06 * LEFT, buff=0.05,
                       color=TEAL, stroke_width=3, max_tip_length_to_length_ratio=0.12)
            self.play(GrowFromCenter(d1), *appear(l1), GrowArrow(a1), run_time=1.4)
            c.wait_until("nm1")

            lm = mt(r"n=-1:\ e^{2\pi}\approx 535", size=34, color=TEAL)
            lm.move_to(np.array([4.55, 3.4, 0]))
            set_backstroke(lm, width=8)
            am = Arrow(lm.get_corner(DR) + 0.1 * DOWN, end + 0.2 * UR, buff=0.05,
                       color=TEAL, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            self.play(*appear(lm), GrowArrow(am), run_time=1.4)
            c.wait_until("ray")

            self.play(VShowPassingFlash(Line(O, end, color=YELLOW, stroke_width=8), time_width=0.5),
                      *flash([self.arc], color=YELLOW, run_time=1.6), run_time=1.6)
            c.wait_until("strip")

            strip = two_i_ray(step=1.6, center=np.array([0.9, -0.25, 0]), size=36)
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45),
                      *during([Create(strip.line), *[FadeIn(t) for t in strip.ticks]], 0.45, 0.8),
                      run_time=1.6)
            self.play(*[GrowFromCenter(d) for d in strip.dots],
                      *appear(*strip.tick_labels, lag=0.1), run_time=1.4)
            self.play(*appear(*strip.n_labels, lag=0.1), run_time=1.2)
            c.wait_until("many")

            many = T("infinitely many values", size=44).to_corner(UL, buff=0.6).shift(0.3 * RIGHT)
            self.play(*[FadeIn(e, shift=0.15 * (e.get_center() - strip.line.get_center()) /
                               np.linalg.norm(e.get_center() - strip.line.get_center()))
                        for e in strip.many],
                      *appear(many), run_time=1.2)
