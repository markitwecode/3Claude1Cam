"""Chapter 2, scene 1: hook: row matching finds nothing on p. 150's machine, yet A and D behave alike.
Clips c2.hook.1 – c2.hook.2.

Shared drawing (import with load_scene("ch2_s1_hook")), at its home (right half of the frame):
- `two_lanes()`: the two-lane run, A and D on inputs 0 1 1 0. `.xlabel` (BLUE "X"), `.inputs[i]`
  (BLUE digits along the top), `.labels[l]` ("start in A" / "start in D"), `.circles[l][k]` (k = 0..4,
  `.circle .letter`), `.arrows[l][i]`, `.arrow_labels[l][i]` (i = 0..3), `.outs[l][k]` (0 FG, 1 bright
  GREEN), `.out_rows[l]` (VGroup of the five outputs), `.out_boxes[l]` (GOLD), `.eq` (GOLD "=" between
  the output rows), `.step(i)` (VGroup: what step i adds in both lanes: arrows, labels, next circles).
  Lane 0 = start in A (A D E A D), lane 1 = start in D (D A C D A); lane 1 is mirrored, so the two
  output rows face each other with the "=" between them.
- `handover_shot()`: p. 150's table alone at its home (s2 opens on it).
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
from lib.titles import title_card  # noqa: E402

S3 = load_scene("ch1_s3_mealy")
S5 = load_scene("ch1_s5_hi")
L5 = load_scene("ch2_s5_layout")
R8 = load_scene("ch1_s8_recap")


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ shared: the two-lane run
INPUTS = "0110"
LANES = (("A", "D", "E", "A", "D"), ("D", "A", "C", "D", "A"))
OUT = {"A": "0", "B": "0", "C": "1", "D": "0", "E": "1", "F": "1", "G": "0", "H": "1"}
COL_X = [0.6 + 1.4 * k for k in range(5)]
LANE_Y = (1.5, -1.0)          # circle centres
OUT_Y = (0.75, -0.25)         # output rows (lane 1 mirrored: outputs above its circles)
ALAB_DY = (0.33, -0.36)       # arrow labels above lane 0's arrows, below lane 1's
LABEL_Y = (2.5, -1.95)
TOP_Y = 3.25
R_CIRC = 0.32


def _circle(name, center):
    c = Circle(radius=R_CIRC).set_stroke(FG, 3).set_fill(BG, 0).move_to(center)
    t = T(name, 30).move_to(center)
    g = VGroup(c, t)
    g.circle, g.letter = c, t
    return g


def two_lanes():
    g = VGroup()
    xlabel = T("X", 34, BLUE).move_to(_p(0.2, TOP_Y))
    inputs = [T(d, 36, BLUE).move_to(_p((COL_X[i] + COL_X[i + 1]) / 2, TOP_Y)) for i, d in enumerate(INPUTS)]
    labels, circles, arrows, alabs, outs, out_rows, out_boxes = [], [], [], [], [], [], []
    for l, seq in enumerate(LANES):
        lab = T(f"start in {seq[0]}", 30).move_to(_p(0, LABEL_Y[l]), aligned_edge=LEFT)
        lab.align_to(_p(COL_X[0] - R_CIRC, 0, ), LEFT)
        labels.append(lab)
        cs = [_circle(s, _p(COL_X[k], LANE_Y[l])) for k, s in enumerate(seq)]
        circles.append(cs)
        ars, als = [], []
        for i in range(4):
            a = Arrow(cs[i].get_right() + 0.04 * RIGHT, cs[i + 1].get_left() + 0.04 * LEFT, buff=0,
                      stroke_width=3, color=FG, tip_length=0.18, max_tip_length_to_length_ratio=0.3)
            ars.append(a)
            als.append(T(INPUTS[i], 30, BLUE).move_to(a.get_center() + ALAB_DY[l] * UP))
        arrows.append(ars)
        alabs.append(als)
        os_ = []
        for k, s in enumerate(seq):
            v = OUT[s]
            t = T(v, 32, GREEN, weight=BOLD) if v == "1" else T(v, 32)
            os_.append(t.move_to(_p(COL_X[k], OUT_Y[l])))
        outs.append(os_)
        row = VGroup(*os_)
        out_rows.append(row)
        box = (Rectangle(width=COL_X[4] - COL_X[0] + 0.7, height=0.48).move_to(_p((COL_X[0] + COL_X[4]) / 2, OUT_Y[l]))
               .set_stroke(GOLD, 2.5).set_fill(GOLD, 0.15).set_z_index(-1))
        out_boxes.append(box)
    eq = T("=", 44, GOLD).rotate(PI / 2).move_to(_p(COL_X[2], (OUT_Y[0] + OUT_Y[1]) / 2))
    g.add(xlabel, *inputs, *labels)
    for l in range(2):
        g.add(*circles[l], *arrows[l], *alabs[l], *outs[l], out_boxes[l])
    g.add(eq)
    g.xlabel, g.inputs, g.labels, g.circles, g.arrows = xlabel, inputs, labels, circles, arrows
    g.arrow_labels, g.outs, g.out_rows, g.out_boxes, g.eq = alabs, outs, out_rows, out_boxes, eq
    g.step = lambda i: VGroup(*[m for l in range(2) for m in (arrows[l][i], alabs[l][i], circles[l][i + 1])])
    return g


def handover_shot():
    return VGroup(L5.p150_table())


def _span_box(tbl, r0, r1, color=BLUE):
    """A box over table rows r0..r1 (inclusive), as wide as a row box."""
    a, b = tbl.row_box(r0, color), tbl.row_box(r1, color)
    top, bot = a.get_top()[1], b.get_bottom()[1]
    return (Rectangle(width=a.width, height=top - bot).move_to(_p(a.get_x(), (top + bot) / 2))
            .set_stroke(color, 2).set_fill(color, 0.1).set_z_index(-1))


SMALL_ROWS = [("C", "F", "G", "0", "0"), ("D", "H", "H", "0", "0"), ("G", "H", "H", "0", "0")]


class Hook(NarratedScene):
    def construct(self):
        endc = R8.end_card()
        self.add(endc)
        self.wait(0.7)
        self.clip1(endc)
        self.clip2()
        # back to the bare table s2 opens on
        keep = self.tbl
        self.wait(1.2)
        self.play(*disappear(*[m for m in self.mobjects if m is not keep]), run_time=1.0)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    # ------------------------------------------------------------ c1: title, last time, the new table
    def clip1(self, endc):
        with self.say("c2.hook.1") as c:
            card = title_card("Part 2 · When are two states the same?")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            nxt = endc.next
            rest = [m for m in endc if m is not nxt]
            self.play(*during([FadeOut(m) for m in rest], 0, 0.45),
                      *during([nxt.animate.scale(36 / 40).move_to(card.part)], 0.4, 1.0),
                      run_time=1.3)
            self.remove(nxt)
            self.add(card.part)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      FadeIn(card.course, shift=0.25 * DOWN), run_time=1.1)

            # last time: ch1's compact table, rows D and G identical
            c.wait_until("when two rows")
            small = S3.state_table(SMALL_ROWS, top=2.3, x0=-5.4, rules_after=())
            sweep_clear(self, FadeIn(small), run_time=min(1.4, c.until("identical") - 0.2))  # early: the table shown whole
            settle(self, small)
            c.wait_until("identical")
            gd = small.row_box(1, GOLD)
            gg = small.row_box(2, GOLD)
            self.play(FadeIn(gd), FadeIn(gg), *flash([small.rows[1], small.rows[2]], color=GOLD),
                      run_time=min(1.2, c.until("merged")))

            # merged: C's G becomes D, row G leaves
            c.wait_until("merged")
            S5.replace_entry(self, small, 0, 2, "D", run_time=min(1.4, c.until("its row")))
            c.wait_until("its row")
            self.play(*set_alpha([small.rows[2]], DIMMED), *disappear(gg), run_time=0.6)
            S5.delete_row(self, small, "G", run_time=max(0.8, min(1.2, c.until("here's a new machine") - 0.1)))

            # the new machine: p. 150's table, hero, left half
            c.wait_until("here's a new machine")
            tbl = L5.p150_table()
            self.tbl = tbl
            heads = during(appear(tbl.head, tbl.rules, tbl.seps, shift=None), 0.5, 1.0)
            sweep_clear(self, *heads, run_time=1.3)  # early: the table shown whole
            self.play(*appear(*tbl.rows, lag=0.15, shift=None), run_time=min(1.6, c.until("from state A")))
            settle(self, tbl)
            c.wait_until("from state A")
            self.play(FlashAround(tbl.col(0), time_width=1.5), run_time=min(1.8, c.until("one output")))
            c.wait_until("one output")
            self.play(FlashAround(tbl.col(3), color=GREEN, time_width=1.5), run_time=min(1.8, c.until("nomatch")))

            # no match: each row against the rows below it
            c.wait_until("nomatch")
            base = tbl.row_box(0, YELLOW)
            comp = _span_box(tbl, 1, 7)
            self.play(FadeIn(base), FadeIn(comp), run_time=0.8)
            self.wait(0.4)
            for r in range(1, 7):
                self.play(Transform(base, tbl.row_box(r, YELLOW)), Transform(comp, _span_box(tbl, r + 1, 7)),
                          run_time=0.7 if r == 1 else 0.42)
            c.wait_until("no two rows")
            note = T("no two rows identical", 30, DIM).move_to(_p(tbl.get_x(), -3.3))
            self.play(*disappear(base, comp), *during(appear(note), 0.3, 1.0), run_time=1.2)
            self.note = note

    # ------------------------------------------------------------ c2: two copies, A and D
    def clip2(self):
        tbl = self.tbl
        L = two_lanes()
        with self.say("c2.hook.2") as c:
            ra = tbl.row_of("A")
            rd = tbl.row_of("D")
            box = [tbl.row_box(ra, YELLOW), tbl.row_box(rd, YELLOW)]
            self.play(*appear(L.labels[0], L.circles[0][0]), FadeIn(box[0]),
                      run_time=min(1.2, c.until("start a copy")))
            c.wait_until("start a copy")
            self.play(*appear(L.labels[1], L.circles[1][0]), FadeIn(box[1]),
                      run_time=min(1.2, c.until("feed both")))
            c.wait_until("feed both")
            self.play(*appear(L.xlabel, *L.inputs, lag=0.15), run_time=min(1.2, c.until("zero")))  # early: the inputs, read next
            c.wait_until("zero")

            # four steps, both lanes at once; each reads its row's next state
            rt = float(np.clip((c.until("yet") - 2.4) / 4, 0.7, 1.2))
            for i in range(4):
                anims = [FlashAround(L.inputs[i], color=BLUE, time_width=1.5)]
                for l in range(2):
                    nxt = LANES[l][i + 1]
                    anims += [GrowArrow(L.arrows[l][i]),
                              *during(appear(L.arrow_labels[l][i], shift=None), 0.0, 0.6),
                              *during(appear(L.circles[l][i + 1], shift=None), 0.4, 1.0),
                              Transform(box[l], tbl.row_box(tbl.row_of(nxt), YELLOW))]
                self.play(*anims, run_time=rt)

            # differ: a different letter in every column
            c.wait_until("differ")
            span = min(2.6, c.until("yet", floor=1.0))
            fl = []
            for k in range(5):
                a, b = 0.15 * k * span, 0.15 * k * span + 0.4 * span
                fl += [time_span(FlashAround(L.circles[l][k].circle, color=FG, time_width=1.2), a, b)
                       for l in range(2)]
            self.play(*fl, run_time=span)

            # same: the outputs, as they are read
            c.wait_until("outputs")
            nths = (("zero", 2), ("zero", 3), ("one", 2), ("zero", 4), ("zero", 5))
            for k, (w, n) in enumerate(nths):
                c.wait_until(w, nth=n)
                self.play(*appear(L.outs[0][k], L.outs[1][k], shift=None, lag=0), run_time=0.5)
            self.play(FadeIn(L.out_boxes[0]), FadeIn(L.out_boxes[1]),
                      *during(appear(L.eq, shift=None), 0.3, 1.0),
                      run_time=min(1.2, c.until("question")))

            # question
            c.wait_until("question")
            q = T("same outputs, different rows?", 34, YELLOW).move_to(_p(COL_X[2], -2.75))
            self.play(*appear(q), run_time=1.0)
            self.play(*flash([tbl.rows[ra], tbl.rows[rd]], color=YELLOW, time_width=1.5), run_time=1.5)
