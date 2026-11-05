"""Chapter 1, scene 7: the build order, power first, and the inputs you don't use. Clips c1.build.1 – c1.build.5.

Reusable drawings (s8 and Lecture 7 ch2 s7 import them via load_scene("ch1_s7_build")):
  checklist()                 the five-line build checklist, centred on ORIGIN, 4.4 wide
        (.items[0..4], each a VGroup (num, *lines); .ticks[0..4] GREEN ticks placed, not added)
  two_chip_board(ties=True)   s6's board with IC2 seated at C2, built at s6's place and scale, rails continuous
        (.board .chip .pin_nums .power .wires   (IC1, as s6)
         .ic2 .ic2_nums .ic2_power[2] .ic2_wires[2] (gate a's inputs) .ties[6] (pins 4,5,9,10,12,13 to 0 V))
  place(g, at, scale, nums=(7, 14))  scale/move it; only pins `nums` keep numbers on screen (.ic1_shown .ic2_shown);
        .pin_nums/.ic2_nums still hold all 14 (placed, not added)
  finished_board()            two_chip_board(ties=True) placed as at the end of this scene
  floating_inputs()           THE floating-input visual: IC2 drawn ~2x, gate a wired, six open spare inputs,
        three output lamps; .waves and .tag ("floating") built but not added (see its docstring)
  ic2_strip(b, n)             the board strip IC2's pin n sits in
  pickup_waves(b, pins)       wavy PURPLE pickup lines in the free part of each pin's column
  start_wobble(waves)         makes them wobble (updater)
  Flicker(parts, ...)         invisible controller toggling parts' fill at random; feeds a power tracker
  power_gauge(tracker)        the GOLD power bar ("IC2" label, frame, bar following tracker)
  power_tag()                 "CMOS power goes with / how often it switches", GOLD
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
S6 = load_scene("ch1_s6_wiring")


def _p(x, y):
    return np.array([x, y, 0.0])


C, C2 = S6.C, S6.C2
B_SCALE = 0.8
B_AT = _p(2.6, -0.55)          # the board's centre on screen in this scene
COL_X = -4.2                   # the left column's centre (x -6.6 .. -1.8)
SPARE_IN = [4, 5, 9, 10, 12, 13]
SPARE_OUT = [6, 8, 11]


# ── the checklist (shared) ─────────────────────────────────────────────────────────
CHECK_LINES = [["check every chip", "has all its legs"],
               ["insert all chips:", "same way round,", "no pin folded"],
               ["wire 5 V and 0 V", "to every chip"],
               ["tie unused inputs", "to 0 V"],
               ["then the rest"]]


def checklist(size=30):
    g = VGroup()
    g.items, g.ticks = [], []
    for k, lines in enumerate(CHECK_LINES):
        txt = VGroup(*[T(s, size, FG) for s in lines]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        num = T(str(k + 1), size, GOLD)
        num.next_to(txt[0], LEFT, buff=0.3)
        item = VGroup(num, *txt)
        g.items.append(item)
    VGroup(*g.items).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
    g.add(*g.items)
    g.move_to(ORIGIN).shift(RIGHT * 0.3)
    for item in g.items:
        t = check_mark().scale(0.75)
        t.next_to(item[0], LEFT, buff=0.22)
        g.ticks.append(t)
    return g


# ── the board with IC2 (shared) ────────────────────────────────────────────────────
def ic2_col(n):
    """IC2's pin n -> (row, col) of the hole it sits in."""
    return (5, C2 + n - 1) if n <= 7 else (4, C2 + 14 - n)


def ic2_strip(b, n):
    row, col = ic2_col(n)
    return b.col_strip(col, row)


def _join_rails(b):
    """Make every power rail one continuous strip (no break halfway), keeping its fill."""
    for r in b.rails:
        parts = list(r.submobjects)
        if len(parts) < 2:
            continue
        a, z = parts[0], parts[-1]
        whole = RoundedRectangle(corner_radius=0.05, width=z.get_right()[0] - a.get_left()[0], height=a.height)
        whole.move_to([(a.get_left()[0] + z.get_right()[0]) / 2, a.get_y(), 0])
        whole.set_fill(a.get_fill_color(), opacity=a.get_fill_opacity()).set_stroke(width=0)
        r.remove(*parts)
        r.add(whole)
    b.break_col = None


def two_chip_board(ties=True):
    g = S6.wired_board()
    b = g.board
    _join_rails(b)                     # continuous rails: IC2's pin 14 (col C2) is on live 5 V
    P = b.hole
    g.ic2 = S6.seat_chip(b, C2)
    g.ic2_nums = S6.chip_pin_numbers(g.ic2)
    g.ic2_power = [S3.wire(P(0, C2), b.rail_hole(1, C2), GOLD, width=6),
                   S3.wire(P(9, C2 + 6), b.rail_hole(2, C2 + 6), DIM, width=6)]
    g.ic2_wires = [S3.wire(P(9, C + 8), P(9, C2), S6.NET_A2),          # IC1's 3 net feeds gate a
                   S3.wire(P(6, C2), P(6, C2 + 1), S6.NET_A2, angle=PI)]  # pins 1 and 2 together
    g.ties = []
    for n in SPARE_IN:
        row, col = ic2_col(n)
        if row == 5:
            g.ties.append(S3.wire(P(9, col), b.rail_hole(2, col), DIM, width=6))
        else:
            g.ties.append(S3.wire(P(0, col), b.rail_hole(0, col), DIM, width=6))
    g.add(*g.ic2_power, g.ic2, g.ic2_nums, *g.ic2_wires)
    if ties:
        g.add(*g.ties)
    return g


def place(g, at=B_AT, scale=B_SCALE, nums=(7, 14)):
    """Scale and move the board; rebuild pin numbers at size 28. At this scale all fourteen run
    together, so only the pins in `nums` stay on the board (for both chips): .ic1_shown, .ic2_shown.
    .pin_nums / .ic2_nums keep all fourteen (index n-1), placed but not added."""
    g.scale(scale, about_point=S6.BOARD_AT).shift(at - S6.BOARD_AT)
    for chip, ns in ((g.chip, g.pin_nums), (g.ic2, g.ic2_nums)):
        cy = chip.body.get_y()
        for n, t in enumerate(ns, start=1):
            t.become(T(str(n), 28, GOLD).move_to([chip.pin(n).get_x(), cy + (0.14 if n > 7 else -0.14), 0]))
    g.remove(g.pin_nums, g.ic2_nums)
    g.ic1_shown = VGroup(*[g.pin_nums[n - 1] for n in nums])
    g.ic2_shown = VGroup(*[g.ic2_nums[n - 1] for n in nums])
    g.add(g.ic1_shown, g.ic2_shown)
    return g


def finished_board():
    return place(two_chip_board(ties=True))


# ── the floating-input visual (shared) ─────────────────────────────────────────────
def _wave_points(x, y0, y1, phase, amp=0.07, k=9.0):
    ys = np.linspace(y0, y1, 40)
    return [np.array([x + amp * np.sin(k * (y - y0) + phase) * np.sin(np.pi * (y - y0) / (y1 - y0) * 0.5 + 0.3),
                      y, 0]) for y in ys]


def pickup_waves(b, pins=SPARE_IN, color=PURPLE):
    waves = VGroup()
    for i, n in enumerate(pins):
        row, col = ic2_col(n)
        x = b.hole(0, col)[0]
        if row == 4:
            y0, y1 = b.hole(0, col)[1] + 0.25, b.hole(3, col)[1]
        else:
            y0, y1 = b.hole(9, col)[1] - 0.25, b.hole(6, col)[1]
        w = VMobject().set_points_smoothly(_wave_points(x, y0, y1, i))
        w.set_stroke(color, 3, opacity=0.85)
        w.wave = (x, y0, y1, float(i))
        waves.add(w)
    return waves


def start_wobble(waves, speed=7.0):
    for w in waves:
        def upd(m, dt):
            x, y0, y1, ph = m.wave
            m.wave = (x, y0, y1, ph + speed * dt)
            m.set_points_smoothly(_wave_points(x, y0, y1, ph + speed * dt))
        w.add_updater(upd)


class Flicker(Mobject):
    """Toggles each part's fill between `on` and `off` (colour, opacity) at random intervals.
    With `power` (a ValueTracker), each switch-on adds `gain` to it, and it decays slowly."""

    def __init__(self, parts, on=(RED, 0.85), off=(TEAL, 0.0), period=(0.15, 0.55), seed=1,
                 power=None, gain=0.0, cap=0.92, floor=0.12):
        super().__init__()
        self.parts, self.on, self.off, self.period = list(parts), on, off, period
        self.rng = np.random.default_rng(seed)
        self.timers = [self.rng.uniform(0, period[1]) for _ in self.parts]
        self.state = [False] * len(self.parts)
        self.power, self.gain, self.cap, self.floor = power, gain, cap, floor
        self.add_updater(lambda m, dt: m._tick(dt))

    def _tick(self, dt):
        for i, p in enumerate(self.parts):
            self.timers[i] -= dt
            if self.timers[i] <= 0:
                self.state[i] = not self.state[i]
                self.timers[i] = self.rng.uniform(*self.period)
                col, op = self.on if self.state[i] else self.off
                p.set_fill(col, opacity=op)
                if self.power is not None and self.state[i]:
                    self.power.set_value(min(self.cap, self.power.get_value() + self.gain))
        if self.power is not None and dt > 0:
            self.power.set_value(max(self.floor, self.power.get_value() - 0.03 * dt))

    def stop(self):
        self.clear_updaters()
        for p in self.parts:
            p.set_fill(self.off[0], opacity=self.off[1])


FI_AT = _p(2.7, -0.15)


def floating_inputs(at=FI_AT, pitch=0.78):
    """The floating-input visual: IC2 drawn large (about 2x its board size), one gate wired.
    Static parts are in the group: .chip, .nums (14 Texts, index n-1, size 34 GOLD), .power (pin 14
    GOLD lead + "5 V", pin 7 DIM lead + "0 V"), .feed (pins 1 and 2 joined, YELLOW, fed from below),
    .leads{n} (pins 3 and the spare ones), .ends{n} (open circles on the six spare inputs; fill to hum),
    .lamps{n} (circles on outputs 3, 6, 8, 11; fill to flicker). Not added: .waves (pickup lines
    beyond the six open ends, start_wobble works on them) and .tag (RED "floating" above the top ones)."""
    g = VGroup()
    ch = S3.DipChip(14, "74HC00", pitch=pitch).stretch(S6.WIDEN, 0)
    ch.remove(ch.label)
    ch.move_to(at)
    g.chip = ch
    cy = ch.body.get_y()
    off = 0.26 * pitch / 0.7
    g.nums = VGroup(*[T(str(n), 36, GOLD).move_to([ch.pin(n).get_x(), cy + (off if n > 7 else -off), 0])
                      for n in range(1, 15)])
    for n in (1, 14):                  # clear of the notch
        g.nums[n - 1].shift(RIGHT * 0.1)

    def tip(n):
        return ch.pin(n).get_top() if n > 7 else ch.pin(n).get_bottom()

    def out(n, d):
        return tip(n) + (UP if n > 7 else DOWN) * d

    L = 0.55
    g.leads, g.ends, g.lamps = {}, {}, {}
    for n in SPARE_IN:
        g.leads[n] = Line(tip(n), out(n, L)).set_stroke(DIM, 4)
        g.ends[n] = Circle(radius=0.1).move_to(out(n, L + 0.1)).set_stroke(DIM, 3).set_fill(PURPLE, 0)
    for n in [3] + SPARE_OUT:
        col = YELLOW if n == 3 else DIM
        g.leads[n] = Line(tip(n), out(n, L)).set_stroke(col, 4)
        g.lamps[n] = Circle(radius=0.17).move_to(out(n, L + 0.17)).set_stroke(col, 3).set_fill(RED, 0)
    j1, j2 = out(1, L), out(2, L)
    mid = (j1 + j2) / 2
    g.feed = VGroup(Line(tip(1), j1), Line(tip(2), j2), Line(j1, j2), Line(mid, mid + DOWN * 0.55))
    g.feed.set_stroke(YELLOW, 4)
    l14 = Line(tip(14), out(14, 0.45)).set_stroke(GOLD, 5)
    l7 = Line(tip(7), out(7, 0.45)).set_stroke(DIM, 5)
    v5 = T("5 V", 30, GOLD).next_to(l14, UP, buff=0.1)
    v0 = T("0 V", 30, DIM).next_to(l7, DOWN, buff=0.1)
    g.power = VGroup(l14, v5, l7, v0)

    g.waves = VGroup()
    for i, n in enumerate(SPARE_IN):
        e = g.ends[n]
        x = e.get_x()
        if n > 7:
            y0 = e.get_top()[1] + 0.12
            y1 = y0 + 1.0
        else:
            y0 = e.get_bottom()[1] - 0.12
            y1 = y0 - 1.0
        w = VMobject().set_points_smoothly(_wave_points(x, y0, y1, float(i)))
        w.set_stroke(PURPLE, 3, opacity=0.85)
        w.wave = (x, y0, y1, float(i))
        g.waves.add(w)
    top = max(w.get_top()[1] for w in g.waves)
    g.tag = T("floating", 32, RED).move_to([ch.pin(11).get_x(), top + 0.32, 0])
    g.add(g.power, g.feed, *g.leads.values(), *g.ends.values(), *g.lamps.values(), ch, g.nums)
    return g


GAUGE_W = 3.4


def power_gauge(tracker, at=_p(COL_X, 2.15)):
    g = VGroup()
    g.label = T("IC2", 30, DIM)
    g.frame = Rectangle(width=GAUGE_W, height=0.34).set_stroke(DIM, 2).set_fill(BG, 0)
    VGroup(g.label, g.frame).arrange(RIGHT, buff=0.3).move_to(at)
    left = g.frame.get_left()

    def bar():
        w = max(0.02, tracker.get_value() * GAUGE_W)
        return Rectangle(width=w, height=0.26).set_stroke(width=0).set_fill(GOLD, 1).move_to(
            left + RIGHT * (w / 2 + 0.0))
    g.bar = always_redraw(bar)
    g.add(g.frame, g.bar, g.label)
    return g


def power_tag(at=_p(COL_X, 3.1)):
    g = VGroup(T("CMOS power goes with", 30, GOLD), T("how often it switches", 30, GOLD))
    g.arrange(DOWN, buff=0.12).move_to(at)
    return g


# ── small drawings for this scene ──────────────────────────────────────────────────
def panel(w, h, at):
    return RoundedRectangle(corner_radius=0.15, width=w, height=h).move_to(at).set_fill(BG, 0.96).set_stroke(DIM, 2)


def loose_chip(scale=1.0):
    ch = S3.DipChip(14, "74HC00", pitch=S6.PITCH).stretch(S6.WIDEN, 0)
    ch.remove(ch.label)
    return ch.scale(scale)


def spark(at, r=0.45):
    rays = VGroup()
    for k in range(8):
        a = k * TAU / 8 + 0.2
        d = np.array([np.cos(a), np.sin(a), 0])
        rays.add(Line(at + d * r * 0.3, at + d * r * (1.0 if k % 2 else 0.7)).set_stroke(YELLOW if k % 2 else RED, 5))
    return rays


def fan_icon(color=DIM):
    ring = Circle(radius=0.34).set_stroke(color, 3)
    blades = VGroup(*[Ellipse(width=0.16, height=0.3).shift(UP * 0.15).rotate(k * TAU / 3, about_point=ORIGIN)
                      for k in range(3)]).set_stroke(color, 3)
    return VGroup(ring, blades)


def heater_icon(color=DIM):
    pts = [_p(-0.34 + 0.68 * i / 8, 0.22 * (1 if i % 2 else -1)) for i in range(9)]
    return VGroup(VMobject().set_points_as_corners(pts).set_stroke(color, 4),
                  Line(_p(-0.4, -0.34), _p(0.4, -0.34)).set_stroke(color, 3))


def hand_icon(color=FG):
    palm = RoundedRectangle(corner_radius=0.12, width=0.5, height=0.5).set_stroke(color, 3).set_fill(BG, 1)
    fingers = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.11, height=h).set_stroke(color, 3).set_fill(BG, 1)
                       .next_to(palm, UP, buff=-0.04).set_x(palm.get_left()[0] + 0.07 + 0.12 * i)
                       for i, h in enumerate((0.3, 0.36, 0.34, 0.26))])
    thumb = RoundedRectangle(corner_radius=0.05, width=0.11, height=0.28).set_stroke(color, 3).set_fill(BG, 1)
    thumb.rotate(0.7).move_to(palm.get_left() + _p(-0.06, 0.02))
    return VGroup(fingers, thumb, palm)


def booklet_icon():
    left = Polygon(_p(-0.42, 0.3), _p(0, 0.24), _p(0, -0.3), _p(-0.42, -0.24)).set_stroke(FG, 3)
    right = left.copy().flip(UP, about_point=ORIGIN)
    lines = VGroup(*[Line(_p(-0.34, 0.14 - 0.12 * i), _p(-0.08, 0.1 - 0.12 * i)).set_stroke(DIM, 2) for i in range(3)])
    return VGroup(left, right, lines, lines.copy().flip(UP, about_point=ORIGIN))


class Build(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        for m in list(self.mobjects):
            m.clear_updaters()
        self.remove(*[m for m in self.mobjects if isinstance(m, Flicker)])
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.build.1: the checklist, ticked as the board gets IC2 and power
    def clip1(self):
        with self.say("c1.build.1") as c:
            fb = place(two_chip_board(ties=True))
            self.fb = fb
            b = fb.board
            ic1 = [b, *fb.power, fb.chip, fb.ic1_shown, *fb.wires]
            cl = checklist().move_to(_p(COL_X, 0.0))
            self.cl = cl
            self.play(FadeIn(VGroup(*ic1)), run_time=1.2)
            self.remove(VGroup(*ic1))
            self.add(*ic1)

            # 1: every leg
            c.wait_until("legs")
            self.play(*appear(cl.items[0]), run_time=1.0)  # early: a checklist item appears whole
            pnl = panel(8.0, 2.6, _p(2.6, 0.2)).set_fill(S3.BOARD_WHITE, 1)
            good = loose_chip(1.1).move_to(_p(4.6, 0.2))
            bad = loose_chip(1.1).move_to(_p(0.6, 0.2))
            gap_at = bad.pin(4).get_center()
            bad.remove(bad.pin(4))
            gap = Rectangle(width=0.22, height=0.24).move_to(gap_at).set_stroke(RED, 4)
            self.play(FadeIn(pnl), *appear(bad, good, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("others")
            self.play(FadeIn(gap), FlashAround(gap, color=RED, run_time=1.0), run_time=1.0)
            self.play(GrowFromCenter(cl.ticks[0]), run_time=min(0.8, c.until("insert")))

            # 2: insert, same way round, one pin folds and is straightened
            c.wait_until("insert")
            pin5 = fb.ic2.pin(5)
            straight = pin5.copy()
            pin5.rotate(-PI / 2, about_point=pin5.get_top()).set_fill(RED, 1)
            self.play(*appear(cl.items[1]), *during(disappear(bad, gap, pnl), 0, 0.6), run_time=1.0)  # early: a checklist item appears whole
            self.play(ReplacementTransform(good, fb.ic2), run_time=1.5)
            ring = Circle(radius=0.32).move_to(pin5.get_center()).set_stroke(RED, 4)
            c.wait_until("folded")
            self.play(GrowFromCenter(ring), run_time=0.6)
            self.play(Transform(pin5, straight), ring.animate.set_stroke(GREEN), run_time=0.9)
            self.play(FadeOut(ring), *appear(fb.ic2_shown, shift=None), GrowFromCenter(cl.ticks[1]),
                      run_time=min(0.9, c.until("five volts")))

            # 3: power to every chip
            c.wait_until("five volts")
            self.play(*appear(cl.items[2]), run_time=0.8)
            self.play(*[Create(w) for w in fb.ic2_power],
                      *[VShowPassingFlash(w[0].copy().set_stroke(WHITE, 9).set_stroke(width=0, background=True),
                                          time_width=0.6) for w in fb.power], run_time=1.4)
            self.play(GrowFromCenter(cl.ticks[2]), run_time=min(0.8, c.until("fourth")))

            # 4 and 5
            c.wait_until("fourth")
            self.play(*appear(cl.items[3]), run_time=1.0)
            c.wait_until("rest")
            self.play(*appear(cl.items[4]), *[Create(w) for w in fb.ic2_wires], run_time=min(1.2, c.until()))

    # c1.build.2: why power first: the log book leaves it out; the back door through the inputs
    def clip2(self):
        with self.say("c1.build.2") as c:
            pg = S6.logbook_page()
            for m in [*pg.gate_labels, pg.tag, *pg.pin_labels.values()]:
                pg.add(m)
            pg.scale(0.95).move_to(_p(-3.55, 0.0))
            item3 = self.cl.items[2]
            self.play(FlashAround(item3, color=GOLD, run_time=1.4), *recolor(item3[1:], GOLD), run_time=1.4)
            c.wait_until("diagrams")
            sweep_clear(self, FadeIn(pg, shift=0.2 * UP), keep=[], run_time=1.4)
            tag = VGroup(T("5 V and 0 V:", 32, GOLD), T("taken as read", 32, FG)).arrange(RIGHT, buff=0.2)
            tag.move_to(_p(3.6, 3.3))
            c.wait_until("supply")
            self.play(*appear(tag), FlashAround(pg.box, color=GOLD, run_time=1.4), run_time=1.4)  # early: tag sums up the sentence

            # the back door
            c.wait_until("backdoor")
            ch = S3.DipChip(14, "74HC00", pitch=0.55)
            ch.remove(ch.label)
            ch.move_to(_p(3.6, 1.0))
            p14, p7, p1 = ch.pin(14), ch.pin(7), ch.pin(1)
            stub14 = DashedLine(p14.get_top(), p14.get_top() + UP * 0.55, dash_length=0.08).set_stroke(DIM, 3)
            stub7 = DashedLine(p7.get_bottom(), p7.get_bottom() + DOWN * 0.55, dash_length=0.08).set_stroke(DIM, 3)
            o14 = Circle(radius=0.07).move_to(stub14.get_end()).set_stroke(DIM, 3)
            o7 = Circle(radius=0.07).move_to(stub7.get_end()).set_stroke(DIM, 3)
            n14 = T("14", 30, GOLD).next_to(o14, LEFT, buff=0.15)
            n7 = T("7", 30, GOLD).next_to(o7, RIGHT, buff=0.15)
            self.play(FadeIn(ch), *[Create(m) for m in (stub14, stub7, o14, o7)],
                      *appear(n14, n7, shift=None), run_time=1.2)  # early: the pin numbers name the chip's pins
            v5 = T("5 V", 32, GOLD).move_to(p1.get_bottom() + _p(-0.9, -1.0))
            w5 = VMobject().set_points_as_corners([p1.get_bottom(), p1.get_bottom() + DOWN * 1.0,
                                                   v5.get_right() + RIGHT * 0.12])
            w5.set_stroke(GOLD, 6)
            c.wait_until("five volts")
            self.play(Create(w5), *appear(v5, shift=None), p1.animate.set_fill(GOLD, 1), run_time=1.0)
            leak = DashedLine(p1.get_top(), p14.get_bottom(), dash_length=0.12).set_stroke(GOLD, 6)
            glow = ch.body.copy().set_fill(GOLD, 0.18).set_stroke(GOLD, 3)
            diode = VGroup(T("through the inputs'", 28, DIM), T("protection diodes", 28, DIM))
            diode.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(_p(3.9, -1.3))
            self.play(Create(leak), FadeIn(glow), p14.animate.set_fill(GOLD, 0.6), run_time=1.4)
            self.play(*appear(diode), run_time=min(1.0, c.until("half")))  # early: aside on the mechanism

            # half works
            c.wait_until("half")
            outs = [ch.pin(n) for n in (3, 6, 8, 11)]
            fl = Flicker(outs, on=(GOLD, 1.0), off=(S3.PIN_GREY, 1.0), period=(0.25, 0.7), seed=4)
            self.add(fl)
            quote = T("“almost working, but not quite”", 32, FG, slant=ITALIC).move_to(_p(3.4, -2.6))
            self.play(*appear(quote), run_time=1.0)  # early: his words, shown as the half-working starts
            c.wait_until()
            fl.stop()
            self.remove(fl)
            self.clip2_mobs = [pg, tag, ch, stub14, stub7, o14, o7, n14, n7, v5, w5, leak, glow, diode, quote]

    # c1.build.3: IC2 large: one gate used, three spare; pickup; random switching; power; upset
    def clip3(self):
        with self.say("c1.build.3") as c:
            view = floating_inputs()
            self.view = view
            sweep_clear(self, FadeIn(view), keep=[], run_time=1.6)
            used = T("1 gate in use", 32, YELLOW).move_to(_p(COL_X, 0.95))
            spare = T("3 spare", 32, PURPLE).move_to(_p(COL_X, 0.35))
            nums = view.nums
            c.wait_until("one gate")
            self.play(*appear(used), *recolor([nums[i - 1] for i in (1, 2, 3)], YELLOW), run_time=1.2)
            c.wait_until("three spare")
            self.play(*appear(spare), *recolor([nums[n - 1] for n in SPARE_IN + SPARE_OUT], PURPLE),
                      *[view.leads[n].animate.set_stroke(PURPLE) for n in SPARE_IN], run_time=1.0)

            # pickup
            c.wait_until("pickup")
            waves = view.waves
            start_wobble(waves)
            self.play(FadeIn(waves), run_time=1.2)
            hum = Flicker([view.ends[n] for n in SPARE_IN], on=(PURPLE, 0.7), off=(PURPLE, 0.0),
                          period=(0.08, 0.25), seed=2)
            self.add(hum)
            self.hum, self.waves = hum, waves

            # random switching
            c.wait_until("flicker")
            power = ValueTracker(0.12)
            self.power = power
            outs = Flicker([view.lamps[n] for n in SPARE_OUT], on=(RED, 0.9), off=(RED, 0.0),
                           period=(0.2, 0.6), seed=5, power=power, gain=0.07)
            self.add(outs)
            self.outs = outs
            ftag = view.tag
            c.wait_until(own_word=ftag)
            self.play(*appear(ftag), run_time=1.0)
            self.ftag = ftag

            # power gauge
            c.wait_until("meter")
            ptag = power_tag()
            gauge = power_gauge(power)
            self.ptag, self.gauge = ptag, gauge
            self.play(*appear(ptag), FadeIn(gauge), run_time=1.2)

            # the used gate wobbles too
            c.wait_until("upset")
            upset = Flicker([view.lamps[3]], on=(RED, 0.9), off=(RED, 0.0), period=(0.25, 0.6), seed=9,
                            power=power, gain=0.04)
            self.add(upset)
            self.upset = upset
            quote = VGroup(T("“miss operation of", 30, FG, slant=ITALIC), T("the other gates on", 30, FG, slant=ITALIC),
                           T("the same package”", 30, FG, slant=ITALIC)).arrange(DOWN, buff=0.12)
            quote.move_to(_p(COL_X, -1.6))
            self.play(*appear(quote), run_time=min(1.2, c.until()))  # early: the slide's wording of the sentence
            self.c3_left = [used, spare, quote]

    # c1.build.4: the shop's heating controller; tie them to 0 V; control inputs on bigger chips
    def clip4(self):
        with self.say("c1.build.4") as c:
            box = RoundedRectangle(corner_radius=0.12, width=3.2, height=2.0).move_to(_p(COL_X - 0.4, -1.2))
            box.set_fill("#1A1D23", 1).set_stroke(DIM, 3)
            lid = Line(box.get_corner(UL), box.get_corner(UR)).set_stroke(FG, 5)
            name = T("heating controller", 30, DIM).next_to(box, DOWN, buff=0.3)
            fan = fan_icon().move_to(box.get_center() + LEFT * 0.75)
            heat = heater_icon().move_to(box.get_center() + RIGHT * 0.75)
            hand = hand_icon().move_to(box.get_right() + _p(0.75, 0.6))
            self.play(*during(disappear(*self.c3_left), 0, 0.45),
                      *during([FadeIn(box), FadeIn(lid), FadeIn(fan), FadeIn(heat)], 0.5, 1), run_time=1.2)
            self.play(*appear(name, shift=None), FadeIn(hand, shift=0.3 * LEFT), run_time=1.0)  # early: names the box being drawn
            for k in range(3):
                on = k % 2 == 0
                col = RED if on else DIM
                self.play(Rotate(hand, 0.35 if on else -0.35), *[m.animate.set_stroke(col) for m in (*fan, *heat)],
                          run_time=0.7)
                self.wait(0.25)

            # inside
            c.wait_until("inside")
            chip = S3.DipChip(14, "IC", pitch=0.26)
            chip.remove(chip.label)
            chip.move_to(box.get_center() + DOWN * 0.15)
            loose = VGroup()
            for n in (9, 10, 12, 13):
                p = chip.pin(n).get_top()
                end = p + _p(0.12 * (n % 3 - 1), 0.45)
                loose.add(Line(p, end).set_stroke(RED, 3), Circle(radius=0.05).move_to(end).set_stroke(RED, 3))
            self.play(Rotate(lid, 0.55, about_point=lid.get_start()), FadeOut(fan), FadeOut(heat), FadeOut(hand),
                      run_time=1.2)
            self.play(FadeIn(chip), *[Create(m) for m in loose], run_time=1.0)

            # the fix: back on the board
            c.wait_until("fix")
            fb = self.fb
            b = fb.board
            item = checklist().items[3]
            tick = check_mark().scale(0.75)
            item.move_to(_p(COL_X + 0.3, 0.7))
            tick.next_to(item[0], LEFT, buff=0.22)
            for f in (self.hum, self.outs, self.upset):
                f.stop()
                self.remove(f)
            self.waves.clear_updaters()
            shown = [b, *fb.power, fb.chip, fb.ic1_shown, *fb.wires, *fb.ic2_power, fb.ic2, fb.ic2_shown,
                     *fb.ic2_wires]
            self.play(*during(disappear(box, lid, chip, loose, name, self.view, self.waves, self.ftag), 0, 0.45),
                      *during([FadeIn(VGroup(*shown))], 0.5, 1), *during(appear(item), 0.5, 1), run_time=1.2)
            self.remove(VGroup(*shown))
            self.add(*shown)
            bfl = Flicker([ic2_strip(b, n) for n in SPARE_OUT], on=(RED, 0.9), off=(TEAL, 0.0),
                          period=(0.15, 0.4), seed=5, power=self.power, gain=0.05)
            self.add(bfl)
            self.play(*[Create(t) for t in fb.ties], run_time=1.0)
            bfl.stop()
            self.remove(bfl)
            self.play(self.power.animate.set_value(0.1), GrowFromCenter(tick), run_time=min(0.9, c.until("control")))
            self.item4 = VGroup(item, tick)

            # control inputs on bigger chips
            c.wait_until("control")
            big = S3.DipChip(16, "IC", pitch=0.32)
            big.remove(big.label)
            big.move_to(_p(COL_X - 0.6, -2.4))
            cp = big.pin(11)
            cp.set_fill(YELLOW, 1)
            level = Line(_p(COL_X - 2.1, -0.9), _p(COL_X + 0.9, -0.9)).set_stroke(DIM, 4)
            lvl_t = T("idle level", 30, FG).next_to(level, UP, buff=0.12).align_to(level, LEFT)
            cw = Line(cp.get_top(), [cp.get_x(), level.get_y(), 0]).set_stroke(YELLOW, 5)
            book = booklet_icon().move_to(_p(COL_X + 1.7, -2.3))
            book_t = T("pin-out", 28, DIM).next_to(book, DOWN, buff=0.15)
            self.play(FadeIn(big), Create(level), *appear(lvl_t, shift=None), run_time=1.2)  # early: names the level the wire goes to
            self.play(Create(cw), FlashAround(cp, color=YELLOW, run_time=1.0), FadeIn(book), *appear(book_t),
                      run_time=1.2)  # early: the booklet sits beside the chip it documents
            self.ctrl = [big, level, lvl_t, cw, book, book_t]

    # c1.build.5: never tie an output; power goes with switching, back in part 2
    def clip5(self):
        with self.say("c1.build.5") as c:
            fb = self.fb
            b = fb.board
            row, col = ic2_col(6)
            bad = S3.wire(b.hole(9, col), b.rail_hole(2, col), RED, width=6)
            onums = [fb.ic2_nums[n - 1] for n in SPARE_OUT]
            self.play(*during(disappear(*self.ctrl), 0, 0.45), *during(appear(*onums, shift=None), 0.5, 1),
                      run_time=1.0)  # early: the output pins' numbers, as "output" is said
            self.play(Create(bad), run_time=1.0)

            c.wait_until("short")
            strip6 = ic2_strip(b, 6)
            sp = spark(bad[0].get_center())
            stag = VGroup(T("5 V into a", 32, RED), T("short circuit", 32, RED)).arrange(DOWN, buff=0.12)
            stag.move_to(_p(COL_X, -0.55))
            self.play(strip6.animate.set_fill(GOLD, 0.9), *appear(stag), run_time=1.0)  # early: names what the sentence describes
            c.wait_until("short circuit")
            self.play(GrowFromCenter(sp), run_time=0.8)
            self.play(FadeOut(sp, scale=1.4), run_time=0.6)

            rings = [Circle(radius=0.26).move_to(fb.ic2.pin(n).get_center()).set_stroke(GREEN, 4) for n in SPARE_OUT]
            ok = VGroup(check_mark().scale(0.8), T("unused output:", 32, GREEN)).arrange(RIGHT, buff=0.25)
            ok2 = T("leave it alone", 32, GREEN)
            okg = VGroup(ok, ok2).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to(_p(COL_X, -2.3))
            c.wait_until("outputs a one")
            self.play(*during(disappear(bad, stag), 0, 0.45), *during([strip6.animate.set_fill(TEAL, 0.0)], 0, 0.45),
                      *during(appear(okg), 0.5, 1), *during([GrowFromCenter(r) for r in rings], 0.5, 1),
                      run_time=1.4)

            # plant
            c.wait_until("remember")
            plant = T("power goes with how often it switches", 36, GOLD).move_to(_p(0, 3.45))
            back = T("back in part 2", 30, DIM).move_to(_p(0, 2.85))
            self.play(*swap(self.ptag, plant), run_time=1.4)
            c.wait_until("part two")
            self.play(*appear(back), run_time=1.0)
        self.wait(3.0)
