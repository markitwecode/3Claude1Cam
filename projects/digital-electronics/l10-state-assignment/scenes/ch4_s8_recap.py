"""Chapter 4, scene 8: recap in six panels on a 3 x 2 grid, then a silhouette of Part 5. Clips c4.recap.1 – c4.recap.3.

Layout as ch2_s8_recap (its slot_frame / vis_center / fit / caption / veil are imported): "Recap" T 40
at (0, 3.4), six faint DIM slot frames, each panel's picture fitted into its slot, its line (T 28) under it,
earlier panels dimmed under a BG veil.
 r1 s1's onehot_row (eight cells) with s2's YELLOW "hot" tag, the GOLD 1 stepping along;
 r2 s3's ring4 on its CLK line, stepping, over p. 138's table (transposed: now / next codes);
 r3 s4's onehot_circuit, the ORs flashed and the lamps lit in their colours;
 r4 s5's two panels (l9_circuit + onehot_circuit, TEAL loop / GOLD output bands), the gate riding the arrow;
 r5 the amber flip-flop a with ch3 s6's RED active-low S pin: level 1 -> 0, its 1 arrives, the amber lamp lights;
 r6 s7's budget bar (L8 budget_bar): the PURPLE segment shrinks away, then T_c >= t_pc + t_su.
{next}: the grid shrinks away; a tape of white bits slides right (pattern 01111110 every 16 bits,
outlined YELLOW); three empty BLUE state circles (p. 123's layout) below. {both}: two chips (ch1 s1's
chip()), "Part 5: two flip-flops" lit, "Part 6: one-hot" DIM.
End card (handover to ch5 s1): end_card() = the tape at END_OFF, the circles, the chips and
"Part 5 · Hunt, Sight and Sync" T 40 at (0, 3.2). The tape keeps sliding ~7 s, stops, holds.
"""
# style: 2
# handover: next
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

G2 = load_scene("ch2_s8_recap")          # the recap grid
S1 = load_scene("ch1_s1_hook")           # lamp colours, chip()
S21 = load_scene("ch2_s1_hook")          # make_ff, and_gate
S25 = load_scene("ch2_s5_ring")          # ring_cell_style, cell_bit
OH = load_scene("ch4_s1_hook")           # onehot_row, hot_bit
S3 = load_scene("ch4_s3_ring4")          # ring4
S4 = load_scene("ch4_s4_outputs")        # onehot_circuit
C5 = load_scene("ch4_s5_compare")        # l9_circuit, band, placed
F7 = load_scene("ch4_s7_fast")           # budget_bar, ineq_tex
P6 = load_scene("ch3_s6_preset")         # pin
slot, slot_frame, vis_center, fit, caption, veil = (G2.slot, G2.slot_frame, G2.vis_center, G2.fit,
                                                    G2.caption, G2.veil)
COL_X = G2.COL_X
LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)
ONEHOT = S3.ONEHOT


def _p(x, y):
    return np.array([x, y, 0.0])


# =============================================================================================
# the Part 5 silhouette and the end card (ch5 s1 opens on end_card())
# =============================================================================================
PATTERN = "01111110"
_DATA = ["10010110", "00101101", "11010010", "01001011", "10100110", "00110101"]
TAPE_Y = 2.0
BIT_P = 0.42                 # bit pitch: no gaps
TAPE_SIZE = 40
FRAME = 16                   # pattern + 8 data bits
SPEED = 0.9                  # units per second
END_OFF = 15.0               # the tape's offset in the last frame
FADE_X0, FADE_X1 = 5.4, 6.5  # bits fade out between these |x|
TAPE_N = 72
TAPE_X0 = -6.9 - END_OFF     # bit 0's x at offset 0


def tape_bits():
    s = ""
    k = 0
    while len(s) < TAPE_N:
        s += PATTERN + _DATA[k % len(_DATA)]
        k += 1
    return s[:TAPE_N]


def _edge_op(x, half=0.0):
    a = abs(x) + half
    return float(np.clip((FADE_X1 - a) / (FADE_X1 - FADE_X0), 0, 1))


def tape(off=0.0, vis=1.0):
    """The bit stream: .bits (Mono, white), .boxes (YELLOW outlines round each PATTERN copy).
    .layout(off, vis) places everything for that offset (bits fade near the frame edges)."""
    s = tape_bits()
    bits = [Mono(b, TAPE_SIZE, FG) for b in s]
    starts = [i for i in range(0, TAPE_N - len(PATTERN) + 1, FRAME)]
    boxes = [RoundedRectangle(corner_radius=0.1, width=len(PATTERN) * BIT_P + 0.08, height=0.72)
             .set_stroke(YELLOW, 3).set_fill(opacity=0) for _ in starts]
    g = VGroup(*boxes, *bits)
    g.bits, g.boxes, g.starts = bits, boxes, starts

    def layout(o, v=1.0):
        for i, b in enumerate(bits):
            x = TAPE_X0 + i * BIT_P + o
            b.move_to(_p(x, TAPE_Y))
            b.set_opacity(v * _edge_op(x))
        for st, bx in zip(starts, boxes):
            x = TAPE_X0 + (st + (len(PATTERN) - 1) / 2) * BIT_P + o
            bx.move_to(_p(x, TAPE_Y))
            bx.set_stroke(opacity=v * _edge_op(x, bx.width / 2 - 0.6))
        return g

    g.layout = layout
    layout(off, vis)
    return g


CIRC_R = 0.75
CIRC_C = (_p(-2.0, 0.35), _p(2.0, 0.35), _p(0.0, -1.2))   # p. 123: A top left, B top right, C below
CHIP_Y = -2.85


def state_circles():
    return VGroup(*[Circle(radius=CIRC_R).set_stroke(BLUE, 4).set_fill(BG, 1).move_to(c) for c in CIRC_C])


def part_chips():
    lit = S1.chip("Part 5: two flip-flops", "Part 5:", size=30)
    lit.box.set_stroke(YELLOW, 3)
    dim = S1.chip("Part 6: one-hot", "Part 6:", size=30)
    dim.text.set_color(DIM)
    g = VGroup(lit, dim).arrange(RIGHT, buff=0.7).move_to(_p(0, CHIP_Y))
    g.lit, g.dim = lit, dim
    return g


def part5_line():
    return T("Part 5 · Hunt, Sight and Sync", 40).move_to(_p(0, 3.2))


def end_card():
    """ch4's last frame: the tape at END_OFF, three empty state circles, the two chips, the part line."""
    tp = tape(END_OFF)
    circ = state_circles()
    chips = part_chips()
    part = part5_line()
    g = VGroup(tp, circ, chips, part)
    g.tape, g.circles, g.chips, g.part = tp, circ, chips, part
    return g


def handover_shot():
    return end_card()


# =============================================================================================
# panel pictures
# =============================================================================================
MIN_TXT = 27.5


def strip_text(m, keep=()):
    """Remove every Text / MathTex inside m (too small to read once shrunk into a slot), except `keep`."""
    keep_ids = {id(x) for k in keep for x in k.get_family()}
    for mob in m.get_family():
        for sub in list(mob.submobjects):
            if isinstance(sub, (Text, SingleStringMathTex)) and id(sub) not in keep_ids:
                mob.remove(sub)
    return m


def fit_legible(m, ctr, w=G2.VIS_W, h=G2.VIS_H, texts=None):
    """fit(), after growing the texts (`texts`, default all) about their centres to end >= MIN_TXT."""
    k0 = min(w / m.width, h / m.height)
    F7.legible(VGroup(*texts) if texts is not None else m, k0, MIN_TXT)
    return fit(m, ctr, w, h)


# =============================================================================================
# =============================================================================================
def amber_ff():
    """r5: flip-flop a (ring4's look, holding 0), its RED active-low S pin, Q into the amber lamp."""
    ff = S21.make_ff(size=56)
    ff.remove(ff.qb_w, ff.qb_l)
    S25.ring_cell_style(ff.box, 0)
    bit = S25.cell_bit(0, 56).move_to(ff.box.get_center() + 0.4 * DOWN)
    name = T("a", 56, GREEN).next_to(ff.box, UP, buff=0.3).align_to(ff.box, RIGHT).shift(0.1 * LEFT)
    sp = P6.pin(ff, "S", size=48)
    q_end = ff.q_w.get_end()
    lamp_c = q_end + 1.0 * RIGHT
    lamp = Circle(radius=0.5).set_stroke(DIM, 2).set_fill(S1.LAMP_OFF, 1).move_to(lamp_c + 0.5 * RIGHT)
    wire = Line(q_end, lamp.get_left()).set_stroke(FG, 4)
    lab = T("A", 52, S1.LAMP_AMBER).next_to(lamp, DOWN, buff=0.2)
    g = VGroup(wire, ff, bit, name, sp, lamp, lab)
    g.ff, g.bit, g.name, g.pin, g.lamp, g.lamp_label, g.wire = ff, bit, name, sp, lamp, lab, wire
    return g


class Recap(NarratedScene):
    def construct(self):
        self.panels = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.end()

    def dim_previous(self):
        out = []
        for t in self.panels:
            if not getattr(t, "veiled", False):
                t.veiled = True
                out.append(FadeIn(veil(t)))
        return out

    # -- r1 helper: the GOLD 1 moves one cell on, the "hot" tag follows -----------------------------
    def oh_step(self):
        row, k = self.row, self.row_k
        i = self.hot
        j = (i + 1) % 8
        old_i, old_j = self.digs[i], self.digs[j]
        new_i = OH.hot_bit(0, self.r1_size).scale(k).move_to(old_i)
        new_j = OH.hot_bit(1, self.r1_size).scale(k).move_to(old_j)
        bi, bj = row.boxes[i].copy(), row.boxes[j].copy()
        S25.ring_cell_style(bi, 0)
        S25.ring_cell_style(bj, 1)
        anims = [*swap(old_i, new_i, shift=None), *swap(old_j, new_j, shift=None),
                 Transform(row.boxes[i], bi), Transform(row.boxes[j], bj),
                 self.tag.animate.set_x(row.boxes[j].get_x())]
        self.digs[i], self.digs[j] = new_i, new_j
        self.hot = j
        self._oh_pending = ([new_i, new_j], [old_i, old_j])
        return anims

    def oh_settle(self):
        add, drop = self._oh_pending
        settle(self, self.row, add=add, drop=drop)

    # -- r2 helper: one clock edge on the small ring --------------------------------------------------
    def ring_step(self, run_time):
        R, k = self.R, self.R_k
        i = R.values.index(1)
        j = (i + 1) % 4
        old_i, old_j = R.bits[i], R.bits[j]
        new_i = S25.cell_bit(0, self.r2_size).scale(k).move_to(old_i)
        new_j = S25.cell_bit(1, self.r2_size).scale(k).move_to(old_j)
        ti, tj = R.cells[i].copy(), R.cells[j].copy()
        S25.ring_cell_style(ti, 0)
        S25.ring_cell_style(tj, 1)
        path = R.wires[i][0].copy().set_stroke(GOLD, 6)
        self.play(*swap(old_i, new_i, shift=None), *swap(old_j, new_j, shift=None),
                  Transform(R.cells[i], ti), Transform(R.cells[j], tj),
                  VShowPassingFlash(path, time_width=0.6, taper_width=0.1),
                  Transform(self.tbox, self.col_box(j)), run_time=run_time)
        R.values[i], R.values[j] = 0, 1
        R.bits[i], R.bits[j] = new_i, new_j
        settle(self, R, add=[new_i, new_j], drop=[old_i, old_j])

    # -- r3 helper: one clock edge on the output circuit's ring; the lamps follow the hot 1 ----------
    def circ_step(self, run_time, *extra):
        C = self.C
        R = C.ring
        i = R.values.index(1)
        j = (i + 1) % 4
        old_i, old_j = R.bits[i], R.bits[j]
        k = old_i.height / S25.cell_bit(1, S3.R4_BIT).height
        new_i = S25.cell_bit(0, S3.R4_BIT).scale(k).move_to(old_i)
        new_j = S25.cell_bit(1, S3.R4_BIT).scale(k).move_to(old_j)
        ti, tj = R.cells[i].copy(), R.cells[j].copy()
        S25.ring_cell_style(ti, 0)
        S25.ring_cell_style(tj, 1)
        self.play(*swap(old_i, new_i, shift=None), *swap(old_j, new_j, shift=None),
                  Transform(R.cells[i], ti), Transform(R.cells[j], tj), *C.light(j), *extra,
                  run_time=run_time)
        R.values[i], R.values[j] = 0, 1
        R.bits[i], R.bits[j] = new_i, new_j
        R.remove(old_i, old_j)
        R.add(new_i, new_j)
        fam = set(id(m) for m in C.get_family())
        self.mobjects = [m for m in self.mobjects if id(m) not in fam or m is C]
        if C not in self.mobjects:
            self.add(C)

    def col_box(self, j):
        g = VGroup(*self.tcols[j])
        return (RoundedRectangle(corner_radius=0.08, width=g.width + 0.16, height=g.height + 0.16)
                .set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).move_to(g).set_z_index(-1))

    # -- c4.recap.1: r1 one-hot row, r2 ring of four + table, r3 the output gates --------------------
    def clip1(self):
        with self.say("c4.recap.1") as c:
            head = T("Recap", 40).move_to(_p(0, 3.4))
            frames = [slot_frame(i) for i in range(6)]
            self.play(*appear(head, shift=None), *[FadeIn(f) for f in frames],  # early: the scene's heading
                      run_time=min(1.2, c.until("r1")))

            # r1: eight cells, one GOLD 1, the "hot" tag over it
            c.wait_until("r1")
            row = self.row = OH.onehot_row(8, hot=0)
            k0 = min(G2.VIS_W / row.width, 1.5 / row.height)
            self.r1_size = MIN_TXT / k0
            for d in row.digits:
                d.scale(self.r1_size / OH.BIT_SIZE)
            F7.legible(VGroup(row.clk_label), k0, MIN_TXT)
            row.clk_label.next_to(row.clk.get_left(), DOWN, buff=0.14, aligned_edge=LEFT)
            k = self.row_k = fit(row, vis_center(0) + 0.22 * DOWN, h=1.5)
            self.digs = list(row.digits)
            self.hot = 0
            tag = self.tag = T("hot", 30, YELLOW)
            tag.move_to(_p(row.boxes[0].get_x(), row.boxes[0].get_y() + 1.65 * k + 0.12))
            cap1 = caption(0, ["one 1 at a time:", "one flip-flop per state"], t2c={"1": GOLD})
            self.play(FadeIn(row), *appear(tag), *appear(cap1, shift=None), run_time=1.0)  # early: panel shown whole
            c.wait_until("holds a one")
            self.play(*self.oh_step(), run_time=0.9)
            self.oh_settle()
            c.wait_until("one flip-flop per state")
            self.play(*self.oh_step(), run_time=0.8)
            self.oh_settle()
            self.play(*self.oh_step(), run_time=min(0.8, c.until("r2", floor=0.5)))
            self.oh_settle()
            self.panels.append(VGroup(row, tag, cap1))

            # r2: the ring of four on its CLK line, over the table (now / next codes)
            c.wait_until("r2")
            vc = vis_center(1)
            R = self.R = S3.ring4("1000")
            R.remove(*R.heads)
            strip_text(R, keep=R.bits)
            k0 = min(3.9 / R.width, 1.05 / R.height)
            self.r2_size = MIN_TXT / k0
            for d in R.bits:
                d.scale(self.r2_size / S3.R4_BIT)
            self.R_k = fit(R, vc + 0.48 * UP, w=3.9, h=1.05)
            xs = [vc[0] + (j - 1.5) * 1.0 for j in range(4)]
            now = [Mono(ONEHOT[j], 27, FG, t2c={"1": GOLD}).move_to(_p(xs[j], vc[1] - 0.42)) for j in range(4)]
            nxt = [Mono(ONEHOT[(j + 1) % 4], 27, FG, t2c={"1": GOLD}).move_to(_p(xs[j], vc[1] - 0.88))
                   for j in range(4)]
            rule = Line(_p(xs[0] - 0.45, vc[1] - 0.65), _p(xs[3] + 0.45, vc[1] - 0.65)).set_stroke(DIM, 2)
            self.tcols = [[now[j], nxt[j]] for j in range(4)]
            self.tbox = self.col_box(0)
            cap2 = caption(1, ["a ring of four:", "no next-state logic"])
            self.play(*self.dim_previous(), FadeIn(R), *appear(*now, *nxt, lag=0.05, shift=None),  # early: panel shown whole
                      FadeIn(rule), FadeIn(self.tbox), *appear(cap2, shift=None), run_time=1.0)
            c.wait_until("ring of four")
            self.ring_step(0.9)
            c.wait_until("no next-state logic")
            self.ring_step(0.8)
            self.panels.append(VGroup(R, *now, *nxt, rule, self.tbox, cap2))

            # r3: the lamps from two ORs and a wire
            c.wait_until("r3")
            C = S4.onehot_circuit("1000")
            C.ring.remove(*C.ring.heads)
            strip_text(C, keep=C.ring.bits)
            fit_legible(C, vis_center(2), h=2.0, texts=C.ring.bits)
            for u in C.lamps:
                u.scale(1.6)
            cap3 = caption(2, ["R = r + ra", "A = ra + a,  G = g"],
                           t2c={"R": S1.LAMP_RED, "A": S1.LAMP_AMBER, "G": S1.LAMP_GREEN,
                                "r": GREEN, "a": GREEN, "g": GREEN})
            C.lamps[0].set_fill(S1.LAMP_RED, 1)                 # state r: red
            self.C = C
            self.play(*self.dim_previous(), FadeIn(C), *appear(cap3, shift=None), run_time=1.0)  # early: panel shown whole
            c.wait_until("two or gates")
            self.circ_step(min(1.0, c.until("plain wire", floor=0.7)),
                           *[FlashAround(g, time_width=1.5) for g in C.gates])        # r -> ra: red and amber
            c.wait_until("plain wire")
            self.circ_step(min(1.0, c.until(floor=0.7)), FlashAround(C.g_wire, time_width=1.5))  # ra -> g: green
            if c.remaining >= 0.9:
                self.circ_step(min(0.8, c.remaining))                                   # g -> a: amber
            self.panels.append(VGroup(C, cap3))

    # -- c4.recap.2: r4 the logic moved, r5 the asynchronous set, r6 the budget bar ------------------
    def clip2(self):
        with self.say("c4.recap.2") as c:
            # r4: s5's two panels, bands, the gate riding the arrow
            L = C5.l9_circuit()
            top = L.get_top()[1]
            lb = [C5.band(-7.25, 6.55, -1.66, top + 0.15, TEAL), C5.band(-7.25, 6.55, -2.42, -1.72, GOLD)]
            C5.placed(L, lb, 6.3, _p(C5.L_X, C5.CIRC_Y))
            Rc = S4.onehot_circuit()
            rb = [C5.band(-6.15, 5.75, -0.3, 3.15, TEAL), C5.band(-6.15, 5.75, -2.95, -0.45, GOLD)]
            C5.placed(Rc, rb, 6.1, _p(C5.R_X, C5.CIRC_Y))
            hL = T("Lecture 9", 100, FG).move_to(_p(C5.L_X, 3.6))
            hR = T("one-hot", 100, FG).move_to(_p(C5.R_X, 3.6))
            a0 = lb[0].get_corner(DR) + _p(-0.35, 0.55)
            a1 = rb[1].get_corner(UL) + _p(0.45, -0.55)
            arrow = CurvedArrow(a0, a1, angle=-PI / 3, color=YELLOW, stroke_width=4, tip_length=0.2)
            arc = ArcBetweenPoints(a0, a1, angle=-PI / 3)
            icon = S21.and_gate(color=YELLOW).rotate(-PI / 2).scale(0.5).move_to(a0)
            strip_text(L)
            strip_text(Rc)
            big = VGroup(L, *lb, Rc, *rb, hL, hR, arrow, arc, icon)
            fit(big, vis_center(3))
            cap4 = caption(3, ["the logic moved", "out of the loop"])
            self.play(*self.dim_previous(), FadeIn(L), FadeIn(Rc), *[FadeIn(b) for b in lb + rb],  # early: panel shown whole
                      *appear(hL, hR, shift=None), *appear(cap4, shift=None), run_time=1.0)
            c.wait_until("moved out of the loop")
            self.play(GrowFromCenter(icon), run_time=0.5)
            self.play(Create(arrow), MoveAlongPath(icon, arc), run_time=min(1.6, c.until("r5", floor=0.8)))
            self.panels.append(VGroup(L, *lb, Rc, *rb, hL, hR, arrow, icon, cap4))

            # r5: the amber flip-flop, set through its active-low pin
            c.wait_until("r5")
            A = amber_ff()
            fit_legible(A, vis_center(4) + 0.1 * UP, w=3.0, h=1.95)
            lvl = value_label("1", 30, GOLD).next_to(A.pin.label, LEFT, buff=0.15)
            cap5 = caption(4, ["start in a used state"])
            self.play(*self.dim_previous(), FadeIn(A), *appear(lvl, shift=None), *appear(cap5, shift=None),  # early: panel shown whole
                      run_time=1.0)
            c.wait_until("asynchronous set")
            lvl0 = value_label("0", 30, RED).move_to(lvl)
            z = S25.cell_bit(0, 56)
            one = S25.cell_bit(1, 56).scale(A.bit.height / z.height).move_to(A.bit)
            box1 = A.ff.box.copy()
            S25.ring_cell_style(box1, 1)
            self.play(*swap(lvl, lvl0), FlashAround(A.pin.bub, color=RED, time_width=1.5),
                      *during(swap(A.bit, one, shift=None), 0.3, 0.8),
                      *during([Transform(A.ff.box, box1)], 0.3, 0.8),
                      *during([A.lamp.animate.set_fill(S1.LAMP_AMBER, 1)], 0.6, 1.0),
                      run_time=min(1.5, c.until(floor=0.9)))
            lvl1 = value_label("1", 30, GOLD).move_to(lvl0)
            self.play(*swap(lvl0, lvl1), run_time=min(0.9, c.until("r6", floor=0.5)))
            self.panels.append(VGroup(A.wire, A.ff, A.name, A.pin, A.lamp, A.lamp_label, one, lvl1, cap5))

            # r6: the budget bar loses its PURPLE segment
            c.wait_until("r6")
            vc = vis_center(5)
            bar = F7.budget_bar([(t, col, w) for (t, col, _), w in zip(F7.L8B.SEGS, F7.SEG_L)], sum(F7.SEG_L),
                                x0=0, y=0, sym_size=80)
            bar.tc.scale(1.7, about_edge=RIGHT)
            fit(bar, vc + 0.45 * UP, w=3.7, h=1.0)
            ineq = F7.ineq_tex("T_c", r"\ge", "t_{pc}", "+", "t_{su}", size=40).move_to(vc + 0.55 * DOWN)
            cap6 = caption(5, ["no logic in the loop:", "as fast as the flip-flops"])
            self.play(*self.dim_previous(), FadeIn(bar), *appear(cap6, shift=None), run_time=1.0)  # early: panel shown whole
            c.wait_until("no logic in its loop")
            pink, purple, gold = bar.segs
            sym_pd, sym_su = bar.syms[1], bar.syms[2]
            dx = purple.width
            flat = purple.copy().stretch_to_fit_width(0.01).align_to(purple, LEFT)
            out2 = bar.outline.copy().stretch_to_fit_width(bar.outline.width - dx).align_to(bar.outline, LEFT)
            self.play(*during(disappear(sym_pd), 0, 0.3),
                      *during([Transform(purple, flat), Transform(bar.outline, out2),
                               gold.animate.shift(dx * LEFT), sym_su.animate.shift(dx * LEFT)], 0.15, 1.0),
                      run_time=min(1.4, c.until("as fast", floor=0.9)))
            self.remove(purple)
            settle(self, bar, drop=[purple, sym_pd])
            bar.segs, bar.syms = [pink, gold], [bar.syms[0], sym_su]
            c.wait_until("as fast")
            bar.generate_target()
            tg = bar.target
            tg.scale(1.8).move_to(_p(vc[0], vc[1] + 0.45))
            tg.syms[0].next_to(tg.segs[0], UP, buff=0.15).align_to(tg.segs[0], RIGHT).shift(0.06 * LEFT)
            tg.syms[1].next_to(tg.segs[1], UP, buff=0.15).align_to(tg.segs[1], LEFT).shift(0.06 * RIGHT)
            self.play(MoveToTarget(bar), *appear(ineq, shift=None),
                      run_time=min(1.2, c.until(floor=0.8)))
            self.panels.append(VGroup(bar, ineq, cap6))

    # -- c4.recap.3: next time, a real machine with inputs ---------------------------------------------
    def slide(self, rt, *anims):
        self.play(self.trk.animate(rate_func=linear).set_value(self.trk.get_value() + SPEED * rt), *anims,
                  run_time=rt)

    def clip3(self):
        trk = self.trk = ValueTracker(0.0)
        vis = self.vis = ValueTracker(0.0)
        tp = self.tp = tape(0.0, 0.0)
        tp.add_updater(lambda m: m.layout(trk.get_value(), vis.get_value()))
        circ = self.circ = state_circles()
        chips = self.chips = part_chips()
        with self.say("c4.recap.3") as c:
            old = list(self.mobjects)
            self.add(tp)
            self.slide(1.4, *during([FadeOut(m, scale=0.5) for m in old], 0, 0.5),
                       during([vis.animate.set_value(1.0)], 0.5, 1.0)[0])
            rt = c.until("real machine", floor=0.05)
            if rt > 0.1:
                self.slide(rt)
            self.slide(1.0, *[FadeIn(cc) for cc in circ])
            rt = c.until("two flip-flops", floor=0.05)
            if rt > 0.1:
                self.slide(rt)
            self.slide(1.0, *appear(chips.lit, shift=None))
            rt = c.until("one-hot", floor=0.05)
            if rt > 0.1:
                self.slide(rt)
            self.slide(1.0, *appear(chips.dim, shift=None))
            rt = c.until(floor=0.05)
            if rt > 0.1:
                self.slide(rt)

    # -- end card: the stream keeps passing under "Part 5 · Hunt, Sight and Sync" ---------------------
    def end(self):
        part = part5_line()
        self.slide(1.2, *appear(part))
        rest = END_OFF - self.trk.get_value()
        self.play(self.trk.animate(rate_func=linear).set_value(END_OFF), run_time=max(2.0, rest / SPEED))
        self.tp.clear_updaters()
        self.tp.layout(END_OFF, 1.0)
        self.wait(1.2)                     # handover: ch5 s1 opens on end_card()
