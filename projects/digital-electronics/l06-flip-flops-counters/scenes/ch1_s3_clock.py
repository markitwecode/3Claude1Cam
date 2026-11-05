"""Chapter 1, scene 3: synchronous operation and the clock (levels, period, frequency, edges, purpose). Clips c1.clock.1 – c1.clock.4."""
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


# ---------------------------------------------------------------------------------------------
# Shared visuals of chapter 1 (s2, s3, s4, s6, s7 copy these two blocks verbatim).
# ---------------------------------------------------------------------------------------------
def _bit_style(bit):
    """(colour, stroke width, fill opacity) of a memory cell holding `bit`."""
    return (GREEN, 4, 0.16) if bit else (DIM, 3, 0.0)


def memory_cell(bit=0, size=1.1):
    """One-bit memory: rounded square with a 0/1 inside. GREEN bright for 1, DIM for 0.
    VGroup(box, digit) with .box .digit .bit .size; built at ORIGIN."""
    col, sw, fo = _bit_style(bit)
    box = RoundedRectangle(corner_radius=0.16 * size, width=size, height=size)
    box.set_stroke(col, sw).set_fill(col, fo)
    digit = T(str(bit), size=44 * size / 1.1, color=col)
    digit.move_to(box)
    cell = VGroup(box, digit)
    cell.box, cell.digit, cell.bit, cell.size = box, digit, bit, size
    return cell


def flip_cell(cell, bit=None):
    """Animations that set `cell` to `bit` (default: the other bit): the digit is swapped (old rises
    out, new rises in) and the box recoloured. Returns (anims, new_digit); after the play call
    finish_flip(scene, cell, new_digit, bit)."""
    bit = 1 - cell.bit if bit is None else bit
    col, sw, fo = _bit_style(bit)
    new = T(str(bit), size=44, color=col)
    new.set_height(cell.digit.height).move_to(cell.box)
    anims = [*swap(cell.digit, new, shift=0.12 * UP),
             cell.box.animate.set_stroke(col, sw).set_fill(col, fo)]
    return anims, new


def finish_flip(scene, cell, new_digit, bit):
    """Put the new digit into the cell group and the cell back on screen as one object."""
    old = cell.digit
    settle(scene, cell, add=[new_digit], drop=[old])
    cell.digit, cell.bit = new_digit, bit


class ClockWave(VGroup):
    """YELLOW clock square wave: starts low for half a period, then `periods` cycles (high half,
    low half). Flat levels, sharp vertical edges, small ▲ on every rising edge (▼ on falling
    edges if down_arrows). .wave (the line), .ups, .downs; .period; .rising_x(i)/.falling_x(i)
    give the current absolute x of edge i. Default 9.9 × 0.7, period 1.8, centred at ORIGIN."""

    def __init__(self, width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True,
                 down_arrows=False, stroke_width=4, **kw):
        super().__init__(**kw)
        p = width / (periods + 0.5)
        x0, lo, hi = -width / 2, -height / 2, height / 2
        pts, self._rise, self._fall = [[x0, lo, 0]], [], []
        x = x0 + p / 2
        for _ in range(periods):
            pts += [[x, lo, 0], [x, hi, 0]]
            self._rise.append(x - x0)
            x += p / 2
            pts += [[x, hi, 0], [x, lo, 0]]
            self._fall.append(x - x0)
            x += p / 2
        pts.append([x0 + width, lo, 0])
        self.wave = VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width)
        self.period, self._width = p, width
        tri = 0.11 * min(1.0, height / 0.7)
        self.ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1)
                            .move_to([x0 + r, 0, 0]) for r in (self._rise if up_arrows else [])])
        self.downs = VGroup(*[Triangle().rotate(PI).scale(tri).set_stroke(width=0).set_fill(color, 1)
                              .move_to([x0 + f, 0, 0]) for f in (self._fall if down_arrows else [])])
        self.add(self.wave, self.ups, self.downs)

    def rising_x(self, i):
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._span()  # scale-safe

    def falling_x(self, i):
        return self.wave.get_left()[0] + self._fall[i] * self.wave.width / self._span()

    def _span(self):
        return self._width


def clock_wave(width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True, down_arrows=False):
    return ClockWave(width, height, periods, color, up_arrows, down_arrows)

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
# Scene-only layout
# =============================================================================================
CORNER_SCALE = 0.4                    # latch: 1.15 -> 0.46 in the top-left corner
CORNER_POS = _p(-4.9, 2.85)
WAVE_W, WAVE_H, WAVE_PERIODS = 10.6, 1.6, 3
WAVE_POS = _p(0.1, -0.15)             # hero wave: lo -0.95, hi 0.65
ARROW_GROW = 1.8                      # edge triangles enlarged for the hero wave


class Clock(NarratedScene):
    def construct(self):
        L = rs_latch().scale(LATCH_SCALE).move_to(LATCH_POS)
        self.add(L)
        self.L = L
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- clip 1: synchronous operation, the rule, the system clock -------------------------
    def clip1(self):
        L = self.L
        with self.say("c1.clock.1") as c:
            corner = L.copy().scale(CORNER_SCALE / LATCH_SCALE).move_to(CORNER_POS)
            self.asyn = T("asynchronous", size=30, color=DIM).next_to(corner, DOWN, buff=0.22)
            # the corner copy is too small for its labels and gate numbers: they fade as it moves
            small = [*L.labels, L.g1.num, L.g2.num]
            L.remove(*L.labels)
            L.g1.remove(L.g1.num)
            L.g2.remove(L.g2.num)
            self.add(*small)
            self.play(*during(disappear(*small), 0, 0.35),
                      L.animate.scale(CORNER_SCALE / LATCH_SCALE).move_to(CORNER_POS),
                      *during(appear(self.asyn), 0.55, 1.0), run_time=2.0)  # early: names s2's latch as it moves aside
            self.syn = T("synchronous", size=52, color=YELLOW).move_to(_p(2.0, 0.9))
            c.wait_until(own_word=self.syn)
            self.play(*appear(self.syn), run_time=1.0)

            self.rule = T("outputs change only at a time specified\nby a global enabling signal",
                          size=34, line_spacing=1.1, disable_ligatures=True).move_to(_p(2.0, -0.55))
            c.wait_until("rule")
            self.play(*appear(self.rule), run_time=1.2)

            self.name = T("the system clock", size=46, color=YELLOW).move_to(_p(2.0, -2.2))
            c.wait_until("name")
            self.play(*recolor(select(self.rule, "global enabling signal")[0], YELLOW),
                      *during(appear(self.name), 0.3, 1.0), run_time=1.3)

    # -- clip 2: the wave, levels, period, frequency ---------------------------------------
    def clip2(self):
        with self.say("c1.clock.2") as c:
            w = clock_wave(WAVE_W, WAVE_H, WAVE_PERIODS, up_arrows=True, down_arrows=True)
            w.move_to(WAVE_POS)
            for tri in [*w.ups, *w.downs]:
                tri.scale(ARROW_GROW)
            self.w = w
            lo, hi = w.wave.get_bottom()[1], w.wave.get_top()[1]
            self.lo, self.hi = lo, hi
            self.clk = T("CLK", size=40, color=YELLOW).next_to(w.wave, LEFT, buff=0.3)
            self.clk.set_y((lo + hi) / 2)

            sync_head = self.syn.copy().scale(36 / 52).move_to(_p(4.6, 2.85))
            self.play(*during(disappear(self.rule), 0, 0.45),
                      *during([self.syn.animate.scale(36 / 52).move_to(sync_head)], 0.2, 0.8),
                      run_time=1.2)
            # "the system clock" becomes the wave's CLK label as the wave is drawn
            self.play(Create(w.wave, rate_func=linear), *during(fly(self.name, self.clk), 0.0, 0.5),
                      run_time=min(2.4, c.until("levels")))
            self.remove(self.name)

            # levels
            x_l, x_r = w.wave.get_left()[0], w.wave.get_right()[0]
            self.g_hi = DashedLine(_p(x_l, hi), _p(x_r + 0.1, hi), dash_length=0.12).set_stroke(DIM, 2)
            self.g_lo = DashedLine(_p(x_l, lo), _p(x_r + 0.1, lo), dash_length=0.12).set_stroke(DIM, 2)
            self.l_hi = T("high", size=32, color=FG).next_to(self.g_hi, RIGHT, buff=0.2)
            self.l_lo = T("low", size=32, color=FG).next_to(self.g_lo, RIGHT, buff=0.2)
            for g in (self.g_hi, self.g_lo):
                g.set_z_index(-1)
            c.wait_until("levels")
            c.wait_until(own_word=self.l_hi)
            self.play(FadeIn(self.g_hi), *appear(self.l_hi), run_time=1.0)
            c.wait_until("a low level")
            self.play(FadeIn(self.g_lo), *appear(self.l_lo), run_time=1.0)

            # period: rising edge 0 to rising edge 1
            r0, r1 = w.rising_x(0), w.rising_x(1)
            ya = hi + 0.5
            self.per_arrow = DoubleArrow(_p(r0, ya), _p(r1, ya), buff=0, stroke_width=4,
                                         tip_length=0.22, max_tip_length_to_length_ratio=0.2).set_color(GOLD)
            self.ticks = VGroup(*[DashedLine(_p(x, hi + 0.05), _p(x, ya + 0.15), dash_length=0.08)
                                  .set_stroke(GOLD, 2) for x in (r0, r1)])
            self.per_lbl = T("period", size=34, color=GOLD).next_to(self.per_arrow, UP, buff=0.15)
            c.wait_until("period")
            self.play(FadeIn(self.ticks), GrowFromCenter(self.per_arrow), run_time=1.2)
            c.wait_until(own_word=self.per_lbl)
            self.play(*appear(self.per_lbl), run_time=0.9)

            self.freq = T("frequency = 1 / period", size=40, color=GOLD).move_to(_p(0.1, -1.75))
            c.wait_until("freq")
            self.play(*appear(self.freq), run_time=1.0)

            self.example = T("1 ms → 1000 Hz = 1 kHz", size=40, color=GOLD).move_to(_p(0.1, -2.6))
            c.wait_until("example")
            self.play(*appear(self.example), run_time=1.2)  # early: the worked example, read as it is said

    # -- clip 3: edges ---------------------------------------------------------------------
    def clip3(self):
        w, lo, hi = self.w, self.lo, self.hi
        with self.say("c1.clock.3") as c:
            edges = [Line(_p(x, lo), _p(x, hi)) for x in
                     [w.rising_x(i) for i in range(WAVE_PERIODS)] + [w.falling_x(i) for i in range(WAVE_PERIODS)]]
            glows = [VShowPassingFlash(e.set_stroke(WHITE, 10), time_width=0.8) for e in edges]
            self.play(*during(disappear(self.per_arrow, self.per_lbl, self.ticks,
                                        self.g_hi, self.g_lo, self.l_hi, self.l_lo), 0, 0.45),
                      *during(glows, 0.3, 1.0), run_time=1.8)
            self.play(*[VShowPassingFlash(e.copy(), time_width=0.8) for e in edges], run_time=1.0)

            self.rise_lbl = T("rising edge (positive-going)", size=36, color=YELLOW).move_to(_p(0.1, hi + 0.75))
            c.wait_until("rising")
            self.play(*appear(*w.ups, shift=0.2 * UP, lag=0.15), run_time=1.2)
            c.wait_until(own_word=self.rise_lbl)
            self.play(*appear(self.rise_lbl), run_time=1.0)

            self.fall_lbl = T("falling edge (negative-going)", size=36, color=YELLOW).move_to(_p(0.1, -1.75))
            c.wait_until("falling")
            self.play(*during(disappear(self.freq, self.example), 0, 0.45),
                      *during(appear(*w.downs, shift=0.2 * DOWN, lag=0.15), 0.3, 1.0), run_time=1.4)
            c.wait_until(own_word=self.fall_lbl)
            self.play(*appear(self.fall_lbl), run_time=1.0)
            settle(self, w)

    # -- clip 4: what the clock is for; the question ---------------------------------------
    def clip4(self):
        w, L = self.w, self.L
        with self.say("c1.clock.4", gap=3.5) as c:
            s = 0.75
            wpos = _p(0.3, -2.85)
            head = T("The Clock: What is it and what is it for?", size=44).move_to(_p(0, 3.2))
            w_t = w.copy().scale(s).move_to(wpos)
            clk_to = self.clk.copy().next_to(w_t.wave, LEFT, buff=0.3).set_y(w_t.wave.get_center()[1])
            self.play(*during(disappear(L, self.asyn, self.syn), 0, 0.5),
                      *during(appear(head), 0.45, 1.0), run_time=min(1.6, c.until("order")))

            order = T("It imposes order on the state changes", size=34).move_to(_p(0, 2.25))
            c.wait_until("order")
            self.play(*during(disappear(self.rise_lbl, self.fall_lbl), 0, 0.4),
                      *during([w.animate.scale(s).move_to(wpos), self.clk.animate.move_to(clk_to)], 0.2, 0.8),
                      *during(appear(order), 0.6, 1.0), run_time=1.8)

            together = T("Allows lots of states to appear to update simultaneously", size=34
                         ).move_to(_p(0, 1.5))
            bits = [1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1]
            self.cells = [memory_cell(b, size=0.6) for b in bits]
            VGroup(*self.cells).arrange_in_grid(4, 4, buff=0.16).move_to(_p(0.3, -0.6))
            c.wait_until("together")
            self.play(*appear(together), run_time=1.0)  # early: slide p. 85's line, read as paraphrased
            self.play(*appear(*self.cells, shift=None, lag=0.05), run_time=1.0)

            # the beat: a guide sweeps the wave, the grid flips together on each rising edge
            p = w.period * w.wave.width / WAVE_W
            x0 = w.wave.get_left()[0]
            yb, yt = w.wave.get_bottom()[1] - 0.25, w.wave.get_top()[1] + 0.25
            guide = Line(_p(x0, yb), _p(x0, yt)).set_stroke(FG, 2, opacity=0.7)
            self.play(FadeIn(guide), run_time=0.4)
            rng = np.random.default_rng(3)
            beat_rt = min(1.6, max(0.8, (c.until("question") - 0.3) / WAVE_PERIODS))
            for k in range(WAVE_PERIODS):
                x_to = w.rising_x(k) + p / 2
                n = int(rng.integers(5, 9))
                picks = [self.cells[i] for i in rng.choice(16, n, replace=False)]
                anims, news = [], []
                for cell in picks:
                    a, new = flip_cell(cell)
                    anims += a
                    news.append((cell, new, 1 - cell.bit))
                self.play(*during(anims, 0.5, 0.75), guide.animate(rate_func=linear).set_x(x_to),
                          run_time=beat_rt, rate_func=linear)
                for cell, new, bit in news:
                    finish_flip(self, cell, new, bit)

            # the question: the latch comes back beside the clock
            c.wait_until("question")
            w2 = w.copy().scale(4.2 / w.wave.width).move_to(_p(4.5, 1.1))
            clk2 = self.clk.copy().next_to(w2.wave, LEFT, buff=0.3).set_y(w2.wave.get_center()[1])
            L = rs_latch().move_to(_p(-3.75, 1.15))
            qm = T("?", size=110, color=YELLOW).move_to(_p(0.05, 1.1))
            sweep_clear(self, w.animate.scale(4.2 / w.wave.width).move_to(w2),
                        self.clk.animate.move_to(clk2), FadeIn(L),
                        *during(appear(qm, shift=0.2 * DOWN), 0.6, 1.0),
                        keep=[w, self.clk], run_time=1.6)

            question = T("How can we modify an asynchronous circuit\n"
                         "to act synchronously, i.e., in synchronism\n"
                         "with a clock signal?", size=36, line_spacing=1.1).move_to(_p(0, -2.15))
            # fully up before the voice reads it (fix pass: it was still fading in during "How can we")
            self.play(*appear(question), run_time=min(0.9, c.until("How can we")))  # early: slide p. 85's question, shown on "the slide's question"
