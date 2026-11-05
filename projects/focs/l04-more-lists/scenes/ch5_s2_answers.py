"""Chapter 5, scene 2: a list of answers (the result type and the two base cases). Clips c5.answers.1 – c5.answers.4.

PLAN
  c5.answers.1  {type} ch4's reply at the top, DIM, its return type `int list` turning GREEN.
                {one} one solution, big: a TEAL box, coins 2 2 2 drop in; "one way: int list".
                {many} it shrinks and a bigger TEAL box opens around it. {example} coins 2, 1 -> "make 4";
                the big box widens; the three solutions arrive one per phrase with their code below.
                {listlist} the reply grows `int list` -> `int list list` (new `list` flashes GREEN);
                "a list of solutions: int list list".
  c5.answers.2  split, left: amount 0, "?" -> "1" {exactly} -> one empty solution box ("no coins");
                {nil} `[]` under it, then a big box around it, `[]` -> `[[]]`; {success} GREEN "one way: no coins".
  c5.answers.3  right: till `[]` and amount 6 {none}; {noway} an empty big box, `[]`; {failure} RED "no ways".
                {pair} the two boxes centred and larger, labels -> GREEN "success" / RED "failure"; each flashes.
  c5.answers.4  {noraise} ch4's exception (Code 32, RED) above them, struck out. {quiet} `[]` spotlit.
                {combine} the example row returns; an empty box with a GOLD `@` drops into it; the row is unchanged.

CONTINUITY (the solution-box look for the whole chapter, see solution() / solutions() below)
  base proportions: coin(v) scaled 0.6 (r 0.252), buff 0.1, in a TEAL RoundedRectangle (corner 0.1,
  stroke 3, padding 0.12): 0.744 tall. List of solutions: boxes buff 0.2 in a TEAL RoundedRectangle
  (corner 0.15, stroke 4, padding 0.2); empty list = 1.144 square.
  {example} (end of c5.answers.1): solutions([[2, 2], [2, 1, 1], [1, 1, 1, 1]]).scale(1.48), centred
  at (0, 0): big box 9.85 x 1.69, inner boxes 2.00 / 2.89 / 3.78 wide, 1.10 tall, centres x = -3.63,
  -0.89, 2.74; coins r 0.37, values size 30. Its code `[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]` Code 32
  centred at (0, -1.55). The same row ends the scene alone at (0, -0.5).
  The reply `val change : int list -> int -> int list list = <fun>` Code 28 DIM, `int list list` GREEN,
  left edge x = -6.4, centre y = 3.25.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ── chapter looks (copied from ch1_s1_hook / ch4) ─────────────────────────────
COIN_R = 0.42                # the coin disc reused by ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


SOL = 0.6                    # coin scale inside a solution
PAD1, BUFF1 = 0.12, 0.1      # one solution: padding, coin spacing
PAD2, BUFF2 = 0.2, 0.2       # a list of solutions: padding, box spacing
D = 2 * COIN_R * SOL         # coin diameter in a solution (0.504)
H1 = D + 2 * PAD1            # a solution box's height (0.744)
H2 = H1 + 2 * PAD2           # a list-of-solutions box's height (1.144)


def solution(values):
    """One solution (an int list): coins in a row inside a TEAL box; empty = an H1 square."""
    coins = VGroup(*[coin(v).scale(SOL) for v in values])
    if values:
        coins.arrange(RIGHT, buff=BUFF1)
    w = (coins.width if values else D) + 2 * PAD1
    box = RoundedRectangle(corner_radius=0.1, width=w, height=H1).set_stroke(TEAL, 3)
    coins.move_to(box)
    g = VGroup(box, coins)
    g.box, g.coins = box, coins
    return g


def big_box(width, height=H2):
    return RoundedRectangle(corner_radius=0.15, width=width, height=height).set_stroke(TEAL, 4)


def solutions(lists):
    """A list of solutions (an int list list): solution boxes in a row inside a bigger TEAL box."""
    sols = VGroup(*[solution(v) for v in lists])
    if lists:
        sols.arrange(RIGHT, buff=BUFF2)
    box = big_box(sols.width + 2 * PAD2 if lists else H2)
    sols.move_to(box)
    g = VGroup(box, sols)
    g.box, g.sols = box, sols
    return g


# ── this scene ────────────────────────────────────────────────────────────────
R1 = "val change : int list -> int -> int list = <fun>"
R2 = "val change : int list -> int -> int list list = <fun>"
EXC = 'Exception: Failure "no more coins!".'
LST = "[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]"
EXAMPLE = [[2, 2], [2, 1, 1], [1, 1, 1, 1]]

REPLY_L, REPLY_Y = -6.4, 3.25
K = 1.48                     # the example's scale (coin values at size 30)
BIG1 = 1.6                   # the lone solution at {one} is K * BIG1
Y_BOX = 0.0                  # the example's centre
Y_HDR, Y_LST, Y_LAB = 1.6, -1.55, -2.7
Y_LAB1 = -1.75               # "one way: int list"

BS = 1.9                     # base cases: box scale (big box 2.17 square)
XL, XR = -3.4, 3.4
Y_TAG, Y_Q, Y_ANS, Y_CODE, Y_SUB = 2.4, 1.72, -0.15, -1.85, -2.75
PAIR = 1.25                  # {pair}: scale up about each box centre
XP, Y_P = 2.7, 0.25
Y_PCODE, Y_PLAB = -1.8, -2.8
Y_EXC = 2.35

Y_ROW = -0.5                 # {combine}: the example row
DROP = np.array([3.3, 1.55, 0])


def typed(words, ty, size=36):
    """'words' in serif FG, then a GREEN Mono type, on one baseline."""
    a = T(words, size=size)
    b = Mono(ty, size=size, color=GREEN)
    b.next_to(a, RIGHT, buff=0.22).align_to(a[0], DOWN)
    return VGroup(a, b)


def tag(text, x, y):
    return T(text, size=30, color=DIM).move_to([x, y, 0])


class Answers(NarratedScene):
    def construct(self):
        self.result_type()
        self.zero_case()
        self.empty_till()
        self.no_exception()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c5.answers.1: one way is an int list, every way an int list list ──────
    def result_type(self):
        with self.say("c5.answers.1") as c:
            r1 = Code(R1, size=28).set_color(DIM)
            r1.move_to(UP * REPLY_Y)
            r1.shift(RIGHT * (REPLY_L - r1.get_left()[0]))
            self.play(FadeIn(r1, shift=0.2 * DOWN), run_time=1.0)
            ret = r1.find("int list", nth=1)
            self.play(FlashAround(ret, color=YELLOW, time_width=1.5), *recolor(ret, GREEN),
                      run_time=min(1.5, max(0.6, c.until("one") - 0.3)))
            c.wait_until("one")

            # {one}: a single solution, big
            single = solution([2, 2, 2]).scale(K * BIG1).move_to(UP * Y_BOX)
            lab1 = typed("one way:", "int list").move_to(UP * Y_LAB1)
            self.play(Create(single.box), FadeIn(lab1, shift=0.3 * DOWN),
                      run_time=min(1.4, 0.7 * c.until("such as")))
            c.wait_until("such as")
            self.play(FadeIn(single.coins, shift=0.3 * DOWN, lag_ratio=0.45),
                      run_time=min(2.0, 0.8 * c.until("many")))
            settle(self, single)
            c.wait_until("many")

            # {many}: it shrinks, a bigger box opens around it
            snug = big_box(single.width / (K * BIG1) + 2 * PAD2).scale(K).move_to(UP * Y_BOX)
            self.play(single.animate.scale(1 / BIG1),
                      time_span(GrowFromCenter(snug), 0.5, 1.6), run_time=1.6)
            c.wait_until("example")

            # {example}: coins 2 and 1, make 4; the box widens for three answers
            ex = solutions(EXAMPLE).scale(K).move_to(UP * Y_BOX)
            hdr = VGroup(coin(2).scale(0.9), coin(1).scale(0.9)).arrange(RIGHT, buff=0.22)
            make = T("make 4", size=40, t2c={"4": GOLD})
            hdr.add(make)
            make.next_to(hdr[1], RIGHT, buff=0.45)
            hdr.move_to(UP * Y_HDR)
            self.play(FadeOut(single, scale=0.7), FadeOut(lab1, shift=0.3 * DOWN),
                      ReplacementTransform(snug, ex.box), FadeIn(hdr, shift=0.3 * DOWN), run_time=1.6)
            c.wait_until("Two and two")

            lst = Code(LST, size=32).move_to(UP * Y_LST)
            glyphs = lst.line(0)
            pieces = [[glyphs[0], *lst.find("[2; 2]")],
                      list(lst.find("; [2; 1; 1]")),
                      [*lst.find("; [1; 1; 1; 1]"), glyphs[-1]]]
            nexts = ["Two, one and one", "And four ones", "listlist"]
            for sol, piece, nxt in zip(ex.sols, pieces, nexts):
                self.play(Create(sol.box), FadeIn(sol.coins, shift=0.25 * DOWN, lag_ratio=0.3),
                          *[FadeIn(g, shift=0.2 * UP) for g in piece],
                          run_time=min(1.1, 0.7 * c.until(nxt)))
                c.wait_until(nxt)
            settle(self, ex)
            settle(self, lst)

            # {listlist}: the type grows one `list`
            r2 = Code(R2, size=28).set_color(DIM)
            r2.move_to(UP * REPLY_Y)
            r2.shift(r1.find("val").get_center() - r2.find("val").get_center())
            for g in r2.find("int list list"):
                g.set_color(GREEN)
            new = r2.find("list", nth=2)
            ghost = new.copy()
            lab2 = typed("a list of solutions:", "int list list").move_to(UP * Y_LAB)
            self.play(*[g1.animate.move_to(g2) for g1, g2 in zip(r1.find("= <fun>"), r2.find("= <fun>"))],
                      FadeIn(ghost, shift=0.2 * DOWN), FadeIn(lab2, shift=0.3 * DOWN), run_time=1.4)
            self.remove(r1, ghost)
            self.add(r2)
            self.play(FlashAround(new, color=GREEN, time_width=1.5), run_time=1.5)
            self.reply = r2
            c.wait_until()

    # ── c5.answers.2: change for zero is [[]] ─────────────────────────────────
    def zero_case(self):
        with self.say("c5.answers.2") as c:
            c.wait_until("How many ways")
            amt = tag("amount", XL, Y_TAG)
            zero = T("0", size=64, color=GOLD).move_to([XL, Y_Q, 0])
            sweep_clear(self, time_span(FadeIn(amt, shift=0.3 * DOWN), 0.5, 1.3),
                        time_span(FadeIn(zero, shift=0.3 * DOWN), 0.6, 1.4), keep=[self.reply], run_time=1.4)
            q = T("?", size=80, color=YELLOW).move_to([XL, Y_ANS, 0])
            self.play(FadeIn(q, scale=0.6), run_time=0.9)
            c.wait_until("exactly")

            one = T("1", size=80, color=GOLD).move_to(q)
            self.play(ReplacementTransform(q, one), run_time=1.0)
            c.wait_until("You hand over")

            inner = solution([]).scale(BS).move_to([XL, Y_ANS, 0])
            self.play(FadeTransform(one, inner), run_time=1.2)
            c.wait_until("nil")

            nil = Code("[]", size=40).move_to([XL, Y_CODE, 0])
            self.play(FadeIn(nil, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("so the answer")

            outer = big_box(H2).scale(BS).move_to(inner)
            nn = Code("[[]]", size=40).move_to(nil)
            mid = nn.find("[]")
            ends = [nn.line(0)[0].copy(), nn.line(0)[-1].copy()]
            self.play(GrowFromCenter(outer), nil.animate.move_to(mid),
                      *[FadeIn(e, scale=0.5) for e in ends], run_time=1.6)
            self.remove(nil, *ends)
            self.add(nn)
            c.wait_until("success")

            ok = T("one way: no coins", size=34, color=GREEN).move_to([XL, Y_SUB, 0])
            self.play(FadeIn(ok, shift=0.3 * DOWN), run_time=1.0)
            self.left = dict(tag=amt, q=zero, inner=inner, outer=outer, code=nn, label=ok)
            c.wait_until()

    # ── c5.answers.3: an empty till with money owed is [] ─────────────────────
    def empty_till(self):
        with self.say("c5.answers.3") as c:
            till_tag = tag("till", XR - 1.1, Y_TAG)
            till = Mono("[]", size=56, color=TEAL).move_to([XR - 1.1, Y_Q, 0])
            self.play(FadeIn(till_tag, shift=0.3 * DOWN), FadeIn(till, shift=0.3 * DOWN),
                      run_time=min(1.0, 0.6 * c.until("but there's still money")))
            c.wait_until("but there's still money")
            amt = tag("amount", XR + 1.1, Y_TAG)
            six = T("6", size=64, color=GOLD).move_to([XR + 1.1, Y_Q, 0])
            self.play(FadeIn(amt, shift=0.3 * DOWN), FadeIn(six, shift=0.3 * DOWN),
                      run_time=min(1.0, 0.6 * c.until("noway")))
            c.wait_until("noway")

            empty = big_box(H2).scale(BS).move_to([XR, Y_ANS, 0])
            self.play(GrowFromCenter(empty), run_time=1.2)
            c.wait_until("so the answer")
            nil = Code("[]", size=40).move_to([XR, Y_CODE, 0])
            self.play(FadeIn(nil, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("failure")

            bad = T("no ways", size=34, color=RED).move_to([XR, Y_SUB, 0])
            self.play(FadeIn(bad, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("pair")

            # {pair}: the two answers side by side, larger
            L = self.left
            moves = []
            for mobs, x0, x1 in [([L["inner"], L["outer"], L["code"]], XL, -XP), ([empty, nil], XR, XP)]:
                about = np.array([x0, Y_ANS, 0])
                shift = np.array([x1 - x0, Y_P - Y_ANS, 0])
                for m in mobs:
                    moves.append(m.animate.scale(PAIR, about_point=about).shift(shift))
            succ = T("success", size=44, color=GREEN).move_to([-XP, Y_PLAB, 0])
            fail = T("failure", size=44, color=RED).move_to([XP, Y_PLAB, 0])
            self.play(*[FadeOut(m) for m in (L["tag"], L["q"], till_tag, till, amt, six)],
                      *moves, FadeTransform(L["label"], succ), FadeTransform(bad, fail), run_time=1.8)
            c.wait_until("one way, using nothing")
            self.play(FlashAround(L["outer"], color=GREEN, time_width=1.5, buff=0.12), run_time=1.5)
            c.wait_until("while nil itself")
            self.play(FlashAround(empty, color=RED, time_width=1.5, buff=0.12), run_time=1.5)
            self.pair = dict(left=[L["inner"], L["outer"], L["code"], succ], empty=empty, nil=nil, fail=fail)
            c.wait_until()

    # ── c5.answers.4: no exception; [] combines for free ──────────────────────
    def no_exception(self):
        with self.say("c5.answers.4") as c:
            exc = Code(EXC, size=32).set_color(RED).move_to(UP * Y_EXC)
            strike = Line(exc.get_left() + LEFT * 0.15, exc.get_right() + RIGHT * 0.15).set_stroke(FG, 5)
            self.play(FadeIn(exc, shift=0.2 * DOWN), run_time=0.9)
            self.play(Create(strike), run_time=0.8)
            c.wait_until("quiet")

            P = self.pair
            self.play(*[restyle(m, op=DIMMED) for m in P["left"]],
                      FlashAround(P["empty"], color=RED, time_width=1.5, buff=0.12), run_time=1.5)
            c.wait_until("combine")

            row = solutions(EXAMPLE).scale(K).move_to(UP * Y_ROW)
            empty = P["empty"]
            target = empty.copy().scale(H2 * K / empty.height).move_to(DROP)
            at = Mono("@", size=52, color=GOLD).next_to(target, LEFT, buff=0.35)
            sweep_clear(self, Transform(empty, target), time_span(FadeIn(row, shift=0.3 * UP), 0.5, 1.5),
                        time_span(FadeIn(at), 0.8, 1.5), keep=[empty], run_time=1.5)
            c.wait_until("When we gather up")
            self.play(FlashAround(row, color=YELLOW, time_width=1.5, buff=0.15),
                      run_time=min(1.6, 0.8 * c.until("a dead end")))
            c.wait_until("a dead end")

            slot = row.box.get_right() + LEFT * PAD2 * K * 0.5
            self.play(FadeOut(empty, target_position=slot, scale=0.05),
                      FadeOut(at, target_position=slot, scale=0.05), run_time=min(1.6, 0.8 * c.remaining))
            c.wait_until()
            self.wait(0.6)
