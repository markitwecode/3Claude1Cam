"""Chapter 2, scene 6: flip-flops vs latches, their symbols, the switch demo, and the box the rest
of the lecture uses. Clips c2.symbol.1 – c2.symbol.5.

Opening: s3's end shot (`master_slave_end_shot()`, copied from ch2_s3_masterslave.py); the demo
uses s3's `MasterSlave()` at full size, with switches, a Q-bar output and LEDs added.
The flip-flop box (`make_ff`) is the one ch3/ch4 reuse: same size and stroke as s1's latch.
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


WIRE_C, WIRE_W, GATE_COLOR = FG, 4, BLUE
BOX_W, BOX_H = 1.5, 2.6


def _p(x, y):
    return np.array([x, y, 0.0])


def wire(*pts, color=WIRE_C, width=WIRE_W):
    return VMobject().set_points_as_corners([_p(*p) for p in pts]).set_stroke(color, width)


# ==== copied from ch2_s3_masterslave.py (renamed: wire->ms_wire, PIN_Y/CLK_Y/EN_Y/TOP_Y->MS_*) ====
# ---- latch box (matches ch2_s1_hook.make_latch) ------------------------------------------------
PIN_DY = 0.6          # D and Q pins sit 0.6 above the box centre
MS_WIRE_W = 5


def latch_box(center=ORIGIN, stubs=False):
    """s1's latch: box 1.5 x 2.6 (FG, stroke 4), D (BLUE) / Q (GREEN) labels inside at the pin
    height, EN (BLUE) inside at the bottom, a 0.2 BLUE square on the bottom edge.
    Parts .box .square .lab_d .lab_q .lab_en; with stubs=True also s1's .d_w .q_w .en_w wires."""
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4).set_fill(BG, 1)
    sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(box.get_bottom())
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_DY, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_DY, 0])
    en_l = T("EN", 30, BLUE).move_to([0, -BOX_H / 2 + 0.42, 0])
    g = VGroup()
    if stubs:
        g.d_w = Line([-BOX_W / 2 - 0.85, PIN_DY, 0], [-BOX_W / 2, PIN_DY, 0]).set_stroke(BLUE, 5)
        g.q_w = Line([BOX_W / 2, PIN_DY, 0], [BOX_W / 2 + 0.85, PIN_DY, 0]).set_stroke(GREEN, 5)
        g.en_w = Line([0, -BOX_H / 2 - 1.0, 0], [0, -BOX_H / 2 - 0.1, 0]).set_stroke(BLUE, 5)
        g.stubs = [g.d_w, g.q_w, g.en_w]
        g.add(*g.stubs)
    g.add(box, sq, d_l, q_l, en_l)
    g.box, g.square, g.lab_d, g.lab_q, g.lab_en = box, sq, d_l, q_l, en_l
    g.body = [box, sq, d_l, q_l, en_l]
    g.shift(center)
    return g


def ms_wire(*pts, color=FG, width=MS_WIRE_W):
    w = VMobject().set_points_as_corners([_p(*p) for p in pts])
    return w.set_stroke(color, width)


def inverter(x, y, color=BLUE):
    """Triangle + output bubble pointing right, centred at (x, y); input at x-0.4, output x+0.46."""
    tri = Polygon(_p(x - 0.4, y + 0.35), _p(x - 0.4, y - 0.35), _p(x + 0.3, y))
    tri.set_stroke(color, 4).set_fill(BG, 1)
    bubble = Circle(radius=0.08).set_stroke(color, 4).set_fill(BG, 1).move_to(_p(x + 0.38, y))
    g = VGroup(tri, bubble)
    g.tri, g.bubble = tri, bubble
    return g


# ---- the p. 87 circuit ---------------------------------------------------------------------------
MX, SX, CY = -2.6, 2.6, 0.2      # box centres
MS_PIN_Y = CY + PIN_DY              # 0.8: D / Q_int / Q wire height
MS_CLK_Y = -2.3                     # clock line
MS_EN_Y = CY - BOX_H / 2 - 0.1      # bottom of the enable square
X_IN, X_OUT = -5.3, 5.3          # D wire start, Q wire end
INV1_X, INV2_X = -4.3, 0.0
MS_TOP_Y = 2.85                     # tag / door row (above the Master / Slave labels)


class MasterSlave(VGroup):
    """Slide p. 87 at full size (12 wide, labels to x = +-6). Parts:
    .master .slave        latch_box groups at (-2.6, 0.2) / (2.6, 0.2)
    .lab_master .lab_slave T 40 "Master" / "Slave" above the boxes (y 1.95)
    .d_wire .lab_d        BLUE D wire (y 0.8) and its label
    .qint_wire .lab_qint  TEAL Q_int wire between the boxes, MathTex Q_{int} above it
    .q_wire .lab_q        GREEN Q wire and label
    .clk_wire .lab_clk    YELLOW CLK in at bottom left (y -2.3), stroke 6
    .inv1 .inv2           inverters (BLUE, .bubble)
    .clkb_wire .node .mid_wire   CLK-bar: inv1 out -> node under the master -> up into its enable;
                                 node -> inv2 in.  .clkb_part = these three
    .clk2_wire            inv2 out -> up into the slave's enable (CLK again)
    .lab_clkb .lab_clk2   MathTex \\overline{CLK} / CLK beside the enable wires
    .clk_part = [clk_wire, clk2_wire] (the CLK-phase wires)"""

    def __init__(self):
        super().__init__()
        self.master = latch_box(_p(MX, CY))
        self.slave = latch_box(_p(SX, CY))
        for lb in (self.master, self.slave):
            for m in lb.body:
                m.set_z_index(1)
        self.lab_master = T("Master", 40).move_to(_p(MX, 1.95))
        self.lab_slave = T("Slave", 40).move_to(_p(SX, 1.95))

        self.d_wire = ms_wire((X_IN, MS_PIN_Y), (MX - BOX_W / 2, MS_PIN_Y), color=BLUE)
        self.lab_d = T("D", 40, BLUE).next_to(self.d_wire.get_start(), LEFT, buff=0.18)
        self.qint_wire = ms_wire((MX + BOX_W / 2, MS_PIN_Y), (SX - BOX_W / 2, MS_PIN_Y), color=TEAL)
        self.lab_qint = MathTex(r"Q_{\mathrm{int}}", font_size=44, color=TEAL).move_to(_p(0, MS_PIN_Y + 0.42))
        self.q_wire = ms_wire((SX + BOX_W / 2, MS_PIN_Y), (X_OUT, MS_PIN_Y), color=GREEN)
        self.lab_q = T("Q", 40, GREEN).next_to(self.q_wire.get_end(), RIGHT, buff=0.18)

        self.clk_wire = ms_wire((X_IN, MS_CLK_Y), (INV1_X - 0.4, MS_CLK_Y), color=YELLOW, width=6)
        self.lab_clk = MathTex(r"\mathrm{CLK}", font_size=40, color=YELLOW)
        self.lab_clk.next_to(self.clk_wire.get_start(), LEFT, buff=0.15)
        self.inv1 = inverter(INV1_X, MS_CLK_Y).set_z_index(1)
        self.clkb_wire = ms_wire((INV1_X + 0.46, MS_CLK_Y), (MX, MS_CLK_Y), (MX, MS_EN_Y), color=YELLOW, width=6)
        self.node = Dot(_p(MX, MS_CLK_Y), radius=0.09, color=YELLOW)
        self.mid_wire = ms_wire((MX, MS_CLK_Y), (INV2_X - 0.4, MS_CLK_Y), color=YELLOW, width=6)
        self.inv2 = inverter(INV2_X, MS_CLK_Y).set_z_index(1)
        self.clk2_wire = ms_wire((INV2_X + 0.46, MS_CLK_Y), (SX, MS_CLK_Y), (SX, MS_EN_Y), color=YELLOW, width=6)
        self.lab_clkb = MathTex(r"\overline{\mathrm{CLK}}", font_size=40, color=YELLOW)
        self.lab_clkb.move_to(_p(MX - 0.62, (MS_EN_Y + MS_CLK_Y) / 2))
        self.lab_clk2 = MathTex(r"\mathrm{CLK}", font_size=40, color=YELLOW)
        self.lab_clk2.move_to(_p(SX - 0.62, (MS_EN_Y + MS_CLK_Y) / 2))
        self.clkb_part = [self.clkb_wire, self.node, self.mid_wire]
        self.clk_part = [self.clk_wire, self.clk2_wire]

        self.add(self.d_wire, self.qint_wire, self.q_wire, self.clk_wire, self.clkb_wire,
                 self.mid_wire, self.clk2_wire, self.node, self.master, self.slave, self.inv1,
                 self.inv2, self.lab_master, self.lab_slave, self.lab_d, self.lab_qint, self.lab_q,
                 self.lab_clk, self.lab_clkb, self.lab_clk2)


END_SCALE = 0.42
END_CENTER = _p(0, 2.45)


LABEL_K = 1.7      # labels grow by this much more than the circuit, so they stay readable (~28)


def end_strokes(ms):
    """At END_SCALE the full-size strokes swamp the small parts (bubbles read as dots, the enable
    squares as blobs): thin the gate and square outlines. Positions and sizes are untouched."""
    for inv in (ms.inv1, ms.inv2):
        inv.tri.set_stroke(width=2.5)
        inv.bubble.set_stroke(width=2)
        inv.bubble.scale(1.35, about_point=inv.bubble.get_left())
    for lb in (ms.master, ms.slave):
        lb.square.set_stroke(width=2)
        lb.box.set_stroke(width=3)
    return ms


def end_pose(ms):
    """In place: scale a MasterSlave to the end shot. The boxes' inner D/Q/EN labels are not part
    of the end shot (too small at this scale): drop them first (see master_slave_end_shot)."""
    ms.scale(END_SCALE).move_to(END_CENTER)
    for lab in (ms.lab_master, ms.lab_slave, ms.lab_d, ms.lab_q, ms.lab_qint, ms.lab_clk,
                ms.lab_clkb, ms.lab_clk2):
        lab.scale(LABEL_K)
    ms.lab_d.next_to(ms.d_wire.get_start(), LEFT, buff=0.1)
    ms.lab_q.next_to(ms.q_wire.get_end(), RIGHT, buff=0.1)
    ms.lab_clk.next_to(ms.clk_wire.get_start(), LEFT, buff=0.1)
    ms.lab_qint.next_to(ms.qint_wire, UP, buff=0.08)
    ms.lab_master.next_to(ms.master.box, UP, buff=0.1)
    ms.lab_slave.next_to(ms.slave.box, UP, buff=0.1)
    for lab, lb in ((ms.lab_clkb, ms.master), (ms.lab_clk2, ms.slave)):
        x = lb.box.get_x()
        y = (lb.box.get_bottom()[1] + ms.clk_wire.get_y()) / 2
        lab.move_to(_p(x - 0.12 - lab.width / 2, y))
    ms.move_to(END_CENTER)      # re-centre the bounding box (labels included)
    return end_strokes(ms)


def master_slave_end_shot():
    """The circuit exactly as this scene ends: MasterSlave() without the boxes' inner D/Q/EN labels,
    scaled 0.42, its bounding box centred at (0, 2.45), its labels 1.7x larger again
    (~28 pt) and re-anchored to their wires; all parts in their default colours."""
    ms = MasterSlave()
    for lb in (ms.master, ms.slave):
        lb.remove(lb.lab_d, lb.lab_q, lb.lab_en)
    return end_pose(ms)




# ---- latch symbol (copied from ch2_s1_hook.py `make_latch`; .sq added) ----------------------
PIN_Y = 0.6          # D and Q pins sit 0.6 above the box centre
WIRE = 0.85          # D / Q wire length
EN_WIRE = 1.0        # EN wire length below the box


def make_latch(center=ORIGIN):
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(box.get_bottom())
    d_w = Line([-BOX_W / 2 - WIRE, PIN_Y, 0], [-BOX_W / 2, PIN_Y, 0]).set_stroke(BLUE, 5)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    en_w = Line([0, -BOX_H / 2 - EN_WIRE, 0], [0, -BOX_H / 2 - 0.1, 0]).set_stroke(BLUE, 5)
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    en_l = T("EN", 30, BLUE).move_to([0, -BOX_H / 2 + 0.42, 0])
    g = VGroup(d_w, q_w, en_w, box, sq, d_l, q_l, en_l)
    g.box, g.en_wire, g.sq = box, en_w, sq
    g.shift(center)
    return g


# ---- THE flip-flop symbol (ch3 / ch4 reuse this) ---------------------------------------------
def qbar(size=36, color=GREEN):
    """Q with an overbar, in the T font (matches the T labels of the latch)."""
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False):
    """D flip-flop box, same size/stroke as s1's latch: box 1.5 x 2.6, FG outline stroke 4.
    D in (BLUE wire, 0.85 long, stroke 5) and Q out (GREEN) 0.6 above centre, Q-bar out (GREEN) 0.6
    below; clock wire (YELLOW, stroke 5) from 1.0 below the box up to a small triangle (FG stroke 3,
    BG fill, 0.34 wide x 0.26 tall, base on the bottom edge). bubble=True: a 0.1-radius FG bubble
    sits under the edge, before the triangle (falling-edge flip-flop).
    Parts: .box .tri .bub (or None) .d_l .q_l .qb_l .d_w .q_w .qb_w .clk_w.
    At scale 1, 3.2 wide x 3.6 tall, box centred at `center`."""
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
    d_l = T("D", 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


def place(g, scale, box_center):
    g.scale(scale)
    g.shift(_p(*box_center[:2]) - g.box.get_center())
    return g


# ---- tiny one-period clock traces under the symbols ----------------------------------------
def tiny_trace(center, kind, w=2.4, h=0.4):
    """Low, high, low. kind 'level': the high level shaded (YELLOW 0.18); 'rise': ▲ on the rising
    edge; 'fall': ▼ on the falling edge."""
    cx, cy = center
    x0, lo, hi = cx - w / 2, cy - h / 2, cy + h / 2
    xr, xf = x0 + w / 4, x0 + 3 * w / 4
    line = wire((x0, lo), (xr, lo), (xr, hi), (xf, hi), (xf, lo), (x0 + w, lo), color=YELLOW)
    g = VGroup()
    if kind == "level":
        band = Rectangle(width=xf - xr, height=h).set_stroke(width=0).set_fill(YELLOW, 0.18)
        g.add(band.move_to(_p((xr + xf) / 2, cy)))
    g.add(line)
    if kind == "rise":
        g.add(Triangle().scale(0.11).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(xr, cy)))
    if kind == "fall":
        g.add(Triangle().rotate(PI).scale(0.11).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(xf, cy)))
    return g


# ---- demo pieces (switch and LED as in ch1_s6_transparent.py, switch colour added) -----------
def toggle(v, color=BLUE):
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(color, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    g.track, g.knob, g.v, g.sw_color = track, knob, v, color   # not .color: that setter recolours the whole group

    def knob_pos(val):
        return g.track.get_center() + (0.2 if val else -0.2) * RIGHT
    g.knob_pos = knob_pos
    knob.move_to(knob_pos(v)).set_fill(color if v else DIM, 1)
    return g


def flip(sw, v):
    sw.v = v
    return sw.knob.animate.move_to(sw.knob_pos(v)).set_fill(sw.sw_color if v else DIM, 1)


def led(on):
    c = Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)
    c.on = on
    return c


def set_led(l, on):
    l.on = on
    return l.animate.set_fill(GREEN, 0.9 if on else 0.0)


LOW_OP = 0.18    # a wire at 0 keeps its role colour at this opacity; at 1 it is full


DEMO_SCALE, DEMO_SHIFT = 0.95, 0.35 * UP


def demo_circuit():
    """s3's MasterSlave() (full size) with switches on D and CLK, a Q-bar output on the slave and
    LEDs on Q and Q-bar; then scaled DEMO_SCALE and shifted up for the CLK trace below.
    .w = {d, qint, q, qb, clk, nclk, clk2} wires; .dot (CLK-bar node); .sw_d .sw_c .led_q .led_qb;
    .master (.name_l = "Master" label); .core .ins .outs groups."""
    ms = MasterSlave()
    x_sw, x_led = -5.05, X_OUT + 0.21
    sw_d = toggle(0, BLUE).move_to(_p(x_sw, MS_PIN_Y)).set_z_index(2)
    sw_c = toggle(0, YELLOW).move_to(_p(x_sw, MS_CLK_Y)).set_z_index(2)
    ms.lab_d.next_to(sw_d, LEFT, buff=0.18)
    ms.lab_clk.next_to(sw_c, LEFT, buff=0.18)
    y_qb = CY - 0.2          # Q-bar pin raised so its label clears EN inside the box
    qb_wire = ms_wire((SX + BOX_W / 2, y_qb), (X_OUT, y_qb), color=GREEN)
    qb_in = qbar().move_to(_p(SX + BOX_W / 2 - 0.3, y_qb + 0.05)).set_z_index(1)
    led_q, led_qb = led(False).move_to(_p(x_led, MS_PIN_Y)), led(False).move_to(_p(x_led, y_qb))
    ms.lab_q.next_to(led_q, RIGHT, buff=0.18)
    lab_qb = qbar(40).next_to(led_qb, RIGHT, buff=0.18)
    ms.remove(ms.lab_d, ms.lab_clk, ms.lab_q)
    ms.add(qb_wire, qb_in)
    g = VGroup()
    ins = VGroup(sw_d, ms.lab_d, sw_c, ms.lab_clk)
    outs = VGroup(led_q, ms.lab_q, led_qb, lab_qb)
    g.add(ms, ins, outs)
    g.scale(DEMO_SCALE, about_point=ORIGIN).shift(DEMO_SHIFT)
    g.w = {"d": ms.d_wire, "qint": ms.qint_wire, "q": ms.q_wire, "qb": qb_wire, "clk": ms.clk_wire,
           "nclk": VGroup(ms.clkb_wire, ms.mid_wire), "clk2": ms.clk2_wire}
    g.dot, g.sw_d, g.sw_c, g.led_q, g.led_qb = ms.node, sw_d, sw_c, led_q, led_qb
    g.master = ms.master
    g.master.name_l = ms.lab_master
    g.core, g.ins, g.outs = ms, ins, outs
    return g


def lev(m, v):
    """A wire (or VGroup of wires) to logic level v: full role colour at 1, faint at 0."""
    return m.animate.set_stroke(opacity=1.0 if v else LOW_OP)


# CLK trace under the demo: one level per switch flip.
TR_X0, TR_W, TR_Y, TR_H = -3.9, 0.95, -3.05, 0.4
CLK_LEVELS = [1, 0, 1, 0, 1, 0, 1, 0, 1]   # start, fall, rise, (fall, rise) x2, fall, rise


def trace_piece(k):
    y = lambda v: TR_Y + (TR_H / 2 if v else -TR_H / 2)  # noqa: E731
    x = TR_X0 + k * TR_W
    if k == 0:
        return wire((x, y(1)), (x + TR_W, y(1)), color=YELLOW)
    return wire((x, y(CLK_LEVELS[k - 1])), (x, y(CLK_LEVELS[k])), (x + TR_W, y(CLK_LEVELS[k])), color=YELLOW)


def up_arrow(k):
    return Triangle().scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(TR_X0 + k * TR_W, TR_Y))


# ---- layout of the symbols comparison -----------------------------------------------------
BOX_Y = 1.5
A_SCALE, A_X = 1.2, 3.3            # clip 1 / first half of clip 2: latch at -A_X, flip-flop at +A_X
B_X = (-4.75, -0.35, 4.4)          # from {bubble}: latch, flip-flop (scale 1), bubble flip-flop
LAB_Y, GOLD_Y, TR_Y2 = (-1.6, -2.08), -2.75, -3.4


def two_line(a, b, x, ca=FG):
    l1 = T(a, 32, ca).move_to(_p(x, LAB_Y[0]))
    l2 = T(b, 32, ca).move_to(_p(x, LAB_Y[1]))
    return VGroup(l1, l2)


class Symbols(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c2.symbol.1
    def clip1(self):
        with self.say("c2.symbol.1") as c:
            circ = master_slave_end_shot()
            self.play(FadeIn(circ), run_time=1.0)
            ff = place(make_ff(), A_SCALE, (A_X, BOX_Y))
            self.ff = ff
            self.play(*during(circ.animate.scale(0.45).move_to(ff.box).set_opacity(0), 0, 0.5),
                      *during(FadeIn(ff, scale=0.8), 0.45, 1.0),
                      run_time=min(1.8, c.until("terms")))
            self.remove(circ)
            c.wait_until("terms")
            latch = make_latch()
            place(latch, A_SCALE, (-A_X, BOX_Y))
            self.latch = latch
            self.play(*appear(latch, shift=None), run_time=min(1.2, c.until("A latch")))
            self.lab_l = two_line("latch:", "level-triggered", -A_X)
            self.lab_f = two_line("flip-flop:", "edge-triggered", A_X)
            c.wait_until("A latch")
            self.play(*appear(self.lab_l, lag=0.4), run_time=1.2)
            c.wait_until("and a flip-flop")
            self.play(*appear(self.lab_f, lag=0.4), run_time=1.2)
            self.gold = T("99 times out of 100", 32, GOLD).move_to(_p(A_X, GOLD_Y))
            c.wait_until("ninety-nine")
            self.play(*appear(self.gold), run_time=1.0)

    # ------------------------------------------------------------------ c2.symbol.2
    def clip2(self):
        latch, ff = self.latch, self.ff
        with self.say("c2.symbol.2") as c:
            self.play(*flash([latch.sq, ff.tri], run_time=1.5, time_width=1.5, buff=0.08),
                      run_time=min(1.5, c.until("square")))
            c.wait_until("square")
            self.play(latch.sq.animate.set_stroke(YELLOW), FlashAround(latch.sq, run_time=1.5, buff=0.08),
                      run_time=1.5)
            self.tr_l = tiny_trace((-A_X, TR_Y2), "level")
            c.wait_until("which means")
            self.play(*appear(self.tr_l, shift=None), run_time=1.0)

            c.wait_until("triangle")
            self.play(ff.tri.animate.set_stroke(YELLOW), FlashAround(ff.tri, run_time=1.5, buff=0.08),
                      run_time=1.5)
            self.tr_f = tiny_trace((A_X, TR_Y2), "rise")
            c.wait_until("rising edge")
            self.play(*appear(self.tr_f, shift=None), run_time=1.0)

            # {bubble}: make room on the right, then the third, smaller flip-flop
            c.wait_until("bubble")
            lx, fx, bx = B_X
            tl = latch.copy()
            place(tl, 1.0 / A_SCALE, (lx, BOX_Y))
            tf = ff.copy()
            place(tf, 1.0 / A_SCALE, (fx, BOX_Y))
            self.play(Transform(latch, tl), Transform(ff, tf),
                      self.lab_l.animate.set_x(lx), self.tr_l.animate.set_x(lx),
                      self.lab_f.animate.set_x(fx), self.gold.animate.set_x(fx), self.tr_f.animate.set_x(fx),
                      run_time=1.5)
            bff = place(make_ff(bubble=True), 0.85, (bx, BOX_Y))
            self.bff = bff
            self.play(*appear(bff, shift=None), run_time=1.0)
            c.wait_until("complement")
            self.play(bff.bub.animate.set_stroke(YELLOW), FlashAround(bff.bub, run_time=1.5, buff=0.08),
                      run_time=1.5)
            self.tag_b = T("falling edge", 32, YELLOW).move_to(_p(bx, LAB_Y[0]))
            self.tr_b = tiny_trace((bx, TR_Y2), "fall")
            c.wait_until("falling edge")
            self.play(*appear(self.tag_b, self.tr_b, lag=0.3), run_time=1.2)

            c.wait_until("ripple")
            self.tag_r = T("part 4: ripple counter", 28, DIM).move_to(_p(bx, GOLD_Y))
            self.play(*appear(self.tag_r), run_time=1.0)

            # {data}: D = data, and the title over the box
            c.wait_until("data")
            self.data_l = T("D = data", 34, BLUE)
            self.data_l.next_to(ff.d_w, DOWN, buff=0.25).align_to(ff.box.get_left() + 0.15 * LEFT, RIGHT)
            self.play(*fly(ff.d_l, self.data_l), run_time=1.5)
            self.title = T("D flip-flop", 44).next_to(ff.box, UP, buff=0.35)
            self.play(*appear(self.title), run_time=1.0)

    # ------------------------------------------------------------------ c2.symbol.3
    def clock(self, v, k, rt, extra=()):
        d = self.demo
        anims = [flip(d.sw_c, v), lev(d.w["clk"], v), lev(d.w["nclk"], 1 - v),
                 d.dot.animate.set_fill(opacity=1.0 if (1 - v) else LOW_OP), lev(d.w["clk2"], v),
                 Create(self.tr[k])]
        if k in self.ups:
            anims.append(FadeIn(self.ups[k]))
        self.play(*during(anims, 0, 0.5 if extra else 1.0), *extra, run_time=rt)

    def clip3(self):
        with self.say("c2.symbol.3") as c:
            d = demo_circuit()
            self.demo = d
            self.tr = [trace_piece(k) for k in range(len(CLK_LEVELS))]
            self.ups = {k: up_arrow(k) for k in range(1, len(CLK_LEVELS))
                        if CLK_LEVELS[k] == 1}
            self.tr_lab = T("CLK", 30, YELLOW).move_to(_p(TR_X0 - 0.75, TR_Y))
            # clear the symbols board completely first (appear's lag spans let sweep_clear start them early)
            self.play(FadeOut(*self.mobjects), run_time=0.8)
            self.play(*appear(d.core, d.ins, d.outs, shift=None, lag=0.3), run_time=min(1.8, c.until("start")))  # early: the demo circuit shown whole
            c.wait_until("start")
            w = d.w
            self.play(flip(d.sw_c, 1), lev(w["d"], 0), lev(w["qint"], 0), lev(w["q"], 0),
                      lev(w["nclk"], 0), d.dot.animate.set_fill(opacity=LOW_OP), set_led(d.led_qb, True),
                      FadeIn(self.tr_lab), Create(self.tr[0]),
                      run_time=1.5)
            c.wait_until("setd")
            self.play(flip(d.sw_d, 1), lev(w["d"], 1), run_time=1.0)
            c.wait_until("nothing happens")
            self.play(FlashAround(d.led_q, color=GREEN, run_time=1.2, buff=0.12), run_time=1.2)
            c.wait_until("fall")
            self.clock(0, 1, 1.6, extra=during(lev(w["qint"], 1), 0.5, 1.0))
            c.wait_until("only the master")
            path = w["qint"].copy().set_stroke(TEAL, 10, opacity=1)
            self.play(VShowPassingFlash(path, time_width=0.6), FlashAround(d.master.name_l, color=TEAL),
                      run_time=min(1.5, c.until()))

    # ------------------------------------------------------------------ c2.symbol.4
    def clip4(self):
        d, w = self.demo, self.demo.w
        with self.say("c2.symbol.4") as c:
            self.clock(1, 2, 1.6, extra=during([lev(w["q"], 1), lev(w["qb"], 0), set_led(d.led_q, True),
                                                set_led(d.led_qb, False)], 0.5, 1.0))
            c.wait_until("more")
            for k in (3, 4, 5, 6):
                self.clock(CLK_LEVELS[k], k, 0.5)
                self.wait(0.15)
            c.wait_until("zero")
            self.clock(0, 7, 0.9)
            c.wait_until("set dee back")
            self.play(*during([flip(d.sw_d, 0), lev(w["d"], 0)], 0, 0.5),
                      *during(lev(w["qint"], 0), 0.3, 0.8), run_time=1.4)
            c.wait_until("waits")
            self.play(FlashAround(d.led_q, color=GREEN, run_time=1.2, buff=0.12), run_time=1.2)
            c.wait_until("edge")
            self.clock(1, 8, 1.6, extra=during([lev(w["q"], 0), lev(w["qb"], 1), set_led(d.led_q, False),
                                                set_led(d.led_qb, True)], 0.5, 1.0))
            c.wait_until("edgeaction")
            self.play(*flash(list(self.ups.values()), run_time=1.5, time_width=1.5, buff=0.08),
                      run_time=1.5)

    # ------------------------------------------------------------------ c2.symbol.5
    def clip5(self):
        with self.say("c2.symbol.5") as c:
            head = T("D Flip-Flops", 48).move_to(_p(0, 2.6))
            # the whole demo leaves together (sweep_clear's lagged per-object fade let the boxes go first)
            self.play(FadeOut(*self.mobjects), run_time=min(1.0, 0.5 * c.until("superseded")))
            self.play(*appear(head), run_time=min(1.0, c.until("superseded")))  # early: the slide's heading
            l1 = T("Master-slave: superseded by new flip-flop circuits", 36).move_to(_p(0, 1.15))
            l1b = T("easier to implement, better performance", 32, DIM).move_to(_p(0, 0.5))
            l2 = T("use truly edge-triggered flip-flops", 36, t2c={"edge-triggered": YELLOW}).move_to(_p(0, -0.75))
            l3 = T("their design: not on this course", 32, DIM).move_to(_p(0, -1.9))
            c.wait_until("superseded")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("easier")
            self.play(*appear(l1b), run_time=1.0)
            c.wait_until("use")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("inside")
            self.play(*appear(l3), run_time=1.0)
            c.wait_until("box")
            ff = place(make_ff(), FINAL_SCALE, (0, FINAL_Y))
            sweep_clear(self, *appear(ff, shift=None), run_time=min(1.6, c.until()))


FINAL_SCALE, FINAL_Y = 1.5, 0.55     # final box: 4.8 x 5.4 overall, box 2.25 x 3.9 centred (0, 0.55)
