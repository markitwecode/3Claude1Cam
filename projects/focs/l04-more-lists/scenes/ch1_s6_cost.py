"""Chapter 1, scene 6: what take and drop cost. Clips c1.cost.1 – c1.cost.4.

Layout: two columns. Left = take's finished trace (scene 3: growing, YELLOW waiting conses),
right = drop's flat trace (scene 4). Rows are Code TRACE_SIZE, baselines BASE, DIM ⇒ column
(MathTex IMPLIES_SIZE). Costs build under each column, left-aligned with its ⇒ column, rows at
TIME_Y / SPACE_Y / WHY1_Y / WHY2_Y. In c1.cost.2 a DIM card-pile sketch (L3 ch4's piles) sits
under the dimmed drop trace; c1.cost.3 clears it. c1.cost.4 sweeps to two O(i) labels on top
and a small work-vs-i graph. Starts and ends on an empty frame.

STATUS: built; check clean except one dwell note (drop's "O(1) space" up 4.5 s of 5.5 before the
c1.cost.4 sweep; it stays through the next sentence). Trace and cell styling match s3–s5 as
reported (continuity block below), scaled from Code 40 to TRACE_SIZE.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── continuity with scenes 3–5 (one place: update when their builders report) ──────────────
# s3/s4 trace style (Code 40, pitch 0.84, ⇒ MathTex 64 DIM, 0.3 left of rows, baseline + 0.13,
# call box 0.66 tall), scaled down to TRACE_SIZE so the two traces fit side by side.
TRACE_SIZE = 28          # Code size of both traces
S = TRACE_SIZE / 40
IMPLIES_SIZE = 64 * S    # the DIM ⇒ (MathTex)
ARROW_GAP = 0.3 * S      # ⇒ to row
IMPLIES_DY = 0.13 * S    # ⇒ centre above the row baseline
PITCH = 0.84 * S         # row pitch
BOX_H = 0.66 * S         # L3's highlight box
COUNT_C = GOLD           # the count argument of each call
ELEM_C = FG              # list elements (recoloured after highlighting, as s4)
NAME_C = FG              # take / drop, plain in the trace
WAIT_C = YELLOW          # waiting conses
ANSWER_C = GREEN         # take's built answer [3; 5]
UNSEEN_OP = 0.3          # elements take never looks at (9; 4; 7)
NEW_C = YELLOW           # new cells (s5): YELLOW outlines, FG value, BG fill; own nil plain Nil()
SHARED_C = TEAL          # drop's shared tail (s5)

TAKE_ROWS = ["take 2 [3; 5; 9; 4; 7]",
             "3 :: take 1 [5; 9; 4; 7]",
             "3 :: 5 :: take 0 [9; 4; 7]",
             "3 :: 5 :: []",
             "[3; 5]"]
TAKE_WAIT = [None, "3 ::", "3 :: 5 ::", "3 :: 5 ::", None]
DROP_ROWS = ["drop 2 [3; 5; 9; 4; 7]",
             "drop 1 [5; 9; 4; 7]",
             "drop 0 [9; 4; 7]",
             "[9; 4; 7]"]

BASE = [2.95 - PITCH * k for k in range(5)]
EDGE = 6.55                       # both columns stay inside ±EDGE
TIME_Y, SPACE_Y, WHY1_Y, WHY2_Y = -0.2, -0.94, -1.62, -2.35
COST_SIZE = 46
WHY_SIZE = 30

# card piles (L3 ch4), small, under the drop column
CARD_W, CARD_H, SLOT = 0.85, 0.5, 0.58
PILE_Y0 = -2.6                    # centre of the bottom slot

# the graph in c1.cost.4
ORIG = np.array([-3.4, -2.45, 0.0])
X_LEN, Y_LEN = 6.5, 4.45
TAKE_END = ORIG + np.array([4.3, 3.95, 0.0])
DROP_END = ORIG + np.array([6.0, 1.3, 0.0])

_ON_BASE = set("abcdefhiklmnorstuvwxz0123456789")


def baseline(code):
    """y of the text baseline of a Code (first glyph that sits on it)."""
    chars = [ch for ch in code.src if not ch.isspace()]
    for ch, g in zip(chars, code.text):
        if ch in _ON_BASE:
            return g.get_bottom()[1]
    return code.get_bottom()[1]


def put(code, left, base):
    code.shift(RIGHT * (left - code.get_left()[0]) + UP * (base - baseline(code)))
    return code


def implies():
    return MathTex(r"\Rightarrow", font_size=IMPLIES_SIZE, color=DIM)


def G(code, sub, nth=0):
    return VGroup(*code.find(sub, nth=nth))


def trace_column(srcs, x0, name):
    """Rows left-aligned at x0, ⇒ to the left of every row but the first."""
    rows = [Code(s, size=TRACE_SIZE) for s in srcs]
    arrows = []
    for k, (r, b) in enumerate(zip(rows, BASE)):
        put(r, x0, b)
        if name in r.src:
            G(r, name).set_color(NAME_C)
        if k:
            arrows.append(implies().next_to(r, LEFT, buff=ARROW_GAP).set_y(b + IMPLIES_DY))
    for r in rows:                          # list elements plain
        a, z = r.src.find("["), r.src.find("]")
        if 0 <= a and z > a + 1:
            for glyph in r.find(r.src[a:z + 1])[1:-1]:
                glyph.set_color(ELEM_C)
    for r in rows:                          # the count argument of each call
        i = r.src.find(name + " ")
        if i >= 0:
            digit = r.src[i + len(name) + 1]
            for glyph in r.find(f"{name} {digit}")[-1:]:
                glyph.set_color(COUNT_C)
    return rows, arrows


def cost(tex, color, left, y):
    m = MathTex(tex, font_size=COST_SIZE, color=color)
    return m.move_to([left + m.width / 2, y, 0])


def why(words, value, left, y, color=FG, t2c=None):
    """A reason row: words, then the amount (MathTex), on one baseline."""
    t = T(words, WHY_SIZE, color=color, t2c=t2c or {})
    v = MathTex(value, font_size=WHY_SIZE + 6, color=GOLD)
    v.next_to(t, RIGHT, buff=0.16).align_to(t[-1], DOWN)
    g = VGroup(t, v)
    return g.move_to([left + g.width / 2, y, 0])


def card(v, color=DIM):
    box = RoundedRectangle(width=CARD_W, height=CARD_H, corner_radius=0.1, stroke_color=color,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(box, value_label(v, size=32).move_to(box))


def slot(x, k):
    return np.array([x, PILE_Y0 + SLOT * k, 0.0])


def landed(crd, pos, color):
    crd.generate_target()
    crd.target.move_to(pos)
    crd.target[0].set_stroke(color)
    return crd


class WhatTheyCost(NarratedScene):
    def construct(self):
        self.build()
        self.take_costs()          # c1.cost.1
        self.accumulator()         # c1.cost.2
        self.drop_costs()          # c1.cost.3
        self.constant_factors()    # c1.cost.4
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── layout, built up front ──────────────────────────────────────────────────────────
    def build(self):
        w_imp = implies().width
        self.tl = -EDGE                                       # left of take's ⇒ column
        tx0 = self.tl + w_imp + ARROW_GAP
        self.tr, t_arr = trace_column(TAKE_ROWS, tx0, "take")
        for r, sub in zip(self.tr, TAKE_WAIT):
            if sub:
                G(r, sub).set_color(WAIT_C)
        G(self.tr[4], "[3; 5]").set_color(ANSWER_C)
        for r in self.tr[:3]:
            G(r, "9; 4; 7").set_opacity(UNSEEN_OP)
        self.box_dy = self.tr[0].get_y() - BASE[0]
        widest = max(Code(s, size=TRACE_SIZE).width for s in DROP_ROWS)
        dx0 = EDGE - widest
        self.dl = dx0 - ARROW_GAP - w_imp                     # left of drop's ⇒ column
        self.dr, d_arr = trace_column(DROP_ROWS, dx0, "drop")
        self.take_col = VGroup(*self.tr, *t_arr)
        self.drop_col = VGroup(*self.dr, *d_arr)

        # take's costs
        tl, dl = self.tl, self.dl
        self.t_time = cost(r"O(i)\ \text{time}", GOLD, tl, TIME_Y)
        self.t_space = cost(r"O(i)\ \text{space}", GOLD, tl, SPACE_Y)
        self.t_wait = why("waiting conses:", "i", tl, WHY1_Y, t2c={"waiting conses": WAIT_C})
        self.t_new = why("new cells:", "i", tl, WHY2_Y, t2c={"new cells": NEW_C})
        ch = ConsChain([3, 5], color=NEW_C).scale(0.7)
        self.t_chain = ch.next_to(self.t_new, RIGHT, buff=0.45).set_y(WHY2_Y)

        # drop's costs
        self.d_time = cost(r"O(i)\ \text{time}", GOLD, dl, TIME_Y)
        self.d_space = cost(r"O(1)\ \text{space}", GREEN, dl, SPACE_Y)
        self.d_wait = T("nothing waits", WHY_SIZE, color=GREEN)
        self.d_wait.move_to([dl + self.d_wait.width / 2, WHY1_Y, 0])
        self.d_new = why("new cells:", "1", dl, WHY2_Y, t2c={"new cells": NEW_C})
        c9 = ConsCell(9, color=NEW_C).scale(0.7)
        c9.next_to(self.d_new, RIGHT, buff=0.45).set_y(WHY2_Y)
        self.c9 = c9
        self.c9_arrow = Arrow(c9.tail_start(), c9.tail_start() + RIGHT * 0.85, buff=0,
                              stroke_width=4, color=SHARED_C, tip_length=0.18)
        self.c9_shared = T("shared", WHY_SIZE, color=SHARED_C).next_to(self.c9_arrow, RIGHT, 0.12)

    def hbox(self, glyphs, k, color=GOLD):
        """L3's call box (thin stroke, faint fill, fixed height) behind glyphs of row k."""
        g = VGroup(*glyphs)
        r = Rectangle(width=g.width + 2 * 0.12 * S + 0.1, height=BOX_H, stroke_color=color,
                      stroke_width=2.5).set_fill(color, opacity=0.18).set_z_index(-1)
        return r.move_to([g.get_x(), BASE[k] + self.box_dy, 0])

    def calls_row(self, left):
        w = T("calls:", 32)
        w.move_to([left + w.width / 2, TIME_Y, 0])
        d1 = Mono("1", 34, color=GOLD).next_to(w, RIGHT, buff=0.22).align_to(w, DOWN)
        d2 = Mono("2", 34, color=GOLD).next_to(d1, RIGHT, buff=0.26).align_to(w, DOWN)
        return w, d1, d2

    # ── c1.cost.1: take, O(i) time and O(i) space ───────────────────────────────────────
    def take_costs(self):
        tr = self.tr
        with self.say("c1.cost.1") as c:
            self.play(LaggedStart(FadeIn(self.take_col, shift=0.2 * DOWN),
                                  FadeIn(self.drop_col, shift=0.2 * DOWN), lag_ratio=0.35),
                      run_time=min(1.8, 0.8 * c.until("Take makes")))
            c.wait_until("Take makes")

            w, d1, d2 = self.calls_row(self.tl)
            box = self.hbox(tr[1].find("take 1"), 1)
            self.play(FadeIn(box), FadeIn(w, shift=0.2 * DOWN), FadeIn(d1, shift=0.3 * DOWN),
                      run_time=min(1.2, 0.7 * c.until("for each element")))
            c.wait_until("for each element")
            self.play(Transform(box, self.hbox(tr[2].find("take 0"), 2)),
                      FadeIn(d2, shift=0.3 * DOWN),
                      run_time=min(1.0, 0.7 * c.until("count of eye")))
            c.wait_until("count of eye")
            self.play(Transform(box, self.hbox(tr[0].find("2"), 0)),
                      run_time=min(0.9, 0.7 * c.until("its time")))
            c.wait_until("its time")
            calls = VGroup(w, d1, d2)
            settle(self, calls)
            self.play(FadeOut(box), ReplacementTransform(calls, self.t_time),
                      run_time=min(1.5, 0.7 * c.until("Its space")))

            c.wait_until("Its space")
            self.play(FadeIn(self.t_space, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("While it runs")
            self.play(FadeIn(self.t_wait, shift=0.2 * DOWN),
                      FlashAround(G(tr[2], "3 :: 5 ::"), color=WAIT_C, time_width=1.5),
                      run_time=1.6)
            c.wait_until("And when it's done")
            self.play(FadeIn(self.t_new, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("the answer is a copy")
            self.play(TransformFromCopy(G(tr[4], "[3; 5]"), self.t_chain),
                      run_time=min(1.6, 0.8 * c.until("one new cell")))
            c.wait_until("one new cell")
            self.play(*[FlashAround(cell, color=NEW_C, time_width=1.5) for cell in self.t_chain.cells],
                      run_time=1.5)

    # ── c1.cost.2: an accumulator would build the copy backwards ────────────────────────
    def accumulator(self):
        src_x = self.dl + 0.65
        acc_x = src_x + 1.45
        self.cards = {v: card(v) for v in (3, 5, 9, 4, 7)}
        for k, v in enumerate((7, 4, 9, 5, 3)):              # 3 on top
            self.cards[v].move_to(slot(src_x, k))
        self.outline = DashedVMobject(RoundedRectangle(width=CARD_W, height=CARD_H, corner_radius=0.1,
                                                       stroke_color=DIM, stroke_width=3),
                                      num_dashes=20).move_to(slot(acc_x, 0))
        self.acc_lbl = Mono("acc", 30, color=DIM).move_to(slot(acc_x, 1) + UP * (CARD_H / 2 + 0.32))
        mid_y = (slot(acc_x, 0)[1] + slot(acc_x, 1)[1]) / 2
        a_x = acc_x + CARD_W / 2 + 0.12
        self.rev_arrow = ArcBetweenPoints([a_x, slot(acc_x, 1)[1] + 0.12, 0],
                                          [a_x, slot(acc_x, 0)[1] - 0.12, 0],
                                          angle=-0.8 * PI, color=GOLD, stroke_width=4)
        self.rev_arrow.add_tip(tip_length=0.16, tip_width=0.16)
        self.rev_arrow.add_tip(at_start=True, tip_length=0.16, tip_width=0.16)
        lbl_x = a_x + 0.62
        self.back_lbl = T("backwards", 32, color=RED)
        self.back_lbl.move_to([lbl_x + self.back_lbl.width / 2, mid_y, 0])
        self.rev_lbl = T("+ a reversal", 32, color=GOLD)
        self.rev_lbl.move_to([lbl_x + self.rev_lbl.width / 2, mid_y, 0])
        self.warn = T("an extra reversal can cost more than it saves", 30, color=DIM).move_to([0, -3.42, 0])
        cards = self.cards

        with self.say("c1.cost.2") as c:
            pile = [cards[v] for v in (7, 4, 9, 5, 3)]
            self.play(restyle(self.drop_col, op=DIMMED),
                      LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in pile + [self.outline, self.acc_lbl]],
                                  lag_ratio=0.12),
                      run_time=min(1.6, 0.6 * c.until("Not here")))
            c.wait_until("one new cell")
            self.play(FlashAround(self.t_new, color=NEW_C, time_width=1.5),
                      *[FlashAround(cell, color=NEW_C, time_width=1.5) for cell in self.t_chain.cells],
                      run_time=1.5)
            c.wait_until("space whatever")
            self.play(FlashAround(self.t_space, color=GOLD, time_width=1.5), run_time=1.6)

            c.wait_until("And an accumulator would")
            rt = min(2.4, 0.95 * c.until("backwards"))
            landed(cards[3], slot(acc_x, 0), NEW_C)
            landed(cards[5], slot(acc_x, 1), NEW_C)
            self.play(MoveToTarget(cards[3], path_arc=-0.6 * PI),
                      time_span(FadeOut(self.outline), 0.5 * rt, 0.8 * rt),
                      time_span(MoveToTarget(cards[5], path_arc=-0.6 * PI), 0.45 * rt, rt),
                      run_time=rt)
            c.wait_until("backwards")
            self.play(FadeIn(self.back_lbl, shift=0.2 * LEFT), run_time=0.8)

            c.wait_until("So we'd need")
            landed(cards[3], slot(acc_x, 1), NEW_C)
            landed(cards[5], slot(acc_x, 0), NEW_C)
            self.play(MoveToTarget(cards[3], path_arc=-PI), MoveToTarget(cards[5], path_arc=-PI),
                      Create(self.rev_arrow),
                      time_span(FadeTransform(self.back_lbl, self.rev_lbl), 0.7, 1.7),
                      run_time=1.7)
            c.wait_until("That's the warning")
            self.play(FadeIn(self.warn, shift=0.2 * UP), run_time=1.0)
            c.wait_until("extra reversal")
            self.play(FlashAround(self.rev_lbl, color=GOLD, time_width=1.5), run_time=1.5)

    # ── c1.cost.3: drop, O(i) time and O(1) space ───────────────────────────────────────
    def drop_costs(self):
        dr = self.dr
        sketch = [*self.cards.values(), self.acc_lbl, self.rev_arrow, self.rev_lbl]
        with self.say("c1.cost.3") as c:
            self.play(LaggedStart(*[FadeOut(m) for m in sketch], lag_ratio=0.08),
                      restyle(self.drop_col, op=1),
                      run_time=min(1.4, 0.8 * c.until("It skips")))
            c.wait_until("It skips")
            w, d1, d2 = self.calls_row(self.dl)
            box = self.hbox(dr[1].find("drop 1"), 1)
            self.play(FadeIn(box), FadeIn(w, shift=0.2 * DOWN), FadeIn(d1, shift=0.3 * DOWN),
                      FadeOut(self.warn), run_time=min(1.0, 0.7 * c.until("one call at a time")))
            c.wait_until("one call at a time")
            self.play(Transform(box, self.hbox(dr[2].find("drop 0"), 2)),
                      FadeIn(d2, shift=0.3 * DOWN),
                      run_time=min(0.8, 0.7 * c.until("at most eye")))
            c.wait_until("at most eye")
            self.play(Transform(box, self.hbox(dr[0].find("2"), 0)),
                      run_time=min(0.8, 0.7 * c.until("so its time")))
            c.wait_until("so its time")
            calls = VGroup(w, d1, d2)
            settle(self, calls)
            self.play(FadeOut(box), ReplacementTransform(calls, self.d_time),
                      run_time=min(1.4, 0.7 * c.until("nothing waits")))

            c.wait_until("nothing waits")
            self.play(FadeIn(self.d_wait, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("at most one new cell")
            rt = min(1.6, 0.85 * c.until("its space is constant"))
            self.play(FadeIn(self.d_new, shift=0.2 * DOWN),
                      TransformFromCopy(G(dr[3], "9"), self.c9),
                      time_span(GrowArrow(self.c9_arrow), 0.5 * rt, 0.85 * rt),
                      time_span(FadeIn(self.c9_shared, shift=0.2 * LEFT), 0.6 * rt, rt),
                      run_time=rt)
            c.wait_until("its space is constant")
            self.play(FadeIn(self.d_space, shift=0.3 * DOWN), run_time=1.0)
            self.play(FlashAround(self.d_space, color=GREEN, time_width=1.5),
                      run_time=min(1.5, max(0.5, c.remaining)))

    # ── c1.cost.4: same big O, different constant factors ───────────────────────────────
    def constant_factors(self):
        t_time, d_time = self.t_time, self.d_time
        top_t = VGroup(Mono("take", 36, color=NAME_C), t_time.copy())
        top_d = VGroup(Mono("drop", 36, color=NAME_C), d_time.copy())
        for g, x in ((top_t, -3.55), (top_d, 3.55)):
            g[0].next_to(g[1], LEFT, buff=0.35).align_to(g[1][0][-1], DOWN)
            g.move_to([x, 3.2, 0])
        x_ax = Arrow(ORIG, ORIG + RIGHT * X_LEN, buff=0, stroke_width=3, color=FG, tip_length=0.2)
        y_ax = Arrow(ORIG, ORIG + UP * Y_LEN, buff=0, stroke_width=3, color=FG, tip_length=0.2)
        i_lbl = MathTex("i", font_size=40, color=FG).next_to(x_ax.get_end(), RIGHT, buff=0.15)
        work = T("work", 30, color=FG).next_to(y_ax.get_end(), LEFT, buff=0.2).shift(DOWN * 0.15)
        take_line = Line(ORIG, TAKE_END, color=GOLD, stroke_width=6)
        drop_line = Line(ORIG, DROP_END, color=GREEN, stroke_width=6)
        take_lbl = Mono("take", 32, color=GOLD).next_to(TAKE_END, RIGHT, buff=0.25)
        drop_lbl = Mono("drop", 32, color=GREEN).next_to(DROP_END, RIGHT, buff=0.25)
        copy_lbl = T("copy", 30, color=GOLD).next_to(take_lbl, DOWN, buff=0.14, aligned_edge=LEFT)
        skip_lbl = T("skip", 30, color=GREEN).next_to(drop_lbl, DOWN, buff=0.14, aligned_edge=LEFT)
        caption = VGroup(T("O-notation hides constant factors", 34),
                         T("Lecture 2", 30, color=DIM)).arrange(RIGHT, buff=0.5)
        caption[1].align_to(caption[0], DOWN)
        caption.move_to([0, -3.42, 0])

        def glow(line, color):
            return VShowPassingFlash(line.copy().set_stroke(color, width=12), time_width=0.6)

        with self.say("c1.cost.4") as c:
            self.play(FlashAround(t_time, color=GOLD, time_width=1.5),
                      FlashAround(d_time, color=GOLD, time_width=1.5), run_time=1.6)
            c.wait_until("Are they equally fast")
            sweep_clear(self,
                        t_time.animate.move_to(top_t[1]), d_time.animate.move_to(top_d[1]),
                        time_span(FadeIn(top_t[0], shift=0.2 * RIGHT), 0.8, 1.8),
                        time_span(FadeIn(top_d[0], shift=0.2 * RIGHT), 0.8, 1.8),
                        time_span(GrowArrow(x_ax), 0.6, 1.6), time_span(GrowArrow(y_ax), 0.6, 1.6),
                        time_span(FadeIn(i_lbl), 1.1, 1.8), time_span(FadeIn(work), 1.1, 1.8),
                        keep=[t_time, d_time], run_time=1.8)
            c.wait_until("No")
            self.play(Create(take_line), Create(drop_line),
                      time_span(FadeIn(take_lbl, shift=0.2 * LEFT), 0.8, 1.4),
                      time_span(FadeIn(drop_lbl, shift=0.2 * LEFT), 0.8, 1.4),
                      run_time=1.4)
            c.wait_until("Skipping")
            self.play(FadeIn(skip_lbl, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("copying")
            self.play(FadeIn(copy_lbl, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("constant factor is smaller")
            self.play(glow(drop_line, GREEN), FlashAround(VGroup(drop_lbl, skip_lbl), color=GREEN,
                                                          time_width=1.5), run_time=1.5)
            c.wait_until("And as lecture two")
            self.play(FadeIn(caption, shift=0.2 * UP), run_time=1.0)
            c.wait_until("Two functions")
            self.play(FlashAround(t_time, color=GOLD, time_width=1.5),
                      FlashAround(d_time, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("very different speeds")
            self.play(glow(take_line, GOLD), glow(drop_line, GREEN),
                      run_time=min(1.3, max(0.5, c.remaining)))
