"""Chapter 2, scene 4: timing diagram, part 1: the clocks, D, and the master's output Q_int.
Clips c2.master.1 – c2.master.4.

The five-row timing diagram is owned here (`timing_diagram()`); ch2_s5_slave continues it.
The circuit at the top is s3's end shot (`master_slave_end_shot()`, helpers copied from ch2_s3).
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


# ---- copied verbatim from ch2_s3_masterslave.py (circuit, end pose, door) ----------------------
def _p(x, y):
    return np.array([x, y, 0.0])


# ---- latch box (matches ch2_s1_hook.make_latch) ------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_DY = 0.6          # D and Q pins sit 0.6 above the box centre
WIRE_W = 5


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


def wire(*pts, color=FG, width=WIRE_W):
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
PIN_Y = CY + PIN_DY              # 0.8: D / Q_int / Q wire height
CLK_Y = -2.3                     # clock line
EN_Y = CY - BOX_H / 2 - 0.1      # bottom of the enable square
X_IN, X_OUT = -5.3, 5.3          # D wire start, Q wire end
INV1_X, INV2_X = -4.3, 0.0
TOP_Y = 2.85                     # tag / door row (above the Master / Slave labels)


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

        self.d_wire = wire((X_IN, PIN_Y), (MX - BOX_W / 2, PIN_Y), color=BLUE)
        self.lab_d = T("D", 40, BLUE).next_to(self.d_wire.get_start(), LEFT, buff=0.18)
        self.qint_wire = wire((MX + BOX_W / 2, PIN_Y), (SX - BOX_W / 2, PIN_Y), color=TEAL)
        self.lab_qint = MathTex(r"Q_{\mathrm{int}}", font_size=44, color=TEAL).move_to(_p(0, PIN_Y + 0.42))
        self.q_wire = wire((SX + BOX_W / 2, PIN_Y), (X_OUT, PIN_Y), color=GREEN)
        self.lab_q = T("Q", 40, GREEN).next_to(self.q_wire.get_end(), RIGHT, buff=0.18)

        self.clk_wire = wire((X_IN, CLK_Y), (INV1_X - 0.4, CLK_Y), color=YELLOW, width=6)
        self.lab_clk = MathTex(r"\mathrm{CLK}", font_size=40, color=YELLOW)
        self.lab_clk.next_to(self.clk_wire.get_start(), LEFT, buff=0.15)
        self.inv1 = inverter(INV1_X, CLK_Y).set_z_index(1)
        self.clkb_wire = wire((INV1_X + 0.46, CLK_Y), (MX, CLK_Y), (MX, EN_Y), color=YELLOW, width=6)
        self.node = Dot(_p(MX, CLK_Y), radius=0.09, color=YELLOW)
        self.mid_wire = wire((MX, CLK_Y), (INV2_X - 0.4, CLK_Y), color=YELLOW, width=6)
        self.inv2 = inverter(INV2_X, CLK_Y).set_z_index(1)
        self.clk2_wire = wire((INV2_X + 0.46, CLK_Y), (SX, CLK_Y), (SX, EN_Y), color=YELLOW, width=6)
        self.lab_clkb = MathTex(r"\overline{\mathrm{CLK}}", font_size=40, color=YELLOW)
        self.lab_clkb.move_to(_p(MX - 0.62, (EN_Y + CLK_Y) / 2))
        self.lab_clk2 = MathTex(r"\mathrm{CLK}", font_size=40, color=YELLOW)
        self.lab_clk2.move_to(_p(SX - 0.62, (EN_Y + CLK_Y) / 2))
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


# ---- airlock door ----------------------------------------------------------------------------------
def door_icon(is_open, height=0.8, color=None):
    """Airlock door, `height` tall, 0.65 * height wide. Shut: FG frame filled by a RED panel with
    a BG knob. Open: GREEN frame, dark doorway, a GREEN panel swung out on the left hinge.
    `color` overrides both (DIM for a ghost). Parts .frame .panel .knob (None when open)."""
    h, w = height, 0.65 * height
    col = color or (GREEN if is_open else RED)
    frame = Rectangle(width=w, height=h).set_stroke(color or (GREEN if is_open else FG), 3).set_fill(BG, 1)
    g = VGroup(frame)
    if is_open:
        swing = 0.42 * w
        panel = Polygon(_p(-w / 2, h / 2), _p(-w / 2, -h / 2), _p(-w / 2 - swing, -h / 2 - 0.1 * h),
                        _p(-w / 2 - swing, h / 2 + 0.1 * h))
        panel.set_stroke(col, 2).set_fill(col, 0.85)
        knob = None
        g.add(panel)
    else:
        panel = Rectangle(width=w - 0.12 * h, height=h - 0.12 * h).set_stroke(width=0).set_fill(col, 0.9)
        knob = Dot(_p(w / 2 - 0.2 * w, 0), radius=0.045 * h / 0.8, color=BG)
        g.add(panel, knob)
    g.frame, g.panel, g.knob, g.is_open = frame, panel, knob, is_open
    return g



# ---- the five-row timing diagram (owned here; s5 continues it) ------------------------------
ROW_COLORS = [YELLOW, YELLOW, BLUE, TEAL, GREEN]


class TimingDiagram(VGroup):
    """Slide p. 88 timing diagram. Rows 0..4 = CLK, CLK-bar, D, Q_int, Q at .row_y[i]
    (top 0.88, pitch 0.875); levels at row_y ± AMP (0.2). Waves run x0 = -5.2 → x1 = 3.0, period P.
    CLK starts high, falls at .fall[0] = x0 + 0.4P, then regular: .rise[k] = fall[k] + P/2,
    .fall[k+1] = fall[k] + P (k = 0..4); the wave ends 0.2P after rise[4], high.
    Parts: .labels (MathTex, start DIM), .guides (rise[0..3], DIM), .ups (▲ on CLK at rise[0..4])."""
    AMP = 0.2

    def __init__(self, x0=-5.2, x1=3.0, top=0.88, pitch=0.875, **kw):
        super().__init__(**kw)
        P = (x1 - x0) / 5.1
        self.x0, self.x1, self.P = x0, x1, P
        self.fall = [x0 + 0.4 * P + k * P for k in range(5)]
        self.rise = [f + 0.5 * P for f in self.fall]
        self.row_y = [top - i * pitch for i in range(5)]
        texs = [r"\mathrm{CLK}", r"\overline{\mathrm{CLK}}", "D", r"Q_{\mathrm{int}}", "Q"]
        self.labels = VGroup(*[
            MathTex(t, font_size=40, color=DIM).move_to(_p(0, y)).align_to(_p(x0 - 0.35, 0, ), RIGHT)
            for t, y in zip(texs, self.row_y)])
        g_top, g_bot = self.row_y[0] + self.AMP + 0.12, self.row_y[4] - self.AMP - 0.12
        self.guides = VGroup(*[Line(_p(x, g_top), _p(x, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2)
                               for x in self.rise[:4]])
        self.ups = VGroup(*[Triangle().scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1)
                            .move_to(_p(x, self.row_y[0])) for x in self.rise])
        self.add(self.labels)

    def y(self, row, bit):
        return self.row_y[row] + (self.AMP if bit else -self.AMP)

    def path(self, row, pts, color=None, width=4):
        """Polyline at row levels: pts = [(x, bit), ...]; a change of bit at the same x is a step."""
        return (VMobject().set_points_as_corners([_p(x, self.y(row, b)) for x, b in pts])
                .set_stroke(color or ROW_COLORS[row], width))

    def clk_wave(self, row=0):
        pts = [(self.x0, 1)]
        for f, r in zip(self.fall, self.rise):
            pts += [(f, 1), (f, 0), (r, 0), (r, 1)]
        pts.append((self.x1, 1))
        return self.path(row, pts, YELLOW)


def timing_diagram():
    return TimingDiagram()


def small_arrow(a, b, color=TEAL):
    return Arrow(a, b, buff=0, stroke_width=3, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35).set_color(color)


class Master(NarratedScene):
    def construct(self):
        self.circ = master_slave_end_shot()
        self.td = timing_diagram()
        td = self.td
        self.x_rise = td.rise[0] + 0.25 * td.P        # D steps up, mid CLK-high after r1
        self.x_fall = td.rise[2] + 0.2 * td.P         # D steps down, just after r3
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        td, circ = self.td, self.circ
        with self.say("c2.master.1") as c:
            self.play(FadeIn(circ), run_time=1.0)          # s3's end shot fades back in (handoff)
            self.play(*appear(*td.labels, lag=0.15, shift=0.2 * RIGHT),  # early: the diagram's empty frame, rows filled one by one
                      run_time=min(1.6, c.until("clk")))
            c.wait_until("clk")
            self.clk = td.clk_wave(0)
            self.play(Create(self.clk), td.labels[0].animate.set_color(YELLOW),
                      run_time=min(1.6, c.until("notclk")), rate_func=linear)
            c.wait_until("notclk")
            self.clkb = self.clk.copy()
            self.play(self.clkb.animate.flip(RIGHT).move_to(_p(self.clk.get_x(), td.row_y[1])),
                      td.labels[1].animate.set_color(YELLOW),
                      run_time=min(1.8, c.until("edges")))
            c.wait_until("edges")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(u, shift=0.15 * DOWN), GrowFromEdge(g, UP))
                                    for u, g in zip(td.ups[:4], td.guides)], lag_ratio=0.35),
                      run_time=min(2.4, c.until("neglect")))
            self.play(FadeIn(td.ups[4], shift=0.15 * DOWN), run_time=0.6)
            c.wait_until("neglect")
            self.note = T("Note propagation\ndelays have been\nneglected in the\ntiming diagram",
                          28, color=DIM, line_spacing=1.0)
            self.note.move_to(_p(0, (td.row_y[0] + td.row_y[1]) / 2)).align_to(_p(3.5, 0), LEFT)
            self.play(*appear(self.note), run_time=1.2)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        td = self.td
        tag_y = (td.y(1, 0) + td.y(2, 1)) / 2
        with self.say("c2.master.2") as c:
            self.d0 = td.path(2, [(td.x0, 0), (self.x_rise, 0)])
            self.play(Create(self.d0), td.labels[2].animate.set_color(BLUE),
                      run_time=min(2.0, c.until("rise")), rate_func=linear)
            c.wait_until("rise")
            self.d1 = td.path(2, [(self.x_rise, 0), (self.x_rise, 1), (self.x_fall, 1)])
            self.tag1 = T("CLK high", 28, color=YELLOW).move_to(_p(0, tag_y)).align_to(
                _p(td.rise[0] + 0.1, 0), LEFT)
            self.play(Create(self.d1), run_time=min(1.6, c.until("fall")))
            self.play(*appear(self.tag1), run_time=1.0)
            c.wait_until("fall")
            self.d2 = td.path(2, [(self.x_fall, 1), (self.x_fall, 0), (td.x1, 0)])
            self.tag2 = T("CLK high", 28, color=YELLOW).move_to(_p(0, tag_y)).align_to(
                _p(td.rise[2] + 0.1, 0), LEFT)
            self.play(Create(self.d2), run_time=min(1.6, c.until("note")))
            self.play(*appear(self.tag2), run_time=1.0)
            c.wait_until("note")
            self.play(*flash([self.tag1, self.tag2]), run_time=2.0)

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        td = self.td
        with self.say("c2.master.3") as c:
            self.play(td.labels[3].animate.set_color(TEAL), *flash([td.labels[3]], color=TEAL),
                      *disappear(self.tag1, self.tag2), run_time=min(1.5, c.until("rule")))
            c.wait_until("rule")
            # CLK-bar is high where CLK is low: flash those stretches
            highs = [Line(_p(f, td.y(1, 1)), _p(r, td.y(1, 1))) for f, r in zip(td.fall, td.rise)]
            self.play(*[VShowPassingFlash(h.copy().set_stroke(TEAL, 9), time_width=0.6) for h in highs],
                      run_time=min(1.8, c.until("shade")))
            c.wait_until("shade")
            hgt = 2 * td.AMP
            self.shades = VGroup(*[Rectangle(width=r - f, height=hgt).set_stroke(width=0)
                                   .set_fill(TEAL, 0.18).move_to(_p((f + r) / 2, td.row_y[3]))
                                   .set_z_index(-1) for f, r in zip(td.fall, td.rise)])
            sw = Square(0.3).set_stroke(width=0).set_fill(TEAL, 0.35)
            self.open_tag = VGroup(sw, T("master open", 28, color=TEAL)).arrange(RIGHT, buff=0.15)
            self.open_tag.move_to(_p(0, td.row_y[3])).align_to(_p(3.5, 0), LEFT)
            self.play(LaggedStart(*[FadeIn(s) for s in self.shades], lag_ratio=0.2),
                      run_time=min(1.5, c.until("unknown")))
            self.play(*appear(self.open_tag), run_time=1.0)
            c.wait_until("unknown")
            self.q_hi0 = td.path(3, [(td.x0, 1), (td.fall[0], 1)])
            self.q_lo0 = td.path(3, [(td.x0, 0), (td.fall[0], 0)])
            self.play(Create(self.q_hi0), Create(self.q_lo0), run_time=min(1.5, c.until("both")))
            c.wait_until("both")
            self.play(FlashAround(VGroup(self.q_hi0.copy(), self.q_lo0.copy()), color=TEAL,
                                  time_width=1.5, buff=0.12), run_time=min(2.0, c.until("copy")))
            c.wait_until("copy")
            self.play(Flash(_p(td.fall[0], td.row_y[0]), color=YELLOW, flash_radius=0.3),
                      run_time=1.0)
            c.wait_until("The master opens")
            xa = td.fall[0] + 0.15
            self.arr0 = small_arrow(_p(xa, td.y(2, 0)), _p(xa, td.y(3, 0) + 0.04))
            self.q1 = td.path(3, [(td.fall[0], 1), (td.fall[0], 0), (td.rise[0], 0)])
            self.play(GrowArrow(self.arr0), run_time=1.0)
            self.play(Create(self.q1), run_time=min(1.5, c.until()))

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        td, circ = self.td, self.circ
        with self.say("c2.master.4") as c:
            self.q2 = td.path(3, [(td.rise[0], 0), (self.x_rise, 0)])
            self.play(Create(self.q2), FlashAround(circ.master.box, color=RED, time_width=1.5),
                      run_time=min(1.8, c.until("drise")))
            c.wait_until("drise")
            self.door = door_icon(False, height=0.55).move_to(circ.master.box.get_center()).set_z_index(3)
            self.play(FlashAround(self.d1, color=BLUE, time_width=1.5, buff=0.08),
                      run_time=min(1.5, c.until("But the master is shut")))
            c.wait_until("But the master is shut")
            self.q3 = td.path(3, [(self.x_rise, 0), (td.fall[1], 0)])
            self.play(FadeIn(self.door, scale=0.7), Create(self.q3),
                      run_time=min(1.5, c.until("catch")))
            c.wait_until("catch")
            self.arr1 = small_arrow(_p(self.x_rise, td.y(2, 1)), _p(td.fall[1] - 0.03, td.y(3, 1) + 0.03))
            self.q4 = td.path(3, [(td.fall[1], 0), (td.fall[1], 1), (td.rise[1], 1)])
            self.play(FadeOut(self.door, scale=0.7), GrowArrow(self.arr1),
                      run_time=1.2)
            self.play(Create(self.q4), run_time=min(1.5, c.until("stay")))
            c.wait_until("stay")
            self.q5 = td.path(3, [(td.rise[1], 1), (self.x_fall, 1)])
            self.play(Create(self.q5), run_time=min(2.2, c.until("dfall")), rate_func=linear)
            c.wait_until("dfall")
            self.door2 = door_icon(False, height=0.55).move_to(circ.master.box.get_center()).set_z_index(3)
            self.q6 = td.path(3, [(self.x_fall, 1), (td.fall[3], 1)])
            self.play(FadeIn(self.door2, scale=0.7), Create(self.q6),
                      run_time=min(1.5, c.until("catch2")))
            c.wait_until("catch2")
            self.arr2 = small_arrow(_p(self.x_fall, td.y(2, 0)), _p(td.fall[3] - 0.03, td.y(3, 1) - 0.03))
            self.q7 = td.path(3, [(td.fall[3], 1), (td.fall[3], 0), (td.x1, 0)])
            self.play(FadeOut(self.door2, scale=0.7), GrowArrow(self.arr2), run_time=1.0)
            self.play(Create(self.q7), run_time=min(1.8, c.until("pattern")))
            c.wait_until("pattern")
            self.caption = MathTex(r"Q_{\mathrm{int}}\text{ follows }D\text{ while CLK is low, "
                                   r"and freezes while CLK is high}", font_size=34)
            self.caption.move_to(_p(-0.3, -3.3))
            self.caption[0][0:4].set_color(TEAL)
            self.caption[0][11].set_color(BLUE)
            self.play(*appear(self.caption), run_time=1.2)
        # the voice reads the caption aloud; clear it (and the helper arrows) for the end shot
        self.play(*disappear(self.caption, self.arr0, self.arr1, self.arr2), run_time=0.8)
        self.wait(0.6)
