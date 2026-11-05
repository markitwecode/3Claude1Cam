"""Chapter 7, scene 2: G1, tanh(x + y). Clips c7.g1.1 – c7.g1.5.

Opens on ch7_s1's four-card row; G1 grows to the hero spot, pause icon. Route 1: (95)'s TEAL
sinh/cosh lines feed tanh = sinh/cosh, divide by cosh x cosh y, collapse, boxed answer.
Route 2: e^{2x} = (1 + p)/(1 - p), multiply, clear fractions, cancel, same answer.
Check: BLUE tan(x + y) with its - -> YELLOW +, RED slip, test at 1/2 against a tanh graph.

Shared (import with load_scene("ch7_s2_g1")):
  boxed_answer(size=48)     VGroup(eq, box): tanh(x+y) = (tanh x + tanh y)/(1 + tanh x tanh y),
                            YELLOW box, YELLOW + underneath; .eq .box .plus (eq has .lhs .num .bar .den)
  tan_sum_formula(size=44)  BLUE tan(x+y) = (tan x + tan y)/(1 - tan x tan y); .minus (the -)
  eqn(lhs, num, den, color, size)  the fraction-equation builder both use
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch7_s1_intro")

HERO = np.array([-1.5, 0.3, 0])
HL, BAR_Y = -5.0, 0.1            # route 1: lhs left edge, main fraction bar height


# ---------------------------------------------------------------- builders (shared)
def frac_of(n, d, color, gap=0.14):
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=3.5, color=color)
    n.next_to(bar, UP, buff=gap)
    d.next_to(bar, DOWN, buff=gap)
    return VGroup(n, bar, d)


def eqn(lhs, num, den, color=FG, size=48):
    """lhs = num/den with the bar on the = sign: VGroup(lhs, VGroup(num, bar, den))."""
    l = MathTex(lhs, "=", font_size=size, color=color)
    n = MathTex(*num, font_size=size, color=color)
    d = MathTex(*den, font_size=size, color=color)
    fr = frac_of(n, d, color)
    fr.next_to(l, RIGHT, buff=0.3)
    fr.shift(UP * (l[1].get_y() - fr[1].get_y()))
    g = VGroup(l, fr)
    g.lhs, g.num, g.bar, g.den = l, n, fr[1], d
    return g


def boxed_answer(size=48):
    eq = eqn(r"\tanh(x+y)", [r"\tanh x", "+", r"\tanh y"], ["1", "+", r"\tanh x\,\tanh y"], size=size)
    eq.den[1].set_color(YELLOW)
    box = SurroundingRectangle(eq, color=YELLOW, buff=0.3).set_stroke(YELLOW, 3)
    g = VGroup(eq, box)
    g.eq, g.box, g.plus = eq, box, eq.den[1]
    return g


def tan_sum_formula(size=44):
    g = eqn(r"\tan(x+y)", [r"\tan x", "+", r"\tan y"], ["1", "-", r"\tan x\,\tan y"], color=BLUE, size=size)
    g.minus = g.den[1]
    return g


def stage(num, den):
    e = eqn(r"\tanh(x+y)", num, den)
    e.shift(RIGHT * (HL - e.lhs.get_left()[0]) + UP * (BAR_Y - e.bar.get_y()))
    return e


def strike(m):
    return Line(m.get_corner(DL) + 0.05 * LEFT, m.get_corner(UR) + 0.05 * RIGHT, color=RED, stroke_width=4)


class G1TanhSum(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the card
    def clip1(self):
        row = S1.handover_shot()
        self.add(row)
        self.remove(row)
        self.add(*row)
        g1 = row[0]
        sheet = Tex(r"Express $\tanh(x+y)$ in terms of $\tanh x$ and $\tanh y$.", font_size=40)
        sheet.move_to([-0.5, -2.85, 0])
        pause = S1.pause_icon(height=1.2).move_to([4.5, 0.3, 0])
        with self.say("c7.g1.1") as c:
            self.play(*during([FadeOut(m) for m in row[1:]], 0, 0.4),
                      *during([g1.animate.scale(1.5).move_to(HERO)], 0.3, 1),
                      run_time=min(2.0, c.until("express")))
            c.wait_until("express")
            self.play(*appear(sheet), run_time=1.2)
            c.wait_until("stop")
            self.play(*appear(pause, shift=None), run_time=1.0)

    # ------------------------------------------------------------ route 1
    def clip2(self):
        l1 = MathTex(r"\sinh(x+y)", "=", r"\sinh x\,\cosh y+\cosh x\,\sinh y", font_size=48, color=TEAL)
        l2 = MathTex(r"\cosh(x+y)", "=", r"\cosh x\,\cosh y+\sinh x\,\sinh y", font_size=48, color=TEAL)
        l1.move_to([0, 2.8, 0])
        l2.move_to([0, -2.7, 0])
        s0 = stage([r"\sinh(x+y)"], [r"\cosh(x+y)"])
        s1 = stage([r"\sinh x\,\cosh y", "+", r"\cosh x\,\sinh y"], [r"\cosh(x+y)"])
        s2 = stage([r"\sinh x\,\cosh y", "+", r"\cosh x\,\sinh y"],
                   [r"\cosh x\,\cosh y", "+", r"\sinh x\,\sinh y"])
        s3 = stage([r"\dfrac{\sinh x\,\cosh y}{", r"\cosh x\,\cosh y", r"}+\dfrac{\cosh x\,\sinh y}{",
                    r"\cosh x\,\cosh y", "}"],
                   [r"\dfrac{\cosh x\,\cosh y}{", r"\cosh x\,\cosh y", r"}+\dfrac{\sinh x\,\sinh y}{",
                    r"\cosh x\,\cosh y", "}"])
        for part in (s3.num[1], s3.num[3], s3.den[1], s3.den[3]):
            part.set_color(YELLOW)
        ans = boxed_answer().move_to([0, 0.2, 0])
        delta = (RIGHT * (HL - ans.eq.lhs.get_left()[0]) + UP * (BAR_Y - ans.eq.bar.get_y()))
        s4 = ans.eq.copy().shift(delta)
        s4.den[1].set_color(FG)
        note = MathTex(r"\cosh\ge 1,\ \text{never } 0", font_size=40, color=GREEN)
        note.move_to([-3.4, BAR_Y - 1.3, 0])
        lhs, bar = s0.lhs, s0.bar
        with self.say("c7.g1.2") as c:
            sweep_clear(self, *appear(l1, l2, lag=0.5), run_time=2.0)
            c.wait_until("since")
            self.play(*appear(lhs, shift=None), GrowFromCenter(bar),
                      *appear(s0.num, shift=None), *appear(s0.den, shift=None), run_time=min(2.0, c.until("top")))
            c.wait_until("top")
            self.play(*disappear(s0.num), Transform(bar, s1.bar), run_time=0.8)
            self.play(FlashAround(l1[2], color=TEAL, time_width=1.5), *during(appear(s1.num), 0.3, 1), run_time=1.8)
            c.wait_until("bottom")
            self.play(*disappear(s0.den), Transform(bar, s2.bar), run_time=0.8)
            self.play(FlashAround(l2[2], color=TEAL, time_width=1.5), *during(appear(s2.den, shift=0.25 * UP), 0.3, 1), run_time=1.8)
            c.wait_until("divide")
            self.play(*edit(s1.num, s3.num), *edit(s2.den, s3.den), Transform(bar, s3.bar),
                      *set_alpha([l1, l2], 0.4), run_time=2.0)
            c.wait_until("never zero")
            self.play(*appear(note), run_time=1.0)
            c.wait_until("collapse")
            self.play(*swap(s3.num, s4.num), run_time=1.5)
            c.wait_until("the first term underneath")
            self.play(*swap(s3.den, s4.den), Transform(bar, s4.bar), run_time=1.5)
            c.wait_until("result")
            self.play(*disappear(l1, l2, note),
                      *[m.animate.shift(-delta) for m in (lhs, s4.num, bar, s4.den)], run_time=1.5)
            self.play(GrowFromCenter(ans.box), *recolor([s4.den[1]], YELLOW),
                      FlashAround(s4.den[1], time_width=1.5), run_time=1.5)
            self.remove(lhs, s4.num, bar, s4.den, ans.box)
            self.add(ans)
        self.ans = ans

    # ------------------------------------------------------------ route 2
    def clip3(self):
        ans = self.ans
        A = MathTex(r"\tanh x", "=", r"\frac{e^x-e^{-x}}{e^x+e^{-x}}", font_size=48).move_to([-1.5, 1.4, 0])
        lab1 = MathTex(r"\times e^x", font_size=36, color=GOLD)
        lab2 = lab1.copy()
        lab1.next_to(A[2], RIGHT, buff=0.45).shift(UP * 0.4)
        lab2.next_to(A[2], RIGHT, buff=0.45).shift(DOWN * 0.4)
        B = MathTex(r"\tanh x", "=", r"\frac{", r"e^{2x}", "-1}{", r"e^{2x}", "+1}", font_size=48)
        B[3].set_color(GOLD)
        B[5].set_color(GOLD)
        B.shift(UP * (A.get_y() - B.get_y()) + RIGHT * (A[1].get_x() - B[1].get_x()))
        C = MathTex(r"e^{2x}", "=", r"\frac{1+", r"\tanh x", "}{1-", r"\tanh x", "}", font_size=48)
        C[0].set_color(GOLD)
        C.shift(UP * (-1.1 - C.get_y()) + RIGHT * (A[1].get_x() - C[1].get_x()))
        tag = T("Example 34", 30, DIM).next_to(C, LEFT, buff=0.6)
        tp = MathTex(r"p=\tanh x", font_size=40, color=YELLOW).move_to([-5.0, 3.35, 0])
        tq = MathTex(r"q=\tanh y", font_size=40, color=YELLOW).next_to(tp, RIGHT, buff=0.8)
        with self.say("c7.g1.3") as c:
            self.play(*during([ans.animate.scale(0.7).to_corner(UR, buff=0.4)], 0, 0.6),
                      *during(appear(A), 0.5, 1), run_time=2.2)
            c.wait_until("e2x")
            self.play(*appear(lab1, lab2, lag=0.3), run_time=1.2)
            c.wait_until("tanch of ex becomes")
            self.play(*disappear(lab1, lab2), *edit(A, B), run_time=2.0)
            c.wait_until("ex34")
            self.play(*appear(C, tag, lag=0.4), run_time=1.4)
            c.wait_until("names")
            self.play(*appear(tp), *recolor([C[3], C[5]], YELLOW), run_time=1.0)
            c.wait_until("and tanch of why")
            self.play(*appear(tq), run_time=1.0)
        self.A, self.B, self.C, self.tag, self.tp, self.tq = A, B, C, tag, tp, tq

    def clip4(self):
        ans, C = self.ans, self.C
        D = MathTex(r"e^{2x}", r"\,", r"e^{2y}", "=", r"e^{2(x+y)}", "=",
                    r"\frac{(1+p)(1+q)}{(1-p)(1-q)}", font_size=46)
        for i in (0, 2, 4):
            D[i].set_color(GOLD)
        D.move_to([-1.6, 1.6, 0])
        C.generate_target()
        C.target.shift(UP * (D[3].get_y() - C.target[1].get_y()) + RIGHT * (D.get_left()[0] - C.target.get_left()[0]))
        ey = -1.2
        E1 = MathTex(r"\tanh(x+y)=\frac{(1+p)(1+q)-(1-p)(1-q)}{(1+p)(1+q)+(1-p)(1-q)}", font_size=44)
        E2 = MathTex(r"\tanh(x+y)=\frac{(", "1", "+p+q", "+pq", ")-(", "1", "-p-q", "+pq",
                     r")}{(1", "+p", "+q", r"+pq)+(1", "-p", "-q", r"+pq)}", font_size=44)
        E4 = MathTex(r"\tanh(x+y)=\frac{2p+2q}{2+2pq}", font_size=44)
        E5 = MathTex(r"\tanh(x+y)=\frac{p+q}{1", "+", "pq}", font_size=44)
        E5[1].set_color(YELLOW)
        E2.move_to([0, ey, 0])
        for e in (E1, E4, E5):
            e.move_to([0, ey, 0]).align_to(E2, LEFT)
        with self.say("c7.g1.4") as c:
            sweep_clear(self, MoveToTarget(C), keep=[ans, self.tp, self.tq, C], run_time=1.6)
            self.play(*edit(C, D), run_time=2.0)
            c.wait_until("plug")
            self.play(*appear(E1), run_time=1.5)
            c.wait_until("cancel")
            self.play(*swap(E1, E2), run_time=1.2)
            # numerator only: the two 1s and the two +pq
            top = [strike(E2[i]) for i in (1, 5, 3, 7)]
            self.play(LaggedStart(*[Create(s) for s in top], lag_ratio=0.35), run_time=1.4)
            c.wait_until("underneath")
            # denominator only: +p with -p, +q with -q
            bot = [strike(E2[i]) for i in (9, 12, 10, 13)]
            self.play(LaggedStart(*[Create(s) for s in bot], lag_ratio=0.35), run_time=1.4)
            c.wait_until("leaving", nth=1)
            settle(self, E2, add=top + bot)
            self.play(*swap(E2, E4), run_time=1.2)
            c.wait_until("same")
            self.play(*swap(E4, E5), run_time=1.2)
            self.play(FlashAround(E5, time_width=1.5, buff=0.2), FlashAround(ans, time_width=1.5),
                      run_time=min(2.0, c.until()))

    # ------------------------------------------------------------ check
    def clip5(self):
        ans = self.ans
        ans.generate_target()
        ans.target.scale(0.84 / 0.7).move_to([-3.0, 0.3, 0])
        tan = tan_sum_formula(size=40).move_to([-3.0, 2.6, 0])
        hid = VGroup(T("hidden", 30, YELLOW), MathTex(r"\sinh x\,\sinh y", font_size=36, color=YELLOW))
        hid.arrange(RIGHT, buff=0.18)
        red = eqn(r"\tanh(x+y)", [r"\tanh x", "+", r"\tanh y"], ["1", "-", r"\tanh x\,\tanh y"],
                  color=RED, size=40).move_to([-3.0, -2.55, 0])
        xm = cross_mark().next_to(red, RIGHT, buff=0.3)
        head = MathTex(r"\tanh x=\tanh y=\tfrac12", font_size=40).move_to([3.7, 3.25, 0])
        sub = MathTex(r"(x=y=\tfrac12\ln 3)", font_size=32, color=DIM).next_to(head, DOWN, buff=0.2)
        right = MathTex(r"\frac{1}{1+\frac14}", "=", r"\frac45", font_size=40, color=GREEN).move_to([2.5, 1.35, 0])
        wrong = MathTex(r"\frac{1}{1-\frac14}", "=", r"\frac43", font_size=40, color=RED).move_to([5.2, 1.35, 0])
        ax = Axes(x_range=[-2.5, 2.5, 1], y_range=[-1.5, 1.5, 1], x_length=5, y_length=3, tips=False,
                  axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False}).move_to([3.7, -1.95, 0])
        curve = ax.plot(np.tanh, x_range=[-2.5, 2.5], color=TEAL, stroke_width=4)
        y1 = DashedLine(ax.c2p(-2.5, 1), ax.c2p(2.5, 1), color=GOLD, dash_length=0.12)
        ym1 = DashedLine(ax.c2p(-2.5, -1), ax.c2p(2.5, -1), color=PURPLE, dash_length=0.12)
        n1 = MathTex("1", font_size=30, color=GOLD).next_to(ax.c2p(-2.5, 1), LEFT, buff=0.12)
        nm1 = MathTex("-1", font_size=30, color=PURPLE).next_to(ax.c2p(-2.5, -1), LEFT, buff=0.12)
        L3 = np.log(3)
        gdot = Dot(ax.c2p(L3, 0.8), radius=0.1, color=GREEN)
        rdot = Dot(ax.c2p(L3, 4 / 3), radius=0.1, color=RED)
        glab = MathTex(r"\frac45", font_size=30, color=GREEN).next_to(gdot, DR, buff=0.08)
        rlab = MathTex(r"\frac43", font_size=30, color=RED).next_to(rdot, RIGHT, buff=0.15)
        with self.say("c7.g1.5") as c:
            sweep_clear(self, MoveToTarget(ans), keep=[ans], run_time=1.6)
            self.play(*appear(tan), run_time=1.0)
            c.wait_until("hidden")
            box = token_box(tan.minus, tan.den)
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("hides")
            hid.next_to(ans, DOWN, buff=0.25)
            self.play(*appear(hid), FlashUnder(ans.eq.den[2], time_width=1.5), run_time=1.5)
            c.wait_until("flips")
            self.play(Transform(box, token_box(ans.plus, ans.eq.den)), run_time=1.5)
            self.play(FlashAround(ans.plus, time_width=1.5), run_time=1.0)
            c.wait_until("slip")
            self.play(*disappear(box), *appear(red, xm, lag=0.3), run_time=1.4)
            c.wait_until("test")
            self.play(*appear(head, sub, lag=0.3), run_time=1.2)
            self.wait(0.4)
            self.play(Create(ax), Create(curve), *appear(y1, ym1, n1, nm1, shift=None, lag=0.1), run_time=1.6)
            c.wait_until("right")
            self.play(*appear(right), *appear(gdot, glab, shift=None), run_time=1.2)
            c.wait_until("wrong")
            self.play(*appear(wrong), *appear(rdot, rlab, shift=None), run_time=1.2)
            c.wait_until("bigger")
            self.play(VShowPassingFlash(Line(ax.c2p(-2.5, 1), ax.c2p(2.5, 1)).set_stroke(YELLOW, 6),
                                        time_width=0.5),
                      FlashAround(rdot, color=RED, time_width=1.5), run_time=1.5)
