"""Chapter 3, scene 4: the quicksort code, In [80]. Clips c3.code.1 – c3.code.5.

Plan: In [80] hero (Code 28, left edge x=-6.3, centred on y=0) → one YELLOW box walks the
clauses ([] / [x] / a::bs / a / the local `part` block, braced "local helper" / `part [] [] bs`),
DIM notes beside the [x] clause → the pivot `a` and its two uses glow YELLOW, allc inset top
right → accumulators l, r tagged, the test and both branches (x::l, x::r TEAL) → the [] clause,
box walking (quick l), a ::, quick r → code shrinks to the top-left (scale CODE_S, top-left at
CODE_TL), replies in a band below, the ticked chain to the right → replies cleared.
Shared look (s5, s7, ch4): `quick_code()` = ocode(QUICK_SRC, 28) with every `quick` and `part`
YELLOW and `@` GOLD.
HANDOVER: ends on handover_shot() = quick_code() scaled CODE_S, top-left corner at CODE_TL.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

QUICK_SRC = """let rec quick = function
  | [] -> []
  | [x] -> [x]
  | a::bs ->
      let rec part l r = function
        | [] -> (quick l) @ (a :: quick r)
        | x::xs ->
            if (x <= a) then
              part (x::l) r xs
            else
              part l (x::r) xs
      in
      part [] [] bs"""

SIZE = 28
LEFT_X = -6.3                  # hero code's left edge
CODE_S = 0.55                  # code scale once the replies come
CODE_TL = (-6.4, 3.45)         # its top-left corner then (and in the handover shot)
BOX_H = 0.46
RSIZE = 28                     # toplevel lines
ROWS = [-0.9, -1.85, -2.55]    # the band under the small code
CHECK_X = -1.7                 # left edge of the check exchange, right of the small code


def _all(c, sub):
    out, k = [], 0
    while True:
        try:
            out.append(c.find(sub, nth=k))
        except ValueError:
            return out
        k += 1


def quick_code(size=SIZE):
    """In [80] in the studio's code style: `quick`, `part` YELLOW, `@` GOLD."""
    from lib.paths import load_scene
    c = load_scene("ch2_s2_ins").ocode(QUICK_SRC, size)
    for name in ("quick", "part"):
        for g in _all(c, name):
            g.set_color(YELLOW)
    for g in _all(c, "@"):
        g.set_color(GOLD)
    return c


def place_small(c):
    c.scale(CODE_S)
    c.shift(np.array([CODE_TL[0], CODE_TL[1], 0]) - c.get_corner(UL))
    return c


def handover_shot():
    return VGroup(place_small(quick_code()))


def left_at(m, x, y):
    m.move_to([0, y, 0]).shift(RIGHT * (x - m.get_left()[0]))
    return m


class QuickCode(NarratedScene):
    def construct(self):
        c = self.code = quick_code()
        c.move_to(ORIGIN).shift(RIGHT * (LEFT_X - c.get_left()[0]))
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        olds = [m for m in self.mobjects if m is not self.code]
        self.play(*disappear(*olds), run_time=1.0)
        self.wait(1.0)

    # helpers -------------------------------------------------------------
    def box_to(self, glyphs, line, h=BOX_H):
        return token_box(glyphs, self.code.line(line), height=h)

    def row_y(self, i):
        return self.code.line(i).get_center()[1]

    def line_end(self, i):
        return self.code.line(i).get_right()[0]

    # clips -----------------------------------------------------------------
    def clip1(self):
        code = self.code
        with self.say("c3.code.1") as c:
            self.play(*appear(code, shift=None), run_time=min(1.5, 0.6 * c.until("nil")))  # early: code shown whole, then walked
            c.wait_until("nil")
            self.box = self.box_to(code.find("[] -> []", line=1), 1)
            self.play(FadeIn(self.box), run_time=1.0)
            c.wait_until("one")
            self.play(Transform(self.box, self.box_to(code.find("[x] -> [x]", line=2), 2)),
                      run_time=1.2)
            self.tag1 = T("exactly one element", size=30, color=DIM)
            left_at(self.tag1, self.line_end(2) + 0.5, self.row_y(2))
            c.wait_until(own_word=self.tag1)
            self.play(*appear(self.tag1), run_time=1.0)

    def clip2(self):
        code = self.code
        with self.say("c3.code.2") as c:
            self.play(*set_alpha(list(code.line(2)), 0.4), run_time=1.0)
            self.note1 = T("without it: same answers, same comparisons", size=30, color=DIM)
            left_at(self.note1, self.line_end(2) + 0.5, self.row_y(2))
            c.wait_until(own_word=self.note1)
            self.play(*swap(self.tag1, self.note1), run_time=1.2)
            c.wait_until("special")
            self.note2 = T("lists up to five or so: often special-cased for speed", size=28, color=DIM)
            left_at(self.note2, self.line_end(3) + 0.4, self.row_y(3))
            self.play(*set_alpha(list(code.line(2)), 1), *appear(self.note2), run_time=1.2)  # early: the note sums up the sentence

    def clip3(self):
        code = self.code
        with self.say("c3.code.3") as c:
            self.play(Transform(self.box, self.box_to(code.find("a::bs", line=3), 3)), run_time=1.2)
            c.wait_until("pivot")
            a3 = code.find("a", line=3)
            self.play(*during(disappear(self.note1, self.note2), 0, 0.45),
                      *during([Transform(self.box, self.box_to(a3, 3))], 0.2, 1),
                      *during(recolor(a3, YELLOW), 0.2, 1), run_time=1.4)
            self.pivot = T("pivot", size=30, color=YELLOW)
            left_at(self.pivot, self.line_end(3) + 0.5, self.row_y(3))
            c.wait_until(own_word=self.pivot)
            self.play(*appear(self.pivot), run_time=1.0)

            c.wait_until("local")
            block = VGroup(*[code.line(i) for i in range(4, 12)])
            blk_box = token_box(block, block, height=block.height + 0.2)
            self.brace = Brace(block, RIGHT, buff=0.2, color=DIM)
            self.play(Transform(self.box, blk_box), GrowFromCenter(self.brace), run_time=1.5)
            self.local = T("local helper", size=30, color=FG).next_to(self.brace, RIGHT, buff=0.2)
            c.wait_until("helper")
            self.play(*appear(self.local), run_time=1.0)  # early: names the helper on "helper"

            c.wait_until("why")
            a5, a7 = code.find("a", line=5), code.find("a", line=7)
            self.play(*recolor(a5, YELLOW), *recolor(a7, YELLOW),
                      FlashAround(a5, run_time=1.5, time_width=1.5),
                      FlashAround(a7, run_time=1.5, time_width=1.5),
                      FlashAround(a3, run_time=1.5, time_width=1.5), run_time=1.5)
            inset = self.inset = Code("| cs :: css -> (c::cs) :: allc css", size=28)
            inset.move_to([0, (self.row_y(1) + self.row_y(2)) / 2, 0])
            inset.shift(RIGHT * (6.5 - inset.get_right()[0]))
            self.inset_lab = T("local, like allc (Lecture 4)", size=28, color=DIM)
            self.inset_lab.move_to([0, self.row_y(0), 0])
            self.inset_lab.shift(RIGHT * (inset.get_right()[0] - self.inset_lab.get_right()[0]))
            c.wait_until("like all-see")
            self.play(*appear(self.inset_lab, inset, lag=0.3), run_time=1.2)
            cc = inset.find("c::cs")[0]
            self.play(*recolor([cc], YELLOW), FlashAround(cc, run_time=1.5, time_width=1.5),
                      run_time=1.5)

            c.wait_until("calls")
            ql, qr = code.find("quick l", line=5), code.find("quick r", line=5)
            self.calls = T("recursive calls", size=30, color=YELLOW)
            self.calls.move_to([(ql.get_center()[0] + qr.get_center()[0]) / 2, self.row_y(6), 0])
            self.play(FlashAround(ql, run_time=1.5, time_width=1.5),
                      FlashAround(qr, run_time=1.5, time_width=1.5),
                      *appear(self.calls), run_time=1.5)  # early: the voice says "calls quick"

            c.wait_until("start")
            self.play(*during(disappear(self.inset_lab, self.inset, self.local, self.brace), 0, 0.45),
                      *during([Transform(self.box, self.box_to(code.find("part [] [] bs", line=12), 12))],
                              0.2, 1), run_time=1.5)

    def clip4(self):
        code = self.code
        with self.say("c3.code.4") as c:
            lr = code.find("l r =", line=4)
            l4, r4 = lr[0], lr[1]
            self.play(*during(disappear(self.pivot, self.calls), 0, 0.45),
                      *during([Transform(self.box, self.box_to(VGroup(l4, r4), 4))], 0.2, 1),
                      *during(recolor([l4, r4], YELLOW), 0.2, 1), run_time=1.5)
            y3 = self.row_y(3)
            self.tl = T("left: ≤ a", size=28, color=YELLOW)
            self.tl.move_to([0, y3, 0]).shift(RIGHT * (l4.get_right()[0] + 0.05 - self.tl.get_right()[0]))
            self.tr = T("right: > a", size=28, color=YELLOW)
            self.tr.move_to([0, y3, 0]).shift(RIGHT * (r4.get_left()[0] + 0.05 - self.tr.get_left()[0]))
            c.wait_until(own_word=self.tl)
            self.play(*appear(self.tl), run_time=1.0)
            c.wait_until(own_word=self.tr)
            self.play(*appear(self.tr), run_time=1.0)

            c.wait_until("test")
            self.play(Transform(self.box, self.box_to(code.find("if (x <= a) then", line=7), 7)),
                      run_time=1.2)
            c.wait_until("left")
            self.play(Transform(self.box, self.box_to(code.find("part (x::l) r xs", line=8), 8)),
                      *recolor(code.find("x::l", line=8), TEAL), run_time=1.2)
            c.wait_until("right")
            self.play(Transform(self.box, self.box_to(code.find("part l (x::r) xs", line=10), 10)),
                      *recolor(code.find("x::r", line=10), TEAL), run_time=1.2)

            c.wait_until("end")
            self.play(*during(disappear(self.tl, self.tr), 0, 0.45),
                      *during([Transform(self.box, self.box_to(
                          code.find("| [] -> (quick l) @ (a :: quick r)", line=5), 5))], 0.2, 1),
                      run_time=1.5)
            self.comb = T("combine", size=30, color=YELLOW)
            ql, qr = code.find("(quick l)", line=5), code.find("quick r", line=5)
            self.comb.move_to([(ql.get_center()[0] + qr.get_center()[0]) / 2, self.row_y(6), 0])
            c.wait_until("combine")
            self.play(*appear(self.comb), run_time=1.0)
            c.wait_until("First the sorted left part")
            self.play(Transform(self.box, self.box_to(ql, 5)), run_time=1.0)
            c.wait_until("then ay")
            self.play(Transform(self.box, self.box_to(code.find("a ::", line=5), 5)), run_time=1.0)
            c.wait_until("then the sorted right part")
            self.play(Transform(self.box, self.box_to(qr, 5)), run_time=1.0)
            c.wait_until("with a cons")
            self.play(Transform(self.box, self.box_to(code.find("::", line=5), 5)), run_time=0.9)
            c.wait_until("append")
            self.play(Transform(self.box, self.box_to(code.find("@", line=5), 5)),
                      run_time=min(0.9, c.until()))

    def clip5(self):
        code = self.code
        with self.say("c3.code.5", gap=2.5) as c:
            small = place_small(quick_code())
            self.play(*during(disappear(self.comb, self.box), 0, 0.4),
                      *during([Transform(code, small)], 0.15, 1), run_time=1.6)
            x0 = CODE_TL[0]
            rep0 = left_at(Code("val quick : 'a list -> 'a list = <fun>", size=RSIZE), x0, ROWS[0])
            self.play(*appear(rep0), run_time=1.0)
            c.wait_until("poly")
            in1 = left_at(Code('quick ["dog"; "cat"; "emu"]', size=RSIZE), x0, ROWS[1])
            self.play(*appear(in1), run_time=1.0)
            c.wait_until("Dog, cat, emu")
            rep1 = left_at(Code('- : string list = ["cat"; "dog"; "emu"]', size=RSIZE), x0, ROWS[2])
            self.play(*appear(rep1), run_time=1.0)
            c.wait_until("check")
            in2 = left_at(Code("quick [3; 5; 9; 4; 7]", size=RSIZE), CHECK_X, 3.0)
            rep2 = left_at(Code("- : int list = [3; 4; 5; 7; 9]", size=RSIZE), CHECK_X, 2.35)
            self.play(*appear(in2, rep2, lag=0.5), run_time=1.4)
            chain = ConsChain([3, 4, 5, 7, 9]).scale(0.62)
            left_at(chain, CHECK_X, 1.2)
            tick = check_mark(GREEN).next_to(chain, RIGHT, buff=0.2)
            self.play(*appear(chain, shift=0.15 * DOWN), run_time=1.2)
            self.play(GrowFromCenter(tick), run_time=0.8)
