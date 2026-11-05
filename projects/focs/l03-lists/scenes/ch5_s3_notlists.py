"""Chapter 5, scene 3: a string is not a list, a char is not a string, the form of a char.

Clips c5.type.1 – c5.type.4. Opens on the hook's question from scene 1 ([c][a][t], a dashed
cons-chain ghost, a GOLD "?") and turns the "?" into the answer (P23).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, select, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

QUOTE = YELLOW   # quote marks (chapter 5 convention, from scene 2)
BOX = 1.5        # letter-box side in the hook picture (as ch5_s1_hook)
CAT_Y, Q_Y, GHOST_Y = 1.75, -0.05, -1.85
DIMMED = 0.35    # earlier content stepping back (PATTERNS P9)
ERR = 30         # OCaml's error text
CODE = 56        # the rejected inputs
HERO = 88        # the character constant 'c' (bigger and Menlo's quote turns into a bar)


# ── helpers (local to this scene) ──────────────────────────────────────────────
# Parts of a Code are animated glyph by glyph: wrapping them in a VGroup/AnimationGroup
# pulls them out of the Code (LESSONS.md).
def chars(code, ch):
    """Every glyph of `code` that is the character `ch`, as a list."""
    return [g for k in range(code.src.count(ch)) for g in code.find(ch, nth=k)]


def paint_quotes(code):
    for g in chars(code, '"') + chars(code, "'"):
        g.set_color(QUOTE)
    return code


def set_op(mob, op):
    """Dim/restore in place (P9): opacity goes on the fill of filled parts (text, arrow
    tips) and on the stroke of outlines, which stay unfilled (as in ch1_s3_compare)."""
    for leaf in mob.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_opacity(op)
        else:
            leaf.set_stroke(opacity=op)
    return mob


def restyle(mob, op=None, shift=None):
    """One Transform that dims/restores and moves `mob` together."""
    t = mob.copy()
    if op is not None:
        set_op(t, op)
    if shift is not None:
        t.shift(shift)
    return Transform(mob, t)


def underline(glyphs, color, buff=0.12, width=5):
    g = VGroup(*glyphs)
    return Line(g.get_corner(DL), g.get_corner(DR), color=color, stroke_width=width).shift(DOWN * buff)


def hl_box(glyphs, line, color):
    """The sliding highlight (P8): faint fill behind the text, as tall as the line."""
    g = VGroup(*glyphs)
    r = Rectangle(width=g.width + 0.2, height=line.height + 0.22)
    r.move_to([g.get_x(), line.get_y(), 0]).set_stroke(color, 2).set_fill(color, 0.22)
    return r.set_z_index(-1)


def error_lines(expected):
    """OCaml's reply, verified with `ocaml` (5.4.1); its one long line is wrapped in two:
    Error: This constant has type string but an expression was expected of type <expected>"""
    a = Mono("Error: This constant has type string", size=ERR)
    b = Mono(f"but an expression was expected of type {expected}", size=ERR)
    select(a, "Error:")[0].set_color(RED)
    select(a, "string")[0].set_color(GREEN)
    if expected == "'a list":
        select(b, "'a")[0].set_color(PINK)
        select(b, "list")[0].set_color(GREEN)
    else:
        select(b, expected)[0].set_color(GREEN)
    VGroup(a, b).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    return a, b


# ── the hook picture, exactly as ch5_s1_hook.py leaves it (geometry copied from there) ──
def letter_box(ch):
    sq = Square(BOX, stroke_color=BLUE, stroke_width=3)
    return VGroup(sq, Mono(ch, size=80, color=GOLD).move_to(sq))


def ghost_cell(ch, at):
    """A dashed, dim cons cell with its value box centred at `at`."""
    sq = Square(CELL).move_to(at).set_stroke(DIM, 3)
    tr, br = sq.get_corner(UR), sq.get_corner(DR)
    ptr_path = VMobject().set_points_as_corners([tr, tr + RIGHT * PTR_W, br + RIGHT * PTR_W, br])
    ptr_path.set_stroke(DIM, 3)
    box = DashedVMobject(sq, num_dashes=16, dashed_ratio=0.55)
    ptr = DashedVMobject(ptr_path, num_dashes=9, dashed_ratio=0.55)
    dot = Dot(at + RIGHT * (CELL + PTR_W) / 2, radius=0.07, color=DIM)
    label = Mono(ch, size=44, color=DIM).move_to(at)
    cell = VGroup(box, ptr, dot, label)
    cell.left, cell.tail, cell.label = sq.get_left(), dot.get_center(), label
    return cell


def ghost_chain(letters, center):
    """['c'; 'a'; 't'] as a dashed, dim cons chain: what a string *might* secretly be."""
    step = CELL + PTR_W + LINK
    width = len(letters) * step + 0.6
    x0 = center[0] - width / 2 + CELL / 2
    cells = [ghost_cell(ch, np.array([x0 + i * step, center[1], 0])) for i, ch in enumerate(letters)]
    nil = Text("[]", font=MONO, font_size=42, color=DIM)
    nil.move_to([x0 + len(letters) * step - CELL / 2 + nil.width / 2, center[1], 0])
    targets = [c.left for c in cells[1:]] + [nil.get_left() + LEFT * 0.05]
    arrows = [Arrow(c.tail, t, buff=0, stroke_width=3, color=DIM,
                    max_tip_length_to_length_ratio=0.3, tip_length=0.16)
              for c, t in zip(cells, targets)]
    chain = VGroup(*cells, *arrows, nil)
    chain.cells, chain.arrows, chain.nil = cells, arrows, nil
    return chain


def lit(chain):
    """The ghost drawn as a real list: blue cells, bright values, arrows and nil."""
    t = chain.copy()
    for cell in t.cells:
        cell[0].set_stroke(BLUE)
        cell[1].set_stroke(BLUE)
        cell[2].set_color(FG)
        cell[3].set_color(FG)
    for a in t.arrows:
        a.set_color(FG)
    t.nil.set_color(TEAL)
    return t


class StringsAreNotLists(NarratedScene):
    def construct(self):
        self.the_answer()
        block1 = self.append_strings()
        block2 = self.char_vs_string(block1)
        self.char_form(block1, block2)
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.05), run_time=1.0)
        self.wait(0.1)  # a truly empty last frame

    def sweep_clear(self, *incoming, keep=(), run_time=1.5):
        """Clear the board in a lagged sweep (P18), alongside whatever needs the space."""
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        old = [m for m in self.mobjects if id(m) not in keep_ids]
        self.play(LaggedStart(*[FadeOut(m) for m in old], lag_ratio=0.1), *incoming, run_time=run_time)

    # type.1: the hook's question comes back, and the "?" becomes the answer
    def the_answer(self):
        boxes = VGroup(*[letter_box(ch) for ch in "cat"]).arrange(RIGHT, buff=0).move_to(UP * CAT_Y)
        q_left = Mono('"', size=110, color=QUOTE).next_to(boxes, LEFT, buff=0.3)
        q_right = Mono('"', size=110, color=QUOTE).next_to(boxes, RIGHT, buff=0.3)
        for qm in (q_left, q_right):
            qm.align_to(boxes, UP).shift(DOWN * 0.1)
        string = VGroup(q_left, boxes, q_right)
        q = T("?", size=110, color=GOLD).move_to(UP * Q_Y)
        ghost = ghost_chain("cat", UP * GHOST_Y)
        dim_ghost, lit_ghost = ghost.copy(), lit(ghost)

        some = T("in some languages", size=34, color=DIM).next_to(ghost, DOWN, buff=0.4)
        not_ocaml = T("not in OCaml", size=34, color=RED).move_to(some)
        cross = Cross(SurroundingRectangle(ghost, buff=0.2), stroke_color=RED, stroke_width=7)
        answer = T("its own type", size=60, color=GREEN).move_to(q)

        # the merge: one value, "cat" at word spacing inside a single box
        word = Mono('"cat"', size=80).move_to(UP * CAT_Y)
        word[1:4].set_color(GOLD)
        whole = RoundedRectangle(corner_radius=0.22, width=word.width + 0.9, height=BOX,
                                 stroke_color=BLUE, stroke_width=3).move_to(UP * CAT_Y)
        word.align_to(boxes[0][1], DOWN)   # keep the letters' baseline

        with self.say("c5.type.1") as c:
            # "So, back to our question." The hook's picture, as scene 1 left it
            self.play(FadeIn(string), time_span(FadeIn(ghost), 0.3, 1.4),
                      time_span(FadeIn(q, scale=0.6), 0.6, 1.5), run_time=1.5)
            c.wait_until("list of characters")
            self.play(FlashAround(q, color=GOLD, time_width=1.5, buff=0.15), run_time=1.2)

            # "In a few programming languages, it really is." The ghost becomes a real list
            c.wait_until("some")
            self.play(Transform(ghost, lit_ghost), FadeIn(some, shift=0.3 * UP), run_time=1.5)

            # "But not in OCaml." Back to a ghost, crossed out
            c.wait_until("no")
            self.play(Transform(ghost, dim_ghost), Create(cross), FadeTransform(some, not_ocaml),
                      run_time=1.5)

            # "string is a separate type": the question turns into the answer (P23)
            c.wait_until("separate")
            self.play(FadeTransform(q, answer), run_time=1.5)

            # "an abstract idea in its own right": the three boxes become one value
            c.wait_until("abstract")
            self.play(*[Transform(b[0], whole.copy()) for b in boxes],
                      *[b[1].animate.move_to(word[i + 1]) for i, b in enumerate(boxes)],
                      q_left.animate.scale(80 / 110).move_to(word[0]),
                      q_right.animate.scale(80 / 110).move_to(word[4]), run_time=1.5)
            self.remove(boxes[1][0], boxes[2][0])
            c.wait_until("not a chain")
            self.play(FlashAround(VGroup(ghost, cross), color=RED, time_width=1.5), run_time=1.0)

    # type.2: "abc" @ "def" is rejected
    def append_strings(self):
        code = paint_quotes(Code('"abc" @ "def"', size=CODE)).move_to(UP * 0.6)
        at = code.find("@")[0]
        q = T("?", size=80, color=GOLD).next_to(code, RIGHT, buff=0.5)
        err_a, err_b = error_lines("'a list")
        err = VGroup(err_a, err_b).next_to(code, DOWN, buff=0.75)
        caret = underline(code.find('"abc"'), RED)
        box = hl_box(select(err_b, "'a list")[0], err_b, GREEN)
        box_got = hl_box(select(err_a, "string")[0], err_a, GREEN)

        with self.say("c5.type.2") as c:
            # "Try joining two strings with the at sign": the picture makes way
            c.wait_until("append")
            self.sweep_clear(time_span(FadeIn(code, shift=0.3 * DOWN), 0.6, 1.6), run_time=1.6)
            c.wait_until("at sign")
            self.play(FlashAround(at, color=YELLOW, time_width=1.5), at.animate.set_color(YELLOW),
                      run_time=1.0)
            # "the way you'd join two lists" ... will it work? (hold through the pause)
            c.wait_until("the way")
            self.play(FadeIn(q, scale=0.6), run_time=1.0)

            # "OCaml rejects it." The "?" becomes OCaml's answer (P23)
            c.wait_until("reject")
            self.play(FadeTransform(q, err), code.animate.set_color(RED),
                      time_span(Create(caret), 0.6, 1.4), run_time=1.5)

            # "It expected a list, and it got a string." One box, sliding (P8)
            c.wait_until("expected")
            self.play(FadeIn(box), FlashUnder(select(err_b, "'a list")[0], color=GREEN), run_time=0.8)
            c.wait_until("and it got")
            self.play(box.animate.become(box_got), run_time=0.8)
        return VGroup(code, caret, err_a, err_b), box

    # type.3: 'a' is not "a", and comparing them is a type error
    def char_vs_string(self, block1):
        group1, box1 = block1
        UP_BY = 2.25                      # block 1 steps up to the top of the frame
        Y = -0.55                         # block 2's code line
        ch = paint_quotes(Code("'a'", size=CODE)).move_to([-2.3, Y, 0])
        st = paint_quotes(Code('"a"', size=CODE)).move_to([2.3, Y, 0])
        neq = MathTex(r"\neq", font_size=84).move_to([0, Y, 0])
        ch_t = Mono("char", size=36, color=GREEN).next_to(ch, DOWN, buff=0.4)
        st_t = Mono("string", size=36, color=GREEN).next_to(st, DOWN, buff=0.4)
        st_t.align_to(ch_t, UP)

        code = paint_quotes(Code("'a' = \"a\"", size=CODE)).move_to([0, Y, 0])
        q = T("?", size=80, color=GOLD).next_to(code, RIGHT, buff=0.5)
        err_a, err_b = error_lines("char")
        err = VGroup(err_a, err_b).next_to(code, DOWN, buff=0.75)
        caret = underline(code.find('"a"'), RED)
        box = hl_box(select(err_b, "char")[0], err_b, GREEN)
        box_got = hl_box(select(err_a, "string")[0], err_a, GREEN)

        with self.say("c5.type.3") as c:
            # "The same goes for characters." The first rejection steps back (P9)
            self.play(restyle(group1, DIMMED, shift=UP * UP_BY),
                      box1.animate.shift(UP * UP_BY).set_fill(opacity=0.08).set_stroke(opacity=DIMMED),
                      run_time=1.5)

            # "A character is not a string of length one."
            c.wait_until("a character")
            self.play(FadeIn(ch, shift=0.3 * DOWN), FadeIn(ch_t, shift=0.3 * UP), run_time=1.0)
            c.wait_until("string of length")
            self.play(FadeIn(st, shift=0.3 * DOWN), FadeIn(st_t, shift=0.3 * UP),
                      time_span(Write(neq), 0.4, 1.2), run_time=1.2)
            c.wait_until("primitive")
            self.play(FlashUnder(ch_t, color=GREEN, time_width=1.5), run_time=1.2)

            # "ask whether the character A equals the string A": the two slide together
            # into one input, the not-equal becoming the question's equals (P5)
            c.wait_until("ask whether")
            parts = [(ch.text, code.find("'a'")), (st.text, code.find('"a"'))]
            self.play(*[ReplacementTransform(g, t) for src, dst in parts for g, t in zip(src, dst)],
                      ReplacementTransform(neq, code.find("=")[0]),
                      time_span(FadeOut(ch_t), 0, 0.6), time_span(FadeOut(st_t), 0, 0.6), run_time=1.5)
            self.remove(*code.get_family())
            self.add(code)
            c.wait_until("the string a")
            self.play(FadeIn(q, scale=0.6), run_time=1.0)

            # "OCaml won't even run it."
            c.wait_until("error")
            self.play(FadeTransform(q, err), code.animate.set_color(RED),
                      time_span(Create(caret), 0.6, 1.4), run_time=1.5)

            # "A char and a string are different types"
            c.wait_until("a char")
            self.play(FadeIn(box), FlashUnder(select(err_b, "char")[0], color=GREEN), run_time=0.8)
            c.wait_until("string", nth=2)
            self.play(box.animate.become(box_got), run_time=0.8)
            c.wait_until("comparing")
            self.play(FlashAround(code.find("=")[0], color=RED, time_width=1.5), run_time=1.0)
        return VGroup(code, caret, err_a, err_b), box

    # type.4: quote, character, quote, and the comma
    def char_form(self, block1, block2):
        group2, box2 = block2
        UP_BY = 3.3                        # block 2 takes the top
        hero = paint_quotes(Code("'c'", size=HERO)).move_to(DOWN * 0.4)
        lq, cc, rq = hero.text[0], hero.text[1], hero.text[2]
        reply = paint_quotes(Code("- : char = 'c'", size=46)).move_to(DOWN * 2.95)
        reply.find("char").set_color(GREEN)
        r_lit = reply.find("'c'")
        r_c = r_lit[1]

        comma = paint_quotes(Code("','", size=HERO))
        comma.shift(lq.get_center() - comma.text[0].get_center())
        r_comma = paint_quotes(Code("','", size=46))
        r_comma.shift(r_lit[0].get_center() - r_comma.text[0].get_center())

        def side_label(glyph, side):
            """'quote' beside a quote mark, with a short arrow in (side: -1 left, +1 right)."""
            lab = T("quote", size=36, color=QUOTE)
            lab.move_to([glyph.get_x() + side * 2.1, glyph.get_y(), 0])
            arr = Arrow(lab.get_edge_center(-side * RIGHT), glyph.get_edge_center(side * RIGHT),
                        buff=0.18, stroke_width=4, color=QUOTE,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.18)
            return lab, arr

        lq_lab, lq_arr = side_label(lq, -1)
        rq_lab, rq_arr = side_label(rq, 1)
        base = hero.get_bottom()[1]
        c_lab = T("character", size=36, color=GOLD).move_to([0, base - 0.85, 0])
        c_arr = Arrow(c_lab.get_top(), [cc.get_x(), base, 0], buff=0.12, stroke_width=4, color=GOLD,
                      max_tip_length_to_length_ratio=0.35, tip_length=0.18)

        with self.say("c5.type.4") as c:
            # "Every character constant has the same simple form." The first rejection
            # goes; the second takes the top, dimmed; the form arrives in the middle
            g1, b1 = block1
            self.play(LaggedStart(FadeOut(g1), FadeOut(b1), lag_ratio=0.1),
                      restyle(group2, DIMMED, shift=UP * UP_BY),
                      box2.animate.shift(UP * UP_BY).set_fill(opacity=0.08).set_stroke(opacity=DIMMED),
                      time_span(FadeIn(hero, shift=0.3 * DOWN), 0.6, 1.6), run_time=1.6)
            c.wait_until("same simple form")
            lit_ids = {id(g) for g in r_lit}
            reply_rest = [g for g in reply.text if id(g) not in lit_ids]
            self.play(TransformFromCopy(hero.text, r_lit), FadeIn(VGroup(*reply_rest), shift=0.3 * DOWN),
                      run_time=1.2)
            self.remove(*r_lit, *reply_rest)
            self.add(reply)

            # "A single quote, the character itself, and another single quote."
            c.wait_until("a single quote")
            self.play(FadeIn(lq_lab, shift=0.3 * RIGHT), GrowArrow(lq_arr), run_time=0.8)
            c.wait_until("the character itself")
            self.play(FadeIn(c_lab, shift=0.3 * UP), GrowArrow(c_arr), run_time=0.8)
            c.wait_until("another")
            self.play(FadeIn(rq_lab, shift=0.3 * LEFT), GrowArrow(rq_arr), run_time=0.8)

            # "So the comma character is written as a comma": only the middle changes
            c.wait_until("comma character")
            self.play(Transform(cc, comma.text[1]), Transform(r_c, r_comma.text[1]), run_time=1.5)
            c.wait_until("between two")
            self.play(FlashAround(lq, color=QUOTE, time_width=1.5), FlashAround(rq, color=QUOTE, time_width=1.5),
                      run_time=1.0)
