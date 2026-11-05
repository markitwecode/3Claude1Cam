"""Chapter 4, scene 5: Lecture 9's traffic-light circuit beside the one-hot one; the logic moves from
the loop to the outputs; both go on the scoreboard. Clips c4.compare.1 – c4.compare.3.

Chapter-wide helper owned here (ch4 s7 imports it via load_scene("ch4_s5_compare")):
- l9_circuit() -> VGroup, p. 127's Lecture 9 traffic light at native size (about 13.6 x 7.0,
  x -7.0..6.3, y -2.75..4.3), drawn from ch2 s1's make_ff / xor_gate / and_gate. Flip-flops R, A, G
  (box centres y = 0 at x = -4.4, 0, 4.4; GREEN names T 56 above the boxes; Q-bar kept only on A).
  An XOR (pointing down, inputs labelled R, A) into D_R; Q-bar of A wired under its own box back
  into D_A (GREEN, crosses A's clock stub); an AND (inputs R, A) into D_G; one YELLOW CLK bus at
  y = -2.75; a lamp (dark disc, rim in the lamp colour) hanging straight off each Q at y = -2.05.
  Attributes: .ffs, .names, .gates [xor, and], .in_labels [[R, A], [R, A]], .risers, .da_wire,
  .lamps [R, A, G], .lamp_wires, .clk (VGroup(bus, stubs, dots, label)).
  .light(state) -> anims lighting the lamps of state 0-3 (red, red+amber, green, amber); None: off.
  Scale/shift the whole group freely.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch1_s1_hook")
S21 = load_scene("ch2_s1_hook")
S27 = load_scene("ch2_s7_tradeoff")
S4 = load_scene("ch4_s4_outputs")

LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)


def _p(x, y):
    return np.array([x, y, 0.0])


def _poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- l9_circuit (chapter-wide) ----------------------------------------------------------------------
L9_FF_X = (-4.4, 0.0, 4.4)
L9_GATE_OUT_Y = 1.7
L9_LAMP_Y = -2.05
L9_LAMP_R = 0.28
L9_BUS_Y = -2.75
L9_DA_Y = -1.55          # the Q-bar_A -> D_A wire under A's box
L9_DA_X = (1.05, -2.0)   # where it leaves Q-bar_A and where it rises to D_A


def l9_circuit():
    W, PIN = S21.BOX_W, S21.PIN_Y
    half = W / 2 + S21.WIRE                      # 1.6: stub ends
    ffs, names = [], []
    for i, x in enumerate(L9_FF_X):
        ff = S21.make_ff(_p(x, 0), size=46)
        ff.remove(ff.qb_w)
        if i != 1:
            ff.remove(ff.qb_l)
        ffs.append(ff)
        names.append(T("RAG"[i], 56, GREEN).move_to(_p(x, 1.85)))
    # next-state gates: XOR -> D_R, AND -> D_G (pointing down, ch1 s8 style)
    gates, stubs, in_labels, risers = [], [], [], []
    for x, kind in ((L9_FF_X[0], S21.xor_gate), (L9_FF_X[2], S21.and_gate)):
        g = kind().rotate(-PI / 2)
        g.shift(_p(x - 2.0, L9_GATE_OUT_Y) - g.out())
        gates.append(g)
        labs = [T("R", 52, GREEN), T("A", 52, GREEN)]
        for i in range(2):
            p = g.inp(i)
            stubs.append(Line(p, p + 0.4 * UP).set_stroke(GREEN, 4))
        labs[0].move_to(g.inp(1) + 0.55 * UP, aligned_edge=DOWN).shift(0.08 * LEFT)
        labs[1].move_to(g.inp(0) + 0.55 * UP, aligned_edge=DOWN).shift(0.08 * RIGHT)
        in_labels.append(labs)
        risers.append(_poly([(x - 2.0, L9_GATE_OUT_Y), (x - 2.0, PIN), (x - half, PIN)], BLUE))
    # D_A from Q-bar_A, under A's box
    x0, x1 = L9_DA_X
    da = _poly([(W / 2, -PIN), (x0, -PIN), (x0, L9_DA_Y), (x1, L9_DA_Y), (x1, PIN), (-half, PIN)], GREEN)
    # lamps straight off each Q
    lamps, lamp_wires = [], []
    for i, x in enumerate(L9_FF_X):
        lx = x + half
        lamp_wires.append(Line(_p(lx, PIN), _p(lx, L9_LAMP_Y + L9_LAMP_R)).set_stroke(GREEN, 4))
        lamps.append(Circle(radius=L9_LAMP_R).set_stroke(LAMP_COLS[i], 3).set_fill(S1.LAMP_OFF, 1)
                     .move_to(_p(lx, L9_LAMP_Y)))
    # clock
    hb = S21.BOX_H / 2 + S21.EN_WIRE
    bus = Line(_p(L9_FF_X[0] - 1.2, L9_BUS_Y), _p(L9_FF_X[2], L9_BUS_Y)).set_stroke(YELLOW, 5)
    ext = [Line(_p(x, -hb), _p(x, L9_BUS_Y)).set_stroke(YELLOW, 5) for x in L9_FF_X]
    dots = [Dot(_p(x, L9_BUS_Y), radius=0.08, color=YELLOW) for x in L9_FF_X[:2]]
    clk_l = T("CLK", 46, YELLOW).next_to(bus, LEFT, buff=0.15)
    clk = VGroup(bus, *ext, *dots, clk_l)
    C = VGroup(clk, *risers, da, *lamp_wires, *ffs, *names, *gates, *stubs,
               *[l for pair in in_labels for l in pair], *lamps)
    C.ffs, C.names, C.gates, C.in_labels, C.risers = ffs, names, gates, in_labels, risers
    C.da_wire, C.lamps, C.lamp_wires, C.clk = da, lamps, lamp_wires, clk

    def light(state):
        on = (0, 0, 0) if state is None else S1.STATE_LAMPS[state]
        return [lamps[k].animate.set_fill(LAMP_COLS[k] if on[k] else S1.LAMP_OFF, 1) for k in range(3)]

    C.light = light
    return C


# ---- this scene -------------------------------------------------------------------------------------
L_X, R_X = -3.6, 3.6
HEAD_Y = 3.5
CIRC_Y = -0.45
CODES = ["100", "110", "001", "010"]


def band(x0, x1, y0, y1, color):
    r = RoundedRectangle(corner_radius=0.12, width=x1 - x0, height=y1 - y0)
    r.move_to(_p((x0 + x1) / 2, (y0 + y1) / 2))
    return r.set_stroke(color, 2, opacity=0.7).set_fill(color, 0.13).set_z_index(-2)


def placed(circ, bands, width, center):
    """Scale/move circ together with bands drawn in its native coordinates."""
    g = VGroup(circ, *bands)
    k = width / circ.width
    g.scale(k)
    g.shift(center - circ.get_center())
    return circ, bands


def eq(parts):
    m = MathTex(*parts, font_size=32)
    m[0].set_color(BLUE)
    return m


def gate_glow(g, color):
    return [s.animate.set_stroke(color) for s in g.strokes()]


def cell(sb, r, col, text):
    t = T(text, S27.SB_SIZE, FG, t2c={"2": GOLD, "3": GOLD, "4": GOLD, "0": GOLD})
    a = sb.anchors[r][col].get_center()
    return t.move_to(a, aligned_edge=LEFT) if col == 0 else t.move_to(a)


def xor_and_cell(sb, r):
    parts = VGroup(T("2 (", S27.SB_SIZE, FG, t2c={"2": GOLD}), MathTex(r"\oplus", font_size=40),
                   T(", AND)", S27.SB_SIZE, FG))
    parts.arrange(RIGHT, buff=0.06)
    parts[1].set_y(parts[0][1].get_y())
    parts[2].align_to(parts[0], DOWN)
    return parts.move_to(sb.anchors[r][2].get_center())


class Compare(NarratedScene):
    def construct(self):
        # left panel
        L = l9_circuit()
        top = L.get_top()[1]
        lb = [band(-7.25, 6.55, -1.66, top + 0.15, TEAL), band(-7.25, 6.55, -2.42, -1.72, GOLD)]
        self.L, self.Lbands = placed(L, lb, 6.3, _p(L_X, CIRC_Y))
        # right panel
        Rc = S4.onehot_circuit()
        rb = [band(-6.15, 5.75, -0.3, 3.15, TEAL), band(-6.15, 5.75, -2.95, -0.45, GOLD)]
        self.Rc, self.Rbands = placed(Rc, rb, 6.1, _p(R_X, CIRC_Y))
        self.hL = T("Lecture 9", 40, FG).move_to(_p(L_X, HEAD_Y))
        self.hR = T("one-hot", 40, FG).move_to(_p(R_X, HEAD_Y))
        # codes and equations above the left circuit
        cap = T("R A G", 28, DIM)
        self.codes = [Mono(s, 32, GREEN) for s in CODES]
        arrows = [MathTex(r"\to", font_size=30, color=DIM) for _ in range(3)]
        row = VGroup(cap, self.codes[0], arrows[0], self.codes[1], arrows[1], self.codes[2], arrows[2],
                     self.codes[3]).arrange(RIGHT, buff=0.16)
        row.move_to(_p(L_X, 2.7))
        self.code_row = row
        self.eqs = [eq([r"D_R", "=", "R", r"\oplus", "A"]), eq([r"D_A", "=", r"\bar{A}"]),
                    eq([r"D_G", "=", "R", r"\cdot", "A"])]
        VGroup(*self.eqs).arrange(RIGHT, buff=0.45).move_to(_p(L_X, 1.85))
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(2.3)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------- c4.compare.1
    def clip1(self):
        L, Rc = self.L, self.Rc
        veil = Rectangle(width=6.9, height=7.6).move_to(_p(R_X, 0)).set_stroke(width=0)
        veil.set_fill(BG, 0.75).set_z_index(10)
        self.veil = veil
        xor, andg = L.gates
        with self.say("c4.compare.1") as c:
            self.add(veil)
            self.play(*appear(self.hL, self.hR, Rc), run_time=1.2)
            self.play(FadeIn(L, lag_ratio=0.0), run_time=min(1.5, c.until("part one's codes")))
            c.wait_until("part one's codes")
            self.play(*appear(*self.code_row, lag=0.12, shift=None),
                      run_time=min(1.5, c.until("three flip-flops")))
            c.wait_until("one per lamp")
            self.play(*[FlashAround(ff.box, time_width=1.5) for ff in L.ffs],
                      *[FlashAround(l, color=LAMP_COLS[k], time_width=1.5) for k, l in enumerate(L.lamps)],
                      run_time=min(1.5, c.until("xor")))
            # {xor}
            c.wait_until("xor")
            self.play(*gate_glow(xor, YELLOW), FlashAround(xor, run_time=1.5, time_width=1.5),
                      *appear(self.eqs[0]), run_time=1.5)
            self.play(*recolor(self.eqs[0][3], YELLOW), run_time=0.8)
            c.wait_until("red and amber outputs")
            self.play(*flash(L.in_labels[0]), run_time=1.2)
            # {toggle}
            c.wait_until("toggle")
            path = L.da_wire.copy().set_stroke(YELLOW, 8)
            self.play(*gate_glow(xor, BLUE), *recolor(self.eqs[0][3], FG),
                      L.da_wire.animate.set_stroke(YELLOW), VShowPassingFlash(path, time_width=0.6),
                      *appear(self.eqs[1]), run_time=1.6)
            c.wait_until("flips on every edge")
            mids = [code[1] for code in self.codes]
            self.play(*recolor(mids, YELLOW), *[FlashAround(m, time_width=1.5) for m in mids],
                      run_time=1.5)
            # {and}
            c.wait_until("and")
            self.play(*recolor(mids, GREEN), L.da_wire.animate.set_stroke(GREEN),
                      *gate_glow(andg, YELLOW), FlashAround(andg, time_width=1.5),
                      *appear(self.eqs[2]), run_time=1.5)
            c.wait_until("always follows")
            box = token_box(self.codes[1], self.code_row)
            self.box = box
            self.play(FadeIn(box), *recolor(self.codes[1], YELLOW), *L.light(1), run_time=1.0)
            c.wait_until("both of them lit")
            self.play(Transform(box, token_box(self.codes[2], self.code_row)), *recolor(self.codes[1], GREEN),
                      *recolor(self.codes[2], YELLOW), *L.light(2), run_time=1.0)
            # {noout}
            c.wait_until("noout")
            tag = T("no output logic", 32, GOLD).move_to(_p(L_X, -2.75))
            self.tag = tag
            self.play(FadeOut(box), *recolor(self.codes[2], GREEN), *L.light(None), *gate_glow(andg, BLUE), *appear(tag),
                      *[FlashAround(l, color=GOLD, time_width=1.5) for l in L.lamps], run_time=1.5)

    # ------------------------------------------------------------------------------- c4.compare.2
    def clip2(self):
        L, Rc = self.L, self.Rc
        with self.say("c4.compare.2") as c:
            self.play(FadeOut(self.veil), run_time=1.2)
            self.remove(self.veil)
            c.wait_until("loop")
            self.play(*[FadeIn(b) for b in self.Lbands], run_time=1.2)
            c.wait_until("two gates between")
            self.play(*[FlashAround(g, time_width=1.5) for g in L.gates], *[gate_glow(g, YELLOW)[0] for g in L.gates],
                      run_time=1.4)
            c.wait_until("one-hot needs none")
            self.play(FadeIn(self.Rbands[0]), *[gate_glow(g, BLUE)[0] for g in L.gates], run_time=1.2)
            c.wait_until("two gates after them")
            self.play(FadeIn(self.Rbands[1]), *[FlashAround(g, time_width=1.5) for g in Rc.gates],
                      *[s.animate.set_stroke(YELLOW) for g in Rc.gates for s in g.strokes()], run_time=1.4)
            # {moved}
            c.wait_until("moved")
            a0 = self.Lbands[0].get_corner(DR) + _p(-0.35, 0.55)
            a1 = self.Rbands[1].get_corner(UL) + _p(0.45, -0.55)
            arrow = CurvedArrow(a0, a1, angle=-PI / 3, color=YELLOW, stroke_width=4, tip_length=0.2)
            icon = S21.and_gate(color=YELLOW).rotate(-PI / 2).scale(0.32).move_to(a0)
            self.arrow, self.icon = arrow, icon
            self.play(*[s.animate.set_stroke(BLUE) for g in Rc.gates for s in g.strokes()],
                      GrowFromCenter(icon), run_time=0.8)
            self.play(Create(arrow), MoveAlongPath(icon, ArcBetweenPoints(a0, a1, angle=-PI / 3)),
                      run_time=min(2.0, c.until("same")))
            # {same}
            c.wait_until("same")
            line = T("same machine, same lamps, different state assignment", 36, FG,
                     t2c={"different state assignment": YELLOW}).move_to(_p(0, -3.45))
            self.line = line
            self.play(*appear(line), run_time=1.2)

    # ------------------------------------------------------------------------------- c4.compare.3
    def clip3(self):
        L, Rc = self.L, self.Rc
        sb = S27.scoreboard([("binary", "3", "3", "none"), ("sliding", "3", "1", "none")], n_rows=6)
        ring = VGroup(*S27.ring_cells(sb))
        sb.rows.append(ring)
        sb.add(ring)
        sb.shift(_p(-1.4, 0.35))
        with self.say("c4.compare.3") as c:
            gone = [*self.code_row, *self.eqs, *self.Lbands, *self.Rbands, self.arrow, self.icon, self.tag, self.hL, self.hR]
            for m in (L, Rc):
                m.generate_target()
            L.target.scale_to_fit_height(1.55).move_to(_p(-2.6, 2.7))
            Rc.target.scale_to_fit_height(1.55).move_to(_p(4.7, 2.7))
            hl = T("Lecture 9", 32, FG).next_to(L.target, LEFT, buff=0.35)
            hr = T("one-hot", 32, FG).next_to(Rc.target, LEFT, buff=0.35)
            self.play(*during(disappear(*gone), 0, 0.45),
                      *during([MoveToTarget(L), MoveToTarget(Rc)], 0.3, 1.0),
                      *during(appear(hl, hr, shift=None), 0.7, 1.0),
                      run_time=1.6)
            self.play(FadeIn(sb, shift=0.4 * UP), run_time=1.0)  # early: the board slides in whole
            # {row9}
            c.wait_until("row9")
            sub = T("traffic light", 28, DIM, slant=ITALIC).move_to(sb.anchors[3][0].get_center(), aligned_edge=LEFT)
            r9 = [cell(sb, 4, 0, "Lecture 9"), cell(sb, 4, 1, "3"), xor_and_cell(sb, 4), cell(sb, 4, 3, "none")]
            self.play(*appear(sub, *r9, lag=0.3), run_time=2.0)
            # {rowhot}
            c.wait_until("rowhot")
            rh = [cell(sb, 5, 0, "one-hot"), cell(sb, 5, 1, "4"), cell(sb, 5, 2, "0"), cell(sb, 5, 3, "2 OR")]
            self.play(*appear(*rh, lag=0.3), run_time=2.0)
            # {depends}
            c.wait_until("depends")
            card = S27.quote_card("best depends on\nwhat you optimise", 30).move_to(_p(4.9, -0.9))
            self.play(*appear(card), run_time=1.2)
            c.wait_until()
