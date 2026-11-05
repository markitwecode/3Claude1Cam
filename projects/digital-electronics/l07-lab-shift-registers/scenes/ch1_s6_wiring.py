"""Chapter 1, scene 6: from the log-book diagram to wires on the board. Clips c1.wire.1 – c1.wire.5.

Reusable drawings (s1, s7, s8 import them via load_scene("ch1_s6_wiring")):
  logbook_page(chip="IC1", wires=True)  the cream log-book page with the lecturer's excerpt
        (.paper .gates .box .ic_label .gate_labels .tag .pin_labels{n} .paths{"l1".."l6"} .leads)
  connection_list()                     the six-line connection list (.header .lines .strikes)
  logbook_excerpt(struck=True)          page + list side by side, as at the end of c1.wire.3
                                        (.page .list); struck=True: every line struck off
  wired_board()                         the finished board of c1.wire.4 at its place on screen
        (.board .chip .pin_nums .power .wires[0..5] in list order); chip label replaced by pin numbers
  route(points, color)                  a jumper wire laid along a polyline (.path)
Board, chip and wire() come from ch1_s3_breadboard; probe_leads from ch1_s5_leds.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S3 = load_scene("ch1_s3_breadboard")
S5 = load_scene("ch1_s5_leds")

# ── the log-book page (shared) ────────────────────────────────────────────────────
PAPER = "#EEE6CD"
PENCIL = "#4C4F55"
INK_A = "#2C77C0"        # the input line feeding 1, 2 and 13
INK_B = "#7A4A9E"        # the input line feeding 4, 5 and 12
LABEL_EDGE = "#2A2620"
STRIKE = "#A3A7AD"       # pencil strike-through on the dark background

# net colours on the board and in the list
NET_A = BLUE
NET_B = PURPLE
NET_A2 = "#A9E1F2"       # 3–9, a light shade of the BLUE net
NET_B2 = "#CDB3E0"       # 6–10, a light shade of the PURPLE net


def _p(x, y):
    return np.array([x, y, 0.0])


def nand_gate(center, w=0.9, h=0.8, color=PENCIL, width=3):
    """NAND symbol (flat back, round front, output bubble); .in_pt(k) k=0 top / 1 bottom, .out_pt()."""
    cx, cy = center
    g = VGroup(
        Line(_p(cx - w / 2, cy + h / 2), _p(cx, cy + h / 2)),
        Line(_p(cx - w / 2, cy - h / 2), _p(cx, cy - h / 2)),
        Line(_p(cx - w / 2, cy + h / 2), _p(cx - w / 2, cy - h / 2)),
        Arc(radius=h / 2, start_angle=PI / 2, angle=-PI, arc_center=_p(cx, cy)),
        Circle(radius=0.08).move_to(_p(cx + h / 2 + 0.08, cy)),
    ).set_stroke(color, width)
    g.in_pt = lambda k: interpolate(g[2].get_start(), g[2].get_end(), 0.25 if k == 0 else 0.75)
    g.out_pt = lambda: g[4].get_right()
    return g


def _label(text, size, color, at):
    t = T(text, size, color).move_to(_p(*at))
    return set_backstroke(t, LABEL_EDGE, 5)


def _poly(pts, color, width):
    return VMobject().set_points_as_corners([_p(*q) for q in pts]).set_stroke(color, width)


GATES = {"a": (-0.2, 2.0), "b": (-0.2, 0.4), "c": (2.0, 1.2), "d": (-0.2, -1.6)}
NETS = {   # the connection list, read off the diagram
    "l1": ([(-0.65, 2.2), (-1.05, 2.2), (-1.05, 1.8), (-0.65, 1.8)], INK_A),
    "l2": ([(-1.05, 2.0), (-1.5, 2.0), (-1.5, -1.4), (-0.65, -1.4)], INK_A),
    "l3": ([(-0.65, 0.6), (-1.05, 0.6), (-1.05, 0.2), (-0.65, 0.2)], INK_B),
    "l4": ([(-1.05, 0.4), (-1.9, 0.4), (-1.9, -1.8), (-0.65, -1.8)], INK_B),
    "l5": ([(0.36, 2.0), (1.0, 2.0), (1.0, 1.4), (1.55, 1.4)], PENCIL),
    "l6": ([(0.36, 0.4), (1.0, 0.4), (1.0, 1.0), (1.55, 1.0)], PENCIL),
}
PIN_AT = {1: (-0.85, 2.4), 2: (-0.85, 1.6), 3: (0.68, 2.2), 4: (-0.85, 0.8), 5: (-0.85, 0.0),
          6: (0.68, 0.6), 9: (1.27, 1.6), 10: (1.27, 0.8), 8: (2.82, 1.4),
          13: (-0.92, -1.2), 12: (-0.92, -2.0), 11: (0.7, -1.4)}


def logbook_page(chip="IC1", wires=True):
    """The excerpt on a cream page, centred on ORIGIN, 6.1 x 6.7. chip="IC2", wires=False: the
    second chip's outline only (four gates, dashed box, its name)."""
    n = chip[-1]
    g = VGroup()
    g.paper = Rectangle(width=6.1, height=6.7).move_to(_p(0.3, 0.1))
    g.paper.set_fill(PAPER, 1).set_stroke("#BDB49A", 2)
    g.gates = [nand_gate(GATES[k]) for k in "abcd"]
    g.box = DashedVMobject(Rectangle(width=3.91, height=4.95).move_to(_p(0.705, 0.175)),
                           num_dashes=56).set_stroke(PENCIL, 3)
    g.ic_label = T(chip, 32 if wires else 38, PENCIL).move_to(_p(-0.75, 2.97))
    g.gate_labels = [_label(f"{n}{k}", 30, YELLOW, (GATES[k][0] - 0.06, GATES[k][1])) for k in "abcd"]
    g.tag = _label(f"{chip}a, {chip}b, …", 30, YELLOW, (0.7, -2.84))
    g.add(g.paper, *g.gates, g.box, g.ic_label)
    g.paths, g.pin_labels, g.leads, g.dots = {}, {}, [], []
    if wires:
        g.paths = {k: _poly(pts, col, 4 if col != PENCIL else 3) for k, (pts, col) in NETS.items()}
        g.leads = [_poly([(-2.4, 2.0), (-1.5, 2.0)], INK_A, 4), _poly([(-2.4, 0.4), (-1.9, 0.4)], INK_B, 4),
                   _poly([(2.56, 1.2), (3.0, 1.2)], PENCIL, 3), _poly([(0.36, -1.6), (1.0, -1.6)], PENCIL, 3)]
        g.dots = [Dot(_p(*q), radius=0.07, color=col) for q, col in
                  (((-1.5, 2.0), INK_A), ((-1.05, 2.0), INK_A), ((-1.9, 0.4), INK_B), ((-1.05, 0.4), INK_B))]
        g.pin_labels = {k: _label(str(k), 30, GOLD, at) for k, at in PIN_AT.items()}
        g.add(*g.paths.values(), *g.leads, *g.dots)
    g.shift(_p(-0.3, -0.1))
    return g


LIST_TEXT = ["1–2", "1/2–13", "4–5", "4/5–12", "3–9", "6–10"]
LIST_COLORS = [NET_A, NET_A, NET_B, NET_B, NET_A2, NET_B2]


def connection_list():
    """The connection list as a column (header "connections", six lines), centred on ORIGIN;
    .strikes are the pencil strike-through lines (not added)."""
    g = VGroup()
    g.header = T("connections", 30, DIM)
    g.lines = [T(s, 36, c) for s, c in zip(LIST_TEXT, LIST_COLORS)]
    col = VGroup(*g.lines).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
    g.header.next_to(col, UP, buff=0.5).align_to(col, LEFT)
    g.add(g.header, *g.lines)
    g.move_to(ORIGIN)
    g.strikes = [Line(ln.get_left() + LEFT * 0.1, ln.get_right() + RIGHT * 0.1).set_stroke(STRIKE, 3)
                 for ln in g.lines]
    return g


PAGE_AT = _p(-1.25, 0.0)     # c1.wire.3 layout: page left, list at its right
LIST_AT = _p(3.55, 0.0)
LIST_LEFT_AT = _p(-5.35, 0.0)   # c1.wire.4 on: the list in the left column


def logbook_excerpt(struck=True):
    g = VGroup()
    g.page = logbook_page().move_to(PAGE_AT)
    for m in [*g.page.gate_labels, g.page.tag, *g.page.pin_labels.values()]:
        g.page.add(m)
    g.list = connection_list().move_to(LIST_AT)
    if struck:
        for ln, s in zip(g.list.lines, g.list.strikes):
            s.move_to(ln)
            g.list.add(s)
    g.add(g.page, g.list)
    return g


# ── the board (shared) ─────────────────────────────────────────────────────────────
PITCH = 0.4
WIDEN = 1.2    # the board is drawn 1.2x wider than tall, so two-digit pin numbers fit
BOARD_AT = _p(1.6, 0.0)
C = 3          # pin 1's column
C2 = 12        # where a second chip would go


def seat_chip(b, col):
    """A 74HC00 (marking removed) astride the trench of the widened board, pin 1 in column col."""
    chip = S3.DipChip(14, "74HC00", pitch=PITCH).stretch(WIDEN, 0)
    chip.remove(chip.label)
    return chip.move_to([(b.hole(5, col)[0] + b.hole(5, col + 6)[0]) / 2, b.trench_y(), 0])


def route(points, color, width=7):
    """A jumper wire laid flat along a polyline through `points`, dark-edged, leg ends at both ends."""
    path = VMobject().set_points_as_corners([np.array(q) for q in points])
    path.set_stroke(color, width)
    path.set_stroke(S3.WIRE_DARK, width + 3, background=True)
    g = VGroup(path, Dot(points[0], radius=0.06, color=S3.LEG_GREY), Dot(points[-1], radius=0.06, color=S3.LEG_GREY))
    g.path = path
    return g


def connection_wires(b):
    """The six wires, in list order, on board b (chip pin 1 in column C)."""
    P = b.hole
    w1 = S3.wire(P(6, C), P(6, C + 1), NET_A, angle=PI)
    w2 = route([P(7, C), P(7, C - 1), P(2, C - 1), P(2, C + 1)], NET_A)
    w3 = S3.wire(P(6, C + 3), P(6, C + 4), NET_B, angle=PI)
    w4 = route([P(9, C + 3), P(9, C - 2), P(1, C - 2), P(1, C + 2)], NET_B)
    w5 = route([P(8, C + 2), P(8, C + 8), P(0, C + 8), P(0, C + 5)], NET_A2)
    w6 = route([P(7, C + 5), P(7, C + 7), P(1, C + 7), P(1, C + 4)], NET_B2)
    for w in (w1, w3):
        w.path = w[0]
    return [w1, w2, w3, w4, w5, w6]


def chip_pin_numbers(chip):
    """GOLD pin numbers on the chip body, each beside its pin (they replace the chip's marking)."""
    cy = chip.body.get_y()
    nums = VGroup()
    for n in range(1, 15):
        y = cy - 0.165 if n <= 7 else cy + 0.165
        nums.add(T(str(n), 28, GOLD).move_to([chip.pin(n).get_x(), y, 0]))
    return nums


def bare_board():
    """Board (continuous rails), chip (pin numbers instead of marking), powered rails and the two power wires."""
    b = S3.Breadboard(cols=19, pitch=PITCH, rail_breaks=()).stretch(WIDEN, 0).move_to(BOARD_AT)
    for i, col in ((0, DIM), (1, GOLD), (2, DIM), (3, GOLD)):
        b.rails[i].set_fill(col, opacity=1.0)
    chip = seat_chip(b, C)
    nums = chip_pin_numbers(chip)
    power = [S3.wire(b.hole(0, C), b.rail_hole(1, C), GOLD, width=6),
             S3.wire(b.hole(9, C + 6), b.rail_hole(2, C + 6), DIM, width=6)]
    return b, chip, nums, power


def wired_board():
    g = VGroup()
    g.board, g.chip, g.pin_nums, g.power = bare_board()
    g.wires = connection_wires(g.board)
    g.add(g.board, *g.power, g.chip, g.pin_nums, *g.wires)
    return g


def demonstrator_icon(color=FG):
    head = Circle(radius=0.32).set_stroke(color, 4).move_to(UP * 0.55)
    body = Arc(radius=0.62, start_angle=0, angle=PI).set_stroke(color, 4).move_to(DOWN * 0.3)
    base = Line(LEFT * 0.62, RIGHT * 0.62).set_stroke(color, 4).move_to(body.get_bottom())
    return VGroup(head, body, base)


class Wiring(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.wire.1: draw it in the log book: number chips, letter gates, pin numbers
    def clip1(self):
        with self.say("c1.wire.1") as c:
            pg = logbook_page().scale(1.08).move_to(ORIGIN)
            self.page = pg
            self.play(FadeIn(pg.paper, shift=0.3 * UP), run_time=1.0)
            drawn = [*pg.gates, *pg.paths.values(), *pg.leads]
            self.play(*[Create(m) for m in drawn], *[FadeIn(d) for d in pg.dots],
                      run_time=min(2.0, c.until("number") - 0.2))
            c.wait_until("number")
            self.play(Create(pg.box), *appear(pg.ic_label), run_time=1.2)
            c.wait_until("letter")
            self.play(*appear(*pg.gate_labels, pg.tag, lag=0.15), run_time=min(1.2, c.until("pin number")))
            c.wait_until("pin number")
            pins = [pg.pin_labels[k] for k in (1, 2, 3, 4, 5, 6, 9, 10, 8, 13, 12, 11)]
            self.play(*appear(*pins, shift=0.1 * DOWN, lag=0.1), run_time=2.0)
            settle(self, pg, add=[*pg.gate_labels, pg.tag, *pins])

    # c1.wire.2: two identical chips; no labels = wiring disaster; the demonstrator needs a page
    def clip2(self):
        pg = self.page
        with self.say("c1.wire.2", gap=1.4) as c:
            ic2 = logbook_page("IC2", wires=False).scale(0.85).move_to(_p(3.75, -0.35))
            self.play(pg.animate.scale(1 / 1.08).move_to(_p(-3.5, -0.35)), run_time=1.3)
            self.play(*appear(ic2, shift=0.3 * DOWN), run_time=min(1.2, c.until("two identical")))
            c.wait_until("identical")
            self.play(FlashAround(pg.box, color=YELLOW, time_width=1.5),
                      FlashAround(ic2.box, color=YELLOW, time_width=1.5), run_time=1.5)
            labels = [*pg.gate_labels, pg.tag, *pg.pin_labels.values(), pg.ic_label]
            c.wait_until("without labels")
            self.play(*[m.animate.set_opacity(0) for m in [*labels, ic2.ic_label]], run_time=1.0)
            src = [pg.paths["l5"].get_end(), pg.leads[2].get_end(), pg.leads[3].get_end()]
            dst = [ic2.gates[3].in_pt(0), ic2.gates[0].in_pt(1), ic2.gates[2].in_pt(1)]
            tangle = [ArcBetweenPoints(s, d, angle=a).set_stroke(RED, 4)
                      for s, d, a in zip(src, dst, (-1.1, 0.9, -0.7))]
            cap = T("“wiring disaster”", 40, RED).move_to(_p(0.15, 3.42))
            c.wait_until("wiring disaster")
            self.play(*[Create(t) for t in tangle], *appear(cap), run_time=1.2)
            c.wait_until("demonstrator")
            self.play(*during(disappear(*tangle, ic2, cap), 0, 0.45),
                      *during([m.animate.set_opacity(1) for m in labels], 0.4, 1), run_time=1.2)
            blank = Rectangle(width=2.0, height=2.6).set_fill(PAPER, 1).set_stroke("#BDB49A", 2)
            blank.move_to(_p(4.7, -0.35))
            who = demonstrator_icon().move_to(_p(2.0, -0.35))
            q = T("?", 56, YELLOW).next_to(who, UP, buff=0.3)
            self.play(*appear(who, blank, q, lag=0.2), run_time=1.0)
            tick = check_mark().scale(1.6).move_to(_p(0.15, 2.6))
            c.wait_until("check")
            self.play(Create(tick), run_time=min(0.8, c.until()))
            self.demo = [who, blank, q, tick]

    # c1.wire.3: the excerpt; the connection list read off it line by line
    def clip3(self):
        pg = self.page
        with self.say("c1.wire.3") as c:
            self.play(*during(disappear(*self.demo), 0, 0.45),
                      *during([pg.animate.move_to(PAGE_AT)], 0.3, 1), run_time=1.6)
            c.wait_until("four gates")
            self.play(FlashAround(pg.box, color=YELLOW, time_width=1.5), run_time=1.5)
            lst = connection_list().move_to(LIST_AT)
            self.list = lst
            c.wait_until(own_word=lst.header)
            self.play(*appear(lst.header), run_time=1.0)
            cues = ["l1", "l2", "l3", "l4", "l5", "l6"]
            for i, (cue, ln) in enumerate(zip(cues, lst.lines)):
                c.wait_until(cue)
                nxt = cues[i + 1] if i + 1 < len(cues) else None
                rt = min(1.1, max(0.6, 0.8 * c.until(nxt)))
                flash_path = pg.paths[cue].copy().set_stroke(YELLOW, 9)
                self.play(VShowPassingFlash(flash_path, time_width=0.6),
                          *appear(ln, shift=0.25 * LEFT), run_time=rt)

    # c1.wire.4: wire them one at a time, striking each off
    def clip4(self):
        pg, lst = self.page, self.list
        with self.say("c1.wire.4") as c:
            b, chip, nums, power = bare_board()
            self.board, self.chip, self.nums = b, chip, nums
            self.play(*during(disappear(pg), 0, 0.4),
                      *during([lst.animate.move_to(LIST_LEFT_AT)], 0.35, 0.85),
                      *during(appear(b, *power, chip, nums, shift=None, lag=0.1), 0.5, 1), run_time=2.0)
            wires = connection_wires(b)
            self.wires = wires
            for s, ln in zip(lst.strikes, lst.lines):
                s.move_to(ln)

            def lay(i, rt):
                self.play(Create(wires[i], lag_ratio=0), *during([Create(lst.strikes[i])], 0.6, 1), run_time=rt)

            c.wait_until("w1")
            lay(0, 1.4)
            c.wait_until("spag")
            far = [b.hole(8, 17), b.hole(9, 18)]
            spag = [S3.wire(b.hole(8, C), far[0], RED, angle=0.9), S3.wire(b.hole(8, C + 1), far[1], RED, angle=1.1)]
            self.play(*[Create(s, lag_ratio=0) for s in spag], run_time=1.4)
            c.wait_until("starts")
            self.play(*disappear(*spag), run_time=min(1.0, c.until("w2")))
            c.wait_until("w2")
            lay(1, 1.8)
            c.wait_until("w3")
            lay(2, 1.3)
            c.wait_until("w4")
            lay(3, 1.6)
            c.wait_until("w5")
            lay(4, min(1.3, 0.9 * c.until("w6")))
            c.wait_until("w6")
            lay(5, 1.3)

    # c1.wire.5: round, never over; same way; near; colours; one section at a time
    def clip5(self):
        b, chip, nums, wires, lst = self.board, self.chip, self.nums, self.wires, self.list
        with self.say("c1.wire.5", gap=4.5) as c:
            over = S3.wire(b.hole(6, C + 2), b.hole(3, C + 5), RED)
            self.play(Create(over, lag_ratio=0), run_time=1.0)
            a, z = b.hole(6, C + 2), b.hole(3, C + 5)
            ty = chip.pin(10).get_y()
            tip = a + (z - a) * (ty - a[1]) / (z[1] - a[1])
            meter = S5.multimeter_drawing().move_to(_p(tip[0] + 0.8, -9.0))
            probe = S5.probe_leads(meter, tip, tip + LEFT).red
            probe.shift(DOWN * 4.6)
            self.add(probe)
            c.wait_until("probe")
            self.play(probe.animate.shift(UP * 4.6), run_time=1.2)
            self.play(FlashAround(Dot(tip, radius=0.12), color=RED, time_width=1.5, buff=0.04), run_time=0.9)
            c.wait_until("trap")
            self.play(probe.animate.shift(DOWN * 4.6),
                      chip.animate(rate_func=there_and_back).shift(UP * 0.22),
                      nums.animate(rate_func=there_and_back).shift(UP * 0.22),
                      FlashAround(over, color=RED, time_width=1.5, buff=0.06), run_time=1.3)
            self.remove(probe)
            x = cross_mark().scale(1.5).move_to(chip.body.get_center())
            self.play(Create(x), run_time=0.6)
            self.play(*disappear(over, x), run_time=min(0.9, c.until("sameway")))

            c.wait_until("sameway")
            chip2 = seat_chip(b, C2)
            chip2.rotate(PI)
            chip2.body.set_stroke(RED, 4)
            mark_at = _p(chip2.get_x(), b.hole(1, C2 + 3)[1])
            bad = cross_mark().move_to(mark_at)
            self.play(FadeIn(chip2, shift=0.4 * DOWN), run_time=1.0)
            self.play(Create(bad), run_time=0.6)
            c.wait_until("pin one")
            good = check_mark().scale(1.2).move_to(mark_at)
            self.play(Rotate(chip2, PI), *during(disappear(bad), 0, 0.4), run_time=1.4)
            self.play(chip2.body.animate.set_stroke(GREEN, 4), Create(good), run_time=0.8)

            c.wait_until("near")
            ca = S3.DipChip(label="IC", pitch=0.3)
            cb = S3.DipChip(label="IC", pitch=0.3)
            for ch in (ca, cb):
                ch.remove(ch.label)
            ca.rotate(PI / 2)       # pins 1..7 up its right side
            cb.rotate(-PI / 2)      # pins 1..7 down its left side, facing ca
            MX, MY = -5.15, 2.3
            ca.move_to(_p(MX - 1.45, MY))
            cb.move_to(_p(MX + 1.45, MY))
            cols = [NET_A, NET_B, NET_A2, NET_B2]
            links = [always_redraw(lambda k=k, col=col: Line(ca.pin(k).get_right(), cb.pin(8 - k).get_left())
                                   .set_stroke(col, 6)) for k, col in zip((2, 3, 4, 5), cols)]
            leaving = [*lst.lines, lst.header, *lst.strikes, chip2, good]
            self.play(*during(disappear(*leaving), 0, 0.45),
                      *during(appear(ca, cb, shift=None), 0.5, 1), run_time=1.2)
            self.add(*links)
            self.play(ca.animate.move_to(_p(MX - 0.65, MY)), cb.animate.move_to(_p(MX + 0.65, MY)), run_time=1.6)

            cap1 = VGroup(T("colour-coded", 32, FG), T("wires", 32, FG)).arrange(DOWN, buff=0.2).move_to(_p(MX, 0.15))
            c.wait_until("colours")
            self.play(*appear(cap1),
                      *[VShowPassingFlash(w.path.copy().set_stroke(WHITE, 10).set_stroke(width=0, background=True),
                                          time_width=0.5) for w in wires], run_time=1.4)
            cap2 = VGroup(*[T(s, 32, YELLOW) for s in ("build and test", "one section", "at a time")])
            cap2.arrange(DOWN, buff=0.2).move_to(_p(MX, -1.75))
            # the section: this chip's terminal rows only (rows 0..9, cols C-2..C+8), clear of the rails
            x0, x1 = b.hole(0, C - 2)[0] - 0.3, b.hole(0, C + 8)[0] + 0.3
            y0, y1 = b.hole(9, C)[1] - 0.22, b.hole(0, C)[1] + 0.22
            sec = DashedVMobject(Rectangle(width=x1 - x0, height=y1 - y0).move_to(_p((x0 + x1) / 2, (y0 + y1) / 2)),
                                 num_dashes=70).set_stroke(YELLOW, 6)
            c.wait_until("section")
            self.play(Create(sec), *appear(cap2), run_time=min(1.6, c.until()))
