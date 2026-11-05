"""Chapter 2, scene 4: half a turn, back to the centre (d²/dt² e^{iωt} = −ω² e^{iωt}). Clips c2.acc.1 – c2.acc.3.

Exports (for the recap, s9):
  FAN_SCALE  the zoomed plane's scale (unit circle 0.6 units), so 1, 2, 4 keep their true lengths.
  fan(t, scale=FAN_SCALE, origin=PLANE_O, glow=0.0, width=6)
             GOLD e^{iωt}, GREEN iω e^{iωt} and RED −ω² e^{iωt}, all from the origin, plus the two
             right-angle marks between neighbours (GOLD→GREEN, GREEN→RED). `t`, `scale`, `glow`
             take a ValueTracker (live) or a number (still). .gold .green .red .m1 .m2
  zoom_plane(sc)  the arrow kit's plane, live while tracker sc runs 1 → FAN_SCALE (a camera zoom:
             same frame, the grid gets denser); at FAN_SCALE it matches plane(FAN_SCALE, re 4, im 3.5).
"""
# style: 2
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

PLANE_O = ak.PLANE_O
OMEGA = ak.OMEGA
FAN_SCALE = 0.6 / ak.PLANE_R          # unit circle 0.6 units: GOLD 0.6, GREEN 1.2, RED 2.4
_v = ak._v


def fan(t, scale=FAN_SCALE, origin=PLANE_O, glow=0.0, width=6):
    """GOLD, GREEN and RED from the origin turning together, with right-angle marks between
    neighbours. .gold .green .red .m1 (GOLD→GREEN) .m2 (GREEN→RED)"""
    def dyn(build):
        return ak._dyn(build, t, scale, glow)

    gold = dyn(lambda: ak.turning_arrow(_v(t), scale=_v(scale), origin=origin, width=width))
    green = dyn(lambda: ak.velocity_arrow(_v(t), base=0.0, scale=_v(scale), origin=origin,
                                          width=width))
    red = dyn(lambda: ak.accel_arrow(_v(t), base=0.0, scale=_v(scale), origin=origin, width=width))
    m1 = dyn(lambda: ak.right_angle(_v(t), at_tip=False, scale=_v(scale), origin=origin,
                                    glow=_v(glow)))
    m2 = dyn(lambda: ak.right_angle(_v(t), at_tip=False, offset=PI / 2, scale=_v(scale),
                                    origin=origin, glow=_v(glow)))
    g = VGroup(gold, green, red, m1, m2)
    g.gold, g.green, g.red, g.m1, g.m2 = gold, green, red, m1, m2
    return g


def zoom_plane(sc, origin=PLANE_O):
    """The kit's plane while tracker sc zooms 1 → FAN_SCALE: the frame stays about the same
    size, the grid gets denser (re 2 → 4 units, im 1.5 → 3.5)."""
    o = np.array(origin, dtype=float)
    re0, im0 = T("Re", size=28, color=DIM), T("Im", size=28, color=DIM)

    def build():
        s = _v(sc)
        a = (1 - s) / (1 - FAN_SCALE)
        u = ak.PLANE_R * s
        X = interpolate(2.0 * ak.PLANE_R, 4.0 * ak.PLANE_R * FAN_SCALE, a)
        Y = interpolate(1.5 * ak.PLANE_R, 3.5 * ak.PLANE_R * FAN_SCALE, a)
        kx, ky = int(X / (0.5 * u) + 1e-6), int(Y / (0.5 * u) + 1e-6)
        grid = VGroup(*[Line(o + [k * 0.5 * u, -Y, 0], o + [k * 0.5 * u, Y, 0])
                        for k in range(-kx, kx + 1)],
                      *[Line(o + [-X, k * 0.5 * u, 0], o + [X, k * 0.5 * u, 0])
                        for k in range(-ky, ky + 1)])
        grid.set_stroke(DIM, 1, opacity=0.35)
        ext = 0.25 * u
        re_ax = Line(o + [-(X + ext), 0, 0], o + [X + ext, 0, 0])
        im_ax = Line(o + [0, -(Y + ext), 0], o + [0, Y + ext, 0])
        axes = VGroup(re_ax, im_ax).set_stroke(DIM, 2.5)
        circle = Circle(radius=u).move_to(o).set_stroke(DIM, 2.5)
        f = interpolate(1.0, 22 / 28, a)
        re = re0.copy().scale(f).next_to(re_ax.get_end(), RIGHT, buff=0.15)
        im = im0.copy().scale(f).next_to(im_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
        g = VGroup(grid, axes, circle, re, im)
        g.set_z_index(-4)
        return g
    return always_redraw(build)


def chevron(t=ak.T_END, scale=FAN_SCALE, origin=PLANE_O):
    """A short RED arrow just outside the GOLD tip, pointing at the centre."""
    tip = ak.plane_point(ak.phasor(t), scale, origin)
    u = (tip - np.array(origin, dtype=float))
    u = u / np.linalg.norm(u)
    return ak.arrow_between(tip + 0.72 * u, tip + 0.1 * u, RED, 5, -1.6)


def _ci(y):
    return (kit.COL_TOP - y) / kit.COL_PITCH


def _cj(y):
    return (kit.COL_TOP - y) / kit.COL_PITCH + 0.5


G_ANGLE = OMEGA * ak.T_END + PI / 2      # GREEN's angle in the frozen shot (130°)


class Accel(NarratedScene):
    def construct(self):
        hs = ak.handover_shot()
        self.t = ak.clock(ValueTracker(ak.T_END))
        self.sc = ValueTracker(1.0)
        self.glow = ValueTracker(0.0)
        self.add(self.t, self.sc, self.glow)
        self.F = fan(self.t, self.sc, glow=self.glow)
        # s3's last frame, with the two arrows made live (identical drawing)
        self.pl = hs.plane
        self.pin, self.leg, self.card, self.cap = hs.pin, hs.legend, hs.card, hs.caption
        self.add(self.pl, self.pin, self.leg, self.card, self.cap, self.F.gold, self.F.green)
        self.clip1()
        self.clip2()
        self.clip3()
        ak.run(self.t, False)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c2.acc.1: think stop T2.2 ─────────────────────────────────────────────────
    def clip1(self):
        self.think = kit.think_box("The velocity: a quarter turn ahead,\nstretched by ω.\n"
                                   "Where does the acceleration point,\nand how long is it?",
                                   size=30, pos=np.array([2.8, -1.75, 0]))
        self.ring = kit.think_ring()
        with self.say("c2.acc.1") as c:
            self.play(*set_alpha([self.card], 0.6),
                      FlashAround(self.cap.line[0], color=GREEN, time_width=1.5), run_time=1.4)
            c.wait_until("the velocity")
            self.play(*appear(self.think, self.ring, shift=None, lag=0.2),  # early: the think box is read whole
                      run_time=1.2)
            c.wait_until("pause the video")
            self.play(kit.drain(self.ring, run_time=max(1.0, c.until(None) - 0.25)))

    # ── c2.acc.2: a further quarter turn, a further stretch: the RED arrow ──────────
    def clip2(self):
        sc, F = self.sc, self.F
        rot, st, col = ValueTracker(0.0), ValueTracker(2.0), ValueTracker(0.0)
        self.add(rot, st, col)

        def copy_build():
            z = st.get_value() * complex(math.cos(G_ANGLE + rot.get_value()),
                                         math.sin(G_ANGLE + rot.get_value()))
            c_ = interpolate_color(ManimColor(GREEN), ManimColor(RED), col.get_value())
            return ak.arrow_between(PLANE_O, ak.plane_point(z, sc.get_value()), c_, 6, -1.75)
        copy = always_redraw(copy_build)

        times_i = MathTex(r"\times", "i", font_size=40, color=PINK)
        mid_a = G_ANGLE + PI / 4

        def place_i(m):
            m.move_to(ak.plane_point(1.55 * complex(math.cos(mid_a), math.sin(mid_a)),
                                     sc.get_value()))
        place_i(times_i)
        times_i.add_updater(place_i)
        times_2 = MathTex(r"\times", "2", font_size=40, color=FG)
        r_ang = G_ANGLE + PI / 2

        def place_2(m):
            d = complex(math.cos(r_ang), math.sin(r_ang))
            mid = ak.plane_point(0.5 * st.get_value() * d, sc.get_value())
            m.move_to(mid + 0.45 * np.array([-d.imag, d.real, 0]))
        place_2(times_2)
        times_2.add_updater(place_2)

        with self.say("c2.acc.2") as c:
            self.play(*disappear(self.think, self.ring), *set_alpha([self.card], 1.0),
                      FadeIn(F.m1), run_time=1.0)
            self.add(copy)
            self.play(rot.animate.set_value(PI / 2), *appear(times_i), run_time=1.6)
            c.wait_until("stretch")
            # the zoom: GREEN's copy stretches ×2 into the RED arrow while the plane zooms out
            zp = zoom_plane(sc)
            self.remove(self.pl)
            self.add(zp)
            self.pl = zp
            self.play(st.animate.set_value(4.0), col.animate.set_value(1.0),
                      sc.animate.set_value(FAN_SCALE), *during([FadeIn(F.m2)], 0, 0.3),
                      *during(appear(times_2, shift=None), 0.55, 1.0), run_time=2.6)
            self.remove(copy)
            self.add(F.red)
            c.wait_until("two quarter turns")
            self.play(self.glow.animate(rate_func=there_and_back).set_value(1.0), run_time=1.4)
            c.wait_until("straight back")
            self.chev = chevron()
            self.toward = T("toward the centre", size=28, color=RED)
            self.toward.move_to([-2.45, 1.62, 0], aligned_edge=LEFT)
            set_backstroke(self.toward, width=5)
            self.play(GrowArrow(self.chev), *appear(self.toward), run_time=1.3)
            c.wait_until("len")
            self.len_a = MathTex(r"\text{length}", r"\ \omega^2", font_size=40, color=RED)
            self.len_a.move_to([-1.95, -1.05, 0])
            self.len_b = MathTex("=", "4", font_size=40)
            self.len_b[1].set_color(GOLD)
            self.len_b.next_to(self.len_a, RIGHT, buff=0.2)
            for m in (self.len_a, self.len_b):
                set_backstroke(m, width=5)
            self.play(*during(disappear(times_i, times_2), 0, 0.4),
                      *during(appear(self.len_a), 0.35, 1.0), run_time=1.4)
            c.wait_until("four")
            self.play(*appear(self.len_b), run_time=1.0)
            c.wait_until("caption")
            # the column: the velocity caption dims, the second derivative stacks under it
            l1 = MathTex(r"\frac{d^2}{dt^2}\,", r"e^{i\omega t}", "=", "i", r"\omega", r"\cdot", "i",
                         r"\omega", r"\,", r"e^{i\omega t}", font_size=kit.COL_SIZE)
            l1[0].set_color(RED)
            l1[1].set_color(RED)
            l1[3].set_color(PINK)
            l1[6].set_color(PINK)
            l1[9].set_color(GOLD)
            kit.col_place(l1, _ci(-0.12))
            s1 = kit.step_label("×iω again", _cj(0.47))
            eq_x = l1[2].get_center()[0]
            l2 = MathTex("=", "(", "i", r"\omega", ")^2", r"\,", r"e^{i\omega t}",
                         font_size=kit.COL_SIZE)
            l2[2].set_color(PINK)
            l2[6].set_color(GOLD)
            kit.col_place(l2, _ci(-1.12))
            l2.shift((eq_x - l2[0].get_center()[0]) * RIGHT)
            s2 = kit.step_label("collect", _cj(-0.68))
            l3 = MathTex("=", r"-\omega^2", r"\,", r"e^{i\omega t}", font_size=kit.COL_SIZE + 2)
            l3[3].set_color(GOLD)
            kit.col_place(l3, _ci(-2.02))
            l3.shift((eq_x - l3[0].get_center()[0]) * RIGHT)
            s3 = kit.step_label("i² = −1", _cj(-1.6))
            box3 = SurroundingRectangle(VGroup(l3[1], l3[3]), color=YELLOW, buff=0.14)
            box3.set_stroke(YELLOW, 3)
            self.ctag = kit.corner_tag()
            self.play(*set_alpha([self.cap], 0.4),
                      *appear(self.ctag, shift=None), run_time=1.0)  # early: the tier tag
            c.wait_until("multiply")
            self.play(*appear(s1, l1, shift=None, lag=0.3), run_time=1.4)
            c.wait_until("all squared")
            self.play(*appear(s2, l2, shift=None, lag=0.3),
                      run_time=min(1.3, c.until("is minus", floor=0.8)))
            c.wait_until("is minus")
            self.play(*appear(s3, l3, shift=None, lag=0.3), *set_alpha([l1], 0.4),
                      run_time=min(1.3, c.until(None, floor=0.8)))
            self.col = [l1, l2, l3, s1, s2, s3]
            self.box3 = box3
            self.l3 = l3

    # ── c2.acc.3: the fan turns; the rule; why ω²; toward the centre ──────────────
    def clip3(self):
        t, F = self.t, self.F
        with self.say("c2.acc.3") as c:
            self.wt = ak.wt_readout(t, size=26).move_to([-6.5, 2.95, 0], aligned_edge=LEFT)
            self.play(GrowFromCenter(self.box3),
                      *during(disappear(self.chev, self.toward, self.len_a, self.len_b), 0, 0.5),
                      *during(appear(self.wt, shift=None), 0.4, 1.0), run_time=1.2)
            ak.run(t, True)
            rule = VGroup(T("acceleration", size=30, color=RED), T("=", size=30),
                          MathTex(r"-\omega^2", font_size=36), T("×", size=30),
                          T("position", size=30, color=GOLD)).arrange(RIGHT, buff=0.15)
            rule[2].shift(0.03 * UP)
            kit.col_place(rule, _ci(-2.92))
            c.wait_until("rule")
            self.play(FlashAround(self.pin.formula, time_width=1.5), *appear(rule), run_time=1.5)
            c.wait_until("that's the rule")
            self.play(FlashAround(self.pin.formula, time_width=1.5),
                      FlashAround(rule, time_width=1.5), run_time=1.5)
            c.wait_until("why_sq")
            w = self.pin.formula[2][1]
            note = kit.tag("ω = the arrow's turning rate")
            note.next_to(self.pin.formula, DOWN, buff=0.14)
            self.play(*recolor([w], YELLOW), FlashAround(w, time_width=1.5), run_time=1.4)
            c.wait_until("omega itself")
            self.play(*appear(note), FlashAround(self.wt, time_width=1.5),  # early: the note names ω on its sentence
                      run_time=1.4)
            c.wait_until("centre")
            # freeze on the GOLD-at-40° pose, then the pull toward the centre
            ak.run(t, False)
            cur = t.get_value()
            target = ak.T_END + math.ceil((cur - ak.T_END) / PI + 1e-6) * PI
            self.play(t.animate.set_value(target), rate_func=linear, run_time=target - cur)
            chev = chevron()
            cp = kit.tag("centripetal acceleration")      # by the RED arrow, in the empty quadrant
            cp.move_to([-3.0, -0.8, 0], aligned_edge=LEFT)
            set_backstroke(cp, width=5)
            self.play(GrowArrow(chev), *appear(cp, shift=None), run_time=1.0)
            u = -chev.get_vector() / np.linalg.norm(chev.get_vector())
            self.play(chev.animate(rate_func=there_and_back).shift(-0.18 * u), run_time=0.9)
        self.wait(1.2)      # the picture holds: pulled toward the centre
        self.play(chev.animate(rate_func=there_and_back).shift(-0.18 * u), run_time=0.9)
        self.wait(1.6)
