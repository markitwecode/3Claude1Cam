"""Chapter 7, scene 3: G2, the two loci (ellipse and one-branch hyperbola). Clips c7.g2.1 – c7.g2.5.

Card G2 grows out of the row, its three lines lit in turn, pause icon. Then the screen splits:
"i." left (x/a = cos, y/b = sin -> ellipse, circle ghost, running point, direction flip),
"ii." right (x/a = cosh, y/b = sinh -> hyperbola; x/a >= 1 so one branch only, a < 0 the other).
Finally the two-branch Cartesian sketch (extra branch RED) replaces part i on the left, with
x = ±s cosh θ, y = s sinh θ.

Shared with s6 (recap), built at `center`:
  ellipse_sketch(center=ORIGIN)    BLUE ellipse (a = 2, b = 1, unit UE), axes, YELLOW centre,
                                   GOLD |a|, GREEN |b|, running point .point at θ = 0
  hyperbola_sketch(center=ORIGIN)  x²/4 − y² = 1 (unit UH): right branch solid TEAL, left dashed,
                                   RED ✗ on the left branch (.cross)
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

UE, UH = 1.2, 0.65                       # world units per maths unit: ellipse, hyperbola
LX, RX = -3.55, 3.55                     # panel centres
HEAD_Y, L1_Y, L2_Y, L3_Y, SK_Y = 3.3, 2.55, 1.6, 0.6, -1.75
E_C = np.array([LX, SK_Y, 0.0])
H_C = np.array([RX, SK_Y, 0.0])
TM = float(np.arccosh(2.25))             # branch drawn for |x| <= 4.5
X_TH = 0.8                               # where the ✗ sits on a branch


def _axes(center, xr, yr, unit):
    center = np.array(center, dtype=float)
    return VGroup(Line(center + LEFT * xr * unit, center + RIGHT * xr * unit),
                  Line(center + DOWN * yr * unit, center + UP * yr * unit)).set_stroke(DIM, 2)


def ell_pt(th, a=2, b=1, center=E_C):
    return np.array(center, dtype=float) + UE * np.array([a * np.cos(th), b * np.sin(th), 0])


def hyp_pt(t, a=2, b=1, center=H_C):
    return np.array(center, dtype=float) + UH * np.array([a * np.cosh(t), b * np.sinh(t), 0])


def hyp_branch(sign, center=H_C, t1=TM, color=TEAL, width=4):
    return ParametricFunction(lambda t: hyp_pt(t, 2 * sign, 1, center),
                              t_range=[-TM, t1, 0.02]).set_stroke(color, width)


def dashed_branch(sign, center=H_C):
    return DashedVMobject(hyp_branch(sign, center, width=3), num_dashes=22,
                          dashed_ratio=0.55).set_stroke(TEAL, 3, opacity=0.55)


def ellipse_sketch(center=ORIGIN):
    center = np.array(center, dtype=float)
    g = VGroup()
    g.axes = _axes(center, 2.5, 1.3, UE)
    g.curve = Ellipse(width=4 * UE, height=2 * UE).move_to(center).set_stroke(BLUE, 4)
    g.centre = Dot(center, radius=0.09, color=YELLOW)
    g.major = Line(center, center + 2 * UE * RIGHT).set_stroke(GOLD, 5)
    g.minor = Line(center, center + UE * UP).set_stroke(GREEN, 5)
    g.la = MathTex(r"|a|", font_size=36, color=GOLD).move_to(center + UE * RIGHT + 0.32 * DOWN)
    g.lb = MathTex(r"|b|", font_size=36, color=GREEN).move_to(center + 0.5 * UE * UP + 0.42 * LEFT)
    g.point = Dot(ell_pt(0, center=center), radius=0.12, color=FG).set_stroke(BLUE, 2)
    g.add(g.axes, g.curve, g.major, g.minor, g.centre, g.la, g.lb, g.point)
    return g


def hyperbola_sketch(center=ORIGIN):
    center = np.array(center, dtype=float)
    g = VGroup()
    g.axes = _axes(center, 4.7, 2.0, UH)
    g.left = dashed_branch(-1, center)
    g.right = hyp_branch(1, center)
    g.cross = cross_mark(RED).scale(0.8).move_to(hyp_pt(X_TH, -2, 1, center))
    g.add(g.axes, g.left, g.right, g.cross)
    return g


def _ex(a):
    return MathTex(rf"a = {a},\ b = 1", font_size=34, color=DIM)


class G2Loci(NarratedScene):
    def construct(self):
        s1 = load_scene("ch7_s1_intro")
        row = s1.card_row(lit=True)
        self.play(FadeIn(row), run_time=0.6)  # early: the inherited card row (opening shared with s2-s5)
        self.clip1(s1, row)
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- card
    def clip1(self, s1, row):
        with self.say("c7.g2.1") as c:
            hero = s1.g_card(2).scale_to_fit_height(4.5).move_to([-1.5, 0.3, 0])
            for ln in hero.body:
                ln.set_opacity(0.3)
            self.play(Transform(row[1], hero), *[FadeOut(row[k]) for k in (0, 2, 3)], run_time=1.5)
            self.remove(*row[1].get_family())
            self.add(hero)
            self.hero = hero
            for k, cue in enumerate(["A point has", "part2", "task"]):
                c.wait_until(cue)
                ln = hero.body[k]
                self.play(*set_alpha([ln], 1), FlashAround(ln, color=YELLOW, time_width=1.5), run_time=1.5)  # early: the card's own line, lit as it is read
            c.wait_until("stop")
            self.pause = s1.pause_icon(height=1.2).move_to([4.5, 0.3, 0])
            self.play(FadeIn(self.pause), run_time=0.8)

    # ---------------------------------------------------------------- part i
    def clip2(self):
        with self.say("c7.g2.2") as c:
            self.headL = T("i.", 40).move_to([LX - 2.8, HEAD_Y, 0])
            given = MathTex(r"x = a\cos\theta,\quad y = b\sin\theta", font_size=48,
                            color=BLUE).move_to([LX, L1_Y, 0])
            sweep_clear(self, *appear(self.headL, given, lag=0.3))
            c.wait_until("Divide ex by A")
            self.divL = MathTex(r"\frac{x}{a} = \cos\theta,\quad \frac{y}{b} = \sin\theta",
                                font_size=48, color=BLUE).move_to([LX, L1_Y, 0])
            self.play(*edit(given, self.divL), run_time=min(1.8, c.until("sq")))
            c.wait_until("sq")
            self.idL = MathTex(r"\cos^2\theta + \sin^2\theta = 1", font_size=42).move_to([LX, L2_Y, 0])
            self.play(*appear(self.idL), run_time=1.0)
            c.wait_until("so ex over A")
            self.resL = MathTex(r"\left(\frac{x}{a}\right)^2 + \left(\frac{y}{b}\right)^2 = 1",
                                font_size=48).move_to([LX, L3_Y, 0])
            self.boxL = SurroundingRectangle(self.resL, color=BLUE, buff=0.1)
            self.play(*appear(self.resL, shift=None), run_time=1.0)
            self.play(FadeIn(self.boxL), run_time=0.8)

            c.wait_until("ellipse")
            es = ellipse_sketch(E_C)
            self.es = es
            self.exL = _ex(2).move_to([LX + 2.1, HEAD_Y, 0])
            self.play(FadeIn(es.axes), Create(es.curve), FadeIn(es.centre), *appear(self.exL),
                      run_time=1.8)
            c.wait_until("reaching out to mod A")
            self.play(Create(es.major), *appear(es.la), run_time=1.2)
            c.wait_until("and to mod B")
            self.play(Create(es.minor), *appear(es.lb), run_time=1.2)

            c.wait_until("circle")
            ghost = es.curve.copy().set_stroke(BLUE, 3, opacity=0.5)
            self.add(ghost)
            circ = Circle(radius=1.5 * UE).move_to(E_C).set_stroke(BLUE, 3, opacity=0.5)
            self.play(Transform(ghost, circ), run_time=1.0)
            self.wait(0.4)
            self.play(Transform(ghost, es.curve.copy().set_stroke(BLUE, 3, opacity=0.5)), run_time=1.0)
            self.remove(ghost)

            c.wait_until("all")
            th = ValueTracker(0)
            pt = es.point
            self.play(FadeIn(pt, scale=0.5), run_time=0.4)
            pt.add_updater(lambda d: d.move_to(ell_pt(th.get_value())))
            self.play(th.animate.set_value(TAU), rate_func=linear,
                      run_time=max(1.0, min(2.6, c.until("signs") - 0.1)))
            pt.clear_updaters()

            c.wait_until("signs")
            exN = _ex(-2).move_to(self.exL)
            self.play(*swap(self.exL, exN), pt.animate.move_to(ell_pt(0, -2)), run_time=1.0)
            self.exL = exN
            th.set_value(0)
            pt.add_updater(lambda d: d.move_to(ell_pt(th.get_value(), -2)))
            self.play(th.animate.set_value(TAU), rate_func=linear,
                      run_time=max(1.0, min(2.5, c.until() - 0.05)))
            pt.clear_updaters()

    # ---------------------------------------------------------------- part ii
    def clip3(self):
        with self.say("c7.g2.3") as c:
            es = self.es
            self.left = [self.headL, self.exL, self.divL, self.idL, self.resL, self.boxL,
                         es.axes, es.curve, es.major, es.minor, es.centre, es.la, es.lb, es.point]
            self.divider = Line([0, 3.5, 0], [0, -3.5, 0]).set_stroke(DIM, 2, opacity=0.5)
            self.headR = T("ii.", 40).move_to([RX - 2.8, HEAD_Y, 0])
            self.exR = _ex(2).move_to([RX + 2.1, HEAD_Y, 0])
            self.divR = MathTex(r"\frac{x}{a} = \cosh\theta,", r"\quad \frac{y}{b} = \sinh\theta",
                                font_size=48, color=TEAL).move_to([RX, L1_Y, 0])
            self.play(*set_alpha(self.left, 0.4), FadeIn(self.divider), run_time=0.8)
            self.play(*appear(self.headR, self.divR, lag=0.3), run_time=1.2)
            c.wait_until("identity")
            self.idR = MathTex(r"\cosh^2\theta - \sinh^2\theta = 1", font_size=42).move_to([RX, L2_Y, 0])
            self.play(*appear(self.idR), run_time=1.0)
            c.wait_until("gives ex over A")
            self.resR = MathTex(r"\left(\frac{x}{a}\right)^2 - \left(\frac{y}{b}\right)^2 = 1",
                                font_size=48).move_to([RX, L3_Y, 0])
            self.boxR = SurroundingRectangle(self.resR, color=TEAL, buff=0.1)
            self.play(*appear(self.resR, shift=None), run_time=1.0)
            self.play(FadeIn(self.boxR), run_time=0.8)

            c.wait_until("hyperbola")
            self.h_axes = _axes(H_C, 4.7, 2.0, UH)
            self.dL, self.dR = dashed_branch(-1), dashed_branch(1)
            self.play(FadeIn(self.h_axes), Create(self.dL), Create(self.dR), *appear(self.exR),
                      run_time=1.6)
            vs = [Dot(hyp_pt(0, s * 2), radius=0.08, color=GOLD) for s in (-1, 1)]
            vl = [MathTex(t, font_size=30, color=GOLD).move_to(hyp_pt(0, s * 2) + 0.42 * s * LEFT
                                                                 + 0.3 * DOWN)
                  for s, t in ((-1, "-2"), (1, "2"))]
            self.verts = vs + vl
            self.play(*[FadeIn(v) for v in vs], *appear(*vl), run_time=1.0)
            c.wait_until("ask")

    # ---------------------------------------------------------------- one branch
    def _run(self, sign, color, rt):
        tr = ValueTracker(-TM)
        dot = Dot(hyp_pt(-TM, 2 * sign), radius=0.12, color=color)
        trail = always_redraw(lambda: hyp_branch(sign, t1=max(tr.get_value(), -TM + 0.03),
                                                 color=color))
        self.add(trail)
        self.play(FadeIn(dot, scale=0.5), run_time=0.3)
        dot.add_updater(lambda d: d.move_to(hyp_pt(tr.get_value(), 2 * sign)))
        self.play(tr.animate.set_value(TM), rate_func=linear, run_time=rt)
        dot.clear_updaters()
        self.remove(trail)
        solid = hyp_branch(sign, color=color)
        self.add(solid)
        return solid, dot

    def _never(self, sign):
        p = hyp_pt(X_TH, 2 * sign)
        return p, np.array([p[0] - 0.3 * sign, SK_Y + 1.35, 0])

    def clip4(self):
        with self.say("c7.g2.4") as c:
            self.play(FlashAround(self.divR[0], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("It's cosh of theta")
            catch = MathTex(r"x/a = \cosh\theta \ge 1", font_size=44,
                            color=YELLOW).move_to([RX, L2_Y, 0])
            self.play(*swap(self.idR, catch), run_time=1.2)
            self.catch = catch
            c.wait_until("sign")
            sign_t = MathTex(r"x \text{ has the sign of } a,\quad |x| \ge |a|",
                             font_size=36).move_to([RX, -3.3, 0])
            self.play(*appear(sign_t), run_time=1.0)

            c.wait_until("right")
            solidR, dot = self._run(1, TEAL, rt=min(2.0, max(1.0, c.until("flip") - 1.5)))
            p, lp = self._never(-1)
            cross = cross_mark(RED).scale(0.8).move_to(p)
            never = set_backstroke(T("never reached", 28, color=RED)).move_to(lp)
            self.play(FadeOut(dot), FadeIn(cross, scale=0.6), *appear(never),  # early: names the ✗ ("never reaches" comes at the clip's end)
                      run_time=min(0.9, max(0.4, c.until("flip"))))

            c.wait_until("flip")
            ex2 = _ex(-2).move_to(self.exR)
            q, lq = self._never(1)
            self.play(*swap(self.exR, ex2), cross.animate.move_to(q), never.animate.move_to(lq),
                      FadeOut(solidR), run_time=1.0)
            solidL, pdot = self._run(-1, PURPLE, rt=min(1.6, max(0.8, c.until("whole") - 0.4)))
            self.play(FadeOut(pdot), run_time=0.3)

            c.wait_until("whole")
            y_t = MathTex(r"y = b\sinh\theta \text{ takes every real value}",
                          font_size=36).move_to(sign_t)
            arrow = DoubleArrow(H_C + 1.25 * DOWN, H_C + 1.25 * UP, buff=0, color=YELLOW,
                                stroke_width=5, tip_length=0.22)
            self.play(*swap(sign_t, y_t), GrowFromCenter(arrow), run_time=1.5)
            self.y_t = y_t

            c.wait_until("So the point runs along")
            ex3 = _ex(2).move_to(self.exR)
            self.solidR = hyp_branch(1)
            self.play(*swap(ex2, ex3), FadeOut(solidL), FadeIn(self.solidR), FadeOut(arrow),
                      cross.animate.move_to(p), never.animate.move_to(lp),
                      run_time=min(1.5, c.until()))
            self.exR, self.cross, self.never = ex3, cross, never

    # ---------------------------------------------------------------- the sketch
    def clip5(self):
        with self.say("c7.g2.5", gap=4.0) as c:
            asy = VGroup(*[DashedLine(H_C + UH * np.array([-4.6, -2.3 * s, 0]),
                                      H_C + UH * np.array([4.6, 2.3 * s, 0]),
                                      dash_length=0.12).set_stroke(FG, 2, opacity=0.5)
                           for s in (1, -1)])
            self.play(Create(asy[0]), Create(asy[1]), run_time=1.5)

            c.wait_until("slip")
            self.play(*disappear(*self.left), run_time=0.8)
            c_axes = _axes(E_C, 4.7, 2.0, UH)
            c_r = hyp_branch(1, center=E_C)
            c_l = hyp_branch(-1, center=E_C, color=RED)
            # shift the Cartesian sketch so its maths origin sits at the left panel centre
            resC = MathTex(r"\left(\frac{x}{a}\right)^2 - \left(\frac{y}{b}\right)^2 = 1",
                           font_size=48).move_to([LX, L3_Y, 0])
            self.play(FadeIn(resC, shift=0.2 * DOWN), FlashAround(self.resR, color=YELLOW, time_width=1.5), FadeIn(c_axes), Create(c_r), Create(c_l), run_time=1.6)

            c.wait_until("pm")
            self.play(VShowPassingFlash(self.solidR.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.2)
            c.wait_until("In part six")
            pm = MathTex(r"x = ", r"\pm", r"s\cosh\theta,\quad y = s\sinh\theta",
                         font_size=48).move_to([LX, L1_Y, 0])
            pm[1].set_color(YELLOW)
            note = T("Each sign gives one branch", 30).move_to([LX, L2_Y, 0])
            self.play(*appear(pm, note, lag=0.5), run_time=1.6)  # early: the notes' line, read with the formula
