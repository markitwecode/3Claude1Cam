"""Chapter 5, scene 2: the circle's equation, (98) and (99). Clips c5.circle.1 – c5.circle.3."""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

R = 2.0                                   # radius, axis units (1 axis unit = 1 screen unit)
TH = float(np.arctan2(1.2, 1.6))          # the point P sits at (1.6, 1.2) from the centre
PV = np.array([1.6, 1.2, 0.0])            # centre -> P
CEN = np.array([1.5, 1.2, 0.0])           # (x0, y0)
O1 = np.array([0.0, -0.2, 0.0])           # origin while the picture is alone
O2 = np.array([-4.2, -0.6, 0.0])          # origin once the equations need the right half
A = O2 + np.array([0.9, 0.5, 0.0])        # the axes' centre: shrink about it in clip 3
B = np.array([4.75, -2.05, 0.0]) - A      # then move it to the lower right
SHRINK = 0.5
EQ_C = np.array([3.5, 0.6, 0.0])          # equation centre, clips 1-2
LEFT_X = -6.3                             # left edge of the working, clip 3


def M(parts, size=44, colors=None, color=FG):
    m = MathTex(*parts, font_size=size, color=color)
    for i, col in (colors or {}).items():
        m[i].set_color(col)
    return m


def build_axes(origin):
    ax = Axes(x_range=[-2.4, 4.2, 1], y_range=[-2.6, 3.6, 1], x_length=6.6, y_length=6.2,
              axis_config={"color": DIM, "include_ticks": False, "stroke_width": 2})
    ax.shift(origin - ax.c2p(0, 0))
    return ax


def build_circle(centre):
    return Arc(radius=R, start_angle=TH, angle=TAU, arc_center=centre, color=BLUE, stroke_width=5)


def shrink(m):
    return m.scale(SHRINK, about_point=A).shift(B)


def shrink_point(p):
    return A + SHRINK * (p - A) + B


def dim_shape(m):
    for sm in m.family_members_with_points():
        sm.set_stroke(opacity=DIMMED)
        if sm.get_fill_opacity() > 0:
            sm.set_fill(opacity=DIMMED)
    return m


def general_eq():
    eq = M(["x^2", "+", "a", "x", "+", "y^2", "+", "b", "y", "+", "c", "=", "0"], 56)
    tag = T("(99)", 36, DIM)
    return eq, tag


def handover_parts():
    ax = dim_shape(shrink(build_axes(O2)))
    circ = dim_shape(shrink(build_circle(O2 + CEN)))
    q = T("?", 52, YELLOW).move_to(shrink_point(O2 + CEN))
    eq, tag = general_eq()
    tag.next_to(eq, RIGHT, buff=0.45)
    VGroup(eq, tag).move_to([0, 3.0, 0])
    return ax, circ, q, eq, tag


def handover_shot():
    return VGroup(*handover_parts())


class CircleEquation(NarratedScene):
    def construct(self):
        u = np.array([np.cos(TH), np.sin(TH), 0.0])
        nrm = np.array([-np.sin(TH), np.cos(TH), 0.0])

        # ---------------- clip 1: definition, x^2 + y^2 = r^2 -----------------
        with self.say("c5.circle.1") as c:
            ax = build_axes(O1)
            cdot = Dot(O1, radius=0.1, color=YELLOW).set_z_index(3)
            self.play(*appear(ax, cdot, shift=None, lag=0.3), run_time=1.0)

            circle = build_circle(O1)
            radius = Line(O1, O1 + R * u, color=GOLD, stroke_width=5).set_z_index(2)

            def sweep(m, a):
                ang = TH + TAU * a
                m.put_start_and_end_on(O1, O1 + R * np.array([np.cos(ang), np.sin(ang), 0.0]))

            self.play(Create(circle, rate_func=linear),
                      UpdateFromAlphaFunc(radius, sweep, rate_func=linear),
                      run_time=max(2.0, min(3.0, c.until("that distance"))))
            radius.put_start_and_end_on(O1, O1 + R * u)

            rlab = set_backstroke(MathTex("r", font_size=44, color=GOLD))
            rlab.move_to(O1 + 0.5 * R * u + 0.32 * nrm)
            c.wait_until("radius")
            self.play(*appear(rlab), run_time=1.0)
            c.wait_until("origin")

            # the centre is the origin: the picture moves left to make room
            D = O2 - O1
            self.play(*[m.animate.shift(D) for m in (ax, cdot, circle, radius, rlab)],
                      run_time=min(1.5, 0.5 * c.until("pick a point")))
            P = O2 + PV
            foot = O2 + np.array([PV[0], 0, 0])
            pdot = Dot(P, radius=0.08, color=FG).set_z_index(3)
            plab = set_backstroke(MathTex("(x,\\, y)", font_size=40)).next_to(P, UR, buff=0.1)
            dash = DashedLine(P, foot, dash_length=0.12, color=FG, stroke_width=3)
            c.wait_until("pick a point")
            self.play(*appear(pdot, dash, plab, lag=0.3), run_time=1.4)
            c.wait_until("tri")

            # the right-angled triangle
            hleg = Line(O2, foot, color=FG, stroke_width=5)
            vleg = Line(foot, P, color=FG, stroke_width=5)
            s = 0.25
            rangle = VMobject(color=FG, stroke_width=3).set_points_as_corners(
                [foot + np.array([-s, 0, 0]), foot + np.array([-s, s, 0]), foot + np.array([0, s, 0])])
            self.play(*during(disappear(dash), 0, 0.4),
                      *during([Create(hleg), Create(vleg)], 0.2, 1.0),
                      run_time=1.5)
            xlab = set_backstroke(MathTex("x", font_size=44)).next_to(hleg, DOWN, buff=0.15)
            ylab = set_backstroke(MathTex("y", font_size=44)).next_to(vleg, RIGHT, buff=0.15)
            self.play(FadeIn(rangle), *appear(xlab, ylab, lag=0.4), run_time=1.2)
            c.wait_until("pyth")

            # x^2 + y^2 = r^2, built from the three labels
            eq98 = M(["x^2", "+", "y^2", "=", "r^2"], 60, {4: GOLD}).move_to(EQ_C)
            self.play(*fly(xlab, eq98[0][0], arc=-0.5),
                      *during(appear(eq98[0][1], shift=None), 0.75, 1.0),
                      run_time=min(1.3, c.until("plus why", floor=0.8)))
            c.wait_until("plus why")
            self.play(*during(appear(eq98[1], shift=None), 0.8, 1.0), *fly(ylab, eq98[2][0], arc=-1.2),
                      *during(appear(eq98[2][1], shift=None), 0.75, 1.0), run_time=1.2)
            c.wait_until("equals r")
            # fly from a halo-free twin of the label: the halo made the faint copy read as a grey "r"
            rsrc = MathTex("r", font_size=44, color=GOLD).move_to(rlab)
            self.play(*appear(eq98[3], shift=None), *fly(rsrc, eq98[4][0], arc=1.2),
                      *during(appear(eq98[4][1], shift=None), 0.75, 1.0), run_time=1.3)
            settle(self, eq98)
            c.wait_until("tag")

            tag98 = T("(98)", 36, DIM).next_to(eq98, RIGHT, buff=0.5)
            qual = M([r"\text{for } x,\, y,\, r \in \mathbb{R}"], 38, color=DIM).next_to(eq98, DOWN, buff=0.5)
            self.play(*appear(tag98, qual, lag=0.5), run_time=1.3)

        # ---------------- clip 2: move the centre --------------------------------
        with self.say("c5.circle.2") as c:
            D2 = CEN.copy()
            mov = [circle, cdot, radius, rlab, pdot, plab, hleg, vleg, rangle, xlab, ylab]
            self.play(*[m.animate.shift(D2) for m in mov], run_time=min(1.8, 0.55 * c.until("legs")))
            C2 = O2 + CEN
            dx = DashedLine(C2, np.array([C2[0], O2[1], 0]), dash_length=0.12, color=YELLOW, stroke_width=3)
            dy = DashedLine(C2, np.array([O2[0], C2[1], 0]), dash_length=0.12, color=YELLOW, stroke_width=3)
            x0lab = set_backstroke(MathTex("x_0", font_size=40, color=YELLOW))
            x0lab.next_to(np.array([C2[0], O2[1], 0]), DOWN, buff=0.15)
            y0lab = set_backstroke(MathTex("y_0", font_size=40, color=YELLOW))
            y0lab.move_to(np.array([O2[0] + 0.4, C2[1] + 0.3, 0]))
            self.play(*appear(dx, dy, x0lab, y0lab, lag=0.25), run_time=1.1)
            c.wait_until("ex minus ex zero")

            xlab2 = set_backstroke(M(["x -", "x_0"], 40, {1: YELLOW})).next_to(hleg, DOWN, buff=0.15)
            ylab2 = set_backstroke(M(["y -", "y_0"], 40, {1: YELLOW})).next_to(vleg, RIGHT, buff=0.42)
            self.play(*swap(xlab, xlab2), run_time=1.2)
            c.wait_until("why minus why zero")
            self.play(*swap(ylab, ylab2), run_time=1.2)
            c.wait_until("shift")

            eqs = M(["(x -", "x_0", ")^2", "+", "(y -", "y_0", ")^2", "=", "r^2"], 48,
                    {1: YELLOW, 5: YELLOW, 8: GOLD}).move_to(EQ_C + 0.25 * RIGHT)
            self.play(*during(disappear(tag98, qual), 0, 0.35),
                      *during(edit(eq98, eqs), 0.3, 1.0),
                      run_time=2.0)
            cap = T("subtract the centre before squaring", 29)
            cap.move_to(np.array([3.45, -1.1, 0]))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)

        # ---------------- clip 3: expand, (99), the centre is hidden -------------
        with self.say("c5.circle.3") as c:
            gone = [rlab, pdot, plab, hleg, vleg, rangle, xlab2, ylab2, x0lab, y0lab]
            kept = [ax, circle, cdot, radius, dx, dy]
            eqs.generate_target()
            eqs.target.scale(44 / 48)
            eqs.target.shift(np.array([LEFT_X - eqs.target.get_left()[0], 3.3 - eqs.target.get_center()[1], 0]))
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during([shrink_anim(m) for m in kept], 0.25, 0.85),
                      *during([MoveToTarget(eqs)], 0.3, 1.0),
                      *during([cap.animate.move_to(np.array([-2.0, -2.7, 0]))], 0.3, 1.0),
                      run_time=1.8)

            line1 = M(["x^2", "-2", "x_0", "x", "+", "x_0^2", "+", "y^2", "-2", "y_0", "y", "+", "y_0^2", "=", "r^2"],
                      44, {2: YELLOW, 5: YELLOW, 9: YELLOW, 12: YELLOW, 14: GOLD})
            line1.shift(np.array([LEFT_X - line1.get_left()[0], 2.3 - line1.get_center()[1], 0]))
            derive(self, eqs, line1, run_time=max(1.4, min(2.0, c.until("terms") - 0.1)))
            c.wait_until("terms")

            line2 = M(["x^2", "-2", "x_0", "x", "+", "y^2", "-2", "y_0", "y", "=", "r^2", "-", "x_0^2", "-", "y_0^2"],
                      44, {2: YELLOW, 7: YELLOW, 12: YELLOW, 14: YELLOW, 10: GOLD})
            line2.shift(np.array([LEFT_X - line2.get_left()[0], 1.35 - line2.get_center()[1], 0]))
            derive(self, line1, line2, run_time=1.8)

            gen, tag99 = general_eq()
            gen.shift(np.array([LEFT_X - gen.get_left()[0], -0.6 - gen.get_center()[1], 0]))
            self.play(*appear(gen), run_time=1.0)

            ba = Brace(pad_line(gen[2]), UP, buff=0.12, color=DIM)
            bb = Brace(pad_line(gen[7]), UP, buff=0.12, color=DIM)
            bc = Brace(pad_line(gen[10]), UP, buff=0.12, color=DIM)
            la = M(["-2", "x_0"], 38, {1: YELLOW}).next_to(ba, UP, buff=0.08)
            lb = M(["-2", "y_0"], 38, {1: YELLOW}).next_to(bb, UP, buff=0.08)
            lc = M(["x_0^2", "+", "y_0^2", "-", "r^2"], 38, {0: YELLOW, 2: YELLOW, 4: GOLD}).next_to(bc, UP, buff=0.08)
            lc.shift(RIGHT * max(0.0, lb.get_right()[0] + 0.35 - lc.get_left()[0]))
            self.play(GrowFromCenter(ba), GrowFromCenter(bb),
                      *fly(VGroup(line2[1], line2[2]), la),
                      *fly(VGroup(line2[6], line2[7]), lb),
                      run_time=1.6)
            c.wait_until("plus a constant")
            self.play(FlashAround(VGroup(*line2[10:15]), run_time=1.6, time_width=1.5),
                      *during([GrowFromCenter(bc)], 0.3, 0.8), *during(appear(lc), 0.45, 1.0), run_time=1.6)
            c.wait_until("general")

            tag99.next_to(gen, RIGHT, buff=0.45)
            self.play(*appear(tag99), run_time=1.0)
            c.wait_until("three numbers")
            # a tight ring per coefficient glyph (FlashAround's ring spilled onto the x and y)
            rings = [Ellipse(width=g.width + 0.16, height=g.height + 0.14, color=YELLOW, stroke_width=4).move_to(g)
                     for g in (gen[2], gen[7], gen[10])]
            self.play(*[Succession(FadeIn(r, scale=1.4), FadeOut(r)) for r in rings], run_time=1.5)
            c.wait_until("hide")

            hs_ax, hs_circ, hs_q, hs_eq, hs_tag = handover_parts()
            self.play(*during([FadeOut(cdot), FadeOut(radius), FadeOut(dx), FadeOut(dy)], 0, 0.5),
                      *during([ReplacementTransform(ax, hs_ax), ReplacementTransform(circle, hs_circ)], 0, 0.8),
                      *during(appear(hs_q), 0.5, 1.0),
                      run_time=1.8)
            c.wait_until("ask")

            self.play(*during(disappear(eqs, line1, line2, cap, ba, bb, bc, la, lb, lc), 0, 0.45),
                      *during([gen.animate.move_to(hs_eq), tag99.animate.move_to(hs_tag)], 0.35, 1.0),
                      run_time=1.8)

        # handover: the final frame is exactly handover_shot()
        self.remove(gen, tag99)
        self.add(hs_eq, hs_tag)
        self.wait(1.0)


def pad_line(glyph, width=0.62):
    """An invisible span over a single letter, so its brace reads as a brace, not a caret."""
    top = glyph.get_top()
    y = max(top[1], glyph.get_center()[1] + 0.18)
    return Line(np.array([top[0] - width / 2, y, 0]), np.array([top[0] + width / 2, y, 0]))


def shrink_anim(m):
    return m.animate.scale(SHRINK, about_point=A).shift(B)
