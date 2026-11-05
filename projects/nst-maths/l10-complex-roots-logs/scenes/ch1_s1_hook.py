"""Chapter 1, scene 1: hook: x^5 = 32 on the line, z^5 = 2i in the plane, the road. Clips c1.hook.1 – c1.hook.3."""
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

# The Argand plane: origin on screen, unit length, half-extent of the axes.
O = np.array([-2.2, -0.4, 0.0])
U = 1.1
EXT = 3.3
LINE_U = 1.2                      # unit of the opening real number line
LINE_C = np.array([0.0, -0.4, 0.0])
ROAD = ["Roots", "De Moivre", "Sums of\ncosines", "Logarithms", "Powers", "Oscillations", "Circuits"]


def argand_plane(center=O, unit=U, extent=EXT):
    """PLAN.md's running Argand plane: faint grid, Re/Im axes, DIM unit circle."""
    step = unit / 2
    n = int(extent // step)
    grid = VGroup()
    for k in range(-n, n + 1):
        if k == 0:
            continue
        grid.add(Line(center + [k * step, -extent, 0], center + [k * step, extent, 0]))
        grid.add(Line(center + [-extent, k * step, 0], center + [extent, k * step, 0]))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(center + [-extent, 0, 0], center + [extent, 0, 0], **ax_kw).set_opacity(0.7)
    y_ax = Arrow(center + [0, -extent, 0], center + [0, extent, 0], **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=unit, color=DIM, stroke_width=2.5).move_to(center)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle = grid, VGroup(x_ax, y_ax), circle
    return g


def number_line():
    line = Line(LINE_C + 4.1 * LEFT, LINE_C + 4.1 * RIGHT, stroke_width=2.5, color=FG).set_opacity(0.7)
    ticks, nums = VGroup(), VGroup()
    for k in range(-3, 4):
        p = LINE_C + k * LINE_U * RIGHT
        ticks.add(Line(p + 0.12 * DOWN, p + 0.12 * UP, stroke_width=2.5, color=FG))
        nums.add(MathTex(str(k), font_size=40, color=DIM).next_to(p, DOWN, buff=0.3))
    return line, ticks, nums


def road_tile(i, name):
    color = YELLOW if i == 0 else DIM
    box = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.9)
    box.set_stroke(color, 3).set_fill(color, 0.15 if i == 0 else 0.0)
    num = T(str(i + 1), size=36, color=color).move_to(box)
    lab = T(name, size=28, color=FG if i == 0 else DIM, line_spacing=0.8).next_to(box, DOWN, buff=0.18)
    return VGroup(box, num, lab)


class Hook(NarratedScene):
    def construct(self):
        # ---------------- clip 1: title card
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Roots of a complex number")
            card.title.scale_to_fit_width(12.4)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.2)
            self.play(*appear(card.course), run_time=1.0)  # early: title card
            self.play(*appear(card.part), run_time=1.0)  # early: title card

        # ---------------- clip 2: the real line, then the plane
        with self.say("c1.hook.2") as c:
            line, ticks, nums = number_line()
            sweep_clear(self, FadeIn(line), FadeIn(ticks), FadeIn(nums), run_time=1.6)
            eq_r = MathTex("x^5", "=", "32", font_size=72).move_to([0, 1.5, 0])
            eq_r[2].set_color(GOLD)
            c.wait_until("which real number")
            self.play(*appear(eq_r), run_time=1.0)
            c.wait_until("two")

            dot2 = Dot(LINE_C + 2 * LINE_U * RIGHT, radius=0.12, color=GOLD)
            lab2 = MathTex("x = 2", font_size=44, color=GOLD).next_to(dot2, UP, buff=0.3)
            self.play(FadeIn(dot2, shift=0.6 * DOWN), *during(appear(lab2), 0.4, 1.0), run_time=1.2)
            c.wait_until("plane")

            plane = argand_plane()
            x_ax, y_ax = plane.axes
            eq_c = MathTex("z^5", "=", "2i", font_size=72).move_to([4.2, 1.3, 0])
            eq_c[2].set_color(YELLOW)
            self.play(
                *during([FadeOut(ticks), FadeOut(nums)], 0, 0.4),
                *during([dot2.animate.move_to(O + 2 * U * RIGHT), lab2.animate.shift(O + 2 * U * RIGHT - dot2.get_center())], 0.15, 0.7),
                *during(ReplacementTransform(line, x_ax), 0.15, 0.7),
                *during([GrowArrow(y_ax), FadeIn(plane.grid), Create(plane.circle)], 0.35, 1.0),
                *during(appear(plane[4], plane[5], shift=None), 0.6, 1.0),
                *swap(eq_r, eq_c),
                run_time=min(2.4, c.until("point")))
            settle(self, plane)
            c.wait_until("point")

            p2i = Dot(O + 2 * U * UP, radius=0.12, color=YELLOW)
            l2i = MathTex("2i", font_size=48, color=YELLOW).next_to(p2i, RIGHT, buff=0.2)
            self.play(FadeIn(p2i, scale=0.5), FlashAround(eq_c[2], run_time=1.4, time_width=1.5), run_time=1.4)
            self.play(*appear(l2i), run_time=0.8)
            c.wait_until("which complex numbers")

            spots = [(2.6, 1.4), (-1.6, 1.9), (-2.5, -0.9), (0.7, -2.2), (2.1, -1.7), (-2.7, 1.1)]
            qs = VGroup(*[T("?", size=48, color=YELLOW).set_opacity(0.5).move_to(O + [x, y, 0]) for x, y in spots])
            self.play(*appear(*qs, shift=None, lag=0.3), run_time=min(2.2, c.until("how many")))  # early: scattered marks, not labels

        # ---------------- clip 3: definitions, names, the road
        with self.say("c1.hook.3") as c:
            dimmable = [plane.grid, x_ax, y_ax, plane.circle]
            self.play(*disappear(qs, l2i, p2i, dot2, lab2, plane[4], plane[5], eq_c),
                      *set_alpha(dimmable, 0.3), run_time=1.2)
            head = T("Everything comes from definitions", size=44).move_to([0, 3.15, 0])
            c.wait_until("everything")
            self.play(*appear(head), run_time=1.0)
            c.wait_until("names")

            cols = {}
            for side, x in (("real", -2.4), ("complex", 2.4)):
                h = T(side, size=36, color=DIM).move_to([x, 2.15, 0])
                cols[side] = [h]
            r1 = MathTex("x^5", font_size=60).move_to([-2.4, 1.15, 0])
            c1 = MathTex("z^5", font_size=60).move_to([2.4, 1.15, 0])
            r2 = MathTex(r"\ln x", font_size=60).move_to([-2.4, -0.05, 0])
            c2 = MathTex(r"\ln z", font_size=60).move_to([2.4, -0.05, 0])
            a1 = Arrow([-1.3, 1.15, 0], [1.3, 1.15, 0], buff=0, stroke_width=3, color=DIM,
                       max_tip_length_to_length_ratio=0.12)
            a2 = a1.copy().move_to([0, -0.05, 0])
            self.play(*appear(cols["real"][0], r1, r2, lag=0.2), run_time=1.0)
            self.play(*appear(cols["complex"][0], shift=None), GrowArrow(a1), GrowArrow(a2),
                      *during([FadeIn(c1, shift=0.3 * RIGHT), FadeIn(c2, shift=0.3 * RIGHT)], 0.35, 1.0),
                      run_time=1.6)  # early: column header
            c.wait_until("different")

            ul = Line([1.2, -0.55, 0], [3.6, -0.55, 0], stroke_width=5, color=YELLOW)
            diff = T("what's different", size=32, color=YELLOW).next_to(ul, DOWN, buff=0.22)
            self.play(Create(ul), run_time=0.8)
            self.play(*appear(diff), run_time=0.8)
            c.wait_until("road")

            tiles = VGroup(*[road_tile(i, n) for i, n in enumerate(ROAD)])
            for i, t in enumerate(tiles):
                t.move_to([(i - 3) * 1.98, 0, 0], aligned_edge=UP).set_y(-1.6, direction=UP)
            self.play(*disappear(*dimmable), *appear(*tiles, lag=0.12), run_time=1.8)  # early: the road shown whole, then walked
            c.wait_until("roots")
            self.play(FlashAround(tiles[0][0], run_time=1.5, time_width=1.5))

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
