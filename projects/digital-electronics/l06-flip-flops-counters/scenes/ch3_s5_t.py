"""Chapter 3, scene 5: the T flip-flop (J = K = T; Q' = T xor Q; a D flip-flop with Q-bar fed back
to D toggles once per edge, unlike part 2's oscillating latch). Clips c3.t.1 – c3.t.4.

Reusable (copy, don't import):
  jk_symbol / place_symbol / jk_table / make_ff / grid_table ...   copied from ch3_s3_jk.py
                         (make_ff gains a q_len argument, default unchanged).
  t_table()              the T table this scene ends clip 1 with (jk_table styling, same geometry).
  xor_formula()          Q' = T xor Q.
  toggle_loop()          D flip-flop with the GREEN Q-bar -> D loop over the top (the recap and
                         ch6 s2 reuse it). Built with the box centred at ORIGIN, scale 1;
                         parts .ff (make_ff, D) and .loop.
  feedback_latch / buzz_window   copied from ch2_s2_window.py.
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


def poly(pts, color, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# =============================================================================================
# Copied from scenes/ch3_s3_jk.py (shared J-K pieces), unchanged except make_ff's q_len
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


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE):
    """ch2_s7's make_ff box, pins and triangle; `ins` = (label, y) BLUE inputs on the left.
    (q_len: added here, so toggle_loop's Q wire can run past the loop; default as in s3.)"""
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
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
# This scene's shared pieces (the recap and ch6 s2 reuse them)
# =============================================================================================
QB = r"$\overline{Q}"
T_COL = 0.375          # the T column: midway between J (x 0) and K (x 0.75) of TAB_XS


def t_table():
    """The T table, as this scene leaves it: header `T | Q' Q-bar' | comment`, rows
    `0 | Q Q-bar | hold`, `1 | Q-bar Q | toggle`, in jk_table()'s styling and geometry (header at
    y = 0, the J column's x = 0, so shift by the same point as a J-K table). .rows .lines."""
    tab = grid_table([["$T", "$Q'", r"$\overline{Q}\,'", "comment"],
                      ["$0", "$Q", QB, "hold"],
                      ["$1", QB, "$Q", "toggle"]],
                     [T_COL] + TAB_XS[2:], size=44, pitch=TAB_PITCH, seps=TAB_SEPS)
    r = tab.rows
    r[0][0].set_color(BLUE)
    for i in (0, 1, 2):
        for m in r[i][1:3]:
            m.set_color(GREEN)
    r[2][3].set_color(YELLOW)
    return tab


def xor_formula(size=84):
    """Q' = T xor Q (Q', Q GREEN; T BLUE). Parts [0] Q' [1] = [2] T [3] xor [4] Q."""
    f = MathTex("Q'", "=", "T", r"\oplus", "Q", font_size=size)
    f[0].set_color(GREEN)
    f[2].set_color(BLUE)
    f[4].set_color(GREEN)
    return f


def toggle_loop():
    """D flip-flop (make_ff) with Q-bar wired back to D: GREEN loop right of Q-bar, up (hopping
    over Q), over the top, down to D's stub. Box centred at ORIGIN, scale 1; .ff .loop .box."""
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    ff = make_ff(q_len=WIRE + 0.85)                 # Q's wire runs past the loop's riser
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    loop = VMobject().set_points_as_corners(pts).set_stroke(GREEN, 5)
    g = VGroup(ff, loop)
    g.ff, g.loop, g.box = ff, loop, ff.box
    return g


def pulse(mob, color=YELLOW):
    """Emphasis on a single glyph: its colour goes to `color` and back (no flash outline: a
    FlashAround on one letter shows its top edge first, which reads as an overbar)."""
    base = mob.get_color()

    def f(m, a):
        m.set_color(interpolate_color(ManimColor(base), ManimColor(color), there_and_back(a)))
    return UpdateFromAlphaFunc(mob, f)


def table_lines(n, pitch, seps, x0, x1):
    top, bot = 0.4, -(n - 1) * pitch - 0.38
    lines = VGroup(*[Line(_p(x, top), _p(x, bot)).set_stroke(DIM, 2) for x in seps])
    lines.add(Line(_p(x0, -pitch / 2), _p(x1, -pitch / 2)).set_stroke(DIM, 2))
    return lines


def footnote(tab):
    """s3's footnote, under the (full) J-K table."""
    foot = T("Where Q′ is the next state\nand Q is the current state", 32, line_spacing=1.15,
             t2c={"Q": GREEN})
    return foot.next_to(tab, DOWN, buff=1.1).set_x(tab.get_x())


# ---- ch2 s2's oscillating latch (copied from ch2_s2_window.py) ----------------------------------
def feedback_latch(center=ORIGIN, s=0.8):
    c = np.array(center)
    FB_EN = 0.6

    def P(x, y):
        return c + s * _p(x, y)

    hw, hh = s * BOX_W / 2, s * BOX_H / 2
    g = VGroup()
    g.box = Rectangle(width=2 * hw, height=2 * hh).set_stroke(FG, 4).set_fill(BG, 1).move_to(c)
    g.sq = Square(0.2).set_stroke(BLUE, 3).set_fill(BG, 1).move_to(g.box.get_bottom())
    xr_q = BOX_W / 2 + WIRE + 0.85
    g.d_w = Line(P(-BOX_W / 2 - WIRE, PIN_Y), P(-BOX_W / 2, PIN_Y)).set_stroke(BLUE, 5)
    g.q_w = Line(P(BOX_W / 2, PIN_Y), P(xr_q, PIN_Y)).set_stroke(GREEN, 5)
    g.qb_w = Line(P(BOX_W / 2, -PIN_Y), P(BOX_W / 2 + WIRE, -PIN_Y)).set_stroke(GREEN, 5)
    g.en_w = Line(P(0, -BOX_H / 2 - FB_EN), P(0, -BOX_H / 2) + 0.1 * DOWN).set_stroke(BLUE, 5)
    g.d_l = T("D", 36, BLUE).move_to(P(-BOX_W / 2, PIN_Y) + 0.3 * RIGHT)
    g.q_l = T("Q", 36, GREEN).move_to(P(BOX_W / 2, PIN_Y) + 0.3 * LEFT)
    g.qb_l = MathTex(r"\overline{Q}", font_size=40, color=GREEN).move_to(P(BOX_W / 2, -PIN_Y) + 0.3 * LEFT)
    g.en_l = T("EN", 30, BLUE).move_to(g.box.get_bottom() + 0.42 * UP)
    g.sym = VGroup(g.d_w, g.q_w, g.qb_w, g.en_w, g.box, g.sq, g.d_l, g.q_l, g.qb_l, g.en_l)
    g.add(g.sym)
    xr, top, xl, r = BOX_W / 2 + WIRE + 0.4, BOX_H / 2 + 0.45, -(BOX_W / 2 + WIRE + 0.4), 0.17
    arc = [_p(xr + r * np.cos(a), PIN_Y + r * np.sin(a)) for a in np.linspace(-PI / 2, PI / 2, 13)]
    pts = ([_p(BOX_W / 2 + WIRE, -PIN_Y), _p(xr, -PIN_Y), _p(xr, PIN_Y - r)] + arc[1:-1]
           + [_p(xr, PIN_Y + r), _p(xr, top), _p(xl, top), _p(xl, PIN_Y), _p(-BOX_W / 2 - WIRE, PIN_Y)])
    g.loop = VMobject().set_points_as_corners([c + s * q for q in pts]).set_stroke(GREEN, 5)
    g.clk_w = g.en_w.copy().set_stroke(YELLOW, 6).set_z_index(1)
    g.clk_l = T("CLK", 30, YELLOW).next_to(g.en_w.get_start(), LEFT, buff=0.18).shift(0.12 * UP)
    return g


def red_buzz(x_r, x_f, y_lo, h, offset, step, n, start_high, color=RED, width=4):
    lv = start_high
    pts = [(x_r, y_lo + h * lv)]
    for k in range(n):
        x = x_r + offset + k * step
        pts += [(x, y_lo + h * lv)]
        lv = 1 - lv
        pts += [(x, y_lo + h * lv)]
    pts.append((x_f, y_lo + h * lv))
    return poly(pts, color, width)


def buzz_window(w=2.4, h=0.6, gap=0.5, n=9):
    m = 0.35 * w
    x0, xr, xf, x1 = -w / 2 - m, -w / 2, w / 2, w / 2 + m
    yc = gap / 2
    g = VGroup()
    g.clk = poly([(x0, yc), (xr, yc), (xr, yc + h), (xf, yc + h), (xf, yc), (x1, yc)], YELLOW)
    g.band = Rectangle(width=w, height=2 * h + gap + 0.3).set_stroke(width=0).set_fill(YELLOW, 0.12)
    g.band.set_z_index(-1)
    g.buzz = red_buzz(xr, xf, -yc - h, h, 0.1 * w, 0.8 * w / (n - 1), n, 0)
    g.add(g.band, g.clk, g.buzz)
    return g


# ---- layout constants ----------------------------------------------------------------------------
TL_C = _p(-3.3, 0.75)          # clip 3: the toggle loop's box centre
TL_C4, TL_K4 = _p(3.4, 1.75), 0.85   # clip 4: moved right, smaller
LATCH_C = _p(-3.6, 1.35)


class TFlipFlop(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    # ---- c3.t.1: tie J and K together; the table collapses to hold / toggle -------------------------
    def clip1(self):
        with self.say("c3.t.1") as c:
            S = self.S = jk_symbol(0, 0, 1)
            place_symbol(S, *SYM_A)
            tab = self.tab = jk_table()
            tab.shift(JK_A)
            foot = self.foot = footnote(tab)
            self.play(*appear(S, tab, foot, shift=None, lag=0), run_time=1.0)  # early: continuity from s3

            # {tie}: the J and K wires bend together into one wire, the two switches become one; J, K -> T
            ff = S.ff
            j_w, k_w = ff.in_w
            j_l, k_l = ff.labels[0], ff.labels[1]
            yc = ff.box.get_y()
            t_w = j_w.copy().set_y(yc)
            t_l = T("T", 36, BLUE).scale(S.s).move_to(_p(j_l.get_x(), yc))
            self.play(Transform(j_w, t_w), Transform(k_w, t_w.copy()),
                      S.sw_j.animate.set_y(yc), S.sw_k.animate.set_y(yc),
                      *during(disappear(j_l, k_l), 0, 0.45),
                      run_time=min(1.6, max(0.8, c.until("tee") - 0.1)))
            ff.remove(k_w, j_l, k_l)
            S.remove(S.sw_k)
            self.remove(k_w, j_l, k_l, S.sw_k)
            settle(self, S)
            S.sw_t = S.sw_j
            c.wait_until("tee")
            self.play(*appear(t_l), run_time=1.0)
            ff.add(t_l)
            settle(self, S)
            c.wait_until("rows")

            # {rows}: J != K rows go, the two J = K rows slide together
            r = tab.rows
            self.play(*disappear(r[2], r[3]), run_time=1.0)
            settle(self, tab, drop=[r[2], r[3]])
            new_lines = table_lines(3, TAB_PITCH, TAB_SEPS, r[0].get_left()[0] - JK_A[0] - 0.3,
                                    r[0].get_right()[0] - JK_A[0] + 0.3).shift(JK_A)
            self.play(r[4].animate.shift(2 * TAB_PITCH * UP),
                      *[Transform(a, b) for a, b in zip(tab.lines, new_lines)],
                      run_time=min(1.5, max(0.8, c.until("hold") - 0.6)))
            c.wait_until("hold")

            # {hold}: the J K column becomes one T column (header and both rows at once)
            tx = JK_A[0] + T_COL
            t_head = MathTex("T", font_size=44, color=BLUE).move_to(_p(tx, r[0][0].get_y()))
            self.play(*during(disappear(r[0][0], r[0][1], r[1][1], r[4][1]), 0, 0.45),
                      *during([r[1][0].animate.set_x(tx), r[4][0].animate.set_x(tx)], 0.35, 1),
                      *during(appear(t_head, shift=None), 0.5, 1),
                      run_time=1.4)
            self.play(FlashAround(r[1], run_time=1.2, time_width=1.5, color=FG), run_time=1.2)
            c.wait_until("toggle")

            # {toggle}: the toggle row lights up
            self.play(FlashAround(r[4], run_time=1.4, time_width=1.5), run_time=1.4)
            for row, drop in ((r[0], [r[0][0], r[0][1]]), (r[1], [r[1][1]]), (r[4], [r[4][1]])):
                row.remove(*drop)
            r[0].add(t_head)
            settle(self, tab)
            self.trows = [r[1], r[4]]

            # {name}: the T flip-flop
            name = T("T flip-flop (toggle)", 36, FG, t2c={"(toggle)": YELLOW})
            name.next_to(S.ff.box, UP, buff=0.4)
            self.name = name
            c.wait_until("name")
            self.play(*appear(name), run_time=1.0)

    # ---- c3.t.2: Q' = T xor Q ------------------------------------------------------------------------
    def clip2(self):
        tab, S = self.tab, self.S
        with self.say("c3.t.2") as c:
            # {compact}: clear the symbol, table to the top left, its rows pulse
            self.play(*disappear(S, self.name, self.foot), run_time=1.0)
            self.play(*flash(self.trows, run_time=1.3, time_width=1.5), run_time=1.3)
            c.wait_until("xor")

            # {xor}: the formula grows out of the table
            f = xor_formula().move_to(_p(3.4, tab.rows[1].get_y()))
            self.formula = f
            self.play(FadeIn(f, target_position=tab.get_right() + 0.9 * RIGHT, scale=0.4),
                      run_time=1.6)
            c.wait_until("exclusive")

            # the four-row check beside it
            ck = grid_table([["$T", "$Q", "$Q'"], ["$0", "$0", "$0"], ["$0", "$1", "$1"],
                             ["$1", "$0", "$1"], ["$1", "$1", "$0"]],
                            [0, 0.75, 1.75], size=44, pitch=TAB_PITCH, seps=[1.25])
            ck.rows[0][0].set_color(BLUE)
            ck.rows[0][1].set_color(GREEN)
            ck.rows[0][2].set_color(GREEN)
            ck.shift(_p(-1.6, -0.45))
            self.ck = ck
            # grid and digits fade in together, in place (a lagged drop let rows pass through each other)
            self.play(*appear(ck, shift=None, lag=0),  # early: the check table is shown whole, then walked
                      run_time=min(1.2, c.until("zero") - 0.5))
            c.wait_until("zero")

            # {zero}: T = 0 keeps Q
            br0 = Brace(VGroup(ck.rows[1], ck.rows[2]), RIGHT, buff=0.35, color=FG)
            lb0 = T("keeps Q", 34, FG).next_to(br0, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br0), pulse(f[2]), run_time=1.2)
            c.wait_until(own_word=lb0)
            self.play(*appear(lb0), run_time=1.0)
            c.wait_until("one")

            # {one}: T = 1 flips Q
            br1 = Brace(VGroup(ck.rows[3], ck.rows[4]), RIGHT, buff=0.35, color=YELLOW)
            lb1 = T("flips Q", 34, YELLOW).next_to(br1, RIGHT, buff=0.2)
            self.play(GrowFromCenter(br1), *recolor([ck.rows[3][2], ck.rows[4][2]], YELLOW), run_time=1.2)
            self.play(*appear(lb1), run_time=1.0)
            c.wait_until("match")

            # {match}: the brackets name the table's hold and toggle
            # each pair is spotlit on its own word: the other pair dims meanwhile
            hold, tog = self.trows[0][-1], self.trows[1][-1]
            side0 = [br0, lb0, ck.rows[1], ck.rows[2], self.trows[0]]
            side1 = [br1, lb1, ck.rows[3], ck.rows[4], self.trows[1]]
            c.wait_until("hold")
            self.play(*set_alpha(side1, DIMMED),
                      *flash([lb0, hold], color=FG, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("toggle")
            self.play(*set_alpha(side1, 1), *set_alpha(side0, DIMMED),
                      *flash([lb1, tog], run_time=1.2, time_width=1.5), run_time=1.2)

    # ---- c3.t.3: a D flip-flop with Q-bar fed back to D --------------------------------------------
    def clip3(self):
        with self.say("c3.t.3") as c:
            TL = self.TL = toggle_loop()
            TL.shift(TL_C)
            self.play(*during(disappear(*self.mobjects), 0, 0.45),           # all of clip 2 leaves together
                      *during(appear(TL.ff, shift=0.2 * UP), 0.5, 1), run_time=1.6)
            c.wait_until("wire its")
            self.play(Create(TL.loop), run_time=min(2.0, c.until("next") - 0.5))
            settle(self, TL)
            c.wait_until("next")

            # {next}: Q' = D = Q-bar
            lab = MathTex("Q'", "=", "D", "=", r"\overline{Q}", font_size=60)
            lab[0].set_color(GREEN)
            lab[2].set_color(BLUE)
            lab[4].set_color(GREEN)
            lab.move_to(_p(TL_C[0] + 0.3, -2.45))
            self.play(FlashAround(TL.ff.tri, run_time=1.2, time_width=1.5, buff=0.08),
                      *during(appear(lab), 0.3, 1), run_time=1.4)
            c.wait_until("same")

            # {same}: = the T flip-flop with T tied to 1
            eq = MathTex("=", font_size=96).move_to(_p(0.55, TL_C[1]))
            ts = make_ff(_p(3.95, TL_C[1]), ins=(("T", 0.0),))
            one = MathTex("1", font_size=52, color=BLUE).next_to(ts.in_w[0].get_start(), LEFT, buff=0.15)
            tsym = VGroup(ts, one)
            self.play(*appear(eq, shift=None), *appear(tsym, shift=None), run_time=1.5)
            f2 = MathTex("Q'", "=", "1", r"\oplus", "Q", "=", r"\overline{Q}", font_size=60)
            for i in (0, 4, 6):
                f2[i].set_color(GREEN)
            f2[2].set_color(BLUE)
            f2.move_to(_p(3.95, lab.get_y()))
            self.c3_extra = [lab, eq, tsym, f2]
            c.wait_until("with tee")
            self.play(*appear(f2), pulse(one), run_time=1.2)

    # ---- c3.t.4: the latch oscillated; the flip-flop flips once per edge ---------------------------
    def clip4(self):
        TL = self.TL
        with self.say("c3.t.4", gap=2.6) as c:
            # {runaway}: keep the loop, move it right; the latch version comes in on the left
            c.wait_until("in part two")
            L = feedback_latch(LATCH_C, s=1.0)
            L.en_l.shift(0.16 * LEFT)
            rest = [m for m in self.mobjects if m is not TL]
            self.play(*during(disappear(*rest), 0, 0.4),                     # the T side and both formulas leave together
                      *during([TL.animate.scale(TL_K4).move_to(
                          TL_C4 + (TL.get_center() - TL.box.get_center()) * TL_K4)], 0.3, 0.75),
                      *during(appear(VGroup(L.sym, L.loop, L.clk_w), L.clk_l, shift=None, lag=0), 0.72, 1),
                      run_time=2.2)
            c.wait_until("while enable")

            # the EN-high window: Q buzzes RED all through it
            bw = buzz_window(w=2.4, h=0.55, gap=0.5, n=11)
            bw.move_to(_p(LATCH_C[0] + 0.3, -2.0))
            l_clk = T("CLK", 30, YELLOW).next_to(bw.clk, LEFT, buff=0.2).align_to(bw.clk, DOWN)
            l_q = T("Q", 32, RED).next_to(bw.buzz, LEFT, buff=0.2).set_x(l_clk.get_x())
            self.play(FadeIn(bw.band), Create(bw.clk), *appear(l_clk, l_q, shift=None, lag=0), run_time=1.0)
            self.play(Create(bw.buzz, rate_func=linear), L.loop.animate.set_stroke(RED),
                      L.q_w.animate.set_stroke(RED), run_time=min(3.5, c.until("safe") - 0.4))
            c.wait_until("safe")

            # {safe}: the flip-flop: one clean step per rising edge
            x0, x1, per = 1.3, 6.55, 1.25
            rises = [1.65 + k * per for k in range(4)]
            ylo_c, ylo_q, h = -1.15, -2.45, 0.5
            cpts = [(x0, ylo_c)]
            for xr_ in rises:
                cpts += [(xr_, ylo_c), (xr_, ylo_c + h), (xr_ + per / 2, ylo_c + h), (xr_ + per / 2, ylo_c)]
            cpts.append((x1, ylo_c))
            clk = poly(cpts, YELLOW)
            qpts, lv = [(x0, ylo_q)], 0
            for xr_ in rises:
                qpts += [(xr_ + 0.05, ylo_q + h * lv)]
                lv = 1 - lv
                qpts += [(xr_ + 0.05, ylo_q + h * lv)]
            qpts.append((x1, ylo_q + h * lv))
            qw = poly(qpts, GREEN, 5)
            ticks = VGroup(*[DashedLine(_p(xr_, ylo_c), _p(xr_, ylo_q + h + 0.1), dash_length=0.08)
                             .set_stroke(YELLOW, 2, opacity=0.5) for xr_ in rises])
            r_clk = T("CLK", 30, YELLOW).move_to(_p(0.75, ylo_c + h / 2))
            r_q = T("Q", 32, GREEN).move_to(_p(0.75, ylo_q + h / 2))
            self.play(Create(clk), FadeIn(ticks), *appear(r_clk, r_q, shift=None, lag=0), run_time=1.2)
            self.play(Create(qw, rate_func=linear), run_time=min(3.0, c.until("ch6") - 0.4))
            c.wait_until("ch6")

            # {ch6}: forward tag
            tag = T("Part 6: first stage of a counter", 32, FG, t2c={"Part 6:": GOLD})
            tag.move_to(_p(3.7, -3.4))
            self.play(*appear(tag), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
