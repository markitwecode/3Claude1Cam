"""Chapter 2, scene 4: the four-bit shift register in the simulator, run by hand. Clips c2.demo.1 – c2.demo.3.

Drawing: L8's make_ff (K = 0.6) x4, Q (GREEN) into the next D; ch1 s6's IC1a..IC2b labels and
dashed DIM outlines; ch1 s4's part-number split (74 | HC | 74 built here, same colours/tags);
ch1 s5's banded resistor (270 ohm: red violet brown) and diode symbol, LED to 0 V (ground).
L6's toggle switches: INPUT (BLUE) into IC1a's D, CLK (YELLOW) on one bus to all four clocks.
Last shot (opens s5): handover_shot().
"""
# style: 2
# handover: next
import importlib.util
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

_HERE = Path(__file__).resolve()


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L8 = _load("_l08_ch2_s3_shiftreg", _HERE.parents[2] / "l08-timing-metastability" / "scenes" / "ch2_s3_shiftreg.py")
L6 = _load("_l06_ch1_s6_transparent", _HERE.parents[2] / "l06-flip-flops-counters" / "scenes" / "ch1_s6_transparent.py")
S5 = _load("_l07_ch1_s5_leds", _HERE.parent / "ch1_s5_leds.py")


def _p(x, y):
    return np.array([x, y, 0.0])


# ── ch1 s4's part-number split, as 74 | HC | 74 ──────────────────────────────────────
SPLIT_COLORS = (BLUE, GREEN, YELLOW)
SPLIT_TAGS = ("the series", "the technology", "the function")


def part_split_74(center=ORIGIN, size=72, gap=3.0):
    g = T("74HC74", size=size).move_to(center)
    g.parts = [[g[0], g[1]], [g[2], g[3]], [g[4], g[5]]]
    g.colors = SPLIT_COLORS
    g.tags = SPLIT_TAGS
    g.cols = [np.array(center) + RIGHT * gap * (i - 1) for i in range(3)]

    def split_moves():
        out = []
        for part, col in zip(g.parts, g.cols):
            d = col - VGroup(*part).get_center()
            out += [gl.animate.shift(d) for gl in part]
        return out
    g.split_moves = split_moves
    return g


def split_box(part, color):
    box = SurroundingRectangle(VGroup(*part), color=color, buff=0.18, corner_radius=0.08)
    return box.set_stroke(color, 3).set_fill(color, 0.12).set_z_index(-1)


# ── layout ───────────────────────────────────────────────────────────────────────────
K = 0.6
FF_X = (-2.9, -0.4, 2.1, 4.6)
FY = 0.9
QY = FY + L8.PIN_Y * K                 # 1.26
HX = (L8.BOX_W / 2 + L8.WIRE) * K       # 0.96
BOT = FY - L8.BOX_H / 2 * K             # box bottom 0.12
TAPS = [x + 1.25 for x in FF_X]         # -1.65, 0.85, 3.35, 5.85
SW_X = -5.7
BUS_Y = -2.3
RES_Y, LED_Y, GND_Y = -0.4, -1.3, -1.85
TR_X0, TR_LO, TR_HI = -5.0, -3.15, -2.75
TR_HI_W, TR_PER = 0.35, 0.75
RUN = 13                                 # rising edges logged in the run
STREAM_X = [-5.0, -4.65, -4.3, -3.95]   # GOLD bits on the INPUT wire, left to right
STREAM = [1, 0, 1, 1]                    # the rightmost goes in first
WORD = [1, 0, 1, 1]                      # Q_0..Q_3 after the stream


def toggle(color):
    sw = L6.toggle(0).scale(1.3)
    sw.track.set_stroke(color, 3)
    sw.col = color
    return sw


def flip(sw, v):
    sw.v = v
    return sw.knob.animate.move_to(sw.knob_pos(v)).set_fill(sw.col if v else DIM, 1)


def ground(x, y):
    g = VGroup(*[Line(_p(x - w / 2, y - k * 0.09), _p(x + w / 2, y - k * 0.09)) for k, w in enumerate((0.38, 0.25, 0.12))])
    return g.set_stroke(DIM, 4)


def led_state(d, on):
    """Set LED d (diode + glow) lit/off directly."""
    col = GREEN if on else DIM
    d.tri.set_fill(GREEN, 1 if on else 0).set_stroke(col)
    d.bar.set_stroke(col)
    d.glow.set_fill(GREEN, 0.3 if on else 0)
    d.on = on


def led_anims(d, on):
    col = GREEN if on else DIM
    d.on = on
    return [d.tri.animate.set_fill(GREEN, 1 if on else 0).set_stroke(col),
            d.bar.animate.set_stroke(col), d.glow.animate.set_fill(GREEN, 0.3 if on else 0)]


def build():
    R = VGroup()
    R.title = T("Four-Bit Shift Register", 44).move_to(_p(-0.5, 3.25))
    R.sim = T("simulation", 28, DIM).next_to(R.title, RIGHT, buff=0.4).align_to(R.title, DOWN)
    # flip-flops
    R.ffs = []
    for x in FF_X:
        f = L8.make_ff()
        f.scale(K, about_point=ORIGIN).shift(_p(x, FY))
        for lb in (f.d_l, f.q_l):
            lb.scale(1.3, about_point=lb.get_center())
        R.ffs.append(f)
    R.links = [Line(_p(FF_X[i] + HX, QY), _p(FF_X[i + 1] - HX, QY)).set_stroke(GREEN, 5) for i in range(3)]
    R.tail = Line(_p(FF_X[3] + HX, QY), _p(6.2, QY)).set_stroke(GREEN, 5)
    R.qls = [MathTex(f"Q_{i}", font_size=40, color=GREEN).move_to(_p(t, QY + 0.38)) for i, t in enumerate(TAPS)]
    # chips
    R.ics = [T(n, 30, YELLOW).move_to(_p(x, 1.98)) for n, x in zip(("IC1a", "IC1b", "IC2a", "IC2b"), FF_X)]
    R.outlines, R.chip_tags = [], []
    for a, b in ((0, 1), (2, 3)):
        x0, x1 = FF_X[a] - 0.82, FF_X[b] + 0.82
        o = DashedVMobject(Rectangle(width=x1 - x0, height=2.3).move_to(_p((x0 + x1) / 2, 1.17)),
                           num_dashes=60).set_stroke(DIM, 3)
        R.outlines.append(o)
        R.chip_tags.append(T("74HC74", 32).move_to(_p((x0 + x1) / 2, 2.62)))
    # outputs: Q tap -> 270 ohm -> LED -> 0 V
    R.res, R.leds, R.gnds, R.bwires, R.taps = [], [], [], [], []
    for t in TAPS:
        r = S5.resistor_drawing(("red", "violet", "brown"), length=0.55).rotate(PI / 2).move_to(_p(t, RES_Y))
        d = S5.diode_symbol(DOWN, size=0.45, color=DIM).move_to(_p(t, LED_Y))
        d.leads.set_stroke(FG, 4)
        d.glow = Circle(radius=0.3).set_stroke(width=0).set_fill(GREEN, 0).move_to(d.get_center()).set_z_index(-2)
        led_state(d, 0)
        w = VGroup(Line(_p(t, QY), _p(t, r.get_top()[1])), Line(_p(t, r.get_bottom()[1]), d.get_top()),
                   Line(d.get_bottom(), _p(t, GND_Y))).set_stroke(FG, 4)
        R.res.append(r)
        R.leds.append(d)
        R.gnds.append(ground(t, GND_Y))
        R.bwires.append(w)
        R.taps.append(Dot(_p(t, QY), radius=0.07, color=GREEN))
    R.ohm = T("270 Ω", 28).next_to(R.res[0], LEFT, buff=0.15)
    # clear of IC1a's clock wire (x = FF_X[0], stroke 5): 0.13 gap; it then sits 0.06 off its resistor
    R.ohm.align_to(_p(FF_X[0] + 0.025 + 0.13, 0), LEFT)
    R.zero_v = T("0 V", 28, DIM).next_to(R.gnds[3], RIGHT, buff=0.15)
    # switches
    R.sw_in = toggle(BLUE).move_to(_p(SW_X, QY))
    R.in_l = T("INPUT", 30, BLUE).next_to(R.sw_in, UP, buff=0.15)
    R.in_w = Line(_p(R.sw_in.get_right()[0], QY), R.ffs[0].d_w.get_start()).set_stroke(BLUE, 5)
    R.sw_clk = toggle(YELLOW).move_to(_p(SW_X, BUS_Y))
    R.clk_l = T("CLK", 30, YELLOW).next_to(R.sw_clk, UP, buff=0.15)
    R.bus = Line(_p(R.sw_clk.get_right()[0], BUS_Y), _p(FF_X[3], BUS_Y)).set_stroke(YELLOW, 5)
    R.stubs = [Line(_p(x, BOT), _p(x, BUS_Y)).set_stroke(YELLOW, 5) for x in FF_X]
    R.jdots = [Dot(_p(x, BUS_Y), radius=0.07, color=YELLOW) for x in FF_X[:3]]
    # sipo
    R.brace = span_brace(_p(TAPS[0] - 0.3, BUS_Y), _p(TAPS[3] + 0.3, BUS_Y), DOWN, color=GOLD)
    R.tag = T("serial in, parallel out", 36, YELLOW).next_to(R.brace, DOWN, buff=0.18)
    R.bits = [Mono(str(v), 36, GOLD).move_to(_p(t + 0.62, LED_Y)) for v, t in zip(WORD, TAPS)]
    return R


def circuit_parts(R):
    """Everything of the drawing that stays to the end, in drawing order."""
    out = [R.title, R.sim, *R.outlines, *R.chip_tags, *R.ics]
    for f in R.ffs:
        out += [f]
    out += [*R.links, R.tail, *R.qls]
    for i in range(4):
        out += [R.bwires[i], R.taps[i], R.res[i], R.leds[i].glow, R.leds[i], R.gnds[i]]
    out += [R.ohm, R.zero_v, R.sw_in, R.in_l, R.in_w, R.sw_clk, R.clk_l, R.bus, *R.stubs, *R.jdots]
    return out


def handover_shot():
    R = build()
    for d, v in zip(R.leds, WORD):
        led_state(d, v)
    return VGroup(*circuit_parts(R), *R.bits, R.brace, R.tag)


class DemoScene(NarratedScene):
    def construct(self):
        self.R = build()
        self.state = [0, 0, 0, 0]
        self.n_edge = 0
        self.trace = []
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)   # handover: s5 opens on this shot

    # one clock edge: CLK 0 -> 1 (logged, marked with an up-arrow), the register shifts, CLK back to 0
    def edge(self, din, rt, extra=()):
        R = self.R
        k = self.n_edge
        self.n_edge += 1
        xr = TR_X0 + 0.3 + k * TR_PER
        up = Arrow(_p(xr, TR_LO), _p(xr, TR_HI + 0.08), buff=0, stroke_width=4, color=YELLOW,
                   tip_length=0.14, max_tip_length_to_length_ratio=0.5)
        hi = Line(_p(xr, TR_HI), _p(xr + TR_HI_W, TR_HI)).set_stroke(YELLOW, 4)
        dn = Line(_p(xr + TR_HI_W, TR_HI), _p(xr + TR_HI_W, TR_LO)).set_stroke(YELLOW, 4)
        lo = Line(_p(xr + TR_HI_W, TR_LO), _p(xr + TR_PER, TR_LO)).set_stroke(YELLOW, 4)
        self.trace += [up, hi, dn, lo]
        new = [din] + self.state[:3]
        leds = []
        for d, a, b in zip(R.leds, self.state, new):
            if a != b:
                leds += led_anims(d, b)
        self.state = new
        self.play(*during([flip(R.sw_clk, 1)], 0, 0.3), *during([GrowArrow(up), Create(hi)], 0, 0.45),
                  *during(leds, 0.2, 0.55), *during([flip(R.sw_clk, 0)], 0.55, 0.85),
                  *during([Create(dn), Create(lo)], 0.55, 1.0), *extra, run_time=rt)

    def edges(self, c, din, n, cue=None, first=None, hold=0.6):
        """n edges with input din, spread over the time left to `cue` (minus a hold)."""
        for i in range(n):
            left = c.until(cue) - hold
            rt = max(0.5, min(1.2, left / (n - i)))
            if i == 0 and first:
                rt = max(rt, min(first, left))
            self.edge(din, rt)

    # ── c2.demo.1: the simulator drawing, chips, part number, LEDs ──────────────────
    def clip1(self):
        R = self.R
        with self.say("c2.demo.1") as c:
            self.play(*appear(R.title, R.sim, lag=0.3), run_time=1.0)   # early: title of the drawing
            c.wait_until("four-bit")
            self.play(*appear(*R.ffs, lag=0.25), *during([FadeIn(m) for m in (*R.links, R.tail)], 0.5, 1.0),
                      run_time=min(1.8, c.until("circuit simulator")))
            self.play(*appear(*R.qls, lag=0.2), run_time=1.0)
            c.wait_until("two chips")
            self.play(*[FadeIn(o) for o in R.outlines], run_time=1.0)
            c.wait_until("labelled")
            self.play(*appear(*R.ics, lag=0.3), run_time=1.2)
            c.wait_until("seventy-four")
            self.play(*appear(*R.chip_tags, lag=0.3), run_time=1.0)

            c.wait_until("decode")
            split = part_split_74(center=_p(-1.0, -1.2), gap=3.2)
            self.play(*appear(split), *flash([R.chip_tags[0]]), run_time=0.9)
            cols = split.cols
            tags = [T(split.tags[i], 34, color=col).move_to([cols[i][0], -2.25, 0])
                    for i, col in enumerate(split.colors)]
            boxes = [split_box(p, col) for p, col in zip(split.parts, split.colors)]
            # boxes are built where the parts land
            for b, col in zip(boxes, cols):
                b.move_to([col[0], b.get_y(), 0])
            self.play(*split.split_moves(), *during([GrowFromCenter(b) for b in boxes], 0.6, 1.0),
                      *during(appear(*tags, lag=0.3), 0.5, 1.0), run_time=1.8)
            c.wait_until("means")
            dual = T("dual D flip-flop", 30).move_to([cols[2][0], -2.85, 0])
            self.play(*appear(dual), *flash([boxes[2]]), run_time=1.0)

            c.wait_until("a light")
            out = [*boxes, *tags, dual]
            self.play(*during([FadeOut(m) for m in out] + [FadeOut(split)], 0, 0.4),
                      *during([FadeIn(m) for i in range(4) for m in (R.bwires[i], R.taps[i])], 0.4, 0.7),
                      *during([FadeIn(m) for i in range(4) for m in (R.res[i], R.leds[i].glow, R.leds[i], R.gnds[i])],
                              0.5, 1.0), run_time=2.0)
            self.play(*appear(R.zero_v), run_time=0.8)
            c.wait_until("two hundred")
            self.play(*appear(R.ohm), *flash([R.res[0]]), run_time=1.0)

            # what-if: the resistor out, the light bursts, the resistor back
            c.wait_until("boom")
            r, d = R.res[0], R.leds[0]
            t = TAPS[0]
            bypass = Line(_p(t, r.get_top()[1]), _p(t, r.get_bottom()[1])).set_stroke(FG, 4)
            self.play(r.animate.shift(RIGHT * 0.75 + UP * 0.1), *during([FadeIn(bypass)], 0.5, 1.0), run_time=1.0)
            dc = d.get_center()
            burst = VGroup(*[Line(dc + 0.42 * np.array([np.cos(a), np.sin(a), 0]),
                                  dc + 0.68 * np.array([np.cos(a), np.sin(a), 0]))
                             for a in np.linspace(0, TAU, 9)[:-1] + PI / 8]).set_stroke(RED, 5)
            self.play(d.tri.animate.set_fill(RED, 1).set_stroke(RED), d.bar.animate.set_stroke(RED),
                      d.glow.animate.set_fill(RED, 0.5), FadeIn(burst, scale=0.6), run_time=0.8)
            self.wait(min(0.8, max(0.0, c.until() - 1.4)))
            self.play(*during([FadeOut(burst), d.glow.animate.set_fill(GREEN, 0),
                               d.tri.animate.set_fill(GREEN, 0).set_stroke(DIM), d.bar.animate.set_stroke(DIM)], 0, 0.5),
                      *during([r.animate.shift(-(RIGHT * 0.75 + UP * 0.1)), FadeOut(bypass)], 0.3, 1.0),
                      run_time=min(1.2, c.until()))

    # ── c2.demo.2: the two switches; ones fill, zeros follow ────────────────────────
    def clip2(self):
        R = self.R
        with self.say("c2.demo.2") as c:
            self.play(FadeIn(R.sw_in), FadeIn(R.in_w), *appear(R.in_l), run_time=1.0)
            c.wait_until("clock signal")
            self.play(FadeIn(R.sw_clk), *appear(R.clk_l),
                      *during([Create(R.bus), *[Create(s) for s in R.stubs], *[FadeIn(j) for j in R.jdots]], 0.3, 1.0),
                      run_time=1.5)
            c.wait_until("flipped by hand")
            self.tr_label = T("CLK", 28, DIM).move_to(_p(SW_X, (TR_LO + TR_HI) / 2))
            lead = Line(_p(TR_X0, TR_LO), _p(TR_X0 + 0.3, TR_LO)).set_stroke(YELLOW, 4)
            self.trace.append(lead)
            self.play(*appear(self.tr_label), Create(lead), run_time=1.0)
            c.wait_until("rising edge")
            self.play(*flash([f.tri for f in R.ffs], color=YELLOW), run_time=1.2)

            c.wait_until("fill")
            self.play(flip(R.sw_in, 1), run_time=0.6)
            c.wait_until("four edges")
            self.edges(c, 1, 4, cue="empty", first=1.1, hold=0.9)
            c.wait_until("empty")
            self.play(flip(R.sw_in, 0), run_time=0.5)
            self.edges(c, 0, 4, hold=0.1)

    # ── c2.demo.3: a single 1 walks along and out; serial in, parallel out ─────────
    def clip3(self):
        R = self.R
        with self.say("c2.demo.3") as c:
            self.play(flip(R.sw_in, 1), run_time=0.6)
            c.wait_until("single one")
            self.edge(1, 1.1)
            self.play(flip(R.sw_in, 0), run_time=0.6)
            c.wait_until("walk")
            self.edges(c, 0, 3, cue="out", hold=0.1)
            c.wait_until("out")
            one = Mono("1", 36, GOLD).move_to(_p(6.05, QY - 0.32))
            one.set_opacity(0)
            start = one.get_center()

            def slide(m, a):
                m.move_to(start + RIGHT * 0.6 * a)
                m.set_opacity(min(1, 4 * a) if a < 0.5 else max(0, 2 - 2 * a))
            self.add(one)
            # the 1 leaves only once Q_3's LED is out (LEDs change in 0.2-0.55 of the edge)
            rt = max(1.6, min(2.2, c.until("sipo") - 0.3))
            self.edge(0, rt, extra=[time_span(UpdateFromAlphaFunc(one, slide), 0.56 * rt, rt)])
            self.remove(one)

            c.wait_until("sipo")
            stream = [Mono(str(v), 32, GOLD).move_to(_p(x, QY - 0.32)) for v, x in zip(STREAM, STREAM_X)]
            self.play(*during([FadeOut(m) for m in self.trace] + disappear(self.tr_label), 0, 0.45),
                      *during(appear(*stream, lag=0.15), 0.4, 1.0), run_time=1.3)
            c.wait_until("one wire")
            # bits go in, rightmost first, one per clock
            queue = list(zip(STREAM, stream))
            for k in range(4):
                v, head = queue.pop()
                new = [v] + self.state[:3]
                leds = []
                for d, a, b in zip(R.leds, self.state, new):
                    if a != b:
                        leds += led_anims(d, b)
                self.state = new
                rt = 0.9 if k == 0 else 0.65
                self.play(head.animate.shift(RIGHT * 0.3).set_opacity(0),
                          *[m.animate.shift(RIGHT * 0.35) for _, m in queue],
                          *during([flip(R.sw_clk, 1)], 0, 0.35), *during(leds, 0.25, 0.7),
                          *during([flip(R.sw_clk, 0)], 0.6, 0.95), run_time=rt)
                self.remove(head)
            c.wait_until("four-bit word")
            self.play(GrowFromCenter(R.brace), *appear(*R.bits, lag=0.15), run_time=1.2)
            c.wait_until("serial in")
            self.play(*appear(R.tag), run_time=1.0)
