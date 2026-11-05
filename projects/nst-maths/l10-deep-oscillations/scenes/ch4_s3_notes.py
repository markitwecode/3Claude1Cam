"""Chapter 4, scene 3: your turn, with letters (the notes' example x(0) = c, ẋ(0) = √3cω). Clips c4.faded.1 – c4.faded.5.

Opens on ch4_s2_start's handover shot. Drawn with c = 2.5 cm, ω = 3 (s2's plane and scale; neither
number is on screen). Exports think_math(lines, size, pos) (the kit's think box with maths inline).
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
s2 = load_scene("ch4_s2_start")

O, U, F, OMEGA, EXT = s2.O, s2.U, s2.F, s2.OMEGA, s2.EXT
P = s2.P
R3 = math.sqrt(3)
CC = 2.5                                  # c (cm), drawing only
AMP = CC * complex(1, -R3)                # A = c(1 − i√3)
V0 = R3 * CC * OMEGA                      # √3 c ω (cm/s)
PUSH_Y = O[1] + spr.BLOCK_H / 2 + 0.3
TABLE_Y = O[1] - spr.BLOCK_H / 2
Z_MARK = -1.7
COLX = kit.COL_LEFT
SZ = 34

E_C = (r"c", BLUE, "starting position")
E_W = (r"\omega", FG, "turning rate")
E_A = (r"A", GOLD, "complex amplitude")
E_B = (r"\beta", PINK, "A's vertical part")
E_ABS = (r"|A|", GOLD, "amplitude")
E_ARG = (r"\arg A", YELLOW, "phase")


def _bs(m):
    return set_backstroke(m, BG, 5)


def mt(spec, size=SZ):
    m = MathTex(*[p for p, _ in spec], font_size=size)
    for k, (_, col) in enumerate(spec):
        m[k].set_color(col)
    return m


def frac_color(frac, num=None, den=None):
    """Colour a \\dfrac's numerator / denominator glyphs (by height against the bar)."""
    cy = frac.get_center()[1]
    for g in frac:
        if g.width > 0.8 * frac.width:
            continue
        y = g.get_center()[1]
        if y > cy + 0.05 and num:
            g.set_color(num)
        elif y < cy - 0.05 and den:
            g.set_color(den)
    return frac


def lab(spec):
    """A DIM step label: "text", "m:tex", or ("text", "tex")."""
    if isinstance(spec, tuple):
        a = kit.tag(spec[0])
        b = MathTex(spec[1], font_size=26, color=DIM)
        b.next_to(a, RIGHT, buff=0.1).align_to(a, DOWN).shift(0.02 * DOWN)
        return VGroup(a, b)
    if spec.startswith("m:"):
        return MathTex(spec[2:], font_size=26, color=DIM)
    return kit.tag(spec)


def place(labs, row, idxs, right=kit.EDGE_X, up=0.24):
    last = None
    for lb, k in zip(labs, idxs):
        lb.move_to([row[k].get_center()[0], 0, 0])
        lb.shift((row[k].get_center()[1] + up - lb.get_bottom()[1]) * UP)
        if last is not None and lb.get_left()[0] < last.get_right()[0] + 0.15:
            lb.shift((last.get_right()[0] + 0.15 - lb.get_left()[0]) * RIGHT)
        if lb.get_right()[0] > right:
            lb.shift((right - lb.get_right()[0]) * RIGHT)
        last = lb
    return labs


def think_math(lines, size=28, pos=None):
    """The kit's think box (FG stroke 2, CARD_FILL, DIM hint under it) with maths inline.
    lines: [[("t", text) | ("m", tex, colour), …], …]. .box .question (VGroup of lines) .hint"""
    rows = VGroup()
    for li, ln in enumerate(lines):
        row, x = VGroup(), 0.0
        for item in ln:
            if item[0] == "t":
                m = kit._t(item[1], size, FG)
                kit._baseline_align(m, 0)
                gap = 0.03 if item[1][0] in ",.?" else 0.13
            else:
                full = MathTex(r"\mathrm{x}", item[1], font_size=size * 1.08)
                full.shift(-full[0].get_bottom()[1] * UP)
                m = full[1].set_color(item[2])
                gap = 0.13
            if len(row) == 0:
                gap = 0
            m.shift((x + gap - m.get_left()[0]) * RIGHT)
            x = m.get_right()[0]
            row.add(m)
        row.shift(-li * 0.5 * size / 28 * UP)
        rows.add(row)
    for r in rows:
        r.shift((rows.get_center()[0] - r.get_center()[0]) * RIGHT)
    box = RoundedRectangle(corner_radius=0.12, width=rows.width + 0.5, height=rows.height + 0.42)
    box.set_stroke(FG, 2).set_fill(kit.CARD_FILL, 1).move_to(rows)
    hint = kit._t("pause the video if you want longer", 24, DIM).next_to(box, DOWN, buff=0.14)
    g = VGroup(box, rows, hint)
    g.move_to(pos if pos is not None else kit.THINK_POS)
    g.box, g.question, g.hint = box, rows, hint
    return g


# ── right column specs ───────────────────────────────────────────────────────────
FACT1 = [("x", BLUE), ("(0)", FG), ("=", FG), ("c", BLUE)]
FACT2 = [("v(0)", FG), (r"\equiv", FG), (r"\dot x", GREEN), ("(0)", FG), ("=", FG),
         (r"\sqrt{3}\,c\,\omega", GREEN)]
S0 = [("A", GOLD), ("=", FG), ("c", BLUE), ("-", FG), ("i", PINK),
      (r"\,\dfrac{\sqrt{3}\,c\,\omega}{\omega}", FG)]
S1 = [("=", FG), ("c", BLUE), ("-", PINK), ("i", PINK), (r"\sqrt{3}\,c", PINK)]
S2 = [("=", FG), ("c", BLUE), ("(1", FG), ("-", PINK), (r"i\sqrt{3}", PINK), (")", FG)]
AR = [("A", GOLD)] + S2
AR2 = AR + [("=", FG), ("2c", GOLD), (r"\,e^{-i\pi/3}", GOLD)]
LR = [("|A|", GOLD), ("=", FG), (r"\sqrt{c^2 + 3c^2}", FG), ("=", FG), (r"\sqrt{4c^2}", FG), ("=", FG),
      ("2c", GOLD)]
CR = [(r"\cos(\text{angle})", FG), ("=", FG), (r"\dfrac{c}{2c}", FG), ("=", FG), (r"\dfrac{1}{2}", FG)]

# the long way (notes p. 109)
LW = [
    [("x", BLUE), ("(0)", FG), ("=", FG), (r"\mathrm{Re}(", FG), ("A", GOLD), (")", FG), ("=", FG), ("c", BLUE),
     (r"\;\Rightarrow\;", FG), ("A", GOLD), ("=", FG), ("c", BLUE), ("+", FG), ("i", PINK), (r"\beta", PINK)],
    [(r"\dot x", GREEN), ("(0)", FG), ("=", FG), (r"\mathrm{Re}(", FG), ("i", PINK), (r"\omega", FG), ("A", GOLD),
     (")", FG), ("=", FG), (r"\sqrt{3}\,c\,\omega", GREEN)],
    [("i", PINK), (r"\omega", FG), ("(", FG), ("c", BLUE), ("+", FG), ("i", PINK), (r"\beta", PINK), (")", FG),
     ("=", FG), ("i", PINK), (r"\omega", FG), ("c", BLUE), ("+", FG), ("i^2", PINK), (r"\omega", FG),
     (r"\beta", PINK), ("=", FG), ("i", PINK), (r"\omega", FG), ("c", BLUE), ("-", FG), (r"\omega", FG),
     (r"\beta", PINK)],
    [("-", FG), (r"\omega", FG), (r"\beta", PINK), ("=", FG), (r"\sqrt{3}\,c\,\omega", GREEN),
     (r"\;\Rightarrow\;", FG), (r"\beta", PINK), ("=", FG), ("-", PINK), (r"\sqrt{3}\,c", PINK)],
    [("A", GOLD), ("=", FG), ("c", BLUE), ("+", FG), ("i", PINK), (r"\beta", PINK), ("=", FG), ("c", BLUE),
     ("(1", FG), ("-", PINK), (r"i\sqrt{3}", PINK), (")", FG)],
]
LW_LABS = [(["m:e^0 = 1", "real part c"], [2, 8]),
           (["m:e^0 = 1"], [2]),
           (["multiply out", "m:i^2 = -1"], [8, 16]),
           (["real parts match", "divide by −ω"], [3, 5]),
           ([("put in", r"\beta")], [6])]


class Notes(NarratedScene):
    def construct(self):
        self.t = ValueTracker(0.0)
        self.xw = ValueTracker(3.0)        # the weight's start (s2 left it at 3 cm)
        self.push_op = ValueTracker(0.0)
        self.drop_op = ValueTracker(0.0)
        self.grow = ValueTracker(0.0)
        self.opening()
        self.clip1()
        self.clip2()
        self.long_way()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── live pieces ──
    def z(self):
        return AMP * cmath.exp(1j * OMEGA * self.t.get_value())

    def weight_x(self):
        return self.xw.get_value() + self.z().real - CC

    def opening(self):
        shot = s2.handover_shot()
        self.add(*shot)
        self.plane, self.old_gold, self.gen, self.card = shot.plane, shot.gold, shot.general, shot.card
        self.leg, self.pin = shot.legend, shot.pin
        self.spring = always_redraw(lambda: s2.spring_at(self.weight_x()))
        self.remove(shot.spring)
        self.add(self.spring)
        self.push = always_redraw(lambda: s2.push_arrow(self.weight_x(), V0, op=self.push_op.get_value()))
        self.gold = always_redraw(lambda: s2.gold_arrow(self.z(), grow=self.grow.get_value()))

        def drop():
            tip, foot = P(self.z()), P(self.z().real)
            op = self.drop_op.get_value()
            if op < 0.01 or np.linalg.norm(tip - foot) < 0.06:
                return s2._empty()
            return DashedLine(tip, foot, dash_length=0.08).set_stroke(DIM, 2, opacity=op)
        self.drop = always_redraw(drop)
        self.add(self.push, self.gold, self.drop)

    # ── clip 1: the start, think stop T4.1 ──
    def clip1(self):
        gen_t = self.gen.copy().scale(0.8)
        gen_t.move_to([COLX, self.card.get_bottom()[1] - 0.18, 0], aligned_edge=UL)
        self.f1 = mt(FACT1, 32).move_to([COLX, 0.72, 0], aligned_edge=LEFT)
        self.f2 = mt(FACT2, 32).move_to([COLX, 0.15, 0], aligned_edge=LEFT)
        self.ftag = kit.tag("example · notes p. 109", self.f1, RIGHT, buff=0.45)
        xc = P(CC)[0]
        self.tick = Line([xc, TABLE_Y, 0], [xc, TABLE_Y - 0.16, 0]).set_stroke(BLUE, 4)
        self.clab = MathTex("c", font_size=34, color=BLUE).move_to([xc + 0.16, TABLE_Y - 0.12, 0], aligned_edge=UL)
        self.plab = _bs(MathTex(r"\sqrt{3}\,c\,\omega", font_size=30, color=GREEN))

        def stick(m):
            m.move_to([P(self.weight_x())[0] + 0.1, PUSH_Y + 0.32, 0], aligned_edge=LEFT)
        stick(self.plab)
        self.plab.add_updater(stick)
        self.q1 = think_math([[("t", "It starts at"), ("m", "c", BLUE), ("t", ",")],
                              [("t", "moving outward at"), ("m", r"\sqrt{3}\,c\,\omega", GREEN), ("t", ".")],
                              [("t", "Using the move,")],
                              [("t", "what's the complex amplitude?")]], pos=[2.75, -1.95, 0])
        self.ring = kit.think_ring()
        with self.say("c4.faded.1") as c:
            kit.legend_set(self, self.leg, [E_C, E_W, E_A, E_B],  # early: the scene's letters, listed as the board resets
                           FadeOut(self.old_gold), Transform(self.gen, gen_t), run_time=1.5)
            self.play(*appear(self.f1, self.f2, self.ftag, lag=0.35, shift=None), run_time=1.5)  # early: the example's start, as the notes print it
            c.wait_until("start")
            self.play(self.xw.animate.set_value(CC), *during(appear(self.tick, self.clab), 0.5, 1),
                      run_time=min(1.6, c.until("push") - 0.1))
            c.wait_until("push")
            self.play(self.push_op.animate.set_value(1.0), *appear(self.plab), run_time=1.2)
            c.wait_until("think")
            self.play(FadeIn(self.q1.box), *appear(*self.q1.question, lag=0.3, shift=None), FadeIn(self.ring),  # early: the think stop's question, read at once
                      *set_alpha([self.card], 0.6), run_time=1.4)
            c.wait_until("pause the video")
            self.play(*appear(self.q1.hint), run_time=0.8)
            self.play(kit.drain(self.ring, max(0.5, c.until() - 0.05)))

    # ── clip 2: the short way ──
    def clip2(self):
        s0 = mt(S0)
        frac_color(s0[5], num=GREEN)
        s0.move_to([COLX, -0.85, 0], aligned_edge=LEFT)
        self.s0a, self.s0b = VGroup(*s0[0:3]), VGroup(*s0[3:])
        self.s0 = s0
        self.l0 = place([lab("put in the start")], s0, [1])
        over = self.l0[0].get_right()[0] - (s0[5].get_left()[0] - 0.15)
        if over > 0:
            self.l0[0].shift(over * LEFT)
        eqx = s0[1].get_center()[0]
        self.s1 = mt(S1)
        self.s1.shift((eqx - self.s1[0].get_center()[0]) * RIGHT + (-1.85 - self.s1[0].get_center()[1]) * UP)
        self.l1 = place([lab("ω cancels")], self.s1, [0])
        self.s2r = mt(S2)
        self.s2r.shift((eqx - self.s2r[0].get_center()[0]) * RIGHT + (-2.65 - self.s2r[0].get_center()[1]) * UP)
        self.l2 = place([lab("take out c")], self.s2r, [0])
        gl = self.gen.line
        with self.say("c4.faded.2") as c:
            self.play(*disappear(self.q1, self.ring), *set_alpha([self.card], 1.0), run_time=0.8)
            self.play(*appear(self.s0a, *self.l0, shift=None, lag=0.3),
                      FlashAround(gl[2], color=BLUE, time_width=1.5), run_time=1.3)
            c.wait_until("vertical part")
            self.play(*appear(self.s0b, shift=None), FlashAround(gl[5], color=GREEN, time_width=1.5),
                      run_time=1.4)
            c.wait_until("cancel")
            self.play(*appear(self.s1, *self.l1, shift=None, lag=0.3),
                      FlashAround(s0[5], color=FG, time_width=1.5), run_time=1.3)
            c.wait_until("result")
            self.play(*appear(self.s2r, *self.l2, shift=None, lag=0.3),
                      *set_alpha([self.gen, self.f1, self.ftag], 0.5), run_time=1.3)
            c.wait_until("route")
            self.lw_frame()
            self.play(FadeIn(self.lw_box), *appear(self.lw_head, self.lw_tag, shift=None, lag=0.3),
                      run_time=min(1.0, c.until()))

    def lw_frame(self):
        top, bot = 2.95, kit.legend([E_C, E_W, E_A, E_B]).get_top()[1] + 0.12
        left, right = -kit.EDGE_X, 0.2
        self.lw_box = RoundedRectangle(corner_radius=0.12, width=right - left, height=top - bot)
        self.lw_box.set_stroke(DIM, 1.5).set_fill(kit.CARD_FILL, 0.97).move_to([(left + right) / 2, (top + bot) / 2, 0])
        self.lw_box.set_z_index(5)
        self.lw_head = kit._t("the long way", 26, DIM).move_to([left + 0.3, top - 0.32, 0], aligned_edge=LEFT)
        self.lw_tag = kit.tag("notes p. 109", self.lw_head, RIGHT, buff=0.35)
        rows, labs = [], []
        y0 = top - 1.12
        pitch = (y0 - (bot + 0.4)) / 4
        for i, (spec, (ls, idx)) in enumerate(zip(LW, LW_LABS)):
            r = mt(spec, 30).move_to([left + 0.35, y0 - i * pitch, 0], aligned_edge=LEFT)
            rows.append(r)
            labs.append(place([lab(s) for s in ls], r, idx, right=right - 0.15))
        self.lw_rows, self.lw_labs = rows, labs
        for m in [self.lw_head, self.lw_tag, *rows, *[x for ls in labs for x in ls]]:
            m.set_z_index(6)

    # ── the long way, built in the pause after c4.faded.2 ──
    def long_way(self):
        for i, (r, ls) in enumerate(zip(self.lw_rows, self.lw_labs)):
            self.play(*appear(r, shift=None), *appear(*ls, shift=None, lag=0.4), run_time=1.0)
            self.wait(0.35)
        self.play(FlashAround(self.lw_rows[4][7:], color=YELLOW, time_width=1.5),
                  FlashAround(self.s2r[1:], color=YELLOW, time_width=1.5), run_time=1.4)
        self.wait(0.6)

    # ── clip 3: think stop T4.2, length and angle ──
    def clip3(self):
        self.ar = mt(AR)
        self.ar.shift((COLX - self.ar.get_left()[0]) * RIGHT + (-0.85 - self.ar[1].get_center()[1]) * UP)
        self.q2 = kit.think_box("How long is that arrow,\nand at what angle?", size=32, pos=[3.2, -2.35, 0])
        ring = kit.think_ring()
        blue = s2._leg(0, CC, BLUE)
        pink = s2._leg(CC, AMP, PINK)
        self.legs = [blue, pink]
        self.pl = _bs(MathTex(r"\sqrt{3}\,c", font_size=30, color=PINK))
        self.pl.move_to([P(CC)[0] + 0.15, O[1] - 1.2, 0], aligned_edge=LEFT)
        lr = mt(LR)
        lr.move_to([COLX, -1.85, 0], aligned_edge=LEFT)
        lls = place([lab(s) for s in ["Pythagoras", "add", "c > 0"]], lr, [1, 3, 5])
        self.lr, self.lls = lr, lls
        la, lb, lc = VGroup(*lr[0:3]), VGroup(*lr[3:5]), VGroup(*lr[5:7])
        self.gl = _bs(MathTex("2c", font_size=32, color=GOLD)).move_to([O[0] + 0.25, O[1] - 1.15, 0])
        cr = mt(CR)
        cr[0][4:9].set_color(YELLOW)
        frac_color(cr[2], num=BLUE, den=GOLD)
        cr.move_to([COLX, -2.95, 0], aligned_edge=LEFT)
        self.cr = cr
        self.br = span_brace(np.array([O[0], TABLE_Y + spr.BLOCK_H + 0.02, 0]),
                             np.array([P(CC)[0], TABLE_Y + spr.BLOCK_H + 0.02, 0]), direction=UP, color=DIM)
        self.brl = _bs(kit._t("half of 2c", 26, FG)).next_to(self.br, UP, buff=0.08)
        self.arc = Arc(radius=0.45, start_angle=0, angle=-PI / 3, arc_center=O).set_stroke(YELLOW, 4)
        self.arc.set_z_index(Z_MARK)
        self.argl = _bs(MathTex(r"-\pi/3\ \ (-60^\circ)", font_size=30, color=YELLOW))
        self.argl.move_to([O[0] - 0.15, O[1] - 0.7, 0], aligned_edge=RIGHT)
        self.cpos = kit.tag("c > 0").next_to(self.argl, DOWN, buff=0.12).align_to(self.argl, RIGHT)
        _bs(self.cpos)
        with self.say("c4.faded.3") as c:
            self.play(*during(disappear(self.s0a, self.s0b, self.s1, *self.l0, *self.l1, *self.l2), 0, 0.45),
                      *during(edit(self.s2r, self.ar), 0.4, 1.0),
                      *during(set_alpha([self.f2], 0.5), 0.4, 1.0), run_time=1.4)
            self.play(FadeIn(self.q2.box), *appear(self.q2.question, shift=None), FadeIn(ring),  # early: the think stop's question, read at once
                      *set_alpha([self.card], 0.6), run_time=1.2)
            c.wait_until("pause the video")
            self.play(*appear(self.q2.hint), run_time=0.8)
            self.play(kit.drain(ring, max(0.5, c.until("legs") - 0.05)))
            c.wait_until("legs")
            lwall = [self.lw_box, self.lw_head, self.lw_tag, *self.lw_rows, *[x for ls in self.lw_labs for x in ls]]
            self.plab.clear_updaters()
            self.play(*disappear(self.q2, ring, *lwall, self.plab), *set_alpha([self.card], 1.0),
                      self.push_op.animate.set_value(0.0), run_time=0.9)
            kit.legend_remove(self, self.leg, r"\beta", run_time=1.6,
                              extra=[*during([Create(blue)], 0.0, 0.4), *during([Create(pink)], 0.35, 0.7),
                                     *during([self.grow.animate.set_value(1.0)], 0.6, 1.0)])
            c.wait_until("root three c down")
            self.play(*appear(self.pl), FlashAround(pink, color=PINK, time_width=1.5), run_time=1.0)
            c.wait_until("length")
            kit.legend_add(self, self.leg, E_ABS, run_time=1.4,  # early: |A| joins the legend as its row starts
                           extra=[*appear(la, *lls[:1], shift=None, lag=0.3), *set_alpha([self.ar], 1.0)])
            c.wait_until("make four")
            self.play(*appear(lb, lls[1], shift=None, lag=0.3), run_time=1.0)
            c.wait_until("two c long")
            self.play(*appear(lc, lls[2], shift=None, lag=0.3), *appear(self.gl),
                      *set_alpha([self.f1, self.f2, self.ftag], 0.3), run_time=1.2)
            c.wait_until("angle")
            self.play(GrowFromCenter(self.br), *appear(self.brl), run_time=1.0)
            c.wait_until("so the angle")
            self.play(*appear(self.cr, shift=None), run_time=1.0)
            c.wait_until("sixty")
            kit.legend_add(self, self.leg, E_ARG, run_time=1.3,  # early: "phase" names the angle being drawn
                           extra=[Create(self.arc), *appear(self.argl)])  # early: "phase" names the angle being drawn
            c.wait_until("taking")
            self.ar2 = mt(AR2)
            self.ar2[8][1:].set_color(YELLOW)
            self.ar2.shift(self.ar[0].get_center() - self.ar2[0].get_center())
            self.play(*appear(self.cpos), *edit(self.ar, self.ar2), run_time=min(1.5, max(0.6, c.until())))

    # ── clip 4: the answer, then check it on the picture ──
    def clip4(self):
        top_y = self.gen.get_center()[1]
        amp = VGroup(kit._t("amplitude", 30, GOLD), MathTex(r"|A| = 2c", font_size=34, color=GOLD)).arrange(RIGHT, buff=0.2)
        ph = VGroup(kit._t("phase", 30, YELLOW), MathTex(r"-\pi/3", font_size=34, color=YELLOW)).arrange(RIGHT, buff=0.2)
        for g in (amp, ph):
            g[0].align_to(g[1], DOWN)
        amp.move_to([COLX, 0.75, 0], aligned_edge=LEFT)
        ph.next_to(amp, RIGHT, buff=0.6).align_to(amp, DOWN)
        self.amp, self.ph = amp, ph
        xt = MathTex("x", "(t)", "=", "2c", r"\cos(", r"\omega t", "-", r"\tfrac{1}{3}\pi", ")", font_size=40)
        xt[0].set_color(BLUE)
        xt[3].set_color(GOLD)
        xt[7].set_color(YELLOW)
        xt.move_to([COLX + 0.2, -0.05, 0], aligned_edge=LEFT)
        box = SurroundingRectangle(xt, color=YELLOW, buff=0.16).set_stroke(YELLOW, 3)
        self.xt, self.xbox = xt, box
        self.xtag = kit.tag("notes p. 109").next_to(box, DOWN, buff=0.12).align_to(box, RIGHT)
        self.wt = ak.wt_readout(self.t, omega=OMEGA)
        self.wt.move_to([-kit.EDGE_X + 0.1, O[1] + EXT * U - 0.1, 0], aligned_edge=LEFT)
        self.br2 = self.br.copy()
        self.brl2 = _bs(kit._t("half the amplitude", 26, FG)).next_to(self.br2, UP, buff=0.08)
        with self.say("c4.faded.4") as c:
            dy = top_y - self.ar2.get_center()[1]
            gone = [self.gen, self.f1, self.f2, self.ftag, self.br, self.brl]
            self.play(*during(disappear(*gone), 0, 0.45), *during(set_alpha([self.lr, *self.lls, self.cr], 0.4), 0, 0.45),
                      *during([self.ar2.animate.shift(dy * UP)], 0.4, 1.0), run_time=1.4)
            c.wait_until("amplitude")
            self.play(*appear(amp, shift=None), FlashAround(self.gl, color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("phase")
            self.play(*appear(ph, shift=None), FlashAround(self.argl, color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("displacement")
            self.play(*appear(xt, shift=None), FadeIn(box), *appear(self.xtag, shift=None), run_time=1.4)
            c.wait_until("go")
            self.play(*disappear(*self.legs, self.pl, self.gl, self.arc, self.argl, self.cpos),
                      *appear(self.wt, shift=None), self.drop_op.animate.set_value(1.0), run_time=0.6)
            self.play(self.t.animate.set_value(TAU / OMEGA), run_time=max(0.8, c.until("half") - 0.05),
                      rate_func=linear)
            self.t.set_value(0.0)
            c.wait_until("half")
            self.play(GrowFromCenter(self.br2), *appear(self.brl2), run_time=1.0)
            c.wait_until("moves outward")
            self.play(self.t.animate.set_value(0.16), run_time=1.4, rate_func=linear)
            c.wait_until("vel")
            A = AMP
            vel = 1j * OMEGA * A
            tip = P(A)
            vend = tip + F * np.array([vel.real, vel.imag, 0])
            self.green = ak.arrow_between(tip, vend, GREEN, 6, -2)
            d = -np.array([A.real, A.imag, 0]) / abs(A)
            v = np.array([vel.real, vel.imag, 0]) / abs(vel)
            s = 0.17
            self.rang = VMobject().set_points_as_corners([tip + s * d, tip + s * (d + v), tip + s * v])
            self.rang.set_stroke(FG, 2.5).set_z_index(Z_MARK)
            self.vlab = _bs(MathTex(r"i\omega A\ \ (+30^\circ)", font_size=28, color=GREEN))
            self.vlab.move_to(tip + np.array([-0.15, -0.3, 0]), aligned_edge=RIGHT)
            self.vdrop = DashedLine(vend, [vend[0], PUSH_Y, 0], dash_length=0.08).set_stroke(DIM, 2)
            self.play(self.t.animate.set_value(0.0), *disappear(self.br2, self.brl2), run_time=0.9)
            self.play(*during([GrowArrow(self.green), FadeIn(self.rang)], 0, 0.7),
                      *during(appear(self.vlab), 0.4, 1), run_time=1.5)
            self.plab.add_updater(lambda m: m.move_to([P(self.weight_x())[0] + 0.1, PUSH_Y + 0.32, 0],
                                                      aligned_edge=LEFT))
            c.wait_until("shadow is exactly")
            self.play(Create(self.vdrop), self.push_op.animate.set_value(1.0), *appear(self.plab),
                      run_time=min(1.4, max(0.6, c.until("root three"))))
            self.play(FlashAround(self.plab, color=GREEN, time_width=1.5), run_time=min(1.2, max(0.5, c.until())))

    # ── clip 5: the side panel ──
    def clip5(self):
        top, bot, left, right = -0.6, -kit.EDGE_Y, -0.2, kit.EDGE_X
        panel = RoundedRectangle(corner_radius=0.12, width=right - left, height=top - bot)
        panel.set_stroke(DIM, 1.5).set_fill(kit.CARD_FILL, 0.95).move_to([(left + right) / 2, (top + bot) / 2, 0])
        split = right - 2.75
        divider = DashedLine([split, top - 0.2, 0], [split, bot + 0.2, 0], dash_length=0.08).set_stroke(DIM, 1.5)
        h1 = kit._t("With sines and cosines", 24, FG).move_to([left + 0.25, top - 0.3, 0], aligned_edge=UL)
        h2 = VGroup(kit._t("With the complex", 24, FG), kit._t("amplitude", 24, FG)).arrange(
            DOWN, buff=0.1, aligned_edge=LEFT).move_to([split + 0.25, top - 0.3, 0], aligned_edge=UL)
        rtag = kit.tag("reference").move_to([left + 0.05, top + 0.12, 0], aligned_edge=DL)
        ab1 = MathTex("a", "=", "c", ",", font_size=30)
        ab1[2].set_color(BLUE)
        ab1.move_to([left + 0.3, top - 0.9, 0], aligned_edge=LEFT)
        ab2 = MathTex("b", "=", r"\sqrt{3}\,c", font_size=30)
        ab2[2].set_color(BLUE)
        ab2.next_to(ab1, RIGHT, buff=0.45).align_to(ab1, DOWN)
        note = MathTex(r"\text{part two: }x(0) = a,\ \dot x(0) = b\,\omega", font_size=25, color=DIM)
        note.move_to([left + 0.3, top - 1.35, 0], aligned_edge=LEFT)
        id1 = MathTex(r"c\cos\omega t + \sqrt{3}\,c\sin\omega t", font_size=28)
        id1.move_to([left + 0.3, top - 1.75, 0], aligned_edge=LEFT)
        id2 = MathTex("=", r"2c\cos(\omega t - \pi/3)", font_size=28)
        id2.move_to([left + 0.95, top - 2.5, 0], aligned_edge=LEFT)
        idl = place([lab("trig identity")], id2, [0], right=split - 0.15, up=0.2)
        cA = MathTex("A", "=", "2c", r"\,e^{-i\pi/3}", font_size=36)
        cA[0].set_color(GOLD)
        cA[2].set_color(GOLD)
        cA[3].set_color(GOLD)
        cA[3][1:].set_color(YELLOW)
        cA.move_to([split + 0.3, top - 1.3, 0], aligned_edge=LEFT)
        u1 = underline(cA[2], GOLD, buff=0.1)
        u2 = underline(cA[3][1:], YELLOW, buff=0.1)
        t1 = VGroup(MathTex("2c", font_size=28, color=GOLD), kit.tag("amplitude")).arrange(RIGHT, buff=0.15)
        t2 = VGroup(MathTex(r"-\pi/3", font_size=28, color=YELLOW), kit.tag("phase")).arrange(RIGHT, buff=0.15)
        t1.move_to([split + 0.3, top - 1.95, 0], aligned_edge=LEFT)
        t2.move_to([split + 0.3, top - 2.4, 0], aligned_edge=LEFT)
        leftcol = [h1, ab1, ab2, note, id1, id2, *idl]
        with self.say("c4.faded.5") as c:
            self.play(*disappear(self.lr, *self.lls, self.cr), run_time=0.6)
            self.play(FadeIn(panel), Create(divider), *appear(h1, h2, rtag, shift=None, lag=0.3),  # early: the panel's two column heads, shown whole
                      *set_alpha([self.amp, self.ph], 0.6), run_time=1.3)
            c.wait_until("cosine coefficient")
            self.play(*appear(ab1, shift=None), run_time=0.9)
            c.wait_until("sine coefficient")
            self.play(*appear(ab2, note, shift=None, lag=0.4), run_time=1.1)
            c.wait_until("trig identity")
            self.play(*appear(id1, idl[0], id2, shift=None, lag=0.4), run_time=1.5)
            c.wait_until("glow")
            self.play(*appear(cA, shift=None), *set_alpha(leftcol, 0.45), run_time=1.2)
            c.wait_until("length")
            self.play(Create(u1), *appear(t1, shift=None), run_time=0.9)
            c.wait_until("angle")
            self.play(Create(u2), *appear(t2, shift=None), run_time=0.9)
            self.play(FlashAround(VGroup(cA, t1, t2), color=GOLD, time_width=1.5, buff=0.2),
                      run_time=min(1.4, max(0.5, c.until())))
