"""Chapter 5, scene 1: Hook. Greedy's dead end replayed on the 5 -> 2 till, then the idea of the
chapter: keep every way, as a tree of choices. Clips c5.hook.1 – c5.hook.2.

Layout (frame x ±7.1, y ±4):
hook.1  {title}: title_card("Part 5 · Every way to make change"), centred, held into {stuck}.
        "five and two": the card goes; ch4_s6_greedy's setting comes back at its positions: the till
        till_chain([5, 2], 1.0) centred (-1.30, 2.55), DIM "amount" T 30 (3.40, 3.25), GOLD "6" T 64
        (3.40, 2.55), DIM "paid" T 30 left of paid slot 0 (-3.32, 1.20). "took the five": a copy of
        the 5 disc drops into slot 0; "left one": 6 -> 1.
        {fail}: the 5 cell, then the 2 cell, dims with a RED "too big" (T 30); "the till ran out":
        both slide off left, the TEAL nil flashes; "an exception": RED Code 32 reply centred (0, -0.30).
        {twos}: three GREEN coin(2) discs drop into a fresh row at y -1.55 (x -1.12 / 0 / 1.12);
        "two plus two": MathTex 56 GREEN `2 + 2 + 2 = 6` born from them at y -2.65.
hook.2  {idea}: the top clears (nil, counter); the root node "6, [5; 2]" (Mono 40, 6 GOLD, [5; 2]
        TEAL, BLUE box 3.5 x 0.85 as ch4_s7's end card) at (0, 1.85); the "use 5" edge (FG 4) grows
        down-left as the paid 5 becomes its tag's 5 (T 32, 5 GOLD). "never takes it back": the
        exception shrinks into a RED cross (r 0.3), the dead end at (-3.3, -0.25).
        {all}/"new idea": YELLOW "every way, not one" (T 48) at y 3.2; "every way" flashes.
        {tree}: "a dead end": the use edge turns RED; "the other paths": the sum goes, the "skip 5"
        edge opens down-right and the GREEN 2s slide up to its end, centred (3.3, -0.25).
        {today}: the answer's shape at (0, -2.45): a TEAL box of three TEAL solution boxes
        [2 2] [2 1 1] [1 1 1 1] (s2's example), scale 1.4 (9.3 wide); "one list": TEAL flash.
End: fade to an empty frame (s2 opens fresh).

STATUS: built; check clean apart from dwell notes: the title card's course/part lines (5.1 s; the
till comes in on "five and two") and the two "too big" labels (~1.3 s; the brief's dim-and-slide
inside "Every coin was now too big, the till ran out").
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# ── the coin and the till (copied from scenes/ch1_s1_hook.py, scenes/ch4_s2_idea.py) ─────────
COIN_R = 0.42
COIN_LABEL = 34


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def till_chain(values, scale=0.85):
    """The till: ConsChain(values) scaled `scale`; each cell's label is coin(v, r=COIN_R*scale)
    (the value stays size 34). Nil TEAL as in ConsChain. Centred on ORIGIN."""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


# ── solutions (the chapter-wide look) ─────────────────────────────────────────
def solution(values, s=0.6):
    """One way to make change: coins (scaled s) in a row inside a TEAL rounded box."""
    if values:
        inner = VGroup(*[coin(v).scale(s) for v in values]).arrange(RIGHT, buff=0.1)
    else:
        inner = Square(side_length=2 * COIN_R * s).set_opacity(0)
    box = RoundedRectangle(corner_radius=0.1, width=inner.width + 0.24, height=inner.height + 0.24)
    box.set_stroke(TEAL, 3).move_to(inner)
    return VGroup(box, inner)


def solutions(lists):
    """A list of solutions: solution boxes in a row inside a bigger TEAL rounded box."""
    row = VGroup(*[solution(v) for v in lists]).arrange(RIGHT, buff=0.2)
    big = RoundedRectangle(corner_radius=0.15, width=row.width + 0.4, height=row.height + 0.4)
    big.set_stroke(TEAL, 4).move_to(row)
    return VGroup(big, *row)


# ── layout ────────────────────────────────────────────────────────────────────
TILL_Y, CHAIN_X = 2.55, -1.3            # ch4_s6_greedy's end shot
COUNTER_X, AMOUNT_LABEL_Y = 3.4, 3.25
PAID_Y = 1.2

EXC = 'Exception: Failure "no more coins!".'
EXC_SIZE, EXC_Y = 32, -0.30
TWOS_X, TWOS_Y, EQ_Y = (-1.12, 0.0, 1.12), -1.55, -2.65

ROOT_Y = 1.85                           # ch4_s7's end card had it at 1.75, kids at ±2.8
KID_DX, KID_Y = 3.3, -0.25
HEAD_Y = 3.2
PREV_Y, PREV_S = -2.45, 1.4
PREVIEW = [[2, 2], [2, 1, 1], [1, 1, 1, 1]]


def faded(mob, k):
    """A copy of mob with every fill and stroke opacity scaled by k (keeps faint fills faint)."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k)
    return t


def edge(a, b, color=FG):
    return Line(a, b, buff=0).set_stroke(color, 4)


def edge_tag(text, e, side):
    tag = T(text, size=32, t2c={"5": GOLD})
    tag.next_to(e.point_from_proportion(0.6), side, buff=0.4).shift(0.12 * UP)
    return tag


class Hook(NarratedScene):
    def construct(self):
        self.build()
        self.greedy_again()     # c5.hook.1
        self.every_way()        # c5.hook.2
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── everything, built up front ────────────────────────────────────────────────
    def build(self):
        self.card = title_card("Part 5 · Every way to make change")

        self.chain = till_chain([5, 2], scale=1.0).move_to([CHAIN_X, TILL_Y, 0])
        self.amount = T("amount", 30, DIM).move_to([COUNTER_X, AMOUNT_LABEL_Y, 0])
        self.num = T("6", 64, GOLD).move_to([COUNTER_X, TILL_Y, 0])
        slot0 = self.chain.cells[0].box.get_x()
        self.paid = T("paid", 30, DIM)
        self.paid.move_to([slot0 - COIN_R - 0.3 - self.paid.width / 2, PAID_Y, 0])
        self.paid5 = coin(5).move_to([slot0, PAID_Y, 0])
        self.bigs = [T("too big", 30, RED).next_to(c, UP, buff=0.12) for c in self.chain.cells]
        self.exc = Code(EXC, size=EXC_SIZE).set_color(RED).move_to([0, EXC_Y, 0])

        self.twos = VGroup(*[coin(2).set_color(GREEN).move_to([x, TWOS_Y, 0]) for x in TWOS_X])
        self.eq = MathTex("2", "+", "2", "+", "2", "=", "6", font_size=56, color=GREEN)
        self.eq.move_to([0, EQ_Y, 0])

        # the tree's outline: root, "use 5" to a dead end, "skip 5" to the 2s
        box = RoundedRectangle(corner_radius=0.15, width=3.5, height=0.85).set_stroke(BLUE, 3)
        box.move_to([0, ROOT_Y, 0])
        label = Mono("6, [5; 2]", size=40, t2c={"6": GOLD, "[5; 2]": TEAL}).move_to(box)
        self.root = VGroup(box, label)
        self.dead = cross_mark(RED, r=0.3).move_to([-KID_DX, KID_Y, 0])
        self.e_use = edge(box.get_bottom() + LEFT * 0.9, self.dead.get_top() + UP * 0.12)
        self.tag_use = edge_tag("use 5", self.e_use, LEFT)
        self.twos_at = np.array([KID_DX, KID_Y, 0])
        top = self.twos_at + UP * (COIN_R + 0.12)
        self.e_skip = edge(box.get_bottom() + RIGHT * 0.9, top)
        self.tag_skip = edge_tag("skip 5", self.e_skip, RIGHT)

        self.head = T("every way, not one", 48, YELLOW).move_to([0, HEAD_Y, 0])
        self.preview = solutions(PREVIEW).scale(PREV_S).move_to([0, PREV_Y, 0])

    def skip_cell(self, i):
        """The i-th till cell dims and gets its RED "too big"."""
        cell, arrow = self.chain.cells[i], self.chain.arrows[i]
        return [Transform(cell, faded(cell, 0.35)), Transform(arrow, faded(arrow, 0.35)),
                FadeIn(self.bigs[i], shift=0.15 * DOWN)]

    # ── hook.1: greedy's dead end, once more ─────────────────────────────────────
    def greedy_again(self):
        card, ch, cells = self.card, self.chain, self.chain.cells
        with self.say("c5.hook.1") as c:
            # "Last time, we wrote a greedy function for making change, ..."
            self.play(
                time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.7),
                time_span(GrowFromCenter(card.rule), 0, 0.7),
                time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.15, 0.85),
                time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.3, 1.0),
                run_time=1.0,
            )

            # "With coins of five and two, ..."  (the card holds into the sentence)
            c.wait_until("five and two")
            self.play(time_span(FadeOut(card, shift=0.3 * UP), 0, 0.7),
                      time_span(FadeIn(ch, lag_ratio=0.15), 0.3, 1.5),
                      time_span(FadeIn(self.paid, shift=0.2 * DOWN), 0.8, 1.5), run_time=1.5)
            # "... and an amount of six, ..."
            c.wait_until("an amount of six")
            self.play(FadeIn(self.amount, self.num, shift=0.2 * DOWN),
                      run_time=min(0.9, 0.9 * c.until("took the five")))
            # "... it took the five, ..."
            c.wait_until("took the five")
            self.play(TransformFromCopy(cells[0].label, self.paid5),
                      FlashAround(cells[0], color=YELLOW, time_width=1.5),
                      run_time=min(1.3, 0.9 * c.until("that left one")))
            # "... and that left one."
            c.wait_until("that left one")
            one = T("1", 64, GOLD).move_to(self.num)
            self.play(ReplacementTransform(self.num, one), run_time=min(1.0, 0.9 * c.until("fail")))
            self.num = one

            # "Every coin was now too big, ..."
            c.wait_until("fail")
            t = min(1.0, 0.9 * c.until("the till ran out"))
            self.play(*[time_span(a, 0, 0.7 * t) for a in self.skip_cell(0)],
                      *[time_span(a, 0.3 * t, t) for a in self.skip_cell(1)], run_time=t)
            # "... the till ran out, ..."
            c.wait_until("the till ran out")
            off, t = 1.6 * LEFT, min(1.6, 0.95 * c.until("an exception"))
            gone = []
            for i, (a, b) in enumerate([(0.45, 0.9), (0.55, 1.0)]):
                for m in (cells[i], ch.arrows[i], self.bigs[i]):
                    gone.append(time_span(FadeOut(m, shift=off), a * t, b * t))
            self.play(*gone, time_span(FlashAround(ch.nil, color=TEAL, time_width=1.5), 0.5 * t, t),
                      run_time=t)
            # "... and it raised an exception."
            c.wait_until("an exception")
            self.play(FadeIn(self.exc, shift=0.3 * DOWN), run_time=1.0)

            # "Yet there's a way to make six."
            c.wait_until("twos")
            self.play(LaggedStart(*[FadeIn(d, shift=0.5 * DOWN) for d in self.twos], lag_ratio=0.3),
                      run_time=1.3)
            # "Two, plus two, plus two."
            c.wait_until("two plus two")
            eq, t = self.eq, min(2.2, c.remaining)
            anims = [time_span(TransformFromCopy(self.twos[i][1], eq[2 * i]),
                               (0.27 * i) * t, (0.27 * i + 0.45) * t) for i in range(3)]
            anims += [time_span(FadeIn(eq[1]), 0.18 * t, 0.45 * t),
                      time_span(FadeIn(eq[3]), 0.45 * t, 0.72 * t),
                      time_span(FadeIn(eq[5]), 0.72 * t, 0.92 * t),
                      time_span(FadeIn(eq[6]), 0.8 * t, t)]
            self.play(*anims, run_time=t)
            settle(self, eq)

    # ── hook.2: every way, as a tree of choices ───────────────────────────────────
    def every_way(self):
        tag = self.tag_use
        with self.say("c5.hook.2") as c:
            # "The trouble is that greedy commits to its first choice, ..."
            # The top clears; the call becomes a node, and the paid row becomes its one path.
            self.play(*[time_span(FadeOut(m, shift=0.2 * UP), 0, 0.7)
                        for m in (self.chain.nil, self.amount, self.num)],
                      time_span(FadeIn(self.root, shift=0.3 * DOWN), 0.3, 1.2),
                      time_span(Create(self.e_use), 0.9, 1.8),
                      time_span(FadeOut(self.paid), 0.9, 1.5),
                      time_span(FadeOut(self.paid5[0], scale=0.5), 1.0, 1.7),
                      time_span(ReplacementTransform(self.paid5[1], tag[3]), 1.0, 2.0),
                      *[time_span(FadeIn(g, shift=0.15 * RIGHT), 1.3, 2.0) for g in tag[:3]],
                      run_time=2.0)
            settle(self, tag)
            # "... and never takes it back."
            c.wait_until("never takes it back")
            self.play(FadeOut(self.exc, target_position=self.dead, scale=0.1),
                      time_span(GrowFromCenter(self.dead), 0.4, 1.2), run_time=1.2)

            # "So here's a new idea."
            c.wait_until("new idea")
            self.play(FadeIn(self.head, shift=0.3 * DOWN), run_time=1.0)
            # "Instead of returning one way to make change, return every way."
            c.wait_until("every way")
            self.play(FlashUnder(VGroup(*self.head[:8]), color=YELLOW, time_width=1.5),
                      run_time=min(1.4, c.until("tree")))

            # "Then a dead end only closes one path, ..."
            c.wait_until("a dead end")
            self.play(self.e_use.animate.set_stroke(RED),
                      FlashAround(self.dead, color=RED, time_width=1.5),
                      run_time=min(1.2, 0.9 * c.until("the other paths")))
            # "... and the other paths still get explored."
            c.wait_until("the other paths")
            self.play(time_span(FadeOut(self.eq, shift=0.2 * DOWN), 0, 0.7),
                      time_span(Create(self.e_skip), 0.2, 1.1),
                      time_span(self.twos.animate.move_to(self.twos_at), 0.4, 1.8),
                      time_span(FadeIn(self.tag_skip, shift=0.2 * DOWN), 0.9, 1.6), run_time=1.8)

            # "In this chapter, we write that function, ..."
            c.wait_until("today")
            prev = self.preview
            t = min(2.0, 0.95 * c.until("one list"))
            self.play(time_span(Create(prev[0]), 0, 0.5 * t),
                      *[time_span(FadeIn(s, shift=0.2 * DOWN), (0.3 + 0.2 * i) * t, (0.6 + 0.2 * i) * t)
                        for i, s in enumerate(prev[1:])], run_time=t)
            settle(self, prev)
            # "... and see how one list can hold all of its answers."
            c.wait_until("one list")
            self.play(FlashAround(prev, color=TEAL, time_width=1.5),
                      run_time=min(1.4, 0.95 * c.until("all of its answers")))
