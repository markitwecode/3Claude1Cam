"""Chapter 5, scene 5: the synchroniser's state transition table, with don't-care inputs (p. 140). Clips c5.table.1 – c5.table.5.

Shared helpers (load_scene("ch5_s5_table")), for s6, s7, s8 and ch6's one-hot table:
- `coded_diagram(codes=None)`: ch5_s4's coded_diagram() (sync_diagram(SYNC_CODES, unused=True),
  scaled 0.55 about the origin, shifted (-3.9, 0.05): x -6.58 .. -1.03). Other codes (ch6's
  one-hot): the same placement applied to sync_diagram(codes, unused=True).
- `state_table(rows, heads, titles, head_colors, breaks, dim_rows, x, filled=True)`: p. 140's
  table in L6's mod_table() styling (T 28 titles, MathTex 40 GREEN/BLUE sub-headers, MathTex 38
  cells, DIM stroke-2 rules). rows: one tuple of strings per row, one string per column group, one
  character per cell (e.g. ("00", "X0", "00")). heads: per group, the MathTex of each column.
  breaks: row indices that get a rule above them. A double rule stands before the last group.
  Absolute y: titles 3.35, sub-headers 2.75, rows ROW0_Y - PITCH * i. Centred at x.
  .titles[g] .heads[g] (VGroup of cells) .lines (all rules) .vlines .hrules (group rules, in
  `breaks` order) .rows[i] (VGroup of group VGroups) .cell(i, g, j) .col(g, j) .row_y(i)
  .make_row(strings, y, color) (an extra row in the same columns, not added). filled=False: the
  group holds only lines (titles, heads and rows built but not in it).
- `sync_table(filled=True)`: this scene's table (SYNC_ROWS, unused row DIM).
- `handover_shot()`: VGroup(coded_diagram(), sync_table()), this scene's last frame.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- shared: the coded diagram
SYNC_CODES = {"Hunt": "00", "Sight": "01", "Sync": "10"}
DIAG_SCALE, DIAG_SHIFT = 0.55, (-3.9, 0.05)     # ch5_s4's placement


def coded_diagram(codes=None):
    if codes is None:
        return load_scene("ch5_s4_twoffs").coded_diagram()
    d = load_scene("ch5_s3_diagram").sync_diagram(codes=codes, unused=True)
    d.scale(DIAG_SCALE, about_point=ORIGIN)
    d.shift(_p(*DIAG_SHIFT))
    return d


# ---------------------------------------------------------------- shared: the state table
SYNC_ROWS = [("00", "X0", "00"), ("00", "X1", "01"),
             ("01", "0X", "01"), ("01", "10", "00"), ("01", "11", "10"),
             ("10", "0X", "10"), ("10", "10", "00"), ("10", "11", "10"),
             ("11", "XX", "XX")]
SYNC_HEADS = (("s_1", "s_0"), ("e", "r"), ("s_1'", "s_0'"))
SYNC_TITLES = ("Current state", "Input", "Next state")
TABLE_X = 3.05
TITLE_Y, HEAD_Y, HEAD_RULE_Y = 3.35, 2.75, 2.38
ROW0_Y, PITCH = 2.0, 0.48
DX = 0.7


def state_table(rows=SYNC_ROWS, heads=SYNC_HEADS, titles=SYNC_TITLES, head_colors=(GREEN, BLUE, GREEN),
                breaks=(2, 5, 8), dim_rows=(), x=TABLE_X, filled=True):
    tit = [T(s, 28) for s in titles]
    widths = [max(t.width, len(h) * DX) + 0.5 for t, h in zip(tit, heads)]
    total = sum(widths)
    left = x - total / 2
    edges = [left]
    for w in widths:
        edges.append(edges[-1] + w)
    gx = [(edges[k] + edges[k + 1]) / 2 for k in range(len(heads))]

    def col_x(g, j):
        n = len(heads[g])
        return gx[g] + (j - (n - 1) / 2) * DX

    def row_y(i):
        return ROW0_Y - PITCH * i

    for t, cx in zip(tit, gx):
        t.move_to(_p(cx, TITLE_Y))
    titles_g = VGroup(*tit)
    heads_g = VGroup(*[VGroup(*[MathTex(h, font_size=40, color=col).move_to(_p(col_x(g, j), HEAD_Y))
                                for j, h in enumerate(hs)])
                       for g, (hs, col) in enumerate(zip(heads, head_colors))])

    def make_row(strings, y, color=FG):
        return VGroup(*[VGroup(*[MathTex(ch, font_size=38, color=color).move_to(_p(col_x(g, j), y))
                                 for j, ch in enumerate(s)])
                        for g, s in enumerate(strings)])

    row_mobs = [make_row(r, row_y(i), DIM if i in dim_rows else FG) for i, r in enumerate(rows)]
    top, bot = TITLE_Y + 0.3, row_y(len(rows) - 1) - 0.3
    vlines = VGroup()
    for k in range(1, len(heads)):
        ex = edges[k]
        if k == len(heads) - 1:
            vlines.add(Line(_p(ex - 0.05, top), _p(ex - 0.05, bot)).set_stroke(DIM, 2))
            vlines.add(Line(_p(ex + 0.05, top), _p(ex + 0.05, bot)).set_stroke(DIM, 2))
        else:
            vlines.add(Line(_p(ex, top), _p(ex, bot)).set_stroke(DIM, 2))
    head_rule = Line(_p(left + 0.1, HEAD_RULE_Y), _p(edges[-1] - 0.1, HEAD_RULE_Y)).set_stroke(DIM, 2)
    hrules = [Line(_p(left + 0.1, row_y(b) + PITCH / 2), _p(edges[-1] - 0.1, row_y(b) + PITCH / 2)).set_stroke(DIM, 2)
              for b in breaks]
    lines = VGroup(*vlines, head_rule, *hrules)
    g = VGroup(lines, titles_g, heads_g, *row_mobs) if filled else VGroup(lines)
    g.titles, g.heads, g.lines, g.vlines, g.hrules, g.head_rule = titles_g, heads_g, lines, vlines, hrules, head_rule
    g.rows = row_mobs
    g.cell = lambda i, gi, j: row_mobs[i][gi][j]
    g.col = lambda gi, j: VGroup(*[r[gi][j] for r in row_mobs])
    g.row_y, g.col_x, g.make_row = row_y, col_x, make_row
    g.edges, g.bottom_y = edges, bot
    return g


def sync_table(filled=True):
    return state_table(dim_rows=(8,), filled=filled)


def handover_shot():
    return VGroup(coded_diagram(), sync_table())


# ---------------------------------------------------------------- local
ROW_ARC = [3, 4, 5, 7, 6, 0, 2, 1]    # the diagram arc each used row reads
CAP_Y, EXPL_Y = -2.6, -3.15     # below the table (bottom rule -2.14), right of the diagram's [11]
TAGS_CX = 2.8


def cell_box(mobs, color=YELLOW, buff=0.1):
    return SurroundingRectangle(*mobs, color=color, buff=buff).set_stroke(color, 2).set_fill(color, 0.2).set_z_index(-1)


def explode(scene, row):
    """Put a row's cells on screen as separate objects (no visible change), so one cell can be swapped."""
    cells = [m for grp in row for m in grp]
    scene.remove(*row.get_family())
    scene.add(*cells)
    return cells


class TheTable(NarratedScene):
    def construct(self):
        self.d = coded_diagram()
        self.t = sync_table()
        self.lit = None
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ---- helpers
    def glow(self, name, prev=None):
        anims = [restyle(self.d.circle[name], outline=YELLOW, width=6)]
        if prev:
            anims.append(restyle(self.d.circle[prev], outline=FG, width=4))
        return anims

    def unglow(self, name):
        return [restyle(self.d.circle[name], outline=FG, width=4)]

    def arc_anims(self, i=None):
        d, anims = self.d, []
        if self.lit is not None:
            anims += [d.arcs[self.lit].animate.set_color(FG).set_stroke(width=3, family=False), d.labels[self.lit].animate.set_color(BLUE)]
        if i is not None:
            anims += [d.arcs[i].animate.set_color(YELLOW).set_stroke(width=5, family=False), d.labels[i].animate.set_color(YELLOW)]
        self.lit = i
        return anims

    def write_row(self, i, extra=(), rt=1.5):
        row = self.t.rows[i]
        self.play(*appear(*row, lag=0.3), *self.arc_anims(ROW_ARC[i]) if i < 8 else (), *extra, run_time=rt)
        settle(self, row)

    def pulse(self, mob, color=YELLOW):
        return VShowPassingFlash(mob.copy().set_stroke(color, 8), time_width=1.0)

    # ---- clips
    def clip1(self):
        d, t = self.d, self.t
        with self.say("c5.table.1") as c:
            self.play(*appear(d, t.lines, shift=None, lag=0.4), run_time=min(2.0, c.until("cols")))  # early: recap of s4's coded diagram, the source of every row
            for g, cue, nxt in ((0, "the current state", "in the middle"),
                                (1, "the inputs", "on the right"),
                                (2, "the next state", "build")):
                c.wait_until(cue)
                self.play(*appear(t.titles[g], *t.heads[g], lag=0.25), run_time=min(1.2, 0.5 * c.until(nxt)))
                self.play(FlashUnder(t.heads[g], time_width=1.5, color=t.heads[g][0].get_color()),
                          run_time=min(1.2, 0.8 * c.until(nxt)))
                c.wait_until(nxt)
            self.play(self.pulse(d.circle["Hunt"]), run_time=min(1.6, c.until()))

    def clip2(self):
        d, t = self.d, self.t
        with self.say("c5.table.2") as c:
            self.play(*self.glow("Hunt"), run_time=min(1.0, c.until("r0")))
            c.wait_until("r0")
            self.write_row(0, rt=min(1.6, 0.6 * c.until("r1")))
            c.wait_until("r1")
            self.write_row(1, rt=min(1.6, 0.6 * c.until("ex")))
            c.wait_until("ex")
            self.box_e = cell_box([t.cell(0, 1, 0), t.cell(1, 1, 0)])
            self.play(FadeIn(self.box_e), run_time=min(1.0, c.until("so the")))
            c.wait_until("so the")
            self.play(*flash([t.cell(0, 1, 0), t.cell(1, 1, 0)], run_time=1.5, time_width=1.5),
                      run_time=min(1.5, c.until()))

    def clip3(self):
        d, t = self.d, self.t
        with self.say("c5.table.3") as c:
            self.play(*self.glow("Sight", "Hunt"), *self.arc_anims(None), FadeOut(self.box_e),
                      run_time=min(1.2, c.until("e0")))
            c.wait_until("e0")
            self.write_row(2, rt=min(1.6, 0.4 * c.until("e1r0")))
            c.wait_until("so ar gets")
            box_r = cell_box([t.cell(2, 1, 1)])
            self.play(FadeIn(box_r), run_time=min(1.0, c.until("e1r0")))
            c.wait_until("e1r0")
            self.write_row(3, extra=[FadeOut(box_r)], rt=min(1.6, 0.6 * c.until("e1r1")))
            c.wait_until("e1r1")
            self.write_row(4, rt=min(1.6, 0.6 * c.until("sync")))
            c.wait_until("sync")
            self.play(*self.glow("Sync", "Sight"), *self.arc_anims(None), run_time=min(1.2, c.until("with ee zero")))
            c.wait_until("with ee zero")
            self.write_row(5, rt=min(1.5, 0.6 * c.until("with ee one")))
            c.wait_until("with ee one")
            self.write_row(6, rt=min(1.3, 0.8 * c.until("and stays")))
            c.wait_until("and stays")
            self.write_row(7, rt=min(1.3, c.until()))

    def clip4(self):
        d, t = self.d, self.t
        with self.say("c5.table.4") as c:
            row = t.rows[8]
            self.play(*self.unglow("Sync"), *self.arc_anims(None), *appear(*row, lag=0.3),
                      d.unused.circle.animate(rate_func=there_and_back_with_pause).set_stroke(YELLOW, 7),
                      d.unused.code.animate(rate_func=there_and_back_with_pause).set_color(YELLOW),
                      self.pulse(d.unused.circle), run_time=min(2.2, c.until("never")))
            settle(self, row)
            self.cap = T("next-state logic never sees 11", 30, DIM).move_to(_p(TABLE_X, CAP_Y))
            c.wait_until("never", own_word=self.cap)
            self.play(*appear(self.cap), run_time=min(1.0, c.until("xx")))
            c.wait_until("xx")
            self.play(FlashAround(row[2], time_width=1.5, color=YELLOW), run_time=min(1.6, c.until()))

    def clip5(self):
        d, t = self.d, self.t
        with self.say("c5.table.5") as c:
            tag1 = T("X under the inputs", 30, YELLOW)
            tag2 = T("X in the next state", 30, FG)
            VGroup(tag1, tag2).arrange(RIGHT, buff=0.45).move_to(_p(TAGS_CX, CAP_Y))
            self.play(*swap(self.cap, VGroup(tag1, tag2)), run_time=min(1.2, c.until("inputx")))  # early: the two kinds are named together, then read one by one
            c.wait_until("inputx")
            box1 = cell_box([t.cell(0, 1, 0)])
            self.play(FadeIn(box1), run_time=min(1.0, c.until("both values")))
            c.wait_until("both values")
            expl1 = T("either value, same next state", 28, FG).move_to(_p(0, EXPL_Y)).align_to(tag1, LEFT)
            self.play(*appear(expl1), run_time=min(1.0, c.until("expand")))

            # {expand}: row 1 splits in two. The unused row steps aside so the table keeps its size,
            # rows 2-8 move down one pitch, a copy of row 1 fills the gap under it, then each X is resolved.
            c.wait_until("expand")
            r0, last, rule8 = t.rows[0], t.rows[8], t.hrules[2]
            below = [*t.rows[1:8], *t.hrules[:2]]
            self.play(*during([FadeOut(box1), *disappear(last), restyle(rule8, 0)], 0, 0.4),
                      *during([m.animate.shift(PITCH * DOWN) for m in below], 0.35, 1.0),
                      run_time=min(1.4, 0.8 * c.until("two rows")))
            c.wait_until("two rows")
            r1 = r0.copy().shift(PITCH * DOWN)
            self.play(*appear(r1, shift=None), FlashAround(VGroup(r0, r1), time_width=1.5),
                      run_time=min(1.5, 0.9 * c.until("ee zero")))
            cellsA, cellsB = explode(self, r0), explode(self, r1)
            xA, xB = cellsA[2], cellsB[2]
            zero = MathTex("0", font_size=38, color=YELLOW).move_to(xA)
            one = MathTex("1", font_size=38, color=YELLOW).move_to(xB)
            c.wait_until("ee zero")
            self.play(*swap(xA, zero), run_time=min(1.0, 0.9 * c.until("ee one")))
            c.wait_until("ee one")
            self.play(*swap(xB, one), run_time=min(1.0, 0.8 * c.until("nextx")))

            # fold back: the copy leaves, the 0 turns back into X, the rows close up, the unused row returns
            c.wait_until("nextx")
            xA2 = xA.copy().set_opacity(1)
            self.play(*during(disappear(*[m for m in cellsB if m is not xB], one), 0, 0.5),
                      *during(disappear(expl1), 0, 0.5),
                      *during(swap(zero, xA2), 0.3, 1.0),
                      run_time=min(1.0, 0.3 * c.until("that row never")))
            self.play(*during([m.animate.shift(PITCH * UP) for m in below], 0, 0.6),
                      *during([*appear(last, shift=None), restyle(rule8, 1)], 0.55, 1.0),
                      run_time=min(1.3, 0.45 * c.until("that row never")))
            box2 = cell_box([t.rows[8][2]], color=DIM)
            self.play(FadeIn(box2), run_time=min(1.0, c.until("that row never")))
            c.wait_until("that row never")
            expl2 = T("never happens: 0 or 1, whichever is simpler", 28, FG).move_to(_p(0, EXPL_Y)).align_to(tag2, RIGHT)
            self.play(*appear(expl2), run_time=min(1.0, c.until()))
        self.wait(2.2)
        self.play(*disappear(tag1, tag2, expl2, box2), run_time=1.0)
        # handover: swap the pieces for the exact shot s6 opens on
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)
