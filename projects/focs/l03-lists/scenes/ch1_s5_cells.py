"""Chapter 1, scene 5: inside the computer. One cons cell, the 3 -> 5 -> 9 -> [] chain,
consing 1 onto the front (the wrong picture first), O(1), and sharing between x and y.

Clips c1.cells.1 - c1.cells.4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, TransformMatchingStrings, VShowPassingFlash, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# The chain is drawn at 1.08x. That is the most the "shuffle" picture allows: it needs the
# chain's width plus a cell's step on BOTH sides (gap in front + chain pushed right).
S = 1.08
STEP = (CELL + PTR_W + LINK) * S   # distance between neighbouring cells
ROW_Y = -0.1                        # height of the cell row


# ── helpers (local to this scene) ───────────────────────────────────────────────
def slink(src, dst, color=FG):
    """lib.style.link at this scene's scale (tip scaled like the chain's own arrows)."""
    return Arrow(src.tail_start(), dst.entry(), buff=0, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16 * S)


def arrow_between(start, end, color=FG, width=3, tip=0.16):
    return Arrow(start, end, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=tip)


def flash_along(src, dst, color=YELLOW, run_time=1.0):
    """A bright pulse travelling along one pointer arrow (PATTERNS P6, along a path)."""
    path = Line(src.tail_start(), dst.entry()).set_stroke(color, 8)
    return VShowPassingFlash(path, time_width=0.6, run_time=run_time)


def span_brace(left_pt, right_pt, direction=DOWN, color=DIM, inset=0.06, buff=0.18):
    """A brace under (or over) the horizontal span left_pt..right_pt."""
    line = Line(left_pt + RIGHT * inset, right_pt + LEFT * inset)
    return Brace(line, direction, buff=buff, color=color)


def name_pointer(src, target, color, direction):
    """`x = [3; 5; 9]` under (DOWN) or over (UP) a cell, with an arrow from the name.

    Returns (name glyph, rest of the line, arrow): the name and arrow appear first,
    the value afterwards.
    """
    code = Code(src, size=38)
    name = code.text[0]
    rest = VGroup(*code.text[1:])
    name.set_color(color)
    edge = target.box.get_edge_center(direction)
    code.shift(edge + direction * 1.1 - name.get_center())
    code.shift(RIGHT * (target.box.get_x() - name.get_x()))
    start = name.get_edge_center(-direction) - direction * 0.08
    arr = Arrow(start, edge, buff=0.06, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.35, tip_length=0.17)
    return name, rest, arr


def padlock(color=FG, h=0.46):
    body = RoundedRectangle(corner_radius=0.06, width=h * 1.15, height=h,
                            stroke_color=color, stroke_width=3, fill_opacity=0)
    shackle = Arc(radius=h * 0.36, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    legs = VGroup(Line(shackle.get_start(), shackle.get_start() + DOWN * 0.05),
                  Line(shackle.get_end(), shackle.get_end() + DOWN * 0.05)).set_stroke(color, 3)
    hole = Dot(body.get_center(), radius=0.045, color=color)
    return VGroup(body, shackle, legs, hole)


def outline_to(cells, color):
    # A list, to unpack into play(): wrapping these in an AnimationGroup would add a new Group
    # of the boxes on top of the scene, and their opaque fill would hide the values.
    return [m.animate.set_stroke(color) for c in cells for m in (c.box, c.ptr)]


class InsideTheComputer(NarratedScene):
    def construct(self):
        chain = self.one_cell()
        new, new_arrow = self.cons_one(chain)
        self.constant(chain, new, new_arrow)
        self.sharing(chain, new, new_arrow)

    # cells.1: one big cell (value + arrow), which then becomes the head of 3 -> 5 -> 9 -> []
    def one_cell(self):
        chain = ConsChain([3, 5, 9]).scale(S).move_to(UP * ROW_Y)
        title = T("Inside the computer", size=50).to_edge(UP, buff=0.55)

        # the first cell on its own, as the hero: ~2/3 of the frame width with its arrow
        big = ConsCell(3).scale(2.0)
        rest_lbl = T("rest of the list", size=38, color=DIM)
        rest_box = DashedVMobject(
            RoundedRectangle(corner_radius=0.2, width=rest_lbl.width + 0.9, height=2.0),
            num_dashes=48).set_stroke(DIM, 3)
        gap = 2.0
        total = big.width + gap + rest_box.width
        big.move_to(RIGHT * (-total / 2 + big.width / 2) + UP * ROW_Y)
        rest_box.move_to(RIGHT * (total / 2 - rest_box.width / 2) + UP * ROW_Y)
        rest_lbl.move_to(rest_box)
        intro_arrow = arrow_between(big.tail_start(), rest_box.get_left(), width=5, tip=0.3)

        v_brace = span_brace(big.box.get_corner(DL), big.box.get_corner(DR))
        v_lab = T("value", size=40).next_to(v_brace, DOWN, buff=0.18)
        a_brace = span_brace(big.ptr.get_corner(DL), intro_arrow.get_end() * RIGHT + big.ptr.get_bottom() * UP)
        a_lab = T("arrow", size=40).next_to(a_brace, DOWN, buff=0.18)
        a_lab.align_to(v_lab, UP)

        with self.say("c1.cells.1") as c:
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.0)

            # "Each cons builds one small cell in memory."
            c.wait_until("cells")
            self.play(Create(big.box), Create(big.ptr), run_time=1.8)

            # "A cell holds two things:"  (preview both compartments, P2)
            c.wait_until("value")
            self.play(LaggedStart(FlashAround(big.box, color=BLUE, time_width=1.5),
                                  FlashAround(big.ptr, color=BLUE, time_width=1.5), lag_ratio=0.5),
                      run_time=1.5)

            # "...the value,"
            c.wait_until("slot")
            self.play(Write(big.label), GrowFromCenter(v_brace), FadeIn(v_lab, shift=0.25 * UP),
                      run_time=c.until("arrow", floor=0.6))
            # "...and an arrow pointing to the rest of the list."
            self.play(FadeIn(big.dot, scale=0.5), GrowArrow(intro_arrow),
                      LaggedStart(GrowFromCenter(a_brace), FadeIn(a_lab, shift=0.25 * UP), lag_ratio=0.3),
                      run_time=1.3)
            c.wait_until("the rest of")
            self.play(Create(rest_box), FadeIn(rest_lbl), run_time=1.2)

            # "So three, five, nine is a chain of three cells, ending in nil."
            # The cell shrinks into the chain's head; "rest of the list" becomes the real rest (P5).
            # The "value" / "arrow" labels ride along onto the head cell and stay a while.
            c.wait_until("chain")
            head = chain.cells[0]
            v_brace2 = span_brace(head.box.get_corner(DL), head.box.get_corner(DR), buff=0.15)
            v_lab2 = T("value", size=34).next_to(v_brace2, DOWN, buff=0.12)
            # (at this size "arrow" goes above the pointer, so the two labels can't run together)
            a_brace2 = span_brace(head.ptr.get_corner(UL),
                                  chain.arrows[0].get_end() * RIGHT + head.ptr.get_top() * UP, direction=UP, buff=0.15)
            a_lab2 = T("arrow", size=34).next_to(a_brace2, UP, buff=0.12)
            rest_parts = VGroup(chain.cells[1], chain.arrows[1], chain.cells[2], chain.arrows[2], chain.nil)
            self.play(ReplacementTransform(VGroup(big, intro_arrow, v_brace, v_lab),
                                           VGroup(head, chain.arrows[0], v_brace2, v_lab2)),
                      FadeTransform(VGroup(a_brace, a_lab), VGroup(a_brace2, a_lab2)),
                      FadeTransform(VGroup(rest_box, rest_lbl), rest_parts), run_time=2.0)
            c.wait_until("ending in nil")
            self.play(FlashAround(chain.nil, color=TEAL, time_width=1.5), run_time=1.2)
        self.add(chain)
        self.title = title
        self.cell_labels = VGroup(v_brace2, v_lab2, a_brace2, a_lab2)
        return chain

    # cells.2: the tempting wrong picture, crossed out; then one new cell and one arrow
    def cons_one(self, chain):
        code = Code("1 :: [3; 5; 9]", size=42).move_to(UP * 2.35)
        one_glyph = code.find("1")
        cells = chain.cells
        targets = cells[1:] + [chain.nil]

        slot = DashedVMobject(Square(CELL * S), num_dashes=16).set_stroke(DIM, 3)
        slot.move_to(cells[0].box)
        slot_one = value_label(1, color=YELLOW).scale(S).move_to(slot)

        new = ConsCell(1, color=YELLOW).scale(S).move_to(cells[0].get_center() + LEFT * STEP)
        new_arrow = slink(new, cells[0], color=YELLOW)

        with self.say("c1.cells.2") as c:
            self.play(FadeOut(self.title, shift=0.3 * UP), run_time=1.0)
            # "Suppose we want to put a one on the front."
            c.wait_until("put a one")
            self.play(FadeIn(code, shift=0.3 * DOWN), run_time=1.2)

            # "You might imagine the computer shuffling every element along, to make room."
            c.wait_until("shuffle")
            for arr, src, dst in zip(chain.arrows, cells, targets):
                arr.add_updater(lambda a, s=src, d=dst: a.become(slink(s, d)))
            movers = [chain.nil, cells[2], cells[1], cells[0]]
            self.play(LaggedStart(*[m.animate.shift(RIGHT * STEP) for m in movers], lag_ratio=0.35),
                      time_span(FadeOut(self.cell_labels), 0, 1.0), run_time=2.4)
            for arr in chain.arrows:
                arr.clear_updaters()
            self.play(FadeIn(slot), TransformFromCopy(one_glyph, slot_one), run_time=1.3)

            # "It doesn't do that at all."
            c.wait_until("nope")
            wrong = VGroup(slot, chain)
            fog = Rectangle(width=wrong.width + 0.6, height=2.2).set_stroke(width=0)
            fog.set_fill(BG, opacity=0.6).move_to(wrong)
            cross = Cross(stroke_color=RED, stroke_width=10)
            cross.stretch_to_fit_width(3.4).stretch_to_fit_height(2.4).move_to(wrong)
            self.play(FadeIn(fog), Create(cross), run_time=1.0)

            # "It builds one new cell,"  (beside the crossed-out picture, which stays readable)
            c.wait_until("new")
            self.play(Create(VGroup(new.box, new.ptr)), run_time=1.5)
            # "holding the one,"  The wrong picture gives way to the right one, and the 1 comes out
            # of the code that asked for it (P5).
            c.wait_until("holding the one")
            self.play(FadeOut(VGroup(fog, cross, slot, slot_one)), chain.animate.shift(LEFT * STEP),
                      TransformFromCopy(one_glyph, new.label), run_time=c.until("point", floor=0.8))
            # "and points its arrow at the list that was already there."
            self.play(FadeIn(new.dot, scale=0.5), GrowArrow(new_arrow), run_time=1.4)
            c.wait_until("already there")
            self.play(FlashAround(VGroup(*cells, chain.nil), color=BLUE, time_width=1.5), run_time=1.5)
        self.code = code
        return new, new_arrow

    # cells.3: one cell, one arrow, whatever the length: O(1)
    def constant(self, chain, new, new_arrow):
        cells = chain.cells
        bot = cells[0].box.get_bottom()[1]

        n_brace = span_brace(new.get_corner(DL), new.get_corner(DR), color=GOLD)
        n_lab = T("1 new cell", size=38, color=GOLD).next_to(n_brace, DOWN, buff=0.18)
        n_lab.align_to(new, LEFT)

        def size_brace(right_x):
            return span_brace(np.array([cells[0].get_left()[0], bot, 0]), np.array([right_x, bot, 0]))

        s_brace = size_brace(chain.nil.get_right()[0])
        s_lab = T("3 elements", size=38).next_to(s_brace, DOWN, buff=0.18)
        n_lab.align_to(s_lab, DOWN)

        # the long version: 3 -> 5 -> 9 -> ... -> []
        old_nil_pos = chain.nil.get_center()
        dots = MathTex(r"\cdots", font_size=60).move_to(old_nil_pos)
        far_nil = old_nil_pos + RIGHT * 1.75
        dots_arrow = arrow_between(dots.get_right() + RIGHT * 0.15,
                                   far_nil + LEFT * (chain.nil.width / 2 + 0.05), tip=0.16 * S)
        l_brace = size_brace(far_nil[0] + chain.nil.width / 2)
        l_lab = T("3 million elements", size=38).next_to(l_brace, DOWN, buff=0.18)

        o1 = MathTex(r"O(1)", font_size=84, color=GOLD).move_to(UP * 2.3)
        const = T("constant time", size=36, color=DIM).next_to(o1, DOWN, buff=0.22)

        with self.say("c1.cells.3") as c:
            # "One new cell, one arrow."
            self.play(FadeOut(self.code, shift=0.3 * UP), FlashAround(new, time_width=1.5), run_time=1.1)
            c.wait_until("one arrow")
            self.play(flash_along(new, cells[0]), run_time=1.0)

            # "It doesn't matter whether the list has three elements or three million."
            c.wait_until("it doesn't matter")
            self.play(GrowFromCenter(n_brace), FadeIn(n_lab, shift=0.25 * UP), run_time=1.2)
            c.wait_until("three elements")
            self.play(GrowFromCenter(s_brace), FadeIn(s_lab, shift=0.25 * UP), run_time=c.until("three million", floor=0.6))
            # the list grows; its label follows; the new cell does not change
            self.play(chain.nil.animate.move_to(far_nil), FadeIn(dots), GrowArrow(dots_arrow),
                      Transform(s_brace, l_brace), TransformMatchingStrings(s_lab, l_lab), run_time=1.6)

            # "Cons always does the same tiny amount of work."
            c.wait_until("same tiny")
            self.play(FlashAround(VGroup(new, n_brace, n_lab), color=GOLD, time_width=1.5), run_time=1.5)

            # "We say it takes constant time, written big O of one."  (O(1) comes out of "1 new cell")
            c.wait_until("o1")
            self.play(FadeTransform(n_lab.copy(), o1), run_time=1.8)
            self.play(FadeIn(const, shift=0.25 * UP), run_time=1.0)
        self.cost = VGroup(n_brace, n_lab, s_brace, l_lab)
        self.o1 = VGroup(o1, const)
        self.long_bits = VGroup(dots, dots_arrow)
        self.old_nil_pos = old_nil_pos

    # cells.4: x is still [3; 5; 9], y = [1; 3; 5; 9], they share cells, nothing ever changes
    def sharing(self, chain, new, new_arrow):
        cells = chain.cells
        old = VGroup(*cells, chain.nil)

        x_name, x_rest, x_arr = name_pointer("x = [3; 5; 9]", cells[0], BLUE, DOWN)
        y_name, y_rest, y_arr = name_pointer("y = [1; 3; 5; 9]", new, YELLOW, UP)

        with self.say("c1.cells.4") as c:
            # back to the real three-element list (lagged sweep, P18)
            # The cells.3 picture stays through "And there's a second, more surprising consequence."
            # On "The old list" it goes back to [3; 5; 9]; O(1) shrinks into the corner and stays.
            c.wait_until("old")
            self.play(LaggedStart(*[FadeOut(m) for m in (*self.cost, *self.long_bits)], lag_ratio=0.1),
                      chain.nil.animate.move_to(self.old_nil_pos),
                      self.o1.animate.scale(0.8).to_corner(UR, buff=0.5), run_time=c.until("three", floor=0.8))

            # "The old list, three, five, nine, hasn't changed at all."
            c.wait_until("three")
            self.play(FlashAround(old, color=BLUE, time_width=1.5), run_time=2.0)

            # "If we had called it ex, then ex still means three, five, nine."
            c.wait_until("x")
            self.play(FadeIn(x_name, shift=0.25 * UP), GrowArrow(x_arr), run_time=1.2)
            c.wait_until("still means")
            self.play(FadeIn(x_rest, shift=0.25 * LEFT), run_time=1.0)

            # "The new list, call it why, is one, three, five, nine."
            c.wait_until("y")
            self.play(FadeIn(y_name, shift=0.25 * DOWN), GrowArrow(y_arr), run_time=1.2)
            c.wait_until("is one")
            self.play(FadeIn(y_rest, shift=0.25 * LEFT), run_time=1.0)

            # "And the two lists share the very same cells."  (the colour change stays, P6)
            c.wait_until("share")
            shared_box = SurroundingRectangle(old, color=TEAL, buff=0.2, corner_radius=0.1)
            self.play(*outline_to(cells, TEAL), Create(shared_box), run_time=1.6)
            shared_lab = T("shared by x and y", size=36, color=TEAL)
            shared_lab.next_to(shared_box, UP, buff=0.2).align_to(shared_box, RIGHT)
            c.wait_until("very same")
            self.play(FadeIn(shared_lab, shift=0.25 * DOWN), run_time=1.0)

            # "This sharing is only safe because OCaml lists never change once they're built."
            c.wait_until("immut")
            note = VGroup(padlock(), T("never changes", size=38)).arrange(RIGHT, buff=0.25)
            note.move_to([shared_box.get_x(), -2.6, 0])
            self.play(FadeIn(note, shift=0.25 * UP), run_time=1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.15)  # the last play() never renders its final (empty) frame
