"""Chapter 1, scene 3: roots of unity, z^4 = 1 worked, then z^n = 1 and the n = 5 pentagon. Clips c1.unity.1 – c1.unity.4."""
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
from lib.style import *  # noqa: E402,F403

# The Argand plane on the right, the working on the left.
O = np.array([3.5, -0.3, 0.0])
U = 2.2            # unit circle radius on screen
EXT = 3.0
LX = -6.3          # left edge of the working
DOT_R = 0.12


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


def unity_plane(center=O, unit=U, extent=EXT):
    """The ch1 plane: ch2's argand_plane with the unit circle at full strength."""
    g = argand_plane(center, unit, extent)
    g.circle.set_stroke(FG, 3.5, opacity=1)
    return g


def on_circle(deg, center=O, unit=U, r=1.0):
    a = np.deg2rad(deg)
    return center + unit * r * np.array([np.cos(a), np.sin(a), 0])


def ray(deg, r=1.0, color=GOLD, center=O, unit=U):
    return Arrow(center, on_circle(deg, center, unit, r), buff=0, stroke_width=6,
                 max_tip_length_to_length_ratio=0.14, tip_length=0.28, color=color)


ROOT_TEX = ["1", "i", "-1", "-i"]
LABEL_OFF = [np.array([0.3, 0.32, 0]), np.array([-0.32, 0.3, 0]),
             np.array([-0.4, 0.32, 0]), np.array([0.38, -0.3, 0])]


def four_roots(center=O, unit=U, labels=True, label_size=40):
    """The fourth roots of unity: GREEN dot at 1, TEAL at i, -1, -i (with labels).
    Returns VGroup(dots, labels); .dots .labels (labels empty when labels=False)."""
    dots = VGroup(*[Dot(on_circle(90 * k, center, unit), radius=DOT_R * unit / U if unit < U else DOT_R,
                        color=GREEN if k == 0 else TEAL).set_z_index(2) for k in range(4)])
    labs = VGroup()
    if labels:
        for k in range(4):
            lab = MathTex(ROOT_TEX[k], font_size=label_size, color=GREEN if k == 0 else TEAL)
            lab.move_to(on_circle(90 * k, center, unit) + LABEL_OFF[k] * (label_size / 40))
            labs.add(lab)
    g = VGroup(dots, labs)
    g.dots, g.labels = dots, labs
    return g


def nth_roots(n, center=O, unit=U, rays=True, dot_r=DOT_R):
    """Figure 23: n dots round the unit circle (GREEN at 1, TEAL others), with DIM rays.
    Returns VGroup(rays, dots); .rays .dots."""
    rs = VGroup()
    if rays:
        rs = VGroup(*[Line(center, on_circle(360 * k / n, center, unit), stroke_width=2.5, color=DIM)
                      for k in range(n)])
    dots = VGroup(*[Dot(on_circle(360 * k / n, center, unit), radius=dot_r,
                        color=GREEN if k == 0 else TEAL).set_z_index(2) for k in range(n)])
    g = VGroup(rs, dots)
    g.rays, g.dots = rs, dots
    return g


def unity_pentagon(center=O, unit=U, dot_r=DOT_R):
    """The five fifth roots of unity: a regular pentagon with a vertex at 1 (GREEN), four TEAL.
    Returns VGroup(polygon, dots); .polygon .dots. ch1_s5_ring scales and turns this."""
    pts = [on_circle(72 * k, center, unit) for k in range(5)]
    poly = Polygon(*pts, color=TEAL, stroke_width=4).set_stroke(opacity=0.85)
    dots = VGroup(*[Dot(p, radius=dot_r, color=GREEN if k == 0 else TEAL).set_z_index(2)
                    for k, p in enumerate(pts)])
    g = VGroup(poly, dots)
    g.polygon, g.dots = poly, dots
    return g


def tex(s, size=50, color=FG):
    return MathTex(s, font_size=size, color=color)


def left_at(m, y):
    m.move_to([0, y, 0]).align_to([LX, 0, 0], LEFT)
    return m


class Unity(NarratedScene):
    def construct(self):
        plane = unity_plane()

        # ---- clip 1: z^4 = 1, z = re^{iθ}, r^4 e^{4iθ} = 1
        with self.say("c1.unity.1") as c:
            self.play(FadeIn(plane), run_time=min(1.5, c.until("example")))
            c.wait_until("example")
            L0 = left_at(tex(r"z^4 = 1", 56), 3.0)
            self.play(*appear(L0), run_time=1.0)
            c.wait_until("polar")
            L1 = left_at(tex(r"z = re^{i\theta}"), 2.0)
            L1[0][2].set_color(GOLD)
            L1[0][5].set_color(YELLOW)
            z_ray = ray(40, r=1.3)
            th_arc = Arc(radius=0.65, start_angle=0, angle=np.deg2rad(40), arc_center=O, color=YELLOW, stroke_width=4)
            th_lab = tex(r"\theta", 38, YELLOW).move_to(O + 0.95 * np.array([np.cos(np.deg2rad(20)), np.sin(np.deg2rad(20)), 0]))
            r_lab = tex("r", 40, GOLD)
            r_lab.move_to(on_circle(40, r=0.65) + 0.3 * np.array([-np.sin(np.deg2rad(40)), np.cos(np.deg2rad(40)), 0]))
            self.play(*appear(L1), GrowArrow(z_ray), run_time=1.4)
            self.play(Create(th_arc), *appear(th_lab, r_lab), run_time=1.0)
            c.wait_until("power")
            L2 = left_at(tex(r"r^4e^{4i\theta} = 1"), 1.0)
            L2[0][0:2].set_color(GOLD)
            L2[0][5].set_color(YELLOW)
            self.play(*appear(L2), run_time=min(1.5, c.until("must equal")))
            c.wait_until("must equal")
            self.play(FlashUnder(L2, color=YELLOW, time_width=1.5), run_time=min(1.5, c.until()))

        # ---- clip 2: compare lengths, compare angles
        with self.say("c1.unity.2") as c:
            self.play(FlashAround(L2[0][0:2], color=GOLD, run_time=1.2, time_width=1.5))
            c.wait_until("is one")
            L3 = left_at(tex(r"r^4 = 1 \Rightarrow r = 1", 50, GOLD), 0.0)
            self.play(*appear(L3), run_time=1.0)
            c.wait_until("so r equals")
            self.play(Transform(z_ray, ray(40, r=1.0)),
                      r_lab.animate.move_to(on_circle(40, r=0.5) + 0.3 * np.array([-np.sin(np.deg2rad(40)), np.cos(np.deg2rad(40)), 0])),
                      run_time=1.5)
            c.wait_until("angle")
            self.play(FlashAround(L2[0][2:6], color=YELLOW, run_time=1.2, time_width=1.5),
                      FlashAround(th_lab, color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("whole number")
            L4 = left_at(tex(r"4\theta = 2\pi m,\ m \in \mathbb{Z}"), -1.0)
            L4[0][1].set_color(YELLOW)
            L4[0][3:6].set_color(TEAL)
            self.play(*appear(L4), run_time=1.2)
            c.wait_until("theta")
            L5 = left_at(tex(r"\theta = \frac{\pi m}{2}"), -2.3)
            L5[0][0].set_color(YELLOW)
            self.play(*appear(L5), run_time=1.2)
            c.wait_until("quarter turns")
            # make room for the table: the middle working goes, θ = πm/2 rises under z^4 = 1
            self.play(*during(disappear(L1, L2, L3, L4), 0, 0.45),
                      *during([L5.animate.move_to(left_at(L5.copy(), 2.0).get_center())], 0.35, 1.0),
                      run_time=min(1.5, c.until()))

        # ---- clip 3: the table, one quarter turn per row
        MX, ZX = -5.5, -3.9
        ROW_Y = [0.3, -0.25, -0.8, -1.35, -1.9]
        head_m = tex("m", 40, DIM).move_to([MX, 1.02, 0])
        head_z = tex("z", 40, DIM).move_to([ZX, 1.02, 0])
        rule = Line([LX, 0.72, 0], [-2.4, 0.72, 0], stroke_width=2, color=DIM)
        z_vals = ["1", "i", "-1", "-i", "1"]
        m_cells = [tex(str(k), 44).move_to([MX, ROW_Y[k], 0]) for k in range(5)]
        z_cells = [tex(z_vals[k], 44, GREEN if k in (0, 4) else TEAL).move_to([ZX, ROW_Y[k], 0]) for k in range(5)]
        again = T("(again)", 32, DIM).next_to(z_cells[4], RIGHT, buff=0.25)
        roots = four_roots()

        with self.say("c1.unity.3") as c:
            self.play(*disappear(th_arc, th_lab, r_lab),  # early: the table head comes with its first row
                      Rotate(z_ray, -np.deg2rad(40), about_point=O),
                      *appear(head_m, head_z, rule, m_cells[0], lag=0.1),
                      run_time=1.2)
            self.play(*appear(z_cells[0], shift=None), FadeIn(roots.dots[0], scale=0.5),
                      *appear(roots.labels[0]), run_time=0.9)
            c.wait_until("m1")
            self.play(*appear(m_cells[1]), Rotate(z_ray, PI / 2, about_point=O), run_time=1.5)
            self.play(*appear(z_cells[1], shift=None), FadeIn(roots.dots[1], scale=0.5),
                      *appear(roots.labels[1]), run_time=0.9)
            c.wait_until("m2")
            self.play(*appear(m_cells[2], z_cells[2], lag=0), Rotate(z_ray, PI / 2, about_point=O),
                      FadeIn(roots.dots[2], scale=0.5), *appear(roots.labels[2]),
                      run_time=min(0.9, c.until("m3")))
            c.wait_until("m3")
            self.play(*appear(m_cells[3], z_cells[3], lag=0), Rotate(z_ray, PI / 2, about_point=O),
                      FadeIn(roots.dots[3], scale=0.5), *appear(roots.labels[3]),
                      run_time=min(0.9, c.until("full turn")))
            c.wait_until("full turn")
            self.play(*appear(m_cells[4]), Rotate(z_ray, PI / 2, about_point=O), run_time=1.5)
            c.wait_until("back to one")
            self.play(*appear(z_cells[4], again, lag=0.4),
                      FlashAround(roots.dots[0], color=GREEN, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("quote")
            quote = VGroup(Tex(r"\textit{Infinitely many in} $\theta$\textit{,}", font_size=40, color=FG),
                           Tex(r"\textit{but four distinct in} $z$\textit{.}", font_size=40, color=FG)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            left_at(quote, -2.85)
            self.play(*appear(quote), run_time=1.2)

        # ---- clip 4: z^n = 1, n points evenly round the circle, n = 5
        with self.say("c1.unity.4") as c:
            G1 = left_at(tex(r"z^n = 1 \;\Rightarrow\; z = e^{2\pi i m/n}", 52), 1.0)
            G2 = left_at(tex(r"m = 0,\ 1,\ \dots,\ n-1", 44), -0.1).shift(0.6 * RIGHT)
            sweep_clear(self, time_span(FadeIn(G1, shift=0.2 * DOWN), 0.6, 1.2), keep=[plane, roots, z_ray, quote], run_time=1.2)
            self.play(*appear(G2), run_time=1.0)
            c.wait_until("ring")
            ring = nth_roots(8)
            self.play(*during(disappear(roots, z_ray, quote), 0, 0.4),
                      *during([Create(r) for r in ring.rays], 0.4, 1.0),
                      *during([FadeIn(d, scale=0.5) for d in ring.dots], 0.45, 1.0), run_time=1.8)
            c.wait_until("gap")
            gap = Arc(radius=U, start_angle=0, angle=TAU / 8, arc_center=O, color=YELLOW, stroke_width=7).set_z_index(1)
            gap_lab = tex(r"2\pi/n", 40, YELLOW).move_to(on_circle(22.5, r=1.0) + 0.6 * np.array([np.cos(np.deg2rad(22.5)), np.sin(np.deg2rad(22.5)), 0]))
            set_backstroke(gap_lab)
            self.play(Create(gap), *appear(gap_lab), run_time=1.0)
            c.wait_until("start")
            self.play(FlashAround(ring.dots[0], color=GREEN, run_time=1.2, time_width=1.5))
            c.wait_until("five")
            penta = unity_pentagon()
            n5 = left_at(tex(r"n = 5", 48, YELLOW), -1.4).shift(0.6 * RIGHT)
            lab5 = gap_lab.copy().move_to(on_circle(36, r=1.0) + 0.6 * np.array([np.cos(np.deg2rad(36)), np.sin(np.deg2rad(36)), 0]))
            self.play(*during(disappear(ring), 0, 0.45),
                      *during([Transform(gap, Arc(radius=U, start_angle=0, angle=TAU / 5, arc_center=O, color=YELLOW,
                                                 stroke_width=7).set_z_index(1)),
                               gap_lab.animate.move_to(lab5.get_center())], 0.2, 0.8),
                      *during([Create(penta.polygon)], 0.45, 1.0),
                      *during([FadeIn(d, scale=0.5) for d in penta.dots], 0.5, 1.0),
                      *during(appear(n5), 0.4, 1.0),
                      run_time=1.6)
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
