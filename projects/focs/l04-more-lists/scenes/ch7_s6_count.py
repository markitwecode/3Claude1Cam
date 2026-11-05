"""Chapter 7, scene 6: Exercise 4.5, counting the ways. Clips c7.count.1 – c7.count.5.

PLAN
Opening as s2–s7: ch6's pill strip fades in (4.1–4.4 DONE, 4.5 CURRENT, 4.6 TODO); card 4.5
grows out of its pill (ch6_s6's rows: "Two coin values." / "Show there are O(n) ways ..." / the
[5][2][2] = [2][5][2] "count as one" picture / "Three values?  Four?  …"), pause tag top right.
The strip stays as the header (y 3.2) for the whole scene; content lives below y 2.7.
- count.1 the card, row by row on its words; {stop}: pause tag.
- count.2 {ignore}: the card shrinks into its pill but its coin picture stays and grows to the
  centre; each order flashes coin by coin as it is read; "A way is": both rows merge into one
  [5] [2][2] "one 5, two 2s". {small}: header band [5] [2] amount 20 born from it. {k}: five rows,
  0–4 five-pence discs out of the header 5; {rest}: what's left (GOLD, out of the 20) as a box
  0.336 per penny, 2p discs out of the header 2 pack it; {check}: each left amount flashes on its
  word, GREEN ✓ for 20/10/0, RED ✗ and a RED one-penny gap for 15/5; {three}: the ✓ rows' discs
  fly into ch5's reply (`change [5; 2] 20`, one inner list per line), brace + GOLD "3 ways".
- count.3 {general}: coins a, b (YELLOW symbols), "a > b" (the reply still up); {fix} the reply
  steps down, dimmed, under "number of a's: 0, 1, …, n/a"; {once} it leaves for "the rest: all
  b's, 1 way or none"; {bound} "ways ≤ n/a + 1" (n/a out of line 1), "= O(n)" on "big O of en".
- count.4 {three}: coin c joins the band, "c > a > b". {split}: the lines clear, "= O(n)" becomes
  "2 coins: O(n)", the top of a column on the right; a fan out of c, one branch per count 0, 1, 2, ⋮, n/c, each
  into a box "two-coin problem: O(n) ways"; {mult}: "O(n) choices × O(n) ways = O(n²)",
  O(n²) -> "3 coins: O(n²)"; {induct}: the fan dims, "4 coins: O(n³)", then "k coins: O(n^(k-1))".
- count.5 {table}: the board clears (the column stays a beat); the table: amounts 10 … 160 with
  ×2 between them; one row per beat, GOLD counts left to right, tags ≈ ×2: O(n), → ×4: O(n²),
  → ×8: O(n³); {uk}: the six-coin till as GOLD discs, "6 coins: O(n⁵)", "99p:  4366 ways".
Ends: everything (strip included) fades to an empty frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s1_hook import coin  # noqa: E402  ch1's GOLD coin disc
from scenes.ch6_s5_hints1 import (COL_X, CURRENT, DONE, TODO, HeroCard, enter_card,  # noqa: E402
                                  finish, fit, hold_for, make_strip, pause_tag)

# ── card 4.5 (as ch6_s6_hints2 draws it) ─────────────────────────────────────────
STEP45 = 0.75
H45 = 0.46 + 5 * STEP45 + 0.46       # header, two rows, the coin picture, the last row
COIN_SMALL = 0.44

# ── count.2: the orders, the one way, the small case ───────────────────────────────
PIC_Y, PIC_R = -0.2, 0.6
BAND_Y = 2.05                        # header band under the strip
ROW_Y = (1.05, 0.12, -0.81, -1.74, -2.67)
DISC_R = 0.3
PENNY = 0.336                        # box length per penny: a 2p disc spans two
K_X = -6.1                           # how many fives (DIM)
FIVE_L = -5.55                       # first five-pence disc's left edge
FIVE_STEP = 0.68
REST_R = -1.75                       # what's left (GOLD), right-aligned here
BOX_L = -1.45
MARK_X = 5.95
CALL = "change [5; 2] 20"
REPLY = ("- : int list list =\n"
         "[[5; 5; 5; 5];\n"
         " [5; 5; 2; 2; 2; 2; 2];\n"
         " [2; 2; 2; 2; 2; 2; 2; 2; 2; 2]]")
OUT_L, CALL_Y = -5.0, 1.05
OUT_DROP = 1.05                      # {fix}: the reply steps down and back under line 1

# ── count.3 / count.4: the general argument ────────────────────────────────────────
LX = -3.6
L_Y = (0.75, -0.45, -1.9)
ROOT = (-5.85, -0.45)
FAN_Y = (1.15, 0.3, -0.55, -2.05)    # branch ends; ⋮ at -1.3
BOX4_L = -3.3
COL4_L = 2.45

# ── count.5: the table ─────────────────────────────────────────────────────────────
TAB_L = -6.3
NUM_X = (-2.15, -0.85, 0.45, 1.75, 3.05)
TAG_L = 3.95
HDR_Y, X2_Y, RULE_Y = 1.85, 2.4, 1.38
TROW_Y = (0.85, -0.05, -0.95)
AMOUNTS = (10, 20, 40, 80, 160)
TABLE = (("[5; 2]", (2, 3, 5, 9, 17), r"\approx\ \times 2", "O(n)"),
         ("[5; 2; 1]", (10, 29, 97, 353, 1345), r"\to\ \times 4", "O(n^2)"),
         ("[10; 5; 2; 1]", (11, 40, 195, 1173, 8041), r"\to\ \times 8", "O(n^3)"))
TABLE_CUES = (("two", "linearly"), ("threec", "four times"), ("four", "eight times"))
TILL = (50, 20, 10, 5, 2, 1)
UK_Y, P99_Y = -2.2, -3.2


def coin_row(values, r=COIN_SMALL, buff=0.14):
    return VGroup(*[coin(v, r=r) for v in values]).arrange(RIGHT, buff=buff)


def sym_coin(sym, r):
    """ch1's GOLD disc with a YELLOW symbol (a, b, c) instead of a value."""
    disc = coin(1, r=r)[0]
    return VGroup(disc, MathTex(sym, font_size=int(120 * r), color=YELLOW).move_to(disc))


def dim_to(m, f):
    """Transform m to f times its own opacities (coins keep their faint fill)."""
    t = m.copy()
    for s in t.get_family():
        if isinstance(s, VMobject):
            s.set_fill(opacity=s.get_fill_opacity() * f, family=False)
            s.set_stroke(opacity=s.get_stroke_opacity() * f, family=False)
    return Transform(m, t)


def gold_parts(tex, *idx):
    for i in idx:
        tex[i].set_color(GOLD)
    return tex


class CountingTheWays(NarratedScene):
    def construct(self):
        self.statement()
        self.small_case()
        self.general()
        self.three_coins()
        self.table()
        finish(self)

    # ── c7.count.1: card 4.5 ────────────────────────────────────────────────────────
    def statement(self):
        strip = self.strip = make_strip([DONE] * 4 + [CURRENT, TODO])
        card = self.card = HeroCard(4, H45, step=STEP45)
        r0 = card.at_row(T("Two coin values.", size=36), 1)
        r1 = card.at_row(T("Show there are O(n) ways to make change for n.", size=36,
                           t2c={"O(n)": GOLD}), 2)
        a, b = coin_row([5, 2, 2]), coin_row([2, 5, 2])
        eq = MathTex("=", font_size=60, color=FG)
        one = T("count as one", size=32)
        pic = VGroup(a, eq, b, one).arrange(RIGHT, buff=0.55)
        pic.move_to([COL_X + 0.6, card.row_y(3.5), 0], aligned_edge=LEFT)
        one.shift(0.25 * RIGHT)
        r3 = card.at_row(T("Three values?  Four?  …", size=36), 5)
        card.lower(r0, r1, pic, r3)
        ptag = pause_tag()
        self.pic = (a, b, eq, one, ptag)

        with self.say("c7.count.1") as c:
            # {card} "Exercise four point five."
            self.play(FadeIn(strip, lag_ratio=0.15), run_time=0.8)
            self.play(*enter_card(strip, card, light=False), run_time=1.2)
            # "Take two coin values, and an amount to make, called en."
            c.wait_until("Take two")
            self.play(FadeIn(r0, shift=0.2 * DOWN), run_time=1.0)
            # "Ignoring order, ..."
            c.wait_until("Ignoring order")
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in a], lag_ratio=0.25), run_time=0.9)
            self.play(TransformFromCopy(a[0], b[1], path_arc=-PI / 2),
                      TransformFromCopy(a[1], b[0], path_arc=-PI / 2),
                      TransformFromCopy(a[2], b[2]),
                      time_span(GrowFromCenter(eq), 0.7, 1.4),
                      time_span(FadeIn(one, shift=0.2 * LEFT), 0.8, 1.4), run_time=1.4)
            # "... show that the number of ways to do it is big O of en."
            c.wait_until("number of ways")
            self.play(FadeIn(r1, shift=0.2 * DOWN), run_time=1.0)
            # "What about three or more coin values?"
            c.wait_until("What about")
            self.play(FadeIn(r3, shift=0.2 * DOWN), run_time=1.0)
            # {stop} "Pause, and try a small case first."
            c.wait_until("stop")
            self.play(FadeIn(ptag, shift=0.2 * DOWN), run_time=0.8)
        card.keep(r0, r1, r3)

    # ── c7.count.2: one way = how many of each coin; fives and twos making 20 ─────────
    def small_case(self):
        strip, card = self.strip, self.card
        a, b, eq, one, ptag = self.pic
        big_a = coin_row([5, 2, 2], r=PIC_R, buff=0.2)
        big_b = coin_row([2, 5, 2], r=PIC_R, buff=0.2)
        big_eq = MathTex("=", font_size=80, color=FG)
        VGroup(big_a, big_eq, big_b).arrange(RIGHT, buff=0.8).move_to([0, PIC_Y, 0])

        m5, m2a, m2b = coin(5, r=PIC_R), coin(2, r=PIC_R), coin(2, r=PIC_R)
        twos = VGroup(m2a, m2b).arrange(RIGHT, buff=0.2)
        VGroup(m5, twos).arrange(RIGHT, buff=0.75).move_to([0, PIC_Y, 0])
        way = T("one 5, two 2s", size=40, t2c={"5": GOLD, "2": GOLD})
        way.next_to(VGroup(m5, twos), DOWN, buff=0.55)

        h5, h2 = coin(5), coin(2)
        amount = T("amount", size=38, color=DIM)
        n20 = T("20", size=52, color=GOLD)
        VGroup(h5, h2).arrange(RIGHT, buff=0.25)
        amount.next_to(h2, RIGHT, buff=0.8)
        n20.next_to(amount, RIGHT, buff=0.22).align_to(amount, DOWN)
        VGroup(h5, h2, amount, n20).move_to([0, BAND_Y, 0])

        # the five rows: k fives, what's left, the 2p discs packing it, ✓ / ✗
        counts, fives, rests, boxes, twos_r, gaps, marks = [], [], [], [], [], [], []
        for k, y in enumerate(ROW_Y):
            left = 20 - 5 * k
            counts.append(T(str(k), size=34, color=DIM).move_to([K_X, y, 0]))
            fives.append([coin(5, r=DISC_R).move_to([FIVE_L + DISC_R + FIVE_STEP * j, y, 0])
                          for j in range(k)])
            rests.append(T(str(left), size=40, color=GOLD).move_to([REST_R, y, 0], aligned_edge=RIGHT))
            if left:
                bx = RoundedRectangle(corner_radius=0.06, width=left * PENNY, height=0.72)
                bx.set_stroke(DIM, 2).set_fill(opacity=0).move_to([BOX_L, y, 0], aligned_edge=LEFT)
                boxes.append(bx)
            twos_r.append([coin(2, r=DISC_R).move_to([BOX_L + PENNY * (1 + 2 * j), y, 0])
                           for j in range(left // 2)])
            if left % 2:
                g = Rectangle(width=PENNY - 0.04, height=0.6).set_stroke(width=0).set_fill(RED, 0.75)
                gaps.append(g.move_to([BOX_L + PENNY * (left - 0.5), y, 0]))
            mark = check_mark(GREEN) if left % 2 == 0 else cross_mark(RED)
            marks.append(mark.move_to([MARK_X, y, 0]))
        checks = [marks[k] for k in (0, 2, 4)]

        with self.say("c7.count.2") as c:
            # {ignore} the card goes home; its picture stays and grows
            # (as ch7_s2: contents fade, the frame shrinks onto pill 4.5, which stays CURRENT)
            self.play(*[FadeOut(m) for m in (*card.shown, one)],
                      Transform(card.frame, strip[4].frame.copy()),
                      *[Transform(m, t) for m, t in zip([*a, *b, eq], [*big_a, *big_b, big_eq])],
                      run_time=1.5)
            self.remove(card.frame)
            # "... five, then two, then two, ..."
            c.wait_until("five then two")
            self.play(LaggedStart(*[FlashAround(m, color=YELLOW, time_width=1.0) for m in a],
                                  lag_ratio=0.45), FadeOut(ptag),       # the pause is over
                      run_time=fit(c, "two then five", 0.85, 1.0, 1.8))
            # "... is the same way as two, then five, then two."
            c.wait_until("two then five")
            self.play(LaggedStart(*[FlashAround(m, color=YELLOW, time_width=1.0) for m in b],
                                  lag_ratio=0.45), run_time=fit(c, "A way is", 0.85, 1.0, 1.8))
            # "A way is just how many of each coin it uses."
            c.wait_until("A way is")
            self.play(Transform(a[0], m5), Transform(a[1], m2a), Transform(a[2], m2b),
                      FadeOut(b[1], target_position=m5.get_center()),
                      FadeOut(b[0], target_position=m2a.get_center()),
                      FadeOut(b[2], target_position=m2b.get_center()),
                      FadeOut(eq), time_span(FadeIn(way, shift=0.3 * DOWN), 1.0, 1.8),
                      run_time=1.8)

            # {small} "Here's an example: fives and twos, making twenty."
            c.wait_until("small")
            self.play(TransformFromCopy(a[0], h5), TransformFromCopy(a[1], h2), run_time=1.2)
            c.wait_until("making twenty")
            self.play(FadeIn(amount, shift=0.2 * DOWN), FadeIn(n20, shift=0.2 * DOWN), run_time=0.9)

            # {k} "There can be zero to four fives."
            c.wait_until("k")
            all5 = [d for row in fives for d in row]
            self.play(*[FadeOut(m) for m in (*a, way)],
                      LaggedStart(*[FadeIn(m, shift=0.2 * RIGHT) for m in counts], lag_ratio=0.15),
                      LaggedStart(*[TransformFromCopy(h5, d) for d in all5], lag_ratio=0.12),
                      run_time=2.0)

            # {rest} "Whatever is left must be made of twos, ..."
            c.wait_until("rest")
            self.play(LaggedStart(*[TransformFromCopy(n20, r) for r in rests], lag_ratio=0.15),
                      LaggedStart(*[GrowFromEdge(bx, LEFT) for bx in boxes], lag_ratio=0.15),
                      run_time=1.6)
            c.wait_until("made of twos")
            all2 = [d for row in twos_r for d in row]
            self.play(LaggedStart(*[TransformFromCopy(h2, d) for d in all2], lag_ratio=0.07),
                      run_time=2.4)

            # {check} "What's left is twenty, fifteen, ten, five or zero, ..."
            c.wait_until("check")
            offs = [c.until(w, floor=0.0) for w in
                    ("twenty fifteen", "fifteen ten", "ten five", "five or", "or zero")]
            self.play(*[time_span(FlashAround(r, color=GOLD, time_width=1.0), t, t + 0.8)
                        for t, r in zip(offs, rests)], run_time=offs[-1] + 0.8)
            # "... and only the even amounts work."
            c.wait_until("only the even")
            self.play(*[Create(m) for m in marks], *[FadeIn(g) for g in gaps],
                      *[r.animate.set_color(RED) for k, r in enumerate(rests) if k % 2],
                      run_time=1.2)

            # {three} "So there are three ways, as change finds."
            # The ✓ rows' coins fly into ch5's reply, one inner list per row; the header into the call.
            c.wait_until("three")
            call = Code(CALL, size=34).move_to([OUT_L, CALL_Y, 0], aligned_edge=LEFT)
            reply = Code(REPLY, size=32)
            reply.next_to(call, DOWN, buff=0.32, aligned_edge=LEFT)
            lists = VGroup(*[g.copy() for i in (1, 2, 3) for g in reply.line(i)])
            brace = Brace(lists, RIGHT, buff=0.25, color=GOLD)
            ways = T("3 ways", size=44, color=GOLD).next_to(brace, RIGHT, buff=0.3)
            flies, landed, used = [], [], set()

            def fly(src, glyphs):
                tgt = VGroup(*[g.copy() for g in glyphs])
                used.update(id(g) for g in glyphs)
                landed.append(tgt)
                flies.append(ReplacementTransform(src, tgt))

            for j, d in enumerate(fives[4]):
                fly(d, reply.find("5", line=1, nth=j))
            for j, d in enumerate(fives[2]):
                fly(d, reply.find("5", line=2, nth=j))
            for j, d in enumerate(twos_r[2]):
                fly(d, reply.find("2", line=2, nth=j))
            for j, d in enumerate(twos_r[0]):
                fly(d, reply.find("2", line=3, nth=j))
            fly(h5, call.find("5"))
            fly(h2, call.find("2"))
            fly(n20, call.find("20"))
            rest_glyphs = [g.copy() for g in (*call.line(0), *[g for i in range(4) for g in reply.line(i)])
                           if id(g) not in used]
            gone = [*counts, *rests, *boxes, *gaps, *[marks[k] for k in (1, 3)], amount,
                    *fives[1], *fives[3], *twos_r[1], *twos_r[3]]
            self.play(*[time_span(FadeOut(m), 0.0, 0.7) for m in gone],
                      *[time_span(FadeOut(m), 0.8, 1.4) for m in checks],
                      *[time_span(f, 0.3, 2.0) for f in flies],
                      *[time_span(FadeIn(g), 0.9, 1.8) for g in rest_glyphs],
                      time_span(GrowFromCenter(brace), 1.4, 2.2),
                      time_span(FadeIn(ways, shift=0.2 * LEFT), 1.5, 2.2),
                      run_time=2.2)
            self.remove(*landed, *rest_glyphs)
            self.add(call, reply)
        self.out = (call, reply, brace, ways)

    # ── c7.count.3: two coins in general ─────────────────────────────────────────────
    def general(self):
        a, b = sym_coin("a", 0.5), sym_coin("b", 0.36)
        rel = MathTex("a", ">", "b", font_size=52)
        rel[0].set_color(YELLOW)
        rel[2].set_color(YELLOW)
        amt = T("amount", size=38, color=DIM)
        nn = T("n", size=52, color=GOLD, slant=ITALIC)
        VGroup(a, b).arrange(RIGHT, buff=0.3)
        rel.next_to(b, RIGHT, buff=0.8)
        amt.next_to(rel, RIGHT, buff=1.0)
        nn.next_to(amt, RIGHT, buff=0.2).align_to(amt, DOWN)
        VGroup(a, b, rel, amt, nn).move_to([0, BAND_Y, 0])
        self.band = [a, b, rel, amt, nn]

        l1 = MathTex(r"\text{number of }", "a", r"\text{'s:}\quad 0,\ 1,\ \dots,\ ", "n", "/", "a",
                     font_size=52)
        l1[1].set_color(YELLOW)
        l1[5].set_color(YELLOW)
        l2 = MathTex(r"\text{the rest: all }", "b", r"\text{'s, 1 way or none}", font_size=52)
        l2[1].set_color(YELLOW)
        l3 = MathTex(r"\text{ways}", r"\;\le\;", "n", "/", "a", r"\;+\;1", r"\;=\;O(n)",
                     font_size=60)
        l3[4].set_color(YELLOW)
        l3[6][1:].set_color(GOLD)          # "= O(n)" is one part: it travels into the column
        for line, y in zip((l1, l2, l3), L_Y):
            line.move_to([LX, y, 0], aligned_edge=LEFT)
        self.lines = (l1, l2, l3)

        with self.say("c7.count.3") as c:
            # {general} "In general, take two coins, a big one and a small one."
            c.wait_until("take two coins")
            self.play(GrowFromCenter(a), time_span(GrowFromCenter(b), 0.3, 1.1), run_time=1.1)
            c.wait_until("a big one")
            self.play(FadeIn(rel, shift=0.2 * DOWN), FlashAround(a, color=YELLOW, time_width=1.0),
                      time_span(FlashAround(b, color=YELLOW, time_width=1.0), 0.5, 1.3), run_time=1.3)

            # {fix} "A way is fixed by how many big coins it uses, ... zero to the amount divided by the big coin."
            # (ch5's reply steps down and back, under line 1, until line 2 needs the room)
            c.wait_until("fix")
            self.play(*[restyle(m, op=0.4, shift=OUT_DROP * DOWN) for m in self.out],
                      time_span(FadeIn(l1, shift=0.2 * DOWN), 0.5, 1.5),
                      time_span(FadeIn(amt), 0.5, 1.5), time_span(FadeIn(nn), 0.5, 1.5), run_time=1.5)

            # {once} "The rest must be all small coins, so each count gives one way, or none."
            c.wait_until("once")
            self.play(*[time_span(FadeOut(m), 0.0, 0.7) for m in self.out],
                      time_span(FadeIn(l2, shift=0.2 * DOWN), 0.5, 1.4),
                      time_span(FlashAround(b, color=YELLOW, time_width=1.0), 0.5, 1.4), run_time=1.4)

            # {bound} "So the number of ways is at most one more than en divided by the big coin."
            c.wait_until("bound")
            self.play(*[TransformFromCopy(l1[i], l3[j]) for i, j in ((3, 2), (4, 3), (5, 4))],
                      time_span(FadeIn(l3[0]), 0.4, 1.5), time_span(FadeIn(l3[1]), 0.4, 1.5),
                      time_span(FadeIn(l3[5]), 0.6, 1.6), run_time=1.6)
            # "That's big O of en."
            c.wait_until("That's big O")
            self.play(FadeIn(l3[6], shift=0.2 * LEFT),
                      time_span(FlashAround(l3[6][1:].copy(), color=GOLD, time_width=1.5), 0.4, 1.4),
                      run_time=1.4)

    # ── c7.count.4: three coins and more ─────────────────────────────────────────────
    def three_coins(self):
        a, b, rel, amt, nn = self.band
        l1, l2, l3 = self.lines
        cc = sym_coin("c", 0.58)
        rel2 = MathTex("c", ">", "a", ">", "b", font_size=52)
        for i in (0, 2, 4):
            rel2[i].set_color(YELLOW)
        band2 = VGroup(cc, a.copy(), b.copy(), rel2, amt.copy(), nn.copy())
        band2[:3].arrange(RIGHT, buff=0.3)
        rel2.next_to(band2[2], RIGHT, buff=0.8)
        band2[4].next_to(rel2, RIGHT, buff=1.0)
        band2[5].next_to(band2[4], RIGHT, buff=0.2).align_to(band2[4], DOWN)
        band2.move_to([0, BAND_Y, 0])

        col = [gold_parts(MathTex(rf"{k}\text{{ coins: }}", o, font_size=40), 1)
               for k, o in (("2", "O(n)"), ("3", "O(n^2)"), ("4", "O(n^3)"), ("k", "O(n^{k-1})"))]
        for m, y in zip(col, FAN_Y):
            m.move_to([COL4_L, y, 0], aligned_edge=LEFT)
        col_dots = MathTex(r"\vdots", font_size=40).move_to([COL4_L + 0.25, -1.3, 0])

        root = sym_coin("c", 0.5).move_to([*ROOT, 0])
        labels = [MathTex("0", font_size=40), MathTex("1", font_size=40), MathTex("2", font_size=40),
                  MathTex("n", "/", "c", font_size=40)]
        labels[3][2].set_color(YELLOW)
        lab_x = BOX4_L - 0.45
        for m, y in zip(labels, FAN_Y):
            m.move_to([lab_x, y, 0])
        ends = [np.array([lab_x - 0.45, y, 0]) for y in FAN_Y]
        rc = root.get_center()
        branches = [Line(rc + 0.58 * normalize(e - rc), e).set_stroke(FG, 3) for e in ends]
        fan_dots = [MathTex(r"\vdots", font_size=40).move_to([lab_x, -1.3, 0])]
        boxes = []
        for y in FAN_Y:
            t = T("two-coin problem: O(n) ways", size=28, t2c={"O(n)": GOLD})
            bx = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=0.62)
            bx.set_stroke(BLUE, 2).set_fill(BLUE, 0.08)
            VGroup(bx, t).move_to([BOX4_L, y, 0], aligned_edge=LEFT)
            t.move_to(bx)
            boxes.append(VGroup(bx, t))
        fan_dots.append(MathTex(r"\vdots", font_size=40).move_to([boxes[0].get_center()[0], -1.3, 0]))

        mult = MathTex("O(n)", r"\text{ choices}", r"\;\times\;", "O(n)", r"\text{ ways}", r"\;=\;",
                       "O(n^2)", font_size=44)
        gold_parts(mult, 0, 3, 6)
        mult.move_to([(ROOT[0] - 0.5 + boxes[0].get_right()[0]) / 2, -3.15, 0])

        with self.say("c7.count.4") as c:
            # {three} "Now add a third coin."
            c.wait_until("three")
            self.play(*[m.animate.move_to(t) for m, t in zip((a, b, amt, nn), band2[1:3].submobjects
                                                             + band2[4:].submobjects)],
                      ReplacementTransform(rel, rel2),
                      time_span(GrowFromCenter(cc), 0.4, 1.4), run_time=1.4)

            # {split} "Fix how many of the largest coin you use."  The two-coin result becomes the
            # top of a column; the fan grows out of c.
            c.wait_until("split")
            self.play(*[time_span(FadeOut(m), 0.0, 0.7) for m in (l1, l2, *l3[:6])],
                      ReplacementTransform(l3[6], col[0][1]),
                      time_span(FadeIn(col[0][0], shift=0.2 * LEFT), 0.4, 1.1), run_time=1.1)
            self.play(TransformFromCopy(cc, root),
                      time_span(LaggedStart(*[Create(br) for br in branches], lag_ratio=0.2), 0.6, 1.8),
                      time_span(LaggedStart(*[FadeIn(m) for m in (*labels[:3], fan_dots[0], labels[3])],
                                            lag_ratio=0.2), 0.9, 2.0), run_time=2.0)
            # "What's left is a two-coin problem, with big O of en ways."
            c.wait_until("What's left")
            self.play(LaggedStart(*[FadeIn(bx, shift=0.2 * RIGHT) for bx in boxes], lag_ratio=0.2),
                      time_span(FadeIn(fan_dots[1]), 0.6, 1.4),
                      time_span(FlashAround(col[0][1], color=GOLD, time_width=1.5), 0.8, 1.8), run_time=1.8)

            # {mult} "And there are big O of en choices for the largest coin, ..."
            c.wait_until("mult")
            self.play(FadeIn(mult[0]), FadeIn(mult[1]),
                      *[time_span(FlashAround(m, color=YELLOW, time_width=1.0), 0.2 + 0.15 * i, 1.0 + 0.15 * i)
                        for i, m in enumerate(labels)], run_time=1.5)
            # "... so there are big O of en squared ways altogether."
            c.wait_until("so there are")
            self.play(FadeIn(mult[2]), FadeIn(mult[3]), FadeIn(mult[4]),
                      *[time_span(FlashAround(bx, color=GOLD, time_width=1.0), 0.2 + 0.15 * i, 1.0 + 0.15 * i)
                        for i, bx in enumerate(boxes)], run_time=1.5)
            c.wait_until("squared")
            self.play(FadeIn(mult[5]), FadeIn(mult[6], shift=0.2 * LEFT), run_time=0.9)
            self.play(TransformFromCopy(mult[6], col[1][1]), FadeIn(col[1][0], shift=0.2 * LEFT),
                      run_time=1.3)

            # {induct} "Each extra coin brings one more factor of en."
            c.wait_until("induct")
            fan = [root, *branches, *labels, *fan_dots, *boxes, *mult, cc, a, b, rel2, amt, nn]
            self.play(*[dim_to(m, 0.3) for m in fan], run_time=0.8)
            self.play(TransformFromCopy(col[1], col[2]), run_time=1.3)
            # "So the power is one less than the number of coins."
            c.wait_until("So the power")
            self.play(FadeIn(col_dots), TransformFromCopy(col[2], col[3]), run_time=1.4)
            self.play(FlashAround(col[3][1], color=GOLD, time_width=1.5), run_time=1.2)
        self.col = [col[0][0], col[0][1], col[1][0], col[1][1], col[2], col_dots, col[3]]

    # ── c7.count.5: real counts ────────────────────────────────────────────────────
    def table(self):
        hdr_lab = T("amount", size=32, color=DIM).move_to([TAB_L, HDR_Y, 0], aligned_edge=LEFT)
        hdr = [T(str(n), size=40).move_to([x, HDR_Y, 0]) for n, x in zip(AMOUNTS, NUM_X)]
        x2 = [T("×2", size=28, color=DIM).move_to([(NUM_X[i] + NUM_X[i + 1]) / 2, X2_Y, 0])
              for i in range(4)]
        rule = Line([TAB_L, RULE_Y, 0], [6.4, RULE_Y, 0]).set_stroke(DIM, 2)
        rows = []
        for (src, nums, ratio, big_o), y in zip(TABLE, TROW_Y):
            lab = Code(src, size=32).move_to([TAB_L, y, 0], aligned_edge=LEFT)
            cells = [T(str(v), size=40, color=GOLD).move_to([x, y, 0]) for v, x in zip(nums, NUM_X)]
            tag = gold_parts(MathTex(ratio, r"{:}\ ", big_o, font_size=40), 2)
            tag.move_to([TAG_L, y, 0], aligned_edge=LEFT)
            rows.append((lab, cells, tag))
        till = coin_row(TILL, r=0.42, buff=0.16).move_to([TAB_L, UK_Y, 0], aligned_edge=LEFT)
        six = gold_parts(MathTex(r"6\text{ coins: }", "O(n^5)", font_size=44), 1)
        six.move_to([0.3, UK_Y, 0], aligned_edge=LEFT)
        p99 = T("99p:  4366 ways", size=40, t2c={"4366": GOLD})
        p99.move_to([0.3, P99_Y, 0], aligned_edge=LEFT)

        with self.say("c7.count.5") as c:
            # {table} "Real counts agree."  (the column of powers stays a beat)
            sweep_clear(self, keep=[self.strip, *self.col], run_time=1.2)
            # "Watch each one as the amount doubles."
            c.wait_until("Watch each")
            self.play(FadeIn(hdr_lab), Create(rule),
                      LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in hdr], lag_ratio=0.25),
                      time_span(LaggedStart(*[FadeIn(m, shift=0.2 * RIGHT) for m in x2], lag_ratio=0.3),
                                0.6, 1.8), run_time=1.8)
            for k, ((lab, cells, tag), (cue, tag_cue)) in enumerate(zip(rows, TABLE_CUES)):
                c.wait_until(cue)
                extra = [time_span(FadeOut(m), 0.0, 0.8) for m in self.col] if k == 0 else []
                self.play(*extra, FadeIn(lab, shift=0.2 * RIGHT),
                          time_span(LaggedStart(*[FadeIn(m, shift=0.15 * DOWN) for m in cells],
                                                lag_ratio=0.35), 0.4, 2.0), run_time=2.0)
                c.wait_until(tag_cue)
                self.play(FadeIn(tag, shift=0.2 * LEFT), run_time=0.9)

            # {uk} "With all six coins, from fifty down to one, ..."
            c.wait_until("uk")
            self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in till], lag_ratio=0.3), run_time=2.0)
            # "... the count grows as big O of en to the fifth."
            c.wait_until("big O")
            self.play(FadeIn(six, shift=0.2 * LEFT), run_time=1.0)
            # "That's why ninety-nine pence already has four thousand, three hundred and sixty-six ways."
            c.wait_until("ninety-nine")
            n4366 = select(p99, "4366")[0]
            self.play(FadeIn(p99, shift=0.2 * DOWN),
                      time_span(FlashAround(n4366.copy(), color=GOLD, time_width=1.5), 0.6, 2.0),
                      run_time=2.0)
            born = self.time
        hold_for(self, born, 15)
