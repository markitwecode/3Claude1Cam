"""Chapter 5, scene 3: the RS latch's table unfolds into a state transition table; the counter's table
skeleton (current / next / FF inputs). Clips c5.table.1 – c5.table.3."""
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
# ch1_s2's NOR RS latch (copied verbatim from ch1_s2_rslatch.py)
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




# =============================================================================================
# ch5_s6's counter table (copied verbatim from ch5_s6_modtable.py)
# =============================================================================================
MT_GX = (-2.8, 0.0, 2.8)      # column-group centres (current, next, FF inputs), rel. to x
MT_DX = 0.72                  # column pitch inside a group (bit 2, 1, 0 at -DX, 0, +DX)
MT_DEC = -4.1                 # GOLD decimal column, rel. to x
MT_SEPS = (-1.4, 1.4)         # vertical rules between the groups, rel. to x
MT_TITLE_Y, MT_HEAD_Y, MT_RULE_Y = 3.45, 2.75, 2.35
MT_ROW0_Y, MT_PITCH = 1.9, 0.6                 # data row i at y = 1.9 - 0.6 i (row 7 at -2.3)
MT_TOP, MT_BOT = 3.8, -2.65
MT_CELL, MT_HEAD = 40, 42                      # MathTex sizes of data cells / column headers


def mt_row_y(i):
    return MT_ROW0_Y - i * MT_PITCH


def mod_table(filled=True, x=0.0):
    titles = VGroup(*[T(s, 30).move_to(_p(gx, MT_TITLE_Y))
                      for s, gx in zip(("Current state", "Next state", "FF inputs"), MT_GX)])
    head_tex = (["Q_2", "Q_1", "Q_0"], ["Q_2'", "Q_1'", "Q_0'"], ["D_2", "D_1", "D_0"])
    head_col = (GREEN, GREEN, BLUE)
    heads = VGroup(*[VGroup(*[MathTex(t, font_size=MT_HEAD, color=col).move_to(_p(gx + (j - 1) * MT_DX, MT_HEAD_Y))
                              for j, t in enumerate(ts)])
                     for ts, col, gx in zip(head_tex, head_col, MT_GX)])
    lines = VGroup(*[Line(_p(sx, MT_TOP), _p(sx, MT_BOT)).set_stroke(DIM, 2) for sx in MT_SEPS])
    lines.add(Line(_p(MT_DEC - 0.35, MT_RULE_Y), _p(MT_GX[2] + 1.35, MT_RULE_Y)).set_stroke(DIM, 2))
    skel = VGroup(titles, heads, lines)

    def bits_row(v, gx):
        return VGroup(*[MathTex(b, font_size=MT_CELL).move_to(_p(gx + (j - 1) * MT_DX, mt_row_y(i)))
                        for j, b in enumerate(format(v, "03b"))])
    dec, cur, nxt, inp = VGroup(), VGroup(), VGroup(), VGroup()
    for i in range(8):
        dec.add(MathTex(str(i), font_size=MT_CELL, color=GOLD).move_to(_p(MT_DEC, mt_row_y(i))))
        cur.add(bits_row(i, MT_GX[0]))
        nxt.add(bits_row((i + 1) % 8, MT_GX[1]))
        inp.add(bits_row((i + 1) % 8, MT_GX[2]))
    g = VGroup(skel, dec, cur, nxt, inp) if filled else VGroup(skel)
    for m in (skel, dec, cur, nxt, inp):
        m.shift(RIGHT * x)
    g.skel, g.titles, g.heads, g.lines = skel, titles, heads, lines
    g.dec, g.cur, g.nxt, g.inp = dec, cur, nxt, inp
    g.groups = [cur, nxt, inp]
    g.col = lambda gi, j: VGroup(*[row[j] for row in g.groups[gi]])
    return g


def tiny_dff():
    """A small D flip-flop icon: box, D (BLUE) in, Q (GREEN) out, clock triangle and wire."""
    box = Rectangle(width=0.8, height=1.1).set_stroke(FG, 3)
    tri = Polygon(_p(-0.12, -0.55), _p(0.12, -0.55), _p(0, -0.37)).set_stroke(FG, 2)
    d_w = Line(_p(-0.65, 0.25), _p(-0.4, 0.25)).set_stroke(BLUE, 4)
    q_w = Line(_p(0.4, 0.25), _p(0.65, 0.25)).set_stroke(GREEN, 4)
    c_w = Line(_p(0, -0.8), _p(0, -0.55)).set_stroke(YELLOW, 4)
    d = T("D", 30, BLUE).move_to(_p(-0.2, 0.25))
    q = T("Q", 30, GREEN).move_to(_p(0.2, 0.25))
    return VGroup(box, tri, d_w, q_w, c_w, d, q)


# =============================================================================================
# Scene layout
# =============================================================================================
# clip 1: the RS table (ch1 s2 styling: MathTex 44 cells, T 36 comments, DIM rules)
CX = {"Q": -1.65, "S": -0.5, "R": 0.25, "Qn": 1.4, "Qb": 2.3}
CM0, CM1 = 3.25, 2.3            # comment column left edge: before / after the unfold
Y0, P0 = 1.6, 0.66              # RS table: header y, pitch (as in ch1)
HY, P1, GAP = 3.0, 0.56, 0.14   # unfolded table: header y, pitch, gap between the two blocks
ICON_POS = _p(-4.7, 0.3)


def ry(i):
    """y of data row i (0..7) of the unfolded table."""
    return HY - P1 * (i + 1) - (GAP if i >= 4 else 0)


def cell(s, x, y, color=FG, left=False):
    m = MathTex(s[1:], font_size=44, color=color) if s.startswith("$") else T(s, 36, color)
    if left:
        m.move_to(_p(x, y), aligned_edge=LEFT).set_y(y)
    else:
        m.move_to(_p(x, y))
    return m


def vline(x, top, bot):
    return Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2)


def hline(x0, x1, y):
    return Line(_p(x0, y), _p(x1, y)).set_stroke(DIM, 2)


# clip 2-3: the counter's table, scaled about ORIGIN then shifted
MS = 0.92
MSHIFT = _p(0.35, 1.85 - MT_TITLE_Y * MS)


def mpt(x, y):
    """A point of the unscaled mod_table frame mapped to the screen."""
    return _p(x, y) * MS + MSHIFT


class StateTable(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        rows = [["$S", "$R", "$Q'", r"$\overline{Q}\,'", "comment"],
                ["$0", "$0", "$Q", r"$\overline{Q}", "hold"],
                ["$0", "$1", "$0", "$1", "reset"],
                ["$1", "$0", "$1", "$0", "set"],
                ["$1", "$1", "$0", "$0", "illegal"]]
        keys = ["S", "R", "Qn", "Qb", "C"]
        cells = {}
        for r, row in enumerate(rows):
            for k, s in zip(keys, row):
                col = RED if r == 4 else FG
                cells[(r, k)] = cell(s, CM0 if k == "C" else CX[k], Y0 - r * P0, col, left=(k == "C"))
        top, bot = Y0 + 0.4, Y0 - 4 * P0 - 0.38
        hdr = VGroup(*[cells[(0, k)] for k in keys])
        lines0 = [vline(0.82, top, bot), vline(2.9, top, bot),
                  hline(hdr.get_left()[0] - 0.3, hdr.get_right()[0] + 0.3, Y0 - P0 / 2)]
        icon = rs_latch()
        icon.remove(icon.g1.num, icon.g2.num)
        icon.g1.remove(icon.g1.num)
        icon.g2.remove(icon.g2.num)
        icon.scale(0.6).move_to(ICON_POS)

        with self.say("c5.table.1") as c:
            c.wait_until("recall")
            self.play(*appear(icon, shift=None), run_time=1.0)
            c.wait_until("rs")
            self.play(*appear(*[cells[(0, k)] for k in keys], *lines0, shift=None, lag=0.05),  # early: table shown whole
                      run_time=1.0)
            self.play(*appear(*[VGroup(*[cells[(r, k)] for k in keys]) for r in range(1, 5)], lag=0.35),  # early: the ch1 table returns whole
                      run_time=1.6)
            # ---- unfold A: Q-bar' column goes, table moves up, Q column header arrives
            c.wait_until("unfold")
            qb = [cells[(r, "Qb")] for r in range(5)]
            moves = []
            for r in range(5):
                y = HY if r == 0 else ry(r - 1)
                for k in ["S", "R", "Qn"]:
                    m = cells[(r, k)]
                    a = m.animate.move_to(_p(CX[k], y))
                    if r == 0:
                        a = a.set_color(BLUE if k in "SR" else GREEN)
                    elif r == 4:
                        a = a.set_color(FG)
                    moves.append(a)
                m = cells[(r, "C")]
                moves.append(m.animate.move_to(_p(CM1 + m.width / 2, y)))
            q_head = cell("$Q", CX["Q"], HY, GREEN)
            tb, bb = HY + 0.4, ry(7) - 0.28
            lines1 = [vline(0.82, tb, bb), vline(1.95, tb, bb), hline(CX["Q"] - 0.4, 4.25, HY - 0.31)]
            self.play(*during(disappear(*qb), 0, 0.4),
                      *during(moves, 0.3, 1.0),
                      *during([ReplacementTransform(a, b) for a, b in zip(lines0, lines1)], 0.3, 1.0),
                      *during(appear(q_head), 0.65, 1.0), run_time=1.6)
            # ---- unfold B: the four rows are copied into the lower block (Q = 1)
            shift = ry(4) - ry(0)
            copies = {}
            for r in range(1, 5):
                for k in ["S", "R", "Qn", "C"]:
                    copies[(r, k)] = cells[(r, k)].copy().shift(shift * UP)
            region0 = Rectangle(width=4.25 - CX["S"] + 0.75, height=4 * P1).move_to(
                _p((CX["S"] - 0.4 + 4.25) / 2, (ry(0) + ry(3)) / 2))
            self.play(FlashAround(region0, time_width=1.5, color=TEAL, buff=0.02),  # early: copied rows of the table
                      *during(appear(*[VGroup(*[copies[(r, k)] for k in ["S", "R", "Qn", "C"]]) for r in range(1, 5)],
                                     shift=0.45 * DOWN, lag=0.2), 0.25, 1.0), run_time=1.8)
            self.wait(0.6)
            # ---- unfold C: the Q column fills, the hold rows' Q resolves to 0 and 1
            qcol = [cell("$0" if i < 4 else "$1", CX["Q"], ry(i)) for i in range(8)]
            h0 = cell("$0", CX["Qn"], ry(0))
            h1 = cell("$1", CX["Qn"], ry(4))
            self.play(*appear(*qcol, shift=None, lag=0.08),
                      *swap(cells[(1, "Qn")], h0), *swap(copies[(1, "Qn")], h1), run_time=1.6)

            # ---- cols: braces under the column groups
            by = ry(7) - 0.3
            specs = [("current\nstate", CX["Q"] - 0.32, CX["Q"] + 0.32, GREEN, "the current state"),
                     ("inputs", CX["S"] - 0.32, CX["R"] + 0.32, BLUE, "reset inputs"),
                     ("next\nstate", CX["Qn"] - 0.32, CX["Qn"] + 0.32, GREEN, "the next state")]
            braces = []
            for txt, xl, xr, col, cue in specs:
                br = span_brace(_p(xl, by), _p(xr, by), DOWN, color=col, buff=0.05)
                lab = VGroup(*[T(w, 30, col) for w in txt.split("\n")]).arrange(DOWN, buff=0.08)
                lab.next_to(br, DOWN, buff=0.1)
                braces += [br, lab]
                c.wait_until(cue)
                self.play(GrowFromCenter(br), *appear(lab), run_time=1.0)

            # ---- rows: the two blocks
            tags = []
            for i, (cue, v) in enumerate([("once with cue at zero", "0"), ("once with cue at one", "1")]):
                blk = VGroup(*qcol[4 * i:4 * i + 4])
                tag = MathTex(f"Q = {v}", font_size=40, color=GREEN).move_to(_p(5.3, (ry(4 * i) + ry(4 * i + 3)) / 2))
                tags.append(tag)
                c.wait_until(cue)
                region = Rectangle(width=4.25 - CX["Q"] + 0.35, height=4 * P1).move_to(
                    _p((CX["Q"] - 0.4 + 4.25) / 2, (ry(4 * i) + ry(4 * i + 3)) / 2))
                self.play(FlashAround(region, run_time=1.5, time_width=1.5, color=GREEN, buff=0.02),
                          *appear(tag), run_time=1.5)

            # ---- read: one row, left part -> Q'
            c.wait_until("read")
            y = ry(2)
            row = [qcol[2], cells[(3, "S")], cells[(3, "R")], cells[(3, "Qn")], cells[(3, "C")]]
            box = Rectangle(width=4.25 - CX["Q"] + 0.25, height=0.5).move_to(_p((CX["Q"] - 0.4 + 4.25) / 2, y))
            box.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).set_z_index(-1)
            self.play(FadeIn(box), *recolor(row, YELLOW), run_time=1.0)
            arr = Arrow(_p(CX["R"] + 0.17, y), _p(CX["Qn"] - 0.17, y), buff=0, color=YELLOW,
                        stroke_width=5, max_tip_length_to_length_ratio=0.35)
            self.play(GrowArrow(arr), run_time=1.0)

        self.rs_parts = ([cells[k] for k in cells if k[1] != "Qb" and k != (1, "Qn")]
                         + [copies[k] for k in copies if k != (1, "Qn")]
                         + qcol + [h0, h1, q_head] + lines1)
        self.rs_extra = [icon, *braces, *tags, box, arr]

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        m = mod_table(filled=False)
        rule_short = Line(_p(MT_DEC - 0.35, MT_RULE_Y), _p(MT_SEPS[1], MT_RULE_Y)).set_stroke(DIM, 2)
        everything = VGroup(m.skel, m.dec, m.cur, m.nxt, m.inp, rule_short)
        everything.scale(MS, about_point=ORIGIN).shift(MSHIFT)
        for t in m.titles:
            t.scale(1.04)
        self.m, self.rule_short = m, rule_short

        mini = VGroup(*self.rs_parts)
        with self.say("c5.table.2") as c:
            settle(self, mini)
            mini.generate_target()
            mini.target.scale_to_fit_width(2.4).to_corner(UL, buff=0.5).set_opacity(DIMMED)
            sk = [m.titles[0], m.titles[1], m.heads[0], m.heads[1], m.lines[0], rule_short]
            self.play(*during(disappear(*self.rs_extra), 0, 0.4),
                      *during([MoveToTarget(mini)], 0.15, 0.75),
                      *during(appear(*sk, shift=None, lag=0.05), 0.55, 1.0),  # early: table skeleton
                      run_time=2.0)
            # noinputs
            tag = T("only input: CLK", 30, YELLOW).move_to(_p(4.45, mpt(0, mt_row_y(1))[1]))
            c.wait_until("noinputs")
            self.play(*appear(tag), run_time=1.0)  # early: tag on {noinputs} (the voice says "clock")
            # pair
            yb = mpt(0, mt_row_y(1.6))[1]
            pair = CurvedArrow(_p(mpt(MT_GX[0], 0)[0], yb), _p(mpt(MT_GX[1], 0)[0], yb), angle=-PI / 3,
                               color=YELLOW, stroke_width=4)
            c.wait_until("pair")
            self.play(Create(pair), run_time=1.2)
            # example
            four = MathTex("4", font_size=MT_CELL, color=GOLD).scale(MS).move_to(
                mpt(MT_SEPS[1] + 0.4, mt_row_y(3)))
            c.wait_until("three")
            self.play(*appear(m.dec[3]), run_time=0.8)
            c.wait_until("written zero")
            self.play(*appear(*m.cur[3], lag=0.3), run_time=1.2)
            c.wait_until("four")
            self.play(*appear(four), run_time=0.8)
            c.wait_until("written one")
            self.play(*appear(*m.nxt[3], lag=0.3), run_time=1.2)
        self.tag, self.four, self.pair = tag, four, pair

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        m = self.m
        with self.say("c5.table.3") as c:
            c.wait_until("more columns")
            ff = [m.titles[2], *m.heads[2], m.lines[1]]
            self.play(*during(disappear(self.tag, m.dec[3], self.four), 0, 0.4),
                      *during([FadeIn(x, shift=0.6 * LEFT) for x in ff], 0.35, 1.0),  # early: header of new cols
                      *during([ReplacementTransform(self.rule_short, m.lines[2])], 0.35, 1.0),
                      run_time=1.6)
            # inputs: arrow down to a tiny D flip-flop
            ffl = tiny_dff().scale(0.95).move_to(_p(5.85, mpt(0, mt_row_y(4))[1]))
            dy = ffl[2].get_center()[1]
            dn = Arrow(_p(mpt(MT_GX[2] + 1.4, 0)[0], dy), _p(ffl[2].get_left()[0] - 0.02, dy), buff=0,
                       color=BLUE, stroke_width=5, max_tip_length_to_length_ratio=0.4)
            c.wait_until("inputs")
            self.play(GrowArrow(dn), *during(appear(ffl, shift=None), 0.4, 1.0), run_time=1.4)
            # excitation
            br = Brace(VGroup(m.titles[2], *m.heads[2]), UP, buff=0.12, color=YELLOW)
            ex = T("excitation", 30, YELLOW).next_to(br, UP, buff=0.08)
            c.wait_until(own_word=ex)
            self.play(GrowFromCenter(br), *appear(ex), run_time=1.2)
            title = T("Modified state transition table", 44).move_to(_p(0.35, 3.2))
            c.wait_until("modified state transition table")
            self.play(*appear(title), run_time=1.0)
