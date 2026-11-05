"""Chapter 4, scene 1: Hook. Last time's zip picture, then a till, 43p owed: which coins?
Greedy grabs the 20; this chapter turns that into a program; a till where it gets stuck.
Clips c4.hook.1 – c4.hook.2.

Layout:
hook.1  title card (shifted UP 0.8); ch3's general zip picture under it, small and DIM, zips on
        "zipped" and unzips on "unzipped". {till}: on "everyday life" a sweep; a DIM till tray (six compartments)
        centred at y 0.5; DIM "unlimited supply" under it on "endless supply"; the six coins (each
        with a short GOLD stack behind) drop in on their spoken values. {owe}: the till slides to
        x -2.6; GOLD "43p" at the right, YELLOW pill "change" over it on "change".
        {which}: YELLOW "?" between them.
hook.2  {grab}: YELLOW ring onto the 50, RED on "that fits", hops to the 20 (the "?" goes); a copy
        of the 20 drops below the till; "43p -> 23p". {program}: the coins' copies become Code
        [50; 20; 10; 5; 2; 1] at y -2.75; on "forty-three pence" a copy of 43p becomes a GOLD `43`
        beside it. {catch}: the grab clears, the stacks fade, the rest dims to 0.4; a small till (5, 2) at the right
        with GOLD "6p"; a RED "?" on "stuck".
End shot (s2 opens from it): six coin(v) discs 50 20 10 5 2 1 in one row, buff 0.28, centred at
ORIGIN (row 6.44 x 0.84), GOLD stroke 4, GOLD fill 0.15, GOLD serif values at 34; nothing else.
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

VALUES = [50, 20, 10, 5, 2, 1]
VALUE_CUES = ["fifty", "twenty", "ten", "five", "two and", "one pence"]

CARD_Y = 0.8                  # the title card's shift up
PIC_Y, PIC_W = -2.45, 8.6     # ch3's zip picture under the card (DIM)
TEX_SIZE = 54

TILL_ALONE = np.array([0.0, 0.5, 0])    # the till's coin-row centre while it is alone
TILL_AT = np.array([-2.6, 0.5, 0])      # ... from {owe} on
AMOUNT_X = 3.15                         # centre x of "43p"
DROP_DY = 2.0                           # the handed-over 20 sits this far under its coin
CODE_Y = -2.75
SMALL_AT = np.array([4.75, 0.5, 0])     # the second, smaller till ({catch})
SMALL_S = 0.8

COIN_R = 0.42                 # the coin disc reused by ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34
STACK_OFF = np.array([0.06, 0.08, 0])   # each disc of a stack sits this far up-right of the one in front


def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def dim_coin(k, op=0.4):
    """A coin at opacity op, its fill scaled with it (so it still reads as a disc)."""
    t = k.copy()
    t[0].set_stroke(opacity=op).set_fill(opacity=0.15 * op)
    t[1].set_opacity(op)
    return t


def pile_behind(k, s=1.0):
    """A short stack behind coin k: two opaque discs up-right of it, and a BG blocker under it
    so the stack doesn't show through the coin's translucent fill."""
    r = COIN_R * s
    tint = ManimColor(BG).interpolate(ManimColor(GOLD), 0.15)
    discs = []
    for n, op in ((2, 0.45), (1, 0.7)):
        d = Circle(radius=r).set_stroke(GOLD, 3 * s, opacity=op).set_fill(tint, opacity=1)
        discs.append(d.move_to(k[0].get_center() + n * s * STACK_OFF))
    blocker = Circle(radius=r).set_stroke(width=0).set_fill(BG, opacity=1).move_to(k[0])
    return VGroup(*discs, blocker)


class Till:
    """A row of coins with stacks behind, in a DIM tray with one compartment per coin."""

    def __init__(self, values, s=1.0, caption=None):
        self.coins = VGroup(*[coin(v, COIN_R * s) for v in values]).arrange(RIGHT, buff=0.28 * s)
        for k in self.coins:
            k[1].scale(s).move_to(k[0])
        self.piles = [pile_behind(k, s) for k in self.coins]
        body = VGroup(self.coins, *self.piles)
        pad = 0.24 * s
        self.tray = RoundedRectangle(corner_radius=0.18 * s, width=body.width + 2 * pad,
                                     height=body.height + 2 * pad).set_stroke(DIM, 2.5).move_to(body)
        top, bot = self.tray.get_top()[1], self.tray.get_bottom()[1]
        self.dividers = []
        for a, b in zip(self.coins[:-1], self.coins[1:]):
            x = (a.get_right()[0] + 2 * s * STACK_OFF[0] + b.get_left()[0]) / 2
            self.dividers.append(Line([x, top, 0], [x, bot, 0], stroke_width=2, color=DIM))
        self.units = [VGroup(p, k) for p, k in zip(self.piles, self.coins)]
        parts = [self.tray, *self.dividers]
        for p, k in zip(self.piles, self.coins):
            parts += [p, k]
        self.caption = None
        if caption:
            self.caption = T(caption, 32, DIM).next_to(self.tray, DOWN, buff=0.3)
            parts.append(self.caption)
        self.group = VGroup(*parts)

    def place(self, row_centre):
        self.group.shift(row_centre - self.coins.get_center())
        return self


def maps_arrow(start, end, color=FG):
    """A long mapsto (as in ch3): an arrow from start to end with a short bar across its tail."""
    arrow = Arrow(start, end, buff=0, stroke_width=5, color=color,
                  max_tip_length_to_length_ratio=0.14)
    tick = Line(start + 0.17 * UP, start + 0.17 * DOWN, stroke_width=5, color=color)
    return arrow, tick


def tag(text, color, size=36):
    """A small outlined pill with a word in it (ch2's tag)."""
    t = T(text, size=size, color=color)
    pill = RoundedRectangle(corner_radius=0.22, width=t.width + 0.55, height=t.height + 0.36,
                            stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.10)
    pill.move_to(t)
    return VGroup(pill, t)


class Ch4S1Hook(NarratedScene):
    def construct(self):
        self.build_picture()
        self.till = Till(VALUES, caption="unlimited supply").place(TILL_ALONE)
        with self.say("c4.hook.1") as c:
            self.last_time(c)
            self.the_till_opening(c)
            self.the_till(c)
        self.greedy()
        self.hand_off()

    # ── ch3's general picture, small and DIM ────────────────────────────────
    def build_picture(self):
        xs = MathTex("[", "x_1", ",", r"\ldots", ",", "x_n", "]", font_size=TEX_SIZE)
        ys = MathTex("[", "y_1", ",", r"\ldots", ",", "y_n", "]", font_size=TEX_SIZE)
        left = VGroup(xs, ys).arrange(DOWN, buff=0.45)
        brace = Brace(left, RIGHT, buff=0.2)
        tip = brace.get_tip()
        r_start = tip + RIGHT * 0.35 + UP * 0.3
        r_end = r_start + RIGHT * 2.3
        zarrow, ztick = maps_arrow(r_start, r_end)
        rp = MathTex("[(", "x_1", ",", "y_1", "),", r"\ldots", ",(", "x_n", ",", "y_n", ")]",
                     font_size=TEX_SIZE)
        rp.next_to(r_end, RIGHT, buff=0.35).set_y(tip[1])
        uarrow, utick = maps_arrow(np.array([r_end[0], tip[1] - 0.3, 0]),
                                   np.array([r_start[0], tip[1] - 0.3, 0]))
        zip_lab = Mono("zip", 44).next_to(zarrow, UP, buff=0.2)
        unzip_lab = Mono("unzip", 44).next_to(uarrow, DOWN, buff=0.2)
        pic = VGroup(left, brace, zarrow, ztick, rp, uarrow, utick, zip_lab, unzip_lab)
        pic.scale(PIC_W / pic.width).move_to(UP * PIC_Y).set_color(DIM)
        self.pic = pic
        self.xs, self.ys, self.rp, self.brace = xs, ys, rp, brace
        self.zip_parts = (zarrow, ztick, zip_lab)
        self.unzip_parts = (uarrow, utick, unzip_lab)

    # ── c4.hook.1, sentence 1: last time ────────────────────────────────────
    def last_time(self, c):
        xs, ys, rp = self.xs, self.ys, self.rp
        zarrow, ztick, zip_lab = self.zip_parts
        uarrow, utick, unzip_lab = self.unzip_parts
        card = title_card("Part 4 · Making change").shift(UP * CARD_Y)
        self.card = card
        self.play(
            time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.7),
            time_span(GrowFromCenter(card.rule), 0, 0.7),
            time_span(FadeIn(card.course, shift=0.25 * DOWN), 0.1, 0.8),
            time_span(FadeIn(card.part, shift=0.25 * DOWN), 0.2, 0.9),
            time_span(FadeIn(VGroup(xs, ys, self.brace), shift=0.2 * DOWN), 0.4, 1.1),
            run_time=1.1,
        )
        # zip: the x's and y's fly into the pairs
        c.wait_until("zipped")
        rt = min(1.8, 0.9 * c.until("unzipped"))
        u = rt / 1.8
        moved = [(xs[1], rp[1]), (ys[1], rp[3]), (xs[5], rp[7]), (ys[5], rp[9])]
        self.play(
            time_span(GrowArrow(zarrow), 0, 0.6 * u),
            time_span(FadeIn(ztick), 0, 0.5 * u),
            time_span(FadeIn(zip_lab, shift=0.2 * DOWN), 0.1, 0.7 * u),
            *[time_span(TransformFromCopy(a, b), 0.4 * u, 1.8 * u) for a, b in moved],
            *[time_span(FadeIn(rp[i]), 0.8 * u, 1.6 * u) for i in (0, 2, 4, 5, 6, 8, 10)],
            run_time=rt,
        )
        settle(self, rp)
        # unzip: they fly back
        c.wait_until("unzipped")
        rt = min(1.6, 0.9 * c.until("till"))
        u = rt / 1.6
        backs = [(rp[1], xs[1]), (rp[3], ys[1]), (rp[7], xs[5]), (rp[9], ys[5])]
        flyers = [a.copy() for a, _ in backs]
        self.play(
            time_span(GrowArrow(uarrow), 0, 0.6 * u),
            time_span(FadeIn(utick), 0, 0.5 * u),
            time_span(FadeIn(unzip_lab, shift=0.2 * UP), 0.1, 0.7 * u),
            *[time_span(Transform(f, b.copy()), 0.3 * u, 1.6 * u) for f, (_, b) in zip(flyers, backs)],
            run_time=rt,
        )
        self.remove(*flyers)

    # ── c4.hook.1, sentences 2-5: the till, 43p owed, which coins? ──────────
    def the_till_opening(self, c):
        till = self.till
        # {till} ... "everyday life": the recap clears as an empty DIM tray draws in
        c.wait_until("everyday life")
        sweep_clear(self, time_span(Create(till.tray), 0.4, 1.4),
                    *[time_span(Create(d), 0.8, 1.4) for d in till.dividers], run_time=1.4)
        # "endless supply": the caption; then each coin with its stack on its value
        c.wait_until("endless supply")
        self.play(FadeIn(till.caption, shift=0.25 * DOWN), run_time=min(1.0, 0.8 * c.until("fifty")))
        c.wait_until("fifty")
        offs = [c.until(w, floor=0.0) for w in VALUE_CUES]
        self.play(*[time_span(FadeIn(unit, shift=0.35 * DOWN), max(0, o - 0.1), o + 0.6)
                    for unit, o in zip(till.units, offs)],
                  run_time=offs[-1] + 0.6)
        settle(self, till.group)

    def the_till(self, c):
        till = self.till
        self.amount = T("43p", 64, GOLD).move_to([AMOUNT_X, TILL_AT[1], 0])
        self.change = tag("change", YELLOW).next_to(self.amount, UP, buff=0.4)
        self.ask = T("?", 80, YELLOW)
        gap_l = till.tray.get_right()[0] + (TILL_AT - TILL_ALONE)[0]
        self.ask.move_to([(gap_l + self.amount.get_left()[0]) / 2, TILL_AT[1], 0])
        # {owe}: the till moves over; the amount owed
        c.wait_until("owe")
        k = min(1.6, 0.9 * c.until("change"))
        self.play(
            time_span(till.group.animate.shift(TILL_AT - TILL_ALONE), 0, 0.75 * k),
            time_span(FadeIn(self.amount, shift=0.3 * LEFT), 0.45 * k, k),
            run_time=k,
        )
        c.wait_until("change")
        self.play(FadeIn(self.change, shift=0.3 * DOWN), run_time=min(1.0, 0.9 * c.until("which")))
        # {which}
        c.wait_until("which")
        self.play(FadeIn(self.ask, scale=0.6), run_time=1.0)

    # ── c4.hook.2: greedy; a program; a till that gets stuck ────────────────
    def greedy(self):
        till = self.till
        coins = till.coins
        ring = Circle(radius=COIN_R + 0.13).set_stroke(YELLOW, 6).move_to(coins[0])
        handed = coin(20).move_to(coins[1]).shift(DROP_DY * DOWN)
        arrow = Arrow(ORIGIN, RIGHT * 0.8, buff=0, stroke_width=5, color=FG,
                      max_tip_length_to_length_ratio=0.3)
        arrow.next_to(self.amount, RIGHT, buff=0.25)
        left = T("23p", 64, GOLD).next_to(arrow, RIGHT, buff=0.25)
        left.align_to(self.amount, DOWN)

        code = Code("[50; 20; 10; 5; 2; 1]", size=44)
        owed = Code("43", size=44)
        VGroup(code, owed).arrange(RIGHT, buff=0.9)
        code_dx = coins.get_x() + 0.6 - code.get_x()
        VGroup(code, owed).shift(code_dx * RIGHT).set_y(CODE_Y)
        nums = [code.find(str(v), nth=1 if v in (5, 2, 1) else 0) for v in VALUES]
        frame = [g for g in code.line(0) if all(g is not n for grp in nums for n in grp)]

        small = Till([5, 2], s=SMALL_S).place(SMALL_AT)
        six = T("6p", 56, GOLD).next_to(small.tray, DOWN, buff=0.45)
        stuck = T("?", 72, RED).next_to(six, RIGHT, buff=0.3)
        VGroup(six, stuck).set_x(small.tray.get_x())

        with self.say("c4.hook.2") as c:
            # {grab}: the ring lands on the biggest coin ...
            c.wait_until("grab")
            self.play(FadeIn(ring, scale=1.3),
                      run_time=min(0.9, 0.9 * c.until("that fits")))
            c.wait_until("that fits")
            # ... too big for 43p
            self.play(ring.animate.set_stroke(RED),
                      FlashAround(coins[0], color=RED, time_width=1.5, buff=0.2),
                      run_time=min(1.0, 0.9 * c.until("twenty")))
            c.wait_until("twenty")
            # the twenty fits
            self.play(ring.animate(path_arc=-0.7 * PI).move_to(coins[1]).set_stroke(YELLOW),
                      FadeOut(self.ask, scale=0.6),
                      run_time=min(1.0, 0.9 * c.until("and then")))
            c.wait_until("and then")
            k = min(1.5, 0.95 * c.until("program"))
            self.play(
                time_span(TransformFromCopy(coins[1], handed), 0, 0.8 * k),
                time_span(GrowArrow(arrow), 0.4 * k, 0.8 * k),
                time_span(FadeIn(left, shift=0.3 * LEFT), 0.5 * k, k),
                run_time=k,
            )

            # {program}: the coins' copies come down as an OCaml list
            c.wait_until("program")
            rt = min(2.2, 0.9 * c.until("forty-three pence"))
            u = rt / 2.2
            anims = []
            for i, (k_, grp) in enumerate(zip(coins, nums)):
                s = 0.12 * i * u
                e = s + 1.5 * u
                anims += [time_span(TransformFromCopy(a, b), s, e) for a, b in zip(k_[1], grp)]
                anims.append(time_span(FadeOut(k_[0].copy(), target_position=grp.get_center(),
                                               scale=0.35), s, e))
            anims += [time_span(FadeIn(g), 1.0 * u, 2.2 * u) for g in frame]
            self.play(*anims, run_time=rt)
            settle(self, code)
            settle(self, till.group)

            # "forty-three pence": the program's 43 comes from the amount owed
            c.wait_until("forty-three pence")
            self.play(TransformFromCopy(self.amount, owed), run_time=min(1.3, 0.9 * c.until("catch")))

            # {catch}: the grab clears, the rest dims; another till, where it gets stuck
            c.wait_until("catch")
            k = min(1.6, 0.9 * c.until("stuck"))
            # the main till's parts one by one: its stacks fade so the dimmed coins still read as discs
            self.remove(till.group)
            self.add(*till.group.submobjects)
            self.play(
                *[time_span(FadeOut(p), 0, 0.6 * k) for p in till.piles],
                *[time_span(FadeOut(m), 0, 0.5 * k)
                  for m in (ring, handed, arrow, left, self.amount, self.change)],
                *set_alpha([till.tray, *till.dividers, till.caption, code, owed], 0.4),
                *[Transform(k, dim_coin(k)) for k in coins],
                time_span(FadeIn(small.group, shift=0.3 * DOWN), 0.35 * k, k),
                time_span(FadeIn(six, shift=0.3 * DOWN), 0.5 * k, k),
                run_time=k,
            )
            c.wait_until("stuck")
            self.play(FadeIn(stuck, scale=0.6), run_time=0.8)
        self.code, self.owed = code, owed

    # ── hand-off: the six coins alone, centred ─────────────────────────────
    def hand_off(self):
        till = self.till
        row = VGroup(*[coin(v) for v in VALUES]).arrange(RIGHT, buff=0.28).move_to(ORIGIN)
        self.wait(0.6)
        self.remove(till.group)
        self.add(till.tray, *till.dividers, till.caption)
        self.add(*till.coins)
        others = [m for m in self.mobjects if all(m is not k for k in till.coins)]
        self.play(*[FadeOut(m) for m in others],
                  *[Transform(k, t) for k, t in zip(till.coins, row)], run_time=1.2)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)   # end on an empty frame
        self.wait(0.15)
