"""Chapter 2, scene 7: every swing is a cos ωt + b sin ωt. Clips c2.every.1 – c2.every.5.

Exports (for parts 3–4, the running example x = 3 cos 3t + 4 sin 3t):
  graph_axes()             the t–x panel (t 0..2.5 s, x in cm), TEAL period mark at 2π/3.
  graph_waves(a, b)        BLUE dashed a cos 3t, dotted b sin 3t, solid sum (b may be a tracker).
  graph_key(b_tex)         the key row: dashed "3 cos 3t", dotted "<b> sin 3t", solid "x".
  example_graph()          the finished picture: axes + 3 cos 3t and 4 sin 3t adding into
                           x = 3 cos 3t + 4 sin 3t, with its key. .axes .waves .key
  block_card(x_cm)         ch1's spring and block, small (scale 0.55), rest point BC_REST.
"""
# style: 2
import math
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
spr = load_scene("ch1_s3_spring")
pen = load_scene("ch1_s5_gravity")

W = ak.OMEGA
THUMB_O = np.array([-5.35, 2.05, 0])     # the plane's corner home (scale THUMB_S)
THUMB_S = 0.36

# ── the graph panel (ω = 3) ──────────────────────────────────────────────────────
GRAPH_O = np.array([-6.0, -0.5, 0])
G_SX, G_SY = 2.35, 0.19                  # units per second, per cm
G_TMAX = 2.5
G_W = 3.0
PERIOD = TAU / G_W


def _gp(t, x, origin=GRAPH_O):
    return np.array(origin, dtype=float) + np.array([G_SX * t, G_SY * x, 0.0])


def graph_axes(origin=GRAPH_O):
    """DIM t and x axes, a "1" tick, "3" on x, the TEAL period mark at 2π/3 ≈ 2.09 s.
    .t_axis .x_axis .period"""
    o = np.array(origin, dtype=float)
    t_ax = Arrow(o + LEFT * 0.1, _gp(G_TMAX, 0, o) + RIGHT * 0.25, buff=0, stroke_width=2.5,
                 tip_length=0.16, color=DIM)
    x_ax = Arrow(_gp(0, -5.3, o), _gp(0, 5.6, o), buff=0, stroke_width=2.5, tip_length=0.16,
                 color=DIM)
    t_lab = T("t (s)", size=24, color=DIM).next_to(t_ax.get_end(), RIGHT, buff=0.1)
    x_lab = T("x (cm)", size=24, color=DIM).next_to(x_ax.get_end(), UP, buff=0.06)
    tick1 = Line(_gp(1, 0, o) + DOWN * 0.07, _gp(1, 0, o) + UP * 0.07).set_stroke(DIM, 2)
    one = T("1", size=22, color=DIM).next_to(tick1, DOWN, buff=0.08)
    set_backstroke(one, width=4)
    tick3 = Line(_gp(0, 3, o) + LEFT * 0.07, _gp(0, 3, o) + RIGHT * 0.07).set_stroke(DIM, 2)
    three = T("3", size=22, color=DIM).next_to(tick3, LEFT, buff=0.08)
    per_line = DashedLine(_gp(PERIOD, -5, o), _gp(PERIOD, 5, o), dash_length=0.08)
    per_line.set_stroke(TEAL, 2, opacity=0.6)
    per_tick = Line(_gp(PERIOD, 0, o) + DOWN * 0.1, _gp(PERIOD, 0, o) + UP * 0.1).set_stroke(TEAL, 4)
    per_lab = T("2π/3 ≈ 2.09 s", size=22, color=TEAL).next_to(per_line, UP, buff=0.06)
    period = VGroup(per_line, per_tick, per_lab)
    g = VGroup(t_ax, x_ax, t_lab, x_lab, tick1, one, tick3, three, period)
    g.t_axis, g.x_axis, g.period = t_ax, x_ax, period
    g.set_z_index(-3)
    return g


def _vv(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _waves_still(a, b, origin=GRAPH_O):
    ts = np.linspace(0, G_TMAX, 160)

    def curve(f):
        m = VMobject()
        m.set_points_smoothly([_gp(t, f(t), origin) for t in ts])
        return m
    cw = DashedVMobject(curve(lambda t: a * math.cos(G_W * t)), num_dashes=34, dashed_ratio=0.55)
    cw.set_stroke(BLUE, 3, opacity=0.85)
    sw = DashedVMobject(curve(lambda t: b * math.sin(G_W * t)), num_dashes=95, dashed_ratio=0.28)
    sw.set_stroke(BLUE, 3.5, opacity=0.85)
    tot = curve(lambda t: a * math.cos(G_W * t) + b * math.sin(G_W * t)).set_stroke(BLUE, 5)
    g = VGroup(cw, sw, tot)
    g.cos, g.sin, g.sum = cw, sw, tot
    return g


def graph_waves(a=3.0, b=4.0, origin=GRAPH_O):
    """a cos 3t (dashed), b sin 3t (dotted), their sum (solid), all BLUE. b: number or tracker.
    .cos .sin .sum (still version only)"""
    if hasattr(b, "get_value"):
        return always_redraw(lambda: _waves_still(a, b.get_value(), origin))
    return _waves_still(a, b, origin)


def graph_key(b_tex="b", a_tex="3"):
    """Key row above the panel: dashed a cos 3t, dotted b sin 3t, solid x. .items"""
    def sample(kind):
        ln = Line(ORIGIN, RIGHT * 0.5)
        if kind == "dash":
            m = DashedVMobject(ln, num_dashes=3, dashed_ratio=0.55).set_stroke(BLUE, 3)
        elif kind == "dot":
            m = DashedVMobject(ln, num_dashes=6, dashed_ratio=0.3).set_stroke(BLUE, 3.5)
        else:
            m = ln.set_stroke(BLUE, 5)
        return m
    items = []
    for kind, tex in (("dash", a_tex + r"\cos 3t"), ("dot", b_tex + r"\sin 3t"), ("solid", "x")):
        lab = MathTex(tex, font_size=30, color=BLUE)
        items.append(VGroup(sample(kind), lab).arrange(RIGHT, buff=0.14))
    g = VGroup(*items).arrange(RIGHT, buff=0.45)
    g.move_to([GRAPH_O[0] + 0.55, 0.97, 0], aligned_edge=LEFT)
    g.items = items
    return g


def example_graph():
    """The running example's picture: 3 cos 3t and 4 sin 3t adding into x = 3 cos 3t + 4 sin 3t.
    .axes .waves .key"""
    ax = graph_axes()
    wv = graph_waves(3.0, 4.0)
    key = graph_key("4")
    g = VGroup(ax, wv, key)
    g.axes, g.waves, g.key = ax, wv, key
    return g


# ── the small block card ─────────────────────────────────────────────────────────
BC_REST = np.array([-1.7, 1.5, 0])
BC_S = 0.55


def block_card(x_cm):
    g = spr.spring_drawing(x_cm, y=spr.SPRING_Y, zero=False)
    g.shift(BC_REST - np.array([spr.SPRING_REST_X, spr.SPRING_Y, 0]))
    g.scale(BC_S, about_point=BC_REST)
    return g


def bc_center(x_cm):
    return BC_REST + BC_S * np.array([spr.SPRING_UNIT * x_cm, spr.BLOCK_H / 2, 0])


# ── legend entries ───────────────────────────────────────────────────────────────
E_COS = (r"e^{i\omega t}", GOLD, "cosine arrow")
E_SIN = (r"-i\,e^{i\omega t}", GOLD, "sine arrow: starts at −i")
E_A = ("a", BLUE, "cosine coefficient")
E_B = ("b", BLUE, "sine coefficient")
E_X0 = ("x_0", BLUE, "start position")
E_V0 = ("v_0", GREEN, "start velocity")

COLX = kit.COL_LEFT


def at_col(mob, y):
    return mob.move_to([COLX, y, 0], aligned_edge=LEFT)


def lab_at(text, y):
    """kit.step_label whose label sits at height y."""
    return kit.step_label(text, (kit.COL_TOP - y) / kit.COL_PITCH + 0.5)


def align_eq(line, ref_eq, idx=0):
    line.shift((ref_eq.get_center()[0] - line[idx].get_center()[0]) * RIGHT)
    return line


def ybox(mob, buff=0.14, width=3):
    return SurroundingRectangle(mob, color=YELLOW, buff=buff).set_stroke(YELLOW, width)


S = kit.COL_SIZE


class Every(NarratedScene):
    def construct(self):
        self.t = ak.clock(ValueTracker(0.0))
        self.z = ValueTracker(0.0)          # 0: plane at s3's scale, 1: in the corner
        self.cop = ValueTracker(1.0)        # cosine arrow opacity
        self.sop = ValueTracker(1.0)        # spring opacity
        self.bx = ValueTracker(1.0)         # block (real part) before it follows the sine
        self.follow = False
        self.add(self.t, self.z, self.cop, self.sop, self.bx)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(2.2)                      # the pendulum swings on
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── geometry of the zooming plane ────────────────────────────────────────────
    def geo(self):
        z = self.z.get_value()
        return 1 + (THUMB_S - 1) * z, ak.PLANE_O + (THUMB_O - ak.PLANE_O) * z

    def _plane(self):
        s, o = self.geo()
        return ak.plane(s, o)

    def _arrow(self, offset, op=None):
        s, o = self.geo()
        a = ak.turning_arrow(self.t.get_value(), offset=offset, scale=s, origin=o,
                             width=6 - 2 * self.z.get_value())
        if op is not None:
            a.set_opacity(op.get_value())
        return a

    def _shadow(self, offset, op=None):
        s, o = self.geo()
        g = ak.shadow(self.t.get_value(), offset=offset, scale=s, origin=o)
        if op is not None:
            g.set_opacity(op.get_value())
        return g

    def _spring(self):
        s, o = self.geo()
        xr = math.sin(W * self.t.get_value()) if self.follow else self.bx.get_value()
        g = spr.spring_drawing(ak.PLANE_R * xr / spr.SPRING_UNIT,
                               y=ak.PLANE_O[1] - spr.BLOCK_H / 2, zero=False)
        g.shift(o - ak.PLANE_O)
        g.scale(s, about_point=o)
        op = self.sop.get_value()
        g.set_stroke(opacity=op)
        g.block.set_fill(BLUE, 0.3 * op)
        return g

    def tip(self, offset):
        s, o = self.geo()
        return ak.plane_point(ak.phasor(self.t.get_value(), offset=offset), s, o)

    def place_label(self, m, offset, gap=0.45):
        """Put label m on the clockwise side of the arrow's tip, clear of it by `gap`."""
        phi = W * self.t.get_value() + offset
        n = np.array([math.sin(phi), -math.cos(phi), 0.0])
        ext = abs(n[0]) * m.width / 2 + abs(n[1]) * m.height / 2
        m.move_to(self.tip(offset) + n * (gap + ext))
        return m

    # ── c2.every.1: the sine arrow ──────────────────────────────────────────────
    def clip1(self):
        t = self.t
        self.pl = always_redraw(self._plane)
        self.pin = ak.rule_pin()
        self.leg = kit.legend([ak.E_X, ak.E_W, ak.E_T, E_COS], max_rows=5)
        self.cos = always_redraw(lambda: self._arrow(0.0, self.cop))
        self.cos_sh = always_redraw(lambda: self._shadow(0.0, self.cop))
        self.spring = always_redraw(self._spring)
        self.cos_lab = T("cosine arrow", size=28, color=GOLD)
        self.place_label(self.cos_lab, 0.0)
        set_backstroke(self.cos_lab, width=5)
        with self.say("c2.every.1") as c:
            self.play(*appear(self.pl, self.pin, self.leg, shift=None, lag=0.2),  # early: the board
                      run_time=1.3)
            self.play(GrowArrow(self.cos), FadeIn(self.cos_sh), FadeIn(self.spring), run_time=1.3)
            c.wait_until("the cosine")
            self.play(*appear(self.cos_lab), run_time=1.0)

            # {push}: start anywhere, at any speed
            c.wait_until("push")
            o = ak.PLANE_O
            gy = o[1] + spr.BLOCK_H / 2 + 0.3
            self.push = ak.arrow_between([o[0], gy, 0], [o[0] + 1.2, gy, 0], GREEN, 6, z=0)
            self.push_txt = T("start anywhere, at any speed", size=34)
            self.push_txt.move_to([(COLX + kit.EDGE_X) / 2, o[1], 0])
            self.play(self.bx.animate.set_value(0.0), *appear(self.push_txt), run_time=1.5)
            self.play(GrowArrow(self.push), run_time=1.1)

            # {down}: the arrow that starts at -i
            c.wait_until("down")
            self.sin = always_redraw(lambda: self._arrow(-PI / 2))
            self.sin_sh = always_redraw(lambda: self._shadow(-PI / 2))
            self.sin_lab = MathTex("-i", r"\,e^{i\omega t}", font_size=38)
            self.sin_lab[0].set_color(PINK)
            self.sin_lab[1].set_color(GOLD)
            self.place_label(self.sin_lab, -PI / 2)
            set_backstroke(self.sin_lab, width=5)
            self.play(*during(disappear(self.push), 0, 0.4),
                      *during([self.cop.animate.set_value(0.4), *set_alpha([self.cos_lab], 0.45)],
                              0, 0.6),
                      *during([GrowArrow(self.sin), FadeIn(self.sin_sh)], 0.4, 1.0),
                      *during(appear(self.sin_lab), 0.6, 1.0), run_time=1.9)

            c.wait_until("quarter turn behind")
            o = ak.PLANE_O
            self.qarc = Arc(radius=0.55, start_angle=-PI / 2, angle=PI / 2, arc_center=o)
            self.qarc.set_stroke(DIM, 3)
            self.qtxt = T("¼ turn behind", size=26, color=DIM).move_to([-2.05, -0.86, 0])
            set_backstroke(self.qtxt, width=5)
            self.play(Create(self.qarc), *appear(self.qtxt), *disappear(self.push_txt), run_time=1.3)
            c.wait_until("obeys the rule")
            self.play(FlashAround(self.pin.formula, color=YELLOW, time_width=1.5), run_time=1.5)

            # {predict}: where does its shadow start?
            c.wait_until("predict")
            self.q = T("?", size=56, color=YELLOW).move_to(o + UP * 0.85)
            set_backstroke(self.q, width=6)
            self.play(*appear(self.q, shift=None), run_time=0.8)

            # {sine}: release; the shadow starts at 0, heads right, reaches 1
            c.wait_until("sine")
            self.play(*disappear(self.q, self.qtxt), FadeOut(self.qarc), run_time=0.7)
            self.follow = True
            self.cos_lab.add_updater(lambda m: self.place_label(m, 0.0))
            self.sin_lab.add_updater(lambda m: self.place_label(m, -PI / 2))
            rt = max(1.8, c.until("a quarter turn later", floor=0.3) + 0.6)
            self.play(t.animate.set_value(PI / (2 * W)), run_time=min(3.2, rt))
            self.cos_lab.clear_updaters()
            self.sin_lab.clear_updaters()
            self.flag = MathTex(r"\omega t = \pi/2", font_size=32, color=YELLOW)
            self.flag.move_to(ak.plane_point(1.0) + RIGHT * 1.2 + UP * 0.72)
            set_backstroke(self.flag, width=5)
            self.play(*appear(self.flag), run_time=0.9)

            c.wait_until("that's the sine")
            self.sin_name = T("sine arrow", size=28, color=GOLD)
            self.sin_name.move_to(self.sin_lab)
            set_backstroke(self.sin_name, width=5)
            kit.legend_add(self, self.leg, E_SIN, run_time=1.3,
                           extra=swap(self.sin_lab, self.sin_name))

            # {algebra}: −i times Euler's formula
            c.wait_until("algebra")
            self.tag = kit.corner_tag()
            A0 = MathTex("-i", r"\,e^{i\omega t}", "=", "-i", r"(\cos\omega t + i\sin\omega t)",
                         font_size=S)
            A0[0].set_color(PINK)
            A0[1].set_color(GOLD)
            A0[3].set_color(PINK)
            A1 = MathTex("=", r"-i\cos\omega t", "-", "i^2", r"\sin\omega t", font_size=S)
            A1[3].set_color(PINK)
            A2 = MathTex("=", r"\sin\omega t", "-", r"i\cos\omega t", font_size=S)
            A3 = MathTex(r"\mathrm{Re}\!\left[-i\,e^{i\omega t}\right]", "=", r"\sin\omega t",
                         font_size=S + 2)
            A3[2].set_color(BLUE)
            at_col(A0, 2.4)
            at_col(A1, 1.6)
            at_col(A2, 0.8)
            at_col(A3, -0.15)
            align_eq(A1, A0[2])
            align_eq(A2, A0[2])
            a3box = ybox(A3)
            l0 = lab_at("Euler's formula", 2.78)
            l1 = lab_at("multiply out", 1.98)
            l2 = lab_at("i² = −1", 1.18)
            l3 = lab_at("take the shadow", 0.4)
            self.play(*appear(l0, A0, l1, A1, shift=None, lag=0.3),  # early: atomic lines at pace
                      *appear(self.tag, shift=None),
                      *disappear(self.flag), run_time=1.6)
            ak.run(t, True)
            self.cos_lab.add_updater(lambda m: self.place_label(m, 0.0))
            self.sin_name.add_updater(lambda m: self.place_label(m, -PI / 2))
            self.play(*appear(l2, A2, l3, A3, shift=None, lag=0.3),  # early: atomic lines at pace
                      time_span(GrowFromCenter(a3box), 1.1, 1.7), run_time=1.7)
            self.alg = [A0, A1, A2, l0, l1, l2, l3]
            self.A3, self.a3box = A3, a3box

    # ── c2.every.2: mix them; (81); the b sweep ─────────────────────────────────
    def clip2(self):
        self.axes = graph_axes()
        self.b = ValueTracker(2.0)
        self.b.rate = 0.0

        def sweep(m, dt):
            if m.rate:
                m.set_value(min(4.0, m.get_value() + m.rate * dt))
        self.b.add_updater(sweep)
        self.add(self.b)
        self.waves = graph_waves(3.0, 2.0)
        self.key = graph_key("b")
        with self.say("c2.every.2") as c:
            # {mix}: the plane goes to the corner, the graph takes the picture
            self.leg.max_rows = 4
            kit.legend_set(self, self.leg, [ak.E_X, kit.E_XDD, ak.E_W, ak.E_T],
                           self.z.animate.set_value(1.0),
                           *during([self.sop.animate.set_value(0.0)], 0, 0.45),
                           *during(disappear(self.cos_lab, self.sin_name), 0, 0.3),
                           *during(appear(self.axes, shift=None), 0.55, 1.0),
                           run_time=2.0)
            self.remove(self.spring)
            self.play(*appear(self.waves.cos, self.key.items[0], self.waves.sin, self.key.items[1],
                              shift=None, lag=0.25), run_time=1.3)

            # the rule is linear
            c.wait_until("linear")
            top = 2.6
            self.play(*during(disappear(*self.alg), 0, 0.45),
                      *during([self.A3.animate.move_to([COLX + self.A3.width / 2, top, 0]),
                               self.a3box.animate.move_to([COLX + self.A3.width / 2, top, 0])],
                              0.35, 0.9),
                      run_time=1.3)
            B0 = MathTex(r"\ddot{x}_1", "=", r"-\omega^2", "x_1", font_size=S)
            B1 = MathTex(r"\ddot{x}_2", "=", r"-\omega^2", "x_2", font_size=S)
            for B in (B0, B1):
                B[0].set_color(RED)
                B[3].set_color(BLUE)
            at_col(B0, 1.6)
            at_col(B1, 1.0)
            k0 = lab_at("two motions that obey", 2.0)
            self.play(*appear(k0, B0, B1, shift=None, lag=0.3), *set_alpha([self.A3, self.a3box], 0.4),
                      run_time=1.4)

            c.wait_until("add multiples")
            B2 = MathTex("a", r"\ddot{x}_1", "+", "b", r"\ddot{x}_2", "=", r"-\omega^2", "(",
                         "a", "x_1", "+", "b", "x_2", ")", font_size=S)
            for i in (1, 4):
                B2[i].set_color(RED)
            for i in (0, 3, 8, 9, 11, 12):
                B2[i].set_color(BLUE)
            at_col(B2, 0.2)
            k2 = lab_at("a × first + b × second", 0.6)
            self.play(*appear(k2, B2, shift=None, lag=0.3), Create(self.waves.sum),
                      *appear(self.key.items[2], shift=None), run_time=1.7)

            c.wait_until("accelerations add")
            B3 = MathTex(r"\tfrac{d^2}{dt^2}", r"(a x_1 + b x_2)", "=", r"-\omega^2",
                         r"(a x_1 + b x_2)", font_size=S)
            B3[0].set_color(RED)
            B3[1].set_color(BLUE)
            B3[4].set_color(BLUE)
            at_col(B3, -0.72)
            k3 = lab_at("the left side is the mix's acceleration", -0.26)
            self.play(*appear(k3, B3, shift=None, lag=0.3), *set_alpha([B0, B1], 0.4),
                      run_time=1.5)
            self.lin = [B0, B1, B2, B3, k0, k2, k3]

            # physically: the pulls add
            c.wait_until("physically")
            self.card = block_card(2.5)
            cx = bc_center(2.5)[0]
            r1, r2, r3 = 2.18, 2.62, 2.92
            p1 = ak.arrow_between([cx, r1, 0], [cx - 0.72, r1, 0], RED, 5, z=0)
            p2 = ak.arrow_between([cx, r2, 0], [cx - 0.48, r2, 0], RED, 5, z=0)
            q1 = MathTex(r"a\ddot{x}_1", font_size=26, color=RED).next_to([cx, r1, 0], RIGHT, buff=0.12)
            q2 = MathTex(r"b\ddot{x}_2", font_size=26, color=RED).next_to([cx, r2, 0], RIGHT, buff=0.12)
            self.play(*appear(self.card, shift=None), GrowArrow(p1), GrowArrow(p2),
                      *appear(q1, q2, shift=None, lag=0.3), run_time=1.4)
            d = np.array([-0.72, r1 - r2, 0])
            p3 = ak.arrow_between([cx, r3, 0], [cx - 1.2, r3, 0], RED, 7, z=0)
            q3 = MathTex(r"\ddot{x}", font_size=28, color=RED).next_to(p3, LEFT, buff=0.12)
            q2b = MathTex(r"b\ddot{x}_2", font_size=26, color=RED)
            q2b.next_to(p2.copy().shift(d), UP, buff=0.06)
            self.play(*during(disappear(q2), 0, 0.3), *during([p2.animate.shift(d)], 0.1, 0.55),
                      *during(appear(q2b, shift=None), 0.5, 0.75),
                      *during([GrowArrow(p3)], 0.55, 1.0), *during(appear(q3, shift=None), 0.7, 1.0),
                      run_time=1.8)
            self.pulls = [p1, p2, p3, q1, q2b, q3]

            # {caption}: x(t) = a cos ωt + b sin ωt
            c.wait_until("caption")
            cap = MathTex("x(t)", "=", "a", r"\cos\omega t", "+", "b", r"\sin\omega t",
                          font_size=40)
            for i in (0, 2, 3, 5, 6):
                cap[i].set_color(BLUE)
            at_col(cap, -1.68)
            capbox = ybox(cap, buff=0.16)
            self.cap, self.capbox = cap, capbox
            self.capt = kit.tag("(81) · notes p. 108")
            self.capt.next_to(capbox, DOWN, buff=0.12, aligned_edge=RIGHT)
            self.play(*appear(cap, shift=None), GrowFromCenter(capbox), *set_alpha([B2], 0.4),
                      run_time=1.5)
            self.play(*appear(self.capt, shift=None), run_time=0.8)
            c.wait_until("cosine coefficient")
            kit.legend_add(self, self.leg, E_A, run_time=1.2,
                           extra=[FlashAround(cap[2], color=YELLOW, time_width=1.5)])
            c.wait_until("plus a sine coefficient")
            kit.legend_add(self, self.leg, E_B, run_time=1.2,
                           extra=[FlashAround(cap[5], color=YELLOW, time_width=1.5)])

            # {shm}: the column makes room; the name
            c.wait_until("shm")
            cap_to = np.array([COLX + capbox.width / 2 - 0.16, 2.6, 0])
            dcap = cap_to - capbox.get_center()
            self.shm = T("simple harmonic motion", size=30, color=YELLOW)
            shm_box = SurroundingRectangle(self.shm, color=YELLOW, buff=0.14).set_stroke(YELLOW, 2.5)
            self.shm_g = VGroup(self.shm, shm_box)
            at_col(self.shm_g, 1.42)
            self.shm_sub = kit.tag("part one: its rule · here: its form")
            self.shm_sub.next_to(self.shm_g, DOWN, buff=0.16, aligned_edge=LEFT)
            self.play(*during(disappear(*self.lin, self.A3, self.a3box, *self.pulls), 0, 0.4),
                      *during([cap.animate.shift(dcap), capbox.animate.shift(dcap),
                               self.capt.animate.shift(dcap)], 0.4, 0.85),
                      *during(appear(self.shm_g, shift=None), 0.8, 1.0), run_time=2.2)
            c.wait_until("part one")
            self.play(*appear(self.shm_sub, shift=None), run_time=0.9)
            c.wait_until("now you have its formula")
            self.play(FlashAround(VGroup(cap, capbox), color=YELLOW, time_width=1.5), run_time=1.5)

            # {sweep}: turn up b
            c.wait_until("sweep")
            dyn = graph_waves(3.0, self.b)
            self.remove(self.waves.cos, self.waves.sin, self.waves.sum)
            self.add(dyn)
            self.waves = dyn
            self.rd = ak._readout(r"b =", lambda: self.b.get_value(), "", BLUE, 32, 2)
            self.rd.move_to([COLX, 0.4, 0], aligned_edge=LEFT)
            self.play(*appear(self.rd, shift=None), self.b.animate.set_value(0.0), run_time=1.2)
            self.b.rate = 4.0 / 6.2
            c.wait_until("keeps its beat")
            if c.remaining > 0.8:
                self.play(VShowPassingFlash(self.axes.period[0].copy().set_stroke(TEAL, 6),
                                            time_width=0.6),
                          FlashAround(self.axes.period[2], color=TEAL, time_width=1.5),
                          run_time=min(1.5, c.remaining - 0.1))

    # ── c2.every.3: what a and b mean; the example ──────────────────────────────
    def clip3(self):
        with self.say("c2.every.3") as c:
            if self.b.rate and self.b.get_value() < 4.0:
                self.wait((4.0 - self.b.get_value()) / self.b.rate + 0.05)
            self.b.rate = 0.0
            self.b.set_value(4.0)
            self.play(*disappear(self.shm_sub, self.rd),
                      FlashAround(self.cap[2], color=YELLOW, time_width=1.5),
                      FlashAround(self.cap[5], color=YELLOW, time_width=1.5), run_time=1.1)

            # {a}
            c.wait_until("a")
            M1 = MathTex("x", "(0)", "=", "a", r"\cdot 1", "+", "b", r"\cdot 0", "=", "a",
                         font_size=S)
            for i in (0, 3, 6, 9):
                M1[i].set_color(BLUE)
            at_col(M1, 0.5)
            m1 = lab_at("cos 0 = 1, sin 0 = 0", 0.88)
            self.play(*appear(m1, M1, shift=None, lag=0.3), run_time=1.4)
            c.wait_until("where the swing starts")
            kit.legend_set(self, self.leg, [ak.E_X, kit.E_XDD, ak.E_W, ak.E_T, E_A, E_B, E_X0],
                           FlashAround(M1[9], color=YELLOW, time_width=1.5), run_time=1.3)

            # {b}
            c.wait_until("b")
            M2 = MathTex(r"\dot{x}", "=", "-a", r"\omega\sin\omega t", "+", "b",
                         r"\omega\cos\omega t", font_size=S)
            M2[0].set_color(GREEN)
            M2[2].set_color(BLUE)
            M2[5].set_color(BLUE)
            at_col(M2, -0.32)
            m2 = lab_at("chain rule", 0.06)
            self.play(*appear(m2, M2, shift=None, lag=0.3), run_time=1.4)
            c.wait_until("times omega")
            M3 = MathTex(r"\dot{x}", "(0)", "=", "b", r"\omega", font_size=S)
            M3[0].set_color(GREEN)
            M3[3].set_color(BLUE)
            at_col(M3, -1.14)
            m3 = lab_at("set t = 0", -0.76)
            self.play(*appear(m3, M3, shift=None, lag=0.3), *set_alpha([M1, m1], 0.4), run_time=1.3)
            c.wait_until("divided by omega")
            M4 = MathTex("a", "=", "x_0", r",\qquad", "b", "=", r"v_0", r"/\omega", font_size=S + 2)
            for i in (0, 2, 4):
                M4[i].set_color(BLUE)
            M4[6].set_color(GREEN)
            at_col(M4, -2.02)
            M4.shift(0.16 * RIGHT)
            m4box = ybox(M4)
            m4 = lab_at("so", -1.56)
            self.play(*appear(m4, M4, shift=None, lag=0.3), time_span(GrowFromCenter(m4box), 0.6, 1.4),
                      run_time=1.4)
            kit.legend_set(self, self.leg,
                           [ak.E_X, kit.E_XD, ak.E_W, ak.E_T, E_A, E_B, E_X0, E_V0], run_time=1.2)

            # {example}: 3 cm out, moving out at 12 cm/s, ω = 3
            c.wait_until("example")
            m4_to = np.array([m4box.get_center()[0], 0.6, 0])
            dm4 = m4_to - m4box.get_center()
            self.play(*during(disappear(M1, M2, M3, m1, m2, m3, m4), 0, 0.4),
                      *during([M4.animate.shift(dm4), m4box.animate.shift(dm4)], 0.35, 0.85),
                      *during([Transform(self.card, block_card(3.0))], 0.2, 0.9), run_time=1.7)
            cx = bc_center(3.0)
            ve = ak.arrow_between(cx + RIGHT * 0.3, cx + RIGHT * 1.15, GREEN, 6, z=0)
            vl = MathTex("v_0", font_size=28, color=GREEN).next_to(ve, UP, buff=0.08)
            G = MathTex("x_0", r"= 3\text{ cm},\quad", "v_0", r"= 12\text{ cm/s},\quad", r"\omega = 3",
                        font_size=30)
            G[0].set_color(BLUE)
            G[2].set_color(GREEN)
            at_col(G, -0.2)
            self.play(GrowArrow(ve), *appear(vl, G, shift=None, lag=0.3), run_time=1.4)

            # {coeffs}
            c.wait_until("coeffs")
            C1 = MathTex("a", "= 3", font_size=S)
            C1[0].set_color(BLUE)
            at_col(C1, -1.02)
            n1 = lab_at("a = x₀", -0.62)
            self.play(*appear(n1, C1, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("twelve over three")
            C2 = MathTex("b", r"= 12/3 = 4", font_size=S)
            C2[0].set_color(BLUE)
            at_col(C2, -1.84)
            n2 = lab_at("b = v₀/ω", -1.44)
            self.play(*appear(n2, C2, shift=None, lag=0.3), *set_alpha([G], 0.4), run_time=1.2)
            c.wait_until("which is four")
            C3 = MathTex("x", "=", r"3\cos 3t", "+", r"4\sin 3t", font_size=S + 4, color=BLUE)
            C3[1].set_color(FG)
            C3[3].set_color(FG)
            at_col(C3, -2.75)
            C3.shift(0.16 * RIGHT)
            c3box = ybox(C3)
            key4 = graph_key("4")
            self.play(*swap(self.key.items[1][1], key4.items[1][1]),
                      *appear(C3, shift=None), time_span(GrowFromCenter(c3box), 0.6, 1.5),
                      VShowPassingFlash(_waves_still(3.0, 4.0).sum.set_stroke(YELLOW, 8),
                                        time_width=0.5),
                      run_time=1.6)
            self.key.items[1].remove(self.key.items[1][1])
            c.wait_until("keep this swing in mind")
            self.play(FlashAround(c3box, color=YELLOW, time_width=1.5), run_time=1.5)
            self.ex = [G, C1, C2, n1, n2]
            self.M4, self.m4box, self.C3, self.c3box = M4, m4box, C3, c3box
            self.ve, self.vl = ve, vl

    # ── c2.every.4: the start decides everything ────────────────────────────────
    def clip4(self):
        with self.say("c2.every.4", gap=2.0) as c:
            c3_to = np.array([self.c3box.get_center()[0], -0.3, 0])
            d = c3_to - self.c3box.get_center()
            self.play(*during(disappear(*self.ex), 0, 0.45),
                      *during([self.C3.animate.shift(d), self.c3box.animate.shift(d)], 0.4, 0.9),
                      run_time=1.4)
            c.wait_until("two numbers match")
            self.play(FlashAround(self.M4[0:3], color=YELLOW, time_width=1.5),
                      FlashAround(self.M4[4:8], color=YELLOW, time_width=1.5), run_time=1.6)

            c.wait_until("fixes the acceleration")
            cx = bc_center(3.0)[0]
            pull = ak.arrow_between([cx, 2.18, 0], [cx - 0.75, 2.18, 0], RED, 6, z=0)
            pl = MathTex(r"\ddot{x}", font_size=28, color=RED).next_to(pull, LEFT, buff=0.12)
            self.play(GrowArrow(pull), *appear(pl, shift=None),
                      FlashAround(self.pin.formula, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("the start decides")
            s1 = T("start position + start velocity", size=30,
                   t2c={"start position": BLUE, "start velocity": GREEN})
            s2 = T("→ everything after", size=30)
            st = VGroup(s1, s2).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            at_col(st, -1.45)
            self.play(*appear(s1, s2, lag=0.4), run_time=1.3)
            c.wait_until("next term")
            proof = kit.tag("proved next term")
            proof.next_to(st, DOWN, buff=0.22, aligned_edge=LEFT)
            self.play(*appear(proof, shift=None), run_time=0.9)

    # ── c2.every.5: think stop T2.3 ─────────────────────────────────────────────
    def clip5(self):
        th0 = 0.1
        P = pen.PIVOT
        pend = pen.pendulum(math.degrees(th0), labels=False, angle=False)
        arc = Arc(radius=2.3, start_angle=-PI / 2, angle=-th0, arc_center=P).set_stroke(BLUE, 8)
        alab = MathTex("x_0", r"= 0.1\text{ rad}", font_size=34, color=BLUE)
        alab.next_to(arc, LEFT, buff=0.3)
        set_backstroke(alab, width=5)
        with self.say("c2.every.5") as c:
            self.wait(max(0.0, c.until("a pendulum", floor=0) - 1.6))
            sweep_clear(self, *appear(pend, shift=None), keep=[self.pin, self.leg], run_time=1.6)
            ak.run(self.t, False)
            c.wait_until("let go from rest")
            self.play(Create(arc), *appear(alab), run_time=1.3)

            c.wait_until("what are its")
            box = kit.think_box("Let go from rest at 0.1 rad.\nCosine coefficient a?\n"
                                "Sine coefficient b?", size=32, pos=np.array([2.7, -2.3, 0]))
            ring = kit.think_ring()
            self.play(*appear(box, shift=None), FadeIn(ring), run_time=1.2)  # early: the question
            self.play(kit.drain(ring, run_time=max(1.0, c.until("ans_a") - 0.2)))

            c.wait_until("ans_a")
            D0 = MathTex("a", "=", "x_0", "=", "0.1", font_size=44)
            for i in (0, 2):
                D0[i].set_color(BLUE)
            at_col(D0, 2.35)
            self.play(*during(disappear(box, ring), 0, 0.45), *during(appear(D0, shift=None), 0.45, 1),
                      run_time=1.5)
            c.wait_until("ans_b")
            D1 = MathTex("b", r"\omega", "=", "v_0", "= 0", r"\quad\Rightarrow\quad", "b", "= 0",
                         font_size=42)
            for i in (0, 6):
                D1[i].set_color(BLUE)
            D1[3].set_color(GREEN)
            at_col(D1, 1.3)
            self.play(*appear(D1, shift=None), run_time=1.3)
            c.wait_until("the swing is")
            D2 = MathTex("x", "=", r"0.1\cos\omega t", font_size=50, color=BLUE)
            D2[1].set_color(FG)
            at_col(D2, 0.1)
            D2.shift(0.16 * RIGHT)
            d2box = ybox(D2, buff=0.16)
            tp = ak.clock(ValueTracker(0.0))
            self.add(tp)
            swing = always_redraw(lambda: pen.pendulum(
                math.degrees(th0 * math.cos(3.13 * tp.get_value())), labels=False, angle=False))
            self.remove(*pend.get_family())
            self.add(swing)
            ak.run(tp, True)
            self.play(*appear(D2, shift=None), GrowFromCenter(d2box), run_time=1.4)
