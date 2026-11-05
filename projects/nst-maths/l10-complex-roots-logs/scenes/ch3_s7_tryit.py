"""Chapter 3, scene 7: three questions on Examples Sheet I (F12, F13, F17), each with a hint grown
out of an icon from ch2/ch3. Clips c3.try.1 – c3.try.3.

Cards match ch6_s6_recap's examples-sheet cards (T 44 title with the question number YELLOW, DIM rule,
the question verbatim below). Icons reused via load_scene: ch2_s2 ray(), ch3_s2 pair()/plane(),
ch3_s3 argand_plane()/unit_chain(), ch3_s4 lam_flag(). Ends on an empty frame.
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

THM = load_scene("ch2_s2_theorem")      # ray(), argand_plane()
CUBE = load_scene("ch3_s2_cube")        # pair(), plane()
EXPO = load_scene("ch2_s6_expo")        # arrow_between()
SUM = load_scene("ch3_s3_sum")          # argand_plane(), unit_chain()
GEO = load_scene("ch3_s4_geometric")    # lam_flag()

TITLE_Y, RULE_Y = 3.35, 2.95
CARD_X = -6.4                           # left edge of the question text


def title_for(q=None):
    """The bare title, or (prefix, tag): the tag is its own Text so it can be swapped whole."""
    if q is None:
        return T("Examples Sheet I", 44).move_to([0, TITLE_Y, 0])
    pre = T("Examples Sheet I  ·", 44)
    tag = T(q, 44, YELLOW).next_to(pre, RIGHT, buff=0.4).align_to(pre[-2], DOWN)   # on the "I" baseline
    VGroup(pre, tag).move_to([0, TITLE_Y, 0])
    return pre, tag


def tx(*parts, size=44, color=FG):
    return Tex(*parts, font_size=size, color=color)


def mtx(*parts, size=44, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def card_lines(*lines, top=2.35, pitch=0.68):
    for k, ln in enumerate(lines):
        ln.move_to([0, top - k * pitch, 0]).align_to([CARD_X, 0, 0], LEFT)
    return lines


def diff_purple(th, k, center, unit):
    """s2's mirror pair turned into a difference: from e^{ikθ}, add -e^{-ikθ}; lands on 2i sin kθ."""
    e = np.exp(1j * k * th)
    end = 2j * e.imag
    arr = EXPO.arrow_between(CUBE.P(e, center, unit), CUBE.P(end, center, unit), PURPLE)
    dot = Dot(CUBE.P(end, center, unit), radius=0.09, color=PINK)
    return arr, dot


class TryIt(NarratedScene):
    def construct(self):
        self.try_1()
        self.try_2()
        self.try_3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ============================================================ c3.try.1  F12
    def try_1(self):
        with self.say("c3.try.1", gap=1.8) as c:
            title = title_for()
            rule = Line(LEFT * 3.4, RIGHT * 3.4, color=DIM, stroke_width=2).move_to([0, RULE_Y, 0])
            tags = [T(q, 56, YELLOW).move_to([x, 0, 0]) for q, x in (("F12", -3.6), ("F13", 0), ("F17", 3.6))]
            self.play(*appear(title, shift=None), GrowFromCenter(rule),  # early: the sheet's title card
                      *during(appear(*tags, lag=0.3), 0.3, 1), run_time=1.6)

            # {f12}: the card
            pre12, tag12 = title_for("F12")
            q_i = tx(r"Express: \ i. $\sin 3\theta$ in terms of powers of $\sin\theta$; and")
            q_ii = tx(r"ii. $\sin^5\theta$ in terms of $\sin\theta$, $\sin 2\theta$, $\sin 3\theta$ etc.")
            card_lines(q_i, q_ii)
            c.wait_until("f12")
            self.play(*during(disappear(*tags), 0, 0.4), *during(edit(title, pre12), 0.3, 0.7),
                      *during(appear(tag12, shift=None), 0.5, 0.8),
                      *during(appear(q_i, q_ii, lag=0.3), 0.55, 1), run_time=2.2)  # early: the question card
            title = VGroup(pre12, tag12)
            settle(self, title)

            # De Moivre: ch2's unit arrow at 3θ
            pc, pu = np.array([-4.7, -1.35, 0]), 1.3
            pl = THM.argand_plane(center=pc, unit=pu, extent=1.7)
            arr = THM.ray(75, center=pc, unit=pu)
            arc = Arc(radius=0.5, start_angle=0, angle=np.deg2rad(75), arc_center=pc, color=YELLOW,
                      stroke_width=4)
            th3 = mtx(r"3\theta", size=36, color=YELLOW).move_to(pc + 0.85 * np.array([np.cos(0.65), np.sin(0.65), 0]))
            c.wait_until("use De")
            self.play(*appear(pl, shift=None), GrowArrow(arr), run_time=1.2)
            self.play(Create(arc), *appear(th3, shift=None), run_time=0.8)

            a_line = mtx(r"\mathrm{Im}", r"\,(\cos\theta + i\sin\theta)^3", size=56)
            a_line[0].set_color(PINK)
            a_line.move_to([1.3, -0.5, 0])
            c.wait_until("with the power")
            self.play(*fly(arr, a_line[1]), run_time=min(1.5, 0.9 * c.until("imaginary part")))
            c.wait_until("imaginary part")
            self.play(*appear(a_line[0], shift=None), FlashAround(a_line[0], run_time=1.2), run_time=1.2)

            b_line = mtx(r"\cos^2\theta", "=", r"1 - \sin^2\theta", size=56)
            b_line.next_to(a_line, DOWN, buff=0.75).align_to(a_line[1], LEFT)
            c.wait_until("Then replace")
            self.play(*appear(b_line), run_time=1.2)

            # {f12b}: hint (ii) on a fresh board
            s5 = mtx(r"\sin^5\theta", "=", r"\Big[", r"\frac{e^{i\theta} - e^{-i\theta}}{2i}", r"\Big]^5", size=56)
            s5.move_to([0, 0.55, 0])
            c.wait_until("f12b")
            sweep_clear(self, *set_alpha([q_i], 0.4), time_span(FadeIn(s5), 0.6, 1.2),
                        keep=[title, rule, q_i, q_ii])

            nums = ["1", "5", "10", "10", "5", "1"]
            row = VGroup(*[mtx(n, size=48, color=GOLD) for n in nums]).arrange(RIGHT, buff=0.7)
            row.move_to([0, -0.85, 0])
            c.wait_until("fifth power")
            self.play(*appear(*row, shift=None, lag=0.12), run_time=1.1)

            # pair the mirror terms (s2's picture, as a sum first)
            mc, mu = np.array([-5.0, -2.2, 0]), 0.68
            mpl = CUBE.plane(mc, mu, 1.4)
            mpl[4].set_opacity(0); mpl[5].set_opacity(0)    # no Re/Im tags: the pair sits on them
            th = 14 * DEGREES                                # the ±5θ pair, 5θ = 70°
            gold, purple, bdot = CUBE.pair(th, 5, mc, mu)
            arcs = VGroup(*[ArcBetweenPoints(row[i].get_bottom() + 0.1 * DOWN, row[5 - i].get_bottom() + 0.1 * DOWN,
                                             angle=PI / 2, color=YELLOW, stroke_width=3) for i in range(3)])
            c.wait_until("mirror terms")
            self.play(*appear(mpl, shift=None), GrowArrow(gold), *[Create(a) for a in arcs], run_time=1.3)
            self.play(GrowArrow(purple), FadeIn(bdot, scale=0.5), run_time=1.0)

            # {difference}: the purple arrow flips; the pair lands on the imaginary axis
            p2, d2 = diff_purple(th, 5, mc, mu)
            lab = mtx(r"2i\sin 5\theta", size=34, color=PINK).next_to(d2, UP, buff=0.15)
            set_backstroke(lab, width=5)
            d_line = mtx(r"e^{5i\theta}", "-", r"e^{-5i\theta}", "=", r"2i\sin 5\theta", size=54)
            d_line[0].set_color(GOLD)
            d_line[2].set_color(PURPLE)
            d_line[4].set_color(PINK)
            d_line.move_to([2.6, -2.95, 0])
            c.wait_until("difference")
            self.play(*during([ReplacementTransform(purple, p2), ReplacementTransform(bdot, d2)], 0, 0.5),
                      *during(appear(lab, d_line, lag=0.3), 0.45, 1), run_time=min(2.4, c.until(floor=0.5)))
        self.wait(2.5)                                       # hold the F12(ii) result before the clear
        self.title, self.rule = title, rule

    def next_tag(self, title, rule, q):
        """Clear the board (all at once, no lagged stragglers), then swap the whole question tag."""
        pre, tag = title
        _, new_tag = title_for(q)
        board = [m for m in self.mobjects if m not in (title, pre, tag, rule)]
        self.play(*during(disappear(*board), 0, 0.5), *during(swap(tag, new_tag), 0.45, 1), run_time=1.4)
        title = VGroup(pre, new_tag)
        settle(self, title)
        return title

    # ============================================================ c3.try.2  F13
    def try_2(self):
        title, rule = self.title, self.rule
        with self.say("c3.try.2", gap=1.0) as c:
            title = self.next_tag(title, rule, "F13")

            head = tx(r"Evaluate the following sums:")
            card_lines(head)
            sums = [mtx(r"\text{(a)}\;\;", r"\sum_{n=1}^{5} \cos n\theta", size=46),
                    mtx(r"\text{(b)}\;\;", r"\sum_{n=1}^{5} \sin n\theta", size=46),
                    mtx(r"\text{(c)}\;\;", r"\sum_{n=1}^{5} r^n \cos n\theta", size=46)]
            for s, y in zip(sums, (1.0, -0.8, -2.6)):
                s.move_to([0, y, 0]).align_to([CARD_X, 0, 0], LEFT)
            self.play(*appear(head, *sums, shift=None, lag=0.25), run_time=1.6)  # early: the question card

            # {first}: Re of a geometric progression; s3's chain, five arrows from e^{iθ}
            re_a = mtx("=", r"\mathrm{Re}", r"\sum_{n=1}^{5} e^{in\theta}", size=46)
            re_a[1].set_color(BLUE)
            re_a.next_to(sums[0], RIGHT, buff=0.3)
            c.wait_until("first")
            self.play(*appear(re_a, shift=None), run_time=1.1)

            th = PI / 6
            o, u = np.array([1.05, -3.3, 0]), 1.02
            pl = SUM.argand_plane(origin=o, unit=u, xr=(-0.5, 1.95), yr=(-0.15, 3.85))
            chain = SUM.unit_chain(5, th, start=th, origin=o, unit=u)
            c.wait_until("geometric progression")
            self.play(*appear(pl, shift=None), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in chain], lag_ratio=0.6), run_time=1.6)

            lx = 3.3
            l1 = mtx(r"\text{first term }", r"e^{i\theta}", size=42)
            l2 = mtx(r"\text{ratio }", r"e^{i\theta}", size=42)
            l3 = mtx(r"\text{five terms}", size=42)
            for m, y in zip((l1, l2, l3), (0.5, -0.4, -1.3)):
                m[-1].set_color(GOLD) if len(m) > 1 else None
                m.move_to([0, y, 0]).align_to([lx, 0, 0], LEFT)
            c.wait_until("first term")
            self.play(*appear(l1), FlashAround(chain[0], run_time=1.2), run_time=1.2)
            self.play(*appear(l2, l3, lag=0.4), run_time=1.2)  # early: the GP's other data, read off the chain

            # {second}: Im of the same sum
            im_b = mtx("=", r"\mathrm{Im}", r"\sum_{n=1}^{5} e^{in\theta}", size=46)
            im_b[1].set_color(PINK)
            im_b.next_to(sums[1], RIGHT, buff=0.3)
            c.wait_until("second")
            self.play(*appear(im_b, shift=None), run_time=1.1)

            # {third}: ratio r e^{iθ}, the chain becomes a spiral
            rat_c = mtx(r"\text{ratio }", r"r\,e^{i\theta}", size=44)
            rat_c[1].set_color(GOLD)
            rat_c.next_to(sums[2], RIGHT, buff=0.45)
            spiral = SUM.unit_chain(5, th, start=th, r=0.78, origin=o, unit=u)
            c.wait_until("common ratio")
            self.play(*appear(rat_c), run_time=1.0)
            self.play(*[Transform(a, b) for a, b in zip(chain, spiral)], run_time=min(2.0, c.until(floor=0.5)))
        self.title = title

    # ============================================================ c3.try.3  F17
    def try_3(self):
        title, rule = self.title, self.rule
        with self.say("c3.try.3") as c:
            title = self.next_tag(title, rule, "F17")

            q1 = tx(r"If $\omega^3 = 1$, find all values of ", r"$1 + \omega + \omega^2$", r".")
            q2 = tx(r"Generalise your result to the case $\omega^n = 1$")
            q3 = tx(r"for $n$ a positive integer.")
            card_lines(q1, q2, q3)
            self.play(*appear(q1, q2, q3, shift=None, lag=0.25), run_time=1.5)  # early: the question card

            hero = mtx("1", "+", r"\omega", "+", r"\omega^2", size=64)
            hero.move_to([0, -0.45, 0])
            c.wait_until("One plus")
            self.play(FlashAround(q1[1], run_time=1.2), *during(appear(hero, shift=None), 0.3, 1), run_time=1.5)

            brace = Brace(Line(hero.get_corner(DL), hero.get_corner(DR)), DOWN, buff=0.2, color=DIM)
            gp = mtx(r"\text{geometric progression, ratio }", r"\omega", size=42)
            gp[1].set_color(GOLD)
            gp.next_to(brace, DOWN, buff=0.2)
            c.wait_until("geometric progression")
            self.play(GrowFromCenter(brace), *appear(gp), run_time=1.2)

            flag = GEO.lam_flag(text=r"\omega = 1\ ?").scale(1.4).move_to([3.9, -2.6, 0])
            c.wait_until("careful")
            self.play(*appear(flag), run_time=1.0)
            c.wait_until("exception")
            self.play(FlashAround(flag, color=RED, run_time=1.4, time_width=1.5), run_time=1.4)

            # {general}
            hero_n = mtx("1", "+", r"\omega", "+", r"\omega^2", "+", r"\cdots", "+", r"\omega^{n-1}", size=64)
            hero_n.move_to([0, -0.45, 0])
            c.wait_until("general")
            a0, b0 = hero.get_corner(DL), hero.get_corner(DR)
            a1, b1 = hero_n.get_corner(DL), hero_n.get_corner(DR)

            def grow(m, t):                                  # the brace widens with the expression
                m.become(Brace(Line(interpolate(a0, a1, t), interpolate(b0, b1, t)), DOWN, buff=0.2, color=DIM))
            self.play(*during(edit(hero, hero_n), 0, 0.75),
                      *during([UpdateFromAlphaFunc(brace, grow, rate_func=smooth)], 0, 0.75),
                      FlashAround(q2, run_time=1.6, time_width=1.5), run_time=1.6)

            part8 = T("Full solutions: Part 8", 32, DIM).move_to([0, -3.4, 0])
            c.wait_until(own_word=part8, cue="solutions")
            self.play(*appear(part8), run_time=0.9)
        self.wait(4.0)
