"""Chapter 5, scene 6: the counter's modified state transition table, filled in three steps. Clips c5.mod.1 – c5.mod.5."""
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


# ---- ch5_s4's D excitation table (copied verbatim) -------------------------------------------
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """ch1_s2's grid_table: rows of strings ('$...' -> MathTex, else T); header row at y = 0,
    column centres xs (or ('L', x) for left-aligned). VGroup(*rows, lines), .rows, .lines."""
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


D_XS = [0, 0.9, 2.1]      # Q, Q', D column centres
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


# =============================================================================================
# Scene-only helpers and layout
# =============================================================================================
TX = -1.85          # table x while it is being filled (Next-state group centre)
PX = 4.6            # centre of the right-hand panel
CH = TX + MT_SEPS[0]   # x of the channel between the current and next groups
STEP_L = 2.5           # left edge of the step list


def tiny_dff():
    """A small D flip-flop icon: box, D (BLUE) in, Q (GREEN) out, clock triangle and wire."""
    box = Rectangle(width=0.8, height=1.1).set_stroke(FG, 3)
    tri = Polygon(_p(-0.12, -0.55), _p(0.12, -0.55), _p(0, -0.37)).set_stroke(FG, 2)
    d_w = Line(_p(-0.65, 0.25), _p(-0.4, 0.25)).set_stroke(BLUE, 4)
    q_w = Line(_p(0.4, 0.25), _p(0.65, 0.25)).set_stroke(GREEN, 4)
    c_w = Line(_p(0, -0.8), _p(0, -0.55)).set_stroke(YELLOW, 4)
    d = T("D", 30, BLUE).move_to(_p(-0.2, 0.25))
    q = T("Q", 30, GREEN).move_to(_p(0.2, 0.25))
    return VGroup(box, tri, d_w, q_w, c_w, d, q)


def step_text(n, body):
    num = T(f"{n}.", 28, GOLD)
    txt = T(body, 28, line_spacing=0.9)
    txt.next_to(num, RIGHT, buff=0.18, aligned_edge=UP)
    g = VGroup(num, txt)
    g.num, g.txt = num, txt
    return g


def travel(src, pts, scales=None, clear=0.15):
    """A copy of src rides the polyline pts... (straight legs, no arcs). It is born just clear of
    src (to its right, `clear` beyond its edge, or at pts[0] if that is further on) and fades in
    over the first 20%, so it is never drawn over its source; `scales` (one per corner) scales it
    along the way. Returns (copy, animation); after the play remove the copy, add the real dst."""
    cp = src.copy().set_opacity(0)
    sc = scales or [1.0] * len(pts)
    w0 = cp.width
    corners = list(pts)
    if len(corners) < 2:
        corners = [src.get_center() + RIGHT * (w0 + clear)] + corners
        sc = [1.0] + list(sc)
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


def head_box(tab, g, color=YELLOW):
    box = SurroundingRectangle(VGroup(tab.titles[g], tab.heads[g]), color=color, buff=0.12)
    return box.set_stroke(color, 3).set_fill(color, 0.12).set_z_index(-1)


class ModTable(NarratedScene):
    def construct(self):
        self.tab = mod_table(filled=True, x=TX)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ------------------------------------------------ the skeleton and its three groups
    def clip1(self):
        tab = self.tab
        with self.say("c5.mod.1") as c:
            self.play(*appear(tab.lines, *tab.titles, *tab.heads, lag=0.15, shift=None),  # early: the skeleton is shown whole, then walked
                      run_time=min(1.6, c.until("three")))
            c.wait_until("three flip-flops")
            icons = VGroup(*[tiny_dff() for _ in range(3)]).arrange(RIGHT, buff=0.12).move_to(_p(PX, 0.9))
            self.play(*appear(*icons, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("two to the power")
            eight = MathTex(r"2^3 = 8", r"\ \text{states}", font_size=52, color=GOLD).move_to(_p(PX, -0.7))
            self.play(*appear(eight), run_time=1.0)
            self.side = [icons, eight]
            c.wait_until("layout")

            # {layout}: a flash runs down each group rule
            self.play(*[VShowPassingFlash(l.copy().set_stroke(YELLOW, 5), time_width=0.5)
                        for l in tab.lines[:2]], run_time=1.5)
            c.wait_until("current")

            # {current}, {next}, {inputs}: one box slides over the header groups
            box = head_box(tab, 0)
            self.play(FadeIn(box), run_time=0.8)
            msb = label_pointer("MSB", tab.heads[0][0], direction=DOWN, color=YELLOW, size=30, length=0.4)
            c.wait_until("most significant")
            self.play(*appear(msb), run_time=1.0)
            c.wait_until("next")
            self.play(Transform(box, head_box(tab, 1)), run_time=1.2)
            c.wait_until("inputs")
            self.play(Transform(box, head_box(tab, 2)), run_time=1.2)
            self.wait(min(2.0, c.until(floor=0)))
            self.play(FadeOut(box), run_time=min(0.8, c.until(floor=0.3)))
            self.msb = msb

    # ------------------------------------------------ step 1: the count sequence
    def clip2(self):
        tab = self.tab
        with self.say("c5.mod.2") as c:
            self.play(*disappear(*self.side), run_time=1.0)
            s1 = step_text(1, "Write down the\ndesired count\nsequence in the\ncurrent state columns")
            s1.move_to(_p(PX, 0)).align_to(_p(0, 3.45), UP).align_to(_p(STEP_L, 0), LEFT)
            c.wait_until(own_word=s1.txt, cue="step one")
            self.play(*appear(s1), run_time=1.0)
            self.steps = [s1]
            c.wait_until("count")

            # {count}: ch4's binary column, then each row flies into the current-state columns
            # the count fills the current-state columns in place, row by row from the top
            self.play(FadeOut(self.msb), run_time=0.5)
            self.play(*appear(*tab.cur, lag=0.3, shift=None), run_time=min(2.6, c.until("from zero")))
            c.wait_until("from zero")
            self.play(*appear(*tab.dec, lag=0.3, shift=None), run_time=min(2.6, c.until("order")))
            c.wait_until("order")

            # {order}: a downward arrow beside the column
            arr = Arrow(_p(TX + MT_DEC - 0.55, mt_row_y(0) + 0.15), _p(TX + MT_DEC - 0.55, mt_row_y(7) - 0.15),
                        buff=0, stroke_width=5, color=GOLD, max_tip_length_to_length_ratio=0.08)
            lab = T("count order", 30, GOLD).next_to(arr, DOWN, buff=0.3).align_to(_p(-6.55, 0), LEFT)
            self.play(GrowArrow(arr), run_time=1.0)
            self.play(*appear(lab), run_time=1.0)
            self.order = [arr, lab]

    # ------------------------------------------------ step 2: next states
    def next_row(self, i, rt):
        """Row i's next state is born from row i+1's current state: a copy fades in inside row i+1's
        (still empty) next-state cell, clear of the divider, then rises into row i."""
        tab = self.tab
        cp, anim = travel(tab.cur[i + 1], [tab.nxt[i + 1].get_center(), tab.nxt[i].get_center()])
        return cp, anim

    def clip3(self):
        tab = self.tab
        with self.say("c5.mod.3") as c:
            s2 = step_text(2, "Write down the\nrequired next\nstates in the next\nstate columns")
            s2.align_to(self.steps[0], LEFT).next_to(self.steps[0], DOWN, buff=0.4, aligned_edge=LEFT)
            c.wait_until(own_word=s2.txt, cue="step two")
            self.play(*appear(s2), *set_alpha([self.steps[0]], 0.4), run_time=1.0)
            self.steps.append(s2)
            c.wait_until("r0")

            for cue, i, nxt_cue, rt in (("r0", 0, "r1", 2.0), ("r1", 1, "down", 1.6)):
                c.wait_until(cue)
                # the row we're on (YELLOW), then its source, row i+1's current state (lighter)
                y = mt_row_y(i)
                x0, x1 = TX + MT_DEC - 0.3, TX + MT_GX[1] + MT_DX + 0.3
                row_box = Rectangle(width=x1 - x0, height=0.5).move_to(_p((x0 + x1) / 2, y))
                row_box.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.1).set_z_index(-1)
                src_box = SurroundingRectangle(tab.cur[i + 1], buff=0.08).set_stroke(YELLOW, 2, opacity=0.45)
                self.play(FadeIn(row_box), run_time=0.6)
                self.play(FadeIn(src_box), run_time=0.5)
                cp, anim = self.next_row(i, rt)
                self.play(anim, run_time=min(rt, c.until(nxt_cue)))
                self.remove(cp)
                self.add(tab.nxt[i])
                self.play(FadeOut(row_box), FadeOut(src_box), run_time=min(0.5, c.until(nxt_cue)))
            c.wait_until("down")

            # {down}: rows 2..6, quickly, top to bottom
            cps, anims = [], []
            for k, i in enumerate(range(2, 7)):
                cp, anim = self.next_row(i, 1.0)
                cps.append(cp)
                anims += during([anim], 0.2 * k, 0.2 * k + 0.2)   # one copy at a time
            self.play(*anims, run_time=min(2.4, c.until("wrap")))
            self.remove(*cps)
            self.add(*tab.nxt[2:7])
            c.wait_until("wrap")

            # {wrap}: row 7 gets row 0's state, down the channel between the groups
            arc = CurvedArrow(_p(CH - 0.3, mt_row_y(0)), _p(CH + 0.3, mt_row_y(7)), angle=-0.25,
                              color=YELLOW, stroke_width=4)
            self.play(Create(arc), run_time=1.2)
            # row 0's current state is the source (light box); 0 0 0 appears at the arrow's tip
            src_box = SurroundingRectangle(tab.cur[0], buff=0.08).set_stroke(YELLOW, 2, opacity=0.45)
            self.play(FadeIn(src_box), run_time=0.5)
            c.wait_until("zero zero zero")
            self.play(*appear(tab.nxt[7], shift=0.25 * RIGHT), run_time=min(1.2, c.until(floor=0.5)))
            self.play(FadeOut(src_box), run_time=min(0.6, c.until(floor=0.3)))
            self.wrap = arc

    # ------------------------------------------------ step 3: the inputs
    def clip4(self):
        tab = self.tab
        with self.say("c5.mod.4") as c:
            s3 = step_text(3, "Fill in the FF\ninputs required to\ngive the defined\nnext state")
            s3.next_to(self.steps[1], DOWN, buff=0.4, aligned_edge=LEFT)
            c.wait_until(own_word=s3.txt, cue="step three")
            self.play(*appear(s3), *set_alpha([self.steps[1]], 0.4), FadeOut(self.wrap), run_time=1.0)
            c.wait_until("lookup")

            # {lookup}: steps 1-2 and the order arrow make room; s4's table and D = Q'
            dtab = d_exc_table().scale(0.8).move_to(_p(PX, 0.0))
            rule = MathTex("D", "=", "Q'", font_size=64).move_to(_p(PX, -2.3))
            rule[0].set_color(BLUE)
            rule[2].set_color(GREEN)
            self.play(*during(disappear(*self.steps[:2], *self.order), 0, 0.45),
                      *during([s3.animate.align_to(_p(0, 3.45), UP)], 0.3, 1.0), run_time=1.4)
            self.play(*appear(dtab, shift=None), run_time=1.0)
            self.play(*appear(rule, shift=None), run_time=min(1.0, c.until("copy")))
            c.wait_until("copy")

            # {copy}: next-state columns slide right as copies into the D columns
            rbox = SurroundingRectangle(rule, color=YELLOW, buff=0.18).set_stroke(YELLOW, 3)
            self.play(FadeIn(rbox), run_time=0.6)
            cps, anims = [], []
            for i in range(8):
                cp, anim = travel(tab.nxt[i], [tab.nxt[i].get_center() + RIGHT * 1.85, tab.inp[i].get_center()])
                cps.append(cp)
                anims.append(anim)
            self.play(*anims, run_time=min(2.0, c.until("skip")))
            self.play(FadeOut(rbox), run_time=min(0.6, c.until("skip")))
            self.remove(*cps)
            self.add(*tab.inp)
            c.wait_until("skip")

            # {skip}: "=" between the groups, the slide's note, D group dims briefly
            eq = set_backstroke(MathTex("=", font_size=72, color=YELLOW), width=14)
            eq.move_to(_p(TX + MT_SEPS[1], (mt_row_y(0) + mt_row_y(7)) / 2))
            note = T("Note: Since D = Q′, for a D-FF, the required\nFF inputs are identical to the required next state",
                     28, DIM, line_spacing=0.9)
            note.move_to(_p(tab.lines.get_center()[0] - 0.4, -3.2))
            dgroup = [tab.titles[2], tab.heads[2], *tab.inp]
            self.play(*appear(eq, shift=None), run_time=0.8)
            self.play(*appear(note), *set_alpha(dgroup, DIMMED), run_time=1.2)
            c.wait_until("identical")
            self.play(*set_alpha(dgroup, 1), run_time=1.0)
            self.side = [s3, dtab, rule, eq]
            self.note = note

    # ------------------------------------------------ what the logic must produce
    def clip5(self):
        tab = self.tab
        with self.say("c5.mod.5") as c:
            self.play(*disappear(*self.side), run_time=1.0)
            c.wait_until("columns")

            # {columns}: the three D columns glow BLUE, eight bits each
            boxes = [SurroundingRectangle(VGroup(tab.heads[2][j], tab.col(2, j)), color=BLUE, buff=0.1)
                     .set_stroke(BLUE, 3).set_fill(BLUE, 0.1).set_z_index(-1) for j in range(3)]
            digits = [m for row in tab.inp for m in row]
            self.play(*appear(*boxes, lag=0.3, shift=None), *recolor(digits, BLUE), run_time=1.5)
            c.wait_until("logic")

            # {logic}: s2's logic box, small: Q2 Q1 Q0 in, D2 D1 D0 out
            lbox = RoundedRectangle(corner_radius=0.2, width=3.1, height=1.3).set_stroke(BLUE, 4).move_to(_p(PX, 0))
            ltxt = VGroup(T("combinational", 30), T("logic", 30)).arrange(DOWN, buff=0.12).move_to(lbox)
            xs = [PX - 0.9, PX, PX + 0.9]
            qin = VGroup(*[MathTex(f"Q_{2 - j}", font_size=38, color=GREEN).move_to(_p(x, 2.1)) for j, x in enumerate(xs)])
            dout = VGroup(*[MathTex(f"D_{2 - j}", font_size=38, color=BLUE).move_to(_p(x, -2.1)) for j, x in enumerate(xs)])
            a_in = [Arrow(_p(x, 1.8), _p(x, 0.65), buff=0, stroke_width=4, color=GREEN) for x in xs]
            a_out = [Arrow(_p(x, -0.65), _p(x, -1.8), buff=0, stroke_width=4, color=BLUE) for x in xs]
            self.play(*appear(lbox, ltxt, shift=None), run_time=1.0)
            self.play(*appear(*qin, shift=None, lag=0.1), *[GrowArrow(a) for a in a_in],
                      *[GrowArrow(a) for a in a_out], *appear(*dout, shift=None, lag=0.1), run_time=1.4)
            c.wait_until("keep")
            c.wait_until("the one")

            # {keep}: the table alone, centred
            self.play(*disappear(lbox, ltxt, *qin, *dout, *a_in, *a_out, *boxes, self.note),
                      *recolor(digits, FG), run_time=1.0)
            settle(self, tab)
            self.play(tab.animate.shift(RIGHT * -TX), run_time=min(1.5, c.until(floor=0.5)))
        self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
