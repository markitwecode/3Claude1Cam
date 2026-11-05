"""Chapter 5, scene 2: synchronous design: one clock, more logic, the shape of every synchronous
counter. Clips c5.sync.1 – c5.sync.4.

sync_structure(k=0.85, center=(0, -0.5)) is the shared picture (s6 {logic} and the s8 recap bring
it back small): ch2_s6's make_ff (no bubble) x3, FF0 on the left, box centres x = -4.3, 0, 4.3,
y = 0 before scaling (so at k = 0.85 the pitch is 3.655, as in ch5_s1_hook's end shot); one YELLOW
CLK bus at y = -2.3 from FF0 to FF2 (junction dot at FF1), CLK label T 36 under FF0's clock wire;
Q_k (MathTex 48 GREEN) above each box's right corner, D_k (MathTex 48 BLUE) above its left corner;
GREEN Q wires run straight up from each Q pin (x + 1.6) into a BLUE rounded "combinational logic"
box (12.4 x 1.2, centre y = 4.05), BLUE D wires come straight down from it to each D pin (x - 1.6);
thin brackets across the three Q wires (GREEN, y = 3.12, just under the box, "current state" at its left end) and the
three D wires (BLUE, y = 2.5, "next state" at its right end), simply crossing the other colour's wires. Built at ORIGIN,
then .scale(k, about_point=ORIGIN).shift(center). Default: spans x -5.6 … 5.4, y -2.9 … 3.45.
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


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CH_X = (-4.3, 0.0, 4.3)
FEED_Y = -BOX_H / 2 - EN_WIRE          # -2.3: the clock bus
STUB_Y = 1.75


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


# ---- ch2_s6_symbols' make_ff (D flip-flop; bubble for the ripple mini) -----------------------
def make_ff(center=ORIGIN, bubble=False, d_text="D"):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    bub = None
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.1))
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.2)).set_stroke(YELLOW, 5)
    else:
        clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- THE synchronous counter structure (s6 {logic} and the s8 recap reuse this) --------------
def sync_structure(k=0.85, center=_p(0, -0.5)):
    """Three D flip-flops on one clock, a combinational-logic box above, Q wires up, D wires down.
    Parts: .ffs .bus .jdot .clk_l .q_labels .d_labels .q_up .d_down .box .box_l .cur_l .next_l
    .cur_br .next_br (thin brackets across the three Q / the three D wires, the labels at their ends);
    .core = VGroup(ffs, bus, jdot, clk_l) (s1's end shot); .q_spot(i) / .d_spot(i): where a GOLD/GREEN
    value digit sits just above Q_i's / D_i's pin wire (outside the box); .clk_paths(): fresh
    YELLOW paths (bus, then each clock wire) for a clock pulse."""
    ffs = [make_ff(_p(x, 0)) for x in CH_X]
    bus = Line(_p(CH_X[0], FEED_Y), _p(CH_X[2], FEED_Y)).set_stroke(YELLOW, 5)
    jdot = Dot(_p(CH_X[1], FEED_Y), radius=0.09, color=YELLOW)
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    q_labels = [MathTex(f"Q_{i}", font_size=48, color=GREEN).move_to(_p(x + 1.15, 1.85))
                for i, x in enumerate(CH_X)]
    d_labels = [MathTex(f"D_{i}", font_size=48, color=BLUE).move_to(_p(x - 1.15, 1.85))
                for i, x in enumerate(CH_X)]
    box_y0, box_h = 3.45, 1.2
    box = RoundedRectangle(corner_radius=0.3, width=12.4, height=box_h).set_stroke(BLUE, 4)
    box.set_fill(BG, 1).move_to(_p(0, box_y0 + box_h / 2))
    box_l = T("combinational logic", 52, FG).move_to(box)
    q_up = [poly([(x + BOX_W / 2 + WIRE, PIN_Y), (x + BOX_W / 2 + WIRE, box_y0)], GREEN) for x in CH_X]
    d_down = [poly([(x - BOX_W / 2 - WIRE, box_y0), (x - BOX_W / 2 - WIRE, PIN_Y)], BLUE) for x in CH_X]
    qx = [x + BOX_W / 2 + WIRE for x in CH_X]
    dx = [x - BOX_W / 2 - WIRE for x in CH_X]

    def bracket(x0, x1, y, color):
        cap = 0.16
        br = VGroup(Line(_p(x0, y), _p(x1, y)), Line(_p(x0, y - cap), _p(x0, y + cap)),
                    Line(_p(x1, y - cap), _p(x1, y + cap))).set_stroke(color, 2.5)
        br.set_z_index(-1)
        return br
    cur_br = bracket(qx[0], qx[2], 3.12, GREEN)          # across the three Q wires
    next_br = bracket(dx[0], dx[2], 2.5, BLUE)          # across the three D wires
    cur_l = T("current state", 35, GREEN).next_to(_p(qx[0], 3.12), LEFT, buff=0.2)
    next_l = T("next state", 35, BLUE).next_to(_p(dx[2], 2.5), RIGHT, buff=0.2)
    # spots for value digits (unscaled), moved along with the group by invisible dots
    q_pts = [Dot(_p(x + 1.15, 1.08), radius=0.01).set_opacity(0) for x in CH_X]
    d_pts = [Dot(_p(x - 1.15, 1.08), radius=0.01).set_opacity(0) for x in CH_X]
    g = VGroup(*ffs, bus, jdot, clk_l, *q_labels, *d_labels, *q_up, *d_down, box, box_l, cur_br, cur_l, next_br, next_l,
               *q_pts, *d_pts)
    g.scale(k, about_point=ORIGIN).shift(center)
    g.ffs, g.bus, g.jdot, g.clk_l, g.q_labels, g.d_labels = ffs, bus, jdot, clk_l, q_labels, d_labels
    g.q_up, g.d_down, g.box, g.box_l, g.cur_l, g.next_l = q_up, d_down, box, box_l, cur_l, next_l
    g.cur_br, g.next_br = cur_br, next_br
    g.core = VGroup(*ffs, bus, jdot, clk_l)
    g.q_spot = lambda i: q_pts[i].get_center()
    g.d_spot = lambda i: d_pts[i].get_center()

    def clk_paths():
        return ([bus.copy().set_stroke(YELLOW, 10)],
                [f.clk_w.copy().set_stroke(YELLOW, 10) for f in ffs])
    g.clk_paths = clk_paths
    return g


# ---- ch4_s3_ripple's ripple_circuit (for the RED card and the crossed-out wire) ---------------
def ripple_circuit(k=0.85, center=_p(0, 0.85)):
    ffs = [make_ff(_p(x, 0), bubble=True, d_text="T") for x in CH_X]
    ones = [MathTex("1", font_size=44, color=BLUE).next_to(f.d_w.get_start(), LEFT, buff=0.12) for f in ffs]
    feeds, stubs, dots, q_labels = [], [], [], []
    for i, x in enumerate(CH_X):
        jx = x + BOX_W / 2 + WIRE + 0.4
        stubs.append(poly([(x + BOX_W / 2 + WIRE, PIN_Y), (jx, PIN_Y), (jx, STUB_Y)], GREEN))
        q_labels.append(MathTex(f"Q_{i}", font_size=44, color=GREEN).next_to(_p(jx, STUB_Y), UP, buff=0.1))
        if i < 2:
            ffs[i + 1].clk_w.set_stroke(GREEN)
            feeds.append(poly([(jx, PIN_Y), (jx, FEED_Y), (CH_X[i + 1], FEED_Y)], GREEN))
            dots.append(Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN))
    clk_l = T("CLK", 36, YELLOW).next_to(ffs[0].clk_w.get_start(), DOWN, buff=0.12)
    g = VGroup(*ffs, *ones, *stubs, *feeds, *dots, *q_labels, clk_l)
    g.scale(k, about_point=ORIGIN).shift(center)
    g.ffs, g.ones, g.feeds, g.stubs, g.dots, g.q_labels = ffs, ones, feeds, stubs, dots, q_labels
    return g


# ---- ch4_s2's ring of eight states (copied from ch4_s3_ripple) ---------------------------------
NODE_R = 0.5


def state_ring(n_bits=3, radius=2.3):
    n = 2 ** n_bits

    def dirn(i):
        a = PI / 2 - TAU * i / n
        return np.array([np.cos(a), np.sin(a), 0.0])

    nodes, decimals, arrows = [], [], []
    for i in range(n):
        p = radius * dirn(i)
        circ = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        b = Mono(format(i, f"0{n_bits}b"), size=28, color=GREEN).move_to(p)
        nodes.append(VGroup(circ, b))
        decimals.append(T(str(i), 34, color=GOLD).move_to(p - 0.85 * dirn(i)))
    for i in range(n):
        p, q = radius * dirn(i), radius * dirn((i + 1) % n)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.5))
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*decimals))
    return ring


def tiny_ripple_wire():
    """DIM copy of the ripple chain's first two flip-flops, the GREEN Q0 -> clock wire kept."""
    r = ripple_circuit()
    g = strip_text(VGroup(r.ffs[0], r.ffs[1], r.stubs[0], r.feeds[0], r.dots[0]).copy())
    for m in g[0].family_members_with_points() + g[1].family_members_with_points():
        if m.get_stroke_width() > 0 and m.get_stroke_color() != ManimColor(GREEN):
            m.set_stroke(DIM)
        if m.get_fill_opacity() > 0 and m.get_stroke_width() == 0:
            m.set_fill(DIM)
    for m in (g[2], g[3], g[4]):
        m.set_stroke(opacity=0.8)
    return g


def strip_text(g):
    """Remove every Text / MathTex part (a mini circuit is drawn without its small letters)."""
    for m in list(g.get_family()):
        for sub in list(m.submobjects):
            if isinstance(sub, (Text, MathTex)) or (isinstance(sub, VGroup) and sub.submobjects and all(
                    isinstance(x, (Text, Line)) for x in sub.submobjects)
                and any(isinstance(x, Text) for x in sub.submobjects)):
                m.remove(sub)
    return g


def digit(v, color, at):
    d = Mono(str(v), 40, color).move_to(at)
    d.set_opacity(1 if v else 0.35)
    return d


class SyncDesign(NarratedScene):
    def construct(self):
        self.S = sync_structure()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clock_pulse(self, extra=(), run_time=1.6):
        bus_p, clk_p = self.S.clk_paths()
        self.play(*during([VShowPassingFlash(p, time_width=0.6) for p in bus_p], 0, 0.5),
                  *during([VShowPassingFlash(p, time_width=0.8) for p in clk_p], 0.5, 0.75),
                  *extra, run_time=run_time)

    # ------------------------------------------------------------------ c5.sync.1
    def clip1(self):
        S = self.S
        with self.say("c5.sync.1") as c:
            # {rule}: two cards, RED ripple, GREEN synchronous
            cards = []
            for y, col, head, sub in ((1.75, RED, "Ripple counters:", "should not usually be used"),
                                      (-1.75, GREEN, "Synchronous designs:", "recommended")):
                frame = RoundedRectangle(corner_radius=0.25, width=12.6, height=3.0).set_stroke(col, 3)
                frame.move_to(_p(0, y))
                h = T(head, 44, col)
                s = T(sub, 36, FG)
                txt = VGroup(h, s).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
                txt.move_to(_p(0, y)).align_to(_p(-0.4, 0), LEFT)
                cards.append((frame, txt))
            rip = strip_text(ripple_circuit()).set_width(4.6).move_to(_p(-3.5, 1.75))
            core = S.core
            core_txt = [f.d_l for f in S.ffs] + [f.q_l for f in S.ffs] + [f.qb_l for f in S.ffs] + [S.clk_l]
            s_k = 4.6 / core.width
            mini = strip_text(core.copy()).scale(s_k, scale_stroke=True).move_to(_p(-3.5, -1.75))
            self.play(FadeIn(cards[0][0]), FadeIn(rip), *during(appear(cards[0][1], lag=0.3), 0.2, 0.6),  # early: the slide's advice, shown whole
                      *during([FadeIn(cards[1][0]), FadeIn(mini)], 0.4, 0.8),
                      *during(appear(cards[1][1], lag=0.3), 0.6, 1.0),
                      run_time=1.3)
            c.wait_until("Use a synchronous")
            self.play(cards[1][0].animate(rate_func=there_and_back).set_stroke(GREEN, 8), run_time=1.2)

            # {clocks}: the cards clear, the GREEN card's circuit becomes the hero
            c.wait_until("clocks")
            gone = [cards[0][0], cards[0][1], rip, cards[1][0], cards[1][1]]
            self.play(*during([FadeOut(*gone)], 0, 0.4),
                      *during([mini.animate.scale(1 / s_k, scale_stroke=True).move_to(core.get_center())],
                              0.4, 1.0),
                      *during([FadeIn(*core_txt)], 0.85, 1.0),
                      run_time=min(2.0, c.until("clock signal")))
            self.remove(mini)
            self.add(*core)
            self.q = [digit(v, GREEN, S.q_spot(i)) for i, v in enumerate((1, 1, 0))]
            self.play(*appear(*S.d_labels, *S.q_labels, lag=0), *during(appear(*self.q, shift=None), 0.4, 1),
                      run_time=1.2)  # early: names of the pins, not spoken
            c.wait_until("clock signal")
            self.clock_pulse(run_time=1.6)

            # {same}: one pulse, all three Q outputs change in the same frame
            c.wait_until("same")
            new = [digit(v, GREEN, S.q_spot(i)) for i, v in enumerate((0, 0, 1))]
            swaps = []
            for o, n in zip(self.q, new):
                swaps += swap(o, n)
            self.clock_pulse(extra=during(swaps, 0.72, 1.0), run_time=2.2)
            self.q = new
            self.play(*[FlashAround(VGroup(f.box), color=YELLOW, time_width=1.5, buff=0.1) for f in S.ffs],
                      run_time=1.2)

    # ------------------------------------------------------------------ c5.sync.2
    def clip2(self):
        S = self.S
        with self.say("c5.sync.2") as c:
            self.tag = T("the price: more combinational logic", 44, GOLD).move_to(_p(0, 3.0)).align_to(_p(-6.2, 0), LEFT)
            self.play(*appear(self.tag), run_time=1.0)
            # {logic}: each D input now needs its own logic
            c.wait_until("input")
            self.play(*[VShowPassingFlash(f.d_w.copy().set_stroke(YELLOW, 10), time_width=0.6) for f in S.ffs],
                      run_time=1.2)
            # {type}
            c.wait_until("type")
            self.type_l = T("(different for each flip-flop type)", 32, DIM).next_to(self.tag, DOWN, buff=0.25)
            self.type_l.align_to(self.tag, LEFT)
            self.play(*appear(self.type_l), run_time=1.0)  # early: caption of the sentence
            # {wiring}: the ripple chain's Q0 -> clock wire, crossed out
            c.wait_until("wiring")
            self.tiny = tiny_ripple_wire().set_width(2.6).move_to(_p(5.1, 2.75))
            self.cross = Cross(self.tiny, stroke_color=RED, stroke_width=6, scale_factor=0.9)
            self.play(FadeIn(self.tiny), run_time=1.0)
            self.play(Create(self.cross), run_time=min(1.0, c.until("Here")))
            c.wait_until("Here")
            self.play(*recolor(self.tag, YELLOW), run_time=0.8)
            self.play(*recolor(self.tag, GOLD), run_time=0.8)

    # ------------------------------------------------------------------ c5.sync.3
    def clip3(self):
        S = self.S
        with self.say("c5.sync.3") as c:
            # {structure}: the price clears; the logic box arrives above the flip-flops
            self.play(*during([FadeOut(self.tag, self.type_l, self.tiny, self.cross)], 0, 0.45),
                      *during([FadeIn(S.box)], 0.45, 1.0), *during(appear(S.box_l, shift=None), 0.6, 1.0),
                      run_time=min(1.8, c.until("current")))
            # {current}: Q wires run up into the box
            c.wait_until("current")
            self.play(*[Create(w) for w in S.q_up], run_time=1.5)
            c.wait_until(own_word=S.cur_l)
            self.play(FadeIn(S.cur_br), *during(appear(S.cur_l, shift=None), 0.3, 1.0), run_time=1.2)
            # {block}: values flow up, the box glows
            c.wait_until("block")
            self.play(*[VShowPassingFlash(w.copy().set_stroke(GREEN, 10), time_width=0.6) for w in S.q_up],
                      *during([FlashAround(S.box, color=YELLOW, time_width=1.5, buff=0.08)], 0.4, 1.0),
                      run_time=1.8)
            # {next}: D wires come down out of it
            c.wait_until("next")
            self.play(*[Create(w) for w in S.d_down], run_time=1.5)
            self.d = [digit(v, BLUE, S.d_spot(i)) for i, v in enumerate((1, 0, 1))]
            self.play(*appear(*self.d, shift=None, lag=0.15), run_time=1.0)
            c.wait_until(own_word=S.next_l)
            self.play(FadeIn(S.next_br), *during(appear(S.next_l, shift=None), 0.3, 1.0), run_time=1.2)
            # {edge}: CLK pulse, D values jump into Q, flow up, new D values come out
            c.wait_until("edge")
            newq = [digit(v, GREEN, S.q_spot(i)) for i, v in enumerate((1, 0, 1))]
            moves = []
            for d, n in zip(self.d, newq):
                moves += fly(d, n)
            self.clock_pulse(extra=[*during([FadeOut(*self.q)], 0.5, 0.7), *during(moves, 0.65, 1.0)],
                             run_time=min(2.0, 0.45 * c.until()))
            self.q = newq
            self.play(*[VShowPassingFlash(w.copy().set_stroke(GREEN, 10), time_width=0.6) for w in S.q_up],
                      *during([FlashAround(S.box, color=YELLOW, time_width=1.5, buff=0.08)], 0.4, 1.0),
                      run_time=min(1.2, 0.5 * c.until()))
            newd = [digit(v, BLUE, S.d_spot(i)) for i, v in enumerate((0, 1, 1))]
            sw = []
            for o, n in zip(self.d, newd):
                sw += swap(o, n)
            self.play(*[VShowPassingFlash(w.copy().set_stroke(BLUE, 10), time_width=0.6) for w in S.d_down],
                      *during(sw, 0.4, 1.0), run_time=min(1.2, c.until(floor=0.5)))
            self.d = newd

    # ------------------------------------------------------------------ c5.sync.4
    def clip4(self):
        S = self.S
        with self.say("c5.sync.4") as c:
            # {donly}
            cap = T("D flip-flops only (the technique extends to other types)", 32, FG).move_to(_p(0, -3.4))
            self.play(*appear(cap), run_time=1.0)
            # {example}: the structure shrinks left, the ring of eight appears right
            c.wait_until("example")
            S.remove(S.cur_l, S.next_l, S.cur_br, S.next_br, S.clk_l)
            small = [S.clk_l]
            for f in S.ffs:                       # in-box letters would be ~20 pt once shrunk
                f.remove(f.d_l, f.q_l, f.qb_l)
                small += [f.d_l, f.q_l, f.qb_l]
            k = 0.66
            self.play(*during([FadeOut(*self.q, *self.d, S.cur_l, S.next_l, S.cur_br, S.next_br, *small)], 0, 0.35),
                      *during([S.animate.scale(k, scale_stroke=False).move_to(_p(-2.95, 0.35))], 0.35, 1.0),
                      run_time=1.6)
            ring = state_ring(radius=1.75).move_to(_p(4.4, 0.55))
            ring_l = T("0 to 7 up-counter", 34, FG).next_to(ring, DOWN, buff=0.3)
            self.play(FadeIn(ring[0]), *appear(*ring[1], shift=None, lag=0.08),
                      *during(appear(*ring[2], shift=None, lag=0.05), 0.4, 1.0), run_time=1.8)
            self.play(*appear(ring_l), run_time=1.0)
            # {job}: a YELLOW "?" fills the logic box and stays
            c.wait_until("job")
            S.remove(S.box_l)
            qm = T("?", 64, YELLOW, weight=BOLD).move_to(S.box)
            self.play(*swap(S.box_l, qm), run_time=1.2)
            self.play(S.box.animate(rate_func=there_and_back).set_stroke(YELLOW, 8), run_time=1.5)
            # {build}
            c.wait_until("build")
            cap2 = T("this part: what it must produce  ·  next part: the gates", 32, DIM).move_to(cap)
            self.play(*swap(cap, cap2), run_time=1.2)
