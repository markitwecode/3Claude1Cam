"""Chapter 2, scene 1: Hook. Is 9 in this list? A program sees one cell at a time. Clips c2.hook.1 – c2.hook.3.

End shot (s2 opens from it, s4 brings it back): ConsChain([3, 5, 9, 4, 7]) at library default
size, centred at ORIGIN, normal colours; a GOLD marker(GOLD, scale=0.24) at
above(chain.cells[0].box).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

VALUES = [3, 5, 9, 4, 7]
WORDS = ["three", "five", "nine", "four", "seven"]


def tag(text, color, size=38):
    """A small outlined pill with a short question in it."""
    t = T(text, size=size, color=color)
    pill = RoundedRectangle(corner_radius=0.22, width=t.width + 0.55, height=t.height + 0.36,
                            stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.10)
    pill.move_to(t)
    return VGroup(pill, t)


class Hook(NarratedScene):
    def construct(self):
        chain = ConsChain(VALUES)
        cells = chain.cells

        # ch1's cut after cell 2 and its two braces, rebuilt
        x_cut = (cells[1].ptr.get_right()[0] + cells[2].box.get_left()[0]) / 2
        cut = DashedLine([x_cut, 1.05, 0], [x_cut, -1.05, 0], dash_length=0.12,
                         color=GOLD, stroke_width=5)
        take_brace = span_brace(cells[0].box.get_corner(UL), cells[1].ptr.get_corner(UR), UP)
        drop_brace = span_brace(cells[2].box.get_corner(UL), cells[4].ptr.get_corner(UR), UP)
        take_lab = Mono("take 2", size=36, t2c={"take": YELLOW, "2": GOLD})
        drop_lab = Mono("drop 2", size=36, t2c={"drop": YELLOW, "2": GOLD})
        take_lab.next_to(take_brace, UP, buff=0.15)
        drop_lab.next_to(drop_brace, UP, buff=0.15)

        question = T("Is 9 in this list?", size=50, color=YELLOW).move_to(UP * 2.35)
        pointer = marker(GOLD, scale=0.24).move_to(above(cells[0].box))

        t_long = tag("how long?", GOLD)
        t_ocaml = tag("how, in OCaml?", BLUE)
        VGroup(t_long, t_ocaml).arrange(RIGHT, buff=0.8).move_to(DOWN * 1.75)
        t_equal = tag("what does equal mean?", YELLOW).move_to(DOWN * 2.95)

        rest = [*cells[1:], *chain.arrows, chain.nil]

        # ── c2.hook.1 ─────────────────────────────────────────────────────────
        with self.say("c2.hook.1") as c:
            card = title_card("Part 2 · Searching a list")
            self.play(
                time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),
                time_span(GrowFromCenter(card.rule), 0, 0.6),
                time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.1, 0.7),
                time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.2, 0.8),
                run_time=0.8,
            )
            # the card stays up through the pause and "Last time, take and drop"; on "cut" it clears, the
            # chain comes in and the GOLD cut lands, then the take/drop braces
            c.wait_until("cut a list")
            k = min(1.0, 0.95 * c.until("take made") / 1.6)
            self.play(
                *[time_span(FadeOut(m), 0, 0.6 * k) for m in (card.title, card.rule, card.course, card.part)],
                time_span(FadeIn(chain, shift=0.3 * UP), 0.2 * k, 0.8 * k),
                time_span(Create(cut), 0.5 * k, 1.05 * k),
                time_span(GrowFromCenter(VGroup(take_brace, drop_brace)), 1.0 * k, 1.6 * k),
                time_span(FadeIn(VGroup(take_lab, drop_lab), shift=0.3 * DOWN), 1.0 * k, 1.6 * k),
                run_time=1.6 * k,
            )
            c.wait_until("copy")
            self.play(*flash([cells[0], cells[1]], YELLOW, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("skipped")))
            c.wait_until("skipped")
            self.play(drop_brace.animate(rate_func=there_and_back).set_color(YELLOW).stretch(1.06, 0),
                      FlashUnder(drop_lab, color=YELLOW, time_width=1.5),
                      run_time=min(1.2, c.remaining))

        # ── c2.hook.2 ─────────────────────────────────────────────────────────
        with self.say("c2.hook.2") as c:
            c.wait_until("again")
            self.play(FadeOut(cut), FadeOut(VGroup(take_brace, drop_brace, take_lab, drop_lab)),
                      run_time=1.0)
            # read along: each value swells as it is spoken
            offs = [c.until(w, floor=0.0) for w in WORDS]
            self.play(*[time_span(cell.label.animate(rate_func=there_and_back).scale(1.3), o, o + 0.6)
                        for cell, o in zip(cells, offs)],
                      run_time=offs[-1] + 0.6)
            c.wait_until("ask")
            self.play(FadeIn(question, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("glance")
            # the eye's view: every value at once
            self.play(*recolor([cell.label for cell in cells], YELLOW), run_time=0.8)
            c.wait_until("that it is")
            self.play(FlashAround(cells[2], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("program")
            self.play(*recolor([cell.label for cell in cells], FG), run_time=1.0)
            c.wait_until("one")
            # the program's eye: one cell, the rest dimmed
            self.play(*set_alpha(rest + [question], DIMMED),
                      FadeIn(pointer, shift=0.45 * DOWN), run_time=1.2)
            c.wait_until("one element")
            self.play(FlashAround(cells[0], color=GOLD, time_width=1.5),
                      run_time=min(1.2, c.remaining))

        # ── c2.hook.3 ─────────────────────────────────────────────────────────
        with self.say("c2.hook.3") as c:
            self.play(restyle(question, 1), FadeIn(t_long, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("how do you write")
            self.play(FadeIn(t_ocaml, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("equal")
            self.play(FadeIn(t_equal, shift=0.3 * DOWN), run_time=1.0)

        # hand-off shot: the chain alone, normal colours, pointer over the head
        self.play(FadeOut(VGroup(question, t_long, t_ocaml, t_equal)), *set_alpha(rest, 1),
                  run_time=0.8)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)   # end on an empty frame
        self.wait(0.15)
