"""Chapter 5, scene 6: a four-variable K-map for D1 (p. 140). Clips c5.kmap.1 – c5.kmap.5.

Shared helpers (load_scene("ch5_s6_d1")), for s7 (D0), s8 and ch6 s1:
- `kmap4(values=None, center=ORIGIN, scale=1.0, title=None)`: p. 140's 4 x 4 K-map in L6 kmap()
  style. Rows s1 s0, columns e r, both Gray order 00 01 11 10. BLUE grid (stroke 3), cells
  0.88*scale; column headings BLUE, row headings GREEN (MathTex 44); corner diagonal with `e r`
  (BLUE) above-right and `s_1 s_0` (GREEN) below-left; bars: e over columns 11-10, r under 01-11
  (BLUE), s0 right of rows 01-11, s1 left of rows 11-10 (GREEN). Title (T 32) right of the e bar.
  `center` is the grid centre. values: 4 rows of 4 strings, "1" (FG), "X" (DIM), "0" (DIM),
  "" (empty). Fonts scale with `scale` (never below 28 for headings at scale >= 0.64).
  Attrs .grid .col_heads[k] .row_heads[r] .corner (diag, er (e, r), ss (s1, s0)) .bars
  (ebar, elab, rbar, rlab, s0bar, s0lab, s1bar, s1lab) .title .entries .ent[r][k] (None if empty)
  .pos(r, k) .value(r, k, v) .sq(r, k) (cell Rectangle, not drawn) .edge(side) (grid edge Line)
  .cell .s .L .R .top .bot .cx .cy.
- `loop4(m, cells, color, inset=0.1)`: L6 loop_round(): rounded loop round a block of cells.
- `loop_label(m, tex, color, pos)`: MathTex 44*s term in its colour at m-relative pos (dx from
  m.L / m.R, given as ("L"|"R", dx, dy from m.top)).
- `d1_parts(m)`: D1's loops and labels for map m: list of (loop, label).
- `term_eq(lhs, terms, colors, cx, y, xs=EQ_XS, size=48)`: the equation as separate MathTex
  pieces (lhs "D_1 =" with D BLUE, terms in colour, two "+"), term centres at cx + xs.
  Attrs .lhs .terms .plus.
- `d1_shot(cx=0.0)`: the finished D1 map at grid centre (cx, MAP_Y): values, loops, essential
  ones coloured, equation under it (the loop labels have moved into it). VGroup(map, loops, eq).
  The equation's terms sit at cx + EQ_XS, y EQ_Y (-2.35); the map spans y -1.75 .. 3.5.
- `handover_shot()`: d1_shot(0): this scene's last frame (no table, no captions).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# Shared: kmap4()
# =============================================================================================
GRAY = ("00", "01", "11", "10")
MAP_Y = 0.74                     # grid centre y (top 2.5, bottom -1.02 at scale 1)
D1_MAP = (("", "", "", ""), ("", "", "1", ""), ("X", "X", "X", "X"), ("1", "1", "1", ""))
D1_TERMS = (r"s_1\cdot\overline{e}", r"s_1\cdot r", r"s_0\cdot e\cdot r")
D1_COLORS = (PINK, PURPLE, TEAL)
D1_LOOPS = (([(2, 0), (2, 1), (3, 0), (3, 1)], 0.08),
            ([(2, 1), (2, 2), (3, 1), (3, 2)], 0.2),
            ([(1, 2), (2, 2)], 0.06))
D1_LABEL_POS = (("L", -2.45, -3.0), ("R", 0.85, -4.6), ("R", 2.0, -2.0))   # in cells for dy
D1_ESSENTIAL = ((3, 0), (3, 2), (1, 2))
EQ_Y = -2.35
EQ_XS = (-2.5, 0.6, 3.7)


def kmap4(values=None, center=ORIGIN, scale=1.0, title=None):
    """See the module docstring."""
    c = np.array(center, dtype=float)
    s = scale
    cell = 0.88 * s
    W = 4 * cell
    L, R, top, bot = c[0] - W / 2, c[0] + W / 2, c[1] + W / 2, c[1] - W / 2
    grid = VGroup(Square(side_length=W).move_to(c),
                  *[Line(_p(L + k * cell, top), _p(L + k * cell, bot)) for k in (1, 2, 3)],
                  *[Line(_p(L, top - k * cell), _p(R, top - k * cell)) for k in (1, 2, 3)]).set_stroke(BLUE, 3)
    col_heads = VGroup(*[MathTex(h, font_size=44 * s, color=BLUE).move_to(_p(L + (k + 0.5) * cell, top + 0.3 * s))
                         for k, h in enumerate(GRAY)])
    row_heads = VGroup(*[MathTex(h, font_size=44 * s, color=GREEN).move_to(_p(L - 0.42 * s, top - (r + 0.5) * cell))
                         for r, h in enumerate(GRAY)])
    diag = Line(_p(L, top), _p(L - 0.75 * s, top + 0.75 * s)).set_stroke(FG, 2)
    ce = MathTex("e", font_size=40 * s, color=BLUE)
    cr = MathTex("r", font_size=40 * s, color=BLUE)
    er = VGroup(ce, cr).arrange(RIGHT, buff=0.1 * s)
    er.move_to(_p(L - 0.45 * s, top + 0.78 * s), aligned_edge=LEFT)
    c1 = MathTex("s_1", font_size=40 * s, color=GREEN)
    c0 = MathTex("s_0", font_size=40 * s, color=GREEN)
    ss = VGroup(c1, c0).arrange(RIGHT, buff=0.08 * s)
    ss.move_to(_p(L - 0.95 * s, top + 0.24 * s))
    corner = VGroup(diag, er, ss)
    ebar = Line(_p(L + 2 * cell, top + 0.6 * s), _p(R, top + 0.6 * s)).set_stroke(BLUE, 4)
    elab = MathTex("e", font_size=40 * s, color=BLUE).move_to(_p(L + 3 * cell, top + 0.86 * s))
    rbar = Line(_p(L + cell, bot - 0.25 * s), _p(L + 3 * cell, bot - 0.25 * s)).set_stroke(BLUE, 4)
    rlab = MathTex("r", font_size=40 * s, color=BLUE).move_to(_p(L + 2 * cell, bot - 0.55 * s))
    s0bar = Line(_p(R + 0.25 * s, top - cell), _p(R + 0.25 * s, top - 3 * cell)).set_stroke(GREEN, 4)
    s0lab = MathTex("s_0", font_size=40 * s, color=GREEN).move_to(_p(R + 0.62 * s, top - 2 * cell))
    s1bar = Line(_p(L - 0.82 * s, top - 2 * cell), _p(L - 0.82 * s, bot)).set_stroke(GREEN, 4)
    s1lab = MathTex("s_1", font_size=40 * s, color=GREEN).move_to(_p(L - 1.2 * s, top - 3 * cell))
    bars = VGroup(ebar, elab, rbar, rlab, s0bar, s0lab, s1bar, s1lab)

    def pos(r, k):
        return _p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)

    def value(r, k, v):
        if v == "X":
            return MathTex("X", font_size=46 * s, color=DIM).move_to(pos(r, k))
        return MathTex(str(v), font_size=52 * s, color=FG if v == "1" else DIM).move_to(pos(r, k))

    def sq(r, k):
        return Rectangle(width=cell, height=cell).move_to(pos(r, k))

    def edge(side):
        return {"top": Line(_p(L, top), _p(R, top)), "bottom": Line(_p(L, bot), _p(R, bot)),
                "left": Line(_p(L, top), _p(L, bot)), "right": Line(_p(R, top), _p(R, bot))}[side]

    g = VGroup(grid, col_heads, row_heads, corner, bars)
    g.title = None
    if title:
        tt = T(title, max(32 * s, 28)).move_to(_p(0, top + 0.7 * s))
        tt.align_to(_p(R + 0.25 * s, 0), LEFT)
        g.title = tt
        g.add(tt)
    entries = VGroup()
    g.ent = [[None] * 4 for _ in range(4)]
    if values is not None:
        for r in range(4):
            for k in range(4):
                if values[r][k]:
                    e = value(r, k, values[r][k])
                    g.ent[r][k] = e
                    entries.add(e)
    g.add(entries)
    g.grid, g.col_heads, g.row_heads, g.corner, g.bars, g.entries = grid, col_heads, row_heads, corner, bars, entries
    g.er, g.ss = er, ss
    g.cell, g.s, g.L, g.R, g.top, g.bot, g.cx, g.cy = cell, s, L, R, top, bot, c[0], c[1]
    g.pos, g.value, g.sq, g.edge = pos, value, sq, edge
    return g


def loop4(m, cells, color, inset=0.1):
    sqs = VGroup(*[m.sq(r, k) for r, k in cells])
    i = inset * m.s
    return RoundedRectangle(corner_radius=0.3 * m.s, width=sqs.width - 2 * i, height=sqs.height - 2 * i,
                            stroke_color=color, stroke_width=6 if m.s >= 0.8 else 4).move_to(sqs)


def loop_label(m, tex, color, pos):
    side, dx, dy = pos
    x = (m.L if side == "L" else m.R) + dx * m.s
    y = m.top + dy * m.cell
    return MathTex(tex, font_size=44 * m.s, color=color).move_to(_p(x, y))


def d1_parts(m):
    return [(loop4(m, cells, col, inset), loop_label(m, tex, col, lp))
            for (cells, inset), col, tex, lp in zip(D1_LOOPS, D1_COLORS, D1_TERMS, D1_LABEL_POS)]


def term_eq(lhs, terms, colors, cx=0.0, y=EQ_Y, xs=EQ_XS, size=48):
    ts = [MathTex(t, font_size=size, color=col).move_to(_p(cx + x, y)) for t, x, col in zip(terms, xs, colors)]
    for t in ts:
        t.set_y(y)
    plus = [MathTex("+", font_size=size, color=FG).move_to(_p((a.get_right()[0] + b.get_left()[0]) / 2, y))
            for a, b in zip(ts, ts[1:])]
    lh = MathTex(lhs, "=", font_size=size, color=FG)
    lh[0].set_color(BLUE)
    lh.next_to(ts[0], LEFT, buff=0.25)
    lh.set_y(y)
    g = VGroup(lh, *ts, *plus)
    g.lhs, g.terms, g.plus = lh, ts, plus
    return g


def d1_eq(cx=0.0, y=EQ_Y):
    return term_eq("D_1", D1_TERMS, D1_COLORS, cx, y)


def d1_shot(cx=0.0):
    m = kmap4(D1_MAP, center=_p(cx, MAP_Y), title="For FF 1:")
    for (r, k), col in zip(D1_ESSENTIAL, D1_COLORS):
        m.ent[r][k].set_color(col)
    lps = VGroup(*[lp for lp, _ in d1_parts(m)])
    return VGroup(m, lps, d1_eq(cx))


def handover_shot():
    return d1_shot(0.0)


# =============================================================================================
# The scene
# =============================================================================================
MAP_X1 = 2.9          # grid centre x while the table is on the left (clips 1-3)
TAB_SCALE = 0.75
CAPTIONS = ("in Sync,\nnothing expected", "in Sync,\nsequence there", "from Sight,\non time")


class D1Map(NarratedScene):
    def construct(self):
        S5 = load_scene("ch5_s5_table")
        self.cell_box = S5.cell_box
        shot = S5.handover_shot()
        self.d, self.t = shot[0], shot[1]
        self.add(shot)
        self.m = kmap4(None, center=_p(MAP_X1, MAP_Y), title="For FF 1:")
        self.on_map = []          # every map piece on screen (shifted together in clip 4)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        d, t = self.d, self.t
        with self.say("c5.kmap.1") as c:
            dee = MathTex("D", "=", "Q'", font_size=56, color=YELLOW).move_to(_p(t.get_center()[0], -3.0))
            self.play(*appear(dee), run_time=min(1.0, c.until("d1")))
            c.wait_until("d1")
            # the diagram goes, its [11] circle stays; the table shrinks to the left
            u = d.unused
            self.remove(d)
            others = [x for x in d.submobjects if x is not u]
            self.add(*others, u)
            t.remove(t.titles)
            self.add(t.titles)
            t.generate_target()
            t.target.scale(TAB_SCALE)
            t.target.align_to(_p(-6.55, 0), LEFT).align_to(_p(0, 3.45), UP)
            u.generate_target()
            u.target.scale(1 / 0.55 * 0.9).move_to(_p(-5.1, -2.45))
            self.play(*during(disappear(*others, t.titles), 0, 0.45),
                      *during([MoveToTarget(t)], 0.45, 1.0),
                      *during([MoveToTarget(u)], 0.3, 1.0),
                      run_time=min(1.8, c.until("ess one prime column")))
            c.wait_until("ess one prime column")
            col = VGroup(t.heads[2][0], *[r[2][0] for r in t.rows])
            self.colbox = SurroundingRectangle(col, buff=0.1).set_stroke(BLUE, 3).set_fill(BLUE, 0.15).set_z_index(-1)
            self.d1lab = MathTex("D_1", "=", "s_1'", font_size=48, color=FG)
            self.d1lab[0].set_color(BLUE)
            self.d1lab.next_to(self.colbox, DOWN, buff=0.3)
            if self.d1lab.get_right()[0] > -0.9:
                self.d1lab.shift((-0.9 - self.d1lab.get_right()[0]) * RIGHT)
            self.play(FadeIn(self.colbox), *swap(dee, self.d1lab), run_time=min(1.4, c.until("four")))
            c.wait_until("four variables")
            chips = [MathTex(x, font_size=64, color=col) for x, col in
                     (("s_1", GREEN), ("s_0", GREEN), ("e", BLUE), ("r", BLUE))]
            VGroup(*chips).arrange(RIGHT, buff=0.75).move_to(_p(MAP_X1, MAP_Y))
            for ch in chips:
                ch.set_y(MAP_Y)
            heads = [t.heads[0][0], t.heads[0][1], t.heads[1][0], t.heads[1][1]]
            self.play(*appear(*chips, lag=0.5), *flash(heads, run_time=1.5),
                      run_time=min(2.2, c.until("so we need")))
            self.chips = chips
        self.u = u

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        m = self.m
        with self.say("c5.kmap.2") as c:
            targets = [m.ss[0], m.ss[1], m.er[0], m.er[1]]
            moves = [ch.animate.scale(tg.height / ch.height).move_to(tg) for ch, tg in zip(self.chips, targets)]
            self.play(Create(m.grid, lag_ratio=0.1), Create(m.corner[0]), *moves,
                      *appear(m.title, shift=None),  # early: the map's title, shown with the grid
                      run_time=min(1.6, c.until("ess one and ess zero")))
            self.remove(*self.chips)
            self.add(*targets)
            self.on_map += [m.grid, m.corner, m.title]
            self.add(m.corner)
            c.wait_until("ess one and ess zero")
            b = m.bars
            self.play(*appear(*m.row_heads, lag=0.15), FadeIn(b[6]), FadeIn(b[4]),
                      *appear(b[7], b[5], shift=None),
                      run_time=min(1.4, c.until("the columns")))
            c.wait_until("the columns")
            self.play(*appear(*m.col_heads, lag=0.15), FadeIn(b[0]), FadeIn(b[2]),
                      *appear(b[1], b[3], shift=None),
                      run_time=min(1.4, c.until("gray")))
            self.on_map += [m.row_heads, m.col_heads, m.bars]
            self.add(m.row_heads, m.col_heads, m.bars)

            # {gray}: the headings, then neighbours in pairs, the changed bit YELLOW
            c.wait_until("zero zero")
            fl = [FlashAround(VGroup(m.col_heads[k], m.row_heads[k]), color=YELLOW, run_time=1.0) for k in range(4)]
            self.play(LaggedStart(*fl, lag_ratio=0.45), run_time=min(2.6, c.until("so neighbouring")))
            c.wait_until("so neighbouring")
            changed = (1, 0, 1)
            prev = []
            per = c.until("wrap") / 3.6
            for k, bit in enumerate(changed):
                glyphs = [m.col_heads[k][0][bit], m.col_heads[k + 1][0][bit],
                          m.row_heads[k][0][bit], m.row_heads[k + 1][0][bit]]
                restore = ([g.animate.set_color(BLUE) for g in prev[:2]]
                           + [g.animate.set_color(GREEN) for g in prev[2:]])
                self.play(*restore, *recolor(glyphs, YELLOW),
                          FlashAround(VGroup(m.col_heads[k], m.col_heads[k + 1]), color=YELLOW),
                          run_time=min(1.1, per))
                self.wait(min(0.3, per * 0.2))
                prev = glyphs
            self.play(*[g.animate.set_color(BLUE) for g in prev[:2]],
                      *[g.animate.set_color(GREEN) for g in prev[2:]], run_time=0.6)

            # {wrap}
            c.wait_until("top to bottom")
            self.play(*[VShowPassingFlash(m.edge(s).set_stroke(YELLOW, 10), time_width=0.8) for s in ("top", "bottom")],
                      run_time=min(1.3, c.until("side to side")))
            c.wait_until("side to side")
            self.play(*[VShowPassingFlash(m.edge(s).set_stroke(YELLOW, 10), time_width=0.8) for s in ("left", "right")],
                      run_time=min(1.3, c.until("xrow")))

            # {xrow}
            c.wait_until("xrow")
            self.play(FlashAround(m.row_heads[2], color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until("between zero one")
            self.play(*flash([m.row_heads[1], m.row_heads[3]], run_time=1.2), run_time=1.2)
            c.wait_until("unused state")
            self.play(FlashAround(self.u, color=YELLOW, run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("don't cares")
            xs = [m.value(2, k, "X") for k in range(4)]
            self.play(*appear(*xs, lag=0.2, shift=None), run_time=min(1.3, c.until()))
            self.xs = xs
            self.on_map += xs

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        m, t = self.m, self.t
        with self.say("c5.kmap.3") as c:
            ones_rows = (4, 5, 7)
            onecells = [t.cell(i, 2, 0) for i in ones_rows]
            self.play(*recolor(onecells, YELLOW), *flash(onecells, run_time=1.2),
                      run_time=min(1.2, c.until("first")))
            c.wait_until("first")
            box = self.cell_box([t.rows[4]])
            self.play(FadeIn(box), run_time=min(1.0, c.until("column one one")))
            c.wait_until("column one one")
            e1 = m.value(1, 2, "1")
            self.play(*appear(e1, shift=None), FlashAround(m.sq(1, 2), color=YELLOW, run_time=1.2),
                      run_time=min(1.2, c.until("sync")))
            c.wait_until("sync")
            self.play(Transform(box, self.cell_box([t.rows[5]])), run_time=min(1.0, c.until("ar is an ex")))
            c.wait_until("ar is an ex")
            xbox = self.cell_box([t.cell(5, 1, 1)], buff=0.12)
            xbox.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.3).set_z_index(-0.5)
            self.play(FadeIn(xbox), run_time=min(0.9, c.until("two cells")))
            c.wait_until("two cells")
            e2, e3 = m.value(3, 0, "1"), m.value(3, 1, "1")
            self.play(*appear(e2, e3, shift=None, lag=0),
                      FlashAround(VGroup(m.sq(3, 0), m.sq(3, 1)), color=YELLOW, run_time=1.4),
                      run_time=min(1.4, c.until("last")))
            c.wait_until("last")
            self.play(FadeOut(xbox), Transform(box, self.cell_box([t.rows[7]])), run_time=min(1.0, c.until("both one", nth=1)))
            c.wait_until("both one", nth=1)
            e4 = m.value(3, 2, "1")
            self.play(*appear(e4, shift=None), FlashAround(m.sq(3, 2), color=YELLOW, run_time=1.2),
                      run_time=min(1.2, c.until("try")))
            self.ones = [e1, e2, e3, e4]
            self.on_map += self.ones
            c.wait_until("try")
            self.tag = T("your turn", 30, YELLOW).move_to(_p(MAP_X1 + 2.6, -2.4))
            self.play(FadeOut(box), *flash(self.ones, run_time=1.4), *appear(self.tag),  # early: the prompt, read out just after
                      run_time=min(1.4, c.until("try grouping")))

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        m, t = self.m, self.t
        dx = -MAP_X1 * RIGHT
        with self.say("c5.kmap.4") as c:
            leaving = [t, self.colbox, self.d1lab, self.u, self.tag]
            self.play(*during(disappear(*leaving), 0, 0.45),
                      *during([x.animate.shift(dx) for x in self.on_map], 0.3, 1.0),
                      run_time=min(1.6, c.until("sync's two cells")))
            m = self.m = kmap4(None, center=_p(0.0, MAP_Y), title="For FF 1:")   # same map, its new place
            parts = d1_parts(m)
            self.parts = parts
            ent = {(1, 2): self.ones[0], (3, 0): self.ones[1], (3, 1): self.ones[2], (3, 2): self.ones[3]}
            self.ent = ent
            steps = (("sync's two cells", [(3, 0), (3, 1)], "block of four", "ess one and not ee", "purple"),
                     ("purple", [(3, 1), (3, 2)], "the don't cares above them too", "ess one and ar", "teal"),
                     ("the lone one", [(1, 2)], "right below it", "S zero and ee and ar", None))
            for i, (cue, cells, lcue, tcue, nxt) in enumerate(steps):
                col = D1_COLORS[i]
                loop, lab = parts[i]
                c.wait_until(cue)
                self.play(*[FlashAround(m.sq(r, k), color=col, run_time=1.2) for r, k in cells],
                          run_time=min(1.2, c.until(lcue)))
                c.wait_until(lcue)
                self.play(FadeIn(loop, scale=1.15), run_time=min(1.5, c.until(tcue)))
                c.wait_until(tcue)
                self.play(*appear(lab), run_time=min(1.0, c.until(nxt) if nxt else c.until()))

    # ------------------------------------------------------------------ clip 5
    def clip5(self):
        m = self.m
        with self.say("c5.kmap.5") as c:
            for (r, k), col, cue in zip(D1_ESSENTIAL, D1_COLORS, ("covers a one", "no other group", "reaches")):
                c.wait_until(cue)
                e = self.ent[(r, k)]
                self.play(e.animate.set_color(col), FlashAround(m.sq(r, k), color=col, run_time=1.0, stroke_width=6),
                          run_time=min(1.0, c.until("so all three")))
            c.wait_until("result")
            eq = d1_eq(0.0)
            self.play(*appear(eq.lhs, shift=None), run_time=min(0.8, c.until("ess one and not ee")))
            for i, cue in enumerate(("ess one and not ee", "or ess one", "or ess zero")):
                c.wait_until(cue)
                extra = appear(eq.plus[i - 1], shift=None) if i else []
                lab, term = self.parts[i][1], eq.terms[i]
                self.play(lab.animate.scale(term.height / lab.height).move_to(term), *extra,
                          run_time=min(1.4, c.until(("or ess one", "or ess zero", "meaning")[i])))
                self.remove(lab)
                self.add(term)
            caps = [T(s, 28, col) for s, col in zip(CAPTIONS, D1_COLORS)]
            cap_top = min(t.get_bottom()[1] for t in eq.terms) - 0.2
            for cap, term in zip(caps, eq.terms):
                cap.next_to(term, DOWN, buff=0.3)
                cap.align_to(_p(0, cap_top), UP)
            for cap, cue in zip(caps, ("m1", "m2", "m3")):
                c.wait_until(cue)
                self.play(*appear(cap), run_time=min(1.0, c.until(("m2", "m3", None)[caps.index(cap)])))
        self.wait(3.0)
        self.play(*disappear(*caps), run_time=0.8)
        # handover: swap the pieces for the exact shot s7 opens on
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)
