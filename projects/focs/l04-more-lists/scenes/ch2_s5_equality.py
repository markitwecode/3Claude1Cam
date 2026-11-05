"""Chapter 2, scene 5: polymorphic equality. Clips c2.eq.1 – c2.eq.4.

Plan
  c2.eq.1  title; the five operators in a row (BLUE), a YELLOW box sliding onto each as it is
           named; `'a -> 'a -> bool` below on {any}; the two 'a flash on {inspect}.
  c2.eq.2  1 -> 2 -> [] above 1 -> 2 -> []; row 1 `[1; 2] = [1; 2]` with a "?"; a YELLOW scanner
           walks the column pairs, a GREEN tick per pair and on the nils; "?" -> `- : bool = true`.
           {less}: lower 2 becomes 3, row 2 `[1; 2] < [1; 3]` born from row 1; "Yes." -> true;
           scan again: tick on 1/1, the 2/3 column glows GOLD, `2 < 3` born from the two labels.
           {strings}: L3's `"apple" < "banana"` small and DIM as row 3 (its < under row 2's),
           first letters boxed GOLD.
  c2.eq.3  `("Bob", 1) > ("Amy", 9)`, a DIM left-to-right arrow, names boxed GOLD on {first},
           `>` turns GOLD, 1 and 9 dimmed on {never}, -> true; `true > false` -> true below.
  c2.eq.4  `member "dog" ["cat"; "dog"]` (box slides from the key to the match, turns GREEN) and
           `member [1; 2] [[3]; [1; 2]]` (same, inner [1; 2]); TEAL underlines on the elements;
           {safe}: the six lines become a table, every reply GREEN, caption below.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


REPLY = "- : bool = true"

# clip 2 layout
CHAIN_SCALE = 1.15
A_Y, B_Y = 2.5, 1.0          # the two chains
TICK_Y = -0.25               # ticks / "2 < 3" under the columns
ROW_Y = [-1.25, -2.15, -3.0]  # row 1, row 2, the DIM strings row
X_E, X_R = -5.6, 0.6         # left edges: expression column, reply column


def qmark():
    return T("?", size=60, color=YELLOW)


def scan_rect(x, color=YELLOW):
    """The scanner: one column pairing a cell of the upper chain with the cell below it."""
    side = CELL * CHAIN_SCALE
    return Rectangle(width=side + 0.36, height=A_Y - B_Y + side + 0.3,
                     stroke_color=color, stroke_width=5).move_to([x, (A_Y + B_Y) / 2, 0])


def row_code(src, y, size=40):
    return Code(src, size=size).move_to([X_E, y, 0], aligned_edge=LEFT)


def row_reply(y, size=40):
    return Code(REPLY, size=size).move_to([X_R, y, 0], aligned_edge=LEFT)


class Equality(NarratedScene):
    def construct(self):
        self.operators()
        self.lists()
        self.tuples()
        self.member()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.eq.1 ────────────────────────────────────────────────────────────────
    def operators(self):
        with self.say("c2.eq.1") as c:
            title = T("polymorphic equality", size=56).move_to([0, 2.0, 0])
            ops = [Mono(s, size=80, color=BLUE) for s in ("=", "<", "<=", ">", ">=")]
            row = VGroup(*ops).arrange(RIGHT, buff=1.1).move_to([0, 0.0, 0])
            ty = Code("'a -> 'a -> bool", size=44).move_to([0, -2.0, 0])

            c.wait_until("called")
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.2)

            c.wait_until("ops")
            self.play(LaggedStart(*[FadeIn(o, shift=0.3 * DOWN) for o in ops], lag_ratio=0.15),
                      run_time=min(1.2, max(0.6, 0.9 * c.until("equals sign"))))

            # one YELLOW box sliding onto each operator as it is named
            names = ["equals sign", "less than", "less than or equal", "greater than",
                     "greater than or equal", "any"]
            c.wait_until("equals sign")
            box = token_box([ops[0]], row, color=YELLOW, pad=0.4)
            self.play(FadeIn(box), ops[0].animate.set_color(YELLOW), run_time=0.6)
            for i in range(1, 5):
                c.wait_until(names[i])
                rt = min(0.6, max(0.3, 0.7 * c.until(names[i + 1])))
                self.play(Transform(box, token_box([ops[i]], row, color=YELLOW, pad=0.4)),
                          ops[i - 1].animate.set_color(BLUE), ops[i].animate.set_color(YELLOW),
                          run_time=rt)

            c.wait_until("any")
            self.play(FadeOut(box), ops[4].animate.set_color(BLUE),
                      FadeIn(ty, shift=0.3 * DOWN), run_time=1.2)

            c.wait_until("inspect")
            self.play(FlashAround(ty.find("'a", nth=0), color=PINK, run_time=1.6, time_width=1.5),
                      FlashAround(ty.find("'a", nth=1), color=PINK, run_time=1.6, time_width=1.5))

            c.wait_until("consistent order")
            self.play(FlashUnder(VGroup(*ops[1:]), color=YELLOW,
                                 run_time=max(0.6, min(1.4, c.remaining))))

    # ── c2.eq.2 ────────────────────────────────────────────────────────────────
    def lists(self):
        with self.say("c2.eq.2") as c:
            chain_a = ConsChain([1, 2]).scale(CHAIN_SCALE).move_to([0, A_Y, 0])
            chain_b = ConsChain([1, 2]).scale(CHAIN_SCALE).move_to([0, B_Y, 0])
            col_x = [chain_a.cells[0].box.get_x(), chain_a.cells[1].box.get_x(),
                     chain_a.nil.get_x()]

            sweep_clear(self, time_span(FadeIn(chain_a, shift=0.3 * DOWN), 0.4, 1.3),
                        time_span(FadeIn(chain_b, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            c.wait_until("Is the list one")
            expr1 = row_code("[1; 2] = [1; 2]", ROW_Y[0])
            reply1 = row_reply(ROW_Y[0])
            q1 = qmark().move_to(reply1)
            self.play(FadeIn(expr1, shift=0.3 * DOWN),
                      time_span(FadeIn(q1, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)

            # the walk: pair by pair, a tick each, then the two nils
            c.wait_until("walk")
            scanner = scan_rect(col_x[0])
            ticks = [check_mark().scale(1.2).move_to([x, TICK_Y, 0]) for x in col_x]
            self.play(Create(scanner),
                      time_span(FadeIn(ticks[0], scale=0.5), 0.6, 1.1), run_time=1.1)
            c.wait_until("pair by pair")
            self.play(Transform(scanner, scan_rect(col_x[1])),
                      time_span(FadeIn(ticks[1], scale=0.5), 0.5, 1.0), run_time=1.0)
            c.wait_until("match")
            self.play(Transform(scanner, scan_rect(col_x[2])),
                      time_span(FadeIn(ticks[2], scale=0.5), 0.5, 1.0), run_time=1.0)

            c.wait_until("so the answer is true")
            self.play(ReplacementTransform(q1, reply1), run_time=1.0)

            # less than: the lower 2 becomes 3, row 2 is born from row 1
            c.wait_until("less")
            self.play(FadeOut(scanner), *[FadeOut(t) for t in ticks], run_time=0.7)
            label_a, label_b = chain_a.cells[1].label, chain_b.cells[1].label
            three = value_label(3).scale(CHAIN_SCALE).move_to(label_b)
            expr2 = row_code("[1; 2] < [1; 3]", ROW_Y[1])
            reply2 = row_reply(ROW_Y[1])
            q2 = qmark().move_to(reply2)
            self.play(Transform(label_b, three), TransformFromCopy(expr1, expr2),
                      time_span(FadeIn(q2, shift=0.2 * DOWN), 0.8, 1.5), run_time=1.5)

            c.wait_until("decide")
            self.play(ReplacementTransform(q2, reply2), run_time=1.0)

            c.wait_until("The first elements are equal")
            scanner2 = scan_rect(col_x[0])
            tick0 = check_mark().scale(1.2).move_to([col_x[0], TICK_Y, 0])
            self.play(Create(scanner2),
                      time_span(FadeIn(tick0, scale=0.5), 0.6, 1.1), run_time=1.1)

            c.wait_until("comes down to the second elements")
            self.play(Transform(scanner2, scan_rect(col_x[1], color=GOLD)),
                      label_a.animate.set_color(GOLD), label_b.animate.set_color(GOLD),
                      run_time=1.2)

            c.wait_until("two is less than three")
            two_m, lt_m, three_m = (MathTex(s, font_size=52).set_color(GOLD) for s in ("2", "<", "3"))
            VGroup(two_m, lt_m, three_m).arrange(RIGHT, buff=0.18).move_to([col_x[1], TICK_Y, 0])
            self.play(TransformFromCopy(label_a, two_m), TransformFromCopy(label_b, three_m),
                      time_span(FadeIn(lt_m), 0.5, 1.5), run_time=1.5)

            # the same rule as L3's strings: a small DIM row 3, its < under row 2's
            c.wait_until("strings")
            s_expr = Code('"apple" < "banana"', size=32).set_color(DIM)
            s_expr.move_to([0, ROW_Y[2], 0])
            s_expr.shift((expr2.find("<").get_x() - s_expr.find("<").get_x()) * RIGHT)
            s_reply = row_reply(ROW_Y[2], size=32).set_color(DIM)
            self.play(FadeIn(s_expr, shift=0.2 * DOWN),
                      time_span(FadeIn(s_reply, shift=0.2 * DOWN), 0.3, 1.0), run_time=1.0)
            first_a = s_expr.find('"apple"')[1]
            first_b = s_expr.find('"banana"')[1]
            self.s_boxes = [
                Rectangle(width=g.width + 0.12, height=s_expr.height + 0.16, stroke_color=GOLD,
                          stroke_width=2).set_fill(GOLD, opacity=0.25)
                .move_to([g.get_x(), s_expr.get_y(), 0]).set_z_index(-1)
                for g in (first_a, first_b)]
            self.play(*[FadeIn(b) for b in self.s_boxes],
                      first_a.animate.set_color(GOLD), first_b.animate.set_color(GOLD),
                      run_time=0.8)
            self.s_row = [s_expr, s_reply, *self.s_boxes, two_m, lt_m, three_m]   # 2 < 3 lingers too

    # ── c2.eq.3 ────────────────────────────────────────────────────────────────
    def tuples(self):
        with self.say("c2.eq.3") as c:
            tup = Code('("Bob", 1) > ("Amy", 9)', size=48).move_to([0, 1.5, 0])
            # the DIM strings row lingers a moment longer
            sweep_clear(self, time_span(FadeIn(tup, shift=0.3 * DOWN), 0.6, 1.4),
                        keep=self.s_row, run_time=1.4)

            c.wait_until("from left to right")
            arrow = Arrow([tup.get_left()[0], 2.45, 0], [tup.get_right()[0], 2.45, 0],
                          buff=0, color=DIM, stroke_width=4, max_tip_length_to_length_ratio=0.04)
            self.play(GrowArrow(arrow), run_time=1.2)

            c.wait_until("bob")
            q = qmark().move_to([0, 0.5, 0])
            self.play(FadeIn(q, shift=0.2 * DOWN), *[FadeOut(m) for m in self.s_row], run_time=0.8)

            c.wait_until("first")
            boxes = [token_box(tup.find(name), tup, color=GOLD, pad=0.2)
                     for name in ('"Bob"', '"Amy"')]
            self.play(*[FadeIn(b) for b in boxes], run_time=1.0)

            c.wait_until("Bob comes after Amy")
            gt = tup.find(">")
            self.play(*recolor(gt, GOLD), FlashAround(gt, color=GOLD, run_time=1.4), run_time=1.4)

            c.wait_until("never")
            self.play(restyle(tup.find("1"), op=DIMMED), restyle(tup.find("9"), op=DIMMED),
                      run_time=1.0)
            c.wait_until("even compared")
            reply = Code(REPLY, size=44).move_to(q)
            self.play(ReplacementTransform(q, reply),
                      run_time=min(1.0, max(0.5, 0.9 * c.until("bools"))))

            c.wait_until("bools")
            bexpr = Code("true > false", size=48).move_to([0, -1.25, 0])
            bq = qmark().move_to([0, -2.25, 0])
            self.play(FadeIn(bexpr, shift=0.3 * DOWN),
                      time_span(FadeIn(bq, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)

            c.wait_until("True is greater than false")
            breply = Code(REPLY, size=44).move_to(bq)
            self.play(ReplacementTransform(bq, breply), run_time=1.0)
            self.b_row = [bexpr, breply]

    # ── c2.eq.4 ────────────────────────────────────────────────────────────────
    def member(self):
        with self.say("c2.eq.4") as c:
            m1 = Code('member "dog" ["cat"; "dog"]', size=44).move_to([0, 1.6, 0])
            # the booleans row lingers until the first question
            sweep_clear(self, time_span(FadeIn(m1, shift=0.3 * DOWN), 0.6, 1.4),
                        keep=self.b_row, run_time=1.4)

            c.wait_until("dog")
            q1 = qmark().move_to([0, 0.6, 0])
            box1 = token_box(m1.find('"dog"'), m1, color=YELLOW, pad=0.2)
            self.play(FadeIn(box1), FadeIn(q1, shift=0.2 * DOWN), *set_alpha(self.b_row, 0.4),
                      run_time=0.9)

            c.wait_until("True")
            reply1 = Code(REPLY, size=44).move_to(q1)
            self.play(Transform(box1, token_box(m1.find('"dog"', nth=1), m1, color=GREEN, pad=0.2)),
                      ReplacementTransform(q1, reply1), *[FadeOut(m) for m in self.b_row],
                      run_time=1.2)

            c.wait_until("nested")
            m2 = Code("member [1; 2] [[3]; [1; 2]]", size=44).move_to([0, -0.9, 0])
            q2 = qmark().move_to([0, -1.95, 0])
            self.play(FadeIn(m2, shift=0.3 * DOWN),
                      time_span(FadeIn(q2, shift=0.2 * DOWN), 0.6, 1.2), run_time=1.2)
            c.wait_until("a member of a list")
            box2 = token_box(m2.find("[1; 2]"), m2, color=YELLOW, pad=0.2)
            self.play(FadeIn(box2), run_time=0.8)

            c.wait_until("Also true")
            reply2 = Code(REPLY, size=44).move_to(q2)
            self.play(Transform(box2, token_box(m2.find("[1; 2]", nth=1), m2, color=GREEN, pad=0.2)),
                      ReplacementTransform(q2, reply2), run_time=1.2)

            c.wait_until("whole")
            uls = [underline(m2.find(s, nth=k), TEAL) for s, k in (("[3]", 0), ("[1; 2]", 1))]
            self.play(*[Create(u) for u in uls], run_time=1.0)
            c.wait_until("compares them whole")
            self.play(FlashAround(m2.find("[1; 2]"), color=YELLOW, run_time=1.6, time_width=1.5),
                      FlashAround(m2.find("[1; 2]", nth=1), color=YELLOW, run_time=1.6,
                                  time_width=1.5))

            # the six lines as one table
            c.wait_until("safe")
            srcs = ["[1; 2] = [1; 2]", "[1; 2] < [1; 3]", '("Bob", 1) > ("Amy", 9)',
                    "true > false", 'member "dog" ["cat"; "dog"]', "member [1; 2] [[3]; [1; 2]]"]
            ys = [2.55, 1.8, 1.05, 0.3, -0.45, -1.2]
            x0, x1 = -6.1, 2.0
            exprs = [Code(s, size=32).move_to([x0, y, 0], aligned_edge=LEFT) for s, y in zip(srcs, ys)]
            replies = [Code(REPLY, size=32).move_to([x1, y, 0], aligned_edge=LEFT) for y in ys]
            caption = T("ints, strings, bools, and tuples or lists of them", size=36).move_to([0, -2.5, 0])
            self.play(ReplacementTransform(m1, exprs[4]), ReplacementTransform(reply1, replies[4]),
                      ReplacementTransform(m2, exprs[5]), ReplacementTransform(reply2, replies[5]),
                      *[FadeOut(m) for m in (box1, box2, *uls)],
                      time_span(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN)
                                              for pair in zip(exprs[:4], replies[:4]) for m in pair],
                                            lag_ratio=0.15), 0.4, 1.8),
                      time_span(FadeIn(caption, shift=0.3 * DOWN), 0.6, 1.4),
                      run_time=2.0)
            self.play(LaggedStart(*[r.animate.set_color(GREEN) for r in replies], lag_ratio=0.12),
                      run_time=1.5)
        self.wait(2.5)
