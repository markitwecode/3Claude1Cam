"""Chapter 1, scene 1: title card, what this lecture holds, then the take/drop question on cells. Clips c1.hook.1 – c1.hook.2.

Layout:
hook.1  title card (shifted UP 0.4); DIM row of L3's tools (build, match, length, append, reverse)
        word by word at y -2.5.  {plan}: tools go, card scales 0.8 and rises to y 2.2; two lines
        "more list utilities" (tools go) / "more patterns of recursion"; {change} ("at the end"):
        six GOLD coin discs 50 20 10 5 2 1 + "making change".
hook.2  {chain}: sweep; L3's 3 -> 5 -> 9 -> [] (centred); the 4 and the 7 join on their words
        (the chain recentres each time) -> ConsChain([3, 5, 9, 4, 7]) at ORIGIN, default size.
        "cut it": GOLD dashed cut between the 5 and the 9; YELLOW "?" over each side; GOLD
        "cost?" under each; "take"/"drop": the "?"s become YELLOW take / drop, "cost?" goes.
End shot (s2 opens from it): chain + cut + take/drop labels alone.
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
TOOLS = ["build", "match", "length", "append", "reverse"]
TOOL_CUES = ["built", "apart", "length", "append", "reverse"]

CARD_Y = 0.4                 # the card's centre at first
TOOLS_Y = -2.5               # the row of L3's tools
CARD_S, CARD_UP = 0.8, 2.2   # on {plan} the card shrinks and rises
LINE_Y = (0.0, -0.8)       # "more list utilities" / "more patterns of recursion"
COIN_Y, CAPTION_Y = -2.1, -3.0

COIN_R = 0.42                # the coin disc reused by ch4-ch7
COIN_LABEL = 34

Q_Y, COST_Y = 1.95, 1.2      # "?" and "cost?" over each side of the cut


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


class Hook(NarratedScene):
    def construct(self):
        self.plan()
        self.question()
        # hand-off shot: chain + cut + take / drop, alone
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c1.hook.1: title card, last time's tools, this lecture's plan ────────────
    def plan(self):
        card = title_card("Part 1 · Take and drop").shift(UP * CARD_Y)
        tools = VGroup(*[T(w, size=34, color=DIM) for w in TOOLS]).arrange(RIGHT, buff=0.9)
        tools.move_to(UP * TOOLS_Y)
        line1 = T("more list utilities", size=46).move_to(UP * LINE_Y[0])
        line2 = T("more patterns of recursion", size=46).move_to(UP * LINE_Y[1])
        coins = VGroup(*[coin(v) for v in [50, 20, 10, 5, 2, 1]]).arrange(RIGHT, buff=0.28)
        coins.move_to(UP * COIN_Y)
        caption = T("making change", size=34).move_to(UP * CAPTION_Y)

        with self.say("c1.hook.1") as c:
            self.play(
                time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.8),
                time_span(GrowFromCenter(card.rule), 0, 0.8),
                time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.2, 1.0),
                time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.4, 1.2),
                run_time=1.2,
            )
            settle(self, card)
            # one DIM label per beat of "built lists, took them apart, length, append, reverse"
            for word, cue in zip(tools, TOOL_CUES):
                c.wait_until(cue)
                self.play(FadeIn(word, shift=0.25 * DOWN), run_time=0.5)

            # {plan}: the card rises; the tools give way to this lecture's two lines
            c.wait_until("plan")
            self.play(card.animate.scale(CARD_S).move_to(UP * CARD_UP), run_time=1.2)
            c.wait_until("list utilities")
            self.play(LaggedStart(*[FadeOut(w, shift=0.2 * DOWN) for w in tools], lag_ratio=0.1),
                      time_span(FadeIn(line1, shift=0.3 * DOWN), 0.3, 1.2), run_time=1.2)
            c.wait_until("patterns of recursion")
            self.play(FadeIn(line2, shift=0.3 * DOWN), run_time=1.0)

            # {change}: the coins a till hands you
            c.wait_until("at the end")
            self.play(LaggedStart(*[FadeIn(k, shift=0.3 * DOWN) for k in coins], lag_ratio=0.2),
                      time_span(FadeIn(caption, shift=0.25 * DOWN), 1.2, 2.0), run_time=2.0)

    # ── c1.hook.2: the running chain, a cut, two questions, two names ────────────
    def join(self, src, dst, run_time):
        """src (k cells) -> dst (k + 1 cells): the old cells slide left, [] slides right and
        the new cell drops into the gap; both chains are centred on ORIGIN."""
        k = len(src.cells)
        self.remove(src)
        self.add(*src.submobjects)
        anims = [ReplacementTransform(a, b) for a, b in zip(src.cells, dst.cells)]
        anims += [ReplacementTransform(a, b) for a, b in zip(src.arrows, dst.arrows)]
        anims += [ReplacementTransform(src.nil, dst.nil),
                  time_span(FadeIn(dst.cells[k], shift=0.4 * DOWN), 0.2 * run_time, 0.85 * run_time),
                  time_span(GrowArrow(dst.arrows[k]), 0.55 * run_time, run_time)]
        self.play(*anims, run_time=run_time)
        settle(self, dst)

    def question(self):
        a = ConsChain(VALUES[:3])
        b = ConsChain(VALUES[:4])
        chain = ConsChain(VALUES)
        cells = chain.cells

        x_cut = (cells[1].ptr.get_right()[0] + cells[2].box.get_left()[0]) / 2
        cut = DashedLine([x_cut, 1.05, 0], [x_cut, -1.05, 0], dash_length=0.12,
                         color=GOLD, stroke_width=5)
        left_x = (cells[0].box.get_left()[0] + cells[1].ptr.get_right()[0]) / 2
        right_x = (cells[2].box.get_left()[0] + chain.nil.get_right()[0]) / 2

        q_l = T("?", size=84, color=YELLOW).move_to([left_x, Q_Y, 0])
        q_r = T("?", size=84, color=YELLOW).move_to([right_x, Q_Y, 0])
        cost_l = T("cost?", size=32, color=GOLD).move_to([left_x, COST_Y, 0])
        cost_r = T("cost?", size=32, color=GOLD).move_to([right_x, COST_Y, 0])
        take_lab = Mono("take", size=48, color=YELLOW).move_to([left_x, Q_Y, 0])
        drop_lab = Mono("drop", size=48, color=YELLOW).move_to([right_x, Q_Y, 0])

        with self.say("c1.hook.2") as c:
            # {chain}: everything goes; Lecture 3's 3 -> 5 -> 9 comes back
            sweep_clear(self, time_span(FadeIn(a, shift=0.3 * UP), 0.7, 1.7), run_time=1.7)
            # "... four, seven": the new cells join on their words
            c.wait_until("four")
            self.join(a, b, run_time=max(0.6, min(1.0, 0.9 * c.until("seven"))))
            c.wait_until("seven")
            self.join(b, chain, run_time=1.0)

            # {cut}: right after the second element
            c.wait_until("cut it")
            self.play(Create(cut), run_time=max(0.8, min(1.3, 0.9 * c.until("second element"))))
            c.wait_until("second element")
            self.play(FlashAround(cells[1], color=YELLOW, time_width=1.5), run_time=1.2)

            # {sides}: the front part? the rest?
            c.wait_until("front part")
            self.play(FadeIn(q_l, shift=0.3 * DOWN, scale=0.6), run_time=0.9)
            c.wait_until("the rest")
            self.play(FadeIn(q_r, shift=0.3 * DOWN, scale=0.6), run_time=0.9)

            # {cost}: and what does each cost?
            c.wait_until("what does each")
            self.play(LaggedStart(FadeIn(cost_l, shift=0.2 * DOWN), FadeIn(cost_r, shift=0.2 * DOWN),
                                  lag_ratio=0.3), run_time=1.2)

            # {names}: the two "?"s become the two functions
            c.wait_until("take")
            self.play(ReplacementTransform(q_l, take_lab), FadeOut(cost_l),
                      run_time=max(0.5, min(0.9, c.until("drop"))))
            c.wait_until("drop")
            self.play(ReplacementTransform(q_r, drop_lab), FadeOut(cost_r),
                      run_time=max(0.5, min(0.9, c.remaining)))
