"""Chapter 4, scene 7: counting to nine (BCD by reset on 10). Clips c4.bcd.1 – c4.bcd.5.

Circuit: ch3_s7_recap's make_ff(bubble=True) / ripple_chain grown to four T flip-flops (outputs
Q0..Q3 GREEN), each with ch3_s6_async's RED CLR pin underneath, joined by one RED bus; ch1_s2's
and_gate on Q3 and Q1 feeds the bus. Module-level helpers for s8's recap: bcd_chain(),
mini_timeline(), light_bits().
Departure: the "column" 0000..1010 is drawn transposed (one column per count, GOLD decimal on top,
GREEN bits underneath, row headers Q3 Q2 Q1 Q0), so it fits above the circuit.
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


def poly(pts, color, width=5):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


# ---- ch3_s7_recap's make_ff (label size added for small scales) --------------------------------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0
CLR_DX = 0.55        # CLR pin 0.55 right of the clock pin (ch3_s6_async)


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(center=ORIGIN, ins=(("D", PIN_Y),), q_len=WIRE, bubble=False, lab=36):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + q_len, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    top_clk = -hb - (0.22 if bubble else 0.02)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, top_clk)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, lab, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", lab, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar(lab).move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    parts = [*in_w, q_w, qb_w, clk_w, box, tri]
    if bubble:
        bub = Circle(radius=0.1).set_stroke(FG, 3).set_fill(BG, 1).move_to(_p(0, -hb - 0.11))
        parts.append(bub)
    g = VGroup(*parts, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.q_w, g.qb_w, g.in_w = box, tri, clk_w, q_w, qb_w, in_w
    g.qb_l = qb_l
    g.labels = [*in_l, q_l, qb_l]
    g.shift(center)
    return g


# ---- ch1_s2_rslatch's AND gate ------------------------------------------------------------------
class Gate(VGroup):
    def __init__(self, body, ins, out, color=BLUE):
        super().__init__()
        body.set_stroke(color, 4).set_fill(BG, 1)
        self.body = body
        self._ins = [VectorizedPoint(_p(*q)) for q in ins]
        self._out = VectorizedPoint(_p(*out))
        self.add(body, *self._ins, self._out)

    def inp(self, i):
        return self._ins[i].get_center()

    def out(self):
        return self._out.get_center()


def and_gate(color=BLUE):
    """AND (flat back, round front), 1.3 wide x 1.2 tall. inp(0) (-0.7, 0.3), inp(1) (-0.7, -0.3),
    out() (0.6, 0)."""
    k = 0.5523 * 0.6
    b = VMobject()
    b.start_new_path(_p(-0.7, 0.6))
    b.add_line_to(_p(0.0, 0.6))
    b.add_cubic_bezier_curve_to(_p(k, 0.6), _p(0.6, k), _p(0.6, 0.0))
    b.add_cubic_bezier_curve_to(_p(0.6, -k), _p(k, -0.6), _p(0.0, -0.6))
    b.add_line_to(_p(-0.7, -0.6))
    b.add_line_to(_p(-0.7, 0.6))
    return Gate(b, [(-0.7, 0.3), (-0.7, -0.3)], (0.6, 0.0), color=color)


# ---- the four-stage ripple counter with CLR bus and the AND on Q3, Q1 -----------------------------
FF_X = (-6.45, -2.15, 2.15, 6.45)
JX = BOX_W / 2 + WIRE + 0.4          # output junction, 2.0 right of each FF centre
STUB_Y = 1.9
CLR_Y = -2.9
GATE_C = (9.75, 2.4)
RET_X = 10.75
CH_K = 0.6
CH_C = _p(0, -1.62)
LAB = 48                             # unscaled label size (x0.6 on screen)


def bcd_chain():
    """Four T flip-flops (falling-edge clocks), Q_k clocking FF k+1, RED CLR pins on one bus,
    AND(Q3, Q1) driving the bus. Parts: .base .qlabs .clr (pins + bus + label) .gate .taps
    .gate_out .nets[k] (wires carrying Q_k) .bus .pins."""
    hb = BOX_H / 2
    ffs = [make_ff(_p(x, 0), ins=(("T", PIN_Y),), bubble=True, lab=LAB) for x in FF_X]
    for f in ffs:
        f.qb_w.set_stroke(DIM)
        f.qb_l.set_color(DIM)
    ones = [MathTex("1", font_size=56, color=BLUE).next_to(f.in_w[0].get_start(), LEFT, buff=0.12)
            for f in ffs]
    nets, dots, qlabs, wires = [], [], [], []
    for k, x in enumerate(FF_X):
        jx = x + JX
        up = poly([(x + BOX_W / 2 + WIRE, PIN_Y), (jx, PIN_Y), (jx, STUB_Y)], GREEN)
        net = [ffs[k].q_w, up]
        wires.append(up)
        qlabs.append(MathTex(f"Q_{k}", font_size=LAB + 4, color=GREEN)
                     .move_to(_p(jx - 0.62, 1.35)))
        if k < 3:
            ffs[k + 1].clk_w.set_stroke(GREEN)
            down = poly([(jx, PIN_Y), (jx, -hb - EN_WIRE), (FF_X[k + 1], -hb - EN_WIRE)], GREEN)
            d = Dot(_p(jx, PIN_Y), radius=0.09, color=GREEN)
            wires.append(down)
            dots.append(d)
            net += [down, d, ffs[k + 1].clk_w]
        nets.append(net)
    clk_l = T("CLK", LAB, YELLOW).next_to(ffs[0].clk_w.get_start(), LEFT, buff=0.15)
    pins = [Line(_p(x + CLR_DX, -hb), _p(x + CLR_DX, CLR_Y)).set_stroke(RED, 5) for x in FF_X]
    bus = Line(_p(FF_X[0] + CLR_DX, CLR_Y), _p(FF_X[3] + CLR_DX, CLR_Y)).set_stroke(RED, 5)
    clr_l = T("CLR", LAB, RED).next_to(bus.get_start(), LEFT, buff=0.15)
    gate = and_gate().move_to(_p(*GATE_C))
    i0, i1, o = gate.inp(0), gate.inp(1), gate.out()
    taps = {1: poly([(FF_X[1] + JX, STUB_Y), (FF_X[1] + JX, i0[1]), (i0[0], i0[1])], GREEN),
            3: poly([(FF_X[3] + JX, STUB_Y), (FF_X[3] + JX, i1[1]), (i1[0], i1[1])], GREEN)}
    gate_out = poly([(o[0], o[1]), (RET_X, o[1]), (RET_X, CLR_Y), (FF_X[3] + CLR_DX, CLR_Y)], RED)
    base = VGroup(*ffs, *ones, *wires, *dots, clk_l)
    clr = VGroup(*pins, bus, clr_l)
    g = VGroup(base, VGroup(*qlabs), clr, gate, taps[1], taps[3], gate_out)
    g.scale(CH_K, about_point=ORIGIN).move_to(CH_C)
    g.ffs, g.base, g.qlabs, g.clr, g.pins, g.bus, g.clr_l = ffs, base, qlabs, clr, pins, bus, clr_l
    g.gate, g.taps, g.gate_out, g.nets, g.clk_l = gate, taps, gate_out, nets, clk_l
    return g


def light_bits(chain, v, taps=True):
    """Animations: every wire carrying Q_k goes bright GREEN for a 1, DIM for a 0."""
    out = []
    for k in range(4):
        col = GREEN if (v >> k) & 1 else DIM
        ms = list(chain.nets[k]) + ([chain.taps[k]] if taps and k in chain.taps else [])
        out += [m.animate.set_color(col) for m in ms]
    return out


# ---- mini timeline: 8, 9 full blocks, the reset count a thin RED sliver ---------------------------
TL_W, TL_H, SLIVER = 1.5, 0.55, 0.13


def mini_timeline(reset_at=10, w=TL_W, h=TL_H, faded=False):
    """Blocks 8, 9, (10), 0 left to right; the count that triggers the reset is a RED sliver with
    its number below. reset_at=9: 8, sliver 9, 0. .cells {value: rect}, .nums {value: label}."""
    seq = [8, 9, 10, 0] if reset_at == 10 else [8, 9, 0]
    col = DIM if faded else GOLD
    g, cells, nums = VGroup(), {}, {}
    x = 0.0
    for v in seq:
        if v == reset_at:
            r = Rectangle(width=SLIVER, height=h).set_stroke(RED, 2).set_fill(RED, 1)
            r.move_to(_p(x + SLIVER / 2, 0))
            n = T(str(v), 30, RED).next_to(r, DOWN, buff=0.12)
            x += SLIVER
        else:
            r = Rectangle(width=w, height=h).set_stroke(col, 3).set_fill(col, 0.12)
            r.move_to(_p(x + w / 2, 0))
            n = T(str(v), 34, col).move_to(r)
            x += w
        cells[v], nums[v] = r, n
        g.add(r, n)
    g.cells, g.nums = cells, nums
    return g


# ---- counting tables ------------------------------------------------------------------------------
def count_column(nbits, n, x, top=2.85, pitch=0.4, size=28, dsize=34):
    """Vertical list: GREEN bits, GOLD decimal; .rows."""
    rows = []
    for v in range(n):
        b = Mono(format(v, f"0{nbits}b"), size, GREEN)
        d = T(str(v), dsize, GOLD).next_to(b, RIGHT, buff=0.35)
        rows.append(VGroup(b, d))
    g = VGroup(*rows)
    for i, r in enumerate(rows):
        r[0].move_to(_p(x - 0.3, top - i * pitch))
        r[1].next_to(r[0], RIGHT, buff=0.35)
        r[1].set_x(x + 0.55 + (0.09 if r[1].width < 0.15 else 0))
    g.rows = rows
    return g


def count_table(n, headers=False, dec=40, bit=32, pitch=1.0, row=0.45, gap=0.58):
    """One column per count: GOLD decimal on top, its four bits (Q3..Q0) underneath in GREEN.
    .cols[v] (VGroup dec + bits, .dec .bits), .rows[j] (bits of Q(3-j)), .heads."""
    cols, rows = [], [[] for _ in range(4)]
    for v in range(n):
        d = T(str(v), dec, GOLD).move_to(_p(v * pitch, 0))
        bs = []
        for j, b in enumerate((3, 2, 1, 0)):
            t = Mono(str((v >> b) & 1), bit, GREEN).move_to(_p(v * pitch, -gap - j * row))
            bs.append(t)
            rows[j].append(t)
        c = VGroup(d, *bs)
        c.dec, c.bits = d, bs
        cols.append(c)
    g = VGroup(*cols)
    heads = []
    if headers:
        heads = [MathTex(f"Q_{b}", font_size=bit + 10, color=GREEN).move_to(_p(-1.15, -gap - j * row))
                 for j, b in enumerate((3, 2, 1, 0))]
        g.add(*heads)
    g.cols, g.rows, g.heads = cols, rows, heads
    return g


def bit_digit(b, size=50):
    return T(str(b), size, GREEN if b else DIM)


class CountingToNine(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        with self.say("c4.bcd.1") as c:
            col3 = count_column(3, 8, x=-2.6)
            col4 = count_column(4, 16, x=2.4)
            h3 = MathTex("Q_2", r"\ Q_1", r"\ Q_0", font_size=40, color=GREEN).move_to(_p(-2.6, 3.4))
            h4 = MathTex("Q_3", r"\ Q_2", r"\ Q_1", r"\ Q_0", font_size=40, color=GREEN).move_to(_p(2.4, 3.4))
            h3.set_x(col3.rows[0][0].get_x())
            h4.set_x(col4.rows[0][0].get_x())

            def wrap(col):
                a, b = col.rows[-1].get_left() + 0.3 * LEFT, col.rows[0].get_left() + 0.3 * LEFT
                return CurvedArrow(a, b, angle=-PI / 3, color=DIM, stroke_width=3, tip_length=0.18)

            w3, w4 = wrap(col3), wrap(col4)
            self.play(*appear(h3, *col3.rows, shift=None, lag=0.12), run_time=1.4)
            self.play(*appear(h4, *col4.rows, shift=None, lag=0.06), run_time=min(1.6, c.until("Three bits")))
            c.wait_until("Three bits")
            self.play(FadeIn(w3), run_time=1.0)
            c.wait_until("four bits")
            self.play(FadeIn(w4), run_time=1.0)
            c.wait_until("bcd")
            self.play(FadeOut(col3, col4, h3, h4, w3, w4), run_time=0.8)

            quote = T("“Often we wish to have a count which is not a power of 2,\n"
                      "e.g., for a BCD counter (0 to 9)”", 34, line_spacing=1.0).move_to(_p(0, 2.7))
            self.play(*appear(quote), run_time=1.0)   # early: the slide's line, read while the voice paraphrases
            tab = count_table(10, dec=48, bit=36, pitch=1.15, row=0.5, gap=0.68)
            tab.move_to(_p(0, -1.05))
            c.wait_until("binary-coded decimal")
            self.play(*appear(*tab.cols, shift=None, lag=0.15), run_time=2.0)
            a = tab.cols[9].dec.get_top() + 0.25 * UP
            b = tab.cols[0].dec.get_top() + 0.25 * UP
            back = CurvedArrow(a, b, angle=PI / 5, color=DIM, stroke_width=3, tip_length=0.2)
            self.play(Create(back), run_time=min(1.2, c.until()))
        self.c1 = (quote, tab, back)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        with self.say("c4.bcd.2") as c:
            ch = self.chain = bcd_chain()
            quote, tab1, back = self.c1
            self.play(*during([FadeOut(quote), FadeOut(back)], 0, 0.4),
                      *during(tab1.animate.scale(0.85).move_to(_p(0.5, 2.35)), 0.4, 1), run_time=1.3)
            self.play(*appear(ch.base, shift=None), *appear(*ch.qlabs, lag=0.15),
                      run_time=min(1.3, c.until("clr")))

            b1 = T("• use FFs having a Reset/Clear input", 34)
            b2 = T("• Use an AND gate to detect the count of 10\n"
                   "   and use its output to Reset the FFs", 34, line_spacing=1.0)
            VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(_p(0, 2.55))
            c.wait_until("clr")
            self.play(*during(disappear(tab1), 0, 0.45), *during(appear(b1), 0.5, 1), run_time=1.3)
            self.play(*[GrowFromEdge(p, UP) for p in ch.pins], run_time=1.0)
            self.play(Create(ch.bus), *appear(ch.clr_l), run_time=1.0)
            c.wait_until("and")
            self.play(*appear(b2), run_time=1.2)

            c.wait_until("which")
            tab = self.tab = count_table(11, headers=True, dec=34, bit=28, pitch=1.0, row=0.45, gap=0.55)
            tab.move_to(_p(0, 2.35))
            self.play(*disappear(b1, b2), run_time=0.8)
            self.play(FadeIn(tab), run_time=1.2)

            c.wait_until("ten")
            col10 = tab.cols[10]
            self.box10 = SurroundingRectangle(col10, color=YELLOW, buff=0.12).set_stroke(YELLOW, 2)
            self.box10.set_fill(YELLOW, 0.12).set_z_index(-1)
            self.play(FadeIn(self.box10), *recolor([col10.dec, *col10.bits], YELLOW), run_time=1.5)

            c.wait_until("first")
            dimmed = tab.rows[1] + tab.rows[3] + [tab.heads[1], tab.heads[3]]
            self.play(*set_alpha(dimmed, DIMMED), run_time=1.6)

            c.wait_until("So an and gate")
            self.play(*appear(ch.gate, shift=None), Create(ch.taps[1]), Create(ch.taps[3]), run_time=1.5)
            self.play(Create(ch.gate_out), run_time=1.0)
            tag = self.tag = T("ours: the slide says only\n‘an AND gate to detect the count of 10’", 28, DIM,
                               line_spacing=0.9)
            tag.next_to(ch.gate, LEFT, buff=0.5).align_to(ch.gate, DOWN).shift(0.75 * UP)
            self.play(*appear(tag, shift=None), run_time=0.8)   # early: our side note on the gate, not spoken

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        ch, tab = self.chain, self.tab
        with self.say("c4.bcd.3") as c:
            self.play(*disappear(tab, self.box10, self.tag), run_time=0.8)

            num = T("8", 84, GOLD).move_to(_p(-4.6, 2.75))
            bits = [bit_digit((8 >> b) & 1) for b in (3, 2, 1, 0)]
            row = VGroup(*bits).arrange(RIGHT, buff=0.42).move_to(_p(-4.6, 1.55))
            heads = VGroup(*[MathTex(f"Q_{b}", font_size=32, color=DIM).next_to(d, DOWN, buff=0.18)
                             for d, b in zip(bits, (3, 2, 1, 0))])
            heads.set_y(heads[0].get_y())
            self.play(*appear(num, shift=None), *appear(*bits, shift=None, lag=0.1), FadeIn(heads),
                      *light_bits(ch, 8), run_time=1.4)

            def step(v, color=GOLD, rt=1.2):
                nonlocal num
                new = T(str(v), 84, color).move_to(num)
                anims = swap(num, new, shift=0 * UP)
                for i, b in enumerate((3, 2, 1, 0)):
                    nb = (v >> b) & 1
                    if nb != (int(bits[i].text) if hasattr(bits[i], "text") else -1):
                        d = bit_digit(nb).move_to(bits[i])
                        anims += swap(bits[i], d, shift=0 * UP)
                        bits[i] = d
                num = new
                self.play(*anims, *light_bits(ch, v), run_time=rt)

            c.wait_until("nine")
            step(9)
            c.wait_until("appears")
            step(10, RED, rt=1.5)

            c.wait_until("reset")
            pulse = ch.gate_out.copy().set_stroke(RED, 10)
            self.play(VShowPassingFlash(pulse, time_width=0.5), FlashAround(ch.gate, color=RED),
                      run_time=1.6)
            c.wait_until("the clear inputs act")
            fl = [Line(ch.bus.get_end(), ch.bus.get_start()).set_stroke(RED, 10)]
            fl += [Line(p.get_end(), p.get_start()).set_stroke(RED, 10) for p in ch.pins]
            self.play(VShowPassingFlash(fl[0], time_width=0.5), run_time=1.0)
            self.play(*[VShowPassingFlash(f, time_width=0.6) for f in fl[1:]], run_time=0.7)
            c.wait_until("drops to zero")
            step(0, rt=1.5)
            c.wait_until("without waiting")
            self.play(*set_alpha([ch.clk_l, ch.ffs[0].clk_w], 0.35), run_time=1.2)   # the clock plays no part

            c.wait_until("flash")
            tl = self.tl = mini_timeline(10).move_to(_p(2.4, 2.45))
            self.play(*appear(*[tl.cells[v] for v in (8, 9, 10, 0)],
                              *[tl.nums[v] for v in (8, 9, 10, 0)], shift=None, lag=0.1), run_time=1.5)
        self.disp = VGroup(num, *bits, heads)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        tl = self.tl
        with self.say("c4.bcd.4") as c:
            row_x = -4.6
            self.play(FadeOut(self.chain.base, *self.chain.qlabs, *self.chain.pins, self.chain.bus, self.chain.clr_l, self.chain.gate,
                              self.chain.taps[1], self.chain.taps[3], self.chain.gate_out, self.disp),
                      tl.animate.scale(1.35).move_to(_p(0.9, 1.5)), run_time=1.3)
            q = T("Why detect 10, and not 9?", 44).move_to(_p(0, -1.0))
            self.play(*appear(q), run_time=0.9)
            lab1 = T("reset at 10", 32).move_to(_p(row_x, 1.5))

            c.wait_until("held")
            nine = tl.cells[9]
            br = Brace(nine, UP, buff=0.12, color=GOLD)
            brl = T("one clock period", 30, GOLD).next_to(br, UP, buff=0.12)
            self.play(nine.animate.set_fill(GOLD, 0.45),
                      FlashAround(nine, color=GOLD, time_width=1.5), GrowFromCenter(br), run_time=1.5)
            self.play(*appear(brl), *appear(lab1, shift=None), run_time=1.0)

            c.wait_until("ifnine")
            tl2 = mini_timeline(9, w=TL_W * 1.35, h=TL_H * 1.35, faded=True)
            tl2.move_to(_p(0, -0.8)).align_to(tl, LEFT)
            lab2 = T("reset at 9", 32, DIM).move_to(_p(row_x, tl2.cells[8].get_y()))
            self.play(*disappear(q), run_time=0.7)
            self.play(*appear(lab2, shift=None), *appear(tl2, shift=None), run_time=1.3)
            r08 = T("count 0 to 8", 30, DIM).next_to(tl2, RIGHT, buff=0.4).align_to(tl2.cells[8], UP)
            r08.set_y(tl2.cells[8].get_y())
            c.wait_until("zero to eight", own_word=r08)
            self.play(*appear(r08), FlashAround(tl2.cells[9], color=RED), run_time=1.2)

            c.wait_until("glitch")
            y = -2.75
            sl = []
            for v, x in ((6, -1.2), (4, 0.0), (10, 1.2)):
                r = Rectangle(width=SLIVER * 1.35, height=TL_H * 1.35).set_stroke(RED, 2).set_fill(RED, 1)
                r.move_to(_p(x, y))
                n = T(str(v), 30, RED).next_to(r, RIGHT, buff=0.12)
                sl.append((r, n))
            fc = T("false counts", 30, RED).move_to(_p(row_x, y))
            self.play(FlashAround(tl.cells[10], color=RED, time_width=1.5),
                      *appear(sl[2][0], sl[2][1], shift=None), run_time=1.3)
            c.wait_until(own_word=fc)
            self.play(*appear(fc, shift=None), run_time=0.9)
            c.wait_until("six and four")
            self.play(*appear(sl[0][0], sl[0][1], sl[1][0], sl[1][1], shift=None, lag=0.3), run_time=1.2)

    # ------------------------------------------------------------------------------------------
    def clip5(self):
        with self.say("c4.bcd.5") as c:
            self.wait(max(0.0, c.until("simple") - 1.0))
            self.play(FadeOut(*self.mobjects), run_time=0.8)
            l1 = T("arbitrary counts: easy", 48, GREEN).move_to(_p(0, 0.7))
            l2 = T("in general: stick to synchronous designs", 48, BLUE).move_to(_p(0, -0.7))
            c.wait_until("simple")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("stick")
            self.play(*appear(l2), run_time=1.0)
