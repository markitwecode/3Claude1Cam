"""Chapter 3, scene 6: the real part of the top, the boxed answer, a check, and theta = 2 pi m. Clips c3.res.1 – c3.res.5.

Shared: boxed_result() and straight_chain() are imported by ch3_s8_recap. Keep their names and signatures."""
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch3_s3_sum")
S4 = load_scene("ch3_s4_geometric")
S5 = load_scene("ch3_s5_conjugate")
N6, TH6 = S3.N6, S3.TH6

HS = 52                          # hero size
Y_H = 0.2                        # hero row (as in s5)
RS = 40                          # the expanded row
Y_ROW = -1.6                     # its y
PS = 34                          # the parked PINK row
PARK = np.array([-6.5, -3.25, 0])  # its left end

# the theta = 2 pi m picture (res.4); straight_chain() defaults to it
O4 = np.array([1.3, 0.0, 0.0])
U4 = 0.85
# the check picture (res.3)
O3 = np.array([-4.6, -0.6, 0.0])
U3 = 1.5


# ---------------------------------------------------------------- shared (ch3_s8_recap imports these)
def boxed_result(size=HS):
    """S_N = 1/2 + [cos(N-1)θ - cos Nθ] / [2(1 - cos θ)] in a YELLOW box, centred at ORIGIN.
    Attributes: .S .eq .half .plus .F (.top .bar .bot) .box; the cosines and the bottom BLUE."""
    top = S5.mt([(r"\cos(N-1)\theta", BLUE), ("-", FG), (r"\cos N\theta", BLUE)], size)
    bot = MathTex(r"2(1-\cos\theta)", font_size=size, color=BLUE)
    F = S5.frac(top, bot)
    axis = F.bar.get_y()
    S = MathTex("S_N", font_size=size)
    eq = MathTex("=", font_size=size)
    half = MathTex(r"\frac{1}{2}", font_size=size)
    plus = MathTex("+", font_size=size)
    x = 0.0
    for m, buff in ((S, 0.0), (eq, 0.2), (half, 0.2), (plus, 0.18), (F, 0.18)):
        m.shift((x + buff - m.get_left()[0]) * RIGHT)
        x = m.get_right()[0]
    S.set_y(axis - 0.06)
    for m in (eq, half, plus):
        m.set_y(axis)
    inner = VGroup(S, eq, half, plus, F)
    box = SurroundingRectangle(inner, color=YELLOW, buff=0.3, stroke_width=3)
    g = VGroup(S, eq, half, plus, F, box)
    g.shift(-inner.get_center())
    g.S, g.eq, g.half, g.plus, g.F, g.box = S, eq, half, plus, F, box
    return g


def straight_chain(n=N6, origin=O4, unit=U4):
    """The chain at θ = 2πm: n GOLD unit arrows flat along the real axis, a GOLD brace under them
    labelled N (a length). VGroup(chain, brace, label); .chain .brace .label."""
    origin = np.array(origin, dtype=float)
    chain = S3.unit_chain(n, 0.0, origin=origin, unit=unit)
    brace = span_brace(origin, chain.end, direction=DOWN, color=GOLD, buff=0.22)
    label = MathTex("N", font_size=44, color=GOLD).next_to(brace, DOWN, buff=0.15)
    g = VGroup(chain, brace, label)
    g.chain, g.brace, g.label = chain, brace, label
    return g


# ---------------------------------------------------------------- this scene's pieces
def frac_line(F, size=HS, y=Y_H, lhs="S_N"):
    """lhs = F, the '=' on F's bar; centred in x, the bar at y."""
    axis = F.bar.get_y()
    eq = MathTex("=", font_size=size)
    S = MathTex(lhs, font_size=size)
    eq.next_to(F, LEFT, buff=0.2).set_y(axis)
    S.next_to(eq, LEFT, buff=0.2).set_y(axis - 0.06)
    g = VGroup(S, eq, F)
    g.shift(np.array([-g.get_center()[0], y - axis, 0]))
    g.S, g.eq, g.F = S, eq, F
    return g


def left_top(size=HS):
    return S5.mt([("1", FG), ("-", FG), (r"\cos\theta", BLUE), ("-", FG), (r"\cos N\theta", BLUE),
                  ("+", FG), (r"\cos(N-1)\theta", BLUE)], size)


def hero5(y=Y_H):
    return frac_line(S5.frac(left_top(), MathTex(r"2(1-\cos\theta)", font_size=HS, color=BLUE)), y=y)


ROW_G = [[("1", FG)], [("-", FG), (r"\cos\theta", BLUE)], [(r"+i\sin\theta", PINK)],
         [("-", FG), (r"\cos N\theta", BLUE)], [(r"-i\sin N\theta", PINK)],
         [("+", FG), (r"\cos(N-1)\theta", BLUE)], [(r"+i\sin(N-1)\theta", PINK)]]
COS_IDX = [(0, 0, 1), (1, 1, 3), (3, 3, 5), (5, 5, 7)]    # row group -> left_top parts [a:b]
SIN_IDX = [2, 4, 6]


def sine_formula(size=48):
    top = MathTex(r"\sin\theta-\sin N\theta+\sin(N-1)\theta", font_size=size, color=PINK)
    bot = MathTex(r"2(1-\cos\theta)", font_size=size, color=BLUE)
    F = S5.frac(top, bot)
    axis = F.bar.get_y()
    lhs = MathTex(r"\sum_{k=0}^{N-1}\sin k\theta", font_size=size, color=PINK)
    eq = MathTex("=", font_size=size)
    eq.next_to(F, LEFT, buff=0.2).set_y(axis)
    lhs.next_to(eq, LEFT, buff=0.2).set_y(axis)
    g = VGroup(lhs, eq, F)
    g.lhs, g.eq, g.F = lhs, eq, F
    return g


class Ch3S6Result(NarratedScene):
    def construct(self):
        hs = S5.handover_shot()
        self.add(hs)
        self.remove(hs)
        self.add(*hs)
        self.header, self.tb, self.s3l, self.fb, self.H4 = hs
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ res.1: real part of the top
    def clip1(self):
        H4 = self.H4
        with self.say("c3.res.1") as c:
            self.play(FlashAround(H4.body.bot, color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("real part of the top")
            self.play(FlashAround(VGroup(H4.Re, H4.body.top), run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("euler")
            row = S5.pieces(ROW_G, RS).move_to([0, Y_ROW, 0])
            top = H4.body.top
            self.play(FlashAround(top[1], color=PURPLE, run_time=1.4, time_width=1.5),
                      *appear(row[0], row[1], row[2], lag=0.3), run_time=1.5)
            self.play(FlashAround(VGroup(top[3], top[5]), color=GOLD, run_time=1.5, time_width=1.5),
                      *appear(row[3], row[4], row[5], row[6], lag=0.3), run_time=1.6)

            c.wait_until("drop")
            self.play(*flash([row[1], row[3], row[5]], color=BLUE, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("the sines all")
            park = S5.pieces([[(r"+i\sin\theta", PINK)], [(r"-i\sin N\theta", PINK)],
                              [(r"+i\sin(N-1)\theta", PINK)]], PS)
            park.move_to(PARK, aligned_edge=LEFT)
            self.play(*[row[i].animate.set_y(PARK[1]) for i in SIN_IDX], run_time=1.2)
            for j, i in enumerate(SIN_IDX):
                row[i].target = park[j]
            self.play(*[MoveToTarget(row[i]) for i in SIN_IDX], run_time=1.2)
            self.pinks = [row[i] for i in SIN_IDX]

            c.wait_until("left")
            H5 = hero5()
            H5.shift((Y_ROW - H5.F.top.get_y()) * UP)
            moves = []
            for gi, a, b in COS_IDX:
                dst = VGroup(*H5.F.top[a:b])
                moves.append(row[gi].animate.scale(HS / RS).move_to(dst.get_center()))
            old = [H4.S, H4.eq, H4.Re, H4.lb, H4.body.top, H4.body.bar, H4.body.bot, H4.rb]
            self.play(*during(disappear(*old), 0, 0.45),
                      *during(moves, 0.2, 0.9),
                      *during(appear(H5.S, H5.eq, H5.F.bar, H5.F.bot, shift=None), 0.5, 1.0),
                      run_time=1.8)
            self.remove(*H4.get_family(), *[row[gi] for gi, _, _ in COS_IDX])
            self.add(H5)
            self.H5 = H5

    # ------------------------------------------------------------ res.2: split off the half, box it
    def clip2(self):
        H5 = self.H5
        with self.say("c3.res.2") as c:
            self.play(*during(disappear(self.tb, self.s3l), 0, 0.5),
                      *during([H5.animate.shift((Y_H - H5.F.bar.get_y()) * UP)], 0.3, 1.0), run_time=1.6)

            c.wait_until("half")
            top, bot = H5.F.top, H5.F.bot
            bg = list(bot[0][2:8])
            self.play(FlashAround(VGroup(*top[0:3]), run_time=1.5, time_width=1.5),
                      FlashAround(VGroup(*bg), run_time=1.5, time_width=1.5),
                      *recolor([top[0], top[1], top[2], *bg], YELLOW), run_time=1.5)
            mini = MathTex(r"\frac{1-\cos\theta}{2(1-\cos\theta)}", "=", font_size=44, color=YELLOW)
            mhalf = MathTex(r"\frac{1}{2}", font_size=44, color=YELLOW)
            VGroup(mini, mhalf).arrange(RIGHT, buff=0.2).move_to([0, -2.0, 0])
            hx = boxed_result().move_to([0, Y_H, 0]).half.get_x()
            VGroup(mini, mhalf).shift((hx - mhalf.get_x()) * RIGHT)
            mini[1].set_color(FG)
            self.play(*appear(mini, mhalf, lag=0.4), run_time=1.4)

            self.mini = (mini, mhalf)
            c.wait_until("box")
            B = boxed_result().move_to([0, Y_H, 0])
            self.play(*disappear(H5), run_time=0.8)
            self.play(*during(disappear(mini), 0, 0.4), *during([ReplacementTransform(mhalf, B.half)], 0.1, 0.8),
                      *during(appear(B.S, B.eq, B.plus, B.F, shift=None), 0.3, 1.0),
                      *during([GrowFromCenter(B.box)], 0.5, 1.0), run_time=1.6)
            self.remove(*B.get_family())
            self.add(B)
            self.B = B

            c.wait_until("top")
            self.play(FlashAround(B.F.top, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("bottom")
            self.play(FlashAround(B.F.bot, run_time=1.5, time_width=1.5), run_time=1.5)

    # ------------------------------------------------------------ res.3: check N = 3, θ = π/2
    def clip3(self):
        B = self.B
        with self.say("c3.res.3", gap=1.8) as c:
            sweep_clear(self, *during([B.animate.scale(0.75).move_to([1.3, 2.6, 0])], 0.3, 1.0),
                        keep=[B, *self.pinks], run_time=1.6)

            c.wait_until("n equal to three")
            plane = S3.argand_plane(origin=O3, unit=U3, xr=(-0.5, 1.7), yr=(-0.15, 1.65))
            nt = MathTex(r"N=3,\quad \theta=\tfrac{\pi}{2}", font_size=42).move_to([-4.6, 2.75, 0])
            self.play(FadeIn(plane), *during(appear(nt), 0.3, 1.0), run_time=1.4)

            c.wait_until("chain")
            chain = S3.unit_chain(3, PI / 2, origin=O3, unit=U3)
            self.play(LaggedStart(*[GrowArrow(a) for a in chain], lag_ratio=0.7), run_time=2.4)
            dot = Dot(chain.end, radius=0.1, color=YELLOW)
            il = MathTex("i", font_size=44, color=YELLOW).next_to(dot, UL, buff=0.12)
            set_backstroke(il)
            self.play(FadeIn(dot, scale=0.5), *appear(il), run_time=0.9)

            c.wait_until("direct")
            shadow = S3.chain_shadow(3, PI / 2, origin=O3, unit=U3)
            self.play(LaggedStart(*[ReplacementTransform(a.copy(), s) for a, s in zip(chain, shadow)],
                                  lag_ratio=0.4), run_time=1.8)
            direct = MathTex("1", "+", "0", "+", "(-1)", "=", "0", font_size=44)
            for i in (0, 2, 4):
                direct[i].set_color(BLUE)
            direct.move_to([-4.2, -2.55, 0])
            self.play(*appear(direct), run_time=1.2)

            c.wait_until("formula")
            F1 = MathTex(r"S_3", "=", r"\frac{1}{2}", "+",
                         r"\frac{\cos\pi-\cos\tfrac{3\pi}{2}}{2(1-\cos\tfrac{\pi}{2})}", font_size=44)
            F1.move_to([2.9, 0.2, 0])
            self.play(*appear(F1), run_time=1.3)
            c.wait_until("minus one minus zero")
            F2 = MathTex("=", r"\frac{1}{2}", "+", r"\frac{-1-0}{2}", font_size=44)
            F2.next_to(F1, DOWN, buff=0.5)
            F2.shift((F1[1].get_x() - F2[0].get_x()) * RIGHT)
            self.play(*appear(F2), run_time=1.3)
            c.wait_until("one half minus one half")
            F3 = MathTex("=", "0", font_size=44).next_to(F2, RIGHT, buff=0.25)
            F3.set_y(F2[0].get_y())
            tick = check_mark().next_to(F3, RIGHT, buff=0.35)
            self.play(*appear(F3), *during([FadeIn(tick, scale=0.6)], 0.4, 1.0), run_time=1.3)

    # ------------------------------------------------------------ res.4: λ = 1, θ = 2πm
    def clip4(self):
        B = self.B
        with self.say("c3.res.4", gap=1.2) as c:
            flag = S4.lam_flag().move_to([-3.7, 0.95, 0])
            sweep_clear(self, *during([B.animate.scale(0.82).move_to([-3.7, 2.55, 0])], 0.3, 1.0),
                        *during(appear(flag), 0.55, 1.0), keep=[B, *self.pinks], run_time=1.8)

            c.wait_until("lam")
            lam = MathTex(r"\lambda", "=", "1", r"\iff", r"\theta", "=", r"2\pi m", r",\ m\in\mathbb{Z}",
                          font_size=44)
            lam[0].set_color(GOLD)
            lam[6].set_color(TEAL)
            lam.move_to([-3.7, -0.05, 0])
            self.play(*appear(lam), run_time=1.3)

            c.wait_until("whole number")
            plane = S3.argand_plane(origin=O4, unit=U4, xr=(-0.6, 6.25), yr=(-3.95, 3.95))
            chain0 = S3.unit_chain(N6, TH6, origin=O4, unit=U4)
            self.play(FadeIn(plane), FlashAround(lam[6], color=TEAL, run_time=1.5, time_width=1.5),
                      *during([LaggedStart(*[GrowArrow(a) for a in chain0], lag_ratio=0.3)], 0.3, 1.0),
                      run_time=1.8)

            c.wait_until("sweep")
            th = ValueTracker(TH6)
            live = always_redraw(lambda: S3.unit_chain(N6, th.get_value(), origin=O4, unit=U4))
            self.remove(chain0, *chain0)   # GrowArrow put each arrow on screen by itself
            self.add(live)
            self.play(th.animate.set_value(2 * PI), run_time=c.until("straight") + 0.6, rate_func=smooth)
            st = straight_chain()
            live.clear_updaters()
            self.remove(live)
            self.add(st.chain)

            c.wait_until("ones")
            ones = MathTex("S_N", "=", "1", "+", "1", "+", r"\cdots", "+", "1", "=", "N", font_size=44)
            ones[10].set_color(GOLD)
            ones.move_to([-3.7, -1.3, 0])
            self.play(*appear(ones), run_time=1.3)
            self.play(GrowFromCenter(st.brace), *during(appear(st.label), 0.4, 1.0), run_time=1.3)
            c.wait_until("just n")
            self.play(FlashAround(ones[10], color=GOLD, run_time=1.4, time_width=1.5),
                      FlashAround(st.label, color=GOLD, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("zero")
            z0 = MathTex("=0", font_size=36, color=RED)
            z0.next_to(B.box, DOWN, buff=0.14).set_x(B.F.bot.get_x())   # under the denominator
            self.play(restyle(B.F.bot, fill=RED), FlashAround(B.F.bot, color=RED, run_time=1.4, time_width=1.5),
                      *during(appear(z0, shift=None), 0.3, 1.0), run_time=1.4)

    # ------------------------------------------------------------ res.5: the sines, for free
    def clip5(self):
        B = self.B
        with self.say("c3.res.5", gap=3.2) as c:
            B2 = boxed_result().scale(0.85).move_to([0, 1.75, 0])
            sweep_clear(self, *during([Transform(B, B2)], 0.3, 1.0), keep=[B, *self.pinks], run_time=1.6)

            c.wait_until("sines")
            SF = sine_formula().move_to([0, -1.1, 0])
            dst = SF.F.top.get_center()
            pm = [p.animate.move_to(dst + (p.get_center() - self.pinks[1].get_center())).set_opacity(0)
                  for p in self.pinks]
            self.play(*during(pm, 0, 0.5), *during(appear(SF, shift=None), 0.5, 1.0), run_time=1.8)
            self.remove(*self.pinks)

            c.wait_until("same")
            self.play(FlashAround(B.F.bot, color=BLUE, run_time=1.5, time_width=1.5),
                      FlashAround(SF.F.bot, color=BLUE, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("sheet")
            tag = T("F13(b)", 32, color=DIM).next_to(SF, DOWN, buff=0.45).align_to(SF, RIGHT)
            self.play(*appear(tag), run_time=1.0)
