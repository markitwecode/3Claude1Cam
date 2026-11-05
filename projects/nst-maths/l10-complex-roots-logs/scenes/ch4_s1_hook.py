"""Chapter 4, scene 1: hook: run the exponential backwards; e^x = 2 has one answer, e^w = 2i? Clips c4.hook.1 – c4.hook.3."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

U = 1.0                        # screen units per plane unit (right-half Argand plane)
O = np.array([3.4, -1.5, 0])   # plane origin on screen


def P(x, y):
    return O + U * np.array([x, y, 0])


def argand_plane(xr=(-2.2, 2.2), yr=(-0.9, 2.3)):
    """Re/Im axes, faint grid, DIM unit circle (look copied from ch2_s1_hook)."""
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(P(x, yr[0]), P(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(P(xr[0], y), P(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0), P(xr[1] + 0.2, 0), buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0]), P(0, yr[1] + 0.2), buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    re = T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    unit = Circle(radius=U, color=DIM, stroke_width=2).move_to(O)
    return VGroup(grid, xax, yax, re, im, unit)


def curling_chain(origin, s=0.75, theta=0.55, n=5):
    """ch3 s3's look: GOLD unit arrows e^{ik theta} head to tail, BLUE shadow on the real axis."""
    pts = [np.array(origin, dtype=float)]
    for k in range(n):
        pts.append(pts[-1] + s * np.array([np.cos(k * theta), np.sin(k * theta), 0]))
    axis = Line(pts[0] + 0.4 * LEFT, pts[0] + (s * 2.4) * RIGHT, stroke_width=2, color=DIM)
    arrows = VGroup(*[Arrow(pts[k], pts[k + 1], buff=0, color=GOLD, stroke_width=4,
                            max_tip_length_to_length_ratio=0.22) for k in range(n)])
    shadow = Line(pts[0], np.array([pts[-1][0], pts[0][1], 0]), stroke_width=7, color=BLUE)
    drop = DashedLine(pts[-1], np.array([pts[-1][0], pts[0][1], 0]), color=BLUE, stroke_width=2,
                      dash_length=0.08)
    return VGroup(axis, shadow, drop, arrows)


class Hook(NarratedScene):
    def construct(self):
        # ---------------- clip 1: title, last time, run it backwards
        # silent lead-in: the title card is built and read before the voice starts
        card = title_card("Part 4 · The complex logarithm")
        card.title.scale_to_fit_width(12.4)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
        self.play(*appear(card.course, card.part, lag=0.3), run_time=1.0)  # early: title card
        self.wait(2.6)  # silent hold on the card before the first line (not a sync wait)
        with self.say("c4.hook.1", gap=0.8) as c:
            c.wait_until("last")

            last = T("Last time", size=32, color=DIM).move_to([-5.6, 3.4, 0])
            chain = curling_chain([-4.6, -0.5, 0], s=1.1)
            ident = MathTex(r"\cos^3\theta", "=", r"\tfrac14\cos 3\theta", "+", r"\tfrac34\cos\theta",
                            font_size=48).move_to([2.0, 1.3, 0])
            sweep_clear(self, *appear(last), FadeIn(chain), run_time=1.4)
            self.play(*appear(ident), run_time=1.0)  # early: last time panel, shown whole

            wdot = Dot([-2.4, -1.9, 0], radius=0.1, color=FG)
            zdot = Dot([2.4, -1.9, 0], radius=0.1, color=FG)
            wl = MathTex("w", font_size=48).next_to(wdot, DOWN, buff=0.2)
            zl = MathTex("z", font_size=48).next_to(zdot, DOWN, buff=0.2)
            arr = Arrow(wdot.get_center(), zdot.get_center(), buff=0.22, color=GOLD, stroke_width=6,
                        max_tip_length_to_length_ratio=0.08)
            el = MathTex("e^w", font_size=48, color=GOLD).next_to(arr, UP, buff=0.2)
            self.play(FadeIn(wdot), FadeIn(zdot), *appear(wl, zl, lag=0.1), run_time=0.8)
            self.play(GrowArrow(arr), *appear(el), run_time=1.0)
            c.wait_until("back")
            self.play(*set_alpha([last, chain, ident], 0.4),
                      Rotate(arr, PI, axis=UP), run_time=min(1.6, c.until(floor=0.5)))

        # ---------------- clip 2: real case, then the complex one
        with self.say("c4.hook.2") as c:
            nl = NumberLine(x_range=[-1, 2, 1], length=5.1, color=FG, stroke_width=2.5,
                            include_tip=False).move_to([-3.6, -1.5, 0])
            nums = VGroup(*[MathTex(str(v), font_size=32).next_to(nl.n2p(v), DOWN, buff=0.2)
                            for v in (-1, 0, 1, 2)])
            eq1 = MathTex("e^x", "=", "2", font_size=52).move_to([-3.6, 1.6, 0])
            eq2 = MathTex("x", "=", r"\ln 2", r"\approx", "0.693", font_size=52).move_to([-3.6, 0.5, 0])
            eq2[4].set_color(BLUE)
            sweep_clear(self, FadeIn(nl), *appear(*nums, lag=0.1), run_time=1.4)
            self.play(*appear(eq1), run_time=1.0)
            try:
                c.wait_until("log two")
            except KeyError:
                pass  # line re-voiced without the phrase: answer follows the equation
            rdot = Dot(nl.n2p(np.log(2)), radius=0.13, color=BLUE)
            self.play(*appear(eq2), run_time=1.2)
            self.play(FadeIn(rdot, scale=0.5), run_time=0.8)
            self.play(FlashAround(rdot, run_time=1.2, time_width=1.5, color=BLUE))
            c.wait_until("plane")

            divider = Line([0.0, 2.6, 0], [0.0, -2.2, 0], stroke_width=1.5, color=DIM, stroke_opacity=0.5)
            plane = argand_plane()
            zdot2 = Dot(P(0, 2), radius=0.12, color=YELLOW)
            zlab = MathTex("2i", font_size=44, color=YELLOW).next_to(zdot2, LEFT, buff=0.2)
            self.play(*set_alpha([nl, nums, eq1, eq2, rdot], 0.4), FadeIn(divider), FadeIn(plane),
                      run_time=1.4)
            self.play(FadeIn(zdot2, scale=0.5), *appear(zlab), run_time=1.0)
            c.wait_until("ask")

            q1 = MathTex("e^w", "=", "2i", font_size=52).move_to([3.4, 3.1, 0])
            q1[2].set_color(YELLOW)
            q2 = MathTex("w", "=", r"\mathord{?}", font_size=52).move_to([3.4, 2.15, 0])
            q2[2].set_color(YELLOW)
            self.play(*appear(q1), run_time=1.2)
            self.play(*appear(q2), run_time=1.0)
            c.wait_until("many")
            qm = q2[2]
            self.play(FlashAround(qm, run_time=1.4, time_width=1.5),
                      qm.animate(rate_func=there_and_back, run_time=1.4).scale(1.5))
            self.play(FlashAround(qm, run_time=1.2, time_width=1.5),
                      qm.animate(rate_func=there_and_back, run_time=1.2).scale(1.4))

        # ---------------- clip 3: the definition, and her words
        with self.say("c4.hook.3", gap=2.5) as c:
            upper = VGroup(nl, nums, eq1, eq2, rdot, divider, plane, zdot2, zlab, q1, q2)
            defn = MathTex("w", "=", r"\ln z", r"\quad\text{if}\quad", "e^w", "=", "z", font_size=56)
            defn[2].set_color(YELLOW)
            defn.move_to([0, -1.85, 0])
            upper.generate_target()
            upper.target.scale(0.8, about_point=np.array([0, 3.6, 0]))
            for lab in [*upper.target[1], upper.target[6][3], upper.target[6][4]]:
                lab.scale(1.25)   # tick numbers, Re, Im stay at readable size
            self.play(MoveToTarget(upper), run_time=1.2)
            self.play(FadeIn(defn, shift=0.4 * UP), run_time=1.2)
            c.wait_until("quote")
            quote = T("“each time you see the logarithm,\nyou have to go through this definition”",
                      size=32, slant=ITALIC, line_spacing=1.0).move_to([0, -2.95, 0])
            self.play(*appear(quote), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
