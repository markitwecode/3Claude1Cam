"""Chapter 2, scene 2: try an exponential; the rule asks for λ² = −ω², so λ = ±iω. Clips c2.guess.1 – c2.guess.4.

Exported for the recap (s9):
- lambda_picture(scale=1.0, lam=1.0): axes (t 0..2.5, value 0..4), the live curve e^{λt}, the
  slider and the "λ = 1.00" readout. Drive it with `g.tracker` (λ). Build it at the size you want
  with `scale`, then move it as a whole (.move_to / .shift).
- parabola_picture(scale=1.0): axes (λ −3..3), the parabola λ², the RED dashed line at −ω² = −4
  with its label, an FG dot riding λ² and readouts "λ = …", "λ² = …". Drive it with `g.tracker`.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

kit = load_scene("ch1_s2_tools")

ENTRIES = [(r"x", BLUE, "displacement"), (r"\dot{x}", GREEN, "velocity"),
           (r"\ddot{x}", RED, "acceleration"), (r"\omega", FG, "angular frequency, rad/s"),
           (r"t", FG, "time")]
E_LAM = (r"\lambda", FG, "trial rate")

EXP_ORIGIN = np.array([-5.9, -0.45, 0])
PAR_ORIGIN = np.array([-3.9, 0.25, 0])
READ_POS = np.array([-5.55, 2.3, 0])        # readout slot inside the exp axes (upper left)
READ_POS2 = np.array([-2.55, 2.3, 0])       # second slot (upper right, where e^t has left)
S = kit.COL_SIZE


PITCH2 = 0.8   # c2.guess.2's column: a little more pitch than kit.COL_PITCH so step labels clear the lines


def _cplace(mob, i):
    return kit.col_place(mob, i).shift(i * (PITCH2 - kit.COL_PITCH) * DOWN)


def _slabel(text, i):
    return kit.step_label(text, i).shift((i - 0.5) * (PITCH2 - kit.COL_PITCH) * DOWN)


def rule_pin():
    """The pinned rule ẍ = −ω²x (ẍ RED, x BLUE, ω FG), label "the rule" (same as ch2_s1_hook)."""
    p = kit.pinned([r"\ddot{x}", "=", r"-\omega^2", "x"], label="the rule")
    p.formula[0].set_color(RED)
    p.formula[3].set_color(BLUE)
    return p


# ── pictures (module level: the recap reuses them) ──────────────────────────────
def _exp_axes(scale=1.0):
    ax = Axes(x_range=[0, 2.5, 0.5], y_range=[0, 4, 1], x_length=5.4 * scale, y_length=3.1 * scale,
              tips=False, axis_config={"color": DIM, "stroke_width": 2})
    ax.shift(EXP_ORIGIN - ax.c2p(0, 0))
    grid = VGroup(*[Line(ax.c2p(t, 0), ax.c2p(t, 4)) for t in (0.5, 1, 1.5, 2, 2.5)],
                  *[Line(ax.c2p(0, v), ax.c2p(2.5, v)) for v in (1, 2, 3, 4)])
    grid.set_stroke(DIM, 1, opacity=0.35)
    ticks = VGroup(*[MathTex(str(t), font_size=24 * scale, color=DIM).next_to(ax.c2p(t, 0), DOWN, buff=0.12 * scale)
                     for t in (1, 2)],
                   *[MathTex(str(v), font_size=24 * scale, color=DIM).next_to(ax.c2p(0, v), LEFT, buff=0.12 * scale)
                     for v in (1, 2, 3)])
    tl = MathTex("t", font_size=30 * scale, color=FG).next_to(ax.c2p(2.5, 0), RIGHT, buff=0.15 * scale)
    vl = T("value", size=24 * scale, color=DIM).next_to(ax.c2p(0, 4), UP, buff=0.1 * scale)
    g = VGroup(grid, ax, ticks, tl, vl)
    g.axes, g.grid = ax, grid
    return g


def _exp_graph(ax, lam, color, width=4):
    tmax = 2.5 if lam <= 0.01 else min(2.5, np.log(4.0) / lam)
    return ax.plot(lambda t: np.exp(lam * t), x_range=[0, tmax, tmax / 60], color=color,
                   stroke_width=width)


def lambda_picture(scale=1.0, lam=1.0):
    """Axes, live curve e^{λt}, slider under the axes, readout "λ = 1.00".
    .frame (static axes group) .axes .curve .label .slider .handle .readout .tracker"""
    s = scale
    frame = _exp_axes(s)
    ax = frame.axes
    lab = MathTex(r"x = e^{\lambda t}", font_size=36 * s, color=FG)
    lab.move_to(ax.c2p(0, 0) + np.array([0.35, 2.75, 0]) * s, aligned_edge=LEFT)
    # slider: λ from −1 to 1, under the axes (right part, clear of the legend)
    y = ax.c2p(0, 0)[1] - 0.95 * s
    x0, x1 = ax.c2p(0, 0)[0] + 3.9 * s, ax.c2p(0, 0)[0] + 6.1 * s
    track = Line([x0, y, 0], [x1, y, 0]).set_stroke(DIM, 3)
    marks = VGroup(*[Line([x0 + (x1 - x0) * (v + 1) / 2, y - 0.08 * s, 0],
                          [x0 + (x1 - x0) * (v + 1) / 2, y + 0.08 * s, 0]).set_stroke(DIM, 2)
                     for v in (-1, 0, 1)])
    nums = VGroup(*[MathTex(t, font_size=24 * s, color=DIM).next_to(m, DOWN, buff=0.1 * s)
                    for t, m in zip(("-1", "0", "1"), marks)])
    slider = VGroup(track, marks, nums)
    rl = MathTex(r"\lambda =", font_size=32 * s, color=FG)
    num = DecimalNumber(lam, num_decimal_places=2, font_size=32 * s, color=FG)
    rl.move_to([(x0 + x1) / 2 - 0.9 * s, y - 0.75 * s, 0])
    num.next_to(rl, RIGHT, buff=0.15 * s)
    tracker = ValueTracker(lam)

    def lam_now():
        return float(np.clip(tracker.get_value(), -1, 1))

    num.add_updater(lambda m: m.set_value(tracker.get_value()).next_to(rl, RIGHT, buff=0.15 * s))
    curve = always_redraw(lambda: _exp_graph(ax, tracker.get_value(), FG))
    handle = always_redraw(lambda: Dot([x0 + (x1 - x0) * (lam_now() + 1) / 2, y, 0],
                                       radius=0.11 * s, color=FG))
    readout = VGroup(rl, num)
    g = VGroup(frame, curve, lab, slider, handle, readout)
    g.frame, g.axes, g.curve, g.label, g.slider, g.handle, g.readout, g.tracker = (
        frame, ax, curve, lab, slider, handle, readout, tracker)
    return g


def parabola_picture(scale=1.0):
    """λ across (−3..3), λ² up, the parabola, RED dashed line at −ω² = −4 with label, an FG dot
    riding λ² with readouts. .frame .axes .curve .target (line, label) .dot .readouts .tracker"""
    s = scale
    ax = Axes(x_range=[-3, 3, 1], y_range=[-5, 9, 1], x_length=4.6 * s, y_length=3.8 * s,
              tips=False, axis_config={"color": DIM, "stroke_width": 2, "tick_size": 0.05 * s})
    ax.shift(PAR_ORIGIN - ax.c2p(0, 0))
    ticks = VGroup(*[MathTex(str(v).replace("-", "-"), font_size=22 * s, color=DIM)
                     .next_to(ax.c2p(v, 0), DOWN, buff=0.1 * s) for v in (-3, -2, -1, 1, 2, 3)],
                   *[MathTex(str(v), font_size=22 * s, color=DIM).next_to(ax.c2p(0, v), LEFT, buff=0.1 * s)
                     for v in (4, 8)])
    xl = MathTex(r"\lambda", font_size=30 * s, color=FG).next_to(ax.c2p(3, 0), RIGHT, buff=0.15 * s)
    yl = MathTex(r"\lambda^2", font_size=30 * s, color=FG).next_to(ax.c2p(0, 9), RIGHT, buff=0.12 * s)
    frame = VGroup(ax, ticks, xl, yl)
    curve = ax.plot(lambda v: v * v, x_range=[-3, 3, 0.05], color=FG, stroke_width=4)
    line = DashedLine(ax.c2p(-3, -4), ax.c2p(3, -4), dash_length=0.12 * s).set_stroke(RED, 3)
    tlab = MathTex(r"-\omega^2 = -4", font_size=30 * s, color=RED).next_to(line, RIGHT, buff=0.15 * s)
    target = VGroup(line, tlab)
    tracker = ValueTracker(-3.0)
    dot = always_redraw(lambda: Dot(ax.c2p(tracker.get_value(), tracker.get_value() ** 2),
                                    radius=0.1 * s, color=FG))
    r1l = MathTex(r"\lambda =", font_size=32 * s, color=FG)
    r2l = MathTex(r"\lambda^2 =", font_size=32 * s, color=FG)
    r1l.move_to(ax.c2p(0, 0) + np.array([2.4, -1.75, 0]) * s, aligned_edge=RIGHT)
    r2l.move_to(ax.c2p(0, 0) + np.array([2.4, -2.3, 0]) * s, aligned_edge=RIGHT)
    n1 = DecimalNumber(-3.0, num_decimal_places=2, font_size=32 * s, color=FG)
    n2 = DecimalNumber(9.0, num_decimal_places=2, font_size=32 * s, color=FG)
    n1.next_to(r1l, RIGHT, buff=0.15 * s)
    n2.next_to(r2l, RIGHT, buff=0.15 * s)
    n1.add_updater(lambda m: m.set_value(tracker.get_value()).next_to(r1l, RIGHT, buff=0.15 * s))
    n2.add_updater(lambda m: m.set_value(tracker.get_value() ** 2).next_to(r2l, RIGHT, buff=0.15 * s))
    readouts = VGroup(VGroup(r1l, n1), VGroup(r2l, n2))
    g = VGroup(frame, curve, target, dot, readouts)
    g.frame, g.axes, g.curve, g.target, g.dot, g.readouts, g.tracker = (
        frame, ax, curve, target, dot, readouts, tracker)
    return g


# ── this scene's pieces ──────────────────────────────────────────────────────────
def _wave():
    """s1's wave, small: BLUE x = cos 2t on its side, time running down, DIM axis, "t" at its foot."""
    top, h, amp, x = 2.55, 2.5, 0.5, -5.2
    axis = Line([x, top + 0.1, 0], [x, top - h - 0.05, 0]).set_stroke(DIM, 2)
    tl = MathTex("t", font_size=26, color=DIM).next_to(axis, DOWN, buff=0.08)
    k = h / (2 * PI)
    curve = ParametricFunction(lambda t: np.array([x + amp * np.cos(2 * t), top - k * t, 0]),
                               t_range=[0, 2 * PI, 0.02]).set_stroke(BLUE, 4)
    tag_ = T("your guess?", size=30, color=YELLOW).next_to(curve, RIGHT, buff=0.45)
    return VGroup(axis, tl, curve), tag_


def _readouts(color, val_fn, slope_fn, pos=READ_POS):
    l1 = T("value", size=28, color=color)
    l2 = T("slope", size=28, color=color)
    l1.move_to(pos, aligned_edge=LEFT)
    l2.next_to(l1, DOWN, buff=0.2, aligned_edge=LEFT)
    n1 = DecimalNumber(val_fn(), num_decimal_places=2, font_size=32, color=FG)
    n2 = DecimalNumber(slope_fn(), num_decimal_places=2, font_size=32, color=FG)
    xr = l1.get_right()[0] + 0.25
    n1.add_updater(lambda m: m.set_value(val_fn()).move_to([xr, l1.get_center()[1], 0], aligned_edge=LEFT))
    n2.add_updater(lambda m: m.set_value(slope_fn()).move_to([xr, l2.get_center()[1], 0], aligned_edge=LEFT))
    n1.update()
    n2.update()
    return VGroup(VGroup(l1, n1), VGroup(l2, n2))


def _rider(ax, tt, f, df, color):
    def dot():
        t = tt.get_value()
        return Dot(ax.c2p(t, f(t)), radius=0.08, color=color)

    def tan():
        t = tt.get_value()
        p = ax.c2p(t, f(t))
        d = ax.c2p(t + 1, f(t) + df(t)) - ax.c2p(t, f(t))
        d = d / np.linalg.norm(d)
        return Line(p - 0.6 * d, p + 0.6 * d).set_stroke(color, 3)

    return always_redraw(tan), always_redraw(dot)


def _line(parts, colors=None, isolate_i=False):
    kw = {"substrings_to_isolate": ["i"]} if isolate_i else {}
    m = MathTex(*parts, font_size=S, color=FG, **kw)
    for k, col in (colors or {}).items():
        m[k].set_color(col)
    if isolate_i:
        m.set_color_by_tex("i", PINK)
    return m


def _move_card():
    card = kit.move_card("Try eλt: each derivative just multiplies by λ")
    ln = card.body[0]
    # raise "λt" into a superscript (glyphs: T r y e λ t : …)
    sup = VGroup(ln[4], ln[5])
    w0 = sup.width
    sup.scale(0.68, about_edge=DL).shift(0.15 * UP + 0.02 * RIGHT)
    dx = w0 - sup.width - 0.02
    for g in ln[6:]:
        g.shift(dx * LEFT)
    return card


class Guess(NarratedScene):
    def construct(self):
        self.pin = rule_pin()
        self.leg = kit.legend(ENTRIES)
        self.add(self.pin, self.leg)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c2.guess.1: e^t, e^{-t}, then the λ knob ──────────────────────────────
    def clip1(self):
        with self.say("c2.guess.1") as c:
            wave, gtag = _wave()
            self.play(FadeIn(wave[0]), FadeIn(wave[1]), Create(wave[2]), run_time=1.6)
            c.wait_until("a guess")
            self.play(*appear(gtag), run_time=1.0)
            c.wait_until("hard")
            dots = self.pin.formula[0][0]
            self.play(FlashAround(dots, color=RED, buff=0.08, run_time=2, time_width=1.5),
                      dots.animate(rate_func=there_and_back).scale(1.6), run_time=2.0)
            self.play(*disappear(wave, gtag), run_time=1.0)

            c.wait_until("so look for")
            pic = lambda_picture(1.0, lam=1.0)
            self.lp = pic
            ax = pic.axes
            self.play(*appear(pic.frame, shift=None), run_time=1.2)  # early: axis labels of the picture

            c.wait_until("grow")
            f1, d1 = np.exp, np.exp
            et = _exp_graph(ax, 1.0, GOLD)
            et_lab = MathTex(r"e^{t}", font_size=38, color=GOLD).next_to(ax.c2p(1.386, 4), RIGHT, buff=0.15)
            self.play(Create(et), run_time=1.5)
            self.play(*appear(et_lab), run_time=0.8)
            c.wait_until("its rate of change")
            tt = ValueTracker(0.0)
            tan, dot = _rider(ax, tt, f1, d1, GOLD)
            ro = _readouts(GOLD, lambda: np.exp(tt.get_value()), lambda: np.exp(tt.get_value()))
            self.play(FadeIn(dot), FadeIn(tan), *appear(ro, shift=None, lag=0.2), run_time=0.8)  # early: live readouts
            self.play(tt.animate.set_value(1.0), run_time=min(2.4, c.until("decay") - 0.2),
                      rate_func=smooth)

            c.wait_until("decay")
            self.play(*disappear(tan, dot), run_time=0.6)
            em = _exp_graph(ax, -1.0, PURPLE)
            em_lab = MathTex(r"e^{-t}", font_size=38, color=PURPLE).next_to(ax.c2p(2.5, np.exp(-2.5)), UP, buff=0.15)
            em_lab.shift(0.25 * LEFT)
            self.play(Create(em), *during(appear(em_lab), 0.5, 1.0), run_time=1.3)
            tt2 = ValueTracker(0.0)
            tan2, dot2 = _rider(ax, tt2, lambda t: np.exp(-t), lambda t: -np.exp(-t), PURPLE)
            ro2 = _readouts(PURPLE, lambda: np.exp(-tt2.get_value()), lambda: -np.exp(-tt2.get_value()), pos=READ_POS2)
            self.play(FadeIn(dot2), FadeIn(tan2), *appear(ro2, shift=None, lag=0.2), run_time=0.6)  # early: live readouts
            self.play(tt2.animate.set_value(1.0), run_time=max(0.5, min(1.4, c.until("knob") - 0.2)),
                      rate_func=smooth)

            c.wait_until("knob")
            self.play(*disappear(ro, ro2, tan2, dot2), restyle(et, outline=DIM), restyle(em, outline=DIM),
                      restyle(et_lab, fill=DIM), restyle(em_lab, fill=DIM), run_time=1.0)
            self.dimmed = VGroup(et, em, et_lab, em_lab)
            self.play(FadeIn(pic.curve), *appear(pic.label, pic.slider, pic.handle, pic.readout,
                                                 shift=None, lag=0.2), run_time=1.4)
            kit.legend_add(self, self.leg, E_LAM, run_time=1.0)
            c.wait_until("as you turn lambda")
            self.play(pic.tracker.animate.set_value(-1.0), run_time=max(1.0, c.until() - 0.3),
                      rate_func=smooth)

    # ── c2.guess.2: the move and the derivation ─────────────────────────────────
    def clip2(self):
        with self.say("c2.guess.2") as c:
            self.card = _move_card()
            self.play(*appear(self.card, shift=None), run_time=1.0)  # early: the move card is read as the sentence says it
            L0 = _cplace(_line([r"x", "=", r"e^{\lambda t}"], {0: BLUE}), 0)
            r0 = kit.tag("try an exponential", L0)
            c.wait_until("e to the lambda t")
            self.play(*appear(L0, r0, lag=0.3), run_time=1.0)  # early: the step's reason, read with the line
            L1 = _cplace(_line([r"\dot{x}", "=", r"\lambda", r"e^{\lambda t}"], {0: GREEN}), 1)
            r1 = _slabel("rate = λ × value", 1)
            c.wait_until("because")
            self.play(*appear(r1, L1, shift=None, lag=0.3), run_time=1.0)

            c.wait_until("d2")
            L2 = _cplace(_line([r"\ddot{x}", "=", r"\lambda^2", r"e^{\lambda t}"], {0: RED}), 2)
            r2 = _slabel("differentiate again", 2)
            self.play(*appear(r2, L2, shift=None, lag=0.3), run_time=1.0)

            c.wait_until("sub")
            L3 = _cplace(_line([r"\lambda^2", r"e^{\lambda t}", "=", r"-\omega^2", r"e^{\lambda t}"]), 3)
            r3 = _slabel("put it into the rule", 3)
            self.play(*appear(r3, L3, shift=None, lag=0.25), *set_alpha([L0, r0], 0.4),
                      run_time=min(1.1, c.until("cancel")))

            c.wait_until("cancel")
            self.play(FlashAround(L3[1], run_time=1.2, time_width=1.5),
                      FlashAround(L3[4], run_time=1.2, time_width=1.5),
                      *set_alpha([L1, r1], 0.4), run_time=1.2)
            L4 = _cplace(_line([r"\lambda^2", "=", r"-\omega^2"]), 4)
            cp = L3.copy()
            self.add(cp)
            self.play(cp.animate.shift(PITCH2 * DOWN), run_time=0.8)
            self.play(*during([cp[1].animate.shift(0.3 * UP).set_opacity(0),
                               cp[4].animate.shift(0.3 * UP).set_opacity(0)], 0, 0.45),
                      *during([cp[0].animate.move_to(L4[0]), cp[2].animate.move_to(L4[1]),
                               cp[3].animate.move_to(L4[2])], 0.4, 1.0), run_time=1.5)
            self.remove(*cp.get_family())
            self.add(L4)
            r4 = _slabel("never zero, so divide", 4)
            self.play(*appear(r4, shift=None), run_time=0.8)

            c.wait_until("result")
            box = SurroundingRectangle(L4, color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
            self.play(FadeIn(box), *set_alpha([L2, r2], 0.4), run_time=1.0)
            self.col = [L0, r0, L1, r1, L2, r2, L3, r3, r4]
            self.L4, self.box4 = L4, box

    # ── c2.guess.3: think stop, the parabola, λ = ±iω ───────────────────────────
    def clip3(self):
        with self.say("c2.guess.3") as c:
            tb = kit.think_box("ω = 2, so λ² = −4. Which λ?")
            ring = kit.think_ring()
            self.play(*set_alpha([self.card], 0.6), *appear(tb, ring, shift=None, lag=0.2), run_time=1.0)
            self.play(kit.drain(ring, run_time=max(1.0, c.until("real") - 0.2)))

            c.wait_until("real")
            lp = self.lp
            for m in (lp.curve, lp.handle):
                m.clear_updaters()
            lp.readout[1].clear_updaters()
            pp = parabola_picture(1.0)
            self.pp = pp
            old = [lp.frame, lp.curve, lp.label, lp.slider, lp.handle, lp.readout, self.dimmed]
            self.play(*during(disappear(tb, ring, *old), 0, 0.45), *set_alpha([self.card], 1.0),
                      *during([FadeIn(pp.frame), Create(pp.curve)], 0.5, 1.0), run_time=2.2)
            c.wait_until("any real number")
            self.play(Create(pp.target[0]), *appear(pp.target[1], shift=None), run_time=1.0)
            self.play(FadeIn(pp.dot), *appear(pp.readouts, shift=None, lag=0.2), run_time=0.6)
            self.play(pp.tracker.animate.set_value(3.0), run_time=max(1.0, c.until("imag") - 0.3),
                      rate_func=linear)

            c.wait_until("imag")
            target_y = kit.col_point(0)[1] - self.L4.get_center()[1]
            self.play(*during(disappear(*self.col), 0, 0.45),
                      *during([self.L4.animate.shift(target_y * UP), self.box4.animate.shift(target_y * UP)],
                              0.4, 1.0), run_time=1.5)
            M1 = kit.col_place(_line(["(2", "i", ")^2 = 4", "i", "^2 = -4"], isolate_i=True), 1)
            q1 = kit.step_label("i² = −1", 1)
            c.wait_until("so two")
            self.play(*appear(q1, M1, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("in general")
            M2 = kit.col_place(_line(["(", "i", r"\omega)^2 = ", "i", r"^2\omega^2 = -\omega^2"], isolate_i=True), 2)
            q2 = kit.step_label("ω in place of 2", 2)
            self.play(*appear(q2, M2, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("minus eye omega works")
            M3 = kit.col_place(_line(["(-", "i", r"\omega)^2 = -\omega^2"], isolate_i=True), 3)
            q3 = kit.step_label("the minus squares away", 3)
            self.play(*appear(q3, M3, shift=None, lag=0.3), *set_alpha([M1, q1], 0.4), run_time=1.0)

            c.wait_until("answer")
            A = kit.col_place(_line([r"\lambda = ", "i", r"\omega \;\text{ or }\; \lambda = -", "i", r"\omega"],
                                    isolate_i=True), 4)
            abox = SurroundingRectangle(A, color=YELLOW, buff=0.14).set_stroke(YELLOW, 3)
            q4 = kit.step_label("both work", 4)
            # small imaginary axis beside the parabola, PINK dots at ±2i
            cx, cy, u = -0.55, 1.3, 0.95
            im_ax = Line([cx, cy - 1.35, 0], [cx, cy + 1.35, 0]).set_stroke(DIM, 2)
            zt = Line([cx - 0.08, cy, 0], [cx + 0.08, cy, 0]).set_stroke(DIM, 2)
            iml = T("Im", size=24, color=DIM).next_to(im_ax, UP, buff=0.08)
            d_up = Dot([cx, cy + u, 0], radius=0.1, color=PINK)
            d_dn = Dot([cx, cy - u, 0], radius=0.1, color=PINK)
            l_up = MathTex(r"2i", font_size=28, color=PINK).next_to(d_up, RIGHT, buff=0.12)
            l_dn = MathTex(r"-2i", font_size=28, color=PINK).next_to(d_dn, RIGHT, buff=0.12)
            self.imag = VGroup(im_ax, zt, iml, d_up, d_dn, l_up, l_dn)
            rt = min(2.2, c.until())
            self.play(*during(appear(q4, A, shift=None, lag=0.3), 0, 0.6), *during([FadeIn(abox)], 0.5, 0.8),
                      *set_alpha([M2, q2], 0.4),
                      *during(appear(VGroup(im_ax, zt, iml), shift=None), 0.3, 0.7),
                      *during(appear(VGroup(d_up, l_up), VGroup(d_dn, l_dn), shift=None, lag=0.3), 0.6, 1.0),
                      run_time=rt)
            self.A = A

    # ── c2.guess.4: the question for s3, and the tag ────────────────────────────
    def clip4(self):
        with self.say("c2.guess.4") as c:
            e = MathTex(r"e^{", "i", r"\omega t}", font_size=44, color=GOLD)
            e[1].set_color(PINK)
            qm = T("?", size=44, color=YELLOW)
            rate = MathTex(r"\text{rate} = ", "i", r"\omega \times \text{value}\,?", font_size=32, color=FG)
            rate[1].set_color(PINK)
            ask = VGroup(e, qm, rate).arrange(RIGHT, buff=0.25)
            rate.shift(0.05 * DOWN)
            ask.move_to([kit.COL_LEFT, kit.COL_TOP - 5.4 * kit.COL_PITCH, 0], aligned_edge=LEFT)
            self.play(*appear(e, qm, lag=0.3), run_time=1.0)
            c.wait_until("but does")
            self.play(*appear(rate), run_time=1.0)

            tg = kit.tag("beyond the notes")
            tg.move_to([kit.EDGE_X, kit.COL_TOP, 0], aligned_edge=RIGHT)
            c.wait_until("tag", own_word=tg)
            self.play(*appear(tg, shift=None), run_time=1.0)
            c.wait_until("this small tag")
            self.play(FlashAround(tg, run_time=1.5, time_width=1.5, color=DIM), run_time=1.5)
