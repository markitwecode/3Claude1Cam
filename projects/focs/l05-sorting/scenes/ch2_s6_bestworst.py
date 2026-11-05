"""Chapter 2, scene 6: best and worst inputs for insertion sort. Clips c2.best.1 – c2.best.4.

Plan: two chains stacked as a little table (label column on the left, values from x = -3.1):
sorted [3; 4; 5; 7; 9] on top, reversed [9; 7; 5; 4; 3] below, each with a GOLD tally row of
comparisons and a row for the 10,000-item `rs`. Each chain is sorted in place the way insort
works: the sorted part grows from the right, and each new item lifts 0.4, compares (YELLOW
flash on the item it is compared with, its tally entry ticks up), glides past while that
neighbour slides back under it, then drops into its gap (outline GREEN = sorted part).
Clip 4 clears to the sorted chain (top) and the {range} scale (built by `range_scale()`,
importable for s7's recap icon).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---- layout -------------------------------------------------------------------------------
CH_SCALE = 0.75          # chains: 5 cells + [] -> 8.96 wide, cells 0.75 tall
X0 = -3.1                # left edge of the value column (chains, tallies, rs numbers)
HX = -3.5                # right edge of the label column
LIFT = 0.4               # slide-into-place: lift, glide, drop
TALLY_FS = 48

TOP_Y, TOP_TALLY_Y, TOP_RS_Y = 2.35, 1.3, 0.5
BOT_Y, BOT_TALLY_Y, BOT_RS_Y = -0.9, -2.0, -2.95

# nominal timings of one insert (scaled to the time the narration gives the run)
LIFT_T, CMP_T, PASS_T, DROP_T, HOLD_T = 0.5, 0.8, 1.0, 0.5, 0.2
MULTS = [1.0, 0.62, 0.47, 0.38]      # first insert slow, the rest quicker


def range_scale(width=10.0):
    """The {range} scale: comparisons for 10,000 items, 0 .. 50M across `width`, GOLD line at y=0.
    Ticks: 9,999 sorted (GREEN), 25,146,194 random (FG), 49,995,000 reversed (RED).
    Attributes: .line .ticks .values .names .bigos (O(n) under sorted, O(n^2) under reversed) .caption."""
    g = VGroup()
    g.line = Line(LEFT * width / 2, RIGHT * width / 2, color=GOLD, stroke_width=6)
    g.ticks, g.values, g.names = VGroup(), VGroup(), VGroup()
    for v, txt, name, col in [(9_999, "9,999", "sorted", GREEN),
                              (25_146_194, "25,146,194", "random", FG),
                              (49_995_000, "49,995,000", "reversed", RED)]:
        x = -width / 2 + width * v / 50_000_000
        tick = Line(UP * 0.24, DOWN * 0.24, color=col, stroke_width=6).move_to([x, 0, 0])
        g.ticks.add(tick)
        g.values.add(T(txt, 34, col).next_to(tick, UP, buff=0.2))
        g.names.add(T(name, 30, col).next_to(tick, DOWN, buff=0.2))
    g.bigos = VGroup(MathTex("O(n)", font_size=40, color=GREEN).next_to(g.names[0], DOWN, buff=0.2),
                     MathTex("O(n^2)", font_size=40, color=RED).next_to(g.names[2], DOWN, buff=0.2))
    g.caption = T("comparisons for 10,000 items", 30, DIM).move_to([0, -1.75, 0])
    g.add(g.line, g.ticks, g.values, g.names, g.bigos, g.caption)
    return g


class Block:
    """One chain row of the table, plus its tally row and rs row."""

    def __init__(self, values, name, color, y, tally_y, rs_y, tally_parts, rs_text):
        self.values = list(values)
        self.chain = ConsChain(self.values).scale(CH_SCALE)
        self.chain.shift([X0 - self.chain.get_left()[0], y - self.chain.get_center()[1], 0])
        for cell in self.chain.cells:
            cell.set_z_index(1)
        self.slots = [cell.get_center().copy() for cell in self.chain.cells]
        self.order = list(self.chain.cells)          # cell in each slot, left to right
        self.right = self.chain.get_right()[0]
        self.label = T(name, 40, color)
        self.label.shift([HX - self.label.get_right()[0], y - self.label.get_center()[1], 0])
        self.q = T("?", 54, YELLOW).move_to([self.chain.get_center()[0], y + 0.375 * 1.0 + 0.48, 0])
        # tally row: digits GOLD, operators FG
        self.tex = MathTex(*tally_parts, font_size=TALLY_FS)
        for i, part in enumerate(self.tex):
            part.set_color(FG if tally_parts[i] in ("+", "=") else GOLD)
        self.tex.shift([X0 - self.tex[0].get_left()[0], tally_y - self.tex[0].get_center()[1], 0])
        self.tally_head = T("comparisons", 30, DIM)
        self.tally_head.shift([HX - self.tally_head.get_right()[0],
                               self.tex[0].get_center()[1] - self.tally_head.get_center()[1], 0])
        self.entries = []
        # rs row
        self.rs_head = T(f"{name} rs", 30, DIM)
        self.rs_head.shift([HX - self.rs_head.get_right()[0], rs_y - self.rs_head.get_center()[1], 0])
        self.rs_val = T(rs_text, 40, GOLD)
        self.rs_val.shift([X0 - self.rs_val.get_left()[0], rs_y - self.rs_val.get_center()[1], 0])
        self.verdict_pos = np.array([self.right - 0.4, rs_y, 0])

    def entry(self, n, idx):
        return MathTex(str(n), font_size=TALLY_FS, color=GOLD).move_to(self.tex[2 * idx])


class BestWorst(NarratedScene):
    def construct(self):
        self.top = Block([3, 4, 5, 7, 9], "sorted", GREEN, TOP_Y, TOP_TALLY_Y, TOP_RS_Y,
                         ["0", "+", "1", "+", "1", "+", "1", "+", "1", "=", "4", "=", "n-1"], "9,999")
        self.bot = Block([9, 7, 5, 4, 3], "reversed", RED, BOT_Y, BOT_TALLY_Y, BOT_RS_Y,
                         ["0", "+", "1", "+", "2", "+", "3", "+", "4", "=", "10", "=", r"\frac{n(n-1)}{2}"],
                         "49,995,000")
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---- helpers ------------------------------------------------------------------------
    def read_along(self, c, blk, first_cue, last_cue, color):
        """Underline flashes walking the cells left to right as the voice reads the values."""
        c.wait_until(first_cue)
        span = c.until(last_cue, floor=1.0)
        self.play(LaggedStart(*[FlashUnder(cell, color=color, time_width=1.0) for cell in blk.order],
                              lag_ratio=1.0, run_time=1.25 * span))

    def first_insert(self, blk):
        """ins x [] = [x]: no comparison; the last cell becomes the sorted part."""
        cell = blk.order[-1]
        e = blk.entry(0, 0)
        blk.entries.append(e)
        self.play(cell.animate.set_stroke(GREEN), FadeIn(blk.tally_head), FadeIn(e, shift=0.2 * DOWN),
                  run_time=0.9)

    def run_inserts(self, blk, avail):
        """Insert slots n-2 .. 0 into the sorted suffix, in place, within `avail` seconds."""
        n = len(blk.order)
        vals = list(blk.values)
        plans = []
        for k in range(n - 2, -1, -1):
            j, m, passes = k, 0, 0
            while j + 1 < n:
                m += 1
                if vals[j] <= vals[j + 1]:
                    break
                vals[j], vals[j + 1] = vals[j + 1], vals[j]
                j += 1
                passes += 1
            plans.append((k, m, passes))
        nominal = sum((LIFT_T + p * PASS_T + (m - p) * CMP_T + DROP_T + HOLD_T) * MULTS[i]
                      for i, (_, m, p) in enumerate(plans))
        scale = min(1.0, avail / nominal)

        for idx, (k, m, passes) in enumerate(plans):
            s = MULTS[idx] * scale
            cell = blk.order[k]
            e = blk.entry(0, idx + 1)
            blk.entries.append(e)
            cell.set_z_index(3)
            self.play(cell.animate.shift(LIFT * UP).set_stroke(YELLOW),
                      FadeIn(blk.tex[2 * idx + 1]), FadeIn(e),
                      run_time=max(0.22, LIFT_T * s))
            j = k
            for step in range(m):
                other = blk.order[j + 1]
                passing = step < passes
                rt = max(0.3, (PASS_T if passing else CMP_T) * s)
                anims = [FlashAround(other, color=YELLOW, time_width=1.5,
                                     run_time=0.6 * rt if passing else rt),
                         Transform(e, blk.entry(step + 1, idx + 1), run_time=0.5 * rt)]
                if passing:
                    anims += [time_span(cell.animate.move_to(blk.slots[j + 1] + LIFT * UP), 0.4 * rt, rt),
                              time_span(other.animate.move_to(blk.slots[j]), 0.4 * rt, rt)]
                    blk.order[j], blk.order[j + 1] = other, cell
                    j += 1
                self.play(*anims)
            self.play(cell.animate.move_to(blk.slots[j]).set_stroke(GREEN), run_time=max(0.22, DROP_T * s))
            cell.set_z_index(1)
            self.wait(HOLD_T * s)

    # ---- clips --------------------------------------------------------------------------
    def clip1(self):
        top, bot = self.top, self.bot
        with self.say("c2.best.1") as c:
            six = T("6", 88, GOLD).move_to([-4.2, 0.4, 0])
            rnd = T("25,146,194", 88, GOLD).move_to([1.7, 0.4, 0]).align_to(six, UP)
            six_cap = T("our chain", 34, DIM).next_to(six, DOWN, buff=0.45)
            rnd_cap = T("random rs", 34, DIM).next_to(rnd, DOWN, buff=0.45).match_y(six_cap)
            self.play(FadeIn(six, shift=0.3 * DOWN), FadeIn(six_cap), run_time=1.0)
            c.wait_until("twenty-five million")
            self.play(FadeIn(rnd, shift=0.3 * DOWN), FadeIn(rnd_cap), run_time=1.0)
            c.wait_until("ask")
            sweep_clear(self,
                        time_span(FadeIn(top.label), 0.3, 1.2), time_span(FadeIn(top.chain), 0.3, 1.3),
                        time_span(FadeIn(bot.label), 0.6, 1.5), time_span(FadeIn(bot.chain), 0.6, 1.6),
                        run_time=1.6)
            c.wait_until("best")
            self.play(FadeIn(top.q, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("worst")
            self.play(FadeIn(bot.q, shift=0.3 * DOWN), run_time=0.8)

    def clip2(self):
        top, bot = self.top, self.bot
        with self.say("c2.best.2") as c:
            # {sorted}: spotlight the sorted chain; its "?" goes to wait where the verdict lands
            self.play(*set_alpha([bot.label, bot.chain, bot.q], DIMMED),
                      top.q.animate.move_to(top.verdict_pos), run_time=1.0)
            self.read_along(c, top, "three", "nine", GREEN)
            self.first_insert(top)
            # {stop}: each insert stops at its first comparison
            c.wait_until("stop")
            self.run_inserts(top, c.until("four") - 0.15)
            # {four}
            c.wait_until("four")
            self.play(FadeIn(top.tex[9]), TransformFromCopy(VGroup(*top.entries), top.tex[10]), run_time=1.5)
            c.wait_until("one fewer")
            self.play(FadeIn(top.tex[11]), FadeIn(top.tex[12], shift=0.2 * DOWN), run_time=1.0)
            # {sortedrs}
            c.wait_until("sortedrs")
            self.play(FadeIn(top.rs_head), run_time=0.8)
            c.wait_until("it takes")
            self.play(FadeIn(top.rs_val, shift=0.3 * DOWN), run_time=1.0)
            # {linear}: the question becomes the answer
            c.wait_until("linear")
            verdict = MathTex("O(n)", font_size=52, color=GREEN)
            verdict.move_to(top.verdict_pos).align_to(np.array([top.right, 0, 0]), RIGHT)
            self.top_verdict = verdict
            self.play(ReplacementTransform(top.q, verdict), run_time=1.2)

    def clip3(self):
        top, bot = self.top, self.bot
        with self.say("c2.best.3", gap=0.8) as c:
            # {reversed}: spotlight swaps to the bottom chain
            self.play(*set_alpha([bot.label, bot.chain], 1),
                      restyle(bot.q, op=1, shift=bot.verdict_pos - bot.q.get_center()),
                      restyle(top.label, op=0.4), restyle(top.chain, op=0.4), run_time=1.0)
            self.read_along(c, bot, "nine", "three", RED)
            self.first_insert(bot)
            # {walk}: every insert walks the whole sorted part, to the end
            c.wait_until("walk")
            self.run_inserts(bot, c.until("ten") - 0.1)
            # {ten}: read the tally term by term
            c.wait_until("ten")
            box = token_box(bot.entries[0], bot.entries[0])
            self.play(FadeIn(box), run_time=0.4)
            for i, cue in enumerate(["plus one", "plus two", "plus three", "plus four"]):
                c.wait_until(cue)
                self.play(Transform(box, token_box(bot.entries[i + 1], bot.entries[i + 1])), run_time=0.4)
            c.wait_until("ten comparisons")
            self.play(FadeOut(box), FadeIn(bot.tex[9]),
                      TransformFromCopy(VGroup(*bot.entries), bot.tex[10]), run_time=1.5)
            c.wait_until("which is")
            self.play(FadeIn(bot.tex[11]), FadeIn(bot.tex[12], shift=0.2 * DOWN), run_time=1.2)
            # {revrs}
            c.wait_until("revrs")
            self.play(FadeIn(bot.rs_head), run_time=0.8)
            c.wait_until("numbers take")
            self.play(FadeIn(bot.rs_val, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("nine hundred")
            verdict = MathTex("O(n^2)", font_size=52, color=RED)
            verdict.move_to(bot.verdict_pos).align_to(np.array([bot.right, 0, 0]), RIGHT)
            self.play(ReplacementTransform(bot.q, verdict), run_time=1.2)
            # the worst case exactly, about twice random
            c.wait_until("the worst case")
            note = T("≈ 2 × 25,146,194", 30, DIM).next_to(bot.rs_val, RIGHT, buff=0.5)
            self.play(FlashAround(bot.rs_val, run_time=2, time_width=1.5),
                      FlashAround(bot.tex[12], run_time=2, time_width=1.5),
                      time_span(FadeIn(note, shift=0.2 * DOWN), 1.0, 2.0))

    def clip4(self):
        top = self.top
        with self.say("c2.best.4") as c:
            # {range}: keep the sorted chain (to the top, centred), clear the rest, draw the scale
            grp = VGroup(top.label, top.chain)
            shift = np.array([-grp.get_center()[0], 2.45 - top.chain.get_center()[1], 0])
            sweep_clear(self, restyle(top.chain, op=1, shift=shift), restyle(top.label, op=1, shift=shift),
                        keep=[top.chain, top.label], run_time=1.2)
            sc = range_scale().shift(0.55 * DOWN)
            self.play(Create(sc.line), FadeIn(sc.caption), run_time=1.2)
            c.wait_until("linear")
            self.play(GrowFromCenter(sc.ticks[0]), FadeIn(sc.values[0], shift=0.3 * DOWN),
                      FadeIn(sc.names[0]), FadeIn(sc.bigos[0]), run_time=1.0)
            c.wait_until("quadratic")
            self.play(GrowFromCenter(sc.ticks[2]), FadeIn(sc.values[2], shift=0.3 * DOWN),
                      FadeIn(sc.names[2]), FadeIn(sc.bigos[1]), run_time=1.0)
            c.wait_until("with random input")
            self.play(GrowFromCenter(sc.ticks[1]), FadeIn(sc.values[1], shift=0.3 * DOWN),
                      FadeIn(sc.names[1]), run_time=1.0)
            c.wait_until("half the worst")
            self.play(FlashAround(sc.values[1], run_time=1.5, time_width=1.5))
            # {remember}: the sorted chain, framed
            c.wait_until("remember")
            frame = SurroundingRectangle(top.chain, color=YELLOW, buff=0.2)
            tag = T("quicksort's worst case (Part 4)", 32, DIM).next_to(frame, DOWN, buff=0.3)
            self.play(Create(frame), time_span(FadeIn(tag, shift=0.3 * DOWN), 0.6, 1.6))
            c.wait_until("favourite")
            self.play(FlashAround(sc.values[0], color=GREEN, run_time=1.5, time_width=1.5))
            c.wait_until("quicksort")
            self.play(FlashAround(tag, run_time=1.5, time_width=1.5))
