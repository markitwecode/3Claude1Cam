"""Chapter 5, scene 8: recap in six tiles, then next time (from table to circuit). Clips c5.recap.1 – c5.recap.2.

Grid, captions and show_tile as ch3_s7_recap / ch4_s8_recap (three tiles on top, three below, the
previous tile dims to 0.5). Tiles reuse, scaled down: s2's sync_structure() with the YELLOW "?" as
at s2's {job} (inner pin letters dropped at this size); s3's DIM unfolded RS table beside the
counter table's header groups, the BLUE D group growing in under the YELLOW "excitation" brace;
s4's d_exc_table() + "D = Q'"; s5's jk_exc_table() with its x cells pulsed YELLOW; s6's 0-to-7
table (rebuilt at tile size, one header per group) with the YELLOW "="; s7's Q0 | Q0' | J0 K0
columns, all 1s. {next}: the other tiles fade out, s6's table grows to the centre, three BLUE
arrows leave its D columns towards three faint gate outlines, a tiny K-map grid beside them.
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


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


def bump(m, k):
    """Grow a label back by k about its own centre after its tile was shrunk."""
    return m.scale(k, about_point=m.get_center())


def thin(g, k):
    """Strokes do not scale with the tile: thin them by k so small parts keep their shape."""
    for m in g.family_members_with_points():
        w = m.get_stroke_width()
        if w > 0:
            m.set_stroke(width=max(1.0, w * k))
    return g


# ---- recap grid: 3 tiles on top, 3 below (tile widths differ: the tables are narrow) ----------
TILE_X = ((-4.6, 0.7, 5.15), (-4.4, 0.0, 4.6))
VIS = ((1.1, 3.6), (-2.75, -0.25))     # visual band (bottom, top) per row
CAP_TOP = (0.95, -2.9)                # caption tops
TS = 27                                 # cell / label size inside the tiles


def vis_at(i):
    r = i // 3
    return _p(TILE_X[r][i % 3], (VIS[r][0] + VIS[r][1]) / 2)


def caption(text, i, **kw):
    t = T(text, 28, line_spacing=0.8, **kw)
    return t.move_to(_p(vis_at(i)[0], CAP_TOP[i // 3]), aligned_edge=UP).set_x(vis_at(i)[0])


def tile_grid(rows, xs, pitch=0.27, head_gap=0.38, size=TS, seps=(), color=FG):
    """A table at tile size: rows of MathTex strings, header at y = 0, data row i (1..) at
    y = -head_gap - (i - 1) * pitch; column centres xs; DIM separators and header rule."""
    out = []
    ys = [0.0] + [-head_gap - k * pitch for k in range(len(rows) - 1)]
    for row, y in zip(rows, ys):
        out.append(VGroup(*[MathTex(s, font_size=size, color=color).move_to(_p(x, y))
                            for s, x in zip(row, xs)]))
    top, bot = 0.2, ys[-1] - 0.17
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.15, -head_gap / 2 - 0.01),
                   _p(out[0].get_right()[0] + 0.15, -head_gap / 2 - 0.01)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines, g.ys = out, lines, ys
    return g


# ---- {r1}: ch5_s2_sync's sync_structure (copied) ------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CH_X = (-4.3, 0.0, 4.3)
FEED_Y = -BOX_H / 2 - EN_WIRE


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


def sync_structure(k=0.85, center=_p(0, -0.45)):
    ffs = [make_ff(_p(x, 0)) for x in CH_X]
    bus = Line(_p(CH_X[0], FEED_Y), _p(CH_X[2], FEED_Y)).set_stroke(YELLOW, 5)
    jdot = Dot(_p(CH_X[1], FEED_Y), radius=0.09, color=YELLOW)
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    q_labels = [MathTex(f"Q_{i}", font_size=48, color=GREEN).move_to(_p(x + 1.15, 2.0))
                for i, x in enumerate(CH_X)]
    d_labels = [MathTex(f"D_{i}", font_size=48, color=BLUE).move_to(_p(x - 1.15, 2.0))
                for i, x in enumerate(CH_X)]
    box_y0, box_h = 2.5, 1.5
    box = RoundedRectangle(corner_radius=0.3, width=12.4, height=box_h).set_stroke(BLUE, 4)
    box.set_fill(BG, 1).move_to(_p(0, box_y0 + box_h / 2))
    box_l = T("combinational logic", 52, FG).move_to(box)
    q_up = [poly([(x + BOX_W / 2 + WIRE, PIN_Y), (x + BOX_W / 2 + WIRE, box_y0)], GREEN) for x in CH_X]
    d_down = [poly([(x - BOX_W / 2 - WIRE, box_y0), (x - BOX_W / 2 - WIRE, PIN_Y)], BLUE) for x in CH_X]
    cur_l = VGroup(T("current", 35, GREEN), T("state", 35, GREEN)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    cur_l.next_to(_p(CH_X[2] + 1.6, 1.55), RIGHT, buff=0.15)
    next_l = VGroup(T("next", 35, BLUE), T("state", 35, BLUE)).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
    next_l.next_to(_p(CH_X[0] - 1.6, 1.55), LEFT, buff=0.15)
    g = VGroup(*ffs, bus, jdot, clk_l, *q_labels, *d_labels, *q_up, *d_down, box, box_l, cur_l, next_l)
    g.scale(k, about_point=ORIGIN).shift(center)
    g.ffs, g.bus, g.jdot, g.clk_l, g.q_labels, g.d_labels = ffs, bus, jdot, clk_l, q_labels, d_labels
    g.q_up, g.d_down, g.box, g.box_l, g.cur_l, g.next_l = q_up, d_down, box, box_l, cur_l, next_l
    return g


def panel_sync():
    """The structure as at s2's {job}: pin letters, Q/D labels and side labels gone, "?" in the box."""
    S = sync_structure(k=1.0, center=ORIGIN)
    S.remove(*S.q_labels, *S.d_labels, S.box_l, S.cur_l, S.next_l)
    for f in S.ffs:
        f.remove(f.d_l, f.q_l, f.qb_l)
    qm = T("?", 64, YELLOW, weight=BOLD).move_to(S.box)
    S.add(qm)
    s = 3.8 / S.box.width
    S.scale(s, about_point=ORIGIN)
    thin(S, 0.55)
    bump(qm, 38 / (64 * s))
    bump(S.clk_l, TS / (36 * s)).next_to(S.ffs[0].clk_w.get_start(), DOWN, buff=0.06)
    S.move_to(vis_at(0))
    S.qm = qm
    return S


# ---- {r2}: s3's DIM RS table beside the counter table's header groups --------------------------
RS_XS = [0, 0.45, 0.8, 1.35]
GP = 1.3                                 # skeleton group pitch


def panel_skeleton():
    q01 = [0, 0, 1, 0, 1, 0, 1, 0]
    rows = [["Q", "S", "R", "Q'"]] + [[str(i // 4), str((i >> 1) & 1), str(i & 1), str(q01[i])] for i in range(8)]
    rs = tile_grid(rows, RS_XS, seps=[1.08], color=DIM)
    hy = rs.ys[2] - 0.1                  # the counter table's header row sits lower: room for the brace
    x0 = 1.5 + 0.45 + 0.55
    heads = [MathTex(r"Q_2\,Q_1\,Q_0", font_size=TS, color=GREEN),
             MathTex(r"Q_2'\,Q_1'\,Q_0'", font_size=TS, color=GREEN),
             MathTex(r"D_2\,D_1\,D_0", font_size=TS, color=BLUE)]
    for k, h in enumerate(heads):
        h.move_to(_p(x0 + k * GP, hy))
    bot = rs.ys[-1] - 0.17
    seps = [Line(_p(x0 + (k + 0.5) * GP, hy + 0.2), _p(x0 + (k + 0.5) * GP, bot)).set_stroke(DIM, 2)
            for k in range(2)]
    ry = hy - 0.19
    rule_a = Line(_p(x0 - 0.62, ry), _p(x0 + 1.5 * GP, ry)).set_stroke(DIM, 2)
    rule_b = Line(_p(x0 + 1.5 * GP, ry), _p(x0 + 2 * GP + 0.62, ry)).set_stroke(DIM, 2)
    br = Brace(heads[2], UP, buff=0.08, color=YELLOW)
    ex = T("excitation", TS, YELLOW).next_to(br, UP, buff=0.05)
    base = VGroup(rs, heads[0], heads[1], seps[0], rule_a)
    g = VGroup(base, heads[2], seps[1], rule_b, br, ex)
    g.move_to(vis_at(1))
    g.remove(heads[2], seps[1], rule_b, br, ex)
    g.base, g.dgroup, g.br, g.ex = base, [heads[2], seps[1], rule_b], br, ex
    return g


# ---- {r3}: ch5_s4_dexcite's d_exc_table (copied) -----------------------------------------------
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            m = MathTex(s[1:], font_size=size, color=col) if s.startswith("$") else T(s, size=size * 0.82, color=col)
            m.move_to(_p(xs[j], -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g


D_XS = [0, 0.9, 2.1]
D_SEPS = [1.5]


def d_exc_table():
    rows = [["$Q", "$Q'", "$D"],
            ["$0", "$0", "$0"],
            ["$0", "$1", "$1"],
            ["$1", "$0", "$0"],
            ["$1", "$1", "$1"]]
    tab = grid_table(rows, D_XS, size=44, pitch=0.66, seps=D_SEPS)
    h = tab.rows[0]
    h[0].set_color(GREEN)
    h[1].set_color(GREEN)
    h[2].set_color(BLUE)
    return tab


def panel_dexc():
    tab = d_exc_table().scale(0.6)
    rule = MathTex("D", "=", "Q'", font_size=36)
    rule[0].set_color(BLUE)
    rule[2].set_color(GREEN)
    rule.next_to(tab, DOWN, buff=0.12)
    g = VGroup(tab, rule).move_to(vis_at(2))
    g.remove(rule)
    g.tab, g.rule = tab, rule
    return g


# ---- {r4}: ch5_s5_jkexcite's jk_exc_table (copied) ---------------------------------------------
R_XS = [0, 0.85, 2.95, 3.95]
R_SEPS = [1.9]


def jk_exc_table(pitch=0.8, x_color=FG):
    rows = [["$Q", "$Q'", "$J", "$K"],
            ["$0", "$0", "$0", "$x"],
            ["$0", "$1", "$1", "$x"],
            ["$1", "$0", "$x", "$1"],
            ["$1", "$1", "$x", "$0"]]
    tab = grid_table(rows, R_XS, size=44, pitch=pitch, seps=R_SEPS)
    h = tab.rows[0]
    h[0].set_color(GREEN)
    h[1].set_color(GREEN)
    h[2].set_color(BLUE)
    h[3].set_color(BLUE)
    tab.xs = [tab.rows[1][3], tab.rows[2][3], tab.rows[3][2], tab.rows[4][2]]
    for m in tab.xs:
        m.set_color(x_color)
    return tab


def pulse(m, to=YELLOW, base=FG, end=None, s=0.0, e=1.0):
    """Colour pulse base -> to -> end (default base) with a small swell, in [s, e] of the play."""
    ref = m.copy()
    end = base if end is None else end

    def f(mob, a):
        t = min(1.0, max(0.0, (a - s) / (e - s)))
        k = there_and_back(t)
        col = interpolate_color(ManimColor(base), ManimColor(to), k) if t < 0.5 else \
            interpolate_color(ManimColor(end), ManimColor(to), k)
        mob.become(ref.copy().scale(1 + 0.35 * k).set_color(col))
    return UpdateFromAlphaFunc(m, f, rate_func=linear)


def panel_jkexc():
    tab = jk_exc_table().scale(0.6).move_to(vis_at(3))
    return tab


# ---- {r5}: s6's 0-to-7 table at tile size, one header per group, the YELLOW "=" ----------------
M_X = {"dec": 0.0, "g": (0.85, 0.85 + GP, 0.85 + 2 * GP)}
M_DX = 0.3


def panel_mod():
    heads = ["", r"Q_2\,Q_1\,Q_0", r"Q_2'\,Q_1'\,Q_0'", r"D_2\,D_1\,D_0"]
    hcol = [GREEN, GREEN, BLUE]
    hs = [MathTex(h, font_size=TS, color=c).move_to(_p(x, 0)) for h, c, x in zip(heads[1:], hcol, M_X["g"])]
    ys = [-0.38 - k * 0.27 for k in range(8)]
    dec, cur, nxt, inp = VGroup(), VGroup(), VGroup(), VGroup()
    for i, y in enumerate(ys):
        dec.add(MathTex(str(i), font_size=TS, color=GOLD).move_to(_p(M_X["dec"], y)))
        for grp, v, gx in ((cur, i, M_X["g"][0]), (nxt, (i + 1) % 8, M_X["g"][1]), (inp, (i + 1) % 8, M_X["g"][2])):
            grp.add(VGroup(*[MathTex(b, font_size=TS).move_to(_p(gx + (j - 1) * M_DX, y))
                             for j, b in enumerate(format(v, "03b"))]))
    bot = ys[-1] - 0.17
    lines = VGroup(*[Line(_p(M_X["g"][k] + GP / 2, 0.2), _p(M_X["g"][k] + GP / 2, bot)).set_stroke(DIM, 2)
                     for k in range(2)])
    lines.add(Line(_p(-0.25, -0.2), _p(M_X["g"][2] + 0.62, -0.2)).set_stroke(DIM, 2))
    eq = set_backstroke(MathTex("=", font_size=40, color=YELLOW), width=10)
    eq.move_to(_p(M_X["g"][1] + GP / 2, (ys[0] + ys[-1]) / 2))
    g = VGroup(lines, *hs, dec, cur, nxt, inp, eq).move_to(vis_at(4))
    g.remove(eq)
    g.heads, g.lines, g.dec, g.cur, g.nxt, g.inp, g.eq = hs, lines, dec, cur, nxt, inp, eq
    return g


# ---- {r6}: s7's Q0 | Q0' | J0 K0 columns, all 1s after the swap ---------------------------------
J_XS = [0, 0.62, 1.4, 1.95]


def panel_jk0():
    rows = [["Q_0", "Q_0'", "J_0", "K_0"]] + [[str(i % 2), str(1 - i % 2), "1", "1"] for i in range(8)]
    tab = tile_grid(rows, J_XS, seps=[1.02])
    for k, c in enumerate([GREEN, GREEN, BLUE, BLUE]):
        tab.rows[0][k].set_color(c)
    mid = (tab.ys[1] + tab.ys[-1]) / 2
    h = tab.ys[1] - tab.ys[-1] + 0.3
    strips = [Rectangle(width=0.36, height=h).set_stroke(BLUE, 2, opacity=0.35).set_fill(BLUE, 0.06)
              .move_to(_p(x, mid)).set_z_index(-2) for x in J_XS[2:]]
    g = VGroup(*strips, tab).move_to(vis_at(5))
    g.tab, g.strips = tab, strips
    g.ones = [r[k] for r in tab.rows[1:] for k in (2, 3)]
    return g


def row_box(tab, i, left, right, color=YELLOW):
    y = tab.rows[i][0].get_y()
    return (Rectangle(width=right - left, height=0.25).set_stroke(color, 2.5).set_fill(color, 0.12)
            .move_to(_p((left + right) / 2, y)).set_z_index(-1))


# ---- {next}: faint gates and a tiny K-map (ch4_s8's and_gate, copied) ---------------------------
class Gate(VGroup):
    def __init__(self, body, ins, out, color=BLUE):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body, *self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def and_gate(color=BLUE):
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


TAB_C, TAB_K = _p(-1.95, -0.25), 1.6
GATE_X, GATE_YS = 3.75, (1.05, -0.25, -1.55)
KMAP_C, KMAP_S = _p(5.75, -0.25), 0.36


def faint_gates():
    gs = []
    for y in GATE_YS:
        g = and_gate(color=DIM).scale(0.6).move_to(_p(GATE_X, y))
        g.body.set_stroke(DIM, 3, opacity=0.7)
        stub = Line(g.out(), g.out() + 0.35 * RIGHT).set_stroke(DIM, 3, opacity=0.7)
        gs.append(VGroup(g, stub))
    return gs


def tiny_kmap():
    cells = VGroup(*[Square(KMAP_S).set_stroke(DIM, 2).move_to(KMAP_C + _p((c - 1.5) * KMAP_S, (0.5 - r) * KMAP_S))
                     for r in range(2) for c in range(4)])
    lab = T("K-map", 28, DIM).next_to(cells, UP, buff=0.18)
    return cells, lab


# ------------------------------------------------------------------------------------------------
class Recap(NarratedScene):
    def construct(self):
        self.tiles = []
        self.clip1()
        self.clip2()
        self.wait(7.6)                       # end card, carried by the music
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def show_tile(self, panel, cap, rt=1.5):
        prev = self.tiles[-1] if self.tiles else []
        anims = [*set_alpha(prev, 0.5), *appear(panel, shift=None), *during(appear(cap), 0.4, 1.0)]
        self.play(*anims, run_time=rt)  # early: recap tile, seen whole
        self.tiles.append([panel, cap])

    # ------------------------------------------------------------------ c5.recap.1
    def clip1(self):
        with self.say("c5.recap.1") as c:
            # {r1}: three D flip-flops on one clock, the logic box with its "?"
            p1 = panel_sync()
            cap1 = caption("one clock, logic\nmakes the inputs", 0, t2c={"one clock,": YELLOW, "inputs": BLUE})
            c.wait_until("r1")
            self.show_tile(p1, cap1)
            c.wait_until("one clock")
            self.play(VShowPassingFlash(p1.bus.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      *[VShowPassingFlash(f.clk_w.copy().set_stroke(YELLOW, 8), time_width=0.6) for f in p1.ffs],
                      run_time=1.3)
            c.wait_until("combinational logic")
            self.play(*during([VShowPassingFlash(w.copy().set_stroke(GREEN, 8), time_width=0.6) for w in p1.q_up],
                              0, 0.5),
                      *during([p1.box.animate(rate_func=there_and_back).set_stroke(YELLOW, 6)], 0.3, 0.7),
                      *during([VShowPassingFlash(w.copy().set_stroke(BLUE, 8), time_width=0.6) for w in p1.d_down],
                              0.5, 1.0),
                      run_time=min(2.2, c.until("r2") - 0.1))

            # {r2}: the DIM RS table beside the counter's table; the D group grows in
            p2 = panel_skeleton()
            cap2 = caption("the modified table\nadds the inputs", 1, t2c={"inputs": BLUE})
            c.wait_until("r2")
            self.show_tile(p2, cap2)
            c.wait_until("inputs needed")
            self.play(*[FadeIn(m, shift=0.4 * LEFT) for m in p2.dgroup], run_time=1.2)
            c.wait_until(own_word=p2.ex, cue="excitation")
            self.play(GrowFromCenter(p2.br), *appear(p2.ex), run_time=1.0)
            p2.add(*p2.dgroup, p2.br, p2.ex)

            # {r3}: the D excitation table, then D = Q'
            p3 = panel_dexc()
            cap3 = caption("excitation works\nbackwards", 2, t2c={"backwards": YELLOW})
            c.wait_until("r3")
            self.show_tile(p3, cap3)
            c.wait_until("dee equals")
            self.play(*appear(p3.rule, shift=0.15 * DOWN), run_time=min(1.0, c.until(floor=0.4)))
            p3.add(p3.rule)

    # ------------------------------------------------------------------ c5.recap.2
    def clip2(self):
        with self.say("c5.recap.2") as c:
            # {r4}: the J-K excitation table; its four x cells light up
            p4 = panel_jkexc()
            cap4 = caption("one don't care per row", 3, t2c={"don't care": YELLOW})
            self.show_tile(p4, cap4)
            c.wait_until("don't care")
            self.play(*[pulse(m, end=YELLOW, s=0.2 * k, e=0.2 * k + 0.4) for k, m in enumerate(p4.xs)],
                      run_time=min(2.2, c.until("r5") - 0.1))

            # {r5}: s6's table; "=" between next state and D
            p5 = panel_mod()
            cap5 = caption("D columns = next state", 4, t2c={"D columns": BLUE, "next state": GREEN})
            c.wait_until("r5")
            self.show_tile(p5, cap5)
            c.wait_until("simply the next state")
            cells = [m for grp in (p5.nxt, p5.inp) for row in grp for m in row]
            self.play(*appear(p5.eq, shift=None),
                      *[m.animate(rate_func=there_and_back).set_color(YELLOW) for m in cells],
                      run_time=min(1.4, c.until("r6") - 0.1))
            p5.add(p5.eq)

            # {r6}: J0 K0, every cell a lookup, all 1s: toggle
            p6 = panel_jk0()
            cap6 = caption("J-K: a lookup per cell", 5, t2c={"J-K:": BLUE, "lookup": YELLOW})
            c.wait_until("r6")
            self.show_tile(p6, cap6, rt=1.0)
            tab = p6.tab
            left, right = tab.rows[0][0].get_left()[0] - 0.12, tab.rows[0][3].get_right()[0] + 0.12
            box = row_box(tab, 1, left, right)
            c.wait_until("lookup")
            self.play(FadeIn(box), run_time=0.5)
            # the box hops row to row (quick move, then a hold on each row): it never straddles two
            # rows, and it stops on row 7
            ys = [r[0].get_y() for r in tab.rows[1:]]

            def hop(m, a, n=7):
                k = min(int(a * n), n - 1)
                u = smooth(min(1.0, (a * n - k) / 0.35))
                m.set_y(ys[k] + u * (ys[k + 1] - ys[k]))
            self.play(UpdateFromAlphaFunc(box, hop, rate_func=linear),
                      run_time=min(1.8, c.until("toggles") - 0.1))
            box.set_y(ys[-1])
            c.wait_until("toggles")
            self.play(FadeOut(box), *recolor(p6.ones, YELLOW),
                      *[restyle(s, outline=YELLOW, width=3) for s in p6.strips],
                      run_time=min(1.0, c.until("next") - 0.05))

            # {next}: the other tiles fade out together; s6's table grows to the centre
            c.wait_until("we turn")
            others = [m for m in self.mobjects if m is not p5]
            self.play(FadeOut(*others, scale=0.8), *set_alpha([p5], 1), run_time=0.9)
            title = T("Next: gates for the D columns", 48, t2c={"Next:": YELLOW}).move_to(_p(0, 3.35))
            p5.generate_target()
            p5.target.scale(TAB_K).move_to(TAB_C)
            self.play(MoveToTarget(p5), *during(appear(title), 0.5, 1.0), run_time=1.5)  # early: the next topic's title, said in this sentence

            # first by inspection: three arrows out of the D columns to three faint gates
            gates = faint_gates()
            x0 = p5.get_right()[0] + 0.15
            arrows = [Arrow(_p(x0, y), _p(g[0].get_left()[0] - 0.08, y), buff=0, color=BLUE, stroke_width=4,
                            max_tip_length_to_length_ratio=0.15) for g, y in zip(gates, GATE_YS)]
            c.wait_until("inspection")
            self.play(*[GrowArrow(a) for a in arrows], *during([FadeIn(g) for g in gates], 0.4, 1.0),
                      run_time=1.3)
            # then with a K-map
            cells, klab = tiny_kmap()
            c.wait_until("then with a")
            self.play(*[FadeIn(sq) for sq in cells], *appear(klab), run_time=1.0)
            part = T("Part 6 · From table to circuit", 40).move_to(_p(0, -3.3))
            c.wait_until("complete counter")
            self.play(*appear(part), run_time=1.0)  # early: end-card line, not read aloud
