"""Chapter 10, scene 1: spoiler warning, then the three exercises this part solves. Clips c10.intro.1 – c10.intro.2.

Opens on ch9 s9's next_card() (loaded, never copied), holds ~0.7 s, clears to the title card on {title}.
{lasttime}: ch9 s1's ex_row() (13–16) passes by small and DIM with GREEN ticks, then slides off left while a
small DIM preview of 17–19 comes in. {warn}: ch9 s1's spoiler_banner() + pause_icon(). Clip 2: next_card()
again at its own positions, cards dim, each brightens on its number; DuckDB tag under 19; on {hints} the
header and tag go, the row lifts 1.25 and each card's hint (DIM, T 28) appears under it. Ends on an empty frame.

EXPORTS (static; `load_scene("ch10_s1_intro").<name>()`):
- hint_block(n), n = 17/18/19: the DIM hint lines (T 28) under card n, centred under it at the lifted row
  (cards shifted up by LIFT); 17 = ch6 s7's three chips word for word, 18 = ch6 s7's hint_chip() text,
  19 = ch8 s7's HINTS_LINE items, one per line (19.1–19.4).
- LIFT = 1.3: how far the row moves up on {hints}.
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

R9 = load_scene("ch9_s9_recap")
I9 = load_scene("ch9_s1_intro")
T6 = load_scene("ch6_s7_recap")
T8 = load_scene("ch8_s7_try")

LIFT = 1.3
SHRINK = 0.35   # on {hints} each card's box loses this much empty space at its bottom
HINT_LINES = {
    17: ["tree or tangle?", "what is updated,", "and how often?", "one structure or many?"],
    18: ["one document at a time"],   # ch6 s7's hint_chip() text
    19: T8.HINTS_LINE.split(" · "),   # ch8 s7's hints_line(), one item per sub-card
}
DIMMED_CARD = 0.3


def hint_block(n):
    nc = R9.next_card()
    card = nc.cards[n]
    g = VGroup(*[T(s, 28, DIM) for s in HINT_LINES[n]]).arrange(DOWN, buff=0.08)
    g.next_to(card, DOWN, buff=0.16).shift((LIFT + SHRINK) * UP)
    if g.get_right()[0] > 6.5:
        g.shift((6.5 - g.get_right()[0]) * RIGHT)
    return g


def mini(n, solved):
    """A small stand-in for exercise card n: DIM rounded box, its head at T 30."""
    head = T(f"Exercise {n}", 30, DIM if solved else YELLOW)
    box = RoundedRectangle(corner_radius=0.16, width=2.6, height=1.3).set_stroke(DIM, 2).set_fill(BG, 0)
    head.move_to(box)
    g = VGroup(box, head)
    g.box, g.head = box, head
    return g


def dim_card(card, op=DIMMED_CARD):
    card.box.set_stroke(opacity=op)
    for part in card[1:]:
        part.set_opacity(op)


class Ch10S1Intro(NarratedScene):
    def construct(self):
        self.add(R9.next_card())
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c10.intro.1") as c:
            self.wait(0.7)
            tc = title_card("Part 10 · Solutions: modelling and JSON queries")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),  # early: title card
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("lasttime")

            # part nine's four cards pass by small and DIM, each ticked
            # (ch9 s1's ex_row() cards hold 28-size text: at "small" scale it falls under 28, so the
            # same four cards are drawn here as their heads only, in ex_row's order)
            row = VGroup(*[mini(n, True) for n in (13, 14, 15, 16)]).arrange(RIGHT, buff=0.35)
            row.move_to([0, 0.45, 0])
            ticks = VGroup(*[check_mark(GREEN).next_to(m, DOWN, buff=0.3) for m in row])
            sweep_clear(self, time_span(FadeIn(row, shift=1.5 * LEFT), 0.5, 1.6), run_time=1.6)  # early: a callback picture
            self.play(*appear(*ticks, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("this one solves")

            # they slide off left; part ten's three cards come in, small, unticked
            prev = VGroup(*[mini(n, False) for n in (17, 18, 19)]).arrange(RIGHT, buff=0.35)
            prev.move_to([0, 0.45, 0])
            self.play(*during([FadeOut(row, shift=3 * LEFT), FadeOut(ticks, shift=3 * LEFT)], 0, 0.5),  # early: a preview of the three cards
                      *during([FadeIn(prev, shift=1.5 * LEFT)], 0.45, 1),
                      run_time=min(1.8, c.until("modelling")))
            c.wait_until("warn")

            banner = I9.spoiler_banner()
            sweep_clear(self, time_span(FadeIn(banner, scale=0.9), 0.6, 1.4), run_time=1.4)  # early: the banner
            pause = I9.pause_icon(1.6).move_to([0, -1.6, 0])
            c.wait_until("pause the video")
            self.play(FadeIn(pause, scale=0.8), run_time=min(1.0, c.until()))

    def clip2(self):
        with self.say("c10.intro.2", gap=0.6) as c:
            nc = R9.next_card()
            cards = nc.cards
            for n in (17, 18, 19):
                dim_card(cards[n])
            sweep_clear(self, time_span(FadeIn(nc.header), 0.5, 1.2),  # early: the three cards shown whole, then lit one by one
                        time_span(FadeIn(nc.row), 0.6, 1.4), run_time=1.4)
            tag = T("DuckDB v1.5.6", 30, DIM).next_to(cards[19], DOWN, buff=0.22)
            for n, cue in ((17, "e17"), (18, "e18"), (19, "e19")):
                c.wait_until(cue)
                self.play(*set_alpha([cards[n]], 1), run_time=1.0)  # early: each card brightens on its number, its title read just after
            self.play(*appear(tag), run_time=1.0)  # early: the engine tag, named in this sentence
            c.wait_until("hints")

            hints = [hint_block(n) for n in (17, 18, 19)]
            self.play(*during([FadeOut(nc.header), FadeOut(tag)], 0, 0.4),  # early: no new text
                      *[c_.box.animate.stretch_to_fit_height(c_.box.height - SHRINK).shift(
                          (LIFT + SHRINK / 2) * UP) for c_ in cards.values()],
                      *[m.animate.shift(LIFT * UP) for c_ in cards.values() for m in c_[1:]],
                      run_time=1.2)
            self.play(*appear(*hints, lag=0.35), run_time=min(1.6, c.until(floor=0.8)))  # early: each card's hint, read in the next scenes
        self.wait(4.0)
