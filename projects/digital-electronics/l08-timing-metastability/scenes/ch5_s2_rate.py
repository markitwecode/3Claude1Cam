"""Chapter 5, scene 2: from one change to failures per second. Clips c5.rate.1 – c5.rate.3.

Shots: ch5_s1's small synchroniser (sync_circuit() x0.6, to_corner(UL, buff=0.5)) stays upper
left throughout. time_axis() across the middle (0 s .. 6 s) -> a BLUE change tick at 1.5 s, a big
die pops up, rolls, face GOLD P_fail -> GREEN check, D1 settles -> second change at 4.5 s, die ->
RED cross, D1/Q RED, "???" flickers -> one tick + small die per second, brace over 2-3 s, label
"1 change per second -> probability ... = P_fail" -> three per second, "N changes", "N P_fail" ->
ticks jitter, "N: average changes per second" -> board clears to the formula P_fail/s = N P_fail,
"failures per second", grey sample, curved YELLOW arrow round the label (end shot for s3).
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


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# push_button() + make_ff() + fingertip(): copied from ch4_s5_synchroniser.py
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
# sync_circuit(): copied from ch4_s5_synchroniser.py (slide p. 112)
# =============================================================================================
SK = 0.62
SFF_X = (-1.7, 2.1)
SFF_Y = 2.244
SBTN_X = -4.3
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


def small_sync():
    """ch5's small synchroniser: x0.6 (labels >= 18), to_corner(UL, buff=0.5), as in ch5_s1."""
    C = sync_circuit()
    C.scale(0.6)
    C.to_corner(UL, buff=0.5)
    return C
# =============================================================================================


# =============================================================================================
# time_axis() + change_tick() + small_die(): ch5's time axis (s4 and the recap redraw it small).
# Axis FG from x=-6.3 to 6.3 at y=AX_Y, 0 s at x=-6, 2 units per second, DIM second marks and
# "k s" labels (T 30 DIM); BLUE change ticks; dice (FG outline, three FG pips) above them.
# =============================================================================================
AX_Y = -0.4
AX_X0 = -6.0
AX_UNIT = 2.0
DIE_Y = AX_Y + 0.6           # small dice centres
DIE_S = 0.46


def ax_x(t):
    return AX_X0 + AX_UNIT * t


def time_axis(seconds=6):
    line = Line(_p(ax_x(0) - 0.3, AX_Y), _p(ax_x(seconds) + 0.3, AX_Y)).set_stroke(FG, 3)
    marks = VGroup(*[Line(_p(ax_x(k), AX_Y - 0.1), _p(ax_x(k), AX_Y + 0.1)).set_stroke(DIM, 3)
                     for k in range(seconds + 1)])
    labels = VGroup(*[T(f"{k} s", 30, DIM).next_to(_p(ax_x(k), AX_Y - 0.12), DOWN, buff=0.14)
                      for k in range(seconds + 1)])
    g = VGroup(line, marks, labels)
    g.line, g.marks, g.labels = line, marks, labels
    return g


def change_tick(t, color=BLUE):
    return Line(_p(ax_x(t), AX_Y - 0.22), _p(ax_x(t), AX_Y + 0.22)).set_stroke(color, 5)


def small_die(x, size=DIE_S, y=DIE_Y):
    body = RoundedRectangle(corner_radius=0.18 * size, width=size, height=size)
    body.set_stroke(FG, 3).set_fill(BG, 1)
    r = 0.09 * size
    pips = VGroup(*[Dot(_p(dx * size * 0.27, dy * size * 0.27), radius=r, color=FG)
                    for dx, dy in ((-1, 1), (0, 0), (1, -1))])
    g = VGroup(body, pips)
    g.body, g.pips = body, pips
    g.move_to(_p(x, y))
    return g
# =============================================================================================


GOLDS = ("N", r"P_{\text{fail}}")


def tex(s, size=40, color=FG):
    import re
    pieces = [x for x in re.split(r"(N|P_\{\\text\{fail\}\})", s) if x]
    m = MathTex(*pieces, font_size=size, color=color)
    for part in m.submobjects:
        if getattr(part, "tex_string", "") in GOLDS:
            part.set_color(GOLD)
    return m


def roll(die, face, turns=1):
    """The die hops and spins; its pips fade, the GOLD face fades in on landing."""
    start = die.copy()
    c0 = die.get_center()

    def upd(m, a):
        m.become(start)
        m.pips.set_opacity(max(0.0, 1 - a / 0.4))
        m.rotate(-TAU * turns * a, about_point=c0)
        m.shift(0.5 * np.sin(PI * a) * UP)

    return [UpdateFromAlphaFunc(die, upd, rate_func=smooth), *during([FadeIn(face)], 0.65, 1)]


def flicker(mob, n=3):
    def upd(m, a):
        m.set_opacity(0.35 + 0.65 * abs(np.cos(PI * n * a)))
    return UpdateFromAlphaFunc(mob, upd, rate_func=linear)


class RateScene(NarratedScene):
    def construct(self):
        C = small_sync()
        self.add(C)
        ax = time_axis()
        BIG = 1.5
        BIG_Y = AX_Y + 1.5

        # ---------------------------------------------------------------- c5.rate.1
        with self.say("c5.rate.1") as c:
            self.play(Create(ax.line), *appear(*ax.marks, *ax.labels, lag=0.05, shift=None),
                      run_time=min(1.5, c.until("every time")))
            c.wait_until("changes")
            t1 = change_tick(1.5)
            die1 = small_die(ax_x(1.5), size=BIG, y=BIG_Y)
            self.play(GrowFromCenter(t1), FadeIn(die1, shift=0.4 * UP, scale=0.5),
                      run_time=min(1.2, c.until("roll")))
            self.play(*flash([C.d0_l], color=BLUE), run_time=1.2)
            c.wait_until("roll")
            face1 = tex(r"P_{\text{fail}}", 48).move_to(die1.body)
            self.play(*roll(die1, face1), run_time=min(2.0, 0.8 * c.until("safe")))
            c.wait_until("resolves")
            # lands on a GREEN check; D1 stays TEAL (resolved) -- RED belongs to {fail} only
            chk = check_mark(GREEN).move_to(_p(ax_x(1.5), DIE_Y))
            self.play(*swap(VGroup(die1.body, face1), chk), FlashAround(C.d1_l, color=TEAL, time_width=1.5),
                      run_time=min(1.5, c.until("fail")))
            self.remove(die1)
            c.wait_until("fail")
            # a later change: the die lands on a RED cross
            t2 = change_tick(4.5)
            die2 = small_die(ax_x(4.5), size=BIG, y=BIG_Y)
            self.play(GrowFromCenter(t2), FadeIn(die2, shift=0.4 * UP, scale=0.5), run_time=1.0)
            face2 = tex(r"P_{\text{fail}}", 48).move_to(die2.body)
            self.play(*roll(die2, face2), run_time=1.3)
            c.wait_until("set-up deadline")
            crs = cross_mark(RED).move_to(_p(ax_x(4.5), DIE_Y))
            self.play(*swap(VGroup(die2.body, face2), crs),
                      *[restyle(w, outline=RED) for w in C.d1_wires], recolor(C.d1_l, RED)[0],
                      run_time=min(1.4, c.until("so the output")))
            self.remove(die2)
            c.wait_until("goes meta-stable")
            qq = T("???", 30, RED).next_to(C.q_l, RIGHT, buff=0.15)
            self.play(restyle(C.ff1.q_w, outline=RED), recolor(C.q_l, RED)[0], *appear(qq, shift=None),
                      run_time=1.0)
            self.play(flicker(qq), run_time=min(1.5, c.until("that's a failure")))
            c.wait_until("that's a failure")
            self.play(FlashAround(crs, color=RED, time_width=1.5), run_time=min(1.0, c.until(floor=0.5)))

        # ---------------------------------------------------------------- c5.rate.2
        with self.say("c5.rate.2") as c:
            times = [k + 0.5 for k in range(6)]
            ticks = {1.5: t1, 4.5: t2}
            dice = {t: small_die(ax_x(t)) for t in times}
            for t in times:
                ticks.setdefault(t, change_tick(t))
            new1 = [t for t in times if t not in (1.5, 4.5)]
            # circuit back to normal; check and cross become dice
            self.play(*swap(chk, dice[1.5]), *swap(crs, dice[4.5]),
                      *[restyle(w, outline=TEAL) for w in C.d1_wires],
                      run_time=min(1.2, c.until("once per second")))
            self.play(recolor(C.d1_l, TEAL)[0], restyle(C.ff1.q_w, outline=GREEN), recolor(C.q_l, GREEN)[0],
                      *disappear(qq), run_time=0.8)
            self.play(*[GrowFromCenter(ticks[t]) for t in new1],
                      *[FadeIn(dice[t], shift=0.3 * UP) for t in new1],
                      lag_ratio=0.15, run_time=min(1.6, c.until("one gamble")))
            c.wait_until("one gamble")
            brace = span_brace(_p(ax_x(2), 0), _p(ax_x(3), 0), direction=DOWN, color=FG)
            brace.next_to(ax.labels, DOWN, buff=0.12).set_x(ax_x(2.5))
            l1 = tex(r"\text{1 change per second}", 46)
            l2 = tex(r"\rightarrow\ \text{probability of failure per second} = P_{\text{fail}}", 46)
            LX = ax_x(2.5)
            l1.next_to(brace, DOWN, buff=0.2).set_x(LX)
            l2.next_to(l1, DOWN, buff=0.22).set_x(LX)
            self.play(GrowFromCenter(brace), *appear(l1), run_time=min(1.2, c.until("so the probability")))
            c.wait_until("so the probability")
            self.play(*appear(l2), run_time=1.2)
            c.wait_until("many")
            # three per second
            times3 = [k + f for k in range(6) for f in (1 / 6, 5 / 6)]
            for t in times3:
                ticks[t] = change_tick(t)
                dice[t] = small_die(ax_x(t))
            self.play(*[GrowFromCenter(ticks[t]) for t in times3],
                      *[FadeIn(dice[t], shift=0.3 * UP) for t in times3],
                      lag_ratio=0.06, run_time=min(2.0, c.until("there are n gambles")))
            c.wait_until("there are n gambles")
            l1b = tex(r"N\text{ changes per second}", 46).move_to(l1)
            self.play(*edit(l1, l1b), run_time=1.5)
            c.wait_until("n times greater")
            l2b = tex(r"\rightarrow\ \text{probability of failure per second} = N\,P_{\text{fail}}", 46)
            l2b.move_to(l2)
            self.play(*edit(l2, l2b), run_time=1.5)
            c.wait_until("average")
            # random arrival times: the ticks jitter, still about three per second
            all_t = sorted(ticks)
            rng = np.random.default_rng(7)
            while True:
                off = rng.uniform(-0.3, 0.3, len(all_t))
                xs = [ax_x(t) + o for t, o in zip(all_t, off)]
                if all(b - a >= 0.5 for a, b in zip(xs, xs[1:])) and xs[0] > -6.0 and xs[-1] < 6.0:
                    break
            moves = []
            for t, o in zip(all_t, off):
                moves += [ticks[t].animate.shift(o * RIGHT), dice[t].animate.shift(o * RIGHT)]
            self.play(*moves, run_time=min(1.8, 0.8 * c.until("an average")))
            c.wait_until("an average")
            l1c = tex(r"N\text{: average changes per second}", 46).move_to(l1b)
            self.play(*edit(l1b, l1c), run_time=min(1.5, c.until(floor=0.8)))

        # ---------------------------------------------------------------- c5.rate.3
        with self.say("c5.rate.3") as c:
            formula = tex(r"P_{\text{fail}}/\text{s} = N\,P_{\text{fail}}", 84).move_to(_p(0, 0.5))
            sweep_clear(self, *appear(formula, shift=None), keep=[C, l1c, l2b],
                        run_time=min(2.0, c.until("equals")))
            c.wait_until("rate")
            rate = T("failures per second", 44).next_to(formula, DOWN, buff=0.7)
            self.play(*during(disappear(l1c, l2b), 0, 0.45), *during(appear(rate), 0.5, 1),
                      run_time=1.6)
            c.wait_until("tiny")
            sample = tex(r"N = 1,\ \ P_{\text{fail}} = 10^{-7}\ \ \rightarrow\ \ "
                         r"10^{-7}\ \text{failures per second}", 40, DIM)
            for part in sample.submobjects:
                part.set_color(DIM)
            sample.move_to(_p(0, -3.0))
            self.play(*appear(sample), run_time=1.2)
            c.wait_until("upside down")
            a0 = rate.get_right() + _p(0.45, -0.05)
            a1 = rate.get_left() + _p(-0.45, -0.05)
            arrow = CurvedArrow(a0, a1, angle=-PI * 0.55, color=YELLOW).set_stroke(width=5)
            self.play(Create(arrow), run_time=min(1.5, c.until(floor=0.8)))

        # hand over to s3: formula, label and arrow alone
        self.play(*disappear(C, sample), run_time=1.0)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
