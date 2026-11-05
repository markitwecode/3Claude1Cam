"""Chapter 1, scene 4: an AND gate as a valve (block / pass, truth table, set-up for the D latch). Clips c1.valve.1 – c1.valve.3."""
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
GATE_SCALE = 2.0
GATE_POS = _p(-3.0, -1.3)
TRACE_X0, TRACE_W = -5.7, 5.2           # two halves: a = 0 (left), a = 1 (right)
B_Y, Y_Y, TRACE_H = 2.45, 1.25, 0.6
WIGGLE = [0.12, 0.3, 0.42, 0.52, 0.66, 0.88]   # b's toggle points (fractions of a half), starts low
SLOT = _p(-3.0, -3.25)                  # caption slot under the gate
TABLE_POS = _p(4.3, 0.15)
SW_ON_FILL = interpolate_color(ManimColor(BG), ManimColor(ON), 0.2)   # switch at 1: GREEN tint (opaque, hides the wire)
LIFT = 1.2                              # clip 1: gate higher, before the traces arrive


def trace(x0, w, toggles, yc, color, h=TRACE_H):
    """Timing trace in the clock_wave stroke style: starts low, toggles at the given fractions."""
    lo, hi = yc - h / 2, yc + h / 2
    lvl, pts = lo, [[x0, lo, 0]]
    for f in toggles:
        x = x0 + f * w
        pts += [[x, lvl, 0]]
        lvl = hi if lvl == lo else lo
        pts += [[x, lvl, 0]]
    pts.append([x0 + w, lvl, 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, 4)


def rises(toggles):
    return toggles[0::2]


def pulse(w, color=ON):
    """A bright bump travelling along wire w (a copy), removed at the end."""
    return VShowPassingFlash(w.copy().set_stroke(color, 12), time_width=0.6, taper_width=0.05)


def bit_switch(bit):
    col = ON if bit else OFF
    box = RoundedRectangle(corner_radius=0.1, width=0.62, height=0.62)
    box.set_stroke(col, 4).set_fill(BG, 1).set_z_index(2)
    return box


def bit_digit(bit, at):
    return T(str(bit), size=36, color=ON if bit else OFF).move_to(at).set_z_index(3)


def row_box(table, i0, i1, color):
    """Highlight behind table rows i0..i1 (rows counted with the header as 0)."""
    top = table.rows[i0].get_top()[1] + 0.12
    bot = table.rows[i1].get_bottom()[1] - 0.12
    left = table.rows[0].get_left()[0] - 0.3
    right = table.rows[0].get_right()[0] + 0.3
    r = Rectangle(width=right - left, height=top - bot).move_to(_p((left + right) / 2, (top + bot) / 2))
    return r.set_stroke(color, 2).set_fill(color, 0.2).set_z_index(-1)


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


class AndGateValve(NarratedScene):
    def construct(self):
        self.build()
        self.clip1()
        self.clip2()
        self.clip3()
        # no final fade: s5 opens with d_latch().latch already on screen at this exact placement

    def build(self):
        g = and_gate().scale(GATE_SCALE).move_to(GATE_POS)
        self.gate = g
        a_in, b_in, out = g.inp(0), g.inp(1), g.out()
        self.wa = wire((-5.55, a_in[1]), tuple(a_in[:2]))   # starts inside the switch
        self.wb = wire((-5.9, b_in[1]), tuple(b_in[:2]))
        self.wy = wire(tuple(out[:2]), (-0.4, out[1]))
        self.la = MathTex("a", font_size=52, color=BLUE).next_to(_p(-5.9, a_in[1]), LEFT, buff=0.2)
        self.lb = MathTex("b", font_size=52, color=BLUE).next_to(self.wb.get_start(), LEFT, buff=0.2)
        self.ly = MathTex("y", font_size=52, color=GREEN).next_to(self.wy.get_end(), RIGHT, buff=0.2)
        self.sw_at = _p(-5.55, a_in[1])

        rows = [["$a", "$b", "$y"], ["$0", "$0", "$0"], ["$0", "$1", "$0"],
                ["$1", "$0", "$0"], ["$1", "$1", "$1"]]
        tab = grid_table(rows, [0.0, 0.8, 2.0], size=48, pitch=0.7, seps=(1.4,))
        tab.rows[0][0].set_color(BLUE)
        tab.rows[0][1].set_color(BLUE)
        tab.rows[0][2].set_color(GREEN)
        tab.move_to(TABLE_POS)
        self.table = tab

        # traces (b on top, y below), each in two halves: a = 0 then a = 1
        x0, w = TRACE_X0, TRACE_W / 2
        self.b0 = trace(x0, w, WIGGLE, B_Y, BLUE)
        self.y0 = trace(x0, w, [], Y_Y, GREEN)
        self.b1 = trace(x0 + w, w, WIGGLE, B_Y, BLUE)
        self.y1 = trace(x0 + w, w, WIGGLE, Y_Y, GREEN)
        self.tb = MathTex("b", font_size=44, color=BLUE).move_to(_p(-6.3, B_Y))
        self.ty = MathTex("y", font_size=44, color=GREEN).move_to(_p(-6.3, Y_Y))
        self.h0 = T("a = 0", size=30, color=DIM).move_to(_p(x0 + w / 2, B_Y + 0.8))
        self.h1 = T("a = 1", size=30, color=DIM).move_to(_p(x0 + 1.5 * w, B_Y + 0.8))
        self.divider = DashedLine(_p(x0 + w, Y_Y - 0.45), _p(x0 + w, B_Y + 0.45),
                                  dash_length=0.08).set_stroke(DIM, 2)

    def wiggle(self, c, b_tr, y_tr, run_time, extra=(), through=False):
        """Draw one half of the traces left to right (linear) while b's pulses run along its wire;
        if `through`, each pulse continues along y's wire."""
        anims = [Create(b_tr, rate_func=linear), Create(y_tr, rate_func=linear)]
        for r in rises(WIGGLE):
            anims += during(pulse(self.wb), r, min(1.0, r + 0.22))
            if through:
                anims += during(pulse(self.wy), min(0.9, r + 0.1), min(1.0, r + 0.3))
        self.play(*anims, *extra, run_time=run_time)

    # -- c1.valve.1 -------------------------------------------------------------------------
    def clip1(self):
        with self.say("c1.valve.1") as c:
            # until the traces arrive, the gate sits higher (balanced with the table)
            for m in (self.wa, self.wb, self.wy, self.gate, self.la, self.lb, self.ly):
                m.shift(LIFT * UP)
            self.play(FadeIn(VGroup(self.wa, self.wb, self.wy, self.gate)),
                      *during(appear(self.la, self.lb, self.ly, lag=0.2), 0.3, 1),
                      run_time=min(1.6, c.until("use an and gate")))
            c.wait_until("use an and gate")
            self.cap = T("AND gate", size=40, color=BLUE).move_to(SLOT + LIFT * UP)
            c.wait_until(own_word=self.cap)
            self.play(*appear(self.cap), run_time=1.0)

            c.wait_until("table")
            self.play(*appear(*self.table.rows, self.table.lines, lag=0.2),  # early: table shown whole, then read
                      run_time=min(1.6, c.until("one")))
            c.wait_until("one")
            self.box = row_box(self.table, 4, 4, YELLOW)
            self.play(FadeIn(self.box), *flash(self.table.rows[4]),
                      light(self.wa, 1), light(self.wb, 1), light(self.wy, 1),
                      run_time=min(1.5, c.until()))

    # -- c1.valve.2 -------------------------------------------------------------------------
    def clip2(self):
        with self.say("c1.valve.2") as c:
            # a held at 0; b's wire and y's wire idle low
            self.sw = bit_switch(0).move_to(self.sw_at)
            self.dig = bit_digit(0, self.sw_at)
            down = [m.animate.shift(LIFT * DOWN) for m in (self.gate, self.la, self.lb, self.ly, self.cap)]
            down += [w.animate.shift(LIFT * DOWN).set_color(OFF) for w in (self.wa, self.wb, self.wy)]
            self.play(*during(down, 0, 0.55),
                      *during(appear(self.sw, self.dig, shift=None, lag=0.1), 0.5, 1),
                      *during(appear(self.tb, self.ty, self.h0, lag=0.15), 0.4, 1),
                      run_time=1.4)
            # b wiggles; its pulses die at the gate; y stays flat. Rows 0 0 / 0 1 light on {stuck}.
            rt = min(4.0, max(2.5, 0.85 * c.until("signal is blocked")))
            f = min(0.7, c.until("stuck", floor=0) / rt)
            new_box = row_box(self.table, 1, 2, RED)
            self.wiggle(c, self.b0, self.y0, rt,
                        extra=during([FadeOut(self.box)], f, min(1.0, f + 0.12))
                        + during([FadeIn(new_box)], min(0.95, f + 0.12), min(1.0, f + 0.3)))
            self.box = new_box
            c.wait_until("signal is blocked")
            blocked = T("blocked", size=40, color=RED).move_to(SLOT)
            self.play(*swap(self.cap, blocked), FlashUnder(self.y0, color=RED, run_time=1.4),
                      run_time=1.4)
            self.cap = blocked

            c.wait_until("pass")
            dig1 = bit_digit(1, self.sw_at)
            self.play(*swap(self.dig, dig1), self.sw.animate.set_stroke(ON, 4).set_fill(SW_ON_FILL, 1), light(self.wa, 1),
                      *during(disappear(self.box, self.cap), 0, 0.45),   # a = 1: the 'blocked' rows/label go
                      *during(appear(self.divider, self.h1, shift=None, lag=0.3), 0.4, 1),
                      run_time=min(1.4, c.until("copy")))
            self.dig = dig1
            c.wait_until("copy")
            rt = min(4.0, max(2.5, 0.85 * c.until("signal passes")))
            new_box = row_box(self.table, 3, 4, GREEN)
            self.wiggle(c, self.b1, self.y1, rt, through=True,
                        extra=during([FadeIn(new_box)], 0.7, 1.0))
            self.box = new_box
            c.wait_until("signal passes")
            passes = T("passes", size=40, color=GREEN).move_to(SLOT)
            self.play(*appear(passes), run_time=min(1.2, c.until()))
            self.cap = passes

    # -- c1.valve.3 -------------------------------------------------------------------------
    def clip3(self):
        with self.say("c1.valve.3") as c:
            # the gate becomes a valve on b's path to y, with a as the handle (open: a = 1)
            g = self.gate
            ctr = g.body.get_center() + 0.05 * RIGHT
            ring = Circle(radius=0.48).move_to(ctr).set_stroke(YELLOW, 4).set_fill(BG, 1).set_z_index(1)
            flap = Line(ctr + 0.42 * LEFT, ctr + 0.42 * RIGHT).set_stroke(BLUE, 8).set_z_index(2)
            hub = Dot(ctr, radius=0.09, color=BLUE).set_z_index(3)
            handle_lab = MathTex("a", font_size=44, color=BLUE).next_to(ring, UP, buff=0.12)
            p_in = DashedLine(g.inp(1), ring.point_at_angle(PI + 0.5), dash_length=0.12).set_stroke(BLUE, 3)
            p_out = DashedLine(ring.get_right(), g.out(), dash_length=0.12).set_stroke(ON, 3)
            self.play(restyle(g, op=0.3), FadeOut(self.box),
                      *during([FadeIn(ring), FadeIn(flap), FadeIn(hub), FadeIn(p_in), FadeIn(p_out)], 0.3, 1),
                      *during(appear(handle_lab), 0.5, 1),
                      run_time=min(1.8, c.until("closed")))

            c.wait_until("closed")
            closed = T("a = 0: closed", size=40, color=RED).move_to(SLOT)
            dig0 = bit_digit(0, self.sw_at)
            self.play(*swap(self.dig, dig0), self.sw.animate.set_stroke(OFF, 4).set_fill(BG, 1), light(self.wa, 0),
                      Rotate(flap, PI / 2, about_point=ctr), p_out.animate.set_stroke(OFF),
                      *swap(self.cap, closed), run_time=min(1.4, c.until("open")))
            self.dig, self.cap = dig0, closed

            c.wait_until("open")
            opened = T("a = 1: open", size=40, color=GREEN).move_to(SLOT)
            dig1 = bit_digit(1, self.sw_at)
            self.play(*swap(self.dig, dig1), self.sw.animate.set_stroke(ON, 4).set_fill(SW_ON_FILL, 1), light(self.wa, 1),
                      Rotate(flap, -PI / 2, about_point=ctr), p_out.animate.set_stroke(ON),
                      *swap(self.cap, opened), run_time=min(1.4, c.until("plan")))
            self.dig, self.cap = dig1, opened

            # {plan}: the board clears to the latch; two copies of the gate slide to R and S
            c.wait_until("plan")
            dl = d_latch()
            latch = dl.latch
            board = [m for m in self.mobjects if m is not g]
            self.play(*during(disappear(*board), 0, 0.5), restyle(g, op=1),
                      *during([FadeIn(latch)], 0.5, 1), run_time=1.4)
            # the big gate fades; two unit-size gates fade in already apart (never stacked), then slide
            top = g.copy().scale(1 / GATE_SCALE).move_to(g.get_center() + 0.9 * UP)
            bot = g.copy().scale(1 / GATE_SCALE).move_to(g.get_center() + 0.9 * DOWN)
            self.play(*during([FadeOut(g)], 0, 0.5), *during([FadeIn(top), FadeIn(bot)], 0.45, 1),
                      run_time=1.0)
            self.play(top.animate.move_to(dl.and_r), bot.animate.move_to(dl.and_s),
                      run_time=min(1.5, max(1.0, c.until() - 1.2)))
            self.wait(0.4)
            self.play(*disappear(top, bot), run_time=0.8)
        self.wait(1.0)   # the bare latch: s5 opens with d_latch().latch on screen
