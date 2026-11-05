"""Chapter 7, scene 1: spoiler warning, then the four exercises, the routine, the test lists.
Clips c7.intro.1 – c7.intro.2.

Opens on ch6's end card (`open_card()`: ch6 s4's `four_cards()` row with its note, static), held
0.7 s, cleared to the title card on {title}. {warn}: title and rule lift away, course and part
lines rise as the header, GOLD "SPOILERS AHEAD" banner with a big ‖. {cards}: the same row at its
default place (no note); {two}: YELLOW "selection sort" / "bubble sort" over the pairs; {ritual}:
three steps under card 5.1; {test}: `test_chains()` beside them; {wrong}: the steps give way to a
RED ✗ "tempting bugs" card, the repeats list gets a RED outline. Ends on an empty frame.

Exports: open_card() (for ch6 s6 to end on), test_chains() (for the recap).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402
from scenes.ch6_s4_hints1 import CARD_FILL, four_cards, hold_for, pause_icon  # noqa: E402  (the shared kit)

HEADER_Y = 2.65      # the part line, kept as the header (as L4's bonus) ...
TOP_Y = 3.0          # ... rising to the kit's header height when the cards arrive
COURSE_Y = 3.28      # the course line rides above it until the cards arrive
PAIR_Y = 1.72        # "selection sort" / "bubble sort" over the pairs (card tops at 1.2)
STEPS_L = -6.4       # the ritual's left edge, under card 5.1
STEPS_TOP = -1.2
CHAIN_X = 2.4        # the two test chains, beside the steps
CHAIN_YS = (-1.6, -2.75)
CHAIN_S = 0.68
RUNNING = [3, 5, 9, 4, 7]
REPEATS = [3, 5, 3, 1, 5]


def open_card():
    """ch6's end card, exactly as ch6 s4 draws it at {bonus}: the four dim BigCards in one row
    (3.1 x 2.0 each, buff 0.2, centred at y 0.2: x -6.5..6.5, y -0.8..1.2) and the DIM note
    "Solutions: bonus chapter" (T 34, "bonus chapter" YELLOW) at (0, -2.1). Static."""
    return four_cards()


def test_chains():
    """The two test lists of {test}: running 3 5 9 4 7 [] over repeats 3 5 3 1 5 [] (its 3s and
    5s YELLOW), ConsChain x0.68, centred at x 2.4, y -1.6 and -2.75. VGroup(running, repeats)."""
    running = ConsChain(RUNNING)
    repeats = ConsChain(REPEATS)
    for cell, v in zip(repeats.cells, REPEATS):
        if v in (3, 5):
            cell.label.set_color(YELLOW)
    g = VGroup(running, repeats)
    for ch, y in zip(g, CHAIN_YS):
        ch.scale(CHAIN_S).move_to([CHAIN_X, y, 0])
    g.running, g.repeats = running, repeats
    return g


class SolutionsIntro(NarratedScene):
    def construct(self):
        self.warning()
        self.routine()
        hold_for(self, self.wrong_born, len("tempting bugs"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # intro.1: ch6's end card gives way to the title card, then the spoiler banner
    def warning(self):
        opening = open_card()
        self.add(opening)
        self.wait(0.7)

        card = title_card("Bonus · Solutions to the exercises")
        icon = pause_icon(color=GOLD, h=1.4)
        words = T("SPOILERS AHEAD", size=56, color=GOLD, weight=BOLD)
        inner = VGroup(icon, words).arrange(RIGHT, buff=0.7)
        frame = RoundedRectangle(corner_radius=0.3, width=inner.width + 1.6, height=2.7)
        frame.set_stroke(GOLD, 4).set_fill(GOLD, 0.08)
        banner = VGroup(frame, inner).move_to(DOWN * 0.55)
        inner.move_to(frame)

        with self.say("c7.intro.1") as c:
            # "This bonus chapter for lecture five has worked solutions to the four exercises ..."
            sweep_clear(self, FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                        run_time=1.6)  # early: the chapter title
            c.wait_until("lecture five")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)  # early: the title card's course line
            c.wait_until("worked solutions")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

            # "Everything from here on is a spoiler."
            c.wait_until("warn")
            self.play(
                *[time_span(FadeOut(m, shift=0.4 * UP), 0, 0.6) for m in (card.title, card.rule)],
                time_span(card.course.animate.scale(0.9).move_to(UP * COURSE_Y), 0.55, 1.4),
                time_span(card.part.animate.scale(1.2).move_to(UP * HEADER_Y), 0.55, 1.4),
                time_span(FadeIn(banner, scale=0.92), 0.9, 1.8),
                run_time=1.8,
            )

            # "If you'd like to try them first, stop the video now, and have a go."
            c.wait_until("stop the video")
            self.play(FlashAround(icon, color=GOLD, time_width=1.5, buff=0.25,
                                  run_time=min(2.0, max(1.0, c.remaining - 0.1))))
        self.header, self.course, self.banner = card.part, card.course, banner

    # intro.2: the four cards, the two sorts, the routine, the test lists, the bugs
    def routine(self):
        cards = four_cards().cards               # the kit's row at its default place

        def pair_label(text, i):
            left, right = cards[i].get_left()[0], cards[i + 1].get_right()[0]
            rule = Line([left + 0.1, PAIR_Y - 0.3, 0], [right - 0.1, PAIR_Y - 0.3, 0])
            rule.set_stroke(YELLOW, 2.5)
            lab = T(text, size=36, color=YELLOW).move_to([(left + right) / 2, PAIR_Y, 0])
            return lab, rule

        sel_lab, sel_rule = pair_label("selection sort", 0)
        bub_lab, bub_rule = pair_label("bubble sort", 2)

        s1 = VGroup(T("pause", size=32), pause_icon(h=0.32)).arrange(RIGHT, buff=0.2)
        s2 = T("solve", size=32)
        s3 = T("count the comparisons", size=32, t2c={"comparisons": GOLD})
        steps = VGroup(s1, s2, s3).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        steps.move_to([STEPS_L, STEPS_TOP, 0], aligned_edge=UL)

        tests = test_chains()
        running, repeats = tests.running, tests.repeats

        lab = VGroup(cross_mark(RED), T("tempting bugs", size=32)).arrange(RIGHT, buff=0.28)
        box = RoundedRectangle(corner_radius=0.2, width=lab.width + 0.7, height=0.95)
        box.set_stroke(RED, 2.5).set_fill(CARD_FILL, 1)
        lab.move_to(box)
        wrong = VGroup(box, lab).move_to([-6.6, CHAIN_YS[1], 0], aligned_edge=LEFT)
        outline = SurroundingRectangle(repeats, color=RED, buff=0.12, corner_radius=0.1)
        outline.set_stroke(RED, 3)

        with self.say("c7.intro.2") as c:
            # "The exercises bring two new contestants,"  The banner goes; the four cards arrive.
            self.play(  # early: the four cards, each named by the labels that follow
                time_span(FadeOut(self.banner, shift=0.3 * UP), 0, 0.7),
                time_span(FadeOut(self.course, shift=0.2 * UP), 0, 0.7),
                time_span(self.header.animate.set_y(TOP_Y), 0, 0.8),
                time_span(LaggedStart(*[FadeIn(b, shift=0.3 * UP) for b in cards], lag_ratio=0.2), 0.5, 1.8),
                run_time=1.8,
            )

            # "selection sort and bubble sort, first their cost, then their code."
            c.wait_until("selection sort")
            self.play(*appear(sel_lab), GrowFromCenter(sel_rule), run_time=0.9)
            c.wait_until("bubble sort")
            self.play(*appear(bub_lab), GrowFromCenter(bub_rule), run_time=0.9)

            # "Each exercise starts with the question, and a moment to pause."
            c.wait_until("ritual")
            first = cards[0]
            self.play(first.frame.animate.set_stroke(YELLOW, 3.0), first.num.animate.set_color(YELLOW),
                      *set_alpha(cards[1:], 0.4), run_time=1.0)
            c.wait_until("a moment to pause")
            self.play(*appear(s1), run_time=0.9)

            # "Then we solve it, and count the comparisons."
            c.wait_until("solve it")
            self.play(*appear(s2), run_time=0.9)
            c.wait_until("count the comparisons")
            self.play(*appear(s3), run_time=0.9)

            # "We'll test each sort on our running list, and on a list with repeats."
            c.wait_until("running list")
            self.play(*appear(running, shift=0.2 * LEFT), run_time=1.0)
            c.wait_until("repeats")
            self.play(*appear(repeats, shift=0.2 * LEFT), run_time=1.0)

            # "Both sorts have a tempting bug, and only the repeats reveal it."
            c.wait_until("wrong")
            self.play(*during(disappear(steps), 0, 0.45),
                      *during([FadeIn(wrong, shift=0.8 * RIGHT)], 0.45, 1), run_time=1.4)
            self.wrong_born = self.time
            c.wait_until("repeats reveal")
            self.play(FadeIn(outline), run_time=0.9)
