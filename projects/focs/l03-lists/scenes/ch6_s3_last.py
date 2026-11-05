"""Chapter 6, scene 3: the solution to exercise 3.2, the last element. Clips c6.last.1 - c6.last.7.

Opens on s1's five-card row (ch5_s6's overview: BigCards 2.4x1.8, centres x = -5.3 ... 5.3,
y = 0.7); card 3.2 grows into the kit's hero card, then the kit's pause tag (top right).
The code is built out of two list shapes (one cell -> [], a cell -> xs); OCaml's reply
(warning 8, the type), last [] raising Match_failure beside a dimmed hd; a trace on the
3 -> 5 -> 9 -> [] chain (shared with s2); the swapped-clauses mistake (warning 11,
Match_failure); the `| [] -> 0` temptation ('a turns int); the cost: O(n) time, O(1) space,
against List.hd (List.rev ...) with its reversed copy.

Layout: the code sits top left for the whole solution (left edge x = -6.3, 3 lines at 40,
centre y = 2.4); notes go in a column to its right (x >= 2.0); OCaml's replies, calls and
traces go below it; the chain at y = -1.6.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch5_s6_sumlast import (  # noqa: E402  the shared exercise-card kit (read-only)
    BigCard, HeroCard, Tag, at_row, finish, hold_for, pause_tag)

# ── the code and OCaml's replies (verified with ocaml 5.4.1) ─────────────────────
SRC = """let rec last = function
  | [x] -> x
  | x :: xs -> last xs"""
SWAP_SRC = """let rec last = function
  | x :: xs -> last xs
  | [x] -> x"""
ZERO_SRC = SRC + "\n  | [] -> 0"
L0, L1, L2 = "let rec last = function", "| [x] -> x", "| x :: xs -> last xs"
SAME3 = [((L0, 0), (L0, 0)), ((L1, 1), (L1, 1)), ((L2, 2), (L2, 2))]


def bump(dx):
    """A path that swings sideways by dx on the way (so two swapping lines never overlap)."""
    def f(start, end, alpha):
        return start + alpha * (end - start) + np.array([dx, 0, 0]) * np.sin(np.pi * alpha)
    return f


SWING = {"path_func": bump(7.0)}        # the short [x] clause steps out right, past the long one
SWAP = [((L0, 0), (L0, 0)), ((L1, 1), (L1, 2), SWING), ((L2, 2), (L2, 1))]     # SRC -> SWAP_SRC
UNSWAP = [((L0, 0), (L0, 0)), ((L2, 1), (L2, 2)), ((L1, 2), (L1, 1), SWING)]   # SWAP_SRC -> SRC
# warnings wrapped as ch2_s3_hdtl shows them (the same warning 8 as hd's)
W8_SRC = ("Warning 8 [partial-match]:\n"
          "this pattern-matching is not exhaustive.\n"
          "Here is an example of a case that is not matched: []")
W11_SRC = "Warning 11 [redundant-case]:\nthis match case is unused."
VAL_A = "val last : 'a list -> 'a = <fun>"
VAL_INT = "val last : int list -> int = <fun>"
EXC_SRC = 'Exception: Match_failure ("//toplevel//", 1, 15).'

# ── layout ──────────────────────────────────────────────────────────────────────
CODE_SIZE = 40
CODE_L, CODE_Y = -6.3, 2.4          # the definition, top left
OUT_L = -6.1                        # left edge of OCaml's replies
RC_X = 2.0                          # the note column right of the code
R1, R2, R3 = 2.95, 2.25, 1.55       # its rows
SHAPE_Y, SHAPE1_X, SHAPE2_X = -1.3, -3.4, 2.9
WARN_Y, VAL_Y, NIL_Y, EXC_Y = 0.0, -1.4, -2.25, -2.9    # clip 3's reply column
MID_Y, CALL_L = 0.35, -2.55         # the call being traced, above the chain
CHAIN_Y = -1.6
LOW_Y = -2.85                       # under the chain
VAL6_Y = 0.1                        # clip 6's type, under the 4-line code
REV_X, REV_Y = -0.9, -2.55            # the reversed copy (clip 7); the chain moves up to -0.95
CHAIN_UP = 0.65 * UP + 0.9 * LEFT


# ── helpers (local) ─────────────────────────────────────────────────────────────
def _glyphs(code, spec):
    """spec: "sub" or ("sub", line) or ("sub", line, nth)."""
    if isinstance(spec, str):
        return list(code.find(spec))
    sub, line, *rest = spec
    return list(code.find(sub, line=line, nth=rest[0] if rest else 0))


def morph(scene, a, b, pairs=(), born=(), run_time=1.2, path_arc=0, extra=(), shift=0.2 * DOWN, span=None):
    """Rewrite Code `a` (None: nothing) into Code `b`, already placed: each glyph run in
    `pairs` moves to its new place, each (source, run of b) in `born` flies out of a copy of
    the source, the rest of a fades out and the rest of b fades in. Works on glyph copies,
    so neither Code is pulled apart; afterwards b alone is on screen."""
    anims, temps, used_a, used_b = [], [], set(), set()
    for sa, sb, *kw in pairs:
        xs, ys = _glyphs(a, sa), _glyphs(b, sb)
        used_a.update(map(id, xs))
        used_b.update(map(id, ys))
        t = VGroup(*[x.copy() for x in xs])
        temps.append(t)
        anims.append(Transform(t, VGroup(*[y.copy() for y in ys]), **(kw[0] if kw else {"path_arc": path_arc})))
    if a is not None:
        gone = VGroup(*[x.copy() for x in a.text if id(x) not in used_a])
        scene.remove(a)
        scene.add(*temps, gone)
        if len(gone):
            anims.append(FadeOut(gone))
    for src, sb in born:
        ys = _glyphs(b, sb)
        used_b.update(map(id, ys))
        t = VGroup(*[y.copy() for y in ys])
        temps.append(t)
        anims.append(TransformFromCopy(src, t))
    new = VGroup(*[y.copy() for y in b.text if id(y) not in used_b])
    if len(new):
        temps.append(new)
        anims.append(FadeIn(new, shift=shift))
    if span is not None:
        anims = [time_span(x, *span) for x in anims]
    scene.play(*anims, *extra, run_time=run_time)
    scene.remove(*temps)
    scene.add(b)


class Pieces:
    """Copies of a Code's glyphs, handed out run by run to bring the code on screen bit by
    bit; done() swaps them all for the Code itself (it looks identical)."""

    def __init__(self, code):
        self.code, self.copies, self.groups = code, {}, []

    def get(self, sub, line=None, nth=0):
        g = VGroup(*[self.copies.setdefault(id(x), x.copy()) for x in self.code.find(sub, line=line, nth=nth)])
        self.groups.append(g)
        return g

    def done(self, scene):
        scene.remove(*self.groups)
        scene.add(self.code)


def recolor_code(code, base, spans):
    """A Code block read as plain toplevel output: one base colour, a few spans picked out."""
    code.text.set_color(base)
    for sub, color in spans:
        VGroup(*code.find(sub)).set_color(color)
    return code


def place(mob, x, y):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def cost_label(kind, big, x, y):
    lab = place(T(kind, size=38), x, y)
    o = place(MathTex(big, font_size=52, color=GOLD), x + 1.45, y)
    return VGroup(lab, o)


class LastSolution(NarratedScene):
    def construct(self):
        self.statement()
        self.shapes()
        self.reply()
        self.trace()
        self.mistake()
        self.zero()
        self.cost()
        hold_for(self, self.labels_born, len("time O(n) space O(n)"))
        finish(self)

    # last.1: the five cards; 3.2 grows into the hero card; the pause tag
    def statement(self):
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * 0.7)
        big = bigs[1]
        card = HeroCard(1, height=2.72)
        task = at_row(T("Return the last element of a non-empty list.", size=36), 1)
        ask = at_row(T("How efficiently can this be done?", size=36, color=GOLD), 2)
        card.lower(task, ask)
        tag = pause_tag()

        with self.say("c6.last.1") as c:
            # "Exercise three point two."  s1's row comes back; card 3.2 becomes the hero card
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * UP) for b in bigs], lag_ratio=0.1), run_time=0.8)
            self.wait(0.9)     # the row settles before 3.2 grows (as s2, s5, s6 open)
            self.play(TransformFromCopy(big.frame, card.frame), FadeTransform(big.num.copy(), card.header),
                      *[FadeOut(b) for b in bigs], run_time=1.2)
            # "Code a function to return the last element of a non-empty list."
            c.wait_until("code a function")
            self.play(FadeIn(task, shift=0.25 * DOWN), run_time=1.0)
            # "How efficiently can this be done?"
            c.wait_until("how efficiently")
            self.play(FadeIn(ask, shift=0.25 * DOWN), run_time=1.0)
            # "Pause now, if you'd like a go."  Then still.
            c.wait_until("stop")
            self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.8)
        self.tag = tag

    # last.2: the two shapes of list with an obvious last element become the two clauses
    def shapes(self):
        code = place(Code(SRC, size=CODE_SIZE), CODE_L, CODE_Y)
        P = Pieces(code)
        head, head_last = P.get(L0, line=0), P.get("last", line=0)
        pat1, arr1, res1 = P.get("| [x]", line=1), P.get("->", line=1), P.get("x", line=1, nth=1)
        pat2, arr2 = P.get("| x :: xs", line=2), P.get("->", line=2)
        rlast, rxs = P.get("last", line=2), P.get("xs", line=2, nth=1)

        one = ConsChain(["x"]).move_to([SHAPE1_X, SHAPE_Y, 0])
        cell = ConsCell("x")
        rest = DashedVMobject(RoundedRectangle(corner_radius=0.16, width=2.3, height=CELL),
                              num_dashes=26).set_stroke(BLUE, 3)
        rest.next_to(cell, RIGHT, buff=LINK)
        xs = T("xs", size=42, slant=ITALIC).move_to(rest)
        arrow = Arrow(cell.tail_start(), rest.get_left(), buff=0, stroke_width=3, color=FG,
                      max_tip_length_to_length_ratio=0.3, tip_length=0.16)
        two = VGroup(cell, arrow, rest, xs).move_to([SHAPE2_X, SHAPE_Y, 0])

        with self.say("c6.last.2") as c:
            # "Which lists have an obvious last element?"  The card clears; the header and two shapes
            sweep_clear(self, time_span(FadeIn(head, shift=0.25 * DOWN), 0.5, 1.4),
                        time_span(LaggedStart(FadeIn(one, shift=0.3 * UP), FadeIn(two, shift=0.3 * UP),
                                              lag_ratio=0.35), 0.8, 2.2), keep=[self.tag], run_time=2.2)
            # "If the list holds a single element, ex, the answer is ex."
            c.wait_until("single")
            self.play(TransformFromCopy(one, pat1), restyle(two, op=0.3), FadeOut(self.tag), run_time=1.5)
            c.wait_until("the answer is")
            self.play(FadeIn(arr1, shift=0.2 * RIGHT), TransformFromCopy(one.cells[0].label, res1), run_time=1.2)
            # "Any longer list is a head consed onto exes, and its last element is the last element of exes."
            c.wait_until("longer")
            self.play(TransformFromCopy(two, pat2), restyle(two, op=1), restyle(one, op=0.3), run_time=1.5)
            c.wait_until("the last element of exes")
            self.play(FadeIn(arr2, shift=0.2 * RIGHT), TransformFromCopy(head_last, rlast),
                      TransformFromCopy(xs, rxs), run_time=1.5)
        P.done(self)
        self.code, self.one, self.two = code, one, two

    # last.3: OCaml's reply: warning 8 (fine: non-empty), last [] fails like hd, the type
    def reply(self):
        wtext = recolor_code(Code(W8_SRC, size=28), FG, [("Warning 8 [partial-match]:", YELLOW), ("[]", TEAL)])
        place(wtext, OUT_L, WARN_Y)
        wbox = SurroundingRectangle(wtext, buff=0.2, color=YELLOW, stroke_width=3, corner_radius=0.08)
        val = place(Code(VAL_A, size=32), OUT_L, VAL_Y)
        w_nil = VGroup(*wtext.find("[]"))
        ok = check_mark(GREEN)
        ok_t = T("non-empty lists only", size=30, color=GREEN)
        note = VGroup(ok, ok_t).arrange(RIGHT, buff=0.22)
        place(note, RC_X, R1)
        hd = place(Code("let hd (x::l) = x", size=30), RC_X, R2).set_opacity(0.5)
        w8 = place(Mono("Warning 8", size=28, color=YELLOW), RC_X, R3).set_opacity(0.5)
        nilcall = place(Code("last []", size=32), OUT_L, NIL_Y)
        exc = place(Code(EXC_SRC, size=28), OUT_L, EXC_Y)
        exc.text.set_color(RED)
        only_call = place(Code('last ["only"]', size=28), RC_X, R1 - 0.2)
        only_reply = place(Code('- : string = "only"', size=28), RC_X, R2 - 0.2)

        with self.say("c6.last.3") as c:
            # "OCaml accepts it with a warning, because the empty list isn't covered."
            c.wait_until("warning")
            self.play(LaggedStart(FadeOut(self.one), FadeOut(self.two), lag_ratio=0.2),
                      time_span(Create(wbox), 0.3, 1.3), time_span(FadeIn(wtext, shift=0.2 * DOWN), 0.5, 1.5),
                      time_span(FadeIn(val, shift=0.2 * DOWN), 1.3, 2.1), run_time=2.1)
            # "That's fine, since the exercise promised a non-empty list."
            c.wait_until("fine")
            self.play(Create(ok), FadeIn(ok_t, shift=0.2 * LEFT), run_time=1.0)
            # "Like the head function, it raises an exception on nil."  (hd, dimmed, had the same warning)
            c.wait_until("like the head function")
            self.play(FadeIn(hd, shift=0.2 * DOWN), FadeIn(w8, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("raises")
            morph(self, None, nilcall, born=[(w_nil, "[]")], run_time=min(1.7, max(1.0, 0.9 * c.until("type"))),
                  extra=[time_span(FadeIn(exc, shift=0.15 * DOWN), 0.7, 1.0)])
            # "Its type is alpha list to alpha, so it works on lists of anything."
            c.wait_until("type")
            self.play(FlashAround(VGroup(*val.find("'a list -> 'a")), color=PINK, time_width=1.5),
                      run_time=min(1.3, max(0.6, 0.9 * c.until("so it works"))))
            c.wait_until("so it works")
            rt = min(1.2, max(0.4, c.remaining))
            self.play(FadeOut(note), FadeOut(hd), FadeOut(w8),
                      time_span(FadeIn(only_call, shift=0.2 * DOWN), 0.25 * rt, 0.8 * rt),
                      time_span(FadeIn(only_reply, shift=0.2 * DOWN), 0.4 * rt, rt), run_time=rt)
        self.only = (only_call, only_reply)
        self.nil_bits = (nilcall, exc)

    # last.4: the trace: a marker steps along 3 -> 5 -> 9 while the call rewrites in place
    def trace(self):
        code = self.code
        chain = ConsChain([3, 5, 9]).move_to([0, CHAIN_Y, 0])
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil
        calls = [place(Code(s, size=44), CALL_L, MID_Y) for s in ("last [3; 5; 9]", "last [5; 9]", "last [9]")]
        reply = place(Code("- : int = 9", size=44), CALL_L, MID_Y)
        mk = marker(YELLOW).move_to(above(cells[0].box))

        with self.say("c6.last.4") as c:
            # "On three, five, nine, it steps along,"
            sweep_clear(self, time_span(FadeIn(chain, shift=0.3 * UP), 0.4, 1.4),
                        time_span(FadeIn(calls[0], shift=0.2 * DOWN), 0.6, 1.4),
                        time_span(FadeIn(mk, shift=0.2 * DOWN), 1.0, 1.6),
                        *set_alpha(self.nil_bits, 0.5), keep=[code, *self.only, *self.nil_bits], run_time=1.6)
            # "to five, nine,"
            c.wait_until("s1")
            morph(self, calls[0], calls[1], [("last [", "last ["), ("5; 9]", "5; 9]")], run_time=1.0,
                  extra=[mk.animate.move_to(above(cells[1].box)), restyle(cells[0], op=0.3),
                         restyle(arrows[0], op=0.3)])
            # "then to nine,"
            c.wait_until("s2")
            morph(self, calls[1], calls[2], [("last [", "last ["), ("9]", "9]")], run_time=0.6,
                  extra=[mk.animate.move_to(above(cells[2].box)), restyle(cells[1], op=0.3),
                         restyle(arrows[1], op=0.3)])
            # "which matches the single element clause, so the answer is nine."
            c.wait_until("s3")
            self.play(FlashAround(VGroup(*code.line(1)), time_width=1.5),
                      flash_along(cells[2], nil, color=TEAL), *[FadeOut(m) for m in self.nil_bits], run_time=1.1)
            c.wait_until("the answer is")
            morph(self, calls[2], reply, born=[(cells[2].label, "9")], run_time=min(1.0, max(0.5, c.remaining - 0.1)))
        self.chain, self.mk, self.reply_9 = chain, mk, reply

    # last.5: the clauses swapped: [9] is 9 :: [], so the general clause walks on to nil
    def mistake(self):
        code, chain, mk = self.code, self.chain, self.mk
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil
        sw = Code(SWAP_SRC, size=CODE_SIZE).move_to(code.get_corner(UL), aligned_edge=UL)
        good = Code(SRC, size=CODE_SIZE).move_to(code.get_corner(UL), aligned_edge=UL)
        call_q = place(Code("last [3; 5; 9]", size=44), CALL_L, MID_Y)
        q = T("?", size=96, color=GOLD).next_to(call_q, RIGHT, buff=0.5)
        eq = place(Code("[9]  =  9 :: []", size=44), CALL_L, MID_Y)
        tail = Code("xs = []", size=36)
        tail.text.set_color(TEAL)
        tail.next_to(nil, RIGHT, buff=0.55)
        exc = place(Code(EXC_SRC, size=28), OUT_L, LOW_Y)
        exc.text.set_color(RED)
        w11 = recolor_code(Code(W11_SRC, size=28), FG, [("Warning 11 [redundant-case]:", YELLOW)])
        place(w11, OUT_L, 0.5)
        w11box = SurroundingRectangle(w11, buff=0.15, color=YELLOW, stroke_width=3, corner_radius=0.08)
        lit = (cells[0], cells[1], arrows[0], arrows[1])

        with self.say("c6.last.5") as c:
            # "Here's a classic mistake."
            self.play(*[FadeOut(m) for m in self.only], FadeOut(mk), *[restyle(m, op=1) for m in lit], run_time=1.0)
            # "Write the two clauses the other way round."
            c.wait_until("write the two clauses")
            morph(self, code, sw, SWAP, run_time=2.0)
            # "What goes wrong?"  Hold on the question.
            c.wait_until("ask")
            morph(self, self.reply_9, call_q, [("9", "9")], run_time=1.0, extra=[FadeIn(q, scale=0.6)])
            # "A list of just nine is also a head consed onto a tail, the tail being nil."
            c.wait_until("catch")
            mk.move_to(above(cells[2].box))
            morph(self, call_q, eq, [("[", "["), ("9]", "9]")], born=[(q, "9 :: []")], run_time=1.5,
                  extra=[FadeOut(q), FadeIn(mk, shift=0.2 * DOWN), *[restyle(m, op=0.3) for m in lit]])
            c.wait_until("the tail being nil")
            tbox = token_box(sw.find("x :: xs", line=1), sw.line(1))
            morph(self, None, tail, born=[(VGroup(*sw.find("xs", line=1)), "xs"), (nil, "[]")], run_time=1.4,
                  extra=[FadeIn(tbox)])
            # "So the general clause catches it, and the walk carries on to nil, where nothing matches."
            c.wait_until("so the general clause")
            self.play(FlashAround(VGroup(*sw.line(1)), time_width=1.5), run_time=1.2)
            c.wait_until("carries on to nil")
            self.play(mk.animate.move_to(above(nil)), restyle(cells[2], op=0.3),
                      flash_along(cells[2], nil, color=YELLOW), run_time=1.0)
            c.wait_until("nothing matches")
            self.play(nil.animate.set_color(RED), mk.animate.set_color(RED),
                      FadeIn(exc, shift=0.2 * DOWN), run_time=1.0)
            # "OCaml even warns that the single element clause is unused."
            c.wait_until("unused")
            self.play(FadeOut(eq), Transform(tbox, token_box(sw.find("[x]", line=2), sw.line(2))),
                      time_span(Create(w11box), 0.2, 1.2), time_span(FadeIn(w11, shift=0.2 * DOWN), 0.4, 1.4),
                      run_time=1.4)
            # "Order matters."  The clauses go back; the swapped version's replies fade back.
            c.wait_until("order")
            morph(self, sw, good, UNSWAP,
                  run_time=min(2.0, max(1.2, 0.9 * c.until("put the most specific"))),
                  extra=[FadeOut(tbox), *set_alpha([w11, w11box, exc], 0.5)])
            # "Put the most specific pattern first."
            c.wait_until("put the most specific")
            gbox = token_box(good.find("[x]", line=1), good.line(1), color=GREEN)
            spec = place(T("most specific first", size=32, color=GREEN), RC_X, good.line(1).get_y())
            self.play(FadeIn(gbox), FadeIn(spec, shift=0.2 * LEFT),
                      *[FadeOut(m) for m in (tail, mk)], nil.animate.set_color(TEAL),
                      *[restyle(m, op=1) for m in (*cells, *arrows[:2])], run_time=1.0)
        self.code, self.gbox, self.spec = good, gbox, spec
        self.old_order = (w11, w11box, exc)     # dimmed; they leave when the zero clause arrives

    # last.6: | [] -> 0: the type becomes int list -> int, and last [] makes up an answer
    def zero(self):
        code, chain = self.code, self.chain
        nil = chain.nil
        zc = Code(ZERO_SRC, size=CODE_SIZE).move_to(code.get_corner(UL), aligned_edge=UL)
        val_a = place(Code(VAL_A, size=30), OUT_L, VAL6_Y)
        val_i = place(Code(VAL_INT, size=30), OUT_L, VAL6_Y)
        ok = check_mark(GREEN)
        any_t = T("works on any list", size=28, color=GREEN)
        anyl = VGroup(ok, any_t).arrange(RIGHT, buff=0.2)
        place(anyl, val_i.get_right()[0] + 0.4, VAL6_Y)
        bad = cross_mark(RED).move_to(ok)
        made = Code("last []  ⇒  - : int = 0", size=32).move_to([0, LOW_Y, 0])
        zero_g = VGroup(*made.find("0"))
        zero_g.set_color(RED)

        with self.say("c6.last.6") as c:
            # "Another temptation is to say that the last element of nil is zero."
            self.play(restyle(chain, op=0.3), run_time=1.0)
            c.wait_until("the last element of nil")
            rt = min(1.5, max(0.9, 0.95 * c.until("mono")))
            morph(self, code, zc, SAME3, run_time=rt,
                  extra=[*[time_span(FadeOut(m), 0, 0.45 * rt) for m in self.old_order],
                         time_span(FadeIn(val_a, shift=0.2 * DOWN), 0.45 * rt, 0.9 * rt),
                         time_span(FadeIn(anyl, shift=0.2 * DOWN), 0.55 * rt, rt)])
            # "But then the type becomes int list to int, and on nil it returns a made-up answer."
            c.wait_until("mono")
            morph(self, val_a, val_i,
                  [("val last :", "val last :"), (("'a", None, 0), ("int", None, 0)), ("list ->", "list ->"),
                   (("'a", None, 1), ("int", None, 1)), ("= <fun>", "= <fun>")], run_time=1.5,
                  extra=[ReplacementTransform(ok, bad), any_t.animate.set_color(RED)])
            c.wait_until("on nil it returns")
            morph(self, None, made, born=[(nil, "[]")], run_time=1.2, extra=[FadeOut(self.spec), FadeOut(self.gbox)])
            c.wait_until("answer")
            self.play(FlashAround(zero_g, color=RED, time_width=1.5), run_time=min(1.0, max(0.5, c.remaining - 0.1)))
        self.zc, self.zero_stuff = zc, [val_i, bad, any_t, made]

    # last.7: the cost: a walk to the end (O(n) time), a tail call (O(1) space); rev's copy
    def cost(self):
        zc, chain, mk = self.zc, self.chain, self.mk
        cells = chain.cells
        final = Code(SRC, size=CODE_SIZE).move_to(zc.get_corner(UL), aligned_edge=UL)
        time_l = cost_label("time", "O(n)", RC_X, R1)
        space_l = cost_label("space", "O(1)", RC_X, R2)
        it_tag = Tag("already iterative", GREEN)
        place(it_tag, RC_X, R3)
        start, end = above(cells[0].box), above(cells[2].box)

        expr, rep = [place(Code(s, size=32), OUT_L, MID_Y) for s in
                     ("List.hd (List.rev [3; 5; 9])", "List.hd (List.rev [3; 5; 9])  ⇒  - : int = 9")]
        rep = Code("⇒  - : int = 9", size=32).move_to(VGroup(*rep.find("⇒  - : int = 9")))
        rev = ConsChain([9, 5, 3]).move_to([REV_X, REV_Y, 0])
        rx = rev.get_right()[0] + 0.55
        rt_l = cost_label("time", "O(n)", rx, REV_Y + 0.33)
        rs_l = cost_label("space", "O(n)", rx, REV_Y - 0.37)

        with self.say("c6.last.7") as c:
            # "So how efficient is it?"  The list comes back into the light, the marker at its head.
            mk.move_to(start).set_color(YELLOW)
            self.play(restyle(chain, op=1), FadeIn(mk, shift=0.2 * DOWN), run_time=1.0)
            # "There's no shortcut to the end of a list, so it takes big O of en time."
            # The right definition comes back while the marker walks the whole list, slowly.
            c.wait_until("walk")
            walk = max(3.8, 0.95 * c.until("space"))
            t1 = min(2.4, walk - 1.4)                    # first leg; the zero version leaves after it
            mid = start + (end - start) * (t1 / walk)
            trails = [Line(a, b).set_stroke(GOLD, 5).set_z_index(-1) for a, b in ((start, mid), (mid, end))]
            self.play(mk.animate(rate_func=linear).move_to(mid), Create(trails[0], rate_func=linear), run_time=t1)
            t2 = walk - t1
            s = min(max(0.0, c.until("big o of en time", floor=0.0)), t2 - 0.8)
            morph(self, zc, final, SAME3, run_time=t2, span=(0, min(1.2, t2)),
                  extra=[*[time_span(FadeOut(m), 0, 0.8) for m in self.zero_stuff],
                         mk.animate(rate_func=linear).move_to(end), Create(trails[1], rate_func=linear),
                         time_span(FadeIn(time_l, shift=0.2 * DOWN), s, s + 0.8)])
            # "But the space is only big O of one, because the recursive call is the last thing that happens."
            c.wait_until("space")
            self.play(FadeIn(space_l, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("the recursive call")
            lx = VGroup(*final.find("last xs", line=2))
            self.play(FadeIn(token_box(final.find("last xs", line=2), final.line(2), color=GREEN)),
                      FlashAround(lx, color=GREEN, time_width=1.5), run_time=1.2)
            # "It's already iterative, with no accumulator needed."
            c.wait_until("already")
            self.play(FadeIn(it_tag, shift=0.2 * DOWN), run_time=0.9)
            # "Reversing the list and taking its head also works, but the reversed copy costs big O of en space."
            c.wait_until("rev")
            self.play(FadeOut(mk), *[FadeOut(t) for t in trails], chain.animate.shift(CHAIN_UP),
                      FadeIn(expr, shift=0.2 * DOWN), run_time=1.0)
            self.play(LaggedStart(*[TransformFromCopy(cells[2 - i], rev.cells[i]) for i in range(3)], lag_ratio=0.25),
                      time_span(LaggedStart(*[GrowArrow(a) for a in rev.arrows], lag_ratio=0.3), 0.7, 1.5),
                      time_span(FadeIn(rev.nil), 1.1, 1.6), run_time=1.6)
            c.wait_until("also works")
            self.play(FadeIn(rep, shift=0.2 * LEFT), run_time=0.8)
            c.wait_until("big o of en space")
            self.play(LaggedStart(FadeIn(rt_l, shift=0.2 * LEFT), FadeIn(rs_l, shift=0.2 * LEFT), lag_ratio=0.4),
                      FlashAround(VGroup(*rev.cells, *rev.arrows, rev.nil), color=GOLD, time_width=1.5),
                      run_time=min(1.3, max(0.6, c.remaining - 0.1)))
        self.labels_born = self.time
