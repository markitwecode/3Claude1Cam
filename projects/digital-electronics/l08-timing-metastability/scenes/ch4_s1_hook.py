"""Chapter 4, scene 1: hook: a push-button on D, presses land anywhere, one lands in the window.
Clips c4.hook.1 – c4.hook.2.

Shots: title card -> ch3's split-clock path small in the upper left (GOLD window on D1, GREEN tick,
"our own signals: we choose when they change") -> it shrinks and dims into the corner; hero:
button_ff() at centre (button far left wired to D), two scrolling data-sheet traces below
(CLK YELLOW sloped, D BLUE drawn up to a DIM "now" line, GOLD window round every rising edge)
-> a fingertip presses (D up, GREEN tick), lets go (D down, tick), presses again inside a
window: the window turns RED, scrolling stops -> lecturer's quote upper right -> all dims but
the RED window and D's edge in it; the circuit clears, the traces rise, the YELLOW question above
-> the three-chip road along the bottom, "metastability" lit YELLOW.
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# make_ff + path_diagram + split_path, copied from ch3_s2_skew.py
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


P_FF_X = (-4.4, 4.4)
P_FF_Y = 0.5
P_PIN = P_FF_Y + PIN_Y                       # 1.1
P_BUS = P_FF_Y - BOX_H / 2 - EN_WIRE         # -1.8
P_BUS_X0 = -5.6
P_CL_W, P_CL_H = 3.4, 1.6


def path_diagram():
    P = VGroup()
    ffs = []
    for x in P_FF_X:
        f = make_ff(_p(x, P_FF_Y))
        f.remove(f.clk_w)
        ffs.append(f)
    P.ff0, P.ff1 = ffs
    P.names = [T(f"FF{i}", 36, FG).next_to(f.box, UP, buff=0.2) for i, f in enumerate(ffs)]
    x_q0 = P_FF_X[0] + BOX_W / 2 + WIRE
    x_d1 = P_FF_X[1] - BOX_W / 2 - WIRE
    P.cl = Rectangle(width=P_CL_W, height=P_CL_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(0, P_PIN))
    P.cl_l = VGroup(T("Combinational", 32, BLUE), T("Logic (CL)", 32, BLUE)).arrange(DOWN, buff=0.12).move_to(P.cl)
    P.q0_w = Line(_p(x_q0, P_PIN), _p(-P_CL_W / 2, P_PIN)).set_stroke(GREEN, 5)
    P.d1_w = Line(_p(P_CL_W / 2, P_PIN), _p(x_d1, P_PIN)).set_stroke(BLUE, 5)
    P.q0_l = MathTex("Q_0", font_size=40, color=GREEN).next_to(_p(x_q0, P_PIN), UP, buff=0.15)
    P.d1_l = MathTex("D_1", font_size=40, color=BLUE).next_to(_p(x_d1, P_PIN), UP, buff=0.15)
    P.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(P.ff0.d_w, LEFT, buff=0.12)
    P.q1_l = MathTex("Q_1", font_size=40, color=GREEN).next_to(P.ff1.q_w, RIGHT, buff=0.12)
    P.clk_bus = Line(_p(P_BUS_X0, P_BUS), _p(P_FF_X[1], P_BUS)).set_stroke(YELLOW, 5)
    P.clk_dot = Dot(_p(P_FF_X[0], P_BUS), radius=0.08, color=YELLOW)
    P.clk_l = T("CLK", 34, YELLOW).next_to(_p(P_BUS_X0, P_BUS), LEFT, buff=0.15)
    P.clk_br0, P.clk_br1 = ffs[0].clk_w, ffs[1].clk_w
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1]
    P.add(*P.all)
    return P


SRC_X, SRC_R = 6.25, 0.3
LONG_Y = -2.55
TRI_Y = P_FF_Y - BOX_H / 2 - 0.02
CLK1_OP = 0.55


def split_path():
    P = path_diagram()
    P.remove(P.clk_bus, P.clk_dot, P.clk_l, P.clk_br0, P.clk_br1)
    ring = Circle(radius=SRC_R).set_stroke(YELLOW, 4).set_fill(BG, 1)
    sq = VMobject().set_points_as_corners([_p(-0.17, -0.08), _p(-0.08, -0.08), _p(-0.08, 0.08),
                                           _p(0.04, 0.08), _p(0.04, -0.08), _p(0.17, -0.08)])
    sq.set_stroke(YELLOW, 3)
    P.src = VGroup(ring, sq).move_to(_p(SRC_X, P_BUS))
    x0, x1 = P_FF_X
    P.clk_br1 = VMobject().set_points_as_corners([_p(SRC_X - SRC_R, P_BUS), _p(x1, P_BUS), _p(x1, TRI_Y)])
    P.clk_br1.set_stroke(YELLOW, 5, opacity=CLK1_OP)
    P.clk_br0 = VMobject().set_points_as_corners([_p(SRC_X, P_BUS - SRC_R), _p(SRC_X, LONG_Y),
                                                  _p(x0, LONG_Y), _p(x0, TRI_Y)])
    P.clk_br0.set_stroke(YELLOW, 5)
    P.clk0_l = T("CLK0", 34, YELLOW).next_to(_p(-1.6, LONG_Y), DOWN, buff=0.15)
    P.clk1_l = T("CLK1", 34, YELLOW).next_to(_p((x1 + SRC_X - SRC_R) / 2 + 0.05, P_BUS), UP, buff=0.15)
    P.clk1_l.set_opacity(0.7)
    P.all = [P.ff0, P.ff1, *P.names, P.cl, P.cl_l, P.q0_w, P.q0_l, P.d1_w, P.d1_l, P.d0_l, P.q1_l,
             P.clk_br0, P.clk_br1, P.src, P.clk0_l, P.clk1_l]
    P.add(P.clk_br0, P.clk_br1, P.src, P.clk0_l, P.clk1_l)
    return P
# =============================================================================================


# =============================================================================================
# push_button() + button_ff(): ch4's hero circuit. ch4 s2 (shrunk to its corner), s5 (button on
# D0) and the recap copy this block verbatim.
# =============================================================================================
PUSH = 0.18          # how far the plunger (and the finger on it) travels when pressed


def push_button(center=ORIGIN):
    """Side view of a push-button: a housing (.body) with a plunger (.plunger = stem + cap)
    sticking out to the left. Press: shift .plunger (and .finger) by PUSH * RIGHT.
    .out() = the right edge of the housing, where the D wire leaves."""
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)            # body last: it hides the stem when pushed in
    g.stem, g.cap, g.body = stem, cap, body
    g.plunger = VGroup(stem, cap)
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    """A fingertip pointing right, its tip at the local origin; .nail."""
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    g = VGroup(f, nail)
    g.nail = nail
    return g


HERO_FF = _p(0.6, 0.95)     # centre of the hero flip-flop
HERO_K = 0.85               # its scale
BTN_X = -4.0                # the button's housing centre


def button_ff(ff_center=HERO_FF, k=HERO_K, btn_x=BTN_X):
    """L6 make_ff() scaled by k at ff_center, a push_button() at btn_x on the D row wired to D
    (BLUE), CLK (YELLOW) in from below with its label. Parts: .ff .btn .wire .clk_l .finger
    (fingertip resting on the cap, not in the group: add it when a finger is wanted)."""
    ff = make_ff().scale(k).move_to(ff_center)
    y = ff.d_w.get_center()[1]
    btn = push_button(_p(btn_x, y))
    wire = Line(btn.out(), ff.d_w.get_left()).set_stroke(BLUE, 5)
    clk_l = T("CLK", 30, YELLOW).next_to(ff.clk_w.get_bottom(), LEFT, buff=0.15).shift(0.12 * UP)
    g = VGroup(wire, ff, btn, clk_l)
    g.ff, g.btn, g.wire, g.clk_l = ff, btn, wire, clk_l
    g.finger = fingertip().shift(btn.cap.get_left())
    return g
# =============================================================================================


# ---------------------------------------------------------------------------------------------
# Scrolling data-sheet traces (ch1_s5's look: sloped CLK edges, stroke 4, DIM guides; drawn by
# clipped polylines so they can scroll). x_now = the world time sitting on the "now" line.
# ---------------------------------------------------------------------------------------------
PER = 2.4                    # clock period, in x units
SU, HO = 0.6, 0.4            # set-up before / hold after each rising edge (the GOLD window)
XA, XB, NOW_X = -4.8, 6.4, 2.6
Y_CLK, Y_D = -1.7, -3.0
ROW = 0.7
SLOPE = 0.35
D_SLOPE = 0.16
WAVE_W = 4
WIN_H = ROW + 0.25


def clip_poly(pts, xa, xb):
    out = []
    for a, b in zip(pts[:-1], pts[1:]):
        ax, bx = a[0], b[0]
        if bx - ax < 1e-9:
            if xa <= ax <= xb:
                seg = [a, b]
            else:
                continue
        else:
            t0 = max(0.0, (xa - ax) / (bx - ax))
            t1 = min(1.0, (xb - ax) / (bx - ax))
            if t1 <= t0:
                continue
            seg = [a + t0 * (b - a), a + t1 * (b - a)]
        for p in seg:
            if not out or np.linalg.norm(out[-1] - p) > 1e-6:
                out.append(p)
    return out


def poly(pts, color, width=WAVE_W):
    m = VMobject()
    if len(pts) >= 2:
        m.set_points_as_corners(pts)
    else:
        m.set_points_as_corners([_p(XA, Y_D), _p(XA, Y_D)])
    return m.set_stroke(color, width)


def sx(w, x_now):
    return w - x_now + NOW_X


def clk_trace(x_now):
    lo, hi = Y_CLK - ROW / 2, Y_CLK + ROW / 2
    wl, wr = x_now - (NOW_X - XA) - 1, x_now + (XB - NOW_X) + 1
    k0 = int(np.floor(wl / PER)) - 1
    edges = []
    for k in range(k0, k0 + 12):
        for e, up in ((k * PER, True), (k * PER + PER / 2, False)):
            if wl < e < wr:
                edges.append((e, up))
    first_up = edges[0][1]
    level = lo if first_up else hi
    pts = [_p(sx(wl, x_now), level)]
    for e, up in edges:
        other = hi if up else lo
        pts.append(_p(sx(e, x_now) - SLOPE / 2, level))
        pts.append(_p(sx(e, x_now) + SLOPE / 2, other))
        level = other
    pts.append(_p(sx(wr, x_now), level))
    return poly(clip_poly(pts, XA, XB), YELLOW)


def d_trace(x_now, steps, xa=XA, xb=NOW_X, color=BLUE):
    """steps: [(world x, level 0/1)], sorted; D starts low and is drawn up to the now line."""
    lo, hi = Y_D - ROW / 2, Y_D + ROW / 2
    pts = [_p(-100, lo)]
    level = lo
    for w, v in steps:
        if w > x_now + 1e-6:
            break
        nxt = hi if v else lo
        pts.append(_p(sx(w, x_now) - D_SLOPE / 2, level))
        pts.append(_p(sx(w, x_now) + D_SLOPE / 2, nxt))
        level = nxt
    pts.append(_p(NOW_X, level))
    return poly(clip_poly(pts, xa, min(xb, NOW_X)), color)


def edges_in_view(x_now, pad=0.0):
    out = []
    k0 = int(np.floor((x_now - (NOW_X - XA)) / PER)) - 1
    for k in range(k0, k0 + 8):
        x = sx(k * PER, x_now)
        if XA - SU - HO - pad < x < XB + SU + HO + pad:
            out.append((k, x))
    return out


def windows(x_now):
    g = VGroup()
    g.by_k = {}
    for k, x in edges_in_view(x_now):
        a, b = max(XA, x - SU), min(XB, x + HO)
        if b - a > 0.02:
            r = Rectangle(width=b - a, height=WIN_H).set_stroke(width=0).set_fill(GOLD, 0.25)
            r.move_to(_p((a + b) / 2, Y_D))
            g.add(r)
            g.by_k[k] = r
    return g


def guides(x_now):
    g = VGroup()
    for k, x in edges_in_view(x_now):
        if XA < x < XB:
            g.add(Line(_p(x, Y_CLK + ROW / 2 + 0.15), _p(x, Y_D - WIN_H / 2 - 0.05)).set_stroke(DIM, 1.5))
    return g


def now_line():
    return DashedLine(_p(NOW_X, Y_CLK + ROW / 2 + 0.2), _p(NOW_X, Y_D - WIN_H / 2 - 0.1),
                      dash_length=0.08).set_stroke(FG, 2, opacity=0.6)


def plan_scroll(t0, events, v0=0.7):
    """Constant speed v and start x0 so that, at each event (scene time, 'open'|'inside'),
    the now line sits mid-gap between windows ('open') or just before an edge ('inside')."""
    ranges = {"open": (HO + 0.3, PER - SU - 0.3), "inside": (PER - SU + 0.25, PER - 0.2)}
    best = None
    for v in np.arange(0.5, 0.95, 0.005):
        for x0 in np.arange(0.0, PER, 0.01):
            cost = 4 * (v - v0) ** 2
            for tau, kind in events:
                ph = (x0 + v * (tau - t0)) % PER
                a, b = ranges[kind]
                d = 0.0 if a <= ph <= b else min(abs(ph - a), abs(ph - b), PER - abs(ph - a), PER - abs(ph - b))
                cost += 10 * d * d
            if best is None or cost < best[0]:
                best = (cost, v, x0)
    return best[1], best[2] + 10 * PER          # start well into positive x


def dim_target(mob, op, scale=1.0, to=None):
    t = mob.copy()
    if scale != 1.0:
        t.scale(scale)
    if to is not None:
        t.move_to(to)
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_fill(opacity=leaf.get_fill_opacity() * op)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * op)
    return t


class MetaHook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ scrolling
    def scroll(self, dt, *anims):
        dt = max(dt, 0.05)
        self.play(self.xt.animate.increment_value(self.v * dt), *anims, run_time=dt, rate_func=linear)

    def scroll_until(self, tau, *anims):
        self.scroll(tau - self.time, *anims)

    def step_d(self, level, dt):
        """D changes at the end of a dt-long press/release: record it there."""
        self.steps.append((self.xt.get_value() + self.v * dt, level))

    def make_tick(self, w):
        tick = check_mark(GREEN).scale(0.62)
        xt = self.xt

        def upd(m):
            x = sx(w, xt.get_value())
            m.move_to(_p(x, Y_D + ROW / 2 + 0.33))
            age = xt.get_value() - w
            op = min(1.0, max(0.0, age / 0.35)) * (1.0 if x > XA + 0.3 else 0.0)
            m.set_stroke(opacity=op)
        tick.add_updater(upd)
        upd(tick)
        self.add(tick)
        self.ticks.append(tick)

    # ------------------------------------------------------------------ c4.hook.1
    def clip1(self):
        with self.say("c4.hook.1") as c:
            # {title}
            card = title_card("Part 4 · Metastability and the synchroniser")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            # {ours}: ch3's split path, small, upper left; GOLD window on D1, GREEN tick
            P = split_path()
            band = Rectangle(width=0.75, height=0.7).set_stroke(width=0).set_fill(GOLD, 0.45)
            band.move_to(_p(2.12, P_PIN))
            tick = check_mark(GREEN).scale(2.0).move_to(_p(2.45, 0.05))
            ours = VGroup(P, band, tick)
            ours.scale(0.55).to_corner(UL, buff=0.5)
            # the small copy's labels, re-set at a readable size (dropped again in the corner)
            texts = [P.ff0.d_l, P.ff0.q_l, P.ff0.qb_l, P.ff1.d_l, P.ff1.q_l, P.ff1.qb_l, P.cl_l,
                     P.q0_l, P.d1_l, P.d0_l, P.q1_l, *P.names, P.clk0_l, P.clk1_l]
            for m in texts:
                m.parent = None
            for f in (P.ff0, P.ff1):
                f.remove(f.d_l, f.q_l, f.qb_l)
            P.remove(*texts[6:])
            labs = VGroup(*[T(f"FF{i}", 28, FG).move_to(n) for i, n in enumerate(P.names)],
                          T("CL", 28, BLUE).move_to(P.cl),
                          T("CLK0", 28, YELLOW).move_to(P.clk0_l),
                          T("CLK1", 28, YELLOW).next_to(P.src, RIGHT, buff=0.12).set_opacity(0.7))
            cap = T("our own signals: we choose when they change", 34, FG)
            cap.next_to(ours, DOWN, buff=0.6).align_to(ours, LEFT)
            c.wait_until("ours")
            sweep_clear(self, time_span(FadeIn(P), 0.6, 1.4), time_span(FadeIn(labs), 0.8, 1.4), run_time=1.4)  # early: the path's labels come with it
            self.play(FadeIn(band), *appear(tick, shift=None), *during(appear(cap), 0.35, 1.0),
                      run_time=1.2)  # early: the line sums up the sentence

            # {button}: path to the corner, dimmed; the hero circuit and the traces
            c.wait_until("button")
            t_button = self.time
            H = button_ff()
            self.H = H
            self.steps = []
            self.ticks = []
            ev = [(c.at("presses") + 0.3, "open"), (c.at("no idea") + 0.3, "open"),
                  (c.at("lands") + 0.3, "inside")]
            self.v, x0 = plan_scroll(t_button + 1.5 + 1.1 + 0.9, ev)   # the three plays below
            self.xt = ValueTracker(x0)
            xt = self.xt
            self.wins = always_redraw(lambda: windows(xt.get_value()))
            self.gds = always_redraw(lambda: guides(xt.get_value()))
            self.clk = always_redraw(lambda: clk_trace(xt.get_value()))
            self.dw = always_redraw(lambda: d_trace(xt.get_value(), self.steps))
            self.now = now_line()
            self.lab_clk = T("CLK", 34, YELLOW).next_to(_p(XA, Y_CLK), LEFT, buff=0.25)
            self.lab_d = T("D", 34, BLUE).next_to(_p(XA, Y_D), LEFT, buff=0.25)
            corner = dim_target(ours, 0.3, scale=0.62)
            corner.to_corner(UL, buff=0.45)
            self.play(*disappear(cap, labs),
                      *during([Transform(ours, corner)], 0.0, 0.7),
                      *during([FadeIn(H.ff), FadeIn(H.clk_l)], 0.35, 1.0),
                      run_time=1.5)
            self.ours = ours
            self.play(GrowFromCenter(H.btn), *during([Create(H.wire)], 0.3, 1.0), run_time=1.1)
            self.play(FadeIn(self.wins), FadeIn(self.gds), FadeIn(self.clk), FadeIn(self.dw), FadeIn(self.now),
                      *appear(self.lab_clk, self.lab_d, shift=None, lag=0.2), run_time=0.9)  # early: trace labels with their rows

            # {press}: the finger presses between two windows; later it lets go, also between
            finger = H.finger.shift(0.35 * LEFT)
            self.scroll_until(c.at("press"))
            self.scroll(0.5, FadeIn(finger, shift=0.3 * RIGHT))
            self.scroll_until(c.at("presses"))
            self.step_d(1, 0.3)
            self.make_tick(self.steps[-1][0])
            self.scroll(0.3, finger.animate.shift((0.35 + PUSH) * RIGHT), *during([H.btn.plunger.animate.shift(PUSH * RIGHT)], 0.6, 1.0))
            self.scroll_until(c.at("no idea"))
            self.step_d(0, 0.3)
            self.make_tick(self.steps[-1][0])
            self.scroll(0.3, finger.animate.shift((0.35 + PUSH) * LEFT), H.btn.plunger.animate.shift(PUSH * LEFT))

            # {inside}: the next press lands inside a window; it turns RED and the scroll stops
            self.scroll_until(c.at("lands") - 0.45)
            self.scroll(0.45, finger.animate.shift(0.35 * RIGHT))
            self.step_d(1, 0.3)
            self.scroll(0.3, finger.animate.shift(PUSH * RIGHT), H.btn.plunger.animate.shift(PUSH * RIGHT))
            self.freeze()
            red = self.win_hit
            self.play(red.animate.set_fill(RED, 0.45), FlashAround(red, color=RED, time_width=1.5, buff=0.08),
                      run_time=1.2)
            c.wait_until()

    def freeze(self):
        """Stop the scroll: swap the redrawn traces for identical static ones."""
        x = self.xt.get_value()
        for m in (self.wins, self.gds, self.clk, self.dw):
            m.clear_updaters()
            self.remove(m)
        for t in self.ticks:
            t.clear_updaters()
        self.x_stop = x
        wins = windows(x)
        k_hit = min(wins.by_k, key=lambda k: abs(sx(k * PER, x) - NOW_X - 0.2))
        self.win_hit = wins.by_k[k_hit]
        self.k_hit = k_hit
        self.win_rest = [r for k, r in wins.by_k.items() if k != k_hit]
        self.gds = guides(x)
        self.clk = clk_trace(x)
        self.dw = d_trace(x, self.steps)
        self.add(*self.win_rest, self.win_hit, self.gds, self.clk, self.dw)
        self.add(self.now)

    # ------------------------------------------------------------------ c4.hook.2
    def clip2(self):
        H = self.H
        with self.say("c4.hook.2") as c:
            # {sigh}: the lecturer's words, upper right
            quote = VGroup(T("“So many problems", 38, YELLOW, slant=ITALIC),
                           T("with flip-flops!”", 38, YELLOW, slant=ITALIC)).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
            who = T("— the lecturer", 30, DIM)
            qg = VGroup(quote, who)
            who.next_to(quote, DOWN, buff=0.22).align_to(quote, RIGHT)
            qg.to_corner(UR, buff=0.55)
            c.wait_until(own_word=who)
            self.play(*appear(*quote, who, lag=0.3), run_time=1.4)  # early: the quote is read as one line

            # {question}: everything dims but the RED window with D's edge in it
            x = self.x_stop
            w = self.win_hit
            edge = d_trace(x, self.steps, xa=w.get_left()[0], xb=w.get_right()[0], color=BLUE)
            self.add(edge)
            c.wait_until("question")
            self.remove(self.xt)
            rest = [m for m in self.mobjects if m not in (w, edge)]
            gold = [m for m in self.win_rest]
            others = [m for m in rest if m not in gold]
            self.play(*set_alpha(others, DIMMED),
                      *[m.animate.set_fill(GOLD, 0.08) for m in gold], run_time=1.0)
            self.wait(0.4)
            # the circuit, path, finger and quote clear; the traces rise to the middle
            traces = [*self.win_rest, w, self.gds, self.clk, self.dw, edge, self.now,
                      self.lab_clk, self.lab_d, *self.ticks]
            leave = [m for m in self.mobjects if m not in traces]
            self.play(*during([FadeOut(m) for m in leave], 0.0, 0.45),
                      *during([m.animate.shift(2.3 * UP) for m in traces], 0.35, 1.0), run_time=1.6)
            q = VGroup(T("What does a flip-flop do when its input", 42, YELLOW),
                       T("changes inside the window?", 42, YELLOW)).arrange(DOWN, buff=0.2)
            q.move_to(_p(0, 2.5))
            c.wait_until("what does")
            self.play(*appear(*q, lag=0.3), run_time=1.3)  # early: the question is read as one sentence
            c.wait_until("road")

            # {road}: the lecture's three chips; the first done, "metastability" lit YELLOW
            chips = [chip("timing rules"), chip("metastability"), chip("parallelism")]
            for ch, xx in zip(chips, (-4.3, 0.0, 4.3)):
                ch.scale(0.8).move_to(_p(xx, -2.75))
            self.play(*appear(*chips, shift=None, lag=0.2), run_time=1.2)  # early: the road shown whole, then walked
            c.wait_until("second")
            self.play(*set_alpha([chips[0]], 0.35), run_time=0.8)
            c.wait_until("meta-stability")
            m = chips[1]
            self.play(*recolor([m.body, *m.pins, m.notch, m.lab], YELLOW),
                      FlashAround(m, color=YELLOW, time_width=1.5, buff=0.15), run_time=1.0)
            c.wait_until()
            self.wait(1.4)


def chip(label, w=3.4, h=1.6, n_pins=5):
    """ch1_s1_hook.py's road chip."""
    body = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(DIM, 4).set_fill(BG, 0)
    pins = []
    for j in range(n_pins):
        x = -w / 2 + (j + 0.5) * w / n_pins
        pins.append(Line(_p(x, h / 2), _p(x, h / 2 + 0.25)).set_stroke(DIM, 4))
        pins.append(Line(_p(x, -h / 2), _p(x, -h / 2 - 0.25)).set_stroke(DIM, 4))
    notch = Dot(_p(-w / 2 + 0.25, h / 2 - 0.25), radius=0.07, color=DIM)
    lab = T(label, 36, DIM)
    g = VGroup(body, *pins, notch, lab)
    g.body, g.pins, g.notch, g.lab = body, pins, notch, lab
    return g
