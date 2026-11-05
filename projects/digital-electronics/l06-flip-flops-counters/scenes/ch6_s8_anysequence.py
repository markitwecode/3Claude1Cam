"""Chapter 6, scene 8: any count sequence, recap, next lecture. Clips c6.any.1 – c6.any.4.

Copied helpers: mod_table (ch5_s6), kmap / loops (ch6_s4, ch6_s5), state_ring style (ch4_s2, here
for six nodes), make_ff / toggle_loop (ch6_s2), make_dff / Gate / xor_gate / sync_counter /
ladder_line (ch6_s7), recap grid fit / caption / thin (ch4_s8), the road (ch1_s1).
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


def thin(g, k):
    for m in g.family_members_with_points():
        w = m.get_stroke_width()
        if w > 0:
            m.set_stroke(width=max(1.0, w * k))
    return g


# ---- ch5_s6's mod_table ---------------------------------------------------------------------------
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


def mod_table():
    titles = VGroup(*[T(s, 30).move_to(_p(gx, MT_TITLE_Y))
                      for s, gx in zip(("Current state", "Next state", "FF inputs"), MT_GX)])
    head_tex = (["Q_2", "Q_1", "Q_0"], ["Q_2'", "Q_1'", "Q_0'"], ["D_2", "D_1", "D_0"])
    head_col = (GREEN, GREEN, BLUE)
    heads = VGroup(*[VGroup(*[MathTex(t, font_size=MT_HEAD, color=col).move_to(_p(gx + (j - 1) * MT_DX, MT_HEAD_Y))
                              for j, t in enumerate(ts)])
                     for ts, col, gx in zip(head_tex, head_col, MT_GX)])
    lines = VGroup(*[Line(_p(sx, MT_TOP), _p(sx, MT_BOT)).set_stroke(DIM, 2) for sx in MT_SEPS])
    lines.add(Line(_p(MT_DEC - 0.35, MT_RULE_Y), _p(MT_GX[2] + 1.35, MT_RULE_Y)).set_stroke(DIM, 2))

    def bits_row(i, v, gx):
        return VGroup(*[MathTex(b, font_size=MT_CELL).move_to(_p(gx + (j - 1) * MT_DX, mt_row_y(i)))
                        for j, b in enumerate(format(v, "03b"))])
    dec, cur, nxt, inp = VGroup(), VGroup(), VGroup(), VGroup()
    for i in range(8):
        dec.add(MathTex(str(i), font_size=MT_CELL, color=GOLD).move_to(_p(MT_DEC, mt_row_y(i))))
        cur.add(bits_row(i, i, MT_GX[0]))
        nxt.add(bits_row(i, (i + 1) % 8, MT_GX[1]))
        inp.add(bits_row(i, (i + 1) % 8, MT_GX[2]))
    return VGroup(VGroup(titles, heads, lines), dec, cur, nxt, inp)


# ---- ch6_s4's kmap (verbatim) + ch6_s5's loops ------------------------------------------------------
KM_COLS = ("00", "01", "11", "10")
D2_MAP = ((0, 0, 1, 0), (1, 1, 0, 1))


def kmap(center=ORIGIN, scale=1.0, values=None):
    def p(x, y):
        return np.array([x, y, 0.0])
    c = np.array(center, dtype=float)
    s = scale
    cell = 1.1 * s
    W, H = 4 * cell, 2 * cell
    L, R, top, bot = c[0] - W / 2, c[0] + W / 2, c[1] + H / 2, c[1] - H / 2
    grid = VGroup(Rectangle(width=W, height=H).move_to(c),
                  *[Line(p(L + k * cell, top), p(L + k * cell, bot)) for k in (1, 2, 3)],
                  Line(p(L, c[1]), p(R, c[1]))).set_stroke(BLUE, 3)
    col_heads = VGroup(*[MathTex(h, font_size=44 * s, color=FG).move_to(p(L + (k + 0.5) * cell, top + 0.32 * s))
                         for k, h in enumerate(KM_COLS)])
    row_heads = VGroup(*[MathTex(str(r), font_size=44 * s, color=FG).move_to(p(L - 0.35 * s, top - (r + 0.5) * cell))
                         for r in (0, 1)])
    diag = Line(p(L, top), p(L - 0.75 * s, top + 0.75 * s)).set_stroke(FG, 2)
    q1q0 = MathTex("Q_1Q_0", font_size=40 * s, color=GREEN)
    q1q0.move_to(p(L - 0.5 * s, top + 0.8 * s), aligned_edge=LEFT)
    q2c = MathTex("Q_2", font_size=40 * s, color=GREEN).move_to(p(L - 0.82 * s, top + 0.22 * s))
    corner = VGroup(diag, q1q0, q2c)
    q0bar = Line(p(L + cell, top + 0.64 * s), p(L + 3 * cell, top + 0.64 * s)).set_stroke(GREEN, 4)
    q0lab = MathTex("Q_0", font_size=40 * s, color=GREEN).move_to(p(c[0], top + 0.98 * s))
    q1bar = Line(p(L + 2 * cell, bot - 0.28 * s), p(R, bot - 0.28 * s)).set_stroke(GREEN, 4)
    q1lab = MathTex("Q_1", font_size=40 * s, color=GREEN).move_to(p(L + 3 * cell, bot - 0.62 * s))
    q2bar = Line(p(R + 0.28 * s, bot), p(R + 0.28 * s, bot + cell)).set_stroke(GREEN, 4)
    q2lab = MathTex("Q_2", font_size=40 * s, color=GREEN).move_to(p(R + 0.66 * s, bot + cell / 2))
    bars = VGroup(q0bar, q0lab, q1bar, q1lab, q2bar, q2lab)

    def pos(r, k):
        return p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)

    def value(r, k, v):
        col = YELLOW if v == "X" else (FG if v else DIM)
        return MathTex(str(v), font_size=56 * s, color=col).move_to(pos(r, k))

    entries = VGroup()
    if values is not None:
        for r in (0, 1):
            for k in range(4):
                if values[r][k] is not None:
                    entries.add(value(r, k, values[r][k]))
    g = VGroup(grid, col_heads, row_heads, corner, bars, entries)
    g.grid, g.entries, g.cell, g.s = grid, entries, cell, s
    g.small = [q1q0, q2c, q0lab, q1lab, q2lab]
    g.heads = [*col_heads, *row_heads]
    g.pos, g.value = pos, value
    g.sq = [[Rectangle(width=cell, height=cell).move_to(pos(r, k)) for k in range(4)] for r in range(2)]
    return g


def rounded_path(pts_corners, rad, n=8):
    out = [pts_corners[0]]
    for i in range(1, len(pts_corners) - 1):
        p0, p1, p2 = (np.array(pts_corners[j], dtype=float) for j in (i - 1, i, i + 1))
        a = p1 + rad * (p0 - p1) / np.linalg.norm(p0 - p1)
        b = p1 + rad * (p2 - p1) / np.linalg.norm(p2 - p1)
        for k in range(n + 1):
            t = k / n
            out.append((1 - t) ** 2 * a + 2 * (1 - t) * t * p1 + t ** 2 * b)
    out.append(pts_corners[-1])
    return VMobject().set_points_as_corners([np.array(p, dtype=float) for p in out])


def loop_round(m, cells, color, inset=0.1):
    sqs = VGroup(*[m.sq[r][c] for r, c in cells])
    return RoundedRectangle(corner_radius=0.32, width=sqs.width - 2 * inset, height=sqs.height - 2 * inset,
                            stroke_color=color, stroke_width=6).move_to(sqs)


def half_loop(m, r, c, open_to, color, inset=0.1, ext=0.2):
    sq = m.sq[r][c]
    x0, x1 = sq.get_left()[0], sq.get_right()[0]
    t, b = sq.get_top()[1] - inset, sq.get_bottom()[1] + inset
    if open_to is LEFT:
        xo, xi = x0 - ext, x1 - inset
    else:
        xo, xi = x1 + ext, x0 + inset
    return rounded_path([[xo, t, 0], [xi, t, 0], [xi, b, 0], [xo, b, 0]], 0.32).set_stroke(color, 6)


def map_loops(m):
    pink = Circle(radius=0.44, stroke_color=PINK, stroke_width=6).move_to(m.sq[0][2])
    purple = VGroup(half_loop(m, 1, 0, LEFT, PURPLE), half_loop(m, 1, 3, RIGHT, PURPLE))
    teal = loop_round(m, [(1, 0), (1, 1)], TEAL, inset=0.2)
    return pink, purple, teal


# ---- flip-flops (ch6_s2's make_ff / toggle_loop; ch6_s7's make_dff) --------------------------------
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
    g.box, g.labels = box, [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def toggle_loop():
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    ff = make_ff(q_len=WIRE + 0.85)
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    loop = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 5)
    g = VGroup(ff, loop)
    g.ff, g.loop = ff, loop
    return g


def make_dff(center=ORIGIN):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.d_w, g.q_w, g.qb_w, g.clk_w, g.qb_l = box, d_w, q_w, qb_w, clk_w, qb_l
    g.labels = [d_l, q_l, qb_l]
    g.shift(center)
    return g


# ---- ch6_s7's gates and sync_counter ------------------------------------------------------------
GATE_COLOR = BLUE


class Gate(VGroup):
    def __init__(self, body, ins, out, extra=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        if extra is not None:
            extra.set_stroke(color, 4).set_fill(opacity=0)
            self.add(extra)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def _or_body():
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    return b


def xor_gate(color=GATE_COLOR):
    arc = VMobject()
    arc.start_new_path(_p(-0.85, 0.6))
    arc.add_cubic_bezier_curve_to(_p(-0.6, 0.2), _p(-0.6, -0.2), _p(-0.85, -0.6))
    return Gate(_or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), extra=arc, color=color)


K = 0.78
FF_X = (-5.1, -0.3, 4.75)
FF_Y = -0.5
HX = (BOX_W / 2 + WIRE) * K
QY = FF_Y + PIN_Y * K
QBY = FF_Y - PIN_Y * K
BUS_Y = FF_Y - (BOX_H / 2 + EN_WIRE) * K
LOOP_Y = -1.9
DROP_X, DROP_Y = -5.8, -2.75
RISE_TOP = 1.45


def sync_counter():
    """s6's circuit, without the in-tile-unreadable names (FF names, block caption, pin labels)."""
    S = VGroup()
    S.ffs = [make_dff().scale(K, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_X]
    for f in S.ffs:
        f.remove(*f.labels)
    S.bus = poly([(DROP_X, DROP_Y), (DROP_X, BUS_Y), (FF_X[2], BUS_Y)], YELLOW, 5)
    S.jdots = [Dot(_p(x, BUS_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    S.risers = [Line(_p(x + HX, QY), _p(x + HX, RISE_TOP)).set_stroke(GREEN, 5) for x in FF_X]
    x0 = FF_X[0]
    S.loop = poly([(x0 + HX, QBY), (x0 + HX, LOOP_Y), (x0 - HX, LOOP_Y), (x0 - HX, QY)], BLUE, 5)
    xg = xor_gate().scale(K)
    xg.shift(_p(FF_X[1] - HX, QY) - xg.out())
    S.xor_stubs = [Line(xg.inp(j) + 0.35 * LEFT, xg.inp(j)).set_stroke(GREEN, 4) for j in range(2)]
    x2 = FF_X[2]
    bx1 = x2 - HX - 0.3
    S.block = Rectangle(width=1.2, height=2.4).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(bx1 - 0.6, QY))
    S.block_out = Line(_p(bx1, QY), _p(x2 - HX, QY)).set_stroke(BLUE, 5)
    S.block_stubs = [Line(_p(bx1 - 1.45, QY + 1.0 - 0.4 * j), _p(bx1 - 1.2, QY + 1.0 - 0.4 * j)).set_stroke(GREEN, 4)
                     for j in range(6)]
    S.add(*S.ffs, S.bus, *S.jdots, *S.risers, S.loop, xg, *S.xor_stubs, S.block, S.block_out, *S.block_stubs)
    return S


# ---- ch6_s7's ladder line ---------------------------------------------------------------------------
def ladder_line(k, rhs, y, size=64):
    m = MathTex(f"D_{k}", "=", f"Q_{k}", r"\oplus", rhs, font_size=size)
    m[0].set_color(FG)
    m[2].set_color(GREEN)
    m[4].set_color(BLUE)
    m.shift(_p(0, y) - m[3].get_center())
    return m


# ---- the steps' icons -----------------------------------------------------------------------------
def icon_table():
    """A crop of ch5 s6's table: current state | next state, three rows (Mono 28)."""
    hq = MathTex("Q", font_size=36, color=GREEN)
    hn = MathTex("Q'", font_size=36, color=GREEN)
    rows = [(Mono(format(i, "03b"), 28), Mono(format(i + 1, "03b"), 28)) for i in range(3)]
    for j, (a, b) in enumerate(rows):
        a.move_to(_p(-0.55, -0.55 - 0.4 * j))
        b.move_to(_p(0.55, -0.55 - 0.4 * j))
    hq.move_to(_p(-0.55, 0))
    hn.move_to(_p(0.55, 0))
    sep = Line(_p(0, 0.25), _p(0, -1.55)).set_stroke(DIM, 2)
    rule = Line(_p(-1.0, -0.28), _p(1.0, -0.28)).set_stroke(DIM, 2)
    return VGroup(hq, hn, *[m for r in rows for m in r], sep, rule)


def icon_dq(size=56):
    m = MathTex("D", "=", "Q'", font_size=size)
    m[0].set_color(BLUE)
    m[2].set_color(GREEN)
    return m


def icon_kmap(s=0.5):
    m = kmap(scale=s, values=D2_MAP)
    return VGroup(m.grid, m.entries)


def tiny_table():
    box = Rectangle(width=1.3, height=1.3).set_stroke(DIM, 2)
    seps = [Line(_p(x, 0.65), _p(x, -0.65)).set_stroke(DIM, 2) for x in (-0.22, 0.22)]
    rule = Line(_p(-0.65, 0.38), _p(0.65, 0.38)).set_stroke(DIM, 2)
    bars = []
    for j in range(4):
        y = 0.18 - 0.25 * j
        for x, col in ((-0.43, GREEN), (0.0, GREEN), (0.43, BLUE)):
            bars.append(Line(_p(x - 0.13, y), _p(x + 0.13, y)).set_stroke(col, 3))
    return VGroup(box, *seps, rule, *bars)


def tiny_kmap():
    c = 0.4
    grid = VGroup(Rectangle(width=4 * c, height=2 * c),
                  *[Line(_p(-2 * c + k * c, c), _p(-2 * c + k * c, -c)) for k in (1, 2, 3)],
                  Line(_p(-2 * c, 0), _p(2 * c, 0))).set_stroke(BLUE, 2)
    pink = Circle(radius=0.15).set_stroke(PINK, 3).move_to(_p(0.5 * c, 0.5 * c))
    teal = RoundedRectangle(corner_radius=0.1, width=2 * c - 0.1, height=c - 0.1).set_stroke(TEAL, 3)
    teal.move_to(_p(-c, -0.5 * c))
    return VGroup(grid, pink, teal)


# ---- the 0..5 ring (ch4_s2's state_ring style, six nodes) -----------------------------------------
NODE_R = 0.5


def ring6(center, radius=2.2):
    c = np.array(center, dtype=float)

    def dirn(i):
        a = PI / 2 - TAU * i / 6
        return np.array([np.cos(a), np.sin(a), 0.0])
    nodes, circles, decs, arrows = [], [], [], []
    for i in range(6):
        p = c + radius * dirn(i)
        circ = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        b = Mono(format(i, "03b"), size=28, color=GREEN).move_to(p)
        circles.append(circ)
        nodes.append(VGroup(circ, b))
        decs.append(T(str(i), 34, color=GOLD).move_to(p - 0.85 * dirn(i)))
    for i in range(6):
        p, q = c + radius * dirn(i), c + radius * dirn((i + 1) % 6)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4))
    return nodes, circles, decs, arrows


def lone_node(v, at):
    circ = Circle(radius=NODE_R, color=DIM, stroke_width=4).set_fill(BG, 1).move_to(at)
    b = Mono(format(v, "03b"), size=28, color=DIM).move_to(at)
    d = T(str(v), 34, color=DIM).next_to(circ, LEFT, buff=0.3)
    return VGroup(circ, b), d


# ---- slide p. 101 ----------------------------------------------------------------------------------
TXT_L = -6.6
ICON_X = 5.4
BODY = 28


def lines(strs, size=BODY, color=FG, indent=0.0):
    g = VGroup(*[T(s, size, color) for s in strs]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    for m in g[1:]:
        m.shift(indent * RIGHT)
    return g


# ---- recap grid (ch4_s8) ------------------------------------------------------------------------
TILE_X = (-4.55, 0.0, 4.55)
VIS_Y = (2.25, -1.05)
CAP_Y = (0.85, -2.25)
TILE_W, TILE_H = 4.1, (2.4, 2.0)


def vis_at(i):
    return _p(TILE_X[i % 3], VIS_Y[i // 3])


def fit(m, i, w=TILE_W, h=None, dy=0.0):
    h = TILE_H[i // 3] if h is None else h
    s = min(w / m.width, h / m.height)
    m.scale(s, about_point=m.get_center())
    thin(m, max(0.45, s))
    m.move_to(vis_at(i) + dy * UP)
    return s


def caption(parts, i):
    if isinstance(parts, str):
        g = VGroup(*[T(s, 28) for s in parts.split("\n")]).arrange(DOWN, buff=0.12)
    else:
        g = parts
    return g.move_to(_p(vis_at(i)[0], CAP_Y[i // 3]), aligned_edge=UP).set_x(vis_at(i)[0])


def col_panel(heads, cols, xs, sep_x=None, n=4, size=44):
    """Small truth columns: MathTex heads, n rows of bits, a rule under the heads."""
    hs = VGroup(*[MathTex(t, font_size=size + 2, color=col).move_to(_p(x, 0)) for (t, col), x in zip(heads, xs)])
    rows = VGroup(*[VGroup(*[MathTex(str(c[i]), font_size=size).move_to(_p(x, -0.75 - 0.6 * i))
                             for c, x in zip(cols, xs)]) for i in range(n)])
    rule = Line(_p(xs[0] - 0.4, -0.38), _p(xs[-1] + 0.4, -0.38)).set_stroke(DIM, 2)
    g = VGroup(hs, rows, rule)
    if sep_x is not None:
        g.add(Line(_p(sep_x, 0.3), _p(sep_x, -0.75 - 0.6 * (n - 1) - 0.3)).set_stroke(DIM, 2))
    g.rows = rows
    return g


def panel_r1():
    cols = col_panel([("Q_0", GREEN), ("D_0", BLUE)], [[0, 1, 0, 1], [1, 0, 1, 0]], [0, 1.0], size=48)
    tl = toggle_loop()
    tl.next_to(cols, RIGHT, buff=0.9)
    g = VGroup(cols, tl)
    g.loop, g.labels = tl.loop, tl.ff.labels
    return g


def panel_r2():
    cols = col_panel([("Q_1", GREEN), ("Q_0", GREEN), ("D_1", BLUE)],
                     [[0, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0]], [0, 0.85, 2.05], sep_x=1.45)
    cols.d1 = VGroup(*[r[2] for r in cols.rows])
    return cols


def panel_r3():
    m = kmap(values=D2_MAP)
    pink, purple, teal = map_loops(m)
    g = VGroup(m, pink, purple, teal)
    g.loops = [pink, purple, teal]
    return g


def panel_r5():
    ls = [ladder_line(0, "1", 1.15), ladder_line(1, "Q_0", 0.0), ladder_line(2, "Q_1.Q_0", -1.15)]
    g = VGroup(*ls)
    g.ls = ls
    return g


def panel_steps():
    a = tiny_table()
    b = icon_dq(48)
    c = tiny_kmap()
    ar = [Arrow(LEFT, RIGHT, buff=0, stroke_width=4, color=DIM, tip_length=0.16).set_length(0.4) for _ in range(2)]
    return VGroup(a, ar[0], b, ar[1], c).arrange(RIGHT, buff=0.15)


# ---- shift register sketch (p. 101), make_dff from ch5_s2 --------------------------------------------
SR_K = 0.6
SR_X = (-3.4, 0.0, 3.4)
SR_Y = -0.7


def shift_register():
    ffs = []
    for x in SR_X:
        f = make_dff()
        f.remove(f.qb_w, f.qb_l)
        f.scale(SR_K, about_point=ORIGIN).shift(_p(x, SR_Y))
        for lb in f.labels[:2]:
            lb.scale(1.3, about_point=lb.get_center())
        ffs.append(f)
    qy = SR_Y + PIN_Y * SR_K
    he = (BOX_W / 2 + WIRE) * SR_K
    links = [Line(_p(SR_X[i] + he, qy), _p(SR_X[i + 1] - he, qy)).set_stroke(GREEN, 4) for i in range(2)]
    tail = Line(_p(SR_X[2] + he, qy), _p(SR_X[2] + he + 0.5, qy)).set_stroke(GREEN, 4)
    rx = [(SR_X[0] + SR_X[1]) / 2, (SR_X[1] + SR_X[2]) / 2, SR_X[2] + he + 0.5]
    top = SR_Y + BOX_H / 2 * SR_K + 0.45
    risers = [Line(_p(x, qy), _p(x, top)).set_stroke(GREEN, 4) for x in rx]
    dots = [Dot(_p(x, qy), radius=0.07, color=GREEN) for x in rx[:2]]
    qls = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x, top), UP, buff=0.1) for i, x in enumerate(rx)]
    din = T("Din", 32, BLUE).next_to(_p(SR_X[0] - he, qy), LEFT, buff=0.15)
    by = SR_Y - (BOX_H / 2 + EN_WIRE) * SR_K
    bus = Line(_p(SR_X[0] - 1.2, by), _p(SR_X[2], by)).set_stroke(YELLOW, 4)
    jd = [Dot(_p(x, by), radius=0.07, color=YELLOW) for x in SR_X[:2]]
    clk = T("CLK", 30, YELLOW).next_to(bus.get_start(), LEFT, buff=0.15)
    g = VGroup(*ffs, *links, tail, *risers, *dots, *qls, din, bus, *jd, clk)
    thin(g, 0.8)
    return g


class AnySequence(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(7.6)   # end card, carried by the music
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c6.any.1
    def clip1(self):
        with self.say("c6.any.1") as c:
            title = T("Synchronous Counter", 48, YELLOW).move_to(_p(0, 3.35))
            self.play(*appear(title), run_time=1.0)  # early: the slide's title
            bullet = lines(["• A similar procedure can be used to design counters",
                            "having an arbitrary count sequence"], size=30, indent=0.3)
            s1 = lines(["– Write down the state transition table"], color=DIM)
            s2 = lines(["– Determine the FF excitation (easy for D-types)"], color=DIM)
            s3 = lines(["– Determine the combinational logic necessary to generate",
                        "the required FF excitation from the current states"], color=DIM, indent=0.3)
            note = lines(["Note: remember to take into account any unused counts",
                          "since these can be used as don't care states when",
                          "determining the combinational logic circuits"], color=DIM)
            bullet.move_to(_p(0, 2.35), aligned_edge=LEFT).set_x(TXT_L, LEFT)
            for m, y in ((s1, 1.3), (s2, 0.2), (s3, -0.95)):
                m.move_to(_p(0, y)).set_x(TXT_L + 0.35, LEFT)
            note.move_to(_p(0, -2.6)).set_x(TXT_L + 0.65, LEFT)
            self.steps = [s1, s2, s3]
            self.note = note

            c.wait_until("steps")
            self.play(*appear(bullet), run_time=1.0)
            self.play(*appear(s1, s2, s3, note, shift=None, lag=0.15), run_time=1.2)  # early: the slide's list, shown whole then walked

            i1 = icon_table().move_to(_p(ICON_X, 1.45))
            i2 = icon_dq(56).move_to(_p(ICON_X, 0.2))
            i3 = icon_kmap(0.5).move_to(_p(ICON_X, -1.05))
            self.icons = [i1, i2, i3]
            for k, (s, ic, cue) in enumerate(zip(self.steps, self.icons, ("one", "two", "three"))):
                c.wait_until(cue)
                self.play(*recolor(list(s), FG), *during(appear(ic, shift=None), 0.2, 1), run_time=1.4)  # early: icon of the step being read
                if k == 1:
                    c.wait_until("easy")
                    self.play(FlashUnder(select(s2[0], "(easy for D-types)")[0], color=GREEN, time_width=1.5), run_time=1.2)

    # ------------------------------------------------------------------ c6.any.2
    def clip2(self):
        with self.say("c6.any.2") as c:
            # {unused}: the note turns YELLOW
            self.play(*recolor(list(self.note), YELLOW), run_time=1.0)
            self.play(FlashAround(self.note, color=YELLOW, time_width=1.5, buff=0.15), run_time=1.0)

            # {five}: the 0..5 ring, 110 and 111 outside it
            c.wait_until("five")
            RC = _p(-1.6, -0.35)
            nodes, circles, decs, arrows = ring6(RC)
            n6, d6 = lone_node(6, _p(3.6, 0.85))
            n7, d7 = lone_node(7, _p(3.6, -1.55))
            sweep_clear(self, run_time=1.0)
            self.play(*appear(*nodes, shift=None, lag=0.1), *[GrowArrow(a) for a in arrows],
                      *during(appear(*decs, n6, d6, n7, d7, shift=None, lag=0.05), 0.4, 1), run_time=1.6)  # early: the ring's states, read as a whole

            # {never}: a lap of the ring; 6 and 7 stay unlit
            c.wait_until("never")
            self.play(LaggedStart(*[VShowPassingFlash(ci.copy().set_stroke(YELLOW, 7), time_width=0.6)
                                    for ci in circles], lag_ratio=0.18),
                      run_time=min(1.6, c.until("six", floor=0.8) - 0.1))
            c.wait_until("six")
            self.play(*flash([n6, n7], color=YELLOW, time_width=1.5, buff=0.12), run_time=1.0)

            # {dc}: three small K-maps, X in cells 110 and 111
            c.wait_until("dc")
            S = 0.67
            vals = {"2": ((0, 0, 1, 0), (1, 0, None, None)),
                    "1": ((0, 1, 0, 1), (0, 0, None, None)),
                    "0": ((1, 0, 0, 1), (1, 0, None, None))}
            maps, labs, xcells = [], [], []
            for name, cx in (("2", -4.4), ("1", 0.05), ("0", 4.5)):
                m = kmap(center=_p(cx, -0.25), scale=S, values=vals[name])
                maps.append(m)
                labs.append(MathTex(f"D_{name}", font_size=52, color=BLUE).move_to(_p(cx, 2.15)))
                xcells.append([m.value(1, 2, "X"), m.value(1, 3, "X")])
            sweep_clear(self, run_time=1.0)
            self.play(*appear(*maps, shift=None, lag=0.12), *appear(*labs, lag=0.12), run_time=1.4)  # early: the three maps, shown whole
            self.play(*appear(*[x for pair in xcells for x in pair], shift=None, lag=0.08), run_time=1.0)
            self.maps, self.xcells = maps, xcells
            for m, xc in zip(maps, xcells):
                m.add(*xc)

            # {pair}: on D2, 011 pairs with the X below it
            c.wait_until("pair")
            m2 = maps[0]
            circ = Circle(radius=0.3, stroke_color=PINK, stroke_width=6).move_to(m2.pos(0, 2))
            old = MathTex(r"Q_0.Q_1.\overline{Q_2}", font_size=48, color=PINK).move_to(_p(-4.6, -2.7))
            self.play(*set_alpha([maps[1], maps[2], labs[1], labs[2]], DIMMED),
                      FlashAround(labs[0], color=BLUE, time_width=1.5), run_time=1.2)
            c.wait_until("lone cell")
            self.play(GrowFromCenter(circ), *during(appear(old), 0.3, 1), run_time=1.2)
            c.wait_until("can now pair")
            cell = m2.cell
            loop = RoundedRectangle(corner_radius=0.22, width=cell - 0.16, height=2 * cell - 0.16,
                                    stroke_color=PINK, stroke_width=6).move_to(
                (m2.pos(0, 2) + m2.pos(1, 2)) / 2)
            self.play(Transform(circ, loop), FlashAround(xcells[0][0], color=YELLOW, time_width=1.5),
                      run_time=1.5)
            c.wait_until("shrinks")
            new = MathTex(r"Q_1.Q_0", font_size=56, color=PINK).move_to(_p(-0.9, -2.7))
            arr = Arrow(_p(-3.3, -2.7), _p(-2.0, -2.7), buff=0, stroke_width=4, color=PINK, tip_length=0.2)
            self.play(*set_alpha([old], 0.4), GrowArrow(arr), *during(appear(new, shift=None), 0.35, 1),
                      run_time=1.3)
            self.play(FlashAround(new, color=PINK, time_width=1.5, buff=0.12),
                      run_time=min(1.2, c.until(floor=0.4)))

    # ------------------------------------------------------------------ c6.any.3
    def show_tile(self, panel, cap, rt=1.5):
        self.play(*appear(panel, shift=None), *during(appear(cap), 0.4, 1.0), run_time=rt)  # early: recap tile, seen whole
        self.tiles.append((panel, cap))

    def clip3(self):
        self.tiles = []
        with self.say("c6.any.3") as c:
            # {r1}
            p1 = panel_r1()
            k1 = fit(p1, 0)
            for lb in p1.labels:
                lb.scale(30 / (36 * k1), about_point=lb.get_center())
            cap1 = VGroup(MathTex(r"D_0 = \overline{Q_0}", font_size=40), T(": FF0 toggles", 28)).arrange(RIGHT, buff=0.08)
            cap1[0][0][0:2].set_color(BLUE)
            cap1[0][0][3:].set_color(GREEN)
            caption(cap1, 0)
            self.wait(max(0.0, c.until("r1") - 0.7))
            sweep_clear(self, run_time=1.4)
            self.show_tile(p1, cap1)
            c.wait_until("toggles")
            self.play(VShowPassingFlash(p1.loop.copy().set_stroke(YELLOW, 6), time_width=0.5), run_time=1.3)

            # {r2}
            p2 = panel_r2()
            fit(p2, 1)
            cap2 = MathTex("D_1", "=", "Q_0", r"\oplus", "Q_1", font_size=44)
            cap2[0].set_color(BLUE)
            cap2[2].set_color(GREEN)
            cap2[3].set_color(YELLOW)
            cap2[4].set_color(GREEN)
            caption(cap2, 1)
            c.wait_until("r2")
            self.show_tile(p2, cap2)
            c.wait_until("ex-or")
            self.play(*recolor(list(p2.d1), YELLOW), run_time=0.9)

            # {r3}
            p3 = panel_r3()
            k3 = fit(p3, 2)
            for lb in p3[0].small:
                lb.scale(28 / (40 * k3), about_point=lb.get_center())
            for lb in p3[0].heads:
                lb.scale(28 / (44 * k3), about_point=lb.get_center())
            for lp in p3.loops:
                p3.remove(lp)
            cap3 = caption("three essential\nprime implicants", 2)
            c.wait_until("r3")
            self.show_tile(p3, cap3)
            c.wait_until("three essential")
            self.play(LaggedStart(*[Create(lp) for lp in p3.loops], lag_ratio=0.4), run_time=1.6)
            settle(self, p3, add=p3.loops)

            # {r4}
            p4 = sync_counter()
            fit(p4, 3, h=1.4, dy=-0.25)
            rd = Mono("111 → 000", 30, GREEN).move_to(vis_at(3) + 0.85 * UP)
            p4b = VGroup(p4, rd)
            cap4 = caption("one clock: every bit\non the same edge", 3)
            c.wait_until("r4")
            self.show_tile(p4b, cap4)
            c.wait_until("same edge")
            self.play(VShowPassingFlash(p4.bus.copy().set_stroke(YELLOW, 8), time_width=0.6), run_time=1.2)

            # {r5}
            p5 = panel_r5()
            fit(p5, 4)
            cap5 = caption("a bit flips when all the\nbits below it are 1", 4)
            c.wait_until("r5")
            self.show_tile(p5, cap5)
            c.wait_until("the carry")
            self.play(*flash([l[4] for l in p5.ls], color=BLUE, time_width=1.5, buff=0.06), run_time=1.2)

            # {r6}
            p6 = panel_steps()
            fit(p6, 5, h=1.6)
            cap6 = caption("table → excitation\n→ logic", 5)
            c.wait_until("r6")
            self.show_tile(p6, cap6)

    # ------------------------------------------------------------------ c6.any.4
    def clip4(self):
        with self.say("c6.any.4") as c:
            # {line}: the slots shrink away; ch1's road returns as one line
            panels = [p for p, _ in self.tiles]
            caps = [cp for _, cp in self.tiles]
            names = ["latch", "flip-flop", "counter"]
            boxes = [RoundedRectangle(corner_radius=0.18, width=2.6, height=0.95)
                     .set_stroke(DIM, 3).set_fill(BG, 1) for _ in names]
            VGroup(*boxes).arrange(RIGHT, buff=1.0).move_to(_p(0, 0.3))
            arrows = [Arrow(a.get_right(), b.get_left(), buff=0.12, stroke_width=4).set_color(DIM)
                      for a, b in zip(boxes, boxes[1:])]
            labels = [T(n, 40).move_to(b) for n, b in zip(names, boxes)]
            self.wait(max(0.0, c.until("latch") - 1.6))
            self.play(*during([LaggedStart(*[FadeOut(VGroup(p, cp), scale=0.4) for p, cp in zip(panels, caps)],
                                           lag_ratio=0.08)], 0, 0.55),
                      *during(appear(boxes[0], arrows[0], boxes[1], arrows[1], boxes[2], shift=None, lag=0.15),
                              0.45, 1), run_time=1.5)
            for i, cue in enumerate(["latch", "flipflop", "counter"]):
                c.wait_until(cue, own_word=labels[i])
                nxt = ["flipflop", "counter", "next"][i]
                self.play(*appear(labels[i], shift=0.2 * DOWN), boxes[i].animate.set_stroke(YELLOW, 4),
                          run_time=min(1.0, max(0.5, c.until(nxt) - 0.1)))
            road = VGroup(*boxes, *arrows, *labels)
            self.add(road)

            # {next}: the slots leave; next lecture's title and its shift register
            c.wait_until("next")
            title = T("Next lecture: shift registers", 48, t2c={"Next lecture:": YELLOW}).move_to(_p(0, 1.5))
            self.play(*during([road.animate.move_to(_p(0, 2.85))], 0, 0.6),
                      *during(appear(title), 0.5, 1), run_time=1.4)  # early: the next topic's title, said in this sentence
            sr = shift_register()
            self.play(*appear(sr, shift=None), run_time=min(1.2, c.until("timing", floor=0.6)))  # early: the register sketch, under its title

            # {timing}: the three timing words, each on its word
            words = [T("set-up and hold times", 36, GOLD), T("clock skew", 36, GOLD), T("metastability", 36, GOLD)]
            VGroup(*words).arrange(RIGHT, buff=0.9).move_to(_p(0, -3.0))
            for w, cue in zip(words, ("set-up and hold times", "clock skew", "meta-stability")):
                c.wait_until(cue)
                self.play(*appear(w, shift=None), run_time=min(0.9, max(0.5, c.until(floor=0.5) - 0.05)))
