"""Chapter 2, scene 2: inserting one item, `ins`. Clips c2.ins.1 – c2.ins.5.

Plan: a sorted list takes a 4 into its slot (the job) → the `ins` code, hero, centred (Code 36,
both `ins` YELLOW) → one BLUE box walks the clauses (YELLOW on the test `x <= y`), a YELLOW box +
label on `ins x ys` → the type reply below, a box walking its 'a / 'a list → `<=` flashes, DIM tag
→ code shrinks to the top (scale 0.78, centre (0, 2.65)), trace below with GOLD questions, reply,
comparison counter → the unsorted input `ins 4 [9; 3]` gives a RED reply with a cross.
Shared look (s4, s7): `ins_code()` = Code(INS_SRC, 36) with every `ins` recoloured YELLOW.
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

INS_SRC = """let rec ins x = function
  | [] -> [x]
  | y::ys -> if x <= y then x :: y :: ys
             else y :: ins x ys"""

SIZE = 36            # hero code
H = 0.6              # clause-box height at SIZE
SMALL = 0.78         # code scale once the trace starts
HS = H * SMALL
TSIZE = 40           # trace rows
RSIZE = 34           # toplevel replies under the trace
L = -4.0             # left edge of the trace code column
ROW_Y = [0.95, 0.15, -0.65, -1.45]
REPLY_Y = -2.45


def ocode(src, size=SIZE):
    """Code with every `ins` YELLOW (the definition is YELLOW already; calls too)."""
    c = Code(src, size=size)
    k = 0
    while True:
        try:
            g = c.find("ins", nth=k)
        except ValueError:
            break
        g.set_color(YELLOW)
        k += 1
    return c


def row(src, y, arrow=True):
    """A trace row: DIM ⇒ then the code, code left edge at x=L, centred on y."""
    code = ocode(src, TSIZE)
    code.move_to([0, y, 0]).shift(RIGHT * (L - code.get_left()[0]))
    if not arrow:
        return code
    a = MathTex(r"\Rightarrow", font_size=64, color=DIM)
    a.next_to(code, LEFT, buff=0.25).set_y(y)
    return VGroup(a, code)


def question(tex, y, x_left):
    q = MathTex(tex, font_size=48, color=GOLD)
    q.move_to([0, y, 0]).shift(RIGHT * (x_left - q.get_left()[0]))
    return q


def answer(word, q):
    a = T(word, size=36, color=GOLD).next_to(q, RIGHT, buff=0.25)
    a.shift(UP * (q.get_bottom()[1] - a[-1].get_bottom()[1]))     # sit on q's baseline
    return a


class InsertOne(NarratedScene):
    def construct(self):
        self.job()
        self.clauses()
        self.reply()
        self.trace()
        self.warning()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # helpers ---------------------------------------------------------------
    def tb(self, sub, line, color=BLUE, code=None, height=None, nth=0):
        code = code or self.code
        return token_box(code.find(sub, line=line, nth=nth), code.line(line), color=color,
                         height=height or H)

    # c2.ins.1 ----------------------------------------------------------------
    def job(self):
        with self.say("c2.ins.1") as c:
            lst = Code("[3; 5; 9]", size=64).move_to(0.5 * DOWN)
            self.play(FadeIn(lst, shift=0.2 * UP), run_time=1.0)
            c.wait_until("one small job")
            item = Mono("4", size=64, color=YELLOW).move_to(lst.get_center() + 1.7 * UP)
            self.play(FadeIn(item, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("Put one item")
            tgt = Code("[3; 4; 5; 9]", size=64).move_to(lst)
            tgt.text[3].set_color(YELLOW)
            moves = [Transform(lst.text[i], tgt.text[i]) for i in range(3)]
            moves += [Transform(lst.text[i], tgt.text[i + 2]) for i in range(3, 7)]
            self.play(*moves, Transform(item, tgt.text[3]), FadeIn(tgt.text[4]),
                      run_time=min(2.0, 0.6 * c.until("in its right place")))
            self.remove(*lst.get_family(), item, tgt.text[4])
            self.add(tgt)
            c.wait_until("in its right place")
            self.play(FlashAround(tgt.text[3], run_time=1.5, time_width=1.5))

            c.wait_until("code")
            code = self.code = ocode(INS_SRC).move_to(0.15 * UP)
            sweep_clear(self, time_span(FadeIn(code), 0.4, 1.5), run_time=1.5)

            c.wait_until("It's called ins")
            self.box = self.tb("ins", 0)
            self.play(FadeIn(self.box), run_time=0.8)

            c.wait_until("args")
            lab_x = label_pointer("item", code.find("x", line=0), color=BLUE)
            self.play(Transform(self.box, self.tb("x", 0)), FadeIn(lab_x, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("the sorted list")
            lab_l = label_pointer("sorted list", code.find("function", line=0), color=BLUE)
            self.play(Transform(self.box, self.tb("function", 0)), FadeIn(lab_l, shift=0.3 * DOWN),
                      run_time=1.0)

            self.labels = (lab_x, lab_l)

            c.wait_until("nil")
            self.play(Transform(self.box, self.tb("[] -> [x]", 1)), run_time=1.2)

    # c2.ins.2 ----------------------------------------------------------------
    def clauses(self):
        code = self.code
        with self.say("c2.ins.2") as c:
            self.play(Transform(self.box, self.tb("y::ys", 2)), run_time=1.0)
            c.wait_until("test")
            self.play(Transform(self.box, self.tb("x <= y", 2, YELLOW)), FadeOut(*self.labels), run_time=1.0)
            c.wait_until("stop")
            self.play(Transform(self.box, self.tb("x :: y :: ys", 2)), run_time=1.0)
            c.wait_until("The answer is")
            self.play(FlashUnder(code.find("x :: y :: ys", line=2), color=BLUE, run_time=2, time_width=1.5))
            c.wait_until("else")
            self.play(Transform(self.box, self.tb("y :: ins x ys", 3)), run_time=1.0)
            c.wait_until("carry")
            self.cbox = self.tb("ins x ys", 3, YELLOW, height=H - 0.1)
            self.clab = T("the smaller problem", size=30, color=YELLOW).next_to(self.cbox, DOWN, buff=0.3)
            self.play(FadeIn(self.cbox), FadeIn(self.clab, shift=0.3 * DOWN), run_time=1.0)

    # c2.ins.3 ----------------------------------------------------------------
    def reply(self):
        code = self.code
        with self.say("c2.ins.3") as c:
            rep = self.rep = ocode("val ins : 'a -> 'a list -> 'a list = <fun>", 32)
            rep.move_to(2.5 * DOWN).align_to(code, LEFT)
            self.play(FadeOut(self.box), FadeIn(rep, shift=0.2 * UP), run_time=1.2)
            c.wait_until("takes an alpha")
            rbox = token_box(rep.find("'a"), rep)
            self.play(FadeIn(rbox), run_time=0.6)
            c.wait_until("and an alpha list")
            self.play(Transform(rbox, token_box(rep.find("'a list"), rep)), run_time=0.8)
            c.wait_until("returns an alpha list")
            self.play(Transform(rbox, token_box(rep.find("'a list", nth=1), rep)), run_time=0.8)

            c.wait_until("poly")
            le = code.find("<=", line=2)
            tag = self.tag = T("polymorphic (Lecture 4)", size=30, color=DIM)
            tag.move_to([0, code.line(1).get_y(), 0]).shift(RIGHT * (le.get_left()[0] - 0.3 - tag.get_left()[0]))
            self.play(FadeOut(rbox, self.cbox, self.clab, run_time=1.0),
                      FlashAround(le, run_time=2, time_width=1.5),
                      FadeIn(tag, shift=0.3 * DOWN, run_time=1.2))

    # c2.ins.4 ----------------------------------------------------------------
    def trace(self):
        code = self.code
        with self.say("c2.ins.4") as c:
            code.generate_target()
            code.target.scale(SMALL).move_to(2.65 * UP)
            self.play(FadeOut(self.rep, self.tag), MoveToTarget(code), run_time=1.5)
            r1 = row("ins 4 [3; 5; 9]", ROW_Y[0], arrow=False)
            r2 = row("3 :: ins 4 [5; 9]", ROW_Y[1])
            r3 = row("3 :: 4 :: 5 :: [9]", ROW_Y[2])
            r4 = row("[3; 4; 5; 9]", ROW_Y[3])
            qx = r3.get_right()[0] + 0.6
            self.play(FadeIn(r1, shift=0.2 * UP), run_time=1.0)

            c.wait_until("t1")
            q1 = question(r"4 \le 3\,?", ROW_Y[1], qx)
            sb = self.tb("x <= y", 2, YELLOW, height=HS)
            self.play(FadeIn(q1, shift=0.3 * DOWN), FadeIn(sb), run_time=1.0)
            c.wait_until("No")
            a1 = answer("no", q1)
            self.play(FadeIn(a1, shift=0.2 * LEFT), run_time=0.6)
            c.wait_until("So the three stays")
            self.play(TransformFromCopy(r1, r2), Transform(sb, self.tb("y :: ins x ys", 3, height=HS)),
                      run_time=1.6)

            c.wait_until("t2")
            q2 = question(r"4 \le 5\,?", ROW_Y[2], qx)
            self.play(FadeIn(q2, shift=0.3 * DOWN), Transform(sb, self.tb("x <= y", 2, YELLOW, height=HS)),
                      run_time=1.0)
            c.wait_until("Yes")
            a2 = answer("yes", q2)
            self.play(FadeIn(a2, shift=0.2 * LEFT), run_time=0.6)
            c.wait_until("So the four goes")
            self.play(TransformFromCopy(r2, r3), Transform(sb, self.tb("x :: y :: ys", 2, height=HS)),
                      run_time=1.6)

            c.wait_until("done")
            rep = ocode("- : int list = [3; 4; 5; 9]", RSIZE)
            rep.move_to([0, REPLY_Y, 0]).shift(RIGHT * (L - rep.get_left()[0]))
            self.play(TransformFromCopy(r3, r4), FadeOut(sb), run_time=min(1.4, 0.55 * c.until("two")))
            self.play(FadeIn(rep, shift=0.2 * UP), run_time=min(1.0, 0.8 * c.until("two")))

            c.wait_until("two")
            counter = T("comparisons: 2", size=34, color=GOLD)
            counter.move_to([0, ROW_Y[3], 0]).shift(RIGHT * (qx - counter.get_left()[0]))
            self.play(TransformFromCopy(VGroup(q1, q2), counter), run_time=1.5)

    # c2.ins.5 ----------------------------------------------------------------
    def warning(self):
        code = self.code
        with self.say("c2.ins.5", gap=2.8) as c:
            c.wait_until("bad")
            b1 = row("ins 4 [9; 3]", ROW_Y[0], arrow=False)
            b2 = row("4 :: 9 :: [3]", ROW_Y[1])
            sweep_clear(self, time_span(FadeIn(b1, shift=0.2 * UP), 0.7, 1.6), keep=[code], run_time=1.6)

            c.wait_until("first")
            qx = b2.get_right()[0] + 0.7
            q3 = question(r"4 \le 9\,?", ROW_Y[1], qx)
            a3 = answer("yes", q3)
            sb = self.tb("x <= y", 2, YELLOW, height=HS)
            self.play(FadeIn(q3, shift=0.3 * DOWN), FadeIn(a3, shift=0.3 * DOWN), FadeIn(sb), run_time=1.0)
            c.wait_until("so it goes in front")
            self.play(TransformFromCopy(b1, b2), Transform(sb, self.tb("x :: y :: ys", 2, height=HS)),
                      run_time=1.6)

            c.wait_until("wrong")
            rep = ocode("- : int list = [4; 9; 3]", RSIZE).set_color(RED)
            rep.move_to([0, -1.0, 0]).shift(RIGHT * (L - rep.get_left()[0]))
            cross = cross_mark().next_to(rep, RIGHT, buff=0.45)
            bad_list = b1.find("[9; 3]")
            ul = underline(bad_list, RED)
            tag = T("assumes the list is sorted", size=30, color=DIM)
            tag.next_to(b1, RIGHT, buff=0.7).set_y(b1.get_y())
            self.play(FadeIn(rep, shift=0.2 * UP), time_span(Create(cross), 0.5, 1.2), run_time=1.2)
            self.play(Create(ul), FadeIn(tag, shift=0.3 * DOWN), run_time=0.9)
