"""Chapter 3, scene 4: from two numbers to one arrow (add the arrows, not the waves: A = a − ib). Clips c3.add.1 – c3.add.6.

Shared (load_scene("ch3_s4_add")):
  MOVE_M8, move_m8()     M8's move card text and the card (kit.move_card, top-right slot).
  tip_to_tail(t=0.0, a=4, b=2, origin=PLANE3_O, unit=CM, gold=True, shadows=True, width=6)
                         the L: BLUE a·e^{iωt} from the origin, PINK −ib·e^{iωt} on its tip, GOLD sum;
                         shadows = BLUE and PINK segments end to end just under the real axis + the
                         GOLD shadow dot. t a number or a ValueTracker (then it redraws every frame).
                         .blue .pink .gold .shadows (None when off). For the recap: scale down by
                         passing a smaller unit and another origin.
  A_DEMO = 4, B_DEMO = 2 the a, b this scene draws (rows 1 and 2 of the hook).
Clock: model time t (s); the drawings turn at OMEGA3 = 3 rad/s, the clock runs at CLOCK = 2/3 of real
time, frame-exact (it reads the scene's own time).
"""
# style: 2
import cmath
import math
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
spr = load_scene("ch1_s3_spring")
hook = load_scene("ch3_s1_hook")
s2 = load_scene("ch3_s2_freeze")

PLANE3_O, CM, OMEGA3, CLOCK, PERIOD3 = s2.PLANE3_O, s2.CM, s2.OMEGA3, s2.CLOCK, s2.PERIOD3
Z_GOLD, Z_MARK = -2, -1.7
A_DEMO, B_DEMO = 4.0, 2.0

# ═══════════════════════════════ shared ═══════════════════════════════
MOVE_M8 = "Add the arrows, not the waves: flat a plus downward −ib is A."


def move_m8():
    """kit.move_card's look (top-right slot), two evenly spaced lines; a, −ib, A set as maths in
    the column's colours. .box .label .body (VGroup of the two lines)."""
    size, pitch = 28, 0.46
    l1 = T("Add the arrows, not the waves:", size=size)
    parts = [("t", "flat"), ("m", "a", BLUE), ("t", "plus downward"), ("m", "-ib", PINK),
             ("t", "is"), ("m", "A.", GOLD)]
    l2 = VGroup()
    for p in parts:
        m = T(p[1], size=size) if p[0] == "t" else MathTex(p[1], font_size=size + 4, color=p[2])
        if len(l2):
            m.next_to(l2[-1], RIGHT, buff=0.1)
        l2.add(m)
    # common baseline: T pieces by a descender-free glyph, MathTex pieces by their bottom
    base1 = l1[0].get_bottom()[1]
    base2 = base1 - pitch
    for m in l2:
        ref = m[1] if isinstance(m, Text) and m.text.startswith("plus") else m
        m.shift((base2 - ref.get_bottom()[1]) * UP)
    l2.align_to(l1, LEFT)
    body = VGroup(l1, l2)
    pad, lab = 0.24, T("The move", size=24, color=YELLOW)
    lab.next_to(body, UP, buff=0.14, aligned_edge=LEFT)
    inner = VGroup(lab, body)
    box = RoundedRectangle(corner_radius=0.12, width=inner.width + 2 * pad, height=inner.height + 2 * pad)
    box.set_stroke(YELLOW, 2).set_fill(kit.CARD_FILL, 1).move_to(inner)
    card = VGroup(box, lab, body)
    card.box, card.label, card.body = box, lab, body
    card.move_to(kit.MOVE_TR, aligned_edge=UR)
    return card


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _opac(m, op):
    if op >= 0.999:
        return m
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * op)
        sm.set_fill(opacity=sm.get_fill_opacity() * op)
    return m


def _rot(t):
    return cmath.exp(1j * OMEGA3 * t)


def _P(z, origin=PLANE3_O, unit=CM):
    z = complex(z)
    return np.array(origin, dtype=float) + unit * np.array([z.real, z.imag, 0.0])


def _arr(p0, p1, color, op=1.0, width=6, z=Z_GOLD):
    p0, p1 = np.array(p0, dtype=float), np.array(p1, dtype=float)
    if np.linalg.norm(p1 - p0) < 0.06 or op < 0.01:
        return VMobject()
    return _opac(ak.arrow_between(p0, p1, color, width, z), op)


def _seg(x0, x1, color, origin, unit, op=1.0, dy=-0.11, width=7):
    o = np.array(origin, dtype=float)
    p0, p1 = o + np.array([unit * x0, dy, 0]), o + np.array([unit * x1, dy, 0])
    if abs(x1 - x0) * unit < 0.02 or op < 0.01:
        return VMobject()
    return Line(p0, p1).set_stroke(color, width, opacity=op).set_z_index(Z_MARK)


def _gold_shadow(tot, origin, unit, op=1.0):
    tip, foot = _P(tot, origin, unit), _P(tot.real, origin, unit)
    parts = []
    if np.linalg.norm(tip - foot) > 0.06:
        parts.append(DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2, opacity=op))
    parts.append(Dot(foot, radius=0.09, color=GOLD).set_opacity(op).set_z_index(Z_MARK + 0.1))
    return VGroup(*parts)


def tip_to_tail(t=0.0, a=A_DEMO, b=B_DEMO, origin=PLANE3_O, unit=CM, gold=True, shadows=True, width=6):
    """The tip-to-tail L at time t (see module docstring)."""
    def build():
        e = _rot(_v(t))
        za, zp = a * e, -1j * b * e
        tot = za + zp
        bl = _arr(_P(0, origin, unit), _P(za, origin, unit), BLUE, width=width)
        pk = _arr(_P(za, origin, unit), _P(tot, origin, unit), PINK, width=width)
        g = VGroup(bl, pk)
        g.blue, g.pink, g.gold, g.shadows = bl, pk, None, None
        if gold:
            gd = _arr(_P(0, origin, unit), _P(tot, origin, unit), GOLD, width=width)
            g.add(gd)
            g.gold = gd
        if shadows:
            sh = VGroup(_seg(0, za.real, BLUE, origin, unit), _seg(za.real, tot.real, PINK, origin, unit),
                        _gold_shadow(tot, origin, unit))
            g.add(sh)
            g.shadows = sh
        return g
    if hasattr(t, "get_value"):
        return always_redraw(build)
    return build()


# ═══════════════════════════════ scene layout ═══════════════════════════════
E_a = (r"a", BLUE, "cos coefficient")
E_b = (r"b", BLUE, "sin coefficient")
E_al = (r"\alpha", BLUE, "Re part of A")
E_be = (r"\beta", PINK, "Im part of A")
ENT_MIX = [ak.E_X, ak.E_W, ak.E_ARROW, s2.E_A, s2.E_ANGLE3, E_a, E_b]
ENT_EXP = [ak.E_X, ak.E_W, ak.E_ARROW, s2.E_A, E_a, E_b, E_al, E_be]

CL = kit.COL_LEFT                      # 0.95: left edge of the right column
ROW_SC = 0.4                           # the hook's rows, small, in the right column
ROW_REST_X = 2.45
ROW_TABLE = [0.75, -1.6]
RW0, RWSPAN, RWS = 4.1, 2.4, 0.12      # wave: t = 0 at x RW0, one period RWSPAN wide, 0.12 per cm
ROW3_REST, ROW3_TABLE = np.array([4.4, -3.2, 0.0]), -3.2
WAVE_Y, WAVE_X0, WAVE_W, WAVE_S = -2.75, 1.2, 4.0, 0.25    # clip 3's b sin ωt panel
TRI_O, TRI_U = np.array([1.3, -3.2, 0.0]), 0.21            # the 6 + 8i triangle, its own scale


def _row_axis_y(i):
    return ROW_TABLE[i] + 0.4 * ROW_SC


def _row_wave_pt(i, tau):
    return np.array([RW0 + RWSPAN * tau / PERIOD3, _row_axis_y(i) + RWS * hook.x_of(i, tau), 0.0])


def _spring_at(x_cm, rest, s, op):
    g = spr.spring_drawing(hook.DRAW * x_cm, 0.0, zero=False)
    hook._place(g, s, rest)
    return _opac(g, op)


def _row_static(i, pair_tex):
    ay = _row_axis_y(i)
    amp = [4, 2][i] * RWS + 0.1
    tl = Line([RW0 - 0.05, ay, 0], [RW0 + RWSPAN + 0.15, ay, 0]).set_stroke(DIM, 2)
    xl = Line([RW0, ay - amp, 0], [RW0, ay + amp, 0]).set_stroke(DIM, 2)
    ts = np.linspace(0, PERIOD3, 80)
    wave = VMobject().set_points_as_corners([_row_wave_pt(i, x) for x in ts]).set_stroke(BLUE, 3)
    pair = MathTex(pair_tex, font_size=28, color=BLUE)
    pair.move_to([ROW_REST_X, ROW_TABLE[i] - 0.32, 0])
    g = VGroup(tl, xl, wave, pair)
    g.pair = pair
    return g


def _step(text, y, size=None):
    g = kit.step_label(text, 0)
    g.shift((y - g[0].get_center()[1]) * UP)
    return g


def _tex(parts, colors, size=32):
    m = MathTex(*parts, font_size=size)
    for i, c in colors.items():
        m[i].set_color(c)
    return m


def _place_left(m, y, x=CL):
    return m.move_to([x, y, 0], aligned_edge=LEFT)


class Add(NarratedScene):
    def construct(self):
        self.t = ValueTracker(0.0)
        self.base, self.t0, self.rate = 0.0, 0.0, CLOCK
        self.t.add_updater(lambda m, dt: m.set_value(self.base + self.rate * (self.time - self.t0))
                           if self.rate is not None else None)
        self.add(self.t)
        self._target = 0.0
        names = dict(lb=0, lp=0, lg=0, ob=1, op=1, og=1, u=0, sdb=0, sdp=0, sgb=0, sgp=0, sgg=0,
                     l4=0, l2=0, la=0, lib=0, od=0, dd=0.16, r0=0, r1=0, r3=0, wd=0)
        self.k = {n: ValueTracker(v) for n, v in names.items()}
        self.add(*self.k.values())
        self.trackers = [self.t, *self.k.values()]
        self.wref = 0.0
        self.build_live()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects if m not in self.trackers], run_time=1.0)
        self.remove(*self.mobjects)
        self.wait(0.15)

    # ── clock ────────────────────────────────────────────────────────────────────
    def set_clock(self, rate, value=None):
        self.base = self.t.get_value() if value is None else value
        self.t0 = self.time
        self.rate = rate
        self.t.set_value(self.base)

    def aim(self, t_abs, tmod=0.0):
        """Trim the clock so the model time is ≡ tmod (mod one period) at scene time t_abs."""
        v0 = self.t.get_value()
        dt = max(t_abs - self.time, 1e-3)
        n = round((v0 + CLOCK * dt - tmod) / PERIOD3)
        v1 = tmod + n * PERIOD3
        while (v1 - v0) / dt < 0.6 * CLOCK:
            v1 += PERIOD3
        self.set_clock((v1 - v0) / dt)
        self._target = v1

    def freeze(self):
        self.set_clock(0.0, self._target)

    def step(self, dv, rt, *extra, rate_func=smooth):
        self.rate = None
        v = self.t.get_value()
        self.play(self.t.animate(rate_func=rate_func).set_value(v + dv), *extra, run_time=rt)
        self.set_clock(0.0)

    def kv(self, name):
        return self.k[name].get_value()

    def to(self, name, value):
        return self.k[name].animate.set_value(value)

    # ── the live drawings ───────────────────────────────────────────────────────
    def geo(self):
        e = _rot(self.t.get_value())
        za = A_DEMO * e
        zp = -1j * B_DEMO * e
        base = self.kv("u") * za
        return za, zp, base

    def build_live(self):
        def blue():
            za, _, _ = self.geo()
            return _arr(_P(0), _P(self.kv("lb") * za), BLUE, self.kv("ob"))

        def pink():
            _, zp, base = self.geo()
            return _arr(_P(base), _P(base + self.kv("lp") * zp), PINK, self.kv("op"))

        def gold():
            za, zp, _ = self.geo()
            return _arr(_P(0), _P(self.kv("lg") * (za + zp)), GOLD, self.kv("og"))

        def pure_shadows():
            za, zp, _ = self.geo()
            g = VGroup()
            for z, col, key in ((za, BLUE, "sdb"), (zp, PINK, "sdp")):
                op = self.kv(key)
                if op < 0.01:
                    continue
                tip, foot = _P(z), _P(z.real)
                if np.linalg.norm(tip - foot) > 0.06:
                    g.add(DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2, opacity=op))
                g.add(Dot(foot, radius=0.09, color=col).set_opacity(op).set_z_index(Z_MARK))
            return g

        def segs():
            za, zp, _ = self.geo()
            tot = za + zp
            g = VGroup(_seg(0, za.real, BLUE, PLANE3_O, CM, self.kv("sgb")),
                       _seg(za.real, tot.real, PINK, PLANE3_O, CM, self.kv("sgp")))
            if self.kv("sgg") > 0.01:
                g.add(_gold_shadow(tot, PLANE3_O, CM, self.kv("sgg")))
            return g

        def twin():
            od = self.kv("od")
            if od < 0.01:
                return VMobject()
            za, zp, _ = self.geo()
            tot = za + zp
            p0, p1 = _P(0), _P(tot)
            d = (p1 - p0) / np.linalg.norm(p1 - p0)
            perp = np.array([-d[1], d[0], 0.0]) * self.kv("dd")
            tl = 0.24
            end = p1 + perp - tl * d
            ln = DashedLine(p0 + perp, end, dash_length=0.13, dashed_ratio=0.55).set_stroke(GOLD, 4, opacity=od)
            side = np.array([-d[1], d[0], 0.0]) * 0.11
            tip = Polygon(p1 + perp, end + side, end - side).set_stroke(width=0).set_fill(GOLD, od)
            return VGroup(ln, tip).set_z_index(Z_GOLD + 0.1)

        def label(tex, color, key, which):
            base_m = MathTex(tex, font_size=34, color=color)

            def build():
                op = self.kv(key)
                if op < 0.01:
                    return VMobject()
                za, zp, base = self.geo()
                if which == "b":
                    p0, p1 = _P(0), _P(self.kv("lb") * za)
                else:
                    p0, p1 = _P(base), _P(base + self.kv("lp") * zp)
                d = p1 - p0
                n = np.linalg.norm(d)
                if n < 0.1:
                    return VMobject()
                d = d / n
                perp = np.array([-d[1], d[0], 0.0])
                m = base_m.copy()
                r = 0.5 * (abs(perp[0]) * m.width + abs(perp[1]) * m.height)
                m.move_to((p0 + p1) / 2 + perp * (0.14 + r))
                return _opac(m, op)
            return always_redraw(build)

        self.blue = always_redraw(blue)
        self.pink = always_redraw(pink)
        self.gold = always_redraw(gold)
        self.pure = always_redraw(pure_shadows)
        self.segs = always_redraw(segs)
        self.twin = always_redraw(twin)
        self.lab4 = label("4", BLUE, "l4", "b")
        self.lab2 = label("-2i", PINK, "l2", "p")
        self.laba = label("a", BLUE, "la", "b")
        self.labib = label("-ib", PINK, "lib", "p")
        self.live_plane = [self.segs, self.pure, self.gold, self.twin, self.blue, self.pink,
                           self.lab4, self.lab2, self.laba, self.labib]

        # the hook's rows (springs live, the rest static)
        def row(i):
            def build():
                op = self.kv(f"r{i}")
                if op < 0.01:
                    return VMobject()
                tau = self.t.get_value()
                g = _spring_at(hook.x_of(i, tau), np.array([ROW_REST_X, ROW_TABLE[i], 0]), ROW_SC, op)
                dot = Dot(_row_wave_pt(i, tau % PERIOD3), radius=0.07, color=BLUE).set_opacity(op)
                return VGroup(g, dot)
            return always_redraw(build)
        self.rows = [row(0), row(1)]

        def row3():
            op = self.kv("r3")
            if op < 0.01:
                return VMobject()
            return _spring_at(hook.x_of(2, self.t.get_value() - self.wref), ROW3_REST, ROW_SC, op)
        self.row3 = always_redraw(row3)

        def wave_dot():
            op = self.kv("wd")
            if op < 0.01:
                return VMobject()
            tau = float(np.clip(self.t.get_value() - self.wref, 0.0, PERIOD3))
            p = [WAVE_X0 + WAVE_W * tau / PERIOD3, WAVE_Y + WAVE_S * B_DEMO * math.sin(OMEGA3 * tau), 0]
            return Dot(p, radius=0.08, color=PINK).set_opacity(op)
        self.wdot = always_redraw(wave_dot)
        self.add(*self.live_plane, *self.rows, self.row3, self.wdot)

    # ── c3.add.1: the pure cases ────────────────────────────────────────────────
    def clip1(self):
        with self.say("c3.add.1") as c:
            self.pl, self.labs = s2.plane3(), s2.plane_labels()
            self.pin = s2.amp_pin()
            self.leg = kit.legend(s2.ENTRIES3, s2.LEG_ROWS3)
            self.card = s2.move_m7()
            self.play(FadeIn(self.pl), FadeIn(self.labs), FadeIn(self.pin), FadeIn(self.leg),  # early: the board returns
                      FadeIn(self.card), run_time=1.2)
            self.rs = [_row_static(0, r"(a, b) = (4, 0)"), _row_static(1, r"(a, b) = (0, 2)")]
            self.play(*appear(*self.rs, shift=None, lag=0.3), self.to("r0", 1), self.to("r1", 1),  # early: the hook's rows return
                      run_time=1.5)
            self.aim(c.at("first"))

            c.wait_until("first")
            self.freeze_free()
            self.play(*set_alpha([self.rs[1]], 0.35), self.to("r1", 0.35), run_time=0.8)
            self.play(self.to("lb", 1), self.to("sdb", 1), self.to("l4", 1), run_time=1.5)
            self.aim(c.at("second"))

            c.wait_until("The cosine's arrow")
            self.f1 = _place_left(_tex(["4", r"\cos 3t", "=", r"\mathrm{Re}\Big[\,", "4", r"\,e^{3it}", r"\Big]"],
                                       {0: BLUE, 4: BLUE}, 34), -0.2)
            self.n1 = _place_left(T("cosine arrow starts at 1", size=24, color=DIM), -0.62)
            self.play(*appear(self.f1, self.n1, lag=0.4, shift=None), run_time=1.5)  # early: the line being said

            c.wait_until("second")
            self.freeze_free()
            self.play(*set_alpha([self.rs[0]], 0.35), self.to("r0", 0.35), *set_alpha([self.rs[1]], 1.0),
                      self.to("r1", 1), self.to("ob", 0.3), self.to("sdb", 0), self.to("l4", 0.3), run_time=1.0)
            self.play(self.to("lp", 1), self.to("sdp", 1), self.to("l2", 1), run_time=1.5)

            c.wait_until("The sine's arrow")
            self.f2 = _place_left(_tex(["2", r"\sin 3t", "=", r"\mathrm{Re}\Big[", "-2i", r"\,e^{3it}", r"\Big]"],
                                       {0: BLUE, 4: PINK}, 34), -2.55)
            self.n2 = _place_left(T("sine arrow starts at −i", size=24, color=DIM), -2.97)
            self.play(*appear(self.f2, self.n2, lag=0.4, shift=None), run_time=1.5)  # early: the line being said

    def freeze_free(self):
        """At an aimed cue: land exactly on the target and keep turning at the house rate."""
        self.set_clock(CLOCK, self._target)

    # ── c3.add.2: tip to tail ───────────────────────────────────────────────────
    def clip2(self):
        with self.say("c3.add.2") as c:
            self.aim(c.at("tip"))
            # {mix}: letters replace the numbers
            self.fa = _place_left(_tex(["a", r"\cos\omega t", "=", r"\mathrm{Re}\Big[\,", "a", r"\,e^{i\omega t}",
                                        r"\Big]"], {0: BLUE, 4: BLUE}, 34), 1.05)
            self.fb = _place_left(_tex(["b", r"\sin\omega t", "=", r"\mathrm{Re}\Big[", "-ib", r"\,e^{i\omega t}",
                                        r"\Big]"], {0: BLUE, 4: PINK}, 34), 0.3)
            self.play(*during(disappear(*self.rs, self.n1, self.n2), 0, 0.35),
                      *during([self.to("r0", 0), self.to("r1", 0)], 0, 0.35),
                      *during(edit(self.f1, self.fa), 0.2, 0.65),
                      *during(edit(self.f2, self.fb), 0.5, 1.0), run_time=1.8)
            self.remove(*self.rows)
            self.play(*during([self.to("l4", 0), self.to("l2", 0), self.to("sdp", 0)], 0, 0.45),
                      *during([self.to("ob", 1), self.to("la", 1), self.to("lib", 1)], 0.55, 1.0),
                      run_time=1.2)

            c.wait_until("move")
            self.m8 = move_m8()
            self.play(*swap(self.card, self.m8), run_time=1.2)
            self.card = self.m8

            # {tip}: the PINK arrow slides onto the BLUE tip; the L turns as one; GOLD is their sum
            c.wait_until("tip")
            self.freeze()
            self.play(self.to("u", 1), run_time=1.5)
            self.corner = kit.corner_tag()
            self.play(self.to("lg", 1), self.to("sgb", 1), self.to("sgp", 1), self.to("sgg", 1),
                      *appear(self.corner), run_time=1.2)  # early: corner tag
            self.step(PERIOD3, PERIOD3 / CLOCK, rate_func=linear)
            self.set_clock(CLOCK)
            self.aim(c.at("readback"))

            # {box}: the sum, then A boxed
            c.wait_until("box")
            self.sl = _step("add the arrows", -0.17)
            self.fs = _place_left(_tex(["a", r"\cos\omega t", "+", "b", r"\sin\omega t", "=",
                                        r"\mathrm{Re}\Big[(", "a", "-ib", r")\,e^{i\omega t}\Big]"],
                                       {0: BLUE, 3: BLUE, 7: BLUE, 8: PINK}, 32), -0.6)
            self.play(*appear(self.sl, self.fs, lag=0.3, shift=None), run_time=1.5)
            c.wait_until("cosine coefficient")
            kit.legend_set(self, self.leg, ENT_MIX, run_time=1.2)
            c.wait_until("minus eye")
            ftx = _tex(["A", "=", "a", "-ib"], {0: GOLD, 2: BLUE, 3: PINK}, 42)
            frame = SurroundingRectangle(ftx, color=YELLOW, buff=0.2).set_stroke(YELLOW, 2.5)
            self.boxA = VGroup(frame, ftx).move_to([CL, -1.55, 0], aligned_edge=LEFT)
            self.boxA.f = ftx
            self.btag = kit.tag("notes p. 108", self.boxA, RIGHT, 0.3)
            self.play(*appear(self.boxA, self.btag, lag=0.4, shift=None), run_time=1.5)  # early: the boxed result and its source tag

            # {readback}: flat, hangs below
            c.wait_until("readback")
            self.freeze()
            za = A_DEMO
            self.w_flat = T("flat", size=28, color=BLUE)
            self.w_flat.next_to(_P(za / 2) + 0.3 * UP, RIGHT, buff=0.32)
            self.w_hang = T("hangs below", size=28, color=PINK)
            self.w_hang.move_to(_P(za - 1j * B_DEMO * 0.5) + 0.28 * DOWN + 0.2 * RIGHT, aligned_edge=UL)
            c.wait_until(own_word=self.w_flat)
            self.play(*appear(self.w_flat), run_time=1.0)
            c.wait_until(own_word=self.w_hang)
            self.play(*appear(self.w_hang), run_time=1.0)

    # ── c3.add.3: why −i ────────────────────────────────────────────────────────
    def clip3(self):
        with self.say("c3.add.3") as c:
            self.why = T("why −i?", size=30, color=YELLOW)
            self.why.next_to(self.w_hang, DOWN, buff=0.18, aligned_edge=LEFT)
            self.play(*appear(self.why), run_time=1.0)

            c.wait_until("down")
            ax = Line([WAVE_X0 - 0.05, WAVE_Y, 0], [WAVE_X0 + WAVE_W + 0.2, WAVE_Y, 0]).set_stroke(DIM, 2)
            vx = Line([WAVE_X0, WAVE_Y - 0.6, 0], [WAVE_X0, WAVE_Y + 0.6, 0]).set_stroke(DIM, 2)
            ts = np.linspace(0, PERIOD3, 90)
            wave = VMobject().set_points_as_corners(
                [[WAVE_X0 + WAVE_W * x / PERIOD3, WAVE_Y + WAVE_S * B_DEMO * math.sin(OMEGA3 * x), 0] for x in ts]
            ).set_stroke(BLUE, 3)
            wl = MathTex(r"b\sin\omega t", font_size=30, color=BLUE).next_to(ax, RIGHT, buff=0.15)
            self.wpanel = VGroup(ax, vx, wave, wl)
            self.wref = self.t.get_value()
            self.play(self.to("ob", 0.25), self.to("og", 0.25), self.to("la", 0.25),
                      self.to("sgb", 0.25), self.to("sgg", 0.25),
                      *appear(self.wpanel, shift=None), self.to("wd", 1), run_time=1.2)

            c.wait_until("peaks")
            cx = WAVE_X0 + WAVE_W / 4
            crest = np.array([cx, WAVE_Y + WAVE_S * B_DEMO, 0])
            base = np.array([cx, WAVE_Y, 0])
            self.crest = VGroup(DashedLine(crest, base, dash_length=0.06).set_stroke(YELLOW, 2.5),
                                Dot(crest, radius=0.08, color=YELLOW),
                                Line(base + 0.1 * DOWN, base + 0.1 * UP).set_stroke(YELLOW, 4))
            self.play(*appear(self.crest, shift=None), run_time=1.0)

            c.wait_until("pointing down")
            p0, p1 = _P(A_DEMO), _P(A_DEMO - 1j * B_DEMO)
            self.play(VShowPassingFlash(Line(p0, p1).set_stroke(YELLOW, 9), time_width=0.6), run_time=1.0)

            c.wait_until("a quarter turn later it")
            self.step(PERIOD3 / 4, min(2.0, max(1.2, c.until() - 0.2)))

    # ── c3.add.4: the long way (reference) ──────────────────────────────────────
    def clip4(self):
        with self.say("c3.add.4") as c:
            olds = [self.fa, self.fb, self.sl, self.fs, self.btag, self.wpanel, self.crest,
                    self.w_flat, self.w_hang, self.why]
            box_y = 1.0
            self.play(*during(disappear(*olds), 0, 0.4),
                      *during([self.to("wd", 0), self.to("ob", 1), self.to("og", 1), self.to("la", 1),
                               self.to("sgb", 1), self.to("sgg", 1)], 0, 0.4),
                      *during([self.boxA.animate.shift((box_y - self.boxA.get_center()[1]) * UP)], 0.35, 0.9),
                      run_time=1.6)
            self.set_clock(CLOCK)
            tx = self.boxA.get_right()[0] + 0.3
            self.rtags = VGroup(kit.tag("reference"), kit.tag("lecturer's working"), kit.tag("notes p. 108"))
            self.rtags.arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([tx, self.boxA.get_top()[1] + box_y - self.boxA.get_center()[1] + 0.02, 0], aligned_edge=UL)
            kit.legend_set(self, self.leg, ENT_EXP, *appear(self.rtags, shift=None), run_time=1.2)  # early: reference tags

            # layout of the whole derivation
            self.e0 = _place_left(_tex(["A", "=", r"\alpha", "+", r"i\beta", r",\quad", r"e^{i\omega t}", "=",
                                        r"\cos\omega t", "+", r"i\sin\omega t"],
                                       {0: GOLD, 2: BLUE, 4: PINK, 10: PINK}, 32), 0.05)
            self.s0 = _step("write both in parts", 0.42)
            self.e1a = _place_left(_tex([r"A\,e^{i\omega t}", "=", r"\alpha\cos\omega t", "+", r"i\alpha\sin\omega t"],
                                        {0: GOLD, 2: BLUE, 4: PINK}, 32), -0.68)
            self.s1 = _step("multiply out", -0.33)
            self.e1b = _tex(["+", r"i\beta\cos\omega t", "+", r"i^2\beta\sin\omega t"], {1: PINK, 3: PINK}, 32)
            self.e1b2 = _tex(["+", r"i\beta\cos\omega t", "-", r"\beta\sin\omega t"], {1: PINK, 2: BLUE, 3: BLUE}, 32)
            for m in (self.e1b, self.e1b2):
                m.move_to([0, -1.12, 0])
                m.shift((self.e1a[2].get_left()[0] - m[1].get_left()[0]) * RIGHT)
            self.e3 = _place_left(_tex([r"\mathrm{Re}\Big[A\,e^{i\omega t}\Big]", "=", r"\alpha\cos\omega t", "-",
                                        r"\beta\sin\omega t"], {2: BLUE, 3: BLUE, 4: BLUE}, 32), -2.02)
            self.s3 = _step("keep the real part", -1.62)
            self.e4 = _place_left(_tex([r"\alpha", "=", "a", r",\quad", r"-\beta", "=", "b"],
                                       {0: BLUE, 2: BLUE, 4: BLUE, 6: BLUE}, 34), -2.8)
            self.s4 = _step("match the coefficients", -2.42)
            self.isq = MathTex(r"i^2 = -1", font_size=26, color=DIM).next_to(self.e1b2, RIGHT, buff=0.3)

            c.wait_until("alpha plus")
            self.play(*appear(self.s0, self.e0, lag=0.35, shift=None), run_time=1.5)

            c.wait_until("multiply")
            self.play(*appear(self.s1, self.e1a, self.e1b, lag=0.4, shift=None), run_time=1.8)

            c.wait_until("isq")
            self.play(*edit(self.e1b, self.e1b2), *appear(self.isq), *set_alpha([self.e0, self.s0], 0.4),
                      run_time=1.2)

            c.wait_until("real")
            self.play(*appear(self.s3, self.e3, lag=0.3, shift=None), run_time=1.5)

            c.wait_until("match")
            self.play(*appear(self.s4, self.e4, lag=0.3, shift=None),
                      *set_alpha([self.e1a, self.e1b2, self.s1, self.isq], 0.4), run_time=1.5)
            self.play(FlashAround(self.e4, time_width=1.5), FlashAround(self.boxA, time_width=1.5), run_time=1.5)

    # ── c3.add.5: is matching allowed? ──────────────────────────────────────────
    def clip5(self):
        with self.say("c3.add.5") as c:
            self.expansion = [self.e0, self.s0, self.e1a, self.e1b2, self.s1, self.isq, self.e3, self.s3,
                              self.e4, self.s4]
            self.play(*set_alpha([self.e3, self.s3, self.e4, self.s4], 0.4), run_time=1.0)

            c.wait_until("same")
            self.play(self.to("ob", 0), self.to("op", 0), self.to("la", 0), self.to("lib", 0),
                      self.to("sgb", 0), self.to("sgp", 0), self.to("od", 1), run_time=1.5)
            self.aim(c.at("t0"))

            c.wait_until("t0")
            self.freeze()
            self.play(self.to("ob", 1), self.to("op", 1), self.to("sgb", 1), self.to("sgp", 1), run_time=1.0)
            x0 = _P(A_DEMO)
            self.tick0 = Line(x0 + 0.2 * DOWN, x0 + 0.2 * UP).set_stroke(BLUE, 5).set_z_index(Z_MARK + 0.2)
            self.say0 = T("real parts equal", size=26, color=BLUE).move_to(_P(A_DEMO / 2) + 0.42 * UP)
            self.play(*appear(self.tick0, shift=None), *appear(self.say0), run_time=1.0)

            c.wait_until("quarter")
            self.step(PERIOD3 / 4, 2.0, *during(disappear(self.tick0, self.say0), 0, 0.3))
            x1 = _P(B_DEMO)
            self.tick1 = Line(x1 + 0.2 * DOWN, x1 + 0.2 * UP).set_stroke(PINK, 5).set_z_index(Z_MARK + 0.2)
            self.say1 = T("imaginary parts equal", size=26, color=PINK).move_to(_P(B_DEMO / 2) + 0.5 * DOWN)
            c.wait_until(own_word=self.say1)
            self.play(*appear(self.tick1, shift=None), *appear(self.say1), run_time=1.0)

            # {merge}: the dashed arrow snaps onto the solid one; the expansion makes room
            c.wait_until("merge")
            self.match = self.e4
            keep_y = self.boxA.get_bottom()[1] - 0.45
            gone = [m for m in self.expansion if m is not self.e4] + [self.rtags]
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during([self.e4.animate.move_to([CL, keep_y, 0], aligned_edge=LEFT)], 0.35, 0.85),
                      *during([self.to("dd", 0)], 0.15, 0.75),
                      *during([self.to("od", 0), self.to("ob", 0), self.to("op", 0), self.to("sgb", 0),
                               self.to("sgp", 0)], 0.75, 1.0), run_time=1.6)
            self.same = VGroup(T("same shadow at every t", size=30),
                               VGroup(MathTex(r"\Rightarrow", font_size=34), T("same arrow", size=30))
                               .arrange(RIGHT, buff=0.18)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            self.same.move_to([CL, keep_y - 0.95, 0], aligned_edge=LEFT)
            self.play(*appear(self.same, shift=None), run_time=1.0)

            c.wait_until("That's why")
            r1 = VGroup(MathTex(r"e^{i\omega t}", font_size=36, color=GOLD), T("on both sides", size=30))
            r1.arrange(RIGHT, buff=0.16)
            self.rule = VGroup(r1, T("of an equation cancels", size=30)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            self.rule.move_to([CL, self.same.get_bottom()[1] - 0.75, 0], aligned_edge=UL)
            self.rtag = kit.tag("lecturer's rule · notes p. 110").next_to(self.rule, DOWN, buff=0.16,
                                                                         aligned_edge=LEFT)
            self.play(*appear(self.rule, self.rtag, lag=0.4, shift=None), run_time=1.5)  # early: the rule and its source tag

    # ── c3.add.6: think stop, the answer, the third weight ──────────────────────
    def clip6(self):
        with self.say("c3.add.6") as c:
            col = [self.boxA, self.e4, self.same, self.rule, self.rtag, self.corner, self.tick1, self.say1]
            self.think = kit.think_box("Which complex amplitude gives\n6 cos 3t − 8 sin 3t,\n"
                                       "and how big is that swing?", size=30, pos=np.array([3.75, -0.4, 0]))
            self.ring = kit.think_ring()
            c.wait_until("Which complex")
            self.play(*during(disappear(*col), 0, 0.45), *during([self.to("og", 0), self.to("sgg", 0)], 0, 0.45),
                      *during(appear(self.think, self.ring, shift=None, lag=0.3), 0.5, 1.0),  # early: think-stop question shown whole
                      *during(set_alpha([self.card], 0.6), 0.5, 1.0), run_time=1.8)
            self.set_clock(0.0)
            c.wait_until("Pause the video")
            self.play(kit.drain(self.ring, max(1.0, c.until("answer") - 0.2)))

            # {answer}
            c.wait_until("answer")
            self.q1 = _place_left(_tex([r"6\cos 3t", "-", r"8\sin 3t", r"\;\Rightarrow\;", "b", "=", "-8"],
                                       {4: BLUE, 6: BLUE}, 34), 1.1)
            self.play(*during(disappear(self.think, self.ring), 0, 0.45), *during(set_alpha([self.card], 1.0), 0, 0.45),
                      *during(appear(self.q1), 0.5, 1.0), run_time=1.6)
            c.wait_until("six plus")
            self.ql = _step("A = a − ib", 0.72)
            self.q2 = _place_left(_tex(["A", "=", "6", "-", "i(-8)", "=", "6", "+", "8i"],
                                       {0: GOLD, 2: BLUE, 4: PINK, 6: BLUE, 8: PINK}, 34), 0.35)
            self.play(*appear(self.ql, self.q2, lag=0.3, shift=None), run_time=1.2)

            c.wait_until("this time")
            o = TRI_O
            pr, pt_ = o + TRI_U * 6 * RIGHT, o + TRI_U * 6 * RIGHT + TRI_U * 8 * UP
            axis = VGroup(Line(o + 0.3 * LEFT, o + 2.3 * RIGHT), Line(o + 0.3 * DOWN, o + 0.5 * UP)).set_stroke(DIM, 2)
            self.t_blue = ak.arrow_between(o, pr, BLUE)
            self.t_pink = ak.arrow_between(pr, pt_, PINK)
            self.t6 = MathTex("6", font_size=34, color=BLUE).next_to((o + pr) / 2, DOWN, buff=0.12)
            self.t8 = MathTex("8", font_size=34, color=PINK).next_to((pr + pt_) / 2, RIGHT, buff=0.15)
            self.play(FadeIn(axis), GrowArrow(self.t_blue), run_time=0.9)
            self.play(GrowArrow(self.t_pink), *appear(self.t6, self.t8, shift=None, lag=0.3), run_time=1.2)
            self.note = VGroup(T("b < 0:", size=26, color=YELLOW), T("the leg points up", size=26, color=YELLOW))
            self.note.arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to(o + np.array([2.1, 0.55, 0]), aligned_edge=DL)
            self.play(*appear(self.note), run_time=1.0)  # early: the voice is on "above the axis"
            self.tri_axis = axis

            # {size}
            c.wait_until("size")
            self.t_gold = ak.arrow_between(o, pt_, GOLD)
            d = (pt_ - o) / np.linalg.norm(pt_ - o)
            self.t10 = MathTex("10", font_size=34, color=GOLD).move_to((o + pt_) / 2 + 0.36 * np.array([-d[1], d[0], 0]))
            self.play(GrowArrow(self.t_gold), *appear(self.t10, shift=None), run_time=1.2)
            c.wait_until("Pythagoras")
            self.pl_ = _step("Pythagoras", -0.07)
            self.q3 = _place_left(_tex([r"|A|", "=", r"\sqrt{6^2 + 8^2}", "=", r"\sqrt{100}", "=", "10"],
                                       {0: GOLD, 6: GOLD}, 34), -0.5)
            self.play(*appear(self.pl_, self.q3, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("ten long")
            gen = _tex([r"|A|", "=", r"\sqrt{a^2 + b^2}"], {0: GOLD}, 34)
            gtag = kit.tag("in general")
            self.gen = VGroup(gtag, gen).arrange(RIGHT, buff=0.25)
            self.gen.move_to([kit.EDGE_X, -1.2, 0], aligned_edge=RIGHT)
            self.play(*appear(self.gen, shift=None), run_time=1.0)

            # {third}: the third weight
            c.wait_until("third")
            tri = VGroup(self.tri_axis, self.t_blue, self.t_pink, self.t_gold, self.t6, self.t8, self.t10)
            dl = tri.get_corner(DL)
            self.play(*during(disappear(self.note), 0, 0.4),
                      *during(set_alpha([self.q1, self.ql, self.q2, self.pl_, self.q3], 0.4), 0, 0.6),
                      *during([tri.animate.scale(0.65, about_point=dl)], 0.3, 1.0), run_time=1.5)
            self.q4 = _place_left(_tex([r"3\cos 3t", "+", r"4\sin 3t", r"\;\to\;", "A", "=", "3", "-4i"],
                                       {4: GOLD, 6: BLUE, 7: PINK}, 32), -1.75)
            b3 = ak.arrow_between(PLANE3_O, s2.pt(3), BLUE)
            p3 = ak.arrow_between(s2.pt(3), s2.pt(3 - 4j), PINK)
            l3 = MathTex("3", font_size=34, color=BLUE).next_to((PLANE3_O + s2.pt(3)) / 2, UP, buff=0.12)
            l4 = MathTex("4", font_size=34, color=PINK).next_to((s2.pt(3) + s2.pt(3 - 4j)) / 2, RIGHT, buff=0.15)
            c.wait_until("three minus four")
            self.play(*appear(self.q4, shift=None), GrowArrow(b3), run_time=1.2)
            self.play(GrowArrow(p3), *appear(l3, l4, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("five long")
            g3 = ak.arrow_between(PLANE3_O, s2.pt(3 - 4j), GOLD)
            gm = (PLANE3_O + s2.pt(3 - 4j)) / 2
            l5 = MathTex("5", font_size=34, color=GOLD).move_to(gm + 0.3 * LEFT + 0.25 * DOWN)
            self.play(GrowArrow(g3), *appear(l5, shift=None), run_time=1.0)
            c.wait_until("the arrow we froze")
            fa = s2.frozen_A()
            self.wref = self.t.get_value()
            self.set_clock(CLOCK)
            self.play(FadeIn(fa.arrow), *appear(fa.label), self.to("r3", 1), run_time=1.2)
            self.remove(g3)
            self.play(VShowPassingFlash(Line(PLANE3_O, s2.pt(3 - 4j)).set_stroke(YELLOW, 8), time_width=0.6),
                      run_time=1.0)
        self.wait(2.0)
