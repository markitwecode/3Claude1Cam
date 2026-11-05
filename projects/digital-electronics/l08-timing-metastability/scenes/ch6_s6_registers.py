"""Chapter 6, scene 6: registers between the stages. Clips c6.reg.1 – c6.reg.4.

Shots: {path} ch1's path at scale K = 0.75 (FF0 x -5, one wide BLUE "combinational logic" block
x -3.8..3.8, FF1 x 5, CLK bus beneath) -> {register} two DIM ghost boxes behind each flip-flop,
"register" labels -> {cut} the block splits into "stage 1 logic" / "stage 2 logic", the middle
register drops into the gap -> {shorter} YELLOW T_c arrow, whole path -> one stage.
c6.reg.2: the middle register lifts out (DIM dashed outline); tokens are 4 horizontal "lanes" per
block whose fronts crawl at different speeds (slow paths lag); GREEN overtakes BLUE in stage 2;
FF1's D wire turns RED with "???".  c6.reg.3: register back; squares inside each register show
the token it holds (1 BLUE, 2 GREEN, 3 TEAL, 4 FG); two clock edges; the slides' sentence.
c6.reg.4: circuit rises; stage boxes; budget bars per stage; bars stack; one YELLOW T_c brace
snaps to the longer bar; "the slowest stage decides".  Ends on the closing picture (see the
pipe_diagram / stage_bars rulers for geometry), held, then faded.
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


# =============================================================================================
# L6's make_ff (D flip-flop), copied from ch1_s4_path.py
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D"):
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
    d_l = T(d_text, 36, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g
# =============================================================================================


# =============================================================================================
# THE pipelined path (ch6 s6; ch7's hook reopens it). Built at scale K of ch1's path:
#   registers (make_ff, box BG-filled) at x -5 / 0 / 5, y FY (0.3 in c6.reg.1–3, 1.8 in c6.reg.4);
#   box 1.125 x 1.95; pin row FY + 0.45; each register has 2 DIM ghost boxes behind it (+0.1, +0.2);
#   "register" labels T 30 FG at y FY + 1.5; logic blocks BLUE stroke 4, BG fill, height 1.3 on
#   the pin row: stage 1 x -3.8..-1.2, stage 2 x 1.2..3.8 (unpipelined: one block -3.8..3.8);
#   their labels T 30 BLUE on the label row; Q_0 GREEN / D_1 BLUE MathTex 36 over the wires;
#   CLK bus YELLOW y FY - 1.725 from x -5.6 to 5, junction dots at -5 and 0, "CLK" T 32 left.
# =============================================================================================
K = 0.75
RX = (-5.0, 0.0, 5.0)
FY0 = 0.3
HX = (BOX_W / 2 + WIRE) * K          # 1.2: box centre to a pin wire's end
BLK_H = 1.3
LAB_DY = 1.5
BUS_DY = -(BOX_H / 2 + EN_WIRE) * K  # -1.725
BUS_X0 = -5.6


def make_reg(x, fy):
    f = make_ff()
    f.scale(K, about_point=ORIGIN)
    for lb in (f.d_l, f.q_l, f.qb_l):
        lb.scale(1.2, about_point=lb.get_center())
    f.shift(_p(x, fy))
    f.box.set_fill(BG, 1)
    br = f.clk_w
    f.remove(br)
    gh = []
    for k in (2, 1):
        r = Rectangle(width=BOX_W * K, height=BOX_H * K).set_stroke(DIM, 3).set_fill(BG, 1)
        r.move_to(f.box.get_center() + 0.1 * k * (UP + RIGHT)).set_z_index(-1 - k)
        gh.append(r)
    return f, br, gh


def pipe_diagram(fy=FY0):
    """Parts: .ffs [FF0, mid, FF1] (make_ff, no clock wire) .brs (clock branches) .ghs (pairs of
    ghost boxes) .reg_ls ("register") .wide .wide_l (one block, "combinational logic") .b1 .b2
    .b1_l .b2_l (stage blocks) .q0_l .d1_l .bus .dots [at FF0, at mid] .clk_l .outline (DIM dashed,
    the lifted-out mid register) .bridge (DIM wire across the gap). .pin .fy .lane_map.
    .clk_paths(regs) -> fresh YELLOW paths bus start -> each register's triangle, current positions."""
    D = VGroup()
    D.fy, D.pin = fy, fy + PIN_Y * K
    D.ffs, D.brs, D.ghs = [], [], []
    for x in RX:
        f, br, gh = make_reg(x, fy)
        D.ffs.append(f)
        D.brs.append(br)
        D.ghs.append(gh)
    lab_y = fy + LAB_DY
    D.reg_ls = [T("register", 30, FG).move_to(_p(x, lab_y)) for x in RX]
    a, b = RX[0] + HX, RX[2] - HX              # -3.8, 3.8
    m0, m1 = RX[1] - HX, RX[1] + HX            # -1.2, 1.2

    def block(x0, x1):
        return Rectangle(width=x1 - x0, height=BLK_H).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(
            _p((x0 + x1) / 2, D.pin))
    D.wide = block(a, b)
    D.wide_l = T("combinational logic", 30, BLUE).move_to(_p(0, lab_y))
    D.b1, D.b2 = block(a, m0), block(m1, b)
    D.b1_l = T("stage 1 logic", 30, BLUE).move_to(_p((a + m0) / 2, lab_y))
    D.b2_l = T("stage 2 logic", 30, BLUE).move_to(_p((m1 + b) / 2, lab_y))
    D.q0_l = set_backstroke(MathTex("Q_0", font_size=36, color=GREEN).next_to(_p(a - 0.3, D.pin), UP, buff=0.12))
    D.d1_l = MathTex("D_1", font_size=36, color=BLUE).next_to(_p(b + 0.3, D.pin), UP, buff=0.12)
    by = fy + BUS_DY
    D.bus = Line(_p(BUS_X0, by), _p(RX[2], by)).set_stroke(YELLOW, 5)
    D.dots = [Dot(_p(x, by), radius=0.08, color=YELLOW) for x in RX[:2]]
    D.clk_l = T("CLK", 32, YELLOW).next_to(_p(BUS_X0, by), LEFT, buff=0.15)
    D.outline = DashedVMobject(Rectangle(width=BOX_W * K, height=BOX_H * K), num_dashes=28).set_stroke(DIM, 3)
    D.outline.move_to(_p(RX[1], fy))
    D.bridge = Line(_p(m0, D.pin), _p(m1, D.pin)).set_stroke(DIM, 5)
    # lane geometry: distance along the logic -> x (block 1, a short hop across the gap, block 2)
    D.W, D.H = (m0 - a) - 0.2, 0.5
    D.lane_map = [(0.0, D.W, a + 0.1), (D.W + D.H, 2 * D.W + D.H, m1 + 0.1)]
    D.gap = (m0, m1)

    def clk_paths(idx=(0, 1, 2), width=10):
        s = D.bus.get_start()
        out = []
        for i in idx:
            br = D.brs[i]
            p0, p1 = br.get_start(), br.get_end()
            out.append(VMobject().set_points_as_corners([s, p0, p1]).set_stroke(YELLOW, width))
        return out
    D.clk_paths = clk_paths
    return D


def mid_parts(D):
    return [D.ffs[1], *D.ghs[1], D.brs[1], D.dots[1], D.reg_ls[1]]


def pipelined_parts(D):
    """The closing circuit (ch7's hook): everything of the pipelined path that stays on screen."""
    out = []
    for i in range(3):
        out += [D.ffs[i], *D.ghs[i], D.brs[i], D.reg_ls[i]]
    return out + [D.b1, D.b2, D.b1_l, D.b2_l, D.q0_l, D.d1_l, D.bus, *D.dots, D.clk_l]
# =============================================================================================


# =============================================================================================
# The two stage budgets (ch1_s6 budget_bar, copied verbatim) and their closing layout.
#   unit lengths: t_pc 0.7 PINK, t_pd 2.2 (stage 1) / 3.1 (stage 2) PURPLE, t_su 0.6 GOLD.
#   Side by side (c6.reg.4 {rule}): bar 1 x0 -4.4, bar 2 x0 0.9, y -0.9; formula MathTex 40 at y -2.0.
#   Stacked (closing): both x0 -4.4; bar 1 y -0.9, bar 2 y -2.2; "stage 1/2" T 30 FG left;
#   YELLOW brace under bar 2 spanning -4.4..0.0 with T_c (44); dashed YELLOW guide at x 0.0
#   (y -2.5..-0.5); bar 1's outline stretched to 4.4; tag "the slowest / stage decides"
#   T 36 YELLOW centred (3.3, -1.55).
# =============================================================================================
BAR_H = 0.5          # segment / outline height
BAR_FILL = 0.85      # segment fill opacity (no stroke)
BAR_OUT_W = 3        # YELLOW outline stroke


def budget_bar(segs, total, x0=-3.3, y=0.0, tc_tex="T_c", syms=True, nums=None,
               sym_size=40, num_size=34):
    g = VGroup()
    g.segs, g.syms, g.nums = [], [], []
    x = x0
    for tex, col, w in segs:
        r = Rectangle(width=w, height=BAR_H).set_stroke(width=0).set_fill(col, BAR_FILL)
        r.move_to([x + w / 2, y, 0])
        g.segs.append(r)
        x += w
    g.outline = Rectangle(width=total, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
    g.outline.move_to([x0 + total / 2, y, 0]).set_z_index(1)
    if syms:
        for (tex, col, _), r in zip(segs, g.segs):
            g.syms.append(MathTex(tex, font_size=sym_size, color=col).next_to(r, UP, buff=0.15))
    g.tc = MathTex(tc_tex, font_size=44, color=YELLOW).next_to(g.outline, LEFT, buff=0.25)
    for txt, r in zip(nums or [], g.segs):
        if txt is not None:
            g.nums.append(T(txt, num_size, GOLD).next_to(r, DOWN, buff=0.2))
    g.add(*g.segs, g.outline, *g.syms, g.tc, *g.nums)
    return g


T_PC, T_SU = 0.7, 0.6
T_PD = (2.2, 3.1)
BAR_X0 = (-4.4, 0.9)
BAR_Y = -0.9
STACK_Y2 = -2.2
LONG = T_PC + T_PD[1] + T_SU          # 4.4


def stage_bar(i, x0=None, y=BAR_Y):
    segs = [("t_{pc}", PINK, T_PC), ("t_{pd}", PURPLE, T_PD[i]), ("t_{su}", GOLD, T_SU)]
    return budget_bar(segs, T_PC + T_PD[i] + T_SU, x0=BAR_X0[i] if x0 is None else x0, y=y,
                      sym_size=36)


def stage_rule(bar):
    f = MathTex("T_c", r"\ge", "t_{pc}", "+", "t_{pd}", "+", "t_{su}", font_size=40)
    for k, col in zip((0, 1, 2, 3, 4, 5, 6), (YELLOW, FG, PINK, FG, PURPLE, FG, GOLD)):
        f[k].set_color(col)
    return f.move_to(_p(bar.outline.get_x(), -2.0))


def t_brace(x1, y=STACK_Y2):
    br = span_brace(_p(BAR_X0[0], y - BAR_H / 2), _p(x1, y - BAR_H / 2), DOWN, YELLOW, buff=0.12)
    return br


def t_guide(x):
    return DashedLine(_p(x, STACK_Y2 - 0.3), _p(x, BAR_Y + 0.4), dash_length=0.1).set_stroke(YELLOW, 2)


def closing_tag():
    return VGroup(T("the slowest", 36, YELLOW), T("stage decides", 36, YELLOW)).arrange(
        DOWN, buff=0.14).move_to(_p(3.3, -1.55))
# =============================================================================================


# ---- tokens as wavefronts: 4 lanes per block, each front at its own speed -------------------
TOK = [BLUE, GREEN, TEAL, FG]
LANE_DY = (0.42, 0.14, -0.14, -0.42)
LANE_V = (0.55, 0.3, 0.17, 0.1)
LANE_SW = 9


class Token:
    """A token's signals in the logic: lane i's front sits at distance starts[i] + speed*v_i*age
    (capped), painted from `lo`. Lanes are always_redraw; fade with .op, advance with .age."""
    _z = 3

    def __init__(self, D, color, starts, speed=1.0, lo=0.0, cap=None, bridge=False, op=1.0):
        self.D, self.color, self.starts, self.speed = D, color, starts, speed
        self.lo = lo
        self.cap = cap if cap is not None else 2 * D.W + D.H
        self.bridge = bridge
        self.age = ValueTracker(0.0)
        self.op = ValueTracker(op)
        Token._z += 1
        self.z = Token._z
        self.lanes = [always_redraw(lambda i=i: self._draw(i)) for i in range(4)]

    def front(self, i):
        return min(self.cap, self.starts[i] + self.speed * LANE_V[i] * self.age.get_value())

    def _draw(self, i):
        D = self.D
        d = self.front(i)
        y = D.pin + LANE_DY[i]
        op = self.op.get_value()
        g = VGroup(VectorizedPoint(_p(D.gap[0], D.pin)))
        for da, db, xa in D.lane_map:
            lo, hi = max(self.lo, da), min(d, db)
            if hi > lo + 1e-3:
                g.add(Line(_p(xa + lo - da, y), _p(xa + hi - da, y)).set_stroke(self.color, LANE_SW, op))
        if self.bridge and i == 0 and d > D.W:
            f = min(1.0, (d - D.W) / D.H)
            x0, x1 = D.gap
            g.add(Line(_p(x0, D.pin), _p(x0 + f * (x1 - x0), D.pin)).set_stroke(self.color, 5, op))
        return g.set_z_index(self.z)

    def run(self, dt):
        return self.age.animate(rate_func=linear).set_value(self.age.get_value() + dt)


def token_sq(color, reg):
    s = RoundedRectangle(width=0.38, height=0.38, corner_radius=0.08).set_stroke(width=0)
    s.set_fill(color, 0.85)
    return s.move_to(reg.box.get_center() + _p(-0.13, -0.2)).set_z_index(2)


def sq_to(sq, color):
    return sq.animate.set_fill(color, 0.85)


class Registers(NarratedScene):
    def construct(self):
        D = pipe_diagram()
        self.D = D
        self.toks = []
        self.clip1(D)
        self.clip2(D)
        self.clip3(D)
        self.clip4(D)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---------------------------------------------------------------------------------------
    def pulse(self, D, idx=(0, 1, 2)):
        return [VShowPassingFlash(p, time_width=0.5) for p in D.clk_paths(idx)]

    def add_tok(self, tok):
        self.toks.append(tok)
        self.add(*tok.lanes)
        return tok

    def drop_toks(self):
        for t in self.toks:
            self.remove(*t.lanes)
        self.toks = []

    # ---------------------------------------------------------------------------------------
    def clip1(self, D):
        f0, fm, f1 = D.ffs
        with self.say("c6.reg.1") as c:
            c.wait_until("path")
            self.play(*appear(f0, D.q0_l, lag=0.2), run_time=1.0)
            c.wait_until(own_word=D.wide_l)
            self.play(*appear(D.wide, D.wide_l, lag=0.3), run_time=1.2)
            c.wait_until("another flip-flop")
            self.play(*appear(f1, D.d1_l, lag=0.2), run_time=1.0)
            self.play(*appear(D.bus, D.dots[0], D.brs[0], D.brs[2], D.clk_l, shift=None, lag=0.1),
                      run_time=1.0)
            # {register}: two ghost copies behind each, "register"
            c.wait_until(own_word=D.reg_ls[0])
            self.play(*appear(*D.ghs[0], *D.ghs[2], shift=0.15 * DL, lag=0.15),
                      *appear(D.reg_ls[0], D.reg_ls[2]), run_time=1.4)
            c.wait_until("same clock")
            self.play(*self.pulse(D, (0, 2)), run_time=1.2)
            # {cut}: the block splits, the middle register drops into the gap
            c.wait_until("cut")
            self.play(ReplacementTransform(D.wide, D.b1), ReplacementTransform(D.wide.copy(), D.b2),  # early: stage names come with the split
                      *swap(D.wide_l, VGroup(D.b1_l, D.b2_l)),
                      run_time=min(1.4, c.until("another register")))
            c.wait_until("another register")
            self.play(*appear(fm, *D.ghs[1], D.brs[1], D.dots[1], shift=0.6 * DOWN, lag=0),
                      *appear(D.reg_ls[1]), run_time=min(1.4, c.until("shorter")))
            # {shorter}: T_c over the whole path, then over one stage
            c.wait_until("shorter")
            ty = D.fy + 2.1
            self.tc_arrow = DoubleArrow(_p(RX[0], ty), _p(RX[2], ty), buff=0, stroke_width=4,
                                        tip_length=0.2, color=YELLOW)
            self.tc_l = MathTex("T_c", font_size=44, color=YELLOW).next_to(self.tc_arrow, UP, buff=0.1)
            self.play(FadeIn(self.tc_arrow), *appear(self.tc_l),
                      run_time=min(1.0, c.until("which can")))
            c.wait_until("which can")
            short = DoubleArrow(_p(RX[0], ty), _p(RX[1], ty), buff=0, stroke_width=4,
                                tip_length=0.2, color=YELLOW)
            self.play(Transform(self.tc_arrow, short),
                      self.tc_l.animate.next_to(short, UP, buff=0.1), run_time=min(1.5, c.until()))

    # ---------------------------------------------------------------------------------------
    def clip2(self, D):
        f0, fm, f1 = D.ffs
        W, H = D.W, D.H
        with self.say("c6.reg.2") as c:
            self.play(FlashAround(fm.box, run_time=1.6, time_width=1.5))
            self.play(*disappear(self.tc_arrow, self.tc_l), run_time=0.8)
            c.wait_until("without")
            # {without}: the middle register lifts out, leaving a dashed outline
            self.play(*[FadeOut(m, shift=0.9 * UP) for m in mid_parts(D)],
                      *during([FadeIn(D.outline), FadeIn(D.bridge)], 0.4, 1), run_time=1.5)
            # token 1 still crawling through stage 2 logic
            blue = self.add_tok(Token(D, BLUE, [W + H + p for p in (W, 1.6, 0.9, 0.3)],
                                      bridge=True, op=0.0))
            self.sq0 = token_sq(BLUE, f0)
            dt = 1.0
            self.play(blue.op.animate.set_value(1.0), FadeIn(self.sq0), blue.run(dt), run_time=dt)
            dt = c.until("ripple", floor=0.1)
            self.play(blue.run(dt), run_time=dt)
            # {ripple}: the input register lets token 2 in; it ripples straight on
            green = self.add_tok(Token(D, GREEN, [0, 0, 0, 0], bridge=True))
            dt = c.until("corrupt")
            self.play(sq_to(self.sq0, GREEN), blue.run(dt), green.run(dt), run_time=dt)
            # {corrupt}: the output is a mix
            self.qq = T("???", 30, RED).move_to(f1.d_w.get_center() + 0.3 * UP + 0.05 * RIGHT).align_to(D.d1_l, DOWN)
            self.play(f1.d_w.animate.set_stroke(RED), *swap(D.d1_l, self.qq), run_time=1.2)

    # ---------------------------------------------------------------------------------------
    def clip3(self, D):
        f0, fm, f1 = D.ffs
        W, H = D.W, D.H
        with self.say("c6.reg.3") as c:
            # {with}: the register drops back in
            d1 = MathTex("D_1", font_size=36, color=BLUE).move_to(D.d1_l)
            D.d1_l = d1
            outs = [t.op.animate.set_value(0.0) for t in self.toks]
            self.play(*during(outs + [FadeOut(self.sq0), FadeOut(D.outline), FadeOut(D.bridge)], 0, 0.45),
                      *during([FadeIn(m, shift=0.9 * DOWN) for m in mid_parts(D)], 0.35, 1),
                      *during(swap(self.qq, d1) + [f1.d_w.animate.set_stroke(BLUE)], 0.35, 1),
                      run_time=min(1.8, c.until("hold")))
            self.drop_toks()
            c.wait_until("hold")
            # {hold}: GREEN stops at the register's input; its output stays BLUE
            self.sqm = token_sq(BLUE, fm)
            self.sq0 = token_sq(GREEN, f0)
            b2 = self.add_tok(Token(D, BLUE, [W + H] * 4, speed=4, lo=W + H))
            g1 = self.add_tok(Token(D, GREEN, [0] * 4, speed=4, cap=W))
            self.play(*appear(self.sqm, self.sq0, shift=None, lag=0.3), b2.run(1.2), g1.run(1.2),
                      run_time=1.2)
            dt = c.until("edge", floor=0.1)
            self.play(b2.run(dt), g1.run(dt), run_time=dt)
            # {edge}: all three registers clock at once; repeat once
            self.sq1 = token_sq(BLUE, f1)
            cols = [(BLUE, GREEN, TEAL), (GREEN, TEAL, FG)]
            for k, (c1, cm, c0) in enumerate(cols):
                anims = self.pulse(D) + [sq_to(self.sqm, cm), sq_to(self.sq0, c0)]
                anims.append(FadeIn(self.sq1) if k == 0 else sq_to(self.sq1, c1))
                self.play(*anims, run_time=1.0)
                s2 = self.add_tok(Token(D, cm, [W + H] * 4, speed=12, lo=W + H))
                s1 = self.add_tok(Token(D, c0, [0] * 4, speed=12, cap=W))
                dt = 2.0 if k == 0 else min(2.0, c.until("stop"))
                self.play(s2.run(dt), s1.run(dt), run_time=dt)
            # {stop}: the slides' sentence
            self.sent = VGroup(
                T("Registers stop a token in one pipeline stage catching up with", 30, FG),
                T("and corrupting the token in the next stage.", 30, FG)).arrange(DOWN, buff=0.16)
            self.sent.move_to(_p(0, -2.75))
            c.wait_until(own_word=self.sent[0])
            self.play(*appear(self.sent, shift=None), run_time=1.2)

    # ---------------------------------------------------------------------------------------
    def clip4(self, D):
        circuit = pipelined_parts(D)
        with self.say("c6.reg.4") as c:
            # {stage}: clear the tokens, the circuit rises; each stage boxed in turn
            outs = [t.op.animate.set_value(0.0) for t in self.toks]
            self.play(*outs, *disappear(self.sqm, self.sq0, self.sq1), run_time=0.7)
            self.drop_toks()
            rise = 1.5 * UP
            self.play(*[m.animate.shift(rise) for m in circuit], run_time=1.3)
            D.fy += 1.5
            D.pin += 1.5

            def stage_box(i):
                x0 = RX[i] - BOX_W * K / 2 - 0.25
                x1 = RX[i + 1] + BOX_W * K / 2 + 0.35
                y0 = D.fy - BOX_H * K / 2 - 0.2
                y1 = D.fy + BOX_H * K / 2 + 0.35
                return Rectangle(width=x1 - x0, height=y1 - y0).set_stroke(YELLOW, 3).set_fill(
                    YELLOW, 0.06).move_to(_p((x0 + x1) / 2, (y0 + y1) / 2)).set_z_index(-4)
            box = stage_box(0)
            c.wait_until("path again")
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("register")
            self.play(Transform(box, stage_box(1)), run_time=min(1.5, c.until("rule")))
            # {rule}: a budget bar under each stage
            c.wait_until("rule")
            bars = [stage_bar(0), stage_bar(1)]
            self.play(*disappear(self.sent, box), run_time=0.8)
            c.wait_until("clock period")
            self.play(*[FadeIn(b.outline) for b in bars], *appear(*[b.tc for b in bars], shift=None),
                      run_time=1.0)
            rules = [stage_rule(b) for b in bars]
            for j, cue in enumerate(("clock-to-output", "delay in that", "set-up time")):
                c.wait_until(cue)
                extra = appear(*rules, shift=None, lag=0.2) if j == 1 else []
                self.play(*[FadeIn(b.segs[j]) for b in bars],
                          *appear(*[b.syms[j] for b in bars], lag=0), *extra, run_time=1.0)
            # {pay}: every stage pays its own t_pc and t_su
            c.wait_until("pay")
            self.play(*[FlashAround(b.segs[j], run_time=2.0, time_width=1.5, color=YELLOW)
                        for b in bars for j in (0, 2)])
            # {slowest}: one clock for every stage
            c.wait_until("slowest")
            self.play(*self.pulse(D), *disappear(*[b.tc for b in bars]), run_time=1.0)
            b1, b2 = bars
            b2.remove(b2.tc)
            b1.remove(b1.tc)
            self.play(*during(disappear(*rules), 0, 0.35),
                      *during([b2.animate.shift((STACK_Y2 - BAR_Y) * UP)], 0.35, 1), run_time=1.2)
            self.play(b2.animate.shift((BAR_X0[0] - BAR_X0[1]) * RIGHT), run_time=1.1)
            # one T_c for both: start at the shorter bar
            x_short = BAR_X0[0] + T_PC + T_PD[0] + T_SU
            brace = t_brace(x_short)
            tcl = MathTex("T_c", font_size=44, color=YELLOW).next_to(brace, DOWN, buff=0.1)
            guide = t_guide(x_short)
            st_ls = [T(f"stage {i + 1}", 30, FG).next_to(b.outline, LEFT, buff=0.3)
                     for i, b in enumerate(bars)]
            c.wait_until("which stage")
            self.play(GrowFromCenter(brace), *appear(tcl, *st_ls, lag=0.1), FadeIn(guide), run_time=1.2)
            # {decides}: it snaps to the longer one
            c.wait_until("decides")
            x_long = BAR_X0[0] + LONG
            long_out = Rectangle(width=LONG, height=BAR_H).set_stroke(YELLOW, BAR_OUT_W).set_fill(opacity=0)
            long_out.move_to(_p(BAR_X0[0] + LONG / 2, BAR_Y)).set_z_index(1)
            nb = t_brace(x_long)
            guide2 = t_guide(x_long)
            self.play(Transform(brace, nb), tcl.animate.next_to(nb, DOWN, buff=0.1),
                      *during([FadeOut(guide)], 0, 0.3), *during([FadeIn(guide2)], 0.75, 1),
                      Transform(b1.outline, long_out), run_time=1.2)
            tag = closing_tag()
            self.play(*appear(tag), run_time=1.0)
            c.wait_until()
            self.wait(1.8)
