"""Chapter 4, scene 5: two consequences of the many-valued log. Clips c4.cons.1 – c4.cons.4."""
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

TAU_ = 2 * PI
U = 0.78                          # screen units per w-plane unit
O = np.array([-5.0, -0.35, 0])    # w-plane origin on screen
XR, YR = (-1.0, 4.3), (-3.6, 4.5)
Z1 = (2.0, -2.2)                  # the generic z of the first bullet
ZX, ZY = 3.0, 4.0                 # the example z = 3 + 4i


def P(x, y, o=O, u=U):
    return o + u * np.array([x, y, 0])


def w_plane(xr=XR, yr=YR, o=O, u=U, im_side=RIGHT):
    """The look of argand_plane() (ch2_s1_hook), with Re w / Im w and no unit circle."""
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(P(x, yr[0], o, u), P(x, yr[1], o, u), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(P(xr[0], y, o, u), P(xr[1], y, o, u), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0, o, u), P(xr[1], 0, o, u) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0], o, u), P(0, yr[1], o, u) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    re = MathTex(r"\mathrm{Re}\,w", font_size=34).next_to(xax.get_end(), DOWN, buff=0.15)
    im = MathTex(r"\mathrm{Im}\,w", font_size=34).next_to(yax.get_end(), im_side, buff=0.15)
    return VGroup(grid, xax, yax, re, im)


def ladder(x, y0, lo, hi, o=O, u=U, r=0.08):
    """GOLD dashed line at Re w = x, TEAL rungs y0 + 2πn within [lo, hi], fading dots past both ends."""
    line = DashedLine(P(x, lo, o, u), P(x, hi, o, u), dash_length=0.12, color=GOLD, stroke_width=3)
    rungs = VGroup()
    n = int(np.ceil((lo - y0) / TAU_))
    while y0 + n * TAU_ <= hi:
        rungs.add(Dot(P(x, y0 + n * TAU_, o, u), radius=r, color=TEAL))
        n += 1
    fades = VGroup()
    for k, op in enumerate((0.6, 0.35, 0.15)):
        fades.add(Dot(P(x, hi, o, u) + (0.17 * (k + 1)) * UP, radius=0.045, color=TEAL, fill_opacity=op))
        fades.add(Dot(P(x, lo, o, u) + (0.17 * (k + 1)) * DOWN, radius=0.045, color=TEAL, fill_opacity=op))
    return VGroup(line, rungs, fades)


def rung_brace(x, ya, yb, o=O, u=U, side=LEFT, size=36):
    seg = Line(P(x, ya, o, u), P(x, yb, o, u))
    br = Brace(seg, direction=side, buff=0.18, color=TEAL)
    lab = MathTex(r"2\pi i", font_size=size, color=TEAL).next_to(br, side, buff=0.12)
    return VGroup(br, lab)


def example_shot():
    """The 3 + 4i round trip: w-plane, principal strip, the ladder, z and its principal rung.
    Indices: 0 plane, 1 strip, 2 strip label, 3 ladder, 4 brace, 5 z dot, 6 z label, 7 tag."""
    plane = w_plane()
    strip = Rectangle(width=U * (XR[1] - XR[0]), height=U * TAU_, stroke_width=0,
                      fill_color=GREEN, fill_opacity=0.13).move_to(P((XR[0] + XR[1]) / 2, 0))
    strip.set_z_index(-2)
    top = Line(P(XR[0], PI), P(XR[1], PI), color=GREEN, stroke_width=2, stroke_opacity=0.7)   # π included
    bot = DashedLine(P(XR[0], -PI), P(XR[1], -PI), dash_length=0.1, color=GREEN, stroke_width=2,
                     stroke_opacity=0.7)                                                # −π excluded
    strip_g = VGroup(strip, top, bot)
    strip_lab = T("principal values", size=30, color=GREEN).next_to(P(XR[1], PI), RIGHT, buff=0.55) \
        .shift(0.45 * DOWN)
    lad = ladder(ZX, ZY, YR[0], YR[1])
    lad[1][0].set_color(GREEN)                      # the rung at 4 − 2π
    brace = rung_brace(ZX, ZY - TAU_, ZY)
    zdot = Dot(P(ZX, ZY), radius=0.11, color=YELLOW).set_z_index(2)
    zlab = MathTex("3 + 4i", font_size=38, color=YELLOW).next_to(zdot, RIGHT, buff=0.2)
    tag = T("principal value", size=30, color=GREEN).next_to(lad[1][0], RIGHT, buff=0.25)
    return VGroup(plane, strip_g, strip_lab, lad, brace, zdot, zlab, tag)


class Consequences(NarratedScene):
    def construct(self):
        shot = example_shot()
        plane = shot[0]
        heading = T("Consequences:", size=44).move_to([-0.4, 3.35, 0], aligned_edge=LEFT)
        b1 = MathTex(r"\bullet\ \ln e^{z} = z + ", r"2\pi i n", font_size=42)
        b1[1].set_color(TEAL)
        b1.next_to(heading, DOWN, buff=0.35, aligned_edge=LEFT).shift(0.3 * RIGHT)

        # ---------------- clip 1: ln e^z
        with self.say("c4.cons.1") as c:
            self.play(FadeIn(plane), run_time=1.0)
            c.wait_until(own_word=heading)
            self.play(*appear(heading), run_time=1.0)
            c.wait_until("first")

            zpt = P(*Z1)
            zdot = Dot(zpt, radius=0.11, color=YELLOW).set_z_index(2)
            zlab = MathTex("z", font_size=40, color=YELLOW).next_to(zdot, LEFT, buff=0.2).shift(0.3 * DOWN)
            self.play(*appear(b1), *appear(zdot, zlab), run_time=1.2)  # early: the bullet is read over this line
            c.wait_until("to the zed")

            ez = Dot([1.4, -1.6, 0], radius=0.1, color=GOLD)
            ezlab = MathTex("e^{z}", font_size=42, color=GOLD).next_to(ez, RIGHT, buff=0.18)
            out = CurvedArrow(zpt + 0.15 * RIGHT, ez.get_center() + 0.15 * LEFT, angle=0.7, color=GOLD,
                              stroke_width=3)
            self.play(Create(out), *appear(ez, ezlab, lag=0.4), run_time=min(1.5, c.until("for real")))
            c.wait_until("for real")

            naive = MathTex(r"\ln e^{z} = z", font_size=44, color=RED).move_to([3.0, 0.75, 0])
            self.play(*appear(naive), run_time=1.0)
            c.wait_until("here")

            strike = Line(naive.get_left() + 0.1 * LEFT, naive.get_right() + 0.1 * RIGHT, color=RED,
                          stroke_width=5)
            self.play(GrowFromEdge(strike, LEFT), FlashAround(b1[1], run_time=1.5, time_width=1.5),
                      restyle(naive, op=0.45), run_time=1.5)
            c.wait_until("why")

            lad1 = ladder(Z1[0], Z1[1], YR[0], YR[1])
            br1 = rung_brace(Z1[0], Z1[1], Z1[1] + TAU_)
            back = VGroup(
                CurvedArrow(ez.get_center() + 0.15 * LEFT + 0.08 * UP, zpt + 0.17 * RIGHT + 0.08 * UP,
                            angle=0.5, color=TEAL, stroke_width=3),
                CurvedArrow(ez.get_center() + 0.12 * UP, lad1[1][1].get_center() + 0.15 * RIGHT,
                            angle=0.45, color=TEAL, stroke_width=3),
            )
            lnlab = MathTex(r"\ln", font_size=40, color=TEAL).move_to([0.2, 1.0, 0])
            self.play(FadeIn(lad1[0]), *[Create(a) for a in back], *appear(lnlab),
                      *during(appear(*lad1[1], *lad1[2], lag=0.1), 0.3, 1), GrowFromCenter(br1[0]),
                      *during(appear(br1[1]), 0.5, 1), run_time=1.6)
            c.wait_until("any rung")
            self.play(*flash(list(lad1[1]), color=TEAL, run_time=1.0), run_time=min(1.0, c.until()))

        # ---------------- clip 2: the 3 + 4i example
        strip_g, strip_lab, lad, brace, zdot2, zlab2, tag = shot[1:]
        prin = lad[1][0]
        prin.set_color(TEAL)
        with self.say("c4.cons.2") as c:
            c.wait_until("zed equals")
            sweep_clear(self, time_span(FadeIn(zdot2), 0.6, 1.2),
                        time_span(FadeIn(zlab2, shift=0.2 * DOWN), 0.7, 1.4),
                        keep=[plane, heading, b1], run_time=1.4)
            c.wait_until("strip")

            self.play(FadeIn(strip_g), *appear(strip_lab), run_time=1.4)
            c.wait_until("above")

            self.play(VShowPassingFlash(strip_g[1].copy().set_stroke(YELLOW, 5), time_width=0.5),
                      FlashAround(zdot2, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("down")

            self.play(FadeIn(lad[0]), *appear(*lad[1], *lad[2], lag=0.1), run_time=1.2)
            mover = zdot2.copy()
            self.play(mover.animate.move_to(prin), GrowFromCenter(brace[0]), *appear(brace[1]),
                      run_time=min(1.6, c.until("its real part")))
            self.remove(mover)
            prin.set_z_index(1)
            self.play(prin.animate.set_color(GREEN).scale(1.3), *appear(tag),
                      run_time=min(1.0, c.until("its real part")))
            c.wait_until("its real part")

            eq1 = MathTex(r"\ln e^{3+4i} = 3 + (4 - 2\pi)\,i", font_size=44).move_to([-0.8, -0.35, 0],
                                                                                     aligned_edge=LEFT)
            eq2 = MathTex(r"\approx 3 - 2.28\,i", font_size=44, color=GREEN)
            eq2.next_to(eq1, DOWN, buff=0.4, aligned_edge=LEFT).shift(1.55 * RIGHT)
            self.play(*appear(eq1), run_time=1.2)
            c.wait_until("about minus")
            self.play(*appear(eq2), run_time=1.0)
            c.wait_until("differ")

            neq = MathTex(r"\neq 3 + 4i", font_size=44, color=RED).next_to(eq2, RIGHT, buff=0.35)
            self.play(*appear(neq), FlashAround(zlab2, color=RED, run_time=1.2, time_width=1.5), run_time=1.2)

        # ---------------- clip 3: products
        S = 0.15                                     # screen units per unit of Im, for the columns
        CY = -0.2
        XS = [-4.65, -1.55, 1.55, 4.65]
        LO, HI = -4.4 * PI, 4.4 * PI

        def H(x, y):
            return np.array([x, CY + S * y, 0])

        grid = VGroup(*[Line(H(-6.3, k * PI), H(6.3, k * PI), stroke_width=1, color=DIM,
                             stroke_opacity=0.45 if k == 0 else 0.25) for k in range(-4, 5)])
        imlab = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(H(-6.3, HI), UP, buff=0.1) \
            .align_to(H(-6.3, 0), LEFT)

        def column(x, ys):
            line = DashedLine(H(x, LO), H(x, HI), dash_length=0.12, color=GOLD, stroke_width=3)
            dots = VGroup(*[Dot(H(x, y), radius=0.09, color=TEAL) for y in ys])
            fades = VGroup()
            for k, op in enumerate((0.6, 0.35, 0.15)):
                fades.add(Dot(H(x, HI) + 0.17 * (k + 1) * UP, radius=0.045, color=TEAL, fill_opacity=op))
                fades.add(Dot(H(x, LO) + 0.17 * (k + 1) * DOWN, radius=0.045, color=TEAL, fill_opacity=op))
            return line, dots, fades

        odd = [-3 * PI, -PI, PI, 3 * PI]
        even = [-4 * PI, -2 * PI, 0, 2 * PI, 4 * PI]
        cols = [column(XS[0], odd), column(XS[1], odd), column(XS[2], even), column(XS[3], even)]
        labs = [MathTex(s, font_size=38).move_to([x, -3.15, 0]) for s, x in
                zip([r"\ln z_1", r"\ln z_2", r"\ln z_1 + \ln z_2", r"\ln(z_1 z_2)"], XS)]

        b2 = MathTex(r"\bullet\ \ln(z_1 z_2) = \ln z_1 + \ln z_2", r"\ \ \text{modulo}\ ", r"2\pi i",
                     font_size=42)
        b2[2].set_color(TEAL)
        with self.say("c4.cons.3") as c:
            c.wait_until("about products")
            heading.generate_target()
            heading.target.move_to([-6.4, 3.4, 0], aligned_edge=LEFT)
            b1.generate_target()
            b1.target.next_to(heading.target, RIGHT, buff=0.7).align_to(heading.target, DOWN).shift(0.05 * DOWN)
            sweep_clear(self, time_span(MoveToTarget(heading), 0.5, 1.5), time_span(MoveToTarget(b1), 0.5, 1.5),
                        keep=[heading, b1], run_time=1.5)
            self.play(FadeIn(grid), *appear(imlab), run_time=1.0)
            c.wait_until("rule")

            b2.next_to(b1, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(*appear(b2), restyle(b1, op=0.45), run_time=1.2)  # early: the rule is read over this line
            c.wait_until("equals log zed one")

            for i in (0, 1):
                ln, dots, fades = cols[i]
                self.play(FadeIn(ln), *appear(*dots, *fades, lag=0.08), *appear(labs[i]),
                          run_time=min(1.2, c.until("plus log zed two" if i == 0 else "up to whole")))
                c.wait_until("plus log zed two" if i == 0 else "up to whole")

            a, b = cols[0][1][2], cols[1][1][2]          # π and π
            target = cols[2][1][3]                       # 2π
            self.play(*recolor([a, b], YELLOW), FadeIn(cols[2][0]), *appear(labs[2]), run_time=1.0)
            ca, cb = a.copy(), b.copy()
            target.set_color(YELLOW)
            self.play(*during([ca.animate.move_to(target), cb.animate.move_to(target)], 0, 0.8),
                      *during([FadeIn(target)], 0.7, 1), run_time=1.4)
            self.remove(ca, cb)
            rest = [d for d in cols[2][1] if d is not target]
            self.play(*recolor([a, b, target], TEAL), *appear(*rest, *cols[2][2], lag=0.08, shift=None),
                      run_time=min(1.2, c.until("sets")))
            c.wait_until("sets")

            ln4, dots4, fades4 = cols[3]
            self.play(FadeIn(ln4), *appear(*dots4, *fades4, lag=0.06, shift=None), *appear(labs[3]), run_time=1.0)
            ghost = VGroup(ln4, dots4, fades4).copy()
            self.play(ghost.animate.move_to([XS[2], ghost.get_y(), 0]), run_time=1.3)
            self.play(FadeOut(ghost), *flash([cols[2][1], dots4], color=TEAL, run_time=1.0), run_time=1.0)
            c.wait_until("pick")

            p3, p4 = cols[2][1][3], dots4[2]             # 2π on the left side, 0 on the right
            gb = Line(H(3.1, 0), H(3.1, 2 * PI))
            br = Brace(gb, direction=RIGHT, buff=0.0, color=TEAL)
            brl = MathTex(r"2\pi i", font_size=38, color=TEAL).next_to(br, RIGHT, buff=0.1)
            g1 = DashedLine(p3.get_center(), H(3.1, 2 * PI), dash_length=0.08, color=YELLOW, stroke_width=2)
            g2 = DashedLine(p4.get_center(), H(3.1, 0), dash_length=0.08, color=YELLOW, stroke_width=2)
            self.play(*recolor([p3, p4], YELLOW), p3.animate.scale(1.4), p4.animate.scale(1.4), run_time=1.0)
            self.play(Create(g1), Create(g2), GrowFromCenter(br), *appear(brl), run_time=1.5)
            c.wait_until("advice")
            self.play(FlashAround(b2[1:], run_time=1.5, time_width=1.5), b2[2].animate.set_color(YELLOW),
                      run_time=1.5)
            self.play(b2[2].animate.set_color(TEAL), run_time=0.6)

        # ---------------- clip 4: even ln 2 has a ladder
        O4, U4 = np.array([-3.6, -0.6, 0]), 0.4
        X4, Y4 = (-1.5, 2.5), (-6.6, 6.6)
        plane4 = w_plane(X4, Y4, O4, U4, im_side=LEFT)
        lad4 = ladder(np.log(2), 0.0, Y4[0], Y4[1], O4, U4)
        n0 = lad4[1][1]
        with self.say("c4.cons.4", gap=2.8) as c:
            sweep_clear(self, time_span(FadeIn(plane4), 0.6, 1.4), keep=[heading, b1, b2], run_time=1.4)
            c.wait_until("whole ladder")
            self.play(FadeIn(lad4[0]), *appear(*lad4[1], *lad4[2], lag=0.1, shift=None), run_time=1.4)
            c.wait_until("it's log two")
            eq4 = MathTex(r"\ln 2 + 2\pi i n", font_size=56).move_to([2.4, 0.6, 0])
            eq4[0][4:].set_color(TEAL)
            self.play(*appear(eq4), run_time=1.2)
            c.wait_until("real")

            real = T("the real ln 2", size=32, color=GREEN).next_to(n0, RIGHT, buff=0.3).shift(0.75 * UP)
            set_backstroke(real)
            self.play(n0.animate.set_color(GREEN).scale(1.4), *appear(real), run_time=1.2)
            self.play(FlashAround(n0, color=GREEN, run_time=1.2), FlashUnder(eq4[0][:3], color=GREEN, run_time=1.2),
                      run_time=1.2)
            c.wait_until("next")
            nxt = T("→ Part 5: 2", size=34, color=YELLOW)
            sup = MathTex("i", font_size=30, color=YELLOW).next_to(nxt, UR, buff=0.02).shift(0.12 * DOWN)
            nxt_g = VGroup(nxt, sup).move_to([4.6, -3.2, 0])
            self.play(*appear(nxt_g), run_time=1.0)  # early: a tag naming the next part

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
