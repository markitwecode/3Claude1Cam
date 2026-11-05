"""Chapter 6, scene 1: Spoiler warning, the five exercises and the routine. Clips c6.intro.1 – c6.intro.2.

Shared drawing:
  pause_icon(color=GOLD) -> VGroup of two RoundedRectangles 0.16 x 0.6 (corner 0.05, fill 1), gap 0.16
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
from lib.titles import title_card  # noqa: E402

S4 = load_scene("ch5_s4_bacon")
S7 = load_scene("ch5_s7_exercises")
S8 = load_scene("ch5_s8_recap")

ROW_S = 1.2
ROW_UP = 2.1          # where the row rises to for the routine


def pause_icon(color=GOLD):
    bars = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.16, height=0.6)
                    .set_stroke(color, 0).set_fill(color, 1) for _ in range(2)])
    bars.arrange(RIGHT, buff=0.16)
    return bars


def last_time_strip():
    h = S4.bacon_histogram(max_h=4.6, with_xlabel=False)
    h.remove(*h.values, *h.ticks)
    h.scale_to_fit_width(3.9)
    langs = VGroup(T("Cypher", 32, color=BLUE), T("GQL", 32, color=BLUE), T("SQL/PGQ", 32, color=BLUE))
    langs.arrange(RIGHT, buff=0.55)
    strip = VGroup(h, langs).arrange(RIGHT, buff=1.2, aligned_edge=DOWN)
    strip.move_to((0, 0, 0)).align_to((0, -3.45, 0), DOWN)
    strip.hist, strip.langs = h, langs
    return strip


def banner():
    rect = RoundedRectangle(corner_radius=0.15, width=13.0, height=2.1).set_stroke(GOLD, 3).set_fill(BG, 0.94)
    icon = pause_icon().scale(2.0)
    word = T("SPOILERS AHEAD", 60, color=GOLD)
    VGroup(icon, word).arrange(RIGHT, buff=0.6).move_to(rect)
    g = VGroup(rect, icon, word)
    g.rect, g.icon, g.word = rect, icon, word
    return g


class Intro(NarratedScene):
    def construct(self):
        self.add(S8.end_card())
        self.wait(1.0)   # hold ch5's end card before the voice starts

        # ------------------------------------------------------------ c6.intro.1
        with self.say("c6.intro.1") as c:
            card = title_card("Part 6 · Solutions to the exercises")
            card.shift(0.6 * UP)
            sweep_clear(self, FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                        run_time=1.4)
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.2)   # early: title card

            strip = last_time_strip()
            c.wait_until("Bacon")
            self.play(*[FadeIn(m, shift=0.15 * UP) for m in strip.hist], run_time=1.0)
            self.play(*set_alpha([strip.hist], 0.5), run_time=0.6)
            c.wait_until("languages")
            self.play(*appear(*strip.langs, lag=0.25), run_time=1.0)   # early: names of the languages said
            self.play(*set_alpha([strip.langs], 0.5), run_time=0.6)

            row = S7.exercise_cards().scale(ROW_S).move_to(ORIGIN)
            qs = VGroup(*[T("?", 56, color=GOLD).next_to(cd, DOWN, buff=0.45) for cd in row])
            c.wait_until("cards")
            sweep_clear(self, *[time_span(FadeIn(cd, shift=0.2 * UP), 0.8 + 0.12 * i, 1.4 + 0.12 * i)
                                for i, cd in enumerate(row)], keep=[strip], run_time=1.9)
            self.play(*appear(*qs, lag=0.2), run_time=1.2)

            ban = banner()
            c.wait_until("warn")
            self.play(*set_alpha([cd.box for cd in row] + list(qs), DIMMED),
                      *during([cd.num.animate.set_opacity(0) for cd in row], 0, 0.4),
                      *during([FadeIn(ban.rect)], 0.2, 0.7),
                      *during([GrowFromCenter(ban.icon)], 0.4, 1.0),
                      *during([FadeIn(ban.word, shift=0.2 * DOWN)], 0.45, 1.0),
                      run_time=1.6)
            self.play(*flash([ban.word], color=GOLD), run_time=1.5)

        # ------------------------------------------------------------ c6.intro.2
        with self.say("c6.intro.2") as c:
            self.play(*disappear(ban, *strip), run_time=0.8)
            self.play(*set_alpha([cd.box for cd in row] + list(qs), 1),
                      *[cd.num.animate.set_opacity(1) for cd in row], run_time=0.6)
            self.play(row.animate.shift(ROW_UP * UP), qs.animate.shift(ROW_UP * UP), run_time=1.2)
            first = row[0]
            self.play(first.box.animate.set_stroke(YELLOW, 4), first.num.animate.set_color(YELLOW),
                      qs[0].animate.set_color(YELLOW), run_time=0.8)

            x0 = first.get_left()[0]
            s1 = VGroup(T("pause", 40), pause_icon().scale(0.75))
            s1.arrange(RIGHT, buff=0.3)
            s2 = T("build it", 40)
            s3 = T("run it on the real database", 40)
            steps = [s1, s2, s3]
            nums = []
            for i, s in enumerate(steps):
                n = T(f"{i + 1}.", 40, color=DIM)
                s.next_to(n, RIGHT, buff=0.3)
                VGroup(n, s).move_to((0, -0.45 - 1.1 * i, 0)).align_to((x0, 0, 0), LEFT)
                nums.append(n)

            c.wait_until(own_word=s1[0])
            self.play(*appear(nums[0], s1, lag=0.2), run_time=1.0)
            c.wait_until(own_word=s2)
            self.play(*appear(nums[1], s2, lag=0.2), run_time=1.0)
            c.wait_until(own_word=s3)
            self.play(*appear(nums[2], s3, lag=0.2), run_time=1.0)

            box = RoundedRectangle(corner_radius=0.2, width=3.4, height=2.6).set_stroke(RED, 4).set_fill(BG, 1)
            cross = cross_mark().scale(1.4)
            word = T("the trap", 44, color=RED)
            VGroup(cross, word).arrange(DOWN, buff=0.4).move_to(box)
            trap = VGroup(box, cross, word)
            trap.move_to((4.6, -1.55, 0))
            c.wait_until("trap")
            self.play(FadeIn(trap, shift=1.2 * LEFT), run_time=1.2)
            c.wait_until("wrong answer")
            self.play(FlashAround(trap, color=RED, run_time=1.5, time_width=1.5))

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
