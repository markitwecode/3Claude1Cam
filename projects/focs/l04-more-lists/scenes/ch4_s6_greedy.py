"""Chapter 4, scene 6: where greedy fails (a 5 -> 2 till, change for 6). Clips c4.greedy.1 – c4.greedy.3.

Layout (frame x ±7.1, y ±4):
greedy.1  {greedy}: YELLOW "greedy" (T 72) at y 0.6, "largest first, never reconsider" (T 40) under it.
          {new}: the till (coin discs in cells, nil TEAL) centred (CHAIN_X, TILL_Y), DIM "paid" row
          label at PAID_Y; "make change for six": the title goes, DIM "amount" + GOLD "6" at
          COUNTER_X, trace row 0 at the bottom left. Trace rows Code 36, ch1's style (DIM ⇒ column
          left edge -6.6, rows left-aligned, elements FG, the count GOLD, each row born from copies
          of the row above). {five}: the 5 disc's copy drops into the paid row; "one is left": 6 -> 1
          and row 1. {stuck5}/{stuck2}: each cell dims with a RED "too big" (rows 2, 3); "both coins
          go": they slide off left. {empty}: nil flashes, counter RED. {fail}: RED exception (Code 32).
greedy.2  {but}: GREEN 2 discs at the bottom right; {twos}: `2 + 2 + 2 = 6` born from them; {ignore}:
          a DIM 5 disc, RED cross, left of them. {blame}: RED loop arrow from row 3 back to row 0,
          "never goes back". {code}: the till area clears; the third clause (Code 28) at the top;
          one YELLOW box slides from the skip to the use, each with its tag.
greedy.3  {often}: code, arrow, cross clear; the bottom dims to 0.4; the UK till (s2's, 0.85) at the
          top. {uk}: its 1 disc GREEN + "1p always finishes the job"; {fewest}: "fewest coins, for
          every amount". {nothere}: the UK till clears, the 5 -> 2 till returns (reset: "6", empty
          paid row) and the bottom brightens; "dead end": row 3 + exception flash RED.
End shot (ch5's hook reopens on it): till 5 -> 2 -> [], amount "6", empty paid row, the stuck trace,
its exception and the GREEN 2 + 2 + 2 = 6 card, alone.

End-shot layout: till_chain([5, 2], scale=1.0) (s2's helper) centred (-1.30, 2.55), 5.05 wide (cells at x -3.32, -1.02; nil
1.03); DIM "amount" T 30 at (3.40, 3.25); GOLD "6" T 64 at (3.40, 2.55); DIM "paid" T 30 at
(-4.43, 1.20), paid slot 0 at (-3.32, 1.20). Trace Code 36, rows left -5.80, baselines BASE, ⇒
MathTex 58 DIM at x -6.33; exception Code 32 RED, left -6.60, baseline -3.10. Card: GREEN coin(2)
discs at (3.83 / 4.95 / 6.07, -1.20); MathTex 56 GREEN `2 + 2 + 2 = 6` centred (4.95, -2.20)
(x 3.30 to 6.60; 0.54 clear of the exception's right end at 2.88).

STATUS: built; check clean apart from dwell notes: the two "too big" labels (the brief's
dims-and-slides-off inside 2 s of narration; the slide is delayed within its play, so they are up
~1.5 s / ~0.8 s, longer than the check measures) and "fewest coins, for every amount" (2.7 s; the
voice reads it, and {nothere} clears the UK till). 75.3 s vs 71.3 s narration (1.8 s end hold).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the till (copied from scenes/ch4_s2_idea.py; ch4–ch7 continuity) ──────────
COIN_R = 0.42                # the coin disc reused by ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34
S = 0.85                     # till chain scale: six cells + [] = 12.1 wide


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def till_chain(values, scale=S):
    """The till: ConsChain(values) scaled `scale`; each cell's label is coin(v, r=COIN_R*scale)
    (the value stays size 34). Nil TEAL as in ConsChain. Centred on ORIGIN."""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


def till_pointer(cell, name="till", length=0.75):
    """YELLOW Mono name above a cell with a short arrow down to its box."""
    tip = cell.box.get_top()
    lab = Mono(name, size=36, color=YELLOW).move_to(tip + UP * (length + 0.3))
    arr = Arrow(lab.get_bottom(), tip, buff=0.06, stroke_width=3, color=YELLOW,
                max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)


# ── layout ────────────────────────────────────────────────────────────────────
TILL_Y = 2.55
CHAIN_X = -1.3
COUNTER_X = 3.4
AMOUNT_LABEL_Y = 3.25
PAID_Y = 1.2

SIZE = 36                                   # trace rows
BASE = [-0.02, -0.78, -1.54, -2.30]         # trace baselines (pitch 0.76)
ARROW_LEFT = -6.6                           # ⇒ column left edge
ARROW_GAP = 0.27
EXC_SIZE, EXC_BASE = 32, -3.10

ROWS = ["change [5; 2] 6", "5 :: change [5; 2] 1", "5 :: change [2] 1", "5 :: change [] 1"]
EXC = 'Exception: Failure "no more coins!".'

TWOS_X = [3.83, 4.95, 6.07]
TWOS_Y, EQ_Y = -1.20, -2.20
FIVE_X = 2.71

CLAUSE = ("| c::till, amt -> if amt < c then change till amt\n"
          "                  else c :: change (c::till) (amt - c)")
CLAUSE_SIZE, CLAUSE_Y = 28, 2.35

UK = [50, 20, 10, 5, 2, 1]
UK_Y = 2.65
UK_LAB_Y = (1.65, 1.05)
BACK_DIM = 0.4

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789ABCDEFGHIKLMNORSTUVWXYZ")


# ── trace helpers (ch1_s3_trace's, so the traces look the same) ─────────────────
def baseline(code):
    """y of the text baseline of a Code."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
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


def all_of(code, sub):
    out, n = [], 0
    while True:
        try:
            out.append(G(code, sub, n))
        except ValueError:
            return out
        n += 1


def implies():
    return MathTex(r"\Rightarrow", font_size=58, color=DIM)


def paint(row):
    """Trace colours: list elements FG, the count (last glyph) GOLD."""
    for d in "52":
        for g in all_of(row, d):
            g.set_color(FG)
    row.text[-1].set_color(GOLD)
    return row


def faded(mob, k):
    """A copy of mob with every fill and stroke opacity scaled by k (keeps faint fills faint)."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k)
    return t


def back_arrow(start, end, x_out, color=RED):
    """A loop arrow: out to the right of `start`, up, and back left into `end`."""
    a = TipableVMobject()
    a.set_points(np.array([start, [x_out, start[1], 0], [x_out, end[1], 0], end]))
    a.set_color(color).set_stroke(color, 5).set_fill(opacity=0)
    a.add_tip(tip_length=0.24, tip_width=0.24)
    a.tip.set_fill(color, 1).set_stroke(color, 0)
    return a


class WhereGreedyFails(NarratedScene):
    def construct(self):
        self.build()
        self.stuck()      # c4.greedy.1
        self.but()        # c4.greedy.2
        self.often()      # c4.greedy.3
        self.wait(1.8)    # hand-off shot (ch5's hook reopens on it)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── layout, built up front ────────────────────────────────────────────────
    def make_till(self):
        chain = till_chain([5, 2], scale=1.0).move_to([CHAIN_X, TILL_Y, 0])
        amount = T("amount", 30, DIM).move_to([COUNTER_X, AMOUNT_LABEL_Y, 0])
        num = T("6", 64, GOLD).move_to([COUNTER_X, TILL_Y, 0])
        slot0 = chain.cells[0].box.get_x()
        paid = T("paid", 30, DIM)
        paid.move_to([slot0 - COIN_R - 0.3 - paid.width / 2, PAID_Y, 0])
        return chain, amount, num, paid

    def build(self):
        self.chain, self.amount, self.num, self.paid = self.make_till()
        self.paid5 = coin(5).move_to([self.chain.cells[0].box.get_x(), PAID_Y, 0])
        self.bigs = [T("too big", 30, RED).next_to(c, UP, buff=0.12) for c in self.chain.cells]

        rows = [paint(Code(s, size=SIZE)) for s in ROWS]
        aw = implies().width
        self.x0 = ARROW_LEFT + aw + ARROW_GAP
        for r, b in zip(rows, BASE):
            put(r, self.x0, b)
        self.rows = rows
        self.arrows = [None] + [implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + 0.12)
                                for r, b in zip(rows[1:], BASE[1:])]
        self.exc = put(Code(EXC, size=EXC_SIZE), ARROW_LEFT, EXC_BASE).set_color(RED)

        # the card: three GREEN 2s and their sum; the five set aside
        self.twos = VGroup(*[coin(2).set_color(GREEN).move_to([x, TWOS_Y, 0]) for x in TWOS_X])
        self.eq = MathTex("2", "+", "2", "+", "2", "=", "6", font_size=56, color=GREEN)
        self.eq.move_to([self.twos.get_x(), EQ_Y, 0])
        self.five = coin(5).set_color(DIM).move_to([FIVE_X, TWOS_Y, 0])
        self.five_x = Line([-0.36, -0.36, 0], [0.36, 0.36, 0]).set_stroke(RED, 6)   # struck out
        self.five_x.move_to(self.five)

        # the road not taken: from the dead end back to the first call
        mid = [b + 0.12 for b in BASE]
        sx, ex = rows[3].get_right()[0] + 0.2, rows[0].get_right()[0] + 0.2
        x_out = (rows[1].get_right()[0] + 0.45 - 0.059 * sx - 0.227 * ex) / 0.714
        self.back = back_arrow([sx, mid[3], 0], [ex, mid[0], 0], x_out)
        self.never = T("never goes back", 30, RED)
        reach = max(self.back.point_from_proportion(t)[0] for t in np.linspace(0, 1, 60))
        self.never.move_to([reach + 0.3 + self.never.width / 2, (mid[0] + mid[1]) / 2, 0])

        # the third clause, small, with its two tags
        self.clause = Code(CLAUSE, size=CLAUSE_SIZE).move_to([0, CLAUSE_Y, 0])
        skip = self.clause.find("if amt < c then change till amt", line=0)
        use = self.clause.find("c :: change (c::till) (amt - c)", line=1)
        self.box1 = token_box(skip, self.clause.line(0), color=YELLOW)
        self.box2 = token_box(use, self.clause.line(1), color=YELLOW)
        self.tag1 = T("skip only if too large", 30, YELLOW).next_to(self.box1, UP, buff=0.15)
        self.tag2 = T("fits: used, for good", 30, YELLOW).next_to(self.box2, DOWN, buff=0.15)

        # the UK till, small, and what it guarantees
        self.uk = till_chain(UK).move_to([0, UK_Y, 0])
        right = self.uk.get_right()[0]
        self.uk_lab1 = T("1p always finishes the job", 32, GREEN)
        self.uk_lab2 = T("fewest coins, for every amount", 32, GREEN)
        for lab, y in zip((self.uk_lab1, self.uk_lab2), UK_LAB_Y):
            lab.move_to([right - lab.width / 2, y, 0])

    def birth(self, k, pairs):
        """Row k+1 born from row k: (src_sub, src_nth, dst_sub, dst_nth, arc) copied down;
        src_sub None fades that part in. Returns (anims, parts); call land() after the play."""
        src, dst = self.rows[k], self.rows[k + 1]
        anims, parts = [], []
        for s_sub, s_nth, d_sub, d_nth, arc in pairs:
            t = G(dst, d_sub, d_nth)
            if s_sub is None:
                anims.append(FadeIn(t, shift=0.15 * DOWN))
            else:
                anims.append(TransformFromCopy(G(src, s_sub, s_nth), t, path_arc=arc))
            parts.append(t)
        anims.append(FadeIn(self.arrows[k + 1], shift=0.2 * DOWN))
        return anims, parts

    def land(self, k, parts):
        self.remove(*parts)
        self.add(self.rows[k + 1])

    def skip_cell(self, i):
        """The i-th till cell dims and gets its RED "too big"."""
        cell, arrow = self.chain.cells[i], self.chain.arrows[i]
        return [Transform(cell, faded(cell, 0.35)), Transform(arrow, faded(arrow, 0.35)),
                FadeIn(self.bigs[i], shift=0.15 * DOWN)]

    # ── greedy.1: greedy, and the till where it gets stuck ──────────────────────
    def stuck(self):
        ch, cells, r = self.chain, self.chain.cells, self.rows
        with self.say("c4.greedy.1") as c:
            # "Our change function is greedy."
            word = T("greedy", 72, YELLOW).move_to(UP * 0.6)
            sub = T("largest first, never reconsider", 40).move_to(DOWN * 0.45)
            self.play(FadeIn(word, shift=0.3 * DOWN), run_time=1.0)
            # "It grabs the largest coin that fits, and never reconsiders."
            c.wait_until("it grabs")
            self.play(FadeIn(sub, shift=0.3 * DOWN), run_time=1.0)

            # "Now take a different till, with only fives and twos, ..."
            c.wait_until("new")
            self.play(FadeIn(ch, lag_ratio=0.15), FadeIn(self.paid, shift=0.2 * DOWN),
                      run_time=1.5)
            # "... and make change for six."
            c.wait_until("make change")
            self.play(time_span(FadeOut(word, sub), 0, 0.7),
                      time_span(FadeIn(self.amount, self.num, shift=0.2 * DOWN), 0.2, 1.1),
                      time_span(FadeIn(r[0], shift=0.3 * DOWN), 0.5, 1.4), run_time=1.4)

            # "Five fits, so we use it, ..."
            c.wait_until("five")
            self.play(TransformFromCopy(cells[0].label, self.paid5),
                      FlashAround(cells[0], color=YELLOW, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("one is left")))
            # "... and one is left."
            c.wait_until("one is left")
            anims, parts = self.birth(0, [("5", 0, "5", 0, 0.6), (None, 0, "::", 0, 0),
                                          ("change", 0, "change", 0, 0),
                                          ("[5; 2]", 0, "[5; 2]", 0, 0), ("6", 0, "1", 0, 0)])
            one = T("1", 64, GOLD).move_to(self.num)
            self.play(*anims, ReplacementTransform(self.num, one),
                      run_time=min(1.3, 0.95 * c.until("stuck5")))
            self.num = one
            self.land(0, parts)

            # "One is less than five,"
            c.wait_until("stuck5")
            step = [("5 ::", 0, "5 ::", 0, 0), ("change", 0, "change", 0, 0),
                    ("[", 0, "[", 0, 0), ("1", 0, "1", 0, 0)]
            anims, parts = self.birth(1, step + [("2]", 0, "2]", 0, 0)])
            self.play(*self.skip_cell(0), *anims, run_time=min(0.9, 0.95 * c.until("stuck2")))
            self.land(1, parts)
            # "and less than two, ..."
            c.wait_until("stuck2")
            anims, parts = self.birth(2, step + [("]", 0, "]", 0, 0)])
            self.play(*self.skip_cell(1), *anims,
                      run_time=min(0.8, 0.9 * c.until("both coins go")))
            self.land(2, parts)
            # "... so both coins go."
            c.wait_until("both coins go")
            off, T_go = 1.6 * LEFT, min(1.8, 0.95 * c.until("empty"))
            gone = []
            for i, (a, b) in enumerate([(0.3, 0.8), (0.45, 1.0)]):
                for m in (cells[i], ch.arrows[i], self.bigs[i]):
                    gone.append(time_span(FadeOut(m, shift=off), a * T_go, b * T_go))
            self.play(*gone, run_time=T_go)

            # "The till is empty, with a penny still owed."
            c.wait_until("empty")
            self.play(FlashAround(ch.nil, color=TEAL, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("a penny")))
            c.wait_until("a penny")
            self.play(self.num.animate.set_color(RED),
                      FlashAround(self.num, color=RED, time_width=1.5), run_time=1.0)

            # "So change raises its exception."
            c.wait_until("fail")
            self.play(FadeIn(self.exc, shift=0.3 * DOWN), run_time=1.0)
            # "No more coins."
            c.wait_until("no more coins")
            self.play(FlashUnder(G(self.exc, '"no more coins!"'), color=RED, time_width=1.5),
                      run_time=min(1.3, c.remaining))

    # ── greedy.2: the change that exists, and why greedy misses it ──────────────
    def but(self):
        r = self.rows
        with self.say("c4.greedy.2") as c:
            # "But change for six can be made."
            self.play(FadeIn(self.twos, shift=0.2 * DOWN, lag_ratio=0.25), run_time=1.2)
            # "Two, plus two, plus two."
            c.wait_until("twos")
            eq = self.eq
            anims = [time_span(TransformFromCopy(self.twos[i][1], eq[2 * i]), 0.6 * i, 0.6 * i + 1.0)
                     for i in range(3)]
            anims += [time_span(FadeIn(eq[1]), 0.4, 1.0), time_span(FadeIn(eq[3]), 1.0, 1.6),
                      time_span(FadeIn(eq[5]), 1.6, 2.1), time_span(FadeIn(eq[6]), 1.8, 2.3)]
            self.play(*anims, run_time=2.3)
            self.remove(*eq)
            self.add(eq)

            # "The only way is to ignore the five altogether."
            c.wait_until("ignore")
            self.play(FadeIn(self.five, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("altogether")
            self.play(Create(self.five_x), run_time=0.7)

            # "Greedy took the five, and never went back to try without it."
            c.wait_until("blame")
            self.play(FlashAround(G(r[1], "5 ::"), color=YELLOW, time_width=1.5),
                      FlashAround(self.paid5, color=YELLOW, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("never went back")))
            c.wait_until("never went back")
            self.play(Create(self.back), time_span(FadeIn(self.never, shift=0.2 * LEFT), 0.7, 1.4),
                      run_time=1.4)

            # "Look at the code again."
            c.wait_until("code")
            keep = [*r, *self.arrows[1:], self.exc, self.twos, eq, self.five, self.five_x,
                    self.back, self.never]
            sweep_clear(self, time_span(FadeIn(self.clause, shift=0.2 * DOWN), 0.5, 1.4),
                        keep=keep, run_time=1.4)
            # "It skips a coin only when the coin is too large."
            c.wait_until("it skips")
            self.play(FadeIn(self.box1), FadeIn(self.tag1, shift=0.2 * DOWN), run_time=1.0)
            # "Once the five fits, it's used, and nothing ever undoes that choice."
            c.wait_until("once the five")
            box = self.box1
            self.play(Transform(box, self.box2), time_span(FadeIn(self.tag2, shift=0.2 * UP), 0.6, 1.4),
                      run_time=1.4)
            c.wait_until("nothing ever undoes")
            self.play(FlashAround(self.never, color=RED, time_width=1.5), run_time=1.2)

            # "So greedy change can fail, even when change is possible."
            c.wait_until("can fail")
            self.play(FlashAround(self.exc, color=RED, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("is possible")))
            c.wait_until("is possible")
            self.play(FlashAround(VGroup(self.twos, eq), color=GREEN, time_width=1.5),
                      run_time=min(1.2, c.remaining))

    # ── greedy.3: when greedy is right, and when it isn't ───────────────────────
    def often(self):
        bottom = [*self.rows, *self.arrows[1:], self.exc, self.twos, self.eq]
        with self.say("c4.greedy.3") as c:
            # "Greedy algorithms are often effective."
            for m in bottom:
                m.save_state()
            sweep_clear(self, *[Transform(m, faded(m, BACK_DIM)) for m in bottom],
                        time_span(FadeIn(self.uk, lag_ratio=0.1), 0.5, 1.8),
                        keep=bottom, run_time=1.8)
            # "With British coins, this one can never get stuck, because the one pence coins ..."
            c.wait_until("uk")
            last = self.uk.cells[-1]
            self.play(last.label.animate.set_color(GREEN),
                      FlashAround(last, color=GREEN, time_width=1.5),
                      time_span(FadeIn(self.uk_lab1, shift=0.2 * DOWN), 0.3, 1.2), run_time=1.2)
            # "And for every amount, it uses the fewest coins possible."
            c.wait_until("fewest")
            self.play(FadeIn(self.uk_lab2, shift=0.2 * DOWN), run_time=0.8)

            # "But with fives and twos, largest first leads to a dead end."
            c.wait_until("nothere")
            chain, amount, num, paid = self.make_till()
            sweep_clear(self, *[Restore(m) for m in bottom],
                        time_span(FadeIn(chain, lag_ratio=0.15), 0.5, 1.6),
                        time_span(FadeIn(amount, num, paid), 0.7, 1.6),
                        keep=bottom, run_time=1.6)
            c.wait_until("dead end")
            self.play(FlashAround(VGroup(self.rows[3], self.exc), color=RED, time_width=1.5),
                      run_time=min(1.3, c.remaining))
