"""Chapter 3, scene 3: size and start (|A| is the amplitude, arg A the phase; x = |A| cos(ωt + arg A)). Clips c3.read.1 – c3.read.4.

Opens on ch3_s2_freeze.handover_shot() (self.add, no FadeIn); ends on an empty frame (s4 fades in).
Plan: the frozen A stays on s2's plane. c1: "?" → GOLD brace |A| and GOLD ticks at ±|A| (the
circle's crossings) → |A| flies to a side panel "amplitude"; YELLOW arc arg A → "phase"; DIM motive
questions. The spring fades at {two} (its block sits on the arc's wedge) and returns at {ours}.
c2: the panel words leave, a time graph under the plane's right (right of the legend) draws the
BLUE wave; live sweeps |A| 5→2→5 and arg A −53°→+60°→−53° (≥ 5 s each, readouts live, DIM crest
guides fixed); readouts settle ("third weight"), the arrow turns once, the weight swings out.
c3: right column, 4 atomic lines with DIM step labels; the boxed cosine form; readback flashes.
c4: think stop (column cleared to its boxed result, moved up); 2i arrow, quarter turn left,
x = −2 sin ωt beside a small copy of the hook's second weight (2 sin 3t), both running one period.
Motion: every tracker is moved inside play() (frame-exact); model time runs at CLOCK (2/3).
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

s2 = load_scene("ch3_s2_freeze")
kit = s2.kit
ak = s2.ak
hook = load_scene("ch3_s1_hook")
# 8 entries in two columns reach x = -0.46 ("amplitude" is the widest word); the kit would fall back
# to one tall column (into the plane) past -0.8. This scene's think box starts right of -0.3.
kit.LEG_MAX_RIGHT = -0.3
spr = load_scene("ch1_s3_spring")

O = np.array(s2.PLANE3_O, dtype=float)
pt = s2.pt
OMEGA3, CLOCK, PERIOD3, PHI3, R3 = s2.OMEGA3, s2.CLOCK, s2.PERIOD3, s2.PHI3, s2.R3
TURN_RT = PERIOD3 / CLOCK                  # one turn at the chapter's on-screen rate (3.14 s)

# legend entries added here (s2's short style)
E_ABS = (r"|A|", GOLD, "amplitude")
E_ARG = (r"\arg A", YELLOW, "phase")

# side panel (clip 1–2), right of the plane
PX, PX_W = 1.2, 2.75
ROW1_Y, ROW2_Y, Q_DY = 0.5, -0.85, 0.55

# time graph, under the plane's right, right of the legend
GX0, GY, WSEC, WS = 0.1, -2.85, 1.42, 0.12
TW = 2 * PERIOD3
G_HALF = 0.64

# derivation column
COLX = 0.65
COL_YS = [1.1, 0.2, -0.8, -1.75]
STOP_Y = 1.0                               # the boxed result's row during clip 4


def z_of(L, ph, t):
    return L * cmath.exp(1j * (ph + OMEGA3 * t))


def gpt(t, x_cm):
    return np.array([GX0 + WSEC * t, GY + WS * x_cm, 0.0])


def paint(m, spans):
    for i, j, col in spans:
        m[0][i:j].set_color(col)
    return m


def step_lab(text, y):
    """kit.step_label's look (DIM arrow + 22-px label) at an explicit gap height."""
    arr = Arrow(UP * 0.16, DOWN * 0.16, buff=0, stroke_width=2.5, tip_length=0.1,
                max_tip_length_to_length_ratio=0.4, color=DIM).move_to([COLX + 0.18, y, 0])
    lab = kit._t(text, kit.STEP_SIZE, DIM).next_to(arr, RIGHT, buff=0.15)
    return VGroup(arr, lab)


_MINUS = {}


def deg_num(rad, size, color):
    """A degree readout as one serif Text, with TeX's minus sign in front when negative (the
    font's own U+2212 reads as a dash)."""
    d = round(math.degrees(rad))
    num = T(f"{abs(d)}°", size=size, color=color)
    if d >= 0:
        return num
    key = (size, color)
    if key not in _MINUS:
        _MINUS[key] = MathTex("-", font_size=size * 1.1, color=color)
    m = _MINUS[key].copy().next_to(num, LEFT, buff=0.06)
    m.set_y(num.get_y())
    return VGroup(m, num)


class Read(NarratedScene):
    def construct(self):
        self.L = ValueTracker(R3)
        self.PH = ValueTracker(PHI3)
        self.TT = ValueTracker(0.0)
        self.sp_op = ValueTracker(1.0)
        self.opening()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.ending()

    # ── live pieces ─────────────────────────────────────────────────────────────
    def z(self):
        return z_of(self.L.get_value(), self.PH.get_value(), self.TT.get_value())

    def opening(self):
        h = s2.handover_shot()
        self.plane, self.labs, self.card, self.pin, self.leg = h.plane, h.labels, h.card, h.pin, h.legend
        self.spring = always_redraw(lambda: s2.spring3(0.0, amp=self.z(), op=self.sp_op.get_value()))
        self.arrow = always_redraw(lambda: ak.arrow_between(O, pt(self.z()), GOLD, 6, s2.Z_GOLD))
        a_base = s2._a_label()
        self.al_op = ValueTracker(1.0)
        self.alab = always_redraw(lambda: s2._fade(a_base.copy().next_to(pt(self.z()), RIGHT, buff=0.22),
                                                   self.al_op.get_value()))
        self.shadow = always_redraw(lambda: s2.shadow3(0.0, amp=self.z()))
        self.add(self.plane, self.labs, self.spring, self.arrow, self.alab, self.shadow,
                 self.card, self.pin, self.leg)

    @staticmethod
    def freeze(*mobs):
        for m in mobs:
            m.clear_updaters()

    # ── c3.read.1: what the frozen arrow tells you ─────────────────────────────────
    def clip1(self):
        with self.say("c3.read.1") as c:
            self.qm = T("?", size=44, color=DIM).next_to(self.alab, RIGHT, buff=0.18)
            self.play(self.sp_op.animate.set_value(0.0), *appear(self.qm), run_time=0.7)
            self.remove(self.spring)

            # {length}: the brace along the arrow, |A|
            c.wait_until("length")
            self.br_op = ValueTracker(0.0)
            blab_base = set_backstroke(MathTex("|A|", font_size=36, color=GOLD))

            def brace_b():
                tip = pt(self.z())
                d = tip - O
                u = d / np.linalg.norm(d)
                n = np.array([u[1], -u[0], 0.0])
                b = BraceBetweenPoints(O, tip, direction=n, buff=0.2, color=GOLD)
                lab = blab_base.copy().move_to(b.get_tip() + n * 0.32)
                g = VGroup(b, lab)
                g.brace, g.label = b, lab
                return s2._fade(g, self.br_op.get_value())
            self.brace = always_redraw(brace_b)
            self.add(self.brace)
            self.play(self.br_op.animate.set_value(1.0), *disappear(self.qm), run_time=1.2)

            # the tip stays on its circle → the shadow's reach: ticks at ±|A|
            c.wait_until("The tip stays")
            ring = self.plane.circle.copy().set_stroke(GOLD, 6)
            self.play(VShowPassingFlash(ring, time_width=0.5), run_time=1.6)
            c.wait_until("each side")
            self.tk_op = ValueTracker(0.0)

            def ticks_b():
                Lv = self.L.get_value()
                g = VGroup(*[Line(pt(s * Lv) + 0.22 * DOWN, pt(s * Lv) + 0.22 * UP).set_stroke(GOLD, 5)
                             for s in (-1, 1)])
                g.set_z_index(s2.Z_MARK)
                return s2._fade(g, self.tk_op.get_value())
            self.ticks = always_redraw(ticks_b)
            self.add(self.ticks)
            self.play(self.tk_op.animate.set_value(1.0), run_time=1.0)

            # "That's the amplitude": |A| flies to the side panel
            c.wait_until("That's the amplitude")
            self.sym1 = MathTex("|A|", font_size=48, color=GOLD).move_to([PX, ROW1_Y, 0], aligned_edge=LEFT)
            self.word1 = T("amplitude", size=36, color=GOLD)
            self.word1.move_to([PX_W, ROW1_Y, 0], aligned_edge=LEFT)
            self.word1.align_to(self.sym1, DOWN).shift(0.06 * UP)
            self.play(FlashAround(self.brace[1], color=GOLD, time_width=1.5), *appear(self.sym1), run_time=1.3)
            c.wait_until("amplitude")
            ents = [e for e in self.leg.entries if e[0] != s2.E_MIRROR[0]] + [E_ABS]
            kit.legend_set(self, self.leg, ents, *appear(self.word1), run_time=1.2)

            # {angle}: the arc from +Re round to A
            c.wait_until("angle")
            self.arc_f, self.arc_op = ValueTracker(0.0), ValueTracker(1.0)

            def arc_b():
                a = self.PH.get_value() * self.arc_f.get_value()
                if abs(a) < 1e-3:
                    a = -1e-3
                arc = Arc(radius=0.55, start_angle=0, angle=a, arc_center=O).set_stroke(YELLOW, 4)
                arc.set_z_index(s2.Z_MARK)
                return s2._fade(arc, self.arc_op.get_value())
            self.arc = always_redraw(arc_b)
            self.add(self.arc)
            self.arg_lab = set_backstroke(MathTex(r"\arg A", font_size=30, color=YELLOW))
            mid = O + 1.0 * np.array([math.cos(PHI3 / 2), math.sin(PHI3 / 2), 0.0])
            self.arg_lab.move_to(mid)
            self.arg_lab.shift((min(0.0, -2.05 - self.arg_lab.get_right()[0])) * RIGHT)
            self.play(self.arc_f.animate.set_value(1.0), run_time=1.2)
            self.play(*appear(self.arg_lab), run_time=0.9)

            # "where in its cycle … the phase"
            c.wait_until("That tells you")
            self.sym2 = MathTex(r"\arg A", font_size=48, color=YELLOW).move_to([PX, ROW2_Y, 0],
                                                                                aligned_edge=LEFT)
            self.word2 = T("phase", size=36, color=YELLOW).move_to([PX_W, ROW2_Y, 0], aligned_edge=LEFT)
            self.word2.align_to(self.sym2, DOWN)
            self.play(FlashAround(self.arg_lab, color=YELLOW, time_width=1.5), *appear(self.sym2), run_time=1.3)
            c.wait_until("phase")
            kit.legend_add(self, self.leg, E_ARG, run_time=1.2, extra=appear(self.word2))

            # {motive}
            c.wait_until("motive")
            self.q1 = T("how big?", size=30, color=DIM).move_to([PX_W, ROW1_Y - Q_DY, 0], aligned_edge=LEFT)
            self.q2 = T("where it starts?", size=30, color=DIM).move_to([PX_W, ROW2_Y - Q_DY, 0],
                                                                        aligned_edge=LEFT)
            self.play(*appear(self.q1, self.q2, lag=0.5), run_time=1.4)

    # ── c3.read.2: the two knobs ───────────────────────────────────────────────────
    def clip2(self):
        with self.say("c3.read.2") as c:
            # the time graph under the plane; the wave drawn from the arrow
            axis = Line(gpt(0, 0), gpt(TW, 0) + 0.3 * RIGHT).set_stroke(DIM, 2.5)
            vax = Line(gpt(0, 0) + G_HALF * DOWN, gpt(0, 0) + G_HALF * UP).set_stroke(DIM, 2.5)
            tl = MathTex("t", font_size=30, color=DIM).next_to(axis, RIGHT, buff=0.12)
            xl = MathTex("x", font_size=32, color=BLUE).next_to(vax.get_top(), LEFT, buff=0.12)
            self.guides = VGroup(*[DashedLine(gpt(tc, 0) + G_HALF * DOWN, gpt(tc, 0) + G_HALF * UP,
                                              dash_length=0.08).set_stroke(DIM, 2)
                                   for tc in [(-PHI3 + TAU * k) / OMEGA3 for k in range(2)]])
            self.axes_g = VGroup(axis, vax, tl, xl)
            self.wd = ValueTracker(0.0)
            self.now_op = ValueTracker(0.0)

            def wave_b():
                f = self.wd.get_value()
                Lv, ph = self.L.get_value(), self.PH.get_value()
                n = max(2, int(180 * f) + 2)
                ts = np.linspace(0, TW * max(f, 1e-3), n)
                w = VMobject().set_points_as_corners([gpt(t, Lv * math.cos(OMEGA3 * t + ph)) for t in ts])
                w.set_stroke(BLUE, 4)
                g = VGroup(w)
                if 0.0 < f < 1.0:
                    g.add(Dot(gpt(ts[-1], Lv * math.cos(OMEGA3 * ts[-1] + ph)), radius=0.07, color=BLUE))
                tn = self.TT.get_value()
                if self.now_op.get_value() > 0 and 0 <= tn <= TW:
                    d = Dot(gpt(tn, Lv * math.cos(OMEGA3 * tn + ph)), radius=0.09, color=BLUE)
                    g.add(d.set_opacity(self.now_op.get_value()))
                return g
            self.wave = always_redraw(wave_b)

            # live readouts beside the panel symbols
            self.ro_op = ValueTracker(0.0)
            self.eq1 = MathTex("=", font_size=44, color=GOLD).next_to(self.sym1, RIGHT, buff=0.2)
            self.eq2 = MathTex("=", font_size=44, color=YELLOW).next_to(self.sym2, RIGHT, buff=0.2)

            def num1_b():
                m = T(f"{self.L.get_value():.2f}", size=44, color=GOLD).next_to(self.eq1, RIGHT, buff=0.18)
                return s2._fade(m, self.ro_op.get_value())

            def num2_b():
                m = deg_num(self.PH.get_value(), 44, YELLOW).next_to(self.eq2, RIGHT, buff=0.18)
                return s2._fade(m, self.ro_op.get_value())
            self.num1, self.num2 = always_redraw(num1_b), always_redraw(num2_b)

            self.play(*during(disappear(self.word1, self.word2, self.arg_lab), 0, 0.45),
                      *during(appear(self.axes_g, self.guides, lag=0.3), 0.45, 1.0), run_time=1.2)
            self.add(self.wave, self.num1, self.num2)
            self.play(self.wd.animate.set_value(1.0), self.ro_op.animate.set_value(1.0),
                      *appear(self.eq1, self.eq2, shift=None), run_time=1.5, rate_func=linear)

            # knob 1: the length 5 → 2 → 5; the height follows, the crests stay
            c.wait_until("Stretch the arrow")
            sweep1 = UpdateFromAlphaFunc(self.L, lambda m, a: m.set_value(R3 - 3.0 * (1 - math.cos(TAU * a)) / 2),
                                         rate_func=linear)
            self.play(sweep1, *during(disappear(self.q1), 0, 0.12), run_time=min(6.0, c.until("knob2") - 0.2))
            self.L.set_value(R3)

            # knob 2: the angle −53° → +60° → −53°; the wave slides at a fixed height
            c.wait_until("knob2")
            top = math.radians(60)

            def ph_at(a):
                return PHI3 + (top - PHI3) * (1 - math.cos(TAU * a)) / 2
            sweep2 = UpdateFromAlphaFunc(self.PH, lambda m, a: m.set_value(ph_at(a)), rate_func=linear)
            self.play(sweep2, *during([self.br_op.animate.set_value(0.0)], 0, 0.1),
                      *during(disappear(self.q2), 0, 0.1), run_time=min(5.6, c.until("ours") - 0.1))
            self.PH.set_value(PHI3)
            self.remove(self.brace)

            # {ours}: the readouts settle on the third weight's arrow
            c.wait_until("ours")
            n1 = T(f"{R3:.2f}", size=44, color=GOLD).next_to(self.eq1, RIGHT, buff=0.18)
            n2 = deg_num(PHI3, 44, YELLOW).next_to(self.eq2, RIGHT, buff=0.18)
            self.remove(self.num1, self.num2)
            self.add(n1, n2)
            self.n1f = T("5", size=44, color=GOLD).next_to(self.eq1, RIGHT, buff=0.18)
            self.n2f = MathTex(r"\approx -0.93\ \mathrm{rad}\ \ (-53^\circ)", font_size=40, color=YELLOW)
            self.n2f.next_to(self.sym2, RIGHT, buff=0.2)
            self.third = T("third weight", size=30, color=FG).move_to([PX, 1.12, 0], aligned_edge=LEFT)
            old2 = VGroup(self.eq2, n2)
            self.play(*swap(n1, self.n1f), *swap(old2, self.n2f), run_time=1.2)
            self.play(*appear(self.third), run_time=0.9)
            c.wait_until("so it swings")
            self.add(self.spring)
            self.play(self.sp_op.animate.set_value(1.0), run_time=1.0)

            # "Its angle …": the arrow turns once; the weight starts at 3 and moves outward
            c.wait_until("Its angle")
            turn = UpdateFromAlphaFunc(self.TT, lambda m, a: m.set_value(PERIOD3 * a), rate_func=linear)
            self.play(*during([self.arc_op.animate.set_value(0.0), self.al_op.animate.set_value(0.0),
                               self.now_op.animate.set_value(1.0)], 0, 0.1),
                      time_span(turn, 0.35, 0.35 + TURN_RT), run_time=0.35 + TURN_RT)
            self.TT.set_value(0.0)
            self.play(self.al_op.animate.set_value(1.0), run_time=0.6)
            self.remove(self.arc)

    # ── c3.read.3: the same reading in symbols ─────────────────────────────────────
    def clip3(self):
        with self.say("c3.read.3") as c:
            G, Y, B = GOLD, YELLOW, BLUE
            self.l0 = paint(MathTex(r"A = |A|\,e^{i\arg A}", font_size=36),
                            [(0, 1, G), (2, 5, G), (7, 11, Y)])
            self.l1 = paint(MathTex(r"A\,e^{i\omega t} = |A|\,e^{i(\omega t + \arg A)}", font_size=36),
                            [(0, 1, G), (3, 5, Y), (6, 9, G), (12, 14, Y), (15, 19, Y)])
            self.l2 = paint(MathTex(r"\mathrm{Re}\left[\,|A|\,e^{i(\omega t + \arg A)}\right] = |A|\cos(\omega t + \arg A)",
                                    font_size=34),
                            [(0, 2, B), (3, 6, G), (9, 11, Y), (12, 16, Y), (19, 22, G), (22, 25, B),
                             (26, 28, Y), (29, 33, Y)])
            self.l3 = paint(MathTex(r"x(t) = |A|\cos(\omega t + \arg A)", font_size=40),
                            [(0, 4, B), (5, 8, G), (8, 11, B), (12, 14, Y), (15, 19, Y)])
            for ln, y in zip((self.l0, self.l1, self.l2, self.l3), COL_YS):
                ln.move_to([COLX, y, 0], aligned_edge=LEFT)
            if self.l2.get_right()[0] > kit.EDGE_X:
                self.l2.scale_to_fit_width(kit.EDGE_X - COLX).move_to([COLX, COL_YS[2], 0], aligned_edge=LEFT)
            self.lab0 = kit.tag("polar form", self.l0, RIGHT, buff=0.35)
            self.lab1 = step_lab("the angles add", (COL_YS[0] + COL_YS[1]) / 2)
            self.lab2 = step_lab("shadow: length × cos angle", (COL_YS[1] + COL_YS[2]) / 2 - 0.03)
            self.lab3 = step_lab("the shadow is x", (COL_YS[2] + COL_YS[3]) / 2 + 0.02)
            self.box3 = SurroundingRectangle(self.l3, color=YELLOW, buff=0.14, corner_radius=0.06).set_stroke(width=2.5)
            self.tag3 = kit.tag("beyond the notes")
            self.tag3.move_to([kit.EDGE_X, self.lab3.get_y(), 0], aligned_edge=RIGHT)

            # {polar}: the panel leaves, the first line arrives
            panel = [self.sym1, self.eq1, self.n1f, self.sym2, self.n2f, self.third]
            self.play(*during(disappear(*panel), 0, 0.45), *during(appear(self.l0), 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("polar form")
            self.play(*appear(self.lab0), run_time=0.9)

            c.wait_until("turn")
            self.play(*appear(self.lab1, self.l1, lag=0.4, shift=None), run_time=min(1.4, c.until("shadow") - 0.1))
            c.wait_until("shadow")
            self.play(*appear(self.lab2, self.l2, lag=0.4, shift=None), run_time=1.5)

            c.wait_until("cosform")
            self.play(*appear(self.lab3, self.l3, lag=0.4, shift=None), *set_alpha([self.l0, self.lab0], 0.4), run_time=1.5)
            self.play(GrowFromCenter(self.box3), *appear(self.tag3), run_time=1.0)

            # {readback}: the wave's height (GOLD) and its shift from t = 0 (YELLOW)
            c.wait_until("readback")
            tc = -PHI3 / OMEGA3
            self.hseg = Line(gpt(tc, 0), gpt(tc, R3)).set_stroke(GOLD, 6)
            self.sseg = Line(gpt(0, 0), gpt(tc, 0)).set_stroke(YELLOW, 6)
            c.wait_until("as tall")
            self.play(GrowFromEdge(self.hseg, DOWN),
                      FlashAround(self.l3[0][5:8], color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("slid in time")
            self.play(GrowFromEdge(self.sseg, LEFT),
                      FlashAround(self.l3[0][15:19], color=YELLOW, time_width=1.5), run_time=1.5)

    # ── c3.read.4: think stop, 2i ──────────────────────────────────────────────────
    def clip4(self):
        with self.say("c3.read.4") as c:
            # {stop}: everything but the boxed result clears; the result moves up; the card dims
            self.freeze(self.wave, self.ticks, self.arrow, self.alab, self.shadow, self.spring)
            gone = [self.axes_g, self.guides, self.wave, self.hseg, self.sseg, self.ticks, self.arrow,
                    self.alab, self.shadow, self.spring, self.l0, self.lab0, self.l1, self.lab1,
                    self.l2, self.lab2, self.lab3, self.tag3]
            dy = (STOP_Y - self.l3.get_y()) * UP
            self.play(*during(disappear(*gone), 0, 0.45),
                      *during([self.l3.animate.shift(dy), self.box3.animate.shift(dy)], 0.4, 1.0),
                      *during([restyle(self.card, 0.6)], 0.4, 1.0), run_time=min(1.8, c.until("Say the")))

            c.wait_until("Say the")
            self.think = kit.think_box("A complex amplitude of 2i.\nWhere does the swing start?\n"
                                       "Which way does it move first?", size=30, pos=np.array([2.75, -2.25, 0]))
            self.ring = kit.think_ring()
            self.play(*appear(self.think, shift=None), FadeIn(self.ring), run_time=1.2)  # early: the think-stop question is read over the next 8 s
            c.wait_until("Pause the video")
            self.play(kit.drain(self.ring, run_time=c.until("up")))

            # {up}: 2i, straight up
            c.wait_until("up")
            self.T2 = ValueTracker(0.0)

            def z2():
                return 2j * cmath.exp(1j * OMEGA3 * self.T2.get_value())
            lab_base = MathTex("2", "i", font_size=40)
            lab_base[0].set_color(GOLD)
            lab_base[1].set_color(PINK)

            def lab2_b():
                tip = pt(z2())
                u = (tip - O) / np.linalg.norm(tip - O)
                return lab_base.copy().move_to(tip + u * 0.38)
            arr0 = ak.arrow_between(O, pt(2j), GOLD, 6, s2.Z_GOLD)
            lab0 = lab2_b()
            self.play(*during(disappear(self.think, self.ring), 0, 0.4), *during([restyle(self.card, 1.0)], 0, 0.4),
                      *during([GrowArrow(arr0)], 0.4, 1.0), *during(appear(lab0), 0.6, 1.0), run_time=1.6)
            self.arrow2 = always_redraw(lambda: ak.arrow_between(O, pt(z2()), GOLD, 6, s2.Z_GOLD))
            self.lab2i = always_redraw(lab2_b)
            self.remove(arr0, lab0)
            self.add(self.arrow2, self.lab2i)

            c.wait_until("its shadow")
            sh0 = s2.shadow3(0.0, amp=2j)
            self.play(FadeIn(sh0, scale=1.6), run_time=0.9)
            self.shadow2 = always_redraw(lambda: s2.shadow3(0.0, amp=z2()))
            self.remove(sh0)
            self.add(self.shadow2)

            # {left}: a quarter turn anticlockwise; the shadow goes to negative x
            c.wait_until("left")
            self.play(self.T2.animate.set_value(PI / (2 * OMEGA3)), run_time=min(2.6, c.until("formula") - 0.3))

            # {formula}: x = −2 sin ωt, beside the opening's second weight (2 sin 3t)
            c.wait_until("formula")
            self.f2 = paint(MathTex(r"x = -2\sin\omega t", font_size=48),
                            [(0, 1, BLUE), (2, 4, GOLD), (4, 7, BLUE), (7, 9, YELLOW)])
            self.f2.move_to([COLX, -0.1, 0], aligned_edge=LEFT)
            self.hk = paint(MathTex(r"x = 2\sin 3t", font_size=36), [(0, 1, BLUE), (2, 3, GOLD), (3, 6, BLUE)])
            self.hk.move_to([COLX, -1.2, 0], aligned_edge=LEFT)
            self.hk_tag = kit.tag("the opening's second weight").next_to(self.hk, DOWN, buff=0.18).align_to(self.hk, LEFT)
            target = np.array([4.75, -1.55, 0.0])

            def mini_b():
                x = 2.0 * math.sin(OMEGA3 * self.T2.get_value())
                return hook._place(spr.spring_drawing(x=x, y=0.0, zero=False), 0.5, target)
            mini0 = mini_b()
            self.play(*appear(self.f2, self.hk, mini0, self.hk_tag, lag=0.3), run_time=1.6)
            self.mini = always_redraw(mini_b)
            self.remove(mini0)
            self.add(self.mini)
            c.wait_until("It's the second weight")
            t0 = self.T2.get_value()
            run = UpdateFromAlphaFunc(self.T2, lambda m, a: m.set_value(t0 + PERIOD3 * a), rate_func=linear)
            self.play(run, run_time=max(1.0, min(TURN_RT, c.until() + 0.3)))

    def ending(self):
        self.freeze(*self.mobjects)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
