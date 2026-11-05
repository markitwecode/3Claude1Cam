"""Chapter 2, scene 4: Example 29, expand (cos θ + i sin θ)^4. Clips c2.exp.1 – c2.exp.4."""
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

HAND = "Bradley Hand"          # the lecturer's handwritten fills
LINE1_POS = np.array([-0.6, 1.7, 0])
EXP_Y = 0.5                    # the five-term line (then its substituted form)
COL_Y = -1.1                   # the collected line
DIAL_C = np.array([3.7, -0.9, 0])
DIAL_C2 = np.array([4.4, -1.95, 0])
PASCAL_TOP = np.array([4.3, 0.3, 0])


def split_mt(parts, size):
    """Like mt, but each part is its own MathTex (so one part can be the source of a fly)."""
    m = mt(parts, size)
    return VGroup(*[MathTex(p, font_size=size, color=col).move_to(sub) for sub, (p, col) in zip(m, parts)])


def fly_lin(src, dst):
    """fly() at constant speed: a long same-text flight leaves its source before the copy shows."""
    anims = fly(src, dst)
    for a in anims:
        a.rate_func = linear
    return anims


def mt(parts, size=40):
    """MathTex from (tex, colour) pairs; one submobject per pair."""
    m = MathTex(*[p for p, _ in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        sub.set_color(col)
    return m


# ---------------------------------------------------------------- shared pieces
def pascal_rows(top=PASCAL_TOP, size=44, dx=0.85, dy=0.7):
    """Pascal's triangle rows 0-4 (row 4 '1 4 6 4 1' GOLD); top row centred at `top`."""
    from math import comb
    rows = VGroup()
    for n in range(5):
        row = VGroup(*[MathTex(str(comb(n, j)), font_size=size, color=GOLD if n == 4 else FG)
                       for j in range(n + 1)])
        for j, num in enumerate(row):
            num.move_to(top + np.array([(j - n / 2) * dx, -n * dy, 0]))
        rows.add(row)
    return rows


def i_dial(center=DIAL_C, r=1.25, size=40):
    """The unit circle with a PINK dot for i; positions 1, i, -1, -i with their values.
    .pts[k] = position of i^k (k mod 4), .dot, .marks[k], .lbls[k] (k = 1..4)."""
    center = np.array(center, dtype=float)
    circle = Circle(radius=r, color=DIM, stroke_width=3).move_to(center)
    axes = VGroup(Line(center + LEFT * (r + 0.25), center + RIGHT * (r + 0.25)),
                  Line(center + DOWN * (r + 0.25), center + UP * (r + 0.25))).set_stroke(DIM, 2, opacity=0.6)
    pts = [center + r * np.array([np.cos(a), np.sin(a), 0]) for a in (0, PI / 2, PI, 3 * PI / 2)]
    l1 = MathTex("i", font_size=size, color=PINK).next_to(pts[1], UP, buff=0.35)
    l2 = split_mt([("i^2", PINK), ("=", FG), ("-1", BLUE)], size).next_to(pts[2], LEFT, buff=0.4)
    l3 = split_mt([("i^3", PINK), ("=", FG), ("-i", PINK)], size).next_to(pts[3], DOWN, buff=0.35)
    l4 = split_mt([("i^4", PINK), ("=", FG), ("1", BLUE)], size).next_to(pts[0], RIGHT, buff=0.4)
    marks = [Dot(p, radius=0.07, color=PINK).set_opacity(0.55) for p in pts]
    dot = Dot(pts[1], radius=0.11, color=PINK)
    g = VGroup(axes, circle, *marks, dot, l1, l2, l3, l4)
    g.center_pt, g.r, g.pts, g.dot, g.axes, g.circle = center, r, pts, dot, axes, circle
    g.marks = {4: marks[0], 1: marks[1], 2: marks[2], 3: marks[3]}
    g.lbls = {1: l1, 2: l2, 3: l3, 4: l4}
    return g


def make_line1():
    """cos 4θ + i sin 4θ = (cos θ + i sin θ)^4 (cos BLUE, i sin PINK, the 4s GOLD)."""
    L = mt([(r"\cos", BLUE), ("4", GOLD), (r"\theta", BLUE), ("+", FG), (r"i\sin", PINK), ("4", GOLD),
            (r"\theta", PINK), ("=", FG), ("(", FG), (r"\cos\theta", BLUE), ("+", FG),
            (r"i\sin\theta", PINK), (")", FG), ("^4", GOLD)], 56)
    return L.move_to(LINE1_POS)


def make_E():
    """The notes' five-term expansion (coefficients GOLD, i PINK)."""
    E = mt([("=", FG), (r"\cos^4\theta", FG), ("+", FG), ("4", GOLD), ("i", PINK),
            (r"\cos^3\theta\sin\theta", FG), ("+", FG), ("6", GOLD), ("i^2", PINK),
            (r"\cos^2\theta\sin^2\theta", FG), ("+", FG), ("4", GOLD), ("i^3", PINK),
            (r"\cos\theta\sin^3\theta", FG), ("+", FG), ("i^4", PINK), (r"\sin^4\theta", FG)], 42)
    return E.move_to([0, EXP_Y, 0])


def make_S(red=False):
    """The expansion with the powers of i put in; real terms BLUE, imaginary PINK."""
    m1, m2 = (RED, RED) if red else (BLUE, PINK)
    S = mt([("=", FG), (r"\cos^4\theta", BLUE), ("+", FG), ("4", PINK), ("i", PINK),
            (r"\cos^3\theta\sin\theta", PINK), ("-", m1), ("6", BLUE),
            (r"\cos^2\theta\sin^2\theta", BLUE), ("-", m2), ("4", PINK), ("i", PINK),
            (r"\cos\theta\sin^3\theta", PINK), ("+", FG), (r"\sin^4\theta", BLUE)], 42)
    S.move_to([0, EXP_Y, 0]).align_to(make_E(), LEFT)
    return S


def make_C():
    """The collected line: real group BLUE, imaginary group PINK."""
    C = mt([("=", FG), (r"\cos^4\theta", BLUE), ("-", BLUE), ("6", BLUE), (r"\cos^2\theta\sin^2\theta", BLUE),
            ("+", BLUE), (r"\sin^4\theta", BLUE), ("+", FG), ("4i", PINK), ("(", PINK),
            (r"\cos^3\theta\sin\theta", PINK), ("-", PINK), (r"\cos\theta\sin^3\theta", PINK), (")", PINK)], 42)
    C.move_to([0, COL_Y, 0]).align_to(make_E(), LEFT)
    return C


def make_braces(C):
    br_r = Brace(VGroup(*C[1:7]), DOWN, buff=0.15, color=BLUE)
    br_i = Brace(VGroup(*C[8:14]), DOWN, buff=0.15, color=PINK)
    lr = T("real", 34, BLUE).next_to(br_r, DOWN, buff=0.12)
    li = T("imaginary", 34, PINK).next_to(br_i, DOWN, buff=0.12)
    return br_r, lr, br_i, li


def handover_shot():
    """The last frame: line 1, the substituted expansion, the collected line and its braces."""
    C = make_C()
    return VGroup(make_line1(), make_S(), C, *make_braces(C))


def make_task():
    head = T("Example 29: De Moivre's theorem", 38, weight=BOLD)
    b1 = T("Use De Moivre's Theorem to determine expressions", 34)
    b2 = VGroup(T("for", 34), MathTex(r"\cos 4\theta", font_size=40), T("and", 34),
                MathTex(r"\sin 4\theta", font_size=40)).arrange(RIGHT, buff=0.2)
    for w in (b2[0], b2[2]):          # sit the words on the formulas' baseline
        w.align_to(b2[1], DOWN)
    hand = Text("in terms of cos θ and sin θ.", font=HAND, font_size=38, color=YELLOW)
    body = VGroup(b1, b2, hand).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    W = max(head.width, body.width) + 1.0
    band = Rectangle(width=W, height=head.height + 0.45).set_fill(GREEN, 0.22).set_stroke(GREEN, 0)
    head.move_to(band)
    body.next_to(band, DOWN, buff=0.35).align_to(band, LEFT).shift(0.5 * RIGHT)
    frame = Rectangle(width=W, height=band.height + body.height + 0.75).set_stroke(GREEN, 3)
    frame.align_to(band, UP)
    g = VGroup(frame, band, head, b1, b2, hand)
    g.frame, g.band, g.head, g.b1, g.b2, g.hand = frame, band, head, b1, b2, hand
    return g


def make_slots():
    """Five slots: (coefficient, cos part, i-sin part); coefficient right edges in one column."""
    specs = [
        [("1", GOLD), (r"\cos^4\theta", BLUE)],
        [("4", GOLD), (r"\cos^3\theta", BLUE), (r"(i\sin\theta)", PINK)],
        [("6", GOLD), (r"\cos^2\theta", BLUE), (r"(i\sin\theta)^2", PINK)],
        [("4", GOLD), (r"\cos\theta", BLUE), (r"(i\sin\theta)^3", PINK)],
        [("1", GOLD), (r"(i\sin\theta)^4", PINK)],
    ]
    slots = []
    for k, spec in enumerate(specs):
        s = mt(spec, 52)
        s.shift(np.array([-5.6 - s[0].get_right()[0], 0.75 - 0.95 * k - s[0].get_center()[1], 0]))
        coef = s[0]
        cos = s[1] if k < 4 else None
        ip = s[-1] if k > 0 else None
        slots.append((coef, cos, ip))
    return slots


class Expand(NarratedScene):
    def construct(self):
        # ------------------------------------------------------------ c2.exp.1
        with self.say("c2.exp.1") as c:
            task = make_task().move_to(UP * 0.9)
            self.play(*appear(VGroup(task.frame, task.band, task.head), shift=None), run_time=1.2)
            c.wait_until("goal")
            self.play(*appear(task.b1, task.b2, lag=0.5), run_time=min(1.8, c.until("in terms of")))
            c.wait_until("in terms of")
            self.play(*appear(task.hand), run_time=1.0)
            settle(self, task)

            c.wait_until("theorem")
            thm = mt([(r"\cos", FG), ("n", FG), (r"\theta", FG), ("+", FG), (r"i\sin", FG), ("n", FG),
                      (r"\theta", FG), ("=", FG), (r"(\cos\theta+i\sin\theta)", FG), ("^n", FG)], 52)
            thm.move_to(DOWN * 1.9)
            box = SurroundingRectangle(thm, color=YELLOW, buff=0.25, stroke_width=3)
            self.play(*appear(thm, box, shift=None, lag=0.1), run_time=1.0)
            c.wait_until("equal to four")
            fours = VGroup()
            for idx, fs in ((1, 52), (5, 52), (9, 36)):
                f = MathTex("4", font_size=fs, color=GOLD).move_to(thm[idx]).align_to(thm[idx], DOWN)
                fours.add(f)
            self.play(*[time_span(thm[i].animate.set_opacity(0), 0, 0.5) for i in (1, 5, 9)],
                      *[time_span(FadeIn(f, shift=0.3 * DOWN), 0.55, 1.3) for f in fours], run_time=1.3)

            c.wait_until("lhs")
            fade_t = task.copy()
            for m in (fade_t.frame, fade_t.b1, fade_t.b2):
                m.set_opacity(0)
            top_t = fade_t.copy()
            hb = VGroup(top_t.band, top_t.head).scale(0.75)
            top_t.band.stretch_to_fit_width(top_t.head.width + 0.5)
            top_t.hand.scale(0.75)
            VGroup(top_t.hand, hb).arrange(RIGHT, buff=0.45).to_edge(UP, buff=0.35)
            mid_t = fade_t.copy()          # header up first, then the handwritten goal beside it
            mid_t.band.become(top_t.band)
            mid_t.head.become(top_t.head)
            self.play(Transform(task, mid_t), run_time=0.9)
            self.play(Transform(task, top_t), run_time=0.8)
            L = make_line1()
            self.play(*fly(VGroup(thm, box, fours), L), run_time=1.6)
            th_txt = Text("Th.", font=HAND, font_size=40, color=YELLOW)
            th_arrow = Arrow(RIGHT * 0.7, ORIGIN, buff=0, color=YELLOW, stroke_width=4,
                             max_tip_length_to_length_ratio=0.35)
            thnote = VGroup(th_arrow, th_txt).arrange(RIGHT, buff=0.12).next_to(L, RIGHT, buff=0.35)
            self.play(*disappear(thm, box, fours), run_time=0.9)   # the theorem box has given its line
            self.play(*appear(thnote, shift=None), run_time=0.9)  # early: the lecturer's margin note, not read aloud

        # ------------------------------------------------------------ c2.exp.2
        with self.say("c2.exp.2") as c:
            rhs = VGroup(*L[8:14])
            self.play(FlashAround(rhs, time_width=1.5), run_time=1.5)
            binom = MathTex("(a+b)^4", font_size=40).move_to(PASCAL_TOP + UP * 0.8)
            self.play(*appear(binom), run_time=1.0)

            c.wait_until("pascal")
            pascal = pascal_rows()
            self.play(*appear(*pascal[:4], lag=0.35, shift=None), run_time=min(2.0, c.until("one four six")))
            c.wait_until("one four six")
            self.play(*appear(*pascal[4], lag=0.45, shift=None), run_time=min(2.2, c.until("count")))
            settle(self, pascal)

            c.wait_until("count")
            slots = make_slots()
            coefs = [s[0] for s in slots]
            coss = [s[1] for s in slots if s[1] is not None]
            ips = [s[2] for s in slots if s[2] is not None]
            self.play(*appear(*coss, lag=0.3), run_time=min(2.0, c.until("and the power of eye")))
            c.wait_until("and the power of eye")
            self.play(*appear(*ips, lag=0.3), run_time=1.5)
            self.play(*appear(*coefs, lag=0.2), *flash(list(pascal[4]), color=GOLD), run_time=1.4)
            slot_grp = VGroup(*coefs, *coss, *ips)
            settle(self, slot_grp)

            c.wait_until("short")
            note = MathTex(r"\cos,\ \sin\;=\;\cos\theta,\ \sin\theta", font_size=36, color=DIM).move_to([4.3, -3.45, 0])
            self.play(*appear(note), run_time=1.0)

        # ------------------------------------------------------------ c2.exp.3
        with self.say("c2.exp.3") as c:
            self.play(*disappear(pascal, binom), *flash(ips, color=PINK), run_time=1.3)
            dial = i_dial()
            self.play(*appear(VGroup(dial.axes, dial.circle), dial.marks[1], dial.dot, dial.lbls[1],
                              lag=0.2, shift=None), run_time=min(1.3, c.until("dial")))
            for k, cue in ((2, "dial"), (3, "cube"), (4, "fourth")):
                c.wait_until(cue)
                self.play(Rotate(dial.dot, PI / 2, about_point=dial.center_pt), run_time=1.1)
                self.play(*appear(dial.marks[k], dial.lbls[k], shift=None, lag=0.1), run_time=0.8)
            settle(self, dial)

            c.wait_until("quarter")
            ctr, r = dial.center_pt, dial.r
            p0 = ctr + (r + 0.3) * np.array([np.cos(22 * DEGREES), np.sin(22 * DEGREES), 0])
            p1 = ctr + (r + 0.3) * np.array([np.cos(68 * DEGREES), np.sin(68 * DEGREES), 0])
            turn = CurvedArrow(p0, p1, angle=46 * DEGREES, color=PINK, stroke_width=4, tip_length=0.2)
            times_i = MathTex(r"\times i", font_size=34, color=PINK).move_to(
                ctr + (r + 0.85) * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]))
            self.play(Create(turn), *appear(times_i, shift=None), run_time=1.2)
            c.wait_until("go round")
            # one quarter turn per word: the dot lands on i, -1, -i, 1 as each is said
            for cue in ("dial eye", "minus one", "minus eye", "back to one"):
                self.play(Rotate(dial.dot, PI / 2, about_point=ctr), run_time=c.until(cue, floor=0.4))

        # ------------------------------------------------------------ c2.exp.4
        with self.say("c2.exp.4") as c:
            self.play(*disappear(slot_grp, note, turn, times_i),
                      dial.animate.scale(0.75).move_to(DIAL_C2), run_time=1.2)
            E = make_E()
            self.play(*appear(E, shift=None), run_time=min(1.5, c.until("real")))

            c.wait_until("real")
            v_m1 = dial.lbls[2][2].copy().next_to(E[8], DOWN, buff=0.3)
            v_1 = dial.lbls[4][2].copy().next_to(E[15], DOWN, buff=0.3)
            v_mi = dial.lbls[3][2].copy().next_to(E[12], DOWN, buff=0.3)
            self.play(*flash([E[8], E[15]]), *fly_lin(dial.lbls[2][2], v_m1), *fly_lin(dial.lbls[4][2], v_1),
                      run_time=1.5)
            real = [g for i in (1, 7, 8, 9, 15, 16) for g in E[i]]
            self.play(*recolor(real, BLUE), run_time=1.0)

            c.wait_until("imag")
            imag = [g for i in (3, 4, 5, 11, 12, 13) for g in E[i]]
            self.play(*fly_lin(dial.lbls[3][2], v_mi), *recolor(imag, PINK), run_time=1.5)

            c.wait_until("signs")
            S = make_S(red=True)
            self.play(*edit(E, S), run_time=1.6)
            c.wait_until("minus four eye")
            self.play(*recolor(S[6], BLUE), *recolor(S[9], PINK), run_time=0.8)

            c.wait_until("collect")
            C = make_C()
            rt = min(1.7, max(1.0, c.until("blue")))
            drop = S.copy().shift((COL_Y - EXP_Y) * UP).align_to(C, LEFT)   # straight down, left edges kept
            leave = fly(S, drop)
            for an in leave:          # quick off the source line, so the copy never sits on it
                an.rate_func = lambda t: t ** 3   # _FlyCopy plays its Transform backwards: this is a fast start
            self.play(*during(disappear(v_m1, v_mi, v_1), 0, 0.3),    # the values under the line clear first
                      *during(disappear(dial, task, thnote), 0, 0.8), *during(leave, 0.3, 1),
                      run_time=rt * 0.6)
            self.play(*edit(drop, C), run_time=rt * 0.5)

            br_r, lr, br_i, li = make_braces(C)
            c.wait_until("blue", own_word=lr)
            self.play(GrowFromCenter(br_r), *appear(lr), run_time=1.2)
            c.wait_until("pink", own_word=li)
            self.play(GrowFromCenter(br_i), *appear(li), run_time=1.2)
            c.wait_until("factor of four eye")
            self.play(FlashAround(C[8], time_width=1.5), run_time=1.2)
            c.wait_until("times a bracket")
            self.play(FlashAround(VGroup(*C[9:14]), time_width=1.5), run_time=1.5)

        self.wait(1.0)   # handover: hold the collected line for ch2_s5_simplify
