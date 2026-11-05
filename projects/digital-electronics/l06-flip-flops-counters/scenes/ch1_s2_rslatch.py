"""Chapter 1, scene 2: last time, the RS latch (NOR facts, reset/hold/set/illegal, table). Clips c1.rs.1 – c1.rs.5."""
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
# Shared visuals of chapter 1 (copied verbatim from ch1_s1_hook.py).
# =============================================================================================
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


class RsLatchRecap(NarratedScene):
    def construct(self):
        self.vals = {}
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ---- value digits next to the latch's terminals -------------------------------------
    def digit_pos(self, key):
        L = self.L
        e = L.end(key)
        dx = {"r": 0.42, "s": 0.42, "q": -0.42, "qb": -0.42}[key]
        dy = {"r": 0.36, "s": -0.36, "q": 0.36, "qb": -0.36}[key]
        return e + _p(dx, dy)

    def digit(self, key, v, color=GOLD):
        return MathTex(str(v), font_size=44, color=color).move_to(self.digit_pos(key))

    def setv(self, key, v, color=GOLD, wire_col=None):
        """Anims: the terminal's digit becomes v (appear or swap) and its wire lights."""
        new = self.digit(key, v, color)
        old = self.vals.get(key)
        self.vals[key] = new
        anims = swap(old, new) if old is not None else appear(new)
        return [*anims, light(self.L.wires[key], v, color=wire_col)]

    # ---- clips --------------------------------------------------------------------------
    def clip1(self):
        with self.say("c1.rs.1") as c:
            head = T("Last lecture", size=36, color=DIM).to_corner(UL, buff=0.5)
            self.head = head
            self.play(*appear(head), run_time=1.0)  # early: section header
            c.wait_until("bistable")
            cell = memory_cell(1, size=2.0).move_to(_p(0, 0.3))
            self.play(*appear(cell, shift=None), run_time=1.0)
            bist = T("bistable", size=40, color=FG).next_to(cell, DOWN, buff=0.4)
            c.wait_until("called a bye-stable")
            self.play(*appear(bist), run_time=1.0)
            st = T("state", size=40, color=YELLOW).move_to(_p(2.9, 0.3))
            st_arrow = Arrow(st.get_left() + _p(-0.1, 0), cell.digit.get_right() + _p(0.1, 0),
                             buff=0.1, stroke_width=4, color=YELLOW)
            c.wait_until("its state")
            self.play(*appear(st), GrowArrow(st_arrow), run_time=1.0)

            c.wait_until("circuit")
            L = rs_latch(labels=True).scale(LATCH_SCALE).move_to(LATCH_POS)
            L.remove(*L.labels)
            self.L = L
            self.intro = VGroup(cell, bist, st, st_arrow)
            self.play(self.intro.animate.scale(0.76).move_to(_p(3.9, 0.3)),
                      *during(appear(L, shift=None), 0.35, 1.0), run_time=2.0)
            c.wait_until("two nor gates")
            self.play(*flash([L.g1, L.g2], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("feeding")
            self.play(VShowPassingFlash(L.fq.copy().set_stroke(YELLOW, 7), time_width=0.4),
                      VShowPassingFlash(L.fqb.copy().set_stroke(YELLOW, 7), time_width=0.4),
                      run_time=2.0)
            c.wait_until("inputs")
            self.play(*appear(L.lab_r), run_time=1.0)
            c.wait_until("and ess")
            self.play(*appear(L.lab_s), run_time=1.0)
            c.wait_until("outputs")
            self.play(*appear(L.lab_q), run_time=1.0)
            c.wait_until("not cue")
            self.play(*appear(L.lab_qb), run_time=1.0)
            c.wait_until("opposites")
            self.play(*flash([L.lab_q, L.lab_qb], color=GREEN, time_width=1.5),
                      run_time=min(1.5, c.until(floor=0.5)))
            settle(self, L, add=[L.lab_r, L.lab_s, L.lab_q, L.lab_qb])

    def clip2(self):
        with self.say("c1.rs.2") as c:
            # small NOR with a, b, y above its truth table, right half
            g = nor_gate()
            ia = wire((-1.3, 0.3), tuple(g.inp(0)[:2]))
            ib = wire((-1.3, -0.3), tuple(g.inp(1)[:2]))
            oy = wire(tuple(g.out()[:2]), (1.6, 0))
            la = MathTex("a", font_size=40).next_to(ia.get_start(), LEFT, buff=0.12)
            lb = MathTex("b", font_size=40).next_to(ib.get_start(), LEFT, buff=0.12)
            ly = MathTex("y", font_size=40).next_to(oy.get_end(), RIGHT, buff=0.12)
            icon = VGroup(ia, ib, oy, g, la, lb, ly).scale(0.85)
            rows = [["$a", "$b", "$y"], ["$0", "$0", "$1"], ["$0", "$1", "$0"],
                    ["$1", "$0", "$0"], ["$1", "$1", "$0"]]
            tab = grid_table(rows, [0, 0.8, 1.9], size=46, pitch=0.68, seps=[1.35])
            tab.move_to(_p(2.15, -0.35), aligned_edge=ORIGIN)
            tab.set_x(1.55)
            icon.next_to(tab, UP, buff=0.55).set_x(tab.rows[0].get_center()[0])
            self.nor_icon, self.nor_tab = icon, tab
            self.play(*during(disappear(self.intro), 0, 0.5),
                      *during(appear(icon, shift=None), 0.45, 1.0), run_time=1.4)
            self.play(*appear(tab.rows[0], tab.lines, shift=None),  # early: table shown whole, then walked
                      *appear(*tab.rows[1:], lag=0.3), run_time=min(1.8, c.until("always") - 1.0))
            c.wait_until("always")
            br1 = Brace(VGroup(tab.rows[3], tab.rows[4]), RIGHT, buff=0.3, color=YELLOW)
            lab1 = T("always 0", size=32, color=YELLOW).next_to(br1, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br1), *recolor([tab.rows[3][2], tab.rows[4][2]], YELLOW), run_time=1.2)
            c.wait_until(own_word=lab1)
            self.play(*appear(lab1), run_time=1.0)
            c.wait_until("comp")
            br2 = Brace(VGroup(tab.rows[1], tab.rows[2]), RIGHT, buff=0.3, color=TEAL)
            lab2 = T("b complemented", size=32, color=TEAL).next_to(br2, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br2), *recolor([tab.rows[1][2], tab.rows[2][2]], TEAL), run_time=1.2)
            c.wait_until("complement", own_word=lab2)
            self.play(*appear(lab2), run_time=1.0)
            self.nor_extra = [br1, lab1, br2, lab2]

    def gate_tag(self, which, text, color=YELLOW):
        g = self.L.g1 if which == 1 else self.L.g2
        t = T(text, size=32, color=color)
        t.next_to(g.body, UP if which == 1 else DOWN, buff=0.22)
        return t

    def state_tag(self, text, color=FG):
        return T(text, size=44, color=color).move_to(_p(LATCH_POS[0], -3.2))

    def clip3(self):
        L = self.L
        with self.say("c1.rs.3") as c:
            c.wait_until("reset")
            self.play(*self.setv("r", 1), *self.setv("s", 0), run_time=1.5)
            c.wait_until("gate one has")
            self.t1 = self.gate_tag(1, "always 0")
            self.play(*appear(self.t1), *flash([L.g1.body], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("so cue is zero")
            self.play(*self.setv("q", 0), run_time=1.2)
            c.wait_until("reset2")
            self.t2 = self.gate_tag(2, "complement")
            self.play(*appear(self.t2), *flash([L.g2.body], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("so not cue is one")
            self.play(*self.setv("qb", 1), run_time=1.2)
            c.wait_until("that's reset")
            self.st = self.state_tag("reset")
            self.play(*appear(self.st), run_time=1.0)
            c.wait_until("hold")
            self.play(*self.setv("r", 0), run_time=1.5)
            c.wait_until("gate one still sees")
            self.play(VShowPassingFlash(L.fqb.copy().set_stroke(YELLOW, 8), time_width=0.4), run_time=2.0)
            c.wait_until("stays at zero")
            self.play(FlashAround(self.vals["q"], color=YELLOW, time_width=1.5, buff=0.22), run_time=1.5)
            c.wait_until("that's hold")
            new = self.state_tag("hold")
            self.play(*swap(self.st, new), run_time=1.0)
            self.st = new

    def clip4(self):
        L = self.L
        with self.say("c1.rs.4") as c:
            c.wait_until("set")
            self.play(*self.setv("s", 1), run_time=1.0)
            new = self.gate_tag(2, "always 0")
            self.play(*swap(self.t2, new), run_time=1.0)  # early: gate condition tag, on {set}
            self.t2 = new
            c.wait_until("so not cue is zero")
            self.play(*self.setv("qb", 0), run_time=1.2)
            c.wait_until("set2")
            new = self.gate_tag(1, "complement")
            self.play(*swap(self.t1, new), run_time=1.0)  # early: gate condition tag (the NOR fact)
            self.t1 = new
            c.wait_until("becomes one")
            self.play(*self.setv("q", 1), run_time=1.2)
            c.wait_until("that's set")
            new = self.state_tag("set")
            self.play(*swap(self.st, new), run_time=1.0)
            self.st = new
            c.wait_until("illegal")
            self.play(*self.setv("r", 1), run_time=1.0)
            new = self.gate_tag(1, "always 0")
            self.play(*swap(self.t1, new), run_time=1.0)  # early: gate condition tag, on {illegal}
            self.t1 = new
            c.wait_until("both gates are forced")
            self.play(*flash([L.g1.body, L.g2.body], time_width=1.5), run_time=1.2)
            c.wait_until("so cue and not cue")
            self.play(*self.setv("q", 0, color=RED), *recolor([self.vals["qb"]], RED), run_time=1.2)
            c.wait_until("contra")
            contra = MathTex(r"Q = \overline{Q}\ ?!", font_size=48, color=RED)
            contra.move_to(_p(LATCH_POS[0] - 1.1, -3.2))
            self.play(*swap(self.st, contra), run_time=1.2)
            ill = T("illegal", size=44, color=RED).next_to(contra, RIGHT, buff=0.7)
            c.wait_until(own_word=ill)
            self.play(*appear(ill), run_time=1.0)
            self.walk_extra = [self.t1, self.t2, contra, ill]

    def clip5(self):
        L = self.L
        with self.say("c1.rs.5") as c:
            rows = [["$S", "$R", "$Q'", r"$\overline{Q}'", "comment"],
                    ["$0", "$0", "$Q", r"$\overline{Q}", "hold"],
                    ["$0", "$1", "$0", "$1", "reset"],
                    ["$1", "$0", "$1", "$0", "set"],
                    ["$1", "$1", "$0", "$0", "illegal"]]
            tab = grid_table(rows, [0, 0.75, 1.9, 2.8, ("L", 3.75)], size=44, pitch=0.66,
                             seps=[1.32, 3.4], colors=[None, None, None, None, RED])
            tab.move_to(_p(3.55, 0.95))
            old = [self.nor_icon, self.nor_tab, *self.nor_extra]
            c.wait_until("table")
            self.play(*during(disappear(*old, lag=0.05), 0, 0.5),
                      *during(appear(tab.rows[0], tab.lines, shift=None), 0.5, 1.0), run_time=1.4)
            self.play(*appear(*tab.rows[1:], lag=0.35), run_time=min(2.0, max(1.2, c.until("prime"))))
            prime = T("Where Q′ is the next state\nand Q is the current state", size=32, color=FG,
                      line_spacing=1.1)
            prime.next_to(tab, DOWN, buff=0.55)
            c.wait_until("prime")
            self.play(*appear(prime), run_time=1.0)
            c.wait_until("async")
            # back to a stored 0: R = S = 0, Q = 0, Q-bar = 1 (as after reset)
            self.play(*disappear(*self.walk_extra), run_time=0.8)
            self.play(*self.setv("r", 0), *self.setv("s", 0), *self.setv("q", 0), *self.setv("qb", 1),
                      run_time=1.2)
            c.wait_until("changes directly")
            # S rises and the outputs answer at once, inside the same play, while S is still 1
            self.play(*during(self.setv("s", 1), 0, 0.45),
                      *during([*self.setv("qb", 0), *self.setv("q", 1)], 0.35, 1.0), run_time=1.4)
            c.wait_until("name")
            self.play(*self.setv("s", 0), run_time=0.8)
            cap = T("asynchronous operation", size=44, color=YELLOW).move_to(_p(LATCH_POS[0], -3.2))
            self.play(*appear(cap), run_time=1.0)
        self.wait(4.9)
        # back to the bare latch at its hero position (s3 opens from it)
        rest = [m for m in self.mobjects if m is not L]
        self.play(*disappear(*rest, lag=0.05),
                  *[light(L.wires[k], color=WIRE) for k in ("r", "s", "q", "qb")], run_time=1.2)
        self.wait(1.0)   # ends on the bare latch: s3 opens with it already on screen
