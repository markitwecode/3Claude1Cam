"""Chapter 5, scene 7: the D0 map (p. 141), then the finished synchroniser circuit and its score.
Clips c5.finish.1 – c5.finish.5.

Shared helpers (load_scene("ch5_s7_d0")), for s8 and ch6:
- `sync_circuit()`: the finished two-flip-flop synchroniser, placed for the full frame (about
  12 x 6.6, x -5.9..6.1, y -2.95..3.65). Left: BLUE inputs e and r, e branching through one
  inverter to ē. Middle: D1's block (AND(s1, ē), AND(s1, r), AND3(s0, e, r) into an OR3) above
  D0's block (AND(s0, ē), AND3(s̄1, s̄0, r) into an OR2); every gate input is a short labelled
  stub. Right: flip-flops FF1 (Q = s1, Q̄ = s̄1) above FF0 (Q = s0, Q̄ = s̄0), one YELLOW CLK line
  entering bottom-left, under FF0 and up the right side to FF1; output s (GREEN) branching off s1.
  Attrs .inputs (VGroup) .inv .ffs [ff1, ff0] .qlabels [s1, s̄1, s0, s̄0] .clk (path, stubs, dot,
  label) .d1 / .d0 (VGroup each, with .ands .or_ .stubs .wires .dlab) .ands (all 5) .ors (both)
  .out (VGroup(dot, wire, label)).
- `sync_board(with_row=True)`: ch4 s5's scoreboard (ch2's scoreboard() at native scale, rows binary,
  sliding, ring, "traffic light" sub-heading, Lecture 9, one-hot) plus the "synchroniser"
  sub-heading (slot 6) and the row "sequential | 2 | 7 | none" (slot 7, numbers GOLD), placed
  at x -6.5..-0.05, y 3.69 (header top) .. -1.9 (slot 7); slot 8 (y -2.5) is free for ch6's
  one-hot row: `sb.anchors[8]`, cells via `sb_cell(sb, r, col, text)` here. Attrs as ch2's
  scoreboard plus .sync_sub, .sync_row (in the group only if with_row).
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

S6 = load_scene("ch5_s6_d1")
S5 = load_scene("ch5_s5_table")
S21 = load_scene("ch2_s1_hook")
S27 = load_scene("ch2_s7_tradeoff")
S45 = load_scene("ch4_s5_compare")


def _p(x, y):
    return np.array([x, y, 0.0])


def _wire(pts, color=BLUE, width=4):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# =============================================================================================
# Shared: sync_circuit()
# =============================================================================================
SIG = {"s1": ("s_1", GREEN), "s0": ("s_0", GREEN), "nb1": (r"\overline{s}_1", GREEN),
       "nb0": (r"\overline{s}_0", GREEN), "e": ("e", BLUE), "eb": (r"\overline{e}", BLUE), "r": ("r", BLUE)}
AND_X, OR_X, FF_X = -0.6, 1.9, 4.6
BEND_X = 0.6
D1_ANDS = ((3.0, ("s1", "eb")), (1.65, ("s1", "r")), (0.3, ("s0", "e", "r")))
D0_ANDS = ((-1.25, ("s0", "eb")), (-2.6, ("nb1", "nb0", "r")))
OR1_Y, OR0_Y = 1.65, -1.925
FF1_Y, FF0_Y = OR1_Y - S21.PIN_Y, OR0_Y - S21.PIN_Y
BUS_X, BUS_Y, CLK_X0 = 8.0, -4.15, 3.2
CIRC_K = 0.82
CIRC_CENTER = _p(0.1, 0.35)


def sig(key, size=40):
    tex, col = SIG[key]
    return MathTex(tex, font_size=size, color=col)


def and_n(n):
    ins = [(-0.7, 0.3), (-0.7, -0.3)] if n == 2 else [(-0.7, 0.42), (-0.7, 0.0), (-0.7, -0.42)]
    return S21.Gate(S21._and_body(), ins, (0.6, 0.0))


def or_n(n):
    ins = [(-0.56, 0.3), (-0.56, -0.3)] if n == 2 else [(-0.6, 0.35), (-0.51, 0.0), (-0.6, -0.35)]
    return S21.Gate(S21._or_body(), ins, (0.7, 0.0))


def inverter():
    tri = Polygon(_p(-0.4, 0.35), _p(-0.4, -0.35), _p(0.3, 0.0))
    bub = Circle(radius=0.08).move_to(_p(0.38, 0))
    return S21.Gate(tri, [(-0.4, 0.0)], (0.46, 0.0), extra=bub)


def _put_label(lab, point, side):
    """Label at a wire end; barred labels sit so their letter, not the bar, is on the wire."""
    lab.next_to(point, side, buff=0.1)
    lab.set_y(point[1] + (0.07 if lab.height > 0.42 else 0.0))
    return lab


def _block(ands_spec, or_y, ff_y, dname):
    ands, stubs, wires = [], [], []
    for y, keys in ands_spec:
        g = and_n(len(keys)).shift(_p(AND_X, y))
        ands.append(g)
        for i, k in enumerate(keys):
            p = g.inp(i)
            ln = Line(p + 0.6 * LEFT, p).set_stroke(SIG[k][1], 4)
            stubs.append(VGroup(ln, _put_label(sig(k, 36), p + 0.6 * LEFT, LEFT)))
    org = or_n(len(ands)).shift(_p(OR_X, or_y))
    for i, g in enumerate(ands):
        a, b = g.out(), org.inp(i)
        if abs(a[1] - b[1]) < 1e-3:
            wires.append(_wire([(a[0], a[1]), (b[0], b[1])]))
        else:
            wires.append(_wire([(a[0], a[1]), (BEND_X, a[1]), (BEND_X, b[1]), (b[0], b[1])]))
    o = org.out()
    d_in = FF_X - S21.BOX_W / 2 - S21.WIRE
    wires.append(_wire([(o[0], o[1]), (d_in + 0.05, o[1])]))
    dlab = MathTex(dname, font_size=36, color=BLUE).move_to(_p((o[0] + d_in) / 2 + 0.2, o[1] + 0.32))
    B = VGroup(*wires, *ands, org, *stubs, dlab)
    B.ands, B.or_, B.stubs, B.wires, B.dlab = ands, org, stubs, wires, dlab
    return B


def sync_circuit():
    # inputs
    e_l, r_l = sig("e"), sig("r")
    e_l.move_to(_p(-6.4, 0.75))
    r_l.move_to(_p(-6.4, -1.65))
    inv = inverter().shift(_p(-4.6, -0.45))
    ew = _wire([(-6.15, 0.75), (-3.55, 0.75)], BLUE)
    edot = Dot(_p(-5.5, 0.75), radius=0.07, color=BLUE)
    ebr = _wire([(-5.5, 0.75), (-5.5, -0.45), (inv.inp(0)[0], -0.45)], BLUE)
    ebw = _wire([(inv.out()[0], -0.45), (-3.55, -0.45)], BLUE)
    eb_l = _put_label(sig("eb"), _p(-3.55, -0.45), RIGHT)
    rw = _wire([(-6.15, -1.65), (-3.55, -1.65)], BLUE)
    inputs = VGroup(ew, edot, ebr, ebw, rw, inv, e_l, r_l, eb_l)
    # flip-flops
    ffs, qlabels = [], []
    q_end = FF_X + S21.BOX_W / 2 + S21.WIRE
    for y, qk, qbk in ((FF1_Y, "s1", "nb1"), (FF0_Y, "s0", "nb0")):
        ff = S21.make_ff(_p(FF_X, y), size=36)
        ff.remove(ff.clk_w)
        ffs.append(ff)
        qlabels.append(_put_label(sig(qk), _p(q_end, y + S21.PIN_Y), RIGHT))
        qlabels.append(_put_label(sig(qbk), _p(q_end, y - S21.PIN_Y), RIGHT))
    # clock
    hb = S21.BOX_H / 2
    path = _wire([(CLK_X0, BUS_Y), (BUS_X, BUS_Y), (BUS_X, FF1_Y - hb - 0.4), (FF_X, FF1_Y - hb - 0.4),
                  (FF_X, FF1_Y - hb - 0.02)], YELLOW, 5)
    stub = Line(_p(FF_X, BUS_Y), _p(FF_X, FF0_Y - hb - 0.02)).set_stroke(YELLOW, 5)
    cdot = Dot(_p(FF_X, BUS_Y), radius=0.08, color=YELLOW)
    clk_l = T("CLK", 36, YELLOW).next_to(_p(CLK_X0, BUS_Y), LEFT, buff=0.15)
    clk = VGroup(path, stub, cdot, clk_l)
    # logic blocks
    d1 = _block(D1_ANDS, OR1_Y, FF1_Y, "D_1")
    d0 = _block(D0_ANDS, OR0_Y, FF0_Y, "D_0")
    # output s, straight from s1
    oy, ox = OR1_Y, FF_X + S21.BOX_W / 2 + 0.4
    odot = Dot(_p(ox, oy), radius=0.07, color=GREEN)
    ow = _wire([(ox, oy), (ox, oy + 1.2), (q_end + 0.2, oy + 1.2)], GREEN, 5)
    ol = MathTex("s", font_size=48, color=GREEN).next_to(_p(q_end + 0.2, oy + 1.2), RIGHT, buff=0.12)
    out = VGroup(ow, odot, ol)
    C = VGroup(clk, inputs, d1, d0, *ffs, *qlabels, out)
    C.scale(CIRC_K, about_point=ORIGIN)
    C.shift(CIRC_CENTER - C.get_center())
    C.inputs, C.inv, C.ffs, C.qlabels, C.clk, C.d1, C.d0, C.out = inputs, inv, ffs, qlabels, clk, d1, d0, out
    C.ands = d1.ands + d0.ands
    C.ors = [d1.or_, d0.or_]
    return C


# =============================================================================================
# Shared: sync_board()
# =============================================================================================
BOARD_SHIFT = _p(-2.95, 2.3)
SYNC_ROW = ("sequential", "2", "7", "none")


def sb_cell(sb, r, col, text):
    t = T(text, S27.SB_SIZE, FG, t2c={d: GOLD for d in "0123456789"} if col else None)
    a = sb.anchors[r][col].get_center()
    return t.move_to(a, aligned_edge=LEFT) if col == 0 else t.move_to(a)


def sync_board(with_row=True):
    sb = S27.scoreboard([("binary", "3", "3", "none"), ("sliding", "3", "1", "none")], n_rows=9)
    ring = VGroup(*S27.ring_cells(sb))
    sb.rows.append(ring)
    sb.add(ring)
    sub9 = T("traffic light", 28, DIM, slant=ITALIC).move_to(sb.anchors[3][0].get_center(), aligned_edge=LEFT)
    r9 = VGroup(S45.cell(sb, 4, 0, "Lecture 9"), S45.cell(sb, 4, 1, "3"), S45.xor_and_cell(sb, 4),
                S45.cell(sb, 4, 3, "none"))
    rh = VGroup(S45.cell(sb, 5, 0, "one-hot"), S45.cell(sb, 5, 1, "4"), S45.cell(sb, 5, 2, "0"),
                S45.cell(sb, 5, 3, "2 OR"))
    sb.add(sub9, r9, rh)
    sb.rows += [r9, rh]
    sub = T("synchroniser", 28, DIM, slant=ITALIC).move_to(sb.anchors[6][0].get_center(), aligned_edge=LEFT)
    row = VGroup(*[sb_cell(sb, 7, k, s) for k, s in enumerate(SYNC_ROW)])
    sb.sync_sub, sb.sync_row = sub, row
    sb.add(sub, row)
    sb.shift(BOARD_SHIFT)
    if not with_row:
        sb.remove(sub, row)
    else:
        sb.rows.append(row)
    return sb


# =============================================================================================
# The scene
# =============================================================================================
MAP_X = 2.9
MAP_C = _p(MAP_X, S6.MAP_Y)
TAB_SCALE = 0.68
CORNER_SCALE = 0.33
D0_TERMS = (r"s_0\cdot\overline{e}", r"\overline{s}_1\cdot\overline{s}_0\cdot r")
D0_COLORS = (PINK, PURPLE)
PINK_CELLS = [(1, 0), (1, 1), (2, 0), (2, 1)]
PURPLE_CELLS = [(0, 1), (0, 2)]
OTHER_CELLS = [(0, 1), (1, 1)]
EQ_Y = -2.7
GHOSTS = (([(0, 1), (0, 2), (1, 1), (1, 2)], [(1, 2)]),
          (None, [(3, 1), (3, 2)]),                      # wrap: row 00 with row 10
          ([(0, 0), (0, 1), (0, 2), (0, 3)], [(0, 0), (0, 3)]))


def dimmed_copy(mob, scale, center, op=0.4):
    t = mob.copy().scale(scale).move_to(center)
    for leaf in t.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_opacity(op)
        else:
            leaf.set_stroke(opacity=op, width=min(leaf.get_stroke_width(), 2.5))
    return t


class D0Map(NarratedScene):
    def construct(self):
        self.shot = S6.handover_shot()
        self.add(self.shot)
        self.m = S6.kmap4(None, center=MAP_C, title="For FF 0:")
        self.ent = {}
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(2.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def cell_box(self, mobs, color=YELLOW, buff=0.08):
        return S5.cell_box(mobs, color=color, buff=buff)

    def fill(self, cells, v="1"):
        out = []
        for r, k in cells:
            e = self.m.value(r, k, v)
            self.ent[(r, k)] = e
            out.append(e)
        return out

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        m = self.m
        t = self.t = S5.sync_table()
        t.scale(TAB_SCALE).align_to(_p(-6.55, 0), LEFT).align_to(_p(0, 1.3), UP)
        with self.say("c5.finish.1") as c:
            tgt = dimmed_copy(self.shot, CORNER_SCALE, ORIGIN)
            tgt.align_to(_p(-6.55, 0), LEFT).align_to(_p(0, 3.5), UP)
            self.play(Transform(self.shot, tgt), run_time=min(1.4, c.until("ess zero prime column")))
            self.play(*appear(t, m, shift=None, lag=0.2), run_time=1.2)  # early: table and map return whole
            c.wait_until("ess zero prime column")
            col = VGroup(t.heads[2][1], *[r[2][1] for r in t.rows])
            self.colbox = SurroundingRectangle(col, buff=0.08).set_stroke(BLUE, 3).set_fill(BLUE, 0.15).set_z_index(-1)
            self.d0lab = MathTex("D_0", "=", "s_0'", font_size=44, color=FG)
            self.d0lab[0].set_color(BLUE)
            self.d0lab.next_to(self.colbox, DOWN, buff=0.25)
            self.play(FadeIn(self.colbox), *appear(self.d0lab), run_time=min(1.2, c.until("hunt")))
            # {hunt}
            c.wait_until("hunt")
            box = self.box = self.cell_box([t.rows[1]])
            self.play(FadeIn(box), FlashAround(t.rows[1], run_time=1.2), run_time=min(1.2, c.until("ee is an ex")))
            c.wait_until("ee is an ex")
            xbox = self.cell_box([t.cell(1, 1, 0)], buff=0.1)
            xbox.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.35).set_z_index(-0.5)
            self.play(FadeIn(xbox), run_time=min(0.9, c.until("two cells")))
            c.wait_until("two cells")
            ones = self.fill([(0, 1), (0, 2)])
            self.play(*appear(*ones, shift=None, lag=0),
                      FlashAround(VGroup(m.sq(0, 1), m.sq(0, 2)), color=YELLOW, run_time=1.4, time_width=1.5),
                      run_time=min(1.4, c.until("sight")))
            # {sight}
            c.wait_until("sight")
            self.play(FadeOut(xbox), Transform(box, self.cell_box([t.rows[2]])), run_time=min(1.0, c.until("two more")))
            c.wait_until("two more")
            ones = self.fill([(1, 0), (1, 1)])
            self.play(*appear(*ones, shift=None, lag=0),
                      FlashAround(VGroup(m.sq(1, 0), m.sq(1, 1)), color=YELLOW, run_time=1.4, time_width=1.5),
                      run_time=min(1.4, c.until("xrow")))
            # {xrow}
            c.wait_until("xrow")
            self.play(Transform(box, self.cell_box([t.rows[8]])), run_time=min(0.9, c.until("don't cares")))
            c.wait_until("don't cares")
            xs = self.fill([(2, k) for k in range(4)], "X")
            self.play(*appear(*xs, lag=0.15, shift=None), run_time=min(1.2, c.until()))

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        m = self.m
        self.eq = eq = S6.term_eq("D_0", D0_TERMS, D0_COLORS, cx=MAP_X, y=EQ_Y, xs=(-0.9, 1.75))
        with self.say("c5.finish.2") as c:
            # {pink}
            self.play(FadeOut(self.box), FlashAround(VGroup(m.sq(1, 0), m.sq(1, 1)), color=PINK, run_time=1.2),
                      run_time=min(1.2, c.until("block of four")))
            c.wait_until("block of four")
            self.pink = S6.loop4(m, PINK_CELLS, PINK, 0.08)
            self.play(FadeIn(self.pink), run_time=min(1.5, c.until("that's ess zero")))
            c.wait_until("that's ess zero")
            self.play(*appear(eq.terms[0]), run_time=min(1.0, c.until("purple")))
            # {purple}
            c.wait_until("purple")
            self.purple = S6.loop4(m, PURPLE_CELLS, PURPLE, 0.08)
            self.play(FadeIn(self.purple), run_time=min(1.3, c.until("every way")))
            c.wait_until("every way")
            for i, (cells, zeros) in enumerate(GHOSTS):
                if cells is None:
                    gl = VGroup(S6.loop4(m, [(0, 1), (0, 2)], PURPLE, -0.06), S6.loop4(m, [(3, 1), (3, 2)], PURPLE, 0.06))
                else:
                    gl = VGroup(S6.loop4(m, cells, PURPLE, -0.06 if len(cells) == 4 and i == 2 else 0.16))
                ghost = VGroup(*[DashedVMobject(x, num_dashes=28).set_stroke(PURPLE, 4, opacity=0.8) for x in gl])
                reds = [m.value(r, k, "0").set_color(RED) for r, k in zeros]
                rt_in, rt_out = (1.1, 0.6) if i == 0 else (0.8, 0.45)
                self.play(FadeIn(ghost), *appear(*reds, shift=None, lag=0),
                          *[FlashAround(m.sq(r, k), color=RED, stroke_width=6, run_time=rt_in) for r, k in zeros],
                          run_time=rt_in)
                self.play(*disappear(ghost, *reds), run_time=rt_out)
            c.wait_until("its term")
            self.play(*appear(eq.terms[1]), run_time=min(1.0, c.until("result")))
            # {result}
            c.wait_until("result")
            self.play(*appear(eq.lhs, eq.plus[0], shift=None, lag=0.3), run_time=min(1.2, c.until()))
            self.play(FlashAround(eq, run_time=1.5, time_width=1.5), run_time=min(1.5, max(0.3, c.until())))

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        m = self.m
        with self.say("c5.finish.3", gap=1.2) as c:
            # {other}
            self.other = DashedVMobject(S6.loop4(m, OTHER_CELLS, DIM, 0.2), num_dashes=24).set_stroke(DIM, 4)
            self.play(*during(disappear(self.t, self.colbox, self.d0lab), 0, 0.5),
                      *during([FadeIn(self.other)], 0.4, 1.0),
                      run_time=min(1.6, c.until("below it")))
            c.wait_until("below it")
            tag = self.otag = MathTex(r"\overline{s}_1\cdot\overline{e}\cdot r", font_size=40, color=DIM)
            tag.move_to(_p(0, m.top - m.cell)).align_to(_p(-0.25, 0), RIGHT)
            self.play(*appear(tag), run_time=min(1.0, c.until("valid")))
            # {valid}
            c.wait_until("valid")
            vtag = T("also a group", 30, DIM).next_to(tag, DOWN, buff=0.3).align_to(tag, RIGHT)
            self.play(*appear(vtag), run_time=min(1.0, c.until("spare")))
            # {spare}
            c.wait_until("spare")
            e02 = self.ent[(0, 2)]
            self.play(e02.animate.set_color(PURPLE),
                      FlashAround(m.sq(0, 2), color=PURPLE, stroke_width=6, run_time=1.2),
                      run_time=min(1.2, c.until("adds nothing")))
            c.wait_until("adds nothing")
            self.play(FlashAround(m.sq(0, 1), color=PURPLE, stroke_width=6, run_time=1.2),
                      FlashAround(m.sq(1, 1), color=PINK, stroke_width=6, run_time=1.2), run_time=1.2)
            self.play(*disappear(self.other, tag, vtag), run_time=min(0.8, max(0.3, c.until("min"))))
            # {min}
            c.wait_until("min")
            mtag = self.mtag = T("two essential groups", 32, YELLOW).move_to(_p(MAP_X, -3.35))
            self.play(self.ent[(1, 0)].animate.set_color(PINK), *appear(mtag),
                      *[FlashAround(lp, color=col, run_time=1.4) for lp, col in ((self.pink, PINK), (self.purple, PURPLE))],
                      run_time=min(1.4, c.until()))

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        C = self.C = sync_circuit()
        with self.say("c5.finish.4") as c:
            # the map, its equation and the GOLD tag all leave together, then the inputs arrive
            self.play(*during([FadeOut(x) for x in list(self.mobjects)], 0, 0.5),
                      *during([FadeIn(C.inputs)], 0.5, 1.0), run_time=min(1.3, c.until("ffs")))
            # {ffs}
            c.wait_until("ffs")
            self.play(*appear(*C.ffs, lag=0.3, shift=None), *appear(*C.qlabels, shift=None, lag=0.1),
                      run_time=min(1.4, c.until("one clock")))
            c.wait_until("one clock")
            clk = C.clk
            self.play(Create(clk[0]), Create(clk[1]), *appear(clk[2], clk[3], shift=None),
                      run_time=min(1.6, c.until("logic1")))
            # {logic1}
            for blk, cue, orcue, nxt in ((C.d1, "logic1", "joined by an or gate", "logic0"),
                                         (C.d0, "logic0", "joined by a second", "out")):
                c.wait_until(cue)
                parts = [VGroup(g, *[s for s in blk.stubs if self._near(s, g)]) for g in blk.ands]
                self.play(*appear(*parts, lag=0.3, shift=None), run_time=min(1.6, c.until(orcue)))
                c.wait_until(orcue)
                self.play(*[Create(w) for w in blk.wires], *appear(blk.or_, blk.dlab, shift=None),
                          run_time=min(1.4, c.until(nxt)))
            # {out}
            c.wait_until("out")
            o = C.out
            self.play(FadeIn(o[1]), Create(o[0]), *appear(o[2], shift=None), run_time=min(1.3, c.until()))
            self.play(FlashAround(o[2], color=GREEN, run_time=1.2), run_time=min(1.2, max(0.3, c.until())))

    @staticmethod
    def _near(stub, g):
        return abs(stub[0].get_end()[0] - g.inp(0)[0]) < 0.05 and \
            min(abs(stub[0].get_end()[1] - g.inp(i)[1]) for i in range(len(g._ins))) < 0.02

    # ------------------------------------------------------------------ clip 5
    def clip5(self):
        C = self.C
        cy = C.get_bottom()[1] - 0.45
        n_and = T("5 AND", 32, GOLD).move_to(_p(C.ands[0].get_x(), cy))
        n_or = T("2 OR", 32, GOLD).move_to(_p(C.ors[0].get_x(), cy))
        n_all = T("= 7 gates", 32, GOLD).next_to(n_or, RIGHT, buff=0.5)
        n_inv = MathTex(r"+\,1\ \text{inverter}\ (\overline{e})", font_size=40, color=DIM)
        n_inv.move_to(_p(C.inv.get_x(), cy))
        with self.say("c5.finish.5") as c:
            c.wait_until("five and gates")
            self.play(*[s.animate.set_stroke(GOLD) for g in C.ands for s in g.strokes()], *appear(n_and),
                      run_time=min(1.2, c.until("two or gates")))
            c.wait_until("two or gates")
            self.play(*[s.animate.set_stroke(BLUE) for g in C.ands for s in g.strokes()],
                      *[s.animate.set_stroke(GOLD) for g in C.ors for s in g.strokes()], *appear(n_or),
                      run_time=min(1.2, c.until("seven in all")))
            c.wait_until("seven in all")
            self.play(*[s.animate.set_stroke(BLUE) for g in C.ors for s in g.strokes()], *appear(n_all),
                      run_time=min(1.0, c.until("plus an inverter")))
            c.wait_until("plus an inverter")
            self.play(*appear(n_inv), FlashAround(C.inv, color=DIM, run_time=1.2), run_time=min(1.2, c.until("free")))
            # {free}
            c.wait_until("free")
            qbs = [C.ffs[0].qb_w, C.ffs[1].qb_w]
            qbl = [C.qlabels[1], C.qlabels[3]]
            tags = [T("free", 30, YELLOW).next_to(l, RIGHT, buff=0.15) for l in qbl]
            self.play(*[w.animate.set_stroke(YELLOW) for w in qbs], *recolor(qbl, YELLOW),
                      run_time=min(1.2, c.until("score")))
            c.wait_until(own_word=tags[0])
            self.play(*appear(*tags, shift=None, lag=0.2), run_time=min(1.0, c.until("score")))
            # {score}
            c.wait_until("score")
            sb = sync_board(with_row=False)
            C.generate_target()
            C.target.scale_to_fit_width(6.0).move_to(_p(3.55, 1.75))
            self.play(*during(disappear(n_and, n_or, n_all, n_inv, *tags), 0, 0.45),  # early: the board slides in whole
                      *during([MoveToTarget(C)], 0.2, 0.7),
                      *during([FadeIn(sb, shift=0.4 * UP)], 0.7, 1.0),  # early: the board slides in whole
                      run_time=min(2.0, c.until("synchroniser")))
            c.wait_until("synchroniser")
            row = sb.sync_row
            self.play(*appear(sb.sync_sub), run_time=min(0.9, c.until("sequential")))
            for i, (cue, nxt) in enumerate((("sequential", "two flip-flops"), ("two flip-flops", "seven gates"),
                                            ("seven gates", "no output logic"), ("no output logic", "plain"))):
                c.wait_until(cue)
                self.play(*appear(row[i]), run_time=min(0.9, c.until(nxt)))
            # {plain}
            c.wait_until("plain")
            codes = VGroup(*[Mono(s, 30, GREEN) for s in ("[00]", "[01]", "[10]")]).arrange(RIGHT, buff=0.35)
            codes.move_to(_p(0, row.get_y())).align_to(_p(0.6, 0), LEFT)
            self.play(*appear(*codes, lag=0.3, shift=None), run_time=min(1.4, c.until("just counting")))
            c.wait_until("just counting")
            jc = T("just counting", 30, YELLOW).next_to(codes, DOWN, buff=0.3)
            self.play(*appear(jc), run_time=min(1.0, c.until()))
