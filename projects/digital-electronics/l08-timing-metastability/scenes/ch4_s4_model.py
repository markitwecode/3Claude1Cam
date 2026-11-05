"""Chapter 4, scene 4: how long might it take? The resolution-time model. Clips c4.model.1 – c4.model.4.

Shots: s2's CLK / D / Q diagram (data-sheet style), Q's RED halfway level splits into two GREEN
lines ("0 or 1"), FG t_res dimension arrow from the clock edge, "resolution time"; the split
slides right twice, "no upper limit" -> board clears; the model P(t_res > t) = T_0/T_c e^(-t/tau)
large in the centre, a YELLOW box walks its three parts; T_c YELLOW "clock period"; T_0 and tau
BLUE "characteristics of the flip-flop"; exponent t GOLD "time we can afford to wait" -> formula
to the top, its fraction flashes; a long YELLOW CLK trace with narrow danger zones (T_0 wide) at
every rising edge, T_c arrow; 40 BLUE input changes rain down, 2 land in zones (RED), "≈ 1 in 20";
the period doubles, a fresh shower, 1 RED hit, "≈ 1 in 40" -> the exponential flashes, s3's hill
small below with a RED ball leaving the summit, tag -> formula to the upper left; s5's
decay_graph() at full size (shift 0.2 DOWN, as s5 opens), curve drawn; GOLD step arcs "÷ e" at each
tau, "e ≈ 2.7", "≈ 150× smaller" at 5 tau; the slide's key point inside the empty upper right of
the plot, DIM "derivation: not on the course" bottom left.
"""
# style: 2
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# model_formula(): slide p. 111's resolution-time model, shared with s6 and the recap.
#   MathTex  P(t_{res} > t) = \frac{T_0}{T_c}\, e^{-t/\tau}  (t_res FG, T_c YELLOW).
#   Parts (glyph VGroups, for reading geometry / one recolor per glyph): .lhs (P(t_res > t))
#   .t_res .eq .T0 .bar .Tc .frac (T0, bar, Tc) .exp (e^{-t/tau}) .t_exp (the t in the exponent)
#   .tau. Built centred on ORIGIN.
# =============================================================================================
MODEL_TEX = r"P(t_{res} > t) = \frac{T_0}{T_c}\, e^{-t/\tau}"


def model_formula(size=72):
    f = MathTex(MODEL_TEX, font_size=size, color=FG)
    g = f[0]
    if len(g) != 20:
        raise ValueError(f"model_formula: expected 20 glyphs, got {len(g)}")
    gl = list(g)
    f.lhs, f.t_res, f.eq = VGroup(*gl[0:9]), VGroup(*gl[2:6]), gl[9]
    fr = sorted(gl[10:15], key=lambda m: -m.get_center()[1])
    top, bar, bot = fr[0:2], fr[2], fr[3:5]
    top.sort(key=lambda m: m.get_center()[0])
    bot.sort(key=lambda m: m.get_center()[0])
    f.T0, f.bar, f.Tc = VGroup(*top), bar, VGroup(*bot)
    f.frac = VGroup(*gl[10:15])
    f.exp = VGroup(*gl[15:20])
    f.t_exp, f.tau = gl[17], gl[19]
    f.Tc.set_color(YELLOW)
    f.move_to(ORIGIN)
    return f
# =============================================================================================


# =============================================================================================
# clock_wave / guide / dim_arrow / sweep_in: copied from ch4_s2_undefined.py (ch1 s5's style)
# =============================================================================================
WAVE_W = 4
ROW_H = 0.8
SLOPE = 0.35
GUIDE_W = 1.5
DIM_W = 3


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    wave = VMobject().set_points_as_corners(pts)
    wave.set_stroke(color, WAVE_W)
    return wave


def guide(x, y_top, y_bot):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def sweep_in(group, x0, x1):
    leaves = group.family_members_with_points()
    origs = [m.copy() for m in leaves]

    def upd(_, a):
        X = x0 + a * (x1 - x0)
        for leaf, orig in zip(leaves, origs):
            lx0, lx1 = orig.get_left()[0], orig.get_right()[0]
            if lx1 - lx0 < 1e-6:
                frac = 1.0 if X >= lx0 else 0.0
            else:
                frac = min(1.0, max(0.0, (X - lx0) / (lx1 - lx0)))
            if a >= 1:
                frac = 1.0
            leaf.pointwise_become_partial(orig, 0, frac)
            leaf.set_stroke(opacity=orig.get_stroke_opacity() if frac * (lx1 - lx0) > 0.15 or frac >= 1
                            else 0)

    return UpdateFromAlphaFunc(group, upd)
# =============================================================================================


# =============================================================================================
# s2's undefined_diagram() geometry (ch4_s2_undefined.py), extended right so Q's split can slide.
# Built in s2's full-size coordinates, then scaled by K and shifted to (OX, OY).
# =============================================================================================
UX0 = -5.0
UXE = -0.6
UXD = UXE - 0.5
D_SLOPE = 0.2
UY_CLK, UY_D, UY_Q = 1.0, -0.3, -1.6
UQ_MID = UY_Q
UXQ = UXE + 0.2
UXQ_FLAT = UXE + 1.4
X_END = 5.0                          # traces run further right than s2's 3.0
XS0, XS1, XS2 = 1.6, 2.8, 4.0        # the split point: first, then slid right twice
SPLIT = 0.35
K, OX, OY = 0.85, 0.2, 1.5


def sx(x):
    return K * x + OX


def sy(y):
    return K * y + OY


def tf(m):
    return m.scale(K, about_point=ORIGIN).shift(_p(OX, OY))


def resolve_diagram():
    """s2's labels and traces (CLK, D rising inside the window, Q drifting to its RED halfway
    level), extended to X_END. Parts: .labs .clk .d (low + rise) .q0 .drift."""
    g = VGroup()
    lab_x = UX0 - 0.55
    labs = VGroup(T("CLK", 36, YELLOW).move_to(_p(lab_x - 0.1, UY_CLK)),
                  T("D", 36, BLUE).move_to(_p(lab_x, UY_D)),
                  T("Q", 36, GREEN).move_to(_p(lab_x, UY_Q)))
    clk = clock_wave(UX0, X_END, UY_CLK, [UXE - 2.6, UXE, UXE + 2.6, UXE + 5.2], start_low=False)
    lo_d, hi_d = UY_D - ROW_H / 2, UY_D + ROW_H / 2
    d = VMobject().set_points_as_corners([_p(UX0, lo_d), _p(UXD - D_SLOPE / 2, lo_d),
                                          _p(UXD + D_SLOPE / 2, hi_d), _p(X_END, hi_d)])
    d.set_stroke(BLUE, WAVE_W)
    lo_q = UY_Q - ROW_H / 2
    q0 = Line(_p(UX0, lo_q), _p(UXQ, lo_q)).set_stroke(GREEN, WAVE_W)
    xs = np.linspace(UXQ, UXQ_FLAT, 24)
    s = (xs - UXQ) / (UXQ_FLAT - UXQ)
    ys = lo_q + (UQ_MID - lo_q) * (s * s * (3 - 2 * s))
    drift = VMobject().set_points_as_corners([_p(x, y) for x, y in zip(xs, ys)]).set_stroke(RED, WAVE_W)
    g.add(labs, clk, d, q0, drift)
    g.labs, g.clk, g.d, g.q0, g.drift = labs, clk, d, q0, drift
    return tf(g)


def red_flat(xs):
    return tf(Line(_p(UXQ_FLAT, UQ_MID), _p(max(xs, UXQ_FLAT + 0.02), UQ_MID)).set_stroke(RED, WAVE_W))


def split_lines(xs, frac=1.0):
    """Q resolves at xs: two parallel GREEN lines (0 or 1) leave the halfway level."""
    hi, lo = UQ_MID + ROW_H / 2, UQ_MID - ROW_H / 2
    g = VGroup()
    for y in (hi, lo):
        full = VMobject().set_points_as_corners([_p(xs, UQ_MID), _p(xs + SPLIT, y), _p(X_END, y)])
        full.set_stroke(GREEN, WAVE_W)
        part = full.copy()
        if frac < 1:
            part.pointwise_become_partial(full, 0, max(frac, 1e-3))
            if frac < 0.02:
                part.set_stroke(opacity=0)
        g.add(part)
    return tf(g)


YA = sy(UY_Q - ROW_H / 2) - 0.45    # the t_res arrow's row (screen)


def tres_arrow(xs):
    return DoubleArrow(_p(sx(UXE), YA), _p(sx(xs), YA), buff=0, stroke_width=DIM_W, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.4, color=FG)
# =============================================================================================


# =============================================================================================
# The long clock with danger zones (clip 3) and s3's hill (clip 4)
# =============================================================================================
TY = -0.1                    # trace centre
TX0, TX1 = -5.2, 6.6
PER = 2.4
ZONE = PER / 20             # T_0: a twentieth of the period
EDGES1 = [0.5 + PER * k for k in range(-2, 3)]          # -4.3 -1.9 0.5 2.9 5.3
EDGES2 = [0.5 + 2 * PER * k for k in range(-1, 2)]      # -4.3 0.5 5.3
CLK_SLOPE = 0.06


def long_clock(per):
    edges = []
    x = 0.5
    while x - per >= TX0:
        x -= per
    while x <= TX1:
        edges += [x, x + per / 2]
        x += per
    edges = [e for e in edges if TX0 < e < TX1]
    return clock_wave(TX0, TX1, TY, edges, slope=CLK_SLOPE, start_low=True)


def zone(x):
    r = Rectangle(width=ZONE, height=1.3).set_stroke(FG, 1.5).set_fill(RED, 0.3)
    return r.move_to(_p(x, TY)).set_z_index(-1)


def tick(x):
    return Line(_p(x, TY - 0.65), _p(x, TY + 0.05)).set_stroke(BLUE, 4)


def hit_anims(ticks, drops):
    """Misses dim; hits turn RED and stand taller, with a RED flash."""
    out = []
    for t, (x, h) in zip(ticks, drops):
        if h:
            out += [t.animate.put_start_and_end_on(_p(x, TY - 0.8), _p(x, TY + 0.8)).set_color(RED),
                    FlashAround(Line(_p(x, TY - 0.8), _p(x, TY + 0.8)), color=RED, time_width=1.5)]
        else:
            out += set_alpha([t], 0.35)
    return out


def shower(edges, hits, seed, n=40):
    """n tick x-positions: `hits` inside zones, the rest clear of every zone."""
    rng = random.Random(seed)
    xs = []
    while len(xs) < n - len(hits):
        x = rng.uniform(TX0 + 0.15, TX1 - 0.15)
        if all(abs(x - e) > ZONE / 2 + 0.12 for e in edges):
            xs.append(x)
    order = [(x, False) for x in xs] + [(x, True) for x in hits]
    rng.shuffle(order)
    return order


U_END = 1.42


def _f(u):
    return (u * u - 1.0) ** 2


class Hill(VGroup):
    """s3's hill (ch4_s3_ball.py), labels left off."""

    def __init__(self, xs=3.0, ys=2.5, color=BLUE, width=6):
        super().__init__()
        self.curve = ParametricFunction(lambda u: _p(u * xs, _f(u) * ys), t_range=(-U_END, U_END, 0.01))
        self.curve.set_stroke(color, width)
        self._o, self._ux, self._uy = VectorizedPoint(ORIGIN), VectorizedPoint(_p(xs, 0)), VectorizedPoint(_p(0, ys))
        self.add(self.curve, self._o, self._ux, self._uy)

    def point(self, u):
        o = self._o.get_center()
        return o + u * (self._ux.get_center() - o) + _f(u) * (self._uy.get_center() - o)

    def ball_point(self, u, r):
        t = self.point(u + 1e-3) - self.point(u - 1e-3)
        n = np.array([-t[1], t[0], 0.0])
        return self.point(u) + r * n / np.linalg.norm(n)


def ball(color=RED, r=0.3):
    b = Circle(radius=r).set_stroke(width=0).set_fill(color, 1)
    b.r = r
    return b


def place(b, h, u):
    return b.move_to(h.ball_point(u, b.r))
# =============================================================================================


# =============================================================================================
# decay_graph(): copied from ch4_s5_synchroniser.py (s5 opens on it, full size, shift 0.2 DOWN)
# =============================================================================================
def decay_graph(width=8.0, height=4.2):
    """FG axes, x "t" with ticks tau..5tau, y "P(t_res > t)", RED curve falling from T_0/T_c.
    Built centred on ORIGIN. Parts: .ax .curve .labels"""
    ax = Axes(x_range=[0, 5.6, 1], y_range=[0, 1.1, 1], x_length=width, y_length=height, tips=False,
              axis_config={"color": FG, "stroke_width": 3, "include_ticks": False})
    ticks = VGroup()
    tlabels = VGroup()
    for i in range(1, 6):
        pt = ax.c2p(i, 0)
        ticks.add(Line(pt + 0.1 * DOWN, pt + 0.1 * UP).set_stroke(FG, 3))
        tlabels.add(MathTex(r"\tau" if i == 1 else rf"{i}\tau", font_size=40, color=FG)
                    .next_to(pt, DOWN, buff=0.2))
    y0 = 0.9
    ytick = Line(ax.c2p(0, y0) + 0.1 * LEFT, ax.c2p(0, y0) + 0.1 * RIGHT).set_stroke(FG, 3)
    ylab0 = MathTex(r"T_0/T_c", font_size=40, color=RED).next_to(ax.c2p(0, y0), LEFT, buff=0.2)
    xl = MathTex("t", font_size=44, color=FG).next_to(ax.c2p(5.6, 0), RIGHT, buff=0.2)
    yl = MathTex(r"P(t_{res} > t)", font_size=44, color=FG).next_to(ax.c2p(0, 1.1), UP, buff=0.2)
    curve = ax.plot(lambda t: y0 * np.exp(-t), x_range=[0, 5.5]).set_stroke(RED, 5)
    g = VGroup(ax, ticks, ytick, curve, tlabels, ylab0, xl, yl)
    g.ax, g.curve = ax, curve
    g.labels = VGroup(tlabels, ylab0, xl, yl)
    g.move_to(ORIGIN)
    return g
# =============================================================================================


class Model(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c4.model.1
    def clip1(self):
        Dg = resolve_diagram()
        xs_t = ValueTracker(XS0)
        fr_t = ValueTracker(0.0)
        with self.say("c4.model.1", gap=0.8) as c:
            # {resolve}: s2's diagram returns; Q sits at its RED halfway level
            flat0 = red_flat(XS0)
            self.play(*appear(*Dg.labs, lag=0.15),  # early: row names come with the diagram
                      sweep_in(VGroup(Dg.clk, Dg.d, Dg.q0, Dg.drift, flat0), sx(UX0), sx(X_END)),
                      run_time=min(2.0, c.until("valid")))
            self.remove(flat0)
            red = always_redraw(lambda: red_flat(xs_t.get_value()))
            grn = always_redraw(lambda: split_lines(xs_t.get_value(), fr_t.get_value()))
            self.add(red, grn)
            # ... and settles: two GREEN lines, 0 or 1
            c.wait_until("valid")
            orone = T("0 or 1", 32, GREEN).next_to(_p(sx(X_END), sy(UQ_MID)), RIGHT, buff=0.25)
            self.play(fr_t.animate.set_value(1.0), run_time=1.2)
            c.wait_until("zero")
            self.play(*appear(orone), run_time=0.9)  # early: on "zero or one"
            # the resolution time: edge guide, t_res arrow, its name
            c.wait_until("resolution time")
            gd = guide(sx(UXE), sy(UY_CLK + ROW_H / 2 + 0.3), YA - 0.15)
            arr = always_redraw(lambda: tres_arrow(xs_t.get_value()))
            tres = MathTex(r"t_{res}", font_size=44, color=FG).next_to(tres_arrow(XS0), DOWN, buff=0.15)
            rt = T("resolution time", 32).next_to(tres, DOWN, buff=0.15)
            self.play(FadeIn(gd), FadeIn(arr), *appear(tres, rt, lag=0.3), run_time=1.3)
            tres.add_updater(lambda m: m.next_to(arr, DOWN, buff=0.15))
            rt.add_updater(lambda m: m.next_to(tres, DOWN, buff=0.15))
            # {unbounded}: the split slides right, and right again
            c.wait_until("unbounded")
            self.play(xs_t.animate.set_value(XS1), run_time=1.5)
            nul = T("no upper limit", 40, RED).move_to(_p(sx(1.0), -2.6))
            c.wait_until(own_word=nul)
            self.play(xs_t.animate.set_value(XS2), *appear(nul), run_time=1.6)
            for m in (red, grn, arr, tres, rt):
                m.clear_updaters()

    # ------------------------------------------------------------------ c4.model.2
    def clip2(self):
        F = self.F = model_formula(84).move_to(_p(0, 0.3))
        F.Tc.set_color(FG)
        with self.say("c4.model.2") as c:
            # {model}: the board clears, the formula arrives large
            sweep_clear(self, FadeIn(F), run_time=min(1.4, c.until("the probability")))
            # walk it: one box slides from part to part
            c.wait_until("the probability")
            box = token_box(F.lhs, F)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("equals")
            self.play(Transform(box, token_box(F.frac, F)), run_time=1.0)
            c.wait_until("times the exponential")
            self.play(Transform(box, token_box(F.exp, F)), run_time=1.0)
            # {tc}: T_c lights YELLOW
            c.wait_until("tc")
            cp = T("clock period", 32, YELLOW).next_to(F.Tc, DOWN, buff=0.35)
            self.play(FadeOut(box), *recolor(F.Tc, YELLOW), *appear(cp), run_time=1.2)  # early: on "clock period"
            # {consts}: T_0 and tau together, BLUE
            c.wait_until("consts")
            self.play(*recolor(F.T0, BLUE), *recolor([F.tau], BLUE),
                      FlashAround(F.T0, color=BLUE, time_width=1.5), FlashAround(F.tau, color=BLUE, time_width=1.5),
                      run_time=1.4)
            ch = T("characteristics of the flip-flop", 34, BLUE).move_to(_p(0, -2.3))
            c.wait_until(own_word=ch)
            self.play(*appear(ch), run_time=1.0)
            # {afford}: the t in the exponent
            c.wait_until("afford")
            tag = label_pointer("time we can afford to wait", F.t_exp, UP, color=GOLD, size=32)
            # no ring round the lone glyph (it crossed the minus and slash): the colour change and the tag
            self.play(*recolor([F.t_exp], GOLD), *appear(tag), run_time=min(1.4, c.until()))  # early: tag on "afford to wait"
            self.cp, self.ch, self.tag = cp, ch, tag

    # ------------------------------------------------------------------ c4.model.3
    def clip3(self):
        F = self.F
        with self.say("c4.model.3", gap=0.6) as c:
            # {bad}: the fraction glows
            box = token_box(F.frac, F)
            self.play(FadeIn(box), FlashAround(F.frac, time_width=1.5, color=YELLOW), run_time=1.6)
            # formula to the top; a long clock, a danger zone at every rising edge
            c.wait_until("picture")
            F.generate_target()
            F.target.scale(0.65).move_to(_p(0, 3.05))
            clk = long_clock(PER)
            clk_l = T("CLK", 36, YELLOW).next_to(_p(TX0, TY), LEFT, buff=0.2)
            self.play(*during(disappear(self.cp, self.ch, self.tag, box), 0, 0.3), *during([MoveToTarget(F)], 0.3, 0.75),
                      *during(appear(clk_l, shift=None), 0.5, 1), *during([sweep_in(clk, TX0, TX1)], 0.4, 1),
                      run_time=min(2.2, c.until("danger zone") + 0.6))  # early: row name with its trace
            c.wait_until("danger zone")
            zones = [zone(x) for x in EDGES1]
            self.play(*[FadeIn(z) for z in zones], run_time=1.0)
            # T_0 on the central zone
            c.wait_until("wide")
            z0 = EDGES1[2]
            yb = TY - 0.95
            t0g = VGroup(guide(z0 - ZONE / 2, TY - 0.65, yb - 0.1), guide(z0 + ZONE / 2, TY - 0.65, yb - 0.1))
            t0a = VGroup(Arrow(_p(z0 - ZONE / 2 - 0.55, yb), _p(z0 - ZONE / 2, yb), buff=0, stroke_width=DIM_W,
                               tip_length=0.15, max_tip_length_to_length_ratio=0.4, color=FG),
                         Arrow(_p(z0 + ZONE / 2 + 0.55, yb), _p(z0 + ZONE / 2, yb), buff=0, stroke_width=DIM_W,
                               tip_length=0.15, max_tip_length_to_length_ratio=0.4, color=FG))
            t0l = MathTex("T_0", font_size=44, color=FG).next_to(_p(z0, yb), DOWN, buff=0.2)
            self.play(FadeIn(t0g), FadeIn(t0a), *appear(t0l), run_time=1.0)
            # one period: T_c
            c.wait_until("rising edge")
            tc = dim_arrow(EDGES1[2], EDGES1[3], TY + 0.95, YELLOW, "T_c")
            self.play(FadeIn(tc[0]), *appear(tc[1]), run_time=1.0)  # early: the period on "every rising edge of the clock"
            # {rain}: 40 input changes at random moments
            c.wait_until("rain")
            drops = shower(EDGES1, [EDGES1[1] + 0.02, EDGES1[3] - 0.025], seed=8)
            ticks = [tick(x) for x, _ in drops]
            self.play(LaggedStart(*[FadeIn(t, shift=0.45 * DOWN) for t in ticks], lag_ratio=0.12),
                      run_time=min(4.0, c.until("if each zone") - 0.3), rate_func=linear)
            self.play(*hit_anims(ticks, drops), run_time=1.4)
            c.wait_until("one change in twenty")
            t20 = T("≈ 1 in 20", 40).move_to(_p(z0, -2.4))
            self.play(*appear(t20), run_time=1.0)
            # {slower}: the period doubles, the zones spread out, a fresh shower
            c.wait_until("slower")
            rem = c.until() + 0.5
            # the trace stretches about the central rising edge: zones and T_c ride their rising edges
            per_t = ValueTracker(PER)
            ks = [round((x - 0.5) / PER) for x in EDGES1]
            clk.add_updater(lambda m: m.become(long_clock(per_t.get_value())))
            for i in (0, 1):
                tc[i].add_updater(lambda m, i=i: m.become(
                    dim_arrow(0.5, 0.5 + per_t.get_value(), TY + 0.95, YELLOW, "T_c")[i]))
            outer = [z for z, k in zip(zones, ks) if abs(k) == 2]     # pushed off-screen: fade them first
            for z, k in zip(zones, ks):
                if abs(k) < 2:
                    z.add_updater(lambda m, k=k: m.move_to(_p(0.5 + k * per_t.get_value(), TY)))
            self.play(*during(disappear(*ticks, *outer), 0, 0.4), *during([per_t.animate.set_value(2 * PER)], 0.25, 1),
                      run_time=min(1.8, 0.32 * rem))
            for m in [clk, tc[0], tc[1], *zones]:
                m.clear_updaters()
            drops2 = shower(EDGES2, [EDGES2[2] - 0.02], seed=5)
            ticks2 = [tick(x) for x, _ in drops2]
            self.play(LaggedStart(*[FadeIn(t, shift=0.45 * DOWN) for t in ticks2], lag_ratio=0.1),
                      run_time=min(1.4, 0.27 * rem), rate_func=linear)
            t40 = T("≈ 1 in 40", 40).move_to(t20)
            self.play(*hit_anims(ticks2, drops2), *swap(t20, t40), run_time=min(1.2, 0.25 * rem))

    # ------------------------------------------------------------------ c4.model.4
    def clip4(self):
        F = self.F
        with self.say("c4.model.4", gap=3.5) as c:
            # {tau}: the exponential glows
            self.play(FlashAround(F.exp, time_width=1.5, color=YELLOW), run_time=min(1.8, c.until("it says")))
            # s3's hill, small, the ball leaving the summit
            c.wait_until("it says")
            H = Hill(xs=2.0, ys=1.5, width=5).shift(_p(0, -1.0))
            b = place(ball(RED, 0.2), H, 0.03)
            tag = T("τ: how fast it leaves the summit", 36).move_to(_p(0, -2.15))
            board = [m for m in self.mobjects if m is not F]     # trace, zones, ticks, tally: all go together
            self.play(*during(disappear(*board), 0, 0.45), *during([FadeIn(H), FadeIn(b)], 0.5, 1),
                      *during(appear(tag), 0.55, 1), run_time=1.5)
            roll = UpdateFromAlphaFunc(b, lambda m, a: place(m, H, min(1.0, 0.03 * (1 / 0.03) ** a)),
                                       rate_func=linear)
            self.play(roll, run_time=min(2.0, c.until("curve")))
            # {curve}: formula to the upper left, the axes, the curve
            c.wait_until("curve")
            G = decay_graph().shift(0.2 * DOWN)
            ax, ticks, ytick, curve, tl, ylab0, xl, yl = G
            tw = T("time waited", 28, DIM).next_to(tl, DOWN, buff=0.15).align_to(xl, RIGHT)
            F.generate_target()
            F.target.scale(0.7).to_corner(UL, buff=0.4)
            self.play(*during(disappear(H, b, tag), 0, 0.5), MoveToTarget(F), run_time=1.3)
            self.play(FadeIn(ax), FadeIn(ticks), FadeIn(ytick),
                      *appear(yl, xl, tw, tl, ylab0, lag=0.12), run_time=1.3)  # early: axis labels with the axes
            self.play(Create(curve), run_time=min(2.0, c.until("divide")))
            # {divide}: every tau divides by e
            c.wait_until("divides")

            def P(t):
                return ax.c2p(t, 0.9 * np.exp(-t))

            arcs, divs = [], []
            for i in range(1, 6):
                a = CurvedArrow(P(i - 1) + (0.3 * UP + 0.3 * RIGHT if i == 1 else 0.2 * UP + 0.1 * RIGHT),
                                P(i) + 0.22 * UP, angle=-0.9 if i == 1 else -0.6,
                                color=GOLD, stroke_width=3, tip_length=0.15)
                mid = a.point_from_proportion(0.5)
                d = MathTex(r"\div e", font_size=36, color=GOLD).next_to(mid, UR if i == 1 else UP, buff=0.1)
                arcs.append(a)
                divs.append(d)
            self.play(Create(arcs[0]), *appear(divs[0]), run_time=1.5)
            self.play(LaggedStart(*[AnimationGroup(Create(a), FadeIn(d)) for a, d in zip(arcs[1:], divs[1:])],
                                  lag_ratio=0.5), run_time=min(2.4, c.until("two point seven")))  # early: one per step
            c.wait_until("two point seven")
            e27 = MathTex(r"e \approx 2.7", font_size=40, color=GOLD).next_to(divs[0], RIGHT, buff=0.4)
            self.play(*appear(e27), run_time=0.9)
            # {five}: 5 tau
            c.wait_until("five")
            small = T("≈ 150× smaller", 34, GOLD).next_to(divs[4], UP, buff=0.3)
            if small.get_right()[0] > 6.6:
                small.shift((6.6 - small.get_right()[0]) * RIGHT)
            self.play(FlashAround(tl[4], color=GOLD, time_width=1.5), *appear(small), run_time=1.3)  # early: on "five tau"
            # {key}: the slide's key point, in the plot's empty upper right
            c.wait_until("key")
            key = T("the longer we wait,\nthe lower the probability\nof a metastable output", 32,
                    line_spacing=0.9).move_to(ax.c2p(3.75, 0.85))
            self.play(*disappear(e27), *during(appear(key), 0.3, 1), run_time=1.4)  # early: key point read whole
            note = T("derivation: not on the course", 28, DIM).to_corner(DL, buff=0.5)
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.0)
