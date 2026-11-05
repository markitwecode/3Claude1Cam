"""Chapter 1, scene 6: the dictionary, valid for every complex x. Clips c1.dict.1 – c1.dict.3.

Opens on ch1_s5_sinix's handover shot (ch1_s4_cosix.dictionary_card(rows=3), small, top-right) and
grows it to the full card. `part2_formula()` is the Part 2 preview's cosh^2 x ? sinh^2 x = 1,
for ch1_s7_recap to reuse on {twin}.
"""
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

S4 = load_scene("ch1_s4_cosix")
ctex, at_glyph, words_var, dictionary_card = S4.ctex, S4.at_glyph, S4.words_var, S4.dictionary_card


def part1_formula(size=44):
    """cos^2 x + sin^2 x = 1, BLUE."""
    return ctex(r"\cos^2 x + \sin^2 x = 1", "BBBBB F BBBBB BB", size=size)


def part2_formula(size=44):
    """cosh^2 x ? sinh^2 x = 1: TEAL, the '?' YELLOW (glyph 6). Reused by ch1_s7_recap."""
    return ctex(r"\cosh^2 x \;?\; \sinh^2 x = 1", "TTTTTT Y TTTTTT TT", size=size)


class Dictionary(NarratedScene):
    def construct(self):
        card = dictionary_card(rows=3)            # s5's last frame
        self.add(card)
        self.card = card
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)                            # let Part 4 settle before the fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1.dict.1
    def clip1(self):
        card = self.card
        full = dictionary_card(rows=3, full=True)
        with self.say("c1.dict.1") as c:
            self.play(card.animate.scale(1.5).move_to(full.get_center()),
                      run_time=min(2.0, c.until("all")))
            c.wait_until("all")
            self.play(FlashAround(card.header, run_time=2, time_width=1.5),
                      card.header.animate.scale(1.08), run_time=1.0)
            self.play(card.header.animate.scale(1 / 1.08), run_time=0.6)
            c.wait_until("Nothing in the working")
            self.play(card.animate.move_to([0, 3.55 - card.height / 2, 0]), run_time=1.2)

            xdef = ctex(r"x = 1 + 2i", "FFGFGP", size=48)
            xdef.move_to([0, -0.9, 0])
            eq1 = ctex(r"\cos\big(i(1 + 2i)\big) \approx -0.642 + 1.069i",
                       "BBBFPFGFGPFF F FFFFFFFFFFFFF", size=48)
            eq2 = ctex(r"\cosh(1 + 2i) \approx -0.642 + 1.069i",
                       "TTTTFGFGPF F FFFFFFFFFFFFF", size=48)
            at_glyph(eq1, 12, 0.2, -1.8)
            at_glyph(eq2, 10, 0.2, -2.7)
            self.check = VGroup(xdef, eq1, eq2)
            c.wait_until("check")
            self.play(*appear(xdef), run_time=1.0)
            c.wait_until("one plus two eye")
            self.play(*appear(eq1, shift=None), run_time=1.0)
            c.wait_until("Work out both sides")
            self.play(*appear(eq2, shift=None), run_time=1.0)
            vals = list(eq1[0][13:]) + list(eq2[0][11:])
            self.play(*recolor(vals, GREEN),
                      FlashAround(VGroup(*eq1[0][13:]), color=GREEN, time_width=1.5),
                      FlashAround(VGroup(*eq2[0][11:]), color=GREEN, time_width=1.5),
                      run_time=min(1.5, c.until(floor=0.5)))

    # ------------------------------------------------------------ c1.dict.2
    def clip2(self):
        card = self.card
        r1, r2, r3 = card.rows
        with self.say("c1.dict.2") as c:
            tick = check_mark().next_to(r1.num, RIGHT, buff=0.45)
            noi = words_var("no", "i", size=32, color=GREEN).next_to(tick, RIGHT, buff=0.22)
            self.play(*appear(tick, noi, lag=0.4), run_time=1.2)
            c.wait_until("extrai")
            pinks = [r2.tex[0][8], r3.tex[0][8]]
            self.play(*disappear(self.check),
                      *[FlashAround(p, color=PINK, time_width=1.5) for p in pinks],
                      *[p.animate.scale(1.25) for p in pinks], run_time=1.2)
            self.play(*[p.animate.scale(1 / 1.25) for p in pinks], run_time=0.6)

            b1 = ctex(r"\cosh x = \cos(ix)", "TTTTF F BBBFPFF", size=52)
            b2 = ctex(r"\sinh x = -i \sin(ix)", "TTTTF F PP BBBFPFF", size=52)
            at_glyph(b1, 5, -0.6, -1.55)
            at_glyph(b2, 5, -0.6, -2.8)
            # "the same card, read right to left": a tag with a left-pointing arrow
            larrow = Arrow(1.3 * RIGHT, ORIGIN, buff=0, color=YELLOW, stroke_width=4,
                           max_tip_length_to_length_ratio=0.3)
            tag = T("read backwards", size=30, color=YELLOW)
            flip = VGroup(larrow, tag).arrange(RIGHT, buff=0.25).move_to([-0.6, -0.8, 0])
            c.wait_until("back")
            self.play(GrowArrow(larrow), *appear(tag, shift=None), run_time=1.2)
            c.wait_until("Cosh of ex")
            self.play(*appear(b1, shift=None), run_time=1.2)
            c.wait_until("back2")
            self.play(*appear(b2, shift=None), run_time=1.2)
            self.play(FlashAround(VGroup(*b2[0][6:8]), color=PINK, time_width=1.5), run_time=1.2)
            self.back = VGroup(tick, noi, flip, b1, b2)

    # ------------------------------------------------------------ c1.dict.3
    def clip3(self):
        card = self.card
        with self.say("c1.dict.3") as c:
            boxes = VGroup(*[RoundedRectangle(corner_radius=0.2, width=6.3, height=4.3,
                                              stroke_color=DIM, stroke_width=2)
                             for _ in range(2)]).arrange(RIGHT, buff=0.5).move_to([0, -1.3, 0])
            lb, rb = boxes
            self.play(*during(disappear(self.back), 0, 0.45),
                      *during([card.animate.scale(1 / 1.5).move_to([0, 3.6 - card.height / 3, 0])],
                              0.2, 0.8),
                      *during([FadeIn(lb), FadeIn(rb)], 0.5, 1),
                      run_time=min(2.0, c.until("ident")))

            # Part 2
            t2 = T("Part 2", size=34, color=YELLOW).move_to(lb.get_top() + 0.5 * DOWN)
            f1 = part1_formula().move_to(lb.get_center() + 0.45 * UP)
            f2 = part2_formula().move_to(lb.get_center() + 1.35 * DOWN)
            a2 = Arrow(f1.get_bottom() + 0.1 * DOWN, f2.get_top() + 0.1 * UP, buff=0.05,
                       color=DIM, stroke_width=4)
            c.wait_until("ident")
            self.play(*appear(t2, f1, lag=0.4), run_time=1.2)  # early: section title shown with its first formula
            c.wait_until("becomes one for cosh")
            self.play(GrowArrow(a2), *appear(f2, shift=None), run_time=1.5)
            c.wait_until("sometimes with a sign flipped")
            self.play(FlashAround(f2[0][6], run_time=1.5, time_width=1.5),
                      f2[0][6].animate.scale(1.3), run_time=1.0)
            self.play(f2[0][6].animate.scale(1 / 1.3), run_time=0.6)

            # Part 4
            t4 = T("Part 4", size=34, color=YELLOW).move_to(rb.get_top() + 0.5 * DOWN)
            cxy = ctex(r"\cos(x + iy)", "BBBFFFPPF", size=48).move_to(rb.get_center() + 0.85 * UP)
            xg, iyg = cxy[0][4], VGroup(*cxy[0][6:8])
            re = T("real part", size=30, color=FG)
            im = T("imaginary part", size=30, color=PINK)
            re.move_to([rb.get_x() - 2.6 + re.width / 2, rb.get_center()[1] - 0.35, 0])
            im.move_to([rb.get_x() + 2.6 - im.width / 2, rb.get_center()[1] - 0.35, 0])
            ar = Arrow(xg.get_bottom(), re.get_top(), buff=0.12, color=FG, stroke_width=4,
                       max_tip_length_to_length_ratio=0.3)
            ai = Arrow(iyg.get_bottom(), im.get_top(), buff=0.12, color=PINK, stroke_width=4,
                       max_tip_length_to_length_ratio=0.3)
            cz = ctex(r"\cos z = 2", "BBBF FG", size=48).move_to(rb.get_bottom() + 0.75 * UP)
            c.wait_until("split")
            self.play(*appear(t4, cxy, lag=0.4), run_time=1.2)  # early: section title shown with its formula
            c.wait_until(own_word=re)
            self.play(GrowArrow(ar), *appear(re), run_time=1.0)
            c.wait_until(own_word=im)
            self.play(GrowArrow(ai), *appear(im), run_time=1.0)
            c.wait_until("That's Part four")
            self.play(*appear(cz), run_time=1.0)
            c.wait_until("where you'll find")
            self.play(FlashAround(cz, run_time=1.5, time_width=1.5), run_time=1.5)
