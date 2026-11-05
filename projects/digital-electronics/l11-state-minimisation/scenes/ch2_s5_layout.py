"""Chapter 2, scene 5: a cell for every pair; the 8 x 8 grid cut down to p. 150's staircase.
Clips c2.grid.1 - c2.grid.3.

Shared drawings (import with load_scene("ch2_s5_layout")); all are returned at their home positions:
- `P150`: p. 150's rows, (state, next X=0, next X=1, Y), verbatim.
- `p150_table()`: p. 150's state table, left third, header "Present State | Next State X=0 X=1 |
  Output (Y)" (one output column). Same API as ch1_s3_mealy's `state_table`: `.rows[r]` (`.cells` =
  [state, n0, n1, y]), `.cell(r, c)`, `.col(c)`, `.row_of(letter)`, `.h_ps` (alias `.h_cs`) `.h_ns`
  `.h_out`, `.subs` (the two "X=0"/"X=1"), `.xs` (their X glyphs), `.y`, `.head`, `.rules`, `.seps`,
  `.pitch`, `.col_box(cols, color)`, `.row_box(r, color)` (Rectangles, not added).
  Light letters with `recolor(tbl.cell(r, c), YELLOW)`.
- `implication_table()`: p. 150's staircase, right of the table, empty: rows B-H, columns A-G.
  `.cell("A", "B")` -> the Square for pair A-B (column letter first), `.cells` dict {"A-B": Square},
  `.squares` VGroup, `.col_letter("A")`, `.row_letter("B")`, `.col_letters` / `.row_letters` dicts
  (Texts), `.side` (cell side, 0.9), `.pairs` (column by column: A-B, A-C, ... G-H).
- `grid8()`: the full 8 x 8 grid (this scene's layout, right two thirds, side 0.72), same API
  (`.cell(col, row)` for every col, row in A-H), for s8's recap panel.
- `cell_label(it, col, row, size=28, color=FG)`: a "col-row" Text centred in that cell (not added).
- `handover_shot()`: table + empty staircase (this scene's last frame; s6 opens on it).
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
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


LETTERS = "ABCDEFGH"

# ------------------------------------------------------------------ shared: p. 150's state table
P150 = [
    ("A", "D", "C", "0"), ("B", "F", "H", "0"), ("C", "E", "D", "1"), ("D", "A", "E", "0"),
    ("E", "C", "A", "1"), ("F", "F", "B", "1"), ("G", "B", "H", "0"), ("H", "C", "G", "1"),
]
P150_COLS = (0.0, 1.75, 2.75, 4.2)


def p150_table(size=32, pitch=0.6, top=1.75, x0=-5.75):
    xs_ = [x0 + c for c in P150_COLS]
    h_ps = T("Present\nState", size, line_spacing=0.8).move_to(_p(xs_[0], top + 0.75))
    h_ns = T("Next State", size).move_to(_p((xs_[1] + xs_[2]) / 2, top + 0.92))
    h_out = T("Output\n(Y)", size, GREEN, line_spacing=0.8).move_to(_p(xs_[3], top + 0.75))
    subs = [T(s, size, t2c={"X": BLUE}).move_to(_p(xs_[i + 1], top + 0.5))
            for i, s in enumerate(["X=0", "X=1"])]
    left, right = xs_[0] - 0.7, h_out.get_right()[0] + 0.1
    bottom = top - (len(P150) - 1) * pitch - pitch / 2
    head_rule = Line(_p(left, top + 0.29), _p(right, top + 0.29)).set_stroke(DIM, 2)
    seps = VGroup(*[Line(_p(x, top + 1.25), _p(x, bottom)).set_stroke(DIM, 2)
                    for x in ((xs_[0] + xs_[1]) / 2 + 0.05, (xs_[2] + xs_[3]) / 2 - 0.1)])
    row_mobs = []
    for r, vals in enumerate(P150):
        y = top - r * pitch
        cells = []
        for c, v in enumerate(vals):
            t = T(v, size, GREEN, weight=BOLD) if (c == 3 and v == "1") else T(v, size)
            cells.append(t.move_to(_p(xs_[c], y)))
        row = VGroup(*cells)
        row.cells = cells
        row_mobs.append(row)
    rules = VGroup(head_rule)
    head = VGroup(h_ps, h_ns, h_out, *subs)
    tbl = VGroup(head, rules, seps, *row_mobs)
    tbl.head, tbl.rules, tbl.seps, tbl.rows = head, rules, seps, row_mobs
    tbl.h_ps = tbl.h_cs = h_ps
    tbl.h_ns, tbl.h_out, tbl.subs = h_ns, h_out, subs
    tbl.xs = [s[0] for s in subs]
    tbl.y = select(h_out, "Y")[0]
    tbl.pitch = pitch
    tbl.cell = lambda r, c: row_mobs[r].cells[c]
    tbl.col = lambda c: VGroup(*[row.cells[c] for row in row_mobs])
    tbl.row_of = lambda letter: [v[0] for v in P150].index(letter)

    def col_box(cols, color=YELLOW):
        xa = min(row_mobs[0].cells[c].get_x() for c in cols) - 0.42
        xb = max(row_mobs[0].cells[c].get_x() for c in cols) + 0.42
        ya = subs[0].get_top()[1] + 0.12
        yb = bottom
        return (Rectangle(width=xb - xa, height=ya - yb).move_to(_p((xa + xb) / 2, (ya + yb) / 2))
                .set_stroke(color, 2).set_fill(color, 0.15).set_z_index(-1))

    def row_box(r, color=YELLOW):
        row = row_mobs[r]
        xa, xb = left + 0.1, right - 0.05
        return (Rectangle(width=xb - xa, height=pitch * 0.92).move_to(_p((xa + xb) / 2, row.cells[0].get_y()))
                .set_stroke(color, 2).set_fill(color, 0.18).set_z_index(-1))

    tbl.col_box, tbl.row_box = col_box, row_box
    return tbl


# ------------------------------------------------------------------ shared: grids of pair cells
def _pair_grid(cols, rows, keep, side, x0, y0, size=32):
    """Cells for (col, row) with keep(col, row); x0/y0 = left/top edge of the first column/row."""
    squares, cells, pairs = VGroup(), {}, []
    for ci, cl in enumerate(cols):
        for ri, rl in enumerate(rows):
            if not keep(cl, rl):
                continue
            sq = (Square(side).set_stroke(FG, 2).set_fill(BG, 0)
                  .move_to(_p(x0 + side * (ci + 0.5), y0 - side * (ri + 0.5))))
            squares.add(sq)
            cells[f"{cl}-{rl}"] = sq
            pairs.append(f"{cl}-{rl}")
    col_letters = {cl: T(cl, size).move_to(_p(x0 + side * (ci + 0.5), y0 - side * len(rows) - 0.36))
                   for ci, cl in enumerate(cols)}
    row_letters = {rl: T(rl, size).move_to(_p(x0 - 0.4, y0 - side * (ri + 0.5)))
                   for ri, rl in enumerate(rows)}
    g = VGroup(squares, VGroup(*col_letters.values()), VGroup(*row_letters.values()))
    g.squares, g.cells, g.pairs, g.side = squares, cells, pairs, side
    g.col_letters, g.row_letters = col_letters, row_letters
    g.cell = lambda c, r: cells[f"{c}-{r}"]
    g.col_letter = lambda c: col_letters[c]
    g.row_letter = lambda r: row_letters[r]
    return g


def implication_table():
    return _pair_grid(LETTERS[:7], LETTERS[1:], lambda c, r: c < r, 0.9, 0.1, 3.3)


def grid8():
    return _pair_grid(LETTERS, LETTERS, lambda c, r: True, 0.72, 0.0, 2.95)


def cell_label(it, col, row, size=28, color=FG):
    return T(f"{col}-{row}", size, color).move_to(it.cell(col, row).get_center())


def handover_shot():
    return VGroup(p150_table(), implication_table())


def _pulse(mob, color=YELLOW, base=FG):
    def f(m, a):
        m.set_color(interpolate_color(ManimColor(base), ManimColor(color), np.sin(PI * a)))
    return UpdateFromAlphaFunc(mob, f)


def _fill_pulse(sq, color=GOLD, peak=0.55):
    def f(m, a):
        m.set_fill(color, peak * np.sin(PI * a))
    return UpdateFromAlphaFunc(sq, f)


class Layout(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        # back to the bare drawing s6 opens on
        self.play(*disappear(self.title2, self.lab), self.it.cell("A", "B").animate.set_stroke(FG, 2),
                  self.it.col_letter("A").animate.set_color(FG), run_time=1.0)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    # ------------------------------------------------------------ c1: the 8 x 8 grid
    def clip1(self):
        with self.say("c2.grid.1") as c:
            title = T("Determination of State Equivalence using an Implication Table", 30).move_to(_p(0, 3.3))
            tbl = p150_table()
            self.title, self.tbl = title, tbl
            self.play(*appear(title, shift=None), run_time=1.0)  # early: the slide's title
            self.play(*appear(tbl.head, tbl.rules, tbl.seps, *tbl.rows, shift=None, lag=0.08),  # early: table returns whole
                      run_time=min(1.5, c.until("grid")))
            settle(self, tbl)
            c.wait_until("grid")

            g = grid8()
            self.g = g
            self.play(*appear(*g.squares, shift=None, lag=0.03), run_time=min(1.8, c.until("along the bottom")))
            c.wait_until("along the bottom")
            self.play(*appear(*g.col_letters.values(), shift=0.15 * DOWN, lag=0.2),
                      run_time=min(1.3, c.until("down the side")))
            c.wait_until("down the side")
            self.play(*appear(*g.row_letters.values(), shift=0.15 * RIGHT, lag=0.2),
                      run_time=min(1.3, c.until("cell")))
            c.wait_until("cell")

            self.lab_ab = cell_label(g, "A", "B", color=YELLOW)
            self.boxes = [tbl.row_box(tbl.row_of("A")), tbl.row_box(tbl.row_of("B"))]
            self.play(g.cell("A", "B").animate.set_stroke(YELLOW, 4), *appear(self.lab_ab, shift=None),
                      *[FadeIn(b) for b in self.boxes], run_time=1.2)
            c.wait_until("state of its column")
            self.play(g.col_letter("A").animate.set_color(YELLOW), run_time=0.8)
            c.wait_until("of its row")
            self.play(g.row_letter("B").animate.set_color(YELLOW), run_time=0.8)
            c.wait_until()

    # ------------------------------------------------------------ c2: drop the mirror half and the diagonal
    def clip2(self):
        g, tbl = self.g, self.tbl
        with self.say("c2.grid.2") as c:
            lab_ba = cell_label(g, "B", "A", color=YELLOW)
            self.play(g.cell("B", "A").animate.set_stroke(YELLOW, 4), *appear(lab_ba, shift=None), run_time=1.0)
            c.wait_until("is the same as")
            self.play(g.cell("A", "B").animate.set_stroke(GOLD, 4).set_fill(GOLD, 0.3),
                      g.cell("B", "A").animate.set_stroke(GOLD, 4).set_fill(GOLD, 0.3),
                      self.lab_ab.animate.set_color(GOLD), lab_ba.animate.set_color(GOLD),
                      g.col_letter("A").animate.set_color(FG), g.row_letter("B").animate.set_color(FG),
                      run_time=1.2)
            c.wait_until("every cell above")

            upper = [g.cell(a, b) for a in LETTERS for b in LETTERS if a > b]
            lower = [g.cell(a, b) for a in LETTERS for b in LETTERS if a < b]
            self.play(*[s.animate.set_stroke(GOLD, 3).set_fill(GOLD, 0.3) for s in upper + lower
                        if s not in (g.cell("A", "B"), g.cell("B", "A"))],
                      run_time=min(1.6, c.until("we drop them")))
            c.wait_until("we drop them")
            self.play(*[FadeOut(s) for s in upper], *disappear(lab_ba, self.lab_ab),
                      *[s.animate.set_stroke(FG, 2).set_fill(BG, 0) for s in lower],
                      *[FadeOut(b) for b in self.boxes], run_time=min(1.5, c.until("diag")))
            c.wait_until("diag")

            diag = [g.cell(a, a) for a in LETTERS]
            dlabs = [cell_label(g, a, a) for a in LETTERS]
            self.play(*appear(*dlabs, shift=None, lag=0.1), run_time=min(1.0, c.until("tells us nothing")))
            c.wait_until("tells us nothing")
            self.play(*[s.animate.set_stroke(DIM, 2) for s in diag], *[l.animate.set_color(DIM) for l in dlabs],
                      run_time=1.0)
            c.wait_until("empty")

            s = g.side
            rowA = (Rectangle(width=8 * s, height=s).move_to(_p(4 * s, 2.95 - s / 2))
                    .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12))
            colH = (Rectangle(width=s, height=8 * s).move_to(_p(7.5 * s, 2.95 - 4 * s))
                    .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12))
            self.play(*during([FadeOut(s) for s in diag] + disappear(*dlabs), 0, 0.5),
                      *during([FadeIn(rowA), FadeIn(colH), g.row_letter("A").animate.set_color(YELLOW),
                               g.col_letter("H").animate.set_color(YELLOW)], 0.4, 1), run_time=1.6)
            c.wait_until("so they go as well")
            self.play(FadeOut(rowA), FadeOut(colH), *disappear(g.row_letter("A"), g.col_letter("H")),
                      run_time=min(1.0, max(0.5, c.remaining)))
            c.wait_until()

    # ------------------------------------------------------------ c3: the staircase, 28 cells
    def clip3(self):
        g, tbl = self.g, self.tbl
        with self.say("c2.grid.3") as c:
            it = implication_table()
            self.it = it
            title2 = T("Example – Implication Table", 30).move_to(_p(tbl.get_center()[0], 3.3))
            self.title2 = title2
            moves = [ReplacementTransform(g.cell(*p.split("-")), it.cell(*p.split("-"))) for p in it.pairs]
            moves += [ReplacementTransform(g.col_letter(l), it.col_letter(l)) for l in LETTERS[:7]]
            moves += [ReplacementTransform(g.row_letter(l), it.row_letter(l)) for l in LETTERS[1:]]
            self.play(*moves, *swap(self.title, title2), run_time=min(2.0, c.until("its rows")))
            settle(self, it)
            c.wait_until("its rows")

            rl = [it.row_letter(l) for l in LETTERS[1:]]
            self.play(*[time_span(_pulse(m), 0.2 * i, 0.2 * i + 0.6) for i, m in enumerate(rl)], run_time=1.8)
            c.wait_until("its columns")
            cl = [it.col_letter(l) for l in LETTERS[:7]]
            self.play(*[time_span(_pulse(m), 0.2 * i, 0.2 * i + 0.6) for i, m in enumerate(cl)], run_time=1.8)
            c.wait_until("count")

            step, span = 0.08, 0.45
            self.play(*[time_span(_fill_pulse(it.cell(*p.split("-"))), step * i, step * i + span)
                        for i, p in enumerate(it.pairs)], run_time=step * 27 + span)
            n28 = T("28", 60, GOLD).move_to(_p(4.4, 2.6))
            self.play(*appear(n28, shift=None), run_time=min(0.9, c.until("eight times seven")))
            c.wait_until("eight times seven")
            calc = MathTex(r"8 \times 7", r"\div 2", font_size=48).next_to(n28, DOWN, buff=0.35)
            self.play(*appear(calc[0], shift=None), run_time=1.0)
            c.wait_until("half")
            self.play(*appear(calc[1], shift=None), run_time=1.0)
            c.wait_until("corner")

            lab = cell_label(it, "A", "B", size=30, color=YELLOW)
            self.lab = lab
            self.play(it.cell("A", "B").animate.set_stroke(YELLOW, 4), *appear(lab, shift=None), run_time=1.2)
            c.wait_until("we name each cell")
            self.play(*disappear(n28, calc), run_time=0.8)
            c.wait_until("column's letter first")
            self.play(*flash([lab[0], it.col_letter("A")], color=YELLOW, time_width=1.5),
                      it.col_letter("A").animate.set_color(YELLOW), run_time=min(1.4, max(0.5, c.remaining)))
            c.wait_until()
