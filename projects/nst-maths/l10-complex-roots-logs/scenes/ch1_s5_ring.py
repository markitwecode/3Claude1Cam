"""Chapter 1, scene 5: the table of n, θ, z, the ring of five, built from the roots of unity; the general recipe and the FTA. Clips c1.ring.1 – c1.ring.5."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S4 = load_scene("ch1_s4_method")
O, U, R5 = S4.O, S4.U, S4.R5
P, root_angle = S4.P, S4.root_angle
FS = 38                     # table font size
DOT_R = 0.11
TX = -6.5                   # table left edge
ROW_Y0, PITCH = 1.95, 0.8   # row n = 0 and row pitch
HEAD_Y = 2.95


def tex(*s, size=FS, color=FG):
    return MathTex(*s, font_size=size, color=color)


def zcell(angle_tex):
    m = tex(r"2^{1/5}", r"e^{i" + angle_tex + "}")
    m[0].set_color(GOLD)
    return m


def arc_at(a0, a1, rad, color=YELLOW):
    return Arc(radius=rad, start_angle=a0, angle=a1 - a0, arc_center=O, color=color, stroke_width=4)


class Ring(NarratedScene):
    def construct(self):
        shot = S4.handover_shot()
        self.add(shot)
        self.plane, self.ring, self.ticks = shot[0], shot[1], shot[2]
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ table layout
    def layout(self):
        self.th = [tex(r"\pi/10"), tex(r"5\pi/10 = \pi/2"), tex(r"9\pi/10"), tex(r"13\pi/10"),
                   tex(r"17\pi/10"), tex(r"\pi/10 + 2\pi")]
        self.pr = [tex(r"= -7\pi/10", color=GREEN), tex(r"= -3\pi/10", color=GREEN)]
        z1 = tex(r"2^{1/5}", r"e^{i\pi/2}", "=", r"2^{1/5}", r"\,i")
        z1[0].set_color(GOLD)
        z1[3].set_color(GOLD)
        z1[4].set_color(PINK)
        self.zs = [zcell(r"\pi/10"), z1, zcell(r"9\pi/10"), zcell(r"13\pi/10"), zcell(r"17\pi/10")]
        self.same = T("same as n = 0", size=34, color=GREEN)
        self.ns = [tex(str(k)) for k in range(6)]
        th_w = max(max(m.width for m in self.th), self.th[3].width + 0.18 + self.pr[0].width)
        nx = TX + 0.15
        thx = TX + 0.75
        zx = thx + th_w + 0.55
        for k in range(6):
            y = ROW_Y0 - k * PITCH
            self.ns[k].move_to([nx, y, 0])
            self.th[k].move_to([0, y, 0]).align_to([thx, 0, 0], LEFT)
            if k < 5:
                self.zs[k].move_to([0, y, 0]).align_to([zx, 0, 0], LEFT)
        self.same.move_to([0, ROW_Y0 - 5 * PITCH, 0]).align_to([zx, 0, 0], LEFT)
        for i, k in enumerate([3, 4]):
            self.pr[i].next_to(self.th[k], RIGHT, buff=0.18)
        hn = tex("n", color=DIM).move_to([nx, HEAD_Y, 0])
        hth = tex(r"\theta", color=DIM).move_to([0, HEAD_Y, 0]).align_to([thx, 0, 0], LEFT)
        hz = tex("z", color=DIM).move_to([0, HEAD_Y, 0]).align_to([zx, 0, 0], LEFT)
        right = max(self.zs[1].get_right()[0], self.same.get_right()[0])
        rule = Line([TX - 0.1, HEAD_Y - 0.42, 0], [right + 0.1, HEAD_Y - 0.42, 0], stroke_width=2, color=DIM)
        self.head = VGroup(hn, hth, hz, rule)
        self.dots = [Dot(P(R5, root_angle(k)), radius=DOT_R, color=GREEN if k == 0 else TEAL).set_z_index(3)
                     for k in range(5)]

    # ------------------------------------------------------------ clip 1: the table
    def clip1(self):
        self.layout()
        with self.say("c1.ring.1") as c:
            self.play(*appear(self.head, shift=None), run_time=min(1.0, c.until("n0")))  # early: table header
            c.wait_until("n0")
            for k, cue in [(0, "imag"), (1, "imag")]:
                self.play(*appear(self.ns[k], self.th[k], self.zs[k], lag=0.3), run_time=1.4)
                if k == 0:
                    self.play(GrowFromCenter(self.dots[0]), FadeOut(self.ticks[0]), run_time=0.8)
                    c.wait_until("n1")
            c.wait_until("imag")
            self.play(GrowFromCenter(self.dots[1]), FadeOut(self.ticks[1]), run_time=0.8)
            self.play(FlashAround(self.zs[1][4], color=PINK, run_time=1.5, time_width=1.5),
                      FlashAround(self.dots[1], color=TEAL, run_time=1.5, time_width=1.5))
            c.wait_until("n234")
            for k, cue in [(2, "thirteen"), (3, "seventeen"), (4, None)]:
                self.play(*appear(self.ns[k], self.th[k], self.zs[k], lag=0.2), run_time=1.0)
                self.play(GrowFromCenter(self.dots[k]), FadeOut(self.ticks[k]), run_time=0.5)
                if cue:
                    c.wait_until(cue)
            c.wait_until("n5")
            self.play(*appear(self.ns[5], self.th[5], lag=0.3), run_time=1.0)
            c.wait_until("same")
            self.arrow = Arrow(O, P(R5, root_angle(0)), buff=0, stroke_width=5, max_tip_length_to_length_ratio=0.18,
                               tip_length=0.24, color=TEAL)
            self.play(GrowArrow(self.arrow), run_time=0.5)
            self.play(Rotate(self.arrow, angle=TAU, about_point=O), run_time=1.8, rate_func=smooth)
            self.play(FlashAround(self.dots[0], color=GREEN, run_time=1.2, time_width=1.5),
                      *disappear(self.arrow), run_time=1.0)
            c.wait_until("same root")
            self.play(*appear(self.same), run_time=min(1.0, c.until()))
        self.remove(self.ticks)

    # ------------------------------------------------------------ clip 2: the picture
    def clip2(self):
        with self.say("c1.ring.2") as c:
            self.poly = Polygon(*[P(R5, root_angle(k)) for k in range(5)], color=TEAL, stroke_width=3)
            self.poly.set_stroke(opacity=0.45)
            self.play(Create(self.poly), run_time=1.5)
            c.wait_until("radius")
            end = P(R5, -PI / 2)
            self.rad = Line(O, end, color=GOLD, stroke_width=4)
            self.rlab = tex(r"r = 2^{1/5}", size=36, color=GOLD).next_to(self.rad, LEFT, buff=0.12)
            self.rlab.shift(0.2 * UP)
            set_backstroke(self.rlab)
            self.play(Create(self.rad), *appear(self.rlab, shift=None), run_time=1.2)
            self.play(FlashAround(self.plane.circle, color=DIM, run_time=1.5, time_width=1.0))
            c.wait_until("first")
            self.a1 = arc_at(0, PI / 10, U * R5 + 0.4)
            self.a1lab = tex(r"\pi/10", size=34, color=YELLOW).move_to(O + (U * R5 + 0.95) * np.array(
                [np.cos(PI / 20), np.sin(PI / 20), 0]))
            set_backstroke(self.a1lab)
            self.play(Create(self.a1), *appear(self.a1lab, shift=None), run_time=1.2)
            c.wait_until("spacing")
            self.a2 = arc_at(root_angle(0), root_angle(1), U * R5 + 0.4, color=TEAL)
            mid = (root_angle(0) + root_angle(1)) / 2
            self.a2lab = tex(r"2\pi/5 = 4\pi/10", size=34, color=TEAL).move_to(
                O + (U * R5 + 1.2) * np.array([np.cos(mid), np.sin(mid), 0]) + 0.35 * RIGHT)
            set_backstroke(self.a2lab)
            self.play(Create(self.a2), *appear(self.a2lab, shift=None), run_time=1.4)
            c.wait_until("contrast")
            ghost_c = self.plane.circle.copy().set_stroke(RED, 3, opacity=0.6)
            ghost_d = Dot(O + U * RIGHT, radius=DOT_R, color=RED).set_opacity(0.6)
            x1 = cross_mark().scale(0.8).move_to(O + U * RIGHT + 0.0 * DOWN)
            x2 = cross_mark().scale(0.8).move_to(O + U * np.array([np.cos(1.25 * PI), np.sin(1.25 * PI), 0]))
            self.ghosts = VGroup(ghost_c, ghost_d)
            self.crosses = VGroup(x1, x2)
            self.play(FadeIn(self.ghosts), run_time=1.0)
            self.play(*[GrowFromCenter(x) for x in self.crosses], run_time=1.0)

    # ------------------------------------------------------------ clip 3: from the roots of unity
    def clip3(self):
        with self.say("c1.ring.3") as c:
            s3 = load_scene("ch1_s3_unity")
            self.pent = s3.unity_pentagon(center=O, unit=U, dot_r=DOT_R)
            self.pent.set_z_index(4)
            self.play(*disappear(self.ghosts, self.crosses, self.a1, self.a1lab, self.a2, self.a2lab, self.rlab),
                      *set_alpha(self.dots + [self.poly], 0.3), run_time=1.0)
            self.play(FadeIn(self.pent), run_time=min(1.2, c.until("scale")))
            c.wait_until("scale")
            pts = [O + R5 * (d.get_center() - O) for d in self.pent.dots]
            self.play(self.pent.polygon.animate.scale(R5, about_point=O),
                      *[d.animate.move_to(p) for d, p in zip(self.pent.dots, pts)],
                      run_time=min(1.8, 0.9 * c.until("turn")))
            c.wait_until("turn")
            self.tarc = arc_at(0, PI / 10, U * R5 + 0.4)
            self.play(Rotate(self.pent.polygon, PI / 10, about_point=O),
                      *[Rotate(d, PI / 10, about_point=O) for d in self.pent.dots],
                      Create(self.tarc), run_time=min(1.8, 0.9 * c.until("land")))
            c.wait_until("land")
            self.play(*set_alpha(self.dots + [self.poly], 1), FadeOut(self.pent), *disappear(self.tarc),
                      run_time=0.8)
            self.play(*flash(self.dots, color=YELLOW, run_time=1.4, time_width=1.5))

    # ------------------------------------------------------------ clip 4: principal arguments, recipe
    def clip4(self):
        with self.say("c1.ring.4", gap=1.6) as c:
            self.play(*appear(*self.pr, lag=0.4), run_time=1.2)
            self.plab = T("principal argument", size=32, color=GREEN)
            self.plab.move_to([self.pr[0].get_x() - 0.6, ROW_Y0 - 5 * PITCH - 0.85, 0])
            c.wait_until(own_word=self.plab)
            self.play(*appear(self.plab), run_time=1.0)
            self.play(*flash([self.dots[3], self.dots[4]], color=GREEN, run_time=1.5, time_width=1.5))
            c.wait_until("recipe")

            l1 = tex(r"z^k = w", size=50)
            l2 = tex(r"|z| = ", r"|w|^{1/k}", size=48)
            l2[1].set_color(GOLD)
            l3 = tex(r"\arg z = \dfrac{\arg w + 2\pi n}{k}", size=48)
            l3[0][10:13].set_color(TEAL)
            l4 = tex(r"n = 0, 1, \dots, k-1", size=40)
            body = VGroup(l1, l2, l3, l4).arrange(DOWN, buff=0.45)
            body.move_to([-3.3, 0.0, 0])
            self.box = SurroundingRectangle(body, color=YELLOW, buff=0.4, corner_radius=0.12, stroke_width=3)
            self.recipe = VGroup(l1, l2, l3, l4)
            sweep_clear(self, keep=[self.plane, self.ring, self.poly, self.rad] + self.dots, run_time=1.0)
            self.play(*appear(l1, l2, lag=0.5), run_time=1.2)
            c.wait_until("angles")
            self.play(*appear(l3), run_time=1.2)
            c.wait_until("That makes K roots")
            self.play(*appear(l4), FadeIn(self.box), run_time=1.2)

    # ------------------------------------------------------------ clip 5: why five
    def clip5(self):
        with self.say("c1.ring.5", gap=3.5) as c:
            self.play(*flash(self.dots, color=TEAL, run_time=1.4, time_width=1.5))
            c.wait_until("quote")
            quote = T("“Indeed, for any polynomial of\ndegree n, there will always be\nn roots in the complex plane\n"
                      "(counted with multiplicity).”", size=34, line_spacing=1.1)
            quote.move_to([-3.3, 1.4, 0])
            self.play(*swap(VGroup(self.recipe, self.box), quote), run_time=1.4)  # early: quoted remark, read in paraphrase
            c.wait_until("fta")
            note = T("This [is] the fundamental theorem\nof algebra (see §2.7).", size=34, color=YELLOW, slant=ITALIC)
            note.next_to(quote, DOWN, buff=0.6).align_to(quote, LEFT)
            self.play(*appear(note), run_time=1.0)
            c.wait_until("five")
            poly = tex(r"z^5 - 2i", size=48).move_to([O[0] - 0.6, 3.15, 0])
            self.play(*appear(poly), run_time=1.0)
            tag = T("degree 5", size=32, color=GOLD).next_to(poly, RIGHT, buff=0.5)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.8)
            nums = []
            for k in range(5):
                a = root_angle(k)
                nums.append(tex(str(k + 1), size=34, color=YELLOW).move_to(
                    O + (U * R5 + 0.45) * np.array([np.cos(a), np.sin(a), 0])))
            for m in nums:
                set_backstroke(m)
            self.play(*appear(*nums, lag=0.5, shift=None), run_time=2.2)
            c.wait_until("l11")
            l11 = T("Lecture 11", size=34, color=DIM).move_to([-3.3, -2.9, 0])
            self.play(*appear(l11), run_time=min(1.0, c.until()))
