"""Chapter 4, scene 5: why stop at zero? Clips c4.zero.1 – c4.zero.3.

Scene 3's `change` comes back compact across the top (Code 26, left edge -6.45, top 3.45): the
two stopping clauses get tags, GREEN "success" and RED "failure"; `change [] 0` ⇒ `- : int list
= []` (the nil flies from clause 1). The success tag turns into the question "why stop at zero?"
and then into the answer. The end of scene 4's trace, in ch1_s3_trace's style (Code 40, pitch
0.84, DIM ⇒ column, each row born from copies of the one above), and the final `[]` glows TEAL,
"does nothing". The trace clears for the novice's `nchange` on a DIM-framed card (Code 28, centred:
it is 52 characters wide, so it cannot share the width with `change`), its `if amt = c then [c]`
RED, and its RED failure on zero. Then the chapter's quote card: YELLOW rule, smaller sign under.

STATUS: built; check clean apart from dwell notes: "does nothing" 4.8 s (needs 4.9), and the
nchange card / its RED failure (~6 s of the 7 asked), which stay up through "The course notes
draw a general lesson" and clear on "Most procedures". 77.3 s vs 71.8 s narration (3.5 s hold on
the quote card, then a 1 s fade to an empty frame).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CHANGE_SRC = """let rec change till amt =
  match till, amt with
  | _, 0         -> []
  | [], _        -> raise (Failure "no more coins!")
  | c::till, amt -> if amt < c then change till amt
                    else c :: change (c::till) (amt - c)"""

NCHANGE_SRC = """let rec nchange till amt =
  match till with
  | []      -> raise (Failure "no more coins!")
  | c::till -> if amt = c then [c]
               else if amt < c then nchange till amt
               else c :: nchange (c::till) (amt - c)"""

CODE_SIZE, CODE_LEFT, CODE_TOP = 26, -6.45, 3.3
CODE_DIM = 0.4

EX_BASE = -1.5                         # baseline of `change [] 0` ⇒ reply
ROWS = ["change [1] 1", "1 :: change [1] 0", "1 :: []"]
SIZE = 40
BASE = [-0.7, -1.54, -2.38]
ARROW_GAP = 0.3

CARD_SIZE = 28
CALL = "nchange [50; 20; 10; 5; 2; 1] 0"
FAIL = 'Exception: Failure "no more coins!".'

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── helpers (ch1_s3_trace's, so the traces look the same) ───────────────────────
def baseline(code):
    """y of the text baseline of a Code."""
    chars_ = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars_, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Move a Code so its left edge is at x=left and its baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def G(code, sub, nth=0, line=None):
    """The glyphs of `sub` in `code`, as a fresh VGroup."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def implies(size=64):
    return MathTex(r"\Rightarrow", font_size=size, color=DIM)


def light(code, lines, op):
    """Lines of `code` brightening (op=1) or stepping back (op=CODE_DIM), glyph by glyph."""
    return [g.animate.set_opacity(op) for i in lines for g in code.line(i)]


class WhyZero(NarratedScene):
    def construct(self):
        self.build()
        self.two_stops()      # c4.zero.1
        self.why_zero()       # c4.zero.2
        self.the_novice()     # c4.zero.3
        self.wait(3.5)        # the quote card gets its reading time
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── layout, built up front ────────────────────────────────────────────────
    def build(self):
        code = Code(CHANGE_SRC, size=CODE_SIZE)
        code.shift(RIGHT * (CODE_LEFT - code.get_left()[0]) + UP * (CODE_TOP - code.get_top()[1]))
        self.code = code

        self.tag_s = T("success", size=30, color=GREEN).next_to(
            VGroup(*code.line(2)), RIGHT, buff=0.4)
        self.tag_f = T("failure", size=30, color=RED).next_to(
            VGroup(*code.line(3)), RIGHT, buff=0.3)
        self.clause1 = G(code, "_, 0         -> []", line=2)

        # change [] 0  ⇒  - : int list = []
        self.inp = Code("change [] 0", size=SIZE)
        self.rep = Code("- : int list = []", size=SIZE)
        self.ex_arrow = implies()
        w = self.inp.width + self.ex_arrow.width + self.rep.width + 2 * ARROW_GAP
        put(self.inp, -w / 2, EX_BASE)
        self.ex_arrow.next_to(self.inp, RIGHT, buff=ARROW_GAP).set_y(EX_BASE + 0.13)
        put(self.rep, self.ex_arrow.get_right()[0] + ARROW_GAP, EX_BASE)

        # the end of scene 4's trace
        rows = [Code(s, size=SIZE) for s in ROWS]
        G(rows[0], "1", 0).set_color(FG)                  # coins FG, the amount GOLD
        G(rows[1], "1", 0).set_color(FG)
        G(rows[1], "1", 1).set_color(FG)
        G(rows[2], "1", 0).set_color(FG)
        aw = implies().width
        left = -(rows[1].width + aw + ARROW_GAP) / 2
        x0 = left + aw + ARROW_GAP
        for r, b in zip(rows, BASE):
            put(r, x0, b)
        self.rows = rows
        self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.13)
                                for r, b in zip(rows[1:], BASE[1:])]
        self.tag_n = T("does nothing", size=30, color=TEAL).next_to(
            G(rows[2], "[]"), DOWN, buff=0.3)

        # the novice's card
        card = Code(NCHANGE_SRC, size=CARD_SIZE).move_to([0, 1.05, 0])
        frame = RoundedRectangle(corner_radius=0.15, width=card.width + 0.7,
                                 height=card.height + 0.6, stroke_color=DIM, stroke_width=2)
        frame.move_to(card)
        self.card, self.frame = card, frame
        self.card_label = T("a base case of one", size=34).next_to(frame, UP, buff=0.15)
        self.card_label.align_to(frame, LEFT).shift(0.1 * RIGHT)
        self.work = G(card, "if amt = c then [c]", line=3)
        self.tag_w = T("the base case builds a list", size=30, color=RED).next_to(
            frame, DOWN, buff=0.3)
        self.tag_w.set_x(self.work.get_x())

        self.call = Code(CALL, size=32)
        self.fail = Code(FAIL, size=32).set_color(RED)
        self.fail_arrow = implies(52)
        fw = self.fail_arrow.width + ARROW_GAP + self.fail.width
        fx = -fw / 2 + self.fail_arrow.width + ARROW_GAP
        put(self.call, fx, -2.05)
        put(self.fail, fx, -2.8)
        self.fail_arrow.next_to(self.fail, LEFT, buff=ARROW_GAP).set_y(-2.8 + 0.11)

        # the quote card
        self.notes = T("from the course notes", size=30, color=DIM)
        self.q1 = T("Most procedures are simplest", size=50, color=YELLOW)
        self.q2 = T("when their base case does nothing.", size=50, color=YELLOW)
        self.rule = Line(3.2 * LEFT, 3.2 * RIGHT, stroke_color=DIM, stroke_width=2)
        self.s1 = T("A base case of one instead of zero", size=36)
        self.s2 = T("is often a sign of a novice.", size=36)
        self.q1.next_to(self.notes, DOWN, buff=0.5)
        self.q2.next_to(self.q1, DOWN, buff=0.22)
        self.rule.next_to(self.q2, DOWN, buff=0.55)
        self.s1.next_to(self.rule, DOWN, buff=0.5)
        self.s2.next_to(self.s1, DOWN, buff=0.2)
        quote = VGroup(self.notes, self.q1, self.q2, self.rule, self.s1, self.s2)
        quote.move_to([0, 0.15, 0])

    # ── zero.1: two ways to stop; the clauses are tried in order ────────────────
    def two_stops(self):
        code = self.code
        with self.say("c4.zero.1") as c:
            # "So there are two ways for change to stop."
            self.play(FadeIn(code, shift=0.2 * DOWN), run_time=1.0)
            self.play(*light(code, [0, 1, 4, 5], CODE_DIM),
                      run_time=min(1.0, 0.8 * c.until("success")))

            # "If the amount reaches zero, that's success."
            c.wait_until("success")
            self.play(FadeIn(self.tag_s, shift=0.3 * LEFT),
                      FlashUnder(self.clause1, color=GREEN, time_width=1.5),
                      run_time=min(1.4, 0.9 * c.until("failure")))

            # "If the till runs out first, that's failure, and the exception."
            c.wait_until("failure")
            self.play(FadeIn(self.tag_f, shift=0.3 * LEFT),
                      FlashUnder(G(code, "[], _        -> raise (Failure \"no more coins!\")",
                                   line=3), color=RED, time_width=1.5),
                      run_time=min(1.4, 0.9 * c.until("order")))

            # "The clauses are tried in order, so an empty till with nothing owed still counts
            #  as success."
            c.wait_until("order")
            self.box = token_box(self.clause1, VGroup(*code.line(2)), color=YELLOW)
            self.play(FadeIn(self.inp, shift=0.3 * DOWN),
                      FadeIn(self.box),
                      run_time=min(1.2, 0.9 * c.until("still counts")))
            c.wait_until("still counts")
            self.play(FlashAround(self.tag_s, color=GREEN, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("even from")))

            # "Even from an empty till, change for zero gives nil, the empty list."
            c.wait_until("even from")
            nil = G(self.rep, "[]")
            rest = G(self.rep, "- : int list =")
            self.play(FadeIn(self.ex_arrow, shift=0.2 * RIGHT),
                      FadeIn(rest, shift=0.2 * RIGHT),
                      TransformFromCopy(G(code, "[]", line=2), nil, path_arc=-0.7),
                      run_time=min(1.8, 0.9 * c.remaining))
            self.remove(nil, rest)
            self.add(self.rep)

    # ── zero.2: why zero? The last coin goes in like any other; the base case does nothing
    def why_zero(self):
        code, r, a = self.code, self.rows, self.arrows
        q = T("why stop at zero?", size=30, color=YELLOW).move_to(self.tag_s, aligned_edge=LEFT)
        ans = T("the simplest way to stop", size=30, color=YELLOW).move_to(
            self.tag_s, aligned_edge=LEFT)
        with self.say("c4.zero.2") as c:
            # "Nobody ever asks for change for zero."
            self.play(FlashAround(G(self.inp, "0"), color=GOLD, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("so why")))

            # "So why is that the base case?"
            c.wait_until("so why")
            self.play(FadeOut(self.inp), FadeOut(self.ex_arrow), FadeOut(self.rep),
                      FadeTransform(self.tag_s, q),
                      run_time=min(1.2, 0.9 * c.until("simple")))

            # "Because it's the simplest way to make the algorithm stop."
            c.wait_until("simple")
            self.play(FadeTransform(q, ans), run_time=min(1.5, 0.9 * c.until("last")))
            self.ans = ans

            # "Look at the last coin from our trace."
            c.wait_until("last")
            self.play(*light(code, [3], CODE_DIM), self.tag_f.animate.set_opacity(CODE_DIM),
                      FadeIn(r[0], shift=0.3 * DOWN),
                      run_time=min(1.2, 0.9 * c.until("the one went")))

            # "The one went in just like every other coin, and left zero behind."
            c.wait_until("the one went")
            self.birth(r[1], a[1], [(G(r[0], "1", 0), "1", 0, -0.9),
                                    (G(code, "::", line=5), "::", 0, 0.6),
                                    (G(r[0], "change"), "change", 0, 0),
                                    (G(r[0], "[1]"), "[1]", 0, 0),
                                    (G(r[0], "1", 1), "0", 0, 0)],
                       extra=light(code, [5], 1.0),
                       run_time=min(1.8, 0.9 * c.until("left zero behind")))
            c.wait_until("left zero behind")
            self.play(FlashAround(G(r[1], "0"), color=GOLD, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("nothing")))

            # "Then the base case does nothing at all.  It just returns nil."
            c.wait_until("nothing")
            self.birth(r[2], a[2], [(G(r[1], "1 ::"), "1 ::", 0, 0),
                                    (G(r[1], "change [1] 0"), "[]", 0, 0)],
                       extra=[*light(code, [5], CODE_DIM),
                              time_span(FlashAround(G(r[2], "[]"), color=TEAL, time_width=1.5),
                                        1.0, 2.1),
                              time_span(FlashAround(G(code, "[]", line=2), color=TEAL,
                                                    time_width=1.5), 1.0, 2.1),
                              time_span(FadeIn(self.tag_n, shift=0.3 * UP), 1.0, 1.8)],
                       span=1.2, run_time=2.1)

    def birth(self, dst, arrow, pairs, extra=(), span=None, run_time=1.5):
        """A trace row born from the one above (ch1_s3_trace): shared parts copied down, the
        coin and the new `::` flying in on an arc."""
        anims, targets = [], []
        for src, d_sub, d_nth, arc in pairs:
            t = G(dst, d_sub, d_nth)
            anims.append(TransformFromCopy(src, t, path_arc=arc))
            targets.append(t)
        anims.append(FadeIn(arrow, shift=0.2 * DOWN))
        if span is not None:                      # the birth in the first `span` seconds only
            anims = [time_span(an, 0, span) for an in anims]
        self.play(*anims, *extra, run_time=run_time)
        self.remove(*targets)
        self.add(dst)

    # ── zero.3: the novice's base case of one, and the lesson ───────────────────
    def the_novice(self):
        r, a = self.rows, self.arrows
        with self.say("c4.zero.3") as c:
            # "A beginner might stop one step earlier, when the amount equals a coin,
            #  and return just that coin."
            step = token_box(VGroup(*r[0].text), r[0], color=YELLOW)
            self.play(FadeIn(step), *set_alpha([r[1], r[2], a[1], a[2], self.tag_n], DIMMED),
                      run_time=min(1.0, 0.9 * c.until("when the amount")))
            c.wait_until("equals a coin")
            sweep_clear(self,
                        time_span(FadeIn(self.card_label, shift=0.3 * DOWN), 0.5, 1.3),
                        time_span(Create(self.frame), 0.6, 1.6),
                        time_span(FadeIn(self.card), 0.7, 1.7),
                        run_time=1.8)

            # "Then the base case has work of its own to do, building a list with that coin."
            c.wait_until("work")
            self.play(*recolor(self.work, RED),
                      FlashUnder(self.work, color=RED, time_width=1.5),
                      FadeIn(self.tag_w, shift=0.3 * UP),
                      run_time=min(1.5, 0.9 * c.until("fails")))

            # "And it gets zero wrong.  Ask it for zero, and it runs out of coins."
            c.wait_until("fails")
            msg = G(self.fail, 'Failure "no more coins!"')
            exc = G(self.fail, "Exception:")
            dot = G(self.fail, ".")
            self.play(time_span(FadeIn(self.call, shift=0.2 * DOWN), 0, 0.9),
                      time_span(TransformFromCopy(G(self.card, 'Failure "no more coins!"',
                                                    line=2), msg, path_arc=0.4), 0.7, 2.2),
                      time_span(FadeIn(exc, shift=0.2 * RIGHT), 0.9, 2.0),
                      time_span(FadeIn(dot, shift=0.2 * RIGHT), 0.9, 2.0),
                      time_span(FadeIn(self.fail_arrow, shift=0.2 * DOWN), 0.7, 1.6),
                      run_time=2.2)
            self.remove(msg, exc, dot)
            self.add(self.fail)
            c.wait_until("runs out of coins")
            self.play(FlashUnder(VGroup(*self.card.line(2)), color=RED, time_width=1.5),
                      run_time=min(1.2, max(0.5, 0.9 * c.until("rule"))))

            # "The course notes draw a general lesson."  (the failure stays up through it)
            # "Most procedures that repeat a step are simplest when, in their base case,
            #  they do nothing."
            c.wait_until("most procedures")
            sweep_clear(self, time_span(FadeIn(self.notes, shift=0.2 * DOWN), 0.6, 1.3),
                        time_span(FadeIn(self.q1, shift=0.2 * DOWN), 0.9, 2.0),
                        time_span(FadeIn(self.q2, shift=0.2 * DOWN), 1.3, 2.4),
                        run_time=2.4)

            # "A base case of one, instead of zero, is often the sign of a novice."
            c.wait_until("sign")
            self.play(GrowFromCenter(self.rule),
                      FadeIn(self.s1, shift=0.2 * UP),
                      time_span(FadeIn(self.s2, shift=0.2 * UP), 0.4, 1.4),
                      run_time=1.4)
