"""Chapter 6, scene 1: the bonus chapter opens: title card, a spoiler warning, the five
exercise cards and the routine each solution follows. Clips c6.intro.1 - c6.intro.2.

Plan: title card ("Bonus · Solutions to the exercises"); on {warn} title and rule lift away,
course and part lines rise to the top (part = header from here on), a GOLD "SPOILERS AHEAD" banner
with a big pause icon fills the centre (flashed on "stop the video"). On {cards} the banner
goes and the five overview cards from ch5_s6 (BigCard row, y 0.7) cascade in. On {ritual}
3.1 lights up (YELLOW, the others dim); the routine grows under the row, ch5-style:
"|| pause -> solve -> trace and cost". On {wrong} a RED x card slides in below it.
The scene ends on the row alone (all cards in their resting style), the shot s2-s6 reopen on.

The cards and the pause icon come from the exercise-card kit in ch5_s6_sumlast.py (read-only).
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
from scenes.ch5_s6_sumlast import BigCard, CARD_FILL, pause_icon  # noqa: E402  the shared exercise-card kit

ROW_Y = 0.7          # the five-card row, exactly as in ch5_s6's overview
HEADER_Y = 2.65      # the part line, kept as the header (ch5_s6's "Exercises" sat at 2.85)
COURSE_Y = 3.28      # the course line rides above it until the cards arrive


def card_row():
    """The five overview cards: BigCard 2.4 x 1.8, 0.25 apart, centred at (0, ROW_Y)."""
    return VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * ROW_Y)


class SolutionsIntro(NarratedScene):
    def construct(self):
        self.warning()
        self.routine()
        self.end_on_row()

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

        with self.say("c6.intro.1") as c:
            # "This bonus chapter for lecture three has solutions to the five exercises ..."
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("lecture three")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("solutions")
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

            # "If you haven't tried the exercises yet, stop the video now, and have a go."
            c.wait_until("stop the video")
            self.play(FlashAround(icon, color=GOLD, run_time=2, time_width=1.5, buff=0.25))
        self.header, self.course, self.banner = card.part, card.course, banner

    # intro.2: the five cards in order; the routine; tempting wrong answers
    def routine(self):
        bigs = card_row()
        s1 = VGroup(pause_icon(h=0.36), T("pause", size=36)).arrange(RIGHT, buff=0.2)
        s2 = T("solve", size=36)
        s3 = T("trace and cost", size=36, t2c={"cost": GOLD})
        a1, a2 = [Arrow(LEFT * 0.45, RIGHT * 0.45, buff=0, stroke_width=3, color=DIM,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.16) for _ in range(2)]
        steps = VGroup(s1, a1, s2, a2, s3).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.3)
        # sit the words on one baseline ("pause" has a descender; its "a" sits on the line)
        s2.align_to(s1[1][1], DOWN)
        s3.align_to(s1[1][1], DOWN)

        lab = VGroup(cross_mark(RED), T("tempting wrong answers", size=36)).arrange(RIGHT, buff=0.32)
        box = RoundedRectangle(corner_radius=0.2, width=lab.width + 0.9, height=1.05)
        box.set_stroke(RED, 2.5).set_fill(CARD_FILL, 1)
        lab.move_to(box)
        wrong = VGroup(box, lab).move_to(DOWN * 2.75)

        with self.say("c6.intro.2") as c:
            # "We'll take them in order."  The banner goes; the cards arrive left to right.
            self.play(
                time_span(FadeOut(self.banner, shift=0.3 * UP), 0, 0.7),
                time_span(FadeOut(self.course, shift=0.2 * UP), 0, 0.7),
                time_span(LaggedStart(*[FadeIn(b, shift=0.3 * UP) for b in bigs], lag_ratio=0.2), 0.3, 1.9),
                run_time=1.9,
            )

            # "Each exercise starts with the question and a moment to pause."
            c.wait_until("ritual")
            first = bigs[0]
            self.play(first.frame.animate.set_stroke(YELLOW, 3.0), first.num.animate.set_color(YELLOW),
                      *set_alpha(bigs[1:], 0.4), run_time=1.0)
            c.wait_until("pause")
            self.play(FadeIn(s1, shift=0.25 * DOWN), run_time=0.9)

            # "Then we solve it, trace it, and work out its cost."
            c.wait_until("we solve")
            self.play(GrowArrow(a1), FadeIn(s2, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("trace it")
            self.play(GrowArrow(a2), FadeIn(s3, shift=0.25 * DOWN), run_time=0.9)

            # "We'll also look at tempting wrong answers, which teach as much as right ones."
            c.wait_until("wrong")
            self.play(FadeIn(wrong, shift=0.8 * LEFT), run_time=1.0)
            self.wrong_born = self.time
        self.bigs, self.steps, self.wrong = bigs, [s1, a1, s2, a2, s3], wrong

    # the closing shot: the row alone, every card at rest (s2-s6 reopen on exactly this)
    def end_on_row(self):
        need = 4.0 + len("tempting wrong answers") / 12.0 + 0.2
        if self.time < self.wrong_born + need:
            self.wait(self.wrong_born + need - self.time)
        first = self.bigs[0]
        self.play(*[FadeOut(m) for m in (self.header, *self.steps, self.wrong)],
                  first.frame.animate.set_stroke(DIM, 2.5), first.num.animate.set_color(FG),
                  *set_alpha(self.bigs[1:], 1), run_time=1.0)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
