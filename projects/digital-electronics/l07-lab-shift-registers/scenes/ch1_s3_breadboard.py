"""Chapter 1, scene 3: which holes on a breadboard are joined. Clips c1.board.1 – c1.board.4.

Shared drawing (s1, s4, s6, s7, s8 copy it): `Breadboard` (holes `hole(row, col)`,
`rail_hole(rail, col)`, strips `col_strip(col, row)` / `rails[i]`, `trench`, `pitch()`),
`dip_chip(board, col, pins, label)` (a `DipChip` seated astride the trench, pin 1 bottom left in
column `col`), `power_strip(...)` (the white bench supply strip), plus `wire`, `resistor`, `led`.
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

# ── the breadboard drawing (shared) ─────────────────────────────────────────────
P_NOM = 0.36            # hole pitch at scale 1
BOARD_WHITE = "#F2F2EE"
HOLE_GREY = "#B4B8BE"
TRENCH_LIGHT = "#D6D8DB"
TRENCH_DARK = "#2A2D33"
CHIP_BODY = "#1C1D21"
PIN_GREY = "#C9CDD2"
UNPOW = "#A9AEB6"       # a power row with nothing feeding it
FAINT = 0.3             # strip opacity when merely "visible under the plastic"
WIRE_DARK = "#202227"
LEG_GREY = "#8C9096"


class Breadboard(VGroup):
    """A breadboard centred on ORIGIN. Rows 0-4: the bank above the trench (top to bottom),
    rows 5-9: the bank below. Rails 0-3: the long power rows, top to bottom (0, 1 above the
    banks; 2, 3 below). Columns 0..cols-1 left to right. Strips (TEAL metal under the plastic)
    start invisible; `rail_breaks` = rail indices whose strip is split halfway (p. 6's drawing)."""

    def __init__(self, cols=26, pitch=P_NOM, rail_breaks=(1,), **kw):
        super().__init__(**kw)
        p, k = pitch, pitch / P_NOM
        self.n_cols = cols
        xs = [(c - (cols - 1) / 2) * p for c in range(cols)]
        bank_y = [(5 - r) * p for r in range(5)] + [-(r - 4) * p for r in range(5, 10)]
        rail_y = [8.0 * p, 6.6 * p, -6.6 * p, -8.0 * p]
        w, h = (cols - 1) * p + 2 * 1.39 * p, 17.6 * p
        sw = 0.24 * k                                   # strip width
        self.body = RoundedRectangle(corner_radius=0.12 * k, width=w, height=h)
        self.body.set_fill(BOARD_WHITE, 1).set_stroke(width=0)
        self.trench = Rectangle(width=w - 0.5 * p, height=0.94 * p)
        self.trench.set_fill(TRENCH_LIGHT, 1).set_stroke(width=0)

        def strip(x0, x1, y0, y1):
            r = RoundedRectangle(corner_radius=0.05 * k, width=x1 - x0, height=y1 - y0)
            return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0]).set_fill(TEAL, 0).set_stroke(width=0)

        self.columns_top = [strip(x - sw / 2, x + sw / 2, bank_y[4] - sw / 2, bank_y[0] + sw / 2) for x in xs]
        self.columns_bot = [strip(x - sw / 2, x + sw / 2, bank_y[9] - sw / 2, bank_y[5] + sw / 2) for x in xs]
        self.rails = []
        mid = cols // 2
        for i, y in enumerate(rail_y):
            if i in rail_breaks:
                halves = [strip(xs[0] - sw / 2, xs[mid - 1] + sw / 2, y - sw / 2, y + sw / 2),
                          strip(xs[mid] - sw / 2, xs[-1] + sw / 2, y - sw / 2, y + sw / 2)]
            else:
                halves = [strip(xs[0] - sw / 2, xs[-1] + sw / 2, y - sw / 2, y + sw / 2)]
            self.rails.append(VGroup(*halves))
        self.break_col = mid            # the right half starts at this column

        def hole(x, y):
            return Square(side_length=0.15 * k).move_to([x, y, 0]).set_fill(HOLE_GREY, 1).set_stroke(width=0)

        self.grid = [[hole(x, y) for x in xs] for y in bank_y]
        self.rail_holes = [[hole(x, y) for x in xs] for y in rail_y]
        self.add(self.body, self.trench, *self.columns_top, *self.columns_bot, *self.rails,
                 *[s for row in self.grid for s in row], *[s for row in self.rail_holes for s in row])

    # coordinates follow the board wherever it has been moved or scaled
    def hole(self, row, col):
        return self.grid[row][col].get_center()

    def rail_hole(self, rail, col):
        return self.rail_holes[rail][col].get_center()

    def pitch(self):
        return float(np.linalg.norm(self.hole(0, 1) - self.hole(0, 0)))

    def trench_y(self):
        return self.trench.get_center()[1]

    def col_strip(self, col, row):
        return (self.columns_top if row < 5 else self.columns_bot)[col]

    def all_strips(self):
        return [*self.columns_top, *self.columns_bot, *self.rails]


def fill_to(mobs, color, op=1.0):
    """Animations recolouring strips (or any filled parts) one by one."""
    return [m.animate.set_fill(color, opacity=op) for m in mobs]


class DipChip(VGroup):
    """A DIP chip built on ORIGIN at hole pitch `pitch`: near-black body, PINK notch at the left
    end, light-grey pins; pin 1 bottom left, 1..n/2 along the bottom left to right, the rest along
    the top right to left. `.pin(n)` is pin n's mobject."""

    def __init__(self, pins=14, label="74HC00", pitch=P_NOM, **kw):
        super().__init__(**kw)
        n, p, k = pins // 2, pitch, pitch / P_NOM
        bw, bh = (n - 1) * p + 0.9 * p, 1.6 * p
        self.body = RoundedRectangle(corner_radius=0.06 * k, width=bw, height=bh)
        self.body.set_fill(CHIP_BODY, 1).set_stroke("#3A3C42", 1.5)
        r, lx = 0.3 * p, -bw / 2
        pts = [[lx + r * np.cos(a), r * np.sin(a), 0] for a in np.linspace(-PI / 2, PI / 2, 25)]
        self.notch = Polygon(*pts).set_fill(PINK, 1).set_stroke(width=0)

        def pin(x, y):
            return Rectangle(width=0.42 * p, height=0.45 * p).move_to([x, y, 0]).set_fill(PIN_GREY, 1).set_stroke("#555A60", 1)

        xs = [(i - (n - 1) / 2) * p for i in range(n)]
        self.pins = [pin(x, -0.93 * p) for x in xs] + [pin(x, 0.93 * p) for x in reversed(xs)]
        self.label = T(label, size=max(28, 28 * k), color=FG).move_to(ORIGIN)
        self.add(*self.pins, self.body, self.notch, self.label)

    def pin(self, n):
        return self.pins[n - 1]


def dip_chip(board, col, pins=14, label="74HC00"):
    """A chip seated astride the trench of `board`, pin 1 in column `col` (row 5), pin n in row 4."""
    p = board.pitch()
    chip = DipChip(pins, label, pitch=p)
    x0 = board.hole(5, col)[0] + (pins // 2 - 1) / 2 * p
    return chip.shift([x0, board.trench_y(), 0])


def chip_columns(board, col, pins=14):
    """The strips the chip's pins sit in, in pin order 1..pins."""
    n = pins // 2
    return [board.col_strip(col + i, 5) for i in range(n)] + [board.col_strip(col + n - 1 - j, 4) for j in range(n)]


def power_strip(center, height, col_gap=0.95, n=17):
    """The white bench power strip: two columns of holes (left 0 V, right 5 V) with strips
    (`.cols[0]`, `.cols[1]`, invisible until filled) and `.hole(side, k)`."""
    g = VGroup()
    g.body = RoundedRectangle(corner_radius=0.1, width=col_gap + 0.6, height=height)
    g.body.set_fill(BOARD_WHITE, 1).set_stroke(width=0).move_to(center)
    cx = [center[0] - col_gap / 2, center[0] + col_gap / 2]
    ys = np.linspace(center[1] - height / 2 + 0.2, center[1] + height / 2 - 0.2, n)
    g.cols = [RoundedRectangle(corner_radius=0.05, width=0.24, height=height - 0.2).move_to([x, center[1], 0])
              .set_fill(TEAL, 0).set_stroke(width=0) for x in cx]
    g.holes = [[Square(side_length=0.13).move_to([x, y, 0]).set_fill(HOLE_GREY, 1).set_stroke(width=0) for y in ys]
               for x in cx]
    g.add(g.body, *g.cols, *[h for col in g.holes for h in col])
    g.hole = lambda side, kk: g.holes[side][kk].get_center()

    def nearest(side, y):
        return min((h.get_center() for h in g.holes[side]), key=lambda q: abs(q[1] - y))
    g.nearest = nearest
    return g


def wire(p1, p2, color, angle=0.0, width=7, ends=(True, True)):
    """A jumper wire from p1 to p2 (an arc if angle != 0), dark-edged so it reads on white."""
    path = ArcBetweenPoints(p1, p2, angle=angle) if angle else Line(p1, p2)
    path.set_stroke(color, width)
    path.set_stroke(WIRE_DARK, width + 3, background=True)
    dots = [Dot(q, radius=0.06, color=LEG_GREY) for q, e in zip((p1, p2), ends) if e]
    return VGroup(path, *dots)


def resistor(p1, p2, scale=1.0):
    """A resistor lying between two holes: legs, beige body, three colour bands, leg ends."""
    p1, p2 = np.array(p1), np.array(p2)
    mid = (p1 + p2) / 2
    bw, bh = 0.62 * scale, 0.24 * scale
    body = RoundedRectangle(corner_radius=0.1 * scale, width=bw, height=bh).move_to(mid)
    body.set_fill("#D8C08E", 1).set_stroke("#6E5A3A", 1.5)
    bands = VGroup(*[Rectangle(width=0.06 * scale, height=bh).move_to(mid + RIGHT * dx * scale)
                     .set_fill(c, 1).set_stroke(width=0)
                     for dx, c in ((-0.17, "#7B4A2A"), (-0.05, "#111111"), (0.07, "#D33A2A"))])
    legs = VGroup(Line(p1, mid + LEFT * bw / 2), Line(mid + RIGHT * bw / 2, p2)).set_stroke(LEG_GREY, 3)
    g = VGroup(legs, body, bands, Dot(p1, radius=0.06, color=LEG_GREY), Dot(p2, radius=0.06, color=LEG_GREY))
    g.ends = [g[3], g[4]]
    return g


def led(p1, p2, scale=1.0):
    """An LED seen from above: red dome just above its two legs (in holes p1, p2)."""
    p1, p2 = np.array(p1), np.array(p2)
    c = (p1 + p2) / 2 + UP * 0.34 * scale
    dome = Circle(radius=0.2 * scale).move_to(c).set_fill("#E03A3A", 1).set_stroke("#8E1F1F", 2)
    shine = Circle(radius=0.06 * scale).move_to(c + (UL * 0.07 * scale)).set_fill(WHITE, 0.6).set_stroke(width=0)
    legs = VGroup(Line(p1, c + DL * 0.12 * scale), Line(p2, c + DR * 0.12 * scale)).set_stroke(LEG_GREY, 3)
    g = VGroup(legs, dome, shine, Dot(p1, radius=0.06, color=LEG_GREY), Dot(p2, radius=0.06, color=LEG_GREY))
    g.ends = [g[3], g[4]]
    return g


WIRE_BLUE = "#3B7DD8"
WIRE_GREEN = "#2E9E5B"
CHIP_COL = 9        # chip 1's pin 1 column
CHIP2_COL = 17      # chip 2 (on the far half of the broken rail)
ZOOM = 0.82
ZOOM_SHIFT = np.array([1.25, -0.15, 0])
LED_DARK = "#3E7A2E"


def green_led(p1, p2, scale=1.0):
    """This chapter's LEDs are GREEN: led() recoloured (led() itself is shared, left as is)."""
    g = led(p1, p2, scale)
    g[1].set_fill(GREEN, 1).set_stroke(LED_DARK, 2)
    return g


def join_rail(board, i):
    """Scene-only: show rail i as one continuous strip (the break opens later with split_rail)."""
    rail = board.rails[i]
    left, right = rail[0], rail[-1]
    full = RoundedRectangle(corner_radius=0.05, width=right.get_right()[0] - left.get_left()[0], height=left.height)
    full.move_to([(left.get_left()[0] + right.get_right()[0]) / 2, left.get_y(), 0])
    full.set_fill(TEAL, 0).set_stroke(width=0)
    rail.remove(*rail.submobjects)
    rail.add(full)


def split_rail(board, i):
    """Scene-only, no animation: replace the continuous rail i by its two halves, same colour,
    the gap between columns break_col-1 and break_col; returns (left, right)."""
    rail = board.rails[i]
    full = rail[0]
    k = board.pitch() / P_NOM
    sw = 0.24 * k
    x_l = board.rail_hole(i, board.break_col - 1)[0] + sw / 2
    x_r = board.rail_hole(i, board.break_col)[0] - sw / 2
    y, h = full.get_y(), full.height
    col, op = full.get_fill_color(), full.get_fill_opacity()

    def piece(x0, x1):
        return (RoundedRectangle(corner_radius=0.05 * k, width=x1 - x0, height=h).move_to([(x0 + x1) / 2, y, 0])
                .set_fill(col, op).set_stroke(width=0))
    halves = [piece(full.get_left()[0], x_l), piece(x_r, full.get_right()[0])]
    rail.remove(full)
    rail.add(*halves)
    return halves


class BreadboardScene(NarratedScene):
    def construct(self):
        self.board = Breadboard()
        join_rail(self.board, 1)        # every rail reads continuous until {split}
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.board.1: under the plastic; rows; columns of five; anything in a column is joined
    def clip1(self):
        b = self.board
        with self.say("c1.board.1") as c:
            self.play(FadeIn(b), run_time=1.0)
            self.play(b.body.animate.set_fill(BOARD_WHITE, opacity=0.9),
                      *fill_to([*b.columns_top, *b.columns_bot, *b.rails], TEAL, FAINT),
                      run_time=min(1.5, c.until("rows")))
            c.wait_until("rows")
            flashes = [VShowPassingFlash(Line(b.rail_hole(i, 0) + LEFT * 0.15, b.rail_hole(i, b.n_cols - 1) + RIGHT * 0.15)
                                         .set_stroke(YELLOW, 7), time_width=0.5) for i in range(4)]
            self.play(*fill_to(b.rails, TEAL, 1.0), *flashes, run_time=1.8)
            c.wait_until("columns")
            self.play(*fill_to(b.rails, TEAL, FAINT),
                      LaggedStart(*[AnimationGroup(*fill_to([t, u], TEAL, 1.0))
                                    for t, u in zip(b.columns_top, b.columns_bot)], lag_ratio=0.06),
                      run_time=1.5)
            x = b.body.get_left()[0] - 0.3
            self.nums = [T(str(r + 1), 30, GOLD).move_to([x, b.hole(r, 0)[1], 0]) for r in range(5)]
            c.wait_until("five")
            self.play(*appear(*self.nums, shift=None, lag=0.2),
                      FlashAround(b.columns_top[0], color=YELLOW, run_time=1.0), run_time=1.0)
            c.wait_until("joined")
            col = CHIP_COL
            self.res = resistor(b.hole(3, col), b.hole(3, col + 3))
            self.play(*fill_to([s for s in [*b.columns_top, *b.columns_bot] if s is not b.columns_top[col]], TEAL, FAINT),
                      b.columns_top[col].animate.set_fill(TEAL, opacity=FAINT),
                      FadeIn(self.res, shift=0.2 * DOWN), run_time=1.0)
            h = b.hole(0, col)
            self.wire1 = wire(h + LEFT * 1.6 + UP * (3.5 - h[1]), h, WIRE_BLUE, angle=-0.7, ends=(False, True))
            c.wait_until("connected")
            self.play(FadeIn(self.wire1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("everything else")
            self.play(b.columns_top[col].animate.set_fill(TEAL, opacity=1.0),
                      self.res.ends[0].animate.set_color(TEAL),
                      FlashAround(b.columns_top[col], color=YELLOW, time_width=1.5),
                      FlashAround(self.res.ends[0], color=YELLOW, time_width=1.5, buff=0.08),
                      run_time=min(1.5, c.until()))

    # c1.board.2: the trench; a chip astride it; facing pins stay apart
    def clip2(self):
        b = self.board
        with self.say("c1.board.2") as c:
            self.play(*disappear(self.res, self.wire1, *self.nums),
                      b.columns_top[CHIP_COL].animate.set_fill(TEAL, opacity=FAINT),
                      b.trench.animate.set_fill(TRENCH_DARK, 1), run_time=1.2)
            y = b.trench_y()
            self.play(VShowPassingFlash(Line([b.body.get_left()[0] + 0.2, y, 0], [b.body.get_right()[0] - 0.2, y, 0])
                                        .set_stroke(YELLOW, 6), time_width=0.4),
                      run_time=min(1.6, c.until("chip")))
            c.wait_until("chip")
            self.chip = dip_chip(b, CHIP_COL)
            self.play(FadeIn(self.chip, shift=0.5 * DOWN), run_time=1.2)
            cols = chip_columns(b, CHIP_COL)
            self.play(LaggedStart(*[s.animate.set_fill(TEAL, opacity=1.0) for s in cols], lag_ratio=0.25),
                      run_time=min(2.0, c.until("apart")))
            c.wait_until("apart")
            top, bot = b.col_strip(CHIP_COL + 2, 4), b.col_strip(CHIP_COL + 2, 5)
            self.apart = T("not joined", 28, FG).move_to([0, y, 0])
            self.apart.next_to(self.chip.body, RIGHT, buff=0.3).set_y(y)
            self.play(*fill_to([s for s in cols if s not in (top, bot)], TEAL, FAINT),
                      bot.animate.set_fill(PURPLE, opacity=1.0),
                      *during(appear(self.apart, shift=None), 0.4, 1), run_time=1.6)

    # c1.board.3: the power strip, jumpers, missing / pulled jumpers, a broken rail
    def clip3(self):
        b, chip = self.board, self.chip
        with self.say("c1.board.3") as c:
            chip.generate_target()
            chip.target.scale(ZOOM, about_point=ORIGIN).shift(ZOOM_SHIFT)
            chip.target.label.scale(1 / ZOOM)        # the marking stays readable (size 28)
            zoom = [m.animate.scale(ZOOM, about_point=ORIGIN).shift(ZOOM_SHIFT) for m in (b,)]
            self.play(*during(disappear(self.apart), 0, 0.3), *during([*zoom, MoveToTarget(chip)], 0.2, 1),
                      run_time=1.7)
            self.play(*fill_to([*b.columns_top, *b.columns_bot], TEAL, FAINT),
                      *fill_to(b.rails, UNPOW, 0.6), run_time=0.8)
            top, bot = b.body.get_top()[1], b.body.get_bottom()[1]
            ps = power_strip([-4.6, (top + bot) / 2, 0], top - bot)
            self.ps = ps
            self.play(FadeIn(ps, shift=0.3 * RIGHT), run_time=min(1.0, c.until("left column")))
            lab0 = T("0 V", 30, DIM).next_to(ps.cols[0], UP, buff=0.25)
            lab5 = T("5 V", 30, GOLD).next_to(ps.cols[1], UP, buff=0.25).align_to(lab0, DOWN)
            c.wait_until("zero volts")
            self.play(ps.cols[0].animate.set_fill(DIM, opacity=1.0), *appear(lab0), run_time=1.0)
            c.wait_until("five volts")
            self.play(ps.cols[1].animate.set_fill(GOLD, opacity=1.0), *appear(lab5), run_time=1.0)
            self.ps_labels = [lab0, lab5]

            # rails: 0 = top outer 0 V, 1 = top inner 5 V, 2 = bottom inner 0 V, 3 = bottom outer 5 V
            volts = {0: (0, DIM, "0 V"), 1: (1, GOLD, "5 V"), 2: (0, DIM, "0 V"), 3: (1, GOLD, "5 V")}
            self.jumpers, self.row_labels = {}, {}
            rx = b.body.get_right()[0] + 0.25
            for i, (side, col, txt) in volts.items():
                end = b.rail_hole(i, 0)
                self.jumpers[i] = wire(ps.nearest(side, end[1]), end, col, width=6)
                self.row_labels[i] = T(txt, 28, col).move_to([0, end[1], 0]).align_to([rx, 0, 0], LEFT)
            c.wait_until("jumpers")
            self.play(*appear(self.jumpers[0], self.jumpers[1], shift=0.2 * DOWN, lag=0.3), run_time=1.2)
            self.play(b.rails[0].animate.set_fill(DIM, opacity=1.0), b.rails[1].animate.set_fill(GOLD, opacity=1.0),
                      *appear(self.row_labels[0], self.row_labels[1], shift=None), run_time=1.0)
            p14 = wire(b.hole(0, CHIP_COL), b.rail_hole(1, CHIP_COL), GOLD, width=6)
            p7 = wire(b.hole(9, CHIP_COL + 6), b.rail_hole(2, CHIP_COL + 6), DIM, width=6)
            self.pwires = [p14, p7]
            c.wait_until("every chip needs both")
            self.play(*appear(p14, p7, shift=None, lag=0.4),
                      FlashAround(chip.pin(14), color=YELLOW, buff=0.06),
                      FlashAround(chip.pin(7), color=YELLOW, buff=0.06), run_time=1.4)

            c.wait_until("missing")
            add = T("add jumpers", 30, YELLOW).move_to([-3.3, bot - 0.42, 0])
            self.play(*appear(add, shift=0.2 * UP), *flash(list(b.rails[2:]), color=YELLOW, buff=0.06), run_time=1.0)
            self.play(*appear(self.jumpers[2], self.jumpers[3], shift=0.2 * DOWN, lag=0.3), run_time=1.0)
            self.play(b.rails[2].animate.set_fill(DIM, opacity=1.0), b.rails[3].animate.set_fill(GOLD, opacity=1.0),
                      *appear(self.row_labels[2], self.row_labels[3], shift=None), run_time=0.9)

            c.wait_until("pulled")
            chk = T("check first", 30, YELLOW).move_to([-1.4, top + 0.38, 0])
            j0 = self.jumpers[0]
            self.play(FadeOut(j0, shift=0.5 * UP),
                      b.rails[0].animate.set_fill(UNPOW, opacity=0.6), run_time=0.9)
            self.play(*appear(chk, shift=0.2 * DOWN), run_time=0.8)
            self.play(FadeIn(j0, shift=0.5 * DOWN), b.rails[0].animate.set_fill(DIM, opacity=1.0),
                      run_time=min(0.9, c.until("split")))

            c.wait_until("split")
            _, right = split_rail(b, 1)
            gap = Rectangle(width=b.pitch(), height=0.25).move_to(
                (b.rail_hole(1, b.break_col - 1) + b.rail_hole(1, b.break_col)) / 2)
            self.play(*disappear(add), right.animate.set_fill(UNPOW, opacity=0.6),
                      FlashAround(gap, color=RED, time_width=1.5, buff=0.05), run_time=1.2)
            self.chip2 = dip_chip(b, CHIP2_COL)
            p14b = wire(b.hole(0, CHIP2_COL), b.rail_hole(1, CHIP2_COL), GOLD, width=6)
            nop = T("no power", 30, RED).move_to([self.chip2.get_x(), top + 0.38, 0])
            self.play(FadeIn(self.chip2, shift=0.4 * DOWN), *during(appear(p14b, shift=None), 0.3, 0.7),
                      *during(appear(nop, shift=0.2 * DOWN), 0.55, 1), run_time=1.3)
            c.wait_until("unpowered")
            self.bridge = wire(b.rail_hole(1, b.break_col - 2), b.rail_hole(1, b.break_col + 1), GOLD, angle=-0.9, width=6)
            self.play(*during(appear(self.bridge, shift=0.2 * DOWN), 0, 0.6),
                      *during(right.animate.set_fill(GOLD, opacity=1.0), 0.4, 1), *during(disappear(nop), 0.5, 1),
                      run_time=max(0.6, min(1.2, c.until())))
            self.chk = chk
            self.pwires.append(p14b)
            self.nop = nop

    # c1.board.4: give yourself room; no prize for small; short wires; left to right
    def clip4(self):
        b = self.board
        with self.say("c1.board.4", gap=3.0) as c:
            leaving = [self.ps, *self.ps_labels, *self.jumpers.values(), *self.row_labels.values(),
                       *self.pwires, self.chip, self.chip2, self.bridge, self.chk]
            b.generate_target()
            b.target.scale(0.9 / ZOOM).move_to(0.1 * DOWN)
            for t in b.target.all_strips():
                t.set_fill(TEAL, opacity=FAINT)
            self.play(*during(disappear(*leaving), 0, 0.5), *during(MoveToTarget(b), 0.3, 1), run_time=1.6)
            s = 0.9
            r1 = resistor(b.hole(2, 9), b.hole(2, 12), s)
            ld = green_led(b.hole(2, 13), b.hole(2, 14), s)
            r2 = resistor(b.hole(3, 15), b.hole(3, 18), s)
            self.play(*appear(r1, ld, r2, shift=0.2 * DOWN, lag=0.2), run_time=1.0)
            c.wait_until("wrong column")
            self.play(Transform(r2, resistor(b.hole(3, 14), b.hole(3, 18), s)), run_time=1.2)
            top = b.body.get_top()[1]
            oops = T("a connection you never meant", 32, RED).move_to([0, top + 0.5, 0])
            bad = b.col_strip(14, 3)
            c.wait_until("connection")
            self.play(bad.animate.set_fill(RED, opacity=1.0), *appear(oops, shift=0.2 * DOWN),
                      FlashAround(ld.ends[1], color=RED, buff=0.08, time_width=1.5),
                      FlashAround(r2.ends[0], color=RED, buff=0.08, time_width=1.5), run_time=1.2)

            c.wait_until("prizes")
            self.play(Transform(r1, resistor(b.hole(2, 4), b.hole(2, 7), s)),
                      Transform(ld, green_led(b.hole(2, 12), b.hole(2, 13), s)),
                      Transform(r2, resistor(b.hole(2, 18), b.hole(2, 21), s)),
                      bad.animate.set_fill(TEAL, opacity=FAINT), run_time=1.5)
            quote = T("“There’s no prizes for making this as small as possible”", 32, YELLOW)
            quote.move_to(oops)
            c.wait_until("as small as possible")
            self.play(*swap(oops, quote), run_time=1.2)

            c.wait_until("short")
            wa_long = wire(b.hole(4, 7), b.hole(4, 12), WIRE_BLUE, angle=1.4 * PI)
            wb_long = wire(b.hole(0, 13), b.hole(0, 18), WIRE_GREEN, angle=-1.2 * PI)
            self.play(*appear(wa_long, wb_long, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("neater")
            self.play(Transform(wa_long, wire(b.hole(4, 7), b.hole(4, 12), WIRE_BLUE, angle=0.25)),
                      Transform(wb_long, wire(b.hole(0, 13), b.hole(0, 18), WIRE_GREEN, angle=-0.25)),
                      run_time=1.6)

            c.wait_until("flow")
            y = b.trench_y()
            arrow = Arrow([b.body.get_left()[0] + 0.2, y, 0], [b.body.get_right()[0] - 0.2, y, 0], buff=0,
                          stroke_width=5, color=YELLOW).set_opacity(0.6)
            ins = T("inputs", 32, YELLOW).next_to(b.body, LEFT, buff=0.2).set_y(y)
            outs = T("outputs", 32, YELLOW).next_to(b.body, RIGHT, buff=0.2).set_y(y)
            self.play(GrowArrow(arrow), run_time=1.2)
            c.wait_until(own_word=ins)
            self.play(*appear(ins, outs, shift=None, lag=0.6), run_time=1.2)
