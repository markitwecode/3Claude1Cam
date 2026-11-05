"""Chapter 1, scene 2: Lecture 9 in one picture (polar form, Euler, product, conjugate, arg + 2πn). Clips c1.polar.1 – c1.polar.5."""
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

# The Argand plane on the right two-thirds: origin, unit length, half-extent of the axes.
O = np.array([2.6, 0.45, 0.0])
U = 1.9
EXT = 2.8
R_Z = 1.35         # |z| of the running point z
DEG = 40           # its argument θ, degrees
LX = -6.4          # left edge of the formula column
ROWS = [2.75, 1.9, 0.95, 0.1, -0.9, -1.9, -2.65, -3.3]
FS = 52            # formula size


def argand_plane(center=O, unit=U, extent=EXT):
    """PLAN.md's running Argand plane: faint grid, Re/Im axes, DIM unit circle (copied unchanged from ch2_s2_theorem)."""
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


def _dir(deg):
    a = np.deg2rad(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def ray(deg, r, color=GOLD, center=O, unit=U):
    return Arrow(center, center + unit * r * _dir(deg), buff=0, stroke_width=6,
                 max_tip_length_to_length_ratio=0.14, tip_length=0.28, color=color)


def angle_arc(start, span, radius, color, center=O):
    return Arc(radius=radius, start_angle=np.deg2rad(start), angle=np.deg2rad(span),
               arc_center=center, color=color, stroke_width=4)


def polar_z(center=O, unit=U, r=R_Z, deg=DEG):
    """The point z: GOLD |z| arrow, dot, z label, |z| label, YELLOW θ arc + θ, TEAL full-turn arc + "+2π".
    Attributes .arrow .dot .label .mod .arc .theta .turn .turn_label. The recap shrinks this into a panel."""
    tip = center + unit * r * _dir(deg)
    arrow = ray(deg, r, center=center, unit=unit)
    dot = Dot(tip, radius=0.08, color=FG)
    label = MathTex("z", font_size=44, color=FG).move_to(tip + 0.32 * _dir(deg + 15))
    mid = center + 0.5 * unit * r * _dir(deg)
    mod = MathTex("|z|", font_size=40, color=GOLD).move_to(mid + 0.42 * _dir(deg + 90))
    arc = angle_arc(0, deg, 0.6, YELLOW, center)
    theta = MathTex(r"\theta", font_size=40, color=YELLOW).move_to(center + 0.9 * _dir(deg / 2))
    turn = angle_arc(deg, 360, 1.0, TEAL, center)
    turn_label = MathTex(r"+2\pi", font_size=38, color=TEAL).move_to(center + 1.4 * _dir(215))
    g = VGroup(arrow, dot, label, mod, arc, theta, turn, turn_label)
    g.arrow, g.dot, g.label, g.mod, g.arc, g.theta, g.turn, g.turn_label = (
        arrow, dot, label, mod, arc, theta, turn, turn_label)
    return g


def xy_drops(center=O, unit=U, r=R_Z, deg=DEG):
    """Dashed BLUE drop to x on Re, dashed PINK line to y on Im, with x and y labels."""
    tip = center + unit * r * _dir(deg)
    px = np.array([tip[0], center[1], 0])
    py = np.array([center[0], tip[1], 0])
    dx = DashedLine(tip, px, dash_length=0.12, color=BLUE, stroke_width=3)
    dy = DashedLine(tip, py, dash_length=0.12, color=PINK, stroke_width=3)
    lx = MathTex("x", font_size=40, color=BLUE).next_to(px, DOWN, buff=0.15)
    ly = set_backstroke(MathTex("y", font_size=40, color=PINK).next_to(py, LEFT, buff=0.15))
    g = VGroup(dx, dy, lx, ly)
    g.dx, g.dy, g.lx, g.ly = dx, dy, lx, ly
    return g


def row(m, i, x=LX):
    m.move_to([0, ROWS[i], 0]).align_to([x, 0, 0], LEFT)
    return m


def spin(arrow, turns, center=O):
    base = arrow.copy()

    def f(m, a):
        m.become(base.copy().rotate(a * turns * TAU, about_point=center))
    return UpdateFromAlphaFunc(arrow, f, rate_func=linear)


class PolarRecap(NarratedScene):
    def construct(self):
        plane = argand_plane()
        z = polar_z()
        drops = xy_drops()

        # ---------------- clip 1: z = x + iy, the point, |z|, θ
        with self.say("c1.polar.1") as c:
            self.play(FadeIn(plane), run_time=min(1.5, c.until("point")))
            c.wait_until("point")
            eq_z = row(MathTex(r"z = x + iy", font_size=FS), 0)
            eq_i = row(MathTex(r"i^2 = -1", font_size=FS), 1)
            self.play(*appear(eq_z), run_time=1.0)
            c.wait_until("where eye squared")
            self.play(*appear(eq_i), run_time=1.0)
            c.wait_until("plane")
            self.play(FadeIn(z.dot, scale=0.5), *appear(z.label), run_time=1.0)
            self.play(Create(drops.dx), Create(drops.dy), *appear(drops.lx, drops.ly, lag=0.5), run_time=1.6)
            c.wait_until("mod")
            self.play(GrowArrow(z.arrow), run_time=1.5)
            c.wait_until("modulus")
            self.play(*appear(z.mod), run_time=1.0)
            c.wait_until("arg")
            self.play(Create(z.arc), run_time=1.5)
            c.wait_until("Call it theta")
            self.play(*appear(z.theta), run_time=0.8)

        # ---------------- clip 2: trig form, Euler, z = |z|e^{iθ}
        with self.say("c1.polar.2") as c:
            eq_x = row(MathTex(r"x = |z|\cos\theta", font_size=FS, color=BLUE), 2)
            eq_y = row(MathTex(r"y = |z|\sin\theta", font_size=FS, color=PINK), 3)
            eq_c = row(MathTex(r"z = |z|(\cos\theta + i\sin\theta)", font_size=FS), 4)
            self.play(*set_alpha([eq_i], 0.4), *fly(drops.lx, eq_x), run_time=1.5)
            c.wait_until("imaginary part")
            self.play(*fly(drops.ly, eq_y), run_time=1.5)
            self.play(*appear(eq_c), run_time=min(1.2, c.until("euler")))
            c.wait_until("euler")
            eq_e = row(MathTex(r"\cos\theta + i\sin\theta", "=", r"e^{i\theta}", font_size=FS), 5)
            eq_e[2].set_color(GOLD)
            tag71 = T("(71)", 28, DIM).next_to(eq_e, DOWN, buff=0.15).align_to(eq_e, RIGHT)
            self.play(*appear(eq_e[0], eq_e[1], eq_e[2], lag=0.4), run_time=2.0)
            self.play(*appear(tag71), run_time=0.8)
            c.wait_until("expform")
            eq_f = MathTex(r"z = |z|", r"e^{i\theta}", font_size=FS)
            eq_f[1].set_color(GOLD)
            row(eq_f, 4)
            self.play(*edit(eq_c, eq_f), run_time=1.5)
            c.wait_until("later")
            later = T("proved in §6.3", 30, DIM)
            later.move_to([0, tag71.get_y(), 0]).align_to(eq_e, LEFT)
            self.play(*appear(later), run_time=1.0)
            c.wait_until("exp")
            expx = MathTex(r"\exp(i\theta) = e^{i\theta}", font_size=36, color=FG)
            expx.move_to([0, tag71.get_y() - 0.7, 0]).align_to(eq_e, LEFT)
            self.play(*appear(expx), run_time=1.0)

        # ---------------- clip 3: product, conjugate
        with self.say("c1.polar.3") as c:
            gone = [eq_z, eq_i, eq_x, eq_y, eq_e, tag71, later, drops.dx, drops.dy, drops.lx, drops.ly,
                    z.arrow, z.dot, z.label, z.mod, z.arc, z.theta]
            self.play(*[FadeOut(m) for m in gone], run_time=1.0)
            self.play(eq_f.animate.move_to([0, ROWS[0], 0]).align_to([LX, 0, 0], LEFT), *disappear(expx), run_time=1.0)
            c.wait_until("Take zed one")
            r1, a1, r2, a2 = 1.1, 15, 1.18, 45
            z1 = ray(a1, r1, FG)
            z2 = ray(a2, r2, FG)
            l1 = MathTex("z_1", font_size=40, color=FG).move_to(z1.get_end() + 0.4 * _dir(a1 - 10))
            l2 = MathTex("z_2", font_size=40, color=FG).move_to(z2.get_end() + 0.4 * _dir(a2 + 15))
            arc1 = angle_arc(0, a1, 0.6, YELLOW)
            arc2 = angle_arc(0, a2, 1.4, YELLOW)
            t1 = MathTex(r"\theta_1", font_size=34, color=YELLOW).move_to(O + 0.98 * _dir(a1 / 2))
            t2 = MathTex(r"\theta_2", font_size=34, color=YELLOW).move_to(O + 1.78 * _dir(30))
            self.play(GrowArrow(z1), Create(arc1), *appear(l1, t1), run_time=1.2)
            self.play(GrowArrow(z2), Create(arc2), *appear(l2, t2), run_time=min(1.2, c.until("product")))
            c.wait_until("product")
            rp, ap = r1 * r2, a1 + a2
            zp = ray(ap, rp, GOLD)
            lp = MathTex("z_1z_2", font_size=40, color=GOLD).move_to(zp.get_end() + 0.45 * _dir(ap + 20))
            mp = MathTex(r"|z_1||z_2|", font_size=36, color=GOLD)
            mp.move_to(O + 0.55 * U * rp * _dir(ap) + 0.95 * _dir(ap + 90))
            set_backstroke(mp)
            p1 = angle_arc(0, a1, 0.95, YELLOW)
            p2 = angle_arc(a1, a2, 0.95, YELLOW)
            self.play(*set_alpha([arc1, arc2, t1, t2], 0.4),
                      ReplacementTransform(arc1.copy(), p1), ReplacementTransform(arc2.copy(), p2), run_time=1.6)
            self.play(GrowArrow(zp), *appear(lp, mp, lag=0.4), run_time=1.5)
            eq_p = MathTex(r"z_1z_2 = ", r"|z_1||z_2|", r"e^{i(\theta_1+\theta_2)}", font_size=48)
            eq_p[1].set_color(GOLD)
            row(eq_p, 2)
            tag73 = T("(73)", 28, DIM).next_to(eq_p, DOWN, buff=0.2).align_to(eq_p, RIGHT)
            self.play(*appear(eq_p, tag73, lag=0.5), run_time=min(1.4, c.until("rule")))
            c.wait_until("rule")
            self.play(FlashAround(eq_p[1], run_time=1.2, time_width=1.5), FlashAround(mp, run_time=1.2, time_width=1.5))
            self.play(FlashAround(eq_p[2], run_time=1.2, time_width=1.5),
                      VShowPassingFlash(VGroup(p1.copy(), p2.copy()).set_stroke(FG, 7), time_width=0.5, run_time=1.2))
            c.wait_until("conj")
            self.play(*[FadeOut(m) for m in [z1, z2, l1, l2, arc1, arc2, t1, t2, p1, p2, zp, lp, mp]],
                      run_time=1.0)
            self.play(GrowArrow(z.arrow), FadeIn(z.dot), Create(z.arc), *appear(z.label, z.mod, z.theta), run_time=1.2)
            zs = polar_z(deg=-DEG)
            for m in (zs.arrow, zs.arc, zs.theta):
                m.set_color(PURPLE)
            zs_lab = MathTex("z^*", font_size=44, color=PURPLE).move_to(zs.dot.get_center() + 0.4 * _dir(-DEG - 15))
            mth = MathTex(r"-\theta", font_size=38, color=PURPLE).move_to(O + 1.0 * _dir(-DEG / 2))
            eq_s = row(MathTex(r"z^* = |z|e^{-i\theta}", font_size=FS, color=PURPLE), 4)
            self.play(GrowArrow(zs.arrow), FadeIn(zs.dot), Create(zs.arc), *appear(zs_lab, mth), run_time=1.5)
            self.play(*appear(eq_s), run_time=min(1.0, c.until("mirror")))
            c.wait_until("mirror")
            mirror = DashedLine(z.dot.get_center(), zs.dot.get_center(), dash_length=0.1, color=DIM, stroke_width=3)
            self.play(Create(mirror), run_time=1.2)

        # ---------------- clip 4: many arguments
        with self.say("c1.polar.4") as c:
            c.wait_until("The argument has many values")
            self.play(*disappear(zs.arrow, zs.dot, zs.arc, zs_lab, mth, mirror, eq_s, eq_p, tag73), run_time=1.0)
            self.play(FlashAround(z.theta, run_time=1.5, time_width=1.5))
            c.wait_until("turn")
            rt = min(5.2, c.until("anyn") - 0.3)
            self.play(*disappear(z.mod, z.theta), run_time=0.4)
            self.play(spin(z.arrow, 1), Create(z.turn, rate_func=linear), run_time=rt)
            self.play(*appear(z.turn_label), run_time=min(0.6, c.until("anyn")))
            c.wait_until("anyn")
            self.play(spin(z.arrow, 1), run_time=1.3)
            self.play(spin(z.arrow, -2), run_time=min(2.4, c.until("formula") - 0.6))
            self.play(*appear(z.mod, z.theta, shift=None), run_time=0.5)
            c.wait_until("formula")
            eq_a = MathTex(r"\arg z = \theta + ", r"2\pi n", r",\ n \in \mathbb{Z}", font_size=FS)
            eq_a[1].set_color(TEAL)
            row(eq_a, 2)
            self.play(*appear(eq_a), run_time=1.2)
            c.wait_until("why")
            eq_w = MathTex(r"e^{2\pi i n} = 1", font_size=FS)
            eq_w[0][1:3].set_color(TEAL)
            row(eq_w, 3)
            self.play(*appear(eq_w), run_time=1.0)

        # ---------------- clip 5: principal argument
        with self.say("c1.polar.5") as c:
            ny = -2.95
            half = 2.2
            axis = Line([O[0] - half - 0.45, ny, 0], [O[0] + half + 0.45, ny, 0]).set_stroke(DIM, 2)
            band = Line([O[0] - half, ny, 0], [O[0] + half, ny, 0]).set_stroke(GREEN, 6)
            open_c = Circle(radius=0.1).move_to([O[0] - half, ny, 0]).set_stroke(GREEN, 3).set_fill(BG, 1)
            shut = Dot([O[0] + half, ny, 0], radius=0.1, color=GREEN)
            lm = MathTex(r"-\pi", font_size=34, color=FG).next_to(open_c, DOWN, buff=0.12)
            lpi = MathTex(r"\pi", font_size=34, color=FG).next_to(shut, DOWN, buff=0.12)
            ineq = MathTex(r"-\pi < \theta \le \pi", font_size=FS, color=GREEN)
            ineq.move_to([0, ny, 0]).align_to([LX, 0, 0], LEFT)
            self.play(Create(axis), Create(band), FadeIn(open_c), FadeIn(shut), run_time=1.5)
            self.play(*appear(lm, lpi), run_time=1.0)
            self.play(*appear(ineq), run_time=min(1.2, c.until("ends")))
            c.wait_until("ends")
            m1 = Dot(O + U * LEFT, radius=0.1, color=GREEN)
            m1_lab = MathTex(r"\pi", font_size=40, color=GREEN).move_to(O + U * LEFT + 0.42 * UP + 0.32 * LEFT)
            self.play(FadeIn(m1, scale=0.5), *appear(m1_lab), run_time=1.2)
            self.play(FlashAround(shut, run_time=1.2, time_width=1.5), FlashAround(open_c, run_time=1.2, time_width=1.5,
                                                                                   color=RED))
            c.wait_until("keep")
            others = [m for m in self.mobjects if m is not eq_a]
            self.play(*set_alpha(others, DIMMED), *set_alpha([eq_a[0], eq_a[2]], DIMMED), run_time=1.0)
            self.play(FlashAround(eq_a[1], run_time=1.5, time_width=1.5))
            c.wait_until("This whole lecture")
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=min(1.0, c.until(None)))
        self.wait(0.15)
