"""Chapter 6, scene 4: a K-map for D2, from the table's four minterms. Clips c6.kmap.1 – c6.kmap.4."""
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


# =============================================================================================
# Shared with ch6_s5 (groups) and ch6_s8 (recap): kmap()
# =============================================================================================
KM_COLS = ("00", "01", "11", "10")             # Q1Q0 column order (Gray code)
KM_CENTER = (0.0, 1.3, 0.0)                    # grid centre of the finished map (end of s4 / s5)
D2_MAP = ((0, 0, 1, 0), (1, 1, 0, 1))          # D2's map, row Q2 = 0 / row Q2 = 1


def kmap(center=KM_CENTER, scale=1.0, values=None):
    """A 3-variable K-map in slide p. 100's style; everything self-contained (numpy, manim, lib.style).
    At scale 1: cells 1.1 square, grid 4.4 x 2.2 (BLUE, stroke 3) centred on `center`; column
    headings 00 01 11 10 and row headings 0 1 (FG MathTex 44); corner diagonal (FG stroke 2) with
    `Q_1Q_0` above-right and `Q_2` below-left (GREEN MathTex 40); GREEN bars (stroke 4) with
    MathTex 40 labels: `Q_0` over columns 01-11, `Q_1` under columns 11-10, `Q_2` right of row 1.
    The whole map spans about x c-3.2 .. c+2.95, y c-1.85 .. c+2.2.
    values (2 rows of 4, e.g. D2_MAP) adds the entries: 1 FG, 0 DIM (MathTex 56).
    Attributes: .grid .col_heads[k] .row_heads[r] .corner (diag, q1q0, q2) .bars (q0bar, q0lab,
    q1bar, q1lab, q2bar, q2lab) .entries (VGroup, empty without values) .cell (side) .s (scale)
    .pos(r, k) (cell centre) .cell_rect(r, k) (a cell-sized Rectangle, unstyled)
    .value(r, k, v) (a new entry MathTex at that cell) .L .R .top .bot (grid edges)."""
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
        return MathTex(str(v), font_size=56 * s, color=FG if v else DIM).move_to(pos(r, k))

    entries = VGroup()
    if values is not None:
        for r in (0, 1):
            for k in range(4):
                entries.add(value(r, k, values[r][k]))
    g = VGroup(grid, col_heads, row_heads, corner, bars, entries)
    g.grid, g.col_heads, g.row_heads, g.corner, g.bars, g.entries = grid, col_heads, row_heads, corner, bars, entries
    g.cell, g.s, g.L, g.R, g.top, g.bot = cell, s, L, R, top, bot
    g.pos, g.value = pos, value
    g.cell_rect = lambda r, k: Rectangle(width=cell, height=cell).move_to(pos(r, k))
    return g


# ---- ch5_s6_modtable's mod_table() (copied verbatim) ---------------------------------------
def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# Shared with ch5_s3 (skeleton), ch5_s7 (J-K columns), ch5_s8 recap, ch6 opening: mod_table()
# =============================================================================================
MT_GX = (-2.8, 0.0, 2.8)      # column-group centres (current, next, FF inputs), rel. to x
MT_DX = 0.72                  # column pitch inside a group (bit 2, 1, 0 at -DX, 0, +DX)
MT_DEC = -4.1                 # GOLD decimal column, rel. to x
MT_SEPS = (-1.4, 1.4)         # vertical rules between the groups, rel. to x
MT_TITLE_Y, MT_HEAD_Y, MT_RULE_Y = 3.45, 2.75, 2.35
MT_ROW0_Y, MT_PITCH = 1.9, 0.6                 # data row i at y = 1.9 - 0.6 i (row 7 at -2.3)
MT_TOP, MT_BOT = 3.8, -2.65
MT_CELL, MT_HEAD = 40, 42                      # MathTex sizes of data cells / column headers


def mt_row_y(i):
    return MT_ROW0_Y - i * MT_PITCH


def mod_table(filled=True, x=0.0):
    """The counter's modified state transition table (slide p. 99), in ch3_s3 jk_table()'s cell
    styling (MathTex cells, DIM stroke-2 rules). Absolute y (titles 3.45, headers 2.75, rows
    1.9 - 0.6 i); the Next-state group is centred at `x` (this scene ends with x = 0: the table
    spans about x -4.25 .. 4.05, 8.3 wide).
    Titles "Current state" / "Next state" / "FF inputs" (T 30, FG); headers Q2 Q1 Q0 and
    Q2' Q1' Q0' GREEN, D2 D1 D0 BLUE (MathTex 42); data cells FG MathTex 40, decimals 0..7 GOLD.
    The returned VGroup holds .skel (= VGroup(titles, heads, lines)) and, if filled, .dec .cur
    .nxt .inp too; the data rows are always built and reachable as attributes (filled=False:
    the empty skeleton, rows ready to be animated in).
    .titles[g], .heads[g] (VGroup of 3), .lines, .dec[i], .cur[i] / .nxt[i] / .inp[i] (VGroup of
    3 cells, bit 2 first), .groups = [cur, nxt, inp], .col(g, j) -> VGroup of column j of group g."""
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

# ---- this scene's layout ---------------------------------------------------------------------
TX = -2.35                                     # mod_table x: its left edge at x = -6.6
SIDE_S = 0.68                                  # the K-map's scale while it shares the frame
SIDE_C = np.array([4.4, 0.4, 0.0])             # its grid centre then
RX = 4.4                                       # centre of the free area right of the table


def hl(width, height, center, color=YELLOW, fill=0.2, stroke=2):
    return (Rectangle(width=width, height=height).move_to(center)
            .set_stroke(color, stroke).set_fill(color, fill).set_z_index(-1))


def chip(text):
    """ch6_s1_hook's chip (copied verbatim): T 40 in a FG stroke-3 rounded box, 1.0 tall."""
    lab = T(text, 40)
    box = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.6, height=1.0).set_stroke(FG, 3)
    box.move_to(lab)
    g = VGroup(box, lab)
    g.box, g.lab = box, lab
    return g


class KMapD2(NarratedScene):
    def construct(self):
        tab = mod_table(filled=True, x=TX)
        self.tab = tab
        d2 = [tab.inp[i][0] for i in range(8)]
        bits = [int(format((i + 1) % 8, "03b")[0]) for i in range(8)]      # 0 0 0 1 1 1 1 0
        dx = d2[0].get_x()

        # ---------------------------------------------------------------- clip 1
        with self.say("c6.kmap.1") as c:
            self.play(*appear(tab, shift=None), run_time=1.0)
            d2box = (Rectangle(width=0.66, height=tab.heads[2][0].get_top()[1] - d2[7].get_bottom()[1] + 0.3)
                     .move_to(_p(dx, (tab.heads[2][0].get_top()[1] + d2[7].get_bottom()[1]) / 2))
                     .set_stroke(BLUE, 4))
            self.play(GrowFromCenter(d2box), run_time=0.9)

            words = [("zero", 0), ("zero", 1), ("zero", 2), ("one", 0), ("one", 1), ("one", 2), ("one", 3),
                     ("zero", 3)]
            slider = None
            for i, (w, n) in enumerate(words):
                c.wait_until(w, nth=n)
                nxt = words[i + 1] if i + 1 < len(words) else None
                rt = min(0.4, 0.8 * c.until(nxt[0], nth=nxt[1], floor=0.2)) if nxt else 0.4
                target = hl(0.58, 0.52, d2[i].get_center())
                anims = []
                if slider is None:
                    slider = target
                    anims.append(FadeIn(slider))
                else:
                    anims.append(slider.animate.move_to(target))
                if bits[i]:
                    anims += recolor([d2[i]], YELLOW)
                self.play(*anims, run_time=rt)

            c.wait_until("stuck")
            q = T("?", 170, YELLOW).set_opacity(0.5).move_to(_p(RX, 0.5))
            self.play(FadeOut(slider), *appear(q, shift=None), run_time=1.0)

            bchip, kchip = chip("Boolean algebra"), chip("K-maps")
            VGroup(bchip, kchip).arrange(DOWN, buff=0.45).move_to(_p(RX, 0.4))
            c.wait_until("tool")
            c.wait_until(own_word=bchip[1])
            self.play(*swap(q, bchip), run_time=1.0)
            c.wait_until("or a")
            self.play(*appear(kchip), run_time=0.8)

            c.wait_until("choose")
            use = VGroup(T("Use a K-map for", 34), MathTex("D_2,", font_size=44, color=BLUE))
            use.arrange(RIGHT, buff=0.16, aligned_edge=DOWN).move_to(_p(RX, 2.75))
            use[1].shift(0.06 * DOWN)
            self.play(restyle(kchip, outline=YELLOW, width=3, shift=0.25 * UP),
                      *set_alpha([bchip], DIMMED), run_time=1.0)
            self.play(*appear(use), run_time=0.9)

        # ---------------------------------------------------------------- clip 2
        with self.say("c6.kmap.2") as c:
            bx = Rectangle(width=1.5, height=2.0).move_to(_p(RX, 0.3)).set_stroke(BLUE, 3)
            ins, in_arrows = VGroup(), VGroup()
            for j, (t, y) in enumerate((("Q_2", 0.9), ("Q_1", 0.3), ("Q_0", -0.3))):
                ins.add(MathTex(t, font_size=42, color=GREEN).move_to(_p(RX - 1.7, y)))
                in_arrows.add(Arrow(_p(RX - 1.42, y), _p(RX - 0.75, y), buff=0, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.3, color=GREEN))
            out_arrow = Arrow(_p(RX + 0.75, 0.3), _p(RX + 1.42, 0.3), buff=0, stroke_width=3,
                              max_tip_length_to_length_ratio=0.3, color=BLUE)
            out = MathTex("D_2", font_size=42, color=BLUE).move_to(_p(RX + 1.72, 0.3))
            self.play(*during(disappear(bchip, kchip), 0, 0.4),
                      *during([FadeIn(bx), GrowArrow(out_arrow), FadeIn(out)], 0.45, 1), run_time=1.6)
            c.wait_until("current state")
            self.play(*[GrowArrow(a) for a in in_arrows], *appear(*ins, lag=0.3), run_time=1.4)

            c.wait_until("mins")
            rowbox = {}
            for i in (3, 4, 5, 6):
                left, right = tab.dec[i].get_left()[0] - 0.25, tab.inp[i].get_right()[0] + 0.25
                rowbox[i] = hl(right - left, 0.52, _p((left + right) / 2, mt_row_y(i)), fill=0.13)
            self.play(*[FadeIn(rowbox[i]) for i in (3, 4, 5, 6)], run_time=1.4)

            c.wait_until("four")
            mins = VGroup(T("minterms", 32, DIM), MathTex(r"3,\ 4,\ 5,\ 6", font_size=50, color=GOLD))
            mins.arrange(DOWN, buff=0.2).move_to(_p(RX, -2.1))
            self.play(*appear(mins, lag=0.3), run_time=1.2)

        # ---------------------------------------------------------------- clip 3
        with self.say("c6.kmap.3") as c:
            km = kmap(SIDE_C, SIDE_S)
            S, cell = SIDE_S, km.cell
            sweep_clear(self, *appear(km, shift=None), keep=[tab, d2box, *rowbox.values(), mins], run_time=1.6)

            c.wait_until("rows")
            rb = hl(km.R - (km.L - 0.65 * S), cell, _p((km.R + km.L - 0.65 * S) / 2, km.pos(0, 0)[1]))
            self.play(FadeIn(rb), run_time=0.8)
            c.wait_until("and one for")
            self.play(rb.animate.move_to(_p(rb.get_x(), km.pos(1, 0)[1])), run_time=0.8)

            c.wait_until("cols")
            self.play(FadeOut(rb), FlashAround(km.corner[1], run_time=1.4, time_width=1.5), run_time=1.4)
            col_cues = [("the order", 0), ("zero one", 0), ("one one", 1), ("one zero", 0)]
            colh = 2 * cell + 0.6 * S
            cb = None
            for k, (w, n) in enumerate(col_cues):
                c.wait_until(w, nth=n)
                tgt = hl(cell, colh, _p(km.pos(0, k)[0], km.bot + colh / 2))
                if cb is None:
                    cb = tgt
                    self.play(FadeIn(cb), run_time=0.6)
                else:
                    self.play(cb.animate.move_to(tgt), run_time=0.25)
            c.wait_until("gray")
            self.play(FadeOut(cb), run_time=0.6)

            # Gray code: neighbouring headings differ in one bit
            hy = km.col_heads[0].get_y()
            pairs = [(0, 1, 1), (1, 2, 0), (2, 3, 1)]          # (col a, col b, changed bit index)
            gb, lit = None, []
            for a, b, bit in pairs:
                tgt = hl(2 * cell - 0.1, 0.5 * S + 0.12, _p((km.pos(0, a)[0] + km.pos(0, b)[0]) / 2, hy))
                new = [km.col_heads[a][0][bit], km.col_heads[b][0][bit]]
                anims = recolor(lit, FG) + recolor(new, YELLOW)
                if gb is None:
                    gb = tgt
                    anims.append(FadeIn(gb))
                else:
                    anims.append(gb.animate.move_to(tgt))
                self.play(*anims, run_time=0.8)
                lit = new
                self.wait(0.35)
            c.wait_until("wrap")
            arc = ArcBetweenPoints(_p(km.L, km.bot), _p(km.R, km.bot), angle=7 * PI / 6).set_stroke(YELLOW, 5)
            self.play(FadeOut(gb), *recolor(lit, FG), *disappear(mins), run_time=0.8)
            self.play(Create(arc), run_time=1.2)

            c.wait_until("zero zero and")
            ends = [hl(cell - 0.1, 0.5 * S + 0.12, _p(km.pos(0, k)[0], hy)) for k in (0, 3)]
            lit = [km.col_heads[0][0][0], km.col_heads[3][0][0]]
            self.play(*[FadeIn(e) for e in ends], *recolor(lit, YELLOW), run_time=1.0)

        # ---------------------------------------------------------------- clip 4
        with self.say("c6.kmap.4") as c:
            self.play(*disappear(arc, *ends), *recolor(lit, FG), run_time=1.0)
            plots = [("m3", 3), ("m4", 4), ("m5", 5), ("m6", 6)]
            tfoc = kfoc = None
            prev = []
            ones = {}
            for j, (cue, v) in enumerate(plots):
                c.wait_until(cue)
                r, k = v >> 2, KM_COLS.index(format(v & 3, "02b"))
                heads = [km.row_heads[r], km.col_heads[k]] + list(tab.cur[v])
                t_t = rowbox[v].copy().set_fill(opacity=0).set_stroke(YELLOW, 5)
                k_t = km.cell_rect(r, k).set_stroke(YELLOW, 5)
                anims = recolor(prev, FG) + recolor(heads, YELLOW)
                if tfoc is None:
                    tfoc, kfoc = t_t, k_t
                    anims += [FadeIn(tfoc), FadeIn(kfoc)]
                else:
                    anims += [tfoc.animate.move_to(t_t), kfoc.animate.move_to(k_t)]
                self.play(*anims, run_time=1.2 if j == 0 else 0.8)
                ones[v] = km.value(r, k, 1)
                self.play(*appear(ones[v], shift=0.15 * DOWN), run_time=1.0 if j == 0 else 0.7)
                prev = heads

            c.wait_until("map")
            zeros = [km.value(r, k, 0) for r in (0, 1) for k in range(4) if not D2_MAP[r][k]]
            self.play(*disappear(tfoc, kfoc), *recolor(prev, FG), run_time=0.8)
            self.play(*appear(*zeros, shift=None, lag=0.2), run_time=1.2)

        # table goes, the map moves to its final place for s5
        shift = np.array(KM_CENTER) - SIDE_C
        movers = [km, *ones.values(), *zeros]
        self.play(*during(disappear(tab, d2box, *rowbox.values()), 0, 0.45),
                  *during([m.animate.scale(1 / SIDE_S, about_point=SIDE_C).shift(shift) for m in movers], 0.4, 1),
                  run_time=2.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # s5 opens on this map, no fade
        self.wait(0.15)
