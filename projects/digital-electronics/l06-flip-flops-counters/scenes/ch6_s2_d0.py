"""Chapter 6, scene 2: D0 by inspection (D0 = not Q0: flip-flop 0 toggles). Clips c6.inspect.1 – c6.inspect.3.

Opens on ch5_s6's mod_table() at full size, left edge x = -6.6 (ch6 s3 / s4 open the same way).
Reused (copied): mod_table (ch5_s6), make_ff / qbar / toggle_loop / xor_formula / feedback_latch /
red_buzz / buzz_window (ch3_s5), clk_points / toggle_pieces / up_arrow / edge_line (ch3_s4).
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


# ---- ch5_s6's mod_table (copied) ---------------------------------------------------------------
MT_GX = (-2.8, 0.0, 2.8)
MT_DX = 0.72
MT_DEC = -4.1
MT_SEPS = (-1.4, 1.4)
MT_TITLE_Y, MT_HEAD_Y, MT_RULE_Y = 3.45, 2.75, 2.35
MT_ROW0_Y, MT_PITCH = 1.9, 0.6
MT_TOP, MT_BOT = 3.8, -2.65
MT_CELL, MT_HEAD = 40, 42


def mt_row_y(i):
    return MT_ROW0_Y - i * MT_PITCH


def mod_table(filled=True, x=0.0):
    titles = VGroup(*[T(s, 30).move_to(_p(gx, MT_TITLE_Y))
                      for s, gx in zip(("Current state", "Next state", "FF inputs"), MT_GX)])
    head_tex = (["Q_2", "Q_1", "Q_0"], ["Q_2'", "Q_1'", "Q_0'"], ["D_2", "D_1", "D_0"])
    head_col = (GREEN, GREEN, BLUE)
    heads = VGroup(*[VGroup(*[MathTex(t, font_size=MT_HEAD, color=col).move_to(_p(gx + (j - 1) * MT_DX, MT_HEAD_Y))
                              for j, t in enumerate(ts)])
                     for ts, col, gx in zip(head_tex, head_col, MT_GX)])
    lines = VGroup(*[Line(_p(sx, MT_TOP), _p(sx, MT_BOT)).set_stroke(DIM, 2) for sx in MT_SEPS])
    lines.add(Line(_p(MT_DEC - 0.35, MT_RULE_Y), _p(MT_GX[2] + 1.35, MT_RULE_Y)).set_stroke(DIM, 2))
    skel = VGroup(titles, heads, lines)

    def bits_row(v, gx):
        return VGroup(*[MathTex(b, font_size=MT_CELL).move_to(_p(gx + (j - 1) * MT_DX, mt_row_y(i)))
                        for j, b in enumerate(format(v, "03b"))])
    dec, cur, nxt, inp = VGroup(), VGroup(), VGroup(), VGroup()
    for i in range(8):
        dec.add(MathTex(str(i), font_size=MT_CELL, color=GOLD).move_to(_p(MT_DEC, mt_row_y(i))))
        cur.add(bits_row(i, MT_GX[0]))
        nxt.add(bits_row((i + 1) % 8, MT_GX[1]))
        inp.add(bits_row((i + 1) % 8, MT_GX[2]))
    g = VGroup(skel, dec, cur, nxt, inp) if filled else VGroup(skel)
    for m in (skel, dec, cur, nxt, inp):
        m.shift(RIGHT * x)
    g.skel, g.titles, g.heads, g.lines = skel, titles, heads, lines
    g.dec, g.cur, g.nxt, g.inp = dec, cur, nxt, inp
    g.groups = [cur, nxt, inp]
    g.col = lambda gi, j: VGroup(*[row[j] for row in g.groups[gi]])
    return g


# ---- ch3_s5's flip-flop pieces (copied) ---------------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w = box, tri, clk_w
    g.in_w, g.q_w, g.qb_w = in_w, q_w, qb_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def xor_formula(size=84):
    f = MathTex("Q'", "=", "T", r"\oplus", "Q", font_size=size)
    f[0].set_color(GREEN)
    f[2].set_color(BLUE)
    f[4].set_color(GREEN)
    return f


def toggle_loop():
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    ff = make_ff(q_len=WIRE + 0.85)
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    loop = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 5)
    g = VGroup(ff, loop)
    g.ff, g.loop, g.box = ff, loop, ff.box
    return g


def feedback_latch(center=ORIGIN, s=0.8):
    c = np.array(center)
    FB_EN = 0.6

    def P(x, y):
        return c + s * _p(x, y)

    hw, hh = s * BOX_W / 2, s * BOX_H / 2
    g = VGroup()
    g.box = Rectangle(width=2 * hw, height=2 * hh).set_stroke(FG, 4).set_fill(BG, 1).move_to(c)
    g.sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(g.box.get_bottom())
    xr_q = BOX_W / 2 + WIRE + 0.85
    g.d_w = Line(P(-BOX_W / 2 - WIRE, PIN_Y), P(-BOX_W / 2, PIN_Y)).set_stroke(BLUE, 5)
    g.q_w = Line(P(BOX_W / 2, PIN_Y), P(xr_q, PIN_Y)).set_stroke(GREEN, 5)
    g.qb_w = Line(P(BOX_W / 2, -PIN_Y), P(BOX_W / 2 + WIRE, -PIN_Y)).set_stroke(GREEN, 5)
    g.en_w = Line(P(0, -BOX_H / 2 - FB_EN), P(0, -BOX_H / 2) + 0.1 * DOWN).set_stroke(BLUE, 5)
    g.d_l = T("D", 36, BLUE).move_to(P(-BOX_W / 2, PIN_Y) + 0.3 * RIGHT)
    g.q_l = T("Q", 36, GREEN).move_to(P(BOX_W / 2, PIN_Y) + 0.3 * LEFT)
    g.qb_l = MathTex(r"\overline{Q}", font_size=40, color=GREEN).move_to(P(BOX_W / 2, -PIN_Y) + 0.3 * LEFT)
    g.en_l = T("EN", 30, BLUE).move_to(g.box.get_bottom() + 0.42 * UP)
    g.sym = VGroup(g.d_w, g.q_w, g.qb_w, g.en_w, g.box, g.sq, g.d_l, g.q_l, g.qb_l, g.en_l)
    g.add(g.sym)
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    g.loop = VMobject().set_points_as_corners([c + s * q for q in pts]).set_stroke(GREEN, 5)
    g.add(g.loop)
    return g


def red_buzz(x_r, x_f, y_lo, h, offset, step, n, start_high, color=RED, width=4):
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


# ---- ch3_s4's waveforms (copied) ---------------------------------------------------------------
def clk_points(x0, x1, rises, period):
    pts = [(x0, 0)]
    for r in rises:
        pts += [(r, 0), (r, 1), (r + period / 2, 1), (r + period / 2, 0)]
    pts.append((x1, 0))
    return pts


def trace(pts, y_mid, amp=0.3, color=GREEN, width=4):
    return (VMobject().set_points_as_corners([_p(x, y_mid + (amp if b else -amp)) for x, b in pts])
            .set_stroke(color, width))


def toggle_pieces(x0, x1, edges, y_mid, amp=0.3, start=0, color=GREEN, width=4):
    xs = [x0, *edges, x1]
    out, b = [], start
    for k in range(len(xs) - 1):
        if k == 0:
            pts = [(xs[0], b), (xs[1], b)]
        else:
            pts = [(xs[k], b), (xs[k], 1 - b), (xs[k + 1], 1 - b)]
            b = 1 - b
        out.append(trace(pts, y_mid, amp, color, width))
    return out


AMP = 0.3


def up_arrow(x, y):
    return Triangle().scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(x, y))


def edge_line(x, y_mid, color, amp=AMP, width=9):
    return Line(_p(x, y_mid - amp), _p(x, y_mid + amp)).set_stroke(color, width)


def pulse(mob, color=YELLOW):
    """A glyph's colour goes to `color` and back (ch3_s5's pulse)."""
    base = ManimColor(mob.get_color())

    def f(m, a):
        m.set_color(interpolate_color(base, ManimColor(color), there_and_back(a)))
    return UpdateFromAlphaFunc(mob, f)


def fill_pulse(mob, color=YELLOW):
    """A filled shape's fill goes to `color` and back (the clock triangle 'listening')."""
    base = ManimColor(BG)

    def f(m, a):
        m.set_fill(interpolate_color(base, ManimColor(color), there_and_back(a)), 1)
    return UpdateFromAlphaFunc(mob, f)


def waves(x0, x1, n, clk_y, q_y, lab_x=None):
    """CLK (YELLOW, n rising edges) and Q (GREEN pieces, one flip per rising edge), labels left."""
    per = (x1 - x0) / (n + 0.3)
    rises = [x0 + 0.5 * per + k * per for k in range(n)]
    w = VGroup()
    w.rises = rises
    w.clk = trace(clk_points(x0, x1, rises, per), clk_y, AMP, YELLOW)
    w.ups = [up_arrow(r, clk_y) for r in rises]
    w.qp = toggle_pieces(x0, x1, rises, q_y, AMP)
    lx = (x0 - 0.35) if lab_x is None else lab_x
    w.clk_l = MathTex(r"\mathrm{CLK}", font_size=40, color=DIM).move_to(_p(0, clk_y)).align_to(_p(lx, 0), RIGHT)
    w.q_l = MathTex("Q", font_size=40, color=DIM).move_to(_p(0, q_y)).align_to(_p(lx, 0), RIGHT)
    return w


# ---- layout ---------------------------------------------------------------------------------------
TAB_LEFT = -6.6
RX = 4.35                       # right-hand column centre (clips 1-2)
FF2_C, FF2_K = _p(-1.8, 1.4), 0.8     # clip 2: the D loop, above its waveforms
W2_X0, W2_X1, W2_CLK, W2_Q = -5.0, 1.4, -1.3, -2.7
FF3_C = _p(-3.6, 0.9)           # clip 3: the D loop, full size, left
T3_C = _p(3.8, 0.9)             # clip 3: the T flip-flop, right


class D0ByInspection(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---- c6.inspect.1: read D0 and Q0 down the table -------------------------------------------
    def clip1(self):
        tab = mod_table(filled=True)
        tab.shift(RIGHT * (TAB_LEFT - tab.get_left()[0]))
        self.tab = tab
        d0 = list(tab.col(2, 2))
        q0 = list(tab.col(0, 2))
        h_d0, h_q0 = tab.heads[2][2], tab.heads[0][2]
        leaves = ([*tab.titles, *tab.lines, *tab.dec]
                  + [m for gi in range(3) for row in tab.groups[gi] for m in row]
                  + [m for hs in tab.heads for m in hs])
        rest = [m for m in leaves if all(m is not k for k in d0 + [h_d0])]
        q0_side = q0 + [h_q0]

        def col_box(head, cells, color):
            return (SurroundingRectangle(VGroup(head, *cells), color=color, buff=0.12)
                    .set_stroke(color, 3).set_fill(color, 0.1).set_z_index(-1))

        with self.say("c6.inspect.1") as c:
            self.play(*appear(tab, shift=None), run_time=0.9)   # early: s1's table comes back whole
            # {d0}: the D0 column boxed, the rest dims
            c.wait_until("dee zero")
            b_d0 = col_box(h_d0, d0, BLUE)
            self.play(FadeIn(b_d0), *set_alpha(rest, DIMMED), run_time=min(1.3, c.until("read", floor=0.6)))
            c.wait_until("one")

            # {read}: the first four entries light on their spoken digits, the rest follow
            self.read_column(c, d0, BLUE, [("one", 0), ("zero", 1), ("one", 1), ("zero", 2)], "and so on")
            c.wait_until("qzero")

            # {qzero}: the Q0 column back, boxed GREEN; its entries step with "zero, one, zero, one"
            b_q0 = col_box(h_q0, q0, GREEN)
            self.play(FadeIn(b_q0), *set_alpha(q0_side, 1), run_time=1.2)
            self.read_column(c, q0, GREEN, [("zero", 4), ("one", 2), ("zero", 5), ("one", 3)], None)
            c.wait_until("opposite")

            # {opposite}: everything between Q0 and D0 drops out; each row's pair is linked, pair by pair
            between = ([*tab.lines[:2]] + [m for row in tab.nxt for m in row]
                       + [m for row in tab.inp for m in row[:2]] + list(tab.heads[1]) + list(tab.heads[2][:2])
                       + [tab.titles[1]])
            links = [Line(q.get_right() + 0.2 * RIGHT, d.get_left() + 0.2 * LEFT).set_stroke(YELLOW, 3)
                     for q, d in zip(q0, d0)]
            self.play(*set_alpha(between, 0.05), run_time=0.6)
            rt = min(3.0, c.until("result", floor=1.5) - 0.2)
            step = (rt - 0.6) / 7
            self.play(*[time_span(Create(l), i * step, i * step + 0.6) for i, l in enumerate(links)],
                      *[time_span(pulse(m), i * step, i * step + 0.6) for i, (q, d) in enumerate(zip(q0, d0))
                        for m in (q, d)],
                      run_time=rt)
            c.wait_until("result")

            # {result}: D0 = Q0-bar, the bar drawn last on "not"
            eq = MathTex("D_0", "=", "Q_0", font_size=88).move_to(_p(RX, 0.35))
            eq[0].set_color(BLUE)
            eq[2].set_color(GREEN)
            bar = Line(LEFT, RIGHT).set_stroke(YELLOW, 6).set_width(eq[2].width * 1.1)
            bar.next_to(eq[2], UP, buff=0.12)
            self.play(*disappear(*links), *set_alpha(between, DIMMED), *appear(eq, shift=None),
                      run_time=min(1.0, c.until("not", floor=0.6)))
            c.wait_until("not")
            self.play(Create(bar), run_time=1.0)
            self.eq = VGroup(eq, bar)
            settle(self, self.eq)
            by = T("By inspection,", 40).move_to(_p(RX, 1.75))
            c.wait_until(own_word=by)
            self.play(*appear(by), run_time=1.0)
            self.by = by

    def read_column(self, c, cells, color, cues, rest_cue):
        """Light the first len(cues) cells one per spoken digit, then the rest in one quick sweep."""
        n = len(cues)
        box = None
        for k, (w, nth) in enumerate(cues):
            c.wait_until(w, nth=nth)
            nw, nn = cues[k + 1] if k + 1 < n else (None, 0)
            rt = min(0.6, c.until(nw, nth=nn, floor=0.3)) if nw else 0.6
            nb = SurroundingRectangle(cells[k], color=YELLOW, buff=0.1).set_stroke(YELLOW, 3)
            if box is None:
                self.play(FadeIn(nb), cells[k].animate.set_color(color), run_time=rt)
                box = nb
            else:
                self.play(Transform(box, nb), cells[k].animate.set_color(color), run_time=rt)
        if rest_cue:
            c.wait_until(rest_cue)
        self.play(FadeOut(box), run_time=0.4)
        rest = cells[n:]
        self.play(*[time_span(m.animate.set_color(color), 0.15 * i, 0.15 * i + 0.4) for i, m in enumerate(rest)],
                  run_time=0.15 * (len(rest) - 1) + 0.4)

    # ---- c6.inspect.2: what it means: FF0 toggles --------------------------------------------------
    def clip2(self):
        with self.say("c6.inspect.2") as c:
            # {meaning}: the table goes, the D flip-flop comes in left
            TL = toggle_loop()
            TL.scale(FF2_K, about_point=ORIGIN).shift(FF2_C)
            self.TL = TL
            sweep_clear(self, *appear(TL.ff, shift=None), keep=[self.eq, self.by], run_time=1.6)
            c.wait_until("feed")

            # {feed}: Q-bar wired round to D
            self.play(Create(TL.loop), run_time=1.6)
            self.play(VShowPassingFlash(TL.loop.copy().set_stroke(YELLOW, 8), time_width=0.4),
                      run_time=min(1.4, c.until("edge", floor=0.6)))
            settle(self, TL)
            c.wait_until("edge")

            # {edge}: CLK under it, up-arrows on the rising edges
            w = waves(W2_X0, W2_X1, 4, W2_CLK, W2_Q)
            self.w2 = w
            self.play(*appear(w.clk_l, shift=None), Create(w.clk, rate_func=linear), run_time=1.5)
            self.play(*[time_span(FadeIn(u, scale=0.5), 0.15 * i, 0.15 * i + 0.5) for i, u in enumerate(w.ups)],
                      run_time=1.0)
            c.wait_until("flips")

            # {flips}: Q steps once per rising edge
            per = w.rises[1] - w.rises[0]
            v0 = T("0", 30, GREEN).move_to(_p((W2_X0 + w.rises[0]) / 2, W2_Q + AMP + 0.28))
            self.play(*appear(w.q_l, v0, shift=None, lag=0), Create(w.qp[0]), run_time=0.8)
            vals = [v0]
            for k in range(4):
                v = (k + 1) % 2
                lab = T(str(v), 30, GREEN).move_to(_p(w.rises[k] + per / 2, W2_Q + AMP + 0.28))
                vals.append(lab)
                self.play(Create(w.qp[k + 1]), *appear(lab, shift=0.15 * DOWN), fill_pulse(TL.ff.tri),
                          VShowPassingFlash(edge_line(w.rises[k], W2_CLK, YELLOW), time_width=1.0),
                          run_time=0.75)
            self.vals = vals
            c.wait_until("note")

            # {note}: the slide's words, on the word itself
            note = T("Note: FF0 is toggling", 36, t2c={"toggling": YELLOW}).move_to(_p(RX, -1.15))
            self.note = note
            c.wait_until("toggling")
            self.play(*appear(note), run_time=min(1.0, c.until(floor=0.5)))

    # ---- c6.inspect.3: = a T flip-flop with T = 1; safe, unlike the latch ---------------------------
    def clip3(self):
        TL, w = self.TL, self.w2
        with self.say("c6.inspect.3", gap=3.0) as c:
            # {wire}: the waveforms leave; the circuit grows to full size, left (the equation stays)
            side = [self.eq, self.by, self.note]
            rest = [m for m in self.mobjects if m is not TL and all(m is not s for s in side)]
            self.play(*during(disappear(*rest), 0, 0.45),
                      *during([TL.animate.scale(1 / FF2_K, about_point=TL.box.get_center()).shift(FF3_C - FF2_C)],
                              0.35, 1), run_time=1.8)
            c.wait_until("wired straight back")
            self.play(VShowPassingFlash(TL.loop.copy().set_stroke(YELLOW, 9), time_width=0.4), run_time=1.6)
            c.wait_until("tee")

            # {tee}: = a T flip-flop with T tied to 1
            eq = MathTex("=", font_size=110, color=YELLOW).move_to(_p(0.15, FF3_C[1]))
            ts = make_ff(T3_C, ins=(("T", 0.0),))
            one = MathTex("1", font_size=56, color=BLUE).next_to(ts.in_w[0].get_start(), LEFT, buff=0.15)
            f = xor_formula(64).move_to(_p(T3_C[0], -2.65))
            self.play(*during(disappear(*side), 0, 0.45),
                      *during(appear(eq, ts, one, shift=None, lag=0.2), 0.45, 1), run_time=1.8)
            self.play(*appear(f), run_time=1.0)
            c.wait_until("stuck at one")
            self.play(FlashAround(one, color=YELLOW, time_width=1.5, buff=0.15), run_time=1.0)
            c.wait_until("so cue prime")
            f2 = MathTex("T", "=", "1", r":\ ", "Q'", "=", r"\overline{Q}", font_size=64)
            f2[0].set_color(BLUE)
            f2[2].set_color(BLUE)
            f2[4].set_color(GREEN)
            f2[6].set_color(GREEN)
            f2.move_to(f)
            self.play(*edit(f, f2), run_time=min(1.5, c.until("latch", floor=0.8)))
            c.wait_until("latch")

            # {latch}: the same loop on a latch runs away while EN is high
            L = feedback_latch(_p(3.5, 1.6), s=1.0)
            L.en_l.shift(0.16 * LEFT)
            bw = buzz_window(w=2.4, h=0.5, gap=0.45, n=11).move_to(_p(3.8, -2.1))
            l_en = T("EN", 30, YELLOW).next_to(bw.clk, LEFT, buff=0.2).align_to(bw.clk, DOWN)
            l_q = T("Q", 32, RED).next_to(bw.buzz, LEFT, buff=0.2).set_x(l_en.get_x())
            self.play(*during(disappear(eq, ts, one), 0, 0.45),
                      *during([f2.animate.move_to(_p(FF3_C[0], -2.65))], 0.2, 0.7),
                      *during(appear(L, shift=None), 0.5, 1), run_time=1.8)
            self.play(FadeIn(bw.band), Create(bw.clk), *appear(l_en, l_q, shift=None, lag=0), run_time=1.0)
            self.play(Create(bw.buzz, rate_func=linear), L.loop.animate.set_stroke(RED),
                      L.q_w.animate.set_stroke(RED), run_time=min(3.5, c.until("safe", floor=1.0) - 0.3))
            c.wait_until("safe")

            # {safe}: back to the flip-flop: it listens only at the edge
            w3 = waves(1.0, 6.4, 4, 1.4, -0.2)
            self.play(*during(disappear(L, bw.band, bw.clk, bw.buzz, l_en, l_q), 0, 0.45),
                      *during([*appear(w3.clk_l, shift=None), Create(w3.clk, rate_func=linear),
                               *[FadeIn(u, scale=0.5) for u in w3.ups]], 0.45, 1),
                      run_time=1.4)
            self.play(*appear(w3.q_l, shift=None), Create(w3.qp[0]), run_time=0.5)
            for k in range(4):
                self.play(Create(w3.qp[k + 1]), fill_pulse(TL.ff.tri),
                          VShowPassingFlash(edge_line(w3.rises[k], 1.4, YELLOW), time_width=1.0),
                          run_time=0.7)
            c.wait_until("once")

            # {once}
            once = T("One edge, one flip", 44, t2c={"one flip": GREEN}).move_to(_p(3.7, -1.75))
            self.play(*appear(once), run_time=1.0)
