"""Chapter 7, scene 6: when pipelining can't help (dependencies, stalls; cores + pipelines). Clips c7.limits.1 – c7.limits.3."""
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

DIM_W = 3


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    """Dimension arrow (ch6_s5_pipe): thin double-headed line, same-colour MathTex label."""
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def grow_dim(arr):
    """Grow a dim_arrow's DoubleArrow from its centre at the true tip size (ch6_s5_pipe)."""
    start, end = arr.get_start(), arr.get_end()
    mid, half = (start + end) / 2, (end - start) / 2
    final = arr.copy()

    def upd(m, a):
        if a >= 1:
            m.become(final)
            return
        if a * np.linalg.norm(end - start) < 0.4:
            m.become(final).set_opacity(0)
            return
        m.become(DoubleArrow(mid - a * half, mid + a * half, buff=0, stroke_width=DIM_W,
                             tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                             color=final.get_color()))

    return UpdateFromAlphaFunc(arr, upd, rate_func=smooth)


# ============================================================================
# ch6 staircase block (copied from ch6_s5_pipe, unchanged)
TASK_COLORS = {1: BLUE, 2: GREEN, 3: TEAL, 4: FG}
PERIOD = 3.4
X0 = -1.5 * PERIOD                 # -5.1
STAGE_W = PERIOD / 2               # 1.7
STAGE_H = 0.9
STAIR_X0 = X0
STAIR_TOP_Y = 1.75
STAIR_PITCH = 1.3
STAIR_ARROW_Y = 2.65
STAIR_N = 4


def stage_box(stage, task, x_left, y, width=STAGE_W, height=STAGE_H, size=40):
    col = TASK_COLORS[task]
    rect = Rectangle(width=width, height=height).set_stroke(col, 3).set_fill(col, 0.18)
    rect.move_to([x_left + width / 2, y, 0])
    lab = MathTex(f"{stage}_{task}", font_size=size, color=col).move_to(rect)
    return VGroup(rect, lab)


def stair_y(row, top=STAIR_TOP_Y, pitch=STAIR_PITCH):
    return top - row * pitch


def stair_x(col, x0=STAIR_X0, w=STAGE_W):
    return x0 + col * w


def staircase(x0=STAIR_X0, top=STAIR_TOP_Y, pitch=STAIR_PITCH, w=STAGE_W, h=STAGE_H, size=40,
              n=STAIR_N, arrow_y=STAIR_ARROW_Y, guide_top=None):
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


def box_alpha(boxes, op):
    anims = []
    for b in boxes:
        t = b.copy()
        t[0].set_stroke(opacity=op).set_fill(opacity=0.18 * op)
        t[1].set_opacity(op)
        anims.append(Transform(b, t))
    return anims
# ============================================================================

DY = 0.6                          # the staircase drops this much to make room for the slide quote
STRAIGHT_Y = 0.6                   # the one-at-a-time row of clip 2


def to_slot(box, col, y):
    return box.animate.move_to([stair_x(col) + STAGE_W / 2, y, 0])


def dep_wire(xb_right, yb, xa_left, ya):
    """YELLOW routed wire from B1's right end down, then along to A2's left end, with a tip."""
    ym = (yb + ya) / 2
    px, qx = xb_right + 0.12, xa_left - 0.27
    path = VMobject().set_points_as_corners([[px - 0.12, yb, 0], [px, yb, 0], [px, ym, 0], [qx, ym, 0],
                                             [qx, ya, 0], [xa_left - 0.16, ya, 0]])
    path.set_stroke(YELLOW, 4)
    tip = Triangle().set_stroke(width=0).set_fill(YELLOW, 1).scale(0.11).rotate(-PI / 2)
    tip.move_to([xa_left - 0.1, ya, 0])
    return VGroup(path, tip)


def tiny_stair(center, s=0.30):
    """The staircase as plain coloured rects, scaled by s, centred at center."""
    g = VGroup()
    for r in range(STAIR_N):
        for col in (r, r + 1):
            col_c = TASK_COLORS[r + 1]
            g.add(Rectangle(width=STAGE_W, height=STAGE_H).set_stroke(col_c, 3).set_fill(col_c, 0.18)
                  .move_to([stair_x(col) + STAGE_W / 2, stair_y(r), 0]))
    g.move_to(ORIGIN).scale(s).move_to(center)
    for m in g:
        m.set_stroke(width=2)
    return g


class PipelineLimits(NarratedScene):
    def construct(self):
        st = staircase()
        A, B = st["A"], st["B"]
        rows = [[A[r], B[r]] for r in range(STAIR_N)]

        # ---------------- clip 1: the dependency and the stall ----------------
        with self.say("c7.limits.1") as c:
            self.play(*[FadeIn(g) for g in st["guides"]], *[grow_dim(t[0]) for t in st["arrows"]],
                      *appear(*[t[1] for t in st["arrows"]], shift=None, lag=0.1),  # early: the staircase returns whole
                      run_time=1.0)
            cols = [[A[0]], [B[0], A[1]], [B[1], A[2]], [B[2], A[3]], [B[3]]]
            self.play(*[time_span(FadeIn(b), 0.3 * i, 0.3 * i + 0.8) for i, grp in enumerate(cols) for b in grp],
                      run_time=2.0)
            c.wait_until("within")

            y0 = stair_y(0)
            within = Arrow([stair_x(0) + 1.15, y0, 0], [stair_x(1) + 0.55, y0, 0], buff=0,
                           stroke_width=5, tip_length=0.2, color=GREEN)
            within_lab = set_backstroke(T("earlier step of the same task", 30, GREEN), width=8)
            within_lab.move_to([stair_x(2) + 0.4, y0, 0], aligned_edge=LEFT)
            self.play(GrowArrow(within), run_time=1.2)
            self.play(*appear(within_lab, shift=None), run_time=1.0)  # early: paraphrases "its own first stage"
            c.wait_until("fine")
            ok = check_mark().next_to(within_lab, RIGHT, buff=0.35)
            self.play(*appear(ok, shift=None), run_time=0.8)
            c.wait_until("depend")

            quote = T("“If a current task is dependent on the result of a prior task,\n"
                      "rather than just prior steps in the current task, the task cannot\n"
                      "start until the prior task has completed.”", 28, line_spacing=0.8)
            quote.move_to([0, 2.8, 0])
            moving = [m for r in rows for m in r] + [within]
            self.play(*during(disappear(*st["guides"], *st["arrows"], within_lab, ok), 0, 0.45),
                      *during([m.animate.shift(DY * DOWN) for m in moving], 0.3, 0.8),
                      *during(appear(quote, shift=None), 0.55, 1.0),  # early: the slide's sentence, quoted whole
                      run_time=2.0)
            c.wait_until("task two")

            def wire_now():
                return dep_wire(B[0][0].get_right()[0], B[0].get_y(), A[1][0].get_left()[0], A[1].get_y())

            wire = wire_now()
            dep_lab = T("task 2 needs task 1's result", 30, YELLOW)
            dep_lab.move_to([stair_x(2) + 0.4, B[0].get_y(), 0], aligned_edge=LEFT)
            self.play(Create(wire[0]), *during([FadeIn(wire[1])], 0.8, 1.0), run_time=1.5)
            self.play(*appear(dep_lab, shift=None), run_time=1.0)
            c.wait_until("wait")

            later = [m for r in rows[1:] for m in r]
            self.play(*[m.animate.shift(STAGE_W * RIGHT) for m in later],
                      UpdateFromAlphaFunc(wire, lambda m, a: m.become(wire_now())), run_time=2.0)
            c.wait_until("stall")

            stall_box = DashedVMobject(Rectangle(width=STAGE_W, height=STAGE_H), num_dashes=24)
            stall_box.set_stroke(RED, 3).move_to([stair_x(1) + STAGE_W / 2, A[1].get_y(), 0])
            stall_lab = T("stall", 30, RED).move_to(stall_box).shift(0.12 * LEFT)
            self.play(FadeIn(stall_box), run_time=1.0)
            c.wait_until(own_word=stall_lab)
            self.play(*appear(stall_lab, shift=None), run_time=0.8)

        # ---------------- clip 2: processors, and the worst case ----------------
        with self.say("c7.limits.2") as c:
            self.play(*box_alpha([m for r in rows[2:] for m in r], 0.3), run_time=1.0)
            c.wait_until("adds")
            add_tag = T("add", 32, BLUE).move_to([stair_x(0) - 0.2, A[0].get_y(), 0], aligned_edge=RIGHT)
            self.play(*appear(add_tag, shift=None), run_time=1.0)
            c.wait_until("next one needs")
            use_tag = T("use the sum", 32, GREEN).move_to([stair_x(1) - 0.15, A[1].get_y(), 0],
                                                         aligned_edge=RIGHT)
            self.play(*appear(use_tag, shift=None), run_time=1.0)
            c.wait_until("has to wait")
            self.play(FlashAround(stall_box, color=RED, time_width=1.5), run_time=1.5)
            c.wait_until("every")

            # straighten into the one-at-a-time row: A1 B1 A2 B2 A3 B3
            self.play(*during(disappear(quote, add_tag, use_tag, dep_lab, wire, stall_box, stall_lab,
                                        within, *rows[3]), 0, 0.45),
                      *box_alpha(rows[2], 1), run_time=1.0)
            # task 3 first slides along its own row into the free slot (cols 4-5), so every pair then
            # rises straight up in its own columns: nothing passes through anything
            self.play(*[to_slot(m, 4 + k, m.get_y()) for k, m in enumerate(rows[2])], run_time=0.9)
            self.play(*[to_slot(m, 2 * r + k, STRAIGHT_Y) for r in range(3) for k, m in enumerate(rows[r])],
                      run_time=1.2)
            per = []
            for i in range(6):
                xa, xb = stair_x(i) + 0.05, stair_x(i + 1) - 0.05
                arr = DoubleArrow([xa, STRAIGHT_Y + 0.85, 0], [xb, STRAIGHT_Y + 0.85, 0], buff=0,
                                  stroke_width=DIM_W, tip_length=0.16, max_tip_length_to_length_ratio=0.4,
                                  color=YELLOW)
                lab = T("6.5 ns", 30, GOLD).next_to(arr, UP, buff=0.15)
                per.append((arr, lab))
            self.play(*[grow_dim(a) for a, _ in per],
                      *appear(*[lab for _, lab in per], shift=None, lag=0.1), run_time=1.2)
            c.wait_until("thirteen")

            form = T("one task per 2 × 6.5 = 13 ns", 40, GOLD)
            form.move_to([stair_x(0), STRAIGHT_Y - 1.35, 0], aligned_edge=LEFT)
            self.play(*appear(form, shift=None), run_time=1.2)
            c.wait_until("worse")

            twelve = T("12 ns", 40, GOLD).move_to([4.3, form.get_y(), 0])
            twelve.align_to(form, DOWN)
            self.play(*appear(twelve, shift=None), run_time=1.0)
            self.play(*recolor(select(form, "13")[0], RED), run_time=0.8)
            nopipe = T("no pipeline", 30, DIM).next_to(twelve, DOWN, buff=0.25)
            c.wait_until(own_word=nopipe)
            self.play(*appear(nopipe, shift=None), run_time=0.8)
            c.wait_until("measures")

            tag = T("processors: special measures", 30, DIM).move_to([0, STRAIGHT_Y - 2.85, 0])
            self.play(*appear(tag, shift=None), run_time=1.0)

        # ---------------- clip 3: still essential; cores + pipelines ----------------
        with self.say("c7.limits.3") as c:
            c.wait_until("important")
            st2 = staircase()
            self.play(*during(disappear(form, twelve, nopipe, tag, *[a for a, _ in per], *[l for _, l in per]),
                              0, 0.4),
                      *during([m.animate.set_y(stair_y(r)) for r in range(3) for m in rows[r]], 0.4, 1.0),
                      run_time=1.5)
            rows[3] = [st2["A"][3], st2["B"][3]]
            self.play(*[to_slot(m, r + k, stair_y(r)) for r in (1, 2) for k, m in enumerate(rows[r])],
                      *during(appear(*rows[3], shift=None), 0.5, 1.0),
                      *during([FadeIn(g) for g in st2["guides"]], 0.3, 1.0),
                      run_time=min(1.8, c.until("cores")))
            c.wait_until("cores")

            # chip with four cores, each holding a tiny staircase
            chip_c = np.array([0, 0.75, 0])
            chip = RoundedRectangle(corner_radius=0.25, width=7.6, height=4.4).set_stroke(FG, 3).move_to(chip_c)
            pins = VGroup()
            for k in range(9):
                x = -3.2 + k * 0.8
                pins.add(Line([x, chip.get_top()[1], 0], [x, chip.get_top()[1] + 0.25, 0]))
                pins.add(Line([x, chip.get_bottom()[1], 0], [x, chip.get_bottom()[1] - 0.25, 0]))
            pins.set_stroke(DIM, 3)
            centres = [chip_c + np.array([sx * 1.8, sy * 1.05, 0]) for sy in (1, -1) for sx in (-1, 1)]
            cores = [Rectangle(width=3.3, height=1.8).set_stroke(DIM, 2).move_to(p) for p in centres]
            minis = [tiny_stair(p) for p in centres]
            boxes = [m for r in rows for m in r]
            # box order in tiny_stair: A1 B1 A2 B2 ...
            targets = []
            for i, b in enumerate(boxes):
                t = b.copy()
                t[0].become(minis[0][i])
                t[1].scale(0.3).move_to(minis[0][i]).set_opacity(0)
                targets.append(t)
            self.play(*during(disappear(*st2["guides"]), 0, 0.4),
                      *during([Transform(b, t) for b, t in zip(boxes, targets)], 0.2, 0.85),
                      *during([FadeIn(chip), FadeIn(pins), *[FadeIn(k) for k in cores]], 0.5, 1.0),
                      *during([FadeIn(m) for m in minis[1:]], 0.6, 1.0),
                      run_time=2.2)
            self.remove(*[m for b in boxes for m in b.get_family()])
            self.add(minis[0])
            c.wait_until("spatial")

            LX = -1.3
            sp_desc = T("several cores", 36).move_to([LX + 0.25, -2.25, 0], aligned_edge=LEFT)
            sp_tag = T("spatial:", 36, BLUE).move_to([LX, -2.25, 0], aligned_edge=RIGHT)
            sp_tag.align_to(sp_desc, DOWN)
            self.play(*[FlashAround(k, time_width=1.5, color=YELLOW) for k in cores],
                      *during(appear(sp_desc, shift=None), 0.3, 1.0), run_time=1.5)
            c.wait_until(own_word=sp_tag)
            self.play(*appear(sp_tag, shift=None), run_time=0.8)
            c.wait_until("temporal")

            tp_desc = T("each core pipelined", 36).move_to([LX + 0.25, -3.0, 0], aligned_edge=LEFT)
            tp_tag = T("temporal:", 36, BLUE).move_to([LX, -3.0, 0], aligned_edge=RIGHT)
            tp_tag.align_to(tp_desc, DOWN)
            self.play(FlashAround(minis[0], time_width=1.5, color=YELLOW),
                      *during(appear(tp_desc, shift=None), 0.3, 1.0), run_time=1.5)
            c.wait_until(own_word=tp_tag)
            self.play(*appear(tp_tag, shift=None), run_time=0.8)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
