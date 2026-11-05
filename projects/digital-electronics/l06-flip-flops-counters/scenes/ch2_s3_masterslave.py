"""Chapter 2, scene 3: two latches, back to back (slide p. 87's master-slave circuit, the clock
with its two inverters, the open/shut phases, the airlock). Clips c2.pair.1 – c2.pair.4.

Owned here and reused by s4–s7 (grep, copy, don't import):
  latch_box(center, stubs=False)  s1's latch look (box 1.5 x 2.6, FG outline, D/Q/EN inside, 0.2 square)
  MasterSlave()                   the whole p. 87 circuit at full size (parts listed in its docstring)
  master_slave_end_shot()         the circuit at this scene's end pose (s4 opens from it)
  door_icon(is_open, height)      the airlock door: open GREEN, shut RED
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


# ---- scene helpers -------------------------------------------------------------------------------
def dim_latch(lb, op):
    return [m.animate.set_opacity(op) if m is not lb.box else m.animate.set_stroke(opacity=op, width=4)
            for m in (lb.box, lb.lab_d, lb.lab_q, lb.lab_en)]


def open_latch(lb):
    return [lb.box.animate.set_stroke(FG, 8, opacity=1),
            *[m.animate.set_opacity(1) for m in (lb.lab_d, lb.lab_q, lb.lab_en)]]


def paint(parts, color):
    return [m.animate.set_color(color) for m in parts]


def passing(w, color, width=10, time_width=0.5):
    return VShowPassingFlash(w.copy().set_stroke(color, width), time_width=time_width)


def dot_path(stop_at_slave=False):
    """D -> through the master (dipping under its D/Q labels) -> Q_int -> (slave) -> Q."""
    dy = PIN_Y - 0.42
    pts = [(X_IN, PIN_Y), (MX - BOX_W / 2 - 0.05, PIN_Y), (MX - BOX_W / 2 + 0.2, dy),
           (MX + BOX_W / 2 - 0.2, dy), (MX + BOX_W / 2 + 0.05, PIN_Y)]
    if stop_at_slave:
        pts.append((SX - BOX_W / 2 - 0.14, PIN_Y))
    else:
        pts += [(SX - BOX_W / 2 - 0.05, PIN_Y), (SX - BOX_W / 2 + 0.2, dy),
                (SX + BOX_W / 2 - 0.2, dy), (SX + BOX_W / 2 + 0.05, PIN_Y), (X_OUT - 0.1, PIN_Y)]
    return VMobject().set_points_as_corners([_p(*p) for p in pts])


class MasterSlaveScene(NarratedScene):
    def construct(self):
        self.ms = MasterSlave()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- c2.pair.1: the two latches, master and slave -----------------------------------------
    def clip1(self):
        ms = self.ms
        # s1's {answer} pair: full latches with their stubs at (+-2.3, -0.4)
        pm, ps = latch_box(_p(-2.3, -0.4), stubs=True), latch_box(_p(2.3, -0.4), stubs=True)
        self.play(*appear(pm, ps, shift=None, lag=0.2), run_time=0.8)
        with self.say("c2.pair.1") as c:
            # {two}: the boxes move into place; s1's stubs fade (the circuit's wires replace them)
            self.remove(pm, ps)
            self.add(*pm.stubs, *ps.stubs, ms.master, ms.slave)
            ms.master.shift(pm.box.get_center() - ms.master.box.get_center())
            ms.slave.shift(ps.box.get_center() - ms.slave.box.get_center())
            self.play(ms.master.animate.shift(_p(MX, CY) - pm.box.get_center()),
                      ms.slave.animate.shift(_p(SX, CY) - ps.box.get_center()),
                      *[FadeOut(s) for s in pm.stubs + ps.stubs], run_time=2.0)
            c.wait_until("master")
            self.play(*appear(ms.lab_master), run_time=1.0)
            c.wait_until("It takes the input")
            self.play(Create(ms.d_wire), *during(appear(ms.lab_d, shift=None), 0.0, 0.5), run_time=1.5)
            c.wait_until("qint")
            self.play(Create(ms.qint_wire), run_time=1.5)
            c.wait_until("called")
            self.play(*appear(ms.lab_qint), run_time=1.0)
            c.wait_until("slave", own_word=ms.lab_slave)
            self.play(*appear(ms.lab_slave), run_time=1.0)
            c.wait_until("q")
            self.play(Create(ms.q_wire), *during(appear(ms.lab_q, shift=None), 0.6, 1.0), run_time=1.5)
            c.wait_until("names")
            self.arrow = Arrow(_p(-0.75, PIN_Y - 0.38), _p(0.75, PIN_Y - 0.38), buff=0, color=TEAL,
                               stroke_width=5, max_tip_length_to_length_ratio=0.2)
            self.play(GrowArrow(self.arrow), run_time=1.2)
            c.wait_until("The slave only ever copies")
            self.play(passing(ms.qint_wire, TEAL), FlashAround(ms.lab_slave, color=TEAL, time_width=1.5),
                      run_time=1.6)

    # -- c2.pair.2: the clock and its two inverters --------------------------------------------
    def clip2(self):
        ms = self.ms
        with self.say("c2.pair.2") as c:
            self.play(*appear(ms.lab_clk, shift=None), *during([Create(ms.clk_wire)], 0.3, 1.0),
                      run_time=1.2)
            c.wait_until("inv1")
            self.play(FadeIn(ms.inv1), *during([Create(ms.clkb_wire)], 0.35, 1.0), run_time=2.0)
            c.wait_until("not clock")
            self.play(*appear(ms.lab_clkb), run_time=1.0)
            c.wait_until("inv2")
            self.play(FadeIn(ms.node, scale=0.5), Create(ms.mid_wire), run_time=1.0)
            self.play(FadeIn(ms.inv2), *during([Create(ms.clk2_wire)], 0.35, 1.0), run_time=1.6)
            c.wait_until("double")
            self.play(Succession(FlashAround(ms.inv1.bubble, color=YELLOW, time_width=1.5, buff=0.08),
                                 FlashAround(ms.inv2.bubble, color=YELLOW, time_width=1.5, buff=0.08)),
                      run_time=1.8)
            self.notnot = T("not not CLK = CLK", 30, t2c={"CLK": YELLOW}).move_to(_p(INV2_X, -3.05))
            c.wait_until("so the slave sees")
            self.play(*appear(self.notnot, shift=None), run_time=1.0)
            c.wait_until("original clock")
            self.play(*appear(ms.lab_clk2), run_time=1.0)
            c.wait_until("both")
            self.play(passing(ms.clkb_wire, YELLOW, 12, 0.6), passing(ms.clk2_wire, YELLOW, 12, 0.6),
                      run_time=1.8)

    # -- c2.pair.3: never both transparent; the airlock -----------------------------------------
    def clip3(self):
        ms = self.ms
        with self.say("c2.pair.3") as c:
            # {never}: CLK low: CLK wires dim, CLK-bar bright
            self.play(FadeOut(self.arrow), *paint(ms.clk_part, DIM), run_time=1.2)
            c.wait_until("low")
            self.tag_m = T("transparent", 32, GREEN).move_to(_p(MX, TOP_Y))
            self.play(*open_latch(ms.master), *appear(self.tag_m, shift=None),
                      passing(ms.d_wire, BLUE, 10, 0.6), run_time=1.5)
            self.play(passing(ms.qint_wire, TEAL, 10, 0.6), run_time=1.0)
            c.wait_until("the slave is shut")
            self.tag_s = T("hold", 32, RED).move_to(_p(SX, TOP_Y))
            self.play(*dim_latch(ms.slave, 0.35), *appear(self.tag_s, shift=None), run_time=1.2)
            # {high}: CLK high, and the roles swap
            c.wait_until("high")
            self.play(*paint(ms.clk_part, YELLOW), *paint(ms.clkb_part, DIM), run_time=1.2)
            c.wait_until("The master is shut")
            tm2, ts2 = T("hold", 32, RED).move_to(_p(MX, TOP_Y)), T("transparent", 32, GREEN).move_to(_p(SX, TOP_Y))
            self.play(*dim_latch(ms.master, 0.35), *open_latch(ms.slave), *during(disappear(self.tag_m, self.tag_s), 0.0, 0.4),
                      *during(appear(tm2, ts2, shift=None, lag=0), 0.55, 1.0), run_time=1.5)
            self.play(passing(ms.q_wire, GREEN, 10, 0.6), run_time=1.0)
            # {airlock}: the tags become doors; they swap once as CLK toggles
            c.wait_until("airlock")
            self.door_m, self.door_s = door_icon(False).move_to(_p(MX, TOP_Y)), door_icon(True).move_to(_p(SX, TOP_Y))
            self.play(*swap(tm2, self.door_m), *swap(ts2, self.door_s), run_time=1.2)
            c.wait_until("two doors")
            dm2, ds2 = door_icon(True).move_to(_p(MX, TOP_Y)), door_icon(False).move_to(_p(SX, TOP_Y))
            self.play(*paint(ms.clk_part, DIM), *paint(ms.clkb_part, YELLOW), *swap(self.door_m, dm2),
                      *swap(self.door_s, ds2), *open_latch(ms.master), *dim_latch(ms.slave, 0.35),
                      run_time=1.2)
            self.door_m, self.door_s = dm2, ds2
            self.cap = T("never both open", 34).move_to(_p(0, TOP_Y))
            c.wait_until("never both open")
            self.play(*appear(self.cap), run_time=1.0)
            # {race}: a ghost of both doors open; a change rushes straight through
            c.wait_until("race")
            self.ghost = [door_icon(True, color=DIM).move_to(_p(x, TOP_Y)) for x in (MX, SX)]
            self.play(*swap(self.door_m, self.ghost[0]), *swap(self.door_s, self.ghost[1]),
                      *open_latch(ms.slave), run_time=1.2)
            self.dot = Dot(_p(X_IN, PIN_Y), radius=0.12, color=BLUE).set_z_index(5)
            c.wait_until("rush straight through")
            self.play(FadeIn(self.dot, scale=0.5), run_time=0.3)
            self.play(MoveAlongPath(self.dot, dot_path()), FlashAround(ms.lab_q, color=RED, time_width=1.5),
                      run_time=1.6, rate_func=rush_into)
            c.wait_until("just as it did")
            self.crosses = [cross_mark().scale(1.6).move_to(g.get_center()) for g in self.ghost]
            self.play(*appear(*self.crosses, shift=None, lag=0.2), run_time=1.0)

    # -- c2.pair.4: through both doors, then the timing diagram ---------------------------------
    def clip4(self):
        ms = self.ms
        with self.say("c2.pair.4") as c:
            # {path}: the real state returns (CLK low: master open, slave shut)
            dm, ds = door_icon(True).move_to(_p(MX, TOP_Y)), door_icon(False).move_to(_p(SX, TOP_Y))
            self.play(*disappear(*self.crosses, self.dot), *during(swap(self.ghost[0], dm), 0.2, 1.0),
                      *during(swap(self.ghost[1], ds), 0.2, 1.0), *dim_latch(ms.slave, 0.35), run_time=1.0)
            dot = Dot(_p(X_IN, PIN_Y), radius=0.12, color=BLUE).set_z_index(5)
            self.play(FadeIn(dot, scale=0.5), run_time=0.3)
            self.play(MoveAlongPath(dot, dot_path(stop_at_slave=True)), run_time=1.8, rate_func=smooth)
            self.play(FlashAround(ds, color=RED, time_width=1.5, buff=0.1), run_time=min(1.0, c.until("ask")))
            c.wait_until("ask")
            q = T("?", 80, YELLOW).move_to(_p(0, 1.95))
            self.play(*appear(q), run_time=1.0)
            # {trace}: everything but the circuit clears, labels included (all full-size text goes
            # first); the bare circuit shrinks; then the end shot's labels fade in at their new size.
            c.wait_until("trace")
            labels = [ms.lab_master, ms.lab_slave, ms.lab_d, ms.lab_q, ms.lab_qint, ms.lab_clk,
                      ms.lab_clkb, ms.lab_clk2]
            inner = [m for lb in (ms.master, ms.slave) for m in (lb.lab_d, lb.lab_q, lb.lab_en)]
            self.play(*disappear(dm, ds, self.cap, q, dot, self.notnot, *inner, *labels),
                      *paint(ms.clk_part + ms.clkb_part, YELLOW),
                      ms.master.box.animate.set_stroke(FG, 4, opacity=1),
                      ms.slave.box.animate.set_stroke(FG, 4, opacity=1), run_time=0.9)
            for lb in (ms.master, ms.slave):
                self.remove(lb.lab_d, lb.lab_q, lb.lab_en)
                lb.remove(lb.lab_d, lb.lab_q, lb.lab_en)
            self.remove(*labels)
            ms.remove(*labels)
            settle(self, ms)
            end = master_slave_end_shot()          # the exact end geometry (s4-s6 copy it)
            ms.generate_target()
            ms.target.scale(END_SCALE)
            ms.target.shift(end.master.box.get_center() - ms.target.master.box.get_center())
            end_strokes(ms.target)
            self.play(MoveToTarget(ms), run_time=1.5)
            end_labels = [end.lab_master, end.lab_slave, end.lab_d, end.lab_qint, end.lab_q,
                          end.lab_clk, end.lab_clkb, end.lab_clk2]
            self.play(*appear(*end_labels, shift=None, lag=0.08), run_time=min(1.0, c.until(floor=0.5)))
