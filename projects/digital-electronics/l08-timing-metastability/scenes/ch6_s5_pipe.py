"""Chapter 6, scene 5: overlapping tasks, the pipeline staircase. Clips c6.pipe.1 – c6.pipe.6."""
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

DIM_W = 3           # dimension arrows (as ch1_s5_datasheet / ch6_s4_nopipe)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    """Dimension arrow (ch6_s4_nopipe): thin double-headed line from xa to xb at y, small tips,
    with a same-colour MathTex label above (UP) or below (DOWN). Returns VGroup(arrow, label)."""
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def grow_dim(arr):
    """Grow a dim_arrow's DoubleArrow from its centre at the true tip size (ch6_s4_nopipe)."""
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
# Timeline builder (copied from ch6_s4_nopipe) + the pipeline staircase (ch7 s6 reuses this block)
TASK_COLORS = {1: BLUE, 2: GREEN, 3: TEAL, 4: FG}
PERIOD = 3.4                       # s4's clock period (both stages), in units
X0 = -1.5 * PERIOD                 # left edge of period 1: -5.1
STAGE_W = PERIOD / 2               # each stage box: 1.7 wide
STAGE_H = 0.9
ARROW_Y = 1.9                      # s4's T_c arrows
LANE1_Y = 0.3
LANE2_Y = -1.9
ROW_Y = (LANE1_Y + LANE2_Y) / 2
GUIDE_TOP, GUIDE_BOT = 1.6, -2.6

# staircase (this scene's hero; ch7 s6 brings it back)
STAIR_X0 = X0                      # left edge of column 0 (same grid as s4: A1, B1 stay put)
STAIR_TOP_Y = 1.75                 # centre y of row 1
STAIR_PITCH = 1.3                  # row pitch
STAIR_ARROW_Y = 2.65               # per-stage T_c arrows
STAIR_N = 4


def slot_left(period, stage):
    """Left x of an s4 stage slot: period 0,1,2…; stage 0 (first) or 1 (second)."""
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


def stair_y(row, top=STAIR_TOP_Y, pitch=STAIR_PITCH):
    """Centre y of staircase row `row` (0 = task 1)."""
    return top - row * pitch


def stair_x(col, x0=STAIR_X0, w=STAGE_W):
    """Left x of staircase column `col` (task k's A sits in column k-1, its B in column k)."""
    return x0 + col * w


def staircase(x0=STAIR_X0, top=STAIR_TOP_Y, pitch=STAIR_PITCH, w=STAGE_W, h=STAGE_H, size=40,
              n=STAIR_N, arrow_y=STAIR_ARROW_Y, guide_top=None):
    """The pipeline staircase: row r holds A_{r+1} (column r) and B_{r+1} (column r+1).
    Returns dict: 'A'/'B' -> list of stage boxes (index = row), 'guides' (DIM dashed lines at every
    column boundary, each running down to the lowest box it touches), 'arrows' (YELLOW T_c
    dim_arrows, one per column, at arrow_y)."""
    A = [stage_box("A", r + 1, x0 + r * w, top - r * pitch, w, h, size) for r in range(n)]
    B = [stage_box("B", r + 1, x0 + (r + 1) * w, top - r * pitch, w, h, size) for r in range(n)]
    gt = top + h / 2 + 0.1 if guide_top is None else guide_top
    guides = VGroup()
    for i in range(n + 2):
        low = min(i, n - 1)
        x = x0 + i * w
        guides.add(DashedLine([x, gt, 0], [x, top - low * pitch - h / 2 - 0.1, 0], dash_length=0.12)
                   .set_stroke(DIM, 2))
    arrows = [dim_arrow(x0 + i * w + 0.05, x0 + (i + 1) * w - 0.05, arrow_y, YELLOW, "T_c", size=36)
              for i in range(n + 1)]
    return {"A": A, "B": B, "guides": guides, "arrows": arrows}


def column_box(col, x0=STAIR_X0, top=STAIR_TOP_Y, pitch=STAIR_PITCH, w=STAGE_W, h=STAGE_H, n=STAIR_N):
    """YELLOW highlight round column `col`: covers the rows that have a box in it."""
    r0, r1 = max(0, col - 1), min(n - 1, col)
    yt, yb = top - r0 * pitch + h / 2 + 0.12, top - r1 * pitch - h / 2 - 0.12
    rect = Rectangle(width=w + 0.16, height=yt - yb).move_to([x0 + (col + 0.5) * w, (yt + yb) / 2, 0])
    return rect.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).set_z_index(-1)


def box_alpha(boxes, op):
    """Dim (op < 1) or restore (op = 1) stage boxes, keeping their faint 0.18 fill."""
    anims = []
    for b in boxes:
        t = b.copy()
        t[0].set_stroke(opacity=op).set_fill(opacity=0.18 * op)
        t[1].set_opacity(op)
        anims.append(Transform(b, t))
    return anims


def finish_tick(x, y, h=STAGE_H):
    """GOLD tick marking a task finishing at x (right end of its B box)."""
    return Line([x, y - h / 2 - 0.15, 0], [x, y + h / 2 + 0.15, 0]).set_stroke(GOLD, 6)
# ============================================================================

# compact layout for the side-by-side comparison (clips 5-6): 25 ns axis, 5 ns per stage box
CX0, CW, CH = -6.2, 1.4, 0.6
TOP_ROW_Y = 2.3
AXIS_Y = 1.35
C_TOP, C_PITCH = 0.25, 0.75
RX = 1.5                            # left edge of the right-hand text column


def label_line(*parts, size=32, color=FG):
    """Prose pieces and MathTex arrows on one baseline."""
    g = VGroup(*parts).arrange(RIGHT, buff=0.18)
    return g


class OverlappingTasks(NarratedScene):
    def construct(self):
        # ---------- s4's end shot ----------
        bounds = [X0 + i * PERIOD for i in range(4)]
        guides4 = VGroup(*[DashedLine([x, GUIDE_BOT, 0], [x, GUIDE_TOP, 0], dash_length=0.12)
                           .set_stroke(DIM, 2) for x in bounds])
        tcs4 = [dim_arrow(bounds[i] + 0.05, bounds[i + 1] - 0.05, ARROW_Y, YELLOW, "T_c", size=36)
                for i in range(3)]
        a1 = stage_box("A", 1, slot_left(0, 0), LANE1_Y)
        b1 = stage_box("B", 1, slot_left(0, 1), LANE2_Y)
        a2 = stage_box("A", 2, slot_left(1, 0), LANE1_Y)
        b2 = stage_box("B", 2, slot_left(1, 1), LANE2_Y)
        a3 = stage_box("A", 3, slot_left(2, 0), LANE1_Y)
        lane1 = T("first-stage hardware", size=30).move_to(
            [X0, LANE1_Y + STAGE_H / 2 + 0.3, 0], aligned_edge=LEFT)
        lane2 = T("second-stage hardware", size=30).move_to(
            [X0, LANE2_Y + STAGE_H / 2 + 0.3, 0], aligned_edge=LEFT)
        set_backstroke(lane1, width=8)
        set_backstroke(lane2, width=8)
        gaps1 = [slot_left(0, 1), slot_left(1, 1), slot_left(2, 1)]
        gaps2 = [slot_left(0, 0), slot_left(1, 0), slot_left(2, 0)]
        h1 = [hatch(x, LANE1_Y) for x in gaps1]
        h2 = [hatch(x, LANE2_Y) for x in gaps2]
        idle1 = T("idle", size=30, color=FG).move_to(h1[0])
        idle2 = T("idle", size=30, color=FG).move_to(h2[0])
        set_backstroke(idle1, width=8)
        set_backstroke(idle2, width=8)
        self.add(guides4, *tcs4, *h1, *h2, a1, b1, a2, b2, a3, lane1, lane2, idle1, idle2)

        st = staircase()
        A, B = st["A"], st["B"]

        # ---------- clip 1: the staircase is built ----------
        with self.say("c6.pipe.1") as c:
            r0 = stair_y(0)
            self.play(*during(disappear(*h1, *h2, idle1, idle2, lane1, lane2, guides4), 0, 0.45),
                      *during([m.animate.move_to([m.get_x(), r0, 0]) for m in (a1, b1, a2, b2, a3)],
                              0.3, 1.0),
                      *[t.animate.shift((STAIR_ARROW_Y - ARROW_Y) * UP) for t in tcs4],
                      run_time=min(2.2, c.until("start")))
            c.wait_until("start")

            free_box = DashedVMobject(Rectangle(width=STAGE_W, height=STAGE_H), num_dashes=24)
            free_box.set_stroke(YELLOW, 3).move_to(A[1][0])
            free = T("free", size=32, color=YELLOW).move_to(free_box)
            self.play(FlashAround(a1, time_width=1.5, color=YELLOW), FadeIn(free_box), run_time=1.5)
            self.play(*appear(free, shift=None), run_time=0.8)  # early: names the slot the sentence is about
            c.wait_until("so task two starts")

            def corner_path(mob, dst):
                p, q = mob.get_center(), dst.get_center()
                return VMobject().set_points_as_corners([p, [p[0], q[1], 0], q])

            self.play(*during(disappear(free, free_box), 0.3, 0.6),
                      MoveAlongPath(a2, corner_path(a2, A[1])),
                      MoveAlongPath(b2, corner_path(b2, B[1])),
                      run_time=2.0)
            c.wait_until("stair")

            self.play(MoveAlongPath(a3, corner_path(a3, A[2])),
                      *during(appear(B[2], shift=None), 0.75, 1.0), run_time=2.0)
            c.wait_until("and task four")
            self.play(*appear(A[3], B[3], shift=None, lag=0.4), run_time=1.3)
            c.wait_until("the timeline becomes")

            self.play(*during(disappear(*tcs4), 0, 0.45),
                      *during([FadeIn(g) for g in st["guides"]], 0.3, 1.0),
                      *during([grow_dim(t[0]) for t in st["arrows"]], 0.5, 1.0),
                      *during(appear(*[t[1] for t in st["arrows"]], shift=None, lag=0.1), 0.6, 1.0),
                      run_time=min(2.0, c.until()))
            # the moved s4 boxes stand in for the staircase's own
            A[0], B[0], A[1], B[1], A[2] = a1, b1, a2, b2, a3

        # ---------- clip 2: read it by columns ----------
        with self.say("c6.pipe.2") as c:
            hl = column_box(0)
            self.play(FadeIn(hl), run_time=1.0)
            c.wait_until("fill")
            self.play(FlashAround(A[0], time_width=1.5, color=YELLOW), run_time=1.5)
            c.wait_until("c1")
            self.play(Transform(hl, column_box(1)), run_time=1.2)
            c.wait_until("c2")
            self.play(Transform(hl, column_box(2)), run_time=1.0)
            c.wait_until("c3")
            self.play(Transform(hl, column_box(3)), run_time=1.0)
            c.wait_until("each")

            note = T("Each task passes through both\n"
                     "stages, but a different task will be in\n"
                     "each stage at any given time, i.e.,\n"
                     "multiple tasks can overlap", size=28, color=DIM, line_spacing=0.6)
            note.move_to([-6.6, stair_y(2) - STAGE_H / 2 - 0.15, 0], aligned_edge=UL)
            self.play(FadeOut(hl), *appear(note, shift=None), run_time=1.2)  # early: the slide's note, quoted whole

        # ---------- clip 3: latency and throughput ----------
        with self.say("c6.pipe.3") as c:
            lat_q = T("latency?", size=36, color=GOLD).move_to([-1.9, stair_y(1) - 1.15, 0], aligned_edge=RIGHT)
            thr_pos = np.array([4.3, stair_y(1) - 0.2, 0])
            thr_q = T("throughput?", size=36, color=GOLD).move_to(thr_pos)
            c.wait_until(own_word=lat_q)
            self.play(*appear(lat_q, thr_q, lag=0.3), run_time=1.2)
            c.wait_until("two")

            others = [m for r in (0, 2, 3) for m in (A[r], B[r])]
            brace = span_brace([stair_x(1), stair_y(1) - STAGE_H / 2, 0],
                               [stair_x(3), stair_y(1) - STAGE_H / 2, 0], DOWN, color=GOLD, buff=0.08)
            self.play(*box_alpha(others, 0.3), GrowFromCenter(brace), run_time=1.5)
            lat = MathTex(r"\text{Latency}", "=", "2", "T_c", font_size=44)
            lat[2].set_color(GOLD)
            lat[3].set_color(YELLOW)
            lat.move_to([-1.9, stair_y(1) - 1.15, 0], aligned_edge=RIGHT)
            c.wait_until("so the latency")
            self.play(*swap(lat_q, lat), run_time=1.2)
            c.wait_until("thru")

            ticks = [finish_tick(stair_x(r + 2), stair_y(r)) for r in range(STAIR_N)]
            self.play(*box_alpha(others, 1),
                      *during([FadeIn(t, shift=0.15 * DOWN) for t in ticks[:1]], 0.2, 0.45),
                      *during([FadeIn(t, shift=0.15 * DOWN) for t in ticks[1:2]], 0.4, 0.65),
                      *during([FadeIn(t, shift=0.15 * DOWN) for t in ticks[2:3]], 0.6, 0.85),
                      *during([FadeIn(t, shift=0.15 * DOWN) for t in ticks[3:]], 0.8, 1.0),
                      run_time=2.4)
            c.wait_until("so the throughput is")

            thr = MathTex(r"\text{Throughput}", "=", r"\frac{1}{T_c}", font_size=44)
            thr[2][2:].set_color(YELLOW)
            thr.move_to(thr_pos)
            self.play(*swap(thr_q, thr), run_time=1.2)

        # ---------- clip 4: same formula, different period ----------
        with self.say("c6.pipe.4") as c:
            old = MathTex(r"\text{Throughput}", "=", r"\frac{1}{T_c}", font_size=44)
            old[2][2:].set_color(YELLOW)
            old.move_to(thr_pos + 1.5 * UP)
            self.play(FadeIn(old, shift=0.6 * LEFT), run_time=0.9)
            c.wait_until("that's the same")
            qm = MathTex("?", font_size=60, color=YELLOW).move_to(thr_pos + 0.78 * UP)
            self.play(FlashAround(old, time_width=1.5), FlashAround(thr, time_width=1.5),
                      *during(appear(qm, shift=None), 0.4, 1.0), run_time=2.0)
            c.wait_until("period")

            # the long period takes the place of the first two per-stage arrows, label centred above
            short2 = st["arrows"][:2]
            long_tc = VGroup(
                DoubleArrow([stair_x(0) + 0.05, STAIR_ARROW_Y, 0], [stair_x(2) - 0.05, STAIR_ARROW_Y, 0],
                            buff=0, stroke_width=DIM_W, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.4, color=YELLOW))
            long_lab = MathTex("T_c", font_size=36, color=YELLOW).next_to(long_tc[0], UP, buff=0.15)
            self.play(*during(disappear(*short2), 0, 0.4),
                      *during([grow_dim(long_tc[0])], 0.4, 1.0),
                      *during(appear(long_lab, shift=None), 0.6, 1.0), run_time=1.8)
            c.wait_until("before one period")

            two_stages = Rectangle(width=2 * STAGE_W, height=STAGE_H).move_to(
                [stair_x(1), stair_y(0), 0])
            self.play(FlashAround(long_tc[0], time_width=1.5), FlashAround(two_stages, time_width=1.5),
                      run_time=1.8)
            c.wait_until("now it only")
            self.play(*during(disappear(long_tc, long_lab), 0, 0.45),
                      *during(appear(*short2, shift=None), 0.5, 1.0), run_time=1.2)
            self.play(st["arrows"][0].animate(rate_func=there_and_back).set_color(FG).scale(1.12),
                      FlashAround(A[0], time_width=1.5), run_time=min(1.8, c.until()))

        # ---------- clip 5: one nanosecond scale ----------
        with self.say("c6.pipe.5") as c:
            cs = staircase(x0=CX0, top=C_TOP, pitch=C_PITCH, w=CW, h=CH, size=32, guide_top=C_TOP + 0.4)
            stair_boxes = A + B
            top_specs = [("A", 1), ("B", 1), ("A", 2), ("B", 2), ("A", 3)]
            top_row = [stage_box(s, k, CX0 + i * CW, TOP_ROW_Y, CW, CH, 32)
                       for i, (s, k) in enumerate(top_specs)]
            axis = Line([CX0, AXIS_Y, 0], [CX0 + 5 * CW, AXIS_Y, 0]).set_stroke(FG, 2)
            axis_ticks = VGroup(*[Line([CX0 + i * CW, AXIS_Y - 0.12, 0], [CX0 + i * CW, AXIS_Y + 0.12, 0])
                                  .set_stroke(GOLD, 4) for i in range(6)])
            axis_nums = VGroup(*[T(str(5 * i), size=28, color=GOLD).next_to(axis_ticks[i], DOWN, buff=0.1)
                                 for i in range(6)])
            ns = T("ns", size=28, color=DIM).next_to(axis, RIGHT, buff=0.2)
            sweep_clear(self,
                        *[Transform(m, n) for m, n in zip(stair_boxes, cs["A"] + cs["B"])],
                        *[FadeIn(g) for g in cs["guides"]],
                        *[FadeIn(m) for m in top_row],
                        Create(axis), *[FadeIn(t) for t in axis_ticks],
                        keep=stair_boxes, run_time=2.1)
            self.play(*appear(*axis_nums, ns, shift=None, lag=0.05), run_time=0.8)  # early: the axis scale
            c.wait_until("ten")

            tc10 = MathTex("T_c", r"=10\,\text{ns}", font_size=40)
            tc10[0].set_color(YELLOW)
            tc10[1].set_color(GOLD)
            tc10.move_to([RX, 2.65, 0], aligned_edge=LEFT)
            self.play(*appear(tc10, shift=None), run_time=1.0)
            c.wait_until("finishes every ten")
            top_ticks = [finish_tick(CX0 + i * CW, TOP_ROW_Y, CH) for i in (2, 4)]
            self.play(*appear(*top_ticks, shift=0.15 * DOWN, lag=0.4), run_time=1.2)
            every10 = T("1 every 10 ns", size=30).move_to([RX, 2.1, 0], aligned_edge=LEFT)
            self.play(*appear(every10, shift=None), run_time=0.9)
            m100 = T("100 million / s", size=30, color=GOLD).move_to([RX, 1.62, 0], aligned_edge=LEFT)
            c.wait_until(own_word=m100)
            self.play(*appear(m100, shift=None), run_time=0.9)
            c.wait_until("five")

            tc5 = MathTex("T_c", r"=5\,\text{ns}", font_size=40)
            tc5[0].set_color(YELLOW)
            tc5[1].set_color(GOLD)
            tc5.move_to([RX, 0.3, 0], aligned_edge=LEFT)
            self.play(*appear(tc5, shift=None), run_time=1.0)
            c.wait_until("finishes every five")
            bot_ticks = [finish_tick(CX0 + (r + 2) * CW, C_TOP - r * C_PITCH, CH) for r in range(4)]
            self.play(*appear(*bot_ticks, shift=0.15 * DOWN, lag=0.25), run_time=1.2)
            every5 = T("1 every 5 ns", size=30).move_to([RX, -0.2, 0], aligned_edge=LEFT)
            self.play(*appear(every5, shift=None), run_time=0.9)
            m200 = T("200 million / s", size=30, color=GOLD).move_to([RX, -0.68, 0], aligned_edge=LEFT)
            c.wait_until(own_word=m200)
            self.play(*appear(m200, shift=None), run_time=0.9)
            c.wait_until("twice the throughput")
            self.play(FlashAround(m200, time_width=1.5), FlashAround(m100, time_width=1.5), run_time=1.5)
            c.wait_until("latency")

            not2 = [m for m in top_row if m not in (top_row[2], top_row[3])] + \
                   [m for r in (0, 2, 3) for m in (A[r], B[r])]
            tb = span_brace([CX0 + 2 * CW, TOP_ROW_Y + CH / 2, 0], [CX0 + 4 * CW, TOP_ROW_Y + CH / 2, 0],
                            UP, color=GOLD, buff=0.08)
            tb_lab = T("10 ns", size=30, color=GOLD).next_to(tb, UP, buff=0.1)
            bb = span_brace([CX0 + CW, -2.3, 0], [CX0 + 3 * CW, -2.3, 0], DOWN, color=GOLD, buff=0.1)
            bb_lab = T("10 ns", size=30, color=GOLD).next_to(bb, LEFT, buff=0.15)
            self.play(*box_alpha(not2, 0.3), GrowFromCenter(tb), GrowFromCenter(bb),
                      *during(appear(tb_lab, bb_lab, shift=None), 0.5, 1.0), run_time=1.8)
            c.wait_until("untied")

            old_f = T("throughput = 1 / latency", size=30, color=GOLD).move_to([RX, -1.35, 0],
                                                                            aligned_edge=LEFT)
            strike = Line(old_f.get_left() + 0.1 * LEFT, old_f.get_right() + 0.1 * RIGHT).set_stroke(RED, 4)
            self.play(*box_alpha(not2, 1), *appear(old_f, shift=None), run_time=1.0)
            self.play(Create(strike), run_time=0.8)

        # ---------- clip 6: the lecturer's summary ----------
        with self.say("c6.pipe.6") as c:
            c.wait_until("increased the throughput")
            self.play(FlashAround(m200, time_width=1.5), run_time=1.4)
            c.wait_until("also increased the latency")
            self.play(FlashAround(tb_lab, time_width=1.5), FlashAround(bb_lab, time_width=1.5),
                      run_time=1.4)
            c.wait_until("counted in clock periods")

            # right column, in the struck-through formula's place
            head = T("latency", size=32, color=GOLD).move_to([RX, -1.3, 0], aligned_edge=LEFT)
            summ = label_line(T("in periods:  1", size=32), MathTex(r"\rightarrow", font_size=40),
                              T("2", size=32))
            summ.move_to([RX + 0.3, -1.85, 0], aligned_edge=LEFT)
            x2 = MathTex(r"\times\,2", font_size=44, color=GOLD).next_to(summ, RIGHT, buff=0.4)
            self.play(*during(disappear(old_f, strike), 0, 0.45),
                      *during(appear(head, summ, shift=None, lag=0.3), 0.45, 1.0), run_time=1.6)
            c.wait_until("one to two")
            self.play(*appear(x2, shift=None), *recolor(summ[2], GOLD), run_time=1.4)
            c.wait_until("ns")

            in_ns = label_line(T("in ns:  10", size=32), MathTex(r"\rightarrow", font_size=40),
                               T("10  (ideal)", size=32))
            in_ns.move_to([RX + 0.3, -2.4, 0], aligned_edge=LEFT)
            self.play(*appear(in_ns, shift=None), run_time=1.2)  # early: the line is read across the sentence
            real = T("real circuit: a little more", size=28, color=DIM).move_to([RX + 0.3, -2.95, 0],
                                                                             aligned_edge=LEFT)
            c.wait_until(own_word=real)
            self.play(*appear(real, shift=None), run_time=1.0)

        self.wait(2.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
