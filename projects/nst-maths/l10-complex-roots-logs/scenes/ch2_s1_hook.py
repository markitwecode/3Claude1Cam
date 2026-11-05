"""Chapter 2, scene 1: hook: from the ring of five to cos 4θ and one power. Clips c2.hook.1 – c2.hook.2."""
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

U = 1.2                      # screen units per plane unit
O = np.array([-3.4, -0.6, 0])  # plane origin on screen
R5 = 2 ** 0.2                # radius of the ring of five


def P(x, y):
    return O + U * np.array([x, y, 0])


def argand_plane(xr=(-2.0, 2.0), yr=(-1.6, 2.5)):
    """Re/Im axes, faint grid, DIM unit circle (PLAN.md running visual)."""
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


def ring_of_five():
    circ = DashedVMobject(Circle(radius=U * R5, color=GOLD, stroke_width=3).move_to(O), num_dashes=40)
    dots = VGroup()
    for k in range(5):
        a = PI / 10 + 2 * PI * k / 5
        dots.add(Dot(P(R5 * np.cos(a), R5 * np.sin(a)), radius=0.11, color=GREEN if k == 0 else TEAL))
    return circ, dots


class Hook(NarratedScene):
    def construct(self):
        # ---------------- clip 1
        with self.say("c2.hook.1") as c:
            card = title_card("Part 2 · De Moivre's theorem")
            card.title.scale_to_fit_width(12.4)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.2)
            self.play(*appear(card.course), run_time=1.0)  # early: title card
            self.play(*appear(card.part), run_time=1.0)  # early: title card
            c.wait_until("ring")

            plane = argand_plane()
            circ, dots = ring_of_five()
            label = MathTex("z^5 =", "2i", font_size=60)
            label[1].set_color(YELLOW)
            label.move_to([3.4, 1.9, 0])
            sweep_clear(self, FadeIn(plane), FadeIn(circ), run_time=1.4)
            self.play(*appear(*dots, lag=0.15), *appear(label), run_time=1.2)
            c.wait_until("turns")

            # the first root: arrow and its angle arc
            t = ValueTracker(1)

            def arrow_at():
                k = t.get_value()
                a, r = k * PI / 10, 2 ** (k / 5)
                return Arrow(O, P(r * np.cos(a), r * np.sin(a)), buff=0, color=GOLD, stroke_width=5,
                             max_tip_length_to_length_ratio=0.12)

            arrow = always_redraw(arrow_at)
            arcs = [Arc(radius=0.55, start_angle=k * PI / 10, angle=PI / 10, arc_center=O,
                        color=YELLOW, stroke_width=5) for k in range(5)]
            arrow0 = arrow_at()
            self.play(GrowArrow(arrow0), Create(arcs[0]), run_time=1.0)
            self.remove(arrow0)
            self.add(arrow)
            caption = T("multiplying adds angles", size=36).move_to([O[0], -3.3, 0])
            self.play(*appear(caption), run_time=1.0)
            c.wait_until("adds their angles")

            eq = MathTex(r"5 \times \tfrac{\pi}{10} = \tfrac{\pi}{2}", font_size=54).move_to([3.4, 0.4, 0])
            tip = MathTex("2i", font_size=40, color=YELLOW).next_to(P(0, 2), LEFT, buff=0.2)
            rt = min(3.5, max(1.5, c.until("so a fifth power") + 1.0))
            self.play(t.animate.set_value(5),
                      LaggedStart(*[ReplacementTransform(arcs[0].copy(), arcs[k], path_arc=k * PI / 10)
                                    for k in range(1, 5)], lag_ratio=0.25),
                      *during(appear(eq), 0.3, 0.75), *during(appear(tip), 0.8, 1),
                      run_time=rt, rate_func=linear)

        # ---------------- clip 2
        with self.say("c2.hook.2") as c:
            arrow.clear_updaters()
            final_arrow = arrow_at()
            self.remove(arrow)
            self.add(final_arrow)
            left_side = VGroup(plane, circ, *dots, final_arrow, *arcs, tip)
            q = MathTex(r"\cos 4\theta =", r"\mathord{?}", font_size=84)
            q[1].set_color(YELLOW)
            q.move_to([0, 0.5, 0])
            self.play(*during(disappear(label, eq, caption), 0, 0.4),
                      *during([left_side.animate.shift(9 * LEFT)], 0, 0.7),
                      *during(appear(q), 0.5, 1),
                      run_time=1.8)
            self.remove(*left_side.get_family())
            sub = MathTex(r"\text{in terms of }", r"\cos\theta", font_size=48)
            sub[1].set_color(BLUE)
            sub.next_to(q, DOWN, buff=0.6)
            c.wait_until("written using")
            self.play(*appear(sub), run_time=1.0)
            c.wait_until("long")

            # the double-angle route, at right
            qg = VGroup(q, sub)
            l1 = MathTex(r"\cos 4\theta = 2\cos^2 2\theta - 1", font_size=40)
            l2 = MathTex(r"= 2(2\cos^2\theta - 1)^2 - 1", font_size=40)
            l1.move_to([2.9, 2.9, 0])
            l2.next_to(l1, DOWN, buff=0.3).align_to(l1[0][6], LEFT)
            self.play(qg.animate.scale(0.75).move_to([-3.6, 0.3, 0]), run_time=1.2)
            self.play(*appear(l1), run_time=1.0)
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("seven")

            q7 = MathTex(r"\cos 7\theta =", r"\mathord{?}", font_size=44)
            q7[1].set_color(YELLOW)
            q7.next_to(l2, DOWN, buff=0.45).align_to(l1, LEFT)
            stack_src = [
                r"\cos(A+B) = \cos A\cos B - \sin A\sin B",
                r"\cos 7\theta = \cos 4\theta\cos 3\theta - \sin 4\theta\sin 3\theta",
                r"\cos 3\theta = \cos 2\theta\cos\theta - \sin 2\theta\sin\theta",
                r"\sin 4\theta = 2\sin 2\theta\cos 2\theta",
                r"\sin 3\theta = \sin 2\theta\cos\theta + \cos 2\theta\sin\theta",
            ]
            stack = VGroup(*[MathTex(s, font_size=32, color=DIM) for s in stack_src])
            stack.arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(q7, DOWN, buff=0.35).align_to(l1, LEFT)
            self.play(*appear(q7), run_time=0.9)
            self.play(*appear(*stack, lag=0.3), run_time=min(2.4, c.until("power", floor=1.0)))  # early: a pile, read as a mass
            c.wait_until("power")

            pw = MathTex("(", r"\cos\theta", "+", r"i\sin\theta", ")^4", font_size=80)
            pw[1].set_color(BLUE)
            pw[3].set_color(PINK)
            pw.move_to([0, 0.2, 0])
            box = SurroundingRectangle(pw, color=YELLOW, buff=0.3, stroke_width=4)
            self.play(*during(disappear(l1, l2, q7, *stack, qg), 0, 0.45),
                      *during(appear(pw), 0.5, 1), run_time=1.6)
            self.play(FadeIn(box), run_time=0.8)

        self.wait(1.0)   # let the one power sit before the topic changes
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
