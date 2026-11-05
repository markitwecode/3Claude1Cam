"""Chapter 1, scene 1: the hook (pendulum and spring in step; wide and narrow swings keep the beat; title). Clips c1.hook.1 – c1.hook.2."""
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
from lib.titles import title_card  # noqa: E402

kit = load_scene("ch1_s2_tools")
grav = load_scene("ch1_s5_gravity")
spr = load_scene("ch1_s3_spring")

OMEGA = 3.13                 # rad/s: sqrt(9.81) for a 1 m pendulum
HALF = PI / OMEGA            # one swing across, ≈ 1.004 s
PIV_Y = 2.4
ROD = grav.ROD_L             # 2.75
P1_START_X, P1_X, P2_X = -3.4, -4.8, 4.8
READ_Y = -1.05

# spring: s3's drawing, scaled about its rest point and moved to centre-right
SPR_Y = -0.75
SPR_SCALE = 0.85
SPR_REST_TO = 2.9            # where the block's rest point lands
SPR_AMP = 3.0                # cm


def handover_shot():
    """The last frame (s2 opens on it): the chapter's corner tag alone."""
    return kit.corner_tag()


def _faded(mob, a):
    if a >= 0.999:
        return mob
    for m in mob.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * a)
        m.set_fill(opacity=m.get_fill_opacity() * a)
    return mob


def _spring(x):
    g = spr.spring_drawing(x, y=SPR_Y, zero=False)
    g.scale(SPR_SCALE, about_point=np.array([spr.SPRING_REST_X, SPR_Y, 0]))
    g.shift((SPR_REST_TO - spr.SPRING_REST_X) * RIGHT)
    return g


def _pendulum_icon():
    g = grav.pendulum(22, labels=False, angle=False, pivot=ORIGIN)
    g.remove(g.vert)
    g.set_color(DIM)
    g.scale(0.32)
    return g


def _ac_icon():
    ring = Circle(radius=0.4).set_stroke(DIM, 3)
    s = MathTex(r"\sim", font_size=60, color=DIM).move_to(ring)
    return VGroup(ring, s)


def _wave_icon():
    w = FunctionGraph(lambda x: 0.16 * np.sin(TAU * x / 0.7), x_range=[-0.7, 0.7]).set_stroke(DIM, 3)
    w2 = w.copy().shift(0.28 * DOWN).set_stroke(DIM, 2, opacity=0.6)
    return VGroup(w, w2)


class Hook(NarratedScene):
    def construct(self):
        self.tt = ValueTracker(0.0)
        self.tt.add_updater(lambda m, dt: m.increment_value(dt))
        self.add(self.tt)
        self.op1, self.op2, self.ops, self.opc = (ValueTracker(0.0) for _ in range(4))
        self.px1 = ValueTracker(P1_START_X)
        self.amp1 = ValueTracker(12.0)
        self.amp2 = ValueTracker(5.0)
        self._counts = {}
        self.hook1()
        self.hook2()

    # ── live pictures ───────────────────────────────────────────────────────────
    def _theta(self, amp):
        return amp * np.cos(OMEGA * self.tt.get_value())

    def _count(self):
        n = int(self.tt.get_value() // HALF)
        if n not in self._counts:
            self._counts[n] = T(f"{n} s", size=40).move_to([0, 3.35, 0])
        return self._counts[n].copy()

    def _live(self):
        tt = self.tt
        p1 = always_redraw(lambda: _faded(grav.pendulum(
            self._theta(self.amp1.get_value()), labels=False, angle=False,
            pivot=np.array([self.px1.get_value(), PIV_Y, 0]), length=ROD), self.op1.get_value()))
        p2 = always_redraw(lambda: _faded(grav.pendulum(
            self._theta(self.amp2.get_value()), labels=False, angle=False,
            pivot=np.array([P2_X, PIV_Y, 0]), length=ROD), self.op2.get_value()))
        sp = always_redraw(lambda: _faded(
            _spring(-SPR_AMP * np.cos(OMEGA * tt.get_value())), self.ops.get_value()))
        cnt = always_redraw(lambda: _faded(self._count(), self.opc.get_value()))
        return p1, p2, sp, cnt

    # ── c1.hook.1 ───────────────────────────────────────────────────────────────
    def hook1(self):
        with self.say("c1.hook.1") as c:
            self.tt.set_value(0.0)
            self.p1, self.p2, self.sp, self.cnt = self._live()
            self.add(self.sp, self.p1, self.p2, self.cnt)
            self.play(self.op1.animate.set_value(1), self.ops.animate.set_value(1),
                      self.opc.animate.set_value(1), run_time=1.5)

            c.wait_until("second")
            self.play(FlashAround(self.cnt, run_time=1.5, time_width=1.5))
            c.wait_until("swing back")
            self.play(FlashAround(self.cnt, run_time=1.5, time_width=1.5))

            c.wait_until("twins")
            self.play(*during([self.ops.animate.set_value(0)], 0, 0.5),
                      self.px1.animate.set_value(P1_X),
                      *during([self.op2.animate.set_value(1)], 0.45, 1),
                      run_time=min(2.0, c.until("wide swing")))
            self.r1 = T("15°", size=34, color=YELLOW).move_to([P1_X, READ_Y, 0])
            self.r2 = T("5°", size=34, color=YELLOW).move_to([P2_X, READ_Y, 0])
            self.remove(self.sp)
            c.wait_until("wide swing")
            self.play(self.amp1.animate.set_value(15.0), *appear(self.r1), run_time=1.2)
            c.wait_until("narrow one")
            self.play(*appear(self.r2), run_time=1.0)

            c.wait_until("lag")
            self.q = T("?", size=60, color=DIM).move_to([P1_X, PIV_Y + 0.75, 0])
            self.play(*appear(self.q), run_time=1.0)

            c.wait_until("beat")
            self.ok = check_mark().move_to(self.q)
            self.play(*swap(self.q, self.ok), run_time=1.0)
            self.play(FlashAround(self.cnt, run_time=1.5, time_width=1.5))

    # ── c1.hook.2 ───────────────────────────────────────────────────────────────
    def hook2(self):
        with self.say("c1.hook.2") as c:
            q1 = T("What rule makes it swing?", size=44, color=YELLOW).move_to([0, 1.15, 0])
            q2 = T("What sets the beat?", size=44, color=YELLOW).move_to([0, 0.35, 0])
            self.play(*appear(q1), *disappear(self.ok), run_time=1.0)
            c.wait_until("what sets the beat")
            self.play(*appear(q2), run_time=1.0)

            c.wait_until("title")
            card = title_card("Part 1 · The rule behind every swing")
            self.play(self.opc.animate.set_value(0),
                      q1.animate.scale(34 / 44).move_to([0, 3.05, 0]),
                      q2.animate.scale(34 / 44).move_to([0, 2.5, 0]),
                      *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.4, 1),
                      run_time=1.4)  # early: title card
            self.remove(self.cnt)
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.2)  # early: title card

            # the things that swing, along the bottom
            ic_y, w_y = -2.4, -3.05
            icons = [_pendulum_icon(), _ac_icon(), _wave_icon()]
            words = ["pendulums", "alternating currents", "waves"]
            xs = [-4.6, -1.3, 1.7]
            items = []
            for ic, w, x in zip(icons, words, xs):
                ic.move_to([x, ic_y, 0])
                lab = T(w, size=28, color=DIM).move_to([x, w_y, 0])
                items.append(VGroup(ic, lab))
            arrow_c = np.array([3.1, ic_y, 0])
            pivot_dot = Dot(arrow_c, radius=0.05, color=GOLD)
            garrow = Arrow(arrow_c, arrow_c + 0.55 * RIGHT, buff=0, stroke_width=5,
                           max_tip_length_to_length_ratio=0.35, color=GOLD)
            ref = kit.tag("reference").move_to([4.0, ic_y + 0.2, 0], aligned_edge=LEFT)
            notes = kit.tag("§2.6 · notes p. 108").move_to([4.0, ic_y - 0.25, 0], aligned_edge=LEFT)
            nxt = T("their equations: next term", size=28, color=DIM).move_to([xs[1], -3.5, 0])

            c.wait_until("things")
            self.play(*appear(items[0]), run_time=1.0)
            c.wait_until("alternating currents")
            self.play(*appear(items[1]), run_time=1.0)
            c.wait_until("waves")
            self.play(*appear(items[2]), run_time=1.0)
            self.play(*appear(ref, notes, lag=0.3), run_time=1.0)  # early: notes tags, not read aloud

            c.wait_until("complex")
            self.play(FadeIn(pivot_dot, garrow), run_time=0.6)
            self.play(Rotate(garrow, angle=TAU, about_point=arrow_c), run_time=1.6,
                      rate_func=linear)

            c.wait_until("next_term")
            self.play(*disappear(card, q1, q2), *during(appear(nxt), 0.4, 1), run_time=1.4)

            c.wait_until("beyond")
            tagc = handover_shot()
            self.play(*disappear(*items, pivot_dot, garrow, ref, notes), run_time=1.0)
            self.play(*appear(tagc, shift=None), run_time=1.0)

            c.wait_until("here you build it")
            self.play(*disappear(self.r1, self.r2, nxt),
                      self.op1.animate.set_value(0), self.op2.animate.set_value(0),
                      run_time=min(1.5, c.until(floor=0.6)))
            self.remove(self.p1, self.p2)
            self.tt.clear_updaters()
            self.remove(self.tt)
        self.wait(1.0)
