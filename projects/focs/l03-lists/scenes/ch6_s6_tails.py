"""Chapter 6, scene 6: Exercise 3.5, tails. Clips c6.tails.1 - c6.tails.6.

Plan. tails.1: s1's five-card row (ch5_s6 overview geometry) fades in; card 3.5 grows into the
kit's hero card ("Exercise 3.5"), task, then the example, each tail of the answer
flying out of the input's suffix; the kit's pause tag comes with the card, flashed on {stop}.
tails.2: the card shrinks to a one-line reference at the top; the tails flash in turn; the two
cases are asked as equations (tails [] => ? turns into [[]], out of the answer's final [];
tails l => l :: tails xs, "l = x :: xs" underneath), which rebuild into the code on {match}
(whole-list l in YELLOW) + its val reply.
tails.3: code and reply go up; the trace, each line born from the one above; the answer, four
tails numbered in GOLD.
tails.4: memory. The answer at the top, the chain 1 -> 2 -> 3 -> [] below; the tempting picture
(three copies, "copied: 6") crossed out; then the outer spine of four BLUE cells whose TEAL value
arrows drop into the one chain (ch1_s5 sharing look: TEAL outlines, TEAL box, "shared", padlock
+ "never changes"), "new cells: 4".
tails.5: the two mistakes: `| [] -> []` (same type, the [] missing as a RED gap), then addtails
(@ copies acc: 1 + 2 + 3 + ... + n = O(n^2), like a dimmed nrev).
tails.6: the code and a small cost table: time O(n), space O(n), not iterative.
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
    CARD_FILL, COL_X, BigCard, HeroCard, at_row, fit, hold_for, pause_tag,
)

# ── sources (OCaml 5.4.1 replies as quoted by the brief) ─────────────────────────
TAILS = """let rec tails l = match l with
  | [] -> [[]]
  | x :: xs -> l :: tails xs"""
WRONG1 = TAILS.replace("-> [[]]", "-> []")
ADDTAILS = """let rec addtails acc l = match l with
  | [] -> acc @ [[]]
  | x :: xs -> addtails (acc @ [l]) xs"""
VAL = "val tails : 'a list -> 'a list list = <fun>"
EX_IN = "tails [1; 2; 3]"
ANSWER = "[[1; 2; 3]; [2; 3]; [3]; []]"
EX_OUT = "⇒  " + ANSWER
OUT_PARTS = ["⇒  [", "[1; 2; 3];", "[2; 3];", "[3];", "[]]"]   # revealed one tail at a time
REF = EX_IN + "  " + EX_OUT
EQ1 = "tails []  ⇒  [[]]"
EQ2 = "tails l   ⇒  l :: tails xs"
TRACE = ["⇒ [1; 2; 3] :: tails [2; 3]",
         "⇒ [1; 2; 3] :: [2; 3] :: tails [3]",
         "⇒ … :: [3] :: tails []",
         "⇒ … :: [3] :: [[]]"]
REPLY1 = "- : int list list = [[1; 2; 3]; [2; 3]; [3]"     # the wrong base case's answer

# the whole-list l (YELLOW) in each piece of code: (substring, line, glyph index)
TAILS_LS = [("tails l", 0, -1), ("match l", 0, -1), ("l ::", 2, 0)]
ADD_LS = [("acc l", 0, -1), ("match l", 0, -1), ("[l]", 2, 1)]

# ── layout ───────────────────────────────────────────────────────────────────────
ROW_Y = 0.7                    # s1's five-card row: cards at x = -5.3 .. 5.3, y = 0.7
CARD_H = 3.21                  # hero card: header, task, example input, example answer
EX_S, REF_S, EQ_S, CODE_S, VAL_S, TR_S = 40, 30, 44, 40, 30, 34
REF_Y = 3.1                    # tails.2: the example, shrunk to one line at the top
EQ1_Y, EQ2_Y = 0.7, -0.45      # tails.2: the two equations (they land on code lines 1 and 2)
CODE_Y, VAL_Y = 0.35, -1.55    # tails.2: the hero code and its reply
TOP_CODE_Y, TOP_VAL_Y = 2.75, 1.6        # tails.3: code (at 28) and reply moved up
HEAD_Y, STEP_YS, FINAL_Y = 0.85, (0.2, -0.45, -1.1, -1.75), -2.5   # tails.3: the trace
S = 0.9                        # tails.4: cells
ANS_Y, SPINE_Y, CHAIN_Y = 3.2, 0.7, -2.0
COPY_YS = (1.95, 0.8, -0.35)   # tails.4: the tempting picture's three copies
TITLE_Y = 3.2                  # tails.5: "Two tempting mistakes"
X1 = -6.0                      # tails.5: left edge of the first mistake's lines


# ── helpers (local to this scene) ────────────────────────────────────────────────
def gl(code, sub, line=None, nth=0):
    """Glyphs of `sub` as a throwaway group: for flashes, positions and copies only."""
    return VGroup(*code.find(sub, line=line, nth=nth))


def put(piece, full, sub, nth=0):
    """Place a Code piece exactly over `sub` in the laid-out line `full` (same glyphs)."""
    return piece.move_to(gl(full, sub, nth=nth))


def cut(full, subs, size):
    return [put(Code(s, size=size), full, s) for s in subs]


def whole_l(code, marks):
    for sub, line, idx in marks:
        code.find(sub, line=line)[idx].set_color(YELLOW)
    return code


def morph_into(scene, code, moves, fade=(), run_time=2.0):
    """Rebuild `code` out of pieces already on screen. moves = [(src, glyphs of code, whole)]:
    whole=True, the src object itself flies there; False, a copy flies (src fades via `fade`).
    Glyphs nothing flies into fade in. Afterwards the real `code` replaces the flown copies."""
    used, anims, temps = set(), [], []
    for src, glyphs, whole in moves:
        used.update(id(g) for g in glyphs)
        tgt = VGroup(*[g.copy() for g in glyphs])
        temps.append(tgt)
        anims.append(ReplacementTransform(src, tgt) if whole else TransformFromCopy(src, tgt))
    rest = VGroup(*[g.copy() for g in code.text if id(g) not in used])
    temps.append(rest)
    scene.play(*anims, time_span(FadeIn(rest), 0.5 * run_time, run_time),
               *[FadeOut(m) for m in fade], run_time=run_time)
    scene.remove(*temps)
    scene.add(code)


def pointer_spine(n):
    """The answer's outer list: n BLUE cells whose values are pointers (a dot, no number)."""
    spine = ConsChain([0] * n)
    for cell in spine.cells:
        cell.remove(cell.label)
        cell.vdot = Dot(cell.box.get_center(), radius=0.07, color=FG)
        cell.add(cell.vdot)
    return spine


def drop_arrow(cell, target):
    end = (target.box.get_top() if hasattr(target, "box") else target.label.get_top()) + UP * 0.04
    return Arrow(cell.vdot.get_center(), end, buff=0, stroke_width=3, color=TEAL,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16 * S)


def outline_to(cells, color):
    # one animation per part (ch1_s5): a wrapper would lift the opaque boxes over their values
    return [m.animate.set_stroke(color) for c in cells for m in (c.box, c.ptr)]


def padlock(color=FG, h=0.46):
    """ch1_s5's padlock (the "never changes" note)."""
    body = RoundedRectangle(corner_radius=0.06, width=h * 1.15, height=h,
                            stroke_color=color, stroke_width=3, fill_opacity=0)
    shackle = Arc(radius=h * 0.36, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    legs = VGroup(Line(shackle.get_start(), shackle.get_start() + DOWN * 0.05),
                  Line(shackle.get_end(), shackle.get_end() + DOWN * 0.05)).set_stroke(color, 3)
    hole = Dot(body.get_center(), radius=0.045, color=color)
    return VGroup(body, shackle, legs, hole)


class ExerciseTails(NarratedScene):
    def construct(self):
        self.statement()
        self.design()
        self.trace()
        self.memory()
        self.mistakes()
        self.cost()
        hold_for(self, self.last_born, len("but the answer itself is that big"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)   # the last play() never renders its final (empty) frame

    # tails.1: the row of five cards; 3.5 becomes the hero card; the example; pause
    def statement(self):
        bigs = VGroup(*[BigCard(i) for i in range(5)]).arrange(RIGHT, buff=0.25).move_to(UP * ROW_Y)
        card = HeroCard(4, height=CARD_H)
        task = at_row(T("Return the list of all the tails of its argument.", size=34), 1)
        ex_in = at_row(Code(EX_IN, size=EX_S), 2)
        out_full = at_row(Code(EX_OUT, size=EX_S), 3, x=COL_X + 0.6)
        outs = cut(out_full, OUT_PARTS, EX_S)
        card.lower(task, ex_in, *outs)
        tag = pause_tag()

        with self.say("c6.tails.1") as c:
            # "Finally, exercise three point five."  s1's row; 3.5 grows into the hero card.
            self.play(LaggedStart(*[FadeIn(b) for b in bigs], lag_ratio=0.1), run_time=0.8)
            self.wait(0.9)   # the row settles before 3.5 is picked (as in s3, s5)
            big = bigs[4]
            self.play(TransformFromCopy(big.frame, card.frame),
                      FadeTransform(big.num.copy(), card.header),
                      LaggedStart(*[FadeOut(b) for b in bigs], lag_ratio=0.08),
                      time_span(FadeIn(tag, shift=0.2 * DOWN), 0.6, 1.5), run_time=1.5)
            # "Code a function, tails, returning the list of all the tails of its argument."
            c.wait_until("returning")
            self.play(FadeIn(task, shift=0.25 * DOWN), run_time=1.0)
            # "Given the list one, two, three, it should return one, two, three, then two, three,
            #  then three, then nil."  Each tail flies out of the input's suffix.
            c.wait_until("example")
            self.play(FadeIn(ex_in, shift=0.25 * DOWN), run_time=fit(c, "should return", hi=1.0))
            c.wait_until("should return")
            self.play(FadeIn(outs[0], shift=0.2 * RIGHT),
                      TransformFromCopy(gl(ex_in, "[1; 2; 3]"), outs[1]),
                      run_time=fit(c, "then two", 0.85, 0.6, 1.3))
            c.wait_until("then two")
            self.play(TransformFromCopy(gl(ex_in, "2; 3]"), outs[2]), run_time=fit(c, "then three", 0.85, 0.5, 1.0))
            c.wait_until("then three")
            self.play(TransformFromCopy(gl(ex_in, "3]"), outs[3]), run_time=fit(c, "then nil", 0.85, 0.5, 1.0))
            c.wait_until("then nil")
            self.play(FadeIn(outs[4], shift=0.2 * LEFT), run_time=0.8)
            # "Pause here, for the last time."
            c.wait_until("stop")
            self.play(FlashAround(tag, color=YELLOW, time_width=1.5), run_time=1.6)
        self.card, self.ex_in, self.outs, self.ptag = card, ex_in, outs, tag
        self.card_bits = [card.header, task]

    # tails.2: what a tail is; the two cases as equations; they become the code with match
    def design(self):
        card, ex_in, outs = self.card, self.ex_in, self.outs
        ref = Code(REF, size=REF_S).move_to([0, REF_Y, 0])
        ref_frame = RoundedRectangle(corner_radius=0.16, width=ref.width + 0.5, height=0.74)
        ref_frame.set_stroke(DIM, 2).set_fill(CARD_FILL, 1).move_to(ref)
        for piece, sub in [(ex_in, EX_IN), *zip(outs, OUT_PARTS)]:
            piece.generate_target()
            piece.target.scale(REF_S / EX_S).move_to(gl(ref, sub))

        eq2 = Code(EQ2, size=EQ_S).move_to([0, EQ2_Y, 0])
        eq1 = Code(EQ1, size=EQ_S).move_to([0, EQ1_Y, 0]).align_to(eq2, LEFT)
        e1_lhs, e1_arr, e1_ans = cut(eq1, ["tails []", "⇒", "[[]]"], EQ_S)
        e2_lhs, e2_arr, e2_rest = cut(eq2, ["tails l", "⇒", ":: tails xs"], EQ_S)
        e2_l = Code("l", size=EQ_S).move_to(eq2.find("l ::")[0]).set_color(YELLOW)
        e2_lhs.find("tails l")[-1].set_color(YELLOW)
        q = T("?", size=72, color=GOLD).move_to(e1_ans).align_to(e1_ans, LEFT)
        cap = Code("l = x :: xs", size=32).next_to(e2_lhs, DOWN, buff=0.35).align_to(e2_lhs, LEFT)
        cap.find("l")[0].set_color(YELLOW)
        code = whole_l(Code(TAILS, size=CODE_S), TAILS_LS).move_to([0, CODE_Y, 0])
        val = Code(VAL, size=VAL_S).move_to([0, VAL_Y, 0])

        with self.say("c6.tails.2") as c:
            # "Here, a tail means any suffix, from the whole list down to nil."  (on the card)
            def tails_of_answer():
                return [gl(outs[1], "[1; 2; 3]"), gl(outs[2], "[2; 3]"), gl(outs[3], "[3]"), gl(outs[4], "[]")]
            c.wait_until("suffix")
            self.play(LaggedStart(*[FlashUnder(e, color=YELLOW) for e in tails_of_answer()], lag_ratio=0.5),
                      run_time=fit(c, "base", 0.85, 1.5, 3.0))
            # "So what are the tails of nil?"  The card shrinks to one line at the top; the question.
            c.wait_until("base")
            self.play(Transform(card.frame, ref_frame), MoveToTarget(ex_in), *[MoveToTarget(p) for p in outs],
                      *[FadeOut(m) for m in (*self.card_bits, self.ptag)],
                      time_span(FadeIn(e1_lhs, shift=0.25 * DOWN), 0.9, 1.8), time_span(FadeIn(e1_arr), 0.9, 1.8),
                      time_span(FadeIn(q, scale=0.7), 1.1, 1.8), run_time=1.8)
            els = tails_of_answer()
            # "The answer always ends with nil, ..."
            nil_ptr = Arrow(els[3].get_bottom() + DOWN * 0.8, els[3].get_bottom() + DOWN * 0.06, buff=0,
                            stroke_width=4, color=TEAL, max_tip_length_to_length_ratio=0.35, tip_length=0.2)
            c.wait_until("notempty")
            self.play(GrowArrow(nil_ptr), FlashAround(els[3], color=TEAL, time_width=1.5), run_time=1.5)
            # "... so the tails of nil must be a list containing nil."  The ? becomes [[]].
            c.wait_until("list containing nil")
            self.play(TransformFromCopy(els[3], e1_ans), FadeOut(q, scale=0.6), FadeOut(nil_ptr), run_time=1.6)
            # "For a non-empty list, ell, the tails are ell itself, consed onto the tails of exes."
            c.wait_until("step")
            self.play(FadeIn(e2_lhs, shift=0.25 * DOWN), FadeIn(cap, shift=0.2 * UP), run_time=1.2)
            c.wait_until("itself")
            self.play(FadeIn(e2_arr), TransformFromCopy(VGroup(*e2_lhs.find("tails l")[-1:]), e2_l), run_time=1.2)
            c.wait_until("consed onto")
            self.play(FadeIn(e2_rest, shift=0.25 * LEFT), run_time=1.0)
            # "Using match gives us a name, ell, for the whole list."  The equations become the code.
            c.wait_until("match")
            morph_into(self, code, [
                (gl(e1_lhs, "[]"), code.find("[]", line=1), False),
                (e1_arr, code.find("->", line=1), True),
                (e1_ans, code.find("[[]]", line=1), True),
                (e2_lhs, code.find("tails l", line=0), True),
                (e2_arr, code.find("->", line=2), True),
                (e2_l, code.find("l ::", line=2)[:1], True),
                (e2_rest, code.find(":: tails xs", line=2), True),
                (gl(cap, "x :: xs"), code.find("x :: xs", line=2), False),
            ], fade=[e1_lhs, cap], run_time=1.9)
            self.play(FadeIn(val, shift=0.2 * UP),
                      FlashAround(VGroup(code.find("match l", line=0)[-1]), color=YELLOW, time_width=1.5),
                      run_time=max(0.5, min(1.1, c.remaining - 0.05)))
        self.code, self.val = code, val

    # tails.3: the trace on [1; 2; 3]; four tails for three elements
    def trace(self):
        code, val, ex_in = self.code, self.val, self.ex_in
        steps = [Code(s, size=TR_S) for s in TRACE]
        tx = -Code(TRACE[1], size=TR_S).width / 2
        for ln, y in zip(steps, STEP_YS):
            ln.move_to([tx, y, 0], aligned_edge=LEFT)
        head = Code(EX_IN, size=TR_S)
        head.move_to([steps[0].find("[1; 2; 3]")[0].get_left()[0], HEAD_Y, 0], aligned_edge=LEFT)
        final_full = Code("⇒ " + ANSWER, size=TR_S).move_to([tx, FINAL_Y, 0], aligned_edge=LEFT)
        f_arr, f_val = cut(final_full, ["⇒", ANSWER], TR_S)
        nums = [T(str(k + 1), size=30, color=GOLD).next_to(gl(f_val, sub), DOWN, buff=0.14)
                for k, sub in enumerate(["[1; 2; 3]", "[2; 3]", "[3]", "[]"])]
        code.generate_target()
        code.target.scale(0.7).move_to([0, TOP_CODE_Y, 0])
        val.generate_target()
        val.target.scale(28 / VAL_S).move_to([0, TOP_VAL_Y, 0])

        with self.say("c6.tails.3") as c:
            # "On one, two, three,"  the code goes up; the example's input starts the trace
            self.play(MoveToTarget(code), MoveToTarget(val), TransformFromCopy(ex_in, head),
                      *[FadeOut(m) for m in (self.card.frame, ex_in, *self.outs)], run_time=1.2)
            # "the first tail is the whole list, consed onto the tails of two, three."
            c.wait_until("s1")
            self.play(TransformFromCopy(head, steps[0]), run_time=1.6)
            c.wait_until("consed onto")
            self.play(FlashAround(gl(code, "l :: tails xs", line=2), color=YELLOW, time_width=1.5),
                      FlashAround(gl(steps[0], "[1; 2; 3] :: tails [2; 3]"), color=YELLOW, time_width=1.5),
                      run_time=fit(c, "s2", 0.9, 0.8, 1.6))
            # "Then comes two, three,"
            c.wait_until("s2")
            self.play(TransformFromCopy(steps[0], steps[1]), run_time=fit(c, "s3", 0.85, 0.6, 1.2))
            # "then three,"
            c.wait_until("s3")
            self.play(TransformFromCopy(steps[1], steps[2]), run_time=fit(c, "s4", 0.9, 0.5, 0.8))
            # "and finally the tails of nil, the list containing nil."
            c.wait_until("list containing nil")
            self.play(TransformFromCopy(steps[2], steps[3]),
                      FlashAround(gl(code, "[[]]", line=1), color=TEAL, time_width=1.5), run_time=1.0)
            # "Four tails, for three elements."
            c.wait_until("four")
            self.play(TransformFromCopy(gl(steps[3], "⇒"), f_arr),
                      TransformFromCopy(gl(steps[3], "… :: [3] :: [[]]"), f_val), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(n, shift=0.2 * UP) for n in nums], lag_ratio=0.3),
                      run_time=max(0.5, min(1.2, c.remaining - 0.05)))
        self.answer, self.nums = f_val, nums

    # tails.4: memory: not copies, one shared chain plus four new cells
    def memory(self):
        ans, nums = self.answer, self.nums
        k_up, d_up = 36 / TR_S, np.array([0, ANS_Y, 0]) - ans.get_center()
        rise = [ans.animate.scale(k_up).shift(d_up)] + [
            n.animate.move_to(ans.get_center() + d_up + (n.get_center() - ans.get_center()) * k_up) for n in nums]
        spine = pointer_spine(4).scale(S)
        spine.shift(RIGHT * (0 - spine.get_x()) + UP * (SPINE_Y - spine.cells[0].get_y()))
        chain = ConsChain([1, 2, 3]).scale(S)
        chain.shift(RIGHT * (spine.cells[0].get_x() - chain.cells[0].get_x())
                    + UP * (CHAIN_Y - chain.cells[0].get_y()))
        drops = [drop_arrow(cell, tgt) for cell, tgt in zip(spine.cells, [*chain.cells, chain.nil])]

        copies, srcs = [], []
        for k in range(3):
            cp = ConsChain([1, 2, 3][k:]).scale(S)
            cp.shift(RIGHT * (chain.cells[k].get_x() - cp.cells[0].get_x())
                     + UP * (COPY_YS[k] - cp.cells[0].get_y()))
            copies.append(cp)
            srcs.append(VGroup(*chain.cells[k:], *chain.arrows[k:], chain.nil))
        copied = T("copied: 6", size=36, color=GOLD)
        copied.move_to([chain.cells[2].get_left()[0] - 0.5, COPY_YS[2], 0], aligned_edge=RIGHT)
        cross = Cross(VGroup(*copies, copied), stroke_color=RED, stroke_width=6)

        shared_box = SurroundingRectangle(chain, color=TEAL, buff=0.2, corner_radius=0.1)
        shared_lab = T("shared", size=36, color=TEAL)
        shared_lab.next_to(shared_box, RIGHT, buff=0.35).align_to(shared_box, UP).shift(DOWN * 0.08)
        note = VGroup(padlock(), T("never changes", size=32)).arrange(RIGHT, buff=0.25)
        note.next_to(shared_lab, DOWN, buff=0.35, aligned_edge=LEFT)
        newc = T("new cells: 4", size=36, color=GOLD).move_to([0, (ANS_Y + SPINE_Y) / 2 + 0.1, 0])

        with self.say("c6.tails.4") as c:
            # "Now look at it in memory."  The trace and its count stay up for this line.
            # "The answer seems to hold six numbers."  The answer goes up (its count riding
            # with it); the list it was made from appears; the six numbers flash.
            c.wait_until("looks")
            kept = {id(m) for m in (ans, *nums)}     # the trace clears first, so the answer
            self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects) if id(m) not in kept],
                                  lag_ratio=0.05), run_time=0.6)   # rises through an empty frame
            self.play(*rise, time_span(FadeIn(chain, shift=0.3 * UP), 0.3, 1.2), run_time=1.2)
            digits = [ans.find(d, nth=n)[0] for d, n in (("1", 0), ("2", 0), ("3", 0), ("2", 1), ("3", 1), ("3", 2))]
            rt = fit(c, "ask", 0.95, 1.3, 2.0)
            self.play(LaggedStart(*[FlashAround(d, color=GOLD, buff=0.08) for d in digits], lag_ratio=0.25),
                      *[time_span(FadeOut(n), 0.6 * rt, rt) for n in nums], run_time=rt)
            # "So does it copy the list, again and again?"  The tempting picture: three copies.
            c.wait_until("ask")
            self.play(LaggedStart(*[TransformFromCopy(s, cp) for s, cp in zip(srcs, copies)], lag_ratio=0.35),
                      time_span(FadeIn(copied, shift=0.2 * UP), 1.4, 2.2), run_time=2.2)
            # "No."
            c.wait_until("share")
            self.play(Create(cross), run_time=0.7)
            # "Each tail is the original list, from some cell onwards, so the answer points into
            #  the same chain."
            c.wait_until("original list")
            self.play(*[FadeOut(m) for m in (*copies, copied, cross)],
                      time_span(FadeIn(spine, shift=0.2 * DOWN, lag_ratio=0.1), 0.4, 1.6), run_time=1.6)
            c.wait_until("some cell")
            self.play(LaggedStart(*[GrowArrow(a) for a in drops], lag_ratio=0.3),
                      run_time=fit(c, "same chain", 0.85, 1.2, 2.2))
            c.wait_until("same chain")
            self.play(*outline_to(chain.cells, TEAL), Create(shared_box),
                      FadeIn(shared_lab, shift=0.2 * LEFT), run_time=1.3)
            # "The only new cells are the four in the outer list."
            c.wait_until("spine")
            self.play(LaggedStart(*[FlashAround(cell, color=GOLD, buff=0.1) for cell in spine.cells], lag_ratio=0.25),
                      time_span(FadeIn(newc, shift=0.2 * DOWN), 0.6, 1.4), run_time=1.8)
            # "As we saw in chapter one, that sharing is safe because lists never change."
            c.wait_until("immut")
            self.play(FadeIn(note, shift=0.25 * UP), run_time=1.2)

    # tails.5: two tempting mistakes
    def mistakes(self):
        title = VGroup(cross_mark(), T("Two tempting mistakes", size=40)).arrange(RIGHT, buff=0.3)
        title.move_to([0, TITLE_Y, 0])
        w1 = whole_l(Code(WRONG1, size=36), TAILS_LS).move_to([X1, 1.2, 0], aligned_edge=LEFT)
        bad = w1.find("-> []", line=1)[2:]
        val1 = Code(VAL, size=30).move_to([X1, -0.4, 0], aligned_edge=LEFT)
        ok1 = check_mark().next_to(val1, RIGHT, buff=0.35)
        call1 = Code(EX_IN, size=30).move_to([X1, -1.5, 0], aligned_edge=LEFT)
        rep1 = Code(REPLY1, size=30).move_to([X1, -2.15, 0], aligned_edge=LEFT)
        bracket_y = rep1.find("]")[0].get_y()
        gap = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=0.95, height=0.5), num_dashes=16)
        gap.set_stroke(RED, 2.5).next_to(rep1, RIGHT, buff=0.12).set_y(bracket_y)
        ghost = Code("[]", size=30).set_color(RED).set_opacity(0.45).move_to(gap)
        close = Code("]", size=30).next_to(gap, RIGHT, buff=0.12).set_y(bracket_y)

        w2 = whole_l(Code(ADDTAILS, size=34), ADD_LS).move_to([0, 1.1, 0])
        box = token_box(w2.find("acc @ [l]", line=2), VGroup(*w2.line(2)))
        call2 = VGroup(Code("addtails [] [1; 2; 3]", size=32), check_mark(),
                       T("right answer", size=30, color=GREEN)).arrange(RIGHT, buff=0.3).move_to([0, -0.45, 0])
        ats = [w2.find("@", nth=0)[0], w2.find("@", nth=1)[0]]
        terms = MathTex("1", "+", "2", "+", "3", "+", "\\cdots", "+", "n", font_size=52).set_color(GOLD)
        big_o = MathTex("=", "O(n^2)", font_size=52)
        big_o[1].set_color(GOLD)
        like = VGroup(T("like", size=32, color=DIM), Code("nrev", size=34).set_opacity(0.45)).arrange(RIGHT, buff=0.2)
        VGroup(terms, big_o).arrange(RIGHT, buff=0.3)
        like.next_to(big_o, RIGHT, buff=0.7)
        VGroup(terms, big_o, like).move_to([0, -1.85, 0])

        with self.say("c6.tails.5") as c:
            # "There are two tempting mistakes."
            c.wait_until("tempting")
            sweep_clear(self, time_span(FadeIn(title, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)
            # "First, making the tails of nil just nil."
            c.wait_until("nilbase")
            self.play(FadeIn(w1, shift=0.25 * UP), run_time=1.0)
            c.wait_until("just nil")
            self.play(FlashAround(VGroup(*bad), color=RED, time_width=1.5), *recolor(bad, RED), run_time=1.2)
            # "The type is the same, so OCaml can't help, but the empty tail goes missing."
            c.wait_until("type is the same")
            self.play(FadeIn(val1, shift=0.2 * UP), time_span(Create(ok1), 0.5, 1.1), run_time=1.1)
            c.wait_until("so ocaml")
            self.play(FadeIn(call1, shift=0.2 * UP), FadeIn(rep1, shift=0.2 * UP), FadeIn(close, shift=0.2 * UP),
                      run_time=1.0)
            c.wait_until("goes missing")
            self.play(Create(gap), FadeIn(ghost, scale=0.8), run_time=fit(c, "append", 0.8, 0.6, 1.0))
            # "Second, using append to add each tail on the end of an accumulator."
            c.wait_until("append")
            # The first mistake's evidence (same type, missing []) stays through this sentence,
            # moved down and dimmed so it doesn't read as addtails's reply.
            # The first mistake's code waits, dimmed, until addtails takes its place.
            w1_rest = [val1, ok1, call1, rep1, gap, close]
            self.play(*[restyle(m, op=0.55, shift=DOWN * 0.9) for m in w1_rest],
                      restyle(ghost, op=0.3, shift=DOWN * 0.9), restyle(w1, op=0.55), run_time=1.0)
            c.wait_until("each tail")
            self.play(FadeOut(w1), time_span(FadeIn(w2, shift=0.25 * UP), 0.3, 1.2), run_time=1.2)
            c.wait_until("on the end")
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("accumulator")
            self.play(FadeIn(call2, shift=0.2 * UP), run_time=fit(c, "each append", 0.85, 0.5, 0.9))
            # "Each append copies the accumulator, so that's one, plus two, plus three, and so on,
            #  which is big O of en squared, just like en-rev."
            c.wait_until("each append")
            self.play(*[FlashAround(a, color=RED, buff=0.08) for a in ats], *recolor(ats, RED),
                      *[FadeOut(m) for m in (val1, ok1, call1, rep1, gap, ghost, close)], run_time=1.2)
            c.wait_until("one plus two")
            self.play(LaggedStart(*[FadeIn(t, shift=0.2 * UP) for t in terms], lag_ratio=0.35),
                      run_time=fit(c, "big o", 0.85, 1.5, 3.0))
            settle(self, terms)
            c.wait_until("big o")
            self.play(FadeIn(big_o, shift=0.2 * LEFT), time_span(FadeIn(like, shift=0.2 * LEFT), 0.6, 1.4),
                      run_time=1.4)
        self.quadratic = [terms, big_o, like]

    # tails.6: the cost
    def cost(self):
        code = whole_l(Code(TAILS, size=36), TAILS_LS).move_to([0, 1.95, 0])
        lx, mx, ox = -5.6, -3.4, 4.6
        rows_y = (-0.15, -1.25, -2.55)
        lab_t = T("time", size=36, color=DIM).move_to([lx, rows_y[0], 0], aligned_edge=LEFT)
        calls = T("n + 1 calls", size=36, t2c={"n + 1": GOLD}).move_to([mx, rows_y[0], 0], aligned_edge=LEFT)
        o_t = MathTex("O(n)", font_size=56, color=GOLD).move_to([ox, rows_y[0], 0])
        lab_s = T("space", size=36, color=DIM).move_to([lx, rows_y[1], 0], aligned_edge=LEFT)
        per = T("a new cell per tail", size=36).move_to([mx, rows_y[1], 0], aligned_edge=LEFT)
        o_s = MathTex("O(n)", font_size=56, color=GOLD).move_to([ox, rows_y[1], 0])
        p1 = T("not iterative,", size=34, color=DIM).move_to([lx, rows_y[2], 0], aligned_edge=LEFT)
        p2 = T("but the answer itself is that big", size=34)
        p2.next_to(p1, RIGHT, buff=0.22).align_to(p1, DOWN)

        with self.say("c6.tails.6") as c:
            # "It makes a call per element, plus a call for nil, so it takes big O of en time."
            # addtails's O(n^2) row stays for this sentence, under tails's O(n)
            sweep_clear(self, time_span(FadeIn(code, shift=0.25 * DOWN), 0.5, 1.3),
                        keep=self.quadratic, run_time=1.3)
            c.wait_until("call per element")
            self.play(FadeIn(lab_t, shift=0.2 * RIGHT),
                      FlashAround(gl(code, "tails xs", line=2), color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("call for nil")
            self.play(FadeIn(calls, shift=0.2 * RIGHT),
                      FlashAround(gl(code, "| [] -> [[]]", line=1), color=TEAL, time_width=1.5), run_time=1.1)
            c.wait_until("en time")
            self.play(FadeIn(o_t, scale=0.8), run_time=0.9)
            # "It builds a new cell per tail, so its space is big O of en too."
            c.wait_until("space")
            self.play(FadeIn(lab_s, shift=0.2 * RIGHT), *[FadeOut(m) for m in self.quadratic],
                      FlashAround(gl(code, "l ::", line=2), color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("new cell per tail")
            self.play(FadeIn(per, shift=0.2 * RIGHT), run_time=1.0)
            c.wait_until("space is")
            self.play(FadeIn(o_s, scale=0.8), run_time=0.9)
            # "It isn't iterative, but there's nothing to gain, since the answer itself is that big."
            c.wait_until("close")
            self.play(FadeIn(p1, shift=0.2 * UP), run_time=1.0)
            c.wait_until("nothing to gain")
            self.play(FadeIn(p2, shift=0.2 * UP), run_time=1.0)
            self.last_born = self.time
