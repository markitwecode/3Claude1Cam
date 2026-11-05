"""Chapter 3, scene 1: hook. Title card, part two's rules, two awkward cases. Clips c3.hook.1 – c3.hook.3."""
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
from lib.titles import title_card  # noqa: E402

PART = "Part 3 · Implicit differentiation and inverse functions"


def open_card():
    """The chapter's title card exactly as it stands once settled (static VGroup at ORIGIN)."""
    return title_card(PART)


# ---------- part two's three rules (first function BLUE, second PURPLE)
def chain_rule(size=40):
    return _colour(MathTex(r"\frac{d}{dx}", "f", r"\big(", "u", r"(x)\big) = \frac{d", "f", "}{d", "u",
                           r"}\,\frac{d", "u", "}{dx}", font_size=size, color=FG),
                   {1: BLUE, 5: BLUE, 3: PURPLE, 7: PURPLE, 9: PURPLE})


def product_rule(size=40):
    return _colour(MathTex(r"\frac{d}{dx}(", "f", "g", r") = \frac{d", "f", r"}{dx}\,", "g", " + ", "f",
                           r"\,\frac{d", "g", "}{dx}", font_size=size, color=FG),
                   {1: BLUE, 4: BLUE, 8: BLUE, 2: PURPLE, 6: PURPLE, 10: PURPLE})


def quotient_rule(size=40):
    return _colour(MathTex(r"\frac{d}{dx}\left(\frac{", "u", "}{", "v", r"}\right) = \frac{", "v",
                           r"\,\frac{d", "u", "}{dx} - ", "u", r"\,\frac{d", "v", "}{dx}}{", "v", "^2}",
                           font_size=size, color=FG),
                   {1: BLUE, 7: BLUE, 9: BLUE, 3: PURPLE, 5: PURPLE, 11: PURPLE, 13: PURPLE})


def _colour(m, idx):
    for i, col in idx.items():
        m[i].set_color(col)
    return m


# ---------- the circle (as ch3 s3: equal units, x -3..5, y -3.5..3.5, centre (1, 0), radius 3)
U = 0.7


def circle_axes():
    axes = Axes(x_range=[-3, 5, 1], y_range=[-3.5, 3.5, 1], x_length=8 * U, y_length=7 * U, tips=False,
                axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
    axes.move_to([-3.5, -0.2, 0])
    return axes


def plus_minus(size=40):
    """A ± whose minus is RED (two pieces so the minus can be coloured)."""
    plus = MathTex("+", font_size=size, color=FG)
    bar = Line(LEFT, RIGHT, stroke_width=4, color=RED).set_width(plus.width)
    bar.next_to(plus, DOWN, buff=0.06)
    return VGroup(plus, bar)


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c3.hook.1: title card, then part two's rules
    def clip1(self):
        with self.say("c3.hook.1", gap=1.6) as c:
            card = open_card()
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 1.0),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 1.0),
                      time_span(FadeIn(card.course), 0.3, 1.3),
                      time_span(FadeIn(card.part), 0.6, 1.6), run_time=1.6)
            c.wait_until("last")
            self.play(*disappear(card), run_time=0.7)

            labels = [T("chain rule", 34, DIM), T("product rule", 34, DIM), T("quotient rule", 34, DIM)]
            forms = [chain_rule(48), product_rule(48), quotient_rule(48)]
            rows = VGroup(*[VGroup(lab, f) for lab, f in zip(labels, forms)])
            for lab, f in zip(labels, forms):
                lab.next_to(f, LEFT, buff=0.6)
            rows.arrange(DOWN, buff=0.6)
            for lab in labels:
                lab.align_to(labels[0], RIGHT)
            for f in forms:
                f.align_to(forms[0], LEFT)
            rows.move_to(ORIGIN)
            self.rows, self.labels, self.forms = rows, labels, forms
            for lab, f, cue in zip(labels, forms, ["chain", "product", "quotient"]):
                c.wait_until(cue)
                self.play(*appear(lab, f, lag=0.15), run_time=min(0.8, c.until("quotient"))
                          if cue != "quotient" else 0.8)

    # ---- c3.hook.2: the circle, then the inverse sine
    def clip2(self):
        with self.say("c3.hook.2") as c:
            chain = self.forms[0]
            others = [self.labels[0], self.labels[1], self.forms[1], self.labels[2], self.forms[2]]
            chain.generate_target()
            chain.target.scale(0.65).to_corner(UR, buff=0.45)
            self.play(*during(disappear(*others), 0, 0.45),
                      *during([MoveToTarget(chain)], 0.3, 1), run_time=1.4)
            self.chain = chain

            axes = circle_axes()
            circ = Circle(radius=3 * U, color=BLUE, stroke_width=5).move_to(axes.c2p(1, 0))
            self.play(FadeIn(axes), Create(circ), run_time=min(1.8, c.until("first")))
            c.wait_until("first")
            eq1 = MathTex("y^2 = 9 - (x - 1)^2", font_size=48, color=FG).move_to([-3.5, 2.85, 0])
            self.play(*appear(eq1), run_time=1.2)
            self.axes, self.circ, self.eq1 = axes, circ, eq1

            c.wait_until("two")
            vline = DashedLine(axes.c2p(2.8, -3.5), axes.c2p(2.8, 3.5), color=DIM, stroke_width=3,
                               dash_length=0.1)
            dots = [Dot(axes.c2p(2.8, s * 2.4), radius=0.1, color=YELLOW) for s in (1, -1)]
            self.play(Create(vline), run_time=1.2)
            self.play(*[GrowFromCenter(d) for d in dots], run_time=0.8)
            self.play(*flash(dots, run_time=1.2))
            self.vline, self.dots = vline, dots

            c.wait_until("second")
            eq2 = MathTex(r"y = \sin^{-1}\!\left(\dfrac{x}{\sqrt{1 + x^2}}\right)", font_size=48,
                          color=FG).move_to([3.6, 0.9, 0])
            self.play(*appear(eq2), run_time=1.4)
            self.eq2 = eq2

            c.wait_until("headon")
            ask = MathTex(r"\dfrac{dy}{dx} = \;", "?", font_size=48, color=FG)
            ask[1].set_color(YELLOW)
            ask.next_to(eq2, DOWN, buff=0.8)
            self.play(*appear(ask), run_time=1.0)
            self.ask = ask

    # ---- c3.hook.3: the question, the plan, the preview
    def clip3(self):
        with self.say("c3.hook.3", gap=2.0) as c:
            q = MathTex("?", font_size=110, color=YELLOW).move_to([0.15, 0.3, 0])
            self.play(*appear(q, shift=None), run_time=0.8)
            self.play(q.animate(rate_func=there_and_back).scale(1.3), run_time=1.0)
            self.play(*flash([q], run_time=1.5))

            c.wait_until("plan")
            eq1d = MathTex(r"\frac{d}{dx}\big(y^2\big) = \frac{d}{dx}\big(9 - (x - 1)^2\big)",
                           font_size=40, color=FG).move_to(self.eq1)
            eq2d = MathTex(r"\frac{d}{dx}\,y = \frac{d}{dx}\,\sin^{-1}\!\left(\dfrac{x}{\sqrt{1 + x^2}}\right)",
                           font_size=40, color=FG).move_to(self.eq2).set_x(3.75)
            self.play(*disappear(q), run_time=0.6)
            self.play(*edit(self.eq1, eq1d), *edit(self.eq2, eq2d), run_time=1.6)
            self.play(*flash([self.chain], run_time=1.5))
            self.eq1, self.eq2 = eq1d, eq2d

            c.wait_until("preview")
            board = [self.axes, self.circ, self.vline, *self.dots, self.eq1, self.eq2, self.ask, self.chain]
            tag = T("Tripos 2006", 34, FG)
            pm = plus_minus(48)
            icon1 = VGroup(tag, pm).arrange(RIGHT, buff=0.35)
            frame1 = SurroundingRectangle(icon1, color=DIM, buff=0.2, corner_radius=0.1, stroke_width=2)
            icon1 = VGroup(frame1, tag, pm).move_to([-3.5, -3.2, 0])

            icon2 = MathTex(r"\dfrac{", "dx", "}{", "dy", r"} = \dfrac{1}{dy/dx}", font_size=40, color=FG)
            icon2.move_to([3.6, -3.1, 0])
            top, bot = icon2[1].get_center(), icon2[3].get_center()
            icon2[1].move_to(bot)
            icon2[3].move_to(top)

            self.play(*set_alpha(board, 0.4), *appear(icon1), run_time=1.0)
            self.play(*flash([pm[1]], color=RED, run_time=1.2))
            c.wait_until("derivative gets")
            self.play(*appear(icon2), run_time=0.8)
            self.play(icon2[1].animate(path_arc=PI).move_to(top),
                      icon2[3].animate(path_arc=PI).move_to(bot), run_time=1.2)
