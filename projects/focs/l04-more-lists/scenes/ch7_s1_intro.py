"""Chapter 7, scene 1: the bonus chapter opens: title card, a spoiler warning, the six exercise
cards and the routine each solution follows. Clips c7.intro.1 - c7.intro.2.

Plan (as L3's ch6_s1_intro): title card ("Bonus · Solutions to the exercises"); on {warn} title
and rule lift away, course and part lines rise to the top (the part line is the header from here
on), a GOLD "SPOILERS AHEAD" banner with a big pause icon fills the centre (flashed on "stop the
video"). On {cards} the banner and course line go, the header rises to y 3.0 (where ch6_s5's
"Exercises" sat) and the kit's six_cards() arrive in order at their native layout (BigCards
4.0 x 1.45, columns x -4.2 / 0 / 4.2, rows y 1.35 / -0.30; note "Solutions: bonus chapter" at
y -2.95), as ch6 left them. On "the question" 4.1 lights up (YELLOW frame and number, the others
dim to 0.4); the routine "|| pause -> solve -> trace and cost" grows under the rows (y -1.65).
On {wrong} a RED x card slides in on the bottom band (y -2.85) and pushes the note out (it has
been up 8 s; there is no room for both under the two rows at full size).
Hand-off: everything else fades, the cards return to rest and shrink into the kit's strip
(make_strip([TODO] * 6): left edge -6.5, y STRIP_Y 3.2; frame and number into the pill's, the
title shrinks away), held 1 s, then faded. s2-s7 open on that strip.

The cards and the pause icon come from the exercise-card kit in ch6_s5_hints1.py (read-only).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402
from scenes.ch6_s5_hints1 import (CARD_FILL, TODO, hold_for, make_strip, pause_icon,  # noqa: E402
                                  six_cards)  # the shared exercise-card kit

STEPS_Y = -1.65      # the routine, under the two rows of cards (bottom row ends at -1.025)
WRONG_Y = -2.85      # the "tempting wrong answers" card, on the note's band (y -2.95)
HEADER_Y = 2.65      # the part line, kept as the header (as L3's bonus) ...
TOP_Y = 3.0          # ... rising to ch6_s5's header height when the cards arrive
COURSE_Y = 3.28      # the course line rides above it until the cards arrive


class SolutionsIntro(NarratedScene):
    def construct(self):
        self.warning()
        self.routine()
        self.into_strip()

    # intro.1: title card, then the spoiler banner
    def warning(self):
        card = title_card("Bonus · Solutions to the exercises")

        icon = pause_icon(color=GOLD, h=1.4)
        words = T("SPOILERS AHEAD", size=56, color=GOLD, weight=BOLD)
        inner = VGroup(icon, words).arrange(RIGHT, buff=0.7)
        frame = RoundedRectangle(corner_radius=0.3, width=inner.width + 1.6, height=2.7)
        frame.set_stroke(GOLD, 4).set_fill(GOLD, 0.08)
        banner = VGroup(frame, inner).move_to(DOWN * 0.55)
        inner.move_to(frame)

        with self.say("c7.intro.1") as c:
            # "This bonus chapter for lecture four has worked solutions to the six exercises ..."
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("lecture four")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("worked solutions")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

            # "Everything from here on is a spoiler."  Course and part lines rise to the top;
            # the part line stays on as the header.
            c.wait_until("warn")
            self.play(
                LaggedStart(*[FadeOut(m, shift=0.4 * UP) for m in (card.title, card.rule)], lag_ratio=0.15),
                card.course.animate.scale(0.9).move_to(UP * COURSE_Y),
                card.part.animate.scale(1.2).move_to(UP * HEADER_Y),
                time_span(FadeIn(banner, scale=0.92), 0.5, 1.5),
                run_time=1.5,
            )

            # "If you'd like to try them first, stop the video now, and have a go."
            c.wait_until("stop the video")
            self.play(FlashAround(icon, color=GOLD, time_width=1.5, buff=0.25,
                                  run_time=min(2.0, max(1.0, c.remaining - 0.1))))
        self.header, self.course, self.banner = card.part, card.course, banner

    # intro.2: the six cards in order; the routine; tempting wrong answers
    def routine(self):
        ex = six_cards()                      # native layout, exactly as the kit builds it
        cards, note = ex.cards, ex.note

        s1 = VGroup(pause_icon(h=0.36), T("pause", size=36)).arrange(RIGHT, buff=0.2)
        s2 = T("solve", size=36)
        s3 = T("trace and cost", size=36, t2c={"cost": GOLD})
        a1, a2 = [Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, stroke_width=3, color=DIM,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.16) for _ in range(2)]
        steps = VGroup(s1, a1, s2, a2, s3).arrange(RIGHT, buff=0.35).move_to([0, STEPS_Y, 0])
        # sit the words on one baseline ("pause" has a descender; its "a" sits on the line)
        s2.align_to(s1[1][1], DOWN)
        s3.align_to(s1[1][1], DOWN)

        lab = VGroup(cross_mark(RED), T("tempting wrong answers", size=36)).arrange(RIGHT, buff=0.32)
        box = RoundedRectangle(corner_radius=0.2, width=lab.width + 0.9, height=1.05)
        box.set_stroke(RED, 2.5).set_fill(CARD_FILL, 1)
        lab.move_to(box)
        wrong = VGroup(box, lab).move_to([0, WRONG_Y, 0])

        with self.say("c7.intro.2") as c:
            # "We'll take them in order."  The banner goes; the cards arrive in order, as ch6
            # left them, with their note.
            self.play(
                time_span(FadeOut(self.banner, shift=0.3 * UP), 0, 0.7),
                time_span(FadeOut(self.course, shift=0.2 * UP), 0, 0.7),
                time_span(self.header.animate.set_y(TOP_Y), 0, 0.8),
                time_span(LaggedStart(*[FadeIn(b, shift=0.3 * UP) for b in cards], lag_ratio=0.2), 0.3, 1.9),
                time_span(FadeIn(note, shift=0.2 * UP), 1.2, 2.0),
                run_time=2.0,
            )
            settle(self, cards)

            # "Each one starts with the question, and a moment to pause."
            c.wait_until("the question")
            first = cards[0]
            self.play(first.frame.animate.set_stroke(YELLOW, 3.0), first.num.animate.set_color(YELLOW),
                      *set_alpha(cards[1:], 0.4), run_time=1.0)
            c.wait_until("a moment to pause")
            self.play(FadeIn(s1, shift=0.25 * DOWN), run_time=0.9)

            # "Then we solve it, trace it on a small example, and work out what it costs."
            c.wait_until("then we solve")
            self.play(GrowArrow(a1), FadeIn(s2, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("trace it")
            self.play(GrowArrow(a2), FadeIn(s3, shift=0.25 * DOWN), run_time=0.9)

            # "We'll also meet some tempting wrong answers, which teach as much as the right ones."
            # The wrong-answer card takes the note's band, pushing it out.
            c.wait_until("wrong")
            self.play(FadeOut(note, shift=0.8 * LEFT), FadeIn(wrong, shift=0.8 * LEFT), run_time=1.0)
            self.wrong_born = self.time
        self.cards, self.steps, self.wrong = cards, [s1, a1, s2, a2, s3], wrong

    # the hand-off: the cards, at rest, shrink into the kit's strip (s2-s7 open on it)
    def into_strip(self):
        hold_for(self, self.wrong_born, len("tempting wrong answers"))
        cards, first = self.cards, self.cards[0]
        self.play(*[FadeOut(m) for m in (self.header, *self.steps, self.wrong)],
                  first.frame.animate.set_stroke(DIM, 2.5), first.num.animate.set_color(FG),
                  *set_alpha(cards[1:], 1), run_time=1.0)
        self.wait(0.4)
        strip = make_strip([TODO] * 6)
        shrink = []
        for b, p in zip(cards, strip):
            shrink += [Transform(b.frame, p.frame), Transform(b.num, p.num),
                       b.name.animate.scale(0.3).move_to(p).set_opacity(0)]
        self.play(*shrink, run_time=1.6)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
