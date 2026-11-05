"""Chapter 2, scene 2: linear search, one comparison at a time. Clips c2.lin.1 – c2.lin.3.

Opens on s1's last shot (ConsChain [3,5,9,4,7] at ORIGIN, GOLD marker above cell 0).
c2.lin.1  title "linear search"; looking for 9: tags 9 = 3? ✗, 9 = 5? ✗, 9 = 9? ✓, counter 1..3.
c2.lin.2  reset, looking for 6: the pointer sweeps all five cells (✗ each, counter 5), lands on [].
c2.lin.3  values morph to x₁ x₂ x₃ ⋯ xₙ; three GOLD braces (n/2, n, n incl. []); their n's flash on
          "proportional"; they merge into O(n) on "big O of en" as the title becomes "linear:";
          the abstract chain + "linear: O(n)" shrink to the top-left (s3 opens from that group).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

VALUES = [3, 5, 9, 4, 7]
TAG_Y = -1.1        # comparison tags (and the sweep's crosses) under the cells
MARK_Y = -1.85      # ✗ / ✓ under a tag
CHAIN_Y = 0.9       # where the abstract chain sits while the braces stack below it
LABEL_SIZE = 48     # brace labels (MathTex)
FINAL_SCALE = 0.4   # the top-left group handed to s3


def tag_for(target, value, cell):
    tag = Mono(f"{target} = {value}?", 36)
    tag[0].set_color(YELLOW)
    return tag.move_to([cell.box.get_x(), TAG_Y, 0])


def mark_at(mark, cell, y):
    return mark.move_to([cell.box.get_x(), y, 0])


class LinearSearch(NarratedScene):
    def construct(self):
        self.chain = ConsChain(VALUES)
        self.pointer = marker(GOLD).move_to(above(self.chain.cells[0].box))
        self.title = T("linear search", 48).to_edge(UP, buff=0.55)
        self.clip1()
        self.clip2()
        self.clip3()
        self.ending()

    # ── counter ────────────────────────────────────────────────────────────────
    def make_counter(self):
        self.cword = T("comparisons:", 36, GOLD)
        n0 = self.num(0)
        VGroup(self.cword, n0).to_corner(UR, buff=0.6).set_y(self.title.get_y())
        self.cnum = self.num(0)

    def num(self, n):
        m = T(str(n), 36, GOLD).next_to(self.cword, RIGHT, buff=0.18)
        return m.align_to(self.cword[10], DOWN)      # glyph 10 = the last "s" (no descender)

    def tick(self, n, start=None, end=None):
        old, new = self.cnum, self.num(n)
        self.cnum = new
        anims = [FadeOut(old, shift=0.25 * UP), FadeIn(new, shift=0.25 * UP)]
        if start is not None:
            anims = [time_span(a, start, end) for a in anims]
        return anims

    def counter(self):
        return VGroup(self.cword, self.cnum)   # only for flashes (bounding box)

    # ── c2.lin.1: looking for 9 ────────────────────────────────────────────────
    def clip1(self):
        ch, cells = self.chain, self.chain.cells
        with self.say("c2.lin.1") as c:
            self.play(FadeIn(ch), FadeIn(self.pointer), run_time=0.6)
            c.wait_until("linear search")
            self.play(FadeIn(self.title, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("each")
            self.play(LaggedStart(*[FlashAround(cl.box, color=YELLOW, time_width=1.5) for cl in cells],
                                  lag_ratio=0.3),
                      run_time=min(2.4, 0.8 * c.until("the head")))
            c.wait_until("the head")
            self.play(FlashAround(cells[0].box, color=GOLD, time_width=1.5),
                      self.pointer.animate(rate_func=there_and_back).shift(0.18 * DOWN), run_time=1.2)

            c.wait_until("nine")
            self.look = T("looking for", 40, YELLOW)
            self.digit = T("9", 40, YELLOW)
            self.digit.next_to(self.look, RIGHT, buff=0.2).align_to(self.look[0], DOWN)
            VGroup(self.look, self.digit).move_to(UP * 2.0)
            self.make_counter()
            self.play(FadeIn(self.look, shift=0.3 * DOWN), FadeIn(self.digit, shift=0.3 * DOWN),
                      time_span(FadeIn(self.cword), 0.5, 1.3), time_span(FadeIn(self.cnum), 0.5, 1.3),
                      run_time=1.3)

            tags = [tag_for(9, v, cells[i]) for i, v in enumerate(VALUES[:3])]
            crosses = [mark_at(cross_mark(RED), cells[i], MARK_Y) for i in range(2)]
            tick_mark = mark_at(check_mark(GREEN), cells[2], MARK_Y)

            # first comparison, slowly: the 9 from the label, the 3 from the cell
            c.wait_until("c1")
            t0 = tags[0]
            self.play(TransformFromCopy(self.digit, t0[0]), TransformFromCopy(cells[0].label, t0[2]),
                      FadeIn(t0[1]), FadeIn(t0[3]), *self.tick(1, 0.8, 1.5), run_time=1.5)
            settle(self, t0)
            c.wait_until("no")
            self.play(Create(crosses[0]), run_time=0.5)
            self.play(self.pointer.animate.move_to(above(cells[1].box)), run_time=min(0.8, c.until("c2")))

            c.wait_until("c2")
            self.play(FadeIn(tags[1], shift=0.2 * DOWN), *self.tick(2, 0.3, 0.9), run_time=0.9)
            c.wait_until("no", nth=1)
            self.play(Create(crosses[1]), run_time=0.5)
            self.play(self.pointer.animate.move_to(above(cells[2].box)), run_time=min(0.8, c.until("c3")))

            c.wait_until("c3")
            self.play(FadeIn(tags[2], shift=0.2 * DOWN), *self.tick(3, 0.3, 0.9), run_time=0.9)
            c.wait_until("yes")
            self.play(Create(tick_mark), run_time=0.6)

            c.wait_until("found")
            self.play(cells[2].box.animate.set_stroke(GREEN, 6),
                      FlashAround(cells[2].box, color=GREEN, time_width=1.5), run_time=1.5)
            c.wait_until("three comparisons")
            self.play(FlashAround(self.counter(), color=GOLD, time_width=1.5), run_time=1.5)
            self.tags, self.marks = tags, [*crosses, tick_mark]

    # ── c2.lin.2: looking for 6, every answer no ───────────────────────────────
    def clip2(self):
        ch, cells = self.chain, self.chain.cells
        with self.say("c2.lin.2") as c:
            r = c.until("sweep")
            d6 = T("6", 40, YELLOW).move_to(self.digit).align_to(self.digit, DOWN)
            self.play(FadeOut(*self.tags), FadeOut(*self.marks), cells[2].box.animate.set_stroke(BLUE, 3),
                      ReplacementTransform(self.digit, d6), run_time=min(0.9, 0.5 * r))
            self.digit = d6
            self.play(self.pointer.animate.move_to(above(cells[0].box)), *self.tick(0),
                      run_time=min(0.9, 0.45 * r))

            words = ["three", "five, nine", "nine", "four", "seven"]   # bare "five" is the {five} mark
            self.crosses = [mark_at(cross_mark(RED), cl, TAG_Y) for cl in cells]
            for i, w in enumerate(words):
                c.wait_until(w)
                self.play(FadeIn(self.crosses[i], scale=0.5), *self.tick(i + 1), run_time=0.35)
                if i < 4:
                    self.play(self.pointer.animate.move_to(above(cells[i + 1].box)),
                              run_time=min(0.5, c.until(words[i + 1], floor=0.2)))

            c.wait_until("five")
            self.play(FlashAround(self.counter(), color=GOLD, time_width=1.5), run_time=1.5)

            c.wait_until("nil")
            self.play(self.pointer.animate.move_to([ch.nil.get_x(), self.pointer.get_y(), 0]), run_time=1.0)
            self.play(FlashAround(ch.nil, color=TEAL, time_width=1.5),
                      ch.nil.animate(rate_func=there_and_back).scale(1.25), run_time=1.5)

            c.wait_until("absent")
            self.notfound = T("not found", 40, RED).move_to(DOWN * 2.4)
            self.play(FadeIn(self.notfound, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("compare it")
            self.play(LaggedStart(*[FlashAround(cl.box, color=RED, time_width=1.5) for cl in cells],
                                  lag_ratio=0.25), run_time=min(2.0, max(1.2, c.remaining - 0.05)))

    # ── c2.lin.3: any length n; O(n) ───────────────────────────────────────────
    def clip3(self):
        ch, cells = self.chain, self.chain.cells
        with self.say("c2.lin.3") as c:
            gone = [self.look, self.digit, self.cword, self.cnum, self.pointer, self.notfound, *self.crosses]
            self.play(*[FadeOut(m) for m in gone], ch.animate.shift(UP * CHAIN_Y), run_time=1.0)

            # values -> x1 x2 x3 ⋯ xn: each new label out of the old one; cell 3 collapses into ⋯
            news = {i: MathTex(s, font_size=60).move_to(cells[i].box)
                    for i, s in ((0, "x_1"), (1, "x_2"), (2, "x_3"), (4, "x_n"))}
            lab3 = cells[3].label
            cells[3].remove(lab3)
            ch.add(lab3)
            dots = MathTex(r"\cdots", font_size=60).move_to(cells[3].get_center())
            bridge = Arrow(dots.get_right() + RIGHT * 0.12, cells[4].entry(), buff=0, stroke_width=3,
                           color=FG, max_tip_length_to_length_ratio=0.3, tip_length=0.16)
            anims = [time_span(ReplacementTransform(cells[i].label, news[i]), 0.12 * k, 0.12 * k + 1.0)
                     for k, i in enumerate((0, 1, 2, 4))]
            anims += [time_span(ReplacementTransform(lab3, dots), 0.3, 1.3),
                      time_span(FadeOut(cells[3]), 0.3, 1.1), time_span(FadeOut(ch.arrows[3]), 0.3, 1.1),
                      time_span(GrowArrow(bridge), 0.7, 1.5)]
            self.play(*anims, run_time=1.5)
            for i, m in news.items():
                cells[i].label = m
            ch.remove(cells[3], ch.arrows[3])
            ch.add(bridge)
            settle(self, ch)

            # three spans, stacked under the chain
            x0 = cells[0].box.get_left()[0]
            x_end = cells[4].ptr.get_right()[0]
            x_nil = ch.nil.get_right()[0]
            y = cells[0].box.get_bottom()[1]
            rows = []
            for right, tex in ((0.5 * (x0 + x_end), r"\text{found, on average: about } n/2"),
                               (x_end, r"\text{found, worst case: } n"),
                               (x_nil, r"\text{absent: always } n")):
                brace = span_brace(np.array([x0, y, 0]), np.array([right, y, 0]), color=GOLD)
                label = MathTex(tex, font_size=LABEL_SIZE, color=GOLD).next_to(brace, DOWN, buff=0.12)
                if label.get_left()[0] < -6.5:
                    label.shift(RIGHT * (-6.5 - label.get_left()[0]))
                rows.append((brace, label))
                y = label.get_bottom()[1] - 0.12

            def show(row, *extra):
                brace, label = row
                self.play(GrowFromCenter(brace), time_span(FadeIn(label, shift=0.3 * DOWN), 0.4, 1.2),
                          *extra, run_time=1.2)

            c.wait_until("avg")
            show(rows[0])
            c.wait_until("last element")
            self.play(FlashAround(cells[4].box, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("you check every element")
            show(rows[1])
            c.wait_until("miss")
            show(rows[2], FlashAround(ch.nil, color=TEAL, time_width=1.5))

            # either way: every label is a multiple of n
            c.wait_until("proportional")
            ns = [rows[0][1][0][-3], rows[1][1][0][-1], rows[2][1][0][-1]]
            self.play(LaggedStart(*[FlashAround(g, color=YELLOW, time_width=1.5) for g in ns],
                                  lag_ratio=0.25), run_time=1.6)

            # the three labels merge into one O(n), landing on "big O of en"; the title becomes "linear:"
            c.wait_until("takes linear time")
            final = MathTex(r"\text{linear:}\ ", "O(n)", font_size=96, color=GOLD).move_to(DOWN * 1.4)
            big = final[1].copy()
            copies = [big.copy(), big.copy()]
            rt = min(2.0, max(1.3, c.until("big O of en") + 0.5))
            self.play(*[FadeOut(b) for b, _ in rows],
                      FadeTransform(rows[0][1], big), FadeTransform(rows[1][1], copies[0]),
                      FadeTransform(rows[2][1], copies[1]),
                      time_span(FadeTransform(self.title, final[0]), 0.35 * rt, rt), run_time=rt)
            self.remove(*copies, big, final[0])
            self.add(final)
            self.final = final

    # ── hand-off: the small top-left group s3 opens from ───────────────────────
    def shrink(self, run_time):
        ch, final = self.chain, self.final
        ch.generate_target()
        ch.target.scale(FINAL_SCALE).to_corner(UL, buff=0.55)
        final.generate_target()
        final.target.scale(FINAL_SCALE).next_to(ch.target, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(MoveToTarget(ch), MoveToTarget(final), run_time=run_time)

    def ending(self):
        self.wait(1.4)      # let "linear: O(n)" read at full size after it lands on the last words
        self.shrink(1.0)    # then into the corner
        self.wait(0.3)
        self.play(FadeOut(self.chain), FadeOut(self.final), run_time=0.5)
        self.wait(0.15)
