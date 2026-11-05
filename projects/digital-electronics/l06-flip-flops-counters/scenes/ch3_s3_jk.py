"""Chapter 3, scene 3: the J-K flip-flop, its table built row by row, beside the RS table; toggle. Clips c3.jk.1 – c3.jk.5."""
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
# Shared with ch3_s4 / ch3_s5: jk_symbol(), place_symbol(), jk_table(), rs_table()
# =============================================================================================
# ---- ch2_s7_recap's make_ff geometry --------------------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
LOW_OP = 0.18    # a wire at 0 keeps its role colour at this opacity; at 1 it is full (ch2_s6)


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),)):
    """ch2_s7's make_ff box, pins and triangle; `ins` = (label, y) BLUE inputs on the left."""
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w = box, tri, clk_w
    g.in_w, g.q_w, g.qb_w = in_w, q_w, qb_w
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


# ---- ch2_s6's switch and LED ----------------------------------------------------------------
def toggle(v, color=BLUE):
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(color, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    g.track, g.knob, g.v, g.sw_color = track, knob, v, color

    def knob_pos(val):
        return g.track.get_center() + (0.2 if val else -0.2) * RIGHT * (g.track.width / 0.78)
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


def lev(m, v):
    """A wire to logic level v: full role colour at 1, faint at 0."""
    return m.animate.set_stroke(opacity=1.0 if v else LOW_OP)


def jk_symbol(j=0, k=0, q=1):
    """The J-K flip-flop: ch2_s7's make_ff(ins=(J, K)) with a BLUE toggle switch on J and K, a
    YELLOW push-button under the clock wire, and GREEN LEDs on Q and Q-bar. Built at scale 1 with
    the box centred on ORIGIN (4.41 wide x 3.94 tall incl. switches, LEDs and button); place it
    with place_symbol(). Wires at 0 are faint (LOW_OP), at 1 full.
    .ff (.box .tri .labels) .sw_j .sw_k .led_q .led_qb .btn (.ring .cap)
    .w = {"j", "k", "q", "qb", "clk"} wires; .s = current scale."""
    ff = make_ff(ins=(("J", PIN_Y), ("K", -PIN_Y)))
    hb = BOX_H / 2
    x_in, x_out = -BOX_W / 2 - WIRE, BOX_W / 2 + WIRE
    sw_j = toggle(j, BLUE).move_to(_p(x_in - 0.39, PIN_Y)).set_z_index(2)
    sw_k = toggle(k, BLUE).move_to(_p(x_in - 0.39, -PIN_Y)).set_z_index(2)
    led_q = led(bool(q)).move_to(_p(x_out + 0.21, PIN_Y))
    led_qb = led(not q).move_to(_p(x_out + 0.21, -PIN_Y))
    ring = Circle(radius=0.22).set_stroke(YELLOW, 3).set_fill(BG, 1)
    cap = Circle(radius=0.12).set_stroke(width=0).set_fill(YELLOW, 0.25)
    btn = VGroup(ring, cap).move_to(_p(0, -hb - EN_WIRE - 0.22))
    btn.ring, btn.cap = ring, cap
    g = VGroup(ff, sw_j, sw_k, btn, led_q, led_qb)
    g.ff, g.sw_j, g.sw_k, g.btn, g.led_q, g.led_qb = ff, sw_j, sw_k, btn, led_q, led_qb
    g.w = {"j": ff.in_w[0], "k": ff.in_w[1], "q": ff.q_w, "qb": ff.qb_w, "clk": ff.clk_w}
    for key, v in (("j", j), ("k", k), ("q", q), ("qb", 1 - q), ("clk", 0)):
        g.w[key].set_stroke(opacity=1.0 if v else LOW_OP)
    g.s = 1.0
    g.lab_h = [lab.height for lab in ff.labels]
    return g


def place_symbol(g, box_center, scale, target=None):
    """Scale the symbol (or its .target) to `scale` and put its box centre at `box_center`."""
    m = g if target is None else target
    c = g.ff.box.get_center()
    m.scale(scale / g.s, about_point=c).shift(np.array(box_center) - c)
    g.s = scale
    labs = m[0].labels if hasattr(m[0], "labels") else [m[0][i] for i in range(-4, 0)]
    for lab, h0 in zip(labs, g.lab_h):     # labels never below size 30
        lab.scale_to_fit_height(h0 * max(scale, 30 / 36))
    return m


# Positions used here (box centre, scale):
SYM_A = (_p(3.6, 0.6), 1.25)     # clips 1-3: big on the right
SYM_B = (_p(4.7, 2.75), 0.7)    # clips 4-5: small, top right, above the J-K table


def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """ch1_s2's grid_table: rows of strings ('$...' -> MathTex, else T); header row at y = 0,
    column centres xs (or ('L', x) for left-aligned). VGroup(*rows, lines), .rows, .lines."""
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


TAB_XS = [0, 0.75, 1.9, 2.8, ("L", 3.75)]     # ch1_s2's RS table columns
TAB_SEPS = [1.32, 3.4]
TAB_PITCH = 0.66


def jk_table():
    """The J-K table (p. 90) in ch1's RS-table styling: header `J K | Q' Q-bar' | comment`, rows
    hold / reset / set / toggle. Header row centred at y = 0, J column at x = 0 (shift by the
    J-column centre and header y you want). J, K BLUE; Q, Q-bar, Q', Q-bar' GREEN; "toggle" YELLOW.
    .rows[0] header, .rows[1..4] rows (cells: J, K, Q', Q-bar', comment), .lines."""
    rows = [["$J", "$K", "$Q'", r"$\overline{Q}\,'", "comment"],
            ["$0", "$0", "$Q", r"$\overline{Q}", "hold"],
            ["$0", "$1", "$0", "$1", "reset"],
            ["$1", "$0", "$1", "$0", "set"],
            ["$1", "$1", r"$\overline{Q}", "$Q", "toggle"]]
    tab = grid_table(rows, TAB_XS, size=44, pitch=TAB_PITCH, seps=TAB_SEPS)
    r = tab.rows
    for m in r[0][0:2]:
        m.set_color(BLUE)
    for i in (0, 1, 4):
        for m in r[i][2:4]:
            m.set_color(GREEN)
    r[4][4].set_color(YELLOW)
    return tab


def rs_table():
    """ch1_s2's RS latch table (p. 79), same styling, all FG (row 4 turns RED in this scene)."""
    rows = [["$S", "$R", "$Q'", r"$\overline{Q}\,'", "comment"],
            ["$0", "$0", "$Q", r"$\overline{Q}", "hold"],
            ["$0", "$1", "$0", "$1", "reset"],
            ["$1", "$0", "$1", "$0", "set"],
            ["$1", "$1", "$0", "$0", "illegal"]]
    return grid_table(rows, TAB_XS, size=44, pitch=TAB_PITCH, seps=TAB_SEPS)


# Table positions used here (J/S column centre x, header y):
JK_A = _p(-5.9, 2.3)     # clips 2-3: J-K table on the left
JK_B = _p(0.9, 0.25)     # clips 4-5: J-K table on the right
RS_B = _p(-6.1, 0.25)    # clips 4-5: RS table on the left, rows level with the J-K rows


# =============================================================================================
# Scene-only helpers
# =============================================================================================
def edge_arrow(sym):
    """YELLOW up-arrow beside (left of) the clock wire: a rising edge."""
    s, clk = sym.s, sym.w["clk"]
    x = clk.get_center()[0] - 0.4 * s
    return Arrow(_p(x, clk.get_bottom()[1] + 0.05 * s), _p(x, clk.get_top()[1] - 0.05 * s), buff=0,
                 stroke_width=5, max_tip_length_to_length_ratio=0.35, color=YELLOW)


def glide(src, dst, via):
    """A copy of src travels src -> via... -> dst along straight legs (no arcs), faint until it has
    left src; returns (copy, animation). After the play: remove the copy, add dst (same glyphs)."""
    cp = src.copy()
    path = VMobject().set_points_as_corners([src.get_center(), *via, dst.get_center()])

    c0, w, h = src.get_center(), src.width, src.height

    def f(m, a):
        m.move_to(path.point_from_proportion(smooth(a)))
        d = m.get_center() - c0
        out = max(abs(d[0]) - w, abs(d[1]) - h)        # > 0 once the copy no longer touches src
        m.set_opacity(0.25 + 0.75 * float(np.clip(out / 0.15, 0, 1)))
    return cp, UpdateFromAlphaFunc(cp, f)


def blink_box(mobs, color, buff=0.1, fill=False):
    """A box round the whole cell(s) that fades in, holds, and fades out (no travelling flash).
    fill=True: a soft row highlight behind the cells instead of an outline. Returns (box, anim):
    play anim, then remove box."""
    box = SurroundingRectangle(VGroup(*[m.copy() for m in mobs]), color=color, buff=buff)
    full = 0.3 if fill else 1.0
    if fill:
        box.set_stroke(width=0).set_z_index(-1)
    else:
        box.set_stroke(color, 3)

    def f(m, a):
        op = full * there_and_back_with_pause(a, pause_ratio=0.4)
        if fill:
            m.set_fill(color, op)
        else:
            m.set_stroke(color, 3, opacity=op)
    f(box, 0)
    return box, UpdateFromAlphaFunc(box, f)


def pulse_clock(sym):
    """Button pressed and released, clock wire up and back down (one there-and-back)."""
    cap, clk = sym.btn.cap, sym.w["clk"]

    def f_cap(m, a):
        m.set_fill(YELLOW, 0.25 + 0.75 * there_and_back(a))

    def f_clk(m, a):
        m.set_stroke(opacity=LOW_OP + (1 - LOW_OP) * there_and_back(a))
    return [UpdateFromAlphaFunc(cap, f_cap), UpdateFromAlphaFunc(clk, f_clk)]


def set_q(sym, q):
    return [lev(sym.w["q"], q), lev(sym.w["qb"], 1 - q), set_led(sym.led_q, bool(q)),
            set_led(sym.led_qb, not q)]


class JKFlipFlop(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -------------------------------------------------------------- helpers
    def blink(self, mobs, color, rt, buff=0.1, fill=False, extra=()):
        box, anim = blink_box(mobs, color, buff=buff, fill=fill)
        self.play(anim, *extra, run_time=rt)
        self.remove(box)

    def edge(self, outs=(), rt=1.6):
        """A rising edge: the button pulses the clock, the up-arrow grows; outputs change after it."""
        up = edge_arrow(self.sym)
        self.play(*pulse_clock(self.sym), *during(GrowArrow(up), 0, 0.4),
                  *during(list(outs), 0.45, 0.85), run_time=rt)
        self.up = up

    def set_inputs(self, j=None, k=None, rt=0.9, extra=()):
        s = self.sym
        anims = []
        if j is not None and j != s.sw_j.v:
            anims += [flip(s.sw_j, j), lev(s.w["j"], j)]
        if k is not None and k != s.sw_k.v:
            anims += [flip(s.sw_k, k), lev(s.w["k"], k)]
        self.play(*anims, *extra, run_time=rt)

    # -------------------------------------------------------------- c3.jk.1
    def clip1(self):
        with self.say("c3.jk.1") as c:
            sym = jk_symbol(0, 0, 1)
            place_symbol(sym, *SYM_A)
            self.sym = sym
            self.play(*appear(sym, shift=None), run_time=1.5)
            line = T("The J-K FF is similar\nin function to a clocked\nRS FF, but with the illegal\n"
                     "state replaced with a new\n‘toggle’ state", 36, line_spacing=1.2,
                     t2c={"illegal": RED, "‘toggle’": YELLOW})
            line.move_to(_p(-3.45, 0.6))
            self.slide = line
            self.play(*appear(line, shift=None), run_time=1.2)  # early: the slide's line, read silently
            c.wait_until("triangle")
            tri = sym.ff.tri
            self.blink([tri], YELLOW, 1.5, buff=0.12, extra=[tri.animate.set_stroke(YELLOW, 4).set_fill(YELLOW, 0.35)])
            tag = T("edge-triggered", 32, YELLOW)
            tag.next_to(sym.w["clk"], RIGHT, buff=0.3).shift(0.1 * UP)
            self.tag = tag
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("wiggle")
            for j, k in ((1, None), (None, 1), (0, None), (None, 0), (1, 1), (0, 0)):
                self.set_inputs(j, k, rt=0.4)
                self.wait(0.12)
            c.wait_until("edge")
            self.edge(rt=1.4)
            self.blink([sym.led_q, sym.led_qb], GREEN, 1.4, buff=0.15)

    # -------------------------------------------------------------- c3.jk.2
    def clip2(self):
        with self.say("c3.jk.2") as c:
            tab = jk_table()
            tab.shift(JK_A)
            self.tab = tab
            self.row4 = tab.rows[4]
            tab.remove(self.row4)          # row 4 is built in clip 5, on its own
            hdr = tab.rows[0]
            self.play(*during(disappear(self.slide, self.up), 0, 0.45),
                      *during(appear(hdr, tab.lines, shift=None), 0.5, 1.0), run_time=1.6)  # early: table header
            foot = T("Where Q′ is the next state\nand Q is the current state", 32, line_spacing=1.15,
                     t2c={"Q": GREEN})
            foot.next_to(tab, DOWN, buff=1.1).set_x(tab.get_x())
            self.foot = foot
            c.wait_until("prime")
            self.play(*appear(foot), run_time=1.2)
            c.wait_until("hold")
            self.edge()
            r = tab.rows[1]
            self.play(*disappear(self.up), *appear(*r[:4], lag=0.25), run_time=1.4)
            c.wait_until(own_word=r[4])
            self.play(*appear(r[4]), run_time=1.0)

    # -------------------------------------------------------------- c3.jk.3
    def clip3(self):
        tab, sym = self.tab, self.sym
        with self.say("c3.jk.3") as c:
            self.set_inputs(0, 1, rt=0.9)
            self.wait(0.2)
            self.edge(set_q(sym, 0))
            r = tab.rows[2]
            self.play(*disappear(self.up), *appear(*r[:4], lag=0.25), run_time=1.3)
            c.wait_until(own_word=r[4])
            self.play(*appear(r[4]), run_time=1.0)
            c.wait_until("set")
            self.set_inputs(1, 0, rt=0.9)
            self.wait(0.2)
            self.edge(set_q(sym, 1))
            r = tab.rows[3]
            self.play(*disappear(self.up), *appear(*r[:4], lag=0.25), run_time=1.3)
            c.wait_until("set condition")
            self.play(*appear(r[4]), run_time=1.0)
            c.wait_until("familiar")
            qm = T("?", 80, YELLOW).move_to(_p((tab.rows[0].get_right()[0] + sym.get_left()[0]) / 2, tab.rows[2].get_y()))
            self.qm = qm
            self.play(*appear(qm), run_time=1.0)
        settle(self, tab)

    # -------------------------------------------------------------- c3.jk.4
    def clip4(self):
        tab, sym = self.tab, self.sym
        with self.say("c3.jk.4") as c:
            rs = rs_table().shift(RS_B)
            self.rs = rs
            rs_lab = T("RS latch", 36, DIM).move_to(_p(rs.get_x(), RS_B[1] + 0.85))
            self.rs_lab = rs_lab
            sym.generate_target()
            place_symbol(sym, *SYM_B, target=sym.target)
            delta = JK_B - JK_A
            self.row4.shift(delta)
            gap_x = (rs.rows[0].get_right()[0] + JK_B[0] - 0.15) / 2
            # the "?" leaves before the table moves and comes back in the gap where the "=" signs go
            qm2 = self.qm.copy().scale(0.75).move_to(_p(gap_x, tab.rows[2].get_y() + delta[1]))
            self.play(*during(disappear(self.foot, self.tag, self.qm), 0, 0.3),  # early: the RS table is recalled whole
                      *during(MoveToTarget(sym), 0.05, 0.4),
                      # the table drops first, then slides right under the shrunk symbol, so it never
                      # passes over the symbol; the RS table comes in only once it has arrived
                      *during(MoveAlongPath(tab, VMobject().set_points_as_corners(
                          [tab.get_center(), tab.get_center() + delta[1] * UP, tab.get_center() + delta])),
                          0.3, 0.78),
                      *during(appear(rs, rs_lab, shift=0.8 * RIGHT, lag=0.2), 0.78, 1.0),
                      *during(appear(qm2, shift=None), 0.88, 1.0),
                      run_time=min(3.4, c.until("same") - 0.3))
            c.wait_until("same")
            eqs = [MathTex("=", font_size=56, color=GREEN).move_to(_p(gap_x, tab.rows[i].get_y()))
                   for i in (1, 2, 3)]
            self.eqs = eqs
            self.qm = qm2
            self.play(*during(disappear(self.qm), 0, 0.4),
                      *during(appear(*eqs, shift=None, lag=0.35), 0.4, 1.0), run_time=1.8)
            c.wait_until("differ")
            def row_box(t, row):
                return Rectangle(width=t.rows[0].width + 0.4, height=0.62).set_stroke(YELLOW, 3).move_to(
                    _p(t.rows[0].get_x(), row.get_y()))
            box_rs, box_jk = row_box(rs, rs.rows[4]), row_box(tab, self.row4)
            self.boxes = (box_rs, box_jk)
            self.play(GrowFromCenter(box_rs), GrowFromCenter(box_jk), run_time=1.2)
            c.wait_until("illegal")
            self.play(*recolor(list(rs.rows[4]), RED), run_time=1.2)
            c.wait_until("both outputs")
            self.blink(list(rs.rows[4][2:4]), RED, 1.8, buff=0.1, fill=True)

    # -------------------------------------------------------------- c3.jk.5
    def clip5(self):
        tab, sym, rs, r4 = self.tab, self.sym, self.rs, self.row4
        with self.say("c3.jk.5") as c:
            self.set_inputs(1, 1, rt=1.0)
            c.wait_until("set both inputs")
            self.play(*appear(*r4[:2], shift=None, lag=0.3), run_time=1.0)
            c.wait_until("swap")
            q, qb = tab.rows[1][2], tab.rows[1][3]
            # both copies lift out sideways, drop down the free gap between the Q' and Q-bar' columns
            # (clear of the row 2-3 digits), then step sideways into row 4: Q-bar first, then Q
            gx = (q.get_right()[0] + qb.get_left()[0]) / 2
            c_qb, a_qb = glide(qb, r4[2], [_p(gx, qb.get_y()), _p(gx, r4.get_y())])
            c_q, a_q = glide(q, r4[3], [_p(gx, q.get_y()), _p(gx, r4.get_y())])
            self.play(*during(a_qb, 0, 0.55), *during(a_q, 0.45, 1.0), run_time=3.0)
            self.remove(c_qb, c_q)
            self.add(r4[2], r4[3])
            c.wait_until("flip")
            self.edge(set_q(sym, 0))
            c.wait_until("whatever state")
            self.blink([sym.led_q, sym.led_qb], GREEN, 1.4, buff=0.12, extra=disappear(self.up))
            c.wait_until("name")
            self.play(*appear(r4[4]), run_time=1.0)
            c.wait_until("summary")
            box_rs, box_jk = self.boxes
            arr = Arrow(box_rs.get_right(), box_jk.get_left(), buff=0.05, stroke_width=6,
                        max_tip_length_to_length_ratio=0.3, color=YELLOW)
            rest = [sym, self.rs_lab, *rs.rows[:4], rs.lines, *tab.rows[:4], tab.lines, *self.eqs]
            self.play(*set_alpha(rest, DIMMED), GrowArrow(arr), run_time=1.6)
