"""Chapter 6, scene 1: hook: one task at a time through a 10 ns system, the queue grows. Clips c6.hook.1 – c6.hook.3.

Shots: title card -> {last}: ch4 s5's sync_circuit() (button dropped, scale 1.1, centred) with a YELLOW T_c arrow under
its CLK line that stretches, ch5 s5's trial table below it (circuit rises, pair stacked and centred) (3.04 ns row ticked GREEN) -> {now} both
slide off left -> {box}: the chapter's system box, conveyor in/out, four task squares queued left,
GOLD "10 ns" above -> one task in, a progress sweep, out onto the "done" pile, only then the next ->
{queue}: arrivals outpace exits, GOLD "waiting" count -> {fixed}: "10 ns" boxed, tag "fixed" ->
{question}: YELLOW "more tasks per second?" -> ends on the box and its label alone.
Copied as they stand: make_ff()/sync_circuit() (ch4_s5, via ch5_s1). ch5_s5_trial was not built:
the table is drawn from ch5's brief.
"""
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================


# =============================================================================================
# push_button() + make_ff(): copied from ch4_s1_hook.py (Q-bar dropped here: the synchroniser
# uses Q only, as the slide does)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
PUSH = 0.18


def make_ff(center=ORIGIN, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    g = VGroup(d_w, q_w, box, tri, d_l, q_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.d_w, g.q_w, g.clk_w = d_l, q_l, d_w, q_w, clk_w
    g.shift(center)
    clk_w.shift(center)
    return g


def push_button(center=ORIGIN):
    stem = Line(_p(-0.3, 0), _p(-0.58, 0)).set_stroke(FG, 5)
    cap = RoundedRectangle(corner_radius=0.06, width=0.16, height=0.62).set_stroke(FG, 4).set_fill(DIM, 1)
    cap.move_to(_p(-0.66, 0))
    body = RoundedRectangle(corner_radius=0.08, width=0.6, height=0.84).set_stroke(FG, 4).set_fill(BG, 1)
    g = VGroup(stem, cap, body)
    g.stem, g.cap, g.body = stem, cap, body
    g.shift(center)
    g.out = lambda: body.get_right()
    return g


def fingertip():
    f = RoundedRectangle(corner_radius=0.21, width=1.4, height=0.44).set_stroke(FG, 3).set_fill(BG, 1)
    f.move_to(_p(-0.7, 0))
    nail = RoundedRectangle(corner_radius=0.07, width=0.34, height=0.17).set_stroke(FG, 2)
    nail.move_to(_p(-0.27, 0.07))
    return VGroup(f, nail)
# =============================================================================================


# =============================================================================================
# sync_circuit(): the two-flip-flop synchroniser (slide p. 112), top half. s6 / recap copy it.
# =============================================================================================
SK = 0.62                    # flip-flop scale
SFF_X = (-1.7, 2.1)          # FF0, FF1 centres
SFF_Y = 2.244                # box centre (top 3.05)
SBTN_X = -4.3                # button housing centre
SHX = (BOX_W / 2 + WIRE) * SK


def sync_circuit():
    C = VGroup()
    ffs = []
    for x in SFF_X:
        f = make_ff()
        f.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        f.clk_w.scale(SK, about_point=ORIGIN).shift(_p(x, SFF_Y))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.45, about_point=lb.get_center())
        ffs.append(f)
    C.ff0, C.ff1 = ffs
    py = SFF_Y + PIN_Y * SK
    C.py = py
    C.ff0.q_w.set_stroke(TEAL)
    C.ff0.q_l.set_color(TEAL)
    C.ff1.d_w.set_stroke(TEAL)
    C.ff1.d_l.set_color(TEAL)
    C.names = [T(f"FF{i}", 30, FG).move_to(f.box.get_center() + 0.3 * DOWN) for i, f in enumerate(ffs)]
    C.btn = push_button(_p(SBTN_X, py))
    C.d0_w = Line(C.btn.out(), C.ff0.d_w.get_start()).set_stroke(BLUE, 5)
    C.d0_l = MathTex("D_0", font_size=40, color=BLUE).next_to(
        (C.btn.out() + C.ff0.d_w.get_start()) / 2, UP, buff=0.14)
    C.link = Line(C.ff0.q_w.get_end(), C.ff1.d_w.get_start()).set_stroke(TEAL, 5)
    C.d1_l = MathTex("D_1", font_size=40, color=TEAL).next_to(C.link, UP, buff=0.12)
    C.q_l = MathTex("Q", font_size=40, color=GREEN).next_to(C.ff1.q_w.get_end(), RIGHT, buff=0.15)
    by = SFF_Y - (BOX_H / 2 + EN_WIRE) * SK
    C.by = by
    C.bus = Line(_p(-3.2, by), _p(SFF_X[1], by)).set_stroke(YELLOW, 5)
    C.jdot = Dot(_p(SFF_X[0], by), radius=0.08, color=YELLOW)
    C.clk_ws = [f.clk_w for f in ffs]
    C.clk_l = T("CLK", 30, YELLOW).next_to(C.bus.get_start(), LEFT, buff=0.15)
    C.finger = fingertip().shift(C.btn.cap.get_left())
    C.d1_wires = [C.ff0.q_w, C.link, C.ff1.d_w]
    C.all = [C.ff0, C.ff1, *C.names, C.btn, C.d0_w, C.d0_l, C.link, C.d1_l, C.q_l,
             C.bus, C.jdot, *C.clk_ws, C.clk_l]
    C.add(*C.all)
    return C
# =============================================================================================


# =============================================================================================
# trial_table(): ch5 s5's table, from ch5's brief (T_c YELLOW, MTBF GOLD, 3.04 ns row ticked GREEN)
# =============================================================================================
TROWS = [("2.0 ns", "1.4 days", False), ("2.5 ns", "21 days", False),
         ("3.0 ns", "311 days", False), ("3.04 ns", "384 days ≈ 1.05 years", True)]


def trial_table(top=0.0, cx=0.0):
    """Compact (6.6 wide) so it sits beside the synchroniser."""
    G = VGroup()
    x_tc, x_sep, x_mt = -2.55, -1.65, -1.35
    hy = top - 0.25
    G.h_tc = MathTex("T_c", font_size=40, color=FG).move_to(_p(x_tc, hy))
    G.h_mt = T("MTBF", 32, FG).move_to(_p(x_mt, hy), aligned_edge=LEFT)
    G.rule = Line(_p(-3.25, top - 0.6), _p(3.4, top - 0.6)).set_stroke(DIM, 2)
    G.rows, G.marks = [], []
    for i, (tc, mt, ok) in enumerate(TROWS):
        y = top - 1.0 - 0.56 * i
        a = T(tc, 30, YELLOW).move_to(_p(x_tc, y))
        b = T(mt, 30, GOLD).move_to(_p(x_mt, y), aligned_edge=LEFT)
        m = (check_mark(GREEN) if ok else cross_mark(RED)).move_to(_p(3.05, y))
        G.rows.append(VGroup(a, b))
        G.marks.append(m)
    G.sep = Line(_p(x_sep, top - 0.05), _p(x_sep, top - 1.0 - 0.56 * 3 - 0.25)).set_stroke(DIM, 2)
    G.hl = RoundedRectangle(corner_radius=0.1, width=6.7, height=0.5).set_stroke(GREEN, 2)
    G.hl.set_fill(GREEN, 0.15).move_to(_p(0.07, G.rows[3].get_y())).set_z_index(-1)
    G.add(G.h_tc, G.h_mt, G.rule, G.sep, *G.rows, *G.marks, G.hl)
    G.shift(cx * RIGHT)
    return G
# =============================================================================================


# =============================================================================================
# system_hero(): the chapter-wide system box, conveyor and task squares. ch6 s2 / s4 / ch5 recap
# teaser use the same spec: box 4.4 x 1.8, r 0.25, FG stroke 4, no fill, centre (0, 0.3), "the
# system" FG 36 at its centre; task squares side 0.5, r 0.1, fill 0.85, no stroke, colours below.
# =============================================================================================
SYS_C = _p(0, 0.3)
SYS_W, SYS_H = 4.4, 1.8
TASK_COLORS = [BLUE, GREEN, TEAL, FG]
BELT_Y = -0.55                       # conveyor line (just above the box's bottom edge, -0.6)
SQ_Y = BELT_Y + 0.27                 # a square riding on the belt
Q_X0, Q_PITCH = -2.75, 0.7           # queue slot 0 (just left of the box), spacing
IN_X = 0.0                           # a task inside the box, under the label
PILE_X = 5.3                         # the done pile, on the belt's far end


def system_box():
    box = RoundedRectangle(width=SYS_W, height=SYS_H, corner_radius=0.25).set_stroke(FG, 4).set_fill(opacity=0)
    box.move_to(SYS_C)
    label = T("the system", 36, FG).move_to(SYS_C)
    return box, label


def task_square(n):
    """Task n (1-based): BLUE, GREEN, TEAL, FG, repeating."""
    s = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.1).set_stroke(width=0)
    s.set_fill(TASK_COLORS[(n - 1) % 4], 0.85)
    return s


def conveyor():
    left = Line(_p(-6.6, BELT_Y), _p(-SYS_W / 2, BELT_Y)).set_stroke(DIM, 4)
    right = Line(_p(SYS_W / 2, BELT_Y), _p(6.6, BELT_Y)).set_stroke(DIM, 4)
    return left, right


def q_pos(i):
    return _p(Q_X0 - Q_PITCH * i, SQ_Y)


def pile_pos(k):
    return _p(PILE_X, SQ_Y + 0.58 * k)


def progress(frac, color):
    """The progress sweep: fills the box's inside from the left, frac 0..1."""
    w = max(0.001, (SYS_W - 0.2) * frac)
    r = Rectangle(width=w, height=SYS_H - 0.2).set_stroke(width=0).set_fill(color, 0.2)
    r.move_to(SYS_C + (-(SYS_W - 0.2) / 2 + w / 2) * RIGHT).set_z_index(-2)
    return r
# =============================================================================================


def tick(num, new):
    """A counter's digit changes in place half-way through the play: no blank gap, no overlap."""
    def f(m, a):
        if a >= 0.5:
            m.become(new)
    return UpdateFromAlphaFunc(num, f, rate_func=linear)


class Hook(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- clip 1
        with self.say("c6.hook.1", gap=0.6) as c:
            card = title_card("Part 6 · Latency, throughput and pipelining")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            # {last}: the synchroniser, centred and large, its T_c arrow under the CLK line; when the
            # trial table arrives it slides up and the table settles below it (stacked: side by side
            # the pair is already 13.5 wide, so neither could grow there)
            C = sync_circuit()
            C.remove(C.btn)                    # recap copy: two flip-flops on one CLK line, input wire only
            C.scale(1.1).move_to(ORIGIN)
            TB = trial_table(top=0.0, cx=0.0)
            ty = C.bus.get_y() - 0.32
            xa = C.bus.get_start()[0] + 0.2
            tc_arr = DoubleArrow(_p(xa, ty), _p(xa + 1.1, ty), buff=0, stroke_width=3, tip_length=0.16,
                                 max_tip_length_to_length_ratio=0.4, color=YELLOW)
            tc_lab = MathTex("T_c", font_size=44, color=YELLOW).next_to(tc_arr, DOWN, buff=0.1)
            top_h = C.get_top()[1] - tc_lab.get_bottom()[1]
            stack_gap = 0.45
            total = top_h + stack_gap + TB.height
            up0 = -(C.get_top()[1] - top_h / 2)            # alone: the unit centred on y = 0
            for m in (C, tc_arr, tc_lab):
                m.shift(up0 * UP)
            up1 = total / 2 - C.get_top()[1]               # stacked: the pair centred on y = 0
            TB.move_to(_p(0, total / 2 - top_h - stack_gap - TB.height / 2))
            ty += up0
            c.wait_until("last")
            sweep_clear(self, time_span(FadeIn(C), 0.6, 1.4), time_span(FadeIn(tc_arr, tc_lab), 0.8, 1.4),
                        run_time=1.4)

            # "longer clock period": T_c stretches; the circuit rises and the trial table comes in below
            c.wait_until("longer clock period")
            long_arr = DoubleArrow(_p(xa, ty), _p(xa + 2.3, ty), buff=0, stroke_width=3, tip_length=0.16,
                                   max_tip_length_to_length_ratio=0.4, color=YELLOW)
            self.play(Transform(tc_arr, long_arr),
                      tc_lab.animate.move_to(_p(xa + 1.15, tc_lab.get_y())), run_time=1.5)
            first = [TB.h_tc, TB.h_mt, TB.rule, TB.sep]
            for i in range(3):
                first += [*TB.rows[i], TB.marks[i]]
            self.play(*during([m.animate.shift(up1 * UP) for m in (C, tc_arr, tc_lab)], 0, 0.5),
                      *during(appear(*first, lag=0.05, shift=None), 0.45, 1),
                      run_time=min(1.6, c.until("just over three")))  # early: ch5's table, a recap read whole

            # "just over three": the 3.04 ns row, ticked GREEN
            c.wait_until("just over three")
            self.play(FadeIn(TB.hl), *appear(*TB.rows[3], TB.marks[3], lag=0.15, shift=None), run_time=1.2)  # early: recap row, named by "three nanoseconds"

            # {now}: both slide off to the left
            c.wait_until("now")
            self.play(*[m.animate.shift(15 * LEFT) for m in list(self.mobjects)],
                      run_time=min(1.8, c.until(None)), rate_func=smooth)
            self.remove(*list(self.mobjects))

        # ---------------------------------------------------------------- clip 2
        with self.say("c6.hook.2") as c:
            box, label = system_box()
            belt_l, belt_r = conveyor()
            queue = [task_square(n).move_to(q_pos(n - 1)) for n in range(1, 5)]
            # {box}
            self.play(FadeIn(box), *appear(label, shift=None), run_time=1.2)   # whole box, not drawn round
            self.play(Create(belt_l), Create(belt_r),
                      LaggedStart(*[FadeIn(s, shift=0.3 * RIGHT) for s in queue], lag_ratio=0.25), run_time=1.3)
            ten = T("10 ns", 42, GOLD).move_to(_p(0, 1.68))
            c.wait_until("ten nanoseconds")
            self.play(*appear(ten), run_time=1.0)

            # {one}: the first task slides in; the queue steps up
            done_lab = T("done", 30, DIM).move_to(_p(PILE_X, BELT_Y - 0.4))
            pile = []
            p = ValueTracker(0.0)
            cur = {"color": BLUE}
            sweep = progress(0, BLUE)
            sweep.add_updater(lambda m: m.become(progress(p.get_value(), cur["color"])))
            self.add(sweep)

            def enter(sq_list):
                sq = sq_list.pop(0)
                anims = [sq.animate.move_to(_p(IN_X, SQ_Y))]
                anims += [s.animate.move_to(q_pos(i)) for i, s in enumerate(sq_list)]
                return sq, anims

            c.wait_until("one")
            busy, anims = enter(queue)
            self.play(*anims, run_time=1.0)
            cur["color"] = busy.get_fill_color()
            self.play(p.animate.set_value(1.0), run_time=c.until("comes out", floor=1.0), rate_func=linear)

            # "comes out": out on the right, onto the done pile
            self.play(busy.animate.move_to(pile_pos(0)), p.animate.set_value(0.0),
                      *appear(done_lab, shift=None), run_time=1.2)
            pile.append(busy)

            # {next}: only now the second task
            c.wait_until("next")
            busy, anims = enter(queue)
            cur["color"] = busy.get_fill_color()
            self.play(*anims, run_time=1.0)
            self.play(p.animate.set_value(0.8), run_time=c.until("queue", floor=1.0), rate_func=linear)

            # {queue}: arrivals outpace exits; the waiting count ticks up
            n_next = 5
            w_word = T("waiting", 30, GOLD)
            w_num = T(str(len(queue) + 1), 36, GOLD)
            VGroup(w_word, w_num).arrange(RIGHT, buff=0.18).move_to(_p(-4.0, -1.25))

            def count_mob(n):
                return T(str(n), 36, GOLD).move_to(w_num, aligned_edge=LEFT)

            # arrival 1: count appears with it
            s5 = task_square(n_next).move_to(q_pos(len(queue)))
            n_next += 1
            queue.append(s5)
            self.play(FadeIn(s5, shift=0.9 * RIGHT),
                      *appear(w_word, w_num, shift=None), p.animate.set_value(0.9), run_time=1.0, rate_func=linear)
            # arrival 2: count 3 -> 4 (the digit ticks in place as the square lands), the sweep finishes
            s6 = task_square(n_next).move_to(q_pos(len(queue)))
            n_next += 1
            queue.append(s6)
            self.play(FadeIn(s6, shift=0.9 * RIGHT), tick(w_num, count_mob(len(queue))),
                      p.animate.set_value(1.0), run_time=1.0)
            # task 2 out, task 3 in, and two more arrive: 4 -> 5
            self.play(busy.animate.move_to(pile_pos(1)), p.animate.set_value(0.0), run_time=0.8)
            pile.append(busy)
            busy, anims = enter(queue)
            cur["color"] = busy.get_fill_color()
            arr = []
            for _ in range(2):
                s = task_square(n_next).move_to(q_pos(len(queue)))
                n_next += 1
                queue.append(s)
                arr.append(FadeIn(s, shift=0.9 * RIGHT))
            self.play(*anims, *arr, tick(w_num, count_mob(len(queue))), run_time=min(1.2, c.until(None)))

        # ---------------------------------------------------------------- clip 3
        with self.say("c6.hook.3") as c:
            # {fixed}: the 10 ns gets a thin box and the tag "fixed"
            frame = SurroundingRectangle(ten, color=GOLD, buff=0.14).set_stroke(GOLD, 2)
            fixed = T("fixed", 32, GOLD).next_to(frame, RIGHT, buff=0.25)
            # task 3 keeps processing: the sweep advances steadily through the clip, no jump
            p.add_updater(lambda m, dt: m.set_value(min(0.95, m.get_value() + dt / 14)))
            self.add(p)
            self.play(FadeIn(frame, scale=1.15), run_time=1.0)
            c.wait_until(own_word=fixed)
            self.play(*appear(fixed, shift=0.2 * LEFT), run_time=1.0)

            # {question}
            q = T("more tasks per second?", 44, YELLOW).move_to(_p(0, -2.2))
            c.wait_until("question")
            self.play(*appear(q), run_time=1.2)  # early: the question, read as the voice asks it

        # end on the box and its label alone
        sweep.clear_updaters()
        p.clear_updaters()
        self.remove(p)
        # queue, pile, labels, sweep and question go together; the box stays a moment for s2
        self.play(*[FadeOut(m) for m in list(self.mobjects) if m not in (box, label)], run_time=1.0)
        self.wait(1.0)
        self.play(FadeOut(box), FadeOut(label), run_time=1.0)
        self.wait(0.15)
