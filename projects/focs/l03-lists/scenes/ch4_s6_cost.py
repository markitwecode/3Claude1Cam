"""Chapter 4, scene 6: counting the cost of nrev. Clips c4.cost.1 - c4.cost.5 (music bed under it).

STATUS: built (all five clips). Opens on s5's last shot, `(([] @ [3]) @ [2]) @ [1]` (Code 50, centred (0, 2.9), @ GOLD).
Blocks: Square, fill 0.85, BG stroke; GOLD = copied cons, YELLOW = built by `[x]`.
- cost.1: top line + GOLD box sliding over each @'s left argument; table rows `[] @ [3]`, `[3] @ [2]`, `[3; 2] @ [1]`
  (Code 40, right-aligned at x -1.45) with their result blocks (U 0.85) and a GOLD copy count 0 / 1 / 2;
  {singles} YELLOW blocks fly from `[3]`, `[2]`, `[1]`; {total} "3 copied", "3 built", "6 conses".
- cost.2: row 3 carries over: code -> `(nrev xs) @ [x]` (Code 52, top), blocks -> hero row 6 GOLD + 1 YELLOW;
  braces n - 1 (GOLD) and 1 (YELLOW) merge into n; GOLD `n, n-1, ..., 2, 1, 0`; sum `0 + 1 + 2 + ... + n` term by term.
- cost.3 (v1 s6_nrev.triangle geometry, N = 7, U 0.65): hero row -> staircase bottom row, rows born from the sum's
  terms; BLUE twin, flip, slot, rectangle, braces n and n + 1; twin dims; `= n(n+1)/2` built from the brace labels.
- cost.4: RED O(n^2) from the formula; smooth GOLD triangle, n = 1,000, "500,500 conses" vs GREEN answer bar.
- cost.5: GOLD space O(n); ghost staircase; rows relight one by one, each copied from the one above, which fades
  back to a ghost ("no longer needed"); the bottom row (the answer) stays lit. Ends on an empty frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── cost.1: the last trace line and the per-append table ──────────────────────────────
TOP_SRC = "(([] @ [3]) @ [2]) @ [1]"
TOP_SIZE, TOP_Y = 50, 2.9                 # s5's last shot (continuity): Code 50 at (0, 2.9)
ROW_SRC = ["[] @ [3]", "[3] @ [2]", "[3; 2] @ [1]"]
ROW_SIZE = 40
ROW_Y = [0.9, -0.55, -2.0]
CODE_R = -1.45                            # right edge of the table's code column
U1, BX = 0.85, -0.85                      # table block side, left edge of the first block
COUNT_X = 2.4                             # GOLD copy-count column
SUM_X = 3.4                               # left edge of the tally

# ── cost.2: the general case ─────────────────────────────────────────────────────────
HERO_Y = 1.25

# ── cost.3: staircase geometry (archive v1 s6_nrev): rows 1..N inside an N x (N+1) rectangle
N = 7
U = 0.65                  # block side
L, TOP = -4.6, 3.0       # rectangle's left edge and top edge
W, H = N * U, N * U       # staircase (rows 1..N) width and height
D = 5.15                  # how far right the twin first appears
DROP = 0.5                # ...and how far down (its flip then clears the sum above it)
RX = 3.45                 # centre of the right-hand column (formula, O(...), labels)


def gold_at(code):
    for g in chars(code, "@"):
        g.set_color(GOLD)
    return code


def left_at(mob, x, y):
    mob.move_to([0, y, 0])
    return mob.shift(RIGHT * (x - mob.get_left()[0]))


def block(color, u=U, value=None, op=0.85):
    sq = Square(u, stroke_color=BG, stroke_width=4, fill_color=color, fill_opacity=op)
    if value is None:
        return sq
    return VGroup(sq, Mono(str(value), size=40, color=BG).move_to(sq))


def table_block(row, j, color, value):
    return block(color, U1, value).move_to([BX + (j + 0.5) * U1, ROW_Y[row], 0])


def row_pos(r, j):
    return np.array([L + (j + 0.5) * U, TOP - (r + 0.5) * U, 0])


def stair_row(r, op=0.85):
    """Row r of the staircase: r - 1 copied (GOLD) blocks, then the one built by [x] (YELLOW)."""
    return VGroup(*[block(GOLD if j < r - 1 else YELLOW, U, op=op).move_to(row_pos(r, j))
                    for j in range(r)])


def stair_polygon(steps, **kw):
    """Outline of a staircase with `steps` steps filling the same box as rows 1..N."""
    top, w, h = TOP - U, W / steps, H / steps
    pts = [[L, top, 0]]
    for i in range(1, steps + 1):
        pts += [[L + i * w, top - (i - 1) * h, 0], [L + i * w, top - i * h, 0]]
    pts.append([L, top - H, 0])
    return Polygon(*pts, **kw)


def rt(c, cue, cap, frac=0.85, nth=0):
    """A run_time that ends before `cue` (or the clip end for cue=None)."""
    return max(0.3, min(cap, frac * c.until(cue, nth=nth)))


class CountingTheCost(NarratedScene):
    def construct(self):
        self.count_three()
        self.general()
        self.staircase()
        self.quadratic()
        self.space()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # cost.1: count the conses in (([] @ [3]) @ [2]) @ [1]
    def count_three(self):
        top = gold_at(Code(TOP_SRC, size=TOP_SIZE)).move_to([0, TOP_Y, 0])
        rc = [gold_at(Code(s, size=ROW_SIZE)) for s in ROW_SRC]
        for i, code in enumerate(rc):
            code.move_to([0, ROW_Y[i], 0])
            code.shift(RIGHT * (CODE_R - code.get_right()[0]))
        cnt = [MathTex(str(i), font_size=52, color=GOLD).move_to([COUNT_X, ROW_Y[i], 0]) for i in range(3)]
        g2 = table_block(1, 0, GOLD, 3)
        g3 = [table_block(2, 0, GOLD, 3), table_block(2, 1, GOLD, 2)]
        ys = [table_block(0, 0, YELLOW, 3), table_block(1, 1, YELLOW, 2), table_block(2, 2, YELLOW, 1)]
        lab_cp = left_at(T("3 copied", size=36, color=GOLD), SUM_X, 0.3)
        lab_bt = left_at(T("3 built", size=36, color=YELLOW), SUM_X, -0.4)
        rule = Line([SUM_X, -0.9, 0], [SUM_X + 2.3, -0.9, 0], stroke_width=2, color=DIM)
        six = left_at(T("6 conses", size=44, color=GOLD), SUM_X, -1.45)

        with self.say("c4.cost.1") as c:
            self.play(FadeIn(top), run_time=1.0)
            c.wait_until("last line")
            self.play(FlashUnder(top, color=YELLOW, run_time=rt(c, "inner", 1.5)))

            # innermost: [] @ [3] copies nothing
            c.wait_until("inner")
            box = token_box(top.find("[]"), top, color=GOLD)
            self.play(FadeIn(box), TransformFromCopy(top.find("[] @ [3]"), rc[0]),
                      run_time=rt(c, "copies nothing", 1.5))
            c.wait_until("copies nothing")
            self.play(FadeIn(cnt[0], shift=0.3 * DOWN), run_time=0.8)

            # middle: copies [3], one cell
            c.wait_until("middle")
            self.play(Transform(box, token_box(top.find("([] @ [3])"), top, color=GOLD)),
                      FadeIn(rc[1], shift=0.3 * DOWN), run_time=rt(c, "a single cell", 1.3))
            c.wait_until("a single cell")
            self.play(TransformFromCopy(rc[1].find("[3]"), g2), FadeIn(cnt[1], shift=0.3 * DOWN),
                      run_time=rt(c, "outer", 1.3))

            # outer: copies [3; 2], two cells
            c.wait_until("outer")
            self.play(Transform(box, token_box(top.find("(([] @ [3]) @ [2])"), top, color=GOLD)),
                      FadeIn(rc[2], shift=0.3 * DOWN), run_time=rt(c, "two cells", 1.3))
            c.wait_until("two cells")
            self.play(TransformFromCopy(rc[2].find("3"), g3[0]), TransformFromCopy(rc[2].find("2"), g3[1]),
                      FadeIn(cnt[2], shift=0.3 * DOWN), run_time=rt(c, "singles", 1.4))

            # each [x] is one cons to build
            c.wait_until("singles")
            srcs = [top.find("[3]"), top.find("[2]"), top.find("[1]")]
            self.play(time_span(FadeOut(box), 0, 0.8),
                      *[time_span(TransformFromCopy(s, y), 0.3 * i, 0.3 * i + 1.4) for i, (s, y) in
                        enumerate(zip(srcs, ys))], run_time=2.0)

            # tally
            c.wait_until("total")
            self.play(TransformFromCopy(VGroup(*cnt), lab_cp), run_time=rt(c, "three for building", 1.3))
            c.wait_until("three for building")
            self.play(TransformFromCopy(VGroup(*ys), lab_bt), run_time=rt(c, "six in all", 1.3))
            c.wait_until("six in all")
            self.play(Create(rule), TransformFromCopy(VGroup(lab_cp, lab_bt), six), run_time=1.5)
            self.wait(0.3)
            self.play(FlashAround(six, color=GOLD, run_time=rt(c, None, 1.5)))

        self.row3 = (rc[2], g3[0], g3[1], ys[2], six)

    # cost.2: n elements: n - 1 copied + 1 built at the top, then n - 1, ..., 0
    def general(self):
        code3, g_a, g_b, y_c, six = self.row3
        gen = gold_at(Code("(nrev xs) @ [x]", size=52)).move_to([0, TOP_Y, 0])
        hero = VGroup(*[block(GOLD if i < 6 else YELLOW, U1) for i in range(7)]).arrange(RIGHT, buff=0)
        hero.move_to([0, HERO_Y, 0])
        b1 = span_brace(hero[0].get_corner(DL), hero[5].get_corner(DR), DOWN, color=GOLD)
        l1 = MathTex("n - 1", font_size=48, color=GOLD).next_to(b1, DOWN, buff=0.12)
        b2 = span_brace(hero[6].get_corner(DL), hero[6].get_corner(DR), DOWN, color=YELLOW)
        l2 = MathTex("1", font_size=48, color=YELLOW).next_to(b2, DOWN, buff=0.12)
        bn = span_brace(hero[0].get_corner(DL), hero[6].get_corner(DR), DOWN, color=FG)
        ln = MathTex("n", font_size=48).next_to(bn, DOWN, buff=0.12)
        seq = MathTex("n", r",\;", "n-1", r",\;", r"\dots", r",\;", "2", r",\;", "1", r",\;", "0",
                      font_size=56, color=GOLD).move_to([0, -1.05, 0])
        sm = MathTex("0", "+", "1", "+", "2", "+", r"\cdots", "+", "n", font_size=60, color=GOLD)
        sm.move_to([0, -2.55, 0])

        with self.say("c4.cost.2") as c:
            # values fade first (no morphing digits), then the three squares become hero cells
            sweep_clear(self, FadeTransform(code3, gen),
                        *[time_span(FadeOut(b[1]), 0, 0.5) for b in (g_a, g_b, y_c)],
                        ReplacementTransform(g_a[0], hero[0]), ReplacementTransform(g_b[0], hero[1]),
                        *[time_span(FadeIn(hero[i], scale=0.6), 0.5 + 0.15 * (i - 2), 1.3 + 0.15 * (i - 2))
                          for i in range(2, 6)],
                        ReplacementTransform(y_c[0], hero[6]),
                        keep=[code3, g_a, g_b, y_c, six], run_time=2.2)
            settle(self, hero)

            # append copies the reversed tail: n - 1
            c.wait_until("copy")
            box = token_box(gen.find("(nrev xs)"), gen, color=GOLD)
            self.play(FadeIn(box), FadeOut(six), run_time=0.8)
            c.wait_until("en minus one")
            self.play(GrowFromCenter(b1), FadeIn(l1, shift=0.3 * DOWN), run_time=rt(c, "single", 1.2))

            # [x] is one more
            c.wait_until("single")
            self.play(Transform(box, token_box(gen.find("[x]"), gen, color=YELLOW)),
                      GrowFromCenter(b2), FadeIn(l2, shift=0.3 * DOWN), run_time=rt(c, "en in total", 1.3))
            c.wait_until("en in total")
            bn_dup, ln_dup = bn.copy(), ln.copy()
            self.play(ReplacementTransform(b1, bn), ReplacementTransform(b2, bn_dup),
                      ReplacementTransform(l1, ln), ReplacementTransform(l2, ln_dup),
                      run_time=rt(c, "down", 1.5))
            self.remove(bn_dup, ln_dup)

            # n, n - 1, ..., 0
            c.wait_until("down")
            self.play(FadeOut(box), TransformFromCopy(ln, seq[0]), run_time=rt(c, "en minus one", 1.0, nth=1))
            c.wait_until("en minus one", nth=1)
            self.play(FadeIn(seq[1]), FadeIn(seq[2], shift=0.2 * RIGHT), run_time=rt(c, "and so on", 0.8))
            c.wait_until("and so on")
            self.play(*[time_span(FadeIn(seq[k], shift=0.2 * RIGHT), 0.12 * (k - 3), 0.12 * (k - 3) + 0.5)
                        for k in range(3, 9)], run_time=1.1)
            c.wait_until("costs nothing")
            self.play(FadeIn(seq[9]), FadeIn(seq[10], shift=0.2 * RIGHT), run_time=rt(c, "sum", 0.8))
            settle(self, seq)

            # 0 + 1 + 2 + ... + n, each term from its number
            c.wait_until("sum")
            c.wait_until("zero")
            self.play(TransformFromCopy(seq[10], sm[0]), run_time=rt(c, "plus one", 0.9))
            steps = [("plus one", 0, 1, 2, 8), ("plus two", 0, 3, 4, 6), ("and so on", 1, 5, 6, 4),
                     ("up to en", 0, 7, 8, 0)]
            for k, (cue, nth, plus, term, src) in enumerate(steps):
                c.wait_until(cue, nth=nth)
                nxt = steps[k + 1] if k + 1 < len(steps) else None
                lim = rt(c, nxt[0], 0.8, nth=nxt[1]) if nxt else rt(c, None, 1.0)
                self.play(FadeIn(sm[plus]), TransformFromCopy(seq[src], sm[term]), run_time=lim)
            settle(self, sm)

        self.gen, self.hero, self.bn, self.ln, self.seq, self.sm = gen, hero, bn, ln, seq, sm

    # cost.3: the staircase is half an n x (n + 1) rectangle
    def staircase(self):
        gen, hero, bn, ln, seq, sm = self.gen, self.hero, self.bn, self.ln, self.seq, self.sm
        rows = {r: stair_row(r) for r in range(1, N)}
        bot_l, bot_r = [L, TOP - (N + 1) * U, 0], [L + W, TOP - (N + 1) * U, 0]
        bn3 = span_brace(bot_l, bot_r, DOWN, color=FG)
        outline = stair_polygon(N, stroke_color=YELLOW, stroke_width=6, fill_opacity=0)
        rect = Rectangle(width=W, height=(N + 1) * U, stroke_color=FG, stroke_width=4)
        rect.move_to([L + W / 2, TOP - (N + 1) * U / 2, 0])
        brace_h = Brace(rect, LEFT, buff=0.15, color=FG)
        lab_h = MathTex("n + 1", font_size=44).next_to(brace_h, LEFT, buff=0.15)
        eq = MathTex("=", font_size=56)
        num = MathTex("n", "(n+1)", font_size=56)
        bar = Line(LEFT, RIGHT, stroke_width=3, color=FG).set_width(num.width + 0.15)
        den = MathTex("2", font_size=56)
        frac = VGroup(num, bar, den).arrange(DOWN, buff=0.12)
        rhs = VGroup(eq, frac).arrange(RIGHT, buff=0.25).move_to([RX, 0.4, 0])
        eq.set_y(bar.get_y())

        with self.say("c4.cost.3") as c:
            self.play(FadeOut(gen), FadeOut(seq), run_time=0.8)
            self.play(hero.animate.scale(U / U1).move_to([L + W / 2, TOP - (N + 0.5) * U, 0]),
                      ReplacementTransform(bn, bn3), ln.animate.next_to(bn3, DOWN, buff=0.12),
                      sm.animate.scale(44 / 60).move_to([3.2, 3.38, 0]), run_time=rt(c, "draw each step", 1.6))

            # zero, then one, then two, ..., up to n
            c.wait_until("stair")
            self.play(FlashAround(sm[0], color=YELLOW, run_time=rt(c, "then one", 0.9)))
            c.wait_until("then one")
            self.play(TransformFromCopy(sm[2], rows[1]), run_time=rt(c, "then two", 0.8))
            c.wait_until("then two")
            self.play(TransformFromCopy(sm[4], rows[2]), run_time=rt(c, "all the way", 0.8))
            c.wait_until("all the way")
            t = rt(c, "a staircase", 1.4, frac=0.9)
            self.play(*[time_span(TransformFromCopy(sm[6], rows[r]), 0.15 * t * (r - 3), 0.15 * t * (r - 3) + 0.55 * t)
                        for r in range(3, N)], run_time=t)
            stair = VGroup(*[rows[r] for r in range(1, N)], hero)
            settle(self, stair)
            c.wait_until("a staircase")
            self.play(VShowPassingFlash(outline, time_width=0.6), run_time=rt(c, "twin", 1.3))

            # a second copy, flipped over, slots in
            c.wait_until("twin")
            twin = stair.copy().set_fill(BLUE).shift(RIGHT * D + DOWN * DROP)
            self.play(TransformFromCopy(stair, twin), run_time=rt(c, "flip", 1.2))
            c.wait_until("flip")
            self.play(Rotate(twin, PI), run_time=rt(c, "slot", 0.9, frac=0.95))
            c.wait_until("slot")
            self.play(twin.animate.shift(LEFT * D + UP * (U + DROP)), run_time=rt(c, "rect", 1.2))
            c.wait_until("rect")
            self.play(Create(rect), run_time=rt(c, "wide", 1.0))
            c.wait_until("wide")
            self.play(FlashAround(VGroup(bn3, ln), color=YELLOW, run_time=rt(c, "tall", 0.9, frac=0.95)))
            c.wait_until("tall")
            self.play(GrowFromCenter(brace_h), FadeIn(lab_h, shift=0.3 * RIGHT), run_time=rt(c, "half", 1.0))

            # the staircase is half of it
            c.wait_until("half")
            self.play(twin.animate.set_fill(opacity=0.2), sm.animate.scale(52 / 44).move_to([RX, 1.85, 0]),
                      run_time=rt(c, "formula", 1.3))

            # n (n + 1) / 2, built from the brace labels
            c.wait_until("formula")
            self.play(FadeIn(eq), TransformFromCopy(ln, num[0]), run_time=rt(c, "en plus one", 1.0, nth=1))
            c.wait_until("en plus one", nth=1)
            self.play(TransformFromCopy(lab_h, num[1]), run_time=rt(c, "over two", 1.0))
            c.wait_until("over two")
            self.play(GrowFromCenter(bar), FadeIn(den, shift=0.2 * UP), run_time=rt(c, None, 0.8))
            settle(self, rhs)

        self.stair, self.twin, self.rect, self.brace_h, self.lab_h = stair, twin, rect, brace_h, lab_h
        self.bn3, self.rhs, self.num = bn3, rhs, num

    # cost.4: O(n^2); a thousand elements -> half a million conses
    def quadratic(self):
        stair, bn3, ln, rhs, num = self.stair, self.bn3, self.ln, self.rhs, self.num
        time_row = VGroup(T("time", size=36, color=DIM), MathTex("O(n^2)", font_size=60, color=RED))
        time_row.arrange(RIGHT, buff=0.3).move_to([RX, -1.3, 0])
        steps = 60
        smooth = stair_polygon(steps, stroke_width=0, fill_color=GOLD, fill_opacity=0.85)
        lab_1000 = MathTex(r"n = 1{,}000", font_size=44).next_to(bn3, DOWN, buff=0.12)
        gbar = Rectangle(width=W, height=0.13, stroke_width=0, fill_color=GREEN, fill_opacity=1)
        gbar.move_to([L + W / 2, TOP - U - H + 0.065, 0])
        conses = T("500,500 conses", size=44, color=GOLD).move_to([RX, 0.4, 0])
        c_arrow = Arrow(conses.get_left() + LEFT * 0.1, [L + W / 3, TOP - U - 2 * H / 3, 0], buff=0.1,
                        stroke_width=4, color=GOLD, max_tip_length_to_length_ratio=0.1, tip_length=0.22)
        answer = T("1,000 cells in the answer", size=34, color=GREEN).move_to([RX, -1.5, 0])
        a_arrow = Arrow(answer.get_left() + LEFT * 0.1, gbar.get_right() + RIGHT * 0.05, buff=0.1,
                        stroke_width=4, color=GREEN, max_tip_length_to_length_ratio=0.2, tip_length=0.22)

        with self.say("c4.cost.4") as c:
            self.play(FlashUnder(num, color=YELLOW, run_time=rt(c, "big O", 1.3)))
            c.wait_until("big O")
            self.play(TransformFromCopy(rhs, time_row[1]), FadeIn(time_row[0], shift=0.3 * RIGHT),
                      run_time=rt(c, "quadratic", 1.4))
            settle(self, time_row)
            c.wait_until("quadratic")
            self.play(FlashAround(time_row[1], color=RED, run_time=rt(c, "thousand", 1.2)))

            # n = 1,000
            c.wait_until("thousand")
            sweep_clear(self, time_row.animate.move_to([RX, 2.9, 0]),
                        keep=[stair, bn3, ln, rhs, time_row], run_time=1.0)
            self.play(FadeTransform(stair, smooth), ReplacementTransform(ln, lab_1000),
                      run_time=rt(c, "half a million", 1.3))
            c.wait_until("half a million")
            self.play(FadeTransform(rhs, conses), GrowArrow(c_arrow), run_time=rt(c, "answer", 1.3))
            c.wait_until("answer")
            self.play(FadeIn(gbar), FadeIn(answer, shift=0.3 * LEFT), GrowArrow(a_arrow), run_time=rt(c, None, 1.2))

        self.time_row, self.smooth, self.lab_1000 = time_row, smooth, lab_1000

    # cost.5: but only O(n) space: each copy dies once the next append has copied it
    def space(self):
        time_row, smooth, lab_1000, bn3 = self.time_row, self.smooth, self.lab_1000, self.bn3
        space_row = VGroup(T("space", size=36, color=DIM), MathTex("O(n)", font_size=60, color=GOLD))
        space_row[1].move_to([0, 2.05, 0]).align_to(time_row[1], LEFT)
        space_row[0].next_to(space_row[1], LEFT, buff=0.3)
        ghosts = VGroup(*[stair_row(r, op=0.3) for r in range(1, N + 1)])
        ln = MathTex("n", font_size=48).next_to(bn3, DOWN, buff=0.12)
        arrow = Arrow(RIGHT * 0.7, ORIGIN, buff=0, stroke_width=3, color=DIM, tip_length=0.18,
                      max_tip_length_to_length_ratio=0.4)
        nl = VGroup(arrow, T("no longer needed", size=30, color=DIM)).arrange(RIGHT, buff=0.15)

        def nl_at(r):
            return nl.copy().next_to([L + r * U, TOP - (r + 0.5) * U, 0], RIGHT, buff=0.2)

        def lit_parts(r):
            gold = VGroup(*[block(GOLD).move_to(row_pos(r, j)) for j in range(r - 1)])
            return gold, block(YELLOW).move_to(row_pos(r, r - 1))

        with self.say("c4.cost.5") as c:
            self.play(FadeIn(space_row, shift=0.3 * DOWN), run_time=rt(c, "why", 1.2))
            c.wait_until("why")
            self.play(FlashAround(space_row, color=GOLD, run_time=rt(c, "because the copies", 1.2)))

            # the copies over time, as ghosts (the 500,500 / 1,000 labels go only now)
            c.wait_until("because the copies")
            sweep_clear(self, FadeTransform(smooth, ghosts), ReplacementTransform(lab_1000, ln),
                        keep=[smooth, bn3, lab_1000, time_row, space_row], run_time=rt(c, "gone", 1.5))

            # each row lives only until the next append has copied it
            c.wait_until("gone")
            gold, yel = lit_parts(1)
            self.play(FadeIn(yel, scale=0.6), run_time=0.8)
            self.wait(0.3)
            cur = [yel]
            label = None
            for r in range(1, N):
                if r == 1:
                    t, hold = 2.0, 0.0
                elif r == 2:
                    c.wait_until("after that")
                    t, hold = 1.2, 0.3
                else:
                    per = max(0.5, (c.until("lesson") - 0.3) / (N - r))
                    t, hold = 0.75 * per, 0.25 * per
                gold, yel = lit_parts(r + 1)
                src = VGroup(*[sq for part in cur for sq in (part if isinstance(part, VGroup) else [part])])
                anims = [time_span(TransformFromCopy(src, gold), 0, 0.6 * t),
                         time_span(FadeIn(yel, scale=0.6), 0.4 * t, 0.8 * t),
                         *[time_span(FadeOut(p), 0.6 * t, t) for p in cur]]
                if label is None:
                    label = nl_at(r)
                    anims.append(time_span(FadeIn(label, shift=0.3 * LEFT), 0.6 * t, t))
                else:
                    anims.append(time_span(label.animate.move_to(nl_at(r)), 0.6 * t, t))
                self.play(*anims, run_time=t)
                cur = [gold, yel]
                if hold > 0:
                    self.wait(hold)

            # time wasted, space not
            c.wait_until("lesson")
            self.play(FlashAround(time_row, color=RED, run_time=rt(c, "but not space", 1.2)))
            c.wait_until("but not space")
            self.play(FlashAround(space_row, color=GOLD, run_time=rt(c, None, 1.2)))
