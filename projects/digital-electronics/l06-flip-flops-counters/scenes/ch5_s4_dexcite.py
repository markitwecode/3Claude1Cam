"""Chapter 5, scene 4: the D excitation table, D = Q'. Clips c5.dexc.1 – c5.dexc.3.

Shared with ch5_s5 / s6 / s8: `d_exc_table()` (header `Q Q' | D`, ch3_s3_jk.jk_table() styling).
The D flip-flop is ch2_s6's make_ff (no bubble); the J-K symbol is ch3_s3's jk_symbol() (copied).
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
# Symbols (copied from ch2_s6_symbols.make_ff and ch3_s3_jk.jk_symbol)
# =============================================================================================
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
LOW_OP = 0.18


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),)):
    """ch2_s6's D flip-flop box (no bubble); `ins` = (label, y) BLUE inputs on the left.
    Parts: .box .tri .clk_w .in_w .q_w .qb_w .labels (inputs, Q, Q-bar)."""
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


def place_ff(g, box_center, scale):
    """Scale an ff (labels kept >= size 30) and put its box centre at box_center."""
    hs = [lab.height for lab in g.labels]
    c = g.box.get_center()
    g.scale(scale, about_point=c).shift(np.array(box_center) - c)
    for lab, h0 in zip(g.labels, hs):
        lab.scale_to_fit_height(h0 * max(scale, 30 / 36))
    return g


def toggle(v, color=BLUE):
    g = VGroup()
    track = RoundedRectangle(corner_radius=0.19, width=0.78, height=0.38).set_stroke(color, 3).set_fill(BG, 1)
    knob = Circle(radius=0.13).set_stroke(width=0)
    g.add(track, knob)
    knob.move_to(track.get_center() + (0.2 if v else -0.2) * RIGHT).set_fill(color if v else DIM, 1)
    return g


def led(on):
    return Circle(radius=0.21).set_stroke(GREEN, 3).set_fill(GREEN, 0.9 if on else 0.0)


def jk_symbol(j=0, k=0, q=1):
    """ch3_s3's J-K flip-flop: make_ff(ins=(J, K)) + BLUE switches, YELLOW button, GREEN LEDs."""
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
    g = VGroup(ff, sw_j, sw_k, btn, led_q, led_qb)
    g.ff = ff
    w = {"j": ff.in_w[0], "k": ff.in_w[1], "q": ff.q_w, "qb": ff.qb_w, "clk": ff.clk_w}
    for key, v in (("j", j), ("k", k), ("q", q), ("qb", 1 - q), ("clk", 0)):
        w[key].set_stroke(opacity=1.0 if v else LOW_OP)
    return g


# =============================================================================================
# Shared table: d_exc_table()  (ch3_s3_jk.grid_table styling)
# =============================================================================================
def grid_table(rows, xs, size=44, pitch=0.66, seps=(), colors=None):
    """ch1_s2's grid_table: rows of strings ('$...' -> MathTex, else T); header row at y = 0,
    column centres xs. VGroup(*rows, lines), .rows, .lines."""
    out = []
    for i, row in enumerate(rows):
        cells = []
        for j, s in enumerate(row):
            col = (colors[i] if colors and colors[i] else FG)
            m = MathTex(s[1:], font_size=size, color=col) if s.startswith("$") else T(s, size=size * 0.82, color=col)
            m.move_to(_p(xs[j], -i * pitch))
            cells.append(m)
        out.append(VGroup(*cells))
    top, bot = 0.4, -(len(rows) - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(out[0].get_left()[0] - 0.3, -pitch / 2),
                   _p(out[0].get_right()[0] + 0.3, -pitch / 2)).set_stroke(DIM, 2))
    g = VGroup(*out, lines)
    g.rows, g.lines = out, lines
    return g


D_XS = [0, 0.9, 2.1]      # Q, Q', D column centres
D_SEPS = [1.5]


def d_exc_table():
    """The D flip-flop excitation table (slide p. 97) in ch3_s3's jk_table() styling, size 44,
    pitch 0.66: header `Q Q' | D` (Q, Q' GREEN, D BLUE), rows 00|0, 01|1, 10|0, 11|1 (FG).
    Header row centred at y = 0, Q column at x = 0; 2.7 wide x 3.42 tall incl. lines.
    .rows[0] header, .rows[1..4] (cells: Q, Q', D), .lines (separator, header rule)."""
    rows = [["$Q", "$Q'", "$D"],
            ["$0", "$0", "$0"],
            ["$0", "$1", "$1"],
            ["$1", "$0", "$0"],
            ["$1", "$1", "$1"]]
    tab = grid_table(rows, D_XS, size=44, pitch=0.66, seps=D_SEPS)
    h = tab.rows[0]
    h[0].set_color(GREEN)
    h[1].set_color(GREEN)
    h[2].set_color(BLUE)
    return tab


# =============================================================================================
# Scene-only helpers and layout
# =============================================================================================
def strip(q, q2, center, w=1.6, h=0.3):
    """Tiny before -> after trace: GREEN level Q, then level Q' after the clock edge (DIM dashed
    tick with a small YELLOW triangle under it)."""
    cx, cy = center
    lo, hi = cy - h / 2, cy + h / 2
    y1, y2 = (hi if q else lo), (hi if q2 else lo)
    line = VMobject().set_points_as_corners(
        [_p(cx - w / 2, y1), _p(cx, y1), _p(cx, y2), _p(cx + w / 2, y2)]).set_stroke(GREEN, 4)
    tick = DashedLine(_p(cx, lo - 0.07), _p(cx, hi + 0.07), dash_length=0.05).set_stroke(DIM, 2)
    tri = Triangle().scale(0.06).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(cx, lo - 0.13))
    return VGroup(tick, line, tri)


FF_BIG = (_p(0, 1.4), 1.0)        # clip 1: the D flip-flop, centred
FF_SMALL = (_p(-5.5, 0.5), 0.7)   # clips 2-3: small, left of the table
TAB_K = 1.45                      # table scale here (size 44 -> ~64)
TAB_AT = _p(-0.7, 2.8)            # Q column x, header y
STRIP_X = -2.8
JK_AT = (_p(5.2, 0.5), 0.7)
ROW_Y = (-2.55, -3.45)              # truth / excitation rows


class DExcitation(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- clip 1
        ff = place_ff(make_ff(), *FF_BIG)
        q_wire_end = ff.q_w.get_end()
        d_wire_start = ff.in_w[0].get_start()
        q0 = MathTex("0", font_size=52, color=GREEN).next_to(q_wire_end, RIGHT, buff=0.2)
        want = VGroup(T("want", 32, DIM), MathTex("Q' = 1", font_size=48, color=GREEN)).arrange(RIGHT, buff=0.2)
        want.next_to(q0, RIGHT, buff=0.7).align_to(q0, DOWN)
        d_q = MathTex("D", "=", "?", font_size=52)
        d_q[0].set_color(BLUE)
        d_q.next_to(d_wire_start, LEFT, buff=0.25)

        def arrow_row(label, lcol, left_txt, right_txt, y, direction):
            lab = T(label, 34, lcol)
            lab.move_to(_p(-3.0, y), aligned_edge=RIGHT).set_y(y)
            lt = T(left_txt, 32, BLUE).move_to(_p(-2.0, y))
            rt = T(right_txt, 32, GREEN)
            rt.move_to(_p(0.8, y), aligned_edge=LEFT).set_y(y)
            a, b = _p(-1.3, y), _p(0.55, y)
            arr = Arrow(a, b, buff=0, stroke_width=5, color=FG) if direction == "right" else \
                Arrow(b, a, buff=0, stroke_width=5, color=YELLOW)
            return lab, lt, arr, rt

        t_lab, t_in, t_arr, t_out = arrow_row("truth table", FG, "inputs", "next state", ROW_Y[0], "right")
        e_lab, e_in, e_arr, e_out = arrow_row("excitation table", YELLOW, "input",
                                              "current state, next state", ROW_Y[1], "left")

        with self.say("c5.dexc.1") as c:
            self.play(*appear(ff, shift=None), run_time=1.2)
            c.wait_until("current state")
            self.play(*appear(q0), run_time=1.0)
            c.wait_until(own_word=want[0])
            self.play(*appear(want), run_time=1.0)
            c.wait_until("input")
            self.play(*appear(d_q), run_time=1.0)
            c.wait_until("truth")
            self.play(*appear(t_lab), run_time=1.0)
            c.wait_until("inputs")
            self.play(*appear(t_in), GrowArrow(t_arr), *appear(t_out), run_time=1.5)
            c.wait_until("backwards")
            self.play(*appear(e_lab, e_out), GrowArrow(e_arr), *appear(e_in), run_time=1.8)  # early: the reverse question, already said

        # ---------------------------------------------------------------- clip 2
        tab = d_exc_table()
        tab.scale(TAB_K, about_point=ORIGIN).shift(TAB_AT)
        head, rows = tab.rows[0], tab.rows[1:]
        values = [(0, 0), (0, 1), (1, 0), (1, 1)]
        strips = [strip(a, b, (STRIP_X, r.get_y())) for (a, b), r in zip(values, rows)]

        with self.say("c5.dexc.2") as c:
            ff.target = place_ff(ff.copy(), *FF_SMALL)
            self.play(*disappear(q0, want, d_q), run_time=0.8)
            self.play(MoveToTarget(ff), run_time=1.3)
            self.play(*appear(*head, shift=None, lag=0.15), FadeIn(tab.lines), run_time=1.0)  # early: the column heads, read row by row
            for k, (r, s) in enumerate(zip(rows, strips)):
                c.wait_until(f"r{k + 1}")
                rt = 1.2 if k == 0 else 0.9
                self.play(Create(s), *appear(r[0], r[1], shift=None, lag=0.2), run_time=rt)
                c.wait_until("set", nth=k)
                self.play(*appear(r[2], shift=None), run_time=0.8 if k == 0 else 0.6)
            c.wait_until("copy")
            qp_col = VGroup(head[1], *[r[1] for r in rows])
            d_col = VGroup(head[2], *[r[2] for r in rows])
            box = SurroundingRectangle(qp_col, color=YELLOW, buff=0.15, corner_radius=0.08)
            box.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12)
            box2 = SurroundingRectangle(d_col, color=YELLOW, buff=0.15, corner_radius=0.08)
            box2.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12)
            self.play(FadeIn(box), run_time=1.0)
            c.wait_until("the dee column")
            dx = d_col.get_x() - qp_col.get_x()
            copies = [r[1].copy().set_color(YELLOW) for r in rows]
            self.add(*copies)
            self.play(*[m.animate.shift(dx * RIGHT) for m in copies], Transform(box, box2), run_time=1.8)
            self.remove(*copies)
            self.play(*recolor([r[2] for r in rows], YELLOW), run_time=0.6)

        # ---------------------------------------------------------------- clip 3
        rule = MathTex("D", "=", "Q'", font_size=96)
        rule[0].set_color(BLUE)
        rule[2].set_color(GREEN)
        rule.move_to(_p(tab.get_x(), -2.8))
        q_col = [head[0], *[r[0] for r in rows]]
        tag = T("makes no\ndifference", 32, DIM, line_spacing=0.9)
        tag.move_to(_p(-1.6, rows[1].get_y() / 2 + rows[2].get_y() / 2), aligned_edge=RIGHT)
        tag.set_y((rows[1].get_y() + rows[2].get_y()) / 2)
        jk = jk_symbol()
        c0 = jk.ff.box.get_center()
        hs = [lab.height for lab in jk.ff.labels]
        jk.scale(JK_AT[1], about_point=c0).shift(JK_AT[0] - c0)
        for lab, h0 in zip(jk.ff.labels, hs):
            lab.scale_to_fit_height(h0 * 30 / 36)
        qmark = MathTex("?", font_size=80, color=YELLOW).move_to(_p(JK_AT[0][0], 2.65))

        with self.say("c5.dexc.3") as c:
            self.play(*disappear(t_lab, t_in, t_arr, t_out, e_lab, e_in, e_arr, e_out, box),
                      *recolor([r[2] for r in rows], FG), run_time=0.9)
            self.play(*appear(rule, shift=None), run_time=min(1.2, c.until("current")))
            c.wait_until("current")
            self.play(*set_alpha(q_col, DIMMED), *disappear(*strips), run_time=1.2)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("other")
            self.play(FadeIn(jk, shift=2.0 * LEFT), run_time=1.6)
            self.play(*appear(qmark), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
