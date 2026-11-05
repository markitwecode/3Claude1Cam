"""Chapter 3, scene 4: a J-K with J = K = 1 toggling in time; Q runs at half the clock frequency. Clips c3.toggle.1 – c3.toggle.3.

Opens by fading in s3's J-K symbol and table already in their shrunk upper-left form (s3 ends empty).
Timing diagram in ch2's style (ch2_s5_slave TimingDiagram look, ch2_s6 up-arrows).
ch4 reuses the toggle waveform as Q0: see clk_points / toggle_points / toggle_trace below.
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


# ---- copied verbatim from ch3_s3_jk (don't import) ----------------------------------------
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



# ---- copied from ch3_s3_jk (scene helpers) --------------------------------------------------
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


# ---- timing waveforms (module level: ch4 reuses the toggle trace as Q0) ----------------------
def clk_points(x0, x1, rises, period):
    """CLK starting low: up at each rise, down half a period later."""
    pts = [(x0, 0)]
    for r in rises:
        pts += [(r, 0), (r, 1), (r + period / 2, 1), (r + period / 2, 0)]
    pts.append((x1, 0))
    return pts


def toggle_points(x0, x1, edges, start=0):
    """A trace that flips at every x in `edges` (propagation delay neglected)."""
    pts, b = [(x0, start)], start
    for x in edges:
        pts += [(x, b), (x, 1 - b)]
        b = 1 - b
    pts.append((x1, b))
    return pts


def trace(pts, y_mid, amp=0.3, color=GREEN, width=4):
    return (VMobject().set_points_as_corners([_p(x, y_mid + (amp if b else -amp)) for x, b in pts])
            .set_stroke(color, width))


def toggle_trace(x0, x1, edges, y_mid, amp=0.3, start=0, color=GREEN, width=4):
    return trace(toggle_points(x0, x1, edges, start), y_mid, amp, color, width)


def toggle_pieces(x0, x1, edges, y_mid, amp=0.3, start=0, color=GREEN, width=4):
    """The same trace cut at its edges: piece 0 is the opening flat, piece k starts with edge k-1."""
    xs = [x0, *edges, x1]
    out, b = [], start
    for k in range(len(xs) - 1):
        if k == 0:
            pts = [(xs[0], b), (xs[1], b)]
        else:
            pts = [(xs[k], b), (xs[k], 1 - b), (xs[k + 1], 1 - b)]
            b = 1 - b
        out.append(trace(pts, y_mid, amp, color, width))
    return out


# ---- layout ------------------------------------------------------------------------------------
X0, X1 = -5.0, 4.6
P = (X1 - X0) / 6.3                   # six clock cycles
RISES = [X0 + 0.5 * P + k * P for k in range(6)]
AMP = 0.3
CLK_Y, Q_Y = 0.05, -1.72
G4_Y, G8_Y, G_AMP = -2.75, -3.48, 0.2
SYM_POS = (_p(-5.14, 2.87), 0.58)    # box centre, scale (bbox about x -6.5..-4.0, y 1.3..3.6)
TAB_S, TAB_POS = 0.78, _p(-3.35, 3.38)  # s3's jk_table shrunk; J column x, header y
CAP_C = _p(3.75, 2.75)


def up_arrow(x, y):
    return Triangle().scale(0.1).set_stroke(width=0).set_fill(YELLOW, 1).move_to(_p(x, y))


def edge_line(x, y_mid, color, amp=AMP, width=9):
    return Line(_p(x, y_mid - amp), _p(x, y_mid + amp)).set_stroke(color, width)


class Toggle(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        sym = jk_symbol(j=0, k=0, q=0)
        place_symbol(sym, *SYM_POS)
        self.sym = sym
        tab = jk_table().scale(TAB_S)
        tab.shift(TAB_POS - _p(tab.rows[0][0].get_x(), tab.rows[0][0].get_y()))
        self.tab = tab

        with self.say("c3.toggle.1") as c:
            self.play(FadeIn(sym), FadeIn(tab), run_time=1.0)
            c.wait_until("both at one")
            self.play(flip(sym.sw_j, 1), lev(sym.w["j"], 1), flip(sym.sw_k, 1), lev(sym.w["k"], 1),
                      run_time=1.2)
            self.play(*set_alpha(tab.rows[:4], 0.35), *recolor(list(tab.rows[4]), YELLOW),
                      run_time=min(1.2, c.until("clock")))

            # ---- CLK
            c.wait_until("clock")
            clk_lab = MathTex(r"\mathrm{CLK}", font_size=40, color=DIM)
            clk_lab.move_to(_p(0, CLK_Y)).align_to(_p(X0 - 0.35, 0), RIGHT)
            self.clk = trace(clk_points(X0, X1, RISES, P), CLK_Y, AMP, YELLOW)
            self.play(*appear(clk_lab, shift=None), run_time=0.6)
            self.play(Create(self.clk), rate_func=linear, run_time=min(2.0, c.until("arrows")))
            c.wait_until("arrows")
            self.ups = [up_arrow(r, CLK_Y) for r in RISES]
            self.play(*[time_span(FadeIn(u, scale=0.5), 0.12 * i, 0.12 * i + 0.5) for i, u in enumerate(self.ups)],
                      run_time=1.2)

            # ---- guides: changes exactly on the edges
            c.wait_until("exactly on the edges")
            g_top, g_bot = CLK_Y + AMP + 0.12, Q_Y - AMP - 0.12
            self.guides = [Line(_p(r, g_top), _p(r, g_bot)).set_stroke(DIM, 1.5).set_z_index(-2) for r in RISES]
            self.play(*[GrowFromEdge(g, UP) for g in self.guides], run_time=1.5)

            # ---- Q starts at 0
            c.wait_until("start")
            q_lab = MathTex("Q", font_size=40, color=DIM)
            q_lab.move_to(_p(0, Q_Y)).align_to(_p(X0 - 0.35, 0), RIGHT)
            self.q_lab, self.clk_lab = q_lab, clk_lab
            self.qp = toggle_pieces(X0, X1, RISES, Q_Y, AMP)
            self.play(*appear(q_lab, shift=None), Create(self.qp[0]), run_time=1.2)

            # ---- edge by edge
            self.vals = []
            sym = self.sym
            for k, cue in enumerate(["e1", "e2", "e3", "e4"]):
                c.wait_until(cue)
                v = (k + 1) % 2
                lab = T(str(v), 30, GREEN).move_to(_p(RISES[k] + 0.28, Q_Y + AMP + 0.28))
                self.vals.append(lab)
                rt = 1.2 if k < 2 else 0.8
                self.play(Create(self.qp[k + 1]), *appear(lab, shift=0.15 * DOWN),
                          *pulse_clock(sym), *set_q(sym, v),
                          VShowPassingFlash(edge_line(RISES[k], CLK_Y, YELLOW), time_width=1.0),
                          run_time=rt)
            # the last two cycles fill in on their own
            # in path order: piece 6's riser must not draw before piece 5's flat is done
            rt = max(0.5, c.until() - 0.1)
            self.play(time_span(Create(self.qp[5], rate_func=linear), 0, rt * 0.6),
                      time_span(Create(self.qp[6], rate_func=linear), rt * 0.6, rt), run_time=rt)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        q_full = toggle_trace(X0, X1, RISES, Q_Y, AMP, color=GREEN, width=10)
        with self.say("c3.toggle.2") as c:
            self.play(VShowPassingFlash(q_full, time_width=0.5), run_time=2.0)
            c.wait_until("slower one")
            self.play(VShowPassingFlash(trace(clk_points(X0, X1, RISES, P), CLK_Y, AMP, YELLOW, 10),
                                        time_width=0.5),
                      VShowPassingFlash(q_full.copy(), time_width=0.5), run_time=2.0)

            # ---- count: four clock rises, two Q rises
            c.wait_until("count")
            self.play(*disappear(*self.vals), run_time=0.6)
            self.cnums = [T(str(i + 1), 30, YELLOW).move_to(_p(RISES[i], CLK_Y + AMP + 0.27)) for i in range(4)]
            self.play(*appear(*self.cnums, lag=0.35), run_time=min(2.2, c.until("only twice")))
            c.wait_until("only twice")
            self.qnums = [T(str(i + 1), 32, GREEN).move_to(_p(RISES[2 * i] + 0.3, Q_Y + AMP + 0.3)) for i in range(2)]
            self.play(*appear(*self.qnums, lag=0.5), run_time=1.2)

            # ---- flips: one up, one down
            c.wait_until("flips")
            self.play(VShowPassingFlash(edge_line(RISES[0], Q_Y, GREEN), time_width=1.0),
                      VShowPassingFlash(edge_line(RISES[1], Q_Y, GREEN), time_width=1.0),
                      VShowPassingFlash(self.guides[0].copy().set_stroke(YELLOW, 4), time_width=1.0),
                      VShowPassingFlash(self.guides[1].copy().set_stroke(YELLOW, 4), time_width=1.0),
                      run_time=1.5)
            self.up = T("up", 30, GREEN).move_to(_p(RISES[0] - 0.4, Q_Y + AMP + 0.3))
            self.down = T("down", 30, GREEN).move_to(_p(RISES[1] + 0.5, Q_Y + AMP + 0.3))
            for m in (self.up, self.down):
                set_backstroke(m, width=6)
            c.wait_until("one up")
            self.play(*appear(self.up, shift=0.15 * DOWN),
                      VShowPassingFlash(edge_line(RISES[0], Q_Y, GREEN), time_width=1.0), run_time=1.0)
            c.wait_until("one down")
            self.play(*appear(self.down, shift=0.15 * DOWN),
                      VShowPassingFlash(edge_line(RISES[1], Q_Y, GREEN), time_width=1.0), run_time=1.0)

            # ---- periods
            c.wait_until("period")
            self.play(*disappear(*self.cnums, *self.qnums), run_time=0.7)
            self.b1 = span_brace(_p(RISES[3], CLK_Y - AMP), _p(RISES[4], CLK_Y - AMP), color=GOLD, buff=0.12)
            self.b2 = span_brace(_p(RISES[0], Q_Y - AMP), _p(RISES[2], Q_Y - AMP), color=GOLD, buff=0.12)
            self.l1 = set_backstroke(T("1 clock period", 30, GOLD).next_to(self.b1, DOWN, buff=0.08), width=6)
            self.l2 = set_backstroke(T("2 clock periods", 30, GOLD).next_to(self.b2, DOWN, buff=0.08), width=6)
            self.play(GrowFromCenter(self.b1), GrowFromCenter(self.b2), run_time=1.0)
            self.play(*appear(self.l1, self.l2, lag=0.3, shift=None), run_time=min(1.2, c.until("half")))

            # ---- half the frequency
            c.wait_until("half")
            self.f1 = MathTex("f", font_size=44, color=GOLD).next_to(_p(X1, CLK_Y), RIGHT, buff=0.3)
            self.f2 = MathTex("f/2", font_size=44, color=GOLD).next_to(_p(X1, Q_Y), RIGHT, buff=0.3)
            self.cap = T("half the frequency", 44, GOLD).move_to(CAP_C)
            self.play(*appear(self.f1, self.f2, lag=0.4), run_time=1.2)
            self.play(*appear(self.cap), run_time=min(1.2, c.until()))

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        with self.say("c3.toggle.3", gap=2.0) as c:
            self.play(FlashAround(self.cap, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("divides")
            self.play(FlashAround(self.tab.rows[4], color=YELLOW, time_width=1.5),
                      FlashAround(self.f2, color=GOLD, time_width=1.5), run_time=1.5)

            # ---- chain: ghosts of the next two toggling traces
            c.wait_until("chain")
            self.play(*disappear(self.b1, self.b2, self.l1, self.l2, self.up, self.down), run_time=0.8)
            q4_edges = [RISES[1], RISES[3], RISES[5]]          # flips when the trace above falls
            g4 = toggle_trace(X0, X1, q4_edges, G4_Y, G_AMP, color=GOLD, width=3).set_stroke(opacity=0.5)
            g8 = toggle_trace(X0, X1, [RISES[3]], G8_Y, G_AMP, color=GOLD, width=3).set_stroke(opacity=0.5)
            f4 = MathTex("f/4", font_size=40, color=GOLD).next_to(_p(X1, G4_Y), RIGHT, buff=0.3).set_opacity(0.55)
            f8 = MathTex("f/8", font_size=40, color=GOLD).next_to(_p(X1, G8_Y), RIGHT, buff=0.3).set_opacity(0.55)
            self.play(Create(g4), *appear(f4, shift=None), rate_func=linear, run_time=1.5)
            self.play(Create(g8), *appear(f8, shift=None), rate_func=linear,
                      run_time=min(1.5, c.until("divider")))

            c.wait_until("divider")
            tag = T("Part 4: dividers", 32, FG)
            box = SurroundingRectangle(tag, color=DIM, buff=0.15, corner_radius=0.1).set_stroke(DIM, 2)
            VGroup(tag, box).move_to(CAP_C + 0.85 * DOWN)
            self.play(FadeIn(box), *appear(tag, shift=None), run_time=1.0)
            c.wait_until()

