"""Chapter 1, scene 5: LEDs and resistors. Clips c1.leds.1 – c1.leds.4.

Reusable drawings (ch1_s8 imports them via load_scene("ch1_s5_leds")):
  led_drawing()            the LED pin-out picture (.dome .rim .flat .anode .cathode)
  diode_symbol(direction)  triangle + bar + leads (.tri .bar .leads)
  resistor_drawing(bands)  banded resistor, horizontal (.leads .body .bands .tol)
  multimeter_drawing(r)    DMM (.body .display .reading .dial .pointer .dial_labels .jack_com .jack_red)
  probe_leads(meter, red_pt, black_pt)  red and black probe cables + tips (.red .black)
  worksheet_icon()         small sheet of paper
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# physical band colours (resistor colour code)
BAND = {
    "black": "#1A1A1A", "brown": "#8B5A2B", "red": "#E23B2E", "orange": "#FF7F1F",
    "yellow": "#F4D345", "green": "#3FAE49", "blue": "#3B6FE0", "violet": "#9B5DE5",
    "grey": "#9A9A9A", "white": "#F5F5F5", "gold": "#C9A227",
}
CODE_ORDER = ["black", "brown", "red", "orange", "yellow", "green", "blue", "violet", "grey", "white"]
BODY_COLOR = "#D9C7A0"
LEG_COLOR = "#B8BCC4"


# ---------------------------------------------------------------- reusable drawings
def led_drawing(color=GREEN):
    """LED side view: dome, rim (flat on the right), left leg (anode) longer. ~2 x 5.2."""
    dome = Union(Rectangle(width=1.6, height=1.4).move_to(UP * 0.7),
                 Circle(radius=0.8).move_to(UP * 1.4))
    dome.set_fill(color, 0.85).set_stroke(color, 3)
    rim = Union(Rectangle(width=1.73, height=0.3).move_to([0.015, -0.15, 0]),
                Circle(radius=0.15).move_to([-0.85, -0.15, 0]))
    rim.set_fill(color, 0.6).set_stroke(color, 3)
    flat = Line([0.88, 0, 0], [0.88, -0.3, 0], stroke_width=3, color=color)
    anode = Line([-0.4, -0.3, 0], [-0.4, -3.0, 0], stroke_width=7, color=LEG_COLOR)
    cathode = Line([0.4, -0.3, 0], [0.4, -2.3, 0], stroke_width=7, color=LEG_COLOR)
    g = VGroup(anode, cathode, rim, dome, flat)
    g.dome, g.rim, g.flat, g.anode, g.cathode = dome, rim, flat, anode, cathode
    return g


def diode_symbol(direction=RIGHT, size=1.0, color=FG, fill=None):
    """Diode: triangle pointing `direction` (anode -> cathode), bar, two leads."""
    tri = Polygon([-0.4, 0.4, 0], [-0.4, -0.4, 0], [0.4, 0, 0], stroke_color=color, stroke_width=4)
    tri.set_fill(fill or color, 1 if fill else 0)
    bar = Line([0.4, 0.42, 0], [0.4, -0.42, 0], color=color, stroke_width=5)
    leads = VGroup(Line([-0.9, 0, 0], [-0.4, 0, 0], color=color, stroke_width=4),
                   Line([0.4, 0, 0], [0.9, 0, 0], color=color, stroke_width=4))
    g = VGroup(leads, tri, bar)
    g.tri, g.bar, g.leads = tri, bar, leads
    g.scale(size)
    g.rotate(np.arctan2(direction[1], direction[0]), about_point=ORIGIN)
    return g


def resistor_drawing(bands=("brown", "black", "orange"), tol="gold", length=6.4):
    """Horizontal banded resistor; `length` is the body length. Digit/multiplier bands near the
    left end, tolerance band near the right. 3 or 4 entries in `bands`."""
    L = length
    h = 0.28 * L
    lead = 0.22 * L
    body = RoundedRectangle(corner_radius=0.35 * h, width=L, height=h)
    body.set_fill(BODY_COLOR, 1).set_stroke("#B9A57C", 2)
    leads = VGroup(Line([-L / 2 - lead, 0, 0], [-L / 2, 0, 0]),
                   Line([L / 2, 0, 0], [L / 2 + lead, 0, 0])).set_stroke(LEG_COLOR, 5)
    leads.set_z_index(-1)
    pos = [0.17, 0.29, 0.41] if len(bands) == 3 else [0.15, 0.26, 0.37, 0.48]
    bw = 0.065 * L
    bvs = []
    for f, name in zip(pos, bands):
        b = Rectangle(width=bw, height=h * 0.999).set_stroke(width=0)
        b.set_fill(BAND[name], 1).move_to([-L / 2 + f * L, 0, 0])
        bvs.append(b)
    t = Rectangle(width=bw, height=h * 0.999).set_stroke(width=0)
    t.set_fill(BAND[tol], 1).move_to([-L / 2 + 0.84 * L, 0, 0])
    g = VGroup(leads, body, *bvs, t)
    g.leads, g.body, g.bands, g.tol = leads, body, bvs, t
    return g


def multimeter_drawing(reading="220 Ω", reading_color=GREEN):
    """Digital multimeter, 3 x 4.4: display (top), dial set to Ω, COM and red jacks (bottom)."""
    body = RoundedRectangle(corner_radius=0.3, width=3.0, height=4.4)
    body.set_fill("#2B2E35", 1).set_stroke(YELLOW, 5)
    display = RoundedRectangle(corner_radius=0.08, width=2.4, height=1.0)
    display.set_fill("#14201A", 1).set_stroke(DIM, 2).move_to(UP * 1.6)
    rd = Mono(reading, size=40, color=reading_color).move_to(display)
    dial = Circle(radius=0.62).set_fill("#3A3E47", 1).set_stroke(FG, 3).move_to(DOWN * 0.15)
    pointer = Line(dial.get_center(), dial.get_center() + UP * 0.55, stroke_width=6, color=YELLOW)
    labs = VGroup()
    for txt, ang in (("V", 150), ("Ω", 90), ("A", 30)):
        lab = T(txt, size=30, color=YELLOW if txt == "Ω" else FG)
        lab.move_to(dial.get_center() + 0.92 * np.array([np.cos(ang * DEGREES), np.sin(ang * DEGREES), 0]))
        labs.add(lab)
    jack_com = Circle(radius=0.17).set_fill("#111111", 1).set_stroke(FG, 3).move_to([-0.6, -1.55, 0])
    jack_red = Circle(radius=0.17).set_fill(RED, 1).set_stroke(RED, 3).move_to([0.6, -1.55, 0])
    g = VGroup(body, display, rd, dial, pointer, labs, jack_com, jack_red)
    g.body, g.display, g.reading, g.dial, g.pointer = body, display, rd, dial, pointer
    g.dial_labels, g.jack_com, g.jack_red = labs, jack_com, jack_red
    return g


def _probe(start, end, color, outline):
    tip_len = 0.55
    tip_bottom = end + DOWN * tip_len
    cable = CubicBezier(start, start + DOWN * 1.4, tip_bottom + DOWN * 1.4, tip_bottom)
    cable.set_stroke(color, 6)
    tip = Rectangle(width=0.18, height=tip_len).set_fill(color, 1).set_stroke(outline, 2)
    tip.move_to(end + DOWN * tip_len / 2)
    return VGroup(cable, tip)


def probe_leads(meter, red_pt, black_pt):
    """Red probe from the red jack to red_pt, black probe from COM to black_pt (tips from below)."""
    red = _probe(meter.jack_red.get_center(), np.array(red_pt), RED, RED)
    black = _probe(meter.jack_com.get_center(), np.array(black_pt), "#3A3D44", DIM)
    g = VGroup(black, red)
    g.red, g.black = red, black
    return g


def worksheet_icon():
    page = Rectangle(width=0.66, height=0.86).set_fill(FG, 0.08).set_stroke(FG, 2)
    lines = VGroup(*[Line(LEFT * 0.2, RIGHT * 0.2, stroke_width=2, color=DIM).shift(UP * (0.22 - 0.15 * i))
                     for i in range(4)]).move_to(page)
    return VGroup(page, lines)


def equation(spec, size=44):
    parts = [T(s, size=size, color=c) for s, c in spec]
    return VGroup(*parts).arrange(RIGHT, buff=0.22)


# ---------------------------------------------------------------- scene
class LedsResistors(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c1.leds.1: the LED, anode / cathode, worksheet
    def clip1(self):
        with self.say("c1.leds.1") as c:
            led = led_drawing().scale(0.8).move_to([-1.5, 0.1, 0])
            self.led = led
            self.play(FadeIn(led, shift=0.3 * UP), run_time=1.5)
            c.wait_until("anode")

            sym = diode_symbol(RIGHT, size=0.75).move_to([-1.5, 3.1, 0])
            self.sym = sym
            self.play(*appear(sym), run_time=1.2)
            self.play(VShowPassingFlash(Line(sym.get_left(), sym.get_right()).set_stroke(YELLOW, 6),
                                        time_width=0.5), run_time=1.0)
            c.wait_until("the longer leg")

            a_par = T("(longer leg)", size=30)
            a_name = T("anode", size=36, color=YELLOW)
            a_lab = VGroup(a_name, a_par).arrange(DOWN, buff=0.15, aligned_edge=RIGHT)
            a_lab.next_to(led.anode, LEFT, buff=0.35).set_y(led.anode.get_center()[1] - 0.2)
            self.play(led.anode.animate.set_color(YELLOW), *appear(a_par), run_time=1.0)
            c.wait_until(own_word=a_name)
            self.play(*appear(a_name), run_time=0.8)
            c.wait_until("cathode")

            k_par = T("(shorter leg, flat on the rim)", size=30)
            k_name = T("cathode", size=36, color=BLUE)
            k_lab = VGroup(k_name, k_par).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            k_lab.next_to(led.cathode, RIGHT, buff=0.35).set_y(led.cathode.get_center()[1] - 0.1)
            self.play(led.cathode.animate.set_color(BLUE), *appear(k_par), run_time=1.0)
            c.wait_until("flat")
            self.play(led.flat.animate.set_stroke(YELLOW, 7),
                      FlashAround(led.flat, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until(own_word=k_name)
            self.play(*appear(k_name), run_time=0.6)
            c.wait_until("sheet")

            icon = worksheet_icon()
            s_txt = VGroup(T("which way round:", size=30), T("on the worksheet", size=30)).arrange(
                DOWN, buff=0.12, aligned_edge=LEFT)
            sheet = VGroup(icon, s_txt).arrange(RIGHT, buff=0.3).move_to([-4.4, -2.6, 0])
            self.sheet, self.icon = sheet, icon
            self.play(*appear(icon, s_txt, lag=0.3), run_time=1.2)
            self.labels = [a_lab, k_lab]

    # c1.leds.2: series circuit, without the resistor, value on the worksheet
    def clip2(self):
        with self.say("c1.leds.2") as c:
            cx = 0.8
            v5 = T("5 V", size=36, color=GOLD).move_to([cx, 3.4, 0])
            v0 = T("0 V", size=36, color=DIM).move_to([cx, -3.15, 0])
            d_top, d_bot = Dot([cx, 3.0, 0], radius=0.07), Dot([cx, -2.75, 0], radius=0.07)
            res = resistor_drawing(("brown", "black", "orange"), length=1.4).rotate(PI / 2)
            res.move_to([cx, 1.75, 0])
            r_top, r_bot = res.get_top()[1], res.get_bottom()[1]
            diode = diode_symbol(DOWN, size=0.65, color=GREEN, fill=GREEN).move_to([cx, -0.55, 0])
            dc = diode.get_center()
            glow = Circle(radius=0.6).set_fill(GREEN, 0.3).set_stroke(width=0).move_to(dc)
            glow.set_z_index(-2)
            rays = VGroup(*[Arrow(dc + np.array([0.35 + 0.2 * k, 0.05 - 0.3 * k, 0]),
                                  dc + np.array([0.8 + 0.2 * k, 0.45 - 0.3 * k, 0]),
                                  buff=0, stroke_width=3, color=GREEN,
                                  max_tip_length_to_length_ratio=0.35) for k in range(2)])
            w1 = Line([cx, 3.0, 0], [cx, r_top, 0])
            w2 = Line([cx, r_bot, 0], diode.get_top())
            w3 = Line(diode.get_bottom(), [cx, -2.75, 0])
            wires = VGroup(w1, w2, w3).set_stroke(FG, 4)
            circuit_in = [FadeIn(VGroup(wires, d_top, d_bot)), FadeIn(res), FadeIn(diode),
                          FadeIn(v5, shift=0.2 * DOWN), FadeIn(v0, shift=0.2 * DOWN)]
            led = self.led
            self.play(*during([FadeOut(self.sym), *[FadeOut(l) for l in self.labels]], 0, 0.4),
                      *during([led.animate.scale(0.55).move_to([-4.4, 0.9, 0])], 0.15, 0.7),
                      *during(circuit_in, 0.5, 1.0), run_time=2.0)
            self.play(FadeIn(glow, scale=0.6), *[GrowArrow(r) for r in rays], run_time=0.8)
            c.wait_until("without")

            bypass = Line([cx, r_top, 0], [cx, r_bot, 0]).set_stroke(FG, 4)
            self.play(res.animate.shift(RIGHT * 3.0),
                      *during([FadeIn(bypass)], 0.5, 1.0), run_time=1.0)
            burst = VGroup(*[Line(dc + 0.8 * np.array([np.cos(a), np.sin(a), 0]),
                                  dc + 1.2 * np.array([np.cos(a), np.sin(a), 0]))
                             for a in np.linspace(0, TAU, 9)[:-1] + PI / 8]).set_stroke(RED, 5)
            harm = VGroup(T("can draw enough", size=30), T("current to", size=30),
                          T("destroy itself", size=30)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            harm.set_color(RED).move_to(dc).align_to([cx + 1.4, 0, 0], LEFT)
            self.play(glow.animate.set_fill(RED, 0.55).scale(1.3),
                      *[m.animate.set_color(RED) for m in (diode.tri, diode.bar, *diode.leads)],
                      *[r.animate.set_color(RED) for r in rays],
                      FadeIn(burst, scale=0.6), *during(appear(harm), 0.3, 1.0), run_time=1.2)
            c.wait_until("value")

            tag = T("value: on the worksheet", size=30, color=YELLOW)
            tag.next_to([cx + 0.45, 1.75, 0], RIGHT, buff=0)
            self.play(*during([FadeOut(burst), res.animate.shift(LEFT * 3.0), FadeOut(bypass),
                               *disappear(harm)], 0, 0.5),
                      *during([glow.animate.set_fill(GREEN, 0.3).scale(1 / 1.3),
                               *[m.animate.set_color(GREEN) for m in (diode.tri, diode.bar, *diode.leads)],
                               *[r.animate.set_color(GREEN) for r in rays]], 0.3, 0.7),
                      *during(appear(tag), 0.55, 1.0), run_time=1.8)
            self.play(FlashAround(self.icon, color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("so how")
            self.play(FlashAround(res, color=YELLOW, time_width=1.5), run_time=1.5)
            self.res = res

    # c1.leds.3: reading the bands, the colour code
    def clip3(self):
        with self.say("c1.leds.3") as c:
            res = self.res
            big = resistor_drawing(("brown", "black", "orange"), length=6.4).move_to(UP * 0.1)
            start = res.copy()
            p0, p1 = res.get_center(), big.get_center()
            k = 6.4 / 1.4

            def grow(m, a):
                m.become(start.copy().rotate(-PI / 2 * a).scale(1 + (k - 1) * a).move_to(p0 + (p1 - p0) * a))

            sweep_clear(self, UpdateFromAlphaFunc(res, grow), keep=[res], run_time=2.0)
            self.remove(res)
            self.add(big)
            c.wait_until("digits")

            top, bot = big.body.get_top()[1], big.body.get_bottom()[1]
            b1, b2, b3 = big.bands
            l1 = T("1st digit", size=30).move_to([b1.get_x() - 0.6, top + 0.75, 0])
            l2 = T("2nd digit", size=30).move_to([b2.get_x() + 0.3, top + 1.45, 0])
            ln1 = Line([b1.get_x(), top + 0.05, 0], l1.get_bottom() + DOWN * 0.08 + RIGHT * 0.6,
                       stroke_width=2, color=DIM)
            ln2 = Line([b2.get_x(), top + 0.05, 0], l2.get_bottom() + DOWN * 0.08 + LEFT * 0.3,
                       stroke_width=2, color=DIM)
            self.play(*appear(VGroup(ln1, l1), VGroup(ln2, l2), lag=0.4), run_time=1.2)
            c.wait_until("noughts")

            l3 = T("number of zeros", size=30).move_to([b3.get_x() - 0.6, bot - 0.75, 0])
            ln3 = Line([b3.get_x(), bot - 0.05, 0], l3.get_top() + UP * 0.08 + RIGHT * 0.6,
                       stroke_width=2, color=DIM)
            self.play(*appear(VGroup(ln3, l3), shift=0.25 * UP), run_time=1.0)
            c.wait_until("tol")

            tb = big.tol
            l4 = T("tolerance", size=30).move_to([tb.get_x(), bot - 0.75, 0])
            ln4 = Line([tb.get_x(), bot - 0.05, 0], l4.get_top() + UP * 0.08, stroke_width=2, color=DIM)
            self.play(*appear(VGroup(ln4, l4), shift=0.25 * UP), run_time=1.0)
            gold = T("gold = 5%", size=30, color=BAND["gold"]).next_to(l4, DOWN, buff=0.18)
            c.wait_until(own_word=gold)
            self.play(*appear(gold), FlashAround(tb, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("table")

            # the colour code, filling in as each colour is said
            rows = []
            for i, name in enumerate(CODE_ORDER):
                x = (i - 4.5) * 1.32
                d = T(str(i), size=36, color=GOLD).move_to([x, -0.75, 0])
                sw = Rectangle(width=0.95, height=0.55).set_fill(BAND[name], 1).set_stroke(DIM, 2)
                sw.move_to([x, -1.45, 0])
                nm = T(name, size=28).move_to([x, -2.1, 0])
                rows.append(VGroup(d, sw, nm))
            self.rows = rows
            band_labels = [ln1, l1, ln2, l2, ln3, l3, ln4, l4, gold]
            c.wait_until("black")
            self.play(*during(disappear(*band_labels), 0, 0.4),
                      *during([big.animate.scale(0.8).move_to(UP * 2.35)], 0.2, 0.8),
                      *during(appear(rows[0], shift=None), 0.6, 1.0), run_time=1.0)
            for i, name in enumerate(CODE_ORDER[1:], start=1):
                c.wait_until(name)
                self.play(*appear(rows[i], shift=None), run_time=0.45)
            c.wait_until("rainbow")

            br = span_brace(rows[2][2].get_corner(DL), rows[7][2].get_corner(DR), direction=DOWN, color=FG)
            rb = T("2–7: the rainbow", size=30).next_to(br, DOWN, buff=0.12)
            self.play(GrowFromCenter(br), *during(appear(rb), 0.3, 1.0), run_time=1.2)
            self.big = big
            self.rainbow = VGroup(br, rb)

    # c1.leds.4: three worked examples, then the multimeter
    def clip4(self):
        with self.say("c1.leds.4", gap=3.5) as c:
            big, rows = self.big, self.rows
            idx = {n: i for i, n in enumerate(CODE_ORDER)}

            def set_bands(r, names):
                return [b.animate.set_fill(BAND[n], 1) for b, n in zip(r.bands, names)]

            ex1 = ("red", "red", "brown")
            self.play(*set_bands(big, ex1), run_time=1.5)
            self.play(*flash([rows[idx[n]][1] for n in ("red", "brown")]), run_time=1.2)
            eq1 = equation([("2 2", GOLD), ("+", FG), ("1", GOLD), ("zero", FG), ("=", FG), ("220 Ω", GOLD)])
            eq1.move_to(UP * 0.55)
            left1, right1 = VGroup(*eq1[:4]), VGroup(*eq1[4:])
            self.play(*appear(left1), run_time=1.0)
            c.wait_until("that's")
            self.play(*appear(right1), run_time=1.0)
            c.wait_until("ex2")

            ex2 = ("yellow", "violet", "orange")
            eq2 = equation([("4 7", GOLD), ("+", FG), ("3", GOLD), ("zeros", FG), ("=", FG), ("47 000 Ω", GOLD)])
            eq2.move_to(UP * 0.55)
            self.play(*set_bands(big, ex2), *during(swap(eq1, eq2), 0.2, 1.0), run_time=1.6)
            c.wait_until("ex3")

            # same body, new bands: the 3 old bands fade off the body, the 4 new ones fade on
            # (fading a whole opaque resistor turns its body a muddy dark grey mid-fade)
            big5 = resistor_drawing(("yellow", "violet", "black", "red"), length=6.4).scale(0.8).move_to(big)
            self.play(*during([FadeOut(b) for b in big.bands], 0, 0.45),
                      *during([FadeIn(b) for b in big5.bands], 0.5, 1.0), run_time=1.2)
            self.remove(*big.get_family())
            self.add(big5)
            self.play(FlashAround(VGroup(*big5.bands), color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("then yellow")
            eq3 = equation([("4 7 0", GOLD), ("+", FG), ("2", GOLD), ("zeros", FG), ("=", FG), ("47 000 Ω", GOLD)])
            eq3.move_to(UP * 0.55)
            self.play(*swap(eq2, eq3), run_time=1.4)
            c.wait_until("measure")

            r220 = resistor_drawing(("red", "red", "brown"), length=3.0).move_to([-3.0, -0.2, 0])
            meter = multimeter_drawing("- - -", reading_color=DIM).move_to([3.3, 0.5, 0])
            # the 47 000 Ω resistor shrinks into the 220 Ω one (body never fades)
            sweep_clear(self,
                        *during([Transform(big5.leads, r220.leads), Transform(big5.body, r220.body),
                                 Transform(big5.tol, r220.tol)], 0.3, 0.85),
                        *during([FadeOut(b) for b in big5.bands], 0.0, 0.3),
                        *during([FadeIn(b) for b in r220.bands], 0.7, 1.0),
                        time_span(FadeIn(meter, shift=0.3 * LEFT), 0.7, 1.5),
                        keep=[big5], run_time=1.5)
            self.remove(*big5.get_family())
            self.add(r220)

            probes = probe_leads(meter, r220.leads[1].get_end() + LEFT * 0.15,
                                 r220.leads[0].get_start() + RIGHT * 0.15)
            reading = Mono("220 Ω", size=40, color=GREEN).move_to(meter.display)
            tick = check_mark().next_to(meter.display, RIGHT, buff=0.3)
            self.play(Create(probes.black[0]), FadeIn(probes.black[1]),
                      Create(probes.red[0]), FadeIn(probes.red[1]), run_time=1.0)
            c.wait_until("measures")
            self.play(*swap(meter.reading, reading), *during([FadeIn(tick, scale=0.6)], 0.6, 1.0),
                      run_time=1.0)
