"""Chapter 2, scene 3: why n must be an integer. Clips c2.int.1 – c2.int.4."""
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

# The Argand plane of clips 2-3: centre, unit length, half-extent of the axes.
PC = np.array([-3.0, -0.45, 0.0])
U = 2.45
EXT = 3.0
COL_X = 3.85          # centre of the right-hand label column


def argand_plane(center=PC, unit=U, extent=EXT):
    """PLAN.md's running Argand plane: faint grid, Re/Im axes, DIM unit circle."""
    step = unit / 2
    n = int(extent // step)
    grid = VGroup()
    for k in range(-n, n + 1):
        if k == 0:
            continue
        grid.add(Line(center + [k * step, -extent, 0], center + [k * step, extent, 0]))
        grid.add(Line(center + [-extent, k * step, 0], center + [extent, k * step, 0]))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(center + [-extent, 0, 0], center + [extent, 0, 0], **ax_kw).set_opacity(0.7)
    y_ax = Arrow(center + [0, -extent, 0], center + [0, extent, 0], **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=unit, color=DIM, stroke_width=2.5).move_to(center)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle = grid, VGroup(x_ax, y_ax), circle
    return g


def ray(deg, color, center=PC, unit=U, r=1.0):
    a = np.deg2rad(deg)
    end = center + unit * r * np.array([np.cos(a), np.sin(a), 0])
    return Arrow(center, end, buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.14,
                 tip_length=0.3, color=color)


def tip(deg, center=PC, unit=U):
    a = np.deg2rad(deg)
    return center + unit * np.array([np.cos(a), np.sin(a), 0])


def half_angle_arrows(center=PC, unit=U):
    """The two square roots of e^{i100°}: GOLD arrow at 50°, TEAL at 230°, the TEAL half-turn arc
    between their tips, and the RED "two values" tag (placed below-right of the plane; move it).
    Returned VGroup has .first .second .arc .tag."""
    first = ray(50, GOLD, center, unit)
    second = ray(230, TEAL, center, unit)
    arc = Arc(radius=unit * 1.07, start_angle=np.deg2rad(50), angle=PI, arc_center=center,
              color=TEAL, stroke_width=5)
    tag = T("two values", 32, color=RED).next_to(center + [unit, -unit, 0], RIGHT, buff=0.4)
    g = VGroup(first, second, arc, tag)
    g.first, g.second, g.arc, g.tag = first, second, arc, tag
    return g


def sweep_ray(arrow, start_deg, sweep_deg, color, center=PC, unit=U):
    """Turn `arrow` from start_deg through sweep_deg (can be several full turns)."""
    def upd(m, alpha):
        m.become(ray(start_deg + alpha * sweep_deg, color, center, unit))
    return UpdateFromAlphaFunc(arrow, upd)


def spiral(start_deg, turns, r0, r1, center=PC, color=TEAL):
    a0 = np.deg2rad(start_deg)
    span = turns * TAU

    def f(t):
        r = r0 + (r1 - r0) * t
        a = a0 + span * t
        return center + r * np.array([np.cos(a), np.sin(a), 0])
    return ParametricFunction(f, t_range=[0, 1, 1 / (120 * max(turns, 1))], color=color, stroke_width=4)


class WhyInteger(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.int.1
    def clip1(self):
        with self.say("c2.int.1") as c:
            l1 = T("Note that n must be an integer here:", 40)
            l2 = T("for other n the left-hand side is multivalued.", 40)
            note = VGroup(l1, l2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(UP * 2.2)
            self.note = note
            self.play(*appear(l1, l2, lag=0.5), run_time=1.6)  # early: the notes' sentence shown whole, then read
            c.wait_until("integer")

            integer = select(l1, "n must be an integer")[0]
            self.play(*recolor(integer, YELLOW), FlashUnder(integer, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("hand")

            hand = MathTex(r"(e^{i\theta})^n = e^{in\theta}, \quad n \in \mathbb{Z}", font_size=72, color=RED)
            hand.move_to(DOWN * 0.55)
            self.hand = hand
            self.play(*appear(hand), run_time=1.4)
            c.wait_until("lhs")

            lhs = hand[0][0:6]
            phrase = select(l2, "the left-hand side is multivalued")[0]
            ul_lhs = underline(lhs, YELLOW, buff=0.12)
            ul_phr = underline(phrase, YELLOW, buff=0.1)
            join = Arrow(ul_phr.get_left() + 0.5 * RIGHT + 0.05 * DOWN, lhs.get_top() + 0.15 * UP + 0.3 * RIGHT,
                         buff=0.08, stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.2)
            self.play(GrowFromEdge(ul_lhs, LEFT), run_time=0.9)
            self.play(GrowFromEdge(ul_phr, LEFT), GrowArrow(join), run_time=1.3)
            self.ul = VGroup(ul_lhs, ul_phr, join)
            c.wait_until("why")

            why = MathTex(r"n = \tfrac{1}{2}\ ?", font_size=64, color=YELLOW).move_to(DOWN * 2.45)
            self.why = why
            self.play(*appear(why), run_time=1.2)

    # ------------------------------------------------------------------ c2.int.2
    def clip2(self):
        hand, why = self.hand, self.why
        with self.say("c2.int.2") as c:
            plane = argand_plane()
            self.plane = plane
            hand.generate_target()
            why.generate_target()
            hand.target.scale(0.6)
            why.target.scale(0.6)
            VGroup(hand.target, why.target).arrange(RIGHT, buff=1.2).move_to(UP * 3.42)
            self.play(*during(disappear(self.note, self.ul), 0, 0.4),
                      *during([MoveToTarget(hand), MoveToTarget(why)], 0.35, 0.8),
                      *during(FadeIn(plane), 0.55, 1.0), run_time=1.7)

            a100 = ray(100, GOLD)
            th_arc = Arc(radius=0.75, start_angle=0, angle=np.deg2rad(100), arc_center=PC, color=YELLOW, stroke_width=4)
            th = MathTex(r"\theta", font_size=40, color=YELLOW).move_to(PC + 1.05 * np.array([np.cos(0.87), np.sin(0.87), 0]))
            self.play(GrowArrow(a100), Create(th_arc), run_time=min(1.0, c.until("same")))
            self.play(*appear(th), run_time=0.6)
            c.wait_until("same")

            # one full turn: a TEAL copy sweeps 360° and lands on the arrow
            sweeper = ray(100, TEAL)
            full = Arc(radius=0.48, start_angle=np.deg2rad(100), angle=TAU, arc_center=PC, color=TEAL, stroke_width=4)
            self.add(sweeper)
            self.play(sweep_ray(sweeper, 100, 360, TEAL), Create(full), run_time=2.6, rate_func=smooth)
            self.remove(sweeper)
            rowA = MathTex(r"e^{i\theta} = e^{i(\theta + 2\pi)}", font_size=52)
            rowA[0][8:11].set_color(TEAL)
            rowA.move_to([COL_X, 2.1, 0])
            self.rowA = rowA
            self.play(*appear(rowA), FlashAround(a100, color=TEAL, run_time=1.2), run_time=1.2)
            c.wait_until("half")

            div = MathTex(r"\div\, 2", font_size=56, color=YELLOW).move_to([COL_X, 1.15, 0])
            self.play(*appear(div), *set_alpha([a100, th_arc, full], 0.35), FadeOut(th), run_time=1.2)
            self.play(*flash(rowA[0][1:2] , YELLOW), *flash(rowA[0][6:11], YELLOW), run_time=1.2)
            c.wait_until("first")

            a50 = ray(50, GOLD)
            labC = MathTex(r"e^{i\theta/2}", font_size=52, color=GOLD).move_to([COL_X, 0.15, 0])
            self.play(GrowArrow(a50), run_time=1.3)
            self.play(*appear(labC), run_time=1.0)
            c.wait_until("second")

            a230 = ray(230, TEAL)
            hal = half_angle_arrows()
            labD1 = MathTex(r"e^{i(\theta/2 + \pi)}", font_size=52, color=TEAL)
            labD2 = MathTex(r"= -e^{i\theta/2}", font_size=52, color=TEAL)
            VGroup(labD1, labD2).arrange(RIGHT, buff=0.2).move_to([COL_X, -0.95, 0])
            self.play(*appear(labD1), run_time=1.0)
            self.play(Create(hal.arc), run_time=1.6)
            self.play(GrowArrow(a230), run_time=1.0)
            c.wait_until("opposite point")
            self.play(*appear(labD2), run_time=1.0)
            self.a100, self.th_arc, self.full, self.div = a100, th_arc, full, div
            self.a50, self.a230, self.half_arc = a50, a230, hal.arc
            self.labs = [labC, labD1, labD2]
            self.hal = hal

    # ------------------------------------------------------------------ c2.int.3
    def clip3(self):
        a50, a230, a100 = self.a50, self.a230, self.a100
        with self.say("c2.int.3") as c:
            d1 = Dot(tip(50), radius=0.11, color=GOLD)
            d2 = Dot(tip(230), radius=0.11, color=TEAL)
            self.play(FadeIn(d1, scale=0.5), FadeIn(d2, scale=0.5),
                      Flash(d1, color=GOLD, flash_radius=0.3), Flash(d2, color=TEAL, flash_radius=0.3), run_time=1.0)
            # each angle doubles back onto the 100° arrow
            c1, c2 = ray(50, GOLD), ray(230, TEAL)
            self.add(c1, c2)
            self.play(sweep_ray(c1, 50, 50, GOLD), sweep_ray(c2, 230, 230, TEAL), *set_alpha([a100], 1),
                      run_time=min(1.8, c.until("notone") - 0.6), rate_func=smooth)
            self.play(FadeOut(c1), FadeOut(c2), FlashAround(a100, color=YELLOW), run_time=0.6)
            c.wait_until("notone")

            labE = MathTex(r"(e^{i\theta})^{1/2}", font_size=52).move_to([COL_X - 0.9, -2.3, 0])
            tag = self.hal.tag
            tag.next_to(labE, RIGHT, buff=0.45)
            self.play(*appear(labE), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("whole")

            # the halves, the n = 1/2 question and its two-valued answer all clear before n = 3 comes in
            gone = [a50, a230, self.half_arc, d1, d2, self.div, *self.labs, self.th_arc, self.full,
                    labE, tag, self.why]
            self.play(*disappear(*gone), *set_alpha([a100], 0.35), run_time=0.9)
            n3 = MathTex(r"n = 3", font_size=52, color=YELLOW).move_to([COL_X, 1.15, 0])
            g3 = MathTex(r"3\theta", font_size=52, color=GOLD).move_to([COL_X, 0.15, 0])
            t3 = MathTex(r"3(\theta + 2\pi) = 3\theta + 6\pi", font_size=52, color=TEAL).move_to([COL_X, -0.95, 0])
            a300 = ray(300, GOLD)
            self.play(*appear(n3, g3, t3, lag=0.3), GrowArrow(a300), run_time=1.3)
            winder = ray(300, TEAL)
            sp = spiral(300, 3, 0.35, 1.25)
            self.add(winder)
            self.play(sweep_ray(winder, 300, 1080, TEAL), Create(sp), run_time=2.2,
                      rate_func=smooth)
            ok = check_mark(GREEN)
            one = T("one point", 36, color=GREEN)
            VGroup(ok, one).arrange(RIGHT, buff=0.3).move_to([COL_X, -2.3, 0])
            # the TEAL winder sits exactly on the GOLD 3θ arrow, then fades to reveal it
            self.play(*appear(ok, one, lag=0.2), FadeOut(winder), Flash(Dot(tip(300)), color=GREEN, flash_radius=0.35),
                      run_time=min(1.4, c.until(floor=0.8)))

    # ------------------------------------------------------------------ c2.int.4
    def clip4(self):
        with self.say("c2.int.4") as c:
            pc2, u2 = np.array([-3.0, 0.85, 0]), 1.45
            R = 2 ** 0.2
            plane2 = argand_plane(pc2, u2, 2.4)
            ring = DashedVMobject(Circle(radius=R * u2, color=GOLD, stroke_width=3).move_to(pc2), num_dashes=44)
            dots = []
            for k in range(5):
                deg = 18 + 72 * k
                dots.append(Dot(tip(deg, pc2, R * u2), radius=0.12, color=GREEN if k == 0 else TEAL))
            z5 = MathTex(r"z^5 = ", r"2i", font_size=60)
            z5[1].set_color(YELLOW)
            z5.move_to([3.4, 2.2, 0])
            sweep_clear(self, FadeIn(plane2), FadeIn(ring), *[FadeIn(d, scale=0.5) for d in dots],
                        FadeIn(z5, shift=0.25 * DOWN), run_time=1.8)
            c.wait_until("fifths")

            line = MathTex(r"(\pi/2 + ", r"2\pi n", r")/5 = \pi/10 + ", r"2\pi n", r"/5", font_size=56)
            line[1].set_color(TEAL)
            line[3].set_color(TEAL)
            line.move_to([0, -2.05, 0])
            ft = T("full turns", 30, color=TEAL).next_to(line[1], DOWN, buff=0.22)
            self.play(*appear(line, ft, lag=0.5, shift=None), run_time=1.5)   # no drop: the tag would pass through the line
            self.wait(0.6)
            steps = []
            for k in range(5):
                a0 = np.deg2rad(18 + 72 * k)
                steps.append(Arc(radius=R * u2 + 0.32, start_angle=a0, angle=np.deg2rad(72) if k < 4 else 0.001,
                                 arc_center=pc2, color=TEAL, stroke_width=4))
            lights = []
            for k in range(5):
                anims = [Flash(dots[k], color=dots[k].get_color(), flash_radius=0.3), dots[k].animate.scale(1.4)]
                if k < 4:
                    anims.append(Create(steps[k]))
                lights.append(AnimationGroup(*anims))
            self.play(LaggedStart(*lights, lag_ratio=0.7), run_time=min(3.5, c.until("later", floor=1.0)))
            c.wait_until("later")

            box = RoundedRectangle(corner_radius=0.2, width=5.5, height=2.3, color=DIM, stroke_width=2.5)
            head = T("Part 5: how many values?", 30)
            ii = MathTex(r"i^{\,i}", font_size=64, color=YELLOW)
            VGroup(head, ii).arrange(DOWN, buff=0.35).move_to(box)
            card = VGroup(box, head, ii).move_to([3.75, 0.0, 0])
            self.play(FadeIn(box), *appear(head, ii, lag=0.3), run_time=1.3)
