"""Chapter 4, scene 2: append, the code. Matching on a pair, the two clauses, ys riding
along, the infix @, the polymorphic type, and the rejected mixed-type join.

Clips c4.code.1 - c4.code.5.

STATUS: done; vk check clean (96.0 s for 89.2 s of narration: 4.2 s hold at the end so the error can be read).
Layout: code.1 title / element boxes / `append [1; 2; 3] [4]` + reply (born from copies).
code.2-3 the definition (Code 40, left edge X0) is the hero, the example + reply shrink to a
reminder at the bottom; ONE P8 box: `xs, ys` ("a pair") -> `[], ys` -> `x::xs, ys` ->
`x :: append xs ys` -> `append xs ys` ("the smaller problem"). The tail `xs` (pattern + call)
goes PURPLE, not TEAL as the brief had it: TEAL is ys's colour from {ride} on, and YELLOW
would merge `append xs` and vanish in the YELLOW box.
code.4-5 a REPL-like column at X1: definition (x0.85) at the top, `let (@) = append` + its
reply, the example rewritten to `[1; 2; 3] @ [4]`, then replaced by the rejected
`[1; 2] @ ["three"]` with OCaml's carets and error (its line break moved after "string").
Verified with ocaml 5.4.1: definition gives `val append : 'a list -> 'a list -> 'a list = <fun>`;
append [1; 2; 3] [4] and [1; 2; 3] @ [4] give `- : int list = [1; 2; 3; 4]`;
`let (@) = append` gives `val ( @ ) : 'a list -> 'a list -> 'a list = <fun>`;
`[1; 2] @ ["three"]` gives characters 10-17 carets and
`Error: This constant has type string but an expression was expected of type int`.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = """let rec append xs ys =
  match xs, ys with
  | [], ys    -> ys
  | x::xs, ys -> x :: append xs ys"""
VAL = "val ( @ ) : 'a list -> 'a list -> 'a list = <fun>"

DEF_SZ = 40         # hero code size (as ch3_s2_nlength)
X0 = -5.8           # left edge of the definition and the reminder (code.2-3)
DEF_Y = 1.1        # the definition's centre (code.2-3)
X1 = -6.15          # left edge of the session column (code.4-5)
DEF_S = 0.85        # the definition shrinks to this at {infix}
LET_Y, VAL_Y = 0.3, -0.35
EX_Y, RE_Y = -1.5, -2.15


def at_left(mob, x, y):
    """Put mob's left edge at x and its centre at height y."""
    mob.move_to([0, y, 0])
    mob.shift((x - mob.get_left()[0]) * RIGHT)
    return mob


def elem_box(v, color):
    """A ch1-hook style element box: a rounded square holding a value."""
    sq = RoundedRectangle(corner_radius=0.12, width=1.0, height=1.0)
    sq.set_stroke(color, 4).set_fill(color, opacity=0.15)
    return VGroup(sq, value_label(v).move_to(sq))


def born(target, pairs, path_arc=0.0, shift=0.2 * DOWN):
    """Anims that build Code `target`: glyphs in `pairs` (src, dst) fly from copies of their
    sources, every other glyph fades in. Follow with settle(scene, target)."""
    flying = {id(d) for _, d in pairs}
    anims = [TransformFromCopy(s, d, path_arc=path_arc) for s, d in pairs]
    anims += [FadeIn(g, shift=shift) for g in target.text if id(g) not in flying]
    return anims


class AppendCode(NarratedScene):
    def construct(self):
        self.goal()
        self.the_code()
        self.clauses()
        self.ride_and_infix()
        self.the_type()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # code.1: what append should do, on boxes, then the example and OCaml's reply
    def goal(self):
        title = Mono("append", size=60, color=YELLOW).move_to(UP * 2.6)
        row = VGroup(*[elem_box(v, BLUE).scale(1.3) for v in (1, 2, 3)]).arrange(RIGHT, buff=0.15)
        four = elem_box(4, TEAL).scale(1.3)
        VGroup(row, four).arrange(RIGHT, buff=1.8).move_to(UP * 0.75)
        joined = VGroup(row.copy(), four.copy()).arrange(RIGHT, buff=0.15).move_to(UP * 0.75)

        ex = Code("append [1; 2; 3] [4]", size=44)
        ex.find("append").set_color(YELLOW)
        ex.find("[4]").set_color(TEAL)                 # ys is TEAL all chapter
        reply = Code("- : int list = [1; 2; 3; 4]", size=40)
        reply.find("int list").set_color(GREEN)
        left = -max(ex.width, reply.width) / 2
        at_left(ex, left, -1.3)
        at_left(reply, left, -2.15)
        self.title, self.row, self.four, self.ex, self.reply = title, row, four, ex, reply

        with self.say("c4.code.1") as c:
            # "Let's start with append."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.0)
            # "We want a function that takes two lists, ..."
            c.wait_until("two lists")
            self.play(FadeIn(row, shift=0.2 * DOWN, lag_ratio=0.2),
                      time_span(FadeIn(four, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            # "... and joins them end to end."
            c.wait_until("joins them")
            self.play(row.animate.move_to(joined[0]), four.animate.move_to(joined[1]),
                      run_time=min(1.6, 0.8 * c.until("example")))

            # "Append one, two, three, and the list holding just four, ..."
            c.wait_until("example")
            self.play(*born(ex, list(zip(title, ex.find("append"))), path_arc=0.0), run_time=1.6)
            settle(self, ex)
            # "... and you should get one, two, three, four."  The reply's elements come from the input.
            c.wait_until("you should get")
            pairs = [(ex.find(d)[0], reply.find(d)[0]) for d in "1234"]
            self.play(*born(reply, pairs, path_arc=-PI / 4), run_time=1.6)
            settle(self, reply)

    # code.2: the definition; matching on a pair
    def the_code(self):
        ex, reply = self.ex, self.reply
        code = Code(SRC, size=DEF_SZ)
        code.find("append", line=3).set_color(YELLOW)   # the name keeps its colour everywhere
        at_left(code, X0, DEF_Y)
        self.code = code

        ex.generate_target()
        ex.target.scale(0.8)
        at_left(ex.target, X0, -2.35)
        reply.generate_target()
        reply.target.scale(0.8)
        at_left(reply.target, X0, -3.0)

        pair = code.find("xs, ys", line=1)
        pair_lab = T("a pair", size=40, color=YELLOW)
        pair_lab.next_to(code.line(1), RIGHT, buff=0.6).set_y(code.line(1).get_y())
        self.pair_lab = pair_lab

        with self.say("c4.code.2") as c:
            # "Here's the definition."  The example steps down to a reminder.
            self.play(FadeOut(self.title), FadeOut(self.row), FadeOut(self.four),
                      MoveToTarget(ex), MoveToTarget(reply),
                      time_span(FadeIn(code, shift=0.3 * UP), 0.5, 1.8), run_time=1.8)

            # "Notice something new on the second line."
            c.wait_until("match")
            self.play(FlashUnder(code.line(1), color=YELLOW, time_width=1.5), run_time=1.5)

            # "Instead of matching a single list, we match two things at once, ..."
            c.wait_until("two things")
            self.play(time_span(FlashAround(code.find("xs", line=1), color=YELLOW, time_width=1.5), 0, 1.0),
                      time_span(FlashAround(code.find("ys", line=1), color=YELLOW, time_width=1.5), 0.4, 1.4),
                      run_time=1.4)

            # "... the pair, exes comma whys."  The one highlight box (P8) lands on the pair.
            c.wait_until("pair")
            box = token_box(pair, code.line(1))
            self.play(FadeIn(box), FadeIn(pair_lab, shift=0.3 * LEFT), run_time=1.0)
            self.box = box

            # "So each pattern describes both lists together."
            c.wait_until("patterns")
            pats = [code.find("[], ys", line=2), code.find("x::xs, ys", line=3)]
            self.play(time_span(FlashUnder(pats[0], color=YELLOW, time_width=1.5), 0, 1.2),
                      time_span(FlashUnder(pats[1], color=YELLOW, time_width=1.5), 0.5, 1.7),
                      run_time=1.7)
            # "Patterns can be as complicated as we like."  (hold)

    # code.3: the two clauses; the box walks them
    def clauses(self):
        code, box = self.code, self.box
        pat_ys, ans_ys = code.find("ys", line=2, nth=0), code.find("ys", line=2, nth=1)
        head, tail = code.find("x", line=3, nth=0), code.find("xs", line=3, nth=0)
        call_xs = code.find("xs", line=3, nth=1)
        call = code.find("append xs ys", line=3)

        tail_tag = T("the tail, not the whole list", size=32, color=DIM)
        tail_tag.move_to([tail.get_x(), code.line(3).get_y() - 0.78, 0])
        tail_tag.shift(max(0, X0 - tail_tag.get_left()[0]) * RIGHT)
        small_tag = T("the smaller problem", size=32, color=DIM)
        small_tag.move_to([call.get_x(), tail_tag.get_y(), 0])
        self.tags = [tail_tag, small_tag]

        with self.say("c4.code.3") as c:
            # "The first pattern matches when the first list is empty."
            self.play(Transform(box, token_box(code.find("[], ys", line=2), code.line(2))),
                      FadeOut(self.pair_lab), run_time=1.2)
            # "Then the answer is simply whys."  ys flies from the pattern into the answer.
            c.wait_until("the answer is")
            self.play(*[TransformFromCopy(p, a, path_arc=-PI / 2) for p, a in zip(pat_ys, ans_ys)],
                      run_time=1.6)
            settle(self, code)

            # "The second pattern matches when the first list has a head, ex, and a tail, exes."
            c.wait_until("step")
            self.play(Transform(box, token_box(code.find("x::xs, ys", line=3), code.line(3))),
                      run_time=1.4)
            c.wait_until("a head")
            self.play(FlashAround(head, color=YELLOW, time_width=1.5), run_time=0.9)
            c.wait_until("a tail")
            self.play(FlashAround(tail, color=YELLOW, time_width=1.5), run_time=0.9)

            # "Careful, these are new names."  The tail xs (and its use) take a colour of their own
            # (PURPLE: TEAL is ys's from {ride} on; YELLOW would merge into `append`).
            c.wait_until("fresh")
            self.play(*recolor(tail, PURPLE), *recolor(call_xs, PURPLE), run_time=1.0)
            # "Here, exes means just the tail of the first list."
            c.wait_until("just the tail")
            self.play(FadeIn(tail_tag, shift=0.3 * UP), run_time=1.0)

            # "So the answer is ex, consed onto the append of that tail and whys."
            c.wait_until("result")
            self.play(Transform(box, token_box(code.find("x :: append xs ys", line=3), code.line(3))),
                      run_time=1.2)
            c.wait_until("the append of")
            self.play(Transform(box, token_box(call, code.line(3))),
                      FadeIn(small_tag, shift=0.3 * UP), run_time=min(1.2, 0.9 * c.until(None)))

    # code.4: ys rides along; the infix operator
    def ride_and_infix(self):
        code, box, ex, reply = self.code, self.box, self.ex, self.reply
        ys_all = [code.find("ys", line=0), code.find("ys", line=1),
                  code.find("ys", line=2, nth=0), code.find("ys", line=2, nth=1),
                  code.find("ys", line=3, nth=0), code.find("ys", line=3, nth=1)]

        code.generate_target()
        code.target.scale(DEF_S)
        code.target.shift(np.array([X1, 3.45, 0]) - code.target.get_corner(UL))
        ex.generate_target()
        ex.target.scale(40 / 35.2)
        at_left(ex.target, X1, EX_Y)
        reply.generate_target()
        reply.target.scale(30 / 32)
        at_left(reply.target, X1, RE_Y)

        let = Code("let (@) = append", size=40)
        let.find("append").set_color(YELLOW)
        at_left(let, X1, LET_Y)
        val = Code(VAL, size=30)
        alphas = [val.find("'a", nth=k) for k in range(3)]
        for a in alphas:
            a.set_color(FG)                              # they turn PINK one by one in code.5
        at_left(val, X1, VAL_Y)
        ex2 = Code("[1; 2; 3] @ [4]", size=40)
        ex2.find("[4]").set_color(TEAL)
        self.let, self.val, self.alphas = let, val, alphas

        with self.say("c4.code.4") as c:
            # "Notice that whys just comes along for the ride."  Every ys turns TEAL, top to bottom.
            self.play(*[time_span(g.animate.set_color(TEAL), 0.3 * k, 0.3 * k + 0.8)
                        for k, ys in enumerate(ys_all) for g in ys], run_time=2.3)
            # "Append never takes it apart, ..."  Its patterns only ever name it.
            c.wait_until("takes it apart")
            self.play(time_span(FlashAround(ys_all[2], color=TEAL, time_width=1.5), 0, 1.1),
                      time_span(FlashAround(ys_all[4], color=TEAL, time_width=1.5), 0.3, 1.4),
                      run_time=1.4)

            # "For convenience, we turn append into an operator."
            c.wait_until("infix")
            self.play(FadeOut(box), *[FadeOut(t) for t in self.tags],
                      time_span(MoveToTarget(code), 0.4, 2.0),
                      time_span(MoveToTarget(ex), 0.4, 2.0), time_span(MoveToTarget(reply), 0.4, 2.0),
                      run_time=2.0)

            # "Let the at sign, in brackets, equal append."
            c.wait_until("at")
            self.play(*born(let, list(zip(code.find("append", line=0), let.find("append"))),
                            path_arc=PI / 6), run_time=1.5)
            settle(self, let)
            c.wait_until("equal append")
            self.play(FadeIn(val, shift=0.2 * DOWN), run_time=min(1.0, 0.8 * c.until("use")))

            # "The brackets mark it as an operator, ..."
            c.wait_until("use")
            self.play(FlashAround(let.find("(@)"), color=YELLOW, time_width=1.5), run_time=1.1)
            # "... so now it goes between the two lists."  The example is rewritten; same reply.
            c.wait_until("goes between")
            at_left(ex2, X1, ex.get_y())
            self.play(TransformMatchingStrings(ex, ex2), run_time=min(1.5, 0.9 * c.until(None)))
        self.ex2 = ex2

    # code.5: the polymorphic type; a mixed-type join is rejected
    def the_type(self):
        code, val, alphas, ex2, reply = self.code, self.val, self.alphas, self.ex2, self.reply
        bad = Code('[1; 2] @ ["three"]', size=40)
        at_left(bad, X1, EX_Y)
        three = bad.find('"three"')
        carets = Mono("^^^^^^^", size=40, color=RED)
        carets.next_to(three, DOWN, buff=0.06).set_x(three.get_x())
        err = VGroup(Mono("Error: This constant has type string", size=30, color=RED),
                     Mono("but an expression was expected of type int", size=30, color=RED))
        err.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        err.next_to(carets, DOWN, buff=0.3)
        err.shift((X1 - err.get_left()[0]) * RIGHT)

        with self.say("c4.code.5") as c:
            # "Now look at the type in OCaml's reply."
            self.play(*set_alpha([code, ex2, reply], DIMMED),
                      time_span(FlashUnder(val.find("'a list -> 'a list -> 'a list"), color=GREEN,
                                           time_width=1.5), 0.3, 1.6), run_time=1.6)

            # "It takes an alpha list, and another alpha list, and returns an alpha list."
            for k, cue in enumerate(("takes an alpha", "another alpha", "returns an alpha")):
                c.wait_until(cue)
                self.play(*recolor(alphas[k], PINK),
                          FlashAround(alphas[k], color=PINK, time_width=1.5, buff=0.08),
                          run_time=1.0 if k == 0 else 0.8)

            # "The same alpha all three times."
            c.wait_until("same")
            self.play(*[time_span(FlashAround(a, color=PINK, time_width=1.5, buff=0.08),
                                  0.25 * k, 0.25 * k + 1.0) for k, a in enumerate(alphas)],
                      run_time=1.5)
            # "So you can join any two lists, as long as their elements have the same type."  (hold)

            # "Try joining integers to strings, ..."
            c.wait_until("bad")
            self.play(FadeOut(ex2), FadeOut(reply),
                      time_span(FadeIn(bad, shift=0.2 * DOWN), 0.3, 1.2), run_time=1.2)
            # "... and OCaml rejects it, before the program even runs."  Its reply, word for word.
            c.wait_until("reject")
            self.play(*recolor(three, RED), FadeIn(carets, shift=0.15 * UP),
                      time_span(FadeIn(err, shift=0.2 * DOWN, lag_ratio=0.3), 0.2, 1.0), run_time=1.0)
        self.wait(4.2)                                   # let the error be read before the fade
