"""Chapter 7, scene 5: G4, tanh^-1 x as a log, and its derivative. Clips c7.g4.1 – c7.g4.5.

Card G4 enlarged + pause; Example 34's chain to tanh^-1 x = 1/2 ln[(1+x)/(1-x)]; split the log,
differentiate each piece (the chain-rule (-1) chip in YELLOW), combine to 1/(1-x^2) (boxed);
the dropped-minus slip in RED with a falling curve beside the rising tanh^-1; three checks on the
graph pair (tanh^-1 over 1/(1-x^2), dashed x = 1 GOLD / x = -1 PURPLE); dx/dy = sech^2 y flipped.

Shared with the recap (import with load_scene("ch7_s5_g4")):
  g4_answer(size=52)       VGroup(box, tex): YELLOW-boxed d/dx tanh^-1 x = 1/(1-x^2); .box .tex
  minus_one_chip(size=40)  VGroup(box, tex): the YELLOW (-1) chain-rule chip; .box .tex
  g4_axes(y_lo, y_hi, u)   equal-unit DIM axes, x in [-2, 2]
  atanh_graph(u=0.75)      axes + lighter-TEAL tanh^-1 x; .ax .curve
  deriv_graph(u=0.75)      axes + BLUE 1/(1-x^2); .ax .curve
  graph_pair(u=0.75, center=ORIGIN)  atanh over deriv sharing dashed x = 1 (GOLD), x = -1 (PURPLE);
                           .top .bot .dash_r .dash_l .top_label .bot_label
"""
# style: 2
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

ATANH_C = "#A8EBD9"                 # lighter teal (ch1's SINH_C)
EC = {"e^{y}": GOLD, "e^{-y}": PURPLE}
X_ATANH = math.tanh(2.0)            # tanh^-1 reaches y = 2
X_BLOW = math.sqrt(1 - 1 / 3.5)     # 1/(1-x^2) reaches y = 3.5
HERO_C = np.array([-1.5, 0.3, 0])


# ---------------------------------------------------------------- shared pieces
def g4_answer(size=52):
    tex = MathTex(r"\frac{d}{dx}\tanh^{-1}x = \frac{1}{1-x^{2}}", font_size=size)
    box = SurroundingRectangle(tex, color=YELLOW, buff=0.25, corner_radius=0.1).set_stroke(YELLOW, 3)
    g = VGroup(box, tex)
    g.box, g.tex = box, tex
    return g


def minus_one_chip(size=40):
    tex = MathTex(r"(-1)", font_size=size, color=YELLOW)
    box = RoundedRectangle(corner_radius=0.15, width=tex.width + 0.36, height=tex.height + 0.3)
    box.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12).move_to(tex)
    g = VGroup(box, tex)
    g.box, g.tex = box, tex
    return g


def g4_axes(y_lo, y_hi, u=0.75, y_ticks=True):
    return Axes(x_range=[-2, 2, 1], y_range=[y_lo, y_hi, 1], x_length=4 * u, y_length=(y_hi - y_lo) * u,
                tips=False,
                axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06},
                y_axis_config={"include_ticks": y_ticks})


def atanh_graph(u=0.75):
    ax = g4_axes(-2, 2, u)
    curve = ax.plot(math.atanh, x_range=[-X_ATANH, X_ATANH, 0.01], color=ATANH_C, stroke_width=5)
    g = VGroup(ax, curve)
    g.ax, g.curve = ax, curve
    return g


def deriv_graph(u=0.75):
    ax = g4_axes(-0.5, 3.5, u, y_ticks=False)
    curve = ax.plot(lambda x: 1 / (1 - x * x), x_range=[-X_BLOW, X_BLOW, 0.01], color=BLUE, stroke_width=5)
    g = VGroup(ax, curve)
    g.ax, g.curve = ax, curve
    return g


def graph_pair(u=0.75, center=ORIGIN):
    top, bot = atanh_graph(u), deriv_graph(u)
    VGroup(top, bot).arrange(DOWN, buff=0.6).move_to(center)
    dash_r = DashedLine(top.ax.c2p(1, 2), bot.ax.c2p(1, -0.5), dash_length=0.1).set_stroke(GOLD, 2.5)
    dash_l = DashedLine(top.ax.c2p(-1, 2), bot.ax.c2p(-1, -0.5), dash_length=0.1).set_stroke(PURPLE, 2.5)
    top_label = MathTex(r"\tanh^{-1}x", font_size=36, color=ATANH_C)
    top_label.next_to(top.ax, LEFT, buff=0.25)
    bot_label = MathTex(r"\frac{1}{1-x^{2}}", font_size=36, color=BLUE)
    bot_label.next_to(bot.ax, LEFT, buff=0.25)
    g = VGroup(dash_r, dash_l, top, bot, top_label, bot_label)
    g.top, g.bot, g.dash_r, g.dash_l, g.top_label, g.bot_label = top, bot, dash_r, dash_l, top_label, bot_label
    return g


def _lowest(m):
    return min(m[0], key=lambda s: s.get_center()[1])


def _highest(m):
    return max(m[0], key=lambda s: s.get_center()[1])


def _strike(glyph):
    return Line(glyph.get_corner(DL) + 0.06 * (DL), glyph.get_corner(UR) + 0.06 * UR).set_stroke(GOLD, 4)


class Ch7S5G4(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c7.g4.1
    def clip1(self):
        s1 = load_scene("ch7_s1_intro")
        with self.say("c7.g4.1") as c:
            row = s1.card_row(lit=True)
            self.play(FadeIn(row), run_time=0.6)  # early: the card row is the scene's opening shot
            self.remove(row)
            self.add(*row)
            hero = s1.g_card(4, lit=True)
            hero.scale_to_fit_height(4.5).move_to(HERO_C)
            src = row[3]
            self.play(*during([FadeOut(m) for m in row[:3]], 0, 0.45),
                      *during(Transform(src, hero), 0.3, 1.0), run_time=1.8)
            self.hero = src
            c.wait_until("stop")
            icon = s1.pause_icon(height=1.2).move_to([4.5, 0.3, 0])
            self.play(FadeIn(icon, scale=0.8), run_time=0.8)
            self.icon = icon

    # ------------------------------------------------------------ c7.g4.2
    def clip2(self):
        with self.say("c7.g4.2") as c:
            L1 = MathTex(r"x = \tanh y = \frac{e^{y} - e^{-y}}{e^{y} + e^{-y}}", tex_to_color_map=EC, font_size=44)
            L2 = MathTex(r"x\,(e^{y} + e^{-y}) = e^{y} - e^{-y}", tex_to_color_map=EC, font_size=44)
            L3 = MathTex(r"(1-x)\,e^{2y} = 1+x", tex_to_color_map={"e^{2y}": GOLD}, font_size=44)
            L4 = MathTex(r"e^{2y} = \frac{1+x}{1-x}", tex_to_color_map={"e^{2y}": GOLD}, font_size=44)
            res = MathTex(r"\tanh^{-1}x = \tfrac{1}{2}\ln\!\Big[\frac{1+x}{1-x}\Big]", r",\quad |x|<1",
                          font_size=48)
            res_box = SurroundingRectangle(res, color=YELLOW, buff=0.25, corner_radius=0.1).set_stroke(YELLOW, 3)
            col = VGroup(L1, L2, L3, L4, res).arrange(DOWN, buff=0.42)
            col.move_to([0, 0.15, 0])
            res.shift(0.2 * DOWN)
            res_box.move_to(res)
            self.res = VGroup(res_box, res)

            sweep_clear(self, *appear(L1))
            c.wait_until("clear the fractions")
            self.play(*appear(L2), run_time=min(1.2, 0.8 * c.until("E to the two why")))
            c.wait_until("E to the two why")
            self.play(*appear(L3), run_time=min(1.2, 0.8 * c.until("over one minus ex")))
            c.wait_until("over one minus ex")
            self.play(*appear(L4), run_time=min(1.2, 0.8 * c.until("log")))
            c.wait_until("log")
            self.play(*appear(res), run_time=1.4)
            self.play(GrowFromCenter(res_box), run_time=0.8)
            c.wait_until("between minus one")
            self.play(FlashAround(res[1], run_time=1.5, time_width=1.5))
            self.chain = [L1, L2, L3, L4]

    # ------------------------------------------------------------ c7.g4.3
    def clip3(self):
        with self.say("c7.g4.3") as c:
            res = self.res
            sweep_clear(self, res.animate.scale(0.8).move_to([0, 3.0, 0]), keep=[res])

            # number line -1 .. 1, both factors positive
            nl = NumberLine(x_range=[-1.5, 1.5, 0.5], length=6.0, include_ticks=False, color=DIM, stroke_width=2)
            nl.move_to([-2.4, 1.0, 0])
            seg = Line(nl.n2p(-1), nl.n2p(1)).set_stroke(GREEN, 6)
            ends = VGroup(*[Circle(radius=0.09).set_stroke(GREEN, 3).set_fill(BG, 1).move_to(nl.n2p(v))
                            for v in (-1, 1)])
            ticks = VGroup(*[MathTex(s, font_size=34).next_to(nl.n2p(v), DOWN, buff=0.25)
                             for s, v in (("-1", -1), ("0", 0), ("1", 1))])
            zero_tick = Line(nl.n2p(0) + 0.1 * UP, nl.n2p(0) + 0.1 * DOWN).set_stroke(DIM, 2)
            numline = VGroup(nl, seg, zero_tick, ends, ticks)
            pos1 = MathTex(r"1+x>0", font_size=40, color=GREEN)
            pos2 = MathTex(r"1-x>0", font_size=40, color=GREEN)
            VGroup(pos1, pos2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([3.4, 0.85, 0])
            ck1 = check_mark().next_to(pos1, RIGHT, buff=0.3)
            ck2 = check_mark().next_to(pos2, RIGHT, buff=0.3)
            self.play(*appear(numline, shift=None), run_time=1.2)
            c.wait_until("both one plus ex")
            self.play(*appear(pos1, ck1, lag=0.3), run_time=1.0)
            c.wait_until("and one minus ex")
            self.play(*appear(pos2, ck2, lag=0.3), run_time=1.0)

            split = MathTex(r"\tanh^{-1}x = \tfrac{1}{2}\Big[\ln(1+x)", r"-", r"\ln(1-x)\Big]", font_size=46)
            split.move_to([0, -1.1, 0])
            c.wait_until("difference of logs")
            self.play(*appear(split), run_time=1.4)

            c.wait_until("first")
            self.play(*during(disappear(numline, pos1, pos2, ck1, ck2), 0, 0.45),
                      *during(split.animate.move_to([0, 1.55, 0]), 0.3, 1.0), run_time=1.5)
            first = MathTex(r"\frac{d}{dx}\ln(1+x) = \frac{1}{1+x}", font_size=44)
            first.move_to([0, 0.25, 0])
            c.wait_until("differentiates")
            self.play(*appear(first), run_time=1.3)

            c.wait_until("second")
            second = MathTex(r"\frac{d}{dx}\ln(1-x) = \frac{1}{1-x}\cdot", font_size=44)
            chip = minus_one_chip(44)
            VGroup(second, chip).arrange(RIGHT, buff=0.18).move_to([0, -1.1, 0])
            self.play(*appear(second), run_time=1.3)
            c.wait_until("which is minus one")
            self.play(GrowFromCenter(chip), run_time=1.0)

            c.wait_until("minus")
            self.play(FlashAround(split[1], color=YELLOW, run_time=1.4, time_width=1.5),
                      FlashAround(chip, color=YELLOW, run_time=1.4, time_width=1.5))
            comb = MathTex(r"\frac{d}{dx}\tanh^{-1}x = \tfrac{1}{2}\Big[\frac{1}{1+x}", r"+",
                           r"\frac{1}{1-x}\Big]", font_size=46)
            comb[1].set_color(YELLOW)
            comb.move_to([0, -2.75, 0])
            c.wait_until("makes a plus")
            self.play(*appear(comb), run_time=min(1.2, c.until()))
            self.comb = comb
            self.chip = chip

    # ------------------------------------------------------------ c7.g4.4
    def clip4(self):
        with self.say("c7.g4.4") as c:
            comb = self.comb
            sweep_clear(self, comb.animate.move_to([0, 2.6, 0]), keep=[comb], run_time=1.4)
            c2 = MathTex(r"= \tfrac{1}{2}\cdot\frac{(1-x)+(1+x)}{(1+x)(1-x)}", font_size=46)
            c2.move_to([0.4, 0.9, 0])
            self.play(*appear(c2), run_time=1.2)
            eq = MathTex("=", font_size=46)
            half = MathTex(r"\tfrac{1}{2}", font_size=46)
            dot = MathTex(r"\cdot", font_size=46)
            frac = MathTex(r"\frac{2}{1-x^{2}}", font_size=46)
            c3 = VGroup(eq, half, dot, frac).arrange(RIGHT, buff=0.16).move_to([0, -0.7, 0])
            c3.align_to(c2, LEFT)
            c.wait_until("the top is two")
            self.play(*appear(c3), run_time=1.1)
            s1, s2 = _strike(_lowest(half)), _strike(_highest(frac))
            c.wait_until("the half cancels")
            self.play(Create(s1), Create(s2), run_time=0.9)

            ans = g4_answer(52)
            ans.move_to([0, -2.55, 0])
            c.wait_until("answer")
            self.play(*appear(ans.tex), run_time=1.3)
            self.play(GrowFromCenter(ans.box), run_time=0.8)
            self.ans = ans

            # the slip
            c.wait_until("slip")
            sweep_clear(self, ans.animate.scale(0.85).move_to([0, 2.8, 0]), keep=[ans], run_time=1.4)
            slip = MathTex(r"\tfrac{1}{2}\Big[\frac{1}{1+x}", r"-", r"\frac{1}{1-x}\Big]", font_size=46, color=RED)
            wrong = MathTex(r"= -\frac{x}{1-x^{2}}", font_size=46, color=RED)
            VGroup(slip, wrong).arrange(RIGHT, buff=0.25).move_to([0, 1.15, 0])
            lg = g4_axes(-2, 2, u=0.7)
            lg.move_to([-2.6, -1.65, 0])
            lcurve = lg.plot(math.atanh, x_range=[-X_ATANH, X_ATANH, 0.01], color=ATANH_C, stroke_width=5)
            llab = MathTex(r"\tanh^{-1}x", font_size=34, color=ATANH_C).next_to(lg, LEFT, buff=0.3)
            rg = g4_axes(-2, 2, u=0.7)
            rg.move_to([2.6, -1.65, 0])
            rcurve = rg.plot(lambda x: 0.5 * math.log(1 - x * x), x_range=[0, math.sqrt(1 - math.exp(-4)), 0.005],
                             color=RED, stroke_width=5)
            rlab = MathTex(r"\text{slope} < 0", font_size=34, color=RED).next_to(rg, RIGHT, buff=0.3)
            self.play(*appear(slip), run_time=1.2)
            self.play(FadeIn(lg), Create(lcurve), FadeIn(llab), run_time=1.2)
            c.wait_until("wrong")
            self.play(*appear(wrong), run_time=1.2)
            c.wait_until("negative for every positive")
            self.play(FadeIn(rg), Create(rcurve), FadeIn(rlab), run_time=1.4)
            c.wait_until("always climbs")
            self.play(VShowPassingFlash(lcurve.copy().set_stroke(YELLOW, 8), time_width=0.5), run_time=1.4)

    # ------------------------------------------------------------ c7.g4.5
    def clip5(self):
        with self.say("c7.g4.5") as c:
            ans = self.ans
            gp = graph_pair(0.75, center=[-3.5, -0.2, 0])
            top, bot = gp.top, gp.bot
            sweep_clear(self, ans.animate.scale(0.82).move_to([3.4, 2.85, 0]),
                        time_span(FadeIn(VGroup(top.ax, bot.ax, gp.dash_r, gp.dash_l)), 0.6, 1.6),
                        keep=[ans], run_time=1.6)
            self.play(Create(top.curve), Create(bot.curve), FadeIn(gp.top_label), FadeIn(gp.bot_label),
                      run_time=1.4)

            # three checks
            def item(txt):
                lab = T(txt, 32)
                ck = check_mark()
                g = VGroup(ck, lab).arrange(RIGHT, buff=0.3)
                return g, lab
            i1, l1 = item("positive everywhere")
            i2, l2 = item("one at the origin")
            i3, l3 = item("blows up at x = ±1")
            VGroup(i1, i2, i3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.2, 0.6, 0])

            c.wait_until(own_word=l1)
            area = bot.ax.get_area(bot.curve, x_range=[-X_BLOW, X_BLOW], color=BLUE, opacity=0.25)
            self.play(FadeIn(area), *appear(i1), run_time=1.3)

            c.wait_until(own_word=l2)
            ydot = Dot(bot.ax.c2p(0, 1), radius=0.1, color=YELLOW)
            one = MathTex("1", font_size=32, color=YELLOW).next_to(bot.ax.c2p(0, 1), UL, buff=0.12)
            tan = Line(top.ax.c2p(-0.9, -0.9), top.ax.c2p(0.9, 0.9)).set_stroke(YELLOW, 4)
            self.play(GrowFromCenter(ydot), FadeIn(one), *appear(i2), run_time=1.2)
            self.play(Create(tan), FlashAround(ydot, run_time=1.2), run_time=1.2)

            c.wait_until(own_word=l3)
            rhalf = bot.ax.plot(lambda x: 1 / (1 - x * x), x_range=[0, X_BLOW, 0.01]).set_stroke(YELLOW, 7)
            lhalf = bot.ax.plot(lambda x: 1 / (1 - x * x), x_range=[-X_BLOW, 0, 0.01]).set_stroke(YELLOW, 7)
            lhalf.reverse_points()
            self.play(*appear(i3), run_time=1.0)
            self.play(VShowPassingFlash(rhalf, time_width=0.5), VShowPassingFlash(lhalf, time_width=0.5),
                      run_time=1.5)

            # the flip
            f1 = MathTex(r"x = \tanh y", font_size=42)
            f2 = MathTex(r"\frac{dx}{dy} = \operatorname{sech}^{2} y", font_size=42)
            tag = T("sheet H2(g), next lecture", 28, color=DIM)
            f3a = MathTex(r"= 1-\tanh^{2} y", font_size=42)
            f3b = MathTex(r"= 1-x^{2}", font_size=42)
            f3 = VGroup(f3a, f3b).arrange(RIGHT, buff=0.25)
            f4 = MathTex(r"\frac{dy}{dx} = \frac{1}{dx/dy} = \frac{1}{1-x^{2}}", font_size=42)
            f1.move_to([3.4, 1.5, 0])
            f2.move_to([3.4, 0.45, 0])
            tag.move_to([3.4, -0.4, 0])
            f3.move_to([3.4, -1.35, 0])
            f4.move_to([3.4, -2.85, 0])
            c.wait_until("With ex equal")
            self.play(*during(disappear(i1, i2, i3), 0, 0.45), *during(appear(f1), 0.5, 1.0), run_time=1.4)
            c.wait_until("the derivative of ex")
            self.play(*appear(f2), run_time=1.3)
            c.wait_until("from question H two")
            self.play(*appear(tag), run_time=0.9)  # early: the sheet tag reads with "from question H two"

            c.wait_until("sech")
            self.play(*appear(f3a), run_time=1.2)
            c.wait_until("which is one minus ex squared")
            self.play(*appear(f3b), run_time=1.1)

            c.wait_until("recip")
            self.play(*appear(f4), run_time=min(1.2, c.until("same answer")))
            self.play(FlashAround(f4[0][-6:], run_time=1.4, time_width=1.5),
                      FlashAround(ans.box, run_time=1.4, time_width=1.5, buff=0.05))
        self.wait(2.5)
