"""Chapter 2, scene 9: recap of the three moves, the facts, next time. Clips c2.recap.1 – c2.recap.2.

Reused drawings (never redrawn): s2's lambda_picture / parabola_picture (their small text dropped,
too small at this scale), s4's fan, s3's arrow kit (plane, turning_arrow, shadow, spring_on_axis),
the mirror arrow carried to the GOLD tip (as s6), ch1 s8's recap_card look.
Reversed join: the last frame is exactly load_scene("ch3_s1_hook").opening_card() (chapter 3's
first frame), reached by a cross-fade during the end hold.
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
ak = load_scene("ch2_s3_velocity")
g2 = load_scene("ch2_s2_guess")
a4 = load_scene("ch2_s4_accel")
sh5 = load_scene("ch2_s5_shadow")
r8 = load_scene("ch1_s8_recap")
ch3 = load_scene("ch3_s1_hook")

OMEGA = ak.OMEGA
HEAD_Y = 3.36
REC_TOP = 3.0
PIC_BOTTOM = -1.78
SHORT_Y = -2.32
SHORT_SIZE = 24
FACTS_Y = -3.3
LAM_H, PAR_H = 4.16, 3.8          # heights (per unit scale) of s2's two pictures, small text dropped
S6 = 0.58                          # M6 plane scale

M4_TEXT = "Try eλt: each derivative just multiplies by λ"

# {next}
F81_Y = 1.85
ONE_O = np.array([-2.6, -1.55, 0])
ONE_S = 0.8
ONE_T = 40 * DEGREES / OMEGA
Q_X = 0.4


def m4_card():
    """s2's move card text in the recap-card look, with s2's superscript fix for λt."""
    card = r8.recap_card(M4_TEXT)
    ln = card.body[0]
    sup = VGroup(ln[4], ln[5])
    w0 = sup.width
    sup.scale(0.68, about_edge=DL).shift(0.12 * UP + 0.02 * RIGHT)
    dx = w0 - sup.width - 0.02
    for g in ln[6:]:
        g.shift(dx * LEFT)
    return card


def lambda_small(cx, top, s):
    g = g2.lambda_picture(s, 1.0)
    g.frame.remove(*g.frame.submobjects[2:])          # ticks, "t", "value"
    g.remove(g.label, g.readout)
    g.slider.remove(g.slider[2])                      # slider numbers
    o = g.axes.c2p(0, 0)
    off = np.array([cx - (o[0] + 3.05 * s), top - (o[1] + 3.1 * s), 0])
    g.shift(off)
    g.handle.add_updater(lambda m: m.shift(off))      # its redraw uses build-time coordinates
    lab = MathTex(r"e^{\lambda t}", font_size=26).move_to(g.axes.c2p(2.5, 3.6), aligned_edge=UR)
    lam = MathTex(r"\lambda", font_size=26).next_to(g.slider[0], LEFT, buff=0.14)
    out = VGroup(g, lab, lam)
    out.pic = g
    return out


def parabola_small(cx, top, s):
    g = g2.parabola_picture(s)
    g.frame.remove(*g.frame.submobjects[1:])          # ticks, λ, λ² labels
    g.target.remove(g.target[1])                      # "−ω² = −4"
    g.remove(g.readouts)
    ax = g.axes
    off = np.array([cx - 0.3 - ax.c2p(0, 0)[0], top - ax.c2p(0, 9)[1], 0])
    g.shift(off)
    lab = MathTex(r"-\omega^2", font_size=26, color=RED).next_to(g.target[0], RIGHT, buff=0.1)
    out = VGroup(g, lab)
    out.pic = g
    return out


def short_line(*rows):
    ms = []
    for r in rows:
        parts, colors = r
        m = MathTex(*parts, font_size=SHORT_SIZE)
        for i, col in colors.items():
            m[i].set_color(col)
        ms.append(m)
    return VGroup(*ms).arrange(DOWN, buff=0.14)


def short_m4():
    return short_line(([r"\text{try } e^{\lambda t}:\ \lambda^2 =", r"-\omega^2", ","], {1: RED}),
                      ([r"\text{so } \lambda = \pm", "i", r"\omega"], {1: PINK}))


def short_m5():
    return short_line(([r"\tfrac{d}{dt}:\ \text{a quarter turn ahead,}"], {}),
                      ([r"\times\,\omega;\ \text{twice: straight back}"], {}))


def short_m6():
    return short_line(([r"\text{take the shadow:}"], {}),
                      ([r"\text{a real swing is a mirror pair}"], {}))


def facts_line():
    eu = MathTex(r"\text{Euler: }\ e^{i\omega t} = \cos\omega t + i\sin\omega t", font_size=30)
    dot = MathTex(r"\cdot", font_size=30)
    per = MathTex(r"\text{the period } T = 2\pi/\omega", font_size=30)
    row = VGroup(eu, dot, per).arrange(RIGHT, buff=0.35)
    row.move_to([0, FACTS_Y, 0]).set_color(DIM)
    return eu, dot, per


class Recap(NarratedScene):
    def construct(self):
        self.t5 = ak.clock(ValueTracker(0.0))
        self.t6 = ak.clock(ValueTracker(sh5.T_HAND))
        self.add(self.t5, self.t6)
        self.clip1()
        self.clip2()
        self.end_hold()

    # ── {recap}: three moves, each picture moving ──────────────────────────────
    def clip1(self):
        t5, t6 = self.t5, self.t6
        head = T("Recap", size=28, color=DIM).move_to([0, HEAD_Y, 0])
        cards = [m4_card(), r8.recap_card(ak.MOVE_M5), r8.recap_card(sh5.MOVE_M6)]
        row = VGroup(*cards).arrange(RIGHT, buff=0.35, aligned_edge=UP)
        if row.width > 13.2:
            row.scale_to_fit_width(13.2)
        row.move_to([0, REC_TOP, 0], aligned_edge=UP)
        xs = [cd.get_center()[0] for cd in cards]
        pic_top = min(cd.get_bottom()[1] for cd in cards) - 0.25
        pic_cy = (pic_top + PIC_BOTTOM) / 2
        lines = [short_m4(), short_m5(), short_m6()]
        for ln, x in zip(lines, xs):
            ln.move_to([x, SHORT_Y, 0])

        # M4: s2's two pictures, stacked
        s4 = min(0.48, (pic_top - PIC_BOTTOM - 0.3) / (LAM_H + PAR_H))
        lam = lambda_small(xs[0], pic_top, s4)
        par = parabola_small(xs[0], pic_top - LAM_H * s4 - 0.3, s4)

        # M5: s4's fan
        u5 = min((pic_top - PIC_BOTTOM) / 2 - 0.05, 1.75) / 4.25
        f_s = u5 / ak.PLANE_R
        o5 = np.array([xs[1], pic_cy, 0])
        plane5 = ak.plane(f_s, o5, re_units=4, im_units=4, labels=False)
        gl5 = ValueTracker(0.0)
        fan5 = a4.fan(t5, f_s, o5, glow=gl5, width=4)

        # M6: s5's arrow, shadow and block; s6's mirror pair tip to tail
        o6 = np.array([xs[2] - 0.15, pic_cy, 0])
        op_sp, op_pu = ValueTracker(1.0), ValueTracker(0.0)
        plane6 = ak.plane(S6, o6)
        gold6 = ak.turning_arrow(t6, scale=S6, origin=o6, width=5)
        sh6 = sh5.faded(ak.shadow(t6, scale=S6, origin=o6), op_sp)
        sp6 = sh5.faded(ak.spring_on_axis(t6, scale=S6, origin=o6), op_sp)

        def tip6():
            return ak.plane_point(ak.phasor(t6.get_value()), S6, o6)

        purple6 = sh5.live(lambda: ak.turning_arrow(t6.get_value(), omega=-OMEGA, color=PURPLE,
                                                    scale=S6, origin=tip6(), width=5), op_pu)
        sum6 = sh5.live(lambda: Dot(ak.plane_point(2 * np.cos(OMEGA * t6.get_value()), S6, o6),
                                    radius=0.1, color=BLUE).set_z_index(ak.Z_MARK), op_pu)

        eu, fdot, per = facts_line()

        with self.say("c2.recap.1") as c:
            self.play(*appear(head, shift=None), run_time=1.0)  # early: the recap heading
            c.wait_until("m4")
            self.play(*appear(cards[0], lam, par, shift=None, lag=0.2), run_time=1.4)  # early: the move card names the move as it is said
            c.wait_until("try e to the lambda")
            tr = lam.pic.tracker
            self.play(tr.animate.set_value(-1.0), run_time=2.4)
            self.play(tr.animate.set_value(1.0), run_time=min(2.4, c.until("rule becomes") - 0.1))
            c.wait_until("rule becomes")
            self.play(par.pic.tracker.animate.set_value(0.0), run_time=min(2.2, c.until("minus omega squared")),
                      rate_func=smooth)
            c.wait_until("minus omega squared")
            self.play(FlashAround(par.pic.target[0], color=RED, time_width=1.5),
                      *appear(lines[0], shift=None, lag=0.3), run_time=min(1.5, c.until("m5") - 0.1))

            c.wait_until("m5")
            self.play(*appear(cards[1], plane5, fan5, shift=None, lag=0.2), run_time=1.2)  # early: the move card names the move as it is said
            ak.run(t5, True)
            c.wait_until("quarter turn")
            self.play(gl5.animate.set_value(1.0), run_time=0.8)
            self.play(gl5.animate.set_value(0.0), run_time=0.8)
            c.wait_until("twice points")
            self.play(*appear(lines[1], shift=None, lag=0.3), run_time=1.2)

            c.wait_until("m6")
            ak.run(t5, False)
            self.play(*appear(cards[2], plane6, sp6, gold6, sh6, shift=None, lag=0.12),  # early: the move card names the move as it is said
                      t5.animate.set_value(t5.get_value() + 0.3), run_time=1.3)
            self.add(purple6, sum6)
            ak.run(t6, True)
            c.wait_until("take the shadow")
            self.play(*appear(lines[2][0], shift=None), run_time=1.0)
            c.wait_until("mirror pair")
            self.play(op_sp.animate.set_value(0.0), op_pu.animate.set_value(1.0),
                      *during(appear(lines[2][1], shift=None), 0.4, 1.0), run_time=1.5)

            c.wait_until("oiler's formula")
            self.play(*appear(eu, shift=None), run_time=1.0)
            c.wait_until("the period")
            self.play(*appear(fdot, per, shift=None, lag=0.2), run_time=1.0)
        self.facts = (eu, fdot, per)

    # ── {next}: (81), its d/dt swaps, one number? ──────────────────────────────
    def clip2(self):
        f81 = MathTex("x", "=", "a", r"\cos\omega t", "+", "b", r"\sin\omega t", font_size=56)
        for i in (0, 2, 3, 5, 6):
            f81[i].set_color(BLUE)
        f81.move_to([0, F81_Y, 0])
        tag81 = kit.tag("(81) · notes p. 108", item=f81, direction=RIGHT, buff=0.35)
        ca, sa = f81[3], f81[6]
        arc_a = CurvedArrow(ca.get_top() + 0.12 * UP, sa.get_top() + 0.12 * UP, angle=-PI / 3,
                            color=DIM, stroke_width=3, tip_length=0.2)
        arc_b = CurvedArrow(sa.get_bottom() + 0.12 * DOWN, ca.get_bottom() + 0.12 * DOWN, angle=-PI / 3,
                            color=DIM, stroke_width=3, tip_length=0.2)
        lab_a = MathTex(r"d/dt", font_size=32, color=DIM).next_to(arc_a, UP, buff=0.1)
        lab_b = MathTex(r"d/dt", font_size=32, color=DIM).next_to(arc_b, DOWN, buff=0.1)

        pl = ak.plane(ONE_S, ONE_O, re_units=1.5, im_units=1.0, labels=False)
        gold = ak.turning_arrow(ONE_T, scale=ONE_S, origin=ONE_O)
        q = T("one number?", size=40, color=YELLOW).move_to([Q_X, -1.15, 0], aligned_edge=LEFT)
        self.nxt = T("Next: the complex amplitude", size=30, color=DIM).move_to([Q_X, -2.05, 0], aligned_edge=LEFT)

        with self.say("c2.recap.2") as c:
            ak.run(self.t6, False)
            keep = (self.t5, self.t6)
            gone = [m for m in list(self.mobjects) if m not in keep and m not in self.facts]
            for m in gone:
                for sm in m.get_family():
                    sm.clear_updaters()
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during(appear(f81, shift=None), 0.5, 1.0), run_time=1.8)
            self.play(*appear(tag81, shift=None), run_time=0.8)
            c.wait_until("two numbers")
            self.play(*flash([f81[2], f81[5]], time_width=1.5), run_time=1.5)
            c.wait_until("two functions")
            self.play(*flash([ca, sa], time_width=1.5), run_time=1.5)
            c.wait_until("every derivative")
            self.play(Create(arc_a), *during(appear(lab_a, shift=None), 0.4, 1.0), run_time=1.2)
            self.play(Create(arc_b), *during(appear(lab_b, shift=None), 0.4, 1.0), run_time=1.2)

            c.wait_until("one")
            self.play(*appear(pl, shift=None), GrowArrow(gold), run_time=1.2)
            c.wait_until(own_word=q)
            self.play(*appear(q), run_time=1.0)
        self.end_parts = [f81, tag81, arc_a, arc_b, lab_a, lab_b, pl, gold, q]

    # ── end card, then the cross-fade into chapter 3's first frame ─────────────
    def end_hold(self):
        self.play(*appear(self.nxt, shift=None), run_time=1.0)  # early: the end card's next-part line, after the last word
        self.wait(6.4)
        card = ch3.opening_card()
        gone = [m for m in list(self.mobjects) if m not in (self.t5, self.t6)]
        self.play(*during(disappear(*gone), 0, 0.42),
                  *during([FadeIn(m) for m in card.submobjects], 0.45, 1.0),
                  run_time=2.6)
        self.remove(*[m for m in list(self.mobjects) if m not in (self.t5, self.t6)])
        self.add(ch3.opening_card())
        self.wait(1.2)
