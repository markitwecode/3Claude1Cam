"""Chapter 6, scene 2: latency and throughput. Clips c6.speed.1 – c6.speed.3."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

DIM_W = 3                 # dimension arrows (as ch1_s5_datasheet)
BOX_C = np.array([0, 0.3, 0])
LANE = -0.15              # y of the lane tokens travel along inside the box (clip 2)
WATCH_Y = -1.15           # the stopwatch rides below the box
TASK_COLS = [BLUE, GREEN, TEAL, FG]


def system_box():
    box = RoundedRectangle(width=4.4, height=1.8, corner_radius=0.25).set_stroke(FG, 4).set_fill(opacity=0)
    box.move_to(BOX_C)
    lab = T("the system", 36).move_to(box)
    return box, lab


def task_square(i):
    return RoundedRectangle(width=0.5, height=0.5, corner_radius=0.1).set_stroke(width=0) \
        .set_fill(TASK_COLS[i], 0.85)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)


def grow_dim(arr):
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


# ===================== recap helpers (r1 tile; s5 brings the formula back) =====================
def make_stopwatch(center=ORIGIN):
    """Small stopwatch: FG face r 0.3, crown on top, GOLD hand pointing up. .face .hand"""
    face = Circle(radius=0.3).set_stroke(FG, 3).set_fill(BG, 1)
    stem = Line(face.get_top(), face.get_top() + 0.1 * UP).set_stroke(FG, 3)
    crown = RoundedRectangle(width=0.18, height=0.08, corner_radius=0.03).set_stroke(FG, 2) \
        .set_fill(FG, 1).next_to(stem, UP, buff=0)
    hand = Line(ORIGIN, 0.22 * UP).set_stroke(GOLD, 3)
    w = VGroup(face, stem, crown, hand)
    w.face, w.hand = face, hand
    w.shift(np.array(center) - face.get_center())
    return w


def set_watch(w, center, frac):
    """Put the stopwatch's face at center with the hand turned frac of a full turn."""
    c = np.array(center, dtype=float)
    w.shift(c - w.face.get_center())
    th = TAU * frac
    w.hand.put_start_and_end_on(c, c + 0.22 * np.array([np.sin(th), np.cos(th), 0]))


def tally_mark(i, origin=(3.4, WATCH_Y)):
    """The i-th GOLD tally stroke (0.5 tall) of the exit counter."""
    x, y = origin[0] + 0.25 * i, origin[1]
    return Line([x, y - 0.25, 0], [x, y + 0.25, 0]).set_stroke(GOLD, 5)


def make_formula():
    """GOLD 'throughput = 1 / latency' with the DIM tag 'for this box' under it."""
    f = T("throughput = 1 / latency", 40, color=GOLD)
    tag = T("for this box", 30, color=DIM).next_to(f, DOWN, buff=0.22)
    return f, tag
# ==============================================================================================


def card(text, x, y):
    t = T(text, 32)
    r = RoundedRectangle(width=4.6, height=0.85, corner_radius=0.15).set_stroke(DIM, 2).set_fill(opacity=0)
    g = VGroup(r, t).move_to([x, y, 0])
    return g, t


class LatencyThroughput(NarratedScene):
    def construct(self):
        box, sys_lab = system_box()
        queue = [task_square(i).move_to([-2.9 - 0.7 * i, BOX_C[1], 0]) for i in range(3)]

        # ---------------- clip 1: tokens and tasks ----------------
        with self.say("c6.speed.1") as c:
            self.play(FadeIn(box), FadeIn(sys_lab), run_time=1.0)  # early: s1's end shot fades back in
            c.wait_until("the slides")
            self.play(*appear(*queue, shift=0.25 * RIGHT, lag=0.25), run_time=1.2)
            c.wait_until("token")

            # one square zooms up below the box and opens into a bundle
            big = RoundedRectangle(width=1.0, height=1.0, corner_radius=0.2).set_stroke(width=0) \
                .set_fill(BLUE, 0.85).move_to([0, -1.9, 0])
            self.play(ReplacementTransform(queue[0].copy(), big), run_time=1.2)
            in1 = Line([-1.7, -1.7, 0], [-0.5, -1.7, 0]).set_stroke(BLUE, 5)
            in2 = Line([-1.7, -2.1, 0], [-0.5, -2.1, 0]).set_stroke(BLUE, 5)
            out = Line([0.5, -1.9, 0], [1.7, -1.9, 0]).set_stroke(GREEN, 5)
            self.play(Create(in1), Create(in2), Create(out), run_time=0.8)
            defn = T("token: a group of inputs that are processed\nto produce a group of outputs", 32,
                     t2c={"token:": YELLOW}).move_to([0, -3.15, 0])
            self.play(*appear(defn), run_time=1.0)
            c.wait_until("pairs of numbers")

            n3 = T("3", 42, color=GOLD).next_to(in1.get_start(), LEFT, buff=0.2)
            n4 = T("4", 42, color=GOLD).next_to(in2.get_start(), LEFT, buff=0.2)
            self.play(*appear(n3, n4, shift=0.25 * RIGHT, lag=0.3), run_time=1.0)
            c.wait_until("its sum")
            n7 = T("7", 42, color=GOLD).next_to(out.get_end(), RIGHT, buff=0.2)
            self.play(*appear(n7, shift=0.25 * RIGHT), run_time=1.0)
            c.wait_until("task")
            # the bundle shrinks back into its square, which then gets the tag
            home = queue[0].copy()
            tag = label_pointer("task =\nprocessing one token", queue[0], direction=DOWN,
                                color=FG, size=30, length=0.5)
            self.play(*during([ReplacementTransform(big, home)], 0, 0.55),
                      *during(disappear(in1, in2, out, n3, n4, n7, defn), 0, 0.5),
                      *during(appear(tag, shift=None), 0.55, 1), run_time=1.6)
            self.remove(home)

        # ---------------- clip 2: latency and throughput ----------------
        with self.say("c6.speed.2") as c:
            lat = T("latency", 40, color=YELLOW).move_to([0, 1.85, 0])
            self.play(sys_lab.animate.move_to(BOX_C + 0.5 * UP),
                      *[sq.animate.set_y(LANE) for sq in queue],
                      tag.animate.shift((LANE - BOX_C[1]) * UP), run_time=0.8)
            self.play(*appear(lat), run_time=1.0)
            c.wait_until("from start")

            watch = make_stopwatch([-2.2, WATCH_Y, 0])
            c.wait_until("watch")
            self.play(*during(disappear(tag), 0, 0.4),
                      *during([queue[0].animate.move_to([-2.2, LANE, 0])], 0.3, 0.8),
                      *during(appear(watch, shift=None), 0.6, 1), run_time=1.3)

            x0, x1 = -2.2, 2.2

            def ride(m, a):
                x = x0 + a * (x1 - x0)
                m.move_to([x, LANE, 0])
                set_watch(watch, [x, WATCH_Y, 0], 0.85 * a)

            self.play(UpdateFromAlphaFunc(queue[0], ride, rate_func=linear), run_time=2.2)
            dim = dim_arrow(-2.2, 2.2, -1.95, GOLD, r"10\,\mathrm{ns}", label_dir=DOWN)
            self.play(grow_dim(dim[0]), *appear(dim[1]), run_time=0.9)
            c.wait_until("throughput")

            thr = T("throughput", 40, color=YELLOW).move_to([4.3, 0.95, 0])
            self.play(*appear(thr), run_time=1.0)
            c.wait_until("count")

            # stand at the exit and count
            pile = [[3.0 + 0.65 * i, LANE, 0] for i in range(3)]
            marks = [tally_mark(i) for i in range(3)]
            self.play(queue[0].animate.move_to(pile[0]), time_span(FadeIn(marks[0]), 0.4, 0.8),
                      run_time=0.8)
            for i in (1, 2):
                self.play(queue[i].animate(rate_func=linear).move_to(pile[i]),
                          time_span(FadeIn(marks[i]), 0.75, 1.05), run_time=1.05)
            c.wait_until("one token every")
            rate = T("1 every 10 ns = 100 million per second", 36, color=GOLD).move_to([0, -2.95, 0])
            self.play(*appear(rate), run_time=1.0)

        # ---------------- clip 3: two questions, tied, parallelism ----------------
        with self.say("c6.speed.3") as c:
            gone = [watch, dim, *queue, *marks, lat, thr]
            self.play(*during(disappear(*gone), 0, 0.45),
                      *during([box.animate.shift(0.6 * UP), sys_lab.animate.shift(0.6 * UP)], 0.3, 1),
                      run_time=1.4)
            c.wait_until("mine")

            lat2 = T("latency", 40, color=YELLOW).move_to([-3.5, -0.5, 0])
            card1, _ = card("How long for mine?", -3.5, -1.35)
            self.play(*appear(lat2, card1, lag=0.3), run_time=1.2)
            c.wait_until("many")
            thr2 = T("throughput", 40, color=YELLOW).move_to([3.5, -0.5, 0])
            card2, _ = card("How many per second?", 3.5, -1.35)
            self.play(*appear(thr2, card2, lag=0.3), run_time=1.2)
            c.wait_until("tied")

            formula, ftag = make_formula()
            VGroup(formula, ftag).move_to([0, -2.75, 0])
            self.play(*swap(rate, formula), *during(appear(ftag), 0.7, 1), run_time=1.5)
            c.wait_until("several tokens")

            # several tokens at once inside the box
            self.play(*during(disappear(lat2, card1, thr2, card2, formula, ftag), 0, 0.45),
                      *during([box.animate.move_to([0, -1.6, 0]),
                               sys_lab.animate.move_to([0, -1.1, 0])], 0.35, 1),
                      run_time=1.4)
            inside = [task_square(i).move_to([-0.8 + 0.8 * i, -2.0, 0]) for i in range(3)]
            c.wait_until("same time")
            self.play(*[FadeIn(s, scale=0.6) for s in inside], run_time=0.8)
            c.wait_until("parallelism")

            par = T("parallelism", 48, color=BLUE).move_to([0, 2.6, 0])
            self.play(*appear(par), run_time=0.8)
            c.wait_until("two types")
            slots, nums, legs = [], [], []
            for k, x in enumerate((-2.3, 2.3)):
                s = DashedVMobject(RoundedRectangle(width=3.6, height=1.4, corner_radius=0.2),
                                   num_dashes=40).set_stroke(BLUE, 3).move_to([x, 0.9, 0])
                slots.append(s)
                nums.append(T(str(k + 1), 36, color=DIM).move_to(s))
                legs.append(Line(par.get_bottom() + 0.12 * DOWN + 0.4 * x / 2.3 * RIGHT,
                                 s.get_top() + 0.08 * UP).set_stroke(DIM, 3))
            self.play(*[Create(l) for l in legs],
                      *[time_span(GrowFromPoint(s, par.get_bottom()), 0.2, 1.1) for s in slots],
                      *[time_span(FadeIn(n), 0.7, 1.2) for n in nums], run_time=1.2)

        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
