"""Chapter 2, scene 1: title card; last time's binary divide-by-5 circuit and scoreboard; the same five
states, new codes to come; the lecturer's "bit of fun"; can the logic vanish, and at what price.
Clips c2.hook.1 – c2.hook.2.

Chapter-wide helpers owned here (s2, s4, s5, s7, s8 copy them verbatim):
- scoreboard(rows, n_rows=3) / sb_cell(sb, r, col, text, color): the four-column table. Header
  "assignment | flip-flops | next-state gates | output logic" (T 28, DIM, two-line headers), a DIM
  rule under it, n_rows row slots (sb.anchors[r][col], invisible points that move/scale with it).
  Names FG, numbers GOLD, "none" FG. Native size 7.3 x 2.6 (three rows). sb.rows[r] = row VGroup.
- five_ring(codes, radius=1.55): five BLUE nodes clockwise from 12 o'clock, state number inside
  (T 34 FG), the GREEN code (Mono 28) just outside each node, radially. ring.nodes/.circles/
  .nums/.codes/.arrows (arrows[i] i -> i+1, arrows[4] the wrap), ring.hub (centre).
  ring.code_at(i, text) places a new code Mono for node i where ring.codes[i] sits.
- binary_circuit(): ch1 s8's finished circuit, L6 make_ff/and_gate/xor_gate (copied). Native
  13 x 6.4; .ffs, .gates [AND->D_a, XOR->D_b, AND->D_c], .gate_parts (gates, input stubs, labels).

Layout: clip 1 circuit scale 0.62 centred (0, 1.35), scoreboard below (top -0.95). From {same}:
circuit width 5.9, top-left (left -6.6, top 3.6); scoreboard width 6.0, top-right (right 6.6,
top 3.6); ring centred (0, -1.3). Quote cards at (+-5.0, -1.3).
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
from lib.titles import title_card  # noqa: E402


def _p(x, y):
    return np.array([x, y, 0.0])


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- L6 ch6_s6_circuit's make_ff (D flip-flop), copied -------------------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def bar_label(ch, size=36, color=GREEN):
    """A letter with an overbar (NOT), e.g. a-bar."""
    q = T(ch, size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(max(q.width * 1.1, 0.2))
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, bubble=False, d_text="D", size=36):
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
    d_l = T(d_text, size, BLUE).move_to([-BOX_W / 2 + 0.3, PIN_Y, 0])
    q_l = T("Q", size, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar(size).move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(d_w, q_w, qb_w, clk_w, box, tri, d_l, q_l, qb_l)
    if bub is not None:
        g.add(bub)
    g.box, g.tri, g.bub = box, tri, bub
    g.d_l, g.q_l, g.qb_l, g.d_w, g.q_w, g.qb_w, g.clk_w = d_l, q_l, qb_l, d_w, q_w, qb_w, clk_w
    g.shift(center)
    return g


# ---- L6 ch6_s6_circuit's gates, copied -----------------------------------------------------------
GATE_COLOR = BLUE


class Gate(VGroup):
    def __init__(self, body, ins, out, extra=None, color=GATE_COLOR):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body)
        self.extra = extra
        if extra is not None:
            extra.set_stroke(color, 4).set_fill(opacity=0)
            self.add(extra)
        self.add(*self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()

    def strokes(self):
        return [m for m in (self.body, self.extra) if m is not None]


def _or_body():
    x0 = -0.7
    b = VMobject()
    b.start_new_path(_p(x0, 0.6))
    b.add_cubic_bezier_curve_to(_p(0.0, 0.6), _p(0.45, 0.35), _p(0.7, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.45, -0.35), _p(0.0, -0.6), _p(x0, -0.6))
    b.add_cubic_bezier_curve_to(_p(x0 + 0.25, -0.2), _p(x0 + 0.25, 0.2), _p(x0, 0.6))
    return b


def xor_gate(color=GATE_COLOR):
    arc = VMobject()
    arc.start_new_path(_p(-0.85, 0.6))
    arc.add_cubic_bezier_curve_to(_p(-0.6, 0.2), _p(-0.6, -0.2), _p(-0.85, -0.6))
    return Gate(_or_body(), [(-0.71, 0.3), (-0.71, -0.3)], (0.7, 0.0), extra=arc, color=color)


def _and_body():
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return b


def and_gate(color=GATE_COLOR):
    return Gate(_and_body(), [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


# ---- ch1 s8's finished binary circuit (drawn here from the parts above) --------------------------
FF_X = (-4.4, 0.0, 4.4)       # flip-flops a, b, c
GATE_OUT_Y = 1.7              # gates point down; their outputs sit here
CLK_Y = -BOX_H / 2 - EN_WIRE  # -2.3


def binary_circuit():
    """D_a = a-bar . c-bar, D_b = a XOR b, D_c = a . b; output from b. Native, about 13 x 6.4."""
    ffs = [make_ff(_p(x, 0), size=42) for x in FF_X]
    names = [T(n, 48, GREEN).move_to(_p(x - 0.5, -1.8)) for n, x in zip("abc", FF_X)]
    kinds = [and_gate, xor_gate, and_gate]
    ins = [[bar_label("a", 46), bar_label("c", 46)], [T("a", 46, GREEN), T("b", 46, GREEN)],
           [T("a", 46, GREEN), T("b", 46, GREEN)]]
    gates, stubs, labels, risers = [], [], [], []
    for x, kind, lab in zip(FF_X, kinds, ins):
        g = kind().rotate(-PI / 2)
        g.shift(_p(x - 2.0, GATE_OUT_Y) - g.out())
        gates.append(g)
        for i in range(2):
            p = g.inp(i)
            stubs.append(Line(p, p + 0.4 * UP).set_stroke(GREEN, 4))
        # rotated -90 deg: inp(0) is on the right, inp(1) on the left
        lab[0].move_to(g.inp(1) + 0.7 * UP, aligned_edge=DOWN).shift(0.08 * LEFT)
        lab[1].move_to(g.inp(0) + 0.7 * UP, aligned_edge=DOWN).shift(0.08 * RIGHT)
        labels.extend(lab)
        risers.append(poly([(x - 2.0, GATE_OUT_Y), (x - 2.0, PIN_Y), (x - BOX_W / 2 - WIRE, PIN_Y)], BLUE))
    clk = Line(_p(FF_X[0] - 1.6, CLK_Y), _p(FF_X[2], CLK_Y)).set_stroke(YELLOW, 5)
    clk_l = T("CLK", 44, YELLOW).next_to(clk, LEFT, buff=0.15)
    dots = [Dot(_p(x, CLK_Y), radius=0.08, color=YELLOW) for x in FF_X[:2]]
    qb_end = _p(FF_X[1] + BOX_W / 2 + WIRE, PIN_Y)
    out_arrow = Arrow(qb_end, qb_end + 1.0 * UP, buff=0, color=GREEN, stroke_width=4,
                      tip_length=0.2, max_tip_length_to_length_ratio=0.3)
    out_dot = Dot(qb_end, radius=0.08, color=GREEN)
    out_l = T("out", 44, GREEN).next_to(out_arrow.get_end(), LEFT, buff=0.12).shift(0.12 * DOWN)
    gate_parts = VGroup(*gates, *stubs, *labels)
    circ = VGroup(clk, *dots, *risers, *ffs, *names, gate_parts, out_arrow, out_dot, out_l, clk_l)
    circ.ffs, circ.gates, circ.gate_parts, circ.names = ffs, gates, gate_parts, names
    circ.gate_center = VectorizedPoint(_p(FF_X[1] - 2.0, GATE_OUT_Y + 0.75))
    circ.add(circ.gate_center)
    return circ


# ---- the chapter's scoreboard --------------------------------------------------------------------
SB_SIZE = 28
SB_HEAD = ["assignment", "flip-\nflops", "next-state\ngates", "output\nlogic"]
SB_COL_X = (-2.65, -1.0, 0.6, 2.3)     # column centres (col 0 is left-aligned at its left edge)
SB_COL0_LEFT = -3.55
SB_HEAD_Y = 0.95
SB_RULE_Y = 0.45
SB_ROW_Y0, SB_ROW_PITCH = 0.0, 0.6


def scoreboard(rows, n_rows=3):
    """rows: list of (name, flip-flops, gates, output) strings. Room for n_rows rows."""
    head = VGroup()
    for i, (h, x) in enumerate(zip(SB_HEAD, SB_COL_X)):
        t = T(h, SB_SIZE, DIM, line_spacing=0.8)
        if i == 0:
            t.move_to(_p(0, SB_HEAD_Y)).align_to(_p(SB_COL0_LEFT, 0), LEFT)
        else:
            t.move_to(_p(x, SB_HEAD_Y))
        head.add(t)
    rule = Line(_p(SB_COL0_LEFT, SB_RULE_Y), _p(SB_COL_X[3] + 0.6, SB_RULE_Y)).set_stroke(DIM, 2)
    anchors = []
    for r in range(n_rows):
        y = SB_ROW_Y0 - r * SB_ROW_PITCH
        anchors.append([VectorizedPoint(_p(SB_COL0_LEFT, y))] + [VectorizedPoint(_p(x, y)) for x in SB_COL_X[1:]])
    sb = VGroup(head, rule, *[a for row in anchors for a in row])
    sb.head, sb.rule, sb.anchors, sb.rows = head, rule, anchors, []
    sb.unit = rule.get_length()   # native rule length: lets sb_cell scale text with the board
    for r, row in enumerate(rows):
        sb.rows.append(VGroup(*[sb_cell(sb, r, c, s) for c, s in enumerate(row)]))
        sb.add(sb.rows[-1])
    return sb


def sb_cell(sb, r, col, text, color=None):
    """A cell's text for row slot r, column col, sized and placed for the board as it is now."""
    if color is None:
        color = FG if (col == 0 or not text.strip().isdigit()) else GOLD
    t = T(text, SB_SIZE, color).scale(sb.rule.get_length() / sb.unit)
    a = sb.anchors[r][col].get_center()
    if col == 0:
        t.move_to(a, aligned_edge=LEFT)
    else:
        t.move_to(a)
    return t


# ---- the five-state ring (L6 state_ring style) ---------------------------------------------------
NODE_R = 0.5


def five_ring(codes, radius=1.55):
    """Five states clockwise from 12 o'clock; codes (strings) GREEN just outside each node."""
    hub = Dot(ORIGIN, radius=0.01).set_opacity(0)

    def dirn(i):
        a = PI / 2 - TAU * i / 5
        return np.array([np.cos(a), np.sin(a), 0.0])

    nodes, circles, nums, arrows = [], [], [], []
    for i in range(5):
        p = radius * dirn(i)
        c = Circle(radius=NODE_R, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        n = T(str(i), 34, FG).move_to(p)
        circles.append(c)
        nums.append(n)
        nodes.append(VGroup(c, n))
    for i in range(5):
        p, q = radius * dirn(i), radius * dirn((i + 1) % 5)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + (NODE_R + 0.04) * u, q - (NODE_R + 0.04) * u, buff=0, color=FG,
                            stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.4))

    def code_pos(i, mob):
        d = dirn(i)
        half = abs(d[0]) * mob.width / 2 + abs(d[1]) * mob.height / 2
        return hub.get_center() + (radius + NODE_R + 0.14 + half) * d

    def code_at(i, text, color=GREEN, size=28):
        m = Mono(text, size=size, color=color)
        return m.move_to(code_pos(i, m))

    codes_m = [code_at(i, s) for i, s in enumerate(codes)]
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*codes_m), hub)
    ring.nodes, ring.circles, ring.nums, ring.arrows, ring.codes, ring.hub = (
        nodes, circles, nums, arrows, codes_m, hub)
    ring.code_at = code_at
    return ring


BINARY = ["000", "001", "010", "011", "100"]


def quote_card(text, size=30):
    t = T(text, size, FG, slant=ITALIC, line_spacing=0.9)
    box = RoundedRectangle(corner_radius=0.15, width=t.width + 0.6, height=t.height + 0.5)
    box.set_stroke(DIM, 2).set_fill(BG, 1)
    return VGroup(box, t.move_to(box))


class Hook(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------------- c2.hook.1
        with self.say("c2.hook.1") as c:
            card = title_card("Part 2 · More flip-flops, less logic")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.3)  # early: title card read whole
            circ = binary_circuit().scale(0.72).move_to(_p(0, 1.2))
            sb = scoreboard([("binary", "3", "3", "none")])
            sb.move_to(_p(0, 0)).align_to(_p(0, -1.35), UP)
            self.wait(max(0.0, c.until("last") - 0.6))
            sweep_clear(self, FadeIn(circ), run_time=1.6)
            c.wait_until("next-state logic")
            self.play(*appear(sb.head, sb.rule, sb.rows[0], lag=0.3), run_time=1.2)  # early: scoreboard read whole
            self.add(sb)
            c.wait_until("three gates")
            self.play(FlashAround(sb.rows[0][2], run_time=1.2, time_width=1.5, color=GOLD))

            and_a, xor_b, and_c = circ.gates
            c.wait_until("two and")
            self.play(*[m.animate.set_stroke(YELLOW) for g in (and_a, and_c) for m in g.strokes()],
                      *flash([and_a, and_c]), run_time=1.0)
            c.wait_until("exclusive-or")
            self.play(*[m.animate.set_stroke(BLUE) for g in (and_a, and_c) for m in g.strokes()],
                      *[m.animate.set_stroke(YELLOW) for m in xor_b.strokes()],
                      *flash([xor_b]), run_time=1.0)
            self.play(*[m.animate.set_stroke(BLUE) for m in xor_b.strokes()],
                      run_time=min(0.8, c.until(None)))

        # ---------------------------------------------------------------- c2.hook.2
        with self.say("c2.hook.2") as c:
            ring = five_ring(BINARY).move_to(_p(0, -1.3))
            circ.generate_target()
            circ.target.scale_to_fit_width(5.7).align_to(_p(-6.6, 0), LEFT).align_to(_p(0, 3.6), UP)
            sb.generate_target()
            sb.target.align_to(_p(6.6, 0), RIGHT).align_to(_p(0, 3.6), UP)
            self.play(*during([MoveToTarget(circ)], 0, 0.5), *during([MoveToTarget(sb)], 0.4, 0.85),
                      time_span(FadeIn(VGroup(ring[0], ring[1], ring[3])), 1.3, 2.0), run_time=2.0)
            self.play(*appear(*ring.codes, lag=0.2), run_time=1.2)
            self.add(ring)

            q1 = quote_card("“just a bit\nof fun”").move_to(_p(-5.0, -1.3))
            q2 = quote_card("“you wouldn’t\nnecessarily do it\nin anger”").move_to(_p(5.0, -1.3))
            c.wait_until("just a bit")
            self.play(*appear(q1), run_time=1.0)
            c.wait_until("necessarily")
            self.play(*appear(q2), run_time=1.0)  # early: the lecturer's words, paraphrased in the voice

            c.wait_until("freedom")
            self.play(*flash(ring.codes, color=GREEN), run_time=1.5)

            c.wait_until("question")
            qs = [ring.code_at(i, "???", color=YELLOW) for i in range(5)]
            self.play(*[a for i in range(5) for a in swap(ring.codes[i], qs[i], shift=None)],
                      *set_alpha([q1, q2], 0.4), run_time=1.4)
            qmarks = [set_backstroke(T("?", 54, YELLOW).move_to(g.body), width=8) for g in circ.gates]
            self.play(*set_alpha([circ.gate_parts], DIMMED), *appear(*qmarks, shift=None, lag=0.15),
                      run_time=1.2)

            c.wait_until("pay")
            pay = sb_cell(sb, 1, 1, "?", GOLD).scale(1.4)
            self.play(*appear(pay), FlashAround(sb.head[1], color=GOLD, run_time=1.2), run_time=1.2)
            c.wait_until(None)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
