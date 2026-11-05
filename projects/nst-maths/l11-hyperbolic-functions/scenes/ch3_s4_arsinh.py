"""Chapter 3, scene 4: undoing sinh: the horizontal-line test, the arsinh derivation, the x = 3/4
check and the mirror graph. Clips c3.arsinh.1 – c3.arsinh.6.

Shared (load_scene("ch3_s4_arsinh")):
  fig25d_shot()      Figure 25(d) on ch3_s2_cosh's fig_axes(): cosh TEAL, sinh SINH_C, tanh TANH_C
                     (a darker teal), labels \\cosh x \\sinh x \\tanh x at the right ends, YELLOW
                     dashed y = x. Attributes .ax .cosh .sinh .tanh .yline .labels (dict). Scene 3
                     ends on exactly this (handover); this scene opens on it.
  check_card(size=44) the x = 3/4 check card centred at ORIGIN (DIM rounded frame). Attributes
                     .frame .x .root .plus .minus .strike .y .verify .tick .rows.
                     s5/s6 build their cards in this style; s6 brings it back small.
  sinh_chain(size=48) the whole derivation as a column (L1 .. L6, the x 2e^y margin beside L2),
                     centred at ORIGIN; attributes .lines (list), .times, .result.
  TANH_C, CHAIN_X, ROW_Y and the line builders l1() .. l6().
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

C1 = load_scene("ch1_s2_define")
F1 = load_scene("ch1_s3_family")
G3 = load_scene("ch7_s4_g3")
S2 = load_scene("ch3_s2_cosh")

SINH_C = C1.SINH_C
INV_C = G3.INV_C
TANH_C = "#34A88C"                     # a third, darker teal: tanh
mt = F1.mt


# ---------------------------------------------------------------- Figure 25(d)
def fig25d_shot():
    ax = S2.fig_axes()             # s2's Figure 25 axes, so 25(a) and 25(d) sit in one place
    ch = C1.cosh_curve(ax)
    sh = C1.sinh_curve(ax)
    th = C1._plot(ax, math.tanh, C1.X_LO, C1.X_HI, TANH_C, 6)
    yl = G3.dline(ax, (-2.5, -2.5), (2.5, 2.5), YELLOW, 3)
    lc = C1.curve_label(ax, "cosh")
    ls = C1.curve_label(ax, "sinh")
    # right of the plot, between the cosh label and the end of y = x: clear of the dashed line and of
    # c3.arsinh.1's sweep (its line ends at x = 2.5, its dots ride the curve)
    ls.next_to(ax.c2p(2.45, 3.35), RIGHT, buff=0.2)
    lt = set_backstroke(MathTex(r"\tanh x", font_size=40, color=TANH_C))
    lt.next_to(ax.c2p(2.5, math.tanh(2.5)), RIGHT, buff=0.2)
    g = VGroup(ax, yl, th, ch, sh, lt, lc, ls)
    g.ax, g.cosh, g.sinh, g.tanh, g.yline = ax, ch, sh, th, yl
    g.labels = {"cosh": lc, "sinh": ls, "tanh": lt}
    return g


# ---------------------------------------------------------------- the sinh graphs (equal units)
BIG_U, BIG_C = 0.82, np.array([-1.6, -0.1, 0])
CORNER_U, CORNER_C = 0.27, np.array([-5.45, 2.45, 0])
S4 = math.asinh(4)


def sinh_graph(unit, center, width=5):
    ax = G3.eq_axes((-4, 4), (-4, 4), unit, center, ticks=False)
    sh = G3.fcurve(ax, math.sinh, -S4, S4, TEAL, width)
    g = VGroup(ax, sh)
    g.ax, g.sinh = ax, sh
    return g


# ---------------------------------------------------------------- the derivation
SZ = 48
CHAIN_X = -0.6
ROW_Y = (2.6, 1.55, 0.5, -0.55, -1.6)
NOTE_X = 4.6


def l1(size=SZ):   # y = sinh^-1 x <=> sinh y = x
    return mt(r"y = \sinh^{-1} x \iff \sinh y = x", size, cmap={(2, 8): SINH_C, (11, 15): SINH_C})


def l2(size=SZ):   # 1/2 (e^y - e^-y) = x
    return mt(r"\tfrac{1}{2}\left(e^{y} - e^{-y}\right) = x", size, cmap={(4, 6): GOLD, (7, 10): PURPLE})


def times2(size=SZ):
    return mt(r"\times\, 2e^{y}", size - 6, DIM, cmap={(2, 4): GOLD})


def l3(size=SZ):
    return mt(r"e^{2y} - 2x\,e^{y} - 1 = 0", size, cmap={(0, 3): GOLD, (6, 8): GOLD})


def l3q(size=SZ):
    return mt(r"\left(e^{y}\right)^2 - 2x\left(e^{y}\right) - 1 = 0", size,
              cmap={(1, 3): GOLD, (9, 11): GOLD})


def l4(size=SZ):
    return mt(r"e^{y} = x \pm \sqrt{x^2 + 1}", size, cmap={(0, 2): GOLD})


def l5(size=SZ):
    return mt(r"e^{y} = x + \sqrt{x^2 + 1}", size, cmap={(0, 2): GOLD, (3, 11): GREEN})


def l6(size=52):
    return mt(r"y = \sinh^{-1} x = \ln\left(x + \sqrt{x^2 + 1}\right)", size, cmap={(2, 8): SINH_C})


def row(m, i):
    return m.move_to([CHAIN_X, ROW_Y[i], 0])


def sinh_chain(size=SZ):
    """The whole derivation, as laid out in this scene before it shrinks, centred at ORIGIN."""
    ls = [row(f(size), i) for i, f in enumerate((l1, l2, l3q, l4, l5))]
    tm = times2(size).next_to(ls[1], RIGHT, buff=0.7)
    res = l6(size + 4).move_to([CHAIN_X, ROW_Y[4] - 1.25, 0])
    g = VGroup(*ls, tm, res).move_to(ORIGIN)
    g.lines, g.times, g.result = ls + [res], tm, res
    return g


def warning_card(size=44):
    """ch1's RED inverse warning (inverse_card styling), for sinh."""
    tex = mt(r"\sinh^{-1} x \ne \dfrac{1}{\sinh x}", size, RED)
    box = SurroundingRectangle(tex, color=RED, buff=0.35, corner_radius=0.15).set_stroke(RED, 3)
    card = VGroup(box, tex)
    card.tex, card.box = tex, box
    return card


def strike(m, color=RED):
    return Line(m.get_left() + 0.08 * LEFT, m.get_right() + 0.08 * RIGHT).set_stroke(color, 5)


# ---------------------------------------------------------------- the x = 3/4 check card
def check_card(size=44):
    x = mt(r"x = \tfrac34", size, cmap={(2, 5): GOLD})
    root = mt(r"\sqrt{\tfrac{9}{16} + 1} = \tfrac54", size)
    plus = mt(r"\tfrac34 + \tfrac54 = 2", size, GREEN)
    minus = mt(r"\tfrac34 - \tfrac54 = -\tfrac12", size, RED)
    pair = VGroup(plus, minus).arrange(RIGHT, buff=1.0)
    y = mt(r"y = \ln 2", size, cmap={(4, 5): GREEN})
    verify = mt(r"\sinh(\ln 2) = \dfrac{2 - \frac12}{2} = \tfrac34", size, cmap={(0, 4): SINH_C})
    rows = VGroup(x, root, pair, y, verify).arrange(DOWN, buff=0.32)
    tick = check_mark().next_to(verify, RIGHT, buff=0.3)
    # a diagonal strike: a level one lies on the fraction bars and swallows the "-" and "=" signs
    st = Line(minus.get_corner(DL) + 0.1 * DL, minus.get_corner(UR) + 0.1 * UR).set_stroke(RED, 5)
    frame = SurroundingRectangle(VGroup(rows, tick), buff=0.35, corner_radius=0.2).set_stroke(DIM, 2)
    card = VGroup(frame, x, root, plus, minus, st, y, verify, tick).move_to(ORIGIN)
    card.frame, card.x, card.root, card.plus, card.minus = frame, x, root, plus, minus
    card.strike, card.y, card.verify, card.tick = st, y, verify, tick
    card.rows = [x, root, plus, minus, y, verify]
    return card


class Arsinh(NarratedScene):
    def construct(self):
        fig = fig25d_shot()
        self.add(*fig.submobjects)
        ax = fig.ax
        self.clip_line(fig, ax)
        self.clip_def()
        self.clip_roots()
        self.clip_result()
        self.clip_check()
        self.clip_graph()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.arsinh.1
    def clip_line(self, fig, ax):
        lab = fig.labels
        h = ValueTracker(-2.5)

        def hline():
            return Line(ax.c2p(-2.5, h.get_value()), ax.c2p(2.5, h.get_value())).set_stroke(YELLOW, 4)

        def on(f):
            return lambda: Dot(ax.c2p(f(h.get_value()), h.get_value()), radius=0.11, color=YELLOW).set_z_index(3)

        with self.say("c3.arsinh.1") as c:
            c.wait_until("line")
            line = always_redraw(hline)
            d_s = always_redraw(on(math.asinh))
            self.play(*set_alpha([fig.cosh, fig.tanh, fig.yline, lab["cosh"], lab["tanh"]], DIMMED),
                      FadeIn(line), FadeIn(d_s), run_time=1.0)
            self.play(h.animate.set_value(4.5), run_time=max(1.0, 0.95 * c.until("mono")),
                      rate_func=linear)
            note = mt(r"e^{x}\nearrow \qquad e^{-x}\searrow", 44, cmap={(0, 2): GOLD, (3, 6): PURPLE})
            note.move_to(ax.c2p(1.45, -2.0))
            self.play(*appear(note), run_time=1.0)
            self.play(h.animate.set_value(-1.6), run_time=max(1.0, 0.9 * c.until("tanh")),
                      rate_func=linear)
            c.wait_until("tanh")
            self.remove(d_s)
            self.play(*set_alpha([fig.sinh, lab["sinh"]], DIMMED),
                      *set_alpha([fig.tanh, lab["tanh"]], 1),
                      h.animate.set_value(0.55), run_time=1.0)
            d_t = always_redraw(on(math.atanh))
            self.play(FadeIn(d_t), run_time=0.4)
            self.play(h.animate.set_value(-0.6), run_time=max(0.5, 0.9 * c.until("cosh")))
            c.wait_until("cosh")
            self.remove(d_t)
            self.play(*set_alpha([fig.tanh, lab["tanh"]], DIMMED),
                      *set_alpha([fig.cosh, lab["cosh"]], 1),
                      h.animate.set_value(2.5), run_time=1.2)
            a = math.acosh(2.5)
            dots = [Dot(ax.c2p(s * a, 2.5), radius=0.11, color=YELLOW).set_z_index(3) for s in (-1, 1)]
            rings = [Circle(radius=0.3).set_stroke(RED, 4).move_to(d) for d in dots]
            self.play(*[FadeIn(d) for d in dots], *[GrowFromCenter(r) for r in rings], run_time=1.0)
            self.fig, self.rings = fig, rings     # the cosh picture holds through "So cosh gets the next
                                                  # scene to itself"; c3.arsinh.2 clears it

    # ------------------------------------------------------------ c3.arsinh.2
    def clip_def(self):
        fig = self.fig
        with self.say("c3.arsinh.2") as c:
            L1 = row(l1(), 0)
            corner = sinh_graph(CORNER_U, CORNER_C, width=3)
            self.corner = corner
            keep = {fig.ax, fig.sinh}
            leaving = [m for m in self.mobjects if m not in keep]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.4),
                      *during([ReplacementTransform(fig.ax, corner.ax),
                               ReplacementTransform(fig.sinh, corner.sinh)], 0.2, 0.75),
                      *during(appear(L1), 0.6, 1), run_time=2.0)
            settle(self, corner)
            c.wait_until("minus")
            warn = warning_card().move_to([NOTE_X - 0.1, 0.6, 0])
            self.play(*appear(warn), FlashAround(VGroup(*L1[0][6:8]), color=RED, run_time=1.5,
                                                 time_width=1.5), run_time=1.5)
            c.wait_until("expo")
            L2 = row(l2(), 1)
            derive(self, L1, L2, run_time=min(2.0, c.until("times")))
            c.wait_until("times")
            tm = times2().next_to(L2, RIGHT, buff=0.7)
            self.play(*during(disappear(warn), 0, 0.45), *during(appear(tm), 0.5, 1), run_time=1.4)
            c.wait_until("square")
            n1 = mt(r"e^{y}\cdot e^{y} = e^{2y}", 42, cmap={(0, 2): GOLD, (3, 5): GOLD, (6, 9): GOLD})
            n1.move_to([NOTE_X, ROW_Y[2], 0])
            self.play(*appear(n1), run_time=1.0)
            c.wait_until("one")
            n2 = mt(r"e^{y}\cdot e^{-y} = 1", 42, cmap={(0, 2): GOLD, (3, 6): PURPLE})
            n2.move_to([NOTE_X, ROW_Y[3], 0])
            n2.align_to(n1, LEFT)
            self.play(*appear(n2), run_time=1.0)
            L3 = row(l3(), 2)
            derive(self, L2, L3, run_time=min(2.0, c.until("quad")))
            c.wait_until("quad")
            L3q = row(l3q(), 2)
            # e^{2y} -> (e^y)^2 as a whole term, in place; the shared glyphs slide, e^y gains brackets
            o, q = L3[0], L3q[0]
            slides = [o[i].animate.move_to(q[j]) for i, j in
                      ((3, 5), (4, 6), (5, 7), (6, 9), (7, 10), (8, 12), (9, 13), (10, 14), (11, 15))]
            self.play(*during(disappear(n1, n2), 0, 0.4),
                      *during([FadeOut(o[k]) for k in range(3)], 0, 0.4),
                      *during(slides, 0.1, 0.55),
                      *during([FadeIn(q[k]) for k in (0, 1, 2, 3, 4, 8, 11)], 0.55, 1),
                      run_time=1.5)
            self.remove(*L3.get_family())
            self.add(L3q)
            boxes = [SurroundingRectangle(VGroup(*L3q[0][a:b]), buff=0.07).set_stroke(YELLOW, 3)
                     for a, b in ((0, 4), (8, 12))]
            qlab = mt(r"\text{a quadratic in } e^{y}", 38, YELLOW).move_to([NOTE_X, ROW_Y[2], 0])
            self.play(*[FadeIn(b) for b in boxes], *appear(qlab), run_time=1.0)
            self.chain = [L1, L2, tm, L3q]
            self.qbits = [qlab, *boxes]

    # ------------------------------------------------------------ c3.arsinh.3
    def clip_roots(self):
        with self.say("c3.arsinh.3") as c:
            L4 = row(l4(), 3)
            derive(self, self.chain[3], L4, run_time=2.0)
            c.wait_until("pos")
            p1 = mt(r"e^{y} > 0", 42, cmap={(0, 2): GOLD}).move_to([NOTE_X, ROW_Y[2], 0])
            self.play(*during(disappear(*self.qbits), 0, 0.45), *during(appear(p1), 0.5, 1), run_time=1.4)
            c.wait_until("bigger")
            p2 = mt(r"\sqrt{x^2 + 1} > |x|", 42).move_to([NOTE_X, ROW_Y[3], 0])
            self.play(*appear(p2), run_time=1.0)
            c.wait_until("neg")
            p3 = mt(r"x - \sqrt{x^2 + 1} < 0", 42, RED).move_to([NOTE_X, ROW_Y[4], 0])
            self.play(*appear(p3), run_time=1.0)
            c.wait_until("reject")
            st = strike(p3)
            self.play(GrowFromEdge(st, LEFT), run_time=0.8)
            self.chain.append(L4)
            self.notes = [p1, p2, p3, st]

    # ------------------------------------------------------------ c3.arsinh.4
    def clip_result(self):
        with self.say("c3.arsinh.4") as c:
            self.play(*disappear(*self.notes), run_time=0.8)
            L5 = row(l5(), 4)
            derive(self, self.chain[-1], L5, run_time=min(2.0, c.until("take logs")))
            self.chain.append(L5)
            c.wait_until("take logs")
            P = np.array([CHAIN_X, ROW_Y[0] + 0.35, 0])
            self.play(*[m.animate.scale(0.7, about_point=P).set_opacity(0.4) for m in self.chain],
                      run_time=1.0)
            c.wait_until("result")
            L6 = l6().move_to([CHAIN_X, -1.45, 0])
            derive(self, L5, L6, run_time=min(2.0, 0.6 * c.until("every")))
            box = SurroundingRectangle(L6, buff=0.25).set_stroke(YELLOW, 3)
            tag = T("(96)", 36, DIM).next_to(box, RIGHT, buff=0.3)
            self.play(GrowFromCenter(box), *appear(tag, shift=None), run_time=1.0)
            c.wait_until("every")
            every = mt(r"\text{every real } x", 40, GREEN).next_to(box, DOWN, buff=0.45)
            self.play(*appear(every), run_time=1.0)
            self.result = [L6, box, tag]
            self.every = every

    # ------------------------------------------------------------ c3.arsinh.5
    def clip_check(self):
        with self.say("c3.arsinh.5") as c:
            card = check_card().move_to([0, -0.75, 0])
            L6, box, tag = self.result
            top = np.array([0, 3.0, 0]) - VGroup(L6, box).get_center()
            self.play(*during([FadeOut(m) for m in self.chain + [self.every]], 0, 0.5),
                      *during([m.animate.scale(0.8, about_point=VGroup(L6, box).get_center()).shift(top)
                               for m in (L6, box, tag)], 0.2, 0.85),
                      *during(appear(card.frame, card.x), 0.55, 1), run_time=1.8)
            c.wait_until("the square root")
            self.play(*appear(card.root), run_time=1.0)
            c.wait_until("the roots are")
            self.play(*appear(card.plus, card.minus, lag=0.5), run_time=1.4)
            c.wait_until("verify")
            self.play(Create(card.strike), *during(appear(card.y), 0.35, 1), run_time=1.2)
            c.wait_until("and shine of")
            self.play(*appear(card.verify), run_time=1.2)
            c.wait_until("three quarters", nth=1)
            self.play(GrowFromCenter(card.tick), run_time=0.8)
            self.card = card

    # ------------------------------------------------------------ c3.arsinh.6
    def clip_graph(self):
        with self.say("c3.arsinh.6") as c:
            c.wait_until("reflecting")
            big = sinh_graph(BIG_U, BIG_C)
            ax = big.ax
            corner = self.corner
            leaving = [m for m in self.mobjects if m is not corner]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.45),
                      *during([ReplacementTransform(corner.ax, big.ax),
                               ReplacementTransform(corner.sinh, big.sinh)], 0.25, 1), run_time=1.6)
            settle(self, big)
            mirror = G3.mirror_line(ax, -4, 4)
            yx = G3.lab("y = x", DIM, 32).next_to(ax.c2p(4, 4), RIGHT, buff=0.15)
            ls = G3.lab(r"\sinh x", TEAL, 40).next_to(ax.c2p(2.0, 3.65), LEFT, buff=0.3)
            self.play(Create(mirror), *appear(yx, ls, lag=0.3), run_time=1.2)
            c.wait_until("mirror")
            cp = big.sinh.copy()
            self.play(G3.flip(cp, ax, run_time=2.0))
            ash = G3.pcurve(ax, math.sinh, lambda t: t, -S4, S4, INV_C, 5)
            la = G3.lab(r"\sinh^{-1} x", INV_C, 40).next_to(ax.c2p(4, S4), RIGHT, buff=0.2)
            self.play(ReplacementTransform(cp, ash), *appear(la), run_time=1.0)
            c.wait_until("slope one")
            o = G3.kdot(ax, 0, 0)
            tg = G3.tangent(ax, 0, 0, 1.0, half=0.9)
            self.play(FadeIn(o), Create(tg), run_time=1.0)
            c.wait_until("names")
            ob = T("other books:", 30, DIM)
            nm = mt(r"\sinh^{-1} x = \operatorname{arsinh} x", 40, DIM)
            VGroup(ob, nm).arrange(DOWN, buff=0.25, aligned_edge=LEFT).move_to([4.6, -1.6, 0])
            self.play(*appear(ob, nm, lag=0.3), run_time=1.2)
        self.wait(2.0)
