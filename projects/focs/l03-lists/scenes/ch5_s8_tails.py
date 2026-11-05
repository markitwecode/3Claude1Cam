"""STATUS: built, vk check clean (104.7 s for 94.3 s of narration; end card holds ~8 s after
the last word). Reviewed at 480p. Ends on an empty frame (the lecture's last shot).

Chapter 5, scene 8: exercise 3.5 (tails) and its hint, then the recap of the whole lecture
and the end card. Same card system as ch5_s6/ch5_s7 (the kit is imported from
ch5_s6_sumlast.py): the card grows out of its pill, task / example / GOLD "?", one hint below,
a still "pause and try it" beat. Never a solution: those are in the bonus chapter.

Plan: ex.11: strip fades in (3.1-3.4 done, 3.5 current); the card states the task and the type
in its slot; `tails [1; 2; 3]  ⇒`, then a skeleton `[ _; _; _; _ ]` of four dashed places on
"four lists", each tail flying out of the input's suffix on its cue, `[]` TEAL on {nil}.
ex.12: the card goes up; chapter 1's chain 1 -> 2 -> 3 -> [] with a TEAL box hopping tail to
tail; {same}: the four results turn TEAL; the bonus question in GOLD; pause tag on {try}.
recap: the card shrinks into its pill, the strip gives way to "Recap" (ch1-ch4 style: T 34 /
Code 32, each new row in while the previous steps back to 0.5), seven rows with an icon each;
{next}: all rows back to full, five pills -> "Solutions: bonus chapter"; end card holds ~8 s.

Clips c5.ex.11, c5.ex.12, c5.recap.1 - c5.recap.3 (the lecture's last scene).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import restyle, settle  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import (  # noqa: E402  the shared exercise-card kit
    COL_X, CURRENT, DONE, HeroCard, at_row, enter_card, exit_card, fit, hint_label,
    make_strip, pause_tag, split_line,
)

# ── exercise 3.5 ─────────────────────────────────────────────────────────────────
RESULT = "[[1; 2; 3]; [2; 3]; [3]; []]"
TAILS = ["[1; 2; 3]", "[2; 3]", "[3]", "[]"]
SUFFIX = ["[1; 2; 3]", "2; 3]", "3]"]       # where each tail starts inside the input
RES_Y = -0.2                                 # the result row (card at the top)
S = 0.85                                     # the hint's chain 1 -> 2 -> 3 -> []
HINT_Y = -2.5
BONUS_X = 0.9

# ── recap ────────────────────────────────────────────────────────────────────────
TITLE_Y = 3.25
ROW_TOP, ROW_PITCH = 2.3, 0.68
ICON_W, ICON_GAP = 1.9, 0.35                 # icon column, then the row's words
END_Y = -2.95
DIM_ROW = 0.5


def tail_box(chain, k, pad=0.16):
    """The TEAL box around tail k of the chain (k = 3: just the nil)."""
    first = chain.cells[k] if k < len(chain.cells) else chain.nil
    left, right = first.get_left()[0] - pad, chain.nil.get_right()[0] + pad
    h = chain.cells[0].box.height + 2 * pad
    box = RoundedRectangle(corner_radius=0.14, width=right - left, height=h)
    box.set_stroke(TEAL, 3).set_fill(opacity=0)
    return box.move_to([(left + right) / 2, chain.cells[0].box.get_y(), 0])


def cost(big, word, color=GOLD, size=34):
    """O(..) and its word, as in the ch3/ch4 recaps."""
    o = MathTex(big, font_size=size + 8, color=color)
    w = T(word, size=size, color=color)
    grp = VGroup(o, w).arrange(RIGHT, buff=0.2)
    w.align_to(o, DOWN).shift(UP * 0.06)
    return grp


def acc_icon():
    box = RoundedRectangle(corner_radius=0.1, width=1.05, height=0.5).set_stroke(GOLD, 2.5)
    return VGroup(box, Mono("acc", size=28, color=GOLD).move_to(box))


def recap_row(icon, parts, y):
    """Icon centred in the icon column, the words left-aligned after it."""
    body = VGroup(*parts).arrange(RIGHT, buff=0.22)
    icon.move_to([0, y, 0])
    body.move_to([ICON_W / 2 + ICON_GAP, y, 0], aligned_edge=LEFT)
    return VGroup(icon, *parts)


class ExercisesTailsRecap(NarratedScene):
    def construct(self):
        self.tails_card()
        self.tails_hint()
        self.recap()
        self.end_card()
        # End card: the finished recap and the way to the solutions hold under the music.
        self.wait(7.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)   # the last play() never renders its final (empty) frame

    # ex.11: the strip comes back (3.1-3.4 done); 3.5 grows; the four tails, one per beat
    def tails_card(self):
        strip = make_strip([DONE, DONE, DONE, DONE, CURRENT])
        card = HeroCard(4, height=3.5, slot_type="'a list -> 'a list list")
        task = at_row(T("Return every tail of a list.", size=34), 1)
        ex_in, ex_to = split_line("tails [1; 2; 3]  ⇒", ["tails [1; 2; 3]", "⇒"], k=2)
        res_x = ex_in.find("[")[0].get_left()[0]          # the tails line up under the input list
        full = Code(RESULT, size=40).move_to([res_x, RES_Y, 0], aligned_edge=LEFT)
        elems = split_line(RESULT, TAILS, size=40, x=res_x, y=RES_Y)
        skel = [full.find("[")[0].copy(), *[full.find("]; [", nth=k)[1].copy() for k in range(3)],
                full.find("]]")[1].copy()]
        ph_h = max(e.height for e in elems) + 0.2
        places = []
        for e in elems:
            r = RoundedRectangle(corner_radius=0.1, width=e.width + 0.22, height=ph_h).move_to(e)
            places.append(DashedVMobject(r, num_dashes=int(5 * (r.width + ph_h))).set_stroke(DIM, 2))
        card.lower(task, ex_in, ex_to, *skel, *places, *elems)
        slot = card.slot

        with self.say("c5.ex.11") as c:
            # "The last exercise is three point five."  From an empty frame: the strip, the card
            self.play(FadeIn(strip, lag_ratio=0.1), run_time=0.8)
            self.play(*enter_card(strip, card, light=False), run_time=1.2)
            # "Write a function called tails, which returns the list of all the tails of its argument."
            c.wait_until("task")
            self.play(FadeIn(task, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7),
                      run_time=1.1)
            c.wait_until("all the tails")
            self.play(FadeIn(slot.sig, shift=0.2 * DOWN), run_time=0.8)
            # "Given one, two, three, it returns four lists."
            c.wait_until("example")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), FadeIn(ex_to, shift=0.2 * LEFT),
                      run_time=fit(c, "four lists", hi=1.0))
            c.wait_until("four lists")
            self.play(LaggedStart(*[FadeIn(m) for m in (skel[0], places[0], skel[1], places[1], skel[2],
                                                        places[2], skel[3], places[3], skel[4])],
                                  lag_ratio=0.12), run_time=1.2)
            # "First, the whole list, one, two, three."  "Then two, three."  "Then the list
            # containing just three."  Each tail flies out of where it starts in the input.
            for k, cue in enumerate(("whole", "two", "three")):
                c.wait_until(cue)
                self.play(TransformFromCopy(VGroup(*ex_in.find(SUFFIX[k])), elems[k]), FadeOut(places[k]),
                          run_time=1.5 if k == 0 else 1.2)
            # "And finally, nil."
            c.wait_until("nil")
            self.play(FadeIn(elems[3], scale=0.8), FadeOut(places[3]),
                      FlashAround(elems[3], color=TEAL, buff=0.08), run_time=1.0)
        card.keep(task, slot.box, slot.q, slot.sig, ex_in, ex_to, *skel, *elems)
        self.strip, self.card, self.elems = strip, card, elems

    # ex.12: hint from chapter 1: tail after tail down to nil visits exactly these lists
    def tails_hint(self):
        card, elems = self.card, self.elems
        hl = hint_label(card, 1)
        chain = ConsChain([1, 2, 3]).scale(S).move_to([COL_X, HINT_Y, 0], aligned_edge=LEFT)
        boxes = [tail_box(chain, k) for k in range(4)]
        box = boxes[0].copy()
        bonus_lab = T("Bonus question:", size=32, color=DIM)
        bonus_q = T("How many new cons cells?", size=34, color=GOLD)
        bonus_lab.move_to([BONUS_X, HINT_Y + 0.33, 0], aligned_edge=LEFT)
        bonus_q.move_to([BONUS_X, HINT_Y - 0.33, 0], aligned_edge=LEFT)
        tag = pause_tag()

        with self.say("c5.ex.12") as c:
            # "The hint is in chapter one."  The card goes up; chapter 1's chain, its whole
            # list boxed.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.5, 1.2),
                      time_span(FadeIn(chain, lag_ratio=0.1), 0.8, 1.7),
                      time_span(Create(box), 1.3, 1.9), run_time=1.9)
            # "Remember taking the tail, then the tail of that, all the way down to nil?"
            c.wait_until("the tail")
            self.play(Transform(box, boxes[1]), run_time=fit(c, "tail of that", lo=0.5, hi=0.9))
            c.wait_until("tail of that")
            self.play(Transform(box, boxes[2]), run_time=fit(c, "all the way", lo=0.5, hi=0.9))
            c.wait_until("all the way")
            self.play(Transform(box, boxes[3]), run_time=max(0.8, min(1.5, c.until("nil") + 0.3)))
            # "That walk visits exactly these lists."
            c.wait_until("same")
            self.play(LaggedStart(*[AnimationGroup(e.animate.set_color(TEAL),
                                                   FlashAround(e, color=TEAL, buff=0.08))
                                    for e in elems], lag_ratio=0.3), run_time=2.0)
            # "And here's a bonus question to think about."
            c.wait_until("share")
            self.play(FadeIn(bonus_lab, shift=0.2 * DOWN), run_time=0.9)
            # "How many new cons cells does your answer really need to build?"
            c.wait_until("how many")
            self.play(FadeIn(bonus_q, shift=0.2 * DOWN), run_time=1.0)
            # "Pause, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.hint = [hl, chain, box, bonus_lab, bonus_q, tag]

    # recap.1-2: the big ideas of the lecture, one row per cue, the previous row stepping back
    def recap(self):
        strip, card = self.strip, self.card
        title = T("Recap", size=48).move_to([0, TITLE_Y, 0])
        ys = [ROW_TOP - ROW_PITCH * i for i in range(7)]

        cell = ConsCell(1).scale(0.68)            # its value stays readable (size 28)
        nrev = Code("nrev", size=32).set_color(YELLOW)
        rev_app = Code("rev_app", size=32).set_color(YELLOW)
        o_n = MathTex(r"O(n)", r"{:}", font_size=42)     # {:}: a tight colon, not a relation
        o_n[0].set_color(GOLD)
        spec = [   # (icon, words, how many of the words come in on the row's first cue)
            (cell, [T("Every list is", size=34), Code("[]", size=32), T("or", size=34),
                    Code("head :: tail", size=32), T("·", size=34, color=DIM), T("cons is", size=34),
                    MathTex(r"O(1)", font_size=42, color=GOLD)], 4),
            (Code("x :: xs", size=32), [T("Pattern matching: a case for each shape", size=34)], 1),
            (Code("'a 'b", size=32), [T("Polymorphism: one function, lists of any type", size=34)], 1),
            (acc_icon(), [T("An accumulator makes it iterative:", size=34), cost(r"O(1)", "space")], 1),
            (Mono("@", size=40, color=RED), [T("Append copies, so", size=34), nrev, T("is", size=34),
                                             MathTex(r"O(n^2)", font_size=42, color=RED)], 3),
            (Mono("::", size=40, color=TEAL), [rev_app, T("is", size=34), o_n,
                                               T("reduction in strength", size=34, color=YELLOW)], 3),
            (Code('"abc"', size=32), [T("Strings and chars: their own types, not lists", size=34,
                                        t2c={"their own types": GREEN})], 1),
        ]
        rows = [recap_row(icon, words, y) for (icon, words, _), y in zip(spec, ys)]
        split = [n for _, _, n in spec]
        right = max(r.get_right()[0] for r in rows)
        dx = -(right - ICON_W / 2) / 2                     # centre the block in the frame
        for r in rows:
            r.shift(RIGHT * dx)
        self.rows = rows

        def part(row, a, b, run_time, *extra):
            self.play(*[FadeIn(m, shift=0.25 * UP) for m in row[a:b]], *extra, run_time=run_time)

        def first(i, run_time=1.5, *extra):
            """Row i's icon and its first words; the row before steps back."""
            part(rows[i], 0, 1 + split[i], run_time, restyle(rows[i - 1], DIM_ROW), *extra)

        def rest(i, run_time=1.0, *extra):
            part(rows[i], 1 + split[i], len(rows[i]), run_time, *extra)
            settle(self, rows[i])

        with self.say("c5.recap.1") as c:
            # "That's the end of lecture three, so let's look back at the big ideas."
            # The card shrinks back into its pill; the strip gives way to the title.
            hint, tag = self.hint[:-1], self.hint[-1]
            c.wait_until("lecture three")
            self.play(*exit_card(strip, card, hint), run_time=1.1)
            self.remove(card.frame)
            self.play(LaggedStart(*[FadeOut(p) for p in strip], lag_ratio=0.1), FadeOut(tag),
                      time_span(FadeIn(title, shift=0.3 * DOWN), 0.3, 1.2), run_time=1.2)
            # "Every list is either nil, or a head consed onto a tail, and cons takes constant time."
            c.wait_until("r1")
            part(rows[0], 0, 1 + split[0], 1.5)
            c.wait_until("constant time")
            rest(0)
            # "Pattern matching takes lists apart, with a case for each shape."
            c.wait_until("r2")
            first(1)
            settle(self, rows[1])
            # "Polymorphic types, with alpha and beta, let a single function work on lists of any type."
            c.wait_until("r3")
            first(2)
            settle(self, rows[2])
            c.wait_until("alpha and beta")
            self.play(FlashAround(rows[2][0], color=PINK, buff=0.08), run_time=1.2)

        with self.say("c5.recap.2") as c:
            # "An accumulating argument makes a function iterative, so it runs in constant space."
            first(3)
            c.wait_until("constant space")
            rest(3)
            # "Append copies its whole first list, so the naive reverse costs big O of en squared."
            c.wait_until("r5")
            first(4)
            c.wait_until("big o")
            rest(4)
            # "Replacing append with cons brings that down to big O of en."  The @ becomes ::.
            c.wait_until("r6")
            self.play(TransformFromCopy(rows[4][0], rows[5][0]), restyle(rows[4], DIM_ROW), run_time=1.5)
            c.wait_until("brings that down")
            part(rows[5], 1, 1 + split[5], 1.2)
            # "That's called reduction in strength."
            c.wait_until("reduction in strength")
            strength = rows[5][-1]
            part(rows[5], len(rows[5]) - 1, len(rows[5]), 1.5,
                 time_span(FlashUnder(strength, color=YELLOW), 0.5, 1.5))
            settle(self, rows[5])
            # "And in OCaml, strings and characters are types of their own, not lists."
            c.wait_until("r7")
            first(6)
            settle(self, rows[6])

    # recap.3: the five exercises, and where their solutions are
    def end_card(self):
        rows = self.rows
        pills = make_strip([DONE] * 5)
        arrow = MathTex(r"\rightarrow", font_size=44, color=DIM)
        sol = VGroup(T("Solutions:", size=34, color=DIM), T("bonus chapter", size=34, color=YELLOW))
        sol.arrange(RIGHT, buff=0.2)
        VGroup(pills, arrow, sol).arrange(RIGHT, buff=0.35).move_to([0, END_Y, 0])
        sol[1].align_to(sol[0], UP)        # same ascenders: same baseline

        with self.say("c5.recap.3") as c:
            # "Now, try those five exercises yourself."  The whole recap back to full brightness.
            self.play(*[restyle(r, 1) for r in rows[:6]],
                      LaggedStart(*[FadeIn(p, shift=0.2 * UP) for p in pills], lag_ratio=0.15),
                      run_time=1.3)
            # "When you're ready, the bonus chapter walks through every solution, step by step."
            c.wait_until("the bonus chapter")
            self.play(FadeIn(arrow, shift=0.2 * RIGHT), FadeIn(sol, shift=0.2 * LEFT), run_time=1.2)
            # "See you there."
            c.wait_until("bye")
            self.play(FlashUnder(sol[1], color=YELLOW), run_time=1.2)
