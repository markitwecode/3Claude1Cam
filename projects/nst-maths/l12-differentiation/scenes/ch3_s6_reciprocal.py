"""Chapter 3, scene 6: the reciprocal rule (111). Clips c3.recip.1 – c3.recip.4.

Exports:

picture(mirror=False, ax=None, chord=True) -> VGroup
    Figure 29 (ch1's styling: BLUE y = x^3 for x in [0, 1.52], YELLOW point (1, 1) and Q at
    x = 1.45, DIM dashed right-angle legs, TEAL braces/labels, TEAL chord, GREEN tangent of slope 3)
    on equal-unit axes (0..3.7 both ways, 1.6 screen units per unit, origin at FIG_O = (-4.6, -3.3)).
    mirror=True draws its reflection in y = x (the cube root; braces swap: δx upright, δy flat).
    Parts: .axes .xlab .ylab .curve .chord (None if chord=False) .tangent .run_leg .rise_leg
    .right_angle .run_brace .run_lab (δx) .rise_brace .rise_lab (δy) .p_dot .q_dot.
    In mirror mode .xlab "x" sits at the vertical axis' top and .ylab "y" at the horizontal axis' end
    (the labels trade places with the reflection).

swapped_pair() -> VGroup (for the recap), same fixed place as above, ~10.4 x 6.3:
    .axes .xlab "x" .ylab "y" .diag (DIM dashed y = x) .diag_lab ("y = x", DIM 32)
    .orig  (picture(mirror=False, chord=False), its axes/labels removed)
    .mirror (picture(mirror=True, chord=False), likewise)
    .r3  MathTex "\\text{slope } 3" (3 GOLD), .r13 "\\text{slope } \\tfrac13" (1/3 GOLD), at the right.
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

U = 1.6
FIG_O = np.array([-4.6, -3.3, 0.0])
RNG = 3.7
DX = 0.45
DIAG_AXIS = np.array([1.0, 1.0, 0.0]) / np.sqrt(2)
RD1 = np.array([4.4, 0.7, 0.0])
RD2 = np.array([4.4, -0.75, 0.0])


def tx(s, size=44, color=FG, iso=(), colors=None):
    """MathTex with isolated substrings coloured."""
    parts = s if isinstance(s, (list, tuple)) else [s]
    m = MathTex(*parts, font_size=size, color=color, substrings_to_isolate=list(iso) or None)
    for k, c in (colors or {}).items():
        m.set_color_by_tex(k, c)
    return m


DELTA = dict(iso=[r"\delta x", r"\delta y"], colors={r"\delta x": TEAL, r"\delta y": TEAL})


def fig_axes(origin=FIG_O, u=U, lo=0.0, hi=RNG):
    ax = Axes(x_range=[lo, hi, 10], y_range=[lo, hi, 10], x_length=(hi - lo) * u,
              y_length=(hi - lo) * u, tips=True,
              axis_config={"color": DIM, "include_ticks": False, "stroke_width": 3})
    ax.shift(origin - ax.c2p(0, 0))
    return ax


def picture(mirror=False, ax=None, chord=True):
    ax = ax or fig_axes()

    def P(x, y):
        return ax.c2p(y, x) if mirror else ax.c2p(x, y)

    g = VGroup()
    g.axes = ax
    x1 = 1.0 + DX
    y1 = x1 ** 3
    m = (y1 - 1.0) / DX
    g.curve = ParametricFunction(lambda t: P(t, t ** 3), t_range=[0, 1.52], color=BLUE, stroke_width=5)
    g.chord = None
    if chord:
        g.chord = Line(P(0.86, 1 - 0.14 * m), P(1.57, 1 + 0.57 * m), color=TEAL, stroke_width=4)
    g.tangent = Line(P(0.75, 0.25), P(1.87, 3.61), color=GREEN, stroke_width=4)
    p, c, q = P(1, 1), P(x1, 1), P(x1, y1)
    g.run_leg = DashedLine(p, c, color=DIM, dash_length=0.1, stroke_width=3)
    g.rise_leg = DashedLine(c, q, color=DIM, dash_length=0.1, stroke_width=3)
    a = (p - c) / np.linalg.norm(p - c)
    b = (q - c) / np.linalg.norm(q - c)
    s = 0.18
    g.right_angle = VMobject(color=DIM, stroke_width=2).set_points_as_corners(
        [c + s * a, c + s * a + s * b, c + s * b])
    rd, sd = (LEFT, UP) if mirror else (DOWN, RIGHT)
    g.run_brace = Brace(Line(p, c), rd, buff=0.1, color=TEAL)
    g.run_lab = tx(r"\delta x", 40, TEAL).next_to(g.run_brace, rd, buff=0.1)
    g.rise_brace = Brace(Line(c, q), sd, buff=0.1, color=TEAL)
    g.rise_lab = tx(r"\delta y", 40, TEAL).next_to(g.rise_brace, sd, buff=0.1)
    g.p_dot = Dot(p, radius=0.09, color=YELLOW)
    g.q_dot = Dot(q, radius=0.09, color=YELLOW)
    xend, yend = ax.x_axis.get_end(), ax.y_axis.get_end()
    g.xlab = MathTex("x", font_size=40)
    g.ylab = MathTex("y", font_size=40)
    if mirror:
        g.xlab.next_to(yend, UP, buff=0.12)
        g.ylab.next_to(xend, RIGHT, buff=0.15)
    else:
        g.xlab.next_to(xend, RIGHT, buff=0.15)
        g.ylab.next_to(yend, UP, buff=0.12)
    for k in ("axes", "xlab", "ylab", "run_leg", "rise_leg", "right_angle", "run_brace", "run_lab",
              "rise_brace", "rise_lab", "curve", "chord", "tangent", "p_dot", "q_dot"):
        if getattr(g, k) is not None:
            g.add(getattr(g, k))
    return g


def geometry(pic):
    """The parts that reflect (axes and text labels excluded)."""
    return [m for m in (pic.run_leg, pic.rise_leg, pic.right_angle, pic.run_brace, pic.rise_brace,
                        pic.curve, pic.chord, pic.tangent, pic.p_dot, pic.q_dot) if m is not None]


def diag_line(ax, hi=3.5):
    return DashedLine(ax.c2p(0, 0), ax.c2p(hi, hi), color=DIM, dash_length=0.12, stroke_width=3)


def readout(num):
    r = tx([r"\text{slope }", num], 44)
    r[1].set_color(GOLD)
    return r


def swapped_pair():
    ax = fig_axes()
    g = VGroup()
    g.axes = ax
    g.orig = picture(False, ax, chord=False)
    g.mirror = picture(True, ax, chord=False)
    g.xlab, g.ylab = g.orig.xlab, g.orig.ylab
    for pic in (g.orig, g.mirror):
        pic.remove(pic.axes, pic.xlab, pic.ylab)
    g.mirror.remove(g.mirror.p_dot)
    g.diag = diag_line(ax)
    g.diag_lab = MathTex("y = x", font_size=32, color=DIM).next_to(g.diag.get_end(), RIGHT, buff=0.15)
    g.r3 = readout("3").move_to(RD1, aligned_edge=LEFT)
    g.r13 = readout(r"\tfrac13").move_to(RD2, aligned_edge=LEFT)
    g.add(ax, g.diag, g.diag_lab, g.xlab, g.ylab, g.orig, g.mirror, g.r3, g.r13)
    return g


# ---- scene 5's triangle and answer box (stand-ins until ch3_s5_sign defines them) ----

def _standin_triangle():
    w, h = 2.6, 1.9
    A, B, C = np.array([-w / 2, -h / 2, 0]), np.array([w / 2, -h / 2, 0]), np.array([w / 2, h / 2, 0])
    g = VGroup()
    g.tri = Polygon(A, B, C, color=BLUE, stroke_width=4)
    s = 0.22
    g.right_angle = VMobject(color=DIM, stroke_width=2).set_points_as_corners(
        [B + s * LEFT, B + s * LEFT + s * UP, B + s * UP])
    g.one = MathTex("1", font_size=40).next_to(Line(A, B), DOWN, buff=0.15)
    g.x = MathTex("x", font_size=40).next_to(Line(B, C), RIGHT, buff=0.15)
    hyp_dir = (C - A) / np.linalg.norm(C - A)
    nrm = np.array([-hyp_dir[1], hyp_dir[0], 0])
    g.hyp = MathTex(r"\sqrt{1 + x^2}", font_size=40).move_to((A + C) / 2 + 0.55 * nrm)
    ang = np.arctan2(h, w)
    g.arc = Arc(radius=0.6, start_angle=0, angle=ang, arc_center=A, color=YELLOW, stroke_width=3)
    g.y = MathTex("y", font_size=40, color=YELLOW).move_to(A + 0.85 * np.array([np.cos(ang / 2), np.sin(ang / 2), 0]))
    g.add(g.tri, g.right_angle, g.one, g.x, g.hyp, g.arc, g.y)
    return g


def _standin_answer_box():
    f = tx([r"\dfrac{dy}{dx}", "=", r"\dfrac{1}{1 + x^2}"], 44)
    f[0].set_color(GREEN)
    rect = SurroundingRectangle(f, color=YELLOW, buff=0.3, stroke_width=3)
    g = VGroup(rect, f)
    g.rect, g.formula = rect, f
    return g


def s5_parts():
    try:
        mod = load_scene("ch3_s5_sign")
        if hasattr(mod, "triangle") and hasattr(mod, "answer_box"):
            return mod.triangle(), mod.answer_box()
    except Exception:
        pass
    return _standin_triangle(), _standin_answer_box()


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def turn(mob, about, angle, c0, c1):
    """Rotate a line by `angle` about a point while its colour goes c0 -> c1."""
    base = mob.copy()

    def upd(m, a):
        m.become(base.copy().rotate(a * angle, about_point=about).set_color(interpolate_color(ManimColor(c0), ManimColor(c1), a)))
    return UpdateFromAlphaFunc(mob, upd)


class Reciprocal(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c3.recip.1
    def clip1(self):
        eq = tx([r"\dfrac{dx}{dy}", "=", r"\dfrac{1}{dy/dx}"], 60, iso=["dy/dx"],
                colors={"dy/dx": GREEN})
        tag = T("(111)", 36, DIM).next_to(eq, RIGHT, buff=0.6)
        eqg = VGroup(eq, tag).move_to(ORIGIN)
        self.eqg, self.eq = eqg, eq
        with self.say("c3.recip.1") as c:
            self.play(*appear(eqg), run_time=1.2)  # early: the rule is the topic sentence's subject
            c.wait_until("one over")
            self.play(FlashAround(eq, time_width=1.5), run_time=min(2, c.until("pic")))
            c.wait_until("pic")
            ax = fig_axes()
            pic = picture(False, ax)
            self.play(eqg.animate.scale(0.75).move_to(2.95 * UP),
                      FadeIn(ax), *appear(pic.xlab, pic.ylab, lag=0.1),  # early: axis labels come with the axes
                      run_time=min(1.5, c.until("a curve")))
            self.play(Create(pic.curve), run_time=min(1.2, c.until("a chord")))
            c.wait_until("a chord")
            self.play(Create(pic.chord), FadeIn(pic.run_leg, pic.rise_leg, pic.right_angle),
                      GrowFromCenter(pic.run_brace), GrowFromCenter(pic.rise_brace),
                      FadeIn(pic.p_dot, pic.q_dot), *appear(pic.run_lab, pic.rise_lab),
                      run_time=min(1.4, c.until("the tangent line")))
            c.wait_until("the tangent line")
            r3 = readout("3").move_to(RD1, aligned_edge=LEFT)
            self.play(Create(pic.tangent), run_time=1.0)
            self.play(*appear(r3), run_time=min(1.0, c.until("swap")))  # early: the tangent's slope readout
            c.wait_until("swap")
            diag = diag_line(ax)
            dlab = MathTex("y = x", font_size=32, color=DIM).next_to(diag.get_end(), RIGHT, buff=0.15)
            self.play(Create(diag), *appear(dlab),  # early: the line is named in this sentence
                      *disappear(pic.run_lab, pic.rise_lab), run_time=min(1.3, c.until("by reflecting")))
            c.wait_until("by reflecting")
            mir = picture(True, ax)
            flips = [Rotate(m, angle=PI, axis=DIAG_AXIS, about_point=ax.c2p(0, 0)) for m in geometry(pic)]
            self.play(*flips, *during(disappear(pic.xlab, pic.ylab), 0, 0.4),
                      *during(appear(mir.xlab, mir.ylab, shift=None), 0.6, 1),
                      run_time=min(2.5, c.until("triangle") - 0.15))
            self.remove(*geometry(pic))
            self.add(*geometry(mir))
            c.wait_until("triangle")
            self.play(*appear(mir.rise_lab), FlashAround(mir.rise_brace, time_width=1.5),
                      run_time=min(1.2, c.until("and the run becomes")))
            c.wait_until("and the run becomes")
            self.play(*appear(mir.run_lab), FlashAround(mir.run_brace, time_width=1.5),
                      run_time=min(1.2, c.until("over")))
            c.wait_until("over")
            r13 = readout(r"\tfrac13").move_to(RD2, aligned_edge=LEFT)
            self.play(*appear(r13), FlashAround(mir.tangent, time_width=1.5),
                      run_time=min(1.4, c.until("a slope of three")))
            c.wait_until("a slope of three")
            self.play(*during(FlashAround(r3, time_width=1.5), 0, 0.5),
                      *during(FlashAround(r13, time_width=1.5), 0.5, 1), run_time=min(2.2, c.until() - 0.1))
        mpic = VGroup(ax, diag, *geometry(mir))
        settle(self, mpic)
        self.labs = [dlab, mir.xlab, mir.ylab, mir.run_lab, mir.rise_lab]
        self.mpic, self.mir, self.r3, self.r13 = mpic, mir, r3, r13

    # ------------------------------------------------------------------ c3.recip.2
    def clip2(self):
        L1a = tx([r"\dfrac{dx}{dy}", "=", r"\lim_{\delta y \to 0}", r"\dfrac{\delta x}{\delta y}"], 42, **DELTA)
        L1b = tx(["=", r"\lim_{\delta y \to 0}", r"\left(\dfrac{\delta y}{\delta x}\right)^{-1}"], 42, **DELTA)
        L1b.next_to(L1a, RIGHT, buff=0.22)
        L1b.shift((L1a[1].get_y() - L1b[0].get_y()) * UP)
        VGroup(L1a, L1b).move_to(1.6 * UP)
        eqx = L1b[0].get_x()

        def row(m, y):
            m.shift(np.array([eqx - m[0].get_x(), y - m[0].get_y(), 0]))
            return m
        L2 = row(tx(["=", r"\lim_{\delta x \to 0}", r"\left(\dfrac{\delta y}{\delta x}\right)^{-1}"], 42, **DELTA), 0.1)
        L3 = row(tx(["=", r"\left(\lim_{\delta x \to 0}", r"\dfrac{\delta y}{\delta x}", r"\right)^{-1}"], 42, **DELTA), -1.4)
        L4 = row(tx(["=", r"\dfrac{1}{dy/dx}"], 42, iso=["dy/dx"], colors={"dy/dx": GREEN}), -2.9)
        aside = T("dx and dy are not numbers (part one)", 28, DIM).move_to(2.05 * UP)
        self.L4 = L4
        with self.say("c3.recip.2") as c:
            self.play(*during(self.mpic.animate.scale(0.42).move_to(np.array([-5.15, -2.15, 0])), 0.35, 1),
                      *during(disappear(self.r3, self.r13, *self.labs), 0, 0.35), run_time=min(1.5, c.until("but")))
            c.wait_until("but")
            self.play(*appear(aside), run_time=1.0)
            c.wait_until("finite")
            self.play(*during(disappear(aside), 0, 0.45), *during(appear(L1a), 0.5, 1), run_time=1.6)
            c.wait_until("power")
            self.play(*appear(L1b), run_time=1.2)
            c.wait_until("tied")
            self.play(FlashUnder(L1b[1], time_width=1.5, color=TEAL), run_time=1.5)
            c.wait_until("tied together")
            self.play(FlashAround(self.mir.run_brace, time_width=1.5, color=TEAL),
                      FlashAround(self.mir.rise_brace, time_width=1.5, color=TEAL), run_time=1.5)
            c.wait_until("switch")
            derive(self, L1b, L2, run_time=min(2.0, c.until("inside") - 0.1))
            c.wait_until("inside")
            derive(self, L2, L3, run_time=min(2.0, c.until("done") - 0.1))
            c.wait_until("done")
            derive(self, L3, L4, run_time=min(2.0, c.until() - 0.1))

    # ------------------------------------------------------------------ c3.recip.3
    def clip3(self):
        cond = tx([r"\dfrac{dy}{dx}", r"\neq 0"], 44)
        cond[0].set_color(GREEN)
        cond[1].set_color(RED)
        cond.next_to(self.L4, RIGHT, buff=1.6)
        top_spot = np.array([4.7, 2.95, 0])
        cu = 1.15
        CO = np.array([-2.6, -0.75, 0])
        ax = fig_axes(origin=CO, u=cu, lo=-2.2, hi=2.2)
        xl = MathTex("x", font_size=36).next_to(ax.x_axis.get_end(), RIGHT, buff=0.12)
        yl = MathTex("y", font_size=36).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        curve = ax.plot(lambda x: x ** 3, x_range=[-1.29, 1.29], color=BLUE, stroke_width=5)
        tan0 = Line(ax.c2p(-1.7, 0), ax.c2p(1.7, 0), color=GREEN, stroke_width=6)
        diag = DashedLine(ax.c2p(-2.0, -2.0), ax.c2p(2.0, 2.0), color=DIM, dash_length=0.12, stroke_width=3)
        lab3 = MathTex("y = x^3", font_size=48, color=BLUE).move_to(np.array([3.3, 1.1, 0]))
        lab13 = MathTex("y = x^{1/3}", font_size=48, color=BLUE).move_to(lab3)
        inf = MathTex(r"\dfrac{1}{0}", font_size=56, color=RED).move_to(np.array([3.3, -0.5, 0]))
        circ = load_scene("ch3_s3_circle").circle_figure(centre_dot=False, ticks=False, verticals=True)
        circ.remove(circ.xlab, circ.ylab)
        fit(circ, 2.5, 2.2).move_to(np.array([5.3, -2.3, 0]))
        with self.say("c3.recip.3") as c:
            self.play(*appear(cond), run_time=1.0)
            c.wait_until("cube")
            sweep_clear(self, cond.animate.move_to(top_spot), keep=[self.eqg, cond],
                        run_time=min(1.6, c.until("the same curve")))
            c.wait_until("the same curve")
            self.play(FadeIn(ax), *appear(xl, yl, lag=0.1), Create(curve),  # early: axis labels with axes
                      run_time=min(1.5, c.until("at the origin")))
            self.play(*appear(lab3), run_time=1.0)  # early: names the curve just spoken
            c.wait_until("flat")
            self.play(Create(tan0), run_time=1.2)
            c.wait_until("reflect")
            self.play(*during(Create(diag), 0, 0.3),
                      *during(Rotate(curve, angle=PI, axis=DIAG_AXIS, about_point=ax.c2p(0, 0)), 0.2, 1),
                      *during(swap(lab3, lab13), 0.5, 1),
                      run_time=min(2.0, c.until("vertical") - 0.05))
            c.wait_until("vertical")
            self.play(turn(tan0, ax.c2p(0, 0), PI / 2, GREEN, RED), run_time=1.5)
            c.wait_until("nofinite")
            self.play(*appear(inf), run_time=1.0)
            c.wait_until("circle")
            self.play(*appear(circ, shift=None), run_time=0.8)
            self.play(FlashAround(circ.v_left, color=RED, time_width=1.5),
                      FlashAround(circ.v_right, color=RED, time_width=1.5),
                      run_time=min(1.4, c.until()))

    # ------------------------------------------------------------------ c3.recip.4
    def clip4(self):
        tri, abox = s5_parts()
        fit(tri, 3.4, 2.6).move_to(np.array([4.6, 1.2, 0]))
        fit(abox, 3.4, 1.6).move_to(np.array([4.6, -2.3, 0]))
        EQX = -2.2

        def row(m, y, i):
            m.shift(np.array([EQX - m[i].get_x(), y - m[i].get_y(), 0]))
            return m
        M0 = row(tx(["x", "=", r"\tan y"], 44), 2.75, 1)
        M1 = row(tx([r"\dfrac{dx}{dy}", "=", r"\sec^2 y"], 44), 1.55, 1)
        M2 = row(tx(["=", r"1 + \tan^2 y"], 44), 0.4, 0)
        M3 = row(tx(["=", r"1 + x^2"], 44), -0.65, 0)
        M4 = row(tx([r"\dfrac{dy}{dx}", "=", r"\dfrac{1}{1 + x^2}"], 44), -2.3, 1)
        M4[0].set_color(GREEN)
        box = SurroundingRectangle(M4, color=YELLOW, buff=0.3, stroke_width=3)
        tick = check_mark()
        with self.say("c3.recip.4") as c:
            sweep_clear(self, *appear(tri, abox, lag=0.3, shift=None), run_time=1.8)
            c.wait_until("tan")
            self.play(FlashAround(tri.y, time_width=1.5), FlashAround(tri.arc, time_width=1.5), run_time=1.3)
            c.wait_until("so ex is")
            self.play(*appear(M0), run_time=1.0)
            c.wait_until("dxdy")
            derive(self, M0, M1, run_time=min(2.0, c.until("identity") - 0.1))
            c.wait_until("identity")
            derive(self, M1, M2, run_time=min(1.8, c.until("back") - 0.1))
            c.wait_until("back")
            derive(self, M2, M3, run_time=min(1.8, c.until("flipit") - 0.1))
            c.wait_until("flipit")
            derive(self, M3, M4, run_time=2.0)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("same")
            res = VGroup(box, M4)
            settle(self, res)
            res.generate_target()
            res.target.scale(abox.height / res.height)
            res.target.next_to(abox, LEFT, buff=0.9)
            tick.move_to((res.target.get_right() + abox.get_left()) / 2)
            self.play(MoveToTarget(res), run_time=1.5)
            self.play(GrowFromCenter(tick), FlashAround(abox, color=GREEN, time_width=1.5),
                      FlashAround(res, color=GREEN, time_width=1.5), run_time=min(1.4, c.until()))
