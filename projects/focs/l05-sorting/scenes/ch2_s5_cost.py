"""Chapter 2, scene 5: counting insertion sort's comparisons. Clips c2.cost.1 – c2.cost.5.

Plan (v1)
- cost.1: sorted chain 1..10 (ConsCells at pitch 2.0, scaled to 12 wide) with a YELLOW new cell
  hovering; GOLD "? comparisons". ins 0 lands at the far left (1 GOLD tally dot) -> "1 comparison";
  ins 11 walks the whole chain (10 dots) -> "10 comparisons"; a random "?" lands mid-list (5 dots)
  -> "about 5" (the three counts stay to the clip end, earlier ones at 0.45) -> GOLD brace over
  the first half, "about half the list" (copied from "about 5").
- cost.2: staircase (L3 ch4 s6 blocks): rows 0..7 of GOLD blocks, U 0.6, left edge -6.2, top 2.4;
  row counts 0, 1, 2, n-1 at the row ends fly into 0 + 1 + 2 + ... + (n-1) (top right).
  T(n+1) = T(n) + n, with a YELLOW ghost row of n blocks under the staircase.
- cost.3: Lecture 2's table slides in, the recurrence becomes its row 2 (YELLOW, DIM nsumsum);
  = n(n-1)/2, RED O(n^2) from the table. Halving: the right half of every row dims, the sum
  becomes 1/2(...), the closed form becomes ~ n^2/4; RED "quadratic".
- cost.4: n = 10,000; n^2/4 = 25,000,000; insort 25,146,194 (DIM "counted by us: a tallying ≤", the board's tag), GREEN
  tick; ch1's floor "lower bound ≈ 118,458", GOLD arrow "× 212".
- cost.5: ch1's make_scoreboard(bound="118,458") at scale 1 (top at 3.5); the
  count flies into insertion sort's cell, the floor into the board's, "174 s"; one DIM aside line
  under the board: "on a laptop today: insertion sort < 1 s  quicksort < 0.01 s" (OCaml 5.4.1
  toplevel, Apple M1 Max), turning RED / GREEN on {hardware}.
Halved staircase (for s7's recap): rows r = 1..7 of r GOLD squares (side 0.6, fill 0.85, BG stroke
4), left-aligned; the blocks right of r/2 at fill 0.25 (odd rows: a half-width bright block).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402

# ── cost.1: one insert into a sorted chain of ten ─────────────────────────────────────
PITCH = 2.0                 # cell pitch before scaling (ConsChain's is 2.3)
CHAIN_W = 12.0              # chain width on screen, [] included
CHAIN_X, CHAIN_Y = 0.3, 0.9
LABEL_UP = 1.3              # value labels scaled back up after the chain shrinks
DOT_Y = CHAIN_Y - 0.62      # GOLD tally dots, one per comparison
LBL_Y = -2.0                # the GOLD comparison counts, one per insert, kept to the clip end

# ── cost.2 / cost.3: the staircase and its labels ─────────────────────────────────────
NR = 8                      # rows 0..7: inserts into 0, 1, ..., n-1 items
U = 0.6                     # block side
SX, STOP = -6.2, 2.4        # staircase left edge, top edge
XL = -0.5                   # left edge of the right-hand column
Y1, Y1B = 2.75, 1.5         # the sum, the closed form
TY = [0.25, -0.6, -1.45, -2.3]   # Lecture 2's table rows
TAB = 36                    # table font size
EQ_POS = np.array([3.0, -0.6, 0])

# ── cost.4: the measurement ────────────────────────────────────────────────────────────
EQX = -1.0                  # x of the "=" in n^2/4 = 25,000,000
YA, YB, YF = 1.35, -0.3, -2.4
BIG = 60                    # the two numbers
SB_TOP = 3.5                # ch1's scoreboard at scale 1, nudged up to leave a line for the laptop aside
ASIDE_Y = -3.27


def rt(c, cue, cap, frac=0.85, nth=0):
    """A run_time that ends before `cue` (or the clip end for cue=None)."""
    return max(0.3, min(cap, frac * c.until(cue, nth=nth)))


def block(color=GOLD, u=U, op=0.85):
    return Square(u, stroke_color=BG, stroke_width=4, fill_color=color, fill_opacity=op)


def blk_pos(r, j):
    return np.array([SX + (j + 0.5) * U, STOP - (r + 0.5) * U, 0])


def left_at(mob, x, y):
    mob.move_to([0, y, 0])
    return mob.shift(RIGHT * (x - mob.get_left()[0]))


def build_chain():
    """[1; ...; 10] as cons cells, scaled to CHAIN_W; returns (chain, cells, nil, scale)."""
    cells = [ConsCell(v) for v in range(1, 11)]
    for i, cl in enumerate(cells):
        cl.move_to([i * PITCH, 0, 0])
    nil = Nil(size=54)
    nil.next_to(cells[-1], RIGHT, buff=PITCH - 1.5)
    arrows = [link(cells[i], cells[i + 1]) for i in range(9)] + [link(cells[9], nil)]
    parts = []
    for i in range(10):
        parts += [cells[i], arrows[i]]
    chain = VGroup(*parts, nil)
    s = CHAIN_W / chain.width
    chain.scale(s).move_to([CHAIN_X, CHAIN_Y, 0])
    for cl in cells:
        cl.label.scale(LABEL_UP)
    return chain, cells, nil, s


def make_item(v, s):
    it = ConsCell(v, color=YELLOW).scale(s)
    it.label.scale(LABEL_UP)
    return it


def walk_anim(item, x0, x1, y_h, y_l, tw, td):
    """One animation: walk right at hover height (linear), then drop into the slot (smooth)."""
    total = tw + td

    def upd(m, a):
        t = a * total
        if t <= tw:
            m.move_to([x0 + (x1 - x0) * (t / tw if tw > 0 else 1), y_h, 0])
        else:
            m.move_to([x1, y_h + (y_l - y_h) * smooth((t - tw) / td), 0])

    return UpdateFromAlphaFunc(item, upd, run_time=total, rate_func=linear)


def floor_board():
    """ch1's scoreboard as ch1 s6 leaves it (make_scoreboard(bound=...)), top at SB_TOP.
    The floor row is taken out of the group: returns (board, VGroup(label, value, line))."""
    sb = make_scoreboard(bound="118,458")
    floor = VGroup(sb.floor_label, sb.floor_value, sb.floor_line)
    sb.remove(*floor)
    VGroup(sb, floor).shift(UP * (SB_TOP - VGroup(sb, floor).get_top()[1]))
    return sb, floor


def make_floor(x0, x1, y):
    """cost.4's floor, built from the board's own floor pieces: label and value moved to (x0, y),
    the solid line re-cut to end at x1. Same three parts as the board's floor, for the morph."""
    fb = make_scoreboard(bound="118,458")
    lab, val = fb.floor_label, fb.floor_value
    words = VGroup(lab, val)
    words.shift(RIGHT * (x0 - lab.get_left()[0]) + UP * (y - lab.get_y()))
    line = Line([val.get_right()[0] + 0.35, y, 0], [x1, y, 0]).set_stroke(GOLD, 3)
    return VGroup(lab, val, line)


class CountingComparisons(NarratedScene):
    def construct(self):
        self.one_insert()
        self.whole_sort()
        self.the_table()
        self.measure()
        self.scoreboard()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # cost.1: one insert costs 1 to 10 comparisons, about half the list
    def one_insert(self):
        chain, cells, nil, s = build_chain()
        land_y = CHAIN_Y + s + 0.12
        hover_y = land_y + 1.0
        slots = [cells[0].get_left()[0] - 0.12]
        for k in range(1, 11):
            nxt = cells[k] if k < 10 else nil
            slots.append((cells[k - 1].get_right()[0] + nxt.get_left()[0]) / 2)
        dots = [Dot(radius=0.09, color=GOLD).move_to([cl.label.get_x(), DOT_Y, 0]) for cl in cells]

        def walk(item, k, tw, td):
            """Animations for walking `item` to slot k: one tally dot per comparison (cells 0..k)."""
            x0, x1 = slots[0], slots[k]
            anims = [walk_anim(item, x0, x1, hover_y, land_y, tw, td)]
            for j in range(min(k + 1, 10)):
                tj = tw * max(0.0, (cells[j].label.get_x() - x0) / (x1 - x0)) if j < k else tw
                anims.append(time_span(FadeIn(dots[j], scale=0.5), min(tj, tw), min(tj, tw) + 0.25))
            if k < 10:      # the cell it stops in front of
                anims.append(time_span(FlashAround(cells[k], color=YELLOW, time_width=1.5), tw, tw + td + 0.3))
            return anims, tw + td + (0.3 if k < 10 else 0.0)

        with self.say("c2.cost.1") as c:
            # the sorted chain, a new item above it, and the question
            item = make_item(0, s).move_to([slots[0], hover_y, 0])
            q = T("? comparisons", size=40, color=GOLD).move_to([CHAIN_X, LBL_Y, 0])
            t = rt(c, "ten", 2.2, frac=0.92)
            self.play(FadeIn(chain, lag_ratio=0.06, run_time=0.7 * t),
                      time_span(FadeIn(item, shift=0.3 * DOWN), 0.45 * t, t),
                      time_span(FadeIn(q, shift=0.2 * DOWN), 0.6 * t, t))

            # ins 0: it belongs at the head, one comparison
            c.wait_until("ten")
            t = rt(c, "one comparison", 1.4)
            self.play(time_span(item.animate.move_to([slots[0], land_y, 0]), 0, 0.7 * t),
                      time_span(FadeIn(dots[0], scale=0.5), 0.6 * t, t),
                      time_span(FlashAround(cells[0], color=YELLOW, time_width=1.5), 0.5 * t, t))
            c.wait_until("one comparison")
            lab = left_at(T("1 comparison", size=40, color=GOLD), chain.get_left()[0], LBL_Y)
            self.play(TransformMatchingStrings(q, lab, run_time=rt(c, "to ten", 0.9, frac=0.95)))

            # ins 11: it walks past every cell, ten comparisons
            c.wait_until("to ten")
            item2 = make_item(11, s).move_to([slots[0], hover_y, 0])
            self.play(FadeOut(item, shift=0.3 * UP), FadeOut(dots[0]), FadeIn(item2, shift=0.3 * DOWN),
                      run_time=0.6)
            avail = c.until("half") - 0.2
            tw = max(0.8, min(1.7, 0.55 * avail))
            td = max(0.3, min(0.5, 0.15 * avail))
            anims, tend = walk(item2, 10, tw, td)
            lab10 = T("10 comparisons", size=40, color=GOLD).move_to([0, LBL_Y, 0])
            lab10.align_to(chain, RIGHT)
            tl = min(0.8, max(0.3, avail - tend - 0.1))
            anims += [time_span(FadeIn(lab10, shift=0.3 * DOWN), tend, tend + tl),
                      time_span(restyle(lab, op=0.45), tend, tend + tl)]
            self.play(*anims)

            # a random item lands somewhere in the middle: about five
            c.wait_until("half")
            item3 = make_item("?", s).move_to([slots[0], hover_y, 0])
            self.play(FadeOut(item2, shift=0.3 * UP), *[FadeOut(d) for d in dots],
                      FadeIn(item3, shift=0.3 * DOWN), run_time=0.7)
            anims, tend = walk(item3, 4, 1.0, 0.5)
            lab5 = T("about 5", size=40, color=GOLD).move_to([CHAIN_X, LBL_Y, 0])
            anims += [time_span(FadeIn(lab5, shift=0.3 * DOWN), tend, tend + 0.8),
                      time_span(restyle(lab10, op=0.45), tend, tend + 0.8)]
            self.play(*anims)

            # in general: about half the list
            c.wait_until("In general")
            brace = span_brace([cells[0].get_left()[0], DOT_Y, 0], [cells[4].get_right()[0], DOT_Y, 0],
                               DOWN, color=GOLD, buff=0.22)
            half = T("about half the list", size=40, color=GOLD).next_to(brace, DOWN, buff=0.18)
            self.play(GrowFromCenter(brace), TransformFromCopy(lab5, half), run_time=rt(c, None, 1.4))

    # cost.2: the whole sort is a staircase; T(n+1) = T(n) + n
    def whole_sort(self):
        rows = {r: VGroup(*[block().move_to(blk_pos(r, j)) for j in range(r)]) for r in range(1, NR)}
        rl = {r: MathTex(tx, font_size=36) for r, tx in [(0, "0"), (1, "1"), (2, "2"), (NR - 1, "n-1")]}
        rl[0].move_to(blk_pos(0, 0))
        for r in (1, 2, NR - 1):
            rl[r].next_to(rows[r], RIGHT, buff=0.22)
        total = MathTex("0", "+", "1", "+", "2", "+", r"\cdots", "+", "(n-1)", font_size=44)
        left_at(total, XL, Y1)
        eq = MathTex("T(n+1)", "=", "T(n)", "+", "n", font_size=48).move_to(EQ_POS)
        ghost = VGroup(*[Square(U, stroke_color=YELLOW, stroke_width=3, fill_color=YELLOW, fill_opacity=0.15)
                         .move_to(blk_pos(NR, j)) for j in range(NR)])
        ghost_n = MathTex("n", font_size=36, color=YELLOW).next_to(ghost, RIGHT, buff=0.22)

        with self.say("c2.cost.2") as c:
            sweep_clear(self, run_time=rt(c, "zero items", 1.2))

            # inserts into 0, 1, 2, ... items
            c.wait_until("zero items")
            self.play(FadeIn(rl[0], shift=0.3 * DOWN), run_time=rt(c, "then one", 0.8))
            c.wait_until("then one")
            self.play(GrowFromEdge(rows[1], LEFT), FadeIn(rl[1], shift=0.3 * LEFT), run_time=rt(c, "then two", 0.9))
            c.wait_until("then two")
            self.play(GrowFromEdge(rows[2], LEFT), FadeIn(rl[2], shift=0.3 * LEFT), run_time=rt(c, "and so on", 0.9))
            c.wait_until("and so on")
            t = rt(c, "worst", 1.8)
            self.play(*[time_span(GrowFromEdge(rows[r], LEFT), 0.12 * t * (r - 3), 0.12 * t * (r - 3) + 0.5 * t)
                        for r in range(3, NR)],
                      time_span(FadeIn(rl[NR - 1], shift=0.3 * LEFT), 0.6 * t, t))

            # at worst, each insert walks the whole list
            c.wait_until("worst")
            t = rt(c, "add up", 1.8)
            flashes = []
            for r in range(1, NR):
                path = Line(rows[r].get_left(), rows[r].get_right()).set_stroke(YELLOW, 8)
                t0 = 0.08 * t * (r - 1)
                flashes.append(time_span(VShowPassingFlash(path, time_width=0.6), t0, t0 + 0.45 * t))
            self.play(*flashes)

            # 0 + 1 + 2 + ... + (n - 1), the row counts flying up into the sum
            c.wait_until("add up")
            t = rt(c, "eq", 2.2)
            src = {0: 0, 2: 1, 4: 2, 8: NR - 1}
            anims = []
            for i, part in enumerate(total):
                t0 = 0.1 * t * i
                a = TransformFromCopy(rl[src[i]], part) if i in src else FadeIn(part)
                anims.append(time_span(a, t0, t0 + 0.2 * t + (0.25 * t if i in src else 0)))
            self.play(*anims)
            settle(self, total)

            # as a recurrence
            c.wait_until("eq")
            self.play(Write(eq), run_time=rt(c, "adds at most", 1.5))
            c.wait_until("adds at most")
            self.play(GrowFromEdge(ghost, LEFT), FadeIn(ghost_n, shift=0.3 * LEFT), run_time=rt(c, "Tee of N", 1.4))
            c.wait_until("Tee of N")
            self.play(*recolor(eq[3:], YELLOW), FlashAround(eq[3:], color=YELLOW, time_width=1.5),
                      run_time=rt(c, None, 1.4))

        self.rows, self.rl, self.total, self.eq, self.ghost, self.ghost_n = rows, rl, total, eq, ghost, ghost_n

    # cost.3: Lecture 2's table; n(n-1)/2; halved on average; quadratic
    def the_table(self):
        rows, total, eq = self.rows, self.total, self.eq
        lhs = [MathTex(r"T(n+1) = T(n) + 1", font_size=TAB), None,
               MathTex(r"T(n) = T(n/2) + 1", font_size=TAB), MathTex(r"T(n) = 2T(n/2) + n", font_size=TAB)]
        os_ = [MathTex(tx, font_size=TAB) for tx in ("O(n)", "O(n^2)", r"O(\log n)", r"O(n\log n)")]
        eq_t = eq.copy().scale(TAB / 48)
        left_at(eq_t, XL, TY[1])
        xc2 = XL + max(eq_t.width, *[m.width for m in lhs if m is not None]) + 0.6
        for i in range(4):
            if lhs[i] is not None:
                left_at(lhs[i], XL, TY[i])
            left_at(os_[i], xc2, TY[i])
        tag = Mono("nsumsum", size=28, color=DIM).next_to(os_[1], RIGHT, buff=0.35)
        closed = MathTex("=", r"\frac{n(n-1)}{2}", font_size=44)
        left_at(closed, XL + 0.4, Y1B)
        o_red = MathTex("O(n^2)", font_size=44, color=RED).next_to(closed, RIGHT, buff=0.8)
        half_l = MathTex(r"\tfrac{1}{2}\Big(", font_size=44)
        half_r = MathTex(r"\Big)", font_size=44)
        left_at(half_l, XL, Y1)
        avg = MathTex(r"\approx", r"\frac{n^2}{4}", font_size=44)
        left_at(avg, XL + 0.4, Y1B)
        quad = T("quadratic", size=40, color=RED)

        with self.say("c2.cost.3") as c:
            # a row of Lecture 2's table
            t = rt(c, "the one for", 1.6)
            incoming = [m for m in lhs if m is not None] + os_
            self.play(FadeOut(self.ghost), FadeOut(self.ghost_n),
                      eq.animate.scale(TAB / 48).move_to(eq_t),
                      *[time_span(FadeIn(m, shift=0.6 * LEFT), 0.25 * t + 0.06 * t * i, 0.65 * t + 0.06 * t * i)
                        for i, m in enumerate(incoming)])
            c.wait_until("the one for")
            self.play(eq.animate.set_color(YELLOW), os_[1].animate.set_color(YELLOW),
                      FadeIn(tag, shift=0.3 * LEFT), run_time=rt(c, "closed", 1.0))

            # it adds up to n(n-1)/2: O(n^2)
            c.wait_until("closed")
            self.play(Write(closed), run_time=rt(c, "Big O", 1.5))
            c.wait_until("Big O")
            self.play(TransformFromCopy(os_[1], o_red), run_time=rt(c, "average", 1.3))

            # on average each insert does half that work
            c.wait_until("average")
            dx = half_l.get_right()[0] + 0.06 - total.get_left()[0]
            half_r.next_to(total.copy().shift(RIGHT * dx), RIGHT, buff=0.06)
            half_r.set_y(total.get_y())
            half_l.set_y(total.get_y())
            table = [m for m in lhs if m is not None] + os_ + [eq, tag]
            self.play(*set_alpha(table, DIMMED), total.animate.shift(RIGHT * dx),
                      FadeIn(half_l), FadeIn(half_r), run_time=rt(c, "half that work", 1.3))
            c.wait_until("half that work")
            t = rt(c, "about N squared", 2.2)
            anims, overlays = [], []
            for r in range(1, NR):
                t0 = 0.07 * t * (r - 1)
                t1 = t0 + 0.55 * t
                for j, b in enumerate(rows[r]):
                    if j + 1 <= r / 2:
                        continue
                    if j < r / 2:       # odd row: the middle block keeps its left half
                        ov = Rectangle(width=U / 2, height=U, stroke_color=BG, stroke_width=0,
                                       fill_color=GOLD, fill_opacity=0.85)
                        ov.move_to(b).align_to(b, LEFT)
                        overlays.append(ov)
                        anims.append(time_span(ov.animate.set_stroke(width=4), t0, t1))
                    anims.append(time_span(restyle(b, op=DIMMED), t0, t1))
            self.add(*overlays)
            self.play(*anims)

            # about n^2 / 4
            c.wait_until("about N squared")
            o_to = o_red.copy().next_to(avg, RIGHT, buff=0.8)
            self.play(ReplacementTransform(closed[0], avg[0]), ReplacementTransform(closed[1], avg[1]),
                      o_red.animate.move_to(o_to), run_time=rt(c, "quad", 1.4))
            self.remove(*closed.get_family())
            settle(self, avg)

            # still O(n^2): quadratic
            c.wait_until("quad")
            quad.next_to(o_to, RIGHT, buff=0.45).align_to(o_to, DOWN)
            self.play(FlashAround(o_red, color=RED, time_width=1.5),
                      time_span(FadeIn(quad, shift=0.3 * LEFT), 0.5, 1.4), run_time=1.5)
            c.wait_until("quadratic")
            self.play(FlashUnder(quad, color=RED, time_width=1.5), run_time=rt(c, None, 1.2))

        self.avg = avg

    # cost.4: 10,000 random numbers: 25,146,194 comparisons, 212 times the floor
    def measure(self):
        avg = self.avg
        n_eq = MathTex(r"n = 10{,}000", font_size=56).move_to([0.2, 2.75, 0])
        row_a = MathTex(r"\frac{n^2}{4}", "=", r"25{,}000{,}000", font_size=BIG, color=GOLD)
        row_a.shift(RIGHT * (EQX - row_a[1].get_x()) + UP * (YA - row_a[1].get_y()))
        num_b = MathTex(r"25{,}146{,}194", font_size=BIG, color=GOLD)
        left_at(num_b, row_a[2].get_left()[0], YB)
        ins = Mono("insort", size=44, color=YELLOW)
        ins.move_to([0, YB, 0]).align_to(row_a[0], RIGHT)
        cap = T("counted by us: a tallying ≤", size=30, color=DIM).next_to(num_b, DOWN, buff=0.3)
        tick = check_mark().next_to(num_b, RIGHT, buff=0.4)
        ax = tick.get_right()[0] + 0.7
        floor = make_floor(-5.0, ax + 0.35, YF)
        arrow = Arrow([ax, YF + 0.05, 0], [ax, YB - 0.1, 0], buff=0.1, stroke_width=5, color=GOLD,
                      max_tip_length_to_length_ratio=0.15)
        times = T("× 212", size=44, color=GOLD).next_to(arrow, RIGHT, buff=0.2)

        with self.say("c2.cost.4") as c:
            c.wait_until("ten thousand")
            t = rt(c, "predict", 1.5)
            sweep_clear(self, time_span(FadeIn(n_eq, shift=0.3 * DOWN), 0.5 * t, t), keep=[avg], run_time=t)

            # the formula predicts 25,000,000
            c.wait_until("predict")
            t = rt(c, "count", 1.8)
            self.play(ReplacementTransform(avg[1], row_a[0]), FadeOut(avg[0]),
                      time_span(FadeIn(row_a[1:], shift=0.3 * LEFT), 0.45 * t, t), run_time=t)
            self.remove(*avg.get_family())
            settle(self, row_a)

            # counted with a tallying <=: 25,146,194
            c.wait_until("count")
            self.play(FadeIn(ins, shift=0.3 * RIGHT), FadeIn(cap, shift=0.2 * UP), run_time=rt(c, "makes", 1.2))
            c.wait_until("makes")
            self.play(Write(num_b), run_time=rt(c, "very close", 2.0))
            c.wait_until("very close")
            self.play(FadeIn(tick, scale=0.5), run_time=rt(c, "floor", 0.8))

            # 212 times ch1's floor
            c.wait_until("floor")
            self.play(FadeIn(floor, shift=0.3 * UP, run_time=0.9), time_span(GrowArrow(arrow), 0.5, 1.5),
                      time_span(FadeIn(times, shift=0.3 * DOWN), 0.8, 1.6))

        self.num_b, self.floor = num_b, floor

    # cost.5: the scoreboard row, and today's laptop
    def scoreboard(self):
        sb, sb_floor = floor_board()
        cells = sb.cells
        val = T("25,146,194", size=44, color=GOLD).move_to(cells[0][0])
        secs = T("174 s", size=44, color=GOLD).move_to(cells[0][1])
        head = T("on a laptop today:", size=30, color=DIM)
        a_ins = T("insertion sort < 1 s", size=30, color=DIM)
        a_qs = T("quicksort < 0.01 s", size=30, color=DIM)
        aside = VGroup(head, a_ins, a_qs).arrange(RIGHT, buff=0.35)
        a_qs.shift(RIGHT * 0.35)
        aside.move_to([0, ASIDE_Y, 0])

        with self.say("c2.cost.5") as c:
            sweep_clear(self, time_span(FadeIn(sb), 0.4, 1.3), keep=[self.num_b, self.floor], run_time=1.3)
            t = rt(c, "secs", 1.6)
            self.play(ReplacementTransform(self.num_b, val), FadeOut(cells[0][0]),
                      ReplacementTransform(self.floor, sb_floor), run_time=t)

            # 174 s on the DECstation
            c.wait_until("it took")
            self.play(ReplacementTransform(cells[0][1], secs), run_time=rt(c, "nearly", 1.2))

            # beyond the notes: today's laptop
            c.wait_until("laptop")
            self.play(FadeIn(head, shift=0.2 * UP), FadeIn(a_ins, shift=0.2 * UP), run_time=rt(c, "quick", 1.2))
            c.wait_until("quick")
            self.play(FadeIn(a_qs, shift=0.3 * LEFT), run_time=rt(c, "hardware", 1.0))

            # faster hardware magnifies the gap
            c.wait_until("hardware")
            self.play(a_ins.animate.set_color(RED), a_qs.animate.set_color(GREEN),
                      FlashAround(a_qs, color=GREEN, time_width=1.5), run_time=rt(c, None, 1.5))
