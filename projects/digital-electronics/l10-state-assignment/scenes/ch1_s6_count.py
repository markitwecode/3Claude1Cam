"""Chapter 1, scene 6: counting in binary: the sequential assignment, its transition table, Output = b. Clips c1.count.1 – c1.count.4.

Shared (imported by s7 and the s8 recap):
  count_table(boxed=False, d_row=False)
      the sequential assignment's state transition table (p. 134) in L6 mod_table() styling:
      titles "Current state" / "Next state" (T 30), headers c b a | c' b' a' (GREEN MathTex 42),
      FG MathTex 40 cells, DIM stroke-2 rules. Canonical: centred on ORIGIN, about 5.5 wide x 5.3
      tall (titles y 2.3, headers 1.6, D row 1.02, rule 0.6, rows 0.1 - 0.6 i, i = 0..4).
      boxed: GREEN box round the current-state b column (header + cells), its cells GREEN.
      d_row: BLUE MathTex row D_c D_b D_a (38) under the next-state headers.
      The box and the D row are always built (.bbox, .drow); the flags only put them in the group.
      Attrs .titles[g] .heads[g] (VGroup of 3) .lines .cur[i] .nxt[i] (VGroup of 3 cells, c first)
      .rows[i] = VGroup(cur[i], nxt[i]) .bbox .drow .col(g, j) -> VGroup of column j of group g.
  handover_shot()  = count_table(boxed=True, d_row=True) scaled 0.8 with its left edge at x -6.6,
      vertically centred (this scene's last frame; s7 opens on it, centre left free for the K-map).
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


# ---- the shared transition table ------------------------------------------------------------------
CT_GX = (-1.55, 1.55)          # group centres (current, next)
CT_DX = 0.72                   # column pitch inside a group
CT_TITLE_Y, CT_HEAD_Y, CT_D_Y, CT_RULE_Y = 2.3, 1.6, 1.02, 0.6
CT_ROW0_Y, CT_PITCH = 0.1, 0.6
CT_TOP, CT_BOT, CT_HALF_W = 2.65, -2.65, 2.75
SEQ = [0, 1, 2, 3, 4]


def ct_row_y(i):
    return CT_ROW0_Y - i * CT_PITCH


def count_table(boxed=False, d_row=False):
    """See the module docstring."""
    titles = VGroup(*[T(s, 30).move_to(_p(gx, CT_TITLE_Y))
                      for s, gx in zip(("Current state", "Next state"), CT_GX)])
    heads = VGroup(*[VGroup(*[MathTex(t, font_size=42, color=GREEN).move_to(_p(gx + (j - 1) * CT_DX, CT_HEAD_Y))
                              for j, t in enumerate(ts)])
                     for ts, gx in zip((["c", "b", "a"], ["c'", "b'", "a'"]), CT_GX)])
    lines = VGroup(Line(_p(0, CT_TOP), _p(0, CT_BOT)).set_stroke(DIM, 2),
                   Line(_p(-CT_HALF_W, CT_RULE_Y), _p(CT_HALF_W, CT_RULE_Y)).set_stroke(DIM, 2))

    def bits_row(v, gx, i):
        return VGroup(*[MathTex(b, font_size=40).move_to(_p(gx + (j - 1) * CT_DX, ct_row_y(i)))
                        for j, b in enumerate(format(v, "03b"))])
    cur = VGroup(*[bits_row(s, CT_GX[0], i) for i, s in enumerate(SEQ)])
    nxt = VGroup(*[bits_row((s + 1) % 5, CT_GX[1], i) for i, s in enumerate(SEQ)])
    rows = [VGroup(cur[i], nxt[i]) for i in range(5)]
    drow = VGroup(*[MathTex(t, font_size=38, color=BLUE).move_to(_p(CT_GX[1] + (j - 1) * CT_DX, CT_D_Y))
                    for j, t in enumerate(("D_c", "D_b", "D_a"))])
    bx = CT_GX[0]
    bbox = Rectangle(width=0.62, height=(CT_HEAD_Y + 0.34) - (ct_row_y(4) - 0.3))
    bbox.move_to(_p(bx, ((CT_HEAD_Y + 0.34) + (ct_row_y(4) - 0.3)) / 2))
    bbox.set_stroke(GREEN, 3.5).set_fill(GREEN, 0.1).set_z_index(-1)
    g = VGroup(titles, heads, lines, cur, nxt)
    if boxed:
        for row in cur:
            row[1].set_color(GREEN)
        g.add(bbox)
    if d_row:
        g.add(drow)
    g.titles, g.heads, g.lines, g.cur, g.nxt, g.rows = titles, heads, lines, cur, nxt, rows
    g.bbox, g.drow = bbox, drow
    groups = [cur, nxt]
    g.col = lambda gi, j: VGroup(*[row[j] for row in groups[gi]])
    return g


# layouts: (scale about ORIGIN, then shift) from the canonical table
L2 = (1.1, _p(3.0, -0.1))     # clip 2: centre right, ring upper left
L3 = (0.95, _p(-4.0, 0.0))     # clips 3-4: left half
LH = (0.8, _p(-6.6 + 0.8 * CT_HALF_W, 0.0))   # handover: left edge at -6.6


def at_layout(m, lay):
    k, v = lay
    return m.scale(k, about_point=ORIGIN).shift(v)


def relayout(m, a, b):
    """m.animate taking a mobject placed at layout a to layout b."""
    r = b[0] / a[0]
    return m.animate.scale(r, about_point=ORIGIN).shift(b[1] - r * a[1])


def handover_shot():
    """The last frame: the boxed table with its D row, shrunk to the left edge."""
    return at_layout(count_table(boxed=True, d_row=True), LH)


# ---- scene ------------------------------------------------------------------------------------------
BITS = ["000", "001", "010", "011", "100"]
RING_K = 1.25                  # the ring grows to this in clip 1
RING_K2, RING_C2 = 0.95, _p(-4.2, 0.3)   # clip 2: shrunk to the upper left
RIGHT_X = 2.85                 # centre of the right-hand column in clips 3-4


class Count(NarratedScene):
    def construct(self):
        self.s5 = load_scene("ch1_s5_divide5")
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.ending()

    # -- c1.count.1: number the ring, code it, name it -----------------------------------------------
    def clip1(self):
        ring = self.s5.handover_shot()
        self.add(ring)
        big = self.s5.state_ring(codes=BITS).scale(RING_K, about_point=ORIGIN)
        with self.say("c1.count.1") as c:
            self.play(ring.animate.scale(RING_K, about_point=ORIGIN), run_time=1.5)
            c.wait_until("numbers")
            self.play(LaggedStart(*flash(ring.nums, color=GOLD), lag_ratio=0.25), run_time=2.0)
            cues = [("zero zero zero", 0), ("zero zero one", 0), ("zero one zero", 1),
                    ("one one", 0), ("and one", 0)]
            new_codes = []
            for i, (cue, nth) in enumerate(cues):
                c.wait_until(cue, nth=nth)
                nxt = cues[i + 1] if i < 4 else ("wrap", 0)
                rt = min(1.2 if i == 0 else 0.9, max(0.5, 0.9 * c.until(nxt[0], nth=nxt[1])))
                self.play(*swap(ring.codes[i], big.codes[i]), run_time=rt)
                new_codes.append(big.codes[i])
            # settle the ring with its new codes as one object
            self.remove(ring, *new_codes)
            ring = VGroup(ring[0], ring[1], VGroup(*new_codes))
            ring.arrows = list(ring[0])
            self.add(ring)
            c.wait_until("wrap")
            wrap = ring.arrows[4]
            path = Line(wrap.get_start(), wrap.get_end()).set_stroke(YELLOW, 7)
            self.play(wrap.animate.set_color(YELLOW), VShowPassingFlash(path, time_width=0.6),
                      run_time=1.4)
            heading = T("Sequential State Assignment", 48, YELLOW).move_to(_p(0, 3.35))
            c.wait_until(own_word=heading, cue="name")
            self.play(*appear(heading), run_time=1.0)
            quote = T("“Here we simply assign the states in an increasing natural binary count”",
                      28, slant=ITALIC).move_to(_p(0, -3.3))
            self.play(*appear(quote, shift=None), run_time=min(1.0, c.until(floor=0.5)))
        self.ring, self.heading, self.quote = ring, heading, quote

    # -- c1.count.2: the transition table -------------------------------------------------------------
    def clip2(self):
        ring = self.ring
        tab = at_layout(count_table(), L2)
        self.tab = tab
        with self.say("c1.count.2") as c:
            r = RING_K2 / RING_K
            self.play(ring.animate.scale(r, about_point=ORIGIN).shift(RING_C2),
                      time_span(Create(tab.lines[0]), 0.8, 1.6), time_span(Create(tab.lines[1]), 0.9, 1.7),
                      run_time=1.8)
            for g, cue in ((0, "current"), (1, "next")):
                c.wait_until(own_word=tab.titles[g], cue=cue)
                self.play(*appear(tab.titles[g], *tab.heads[g], lag=0.15), run_time=1.0)
                self.play(FlashAround(VGroup(tab.titles[g], tab.heads[g]).copy(), color=YELLOW,
                                      time_width=1.5), run_time=1.4)
            # row 1: current, then arrow + next
            def arrow_at(i):
                y = tab.cur[i].get_y()
                return Arrow(_p(tab.cur[i].get_right()[0] + 0.12, y), _p(tab.nxt[i].get_left()[0] - 0.12, y),
                             buff=0, color=YELLOW, stroke_width=4, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.3)
            c.wait_until("row1")
            self.play(*appear(tab.cur[0], shift=None), run_time=1.0)
            arr = arrow_at(0)
            c.wait_until("the next state is")
            self.play(GrowArrow(arr), *during(appear(tab.nxt[0], shift=None), 0.4, 1.0), run_time=1.3)
            c.wait_until("row2")
            self.play(Transform(arr, arrow_at(1)), *appear(tab.cur[1], shift=None), run_time=1.0)
            c.wait_until("it's")
            self.play(*appear(tab.nxt[1], shift=None), *disappear(self.quote), run_time=0.8)
            c.wait_until("rest")
            self.play(*disappear(arr), *during(appear(*tab.rows[2:5], shift=None, lag=0.3), 0.2, 1.0),
                      run_time=1.6)
            c.wait_until("goes back")
            self.play(*recolor(list(tab.cur[4]) + list(tab.nxt[4]), YELLOW),
                      *flash([tab.rows[4]], color=YELLOW, time_width=1.5), run_time=1.4)
            settle(self, tab)

    # -- c1.count.3: unused states; read down b ---------------------------------------------------------
    def clip3(self):
        tab, ring = self.tab, self.ring
        unused = T("Unused states, 101, 110 and 111.", 30, DIM).move_to(_p(L2[1][0], -3.32))
        with self.say("c1.count.3") as c:
            self.play(*appear(unused), *recolor(list(tab.cur[4]) + list(tab.nxt[4]), FG), run_time=1.0)  # early: p. 134's line, read as the voice lists the three patterns
            c.wait_until("output")
            self.play(*during(disappear(ring, self.heading), 0, 0.4),
                      *during(disappear(unused), 0.5, 1.0),
                      *during([relayout(tab, L2, L3)], 0.4, 1.0),
                      run_time=1.8)
            wave = self.s5.divide5_wave(width=5.4, height=0.6, periods=10, gap=1.3, label_size=32,
                                        pattern=(0, 0, 1, 1, 0))
            wave.shift(_p(3.8, 2.0))
            self.wave = wave
            self.play(*appear(wave, shift=None), run_time=min(1.0, c.until("column", floor=0.5)))
            # the b column: spotlight and box it
            full = at_layout(count_table(boxed=True, d_row=True), L3)
            box = full.bbox
            col_b = list(tab.col(0, 1))
            others = ([tab.titles[1], tab.heads[0][0], tab.heads[0][2], *tab.heads[1], *tab.lines]
                      + [row[j] for row in tab.cur for j in (0, 2)] + [m for row in tab.nxt for m in row])
            self.others = others
            c.wait_until("column")
            self.play(GrowFromCenter(box), *set_alpha(others, DIMMED), run_time=1.2)
            settle(self, tab, add=[box])
            self.box = box
            # one GREEN highlight slides down the column, landing on each spoken bit
            cues = [("zero zero", 0), ("zero one one zero", 0), ("one one zero", 1), ("one zero", 2), ("zero", 4)]
            cell_w = 0.5 * L3[0]

            def hl_at(cell):
                return (Rectangle(width=cell_w, height=0.5 * L3[0]).move_to(cell)
                        .set_stroke(GREEN, 2.5).set_fill(GREEN, 0.3).set_z_index(-1))
            hl = None
            for k, (cell, (cue, nth)) in enumerate(zip(col_b, cues)):
                c.wait_until(cue, nth=nth)
                rt = 0.4
                if hl is None:
                    hl = hl_at(cell)
                    self.play(GrowFromCenter(hl), cell.animate.set_color(GREEN), run_time=rt)
                else:
                    self.play(Transform(hl, hl_at(cell)), cell.animate.set_color(GREEN), run_time=rt)
            # the five bits come out of the column and line up under the Output wave, one per period,
            # then repeat: the column flashes cell by cell as each bit lands in its slot
            rx, per = wave.rise_x, wave.period
            slot_y = wave.out_y + 2.0 - 0.3 - 0.45
            slots = [_p(rx[k] + 3.8 + per / 2, slot_y) for k in range(10)]
            bits = [MathTex(format(s, "03b")[1], font_size=40 * L3[0], color=GREEN).move_to(slots[k])
                    for k, s in enumerate(SEQ * 2)]
            self.bits = bits
            c.wait_until("twothree")
            anims = list(during(disappear(hl), 0, 0.15))
            for k in range(5):
                a0 = 0.1 + 0.15 * k
                anims += during([FlashAround(col_b[k], color=GREEN, time_width=1.0)], a0, a0 + 0.3)
                anims += during(appear(bits[k], shift=None), a0 + 0.05, a0 + 0.3)
            self.play(*anims, run_time=2.4)
            self.remove(hl)
            self.play(*appear(*bits[5:], shift=None, lag=0.2), run_time=min(1.2, c.until(floor=0.5)))

    # -- c1.count.4: Output = b; the D inputs; the job ------------------------------------------------
    def clip4(self):
        tab = self.tab
        said = T("“The required output is from FF b”", 30, slant=ITALIC).move_to(_p(RIGHT_X, -0.55))
        out_eq = T("Output = b", 44, GREEN).move_to(_p(RIGHT_X, -1.4))
        none = T("output logic: none", 30, DIM).move_to(_p(RIGHT_X, -2.2))
        fluke = T("“that’s just a fluke”", 38, YELLOW, slant=ITALIC).move_to(_p(RIGHT_X, -3.15))
        with self.say("c1.count.4") as c:
            self.play(*appear(said), *set_alpha(self.others, 1), run_time=1.0)
            c.wait_until(own_word=out_eq, cue="simply")
            self.play(*appear(out_eq), FlashAround(self.box, color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until(own_word=none, cue="no output logic")
            self.play(*appear(none), run_time=1.0)
            c.wait_until("fluke")
            self.play(*appear(fluke), run_time=1.0)
            # dee flip-flops: s2's recipe chip, small, top right
            row = load_scene("ch1_s2_machines").recipe_row(with_dee=True, size=30)
            chip = VGroup(row.chips[2], row.tie, row.dee)
            chip.scale(0.9).move_to(_p(RIGHT_X, 1.85))
            c.wait_until("dee")
            self.play(*during(disappear(self.wave, *self.bits), 0, 0.45),
                      *during(appear(chip, shift=None), 0.5, 1.0), run_time=1.2)
            # the next-state header gains the D row
            drow = at_layout(count_table(boxed=True, d_row=True), L3).drow
            c.wait_until("inputs")
            ncols = [VGroup(tab.heads[1][j], *tab.col(1, j)).copy() for j in range(3)]
            self.play(*appear(*drow, lag=0.2), *flash(ncols, color=BLUE, time_width=1.5),
                      FlashAround(row.dee, color=YELLOW, time_width=1.5), run_time=1.4)
            settle(self, tab, add=[drow])
            # the job: three functions of the current state
            jobs = VGroup(*[MathTex(s, font_size=54, color=BLUE)
                            for s in ("D_a = \\, ?", "D_b = \\, ?", "D_c = \\, ?")])
            jobs.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(_p(RIGHT_X, -1.0))
            self.jobs, self.chip = jobs, chip
            c.wait_until("job")
            self.play(*during(disappear(said, out_eq, none, fluke), 0, 0.45),
                      *during(appear(*jobs, lag=0.3), 0.5, 1.0), run_time=1.8)

    # -- handover: the table alone, shrunk to the left edge --------------------------------------------
    def ending(self):
        self.wait(3.3)
        self.play(*during(disappear(self.jobs, self.chip), 0, 0.45),
                  *during([relayout(self.tab, L3, LH)], 0.3, 1.0), run_time=1.6)
        self.wait(1.0)
