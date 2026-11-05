"""Chapter 3, scene 5: calculus becomes multiplication (v = Re[iωA e^{iωt}], the fan). Clips c3.vel.1 – c3.vel.5.

Exports (load_scene("ch3_s5_velocity")), module-level and free of scene state:
  fan3(t, origin=PLANE3_O, scale=1.0, labels=True, amp=A3, marks=True)
      The fan of three arrows from the origin of ch3's plane, a quarter turn apart and turning
      together: GOLD A e^{iωt} (true length, 0.42·scale per cm), GREEN iωA e^{iωt} and RED −ω²A e^{iωt}
      (both drawn shortened: GREEN_LEN / RED_LEN · scale), each with a dashed drop line and a shadow
      dot on Re (BLUE, GREEN, RED). labels=True adds the tip formulas and the DIM "not to scale:
      length 15 / 45" notes; marks=True the right-angle mark at the origin. `t` a ValueTracker
      (model seconds; redraws every frame) or a number (still). Pair it with
      s2.plane3 / s2.spring3 for the full picture. Z: arrows -2 .. -1.85, dots -1.7, labels 1.
  GREEN_LEN, RED_LEN (scene units at scale 1; true 6.3 and 18.9), E_V (ẋ = v "velocity"),
  E_ACC (ẍ "acceleration"), ENTRIES5 (this scene's legend), MOVE_M9 / move_m9().
Board: s2's plane at PLANE3_O, weight on Re, amp_pin; live readouts x, ẋ, ẍ right of the plane
(below Re); the derivation column at COL_X 2.1 (right of the readouts); a low band (y < -1.8,
x > -0.6) for side lines and the worked numbers. The motion runs on a frame-exact clock (self.clk).
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
s2 = load_scene("ch3_s2_freeze")

PLANE3_O, CM, A3, OMEGA3, CLOCK, PERIOD3 = s2.PLANE3_O, s2.CM, s2.A3, s2.OMEGA3, s2.CLOCK, s2.PERIOD3

# ═══════════════════════════════ the fan (shared) ═══════════════════════════════
GREEN_LEN, RED_LEN = 2.3, 2.45       # drawn lengths (true: 15 cm = 6.3, 45 cm = 18.9 units)
Z_GOLD, Z_GREEN, Z_RED, Z_MARK, Z_LABEL = -2, -1.9, -1.85, -1.7, 1
LAB_SIZE, NTS_SIZE = 28, 22

_DEFAULT = dict(gold=1.0, gsh=1.0, gold_lab=1.0, g_len=1.0, g_op=1.0, gdrop=1.0, g_lab=1.0, xi=0.0,
                mark=1.0, r_len=1.0, r_op=1.0, rdrop=1.0, r_lab=1.0, glow_g=0.0, glow_r=0.0)


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def _fade(m, op):
    if op >= 0.999:
        return m
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * op, family=False)
        sm.set_fill(opacity=sm.get_fill_opacity() * op, family=False)
    return m


def _vec(z):
    return np.array([z.real, z.imag, 0.0])


def _nts(n):
    return VGroup(T("not to scale:", size=NTS_SIZE, color=DIM),
                  T(f"length {n}", size=NTS_SIZE, color=DIM)).arrange(DOWN, buff=0.06, aligned_edge=LEFT)


_LABS = {}


def _labels():
    """Pre-built label pieces (copied every frame)."""
    if not _LABS:
        _LABS["gold"] = MathTex(r"A\,e^{i\omega t}", font_size=LAB_SIZE, color=GOLD)
        g = MathTex(r"i\omega A\,e^{i\omega t}", font_size=LAB_SIZE, color=GREEN)
        gx = MathTex(r"\times\,\omega", font_size=LAB_SIZE + 4, color=GREEN)
        gn = _nts(15)
        grp = VGroup(g, gn).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        gx.move_to(g, aligned_edge=LEFT)
        _LABS["green"], _LABS["green_x"], _LABS["green_n"] = g, gx, gn
        _LABS["green_box"] = grp
        r = MathTex(r"-\omega^2 A\,e^{i\omega t}", font_size=LAB_SIZE, color=RED)
        rn = _nts(45)
        _LABS["red_box"] = VGroup(r, rn).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        _LABS["xi"] = MathTex(r"\times\, i", font_size=LAB_SIZE + 4, color=GREEN)
    return _LABS


def _side(p0, p1, mob, sign=1, buff=0.15):
    return s2._side(p0, p1, mob, sign=sign, buff=buff)


def _drop(tip, foot, color, op):
    if np.linalg.norm(tip - foot) > 0.05:
        ln = DashedLine(tip, foot, dash_length=0.08).set_stroke(color, 2, opacity=op)
    else:
        ln = Line(tip, foot).set_stroke(color, 2, opacity=0)
    return ln


def _fan_build(tv, st, origin=PLANE3_O, scale=1.0, amp=A3, labels=True, marks=True):
    """One frame of the fan. st: dict of opacities / fractions (see _DEFAULT)."""
    o = np.array(origin, dtype=float)
    z = complex(amp) * cmath.exp(1j * OMEGA3 * tv)
    u = z / abs(z)
    gold_tip = o + CM * scale * _vec(z)
    out = VGroup()
    L = _labels() if labels else None
    # GOLD and its BLUE shadow
    if st["gold"] > 0.01:
        a = ak.arrow_between(o, gold_tip, GOLD, 6 * min(1, scale + 0.3), Z_GOLD)
        out.add(_fade(a, st["gold"]))
    if st["gsh"] > 0.01:
        foot = o + CM * scale * np.array([z.real, 0, 0])
        out.add(_fade(VGroup(_drop(gold_tip, foot, DIM, 1.0),
                             Dot(foot, radius=0.09 * min(1, scale + 0.3), color=BLUE).set_z_index(Z_MARK)),
                      st["gsh"]))
    # GREEN (a quarter turn ahead) and RED (half a turn ahead)
    for key, d, length, col, z_ in (("g", 1j * u, GREEN_LEN, GREEN, Z_GREEN),
                                   ("r", -u, RED_LEN, RED, Z_RED)):
        frac, op = st[key + "_len"], st[key + "_op"]
        if op < 0.01 or frac < 0.02:
            continue
        tip = o + length * scale * frac * _vec(d)
        g = st["glow_" + key]
        c = interpolate_color(ManimColor(col), ManimColor(WHITE), 0.35 * g)
        out.add(_fade(ak.arrow_between(o, tip, c, (6 + 4 * g) * min(1, scale + 0.3), z_), op))
        dop = st["gdrop" if key == "g" else "rdrop"] * op
        if dop > 0.01 and frac > 0.98:
            foot = np.array([tip[0], o[1], 0.0])
            out.add(_fade(VGroup(_drop(tip, foot, col, 0.7),
                                 Dot(foot, radius=0.085 * min(1, scale + 0.3), color=col).set_z_index(Z_MARK)),
                          dop))
    if marks and st["mark"] > 0.01 and st["g_op"] > 0.01:
        s = 0.22 * min(1.0, scale + 0.3)
        d1, d2 = _vec(u), _vec(1j * u)
        m = VMobject().set_points_as_corners([o + s * d1, o + s * (d1 + d2), o + s * d2])
        m.set_stroke(FG, 2.5).set_z_index(Z_MARK)
        out.add(_fade(m, st["mark"] * st["g_op"]))
    if labels:
        if st["gold_lab"] > 0.01:
            m = L["gold"].copy()
            m.move_to(_side(o, gold_tip, m, sign=-1)).set_z_index(Z_LABEL)
            out.add(_fade(m, st["gold_lab"]))
        if st["g_op"] > 0.01:
            tip = o + GREEN_LEN * scale * st["g_len"] * _vec(1j * u)
            box = L["green_box"].copy()
            box.move_to(_side(o, tip, box, sign=1)).set_z_index(Z_LABEL)
            f, nts = box[0], box[1]
            gx = L["green_x"].copy().move_to(f, aligned_edge=LEFT).set_z_index(Z_LABEL)
            parts = VGroup(_fade(f, st["g_lab"] * st["g_op"]),
                           _fade(gx, st["xi"] * st["g_op"]),
                           _fade(nts, max(st["g_lab"], st["xi"]) * st["g_op"]))
            out.add(parts)
            if st["xi"] > 0.01:
                xi = L["xi"].copy().move_to(o + 0.62 * _vec(u * cmath.exp(1j * PI / 4)))
                out.add(_fade(xi.set_z_index(Z_LABEL), st["xi"] * st["g_op"]))
        if st["r_op"] > 0.01 and st["r_lab"] > 0.01:
            tip = o + RED_LEN * scale * st["r_len"] * _vec(-u)
            box = L["red_box"].copy()
            box.move_to(_side(o, tip, box, sign=1)).set_z_index(Z_LABEL)
            out.add(_fade(box, st["r_lab"] * st["r_op"]))
    return out


def fan3(t, origin=PLANE3_O, scale=1.0, labels=True, amp=A3, marks=True):
    """The three arrows a quarter turn apart with their shadow dots (see the module docstring)."""
    st = dict(_DEFAULT)

    def build():
        return _fan_build(_v(t), st, origin, scale, amp, labels, marks)
    if hasattr(t, "get_value"):
        return always_redraw(build)
    return build()


E_V = (r"\dot{x} = v", GREEN, "velocity")
E_ACC = (r"\ddot{x}", RED, "acceleration")
E_P = (r"p", BLUE, "real part")
E_Q = (r"q", PINK, "imag. part")
ENTRIES5_0 = [ak.E_X, ak.E_W, ak.E_ARROW, s2.E_A]
ENTRIES5 = ENTRIES5_0 + [E_V, E_ACC]
MOVE_M9 = "Differentiate the arrow, then take the shadow: × iω turns it a quarter ahead."


def move_m9():
    return kit.move_card(MOVE_M9)


# ═══════════════════════════════ the scene ═══════════════════════════════
RO_LX, RO_NX = 0.0, 0.85                 # readouts: label right edge, number right edge
RO_Y = [0.1, -0.45, -1.0]
COL_X = 2.1                               # derivation column, left edge
BAND_X = -0.3                             # low band, left edge
T_POS = np.array([-6.6, 3.25, 0])         # t readout (top-left slot)
THINK_AT = np.array([3.6, 0.45, 0])


def _num(v, places):
    s = f"{v:.{places}f}"
    if float(s) == 0:
        s = f"{0:.{places}f}"
    return s.replace("-", "−")


def _ro_parts(label_tex, unit, color, y, paren=False):
    lab = MathTex(label_tex, font_size=32, color=color)
    un = T(unit, size=24, color=color)
    return lab, un


def _ro_place(lab, num, un, y, paren=False):
    num.move_to([RO_NX, y, 0], aligned_edge=RIGHT)
    lab.move_to([RO_LX, 0, 0], aligned_edge=RIGHT)
    lab.align_to(num, DOWN)
    if paren:
        lab.shift(0.07 * DOWN)
    un.next_to(num, RIGHT, buff=0.1).align_to(num, DOWN)
    return VGroup(lab, num, un)


def live_ro(label_tex, fn, unit, color, y, places, op):
    lab0, un0 = _ro_parts(label_tex, unit, color, y)

    def build():
        num = T(_num(fn(), places), size=30, color=color)
        return _fade(_ro_place(lab0.copy(), num, un0.copy(), y), op.get_value())
    return always_redraw(build)


def still_ro(label_tex, value, unit, color, y, places=0):
    lab, un = _ro_parts(label_tex, unit, color, y)
    num = T(_num(value, places), size=30, color=color)
    g = _ro_place(lab, num, un, y, paren="(" in label_tex)
    g.lab, g.num, g.unit = lab, num, un
    return g


def _tex(parts, colors=(), size=32):
    m = MathTex(*parts, font_size=size)
    for i, col in colors:
        m[i].set_color(col)
    return m


def _step(text, y):
    """kit.step_label moved to this scene's column (DIM arrow + 22 px label centred at y)."""
    sl = kit.step_label(text, 0)
    sl.shift((COL_X - kit.COL_LEFT) * RIGHT + (y - sl[0].get_center()[1]) * UP)
    return sl


def _dim_label(text, over, y):
    m = T(text, size=22, color=DIM)
    m.move_to([over.get_center()[0], y, 0])
    return m


class Velocity(NarratedScene):
    def construct(self):
        self.t = ValueTracker(0.0)
        self.clk = lambda tau: 0.0
        self.t.add_updater(lambda m: m.set_value(self.clk(self.time)))
        self.add(self.t)
        self.st = {k: ValueTracker(v) for k, v in _DEFAULT.items()}
        for k in ("gold", "gsh", "gold_lab", "g_len", "g_op", "gdrop", "g_lab", "xi", "mark", "r_len", "r_op",
                  "rdrop", "r_lab"):
            self.st[k].set_value(0.0)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(4.0)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.t], run_time=1.0)
        self.remove(*self.mobjects)
        self.wait(0.15)

    # ── the clock (frame-exact: a function of scene time) ─────────────────────────────
    def run_clock(self, rate=CLOCK, ease=0.0):
        v0, t0 = self.t.get_value(), self.time

        def f(tau):
            s = max(tau - t0, 0.0)
            if ease > 0 and s < ease:
                return v0 + rate * ease / 3 * (s / ease) ** 3
            return v0 + (rate * ease / 3 if ease > 0 else 0.0) + rate * (s - ease if ease > 0 else s)
        self.clk = f

    def stop_clock(self, dur=1.5, rate=CLOCK):
        v0, t0 = self.t.get_value(), self.time
        d = rate * dur / 3

        def f(tau):
            s = min(max((tau - t0) / dur, 0.0), 1.0)
            return v0 + d * (1 - (1 - s) ** 3)
        self.clk = f

    def land_clock(self, t2, tmod=0.0, dur=1.5, rate=CLOCK):
        """Reach model time ≡ tmod (mod one period) at scene time t2, easing to rest over dur."""
        v0, t0 = self.t.get_value(), self.time
        t1 = t2 - dur
        d = rate * dur / 3
        n = round((v0 + rate * (t1 - t0) + d - tmod) / PERIOD3)
        tgt = tmod + n * PERIOD3
        while (tgt - d - v0) / (t1 - t0) < 0.6 * rate:
            tgt += PERIOD3
        r1 = (tgt - d - v0) / (t1 - t0)

        def f(tau):
            if tau <= t1:
                return v0 + r1 * (tau - t0)
            s = min((tau - t1) / dur, 1.0)
            return tgt - d * (1 - s) ** 3
        self.clk = f

    def hold_clock(self, value):
        self.clk = lambda tau: value

    def S(self, key, val):
        return self.st[key].animate.set_value(val)

    def zt(self, factor=1.0):
        return factor * A3 * cmath.exp(1j * OMEGA3 * self.t.get_value())

    # ── c3.vel.1: where does the velocity's arrow point? ──────────────────────────────
    def clip1(self):
        with self.say("c3.vel.1") as c:
            self.plane = s2.plane3()
            self.labs = s2.plane_labels()
            self.spring_op = ValueTracker(0.0)
            self.spring = s2.spring3(self.t, op=self.spring_op)
            st = self.st
            self.fan = always_redraw(lambda: _fan_build(self.t.get_value(),
                                                        {k: v.get_value() for k, v in st.items()}))
            self.pin = s2.amp_pin()
            self.leg = kit.legend(ENTRIES5_0, s2.LEG_ROWS3)
            self.ro_op = [ValueTracker(0.0) for _ in range(3)]
            self.ros = [
                live_ro(r"x =", lambda: self.zt().real, "cm", BLUE, RO_Y[0], 1, self.ro_op[0]),
                live_ro(r"\dot{x} =", lambda: self.zt(1j * OMEGA3).real, "cm/s", GREEN, RO_Y[1], 0,
                        self.ro_op[1]),
                live_ro(r"\ddot{x} =", lambda: self.zt(-OMEGA3 ** 2).real, "cm/s²", RED, RO_Y[2], 0,
                        self.ro_op[2]),
            ]
            self.add(*self.ros, self.spring, self.fan)
            self.run_clock(CLOCK, ease=1.2)
            self.play(FadeIn(self.plane), FadeIn(self.labs), self.spring_op.animate.set_value(1.0),  # early: the board returns
                      self.S("gold", 1.0), self.S("gsh", 1.0),
                      FadeIn(self.pin), FadeIn(self.leg), self.S("gold_lab", 1.0),
                      *[o.animate.set_value(1.0) for o in self.ro_op], run_time=1.2)

            c.wait_until("velocity")
            kit.legend_add(self, self.leg, E_V, run_time=1.0,
                           extra=[FlashAround(self.ros[1], color=GREEN, time_width=1.5)])

            c.wait_until("predict")
            self.q_op = ValueTracker(0.0)
            ring = DashedVMobject(Circle(radius=0.5).move_to(PLANE3_O), num_dashes=14).set_stroke(GREEN, 3)
            qm = T("?", size=48, color=GREEN)

            def qb():
                d = _vec(self.zt() * 1j / abs(A3))
                m = qm.copy().move_to(PLANE3_O + 0.95 * d).set_z_index(Z_LABEL)
                return _fade(VGroup(ring.copy(), m), self.q_op.get_value())
            self.q = always_redraw(qb)
            self.add(self.q)
            self.play(self.q_op.animate.set_value(1.0), run_time=1.2)

            c.wait_until("answer")
            self.play(*during([self.q_op.animate.set_value(0.0).build()], 0, 0.4),
                      *during([self.S("g_op", 1.0).build(), self.S("xi", 1.0).build(),
                               self.S("mark", 1.0).build()], 0.3, 0.6),
                      *during([self.S("g_len", 1.0).build()], 0.3, 1.0), run_time=2.0)
            self.remove(self.q)

            c.wait_until("match")
            self.st["gdrop"].set_value(0.0)
            self.play(self.S("gdrop", 1.0), run_time=1.0)
            self.play(FlashAround(self.ros[1], color=GREEN, time_width=1.5),
                      self.st["glow_g"].animate(rate_func=there_and_back).set_value(1.0),
                      run_time=1.6)

    # ── c3.vel.2: the caption, then why ──────────────────────────────────────────────
    def clip2(self):
        with self.say("c3.vel.2") as c:
            self.cap = _tex([r"\dot{x}", "=", r"\mathrm{Re}\Big[\,", "i", r"\omega A\,e^{i\omega t}",
                             r"\,\Big]"], [(0, GREEN), (3, PINK)], size=40)
            self.cap.move_to([COL_X, 2.5, 0], aligned_edge=LEFT)
            self.cap_ul = underline(VGroup(self.cap[3], self.cap[4]), GREEN, buff=0.1).set_stroke(width=4)
            self.play(*appear(self.cap), *during([self.S("xi", 0.0).build()], 0, 0.45),
                      *during([self.S("g_lab", 1.0).build()], 0.5, 1.0), run_time=1.5)
            self.play(GrowFromEdge(self.cap_ul, LEFT),
                      self.st["glow_g"].animate(rate_func=there_and_back).set_value(1.0), run_time=1.2)

            c.wait_until("v")
            self.l1 = _tex([r"v", "=", r"\dot{x}", "=", r"\dfrac{d}{dt}\,\mathrm{Re}\Big[",
                            r"A\,e^{i\omega t}", r"\Big]"], [(0, GREEN), (2, GREEN), (5, GOLD)], size=30)
            self.l1.move_to([COL_X, 1.2, 0], aligned_edge=LEFT)
            self.cap_tag = kit.tag("(83) · notes p. 109").move_to([COL_X, 2.05, 0], aligned_edge=LEFT)
            self.sl1 = _step("velocity: rate of change of x", 1.72)
            self.play(*appear(self.sl1, self.l1, lag=0.3, shift=None), *during(appear(self.cap_tag, shift=None), 0.5, 1.0),  # early: reference tag
                      run_time=1.5)
            x_eq = self.l1[3].get_center()[0]

            def eq_line(parts, colors, y):
                m = _tex(parts, colors, size=30)
                m.move_to([0, y, 0])
                m.shift((x_eq - m[0].get_center()[0]) * RIGHT)
                return m

            c.wait_until("swap")
            self.l2 = eq_line(["=", r"\mathrm{Re}\Bigg[\dfrac{d}{dt}\Big(", r"A\,e^{i\omega t}",
                               r"\Big)\Bigg]"], [(2, GOLD)], 0.1)
            self.sl2 = _step("shadow of the derivative", 0.65)
            derive(self, self.l1, self.l2, run_time=1.8)
            self.play(*appear(self.sl2, shift=None), run_time=0.8)

            c.wait_until("The derivative of a shadow")
            self.side = _tex([r"\dfrac{d}{dt}", r"\big(", "p", "+", "i", "q", r"\big)", "=", r"\dot{p}",
                              "+", "i", r"\dot{q}"], [], size=28)
            self.side.set_color(DIM)
            for i, col in ((2, BLUE), (5, PINK), (8, BLUE), (11, PINK)):
                self.side[i].set_color(col)
            self.side.move_to([BAND_X, -2.72, 0], aligned_edge=LEFT)
            self.side_w = T("each part on its own", size=22, color=DIM).next_to(self.side, RIGHT, buff=0.3)
            self.commute = T("Re and d/dt commute", size=24, color=FG).move_to([BAND_X - 0.3, -3.28, 0],
                                                                              aligned_edge=LEFT)
            self.commute_tag = kit.tag("lecturer's rule · notes p. 110", self.commute)
            kit.legend_add(self, self.leg, E_P, E_Q, run_time=1.5,
                           extra=appear(self.side, self.side_w, lag=0.4, shift=None))
            c.wait_until("separately")
            self.play(*appear(self.commute, self.commute_tag, lag=0.3, shift=None), run_time=1.2)  # early: the rule's name and its tag

            c.wait_until("fixed")
            self.l3 = eq_line(["=", r"\mathrm{Re}\Bigg[", "A", r"\,\dfrac{d}{dt}\,", r"e^{i\omega t}",
                               r"\Bigg]"], [(2, GOLD), (4, GOLD)], -1.0)
            self.sl3 = _step("A doesn't change", -0.45)
            derive(self, self.l2, self.l3, run_time=1.8)
            self.play(*appear(self.sl3, shift=None), run_time=0.8)

            c.wait_until("iw")
            self.l4 = eq_line(["=", r"\mathrm{Re}\Big[\,", "i", r"\omega", r"A\,e^{i\omega t}", r"\Big]"],
                              [(2, PINK), (4, GOLD)], -2.0)
            self.sl4 = _step("part two: × iω", -1.56)
            derive(self, self.l3, self.l4, run_time=1.8)
            self.play(*appear(self.sl4, shift=None), run_time=0.8)

            c.wait_until("The derivative of E")
            self.play(FlashAround(VGroup(self.l4[2], self.l4[3]), time_width=1.5),
                      *set_alpha([self.l1, self.l2, self.sl1, self.sl2], 0.4), run_time=1.5)

    # ── c3.vel.3: the move; do it twice ──────────────────────────────────────────────
    def clip3(self):
        with self.say("c3.vel.3") as c:
            self.card = move_m9()
            leaving = [self.l1, self.l2, self.l3, self.l4, self.sl1, self.sl2, self.sl3, self.sl4,
                       self.side, self.side_w, self.commute, self.commute_tag]
            cap_dy = 1.2 - self.cap.get_center()[1]
            kit.legend_remove(self, self.leg, "p", "q", run_time=2.2,
                              extra=[*during(disappear(*leaving), 0, 0.35),
                                     *during([self.cap.animate.shift(cap_dy * UP).build(),
                                              self.cap_ul.animate.shift(cap_dy * UP).build(),
                                              self.cap_tag.animate.move_to([COL_X, 0.77, 0], aligned_edge=LEFT).build()],
                                             0.3, 0.75),
                                     *during(appear(self.card), 0.65, 1.0)])

            c.wait_until("words")
            lines = [r"\text{to differentiate } e^{i\omega t} \text{ we simply}",
                     r"\text{multiply by } i\omega \text{ before taking}",
                     r"\text{the real part}"]
            body = VGroup(*[MathTex(s, font_size=28) for s in lines]).arrange(DOWN, buff=0.12,
                                                                                aligned_edge=LEFT)
            box = SurroundingRectangle(body, buff=0.18, corner_radius=0.08).set_stroke(YELLOW, 2.5)
            self.words = VGroup(box, body)
            self.words.move_to([COL_X - 0.05, -0.3, 0], aligned_edge=LEFT)
            self.play(*appear(self.words), run_time=1.5)  # early: the notes' sentence, read through

            c.wait_until("rate comes down")
            self.lam = _tex([r"\dfrac{d}{dt}\,e^{\lambda t}", "=", r"\lambda\,e^{\lambda t}"], [], size=30)
            self.lam.set_color(DIM)
            self.lam.move_to([COL_X, -1.55, 0], aligned_edge=LEFT)
            self.lam_tag = kit.tag("part two", self.lam)
            self.play(*appear(self.lam, self.lam_tag, lag=0.3), run_time=1.2)

            c.wait_until("red")
            self.sq = _tex([r"(i\omega)^2", "=", r"-\omega^2"], [(2, RED)], size=36)
            self.sq.move_to([COL_X, -2.55, 0], aligned_edge=LEFT)
            self.play(*appear(self.sq), *during([self.S("r_op", 1.0).build(), self.S("r_lab", 1.0).build()], 0.3, 0.6),
                      *during([self.S("r_len", 1.0).build()], 0.3, 1.0), run_time=2.0)

            c.wait_until("The red arrow")
            self.play(self.st["glow_r"].animate(rate_func=there_and_back).set_value(1.0), run_time=1.4)
            c.wait_until("acceleration")
            kit.legend_add(self, self.leg, E_ACC, run_time=min(1.5, c.until(floor=0.8)),
                           extra=[FlashAround(self.ros[2], color=RED, time_width=1.5)])

    # ── c3.vel.4: the fan; the third weight's numbers ───────────────────────────────
    def clip4(self):
        with self.say("c3.vel.4") as c:
            self.land_clock(c.at("starts"), 0.0, dur=1.5)
            self.tro_op = ValueTracker(0.0)
            tl = MathTex(r"t =", font_size=32)
            tu = T("s", size=24)

            def trb():
                num = T(_num(self.t.get_value(), 2), size=30)
                l = tl.copy().move_to(T_POS, aligned_edge=LEFT)
                num.next_to(l, RIGHT, buff=0.15).align_to(l, DOWN)
                u = tu.copy().next_to(num, RIGHT, buff=0.1).align_to(num, DOWN)
                return _fade(VGroup(l, num, u), self.tro_op.get_value())
            self.tro = always_redraw(trb)
            self.add(self.tro)
            self.play(self.tro_op.animate.set_value(1.0), *disappear(self.words, self.lam, self.lam_tag),
                      self.st["glow_g"].animate(rate_func=there_and_back).set_value(1.0),
                      self.st["glow_r"].animate(rate_func=there_and_back).set_value(1.0), run_time=1.5)

            c.wait_until("list")
            self.list = [
                _tex([r"x", r":\ ", "A"], [(0, BLUE), (2, GOLD)], size=32),
                _tex([r"\dot{x}", r":\ ", r"i\omega A"], [(0, GREEN), (2, GREEN)], size=32),
                _tex([r"\ddot{x}", r":\ ", r"-\omega^2 A"], [(0, RED), (2, RED)], size=32),
            ]
            for m, y in zip(self.list[::-1], (-0.8, -0.25, 0.3)):
                m.move_to([COL_X, y, 0], aligned_edge=LEFT)
                m.shift((self.list[2][1].get_right()[0] - m[1].get_right()[0]) * RIGHT)
            self.play(*disappear(self.sq), *set_alpha([self.cap, self.cap_ul, self.cap_tag], 0.4),
                      *during(appear(self.list[0], shift=None), 0.4, 1.0), run_time=1.5)
            c.wait_until("velocity has")
            self.play(*appear(self.list[1], shift=None), run_time=1.0)
            c.wait_until("acceleration has")
            self.play(*appear(self.list[2], shift=None), run_time=1.0)
            self.list_tag = VGroup(T("each oscillating quantity via", size=22, color=DIM),
                                   T("complex amplitudes · notes p. 110", size=22, color=DIM)
                                   ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
            self.list_tag.move_to([COL_X, -1.3, 0], aligned_edge=LEFT)
            self.play(*appear(self.list_tag, shift=None), run_time=1.0)

            c.wait_until("ours")
            self.rA = _tex([r"A", "=", "3", "-", "4i"], [(0, GOLD)], size=30)
            self.rA.move_to([BAND_X, -1.95, 0], aligned_edge=LEFT)
            self.r2 = _tex([r"i\omega A", "=", r"3i(3-4i)", "=", r"9i-12i^2", "=", "12", "+", "9i"],
                           [(0, GREEN)], size=30)
            self.r2.move_to([BAND_X, -2.62, 0], aligned_edge=LEFT)
            self.r3 = _tex([r"-\omega^2 A", "=", r"-9(3-4i)", "=", r"-27", "+", "36i"], [(0, RED)], size=30)
            self.r3.move_to([BAND_X, -3.28, 0], aligned_edge=LEFT)
            self.r3.shift((self.r2[1].get_center()[0] - self.r3[1].get_center()[0]) * RIGHT)
            self.rA.shift((self.r2[1].get_center()[0] - self.rA[1].get_center()[0]) * RIGHT)
            for m in (self.rA, self.r2, self.r3):     # clear of the legend's right edge (-0.8)
                m.shift(0.4 * RIGHT)
            self.lab2a = _dim_label("× 3i", self.r2[1], -2.28)
            self.lab2b = _dim_label("i squared is −1", self.r2[5], -2.28)
            self.lab3 = _dim_label("× (−9)", self.r3[1], -2.95)
            self.play(*appear(self.rA, shift=None), run_time=1.0)
            c.wait_until("three eye")
            self.play(*appear(VGroup(self.r2[0], self.r2[1], self.r2[2]), self.lab2a,
                              VGroup(*self.r2[3:5]), VGroup(*self.r2[5:]), self.lab2b, lag=0.3, shift=None),
                      run_time=2.0)
            c.wait_until("minus nine")
            self.play(*appear(VGroup(*self.r3[0:3]), self.lab3, VGroup(*self.r3[3:]), lag=0.35, shift=None),
                      run_time=1.5)

            c.wait_until("starts")
            self.hold_clock(0.0)
            self.stills = [still_ro(r"x(0) =", 3, "cm", BLUE, RO_Y[0]),
                           still_ro(r"\dot{x}(0) =", 12, "cm/s", GREEN, RO_Y[1]),
                           still_ro(r"\ddot{x}(0) =", -27, "cm/s²", RED, RO_Y[2])]
            srcs = [self.rA[2], self.r2[6], self.r3[4]]
            cols = [BLUE, GREEN, RED]
            self.uls = [underline(s, col, buff=0.08).set_stroke(width=4) for s, col in zip(srcs, cols)]
            cues = ["three centimetres", "twelve", "twenty-seven"]
            for k in range(3):
                if k:
                    c.wait_until(cues[k])
                self.play(GrowFromEdge(self.uls[k], LEFT), FlashAround(srcs[k], color=cols[k], time_width=1.5),
                          *during([self.ro_op[k].animate.set_value(0.0).build()], 0, 0.45),
                          *during(appear(self.stills[k], shift=None), 0.5, 1.0), run_time=1.3)
            self.remove(*self.ros)

            c.wait_until("rule")
            rl = _tex([r"-\omega^2 A", "=", r"-\omega^2", r"\cdot", "A"], [(0, RED), (4, GOLD)], size=32)
            rr = _tex([r"\ddot{x}", "=", r"-\omega^2", "x"], [(0, RED), (3, BLUE)], size=32)
            pair = VGroup(rl, rr).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            rbox = SurroundingRectangle(pair, buff=0.16, corner_radius=0.08).set_stroke(YELLOW, 2.5)
            self.rule = VGroup(rbox, pair)
            self.rule.move_to([COL_X - 0.05, 1.05, 0], aligned_edge=LEFT)
            self.play(*swap(VGroup(self.cap, self.cap_ul, self.cap_tag), self.rule), run_time=1.5)
            c.wait_until("now holds")
            self.play(FlashAround(self.rule, time_width=1.5), run_time=min(1.5, max(0.4, c.remaining - 0.05)))

    # ── c3.vel.5: think stop: amplitude 2, ω = 3 ────────────────────────────────────
    def clip5(self):
        with self.say("c3.vel.5") as c:
            keep_off = [*self.list, self.list_tag, self.rA, self.r2, self.r3, self.lab2a, self.lab2b,
                        self.lab3, *self.uls, self.rule, *self.stills]
            self.box = kit.think_box("A complex amplitude of 2,\n"
                                     "with ω = 3. What's the velocity's\n"
                                     "complex amplitude, and what is\n"
                                     "the weight doing at t = 0?", size=30, pos=THINK_AT)
            self.ring = kit.think_ring()
            self.play(*during(disappear(*keep_off), 0, 0.45), self.tro_op.animate.set_value(0.0),
                      *during([restyle(self.card, 0.6)], 0, 0.6),
                      *during(appear(self.box.box, self.box.question, self.box.hint, self.ring, shift=None, lag=0.1), 0.5, 1.0),  # early: the think box is read whole
                      run_time=2.0)

            c.wait_until("Pause the video")
            self.play(kit.drain(self.ring, run_time=c.until("mult")))

            # the answer
            a1 = _tex([r"i\omega A", "=", "3", "i", r"\cdot", "2"], [(0, GREEN), (3, PINK)], size=40)
            a1.move_to([COL_X, 1.3, 0], aligned_edge=LEFT)
            self.play(*swap(self.box, a1), *disappear(self.ring), restyle(self.card, 1.0), run_time=1.2)
            c.wait_until("six eye")
            a1b = _tex(["=", "6", "i"], [(2, PINK)], size=40).next_to(a1, RIGHT, buff=0.2)
            a1b.align_to(a1[1], DOWN)
            self.play(*appear(a1b), run_time=1.0)

            c.wait_until("still")
            self.v6_op = ValueTracker(0.0)
            self.v6_len = ValueTracker(0.0)
            L6 = 2.3
            lab6 = VGroup(MathTex(r"6i", font_size=32, color=GREEN), _nts(6)).arrange(DOWN, buff=0.1,
                                                                                     aligned_edge=RIGHT)

            def v6():
                tip = PLANE3_O + L6 * max(self.v6_len.get_value(), 0.02) * UP
                a = ak.arrow_between(PLANE3_O, tip, GREEN, 6, Z_GREEN)
                d = Dot(PLANE3_O, radius=0.1, color=GREEN).set_z_index(Z_MARK)
                lb = lab6.copy().next_to(PLANE3_O + 0.55 * L6 * UP, LEFT, buff=0.18).set_z_index(Z_LABEL)
                return _fade(VGroup(a, d, lb), self.v6_op.get_value())
            self.v6 = always_redraw(v6)
            self.add(self.v6)
            a2 = _tex([r"\mathrm{Re}\,[\,6i\,]", "=", "0"], [(2, GREEN)], size=36)
            a2.move_to([COL_X, 0.4, 0], aligned_edge=LEFT)
            self.ro_v0 = still_ro(r"\dot{x}(0) =", 0, "cm/s", GREEN, RO_Y[1])
            self.still_tag = kit.tag("still, for an instant").move_to([BAND_X + 0.3, RO_Y[2], 0], aligned_edge=LEFT)
            self.play(*during([self.S("gold", 0.0).build(), self.S("gsh", 0.0).build(),
                               self.S("gold_lab", 0.0).build(), self.S("g_op", 0.0).build(),
                               self.S("r_op", 0.0).build(), self.spring_op.animate.set_value(0.0).build()],
                              0, 0.45),
                      *during([self.v6_op.animate.set_value(1.0).build(),
                               self.v6_len.animate.set_value(1.0).build()], 0.4, 1.0),
                      *during(appear(a2, self.ro_v0), 0.5, 1.0), run_time=2.0)
            self.remove(self.fan, self.spring, self.tro)
            c.wait_until("for an instant")
            self.play(*appear(self.still_tag), run_time=1.0)

            c.wait_until("end")
            self.gold2 = ak.arrow_between(PLANE3_O, s2.pt(2), GOLD, 6, Z_GOLD)
            g2lab = MathTex(r"A = 2", font_size=30, color=GOLD).move_to(s2.pt(1.0) + 0.75 * DOWN)
            sp2 = s2.spring3(0.0, amp=2)
            sh2 = Dot(s2.pt(2), radius=0.1, color=BLUE).set_z_index(Z_MARK)
            ro_x2 = still_ro(r"x(0) =", 2, "cm", BLUE, RO_Y[0])
            a3 = _tex([r"x", "=", r"2\cos 3t"], [(0, BLUE)], size=36)
            a3.move_to([COL_X, -0.5, 0], aligned_edge=LEFT)
            self.play(GrowArrow(self.gold2), FadeIn(sp2), FadeIn(sh2), *appear(g2lab, ro_x2, lag=0.3),
                      run_time=1.5)
            c.wait_until("far end")
            self.play(*appear(a3), FlashAround(sh2, color=BLUE, time_width=1.5), run_time=1.5)
