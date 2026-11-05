"""Chapter 1, scene 7: three K-maps for D_a, D_b, D_c of the sequential assignment. Clips c1.kmaps.1 – c1.kmaps.5.

Shared (imported by s8 and ch2):
  kmap3(values=None, center=ORIGIN, scale=1.0, loops=(), eq=None, eq_size=None, glow=True)
      a 3-variable K-map in L6 kmap() style, axes as p. 134: rows c = 0 / 1, columns b a in Gray
      order 00 01 11 10; corner diagonal with "ba" above, "c" below (GREEN); GREEN bars: a over
      columns 01-11, b under 11-10, c right of row 1. BLUE grid, cells 1.1*scale. Fonts scale with
      `scale` but never below 28.
      values: 2 rows of 4 entries, each 1 (FG), 0 (DIM) or "X" (don't care, FG).
      loops: [(cells, color), ...], cells = [(r, k), ...]; a pair in columns 0 and 3 is drawn as two
      half-loops open off the left and right edges (the wrap-around).
      eq: list of MathTex parts (e.g. EQ_A), first part BLUE, any \\oplus YELLOW, placed under the map.
      glow: X's inside a loop take that loop's colour, the other X's DIM.
      Attrs .grid .col_heads[k] .row_heads[r] .corner (diag, ba, c) .bars (abar, alab, bbar, blab,
      cbar, clab) .entries (r0k0..r0k3, r1k0..r1k3) .ent[r][k] .loops .eq (None without eq)
      .pos(r, k) .value(r, k, v) .sq(r, k) (cell Rectangle) .cell .s .L .R .top .bot.
  kmap_eq(parts, size) -> the coloured MathTex equation alone.
  MAP_A, MAP_B, MAP_C, LOOPS_A, LOOPS_B, LOOPS_C, EQ_A, EQ_B (short: a ⊕ b), EQ_C.
  compare_maps() / handover_shot(): the three maps (scale 0.58) in a row along the top third,
      centred at x -4.55, 0, 4.55, each with its equation under it; y about 0.5 .. 3.5. VGroup(ma, mb, mc).
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
# Shared: kmap3()
# =============================================================================================
KM_COLS = ("00", "01", "11", "10")             # b a, Gray order
MAP_A = ((1, 0, 0, 1), (0, "X", "X", "X"))
MAP_B = ((0, 1, 0, 1), (0, "X", "X", "X"))
MAP_C = ((0, 0, 1, 0), (0, "X", "X", "X"))
LOOPS_A = [([(0, 0), (0, 3)], PINK)]
LOOPS_B = [([(0, 1), (1, 1)], PINK), ([(0, 3), (1, 3)], PURPLE)]
LOOPS_C = [([(0, 2), (1, 2)], PINK)]
EQ_A = ["D_a", "=", r"\overline{a}\cdot\overline{c}"]
EQ_B_FULL = ["D_b", "=", r"a\cdot\overline{b}", "+", r"\overline{a}\cdot b", "=", "a", r"\oplus", "b"]
EQ_B = ["D_b", "=", "a", r"\oplus", "b"]
EQ_C = ["D_c", "=", r"a\cdot b"]


def kmap_eq(parts, size=52):
    eq = MathTex(*parts, font_size=size, color=FG)
    eq[0].set_color(BLUE)
    for i, t in enumerate(parts):
        if t == r"\oplus":
            eq[i].set_color(YELLOW)
    return eq


def _rounded_path(pts, rad, n=8):
    out = [pts[0]]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = (np.array(pts[j], dtype=float) for j in (i - 1, i, i + 1))
        a = p1 + rad * (p0 - p1) / np.linalg.norm(p0 - p1)
        b = p1 + rad * (p2 - p1) / np.linalg.norm(p2 - p1)
        for k in range(n + 1):
            t = k / n
            out.append((1 - t) ** 2 * a + 2 * (1 - t) * t * p1 + t ** 2 * b)
    out.append(pts[-1])
    return VMobject().set_points_as_corners([np.array(p, dtype=float) for p in out])


def kmap3(values=None, center=ORIGIN, scale=1.0, loops=(), eq=None, eq_size=None, glow=True):
    """See the module docstring."""
    c = np.array(center, dtype=float)
    s = scale

    def fs(x):
        return max(x * s, 28)
    cell = 1.1 * s
    W, H = 4 * cell, 2 * cell
    L, R, top, bot = c[0] - W / 2, c[0] + W / 2, c[1] + H / 2, c[1] - H / 2
    grid = VGroup(Rectangle(width=W, height=H).move_to(c),
                  *[Line(_p(L + k * cell, top), _p(L + k * cell, bot)) for k in (1, 2, 3)],
                  Line(_p(L, c[1]), _p(R, c[1]))).set_stroke(BLUE, 3)
    col_heads = VGroup(*[MathTex(h, font_size=fs(44), color=FG).move_to(_p(L + (k + 0.5) * cell, top + 0.32 * s))
                         for k, h in enumerate(KM_COLS)])
    row_heads = VGroup(*[MathTex(str(r), font_size=fs(44), color=FG).move_to(_p(L - 0.35 * s, top - (r + 0.5) * cell))
                         for r in (0, 1)])
    diag = Line(_p(L, top), _p(L - 0.75 * s, top + 0.75 * s)).set_stroke(FG, 2)
    ba = MathTex("ba", font_size=fs(40), color=GREEN)
    ba.move_to(_p(L - 0.5 * s, top + 0.8 * s), aligned_edge=LEFT)
    cc = MathTex("c", font_size=fs(40), color=GREEN).move_to(_p(L - 0.82 * s, top + 0.22 * s))
    corner = VGroup(diag, ba, cc)
    abar = Line(_p(L + cell, top + 0.64 * s), _p(L + 3 * cell, top + 0.64 * s)).set_stroke(GREEN, 4)
    alab = MathTex("a", font_size=fs(40), color=GREEN).move_to(_p(c[0], top + 0.98 * s))
    bbar = Line(_p(L + 2 * cell, bot - 0.28 * s), _p(R, bot - 0.28 * s)).set_stroke(GREEN, 4)
    blab = MathTex("b", font_size=fs(40), color=GREEN).move_to(_p(L + 3 * cell, bot - 0.62 * s))
    cbar = Line(_p(R + 0.28 * s, bot), _p(R + 0.28 * s, bot + cell)).set_stroke(GREEN, 4)
    clab = MathTex("c", font_size=fs(40), color=GREEN).move_to(_p(R + 0.66 * s, bot + cell / 2))
    bars = VGroup(abar, alab, bbar, blab, cbar, clab)

    def pos(r, k):
        return _p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)

    def value(r, k, v):
        if v == "X":
            return MathTex("X", font_size=fs(50), color=FG).move_to(pos(r, k))
        return MathTex(str(v), font_size=fs(56), color=FG if v else DIM).move_to(pos(r, k))

    def sq(r, k):
        return Rectangle(width=cell, height=cell).move_to(pos(r, k))

    g = VGroup(grid, col_heads, row_heads, corner, bars)
    g.grid, g.col_heads, g.row_heads, g.corner, g.bars = grid, col_heads, row_heads, corner, bars
    g.cell, g.s, g.L, g.R, g.top, g.bot = cell, s, L, R, top, bot
    g.pos, g.value, g.sq = pos, value, sq

    entries = VGroup()
    g.ent = [[None] * 4, [None] * 4]
    if values is not None:
        for r in (0, 1):
            for k in range(4):
                e = value(r, k, values[r][k])
                g.ent[r][k] = e
                entries.add(e)
    g.entries = entries
    g.add(entries)

    lps = VGroup(*[loop_shape(g, cells, color) for cells, color in loops])
    g.loops = lps
    g.add(lps)
    if glow and values is not None:
        for r in (0, 1):
            for k in range(4):
                if values[r][k] == "X":
                    col = DIM
                    for cells, color in loops:
                        if (r, k) in cells:
                            col = color
                    g.ent[r][k].set_color(col)
    g.eq = None
    if eq is not None:
        e = kmap_eq(eq, eq_size or max(52 * s, 36))
        e.next_to(VGroup(grid, bars), DOWN, buff=0.2)
        e.set_x(c[0] - 0.125 * s)
        g.eq = e
        g.add(e)
    return g


def loop_shape(m, cells, color):
    """A rounded loop round a block of cells; a pair in columns 0 and 3: two half-loops (wrap-around)."""
    s = m.s
    inset, rad, sw = 0.1 * s, 0.32 * s, (6 if s >= 0.8 else 4)
    ks = sorted({k for _, k in cells})
    if ks == [0, 3]:
        halves = VGroup()
        rows = sorted({r for r, _ in cells})
        t = m.sq(rows[0], 0).get_top()[1] - inset
        b = m.sq(rows[-1], 0).get_bottom()[1] + inset
        for k, side in ((0, LEFT), (3, RIGHT)):
            sqr = m.sq(rows[0], k)
            x0, x1 = sqr.get_left()[0], sqr.get_right()[0]
            if side is LEFT:
                xo, xi = x0 - 0.2 * s, x1 - inset
            else:
                xo, xi = x1 + 0.2 * s, x0 + inset
            halves.add(_rounded_path([[xo, t, 0], [xi, t, 0], [xi, b, 0], [xo, b, 0]], rad).set_stroke(color, sw))
        return halves
    sqs = VGroup(*[m.sq(r, k) for r, k in cells])
    return RoundedRectangle(corner_radius=rad, width=sqs.width - 2 * inset, height=sqs.height - 2 * inset,
                            stroke_color=color, stroke_width=sw).move_to(sqs)


CMP_S, CMP_Y, CMP_XS = 0.58, 2.2, (-4.55, 0.0, 4.55)


def compare_maps(s=CMP_S, y=CMP_Y, xs=CMP_XS, eq_size=36):
    out = VGroup()
    for x, vals, lps, eq in zip(xs, (MAP_A, MAP_B, MAP_C), (LOOPS_A, LOOPS_B, LOOPS_C), (EQ_A, EQ_B, EQ_C)):
        out.add(kmap3(vals, center=_p(x + 0.125 * s, y), scale=s, loops=lps, eq=eq, eq_size=eq_size))
    return out


# the large comparison (said over {compare}), before it moves up into the handover shot
BIG_S, BIG_Y, BIG_XS = 0.68, 0.55, (-4.5, 0.0, 4.5)


def compare_big():
    return compare_maps(BIG_S, BIG_Y, BIG_XS, 46)


def handover_shot():
    """The last frame: the three maps with their equations along the top third."""
    return compare_maps()


# =============================================================================================
# Scene
# =============================================================================================
MC = _p(2.3, 0.65)            # the big map's grid centre
TITLE_Y, LAB_Y, EQ_Y = 3.45, -1.95, -2.95
STACK = (_p(-4.4, -2.75), _p(-4.4, -3.45))
CELL_OF = {0: (0, 0), 1: (0, 1), 2: (0, 3), 3: (0, 2), 4: (1, 0)}   # table row (state) -> map cell


def col_box(tab, j, color=YELLOW):
    items = VGroup(tab.heads[1][j], tab.drow[j], *[tab.nxt[i][j] for i in range(5)])
    top, bot = items.get_top()[1] + 0.1, items.get_bottom()[1] - 0.1
    r = Rectangle(width=0.55, height=top - bot).move_to(_p(tab.heads[1][j].get_x(), (top + bot) / 2))
    return r.set_stroke(color, 3.5).set_fill(color, 0.1).set_z_index(-1)


def route(src, dst, pts, fade=0.15):
    """A copy of dst, born faint next to src (at src's height), travels the polyline pts (corners rounded)
    and grows to dst's size; returns (animation, mover). After the play: remove mover, add dst."""
    path = _rounded_path([np.array(p, dtype=float) for p in pts], 0.25)
    base = dst.copy()
    k0 = min(1.0, src.height / max(base.height, 1e-3))
    mover = base.copy().scale(k0).move_to(pts[0]).set_opacity(0)

    def upd(mob, a):
        t = smooth(a)
        mob.become(base.copy().scale(k0 + (1 - k0) * t).move_to(path.point_from_proportion(t)))
        mob.set_opacity(min(1.0, a / fade))
    return UpdateFromAlphaFunc(mover, upd), mover


def into(lab, part):
    """The label itself moves (and grows) into its place in the equation, taking its colour."""
    lab.generate_target()
    lab.target.scale(part.height / lab.height).move_to(part).set_color(part.get_color())
    return [MoveToTarget(lab)]


class Kmaps(NarratedScene):
    def construct(self):
        self.tab = load_scene("ch1_s6_count").handover_shot()
        self.add(self.tab)
        self.m = kmap3(center=MC)
        self.ent = {}
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # -- c1.kmaps.1: the empty map, its axes, Gray order, the don't cares --------------------------
    def clip1(self):
        m, tab = self.m, self.tab
        diag, ba, cc = m.corner
        abar, alab, bbar, blab, cbar, clab = m.bars
        h = m.col_heads
        with self.say("c1.kmaps.1") as c:
            self.play(*appear(m.grid, shift=None), run_time=1.2)
            c.wait_until("rows")
            self.play(*appear(m.row_heads[0], m.row_heads[1], cc, cbar, clab, lag=0.2), run_time=1.5)
            c.wait_until("cols")
            self.play(*appear(diag, ba, bbar, blab, abar, alab, lag=0.15), run_time=1.5)
            c.wait_until("zero zero")
            self.play(*appear(*h, lag=0.5), run_time=min(3.0, c.until("gray") - 0.2))  # early: headings read in order
            c.wait_until("gray")
            prev = []
            rt = 0.8
            for k1, k2, idx in ((0, 1, 1), (1, 2, 0), (2, 3, 1)):
                now = [h[k1][0][idx], h[k2][0][idx]]
                back = [g for g in prev if g not in now]
                self.play(*recolor(now, YELLOW), *recolor(back, FG), *flash([h[k1], h[k2]]), run_time=rt)
                prev = now
            arc = ArcBetweenPoints(_p(m.L, m.bot), _p(m.R, m.bot), angle=2.2).set_stroke(YELLOW, 4)
            wrap_bits = [h[3][0][0], h[0][0][0]]
            self.play(Create(arc), *recolor(prev, FG), *recolor(wrap_bits, YELLOW), run_time=1.2)
            self.arc, self.wrap_bits = arc, wrap_bits
            # the don't cares
            c.wait_until("xs")
            unused = T("Unused states, 101, 110 and 111.", 28, DIM).move_to(_p(-6.6, -2.75), aligned_edge=LEFT)
            self.unused = unused
            self.play(*appear(unused), *disappear(arc), *recolor(wrap_bits, FG), run_time=1.0)
            anims, done = [], []
            low = unused.get_bottom()[1] - 0.32
            for i, (code, k) in enumerate((("101", 1), ("110", 3), ("111", 2))):
                x = m.value(1, k, "X")
                self.ent[(1, k)] = x
                src = select(unused, code)[0]
                lo = low - 0.3 * i
                pts = [_p(src.get_x(), lo), _p(x.get_x(), lo), x.get_center()]
                a, mover = route(src, x, pts)
                anims += during([a], 0.15 * i, 0.7 + 0.15 * i)
                done.append((mover, x))
            self.play(*anims, run_time=min(2.2, c.until(None, floor=1.0)))
            for mover, x in done:
                self.remove(mover)
                self.add(x)

    # -- c1.kmaps.2: "Gray coding" means the map's edge order; the codes are free -----------------------
    def clip2(self):
        m, tab = self.m, self.tab
        quote = T("“we have to do Gray coding\nof these assignments”", 32, YELLOW, slant=ITALIC)
        quote.move_to(_p(MC[0] - 0.1, -2.05))
        tag = T("= the map’s order", 30).move_to(_p(MC[0] - 0.1, -3.05))
        ctag = T("the codes: free to choose", 28, GREEN).move_to(_p(-4.4, -2.75))
        self.quote, self.tag, self.ctag = quote, tag, ctag
        with self.say("c1.kmaps.2") as c:
            self.play(*appear(quote), run_time=1.0)
            self.play(FlashAround(m.col_heads, run_time=1.5, time_width=1.5))
            c.wait_until("this order")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("codes")
            self.play(*recolor(list(tab.cur), GREEN), FlashAround(tab.cur, color=GREEN, time_width=1.5),
                      *swap(self.unused, ctag), run_time=1.5)

    # -- the per-flip-flop helpers -----------------------------------------------------------------
    def plot(self, c, col, rows, vals, lane=False):
        """1s fly from the table's next-state column into row 0; then the DIM zeros."""
        m, tab = self.m, self.tab
        anims, movers = [], []
        for n, i in enumerate(rows):
            r, k = CELL_OF[i]
            one = m.value(r, k, 1)
            self.ent[(r, k)] = one
            if lane == "below":
                # down between the columns, under the table, up left of the map, along row 0 into the cell
                src = tab.nxt[i][col]
                lx = src.get_x() - 0.29
                ly = tab.nxt[4][col].get_bottom()[1] - 0.35
                vx = m.L - 0.62
                pts = [_p(lx, src.get_y()), _p(lx, ly), _p(vx, ly), _p(vx, one.get_y()), one.get_center()]
                a, mover = route(src, one, pts)
                d = len(rows) - 1 - n                     # the farther cell first: nothing in its way
                anims += during([a], 0.35 * d, 0.65 + 0.35 * d)
                movers.append((mover, one))
            elif lane:
                src = tab.nxt[i][col]
                lx = src.get_x() - 0.36
                ly = (tab.heads[1][0].get_top()[1] + tab.titles[1].get_bottom()[1]) / 2
                pts = [_p(lx, src.get_y()), _p(lx, ly), _p(m.L + 0.15, ly), one.get_center()]
                a, mover = route(src, one, pts)
                anims.append(a)
                movers.append((mover, one))
            else:
                anims += during(fly(tab.nxt[i][col], one), 0.2 * n, 0.8 + 0.2 * n)
        self.play(*anims, run_time=2.4 if lane == "below" else 1.8)
        for mover, one in movers:
            self.remove(mover)
            self.add(one)
        zeros = []
        for k in range(4):
            if vals[0][k] == 0:
                z = m.value(0, k, 0)
                self.ent[(0, k)] = z
                zeros.append(z)
        if (1, 0) not in self.ent:
            z = m.value(1, 0, 0)
            self.ent[(1, 0)] = z
            zeros.append(z)
        self.wait(0.4)
        self.play(*appear(*zeros, shift=None, lag=0.2), run_time=1.0)

    def reset(self, c, title_text, col, eq_to_stack, stack_pt, stack_size):
        """Next flip-flop: new title, the box slides, row 0, loops and labels go, the equation to the stack."""
        tab = self.tab
        new_title = T(title_text, 44).move_to(_p(MC[0] - 0.1, TITLE_Y))
        row0 = [self.ent.pop((0, k)) for k in range(4)]
        xs = [self.ent[(1, k)] for k in (1, 2, 3)]
        eq = eq_to_stack
        k = stack_size / eq.font_size if hasattr(eq, "font_size") else 1
        self.play(*during(swap(self.title, new_title), 0, 1.0),
                  Transform(tab.bbox, col_box(tab, col)),
                  *during(disappear(*row0, *self.loops, *self.labels), 0, 0.45),
                  *during(recolor(xs, FG), 0.3, 1.0),
                  *during([eq.animate.scale(k).move_to(stack_pt)], 0.3, 1.0),
                  run_time=1.8)
        self.title = new_title

    # -- c1.kmaps.3: D_a ------------------------------------------------------------------------------
    def clip3(self):
        m, tab = self.m, self.tab
        title = T("For FF a:", 44).move_to(_p(MC[0] - 0.1, TITLE_Y))
        self.title = title
        with self.say("c1.kmaps.3") as c:
            self.play(*during(disappear(self.quote, self.tag), 0, 0.45),
                      *during(appear(title), 0.4, 1.0),
                      Transform(tab.bbox, col_box(tab, 2)),
                      *recolor(list(tab.cur), FG), run_time=1.6)
            c.wait_until("plot_a")
            self.plot(c, 2, (0, 2), MAP_A)
            c.wait_until("ends")
            ones = [self.ent[(0, 0)], self.ent[(0, 3)]]
            self.play(*flash(ones), *disappear(self.ctag), run_time=1.2)
            c.wait_until("wrap")
            loop = loop_shape(m, LOOPS_A[0][0], PINK)
            self.play(*[Create(p) for p in loop], run_time=1.5)
            c.wait_until("term_a")
            lab = MathTex(r"\overline{a}\cdot\overline{c}", font_size=44, color=PINK).move_to(_p(MC[0], LAB_Y))
            self.play(*appear(lab), run_time=1.0)
            c.wait_until("so the input")
            eq = kmap_eq(EQ_A, 52).move_to(_p(MC[0], EQ_Y))
            self.play(*into(lab, eq[2]), *during(appear(eq[0], eq[1], shift=None), 0.3, 1.0), run_time=1.5)
            self.remove(lab)
            settle(self, eq)
            c.wait_until("nox")
            xs = [self.ent[(1, k)] for k in (1, 2, 3)]
            self.play(*flash(xs), *during(recolor(xs, DIM), 0.4, 1.0), run_time=1.4)
            self.loops, self.labels, self.eq_a = [loop], [], eq

    # -- c1.kmaps.4: D_b ------------------------------------------------------------------------------
    def clip4(self):
        m = self.m
        with self.say("c1.kmaps.4") as c:
            self.reset(c, "For FF b:", 1, self.eq_a, STACK[0], 36)
            c.wait_until("plot_b")
            self.plot(c, 1, (1, 2), MAP_B, lane="below")   # a straight fly crossed the a' column
            c.wait_until("pairs")
            xs = [self.ent[(1, 1)], self.ent[(1, 3)]]
            self.play(*flash(xs), run_time=1.2)
            labs, loops = [], []
            for cue, (cells, color), tex, k in (("t1", LOOPS_B[0], r"a\cdot\overline{b}", 1),
                                                ("t2", LOOPS_B[1], r"\overline{a}\cdot b", 3)):
                c.wait_until(cue)
                loop = loop_shape(m, cells, color)
                lab = MathTex(tex, font_size=44, color=color).move_to(_p(m.pos(0, k)[0], LAB_Y))
                self.play(Create(loop), *recolor([self.ent[(1, k)]], color), *appear(lab), run_time=1.3)
                labs.append(lab)
                loops.append(loop)
            c.wait_until("xor")
            eq = kmap_eq(EQ_B_FULL, 48).move_to(_p(MC[0], EQ_Y))
            self.play(*into(labs[0], eq[2]), *into(labs[1], eq[4]),
                      *during(appear(eq[0], eq[1], eq[3], shift=None), 0.3, 1.0), run_time=1.6)
            self.remove(*labs)
            self.add(eq[2], eq[4])
            c.wait_until("which is the")
            self.play(*appear(eq[5], eq[6], eq[7], eq[8], shift=None, lag=0.15),
                      *during([FlashAround(eq[7], time_width=1.5)], 0.45, 1.0), run_time=1.8)
            settle(self, eq)
            c.wait_until("spare")
            x = self.ent[(1, 2)]
            # a colour pulse only (a ring round the X read as a stray circle)
            self.play(*recolor([x], YELLOW), run_time=0.6)
            self.play(*recolor([x], DIM), run_time=0.9)
            self.loops, self.labels, self.eq_b = loops, [], eq

    # -- c1.kmaps.5: D_c, then the three maps side by side -----------------------------------------
    def clip5(self):
        m, tab = self.m, self.tab
        with self.say("c1.kmaps.5") as c:
            self.reset(c, "For FF c:", 0, self.eq_b, STACK[1], 32)
            c.wait_until("plot_c")
            self.plot(c, 0, (3,), MAP_C, lane=True)
            c.wait_until("pair_c")
            loop = loop_shape(m, LOOPS_C[0][0], PINK)
            self.play(Create(loop), *recolor([self.ent[(1, 2)]], PINK), run_time=1.3)
            c.wait_until("term_c")
            lab = MathTex(r"a\cdot b", font_size=44, color=PINK).move_to(_p(m.pos(0, 2)[0], LAB_Y))
            self.play(*appear(lab), run_time=1.0)
            eq = kmap_eq(EQ_C, 52).move_to(_p(MC[0], EQ_Y))
            self.wait(0.3)
            self.play(*into(lab, eq[2]), *during(appear(eq[0], eq[1], shift=None), 0.3, 1.0), run_time=1.5)
            self.remove(lab)
            settle(self, eq)
            # {compare}: the three maps large across the frame
            c.wait_until("compare")
            maps = compare_big()
            ma, mb, mc = maps
            ents = [self.ent[(r, k)] for r in (0, 1) for k in range(4)]
            big = [m.grid, m.col_heads, m.row_heads, m.corner, m.bars, *ents, loop]
            small = [mc.grid, mc.col_heads, mc.row_heads, mc.corner, mc.bars, *mc.entries, mc.loops[0]]
            parts_a = [ma.grid, ma.col_heads, ma.row_heads, ma.corner, ma.bars, ma.entries, ma.loops]
            parts_b = [mb.grid, mb.col_heads, mb.row_heads, mb.corner, mb.bars, mb.entries, mb.loops]
            self.play(*during(disappear(tab, self.title), 0, 0.4),
                      *during(edit(eq, mc.eq), 0.3, 0.85),
                      *during([Transform(b, s) for b, s in zip(big, small)], 0.3, 0.8),
                      *during([self.eq_a.animate.move_to(ma.eq)], 0.4, 0.9),
                      *during(edit(self.eq_b, mb.eq), 0.4, 0.95),
                      *during(appear(*parts_a, *parts_b, shift=None), 0.65, 1.0),
                      run_time=2.6)
            self.remove(*[f for mob in self.mobjects for f in mob.get_family()])
            self.add(maps)
            c.wait_until("doubled")
            glow = [(mb.ent[1][1], PINK), (mb.ent[1][3], PURPLE), (mc.ent[1][2], PINK)]
            self.play(*[FlashAround(x, color=col, time_width=1.5) for x, col in glow], run_time=1.5)
        # after the last word: up into the handover shot
        shot = handover_shot()
        self.play(*[Transform(b, s) for b, s in zip(maps, shot)], run_time=1.2)
        self.remove(*[f for mob in self.mobjects for f in mob.get_family()])
        self.add(shot)
        self.wait(1.0)
