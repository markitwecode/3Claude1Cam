"""Chapter 4, scene 6: the lecturer's demo: the one-hot ring starts at 0000 and stays dark; he sets
the amber flip-flop by hand and the lights run; the 16 patterns fall into six loops, 0101 <-> 1010
lights red with green. Clips c4.demo.1 – c4.demo.3.

Circuit: ch4_s4's onehot_circuit("0000"), with ch3_s6's clock source + switch on the CLK line and a
RED S pin with a push button on top of each flip-flop. Loops: ch3_s4's rings (nodes carrying
their codes, arrows round each loop), one per loop of the shift.
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
S25 = load_scene("ch2_s5_ring")
S35 = load_scene("ch3_s5_loops")
S6 = load_scene("ch3_s6_preset")
S43 = load_scene("ch4_s3_ring4")
S4 = load_scene("ch4_s4_outputs")
cell_bit, ring_cell_style = S25.cell_bit, S25.ring_cell_style


def _p(x, y):
    return np.array([x, y, 0.0])


K0 = 0.9                 # circuit scale, clips 1-2
K1 = 0.5                 # circuit scale once it slides aside (its text labels go)
BIT_UP = 1.45            # the bits grow by this when the circuit is small, to stay readable
ROW_Y = -1.4


NODE_R4 = 0.6            # ring nodes carrying their four-bit codes (ch3's ring style, sized down)
LOOP_GAP = 0.24


def _code(text, color, size=28):
    return Mono(text, size, color=color, t2c={"1": GOLD})


def _node(code, pos, color):
    circ = Circle(radius=NODE_R4).set_stroke(color, 3).set_fill(BG, 1).move_to(pos)
    lab = _code(code, FG if color == GREEN else DIM).move_to(pos)
    g = VGroup(circ, lab)
    g.circ, g.code = circ, lab
    return g


def _arrow(p, q, color):
    u = (q - p) / np.linalg.norm(q - p)
    return Arrow(p + (NODE_R4 + 0.04) * u, q - (NODE_R4 + 0.04) * u, buff=0, color=color, stroke_width=3,
                 tip_length=0.16, max_tip_length_to_length_ratio=0.45)


def _tipped(arc, color):
    arc.set_stroke(color, 3)
    arc.add_tip(tip_length=0.16, tip_width=0.16)
    arc.get_tip().set_fill(color, 1).set_stroke(color, 1)
    return arc


def ring4(codes, color=DIM):
    """One loop of the shift: its codes clockwise, each on a node, arrows only round itself.
    1 code: a node with a self-arrow on its left; 2: one above the other, an arc down on the right
    and one back up on the left; 4: a square, clockwise from top left. Built at ORIGIN."""
    n = len(codes)
    if n == 1:
        node = _node(codes[0], ORIGIN, color)
        c = _p(-NODE_R4 - 0.13, 0)
        arc = Arc(radius=0.3, start_angle=np.radians(305), angle=-np.radians(250), arc_center=c)
        arrows = [_tipped(arc, color)]
        nodes = [node]
    elif n == 2:
        d = 0.83
        nodes = [_node(codes[0], _p(0, d), color), _node(codes[1], _p(0, -d), color)]
        a, b = nodes[0].circ.get_center(), nodes[1].circ.get_center()
        r = NODE_R4 + 0.05

        def on(c, deg):
            t = np.radians(deg)
            return c + r * np.array([np.cos(t), np.sin(t), 0.0])
        down = _tipped(ArcBetweenPoints(on(a, -35), on(b, 35), angle=-PI / 2.2), color)
        up = _tipped(ArcBetweenPoints(on(b, 145), on(a, 215), angle=-PI / 2.2), color)
        arrows = [down, up]
    else:
        h = 0.83
        pts = [_p(-h, h), _p(h, h), _p(h, -h), _p(-h, -h)]
        nodes = [_node(cd, pt, color) for cd, pt in zip(codes, pts)]
        arrows = [_arrow(pts[k], pts[(k + 1) % 4], color) for k in range(4)]
    g = VGroup(*arrows, *nodes)
    g.nodes, g.arrows = nodes, arrows
    return g


LOOPS4 = [["0000"], ["1111"], ["1000", "0100", "0010", "0001"], ["0011", "1001", "1100", "0110"],
          ["0101", "1010"], ["0111", "1011", "1101", "1110"]]
OURS4 = 2


def loops_row4(y=ROW_Y):
    """The six loops side by side, centred on (0, y); ours GREEN; 0000 over 1111 in one column."""
    loops = [ring4(codes, GREEN if k == OURS4 else DIM) for k, codes in enumerate(LOOPS4)]
    d = 0.83
    loops[0].shift(_p(0, d) - loops[0].nodes[0].get_center())
    loops[1].shift(_p(0, -d) - loops[1].nodes[0].get_center())
    cols = [VGroup(loops[0], loops[1]), *loops[2:]]
    total = sum(m.width for m in cols) + LOOP_GAP * (len(cols) - 1)
    x = -total / 2
    for m in cols:
        m.shift(_p(x + m.width / 2, y) - _p(m.get_center()[0], 0))
        x += m.width + LOOP_GAP
    g = VGroup(*loops)
    g.loops = loops
    return g


def gap_loop(c=_p(3.55, 1.55), dx=1.65, size=48):
    """0101 <-> 1010 large: two codes, an arc over (→) and one under (←), DIM."""
    a = Mono("0101", size, t2c={"1": GOLD}).move_to(c + dx * LEFT)
    b = Mono("1010", size, t2c={"1": GOLD}).move_to(c + dx * RIGHT)
    top = ArcBetweenPoints(a.get_top() + 0.15 * UP + 0.3 * RIGHT, b.get_top() + 0.15 * UP + 0.3 * LEFT, angle=-PI / 2.4)
    bot = ArcBetweenPoints(b.get_bottom() + 0.15 * DOWN + 0.3 * LEFT, a.get_bottom() + 0.15 * DOWN + 0.3 * RIGHT,
                           angle=-PI / 2.4)
    for arc in (top, bot):
        arc.set_stroke(DIM, 4)
        arc.add_tip(tip_length=0.2, tip_width=0.2)
        arc.get_tip().set_fill(DIM, 1).set_stroke(DIM, 1)
    g = VGroup(top, bot, a, b)
    g.a, g.b, g.arcs = a, b, [top, bot]
    return g


class Demo(NarratedScene):
    def construct(self):
        self.build()
        self.clip1()
        self.clip2()
        self.clip3()
        self.tick(0.8)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- the circuit -----------------------------------------------------------------------------
    def build(self):
        C = S4.onehot_circuit("0000")
        R = C.ring
        y = R.clk_line.get_y()
        src = S6.clock_source().move_to(_p(-6.15, y))
        sw = S6.toggle(1, YELLOW).scale(0.75).move_to(_p(-5.15, y)).set_z_index(2)
        lead = Line(src.get_right(), sw.get_left()).set_stroke(YELLOW, 5)
        R.clk_line.put_start_and_end_on(sw.get_right(), R.clk_line.get_end())
        R.clk_label.next_to(src, UP, buff=0.18)
        hz = T("1 Hz", 30, YELLOW).next_to(src, DOWN, buff=0.18)
        for m in (*R.labels, *R.heads):      # make room for the S pin left of each name
            m.shift(0.14 * RIGHT)
        pins, btns = [], []
        for ff in R.ffs:
            p = S6.pin(ff, "S", size=32, length=1.85)
            b = S6.place_button(S6.push_button(ff.box.width / S6.BOX_W), p.end)
            pins.append(p)
            btns.append(b)
        clock = VGroup(src, hz, lead, sw)
        G = VGroup(C, *pins, *btns, clock)
        clkp = Line(src.get_right(), R.clk_line.get_end())
        aux = VGroup(*R.wire_paths, clkp)
        self.C, self.R, self.G, self.aux, self.clkp = C, R, G, aux, clkp
        self.src, self.sw, self.hz, self.lead, self.clock = src, sw, hz, lead, clock
        self.pins, self.btns = pins, btns
        self.k = 1.0
        self.kb = 1.0          # extra scale of the bits
        self.place(K0, _p(0, -0.2))

    def place(self, k, target, animate=False, run_time=1.8, extra=()):
        G, aux = self.G, self.aux
        c0 = G.get_center()
        f = k / self.k
        if animate:
            self.play(G.animate.scale(f).move_to(target), *extra, run_time=run_time)
        else:
            G.scale(f).move_to(target)
        aux.scale(f, about_point=c0).shift(target - c0)
        self.k = k

    def detach(self, m):
        for parent in self.G.get_family():
            if m in parent.submobjects:
                parent.remove(m)

    def resettle(self):
        self.remove(*self.G.get_family())
        self.add(self.G)

    def clk_after(self):
        return [self.R.clk_line, *[f.clk_w for f in self.R.ffs]]

    def pulse(self):
        return VShowPassingFlash(self.clkp.copy().set_stroke(YELLOW, 10), time_width=0.5, taper_width=0.1)

    def tick(self, rt=0.8, extra=()):
        """One clock edge: the GOLD 1 moves one cell on, the lamps follow."""
        R, C = self.R, self.C
        i = R.values.index(1)
        j = (i + 1) % 4
        old_i, old_j = R.bits[i], R.bits[j]
        new_i = cell_bit(0, S43.R4_BIT).scale(self.k * self.kb).move_to(old_i)
        new_j = cell_bit(1, S43.R4_BIT).scale(self.k * self.kb).move_to(old_j)
        ti, tj = R.cells[i].copy(), R.cells[j].copy()
        ring_cell_style(ti, 0)
        ring_cell_style(tj, 1)
        p = R.wire_paths[i].copy().move_to(R.wires[i]).set_stroke(GOLD, 7)
        self.play(*swap(old_i, new_i, shift=None), *swap(old_j, new_j, shift=None),
                  Transform(R.cells[i], ti), Transform(R.cells[j], tj),
                  VShowPassingFlash(p, time_width=0.6, taper_width=0.1), self.pulse(), *C.light(j), *extra,
                  run_time=rt)
        R.values[i], R.values[j] = 0, 1
        R.bits[i], R.bits[j] = new_i, new_j
        R.remove(old_i, old_j)
        R.add(new_i, new_j)
        self.resettle()

    def zero_edge(self, rt):
        """An edge at 0000: each 0 slides into the next cell (a's 0 round to r) and lands as 0."""
        R = self.R
        b = list(R.bits)
        d = b[1].get_center() - b[0].get_center()
        new0 = b[0].copy()
        fb = R.wire_paths[3].copy().move_to(R.wires[3]).set_stroke(FG, 6)
        self.play(*[b[i].animate.shift(d) for i in range(3)],
                  FadeOut(b[3], shift=0.35 * d), FadeIn(new0, shift=0.35 * d),
                  self.pulse(), VShowPassingFlash(fb, time_width=0.6, taper_width=0.1), run_time=rt)
        R.bits = [new0, b[0], b[1], b[2]]
        R.remove(b[3])
        R.add(new0)
        self.resettle()

    # ---- c4.demo.1: built, ticking, dark; 0000 is unused; zeros shift into zeros ------------------
    def clip1(self):
        C, R, G = self.C, self.R, self.G
        tag = T("the lecturer's simulator", 34, DIM).move_to(_p(0, 3.3))
        q = T("?", 96, YELLOW).move_to(_p(4.6, -2.3))
        with self.say("c4.demo.1") as c:
            self.play(*during(appear(tag), 0, 0.5), FadeIn(C, lag_ratio=0.0), run_time=1.4)
            self.play(*appear(*self.pins, *self.btns, self.clock, lag=0.08), run_time=1.4)
            c.wait_until("run")
            self.play(*[time_span(self.pulse(), 0.95 * k, 0.95 * k + 0.9) for k in range(3)],
                      run_time=min(2.8, c.until("why") - 0.05))
            c.wait_until("why")
            self.play(*appear(q), run_time=0.9)
            c.wait_until("zeros")
            quote = T("“same deal as before”", 36, FG, slant=ITALIC).move_to(tag)
            self.play(*[FlashAround(b, color=YELLOW, time_width=1.5) for b in R.bits],
                      *recolor(R.bits, YELLOW), run_time=1.3)
            self.play(*swap(tag, quote), run_time=1.2)
            unused = VGroup(Mono("0000", 36, YELLOW), T("unused", 32, DIM)).arrange(RIGHT, buff=0.25)
            unused.move_to(q).align_to(_p(3.75, 0), LEFT)
            c.wait_until("unused")
            self.play(*swap(q, unused), run_time=1.2)
            c.wait_until("shift")
            self.zero_edge(1.6)
            self.wait(0.5)
            self.zero_edge(1.0)
        self.quote, self.unused = quote, unused

    # ---- c4.demo.2: clock off; set a by hand (active low); amber lights at once; release ----------
    def clip2(self):
        C, R = self.C, self.R
        with self.say("c4.demo.2") as c:
            self.play(S6.flip(self.sw, 0), *[m.animate.set_stroke(DIM) for m in self.clk_after()], run_time=1.2)
            self.play(*disappear(self.quote), *recolor(R.bits, DIM), run_time=1.0)
            c.wait_until("any")
            self.play(*[time_span(FlashAround(VGroup(p.bub, p.wire), color=YELLOW, time_width=1.5),
                                  0.35 * k, 0.35 * k + 1.0) for k, p in enumerate(self.pins)], run_time=2.1)
            pa, ba = self.pins[3], self.btns[3]
            lvl = value_label("1", 40, GOLD).next_to(pa.label, LEFT, buff=0.2)
            c.wait_until("picks")
            self.play(FlashAround(R.labels[3], color=YELLOW, time_width=1.5), *appear(lvl), run_time=1.2)
            c.wait_until("low")
            lvl0 = value_label("0", 40, RED).move_to(lvl)
            self.play(S6.press(ba), *swap(lvl, lvl0), run_time=1.2)
            c.wait_until("little circle")
            ring = Circle(radius=0.2).set_stroke(YELLOW, 4).move_to(pa.bub)
            self.play(GrowFromCenter(ring), FlashAround(pa.bub, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("amber")
            old = R.bits[3]
            one = cell_bit(1, S43.R4_BIT).scale(self.k).move_to(old)
            ta = R.cells[3].copy()
            ring_cell_style(ta, 1)
            self.play(*swap(old, one, shift=None), Transform(R.cells[3], ta), *disappear(ring), run_time=1.2)
            R.values[3] = 1
            R.bits[3] = one
            R.remove(old)
            R.add(one)
            self.resettle()
            used = VGroup(Mono("0001", 36, FG, t2c={"1": GOLD}), T("used", 32, GREEN)).arrange(RIGHT, buff=0.25)
            used.move_to(self.unused, aligned_edge=LEFT)
            c.wait_until("amber lamp")
            wa = C.in_wires[1][1].copy().set_stroke(GOLD, 8)
            wo = C.out_wires[1].copy().set_stroke(GOLD, 8)
            self.play(time_span(VShowPassingFlash(wa, time_width=0.6), 0, 0.8),
                      time_span(VShowPassingFlash(wo, time_width=0.8), 0.6, 1.1),
                      *[time_span(a, 0.9, 1.4) for a in C.light(3)], run_time=1.4)
            self.play(*swap(self.unused, used), run_time=1.2)  # early: the readout updates with the state
            c.wait_until("release")
            lvl1 = value_label("1", 40, GOLD).move_to(lvl0)
            self.play(S6.press(ba, False), *swap(lvl0, lvl1), run_time=1.2)
        self.lvl, self.used = lvl1, used

    # ---- c4.demo.3: clock back; the lights run; six loops; the gap loop; start in a used state ----
    def clip3(self):
        C, R = self.C, self.R
        with self.say("c4.demo.3") as c:
            self.play(S6.flip(self.sw, 1), *[m.animate.set_stroke(YELLOW) for m in self.clk_after()],
                      *disappear(self.lvl, self.used), run_time=1.0)
            self.resettle()
            c.wait_until("go")
            c.wait_until("amber")
            self.play(FlashAround(C.lamps[1], color=YELLOW, time_width=1.5), run_time=0.8)
            c.wait_until("red")
            self.tick(0.8)
            c.wait_until("red and amber")
            self.tick(0.7)
            c.wait_until("green")
            self.tick(0.7)
            c.wait_until("amber", nth=2)
            self.tick(0.7)

            c.wait_until("trap")
            w, h = self.G.width * K1 / self.k, self.G.height * K1 / self.k
            texts = [*C.dsubs, *[f.d_l for f in R.ffs], *[f.q_l for f in R.ffs], *R.labels, R.clk_label,
                     self.hz, *[p.label for p in self.pins], *C.lamp_labels]
            self.play(*[FadeOut(m) for m in texts], run_time=1.0)
            for m in texts:
                self.detach(m)
            self.resettle()
            w, h = self.G.width * K1 / self.k, self.G.height * K1 / self.k
            self.place(K1, _p(-6.5 + w / 2, 3.6 - h / 2), animate=True, run_time=1.6)
            self.play(*[b.animate.scale(BIT_UP) for b in R.bits], run_time=0.6)
            self.kb = BIT_UP
            c.wait_until("way back")
            self.tick(0.7)
            c.wait_until("goes round")
            self.tick(0.7)

            c.wait_until("loops")
            row = loops_row4()
            self.play(*appear(*row.loops, lag=0.15), run_time=1.8)  # early: the six loops, shown whole
            ours = row.loops[2]
            c.wait_until("ours")
            self.tick(0.8, extra=[FlashAround(ours, color=GREEN, time_width=1.5)])

            c.wait_until("gap")
            big = gap_loop()
            src = row.loops[4]
            others = [m for k, m in enumerate(row.loops) if k != 4]
            self.play(src.animate.scale(1.15).move_to(_p(src.get_x(), big.get_y() + 0.1)), *set_alpha(others, 0.4), run_time=1.3)
            self.play(ReplacementTransform(src.nodes[0].code, big.a), ReplacementTransform(src.nodes[1].code, big.b),
                      *[FadeOut(m) for m in (*src.arrows, *[nd.circ for nd in src.nodes])],
                      *during([FadeIn(m) for m in big.arcs], 0.5, 1), run_time=1.2)
            self.remove(*src.get_family())
            self.add(big)
            c.wait_until("for ever")
            self.tick(0.7)
            ha = S1.lamp_column((1, 1, 0), scale=0.95).next_to(big.a, LEFT, buff=0.3)
            hb = S1.lamp_column((1, 0, 1), scale=0.95).next_to(big.b, RIGHT, buff=0.3)
            bang = T("!", 72, YELLOW).next_to(hb, UP, buff=0.2)
            c.wait_until("red with amber")
            self.play(*appear(ha), FlashAround(big.a, color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("red with green")
            self.play(*appear(hb), FlashAround(big.b, color=YELLOW, time_width=1.5), run_time=1.0)
            self.play(*appear(bang), run_time=0.8)

            line = T("start it in a used state", 40, FG, t2c={"used state": GREEN}).move_to(_p(0, -3.35))
            c.wait_until(own_word=line)
            self.play(*appear(line), run_time=1.0)
            self.tick(0.8, extra=[FlashAround(ours, color=GREEN, time_width=1.5)])
