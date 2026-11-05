"""Chapter 4, scene 3: what the exponential does to the plane (line -> circle, wrapping, the ladder). Clips c4.map.1 – c4.map.4."""
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

LN2 = float(np.log(2))
TAU_ = 2 * PI

# w-plane (left): u across, v up; v squashed so two turns (4π) fit
OW = np.array([-4.2, -1.8, 0])
UX, VY = 1.3, 0.3
W_XR, W_YR = (-1.8, 1.6), (-5.6, 16.3)

# z-plane (right): ch2's Argand look, equal scale
OZ = np.array([3.5, -0.2, 0])
UZ = 0.95
Z_XR, Z_YR = (-2.8, 2.7), (-3.0, 3.0)

COIL_OFF = 0.12       # screen units of extra radius per turn when the line coils


def PW(u, v):
    return OW + np.array([UX * u, VY * v, 0])


def PZ(x, y):
    return OZ + UZ * np.array([x, y, 0])


def _axes(P, xr, yr, xs, ys, xlab, ylab):
    grid = VGroup()
    for x in xs:
        grid.add(Line(P(x, yr[0]), P(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in ys:
        grid.add(Line(P(xr[0], y), P(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0), P(xr[1], 0) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0]), P(0, yr[1]) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    re = T(xlab, size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T(ylab, size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    return VGroup(grid, xax, yax, re, im)


def w_plane():
    """Re w / Im w axes, faint grid (integer u, multiples of π in v), no unit circle."""
    xs = [x for x in range(-1, 2) if x]
    ys = [k * PI for k in range(-1, 6) if k]
    return _axes(PW, W_XR, W_YR, xs, ys, "Re w", "Im w")


def z_plane():
    """ch2's argand_plane look (copied): Re/Im, faint integer grid, DIM unit circle."""
    xs = [x for x in range(-2, 3) if x]
    ys = [y for y in range(-3, 4) if y]
    g = _axes(PZ, Z_XR, Z_YR, xs, ys, "Re", "Im")
    g.add(Circle(radius=UZ, color=DIM, stroke_width=2).move_to(OZ))
    return g


def exp_arrow():
    arr = Arrow(np.array([-1.5, 2.55, 0]), np.array([0.4, 2.55, 0]), buff=0, color=GOLD,
                stroke_width=5, max_tip_length_to_length_ratio=0.18)
    lab = MathTex("e^w", font_size=48, color=GOLD).next_to(arr, UP, buff=0.15)
    return arr, lab


def w_line(u=LN2, n=241):
    """The GOLD vertical line Re w = u, sampled so it can coil."""
    vs = np.linspace(W_YR[0], W_YR[1], n)
    return VMobject(stroke_color=GOLD, stroke_width=4).set_points_as_corners([PW(u, v) for v in vs])


def coil(off=COIL_OFF, u=LN2, n=241):
    """The image of w_line under e^w, each turn offset outward by `off` (0: the circle itself)."""
    vs = np.linspace(W_YR[0], W_YR[1], n)
    r = UZ * np.exp(u)
    pts = [OZ + (r + off * v / TAU_) * np.array([np.cos(v), np.sin(v), 0]) for v in vs]
    return VMobject(stroke_color=GOLD, stroke_width=4).set_points_smoothly(pts)


def z_circle(u=LN2):
    return Circle(radius=max(UZ * np.exp(u), 0.02), color=GOLD, stroke_width=4).move_to(OZ)


def map_pair():
    """For the recap: both planes, the e^w arrow, the GOLD line Re w = ln 2 and its GOLD circle.
    Coil with: Transform(line.copy(), coil()), then Transform(that, coil(0)). Returns
    VGroup(w_plane, z_plane, arrow, arrow_label, line, circle)."""
    arr, lab = exp_arrow()
    return VGroup(w_plane(), z_plane(), arr, lab, w_line(), z_circle())


class Map(NarratedScene):
    def construct(self):
        wp, zp = w_plane(), z_plane()
        arr, alab = exp_arrow()

        # ---------------- clip 1: the two planes
        with self.say("c4.map.1") as c:
            self.play(FadeIn(wp), FadeIn(zp), run_time=1.5)
            c.wait_until("left")
            self.play(*set_alpha([zp], 0.3), FlashAround(VGroup(wp[3], wp[4]).copy(), run_time=1.5),
                      run_time=1.5)
            c.wait_until("right")
            self.play(*set_alpha([zp], 1), *set_alpha([wp], 0.3), run_time=1.2)
            c.wait_until("arrow")
            w0 = (0.3, 1.0)
            ez = np.exp(w0[0]) * np.array([np.cos(w0[1]), np.sin(w0[1])])
            dw = Dot(PW(*w0), radius=0.1, color=YELLOW)
            dz = Dot(PZ(*ez), radius=0.1, color=YELLOW)
            lw = MathTex("w", font_size=40, color=YELLOW).next_to(dw, UR, buff=0.08)
            lz = MathTex("e^w", font_size=40, color=YELLOW).next_to(dz, UR, buff=0.08)
            self.play(*set_alpha([wp], 1), GrowArrow(arr), *appear(alab), run_time=1.2)
            self.play(*appear(dw, lw), run_time=0.8)
            self.play(*fly(dw, dz), time_span(FadeIn(lz), 1.1, 1.5), run_time=1.5)
            c.wait_until()

        # ---------------- clip 2: a vertical line lands on a circle
        with self.say("c4.map.2") as c:
            line = Line(PW(LN2, W_YR[0]), PW(LN2, W_YR[1]), color=GOLD, stroke_width=4)
            self.play(Create(line), run_time=1.5)
            c.wait_until("log two")
            tick = Line(PW(LN2, 0) + 0.1 * DOWN, PW(LN2, 0) + 0.1 * UP, color=GOLD, stroke_width=3)
            tlab = set_backstroke(MathTex(r"\ln 2", font_size=36, color=GOLD)
                                  .next_to(PW(LN2, 0), DR, buff=0.12))
            self.play(FadeIn(tick), *appear(tlab), *disappear(dw, lw, dz, lz), run_time=1.0)
            c.wait_until("circle")
            circ = z_circle()
            # the line's points run across: a flash up the line, then the circle drawn round from 2
            self.play(VShowPassingFlash(line.copy().set_stroke(YELLOW, 8), time_width=0.5),
                      run_time=1.0)
            self.play(Create(circ), run_time=1.2)
            c.wait_until("that's two")
            two = set_backstroke(MathTex("2", font_size=36, color=GOLD).next_to(PZ(2, 0), DR, buff=0.1))
            self.play(*appear(two), run_time=0.8)
            c.wait_until("slide")

            u = ValueTracker(LN2)
            line_r = always_redraw(lambda: w_line(u.get_value(), n=2))
            circ_r = always_redraw(lambda: z_circle(u.get_value()))
            self.remove(line, circ)
            self.add(line_r, circ_r)
            self.play(u.animate.set_value(0.9), *disappear(two), *during(disappear(tlab), 0, 0.3),
                      run_time=min(2.3, 0.8 * c.until("slide it left")))
            c.wait_until("slide it left")
            self.play(u.animate.set_value(-1.2), run_time=min(2.0, 0.8 * c.until("never reaches")))
            c.wait_until("never reaches")
            self.play(u.animate.set_value(LN2), *during(appear(tlab, shift=None), 0.8, 1),
                      run_time=min(1.4, 0.8 * c.until(floor=0.4)))
            line, circ = Line(PW(LN2, W_YR[0]), PW(LN2, W_YR[1]), color=GOLD, stroke_width=4), z_circle()
            self.remove(line_r, circ_r)
            self.add(line, circ)
            c.wait_until()

        # ---------------- clip 3: climbing wraps round
        with self.say("c4.map.3") as c:
            v = ValueTracker(0.0)

            def wpt():
                return PW(LN2, v.get_value())

            def zpt():
                a = v.get_value()
                return PZ(2 * np.cos(a), 2 * np.sin(a))

            seg = always_redraw(lambda: Line(PW(LN2, 0), PW(LN2, max(v.get_value(), 0.02)),
                                             color=YELLOW, stroke_width=6))
            arc1 = always_redraw(lambda: Arc(radius=2 * UZ, start_angle=0,
                                             angle=max(min(v.get_value(), TAU_), 0.002),
                                             arc_center=OZ, color=YELLOW, stroke_width=6))
            arc2 = always_redraw(lambda: Arc(radius=2 * UZ + COIL_OFF, start_angle=0,
                                             angle=max(v.get_value() - TAU_, 0.002), arc_center=OZ,
                                             color=YELLOW, stroke_width=6,
                                             stroke_opacity=1 if v.get_value() > TAU_ else 0))
            rad = always_redraw(lambda: Line(OZ, zpt(), color=YELLOW, stroke_width=2.5))
            dwc = always_redraw(lambda: Dot(wpt(), radius=0.11, color=YELLOW))
            dzc = always_redraw(lambda: Dot(zpt(), radius=0.11, color=YELLOW))
            self.play(FadeIn(seg), FadeIn(arc1), FadeIn(rad), FadeIn(dwc), FadeIn(dzc), run_time=0.6)
            self.add(arc2)
            self.play(v.animate.set_value(TAU_), run_time=min(5.8, c.until("wrap") - 0.3),
                      rate_func=linear)
            c.wait_until("wrap")
            br = Brace(Line(PW(LN2, 0), PW(LN2, TAU_)), direction=RIGHT, buff=0.15, color=TEAL)
            blab = set_backstroke(MathTex(r"2\pi", font_size=40, color=TEAL).next_to(br, RIGHT, buff=0.12))
            self.play(GrowFromCenter(br), *appear(blab, shift=None), run_time=1.0)
            self.play(FlashAround(Dot(PZ(2, 0), radius=0.11), run_time=1.2), run_time=1.2)
            c.wait_until("again")
            self.play(v.animate.set_value(2 * TAU_), run_time=min(3.0, 0.9 * c.until("spool")),
                      rate_func=linear)
            c.wait_until("spool")
            climb = [seg, arc1, arc2, rad, dwc, dzc]
            self.play(*disappear(*climb, br, blab), run_time=0.8)
            sp = w_line()
            self.play(Transform(sp, coil()), run_time=min(2.8, 0.6 * c.until(floor=1.0)))
            self.play(Transform(sp, coil(0.0)), run_time=min(1.4, c.until(floor=0.5)))
            self.remove(sp)
            c.wait_until()

        # ---------------- clip 4: backwards: one point, a whole ladder; real vs complex
        with self.say("c4.map.4") as c:
            log = MathTex(r"\ln z", font_size=48, color=GOLD).move_to(alab)
            self.play(Rotate(arr, PI), *swap(alab, log), run_time=1.2)
            c.wait_until("point")
            pz = Dot(PZ(0, 2), radius=0.12, color=YELLOW)
            plab = set_backstroke(MathTex("2i", font_size=40, color=YELLOW).next_to(pz, UL, buff=0.08))
            self.play(*appear(pz, plab, shift=None), run_time=0.8)
            self.play(FlashAround(pz, run_time=1.2), run_time=1.2)
            c.wait_until("ladder")
            ks = [0, 1, -1, 2]
            dots, arrows = [], []
            for k in ks:
                op = 1.0 if k in (0, 1) else 0.35
                d = Dot(PW(LN2, PI / 2 + TAU_ * k), radius=0.08, color=TEAL, fill_opacity=op)
                a = Arrow(pz.get_center(), d.get_center(), buff=0.16, color=TEAL, stroke_width=2,
                          stroke_opacity=op, max_tip_length_to_length_ratio=0.03)
                a.get_tip().set_fill(opacity=op).set_stroke(opacity=op)
                dots.append(d)
                arrows.append(a)
            rt = min(2.6, 0.8 * c.until("real"))
            self.play(*during([FadeIn(d, scale=0.5) for d in dots], 0, 0.35),
                      *during([GrowArrow(a) for a in arrows], 0.3, 1), run_time=rt)
            c.wait_until("real")

            # shrink the pair to the top; contrast strip underneath
            top = [wp, zp, arr, log, line, circ, pz, plab, *dots, *arrows]
            A = np.array([0, 3.6, 0])
            labels = {id(wp): [wp[3], wp[4]], id(zp): [zp[3], zp[4]], id(tlab): [tlab], id(plab): [plab]}
            for m in top:
                m.generate_target()
                m.target.scale(0.68, about_point=A)
                if id(m) in labels:
                    tg = [m.target] if m is plab else [m.target[3], m.target[4]]
                    for lb in tg:
                        lb.scale(1.42)
            self.play(*[MoveToTarget(m) for m in top], *disappear(tick, tlab), run_time=1.5)
            ys = -2.3
            rl = Line([-6.1, ys, 0], [-3.8, ys, 0], color=BLUE, stroke_width=5)
            rlab = MathTex(r"\mathbb{R}", font_size=40, color=BLUE).next_to(rl, LEFT, buff=0.15)
            zax = Arrow([-3.1, ys, 0], [-0.2, ys, 0], buff=0, color=FG, stroke_width=2.5,
                        max_tip_length_to_length_ratio=0.06)
            o = Dot([-2.6, ys, 0], radius=0.06, color=FG)
            olab = MathTex("0", font_size=34).next_to(o, DOWN, buff=0.15)
            self.play(Create(rl), *appear(rlab, shift=None), FadeIn(zax), FadeIn(o), *appear(olab),
                      run_time=1.2)
            c.wait_until("lays")
            ray = Line([-2.6, ys, 0], [-0.4, ys, 0], color=BLUE, stroke_width=5)
            self.play(VShowPassingFlash(rl.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      Create(ray), run_time=2.0, rate_func=linear)
            c.wait_until("one value")
            gz = Dot([-1.4, ys, 0], radius=0.09, color=GOLD)
            gw = Dot([-4.7, ys, 0], radius=0.09, color=GOLD)
            back = CurvedArrow(gz.get_center() + 0.12 * UP, gw.get_center() + 0.12 * UP,
                               angle=PI / 3, color=GOLD, stroke_width=3)
            one = T("one log", size=30, color=GOLD).next_to(gw, DOWN, buff=0.25)
            self.play(FadeIn(gz), Create(back), run_time=1.0)
            self.play(FadeIn(gw), *appear(one), run_time=0.8)
            c.wait_until("complex")
            many = T("infinitely many w  →  one z", size=36, t2c={"infinitely many": TEAL})
            many.move_to([3.7, ys, 0])
            self.play(*appear(many), run_time=1.0)  # early: shown with the sentence it sums up
            c.wait_until()
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
