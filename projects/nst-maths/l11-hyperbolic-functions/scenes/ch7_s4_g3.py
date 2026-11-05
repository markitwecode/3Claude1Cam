"""Chapter 7, scene 4: G3, six sketches by reflection in y = x. Clips c7.g3.1 – c7.g3.6.

Card G3 enlarged + pause; the mirror shortcut and the pairs; panels e^x -> ln x, cosh (halves,
sideways mirror), sinh -> sinh^-1, tanh -> tanh^-1; the six final sketches (a)-(f) with their marks.

Shared (load_scene("ch7_s4_g3")):
  eq_axes(xr, yr, unit, center)        equal-unit axes (DIM, no tips), bbox centred on `center`
  tanh_panel(inverse_only=False, unit=1.0, center=ORIGIN)
      axes x, y in [-3, 3] (equal units), dashed DIM y = x, TEAL tanh x (dropped if inverse_only),
      INV_C (lighter TEAL) tanh^-1 x for y in [-3, 3], dashed GOLD x = 1 and PURPLE x = -1.
      Attributes .ax .mirror .tanh (or None) .atanh .vp .vm
  INV_C "#A8EBD9" (inverses), LGOLD_C "#F7D3A6" (ln x)
"""
# style: 2
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

INV_C = "#A8EBD9"      # lighter teal: inverses
LGOLD_C = "#F7D3A6"    # lighter gold: ln x
PANEL_C = np.array([-0.9, -0.05, 0])
HERO_C = np.array([-1.5, 0.3, 0])


# ---------------------------------------------------------------- shared graph helpers
def eq_axes(xr, yr, unit=1.0, center=ORIGIN, ticks=True):
    ax = Axes(x_range=[xr[0], xr[1], 1], y_range=[yr[0], yr[1], 1],
              x_length=(xr[1] - xr[0]) * unit, y_length=(yr[1] - yr[0]) * unit, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": ticks,
                           "tick_size": 0.06})
    ax.move_to(center)
    return ax


def pcurve(ax, fx, fy, t0, t1, color, width=5, n=240):
    ts = np.linspace(t0, t1, n)
    m = VMobject().set_points_smoothly([ax.c2p(fx(t), fy(t)) for t in ts])
    return m.set_stroke(color, width).set_fill(opacity=0)


def fcurve(ax, f, x0, x1, color, width=5, n=240):
    return pcurve(ax, lambda t: t, f, x0, x1, color, width, n)


def dashed(m, n=28, ratio=0.55):
    return DashedVMobject(m, num_dashes=n, dashed_ratio=ratio)


def dline(ax, p, q, color, width=3, n=None):
    a, b = ax.c2p(*p), ax.c2p(*q)
    if n is None:
        n = max(8, int(np.linalg.norm(b - a) / 0.22))
    return DashedLine(a, b, dash_length=0.12, dashed_ratio=0.55).set_stroke(color, width)


def mirror_line(ax, lo, hi):
    return dline(ax, (lo, lo), (hi, hi), DIM, 3)


def kdot(ax, x, y, r=0.09):
    return Dot(ax.c2p(x, y), radius=r, color=YELLOW).set_z_index(3)


def tangent(ax, x0, y0, slope=1.0, half=0.75, color=YELLOW):
    dx = half / math.sqrt(1 + slope * slope)
    return Line(ax.c2p(x0 - dx, y0 - slope * dx), ax.c2p(x0 + dx, y0 + slope * dx)).set_stroke(color, 3)


def flip(mob, ax, **kw):
    """Reflect in y = x as a turn about that line (equal units only)."""
    return Rotate(mob, angle=PI, axis=np.array([1.0, 1.0, 0.0]), about_point=ax.c2p(0, 0), **kw)


def clear_to(scene, *incoming, run_time=1.2):
    """Fade the whole board out (first half), incoming in (second half)."""
    scene.play(*during([FadeOut(m) for m in scene.mobjects], 0, 0.5), *during(list(incoming), 0.5, 1),
               run_time=run_time)


def lab(tex, color=FG, size=40):
    return set_backstroke(MathTex(tex, font_size=size, color=color))


def tanh_panel(inverse_only=False, unit=1.0, center=ORIGIN):
    ax = eq_axes((-3, 3), (-3, 3), unit, center)
    mirror = mirror_line(ax, -3, 3)
    th = None if inverse_only else fcurve(ax, math.tanh, -3, 3, TEAL, 5)
    ath = pcurve(ax, math.tanh, lambda t: t, -3, 3, INV_C, 5)
    vp = dline(ax, (1, -3), (1, 3), GOLD)
    vm = dline(ax, (-1, -3), (-1, 3), PURPLE)
    parts = [ax, mirror, vp, vm] + ([th] if th is not None else []) + [ath]
    g = VGroup(*parts)
    g.ax, g.mirror, g.tanh, g.atanh, g.vp, g.vm = ax, mirror, th, ath, vp, vm
    return g


# ---------------------------------------------------------------- final grid sketches
MINI_U = 0.48
MINI_X, MINI_Y = (-2.5, 2.5), (-2.0, 2.5)


def mini(kind, center):
    ax = eq_axes(MINI_X, MINI_Y, MINI_U, ORIGIN, ticks=False)
    w = 4
    if kind == "a":
        parts = [fcurve(ax, math.exp, -2.5, math.log(2.5), GOLD, w), kdot(ax, 0, 1, 0.07)]
        title, marks = r"(a)\ \ e^x", r"(0,1),\ \ y\to 0"
    elif kind == "b":
        a = math.acosh(2.5)
        parts = [fcurve(ax, math.cosh, -a, a, TEAL, w), kdot(ax, 0, 1, 0.07)]
        title, marks = r"(b)\ \ \cosh x", r"\text{min }(0,1),\ \text{even}"
    elif kind == "c":
        parts = [dline(ax, (-2.5, 1), (2.5, 1), GOLD, 2), dline(ax, (-2.5, -1), (2.5, -1), PURPLE, 2),
                 fcurve(ax, math.tanh, -2.5, 2.5, TEAL, w), kdot(ax, 0, 0, 0.07)]
        title, marks = r"(c)\ \ \tanh x", r"y=\pm 1,\ \text{odd}"
    elif kind == "d":
        parts = [dline(ax, (0, -2), (0, 2.5), LGOLD_C, 2),
                 fcurve(ax, math.log, math.exp(-2), 2.5, LGOLD_C, w), kdot(ax, 1, 0, 0.07)]
        title, marks = r"(d)\ \ \ln x", r"(1,0),\ x=0,\ x>0"
    elif kind == "e":
        parts = [fcurve(ax, math.asinh, -2.5, 2.5, INV_C, w), kdot(ax, 0, 0, 0.07)]
        title, marks = r"(e)\ \ \sinh^{-1}x", r"\text{slope 1 at 0, odd}"
    else:
        parts = [dline(ax, (1, -2), (1, 2.5), GOLD, 2), dline(ax, (-1, -2), (-1, 2.5), PURPLE, 2),
                 pcurve(ax, math.tanh, lambda t: t, -2, 2.5, INV_C, w), kdot(ax, 0, 0, 0.07)]
        title, marks = r"(f)\ \ \tanh^{-1}x", r"x=\pm 1,\ \text{odd}"
    ttl = MathTex(title, font_size=36).next_to(ax, UP, buff=0.12)
    mk = MathTex(marks, font_size=30, color=YELLOW).next_to(ax, DOWN, buff=0.14)
    sketch = VGroup(ax, *parts)
    g = VGroup(sketch, ttl, mk).move_to(center)
    g.sketch, g.title, g.marks = sketch, ttl, mk
    return g


class Ch7S4G3(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c7.g3.1 card + pause
    def clip1(self):
        s1 = load_scene("ch7_s1_intro")
        with self.say("c7.g3.1") as c:
            row = s1.card_row(lit=True)
            self.play(FadeIn(row), run_time=0.6)  # early: the cards from the intro
            hero = s1.g_card(3, lit=True).scale_to_fit_height(4.5).move_to(HERO_C)
            others = [row[0], row[1], row[3]]
            self.play(*during([FadeOut(m) for m in others], 0, 0.4),
                      *during([Transform(row[2], hero)], 0.25, 1),
                      run_time=1.8)
            self.remove(*row.get_family())
            self.add(hero)
            c.wait_until("stop")
            pause = s1.pause_icon(height=1.2).move_to([4.5, 0.3, 0])
            self.play(FadeIn(pause, scale=0.8), run_time=0.8)
        self.play(*disappear(hero, pause), run_time=0.8)

    # ------------------------------------------------------------ c7.g3.2 mirror + pairs
    def clip2(self):
        with self.say("c7.g3.2", gap=2.5) as c:
            ax = eq_axes((-2.5, 2.5), (-2.5, 2.5), 1.0, [-3.7, -0.2, 0])
            ex = fcurve(ax, math.exp, -2.5, math.log(2.5), GOLD, 5)
            ex_l = lab("e^x", GOLD).next_to(ax.c2p(math.log(2.5), 2.5), LEFT, buff=0.15)
            self.play(FadeIn(ax), Create(ex), run_time=1.4)
            self.play(*appear(ex_l), run_time=0.6)
            c.wait_until("each inverse")
            mir = mirror_line(ax, -2.5, 2.5)
            mir_l = lab("y=x", DIM, 34).next_to(ax.c2p(2.5, 2.5), RIGHT, buff=0.15)
            self.play(Create(mir), *appear(mir_l), run_time=1.2)
            c.wait_until("reflected")
            ln = ex.copy()
            self.play(flip(ln, ax), run_time=2.0)
            ln_l = lab(r"\ln x", LGOLD_C).next_to(ax.c2p(2.5, math.log(2.5)), DOWN, buff=0.2)
            self.play(ln.animate.set_stroke(LGOLD_C), *appear(ln_l), run_time=0.8)

            ys = [2.1, 0.7, -0.7, -2.1]
            xf, xa, xi = 1.7, 3.55, 5.4

            def row(y, f_tex, f_col, i_tex, i_col, f_op=1.0):
                f = lab(f_tex, f_col, 44).move_to([xf, y, 0])
                f.set_opacity(f_op)
                a = MathTex(r"\leftrightarrow", font_size=44, color=DIM).move_to([xa, y, 0])
                i = lab(i_tex, i_col, 44).move_to([xi, y, 0])
                return f, a, i

            c.wait_until("pairs")
            r1 = row(ys[0], "e^x", GOLD, r"\ln x", LGOLD_C)
            self.play(*appear(*r1, lag=0.3), run_time=1.2)
            c.wait_until("inverse tanch")
            r2 = row(ys[1], r"\tanh x", TEAL, r"\tanh^{-1}x", INV_C)
            self.play(*appear(*r2, lag=0.3), run_time=1.2)
            c.wait_until("inverse shine")
            r3 = row(ys[2], r"\sinh x", TEAL, r"\sinh^{-1}x", INV_C, f_op=0.4)
            self.play(*appear(*r3, lag=0.3), run_time=1.2)
            c.wait_until("which the sheet")
            ch = lab(r"\cosh x", TEAL, 44).move_to([xf, ys[3], 0])
            self.play(*appear(ch), run_time=0.9)  # early: cosh shown alone to complete the six; named in c7.g3.4
        self.clip2_mobs = [ax, ex, ex_l, mir, mir_l, ln, ln_l, *r1, *r2, *r3, ch]

    # ------------------------------------------------------------ c7.g3.3 e^x -> ln x
    def clip3(self):
        with self.say("c7.g3.3") as c:
            ax = eq_axes((-3.5, 3.5), (-3.5, 3.5), 0.95, PANEL_C)
            clear_to(self, FadeIn(ax))
            ex = fcurve(ax, math.exp, -3.5, math.log(3.5), GOLD, 6)
            ex_l = lab("e^x", GOLD, 44).next_to(ax.c2p(math.log(3.5), 3.5), RIGHT, buff=0.2)
            self.play(Create(ex), *during(appear(ex_l), 0.6, 1), run_time=1.6)
            c.wait_until("passes through")
            d01 = kdot(ax, 0, 1)
            d01_l = lab("(0,1)", YELLOW, 36).next_to(ax.c2p(0, 1), LEFT, buff=0.35).shift(0.25 * UP)
            self.play(FadeIn(d01, scale=0.5), *appear(d01_l), run_time=1.0)
            c.wait_until("slope one")
            t01 = tangent(ax, 0, 1, 1, 0.9)
            self.play(GrowFromCenter(t01), run_time=0.9)
            c.wait_until("on the left")
            neg = Line(ax.c2p(-3.5, 0), ax.c2p(0, 0)).set_stroke(YELLOW, 5)
            neg_l = lab(r"y\to 0", YELLOW, 38).move_to(ax.c2p(-2.4, -0.55))
            self.play(Create(neg), run_time=1.4)
            c.wait_until("stays positive")
            self.play(*appear(neg_l), run_time=0.8)

            c.wait_until("log")
            ex_group = [ex, ex_l, d01, d01_l, t01, neg, neg_l]
            mir = mirror_line(ax, -3.5, 3.5)
            self.play(Create(mir), *set_alpha(ex_group, 0.35), run_time=1.0)
            ln = ex.copy().set_stroke(opacity=1)
            self.add(ln)
            self.play(flip(ln, ax), run_time=2.0)
            ln_l = lab(r"\ln x", LGOLD_C, 44).next_to(ax.c2p(3.5, math.log(3.5)), DOWN, buff=0.25)
            self.play(ln.animate.set_stroke(LGOLD_C), *appear(ln_l), run_time=0.8)
            c.wait_until("positive", nth=1)
            pos_l = lab(r"x>0", LGOLD_C, 40).move_to(ax.c2p(2.4, -1.3))
            self.play(*appear(pos_l), run_time=0.9)
            c.wait_until("at one")
            d10 = kdot(ax, 1, 0)
            t10 = tangent(ax, 1, 0, 1, 0.9)
            d10_l = lab("(1,0)", YELLOW, 36).next_to(ax.c2p(1, 0), RIGHT, buff=0.3).shift(0.3 * DOWN)
            self.play(FadeIn(d10, scale=0.5), GrowFromCenter(t10), *appear(d10_l), run_time=1.2)
            c.wait_until("plunges down")
            yax = dline(ax, (0, -3.5), (0, 3.5), LGOLD_C, 4)
            yax_l = lab("x=0", LGOLD_C, 36).next_to(ax.c2p(0, -3.0), RIGHT, buff=0.35)
            self.play(Create(yax), run_time=1.4)
            self.play(*appear(yax_l), run_time=0.8)
            c.wait_until("on the right")
            right = fcurve(ax, math.log, 1.0, 3.5, YELLOW, 8)
            self.play(VShowPassingFlash(right, time_width=0.6), run_time=2.0)

    # ------------------------------------------------------------ c7.g3.4 cosh
    def clip4(self):
        with self.say("c7.g3.4", gap=3.0) as c:
            ax = eq_axes((-3.5, 3.5), (-2.5, 4.0), 0.95, PANEL_C)
            clear_to(self, FadeIn(ax))
            a = math.acosh(3.5)
            ch = fcurve(ax, math.cosh, -a, a, TEAL, 6)
            ch_l = lab(r"\cosh x", TEAL, 44).next_to(ax.c2p(a, 3.5), RIGHT, buff=0.2)
            self.play(Create(ch), *during(appear(ch_l), 0.6, 1), run_time=1.6)
            c.wait_until("even")
            ev_l = lab(r"\text{even}", TEAL, 40).next_to(ax.c2p(-a, 3.5), LEFT, buff=0.2)
            self.play(*appear(ev_l), run_time=0.8)
            c.wait_until("lowest point")
            d = kdot(ax, 0, 1)
            d_l = lab(r"\text{min }(0,1)", YELLOW, 36).move_to(ax.c2p(-1.75, 0.5))
            self.play(FadeIn(d, scale=0.5), *appear(d_l), run_time=1.0)

            c.wait_until("halves")
            l8 = math.log(7)
            hp = dashed(fcurve(ax, lambda x: 0.5 * math.exp(x), 0.2, l8, GOLD, 4), 22)
            hp_l = lab(r"\tfrac12 e^{x}", GOLD, 40).move_to(ax.c2p(2.95, 2.4))
            self.play(Create(hp), *during(appear(hp_l), 0.5, 1), run_time=1.5)
            c.wait_until("minus ex")
            hm = dashed(fcurve(ax, lambda x: 0.5 * math.exp(-x), -l8, -0.2, PURPLE, 4), 22)
            hm_l = lab(r"\tfrac12 e^{-x}", PURPLE, 40).move_to(ax.c2p(-2.95, 2.4))
            self.play(Create(hm), *during(appear(hm_l), 0.5, 1), run_time=1.5)

            c.wait_until("nomirror")
            mir = mirror_line(ax, -2.5, 4.0)
            self.play(Create(mir), *set_alpha([hp, hm, hp_l, hm_l, d_l], 0.3), run_time=1.0)
            up = fcurve(ax, math.cosh, 0, a, TEAL, 5).set_stroke(opacity=0.6)
            lo = fcurve(ax, math.cosh, -a, 0, PURPLE, 5).set_stroke(opacity=0.6)
            self.add(up, lo)
            self.play(flip(up, ax), flip(lo, ax), run_time=2.0)
            xv = 2.5
            yv = math.acosh(xv)
            vl = dline(ax, (xv, -2.0), (xv, 2.0), YELLOW, 2)
            dots = [kdot(ax, xv, yv), kdot(ax, xv, -yv)]
            two_l = T("two values\nfor each x", 32, color=YELLOW, line_spacing=0.8)
            two_l.move_to([5.0, -1.6, 0])
            self.play(Create(vl), *[FadeIn(dd, scale=0.5) for dd in dots], *appear(two_l), run_time=1.2)

    # ------------------------------------------------------------ c7.g3.5 sinh -> sinh^-1
    def clip5(self):
        with self.say("c7.g3.5", gap=2.5) as c:
            ax = eq_axes((-3.5, 3.5), (-3.5, 3.5), 0.95, PANEL_C)
            mir = mirror_line(ax, -3.5, 3.5)
            clear_to(self, FadeIn(ax), FadeIn(mir))
            b = math.asinh(3.5)
            sh = fcurve(ax, math.sinh, -b, b, TEAL, 5).set_stroke(opacity=0.4)
            sh_l = lab(r"\sinh x", TEAL, 40).next_to(ax.c2p(b, 3.5), LEFT, buff=0.25).set_opacity(0.5)
            self.play(Create(sh), *during(appear(sh_l), 0.6, 1), run_time=1.4)
            c.wait_until("origin")
            d = kdot(ax, 0, 0)
            t0 = tangent(ax, 0, 0, 1, 0.9)
            self.play(FadeIn(d, scale=0.5), GrowFromCenter(t0), run_time=1.0)
            c.wait_until("asinh")
            ash = sh.copy().set_stroke(opacity=1)
            self.add(ash)
            self.play(flip(ash, ax), run_time=2.0)
            ash_l = lab(r"\sinh^{-1}x", INV_C, 44).next_to(ax.c2p(-3.5, -b), UP, buff=0.3)
            self.play(ash.animate.set_stroke(INV_C, 6), *appear(ash_l), run_time=0.8)
            c.wait_until("log of two")
            l2 = dashed(fcurve(ax, lambda x: math.log(2 * x), 0.6, 3.5, LGOLD_C, 3), 18)
            l2.set_stroke(opacity=0.7)
            l2_l = lab(r"\ln 2x", LGOLD_C, 38).next_to(ax.c2p(3.5, math.log(7)), DOWN, buff=0.35)
            self.play(Create(l2), *during(appear(l2_l), 0.5, 1), run_time=1.2)
            c.wait_until("every ex")
            note = T("all real x,\nno asymptotes", 34, color=INV_C, line_spacing=0.8)
            note.move_to([4.8, -2.2, 0])
            self.play(*appear(note), run_time=0.9)

    # ------------------------------------------------------------ c7.g3.6 tanh -> tanh^-1, grid
    def clip6(self):
        with self.say("c7.g3.6", gap=3.0) as c:
            P = tanh_panel(unit=1.0, center=PANEL_C)
            ax = P.ax
            clear_to(self, FadeIn(ax))
            th = P.tanh
            th_l = lab(r"\tanh x", TEAL, 44).next_to(ax.c2p(3, math.tanh(3)), DOWN, buff=0.3)
            self.play(Create(th), *during(appear(th_l), 0.6, 1), run_time=1.6)
            c.wait_until("slope one")
            d = kdot(ax, 0, 0)
            t0 = tangent(ax, 0, 0, 1, 0.8)
            self.play(FadeIn(d, scale=0.5), GrowFromCenter(t0), run_time=1.0)
            c.wait_until("squeezed")
            hp = dline(ax, (-3, 1), (3, 1), GOLD)
            hm = dline(ax, (-3, -1), (3, -1), PURPLE)
            hp_l = lab("y=1", GOLD, 36).next_to(ax.c2p(-3, 1), LEFT, buff=0.2)
            hm_l = lab("y=-1", PURPLE, 36).next_to(ax.c2p(-3, -1), LEFT, buff=0.2)
            self.play(Create(hp), Create(hm), *during(appear(hp_l, hm_l), 0.5, 1), run_time=1.4)

            c.wait_until("atanh")
            self.play(Create(P.mirror), run_time=0.9)
            ath = th.copy()
            self.add(ath)
            vp_l = lab("x=1", GOLD, 36).next_to(ax.c2p(1, -2.75), RIGHT, buff=0.2)
            vm_l = lab("x=-1", PURPLE, 36).next_to(ax.c2p(-1, -2.75), LEFT, buff=0.2)
            # the y = ±1 labels leave before the lines tilt; x = ±1 arrive once they stand vertical
            self.play(flip(ath, ax), flip(hp, ax), flip(hm, ax), th.animate.set_stroke(opacity=0.35),
                      th_l.animate.set_opacity(0.35),
                      *during(disappear(hp_l, hm_l), 0, 0.3), *during(appear(vp_l, vm_l), 0.75, 1),
                      run_time=2.4)  # early: the turned asymptotes are named as they land; read at "lives between"
            self.remove(hp, hm)
            self.add(P.vp, P.vm)
            ath_l = lab(r"\tanh^{-1}x", INV_C, 44).next_to(ax.c2p(1.3, 1.65), RIGHT, buff=0.1)
            self.play(ath.animate.set_stroke(INV_C, 6), *appear(ath_l), run_time=0.8)
            c.wait_until("lives between")
            self.play(*flash([vm_l, vp_l]), run_time=1.2)
            inf_p = lab(r"+\infty", YELLOW, 40).next_to(ax.c2p(1, 2.65), RIGHT, buff=0.25)
            inf_m = lab(r"-\infty", YELLOW, 40).next_to(ax.c2p(-1, -1.6), LEFT, buff=0.25)
            self.play(*appear(inf_p, inf_m, lag=0.4), run_time=1.2)

            c.wait_until("features")
            xs, ys = [-4.5, 0.0, 4.5], [1.72, -1.72]
            grid = [mini(k, [xs[i % 3], ys[i // 3], 0]) for i, k in enumerate("abcdef")]
            clear_to(self, *[FadeIn(g) for g in grid], run_time=1.4)
