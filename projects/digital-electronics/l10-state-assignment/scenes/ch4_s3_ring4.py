"""Chapter 4, scene 3: the traffic light, one-hot: four flip-flops r ra g a, one-hot codes, the
transition table, D inputs read off it, and the ring of four. Clips c4.ring.1 – c4.ring.4.

Chapter-wide helper owned here (s4 – s8 import it via load_scene("ch4_s3_ring4")):
- ring4(bits="1000") -> VGroup, the one-hot traffic light as p. 139's shift register, box centres
  on y = 0, centred on x = 0 (about 12.2 x 3.3 incl. the CLK label). Four D flip-flops (ch2 s1
  make_ff, Q-bar dropped, scale R4_S) at x = (i - 1.5) * R4_P, order r, ra, g, a. Cells in ch2's
  style (BLUE border, faint GOLD fill when holding 1), the bit (ch2 cell_bit, Mono 40) in the
  lower half of each box. Q of each into D of the next (FG wires with tips), Q of a back over the
  top into D of r, one YELLOW CLK line underneath with its label at the left.
  Attributes: .ffs[i] (make_ff group: .box .d_l .q_l .d_w .q_w .clk_w), .cells[i] (= ffs[i].box),
  .bits[i] (current digit Mono), .values (list of ints), .labels[i] (GREEN T 40), .heads[i]
  (tiny lamp column of state i), .wires[i] (VGroup(path, tip); wires[3] = the feedback a -> r),
  .wire_paths[i], .clk (VGroup(.clk_line, .clk_label)), .bit_pos(i) -> where cell i's digit sits.
  .step(scene, run_time=0.8, flash=True, settle_group=True, extra=()) plays one clock edge (the 1
  moves one cell on; a GOLD flash runs along its wire) and keeps .bits/.values and the group in sync.
- place_code(ring, i, text, size) -> GREEN Mono code beside state i of ch1's traffic_ring (1s GOLD).
- handover_shot(): this scene's last frame: ring4 at the top (R4_Y), its 1 in r; the traffic ring
  small at the bottom left with its one-hot codes.
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

S1 = load_scene("ch1_s1_hook")
S21 = load_scene("ch2_s1_hook")
S25 = load_scene("ch2_s5_ring")
traffic_ring, lamp_column = S1.traffic_ring, S1.lamp_column
make_ff = S21.make_ff
ring_cell_style, cell_bit, ring_circle = S25.ring_cell_style, S25.cell_bit, S25.ring_circle
LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)

CODES3 = ["100", "110", "001", "010"]
ONEHOT = ["1000", "0100", "0010", "0001"]
NAMES = ["r", "ra", "g", "a"]


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- ring4 (chapter-wide) --------------------------------------------------------------------------
R4_S = 0.6            # flip-flop scale
R4_P = 2.8            # flip-flop pitch
R4_BIT = 40           # digit size
R4_FB_Y = 1.75        # feedback wire height (box centres at 0)
R4_Y = 1.25           # final height of the box centres (handover)


def _tip(end, direction):
    t = Triangle().set_stroke(width=0).set_fill(FG, 1).scale(0.1)
    t.rotate(-PI / 2 if direction[0] > 0 else PI / 2)
    return t.move_to(end - 0.08 * np.array(direction))


def ring4(bits="1000"):
    R = VGroup()
    ffs, labels, heads = [], [], []
    xs = [(i - 1.5) * R4_P for i in range(4)]
    for i, x in enumerate(xs):
        ff = make_ff(size=56)
        ff.remove(ff.qb_w, ff.qb_l)
        ring_cell_style(ff.box, bits[i])
        ff.scale(R4_S, about_point=ORIGIN).shift(x * RIGHT)
        ffs.append(ff)
        ref = T("a", 40).next_to(ff.box, UP, buff=0.22)
        lab = T(NAMES[i], 40, GREEN).move_to(ref).align_to(ref, UP)
        labels.append(lab)
        head = lamp_column(S1.STATE_LAMPS[i], scale=0.32).next_to(lab, RIGHT, buff=0.16)
        head.set_y(ref.get_y())
        heads.append(head)
    half = (S21.BOX_W / 2 + S21.WIRE) * R4_S
    pin = S21.PIN_Y * R4_S
    wires, paths = [], []
    for i in range(3):
        a, b = _p(xs[i] + half, pin), _p(xs[i + 1] - half, pin)
        line = Line(a, b - 0.1 * RIGHT).set_stroke(FG, 4)
        wires.append(VGroup(line, _tip(b, RIGHT)))
        paths.append(Line(a, b).set_stroke(FG, 4))
    e = 0.35
    fb_pts = [_p(xs[3] + half, pin), _p(xs[3] + half + e, pin), _p(xs[3] + half + e, R4_FB_Y),
              _p(xs[0] - half - e, R4_FB_Y), _p(xs[0] - half - e, pin), _p(xs[0] - half, pin)]
    fb = VMobject().set_points_as_corners(fb_pts[:-1] + [fb_pts[-1] - 0.1 * RIGHT]).set_stroke(FG, 4)
    wires.append(VGroup(fb, _tip(fb_pts[-1], RIGHT)))
    paths.append(VMobject().set_points_as_corners(fb_pts).set_stroke(FG, 4))
    clk_y = -(S21.BOX_H / 2 + S21.EN_WIRE) * R4_S
    clk_line = Line(_p(xs[0] - 1.1, clk_y), _p(xs[3], clk_y)).set_stroke(YELLOW, 5)
    clk_label = T("CLK", 32, YELLOW).next_to(clk_line, LEFT, buff=0.18)
    clk = VGroup(clk_line, clk_label)
    digits = [cell_bit(b, R4_BIT).move_to(ffs[i].box.get_center() + 0.35 * R4_S * DOWN)
              for i, b in enumerate(bits)]
    R.add(*wires, clk, *ffs, *labels, *heads, *digits)
    R.ffs, R.cells, R.labels, R.heads = ffs, [f.box for f in ffs], labels, heads
    R.wires, R.wire_paths, R.clk, R.clk_line, R.clk_label = wires, paths, clk, clk_line, clk_label
    R.bits, R.values = digits, [int(b) for b in bits]

    def bit_pos(i):
        return R.cells[i].get_center() + 0.35 * R4_S * DOWN

    def step(scene, run_time=0.8, flash=True, settle_group=True, extra=()):
        i = R.values.index(1)
        j = (i + 1) % 4
        old_i, old_j = R.bits[i], R.bits[j]
        new_i = cell_bit(0, R4_BIT).move_to(bit_pos(i))
        new_j = cell_bit(1, R4_BIT).move_to(bit_pos(j))
        ti, tj = R.cells[i].copy(), R.cells[j].copy()
        ring_cell_style(ti, 0)
        ring_cell_style(tj, 1)
        # the 1 is never missing: it lands in cell j before it leaves cell i
        anims = [*during(disappear(old_j), 0, 0.3), *during(appear(new_j, shift=None), 0.3, 0.65),
                 *during(disappear(old_i), 0.5, 0.8), *during(appear(new_i, shift=None), 0.8, 1.0),
                 Transform(R.cells[i], ti), Transform(R.cells[j], tj)]
        if flash:
            p = R.wire_paths[i].copy().move_to(R.wires[i]).set_stroke(GOLD, 7)
            anims.append(VShowPassingFlash(p, time_width=0.6, taper_width=0.1))
        anims += list(extra)
        scene.play(*anims, run_time=run_time)
        R.values[i], R.values[j] = 0, 1
        R.bits[i], R.bits[j] = new_i, new_j
        if settle_group:
            settle(scene, R, add=[new_i, new_j], drop=[old_i, old_j])
        else:
            R.remove(old_i, old_j)
            R.add(new_i, new_j)

    R.bit_pos, R.step = bit_pos, step
    return R


def place_code(ring, i, text, size=30):
    m = Mono(text, size, GREEN, t2c={"1": GOLD})
    circ = ring.circles[i]
    m.next_to(circ, LEFT if i == 3 else RIGHT, buff=0.15)
    m.set_y(circ.get_y())
    return m


TR_S, TR_C = 0.42, _p(-3.9, -2.2)     # final small traffic ring


def final_ring():
    ring = traffic_ring().scale(TR_S).move_to(TR_C)
    codes = [place_code(ring, i, t, 28) for i, t in enumerate(ONEHOT)]
    return ring, codes


def handover_shot():
    R = ring4("1000").shift(R4_Y * UP)
    ring, codes = final_ring()
    return VGroup(R, ring, *codes)


# ---- this scene's layout ---------------------------------------------------------------------------
RING1_S, RING1_C = 0.65, _p(0.8, 1.35)
RING2_S, RING2_C = 0.5, _p(-3.5, 1.6)
ROW_Y = -2.2                      # box centres of the cells in clips 1-3
TX = 2.9                          # table centre x
CP, GAP = 0.7, 0.45               # table column pitch, gap between halves
HEAD_Y, ROW0_Y, ROW_P = 3.2, 2.55, 0.55
ROW_SIZE = 32
_CP = []


def _cp():
    """Glyph pitch of a table half, "1  0  0  0" in Mono ROW_SIZE (measured once)."""
    if not _CP:
        ref = Mono("0  0  0  0", ROW_SIZE)
        _CP.append((ref[3].get_x() - ref[0].get_x()) / 3)
    return _CP[0]
FIVE_C, FIVE_S = _p(4.3, -1.95), 0.55


def col_x(k):
    """Table column k: 0-3 current r ra g a, 4-7 next r' ra' g' a'."""
    cp = _cp()
    x0 = TX - (7 * cp + GAP) / 2
    return x0 + k * cp + (GAP if k >= 4 else 0)


def ring_flash(circle):
    return VShowPassingFlash(circle.copy().set_stroke(YELLOW, 7), time_width=0.6, taper_width=0.1)


def mini_ff(name, color, x, y):
    ff = make_ff(size=56).scale(0.28, about_point=ORIGIN).shift(_p(x, y))
    ff.remove(ff.d_l, ff.q_l, ff.qb_l)
    ff.set_color(DIM)
    ff.tri.set_fill(BG, 1)
    nm = T(name, 32, color).set_opacity(0.6).next_to(ff.d_w, LEFT, buff=0.08)
    return VGroup(ff, nm)


def eq_tex(sub, rhs):
    m = MathTex("D", "_{" + sub + "}", "=", rhs, font_size=46)
    m[0].set_color(BLUE)
    m[1].set_color(GREEN)
    m[3].set_color(GREEN)
    return m


class TrafficOneHot(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)   # handover: s4 opens on this shot

    # ------------------------------------------------------------------------------------ c4.ring.1
    def clip1(self):
        ring = traffic_ring().scale(RING1_S).move_to(RING1_C)
        codes3 = [Mono(t, 32, GREEN) for t in CODES3]
        for i, m in enumerate(codes3):
            m.next_to(ring.circles[i], LEFT if i == 3 else RIGHT, buff=0.15).set_y(ring.circles[i].get_y())
        R = ring4("1000").shift(ROW_Y * UP)
        for lab in R.labels:
            lab.set_color(DIM)
        self.ring, self.codes3, self.R = ring, codes3, R

        with self.say("c4.ring.1") as c:
            self.play(*[FadeIn(a) for a in ring.arrows], *[FadeIn(s, scale=0.9) for s in ring.states],
                      *appear(*codes3, shift=None, lag=0.1), run_time=min(1.6, c.until("order")))
            c.wait_until("red")
            dot = Dot(ring.inner(0), radius=0.1, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), ring_flash(ring.circles[0]), run_time=0.8)
            for i, cue in enumerate(["red and amber", "then green", "then amber", "back to red"]):
                c.wait_until(cue)
                nxt = (i + 1) % 4
                self.play(dot.animate.move_to(ring.inner(nxt)), ring_flash(ring.circles[nxt]), run_time=0.8)
            self.dot = dot

            c.wait_until("clock")
            clk_tag = VGroup(T("CLK only,", 34, YELLOW), T("no inputs", 34, YELLOW)).arrange(DOWN, buff=0.15)
            clk_tag.move_to(_p(5.5, 1.35))
            self.play(*appear(clk_tag), run_time=1.0)
            self.clk_tag = clk_tag

            c.wait_until("four")
            quote = T("For 1 hot, we need 1 FF for each state, i.e., 4 in this case", 32, FG).move_to(_p(0, 3.35))
            self.play(*appear(quote), run_time=1.0)  # early: the slide's sentence, shown whole as it is read
            self.quote = quote
            c.wait_until("four flip-flops")
            units = [VGroup(R.ffs[i], R.labels[i], R.heads[i], R.bits[i]) for i in range(4)]   # cells always show their digit
            self.play(*appear(*units, lag=0.2), run_time=min(1.8, 0.9 * c.until("names")))
            # the units were only grouped for the entrance: put the pieces back as separate objects
            for u in units:
                self.remove(u)
                self.add(*u)

            for i, cue in enumerate(["call them the red", "red-and-amber", "green and amber", "amber flip-flops"]):
                c.wait_until(cue)
                self.play(R.labels[i].animate.set_color(GREEN), FlashAround(R.cells[i], color=GREEN),
                          run_time=0.8)

            c.wait_until("perstate")
            minis = VGroup(*[mini_ff(n, col, -5.8 + 1.3 * k, 0.0) for k, (n, col) in enumerate(zip("RAG", LAMP_COLS))])
            tag = VGroup(T("one per state", 32, FG), T("(Part 1: one per lamp)", 28, DIM)) \
                .arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            tag.next_to(minis, UP, buff=0.25).align_to(minis, LEFT)
            self.play(*appear(tag), *during(appear(minis, shift=None), 0.3, 1.0), run_time=1.3)  # early: the tag's aside, "lamp" ends the line
            self.tag, self.minis = tag, minis

    # ------------------------------------------------------------------------------------ c4.ring.2
    def clip2(self):
        ring, codes3, R = self.ring, self.codes3, self.R
        with self.say("c4.ring.2") as c:
            self.play(*flash(codes3, color=GREEN, time_width=1.5), *disappear(self.quote, self.clk_tag, self.dot),
                      run_time=1.2)
            c.wait_until("now each code")
            self.play(*disappear(self.tag, self.minis), *[FadeOut(m, shift=0.6 * UP) for m in codes3], run_time=1.0)
            self.play(ring.animate.scale(RING2_S / RING1_S).move_to(RING2_C),
                      run_time=min(2.0, c.until("red is") - 0.1))

            codes = [place_code(ring, i, t, 30) for i, t in enumerate(ONEHOT)]
            self.codes = codes

            def fly_code(k, rt):
                """The cells' pattern is read out beside its state: the cells and the state flash together."""
                self.play(*flash(R.bits, color=GOLD, time_width=1.5), ring_flash(ring.circles[k]),
                          *during(appear(codes[k], shift=0.2 * LEFT if k == 3 else 0.2 * RIGHT), 0.25, 1.0),
                          run_time=rt)

            c.wait_until("red is")
            fly_code(0, 1.3)
            c.wait_until("red and amber is")
            R.step(self, run_time=0.7, flash=False, settle_group=False)
            fly_code(1, 1.1)
            c.wait_until("and so on")
            left = c.until("table")
            rt = max(0.5, (left - 0.2) / 4)
            R.step(self, run_time=rt, flash=False, settle_group=False)
            fly_code(2, rt)
            R.step(self, run_time=rt, flash=False, settle_group=False)
            fly_code(3, rt)

            # ---- the transition table
            c.wait_until("table")
            heads = [T(n, 34, GREEN) for n in NAMES] + [T(n + "′", 34, GREEN) for n in NAMES]
            for k, h in enumerate(heads):
                h.move_to(_p(col_x(k), HEAD_Y))
            rule = Line(_p(col_x(0) - 0.4, HEAD_Y - 0.33), _p(col_x(7) + 0.4, HEAD_Y - 0.33)).set_stroke(DIM, 2)
            div_x = (col_x(3) + col_x(4)) / 2
            div = Line(_p(div_x, HEAD_Y + 0.25), _p(div_x, ROW0_Y - 3 * ROW_P - 0.3)).set_stroke(DIM, 2)

            def row_digits(code, half, r):
                m = Mono("  ".join(code), ROW_SIZE, FG, t2c={"1": GOLD})
                return m.shift(_p(col_x(4 * half), ROW0_Y - r * ROW_P) - m[0].get_center() * np.array([1, 0, 0])
                               - m.get_center() * np.array([0, 1, 0]))

            cur = [row_digits(ONEHOT[r], 0, r) for r in range(4)]
            nxt = [row_digits(ONEHOT[(r + 1) % 4], 1, r) for r in range(4)]
            self.play(*appear(*heads, lag=0.06, shift=None), FadeIn(rule), FadeIn(div),  # early: table header, read as the rows arrive
                      run_time=0.8)
            anims = []
            for r in range(4):       # each row comes in as its state on the ring lights up
                w0, w1 = 0.2 * r, 0.2 * r + 0.36
                anims += [*during([ring_flash(ring.circles[r]), FlashAround(codes[r], color=GREEN)], w0, min(1.0, w1 + 0.04)),
                          *during(appear(cur[r], nxt[r], shift=0.2 * RIGHT, lag=0.3), w0 + 0.05, w1)]
            self.play(*anims, run_time=min(3.0, max(1.5, c.until("wrap") - 0.1)))
            c.wait_until("wrap")
            a0 = _p(col_x(7) + 0.3, ROW0_Y - 3 * ROW_P)
            a1 = _p(col_x(7) + 0.3, ROW0_Y)
            wrap = CurvedArrow(a0, a1, angle=PI / 2).set_stroke(YELLOW, 3)
            wrap.set_fill(YELLOW, 1)
            self.play(Create(wrap), *flash([nxt[3], cur[0]], color=YELLOW, time_width=1.5), run_time=1.2)
            R.step(self, run_time=0.8, flash=False, settle_group=False)

            c.wait_until("unused")
            sixteen = T("16 − 4 = 12", 34, GOLD)
            unused = T("Unused states. Lots!", 34, FG)
            VGroup(unused, sixteen).arrange(RIGHT, buff=0.6).move_to(_p(TX, 0.3))
            self.play(*appear(sixteen), run_time=1.0)
            c.wait_until("that leaves twelve")
            self.play(*appear(unused), run_time=1.0)  # early: the slide's words, "lots" ends the line
            self.table = dict(heads=heads, rule=rule, div=div, cur=cur, nxt=nxt, wrap=wrap)
            self.unused = [unused, sixteen]

    # ------------------------------------------------------------------------------------ c4.ring.3
    def clip3(self):
        tb, R = self.table, self.R
        cur, nxt = tb["cur"], tb["nxt"]
        with self.say("c4.ring.3") as c:
            c.wait_until("with dee flip-flops")
            left = _p(col_x(4) - 0.25, ROW0_Y - 3 * ROW_P - 0.25)
            right = _p(col_x(7) + 0.25, ROW0_Y - 3 * ROW_P - 0.25)
            brace = span_brace(left, right, direction=DOWN, color=BLUE)
            dtag = T("= D inputs", 32, BLUE).next_to(brace, DOWN, buff=0.06)
            self.play(*during(disappear(*self.unused), 0, 0.45), *during([GrowFromCenter(brace)], 0.4, 0.8),
                      *during(appear(dtag, shift=None), 0.5, 1.0), run_time=1.5)
            c.wait_until("just the next state")
            half = VGroup(*tb["heads"][4:], *nxt)
            self.play(FlashAround(half, color=BLUE, time_width=1.5), run_time=1.5)

            def col_box(k):
                glyphs = VGroup(tb["heads"][k], *[(cur if k < 4 else nxt)[r][k % 4] for r in range(4)])
                return SurroundingRectangle(glyphs, color=YELLOW, buff=0.1).set_stroke(YELLOW, 2) \
                    .set_fill(YELLOW, 0.12).set_z_index(-1)

            c.wait_until("dra")
            box_n, box_c = col_box(5), col_box(0)
            self.play(FadeIn(box_n), FadeIn(box_c), run_time=1.0)
            eqs = [eq_tex("a", "g"), eq_tex("g", "ra"), eq_tex("ra", "r"), eq_tex("r", "a")]
            for e, k in zip(eqs, [3, 2, 1, 0]):      # each over its own flip-flop
                e.scale(42 / 46).move_to(_p(R.cells[k].get_x(), -0.52))
            c.wait_until("exactly the current")
            self.play(*appear(eqs[2]), run_time=1.0)
            c.wait_until("so the red-and-amber")
            self.play(FlashAround(R.ffs[0].q_l, color=GREEN, time_width=1.5),
                      FlashAround(R.ffs[1].d_l, color=BLUE, time_width=1.5), run_time=1.4)
            self.boxes, self.eqs, self.brace, self.dtag = (box_n, box_c), eqs, brace, dtag
            self.col_box = col_box

    # ------------------------------------------------------------------------------------ c4.ring.4
    def clip4(self):
        tb, R, ring = self.table, self.R, self.ring
        box_n, box_c = self.boxes
        eqs, col_box = self.eqs, self.col_box
        with self.say("c4.ring.4") as c:
            # (cue, next column, current column, equation, Q of, D of)
            for cue, kn, kc, e, src, dst in [("dg", 6, 1, 1, 1, 2), ("da", 7, 2, 0, 2, 3), ("dr", 4, 3, 3, 3, 0)]:
                c.wait_until(cue)
                rt = min(1.2, max(0.6, c.until() - 0.1)) if cue != "dr" else 1.2
                if cue == "da":
                    rt = min(0.9, max(0.6, c.until("dr") - 0.05))
                self.play(Transform(box_n, col_box(kn)), Transform(box_c, col_box(kc)), *appear(eqs[e]),
                          FlashAround(R.ffs[src].q_l, color=GREEN), FlashAround(R.ffs[dst].d_l, color=BLUE),
                          run_time=rt)

            # ---- the ring of four
            c.wait_until("shift")
            self.play(*flash(eqs, color=YELLOW, time_width=1.5), run_time=1.2)
            gone = [*tb["heads"], tb["rule"], tb["div"], *tb["cur"], *tb["nxt"], tb["wrap"], box_n, box_c,
                    *eqs, self.brace, self.dtag, *self.codes]
            self.play(*disappear(*gone), FadeOut(ring), run_time=0.8)
            v = (R4_Y - ROW_Y) * UP
            for m in [*R.wires, R.clk]:
                m.shift(v)
            parts = [*R.ffs, *R.labels, *R.heads, *R.bits]
            self.play(*[m.animate.shift(v) for m in parts], run_time=1.3)
            small, small_codes = final_ring()
            self.play(*[Create(w) for w in R.wires], Create(R.clk_line), *appear(R.clk_label, shift=None),
                      *during([FadeIn(small, scale=0.9), *appear(*small_codes, shift=None, lag=0.1)], 0.4, 1.0),
                      run_time=1.3)
            for w in R.wires:
                self.remove(w)
            settle(self, R)
            budget = c.until("same5") - 0.15
            rts = [0.3, 0.24, 0.23, 0.23]
            for k in range(4):
                R.step(self, run_time=max(0.5, budget * rts[k] * 0.8))
                if k < 3:
                    self.wait(max(0.1, budget * rts[k] * 0.2))

            # ---- part two's ring of five, small, beside it
            c.wait_until("same5")
            five = ring_circle(_p(0, 0), S25.RING_R, bits="11000")
            five.scale(FIVE_S, about_point=ORIGIN).shift(FIVE_C)
            self.play(FadeIn(five), run_time=0.8)
            tokens = list(five.digits)
            bits = [1, 1, 0, 0, 0]
            rad = S25.RING_R * FIVE_S

            def five_step():
                anims = []
                for i, tok in enumerate(tokens):
                    th0 = PI / 2 - TAU * i / 5

                    def upd(m, a, th0=th0):
                        th = th0 - a * TAU / 5
                        m.move_to(FIVE_C + rad * np.array([np.cos(th), np.sin(th), 0]))
                    anims.append(UpdateFromAlphaFunc(tok, upd))
                new_bits = [bits[(i - 1) % 5] for i in range(5)]
                for i in range(5):
                    tgt = five.boxes[i].copy()
                    ring_cell_style(tgt, new_bits[i])
                    anims.append(Transform(five.boxes[i], tgt))
                bits[:] = new_bits
                tokens[:] = [tokens[(i - 1) % 5] for i in range(5)]
                return anims

            self.play(*five_step(), run_time=0.8)
            self.wait(0.2)
            self.play(*five_step(), run_time=0.8)
            self.wait(max(0.1, c.until() - 0.8))
            self.play(FadeOut(five), run_time=0.7)
