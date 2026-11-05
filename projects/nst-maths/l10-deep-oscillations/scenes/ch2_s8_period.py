"""Chapter 2, scene 8: the beat (T = 2π/ω off one full turn; the 1 m and 4 m pendulums; no size in
the period; the honest catch at big angles). Clips c2.beat.1 – c2.beat.5."""
# style: 2
import math
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
grav = load_scene("ch1_s5_gravity")

# ── numbers ─────────────────────────────────────────────────────────────────────
G = 9.81
W1 = math.sqrt(G)              # 3.1321 rad/s, the 1 m pendulum
P1 = TAU / W1                  # 2.0061 s
HALF1 = P1 / 2                 # one swing across, ≈ 1.003 s
W4 = math.sqrt(G / 4)          # 1.5660 rad/s, the 4 m pendulum
AMP = 8.0                      # degrees: ch1's gentle swing

# ── layout ──────────────────────────────────────────────────────────────────────
PIV_Y = grav.PIVOT[1]          # 2.7
ROD = grav.ROD_L               # 2.75 = 1 m in clips 1-2 and 5
SWING_Y = PIV_Y - ROD          # the bob's line (-0.05)
X1M_SMALL, X4M = -4.8, -2.0    # clip 3: the 1 m (to scale) and the 4 m pendulums
L_SMALL = 1.0                  # clip 3 scale: 1 m = 1.0 unit
CLK_X = 1.8                    # the grandfather clock
O4 = np.array([-3.2, 1.4, 0])  # clip 4 plane origin
S4 = 0.55                      # clip 4 plane scale (the length-2 arrow fits)
Y_IN, Y_OUT = -0.3, -1.35      # clip 4 block tracks
T_FREEZE0 = PI / 12            # clip 4 freeze: the arrows at 30°
X10, X60 = -5.3, -2.1          # clip 5 pivots
CX = kit.COL_LEFT

# ── legend ──────────────────────────────────────────────────────────────────────
E_PER = (r"T", TEAL, "the period")
E7 = [ak.E_X, kit.E_XD, kit.E_XDD, ak.E_W, ak.E_T, ak.E_ARROW, ak.E_ANGLE]
E_PEND = [ak.E_W, ak.E_T, E_PER, grav.E_L, grav.E_G]
E_TWO = [ak.E_X, kit.E_XD, kit.E_XDD, ak.E_W, E_PER, ak.E_ARROW]
E_TH = (r"x", BLUE, "displacement (angle)")
E_BIG = [E_TH, grav.E_L, grav.E_G, ak.E_T]


# ── the real pull, integrated (RK4, L = 1 m) ───────────────────────────────────
def _rk4(theta0_deg, t_end=40.0, dt=0.002):
    def f(s):
        return np.array([s[1], -G * math.sin(s[0])])
    s = np.array([math.radians(theta0_deg), 0.0])
    out = [s[0]]
    for _ in range(int(t_end / dt)):
        k1 = f(s)
        k2 = f(s + dt / 2 * k1)
        k3 = f(s + dt / 2 * k2)
        k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out.append(s[0])
    ts = np.arange(len(out)) * dt
    return ts, np.degrees(np.array(out))


_TS, _TH10 = _rk4(10.0)
_, _TH60 = _rk4(60.0)


def theta10(t):
    return float(np.interp(t, _TS, _TH10))


def theta60(t):
    return float(np.interp(t, _TS, _TH60))


# ── helpers ─────────────────────────────────────────────────────────────────────
def turn_arc(t, radius=0.42):
    """The TEAL arc of the angle ωt, growing to one full turn (not wrapped)."""
    def build():
        a = max(1e-3, min(ak.OMEGA * t.get_value(), TAU))
        return Arc(radius=radius, start_angle=0, angle=a, arc_center=ak.PLANE_O) \
            .set_stroke(TEAL, 4).set_z_index(-1.7)
    return always_redraw(build)


def pend(theta, x, length, y=PIV_Y):
    return grav.pendulum(theta, labels=False, angle=False, pivot=np.array([x, y, 0]),
                         length=length)


def clock_case():
    """A grandfather clock outline (FG): hood with a face, body, base."""
    x = CLK_X
    hood = Rectangle(width=1.25, height=0.85).move_to([x, -0.3, 0])        # top 0.125
    face = Circle(radius=0.29).move_to([x, -0.3, 0])
    h1 = Line([x, -0.3, 0], [x, -0.1, 0])
    h2 = Line([x, -0.3, 0], [x + 0.15, -0.38, 0])
    body = Rectangle(width=0.95, height=2.45).move_to([x, -1.95, 0])       # -3.175 .. -0.725
    base = Rectangle(width=1.25, height=0.25).move_to([x, -3.3, 0])
    g = VGroup(hood, face, h1, h2, body, base).set_stroke(FG, 3)
    return g


def clock_pendulum(theta):
    th = math.radians(theta)
    p = np.array([CLK_X, -0.85, 0])
    b = p + 1.85 * np.array([-math.sin(th), -math.cos(th), 0])
    rod = Line(p, b).set_stroke(FG, 3)
    bob = Circle(radius=0.13).set_fill(BLUE, 1).set_stroke(BLUE, 2).move_to(b)
    return VGroup(rod, bob)


def deg_readout(fn, pos):
    """"x = 10°" (BLUE), live, centred at pos."""
    lab = MathTex(r"x =", font_size=36, color=BLUE)
    num = DecimalNumber(fn(), num_decimal_places=0, unit=r"^\circ", font_size=36, color=BLUE)
    g = VGroup(lab, num)

    def place(m):
        m[1].set_value(fn())
        m[1].next_to(m[0], RIGHT, buff=0.15)
        m[1].align_to(m[0], DOWN)
        m.move_to(pos)
    place(g)
    g.add_updater(place)
    return g


def col_line(tex, y, x=CX, size=36, teal=()):
    m = MathTex(tex, font_size=size)
    for i in teal:
        m[0][i].set_color(TEAL)
    m.move_to([x, y, 0], aligned_edge=LEFT)
    return m


class Period(NarratedScene):
    def construct(self):
        self.t = ValueTracker(0.0)
        self.add(self.t)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.5)
        self.rate = 0.0
        for m in self.mobjects:
            for f in m.get_family():
                f.clear_updaters()
        self.remove(*self.trackers())
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def trackers(self):
        return [m for m in self.mobjects if isinstance(m, ValueTracker)]

    # ── c2.beat.1: one full turn → T = 2π/ω ────────────────────────────────────
    def clip1(self):
        t = self.t
        self.pl = ak.plane()
        self.axis = self.pl.axes[0].copy()          # the shadow's line (carried into clip 2)
        self.gold = ak.turning_arrow(t)
        self.sh = ak.shadow(t)
        self.sp = ak.spring_on_axis(t)
        self.leg = kit.legend(E7, 4)
        self.pin = ak.rule_pin()
        with self.say("c2.beat.1") as c:
            self.play(*appear(self.pl, self.axis, self.sp, self.sh, self.gold, self.leg, self.pin,  # early: the board
                              shift=None, lag=0.12), run_time=1.8)
            c.wait_until("arrow")
            self.play(VShowPassingFlash(Line(ak.PLANE_O, ak.plane_point(1)).set_stroke(YELLOW, 9),
                                        time_width=0.8), run_time=1.3)

            c.wait_until("turn")
            self.arc = turn_arc(t)
            self.tr = ak.t_readout(t).move_to([CX, 3.05, 0], aligned_edge=LEFT)
            self.wr = ak.wt_readout(t).move_to([CX, 2.5, 0], aligned_edge=LEFT)
            self.play(FadeIn(self.arc), *appear(self.tr, self.wr, lag=0.3), run_time=1.0)
            self.play(t.animate(rate_func=linear).set_value(PI), run_time=PI)
            self.tr.clear_updaters()
            self.wr.clear_updaters()

            c.wait_until("angle")
            self.wfull = MathTex(r"\omega t = 2\pi", font_size=37.5, color=TEAL)
            self.wfull.move_to(self.wr, aligned_edge=LEFT)
            ring = Circle(radius=0.42).move_to(ak.PLANE_O).set_stroke(TEAL, 9)
            self.play(*swap(self.wr, self.wfull), VShowPassingFlash(ring, time_width=0.6),
                      run_time=1.3)
            c.wait_until("omega radians")
            self.L0 = MathTex(r"\omega", "T", "=", r"2\pi", font_size=40)
            self.L0[1].set_color(TEAL)
            self.L0[3].set_color(TEAL)
            self.L0.move_to([CX, 1.5, 0], aligned_edge=LEFT)
            self.tag0 = kit.tag("one full turn", self.L0, RIGHT, 0.35)
            self.play(*appear(self.L0, self.tag0, lag=0.4), run_time=1.4)

            c.wait_until("caption")
            self.L1 = col_line(r"T = \frac{2\pi}{\omega}", 0.25, x=CX + 0.16, size=48, teal=(0, 2, 3))
            self.box = SurroundingRectangle(self.L1, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
            self.step = kit.step_label("divide by ω", 1)
            self.step.shift((1.06 - self.step.get_center()[1]) * UP)
            self.bn = kit.tag("beyond the notes", self.box, RIGHT, 0.3)
            self.play(*appear(self.step, self.L1, lag=0.4), run_time=1.3)
            self.play(FadeIn(self.box), *appear(self.bn, shift=None),
                      FlashAround(self.tr, time_width=1.5), run_time=1.1)
            self.boxg = VGroup()
            settle(self, self.boxg, add=[self.L1, self.box, self.bn])
            kit.legend_add(self, self.leg, E_PER, run_time=1.1)

            c.wait_until("read")
            self.read = T("one full turn ÷ turning rate", size=30, color=YELLOW)
            self.read.move_to([CX, -1.05, 0], aligned_edge=LEFT)
            self.play(*appear(self.read), run_time=1.0)
            c.wait_until("one full turn", nth=1)
            self.play(VShowPassingFlash(ring.copy(), time_width=0.6), run_time=1.2)
            c.wait_until("how fast")
            self.play(FlashAround(self.L1[0][5], time_width=1.5), run_time=1.3)

    # ── c2.beat.2: the 1 m pendulum, the grandfather clock ────────────────────
    def clip2(self):
        self.tt = ValueTracker(0.0)
        self.tt_on = False

        def tick(m, dt):
            if self.tt_on:
                m.increment_value(dt)
        self.tt.add_updater(tick)
        self.add(self.tt)
        tt = self.tt
        self.sign = 1.0
        self.p_len = ValueTracker(ROD)
        self.p_x = ValueTracker(grav.PIVOT[0])
        self.add(self.p_len, self.p_x)
        self.pend1 = always_redraw(lambda: pend(self.sign * AMP * math.cos(W1 * tt.get_value()),
                                                self.p_x.get_value(), self.p_len.get_value()))
        self._counts = {}

        def count():
            n = int(tt.get_value() / HALF1 + 1e-6)
            if n not in self._counts:
                self._counts[n] = T(f"{n} s", size=40).move_to([-5.5, 1.0, 0])
            return self._counts[n].copy()
        self.cnt = always_redraw(count)

        with self.say("c2.beat.2") as c:
            dy = 2.35 - self.box.get_center()[1]
            newleg = kit.legend(E_PEND, 3)
            sweep_clear(self, *during([self.axis.animate.put_start_and_end_on(
                                          np.array([-4.7, SWING_Y, 0]), np.array([-1.7, SWING_Y, 0]))],
                                      0.25, 0.8),
                        *during([self.boxg.animate.shift(dy * UP)], 0.5, 1.0),
                        *appear(self.pend1, self.cnt, newleg, shift=None, lag=0.2),
                        keep=[self.boxg, self.pin, self.axis, *self.trackers()],
                        run_time=1.6)
            self.leg = newleg
            self.tt_on = True

            c.wait_until("omega")
            self.w1 = col_line(r"\omega = \sqrt{9.81} \approx 3.13", 1.2)
            self.ps = T("per second", size=28).next_to(self.w1, RIGHT, buff=0.22)
            self.ps.align_to(self.w1, DOWN).shift(0.02 * UP)
            self.play(*appear(self.w1, self.ps, lag=0.4), run_time=1.3)

            c.wait_until("period")
            self.T1 = col_line(r"T = 2\pi/3.13 \approx 2.01\text{ s}", 0.5, teal=(0, 2, 3))
            self.play(*appear(self.T1), run_time=1.2)
            c.wait_until("one second each way")
            self.play(FlashAround(self.cnt, time_width=1.5), run_time=1.4)

            c.wait_until("clock")
            self.case = clock_case()
            self.cpend = always_redraw(lambda: clock_pendulum(AMP * math.cos(PI * tt.get_value())))
            self.play(*appear(self.case, self.cpend, shift=None, lag=0.2), run_time=1.3)
            self.len_lab = T("0.994 m", size=30).move_to([CLK_X + 0.75, -1.8, 0], aligned_edge=LEFT)
            c.wait_until("nine nine four")
            self.play(*appear(self.len_lab), run_time=1.0)
            self.sec_lab = T("one second per swing", size=28, color=YELLOW)
            self.sec_lab.move_to([CLK_X + 0.75, -2.55, 0], aligned_edge=LEFT)
            c.wait_until("each swing")
            self.play(*appear(self.sec_lab), run_time=1.0)

    # ── c2.beat.3: think stop, the 4 m pendulum ───────────────────────────────
    def clip3(self):
        tt = self.tt
        with self.say("c2.beat.3") as c:
            # freeze at the end of a swing; the clock leaves
            now = tt.get_value()
            k = math.ceil(now / HALF1 - 1e-6)
            target = k * HALF1
            if target - now < 0.6:
                k += 1
                target = k * HALF1
            self.tt_on = False
            dt = target - now
            self.play(tt.animate(rate_func=linear).set_value(target),
                      *[time_span(FadeOut(m), 0, 0.8) for m in (self.cnt, self.axis)],
                      run_time=max(dt, 0.8))
            self.sign = 1.0 if k % 2 == 0 else -1.0
            # restart the clock at 0 from this side
            tt.set_value(0.0)
            self._counts = {}
            self.p_len.set_value(ROD)

            # the 1 m shrinks to scale; the 4 m hangs beside it
            self.lab1 = T("1 m", size=30).move_to([X1M_SMALL + 0.62, PIV_Y - 0.6, 0])
            self.play(self.p_len.animate.set_value(L_SMALL), self.p_x.animate.set_value(X1M_SMALL),
                      *disappear(self.case, self.cpend, self.len_lab, self.sec_lab), run_time=1.4)
            self.pend4 = always_redraw(lambda: pend(self.sign * AMP * math.cos(W4 * tt.get_value()),
                                                    X4M, 4 * L_SMALL))
            self.lab4 = T("4 m", size=30).move_to([X4M + 1.0, PIV_Y - 2.0, 0])
            self.play(*appear(self.pend4, shift=None), *appear(self.lab1, self.lab4, lag=0.3),
                      run_time=1.2)

            c.wait_until("period")
            self.think = kit.think_box("A pendulum 4 m long.\nWhat's its period?", pos=kit.THINK_POS + 0.3 * UP)
            self.play(*appear(self.think, shift=None), run_time=1.0)
            c.wait_until("pause")
            self.ring = kit.think_ring()
            self.play(FadeIn(self.ring), run_time=0.6)
            self.play(kit.drain(self.ring, run_time=max(1.0, c.until("quarter") - 0.2)))

            c.wait_until("quarter")
            self.play(*disappear(self.think, self.ring), *set_alpha([self.w1, self.ps, self.T1], 0.4),
                      run_time=1.0)
            self.w4sq = col_line(r"\omega^2 = 9.81/4 \approx 2.45", -0.3)
            self.q1 = kit.tag("a quarter as big", self.w4sq, RIGHT, 0.35)
            self.play(*appear(self.w4sq), run_time=1.2)
            c.wait_until(own_word=self.q1)
            self.play(*appear(self.q1), run_time=1.0)
            # both swing from here, in real time: the 4 m once while the 1 m twice
            self.cnt = always_redraw(lambda: self._count3())
            self.play(*appear(self.cnt, shift=None), run_time=0.6)
            self.tt_on = True

            c.wait_until("omega")
            self.w4 = col_line(r"\omega \approx 1.57", -1.0)
            self.q2 = kit.tag("half as big", self.w4, RIGHT, 0.35)
            self.play(*appear(self.w4, self.q2, lag=0.4), run_time=1.2)
            c.wait_until("double")
            self.T4 = col_line(r"T = 2\pi/1.57 \approx 4.0\text{ s}", -1.7, teal=(0, 2, 3))
            self.q3 = kit.tag("twice as long", self.T4, RIGHT, 0.35)
            self.play(*appear(self.T4, self.q3, lag=0.4), run_time=1.3)
            c.wait_until("about four seconds")
            self.play(FlashAround(self.T4[0][-4:], time_width=1.5), run_time=1.3)

    def _count3(self):
        n = int(self.tt.get_value() / HALF1 + 1e-6)
        if n not in self._counts:
            self._counts[n] = T(f"{n} s", size=40).move_to([X1M_SMALL, 0.6, 0])
        return self._counts[n].copy()

    # ── c2.beat.4: no size in it; two arrows turn together ────────────────────
    def clip4(self):
        self.t4 = ValueTracker(0.0)
        self.add(self.t4)
        t4 = self.t4
        kw_in = dict(scale=S4, origin=O4)
        self.pl4 = ak.plane(scale=S4, origin=O4, re_units=2.0, im_units=2.0)
        self.a1 = ak.turning_arrow(t4, length=1.0, **kw_in)
        self.a2 = ak.turning_arrow(t4, length=2.0, **kw_in)
        self.s1 = ak.shadow(t4, length=1.0, **kw_in)
        self.s2 = ak.shadow(t4, length=2.0, **kw_in)
        self.b1 = ak.spring_on_axis(t4, length=1.0, scale=S4, origin=np.array([O4[0], Y_IN, 0]))
        self.b2 = ak.spring_on_axis(t4, length=2.0, scale=S4, origin=np.array([O4[0], Y_OUT, 0]))
        x4 = 0.3
        with self.say("c2.beat.4") as c:
            self.quote = T("“a wider swing takes longer”", size=30, color=YELLOW)
            self.quote.move_to([x4, 2.3, 0], aligned_edge=LEFT)
            self.cnt.clear_updaters()           # its glyph count must not change mid-fade
            dst = np.array([x4 + 0.16 + self.L1.width / 2, 0.9, 0]) - self.L1.get_center()
            sweep_clear(self, *appear(self.pl4, self.b1, self.b2, self.s1, self.s2, self.a1, self.a2,
                                      shift=None, lag=0.08),
                        *during([self.boxg.animate.shift(dst)], 0.5, 1.0),
                        keep=[self.boxg, self.leg, self.pin, *self.trackers()], run_time=1.8)
            c.wait_until(own_word=self.quote)
            self.play(*appear(self.quote), run_time=1.0)

            c.wait_until("formula")
            self.ul = underline(self.L1, YELLOW, buff=0.22)
            self.play(*disappear(self.box, self.bn), run_time=0.8)
            self.play(Create(self.ul), run_time=0.8)
            self.nosize = T("no size in it", size=32).next_to(self.L1, RIGHT, buff=0.6)
            c.wait_until(own_word=self.nosize)
            self.play(*appear(self.nosize), run_time=1.0)

            c.wait_until("arrows")
            kit.legend_set(self, self.leg, E_TWO, run_time=0.9)
            # the riskiest play: both arrows turn; the quote gets its strike and ✗
            k = max(1, math.floor((c.until("why") + 1.0 - T_FREEZE0) / PI))
            tf = T_FREEZE0 + k * PI
            a = min(max(0.0, c.until("together", floor=0.0)), tf - 1.4)
            self.strike = Line(self.quote.get_left() + 0.05 * LEFT, self.quote.get_right() + 0.05 * RIGHT)
            self.strike.set_stroke(RED, 4)
            self.xm = cross_mark().next_to(self.quote, RIGHT, buff=0.3)
            self.risky_at = c.at("arrows") + 0.9
            self.play(t4.animate(rate_func=linear).set_value(tf),
                      time_span(Create(self.strike), a, a + 0.8),
                      time_span(FadeIn(self.xm, scale=0.6), a + 0.3, a + 1.1),
                      run_time=tf)

            c.wait_until("twice the pull")
            ang = ak.OMEGA * tf
            pull1, pull2, vel1, vel2 = [], [], [], []
            for L, y, store_p, store_v in ((1.0, Y_IN, pull1, vel1), (2.0, Y_OUT, pull2, vel2)):
                xr = ak.PLANE_R * S4 * L * math.cos(ang)
                bx = O4[0] + xr
                store_p.append(ak.arrow_between(np.array([bx, y + 0.42, 0]),
                                                np.array([bx - 1.0 * xr, y + 0.42, 0]), RED, 5, 1))
                vx = -ak.PLANE_R * S4 * L * math.sin(ang) * 1.6
                store_v.append(ak.arrow_between(np.array([bx, y + 0.42, 0]),
                                                np.array([bx + vx, y + 0.42, 0]), GREEN, 5, 1))
            self.pulls = [pull1[0], pull2[0]]
            self.vels = [vel1[0], vel2[0]]
            self.play(LaggedStart(*[GrowArrow(p) for p in self.pulls], lag_ratio=0.5), run_time=1.5)
            c.wait_until("twice as fast")
            self.play(*during(disappear(*self.pulls), 0, 0.4),
                      *during([GrowArrow(v) for v in self.vels], 0.4, 1.0), run_time=1.6)

    # ── c2.beat.5: the catch at big angles ────────────────────────────────────
    def clip5(self):
        self.sim = ValueTracker(0.0)
        self.add(self.sim)
        sim = self.sim
        self.rate = 0.0

        def tick(m, dt):
            if self.rate:
                m.increment_value(dt * self.rate)
        sim.add_updater(tick)
        p10 = always_redraw(lambda: pend(theta10(sim.get_value()), X10, ROD))
        p60 = always_redraw(lambda: pend(theta60(sim.get_value()), X60, ROD))
        r10 = deg_readout(lambda: theta10(sim.get_value()), [X10, -0.85, 0])
        r60 = deg_readout(lambda: theta60(sim.get_value()), [X60, -0.85, 0])
        corner = kit.corner_tag()
        with self.say("c2.beat.5") as c:
            sweep_clear(self, *appear(p10, p60, r10, r60, corner, shift=None, lag=0.15),
                        keep=[self.leg, self.pin, *self.trackers()], run_time=1.8)
            kit.legend_set(self, self.leg, E_BIG, run_time=1.1)

            c.wait_until("pulled back less")
            self.real = MathTex(r"\ddot{x} = -\frac{g}{L}\sin x", font_size=40)
            self.real[0][0].set_color(RED)     # the dots of x-double-dot
            self.real[0][1].set_color(RED)
            self.real[0][10].set_color(BLUE)   # x in sin x
            self.real.move_to([CX, 2.25, 0], aligned_edge=LEFT)
            self.rcap = kit.tag("the real pull", self.real, RIGHT, 0.35)
            self.play(*appear(self.real, self.rcap, lag=0.4), run_time=1.4)

            c.wait_until("pct")
            head = T("period longer by", size=26, color=DIM).move_to([CX, 1.2, 0], aligned_edge=LEFT)
            rows = [T(s, size=32, t2c={p: GOLD}) for s, p in
                    (("10°:  +0.2%", "+0.2%"), ("30°:  +1.7%", "+1.7%"), ("60°:  +7.3%", "+7.3%"))]
            for i, r in enumerate(rows):
                r.move_to([CX + 0.2, 0.62 - 0.6 * i, 0], aligned_edge=LEFT)
            self.play(*appear(head, rows[0], lag=0.4), run_time=1.3)  # early: the table's header
            c.wait_until("thirty degrees")
            self.play(*appear(rows[1]), run_time=1.0)
            c.wait_until("sixty degrees")
            self.play(*appear(rows[2]), run_time=1.0)

            c.wait_until("drift")
            clk = ak.t_readout(sim).move_to([CX, -1.45, 0], aligned_edge=LEFT)
            x3 = kit.tag("× 3").move_to([CX + 2.75, -1.45, 0], aligned_edge=LEFT)
            self.play(*appear(clk, x3, lag=0.3, shift=None), run_time=0.9)
            self.play(sim.animate(rate_func=linear).set_value(15.1), run_time=15.1 / 3)
            x1 = kit.tag("× 1").move_to(x3, aligned_edge=LEFT)
            self.rate = 1.0
            self.play(*swap(x3, x1), run_time=1.0)

            c.wait_until("small")
            self.smallq = T("same beat at any size:\nfor small swings", size=32, color=YELLOW,
                            line_spacing=0.9)
            self.smallq.move_to([CX, -2.6, 0], aligned_edge=LEFT)
            self.play(*appear(self.smallq), run_time=1.2)
