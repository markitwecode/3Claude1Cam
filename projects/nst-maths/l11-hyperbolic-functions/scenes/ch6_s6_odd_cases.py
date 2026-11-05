"""Chapter 6, scene 6: the odd cases (f = 0, missing squares) and the whole family. Clips c6.odd.1 – c6.odd.3.

Opens on s5's bare table, which shrinks to the top-left ("f = 0 ?" GOLD beside it). s2's hyperbola
(shifted right, 0.9 size) shrinks with a GOLD s readout: the YELLOW vertices slide into the centre,
the branches flatten onto the asymptotes, which turn solid TEAL: x^2 - y^2 = 0 => y = +-x. The BLUE
circle shrinks the same way to a YELLOW dot: x^2 + y^2 = 0. The table moves to the top centre and two
cases outside it appear below: the parabola y = x^2 (c = 0) and the parallel lines x^2 = 1. Then the
family grid under the general equation, lit item by item; the lecturer's caption; the end stamp.

Shared (load_scene("ch6_s6_odd_cases")) for the recap:
  collapse_shot()          s2's axes + the asymptotes as solid TEAL lines (s2's framing, centre C)
  crossing_icon(s) point_icon(s) parabola_icon(s) parallel_icon(s)   table-size icons at ORIGIN
                           (s = 1 matches s5's icons; parabola and parallel lines PURPLE)
  FAMILY                   [(name, icon builder)] in the narration's order, ∅ last
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

S5 = load_scene("ch6_s5_classify")
S2 = load_scene("ch6_s2_hyperbola")

PANEL = np.array([3.9, -0.6, 0.0])   # where s2's picture centre goes
PK = 0.9                             # and its scale
LX = -6.4                            # left column edge
EQ1_Y, RD1_Y, EQ2_Y, RD2_Y = 0.55, -0.35, -1.45, -2.35


# ---------------------------------------------------------------- shared builders
def collapse_shot():
    C, H = S2.C, S2.H
    lines = VGroup(Line(C + H * DL, C + H * UR), Line(C + H * UL, C + H * DR)).set_stroke(TEAL, 4)
    g = VGroup(S2.make_axes(), lines)
    g.axes, g.lines = g[0], lines
    return g


def crossing_icon(s=1.0):
    L = 0.54 * s
    lines = VGroup(Line([-L, -L, 0], [L, L, 0]), Line([-L, L, 0], [L, -L, 0])).set_stroke(TEAL, 4)
    return VGroup(S5._axes(s, 1.2, 1.2), lines)


def point_icon(s=1.0):
    return VGroup(S5._axes(s), Dot(ORIGIN, radius=0.08 * s, color=YELLOW))


def parabola_icon(s=1.0):
    curve = ParametricFunction(lambda t: np.array([t * s, 1.25 * t * t * s, 0]), t_range=[-0.6, 0.6, 0.02])
    return VGroup(S5._axes(s, 1.4, 0.9), curve.set_stroke(PURPLE, 4))


def parallel_icon(s=1.0):
    h = 0.42 * s
    lines = VGroup(Line([-0.3 * s, -h, 0], [-0.3 * s, h, 0]),
                   Line([0.3 * s, -h, 0], [0.3 * s, h, 0])).set_stroke(PURPLE, 4)
    return VGroup(S5._axes(s), lines)


FAMILY = [("circle", S5.circle_icon), ("ellipse", S5.ellipse_icon), ("hyperbola", S5.hyperbola_icon),
          ("crossing lines", crossing_icon), ("point", point_icon), ("parabola", parabola_icon),
          ("parallel lines", parallel_icon), ("no solution", S5.empty_icon)]


# ---------------------------------------------------------------- local helpers
def place(m):
    """s2's framing -> this scene's panel."""
    return m.scale(PK, about_point=S2.C).shift(PANEL - S2.C)


def world(x, y):
    return place(VectorizedPoint(S2.to_world(x, y))).get_center()


def left(m, y):
    return m.move_to([LX, y, 0], aligned_edge=LEFT)


def readout(tr, y, places=1):
    lbl = MathTex("s =", font_size=46, color=GOLD)
    num = DecimalNumber(tr.get_value(), num_decimal_places=places, font_size=46, color=GOLD)
    g = VGroup(lbl, num)
    left(lbl, y)
    num.next_to(lbl, RIGHT, buff=0.2)

    def upd(m):
        m.set_value(tr.get_value())
        m.next_to(lbl, RIGHT, buff=0.2)
    num.add_updater(upd)
    return g


class OddCases(NarratedScene):
    def construct(self):
        self.table = S5.handover_shot()
        self.add(self.table)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ f = 0: crossing lines
    def clip1(self):
        t = self.table
        with self.say("c6.odd.1") as c:
            t.generate_target()
            t.target.scale(0.65)
            for r in t.target.rows:          # names back up to label size (30)
                r.name.scale(1.22, about_edge=LEFT)
            t.target.shift([-6.6 - t.target.get_left()[0], 3.7 - t.target.get_top()[1], 0])
            self.play(MoveToTarget(t), run_time=min(1.6, c.until("what if f is zero")))
            c.wait_until("what if f is zero")
            self.fq = MathTex("f = 0\\ ?", font_size=52, color=GOLD).move_to([2.6, 2.75, 0])
            self.play(*appear(self.fq), run_time=1.0)
            c.wait_until("shrink")

            tr = ValueTracker(1.0)
            axes = place(S2.make_axes())
            asym = place(S2.make_asymptotes())
            br = always_redraw(lambda: place(S2.make_branches(max(tr.get_value(), 0.02))))
            vx = always_redraw(lambda: VGroup(*[Dot(world(sg * tr.get_value(), 0), radius=0.08, color=YELLOW)
                                                for sg in (1, -1)]))
            eq = left(MathTex("x^2 - y^2 = s^2", font_size=50), EQ1_Y)
            rd = readout(tr, RD1_Y)
            self.play(FadeIn(axes), FadeIn(asym), FadeIn(br), FadeIn(vx), run_time=1.0)
            self.play(*appear(eq, rd, lag=0.4), run_time=1.0)
            self.play(tr.animate.set_value(0.5), run_time=max(0.5, 0.9 * c.until("collapse")),
                      rate_func=linear)
            c.wait_until("collapse")
            self.play(tr.animate.set_value(0.0), run_time=min(4.2, 0.92 * c.until("lines")),
                      rate_func=smooth)
            c.wait_until("lines")

            solid = collapse_shot()
            place(solid)
            br.clear_updaters()
            vx.clear_updaters()
            rd[1].clear_updaters()
            eq0 = left(MathTex("x^2 - y^2 = 0", font_size=50), EQ1_Y)
            self.play(FadeOut(br), FadeOut(vx), FadeOut(asym), FadeIn(solid.lines),
                      *disappear(rd), run_time=1.4)
            self.play(*edit(eq, eq0), run_time=1.5)
            c.wait_until("two crossing lines")
            pm = left(MathTex(r"\Rightarrow\ y = \pm x", font_size=50), RD1_Y)
            pm[0][-2:].set_color(TEAL)
            self.play(*appear(pm), *[VShowPassingFlash(ln.copy().set_stroke(YELLOW, 8), time_width=0.5)
                                     for ln in solid.lines], run_time=1.5)
        self.axes, self.lines, self.eq0, self.pm = axes, solid.lines, eq0, pm

    # ------------------------------------------------------------ the point; outside the table
    def clip2(self):
        t = self.table
        with self.say("c6.odd.2") as c:
            tr = ValueTracker(3.0)
            circ = always_redraw(lambda: Circle(radius=max(tr.get_value(), 0.01) * S2.H / 4 * PK)
                                 .set_stroke(BLUE, 5).move_to(PANEL))
            eq = left(MathTex("x^2 + y^2 = s^2", font_size=50), EQ2_Y)
            rd = readout(tr, RD2_Y)
            self.play(*disappear(self.lines), *set_alpha([self.eq0, self.pm], 0.5), run_time=1.0)
            self.play(FadeIn(circ), *appear(eq, rd, lag=0.3), run_time=1.2)
            self.play(tr.animate.set_value(0.0), run_time=max(1.0, 0.9 * c.until("equals zero")),
                      rate_func=smooth)
            c.wait_until("equals zero")
            circ.clear_updaters()
            rd[1].clear_updaters()
            eq0 = left(MathTex("x^2 + y^2 = 0", font_size=50), EQ2_Y)
            self.play(*edit(eq, eq0), run_time=1.4)
            c.wait_until("point")
            dot = Dot(PANEL, radius=0.12, color=YELLOW)
            org = left(MathTex("(x, y) = (0, 0)", font_size=46, color=YELLOW), RD2_Y)
            self.remove(circ)
            self.play(GrowFromCenter(dot), *swap(rd, org), run_time=1.3)
            self.play(FlashAround(dot, run_time=1.5, time_width=1.5))
            c.wait_until("outside")

            # the table to the top centre; the board below it clears
            t.generate_target()
            t.target.shift([-t.target.get_x(), 0, 0])
            sweep_clear(self, MoveToTarget(t), keep=[t], run_time=1.8)
            c.wait_until("parabola")

            pa = parabola_icon(2.4).move_to([-3.3, -0.55, 0])
            pa_eq = MathTex("y = x^2", font_size=50).move_to([-3.3, -2.35, 0])
            self.play(*appear(pa, pa_eq, lag=0.4), run_time=1.5)
            c.wait_until("has no why squared term")
            c0 = MathTex("c = 0", font_size=46, color=YELLOW).move_to([-3.3, -3.2, 0])
            self.play(*appear(c0), run_time=1.0)
            c.wait_until("parallel")
            pl = parallel_icon(2.4).move_to([3.3, -0.55, 0])
            pl_eq = MathTex("x^2 = 1", font_size=50).move_to([3.3, -2.35, 0])
            self.play(*appear(pl, pl_eq, lag=0.4), run_time=1.5)
            c.wait_until("two parallel lines")
            pm = MathTex(r"x = \pm 1", font_size=46, color=PURPLE).move_to([3.3, -3.2, 0])
            self.play(*appear(pm), *[FlashAround(ln, run_time=1.5, time_width=1.5, color=PURPLE)
                                     for ln in pl[1]], run_time=1.5)

    # ------------------------------------------------------------ the family
    def clip3(self):
        with self.say("c6.odd.3") as c:
            gen = MathTex("ax^2 + bx + cy^2 + dy + e = 0", font_size=56).move_to([0, 3.15, 0])
            cells = []
            for i, (name, f) in enumerate(FAMILY):
                x = [-5.1, -1.7, 1.7, 5.1][i % 4]
                y = 0.75 if i < 4 else -1.7
                ic = f(1.5).move_to([x, y, 0])
                nm = T(name, size=32).move_to([x, y - 1.05, 0])
                g = VGroup(ic, nm)
                g.icon, g.name = ic, nm
                cells.append(g)
            sweep_clear(self, *appear(gen, *cells, lag=0.12), run_time=2.0)  # early: the whole family shown, then walked
            c.wait_until("one equation")
            cap = T("“One equation, a lot of possibilities.”", size=36, slant=ITALIC).move_to([0, 2.2, 0])
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("list")

            def lbox(g):
                r = RoundedRectangle(corner_radius=0.15, width=3.25, height=2.45)
                r.set_stroke(YELLOW, 2.5).set_fill(YELLOW, 0.1).set_z_index(-1)
                return r.move_to([g.get_x(), g.icon.get_y() - 0.42, 0])
            cues = ["circles", "ellipses", "hyperbolas", "crossing lines", "a point", "a parabola",
                    "parallel lines", "nothing at all"]
            box = lbox(cells[0])
            self.play(FadeIn(box), run_time=0.5)
            for g, cue in zip(cells[1:], cues[1:]):
                c.wait_until(cue)
                self.play(Transform(box, lbox(g)), run_time=0.45)
            c.wait_until("end")
            stamp = T("End of Chapter 3 of the notes", size=30, color=DIM)
            stamp.to_corner(DR, buff=0.4)
            self.play(FadeOut(box), *appear(stamp), run_time=1.0)
