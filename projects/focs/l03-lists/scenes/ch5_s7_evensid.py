"""STATUS (paused): done: ex.6-ex.10 rendered (104 s), dwell 0 flags, reviewed at 480p.
remaining: one more look at the final render after the last small layout tweaks (3.3 rows
nudged down, 3.4 hint copies up 0.08). known issues: 3.4 card code is size 28 (the id/loop
grid only fits at 28); cues avoid the word "eye-dee" except via first_cue(c, "id", "eye-dee").

Chapter 5, scene 7: exercise 3.3 (the even-numbered elements) and exercise 3.4 (two
strange types, id and loop). Same card system as ch5_s6: the card grows out of its pill,
task / example / GOLD "?", then one hint below and a still "pause and try it" beat.
Never a solution, and for 3.4 never the types or values of the two test expressions.

Clips c5.ex.6 - c5.ex.10.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import (  # noqa: E402  the shared exercise-card kit
    CARD_R, COL_X, CURRENT, DONE, TODO, HeroCard, at_row, enter_card, exit_card, finish,
    first_cue, fit, hint_label, hold_for, make_strip, pause_tag, row_y, split_line,
)

PINKS = ["#F6C4EE", PINK, "#C564B4"]   # three shades of 'a: each use of id gets its own


def chars(code, ch):
    """Every glyph of `code` that is the character `ch`."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


class ExercisesEvensId(NarratedScene):
    def construct(self):
        self.evens_card()
        self.evens_hint()
        self.types_card()
        self.types_ask()
        self.types_hint()
        hold_for(self, self.pause_born, len("pause and try it"))
        finish(self)

    # ex.6: the strip comes back (3.1, 3.2 done); 3.3 grows: task, two examples, positions
    def evens_card(self):
        strip = make_strip([DONE, DONE, CURRENT, TODO, TODO])
        card = HeroCard(2, height=3.32, slot_type="'a list -> 'a list")
        task = at_row(T("Keep the even-numbered elements.", size=34), 1)
        e1_in, e1_out = split_line("[a; b; c; d]  ⇒  [b; d]", ["[a; b; c; d]", "⇒  [b; d]"], y=0.55)
        e2_in, e2_out = split_line("[1; 2; 3; 4; 5]  ⇒  [2; 4]", ["[1; 2; 3; 4; 5]", "⇒  [2; 4]"], y=-0.2)
        letters = [e1_in.find(ch)[0] for ch in "abcd"]
        nums = [T(str(k + 1), size=28, color=DIM).move_to([g.get_x(), 0.99, 0]) for k, g in enumerate(letters)]
        kept_out = [e1_out.find(ch)[0] for ch in "bd"]
        card.lower(task, e1_in, e1_out, e2_in, e2_out, *nums)
        slot = card.slot

        with self.say("c5.ex.6") as c:
            # "Exercise three point three."  From an empty frame: the strip, then the card
            self.play(FadeIn(strip, lag_ratio=0.1), run_time=0.8)
            self.play(*enter_card(strip, card, light=False), run_time=1.2)
            # "Write a function that returns the even-numbered elements of a list."
            c.wait_until("task")
            self.play(FadeIn(task, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7), run_time=1.1)
            c.wait_until("of a list")
            self.play(FadeIn(slot.sig, shift=0.2 * DOWN), run_time=0.8)
            # "Given A, B, C, D, it should return B, D."
            c.wait_until("given")
            self.play(FadeIn(e1_in, shift=0.25 * DOWN), run_time=fit(c, "return", hi=1.0))
            c.wait_until("return")
            self.play(FadeIn(e1_out, shift=0.25 * LEFT), run_time=0.8)
            # "Counting from the front, that's the second element and the fourth."
            c.wait_until("count")
            self.play(LaggedStart(*[FadeIn(n, shift=0.2 * DOWN) for n in nums], lag_ratio=0.3), run_time=1.3)
            for k, cue in ((1, "second"), (3, "fourth")):
                c.wait_until(cue)
                out = kept_out[0 if k == 1 else 1]
                self.play(nums[k].animate.set_color(GOLD), letters[k].animate.set_color(GOLD),
                          out.animate.set_color(GOLD), FlashAround(letters[k], color=GOLD, buff=0.06),
                          run_time=0.8)
            # "And given one, two, three, four, five, you'd get two and four."
            c.wait_until("given", nth=1)
            self.play(FadeIn(e2_in, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("two and four")
            self.play(FadeIn(e2_out, shift=0.25 * LEFT), run_time=0.8)
        card.keep(task, slot.box, slot.q, slot.sig, e1_in, e1_out, *nums, e2_in, e2_out)
        self.strip, self.card = strip, card

    # ex.7: hint: a pattern can take two elements at once; then the lists too short for it
    def evens_hint(self):
        card = self.card
        hl = hint_label(card)
        # "x ::" stays put while "xs" turns into "y :: rest" (P5: the new pattern grows out of
        # the old one)
        head, xs = split_line("x :: xs", ["x ::", "xs"], size=48, x=-5.4, y=-1.85)
        _, tail = split_line("x :: y :: rest", ["x ::", "y :: rest"], size=48, x=-5.4, y=-1.85)
        b_one = Brace(head.find("x"), DOWN, buff=0.1, color=DIM)
        l_one = T("one", size=30, color=DIM).next_to(b_one, DOWN, buff=0.08)
        parts = [("x", "first", FG), ("y", "second", GOLD), ("rest", "the rest", TEAL)]
        braces, labels = [], []
        for sub, word, color in parts:
            b = Brace(VGroup(*(head if sub == "x" else tail).find(sub)), DOWN, buff=0.1, color=color)
            braces.append(b)
            labels.append(T(word, size=30, color=color).next_to(b, DOWN, buff=0.08))
        labels[2].align_to(labels[0], DOWN)
        labels[1].align_to(labels[0], DOWN)

        short_lab = T("too short to match", size=30, color=DIM)
        rows = []
        for src in ("[]", "[a]"):
            r = VGroup(Code(src + "  ⇒", size=40), T("?", size=52, color=GOLD)).arrange(RIGHT, buff=0.3)
            rows.append(r)
        rows[1][0].align_to(rows[0][0], RIGHT)
        rows[1][1].align_to(rows[0][1], LEFT)
        short = VGroup(short_lab, *rows).arrange(DOWN, buff=0.3)
        for r in rows:
            r.align_to(short_lab, LEFT).shift(RIGHT * 0.3)
        short.move_to([3.9, -2.2, 0])
        tag = pause_tag()

        with self.say("c5.ex.7") as c:
            # "Here's the hint."  The card goes up to make room.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            # "So far, our patterns have taken a single element off the front."
            c.wait_until("front")
            self.play(FadeIn(head, shift=0.25 * UP), FadeIn(xs, shift=0.25 * UP),
                      run_time=fit(c, "single element", hi=1.2))
            c.wait_until("single element")
            self.play(GrowFromCenter(b_one), FadeIn(l_one, shift=0.2 * DOWN), run_time=1.0)
            # "But a pattern can take two at once."  (the pattern grows a second head, P5)
            c.wait_until("two at once")
            self.play(FadeTransform(xs, tail), run_time=1.3)
            # "Ex, cons why, cons the rest."  (one brace per part, as it's named)
            c.wait_until(first_cue(c, "ex cons why", "cons why"))
            # ("one" becomes "first"; then "second" and "the rest" drop in)
            self.play(ReplacementTransform(b_one, braces[0]), FadeTransform(l_one, labels[0]),
                      run_time=fit(c, "why", lo=0.5, hi=0.8, frac=0.9))
            self.play(LaggedStart(*[AnimationGroup(GrowFromCenter(b), FadeIn(lab, shift=0.2 * DOWN))
                                    for b, lab in zip(braces[1:], labels[1:])], lag_ratio=0.6),
                      run_time=max(1.3, c.until("rest") + 0.5))
            # "Then ask what to do with the short lists that pattern doesn't match."
            c.wait_until("left")
            self.play(FadeIn(short_lab, shift=0.2 * DOWN), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r, shift=0.2 * LEFT) for r in rows], lag_ratio=0.4), run_time=1.2)
            # "Pause, and try it."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time
        # (each piece listed as it was shown, so the fade-out takes exactly what's on screen)
        self.hint = [hl, head, tail, *braces, *labels, short_lab, *rows]
        self.tag = tag

    # ex.8: 3.4 grows: id and loop, each with OCaml's reply
    def types_card(self):
        strip = self.strip
        card = HeroCard(3, height=4.12)
        y_id, y_loop = row_y(0) - 0.7, row_y(0) - 1.26
        reply_x = COL_X + 5.83
        id_def = Code("let id x = x", size=28).move_to([COL_X, y_id, 0], aligned_edge=LEFT)
        id_val = Code("val id : 'a -> 'a = <fun>", size=28).move_to([reply_x, y_id, 0], aligned_edge=LEFT)
        lp_def = Code("let rec loop x = loop x", size=28).move_to([COL_X, y_loop, 0], aligned_edge=LEFT)
        lp_val = Code("val loop : 'a -> 'b = <fun>", size=28).move_to([reply_x, y_loop, 0], aligned_edge=LEFT)
        lp_val.align_to(id_val, LEFT)
        tag = card.tag("about types", GREEN)
        xs = [id_def.find("x", nth=0)[0], id_def.find("x", nth=1)[0]]
        name, body = VGroup(*lp_def.find("loop", nth=0)), VGroup(*lp_def.find("loop", nth=1))
        calls = CurvedArrow(body.get_bottom() + DOWN * 0.06, name.get_bottom() + DOWN * 0.06,
                            angle=-PI / 2.6, color=YELLOW, stroke_width=3, tip_length=0.14)
        self.parts = dict(id_def=id_def, id_val=id_val, lp_def=lp_def, lp_val=lp_val)
        card.lower(id_def, id_val, lp_def, lp_val, calls)

        with self.say("c5.ex.8") as c:
            # "Exercise three point four is different."
            self.play(*exit_card(strip, self.card, self.hint), run_time=1.1)
            self.remove(self.card.frame)
            self.play(*enter_card(strip, card), run_time=1.2)
            # "It's about types."
            c.wait_until("about types")
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=0.9)
            # "Here's a function called eye-dee, short for identity."
            c.wait_until(first_cue(c, "id", "eye-dee"))
            self.play(FadeIn(id_def, shift=0.25 * DOWN), FadeOut(self.tag), run_time=1.0)
            # "It just hands back its argument."  (the x that goes in is the x that comes out)
            c.wait_until("hands back")
            self.play(*[FlashAround(g, color=YELLOW, buff=0.05) for g in xs],
                      *[g.animate.set_color(YELLOW) for g in xs], run_time=1.0)
            # "Its type is alpha to alpha."
            c.wait_until("idtype")
            self.play(FadeIn(id_val, shift=0.25 * LEFT), run_time=1.0)
            c.wait_until("alpha to alpha")
            self.play(*[FlashAround(VGroup(*id_val.find("'a", nth=k)), color=PINK, buff=0.05) for k in range(2)],
                      run_time=1.0)
            # "And here's a function called loop, which calls itself, forever."
            c.wait_until("loop")
            self.play(FadeIn(lp_def, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("calls itself")
            self.play(Create(calls), run_time=1.2)
            # "Its type is alpha to beta."
            c.wait_until("looptype")
            self.play(FadeIn(lp_val, shift=0.25 * LEFT), run_time=1.0)
            c.wait_until("beta")
            self.play(FlashAround(VGroup(*lp_val.find("'b")), color=PINK, buff=0.05), run_time=0.9)
        card.keep(tag, id_def, id_val, lp_def, lp_val, calls)
        self.card, self.calls = card, calls

    # ex.9: the job, and the two strange expressions, each with its type left as a GOLD "?"
    def types_ask(self):
        card = self.card
        dy = card.drop_y
        task = T("Why do these types make sense, and stay safe at run time?", size=32)
        task.move_to([COL_X, row_y(0) - 2.14 - dy, 0], aligned_edge=LEFT)
        y_ex = row_y(0) - 2.84 - dy
        e_id = Code("id [id [id 0]]", size=34)
        e_lp = Code("loop true / loop 3", size=34)
        q_id = VGroup(Code(":", size=34), T("?", size=46, color=GOLD)).arrange(RIGHT, buff=0.3)
        q_lp = q_id.copy()
        g_id = VGroup(e_id, q_id).arrange(RIGHT, buff=0.4)
        g_lp = VGroup(e_lp, q_lp).arrange(RIGHT, buff=0.4)
        for g in (q_id, q_lp):
            g[1].align_to(g[0], DOWN).shift(DOWN * 0.02)
        g_id.move_to([COL_X, y_ex, 0], aligned_edge=LEFT)
        g_lp.move_to([COL_X + 6.2, y_ex, 0], aligned_edge=LEFT)
        slash = e_lp.find("/")[0]
        note = T("/ is integer division", size=28, color=DIM)
        note.move_to([slash.get_x() + note.width / 2 - 0.1, y_ex - 0.52, 0])

        with self.say("c5.ex.9") as c:
            # "Your job is to explain why these types make sense, and why they can never lead
            # to a type error at run time."
            self.play(FadeIn(task, shift=0.25 * DOWN), run_time=1.2)
            # "Even for strange expressions, like eye-dee, applied to a list containing ..."
            c.wait_until("like")
            self.play(FadeIn(e_id, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("zero")
            self.play(FadeIn(q_id, shift=0.2 * LEFT), run_time=0.8)
            # "Or loop true, divided by loop three."
            c.wait_until("div")
            self.play(FadeIn(e_lp, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("three")
            self.play(FadeIn(q_lp, shift=0.2 * LEFT), run_time=0.8)
            # "The slash here is integer division."
            c.wait_until("slash")
            self.play(FlashAround(slash, color=YELLOW, buff=0.06), FadeIn(note, shift=0.2 * UP), run_time=1.0)
        card.keep(task, e_id, q_id, e_lp, q_lp, note)
        self.e_id, self.e_lp = e_id, e_lp

    # ex.10: hint from chapter 2: each id gets its own alpha, inside out; does loop return?
    def types_hint(self):
        card = self.card
        hl = hint_label(card, 2)
        big_id = Code("id [id [id 0]]", size=40).move_to([-3.3, -2.42, 0])
        ids = [VGroup(*big_id.find("id", nth=k)) for k in range(3)]
        alphas = [Mono("'a", size=32, color=col).next_to(i, DOWN, buff=0.22) for i, col in zip(ids, PINKS)]
        for a in alphas[1:]:
            a.align_to(alphas[0], DOWN)
        out = Arrow(alphas[2].get_right() + RIGHT * 0.3, alphas[0].get_left() + LEFT * 0.1, buff=0,
                    stroke_width=3, color=DIM, max_tip_length_to_length_ratio=0.15, tip_length=0.16)
        out.next_to(VGroup(*alphas), DOWN, buff=0.12)
        out_lab = T("inside out", size=28, color=DIM).next_to(out, RIGHT, buff=0.2)

        big_lp = Code("loop true", size=40).move_to([3.0, -2.42, 0])
        lp_name = VGroup(*big_lp.find("loop"))
        again = CurvedArrow(big_lp.get_right() + RIGHT * 0.15 + DOWN * 0.1,
                            lp_name.get_top() + UP * 0.12, angle=PI * 0.75,
                            color=YELLOW, stroke_width=3, tip_length=0.14)
        ever = T("does it ever return?", size=30, color=GOLD).next_to(big_lp, DOWN, buff=0.35)
        tag = pause_tag()

        with self.say("c5.ex.10") as c:
            # "The hint goes back to chapter two."  The card goes up.
            self.play(*card.lift(), time_span(FadeIn(hl, shift=0.25 * DOWN), 0.5, 1.3), run_time=1.3)
            # "Alpha can stand for any type, and each use of eye-dee gets to choose its own."
            c.wait_until("fresh")
            self.play(TransformFromCopy(self.e_id, big_id), run_time=1.5)
            c.wait_until("each use")
            self.play(LaggedStart(*[FadeIn(a, shift=0.2 * DOWN) for a in alphas], lag_ratio=0.4), run_time=1.5)
            # "So work from the inside out."
            c.wait_until("inside out")
            self.play(GrowArrow(out), FadeIn(out_lab, shift=0.2 * LEFT), run_time=1.0)
            # "And for loop, ask yourself a simple question. Does it ever actually return?"
            c.wait_until("ever")
            self.play(TransformFromCopy(VGroup(*self.e_lp.find("loop true")), big_lp), run_time=1.3)
            c.wait_until("does it ever")
            self.play(Create(again), FadeIn(ever, shift=0.2 * DOWN), run_time=1.2)
            # "Pause, and think it through."  Then the screen is still.
            c.wait_until("try")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.6)
        self.pause_born = self.time

