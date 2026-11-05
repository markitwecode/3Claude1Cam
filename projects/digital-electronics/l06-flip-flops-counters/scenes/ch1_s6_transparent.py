"""Chapter 1, scene 6: the D latch's table, transparent vs hold, its symbol, a switch demo and the
level-triggered waveform. Clips c1.transp.1 – c1.transp.5."""
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
# Scene-only helpers (grid_table copied from ch1_s2_rslatch.py)
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


# copied from ch1_s5_dlatch.py
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


def latch_symbol():
    """Slide p. 86 D-latch symbol: a tall BLUE box, D in on the left, Q out on the right, EN in
    from below through a small square on the box's bottom edge. Parts: .box .d_wire .lab_d
    .q_wire .lab_q .en_wire .square .lab_en; groups .d_part .q_part .en_part.
    6.2 wide x 4.2 tall at scale 1, box centred at ORIGIN (box 2.6 x 3.4)."""
    g = VGroup()
    box = Rectangle(width=2.6, height=3.4).set_stroke(GATE_COLOR, 4).set_fill(BG, 1)
    d_wire = wire((-3.1, 0.8), (-1.3, 0.8))
    q_wire = wire((1.3, 0.8), (3.1, 0.8))
    en_wire = wire((0, -2.5), (0, -1.7))
    square = Square(side_length=0.34).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -1.7))
    lab_d = MathTex("D", font_size=52, color=BLUE).move_to(_p(-0.85, 0.8))
    lab_q = MathTex("Q", font_size=52, color=GREEN).move_to(_p(0.85, 0.8))
    lab_en = MathTex(r"\mathrm{EN}", font_size=40, color=BLUE).move_to(_p(0, -0.95))
    g.box, g.d_wire, g.q_wire, g.en_wire, g.square = box, d_wire, q_wire, en_wire, square
    g.lab_d, g.lab_q, g.lab_en = lab_d, lab_q, lab_en
    g.d_part, g.q_part = VGroup(d_wire, lab_d), VGroup(q_wire, lab_q)
    g.en_part = VGroup(en_wire, square, lab_en)
    g.add(box, g.d_part, g.q_part, g.en_part)
    return g


def toggle(v):
    """Toggle switch: BLUE pill with a knob, right and BLUE for 1, left and DIM for 0.
    .track .knob .v; .knob_pos(v) gives the knob centre for value v."""
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(BLUE, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    g.track, g.knob, g.v = track, knob, v

    def knob_pos(val):
        return g.track.get_center() + (0.2 if val else -0.2) * RIGHT
    g.knob_pos = knob_pos
    knob.move_to(knob_pos(v)).set_fill(BLUE if v else DIM, 1)
    return g


def flip(sw, v):
    sw.v = v
    return sw.knob.animate.move_to(sw.knob_pos(v)).set_fill(BLUE if v else DIM, 1)


def led(on):
    """LED: GREEN ring, filled when lit."""
    c = Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    return l.animate.set_fill(GREEN, 0.9 if on else 0.0)


def latch_values(d, en, q):
    """Wire values of the D latch for inputs d (None = don't care), en and stored q (None = not shown)."""
    v = {"en": en}
    v["d"] = d
    v["dn"] = None if d is None else 1 - d
    v["r"] = 0 if (not en or d is None) else (1 - d)
    v["s"] = 0 if (not en or d is None) else d
    v["q"] = q
    v["qb"] = None if q is None else 1 - q
    return v


# Timing diagram (demo): 10 equal steps.
EN_SEQ = [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
D_SEQ = [1, 0, 0, 1, 1, 0, 0, 0, 1, 1]
Q_SEQ = [1, 1, 0, 1, 1, 0, 0, 0, 0, 0]
X0, STEP_W, TR_H = -4.4, 1.0, 0.6
ROW_Y = {"en": -0.6, "d": -1.75, "q": -2.9}       # while the circuit is above; final: +1.75
WAVE_UP = 1.75
TR_COL = {"en": BLUE, "d": BLUE, "q": GREEN}
SEQ = {"en": EN_SEQ, "d": D_SEQ, "q": Q_SEQ}


def trace_seg(key, k):
    """Step k of trace `key`: the vertical edge at the step's start (if the level changed) and
    the flat level across the step. Stroke 4, like clock_wave."""
    vals, y = SEQ[key], ROW_Y[key]
    lv = lambda b: y + (TR_H / 2 if b else -TR_H / 2)  # noqa: E731
    x = X0 + k * STEP_W
    pts = []
    if k > 0 and vals[k] != vals[k - 1]:
        pts.append([x, lv(vals[k - 1]), 0])
    pts += [[x, lv(vals[k]), 0], [x + STEP_W, lv(vals[k]), 0]]
    return VMobject().set_points_as_corners(pts).set_stroke(TR_COL[key], 4)


SC1 = 0.64
CIRC1_POS = _p(-3.65, 0.05)


class Transparent(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        # handoff: end holding the EN/D/Q waveform and its band (s7 opens with them on screen)

    # ---- helpers ------------------------------------------------------------------------
    def light_state(self, dl, vals):
        """Anims lighting dl's wires to vals (only the wires whose value changes)."""
        anims = []
        for k, v in vals.items():
            if self.wv.get(k, "unset") != v:
                anims.append(light(dl.wires[k], v, color=WIRE if v is None else None))
                self.wv[k] = v
        return anims

    def demo_step(self, k, keys=("en", "d", "q"), run_time=1.0, extra=(), extra_span=(0.0, 0.5)):
        """Draw step k of the given traces (after `extra`, the switch/LED/wire changes)."""
        segs = [trace_seg(key, k) for key in keys]
        anims = [Create(s, rate_func=linear) for s in segs]
        if extra:
            self.play(*during(list(extra), *extra_span), *during(anims, 0.35, 1.0), run_time=run_time)
        else:
            self.play(*anims, run_time=run_time)
        settle(self, self.wave, add=segs)
        for key, s in zip(keys, segs):
            self.segs[key][k] = s

    def set_inputs(self, d=None, en=None, q=None):
        """Anims: move switches / LEDs / wires to the new demo state."""
        anims = []
        if d is not None and d != self.sw_d.v:
            anims.append(flip(self.sw_d, d))
        if en is not None and en != self.sw_en.v:
            anims.append(flip(self.sw_en, en))
        if q is not None and q != self.led_q.on:
            anims += [set_led(self.led_q, q), set_led(self.led_qb, 1 - q)]
        self.state.update({k: v for k, v in (("d", d), ("en", en), ("q", q)) if v is not None})
        s = self.state
        anims += self.light_state(self.dl, latch_values(s["d"], s["en"], s["q"]))
        return anims

    # ---- clip 1: the table, row by row, the circuit showing each row --------------------
    def clip1(self):
        dl = add_hop(d_latch())
        self.dl, self.wv = dl, {}
        self.add(dl)
        rows = [["$D", r"$\mathrm{EN}", "$Q'", r"$\overline{Q}'", "comment"],
                ["$X", "$0", "$Q", r"$\overline{Q}", "RS hold"],
                ["$0", "$1", "$0", "$1", "RS reset"],
                ["$1", "$1", "$1", "$0", "RS set"]]
        tab = grid_table(rows, [0, 0.9, 2.05, 2.95, ("L", 3.8)], size=46, pitch=0.78,
                         seps=[1.48, 3.5])
        tab.shift(_p(0.0, 1.22))
        tab.shift((6.55 - tab.get_right()[0]) * RIGHT)
        self.tab = tab
        with self.say("c1.transp.1") as c:
            self.play(dl.animate.scale(SC1).move_to(CIRC1_POS), run_time=1.5)
            self.play(*appear(tab.rows[0], shift=None), FadeIn(tab.lines),
                      dl.latch.g1.num.animate.set_opacity(0), dl.latch.g2.num.animate.set_opacity(0),
                      run_time=1.0)
            c.wait_until("hold")
            self.play(*appear(tab.rows[1]),  # early: table row, read across the sentence
                      *self.light_state(dl, latch_values(None, 0, None)), run_time=1.2)
            c.wait_until("don't care")
            self.play(*flash([tab.rows[1][0]]), run_time=1.2)
            c.wait_until("keeps its value")
            self.play(*flash([tab.rows[1][2], tab.rows[1][3]]), run_time=1.5)
            c.wait_until("reset")
            self.play(*appear(tab.rows[2]),  # early: table row, read across the sentence
                      *self.light_state(dl, latch_values(0, 1, 0)), run_time=1.5)
            c.wait_until("cue prime is zero")
            self.play(*flash([tab.rows[2][2], tab.rows[2][3]]), run_time=1.5)
            c.wait_until("set")
            self.play(*appear(tab.rows[3]),  # early: table row, read across the sentence
                      *self.light_state(dl, latch_values(1, 1, 1)), run_time=1.5)
            c.wait_until("cue prime is one")
            self.play(*flash([tab.rows[3][2], tab.rows[3][3]]), run_time=min(1.5, c.until()))

    # ---- clip 2: read it, transparent, two modes ----------------------------------------
    def clip2(self):
        dl, tab = self.dl, self.tab
        l1 = T("See Q follows D input provided EN=1.", size=36, color=DIM)
        l2 = T("If EN=0, Q maintains previous state", size=36, color=DIM)
        read = VGroup(l1, l2).arrange(DOWN, buff=0.3).move_to(_p(0, -2.65))
        with self.say("c1.transp.2") as c:
            self.play(*appear(l1, shift=None), run_time=0.8)  # early: the slide's line, lit half by half next
            self.play(*appear(l2, shift=None), run_time=0.8)  # early: the slide's line, lit half by half next
            c.wait_until("follow")
            self.play(l1.animate.set_color(FG), FlashUnder(l1, color=YELLOW, run_time=1.5),
                      *set_alpha([tab.rows[1]], DIMMED), run_time=1.5)
            c.wait_until("keep")
            self.play(l2.animate.set_color(FG), FlashUnder(l2, color=YELLOW, run_time=1.5),
                      *set_alpha([tab.rows[1]], 1), *set_alpha([tab.rows[2], tab.rows[3]], DIMMED),
                      run_time=1.5)
            c.wait_until("name")
            sweep_clear(self, dl.animate.scale(0.8 / SC1).move_to(_p(0, 0.55)), keep=[dl], run_time=1.6)
            title = T("transparent", size=56, color=YELLOW).move_to(_p(0, 3.15))
            self.play(*appear(title), run_time=1.0)
            mini_d = MathTex("D", font_size=48, color=BLUE)
            mini_q = MathTex("Q", font_size=48, color=GREEN)
            mini_w = Line(_p(-1.9, -2.35), _p(1.9, -2.35)).set_stroke(YELLOW, 5)
            mini_d.next_to(mini_w, LEFT, buff=0.2)
            mini_q.next_to(mini_w, RIGHT, buff=0.2)
            c.wait_until("whatever you put")
            wires_ = [dl.d[0], dl.latch.s, dl.latch.fqb, dl.latch.q_out]
            flashes = []
            n = len(wires_)
            for i, w in enumerate(wires_):
                fl = VShowPassingFlash(w.copy().set_stroke(YELLOW, 9), time_width=0.6)
                flashes.append(time_span(fl, 3.2 * i / n, 3.2 * (i + 1) / n))
            self.play(*flashes, *during([*appear(mini_d, mini_q, shift=None), Create(mini_w)], 0.55, 1.0),
                      run_time=3.2)
            m1 = T("transparent mode: EN = 1", size=38, color=FG).move_to(_p(0, -2.2))
            m2 = T("hold mode: EN = 0", size=38, color=FG).move_to(_p(0, -2.95))
            m1.align_to(m2, LEFT)
            VGroup(m1, m2).move_to(_p(0, -2.6))
            c.wait_until("transparent while")
            self.play(*swap(VGroup(mini_d, mini_w, mini_q), m1), run_time=1.2)
            c.wait_until("holding while")
            self.play(*appear(m2), run_time=min(1.0, c.until()))
        self.title, self.m1, self.m2 = title, m1, m2

    # ---- clip 3: the symbol ------------------------------------------------------------
    def clip3(self):
        dl = self.dl
        sym = latch_symbol().scale(1.15).shift(0.45 * UP)
        self.sym = sym
        with self.say("c1.transp.3") as c:
            self.play(*during(disappear(self.title), 0, 0.4),
                      *during([FadeOut(dl, scale=0.35, target_position=sym.box.get_center())], 0.0, 0.5),
                      *during([GrowFromCenter(sym.box)], 0.45, 1.0), run_time=1.8)
            c.wait_until("going in")
            self.play(Create(sym.d_wire), *appear(sym.lab_d, shift=None), run_time=1.0)
            c.wait_until("coming out")
            self.play(Create(sym.q_wire), *appear(sym.lab_q, shift=None), run_time=1.0)
            c.wait_until("from below")
            self.play(*during(disappear(self.m1, self.m2), 0, 0.4),
                      *during([Create(sym.en_wire)], 0.4, 0.7),
                      *during([FadeIn(sym.square), *appear(sym.lab_en, shift=None)], 0.65, 1.0),
                      run_time=1.6)
            lab = T("level-triggered", size=38, color=YELLOW)
            lab.move_to(sym.square.get_center() + _p(2.75, -0.75))
            arr = Arrow(lab.get_left() + 0.1 * LEFT, sym.square.get_corner(DR), buff=0.08,
                        stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.3)
            c.wait_until("square")
            self.play(sym.square.animate.set_stroke(YELLOW, 4),
                      FlashAround(sym.square, run_time=2, time_width=1.5, buff=0.12), run_time=2.0)
            c.wait_until(own_word=lab)
            self.play(*appear(lab, shift=None), GrowArrow(arr), run_time=1.2)
        self.sym_lab = VGroup(lab, arr)

    # ---- clip 4: the demo, part 1 -------------------------------------------------------
    def clip4(self):
        sym = self.sym
        dl = add_hop(d_latch()).scale(0.7).move_to(_p(-0.5, 2.0))
        self.dl, self.wv = dl, {}
        self.sw_d = toggle(1).next_to(dl.lab_d, LEFT, buff=0.3)
        self.sw_en = toggle(0).next_to(dl.lab_en, LEFT, buff=0.3)
        self.led_q = led(1).next_to(dl.latch.lab_q, RIGHT, buff=0.3)
        self.led_qb = led(0).next_to(dl.latch.lab_qb, RIGHT, buff=0.3)
        self.led_qb.set_x(self.led_q.get_x())
        self.state = {"d": 1, "en": 0, "q": 1}
        self.wave = VGroup()
        self.segs = {k: [None] * 10 for k in SEQ}
        labs = VGroup(*[MathTex(s, font_size=44, color=TR_COL[k]).move_to(_p(X0 - 0.75, ROW_Y[k]))
                        for k, s in (("en", r"\mathrm{EN}"), ("d", "D"), ("q", "Q"))])
        self.tr_labs = labs
        hold = T("hold", size=38, color=YELLOW)
        hold.next_to(VGroup(self.led_q, self.led_qb), RIGHT, buff=0.45)
        self.hold = hold
        for g in (dl.latch.g1, dl.latch.g2):
            g.remove(g.num)
        with self.say("c1.transp.4") as c:
            c.wait_until("in a simulator")
            self.play(*during(disappear(sym, self.sym_lab), 0, 0.45),
                      *during([FadeIn(dl, scale=0.4)], 0.45, 1.0), run_time=1.8)
            c.wait_until("switches")
            self.play(FadeIn(self.sw_d), FadeIn(self.sw_en), run_time=1.0)
            c.wait_until("lights")
            self.play(FadeIn(self.led_q), FadeIn(self.led_qb), run_time=1.0)
            c.wait_until("setup")
            # faint dashed low-level baselines, so a flat trace reads as high or low
            bases = [DashedLine(_p(X0, ROW_Y[k] - TR_H / 2), _p(X0 + 10 * STEP_W, ROW_Y[k] - TR_H / 2),
                                dash_length=0.08).set_stroke(DIM, 2, opacity=0.6).set_z_index(-1)
                     for k in ("en", "d", "q")]
            self.play(*appear(*labs, lag=0.3), *[FadeIn(b) for b in bases],
                      *self.light_state(dl, latch_values(1, 0, 1)),
                      FlashAround(self.led_q, run_time=1.5, color=GREEN), run_time=1.5)
            settle(self, self.wave, add=bases)
            self.demo_step(0, run_time=1.2)
            c.wait_until("dflip")
            self.demo_step(1, run_time=1.4, extra=self.set_inputs(d=0))
            c.wait_until("nothing")
            self.play(*appear(hold), *flash([self.led_q, self.led_qb], color=GREEN), run_time=1.5)
            c.wait_until("enup")
            self.demo_step(2, keys=("en", "d"), run_time=1.5, extra=self.set_inputs(en=1))
            c.wait_until("jump")
            tr = T("transparent", size=38, color=YELLOW).move_to(hold, aligned_edge=LEFT)
            self.demo_step(2, keys=("q",), run_time=min(1.5, c.until()),
                           extra=[*self.set_inputs(q=0), *swap(hold, tr)], extra_span=(0.0, 0.6))
            self.tag = tr

    # ---- clip 5: wiggle, freeze, the waveform -----------------------------------------
    def clip5(self):
        with self.say("c1.transp.5") as c:
            self.demo_step(3, run_time=1.0, extra=self.set_inputs(d=1, q=1))
            self.demo_step(4, run_time=0.6)
            c.wait_until("then down again")
            self.demo_step(5, run_time=1.0, extra=self.set_inputs(d=0, q=0))
            self.demo_step(6, run_time=0.6)
            c.wait_until("tracks")
            qd = VGroup(*[self.segs[k][i] for k in ("d", "q") for i in range(3, 7)])
            self.play(FlashAround(qd, run_time=1.8, time_width=1.5, buff=0.15), run_time=1.8)
            c.wait_until("endown")
            self.demo_step(7, run_time=1.4, extra=self.set_inputs(en=0))
            c.wait_until("freeze")
            self.play(*swap(self.tag, self.hold), FlashAround(self.segs["q"][7], run_time=1.2, buff=0.15),
                      run_time=1.2)
            c.wait_until("ignore")
            self.demo_step(8, run_time=1.2, extra=self.set_inputs(d=1))
            self.demo_step(9, run_time=0.8)
            c.wait_until("wave")
            sweep_clear(self, self.wave.animate.shift(WAVE_UP * UP),
                        self.tr_labs.animate.shift(WAVE_UP * UP), keep=[self.wave, self.tr_labs],
                        run_time=1.8)
            band = Rectangle(width=5 * STEP_W, height=3.4).set_stroke(width=0).set_fill(YELLOW, 0.13)
            band.move_to(_p(X0 + 4.5 * STEP_W, 0)).set_z_index(-1)
            self.play(FadeIn(band), run_time=1.2)
            c.wait_until("whole stretch")
            self.play(FlashAround(band, run_time=2, time_width=1.5, buff=0.05), run_time=2.0)
            lab = T("level-triggered", size=38, color=YELLOW).next_to(band, UP, buff=0.3)
            c.wait_until("level")
            self.play(*appear(lab), run_time=1.0)  # early: lands on "the level of enable", the reason for the name
        self.wait(1.5)
        self.play(*disappear(lab), run_time=0.8)
        self.wait(1.0)
