"""Chapter 2, scene 7: recap in five panels, then what comes next. Clips c2.recap.1 – c2.recap.2."""
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

S2 = load_scene("ch2_s2_theorem")
S3 = load_scene("ch2_s3_integer")
S4 = load_scene("ch2_s4_expand")
S6 = load_scene("ch2_s6_expo")

TOP_Y = 1.95       # centre of the top row's pictures
BOT_Y = -1.35      # centre of the bottom row's pictures
CAP_SIZE = 30


def caption_under(pic, cap, buff=0.3):
    cap.next_to(pic, DOWN, buff=buff)
    return cap


def panel_r1():
    c = np.array([-5.3, TOP_Y, 0])
    plane = S2.argand_plane(center=c, unit=1.0, extent=1.25)
    steps = S2.power_steps(n=4, center=c, unit=1.0, dim=0.5)
    pic = VGroup(plane, steps)
    cap = MathTex(r"(e^{i\theta})^n", "=", r"e^{in\theta}", font_size=40)
    cap[0].set_color(GOLD)
    cap[2].set_color(GOLD)
    caption_under(pic, cap, 0.2)
    return pic, cap


def panel_r2():
    c = np.array([-2.0, TOP_Y, 0])
    plane = S3.argand_plane(center=c, unit=1.0, extent=1.25)
    halves = S3.half_angle_arrows(center=c, unit=1.0)
    # the tag sits just right of the plane, below the axis: clear of the plane and of r3's row
    halves.remove(halves.tag)
    halves.tag = T("two\nvalues", 30, color=RED, line_spacing=0.8)
    halves.add(halves.tag)
    halves.tag.next_to(c + np.array([1.25, -0.8, 0]), RIGHT, buff=0.15)
    pic = VGroup(plane, halves)
    cap = VGroup(MathTex("n", font_size=38), T("must be an integer", CAP_SIZE))
    cap.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    caption_under(pic, cap, 0.2)
    return pic, cap, halves


def panel_r3():
    rows = S4.pascal_rows(top=np.array([1.25, TOP_Y + 0.75, 0]), size=40, dx=0.44)
    row = rows[4]
    row.move_to([1.1, TOP_Y, 0])
    dial = S4.i_dial(center=np.array([4.65, TOP_Y, 0]), r=0.6, size=30)
    pic = VGroup(row, dial)
    cap = T("Pascal's row, powers of i", CAP_SIZE, t2s={" i": ITALIC})
    cap.set_y(TOP_Y - 1.62).set_x(pic.get_x())
    return pic, cap, row, dial


def panel_r4():
    cos4 = MathTex(r"\cos 4\theta", "=", r"8\cos^4\theta - 8\cos^2\theta + 1", font_size=32)
    sin4 = MathTex(r"\sin 4\theta", "=", r"4\cos\theta\sin\theta\,(2\cos^2\theta - 1)", font_size=32)
    cos4.set_color(BLUE)
    sin4.set_color(PINK)
    for m in (cos4[1], sin4[1]):
        m.set_color(FG)
    lines = VGroup(cos4, sin4).arrange(DOWN, buff=0.45)
    # align the two '=' signs
    sin4.shift((cos4[1].get_x() - sin4[1].get_x()) * RIGHT)
    re = MathTex(r"\mathrm{Re}{:}", font_size=32, color=BLUE).next_to(cos4, LEFT, buff=0.6)
    im = MathTex(r"\mathrm{Im}{:}", font_size=32, color=PINK).next_to(sin4, LEFT, buff=0.6)
    im.align_to(re, LEFT)
    box = SurroundingRectangle(VGroup(cos4, sin4), color=YELLOW, buff=0.25, stroke_width=3)
    pic = VGroup(re, im, cos4, sin4, box).move_to([0, BOT_Y, 0])
    pic.shift((-6.5 - pic.get_left()[0]) * RIGHT)
    cap = T("match real parts, match imaginary parts", 28)
    return pic, cap, box


def panel_r5(theta=S6.TH0):
    cx, cy, u, ex, ey = 0.45, BOT_Y, 0.7, 1.45, 1.3
    e = np.exp(1j * theta)
    P = lambda z: S6.to_pt(z, cx, cy, u)  # noqa: E731
    plane = S6.build_plane(cx, cy, u, ex, ey)
    gold = S6.arrow_between(P(0), P(e), GOLD, width=5)
    purple = S6.arrow_between(P(e), P(e + e.conjugate()), PURPLE, width=5)
    dot = Dot(P(2 * e.real), radius=0.08, color=BLUE)
    dl = MathTex(r"2\cos\theta", font_size=30, color=BLUE).next_to(dot, DOWN, buff=0.18)
    set_backstroke(dl, width=6)
    arrows = VGroup(gold, purple, dot, dl)
    forms = VGroup()
    for f, tag in ((S6.cos_formula(), "(77)"), (S6.sin_formula(), "(78)")):
        f.scale(0.66)
        t, box = S6.tagged_box(f, tag, 28)
        forms.add(VGroup(f, t, box))
    forms.arrange(DOWN, buff=0.22).next_to(plane, RIGHT, buff=0.45)
    pic = VGroup(plane, arrows, forms)
    cap = MathTex(r"\cos\theta\text{ and }\sin\theta\text{ as exponentials}", font_size=34)
    return pic, cap, plane, arrows, forms


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    def clip1(self):
        with self.say("c2.recap.1") as c:
            c.wait_until("r1")
            # r1: the turned arrows
            pic, cap = panel_r1()
            plane, steps = pic
            self.play(FadeIn(plane), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in steps.arrows], lag_ratio=0.35),
                      LaggedStart(*[Create(a) for a in steps.arcs], lag_ratio=0.35),
                      FadeIn(steps.label), run_time=min(2.0, c.until("power")))
            c.wait_until("is E to the eye N theta")
            self.play(*appear(cap), run_time=1.0)
            self.p1 = VGroup(pic, cap)

            # r2: the two half-angle values
            c.wait_until("r2")
            pic, cap, h = panel_r2()
            plane = pic[0]
            self.play(FadeIn(plane), GrowArrow(h.first), run_time=1.0)
            c.wait_until("whole number")
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("a fraction splits")
            self.play(Create(h.arc), GrowArrow(h.second), run_time=1.5)
            self.play(*appear(h.tag), run_time=min(1.0, c.until("r3")))
            self.p2 = VGroup(pic, cap)

            # r3: Pascal's row and the i dial
            c.wait_until("r3")
            pic, cap, row, dial = panel_r3()
            c.wait_until("Pascal's row")
            self.play(*appear(*row, lag=0.15), run_time=1.2)
            c.wait_until("powers of eye")
            self.play(FadeIn(dial, scale=0.9), run_time=1.0)
            self.play(*appear(cap), run_time=1.0)
            self.p3 = VGroup(pic, cap)

            # r4: the boxed pair from s5
            c.wait_until("r4")
            pic, cap, box = panel_r4()
            re, im, cos4, sin4, _ = pic
            cap.set_y(BOT_Y - 1.65).set_x(-6.5 + cap.width / 2)
            self.play(*appear(re, cos4), run_time=1.2)
            c.wait_until("then imaginary parts")
            self.play(*appear(im, sin4), run_time=1.2)
            self.play(GrowFromCenter(box), *appear(cap), run_time=min(1.2, c.until("r5")))
            self.p4 = VGroup(pic, cap)

            # r5: mirror-image arrows tip to tail
            c.wait_until("r5")
            pic, cap, plane, arrows, forms = panel_r5()
            gold, purple, dot, dl = arrows
            cap.set_y(BOT_Y - 1.65).set_x(6.5 - cap.width / 2)
            self.play(FadeIn(plane), GrowArrow(gold), run_time=1.0)
            self.play(GrowArrow(purple), run_time=1.0)
            self.play(FadeIn(dot, scale=0.5), *appear(dl), run_time=0.8)
            c.wait_until("writes cosine and sine")
            self.play(*appear(forms[0], forms[1], lag=0.3), run_time=1.4)
            self.play(*appear(cap), run_time=min(1.0, c.until(None)))
            self.p5 = VGroup(pic, cap)
            self.forms = forms

    def clip2(self):
        heading = T("Next time", 48, color=DIM).move_to([0, 2.3, 0])
        cube = MathTex(r"\cos^3\theta", "=", r"\square", r"\cos 3\theta", "+", r"\square", r"\cos\theta",
                       font_size=60)
        for i, col in enumerate([BLUE, FG, YELLOW, BLUE, FG, YELLOW, BLUE]):
            cube[i].set_color(col)
        cube.move_to([0, 0.6, 0])
        total = MathTex(r"1 + \cos\theta + \cos 2\theta + \dots + \cos(N-1)\theta", "=", "?", font_size=48)
        total[0].set_color(BLUE)
        total[2].set_color(YELLOW)
        total.move_to([0, -1.3, 0])

        with self.say("c2.recap.2") as c:
            others = [self.p1, self.p2, self.p3, self.p4]
            self.play(*set_alpha(others, 0.4), run_time=0.8)
            c.wait_until("those two formulas")
            self.play(*flash(list(self.forms), run_time=1.4, time_width=1.5), run_time=1.4)
            c.wait_until("a power like")
            panels = [self.p1, self.p2, self.p3, self.p4, self.p5]
            self.play(*during([FadeOut(p, scale=0.5) for p in panels], 0, 0.5),
                      *during(appear(heading, cube, lag=0.3), 0.5, 1.0),
                      run_time=min(1.8, c.until("sums")))
            c.wait_until("sums")
            self.play(*appear(total[0], total[1]), run_time=1.2)
            c.wait_until("geometric series")
            self.play(FadeIn(total[2], scale=1.3), run_time=0.6)
            self.play(FlashAround(total[2], run_time=1.5, time_width=1.5))
