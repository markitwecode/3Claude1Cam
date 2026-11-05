"""Chapter 7, scene 3: Exercise 4.2 solved, two lists by sign. Clips c7.signs.1 – c7.signs.6.

Plan
- signs.1: ch6's strip fades in (4.1 done, 4.2 current); card 4.2 grows out of its pill: ch6's task
  text, the example input, the GREEN target type in ch6's Slot; on {halves} two empty BLUE boxes
  ("≥ 0", "< 0") where the output goes, filled number by number from the input; then the
  boxes give way to the pair. Pause tag top right, held; the card shrinks back at signs.2's start.
- signs.2: ch3's unzip (unzip_code from ch3_s5, its let line YELLOW) big, then small and dim at
  lower right; bysign built line by line at top left: the [] clause flies out of unzip's, the
  let line is morphed from unzip's; one YELLOW box slides [] clause -> x::xs -> let -> the test.
  {type}: unzip goes, OCaml's reply under the code.
- signs.3: the reply rises to a header; a GOLD ConsChain at the bottom; ch3-style ladder (calls
  left, DIM "waiting" right, each row born from the one above; chain cells dim as calls peel
  them); ([], []) TEAL; on the way up each number flies from its call to its side; the header
  reply becomes the toplevel answer, a box slides over the two lists.
- signs.4: the code returns (centred), the answer under it; >= YELLOW; a ghost line with > (RED)
  is born from the test; in the answer the 0 hops to the negatives (RED), then back (GREEN).
- signs.5: slow, RED-boxed, its four (slow xs) YELLOW; same answer + GREEN tick; the call becomes
  the root of a doubling call tree (per-level counts GOLD); counters for 20 elements.
- signs.6: revBysign at the top, ch3's revUnzip (ch3_s8's colours) dim at lower right; one
  accumulator box copied from ps, ns to xs, ys; then revUnzip gives way to the reply (wrapped),
  the call and its reversed answer (both lists YELLOW); the input reverses in place and the
  answer comes out in order; time / space O(n) in GOLD. Everything (strip too) fades to empty.

STATUS: built; check clean apart from dwell notes: ladder "waiting" tags (replaced as the calls
return, as in ch3), the unzip/revUnzip/slow callbacks (the narration moves on), the 20-element
counters (~4.9 s on screen; they fade during signs.6's sweep).

Departures: bysign's `if` line is wrapped after `then (x::ps, ns)` (one line is 50 characters:
13+ units at a readable size); slow's long `if` is wrapped keyword-first (`if x >= 0` / `then ...` /
`else ...`); revBysign's reply wrapped after "->" as ch3_s8 wraps revUnzip's.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch6_s5_hints1 import (CURRENT, DONE, EX42_INPUT, EX42_RESULT, EX42_TYPE, EX_TASKS,  # noqa: E402
                                  TODO, HeroCard, Slot, enter_card, first_cue, fit,
                                  hold_for, make_strip, pause_tag, split_line)
from scenes.ch3_s5_unzip import unzip_code  # noqa: E402  ch3's In [65], its colours
from scenes.ch3_s8_revunzip import C as rev_colours, REV as REVUNZIP_SRC  # noqa: E402

# ── code (verbatim from the brief; wraps noted in the docstring) ─────────────────
BYSIGN_SRC = ("let rec bysign = function\n"
              "  | [] -> ([], [])\n"
              "  | x::xs ->\n"
              "      let (ps, ns) = bysign xs in\n"
              "      if x >= 0 then (x::ps, ns)\n"
              "      else (ps, x::ns)")
BYSIGN_TYPE = "val bysign : int list -> int list * int list = <fun>"
ANSWER = "- : int list * int list = ([3; 0; 2], [-1; -5])"
WRONG = "- : int list * int list = ([3; 2], [-1; 0; -5])"
GHOST_SRC = "if x > 0 then (x::ps, ns)"
SLOW_SRC = ("let rec slow = function\n"
            "  | [] -> ([], [])\n"
            "  | x::xs ->\n"
            "      if x >= 0\n"
            "      then (x :: fst (slow xs), snd (slow xs))\n"
            "      else (fst (slow xs), x :: snd (slow xs))")
SLOW_TYPE = "val slow : int list -> int list * int list = <fun>"
SLOW_CALL = "slow [3; -1; 0; -5; 2]"
REVB_SRC = ("let rec revBysign = function\n"
            "  | ([], ps, ns) -> (ps, ns)\n"
            "  | (x::xs, ps, ns) ->\n"
            "      if x >= 0 then revBysign (xs, x::ps, ns)\n"
            "      else revBysign (xs, ps, x::ns)")
REVB_TYPE = ("val revBysign : int list * int list * int list ->\n"
             "  int list * int list = <fun>")
REV_CALL = "revBysign ([3; -1; 0; -5; 2], [], [])"
REV_ANSWER = "- : int list * int list = ([2; 0; 3], [-5; -1])"
FIX_CALL = "revBysign ([2; -5; 0; -1; 3], [], [])"

VALUES = [3, -1, 0, -5, 2]
CALLS = ["bysign [3; -1; 0; -5; 2]", "bysign [-1; 0; -5; 2]", "bysign [0; -5; 2]",
         "bysign [-5; 2]", "bysign [2]", "bysign []"]
RESULTS = ["([3; 0; 2], [-1; -5])", "([0; 2], [-1; -5])", "([0; 2], [-5])",
           "([2], [-5])", "([2], [])", "([], [])"]
TAILS = ["-1; 0; -5; 2]", "0; -5; 2]", "-5; 2]", "2]", "]"]      # what call k hands to call k+1
HEADS = ["3", "-1", "0", "-5", "2"]                                  # call k's head
UP_FLIGHTS = {   # result k <- pieces of result k+1, and call k's head
    4: [("([", "(["), ("], [])", "], [])")],
    3: [("([2], [", "([2], ["), ("])", "])")],
    2: [("([", "(["), ("2], [-5])", "2], [-5])")],
    1: [("([0; 2], [", "([0; 2], ["), ("-5])", "-5])")],
    0: [("([", "(["), ("0; 2], [-1; -5])", "0; 2], [-1; -5])")],
}
LET_PAIRS = [("let", "let"), ("xs, ys", "(ps, ns)"), ("=", "="), ("unzip pairs", "bysign xs"),
             ("in", "in")]
GHOST_PAIRS = [("if x", "if x"), (">=", ">"), ("0 then (x::ps, ns)", "0 then (x::ps, ns)")]

# ── layout ──────────────────────────────────────────────────────────────────────
STEP = 0.66                      # card row pitch (ch6's 4.2 card)
CARD_H = 4.3
UZ_DIM = 0.55                    # a dimmed callback (ch3 code)
CODE_SIZE = 34
CODE_TOP = 2.75                  # bysign, centred under the strip (signs.2 and signs.4)
UZ_UR = (6.5, -0.75)             # signs.2: unzip, small, lower right
LAD = 30                         # ladder text size
ROWS = [1.7, 1.06, 0.42, -0.22, -0.86, -1.5]
CALL_X, RES_X = -6.3, 6.3
HEAD_Y = 2.42                    # the header reply over the ladder
CHAIN_Y, CHAIN_SCALE, CELL_DIM = -2.6, 0.8, 0.3
GHOST_OP = 0.6
TREE_W, TREE_TOP, TREE_DY, COUNT_X = 9.6, 1.95, 0.6, 5.75


# ── helpers (one animation per glyph: never wrap on-screen parts) ─────────────────
def G(code):
    return list(code.text.submobjects)


def ids(glyphs):
    return {id(g) for g in glyphs}


def parts_of(mob):
    return list(mob.submobjects) or [mob]


def morph(src, dst):
    """Each target glyph is born from the proportionally placed source glyph."""
    src, dst = list(src), list(dst)
    n, m = len(src), len(dst)
    return [TransformFromCopy(src[min(n - 1, i * n // m)], d) for i, d in enumerate(dst)]


def build(dst, flights):
    """flights: (source glyphs, dst substring[, nth]); the rest of dst fades in."""
    anims, used = [], set()
    for src, sub, *nth in flights:
        d = list(dst.find(sub, nth=nth[0] if nth else 0))
        anims += morph(src, d)
        used |= ids(d)
    return anims + [FadeIn(g) for g in G(dst) if id(g) not in used]


def morph_line(src, sline, dst, dline, pairs):
    anims = []
    for s, d in pairs:
        anims += morph(src.find(s, line=sline), dst.find(d, line=dline))
    return anims


def left_at(mob, x, y):
    return mob.shift([x - mob.get_left()[0], y - mob.get_center()[1], 0])


def right_at(mob, x, y):
    return mob.shift([x - mob.get_right()[0], y - mob.get_center()[1], 0])


def half_box(mob, color=BLUE):
    r = RoundedRectangle(corner_radius=0.12, width=mob.width + 0.34, height=0.6)
    return r.set_stroke(color, 2.5).set_fill(color, 0.08).move_to(mob)


def bysign_code(size=CODE_SIZE):
    code = Code(BYSIGN_SRC, size=size)
    code.find("bysign", line=3).set_color(YELLOW)     # the recursive call, as ch3 colours unzip's
    return code


def revbysign_code(size):
    code = Code(REVB_SRC, size=size)
    for k in range(3):
        code.find("revBysign", nth=k).set_color(YELLOW)   # ch3_s8: every function name YELLOW
    return code


def shuffle(code, target, mover, color, arc):
    """Move code's glyphs onto target's layout: `mover` (a substring present in both) hops
    along an arc and takes `color`; the other glyphs slide in order."""
    sm, tm = list(code.find(mover)), list(target.find(mover))
    s_rest = [g for g in G(code) if id(g) not in ids(sm)]
    t_rest = [g for g in G(target) if id(g) not in ids(tm)]
    anims = [a.animate.move_to(b) for a, b in zip(s_rest, t_rest)
             if np.linalg.norm(a.get_center() - b.get_center()) > 1e-3]
    for i, (a, b) in enumerate(zip(sm, tm)):
        t = a.copy().move_to(b)
        if i == 0:
            t.set_color(color)
        anims.append(Transform(a, t, path_arc=arc))
    return anims


def reorder(code, target, tokens, arc=-0.6 * PI):
    """Each token's glyphs travel to the same token in `target` (laid over `code`), taking its
    colour; every other glyph takes target's colour in place."""
    anims, moved = [], set()
    for tok in tokens:
        for a, b in zip(code.find(tok), target.find(tok)):
            anims.append(Transform(a, b.copy(), path_arc=arc))
            moved.add(id(a))
    for a, b in zip(G(code), G(target)):
        if id(a) not in moved and not np.allclose(color_to_rgb(a.get_color()), color_to_rgb(b.get_color())):
            anims.append(a.animate.set_color(b.get_color()))
    return anims


class SplitBySign(NarratedScene):
    def construct(self):
        self.clip_card()
        self.clip_code()
        self.clip_trace()
        self.clip_zero()
        self.clip_slow()
        self.clip_rev()
        hold_for(self, self.cost_born, len("space O(n)"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── 1: the card; two halves; pause ─────────────────────────────────────────
    def clip_card(self):
        strip = self.strip = make_strip([DONE, CURRENT] + [TODO] * 4)
        card = HeroCard(1, height=CARD_H, step=STEP)
        task = EX_TASKS[1]
        k = task.index("and the")
        t1 = card.at_row(T(task[:k].rstrip(), size=34), 1)
        t2 = card.at_row(T(task[k:], size=34), 2)
        slot = card.at_row(Slot(EX42_TYPE, size=30), 3)
        lft_src, rgt_src = "[3; 0; 2]", "[-1; -5]"
        ex_in, arrow, lp, lft, comma, rgt, rp = split_line(
            f"{EX42_INPUT}  ⇒  {EX42_RESULT}", [EX42_INPUT, "⇒", "(", lft_src, ",", rgt_src, ")"],
            size=34, y=card.row_y(4) - 0.15)
        box_l, box_r = half_box(lft), half_box(rgt)
        lab_l = MathTex(r"\geq 0", font_size=44, color=BLUE).next_to(box_l, DOWN, buff=0.14)
        lab_r = MathTex(r"< 0", font_size=44, color=BLUE).next_to(box_r, DOWN, buff=0.14)
        card.lower(t1, t2, slot, ex_in, arrow, lp, lft, comma, rgt, rp, box_l, box_r, lab_l, lab_r)
        tag = pause_tag()

        with self.say("c7.signs.1") as c:
            # "Exercise four point two."
            self.play(FadeIn(strip, shift=0.15 * DOWN, lag_ratio=0.1), run_time=0.8)
            self.play(*enter_card(strip, card, light=False), time_span(FadeIn(tag, shift=0.2 * LEFT), 0.4, 1.0),
                      run_time=1.0)
            # "Code a function that takes a list of integers, and returns two lists."
            c.wait_until("code a function")
            self.play(LaggedStart(FadeIn(t1, shift=0.25 * DOWN), FadeIn(t2, shift=0.25 * DOWN),
                                  lag_ratio=0.4), run_time=fit(c, "list of integers", hi=1.3))
            c.wait_until("list of integers")
            self.play(FadeIn(ex_in, shift=0.2 * DOWN), FadeIn(arrow, shift=0.2 * RIGHT),
                      run_time=fit(c, "two lists", hi=1.0))
            c.wait_until("two lists")
            self.play(FadeIn(slot.box), FadeIn(slot.q, scale=0.7), FadeIn(slot.sig, shift=0.2 * DOWN),
                      run_time=fit(c, "halves", hi=1.0))
            # "The first holds the numbers that are zero or more, the non-negative ones."
            c.wait_until("halves")
            self.play(Create(box_l), Create(box_r), FadeIn(lab_l, shift=0.2 * DOWN),
                      FadeIn(lab_r, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until(first_cue(c, "non-negative", "zero or more"))
            self.play(*build(lft, [(ex_in.find(h), h) for h in ("3", "0", "2")]), run_time=1.5)
            self.add(lft)
            # "The second holds the negative ones."  Then the boxes give way to the pair.
            c.wait_until("the second")
            self.play(*build(rgt, [(ex_in.find(h), h) for h in ("-1", "-5")]),
                      time_span(FadeOut(box_l), 1.1, 1.8), time_span(FadeOut(box_r), 1.1, 1.8),
                      *[time_span(FadeIn(m), 1.1, 1.8) for m in (lp, comma, rp)], run_time=1.8)
            self.add(rgt)
            # "Pause, and have a go."
            c.wait_until("stop")
            self.play(FlashAround(tag, color=YELLOW, time_width=1.5, buff=0.12), run_time=1.5)
        card.keep(t1, t2, slot.box, slot.q, slot.sig, ex_in, arrow, lp, lft, comma, rgt, rp, lab_l, lab_r)
        self.card, self.tag = card, tag

    # ── 2: the shape of unzip; bysign line by line; its type ──────────────────────
    def clip_code(self):
        strip, card = self.strip, self.card
        uz = unzip_code(36).move_to([0, -0.25, 0])
        for g in uz.line(3):
            g.set_color(YELLOW)
        uz_small = unzip_code(28)
        for g in G(uz_small):
            g.set_opacity(UZ_DIM)
        for g in uz_small.line(3):
            g.set_color(YELLOW).set_opacity(1)
        uz_small.move_to([*UZ_UR, 0], aligned_edge=UR)
        code = bysign_code().move_to([0, CODE_TOP, 0], aligned_edge=UP)

        def box_on(sub, line):
            return token_box(code.find(sub, line=line), code.line(line))

        reply = Code(BYSIGN_TYPE, size=28).move_to([0, code.get_bottom()[1] - 0.6, 0])

        with self.say("c7.signs.2") as c:
            # "Two results at once is the shape of unzip, from chapter three."
            # the card goes home as ch7_s2's does: contents and tag fade, the frame shrinks onto
            # pill 4.2 as it already looks (CURRENT, for the whole solution)
            self.play(*[FadeOut(m) for m in (*card.shown, self.tag)],
                      Transform(card.frame, strip[card.i].frame.copy()), run_time=1.0)
            self.remove(card.frame)
            c.wait_until("shape of unzip")
            self.play(FadeIn(uz, shift=0.25 * UP),
                      time_span(FlashAround(VGroup(*uz.line(3)), color=YELLOW, time_width=1.5), 0.8, 2.0),
                      run_time=2.0)
            # "Let's call it by-sign."
            c.wait_until("base")
            self.play(Transform(uz, uz_small), *[FadeIn(g, shift=0.2 * DOWN) for g in code.line(0)],
                      run_time=1.3)
            # "On nil, it gives back two empty lists."
            c.wait_until("on nil")
            box = box_on("[] -> ([], [])", 1)
            self.play(*morph(uz.line(1), code.line(1)), time_span(FadeIn(box), 1.0, 1.6), run_time=1.6)
            # "Otherwise, split the tail first, and use a let to name the two halves of its answer."
            c.wait_until("otherwise")
            self.play(*[FadeIn(g, shift=0.2 * DOWN) for g in code.line(2)],
                      Transform(box, box_on("x::xs", 2)), run_time=1.1)
            c.wait_until("use a let")
            self.play(*morph_line(uz, 3, code, 3, LET_PAIRS),
                      Transform(box, token_box(code.line(3), code.line(3))), run_time=1.7)
            # "Then put ex on the front of whichever half it belongs to."
            c.wait_until("decide")
            self.play(FadeOut(uz, shift=0.2 * DOWN),
                      *[time_span(FadeIn(g, shift=0.2 * DOWN), 0.4, 1.4) for g in (*code.line(4), *code.line(5))],
                      Transform(box, box_on("if x >= 0", 4)), run_time=1.4)
            self.add(code)
            # "The type is int list to int list times int list."
            c.wait_until("type")
            self.play(FadeOut(box), FadeIn(reply, shift=0.2 * DOWN), run_time=1.2)
        self.code, self.reply = code, reply

    # ── 3: down to nil and back up ───────────────────────────────────────────────
    def clip_trace(self):
        code, reply = self.code, self.reply
        chain = ConsChain(VALUES).scale(CHAIN_SCALE).move_to([0, CHAIN_Y, 0])
        for cell in chain.cells:
            cell.label.set_color(GOLD)
        pieces = []
        for i, cell in enumerate(chain.cells):
            pieces += [cell, chain.arrows[i]]
        pieces.append(chain.nil)
        calls = [left_at(Code(s, size=LAD), CALL_X, y) for s, y in zip(CALLS, ROWS)]
        res = [right_at(Code(s, size=LAD), RES_X, y) for s, y in zip(RESULTS, ROWS)]
        res[5].set_color(TEAL)
        waits = [right_at(T("waiting", size=30, color=DIM), RES_X, y) for y in ROWS[:5]]
        answer = Code(ANSWER, size=30).move_to([0, HEAD_Y, 0])

        with self.say("c7.signs.3") as c:
            # "On three, minus one, zero, minus five, two,"
            rt = min(2.6, max(1.6, c.until("down") - 1.1))
            self.play(FadeOut(code), reply.animate.move_to([0, HEAD_Y, 0]),
                      LaggedStart(*[FadeIn(p, shift=0.15 * DOWN) for p in pieces], lag_ratio=0.35),
                      run_time=rt)
            settle(self, chain)
            row0 = [(parts_of(chain.cells[i].label), h) for i, h in enumerate(HEADS)]
            self.play(*build(calls[0], row0), run_time=min(1.0, max(0.6, c.until("down") - 0.05)))
            self.add(calls[0])
            for cell in (*chain.cells, *chain.arrows):
                cell.save_state()
            # "the calls go down to nil, which gives two empty lists."
            c.wait_until("down")
            for k, rt in enumerate((0.8, 0.6, 0.5, 0.45, 0.45)):
                nxt = calls[k + 1]
                self.play(*build(nxt, [(calls[k].find("bysign ["), "bysign ["), (calls[k].find(TAILS[k]), TAILS[k])]),
                          FadeIn(waits[k], shift=0.2 * DOWN),
                          restyle(chain.cells[k], op=CELL_DIM), restyle(chain.arrows[k], op=CELL_DIM),
                          run_time=rt)
                self.add(nxt)
            c.wait_until("two empty lists")
            base = res[5]
            self.play(*build(base, [(calls[5].find("[]"), "[]"), (calls[5].find("[]"), "[]", 1)]),
                      run_time=0.8)
            self.add(base)
            # "Then, on the way back, each number joins its side."
            c.wait_until("up")
            for k, rt in zip((4, 3, 2, 1, 0), (1.0, 0.8, 0.65, 0.55, 0.55)):
                below = res[k + 1]
                flights = [(below.find(s), d) for s, d in UP_FLIGHTS[k]] + [(calls[k].find(HEADS[k]), HEADS[k])]
                self.play(*build(res[k], flights), FadeOut(waits[k]),
                          Restore(chain.cells[k]), Restore(chain.arrows[k]), run_time=rt)
                self.add(res[k])
            # "The answer is three, zero, two, and minus one, minus five, in their original order."
            c.wait_until("result")
            flights = [(G(res[0]), RESULTS[0]),
                       (reply.find("int list * int list"), "int list * int list"),
                       (reply.find("="), "=")]
            self.play(FadeOut(reply), *build(answer, flights), run_time=1.5)
            self.add(answer)
            c.wait_until("three, zero, two")
            box = token_box(answer.find("[3; 0; 2]"), answer)
            self.play(FadeIn(box), run_time=0.7)
            c.wait_until("minus one, minus five")
            self.play(Transform(box, token_box(answer.find("[-1; -5]"), answer)), run_time=0.8)
        self.answer = answer

    # ── 4: the test, and what > would do ─────────────────────────────────────────
    def clip_zero(self):
        answer = self.answer
        code = bysign_code().move_to([0, CODE_TOP, 0], aligned_edge=UP)
        line4 = list(code.line(4))
        ge = code.find(">=", line=4)
        r_y = code.get_bottom()[1] - 0.62
        ghost = Code(GHOST_SRC, size=CODE_SIZE)
        left_at(ghost, line4[0].get_left()[0], r_y)
        for g in G(ghost):
            g.set_opacity(GHOST_OP)
        for g in ghost.find(">"):
            g.set_color(RED).set_opacity(1)
        w_y = r_y - 0.92
        wrong = Code(WRONG, size=30).move_to([0, w_y, 0])
        others = [g for g in G(code) if id(g) not in ids(line4)]

        with self.say("c7.signs.4") as c:
            # "Watch the test."
            sweep_clear(self, answer.animate.move_to([0, r_y, 0]),
                        time_span(FadeIn(code, shift=0.2 * DOWN), 0.9, 1.7),
                        keep=[self.strip, answer], run_time=1.7)
            # "It says ex is greater than or equal to zero."
            c.wait_until("greater than or equal")
            self.play(*recolor(ge, YELLOW), FlashAround(VGroup(*ge), color=YELLOW, time_width=1.5, buff=0.1),
                      run_time=1.5)
            # "Write greater than zero instead, and zero lands with the negatives."
            c.wait_until("pitfall")
            self.play(*morph_line(code, 4, ghost, None, GHOST_PAIRS),
                      *[g.animate.set_opacity(0.35) for g in others],
                      answer.animate.move_to([0, w_y, 0]), run_time=1.6)
            self.add(ghost)
            right_place = answer.copy()
            c.wait_until("lands with")
            self.play(*shuffle(answer, wrong, "0;", RED, -0.7 * PI), run_time=1.5)
            # "But zero belongs in the first list."
            c.wait_until("but zero belongs")
            self.play(*shuffle(answer, right_place, "0;", GREEN, 0.7 * PI),
                      *[g.animate.set_opacity(0.3) for g in G(ghost)],
                      *[g.animate.set_opacity(1) for g in others], run_time=1.5)

    # ── 5: calling twice ───────────────────────────────────────────────────────
    def clip_slow(self):
        slow = Code(SLOW_SRC, size=30).move_to([0, 2.7, 0], aligned_edge=UP)
        twice = [slow.find("slow xs", nth=k) for k in range(4)]
        frame = SurroundingRectangle(slow, buff=0.2, corner_radius=0.12).set_stroke(RED, 3)
        stype = Code(SLOW_TYPE, size=28).move_to([0, frame.get_bottom()[1] - 0.45, 0])
        scall = left_at(Code(SLOW_CALL, size=30), -6.15, stype.get_y() - 0.85)
        sres = left_at(Code(ANSWER, size=30), -6.15, scall.get_y() - 0.62)
        tick = check_mark().next_to(sres, RIGHT, buff=0.3)

        def pos(lv, i):
            return np.array([-TREE_W / 2 + (i + 0.5) * TREE_W / 2 ** lv, TREE_TOP - TREE_DY * lv, 0])

        dots = [[Dot(pos(lv, i), radius=0.075 if lv < 5 else 0.06, color=YELLOW).set_z_index(1)
                 for i in range(2 ** lv)] for lv in range(6)]
        edges = [[Line(pos(lv - 1, i // 2), pos(lv, i), stroke_width=2, color=DIM) for i in range(2 ** lv)]
                 for lv in range(1, 6)]
        counts = [T(str(2 ** lv), size=30, color=GOLD).move_to([COUNT_X, TREE_TOP - TREE_DY * lv, 0])
                  for lv in range(6)]
        cap = T("on a list of 20", size=32, color=DIM).move_to([0, -1.9, 0])
        c_slow = T("slow: 2097151 calls", size=40, t2c={"slow:": RED, "2097151": GOLD})
        c_bys = T("bysign: 21 calls", size=40, t2c={"bysign:": GREEN, "21": GOLD})
        c_slow.move_to([-3.4, -2.7, 0])
        c_bys.move_to([3.4, -2.7, 0])

        with self.say("c7.signs.5") as c:
            # "Another trap is to skip the let, and call the function twice, once for each half ..."
            sweep_clear(self, time_span(FadeIn(slow, shift=0.2 * DOWN), 0.5, 1.5),
                        time_span(Create(frame), 0.8, 1.8), time_span(FadeIn(stype, shift=0.2 * DOWN), 1.2, 1.9),
                        keep=[self.strip], run_time=1.9)
            c.wait_until("call the function twice")
            self.play(*[a for g in twice for a in recolor(g, YELLOW)],
                      *[FlashAround(VGroup(*g), color=YELLOW, time_width=1.5, buff=0.06) for g in twice],
                      run_time=1.5)
            # "The answer is still right,"
            c.wait_until("same")
            self.play(FadeIn(scall, shift=0.2 * DOWN), time_span(FadeIn(sres, shift=0.2 * DOWN), 0.4, 1.1),
                      time_span(Create(tick), 0.9, 1.4), run_time=1.4)
            # "but each call makes two more calls, so the work doubles with every element."
            c.wait_until("double")
            sweep_clear(self, scall.animate.move_to([0, TREE_TOP + 0.5, 0]),
                        time_span(FadeIn(dots[0][0], scale=0.5), 0.7, 1.1),
                        time_span(FadeIn(counts[0]), 0.7, 1.1),
                        keep=[self.strip, scall, sres, tick], run_time=1.1)
            for lv, rt in zip(range(1, 6), (0.8, 0.7, 0.6, 0.55, 0.55)):
                self.play(*[Create(e) for e in edges[lv - 1]],
                          *[time_span(FadeIn(d, scale=0.5), 0.4 * rt, rt) for d in dots[lv]],
                          time_span(FadeIn(counts[lv], shift=0.15 * DOWN), 0.4 * rt, rt), run_time=rt)
            # "On a list of twenty, that's over two million calls, against by-sign's twenty-one."
            c.wait_until("count")
            self.play(FadeOut(sres), FadeOut(tick), FadeIn(cap, shift=0.2 * DOWN),
                      time_span(FadeIn(c_slow, shift=0.2 * UP), 0.4, 1.2),
                      time_span(FadeIn(c_bys, shift=0.2 * UP), 0.9, 1.7), run_time=1.7)
        self.counters = [cap, c_slow, c_bys]

    # ── 6: two accumulators; reversed; the fix; the cost ─────────────────────────
    def clip_rev(self):
        rb = revbysign_code(30).move_to([-6.0, CODE_TOP, 0], aligned_edge=UL)
        ru = rev_colours(REVUNZIP_SRC, 28)
        for g in G(ru):
            g.set_opacity(UZ_DIM)
        ru.move_to([6.5, rb.get_bottom()[1] - 0.4, 0], aligned_edge=UR)
        rtype = Code(REVB_TYPE, size=28).move_to([-6.0, rb.get_bottom()[1] - 0.3, 0], aligned_edge=UL)
        call1 = left_at(Code(REV_CALL, size=30), -6.0, rtype.get_bottom()[1] - 0.5)
        ans1 = left_at(Code(REV_ANSWER, size=30), -6.0, call1.get_y() - 0.6)
        call2 = Code(FIX_CALL, size=30).move_to(call1)
        ans2 = Code(ANSWER, size=30).move_to(ans1)
        costs = VGroup(T("time O(n)", size=40, color=GOLD), T("space O(n)", size=40, color=GOLD))
        costs.arrange(RIGHT, buff=1.6).move_to([0, ans1.get_y() - 0.88, 0])
        box1 = token_box(rb.find("ps, ns", line=2), rb.line(2))
        box2 = token_box(ru.find("xs, ys", line=2), ru.line(2))

        with self.say("c7.signs.6") as c:
            # "Two accumulators make it iterative, like rev-unzip in chapter three."
            sweep_clear(self, time_span(FadeIn(rb, shift=0.2 * DOWN), 0.5, 1.5),
                        time_span(FadeIn(ru, shift=0.2 * LEFT), 1.1, 1.9),
                        *[time_span(FadeOut(m), 1.0, 1.8) for m in self.counters],
                        keep=[self.strip, *self.counters], run_time=1.9)
            c.wait_until("iterative")
            self.play(FadeIn(box1), run_time=0.7)
            c.wait_until(first_cue(c, "rev-unzip", "like"))
            self.play(TransformFromCopy(box1, box2), run_time=1.1)
            # "But both lists come out reversed, two, zero, three, and minus five, minus one."
            c.wait_until("but both lists")
            self.play(FadeOut(ru), FadeOut(box1), FadeOut(box2),
                      time_span(FadeIn(rtype, shift=0.2 * DOWN), 0.3, 1.1),
                      time_span(FadeIn(call1, shift=0.2 * DOWN), 0.8, 1.6), run_time=1.6)
            c.wait_until("come out reversed")
            self.play(FadeIn(ans1, shift=0.2 * DOWN), run_time=1.0)
            for words, sub in (("two, zero, three", "[2; 0; 3]"), ("minus five, minus one", "[-5; -1]")):
                c.wait_until(words)
                g = ans1.find(sub)
                self.play(*recolor(g, YELLOW), FlashUnder(VGroup(*g), color=YELLOW), run_time=1.0)
            # "If the order matters, reverse the input first."
            c.wait_until("reverse the input")
            rt = min(2.0, max(1.2, c.until("cost") - 0.1))
            self.play(*[time_span(a, 0, 0.55 * rt) for a in reorder(call1, call2, ["3", "-1", "-5", "2"])],
                      *[time_span(a, 0.45 * rt, rt) for a in reorder(ans1, ans2, ["2", "3", "-5", "-1"])],
                      run_time=rt)
            # "Either way, the time is big O of en, and so is the space the answer takes."
            c.wait_until("cost")
            self.play(FadeIn(costs[0], shift=0.2 * UP), time_span(FadeIn(costs[1], shift=0.2 * UP), 0.6, 1.4),
                      run_time=1.4)
            self.cost_born = self.time
