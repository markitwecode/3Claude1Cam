"""Chapter 5, scene 7: if we'd used J-K flip-flops: six input columns, filled by lookup. Clips c5.jkcol.1 – c5.jkcol.4."""
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
# ch5_s6_modtable's mod_table() (copied verbatim)
# =============================================================================================
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


# =============================================================================================
# ch5_s5_jkexcite's jk_exc_table() (copied verbatim)
# =============================================================================================
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size, color=col)
            else:
                m = T(s, size=size * 0.82, color=col)
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


# =============================================================================================
# ch3_s4_toggle's waveform helpers (copied)
# =============================================================================================
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


# ch5_s6's travel(): a copy rides a polyline, born clear of its source
def travel(src, pts, scales=None):
    cp = src.copy().set_opacity(0)
    sc = scales or [1.0] * len(pts)
    w0 = cp.width
    corners = list(pts)
    path = VMobject().set_points_as_corners(corners)
    seg = [np.linalg.norm(b - a) for a, b in zip(corners, corners[1:])]
    cum = np.concatenate([[0], np.cumsum(seg)]) / sum(seg)

    def f(m, a):
        s = smooth(a)
        k = min(int(np.searchsorted(cum, s, side="right")) - 1, len(seg) - 1)
        u = (s - cum[k]) / max(cum[k + 1] - cum[k], 1e-6)
        m.scale_to_fit_width(w0 * (sc[k] + (sc[k + 1] - sc[k]) * u))
        m.move_to(path.point_from_proportion(s))
        m.set_opacity(min(1.0, a / 0.2))
    return cp, UpdateFromAlphaFunc(cp, f)


# =============================================================================================
# Layout
# =============================================================================================
SH = -2.5                                     # table shift while the J-K columns are up
JKX = [-0.65, -0.07, 0.73, 1.31, 2.11, 2.69]  # J2 K2 J1 K1 J0 K0 column centres
JK_NAMES = ["J_2", "K_2", "J_1", "K_1", "J_0", "K_0"]
JK_TITLE_X = (JKX[0] + JKX[-1]) / 2
LKX, LK_SC, LK_PITCH = 5.0, 0.7, 1.0          # lookup: centre x, scale, unscaled pitch
WAVE_X0, WAVE_X1 = 4.2, 6.55
CLK_Y, Q_Y, AMP = -1.75, -2.75, 0.25
LIGHT = 0.6                                   # "lighter weight" opacity for J2..K1 cells

J0 = ["1", "x"] * 4
K0 = ["x", "1"] * 4
OTHERS = ["0x0x", "0x1x", "0xx0", "1xx1", "x00x", "x01x", "x0x0", "x1x1"]   # J2 K2 J1 K1 per row


def cell_pos(i, c):
    return _p(JKX[c], mt_row_y(i))


def cell_box(i, c, color=YELLOW):
    return (Rectangle(width=0.5, height=0.52).set_stroke(color, 3).set_fill(color, 0.18)
            .move_to(cell_pos(i, c)).set_z_index(-1))


class JKColumns(NarratedScene):
    def construct(self):
        self.tab = mod_table(filled=True, x=0.0)
        self.jk = [[None] * 6 for _ in range(8)]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    # ------------------------------------------------ D columns out, six J-K columns in
    def clip1(self):
        tab = self.tab
        with self.say("c5.jkcol.1") as c:
            pieces = [*tab.titles, *tab.heads, *tab.lines, tab.dec, tab.cur, tab.nxt, tab.inp]
            self.play(FadeIn(*pieces), run_time=1.0)  # early: s6's finished table, carried over whole
            self.wait(1.0)

            # {swap}: the D group slides out right, the table shifts left
            moving = [tab.titles[0], tab.titles[1], tab.heads[0], tab.heads[1],
                      tab.lines[0], tab.lines[1], tab.cur, tab.nxt]
            new_rule = Line(_p(MT_GX[0] + SH - MT_DX - 0.4, MT_RULE_Y),
                            _p(JKX[-1] + 0.4, MT_RULE_Y)).set_stroke(DIM, 2)
            self.play(*during([FadeOut(tab.heads[2], tab.inp, shift=1.2 * RIGHT), FadeOut(tab.dec)], 0, 0.35),
                      *during([m.animate.shift(SH * RIGHT) for m in moving]
                              + [tab.titles[2].animate.move_to(_p(JK_TITLE_X, MT_TITLE_Y)),
                                 Transform(tab.lines[2], new_rule)], 0.3, 1.0),
                      run_time=min(2.2, c.until("cols")))
            c.wait_until("cols")

            # {cols}: six empty BLUE columns slide in
            self.strips = [Rectangle(width=0.48, height=4.75).set_stroke(BLUE, 2, opacity=0.35)
                           .set_fill(BLUE, 0.06).move_to(_p(x, (mt_row_y(0) + mt_row_y(7)) / 2)).set_z_index(-2)
                           for x in JKX]
            self.jk_heads = [MathTex(t, font_size=MT_HEAD, color=BLUE).move_to(_p(x, MT_HEAD_Y)).set_opacity(0.35)
                             for t, x in zip(JK_NAMES, JKX)]
            self.play(*[FadeIn(s, shift=0.6 * LEFT) for s in self.strips],
                      *appear(*self.jk_heads, shift=0.6 * LEFT, lag=0.1), run_time=1.5)
            c.wait_until("names")

            # {names}: each header lights as it is said
            for h, cue in zip(self.jk_heads, ["jay two", "kay two", "jay one", "kay one", "jay zero", "kay zero"]):
                c.wait_until(cue)
                self.play(h.animate.set_color(YELLOW).set_opacity(1), run_time=0.5)
            self.wait(0.5)
            self.play(*recolor(self.jk_heads, BLUE), run_time=min(0.8, c.until("lookup")))
            c.wait_until("lookup")

            # {lookup}: s5's J-K excitation table, small, top right
            lk = jk_exc_table(pitch=LK_PITCH).scale(LK_SC)
            lk.shift(_p(LKX - lk.get_center()[0], MT_HEAD_Y - lk.rows[0][0].get_y()))
            self.lk = lk
            self.lk_title = T("J-K excitation", 30).move_to(_p(LKX, MT_TITLE_Y))
            self.play(*appear(self.lk_title, lk, lag=0.3), run_time=1.4)  # early: the lookup is introduced by "lookup"

    # ------------------------------------------------ rows 0 and 1 by lookup
    def fly_pair(self, src_cells, row, vals, gap_y, rt):
        dsts, copies, anims = [], [], []
        sc = MT_CELL / (44 * LK_SC)
        for s, c, v in zip(src_cells, (4, 5), vals):
            d = MathTex(v, font_size=MT_CELL).move_to(cell_pos(row, c))
            pts = [_p(s.get_x(), gap_y), _p(d.get_x(), gap_y), d.get_center()]
            cp, an = travel(s, pts, scales=[1.0, sc, sc])
            dsts.append(d)
            copies.append(cp)
            anims.append(an)
            self.jk[row][c] = d
        self.play(*anims, run_time=rt)
        self.remove(*copies)
        self.add(*dsts)

    def clip2(self):
        tab, lk = self.tab, self.lk
        with self.say("c5.jkcol.2") as c:
            # {first}: spotlight Q0 -> Q0', row 0
            self.dimmed = ([r[j] for r in tab.cur for j in (0, 1)] + [r[j] for r in tab.nxt for j in (0, 1)]
                           + list(tab.heads[0][:2]) + list(tab.heads[1][:2]) + self.jk_heads[:4])
            self.play(*set_alpha(self.dimmed, 0.3), *recolor([tab.cur[0][2], tab.nxt[0][2]], YELLOW),
                      run_time=1.5)
            c.wait_until("t01")

            # {t01}: tag 0 -> 1
            self.tag = MathTex(r"Q_0:\ 0 \to 1", font_size=40, color=YELLOW).move_to(_p(LKX, -0.9))
            self.play(*appear(self.tag), run_time=1.0)
            c.wait_until("look")

            # {look}: the lookup row 0 1 | 1 x lights
            self.lbox = (SurroundingRectangle(lk.rows[2], buff=0.1).set_stroke(YELLOW, 3)
                         .set_fill(YELLOW, 0.12).set_z_index(-1))
            self.play(FadeIn(self.lbox), run_time=1.0)
            c.wait_until("cell1")

            # {cell1}: its 1 x flies into row 0's J0 K0, through the gap above the lookup row
            gap = (lk.rows[1][0].get_y() + lk.rows[2][0].get_y()) / 2
            self.fly_pair([lk.rows[2][2], lk.rows[2][3]], 0, (J0[0], K0[0]), gap,
                          min(2.0, c.until("second")))
            c.wait_until("second")

            # {second}: row 1, Q0 1 -> 0
            tag2 = MathTex(r"Q_0:\ 1 \to 0", font_size=40, color=YELLOW).move_to(self.tag)
            box2 = (SurroundingRectangle(lk.rows[3], buff=0.1).set_stroke(YELLOW, 3)
                    .set_fill(YELLOW, 0.12).set_z_index(-1))
            self.play(*recolor([tab.cur[0][2], tab.nxt[0][2]], FG), *recolor([tab.cur[1][2], tab.nxt[1][2]], YELLOW),
                      *swap(self.tag, tag2), Transform(self.lbox, box2), run_time=1.5)
            self.tag = tag2
            c.wait_until("cell2")

            # {cell2}: x 1 flies into row 1
            gap = (lk.rows[2][0].get_y() + lk.rows[3][0].get_y()) / 2
            self.fly_pair([lk.rows[3][2], lk.rows[3][3]], 1, (J0[1], K0[1]), gap,
                          min(2.0, c.until(floor=0.5)))

    # ------------------------------------------------ the rest, the pattern, all 1s: toggle
    def clip3(self):
        tab, lk = self.tab, self.lk
        with self.say("c5.jkcol.3") as c:
            # {rest}: the row-1 tag goes; rows 2..7 fill, each from its lookup row
            for i in range(2, 8):
                src = lk.rows[2] if i % 2 == 0 else lk.rows[3]
                box = (SurroundingRectangle(src, buff=0.1).set_stroke(YELLOW, 3)
                       .set_fill(YELLOW, 0.12).set_z_index(-1))
                cells = [MathTex(v, font_size=MT_CELL).move_to(cell_pos(i, col))
                         for col, v in ((4, J0[i]), (5, K0[i]))]
                self.jk[i][4], self.jk[i][5] = cells
                self.play(*recolor([tab.cur[i - 1][2], tab.nxt[i - 1][2]], FG),
                          *recolor([tab.cur[i][2], tab.nxt[i][2]], YELLOW),
                          Transform(self.lbox, box), *appear(*cells, shift=0.2 * LEFT, lag=0.15),
                          *(disappear(self.tag) if i == 2 else []),
                          run_time=0.6 if i > 2 else 1.0)
                self.wait(0.1)
            # {alt}: the current-state Q0 column pulses YELLOW: 0 1 0 1 ...
            c.wait_until("zero, one, zero, one")
            q0col = [r[2] for r in tab.cur]
            self.play(FadeOut(self.lbox), recolor([tab.nxt[7][2]], FG)[0], *recolor(q0col, YELLOW), run_time=1.0)
            self.wait(1.5)
            self.play(*recolor(q0col, FG), run_time=1.0)
            c.wait_until("pattern")

            # {pattern}: the two columns, outlined
            self.play(*[restyle(s, outline=YELLOW, width=3) for s in self.strips[4:]], run_time=1.2)
            c.wait_until("choose")

            # {choose}: every x flashes (cell box) and becomes 1
            xs = [(i, 4) for i in range(8) if J0[i] == "x"] + [(i, 5) for i in range(8) if K0[i] == "x"]
            xs.sort()
            boxes = [cell_box(i, col) for i, col in xs]
            self.play(*[FadeIn(b) for b in boxes], *recolor([self.jk[i][col] for i, col in xs], YELLOW),
                      run_time=0.9)
            anims = []
            for i, col in xs:
                one = MathTex("1", font_size=MT_CELL, color=YELLOW).move_to(cell_pos(i, col))
                anims += swap(self.jk[i][col], one)
                self.jk[i][col] = one
            self.play(*anims, run_time=1.2)
            self.play(*[FadeOut(b) for b in boxes], run_time=0.8)
            c.wait_until("toggle")

            # {toggle}: all 1s; beside them, the toggling waveform
            P = (WAVE_X1 - WAVE_X0) / 3.6
            rises = [WAVE_X0 + 0.4 * P + k * P for k in range(3)]
            clk = trace(clk_points(WAVE_X0, WAVE_X1, rises, P), CLK_Y, AMP, YELLOW)
            q0 = toggle_trace(WAVE_X0, WAVE_X1, rises, Q_Y, AMP, color=GREEN)
            clk_l = T("CLK", 28, YELLOW).move_to(_p(0, CLK_Y)).align_to(_p(WAVE_X0 - 0.15, 0), RIGHT)
            q_l = MathTex("Q_0", font_size=38, color=GREEN).move_to(_p(0, Q_Y)).align_to(_p(WAVE_X0 - 0.15, 0), RIGHT)
            guides = [Line(_p(r, CLK_Y + AMP + 0.1), _p(r, Q_Y - AMP - 0.1)).set_stroke(DIM, 1.5).set_z_index(-2)
                      for r in rises]
            self.play(*[FlashAround(s, time_width=1.5) for s in self.strips[4:]],
                      *appear(clk_l, q_l, shift=None), Create(clk), *[FadeIn(g) for g in guides], run_time=1.5)
            self.play(Create(q0, rate_func=linear), run_time=min(3.0, c.until(floor=0.5) - 0.5))
            self.wave_label = T("J = K = 1: toggle", 30, t2c={"toggle": YELLOW}).move_to(_p(LKX, -0.95))
            c.wait_until(own_word=self.wave_label)
            self.play(*appear(self.wave_label), run_time=1.0)
            c.wait_until("first flip-flop")
            self.play(VShowPassingFlash(q0.copy().set_stroke(YELLOW, 8), time_width=0.4),
                      run_time=min(2.5, c.until(floor=0.5)))
            self.wave = [clk, q0, clk_l, q_l, *guides]

    # ------------------------------------------------ the other four columns; back to D
    def clip4(self):
        tab = self.tab
        with self.say("c5.jkcol.4") as c:
            j01 = [self.jk[i][col] for i in range(8) for col in (4, 5)]
            self.play(*disappear(*self.wave, self.wave_label), *set_alpha(self.dimmed, 1),
                      *recolor(j01, FG), *[restyle(s, outline=BLUE, width=2) for s in self.strips[4:]],
                      run_time=1.0)

            # {others}: J2 K2 J1 K1, lighter, row by row
            rows = []
            for i, vals in enumerate(OTHERS):
                cells = [MathTex(v, font_size=MT_CELL).set_opacity(LIGHT).move_to(cell_pos(i, col))
                         for col, v in enumerate(vals)]
                for col, m in enumerate(cells):
                    self.jk[i][col] = m
                rows.append(VGroup(*cells))
            self.play(*appear(*rows, shift=0.2 * LEFT, lag=0.3), run_time=min(3.5, c.until("exactly one")))
            c.wait_until("exactly one")
            xs = [(i, col) for i, vals in enumerate(OTHERS) for col, v in enumerate(vals) if v == "x"]
            boxes = [cell_box(i, col) for i, col in xs]
            self.play(*[FadeIn(b) for b in boxes], run_time=0.6)
            self.play(*[FadeOut(b) for b in boxes], run_time=min(0.8, c.until("contrast")))
            c.wait_until("contrast")

            # {contrast}: J-K columns out, D columns back, table recentred
            fresh = mod_table(filled=True, x=0.0)
            jk_all = [*self.strips, *self.jk_heads, *rows, *j01, self.lk, self.lk_title]
            moving = [tab.titles[0], tab.titles[1], tab.heads[0], tab.heads[1],
                      tab.lines[0], tab.lines[1], tab.cur, tab.nxt]
            self.tag_d = T("excitation: easy for D-types", 34, GREEN).move_to(_p(0, -3.3))
            self.play(*during([FadeOut(*jk_all, shift=0.6 * RIGHT)], 0, 0.4),
                      *during([m.animate.shift(-SH * RIGHT) for m in moving]
                              + [tab.titles[2].animate.move_to(fresh.titles[2]),
                                 Transform(tab.lines[2], fresh.lines[2])], 0.2, 0.75),
                      *during(appear(fresh.heads[2], fresh.inp, shift=0.6 * LEFT, lag=0.1), 0.55, 1.0),
                      *during(appear(fresh.dec, shift=None), 0.8, 1.0),
                      run_time=2.4)
            self.play(*appear(self.tag_d), run_time=1.0)  # early: the tag sums up the D contrast being said
            c.wait_until("easy")
            self.play(FlashUnder(self.tag_d, run_time=1.5, time_width=1.5, color=GREEN))
        self.play(*disappear(self.tag_d), run_time=0.8)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
