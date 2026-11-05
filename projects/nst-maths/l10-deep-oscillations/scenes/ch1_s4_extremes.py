"""Chapter 1, scene 4: reading the rule at the extremes (numbers in, the swing, middle vs end). Clips c1.ends.1 – c1.ends.4.

Opens on s3's handover shot; ends on s5's opening shot (legend + corner tag).
Units: the brief's metres on s3's spring drawing: drawing x (s3's "cm") = 8 × metres, so ±0.5 m
is ±4 drawing units (±2 scene units); DIM ticks "−0.5 m" / "0.5 m" are added under the table.
"""
# style: 2
# handover: next
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
s3 = load_scene("ch1_s3_spring")
s5 = load_scene("ch1_s5_gravity")

PER_M = 8.0                  # s3 drawing units per metre
OMEGA = 2.0                  # rad/s
AMP = 0.5                    # m
V_LEN = 1.6                  # GREEN arrow length per m/s
V_DY = s3.BLOCK_H + s3.PULL_DY + 0.42   # velocity arrow height above the table
READ_Y = 2.55
TICK_Y = s3.SPRING_Y - 0.52
LAB_Y = -0.62


def handover_shot():
    """Last frame = s5's first: the six-entry legend and the corner tag."""
    return s5.opening_shot()


def _clean(v):
    return 0.0 if abs(v) < 0.005 else v


def _mtex(*parts, colors=None, size=kit.COL_SIZE):
    m = MathTex(*parts, font_size=size)
    for i, col in (colors or {}).items():
        m[i].set_color(col)
    return m


class Extremes(NarratedScene):
    def construct(self):
        hs = s3.handover_shot()
        self.add(*hs)
        self.R, self.leg, self.ctag = hs.rule, hs.legend, hs.tag

        self.ph = ValueTracker(0.0)     # phase
        self.A = ValueTracker(0.0)      # amplitude (m)
        self.pl = ValueTracker(0.0)     # RED arrow scale
        self.vl = ValueTracker(0.0)     # GREEN arrow scale
        self.add(self.ph)

        def xm():
            return self.A.get_value() * np.cos(self.ph.get_value())

        def vm():
            return -OMEGA * self.A.get_value() * np.sin(self.ph.get_value())

        self.xm, self.vm = xm, vm
        y = s3.SPRING_Y
        self.live = always_redraw(lambda: s3.spring_drawing(PER_M * xm(), y))
        self.xarr = always_redraw(lambda: s3.stretch_arrow(PER_M * xm(), y))
        self.parr = always_redraw(lambda: s3.pull_arrow(PER_M * xm(), y,
                                                        per_cm=s3.PULL_PER_CM * self.pl.get_value()))

        def varrow():
            cx = s3.block_center(PER_M * xm(), y)[0]
            return s3._harrow(cx, cx + V_LEN * self.vl.get_value() * vm(), y + V_DY, GREEN)

        self.varr = always_redraw(varrow)
        self.remove(*hs.spring.get_family())
        self.add(self.live, self.xarr, self.parr, self.varr)

        self.c1_numbers()
        self.c2_middle()
        self.c3_end()
        self.c4_never()

    # ── helpers ───────────────────────────────────────────────────────────────────
    def run(self, dph, **kw):
        """Advance the swing by dph radians at the true rate (ω = 2 /s), linearly."""
        return self.ph.animate(rate_func=linear, run_time=dph / OMEGA, **kw).increment_value(dph)

    def go(self, m, dt):
        m.increment_value(OMEGA * dt)

    def xdd_readout(self):
        r = s3._readout(r"\ddot{x}", RED, r"\mathrm{m/s^2}", lambda: _clean(-OMEGA ** 2 * self.xm()), size=32)
        r.move_to([-3.35, READ_Y, 0], aligned_edge=LEFT)
        return r

    # ── c1.ends.1 ─────────────────────────────────────────────────────────────────
    def c1_numbers(self):
        R = self.R
        with self.say("c1.ends.1") as c:
            tgt = R.copy()
            kit.col_place(tgt, 0)
            self.play(R.animate.move_to(tgt), run_time=1.5)

            w2 = _mtex(r"\omega^2", "=", "4")
            kit.col_place(w2, 1)
            xh = _mtex("x", "=", r"0.5\ \mathrm{m}", colors={0: BLUE})
            xh.next_to(w2, RIGHT, buff=0.7)
            xh.shift((w2[1].get_center()[1] - xh[1].get_center()[1]) * UP)
            c.wait_until("omega squared")
            self.play(*appear(w2, shift=None), run_time=1.0)

            ticks = VGroup()
            for xv, s in ((-AMP, r"-0.5\,\mathrm{m}"), (AMP, r"0.5\,\mathrm{m}")):
                px = s3.block_center(PER_M * xv)[0]
                tk = Line([px, y0 := s3.SPRING_Y - 0.14, 0], [px, s3.SPRING_Y, 0]).set_stroke(DIM, 3)
                lb = MathTex(s, font_size=30, color=DIM).move_to([px, TICK_Y, 0])
                ticks.add(tk, lb)
            self.ticks = ticks
            c.wait_until("half a metre")
            self.play(self.A.animate.set_value(AMP), *appear(xh, shift=None),
                      FadeIn(ticks), run_time=1.8)

            st2 = kit.step_label("put the numbers in", 2)
            L2 = _mtex(r"\ddot{x}", "=", r"-4", r"\times", "0.5", colors={0: RED, 4: BLUE})
            kit.col_place(L2, 2)
            c.wait_until("minus four")
            self.play(*appear(st2, L2, shift=None, lag=0.3), run_time=1.4)

            st3 = kit.step_label("multiply", 3)
            L3 = _mtex(r"\ddot{x}", "=", r"-2\ \mathrm{m/s^2}", colors={0: RED, 2: RED})
            kit.col_place(L3, 3)
            c.wait_until("two metres")
            self.play(*appear(st3, L3, shift=None, lag=0.3), run_time=1.4)

            c.wait_until("back toward")
            self.play(self.pl.animate.set_value(1.0), run_time=1.5)
            self.nums = [w2, xh, st2, L2, st3, L3]

            # the swing
            self.xread = s3._readout("x", BLUE, r"\mathrm{m}", lambda: _clean(self.xm()), size=32)
            self.xread.move_to([-6.0, READ_Y, 0], aligned_edge=LEFT)
            self.aread = self.xdd_readout()
            c.wait_until("swing")
            self.vl.set_value(1.0)
            self.play(*set_alpha(self.nums, 0.4), *appear(self.xread, self.aread, shift=None, lag=0.2),
                      run_time=1.0)
            d = c.until() - 0.15
            k = max(0, round((OMEGA * d - 1.5 * PI) / TAU))
            dph = TAU * k + 1.5 * PI          # land crossing 0, moving right
            self.play(self.ph.animate(rate_func=linear).increment_value(dph), run_time=d)

    # ── c1.ends.2 ─────────────────────────────────────────────────────────────────
    def c2_middle(self):
        with self.say("c1.ends.2") as c:
            c.wait_until("ex is zero")
            self.play(FlashAround(self.xread, color=BLUE, time_width=1.5), run_time=1.3)

            nop = T("no pull", size=30)
            fast = T("· fastest", size=30, color=GREEN)
            VGroup(nop, fast).arrange(RIGHT, buff=0.18).move_to([s3.SPRING_REST_X, LAB_Y, 0])
            c.wait_until("no pull")
            self.play(*appear(nop), FlashAround(self.aread, color=RED, time_width=1.5), run_time=1.3)
            c.wait_until("fastest")
            self.play(*appear(fast), FlashAround(self.varr, color=GREEN, time_width=1.5), run_time=1.3)

            c.wait_until("coast")
            ghost = s3.spring_drawing(0.0).block.copy().set_stroke(DIM, 2, opacity=0.6).set_fill(DIM, 0.15)
            self.ghost = ghost
            ghost.set_z_index(-1)
            self.labs2 = [nop, fast]
            self.ph.add_updater(self.go)
            self.play(FadeIn(ghost), run_time=0.8)

    # ── c1.ends.3 ─────────────────────────────────────────────────────────────────
    def c3_end(self):
        R = self.R
        with self.say("c1.ends.3") as c:
            self.ph.clear_updaters()
            p = self.ph.get_value()
            n = np.ceil((p + 2.0) / TAU)
            dph = n * TAU - p
            self.aread[2].clear_updaters()
            self.play(self.ph.animate(rate_func=linear).increment_value(dph),
                      *during(disappear(*self.nums, *self.labs2, self.ghost, self.aread), 0, 0.4),
                      *during([self.pl.animate.set_value(0.0)], 0, 0.3),
                      run_time=dph / OMEGA)
            q = _mtex(r"\ddot{x}", "=", "?", colors={0: RED, 2: RED}, size=32)
            q.move_to(self.aread[0].get_left(), aligned_edge=LEFT)
            q.shift((self.aread[1].get_center()[1] - q[1].get_center()[1]) * UP)
            q[2].move_to([self.aread[2].get_center()[0], q[2].get_center()[1], 0])
            self.play(*appear(q, shift=None), run_time=0.8)

            box = kit.think_box("At the very end of its swing\nthe weight is still for an instant.\n"
                                "Is its acceleration zero there too?", size=30)
            ring = kit.think_ring()
            c.wait_until("stop")
            self.play(*appear(box, shift=None), FadeIn(ring), run_time=1.2)  # early: the think-stop question is read over the next 8 s
            self.play(kit.drain(ring, run_time=max(1.0, c.until("answer") - 0.2)))
            c.wait_until("answer")

            wrong = _mtex(r"\text{still}", r"\;\Rightarrow\;", r"\text{no acceleration}")
            kit.col_place(wrong, 1)
            self.play(*disappear(box, ring), run_time=0.8)
            self.play(*appear(wrong, shift=None), run_time=1.0)

            c.wait_until("only looks at")
            self.play(FlashAround(R.line[3], color=BLUE, time_width=1.5),
                      FlashAround(self.xarr, color=BLUE, time_width=1.5), run_time=1.4)
            c.wait_until("as far out")
            self.play(FlashAround(self.xread, color=BLUE, time_width=1.5), run_time=1.3)

            largest = T("the largest", size=30, color=RED)
            cx = s3.block_center(PER_M * AMP)[0]
            largest.move_to([cx - 0.4 * PER_M * AMP / 2, s3.SPRING_Y + V_DY, 0])
            aread = self.xdd_readout()
            c.wait_until("largest")
            self.play(self.pl.animate.set_value(1.0), *swap(q, aread), *appear(largest), run_time=1.6)
            self.aread = aread

            ans = _mtex(r"\ddot{x}", "=", r"-4", r"\times", "0.5", "=", r"-2\ \mathrm{m/s^2}",
                        colors={0: RED, 4: BLUE, 6: RED})
            kit.col_place(ans, 2)
            c.wait_until("minus four")
            self.play(*appear(ans, shift=None), run_time=1.4)
            self.ans, self.largest = ans, largest

            strike = Line(wrong.get_left() + 0.1 * LEFT, wrong.get_right() + 0.1 * RIGHT).set_stroke(RED, 4)
            x_mark = cross_mark().next_to(wrong, RIGHT, buff=0.3)
            c.wait_until("still")
            self.play(Create(strike), run_time=0.9)
            self.play(FadeIn(x_mark, scale=0.6), *set_alpha([wrong], 0.6), run_time=0.8)
            self.wrong = VGroup(wrong, strike, x_mark)

    # ── c1.ends.4 ─────────────────────────────────────────────────────────────────
    def c4_never(self):
        with self.say("c1.ends.4") as c:
            self.ph.add_updater(self.go)
            self.play(*disappear(self.largest), run_time=0.8)

            over = T("overshoots", size=28, color=DIM).move_to([s3.SPRING_REST_X, LAB_Y, 0])
            tb = [T("turns back", size=28, color=DIM).move_to([s3.block_center(PER_M * xv)[0] + 0.45 * np.sign(xv),
                                                               LAB_Y, 0])
                  for xv in (-AMP, AMP)]
            c.wait_until("too fast")
            self.play(*appear(over), run_time=1.0)  # early: names what the voice describes ("too fast to stop")
            self.play(FlashAround(over, color=DIM, time_width=1.5), run_time=1.0)
            c.wait_until("each end")
            self.play(*appear(*tb, lag=0.3), run_time=1.2)  # early: names what the voice describes ("each end it stops")
            self.play(*flash(tb, color=DIM), run_time=1.0)
            self.labels = [over, *tb]

        final = handover_shot()
        self.xread[2].clear_updaters()
        self.aread[2].clear_updaters()
        self.play(*disappear(self.live, self.xarr, self.parr, self.varr, self.xread, self.aread,
                             self.ticks, self.R, *self.wrong, self.ans, *self.labels), run_time=1.2)
        self.ph.clear_updaters()
        self.remove(*self.leg.get_family(), *self.ctag.get_family(), self.ph)
        self.add(final)
        self.wait(1.0)
