"""Chapter 3, scene 5: watching part at work on [3; 9; 4; 7] with pivot 5. Clips c3.part.1 – c3.part.4.

Opens on ch3_s4_code.handover_shot() (quick_code() small in the top-left corner).
Layout: code in the corner; right of it the pivot, the input chain and the accumulators l / r
(scale S); under it the trace (Code 28, rows ROWS) with each test in GOLD beside its line.
Exports `part_icon()`: a miniature of the part trace ending with l = [4; 3], r = [7; 9] (for s7).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S = 0.72                      # chain scale (cell values ≈ 30)
PIV = (2.2, 3.2)              # pivot
INP_Y = 2.3                   # input chain row
ACC_Y = 0.9                   # accumulators row
L_X, R_X = 0.12, 4.73         # accumulator chain centres
TX = -5.6                     # trace code left edge
ROWS = [-0.76, -1.34, -1.92, -2.5, -3.08]
TEST_X = -0.3                 # tests' left edge
TSIZE = 28

TRACE = ["part [] [] [3; 9; 4; 7]",
         "part [3] [] [9; 4; 7]",
         "part [3] [9] [4; 7]",
         "part [4; 3] [9] [7]",
         "part [4; 3] [7; 9] []"]
TESTS = [("3 ≤ 5?", "yes"), "9 ≤ 5? no", "4 ≤ 5? yes", "7 ≤ 5? no"]


def _all(c, sub):
    out, k = [], 0
    while True:
        try:
            out.append(c.find(sub, nth=k))
        except ValueError:
            return out
        k += 1


def pcode(src, size=TSIZE):
    """Code with `part`/`quick` YELLOW and `@` GOLD, as in quick_code()."""
    c = Code(src, size=size)
    for name in ("part", "quick"):
        for g in _all(c, name):
            g.set_color(YELLOW)
    for g in _all(c, "@"):
        g.set_color(GOLD)
    return c


def left_at(m, x, y):
    m.move_to([0, y, 0]).shift(RIGHT * (x - m.get_left()[0]))
    return m


def implies(code):
    a = MathTex(r"\Rightarrow", font_size=40, color=DIM)
    a.next_to(code, LEFT, buff=0.22).set_y(code.get_y())
    return a


def dim_chain(ch):
    """A chain drawn in DIM outlines (boxes keep their BG fill)."""
    for cell in ch.cells:
        cell.box.set_stroke(DIM)
        cell.ptr.set_stroke(DIM)
        cell.dot.set_color(DIM)
        cell.label.set_color(DIM)
    for a in ch.arrows:
        a.set_color(DIM)
    if ch.nil is not None:
        ch.nil.set_color(DIM)
    return ch


def gold(text):
    return T(text, 28, GOLD)


def part_icon():
    """Miniature of the part trace: the five lines, then l = [4; 3] and r = [7; 9] (≈ 3.4 wide)."""
    lines = VGroup()
    for i, src in enumerate(TRACE):
        c = left_at(pcode(src), 0, -0.68 * i)
        lines.add(VGroup(implies(c), c) if i else c)
    lr = VGroup(Code("l = [4; 3]", size=TSIZE), Code("r = [7; 9]", size=TSIZE)).arrange(RIGHT, buff=0.8)
    lr.next_to(lines, DOWN, buff=0.4)
    for m in lr:
        m.text[0].set_color(YELLOW)
    icon = VGroup(lines, lr)
    icon.scale(3.4 / icon.width).move_to(ORIGIN)
    return icon


class Partitioning(NarratedScene):
    def construct(self):
        self.shot = load_scene("ch3_s4_code").handover_shot()
        self.add(self.shot)
        self.code = self.shot[0]
        self.clip_trace()
        self.clip_cost()
        self.clip_backwards()
        self.clip_equal()
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.part.1
    def clip_trace(self):
        code = self.code
        with self.say("c3.part.1") as c:
            dim = [g for i in (0, 1, 2, 3, 11) for g in code.line(i)]
            self.play(*set_alpha(dim, DIMMED), run_time=1.5)

            pivot = value_label(5, 48, YELLOW).move_to([*PIV, 0])
            plab = T("pivot", 28, DIM).next_to(pivot, LEFT, buff=0.3)
            self.pivot, self.plab = pivot, plab
            inp = ConsChain([3, 9, 4, 7]).scale(S).move_to([PIV[0], INP_Y, 0])
            lch = ConsChain([4, 3]).scale(S).move_to([L_X, ACC_Y, 0])
            rch = ConsChain([7, 9]).scale(S).move_to([R_X, ACC_Y, 0])
            lname = Mono("l", 32).next_to(lch, LEFT, buff=0.2)
            rname = Mono("r", 32).next_to(rch, LEFT, buff=0.2)
            lsplit = T("≤ 5", 30, t2c={"5": YELLOW}).next_to(lch, DOWN, buff=0.18)
            rsplit = T("> 5", 30, t2c={"5": YELLOW}).next_to(rch, DOWN, buff=0.18)
            self.inp, self.lch, self.rch = inp, lch, rch
            self.lname, self.rname, self.lsplit, self.rsplit = lname, rname, lsplit, rsplit

            lines = [left_at(pcode(s), TX, y) for s, y in zip(TRACE, ROWS)]
            arrows = [None] + [implies(l) for l in lines[1:]]
            self.lines, self.arrows = lines, arrows
            q1 = left_at(gold(TESTS[0][0]), TEST_X, ROWS[1])
            yes1 = gold(TESTS[0][1]).next_to(q1, RIGHT, buff=0.15)
            yes1.align_to(q1, DOWN)
            tests = [q1] + [left_at(gold(t), TEST_X, y) for t, y in zip(TESTS[1:], ROWS[2:])]
            self.tests = [q1, yes1] + tests[1:]

            c.wait_until("setup")
            self.play(*appear(pivot, plab, lag=0.3), run_time=min(1.2, c.until("three")))
            c.wait_until("three")
            pieces = []
            for i, cell in enumerate(inp.cells):
                pieces += [cell, inp.arrows[i]]
            pieces.append(inp.nil)
            self.play(*appear(*pieces, shift=None, lag=0.12), run_time=min(1.8, c.until("Both accumulators")))
            c.wait_until("Both accumulators")
            self.play(*appear(lname, lch.nil, lsplit, rname, rch.nil, rsplit, shift=None, lag=0.12),
                      run_time=1.2)
            self.play(*appear(lines[0], shift=None), run_time=min(1.0, c.until("t1")))

            # t1: 3 ≤ 5? yes → onto l
            c.wait_until("t1")
            self.play(*appear(q1), *flash([inp.cells[0], pivot]), run_time=min(1.4, c.until("Yes")))
            c.wait_until("Yes")
            self.play(*appear(yes1, shift=None), run_time=0.6)
            self.row(1, min(1.6, 0.5 * c.until("t2")))
            self.play(*self.cons(0, lch, 1), run_time=min(1.6, c.until("t2") - 0.5))
            c.wait_until("t2")

            # t2: 9 > 5 → onto r
            self.play(*appear(tests[1]), *self.cons(1, rch, 1, arc=-0.6),
                      run_time=min(1.5, 0.5 * c.until("t3")))
            self.row(2, min(1.4, c.until("t3")))
            c.wait_until("t3")

            # t3, t4: quick; each line is born with its cons, beside its test
            derive(self, lines[2], lines[3], *appear(tests[2]), *self.cons(2, lch, 0, arc=-0.5),
                   *appear(arrows[3], shift=None), run_time=1.3, split=0.62)
            c.wait_until("t4")
            derive(self, lines[3], lines[4], *appear(tests[3]), *self.cons(3, rch, 0),
                   *appear(arrows[4], shift=None), run_time=max(0.9, min(1.3, c.until() - 0.1)), split=0.6)

    def row(self, k, rt):
        """Trace line k born from line k-1, then its ⇒."""
        derive(self, self.lines[k - 1], self.lines[k], run_time=0.72 * rt)
        self.play(*appear(self.arrows[k], shift=None), run_time=max(0.3, 0.28 * rt))

    def cons(self, i, acc, j, arc=None):
        """Input cell i leaves; a cell born from it lands at acc.cells[j] (the new front)."""
        inp = self.inp
        return [*fly(inp.cells[i], acc.cells[j], arc=arc),
                *during(disappear(inp.cells[i], inp.arrows[i]), 0.45, 0.9),
                *during([GrowArrow(acc.arrows[j])], 0.65, 1.0)]

    # ------------------------------------------------------------ c3.part.2
    def clip_cost(self):
        lines, arrows = self.lines, self.arrows
        with self.say("c3.part.2") as c:
            c.wait_until("one comparison")
            counter = T("comparisons: 4", 32, GOLD).move_to([PIV[0], INP_Y, 0])
            self.play(*swap(self.inp.nil, counter), *flash(self.tests[0:1] + self.tests[2:], color=GOLD),  # early: the count lands on "one comparison"
                      run_time=min(1.4, c.until("dividing")))
            c.wait_until("dividing")
            formula = T("n items → n − 1 comparisons", 30, GOLD).move_to([PIV[0], 1.62, 0])
            self.play(*appear(formula), run_time=1.2)
            self.counter, self.formula = counter, formula

            c.wait_until("iter")

            def rowbox(k):
                code = lines[k]
                left = TX - 0.75
                w = code.get_right()[0] + 0.15 - left
                b = Rectangle(width=w, height=0.52).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.12)
                b.move_to([left + w / 2, ROWS[k], 0]).set_z_index(-1)
                return b

            box = rowbox(0)
            self.play(*disappear(*self.tests), FadeIn(box), run_time=0.8)
            tag1 = left_at(T("each call hands over to the next", 28, DIM), 0.5, -1.05)
            tag2 = left_at(T("nothing waits: iterative", 28, DIM), 0.5, -1.63)
            self.play(*appear(tag1), run_time=1.0)
            self.play(Succession(*[Transform(box, rowbox(k), run_time=0.6) for k in range(1, 5)]),
                      run_time=min(2.6, max(1.2, c.until("Nothing waits"))))
            c.wait_until(own_word=tag2)
            self.play(*appear(tag2), run_time=1.0)
            c.wait_until("hand")
            self.play(FadeOut(box), FlashAround(self.code.line(5), run_time=1.2), run_time=1.2)
            hand = left_at(pcode("(quick [4; 3]) @ (5 :: quick [7; 9])"), TX, ROWS[4])
            hand.find("5").set_color(YELLOW)
            self.play(*edit(lines[4], hand), run_time=1.6)
            self.hand, self.tags = hand, [tag1, tag2]

    # ------------------------------------------------------------ c3.part.3
    def clip_backwards(self):
        lch, rch = self.lch, self.rch
        with self.say("c3.part.3") as c:
            settle(self, lch)
            settle(self, rch)
            gone = [*self.lines[:4], *self.arrows[1:4], *self.tags, self.counter, self.formula]
            self.play(*disappear(*gone), run_time=1.0)
            self.play(*recolor([self.lname, self.rname], YELLOW), run_time=0.8)
            c.wait_until("Ell is")
            self.play(FlashAround(lch, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("ar is")
            self.play(FlashAround(rch, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("earlier")
            gl = dim_chain(ConsChain([3, 4]).scale(0.67)).move_to([L_X, -0.95, 0])
            gr = dim_chain(ConsChain([9, 7]).scale(0.67)).move_to([R_X, -0.95, 0])
            self.play(*appear(gl, gr, shift=None, lag=0.4), run_time=1.3)
            top, bot = self.lsplit.get_bottom()[1] - 0.1, gl.get_top()[1] + 0.08
            dl = DoubleArrow([L_X, top, 0], [L_X, bot, 0], buff=0, stroke_width=3, color=DIM,
                             tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            dr = DoubleArrow([R_X, top, 0], [R_X, bot, 0], buff=0, stroke_width=3, color=DIM,
                             tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            revl = T("reversed", 28, DIM).next_to(dl, RIGHT, buff=0.15)
            revr = T("reversed", 28, DIM).next_to(dr, RIGHT, buff=0.15)
            c.wait_until("original order")
            self.play(GrowFromCenter(dl), GrowFromCenter(dr), *appear(revl, revr, shift=None),
                      run_time=min(1.2, c.until("reversed")))

            c.wait_until("reversed")
            i1 = Code("rev_app [1; 2; 3] [4; 5]", size=TSIZE)
            i2 = Code("[3; 2; 1; 4; 5]", size=TSIZE)
            for g in [*i1.find("1; 2; 3"), *i2.find("3; 2; 1")]:
                g.set_color(YELLOW)
            cap = T("consing onto an accumulator reverses", 28, DIM)
            i1.move_to([0, -1.88, 0])
            left_at(i2, i1.get_left()[0] + 0.62, -2.5)
            ia = implies(i2)
            cap.move_to([0, -3.12, 0])
            inner = VGroup(i1, i2, ia, cap)
            frame = RoundedRectangle(corner_radius=0.15, width=inner.width + 0.6, height=inner.height + 0.4)
            frame.set_stroke(DIM, 2).move_to(inner)
            VGroup(inner, frame).shift(RIGHT * (2.4 - frame.get_x()))
            self.play(*during(disappear(self.hand, self.arrows[4]), 0, 0.3),
                      *during(appear(frame, i1, ia, i2, cap, shift=None, lag=0.35), 0.35, 1.0), run_time=2.4)

            c.wait_until("fine")
            boxes, qlabs = [], []
            for ch in (lch, rch):
                b = SurroundingRectangle(ch, color=YELLOW, buff=0.12).set_stroke(width=2)
                q = Mono("quick", 28, YELLOW).next_to(b, UP, buff=0.12).align_to(b, RIGHT)
                boxes.append(b)
                qlabs.append(q)
            self.play(*during(disappear(dl, dr, revl, revr), 0, 0.45),
                      *during([FadeIn(boxes[0]), FadeIn(boxes[1])], 0.4, 1.0),
                      *during(appear(*qlabs), 0.45, 1.0), run_time=1.4)
            res_l = Mono("[3; 4]", 32).move_to(gl)
            res_r = Mono("[7; 9]", 32).move_to(gr)
            al = Arrow([L_X, top, 0], [L_X, bot, 0], buff=0, stroke_width=3, color=YELLOW,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            ar = Arrow([R_X, top, 0], [R_X, bot, 0], buff=0, stroke_width=3, color=YELLOW,
                       tip_length=0.15, max_tip_length_to_length_ratio=0.5)
            self.play(GrowArrow(al), GrowArrow(ar), *swap(gl, res_l), *swap(gr, res_r),
                      run_time=min(1.6, c.until("Each part is about")))
            c.wait_until("Each part is about")
            gtag = T("each part is sorted next, so order doesn't matter", 28, GREEN).move_to([1.6, -2.5, 0])
            self.play(*during(disappear(frame, i1, ia, i2, cap), 0, 0.45),
                      *during(appear(gtag, shift=None), 0.5, 1.0), run_time=1.4)
            self.c3_extra = [*boxes, *qlabs, al, ar, res_l, res_r]
            self.gtag = gtag

    # ------------------------------------------------------------ c3.part.4
    def clip_equal(self):
        lch = self.lch
        with self.say("c3.part.4") as c:
            self.play(FlashAround(self.code.find("<="), run_time=1.2), run_time=min(1.2, c.until("The test is")))
            c.wait_until("The test is")
            ghost = ConsCell(5, color=DIM).scale(S).move_to([PIV[0], INP_Y, 0])
            ghost.label.set_color(YELLOW)
            ghost.set_opacity(0.55)
            gtest = gold("5 ≤ 5? yes").next_to(ghost, RIGHT, buff=0.35)
            self.play(*during(disappear(*self.c3_extra), 0, 0.5), *during(appear(ghost, shift=0.5 * DOWN), 0.3, 1.0),
                      run_time=1.3)
            self.play(*appear(gtest, shift=None), run_time=1.0)
            c.wait_until("an item equal")
            self.play(ghost.animate.move_to([L_X, INP_Y, 0]), run_time=1.3)
            eqtag = T("equal to the pivot: left", 28).next_to(ghost, DOWN, buff=0.2)
            eqtag.align_to(ghost, LEFT)
            self.play(*appear(eqtag), run_time=min(1.0, c.until("dupes")))

            c.wait_until("dupes")
            q = left_at(pcode("quick [5; 3; 5; 1]", 36), -4.0, -1.15)
            rep = left_at(Code("- : int list = [1; 3; 5; 5]", size=36), -4.0, -2.1)
            self.play(*during(disappear(self.gtag), 0, 0.45), *during(appear(q, shift=None), 0.5, 1.0),
                      run_time=1.4)
            c.wait_until("gives")
            self.play(*appear(rep, shift=None), run_time=0.7)
            c.wait_until("both fives")
            fives = [q.find("5", nth=0), q.find("5", nth=1), rep.find("5", nth=0), rep.find("5", nth=1)]
            self.play(*recolor(fives, YELLOW), *flash(fives[2:]), run_time=1.4)
