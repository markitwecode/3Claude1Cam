"""Chapter 4, scene 4: the ladder for 2i: ln 2i = ln 2 + i(pi/2 + 2 pi n). Clips c4.ladder.1 – c4.ladder.4."""
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

# z-plane (right third), same look as ch2_s1_hook.argand_plane (copied)
U_Z = 1.2
O_Z = np.array([4.7, -0.9, 0])

# w-plane (hero): anisotropic, so the tall ladder fits
W_O = np.array([-1.4, -0.2, 0])
W_SX = 2.0      # screen units per unit of Re w
W_SY = 0.2      # screen units per unit of Im w (2 pi -> 1.26)


def ZP(x, y):
    return O_Z + U_Z * np.array([x, y, 0])


def WP(x, y, origin=None, sx=W_SX, sy=W_SY):
    o = W_O if origin is None else np.asarray(origin, dtype=float)
    return o + np.array([sx * x, sy * y, 0])


def z_plane(xr=(-1.2, 1.1), yr=(-1.3, 2.5), unit=False):
    """Re/Im axes, faint grid (argand_plane look); unit circle optional."""
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(ZP(x, yr[0]), ZP(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(ZP(xr[0], y), ZP(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(ZP(xr[0], 0), ZP(xr[1], 0) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.06)
    yax = Arrow(ZP(0, yr[0]), ZP(0, yr[1]) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.05)
    re = T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    g = VGroup(grid, xax, yax, re, im)
    if unit:
        g.add(Circle(radius=U_Z, color=DIM, stroke_width=2).move_to(O_Z))
    return g


def w_plane(origin=None, sx=W_SX, sy=W_SY, xr=(-0.25, 1.4), yr=(-17.0, 17.0)):
    """The w-plane: argand look with "Re w" / "Im w", no unit circle."""
    def p(x, y):
        return WP(x, y, origin, sx, sy)
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(p(x, yr[0]), p(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(-15, 16, 5):
        if y and yr[0] <= y <= yr[1]:
            grid.add(Line(p(xr[0], y), p(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(p(xr[0], 0), p(xr[1], 0) + 0.2 * RIGHT, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.06)
    yax = Arrow(p(0, yr[0]), p(0, yr[1]) + 0.2 * UP, buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.03)
    re = T("Re w", size=30).next_to(xax.get_end(), UP, buff=0.15).align_to(xax.get_end(), RIGHT)
    im = T("Im w", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    return VGroup(grid, xax, yax, re, im)


def ladder(origin=None, sx=W_SX, sy=W_SY, ns=(-2, -1, 0, 1, 2), n_fade=3, fade_step=0.28,
           y_lo=-3.6, y_hi=3.5):
    """The ladder of ln 2i in the w-plane whose origin is at `origin` (screen point).

    Returns a VGroup with parts:
      .line        GOLD dashed vertical line at Re w = ln 2 (screen y from y_lo to y_hi)
      .ln2         VGroup(tick, label "ln 2") on the Re axis
      .pi2         VGroup(tick, label "pi/2") on the Im axis
      .dots        dict n -> Dot at ln 2 + i(pi/2 + 2 pi n); n = 0 GREEN, others TEAL
      .tag         GREEN "principal value" right of the n = 0 dot
      .fade_top / .fade_bot   VGroups of fading TEAL dots beyond the end rungs
      .brace, .brace_label    TEAL brace "2 pi i" between rungs 0 and 1 (left side)
      .point(n)    screen point of rung n
    """
    o = W_O if origin is None else np.asarray(origin, dtype=float)

    def p(x, y):
        return WP(x, y, o, sx, sy)

    def point(n):
        return p(LN2, PI / 2 + 2 * PI * n)

    x = p(LN2, 0)[0]
    line = DashedLine([x, y_lo, 0], [x, y_hi, 0], dash_length=0.12, dashed_ratio=0.55,
                      color=GOLD, stroke_width=2.5)
    t1 = Line(p(LN2, 0) + 0.09 * UP, p(LN2, 0) + 0.09 * DOWN, color=GOLD, stroke_width=3)
    l1 = MathTex(r"\ln 2", font_size=34, color=GOLD).next_to(t1, DR, buff=0.08)
    set_backstroke(l1)
    ln2 = VGroup(t1, l1)
    yp = p(0, PI / 2)
    t2 = Line(yp + 0.09 * LEFT, yp + 0.09 * RIGHT, color=YELLOW, stroke_width=3)
    l2 = MathTex(r"\pi/2", font_size=34, color=YELLOW).next_to(t2, LEFT, buff=0.12)
    pi2 = VGroup(t2, l2)
    dots = {n: Dot(point(n), radius=0.09 if n == 0 else 0.08, color=GREEN if n == 0 else TEAL)
            for n in ns}
    tag = T("principal value", size=30, color=GREEN).next_to(dots[0], RIGHT, buff=0.25).shift(0.38 * UP)
    top, bot = point(max(ns)), point(min(ns))
    fade_top = VGroup(*[Dot(top + (k + 1) * fade_step * UP, radius=0.07 - 0.01 * k, color=TEAL,
                            fill_opacity=0.6 - 0.2 * k) for k in range(n_fade)])
    fade_bot = VGroup(*[Dot(bot + (k + 1) * fade_step * DOWN, radius=0.07 - 0.01 * k, color=TEAL,
                            fill_opacity=0.6 - 0.2 * k) for k in range(n_fade)])
    brace = Brace(Line(point(0), point(1)), direction=LEFT, buff=0.18, color=TEAL)
    brace_label = MathTex(r"2\pi i", font_size=36, color=TEAL).next_to(brace, LEFT, buff=0.12)
    g = VGroup(line, ln2, pi2, *dots.values(), tag, fade_top, fade_bot, brace, brace_label)
    g.line, g.ln2, g.pi2, g.dots, g.tag = line, ln2, pi2, dots, tag
    g.fade_top, g.fade_bot, g.brace, g.brace_label = fade_top, fade_bot, brace, brace_label
    g.point = point
    return g


class Ln2i(NarratedScene):
    def construct(self):
        # ---------------- clip 1: 2i in polar form
        with self.say("c4.ladder.1") as c:
            zpl = z_plane()
            zdot = Dot(ZP(0, 2), radius=0.1, color=YELLOW).set_z_index(3)
            zlab = MathTex("2i", font_size=40, color=YELLOW).next_to(zdot, RIGHT, buff=0.2)
            self.play(FadeIn(zpl), run_time=1.0)
            self.play(FadeIn(zdot, scale=0.5), *appear(zlab), run_time=1.0)
            c.wait_until("form")

            eq1 = MathTex("z", "=", "2i", "=", "2", r"e^{i(\pi/2", "+", r"2\pi n", ")}", font_size=56)
            eq1[2].set_color(YELLOW)
            eq1[4].set_color(GOLD)
            eq1[7].set_color(TEAL)
            eq1.move_to([-2.4, 2.3, 0])
            self.play(*appear(eq1), run_time=1.0)  # early: the whole form, then walked
            arc = Arc(radius=0.42, start_angle=0, angle=PI / 2, arc_center=O_Z, color=YELLOW, stroke_width=4)
            alab = MathTex(r"\pi/2", font_size=34, color=YELLOW).move_to(O_Z + 1.0 * np.array([0.64, 0.77, 0]))
            self.play(Create(arc), *appear(alab), run_time=1.0)
            c.wait_until("every version")
            sweep = Arc(radius=0.66, start_angle=PI / 2, angle=2 * PI, arc_center=O_Z, color=TEAL,
                        stroke_width=3).add_tip(tip_length=0.16)
            slab = MathTex(r"+\,2\pi n", font_size=34, color=TEAL).next_to(alab, RIGHT, buff=0.12)
            self.play(Create(sweep), run_time=1.5, rate_func=linear)
            self.play(*appear(slab), run_time=0.6)
            c.wait_until("read")

            seg = Line(O_Z, ZP(0, 2), color=GOLD, stroke_width=6).set_z_index(1)
            mlab = MathTex("2", font_size=40, color=GOLD).next_to(seg, LEFT, buff=0.18)
            self.play(Create(seg), *appear(mlab), FlashUnder(eq1[4], color=GOLD, buff=0.08), run_time=1.2)
            c.wait_until("argument")
            self.play(FlashAround(VGroup(eq1[5][2:], eq1[6], eq1[7]), color=YELLOW, time_width=1.5),
                      FlashAround(VGroup(alab, slab), color=TEAL, time_width=1.5), run_time=1.6)

        # ---------------- clip 2: take the log
        with self.say("c4.ladder.2") as c:
            self.play(*restyle_list([sweep], 0.35), FlashUnder(eq1[4], color=GOLD, buff=0.08, time_width=1.5),
                      FlashAround(VGroup(*eq1[5][3:], eq1[6], eq1[7]), color=TEAL, time_width=1.5),
                      run_time=1.4)
            c.wait_until("result")
            eq2 = MathTex(r"\ln z", "=", r"\ln", "2", "+", "i(", r"\pi/2", "+", r"2\pi n", ")", font_size=56)
            eq2[3].set_color(GOLD)
            eq2[6].set_color(YELLOW)
            eq2[8].set_color(TEAL)
            eq2.move_to([-2.4, 0.1, 0])
            self.play(*appear(eq2), run_time=1.2)
            c.wait_until("re")

            bre = Brace(VGroup(eq2[2], eq2[3]), DOWN, buff=0.15, color=BLUE)
            tre = T("Re", size=46, color=BLUE).next_to(bre, DOWN, buff=0.12)
            self.play(GrowFromCenter(bre), *appear(tre), run_time=1.0)
            c.wait_until("about")
            approx = MathTex(r"\ln 2 \approx 0.69", font_size=48, color=GOLD).next_to(tre, DOWN, buff=0.2)
            self.play(*appear(approx), run_time=1.0)
            c.wait_until("im")
            bim = Brace(VGroup(*eq2[5:10]), DOWN, buff=0.15, color=PINK)
            tim = T("Im", size=46, color=PINK).next_to(bim, DOWN, buff=0.12)
            self.play(GrowFromCenter(bim), *appear(tim), run_time=1.0)

        # ---------------- clip 3: plot the values: the ladder
        with self.say("c4.ladder.3") as c:
            eqs = VGroup(eq1, eq2, bre, tre, approx, bim, tim)
            eqs.generate_target()
            eqs.target.scale_to_fit_width(4.3).to_corner(UL, buff=0.55)
            wpl = w_plane()
            lad = ladder()
            lad.tag.shift(0.16 * UP)   # clear of "Re w"
            zitems = [zdot, zlab, arc, alab, sweep, slab, seg, mlab]
            self.play(MoveToTarget(eqs), *during([FadeIn(wpl)], 0.45, 1.0),
                      *during(set_alpha(zitems, 0.35), 0.0, 0.6), run_time=2.0)
            c.wait_until("line")

            self.play(Create(lad.line), run_time=1.6)
            c.wait_until("at log two")
            self.play(Create(lad.ln2[0]), *appear(lad.ln2[1]), run_time=1.0)
            c.wait_until("principal")

            self.play(FadeIn(lad.dots[0], scale=0.5), Create(lad.pi2[0]), *appear(lad.pi2[1]), run_time=1.2)
            c.wait_until("the principal value")
            self.play(*appear(lad.tag), run_time=1.0)
            c.wait_until("rungs")

            nl = {}
            for n in (1, -1, 2, -2):
                nl[n] = MathTex(f"n={n}".replace("-", "-"), font_size=30, color=DIM) \
                    .next_to(lad.dots[n], RIGHT, buff=0.25)
            self.play(FadeIn(lad.dots[1], scale=0.5), *appear(nl[1]), run_time=0.9)
            self.play(FadeIn(lad.dots[-1], scale=0.5), *appear(nl[-1]), run_time=0.9)
            c.wait_until("two and minus two")
            self.play(FadeIn(lad.dots[2], scale=0.5), *appear(nl[2]), run_time=0.7)
            self.play(FadeIn(lad.dots[-2], scale=0.5), *appear(nl[-2]), run_time=0.7)
            c.wait_until("and so on")
            self.play(*appear(*lad.fade_top, *lad.fade_bot, lag=0.15, shift=None), run_time=1.2)
            c.wait_until("brace")

            self.play(GrowFromCenter(lad.brace), *appear(lad.brace_label), run_time=1.2)
            c.wait_until("every rung")
            self.play(*flash([lad.dots[n] for n in (-2, -1, 0, 1, 2)], color=TEAL, time_width=1.5),
                      run_time=1.6)

        # ---------------- clip 4: a height, not an angle; and every rung works
        with self.say("c4.ladder.4") as c:
            c.wait_until("quote")
            cap = T("“It’s not the angle anymore.\nThis is the actual value.”",
                    size=28, slant=ITALIC, line_spacing=1.1)
            cap.move_to([-4.25, -2.6, 0])
            self.play(FlashAround(lad.pi2[1], color=YELLOW, time_width=1.5), *appear(cap), run_time=1.4)
            warc = Arc(radius=0.45, start_angle=0, angle=PI / 2, arc_center=W_O, color=YELLOW, stroke_width=4)
            self.play(Create(warc), run_time=0.9)
            strike = Line(W_O + np.array([0.05, 0.6, 0]), W_O + np.array([0.6, 0.05, 0]),
                          color=RED, stroke_width=6)
            self.play(Create(strike), run_time=0.7)
            c.wait_until("height")

            hlab = MathTex(r"\pi/2 \approx 1.57", r",\ \text{a height}", font_size=34, color=YELLOW)
            hlab.next_to(lad.pi2[0], LEFT, buff=0.12)
            self.play(*swap(lad.pi2[1], hlab), run_time=1.2)
            c.wait_until("check")

            ns = (-2, -1, 0, 1, 2)
            arrows = [Arrow(lad.point(n), zdot.get_center(), buff=0.14, stroke_width=2.5, color=GOLD,
                            max_tip_length_to_length_ratio=0.04) for n in ns]
            ew = MathTex("e^w", font_size=40, color=GOLD).move_to([2.4, 2.6, 0])
            self.play(*during(disappear(lad.tag, *nl.values(), warc, strike), 0.0, 0.35),
                      *restyle_list([zdot, zlab], 1.0),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                      *during(appear(ew), 0.5, 1.0), run_time=2.2)
            c.wait_until("land on")
            self.play(Flash(zdot, color=YELLOW, line_length=0.25, flash_radius=0.3), run_time=1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)


def restyle_list(mobs, op):
    return set_alpha(mobs, op)
