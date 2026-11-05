"""Chapter 3, scene 4: the tempting mistake. nlength written as two separate `let rec`
definitions: the second replaces the first, so every call ends in a Match_failure.
Clips c3.bad.1 – c3.bad.4.

OCaml 5.4.1 (quoted by the brief): each block replies `val nlength : 'a list -> int = <fun>`;
the warning's example is `_::_` for the first block and `[]` for the second; `nlength [5; 6; 7]`
and `nlength []` both raise `Exception: Match_failure ("//toplevel//", 1, 16).`

Layout: the two declaration boxes (with OCaml's replies under them) sit centred in clip 1, move
up when the warning panel needs the bottom (bad.2 {warn}); the run on [5; 6; 7] uses the bottom
in bad.3; bad.4 ends on the two boxes (top) vs the correct one-box definition (bottom).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

CORRECT = """let rec nlength = function
  | [] -> 0
  | x :: xs -> 1 + nlength xs"""
B1 = "let rec nlength [] = 0"
B2 = "let rec nlength (x::xs) = 1 + nlength xs"
VAL = "val nlength : 'a list -> int = <fun>"
W_HEAD = ("Warning 8 [partial-match]:\n"          # OCaml's words, wrapped to <= 40 chars
          "this pattern-matching is not exhaustive.\n"
          "Here is an example of a case that\n"
          "is not matched: ")
EX1, EX2 = "_::_", "[]"
EXC = 'Exception: Match_failure ("//toplevel//", 1, 16).'

CODE_S, VAL_S, W_S, CALL_S, EXC_S = 36, 32, 30, 34, 28
CX = -6.0                 # left edge of every code line
PAD_X, BOX_H = 0.3, 0.8   # declaration boxes
Y1, Y2 = 1.5, -0.5        # block rows in clips 1-2 ...
UP_SH = 1.4               # ... moved up by this for the warning panel and the run
VAL_DY = 0.9              # OCaml's reply sits this far under its code
Q_Y = -2.85
PANEL_Y = -1.75
COMPACT = 0.65            # bad.3: block 2 moves up into the forgotten reply's row
PARK_S, PARK_R, PARK_Y = 0.68, 6.55, -0.7   # bad.3: the warning panel, shrunk, right of the call
CALL_Y, CHAIN_Y, CHAIN_S, EXC_Y = -0.7, -2.2, 0.9, -3.2
F1, F2 = 1.85, 0.95       # the two boxes in the final comparison
LAB_A_Y, LAB_B_Y, BOX3_TOP = 2.78, -0.02, -0.45


# ── helpers (local to this scene) ───────────────────────────────────────────────
def left_at(mob, x, y):
    mob.move_to([0, y, 0])
    return mob.shift(RIGHT * (x - mob.get_left()[0]))


def decl_box(code, height=BOX_H):
    """One declaration = one box (BLUE: structure)."""
    return RoundedRectangle(corner_radius=0.12, width=code.width + 2 * PAD_X, height=height) \
        .set_stroke(BLUE, 2.5).move_to(code)


def make_chain():
    """bad.3's list, left-aligned under the call (the warning panel sits to the right)."""
    return left_at(ConsChain([5, 6, 7]).scale(CHAIN_S), CX, CHAIN_Y)


def recolor_code(code, base, spans):
    """A Code block read as plain terminal output: one base colour, a few spans picked out."""
    code.text.set_color(base)
    for sub, color in spans:
        VGroup(*code.find(sub)).set_color(color)
    return code


def warning(example):
    return recolor_code(Code(W_HEAD + example, size=W_S), FG,
                        [("Warning 8 [partial-match]:", YELLOW), (example, TEAL)])


def name_tag(text="nlength"):
    """A luggage-style tag pointing left: the name, about to be tied to a function."""
    lab = Mono(text, size=32, color=YELLOW)
    w, h, tip = lab.width + 0.4, lab.height + 0.14, 0.26
    shape = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w / 2, -h / 2, 0], [-w / 2, -h / 2, 0],
                    [-w / 2 - tip, 0, 0]).set_stroke(YELLOW, 3).set_fill(YELLOW, opacity=0.12)
    hole = Circle(radius=0.05).set_stroke(YELLOW, 2).move_to([-w / 2 - 0.02, 0, 0])
    return VGroup(shape, hole, lab.move_to(ORIGIN + RIGHT * 0.04))


def build_from(scene, pairs, fade_in, fade_out=(), extra=(), run_time=2.0):
    """New code born from old (P5): each (source glyphs, target glyphs) pair flies out of a copy
    of the source; `fade_in` glyph runs appear; then the caller adds the real Code objects."""
    pieces = [VGroup(*t) for _, t in pairs]
    news = VGroup(*[g for run in fade_in for g in run])
    scene.play(*[TransformFromCopy(VGroup(*s), p) for (s, _), p in zip(pairs, pieces)],
               FadeIn(news, shift=0.15 * DOWN), *[FadeOut(m) for m in fade_out], *extra,
               run_time=run_time)
    scene.remove(*pieces, news)


class TemptingMistake(NarratedScene):
    def construct(self):
        self.two_blocks()
        self.replaced()
        self.run_it()
        self.lesson()
        self.wait(2.5)                                              # hold the comparison
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # bad.1: the correct definition splits into two let recs; OCaml accepts both
    def two_blocks(self):
        correct = Code(CORRECT, size=40).move_to(UP * 0.3)
        code1 = left_at(Code(B1, size=CODE_S), CX, Y1)
        code2 = left_at(Code(B2, size=CODE_S), CX, Y2)
        box1, box2 = decl_box(code1), decl_box(code2)
        val1 = left_at(Code(VAL, size=VAL_S), CX, Y1 - VAL_DY)
        val2 = left_at(Code(VAL, size=VAL_S), CX, Y2 - VAL_DY)
        q = T("What goes wrong?", size=48, color=YELLOW).move_to(UP * Q_Y)

        with self.say("c3.bad.1") as c:
            # "Before we go on, here's a tempting mistake."  The right definition, as in s2/s3.
            self.play(FadeIn(correct, shift=0.2 * DOWN), run_time=1.2)
            # "Why not write the two cases as two separate definitions?"  Each clause flies out
            # into a let rec of its own.
            c.wait_until("split")
            pairs = [(correct.find("let rec nlength"), code1.find("let rec nlength")),
                     (correct.find("let rec nlength"), code2.find("let rec nlength")),
                     (correct.find("[]"), code1.find("[]")),
                     (correct.find("0", line=1), code1.find("0")),
                     (correct.find("x :: xs"), code2.find("(x::xs)")),
                     (correct.find("1 + nlength xs"), code2.find("1 + nlength xs"))]
            build_from(self, pairs, fade_in=[code1.find("="), code2.find("=")],
                       extra=[time_span(FadeOut(correct), 0, 0.8),
                              time_span(Create(box1), 1.3, 2.1), time_span(Create(box2), 1.4, 2.2)],
                       run_time=2.2)
            self.add(code1, code2)

            # "First, en-length of nil is zero."  Spotlight the first block.
            c.wait_until("first")
            self.play(*set_alpha([box2, code2], DIMMED), FlashAround(box1, color=YELLOW, time_width=1.5),
                      run_time=1.2)
            # "Then, en-length of ex consed onto exes is one plus en-length of exes."
            c.wait_until("second")
            self.play(*set_alpha([box2, code2], 1), *set_alpha([box1, code1], DIMMED),
                      FlashAround(box2, color=YELLOW, time_width=1.5), run_time=1.2)
            # "It looks reasonable, and OCaml accepts both."
            c.wait_until("ask")
            self.play(*set_alpha([box1, code1], 1), run_time=1.0)
            c.wait_until("accepts both")
            self.play(LaggedStart(FadeIn(val1, shift=0.2 * DOWN), FadeIn(val2, shift=0.2 * DOWN),
                                  lag_ratio=0.4), run_time=1.4)
            # "So what goes wrong?"  Asked on screen, held.
            c.wait_until("what goes wrong")
            self.play(FadeIn(q, shift=0.3 * DOWN), run_time=1.0)

        self.code1, self.code2, self.box1, self.box2 = code1, code2, box1, box2
        self.val1, self.val2, self.q = val1, val2, q

    # bad.2: two declarations; the name moves to the second; OCaml warned both times
    def replaced(self):
        code1, code2, box1, box2 = self.code1, self.code2, self.box1, self.box2
        val1, val2 = self.val1, self.val2
        fun1, fun2 = VGroup(*val1.find("<fun>")), VGroup(*val2.find("<fun>"))
        tag = name_tag().next_to(fun1, RIGHT, buff=0.18)
        gone = T("replaced", size=34, color=RED).next_to(box1, RIGHT, buff=0.45)
        hb = token_box(code2.find("(x::xs)"), code2, color=TEAL, pad=0.16)

        w1 = warning(EX1).move_to(UP * PANEL_Y)
        w2 = warning(EX2).align_to(w1, UL)
        wbox = SurroundingRectangle(w1, buff=0.2, color=YELLOW, stroke_width=3, corner_radius=0.08)
        ex1, ex2 = w1.find(EX1), w2.find(EX2)

        with self.say("c3.bad.2") as c:
            # "These are two declarations, not one."
            self.play(LaggedStart(FlashAround(box1, color=BLUE, time_width=1.5),
                                  FlashAround(box2, color=BLUE, time_width=1.5), lag_ratio=0.35),
                      run_time=1.6)
            # "The second let doesn't add a case to the first."  The question turns into the answer:
            # the name nlength, tied for now to the first function.
            c.wait_until("replace")
            self.play(FadeTransform(self.q, tag), FlashAround(VGroup(*code2.find("let")), color=BLUE,
                                                              time_width=1.5), run_time=1.5)
            # "It replaces it."  The tag moves to the second function; the first fades.
            c.wait_until("replaces it")
            self.play(tag.animate.next_to(fun2, RIGHT, buff=0.18),
                      *set_alpha([box1, code1, val1], DIMMED), run_time=1.5)
            # "The first en-length is simply forgotten,"
            c.wait_until("gone")
            self.play(FadeIn(gone, shift=0.25 * DOWN), run_time=1.0)
            # "and the name now means a function that only handles lists that aren't empty."
            c.wait_until("the name now")
            self.play(FlashAround(tag, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("only handles")
            self.play(FadeIn(hb), run_time=0.8)

            # "In fact, OCaml warns you both times that some lists aren't covered."  The boxes
            # make room; one panel, its example first for block 1, then for block 2.
            c.wait_until("warn")
            top = [box1, code1, val1, gone, box2, code2, val2, tag]
            self.play(*[m.animate.shift(UP * UP_SH) for m in top], FadeOut(hb, shift=UP * UP_SH),
                      time_span(Create(wbox), 0.5, 1.4), time_span(FadeIn(w1, shift=0.2 * DOWN), 0.6, 1.6),
                      run_time=1.6)
            c.wait_until("both times")
            self.play(FlashAround(box1, color=YELLOW, time_width=1.5),
                      FlashUnder(VGroup(*ex1), color=TEAL, time_width=1.5), run_time=1.1)
            c.wait_until("some lists")
            self.play(*[FadeOut(g, shift=0.2 * UP) for g in ex1], FadeIn(VGroup(*ex2), shift=0.2 * UP),
                      FlashAround(box2, color=YELLOW, time_width=1.5), run_time=1.1)
            self.remove(*w1.get_family(), *VGroup(*ex2).get_family())
            self.add(w2)

        self.tag, self.gone, self.wtext, self.wbox = tag, gone, w2, wbox

    # bad.3: nlength [5; 6; 7] peels to [], no clause matches; nlength [] fails too
    def run_it(self):
        code1, code2 = self.code1, self.code2
        call = left_at(Code("nlength [5; 6; 7]", size=CALL_S), CX, CALL_Y)
        chain = make_chain()
        exc = Code(EXC, size=EXC_S)
        exc.text.set_color(RED)
        exc.move_to(UP * EXC_Y)
        pat = VGroup(*code2.find("(x::xs)"))
        nbox = SurroundingRectangle(chain.nil, color=YELLOW, buff=0.14, corner_radius=0.08)
        wbox, wtext = self.wbox, self.wtext
        w_nil = VGroup(*wtext.find("[]"))
        about = wbox.get_center()
        park = np.array([PARK_R - wbox.width * PARK_S / 2, PARK_Y, 0]) - about

        with self.say("c3.bad.3") as c:
            # "So let's call it on five, six, seven."  The forgotten reply goes, block 2 moves up,
            # and the warning shrinks to the right: it stays as the prediction of what's coming.
            self.play(FadeOut(self.val1), *[m.animate.shift(UP * COMPACT) for m in (self.box2, code2, self.val2, self.tag)],
                      *[m.animate.scale(PARK_S, about_point=about).shift(park) for m in (wbox, wtext)],
                      run_time=1.1)
            hb = token_box(pat, code2, color=GREEN, pad=0.16)
            c.wait_until("five")
            self.play(FadeIn(call, shift=0.2 * DOWN),
                      time_span(FadeIn(chain, shift=0.2 * DOWN, lag_ratio=0.1), 0.3, 1.2), run_time=1.2)

            # "It strips off five, then six, then seven,"  The (x::xs) clause matches each time.
            for k, (cue, rt) in enumerate((("down", 1.0), ("then six", 0.8), ("then seven", 0.7))):
                c.wait_until(cue)
                match = FadeIn(hb) if k == 0 else FlashAround(pat, color=GREEN, time_width=1.5)
                self.play(FadeOut(chain.cells[k], shift=0.5 * UP), FadeOut(chain.arrows[k], shift=0.5 * UP),
                          match, run_time=rt)
            chain.remove(*chain.cells, *chain.arrows)

            # "and reaches the empty list."
            c.wait_until("stuck")
            self.play(Create(nbox), FlashAround(chain.nil, color=YELLOW, time_width=1.5), run_time=1.0)
            # "But there's no clause for that anymore."  The pattern refuses; the [] clause is gone.
            c.wait_until("no clause")
            # The warning predicted exactly this case: its [] flashes as the list's [] turns red.
            self.play(hb.animate.become(token_box(pat, code2, color=RED, pad=0.16)),
                      nbox.animate.set_color(RED), FlashAround(w_nil, color=RED, time_width=1.5), run_time=1.1)
            c.wait_until("anymore")
            self.play(FlashAround(VGroup(*code1.find("[]")), color=TEAL, time_width=1.5), run_time=1.1)

            # "So the program stops, with an error called a match failure."
            c.wait_until("fail")
            self.play(FadeIn(exc, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("match failure")
            self.play(FlashUnder(VGroup(*exc.find("Match_failure")), color=RED, time_width=1.5), run_time=1.2)

            # "Even en-length of nil fails now."  Same call, empty list: same exception.
            c.wait_until("nil")
            call2 = Code("nlength []", size=CALL_S).move_to(call).align_to(call, LEFT)
            self.play(TransformMatchingStrings(call.text, call2.text), run_time=1.2)
            self.remove(call, *call2.get_family())
            self.add(call2)
            c.wait_until("fails now")
            self.play(FlashAround(exc, color=RED, time_width=1.5), FlashAround(w_nil, color=RED, time_width=1.5),
                      run_time=1.2)

            # "This version can never deliver a result, because every call ends up at the empty list."
            c.wait_until("never")
            ghost = make_chain()                                   # the path every call takes
            ghost.remove(ghost.nil)
            ghost.set_opacity(0.3)
            self.play(FlashUnder(VGroup(*self.val2.find("int")), color=GOLD, time_width=1.5),
                      FadeIn(ghost), run_time=1.2)
            c.wait_until("every call")
            path = [ghost.cells[1], ghost.cells[2], chain.nil]
            rt = c.until(None, floor=1.6)
            self.play(LaggedStart(*[flash_along(a, b, color=YELLOW) for a, b in zip(ghost.cells, path)],
                                  lag_ratio=0.5),
                      time_span(FlashAround(nbox, color=RED, time_width=1.5), 0.55 * rt, rt), run_time=rt)

    # bad.4: a second let never extends; one function with | bars instead
    def lesson(self):
        code1, code2, box1, box2 = self.code1, self.code2, self.box1, self.box2
        d1, d2 = UP * (F1 - box1.get_y()), UP * (F2 - box2.get_y())
        lab_a = T("two functions, one clause each", size=40, color=RED)
        lab_a.move_to([0, LAB_A_Y, 0]).align_to(box1, LEFT)
        correct = Code(CORRECT, size=40)
        box3 = RoundedRectangle(corner_radius=0.12, width=correct.width + 2 * PAD_X,
                                height=correct.height + 0.44).set_stroke(BLUE, 2.5)
        left_at(correct, CX, BOX3_TOP - box3.height / 2)
        box3.move_to(correct)
        lab_b = T("one function, two clauses", size=40, color=GREEN)
        lab_b.move_to([0, LAB_B_Y, 0]).align_to(box3, LEFT)
        bars = [correct.find("|", nth=k) for k in range(2)]

        with self.say("c3.bad.4") as c:
            # "So a second let never extends an earlier one."  The run clears; the two boxes regroup.
            sweep_clear(self, restyle(box1, 1, shift=d1), restyle(code1, 1, shift=d1),
                        box2.animate.shift(d2), code2.animate.shift(d2),
                        keep=[box1, code1, box2, code2], run_time=1.5)
            c.wait_until("never extends")
            self.play(FadeIn(lab_a, shift=0.25 * DOWN), run_time=1.0)

            # "To give a function several cases, put them all in a single definition, ..."  The two
            # clauses fly back into one definition (the opening split, reversed).
            c.wait_until("bar")
            pairs = [(code2.find("let rec nlength"), correct.find("let rec nlength")),
                     (code1.find("[]"), correct.find("[]")),
                     (code1.find("0"), correct.find("0", line=1)),
                     (code2.find("(x::xs)"), correct.find("x :: xs")),
                     (code2.find("1 + nlength xs"), correct.find("1 + nlength xs"))]
            fade_in = [correct.find("= function"), *bars, correct.find("->", nth=0), correct.find("->", nth=1)]
            build_from(self, pairs, fade_in, run_time=2.1,
                       extra=[time_span(Create(box3), 0.9, 1.7),
                              time_span(FadeIn(lab_b, shift=0.25 * DOWN), 1.3, 2.1)])
            self.add(correct)
            # "... in a single definition, ..."  One box.
            c.wait_until("single definition")
            self.play(FlashAround(box3, color=BLUE, time_width=1.5), run_time=1.1)
            # "... separated by vertical bars."  The bars glow and stay lit.
            c.wait_until("vertical bars")
            self.play(*[a for b in bars for a in recolor(b, YELLOW)],
                      *flash([VGroup(*b) for b in bars], color=YELLOW, time_width=1.5), run_time=1.2)
