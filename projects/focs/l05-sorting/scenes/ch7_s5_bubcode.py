"""Chapter 7, scene 5: Exercise 5.4's solution, bubble sort in OCaml (bpass returning a pair,
bubble repeating it, a trace, the repeats test, and the `x < y` slip that loops forever).
Clips c7.bubcode.1 - c7.bubcode.6.

Exports for ch7's recap: rule_pair() (GREEN `x <= y` over the RED struck-through `x < y`),
bpass_code(), bubble_code(). Every reply checked with OCaml 5.4.1 (the slipped bubble on
[3; 5; 3; 1; 5] still running when `timeout 10` stopped it; SIGINT after 3 s: `Interrupted.`).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

K = load_scene("ch6_s4_hints1")          # the exercise-card kit
H = load_scene("ch6_s5_hints2")          # card 5.4, bracket_over
LEFT_X = -6.3

BPASS_SRC = ("let rec bpass = function\n"
             "  | x::y::ys ->\n"
             "      if x <= y then\n"
             "        let (zs, s) = bpass (y::ys) in (x::zs, s)\n"
             "      else\n"
             "        let (zs, _) = bpass (x::ys) in (y::zs, true)\n"
             "  | xs -> (xs, false)")
BUBBLE_SRC = ("let rec bubble xs =\n"
              "  let (ys, swapped) = bpass xs in\n"
              "  if swapped then bubble ys else ys")


def ocode(src, size=28):
    return Code(src, size=size)


def _paint(code, sub, color):
    k = 0
    while True:
        try:
            code.find(sub, nth=k).set_color(color)
        except ValueError:
            return code
        k += 1


def bpass_code(size=28, slip=False):
    """bpass, keywords BLUE, every `bpass` YELLOW, true/false GREEN; slip: `x < y` RED."""
    src = BPASS_SRC.replace("x <= y", "x < y") if slip else BPASS_SRC
    code = Code(src, size=size)
    _paint(code, "bpass", YELLOW)
    _paint(code, "true", GREEN)
    _paint(code, "false", GREEN)
    if slip:
        code.find("x < y").set_color(RED)
    return code


def bubble_code(size=28):
    code = Code(BUBBLE_SRC, size=size)
    _paint(code, "bubble", YELLOW)
    _paint(code, "bpass", YELLOW)
    return code


def rule_pair(size=56):
    """GREEN `x <= y` over the RED `x < y`, struck through. .good .bad .strike; at ORIGIN."""
    good = Mono("x <= y", size=size, color=GREEN)
    bad = Mono("x < y", size=size, color=RED)
    VGroup(good, bad).arrange(DOWN, buff=0.45)
    strike = Line(bad.get_left() + LEFT * 0.15, bad.get_right() + RIGHT * 0.15).set_stroke(RED, 5)
    g = VGroup(good, bad, strike).move_to(ORIGIN)
    g.good, g.bad, g.strike = good, bad, strike
    return g


def left_at(mob, y, x=LEFT_X):
    return mob.move_to([x, y, 0], aligned_edge=LEFT)


def top_at(mob, top, x=LEFT_X):
    mob.move_to([x, 0, 0], aligned_edge=LEFT)
    return mob.shift(UP * (top - mob.get_top()[1]))


def fit(c, cue=None, frac=0.7, lo=0.5, hi=1.5, nth=0):
    return min(hi, max(lo, frac * c.until(cue, floor=0.0, nth=nth)))


def pass_row(values, scale=0.5):
    """A small ConsChain (values re-enlarged), for a pass (s4's rows weren't built yet)."""
    ch = ConsChain(values).scale(scale)
    for cell in ch.cells:
        cell.label.scale(1.4).set_z_index(1)
    ch.nil.scale(1.5)
    return ch


def arc_swap(a, b, arc=0.7 * PI):
    pa, pb = a.get_center().copy(), b.get_center().copy()
    return [a.animate(path_arc=arc).move_to(pb), b.animate(path_arc=arc).move_to(pa)]


class BubbleCode(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        K.hold_for(self, self.label_born, len("test with repeats"))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # 1: the four cards; 5.4 grows from its card: task, slot, the test; pause
    def clip1(self):
        row = K.four_cards()
        card = H.card_5_4()
        test = Code(f"{H.EX54_TEST[0]}  ⇒  {H.EX54_TEST[1]}", size=34).move_to(DOWN * 2.2)
        test.find("bubble").set_color(YELLOW)
        tag = K.pause_tag()
        self.card, self.test, self.tag = card, test, tag
        with self.say("c7.bubcode.1") as c:
            self.play(*appear(row.cards, row.note, lag=0.2), run_time=0.8)  # early: the overview, recalled
            self.wait(0.8)
            src = row.cards[3].frame
            others = [m for m in (*row.cards, row.note) if m is not row.cards[3]]
            self.play(*during([TransformFromCopy(src, card.frame)], 0, 0.6),
                      *during([FadeOut(m) for m in (*others, row.cards[3])], 0, 0.45),
                      *during(appear(card.header), 0.5, 1), run_time=1.4)
            c.wait_until(own_word=card.task, cue="implement")
            self.play(*appear(card.task, card.name, lag=0.3),
                      *during([FadeIn(card.slot, shift=0.2 * DOWN)], 0.4, 1), run_time=1.4)
            c.wait_until("tests")
            self.play(*appear(test), run_time=1.0)
            c.wait_until("stop")
            self.play(*appear(tag, shift=0.2 * LEFT), run_time=0.7)
            self.play(FlashAround(tag[0], color=YELLOW, time_width=1.5, buff=0.12), run_time=1.2)

    # 2: the pass's pair; bpass, walked; the pair's slots fill from the code
    def clip2(self):
        card = self.card
        head = VGroup(card.name, card.slot)
        head_t = head.copy().scale(0.8).move_to([LEFT_X, 3.52, 0], aligned_edge=LEFT)
        py = 2.3
        lp = T("(", size=50).move_to([1.3, py, 0])
        q1 = T("?", size=50, color=GOLD).move_to([2.3, py, 0])
        cm = T(",", size=50).move_to([3.3, py - 0.12, 0])
        q2 = T("?", size=50, color=GOLD).move_to([4.45, py, 0])
        rp = T(")", size=50).move_to([5.55, py, 0])
        l_list = T("list", size=30, color=DIM).move_to([2.3, 3.0, 0])
        l_sw = T("swapped", size=30, color=DIM).move_to([4.45, 3.0, 0])
        b_tag = K.Tag("bool", GREEN).next_to(l_sw, RIGHT, buff=0.2)
        code = top_at(bpass_code(28), 3.1)
        pat = Code("x::y::ys", size=56).move_to([0, -1.35, 0])
        y0 = pat.get_bottom()[1] - 0.1
        braces, blabels = [], []
        for sub, word, color in (("x", "first", FG), ("y", "second", GOLD), ("ys", "the rest", TEAL)):
            g = pat.find(sub)
            b = Brace(Line([g.get_left()[0], y0, 0], [g.get_right()[0], y0, 0]), DOWN, buff=0.02,
                      color=color)
            braces.append(b)
            blabels.append(T(word, size=30, color=color).next_to(b, DOWN, buff=0.08))
        for lab in blabels[1:]:
            lab.align_to(blabels[0], UP)

        def fill(s, slot):
            m = Code(s, size=34)
            if s in ("true", "false"):
                m.set_color(GREEN)
            return m.move_to(slot)

        f1a, f1b = fill("x::zs", q1), fill("s", q2)
        f2a, f2b = fill("y::zs", q1), fill("true", q2)
        f3a, f3b = fill("xs", q1), fill("false", q2)
        ln = code.line
        with self.say("c7.bubcode.2") as c:
            # "One pass returns two things, the new list, and whether it swapped anything."
            gone = [card.frame, card.header, card.task, self.test]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during([Transform(head, head_t)], 0.2, 0.8),
                      *during(appear(lp, q1, cm, q2, rp, lag=0.05), 0.55, 1), run_time=1.5)
            c.wait_until(own_word=l_list, cue="new list")
            self.play(*appear(l_list), *disappear(self.tag), run_time=0.8)
            c.wait_until(own_word=l_sw, cue="whether")
            self.play(*appear(l_sw, b_tag, lag=0.3), run_time=1.0)  # early: ch6's pair, its bool tag recalled
            # "We'll call it bee-pass."
            c.wait_until("code")
            self.play(*appear(code, shift=0.25 * UP), run_time=1.2)  # early: the code shown whole, then walked
            # "A list with at least two items starts with ex and why."
            c.wait_until("pairs")
            box = token_box(code.find("x::y::ys"), ln(1))
            self.play(FadeIn(box), *appear(pat, shift=0.2 * UP), run_time=1.1)
            c.wait_until("starts with")
            self.play(*[a for b, lab in zip(braces, blabels)
                        for a in (GrowFromCenter(b), FadeIn(lab, shift=0.2 * DOWN))],
                      run_time=1.3)  # early: ch6's three parts, recalled
            # "If ex is at most why, ex stays in front, the pass carries on from why, ..."
            c.wait_until("inorder")
            self.play(Transform(box, token_box(code.find("x <= y"), ln(2))), run_time=1.0)
            c.wait_until("carries on")
            self.play(Transform(box, token_box(code.find("bpass (y::ys)"), ln(3))), run_time=0.9)
            c.wait_until("keep its answer")
            grp = code.find("(x::zs, s)")
            self.play(Transform(box, token_box(grp, ln(3))),
                      *during(disappear(q1, q2), 0, 0.35),
                      *fly(code.find("x::zs"), f1a), *fly(grp[-2:-1], f1b), run_time=1.5)
            # "Otherwise, they swap."
            c.wait_until("swap")
            self.play(Transform(box, token_box(code.find("bpass (x::ys)"), ln(5))), run_time=1.0)
            # "Why goes in front, ex is carried on, and the answer is true."
            c.wait_until("why goes")
            self.play(Transform(box, token_box(code.find("(y::zs, true)"), ln(5))),
                      *swap(f1a, f2a), *swap(f1b, f2b), run_time=1.2)
            # "A shorter list is already in order, and nothing swaps."
            c.wait_until("short")
            self.play(Transform(box, token_box(code.find("| xs -> (xs, false)"), ln(6))),
                      *swap(f2a, f3a), *swap(f2b, f3b), run_time=1.2)
        self.code, self.box, self.head = code, box, head
        self.pair = [lp, cm, rp, l_list, l_sw, b_tag, f3a, f3b]
        self.pat = [pat, *braces, *blabels]

    # 3: the carried x; bpass's type; bubble, walked; its type fills ch6's slot; the tail call
    def clip3(self):
        code, box = self.code, self.box
        row = pass_row([3, 5, 9, 4, 7]).move_to([0, -2.3, 0])
        cs = row.cells
        cs[2].label.set_color(YELLOW)
        cx = code.find("(x::ys)")[1]
        ptype = ocode("val bpass : 'a list -> 'a list * bool = <fun>")
        ptype.next_to(code, DOWN, buff=0.16, aligned_edge=LEFT)
        bub = bubble_code(28).next_to(ptype, DOWN, buff=0.2, aligned_edge=LEFT)
        btype = ocode("val bubble : 'a list -> 'a list = <fun>")
        btype.next_to(bub, DOWN, buff=0.15, aligned_edge=LEFT)
        slot = self.head[1]
        tick = check_mark().scale(0.7).move_to(slot.q)
        glow = bub.find("bubble ys")
        ttag = T("a tail call: iterative", size=30, color=DIM)
        ttag.next_to(bub.line(2), RIGHT, buff=0.5)
        with self.say("c7.bubcode.3") as c:
            # "Carrying ex forward is how the largest item rides to the end."
            self.play(*during([FadeOut(m) for m in self.pat], 0, 0.45),
                      *during([Transform(box, token_box(code.find("bpass (x::ys)"), code.line(5)))], 0.1, 0.7),
                      *during(appear(row, shift=None), 0.5, 1), run_time=1.3)
            self.play(cx.animate.set_color(YELLOW), *arc_swap(cs[2].label, cs[3].label), run_time=1.0)
            self.play(*arc_swap(cs[2].label, cs[4].label), run_time=0.8)
            # "Bee-pass takes an alpha list, and returns an alpha list paired with a bool."
            c.wait_until("ptype")
            self.play(*appear(ptype, shift=0.2 * UP), run_time=1.0)
            c.wait_until("paired")
            self.play(FlashUnder(ptype.find("'a list * bool"), color=YELLOW, time_width=1.5),
                      run_time=1.4)
            # "Bubble sort runs one pass."
            c.wait_until("bubble")
            self.play(*during(disappear(box, row, *self.pair), 0, 0.45),
                      *during(appear(bub, shift=0.25 * UP), 0.45, 1), run_time=1.4)  # early: the code shown whole, then walked
            # "If it swapped, it goes again, on the new list."
            c.wait_until("again")
            box2 = token_box(bub.find("then bubble ys"), bub.line(2))
            self.play(FadeIn(box2), run_time=0.8)
            # "If not, the list is sorted."
            c.wait_until("stop2")
            self.play(Transform(box2, token_box(bub.find("else ys"), bub.line(2))), run_time=0.8)
            # "It's alpha list to alpha list."
            c.wait_until("btype")
            self.play(*disappear(box2), *appear(btype), run_time=1.0)
            self.play(*swap(slot.q, tick), slot.box.animate.set_stroke(GREEN),
                      FlashAround(slot, color=GREEN, time_width=1.5), run_time=1.2)
            # "The repeat is the last thing bubble does, so it's iterative."
            c.wait_until("tail")
            self.play(*recolor(glow, YELLOW), FlashAround(glow, color=YELLOW, time_width=1.5),
                      run_time=1.2)
            c.wait_until(own_word=ttag, cue="so it's iterative")
            self.play(*appear(ttag, shift=0.2 * LEFT), run_time=0.8)
        self.bub, self.ttag = bub, ttag
        self.c3 = [code, ptype, btype, *self.head, tick]

    # 4: three passes, one reply each; bubble's reply; the repeats test
    def clip4(self):
        bub, ttag = self.bub, self.ttag
        dy = 3.4 - bub.get_top()[1]
        rows = [("bpass [3; 5; 9; 4; 7];;", "- : int list * bool = ([3; 5; 4; 7; 9], true)"),
                ("bpass [3; 5; 4; 7; 9];;", "- : int list * bool = ([3; 4; 5; 7; 9], true)"),
                ("bpass [3; 4; 5; 7; 9];;", "- : int list * bool = ([3; 4; 5; 7; 9], false)")]
        ys = [1.35, 0.1, -1.15]
        ins = [left_at(ocode(a), y) for (a, _), y in zip(rows, ys)]
        outs = [left_at(ocode(b), y - 0.5) for (_, b), y in zip(rows, ys)]
        for o in outs:
            _paint(o, "true", GREEN)
            _paint(o, "false", GREEN)
        bi = left_at(ocode("bubble [3; 5; 9; 4; 7];;"), -2.4)
        bo = left_at(ocode("- : int list = [3; 4; 5; 7; 9]"), -2.9)
        bk = check_mark().next_to(bo, RIGHT, buff=0.45)
        di = left_at(ocode("bubble [3; 5; 3; 1; 5];;"), -1.15)
        do = left_at(ocode("- : int list = [1; 3; 3; 5; 5]"), -1.65)
        dk = check_mark().next_to(do, RIGHT, buff=0.45)
        note = T("4 passes · 16 comparisons", size=36, color=GOLD).move_to([0, -2.7, 0])
        with self.say("c7.bubcode.4") as c:
            # "On our list, the first pass gives three, five, four, seven, nine, and reports a swap."
            self.play(*during([FadeOut(m) for m in self.c3], 0, 0.45),
                      *during([bub.animate.shift(UP * dy), ttag.animate.shift(UP * dy)], 0.2, 0.8),
                      *during(appear(ins[0]), 0.6, 1), run_time=1.6)
            c.wait_until("gives")
            self.play(*appear(outs[0]), run_time=1.0)
            c.wait_until("reports")
            self.play(FlashAround(outs[0].find("true"), color=GREEN, time_width=1.5), run_time=1.0)
            # "The second pass gives the sorted list, and reports a swap again."
            c.wait_until("p2")
            self.play(*appear(ins[1]), run_time=1.0)
            c.wait_until("gives the sorted")
            self.play(*appear(outs[1]), run_time=0.9)
            c.wait_until("swap again")
            self.play(FlashAround(outs[1].find("true"), color=GREEN, time_width=1.5), run_time=1.0)
            # "The third changes nothing and reports false, so bubble returns the sorted list."
            c.wait_until("p3")
            self.play(*appear(ins[2]), *disappear(ttag), run_time=0.9)
            self.play(*appear(outs[2]), run_time=0.8)
            c.wait_until("false")
            self.play(FlashAround(outs[2].find("false"), color=GREEN, time_width=1.5), run_time=1.0)
            c.wait_until("so bubble")
            self.play(*appear(bi, bo, lag=0.3), run_time=1.0)
            self.play(Create(bk), run_time=0.6)
            # "With repeats, three, five, three, one, five becomes one, three, three, five, five, ..."
            c.wait_until("dups")
            ddy = 1.35 - ins[2].get_y()
            self.play(*during([FadeOut(m) for m in (*ins[:2], *outs[:2])], 0, 0.45),
                      *during([m.animate.shift(UP * ddy) for m in (ins[2], outs[2], bi, bo, bk)], 0.3, 0.8),
                      *during(appear(di), 0.6, 1), run_time=1.6)
            c.wait_until("becomes")
            self.play(*appear(do), run_time=1.0)
            self.play(Create(dk), run_time=0.6)
            c.wait_until(own_word=note, cue="four passes")
            self.play(*appear(note), run_time=0.9)
        self.c4 = [bub, ins[2], outs[2], bi, bo, bk]
        self.dups = [di, do, dk, note]

    # 5: the slip x < y; it still works without repeats; equal neighbours swap; forever
    def clip5(self):
        code = top_at(bpass_code(28), 3.3)
        slip = top_at(bpass_code(28, slip=True), 3.3)
        lt = slip.find("x < y")
        ci = left_at(ocode("bubble [3; 5; 9; 4; 7];;"), -0.65)
        co = left_at(ocode("- : int list = [3; 4; 5; 7; 9]"), -1.15)
        ck = check_mark().next_to(co, RIGHT, buff=0.45)
        eq = K.tiles([3, 3], side=0.85, gap=0.22, size=40).move_to([4.3, -1.0, 0])
        eq_br = H.bracket_over(eq.sq[0], eq.sq[1], color=RED)
        yt = slip.find("(y::zs, true)")

        rem = Code("if x < y then", size=30)
        rem.find("x < y").set_color(RED)
        left_at(rem, 3.35)
        rows = [("bpass [3; 5; 3; 1; 5];;", "- : int list * bool = ([3; 3; 1; 5; 5], true)"),
                ("bpass [3; 3; 1; 5; 5];;", "- : int list * bool = ([3; 1; 3; 5; 5], true)"),
                ("bpass [3; 1; 3; 5; 5];;", "- : int list * bool = ([1; 3; 3; 5; 5], true)")]
        ys = [2.5, 1.3, 0.1]
        ins = [left_at(ocode(a), y) for (a, _), y in zip(rows, ys)]
        outs = [left_at(ocode(b), y - 0.5) for (_, b), y in zip(rows, ys)]
        for o in outs:
            _paint(o, "true", GREEN)
        outs[2].find("[1; 3; 3; 5; 5]").set_color(GREEN)
        ni = left_at(ocode("bpass [1; 3; 3; 5; 5];;"), -1.1)
        no = left_at(ocode("- : int list * bool = ([1; 3; 3; 5; 5], true)"), -1.75)
        _paint(no, "true", GREEN)
        loop = CurvedArrow([no.get_right()[0], -2.1, 0], [LEFT_X + 0.3, -2.1, 0], angle=-0.5,
                           color=RED, stroke_width=3, tip_length=0.2)
        loop_lbl = T("round again, forever", size=30, color=RED).next_to(loop, DOWN, buff=0.12)
        twins = [(no.find("3", nth=0)[0], no.find("3", nth=1)[0]),
                 (no.find("5", nth=0)[0], no.find("5", nth=1)[0])]
        with self.say("c7.bubcode.5", gap=0.9) as c:
            # "Now the tempting slip."
            dd = -1.95 - self.dups[0].get_y()
            di, do, dk, note = self.dups
            self.play(*during([FadeOut(m) for m in self.c4], 0, 0.5),
                      *during([m.animate.shift(UP * dd) for m in (di, do, dk)]
                              + [note.animate.set_y(-3.1)], 0.3, 1), run_time=1.0)
            self.play(*appear(code, shift=0.25 * UP), run_time=1.0)
            # "In the test, write less than, instead of less than or equal."
            c.wait_until("less than")
            self.play(*edit(code, slip), run_time=1.5)
            self.play(FlashAround(lt, color=RED, time_width=1.5), run_time=1.0)
            # "On our list, with no repeats, it still works."
            c.wait_until("chainok")
            self.play(*appear(ci, co, lag=0.3), run_time=1.2)
            c.wait_until("still works")
            self.play(Create(ck), run_time=0.6)
            # "But now two equal neighbours count as out of order, so they swap, ..."
            c.wait_until("equal")
            self.play(*appear(eq, shift=0.2 * UP), *during([GrowFromCenter(eq_br)], 0.5, 1), run_time=1.1)
            c.wait_until("they swap")
            # whole tiles (box and value together) trade places on a half-circle: they pass
            # one above the other, 1.07 apart, so no glyph ever crosses a box edge
            pa, pb = eq.sq[0].get_center().copy(), eq.sq[1].get_center().copy()
            self.play(*[m.animate(path_arc=PI).move_to(pb) for m in (eq.sq[0], eq.vals[0])],
                      *[m.animate(path_arc=PI).move_to(pa) for m in (eq.sq[1], eq.vals[1])],
                      run_time=1.2)
            c.wait_until("reports a swap")
            self.play(*recolor(yt, RED), FlashAround(yt, color=RED, time_width=1.5), run_time=1.2)
            # "On three, five, three, one, five, three passes reach the sorted list."
            c.wait_until("forever")
            self.play(*during([FadeOut(m) for m in (slip, ci, co, ck, eq, eq_br, *self.dups)], 0, 0.45),
                      *during(appear(rem, ins[0], lag=0.2), 0.5, 1), run_time=1.4)
            self.play(*appear(outs[0]), run_time=0.9)
            for k in (1, 2):
                self.play(*appear(ins[k]), run_time=0.8)
                self.play(*appear(outs[k]), run_time=0.6)
            # "After that, every pass swaps the two threes and the two fives, reports true, ..."
            c.wait_until("never")
            self.play(*appear(ni), run_time=0.9)
            self.play(*appear(no), run_time=0.7)
            c.wait_until("two threes")
            self.play(*arc_swap(*twins[0], arc=PI), *arc_swap(*twins[1], arc=PI), run_time=1.0)
            c.wait_until("reports true")
            self.play(FlashAround(no.find("true"), color=RED, time_width=1.5), Create(loop), run_time=1.0)
            self.play(*appear(loop_lbl), run_time=0.8)
            while c.remaining > 1.4:
                self.play(*arc_swap(*twins[0], arc=PI), *arc_swap(*twins[1], arc=PI),
                          VShowPassingFlash(loop.copy().set_stroke(YELLOW, 6), time_width=0.4),
                          run_time=1.0)
                if c.remaining > 1.7:
                    self.wait(0.3)
        self.c5 = [rem, *ins, *outs, ni, no, loop, loop_lbl]

    # 6: the hang; Ctrl-C; the rule; test with repeats
    def clip6(self):
        prompt = Code("# bubble [3; 5; 3; 1; 5];;", size=40)
        prompt.find("bubble").set_color(YELLOW)
        prompt.move_to([-1.4, 2.45, 0])
        face = Circle(radius=0.42).set_stroke(DIM, 3)
        hand = Line(ORIGIN, UP * 0.3).set_stroke(YELLOW, 4)
        hub = Dot(radius=0.05, color=YELLOW)
        clock = VGroup(face, hand, hub).move_to([prompt.get_right()[0] + 1.0, 2.45, 0])
        hand.put_start_and_end_on(face.get_center(), face.get_center() + UP * 0.3)
        cap = RoundedRectangle(corner_radius=0.12, width=2.0, height=0.8)
        cap.set_stroke(FG, 2.5).set_fill(K.CARD_FILL, 1)
        cap_t = Mono("Ctrl-C", size=34).move_to(cap)
        key = VGroup(cap, cap_t).next_to(prompt, RIGHT, buff=0.55)
        intr = left_at(Code("Interrupted.", size=40), 1.65, x=prompt.get_left()[0])
        rp = rule_pair(56).move_to([0, 0.15, 0])
        rp_up = 1.95 - rp.get_y()
        cap2 = T("swap only when x > y", size=36, color=GREEN).next_to(rp, DOWN, buff=0.45)
        chain = ConsChain([3, 5, 3, 1, 5]).scale(0.6)
        for cell in chain.cells:
            cell.label.scale(1.2).set_z_index(1)
        chain.nil.scale(1.25)
        chain.move_to([-0.4, -1.25, 0])
        tk = check_mark().next_to(chain, RIGHT, buff=0.45)
        tcap = T("test with repeats", size=36, color=GREEN).next_to(chain, DOWN, buff=0.45)
        tcap.set_x(0)

        def spin(m, dt):
            m.rotate(-2.4 * dt, about_point=face.get_center())

        with self.say("c7.bubcode.6") as c:
            # "The toplevel never replies."
            self.play(*during([FadeOut(m) for m in self.c5], 0, 0.45),
                      *during(appear(prompt, clock, lag=0.3), 0.5, 1), run_time=1.4)
            hand.add_updater(spin)
            # "Interrupt it, and all it says is, interrupted."
            c.wait_until("interrupt")
            self.play(*swap(clock, key), run_time=1.0)
            hand.clear_updaters()
            self.play(key.animate.shift(DOWN * 0.08), run_time=0.25)
            self.play(key.animate.shift(UP * 0.08), run_time=0.25)
            c.wait_until(own_word=intr, cue="interrupted")
            self.play(*appear(intr), run_time=0.9)
            # "So swap only when ex is strictly greater than why."
            c.wait_until("rule")
            self.play(*set_alpha([prompt, key, intr], 0.4), *appear(rp.bad), run_time=1.2)
            self.play(Create(rp.strike), *during(appear(rp.good, shift=0.25 * UP), 0.3, 1), run_time=1.3)
            c.wait_until(own_word=cap2, cue="strictly")
            self.play(*appear(cap2), run_time=0.9)
            # "And, as with selection sort, always test with repeats."
            c.wait_until("test")
            self.play(*during(disappear(prompt, key, intr), 0, 0.4),
                      *during([m.animate.shift(UP * rp_up) for m in (rp, cap2)], 0.25, 0.75),
                      *during(appear(chain, shift=0.2 * UP), 0.6, 1), run_time=1.6)
            c.wait_until(own_word=tcap, cue="repeats")
            self.play(*appear(tcap), Create(tk), run_time=0.9)
            self.label_born = self.time
