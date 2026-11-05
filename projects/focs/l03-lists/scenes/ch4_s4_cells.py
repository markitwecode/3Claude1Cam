"""Chapter 4, scene 4: copying and sharing in memory. Clips c4.cells.1 - c4.cells.5.

Layout (S = 1.0, pitch 2.3): xs = 1 -> 2 -> 3 -> [] on the top row (y 1.75, slots 0-2),
ys = 4 -> [] on the lower row (y -0.75) at slot 3, under xs's []. The copies 1', 2', 3' are
born on the lower row at slots 0-2, so the result row reads 1 -> 2 -> 3 -> (shared) 4 -> [].
Bottom band (y -3.0): GOLD counter "new cells: 3" (left) and "O(n) time and space" (right).
cells.4 re-uses xs (shifted one slot right): YELLOW x cell in front on the top row (x :: xs),
YELLOW copies + TEAL [x] on the lower row (xs @ [x]); O(1) top right, O(n) bottom right.
cells.5: two columns, append | append + accumulator?, O(n) = O(n); then the maxim card
(YELLOW lines over a DIM rule, the title-card look).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

PITCH = CELL + PTR_W + LINK     # 2.3: box centre to box centre
X0 = -4.324                     # slot 0 box centre in cells.1-3 ([1; 2; 3] + [4] centred)
X4 = X0 - 1.2                   # slot 0 in cells.4 (x in front: five slots + [] centred)
XS_Y = 1.45                     # top row (xs)
RES_Y = -1.05                   # lower row (ys, then the copies)
BAND_Y = -3.1                   # costs
TOP_Y = 2.72                    # O(1) in cells.4, level with the name labels
RIGHT_EDGE = 6.4


def slot(k, y, x0=X0):
    return np.array([x0 + PITCH * k, y, 0.0])


def place(mob, box, pt):
    """Shift a cell or chain so that `box` (one of its cell boxes) is centred on pt."""
    mob.shift(pt - box.get_center())
    return mob


def code_value(cell):
    """Show a cell's value in code font (for `x`)."""
    cell.label.become(Mono(cell.label.text, size=40).move_to(cell.label.get_center()))
    return cell


def new_cell(v, pt, color=YELLOW):
    cell = ConsCell(v, color=color)
    if isinstance(v, str):
        code_value(cell)
    return place(cell, cell.box, pt)


def name_ptr(src, box, direction, color, name=None, size=36, gap=0.42):
    """A code label over (UP) or under (DOWN) a cell box, with a short arrow onto the box.
    If `name` is given those glyphs take `color` and sit centred over the box."""
    code = Code(src, size=size)
    if name:
        key = VGroup(*code.find(name))
        for g in key:
            g.set_color(color)
    else:
        key = code
    code.shift(RIGHT * (box.get_x() - key.get_x()))
    edge = box.get_edge_center(direction)
    if direction[1] > 0:
        code.shift(UP * (edge[1] + 0.1 + gap - code.get_bottom()[1]))
    else:
        code.shift(DOWN * (code.get_top()[1] - (edge[1] - 0.1 - gap)))
    start = np.array([box.get_x(), code.get_edge_center(-direction)[1], 0.0]) - direction * 0.06
    arr = Arrow(start, edge + direction * 0.04, buff=0, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.35, tip_length=0.17)
    return code, arr


def plain_arrow(start, end, color=FG):
    return Arrow(start, end, buff=0, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16)


class CopyingAndSharing(NarratedScene):
    def construct(self):
        self.memory()
        self.copy_and_share()
        self.cost()
        self.payoff()
        self.accumulator()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── cells.1: xs and ys in memory; the tempting shortcut ─────────────────────────
    def memory(self):
        xs = ConsChain([1, 2, 3])
        place(xs, xs.cells[0].box, slot(0, XS_Y))
        ys = ConsChain([4], color=TEAL)
        place(ys, ys.cells[0].box, slot(3, RES_Y))
        xs_lbl, xs_arr = name_ptr("xs = [1; 2; 3]", xs.cells[0].box, UP, BLUE, name="xs")
        ys_lbl, ys_arr = name_ptr("ys", ys.cells[0].box, UP, TEAL, name="ys")
        last = xs.arrows[2]
        last.save_state()
        xs.nil.save_state()
        swung = link(xs.cells[2], ys.cells[0], color=YELLOW)
        q = T("?", size=64, color=YELLOW).move_to(swung.get_center() + LEFT * 0.75)
        self.xs, self.ys, self.xs_lbl, self.xs_arr = xs, ys, xs_lbl, xs_arr
        self.last, self.swung, self.q = last, swung, q

        with self.say("c4.cells.1") as c:
            # "Now let's look at the cells in memory."
            self.play(FadeIn(xs, lag_ratio=0.08), run_time=min(2.0, 0.8 * c.until("xs")))
            # "Here's exes, one, two, three."
            c.wait_until("xs")
            self.play(FadeIn(xs_lbl, shift=0.25 * DOWN), GrowArrow(xs_arr), run_time=1.0)
            # "And here's whys, the list holding four."
            c.wait_until("ys")
            self.play(FadeIn(ys, shift=0.25 * UP), run_time=1.0)
            self.play(FadeIn(ys_lbl, shift=0.25 * DOWN), GrowArrow(ys_arr), run_time=0.9)
            # "... take the last arrow of exes, which points at nil, and point it at the four instead."
            c.wait_until("last arrow")
            self.play(last.animate.set_color(YELLOW), flash_along(xs.cells[2], xs.nil, YELLOW),
                      run_time=1.0)
            c.wait_until("points at nil")
            self.play(FlashAround(xs.nil, color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("point it at")
            self.play(Transform(last, swung), xs.nil.animate.set_opacity(0.35),
                      run_time=min(1.8, 0.9 * c.until("why")))
            # "Why can't we do that?"
            c.wait_until("why")
            self.play(FadeIn(q, scale=0.6), run_time=0.8)

    # ── cells.2: it would change xs; so append copies, and shares the 4 ─────────────
    def copy_and_share(self):
        xs, ys, xs_lbl, last = self.xs, self.ys, self.xs_lbl, self.last
        cross = cross_mark(RED, r=0.3).move_to(self.swung.get_center())
        red_lbl = Code("xs = [1; 2; 3; 4]", size=36)
        for g in red_lbl.find("xs"):
            g.set_color(BLUE)
        for g in red_lbl.find("[1; 2; 3; 4]"):
            g.set_color(RED)
        red_lbl.shift(VGroup(*xs_lbl.find("xs")).get_center() - VGroup(*red_lbl.find("xs")).get_center())
        xs_back = xs_lbl.copy()

        new = [new_cell(v, slot(k, RES_Y)) for k, v in enumerate((1, 2, 3))]
        a01, a12 = link(new[0], new[1]), link(new[1], new[2])
        share = link(new[2], ys.cells[0], color=YELLOW)
        app_lbl, app_arr = name_ptr("xs @ ys", new[0].box, DOWN, YELLOW)
        shared = T("shared", size=32, color=TEAL).next_to(ys.cells[0].box, DOWN, buff=0.22)
        self.xs_lbl = xs_back
        self.new, self.shared = new, shared

        with self.say("c4.cells.2") as c:
            # "Because that would change exes."  The question becomes the answer: no.
            self.play(ReplacementTransform(self.q, cross), run_time=1.0)
            # "Anyone still holding exes would suddenly see one, two, three, four."
            c.wait_until("anyone still holding")
            self.play(TransformMatchingShapes(xs_lbl, red_lbl), run_time=1.2)
            self.play(FlashAround(VGroup(*red_lbl.find("[1; 2; 3; 4]")), color=RED, time_width=1.5),
                      run_time=1.2)
            # "And OCaml lists never change once they're built."  Undo.
            c.wait_until("never change")
            self.play(Restore(last), Restore(xs.nil), FadeOut(cross),
                      TransformMatchingShapes(red_lbl, xs_back), run_time=1.6)
            c.wait_until("once they're built")
            self.play(FlashAround(xs, color=BLUE, time_width=1.5), run_time=1.2)
            # "So append does the only thing it can. ⏸  It copies."  First copy slow, then faster.
            c.wait_until("it copies")
            self.play(TransformFromCopy(xs.cells[0], new[0]),
                      run_time=min(1.8, 0.85 * c.until("for the two")))
            c.wait_until("for the two")
            self.play(TransformFromCopy(xs.cells[1], new[1]), GrowArrow(a01),
                      run_time=min(1.0, 0.9 * c.until("and for the three")))
            c.wait_until("and for the three")
            self.play(TransformFromCopy(xs.cells[2], new[2]), GrowArrow(a12),
                      run_time=min(1.0, 0.8 * c.until("the last new cell")))
            # "The last new cell points straight at the four, which isn't copied at all."
            c.wait_until("the last new cell")
            self.play(GrowArrow(share), run_time=1.2)
            self.play(FadeIn(app_lbl, shift=0.25 * UP), GrowArrow(app_arr), run_time=1.0)
            # "The two lists share it."
            c.wait_until("the two lists share")
            self.play(FlashAround(ys.cells[0], color=TEAL, time_width=1.5),
                      FadeIn(shared, shift=0.2 * UP), run_time=1.2)

    # ── cells.3: one new cell per element of the first list; ys can be any length ────
    def cost(self):
        xs, ys, new = self.xs, self.ys, self.new
        # the counter sits right under the copies it counts (new 2 and 3), level with `xs @ ys`
        cnt_lbl = T("new cells:", size=40, color=GOLD)
        digits = [T(str(k), size=44, color=GOLD).next_to(cnt_lbl, RIGHT, buff=0.2).align_to(cnt_lbl, DOWN)
                  for k in range(4)]
        under = (slot(1, RES_Y) + slot(2, RES_Y)) / 2 + DOWN * 1.2
        shift = under - VGroup(cnt_lbl, digits[3]).get_center()
        for m in (cnt_lbl, *digits):
            m.shift(shift)
        num = digits[0].copy()
        n_brace = span_brace(slot(0, XS_Y) + np.array([-0.5, -0.5, 0]),
                             slot(2, XS_Y) + np.array([1.0, -0.5, 0]), DOWN, color=GOLD)
        n_lbl = T("n = length of the first list", size=32, color=GOLD, t2s={"n =": ITALIC},
                  t2c={"first": YELLOW}).next_to(n_brace, DOWN, buff=0.1)
        big_o = MathTex("O(n)", font_size=60, color=GOLD)
        ts = T("time and space", size=36)
        VGroup(big_o, ts).arrange(RIGHT, buff=0.35).move_to([3.0, BAND_Y, 0])

        # ys stretches: its [] slides right, "⋯" fills the gap, a new arrow joins them
        nil = ys.nil
        dots = MathTex(r"\cdots", font_size=48, color=TEAL)
        dots.move_to([nil.get_left()[0] + 0.1 + dots.width / 2, RES_Y, 0])
        d = dots.get_right()[0] + 0.12 + LINK - nil.entry()[0]
        far = plain_arrow(dots.get_right() + RIGHT * 0.12, nil.entry() + RIGHT * d)
        m_brace = span_brace(ys.cells[0].box.get_corner(DL),
                             np.array([nil.get_right()[0] + d, RES_Y - 0.5, 0]), DOWN, color=TEAL)
        million = T("a million cells", size=32, color=TEAL).next_to(m_brace, DOWN, buff=0.1)

        with self.say("c4.cells.3") as c:
            # "So append builds a new cell for each element of its first list."  The counter ticks
            # with each new cell.
            self.play(FadeIn(cnt_lbl), FadeIn(num), run_time=0.6)
            ticks = [AnimationGroup(FlashAround(new[k], color=GOLD, time_width=1.5),
                                    Transform(num, digits[k + 1])) for k in range(3)]
            self.play(Succession(*ticks), run_time=min(2.4, 0.9 * c.until("if the first list")))
            # "If the first list has en elements, that's big O of en, in time and in space."
            c.wait_until("if the first list")
            self.play(GrowFromCenter(n_brace), FadeIn(n_lbl, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("big o")
            self.play(FadeIn(big_o, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("in time")
            self.play(FadeIn(ts, shift=0.25 * DOWN), run_time=0.8)
            # "The second list doesn't matter.  Make it a million cells long, ..."
            c.wait_until("the second list")
            self.play(FadeOut(self.shared), nil.animate.shift(RIGHT * d),
                      time_span(FadeIn(dots), 0.5, 1.4), time_span(GrowArrow(far), 0.8, 1.8),
                      run_time=1.8)
            c.wait_until("make it a million")
            self.play(GrowFromCenter(m_brace), FadeIn(million, shift=0.2 * DOWN), run_time=1.2)
            # "... and append does the same work."  The counter hasn't moved.
            c.wait_until("same work")
            self.play(FlashAround(VGroup(cnt_lbl, num), color=GOLD, time_width=1.5), run_time=1.2)

    # ── cells.4: front = one cons cell, O(1); end = copy every cell, O(n) ───────────
    def payoff(self):
        xs, xs_lbl, xs_arr = self.xs, self.xs_lbl, self.xs_arr
        step = RIGHT * (X4 + PITCH - X0)            # xs moves one slot right

        with self.say("c4.cells.4") as c:
            # "Now we can answer our opening question properly."
            c.wait_until("properly")
            sweep_clear(self, *[m.animate.shift(step) for m in (xs, xs_lbl, xs_arr)],
                        keep=[xs, xs_lbl, xs_arr], run_time=1.4)

            xcell = new_cell("x", slot(0, XS_Y, X4))
            x_arr = link(xcell, xs.cells[0])
            fl_lbl, fl_arr = name_ptr("x :: xs", xcell.box, UP, YELLOW)
            tx = ConsChain(["x"], color=TEAL)
            code_value(tx.cells[0])
            place(tx, tx.cells[0].box, slot(4, RES_Y, X4))
            copies = [new_cell(v, slot(k + 1, RES_Y, X4)) for k, v in enumerate((1, 2, 3))]
            c_arrs = [link(copies[0], copies[1]), link(copies[1], copies[2]), link(copies[2], tx.cells[0])]
            ap_lbl, ap_arr = name_ptr("xs @ [x]", copies[0].box, DOWN, YELLOW)
            rects = [SurroundingRectangle(xs.cells[k].box, color=YELLOW, buff=0.1) for k in range(3)]
            o1 = VGroup(MathTex("O(1)", font_size=60, color=GOLD), T("constant time", size=36))
            o1.arrange(RIGHT, buff=0.35).move_to([0, TOP_Y, 0]).align_to(RIGHT * RIGHT_EDGE, RIGHT)
            on = VGroup(MathTex("O(n)", font_size=60, color=GOLD), T("linear time", size=36))
            on.arrange(RIGHT, buff=0.35).move_to([0, BAND_Y, 0]).align_to(o1, RIGHT)

            # "To put an element on the front of exes, you cons it.  A single new cell."
            c.wait_until("to put an element")
            self.play(FadeIn(xcell, shift=0.3 * RIGHT), GrowArrow(x_arr), run_time=1.2)
            self.play(FadeIn(fl_lbl, shift=0.25 * DOWN), GrowArrow(fl_arr), run_time=0.9)
            c.wait_until("a single new cell")
            self.play(FlashAround(xcell, color=YELLOW, time_width=1.5), run_time=1.2)
            # "To put it on the end, you append exes and a list holding that element."
            c.wait_until("to put it on the end")
            self.play(FadeIn(ap_lbl, shift=0.25 * UP), run_time=1.0)
            c.wait_until("a list holding")
            self.play(FadeIn(tx, shift=0.25 * LEFT), run_time=1.0)
            # "That doesn't just walk along exes. ⏸"
            c.wait_until("walk along")
            marker = rects[0].copy()
            self.play(Succession(FadeIn(marker), Transform(marker, rects[1]), Transform(marker, rects[2])),
                      run_time=min(2.4, 0.85 * c.until("it copies every cell")))
            # "It copies every cell. ⏸"
            c.wait_until("it copies every cell")
            self.play(FadeOut(marker),
                      LaggedStart(*[TransformFromCopy(xs.cells[k], copies[k]) for k in range(3)],
                                  lag_ratio=0.25),
                      time_span(LaggedStart(*[GrowArrow(a) for a in (*c_arrs, ap_arr)], lag_ratio=0.25),
                                0.8, 1.8),
                      run_time=1.8)
            # "Front, constant time.  End, linear time."
            c.wait_until("front constant time")
            self.play(FadeIn(o1, shift=0.25 * DOWN), FlashAround(xcell, color=GOLD, time_width=1.5),
                      run_time=1.1)
            c.wait_until("linear time")
            self.play(FadeIn(on, shift=0.25 * DOWN),
                      LaggedStart(*[FlashAround(k, color=GOLD, time_width=1.5) for k in copies],
                                  lag_ratio=0.25), run_time=1.3)
            self.remove(on)
            self.add(*on)                                # O(n) is kept on its own next
        self.on = on

    # ── cells.5: an accumulator gains nothing in big O; the maxim ───────────────────
    def accumulator(self):
        L, R, ROW = -2.9, 3.0, -0.45
        on_tex, on_cap = self.on
        left_h = Mono("append", size=40, color=YELLOW).move_to([L, 2.6, 0])
        right_h = VGroup(Mono("append", size=40, color=YELLOW), T("+ accumulator?", size=40))
        right_h.arrange(RIGHT, buff=0.25).move_to([R, 2.6, 0])
        right_h[1].align_to(right_h[0], DOWN)
        it = VGroup(check_mark(GREEN), T("iterative", size=36)).arrange(RIGHT, buff=0.2).move_to([R, 1.75, 0])
        comp = T("but complicated", size=34, color=DIM).move_to([R, 1.18, 0])
        still = T("still copies every element", size=32).move_to([R, 0.45, 0])
        big_r = MathTex("O(n)", font_size=80, color=GOLD).move_to([R, ROW, 0])
        eq = MathTex("=", font_size=80).move_to([(L + R) / 2, ROW, 0])
        nog = T("no gain in big O", size=44).move_to([0, -2.3, 0])
        best = T("at best, a smaller constant", size=34, color=DIM).move_to([0, -3.0, 0])

        m1 = T("Never add an accumulator", size=56, color=YELLOW)
        m2 = T("merely out of habit.", size=56, color=YELLOW)
        maxim = VGroup(m1, m2).arrange(DOWN, buff=0.35).move_to(UP * 0.35)
        rule = Line(LEFT * 3.2, RIGHT * 3.2, stroke_width=2, color=DIM).next_to(maxim, DOWN, buff=0.45)

        with self.say("c4.cells.5") as c:
            # "Could an accumulator help, as it did for length?"
            c.wait_until("for length")
            sweep_clear(self, on_tex.animate.scale(80 / 60).move_to([L, ROW, 0]),
                        on_cap.animate.move_to([L, ROW - 0.8, 0]),
                        time_span(FadeIn(left_h, shift=0.2 * DOWN), 0.4, 1.0),
                        time_span(FadeIn(right_h, shift=0.2 * DOWN), 0.6, 1.2),
                        keep=[on_tex, on_cap], run_time=1.2)
            # "It could make append iterative, but only with real complication."
            c.wait_until("it could make")
            self.play(FadeIn(it, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("complication")
            self.play(FadeIn(comp, shift=0.2 * DOWN), run_time=0.8)
            # "And it would still have to copy every element of the first list, so it would still
            # need big O of en time and space."
            c.wait_until("still have to copy")
            self.play(FadeIn(still, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("big o")
            self.play(TransformFromCopy(on_tex, big_r), run_time=1.5)
            # "No gain in big O. ⏸"
            c.wait_until("nogain")
            self.play(FadeIn(eq), FadeIn(nog, shift=0.2 * UP), run_time=1.0)
            # "At best, a smaller constant factor, and the extra complication will probably cost more."
            c.wait_until("at best")
            self.play(FadeIn(best, shift=0.2 * UP), run_time=0.6)
            # "Here's a rule worth remembering.  Never add an accumulator merely out of habit."
            c.wait_until("remembering")
            sweep_clear(self, time_span(FadeIn(maxim, shift=0.3 * DOWN), 0.5, 1.5),
                        time_span(GrowFromCenter(rule), 0.6, 1.5), run_time=1.5)
        self.wait(2.7)
