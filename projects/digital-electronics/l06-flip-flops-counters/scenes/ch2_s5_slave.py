"""Chapter 2, scene 5: timing diagram, part 2: the slave's output Q. Clips c2.slave.1 – c2.slave.5.

Opens on ch2_s4_master's end shot (rebuilt from copies of s4's TimingDiagram and s3's
master_slave_end_shot() / door_icon()). Row positions: ROW_TOP / ROW_PITCH (follow s4).
Ends on s3's circuit alone at its end-shot position (bbox centred (0, 2.45)), as s6 opens from it.
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


# ---- copied from ch2_s3_masterslave (the circuit and the airlock doors; don't import) -------
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


# ---- this scene's handles on s3's end-shot circuit ---------------------------------------------
def ms_circuit():
    """s3's end shot (bbox centred (0, 2.45), y 1.38..3.52), with the short names this scene uses."""
    ms = master_slave_end_shot()
    ms.box_m, ms.box_s = ms.master.box, ms.slave.box
    ms.w_mid, ms.w_out, ms.w_clk, ms.lab_qi = ms.qint_wire, ms.q_wire, ms.clk2_wire, ms.lab_qint
    return ms


DOOR_ON_BOX = 0.55      # door icon height when it sits on a latch box (box is 0.63 x 1.09 here)
DOOR_BESIDE = 0.62      # the airlock doors beside the circuit
DOORS_X, DOORS_Y = (-5.05, -4.05), 2.45


def shut_door(at, height=DOOR_ON_BOX):
    return door_icon(False, height).move_to(at).set_z_index(3)


def open_door(at, height=DOOR_ON_BOX):
    return door_icon(True, height).move_to(at).set_z_index(3)


# ---- the five-row timing diagram (copied from ch2_s4_master) ---------------------------------
# Row positions live HERE only: s4 is moving its rows down to clear s3's circuit; update to match.
ROW_TOP, ROW_PITCH = 0.88, 0.875   # s4: rows y 0.88 ... -2.62


ROW_COLORS = [YELLOW, YELLOW, BLUE, TEAL, GREEN]


class TimingDiagram(VGroup):
    AMP = 0.2

    def __init__(self, x0=-5.2, x1=3.0, top=1.75, pitch=1.05, **kw):
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
        return (VMobject().set_points_as_corners([_p(x, self.y(row, b)) for x, b in pts])
                .set_stroke(color or ROW_COLORS[row], width))

    def clk_wave(self, row=0):
        pts = [(self.x0, 1)]
        for f, r in zip(self.fall, self.rise):
            pts += [(f, 1), (f, 0), (r, 0), (r, 1)]
        pts.append((self.x1, 1))
        return self.path(row, pts, YELLOW)


def timing_diagram():
    return TimingDiagram(top=ROW_TOP, pitch=ROW_PITCH)


def small_arrow(a, b, color=TEAL):
    return Arrow(a, b, buff=0, stroke_width=3, tip_length=0.16,
                 max_tip_length_to_length_ratio=0.35).set_color(color)


# ---- helpers of this scene ------------------------------------------------------------------
def glow(td, row, x_a, x_b, bit, color, width=10):
    """A bright pulse running along a flat stretch of a row (removes itself)."""
    seg = Line(_p(x_a, td.y(row, bit)), _p(x_b, td.y(row, bit))).set_stroke(color, width)
    return VShowPassingFlash(seg, time_width=1.0, taper_width=0.1)


def blip(td, row, a, b, color):
    return DashedVMobject(td.path(row, [(a, 0), (a, 1), (b, 1), (b, 0)], color, width=4),
                          num_dashes=14, dashed_ratio=0.55)


class Slave(NarratedScene):
    def construct(self):
        self.rebuild_s4_end()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        # the diagram clears; the circuit stays alone at its top position for s6
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.circ], run_time=1.2)
        self.wait(1.0)
        self.play(FadeOut(self.circ), run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def rebuild_s4_end(self):
        """ch2_s4_master's last frame, exactly."""
        self.circ = ms_circuit()
        self.td = td = timing_diagram()
        x_rise = td.rise[0] + 0.25 * td.P
        x_fall = td.rise[2] + 0.2 * td.P
        for lab, col in zip(td.labels, [YELLOW, YELLOW, BLUE, TEAL, DIM]):
            lab.set_color(col)
        self.clk = td.clk_wave(0)
        self.clkb = self.clk.copy()
        self.clkb.flip(RIGHT).move_to(_p(self.clk.get_x(), td.row_y[1]))
        self.note = T("Note propagation\ndelays have been\nneglected in the\ntiming diagram",
                      28, color=DIM, line_spacing=1.0)
        self.note.move_to(_p(0, (td.row_y[0] + td.row_y[1]) / 2)).align_to(_p(3.5, 0), LEFT)
        self.dwave = td.path(2, [(td.x0, 0), (x_rise, 0), (x_rise, 1), (x_fall, 1), (x_fall, 0),
                                 (td.x1, 0)])
        hgt = 2 * td.AMP
        self.shades = VGroup(*[Rectangle(width=r - f, height=hgt).set_stroke(width=0)
                               .set_fill(TEAL, 0.18).move_to(_p((f + r) / 2, td.row_y[3]))
                               .set_z_index(-1) for f, r in zip(td.fall, td.rise)])
        sw = Square(0.3).set_stroke(width=0).set_fill(TEAL, 0.35)
        self.open_tag = VGroup(sw, T("master open", 28, color=TEAL)).arrange(RIGHT, buff=0.15)
        self.open_tag.move_to(_p(0, td.row_y[3])).align_to(_p(3.5, 0), LEFT)
        self.qi_hi0 = td.path(3, [(td.x0, 1), (td.fall[0], 1)])
        self.qi_lo0 = td.path(3, [(td.x0, 0), (td.fall[0], 0)])
        self.qi = td.path(3, [(td.fall[0], 1), (td.fall[0], 0), (td.fall[1], 0), (td.fall[1], 1),
                              (td.fall[3], 1), (td.fall[3], 0), (td.x1, 0)])
        # handoff: s4 fades this shot out to an empty frame; it fades back in here
        self.play(*[FadeIn(m) for m in (self.circ, td, self.clk, self.clkb, *td.guides, *td.ups,
                                        self.note, self.dwave, *self.shades, self.open_tag,
                                        self.qi_hi0, self.qi_lo0, self.qi)], run_time=1.0)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        td, circ = self.td, self.circ
        with self.say("c2.slave.1") as c:
            self.play(FlashAround(circ.box_s, color=GREEN, time_width=1.5, buff=0.08),
                      circ.box_s.animate.set_stroke(GREEN, 3),
                      run_time=min(1.5, c.until("Its input")))
            c.wait_until("Its input")
            self.play(VShowPassingFlash(circ.w_mid.copy().set_stroke(TEAL, 8), time_width=0.6),
                      FlashAround(circ.lab_qi, color=TEAL, time_width=1.5),
                      run_time=min(1.5, c.until("enable")))
            c.wait_until("enable")
            self.play(VShowPassingFlash(circ.w_clk.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      run_time=min(1.5, c.until("rule")))
            c.wait_until("rule")
            # the slave is open where CLK is high
            spans = [(td.x0, td.fall[0])] + [(td.rise[k], td.fall[k + 1]) for k in range(4)] + \
                    [(td.rise[4], td.x1)]
            hgt = 2 * td.AMP
            self.gshades = [Rectangle(width=b - a, height=hgt).set_stroke(width=0)
                            .set_fill(GREEN, 0.14).move_to(_p((a + b) / 2, td.row_y[4])).set_z_index(-1)
                            for a, b in spans]
            rt = min(1.8, c.until("start"))
            self.play(*[s.animate.set_fill(opacity=0.07) for s in self.shades],
                      self.open_tag.animate.set_opacity(0.4),
                      td.labels[4].animate.set_color(GREEN),
                      *[time_span(FadeIn(g), 0.12 * i, 0.12 * i + 1.0) for i, g in enumerate(self.gshades)],
                      run_time=max(rt, 1.6))
            sw = Square(0.3).set_stroke(width=0).set_fill(GREEN, 0.3)
            self.slave_tag = VGroup(sw, T("slave open", 28, color=GREEN)).arrange(RIGHT, buff=0.15)
            self.slave_tag.move_to(_p(0, td.row_y[4])).align_to(_p(3.5, 0), LEFT)
            self.play(*appear(self.slave_tag), run_time=1.0)  # early: legend for the green shading, which "transparent while the clock is high" names
            c.wait_until("start")
            self.play(glow(td, 0, td.x0, td.fall[0], 1, YELLOW),
                      run_time=min(1.6, c.until("which is unknown")))
            c.wait_until("which is unknown")
            # Q_int before f1 sits at both levels: unknown
            self.play(glow(td, 3, td.x0, td.fall[0], 1, TEAL, 12),
                      glow(td, 3, td.x0, td.fall[0], 0, TEAL, 12),
                      FlashAround(VGroup(self.qi_hi0.copy(), self.qi_lo0.copy()), color=TEAL,
                                  time_width=1.5, buff=0.12),
                      run_time=min(1.4, c.until("unknown", nth=1)))
            c.wait_until("unknown", nth=1)
            self.q_hi0 = td.path(4, [(td.x0, 1), (td.rise[0], 1)])
            self.q_lo0 = td.path(4, [(td.x0, 0), (td.rise[0], 0)])
            self.play(Create(self.q_hi0), Create(self.q_lo0), rate_func=linear,
                      run_time=min(2.0, c.until()))

    # ------------------------------------------------------------------------------------------
    def edge_arrow(self, k, bit):
        td = self.td
        x = td.rise[k] + 0.15
        return small_arrow(_p(x, td.y(3, bit) - 0.03), _p(x, td.y(4, bit) + 0.03))

    def touch(self, k, bit):
        """Q_int's level just before edge k glows: what the master is holding."""
        td = self.td
        return glow(td, 3, td.rise[k] - 0.45 * td.P, td.rise[k], bit, TEAL, 10)

    def clip2(self):
        td, circ = self.td, self.circ
        with self.say("c2.slave.2") as c:
            guide0 = td.guides[0]
            self.play(VShowPassingFlash(guide0.copy().set_stroke(YELLOW, 5), time_width=0.8),
                      Flash(td.ups[0].get_center(), color=YELLOW, flash_radius=0.3),
                      FlashAround(circ.box_s, color=GREEN, time_width=1.5, buff=0.08),
                      run_time=min(1.6, c.until("holding a zero")))
            c.wait_until("holding a zero")
            self.arrs = [self.edge_arrow(0, 0)]
            self.q1 = td.path(4, [(td.rise[0], 1), (td.rise[0], 0), (td.fall[1], 0)])
            self.play(GrowArrow(self.arrs[0]), self.touch(0, 0), run_time=1.0)
            self.play(Create(self.q1), run_time=min(1.5, c.until("low1")))
            c.wait_until("low1")
            self.q2 = td.path(4, [(td.fall[1], 0), (td.rise[1], 0)])
            f_edge = Line(_p(td.fall[1], td.y(0, 1)), _p(td.fall[1], td.y(0, 0))).set_stroke(YELLOW, 9)
            self.play(Create(self.q2), VShowPassingFlash(f_edge, time_width=1.0),
                      Flash(_p(td.fall[1], td.y(0, 0)), color=YELLOW, flash_radius=0.25),
                      rate_func=linear, run_time=min(2.0, c.until("e2")))
            c.wait_until("e2")
            # e2: up to 1
            self.arrs.append(self.edge_arrow(1, 1))
            self.q3 = td.path(4, [(td.rise[1], 0), (td.rise[1], 1), (td.rise[2], 1)])
            self.play(GrowArrow(self.arrs[1]), self.touch(1, 1), run_time=0.9)
            self.play(Create(self.q3), run_time=min(1.6, c.until("e3")))
            c.wait_until("e3")
            # e3: stays at 1
            self.arrs.append(self.edge_arrow(2, 1))
            self.q4 = td.path(4, [(td.rise[2], 1), (td.rise[3], 1)])
            self.eq = set_backstroke(MathTex("=", font_size=40, color=YELLOW).move_to(
                _p(td.rise[2], td.row_y[4])), width=8)
            self.play(GrowArrow(self.arrs[2]), self.touch(2, 1), run_time=0.9)
            self.play(Create(self.q4), FadeIn(self.eq, scale=0.6), run_time=min(1.6, c.until("e4")))
            c.wait_until("e4")
            # e4: down to 0
            self.arrs.append(self.edge_arrow(3, 0))
            self.q5 = td.path(4, [(td.rise[3], 1), (td.rise[3], 0), (td.x1, 0)])
            self.play(GrowArrow(self.arrs[3]), self.touch(3, 0), run_time=0.9)
            self.play(Create(self.q5), run_time=min(1.8, c.until()))
        self.qwave = [self.q1, self.q2, self.q3, self.q4, self.q5]

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        td, circ = self.td, self.circ
        vals = [0, 1, 1, 0]
        with self.say("c2.slave.3") as c:
            self.door = shut_door(circ.box_m.get_center())
            self.play(*disappear(*self.arrs), FadeIn(self.door, scale=0.7),
                      circ.box_s.animate.set_stroke(FG, 3), run_time=1.0)
            self.play(*[glow(td, 3, td.rise[k], td.fall[k + 1], v, TEAL) for k, v in enumerate(vals)],
                      *[glow(td, 4, td.rise[k], td.fall[k + 1], v, GREEN) for k, v in enumerate(vals)],
                      run_time=min(2.0, c.until("cycle")))
            c.wait_until("cycle")
            steps = [Line(_p(td.rise[k], td.y(4, 0)), _p(td.rise[k], td.y(4, 1))).set_stroke(YELLOW, 8)
                     for k in range(4)]
            self.play(FadeOut(self.door, scale=0.7), run_time=0.8)
            self.play(*[time_span(VShowPassingFlash(s, time_width=1.0), 0.35 * k, 0.35 * k + 0.9)
                        for k, s in enumerate(steps)],
                      *[time_span(FlashAround(VGroup(s.copy()), color=YELLOW, buff=0.1), 0.35 * k,
                                  0.35 * k + 0.9) for k, s in enumerate(steps)],
                      run_time=1.95)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        td, circ = self.td, self.circ
        bits = [0, 1, 1, 0]
        with self.say("c2.slave.4") as c:
            self.play(*disappear(self.eq),
                      *[time_span(g.animate.set_stroke(FG, 2.5), 0.4 * k, 0.4 * k + 0.8)
                        for k, g in enumerate(td.guides)],
                      run_time=min(2.0, max(c.until("d_at"), 2.0)))
            c.wait_until("d_at")
            self.play(*[glow(td, 2, td.rise[k] - 0.4 * td.P, td.rise[k], b, BLUE, 9)
                        for k, b in enumerate(bits)],
                      run_time=min(1.5, c.until("Zero, one, one, zero")))
            c.wait_until("Zero, one, one, zero")
            self.dvals = [set_backstroke(MathTex(str(b), font_size=34, color=BLUE)
                                         .move_to(_p(td.rise[k] - 0.22, td.row_y[2])), width=8)
                          for k, b in enumerate(bits)]
            self.play(*appear(*self.dvals, lag=0.5, shift=0.15 * UP),
                      run_time=min(2.4, c.until("q_at")))
            c.wait_until("q_at")
            self.play(*[glow(td, 4, td.rise[k], td.rise[k] + 0.4 * td.P, b, GREEN, 9)
                        for k, b in enumerate(bits)],
                      run_time=min(1.5, c.until("Zero, one, one, zero", nth=1)))
            c.wait_until("Zero, one, one, zero", nth=1)
            self.qvals = [set_backstroke(MathTex(str(b), font_size=34, color=GREEN)
                                         .move_to(_p(td.rise[k] + 0.22, td.row_y[4])), width=8)
                          for k, b in enumerate(bits)]
            self.play(*appear(*self.qvals, lag=0.5, shift=0.15 * UP),
                      run_time=min(2.4, c.until("takes")))
            c.wait_until("takes")
            cols = [VGroup(d.copy(), q.copy()) for d, q in zip(self.dvals, self.qvals)]
            self.play(*[time_span(FlashAround(col, color=YELLOW, buff=0.12, time_width=1.5),
                                  0.5 * k, 0.5 * k + 1.2) for k, col in enumerate(cols)],
                      run_time=2.7)
            c.wait_until("words")
            self.words = T("See Q changes on\nrising edge of CLK", 30, line_spacing=1.0,
                           t2c={"Q": GREEN, "rising edge": YELLOW, "CLK": YELLOW})
            self.words.move_to(_p(0, 3.0)).align_to(_p(3.2, 0), LEFT)
            self.play(*appear(self.words), run_time=1.2)

    # ------------------------------------------------------------------------------------------
    def clip5(self):
        td, circ = self.td, self.circ
        a_hi, b_hi = td.rise[3] + 0.15 * td.P, td.rise[3] + 0.35 * td.P
        a_lo, b_lo = td.fall[4] + 0.1 * td.P, td.fall[4] + 0.32 * td.P
        with self.say("c2.slave.5") as c:
            self.play(*disappear(*self.dvals, *self.qvals),
                      *[g.animate.set_stroke(DIM, 1.5) for g in td.guides], run_time=0.9)
            self.blip_hi = blip(td, 2, a_hi, b_hi, DIM)
            self.blip_lo = blip(td, 2, a_lo, b_lo, DIM)
            self.play(time_span(Create(self.blip_hi), 0, 1.0), time_span(Create(self.blip_lo), 0.5, 1.5),
                      run_time=1.5)
            c.wait_until("high")
            self.door_m = shut_door(circ.box_m.get_center())
            self.play(FadeIn(self.door_m, scale=0.7),
                      FlashAround(self.blip_hi, color=YELLOW, time_width=1.5, buff=0.1),
                      glow(td, 0, td.rise[3], td.fall[4], 1, YELLOW, 8),
                      run_time=min(1.5, c.until("stopped")))
            c.wait_until("stopped")
            self.play(glow(td, 3, td.rise[3], td.fall[4], 0, TEAL),
                      glow(td, 4, td.rise[3], td.fall[4], 0, GREEN),
                      run_time=min(1.5, c.until("low")))
            c.wait_until("low")
            self.play(FadeOut(self.door_m, scale=0.7),
                      FlashAround(self.blip_lo, color=YELLOW, time_width=1.5, buff=0.1),
                      glow(td, 0, td.fall[4], td.rise[4], 0, YELLOW, 8),
                      run_time=min(1.4, c.until("gets into")))
            c.wait_until("gets into")
            self.qi_blip = blip(td, 3, a_lo, b_lo, TEAL)
            self.play(*fly(self.blip_lo, self.qi_blip), run_time=min(1.5, c.until("but the slave")))
            c.wait_until("but the slave")
            self.door_s = shut_door(circ.box_s.get_center())
            self.play(FadeIn(self.door_s, scale=0.7), glow(td, 4, td.fall[4], td.rise[4], 0, GREEN),
                      run_time=min(1.4, c.until("gone")))
            c.wait_until("gone")
            self.play(Flash(td.ups[4].get_center(), color=YELLOW, flash_radius=0.3),
                      FlashAround(self.qi_blip, color=TEAL, time_width=1.5, buff=0.1),
                      run_time=min(1.2, c.until("only")))
            c.wait_until("only")
            self.play(FadeOut(self.door_s, scale=0.7),
                      glow(td, 4, td.rise[3], td.x1, 0, GREEN, 12),
                      run_time=min(1.6, c.until("value at the rising")))
            c.wait_until("value at the rising")
            dbits = [0, 1, 1, 0, 0]
            self.dots = [Dot(_p(td.rise[k], td.y(2, b)), radius=0.1, color=YELLOW).set_z_index(2)
                         for k, b in enumerate(dbits)]
            self.play(*[time_span(FadeIn(d, scale=0.4), 0.3 * k, 0.3 * k + 0.6)
                        for k, d in enumerate(self.dots)], run_time=1.8)
            c.wait_until("airlock")
            # s3's airlock doors, small beside the circuit (master left, slave right): CLK low, master open, slave shut
            self.m_open = open_door(_p(DOORS_X[0], DOORS_Y), DOOR_BESIDE)
            self.s_shut = shut_door(_p(DOORS_X[1], DOORS_Y), DOOR_BESIDE)
            self.play(FadeIn(self.m_open, scale=0.7), FadeIn(self.s_shut, scale=0.7),
                      run_time=min(1.2, c.until("At the rising edge", nth=1)))
            c.wait_until("At the rising edge", nth=1)
            self.play(Flash(td.ups[4].get_center(), color=YELLOW, flash_radius=0.3), run_time=1.0)
            c.wait_until("shuts")
            self.m_shut = shut_door(_p(DOORS_X[0], DOORS_Y), DOOR_BESIDE)
            self.s_open = open_door(_p(DOORS_X[1], DOORS_Y), DOOR_BESIDE)
            self.play(*swap(self.m_open, self.m_shut, shift=None),
                      *swap(self.s_shut, self.s_open, shift=None),
                      run_time=min(1.4, c.until("one moment")))
            c.wait_until("one moment")
            self.play(VShowPassingFlash(circ.w_mid.copy().set_stroke(TEAL, 9), time_width=0.6),
                      VShowPassingFlash(circ.w_out.copy().set_stroke(GREEN, 9), time_width=0.6),
                      run_time=1.6)
