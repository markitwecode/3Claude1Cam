"""Chapter 4, scene 3: the ball on the hill (metastability pictured). Clips c4.ball.1 – c4.ball.4."""
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


# =============================================================================================
# Gate drawings, copied verbatim from l06 ch1_s2_rslatch.py (rs_latch() and its helpers).
# =============================================================================================
WIRE, ON, OFF = FG, GREEN, DIM
WIRE_W = 4
GATE_COLOR = BLUE


def _p(x, y):
    return np.array([x, y, 0.0])


def wire(*pts, color=WIRE):
    """Polyline wire through (x, y) points."""
    w = VMobject().set_points_as_corners([_p(*p) if len(p) == 2 else np.array(p) for p in pts])
    return w.set_stroke(color, WIRE_W)


def junction(x, y, color=WIRE):
    return Dot(_p(x, y), radius=0.07, color=color)


def wire_color(v):
    return ON if v else OFF


def light(w, v=None, color=None):
    """Animation: wire (or VGroup of wires and junction dots) to value v (1 bright, 0 dim),
    or to `color` (e.g. WIRE for neutral)."""
    return w.animate.set_color(color if color is not None else wire_color(v))


class Gate(VGroup):
    def __init__(self, body, ins, out, bubble=None, num=None, num_at=(-0.1, 0.0), color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body, self.bubble = body, bubble
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        if bubble is not None:
            bubble.set_stroke(color, 4).set_fill(BG, 1)
            self.add(bubble)
        self.num = None
        if num is not None:
            self.num = T(str(num), size=28, color=DIM).move_to(_p(*num_at))
            self.add(self.num)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def nor_gate(num=None, color=GATE_COLOR):
    """Distinctive-shape NOR (OR body + output bubble), 1.6 wide x 1.2 tall, centred at ORIGIN."""
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    bubble = Circle(radius=0.1).move_to(_p(0.8, 0))
    return Gate(b, [(-0.56, 0.3), (-0.56, -0.3)], (0.9, 0.0), bubble=bubble, num=num, color=color)


class RSLatch(VGroup):
    """Slide p. 79 NOR RS latch. .g1 .g2 .gates, .r .s, .q = VGroup(.q_out, .fq, .q_dot),
    .qb = VGroup(.qb_out, .fqb, .qb_dot), .wires, .lab_r .lab_s (BLUE) .lab_q .lab_qb (GREEN).
    Unscaled 5.4 wide x 3.6 tall, centred at ORIGIN."""

    def __init__(self, labels=True):
        super().__init__()
        g1, g2 = nor_gate(1).shift(1.2 * UP), nor_gate(2).shift(1.2 * DOWN)
        self.g1, self.g2, self.gates = g1, g2, VGroup(g1, g2)
        a1, b1, a2, b2 = g1.inp(0), g1.inp(1), g2.inp(0), g2.inp(1)
        o1, o2 = g1.out(), g2.out()
        xl, xr, xt, xf = -2.2, 2.2, 1.4, -1.2
        self.r = wire((xl, a1[1]), tuple(a1[:2]))
        self.s = wire((xl, b2[1]), tuple(b2[:2]))
        self.q_out = wire(tuple(o1[:2]), (xr, o1[1]))
        self.qb_out = wire(tuple(o2[:2]), (xr, o2[1]))
        self.fq = wire((xt, o1[1]), (xt, 0.5), (xf, -0.5), (xf, a2[1]), tuple(a2[:2]))
        self.fqb = wire((xt, o2[1]), (xt, -0.5), (xf, 0.5), (xf, b1[1]), tuple(b1[:2]))
        self.q_dot, self.qb_dot = junction(xt, o1[1]), junction(xt, o2[1])
        self.q = VGroup(self.q_out, self.fq, self.q_dot)
        self.qb = VGroup(self.qb_out, self.fqb, self.qb_dot)
        self.wires = {"r": self.r, "s": self.s, "q": self.q, "qb": self.qb}
        self.add(self.r, self.s, self.q, self.qb, g1, g2)
        self.lab_r = MathTex("R", font_size=48, color=BLUE).next_to(self.r.get_start(), LEFT, buff=0.15)
        self.lab_s = MathTex("S", font_size=48, color=BLUE).next_to(self.s.get_start(), LEFT, buff=0.15)
        self.lab_q = MathTex("Q", font_size=48, color=GREEN).next_to(self.q_out.get_end(), RIGHT, buff=0.15)
        self.lab_qb = MathTex(r"\overline{Q}", font_size=48, color=GREEN).next_to(
            self.qb_out.get_end(), RIGHT, buff=0.15)
        self.labels = VGroup(self.lab_r, self.lab_s, self.lab_q, self.lab_qb)
        if labels:
            self.add(*self.labels)


def rs_latch(labels=True):
    """The L6 RS latch at unit scale, centred at ORIGIN (see RSLatch)."""
    return RSLatch(labels=labels)


# =============================================================================================
# The hill (slide p. 110), shared with s4 (small copy, ball leaving the summit) and the recap.
#   hill(xs, ys, labels) -> Hill: a BLUE double-valley curve y = ys * (u^2 - 1)^2, x = xs * u,
#     u in [-1.42, 1.42]; valleys at u = -1 (state 0) and u = +1 (state 1), summit at u = 0.
#     Local origin = midpoint between the valley bottoms. Default 8.5 wide, summit 2.5 high.
#     .curve, .lab0 / .lab1 (GREEN digit over "stable"), .lab_meta (RED "metastable"), .labels.
#     .point(u) -> the curve point; .ball_point(u, r) -> centre of a ball of radius r resting
#     there. Both follow any move/scale of the Hill (anchors ride along inside it).
#   ball(color, r) -> filled disc; place(b, hill, u) puts it on the curve at u.
#   timer(size) -> FG DecimalNumber "0.0 τ".
# =============================================================================================
U_END = 1.42
TAU_S = 1.0          # seconds of screen time per τ in the timers and the race


def _f(u):
    return (u * u - 1.0) ** 2


class Hill(VGroup):
    def __init__(self, xs=3.0, ys=2.5, labels=True, color=BLUE, width=6):
        super().__init__()
        self.curve = ParametricFunction(lambda u: _p(u * xs, _f(u) * ys), t_range=(-U_END, U_END, 0.01))
        self.curve.set_stroke(color, width)
        self._o, self._ux, self._uy = VectorizedPoint(ORIGIN), VectorizedPoint(_p(xs, 0)), VectorizedPoint(_p(0, ys))
        self.add(self.curve, self._o, self._ux, self._uy)
        self.lab0 = VGroup(T("0", size=56, color=GREEN), T("stable", size=36)).arrange(DOWN, buff=0.1)
        self.lab1 = VGroup(T("1", size=56, color=GREEN), T("stable", size=36)).arrange(DOWN, buff=0.1)
        self.lab0.next_to(self.point(-1), DOWN, buff=0.3)
        self.lab1.next_to(self.point(1), DOWN, buff=0.3)
        self.lab_meta = T("metastable", size=44, color=RED).next_to(self.point(0), UP, buff=0.85)
        self.labels = VGroup(self.lab0, self.lab1, self.lab_meta)
        if labels:
            self.add(*self.labels)

    def point(self, u):
        o = self._o.get_center()
        return o + u * (self._ux.get_center() - o) + _f(u) * (self._uy.get_center() - o)

    def ball_point(self, u, r):
        t = self.point(u + 1e-3) - self.point(u - 1e-3)
        n = np.array([-t[1], t[0], 0.0])
        return self.point(u) + r * n / np.linalg.norm(n)


def hill(xs=3.0, ys=2.5, labels=True, color=BLUE, width=6):
    return Hill(xs, ys, labels, color, width)


def ball(color=RED, r=0.3):
    b = Circle(radius=r).set_stroke(width=0).set_fill(color, 1)
    b.r = r
    return b


def place(b, h, u):
    return b.move_to(h.ball_point(u, b.r))


def timer(size=48):
    return DecimalNumber(0, num_decimal_places=1, unit=r"\,\tau", font_size=size, color=FG)


# =============================================================================================
# Scene helpers
# =============================================================================================
def rock(b, h, u0, d, amp=0.32):
    """Nudged in a valley: the ball swings up the slope (direction d) and settles back."""
    return UpdateFromAlphaFunc(
        b, lambda m, a: place(m, h, u0 + d * amp * np.exp(-2.5 * a) * np.sin(3 * PI * a)),
        rate_func=linear)


def fall_u(t, x0, T, d, settle=8.0):
    """Linear model near the top: distance from the summit grows like e^(t/τ'), reaching the
    valley (u = ±1) at time T; then a short damped rock in the valley."""
    if t < T:
        tau = T / np.log(1.0 / x0)
        return d * min(1.0, x0 * np.exp(t / tau))
    s = t - T
    v = np.log(1.0 / x0) / T
    return d * (1.0 + (v / settle) * np.exp(-5 * s) * np.sin(settle * s))


def wind_line(y, x0):
    w = ParametricFunction(lambda x: _p(x, 0.09 * np.sin(4.5 * x)), t_range=(0, 1.9, 0.02))
    return w.set_stroke(FG, 3, opacity=0.35).move_to(_p(x0, y))


class BallOnHill(NarratedScene):
    def construct(self):
        H = hill().shift(0.9 * DOWN)          # valleys y -0.9, summit 1.6

        # ---------------------------------------------------------------- c4.ball.1
        with self.say("c4.ball.1") as c:
            self.play(Create(H.curve), run_time=2.0)
            self.add(H._o, H._ux, H._uy)
            c.wait_until("ball")
            b0 = place(ball(GREEN), H, -1)
            self.play(FadeIn(b0, shift=0.4 * DOWN), run_time=1.0)
            c.wait_until("valleys")
            b1 = place(ball(GREEN), H, 1)
            self.play(FadeIn(b1, shift=0.4 * DOWN), *appear(H.lab0, H.lab1, lag=0.5), run_time=1.6)
            c.wait_until("nudge")
            a0 = Arrow(b0.get_left() + 1.1 * LEFT, b0.get_left() + 0.05 * LEFT, buff=0,
                       stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.3)
            self.play(GrowArrow(a0), run_time=0.7)
            self.play(rock(b0, H, -1, +1), FadeOut(a0), run_time=2.4)
            a1 = Arrow(b1.get_right() + 1.1 * RIGHT, b1.get_right() + 0.05 * RIGHT, buff=0,
                       stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.3)
            self.play(GrowArrow(a1), run_time=0.5)
            self.play(rock(b1, H, 1, -1), FadeOut(a1), run_time=min(1.8, c.until(floor=1.0)))

        # ---------------------------------------------------------------- c4.ball.2
        with self.say("c4.ball.2") as c:
            br = place(ball(RED), H, 0)
            self.play(*during(disappear(b0, b1), 0, 0.45),
                      *during(FadeIn(br, shift=0.5 * DOWN), 0.4, 1), run_time=1.6)
            c.wait_until("forever")
            tm = timer().move_to(_p(1.8, 1.75))
            self.play(*appear(tm, shift=None), run_time=0.8)
            tm.add_updater(lambda m, dt: m.set_value(m.get_value() + dt / TAU_S))
            c.wait_until("called")
            self.play(*appear(H.lab_meta), run_time=1.0)
            c.wait_until("wind")
            winds = [wind_line(y, x) for y, x in ((2.0, -5.6), (2.6, -6.0), (3.2, -5.4))]
            R = c.until("roll")
            self.add(*winds)

            def drift(i):
                w, x_start = winds[i], winds[i].get_x()

                def f(m, a):
                    m.set_x(x_start + 3.0 * a + 0.4 * i)
                    m.set_stroke(opacity=0.35 * there_and_back(a))
                return UpdateFromAlphaFunc(w, f, rate_func=linear)

            def tremble(m, a):
                t = a * R
                place(m, H, 0.012 * min(1.0, 2 * a) * np.sin(2 * PI * 6 * t / 1.0))
            self.play(*[drift(i) for i in range(3)], UpdateFromAlphaFunc(br, tremble, rate_func=linear),
                      run_time=R)
            self.remove(*winds)
            RR = min(2.6, c.until(floor=1.5))

            def roll(m, a):
                t = a * RR
                place(m, H, fall_u(t, 0.02, 0.6 * RR, +1))
                k = np.clip((t - 0.6 * RR) / 0.3, 0, 1)
                m.set_fill(interpolate_color(ManimColor(RED), ManimColor(GREEN), k))
            self.play(UpdateFromAlphaFunc(br, roll, rate_func=linear), run_time=RR)
            tm.clear_updaters()

        # ---------------------------------------------------------------- c4.ball.3
        with self.say("c4.ball.3") as c:
            fracs = [0.3, 0.1, 0.03, 0.01, 0.003]
            sides = [+1, -1, +1, -1, +1]
            ys = [2.3, 1.05, -0.2, -1.45, -2.7]
            lanes = [hill(xs=1.9, ys=0.75, labels=False, width=4).shift(_p(-1.2, y)) for y in ys]
            balls = [place(ball(RED, r=0.2), L, s * x) for L, s, x in zip(lanes, sides, fracs)]
            timers = [timer().move_to(_p(3.4, y + 0.35)) for y in ys]
            self.play(*during(disappear(H.labels, br, tm), 0, 0.45),
                      *during(ReplacementTransform(H.curve, VGroup(*[L.curve for L in lanes])), 0.2, 1),
                      run_time=1.8)
            self.remove(H._o, H._ux, H._uy)
            for L in lanes:
                self.add(L._o, L._ux, L._uy)
            self.play(*[FadeIn(b, shift=0.3 * DOWN) for b in balls], run_time=1.0)
            c.wait_until("race")
            self.play(*appear(*timers, shift=None, lag=0.15), run_time=1.2)
            Ts = [TAU_S * np.log(1 / x) for x in fracs]
            RT = Ts[-1] + 0.8

            def runner(i):
                L, b, tmr, x, s, Ti = lanes[i], balls[i], timers[i], fracs[i], sides[i], Ts[i]

                def f(m, a):
                    t = a * RT
                    place(m, L, fall_u(t, x, Ti, s))
                    k = np.clip((t - Ti) / 0.25, 0, 1)
                    m.set_fill(interpolate_color(ManimColor(RED), ManimColor(GREEN), k))
                return UpdateFromAlphaFunc(b, f, rate_func=linear)

            def clock(i):
                Ti = Ts[i]
                return UpdateFromAlphaFunc(
                    timers[i], lambda m, a: m.set_value(min(a * RT, Ti) / TAU_S), rate_func=linear)

            self.play(*[runner(i) for i in range(5)], *[clock(i) for i in range(5)], run_time=RT)
            self.play(*flash(timers[-1]), run_time=1.2)
            c.wait_until("eventually")
            H2 = hill().shift(0.9 * DOWN)
            self.play(*during(disappear(*balls, *timers), 0, 0.45),
                      *during(ReplacementTransform(VGroup(*[L.curve for L in lanes]), H2.curve), 0.2, 0.8),
                      *during(appear(H2.labels, lag=0.1), 0.5, 1), run_time=2.0)
            for L in lanes:
                self.remove(L._o, L._ux, L._uy)
            self.add(H2)
            c.wait_until("settle")
            line = T("eventually a valid 0 or 1, at an unpredictable time", size=40,
                     t2c={"0": GREEN, "1": GREEN}).move_to(_p(0, -3.3))
            self.play(*appear(line), run_time=1.0)

        # ---------------------------------------------------------------- c4.ball.4
        with self.say("c4.ball.4") as c:
            self.play(*disappear(H2.labels), run_time=0.8)
            H2.remove(*H2.labels)
            self.play(H2.animate.scale(0.75).move_to(_p(-3.5, 0.55)), run_time=1.5)
            c.wait_until("Inside")
            latch = rs_latch()
            for g in latch.gates:
                g.remove(g.num)
            latch.scale(0.8).move_to(_p(3.9, 0.6))
            self.play(*during(disappear(line), 0, 0.45), *during(FadeIn(latch), 0.4, 1), run_time=1.6)
            c.wait_until("feedback loop")
            loops = [latch.fq, latch.fqb]
            self.play(*[light(w, color=YELLOW) for w in loops],
                      *[VShowPassingFlash(w.copy().set_stroke(YELLOW, 10), time_width=0.5) for w in loops],
                      run_time=1.6)
            c.wait_until("states")
            tag0 = MathTex("Q = 0", font_size=48, color=GREEN).move_to(_p(2.0, -3.1))
            tag1 = MathTex("Q = 1", font_size=48, color=GREEN).move_to(_p(2.0, -2.1))
            ln0 = DashedLine(tag0.get_left() + 0.15 * LEFT, H2.point(-1) + 0.12 * DOWN,
                             dash_length=0.12, color=GREEN, stroke_width=2)
            ln1 = DashedLine(tag1.get_left() + 0.15 * LEFT, H2.point(1) + 0.12 * DOWN,
                             dash_length=0.12, color=GREEN, stroke_width=2)
            self.play(*appear(tag0), Create(ln0), run_time=1.2)
            c.wait_until("at one")
            self.play(*appear(tag1), Create(ln1), run_time=1.2)
            c.wait_until("balance")
            tagm = MathTex(r"Q \text{ and } \overline{Q} \text{ both halfway}", font_size=44,
                           color=RED).move_to(_p(2.6, 3.3))
            bm = place(ball(RED, r=0.22), H2, 0)
            lnm = DashedLine(tagm.get_left() + 0.15 * LEFT, bm.get_top() + 0.1 * UP,
                             dash_length=0.12, color=RED, stroke_width=2)
            self.play(*appear(tagm), Create(lnm), FadeIn(bm, shift=0.3 * DOWN), run_time=1.4)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
