"""Chapter 6, scene 4: one task at a time, no pipelining. Clips c6.seq.1 – c6.seq.3."""
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

DIM_W = 3           # dimension arrows (as ch1_s5_datasheet)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    """Dimension arrow (ch1_s5_datasheet): thin double-headed line from xa to xb at y, small tips,
    with a same-colour MathTex label above (UP) or below (DOWN). Returns VGroup(arrow, label)."""
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def grow_dim(arr):
    """Grow a dim_arrow's DoubleArrow from its centre at the true tip size (ch1_s5_datasheet)."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()
    min_len = 0.4

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        L = a * np.linalg.norm(end - start)
        if L < min_len:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


# ============================================================================
# Timeline builder (s5 copies this block)
TASK_COLORS = {1: BLUE, 2: GREEN, 3: TEAL, 4: FG}
PERIOD = 3.4                       # one clock period, in units
X0 = -1.5 * PERIOD                 # left edge of period 1: boundaries at -5.1, -1.7, 1.7, 5.1
STAGE_W = PERIOD / 2               # each stage box is half a period: 1.7 wide
STAGE_H = 0.9
ARROW_Y = 1.9                      # T_c arrows over each period
LANE1_Y = 0.3                      # first-stage hardware
LANE2_Y = -1.9                     # second-stage hardware
ROW_Y = (LANE1_Y + LANE2_Y) / 2    # the single row before the split
GUIDE_TOP, GUIDE_BOT = 1.6, -2.6


def slot_left(period, stage):
    """Left x of a stage slot: period 0,1,2…; stage 0 (first) or 1 (second)."""
    return X0 + period * PERIOD + stage * STAGE_W


def stage_box(stage, task, x_left, y, width=STAGE_W, height=STAGE_H, size=40):
    """A stage box: task-coloured outline, faint fill, label like A_1. VGroup(rect, label)."""
    col = TASK_COLORS[task]
    rect = Rectangle(width=width, height=height).set_stroke(col, 3).set_fill(col, 0.18)
    rect.move_to([x_left + width / 2, y, 0])
    lab = MathTex(f"{stage}_{task}", font_size=size, color=col).move_to(rect)
    return VGroup(rect, lab)


def hatch(x_left, y, width=STAGE_W, height=STAGE_H, spacing=0.22, color=DIM):
    """DIM idle hatching: outline plus 45-degree lines clipped to the slot. VGroup(outline, lines)."""
    x0, x1 = x_left, x_left + width
    y0, y1 = y - height / 2, y + height / 2
    lines = VGroup()
    k = x0 - height + spacing / 2
    while k < x1:
        xa, xb = max(x0, k), min(x1, k + height)
        if xb - xa > 0.02:
            lines.add(Line([xa, y0 + xa - k, 0], [xb, y0 + xb - k, 0]).set_stroke(color, 2, 0.6))
        k += spacing
    outline = Rectangle(width=width, height=height).set_stroke(color, 2).move_to([x0 + width / 2, y, 0])
    return VGroup(outline, lines)
# ============================================================================


class OneTaskAtATime(NarratedScene):
    def construct(self):
        # ---- task bar geometry (clips 1-2) ----
        BX, BY, BW, BH = -2.7, -0.5, 6.0, 1.8
        bl, br = BX - BW / 2, BX + BW / 2

        with self.say("c6.seq.1") as c:
            sysbox = RoundedRectangle(width=4.4, height=1.8, corner_radius=0.25).set_stroke(FG, 4)
            sysbox.move_to([BX, BY, 0])
            systxt = T("the system", size=36).move_to(sysbox)
            self.play(FadeIn(sysbox), FadeIn(systxt), run_time=1.0)
            c.wait_until("task")

            bar = RoundedRectangle(width=BW, height=BH, corner_radius=0.25).set_stroke(FG, 4)
            bar.move_to([BX, BY, 0])
            task_lab = T("Task", size=44).move_to([bl, BY + BH / 2 + 1.75, 0], aligned_edge=LEFT)
            self.play(ReplacementTransform(sysbox, bar), systxt.animate.move_to(bar),
                      *during(appear(task_lab), 0.4, 1.0), run_time=1.5)
            c.wait_until("two stages")

            divider = Line([BX, BY - BH / 2, 0], [BX, BY + BH / 2, 0]).set_stroke(FG, 4)
            a_lab = MathTex("A", font_size=60).move_to([BX - BW / 4, BY, 0])
            b_lab = MathTex("B", font_size=60).move_to([BX + BW / 4, BY, 0])
            self.play(*during([FadeOut(systxt, shift=0.2 * UP)], 0, 0.4),
                      *during([GrowFromCenter(divider)], 0.3, 0.7),
                      *during(appear(a_lab, b_lab, lag=0.4), 0.45, 1.0), run_time=2.0)

            legend = T("A = stage 1,  B = stage 2", size=32, color=DIM)
            legend.next_to(task_lab, RIGHT, buff=0.8).align_to(task_lab, DOWN)
            c.wait_until("a first stage", own_word=legend)
            self.play(*appear(legend), run_time=1.0)
            c.wait_until("result")

            # A -> B handover: a curve from under A's middle, sagging below the bar, up into under B's middle
            ry = BY - BH / 2 - 0.15
            res_arrow = CurvedArrow([BX - BW / 4, ry, 0], [BX + BW / 4, ry, 0], angle=PI / 3,
                                    stroke_width=4, color=FG, tip_length=0.22)
            res_lab = T("A's result", size=30).next_to(res_arrow, DOWN, buff=0.15)
            self.play(Create(res_arrow), run_time=1.2)
            c.wait_until(own_word=res_lab)
            self.play(*appear(res_lab), run_time=0.9)
            c.wait_until("period")

            tc = dim_arrow(bl, br, BY + BH / 2 + 0.4, YELLOW, "T_c")
            self.play(grow_dim(tc[0]), *during(appear(tc[1]), 0.4, 1.0), run_time=1.5)
            c.wait_until("ten nanoseconds")

            ten = MathTex(r"=10\,\text{ns}", font_size=44, color=GOLD)
            ten.next_to(tc[1], RIGHT, buff=0.15).align_to(tc[1], DOWN)
            self.play(*appear(ten, shift=None), run_time=1.0)

        with self.say("c6.seq.2", gap=1.2) as c:
            b_region = Rectangle(width=BW / 2, height=BH).move_to([BX + BW / 4, BY, 0])
            self.play(FlashAround(b_region, time_width=1.5, color=YELLOW),
                      *during(disappear(res_arrow, res_lab), 0.3, 1.0), run_time=2.0)
            c.wait_until("latency")

            RX = 1.2
            lat = MathTex(r"\text{Latency}", "=", "T_c", font_size=52)
            lat[2].set_color(YELLOW)
            lat.move_to([RX, BY + 1.2, 0], aligned_edge=LEFT)
            brace = span_brace([bl, BY - BH / 2, 0], [br, BY - BH / 2, 0], DOWN, color=YELLOW)
            self.play(GrowFromCenter(brace), *appear(lat, shift=None), run_time=1.5)
            c.wait_until("the throughput")

            thr = MathTex(r"\text{Throughput}", "=", r"\frac{1}{T_c}", font_size=52)
            thr[2][2:].set_color(YELLOW)
            thr.move_to([RX, BY - 0.15, 0], aligned_edge=LEFT)
            self.play(*appear(thr, shift=None), run_time=1.2)
            c.wait_until("frequency")

            freq = VGroup(MathTex("=", "f_c", font_size=52),
                          T(", the clock frequency", size=32)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            freq[0][1].set_color(YELLOW)
            freq.move_to([RX, BY - 1.45, 0], aligned_edge=LEFT)
            self.play(*appear(freq, shift=None), run_time=1.2)

        with self.say("c6.seq.3") as c:
            bounds = [X0 + i * PERIOD for i in range(4)]
            guides = VGroup(*[DashedLine([x, GUIDE_BOT, 0], [x, GUIDE_TOP, 0], dash_length=0.12)
                              .set_stroke(DIM, 2) for x in bounds])
            tcs = [dim_arrow(bounds[i] + 0.05, bounds[i + 1] - 0.05, ARROW_Y, YELLOW, "T_c", size=36)
                   for i in range(3)]
            sweep_clear(self, *[FadeIn(g) for g in guides], run_time=1.0)
            self.play(*[grow_dim(t[0]) for t in tcs], *appear(*[t[1] for t in tcs], shift=None, lag=0.1),
                      run_time=1.0)
            c.wait_until("t1")

            a1 = stage_box("A", 1, slot_left(0, 0), ROW_Y)
            b1 = stage_box("B", 1, slot_left(0, 1), ROW_Y)
            a2 = stage_box("A", 2, slot_left(1, 0), ROW_Y)
            b2 = stage_box("B", 2, slot_left(1, 1), ROW_Y)
            a3 = stage_box("A", 3, slot_left(2, 0), ROW_Y)
            self.play(*appear(a1, shift=None), run_time=1.0)
            c.wait_until("then its second")
            self.play(*appear(b1, shift=None), run_time=1.0)
            c.wait_until("t2")
            self.play(*appear(a2, shift=None), run_time=0.9)
            c.wait_until("first stage")
            self.play(*appear(b2, shift=None), run_time=0.8)
            c.wait_until("t3")
            self.play(*appear(a3, shift=None), run_time=0.8)
            c.wait_until("look")

            up, down = LANE1_Y - ROW_Y, LANE2_Y - ROW_Y
            self.play(*[m.animate.shift(up * UP) for m in (a1, a2, a3)],
                      *[m.animate.shift(down * UP) for m in (b1, b2)], run_time=2.0)
            lane1 = T("first-stage hardware", size=30).move_to(
                [X0, LANE1_Y + STAGE_H / 2 + 0.3, 0], aligned_edge=LEFT)
            lane2 = T("second-stage hardware", size=30).move_to(
                [X0, LANE2_Y + STAGE_H / 2 + 0.3, 0], aligned_edge=LEFT)
            set_backstroke(lane1, width=8)
            set_backstroke(lane2, width=8)
            c.wait_until("for the first stage")
            self.play(*appear(lane1), run_time=1.0)
            c.wait_until("what is it doing")

            gaps1 = [slot_left(0, 1), slot_left(1, 1), slot_left(2, 1)]
            gaps2 = [slot_left(0, 0), slot_left(1, 0), slot_left(2, 0)]
            regions = [Rectangle(width=STAGE_W, height=STAGE_H).move_to([x + STAGE_W / 2, LANE1_Y, 0])
                       for x in gaps1]
            self.play(*[FlashAround(r, time_width=1.5, color=YELLOW) for r in regions], run_time=1.5)
            c.wait_until("the second stage works")
            self.play(*appear(lane2), run_time=1.0)
            c.wait_until("idle")

            h1 = [hatch(x, LANE1_Y) for x in gaps1]
            idle1 = T("idle", size=30, color=FG).move_to(h1[0])
            set_backstroke(idle1, width=8)
            self.play(*appear(*h1, shift=None, lag=0.2), *during(appear(idle1, shift=None), 0.5, 1.0),
                      run_time=1.5)
            c.wait_until("and the second stage's")

            h2 = [hatch(x, LANE2_Y) for x in gaps2]
            idle2 = T("idle", size=30, color=FG).move_to(h2[0])
            set_backstroke(idle2, width=8)
            self.play(*appear(*h2, shift=None, lag=0.2), *during(appear(idle2, shift=None), 0.5, 1.0),
                      run_time=1.5)

        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
