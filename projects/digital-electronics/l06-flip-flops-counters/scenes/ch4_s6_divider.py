"""Chapter 4, scene 6: counters as frequency dividers; the watch's 32,768 Hz crystal. Clips c4.div.1 – c4.div.3.

c4.div.1: s4's ripple_diagram() (no cause arrows) fades back in, shrunk 0.86 and nudged left so
GOLD frequency labels f, f/2, f/4, f/8 fit at the row ends; GOLD braces measure one period per row,
all from the left edge (lengths 1, 2, 4, 8 clock periods). {callback}: an inset of ch3_s4's toggle
trace + "half the frequency" in the band under the diagram.
c4.div.2: p. 95's sentence replaces the inset ("dividers" YELLOW on {name}); {more}: the diagram
clears, s3's ripple chain (bubble clocks) of 3 then 5 stages with f/2 … f/32, …; "n flip-flops:
f / 2^n"; {thousand}: "3 → ÷ 8", "10 → ÷ 1,024".
c4.div.3: s1's watch (scaled 0.66) with its quartz on the left; about 32 kHz → 32,768 Hz → = 2^15 Hz;
{chain}: 15 small T flip-flops (first three, ⋯, last three) from the crystal to the display;
{second}: the 1 Hz output flashes into the seconds, which tick 00 → 01. Ends empty.
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
    return VMobject().set_points_as_corners([_p(x, y) for x, y in pts]).set_stroke(color, width)


# =============================================================================================
# Shared with ch4_s5 / ch4_s6 (copy verbatim): ripple_diagram()
# =============================================================================================
RD_X0, RD_X1 = -5.1, 6.3                 # waves run x0 -> x1
RD_P = (RD_X1 - RD_X0) / 8.9             # clock period (1.281)
RD_FALL = [RD_X0 + RD_P + k * RD_P for k in range(8)]   # falling edges (guides), k = 0..7
RD_D = 0.2                               # propagation delay, drawn as a gap
RD_ROW_Y = [2.9, 1.5, 0.1, -1.3]         # CLK, Q0, Q1, Q2
RD_AMP = 0.3                             # levels at row_y ± AMP
RD_STUB = RD_X0 + 0.55                   # end of the reset stub on the Q rows


def _rd_y(row, bit):
    return RD_ROW_Y[row] + (RD_AMP if bit else -RD_AMP)


def _rd_poly(row, pts, color, width=4):
    return (VMobject().set_points_as_corners([_p(x, _rd_y(row, b)) for x, b in pts])
            .set_stroke(color, width))


def _rd_pieces(row, edges, color=GREEN):
    """Q trace cut into pieces: [0] reset stub, [1] flat to the first change, [k+2] starts with change k."""
    xs = [RD_STUB, *edges, RD_X1]
    out, b = [_rd_poly(row, [(RD_X0, 0), (RD_STUB, 0)], color)], 0
    for k in range(len(xs) - 1):
        if k == 0:
            pts = [(xs[0], b), (xs[1], b)]
        else:
            pts = [(xs[k], b), (xs[k], 1 - b), (xs[k + 1], 1 - b)]
            b = 1 - b
        out.append(_rd_poly(row, pts, color))
    return out


def _rd_cause(x_from, row_from, x_to, row_to):
    """Small YELLOW arrow: a fall on row_from (at x_from) triggers the change on row_to (at x_to)."""
    a, b = _p(x_from, _rd_y(row_from, 0) - 0.06), _p(x_to, _rd_y(row_to, 1) + 0.06)
    return Arrow(a, b, buff=0, stroke_width=3, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35).set_color(YELLOW)


class RippleDiagram(VGroup):
    """3-bit ripple counter timing diagram (slide p. 94), delays drawn.
    Rows CLK (YELLOW), Q0, Q1, Q2 (GREEN) at RD_ROW_Y; labels right-aligned at x0 - 0.35.
    CLK starts low, rises half a period before each falling edge RD_FALL[k] (k = 0..7), ends low.
    Q0 changes at fall[k] + d; Q1 at fall[1,3,5,7] + 2d; Q2 at fall[3,7] + 3d (d = RD_D).
    Parts: .labels (MathTex, final colours) .clk .downs (YELLOW ▼ on CLK at each fall) .guides (DIM)
    .q[r] (pieces, see _rd_pieces) .causes1 (Q0 -> Q1, 4) .causes2 (Q1 -> Q2, 2)."""

    def __init__(self, **kw):
        super().__init__(**kw)
        d = RD_D
        texs = [r"\mathrm{CLK}", "Q_0", "Q_1", "Q_2"]
        cols = [YELLOW, GREEN, GREEN, GREEN]
        self.labels = VGroup(*[
            MathTex(t, font_size=40, color=c).move_to(_p(0, y)).align_to(_p(RD_X0 - 0.35, 0), RIGHT)
            for t, c, y in zip(texs, cols, RD_ROW_Y)])
        pts = [(RD_X0, 0)]
        for f in RD_FALL:
            pts += [(f - RD_P / 2, 0), (f - RD_P / 2, 1), (f, 1), (f, 0)]
        pts.append((RD_X1, 0))
        self.clk = _rd_poly(0, pts, YELLOW)
        self.downs = VGroup(*[Triangle().rotate(PI).scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1)
                              .move_to(_p(f, RD_ROW_Y[0])) for f in RD_FALL])
        g_top, g_bot = _rd_y(0, 1) + 0.12, _rd_y(3, 0) - 0.12
        self.guides = VGroup(*[Line(_p(f, g_top), _p(f, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2)
                               for f in RD_FALL])
        self.e0 = [f + d for f in RD_FALL]
        self.e1 = [RD_FALL[k] + 2 * d for k in (1, 3, 5, 7)]
        self.e2 = [RD_FALL[k] + 3 * d for k in (3, 7)]
        self.q = [_rd_pieces(1, self.e0), _rd_pieces(2, self.e1), _rd_pieces(3, self.e2)]
        self.causes1 = [_rd_cause(RD_FALL[k] + d, 1, RD_FALL[k] + 2 * d, 2) for k in (1, 3, 5, 7)]
        self.causes2 = [_rd_cause(RD_FALL[k] + 2 * d, 2, RD_FALL[k] + 3 * d, 3) for k in (3, 7)]
        self.add(self.guides, self.labels, self.clk, self.downs, *self.q[0], *self.q[1], *self.q[2],
                 *self.causes1, *self.causes2)


def ripple_diagram():
    return RippleDiagram()
# =============================================================================================

# The diagram here: shrunk and nudged left so the frequency labels fit at the row ends.
DK, DSH = 0.86, _p(-0.55, 0.15)


def dpt(x, y):
    return _p(x, y) * DK + DSH


def period_brace(row, x_end):
    y = _rd_y(row, 0)
    return span_brace(dpt(RD_X0, y), dpt(x_end, y), color=GOLD, buff=0.1)


def freq_label(tex, row):
    return MathTex(tex, font_size=44, color=GOLD).next_to(dpt(RD_X1, RD_ROW_Y[row]), RIGHT, buff=0.3)


# ---- ch3's flip-flop symbol (ch3_s7_recap.make_ff, with s1's scale / lab_k) ------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
STUB_Y = 1.75
FEED_Y = -BOX_H / 2 - EN_WIRE


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False, scale=1.0, lab_k=1.0):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    if bubble:   # hollow: BG fill, stroke thinned with the scale
        bub = Circle(radius=0.1).set_stroke(FG, max(2, 3 * scale)).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.scale(scale, about_point=ORIGIN)
    for lab in g.labels:
        lab.scale(lab_k, about_point=lab.get_center())
    g.shift(_p(*center[:2]))
    return g


# ---- c4.div.2: s3's ripple chain, n stages, built at scale s ----------------------------------
CS = 0.52
C_PITCH = 4.3 * CS
C_X0, C_Y = -4.95, 1.45


def chain_stage(i, s=CS):
    """Stage i: flip-flop (T tied to 1), Q stub up to its GOLD f/2^(i+1) label; for i > 0 also the
    feed from the previous stage's Q (with its junction dot) into this clock."""
    x, y = C_X0 + i * C_PITCH, C_Y
    ff = make_ff(_p(x, y), ins=(("T", PIN_Y),), bubble=True, scale=s, lab_k=28 / (36 * s))
    one = MathTex("1", font_size=36, color=BLUE).next_to(ff.in_w[0].get_start(), LEFT, buff=0.1)
    jx = x + s * (BOX_W / 2 + WIRE + 0.4)
    stub = poly([(x + s * (BOX_W / 2 + WIRE), y + s * PIN_Y), (jx, y + s * PIN_Y), (jx, y + s * STUB_Y)],
                GREEN, 4)
    lab = MathTex("f" if i < 0 else f"f/{2 ** (i + 1)}", font_size=40, color=GOLD)
    lab.next_to(_p(jx, y + s * STUB_Y), UP, buff=0.1)
    g = VGroup(ff, one, stub)
    if i > 0:
        px = x - C_PITCH
        pjx = px + s * (BOX_W / 2 + WIRE + 0.4)
        ff.clk_w.set_stroke(GREEN)
        feed = poly([(pjx, y + s * PIN_Y), (pjx, y + s * FEED_Y), (x, y + s * FEED_Y)], GREEN, 4)
        dot = Dot(_p(pjx, y + s * PIN_Y), radius=0.07, color=GREEN)
        g.add(feed, dot)
    g.lab, g.ff = lab, ff
    return g


# ---- s1's watch and quartz (ch4_s1_hook, verbatim) ---------------------------------------------
WATCH_C = _p(0, 0.85)          # body centre
WATCH_W, WATCH_H = 8.6, 4.6     # body
CASE = "#1B1F26"                # body / strap fill
LCD = "#0A0C10"                 # display window fill
DIGITS = 72                     # Mono size of 12:00:00


def digital_watch(secs="00"):
    body = RoundedRectangle(corner_radius=0.6, width=WATCH_W, height=WATCH_H)
    body.set_stroke(DIM, 4).set_fill(CASE, 1).move_to(WATCH_C)
    top, bot = body.get_top()[1], body.get_bottom()[1]
    straps = VGroup(
        Polygon(_p(-2.3, top), _p(2.3, top), _p(2.0, top + 0.45), _p(-2.0, top + 0.45)),
        Polygon(_p(-2.3, bot), _p(2.3, bot), _p(2.0, bot - 0.45), _p(-2.0, bot - 0.45)),
    ).set_stroke(DIM, 4).set_fill(CASE, 1)
    window = RoundedRectangle(corner_radius=0.15, width=6.4, height=1.4)
    window.set_stroke(DIM, 3).set_fill(LCD, 1).move_to(WATCH_C + _p(0, 1.25))
    ref = Mono("12:00:00", DIGITS).move_to(window)

    def secs_text(s):
        full = Mono("12:00:" + s, DIGITS).move_to(ref).align_to(ref, LEFT)
        t = Mono(s, DIGITS, GOLD)
        t.align_to(full, RIGHT).align_to(full, DOWN)
        return t

    lead = Mono("12:00:", DIGITS).align_to(ref, LEFT).align_to(ref, DOWN)
    sec = secs_text(secs)
    g = VGroup(straps, body, window, lead, sec)
    g.straps, g.body, g.window, g.lead, g.secs = straps, body, window, lead, sec
    g.secs_text = secs_text
    return g


def quartz(center):
    """A small quartz can: rounded capsule with two leads (FG / DIM)."""
    can = RoundedRectangle(corner_radius=0.22, width=1.0, height=0.5).set_stroke(FG, 3).set_fill(PURPLE, 0.35)
    can.move_to(center)
    legs = VGroup(*[Line(can.get_left() + _p(0, dy), can.get_left() + _p(-0.25, dy)).set_stroke(DIM, 3)
                    for dy in (0.1, -0.1)])
    return VGroup(legs, can)


# ---- c4.div.3 layout ---------------------------------------------------------------------------
WK, W_C = 0.66, _p(0.6, 1.75)       # watch scale, body centre
QZ_C = _p(-4.6, 2.6)
LAB_C = _p(-4.6, 1.75)
MS = 0.42                           # mini flip-flop scale
M_Y = -2.1
M_XS = [-5.2, -3.6, -2.0, 0.8, 2.4, 4.0]
M_HZ = ["16{,}384", "8{,}192", "4{,}096", "4", "2", "1"]
M_JX = 0.84                         # Q pin -> junction
FEED_M = M_Y + MS * FEED_Y
QPIN_M = M_Y + MS * PIN_Y
STUB_M = M_Y + MS * STUB_Y


def mini_ff(x, clk_color=GREEN):
    """A small T flip-flop: box, T, clock triangle with a hollow bubble, Q wire (no Q-bar)."""
    s, hb = MS, MS * BOX_H / 2
    box = Rectangle(width=BOX_W * s, height=BOX_H * s).set_stroke(FG, 3).move_to(_p(x, M_Y))
    tri = Polygon(_p(x - 0.17 * s * 1.4, M_Y - hb), _p(x + 0.17 * s * 1.4, M_Y - hb),
                  _p(x, M_Y - hb + 0.26 * s * 1.4)).set_stroke(FG, 2).set_fill(BG, 1)
    bub = Circle(radius=0.065).set_stroke(FG, 1.5).set_fill(BG, 1).move_to(_p(x, M_Y - hb - 0.075))
    clk = Line(_p(x, FEED_M), _p(x, M_Y - hb - 0.14)).set_stroke(clk_color, 4)
    q = Line(_p(x + BOX_W * s / 2, QPIN_M), _p(x + M_JX, QPIN_M)).set_stroke(GREEN, 4)
    t = T("T", 28, BLUE).move_to(_p(x, M_Y + 0.05))
    return VGroup(clk, q, box, tri, bub, t)


class Divider(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------------------------------------
    def clip1(self):
        td = ripple_diagram()
        td.remove(*td.causes1, *td.causes2)
        td.scale(DK, about_point=ORIGIN).shift(DSH)
        self.td = td
        with self.say("c4.div.1") as c:
            self.play(FadeIn(td), run_time=1.2)
            c.wait_until("q0")

            # CLK: one period; f
            self.braces = [period_brace(0, RD_FALL[0]), period_brace(1, td.e0[1]),
                           period_brace(2, td.e1[1]), period_brace(3, td.e2[1])]
            self.flabs = [freq_label(t, r) for r, t in enumerate(["f", "f/2", "f/4", "f/8"])]
            self.play(GrowFromCenter(self.braces[0]), *appear(self.flabs[0]), run_time=1.2)
            c.wait_until("for every two")
            self.play(GrowFromCenter(self.braces[1]), run_time=1.5)
            c.wait_until("half the frequency")
            self.play(*appear(self.flabs[1]), run_time=1.0)

            # {callback}: ch3_s4's toggle trace, small
            c.wait_until("callback")
            x0, x1, p = -4.6, -0.8, 1.2
            rises = [x0 + 0.4 + k * p for k in range(3)]
            cy, qy, amp = -2.6, -3.15, 0.2
            pts = [(x0, 0)]
            for r in rises:
                pts += [(r, 0), (r, 1), (r + p / 2, 1), (r + p / 2, 0)]
            pts.append((x1, 0))
            clk = poly([(x, cy + (amp if b else -amp)) for x, b in pts], YELLOW, 3)
            qpts, b = [(x0, 0)], 0
            for r in rises:
                qpts += [(r, b), (r, 1 - b)]
                b = 1 - b
            qpts.append((x1, b))
            qtr = poly([(x, qy + (amp if b else -amp)) for x, b in qpts], GREEN, 3)
            labs = VGroup(MathTex(r"\mathrm{CLK}", font_size=30, color=DIM).move_to(_p(0, cy)),
                          MathTex("Q", font_size=30, color=DIM).move_to(_p(0, qy)))
            for m in labs:
                m.align_to(_p(x0 - 0.2, 0), RIGHT)
            cap = T("half the frequency", 34, GOLD).move_to(_p(1.75, (cy + qy) / 2))
            frame = RoundedRectangle(corner_radius=0.15, width=9.6, height=1.2)
            frame.set_stroke(DIM, 2).move_to(_p(-0.95, (cy + qy) / 2))
            self.inset = VGroup(frame, labs, clk, qtr, cap)
            self.play(FadeIn(frame), FadeIn(labs), FadeIn(clk), FadeIn(qtr), run_time=1.2)
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("q1")
            self.play(GrowFromCenter(self.braces[2]), run_time=1.5)
            c.wait_until("quarter")
            self.play(*appear(self.flabs[2]), run_time=1.0)

            c.wait_until("q2")
            self.play(GrowFromCenter(self.braces[3]), *appear(self.flabs[3]),
                      run_time=min(1.5, c.until() - 0.05))

    # -------------------------------------------------------------------------------------------
    def clip2(self):
        lines = ["“each has half the frequency, i.e., double the",
                 "repetition period of the previous one. This is why",
                 "counters are often known as dividers”"]
        sent = VGroup(*[T(s, 32) for s in lines]).arrange(DOWN, buff=0.18).move_to(_p(0, -2.85))
        word = select(sent[2], "dividers")[0]
        with self.say("c4.div.2") as c:
            self.play(*swap(self.inset, sent), run_time=1.4)   # early: the quote is shown whole, then read
            c.wait_until("name")
            self.play(*recolor(word, YELLOW), FlashUnder(word, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)

            # {more}: the diagram clears; s3's chain, then more stages
            c.wait_until("more")
            self.play(FadeOut(self.td, *self.braces, *self.flabs), run_time=0.8)
            stages = [chain_stage(i) for i in range(5)]
            ff0 = stages[0].ff
            clk_l = T("CLK", 30, YELLOW).next_to(ff0.clk_w.get_start(), DOWN, buff=0.1)
            f_in = MathTex("f", font_size=40, color=GOLD).next_to(clk_l, LEFT, buff=0.2)
            self.play(*appear(*stages[:3], lag=0.3, shift=None), FadeIn(clk_l), run_time=1.3)
            self.play(*appear(f_in, *[s.lab for s in stages[:3]], lag=0.2), run_time=1.0)
            c.wait_until("each one cuts")
            dots = MathTex(r"\ldots", font_size=48, color=GOLD)
            self.play(*appear(stages[3], stages[4], lag=0.5, shift=None), run_time=1.4)
            dots.next_to(stages[4].lab, RIGHT, buff=0.25).align_to(stages[4].lab, DOWN)
            self.play(*appear(stages[3].lab, stages[4].lab, dots, lag=0.3), run_time=1.0)
            self.chain = VGroup(*stages, *[s.lab for s in stages], dots, clk_l, f_in)

            c.wait_until("with n flip-flops")
            form = MathTex(r"n\ \text{flip-flops:}\quad", r"f\,/\,2^{n}", font_size=52)
            form[1].set_color(GOLD)
            form.move_to(_p(0, -1.4))
            self.form = form
            self.play(*appear(form), run_time=1.2)

            c.wait_until("thousand")
            r3 = MathTex(r"3", r"\ \rightarrow\ ", r"\div\, 8", font_size=52, color=GOLD).move_to(_p(-3.0, -2.85))
            r10 = MathTex(r"10", r"\ \rightarrow\ ", r"\div\, 1{,}024", font_size=52, color=GOLD).move_to(_p(2.8, -2.85))
            self.play(*swap(sent, r3), run_time=1.2)
            c.wait_until("ten flip-flops")
            self.play(*appear(r10), run_time=1.0)

    # -------------------------------------------------------------------------------------------
    def clip3(self):
        w = digital_watch("00")
        w.scale(WK, about_point=WATCH_C).shift(W_C - WATCH_C)
        qz = quartz(QZ_C)
        drop = 1.6 * DOWN               # sits centred until the chain needs the bottom band
        w.shift(drop)
        qz.shift(drop)
        with self.say("c4.div.3") as c:
            self.play(FadeOut(*self.mobjects), run_time=0.8)
            self.play(FadeIn(w), FadeIn(qz), run_time=1.2)

            c.wait_until("crystal")
            about = T("about 32 kHz", 34).move_to(LAB_C + drop)
            c.wait_until("about")
            self.play(*appear(about), run_time=1.0)

            c.wait_until("exact")
            exact = T("32,768 Hz", 38, GOLD).move_to(LAB_C + drop)
            self.play(*swap(about, exact), run_time=1.2)

            c.wait_until("power")
            pw = MathTex(r"=\ 2^{15}\ \mathrm{Hz}", font_size=48, color=GOLD).move_to(LAB_C + drop + _p(0, -0.75))
            self.play(*appear(pw), run_time=1.2)

            # {chain}: fifteen toggling flip-flops, crystal -> display
            c.wait_until("chain")
            self.play(*[m.animate.shift(-drop) for m in (w, qz, exact, pw)], run_time=1.0)
            lead_end = qz[0][0].get_end()
            xtal = poly([(lead_end[0], lead_end[1]), (-6.45, lead_end[1]), (-6.45, FEED_M),
                         (M_XS[0], FEED_M)], YELLOW, 4)
            ffs = [mini_ff(x, YELLOW if i == 0 else GREEN) for i, x in enumerate(M_XS)]
            wires, hz = [], []
            for i, x in enumerate(M_XS):
                jx = x + M_JX
                if i < 5:
                    wires.append(poly([(jx, QPIN_M), (jx, STUB_M)], GREEN, 4))
                    hz.append(MathTex(M_HZ[i], font_size=34, color=GOLD).next_to(_p(jx, STUB_M), UP, buff=0.08))
                if i in (0, 1, 3, 4):
                    wires.append(poly([(jx, QPIN_M), (jx, FEED_M), (M_XS[i + 1], FEED_M)], GREEN, 4))
            wires.append(poly([(M_XS[2] + M_JX, QPIN_M), (M_XS[2] + M_JX, FEED_M), (-0.65, FEED_M)], GREEN, 4))
            wires.append(poly([(0.25, FEED_M), (M_XS[3], FEED_M)], GREEN, 4))
            for m in hz[1:]:
                m.align_to(hz[0], DOWN)
            gap = MathTex(r"\cdots", font_size=48, color=GREEN).move_to(_p(-0.2, FEED_M))
            gap2 = MathTex(r"\cdots", font_size=48, color=GOLD).move_to(_p(-0.05, STUB_M + 0.25))
            win = w.window
            jx5 = M_XS[5] + M_JX
            out = poly([(jx5, QPIN_M), (jx5, win.get_center()[1]), (win.get_right()[0] + 0.02, win.get_center()[1])],
                       GREEN, 4)
            one_hz = T("1 Hz", 34, GOLD).next_to(_p(jx5, 0.4), RIGHT, buff=0.2)
            self.play(Create(xtal), *[time_span(FadeIn(f), 0.3 + 0.15 * i, 1.0 + 0.15 * i) for i, f in enumerate(ffs)],
                      run_time=1.5)
            self.play(*[FadeIn(m) for m in wires], FadeIn(gap), Create(out), run_time=1.0)
            self.play(*appear(*hz, gap2, lag=0.12), run_time=min(1.4, max(0.6, c.until("second") - 0.1)))

            c.wait_until("second")
            self.play(*appear(one_hz), VShowPassingFlash(out.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      run_time=1.2)
            new = Mono("01", DIGITS, GOLD).scale(WK).move_to(w.secs)
            self.play(*swap(w.secs, new, shift=0.15 * UP), run_time=0.8)

            c.wait_until("power of two")
            self.play(FlashAround(pw, color=GOLD, run_time=1.5, time_width=1.5), run_time=1.5)
