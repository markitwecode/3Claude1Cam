"""Chapter 6, scene 3: which way current flows, and how much. Clips c6.current.1 – c6.current.4.

Opens on ch6_s2_electrons' handover (the loop, electrons at rest), sets them drifting.
Shared: i_eq_qt(size) -> the I = Q/t formula (I GOLD), reused small by s5 and s8.
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

S2 = load_scene("ch6_s2_electrons")
DRIFT = S2.DRIFT


def i_eq_qt(size=120):
    """I = Q / t, I in GOLD. Parts: [0] I, [1] =, [2] Q, [3] /, [4] t."""
    m = MathTex("I", "=", "Q", "/", "t", font_size=size)
    m[0].set_color(GOLD)
    return m


def polyline_at(pts, d):
    """Point at arc length d along the polyline pts."""
    for a, b in zip(pts[:-1], pts[1:]):
        seg = np.linalg.norm(b - a)
        if d <= seg:
            return a + (b - a) * (d / seg)
        d -= seg
    return pts[-1]


def ghost_charge(r=0.2):
    ring = DashedVMobject(Circle(radius=r), num_dashes=10).set_stroke(GOLD, 3)
    s = 0.5 * r
    plus = VGroup(Line(LEFT * s, RIGHT * s), Line(DOWN * s, UP * s)).set_stroke(GOLD, 3)
    return VGroup(ring, plus)


def stopwatch(r=0.45):
    face = Circle(radius=r).set_stroke(FG, 4).set_fill(BG, 1)
    knob = Rectangle(width=0.16, height=0.14).set_stroke(FG, 3).set_fill(FG, 1).next_to(face, UP, buff=0)
    ticks = VGroup(*[Line(UP * r * 0.78, UP * r * 0.92).rotate(k * TAU / 12, about_point=ORIGIN)
                     for k in range(12)]).set_stroke(DIM, 2)
    hand = Line(ORIGIN, UP * r * 0.8).set_stroke(GOLD, 4)
    w = VGroup(face, knob, ticks, hand)
    w.face, w.hand = face, hand
    return w


TUBE_Y, TUBE_R = 1.6, 0.55


class Current(NarratedScene):
    def construct(self):
        loop, els = S2.handover_shot()
        self.add(loop, els)
        self.loop, self.els = loop, els
        # electron look: brightness alpha + pulse scale, applied after the drift step
        self.e_alpha, self.e_pulse = ValueTracker(1.0), ValueTracker(0.0)
        base_w = els[0].width

        def e_style(m):
            a = self.e_alpha.get_value()
            s = 1 + 0.7 * abs(np.sin(PI * self.e_pulse.get_value()))
            for e in m:
                e.scale_to_fit_width(base_w * s)
                e[0].set_fill(opacity=a)
                e[1].set_stroke(opacity=a)
        els.start()
        els.add_updater(e_style)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------------------------------
    def clip1(self):
        loop, els = self.loop, self.els
        L, R, B, Tp = loop.bounds()
        cy = (B + Tp) / 2
        o = 0.45
        Lo, Ro, Bo, To = L - o, R + o, B - o, Tp + o

        which = T("which way?", 40, YELLOW).move_to([0, To + 0.55, 0])
        tag = T("imagined, before\nelectrons were known", 32, GOLD, slant=ITALIC).move_to([0, cy + 0.1, 0])

        pts = [np.array(p, dtype=float) for p in
               ([Lo, cy + 0.55, 0], [Lo, To, 0], [Ro, To, 0], [Ro, Bo, 0], [Lo, Bo, 0], [Lo, cy - 0.55, 0])]
        total = sum(np.linalg.norm(b - a) for a, b in zip(pts[:-1], pts[1:]))
        ghosts = VGroup(*[ghost_charge() for _ in range(18)])
        gfade = ValueTracker(1.0)
        head = [0.0]

        def g_upd(m, dt):
            head[0] += 3.0 * dt
            for i, g in enumerate(m):
                d = head[0] - i * 1.5
                if d < 0 or d > total:
                    op = 0.0
                    d = min(max(d, 0), total)
                else:
                    op = min(1.0, d / 0.5, (total - d) / 0.5)
                g.move_to(polyline_at(pts, d))
                g.set_stroke(opacity=op * gfade.get_value())
        ghosts.set_stroke(opacity=0)
        ghosts.move_to(pts[0])

        S = S2.current_arrow
        self.gold = [S([Lo, cy + 0.6, 0], [Lo, Tp - 0.3, 0]).arrow,          # up out of +
                     S([-1.4, To, 0], [1.4, To, 0]).arrow,                    # right along the top
                     S([Ro, cy + 0.9, 0], [Ro, cy - 0.9, 0]).arrow,           # down the right side
                     S([Lo, B + 0.4, 0], [Lo, cy - 0.65, 0]).arrow]           # up into −
        top_lab = T("Direction of current flow", 36, GOLD).move_to(which)
        conv = VGroup(T("conventional current:", 32, GOLD),
                      MathTex(r"+ \to -", font_size=40, color=GOLD)).arrange(RIGHT, buff=0.25)
        conv.move_to([0, B - 0.45, 0])
        self.top_lab, self.conv = top_lab, conv

        self.blue = Arrow([R - 0.5, cy - 1.0, 0], [R - 0.5, cy + 1.0, 0], buff=0, stroke_width=5,
                          color=BLUE, max_tip_length_to_length_ratio=0.3, tip_length=0.24)
        blue_lab = T("Flow of electrons\nin metal wire connected\nacross a battery", 30, BLUE)
        blue_lab.next_to(self.blue, LEFT, buff=0.35).set_y(cy + 0.05)
        self.blue_lab = blue_lab

        with self.say("c6.current.1") as c:
            self.play(*els.motion(drift=DRIFT, jitter=1), run_time=1.0)
            c.wait_until("which way")
            self.play(*appear(which), run_time=1.0)
            c.wait_until("before electrons were discovered")
            self.add(ghosts)
            ghosts.add_updater(g_upd)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("conv")
            self.play(gfade.animate.set_value(0), *disappear(tag),
                      *during([GrowArrow(a) for a in self.gold], 0.3, 1.0), run_time=1.5)
            ghosts.clear_updaters()
            self.remove(ghosts)
            self.play(*swap(which, top_lab), run_time=1.2)
            c.wait_until("conventional")
            self.play(*appear(conv), run_time=1.0)
            c.wait_until("electrons")
            self.play(self.e_pulse.animate.set_value(2.0), run_time=1.6)
            c.wait_until("opposite")
            self.play(GrowArrow(self.blue), *during(appear(blue_lab), 0.4, 1.0),  # early: p. 165's caption, named by its arrow
                      run_time=1.5)

    # ------------------------------------------------------------------------------------------
    def clip2(self):
        els = self.els
        g_small = S2.current_arrow(UP * 0.55, DOWN * 0.55).arrow
        b_small = Arrow(DOWN * 0.55, UP * 0.55, buff=0, stroke_width=5, color=BLUE,
                        max_tip_length_to_length_ratio=0.3, tip_length=0.24)
        eq_sign = MathTex("=", font_size=56)
        row = VGroup(g_small, eq_sign, b_small).arrange(RIGHT, buff=0.5)
        same = T("same current", 34)
        VGroup(row, same).arrange(DOWN, buff=0.4).move_to(self.blue_lab).set_x(0)

        with self.say("c6.current.2") as c:
            c.wait_until("gold")
            self.play(*[a.animate(rate_func=there_and_back).scale(1.3) for a in self.gold], run_time=1.5)
            c.wait_until("blue")
            self.play(self.blue.animate(rate_func=there_and_back).scale(1.3), run_time=1.5)
            c.wait_until("same")
            self.play(*disappear(self.blue_lab), run_time=0.7)
            self.play(ReplacementTransform(self.gold[2].copy(), g_small),
                      ReplacementTransform(self.blue.copy(), b_small),
                      *during(appear(eq_sign, shift=None), 0.5, 1.0), run_time=1.4)
            c.wait_until("the same current")
            self.play(*appear(same), run_time=0.9)
            c.wait_until("rule")
            self.play(self.e_alpha.animate.set_value(DIMMED), *set_alpha([self.blue, b_small], DIMMED),
                      *set_alpha([g_small, eq_sign, same], 0.4), run_time=1.5)
            c.wait_until("from plus to minus")
            self.play(FlashUnder(self.conv, color=GOLD, run_time=1.5, time_width=1.5), run_time=1.5)

    # ------------------------------------------------------------------------------------------
    def clip3(self):
        els = self.els
        y, r = TUBE_Y, TUBE_R
        tube = VGroup(Line([-7.05, y + r, 0], [7.05, y + r, 0]),
                      Line([-7.05, y - r, 0], [7.05, y - r, 0])).set_stroke(FG, 4)
        disc = DashedVMobject(Ellipse(width=0.5, height=2 * r - 0.04), num_dashes=22).set_stroke(GOLD, 3)
        disc.move_to([0, y, 0])
        disc_fill = Ellipse(width=0.5, height=2 * r - 0.04).set_stroke(width=0).set_fill(GOLD, 0.12)
        disc_fill.move_to(disc)

        rng = np.random.default_rng(3)
        n = 16
        stream = VGroup(*[S2.electron() for _ in range(n)])
        xs = list(rng.uniform(-7.4, 7.4, n))
        ys = rng.uniform(y - r + 0.2, y + r - 0.2, n)
        self.s_speed, self.s_alpha = ValueTracker(1.0), ValueTracker(1.0)

        def place():
            for i, e in enumerate(stream):
                e.move_to([xs[i], ys[i], 0])
                op = float(np.clip((6.9 - abs(xs[i])) / 0.6, 0, 1)) * self.s_alpha.get_value()
                e[0].set_fill(opacity=op)
                e[1].set_stroke(opacity=op)

        def s_upd(m, dt):
            v = self.s_speed.get_value()
            for i in range(n):
                xs[i] += v * dt
                if xs[i] > 7.4:
                    xs[i] -= 14.8
            place()
        place()
        self.stream, self.tube, self.disc = stream, tube, VGroup(disc_fill, disc)

        k = ValueTracker(0.0)
        num = DecimalNumber(0, num_decimal_places=0, group_with_commas=True, font_size=60, color=GOLD)
        num_lab = T("electrons", 36)
        right_x = 0.55

        def n_upd(m):
            m.set_value(round(10 ** k.get_value()) - 1)
            m.move_to([0, 3.0, 0]).align_to([right_x, 0, 0], RIGHT)
        n_upd(num)
        num_lab.next_to([right_x, 3.0, 0], RIGHT, buff=0.25)
        num_lab.align_to(num, DOWN)
        coul = T("coulomb (C)", 36, GOLD).move_to([0, y - r - 0.5, 0])
        self.coul = coul

        big = S2.electron(r=0.42)
        one_tag = MathTex(r"1.6\times10^{-19}\,\text{C}", font_size=56, color=GOLD)
        VGroup(big, one_tag).arrange(RIGHT, buff=0.5).move_to([0, -0.85, 0])
        flip = MathTex(r"1 \div (1.6\times10^{-19}) = 6.25\times10^{18}", font_size=52).move_to([0, -2.0, 0])
        stmt = MathTex(r"1\,\text{C}", r"= 6.25\times10^{18}\ \text{electrons}", font_size=52)
        stmt[0].set_color(GOLD)
        stmt.move_to([0, -3.05, 0])
        self.c3 = (num, num_lab, big, one_tag, flip, stmt)

        with self.say("c6.current.3") as c:
            els.clear_updaters()
            sweep_clear(self, FadeIn(tube), FadeIn(self.disc), FadeIn(stream), run_time=1.6)
            stream.add_updater(s_upd)
            c.wait_until("huge")
            num.add_updater(n_upd)
            self.play(*appear(num, num_lab), run_time=1.0)
            self.play(k.animate.set_value(9.4), self.s_speed.animate.set_value(3.5),
                      run_time=min(5.0, c.until("coulomb") - 0.6), rate_func=linear)
            num.clear_updaters()
            c.wait_until(own_word=coul)
            self.play(*appear(coul), run_time=0.9)
            c.wait_until("one")
            src = min(stream, key=lambda e: abs(e.get_x() + 2))
            self.play(self.s_alpha.animate.set_value(0.3), *set_alpha([num, num_lab], 0.4),
                      GrowFromPoint(big, src.get_center()), run_time=1.5)
            c.wait_until("one point six")
            self.play(*appear(one_tag), run_time=1.0)
            c.wait_until("flip")
            self.play(FlashAround(one_tag, color=GOLD, run_time=1.5, time_width=1.5),
                      *during(appear(flip), 0.35, 1.0), run_time=1.5)
            c.wait_until("one coulomb is")
            self.play(*appear(stmt), run_time=1.0)

    # ------------------------------------------------------------------------------------------
    def clip4(self):
        num, num_lab, big, one_tag, flip, stmt = self.c3
        y, r = TUBE_Y, TUBE_R
        watch = stopwatch().move_to([2.4, 3.0, 0])
        bundle = VGroup(RoundedRectangle(corner_radius=0.2, width=1.5, height=0.85)
                        .set_stroke(GOLD, 3).set_fill("#3A2D1E", 1),
                        T("1 C", 36, GOLD)).move_to([-5.2, y, 0]).set_z_index(2)
        amp = T("1 C per second = 1 Ampere (A)", 42, t2c={"1 Ampere (A)": GOLD}).move_to([0, -0.85, 0])

        f = i_eq_qt(120).move_to([0, 0.15, 0])
        tags = [T("current (A)", 32, GOLD), T("charge (C)", 32), T("time (s)", 32)]
        letters = [f[0], f[2], f[4]]
        for tg, x in zip(tags, (-3.6, 0.0, 3.6)):
            tg.move_to([f.get_x() + x, -1.75, 0])
        leads = [Line(lt.get_bottom() + DOWN * 0.15, tg.get_top() + UP * 0.12).set_stroke(DIM, 2)
                 for lt, tg in zip(letters, tags)]
        rate = T("current is the rate of flow of charge", 40).move_to([0, -3.0, 0])
        milli1 = MathTex(r"1\,\text{mA}", r"= 10^{-3}\,\text{C/s}", font_size=52).move_to([0, 3.05, 0])
        milli1[0].set_color(GOLD)
        milli2 = MathTex(r"= 6.25\times10^{15}\ \text{electrons per second}", font_size=44)
        milli2.next_to(milli1, DOWN, buff=0.3)
        milli2.align_to(milli1[1], LEFT)
        VGroup(milli1, milli2).set_x(0)

        with self.say("c6.current.4", gap=3.0) as c:
            self.play(*disappear(num, num_lab, big, one_tag), self.s_alpha.animate.set_value(1.0),
                      *during(appear(watch, shift=None), 0.4, 1.0), run_time=1.0)
            self.play(FadeIn(bundle), run_time=0.4)
            self.play(bundle.animate.move_to([5.2, y, 0]),
                      Rotate(watch.hand, angle=-TAU, about_point=watch.face.get_center()),
                      run_time=2.6, rate_func=linear)
            c.wait_until("the current is one amp")
            self.play(*appear(amp), run_time=1.0)
            c.wait_until("formula")
            self.stream.clear_updaters()
            self.play(*[FadeOut(m) for m in self.mobjects if m is not amp], run_time=0.9)
            self.play(*during([amp.animate.scale(0.8).move_to([0, 3.05, 0])], 0, 0.55),
                      *during([FadeIn(f)], 0.55, 1.0), run_time=1.6)
            self.play(Create(leads[0]), *appear(tags[0]), run_time=0.9)
            c.wait_until("charge")
            self.play(Create(leads[1]), *appear(tags[1]), run_time=0.9)
            c.wait_until("time")
            self.play(Create(leads[2]), *appear(tags[2]), run_time=0.9)
            c.wait_until("rate")
            self.play(*appear(rate), run_time=1.0)
            c.wait_until("milli")
            self.play(*swap(amp, milli1), run_time=1.2)
            c.wait_until("a thousandth")
            self.play(*appear(milli2), run_time=1.0)
