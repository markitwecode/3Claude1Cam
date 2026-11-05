"""Chapter 5, scene 1: hook: the ripple counter's 7 -> 6 -> 4 -> 0, one shared clock, and the question
of what each flip-flop's input should be. Clips c5.hook.1 – c5.hook.2.

Circuit: ch4_s3_ripple's ripple_circuit() (make_ff with bubble, copied), at k = 0.85, centre (0, 1.2).
Readout trail: ch4_s5_problems' zoom_reading / trail_arrows styling (T 36, pitch 2.85).
End shot: three D flip-flops (ch2_s6_symbols make_ff, no bubble, scale 0.85), FF0 on the left,
box centres (-3.655, 1.2), (0, 1.2), (3.655, 1.2); boxes 1.275 x 2.21 (FG stroke 4);
D wires and labels BLUE with a BLUE "?" left of each; Q / Q-bar GREEN; one YELLOW clock bus at
y = -0.755 into all three triangles; CLK label (T 36 YELLOW) under FF0's clock wire.
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


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- ch4_s3_ripple's make_ff (ins=..., bubble=...) ---------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.bub, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, bub, clk_w, q_w, qb_w, in_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


# ---- ch2_s6_symbols' make_ff (the D flip-flop), renamed make_dff ------------------------------
def make_dff(center=ORIGIN):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    g.box, g.tri = box, tri
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- the ripple counter (ch4_s3_ripple.ripple_circuit) ----------------------------------------
CH_X = (-4.3, 0.0, 4.3)
STUB_Y = 1.75
FEED_Y = -BOX_H / 2 - EN_WIRE
K = 0.85
CENTER = _p(0, 1.2)


def _place(m):
    return m.scale(K, about_point=ORIGIN).shift(CENTER)


def ripple_circuit():
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True) for x in CH_X]
    ones = [MathTex("1", font_size=44, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    feeds, stubs, dots, q_labels = [], [], [], []
    for i, x in enumerate(CH_X):
        jx = x + BOX_W / 2 + WIRE + 0.4
        stubs.append(poly([(x + BOX_W / 2 + WIRE, PIN_Y), (jx, PIN_Y), (jx, STUB_Y)], GREEN, 5))
        q_labels.append(MathTex(f"Q_{i}", font_size=44, color=GREEN).next_to(_p(jx, STUB_Y), UP, buff=0.1))
        if i < 2:
            ffs[i + 1].clk_w.set_stroke(GREEN)
            feeds.append(poly([(jx, PIN_Y), (jx, FEED_Y), (CH_X[i + 1], FEED_Y)], GREEN, 5))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    g = VGroup(*ffs, *ones, *stubs, *feeds, *dots, *q_labels)
    for m in (g, clk_l):
        _place(m)
    g.ffs, g.ones, g.feeds, g.stubs, g.dots, g.q_labels, g.clk_l = ffs, ones, feeds, stubs, dots, q_labels, clk_l

    def glow_path(i):
        f, n = ffs[i], ffs[i + 1]
        pts = [f.q_w.get_start(), stubs[i].get_points()[3], *[feeds[i].get_points()[j] for j in (3, 7)],
               n.clk_w.get_end()]
        return VMobject().set_points_as_corners(pts).set_stroke(GREEN, 10)
    g.glow_path = glow_path
    return g


# ---- the readout trail (ch4_s5_problems styling) ----------------------------------------------
READS = [("111", 7, GREEN), ("110", 6, RED), ("100", 4, RED), ("000", 0, GREEN)]
TRAIL_PITCH = 2.85
TRAIL_Y = -2.15


def reading(j):
    bits, v, col = READS[j]
    return T(f"{bits} = {v}", 36, col).move_to(_p((j - 1.5) * TRAIL_PITCH, TRAIL_Y))


def trail_arrows():
    xs = [(j - 1.5) * TRAIL_PITCH for j in range(4)]
    half = 0.5 * T("111 = 7", 36).width
    return [Arrow(_p(xs[j] + half + 0.28, TRAIL_Y), _p(xs[j + 1] - half - 0.28, TRAIL_Y), buff=0,
                  stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4).set_color(DIM)
            for j in range(3)]


def pulse(m, color=YELLOW, k=1.35):
    """A colour pulse that returns to the start (no flash box round a single glyph)."""
    return m.animate(rate_func=there_and_back).scale(k).set_color(color)


class Hook(NarratedScene):
    def construct(self):
        card = self.card = title_card("Part 5 · Designing a synchronous counter")
        if card.title.width > 12.0:
            card.title.scale_to_fit_width(12.0)
        self.wait(0.3)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(FadeIn(card.course), run_time=0.6)  # early: title card
        self.play(FadeIn(card.part), run_time=0.6)  # early: title card
        self.wait(4.4)
        self.clip1()
        self.clip2()
        self.wait(3.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c5.hook.1
    def clip1(self):
        circ = self.circ = ripple_circuit()
        with self.say("c5.hook.1") as c:
            # {ripple}: the card clears, the ripple counter comes in
            c.wait_until("ripple")
            self.play(*[FadeOut(m) for m in (self.card.title, self.card.rule, self.card.course, self.card.part)],
                      run_time=0.8)
            self.play(*appear(*circ.ffs, shift=None, lag=0.2),
                      *during(appear(*circ.ones, *circ.stubs, *circ.feeds, *circ.dots, *circ.q_labels,
                                     circ.clk_l, shift=None, lag=0.05), 0.4, 1.0),
                      run_time=1.6)  # early: the circuit shown whole
            # each clocked by the output of the one before
            c.wait_until("output")
            self.play(VShowPassingFlash(circ.glow_path(0), time_width=0.6), run_time=1.0)
            self.play(VShowPassingFlash(circ.glow_path(1), time_width=0.6), run_time=1.0)

            # {stagger}: 7 -> 6 -> 4 -> 0, each step later than the last
            self.reads = [reading(j) for j in range(4)]
            self.arrows = trail_arrows()
            c.wait_until("seven")
            self.play(*appear(self.reads[0]), run_time=1.0)
            for j, cue in ((1, "six"), (2, "four"), (3, "before")):
                c.wait_until(cue)
                self.play(*during([GrowArrow(self.arrows[j - 1])], 0, 0.5),
                          *during(appear(self.reads[j]), 0.3, 1), run_time=min(1.0, c.until(None, floor=0.5)))

    # ------------------------------------------------------------------ c5.hook.2
    def clip2(self):
        circ = self.circ
        dffs = self.dffs = [_place(make_dff(_p(x, 0))) for x in CH_X]
        with self.say("c5.hook.2") as c:
            # {fix}: the chained clock wires go red
            red = [*circ.feeds, *circ.dots, circ.ffs[1].clk_w, circ.ffs[2].clk_w]
            self.play(*recolor(red, RED), run_time=1.0)

            # {oneclock}: they fade, the bubbles go, one clock line feeds all three
            c.wait_until("oneclock")
            self.play(*[FadeOut(m) for m in red], *[FadeOut(f.bub) for f in circ.ffs], run_time=0.8)
            bus = self.bus = _place(Line(_p(CH_X[0], FEED_Y), _p(CH_X[2], FEED_Y)).set_stroke(YELLOW, 5))
            jdot = self.jdot = _place(Dot(_p(CH_X[1], FEED_Y), radius=0.09, color=YELLOW))
            self.play(FadeIn(dffs[0].clk_w), Create(bus),
                      *during([GrowFromEdge(dffs[1].clk_w, DOWN), GrowFromEdge(dffs[2].clk_w, DOWN),
                               FadeIn(jdot)], 0.5, 1.0),
                      run_time=1.4)
            self.remove(circ.ffs[0].clk_w)
            # a pulse runs along the line and reaches all three boxes in the same frame
            c.wait_until("same edge")
            self.play(*during([VShowPassingFlash(bus.copy().set_stroke(YELLOW, 10), time_width=0.6)], 0, 0.5),
                      *during([VShowPassingFlash(d.clk_w.copy().set_stroke(YELLOW, 10), time_width=0.8)
                               for d in dffs], 0.5, 0.75),
                      *during([f.box.animate(rate_func=there_and_back).set_stroke(YELLOW, 6)
                               for f in circ.ffs], 0.7, 1.0),
                      run_time=1.8)

            # {together}: 7 -> 0 in a single step
            c.wait_until("together")
            r, a = self.reads, self.arrows
            self.play(*disappear(r[1], r[2], a[1], a[2]), run_time=0.8)
            self.play(r[0].animate.shift(TRAIL_PITCH * RIGHT), a[0].animate.shift(TRAIL_PITCH * RIGHT),
                      r[3].animate.move_to(_p(0.5 * TRAIL_PITCH, TRAIL_Y)), run_time=1.5)
            self.play(FlashAround(VGroup(r[0], a[0], r[3]).copy(), color=GREEN, time_width=1.5, buff=0.2),
                      run_time=1.5)

            # {but}: the 1-ties go, each T becomes D, a "?" on each D wire
            c.wait_until("but")
            self.qs = [T("?", 44, BLUE, weight=BOLD).move_to(o) for o in circ.ones]
            self.play(*[FadeOut(o) for o in circ.ones],
                      *[a for f, d in zip(circ.ffs, dffs) for a in swap(f.labels[0], d.d_l)],
                      run_time=1.2)
            self.play(*appear(*self.qs, lag=0.25), run_time=1.0)

            # {tell}: the three "?" pulse in turn; the old readout clears
            c.wait_until("tell")
            self.play(*disappear(r[0], a[0], r[3]), run_time=0.8)
            c.wait_until("each")
            self.play(*[x for i, q in enumerate(self.qs) for x in during([pulse(q)], 0.3 * i, 0.3 * i + 0.4)],
                      run_time=2.2)

            # {question}
            c.wait_until("question")
            self.question = T("What should each flip-flop's input be?", 40, YELLOW).move_to(_p(0, TRAIL_Y - 0.1))
            self.play(*appear(self.question), run_time=1.2)  # early: the question, read as it is asked
