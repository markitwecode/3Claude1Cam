"""Chapter 2, scene 1: the spring's wave, which function is it? Title, three retrieval cards. Clips c2.hook.1 – c2.hook.2.

Shared with later ch2 scenes (load_scene("ch2_s1_hook")):
  opening_card()                 ch2's first frame: ch1 s3's spring drawing alone, block at its right end
                                 (x = 2.6 cm = 1.3 units), table at TABLE_Y, rest point SPRING_REST_X
  rule_pin()                     the chapter's pinned rule ẍ = −ω²x (kit.pinned, label "the rule")
  block_x(t)                     the block's displacement in cm at scene time t: 2.6 cos 2t
  hook_wave(origin, t_end, t_start=0)
                                 the BLUE wave x = 1.3 cos 2t on its side: the point for time t sits at
                                 (origin_x + 1.3 cos 2t, origin_y − WAVE_SEC·(t − t_start)), time running down
  WAVE_SEC, WAVE_AMP, OMEGA, WAVE_ORIGIN, AXIS_BOTTOM, TABLE_Y
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
from lib.titles import title_card  # noqa: E402

kit = load_scene("ch1_s2_tools")
spr = load_scene("ch1_s3_spring")
grav = load_scene("ch1_s5_gravity")

# ═══════════════════════════════ shared with ch2 ═══════════════════════════════
TABLE_Y = 2.0                       # the spring's table line
OMEGA = 2.0                         # rad/s
AMP_CM = 2.6                        # let go from rest at x = 2.6 cm
WAVE_AMP = AMP_CM * spr.SPRING_UNIT  # 1.3 scene units = ch2's unit-circle radius
WAVE_SEC = 0.45                     # time-axis scene units per second (downward)
WAVE_ORIGIN = np.array([spr.SPRING_REST_X, 1.25, 0])   # top of the time axis, under the rest point
AXIS_BOTTOM = -0.9                  # foot of the time axis (the legend sits below)


def block_x(t):
    """The block's displacement (cm) at time t (s): released from rest at the right end."""
    return AMP_CM * np.cos(OMEGA * t)


def opening_card():
    """ch2's first frame (and ch1's last): the spring drawing alone, block at rest at x = 2.6 cm."""
    return spr.spring_drawing(x=AMP_CM, y=TABLE_Y)


def rule_pin():
    """The chapter's pinned rule ẍ = −ω²x (ẍ RED, x BLUE, ω FG), DIM label "the rule". .formula .label"""
    p = kit.pinned([r"\ddot{x}", "=", r"-\omega^2", "x"], label="the rule")
    p.formula[0].set_color(RED)
    p.formula[3].set_color(BLUE)
    return p


def hook_wave(origin, t_end, t_start=0.0, color=BLUE, width=4):
    """The wave x = 1.3 cos 2t on its side, for t in [t_start, t_end]: time runs down from `origin`
    (the axis point for t_start) at WAVE_SEC units per second; x to the right."""
    if t_end - t_start < 0.02:
        return VMobject()
    ts = np.linspace(t_start, t_end, max(3, int((t_end - t_start) / 0.02) + 1))
    pts = [[origin[0] + WAVE_AMP * np.cos(OMEGA * t), origin[1] - WAVE_SEC * (t - t_start), 0] for t in ts]
    return VMobject().set_points_as_corners(pts).set_stroke(color, width)


# ═══════════════════════════════ scene helpers ═══════════════════════════════
E_X_SHORT = (r"x", BLUE, "displacement")
E_OM = (r"\omega", FG, "angular frequency, rad/s")
E_T = (r"t", FG, "time")
ENTRIES = [E_X_SHORT, kit.E_XD, kit.E_XDD, E_OM, E_T]

AXIS_LEN = WAVE_ORIGIN[1] - AXIS_BOTTOM
WINDOW = AXIS_LEN / WAVE_SEC         # seconds of wave on the axis at once
RIGHT_X = 2.9                        # centre of the right-hand area (caption, question, title)

CARD_W, CARD_H, CARD_Y = 2.45, 3.4, -0.5
CARD_XS = [-0.075, 2.625, 5.325]
PIC_Y = 0.35
TXT_Y = [-0.95, -1.5, -1.95]


def _fade(m, op):
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=sm.get_stroke_opacity() * op)
        sm.set_fill(opacity=sm.get_fill_opacity() * op)
    return m


def _card_frame(x):
    return RoundedRectangle(corner_radius=0.12, width=CARD_W, height=CARD_H).set_stroke(DIM, 1.5) \
        .set_fill(kit.CARD_FILL, 1).move_to([x, CARD_Y, 0])


def _pendulum_pic(x):
    th = 20
    P = np.array([x, 1.0, 0])
    p = grav.pendulum(th, labels=False, angle=False, pivot=P, length=1.35)
    u = np.array([-np.sin(th * DEGREES), -np.cos(th * DEGREES), 0])
    n = np.array([np.cos(th * DEGREES), -np.sin(th * DEGREES), 0])
    L = MathTex("L", font_size=32).move_to(P + 0.62 * 1.35 * u + 0.3 * n)
    return VGroup(p, L)


def _plane_pic(x):
    o = np.array([x + 0.25, PIC_Y - 0.45, 0])
    ax = VGroup(Line(o + LEFT * 1.0, o + RIGHT * 0.95), Line(o + DOWN * 0.3, o + UP * 1.15)).set_stroke(DIM, 2)
    d = 1.0 * np.array([np.cos(30 * DEGREES), np.sin(30 * DEGREES), 0])
    arr = Arrow(o, o + d, buff=0, stroke_width=5, tip_length=0.2,
                max_tip_length_to_length_ratio=0.3, color=GOLD)
    g = VGroup(ax, arr)
    g.o, g.arrow = o, arr
    return g


def _right_angle(o, s=0.18):
    u1 = np.array([np.cos(30 * DEGREES), np.sin(30 * DEGREES), 0])
    u2 = np.array([np.cos(120 * DEGREES), np.sin(120 * DEGREES), 0])
    return VMobject().set_points_as_corners([o + s * u1, o + s * (u1 + u2), o + s * u2]).set_stroke(YELLOW, 3)


def _graph_pic(x):
    o = np.array([x - 0.95, PIC_Y, 0])
    ax = VGroup(Line(o, o + RIGHT * 1.95), Line(o + DOWN * 0.7, o + UP * 0.7)).set_stroke(DIM, 2)
    ts = np.linspace(0, 2.1, 80)
    curve = VMobject().set_points_as_corners(
        [o + RIGHT * (t * 1.85 / 2.1) + UP * 0.55 * np.cos(3 * t) for t in ts]).set_stroke(BLUE, 3)
    tl = MathTex("t", font_size=26, color=DIM).next_to(o + RIGHT * 1.95, DOWN, buff=0.1)
    return VGroup(ax, curve, tl)


class Hook(NarratedScene):
    def construct(self):
        self.t0 = self.time
        self.op = ValueTracker(1.0)
        self.spring = opening_card()
        self.add(self.spring)
        self.spring.add_updater(lambda m: m.become(_fade(
            spr.spring_drawing(x=block_x(self.time - self.t0), y=TABLE_Y), self.op.get_value())))
        self.c1()
        self.c2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def tau(self):
        return self.time - self.t0

    # ── the wave being drawn (pen tied to the block) ──
    def wave_now(self):
        t = self.tau()
        t_start = max(self.tw0, t - WINDOW)
        o = WAVE_ORIGIN.copy()
        op = self.op.get_value()
        curve = hook_wave(o, t, t_start)
        y = o[1] - WAVE_SEC * (t - t_start)
        xp = o[0] + WAVE_AMP * np.cos(OMEGA * t)
        pen = Dot([xp, y, 0], radius=0.075, color=BLUE)
        if o[1] - y > 0.12:
            tie = DashedLine([xp, o[1], 0], [xp, y, 0], dash_length=0.08).set_stroke(DIM, 2)
        else:
            tie = VMobject()
        return _fade(VGroup(tie, curve, pen), op)

    def c1(self):
        with self.say("c2.hook.1") as c:
            c.wait_until("wave")
            axis = Arrow(WAVE_ORIGIN, [WAVE_ORIGIN[0], AXIS_BOTTOM, 0], buff=0, stroke_width=3,
                         tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=DIM)
            tlab = MathTex("t", font_size=32, color=DIM).next_to(axis.get_end(), DOWN, buff=0.08)
            self.axis, self.tlab = axis, tlab
            self.play(*appear(axis, tlab, shift=None), run_time=1.0)
            self.tw0 = self.tau()
            self.wave = always_redraw(self.wave_now)
            self.add(self.wave)
            c.wait_until("rule")

            self.legend = kit.legend(ENTRIES)
            self.play(*appear(self.legend, shift=None), run_time=1.2)
            c.wait_until("ex double dot")
            cap = spr.rule_line().scale(56 / kit.COL_SIZE).move_to([RIGHT_X, 1.3, 0])
            self.play(*appear(cap), run_time=min(1.5, c.until("question")))
            c.wait_until("question")

            pin = rule_pin()
            self.pin = pin
            self.play(ReplacementTransform(cap, pin.formula, path_arc=0.7), run_time=1.5)
            self.play(*appear(pin.label, shift=None),
                      *appear(q := MathTex(r"x(t)", r"=\,?", font_size=60, color=YELLOW)
                              .move_to([RIGHT_X, 1.0, 0])), run_time=1.0)
            self.q = q
            c.wait_until("which function")
            sub = VGroup(T("comes back as −ω² × itself", size=30),
                         T("after two derivatives", size=30)).arrange(DOWN, buff=0.16)
            sub.next_to(q, DOWN, buff=0.45)
            self.sub = sub
            self.play(*appear(sub), run_time=1.0)

    def c2(self):
        with self.say("c2.hook.2", gap=0.35) as c:
            card = title_card("Part 2 · Shadows of a turning arrow")
            card.move_to([2.35, 0.1, 0])
            self.play(*during(disappear(self.q, self.sub), 0, 0.45),
                      self.op.animate.set_value(0.4),
                      *set_alpha([self.axis, self.tlab], 0.4),
                      *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.5, 1),
                      run_time=1.6)
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.2)  # early: title card
            c.wait_until("quiz")

            frames = [_card_frame(x) for x in CARD_XS]
            self.play(*during(disappear(card.title, card.rule, card.course, card.part), 0, 0.45),
                      *during(appear(*frames, shift=None, lag=0.2), 0.5, 1), run_time=1.6)

            # q1: the pendulum
            c.wait_until("q1")
            x1 = CARD_XS[0]
            pend = _pendulum_pic(x1)
            self.play(*appear(pend, shift=None), run_time=1.0)
            q1 = MathTex(r"\omega^2", r"=", r"\,?", font_size=36).move_to([x1, TXT_Y[0] - 0.15, 0])
            c.wait_until("omega squared")
            self.play(*appear(q1), run_time=0.8)
            c.wait_until("a1")
            a1 = MathTex(r"\omega^2", r"=", r"g/L", font_size=36).move_to(q1)
            self.play(*edit(q1, a1), run_time=1.2)

            # q2: × i
            c.wait_until("q2")
            x2 = CARD_XS[1]
            plane = _plane_pic(x2)
            self.play(*appear(plane, shift=None), run_time=1.0)
            q2 = MathTex(r"\times\,", "i", r"\ ?", font_size=40).move_to([x2, TXT_Y[0], 0])
            q2[1].set_color(PINK)
            c.wait_until("multiplying")
            self.play(*appear(q2), run_time=0.8)
            c.wait_until("a2")
            turned = plane.arrow.copy()
            self.add(turned)
            self.play(Rotate(turned, angle=PI / 2, about_point=plane.o), run_time=1.5)
            a2 = MathTex(r"\times\,", "i", font_size=40).move_to(q2)
            a2[1].set_color(PINK)
            same = T("same length", size=24).move_to([x2, TXT_Y[1], 0])
            self.play(*edit(q2, a2), FadeIn(rmark := _right_angle(plane.o)), *appear(same), run_time=1.2)

            # q3: the chain rule
            c.wait_until("q3")
            x3 = CARD_XS[2]
            graph = _graph_pic(x3)
            self.play(*appear(graph, shift=None), run_time=1.0)
            q3a = MathTex(r"\frac{d}{dt}\cos 3t", font_size=34).move_to([x3, TXT_Y[0] + 0.05, 0])
            q3b = MathTex(r"=", r"\,?", font_size=34).move_to([x3, TXT_Y[1], 0])
            c.wait_until("derivative")
            self.play(*appear(q3a, q3b, lag=0.3), run_time=1.0)
            c.wait_until("a3")
            a3 = MathTex(r"=", r"-3\sin 3t", font_size=34).move_to([x3, TXT_Y[1], 0])
            chain = kit.tag("chain rule").move_to([x3, TXT_Y[2], 0])
            self.play(*edit(q3b, a3), run_time=1.2)
            c.wait_until(own_word=chain)
            self.play(*appear(chain), run_time=0.8)
            self.card_items = [*frames, pend, a1, plane, turned, a2, same, rmark, graph, q3a, a3, chain]

        self.wait(1.2)
        strip = VGroup(*[m for m in self.mobjects if m in self.card_items])
        self.play(strip.animate.scale(0.45).move_to([2.6, -2.95, 0]).set_opacity(0.4), run_time=1.4)
        self.wait(0.8)
