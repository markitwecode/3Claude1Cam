"""Chapter 2, scene 2: the sliding assignment: two GOLD 1s slide through c b a; codes, columns, waveforms. Clips c2.slide.1 – c2.slide.4."""
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


# ---------------------------------------------------------------- shared helpers (copy these)
SLIDE_PITCH = 2.4    # cell centre to cell centre
SLIDE_SIDE = 1.5     # cell square side
CODES = ["000", "001", "011", "110", "100"]


def _p(x, y):
    return np.array([x, y, 0.0])


def edge_tick(color=YELLOW, w=0.5, h=0.36, width=4):
    """A small rising clock edge: low, up, high."""
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [[-w / 2, -h / 2, 0], [0, -h / 2, 0], [0, h / 2, 0], [w / 2, h / 2, 0]])


def cell_bit(b, size=44):
    """What a cell holds: a GOLD travelling 1, or a DIM 0 (z 2, above the cell fill)."""
    return Mono("1", size, color=GOLD) if b else Mono("0", size, color=DIM)


class SlideRow(VGroup):
    """Three flip-flop cells c b a (a on the right), BLUE squares with GREEN names above,
    DIM arrows showing the shift direction (in at a, a->b->c, out past c).
    .cells .names .links (in, a->b, b->c, out) .items (the bits held, c b a) .bits.
    step(new) -> anims: every bit slides one cell left, c's falls off, `new` enters a;
    cells holding a 1 light faintly GOLD."""

    def __init__(self, center, **kw):
        super().__init__(**kw)
        self.cells = [Square(SLIDE_SIDE, color=BLUE, stroke_width=4).set_fill(BG, 1)
                      .move_to(center + (i - 1) * SLIDE_PITCH * RIGHT) for i in range(3)]
        self.names = [T(n, 40, color=GREEN).next_to(self.cells[i], UP, buff=0.22)
                      for i, n in enumerate("cba")]
        kw_a = dict(buff=0, color=DIM, stroke_width=3, tip_length=0.16,
                    max_tip_length_to_length_ratio=0.4)
        a_r = self.cells[2].get_right()
        c_l = self.cells[0].get_left()
        self.links = [Arrow(a_r + 0.68 * RIGHT, a_r + 0.08 * RIGHT, **kw_a)]
        for i in (1, 0):
            self.links.append(Arrow(self.cells[i + 1].get_left() + 0.08 * LEFT,
                                    self.cells[i].get_right() + 0.08 * RIGHT, **kw_a))
        self.links.append(Arrow(c_l + 0.08 * LEFT, c_l + 0.68 * LEFT, **kw_a))
        self.items, self.bits = [], [0, 0, 0]
        self.add(*self.cells, *self.names, *self.links)

    def zeros(self):
        self.items = [cell_bit(0).move_to(c).set_z_index(2) for c in self.cells]
        return self.items

    def step(self, new):
        old = self.items
        g = cell_bit(new).move_to(self.cells[2]).set_z_index(2)
        s0 = old[0].get_center()

        def leave(m, a, s0=s0):   # slides visibly out past c, fading only in the second half
            m.move_to(s0 + smooth(a) * SLIDE_PITCH * LEFT)
            m.set_opacity(1 - max(0.0, (a - 0.5) / 0.5))
        anims = [UpdateFromAlphaFunc(old[0], leave, remover=True),
                 old[1].animate.shift(SLIDE_PITCH * LEFT),
                 old[2].animate.shift(SLIDE_PITCH * LEFT),
                 FadeIn(g, shift=SLIDE_PITCH * LEFT)]
        self.items = [old[1], old[2], g]
        self.bits = self.bits[1:] + [new]
        for cell, b in zip(self.cells, self.bits):
            anims.append(cell.animate.set_fill(GOLD if b else BG, 0.22 if b else 1))
        return anims


def code_column(x, y_header, gap=0.4, pitch=0.7, codes=CODES, size=36):
    """The "c b a" code column: GREEN header letters, then one row per code, one Mono digit each
    (1s GOLD, 0s FG). gap = digit spacing (widen by moving each glyph to a wider column's spot).
    .header (3 letters) .rows (list of 3-digit VGroups) .col(k) (header letter + its digits)."""
    header = VGroup(*[T(n, 36, color=GREEN).move_to(_p(x + (i - 1) * gap, y_header))
                      for i, n in enumerate("cba")])
    for m in header[1:]:
        m.align_to(header[0], DOWN)   # one baseline (b's ascender would drop it if centred)
    rows = []
    for r, code in enumerate(codes):
        y = y_header - pitch * (r + 1)
        rows.append(VGroup(*[Mono(d, size, color=GOLD if d == "1" else FG)
                             .move_to(_p(x + (i - 1) * gap, y)) for i, d in enumerate(code)]))
    col = VGroup(header, *rows)
    col.header, col.rows = header, rows
    col.col = lambda k: VGroup(header[k], *[row[k] for row in rows])
    return col


def five_ring(center, radius=2.2):
    """Five-state ring (state_ring style): BLUE nodes clockwise from the top, GOLD state
    numbers inside, FG arrows i -> i+1, DIM "???" code slots just outside each node."""
    def dirn(i):
        a = PI / 2 - TAU * i / 5
        return np.array([np.cos(a), np.sin(a), 0.0])

    nodes, arrows, slots = [], [], []
    for i in range(5):
        p = center + radius * dirn(i)
        circ = Circle(radius=0.5, color=BLUE, stroke_width=4).set_fill(BG, 1).move_to(p)
        nodes.append(VGroup(circ, T(str(i), 34, color=GOLD).move_to(p)))
        slots.append(Mono("???", 30, color=DIM).move_to(center + (radius + 1.15) * dirn(i)))
    for i in range(5):
        p, q = center + radius * dirn(i), center + radius * dirn((i + 1) % 5)
        u = (q - p) / np.linalg.norm(q - p)
        arrows.append(Arrow(p + 0.54 * u, q - 0.54 * u, buff=0, color=FG, stroke_width=3,
                            tip_length=0.18, max_tip_length_to_length_ratio=0.4))
    ring = VGroup(VGroup(*arrows), VGroup(*nodes), VGroup(*slots))
    ring.nodes, ring.arrows, ring.slots = nodes, arrows, slots
    ring.slot_point = lambda i: center + (radius + 1.15) * dirn(i)
    return ring


def clk_wave(n, p, h=0.6, color=YELLOW, width=4):
    """CLK: n periods of length p, rising at x = k p (high first half), small ▲ on each rise.
    Built with its left end at x = 0 and its middle at y = 0: place it with .shift()."""
    lo, hi = -h / 2, h / 2
    pts = []
    for k in range(n):
        x = k * p
        pts += [[x, lo, 0], [x, hi, 0], [x + p / 2, hi, 0], [x + p / 2, lo, 0]]
    pts.append([n * p, lo, 0])
    wave = VMobject().set_points_as_corners(pts).set_stroke(color, width)
    tri = 0.1 * min(1.0, h / 0.6)
    ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1).move_to([k * p, 0, 0])
                   for k in range(n)])
    g = VGroup(wave, ups)
    g.wave = wave
    return g


def bit_wave(bits, p, h=0.6, color=GREEN, width=4):
    """A signal holding bits[k] for period k (changes on the rising edges at x = k p).
    Left end at x = 0, middle at y = 0, like clk_wave."""
    lv = lambda b: h / 2 if b else -h / 2  # noqa: E731
    pts = [[0, lv(bits[0]), 0]]
    for k in range(1, len(bits)):
        if bits[k] != bits[k - 1]:
            pts += [[k * p, lv(bits[k - 1]), 0], [k * p, lv(bits[k]), 0]]
    pts.append([len(bits) * p, lv(bits[-1]), 0])
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


# ---------------------------------------------------------------------------------------------
ROW_C = _p(1.2, 0.7)          # centre of the b cell in clips 1-2
COL_X, COL_HEAD_Y = -4.9, 1.75
TICK_Y = ROW_C[1] - 1.4


class Sliding(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- helpers --------------------------------------------------------------------------
    def drop_code(self, row, k, run_time=1.2):
        """The cells' bits flash; the code they spell fades in at the column's row k
        (no flight: a path from the row to the column would cross the edge ticks)."""
        dst = self.col.rows[k]
        self.play(*[FlashAround(m, color=GOLD if b else FG, time_width=1.5) for m, b in zip(row.items, row.bits)],
                  *during(appear(*dst, lag=0.1, shift=0.15 * DOWN), 0.35, 1), run_time=run_time)

    def col_mobs(self):
        return [*self.col.header, *[d for r in self.col.rows for d in r]]

    # -- clip 1 ---------------------------------------------------------------------------
    def clip1(self):
        with self.say("c2.slide.1") as c:
            row = self.row = SlideRow(ROW_C)
            self.col = code_column(COL_X, COL_HEAD_Y)
            self.ticks = [edge_tick().move_to(_p(ROW_C[0] + (k - 2) * 1.2, TICK_Y)) for k in range(5)]

            self.play(*appear(*row.cells, lag=0.2, shift=None), run_time=1.5)
            c.wait_until("edge of the clock")
            demo = edge_tick().move_to(_p(ROW_C[0], TICK_Y))
            self.play(*appear(demo), run_time=0.8)
            c.wait_until("passes")
            self.play(*[GrowArrow(a) for a in row.links], run_time=1.6)

            title = T("Sliding State Assignment", 50).move_to(UP * 3.2)
            c.wait_until("name")
            c.wait_until(own_word=title)
            self.play(*appear(title), *disappear(demo), run_time=1.2)

            c.wait_until("at zero")
            self.play(*appear(*row.zeros(), lag=0.15, shift=None), run_time=1.0)
            self.drop_code(row, 0, run_time=1.3)

            c.wait_until("drawn")
            self.play(*appear(*row.names, *self.col.header, lag=0.12), run_time=1.2)
            c.wait_until("on the right")
            self.play(FlashAround(row.names[2], color=GREEN, run_time=1.4, time_width=1.5),
                      FlashAround(row.cells[2], color=GREEN, run_time=1.4, time_width=1.5))

            c.wait_until("enter")
            self.play(*appear(self.ticks[0]), run_time=0.8)
            c.wait_until("a one enters")
            self.play(*row.step(1), run_time=1.6)
            self.drop_code(row, 1)

            c.wait_until("follow")
            self.play(*appear(self.ticks[1]), run_time=0.8)
            c.wait_until("slides along")
            self.play(*row.step(1), run_time=1.6)
            c.wait_until("second one")
            self.drop_code(row, 2, run_time=min(1.2, c.until(floor=0.8)))

    # -- clip 2 ---------------------------------------------------------------------------
    def clip2(self):
        row = self.row
        with self.say("c2.slide.2") as c:
            self.play(*appear(self.ticks[2]), *row.step(0), run_time=1.4)
            self.drop_code(row, 3, run_time=1.1)

            c.wait_until("drop")
            self.play(*appear(self.ticks[3]), *row.step(0), run_time=1.4)
            self.drop_code(row, 4, run_time=1.1)

            c.wait_until("empty")
            c.wait_until("drops off too")
            self.play(*appear(self.ticks[4]), *row.step(0), run_time=1.4)

            r0, r4 = self.col.rows[0], self.col.rows[4]
            self.loop = CurvedArrow(r4.get_left() + 0.2 * LEFT, r0.get_left() + 0.2 * LEFT,
                                    angle=-PI / 2, color=FG, stroke_width=3, tip_length=0.18)
            c.wait_until("back at zero")
            self.play(Create(self.loop), FlashAround(r0, run_time=1.5, time_width=1.5),
                      FlashAround(VGroup(*row.items), run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("codes")
            ring = self.ring = five_ring(_p(1.9, -0.25))
            sweep_clear(self, FadeIn(ring), keep=[*self.col_mobs(), self.loop], run_time=1.4)
            phrases = ["zero zero zero", "zero zero one", "zero one one", "one one zero", "one zero zero"]
            self.ring_codes = []
            for k, ph in enumerate(phrases):
                lab = Mono(CODES[k], 30, color=FG, t2c={"1": GOLD}).move_to(ring.slot_point(k))
                self.ring_codes.append(lab)
                c.wait_until(ph)
                rt = min(1.1, max(0.6, c.until(phrases[k + 1]) if k < 4 else 1.1))
                self.play(*swap(ring.slots[k], lab), FlashAround(self.col.rows[k], run_time=rt),
                          run_time=rt)
            self.ring.remove(self.ring[2])   # the ??? slots are gone (swapped out)
            c.wait_until("round again")
            flashes = [VShowPassingFlash(a.copy().set_stroke(YELLOW, 6), time_width=0.6) for a in ring.arrows]
            self.play(LaggedStart(*flashes, lag_ratio=0.5),
                      VShowPassingFlash(self.loop.copy().set_stroke(YELLOW, 6), time_width=0.6),
                      run_time=min(2.0, c.until(floor=0.6)))

    # -- clip 3 ---------------------------------------------------------------------------
    def clip3(self):
        with self.say("c2.slide.3") as c:
            x0, p = -1.3, 1.3
            clk = clk_wave(5, p, 0.55).shift(_p(x0, 3.05))
            out = bit_wave([1, 1, 0, 0, 0], p, 0.55).shift(_p(x0, 1.65))
            clk_l = T("CLK", 30, color=YELLOW).next_to(_p(x0, 3.05), LEFT, buff=0.3)
            out_l = T("out", 30, color=GREEN).next_to(_p(x0, 1.65), LEFT, buff=0.3)
            self.wave_small = [clk, out, clk_l, out_l]
            self.play(*during(disappear(self.ring, *self.ring_codes), 0, 0.45),
                      *during(appear(clk_l, clk, out_l, out, lag=0.15, shift=None), 0.5, 1),
                      run_time=1.8)

            c.wait_until("one in two")
            brace = span_brace(_p(x0, 2.6), _p(x0 + 2 * p, 2.6), DOWN, color=GOLD, buff=0.08)
            self.wave_small.append(brace)
            self.play(GrowFromCenter(brace), run_time=1.0)

            c.wait_until("straight from a flip-flop")
            row = self.row2 = SlideRow(_p(1.6, -1.45))
            self.play(*appear(*row.cells, *row.names, lag=0.12, shift=None),
                      *[GrowArrow(a) for a in row.links], run_time=1.4)
            self.play(*appear(*row.zeros(), shift=None), run_time=0.6)

            c.wait_until("pass")
            per = c.until("two of them") / 4
            for b in (1, 0, 0, 0):
                self.play(*row.step(b), run_time=0.62 * per)
                self.wait(0.33 * per)

            c.wait_until("two of them")
            per = c.until() / 5
            for b in (1, 1, 0, 0, 0):
                self.play(*row.step(b), run_time=0.62 * per)
                self.wait(0.3 * per)

    # -- clip 4 ---------------------------------------------------------------------------
    def clip4(self):
        with self.say("c2.slide.4") as c:
            col = self.col
            settle(self, self.row2, add=self.row2.items)   # digits clear with their cells
            wide = code_column(COL_X, COL_HEAD_Y, gap=0.85)
            moves = [time_span(m.animate.move_to(w.get_center()), 0.6, 1.6)
                     for m, w in zip(self.col_mobs(), [*wide.header, *[d for r in wide.rows for d in r]])]
            cs = T("current state", 30, color=DIM).move_to(_p(COL_X, COL_HEAD_Y + 0.7))
            sweep_clear(self, *moves, time_span(FadeIn(cs, shift=0.2 * DOWN), 0.8, 1.6),  # early: table heading, read with the columns
                        keep=self.col_mobs(), run_time=1.6)
            # the column glyphs are now at the wide spots: rebuild col's helpers on them
            col.col = lambda k: VGroup(col.header[k], *[r[k] for r in col.rows])

            box = SurroundingRectangle(col.col(2), color=GREEN, buff=0.14, stroke_width=4)
            c.wait_until("a reads")
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("bee reads")
            self.play(Transform(box, SurroundingRectangle(col.col(1), color=GREEN, buff=0.14,
                                                          stroke_width=4)), run_time=1.0)
            c.wait_until("see reads")
            self.play(Transform(box, SurroundingRectangle(col.col(0), color=GREEN, buff=0.14,
                                                          stroke_width=4)), run_time=1.0)

            # waveforms, two rounds, under one CLK
            x0, p = -2.2, 0.86
            ys = {"CLK": 2.5, "a": 1.2, "b": -0.1, "c": -1.4}
            clk = clk_wave(10, p).shift(_p(x0, ys["CLK"]))
            labs = [T(n, 30 if n == "CLK" else 36, color=YELLOW if n == "CLK" else GREEN)
                    .next_to(_p(x0, y), LEFT, buff=0.3) for n, y in ys.items()]
            seq = {"a": [0, 1, 1, 0, 0], "b": [0, 0, 1, 1, 0], "c": [0, 0, 0, 1, 1]}
            waves = [bit_wave(seq[n] * 2, p).shift(_p(x0, ys[n])) for n in "abc"]
            c.wait_until("waves")
            self.play(*disappear(box), *appear(labs[0], clk, *labs[1:], lag=0.12, shift=None),
                      run_time=1.1)
            pairs = []
            for i, (k, w) in enumerate(zip((2, 1, 0), waves)):
                pairs.append(time_span(FlashAround(col.col(k), color=GREEN, time_width=1.5),
                                       0.8 * i, 0.8 * i + 1.2))
                pairs.append(time_span(Create(w, rate_func=linear), 0.8 * i + 0.3, 0.8 * i + 1.7))
            self.play(*pairs, run_time=max(3.3, min(3.5, c.until("shift"))))

            c.wait_until("shift")
            dashes = [DashedLine(_p(x0 + k * p, 1.65), _p(x0 + k * p, -1.85), dash_length=0.1,
                                 color=DIM, stroke_width=3) for k in (1, 2, 3)]
            self.play(*[time_span(Create(d), 0.3 * i, 0.3 * i + 0.9) for i, d in enumerate(dashes)],
                      run_time=1.5)
            shifts = [Arrow(_p(x0 + p, 0.55), _p(x0 + 2 * p, 0.55), buff=0, color=GOLD, stroke_width=4,
                            tip_length=0.18, max_tip_length_to_length_ratio=0.4),
                      Arrow(_p(x0 + 2 * p, -0.75), _p(x0 + 3 * p, -0.75), buff=0, color=GOLD,
                            stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.4)]
            self.play(GrowArrow(shifts[0]), time_span(GrowArrow(shifts[1]), 0.5, 1.4), run_time=1.4)

            c.wait_until("any")
            outlines = [SurroundingRectangle(w, color=GREEN, buff=0.14, stroke_width=3) for w in waves]
            quote = T("“By inspection we can see that we can use any of the\n"
                      "FF outputs as the wanted output”", 30, slant=ITALIC).move_to(_p(0, -3.05))
            self.play(*[time_span(FadeIn(o), 0.25 * i, 0.25 * i + 1.0) for i, o in enumerate(outlines)],
                      run_time=1.5)
            self.play(*appear(quote), run_time=1.2)  # early: the notes' line, quoted not spoken
        self.wait(1.5)   # let the quote be read before the board clears
