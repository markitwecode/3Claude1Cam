"""Chapter 2, scene 2: why a window is a problem (level vs edge triggering; a D latch with Q-bar fed
back to D buzzes for the whole window and freezes at random). Clips c2.window.1 – c2.window.4.

Reusable for s7's recap and ch6 (copy, don't import):
  feedback_latch(center, s)   the latch box (s1's make_latch style) + Q-bar pin, the GREEN Q-bar -> D
                              loop over the top, the YELLOW CLK wire on EN, small gates (hidden).
  red_buzz(x_r, x_f, y_lo, h, offset, step, n, start_high)   one window's RED oscillation polyline.
  buzz_window(w, h)           a self-contained icon: CLK pulse, YELLOW band, RED buzz under it.
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


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- latch box: s1's make_latch geometry (box 1.5 x 2.6, pins 0.6 off centre, wires 0.85) ----
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 0.6          # s1 uses 1.0; shortened here so the timing rows fit under the circuit


def nor_icon(center, s=0.32):
    """Small NOR outline (OR body + bubble), DIM, for the 'gates inside' hint."""
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(-0.7, -0.6))
    b.add_cubic_bezier_curve_to(_p(-0.45, -0.2), _p(-0.45, 0.2), _p(-0.7, 0.6))
    bub = Circle(radius=0.1).move_to(_p(0.8, 0))
    g = VGroup(b, bub).set_stroke(DIM, 2.5).set_fill(BG, 0)
    return g.scale(s, about_point=ORIGIN).shift(center)


def feedback_latch(center=ORIGIN, s=0.8):
    """D latch box (s1 style) with a Q-bar pin under Q, the GREEN Q-bar -> D feedback loop over the
    top (hop where it crosses Q), and the YELLOW CLK wire on EN. Geometry scales by s, text doesn't.
    Parts: .box .sq .d_w .q_w .qb_w .en_w .d_l .q_l .qb_l .en_l  (.sym = all of these)
           .loop (GREEN wire, Q-bar stub end -> D stub end), .path (Q-bar pin -> D pin, for a dot)
           .clk_w (YELLOW, stroke 6) .clk_l ("CLK" under it), .gates (two DIM NOR icons, not added)
           .q_end (point at Q's wire end).  Added: .sym only; add .loop / .clk_w / .clk_l yourself."""
    c = np.array(center)

    def P(x, y):
        return c + s * _p(x, y)

    hw, hh = s * BOX_W / 2, s * BOX_H / 2
    g = VGroup()
    g.box = Rectangle(width=2 * hw, height=2 * hh).set_stroke(FG, 4).set_fill(BG, 1).move_to(c)
    g.sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(g.box.get_bottom())
    xr_q = BOX_W / 2 + WIRE + 0.85                        # Q's wire runs past the loop's riser
    g.d_w = Line(P(-BOX_W / 2 - WIRE, PIN_Y), P(-BOX_W / 2, PIN_Y)).set_stroke(BLUE, 5)
    g.q_w = Line(P(BOX_W / 2, PIN_Y), P(xr_q, PIN_Y)).set_stroke(GREEN, 5)
    g.qb_w = Line(P(BOX_W / 2, -PIN_Y), P(BOX_W / 2 + WIRE, -PIN_Y)).set_stroke(GREEN, 5)
    g.en_w = Line(P(0, -BOX_H / 2 - EN_WIRE), P(0, -BOX_H / 2) + 0.1 * DOWN).set_stroke(BLUE, 5)
    g.d_l = T("D", 36, BLUE).move_to(P(-BOX_W / 2, PIN_Y) + 0.3 * RIGHT)
    g.q_l = T("Q", 36, GREEN).move_to(P(BOX_W / 2, PIN_Y) + 0.3 * LEFT)
    g.qb_l = MathTex(r"\overline{Q}", font_size=40, color=GREEN).move_to(P(BOX_W / 2, -PIN_Y) + 0.3 * LEFT)
    g.en_l = T("EN", 30, BLUE).move_to(g.box.get_bottom() + 0.42 * UP)
    g.sym = VGroup(g.d_w, g.q_w, g.qb_w, g.en_w, g.box, g.sq, g.d_l, g.q_l, g.qb_l, g.en_l)
    g.add(g.sym)
    g.q_end = g.q_w.get_end()

    # feedback loop: Q-bar stub end -> right -> up (hop over Q) -> over the top -> down -> D stub end
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    g.loop = VMobject().set_points_as_corners([c + s * q for q in pts]).set_stroke(GREEN, 5)
    g.path = VMobject().set_points_as_corners(
        [P(BOX_W / 2, -PIN_Y)] + [c + s * q for q in pts] + [P(-BOX_W / 2, PIN_Y)])
    g.clk_w = g.en_w.copy().set_stroke(YELLOW, 6).set_z_index(1)
    g.clk_l = T("CLK", 32, YELLOW).next_to(g.en_w.get_start(), LEFT, buff=0.18).shift(0.12 * UP)
    g.gates = VGroup(nor_icon(P(0.03, 0.18), 0.26 * s), nor_icon(P(0.03, -0.32), 0.26 * s))
    return g


def red_buzz(x_r, x_f, y_lo, h, offset, step, n, start_high, color=RED, width=4):
    """One window's oscillation: n flips at x_r + offset + k*step, from x_r to x_f (no freeze)."""
    lv = start_high
    pts = [(x_r, y_lo + h * lv)]
    for k in range(n):
        x = x_r + offset + k * step
        pts += [(x, y_lo + h * lv)]
        lv = 1 - lv
        pts += [(x, y_lo + h * lv)]
    pts.append((x_f, y_lo + h * lv))
    return poly(pts, color, width)


def buzz_window(w=2.4, h=0.6, gap=0.5, n=9):
    """Icon for recaps: one CLK pulse (YELLOW) over one RED buzz, the window banded YELLOW.
    Built centred at ORIGIN; .clk .band .buzz."""
    m = 0.35 * w
    x0, xr, xf, x1 = -w / 2 - m, -w / 2, w / 2, w / 2 + m
    yc = gap / 2
    g = VGroup()
    g.clk = poly([(x0, yc), (xr, yc), (xr, yc + h), (xf, yc + h), (xf, yc), (x1, yc)], YELLOW)
    g.band = Rectangle(width=w, height=2 * h + gap + 0.3).set_stroke(width=0).set_fill(YELLOW, 0.12)
    g.band.set_z_index(-1)
    g.buzz = red_buzz(xr, xf, -yc - h, h, 0.1 * w, 0.8 * w / (n - 1), n, 0)
    g.add(g.band, g.clk, g.buzz)
    return g


# ---- timing rows (lecture style: CLK on top, labels at left) ----
X0, XW = -4.6, 11.2
PER = XW / 3.5
RISE = [X0 + PER / 2 + i * PER for i in range(3)]
FALL = [r + PER / 2 for r in RISE]
XE = X0 + XW
TH = 0.5
Y_CLK, Y_Q, Y_W = -1.3, -2.3, -3.3          # row centres
LBL_X = -4.85
# buzz per window: (offset, step, flips, starts high) -> freezes high, low, high
BUZZ = [(0.20, 0.22, 7, 0), (0.14, 0.22, 7, 1), (0.24, 0.22, 7, 0)]


def lo(y):
    return y - TH / 2


class WindowProblem(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        with self.say("c2.window.1") as c:
            l1 = T("D latch: level-triggered, transparent while EN = 1", 38,
                   t2c={"level-triggered": YELLOW}).move_to(_p(0, 3.0))
            l2 = T("simpler: outputs change only on clock edges", 38,
                   t2c={"clock edges": YELLOW}).move_to(_p(0, 2.05))
            c.wait_until(own_word=l1)
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("simpler")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("rising")

            # three small CLK traces
            x0, w, h = -1.6, 6.4, 0.6
            per = w / 3.5
            rs = [x0 + per / 2 + i * per for i in range(3)]
            fs = [r + per / 2 for r in rs]

            def clk(yc):
                pts = [(x0, yc - h / 2)]
                for r, f in zip(rs, fs):
                    pts += [(r, yc - h / 2), (r, yc + h / 2), (f, yc + h / 2), (f, yc - h / 2)]
                pts.append((x0 + w, yc - h / 2))
                return poly(pts, YELLOW)

            ys = [0.55, -0.95, -2.45]
            lab_x = -2.0

            def lab(txt, y):
                return T(txt, 32, YELLOW).move_to(_p(0, y)).align_to(_p(lab_x, 0), RIGHT)

            self.tr_r = clk(ys[0])
            self.ups = [Arrow(_p(r, ys[0] - h / 2), _p(r, ys[0] + h / 2 + 0.3), buff=0, stroke_width=6,
                              tip_length=0.2, max_tip_length_to_length_ratio=0.3, color=YELLOW) for r in rs]
            self.lab_r = lab("rising edge", ys[0])
            self.play(Create(self.tr_r, rate_func=linear), *appear(self.lab_r), run_time=1.0)
            self.play(*[GrowArrow(a) for a in self.ups], run_time=0.8)

            self.tr_f = clk(ys[1])
            self.downs = [Arrow(_p(f, ys[1] + h / 2 + 0.3), _p(f, ys[1] - h / 2), buff=0, stroke_width=6,
                                tip_length=0.2, max_tip_length_to_length_ratio=0.3, color=YELLOW) for f in fs]
            self.lab_f = lab("falling edge", ys[1])
            self.play(Create(self.tr_f, rate_func=linear), *appear(self.lab_f), run_time=1.0)
            self.play(*[GrowArrow(a) for a in self.downs], run_time=0.8)
            c.wait_until("why")

            # {why}: a window: banded highs, sparks anywhere inside
            self.tr_w = clk(ys[2])
            self.bands_w = [Rectangle(width=f - r, height=h + 0.5).set_stroke(width=0)
                            .set_fill(YELLOW, 0.18).set_z_index(-1).move_to(_p((r + f) / 2, ys[2]))
                            for r, f in zip(rs, fs)]
            self.lab_w = lab("inside a window", ys[2])
            self.play(Create(self.tr_w, rate_func=linear), *appear(self.lab_w), run_time=1.2)
            self.play(*appear(*self.bands_w, shift=None, lag=0.2), run_time=1.0)
            fr = [(0, 0.25), (0, 0.7), (1, 0.45), (1, 0.85), (2, 0.15), (2, 0.6)]
            dy = [0.05, -0.12, 0.1, -0.05, -0.1, 0.08]
            self.sparks = [self.spark(_p(rs[i] + u * (fs[i] - rs[i]), ys[2] + d))
                           for (i, u), d in zip(fr, dy)]
            c.wait_until("set off")
            self.play(*appear(*self.sparks, shift=None, lag=0.4), run_time=min(2.4, c.until("instant")))
            c.wait_until("instant")

            # {instant}: the up-arrow trace brightens
            rest = [self.tr_f, *self.downs, self.lab_f, self.tr_w, *self.bands_w, self.lab_w, *self.sparks]
            self.play(*set_alpha(rest, 0.35), self.tr_r.animate.set_stroke(width=7),
                      *[a.animate.set_stroke(width=8) for a in self.ups], run_time=1.2)
            self.play(*flash(self.ups, color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until()

    @staticmethod
    def spark(pos, r=0.16):
        rays = [Line(pos + 0.35 * r * np.array([np.cos(a), np.sin(a), 0]),
                     pos + r * np.array([np.cos(a), np.sin(a), 0])) for a in np.arange(8) * PI / 4]
        return VGroup(*rays).set_stroke(RED, 4)

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        with self.say("c2.window.2") as c:
            L = self.L = feedback_latch(_p(-3.9, 1.55), s=1.2)
            sweep_clear(self, FadeIn(L, shift=0.2 * UP), run_time=1.6)
            c.wait_until("wire")

            # {wire}: Q-bar loops back to D
            self.play(Create(L.loop), run_time=2.0)
            c.wait_until("clock")

            # {clock}: CLK on EN
            target = L.clk_w.copy()
            L.clk_w.shift(0.8 * DOWN).set_stroke(opacity=0)
            self.play(Transform(L.clk_w, target), FadeIn(L.clk_l, shift=0.5 * RIGHT), run_time=1.0)

            # the CLK row with its banded windows
            pts = [(X0, lo(Y_CLK))]
            for r, f in zip(RISE, FALL):
                pts += [(r, lo(Y_CLK)), (r, lo(Y_CLK) + TH), (f, lo(Y_CLK) + TH), (f, lo(Y_CLK))]
            pts.append((XE, lo(Y_CLK)))
            self.clk = poly(pts, YELLOW)
            self.clk_lab = T("CLK", 32, YELLOW).move_to(_p(0, Y_CLK)).align_to(_p(LBL_X, 0), RIGHT)
            self.bands = [self.band(r, f, lo(Y_Q) - 0.25) for r, f in zip(RISE, FALL)]
            self.play(*appear(self.clk_lab, shift=None), Create(self.clk, rate_func=linear),
                      run_time=min(1.6, c.until("want")))
            self.play(*appear(*self.bands, shift=None, lag=0.2), run_time=min(1.0, c.until("want")))

            # {want}: the goal
            self.goal = T("goal: flip once per clock cycle", 32, GREEN).move_to(_p(3.4, 2.75))
            c.wait_until("want")
            self.play(*appear(self.goal), run_time=1.0)
            c.wait_until("ask")

            # {ask}: "?" on the output, and the Q row up to the first rising edge
            self.qq = T("?", 48, YELLOW).next_to(L.q_end, RIGHT, buff=0.15)
            self.play(*appear(self.qq), run_time=1.0)
            self.q_lab = T("Q", 34, GREEN).move_to(_p(0, Y_Q)).align_to(_p(LBL_X, 0), RIGHT)
            self.q_pre = poly([(X0, lo(Y_Q)), (RISE[0], lo(Y_Q))], GREEN)
            self.play(*appear(self.q_lab, shift=None), Create(self.q_pre, rate_func=linear), run_time=1.2)
            c.wait_until()

    @staticmethod
    def band(r, f, y_bot):
        top = Y_CLK + TH / 2 + 0.25
        return (Rectangle(width=f - r, height=top - y_bot).set_stroke(width=0)
                .set_fill(YELLOW, 0.12).set_z_index(-1).move_to(_p((r + f) / 2, (top + y_bot) / 2)))

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        L = self.L
        y0 = lo(Y_Q)
        off, step, n, _ = BUZZ[0]
        t = [RISE[0] + off + k * step for k in range(n)]

        def dig(v, pt):
            return T(str(v), 32, GOLD).move_to(pt)

        q_pos = L.q_w.get_start() + _p(0.42, 0.3)
        qb_pos = L.qb_w.get_center() + _p(0, 0.3)
        d_pos = L.d_w.get_center() + _p(0, 0.3)

        with self.say("c2.window.3") as c:
            # {open}: transparent; D copies Q-bar
            self.play(self.bands[0].animate.set_fill(YELLOW, 0.24), *disappear(self.qq), run_time=1.0)
            dq, dqb = dig(0, q_pos), dig(1, qb_pos)
            self.play(*appear(dq, dqb, lag=0.3), run_time=1.0)
            dd = dig(1, d_pos)
            self.play(*fly(dqb, dd, arc=-PI / 3), run_time=min(1.5, c.until("flip")))
            c.wait_until("flip")

            # {flip}
            pa = poly([(RISE[0], y0), (t[0], y0), (t[0], y0 + TH)], GREEN)
            dq1, dqb1 = dig(1, q_pos), dig(0, qb_pos)
            self.play(Create(pa, rate_func=linear), *swap(dq, dq1), *swap(dqb, dqb1), run_time=1.2)
            c.wait_until("back")

            # {back}: a dot runs round the loop, D takes the new Q-bar
            dot = Dot(L.path.get_start(), radius=0.1, color=YELLOW).set_z_index(3)
            self.play(FadeIn(dot, scale=0.5), run_time=0.3)
            self.play(MoveAlongPath(dot, L.path), run_time=1.4, rate_func=smooth)
            dd1 = dig(0, d_pos)
            self.play(FadeOut(dot), *swap(dd, dd1), run_time=min(0.8, c.until("again")))
            c.wait_until("again")

            # {again}
            pb = poly([(t[0], y0 + TH), (t[1], y0 + TH), (t[1], y0)], GREEN)
            dq2, dqb2 = dig(0, q_pos), dig(1, qb_pos)
            self.play(Create(pb, rate_func=linear), *swap(dq1, dq2), *swap(dqb1, dqb2),
                      run_time=min(1.0, c.until("fast")))
            c.wait_until("fast")

            # {fast}: the rest of the window buzzes, RED
            pts = [(t[1], y0)]
            lv = 0
            for x in t[2:]:
                pts += [(x, y0 + TH * lv)]
                lv = 1 - lv
                pts += [(x, y0 + TH * lv)]
            pts.append((FALL[0], y0 + TH * lv))
            pc = poly(pts, RED)
            self.play(Create(pc, rate_func=linear), pa.animate.set_stroke(RED), pb.animate.set_stroke(RED),
                      run_time=1.4)
            self.fast_l = T("as fast as the gates allow", 30, RED).move_to(
                _p(RISE[0] + 0.6, (lo(Y_Q) + Y_W + TH / 2) / 2))
            self.play(*appear(self.fast_l), run_time=1.0)
            c.wait_until("buzz")

            # {buzz}: the next windows buzz too
            self.buzz = [VGroup(pa, pb, pc)]
            for i in (1, 2):
                o, st, k, hi = BUZZ[i]
                self.buzz.append(red_buzz(RISE[i], FALL[i], y0, TH, o, st, k, hi))
            self.play(self.bands[0].animate.set_fill(YELLOW, 0.12), *disappear(dq2, dqb2, dd1),
                      *[Create(b, rate_func=linear) for b in self.buzz[1:]], run_time=2.0)
            c.wait_until("stop")

            # {stop}: freeze at each falling edge, a different level each time
            ends = [RISE[1], RISE[2], XE]
            levels = [1, 0, 1]
            self.flats, self.tags = [], []
            for f, e, v in zip(FALL, ends, levels):
                self.flats.append(poly([(f, y0 + TH * v), (e, y0 + TH * v)], RED))
                self.tags.append(T("?", 32, RED).move_to(_p(f + 0.4, y0 + TH * v + 0.3)))
            for fl, tg in zip(self.flats, self.tags):
                self.play(Create(fl, rate_func=linear), *appear(tg, shift=None), run_time=0.9)
            c.wait_until("depends")

            # {depends}: the windows flash, then the gates inside the latch
            self.play(*[b.animate(rate_func=there_and_back).set_fill(YELLOW, 0.4) for b in self.bands],
                      run_time=1.2)
            self.play(*appear(*L.gates, shift=None, lag=0.2), run_time=0.8)
            self.play(*[g.animate(rate_func=there_and_back).set_stroke(YELLOW, 4) for g in L.gates],
                      *flash(L.gates, color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until()

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        L = self.L
        with self.say("c2.window.4") as c:
            # {wanted}: a third row, one clean flip per rising edge
            tall = [self.band(r, f, lo(Y_W) - 0.15) for r, f in zip(RISE, FALL)]
            self.play(*disappear(self.fast_l),
                      *[Transform(b, t) for b, t in zip(self.bands, tall)], run_time=1.0)
            y0 = lo(Y_W)
            lv, pts = 0, [(X0, y0)]
            for r in RISE:
                pts += [(r, y0 + TH * lv)]
                lv = 1 - lv
                pts += [(r, y0 + TH * lv)]
            pts.append((XE, y0 + TH * lv))
            self.want = poly(pts, GREEN)
            self.w_lab = T("Q wanted", 32, GREEN).move_to(_p(0, Y_W)).align_to(_p(LBL_X, 0), RIGHT)
            g_top, g_bot = Y_CLK + TH / 2 + 0.45, lo(Y_W) - 0.2
            guides = [Line(_p(r, g_top), _p(r, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2) for r in RISE]
            ups = [Arrow(_p(r, lo(Y_CLK) - 0.05), _p(r, lo(Y_CLK) + TH + 0.35), buff=0, stroke_width=6,
                         tip_length=0.22, max_tip_length_to_length_ratio=0.3, color=YELLOW) for r in RISE]
            self.play(*appear(self.w_lab, shift=None), Create(self.want, rate_func=linear),
                      *[GrowArrow(a) for a in ups], *[Create(gl) for gl in guides], run_time=2.0)
            c.wait_until("zero")

            # "Zero, one, zero, one."
            segs = [(X0, RISE[0]), (RISE[0], RISE[1]), (RISE[1], RISE[2]), (RISE[2], XE)]
            digs = [T(str(v), 32, GOLD).move_to(_p((a + b) / 2, Y_W))
                    for v, (a, b) in zip([0, 1, 0, 1], segs)]
            self.play(*appear(*digs, shift=None, lag=0.5), run_time=min(2.4, c.until("remember")))
            c.wait_until("remember")

            # {remember}: a soft outline round the circuit
            circ = VGroup(L.box, L.loop, L.d_w, L.q_w)
            ring = RoundedRectangle(corner_radius=0.25, width=circ.width + 0.5, height=circ.height + 0.4)
            ring.set_stroke(YELLOW, 3, opacity=0.6).move_to(circ)
            self.play(FadeIn(ring), *disappear(*L.gates), run_time=1.2)
            c.wait_until("later")

            # {later}
            self.tag = T("part 6: the heart of a counter", 32, YELLOW).move_to(_p(3.4, 1.75))
            c.wait_until("later")
            self.play(*appear(self.tag), run_time=1.0)
            c.wait_until()
        self.wait(2.2)
