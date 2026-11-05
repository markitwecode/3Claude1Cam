"""Chapter 3, scene 4: Example 41, take the sine of both sides. Clips c3.tripos.1 – c3.tripos.3."""
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

FRAC = r"\dfrac{x}{\sqrt{1 + x^2}}"
LEFT_X = -6.5          # left edge of the main working column
PX = 3.4              # centre of the side panel
MAIN_SIZE = 44
END_SIZE = 56
END_Y = -0.8


def mt(*parts, size=40, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def question_box():
    """The notes' Example 41 box (p57), in its final place at the top of the frame."""
    head = T("Example 41: Tripos question 2006, paper 2, 1A – (a) only", 30, YELLOW)
    q = mt(r"\text{If }", "y", "=", r"\sin^{-1}\!\left(" + FRAC + r"\right)",
           r"\text{, find } dy/dx \text{ as a function of } x.", size=36)
    mark = T("[4]", 30, GOLD)
    qrow = VGroup(q, mark).arrange(RIGHT, buff=0.6)
    VGroup(head, qrow).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    content = VGroup(head, qrow)
    border = Rectangle(width=content.width + 0.8, height=content.height + 0.6).set_stroke(BLUE, 3)
    border.move_to(content)
    box = VGroup(border, head, q, mark)
    box.move_to(ORIGIN).to_edge(UP, buff=0.3)
    box.border, box.head, box.q, box.mark = border, head, q, mark
    return box


def final_line():
    line = mt(r"\cos y\,", r"\dfrac{dy}{dx}", "=", r"\dfrac{1}{(1 + x^2)^{3/2}}", size=END_SIZE)
    line[1].set_color(GREEN)
    line.move_to([0, END_Y, 0])
    return line


def handover_shot():
    """Scene 5 opens on this: the question box (top) and the line cos y dy/dx = 1/(1+x^2)^{3/2}."""
    box = question_box()
    line = final_line()
    g = VGroup(box, line)
    g.box, g.line = box, line
    return g


class Tripos(NarratedScene):
    def construct(self):
        self.question()
        self.differentiate()
        self.quotient()

    # ---------------------------------------------------------------- clip 1
    def question(self):
        with self.say("c3.tripos.1") as c:
            box = question_box()
            box.scale(1.12).move_to(0.2 * UP)
            self.box = box
            self.play(*appear(box.border, box.head, box.q, box.mark, lag=0.15, shift=None),  # early: the notes' box shown whole
                      run_time=1.2)
            self.play(FlashAround(box.head, run_time=1.5, time_width=1.5))
            c.wait_until("four marks")
            self.play(FlashAround(box.mark, run_time=1.2, time_width=1.5))
            c.wait_until("q")
            self.play(FlashAround(VGroup(*box.q[1:4]), run_time=1.5, time_width=1.5))
            c.wait_until("find the derivative")
            self.play(FlashUnder(box.q[4], run_time=1.5, time_width=1.5))
            c.wait_until("trick")
            self.play(Transform(box, question_box()), run_time=1.5)

            sine = mt(r"\sin", "y", "=", FRAC, size=MAIN_SIZE)
            sine.move_to([0, 0.9, 0]).align_to([LEFT_X, 0, 0], LEFT)
            self.sine = sine
            q = box.q
            c.wait_until("sine")
            self.play(*fly(q[1], sine[1]), *fly(q[2], sine[2]),
                      *fly(VGroup(*q[3][0:5]), sine[0], arc=-PI / 2),
                      *fly(VGroup(*q[3][6:14]), sine[3]), run_time=2.0)
            yx = mt("y", "(x)", size=MAIN_SIZE)
            yx[0].set_color(YELLOW)
            yx.next_to(sine, RIGHT, buff=0.7)
            self.yx = yx
            c.wait_until("depends")
            self.play(*appear(yx), run_time=1.0)

    # ---------------------------------------------------------------- clip 2
    def differentiate(self):
        with self.say("c3.tripos.2") as c:
            diff = mt(r"\dfrac{d}{dx}(\sin y)", "=", r"\dfrac{d}{dx}\left(" + FRAC + r"\right)", size=MAIN_SIZE)
            diff.move_to([0, -1.3, 0]).align_to([LEFT_X, 0, 0], LEFT)
            derive(self, self.sine, diff, run_time=2.0)
            c.wait_until("left")
            self.play(FlashAround(diff[0], run_time=1.5, time_width=1.5))
            main = mt(r"\cos y\,", r"\dfrac{dy}{dx}", "=", r"\dfrac{d}{dx}\left(" + FRAC + r"\right)",
                      size=MAIN_SIZE)
            main[1].set_color(GREEN)
            main.move_to(diff).align_to([LEFT_X, 0, 0], LEFT)
            self.main = main
            c.wait_until("cosine of why")
            self.play(*edit(diff, main), run_time=1.5)

            c.wait_until("right")
            divider = Line([-0.6, 1.5, 0], [-0.6, -3.6, 0]).set_stroke(DIM, 2)
            self.divider = divider
            rhs = main[3]
            self.play(*recolor([rhs[5]], BLUE), run_time=1.0)
            c.wait_until("square root of one")
            self.play(*recolor(list(rhs[7:13]), PURPLE), GrowFromCenter(divider), run_time=1.2)

            rule = mt(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^2}",
                      size=48)
            for i in (5, 12, 17):
                rule[0][i].set_color(BLUE)
            for i in (7, 10, 19, 24):
                rule[0][i].set_color(PURPLE)
            tag = T("(107)", 28, DIM)
            rg = VGroup(rule, tag).arrange(RIGHT, buff=0.45).move_to([PX, 0.85, 0])
            self.rule, self.tag = rule, tag
            c.wait_until("rule")
            self.play(*appear(rule, tag, lag=0.3), run_time=1.2)
            g = rule[0]
            hl = SurroundingRectangle(VGroup(*g[10:16]), buff=0.08).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15)
            hl.set_z_index(-1)
            c.wait_until("bottom times")
            self.play(FadeIn(hl), run_time=0.8)
            c.wait_until("minus the top")
            self.play(Transform(hl, SurroundingRectangle(VGroup(*g[17:23]), buff=0.08)
                                .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)), run_time=1.0)
            c.wait_until("all over")
            self.play(Transform(hl, SurroundingRectangle(VGroup(*g[23:26]), buff=0.08)
                                .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).set_z_index(-1)), run_time=1.0)
            self.hl = hl

    # ---------------------------------------------------------------- clip 3
    def quotient(self):
        with self.say("c3.tripos.3") as c:
            p1 = mt(r"\frac{du}{dx}", "=", "1", size=44)
            p1[0][1].set_color(BLUE)
            p2 = mt(r"\frac{dv}{dx}", "=", FRAC, size=44)
            p2[0][1].set_color(PURPLE)
            VGroup(p1, p2).arrange(RIGHT, buff=0.9).move_to([PX, -0.65, 0])
            self.play(FadeOut(self.hl), *appear(p1), run_time=1.0)
            c.wait_until("the bottom's")
            self.play(*appear(p2), run_time=1.0)

            plug = mt(r"\dfrac{\sqrt{1 + x^2} - \dfrac{x^2}{\sqrt{1 + x^2}}}{1 + x^2}", size=44)
            clear = mt(r"\times\dfrac{\sqrt{1 + x^2}}{\sqrt{1 + x^2}}", size=42, color=YELLOW)
            VGroup(plug, clear).arrange(RIGHT, buff=0.6).move_to([PX, -2.65, 0])
            c.wait_until("plug")
            self.play(*appear(plug, shift=None), run_time=1.2)
            c.wait_until("clear")
            self.play(*appear(clear), run_time=1.0)

            one = mt(r"\dfrac{(1 + x^2) - x^2}{(1 + x^2)^{3/2}}", size=44)
            power = mt("=", r"\dfrac{1}{(1 + x^2)^{3/2}}", size=44)
            VGroup(one, power).arrange(RIGHT, buff=0.3).move_to([PX, -2.65, 0])
            c.wait_until("one")
            self.play(*swap(VGroup(plug, clear), one), run_time=1.2)
            o = one[0]
            s1 = Line(o[3].get_corner(DL), o[4].get_corner(UR) + 0.05 * RIGHT).set_stroke(YELLOW, 4)
            s2 = Line(o[6].get_corner(DL), o[8].get_corner(UR) + 0.05 * RIGHT).set_stroke(YELLOW, 4)
            c.wait_until("leaves just one")
            self.play(Create(s1), Create(s2), run_time=1.0)
            c.wait_until("power")
            self.play(*appear(power, shift=None), run_time=1.2)

            # {so}: the panel's result flies into the main line
            main = self.main
            mid = mt(r"\cos y\,", r"\dfrac{dy}{dx}", "=", r"\dfrac{1}{(1 + x^2)^{3/2}}", size=MAIN_SIZE)
            mid[1].set_color(GREEN)
            mid.shift(main[0].get_center() - mid[0].get_center())
            c.wait_until("so")
            self.play(*during([FadeOut(main[3]), FadeOut(p1), FadeOut(p2)], 0, 0.4),
                      *during(fly(power[1], mid[3], arc=-PI / 5), 0.3, 1.0), run_time=1.6)
            self.remove(*main.get_family())
            self.remove(*mid[3].get_family())
            self.add(mid)

            end = final_line()
            box = self.box
            leaving = [self.sine, self.yx, self.divider, self.rule, self.tag, one, s1, s2, power]
            self.play(*during([FadeOut(m) for m in leaving], 0, 0.5),
                      *during([Transform(mid, end)], 0.35, 1.0), run_time=1.8)
            self.remove(*mid.get_family())
            self.add(end)
            c.wait_until()
        self.wait(1.0)
