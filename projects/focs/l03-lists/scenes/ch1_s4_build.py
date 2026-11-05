"""Chapter 1, scene 4: every list is nil or cons, and [3; 5; 9] is built from the back.

Clips c1.build.1 – c1.build.5. Everything here is code/expressions; the box-and-pointer
cells belong to the next scene (ch1_s5_cells).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

_TOKEN = re.compile(r"\[\]|::|;;|'[a-z]|[A-Za-z_]+|\d+|\S")


class Expr(VGroup):
    """An OCaml snippet as one `Code` per token, placed exactly where the whole line puts it.

    Tokens can then be moved, copied or revealed one at a time:
    expr[i] is the i-th token, expr.tok("::", nth=1) the second `::`.
    """

    def __init__(self, src, size=48, **kw):
        super().__init__(**kw)
        full = Code(src, size=size)
        self.strs = []
        for m in _TOKEN.finditer(src):
            span = full._span(m.start(), m.end())
            tok = Code(m.group(), size=size)
            for g, ref in zip(tok.text, span):       # keep the colours the line gives it
                g.set_color(ref.get_color())
            tok.move_to(span)
            self.add(tok)
            self.strs.append(m.group())

    def tok(self, s, nth=0):
        return [t for t, x in zip(self.submobjects, self.strs) if x == s][nth]


def under(mob, depth, color=YELLOW, tick=0.12):
    """A thin bracket under `mob` (a grouping mark), `depth` units below its bottom."""
    y = mob.get_bottom()[1] - depth
    x0, x1 = mob.get_left()[0], mob.get_right()[0]
    shape = VMobject(stroke_color=color, stroke_width=4)
    shape.set_points_as_corners([[x0, y + tick, 0], [x0, y, 0], [x1, y, 0], [x1, y + tick, 0]])
    return shape


def read_line(mob, color=DIM, buff=0.16):
    """A plain underline used to follow along as a line is read aloud."""
    y = mob.get_bottom()[1] - buff
    return Line([mob.get_left()[0], y, 0], [mob.get_right()[0], y, 0], color=color, stroke_width=3)


def highlight(mob, color, buff=0.15):
    """3b1b's highlight box (PATTERNS P8): thin stroke, faint fill, drawn behind the text."""
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.08, stroke_width=2)
    return box.set_fill(color, 0.15).set_z_index(-1)


class TwoKindsOfList(NarratedScene):
    def construct(self):
        self.two_pieces()      # c1.build.1
        self.head_and_tail()   # c1.build.2
        self.build_up()        # c1.build.3
        self.grouping()        # c1.build.4
        self.nil_type()        # c1.build.5
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.1)  # end on a truly blank frame (the fade's last frame is ~1/12 opaque at 15 fps)

    # c1.build.1: nil and cons, then what cons does
    def two_pieces(self):
        with self.say("c1.build.1") as c:
            c.wait_until("two")
            title = T("Every list is built from two pieces", size=44).to_edge(UP, buff=0.7)
            self.play(FadeIn(title, shift=DOWN * 0.3), run_time=1.5)

            c.wait_until("nil")
            nil = Code("[]", size=96).move_to(LEFT * 3.2 + UP * 0.1)
            self.play(FadeIn(nil, shift=UP * 0.3), run_time=1.5)
            c.wait_until("pair of empty square brackets")
            self.play(FlashAround(nil, color=TEAL, buff=0.2, time_width=1.5, run_time=1.5))
            c.wait_until("called nil")
            nil_lab = T("nil", size=40, color=TEAL).move_to(LEFT * 3.2 + DOWN * 1.3)
            self.play(FadeIn(nil_lab, shift=UP * 0.3), run_time=1.0)

            c.wait_until("cons")
            cons = Code("::", size=96).move_to(RIGHT * 3.2 + UP * 0.1)
            cons_lab = T("cons", size=40, color=TEAL).move_to(RIGHT * 3.2 + DOWN * 1.3)
            self.play(FadeIn(cons, shift=UP * 0.3),
                      time_span(FadeIn(cons_lab, shift=UP * 0.3), 0.8, 1.6), run_time=1.6)
            c.wait_until("double colon")
            self.play(FlashAround(cons, color=TEAL, buff=0.2, time_width=1.5, run_time=1.5))

            # what cons does: an element and a list go in, a longer list comes out
            c.wait_until("what")
            demo = Expr("1 :: [2; 3]", size=80).move_to(UP * 1.7)
            one, op, lst = demo[0], demo[1], VGroup(*demo[2:])
            el_lab = T("element", size=36, color=DIM).next_to(demo, DOWN, buff=0.4).match_x(one)
            ls_lab = T("list", size=36, color=DIM).next_to(demo, DOWN, buff=0.4).match_x(lst)
            # nil leaves (the example needs its space); :: and its name travel to the centre
            self.play(LaggedStart(FadeOut(title), FadeOut(nil), FadeOut(nil_lab), lag_ratio=0.1),
                      ReplacementTransform(cons, op),
                      cons_lab.animate.next_to(op, UP, buff=0.35), run_time=1.2)
            c.wait_until("one element")
            self.play(LaggedStart(FadeIn(VGroup(one, el_lab), shift=DOWN * 0.3),
                                  FadeIn(VGroup(lst, ls_lab), shift=DOWN * 0.3), lag_ratio=0.5),
                      run_time=1.2)

            # the longer list is born from the element and the list (P5)
            c.wait_until("builds")
            result = Expr("[1; 2; 3]", size=80).move_to(DOWN * 1.6)
            arrow = Arrow(UP * 0.2, DOWN * 0.8, buff=0, color=DIM, stroke_width=4,
                          max_tip_length_to_length_ratio=0.25)
            # [ 1 ; 2 ; 3 ]  <-  1 :: [ 2 ; 3 ]   (the new ';' after the 1 fades in)
            pairs = [(0, 1), (2, 0), (3, 3), (4, 4), (5, 5), (6, 6)]
            self.play(GrowArrow(arrow),
                      AnimationGroup(*[TransformFromCopy(demo[a], result[b]) for a, b in pairs],
                                     FadeIn(result[2])), run_time=1.6)
            # emphasis that stays: flash + recolour the element now at the front (P6)
            c.wait_until("stuck on the front")
            self.play(FlashAround(result[1], color=YELLOW, time_width=1.5),
                      result[1].animate.set_color(YELLOW), run_time=1.0)
        self.demo = (demo, el_lab, ls_lab, cons_lab, arrow, result)

    # c1.build.2: x :: l, head and tail; every list is [] or x :: l
    def head_and_tail(self):
        demo, el_lab, ls_lab, cons_lab, arrow, result = self.demo
        lst = VGroup(*demo[2:])
        example = VGroup(*demo, arrow, result)
        xl = Expr("x :: l", size=80).move_to([2.6, 0.4, 0])
        x, op, l = xl
        lab_y = xl.get_bottom()[1] - 0.6
        head = T("head", size=40, color=YELLOW).move_to([x.get_x(), lab_y, 0])
        tail = T("tail", size=40, color=BLUE).move_to([l.get_x(), lab_y, 0])

        with self.say("c1.build.2") as c:
            # the example shrinks aside (it stays readable) while its labels go to their places...
            self.play(example.animate.scale(0.6).move_to([-3.9, 0.2, 0]),
                      AnimationGroup(el_lab.animate.move_to([x.get_x(), lab_y, 0]),
                                     ls_lab.animate.move_to([l.get_x(), lab_y, 0]),
                                     cons_lab.animate.next_to(op, UP, buff=0.35)), run_time=0.9)
            # ...then the general form is born from it (P5)
            self.play(FadeTransform(demo[0].copy(), x, stretch=False), TransformFromCopy(demo[1], op),
                      FadeTransform(lst.copy(), l, stretch=False), run_time=1.3)

            # each name lands with a flash and a colour that stays (P6/P7)
            c.wait_until("ex is called")
            self.play(FlashAround(x, color=YELLOW, time_width=1.5), x.animate.set_color(YELLOW),
                      FadeTransform(el_lab, head, stretch=False), run_time=1.5)
            c.wait_until("ell is called")
            self.play(FlashAround(l, color=BLUE, time_width=1.5), l.animate.set_color(BLUE),
                      FadeTransform(ls_lab, tail, stretch=False), run_time=1.5)

            # every list: either the empty list, or a head stuck onto a tail
            # (the example gives up its space only now, when nil needs it)
            c.wait_until("every")
            nil = Code("[]", size=80).move_to([-3.4, op.get_y(), 0])
            nil_lab = T("nil", size=40, color=TEAL).move_to([-3.4, lab_y, 0])
            or_ = T("or", size=40, color=DIM).move_to(
                [(nil.get_right()[0] + xl.get_left()[0]) / 2, op.get_y(), 0])
            self.play(LaggedStart(FadeOut(example, shift=LEFT * 0.3),
                                  FadeIn(VGroup(nil, nil_lab, or_), shift=RIGHT * 0.3), lag_ratio=0.5),
                      run_time=1.6)

            # one highlight box slides from the head to the tail (P8)
            c.wait_until("a head")
            box = highlight(VGroup(x, head), YELLOW)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("a tail")
            self.play(box.animate.become(highlight(VGroup(l, tail), BLUE)), run_time=0.7)
        self.summary = (nil, VGroup(nil_lab, or_, xl, head, tail, box, cons_lab))

    # c1.build.3: [] -> 9 :: [] -> 5 :: 9 :: [] -> 3 :: 5 :: 9 :: [], with bracket values
    def build_up(self):
        nil, rest = self.summary
        srcs = ["[]  =  []", "9 :: []  =  [9]", "5 :: 9 :: []  =  [5; 9]",
                "3 :: 5 :: 9 :: []  =  [3; 5; 9]"]
        rows = [Expr(s, size=48) for s in srcs]
        # the finished table is centred in the frame; every row shares one monospace
        # grid, aligned on its '=', so the conses line up on the right (P4)
        rows[3].move_to(ORIGIN)
        eq_x = rows[3].tok("=").get_x()
        for row, y in zip(rows, (2.1, 0.7, -0.7, -2.1)):
            row.shift([eq_x, y, 0] - row.tok("=").get_center())

        with self.say("c1.build.3") as c:
            # the summary stays up until the table needs the space; the [] the build
            # starts from is carried into it (P18)
            c.wait_until("start")
            self.play(FadeOut(rest), ReplacementTransform(nil, rows[0][0]),
                      time_span(FadeIn(VGroup(*rows[0][1:]), shift=LEFT * 0.2), 1.0, 1.8),
                      run_time=1.8)

            for k, cue in enumerate(("nine", "five", "three"), start=1):
                prev, cur = rows[k - 1], rows[k]
                # each row is born from a copy of the row above (P5/P11); the row above dims (P9)
                c.wait_until(cue)
                self.play(FadeIn(VGroup(cur[0], cur[1]), shift=RIGHT * 0.3),
                          AnimationGroup(*[TransformFromCopy(prev[i], cur[i + 2])
                                           for i in range(2 * k - 1)]),
                          prev.animate.set_opacity(0.4), run_time=1.6)

                # its value: the new head flies into the brackets, the old value copies down
                c.wait_until("you get", nth=k - 1)
                pv, nv = prev[2 * k:], cur[2 * k + 2:]
                if k == 1:
                    old = [TransformFromCopy(pv[0], VGroup(nv[0], nv[2]))]
                else:
                    old = [TransformFromCopy(pv[0], nv[0]), FadeIn(nv[2])]
                    old += [TransformFromCopy(pv[j], nv[j + 2]) for j in range(1, len(pv))]
                self.play(FadeIn(cur[2 * k + 1]),
                          TransformFromCopy(cur[0], nv[1], path_arc=-1.2),  # dips below the row
                          AnimationGroup(*old), run_time=1.5)
        self.rows = rows

    # c1.build.4: [3; 5; 9] = 3 :: 5 :: 9 :: [] = 3 :: (5 :: (9 :: [])), grouped from the right
    def grouping(self):
        rows = self.rows
        last = rows[3]
        size = 52
        A = Expr("[3; 5; 9]", size=size)
        B = Expr("= 3 :: 5 :: 9 :: []", size=size)
        C = Expr("= 3 :: (5 :: (9 :: []))", size=size)
        C.move_to(UP * 0.1)
        C.set_x(0)
        B.shift([C[0].get_x(), 1.3, 0] - B[0].get_center())
        A.move_to([0, 2.5, 0]).align_to(B[1], LEFT)

        with self.say("c1.build.4") as c:
            # lagged sweep clears the first rows; the last row is carried into the new layout
            self.play(LaggedStart(*[FadeOut(r) for r in rows[:3]], lag_ratio=0.15), run_time=1.0)
            # the bracket form (and the '=') move up first, then the cons form follows
            self.play(LaggedStart(
                AnimationGroup(*[ReplacementTransform(last[8 + i], A[i]) for i in range(7)],
                               ReplacementTransform(last[7], B[0])),
                AnimationGroup(*[ReplacementTransform(last[i], B[i + 1]) for i in range(7)]),
                lag_ratio=0.5), run_time=2.2)

            # follow along as each form is read aloud
            c.wait_until("three five nine in")
            ua = read_line(A)
            self.play(Create(ua), run_time=c.until("means", floor=0.8), rate_func=linear)
            c.wait_until("three cons")
            ub = read_line(VGroup(*B[1:]))
            self.play(Create(ub), run_time=c.until("nil", floor=1.0), rate_func=linear)

            # the conses group from the right: a spaced-out copy, the rest dimmed (P9, P13)
            c.wait_until("right")
            b_to_c = [(0, 0), (1, 1), (2, 2), (3, 4), (4, 5), (5, 7), (6, 8), (7, 9)]
            self.play(FadeOut(VGroup(ua, ub)),
                      AnimationGroup(*[TransformFromCopy(B[a], C[b]) for a, b in b_to_c]),
                      VGroup(A, B).animate.set_opacity(0.35), run_time=1.8)

            g1 = VGroup(*C[7:10])          # 9 :: []
            g2 = VGroup(*C[4:11])          # 5 :: (9 :: [])
            g3 = VGroup(*C[1:12])          # 3 :: (5 :: (9 :: []))
            u1, u2, u3 = (under(g, d) for g, d in ((g1, 0.18), (g2, 0.38), (g3, 0.58)))
            c.wait_until("the nine")
            self.play(FadeIn(C[6], scale=1.4), FadeIn(C[10], scale=1.4), Create(u1), run_time=1.2)
            c.wait_until("then the five")
            self.play(AnimationGroup(FadeIn(C[3], scale=1.4), FadeIn(C[11], scale=1.4)),
                      Create(u2), u1.animate.set_stroke(TEAL), run_time=c.until("then the three",
                                                                                 floor=0.8))
            c.wait_until("then the three")
            self.play(Create(u3), u2.animate.set_stroke(TEAL), run_time=1.2)

            # built from the back, read from the front
            x0, x1 = g3.get_left()[0], g3.get_right()[0]
            yb = u3.get_bottom()[1] - 0.6
            built = Arrow([x1, yb, 0], [x0, yb, 0], buff=0, color=TEAL, stroke_width=4,
                          max_tip_length_to_length_ratio=0.05)
            built_lab = T("built", size=36, color=TEAL).next_to(built, LEFT, buff=0.35)
            read = Arrow([x0, yb - 0.8, 0], [x1, yb - 0.8, 0], buff=0, color=YELLOW,
                         stroke_width=4, max_tip_length_to_length_ratio=0.05)
            read_lab = T("read", size=36, color=YELLOW).next_to(read, LEFT, buff=0.35)
            read_lab.align_to(built_lab, RIGHT)
            # one beat for the whole sentence: "built" first, "read" lands on its word
            c.wait_until("built")
            self.play(time_span(AnimationGroup(GrowArrow(built), FadeIn(built_lab, shift=LEFT * 0.3),
                                               u3.animate.set_stroke(TEAL)), 0, 0.9),
                      time_span(AnimationGroup(GrowArrow(read), FadeIn(read_lab, shift=RIGHT * 0.3),
                                               VGroup(A, B).animate.set_opacity(1)), 0.6, 1.5),
                      run_time=1.5)

    # c1.build.5: ask, hold, then the ? becomes 'a list (P23)
    def nil_type(self):
        size = 64
        ans = Expr("- : 'a list = []", size=size).move_to(UP * 0.6)
        q = Expr("- : ? = []", size=size)
        q.shift(ans[0].get_center() - q[0].get_center())
        q[2].set_color(GOLD)
        inp = Expr("# [];;", size=size)
        inp.shift(np.array([ans.get_left()[0] - inp.get_left()[0], 1.9 - inp[1].get_y(), 0]))
        inp[0].set_color(DIM)

        int_l = Expr("int list", size=52).move_to([-2.8, -1.3, 0])
        str_l = Expr("string list", size=52).move_to([2.8, -1.3, 0])
        too = T("too specific", size=40, color=RED).move_to(DOWN * 2.35)

        with self.say("c1.build.5") as c:
            # the last picture stays while the puzzle is posed; it clears only when the
            # question needs the space, which then sits on screen, boxed, through the {pause}
            c.wait_until("own")
            qbox = highlight(q[2], GOLD, buff=0.12)
            self.play(time_span(FadeOut(*self.mobjects), 0, 0.7),
                      time_span(LaggedStart(FadeIn(inp, shift=DOWN * 0.3), FadeIn(q, shift=DOWN * 0.3),
                                            FadeIn(qbox), lag_ratio=0.35), 0.4, 1.6), run_time=1.6)

            c.wait_until("int list")
            self.play(FadeIn(int_l, shift=UP * 0.3), run_time=1.0)
            c.wait_until("just as well")
            self.play(FadeIn(str_l, shift=UP * 0.3), run_time=1.0)
            c.wait_until("strings")
            self.play(FadeIn(too, shift=UP * 0.3), VGroup(int_l, str_l).animate.set_opacity(0.5),
                      run_time=1.0)

            # the answer: the ? itself turns into 'a list, and its box rides along (P12, P23)
            # the rejected guesses stay, shrunk to the bottom, to make room for alpha
            c.wait_until("alpha")
            self.play(VGroup(int_l, str_l, too).animate.scale(0.8).move_to(DOWN * 2.75),
                      AnimationGroup(ReplacementTransform(q[0], ans[0]),
                                     ReplacementTransform(q[1], ans[1]),
                                     FadeTransform(q[2], VGroup(ans[2], ans[3]), stretch=False),
                                     ReplacementTransform(q[3], ans[4]),
                                     ReplacementTransform(q[4], ans[5])),
                      qbox.animate.become(highlight(VGroup(ans[2], ans[3]), PINK, buff=0.12)),
                      run_time=1.6)

            c.wait_until("list which")
            a_tok = ans.tok("'a")
            alpha = MathTex(r"\alpha", font_size=96, color=PINK).move_to([a_tok.get_x(), -1.15, 0])
            pointer = Arrow(a_tok.get_bottom() + DOWN * 0.15, alpha.get_top() + UP * 0.12, buff=0,
                            color=PINK, stroke_width=3, max_tip_length_to_length_ratio=0.2)
            means = T("= any type", size=48).next_to(alpha, RIGHT, buff=0.4)
            self.play(FadeOut(qbox), AnimationGroup(GrowArrow(pointer), FadeIn(alpha, shift=DOWN * 0.3)),
                      time_span(FadeIn(means, shift=LEFT * 0.3), 0.7, 1.4), run_time=1.4)

            c.wait_until("little alpha")
            self.play(FlashAround(a_tok, color=PINK, time_width=1.5),
                      FlashAround(alpha, color=PINK, time_width=1.5), run_time=1.5)
