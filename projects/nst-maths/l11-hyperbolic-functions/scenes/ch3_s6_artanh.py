"""Chapter 3, scene 6: Example 34, undoing tanh: the derivation, |x| < 1, the x = 3/5 check, the
mirror graph and the three logarithms. Clips c3.artanh.1 – c3.artanh.4.

Shared (load_scene("ch3_s6_artanh")):
  cosh_card(size=44)   old stand-in x = 5/4 card (unused now: the scene shows s5's cosh_check_card()).
  tanh_card(size=44)   this scene's x = 3/5 card; .frame .x .ratio .log .tick .rows.
  boxed(tex_mob, tag)  a result boxed YELLOW with its DIM tag on the right; .tex .box .tag.
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

S4 = load_scene("ch3_s4_arsinh")
S5 = load_scene("ch3_s5_arcosh")
G3 = load_scene("ch7_s4_g3")

mt = S4.mt
TANH_C = S4.TANH_C
SINH_C = S4.SINH_C
INV_C = G3.INV_C
LGOLD_C = G3.LGOLD_C

SZ = 54
CX = 0.0
ROWS = (1.75, 0.2, -1.35)


# ---------------------------------------------------------------- the chain
def l1(size=SZ):
    return mt(r"x = \tanh y = \dfrac{e^{y} - e^{-y}}{e^{y} + e^{-y}}", size,
              cmap={(2, 6): TANH_C, (8, 10): GOLD, (11, 14): PURPLE, (15, 17): GOLD, (18, 21): PURPLE})


def l2(size=SZ):
    return mt(r"x\left(e^{y} + e^{-y}\right) = e^{y} - e^{-y}", size,
              cmap={(2, 4): GOLD, (5, 8): PURPLE, (10, 12): GOLD, (13, 16): PURPLE})


def times_ey(size=SZ):
    return mt(r"\times\, e^{y}", size - 6, DIM, cmap={(1, 3): GOLD})


def l3(size=SZ):
    return mt(r"x\left(e^{2y} + 1\right) = e^{2y} - 1", size, cmap={(2, 5): GOLD, (9, 12): GOLD})


def l4(size=SZ):
    return mt(r"(1 - x)\,e^{2y} = 1 + x", size, cmap={(5, 8): GOLD})


def l5(size=SZ):
    return mt(r"e^{2y} = \dfrac{1 + x}{1 - x}", size, cmap={(0, 3): GOLD})


def l6(size=52):
    return mt(r"y = \tanh^{-1} x = \tfrac12 \ln\left[\dfrac{1 + x}{1 - x}\right], \quad |x| < 1", size,
              cmap={(2, 8): TANH_C})


def l97(size=52):
    return mt(r"y = \cosh^{-1} x = \ln\left(x + \sqrt{x^2 - 1}\right)", size, cmap={(2, 8): TEAL})


LN = {"96": (10, 12), "97": (10, 12), "34": (13, 15)}


def boxed(tex, tag, size=36):
    box = SurroundingRectangle(tex, buff=0.25).set_stroke(YELLOW, 3)
    t = T(tag, size, DIM).next_to(box, RIGHT, buff=0.3)
    g = VGroup(tex, box, t)
    g.tex, g.box, g.tag = tex, box, t
    return g


# ---------------------------------------------------------------- check cards (s4's style)
def cosh_card(size=44):
    strike = S4.strike
    x = mt(r"x = \tfrac54", size, cmap={(2, 5): GOLD})
    root = mt(r"\sqrt{\tfrac{25}{16} - 1} = \tfrac34", size)
    plus = mt(r"\tfrac54 + \tfrac34 = 2", size, GREEN)
    minus = mt(r"\tfrac54 - \tfrac34 = \tfrac12", size, RED)
    pair = VGroup(plus, minus).arrange(RIGHT, buff=1.0)
    y = mt(r"y = \ln 2", size, cmap={(4, 5): GREEN})
    verify = mt(r"\cosh(\ln 2) = \dfrac{2 + \frac12}{2} = \tfrac54", size, cmap={(0, 4): TEAL})
    rows = VGroup(x, root, pair, y, verify).arrange(DOWN, buff=0.32)
    tick = check_mark().next_to(verify, RIGHT, buff=0.3)
    st = strike(minus)
    frame = SurroundingRectangle(VGroup(rows, tick), buff=0.35, corner_radius=0.2).set_stroke(DIM, 2)
    card = VGroup(frame, x, root, plus, minus, st, y, verify, tick).move_to(ORIGIN)
    card.frame, card.x, card.root, card.plus, card.minus = frame, x, root, plus, minus
    card.strike, card.y, card.verify, card.tick = st, y, verify, tick
    card.rows = [x, root, plus, minus, y, verify]
    return card


def tanh_card(size=44):
    x = mt(r"x = \tfrac35", size, cmap={(2, 5): GOLD})
    ratio = mt(r"\dfrac{1 + \frac35}{1 - \frac35} = 4", size, cmap={(12, 13): GOLD})
    log = mt(r"\tfrac12 \ln 4 = \ln 2", size, cmap={(7, 10): GREEN})
    rows = VGroup(x, ratio, log).arrange(DOWN, buff=0.4)
    tick = check_mark().next_to(log, RIGHT, buff=0.3)
    frame = SurroundingRectangle(VGroup(rows, tick), buff=0.35, corner_radius=0.2).set_stroke(DIM, 2)
    card = VGroup(frame, x, ratio, log, tick).move_to(ORIGIN)
    card.frame, card.x, card.ratio, card.log, card.tick = frame, x, ratio, log, tick
    card.rows = [x, ratio, log]
    return card


# ---------------------------------------------------------------- the domain
NL_U = 1.2


def number_line(center):
    c = np.array(center, dtype=float)

    def p(v):
        return c + v * NL_U * UP

    base = Line(p(-1.6), p(1.6)).set_stroke(DIM, 3)
    ticks = [Line(p(v) + 0.1 * LEFT, p(v) + 0.1 * RIGHT).set_stroke(DIM, 3) for v in (-1, 0, 1)]
    labs = [MathTex(s, font_size=36, color=FG).next_to(p(v), LEFT, buff=0.3)
            for s, v in (("-1", -1), ("0", 0), ("1", 1))]
    xl = MathTex("x", font_size=40).next_to(p(1.6), UP, buff=0.15)
    green = Line(p(-1), p(1)).set_stroke(GREEN, 9)
    holes = [Circle(radius=0.13).set_stroke(GREEN, 4).set_fill(BG, 1).move_to(p(v)).set_z_index(2)
             for v in (-1, 1)]
    g = VGroup(base, *ticks, *labs, xl, green, *holes)
    g.base, g.ticks, g.labs, g.xl, g.green, g.holes = base, ticks, labs, xl, green, holes
    return g


def tanh_band(center):
    ax = G3.eq_axes((-2.2, 2.2), (-1.6, 1.6), NL_U, center, ticks=False)
    hp = G3.dline(ax, (-2.2, 1), (2.2, 1), GOLD)
    hm = G3.dline(ax, (-2.2, -1), (2.2, -1), PURPLE)
    th = G3.fcurve(ax, math.tanh, -2.2, 2.2, TEAL, 5)
    lb = G3.lab(r"\tanh x", TEAL, 36).next_to(ax.c2p(1.2, -0.25), DOWN, buff=0.1)
    g = VGroup(ax, hp, hm, th, lb)
    g.ax, g.hp, g.hm, g.tanh, g.label = ax, hp, hm, th, lb
    return g


class Artanh(NarratedScene):
    def construct(self):
        self.clip_chain()
        self.clip_result()
        self.clip_check()
        self.clip_graph()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.artanh.1
    def clip_chain(self):
        with self.say("c3.artanh.1") as c:
            head = T("Example 34", 48, YELLOW)
            sub = T("Identity for inverse hyperbolic tangent", 32, DIM)
            VGroup(head, sub).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).move_to([0, 3.35, 0])
            c.wait_until("example")
            self.play(*appear(head, sub, lag=0.4), run_time=1.4)  # early: the notes' title is shown with its heading
            self.head = [head, sub]
            c.wait_until("write")
            L1 = l1().move_to([CX, ROWS[0], 0])
            self.play(*appear(L1), run_time=1.5)
            c.wait_until("through")
            L2 = l2().move_to([CX, ROWS[1], 0])
            derive(self, L1, L2, run_time=min(2.0, c.until("ey")))
            c.wait_until("ey")
            tm = times_ey().next_to(L2, RIGHT, buff=0.7)
            self.play(*appear(tm), run_time=1.0)
            L3 = l3().move_to([CX, ROWS[2], 0])
            derive(self, L2, L3, run_time=min(2.0, c.until("nosq")))
            c.wait_until("two why")
            self.play(*[FlashAround(VGroup(*L3[0][a:b]), color=GOLD, run_time=1.5, time_width=1.5)
                        for a, b in ((2, 5), (9, 12))], run_time=1.5)
            c.wait_until("plain number")
            self.play(*[FlashAround(L3[0][i], color=YELLOW, run_time=1.5, time_width=1.5)
                        for i in (6, 13)], run_time=1.5)
            self.chain = [L1, L2, tm, L3]

    # ------------------------------------------------------------ c3.artanh.2
    def clip_result(self):
        with self.say("c3.artanh.2") as c:
            L1, L2, tm, L3 = self.chain
            self.play(*during(disappear(L1, L2, tm), 0, 0.45),
                      *during([L3.animate.move_to([CX, ROWS[0], 0])], 0.35, 1), run_time=1.4)
            L4 = l4().move_to([CX, ROWS[1], 0])
            derive(self, L3, L4, run_time=min(2.0, c.until("you get")))
            c.wait_until("divide")
            L5 = l5().move_to([CX, ROWS[2], 0])
            derive(self, L4, L5, run_time=2.0)
            c.wait_until("log")
            P = np.array([CX, 2.4, 0])
            self.play(*[m.animate.scale(0.7, about_point=P).set_opacity(0.4) for m in (L3, L4)],
                      L5.animate.scale(0.7, about_point=P), run_time=1.0)
            L6 = l6().move_to([CX, -1.9, 0])
            derive(self, L5, L6, run_time=min(2.0, 0.9 * c.until("result")))
            c.wait_until("result")
            box = SurroundingRectangle(L6, buff=0.25).set_stroke(YELLOW, 3)
            self.play(GrowFromCenter(box), L5.animate.set_opacity(0.4), run_time=1.0)
            c.wait_until("ratio")
            self.play(FlashAround(VGroup(*L6[0][15:24]), run_time=1.5, time_width=1.5))
            self.chain = [L3, L4, L5]
            self.result = [L6, box]

    # ------------------------------------------------------------ c3.artanh.3
    def clip_check(self):
        with self.say("c3.artanh.3", gap=1.6) as c:
            L6, box = self.result
            ctr = VGroup(L6, box).get_center()
            up = np.array([0, 2.95, 0]) - ctr
            self.play(*during([FadeOut(m) for m in self.chain + self.head], 0, 0.5),
                      *during([m.animate.scale(0.8, about_point=ctr).shift(up) for m in (L6, box)], 0.2, 1),
                      run_time=1.4)
            self.play(FlashAround(VGroup(*L6[0][25:30]), color=GREEN, run_time=1.5, time_width=1.5))
            nl = number_line([-1.0, -0.6, 0])
            self.play(*appear(nl.base, *nl.ticks, *nl.labs, nl.xl, lag=0.1), run_time=1.0)
            self.play(Create(nl.green), *[FadeIn(h, scale=0.5) for h in nl.holes], run_time=1.2)
            c.wait_until("fits")
            band = tanh_band([-2.5, -0.6, 0])
            self.play(nl.animate.shift(4.9 * LEFT), *during(appear(band.ax, band.tanh, band.label), 0.4, 1),
                      run_time=1.4)
            self.play(Create(band.hp), Create(band.hm), run_time=1.0)
            c.wait_until("check")
            card = tanh_card().move_to([3.9, -0.6, 0])
            self.play(*appear(card.frame, card.x), run_time=1.2)
            c.wait_until("one plus")
            self.play(*appear(card.ratio), run_time=1.2)
            c.wait_until("ln2")
            self.play(*appear(card.log), run_time=1.2)
            c.wait_until("again")
            # the three cards side by side, small
            k = 0.64
            c4 = S4.check_card().scale(k).move_to([-4.55, 0.15, 0])
            c5 = S5.cosh_check_card(44).scale(k)
            c5.move_to([(c4.get_right()[0] + 4.55 - card.width * k / 2) / 2, 0.15, 0])
            self.play(*during([FadeOut(m) for m in (nl, band)], 0, 0.45),
                      *during([card.animate.scale(k).move_to([4.55, 0.15, 0])], 0.2, 0.8),
                      *during(appear(c4, c5, lag=0.3), 0.5, 1), run_time=1.8)
            self.play(*flash([VGroup(*c4.y[0][2:5]), VGroup(*c5.y[0][2:5]), VGroup(*card.log[0][7:10])],
                             color=GREEN, run_time=1.2, time_width=1.5), run_time=1.2)
            head = mt(r"\tanh(\ln 2) =", 48, cmap={(0, 4): TANH_C})
            num = mt(r"3/4", 48, SINH_C)
            den = mt(r"5/4", 48, TEAL)
            bar = Line(LEFT, RIGHT).set_width(max(num.width, den.width) + 0.15).set_stroke(FG, 3)
            frac = VGroup(num, bar, den).arrange(DOWN, buff=0.14)
            tail = mt(r"= \tfrac35", 48, cmap={(1, 4): GOLD})
            VGroup(head, frac, tail).arrange(RIGHT, buff=0.3).move_to([0, -2.75, 0])
            head.set_y(bar.get_y())
            tail.set_y(bar.get_y())
            c.wait_until("shine over cosh")
            self.play(*appear(head, bar, lag=0.2), run_time=1.0)
            c.wait_until("three quarters")
            self.play(*fly(VGroup(*c4.verify[0][-3:]), num, arc=0.9), run_time=1.2)
            c.wait_until("five quarters")
            self.play(*fly(VGroup(*c5.verify[0][-3:]), den, arc=-2.0), run_time=1.2)
            c.wait_until("which is", nth=1)
            tick = check_mark().next_to(tail, RIGHT, buff=0.35)
            self.play(*appear(tail), time_span(GrowFromCenter(tick), 0.5, 1.1),
                      time_span(FlashAround(card.x, time_width=1.5), 0.3, 1.1), run_time=1.1)
            self.cards = (c4, c5)

    # ------------------------------------------------------------ c3.artanh.4
    def clip_graph(self):
        with self.say("c3.artanh.4") as c:
            P = G3.tanh_panel(unit=1.1, center=np.array([-0.6, -0.1, 0]))
            ax = P.ax
            th = P.tanh
            th_l = G3.lab(r"\tanh x", TEAL, 44).next_to(ax.c2p(3, math.tanh(3)), DOWN, buff=0.3)
            hp = G3.dline(ax, (-3, 1), (3, 1), GOLD)
            hm = G3.dline(ax, (-3, -1), (3, -1), PURPLE)
            hp_l = G3.lab("y=1", GOLD, 36).next_to(ax.c2p(-3, 1), LEFT, buff=0.2)
            hm_l = G3.lab("y=-1", PURPLE, 36).next_to(ax.c2p(-3, -1), LEFT, buff=0.2)
            sweep_clear(self, FadeIn(ax), FadeIn(th), FadeIn(hp), FadeIn(hm), run_time=1.4)
            self.play(*appear(th_l, hp_l, hm_l, lag=0.2), run_time=1.0)  # early: the curve and its asymptotes, named as drawn
            c.wait_until("in the line")
            yx = G3.lab("y = x", DIM, 32).next_to(ax.c2p(3, 3), RIGHT, buff=0.15)
            self.play(Create(P.mirror), *appear(yx), run_time=1.0)
            c.wait_until("asym")
            ath = th.copy()
            self.add(ath)
            vp_l = G3.lab("x=1", GOLD, 36).next_to(ax.c2p(1, -2.75), RIGHT, buff=0.2)
            vm_l = G3.lab("x=-1", PURPLE, 36).next_to(ax.c2p(-1, -2.75), LEFT, buff=0.2)
            self.play(G3.flip(ath, ax), G3.flip(hp, ax), G3.flip(hm, ax), th.animate.set_stroke(opacity=0.35),
                      th_l.animate.set_opacity(0.35),
                      *during(disappear(hp_l, hm_l), 0, 0.3), *during(appear(vp_l, vm_l), 0.75, 1),
                      run_time=2.4)  # early: the turned asymptotes are named as they land
            self.remove(hp, hm)
            self.add(P.vp, P.vm)
            ath_l = G3.lab(r"\tanh^{-1}x", INV_C, 44).next_to(ax.c2p(1.3, 1.65), RIGHT, buff=0.1)
            self.play(ath.animate.set_stroke(INV_C, 6), *appear(ath_l), run_time=1.0)
            c.wait_until("shoots up")
            inf_p = G3.lab(r"+\infty", YELLOW, 40).next_to(ax.c2p(1, 2.65), RIGHT, buff=0.25)
            self.play(*appear(inf_p), run_time=1.0)
            c.wait_until("down near")
            inf_m = G3.lab(r"-\infty", YELLOW, 40).next_to(ax.c2p(-1, -1.6), LEFT, buff=0.25)
            self.play(*appear(inf_m), run_time=1.0)
            c.wait_until("near")
            near = G3.dline(ax, (-3, -3), (3, 3), YELLOW, 4)
            dot = G3.kdot(ax, 0, 0)
            self.play(FadeOut(P.mirror), FadeIn(near), th.animate.set_stroke(opacity=1),
                      th_l.animate.set_opacity(1), FadeIn(dot, scale=0.5), run_time=1.2)
            self.play(VShowPassingFlash(near.copy().set_stroke(YELLOW, 8), time_width=0.4), run_time=1.5)

            c.wait_until("logs")
            b96 = boxed(S4.l6(44), "(96)")
            b97 = boxed(l97(44), "(97)")
            b34 = boxed(l6(44), "Example 34", 32)
            VGroup(b96, b97, b34).arrange(DOWN, buff=0.7, aligned_edge=LEFT).move_to([-0.3, 0, 0])
            sweep_clear(self, *[FadeIn(b) for b in (b96, b97, b34)], run_time=1.4)
            for b, key in ((b96, "96"), (b97, "97"), (b34, "34")):
                a, z = LN[key]
                ln = VGroup(*b.tex[0][a:z])
                self.play(FlashAround(ln, run_time=0.9, time_width=1.5),
                          *recolor(list(ln), YELLOW), run_time=0.9)
        self.wait(2.6)
