"""Chapter 2, scene 6: crosses from the outputs; 16 cells crossed, 12 left open. Clips c2.cross.1 - c2.cross.3.

Opens on ch2_s5_layout's handover_shot() (p. 150's table + the empty staircase).
Shared drawings (import with load_scene("ch2_s6_outputs")):
- `cell_cross(cell)`: two RED diagonals corner to corner across the whole cell (VGroup of 2 Lines).
- `output_dots(it)`: GREEN dots 0.3 left of the row letters C, E, F, H and column letters C, E, F;
  `.rows` / `.cols` dicts {letter: Dot}.
- `CROSSED`: the 16 output-crossed pairs ("A-C", ...); `OPEN12`: the 12 open pairs.
- `handover_shot()`: table + staircase + dots + the 16 crosses (this scene's last frame; s7 opens on it).
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

L5 = load_scene("ch2_s5_layout")
LETTERS = "ABCDEFGH"
ONES = "CEFH"


def _p(x, y):
    return np.array([x, y, 0.0])


def _pairs(it):
    return list(it.pairs)


def _crossed(pair):
    a, b = pair.split("-")
    return (a in ONES) != (b in ONES)


CROSSED = [p for p in L5.implication_table().pairs if _crossed(p)]
OPEN12 = [p for p in L5.implication_table().pairs if not _crossed(p)]


def cell_cross(cell):
    """Two RED diagonals corner to corner across the whole cell."""
    return VGroup(Line(cell.get_corner(UL), cell.get_corner(DR)),
                  Line(cell.get_corner(UR), cell.get_corner(DL))).set_stroke(RED, 5)


def output_dots(it):
    """GREEN dots beside the output-1 states' letters: rows C E F H, columns C E F."""
    rows = {l: Dot(it.row_letter(l).get_center() + 0.3 * LEFT, radius=0.075, color=GREEN)
            for l in ONES}
    cols = {l: Dot(it.col_letter(l).get_center() + 0.3 * LEFT, radius=0.075, color=GREEN)
            for l in ONES if l in it.col_letters}
    g = VGroup(*rows.values(), *cols.values())
    g.rows, g.cols = rows, cols
    return g


def all_crosses(it):
    g = VGroup(*[cell_cross(it.cell(*p.split("-"))) for p in CROSSED])
    g.by = {p: g[i] for i, p in enumerate(CROSSED)}
    return g


def handover_shot():
    tbl, it = L5.p150_table(), L5.implication_table()
    return VGroup(tbl, it, output_dots(it), all_crosses(it))


def _fill_pulse(sq, color=GOLD, peak=0.5):
    def f(m, a):
        m.set_fill(color, peak * np.sin(PI * a) if a < 1 else 0)
    return UpdateFromAlphaFunc(sq, f)


class Outputs(NarratedScene):
    def construct(self):
        shot = L5.handover_shot()
        self.tbl, self.it = shot[0], shot[1]
        self.add(self.tbl, self.it)
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(0.15)

    # ------------------------------------------------------------------ A vs C
    def clip1(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.cross.1") as c:
            boxes = [tbl.row_box(0), tbl.row_box(2)]
            ac = it.cell("A", "C")
            ac.set_z_index(1)
            self.play(*[FadeIn(b) for b in boxes], ac.animate.set_stroke(YELLOW, 5),
                      run_time=min(1.2, c.until("outs")))
            c.wait_until("outs")

            y0, y1 = tbl.cell(0, 3), tbl.cell(2, 3)
            z = T("0", 60).move_to(_p(3.3, 2.75))
            o = T("1", 60, GREEN, weight=BOLD).move_to(_p(4.7, 2.75))
            ne = MathTex(r"\neq", font_size=64, color=RED).move_to(_p(4.0, 2.75))
            ob = [SurroundingRectangle(m, color=YELLOW, buff=0.12) for m in (y0, y1)]
            self.play(*[FadeIn(b) for b in ob], run_time=0.6)
            self.play(*fly(y0, z, arc=-PI / 3), *fly(y1, o, arc=-PI / 3), run_time=1.6)
            self.play(*appear(ne, shift=None), run_time=0.8)
            c.wait_until("cross")

            self.ac_cross = cell_cross(ac)
            cap = MathTex("A", r"\not\equiv", "C", font_size=56).move_to(_p(4.0, 1.85))
            cap[1].set_color(RED)
            self.play(Create(self.ac_cross[0]), run_time=0.6)
            self.play(Create(self.ac_cross[1]), *appear(cap, shift=None), run_time=0.8)
            c.wait_until("settled")
            self.play(*[FadeOut(b) for b in boxes + ob], ac.animate.set_stroke(FG, 2), run_time=1.0)
            ac.set_z_index(0)
            c.wait_until("no implied pairs")
            self.play(*flash([ac], color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("whatever the next states do")
            nxt = [tbl.cell(r, k) for r in (0, 2) for k in (1, 2)]
            self.play(*flash(nxt, color=BLUE, time_width=1.5), run_time=1.4)
            c.wait_until("the outputs already differ")
            self.play(*flash([VGroup(z, ne, o)], color=RED, time_width=1.5), run_time=1.4)
            self.cmp, self.cap = VGroup(z, ne, o), cap

    # ------------------------------------------------------------------ dots, 16 crosses, 12 open
    def clip2(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.cross.2") as c:
            colb = tbl.col_box([3], GREEN)
            ones = [tbl.cell(tbl.row_of(l), 3) for l in ONES]
            self.play(FadeIn(colb), *flash(ones, color=GREEN, time_width=1.5), run_time=1.2)
            dots = output_dots(it)
            self.dots = dots
            order = [dots.rows[l] for l in ONES] + [dots.cols[l] for l in "CEF"]
            self.play(*[time_span(FadeIn(d, scale=0.3), 0.15 * i, 0.15 * i + 0.5) for i, d in enumerate(order)],
                      run_time=1.5)
            c.wait_until("zeros")
            zeros = [tbl.cell(tbl.row_of(l), 3) for l in "ABDG"]
            self.play(FadeOut(colb), *flash(zeros, color=FG, time_width=1.5), run_time=1.4)
            c.wait_until("all")

            sqs = [it.cell(*p.split("-")) for p in CROSSED]
            self.play(*[sq.animate.set_fill(RED, 0.22) for sq in sqs], run_time=1.2)
            c.wait_until("sixteen")

            fxf = MathTex(r"4 \times 4", font_size=48).move_to(_p(4.0, 1.95))
            self.play(*disappear(self.cmp, self.cap), run_time=0.8)
            self.play(*appear(fxf, shift=None), run_time=0.8)
            crosses = all_crosses(it)
            self.crosses = crosses
            rest = [p for p in CROSSED if p != "A-C"]
            n16 = T("16", 72, GOLD).move_to(_p(4.0, 2.85))
            step, span = 0.09, 0.5
            self.play(*[time_span(Create(crosses.by[p]), step * i, step * i + span) for i, p in enumerate(rest)],
                      *[time_span(sq.animate.set_fill(BG, 0), 0.6, 1.9) for sq in sqs],
                      time_span(FadeIn(n16), 0.4, 1.2),
                      run_time=step * len(rest) + span)
            # the A-C cross drawn in clip 1 is identical: keep one copy
            self.remove(self.ac_cross)
            self.add(crosses.by["A-C"])
            c.wait_until("lecturer")

            note = VGroup(T("the lecturer:", 28, DIM), T("column by column,", 28, DIM), T("the same 16", 28, DIM))
            note.arrange(DOWN, buff=0.14, aligned_edge=RIGHT).move_to(_p(5.0, 0.85))
            note.align_to(_p(6.5, 0), RIGHT)
            self.play(*appear(note, shift=None), run_time=1.0)  # early: one note, read as the sentence goes on
            c.wait_until("twelve")

            opens = [it.cell(*p.split("-")) for p in OPEN12]
            n12 = T("12", 72, GOLD).move_to(fxf.get_center())
            self.play(*[sq.animate.set_stroke(GOLD, 4) for sq in opens], *swap(fxf, n12), run_time=1.4)
            c.wait_until("six among the zeros")
            zz = [it.cell(*p.split("-")) for p in OPEN12 if p[0] not in ONES]
            self.play(*[_fill_pulse(s) for s in zz], run_time=1.2)
            c.wait_until("six among the ones")
            oo = [it.cell(*p.split("-")) for p in OPEN12 if p[0] in ONES]
            self.play(*[_fill_pulse(s) for s in oo], run_time=1.2)
            self.n16, self.n12, self.opens, self.note = n16, n12, opens, note

    # ------------------------------------------------------------------ what the cross means
    def clip3(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.cross.3") as c:
            ac = it.cell("A", "C")
            ac_x = self.crosses.by["A-C"]
            dim_these = ([s for s in it.squares if s is not ac] + list(it.col_letters.values())
                         + list(it.row_letters.values()) + list(self.dots)
                         + [x for p, x in self.crosses.by.items() if p != "A-C"])
            self.play(*disappear(self.n16, self.n12, self.note),
                      *[sq.animate.set_stroke(FG, 2) for sq in self.opens], run_time=0.8)
            self.play(*set_alpha(dim_these, DIMMED), run_time=1.0)
            c.wait_until("placing an ex")
            q = VGroup(T("“we place an X", 32, slant=ITALIC), T("in this cell”", 32, slant=ITALIC))
            q.arrange(DOWN, buff=0.16).move_to(_p(4.4, 2.5))
            self.play(*appear(q, shift=None), run_time=1.0)
            c.wait_until("three")

            # the staircase leaves; the panel of three X's takes its place
            y_sym, y_lab = 0.45, -1.35
            bigx = T("X", 110, BLUE).move_to(_p(0.0, y_sym))
            self.play(*disappear(*[m for m in self.mobjects_except_table() if m is not q], lag=0.03), run_time=1.0)
            self.play(*flash(tbl.xs, color=BLUE, time_width=1.5), *appear(bigx, shift=None), run_time=1.4)
            c.wait_until("input")
            lab1 = T("input", 30, BLUE).move_to(_p(0.0, y_lab))
            self.play(*appear(lab1), run_time=0.8)
            c.wait_until("don't cares")
            km = self.small_kmap(_p(2.6, y_sym - 0.1))
            lab2 = T("don't care", 30, YELLOW).move_to(_p(2.45, y_lab))
            self.play(*appear(km, shift=None), *appear(lab2), run_time=1.2)
            c.wait_until("draw")

            sq3 = Square(1.5).set_stroke(FG, 2).move_to(_p(5.25, y_sym))
            x3 = cell_cross(sq3)
            lab3 = T("not equivalent", 30, RED).move_to(_p(5.25, y_lab))
            self.play(FadeIn(sq3), run_time=0.5)
            self.play(Create(x3[0]), Create(x3[1]), *appear(lab3), run_time=1.2)  # early: the panel's third label, read at "not equivalent"
            c.wait_until("one thing")
            self.play(*flash([sq3], color=RED, time_width=1.5), run_time=1.4)
            c.wait_until("these two states")

            final = handover_shot()
            it2, dots2, crosses2 = final[1], final[2], final[3]
            ac2 = crosses2[CROSSED.index("A-C")]
            back = [m for m in crosses2 if m is not ac2]
            self.play(*during(disappear(bigx, lab1, km, lab2, lab3, sq3, q), 0, 0.4),
                      *during([FadeIn(it2), FadeIn(dots2), *[FadeIn(m) for m in back]], 0.4, 1.0),
                      *during([Transform(x3, ac2.copy())], 0.25, 0.9),
                      run_time=min(1.8, c.remaining))
            self.remove(x3)
            self.add(it2, dots2, crosses2)
            assert tbl in self.mobjects
            c.wait_until()

    def mobjects_except_table(self):
        keep = set(id(m) for m in self.tbl.get_family())
        return [m for m in self.mobjects if id(m) not in keep]

    def small_kmap(self, center):
        """A 2 x 2 K-map in L6's kmap() style: BLUE grid, FG headings, entries 1 FG / 0 DIM, X YELLOW."""
        cell = 0.85
        L, R = center[0] - cell, center[0] + cell
        top, bot = center[1] + cell, center[1] - cell
        grid = VGroup(Rectangle(width=2 * cell, height=2 * cell).move_to(center),
                      Line(_p(center[0], top), _p(center[0], bot)),
                      Line(_p(L, center[1]), _p(R, center[1]))).set_stroke(BLUE, 3)
        heads = VGroup(*[MathTex(str(k), font_size=40, color=FG).move_to(_p(L + (k + 0.5) * cell, top + 0.3))
                         for k in (0, 1)],
                       *[MathTex(str(r), font_size=40, color=FG).move_to(_p(L - 0.3, top - (r + 0.5) * cell))
                         for r in (0, 1)])
        vals = [["1", "X"], ["0", "1"]]
        ents = VGroup()
        for r in (0, 1):
            for k in (0, 1):
                v = vals[r][k]
                col = YELLOW if v == "X" else (FG if v == "1" else DIM)
                ents.add(MathTex(v, font_size=52, color=col).move_to(_p(L + (k + 0.5) * cell, top - (r + 0.5) * cell)))
        return VGroup(grid, heads, ents)
