"""Chapter 1, scene 8: when it fails (scope, DMM, the three-step hunt, 1.2 V), and the recap.
Clips c1.faults.1 – c1.faults.5.

Board: s7's finished_board() (shifted up 0.4). Meter: s5's multimeter_drawing, dial turned to V;
its reading is kept as a separate object (self.rd) and swapped. Probe readings on IC1 only at pins
14, 7, 1, 2, 3, 9 (assessed work); the 1.2 V reading is shown off the board.
Recap: seven tiles built from s2..s7's helpers; end card: the tiles small + the two chains + "Next".
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

S1 = load_scene("ch1_s1_hook")
S2 = load_scene("ch1_s2_kit")
S3 = load_scene("ch1_s3_breadboard")
S4 = load_scene("ch1_s4_chips")
S5 = load_scene("ch1_s5_leds")
S6 = load_scene("ch1_s6_wiring")
S7 = load_scene("ch1_s7_build")
L8 = S1.L8

BLACK_LEAD = "#3A3D44"
BOARD_UP = UP * 0.4
M_AT = np.array([-4.3, -1.05, 0])      # the meter during the hunt (scale 0.75)


def _p(x, y):
    return np.array([x, y, 0.0])


# ── drawings ──────────────────────────────────────────────────────────────────────
def scope_drawing():
    """Oscilloscope, 5.6 x 4.0 on ORIGIN; .vlab / .tlab (axis labels) built but not added; .bnc."""
    g = VGroup()
    body = RoundedRectangle(corner_radius=0.25, width=5.6, height=4.0).set_fill("#2B2E35", 1).set_stroke(BLUE, 4)
    screen = Rectangle(width=3.8, height=3.2).set_fill("#10201A", 1).set_stroke(DIM, 2).move_to(_p(-0.7, 0.1))
    grid = VGroup(*[Line(_p(x, -1.5), _p(x, 1.7)) for x in np.linspace(-2.6, 1.2, 9)[1:-1]],
                  *[Line(_p(-2.6, y), _p(1.2, y)) for y in np.linspace(-1.5, 1.7, 7)[1:-1]])
    grid.set_stroke("#28382F", 1.5)
    o = _p(-2.3, -1.0)
    yax = Arrow(o, _p(-2.3, 1.45), buff=0, stroke_width=3, color=FG, max_tip_length_to_length_ratio=0.08)
    xax = Arrow(o, _p(0.95, -1.0), buff=0, stroke_width=3, color=FG, max_tip_length_to_length_ratio=0.08)
    pts, x0, per = [], -2.0, 0.95
    for i in range(3):
        a = x0 + i * per
        pts += [_p(a, -0.6), _p(a, 0.6), _p(a + per / 2, 0.6), _p(a + per / 2, -0.6)]
    pts.append(_p(x0 + 3 * per, -0.6))
    wave = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 4)
    knobs = VGroup()
    for y in (1.1, 0.2):
        k = Circle(radius=0.28).set_fill("#3A3E47", 1).set_stroke(FG, 2.5).move_to(_p(1.95, y))
        knobs.add(k, Line(k.get_center(), k.get_center() + _p(0.1, 0.2), stroke_width=4, color=FG))
    bnc = VGroup(Circle(radius=0.22).set_fill("#111111", 1).set_stroke(FG, 3),
                 Dot(radius=0.07, color=FG)).move_to(_p(1.95, -1.2))
    g.add(body, screen, grid, yax, xax, wave, knobs, bnc)
    g.bnc = bnc
    g.vlab = T("voltage", 30).next_to(yax.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.1)
    g.tlab = T("time", 30).next_to(xax.get_end(), DOWN, buff=0.1)
    return g


def make_meter(reading="- - -", color=DIM):
    m = S5.multimeter_drawing(reading, color)
    m.pointer.rotate(60 * DEGREES, about_point=m.dial.get_center())
    m.dial_labels[0].set_color(YELLOW)
    m.dial_labels[1].set_color(FG)
    for lab in m.dial_labels:          # so they stay >= 28 when the meter is shown at 0.75
        lab.scale(1.35)
    return m


def lead(start, end, color, outline, above=False, dip=0.9):
    """A probe: cable from a jack, tip touching `end` from below (or from above)."""
    L = 0.5
    end = np.array(end)
    far = end + (UP if above else DOWN) * L
    c2 = far + (UP * 1.1 if above else DOWN * dip)
    cable = CubicBezier(np.array(start), np.array(start) + DOWN * dip, c2, far).set_stroke(color, 6)
    tip = Rectangle(width=0.16, height=L).set_fill(color, 1).set_stroke(outline, 2).move_to((end + far) / 2)
    return VGroup(cable, tip)


def chip(pitch, label=None):
    ch = S3.DipChip(14, "74HC00", pitch=pitch)
    ch.remove(ch.label)
    if label:
        ch.label = T(label, 28).move_to(ch.body)
        ch.add(ch.label)
    return ch


def flag_icon():
    pole = Line(_p(0, -0.5), _p(0, 0.55)).set_stroke(FG, 5)
    cloth = Polygon(_p(0, 0.55), _p(0.7, 0.32), _p(0, 0.08)).set_fill(YELLOW, 1).set_stroke(YELLOW, 2)
    return VGroup(pole, cloth)


def bin_icon():
    body = Polygon(_p(-1.2, 0.8), _p(1.2, 0.8), _p(0.9, -0.8), _p(-0.9, -0.8)).set_fill(BG, 1).set_stroke(FG, 4)
    rim = Line(_p(-1.35, 0.8), _p(1.35, 0.8)).set_stroke(FG, 5)
    ribs = VGroup(*[Line(_p(x, 0.55), _p(x * 0.8, -0.6)).set_stroke(DIM, 3) for x in (-0.5, 0, 0.5)])
    g = VGroup(body, ribs, rim)
    g.set_z_index(2)
    return g


def component_box():
    box = RoundedRectangle(corner_radius=0.1, width=2.6, height=1.5).set_fill(BLUE, 0.1).set_stroke(BLUE, 4)
    chips = VGroup(*[chip(0.16) for _ in range(3)]).arrange(DOWN, buff=0.12).move_to(box)
    return VGroup(box, chips)


def crack(ch):
    b = ch.body
    w, h = b.width, b.height
    c = b.get_center()
    pts = [c + _p(-0.05 * w, 0.5 * h), c + _p(0.04 * w, 0.18 * h), c + _p(-0.06 * w, -0.05 * h),
           c + _p(0.07 * w, -0.25 * h), c + _p(0.0, -0.5 * h)]
    return VMobject().set_points_as_corners(pts).set_stroke(FG, 4)


def fit(g, w, h):
    g.scale(min(w / g.width, h / g.height))
    return g


# ── recap pictures (centred on ORIGIN) ─────────────────────────────────────────────
def pic_box():
    return S2.prototyping_box()


def pic_board():
    b = S3.Breadboard(cols=12, pitch=0.36)
    for s in b.all_strips():
        s.set_fill(TEAL, 0.9)
    ch = S3.dip_chip(b, 2)
    ch.remove(ch.label)
    return VGroup(b, ch)


def pic_chip():
    ch = chip(0.36)
    ch.pin(14).set_fill(GOLD, 1)
    ch.pin(7).set_fill(DIM, 1)
    ch.scale(1.25)
    txt = VGroup(T("74", 30, S4.SPLIT_COLORS[0]), T("|", 30, DIM), T("HC", 30, S4.SPLIT_COLORS[1]),
                 T("|", 30, DIM), T("00", 30, S4.SPLIT_COLORS[2])).arrange(RIGHT, buff=0.12)
    txt.move_to(ch.body)
    return VGroup(ch, txt)


def pic_led():
    led = S5.led_drawing()
    led.scale_to_fit_height(2.6)
    res = S5.resistor_drawing()
    res.scale_to_fit_width(3.6)
    return VGroup(led, res).arrange(RIGHT, buff=0.5)


def pic_excerpt():
    g = S6.logbook_excerpt(struck=True)
    g.list.shift(RIGHT * 0.9)
    return g


def pic_checklist():
    cl = S7.checklist()
    for t in cl.ticks:
        cl.add(t)
    bd = S7.finished_board()
    return VGroup(cl, bd).arrange(RIGHT, buff=0.6)


def pic_meter():
    return make_meter("1.2 V", RED)


PICS = [pic_box, pic_board, pic_chip, pic_led, pic_excerpt, pic_checklist, pic_meter]
CAPS = [["switches in,", "displays out,", "5 V and clock", "signal built in"],
        ["columns joined,", "the trench", "splits them"],
        ["notch = pin 1;", "7 ground, 14 5 V"],
        ["one way round,", "with a resistor;", "bands give", "the value"],
        ["label, list,", "strike off"],
        ["power first;", "unused inputs to 0 V,", "never outputs"],
        ["probe in order:", "supply, clock signal,", "signal path"]]
TOP_X, BOT_X = [-5.1, -1.7, 1.7, 5.1], [-4.6, 0.0, 4.6]
TOP_Y, BOT_Y = 2.6, -1.0


def slot_frame(k):
    if k < 4:
        return RoundedRectangle(corner_radius=0.12, width=3.25, height=1.8).move_to(_p(TOP_X[k], TOP_Y))
    return RoundedRectangle(corner_radius=0.12, width=4.2, height=1.8).move_to(_p(BOT_X[k - 4], BOT_Y))


def chain(lit=True):
    """L8's three-flip-flop chain (as the hook draws it), centred on ORIGIN; returns (lines, texts, C)."""
    C = L8.build_chain()
    clock = [C.bus, *C.jdots, *C.clk_ws, C.clk_l]
    if not lit:
        for m in C.all:
            if not any(m is k for k in clock):
                m.set_color(DIM)
        for f in C.ffs:
            f.tri.set_fill(BG, 1)
    texts = [*C.names, *C.qls, C.din, C.clk_l]
    for f in C.ffs:
        f.remove(f.d_l, f.q_l)
        texts += [f.d_l, f.q_l]
    lines = VGroup(*[m for m in C.all if not any(m is t for t in texts)])
    texts = VGroup(*texts)
    shift = -VGroup(lines, texts).get_center()
    lines.shift(shift)
    texts.shift(shift)
    return lines, texts, C


def light_up(C):
    out = []
    for f in C.ffs:
        out += [f.box.animate.set_stroke(FG), f.tri.animate.set_stroke(FG),
                f.d_w.animate.set_stroke(BLUE), f.q_w.animate.set_stroke(GREEN),
                f.d_l.animate.set_color(BLUE), f.q_l.animate.set_color(GREEN)]
    out += [m.animate.set_stroke(GREEN) for m in (*C.links, C.tail, *C.risers)]
    out += [m.animate.set_color(GREEN) for m in (*C.dots, *C.qls)]
    out += [m.animate.set_color(FG) for m in C.names]
    out.append(C.din.animate.set_color(BLUE))
    return out


class Faults(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.end_card()

    # ── helpers ──
    def moves(self, mobs, k, about, shift):
        return [m.animate.scale(k, about_point=about).shift(shift) for m in mobs]

    def meter_to(self, scale, at):
        """Animations moving the meter and its reading to `scale` (absolute) centred at `at`."""
        k = scale / self.msc
        about = self.meter.get_center()
        d = np.array(at) - about
        self.msc = scale
        return self.moves([self.meter, self.rd], k, about, d)

    def read(self, text, color, rt=0.7, tick=False):
        new = Mono(text, 40, color).scale(self.msc).move_to(self.meter.display)
        anims = swap(self.rd, new, shift=0.1 * UP)
        if self.mtick is not None:
            anims += during(disappear(self.mtick), 0, 0.45)
            self.mtick = None
        self.play(*anims, run_time=rt)
        self.rd = new
        if tick:
            t = check_mark().scale(0.8).next_to(self.meter.display, RIGHT, buff=0.25)
            self.play(GrowFromCenter(t), run_time=0.5)
            self.mtick = t

    def red_lead(self, n):
        p = self.bd.chip.pin(n)
        above = n > 7
        pt = p.get_top() if above else p.get_bottom()
        return lead(self.meter.jack_red.get_center(), pt, RED, RED, above=above)

    def black_lead(self):
        return lead(self.meter.jack_com.get_center(), self.bd.board.rail_hole(2, 1), BLACK_LEAD, DIM, dip=0.8)

    def probe(self, n, rt=0.9):
        new = self.red_lead(n)
        anims = [Transform(self.red, new)]
        if n not in (7, 14):
            num = self.bd.pin_nums[n - 1]
            if n > 7:      # top row: the number sits above the pin, as 1 2 3 sit below theirs
                pin = self.bd.chip.pin(n)    # just left of the probe tip (pin 8, to the right, is never probed)
                num.move_to(pin.get_top() + UP * (0.04 + num.height / 2) + LEFT * (0.13 + num.width / 2)).set_z_index(5)
            self.nums_on.append(num)
            anims += during(appear(num, shift=None), 0.4, 1)
        self.play(*anims, run_time=rt)

    # ── c1: scope, ground clip, DMM ──
    def clip1(self):
        with self.say("c1.faults.1") as c:
            sc = scope_drawing().scale(1.15).move_to(UP * 0.45)
            vlab, tlab = sc.vlab, sc.tlab
            self.play(FadeIn(sc, shift=0.2 * UP), run_time=1.2)
            c.wait_until(own_word=vlab)
            self.play(*appear(vlab, tlab, lag=0.4), run_time=1.0)
            tag = T("takes desk space: for when you're really stuck", 34, DIM).move_to(_p(0, -2.65))
            c.wait_until("desk space", own_word=tag)
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("probe")
            bd = S7.finished_board().shift(BOARD_UP)
            self.bd = bd
            k = 0.68
            about = sc.get_center()
            target = _p(-4.15, 1.35)
            tag2 = VGroup(T("takes desk space:", 30, DIM), T("for when you're really stuck", 30, DIM))
            tag2.arrange(DOWN, buff=0.12).move_to(_p(-4.0, -0.75))
            self.play(*self.moves([sc, vlab, tlab], k, about, target - about),
                      *swap(tag, tag2), FadeIn(bd, shift=0.3 * LEFT), run_time=1.5)
            # the scope probe and its ground clip
            hole = bd.board.rail_hole(2, 1)
            body = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.2).set_fill(BLUE, 0.4).set_stroke(BLUE, 3)
            body.move_to(_p(-2.6, -2.9))
            cable = CubicBezier(sc.bnc.get_center(), sc.bnc.get_center() + DOWN * 1.2,
                                body.get_left() + LEFT * 0.8, body.get_left()).set_stroke(BLUE, 4)
            gnd = CubicBezier(body.get_right(), body.get_right() + RIGHT * 0.6,
                              hole + DOWN * 0.9, hole + DOWN * 0.2).set_stroke(BLACK_LEAD, 4)
            clipm = VGroup(Polygon(_p(-0.12, -0.2), _p(0.12, -0.2), _p(0.07, 0.18), _p(-0.07, 0.18)),
                           Line(_p(-0.09, 0.05), _p(0.09, 0.05))).set_fill(BLACK_LEAD, 1).set_stroke(FG, 2)
            clipm.move_to(hole + DOWN * 0.05)
            self.play(Create(cable), FadeIn(body), run_time=0.9)
            self.play(Create(gnd), FadeIn(clipm, shift=0.5 * DOWN), run_time=0.7)
            glab = T("probe GND to circuit GND", 30, FG).move_to(_p(2.4, -3.3))
            gtick = check_mark().scale(0.8).next_to(glab, RIGHT, buff=0.25)
            c.wait_until("ground", own_word=glab)
            self.play(*appear(glab), FlashAround(clipm, color=GREEN), run_time=1.0)
            self.play(GrowFromCenter(gtick), run_time=0.5)

            c.wait_until("dmm")
            meter = make_meter()
            meter.move_to(_p(-4.3, 0.15))
            meter.remove(meter.reading)
            self.meter, self.rd, self.msc, self.mtick = meter, meter.reading, 1.0, None
            self.nums_on = []
            mlab = T("digital multimeter (DMM)", 30).next_to(meter, DOWN, buff=0.25)
            out = [FadeOut(m, shift=2 * LEFT) for m in (sc, vlab, tlab, tag2, cable, body, gnd, clipm)]
            self.play(*during(out, 0, 0.5), *during([FadeIn(meter, shift=2 * RIGHT), FadeIn(self.rd, shift=2 * RIGHT)], 0.45, 0.8),
                      *during(appear(mlab), 0.7, 1), run_time=1.8)
            self.mlab = mlab
            self.cleanup1 = [glab, gtick]

    # ── c2: the hunt in three steps ──
    def clip2(self):
        with self.say("c1.faults.2") as c:
            items = []
            for k, s in enumerate(["supply pins", "clock signal", "follow the signal"]):
                items.append(VGroup(T(str(k + 1), 34, GOLD), T(s, 34)).arrange(RIGHT, buff=0.25))
            VGroup(*items).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            VGroup(*items).move_to(_p(0, 0)).to_edge(LEFT, buff=1.1).set_y(2.45)
            ticks = [check_mark().scale(0.7).next_to(it, LEFT, buff=0.2) for it in items]
            mh = self.meter.height * 0.75
            mlab_to = _p(M_AT[0], M_AT[1] - mh / 2 - 0.25 - self.mlab.height / 2)
            self.play(*disappear(*self.cleanup1), *self.meter_to(0.75, M_AT),
                      self.mlab.animate.move_to(mlab_to), run_time=1.0)
            self.play(*appear(*items, lag=0.3), run_time=1.2)  # early: the plan shown whole, then walked

            def step(k):
                anims = [GrowFromCenter(ticks[k]), items[k][1].animate.set_color(YELLOW)]
                if k:
                    anims.append(items[k - 1][1].animate.set_color(FG))
                return anims

            # step 1: supply pins
            c.wait_until("supply")
            self.red = self.red_lead(14)
            self.black = self.black_lead()
            self.play(*step(0), *during(disappear(self.mlab), 0, 0.5),
                      *during([FadeIn(self.black), FadeIn(self.red)], 0.4, 1), run_time=1.0)
            c.wait_until("five volts")
            self.read("5.0 V", GOLD, tick=True)
            c.wait_until("zero volts")
            self.probe(7, rt=0.8)
            self.read("0.0 V", DIM, tick=True)

            # the short inset
            c.wait_until("short")
            panel = RoundedRectangle(corner_radius=0.15, width=7.0, height=5.6).set_stroke(DIM, 2).move_to(_p(2.6, 0.1))
            chips, reads = [], []
            for x in (1.05, 4.15):
                for y in (1.3, -0.8):
                    ch = chip(0.3).move_to(_p(x, y))
                    ch.pin(14).set_fill(RED, 1)
                    chips.append(ch)
                    reads.append(Mono("0.0 V", 30, RED).next_to(ch.pin(14), UP, buff=0.12))
            q = T("short between 5 V and 0 V?", 34, t2c={"5 V": GOLD, "0 V": DIM}).move_to(_p(2.6, -2.2))
            blank = Mono("- - -", 40, DIM).scale(self.msc).move_to(self.meter.display)
            leave = disappear(self.bd, self.red, self.black, self.mtick)
            self.mtick = None
            self.play(*during(leave, 0, 0.45), *swap(self.rd, blank, shift=0.1 * UP),
                      *during([FadeIn(panel), *[FadeIn(ch) for ch in chips]], 0.5, 1), run_time=1.4)
            self.rd = blank
            self.play(*appear(*reads, q, lag=0.2), run_time=1.2)  # early: the question beside its readings

            # step 2: the clock signal inset
            c.wait_until("clock")
            gen = RoundedRectangle(corner_radius=0.08, width=1.8, height=0.8).set_fill(S2.CHIP_FILL, 1).set_stroke(DIM, 2.5)
            gen.move_to(_p(0.4, 0.1))
            slot = RoundedRectangle(corner_radius=0.05, width=0.55, height=0.22).set_fill("#111111", 1).set_stroke(DIM, 1.5)
            slot.move_to(gen.get_left() + RIGHT * 0.5)
            slide = Rectangle(width=0.18, height=0.22).set_fill(FG, 1).set_stroke(width=0).move_to(slot)
            ledd = Dot(gen.get_right() + LEFT * 0.3, radius=0.09, color=YELLOW)
            genl = T("clock", 30, DIM).next_to(gen, DOWN, buff=0.2)
            hz = Mono("1 Hz", 34, GOLD).next_to(gen, UP, buff=0.3).shift(LEFT * 0.35)
            ff1 = chip(0.32).move_to(_p(4.4, 1.6))
            ff2 = chip(0.32).move_to(_p(4.4, -1.4))
            fl1 = T("flip-flop", 28).move_to(ff1.body)
            fl2 = T("flip-flop", 28).move_to(ff2.body)
            px = ff1.pin(3).get_x()
            b1 = ff1.pin(3).get_bottom()[1]
            b2 = ff2.pin(3).get_bottom()[1]
            trunk = VMobject().set_points_as_corners([gen.get_right(), _p(2.2, 0.1)]).set_stroke(YELLOW, 6)
            br1 = VMobject().set_points_as_corners([_p(2.2, 0.1), _p(2.2, 0.95), _p(px, 0.95), _p(px, b1)]).set_stroke(YELLOW, 6)
            br2 = VMobject().set_points_as_corners([_p(2.2, 0.1), _p(2.2, -2.25), _p(px, -2.25), _p(px, b2 - 0.32)]).set_stroke(YELLOW, 6)
            jd = Dot(_p(2.2, 0.1), radius=0.09, color=YELLOW)
            gap = DashedLine(_p(px, b2 - 0.3), _p(px, b2), dash_length=0.06).set_stroke(RED, 4)
            ring = Circle(radius=0.24).set_stroke(RED, 4).move_to(ff2.pin(3))
            inset2 = [gen, slot, slide, ledd, trunk, br1, br2, jd, ff1, ff2, genl]
            self.play(*step(1), *during(disappear(*chips, *reads, q), 0, 0.45),
                      *during([FadeIn(m) for m in inset2], 0.5, 1), run_time=1.4)
            self.play(*appear(hz), run_time=0.8)
            c.wait_until("reaching")
            self.play(*[VShowPassingFlash(m.copy().set_stroke(FG, 9), time_width=0.5) for m in (trunk, br1, br2)],
                      run_time=1.4)
            asset = T("as set?", 30, YELLOW).next_to(hz, RIGHT, buff=0.3)
            c.wait_until("rate")
            self.play(*appear(asset), FlashAround(hz, color=GOLD), run_time=1.0)
            c.wait_until("easy to miss")
            self.play(*appear(fl1, fl2, shift=None, lag=0.2), run_time=0.7)
            self.play(Create(gap), GrowFromCenter(ring), run_time=0.9)

            # step 3: follow the signal, back on IC1
            c.wait_until("follow")
            self.red = self.red_lead(1)
            self.black = self.black_lead()
            self.nums_on.append(self.bd.pin_nums[0])
            self.play(*step(2), *during(disappear(*inset2, hz, asset, gap, ring, panel, fl1, fl2), 0, 0.45),
                      *during([FadeIn(self.bd), FadeIn(self.black), FadeIn(self.red), FadeIn(self.bd.pin_nums[0])], 0.5, 1),
                      run_time=1.4)
            self.read("5.0 V", GOLD)
            c.wait_until("inputs")
            self.probe(2, rt=0.6)
            self.read("5.0 V", GOLD, rt=0.5)
            c.wait_until("output")
            self.probe(3, rt=0.6)
            self.read("0.0 V", DIM, rt=0.5)
            row = VGroup(T("NAND", 36, BLUE), T("1 1", 36, GOLD), T("→", 36), T("0", 36, DIM)).arrange(RIGHT, buff=0.3)
            row.move_to(_p(2.2, 3.25))
            rtick = check_mark().scale(0.8).next_to(row, RIGHT, buff=0.3)
            self.play(*appear(row), run_time=0.8)
            self.play(GrowFromCenter(rtick), run_time=0.5)
            c.wait_until("nextpin")
            w = self.bd.wires[4].path.copy().set_stroke(YELLOW, 10)
            self.play(VShowPassingFlash(w, time_width=0.6), run_time=1.0)
            self.probe(9, rt=0.8)
            self.read("0.0 V", DIM, tick=True)

            c.wait_until("stop")
            flag = flag_icon()
            ftxt = VGroup(T("stop at the first", 34), T("fishy reading", 34, t2c={"fishy": YELLOW}))
            ftxt.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            fl = VGroup(flag, ftxt).arrange(RIGHT, buff=0.35).move_to(_p(-4.2, 2.5))
            self.flag = fl
            self.play(*during(disappear(*items, *ticks), 0, 0.45), *during(appear(flag, ftxt), 0.5, 1),
                      run_time=1.2)
            self.extra2 = [row, rtick]

    # ── c3: 1.2 V, fighting outputs, broken chip, ask ──
    def clip3(self):
        with self.say("c1.faults.3") as c:
            bx, by0, bh = 3.0, -2.5, 4.6
            band = Rectangle(width=0.7, height=bh).set_stroke(FG, 3).move_to(_p(bx, by0 + bh / 2))

            def vy(v):
                return by0 + bh * v / 5

            lo = Rectangle(width=0.7, height=vy(0.8) - vy(0)).set_fill(GREEN, 0.5).set_stroke(width=0)
            lo.move_to(_p(bx, (vy(0) + vy(0.8)) / 2))
            hi = Rectangle(width=0.7, height=vy(5) - vy(4.2)).set_fill(GREEN, 0.5).set_stroke(width=0)
            hi.move_to(_p(bx, (vy(4.2) + vy(5)) / 2))
            l5 = T("5 V", 32, GOLD).next_to(_p(bx - 0.35, vy(5)), LEFT, buff=0.2)
            l0 = T("0 V", 32, DIM).next_to(_p(bx - 0.35, vy(0)), LEFT, buff=0.2)
            near = T("near 0 V or near 5 V only", 32).move_to(_p(bx, -3.15))
            sweep_clear(self, *self.meter_to(1.0, _p(-3.4, -0.3)),
                        FadeIn(band), FadeIn(lo), FadeIn(hi), FadeIn(l5), FadeIn(l0),
                        keep=[self.meter, self.rd, *self.flag], run_time=1.6)
            c.wait_until("near zero", own_word=near)
            self.play(*appear(near), run_time=1.0)
            c.wait_until("one point two")
            mk = Line(_p(bx - 0.5, vy(1.2)), _p(bx + 0.5, vy(1.2))).set_stroke(RED, 6)
            mkl = T("1.2 V", 32, RED).next_to(mk, RIGHT, buff=0.25)
            self.read("1.2 V", RED, rt=0.8)
            self.play(GrowFromCenter(mk), *appear(mkl), run_time=1.0)

            # two outputs fighting
            c.wait_until("fight")
            ga, gb = S4.nand_gate().scale(1.2).move_to(_p(-4.6, 1.5)), S4.nand_gate().scale(1.2).move_to(_p(-4.6, -1.5))
            stubs = VGroup(*[Line(g.inp(i) + LEFT * 0.6, g.inp(i)).set_stroke(FG, 4) for g in (ga, gb) for i in (0, 1)])
            xj = -1.6
            oa = Line(ga.out(), _p(xj, 1.5)).set_stroke(FG, 4)
            ob = Line(gb.out(), _p(xj, -1.5)).set_stroke(FG, 4)
            stray = Line(_p(xj, 1.5), _p(xj, -1.5)).set_stroke(RED, 6)
            jdot = Dot(_p(xj, 0), radius=0.1, color=RED)
            tap = Line(_p(xj, 0), _p(0.4, 0)).set_stroke(FG, 4)
            rail = Line(_p(0.6, -2.3), _p(2.8, -2.3)).set_stroke(DIM, 8)
            rl = T("0 V", 30, DIM).next_to(rail, LEFT, buff=0.2)
            sweep_clear(self, *self.meter_to(0.8, _p(4.9, -0.1)),
                        *[FadeIn(m) for m in (ga, gb, stubs, oa, ob, tap, rail, rl)],
                        keep=[self.meter, self.rd], run_time=1.6)
            self.red = lead(self.meter.jack_red.get_center(), _p(0.4, 0), RED, RED)
            self.black = lead(self.meter.jack_com.get_center(), _p(1.7, -2.3), BLACK_LEAD, DIM, dip=0.6)
            self.play(Create(stray), FadeIn(jdot), FadeIn(self.red), FadeIn(self.black), run_time=1.0)
            up = Arrow(_p(-2.6, 1.8), _p(-2.6, 2.9), buff=0, color=GOLD, stroke_width=6)
            upl = T("1", 36, GOLD).next_to(up, LEFT, buff=0.15)
            dn = Arrow(_p(-2.6, -1.8), _p(-2.6, -2.9), buff=0, color=DIM, stroke_width=6)
            dnl = T("0", 36, DIM).next_to(dn, LEFT, buff=0.15)
            c.wait_until("pulling to one")
            self.play(GrowArrow(up), *appear(upl), run_time=0.8)
            c.wait_until("to zero")
            self.play(GrowArrow(dn), *appear(dnl), run_time=0.8)

            # or the chip is broken
            c.wait_until("broken")
            ch = chip(0.55).move_to(_p(-2.6, 0.4))
            cr = crack(ch)
            ch.add(cr)
            newred = lead(self.meter.jack_red.get_center(), ch.pin(3).get_bottom(), RED, RED)
            self.play(*during(disappear(ga, gb, stubs, oa, ob, stray, jdot, tap, up, upl, dn, dnl), 0, 0.45),
                      *during([FadeIn(ch)], 0.5, 1), Transform(self.red, newred), run_time=1.3)

            # bin it
            c.wait_until("bin")
            bn = bin_icon().move_to(_p(-2.6, -2.1))
            self.play(*disappear(self.red, self.black, rail, rl), FadeIn(bn), run_time=0.9)
            self.play(ch.animate.scale(0.45).rotate(0.4).move_to(_p(-2.6, -2.0)), run_time=1.0, rate_func=rush_into)
            self.remove(ch)
            box = component_box().move_to(_p(1.0, -1.9))
            c.wait_until("back in the box")
            self.play(FadeIn(box), run_time=0.8)
            x = cross_mark().scale(3.0).move_to(box)
            self.play(GrowFromCenter(x), run_time=0.6)
            trap = T("a booby trap for next week's class", 36, t2c={"booby trap": RED}).move_to(_p(-0.8, 2.75))
            c.wait_until("booby trap", own_word=trap)
            self.play(*appear(trap), run_time=1.0)

            # ask a demonstrator
            c.wait_until("ask")
            hand = S7.hand_icon().scale(2.6)
            arm = Line(hand.get_bottom() + DOWN * 0.02, hand.get_bottom() + DOWN * 1.0).set_stroke(FG, 5)
            hd = VGroup(arm, hand).move_to(_p(-5.4, 0.3))
            sweep_clear(self, FadeIn(hd, shift=0.3 * UP), keep=[trap], run_time=1.2)
            demo = S6.demonstrator_icon().scale(1.7).move_to(_p(-2.8, 0.2))
            c.wait_until("ask a demonstrator")
            self.play(FadeIn(demo, shift=0.2 * UP), *disappear(trap), run_time=0.9)
            page = S6.logbook_excerpt(struck=True).page
            page.scale_to_fit_height(3.4).move_to(_p(1.0, 0.0))
            tb = S7.finished_board()
            tb.scale_to_fit_width(3.7).move_to(_p(4.75, 0.0))
            gaze = DashedLine(demo[0].get_right() + RIGHT * 0.1, page.get_left() + _p(-0.1, 1.0),
                              dash_length=0.1).set_stroke(DIM, 3)
            c.wait_until("clear")
            self.play(FadeIn(page), Create(gaze), run_time=1.0)
            c.wait_until("tidy wiring")
            self.play(FadeIn(tb), run_time=1.0)
            tk = check_mark().scale(1.8).move_to(_p(2.9, 2.6))
            self.play(GrowFromCenter(tk), run_time=0.7)

    # ── c4: the recap ──
    def clip4(self):
        with self.say("c1.faults.4") as c:
            frames = [slot_frame(k).set_stroke(DIM, 2) for k in range(7)]
            sweep_clear(self, *[FadeIn(f) for f in frames], run_time=1.2)
            self.tiles = []
            for k in range(7):
                fr = frames[k]
                pic = fit(PICS[k](), fr.width - 0.25, fr.height - 0.2).move_to(fr)
                cap = VGroup(*[T(s, 28) for s in CAPS[k]]).arrange(DOWN, buff=0.07)
                cap.next_to(fr, DOWN, buff=0.12)
                c.wait_until(f"r{k + 1}")
                self.play(FadeIn(pic, scale=0.9), run_time=0.8)  # early: a small copy of an earlier picture
                for ln in cap:
                    try:
                        c.wait_until(own_word=ln)
                    except KeyError:
                        pass
                    self.play(*appear(ln, shift=None), run_time=0.6)
                self.tiles += [pic, cap]
            self.frames = frames

    # ── c5: next, the shift register ──
    def clip5(self):
        with self.say("c1.faults.5") as c:
            lines, texts, C = chain(lit=False)
            for m in (lines, texts):
                m.shift(UP * 0.3)
            c.wait_until("lecture")
            old = [*self.frames, *self.tiles]
            self.play(*during([FadeOut(m, scale=0.4) for m in old], 0, 0.5),
                      *during([FadeIn(lines, shift=0.2 * UP), FadeIn(texts, shift=0.2 * UP)], 0.5, 1),
                      run_time=1.4)
            c.wait_until("wire lecture")
            self.play(*light_up(C), run_time=1.2)
            bit = L8.digit("1", C.ffs[0])
            c.wait_until("chain")
            self.play(FadeIn(bit), *[VShowPassingFlash(C.bus.copy().set_stroke(FG, 8), time_width=0.5)], run_time=0.7)
            for i in (1, 2):
                self.play(bit.animate.move_to(L8.digit_pos(C.ffs[i])),
                          VShowPassingFlash(C.bus.copy().set_stroke(FG, 8), time_width=0.5), run_time=0.6)

            # a second chain, joined by a serial link
            c.wait_until("link")
            k = 0.6
            about = VGroup(lines, texts).get_center()
            to = _p(-3.45, 0.3)
            lines2, texts2, C2 = chain(lit=True)
            lines2.scale(k, about_point=ORIGIN).shift(_p(3.45, 0.3))
            self.play(*during(disappear(texts), 0, 0.4),
                      *self.moves([lines, bit], k, about, to - about),
                      *during([FadeIn(lines2)], 0.5, 1), run_time=1.3)
            a = C.tail.get_end()
            b = C2.ffs[0].d_w.get_start()
            wire = Line(a, _p(b[0], a[1])).set_stroke(TEAL, 5)
            lab = T("serial link", 30, TEAL).next_to(wire, DOWN, buff=0.25)
            self.play(Create(wire), FadeOut(bit), run_time=0.7)
            c.wait_until("serial link", own_word=lab)
            self.play(*appear(lab), run_time=0.8)
            dots = [Dot(a, radius=0.1, color=GOLD) for _ in range(3)]
            path = Line(a, _p(b[0], a[1]))
            self.play(*[time_span(MoveAlongPath(d, path, rate_func=linear), 0.4 * i, 0.4 * i + 0.9)
                        for i, d in enumerate(dots)], run_time=1.7)
            self.play(*[FadeOut(d) for d in dots], run_time=0.4)
            self.chains = [lines, lines2, wire, lab]

    def end_card(self):
        pics = []
        xs = np.linspace(-5.6, 5.6, 7)
        for k in range(7):
            pics.append(fit(PICS[k](), 1.6, 1.0).move_to(_p(xs[k], 2.75)))
        nxt = T("Next: shift registers", 48, t2c={"Next:": YELLOW}).move_to(_p(0, -2.55))
        self.play(*[FadeIn(p) for p in pics], *appear(nxt), run_time=1.5)  # early: the end card
        self.wait(6.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
