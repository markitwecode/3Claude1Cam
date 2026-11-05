"""Chapter 1, scene 4: Example 28, z^5 = 2i in three steps, and the 2πn trap. Clips c1.method.1 – c1.method.5."""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# The Argand plane (right half): origin on screen, unit length, half-extent of the axes.
O = np.array([3.7, -0.65, 0.0])
U = 1.25
EXT = 2.8
R5 = 2 ** 0.2                 # 2^{1/5}, radius of the ring of five
X0 = -6.0                     # left edge of the working
NUM_X = -6.55                 # x of the step numerals
FS = 48                       # working font size


def argand_plane(center=O, unit=U, extent=EXT):
    """PLAN.md's running Argand plane: faint grid, Re/Im axes, DIM unit circle (ch2_s2, unchanged)."""
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


def P(r, ang):
    """Screen point of modulus r (plane units), angle ang (radians)."""
    return O + U * r * np.array([np.cos(ang), np.sin(ang), 0])


def ring_circle():
    """The dashed GOLD circle of radius 2^{1/5}, as ch2's ring_of_five()."""
    return DashedVMobject(Circle(radius=U * R5, color=GOLD, stroke_width=3).move_to(O), num_dashes=40)


def root_angle(k):
    return PI / 10 + 2 * PI * k / 5


def ghost_ticks():
    """Five faint radial ticks on the dashed circle, one per fifth of a turn from π/10."""
    ticks = VGroup()
    for k in range(5):
        a = root_angle(k)
        d = np.array([np.cos(a), np.sin(a), 0])
        ticks.add(Line(O + (U * R5 - 0.17) * d, O + (U * R5 + 0.17) * d, stroke_width=4, color=FG,
                       stroke_opacity=0.5))
    return ticks


def handover_shot():
    """Last frame here, first frame of ch1_s5_ring: plane, dashed 2^{1/5} circle, five ghost ticks."""
    return VGroup(argand_plane(), ring_circle(), ghost_ticks())


def condensed_steps(size=40):
    """Example 28's three steps, one line each (for the recap)."""
    s1 = MathTex(r"z^5 = r^5e^{5i\theta}", font_size=size)
    s1[0][3:5].set_color(GOLD)
    s1[0][8].set_color(YELLOW)
    s2 = MathTex(r"2i = 2e^{i(\pi/2 + 2\pi n)}", font_size=size)
    s2[0][3].set_color(GOLD)
    s2[0][10:14].set_color(TEAL)
    s3a = MathTex(r"r = 2^{1/5},\quad \theta = \frac{\pi}{10} +", font_size=size)
    s3a[0][0:6].set_color(GOLD)
    s3b = MathTex(r"\frac{2\pi n}{5}", font_size=size, color=TEAL).next_to(s3a, RIGHT, buff=0.12)
    s3 = VGroup(s3a, s3b)
    rows = VGroup()
    for i, s in enumerate([s1, s2, s3]):
        num = T(str(i + 1), size=size - 6, color=DIM)
        rows.add(VGroup(num, s).arrange(RIGHT, buff=0.4))
    rows.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
    return rows


def row(mob, y):
    """Left-align a working line at X0, centred on height y."""
    mob.move_to([0, y, 0]).align_to([X0, 0, 0], LEFT)
    return mob


def numeral(k, ref):
    return T(str(k), size=34, color=DIM).move_to([NUM_X, ref.get_y(), 0])


class Method(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        # the working clears; the plane, dashed circle and ghost ticks stay for ch1_s5_ring
        keep = [self.plane, self.ring, self.ticks]
        self.play(*[FadeOut(m) for m in self.mobjects if m not in keep], run_time=1.0)
        self.wait(1.0)

    # ---------------------------------------------------------------- step 1
    def clip1(self):
        with self.say("c1.method.1") as c:
            self.plane = argand_plane()
            self.top = MathTex(r"z^5 = 2i", font_size=56)
            self.top[0][3:5].set_color(YELLOW)
            row(self.top, 3.2)
            self.dot2i = Dot(P(2, PI / 2), radius=0.11, color=YELLOW).set_z_index(3)
            self.lab2i = MathTex(r"2i", font_size=36, color=YELLOW).next_to(self.dot2i, UL, buff=0.1)
            self.play(FadeIn(self.plane), *appear(self.top), run_time=1.5)
            self.play(GrowFromCenter(self.dot2i), *appear(self.lab2i), run_time=1.0)
            c.wait_until("step1")

            self.r1 = row(MathTex(r"z = re^{i\theta}", font_size=FS), 2.25)
            self.r1[0][2].set_color(GOLD)
            self.r1[0][5].set_color(YELLOW)
            self.n1 = numeral(1, self.r1)
            self.play(*appear(self.n1), run_time=0.8)
            c.wait_until("polar")
            self.play(*appear(self.r1), run_time=1.0)
            c.wait_until("left")

            self.r2 = row(MathTex(r"z^5 = r^5e^{5i\theta}", font_size=FS), 1.45)
            self.r2[0][3:5].set_color(GOLD)
            self.r2[0][8].set_color(YELLOW)
            self.play(*appear(self.r2), run_time=1.2)

    # ---------------------------------------------------------------- step 2
    def clip2(self):
        with self.say("c1.method.2") as c:
            self.r3a = row(MathTex(r"|2i| = 2,", font_size=FS), 0.45)
            self.r3a[0][5].set_color(GOLD)
            self.r3b = MathTex(r"\arg 2i = \pi/2", font_size=FS).next_to(self.r3a, RIGHT, buff=0.55)
            self.r3b.align_to(self.r3a, DOWN)
            self.r3b[0][6:9].set_color(YELLOW)
            self.n2 = numeral(2, self.r3a)
            self.play(*appear(self.n2), run_time=0.8)
            c.wait_until("up")

            # the lecturer's margin sketch: 2i straight up, length 2, a right angle
            self.arrow = Arrow(O, P(2, PI / 2), buff=0, stroke_width=6, max_tip_length_to_length_ratio=0.12,
                               tip_length=0.26, color=YELLOW)
            self.brace = Brace(Line(O, P(2, PI / 2)), LEFT, buff=0.12, color=GOLD)
            self.brace2 = MathTex("2", font_size=38, color=GOLD).next_to(self.brace, LEFT, buff=0.12)
            self.rangle = Arc(radius=0.38, start_angle=0, angle=PI / 2, arc_center=O, color=YELLOW, stroke_width=4)
            self.pi2 = MathTex(r"\pi/2", font_size=34, color=YELLOW).move_to(O + 0.78 * np.array([1, 1, 0]) / np.sqrt(2) + [0.12, 0, 0])
            self.play(GrowArrow(self.arrow), run_time=1.0)
            self.play(GrowFromCenter(self.brace), *appear(self.brace2), Create(self.rangle), run_time=1.2)
            c.wait_until("modarg")
            self.play(*appear(self.r3a), run_time=1.0)
            c.wait_until("angle")
            self.play(*appear(self.r3b), *appear(self.pi2), run_time=1.0)
            c.wait_until("every")

            # one more full turn: the same point again
            self.spiral = ParametricFunction(
                lambda t: O + U * (1.4 + 0.25 * t / TAU) * np.array([np.cos(PI / 2 + t), np.sin(PI / 2 + t), 0]),
                t_range=[0, TAU], color=TEAL, stroke_width=4)
            self.play(Rotate(self.arrow, angle=TAU, about_point=O), Create(self.spiral),
                      run_time=min(2.2, 0.95 * c.until("keep")))
            c.wait_until("keep")

            self.r4 = row(MathTex(r"2i = 2e^{i(\pi/2 + 2\pi n)}", font_size=FS), -0.4)
            self.r4[0][3].set_color(GOLD)
            self.r4[0][10:14].set_color(TEAL)
            self.play(*appear(self.r4), run_time=1.2)
            c.wait_until("plus two pi n")
            self.play(FlashAround(self.r4[0][10:14], color=TEAL, run_time=1.5, time_width=1.5))
            c.wait_until("hand")

            # the printed notes, and the lecturer's handwritten insertion
            self.aside = MathTex(r"2i = 2\exp(i\pi/2)", font_size=38, color=DIM)
            self.aside_lab = T("printed:", size=28, color=DIM)
            VGroup(self.aside_lab, self.aside).arrange(RIGHT, buff=0.3)
            self.aside_lab.move_to([0, -1.5, 0]).align_to([X0 + 0.3, 0, 0], LEFT)
            self.aside.next_to(self.aside_lab, RIGHT, buff=0.3)
            gap = (self.aside[0][11].get_right() + self.aside[0][12].get_left()) / 2
            self.caret = MathTex(r"\wedge", font_size=30, color=TEAL).move_to([gap[0], self.aside.get_bottom()[1] - 0.22, 0])
            self.ins = MathTex(r"+2\pi n", font_size=30, color=TEAL).move_to([gap[0], self.aside.get_top()[1] + 0.25, 0])
            self.play(*appear(self.aside_lab, self.aside, lag=0.3), run_time=1.2)
            c.wait_until("lecturer")
            self.play(*appear(self.caret, self.ins, lag=0.3, shift=None), run_time=1.0)

    # ---------------------------------------------------------------- what n means; step 3, lengths
    def clip3(self):
        with self.say("c1.method.3") as c:
            n_glyph = self.r4[0][13]
            self.tag = T("n counts full turns", size=30, color=TEAL)
            self.tag.move_to([0, -2.65, 0]).align_to([X0 + 2.6, 0, 0], LEFT)
            self.play(FlashAround(n_glyph, color=TEAL), *appear(self.tag), run_time=1.2)
            c.wait_until("notdeg")

            self.deg = T("degree", size=30, color=DIM).next_to(self.tag, LEFT, buff=0.8)
            self.strike = Line(self.deg.get_left() + 0.1 * LEFT, self.deg.get_right() + 0.1 * RIGHT, color=RED, stroke_width=4)
            c.wait_until(own_word=self.deg)
            self.play(*appear(self.deg), run_time=0.9)
            self.play(Create(self.strike), run_time=0.6)
            c.wait_until("step3")

            # tidy: keep the two sides to be matched, move them up
            gone = disappear(self.n1, self.r1, self.n2, self.r3a, self.r3b,
                              self.aside_lab, self.aside, self.caret, self.ins)
            self.play(*during(gone, 0, 0.45),
                      *during([self.r2.animate.move_to(row(self.r2.copy(), 2.25)),
                               self.r4.animate.move_to(row(self.r4.copy(), 1.45))], 0.45, 1),
                      run_time=1.4)
            self.s1a = row(MathTex(r"r^5 = 2", font_size=FS), 0.45)
            self.s1a[0][0:2].set_color(GOLD)
            self.s1a[0][3].set_color(GOLD)
            self.n3 = numeral(3, self.s1a)
            self.play(*appear(self.n3), run_time=0.8)
            c.wait_until("r")

            self.play(FlashAround(self.r2[0][3:5], color=GOLD), FlashAround(self.r4[0][3], color=GOLD), run_time=1.0)
            self.play(*appear(self.s1a), run_time=1.0)
            c.wait_until("root")

            self.s1b = MathTex(r"\Rightarrow r = 2^{1/5} \approx 1.149", font_size=FS).next_to(self.s1a, RIGHT, buff=0.3)
            for sl in (self.s1b[0][1], self.s1b[0][3:7], self.s1b[0][8:13]):
                sl.set_color(GOLD)
            self.ring = ring_circle()
            self.play(*appear(self.s1b), run_time=1.0)
            self.play(Create(self.ring), *set_alpha([self.arrow, self.brace, self.brace2, self.rangle, self.pi2], 0.3),
                      run_time=1.5)

    # ---------------------------------------------------------------- step 3, angles
    def clip4(self):
        with self.say("c1.method.4") as c:
            self.s2 = row(MathTex(r"5\theta = \pi/2 + 2\pi n", font_size=FS), -0.4)
            self.s2[0][1].set_color(YELLOW)
            self.s2[0][6:10].set_color(TEAL)
            self.play(FlashAround(self.r2[0][6:9]), FlashAround(self.r4[0][5:15]), run_time=1.2)
            self.play(*appear(self.s2), run_time=1.0)
            c.wait_until("divide")

            self.s3a = MathTex(r"\theta = \frac{\pi}{10} +", font_size=FS)
            self.s3a[0][0].set_color(YELLOW)
            row(self.s3a, -1.5)
            self.s3b = MathTex(r"\frac{2\pi n}{5}", font_size=FS, color=TEAL).next_to(self.s3a, RIGHT, buff=0.15)
            self.play(*appear(self.s3a), run_time=1.0)
            c.wait_until("plus two pi n over five")
            self.play(*appear(self.s3b), run_time=1.0)
            c.wait_until("fifths")

            # the full turn shrinks to a fifth of a turn
            self.fifth = Arc(radius=U * 1.5, start_angle=root_angle(0), angle=2 * PI / 5, arc_center=O,
                             color=TEAL, stroke_width=4)
            mid = root_angle(0) + PI / 5
            self.fifth_lab = MathTex(r"2\pi/5", font_size=36, color=TEAL).move_to(P(1.95, mid))
            self.play(Transform(self.spiral, self.fifth), run_time=2.0)
            self.play(*appear(self.fifth_lab), run_time=0.8)
            c.wait_until("full turns became")
            self.play(FlashAround(self.s3b, color=TEAL), run_time=1.2)
            c.wait_until("roots")

            self.ticks = ghost_ticks()
            self.play(LaggedStart(*[GrowFromCenter(t) for t in self.ticks], lag_ratio=0.3), run_time=1.6)
            settle(self, self.ticks)

    # ---------------------------------------------------------------- the trap
    def clip5(self):
        with self.say("c1.method.5", gap=4.6) as c:
            keep = [self.plane, self.ring, self.ticks, self.r4, self.s3a, self.s3b]
            sweep_clear(self,
                        self.r4.animate.move_to(row(self.r4.copy(), 3.1)),
                        self.s3a.animate.move_to(row(self.s3a.copy(), 2.1)),
                        self.s3b.animate.move_to(self.s3b.get_center() + (2.1 - self.s3a.get_y()) * UP),
                        keep=keep, run_time=1.4)
            c.wait_until("drop")

            self.d1 = row(MathTex(r"2i = 2e^{i\pi/2}", font_size=FS), 0.55).shift(0.3 * RIGHT)
            self.frame = RoundedRectangle(corner_radius=0.15, width=6.3, height=3.1, color=RED, stroke_width=3)
            self.frame.move_to([X0 + 3.0, -0.35, 0])
            self.play(FadeIn(self.frame), *appear(self.d1), run_time=1.2)
            c.wait_until("one")

            self.d2 = row(MathTex(r"5\theta = \pi/2 \Rightarrow \theta = \pi/10", font_size=FS), -0.3).shift(0.3 * RIGHT)
            self.green = Dot(P(R5, root_angle(0)), radius=0.11, color=GREEN).set_z_index(3)
            self.play(*appear(self.d2), run_time=1.0)
            self.play(GrowFromCenter(self.green), run_time=0.8)
            c.wait_until("lost")

            self.qs = [T("?", size=52, color=RED).move_to(P(R5, root_angle(k))) for k in range(1, 5)]
            for q in self.qs:
                set_backstroke(q, width=6)
            self.play(*appear(*self.qs, lag=0.2, shift=None), run_time=1.2)
            c.wait_until("late")

            self.d3 = row(MathTex(r"\theta = \pi/10 + 2\pi n", font_size=FS), -1.2).shift(0.3 * RIGHT)
            self.d3[0][6:10].set_color(RED)
            self.play(*appear(self.d3), run_time=1.0)
            self.turn = Arrow(O, P(R5, root_angle(0)), buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.18,
                              tip_length=0.24, color=FG)
            self.play(GrowArrow(self.turn), run_time=0.6)
            self.play(Rotate(self.turn, angle=TAU, about_point=O), run_time=min(2.4, 0.9 * c.until("rule")))
            c.wait_until("rule")

            self.xout = VGroup(Line(self.frame.get_corner(UL), self.frame.get_corner(DR)),
                               Line(self.frame.get_corner(DL), self.frame.get_corner(UR))).set_stroke(RED, 4)
            self.rule = T("put the 2πn in first, then divide", size=36, t2c={"2πn": TEAL})
            self.rule.move_to([self.frame.get_x(), -2.75, 0])
            self.play(Create(self.xout), *appear(self.rule), run_time=1.2)
            self.play(FlashAround(self.r4[0][10:14], color=TEAL, run_time=1.5, time_width=1.5))
