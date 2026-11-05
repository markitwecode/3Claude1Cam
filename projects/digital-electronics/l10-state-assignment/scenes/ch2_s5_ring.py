"""Chapter 2, scene 5: the shift-register (ring) assignment for the divide-by-5. Clips c2.ring.1 – c2.ring.3."""
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


# ---------------------------------------------------------------------------------------------
# Shared visuals owned by this scene (s6 brings the circle and table back, s8 copies the circle).
# ---------------------------------------------------------------------------------------------
RING = "abcde"
RING_STATES = ["00011", "00110", "01100", "11000", "10001"]   # e d c b a, one per clock state
RING_R = 1.75          # circle radius (cell centres)
RING_CELL = 0.85       # square cell side
CIRCLE_C = np.array([-3.6, 0.2, 0.0])
TABLE_C = np.array([3.4, 0.1, 0.0])


def _dirn(i, n=5):
    a = PI / 2 - TAU * i / n
    return np.array([np.cos(a), np.sin(a), 0.0])


def bit_color(b):
    return GOLD if int(b) else DIM


def ring_cell_style(box, bit):
    """s2's cell look (ch2_s2_sliding.py SlideRow): BLUE border; a cell holding a 1 lights faintly
    GOLD, otherwise BG fill. bit None = empty cell."""
    box.set_stroke(BLUE, 4)
    return box.set_fill(GOLD, 0.22) if bit is not None and int(bit) else box.set_fill(BG, 1)


def cell_bit(b, size=44):
    """What a cell holds (s2's cell_bit): a GOLD travelling 1, or a DIM 0."""
    return Mono("1", size, color=GOLD) if int(b) else Mono("0", size, color=DIM)


def ring_circle(center=CIRCLE_C, R=RING_R, bits=None):
    """Five square flip-flop cells a..e clockwise from 12 o'clock round a circle.

    .boxes[i] (RoundedRectangle), .labels[i] (GREEN italic letter, just outside its cell),
    .arrows[0..3] a->b->c->d->e (FG), .close e->a (YELLOW), .digits[i] (T 40, only if `bits` is a
    string in a..e order), .pos(i) cell centre, .center, .R. bits=None leaves the cells empty."""
    center = np.array(center, dtype=float)
    pos = [center + R * _dirn(i) for i in range(5)]
    boxes, labels, digits, arrows = [], [], [], []
    for i in range(5):
        b = RoundedRectangle(corner_radius=0.12, width=RING_CELL, height=RING_CELL).move_to(pos[i])
        ring_cell_style(b, None if bits is None else bits[i])
        boxes.append(b)
        labels.append(T(RING[i], 38, color=GREEN).move_to(center + (R + 0.75) * _dirn(i)))
        if bits is not None:
            digits.append(cell_bit(bits[i], 40).move_to(pos[i]))
    for i in range(5):
        p, q = pos[i], pos[(i + 1) % 5]
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + 0.56 * u, q - 0.56 * u, buff=0, color=YELLOW if i == 4 else FG,
                            stroke_width=4 if i == 4 else 3, tip_length=0.2,
                            max_tip_length_to_length_ratio=0.4))
    g = VGroup(*arrows, *boxes, *labels, *digits)
    g.boxes, g.labels, g.digits, g.arrows, g.close = boxes, labels, digits, arrows[:4], arrows[4]
    g.pos = lambda i: pos[i]
    g.center, g.R = center, R
    return g


def ring_table(center=TABLE_C, rows=5):
    """The ring's transition table (p. 137), styled as s3's slide_table(): titles "Current state" /
    "Next state" (T 30 FG) over the blocks, header e d c b a | e′ d′ c′ b′ a′ (GREEN T 36), `rows`
    rows of Mono 36 digits (1s GOLD, 0s FG), DIM stroke-2 rules.

    .titles (VGroup of 2), .head_l / .head_r (VGroups of 5 GREEN letters), .hline, .vline,
    .cur[k][j] / .nxt[k][j] the digit of row k, column j (j = 0 is e, 4 is a). .row_y(k) row k's y."""
    c = np.array(center, dtype=float)
    lx = [c[0] - 3.1 + 0.6 * j for j in range(5)]
    rx = [c[0] + 0.7 + 0.6 * j for j in range(5)]
    hy = c[1] + 1.75
    ry = [c[1] + 0.7 - 0.7 * k for k in range(5)]
    titles = VGroup(T("Current state", 30).move_to([lx[2], hy + 0.65, 0]),
                    T("Next state", 30).move_to([rx[2] + 0.04, hy + 0.65, 0]))
    head_l = VGroup(*[T(RING[4 - j], 36, color=GREEN).move_to([lx[j], hy, 0]) for j in range(5)])
    head_r = VGroup(*[T(RING[4 - j] + "′", 36, color=GREEN).move_to([rx[j] + 0.08, hy, 0])
                      for j in range(5)])
    for m in [*head_l, *head_r]:
        m.align_to(head_l[0], DOWN) if m is not head_l[0] else None
    hline = Line([lx[0] - 0.4, hy - 0.42, 0], [rx[4] + 0.45, hy - 0.42, 0]).set_stroke(DIM, 2)
    vline = Line([c[0], hy + 0.35, 0], [c[0], ry[rows - 1] - 0.4, 0]).set_stroke(DIM, 2)

    def digit(d, x, y):
        return Mono(d, 36, color=GOLD if d == "1" else FG).move_to([x, y, 0])
    cur, nxt = [], []
    for k in range(rows):
        s, t = RING_STATES[k], RING_STATES[(k + 1) % 5]
        cur.append([digit(s[j], lx[j], ry[k]) for j in range(5)])
        nxt.append([digit(t[j], rx[j], ry[k]) for j in range(5)])
    g = VGroup(titles, head_l, head_r, hline, vline, *[d for r in cur + nxt for d in r])
    g.titles, g.head_l, g.head_r, g.hline, g.vline, g.cur, g.nxt = titles, head_l, head_r, hline, vline, cur, nxt
    g.row_y = lambda k: ry[k]
    return g


def ring_wave(bits, x0, width, y, height=0.55, color=GREEN):
    """Waveform of one flip-flop over the five states (bits[i] = value in state i), aligned with a
    clock_wave(width, periods=5) whose left end is x0: state i holds from rising edge i to i+1;
    before the first edge it shows the last state's value."""
    p = width / 5.5
    lo, hi = y - height / 2, y + height / 2
    lev = lambda b: hi if int(b) else lo  # noqa: E731
    xs = [x0] + [x0 + p / 2 + p * i for i in range(5)] + [x0 + width]
    vals = [bits[4]] + list(bits)
    pts = []
    for i, v in enumerate(vals):
        pts += [[xs[i], lev(v), 0], [xs[i + 1], lev(v), 0]]
    w = VMobject().set_points_as_corners(pts).set_stroke(color, 4)
    return w


# s1's five-state ring (ch2_s1_hook.py five_ring, copied verbatim).
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


# ClockWave: L6 ch1_s3_clock.py's clock (copied verbatim, trimmed to the parts used here).
class ClockWave(VGroup):
    def __init__(self, width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True,
                 down_arrows=False, stroke_width=4, **kw):
        super().__init__(**kw)
        p = width / (periods + 0.5)
        x0, lo, hi = -width / 2, -height / 2, height / 2
        pts, self._rise, self._fall = [[x0, lo, 0]], [], []
        x = x0 + p / 2
        for _ in range(periods):
            pts += [[x, lo, 0], [x, hi, 0]]
            self._rise.append(x - x0)
            x += p / 2
            pts += [[x, hi, 0], [x, lo, 0]]
            self._fall.append(x - x0)
            x += p / 2
        pts.append([x0 + width, lo, 0])
        self.wave = VMobject().set_points_as_corners(pts).set_stroke(color, stroke_width)
        self.period, self._width = p, width
        tri = 0.11 * min(1.0, height / 0.7)
        self.ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1)
                            .move_to([x0 + r, 0, 0]) for r in (self._rise if up_arrows else [])])
        self.downs = VGroup()
        self.add(self.wave, self.ups, self.downs)

    def rising_x(self, i):
        return self.wave.get_left()[0] + self._rise[i] * self.wave.width / self._width


def clock_wave(width=9.9, height=0.7, periods=5, color=YELLOW, up_arrows=True, down_arrows=False):
    return ClockWave(width, height, periods, color, up_arrows, down_arrows)


def _cue(c, phrase, fallback=None):
    """A spoken phrase as a cue, falling back to a mark if the re-voiced line lost it."""
    try:
        c.at(phrase)
        return phrase
    except KeyError:
        return fallback


class RingAssignment(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c2.ring.1: the quote, the ring closing, data cycling -----------------------------------
    def clip1(self):
        ring = ring_circle()
        self.ring = ring
        with self.say("c2.ring.1") as c:
            title = T("Shift Register Assignment", 48).to_edge(UP, buff=0.45)
            self.title = title
            c.wait_until(own_word=title)
            self.play(*appear(title), run_time=1.0)
            quote = T("“an even more egregious use of flip-flops”", 40, slant=ITALIC)
            card = RoundedRectangle(corner_radius=0.2, width=quote.width + 0.9,
                                    height=quote.height + 0.8).set_stroke(DIM, 2)
            VGroup(quote, card).move_to(0.3 * DOWN)
            self.play(FadeIn(card), *appear(quote), run_time=1.2)  # early: the lecturer's words, read straight after the title
            c.wait_until("ring")
            self.quote = VGroup(card, quote)
            self.play(*during([self.quote.animate.scale(0.7).move_to([2.8, 2.5, 0])], 0, 0.45),
                      *during(appear(*[VGroup(b, l) for b, l in zip(ring.boxes, ring.labels)], lag=0.15),
                              0.3, 1.0),
                      *during([GrowArrow(a) for a in ring.arrows], 0.55, 1.0),
                      run_time=min(2.0, c.until("close")))
            self.cells = [VGroup(b, l) for b, l in zip(ring.boxes, ring.labels)]
            c.wait_until("close")
            self.play(GrowArrow(ring.close), run_time=1.5)
            b1 = T("• the output from the final shift register\n"
                   "   in the chain is connected to the input\n"
                   "   of the first FF:", 28, line_spacing=0.9)
            b2 = T("– Consequently the data continuously\n"
                   "   cycles through the register", 28, color=DIM, line_spacing=0.9)
            VGroup(b1, b2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([2.95, 0.1, 0])
            self.bullets = [b1, b2]
            self.play(*appear(b1), run_time=1.0)
            c.wait_until("cycle")
            sweep = Arc(radius=RING_R, start_angle=PI / 2, angle=-TAU, arc_center=ring.center)
            sweep.set_stroke(GOLD, 8, opacity=0.6)
            self.play(VShowPassingFlash(sweep, time_width=0.35), *appear(b2),  # early: slide bullet, shown with its paraphrase
                      run_time=min(3.0, c.until() - 0.1), rate_func=linear)

    # -- c2.ring.2: the pair of 1s, the clock, the table ---------------------------------------
    def clip2(self):
        ring, title = self.ring, self.title
        tab = ring_table()
        self.tab = tab
        tokens = [cell_bit(b, 40).move_to(ring.pos(i)) for i, b in enumerate("11000")]
        bits = [1, 1, 0, 0, 0]
        clock = clock_wave(width=3.8, height=0.5, periods=5).move_to([-3.2, -2.75, 0])
        clk_lab = Mono("CLK", 30, color=YELLOW).next_to(clock, LEFT, buff=0.3)
        mark = marker(YELLOW, scale=0.2)

        def step(k):
            """Animations for the k-th clock edge (k = 0..4): every token one cell round."""
            anims = []
            for i, tok in enumerate(tokens):
                th0 = PI / 2 - TAU * i / 5

                def upd(m, a, th0=th0):
                    th = th0 - a * TAU / 5
                    m.move_to(ring.center + RING_R * np.array([np.cos(th), np.sin(th), 0]))
                anims.append(UpdateFromAlphaFunc(tok, upd))
            new_bits = [bits[(i - 1) % 5] for i in range(5)]
            for i in range(5):
                tgt = ring.boxes[i].copy()
                ring_cell_style(tgt, new_bits[i])
                anims.append(Transform(ring.boxes[i], tgt))
            bits[:] = new_bits
            tokens[:] = [tokens[(i - 1) % 5] for i in range(5)]
            x = clock.rising_x(k)
            if k == 0:
                mark.move_to([x, clock.get_top()[1] + 0.25, 0])
                anims += appear(mark, shift=0.15 * DOWN)
            else:
                anims.append(mark.animate.move_to([x, mark.get_y(), 0]))
            return anims

        def read_off(k):
            """Copy the circle's current state into row k's current-state digits (e d c b a)."""
            ones = [ring.boxes[i].copy() for i in range(5) if bits[i]]
            return [*flash(ones, color=GOLD, time_width=1.5),
                    *appear(*reversed(tab.cur[k]), lag=0.15, shift=None)]

        with self.say("c2.ring.2") as c:
            c.wait_until("pair")
            box_t = []
            for i in range(5):
                t = ring.boxes[i].copy()
                ring_cell_style(t, bits[i])
                box_t.append(Transform(ring.boxes[i], t))
            self.play(*box_t, *appear(*tokens, lag=0.12, shift=None),
                      run_time=min(1.5, 0.6 * c.until("neighbours")))
            nb = _cue(c, "neighbours")
            if nb:
                c.wait_until(nb)
            self.play(*flash([VGroup(ring.boxes[0].copy(), ring.boxes[1].copy())], color=GOLD,
                             run_time=1.5, time_width=1.5))
            c.wait_until("step")
            self.play(*appear(clk_lab, clock, lag=0.2, shift=None), run_time=1.0)
            arcs = []
            for i in (0, 1):
                th = PI / 2 - TAU * i / 5 - 0.18          # inside the circle, clear of cells and labels
                a = Arc(radius=RING_R - 0.8, start_angle=th, angle=-(TAU / 5 - 0.36), arc_center=ring.center)
                a.add_tip(tip_length=0.18)
                a.set_stroke(GOLD, 7)
                a.tip.set_stroke(width=0).set_fill(GOLD, 1)
                arcs.append(a)
            self.play(*[Create(a) for a in arcs], run_time=1.0)
            self.play(*[FadeOut(a) for a in arcs], run_time=0.6)

            c.wait_until("table")
            self.play(*during([FadeOut(m) for m in [*self.bullets, self.quote]], 0, 0.45),  # early: table headings, part of the table shown on "table"
                      *during(appear(tab.titles[0], tab.titles[1], tab.head_l, tab.head_r, lag=0.15, shift=None), 0.45, 1.0),
                      *during([GrowFromCenter(tab.hline), GrowFromCenter(tab.vline)], 0.5, 1.0),
                      run_time=1.6)
            right = _cue(c, "on the right", "table")
            c.wait_until(right)
            self.play(*flash([tab.head_l[4], ring.labels[0]], color=YELLOW, run_time=1.4, time_width=1.5))
            first = _cue(c, "first state", "table")
            c.wait_until(first)
            self.play(*read_off(0), run_time=1.6)
            nxt = _cue(c, "next is", "wrap")
            c.wait_until(nxt)
            self.play(*step(0), *appear(*tab.nxt[0], lag=0.08, shift=None), run_time=1.5)
            self.wait(0.6)
            self.play(*read_off(1), run_time=min(1.4, 0.7 * c.until("wrap")))

            c.wait_until("wrap")
            wraps = _cue(c, "wraps round", None)
            span = (c.until(wraps) if wraps else 0.5 * c.until()) - 0.2
            rt = max(0.7, span / 3.4)
            self.play(*step(1), *appear(*tab.nxt[1], lag=0.08, shift=None), run_time=rt)
            self.wait(0.2 * rt)
            self.play(*read_off(2), run_time=rt)
            self.play(*step(2), *appear(*tab.nxt[2], lag=0.08, shift=None), run_time=rt)
            self.wait(0.2 * rt)
            self.play(*read_off(3), run_time=rt)
            if wraps:
                c.wait_until(wraps)
            self.play(*step(3), *appear(*tab.nxt[3], lag=0.08, shift=None), run_time=1.2)
            row4 = VGroup(*[d.copy() for d in tab.cur[3] + tab.nxt[3]])
            wrap_box = SurroundingRectangle(row4, color=YELLOW, buff=0.14).set_stroke(YELLOW, 2)
            self.wrap_box = wrap_box
            self.play(FadeIn(wrap_box), *flash([tab.cur[3][0], tab.nxt[3][4]], color=YELLOW,
                                               run_time=1.4, time_width=1.5), run_time=1.4)
            self.play(*read_off(4), run_time=min(1.2, max(0.5, c.until("after five steps") - 0.1))
                      if _cue(c, "after five steps") else 1.0)
            five = _cue(c, "after five steps", None)
            if five:
                c.wait_until(five)
            self.play(*step(4), *appear(*tab.nxt[4], lag=0.08, shift=None), run_time=1.0)
            home = VGroup(*[d.copy() for d in tab.nxt[4]])
            start = VGroup(*[d.copy() for d in tab.cur[0]])
            self.play(*flash([home, start, VGroup(ring.boxes[0].copy(), ring.boxes[1].copy())],
                             color=GOLD, run_time=min(1.3, max(0.6, c.until())), time_width=1.5))
        self.tokens, self.clock, self.clk_lab, self.mark = tokens, clock, clk_lab, mark

    # -- c2.ring.3: the count, the five phases, any output -------------------------------------
    def clip3(self):
        tab = self.tab
        with self.say("c2.ring.3", gap=3.0) as c:
            c.wait_until("count")
            l1 = T("5 flip-flops", 38)
            l2 = MathTex(r"\lceil \log_2 5 \rceil = 3", font_size=44, color=FG)
            VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-4.3, -2.75, 0])
            brace = Brace(VGroup(l1, l2), RIGHT, buff=0.3, color=GOLD)
            plus = T("+2", 40, color=GOLD).next_to(brace, RIGHT, buff=0.25)
            self.play(*during(disappear(self.clock, self.clk_lab, self.mark), 0, 0.45),
                      *during(appear(l1), 0.45, 1.0), run_time=1.4)
            two = _cue(c, "two more", "phase")
            c.wait_until(two)
            self.play(*appear(l2), run_time=0.9)
            self.play(GrowFromCenter(brace), *appear(plus, shift=0.2 * LEFT), run_time=1.0)

            c.wait_until("phase")
            block = [tab.titles[0], tab.head_l, *[d for r in tab.cur for d in r]]
            sweep_clear(self, keep=[*block, l1, l2, brace, plus], run_time=1.0)
            # current-state block to the left; CLK and five waveforms on the right
            v = np.array([-4.4, 0.85, 0]) - VGroup(*block).get_center()
            x0, W = 0.1, 6.2
            clk = clock_wave(width=W, height=0.55, periods=5)
            clk.move_to([x0 + W / 2, 3.0, 0])
            clk_l = Mono("CLK", 30, color=YELLOW).move_to([-0.6, 3.0, 0])
            ys = [2.15, 1.3, 0.45, -0.4, -1.25]
            waves, labs = [], []
            for i in range(5):          # rows a..e
                col = 4 - i             # table column of flip-flop i
                seq = "".join(RING_STATES[k][col] for k in range(5))
                waves.append(ring_wave(seq, x0, W, ys[i]))
                labs.append(T(RING[i], 36, color=GREEN, slant=ITALIC).move_to([-0.5, ys[i], 0]))
            self.play(*[m.animate.shift(v) for m in block],
                      *during(appear(clk_l, clk, lag=0.2, shift=None), 0.5, 1.0), run_time=1.4)
            cols = [VGroup(*[tab.cur[k][4 - i].copy() for k in range(5)]) for i in range(5)]
            self.play(LaggedStart(*[AnimationGroup(FadeIn(labs[i]), Create(waves[i]),
                                                   FlashAround(cols[i], color=GREEN, time_width=1.5))
                                    for i in range(5)], lag_ratio=0.3),
                      run_time=min(3.2, c.until("any") - 2.0))
            ring5 = five_ring(RING_STATES, radius=1.2)
            for i, code in enumerate(RING_STATES):      # codes a size up, so they read at 28 once scaled
                old, new = ring5.codes[i], ring5.code_at(i, code, size=34)
                ring5[2].remove(old)
                ring5[2].add(new)
                ring5.codes[i] = new
            ring5.scale(0.84).to_edge(LEFT, buff=0.5).set_y(1.0)
            c.wait_until(_cue(c, "different point", "any"))
            self.play(*swap(VGroup(*block), ring5), run_time=min(1.4, c.until("any")))

            c.wait_until("any")
            outlines = [SurroundingRectangle(w, buff=0.12, corner_radius=0.08).set_stroke(GREEN, 2.5)
                        for w in waves]
            note = T("“By inspection we can see that we\n"
                     "can use any of the FF outputs\n"
                     "as the wanted output”", 30, line_spacing=0.9)
            note.move_to([x0 + W / 2, -2.75, 0])
            self.play(*[FadeIn(o) for o in outlines], *appear(note), run_time=1.2)  # early: slide text, shown with its paraphrase
