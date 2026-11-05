"""Chapter 2, scene 2: the first pattern match, null. Its parts (function, clauses, bars,
patterns, answers), the two patterns as chapter 1's two shapes, then OCaml matching
null [1; 2; 3] clause by clause (x and l land on the parts of the chain) and null [].

Clips c2.null.1 - c2.null.5.

STATUS (paused): done: all 5 clips built, renders clean, dwell 0 flags, no clip overruns
(102.9 s vs 102.0 s narration+gaps + 1.15 s fade); remaining: optional polish only;
known issues: the shapes in null.3 are born from copies of the patterns (FadeTransform)
instead of the brief's arrows; the {cover} beat is shown with flashes only.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

SRC = "let null = function\n  | [] -> true\n  | x :: l -> false"
CODE_SIZE = 48          # the hero: ~7.5 units wide
HOME = UP * 0.9         # code centre while it is being read (null.1-2)
LEFT_EDGE = -6.3        # code's left edge while the shapes sit beside it (null.3)
TOP = UP * 1.9          # code centre during the matching (null.4-5)
SPREAD = 0.5            # null.3: clause 2 drops this much lower, so each clause has room
LIFT = 0.25             #   for its shape beside it; the code rises a little to stay centred
DIM_TO = 0.35           # spotlight: what we're not talking about (PATTERNS P9)
BAR = "#BBBBBB"         # the colour Code gives | and ->
CHAIN_Y = -1.1          # the list being matched
ROW_Y = (-2.5, -3.2)    # the two toplevel calls and their replies
IN_X, OUT_X = -5.0, 0.6  # left edges of the call column and the reply column
MARK_DX = 0.65          # ✗ / ✓ sit this far right of the code


# ── helpers (local to this scene) ───────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph: wrapping on-screen glyphs in a VGroup to
# animate them would pull them out of the Code (LESSONS.md).
def line_y(code, n):
    """Centre of line n (0-based), measured on the full-height | bars of lines 1 and 2."""
    y1 = code.find("|", line=1).get_y()
    y2 = code.find("|", line=2).get_y()
    return y1 + (1 - n) * (y1 - y2)


def hl(code, glyphs, color, line, h=0.74, pad=0.22):
    """The sliding highlight (P8): thin stroke, faint fill, behind the text, one line tall."""
    g = VGroup(*glyphs)
    r = Rectangle(width=g.width + pad, height=h, stroke_color=color, stroke_width=2)
    r.set_fill(color, opacity=0.22).set_z_index(-1)
    return r.move_to([g.get_x(), line_y(code, line), 0])


def hl_block(code, color):
    """One box around both clauses (lines 1-2)."""
    g = VGroup(*code.find("| [] -> true", line=1), *code.find("| x :: l -> false", line=2))
    top, bot = line_y(code, 1) + 0.37, line_y(code, 2) - 0.37
    r = Rectangle(width=g.width + 0.3, height=top - bot, stroke_color=color, stroke_width=2)
    r.set_fill(color, opacity=0.15).set_z_index(-1)
    return r.move_to([g.get_x(), (top + bot) / 2, 0])


def dimmed(code):
    """What fades back while we look at the patterns: line 0 and both answers."""
    return [*code.line(0), *code.find("-> true", line=1), *code.find("-> false", line=2)]


def set_alpha(glyphs, op):
    return [g.animate.set_opacity(op) for g in glyphs]


def recolor(glyphs, color):
    return [g.animate.set_color(color) for g in glyphs]


def check_mark(color=GREEN):
    m = VMobject().set_points_as_corners([[-0.24, 0.0, 0], [-0.07, -0.19, 0], [0.26, 0.23, 0]])
    return m.set_stroke(color, 8).set_cap_style(CapStyleType.ROUND)


def cross_mark(color=RED, r=0.19):
    return VGroup(Line([-r, -r, 0], [r, r, 0]), Line([-r, r, 0], [r, -r, 0])).set_stroke(color, 8)


def cursor():
    """The clause OCaml is trying right now (a small YELLOW pointer in the margin)."""
    return Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).rotate(-PI / 2).scale(0.16)


def span_brace(left_pt, right_pt, direction=UP, color=DIM, inset=0.06, buff=0.12):
    line = Line(left_pt + RIGHT * inset, right_pt + LEFT * inset)
    return Brace(line, direction, buff=buff, color=color)


def cons_shape():
    """`x :: l` as a picture: one cell holding x, its arrow pointing at the rest, l."""
    cell = ConsCell(0)
    cell.remove(cell.label)
    cell.label = Mono("x", size=CODE_SIZE, color=YELLOW).move_to(cell.box)
    cell.add(cell.label)
    rest = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=1.2, height=1.0),
                          num_dashes=26).set_stroke(TEAL, 3)
    rest.next_to(cell, RIGHT, buff=0.6)
    rest_lab = Mono("l", size=CODE_SIZE, color=TEAL).move_to(rest)
    arrow = Arrow(cell.tail_start(), rest.get_left(), buff=0, stroke_width=3, color=FG,
                  max_tip_length_to_length_ratio=0.3, tip_length=0.16)
    shape = VGroup(cell, arrow, rest, rest_lab).scale(1.15)
    shape.cell, shape.rest = cell, VGroup(rest, rest_lab)
    return shape


class NullByPattern(NarratedScene):
    def construct(self):
        self.code = Code(SRC, size=CODE_SIZE).move_to(HOME)
        self.parts()
        self.clauses()
        self.two_shapes()
        self.match_cons()
        self.match_nil()
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.wait(0.15)  # the last play() never renders its final (empty) frame

    # null.1: the code; `function`; instead of a name, the shapes
    def parts(self):
        code = self.code
        reply = Code("val null : 'a list -> bool = <fun>", size=30)
        reply.text.set_color(DIM)
        reply.find("'a").set_color(PINK)       # 'a stays PINK: scene 5 reads it
        reply.move_to([0, -2.0, 0])

        with self.say("c2.null.1") as c:
            # "Here's our first pattern match."
            self.play(FadeIn(code, shift=0.25 * DOWN, lag_ratio=0.03), run_time=2.0)
            # "It's a function called null, which tells you whether a list is empty."
            c.wait_until("called null")
            self.play(FlashAround(code.find("null"), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("whether")
            self.play(FadeIn(reply, shift=0.25 * UP), run_time=1.0)

            # "The keyword, function, says that null takes a single argument."
            c.wait_until("function", nth=1)
            self.box_a = hl(code, code.find("function"), BLUE, 0)
            self.play(FadeIn(self.box_a), FlashAround(code.find("function"), color=BLUE, time_width=1.5),
                      run_time=1.2)

            # "But instead of giving that argument a name, we list the shapes it might have."
            c.wait_until("we list the shapes")
            self.play(self.box_a.animate.become(hl_block(code, TEAL)), run_time=1.2)
        self.reply = reply

    # null.2: clauses, bars, patterns on the left, answers on the right
    def clauses(self):
        code, a = self.code, self.box_a
        b = a.copy()
        self.box_b = b

        def boxes(tok1, tok2, color):
            return (a.animate.become(hl(code, code.find(tok1, line=1), color, 1)),
                    b.animate.become(hl(code, code.find(tok2, line=2), color, 2)))

        clause_labs = VGroup(*[T("clause", size=34, color=DIM).move_to([0, line_y(code, i), 0])
                               for i in (1, 2)])
        clause_labs.set_x(code.get_right()[0] + 0.55 + clause_labs.width / 2)
        under = line_y(code, 2) - 0.85
        pat_col = VGroup(*code.find("[]", line=1), *code.find("x :: l", line=2))
        ans_col = VGroup(*code.find("true", line=1), *code.find("false", line=2))
        pat_lab = T("pattern", size=36, color=TEAL).move_to([pat_col.get_x(), under, 0])
        ans_lab = T("answer", size=36, color=YELLOW).move_to([ans_col.get_x(), under, 0])
        ans_lab.align_to(pat_lab, DOWN)

        with self.say("c2.null.2") as c:
            # "Each shape gets its own line, called a clause,"
            self.add(b)
            self.play(*boxes("| [] -> true", "| x :: l -> false", YELLOW), run_time=1.2)
            c.wait_until("called a clause")
            self.play(LaggedStart(*[FadeIn(m, shift=0.25 * LEFT) for m in clause_labs], lag_ratio=0.3),
                      run_time=1.0)
            # "and the clauses are separated by vertical bars."
            c.wait_until("vertical bars")
            self.play(*boxes("|", "|", BAR), run_time=1.0)

            # "On the left of each arrow is a pattern, a shape the list might have."
            c.wait_until("left")
            self.play(*boxes("[]", "x :: l", TEAL), FadeIn(pat_lab, shift=0.25 * UP), run_time=1.3)
            # "On the right is the answer to give back, if the list has that shape."
            c.wait_until("right")
            self.play(*boxes("true", "false", YELLOW), FadeIn(ans_lab, shift=0.25 * UP), run_time=1.3)
        self.clause_labs = clause_labs
        self.pat_lab, self.ans_lab = pat_lab, ans_lab

    # null.3: the two patterns are the two shapes from chapter 1; exactly one fits
    def two_shapes(self):
        code, a, b = self.code, self.box_a, self.box_b
        shift = RIGHT * (LEFT_EDGE - code.get_left()[0])
        code.generate_target()
        code.target.shift(shift + UP * LIFT)
        for g in code.target.line(2):
            g.shift(DOWN * SPREAD)
        for g in dimmed(code.target):
            g.set_opacity(DIM_TO)
        tgt = code.target
        x0 = tgt.get_right()[0] + 0.95       # left edge of the shape column
        below = shift + UP * LIFT + DOWN * SPREAD   # what sits under clause 2 moves with it

        nil_shape = Nil(size=80)
        nil_shape.move_to([x0 + nil_shape.width / 2, line_y(tgt, 1), 0])
        cons = cons_shape()
        cons.move_to([x0 + cons.width / 2, line_y(tgt, 2), 0])
        caption = VGroup(T("the two shapes", size=34), T("from chapter 1", size=34)).arrange(DOWN, buff=0.15)
        caption.next_to(cons, DOWN, buff=0.55).set_x(VGroup(nil_shape, cons).get_x())

        with self.say("c2.null.3") as c:
            # "Now look closely at the two patterns."  The code steps left to make room; the
            # rest of each line fades back; the boxes go back to the patterns.
            self.play(MoveToTarget(code),
                      a.animate.become(hl(tgt, tgt.find("[]", line=1), TEAL, 1)),
                      b.animate.become(hl(tgt, tgt.find("x :: l", line=2), TEAL, 2)),
                      self.reply.animate.shift(below + DOWN * 0.35), self.pat_lab.animate.shift(below),
                      self.ans_lab.animate.shift(below).set_opacity(DIM_TO),
                      *[FadeOut(m) for m in self.clause_labs], run_time=1.6)

            # "The first is the empty list."  (the picture comes out of the pattern, P5)
            c.wait_until("empty")
            self.play(FadeTransform(code.find("[]", line=1).copy(), nil_shape), run_time=1.5)
            # "The second is ex cons ell, some head consed onto some tail."
            c.wait_until("conspat")
            self.play(FadeTransform(code.find("x :: l", line=2).copy(), cons), run_time=1.8)
            c.wait_until("some head")
            self.play(LaggedStart(FlashAround(cons.cell, color=YELLOW, time_width=1.5),
                                  FlashAround(cons.rest, color=TEAL, time_width=1.5), lag_ratio=1.0),
                      run_time=c.until("these", floor=1.6) * 0.9)

            # "These are exactly the two shapes of a list from chapter one."
            c.wait_until("exactly")
            self.play(FadeIn(caption, shift=0.25 * UP, lag_ratio=0.2), run_time=1.2)

            # "No list has both shapes, and every list has one of them."
            c.wait_until("every list")
            self.play(LaggedStart(FlashAround(nil_shape, color=TEAL, time_width=1.5),
                                  FlashAround(cons, color=BLUE, time_width=1.5), lag_ratio=0.5),
                      run_time=1.6)
            # "So for any list at all, exactly one clause fits."  (one, then the other)
            c.wait_until("exactly one")
            self.play(LaggedStart(FlashAround(code.line(1), color=YELLOW, time_width=1.5),
                                  FlashAround(code.line(2), color=YELLOW, time_width=1.5), lag_ratio=1.0),
                      run_time=1.8)
        self.shapes = [nil_shape, cons, caption]

    # null.4: null [1; 2; 3], tried clause by clause from the top
    def match_cons(self):
        code = self.code
        code.generate_target()
        for g in code.target.line(2):
            g.shift(UP * SPREAD)             # clause 2 back in its place
        code.target.move_to(TOP)
        for g in code.target.text:
            g.set_opacity(1)
        tgt = code.target

        call = Code("null [1; 2; 3]", size=40)
        call.find("null").set_color(YELLOW)
        call.move_to([IN_X, ROW_Y[0], 0], aligned_edge=LEFT)
        reply = Code("- : bool = false", size=40).move_to([OUT_X, ROW_Y[0], 0], aligned_edge=LEFT)

        chain = ConsChain([1, 2, 3]).move_to([0, CHAIN_Y, 0])
        cells = chain.cells
        top_y = cells[0].box.get_top()[1]
        x_br = span_brace(cells[0].box.get_corner(UL), cells[0].box.get_corner(UR), color=YELLOW)
        l_br = span_brace(cells[1].box.get_corner(UL), np.array([chain.nil.get_right()[0], top_y, 0]),
                          color=TEAL)
        x_lab = Mono("x", size=CODE_SIZE, color=YELLOW).next_to(x_br, UP, buff=0.12)
        l_lab = Mono("l", size=CODE_SIZE, color=TEAL).next_to(l_br, UP, buff=0.12).align_to(x_lab, DOWN)
        probe = Code("[]", size=CODE_SIZE).move_to(x_lab)          # clause 1's pattern, tried on the list

        mark_x = tgt.get_right()[0] + MARK_DX
        no = cross_mark().move_to([mark_x, line_y(tgt, 1), 0])
        yes = check_mark().move_to([mark_x, line_y(tgt, 2), 0])
        cur = cursor()
        cur_x = tgt.get_left()[0] - 0.4
        cur.move_to([cur_x, line_y(tgt, 1), 0])

        with self.say("c2.null.4") as c:
            # "So how does OCaml pick the clause?"  The shapes have made their point; the code
            # goes back to the top, whole again, for the matching.
            self.play(LaggedStart(*[FadeOut(m) for m in (*self.shapes, self.box_a, self.box_b, self.reply,
                                                         self.pat_lab, self.ans_lab)], lag_ratio=0.08),
                      time_span(MoveToTarget(code), 0.4, 1.8), run_time=1.8)

            # "Let's call null on the list one, two, three."  (the chain comes out of the call, P5)
            c.wait_until("call null")
            self.play(FadeIn(call, shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("one")
            self.play(FadeTransform(call.find("[1; 2; 3]").copy(), chain), run_time=1.6)

            # "OCaml tries the clauses in order, from the top."
            c.wait_until("tries")
            self.play(FadeIn(cur, shift=0.3 * RIGHT), run_time=1.0)

            # "Is this list empty?"  Clause 1's pattern is held up against the list.
            c.wait_until("first")
            box = hl(code, code.find("[]", line=1), TEAL, 1)
            self.play(FadeIn(box), TransformFromCopy(code.find("[]", line=1), probe.text), run_time=1.5)
            # "No, so the first clause doesn't fit."  The list starts with a cell, not with nil:
            # the failed pattern turns into the ✗ beside its clause.
            c.wait_until("no")
            self.play(FlashAround(cells[0].box, color=RED, time_width=1.5),
                      ReplacementTransform(probe.text, no), run_time=1.3)
            c.wait_until("doesn't fit")
            self.play(*set_alpha(code.line(1), DIM_TO), box.animate.set_opacity(0), run_time=1.0)

            # "Is it some head, ex, consed onto some tail, ell?"
            c.wait_until("second")
            box.become(hl(code, code.find("x :: l", line=2), TEAL, 2)).set_opacity(0)
            self.play(cur.animate.set_y(line_y(code, 2)), box.animate.set_fill(opacity=0.22).set_stroke(opacity=1),
                      run_time=1.2)
            c.wait_until("ex")
            x_src, l_src = code.find("x", line=2), code.find("l", line=2)
            self.play(TransformFromCopy(x_src, x_lab), *recolor(x_src, YELLOW), run_time=1.2)
            c.wait_until("ell")
            self.play(TransformFromCopy(l_src, l_lab), *recolor(l_src, TEAL), run_time=c.until("yes", floor=0.8))

            # "Yes."
            c.wait_until("yes")
            self.play(Create(yes), run_time=0.8)
            # "Ex matches the first element, one,"
            c.wait_until("ex matches")
            self.play(GrowFromCenter(x_br), cells[0].box.animate.set_stroke(YELLOW), run_time=1.5)
            # "and ell matches the rest, two, three."
            c.wait_until("ell matches")
            self.play(GrowFromCenter(l_br),
                      *[m.animate.set_stroke(TEAL) for cell in cells[1:] for m in (cell.box, cell.ptr)],
                      run_time=1.5)

            # "So the second clause fits, and null gives back false."  (the answer comes out
            # of the clause that fit, P5)
            c.wait_until("false")
            self.play(FlashAround(code.line(2), color=GREEN, time_width=1.5), run_time=1.3)
            c.wait_until("null gives back")
            body, prefix = reply.find("false"), reply.find("- : bool =")
            self.play(TransformFromCopy(code.find("false", line=2), body), FadeIn(prefix, shift=0.2 * LEFT),
                      run_time=1.4)
            self.remove(body, prefix)
            self.add(reply)

        self.call1, self.reply1 = call, reply
        self.matched = [x_lab, x_br, l_lab, l_br, chain, no, yes]
        self.box, self.cur = box, cur

    # null.5: null [] fits clause 1 at once; x and l name the parts, unused by null
    def match_nil(self):
        code, box, cur = self.code, self.box, self.cur
        call = Code("null []", size=40)
        call.find("null").set_color(YELLOW)
        call.move_to([IN_X, ROW_Y[1], 0], aligned_edge=LEFT)
        reply = Code("- : bool = true", size=40).move_to([OUT_X, ROW_Y[1], 0], aligned_edge=LEFT)
        nil = Nil(size=72).move_to([0, CHAIN_Y, 0])
        yes = check_mark().move_to([code.get_right()[0] + MARK_DX, line_y(code, 1), 0])

        pat = code.find("x :: l", line=2)
        unused_br = Brace(pat, DOWN, buff=0.3, color=DIM)
        unused = T("never used", size=32, color=DIM).next_to(unused_br, DOWN, buff=0.12)

        with self.say("c2.null.5") as c:
            # "Now call null on the empty list."  The last match clears; its result stays, dimmed.
            self.play(LaggedStart(*[FadeOut(m) for m in self.matched], lag_ratio=0.06),
                      *set_alpha(code.line(1), 1),
                      self.call1.animate.set_opacity(0.45), self.reply1.animate.set_opacity(0.45),
                      time_span(FadeIn(call, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            c.wait_until("empty list")
            self.play(TransformFromCopy(call.find("[]"), nil.label), run_time=1.2)

            # "This time, the very first clause fits, so the answer is true."
            c.wait_until("fits")
            self.play(cur.animate.set_y(line_y(code, 1)),
                      box.animate.become(hl(code, code.find("[]", line=1), TEAL, 1)), run_time=1.0)
            c.wait_until("clause fits")
            self.play(Create(yes), FlashAround(nil, color=TEAL, time_width=1.5), run_time=1.0)
            c.wait_until("is true")
            body, prefix = reply.find("true"), reply.find("- : bool =")
            self.play(TransformFromCopy(code.find("true", line=1), body), FadeIn(prefix, shift=0.2 * LEFT),
                      run_time=1.4)
            self.remove(body, prefix)
            self.add(reply)

            # "Notice something else. The second pattern gives names to the parts of the list,
            #  ex and ell, even though null never uses them."
            c.wait_until("the second pattern")
            self.play(box.animate.become(hl(code, pat, TEAL, 2)), run_time=1.0)
            c.wait_until("ex and ell")
            self.play(LaggedStart(FlashAround(code.find("x", line=2), color=YELLOW, time_width=1.5),
                                  FlashAround(code.find("l", line=2), color=TEAL, time_width=1.5),
                                  lag_ratio=0.35), run_time=1.4)
            c.wait_until("never uses")
            self.play(GrowFromCenter(unused_br), FadeIn(unused, shift=0.25 * DOWN), run_time=1.2)

            # "Those names are where patterns get their real power, as the next two functions show."
            c.wait_until("real power")
            self.play(FlashAround(code.find("x", line=2), color=YELLOW, time_width=1.5),
                      FlashAround(code.find("l", line=2), color=TEAL, time_width=1.5), run_time=1.5)
