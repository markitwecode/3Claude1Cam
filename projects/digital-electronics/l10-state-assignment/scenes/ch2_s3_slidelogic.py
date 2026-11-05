"""Chapter 2, scene 3: the sliding assignment's logic, D_a by K-map, D_b and D_c by eye. Clips c2.logic.1 – c2.logic.4."""
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
# Shared with ch2_s8 recap (r3): slide_table(), standalone
# =============================================================================================
SL_CODES = ["000", "001", "011", "110", "100"]
SL_GX = (-4.9, -1.9)          # current / next block centres (current = s2's widened code column)
SL_GAP = 0.85                 # digit pitch inside a block (c, b, a at -GAP, 0, +GAP)
SL_TITLE_Y, SL_HEAD_Y, SL_PITCH = 2.45, 1.75, 0.7
SL_SEP_X, SL_RULE_Y = -3.4, 1.4


def slide_table(dx=0.0):
    """The sliding assignment's state transition table (p. 135). The current block is exactly s2's
    code_column(-4.9, 1.75, gap=0.85): GREEN T 36 header letters, Mono 36 digits (1s GOLD, 0s FG),
    rows at y = 1.05 - 0.7 r. Next block centred at x = -1.9, headers c′ b′ a′. Titles
    "Current state" / "Next state" T 30 FG at y 2.45; DIM stroke-2 rules (vertical at -3.4, under the
    headers at y 1.4). The table spans about x -6.2 .. -0.6, y 2.7 .. -2.0 (shifted by dx).
    .titles[g] .heads[g] (VGroup of 3) .lines .cur[r] / .nxt[r] (VGroup of 3 digits, c first)
    .groups = [cur, nxt]; .col(g, j) -> VGroup(header j, its 5 digits); .block(g) -> heads+rows."""
    titles = VGroup(*[T(s, 30).move_to(_p(gx, SL_TITLE_Y)) for s, gx in zip(("Current state", "Next state"), SL_GX)])
    heads = VGroup(*[VGroup(*[T(n + pr, 36, color=GREEN).move_to(_p(gx + (j - 1) * SL_GAP, SL_HEAD_Y))
                              for j, n in enumerate("cba")])
                     for pr, gx in zip(("", "′"), SL_GX)])
    lines = VGroup(Line(_p(SL_SEP_X, 2.8), _p(SL_SEP_X, -2.05)).set_stroke(DIM, 2),
                   Line(_p(-6.15, SL_RULE_Y), _p(-0.65, SL_RULE_Y)).set_stroke(DIM, 2))

    def row(code, gx, r):
        y = SL_HEAD_Y - SL_PITCH * (r + 1)
        return VGroup(*[Mono(d, 36, color=GOLD if d == "1" else FG).move_to(_p(gx + (j - 1) * SL_GAP, y))
                        for j, d in enumerate(code)])
    cur = VGroup(*[row(code, SL_GX[0], r) for r, code in enumerate(SL_CODES)])
    nxt = VGroup(*[row(SL_CODES[(r + 1) % 5], SL_GX[1], r) for r in range(5)])
    g = VGroup(titles, heads, lines, cur, nxt)
    g.shift(dx * RIGHT)
    g.titles, g.heads, g.lines, g.cur, g.nxt = titles, heads, lines, cur, nxt
    g.groups = [cur, nxt]
    g.col = lambda gi, j: VGroup(heads[gi][j], *[r[j] for r in g.groups[gi]])
    return g


def col_box(tab, gi, j, color):
    return SurroundingRectangle(tab.col(gi, j), color=color, buff=0.14, stroke_width=4)


# ---- the small binary-count table (ch1 s6's sequential assignment), Mono rows ---------------
BIN_CODES = ["000", "001", "010", "011", "100"]


def bin_table(center):
    """Small copy of ch1's binary-count table: title, c b a | c′ b′ a′, five Mono 30 rows (1s GOLD).
    .title .heads .line .cur[r] .nxt[r] (each a single Mono)."""
    cx, cy = center[0], center[1]
    gx = (cx - 1.1, cx + 1.1)
    title = T("binary count", 30, color=DIM).move_to(_p(cx, cy + 1.55))
    heads = VGroup(*[T(s, 30, color=GREEN).move_to(_p(x, cy + 1.0)) for s, x in zip(("c b a", "c′ b′ a′"), gx)])
    line = Line(_p(cx, cy + 1.25), _p(cx, cy - 1.75)).set_stroke(DIM, 2)
    cur = VGroup(*[Mono(c, 30, t2c={"1": GOLD}).move_to(_p(gx[0], cy + 0.45 - 0.5 * r)) for r, c in enumerate(BIN_CODES)])
    nxt = VGroup(*[Mono(BIN_CODES[(r + 1) % 5], 30, t2c={"1": GOLD}).move_to(_p(gx[1], cy + 0.45 - 0.5 * r))
                   for r in range(5)])
    g = VGroup(title, heads, line, cur, nxt)
    g.title, g.heads, g.line, g.cur, g.nxt = title, heads, line, cur, nxt
    return g


# ---- K-map (L6 ch6_s4 kmap() style, axes relabelled as p. 134: c b a) ----------------------
KM_COLS = ("00", "01", "11", "10")


def kmap(center, scale=1.0):
    """3-variable K-map, L6 kmap() geometry: cells 1.1·s, BLUE grid stroke 3, headings FG MathTex 44,
    corner diagonal with GREEN `ba` / `c`, GREEN bars: a over 01-11, b under 11-10, c right of row 1.
    .pos(r, k) cell centre, .value(r, k, v) new MathTex entry (1 FG, 0 DIM, 'X' FG), .L .R .top .bot."""
    c = np.array(center, dtype=float)
    s = scale
    cell = 1.1 * s
    W, H = 4 * cell, 2 * cell
    L, R, top, bot = c[0] - W / 2, c[0] + W / 2, c[1] + H / 2, c[1] - H / 2
    grid = VGroup(Rectangle(width=W, height=H).move_to(c),
                  *[Line(_p(L + k * cell, top), _p(L + k * cell, bot)) for k in (1, 2, 3)],
                  Line(_p(L, c[1]), _p(R, c[1]))).set_stroke(BLUE, 3)
    col_heads = VGroup(*[MathTex(h, font_size=44 * s, color=FG).move_to(_p(L + (k + 0.5) * cell, top + 0.32 * s))
                         for k, h in enumerate(KM_COLS)])
    row_heads = VGroup(*[MathTex(str(r), font_size=44 * s, color=FG).move_to(_p(L - 0.35 * s, top - (r + 0.5) * cell))
                         for r in (0, 1)])
    diag = Line(_p(L, top), _p(L - 0.75 * s, top + 0.75 * s)).set_stroke(FG, 2)
    ba = MathTex("ba", font_size=40 * s, color=GREEN)
    ba.move_to(_p(L - 0.5 * s, top + 0.8 * s), aligned_edge=LEFT)
    cc = MathTex("c", font_size=40 * s, color=GREEN).move_to(_p(L - 0.82 * s, top + 0.22 * s))
    corner = VGroup(diag, ba, cc)
    abar = Line(_p(L + cell, top + 0.64 * s), _p(L + 3 * cell, top + 0.64 * s)).set_stroke(GREEN, 4)
    alab = MathTex("a", font_size=40 * s, color=GREEN).move_to(_p(c[0], top + 0.98 * s))
    bbar = Line(_p(L + 2 * cell, bot - 0.28 * s), _p(R, bot - 0.28 * s)).set_stroke(GREEN, 4)
    blab = MathTex("b", font_size=40 * s, color=GREEN).move_to(_p(L + 3 * cell, bot - 0.62 * s))
    cbar = Line(_p(R + 0.28 * s, bot), _p(R + 0.28 * s, bot + cell)).set_stroke(GREEN, 4)
    clab = MathTex("c", font_size=40 * s, color=GREEN).move_to(_p(R + 0.66 * s, bot + cell / 2))
    bars = VGroup(abar, alab, bbar, blab, cbar, clab)
    g = VGroup(grid, col_heads, row_heads, corner, bars)
    g.grid, g.col_heads, g.row_heads, g.corner, g.bars = grid, col_heads, row_heads, corner, bars
    g.cell, g.L, g.R, g.top, g.bot = cell, L, R, top, bot

    def pos(r, k):
        return _p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)

    def value(r, k, v):
        tex = r"\mathrm{X}" if v == "X" else str(v)
        return MathTex(tex, font_size=56 * s, color=DIM if v == 0 else FG).move_to(pos(r, k))
    g.pos, g.value = pos, value
    return g


# state code (c b a) -> K-map cell (row c, Gray column of b a)
def cell_of(code):
    return int(code[0]), KM_COLS.index(code[1:])


def connector(tab, j_cur, j_nxt, y=-2.5):
    """DIM bracket under the table from a current column to a next column, gap in the middle for '='."""
    xa = tab.cur[0][j_cur].get_x()
    xb = tab.nxt[0][j_nxt].get_x()
    mid = (xa + xb) / 2
    left = VMobject().set_points_as_corners([_p(xa, -2.07), _p(xa, y), _p(mid - 0.32, y)])
    right = VMobject().set_points_as_corners([_p(mid + 0.32, y), _p(xb, y), _p(xb, -2.07)])
    return VGroup(left, right).set_stroke(DIM, 3), _p(mid, y)


def _bbox(m):
    return m.get_corner(DL)[:2], m.get_corner(UR)[:2]


def _hits(a, b, pad=0.04):
    (al, ar), (bl, br) = a, b
    return al[0] < br[0] + pad and bl[0] < ar[0] + pad and al[1] < br[1] + pad and bl[1] < ar[1] + pad


def carry(src, dst, via=(), span=(0.0, 1.0)):
    """A copy of src travels (through the `via` points) to dst. It stays invisible while it still
    overlaps src (never doubled on its source), then shows; in the last 25% it fades out as dst fades
    in at its place. Returns (anims, cleanup) — call cleanup(scene) after the play."""
    cp = src.copy()
    pts = [src.get_center(), *[np.array(v, dtype=float) for v in via], dst.get_center()]
    path = VMobject().set_points_smoothly(pts) if len(pts) > 2 else Line(pts[0], pts[1])
    sbox = _bbox(src)
    h0, h1 = src.height, dst.height
    state = {"free": None}

    def upd(m, a):
        a = float(np.clip((a - span[0]) / (span[1] - span[0]), 0, 1))
        mv = min(1.0, a / 0.78)    # the copy lands exactly on dst first, then the crossfade happens in place
        m.scale_to_fit_height(h0 + (h1 - h0) * mv).move_to(path.point_from_proportion(mv))
        if state["free"] is None and not _hits(_bbox(m), sbox):
            state["free"] = a
        op = 0.0 if state["free"] is None else min(1.0, (a - state["free"]) / 0.1)
        op *= 1.0 - float(np.clip((a - 0.78) / 0.1, 0, 1))     # gone by 0.88 (Mono vs MathTex glyphs never overlap)
        m.set_opacity(op)

    def dupd(m, a):
        a = float(np.clip((a - span[0]) / (span[1] - span[0]), 0, 1))
        m.set_opacity(float(np.clip((a - 0.88) / 0.12, 0, 1)))
    dst.set_opacity(0)

    def cleanup(scene):
        scene.remove(cp)
        dst.set_opacity(1)
    return [UpdateFromAlphaFunc(cp, upd), UpdateFromAlphaFunc(dst, dupd)], cleanup


KM_C = (3.7, 0.95, 0.0)
KM_S = 0.85
EQ_X = 0.3                    # left edge of the equation stack


class SlideLogic(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def carry_play(self, pairs, run_time, extra=(), stagger=0.0):
        anims, cleans = [], []
        n = len(pairs)
        w = 1.0 - stagger * (n - 1)
        for i, (src, dst, *via) in enumerate(pairs):
            a, cl = carry(src, dst, via[0] if via else (), span=(i * stagger, i * stagger + w))
            anims += a
            cleans.append(cl)
        self.play(*anims, *extra, run_time=run_time)
        for cl in cleans:
            cl(self)

    # -- clip 1: the table, the unused states --------------------------------------------------
    def clip1(self):
        with self.say("c2.logic.1") as c:
            tab = self.tab = slide_table()
            self.play(*appear(tab.heads[0], *tab.cur, lag=0.12, shift=None), run_time=1.1)
            self.play(GrowFromCenter(tab.lines[0]), GrowFromCenter(tab.lines[1]),  # early: table headings, read with the rows
                      *appear(tab.titles[0], tab.titles[1], tab.heads[1], lag=0.2), run_time=1.4)

            c.wait_until("next state is simply")
            self.carry_play([(tab.cur[1], tab.nxt[0])], 1.5)
            self.wait(0.4)
            self.carry_play([(tab.cur[r + 1], tab.nxt[r]) for r in (1, 2, 3)], 1.3)
            self.play(FadeIn(tab.nxt[4]), FlashAround(tab.cur[0], color=YELLOW, time_width=1.5), run_time=1.1)

            # unused line
            c.wait_until("unused")
            lab = T("Unused states:", 32)
            codes = [Mono(s, 32, color=DIM) for s in ("010", "101", "111")]
            seps = [T(",", 32), T(", and", 32)]
            line = VGroup(lab, codes[0], seps[0], codes[1], seps[1], codes[2]).arrange(RIGHT, buff=0.2)
            for s, m in zip(seps, codes[:2]):
                s.next_to(m, RIGHT, buff=0.06).align_to(lab, DOWN).shift(0.06 * DOWN)
            codes[1].next_to(seps[0], RIGHT, buff=0.2).align_to(codes[0], DOWN)
            seps[1].next_to(codes[1], RIGHT, buff=0.06).align_to(lab, DOWN).shift(0.06 * DOWN)
            codes[2].next_to(seps[1], RIGHT, buff=0.2).align_to(codes[0], DOWN)
            line.move_to(_p(-3.4, -2.75))
            self.unused = codes
            self.unused_line = line
            self.play(*appear(lab), run_time=1.0)  # early: the slide's label; the codes follow on their words
            c.wait_until("zero one zero")
            self.play(*appear(codes[0], seps[0], codes[1], seps[1], codes[2], lag=0.45, shift=None),
                      run_time=min(2.6, c.until("binary")))

            # binary count's table: 010 was used there
            c.wait_until("binary")
            bt = self.bt = bin_table(_p(3.7, 0.0))
            self.play(*appear(bt.title, bt.heads, bt.line, *bt.cur, *bt.nxt, lag=0.06, shift=None),  # early: a recalled table
                      run_time=1.3)
            c.wait_until("though the binary count")
            hl = Rectangle(width=bt.cur[2].width + 0.36, height=0.44).move_to(bt.cur[2]) \
                .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.2).set_z_index(-1)
            self.play(FadeIn(hl), bt.cur[2].animate.set_color(YELLOW), run_time=1.0)
            c.wait_until("Which patterns")
            new010 = Mono("010", 32, color=YELLOW).move_to(codes[0])
            self.carry_play([(bt.cur[2], new010, [_p(1.7, bt.cur[2].get_y() - 0.4), _p(1.6, -3.55),
                                                   _p(new010.get_x(), -3.6)])], 1.5,
                            extra=during(disappear(codes[0]), 0, 0.4))
            line.remove(codes[0])
            line.add(new010)
            codes[0] = self.unused[0] = new010
            self.add(new010)
            self.play(*disappear(bt, hl), new010.animate.set_color(DIM), run_time=min(1.0, c.until(floor=0.5)))

    # -- clip 2: the K-map for D_a -------------------------------------------------------------
    def clip2(self):
        with self.say("c2.logic.2") as c:
            tab = self.tab
            km = self.km = kmap(KM_C, KM_S)
            MID_Y = KM_C[1]
            self.play(*appear(km.grid, km.row_heads, km.col_heads, km.corner, km.bars, lag=0.2, shift=None),
                      run_time=1.6)
            c.wait_until("unused states")
            # each X fades in on its own cell while its unused code flashes (nothing flies over the codes)
            xs = self.xs = [km.value(*cell_of(code), "X") for code in ("010", "101", "111")]
            self.play(*[time_span(FadeIn(x), 0.6 * i, 0.6 * i + 0.9) for i, x in enumerate(xs)],
                      *[time_span(FlashAround(m, color=YELLOW, time_width=1.5), 0.6 * i, 0.6 * i + 0.9)
                        for i, m in enumerate(self.unused)], run_time=2.1)

            c.wait_until("The next value")
            box = self.abox = col_box(tab, 1, 2, YELLOW)
            self.play(FadeIn(box), run_time=0.8)
            ents = {}
            c.wait_until("zero zero zero")
            ones = []
            for r in (0, 1):
                v = km.value(*cell_of(SL_CODES[r]), 1)
                ents[r] = v
                ones.append((tab.nxt[r][2], v, [_p(1.0, MID_Y), _p(km.L + 0.05, MID_Y), _p(v.get_x(), MID_Y)]))
            self.carry_play(ones, 1.8, stagger=0.25)
            self.wait(0.5)
            zeros = []
            for i, r in enumerate((2, 3, 4)):
                v = km.value(*cell_of(SL_CODES[r]), 0)
                ents[r] = v
                zeros.append((tab.nxt[r][2], v, [_p(1.0, MID_Y), _p(km.L + 0.05, MID_Y),   # along the mid-line, then
                                                 _p(v.get_x(), MID_Y)]))                     # into its cell: never over a 1 or X
            self.carry_play(zeros, min(2.0, max(1.2, c.until("pair") - 0.1)), stagger=0.3)

            c.wait_until("pair")
            loop = RoundedRectangle(corner_radius=0.3, width=2 * km.cell - 0.2, height=km.cell - 0.2,
                                    stroke_color=PINK, stroke_width=6) \
                .move_to((km.pos(0, 0) + km.pos(0, 1)) / 2)
            lab = MathTex(r"\overline{b}\cdot\overline{c}", font_size=40, color=PINK) \
                .move_to(_p((km.pos(0, 0)[0] + km.pos(0, 1)[0]) / 2, km.bot - 0.5))
            self.play(GrowFromCenter(loop), run_time=min(1.2, c.until("the input to")))
            self.play(*appear(lab), run_time=min(0.9, c.until("the input to")))
            c.wait_until("the input to")
            eq = self.eq_a = MathTex("D_a", "=", r"\overline{b}\cdot\overline{c}", font_size=48)
            eq[0].set_color(BLUE)
            eq[2].set_color(PINK)
            eq.move_to(_p(KM_C[0], km.bot - 1.45))
            self.play(*appear(eq), run_time=1.2)
            settle(self, eq)

            c.wait_until("xs")
            self.play(*flash(xs, color=YELLOW, run_time=1.5, time_width=1.5), run_time=1.5)
            self.km_parts = [*ents.values(), *xs, loop, lab]

    # -- clip 3: D_b and D_c by eye ------------------------------------------------------------
    def clip3(self):
        with self.say("c2.logic.3", gap=1.0) as c:
            tab, km = self.tab, self.km
            settle(self, km, add=self.km_parts)
            sc = 0.7 / KM_S
            dst = np.array(km.grid.get_center()) * 0 + _p(4.55, 2.0)
            shift = dst - np.array(km.grid.get_center()) * sc   # scale about ORIGIN, then shift
            self.play(km.animate.scale(sc, about_point=ORIGIN).shift(shift),
                      self.eq_a.animate.move_to(_p(EQ_X, 0.0), aligned_edge=LEFT),
                      *disappear(self.abox, self.unused_line), run_time=1.6)

            c.wait_until("Look at the column")
            gbox = col_box(tab, 0, 2, GREEN)
            self.play(FadeIn(gbox), run_time=0.9)
            c.wait_until("It reads")
            col = [tab.cur[r][2] for r in range(5)]
            self.play(*[time_span(FlashAround(d, color=GREEN, time_width=1.5, buff=0.08), 0.55 * i, 0.55 * i + 0.9)
                        for i, d in enumerate(col)], run_time=3.1)

            c.wait_until("match")
            bbox = col_box(tab, 1, 1, BLUE)
            self.play(FadeIn(bbox), run_time=0.9)
            c.wait_until("exactly the same")
            con, mid = connector(tab, 2, 1)
            eqs = MathTex("=", font_size=52, color=YELLOW).move_to(mid)
            self.play(Create(con), run_time=1.0)
            self.play(*appear(eqs, shift=None), run_time=0.7)
            c.wait_until("So dee bee")
            eq_b = MathTex("D_b", "=", "a", font_size=48)
            eq_b[0].set_color(BLUE)
            eq_b[2].set_color(GREEN)
            eq_b.move_to(_p(EQ_X, -0.95), aligned_edge=LEFT)
            self.play(*appear(eq_b), run_time=1.0)

            c.wait_until("dc")
            con2, mid2 = connector(tab, 1, 0)
            self.play(Transform(gbox, col_box(tab, 0, 1, GREEN)), Transform(bbox, col_box(tab, 1, 0, BLUE)),
                      Transform(con, con2), eqs.animate.move_to(mid2), run_time=1.6)
            c.wait_until("dee see equals")
            eq_c = MathTex("D_c", "=", "b", font_size=48)
            eq_c[0].set_color(BLUE)
            eq_c[2].set_color(GREEN)
            eq_c.move_to(_p(EQ_X, -1.9), aligned_edge=LEFT)
            self.play(*appear(eq_c), run_time=1.0)

            c.wait_until("quote")
            qt = T("“we like things where\nwe don’t have to\ndo anything”", 30, color=YELLOW, slant=ITALIC)
            who = T("the lecturer", 28, color=DIM)
            card_txt = VGroup(qt, who).arrange(DOWN, buff=0.2, aligned_edge=RIGHT)
            frame = RoundedRectangle(corner_radius=0.2, width=card_txt.width + 0.6, height=card_txt.height + 0.5) \
                .set_stroke(DIM, 2)
            card = VGroup(frame, card_txt).move_to(_p(4.4, -1.95))
            self.play(*disappear(con, eqs),   # the bracket and '=' have done their job
                      *during([FadeIn(frame), *appear(qt, who, lag=0.3)], 0.25, 1), run_time=1.4)  # early: the lecturer's words, quoted
            self.eq_b, self.eq_c = eq_b, eq_c
            self.card, self.marks = card, [gbox, bbox]

    # -- clip 4: a shift register with one AND at its input ------------------------------------
    def clip4(self):
        with self.say("c2.logic.4") as c:
            tab = self.tab
            eqs = [self.eq_a, self.eq_b, self.eq_c]
            self.play(*disappear(self.km, *self.marks),
                      *[time_span(FlashAround(e, color=YELLOW, time_width=1.5), 0.3 * i, 0.3 * i + 1.0)
                        for i, e in enumerate(eqs)], run_time=1.6)

            # the sketch, in circuit order: and-box -> a -> b -> c (where the map was)
            sy = 2.2
            cells, names = [], []
            for i, n in enumerate("abc"):
                sq = Square(0.9, color=BLUE, stroke_width=4).move_to(_p(2.9 + 1.5 * i, sy))
                cells.append(sq)
                names.append(T(n, 36, color=GREEN).move_to(sq))
            akw = dict(buff=0.06, color=FG, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.4)
            ab = Arrow(cells[0].get_right(), cells[1].get_left(), **akw)
            bc = Arrow(cells[1].get_right(), cells[2].get_left(), **akw)
            gtxt = MathTex(r"\overline{b}\cdot\overline{c}", font_size=36)
            gbox = RoundedRectangle(corner_radius=0.12, width=1.05, height=0.75).set_stroke(BLUE, 3).move_to(_p(1.1, sy))
            gtxt.move_to(gbox)
            ga = Arrow(gbox.get_right(), cells[0].get_left(), **akw)

            c.wait_until("Flip-flop bee copies")
            self.play(*appear(*[VGroup(s, n) for s, n in zip(cells, names)], lag=0.2, shift=None), run_time=1.1)
            self.play(GrowArrow(ab), FlashAround(self.eq_b, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("see copies bee")
            self.play(GrowArrow(bc), FlashAround(self.eq_c, color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("shift register")
            # under the cells' bottom edge with a clear gap, so it reads as a brace, not a wire
            brace = span_brace(cells[0].get_corner(DL), cells[2].get_corner(DR), DOWN, color=YELLOW, buff=0.25)
            sr = T("shift register", 32, color=YELLOW).next_to(brace, DOWN, buff=0.15)
            self.play(*during(disappear(self.card), 0, 0.45),
                      *during([GrowFromCenter(brace), *appear(sr)], 0.4, 1), run_time=1.6)

            c.wait_until("gate")
            self.play(*appear(gbox, gtxt, shift=None), GrowArrow(ga),
                      FlashAround(self.eq_a, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("A new one enters")
            top = tab.cur[0][0].get_y() + 0.32
            bot = tab.cur[1][0].get_y() - 0.32
            glow = Rectangle(width=5.5, height=top - bot).move_to(_p(-3.4, (top + bot) / 2)) \
                .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.18).set_z_index(-1)
            cap = T("a new 1 enters a only when b and c are both 0", 30,
                    t2c={"1": GOLD, "0": GOLD}).move_to(_p(-1.9, -2.75))
            self.play(FadeIn(glow), *appear(cap), run_time=1.2)
        self.wait(3.0)   # the caption is read before the board clears
