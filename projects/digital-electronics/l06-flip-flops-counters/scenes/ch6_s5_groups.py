"""Chapter 6, scene 5: grouping the K-map for D2, and the expression. Clips c6.group.1 – c6.group.5."""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- the K-map (s4's end shot)
# ---- ch6_s4_kmap's kmap() (copied verbatim) -------------------------------------------------
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


def kmap_d2(center=KM_CENTER):
    """s4's finished map, plus .sq[r][k] (cell-sized rectangles, not drawn: for flashes and loops)
    and .dig[r][k] (the entries)."""
    m = kmap(center=center, values=D2_MAP)
    m.sq = [[m.cell_rect(r, k) for k in range(4)] for r in range(2)]
    m.dig = [[m.entries[4 * r + k] for k in range(4)] for r in range(2)]
    return m


# ---------------------------------------------------------------- loops
def rounded_path(pts_corners, rad, n=8):
    """Polyline through corner points with each inner corner rounded (radius rad)."""
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
    """A rounded loop round a block of cells [(r, c), ...]."""
    sqs = VGroup(*[m.sq[r][c] for r, c in cells])
    return RoundedRectangle(corner_radius=0.32, width=sqs.width - 2 * inset, height=sqs.height - 2 * inset,
                            stroke_color=color, stroke_width=6).move_to(sqs)


def half_loop(m, r, c, open_to, color, inset=0.1, ext=0.2):
    """A loop round one edge cell, open off the map's edge (open_to = LEFT or RIGHT)."""
    sq = m.sq[r][c]
    x0, x1 = sq.get_left()[0], sq.get_right()[0]
    t, b = sq.get_top()[1] - inset, sq.get_bottom()[1] + inset
    if open_to is LEFT:
        xo, xi = x0 - ext, x1 - inset
    else:
        xo, xi = x1 + ext, x0 + inset
    return rounded_path([[xo, t, 0], [xi, t, 0], [xi, b, 0], [xo, b, 0]], 0.32).set_stroke(color, 6)


def lone_circle(m, r, c, color):
    return Circle(radius=0.44, stroke_color=color, stroke_width=6).move_to(m.sq[r][c])


def map_loops(m):
    pink = lone_circle(m, 0, 2, PINK)
    purple = VGroup(half_loop(m, 1, 0, LEFT, PURPLE), half_loop(m, 1, 3, RIGHT, PURPLE))
    teal = loop_round(m, [(1, 0), (1, 1)], TEAL, inset=0.2)
    return pink, purple, teal


# ---------------------------------------------------------------- equations
E1 = ["D_2", "=", r"\overline{Q_0}", ".", "Q_2", "+", r"\overline{Q_1}", ".", "Q_2", "+", r"Q_0.Q_1.\overline{Q_2}"]
E2 = ["D_2", "=", "Q_2", ".", "(", r"\overline{Q_0}", "+", r"\overline{Q_1}", ")", "+", r"Q_0.Q_1.\overline{Q_2}"]
EQ_SIZE = 56
LINE1_Y, LINE2_Y, LABEL_Y = 1.3, -1.0, -1.95


def line1():
    e = MathTex(*E1, font_size=EQ_SIZE)
    for i in (2, 3, 4):
        e[i].set_color(PURPLE)
    for i in (6, 7, 8):
        e[i].set_color(TEAL)
    e[10].set_color(PINK)
    return e.move_to([0, LINE1_Y, 0])


def line2(l1):
    e = MathTex(*E2, font_size=EQ_SIZE)
    e[2].set_color(YELLOW)
    e[5].set_color(PURPLE)
    e[7].set_color(TEAL)
    e[10].set_color(PINK)
    e.move_to([0, LINE2_Y, 0]).align_to(l1, LEFT)
    return e


def drop_from(src, dst):
    """dst comes out of src: it fades in from just under src (clear of it) and travels to its place."""
    return FadeIn(dst, target_position=src.get_center() + 0.8 * DOWN)


class Groups(NarratedScene):
    def consolidate(self, olds, new):
        self.remove(*[f for o in olds for f in o.get_family()])
        self.add(new)

    def mark_under(self, term, color):
        """An underline spanning the whole term draws left to right, holds, then fades: nothing lingers."""
        ln = underline(term, color, buff=0.12)
        self.play(Create(ln), run_time=0.6)
        self.wait(0.3)
        self.play(FadeOut(ln), run_time=0.5)

    def construct(self):
        m = kmap_d2()                                # s4's end placement; s4 faded out, so fade in
        self.m = m
        self.pink, self.purple, self.teal = map_loops(m)
        self.l1 = line1()
        l1 = self.l1
        # term labels under the map, each straight below its place in the equation
        self.lab_purple = VGroup(*[l1[i].copy() for i in (2, 3, 4)])
        self.lab_teal = VGroup(*[l1[i].copy() for i in (6, 7, 8)])
        self.lab_pink = l1[10].copy()
        for lab in (self.lab_purple, self.lab_teal, self.lab_pink):
            lab.set_y(LABEL_Y)

        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(x) for x in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------ c6.group.1
    def clip1(self):
        m = self.m
        with self.say("c6.group.1") as c:
            cap = T("blocks of 1, 2, 4 or 8 cells, as large as possible", 34, DIM).move_to([0, -3.15, 0])
            ones = [(0, 2), (1, 0), (1, 1), (1, 3)]
            self.play(FadeIn(m), run_time=1.0)
            self.play(*appear(cap), run_time=1.0)  # early: the rule, said as it appears
            self.play(LaggedStart(*[FlashAround(m.sq[r][q], color=YELLOW, time_width=1.5) for r, q in ones],
                                  lag_ratio=0.3), run_time=min(2.0, c.until("lone")))
            c.wait_until("lone")
            self.play(FlashAround(m.sq[0][2], color=YELLOW, time_width=1.5, stroke_width=6), run_time=1.5)
            c.wait_until("around")
            nboxes = []
            for cue, (r, q) in (("left", (0, 1)), ("right", (0, 3)), ("below", (1, 2))):
                c.wait_until(cue)
                bx = m.cell_rect(r, q).set_stroke(YELLOW, 5).set_fill(opacity=0)
                self.play(FadeIn(bx), run_time=0.8)
                nboxes.append(bx)
            c.wait_until("alone")
            self.play(*disappear(*nboxes), run_time=0.8)
            self.play(Create(self.pink), run_time=1.2)
            c.wait_until("gives the term")
            self.play(*appear(self.lab_pink), run_time=1.0)
            c.wait_until()
            self.cap = cap

    # ------------------------------------------------------------ c6.group.2
    def readout(self, vals):
        rows = VGroup()
        for name, v in vals:
            k = MathTex(name, "=", font_size=46)
            val = MathTex(v, font_size=46).next_to(k, RIGHT, buff=0.2)
            rows.add(VGroup(k, val))
        rows.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.75, KM_CENTER[1], 0])
        return rows

    def flicker(self, row, c):
        val = row[1]
        seq = ["1", "0"] if val.get_tex_string() == "0" else ["0", "1"]
        cur = val
        for s in seq:
            nxt = MathTex(s, font_size=46, color=YELLOW).move_to(cur)
            self.play(FadeOut(cur), run_time=0.3)        # in place: old gone before new arrives
            self.play(FadeIn(nxt), run_time=0.3)
            cur = nxt
        row.remove(val)
        row.add(cur)

    def strike(self, row):
        ln = Line(row.get_left() + 0.15 * LEFT, row.get_right() + 0.15 * RIGHT, stroke_color=RED, stroke_width=6)
        self.play(Create(ln), *set_alpha([row], 0.4), run_time=0.8)
        return ln

    def clip2(self):
        m = self.m
        with self.say("c6.group.2") as c:
            self.play(*disappear(self.cap), FlashAround(m.sq[1][0], color=YELLOW, time_width=1.5),
                      FlashAround(m.sq[1][3], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("far")
            y = m.sq[1][0].get_center()[1] - 0.38
            arr = DashedLine([m.sq[1][0].get_center()[0] + 0.1, y, 0], [m.sq[1][3].get_center()[0] - 0.1, y, 0],
                             dash_length=0.14, stroke_color=YELLOW, stroke_width=4)
            arr.add_tip(tip_length=0.22, tip_width=0.22)
            arr.add_tip(at_start=True, tip_length=0.22, tip_width=0.22)
            self.play(GrowFromCenter(arr), run_time=1.0)
            c.wait_until("wrap")
            self.play(*disappear(arr), run_time=0.6)
            self.play(Create(self.purple[0]), Create(self.purple[1]), run_time=1.5)
            c.wait_until("read")
            ro = self.readout([("Q_2", "1"), ("Q_1", "0"), ("Q_0", "0")])
            self.play(*appear(ro[0]), run_time=0.8)
            c.wait_until("cue zero is zero")
            self.play(*appear(ro[2]), run_time=0.8)
            c.wait_until("while cue one changes")
            self.play(*appear(ro[1]), run_time=0.6)
            self.flicker(ro[1], c)
            c.wait_until("so cue one drops out")
            s1 = self.strike(ro[1])
            c.wait_until("term")
            self.play(*appear(self.lab_purple), run_time=1.2)
            c.wait_until("last")
            self.play(*disappear(ro, s1), run_time=0.8)
            self.play(Create(self.teal), run_time=1.2)
            c.wait_until("drop")
            ro2 = self.readout([("Q_2", "1"), ("Q_1", "0"), ("Q_0", "0")])
            self.play(*appear(*ro2, lag=0.15), run_time=0.8)
            self.flicker(ro2[2], c)
            c.wait_until("drops out")
            s2 = self.strike(ro2[2])
            c.wait_until("leaving")
            self.play(*appear(self.lab_teal), run_time=1.0)
            c.wait_until()
            self.ro2 = VGroup(ro2, s2)

    # ------------------------------------------------------------ c6.group.3
    def clip3(self):
        m = self.m
        with self.say("c6.group.3", gap=0.8) as c:
            self.play(*disappear(self.ro2), run_time=0.8)
            q = T("Essential?", 44, YELLOW).move_to([0, -3.15, 0])
            self.play(*appear(q), run_time=1.0)  # early: the question is put as it appears
            c.wait_until("yes")
            ans = T("all three are essential", 44, GREEN).move_to(q)
            self.play(*swap(q, ans), run_time=1.2)
            for cue, (r, k), col in (("cover", (0, 2), PINK), ("only the corner pair", (1, 3), PURPLE),
                                     ("only the last pair", (1, 1), TEAL)):
                c.wait_until(cue)
                self.play(FlashAround(m.sq[r][k], color=col, time_width=1.5, stroke_width=7), run_time=1.5)
            c.wait_until("shared")
            note = T("covered twice:\nallowed", 34, FG, line_spacing=0.8)
            note.next_to(m, LEFT, buff=0.35).set_y(m.sq[1][0].get_center()[1])
            self.play(FlashAround(m.sq[1][0], color=PURPLE, time_width=1.5, stroke_width=7, buff=0.02),  # early: caption paraphrases this sentence
                      FlashAround(m.sq[1][0], color=TEAL, time_width=1.5, stroke_width=7, buff=0.16),
                      *appear(note), run_time=1.5)
            c.wait_until()
            self.ans, self.note = ans, note

    # ------------------------------------------------------------ c6.group.4
    def clip4(self):
        l1 = self.l1
        with self.say("c6.group.4") as c:
            self.play(*disappear(self.m, self.pink, self.purple, self.teal, self.ans, self.note), run_time=1.0)
            tgt = {self.lab_purple: VGroup(*[l1[i] for i in (2, 3, 4)]),
                   self.lab_teal: VGroup(*[l1[i] for i in (6, 7, 8)]),
                   self.lab_pink: l1[10]}
            glue = [l1[i].copy() for i in (0, 1, 5, 9)]
            self.play(*[lab.animate.move_to(t) for lab, t in tgt.items()],
                      *during(appear(*glue, shift=None, lag=0.15), 0.55, 1.0),
                      run_time=min(1.8, c.until("expr")))
            self.consolidate(list(tgt) + glue, l1)
            c.wait_until("expr")
            for cue, idx, col in (("expr", (2, 3, 4), PURPLE), ("or not cue one", (6, 7, 8), TEAL),
                                  ("or cue zero and cue one", (10,), PINK)):
                c.wait_until(cue)
                self.mark_under(VGroup(*[l1[i] for i in idx]), col)
            c.wait_until("factor")
            self.mark_under(VGroup(*[l1[i] for i in range(2, 9)]), YELLOW)
            c.wait_until("both contain")
            self.play(*recolor([l1[4], l1[8]], YELLOW), run_time=1.0)
            c.wait_until("factor it out")
            l2 = line2(l1)
            # work on loose copies of the pieces, so each flight is the same text end to end
            p1 = [MathTex(t, font_size=EQ_SIZE, color=x.get_color()).move_to(x) for t, x in zip(E1, l1)]
            p2 = [MathTex(t, font_size=EQ_SIZE, color=x.get_color()).move_to(x) for t, x in zip(E2, l2)]
            self.remove(l1)
            self.add(*p1)
            self.play(drop_from(p1[0], p2[0]), drop_from(p1[1], p2[1]), drop_from(p1[4], p2[2]), run_time=1.5)
            c.wait_until("final")
            self.play(drop_from(p1[2], p2[5]), drop_from(p1[6], p2[7]),
                      *during(appear(p2[3], p2[4], p2[6], p2[8], shift=None, lag=0.1), 0.75, 1.0), run_time=1.8)
            c.wait_until("and inside it")
            self.mark_under(VGroup(*p2[5:8]), YELLOW)
            c.wait_until("third")
            self.play(*appear(p2[9], shift=None), drop_from(p1[10], p2[10]), run_time=1.5)
            self.consolidate(p1, l1)
            self.consolidate(p2, l2)
            c.wait_until()
            self.l2 = l2

    # ------------------------------------------------------------ c6.group.5
    def clip5(self):
        l1, l2 = self.l1, self.l2
        with self.say("c6.group.5", gap=1.5) as c:
            eqs = VGroup(l1, l2)
            eqs.generate_target()
            eqs.target.arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale(0.75).move_to([0, 2.55, 0])
            small = kmap_d2(ORIGIN)
            pink, purple, teal = map_loops(small)
            mini = VGroup(small, pink, teal, purple).scale(0.72).move_to([-4.4, -1.3, 0])
            self.play(MoveToTarget(eqs), run_time=1.0)
            self.play(*appear(mini, shift=None), run_time=min(1.0, c.until("miss")))
            c.wait_until("miss")
            dashed = VGroup(*[DashedVMobject(p.copy().set_stroke(RED, 6), num_dashes=10) for p in purple])
            self.play(*[FadeOut(p) for p in purple], *[FadeIn(d) for d in dashed], run_time=0.8)
            self.play(*disappear(dashed), run_time=0.8)
            c.wait_until("on its own")
            red = Circle(radius=0.44 * 0.72, stroke_color=RED, stroke_width=6).move_to(small.dig[1][3])
            self.play(Create(red), run_time=1.0)
            c.wait_until("big")
            bad = MathTex(r"Q_2.Q_1.\overline{Q_0}", font_size=52, color=RED).move_to([0, 0.0, 0]).align_to([-0.7, 0, 0], LEFT)
            bad_n = T("three variables", 32, RED).move_to([0, bad.get_y(), 0]).align_to([2.3, 0, 0], LEFT)
            good = MathTex(r"\overline{Q_0}.Q_2", font_size=52, color=PURPLE)
            good.move_to([0, -1.1, 0]).align_to(bad, LEFT)
            good_n = T("two variables", 32, PURPLE).move_to([bad_n.get_x(), good.get_y(), 0]).align_to(bad_n, LEFT)
            self.play(*appear(bad), run_time=1.0)
            c.wait_until(own_word=bad_n)
            self.play(*appear(bad_n), run_time=0.8)
            c.wait_until("where two variables")
            self.play(*appear(good, good_n, lag=0.3), run_time=1.0)
            c.wait_until("still")
            tick = check_mark(GREEN)
            ok = T("still correct", 34, GREEN)
            okg = VGroup(tick, ok).arrange(RIGHT, buff=0.25).move_to([0, -2.6, 0]).align_to(bad, LEFT)
            big = T("bigger circuit", 34, RED).move_to([0, okg.get_y(), 0]).align_to(bad_n, LEFT).shift(0.9 * RIGHT)
            self.play(*appear(tick, ok, lag=0.2), run_time=1.0)
            c.wait_until("bigger")
            self.play(*appear(big), run_time=1.0)
            c.wait_until()
