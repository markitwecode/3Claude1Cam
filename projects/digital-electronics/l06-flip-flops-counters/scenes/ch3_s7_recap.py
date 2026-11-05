"""Chapter 3, scene 7: recap in six tiles, then next time (counters). Clips c3.recap.1 – c3.recap.3.

Layout and styling follow ch2_s7_recap (vis_at / fit / caption / bump), here with six tiles
(three on top, three below). Tiles reuse, scaled down: s2's three symbols, s3's RS / J-K table rows,
s4's toggle traces, s5's t_table / xor_formula / toggle_loop, s6's async_sketch (helpers copied after
the s4-s6 fix passes). The closing chain is ch2_s7_recap's make_ff(ins=...) with a falling-edge
bubble: three T flip-flops (T tied to a BLUE 1), each Q clocking the next, three GREEN LEDs.
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


def bump(m, k):
    """Grow a label back by k about its own centre after its tile was shrunk."""
    return m.scale(k, about_point=m.get_center())


# ---- recap grid: 3 tiles on top, 3 below ------------------------------------------------------
TILE_X = (-4.55, 0.0, 4.55)
VIS_Y = (1.85, -1.45)
CAP_Y = (0.8, -2.57)           # caption tops
TILE_W, TILE_H = 4.1, (1.8, 2.0)
HEAD_Y = 3.3
LAB = 28                        # label size inside the tiles


def vis_at(i):
    return _p(TILE_X[i % 3], VIS_Y[i // 3])


def fit(m, i):
    s = min(TILE_W / m.width, TILE_H[i // 3] / m.height)
    m.scale(s, about_point=m.get_center())
    m.move_to(vis_at(i))
    return s


def caption(text, i, **kw):
    t = T(text, 28, line_spacing=0.8, **kw)
    return t.move_to(_p(vis_at(i)[0], CAP_Y[i // 3]), aligned_edge=UP).set_x(vis_at(i)[0])


# ---- ch2_s7_recap's make_ff (ins=...), plus s5's q_len and a falling-edge bubble ---------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False):
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
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def spread_q(f):
    """At tile size the bumped Q and Q-bar labels nearly touch (the bar reads as part of Q):
    move them apart to 0.3 of the box height above and below its centre."""
    c, h = f.box.get_center(), f.box.height
    f.labels[-2].move_to(c + _p(f.labels[-2].get_x() - c[0], 0.27 * h))
    f.labels[-1].move_to(c + _p(f.labels[-1].get_x() - c[0], -0.25 * h))


# ---- {r1}: s2's row of three symbols, the D ticked ----------------------------------------------
def panel_family():
    d = make_ff(_p(-3.4, 0))
    jk = make_ff(_p(0, 0), ins=(("J", PIN_Y), ("K", -PIN_Y)))
    tf = make_ff(_p(3.4, 0), ins=(("T", PIN_Y),))
    tick = check_mark(GREEN).scale(1.3).move_to(_p(-3.4, BOX_H / 2 + 0.6))
    g = VGroup(d, jk, tf, tick)
    s = fit(g, 0)
    g.remove(tick)
    for f in (d, jk, tf):
        for lab in f.labels:
            bump(lab, LAB / (36 * s))
        spread_q(f)
    g.d, g.jk, g.tf, g.tick = d, jk, tf, tick
    return g


# ---- {r2}: s3's RS and J-K tables (ch1_s2 grid_table), header and row 4 of each ---------------
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None, tk=1.0):
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size * MK, color=col)
            else:
                m = T(s, size=size * 0.82 * tk, color=col)   # tk: prose cells grown to read at tile size
            x = xs[j]
            if isinstance(x, tuple):
                m.move_to(_p(x[1], -i * pitch), aligned_edge=LEFT)
                m.set_y(-i * pitch)
            else:
                m.move_to(_p(x, -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g


TAB_XS = [0, 0.75, 1.9, 2.8, ("L", 3.75)]
TAB_SEPS = [1.32, 3.4]
TAB_PITCH = 0.66
QB = r"$\overline{Q}"
T_COL = 0.375
TK = 1.35
MK = 1.15


def panel_tables():
    rs = grid_table([["$S", "$R", "$Q'", r"$\overline{Q}\,'", "comment"],
                     ["$1", "$1", "$0", "$0", "illegal"]], TAB_XS, seps=TAB_SEPS, tk=TK)
    for m in rs.rows[1]:
        m.set_color(RED)
    jk = grid_table([["$J", "$K", "$Q'", r"$\overline{Q}\,'", "comment"],
                     ["$1", "$1", QB, "$Q", "toggle"]], TAB_XS, seps=TAB_SEPS, tk=TK)
    for m in jk.rows[0][0:2]:
        m.set_color(BLUE)
    for i in (0, 1):
        for m in jk.rows[i][2:4]:
            m.set_color(GREEN)
    jk.rows[1][4].set_color(YELLOW)
    jk.shift(1.5 * DOWN)
    a, b = rs.rows[1][0], jk.rows[1][0]
    arr = CurvedArrow(a.get_left() + 0.2 * LEFT, b.get_left() + 0.2 * LEFT, angle=2 * PI / 3,
                      color=YELLOW, stroke_width=5, tip_length=0.22)
    g = VGroup(rs, jk, arr)
    fit(g, 1)
    g.remove(arr)
    g.rs, g.jk, g.arr = rs, jk, arr
    return g


# ---- {r3}: s4's CLK and Q traces, f and f/2 ----------------------------------------------------
def clk_points(x0, x1, rises, period):
    pts = [(x0, 0)]
    for r in rises:
        pts += [(r, 0), (r, 1), (r + period / 2, 1), (r + period / 2, 0)]
    pts.append((x1, 0))
    return pts


def toggle_points(x0, x1, edges, start=0):
    pts, b = [(x0, start)], start
    for x in edges:
        pts += [(x, b), (x, 1 - b)]
        b = 1 - b
    pts.append((x1, b))
    return pts


def trace(pts, y_mid, amp=0.3, color=GREEN, width=4):
    return (VMobject().set_points_as_corners([_p(x, y_mid + (amp if b else -amp)) for x, b in pts])
            .set_stroke(color, width))


def toggle_trace(x0, x1, edges, y_mid, amp=0.3, start=0, color=GREEN, width=4):
    return trace(toggle_points(x0, x1, edges, start), y_mid, amp, color, width)


def panel_traces():
    x0, x1 = -1.3, 1.5
    per = (x1 - x0) / 4.3
    rises = [x0 + 0.5 * per + k * per for k in range(4)]
    cy, qy, amp = 0.5, -0.5, 0.25
    clk = trace(clk_points(x0, x1, rises, per), cy, amp, YELLOW)
    q = toggle_trace(x0, x1, rises, qy, amp)
    l_clk = MathTex(r"\mathrm{CLK}", font_size=34, color=DIM).move_to(_p(0, cy)).align_to(_p(x0 - 0.2, 0), RIGHT)
    l_q = MathTex("Q", font_size=34, color=DIM).move_to(_p(0, qy)).align_to(_p(x0 - 0.2, 0), RIGHT)
    f1 = MathTex("f", font_size=40, color=GOLD).next_to(_p(x1, cy), RIGHT, buff=0.2)
    f2 = MathTex("f/2", font_size=40, color=GOLD).next_to(_p(x1, qy), RIGHT, buff=0.2)
    g = VGroup(l_clk, l_q, clk, q, f1, f2)
    fit(g, 2)
    g.clk, g.q, g.f1, g.f2 = clk, q, f1, f2
    return g


# ---- {r4}: s5's T table and Q' = T xor Q -------------------------------------------------------
def t_table():
    tab = grid_table([["$T", "$Q'", r"$\overline{Q}\,'", "comment"],
                      ["$0", "$Q", QB, "hold"],
                      ["$1", QB, "$Q", "toggle"]],
                     [T_COL] + TAB_XS[2:], size=44, pitch=TAB_PITCH, seps=TAB_SEPS, tk=TK)
    r = tab.rows
    r[0][0].set_color(BLUE)
    for i in (0, 1, 2):
        for m in r[i][1:3]:
            m.set_color(GREEN)
    r[2][3].set_color(YELLOW)
    return tab


def xor_formula(size=84):
    f = MathTex("Q'", "=", "T", r"\oplus", "Q", font_size=size)
    f[0].set_color(GREEN)
    f[2].set_color(BLUE)
    f[4].set_color(GREEN)
    return f


def panel_t():
    tab = t_table()
    f = xor_formula(64).next_to(tab, DOWN, buff=0.4).set_x(tab.get_x())
    g = VGroup(tab, f)
    fit(g, 3)
    g.remove(f)
    g.tab, g.f = tab, f
    return g


# ---- {loop}: s5's toggle loop = a T flip-flop with T tied to 1 ----------------------------------
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


def panel_loop():
    tl = toggle_loop()
    eq = MathTex("=", font_size=96).move_to(_p(3.05, 0))
    ts = make_ff(_p(6.2, 0), ins=(("T", 0.0),))
    one = MathTex("1", font_size=52, color=BLUE).next_to(ts.in_w[0].get_start(), LEFT, buff=0.15)
    g = VGroup(tl, eq, ts, one)
    s = fit(g, 4)
    for lab in tl.ff.labels + ts.labels:
        bump(lab, LAB / (36 * s))
    bump(one, 36 / (52 * s))
    spread_q(tl.ff)
    spread_q(ts)
    one.next_to(ts.in_w[0].get_start(), LEFT, buff=0.08)
    g.tl, g.eq, g.ts, g.one = tl, eq, ts, one
    return g


def loop_caption(i):
    d = T("D =", 28, BLUE)
    d[1].set_color(FG)
    qb = qbar(28, GREEN)
    tog = T("toggles", 28)
    g = VGroup(d, qb, tog).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    qb.align_to(d, DOWN)
    return g.move_to(_p(vis_at(i)[0], CAP_Y[1]), aligned_edge=UP).set_x(vis_at(i)[0])


# ---- {r5}: s6's async timing sketch -------------------------------------------------------------
SK_X0, SK_X1 = -2.0, 6.5
SK_P = 1.6
SK_RISES = [SK_X0 + 0.5 + k * SK_P for k in range(5)]
SK_ROWS = {"CLK": 1.9, "CLR": 0.3, "Q": -1.4}
SK_AMP = 0.3
SK_A = SK_RISES[0] + 0.3 * SK_P
SK_B = SK_RISES[0] + 0.55 * SK_P


def async_sketch():
    """s6's sketch (no .values, .mark without its text: the caption says it)."""
    g = VGroup()
    y = lambda row, v: SK_ROWS[row] + (SK_AMP if v else -SK_AMP)  # noqa: E731
    r = SK_RISES
    g.labels = VGroup(*[T(n, 30, c).move_to(_p(0, SK_ROWS[n])).align_to(_p(SK_X0 - 0.25, 0), RIGHT)
                        for n, c in (("CLK", YELLOW), ("CLR", RED), ("Q", GREEN))])
    pts = [(SK_X0, y("CLK", 0))]
    for x in r:
        pts += [(x, y("CLK", 0)), (x, y("CLK", 1)), (x + SK_P / 2, y("CLK", 1)), (x + SK_P / 2, y("CLK", 0))]
    pts.append((SK_X1, y("CLK", 0)))
    g.clk = poly(pts, YELLOW)
    top, bot = y("CLK", 1) + 0.15, y("Q", 0) - 0.15
    g.guides = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 1.5).set_z_index(-2) for x in r])
    g.ups = VGroup(*[Triangle().scale(0.11).set_stroke(width=0).set_fill(YELLOW, 1)
                     .move_to(_p(x, SK_ROWS["CLK"])) for x in r])
    lo, hi = y("CLR", 0), y("CLR", 1)
    g.clr = poly([(SK_X0, lo), (SK_A, lo), (SK_A, hi), (SK_B, hi), (SK_B, lo), (SK_X1, lo)], RED)
    g.pulse = poly([(SK_A, lo), (SK_A, hi), (SK_B, hi), (SK_B, lo)], RED, 10)
    qh, ql = y("Q", 1), y("Q", 0)
    g.q_unk0 = VGroup(poly([(SK_X0, qh), (r[0], qh)], GREEN), poly([(SK_X0, ql), (r[0], ql)], GREEN))
    g.q_unk1 = VGroup(poly([(r[0], qh), (SK_A, qh)], GREEN), poly([(r[0], ql), (SK_A, ql)], GREEN))
    g.q_drop = poly([(SK_A, qh), (SK_A, ql), (r[1], ql)], GREEN)
    g.q_known = poly([(r[1], ql), (r[1], qh), (r[2], qh), (r[2], ql), (r[3], ql), (r[3], qh),
                      (r[4], qh), (r[4], ql), (SK_X1, ql)], GREEN)
    g.mark = DashedLine(_p(SK_A, lo - 0.1), _p(SK_A, qh + 0.1), dash_length=0.1).set_stroke(RED, 3)
    g.add(g.guides, g.labels, g.clk, g.ups, g.clr, g.q_unk0, g.q_unk1, g.q_drop, g.q_known, g.mark)
    return g


def panel_async():
    g = async_sketch()
    s = fit(g, 5)
    for lab in g.labels:
        bump(lab, LAB / (30 * s))
        lab.align_to(g.clk.get_left() + 0.12 * LEFT, RIGHT)
    g.move_to(vis_at(5))
    return g


# ---- {next}: three toggling flip-flops in a ripple chain, three GREEN LEDs ----------------------
CH_X = (-4.3, 0.0, 4.3)
LED_Y = 2.3
CH_K = 0.85
CH_C = _p(0, 0.5)


def led(on=False):
    c = Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)
    return c


def ripple_chain():
    hb = BOX_H / 2
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True) for x in CH_X]
    ones = [MathTex("1", font_size=44, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    wires, dots, leds = [], [], []
    for k, x in enumerate(CH_X):
        jx = x + BOX_W / 2 + WIRE + 0.4
        w = [_p(x + BOX_W / 2 + WIRE, PIN_Y), _p(jx, PIN_Y), _p(jx, LED_Y - 0.21)]
        wires.append(VMobject().set_points_as_corners(w).set_stroke(GREEN, 5))
        leds.append(led().move_to(_p(jx, LED_Y)))
        if k < 2:
            ffs[k + 1].clk_w.set_stroke(GREEN)
            down = [_p(jx, PIN_Y), _p(jx, -hb - EN_WIRE), _p(CH_X[k + 1], -hb - EN_WIRE)]
            wires.append(VMobject().set_points_as_corners(down).set_stroke(GREEN, 5))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    names = [MathTex(f"Q_{k}", font_size=40, color=GREEN).next_to(l, RIGHT, buff=0.12)
             for k, l in enumerate(leds)]
    g = VGroup(*ffs, *ones, *wires, *dots, *leds, *names, clk_l)
    g.scale(CH_K, about_point=ORIGIN).move_to(CH_C)
    g.names = names
    g.ffs, g.ones, g.wires, g.dots, g.leds, g.clk_l = ffs, ones, wires, dots, leds, clk_l
    return g


def count_leds(leds, values):
    """The LEDs show `values` in turn (LED 0 = least significant bit), ending on values[-1]."""
    n = len(values)

    def f_for(bit):
        def f(m, a):
            v = values[min(int(a * n), n - 1)]
            m.set_fill(GREEN, 0.9 if (v >> bit) & 1 else 0.0)
        return f
    return [UpdateFromAlphaFunc(l, f_for(b)) for b, l in enumerate(leds)]


class Recap(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def show_tile(self, panel, cap, rt=1.5):
        prev = self.tiles[-1] if self.tiles else []
        anims = [*set_alpha(prev, 0.5), *appear(panel, shift=None), *during(appear(cap), 0.4, 1.0)]
        self.play(*anims, run_time=rt)  # early: recap tile, seen whole
        self.tiles.append([panel, cap])

    # ------------------------------------------------------------------ c3.recap.1
    def clip1(self):
        with self.say("c3.recap.1") as c:
            head = T("Recap", 44).move_to(_p(0, HEAD_Y))
            self.play(*appear(head), run_time=1.0)

            # {r1}: the three symbols; D ticked, J-K and T dimmed
            p1 = panel_family()
            cap1 = caption("D in modern designs;\nJ-K, T for completeness", 0)
            c.wait_until("r1")
            self.show_tile(p1, cap1)
            c.wait_until("dee flip-flops")
            self.play(Create(p1.tick), FlashAround(p1.d.box, color=GREEN, time_width=1.5, buff=0.08),
                      run_time=1.2)
            c.wait_until("jay-kay")
            self.play(*set_alpha([p1.jk, p1.tf], 0.4), run_time=1.0)
            p1.add(p1.tick)

            # {r2}: RS row 4 illegal -> J-K row 4 toggle
            p2 = panel_tables()
            cap2 = caption("J-K: the illegal state\nbecomes toggle", 1,
                           t2c={"illegal": RED, "toggle": YELLOW})
            c.wait_until("r2")
            self.show_tile(p2, cap2)
            c.wait_until("illegal state")
            self.play(*flash([p2.rs.rows[1]], color=RED, time_width=1.5, buff=0.08), run_time=1.2)
            c.wait_until("replaced by toggle")
            self.play(Create(p2.arr), *flash([p2.jk.rows[1]], color=YELLOW, time_width=1.5, buff=0.08),
                      run_time=min(1.4, c.until("r3") - 0.1))
            p2.add(p2.arr)

            # {r3}: CLK f, Q f/2
            p3 = panel_traces()
            cap3 = caption("toggling halves\nthe frequency", 2, t2c={"halves": GOLD})
            c.wait_until("r3")
            self.show_tile(p3, cap3)
            c.wait_until("square wave")
            self.play(VShowPassingFlash(p3.q.copy().set_stroke(GREEN, 8), time_width=0.5), run_time=1.2)
            c.wait_until("half")
            self.play(*flash([p3.f2], color=GOLD, time_width=1.5, buff=0.08),
                      run_time=min(1.2, c.until(floor=0.6)))

    # ------------------------------------------------------------------ c3.recap.2
    def clip2(self):
        with self.say("c3.recap.2") as c:
            # {r4}: the T table, then Q' = T xor Q
            p4 = panel_t()
            cap4 = caption("T: 0 holds, 1 toggles", 3, t2c={"T:": BLUE, "toggles": YELLOW})
            self.show_tile(p4, cap4)
            c.wait_until("holds")
            self.play(*flash([p4.tab.rows[1]], time_width=1.5, buff=0.06), run_time=1.0)
            c.wait_until("toggles")
            self.play(*flash([p4.tab.rows[2]], time_width=1.5, buff=0.06), run_time=1.0)
            c.wait_until("cue prime")
            self.play(*appear(p4.f, shift=0.15 * DOWN), run_time=1.2)
            p4.add(p4.f)

            # {loop}: D = Q-bar fed back = T at 1
            p5 = panel_loop()
            cap5 = loop_caption(4)
            c.wait_until("loop")
            self.show_tile(p5, cap5)
            c.wait_until("fed back")
            self.play(VShowPassingFlash(p5.tl.loop.copy().set_stroke(GREEN, 9), time_width=0.6),
                      run_time=1.4)
            c.wait_until("tee at one")
            self.play(*flash([p5.one], color=BLUE, time_width=1.5, buff=0.08), run_time=1.2)

            # {r5}: CLR forces Q to 0 between edges
            p6 = panel_async()
            cap6 = caption("PRE and CLR:\nno edge needed", 5, t2c={"PRE": RED, "CLR": RED})
            c.wait_until("r5")
            self.show_tile(p6, cap6)
            c.wait_until("clear")
            self.play(VShowPassingFlash(p6.pulse.copy(), time_width=1.0, taper_width=0.1), run_time=1.3)
            c.wait_until("at once")
            self.play(VShowPassingFlash(p6.q_drop.copy().set_stroke(GREEN, 9), time_width=1.0),
                      VShowPassingFlash(p6.mark.copy().set_stroke(RED, 5), time_width=1.0), run_time=1.3)
            c.wait_until()

    # ------------------------------------------------------------------ c3.recap.3
    def clip3(self):
        with self.say("c3.recap.3") as c:
            # {next}: everything clears; the ripple chain
            title = T("Next: counters", 48, t2c={"Next:": YELLOW}).move_to(_p(0, 3.35))
            sweep_clear(self, *appear(title), run_time=1.4)
            ch = ripple_chain()
            parts = [VGroup(f, o) for f, o in zip(ch.ffs, ch.ones)]
            self.play(*appear(*parts, shift=None, lag=0.25), run_time=1.4)
            self.play(*[Create(w) for w in ch.wires], *[FadeIn(d) for d in ch.dots],
                      *[FadeIn(l) for l in ch.leds], *appear(ch.clk_l, *ch.names, shift=None),  # early: the circuit's pin names, shown with it
                      run_time=min(1.3, c.until("ripple") - 0.1))
            self.chain = ch

            # {ripple}: simplest to build, worst to use
            good = T("simplest to build", 40, GOLD).move_to(_p(0, -2.4))
            bad = T("worst to use", 40, RED).move_to(_p(0, -3.1))
            c.wait_until(own_word=good)
            self.play(*appear(good), run_time=1.0)
            c.wait_until(own_word=bad)
            self.play(*appear(bad), run_time=1.0)
        # end card, carried by the music: the LEDs count up once
        self.play(*count_leds(self.chain.leds, list(range(1, 8))), rate_func=linear, run_time=7.3)
