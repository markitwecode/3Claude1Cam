"""Chapter 1, scene 5: from the RS latch to the D latch (gated inputs, EN, the danger, D + inverter). Clips c1.dlatch.1 – c1.dlatch.4."""
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


# =============================================================================================
# Chapter 1 gate drawings (owned here; s3–s7 copy this block verbatim).
#   Wires: neutral WIRE (FG) = value not shown; ON (GREEN, bright) = 1; OFF (DIM) = 0.
#   light(w, v) -> animation that lights a wire (or wire group) to logic value v.
#   Gates are VGroups with .body .bubble (or None) .num (or None), .inp(i) and .out() points
#   (they follow scaling/moving). Built at unit size; 1.2 tall.
# =============================================================================================
WIRE, ON, OFF = FG, GREEN, DIM
WIRE_W = 4
GATE_COLOR = BLUE


def _p(x, y):
    return np.array([x, y, 0.0])


def wire(*pts, color=WIRE):
    """Polyline wire through (x, y) points."""
    w = VMobject().set_points_as_corners([_p(*p) if len(p) == 2 else np.array(p) for p in pts])
    return w.set_stroke(color, WIRE_W)


def junction(x, y, color=WIRE):
    return Dot(_p(x, y), radius=0.07, color=color)


def wire_color(v):
    return ON if v else OFF


def light(w, v=None, color=None):
    """Animation: wire (or VGroup of wires and junction dots) to value v (1 bright, 0 dim),
    or to `color` (e.g. WIRE for neutral)."""
    return w.animate.set_color(color if color is not None else wire_color(v))


class Gate(VGroup):
    def __init__(self, body, ins, out, bubble=None, num=None, num_at=(-0.1, 0.0), color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body, self.bubble = body, bubble
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        if bubble is not None:
            bubble.set_stroke(color, 4).set_fill(BG, 1)
            self.add(bubble)
        self.num = None
        if num is not None:
            self.num = T(str(num), size=28, color=DIM).move_to(_p(*num_at))
            self.add(self.num)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def nor_gate(num=None, color=GATE_COLOR):
    """Distinctive-shape NOR (OR body + output bubble), 1.6 wide x 1.2 tall, centred at ORIGIN.
    inp(0) top input (y +0.3), inp(1) bottom (y -0.3), out() right of the bubble (0.9, 0)."""
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    bubble = Circle(radius=0.1).move_to(_p(0.8, 0))
    return Gate(b, [(-0.56, 0.3), (-0.56, -0.3)], (0.9, 0.0), bubble=bubble, num=num, color=color)


def and_gate(num=None, color=GATE_COLOR):
    """AND (flat back, round front), 1.3 wide x 1.2 tall, centred near ORIGIN.
    inp(0) top (-0.7, 0.3), inp(1) bottom (-0.7, -0.3), out() (0.6, 0)."""
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), num=num, num_at=(-0.15, 0.0), color=color)


def not_gate(color=GATE_COLOR):
    """Inverter: triangle + output bubble, pointing right. inp(0) (-0.4, 0), out() (0.46, 0)."""
    tri = Polygon(_p(-0.4, 0.35), _p(-0.4, -0.35), _p(0.3, 0.0))
    bubble = Circle(radius=0.08).move_to(_p(0.38, 0))
    return Gate(tri, [(-0.4, 0.0)], (0.46, 0.0), bubble=bubble, color=color)


class RSLatch(VGroup):
    """Slide p. 79 NOR RS latch. Parts:
    .g1 (top NOR, "1"), .g2 (bottom NOR, "2"), .gates
    .r .s            input wires (R into g1's top input, S into g2's bottom input)
    .q  = VGroup(.q_out, .fq, .q_dot)    Q node: g1 output line + feedback into g2's top input
    .qb = VGroup(.qb_out, .fqb, .qb_dot) Q-bar node: g2 output line + feedback into g1's bottom input
    .wires = {"r", "s", "q", "qb"} (light(latch.wires[k], v))
    .lab_r .lab_s (BLUE), .lab_q .lab_qb (GREEN), .labels
    Unscaled it is 5.4 wide x 3.6 tall, centred at ORIGIN (wire ends at x = +-2.2)."""

    def __init__(self, labels=True):
        super().__init__()
        g1, g2 = nor_gate(1).shift(1.2 * UP), nor_gate(2).shift(1.2 * DOWN)
        self.g1, self.g2, self.gates = g1, g2, VGroup(g1, g2)
        a1, b1, a2, b2 = g1.inp(0), g1.inp(1), g2.inp(0), g2.inp(1)
        o1, o2 = g1.out(), g2.out()
        xl, xr, xt, xf = -2.2, 2.2, 1.4, -1.2
        self.r = wire((xl, a1[1]), tuple(a1[:2]))
        self.s = wire((xl, b2[1]), tuple(b2[:2]))
        self.q_out = wire(tuple(o1[:2]), (xr, o1[1]))
        self.qb_out = wire(tuple(o2[:2]), (xr, o2[1]))
        self.fq = wire((xt, o1[1]), (xt, 0.5), (xf, -0.5), (xf, a2[1]), tuple(a2[:2]))
        self.fqb = wire((xt, o2[1]), (xt, -0.5), (xf, 0.5), (xf, b1[1]), tuple(b1[:2]))
        self.q_dot, self.qb_dot = junction(xt, o1[1]), junction(xt, o2[1])
        self.q = VGroup(self.q_out, self.fq, self.q_dot)
        self.qb = VGroup(self.qb_out, self.fqb, self.qb_dot)
        self.wires = {"r": self.r, "s": self.s, "q": self.q, "qb": self.qb}
        self.add(self.r, self.s, self.q, self.qb, g1, g2)
        self.lab_r = MathTex("R", font_size=48, color=BLUE).next_to(self.r.get_start(), LEFT, buff=0.15)
        self.lab_s = MathTex("S", font_size=48, color=BLUE).next_to(self.s.get_start(), LEFT, buff=0.15)
        self.lab_q = MathTex("Q", font_size=48, color=GREEN).next_to(self.q_out.get_end(), RIGHT, buff=0.15)
        self.lab_qb = MathTex(r"\overline{Q}", font_size=48, color=GREEN).next_to(
            self.qb_out.get_end(), RIGHT, buff=0.15)
        self.labels = VGroup(self.lab_r, self.lab_s, self.lab_q, self.lab_qb)
        if labels:
            self.add(*self.labels)

    def end(self, key):
        """Outer end point of a terminal wire: 'r', 's' (left ends), 'q', 'qb' (right ends)."""
        return {"r": self.r.get_start(), "s": self.s.get_start(),
                "q": self.q_out.get_end(), "qb": self.qb_out.get_end()}[key]


def rs_latch(labels=True):
    """The chapter's RS latch at unit scale, centred at ORIGIN (see RSLatch)."""
    return RSLatch(labels=labels)


# hero placement used in s2 (and where s3 opens): rs_latch().scale(LATCH_SCALE).move_to(LATCH_POS)
LATCH_SCALE = 1.15
LATCH_POS = _p(-3.4, 0.15)


class DLatch(VGroup):
    """Slide p. 86 D latch: D (bottom left) straight into the S-side AND, through an inverter into
    the R-side AND; EN enters between the ANDs and branches to both; the ANDs feed rs_latch().
    Parts: .latch (RSLatch, its R/S labels dropped), .and_r (top), .and_s (bottom), .inv,
    .d (VGroup: D wire to the S-AND + junction + riser to the inverter), .dn (inverter out -> R-AND),
    .en (VGroup: EN wire, junction, branches), .lab_d .lab_en (BLUE), .wires {"d","dn","en","r","s","q","qb"}.
    Default: 9.3 wide x 4.2 tall at scale 1, centred at ORIGIN."""

    def __init__(self):
        super().__init__()
        L = RSLatch(labels=True)
        L.remove(L.lab_r, L.lab_s)
        self.latch = L
        rs, ss = L.r.get_start(), L.s.get_start()
        ar = and_gate()
        ar.shift(rs - ar.out())
        as_ = and_gate()
        as_.shift(ss - as_.out())
        self.and_r, self.and_s = ar, as_
        xd, xj, xe, xin = -6.2, -5.4, -4.1, ar.inp(0)[0]
        yt, yb = ar.inp(0)[1], as_.inp(1)[1]
        inv = not_gate().move_to(_p(-4.6, yt))
        self.inv = inv
        d_main = wire((xd, yb), (xin, yb))
        d_rise = wire((xj, yb), (xj, yt), tuple(inv.inp(0)[:2]))
        self.d = VGroup(d_main, d_rise, junction(xj, yb))
        self.dn = wire(tuple(inv.out()[:2]), (xin, yt))
        en_main = wire((xd, 0.0), (xe, 0.0))
        en_br = wire((xin, ar.inp(1)[1]), (xe, ar.inp(1)[1]), (xe, as_.inp(0)[1]), (xin, as_.inp(0)[1]))
        self.en = VGroup(en_main, en_br, junction(xe, 0.0))
        self.lab_d = MathTex("D", font_size=48, color=BLUE).next_to(_p(xd, yb), LEFT, buff=0.15)
        self.lab_en = MathTex(r"\mathrm{EN}", font_size=44, color=BLUE).next_to(_p(xd, 0), LEFT, buff=0.15)
        self.wires = {"d": self.d, "dn": self.dn, "en": self.en, **L.wires}
        self.add(self.d, self.dn, self.en, ar, as_, inv, L, self.lab_d, self.lab_en)
        self.move_to(ORIGIN)


def d_latch():
    """The chapter's D latch at unit scale, centred at ORIGIN (see DLatch)."""
    return DLatch()



# =============================================================================================
# Scene-only helpers
# =============================================================================================
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """rows: list of lists of strings ('$...' -> MathTex, else T). Column centres xs (or ('L', x)
    for left-aligned). Returns VGroup(header, *rows, lines) with .rows (incl. header), .lines."""
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            if s.startswith("$"):
                m = MathTex(s[1:], font_size=size, color=col)
            else:
                m = T(s, size=size * 0.82, color=col)
            x = xs[j]
            if isinstance(x, tuple):
                m.move_to(_p(x[1], -i * pitch), aligned_edge=LEFT)
                m.set_y(-i * pitch)
            else:
                m.move_to(_p(x, -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g



def toggle_switch(v=0):
    """Small input switch: BLUE pill with a knob (left + DIM = 0, right + GREEN = 1). Built at ORIGIN."""
    pill = RoundedRectangle(corner_radius=0.17, width=0.72, height=0.34).set_stroke(BLUE, 3).set_fill(BG, 1)
    knob = Circle(radius=0.11).set_stroke(width=0).set_fill(GREEN if v else DIM, 1)
    knob.move_to(_p(0.18 if v else -0.18, 0))
    sw = VGroup(pill, knob)
    sw.pill, sw.knob = pill, knob
    return sw


def flip(sw, v):
    """Animation list: the switch's knob slides to value v."""
    tgt = sw.pill.get_center() + _p(0.18 if v else -0.18, 0)
    return [sw.knob.animate.move_to(tgt).set_fill(GREEN if v else DIM, 1)]


def pulse(w, color=YELLOW):
    """A bright bump running along a copy of wire w."""
    return VShowPassingFlash(w.copy().set_stroke(color, 8), time_width=0.5)


HOP_R = 0.16   # wire-hop radius where D's riser crosses EN


def add_hop(D, r=HOP_R):
    """Redraw D's riser (D.d[1]) with a semicircular hop, bulging LEFT, where it crosses the EN
    wire (centre = riser x, EN y; from (x, y_en - r) to (x, y_en + r)), so it doesn't read as joined."""
    riser = D.d[1]
    p0, p_top, p_inv = riser.get_start(), _p(riser.get_start()[0], D.dn.get_end()[1]), D.inv.inp(0)
    x, y = p0[0], D.en[0].get_start()[1]
    arc = [_p(x + r * np.cos(a), y + r * np.sin(a)) for a in np.linspace(-PI / 2, -3 * PI / 2, 17)]
    riser.set_points_as_corners([p0, *arc, p_top, p_inv])
    return D


class DLatchBuild(NarratedScene):
    def construct(self):
        self.vals = {}
        D = add_hop(d_latch())
        self.D, self.L = D, D.latch
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.finish()

    # ---- value digits ---------------------------------------------------------------------
    def digit_pos(self, key):
        L = self.L
        return {"en": _p(-3.6, 0.33), "d": _p(-3.6, -1.5),
                "r": _p(0.45, 1.13), "s": _p(0.45, -1.17),
                "q": L.end("q") + _p(-0.42, 0.36), "qb": L.end("qb") + _p(-0.42, -0.36)}[key]

    def wire_of(self, key):
        D, L = self.D, self.L
        return {"en": D.en, "d": D.d, "r": L.r, "s": L.s, "q": L.q, "qb": L.qb}[key]

    def setv(self, key, v, color=GOLD, lit=True):
        """Anims: the terminal's digit becomes v (appear or swap) and its wire lights."""
        new = MathTex(str(v), font_size=44, color=color).move_to(self.digit_pos(key))
        old = self.vals.get(key)
        self.vals[key] = new
        anims = swap(old, new) if old is not None else appear(new, shift=None)
        if lit:
            anims.append(light(self.wire_of(key), v))
        return anims

    def make_valves(self):
        """Small copies of s4's valve (YELLOW ring, BLUE flap, hub) on each AND, built shut
        (flap vertical). self.valves = [(ring, flap, hub, ctr), ...]."""
        self.valves = []
        for g in (self.D.and_r, self.D.and_s):
            ctr = g.body.get_center() + 0.05 * RIGHT
            ring = Circle(radius=0.32).move_to(ctr).set_stroke(YELLOW, 3).set_fill(BG, 1).set_z_index(1)
            flap = Line(ctr + 0.27 * DOWN, ctr + 0.27 * UP).set_stroke(BLUE, 6).set_z_index(2)
            hub = Dot(ctr, radius=0.06, color=BLUE).set_z_index(3)
            self.valves.append((ring, flap, hub, ctr))

    def gates_shut(self, shut):
        """Anims: the valves rotate shut (flap across the path) or open (flap along it)."""
        ang = PI / 2 if shut else -PI / 2
        return [Rotate(flap, ang, about_point=ctr) for (_, flap, _, ctr) in self.valves]

    # ---- clips ----------------------------------------------------------------------------
    def clip1(self):
        D, L = self.D, self.L
        with self.say("c1.dlatch.1") as c:
            self.play(FadeIn(L), run_time=1.0)
            c.wait_until("ands")
            # R side: AND gate, its separate input wire with a switch, output label R
            a0 = D.and_r.inp(0)
            self.rin = wire((D.d[0].get_start()[0], a0[1]), (a0[0], a0[1]))
            self.sin = D.d[0]
            self.sw_r = toggle_switch(0).move_to(_p(-4.55, D.and_r.inp(0)[1]))
            self.sw_s = toggle_switch(0).move_to(_p(-4.55, D.and_s.inp(1)[1]))
            self.lab_r = MathTex("R", font_size=44, color=BLUE)
            self.lab_r.move_to(_p(0.05, 1.98), aligned_edge=LEFT).set_y(1.98)
            self.lab_s = MathTex("S", font_size=44, color=BLUE)
            self.lab_s.move_to(_p(0.05, -2.02), aligned_edge=LEFT).set_y(-2.02)
            self.play(GrowFromCenter(D.and_r), Create(self.rin), FadeIn(self.sw_r),
                      *appear(self.lab_r), run_time=1.5)
            c.wait_until("another")
            self.play(GrowFromCenter(D.and_s), Create(self.sin), FadeIn(self.sw_s),
                      *appear(self.lab_s), run_time=1.5)
            c.wait_until("en")
            self.play(Create(D.en[0]), Create(D.en[1]), FadeIn(D.en[2]), run_time=1.6)
            c.wait_until("called enable")
            self.play(*appear(D.lab_en), run_time=1.0)
            c.wait_until("clk")
            self.clk = T("could be\nthe clock", size=32, color=YELLOW, line_spacing=0.9)
            self.clk.move_to(_p(-3.1, -0.85))
            self.play(*appear(self.clk), run_time=1.0)

    def clip2(self):
        D, L = self.D, self.L
        with self.say("c1.dlatch.2") as c:
            # EN = 0: both valves shut
            self.make_valves()
            vparts = [m for (ring, flap, hub, _) in self.valves for m in (ring, flap, hub)]
            self.play(*self.setv("en", 0), *[FadeIn(m) for m in vparts],
                      light(self.rin, 0), light(self.sin, 0), run_time=1.5)
            c.wait_until("zeros")
            self.play(*flip(self.sw_s, 1), light(self.sin, 1), run_time=1.0)
            self.play(pulse(self.sin), *flash([D.and_s.body], color=RED, time_width=1.5),
                      *disappear(self.clk), run_time=1.5)
            self.play(*self.setv("r", 0), *self.setv("s", 0), run_time=1.2)
            self.state = T("hold", size=44, color=FG).move_to(_p(L.get_center()[0], -2.75))
            c.wait_until("hold condition")
            self.play(*appear(self.state), run_time=1.0)
            c.wait_until("frozen")
            self.play(*self.setv("q", 0), *self.setv("qb", 1), run_time=1.2)
            self.play(*flash([self.vals["q"], self.vals["qb"]], color=YELLOW, time_width=1.5), run_time=1.3)
            c.wait_until("on")
            self.play(*self.setv("en", 1), *self.gates_shut(False), run_time=1.5)
            c.wait_until("go straight through")
            self.play(time_span(pulse(self.sin), 0, 0.9), time_span(pulse(L.s), 0.6, 1.5),
                      *self.setv("s", 1), *disappear(self.state), run_time=1.5)
            self.play(*self.setv("qb", 0), *self.setv("q", 1),
                      VShowPassingFlash(L.fqb.copy().set_stroke(YELLOW, 8), time_width=0.4), run_time=1.2)
            c.wait_until("split")
            self.when = T("EN: when", size=34, color=YELLOW).move_to(_p(-3.1, -0.8))
            self.what = T("inputs: what", size=34, color=YELLOW).move_to(_p(-3.0, 2.65))
            c.wait_until("decides when")
            self.play(*appear(self.when), run_time=1.0)
            c.wait_until("the inputs decide")
            self.play(*appear(self.what), run_time=1.0)

    def clip3(self):
        D, L = self.D, self.L
        with self.say("c1.dlatch.3") as c:
            self.play(*flash([self.sw_r, self.sw_s], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("setting both of them to one")
            self.play(*flip(self.sw_r, 1), light(self.rin, 1), *disappear(self.when, self.what), run_time=1.0)
            self.play(time_span(pulse(self.rin), 0, 0.9), time_span(pulse(L.r), 0.6, 1.5),
                      *self.setv("r", 1), run_time=1.5)
            c.wait_until("illegal")
            self.play(*self.setv("q", 0, color=RED), *recolor([self.vals["qb"]], RED),
                      light(L.qb, 0), run_time=1.2)
            self.bad = MathTex(r"Q = \overline{Q} = 0", font_size=48, color=RED)
            self.bad.move_to(_p(L.get_center()[0], -2.75))
            c.wait_until("with cue")
            self.play(*appear(self.bad), run_time=1.0)
            self.play(FlashAround(self.bad, color=RED, time_width=1.5), run_time=1.5)
            self.ask = T("Can we make it impossible?", size=40, color=YELLOW).move_to(_p(0, 3.15))
            c.wait_until(own_word=self.ask)
            self.play(*appear(self.ask), run_time=1.0)

    def clip4(self):
        D, L = self.D, self.L
        with self.say("c1.dlatch.4") as c:
            # clear the danger: digits, red tag, question; wires neutral
            olds = [self.ask, self.bad, *self.vals.values(),
                    *[m for (ring, flap, hub, _) in self.valves for m in (ring, flap, hub)]]
            self.vals = {}
            c.wait_until("replace")
            self.play(*disappear(*olds, self.rin, self.sw_r, self.sw_s, lag=0.05),
                      *[light(w, color=WIRE) for w in (L.r, L.s, L.q, L.qb, D.en, self.sin)],
                      run_time=1.4)
            c.wait_until("called dee")
            self.play(*appear(D.lab_d), run_time=1.0)
            c.wait_until("direct")
            self.play(pulse(D.d[0]), *flash([D.and_s.body], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("inv")
            self.play(Create(D.d[1]), FadeIn(D.d[2]), GrowFromCenter(D.inv), run_time=1.3)
            self.play(Create(D.dn), run_time=0.7)
            # S = D, R = not D (with EN = 1)
            c.wait_until("comp")
            sD = MathTex("S = D", font_size=44, color=BLUE)
            sD.move_to(self.lab_s.get_left(), aligned_edge=LEFT)
            rD = MathTex(r"R = \overline{D}", font_size=44, color=BLUE)
            rD.move_to(self.lab_r.get_left(), aligned_edge=LEFT)
            self.play(*self.setv("en", 1), *self.dvals(0), run_time=1.2)
            c.wait_until("ess equals dee")
            self.play(*edit(self.lab_s, sD), run_time=1.2)
            self.lab_s = sD
            c.wait_until("and ar equals")
            self.play(*edit(self.lab_r, rD), run_time=1.4)
            self.lab_r = rD
            c.wait_until("never")
            self.play(*self.dvals(1), run_time=1.0)
            self.never = T("R and S never both 1", size=36, color=GREEN).move_to(_p(1.6, -3.0))
            c.wait_until(own_word=self.never)
            self.play(*self.dvals(0), run_time=1.0)
            self.play(*appear(self.never), run_time=1.0)
            c.wait_until("safe")
            rows = [["$S", "$R", "$Q'", r"$\overline{Q}'", "comment"],
                    ["$0", "$0", "$Q", r"$\overline{Q}", "hold"],
                    ["$0", "$1", "$0", "$1", "reset"],
                    ["$1", "$0", "$1", "$0", "set"],
                    ["$1", "$1", "$0", "$0", "illegal"]]
            tab = grid_table(rows, [0, 0.75, 1.9, 2.8, ("L", 3.75)], size=44, pitch=0.66,
                             seps=[1.32, 3.4], colors=[None, None, None, None, RED])
            tab.scale(0.8)
            row = tab.rows[4]
            strike = Line(row.get_left() + _p(-0.15, 0), row.get_right() + _p(0.15, 0)).set_stroke(RED, 5)
            card = RoundedRectangle(corner_radius=0.2, width=tab.width + 0.8, height=tab.height + 0.7)
            card.set_stroke(DIM, 2).set_fill(BG, 1)
            card.move_to(tab)
            VGroup(card, tab, strike).move_to(_p(-0.45, 0.05))
            digits = list(self.vals.values())
            self.vals = {}
            rest = [m for m in self.mobjects if m is not self.never and m not in digits]
            self.play(*during(disappear(*digits), 0, 0.5), *during(set_alpha(rest, DIMMED), 0, 0.6),
                      *during([FadeIn(card)], 0.3, 0.7),
                      *during(appear(tab, shift=None), 0.6, 1.0), run_time=1.6)  # early: a reminder table, read whole
            self.play(Create(strike), run_time=0.8)
            c.wait_until("remember to avoid it")
            self.play(*disappear(card, tab, strike), run_time=1.0)
            self.play(*set_alpha(rest, 1), run_time=1.0)

    def dvals(self, v):
        """Anims: D (with EN = 1) set to v: D digit, D and D-bar wires, R = not D, S = D."""
        return [*self.setv("d", v), light(self.D.dn, 1 - v), *self.setv("r", 1 - v), *self.setv("s", v),
                *self.setv("q", v), *self.setv("qb", 1 - v)]

    def finish(self):
        D, L = self.D, self.L
        self.wait(1.0)
        extra = [self.lab_r, self.lab_s, self.never, *self.vals.values()]
        self.play(*disappear(*extra, lag=0.05),
                  *[light(D.wires[k], color=WIRE) for k in ("d", "dn", "en", "r", "s", "q", "qb")], run_time=1.2)
        settle(self, D)
        self.wait(1.2)   # s6 opens on this exact shot: d_latch(), scale 1, at ORIGIN, wires neutral
