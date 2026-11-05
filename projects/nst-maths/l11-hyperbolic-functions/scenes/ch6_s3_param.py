"""Chapter 6, scene 3: cosh and sinh draw the hyperbola. Clips c6.param.1 – c6.param.5.

Opens on ch6 s2's handover shot (axes, s = 1 branches, asymptotes). Clip 1: ch5's small circle
shot top-left, the hyperbola shrinks right, a "?² − ?² = 1" question becomes the identity card.
Clip 2: the notes' working down the left (x = r cosh θ ... r = ±s, boxed). Clip 3: the hyperbola
back as hero, cosh θ ≥ 1, a TEAL point on the right branch, the left branch PURPLE with its point,
the lecturer's x = ±s cosh θ, y = s sinh θ. Clip 4: ch6 s1's glimpse pair, one GOLD θ, captions,
"why hyperbolic?" becomes a GREEN tick. Clip 5: θ is the angle on the circle, not on the hyperbola
(the ray stays under the asymptote y = x).
"""
# style: 2
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

S2 = load_scene("ch6_s2_hyperbola")
HOOK = load_scene("ch6_s1_hook")

LCX = -4.3                                   # left column centre
HC2, K2 = np.array([4.7, -1.2, 0.0]), 0.51   # hyperbola framing during the working
HC3, K3 = np.array([0.9, -0.55, 0.0]), 0.62  # hero framing for the branches
R1_Y, R2_Y, R3_Y, R4_Y = 0.0, -0.85, -1.7, -2.65
LX0 = -6.5


def W(hs, x, y):
    """Maths point -> scene point for the (possibly moved) handover picture."""
    ax = hs[0][0]
    return ax.get_center() + (ax.width / 8) * np.array([x, y, 0.0])


def circle_shot():
    """ch5 s5's last circle shot, small: BLUE circle with its point, x = r cos θ, y = r sin θ and
    cos²θ + sin²θ = 1 under it."""
    th = ValueTracker(0.6)
    ctr = np.array([LCX, 2.75, 0.0])
    axes = VGroup(Line(ctr + 1.05 * LEFT, ctr + 1.05 * RIGHT),
                  Line(ctr + 0.9 * DOWN, ctr + 0.9 * UP)).set_stroke(DIM, 2)
    circ = Circle(radius=0.72).move_to(ctr).set_stroke(BLUE, 4)
    dot = Dot(radius=0.08, color=YELLOW)
    dot.add_updater(lambda m: m.move_to(ctr + 0.72 * np.array([np.cos(th.get_value()),
                                                               np.sin(th.get_value()), 0])))
    dot.update()
    par = MathTex(r"x = r\cos\theta,\quad y = r\sin\theta", font_size=36, color=BLUE)
    par.move_to([LCX, 1.45, 0])
    ident = MathTex(r"\cos^2\theta + \sin^2\theta = 1", font_size=36)
    ident.move_to([LCX, 0.8, 0])
    g = VGroup(axes, circ, dot, par, ident)
    g.axes, g.circ, g.dot, g.par, g.ident, g.theta = axes, circ, dot, par, ident, th
    return g


def identity_card():
    """ch2 s2's card, θ version: TEAL, the minus YELLOW, YELLOW box."""
    r = MathTex(r"\cosh^2\theta", "-", r"\sinh^2\theta", "=", "1", font_size=40, color=TEAL)
    r[1].set_color(YELLOW)
    box = SurroundingRectangle(r, color=YELLOW, buff=0.22)
    g = VGroup(r, box)
    g.tex, g.box = r, box
    return g


def readout(tracker, size=40):
    lab = MathTex(r"\theta =", font_size=size, color=GOLD)
    num = DecimalNumber(tracker.get_value(), num_decimal_places=2, font_size=size, color=GOLD)
    num.add_updater(lambda m: m.set_value(tracker.get_value()))
    g = VGroup(lab, num)
    num.next_to(lab, RIGHT, buff=0.18)
    num.add_updater(lambda m: m.next_to(lab, RIGHT, buff=0.18))
    return g


class ParamHyperbola(NarratedScene):
    def construct(self):
        self.hs = S2.handover_shot()
        self.add(self.hs)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(3.2)   # the closing caption gets its full read
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def clip1(self):
        hs = self.hs
        with self.say("c6.param.1") as c:
            cs = circle_shot()
            self.cs = cs
            self.play(FadeIn(cs.axes), FadeIn(cs.circ), FadeIn(cs.dot), run_time=1.0)
            self.play(*appear(cs.par), cs.theta.animate.set_value(0.6 + TAU * 0.5),
                      run_time=min(2.0, c.until("why")))
            c.wait_until("why")
            self.play(*appear(cs.ident), cs.theta.animate.set_value(0.6 + TAU), run_time=1.6)
            self.play(FlashAround(cs.ident, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("need")
            branches = hs[1]
            self.play(VShowPassingFlash(branches.right.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      VShowPassingFlash(branches.left.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.4)
            q = MathTex("?", "^2", "-", "?", "^2", "= 1", font_size=44)
            for i in (0, 3):
                q[i].set_color(YELLOW)
            q.move_to([0.3, 0.8, 0])
            self.play(hs.animate.scale(K2 / 0.725).move_to(HC2),
                      *during(appear(q), 0.5, 1), run_time=1.8)  # early: the question the voice is posing
            c.wait_until("identity")
            card = identity_card().move_to([0.3, 0.8, 0])
            self.card = card
            self.play(*swap(q, card), run_time=1.2)
            c.wait_until("Cosh squared")
            self.play(FlashAround(card.tex[1], color=YELLOW, time_width=1.5), run_time=1.5)

    # ---------------------------------------------------------------- clip 2
    def clip2(self):
        with self.say("c6.param.2") as c:
            cs, card = self.cs, self.card
            R1 = MathTex(r"x = r\cosh\theta,\quad y = r\sinh\theta", font_size=44)
            R1.move_to([LX0, R1_Y, 0], aligned_edge=LEFT)
            self.play(*set_alpha([cs], 0.4), *appear(R1), run_time=1.2)
            c.wait_until("square")
            R2 = MathTex(r"x^2 - y^2", "=", "r^2", r"\cosh^2\theta", "-", "r^2", r"\sinh^2\theta",
                         font_size=44)
            R2.move_to([LX0, R2_Y, 0], aligned_edge=LEFT)
            self.play(*appear(R2), run_time=1.2)
            c.wait_until("factor")
            R3 = MathTex("=", "r^2", r"(\cosh^2\theta - \sinh^2\theta)", font_size=44)
            R3.move_to([0, R3_Y, 0])
            R3.shift((R2[1].get_x() - R3[0].get_x()) * RIGHT)
            self.play(*fly(R2[2], R3[1]), *appear(R3[0], R3[2]), run_time=1.5)
            c.wait_until("one")
            self.play(FlashAround(R3[2], color=YELLOW, time_width=1.5),
                      FlashAround(card.tex[4], color=YELLOW, time_width=1.5), run_time=1.4)
            one = MathTex(r"\cdot", "1", font_size=44, color=TEAL).next_to(R3[1], RIGHT, buff=0.15)
            one.align_to(R3[0], DOWN)
            one[0].set_color(FG)
            c.wait_until("which is one")
            # the bracket collapses in place into the 1 (no long flight across the empty frame)
            self.play(*during([R3[2].animate.scale(0.15, about_point=one[1].get_center()).set_opacity(0)], 0, 0.5),
                      FlashAround(card.tex[4], color=YELLOW, time_width=1.5),
                      *during(appear(one, shift=None, lag=0.2), 0.5, 1), run_time=1.6)
            self.remove(*R3.get_family(), *one.get_family())
            self.R3 = VGroup(R3[0], R3[1], one)
            self.add(self.R3)
            c.wait_until("result")
            R4 = MathTex(r"x^2 - y^2", "=", "r^2", font_size=44)
            R4.move_to([LX0, R4_Y, 0], aligned_edge=LEFT)
            self.play(*appear(R4), run_time=1.2)
            c.wait_until("match")
            R5 = MathTex("r^2", "=", "s^2", font_size=44)
            R5.move_to([-2.3, R4_Y, 0])
            self.play(*appear(R5), run_time=1.0)
            c.wait_until("must be")
            imp = MathTex(r"\Rightarrow", font_size=44, color=DIM).next_to(R5, RIGHT, buff=0.35)
            R5b = MathTex("r", "=", r"\pm", "s", font_size=48)
            R5b[2].set_color(YELLOW)
            R5b.next_to(imp, RIGHT, buff=0.45)
            box = SurroundingRectangle(R5b, color=YELLOW, buff=0.22)
            self.play(*appear(imp, R5b, lag=0.4), run_time=1.2)
            self.play(GrowFromCenter(box), run_time=0.8)
            self.rbox = VGroup(R5b, box)
            self.remove(R5b, box)
            self.add(self.rbox)

    # ---------------------------------------------------------------- clip 3
    def clip3(self):
        hs = self.hs
        with self.say("c6.param.3") as c:
            sweep_clear(self, hs.animate.scale(K3 / K2).move_to(HC3),
                        self.rbox.animate.move_to([LCX, 2.15, 0]), keep=[hs, self.rbox])
            note = T("Each sign gives one branch.", 30).move_to([LCX + 0.15, 1.25, 0])
            self.play(*appear(note), run_time=1.0)
            c.wait_until("ge")
            tag = MathTex(r"\cosh\theta \ge 1", font_size=44, color=GREEN).move_to([LCX, 0.2, 0])
            self.play(*appear(tag), FlashAround(self.rbox[0][2], color=YELLOW, time_width=1.5),
                      run_time=1.5)

            c.wait_until("right")
            th = ValueTracker(-2.0)
            self.th = th
            tdot = Dot(radius=0.12, color=TEAL).set_stroke(FG, 2)
            tdot.add_updater(lambda m: m.move_to(W(hs, np.cosh(th.get_value()), np.sinh(th.get_value()))))
            tdot.update()
            ro = readout(th).move_to([5.3, -2.2, 0])
            rlab = MathTex(r"x = s\cosh\theta", font_size=40, color=TEAL).move_to([5.3, 0.9, 0])
            self.play(FadeIn(tdot, scale=0.5), *appear(ro, rlab, lag=0.3), run_time=1.0)
            self.play(th.animate.set_value(2.0), run_time=min(3.5, c.until("left") - 0.1),
                      rate_func=linear)

            c.wait_until("left")
            pdot = Dot(radius=0.12, color=PURPLE).set_stroke(FG, 2)
            pdot.add_updater(lambda m: m.move_to(W(hs, -np.cosh(th.get_value()), np.sinh(th.get_value()))))
            pdot.update()
            llab = MathTex(r"x = -s\cosh\theta", font_size=40, color=PURPLE).move_to([LCX, -1.2, 0])
            self.play(*recolor([hs[1].left], PURPLE), FadeIn(pdot, scale=0.5), *appear(llab),
                      run_time=1.0)
            self.play(th.animate.set_value(-2.0), run_time=min(2.6, c.until("ynosign") - 0.1),
                      rate_func=linear)

            c.wait_until("ynosign")
            pm = MathTex(r"x = ", r"\pm", r"s\cosh\theta,\quad y = s\sinh\theta", font_size=48)
            pm[1].set_color(YELLOW)
            pm.move_to([0.9, 3.35, 0])
            self.play(*appear(pm), run_time=1.2)
            nopm = T("no ± on y", 30, color=DIM, t2s={"y": ITALIC})
            nopm.next_to(pm[2], DOWN, buff=0.25).align_to(pm[2], RIGHT)
            self.play(*appear(nopm), run_time=1.0)  # early: the voice's own aside, "no plus or minus"
            c.wait_until("Shine theta takes every real value")
            self.play(th.animate.set_value(2.0), run_time=min(5.5, c.until() - 0.2), rate_func=linear)
            self.dots = (tdot, pdot)

    # ---------------------------------------------------------------- clip 4
    def clip4(self):
        with self.say("c6.param.4") as c:
            for d in self.dots:
                d.clear_updaters()
            pair = HOOK.glimpse_pair()
            o = pair.get_center()
            pair.scale(1.15, about_point=o).shift((0.35 - o[1]) * UP)
            why = pair.why.scale(1.15, about_point=o).shift((0.35 - o[1]) * UP)
            self.pair = pair
            if why.get_right()[0] > 6.5:
                why.shift((6.5 - why.get_right()[0]) * RIGHT)
            if why.get_right()[0] > 6.5:
                why.shift((6.5 - why.get_right()[0]) * RIGHT)
            ro = readout(pair.theta).move_to([0, 3.35, 0])
            self.ro = ro
            sweep_clear(self, FadeIn(pair), *appear(ro), run_time=1.6)
            c.wait_until("circ")
            th = pair.theta
            cc, rr = pair.circle.get_center(), pair.circle.width / 2
            ho = pair.h_origin.get_center()
            # a YELLOW trail that grows behind each running point (in step with it), then fades
            t0 = th.get_value()
            ctrail = always_redraw(lambda: Arc(radius=rr, start_angle=t0, angle=th.get_value() - t0 + 1e-3,
                                               arc_center=cc).set_stroke(YELLOW, 7))
            self.add(ctrail)
            self.play(th.animate.set_value(1.2), run_time=min(2.5, c.until("hyp") - 0.2))
            ctrail.clear_updaters()
            self.play(FadeOut(ctrail), run_time=0.6)
            c.wait_until("hyp")
            t1 = th.get_value()

            def htrail_pts():
                ts = np.linspace(t1, th.get_value() - 1e-3, 40)
                return [ho + rr * np.array([np.cosh(t), np.sinh(t), 0.0]) for t in ts]
            htrail = always_redraw(lambda: VMobject().set_points_smoothly(htrail_pts()).set_stroke(YELLOW, 7))
            self.add(htrail)
            self.play(th.animate.set_value(-1.2), run_time=min(3.0, c.until("answer") - 0.8))
            htrail.clear_updaters()
            self.play(FadeOut(htrail), run_time=0.6)
            c.wait_until("answer")
            self.play(*appear(why), pair.theta.animate.set_value(0.7), run_time=1.4)  # early: part one's question, brought back as it is named
            c.wait_until("Circular functions")
            cap_c = T("circular functions draw circles", 30, color=BLUE)
            cap_c.move_to([-6.5, -3.1, 0], aligned_edge=LEFT)
            cap_h = T("hyperbolic functions draw hyperbolas", 30, color=TEAL)
            cap_h.move_to([6.5, -3.1, 0], aligned_edge=RIGHT)
            self.play(*appear(cap_c), run_time=1.0)
            c.wait_until("hyperbolic functions")
            self.play(*appear(cap_h), run_time=1.0)
            c.wait_until("That's where the name comes from")
            tick = check_mark(GREEN).scale(1.4).move_to(why)
            self.play(*swap(why, tick), run_time=1.2)
            self.caps, self.tick = (cap_c, cap_h), tick

    # ---------------------------------------------------------------- clip 5
    def clip5(self):
        pair = self.pair
        th = pair.theta
        with self.say("c6.param.5") as c:
            self.play(*disappear(self.tick), th.animate.set_value(0.8), run_time=1.0)
            c.wait_until("On the circle")
            cc = pair.circle.get_center()
            grow = ValueTracker(0.001)   # ray and arc grow with this (no Create on redrawn shapes)
            rad = always_redraw(lambda: Line(cc, cc + grow.get_value() * (pair.cdot.get_center() - cc))
                                .set_stroke(FG, 3))
            arc = always_redraw(lambda: Arc(radius=0.38, start_angle=0, angle=grow.get_value() * th.get_value(),
                                            arc_center=cc).set_stroke(GOLD, 4))
            tlab = always_redraw(lambda: MathTex(r"\theta", font_size=36, color=GOLD).move_to(
                cc + 0.62 * np.array([np.cos(th.get_value() / 2), np.sin(th.get_value() / 2), 0])))
            self.add(rad, arc)
            self.play(grow.animate.set_value(1.0), run_time=1.0)
            self.play(*appear(tlab), run_time=0.8)

            c.wait_until("param")
            ho = pair.h_origin.get_center()

            def ang():
                p = pair.hdot.get_center() - ho
                return float(np.arctan2(p[1], p[0]))
            hg = ValueTracker(0.001)
            ray = always_redraw(lambda: Line(ho, ho + hg.get_value() * (pair.hdot.get_center() - ho))
                                .set_stroke(FG, 3, opacity=0.45))
            harc = always_redraw(lambda: Arc(radius=0.7, start_angle=0, angle=hg.get_value() * ang(),
                                             arc_center=ho).set_stroke(RED, 4))
            notth = MathTex(r"\text{not}\ \theta", font_size=36, color=RED).move_to(ho + np.array([0.6, -0.38, 0]))
            self.add(ray, harc)
            self.play(hg.animate.set_value(1.0), run_time=1.0)
            self.play(*appear(notth), run_time=0.8)

            c.wait_until("wedge")
            u = pair.circle.width / 2
            asym = DashedLine(ho, ho + 1.75 * u * np.array([1, 1, 0]), dash_length=0.12,
                              dashed_ratio=0.55).set_stroke(FG, 2.5, opacity=0.55)
            self.play(Create(asym), th.animate.set_value(1.25), run_time=2.0)
            lt = MathTex(r"< 45^\circ", font_size=36, color=YELLOW)
            lt.next_to(notth, DOWN, buff=0.18).align_to(notth, LEFT)   # by the arc, under "not θ"
            self.play(*appear(lt), run_time=1.0)
            cap = MathTex(r"\theta\ \text{is a parameter, not an angle}", font_size=44,
                          color=YELLOW).move_to([0, -3.1, 0])
            self.play(*during(disappear(*self.caps), 0, 0.45), *during(appear(cap), 0.5, 1),
                      run_time=1.6)
