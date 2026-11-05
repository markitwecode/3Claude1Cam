"""Chapter 4, scene 2: the till as a descending int list, three observations, tried on 43. Clips c4.idea.1 – c4.idea.3.

Layout:
idea.1  s1's six coins (coin(v), buff 0.28, ORIGIN) fade in and slide into the till chain at y 0
        (till_chain: ConsChain scaled 0.85, coin(v, r=0.357) in each cell, YELLOW Mono `till` above
        cell 0). {desc}: BLUE "descending" + an arrow growing 50 -> 1 as the values are read.
        {ints}: GREEN `int list` under the chain. "head": cell 0 YELLOW; "one arrow away" by the
        `till` arrow. {pennies}: 43 DIM discs at y -2.4, struck through in RED.
idea.2  {obs}: extras clear, the chain rises to y 1.8. Three cards (scale 1.08) stack centred
        under it, one per mark; card 1's TEAL [] on "empty list", card 2's second line on
        "small enough".
idea.3  {try43}: cards shrink to 1.0 and move right; DIM "amount" + GOLD 43 at the left.
        {fifty}: card 3 flashes, cell 0 RED, then slides off left; `till` moves to the 20.
        {twenty}: card 2 flashes; a copy of the 20 coin drops into the "change" row; 43 -> 23.
        {again}: YELLOW ring on the 20, "still in the till". {each}: cards flash in turn, the
        rest sweeps away.
End shot (s3 re-creates it): the three cards alone, at the right.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

VALUES = [50, 20, 10, 5, 2, 1]

COIN_R = 0.42                # the coin disc reused by ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34

S = 0.85                     # till chain scale: six cells + [] = 12.1 wide
PITCH = (CELL + PTR_W + LINK) * S
CY1, CY2 = 0.0, 1.8          # chain centre y: clip 1 / clips 2-3
DESC_Y = 2.3                 # the "descending" arrow (clip 1)
INTS_Y = -1.15               # `int list`
PENNY_Y = -2.4               # the row of 43 pennies

CARD_TEXT = 32               # observation cards (final size); shown at x1.08 in clip 2
CARD_PAD = 0.26
CARD_BIG = 1.08
CARDS_TOP = CY2 - CELL * S / 2 - 0.4   # top of the card stack (clips 2-3), 0.4 under the chain

AMT_Y, CHG_Y = -0.2, -1.9     # amount / change rows (clip 3), labels' left edge at x -6.3
ROW_X = -6.3


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def till_chain(values, scale=S):
    """The till: ConsChain(values) scaled `scale`; each cell's label is coin(v, r=COIN_R*scale)
    (the value stays size 34). Nil TEAL as in ConsChain. Centred on ORIGIN."""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


def till_pointer(cell, name="till", length=0.75):
    """YELLOW Mono name above a cell with a short arrow down to its box."""
    tip = cell.box.get_top()
    lab = Mono(name, size=36, color=YELLOW).move_to(tip + UP * (length + 0.3))
    arr = Arrow(lab.get_bottom(), tip, buff=0.06, stroke_width=3, color=YELLOW,
                max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)


def ring_flash(mob, color=YELLOW, run_time=1.2):
    ring = Circle(radius=mob.width / 2 + 0.1).move_to(mob).set_stroke(color, 6)
    return VShowPassingFlash(ring, time_width=1.0, run_time=run_time)


def obs_cards():
    """Three observation cards: BLUE bold number, FG text (T 32), DIM rounded frame, equal widths."""
    specs = [("1.", ["change for 0 = no coins"]),
             ("2.", ["largest coin fits?", "use it, reduce the amount"]),
             ("3.", ["too large? remove it"])]
    parts = []
    for num, lines in specs:
        txt = VGroup(*[T(s, size=CARD_TEXT) for s in lines]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        n = T(num, size=CARD_TEXT, color=BLUE, weight=BOLD)
        n.next_to(txt[0], LEFT, buff=0.28).align_to(txt[0][0], DOWN)
        content = VGroup(n, *txt)
        nil = None
        if num == "1.":
            nil = Mono("[]", size=36, color=TEAL).next_to(txt[0], RIGHT, buff=0.5)
            nil.set_y(txt[0][0].get_y())
            content.add(nil)
        parts.append((n, list(txt), nil, content))
    width = max(p[3].width for p in parts) + 2 * CARD_PAD
    cards = VGroup()
    for n, lines, nil, content in parts:
        frame = RoundedRectangle(corner_radius=0.16, width=width, height=content.height + 2 * CARD_PAD)
        frame.set_stroke(DIM, 2).set_fill(BG, 0)
        content.move_to(frame).align_to(frame, LEFT).shift(RIGHT * CARD_PAD)
        card = VGroup(frame, n, *lines, *([nil] if nil is not None else []))
        card.frame, card.num, card.lines, card.nil = frame, n, lines, nil
        cards.add(card)
    cards.arrange(DOWN, buff=0.24)
    return cards


class Idea(NarratedScene):
    def construct(self):
        self.the_list()
        self.observations()
        self.try43()
        # hand-off shot: the three cards alone (s3 re-creates them)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c4.idea.1: the till as a descending int list; the head is at hand ─────────
    def the_list(self):
        coins = VGroup(*[coin(v) for v in VALUES]).arrange(RIGHT, buff=0.28).move_to(ORIGIN)
        self.play(FadeIn(coins), run_time=0.8)

        chain = till_chain(VALUES).move_to(UP * CY1)
        labels = [cell.label for cell in chain.cells]
        for cell in chain.cells:          # build the bare cells; s1's coins become the labels
            cell.remove(cell.label)
        till = till_pointer(chain.cells[0])
        self.chain, self.till = chain, till

        c0, c5 = chain.cells[0].box.get_center(), chain.cells[-1].box.get_center()
        desc_arrow = Arrow([c0[0], DESC_Y, 0], [c5[0], DESC_Y, 0], buff=0, stroke_width=5, color=BLUE,
                           tip_length=0.25, max_tip_length_to_length_ratio=0.05)
        desc_label = T("descending", size=36, color=BLUE).next_to(desc_arrow, UP, buff=0.2)
        int_list = Mono("int list", size=44, color=GREEN).move_to(UP * INTS_Y)
        away = T("one arrow away", size=30, color=YELLOW).next_to(till[1], RIGHT, buff=0.22)
        pennies = VGroup(*[Circle(radius=0.12).set_stroke(DIM, 2).set_fill(DIM, 0.2) for _ in range(43)])
        pennies.arrange(RIGHT, buff=0.05).move_to(UP * PENNY_Y)
        strike = Line(pennies.get_left() + LEFT * 0.2, pennies.get_right() + RIGHT * 0.2).set_stroke(RED, 6)
        self.extras = [desc_arrow, desc_label, int_list, away, pennies, strike]

        with self.say("c4.idea.1") as c:
            for m in coins:
                m.set_z_index(2)
            run = min(2.0, c.until("desc"))
            self.play(*[Transform(m, lab) for m, lab in zip(coins, labels)],
                      time_span(FadeIn(chain), 0.2, 0.75 * run),
                      time_span(FadeIn(till, shift=0.3 * DOWN), 0.55 * run, run),
                      run_time=run)
            for m, cell in zip(coins, chain.cells):     # the moved coins are the cells' coins now
                self.remove(m)
                m.set_z_index(0)
                cell.label = m
                cell.add(m)

            c.wait_until("desc")
            self.play(FadeIn(desc_label, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("fifty")
            run = c.until("one") + 0.5
            self.play(GrowArrow(desc_arrow, rate_func=linear),
                      LaggedStart(*[ring_flash(cell.label, GOLD) for cell in chain.cells], lag_ratio=0.9),
                      run_time=run)

            c.wait_until("so the till")
            self.play(FadeIn(int_list, shift=0.3 * UP), run_time=1.0)

            c.wait_until("head")
            self.play(FlashUnder(desc_label, color=YELLOW, run_time=1.2))
            c.wait_until("the head of a list")
            cell0 = chain.cells[0]
            self.play(cell0.box.animate.set_stroke(YELLOW, 4), cell0.ptr.animate.set_stroke(YELLOW, 4),
                      FlashAround(cell0, color=YELLOW, run_time=1.3), run_time=1.3)
            c.wait_until("one arrow away")
            line = Line(till[0].get_bottom(), cell0.box.get_top())
            self.play(FadeIn(away, shift=0.25 * LEFT),
                      VShowPassingFlash(line.set_stroke(YELLOW, 8), time_width=0.6, run_time=1.0),
                      run_time=1.0)

            c.wait_until("big")
            self.play(ring_flash(cell0.label, YELLOW, run_time=1.3))

            c.wait_until("hand over")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pennies], lag_ratio=0.08),
                      run_time=min(1.5, max(0.6, c.until("pennies"))))
            c.wait_until("pennies")
            self.play(Create(strike), run_time=min(0.6, max(0.3, c.remaining - 0.05)))

    # ── c4.idea.2: three observations ─────────────────────────────────────────────
    def observations(self):
        chain, till = self.chain, self.till
        cards = obs_cards().scale(CARD_BIG)
        cards.move_to(UP * (CARDS_TOP - cards.height / 2))
        self.cards = cards
        k1, k2, k3 = cards

        with self.say("c4.idea.2") as c:
            chain.generate_target()
            chain.target.shift(UP * (CY2 - CY1))
            chain.target.cells[0].box.set_stroke(BLUE, 3)
            chain.target.cells[0].ptr.set_stroke(BLUE, 3)
            self.play(FadeOut(*self.extras), MoveToTarget(chain), till.animate.shift(UP * (CY2 - CY1)),
                      run_time=1.5)

            c.wait_until("zero")
            self.play(FadeIn(k1.frame), FadeIn(k1.num, shift=0.3 * DOWN), FadeIn(k1.lines[0], shift=0.3 * DOWN),
                      run_time=1.0)
            c.wait_until("empty list")
            self.play(FadeIn(k1.nil, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("try")
            self.play(FadeIn(k2.frame), FadeIn(k2.num, shift=0.3 * DOWN), FadeIn(k2.lines[0], shift=0.3 * DOWN),
                      run_time=1.0)
            c.wait_until("small enough")
            self.play(FadeIn(k2.lines[1], shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("skip")
            self.play(FadeIn(k3.frame), FadeIn(k3.num, shift=0.3 * DOWN), FadeIn(k3.lines[0], shift=0.3 * DOWN),
                      run_time=1.0)
            settle(self, cards)

    # ── c4.idea.3: try them on 43 ────────────────────────────────────────────────
    def try43(self):
        chain, till, cards = self.chain, self.till, self.cards
        k1, k2, k3 = cards
        cell0, cell1 = chain.cells[0], chain.cells[1]

        amt_label = T("amount", size=30, color=DIM)
        amt_label.move_to([ROW_X, AMT_Y, 0], aligned_edge=LEFT)
        amt = T("43", size=56, color=GOLD).next_to(amt_label, RIGHT, buff=0.45)
        amt23 = T("23", size=56, color=GOLD).move_to(amt)
        chg_label = T("change", size=30, color=DIM)
        chg_label.move_to([ROW_X, CHG_Y, 0], aligned_edge=LEFT)
        ans = coin(20).next_to(chg_label, RIGHT, buff=0.45)
        ring = Circle(radius=cell1.label.width / 2 + 0.12).move_to(cell1.label).set_stroke(YELLOW, 5)
        still = T("still in the till", size=30, color=YELLOW).next_to(cell1, DOWN, buff=0.25)

        with self.say("c4.idea.3") as c:
            cards.generate_target()
            cards.target.scale(1 / CARD_BIG).to_edge(RIGHT, buff=0.55)
            cards.target.set_y(CARDS_TOP - cards.target.height / 2)
            self.play(MoveToTarget(cards), FadeIn(amt_label, shift=0.3 * DOWN), FadeIn(amt, shift=0.3 * DOWN),
                      run_time=1.5)

            c.wait_until("fifty")
            self.play(FlashAround(k3.frame, color=YELLOW, run_time=1.2),
                      cell0.box.animate.set_stroke(RED, 4), cell0.ptr.animate.set_stroke(RED, 4), run_time=1.0)
            c.wait_until("so it goes")
            arrow0 = chain.arrows[0]
            chain.remove(cell0, arrow0)          # the 50 leaves the till for good
            self.add(cell0, arrow0)
            self.play(FadeOut(cell0, arrow0, shift=0.9 * LEFT), till.animate.shift(RIGHT * PITCH),
                      run_time=min(1.5, max(0.8, c.until("twenty") - 0.1)))

            c.wait_until("twenty")
            self.play(FlashAround(k2.frame, color=YELLOW, run_time=1.2), ring_flash(cell1.label, GREEN, 1.0),
                      run_time=1.0)
            c.wait_until("use it")
            self.play(TransformFromCopy(cell1.label, ans, path_arc=-0.6), FadeIn(chg_label, shift=0.3 * DOWN),
                      run_time=1.3)
            c.wait_until("is left")
            self.play(ReplacementTransform(amt, amt23), run_time=0.9)

            c.wait_until("again")
            self.play(Create(ring), FadeIn(still, shift=0.25 * UP), run_time=0.9)

            c.wait_until("each")
            self.play(LaggedStart(*[FlashAround(k.frame, color=YELLOW) for k in cards], lag_ratio=0.35),
                      run_time=1.6)
            c.wait_until("program")
            sweep_clear(self, keep=[cards], run_time=min(1.0, max(0.5, c.remaining - 0.05)))
