"""Chapter 3, scene 5: undoing cosh: the arcosh derivation, the x = 5/4 check (both roots kept),
the product of the roots, the +/- log, result (97) and Figure 26. Clips c3.arcosh.1 – c3.arcosh.6.

Shared (load_scene("ch3_s5_arcosh")):
  cosh_check_card(size=38) the x = 5/4 check card, centred at ORIGIN, in ch3_s4's check_card style
                     (DIM rounded frame), final colours (both roots GREEN, ticked). Attributes
                     .frame .x .root .plus .minus .y .verify .tick .rows.
  fig26()            Figure 26, two panels on equal-unit axes (unit 0.6): left cosh x (TEAL) for
                     x in [-acosh 10, acosh 10] (left axes x in [-3, 6]) with a dashed DIM y = x
                     labelled (.mlab); right the sideways U, upper
                     branch INV_C labelled \\ln(x + \\sqrt{x^2-1}), lower PURPLE labelled -\\ln(...),
                     YELLOW dot at (1, 0). Attributes .lax .rax .cosh .mirror .mlab .clab .upper .lower
                     .ulab .llab .dot.
  mini_cosh(center, unit) a small cosh U (DIM axes, TEAL curve); .ax .curve.
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

F1 = load_scene("ch1_s3_family")
G3 = load_scene("ch7_s4_g3")
S4 = load_scene("ch3_s4_arsinh")

INV_C = G3.INV_C
mt = F1.mt

SZ = 48
CHAIN_X = 1.9
ROW_Y = (2.6, 1.55, 0.5, -0.55, -1.6)
SHIFT = 5.3                     # the chain moves this far left when the card comes in
CARD_C = np.array([3.85, 0.9, 0])
SQ_Y = -2.85
ACOSH10 = math.acosh(10)
RT = r"\sqrt{x^2 - 1}"


def row(m, i):
    return m.move_to([CHAIN_X, ROW_Y[i], 0])


# ---------------------------------------------------------------- the derivation lines
def a1(size=SZ):
    return mt(r"y = \cosh^{-1} x \iff \cosh y = x", size, cmap={(2, 8): TEAL, (11, 15): TEAL})


def a2(size=SZ):
    return mt(r"\tfrac{1}{2}\left(e^{y} + e^{-y}\right) = x", size, cmap={(4, 6): GOLD, (7, 10): PURPLE})


def a3(size=SZ):
    return mt(r"e^{2y} - 2x\,e^{y} + 1 = 0", size, cmap={(0, 3): GOLD, (6, 8): GOLD})


def a4(size=SZ):
    return mt(r"e^{y} = x \pm " + RT, size, cmap={(0, 2): GOLD})


def sq_line(size=40):
    return mt(r"\left(x - " + RT + r"\right)\left(x + " + RT + r"\right) = x^2 - \left(x^2 - 1\right) = 1",
              size)


def r1(size=44):
    return mt(r"x - " + RT + r" = \dfrac{1}{x + " + RT + "}", size)


def r2(size=44):
    return mt(r"\ln\left(x - " + RT + r"\right) = -\ln\left(x + " + RT + r"\right)", size)


def r3(size=48):
    return mt(r"y = \pm\ln\left(x + " + RT + r"\right)", size, cmap={(2, 3): YELLOW})


def result_line(size=52):
    return mt(r"y = \cosh^{-1} x = \ln\left(x + " + RT + r"\right)", size, cmap={(2, 8): TEAL})


# ---------------------------------------------------------------- the x = 5/4 check card
def cosh_check_card(size=38):
    x = mt(r"x = \tfrac54", size, cmap={(2, 5): GOLD})
    root = mt(r"\sqrt{\tfrac{25}{16} - 1} = \tfrac34", size)
    plus = mt(r"\tfrac54 + \tfrac34 = 2", size, GREEN)
    minus = mt(r"\tfrac54 - \tfrac34 = \tfrac12", size, GREEN)
    pair = VGroup(plus, minus).arrange(RIGHT, buff=0.8)
    y = mt(r"y = \ln 2 \;\text{ or }\; y = \ln\tfrac12", size, cmap={(5, 7): DIM})
    verify = mt(r"\cosh(\ln 2) = \dfrac{2 + \frac12}{2} = \tfrac54", size, cmap={(0, 4): TEAL})
    rows = VGroup(x, root, pair, y, verify).arrange(DOWN, buff=0.32)
    tick = check_mark().next_to(verify, RIGHT, buff=0.3)
    frame = SurroundingRectangle(VGroup(rows, tick), buff=0.35, corner_radius=0.2).set_stroke(DIM, 2)
    card = VGroup(frame, x, root, plus, minus, y, verify, tick).move_to(ORIGIN)
    card.frame, card.x, card.root, card.plus, card.minus = frame, x, root, plus, minus
    card.y, card.verify, card.tick = y, verify, tick
    card.rows = [x, root, plus, minus, y, verify]
    return card


# ---------------------------------------------------------------- small cosh U
def mini_cosh(center, unit=0.45, width=4):
    ax = G3.eq_axes((-2, 2), (0, 4), unit, center, ticks=False)
    cv = G3.fcurve(ax, math.cosh, -math.acosh(3.9), math.acosh(3.9), TEAL, width)
    g = VGroup(ax, cv)
    g.ax, g.curve = ax, cv
    return g


# ---------------------------------------------------------------- Figure 26
FIG_U = 0.6
LAX_C = np.array([-3.8, -0.2, 0])     # x in [-3, 6]: room for a long y = x mirror
RAX_C = np.array([3.5, -0.2, 0])


def fig26():
    lax = G3.eq_axes((-3, 6), (0, 10), FIG_U, LAX_C)
    rax = G3.eq_axes((0, 10), (-3, 3), FIG_U, RAX_C)
    ch = G3.fcurve(lax, math.cosh, -ACOSH10, ACOSH10, TEAL, 5)
    mirror = G3.mirror_line(lax, 0, 6)
    mlab = G3.lab(r"y = x", DIM, 32).next_to(lax.c2p(6, 6), UR, buff=0.08)
    clab = G3.lab(r"\cosh x", TEAL, 38).next_to(lax.c2p(ACOSH10, 10), RIGHT, buff=0.2)
    up = G3.pcurve(rax, math.cosh, lambda t: t, 0, ACOSH10, INV_C, 5)
    lo = G3.pcurve(rax, math.cosh, lambda t: t, -ACOSH10, 0, PURPLE, 5)
    ulab = G3.lab(r"\ln\left(x + " + RT + r"\right)", INV_C, 36)
    ulab.next_to(rax.c2p(6.2, 3), UP, buff=0.3)
    llab = G3.lab(r"-\ln\left(x + " + RT + r"\right)", PURPLE, 36)
    llab.next_to(rax.c2p(6.2, -3), DOWN, buff=0.3)
    dot = G3.kdot(rax, 1, 0)
    g = VGroup(lax, mirror, mlab, ch, clab, rax, lo, up, dot, ulab, llab)
    g.lax, g.rax, g.cosh, g.mirror, g.mlab, g.clab = lax, rax, ch, mirror, mlab, clab
    g.upper, g.lower, g.ulab, g.llab, g.dot = up, lo, ulab, llab, dot
    return g


class Arcosh(NarratedScene):
    def construct(self):
        self.clip_chain()
        self.clip_test()
        self.clip_product()
        self.clip_recip()
        self.clip_result()
        self.clip_fig()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.arcosh.1
    def clip_chain(self):
        with self.say("c3.arcosh.1") as c:
            s4c = S4.sinh_chain(48)
            s4c.remove(s4c.times)
            s4c.scale(28 / 48).set_color(DIM)
            s4c.move_to([-6.6 + s4c.width / 2, 0.3, 0])
            L1 = row(a1(), 0)
            self.play(*appear(s4c), run_time=1.0)  # early: last scene's chain, for comparison
            self.play(*appear(L1), run_time=1.0)
            c.wait_until("expo")
            L2 = row(a2(), 1)
            derive(self, L1, L2, run_time=min(2.0, c.until("times")))
            c.wait_until("times")
            tm = S4.times2().next_to(L2, RIGHT, buff=0.7)
            self.play(*appear(tm), run_time=1.0)
            c.wait_until("quad")
            L3 = row(a3(), 2)
            derive(self, L2, L3, run_time=min(2.0, c.until("sign")))
            c.wait_until("plus one")
            mine = list(L3[0][8:10])
            theirs = list(s4c.lines[2][0][12:14])
            self.play(FlashAround(VGroup(*mine), color=YELLOW, run_time=1.5, time_width=1.5),
                      *recolor(mine, YELLOW), run_time=1.5)
            c.wait_until("minus one")
            self.play(FlashAround(VGroup(*theirs), color=YELLOW, run_time=1.5, time_width=1.5),
                      *recolor(theirs, YELLOW), run_time=1.5)
            c.wait_until("roots")
            L4 = row(a4(), 3)
            derive(self, L3, L4, run_time=2.0)
            ge = mt(r"x \ge 1", 44, DIM).next_to(L4, RIGHT, buff=0.8)
            self.play(*appear(ge), run_time=min(1.0, c.until(floor=0.4)))
            self.s4c = s4c
            self.chain = [L1, L2, tm, L3, L4, ge]
            self.L4 = L4

    # ------------------------------------------------------------ c3.arcosh.2
    def clip_test(self):
        with self.say("c3.arcosh.2") as c:
            L4 = self.L4
            q = T("?", 44, YELLOW).next_to(L4[0][4], UP, buff=0.12)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("try")
            card = cosh_check_card().move_to(CARD_C)
            card.plus.set_color(FG)
            card.minus.set_color(FG)
            self.play(*during(disappear(self.s4c), 0, 0.4),
                      *during([m.animate.shift(SHIFT * LEFT) for m in self.chain + [q]], 0.15, 0.75),
                      *during(appear(card.frame, card.x), 0.6, 1), run_time=min(1.8, c.until("nums")))
            c.wait_until("the square root")
            self.play(*appear(card.root), run_time=1.0)
            c.wait_until("the roots are")
            self.play(*appear(card.plus, card.minus, lag=0.5), run_time=1.4)
            c.wait_until("both")
            self.play(card.plus.animate.set_color(GREEN), card.minus.animate.set_color(GREEN),
                      *flash([card.plus, card.minus], color=GREEN, run_time=1.2), run_time=1.2)
            c.wait_until("bigger")
            note = mt(r"x > " + RT, 44, GREEN).move_to(L4).set_y(ROW_Y[4])
            self.play(*appear(note), run_time=1.0)
            c.wait_until("both roots")
            roots = list(L4[0][3:11])
            self.play(*recolor(roots, GREEN), *during(disappear(q), 0, 0.6), run_time=1.2)
            self.card, self.note = card, note

    # ------------------------------------------------------------ c3.arcosh.3
    def clip_product(self):
        with self.say("c3.arcosh.3") as c:
            card = self.card
            self.play(*appear(card.y), run_time=1.0)
            c.wait_until("log of a half")
            self.play(*appear(card.verify), run_time=1.0)
            self.play(GrowFromCenter(card.tick), run_time=0.6)
            c.wait_until("product")
            P = mt(r"2 \times \tfrac12 = 1", 48, YELLOW).move_to(self.note)
            self.play(*swap(self.note, P),
                      FlashAround(VGroup(*card.y[0][2:5]), run_time=1.2),
                      FlashAround(VGroup(*card.y[0][9:14]), run_time=1.2), run_time=1.2)
            c.wait_until("square")
            SQ = sq_line().move_to([0, SQ_Y, 0])
            self.play(*appear(SQ), run_time=1.2)
            c.wait_until("squared minus one")
            rt = min(1.2, c.until(floor=0.3))
            self.play(FlashAround(SQ[0][31], color=YELLOW, run_time=rt), run_time=rt)
            self.P, self.SQ = P, SQ

    # ------------------------------------------------------------ c3.arcosh.4
    def clip_recip(self):
        with self.say("c3.arcosh.4") as c:
            L4, SQ = self.L4, self.SQ
            leaving = [m for m in self.mobjects if m not in (L4, SQ)]
            R1 = r1().move_to([0, 1.0, 0])
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.4),
                      *during([L4.animate.move_to([0, 3.2, 0]),
                               SQ.animate.scale(0.9).move_to([0, 2.25, 0]).set_opacity(0.5)], 0.2, 0.7),
                      *during(appear(R1), 0.65, 1), run_time=min(2.2, c.until("neglog")))
            c.wait_until("neglog")
            R2 = r2().move_to([0, -0.25, 0])
            derive(self, R1, R2, run_time=2.0)
            c.wait_until("pm")
            R3 = r3().move_to([0, -1.4, 0])
            derive(self, R2, R3, run_time=2.0)
            c.wait_until("sym")
            sym = mt(r"\cosh(-y) = \cosh y", 44, cmap={(0, 4): TEAL, (9, 13): TEAL}).move_to([-2.0, -2.75, 0])
            U = mini_cosh([4.6, -2.45, 0])
            U.ax.set_stroke(opacity=0.4)
            U.curve.set_stroke(opacity=0.4)
            self.play(*appear(sym), FadeIn(U), run_time=1.2)
            c.wait_until("same cosh")
            ax = U.ax
            yax = Line(ax.c2p(0, 0), ax.c2p(0, 4)).set_stroke(YELLOW, 5)
            a = math.acosh(3.9)
            halves = [G3.fcurve(ax, math.cosh, 0, s * a, YELLOW, 6) for s in (1, -1)]
            self.play(VShowPassingFlash(yax, time_width=0.6),
                      *[VShowPassingFlash(h, time_width=0.5) for h in halves], run_time=1.2)
            self.R3 = R3

    # ------------------------------------------------------------ c3.arcosh.5
    def clip_result(self):
        with self.say("c3.arcosh.5") as c:
            R3 = self.R3
            c.wait_until("so we take")
            leaving = [m for m in self.mobjects if m is not R3]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.45),
                      *during([R3.animate.move_to([-0.5, 2.5, 0])], 0.3, 1), run_time=1.5)
            self.play(FlashAround(R3[0][2], color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until("result")
            RES = result_line().move_to([-0.5, 0.9, 0])
            derive(self, R3, RES, run_time=2.0)
            box = SurroundingRectangle(RES, buff=0.25).set_stroke(YELLOW, 3)
            tag = T("(97)", 36, DIM).next_to(box, RIGHT, buff=0.3)
            self.play(*during([FadeIn(box, scale=1.04)], 0, 0.5), *during(appear(tag, shift=None), 0.5, 1),
                      R3.animate.set_opacity(0.4), run_time=1.2)
            c.wait_until("domain")
            ge = mt(r"x \ge 1", 56, GREEN).move_to([-3.3, -1.6, 0])
            self.play(*appear(ge), run_time=1.0)
            U = mini_cosh([1.9, -1.9, 0], unit=0.6)
            ax = U.ax
            shade = Rectangle(width=ax.c2p(2, 0)[0] - ax.c2p(-2, 0)[0],
                              height=ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1])
            shade.set_stroke(width=0).set_fill(RED, 0.35).move_to(
                (ax.c2p(-2, 0) + ax.c2p(2, 1)) / 2).set_z_index(-1)
            no = mt(r"\cosh x \ge 1", 48, TEAL).next_to(U, RIGHT, buff=0.6)
            self.play(FadeIn(U), FadeIn(shade), *appear(no), run_time=1.2)

    # ------------------------------------------------------------ c3.arcosh.6
    def clip_fig(self):
        with self.say("c3.arcosh.6") as c:
            fig = fig26()
            full = fig.cosh.copy()

            def grow(m, al):                 # the U draws out of its vertex, both arms at once
                m.pointwise_become_partial(full, 0.5 - al / 2, 0.5 + al / 2)

            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.4),
                      *during([FadeIn(fig.lax)], 0.4, 0.7),
                      *during([UpdateFromAlphaFunc(fig.cosh, grow)], 0.6, 1), run_time=2.0)
            self.play(*appear(fig.clab), run_time=0.8)
            c.wait_until("reflect")
            self.play(Create(fig.mirror), *appear(fig.mlab, shift=None), run_time=1.0)
            self.play(VShowPassingFlash(fig.mirror.copy().set_stroke(YELLOW, 6), time_width=0.6),
                      FadeIn(fig.rax), run_time=1.0)
            cp = fig.cosh.copy()
            start = cp.copy()
            p = fig.lax.c2p(0, 0)              # turn about the drawn mirror line itself,
            dst = fig.rax.c2p(0, 0)            # carried over to the right panel's origin

            def turn(m, al):
                # first half: fold flat onto y = x in place; second half: unfold while carried over
                mv = smooth(max(0.0, 2 * al - 1))
                m.become(start.copy().rotate(al * PI, axis=np.array([1.0, 1.0, 0.0]), about_point=p)
                         .shift(mv * (dst - p)))

            self.play(UpdateFromAlphaFunc(cp, turn, rate_func=linear), run_time=2.5)
            up, lo = fig.upper, fig.lower
            lo.set_color(TEAL)
            up.set_color(TEAL)
            self.remove(cp)
            self.add(lo, up)
            c.wait_until("starting at one")
            self.play(FadeIn(fig.dot, scale=0.5), FlashAround(fig.dot, color=YELLOW, run_time=1.0),
                      run_time=1.0)
            c.wait_until("upper")
            self.play(up.animate.set_color(INV_C), *appear(fig.ulab), run_time=1.0)
            c.wait_until("lower")
            self.play(lo.animate.set_color(PURPLE), *appear(fig.llab), run_time=1.0)
            c.wait_until("inverse cosh")
            glow = up.copy().set_stroke(YELLOW, 9)
            self.play(VShowPassingFlash(glow, time_width=0.6), run_time=1.5)
        self.wait(1.5)
