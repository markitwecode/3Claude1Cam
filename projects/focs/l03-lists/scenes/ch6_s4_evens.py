"""Chapter 6, scene 4: exercise 3.3 solved, the even positions. Clips c6.evens.1 – c6.evens.6.

Plan: s1's row of five exercise cards fades back in; card 3.3 lights and grows into the kit's
hero card (task, [a; b; c; d] ⇒ [b; d], the dashed slot), then the kit's pause tag. .2:
"even-numbered" lights on the card; on {positions} the task becomes the title and five boxes
10..50 arrive with DIM positions 1-5; values glow GREEN, then 2 and 4 YELLOW, the rest RED at
half; 20 and 40 slide into [20; 40] (kept until {pair}). .3: the code is built clause by
clause (one highlight box sliding from pattern to pattern); on {pair} a chain 10..50 with
x / y / xs born from the pattern and a YELLOW bracket over two cells. .4: the code shrinks to
the top, the chain moves up, and the trace grows row by row (each born from the one above)
while the bracket hops two cells per step; at [50] it covers one cell and the [x] clause
lights up; the reply under the trace. .5: the [x] clause is struck out; OCaml's warning
(wrapped to fit), the even test GREEN, the odd test's Match_failure RED; "read the warnings":
the warning's x::[] flies back in as the clause. .6: time O(n); the pending `20 ::`, `40 ::`
as GOLD plates in s2's pending column (born from the code's `y ::`), space O(n); a ghost
accumulator builds [40; 20], rev gives [20; 40], which is O(n) anyway: the "?" becomes a RED
✗ "no gain"; on {habit} the board dims to 0.12 under the notes' line on a quote card in s5's
Milner-card style, and fades away after the clip so the quote stands alone (final shot).

The toplevel's `val evens : 'a list -> 'a list = <fun>` is not shown (no room under the
trace; the type is on the card's slot in .1).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import (  # noqa: E402  the shared exercise-card kit (read-only)
    CARD_FILL, BigCard, HeroCard, at_row, fit, hold_for, pause_tag, split_line,
)

EVENS = """let rec evens = function
  | [] -> []
  | [x] -> []
  | x :: y :: xs -> y :: evens xs"""
EVENS3 = """let rec evens = function
  | [] -> []
  | x :: y :: xs -> y :: evens xs"""
VALUES = [10, 20, 30, 40, 50]
ROWS = ["evens [10; 20; 30; 40; 50]", "20 :: evens [30; 40; 50]",
        "20 :: 40 :: evens [50]", "20 :: 40 :: []"]
ROW4_FULL = "20 :: 40 :: []  =  [20; 40]"
REPLY = "- : int list = [20; 40]"
WARN = ["Warning 8 [partial-match]: this pattern-matching", "is not exhaustive.",
        "Here is an example of a case that is not matched:", "x::[]"]
QUOTE = "Never add an accumulator merely out of habit."

CODE_BIG, CODE_SMALL = 40, 30      # the code as the hero (.3), then as the reference (.4-.6)
CHAIN_BIG, CHAIN_SMALL = 0.8, 0.75
ROW_SIZE, ROW_PITCH = 32, 0.66
ROW_BASE0 = -0.6                   # baseline of the first trace row
# s2's pending column (ch6_s2_sum.py), same look: plates on a GOLD floor, label under it
CX, PW, PH, FLOOR = 4.9, 2.0, 0.7, -1.0
PLATE_FILL = "#1E222A"

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── helpers (local to this scene) ─────────────────────────────────────────────
def piece(code, sub, line=None, nth=0):
    """Copies of the glyphs of `sub` in `code`, where they sit: a part to reveal on its own
    (the real Code replaces the parts once they're all on screen, see swap)."""
    return VGroup(*[g.copy() for g in code.find(sub, line=line, nth=nth)])


def grow_from(src, dst, pairs):
    """Animations building `dst` out of `src` (P5): each (src_sub, dst_sub) flies across
    (a sub is a string or (string, nth)); the rest of dst fades in. Returns (anims, temps);
    after the play, swap(scene, temps, dst)."""
    anims, temps, used = [], [], set()
    for a, b in pairs:
        sa, na = (a, 0) if isinstance(a, str) else a
        sb, nb = (b, 0) if isinstance(b, str) else b
        glyphs = dst.find(sb, nth=nb)
        used |= {id(g) for g in glyphs}
        tgt = VGroup(*[g.copy() for g in glyphs])
        anims.append(TransformFromCopy(VGroup(*src.find(sa, nth=na)), tgt))
        temps.append(tgt)
    rest = VGroup(*[g.copy() for g in dst.text if id(g) not in used])
    if len(rest):
        anims.append(FadeIn(rest))
        temps.append(rest)
    return anims, temps


def swap(scene, temps, whole, drop=()):
    """Replace parts shown one by one with the one object they make up (same look)."""
    scene.remove(*temps, *drop)
    scene.add(whole)


def sweep(scene, *incoming, keep=(), late=(), run_time=1.6):
    """sweep_clear, except that `late` (results the voice just landed) go last."""
    keep_ids = {id(m) for k in keep for m in k.get_family()}
    late_ids = {id(m) for m in late}
    gone = [m for m in list(scene.mobjects) if id(m) not in keep_ids]
    early = [m for m in gone if id(m) not in late_ids]
    last = [m for m in gone if id(m) in late_ids]
    anims = [time_span(LaggedStart(*[FadeOut(m) for m in early], lag_ratio=0.1), 0.0, 0.6 * run_time)]
    if last:
        anims.append(time_span(AnimationGroup(*[FadeOut(m) for m in last]), 0.5 * run_time, run_time))
    scene.play(*anims, *incoming, run_time=run_time)


def baseline(code):
    chars_ = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars_, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    """Left edge at x=left, text baseline at y=base."""
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def gslice(text, full, sub):
    """The glyphs of `sub` in a T/Mono made from `full` (Text has no glyphs for spaces)."""
    i = full.index(sub)
    a = len(full[:i].replace(" ", ""))
    return text[a:a + len(sub.replace(" ", ""))]


def cbox(code, sub, line):
    """The sliding highlight box behind one pattern (same height on every line)."""
    bar = code.find("|", line=line)
    return token_box(code.find(sub, line=line), bar, pad=0.24, height=bar.height + 0.2)


def bracket(chain, i, j, color=YELLOW):
    """The bracket round cells i..j of a chain (the part a pattern grabs)."""
    a, b = chain.cells[i], chain.cells[j]
    pad = 0.12
    left, right = a.box.get_left()[0] - pad, b.ptr.get_right()[0] + pad
    top, bot = a.box.get_top()[1] + pad, a.box.get_bottom()[1] - pad
    r = RoundedRectangle(corner_radius=0.12, width=right - left, height=top - bot)
    return r.set_stroke(color, 4).set_fill(color, 0).move_to([(left + right) / 2, (top + bot) / 2, 0])


def plate(text, k):
    """One pending cons as a plate on the stack (k = 0 is the bottom one), as in s2."""
    r = Rectangle(width=PW, height=PH).set_stroke(GOLD, 3).set_fill(PLATE_FILL, 1)
    r.move_to([CX, FLOOR + PH * (k + 0.5), 0])
    return VGroup(r, Mono(text, size=36, color=GOLD).move_to(r)).set_z_index(1)


def implies():
    return MathTex(r"\Rightarrow", font_size=44, color=DIM)


def cost_row(word):
    return VGroup(T(word, size=34), MathTex("O(n)", font_size=46, color=GOLD)).arrange(RIGHT, buff=0.25)


class EvenPositions(NarratedScene):
    def construct(self):
        self.statement()     # c6.evens.1
        self.what_asked()    # c6.evens.2
        self.three_shapes()  # c6.evens.3
        self.trace()         # c6.evens.4
        self.mistake()       # c6.evens.5
        self.cost()          # c6.evens.6
        hold_for(self, self.quote_born, len(QUOTE))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # .1: s1's five cards; 3.3 grows into the hero card; task, example, pause
    def statement(self):
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * 0.7)
        card = HeroCard(2, height=2.95, slot_type="'a list -> 'a list")
        task = at_row(T("Return the even-numbered elements.", size=32), 1)
        e_in, e_out = split_line("[a; b; c; d]  ⇒  [b; d]", ["[a; b; c; d]", "⇒  [b; d]"], y=0.62)
        card.lower(task, e_in, e_out)
        slot = card.slot
        tag = pause_tag()

        # s1 ended on this row: it comes back
        self.play(LaggedStart(*[FadeIn(b) for b in bigs], lag_ratio=0.12), run_time=1.0)
        self.wait(1.2)
        with self.say("c6.evens.1") as c:
            # "Exercise three point three."  Its card lights, then grows into the hero card
            b3 = bigs[2]
            self.play(b3.frame.animate.set_stroke(YELLOW, 3), b3.num.animate.set_color(YELLOW),
                      FlashAround(b3.frame, color=YELLOW, buff=0.06), run_time=0.7)
            others = [b for k, b in enumerate(bigs) if k != 2]
            self.play(TransformFromCopy(b3.frame, card.frame),
                      FadeTransform(b3.num.copy(), card.header),
                      FadeOut(b3),
                      LaggedStart(*[FadeOut(b, shift=0.2 * DOWN) for b in others], lag_ratio=0.1),
                      run_time=fit(c, "code a function", lo=1.0, hi=1.4, frac=0.95))
            # "Code a function that returns the even-numbered elements of a list."
            c.wait_until("code a function")
            self.play(FadeIn(task, shift=0.25 * DOWN), FadeIn(slot.box), FadeIn(slot.q, scale=0.7),
                      run_time=1.1)
            c.wait_until("of a list")
            self.play(FadeIn(slot.sig, shift=0.2 * DOWN), run_time=0.8)
            # "Given four letters, it should keep the second and the fourth."
            c.wait_until("given four letters")
            self.play(FadeIn(e_in, shift=0.25 * DOWN), run_time=fit(c, "keep the second", hi=1.0))
            c.wait_until("keep the second")
            b_in, b_out = e_in.find("b"), e_out.find("b")
            self.play(FadeIn(e_out, shift=0.25 * LEFT), *recolor(b_in, GOLD), *recolor(b_out, GOLD),
                      FlashAround(b_in, color=GOLD, buff=0.06), run_time=fit(c, "the fourth", hi=0.9))
            c.wait_until("the fourth")
            d_in, d_out = e_in.find("d"), e_out.find("d")
            self.play(*recolor(d_in, GOLD), *recolor(d_out, GOLD),
                      FlashAround(d_in, color=GOLD, buff=0.06), run_time=0.8)
            # "Pause, and try it."
            c.wait_until("stop")
            self.play(FadeIn(tag, shift=0.2 * DOWN), run_time=0.9)
        self.card, self.task, self.examples, self.tag = card, task, (e_in, e_out), tag

    # .2: even positions, not even values
    def what_asked(self):
        card, slot = self.card, self.card.slot
        full = "Return the even-numbered elements."
        title = T(full, size=42).move_to([0, 2.95, 0])
        gslice(title, full, "even-numbered").set_color(YELLOW)

        cells = [VGroup(Square(1.25).set_stroke(BLUE, 3).set_fill(BG, 1), value_label(v, size=46))
                 for v in VALUES]
        for sq, v in cells:
            v.move_to(sq)
        VGroup(*cells).arrange(RIGHT, buff=0.5).move_to([0, 0.55, 0])
        nums = [T(str(k + 1), size=32, color=DIM).next_to(cl, DOWN, buff=0.3) for k, cl in enumerate(cells)]
        cap = T("position", size=30, color=DIM).next_to(nums[0], LEFT, buff=0.6)
        result = Code("[20; 40]", size=52).move_to([0, -2.2, 0])
        for sub in ("20", "40"):
            result.find(sub).set_color(YELLOW)

        with self.say("c6.evens.2") as c:
            # "Be clear what's asked."  "even-numbered" lights up on the card
            ev = gslice(self.task, full, "even-numbered")
            self.play(*recolor(ev, YELLOW), FlashUnder(ev, color=YELLOW, time_width=1.5), run_time=1.2)
            # "Even-numbered means even positions, the second, the fourth, and so on, not even values."
            # The task becomes the title, the rest of the card goes, the positions arrive
            c.wait_until("positions")
            self.play(ReplacementTransform(self.task, title),
                      *[FadeOut(m) for m in (card.frame, card.header, slot.box, slot.q, slot.sig,
                                             *self.examples)],
                      time_span(FadeOut(self.tag), 0.4, 1.2),
                      time_span(LaggedStart(*[FadeIn(cl, shift=0.3 * UP) for cl in cells], lag_ratio=0.15), 0.6, 1.9),
                      time_span(LaggedStart(*[FadeIn(n, shift=0.2 * DOWN) for n in nums], lag_ratio=0.15), 0.8, 2.0),
                      time_span(FadeIn(cap), 1.2, 2.0), run_time=2.0)
            c.wait_until("the second")
            self.play(*[nums[k].animate.set_color(YELLOW) for k in (1, 3)],
                      *[FlashAround(nums[k], color=YELLOW, buff=0.12) for k in (1, 3)], run_time=1.0)
            # "In ten, twenty, thirty, forty, fifty, every value is even, ..."  (they glow as read)
            c.wait_until("values")
            self.play(LaggedStart(*[cl[1].animate.set_color(GREEN) for cl in cells], lag_ratio=0.2),
                      LaggedStart(*[FlashAround(cl[0], color=GREEN, buff=0.06) for cl in cells], lag_ratio=0.2),
                      run_time=1.6)
            # "... but we keep only twenty and forty."
            c.wait_until("we keep only")
            anims = []
            for k, (sq, v) in enumerate(cells):
                if k in (1, 3):
                    anims += [sq.animate.set_stroke(YELLOW, 4), v.animate.set_color(YELLOW)]
                else:
                    anims += [sq.animate.set_stroke(RED, 3, opacity=0.5), v.animate.set_color(RED).set_opacity(0.5)]
            grow, temps = [], []
            for k, sub in ((1, "20"), (3, "40")):
                tgt = piece(result, sub)
                grow.append(TransformFromCopy(cells[k][1], tgt))
                temps.append(tgt)
            rest = VGroup(*[g.copy() for g in result.text
                            if id(g) not in {id(x) for s in ("20", "40") for x in result.find(s)}])
            # 2 and 4 kept, the rest dropped, then 20 and 40 slide together (settled early)
            self.play(*[time_span(a, 0.0, 0.7) for a in anims],
                      *[time_span(a, 0.5, 1.5) for a in grow], time_span(FadeIn(rest), 0.8, 1.5),
                      run_time=1.5)
            swap(self, [*temps, rest], result)
        self.result = result

    # .3: three shapes, one clause each
    def three_shapes(self):
        code = Code(EVENS, size=CODE_BIG)
        code.move_to(ORIGIN).shift(UP * (3.45 - code.get_top()[1]))
        head = piece(code, "let rec evens = function", line=0)
        pats = [piece(code, "| []", 1), piece(code, "| [x]", 2), piece(code, "| x :: y :: xs", 3)]
        rhs = [piece(code, "-> []", 1), piece(code, "-> []", 2)]

        chain = ConsChain(VALUES).scale(CHAIN_BIG).move_to([0, -1.9, 0])
        cl = chain.cells
        top = cl[0].box.get_top()[1]
        xs_brace = span_brace(cl[2].box.get_corner(UL), np.array([chain.nil.get_right()[0], top, 0]),
                              direction=UP, color=TEAL, buff=0.14)
        lab_x = Mono("x", size=40).move_to([cl[0].box.get_x(), top + 0.68, 0])
        lab_y = Mono("y", size=40, color=YELLOW).move_to([cl[1].box.get_x(), 0, 0]).align_to(lab_x, UP)
        lab_xs = Mono("xs", size=40, color=TEAL).move_to([xs_brace.get_x(), 0, 0]).align_to(lab_x, UP)
        br = bracket(chain, 0, 1)

        with self.say("c6.evens.3") as c:
            # "This time, a list has three shapes."
            c.wait_until("a list")
            sweep_clear(self, time_span(FadeIn(head, shift=0.2 * DOWN), 0.5, 1.3),
                        time_span(LaggedStart(*[FadeIn(p, shift=0.3 * RIGHT) for p in pats],
                                              lag_ratio=0.35), 0.9, 2.0),
                        keep=[self.result], run_time=2.0)
            # "Empty gives empty."
            c.wait_until("empty")
            box = cbox(code, "| []", 1)
            self.play(FadeIn(box), FadeIn(rhs[0], shift=0.3 * LEFT), run_time=0.9)
            # "A single element gives empty too, with no second element to keep."
            c.wait_until("single")
            self.play(Transform(box, cbox(code, "| [x]", 2)), FadeIn(rhs[1], shift=0.3 * LEFT), run_time=1.0)
            c.wait_until("no second element")
            self.play(FlashAround(pats[1][1:], color=YELLOW, time_width=1.5), run_time=1.2)
            # "And for two or more, the pattern ex, cons why, cons exes, grabs two at once."
            c.wait_until("pair")
            self.play(Transform(box, cbox(code, "| x :: y :: xs", 3)),
                      FadeOut(self.result, shift=0.3 * DOWN),
                      FadeIn(chain, shift=0.3 * UP, lag_ratio=0.05), run_time=fit(c, "the pattern", hi=1.4))
            c.wait_until("the pattern")
            self.play(LaggedStart(TransformFromCopy(VGroup(*code.find("x", line=3)), lab_x),
                                  TransformFromCopy(VGroup(*code.find("y", line=3)), lab_y),
                                  AnimationGroup(TransformFromCopy(VGroup(*code.find("xs", line=3)), lab_xs),
                                                 GrowFromCenter(xs_brace)),
                                  lag_ratio=0.5),
                      run_time=fit(c, "grabs two", lo=1.0, hi=1.8, frac=0.85))
            c.wait_until("grabs two")
            self.play(Create(br), run_time=1.0)
            # "We keep why, drop ex, and carry on with exes."
            c.wait_until("keep")
            # the RHS's y and xs come out of the pattern's (nth 0 on line 3 is the pattern's)
            temps = [piece(code, "y", 3, nth=1), piece(code, "xs", 3, nth=1)]
            anims = [TransformFromCopy(VGroup(*code.find(s, line=3)), t) for s, t in zip(("y", "xs"), temps)]
            arrow = piece(code, "->", 3)
            cons = piece(code, "::", 3, nth=2)
            name = piece(code, "evens", 3)
            self.play(anims[0], anims[1], FadeIn(arrow, shift=0.2 * LEFT), FadeIn(cons, shift=0.2 * LEFT),
                      FadeIn(name, shift=0.2 * LEFT), cl[1].label.animate.set_color(YELLOW),
                      run_time=fit(c, "drop ex", lo=0.8, hi=1.3, frac=0.85))
            c.wait_until("drop ex")
            self.play(cl[0].label.animate.set_color(RED).set_opacity(0.4),
                      lab_x.animate.set_color(RED).set_opacity(0.5), run_time=0.7)
            c.wait_until("carry on")
            self.play(FlashAround(lab_xs, color=TEAL, time_width=1.5),
                      FlashAround(temps[1], color=TEAL, time_width=1.5), run_time=1.0)
        # the parts become the one Code they make up
        swap(self, [head, *pats, *rhs, temps[0], temps[1], arrow, cons, name], code)
        self.code, self.box, self.chain, self.br = code, box, chain, br
        self.labels = (lab_x, lab_y, lab_xs, xs_brace)

    # .4: the trace, the bracket hopping two cells per step
    def trace(self):
        code, box, chain, br = self.code, self.box, self.chain, self.br
        code.generate_target()
        code.target.scale(CODE_SMALL / CODE_BIG)
        code.target.move_to(ORIGIN).shift(UP * (3.55 - code.target.get_top()[1]))
        x0 = code.target.get_left()[0]
        chain.generate_target()
        chain.target.scale(CHAIN_SMALL / CHAIN_BIG).move_to([0, 0.5, 0])
        for cell in chain.target.cells:
            cell.label.set_color(FG).set_opacity(1)

        row_x = x0 + 0.8
        bases = [ROW_BASE0 - ROW_PITCH * k for k in range(5)]
        rows = [put(Code(s, size=ROW_SIZE), row_x, b) for s, b in zip(ROWS, bases)]
        arrows = [None] + [implies().next_to(r, LEFT, buff=0.3).set_y(b + 0.1) for r, b in zip(rows[1:], bases[1:])]
        row4 = put(Code(ROW4_FULL, size=ROW_SIZE), row_x, bases[3])
        reply = put(Code(REPLY, size=30), row_x, bases[4])
        cl = chain.cells

        with self.say("c6.evens.4") as c:
            # "On ten, twenty, thirty, forty, fifty,"
            self.play(MoveToTarget(code), Transform(box, cbox(code.target, "| x :: y :: xs", 3)),
                      MoveToTarget(chain), Transform(br, bracket(chain.target, 0, 1)),
                      *[FadeOut(m) for m in self.labels], run_time=1.4)
            self.play(FadeIn(rows[0], shift=0.2 * DOWN), run_time=1.0)
            # "we keep twenty, and carry on with thirty, forty, fifty."
            c.wait_until("s1")
            anims, temps = grow_from(rows[0], rows[1], [("20", "20"), ("evens", "evens"), ("[", "["),
                                                        ("30; 40; 50]", "30; 40; 50]")])
            self.play(*anims, FadeIn(arrows[1]), cl[1].label.animate.set_color(YELLOW),
                      cl[0].label.animate.set_color(DIM), run_time=fit(c, "carry on", lo=1.0, hi=1.5, frac=0.85))
            swap(self, temps, rows[1])
            c.wait_until("carry on")
            self.play(Transform(br, bracket(chain, 2, 3)), run_time=1.0)
            # "We keep forty, and carry on with fifty."
            c.wait_until("s2")
            anims, temps = grow_from(rows[1], rows[2], [("20 ::", "20 ::"), ("40", "40"), ("evens", "evens"),
                                                        ("[", "["), ("50]", "50]")])
            self.play(*anims, FadeIn(arrows[2]), cl[3].label.animate.set_color(YELLOW),
                      cl[2].label.animate.set_color(DIM),
                      run_time=min(1.3, max(0.9, 0.85 * c.until("carry on", floor=0.0, nth=1))))
            swap(self, temps, rows[2])
            c.wait_until("carry on", nth=1)
            self.play(Transform(br, bracket(chain, 4, 4)), run_time=0.9)
            # "A single element gives nil,"
            c.wait_until("s3")
            anims, temps = grow_from(rows[2], rows[3], [("20 :: 40 ::", "20 :: 40 ::"), ("evens [50]", "[]")])
            self.play(*anims, FadeIn(arrows[3]), Transform(box, cbox(code, "| [x]", 2)),
                      FlashAround(VGroup(*code.line(2)), color=YELLOW, time_width=1.5),
                      cl[4].label.animate.set_color(DIM), run_time=fit(c, "result", lo=0.9, hi=1.3, frac=0.85))
            swap(self, temps, rows[3])
            # "so the answer is twenty, forty."
            c.wait_until("result")
            anims, temps = grow_from(rows[3], row4, [("20 :: 40 :: []", "20 :: 40 :: []"),
                                                     (("20", 0), ("20", 1)), (("40", 0), ("40", 1))])
            self.play(*anims, time_span(FadeIn(reply, shift=0.2 * UP), 0.3, 1.0), run_time=1.0)
            swap(self, temps, row4, drop=[rows[3]])
        self.results = (row4, reply)

    # .5: the common mistake: no [x] clause
    def mistake(self):
        code = self.code
        l2, l3 = code.line(2), code.line(3)
        dy = code.find("|", line=2).get_y() - code.find("|", line=3).get_y()
        strike = Line(l2.get_left() + LEFT * 0.15, l2.get_right() + RIGHT * 0.15, color=RED, stroke_width=5)

        warn = VGroup(*[Mono(s, size=28) for s in WARN]).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        gslice(warn[0], WARN[0], "Warning 8 [partial-match]:").set_color(YELLOW)
        warn[3].set_color(TEAL)
        indent = 2 * 0.0083 * 28
        for m in warn[2:]:
            m.shift(RIGHT * indent)
        warn.move_to(ORIGIN).shift(UP * (1.1 - warn.get_top()[1]))
        lx = warn.get_left()[0]
        even_in = put(Code("evens [10; 20; 30; 40]", size=30), lx, -1.35)
        even_out = Mono(REPLY, size=28, color=GREEN)
        even_out.move_to([lx, -1.87, 0], aligned_edge=LEFT)
        odd_in = put(Code("evens [10; 20; 30]", size=30), lx, -2.67)
        odd_out = Mono('Exception: Match_failure ("//toplevel//", 1, 16).', size=28, color=RED)
        odd_out.move_to([lx, -3.19, 0], aligned_edge=LEFT)
        # the code without its [x] clause, as one object, lined up with the shrunk code
        code3 = Code(EVENS3, size=CODE_BIG).scale(CODE_SMALL / CODE_BIG)
        code3.shift(code.line(0).get_corner(UL) - code3.line(0).get_corner(UL))
        ok = check_mark(GREEN).next_to(even_out, RIGHT, buff=0.35)
        bad = cross_mark(RED).next_to(odd_out, RIGHT, buff=0.3)

        with self.say("c6.evens.5") as c:
            # "The common mistake is to forget the single element case."  (the trace stays)
            c.wait_until("single element")
            self.play(Create(strike), FadeOut(self.box), run_time=0.5)
            self.play(*[g.animate.set_opacity(0) for g in l2], FadeOut(strike),
                      *[g.animate.shift(UP * dy) for g in l3], run_time=fit(c, "warn", lo=0.7, hi=1.0, frac=0.9))
            swap(self, [], code3, drop=[code])
            # "OCaml warns you, with an example it can't match, a list of just one element."
            c.wait_until("warn")
            rt = min(2.2, max(1.6, c.until("just one element") - 0.3))
            sweep(self, time_span(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in warn],
                                              lag_ratio=0.2), 0.45 * rt, rt),
                  keep=[code3], late=self.results, run_time=rt)
            c.wait_until("just one element")
            xbox = token_box(warn[3], warn[3], color=YELLOW, pad=0.24)
            self.play(FadeIn(xbox), FlashAround(warn[3], color=YELLOW, time_width=1.5), run_time=1.0)
            # "On even lengths, the function seems fine."
            c.wait_until("even")
            self.play(FadeIn(even_in, shift=0.2 * DOWN),
                      time_span(FadeIn(even_out, shift=0.2 * DOWN), 0.5, 1.2),
                      time_span(Create(ok), 0.9, 1.4), run_time=1.4)
            # "But on ten, twenty, thirty, it's left with the thirty on its own, and fails."
            c.wait_until("odd")
            self.play(FadeIn(odd_in, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("on its own")
            tbox = token_box(odd_in.find("30"), odd_in, color=RED, pad=0.2)
            self.play(FadeIn(tbox), run_time=0.7)
            c.wait_until("and fails")
            self.play(FadeIn(odd_out, shift=0.2 * DOWN), time_span(Create(bad), 0.5, 1.1), run_time=1.1)
            # "So test odd and even lengths, and read the warnings."
            c.wait_until("lesson")
            self.play(FlashAround(odd_in, color=RED, time_width=1.5),
                      FlashAround(even_in, color=GREEN, time_width=1.5),
                      run_time=fit(c, "read the warnings", lo=0.8, hi=1.2))
            c.wait_until("read the warnings")
            back = piece(code, "[x]", 2)          # where the clause's pattern returns to
            swap(self, [], code, drop=[code3])
            self.play(FlashAround(warn, color=YELLOW, time_width=1.5),
                      FadeTransform(warn[3].copy(), back),
                      *[g.animate.set_opacity(1) for g in l2], *[g.animate.shift(DOWN * dy) for g in l3],
                      run_time=min(1.4, max(0.8, c.remaining - 0.1)))
            self.remove(back)
        self.failure = (odd_out, bad)

    # .6: cost; pending conses; an accumulator would gain nothing; the notes' line
    def cost(self):
        code = self.code
        time_row = cost_row("time").move_to([3.2, 3.35, 0], aligned_edge=LEFT)
        space_row = cost_row("space").move_to([3.2, 2.7, 0], aligned_edge=LEFT)

        # s2's pending column, on the right
        floor = Line([CX - PW / 2 - 0.25, FLOOR, 0], [CX + PW / 2 + 0.25, FLOOR, 0]).set_stroke(GOLD, 3)
        pend_label = T("pending conses", size=30, color=GOLD).move_to([CX, FLOOR - 0.42, 0])
        plates = [plate("20 ::", 0), plate("40 ::", 1)]

        # the ghost accumulator version, on the left
        acc_box = DashedVMobject(RoundedRectangle(corner_radius=0.15, width=3.0, height=1.0),
                                 num_dashes=40).set_stroke(DIM, 2.5).move_to([-4.6, -0.35, 0])
        acc0 = Code("[]", size=40).move_to(acc_box)
        acc_val = Code("[40; 20]", size=40).move_to(acc_box)
        rev_arrow = Arrow(acc_box.get_right() + RIGHT * 0.1, acc_box.get_right() + RIGHT * 1.35, buff=0,
                          stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.25, tip_length=0.2)
        rev_lab = Mono("rev", size=32, color=YELLOW).next_to(rev_arrow, UP, buff=0.12)
        answer = Code("[20; 40]", size=40).next_to(rev_arrow, RIGHT, buff=0.18)
        ans_brace = Brace(answer, DOWN, buff=0.15, color=GOLD)
        ans_on = MathTex("O(n)", font_size=44, color=GOLD).next_to(ans_brace, DOWN, buff=0.12)
        mid_x = (acc_box.get_left()[0] + answer.get_right()[0]) / 2
        acc_word = T("accumulator", size=36, color=GOLD)
        acc_q = T("?", size=40, color=GOLD).next_to(acc_word, RIGHT, buff=0.06, aligned_edge=DOWN)
        VGroup(acc_word, acc_q).move_to([mid_x, 0.75, 0])
        verdict = VGroup(cross_mark(RED, r=0.22), T("no gain", size=38, color=RED)).arrange(RIGHT, buff=0.3)
        verdict.move_to([mid_x, -2.55, 0])

        # the quote card, in the style of s5's Milner card (ch6_s5_types.py)
        card = RoundedRectangle(corner_radius=0.25, width=12.2, height=4.0)
        card.set_stroke(DIM, 2).set_fill(CARD_FILL, 1).move_to(ORIGIN)
        mark = T("“", size=110, color=GOLD).move_to(card.get_corner(UL) + np.array([0.55, -0.55, 0]))
        quote = VGroup(T("Never add an accumulator", size=48, slant=ITALIC),
                       T("merely out of habit.", size=48, slant=ITALIC)).arrange(DOWN, buff=0.32)
        quote.move_to([0, 0.6, 0])
        who = T("Lecture notes", size=34).move_to([5.6, -0.8, 0], aligned_edge=RIGHT)
        src = T("Foundations of Computer Science · Lecture 3", size=28, color=DIM, slant=ITALIC)
        src.move_to([5.6, -1.35, 0], aligned_edge=RIGHT)
        quote_card = (card, mark, quote, who, src)
        for k, m in enumerate(quote_card):
            m.set_z_index(2 if k == 0 else 3)     # above s2-style plates (z 1)

        with self.say("c6.evens.6") as c:
            # "The time is big O of en."  (the tests stay up a little longer)
            c.wait_until("big o")
            self.play(FadeIn(time_row, shift=0.2 * DOWN), FlashAround(time_row[1], color=GOLD, time_width=1.5),
                      run_time=1.0)
            # "But like append, it builds a chain of pending conses, so it needs big O of en space."
            c.wait_until("like append")
            ycons = VGroup(*code.find("y ::", line=3, nth=1))
            sweep(self, time_span(Create(floor), 0.5, 1.1),
                  time_span(FadeIn(pend_label, shift=0.2 * UP), 0.7, 1.3),
                  time_span(FadeIn(plates[0][0]), 0.8, 1.6),
                  time_span(TransformFromCopy(ycons, plates[0][1], path_arc=-0.4), 0.8, 1.6),
                  keep=[code, time_row], late=self.failure, run_time=1.6)
            c.wait_until("pending conses")
            self.play(FadeIn(plates[1][0]), TransformFromCopy(ycons, plates[1][1], path_arc=-0.4), run_time=1.0)
            for pl in plates:
                swap(self, [*pl.get_family()], pl)
            c.wait_until("en space")
            self.play(FadeIn(space_row, shift=0.2 * DOWN), FlashAround(space_row[1], color=GOLD, time_width=1.5),
                      FlashAround(VGroup(*plates), color=GOLD, time_width=1.5), run_time=1.1)
            # "Could an accumulator fix that?"
            c.wait_until("acc")
            self.play(FadeIn(acc_word, shift=0.2 * DOWN), FadeIn(acc_q, scale=0.6), Create(acc_box),
                      FadeIn(acc0), run_time=1.2)
            # "It would build the answer backwards, needing a reverse at the end, ..."
            c.wait_until("rev")
            grow, temps = [], []
            for pl, sub in zip(plates, ("20", "40")):
                tgt = piece(acc_val, sub)
                grow.append(TransformFromCopy(gslice(pl[1], pl[1].text, sub), tgt))
                temps.append(tgt)
            brk = VGroup(*[g.copy() for g in acc_val.text
                           if id(g) not in {id(x) for s in ("20", "40") for x in acc_val.find(s)}])
            self.play(*grow, ReplacementTransform(acc0, brk), run_time=fit(c, "a reverse", lo=1.0, hi=1.5))
            swap(self, [*temps, brk], acc_val)
            c.wait_until("a reverse")
            anims, temps = grow_from(acc_val, answer, [("20", "20"), ("40", "40")])
            self.play(GrowArrow(rev_arrow), FadeIn(rev_lab, shift=0.2 * DOWN), *anims,
                      run_time=fit(c, "the answer itself", lo=1.0, hi=1.5))
            swap(self, temps, answer)
            # "... and the answer itself takes big O of en space anyway."
            c.wait_until("the answer itself")
            self.play(GrowFromCenter(ans_brace), FadeIn(ans_on, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("takes big o")
            self.play(ReplacementTransform(acc_q, verdict[0]), FadeIn(verdict[1], shift=0.2 * LEFT),
                      run_time=min(1.0, max(0.6, 0.8 * c.until("habit", floor=0.0))))
            # "As the notes say, never add an accumulator merely out of habit."  The board dims
            # to 0.12 under the quote card (Milner-card style, s5), then leaves after the clip
            c.wait_until("habit")
            board = list(self.mobjects)
            self.play(*[restyle(m, op=0.12) for m in board],
                      time_span(AnimationGroup(FadeIn(card), FadeIn(mark, scale=0.7)), 0.3, 1.1),
                      time_span(FadeIn(who, shift=0.2 * LEFT), 0.7, 1.4),
                      time_span(FadeIn(src, shift=0.2 * LEFT), 0.8, 1.5), run_time=1.5)
            self.play(Write(quote), run_time=min(1.8, max(1.0, 0.9 * c.remaining)))
            self.quote_born = self.time
        # "no gain" has had its time: the board goes, the quote stands alone
        self.play(*[FadeOut(m) for m in board], run_time=1.0)
