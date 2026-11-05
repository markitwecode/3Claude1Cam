"""Chapter 6, scene 1: hook: from i^i to the physical world; why a pendulum wants a complex number.
Clips c6.hook.1 – c6.hook.2."""
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
from lib.titles import title_card  # noqa: E402

PH = load_scene("ch6_s3_phasor")

# ---------------------------------------------------------------- layout
PIVOT = np.array([-3.7, 3.1, 0.0])     # big pendulum, centre-left
PEND_L = 3.0
NL_C = np.array([-3.7, -2.0, 0.0])     # number line centre (angle 0)
NL_K = 1.5 / (20 * DEGREES)            # screen units per radian of angle (20 deg -> 1.5)
PL_C = np.array([3.3, 0.25, 0.0])      # small Argand plane centre
PL_S = 0.75                            # scale of s3's plane


def to_right(mob):
    """s3's plane-space mobject, scaled down and moved to the right-hand plane."""
    return mob.scale(PL_S, about_point=PH.P0).shift(PL_C - PH.P0)


def small_plane():
    g = PH.argand_plane()
    g.remove(g.re_lbl, g.im_lbl)
    to_right(g)
    circ = to_right(PH.plane_circle())
    re_lbl = T("Re", 28, DIM).next_to(g.re_axis.get_end(), UP, buff=0.1).shift(LEFT * 0.2)
    im_lbl = T("Im", 28, DIM).next_to(g.im_axis.get_end(), RIGHT, buff=0.12).shift(DOWN * 0.1)
    return VGroup(g, circ, re_lbl, im_lbl)


def plane_arrow(phase, op=1.0):
    a = to_right(PH.phasor_arrow(phase))
    s = to_right(PH.shadow(phase))
    s[1].scale(1 / PL_S)                      # keep the shadow dot full size
    return VGroup(s, a).set_opacity(op)


def big_pendulum(theta):
    return PH.pendulum(theta, PIVOT, PEND_L, s=1.0, labels=False)


def angle_dot(theta, op=1.0):
    return Dot(NL_C + RIGHT * NL_K * theta, radius=0.12, color=YELLOW).set_opacity(op)


# i^i strip: log scale, n = 0 value at x = 0
LOG_K = 1.45                            # screen units per decade
V0 = np.exp(-PI / 2)
STRIP_Y = 0.0


def xlog(v):
    return LOG_K * (np.log10(v) - np.log10(V0))


def ii_strip():
    axis = Arrow(np.array([-6.0, STRIP_Y, 0]), np.array([6.2, STRIP_Y, 0]), buff=0, stroke_width=3,
                 color=FG, tip_length=0.2, max_tip_length_to_length_ratio=0.05)
    ticks, tlbls = VGroup(), VGroup()
    for k in range(-3, 3):
        x = xlog(10.0 ** k)
        ticks.add(Line([x, STRIP_Y - 0.1, 0], [x, STRIP_Y + 0.1, 0], color=DIM, stroke_width=2))
        src = "1" if k == 0 else f"10^{{{k}}}"
        tlbls.add(MathTex(src, font_size=30, color=DIM).move_to([x, STRIP_Y - 0.5, 0]))
    dots, nlbls = VGroup(), VGroup()
    for n in (1, 0, -1):
        x = xlog(np.exp(-PI / 2 - 2 * PI * n))
        dots.add(Dot([x, STRIP_Y, 0], radius=0.13, color=GREEN if n == 0 else TEAL))
        nlbls.add(MathTex(f"n={n}", font_size=30, color=GREEN if n == 0 else TEAL)
                  .move_to([x, STRIP_Y + 0.5, 0]))
    formula = MathTex(r"i^{\,i} = e^{-\pi/2 - 2\pi n}", font_size=56).move_to([-0.6, 2.0, 0])
    tag = T("real", 52, YELLOW).next_to(formula, RIGHT, buff=0.6)
    val = MathTex(r"e^{-\pi/2} \approx 0.208", font_size=40, color=GREEN).move_to([0, STRIP_Y - 1.45, 0])
    g = VGroup(axis, ticks, tlbls, dots, nlbls, formula, tag, val)
    g.axis, g.ticks, g.tlbls, g.dots, g.nlbls = axis, ticks, tlbls, dots, nlbls
    g.formula, g.tag, g.val = formula, tag, val
    return g.shift(DOWN * 0.3)


# icons for {things}
ICON_Y = 0.7
ICON_X = (-4.4, 0.0, 4.4)


def ac_icon(center):
    c = np.array(center)
    ring = Circle(radius=0.7, color=GOLD, stroke_width=4).move_to(c)
    sim = MathTex(r"\sim", font_size=80, color=GOLD).move_to(c)
    leads = VGroup(Line(c + LEFT * 1.4, c + LEFT * 0.7), Line(c + RIGHT * 0.7, c + RIGHT * 1.4))
    leads.set_stroke(FG, 3)
    return VGroup(leads, ring, sim)


def wave_icon(center):
    c = np.array(center)
    w1 = FunctionGraph(lambda x: 0.28 * np.sin(2.6 * x), x_range=[-1.5, 1.5], color=BLUE,
                       stroke_width=4).move_to(c + UP * 0.25)
    w2 = FunctionGraph(lambda x: 0.2 * np.sin(2.6 * x + 1.2), x_range=[-1.3, 1.3], color=BLUE,
                       stroke_width=3).set_stroke(opacity=0.6).move_to(c + DOWN * 0.45)
    return VGroup(w1, w2)


class Hook(NarratedScene):
    def construct(self):
        clock = self.clock = PH.Clock()
        ticker = VectorizedPoint(ORIGIN)
        ticker.add_updater(lambda m, dt: clock.tick(dt))
        self.add(ticker)
        ph = clock.phase

        # ------------------------------------------------ clip 1
        with self.say("c6.hook.1") as c:
            card = title_card("Part 6 · Oscillations and the complex amplitude")
            card.title.scale_to_fit_width(12.4)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      run_time=1.0)
            self.play(*appear(card.course), run_time=0.8)  # early: title card
            self.play(*appear(card.part), run_time=0.8)  # early: title card
            c.wait_until("last")

            strip = ii_strip()
            sweep_clear(self, time_span(FadeIn(strip.axis, strip.ticks, strip.tlbls), 0.6, 1.2),
                        keep=[ticker], run_time=1.2)
            self.play(*appear(strip.formula, *strip.dots, lag=0.15),
                      *appear(strip.nlbls, strip.val, shift=None), run_time=1.0)
            c.wait_until("real number")
            self.play(*appear(strip.tag), FlashAround(strip.val, color=GREEN), run_time=0.8)
            c.wait_until("turn")

            core = VGroup(strip.formula, strip.tag, strip.axis, strip.dots)
            fine = [strip.ticks, strip.tlbls, strip.nlbls, strip.val]
            core.generate_target()
            core.target.scale(0.55).to_corner(UL, buff=0.5).set_opacity(DIMMED)
            self.play(*disappear(*fine), MoveToTarget(core), run_time=min(1.5, c.until("things")))
            c.wait_until("things")
            osc = T("anything that oscillates", 44, YELLOW).move_to([0, 2.9, 0])
            self.play(*disappear(core), run_time=0.8)
            c.wait_until("oscillates")
            self.play(*appear(osc), run_time=1.0)

            # three icons, each on its word
            p_icon = PH.pendulum(12 * DEGREES, np.array([ICON_X[0], ICON_Y + 1.0, 0]), 1.7,
                                 s=0.6, labels=False)
            ac = ac_icon([ICON_X[1], ICON_Y, 0])
            wv = wave_icon([ICON_X[2], ICON_Y, 0])
            words = [T(w, 32, FG).move_to([x, -1.1, 0])
                     for w, x in zip(("pendulum", "alternating current", "waves"), ICON_X)]
            c.wait_until("swinging pendulum")
            self.play(FadeIn(p_icon), *appear(words[0]),
                      run_time=min(1.0, c.until("alternating current")))
            c.wait_until("alternating current")
            self.play(FadeIn(ac), *appear(words[1]), run_time=min(1.0, c.until("wave on water")))
            c.wait_until("wave on water")
            self.play(FadeIn(wv), *appear(words[2]), run_time=1.0)  # early: "wave" names the icon
            c.wait_until("next_term")
            nt = T("differential equations: next term", 32, DIM).move_to([0, -2.6, 0])
            self.play(*appear(nt), run_time=1.0)
            c.wait_until("Here")
            self.play(*disappear(osc, ac, wv, *words, nt, lag=0.1), run_time=1.2)

        # ------------------------------------------------ clip 2
        with self.say("c6.hook.2") as c:
            pend0 = big_pendulum(PH.PEND_AMP * np.cos(PH.PHI0))
            self.play(ReplacementTransform(p_icon, pend0), run_time=min(1.8, c.until("real")))
            pend = always_redraw(lambda: big_pendulum(PH.PEND_AMP * np.cos(ph())))
            self.remove(pend0)
            self.add(pend)
            clock.start()
            c.wait_until("real")

            nl = VGroup(
                Line(NL_C + LEFT * 2.2, NL_C + RIGHT * 2.2, color=FG, stroke_width=3),
                Line(NL_C + DOWN * 0.15, NL_C + UP * 0.15, color=DIM, stroke_width=3),
                MathTex("0", font_size=30, color=DIM).move_to(NL_C + UP * 0.45 + LEFT * 0.35),
            )
            nl_lbl = T("one real number", 32, YELLOW).move_to(NL_C + DOWN * 0.65)
            dot_op = ValueTracker(0.0)
            adot = always_redraw(lambda: angle_dot(PH.PEND_AMP * np.cos(ph()), dot_op.get_value()))
            self.add(adot)
            self.play(FadeIn(nl), dot_op.animate.set_value(1.0), run_time=1.0)
            c.wait_until(own_word=nl_lbl)
            self.play(*appear(nl_lbl), run_time=1.0)
            c.wait_until("question")

            qmark = T("?", 150, YELLOW).move_to(PL_C + UP * 0.45)
            why = T("why complex?", 40, YELLOW).next_to(qmark, DOWN, buff=0.3)
            question = VGroup(qmark, why)
            self.play(*appear(question, shift=None), run_time=1.0)
            c.wait_until("tease")

            plane = small_plane()
            arr_op = ValueTracker(0.0)
            arr = always_redraw(lambda: plane_arrow(ph(), arr_op.get_value()).set_z_index(3))
            self.add(arr)
            self.play(*swap(question, plane), time_span(arr_op.animate.set_value(1.0), 0.8, 1.6),
                      run_time=1.6)
            c.wait_until("payoff")

            pay = MathTex(r"\text{calculus} \;\to\; \text{algebra}", font_size=44,
                          color=YELLOW).move_to(PL_C + DOWN * 3.3)
            self.play(*appear(pay), run_time=1.0)

        # ------------------------------------------------ end: everything out, pendulum last
        for m in (adot, arr):
            m.clear_updaters()
        self.play(*disappear(plane, arr, pay, nl, nl_lbl, adot), run_time=0.9)
        pend.clear_updaters()
        self.play(FadeOut(pend), run_time=0.9)
        self.wait(0.15)
