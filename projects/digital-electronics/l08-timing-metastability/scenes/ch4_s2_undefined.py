"""Chapter 4, scene 2: neither 0 nor 1: the window violated, Q undefined, metastability.
Clips c4.undef.1 – c4.undef.3.

Shots: s1's button_ff() fades back and shrinks to the top-left corner; centre: the slide-p.110
diagram in ch1 s5's data-sheet style (CLK YELLOW, one sloped rising edge; D BLUE; Q GREEN) ->
guides + GOLD t_su / t_hold arrows + GOLD window over all three rows -> D rises inside the window
-> window RED + caption -> RED dashed ghost edge inside t_hold -> "no control" on the button ->
Q clean 0, then drifts to a RED halfway level, "???" -> voltage axis right (0 V, V_DD, GREEN
valid bands, RED invalid band), a dashed line carries Q's level onto it -> Q's corner wire fans to
two gates, "reads 0" / "reads 1" -> "Metastability" in RED above.
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
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# make_ff + push_button + fingertip + button_ff, copied from ch4_s1_hook.py
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


PUSH = 0.18


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.stem, g.cap, g.body = stem, cap, body
    g.plunger = VGroup(stem, cap)
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    g = VGroup(f, nail)
    g.nail = nail
    return g


HERO_FF = _p(0.6, 0.95)
HERO_K = 0.85
BTN_X = -4.0


def button_ff(ff_center=HERO_FF, k=HERO_K, btn_x=BTN_X):
    ff = make_ff().scale(k).move_to(ff_center)
    y = ff.d_w.get_center()[1]
    btn = push_button(_p(btn_x, y))
    wire = Line(btn.out(), ff.d_w.get_left()).set_stroke(BLUE, 5)
    clk_l = T("CLK", 30, YELLOW).next_to(ff.clk_w.get_bottom(), LEFT, buff=0.15).shift(0.12 * UP)
    g = VGroup(wire, ff, btn, clk_l)
    g.ff, g.btn, g.wire, g.clk_l = ff, btn, wire, clk_l
    g.finger = fingertip().shift(btn.cap.get_left())
    return g


CORNER_K = 0.45             # button_ff() shrunk into the top-left corner (to_corner(UL, buff=0.5))
# =============================================================================================


# =============================================================================================
# Data-sheet kit, copied from ch1_s5_datasheet.py (clock_wave, guide, dim_arrow, sweep_in, grow_dim)
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


def grow_dim(arr):
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()
    min_len = 0.4

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        L = a * np.linalg.norm(end - start)
        if L < min_len:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)
# =============================================================================================


# =============================================================================================
# undefined_diagram() + volt_axis(): ch4's metastability diagram (s4 brings it back small at the
# top; the recap tile shows it with the voltage axis). Full size as built here; scale the group.
# =============================================================================================
UX0, UX1 = -5.0, 3.0         # trace span
UXE = -0.6                   # the clock's rising edge
U_TSU, U_THOLD = 1.3, 0.9    # window: t_su before the edge, t_hold after
UXD = UXE - 0.5              # D's 0 -> 1 change, inside t_su
D_SLOPE = 0.2
UY_CLK, UY_D, UY_Q = 1.0, -0.3, -1.6
UQ_MID = UY_Q                # Q's RED halfway level (between its 0 at UY_Q - ROW_H/2 and its 1)
UXQ = UXE + 0.2              # where Q starts to drift
UXQ_FLAT = UXE + 1.4         # where it reaches the halfway level


def undefined_diagram():
    """Slide p.110 in the data-sheet style. Parts: .labs (CLK, D, Q) .clk .d_low .d_rise
    (the rise + high run, swept in after d_low) .q0 (GREEN clean 0 up to the drift) .q_bad (RED
    drift to the halfway level, flat to UX1) .qmark ("???") .guides (t_su start, edge, t_hold end)
    .band (GOLD window over all rows; RED once violated) .su .hold (dim_arrows) .ghost (RED dashed
    D edge inside t_hold). Everything at full size; the scene builds it piece by piece."""
    g = VGroup()
    lab_x = UX0 - 0.55
    labs = VGroup(T("CLK", 36, YELLOW).move_to(_p(lab_x - 0.1, UY_CLK)),
                  T("D", 36, BLUE).move_to(_p(lab_x, UY_D)),
                  T("Q", 36, GREEN).move_to(_p(lab_x, UY_Q)))
    clk = clock_wave(UX0, UX1, UY_CLK, [UXE - 2.6, UXE, UXE + 2.6], start_low=False)
    lo_d, hi_d = UY_D - ROW_H / 2, UY_D + ROW_H / 2
    d_low = Line(_p(UX0, lo_d), _p(UXD - D_SLOPE / 2, lo_d)).set_stroke(BLUE, WAVE_W)
    d_rise = VMobject().set_points_as_corners([_p(UXD - D_SLOPE / 2, lo_d), _p(UXD + D_SLOPE / 2, hi_d),
                                               _p(UX1, hi_d)]).set_stroke(BLUE, WAVE_W)
    lo_q = UY_Q - ROW_H / 2
    q0 = Line(_p(UX0, lo_q), _p(UXQ, lo_q)).set_stroke(GREEN, WAVE_W)
    xs = np.linspace(UXQ, UXQ_FLAT, 24)
    s = (xs - UXQ) / (UXQ_FLAT - UXQ)
    ys = lo_q + (UQ_MID - lo_q) * (s * s * (3 - 2 * s))
    q_bad = VMobject().set_points_as_corners([_p(x, y) for x, y in zip(xs, ys)] + [_p(UX1, UQ_MID)])
    q_bad.set_stroke(RED, WAVE_W)
    qmark = T("???", 40, RED).move_to(_p((UXQ_FLAT + UX1) / 2, UQ_MID + 0.45))
    g_top, g_bot = UY_CLK + ROW_H / 2 + 0.55, UY_Q - ROW_H / 2 - 0.2
    xa, xb = UXE - U_TSU, UXE + U_THOLD
    guides = VGroup(guide(xa, g_top, g_bot), guide(UXE, g_top, g_bot), guide(xb, g_top, g_bot))
    band = Rectangle(width=xb - xa, height=g_top - g_bot - 0.3).set_stroke(width=0)
    band.set_fill(GOLD, 0.22).move_to(_p((xa + xb) / 2, (g_top + g_bot - 0.3) / 2)).set_z_index(-3)
    ya = g_top - 0.05
    su = dim_arrow(xa, UXE, ya, GOLD, r"t_{\mathrm{su}}", size=40)
    hold = dim_arrow(UXE, xb, ya, GOLD, r"t_{\mathrm{hold}}", size=40)
    xg = UXE + 0.45
    ghost_line = VMobject().set_points_as_corners([_p(xg - 0.5, lo_d), _p(xg - D_SLOPE / 2, lo_d),
                                                   _p(xg + D_SLOPE / 2, hi_d), _p(xg + 0.5, hi_d)])
    ghost = DashedVMobject(ghost_line.set_stroke(RED, WAVE_W), num_dashes=12, dashed_ratio=0.55)
    g.add(band, guides, labs, clk, d_low, d_rise, q0, q_bad, qmark, su, hold)
    g.labs, g.clk, g.d_low, g.d_rise, g.q0, g.q_bad, g.qmark = labs, clk, d_low, d_rise, q0, q_bad, qmark
    g.guides, g.band, g.su, g.hold, g.ghost = guides, band, su, hold, ghost
    return g


VA_X = 4.3                   # the voltage axis line
VA_LO, VA_HI = UQ_MID - 1.8, UQ_MID + 1.8    # 0 V and V_DD: centred on Q's halfway level
VA_BAND = 0.8                # height of each valid band


def volt_axis():
    """Vertical voltage axis right of the traces, centred on Q's halfway level. Parts: .axis
    (line + ticks) .lo_l ("0 V") .hi_l (V_DD) .ok0 .ok1 (GREEN valid bands) .ok0_l .ok1_l
    .bad (RED invalid band) .bad_l .level (RED dashed line from Q's flat level to the axis)."""
    g = VGroup()
    line = Line(_p(VA_X, VA_LO), _p(VA_X, VA_HI)).set_stroke(FG, 3)
    ticks = VGroup(*[Line(_p(VA_X - 0.12, y), _p(VA_X + 0.12, y)).set_stroke(FG, 3) for y in (VA_LO, VA_HI)])
    axis = VGroup(line, ticks)
    lo_l = T("0 V", 30).next_to(_p(VA_X - 0.12, VA_LO), LEFT, buff=0.15)
    hi_l = MathTex(r"V_{DD}", font_size=40).next_to(_p(VA_X, VA_HI), UP, buff=0.15)   # above the top tick, clear of D's trace
    bx, bw = VA_X + 0.35, 0.5

    def band(y0, y1, color, op):
        return Rectangle(width=bw, height=y1 - y0).set_stroke(color, 2).set_fill(color, op).move_to(
            _p(bx, (y0 + y1) / 2))

    ok0 = band(VA_LO, VA_LO + VA_BAND, GREEN, 0.45)
    ok1 = band(VA_HI - VA_BAND, VA_HI, GREEN, 0.45)
    bad = band(VA_LO + VA_BAND, VA_HI - VA_BAND, RED, 0.4)
    ok0_l = T("valid 0", 30, GREEN).next_to(ok0, RIGHT, buff=0.2)
    ok1_l = T("valid 1", 30, GREEN).next_to(ok1, RIGHT, buff=0.2)
    bad_l = T("invalid", 30, RED).next_to(bad, RIGHT, buff=0.2)
    level = DashedLine(_p(UX1 + 0.1, UQ_MID), _p(bx - bw / 2 - 0.05, UQ_MID), dash_length=0.12)
    level.set_stroke(RED, 3)
    g.add(axis, lo_l, hi_l, ok0, ok1, bad, ok0_l, ok1_l, bad_l, level)
    g.axis, g.lo_l, g.hi_l, g.ok0, g.ok1, g.bad = axis, lo_l, hi_l, ok0, ok1, bad
    g.ok0_l, g.ok1_l, g.bad_l, g.level = ok0_l, ok1_l, bad_l, level
    return g
# =============================================================================================


def buffer_gate(left, y, color=FG):
    """A small gate (triangle 0.5 x 0.5) with its input at (left, y)."""
    tri = Polygon(_p(left, y + 0.25), _p(left, y - 0.25), _p(left + 0.5, y)).set_stroke(color, 3)
    out = Line(_p(left + 0.5, y), _p(left + 0.75, y)).set_stroke(color, 3)
    return VGroup(tri, out)


class Undefined(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c4.undef.1
    def clip1(self):
        U = self.U = undefined_diagram()
        with self.say("c4.undef.1") as c:
            # {recall}: the circuit returns and shrinks into the corner; the diagram's rows appear
            H = self.H = button_ff()
            self.play(FadeIn(H), run_time=0.8)
            # the corner copy is an icon: its pin labels would be unreadably small, so they go
            small = [H.ff.d_l, H.ff.q_l, H.ff.qb_l, H.clk_l]
            H.generate_target()
            H.target.scale(CORNER_K).to_corner(UL, buff=0.5)
            self.play(MoveToTarget(H), *[FadeOut(m, run_time=0.5) for m in small], run_time=1.3)
            H.ff.remove(H.ff.d_l, H.ff.q_l, H.ff.qb_l)
            H.remove(H.clk_l)
            self.remove(*small)
            self.play(*appear(*U.labs, lag=0.2), sweep_in(U.clk, UX0, UX1),  # early: row names shown with the diagram
                      sweep_in(U.d_low, UX0, UX1), run_time=min(2.0, c.until("window")))
            # {window}: guides + the GOLD window, then t_su and t_hold on their words
            c.wait_until("window")
            self.play(*appear(*U.guides, shift=None, lag=0.15), FadeIn(U.band), run_time=1.2)
            c.wait_until("set-up time")
            self.play(grow_dim(U.su[0]), *appear(U.su[1]), run_time=1.2)
            c.wait_until("hold time")
            self.play(grow_dim(U.hold[0]), *appear(U.hold[1]), run_time=1.2)
            # {change}: D rises inside the window, just before the edge
            c.wait_until("change")
            self.play(sweep_in(U.d_rise, UXD - D_SLOPE, UX1), run_time=1.8)
            self.play(FlashAround(U.d_rise, time_width=1.5, color=BLUE, buff=0.1), run_time=1.5)
            # {violate}: window turns RED, the slide's phrase below
            c.wait_until("violate")
            self.cap = T("“violates the dynamic requirements”", 34, RED)
            self.cap.move_to(_p((UX0 + UX1) / 2, UY_Q - ROW_H / 2 - 0.75))
            self.play(U.band.animate.set_fill(RED, 0.25), *appear(self.cap), run_time=1.4)
            # {hold}: a dashed ghost edge just after the clock edge, inside t_hold; then it fades
            c.wait_until("hold")
            self.play(Create(U.ghost), run_time=1.2)
            c.wait_until("break them too")
            self.play(*disappear(U.ghost), run_time=1.0)
            # {nocontrol}: the button can't be told to wait
            c.wait_until("nocontrol")
            btn = H.btn
            self.tag = T("no control", 30, RED).next_to(btn, DOWN, buff=0.3).align_to(H, LEFT)
            self.play(*appear(self.tag), FlashAround(btn, color=RED, time_width=1.5),  # early: tag on the line about the user
                      run_time=1.5)

    # ------------------------------------------------------------------ c4.undef.2
    def clip2(self):
        U = self.U
        V = self.V = volt_axis()
        with self.say("c4.undef.2") as c:
            # {before}: Q a clean 0 up to the edge (the caption goes: the topic is now Q)
            self.play(*disappear(self.cap), sweep_in(U.q0, UX0, UXQ), run_time=min(1.8, c.until("undefined")))
            # {undefined}: Q drifts to halfway, RED
            c.wait_until("undefined")
            self.play(sweep_in(U.q_bad, UXQ, UX1), run_time=2.2)
            c.wait_until("three question marks")
            self.play(*appear(U.qmark), run_time=1.0)
            # {volts}: the voltage axis
            c.wait_until("volts")
            self.play(GrowFromEdge(V.axis, DOWN), run_time=1.4)
            c.wait_until("valid zero")
            self.play(FadeIn(V.ok0), *appear(V.ok0_l), *appear(V.lo_l), run_time=1.2)
            c.wait_until("valid one")
            self.play(FadeIn(V.ok1), *appear(V.ok1_l), *appear(V.hi_l), run_time=1.2)
            # {invalid}
            c.wait_until("invalid")
            self.play(FadeIn(V.bad), *appear(V.bad_l), run_time=1.2)
            # Q's level carried across: it lands in the RED band
            c.wait_until("for a moment")
            self.play(Create(V.level), run_time=1.5)
            self.play(FlashAround(V.bad, color=RED, time_width=1.5), run_time=1.5)

    # ------------------------------------------------------------------ c4.undef.3
    def clip3(self):
        H = self.H
        with self.say("c4.undef.3", gap=1.2) as c:
            # {confused}: Q's corner wire fans out to two identical gates
            # the fan branches from a dot well out on Q's wire, clear of the Q-bar pin below it
            q_end = H.ff.q_w.get_right()
            qx, qy = q_end[0], q_end[1]
            jx = qx + 0.45
            gl = jx + 0.4
            ya, yb = qy + 0.3, qy - 0.3
            fan = VGroup(Line(q_end, _p(jx, qy)),
                         VMobject().set_points_as_corners([_p(jx, ya), _p(jx, yb)]),
                         Line(_p(jx, ya), _p(gl, ya)), Line(_p(jx, yb), _p(gl, yb)))
            fan.set_stroke(GREEN, 4)
            dot = Dot(_p(jx, qy), radius=0.07, color=GREEN)
            ga, gb = buffer_gate(gl, ya).scale(0.8, about_point=_p(gl, ya)), \
                buffer_gate(gl, yb).scale(0.8, about_point=_p(gl, yb))
            # the arrows go; the band stays put and the guides shrink to its top edge (no stubs above)
            band_top = self.U.band.get_top()[1]
            trims = [g.animate.put_start_and_end_on(_p(g.get_x(), band_top), g.get_end())
                     for g in self.U.guides]
            self.play(Create(fan), FadeIn(dot), *disappear(self.U.su, self.U.hold), *trims, run_time=1.2)
            self.play(FadeIn(ga), FadeIn(gb), run_time=1.0)
            # {gates}: one reads 0, the other 1
            c.wait_until("as a zero")
            r0 = T("reads 0", 30, RED).next_to(ga, RIGHT, buff=0.2)
            self.play(*appear(r0), ga.animate.set_stroke(RED), run_time=1.0)  # early: tag on "as a zero"
            c.wait_until("as a one")
            r1 = T("reads 1", 30, RED).next_to(gb, RIGHT, buff=0.2)
            self.play(*appear(r1), gb.animate.set_stroke(RED), run_time=1.0)  # early: tag on "as a one"
            # {name}
            c.wait_until("name")
            name = T("Metastability", 56, RED).move_to(_p(2.3, 3.2))
            self.play(*appear(name), run_time=1.2)  # early: the name lands as it is said
