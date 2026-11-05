"""Chapter 3, scene 1: Hook. Clips c3.hook.1 – c3.hook.2.

Title card (as ch2_s1_hook), last time's edge-triggered D flip-flop (ch2_s6 / ch2_s7 make_ff) with a
small CLK / D / Q timing diagram (ch2_s5 conventions: unknown at both levels, YELLOW up-arrows),
then J-K and T boxes rising out of an old textbook, then RED stub pins that bypass the clock.
Ends on the chapter's road: J-K -> T -> asynchronous inputs.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# ---- flip-flop symbol, as ch2_s7_recap.make_ff (ch2_s6's box, pins and triangle) -----------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
SEPIA = "#8C7A5B"


def _p(x, y):
    return np.array([x, y, 0.0])


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),)):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w = box, tri, clk_w, q_w, qb_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


def place(g, scale, box_center):
    """Scale g and put its box centre at box_center (returns g)."""
    g.scale(scale)
    g.shift(_p(*box_center[:2]) - g.box.get_center())
    return g


# ---- small CLK / D / Q timing diagram ---------------------------------------------------------
X0, X1 = -1.0, 6.3
RISES = [-0.2, 1.6, 3.4, 5.2]
HALF = 0.9
ROWS = {"CLK": 1.2, "D": 0.0, "Q": -1.2}
AMP = 0.25


def lvl(row, bit):
    return ROWS[row] + (AMP if bit else -AMP)


def poly(row, pts, color, width=4):
    return VMobject().set_points_as_corners([_p(x, lvl(row, b)) for x, b in pts]).set_stroke(color, width)


def steps(row, start_bit, edges, color):
    pts, b = [(X0, start_bit)], start_bit
    for e in edges:
        pts += [(e, b), (e, 1 - b)]
        b = 1 - b
    pts.append((X1, b))
    return poly(row, pts, color)


def timing():
    edges = []
    for r in RISES:
        edges += [r, r + HALF]
    clk = steps("CLK", 0, [e for e in edges if e < X1], YELLOW)
    d = steps("D", 1, [0.6, 2.1, 2.5, 2.9, 4.4, 5.7], BLUE)
    q_hi = poly("Q", [(X0, 1), (RISES[0], 1)], GREEN)
    q_lo = poly("Q", [(X0, 0), (RISES[0], 0)], GREEN)
    q = poly("Q", [(RISES[0], 1), (RISES[1], 1), (RISES[1], 0), (RISES[2], 0), (RISES[2], 1),
                   (RISES[3], 1), (RISES[3], 0), (X1, 0)], GREEN)
    labs = {k: T(k, 34, c).move_to(_p(0, ROWS[k])).align_to(_p(X0 - 0.3, 0), RIGHT)
            for k, c in (("CLK", YELLOW), ("D", BLUE), ("Q", GREEN))}
    ups = [Arrow(_p(r, ROWS["CLK"] - AMP - 0.1), _p(r, ROWS["CLK"] + AMP + 0.35), buff=0, stroke_width=6,
                 tip_length=0.2, max_tip_length_to_length_ratio=0.3, color=YELLOW) for r in RISES]
    guides = [DashedLine(_p(r, ROWS["CLK"] - AMP - 0.15), _p(r, ROWS["Q"] - AMP - 0.15), dash_length=0.08)
              .set_stroke(DIM, 1.5).set_z_index(-2) for r in RISES]
    flats = [(RISES[0], RISES[1], 1), (RISES[1], RISES[2], 0), (RISES[2], RISES[3], 1), (RISES[3], X1, 0)]
    holds = [Line(_p(a + 0.05, lvl("Q", b)), _p(z - 0.05, lvl("Q", b))).set_stroke(GREEN, 10) for a, z, b in flats]
    return dict(clk=clk, d=d, q_hi=q_hi, q_lo=q_lo, q=q, labs=labs, ups=ups, guides=guides, holds=holds)


def closed_book(center, w=4.6, h=0.6):
    """A closed book lying flat, in outline (sepia-dim): cover, spine, page edges."""
    cx, cy = center
    cover = RoundedRectangle(corner_radius=0.08, width=w, height=h).set_stroke(SEPIA, 3).move_to(_p(cx, cy))
    spine = Line(_p(cx - w / 2 + 0.35, cy - h / 2), _p(cx - w / 2 + 0.35, cy + h / 2)).set_stroke(SEPIA, 3)
    pages = VGroup(*[Line(_p(cx - w / 2 + 0.55, cy + dy), _p(cx + w / 2 - 0.12, cy + dy)).set_stroke(SEPIA, 1.5, 0.7)
                     for dy in (-0.12, 0.0, 0.12)])
    return VGroup(cover, spine, pages)


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.road()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c3.hook.1
    def clip1(self):
        # silent lead-in: the title card is up ~2 s before the first word (as ch2_s1_hook)
        card = title_card("Part 3 · J-K, T, and asynchronous inputs")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(FadeIn(card.course), run_time=0.6)  # early: title card
        self.play(FadeIn(card.part), run_time=0.6)  # early: title card
        self.wait(3.0)
        with self.say("c3.hook.1") as c:
            c.wait_until("last")
            self.ff = ff = place(make_ff(), 1.15, (0, 0.3))
            sweep_clear(self, *appear(ff, shift=None), run_time=min(1.8, c.until("built")))  # early: last time's symbol, shown whole
            c.wait_until("dee flip-flop")
            self.play(FlashAround(ff.box, color=BLUE, time_width=1.5), run_time=min(1.5, c.until("edge")))
            c.wait_until("edge")

            # {edge}: the symbol steps left, the timing diagram appears beside it
            self.td = td = timing()
            self.play(ff.animate.scale(0.85 / 1.15).shift(_p(-3.9, 0) - ff.box.get_center() + _p(0, 0.3)),
                      run_time=1.2)
            rows = [VGroup(td["labs"]["CLK"], td["clk"]), VGroup(td["labs"]["D"], td["d"]),
                    VGroup(td["labs"]["Q"], td["q_hi"], td["q_lo"], td["q"])]
            self.play(*appear(*rows, shift=None, lag=0.3),  # early: diagram shown whole, then walked
                      run_time=min(1.6, c.until("rising edge")))
            c.wait_until("rising edge")
            self.play(*appear(*td["guides"], shift=None, lag=0.1),
                      *[GrowArrow(a) for a in td["ups"]], run_time=min(1.5, c.until("holds")))
            c.wait_until("holds")
            self.play(*[VShowPassingFlash(h.copy(), time_width=1.0, taper_width=0.1) for h in td["holds"]],
                      run_time=min(2.0, c.until("in between")))
            self.rows = rows

    # ------------------------------------------------------------------ c3.hook.2
    def clip2(self):
        ff, td = self.ff, self.td
        with self.say("c3.hook.2") as c:
            # {books}: the diagram clears, D slides left and dims; an old book appears
            old = [*self.rows, *td["ups"], *td["guides"]]
            self.play(*disappear(*old),
                      *during([ff.animate.scale(0.8 / 0.85).shift(_p(-4.7, 0.7) - ff.box.get_center())], 0.2, 1),
                      run_time=1.2)
            book = closed_book((2.2, -2.6))
            self.play(*set_alpha([ff], 0.4), FadeIn(book, shift=0.2 * UP), run_time=1.0)

            jk = place(make_ff(ins=(("J", PIN_Y), ("K", -PIN_Y))), 0.8, (0.0, 0.7))
            tf = place(make_ff(ins=(("T", PIN_Y),)), 0.8, (4.4, 0.7))
            c.wait_until("jay")
            self.play(FadeIn(jk, target_position=book.get_center(), scale=0.3),
                      run_time=min(1.5, c.until("tee")))
            c.wait_until("tee")
            self.play(FadeIn(tf, target_position=book.get_center(), scale=0.3),
                      run_time=min(1.5, c.until("ask")))
            c.wait_until("ask")
            qs = [T("?", 64, YELLOW).move_to(_p(g.box.get_center()[0], 2.45)) for g in (jk, tf)]
            self.play(*appear(*qs, lag=0.3), run_time=1.0)
            c.wait_until("dee-types")
            self.play(FlashAround(ff.box, color=BLUE, time_width=1.5), run_time=min(1.5, c.until("pins")))
            c.wait_until("pins")

            # {pins}: the old pair clears; D comes back to the centre at full brightness
            # the pair and the book are gone before D slides across their place
            self.play(*during(disappear(jk, tf, book, *qs), 0, 0.4),
                      *during([ff.animate.scale(1.1 / 0.8).shift(_p(0, 0.8) - ff.box.get_center())], 0.45, 1),
                      run_time=1.8)
            s = 1.1
            bc = ff.box.get_center()
            top = Line(bc + _p(0, BOX_H / 2 * s), bc + _p(0, BOX_H / 2 * s + 0.9)).set_stroke(RED, 6)
            bot = Line(bc + _p(-0.6, -BOX_H / 2 * s), bc + _p(-0.6, -BOX_H / 2 * s - 0.9)).set_stroke(RED, 6)
            self.play(*set_alpha([ff], 1), Create(top), Create(bot), run_time=min(1.2, c.until("ignore")))
            c.wait_until("ignore")

            # {ignore}: RED paths from the pins straight to the outputs, around the clock
            q_end = ff.q_w.get_end()
            qb_end = ff.qb_w.get_end()
            a_top = CurvedArrow(top.get_end(), q_end + _p(0.15, 0.12), angle=-PI / 2,
                                color=RED, stroke_width=5, tip_length=0.22)
            a_bot = CurvedArrow(bot.get_end(), qb_end + _p(0.2, -0.1), angle=PI,
                                color=RED, stroke_width=5, tip_length=0.22)
            self.play(Create(a_bot), run_time=min(1.6, c.until("Yet real")))
            self.play(Create(a_top), run_time=min(1.0, c.until("Yet real")))
            c.wait_until("extra inputs")
            self.play(FlashAround(top, color=RED, time_width=1.5), FlashAround(bot, color=RED, time_width=1.5),
                      run_time=min(1.4, c.until("why")))
            c.wait_until("why")
            cap = T("inputs that ignore the clock?", 40, FG).move_to(_p(0, -3.3))
            self.play(*appear(cap), run_time=1.0)
            self.extras = [top, bot, a_top, a_bot, cap]

    # ------------------------------------------------------------------ the chapter's road
    def road(self):
        self.wait(2.5)   # the question holds after the voice stops
        items = [T("J-K", 40, BLUE), T("T", 40, BLUE), T("asynchronous inputs", 40, RED)]
        row = VGroup(items[0], items[1], items[2]).arrange(RIGHT, buff=1.4).move_to(ORIGIN)
        arrows = [Arrow(items[i].get_right(), items[i + 1].get_left(), buff=0.25, stroke_width=4,
                        max_tip_length_to_length_ratio=0.25, color=DIM) for i in range(2)]
        del row
        # one simultaneous clear of the D symbol, pins, arrows and caption; then the road
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.play(*appear(items[0], arrows[0], items[1], arrows[1], items[2], shift=None, lag=0.3),  # early: the road ahead, read whole
                  run_time=1.6)
        self.wait(4.0)
