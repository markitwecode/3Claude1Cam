"""Chapter 1, scene 1: title card, L6's synchronous counter clocked faster until it miscounts, the
question, and the lecture's three-topic road. Clips c1.hook.1 – c1.hook.3.

The block between the `# ===` rulers is L6 ch6_s6_circuit's sync_counter() / led_chain / clock_source
copied verbatim, plus this lecture's placement (hook_counter: the whole circuit scaled SC = 0.86, centred
x = 0, bottom at y = -3.4), the readout above it (Q2 Q1 Q0 = bits GREEN = decimal GOLD, centred
x = -3.3, y = 2.85), and the trail of past values to its right (T 42 digits, slots x = 0.2 + 0.8 k,
y = 2.85; GOLD when correct, RED 0, 5, 2, 7 when wrong). ch1_s4 and ch1_s6 copy this block.
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


# ---- ch5_s2_sync's make_ff (D flip-flop) ------------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


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


# ---- ch1_s2_rslatch's gate drawings (OR / XOR from the NOR shape, no bubble) --------------------
GATE_COLOR = BLUE


class Gate(VGroup):
    def __init__(self, body, ins, out, extra=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        self.extra = extra
        if extra is not None:
            extra.set_stroke(color, 4).set_fill(opacity=0)
            self.add(extra)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()

    def strokes(self):
        return [m for m in (self.body, self.extra) if m is not None]


def _or_body():
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    return b


def or_gate(color=GATE_COLOR):
    """OR: the NOR body without its bubble, 1.4 x 1.2. inp(0) (-0.56, 0.3), inp(1) (-0.56, -0.3), out() (0.7, 0)."""
    return Gate(_or_body(), [(-0.56, 0.3), (-0.56, -0.3)], (0.7, 0.0), color=color)


def xor_gate(color=GATE_COLOR):
    """XOR: OR plus a back arc 0.15 behind it. inp(i) on the back arc (-0.71, +-0.3), out() (0.7, 0)."""
    arc = VMobject()
    arc.start_new_path(_p(-0.85, 0.6))
    arc.add_cubic_bezier_curve_to(_p(-0.6, 0.2), _p(-0.6, -0.2), _p(-0.85, -0.6))
    return Gate(_or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), extra=arc, color=color)


def _and_body():
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return b


def and_gate(color=GATE_COLOR):
    """AND, 1.3 x 1.2. inp(0) (-0.7, 0.3), inp(1) (-0.7, -0.3), out() (0.6, 0)."""
    return Gate(_and_body(), [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


def and3_gate(color=GATE_COLOR):
    """Three-input AND: inputs (-0.7, 0.35), (-0.7, 0), (-0.7, -0.35)."""
    return Gate(_and_body(), [(-0.7, 0.35), (-0.7, 0.0), (-0.7, -0.35)], (0.6, 0.0), color=color)


# ---- ch2_s6_symbols' LED (off reads as off: hollow DIM ring) -----------------------------------
LED_R = 0.24


def led(on):
    c = Circle(radius=LED_R)
    if on:
        c.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
    else:
        c.set_stroke(DIM, 3).set_fill(BG, 0)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    if on:
        return l.animate.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
    return l.animate.set_stroke(DIM, 3).set_fill(BG, 0)


# =============================================================================================
# THE synchronous counter (slide p. 100). s7 / s8 copy this block for their insets.
# =============================================================================================
K = 0.78                                   # flip-flop scale
FF_X = (-5.1, -0.3, 4.75)
FF_Y = -0.5
HX = (BOX_W / 2 + WIRE) * K                # box centre to the end of a pin wire (1.248)
QY = FF_Y + PIN_Y * K                      # Q and D pin row (-0.03)
QBY = FF_Y - PIN_Y * K                     # Q-bar pin row (-0.97)
BUS_Y = FF_Y - (BOX_H / 2 + EN_WIRE) * K   # the CLK line (-2.29)
LOOP_Y = -1.9                              # FF0's Q-bar -> D0 loop, under the box
DROP_X, DROP_Y = -5.8, -2.75               # CLK comes in here
RISE_TOP = 1.45
LED_Y = 2.45
LOW = 0.25                                 # a wire at 0 keeps its colour at this opacity


def zigzag(x, y0, y1, n=6, amp=0.13):
    lead = 0.1
    pts = [(x, y0), (x, y0 + lead)]
    h = (y1 - y0 - 2 * lead) / n
    for j in range(n):
        pts.append((x + (amp if j % 2 == 0 else -amp), y0 + lead + (j + 0.5) * h))
    pts += [(x, y1 - lead), (x, y1)]
    return poly(pts, FG, 4)


def led_chain(i, on=False):
    """Resistor + LED on top of riser i: VGroup(res, link, led) with .res .link .led .ohm (label, not in group)."""
    x = FF_X[i] + HX
    res = zigzag(x, RISE_TOP, 2.05)
    link = Line(_p(x, 2.05), _p(x, LED_Y - LED_R)).set_stroke(FG, 4)
    lamp = led(on).move_to(_p(x, LED_Y))
    ohm = T("270 Ω", 28, FG).next_to(_p(x - 0.13, 1.75), LEFT, buff=0.12)
    g = VGroup(res, link, lamp)
    g.res, g.link, g.led, g.ohm = res, link, lamp, ohm
    return g


def sync_counter():
    """Parts (each a separate mobject; .all lists them): .ffs .names .bus (polyline from the drop) .jdots
    .clk_l .risers .q_labels .loop (D0) .xor .xor_stubs .xor_labels .block .block_l .block_out
    .block_stubs .block_labels; .q_spot(i) / .d_spot(i): where a value digit sits above Q_i's / D_i's
    pin wire; .clk_paths(): fresh YELLOW paths (bus, then the clock pins) for a pulse."""
    S = VGroup()
    S.ffs = [make_ff().scale(K, about_point=ORIGIN).shift(_p(x, FF_Y)) for x in FF_X]
    S.names = [T(f"FF{i}", 28, DIM).move_to(_p(x, FF_Y + BOX_H / 2 * K + 0.25)) for i, x in enumerate(FF_X)]
    S.bus = poly([(DROP_X, DROP_Y), (DROP_X, BUS_Y), (FF_X[2], BUS_Y)], YELLOW)
    S.jdots = [Dot(_p(x, BUS_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    S.clk_l = T("CLK", 34, YELLOW).next_to(_p(DROP_X, DROP_Y - 0.1), RIGHT, buff=0.48)
    S.risers = [Line(_p(x + HX, QY), _p(x + HX, RISE_TOP)).set_stroke(GREEN, 5) for x in FF_X]
    S.q_labels = [MathTex(f"Q_{i}", font_size=40, color=GREEN).next_to(_p(x + HX, 1.05), LEFT, buff=0.15)
                  for i, x in enumerate(FF_X)]
    x0 = FF_X[0]
    S.loop = poly([(x0 + HX, QBY), (x0 + HX, LOOP_Y), (x0 - HX, LOOP_Y), (x0 - HX, QY)], BLUE)
    # D1: XOR right against D1's pin wire
    xg = xor_gate().scale(K)
    xg.shift(_p(FF_X[1] - HX, QY) - xg.out())
    S.xor = xg
    S.xor_stubs, S.xor_labels = [], []
    for j in range(2):
        a = xg.inp(j)
        st = Line(a + 0.35 * LEFT, a).set_stroke(GREEN, 4)
        S.xor_stubs.append(st)
        S.xor_labels.append(MathTex(f"Q_{j}", font_size=36, color=GREEN).next_to(st, LEFT, buff=0.08))
    # D2: the combinational-logic block
    x2 = FF_X[2]
    bx1 = x2 - HX - 0.3
    S.block = Rectangle(width=1.2, height=2.4).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(_p(bx1 - 0.6, QY))
    S.block_out = Line(_p(bx1, QY), _p(x2 - HX, QY)).set_stroke(BLUE, 5)
    S.block_l = VGroup(T("combinational", 28, BLUE), T("logic", 28, BLUE)).arrange(DOWN, buff=0.08)
    S.block_l.next_to(S.block, UP, buff=0.15)
    texs = ["Q_0", r"\overline{Q_0}", "Q_1", r"\overline{Q_1}", "Q_2", r"\overline{Q_2}"]
    S.block_stubs, S.block_labels = [], []
    for j, t in enumerate(texs):
        y = QY + 1.0 - 0.4 * j
        st = Line(_p(bx1 - 1.2 - 0.25, y), _p(bx1 - 1.2, y)).set_stroke(GREEN, 4)
        S.block_stubs.append(st)
        S.block_labels.append(MathTex(t, font_size=32, color=GREEN).next_to(st, LEFT, buff=0.08))
    S.all = [*S.ffs, *S.names, S.bus, *S.jdots, S.clk_l, *S.risers, *S.q_labels, S.loop, xg,
             *S.xor_stubs, *S.xor_labels, S.block, S.block_out, S.block_l, *S.block_stubs, *S.block_labels]
    S.add(*S.all)
    S.q_spot = lambda i: _p(FF_X[i] + 0.92, QY + 0.3)
    S.d_spot = lambda i: _p(FF_X[i] - 0.92, QY + 0.3)

    def clk_paths():
        return ([S.bus.copy().set_stroke(YELLOW, 10)],
                [f.clk_w.copy().set_stroke(YELLOW, 10) for f in S.ffs])
    S.clk_paths = clk_paths
    return S


def clock_source():
    """The 1 Hz source at the bottom of the CLK drop: circle with a square wave, "1 Hz" (GOLD) under CLK."""
    c = Circle(radius=0.28).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(DROP_X, DROP_Y - 0.28))
    w = 0.13
    wave = poly([(-2 * w, -w), (-w, -w), (-w, w), (w, w), (w, -w), (2 * w, -w)], YELLOW, 3).move_to(c)
    hz = T("1 Hz", 30, GOLD)
    return VGroup(c, wave), hz



# ---- this lecture's placement of the counter (ch1_s4 / ch1_s6 copy it) ----------------------
SC = 0.86                                  # whole circuit scale
BOTTOM_Y = -3.4                            # circuit bottom (clock source) on screen
READ_X, READ_Y = -3.3, 2.85                # readout row centre
TRAIL_X0, TRAIL_DX, TRAIL_N = 0.2, 0.8, 8  # trail slots: x = TRAIL_X0 + k * TRAIL_DX, at READ_Y
TAG_SIZE = 30


def hook_counter():
    """Returns (S, chains, src, M): L6's counter with LEDs and 1 Hz source, scaled SC and placed;
    M(p) maps an L6 screen point to this placement. Parts are separate mobjects: show them with
    counter_parts(S, chains, src)."""
    S = sync_counter()
    chains = [led_chain(i, on=True) for i in range(3)]
    src, _hz = clock_source()
    W = VGroup(S, *chains, *[ch.ohm for ch in chains], src)
    c0 = W.get_center()
    W.scale(SC)
    W.shift(np.array([0.0, BOTTOM_Y - W.get_bottom()[1], 0.0]) - np.array([W.get_center()[0], 0, 0]))
    c1 = W.get_center()
    # small labels back to their L6 on-screen size (>= 28), each about its own centre
    for m in [*[x for f in S.ffs for x in (f.d_l, f.q_l, f.qb_l)], *S.names]:
        m.scale(1 / SC)
    S.block_l.scale(1 / SC).next_to(S.block, UP, buff=0.13)
    for ch in chains:
        r = ch.ohm.get_right()
        ch.ohm.scale(1 / SC).move_to(r, aligned_edge=RIGHT)

    def M(p):
        return c1 + (np.array(p, dtype=float) - c0) * SC
    return S, chains, src, M


def counter_parts(S, chains, src):
    return [*S.all, *[m for ch in chains for m in (ch.res, ch.link, ch.led, ch.ohm)], src]


def freq_tag(text, S):
    return T(text, TAG_SIZE, YELLOW).next_to(S.clk_l, RIGHT, buff=0.3)


def readout(n, dec_color=GOLD):
    lab = MathTex(r"Q_2\,Q_1\,Q_0", font_size=40, color=GREEN)
    eq1 = MathTex("=", font_size=40)
    bits = Mono(f"{n:03b}", 44, GREEN)
    eq2 = MathTex("=", font_size=40)
    dec = T(str(n), 48, dec_color)
    VGroup(lab, eq1, bits, eq2, dec).arrange(RIGHT, buff=0.25).move_to(_p(READ_X, READ_Y))
    return lab, eq1, bits, eq2, dec


def trail_digit(v, color, k):
    return T(str(v), 42, color).move_to(_p(TRAIL_X0 + k * TRAIL_DX, READ_Y))


def _bits(n):
    return [(n >> i) & 1 for i in range(3)]      # [Q0, Q1, Q2]
# =============================================================================================


from lib.titles import title_card  # noqa: E402


def chip(label, w=3.4, h=1.6, n_pins=5):
    body = RoundedRectangle(corner_radius=0.12, width=w, height=h).set_stroke(DIM, 4).set_fill(BG, 0)
    pins = []
    for j in range(n_pins):
        x = -w / 2 + (j + 0.5) * w / n_pins
        pins.append(Line(_p(x, h / 2), _p(x, h / 2 + 0.25)).set_stroke(DIM, 4))
        pins.append(Line(_p(x, -h / 2), _p(x, -h / 2 - 0.25)).set_stroke(DIM, 4))
    notch = Dot(_p(-w / 2 + 0.25, h / 2 - 0.25), radius=0.07, color=DIM)
    lab = T(label, 36, DIM)
    g = VGroup(body, *pins, notch, lab)
    g.body, g.pins, g.notch, g.lab = body, pins, notch, lab
    return g


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ helpers
    def set_state(self, n, dec_color=GOLD):
        """A real counter changes at once: bits, decimal, LEDs and Q risers switch in one frame."""
        S = self.S
        nb = Mono(f"{n:03b}", 44, GREEN).move_to(self.r_bits)
        nd = T(str(n), 48, dec_color).move_to(self.r_dec)
        self.remove(self.r_bits, self.r_dec)
        self.add(nb, nd)
        self.r_bits, self.r_dec = nb, nd
        for ch, v in zip(self.chains, _bits(n)):
            if v:
                ch.led.set_stroke(GREEN, 3).set_fill(GREEN, 0.9)
            else:
                ch.led.set_stroke(DIM, 3).set_fill(BG, 0)
        for r, v in zip(S.risers, _bits(n)):
            r.set_stroke(opacity=1 if v else LOW)
        self.n = n

    def push(self, v, color=GOLD):
        if len(self.trail) == TRAIL_N:
            old = self.trail.pop(0)
            self.remove(old)
            for d in self.trail:
                d.shift(TRAIL_DX * LEFT)
        d = trail_digit(v, color, len(self.trail))
        self.add(d)
        self.trail.append(d)

    def tick(self, n, rt, dec_color=GOLD, trail=True, extra=()):
        self.set_state(n, dec_color)
        if trail:
            self.push(n, dec_color)
        bus_p, _ = self.S.clk_paths()
        self.play(VShowPassingFlash(bus_p[0], time_width=0.8), *extra, run_time=rt)

    # ------------------------------------------------------------------ c1.hook.1
    def clip1(self):
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · How fast can the clock tick?")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole

            # {counter}: L6's synchronous counter returns, showing 7 (all lights on)
            S, chains, src, M = hook_counter()
            self.S, self.chains, self.src, self.M = S, chains, src, M
            parts = counter_parts(S, chains, src)
            c.wait_until("counter")
            sweep_clear(self, *[time_span(FadeIn(m), 0.5, 1.7) for m in parts], run_time=1.7)
            self.tag = freq_tag("1 Hz", S)
            self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec = readout(7)
            self.trail = []
            self.n = 7
            self.play(*appear(self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec, shift=None, lag=0.1),
                      *during(appear(self.tag, shift=None), 0.3, 1.0),
                      run_time=min(1.2, c.until("together")))  # early: the readout and the 1 Hz tag

            # {together}: one rising edge along CLK, all three flip-flops change at once (7 -> 0)
            c.wait_until("together")
            bus_p, pins = S.clk_paths()
            self.play(VShowPassingFlash(bus_p[0], time_width=0.8), run_time=1.0)
            self.set_state(0)
            self.play(*[VShowPassingFlash(p, time_width=1.0) for p in pins],
                      *[FlashAround(f.box, color=YELLOW, time_width=1.5, buff=0.1) for f in S.ffs],
                      run_time=1.2)

            # {count}: zero, one, two, three
            c.wait_until("zero")
            self.play(*flash([self.r_dec], color=GOLD, time_width=1.5, buff=0.12), run_time=0.6)
            words = (("one", 0), ("two", 0), ("three", 1))
            for n, (w, nth) in enumerate(words, start=1):
                c.wait_until(w, nth=nth)
                # each value lands on its word: the edge flash never delays the next one
                nxt = c.until(words[n][0], nth=words[n][1], floor=0.2) if n < 3 else 0.5
                self.tick(n, min(0.5, 0.9 * nxt), trail=False)

    # ------------------------------------------------------------------ c1.hook.2
    def clip2(self):
        S = self.S
        with self.say("c1.hook.2") as c:
            # {faster}: the clock source flashes; the trail starts beside the readout
            first = trail_digit(self.n, GOLD, 0)
            self.play(FlashAround(self.src, color=YELLOW, time_width=1.5, buff=0.12),
                      *during(appear(first, shift=None), 0.3, 1.0), run_time=1.2)
            self.trail = [first]
            c.wait_until("thousand")
            new = freq_tag("1 kHz", S)
            self.play(*swap(self.tag, new), run_time=0.8)
            self.tag = new
            while c.until("million", floor=0) > 0.35:
                self.tick((self.n + 1) % 8, 0.3)
            c.wait_until("million")
            new = freq_tag("1 MHz", S)
            self.play(*swap(self.tag, new), run_time=0.8)
            self.tag = new
            while c.until("still right", floor=0) > 0.2 or self.n != 7:
                self.tick((self.n + 1) % 8, 0.15)
            # {still right}: every value one more than the last
            self.play(*flash([VGroup(*self.trail)], color=GOLD, time_width=1.5, buff=0.15),
                      run_time=min(1.2, c.until("wrong")))

            # {wrong}: the tag keeps climbing, digits blurring upwards
            c.wait_until("wrong")
            avail = c.until("wrong2")
            for txt in ("10 MHz", "100 MHz", "??? MHz"):
                new = freq_tag(txt, S)
                self.play(*swap(self.tag, new, shift=0.35 * UP), run_time=0.13 * avail)
                self.tag = new
            for n in range(4):
                self.tick(n, 0.1 * avail)

            # {wrong2}: after three comes 0, 5, 2, 7, in RED; D2's logic block flickers
            for v, w in ((0, "zero"), (5, "five"), (2, "two"), (7, "seven")):
                c.wait_until(w)
                self.tick(v, 0.7, dec_color=RED,
                          extra=[FlashAround(S.block, color=RED, time_width=1.5, buff=0.08),
                                 S.block.animate(rate_func=there_and_back).set_stroke(RED, 6)])

            # {same}: nothing changed but the clock: only the tag pulses
            c.wait_until("same")
            self.play(FlashAround(self.tag, color=YELLOW, time_width=1.5, buff=0.12),
                      self.tag.animate(rate_func=there_and_back).scale(1.25), run_time=1.5)

    # ------------------------------------------------------------------ c1.hook.3
    def clip3(self):
        S, M = self.S, self.M
        with self.say("c1.hook.3") as c:
            # {question}: the counter dims; a "?" over its CLK line
            q = T("What sets the fastest clock?", 48, FG).move_to(_p(0, READ_Y))
            mark = T("?", 72, YELLOW).move_to(M(_p(1.5, -1.6)))
            board = [m for m in self.mobjects]
            self.play(*disappear(self.r_lab, self.r_eq1, self.r_bits, self.r_eq2, self.r_dec, *self.trail),
                      *during(set_alpha([m for m in board if m not in (self.r_lab, self.r_eq1, self.r_bits,
                                                                        self.r_eq2, self.r_dec, *self.trail)],
                                        DIMMED), 0.2, 1.0),
                      run_time=1.2)
            self.play(*appear(q, shift=None), *during(appear(mark), 0.3, 1.0), run_time=1.3)

            # {road}: three chips, the lecture's road
            chips = [chip("timing rules"), chip("metastability"), chip("parallelism")]
            for ch, x in zip(chips, (-4.0, 0.0, 4.0)):
                ch.move_to(_p(x, -0.2))
            c.wait_until("road")
            self.play(q.animate.move_to(_p(0, 2.7)),
                      *[FadeOut(m) for m in self.mobjects if m is not q], run_time=1.0)
            self.play(*appear(*chips, shift=None, lag=0.2), run_time=1.2)  # early: the road shown whole, then walked
            cols = (YELLOW, RED, GREEN)
            for ch, col, cue in zip(chips, cols, ("timing", "meta", "parallel")):
                c.wait_until(cue, own_word=ch.lab)
                self.play(*recolor([ch.body, *ch.pins, ch.notch, ch.lab], col),
                          FlashAround(ch, color=col, time_width=1.5, buff=0.15), run_time=0.9)

            # {start}: first chip stays lit, "Part 1 · the set-up rule" under it
            part = T("Part 1 · the set-up rule", 36, YELLOW)
            part.next_to(chips[0], DOWN, buff=0.45).align_to(chips[0], LEFT)
            c.wait_until("start")
            self.play(*set_alpha(chips[1:], DIMMED), run_time=1.0)
            c.wait_until(own_word=part)
            self.play(*appear(part), run_time=1.0)
            c.wait_until()
            self.wait(2.0)
