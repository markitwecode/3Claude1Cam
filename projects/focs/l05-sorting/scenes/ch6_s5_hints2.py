"""Chapter 6, scene 5: exercises 5.3 (bubble sort's cost) and 5.4 (bubble sort in OCaml), each
grown out of its pill onto a hero card: the task, its example, one hint beneath with a GOLD "?"
wherever an answer would go (never a solution), a still "pause" beat. Clips c6.ex.5 - c6.ex.7.

Exports (self-contained; ch6_s6 and ch7 rebuild them): card_5_3(), card_5_4(), bracket_over(),
EX53_LINES, EX54_TASK, EX54_NAME, EX54_TYPE, EX54_TEST. Imports the card kit read-only from
ch6_s4_hints1.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch6_s4_hints1 import (CARD_TOP, COL_X, CURRENT, DONE, RUNNING, TODO, HeroCard,  # noqa: E402,F401
                                  Slot, Tag, enter_card, exit_card, finish, hint_label, hold_for,
                                  make_strip, pause_tag, tiles)

# ── the cards (verbatim card text) ──────────────────────────────────────────────────
EX53_LINES = ("Swap neighbours that are out of order;",
              "repeat until no swaps are possible.",
              "State, with justification, the time complexity.")
EX54_TASK = "Implement bubble sort in OCaml."
EX54_NAME, EX54_TYPE = "bubble", "'a list -> 'a list"
EX54_TEST = ("bubble [3; 5; 3; 1; 5]", "[1; 3; 3; 5; 5]")   # checked with a trial bubble sort

STEP53 = 0.62
H53 = 5.75                      # header, three task rows, the chain with its bracket and loop
L53 = 0.46 + 3 * STEP53 + 0.38  # lifted for the hint: header and task only
CHAIN_S = 0.75
CHAIN_Y = -1.35


def bracket_over(a, b, color=YELLOW, buff=0.15, tick=0.2, width=4):
    """A bracket (a lid with two down-ticks) over the neighbouring mobjects a and b."""
    left, right = a.get_left()[0] - 0.06, b.get_right()[0] + 0.06
    y = max(a.get_top()[1], b.get_top()[1]) + buff
    br = VMobject().set_points_as_corners([[left, y - tick, 0], [left, y, 0],
                                           [right, y, 0], [right, y - tick, 0]])
    return br.set_stroke(color, width)


def card_5_3():
    """Card 5.3 as stated (built; it needs no lowering). Attributes:
    .rows (3 T lines, EX53_LINES; .rows[2] is the task's last sentence),
    .chain (ConsChain(RUNNING) at 0.75, values re-enlarged, centred), .bracket (YELLOW, over cells
    0 and 1), .in_lbl ("in order", GREEN), .bracket2 / .out_lbl (over cells 2 and 3, "out of
    order: swap", RED), .loop / .loop_lbl (the arrow under the chain, "pass after pass").
    whole() = frame, header, rows, chain."""
    card = HeroCard(2, height=H53, step=STEP53, lifted=L53)
    card.rows = [card.at_row(T(s, size=34), k + 1) for k, s in enumerate(EX53_LINES)]
    chain = ConsChain(RUNNING).scale(CHAIN_S)
    for cell in chain.cells:
        cell.label.scale(1.1).set_z_index(1)    # values stay above the boxes they pass over
    chain.move_to([0, CHAIN_Y, 0])
    card.chain = chain
    cs = chain.cells
    card.bracket = bracket_over(cs[0], cs[1])
    card.in_lbl = T("in order", size=32, color=GREEN).next_to(card.bracket, UP, buff=0.14)
    card.bracket2 = bracket_over(cs[2], cs[3])
    card.out_lbl = T("out of order: swap", size=32, color=RED).next_to(card.bracket2, UP, buff=0.14)
    y = cs[0].get_bottom()[1] - 0.16
    card.loop = CurvedArrow([chain.nil.get_center()[0], y, 0], [cs[0].get_center()[0], y, 0],
                            angle=-0.5, color=FG, stroke_width=3, tip_length=0.2)
    card.loop_lbl = T("pass after pass", size=30).next_to(card.loop, DOWN, buff=0.12)
    card.lower(*card.rows, chain, card.bracket, card.in_lbl, card.bracket2, card.out_lbl,
               card.loop, card.loop_lbl)
    card.parts += [*card.rows, chain]
    return card


STEP54 = 0.74
H54 = 0.46 + 2 * STEP54 + 0.45  # header, task, slot (the test belongs to the hint)


def card_5_4():
    """Card 5.4 as stated, built and lowered. Attributes: .task (T), .name (Code "bubble",
    YELLOW), .slot (Slot(EX54_TYPE)). whole() = frame, header, task, name, slot."""
    card = HeroCard(3, height=H54, step=STEP54)
    card.task = card.at_row(T(EX54_TASK, size=36), 1)
    card.name = Code(EX54_NAME, size=36).set_color(YELLOW)
    card.at_row(card.name, 2)
    card.slot = Slot(EX54_TYPE, size=34)
    card.slot.next_to(card.name, RIGHT, buff=0.4).set_y(card.row_y(2))
    card.lower(card.task, card.name, card.slot)
    card.parts += [card.task, card.name, card.slot]
    return card


# ── this scene ───────────────────────────────────────────────────────────────────
class ExercisesHints2(NarratedScene):
    def construct(self):
        self.bubble_card()
        self.bubble_hint()
        self.code_card_and_hint()
        hold_for(self, self.pause_born, len("pause and try it"))
        finish(self)

    # ex.5: strip; 5.3 grows; the chain, a bracket on a pair, the loop, the 9/4 swap, the task
    def bubble_card(self):
        strip = make_strip([DONE, DONE, TODO, TODO])
        card = card_5_3()
        chain, cs = card.chain, card.chain.cells
        with self.say("c6.ex.5") as c:
            # "Exercise five point three is about bubble sort."
            self.play(*appear(strip, shift=None), run_time=0.6)
            self.play(*enter_card(strip, card, card.rows), run_time=1.6)  # early: the task shown whole, then walked
            # "It looks at neighbouring pairs of items, and swaps any pair that's out of order."
            c.wait_until("pairs")
            self.play(*appear(chain, shift=0.2 * UP), run_time=1.0)
            self.play(GrowFromCenter(card.bracket), run_time=0.8)
            c.wait_until(own_word=card.in_lbl, cue="out of order")
            self.play(*appear(card.in_lbl), run_time=0.9)
            # "It repeats this, pass after pass, until no more swaps are possible."
            c.wait_until("repeat")
            self.play(Create(card.loop), run_time=1.2)
            c.wait_until(own_word=card.loop_lbl, cue="pass after pass")
            self.play(*appear(card.loop_lbl), run_time=0.9)
            # "In our list, the nine and the four are out of order, so they swap."
            c.wait_until("example")
            self.play(Transform(card.bracket, card.bracket2), *swap(card.in_lbl, card.out_lbl),
                      run_time=1.2)
            l9, l4 = cs[2].label, cs[3].label
            p9, p4 = l9.get_center().copy(), l4.get_center().copy()
            self.play(l9.animate(path_arc=0.6 * PI).move_to(p4),
                      l4.animate(path_arc=0.6 * PI).move_to(p9), run_time=1.5)
            cs[2].label, cs[3].label = l4, l9
            # "State its time complexity, with justification."
            c.wait_until("task")
            self.play(card.rows[2].animate.set_color(YELLOW),
                      FlashUnder(card.rows[2], color=YELLOW, time_width=1.5), run_time=1.5)
        card.keep(*card.rows, chain, card.bracket, card.out_lbl, card.loop, card.loop_lbl)
        self.strip, self.card = strip, card

    # ex.6: hint: the largest item in one pass; how many passes; comparisons per pass; sorted input
    def bubble_hint(self):
        card = self.card
        drop = [card.chain, card.bracket, card.out_lbl, card.loop, card.loop_lbl]
        hl = hint_label(card)
        tl = tiles(RUNNING, side=0.75, gap=0.2, size=36).move_to([-3.6, -1.85, 0])
        qs = [T("?", size=40, color=GOLD).next_to(tl.sq[k], UP, buff=0.18) for k in (3, 4)]
        one = T("after one pass?", size=30).next_to(tl, DOWN, buff=0.3)
        passes = T("passes: at most ?", size=36, t2c={"?": GOLD}).move_to([0.6, -1.3, 0], aligned_edge=LEFT)
        per = T("comparisons per pass: ?", size=36, t2c={"?": GOLD}).move_to([0.6, -2.1, 0], aligned_edge=LEFT)
        sch = ConsChain(sorted(RUNNING)).scale(0.52)
        for cell in sch.cells:
            cell.label.scale(1.35)
            cell.box.set_stroke(GREEN)
            cell.ptr.set_stroke(GREEN)
        sch.nil.scale(1.45)
        sch.move_to([COL_X, -2.2, 0], aligned_edge=LEFT)
        s_lbl = T("sorted input", size=32, color=GREEN).move_to([COL_X, -1.3, 0], aligned_edge=LEFT)
        s_q = T("?", size=44, color=GOLD).next_to(s_lbl, RIGHT, buff=0.3)
        tag = pause_tag()

        with self.say("c6.ex.6", gap=2.1) as c:
            # "Here's the hint."  The example goes; the card goes up; the hint label beneath.
            self.play(*card.lift(drop), *during(appear(hl), 0.55, 1), run_time=1.4)
            # "Follow the largest item through one pass."
            c.wait_until("largest")
            self.play(*appear(tl, shift=0.2 * UP), run_time=1.0)
            self.play(*recolor([tl.vals[2]], YELLOW), tl.sq[2].animate.set_stroke(YELLOW),
                      FlashAround(tl.sq[2], color=YELLOW, buff=0.08), run_time=1.0)
            # "Where must it end up?"
            c.wait_until("where must")
            self.play(*appear(*qs, one, lag=0.2), run_time=1.1)
            # "So how many passes can it take, at most?"
            c.wait_until("passes")
            self.play(*appear(passes), run_time=1.0)
            # "And how many comparisons does each pass make?"
            c.wait_until("each")
            self.play(*appear(per), run_time=1.0)
            # "Finally, what happens when the input is already sorted?"
            c.wait_until("sortedin")
            self.play(*during(disappear(tl, *qs, one), 0, 0.45),
                      *during(appear(s_lbl, sch, s_q, lag=0.15), 0.45, 1), run_time=1.6)
            # "Pause the video, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.6)
        self.hint = [hl, passes, per, s_lbl, sch, s_q]
        self.tag = tag

    # ex.7: 5.3 shrinks back; 5.4 grows; hint: the pattern, a pass's pair, the loop, a test, equal pair
    def code_card_and_hint(self):
        strip = self.strip
        card = card_5_4()
        hl = hint_label(card)
        top = card.bottom            # the lifted card's bottom edge (the hint area starts below it)

        # the pattern (L3 ch5's hint picture), left
        pat = Code("x::y::ys", size=60)
        pat.move_to([COL_X + 0.3, top - 1.65, 0], aligned_edge=LEFT)
        y0 = pat.get_bottom()[1] - 0.1
        braces, blabels = [], []
        for sub, word, color in (("x", "first", FG), ("y", "second", GOLD), ("ys", "the rest", TEAL)):
            g = pat.find(sub)
            b = Brace(Line([g.get_left()[0], y0, 0], [g.get_right()[0], y0, 0]), DOWN, buff=0.02,
                      color=color)
            braces.append(b)
            blabels.append(T(word, size=30, color=color).next_to(b, DOWN, buff=0.08))
        for lab in blabels[1:]:
            lab.align_to(blabels[0], UP)

        # a pass returns a pair, right
        rx = 3.2
        ret = T("a pass returns", size=30, color=DIM).move_to([rx, top - 1.05, 0])
        py = top - 1.7
        lp = T("(", size=50).move_to([1.7, py, 0])
        q1 = T("?", size=50, color=GOLD).move_to([2.35, py, 0])
        cm = T(",", size=50).move_to([3.2, py - 0.12, 0])
        q2 = T("?", size=50, color=GOLD).move_to([4.1, py, 0])
        rp = T(")", size=50).move_to([4.75, py, 0])
        l_list = T("list", size=30, color=DIM).next_to(q1, DOWN, buff=0.22)
        l_sw = T("swapped", size=30, color=DIM).next_to(q2, DOWN, buff=0.22).align_to(l_list, UP)
        b_tag = Tag("bool", GREEN).next_to(l_sw, RIGHT, buff=0.2)
        ly = l_sw.get_bottom()[1] - 0.2
        loop = CurvedArrow([5.3, ly, 0], [1.6, ly, 0], angle=-0.55, color=FG, stroke_width=3,
                           tip_length=0.2)
        loop_lbl = T("again, until a pass swaps nothing", size=30).next_to(loop, DOWN, buff=0.12)

        # the test, left (where the pattern was)
        test = Code(f"{EX54_TEST[0]}\n  ⇒  {EX54_TEST[1]}", size=32)
        test.move_to([COL_X + 0.1, top - 1.65, 0], aligned_edge=LEFT)

        # two equal neighbours, right (where the pair was)
        eq = tiles([3, 3], side=0.85, gap=0.22, size=40).move_to([3.2, top - 2.35, 0])
        eq_br = bracket_over(eq.sq[0], eq.sq[1], color=YELLOW)
        eq_q = VGroup(T("out of order", size=32), T("?", size=44, color=GOLD)).arrange(RIGHT, buff=0.2)
        eq_q.next_to(eq_br, UP, buff=0.16)
        decide = T("decide before you run it", size=30).next_to(eq, DOWN, buff=0.3)
        tag = pause_tag()

        with self.say("c6.ex.7", gap=2.1) as c:
            # "Exercise five point four."  Then a still beat.
            self.play(*exit_card(strip, self.card, [*self.hint, self.tag]), run_time=0.9)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=0.9)
            # "Implement bubble sort in OCaml."
            c.wait_until(own_word=card.task, cue="implement")
            self.play(*appear(card.task, card.name, lag=0.3),
                      *during([FadeIn(card.slot, shift=0.2 * DOWN)], 0.4, 1), run_time=1.4)
            card.keep(card.task, card.name, card.slot)
            # "Here's the hint."  The card goes up; the hint label beneath.
            c.wait_until("hint")
            self.play(*card.lift(), *during(appear(hl), 0.55, 1), run_time=1.2)
            # "Write one pass with lecture three's pattern, ex cons why cons whys, ..."
            c.wait_until("pattern")
            self.play(*appear(pat, shift=0.2 * UP), run_time=1.0)
            c.wait_until("ex cons why")
            self.play(*[a for b, lab in zip(braces, blabels) for a in (GrowFromCenter(b), FadeIn(lab, shift=0.2 * DOWN))], run_time=1.3)  # early: the pattern's three parts, named as it is read
            # "Have the pass return two things, the new list, and whether it swapped anything."
            c.wait_until("report")
            self.play(*appear(ret, lp, q1, cm, q2, rp, lag=0.08), run_time=1.2)
            c.wait_until(own_word=l_list, cue="new list")
            self.play(*appear(l_list), run_time=0.8)
            c.wait_until(own_word=l_sw, cue="whether")
            self.play(*appear(l_sw, b_tag, lag=0.3), run_time=1.0)
            # "Then keep making passes until one swaps nothing."
            c.wait_until("loop")
            self.play(Create(loop), *during(appear(loop_lbl), 0.4, 1), run_time=1.4)
            # "Test it on three, five, three, one, five."
            c.wait_until("test")
            self.play(*during(disappear(pat, *braces, *blabels), 0, 0.45),
                      *during(appear(test), 0.5, 1), run_time=1.5)
            # "And before you run it, decide what out of order means for two equal neighbours."
            c.wait_until("careful")
            self.play(*during(disappear(ret, lp, q1, cm, q2, rp, l_list, l_sw, b_tag, loop, loop_lbl), 0, 0.45),
                      *during(appear(eq, shift=0.2 * UP), 0.5, 1),
                      *during([GrowFromCenter(eq_br)], 0.7, 1), run_time=1.5)
            c.wait_until(own_word=decide, cue="decide")
            self.play(eq_br.animate.set_stroke(RED), *appear(decide), run_time=1.0)
            c.wait_until("out of order means")
            self.play(*appear(*eq_q, lag=0.3), run_time=1.0)
            # "Pause, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
