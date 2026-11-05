"""Chapter 1, scene 3: a flip-flop's three numbers (set-up, hold, clock-to-Q) around one rising
edge, the GOLD "keep D still" window, and why it is a window (L6's master-slave doors).
Clips c1.window.1 – c1.window.4.

Owned here and copied by ch1_s8 (recap), ch2 (hold) and ch4 (violated window), grep, don't import:
  dim_arrow(...)       lecture-wide dimension arrow (thin double-headed line, small tips, grey guides)
  WindowDiagram(...)   CLK / D / Q square traces round one edge, t_su / t_hold / t_pc, the GOLD band
(between the `# ====` rulers below). L6's master-slave helpers are copied verbatim from
../l06-flip-flops-counters/scenes/ch2_s3_masterslave.py.
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


# ---- copied from L6 ch2_s3_masterslave.py (latch_box ... door_icon), unchanged -------------------
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



# ==================================================================================================
# Lecture-wide dimension arrow + the CLK / D / Q "keep D still" diagram.
# ch1_s8 (recap), ch2 (hold) and ch4 (violated window) copy this block verbatim.
# ==================================================================================================
def dim_arrow(a, b, color, base_a=None, base_b=None, width=3, tip=0.14):
    """Dimension arrow from point a to point b (same y): a thin double-headed line in the
    interval's colour, small tips, and thin DIM vertical guides at both ends running from the
    arrow (0.15 past it) to base_a / base_b (the y the interval is measured on; None = no guide).
    Parts .arrow .guides; the label goes beside it in the same colour."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    arrow = DoubleArrow(a, b, buff=0, stroke_width=width, tip_length=tip,
                        max_tip_length_to_length_ratio=0.4).set_color(color)
    guides = VGroup()
    for p, base in ((a, base_a), (b, base_b)):
        if base is None:
            continue
        over = 0.15 if base < p[1] else -0.15
        guides.add(Line(_p(p[0], base), _p(p[0], p[1] + over)).set_stroke(DIM, 1.5))
    g = VGroup(guides, arrow)
    g.arrow, g.guides = arrow, guides
    return g


class WindowDiagram:
    """Slide p. 104's first diagram in L6's square timing style: rows CLK (YELLOW), D (BLUE),
    Q (GREEN), one rising edge at x = 0 with a thin DIM guide down all rows.
    Geometry in diagram units, mapped by P(x, y) = origin + k * (x, y): rows at y = 2, 0, -2,
    levels +-0.3, waves x -4.6 .. 4.6; CLK high, falls at -2.3, rises at 0, falls at 2.3;
    D rises at -T_SU, falls at +T_HOLD; Q rises at +T_PC. Fonts scale by fs (min 28 for prose).
    Every part is a separate mobject (add / animate them one by one):
      lab_clk lab_d lab_q (MathTex)  guide  up (▲ on the edge)  clk d q (paths)
      su hold pc (dim_arrow: GOLD, GOLD, PINK)  sym_su sym_hold sym_pc (MathTex beside the arrows)
      band (GOLD fill 0.2, from t_su before to t_hold after, over the D row)  band_lab "keep D still"
      one_d (BLUE "1" on D at the edge)  one_q (GREEN "1" on Q after its rise)
      words=True adds word_su "set-up time", word_hold "hold time", note_hold "(slide: t_h)",
      word_pc "clock-to-Q delay" (big pose only).
    .d_change(x) -> RED dashed vertical change of D at x;  .q_unknown() -> RED "???" on Q.
    .parts(names) -> list of those parts;  CORE = names of the parts both poses share."""
    T_SU, T_HOLD, T_PC = 1.3, 1.0, 1.7
    X0, X1, PITCH, AMP = -4.6, 4.6, 2.0, 0.3
    CORE = ["lab_clk", "lab_d", "lab_q", "guide", "up", "clk", "d", "q", "su", "hold", "pc",
            "sym_su", "sym_hold", "sym_pc", "band", "band_lab", "one_d", "one_q"]

    def __init__(self, origin=ORIGIN, k=1.0, fs=1.0, words=True):
        self.o, self.k, self.fs = np.array(origin, dtype=float), k, fs
        P, A, H = self.P, self.AMP, self.PITCH
        self.row_y = [H, 0.0, -H]
        sw = 4 * max(k, 0.8)
        self.lab_clk, self.lab_d, self.lab_q = [
            MathTex(t, font_size=44 * fs, color=c).move_to(P(0, y)).align_to(P(self.X0 - 0.3, 0), RIGHT)
            for t, c, y in zip([r"\mathrm{CLK}", "D", "Q"], [YELLOW, BLUE, GREEN], self.row_y)]
        self.guide = Line(P(0, H + A + 0.3), P(0, -H - A - 0.2)).set_stroke(DIM, 1.5).set_z_index(-2)
        self.up = (Triangle().scale(0.12 * max(k, 0.8)).set_stroke(width=0).set_fill(YELLOW, 1)
                   .move_to(P(0, H)))
        self.clk = self.path(0, [(self.X0, 1), (-2.3, 1), (-2.3, 0), (0, 0), (0, 1), (2.3, 1),
                                 (2.3, 0), (self.X1, 0)], YELLOW, sw)
        self.d = self.path(1, [(self.X0, 0), (-self.T_SU, 0), (-self.T_SU, 1), (self.T_HOLD, 1),
                               (self.T_HOLD, 0), (self.X1, 0)], BLUE, sw)
        self.q = self.path(2, [(self.X0, 0), (self.T_PC, 0), (self.T_PC, 1), (self.X1, 1)], GREEN, sw)
        ya, yp = A + 0.55, -H - A - 0.45
        self.su = dim_arrow(P(-self.T_SU, ya), P(0, ya), GOLD, P(0, A)[1], P(0, A)[1])
        self.hold = dim_arrow(P(0, ya), P(self.T_HOLD, ya), GOLD, P(0, A)[1], P(0, A)[1])
        self.pc = dim_arrow(P(0, yp), P(self.T_PC, yp), PINK, P(0, -H - A)[1], P(0, -H - A)[1])
        mt = 44 * fs
        self.sym_su = MathTex(r"t_{\mathrm{su}}", font_size=mt, color=GOLD).next_to(self.su.arrow, LEFT, buff=0.15)
        self.sym_hold = MathTex(r"t_{\mathrm{hold}}", font_size=mt, color=GOLD).next_to(self.hold.arrow, RIGHT, buff=0.15)
        self.sym_pc = MathTex(r"t_{\mathrm{pc}}", font_size=mt, color=PINK).next_to(self.pc.arrow, RIGHT, buff=0.15)
        self.band = (Rectangle(width=k * (self.T_SU + self.T_HOLD), height=k * (2 * A + 0.3))
                     .set_stroke(width=0).set_fill(GOLD, 0.25).set_z_index(-3)
                     .move_to(P((self.T_HOLD - self.T_SU) / 2, 0)))
        self.band_lab = T("keep D still", max(28, 32 * fs), GOLD).next_to(self.band, DOWN, buff=0.15)
        self.one_d = T("1", max(28, 36 * fs), BLUE).move_to(P(-0.6, 0))
        self.one_q = T("1", max(28, 36 * fs), GREEN).move_to(P(2.9, -H))
        if words:
            self.word_su = T("set-up time", 32 * fs, GOLD).next_to(self.sym_su, LEFT, buff=0.25)
            self.word_hold = T("hold time", 32 * fs, GOLD).next_to(self.sym_hold, RIGHT, buff=0.25)
            self.note_hold = MathTex(r"(\text{slide: }t_{\mathrm{h}})", font_size=32 * fs, color=DIM)
            self.note_hold.next_to(self.word_hold, DOWN, buff=0.15, aligned_edge=LEFT)
            self.word_pc = T("clock-to-Q delay", 32 * fs, PINK).next_to(self.sym_pc, RIGHT, buff=0.25)

    def P(self, x, y):
        return self.o + self.k * np.array([x, y, 0.0])

    def path(self, row, pts, color, width):
        y0 = self.row_y[row]
        return (VMobject().set_points_as_corners([self.P(x, y0 + (self.AMP if b else -self.AMP)) for x, b in pts])
                .set_stroke(color, width))

    def d_change(self, x, color=RED):
        return DashedLine(self.P(x, self.AMP), self.P(x, -self.AMP), dash_length=0.1).set_stroke(color, 4)

    def q_unknown(self):
        return T("???", max(30, 38 * self.fs), RED).move_to(self.one_q)

    def parts(self, names):
        return [getattr(self, n) for n in names]
# ==================================================================================================


def draw_partial(mob, full, a0, a1, **kw):
    """Draw path `mob` from fraction a0 to a1 of `full` (mob shows full[0:a] as it goes)."""
    return UpdateFromAlphaFunc(mob, lambda m, a: m.pointwise_become_partial(full, 0, a0 + (a1 - a0) * a), **kw)


def door_panel_pts(door, f):
    """The door's panel at swing fraction f (0 = open as door_icon(True), 1 = shut)."""
    c, h, w = door.frame.get_center(), door.frame.height, door.frame.width
    s, m = 0.42 * w, 0.06 * h
    opn = [(-w / 2, h / 2), (-w / 2, -h / 2), (-w / 2 - s, -h / 2 - 0.1 * h), (-w / 2 - s, h / 2 + 0.1 * h)]
    sht = [(-w / 2 + m, h / 2 - m), (-w / 2 + m, -h / 2 + m), (w / 2 - m, -h / 2 + m), (w / 2 - m, h / 2 - m)]
    pts = [c + _p(*((1 - f) * np.array(a) + f * np.array(b))) for a, b in zip(opn, sht)]
    return pts + [pts[0]]


def swing(door, f0, f1, **kw):
    """The open door's panel swings from fraction f0 to f1, GREEN turning RED."""
    def upd(m, a):
        f = f0 + (f1 - f0) * a
        col = interpolate_color(ManimColor(GREEN), ManimColor(RED), f)
        m.set_points_as_corners(door_panel_pts(door, f))
        m.set_fill(col, 0.85 + 0.05 * f).set_stroke(col, 2 * (1 - f))
    return UpdateFromAlphaFunc(door.panel, upd, **kw)


def travel(dot, path, color=None, **kw):
    """Dot moves along path; with color, it turns that colour over the last third."""
    c0 = dot.get_color()

    def upd(m, a):
        m.move_to(path.point_from_proportion(smooth(a)))
        if color is not None:
            m.set_color(interpolate_color(ManimColor(c0), ManimColor(color), min(1, max(0, (a - 0.66) * 3))))
    return UpdateFromAlphaFunc(dot, upd, **kw)


BIG = dict(origin=_p(0, 0.3), k=1.0, fs=1.0)
SMALL = dict(origin=_p(-2.6, 0.3), k=0.6, fs=0.85, words=False)
PAIR_CENTER = _p(3.75, 0.75)


class FFNumbers(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c1.window.1: one edge; set-up and hold ---------------------------------------------------
    def clip1(self):
        g = self.g = WindowDiagram(**BIG)
        with self.say("c1.window.1") as c:
            # {ff}: the three rows, named
            self.play(*appear(g.lab_clk, g.lab_d, g.lab_q, lag=0.3), run_time=1.5)  # early: the rows are named as a set, then walked
            c.wait_until("rising edge")
            self.play(GrowFromCenter(g.guide), run_time=1.0)
            # {edge}: the clock, its rising edge marked
            c.wait_until("edge")
            self.play(Create(g.clk), run_time=1.8, rate_func=linear)
            self.play(FadeIn(g.up, shift=0.15 * UP), FlashAround(g.up, color=YELLOW, buff=0.12), run_time=1.0)
            c.wait_until("input")
            self.play(FlashAround(g.lab_d, color=BLUE, time_width=1.5), run_time=1.0)
            c.wait_until("output")
            self.play(FlashAround(g.lab_q, color=GREEN, time_width=1.5), run_time=1.0)
            # {setup}: D rises a little before the edge
            c.wait_until("setup")
            self.d_full = g.d.copy()
            g.d.pointwise_become_partial(self.d_full, 0, 0)
            self.add(g.d)
            self.play(draw_partial(g.d, self.d_full, 0, 0.6), run_time=2.0, rate_func=linear)
            self.play(FadeIn(g.su.guides), GrowFromCenter(g.su.arrow), run_time=1.0)
            c.wait_until("set-up time")
            self.play(*appear(g.sym_su, g.word_su, lag=0.2), run_time=1.0)
            # {hold}: D falls a little after the edge
            c.wait_until("hold")
            self.play(draw_partial(g.d, self.d_full, 0.6, 1.0), run_time=1.5, rate_func=linear)
            self.play(FadeIn(g.hold.guides), GrowFromCenter(g.hold.arrow), run_time=1.0)
            c.wait_until("hold time")
            self.play(*appear(g.sym_hold, g.word_hold, g.note_hold, lag=0.2), run_time=min(1.2, c.until(floor=0.6)))

    # -- c1.window.2: the window, clock-to-Q, the data sheet ---------------------------------------
    def clip2(self):
        g = self.g
        with self.say("c1.window.2") as c:
            # {window}: the GOLD band over the D row
            self.play(FadeIn(g.band), FlashAround(g.band, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=g.band_lab)
            self.play(*appear(g.band_lab), run_time=1.0)
            # {q}: Q answers a little later
            c.wait_until("q")
            self.play(Create(g.q), run_time=1.8, rate_func=linear)
            c.wait_until("the time from")
            self.play(FadeIn(g.pc.guides), GrowFromCenter(g.pc.arrow), run_time=1.0)
            c.wait_until("clock-to-cue")
            self.play(*appear(g.sym_pc, g.word_pc, lag=0.2), run_time=1.0)
            # {follows}: D's value at the edge, then Q's
            c.wait_until("value")
            self.play(*appear(g.one_d), run_time=1.0)
            c.wait_until("that value is one")
            self.play(*appear(g.one_q), run_time=1.0)
            # {datasheet}: the words leave, the diagram shrinks left, a data-sheet card arrives
            c.wait_until("datasheet")
            self.s = s = WindowDiagram(**SMALL)
            words = [g.word_su, g.word_hold, g.note_hold, g.word_pc]
            self.play(*during(disappear(*words), 0, 0.4),
                      *during([Transform(a, b) for a, b in zip(g.parts(g.CORE), s.parts(s.CORE))], 0.4, 1.0),
                      run_time=1.8)
            self.card = self.make_card()
            self.play(*appear(self.card, shift=0.4 * LEFT), run_time=1.0)
            c.wait_until("data sheet")
            self.play(FlashUnder(self.card.head, color=FG, time_width=1.5), run_time=min(1.5, c.until(floor=0.5)))

    def make_card(self):
        head = T("Timing characteristics", 34)
        rows = VGroup()
        for tex, col, word in ((r"t_{\mathrm{su}}", GOLD, "set-up time"),
                               (r"t_{\mathrm{hold}}", GOLD, "hold time"),
                               (r"t_{\mathrm{pc}}", PINK, "clock-to-Q delay")):
            sym = MathTex(tex, font_size=40, color=col)
            wd = T(word, 28, DIM)
            val = T("… ns", 30)
            rows.add(VGroup(sym, wd, val))
        x_sym, x_wd, x_val = -2.55, -1.35, 2.6
        for i, (sym, wd, val) in enumerate(rows):
            y = -0.62 * i
            sym.move_to(_p(x_sym, y), aligned_edge=LEFT)
            wd.move_to(_p(x_wd, y), aligned_edge=LEFT)
            val.move_to(_p(x_val, y), aligned_edge=RIGHT)
        head.next_to(rows, UP, buff=0.45)
        rule = Line(_p(-2.6, 0), _p(2.6, 0)).set_stroke(DIM, 1.5).move_to(
            (head.get_bottom() + rows.get_top()) / 2)
        body = VGroup(head, rule, rows)
        box = RoundedRectangle(corner_radius=0.15, width=body.width + 0.6, height=body.height + 0.6)
        box.set_stroke(DIM, 2).set_fill("#171A20", 1).move_to(body)
        card = VGroup(box, body).move_to(PAIR_CENTER + 0.1 * DOWN)
        card.head = head
        return card

    # -- c1.window.3: why a window: the master's door ---------------------------------------------
    def clip3(self):
        s = self.s
        with self.say("c1.window.3") as c:
            # {why}
            self.play(self.g.band.animate(rate_func=there_and_back).set_fill(GOLD, 0.6), run_time=1.5)
            c.wait_until("simplified picture")
            ms = self.ms = master_slave_end_shot().scale(1.1).move_to(PAIR_CENTER)
            self.door_m = door_icon(True, height=0.62).next_to(ms.lab_master, UP, buff=0.18)
            self.door_s = door_icon(False, height=0.62).next_to(ms.lab_slave, UP, buff=0.18)
            pin_y = ms.d_wire.get_y()
            x_in = ms.d_wire.get_start()[0]
            self.dot = Dot(_p(x_in + 0.35, pin_y), radius=0.11, color=BLUE).set_z_index(5)
            tx0, tx1, ty = ms.get_left()[0] + 0.9, ms.get_right()[0] - 0.9, ms.get_bottom()[1] - 0.75
            self.tr_mid = (tx0 + tx1) / 2
            self.trace_lo = (VMobject().set_points_as_corners([_p(tx0, ty - 0.2), _p(self.tr_mid, ty - 0.2)])
                             .set_stroke(YELLOW, 4))
            self.trace_hi = (VMobject().set_points_as_corners(
                [_p(self.tr_mid, ty - 0.2), _p(self.tr_mid, ty + 0.2), _p(tx1, ty + 0.2)]).set_stroke(YELLOW, 4))
            self.play(*disappear(self.card), run_time=0.8)
            self.play(*appear(ms, self.door_m, self.door_s, shift=None, lag=0.2),  # early: the circuit arrives whole; Master / Slave are named as the story reaches them
                      Create(self.trace_lo), run_time=1.6)
            self.play(FadeIn(self.dot, scale=0.5), run_time=0.6)
            self.tag = T("simplified picture", 30, DIM)
            self.tag.next_to(self.trace_lo, DOWN, buff=0.4).set_x(PAIR_CENTER[0])
            self.play(*appear(self.tag), run_time=0.8)
            # the dot gets inside the open master before the edge
            box = ms.master.box
            self.p_in = VMobject().set_points_as_corners([self.dot.get_center(), _p(box.get_left()[0] + 0.3, pin_y)])
            self.play(travel(self.dot, self.p_in), run_time=max(0.8, min(1.4, c.until("shut") - 0.1)))
            # {shut}: the edge; the master's door swings most of the way shut
            c.wait_until("shut")
            self.play(Create(self.trace_hi), swing(self.door_m, 0, 0.7), run_time=min(2.6, c.until("inside") - 0.3))
            c.wait_until("inside")
            self.play(FlashAround(self.dot, color=BLUE, time_width=1.5, buff=0.08), run_time=1.0)
            c.wait_until("that's the setup time")
            self.play(FlashAround(VGroup(s.su.arrow, s.sym_su), color=GOLD, time_width=1.5), run_time=1.5)
            # {still}: the door finishes its slow swing; the dot sits still
            c.wait_until("still")
            knob = door_icon(False, height=0.62).knob.move_to(self.door_m.frame.get_center()
                                                              + _p(0.3 * self.door_m.frame.width, 0))
            knob.set_opacity(0)
            self.door_m.add(knob)
            self.play(swing(self.door_m, 0.7, 1.0), rate_func=linear,
                      run_time=max(1.5, min(3.6, c.until("that's the hold time") - 0.3)))
            self.play(knob.animate.set_opacity(1), self.door_m.frame.animate.set_stroke(FG), run_time=0.5)
            c.wait_until("that's the hold time")
            self.play(FlashAround(VGroup(s.hold.arrow, s.sym_hold), color=GOLD, time_width=1.5), run_time=1.5)
            # {slave}: the slave's door opens; the value travels on to Q
            c.wait_until("slave passes")
            ds2 = door_icon(True, height=0.62).move_to(self.door_s)
            ds2.shift(self.door_s.frame.get_center() - ds2.frame.get_center())
            self.play(*swap(self.door_s, ds2), run_time=1.0)
            self.door_s = ds2
            sbox = ms.slave.box
            path = VMobject().set_points_as_corners([self.dot.get_center(), _p(sbox.get_right()[0] + 0.05, pin_y),
                                                     _p(ms.q_wire.get_end()[0] - 0.15, pin_y)])
            self.play(travel(self.dot, path, color=GREEN), run_time=1.6)
            self.tick = MathTex(r"t_{\mathrm{pc}}", font_size=36, color=PINK).next_to(ms.q_wire, UP, buff=0.12)
            self.play(*appear(self.tick), run_time=0.8)
            c.wait_until("that's the", nth=2)
            self.play(FlashAround(VGroup(s.pc.arrow, s.sym_pc), color=PINK, time_width=1.5),
                      run_time=min(1.3, c.until(floor=0.5) - 0.1))

    # -- c1.window.4: the caveat; a change inside the window; our job ------------------------------
    def clip4(self):
        g = self.g
        with self.say("c1.window.4") as c:
            # {caveat}
            self.play(FlashUnder(self.tag, color=FG, time_width=1.5), self.tag.animate.set_color(FG), run_time=1.2)
            # {plant}: the pair goes; the diagram returns to full size; D changes inside the band
            c.wait_until("plant")
            b = WindowDiagram(**BIG)
            pair = [self.ms, self.door_m, self.door_s, self.dot, self.trace_lo, self.trace_hi,
                    self.tick, self.tag]
            self.play(*during(disappear(*pair), 0, 0.45),
                      *during([Transform(a, z) for a, z in zip(g.parts(g.CORE), b.parts(b.CORE))], 0.45, 1.0),
                      run_time=1.8)
            bad = b.d_change(0.45)
            unk = b.q_unknown()
            self.play(Create(bad), *swap(g.one_q, unk), run_time=1.2)
            part4 = T("Part 4", 30, RED).next_to(unk, UP, buff=0.25)
            c.wait_until(own_word=part4)
            self.play(*appear(part4), run_time=1.0)
            # {job}: the change moves out of the band; Q is a clean 1 again; the band is ticked
            c.wait_until("job")
            x_ok = -b.T_SU - 0.45
            self.play(bad.animate.move_to(b.P(x_ok, 0)).set_color(BLUE), run_time=1.5)
            # outside the band it is a legal change: it becomes D's own solid BLUE edge
            new_d = b.path(1, [(b.X0, 0), (x_ok, 0), (x_ok, 1), (b.T_HOLD, 1), (b.T_HOLD, 0), (b.X1, 0)],
                           BLUE, g.d.get_stroke_width())
            one_q = b.one_q.copy()
            tick = check_mark().next_to(g.band_lab, RIGHT, buff=0.25)
            self.play(Transform(g.d, new_d), FadeOut(bad), *swap(unk, one_q), *disappear(part4), run_time=1.0)
            self.play(*appear(tick, shift=None), FlashAround(g.band, color=GREEN, time_width=1.5),
                      run_time=min(1.2, c.until(floor=0.5)))
