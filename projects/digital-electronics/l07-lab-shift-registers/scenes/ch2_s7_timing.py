"""Chapter 2, scene 7: how fast should the clock tick? Period, frequency, work, energy, the limit.
Clips c2.timing.1 – c2.timing.3.

Clock wave: L6's clock_wave() (l06 ch1_s1_hook) in clip 1; from clip 2 on the same shape is redrawn by
wave_shape() so it can compress (more edges in the same width). Falling-edge aside: L6's
make_ff(bubble=True) (l06 ch6_s6_circuit). {switch} callback: ch1_s7_build's floating_inputs(),
Flicker and power_tag(), small.

handover_shot() (s8 opens on it): the compressed YELLOW clock wave (width 8, height 0.7, period 0.3,
centred (-0.6, 1.8), x -4.6 .. 3.4), a YELLOW "?" (T 80) at (4.6, 1.8), L6's make_ff() scaled 0.8
centred (4.6, -1.3) (x 3.3 .. 5.9, y -2.75 .. 0.15), and the tag "it starts with the flip-flops"
(T 36 FG) centred (-0.9, -1.0). Attributes .wave .q .ff .tag.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403


def _load_l6(stem):
    path = Path(__file__).resolve().parents[2] / "l06-flip-flops-counters" / "scenes" / f"{stem}.py"
    spec = importlib.util.spec_from_file_location(f"_l06_{stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L6_HOOK = _load_l6("ch1_s1_hook")
L6_FF = _load_l6("ch6_s6_circuit")
S7 = load_scene("ch1_s7_build")


def _p(x, y):
    return np.array([x, y, 0.0])


# ── layout ──────────────────────────────────────────────────────────────────────────
W_X, W_Y, W_W, W_H = -1.0, 1.6, 8.4, 0.8      # the main wave (clips 1-2)
P0 = W_W / 5.5                                  # its period at f = 1 (L6 clock_wave, 5 periods)
DOT_Y = 0.75
W_MARGIN = 0.22                                 # no rising edge in the last 0.22 of the clip-2 wave
F_MAX = 2.8                                     # clip 2's fastest clock (15 edges: still countable)
COL_R = 5.4                                     # right column x

END_X, END_Y, END_W, END_H, END_P = -0.6, 1.8, 8.0, 0.7, 0.3


def wave_shape(cx, cy, width, height, p, color=YELLOW, sw=4, margin=0.0, tri_min=0.0):
    """L6's ClockWave drawn for any period: low for half a period, then high/low halves, cut at
    the right end; small up-triangles on the rising edges. .wave .ups .rises (edge x's).
    margin > 0: no rising edge closer than that to the right end (the wave stays low there), so
    every edge drawn is a whole, visible edge; tri_min: a floor on the triangle size."""
    x0, x1 = cx - width / 2, cx + width / 2
    lo, hi = cy - height / 2, cy + height / 2
    pts, rises = [[x0, lo, 0]], []
    x, level = x0 + p / 2, lo
    while x < x1 - 1e-6:
        if level == lo and x > x1 - margin:
            break
        if level == lo:
            pts += [[x, lo, 0], [x, hi, 0]]
            rises.append(x)
            level = hi
        else:
            pts += [[x, hi, 0], [x, lo, 0]]
            level = lo
        x += p / 2
    pts.append([x1, level, 0])
    g = VGroup()
    g.wave = VMobject().set_points_as_corners(pts).set_stroke(color, sw)
    tri = max(tri_min, 0.11 * min(1.0, height / 0.7) * min(1.0, p / 0.6))
    g.ups = VGroup(*[Triangle().scale(tri).set_stroke(width=0).set_fill(color, 1).move_to([r, cy, 0])
                     for r in rises])
    g.rises = rises
    g.add(g.wave, g.ups)
    return g


def handover_shot():
    g = VGroup()
    g.wave = wave_shape(END_X, END_Y, END_W, END_H, END_P)
    g.q = T("?", 80, YELLOW).move_to(_p(4.6, END_Y))
    g.ff = L6_FF.make_ff().scale(0.8).move_to(_p(4.6, -1.3))
    g.tag = T("it starts with the flip-flops", 36).move_to(_p(-0.9, -1.0))
    g.add(g.wave, g.q, g.ff, g.tag)
    return g


def dim_ff(ff):
    for m in (ff.box, ff.tri, ff.bub, ff.d_w, ff.q_w, ff.qb_w, ff.clk_w):
        if m is not None:
            m.set_stroke(DIM)
    ff.remove(ff.d_l, ff.q_l, ff.qb_l)   # a small aside: the symbol only (its letters would be < 28)
    return ff


def dim_arrow(x0, x1, y, color, sw=3):
    return DoubleArrow(_p(x0, y), _p(x1, y), buff=0, stroke_width=sw, tip_length=0.16,
                       max_tip_length_to_length_ratio=0.2, color=color)


def guide(x, y0, y1, color, op=0.6):
    return Line(_p(x, y0), _p(x, y1)).set_stroke(color, 2, opacity=op)


def chip_icon():
    body = Square(1.1).set_stroke(BLUE, 4).set_fill(BG, 1)
    pins = VGroup()
    for k in range(4):
        o = -0.39 + 0.26 * k
        for d in (UP, DOWN, LEFT, RIGHT):
            perp = np.array([d[1], d[0], 0])
            a = d * 0.55 + perp * o
            pins.add(Line(a, a + d * 0.2).set_stroke(DIM, 3))
    core = Square(0.5).set_stroke(BLUE, 2, opacity=0.6)
    return VGroup(pins, body, core)


def sensor_icon():
    box = RoundedRectangle(corner_radius=0.12, width=1.3, height=0.9).set_stroke(BLUE, 4)
    ant = Line(box.get_corner(UR) + LEFT * 0.25, box.get_corner(UR) + LEFT * 0.25 + UP * 0.45).set_stroke(BLUE, 3)
    tip = Circle(radius=0.07).set_stroke(BLUE, 3).move_to(ant.get_end())
    led = Dot(radius=0.07, color=GREEN).move_to(box.get_center() + LEFT * 0.3)
    cell = Circle(radius=0.4).set_stroke(GOLD, 4).set_fill(BG, 1)
    ring = Circle(radius=0.29).set_stroke(GOLD, 2, opacity=0.6)
    plus = T("+", 32, GOLD).move_to(cell)
    coin = VGroup(cell, ring, plus).next_to(box, RIGHT, buff=0.45)
    lead = Line(box.get_right(), coin.get_left()).set_stroke(DIM, 3)
    return VGroup(lead, box, ant, tip, led, coin)


def laptop_icon():
    scr = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.2).set_stroke(BLUE, 4)
    inner = Rectangle(width=1.6, height=0.9).set_stroke(BLUE, 2, opacity=0.5).move_to(scr)
    c = scr.get_bottom()
    base = Polygon(c + LEFT * 1.05, c + RIGHT * 1.05, c + RIGHT * 1.3 + DOWN * 0.2,
                   c + LEFT * 1.3 + DOWN * 0.2).set_stroke(BLUE, 4)
    lap = VGroup(scr, inner, base)
    batt = Rectangle(width=1.0, height=0.5).set_stroke(GREEN, 4)
    nub = Rectangle(width=0.1, height=0.2).set_stroke(GREEN, 3).set_fill(GREEN, 1).next_to(batt, RIGHT, buff=0)
    bars = VGroup(*[Rectangle(width=0.22, height=0.34).set_stroke(width=0).set_fill(GREEN, 0.9) for _ in range(3)])
    bars.arrange(RIGHT, buff=0.08).move_to(batt)
    battery = VGroup(batt, nub, bars)
    head = RoundedRectangle(corner_radius=0.06, width=0.45, height=0.4).set_stroke(DIM, 3)
    p1 = Line(UP * 0.2, UP * 0.42).set_stroke(DIM, 4).shift(LEFT * 0.1)
    p2 = p1.copy().shift(RIGHT * 0.2)
    cord = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.25).set_stroke(DIM, 3)
    plug = VGroup(head, p1, p2, cord).rotate(-PI / 2)
    side = VGroup(battery, plug).arrange(DOWN, buff=0.3)
    side.next_to(lap, RIGHT, buff=0.45)
    return VGroup(lap, side)


class Timing(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(1.0)   # handover: hold the shot, no fade

    # c2.timing.1: period, falling edges, frequency, GHz
    def clip1(self):
        with self.say("c2.timing.1") as c:
            wave = L6_HOOK.clock_wave(width=W_W, height=W_H, periods=5).move_to(_p(W_X, W_Y))
            self.wave = wave
            ask = T("How fast should the clock tick?", 44).move_to(_p(0, 3.25))
            self.play(Create(wave.wave), LaggedStart(*[FadeIn(u) for u in wave.ups], lag_ratio=0.3),
                      *appear(ask), run_time=min(1.8, c.until("period")))
            self.ask = ask

            c.wait_until("period")
            xa, xb = wave.rising_x(1), wave.rising_x(2)
            g1, g2 = guide(xa, W_Y + W_H / 2 + 0.3, 0.55, YELLOW), guide(xb, W_Y + W_H / 2 + 0.3, 0.55, YELLOW)   # up past the ▲ edges
            arr = dim_arrow(xa, xb, 0.7, YELLOW)
            tc = MathTex("T_c", font_size=52, color=YELLOW).next_to(arr, DOWN, buff=0.18)
            cp = T("clock period", 32).next_to(arr, LEFT, buff=0.3)
            self.play(FadeIn(g1), FadeIn(g2), GrowFromCenter(arr), run_time=1.2)
            self.play(*appear(tc, cp, lag=0.3), run_time=1.0)
            self.period = VGroup(g1, g2, arr, tc, cp)

            c.wait_until("falling")
            ff = dim_ff(L6_FF.make_ff(bubble=True)).scale(0.55).move_to(_p(COL_R, 1.75))
            fa, fb = wave.falling_x(2), wave.falling_x(3)
            f1, f2 = guide(fa, W_Y - W_H / 2, 2.6, DIM, 0.8), guide(fb, W_Y - W_H / 2, 2.6, DIM, 0.8)
            farr = dim_arrow(fa, fb, 2.45, DIM, 3)
            self.play(FadeIn(ff, shift=0.2 * DOWN), FadeIn(f1), FadeIn(f2), GrowFromCenter(farr), run_time=1.5)
            rare = T("rare", 32, DIM).next_to(ff, DOWN, buff=0.25)
            c.wait_until(own_word=rare)
            self.play(*appear(rare), run_time=0.8)
            aside = [ff, f1, f2, farr, rare]

            c.wait_until("freq")
            fc = MathTex("f_c", "=", "1/T_c", font_size=64).move_to(_p(W_X, -0.95))
            fc[0].set_color(YELLOW)
            self.play(*appear(fc), run_time=1.2)
            hz = T("unit: hertz (Hz)", 32, DIM).next_to(fc, DOWN, buff=0.35)
            c.wait_until("hertz")
            self.play(*appear(hz), run_time=1.0)

            c.wait_until("ghz")
            chip = chip_icon().move_to(_p(COL_R, -0.9))
            sev = T("several GHz", 32, GOLD).next_to(chip, DOWN, buff=0.35)
            self.play(*during(disappear(*aside), 0, 0.45), *during([FadeIn(chip, scale=0.9)], 0.4, 1),
                      run_time=1.4)
            self.play(*appear(sev), run_time=0.8)
            line = MathTex("1", r"\,\mathrm{GHz}", r"\;\leftrightarrow\;", "T_c", "=", "1", r"\,\mathrm{ns}",
                           font_size=50).move_to(_p(W_X, -2.95))
            line[0].set_color(GOLD)
            line[5].set_color(GOLD)
            line[3].set_color(YELLOW)
            c.wait_until("one gigahertz means")
            self.play(*appear(line), run_time=1.2)
            self.c1_rest = [ask, self.period, fc, hz, chip, sev, line]

    # c2.timing.2: more work per second; the serial link; energy; the floating-input callback
    def clip2(self):
        with self.say("c2.timing.2") as c:
            f = ValueTracker(1.0)
            self.f = f
            snap = {}

            def shape():
                """The wave at the current f, built once per frame: the wave, its dots and the count
                all read these same rising edges, so they always agree."""
                v = f.get_value()
                if snap.get("v") != v:
                    snap["v"] = v
                    snap["s"] = wave_shape(W_X, W_Y, W_W, W_H, P0 / v, margin=W_MARGIN, tri_min=0.1)
                return snap["s"]

            live = always_redraw(lambda: shape().copy())
            self.remove(self.wave)
            self.add(live)

            quote = VGroup(
                T("“All things being equal, increasing the clock frequency increases", 30, slant=ITALIC),
                T("the ‘work’ that a digital system can accomplish per unit time”", 30, slant=ITALIC),
            ).arrange(DOWN, buff=0.15).move_to(_p(0, -3.1))
            chip, sev, line = self.c1_rest[4:]
            sweep_clear(self, keep=[live, chip, sev, line], run_time=1.2)

            # one GOLD dot per rising edge
            static = shape()
            drops = [Dot(_p(r, DOT_Y), radius=0.1, color=GOLD) for r in static.rises]
            c.wait_until("more work")
            self.play(*during(disappear(chip, sev, line), 0, 0.45), *during(appear(quote), 0.5, 1),
                      run_time=1.4)  # early: the slide's bullet, read as said
            self.play(LaggedStart(*[FadeIn(d, shift=0.35 * DOWN) for d in drops], lag_ratio=0.35),
                      run_time=1.4)

            def dots():
                return VGroup(*[Dot(_p(r, DOT_Y), radius=0.1, color=GOLD) for r in shape().rises])

            live_dots = always_redraw(dots)
            self.remove(*drops)
            self.add(live_dots)
            brace = span_brace(_p(W_X - W_W / 2, DOT_Y), _p(W_X + W_W / 2, DOT_Y), DOWN, DIM, buff=0.25)
            cache = {}

            def count():
                n = len(shape().rises)
                if n not in cache:
                    cache[n] = VGroup(T(str(n), 34, GOLD), T("steps in one second", 32)).arrange(
                        RIGHT, buff=0.15, aligned_edge=DOWN).next_to(brace, DOWN, buff=0.15).set_x(W_X)
                return cache[n].copy()

            steps = always_redraw(count)
            self.play(GrowFromCenter(brace), FadeIn(steps), run_time=1.0)
            c.wait_until("because")
            self.play(f.animate.set_value(2.0), run_time=min(2.2, c.until("linkfast")), rate_func=linear)

            # the serial link needs it too
            c.wait_until("linkfast")
            lx, rx, ly = W_X - 3.0, W_X + 3.0, -1.55
            boxes = VGroup()
            for x, (a, b) in ((lx, ("parallel in", "serial out")), (rx, ("serial in", "parallel out"))):
                r = RoundedRectangle(corner_radius=0.1, width=2.4, height=1.1).set_stroke(BLUE, 3).move_to(_p(x, ly))
                txt = VGroup(T(a, 28), T(b, 28)).arrange(DOWN, buff=0.08).move_to(r)
                boxes.add(VGroup(r, txt))
            wire = Line(boxes[0].get_right(), boxes[1].get_left()).set_stroke(BLUE, 4)
            ntag = T("bits N× faster", 30, GOLD).next_to(wire, UP, buff=0.15)
            self.play(*appear(boxes[0], boxes[1], lag=0.3), GrowFromCenter(wire), run_time=1.2)
            self.play(*appear(ntag), run_time=0.8)
            link = [boxes, wire, ntag]

            # the catch: energy
            c.wait_until("energy")
            mx, mb, mh = COL_R, 0.0, 2.6
            frame = Rectangle(width=0.6, height=mh).set_stroke(GOLD, 3).move_to(_p(mx, mb + mh / 2))

            def level():
                h = max(0.02, min(1.0, f.get_value() / 3.0) * (mh - 0.1))
                return Rectangle(width=0.48, height=h).set_stroke(width=0).set_fill(GOLD, 0.9).move_to(
                    _p(mx, mb + 0.05 + h / 2))

            fill = always_redraw(level)
            self.play(FadeIn(frame), FadeIn(fill), *set_alpha(link, DIMMED), run_time=1.0)
            elabel = VGroup(T("energy", 32, GOLD), T("per second", 32, GOLD)).arrange(DOWN, buff=0.1)
            elabel.next_to(frame, DOWN, buff=0.25)
            c.wait_until("the faster you run")
            self.play(f.animate.set_value(2.4), run_time=min(1.8, c.until("more energy")), rate_func=linear)
            self.play(f.animate.set_value(F_MAX), *appear(elabel), run_time=min(2.0, c.until("switch")),
                      rate_func=smooth)

            # callback: part one's floating inputs
            c.wait_until("switch")
            view = S7.floating_inputs()
            view.remove(view.nums, view.power)
            view.set_width(3.1).move_to(_p(-3.6, -1.4))   # bottom -2.31: 0.34 clear of the quote
            ptag = S7.power_tag(at=_p(1.2, -1.5))
            self.play(*during(disappear(*link), 0, 0.45), *during([FadeIn(view)], 0.45, 1),
                      *during(appear(*ptag, lag=0.4), 0.5, 1), run_time=1.6)  # early: the tag is this sentence
            fl = S7.Flicker([view.lamps[n] for n in [3] + S7.SPARE_OUT], on=(RED, 0.9), off=(RED, 0.0),
                            period=(0.12, 0.4), seed=5)
            self.add(fl)
            self.fl = fl
            self.live, self.live_dots, self.steps, self.fill = live, live_dots, steps, fill

    # c2.timing.3: battery vs mains; the limit; the flip-flops
    def clip3(self):
        with self.say("c2.timing.3") as c:
            self.fl.stop()
            self.remove(self.fl)
            sx, lx2, wy = -3.5, 3.5, 1.8
            swave = wave_shape(sx, wy, 5.0, END_H, 2.2)
            sensor = sensor_icon().move_to(_p(sx, -0.15))
            slab = VGroup(T("sensor node", 32), T("small battery", 28, DIM)).arrange(DOWN, buff=0.12)
            slab.move_to(_p(sx, -1.6))
            sweep_clear(self, *appear(swave, sensor, lag=0.3), keep=[], run_time=1.8)
            self.play(*appear(slab), run_time=0.8)

            c.wait_until("laptop")
            cx, w, p = ValueTracker(lx2), ValueTracker(5.0), ValueTracker(0.55)
            lwave = wave_shape(lx2, wy, 5.0, END_H, 0.55)
            lap = laptop_icon().move_to(_p(lx2, -0.15))
            llab = VGroup(T("laptop", 32), T("big battery or mains", 28, DIM)).arrange(DOWN, buff=0.12)
            llab.move_to(_p(lx2, -1.6))
            self.play(*appear(lap, lwave, llab, lag=0.3), run_time=1.4)

            # the limit
            c.wait_until("limit")
            live = always_redraw(lambda: wave_shape(cx.get_value(), wy, w.get_value(), END_H, p.get_value()))
            self.remove(lwave)
            self.add(live)
            self.play(*during(disappear(swave, sensor, slab), 0, 0.45),
                      *during([cx.animate.set_value(END_X), w.animate.set_value(END_W)], 0.2, 0.9),
                      run_time=1.4)
            shot = handover_shot()
            self.play(p.animate.set_value(END_P), *during(disappear(lap, llab), 0, 0.4),
                      *during(appear(shot.q), 0.65, 1),
                      run_time=min(1.8, c.until("ff")), rate_func=rate_functions.ease_out_cubic)
            p.set_value(END_P)
            self.remove(live)
            self.add(shot.wave)

            c.wait_until(own_word=shot.tag)
            self.play(*appear(shot.ff, shot.tag, lag=0.3), run_time=min(1.2, c.until()))
