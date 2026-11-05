"""Chapter 6, scene 2: the pendulum and simple harmonic motion. Clips c6.pend.1 – c6.pend.3.

Uses s3's shared pendulum(...) and x_graph() (same origin G0, K_T per second, amplitude R), and the
running example: angle = 20 deg * cos(PHI0 + OMEGA t), x(t) = 2 cos(omega t - pi/3).
"""
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

S3 = load_scene("ch6_s3_phasor")
OMEGA, PHI0, PEND_AMP = S3.OMEGA, S3.PHI0, S3.PEND_AMP
G0, K_T, T_MAX, R = S3.G0, S3.K_T, S3.T_MAX, S3.R
PIVOT, L_ROD = S3.FULL_PIVOT, S3.FULL_L
RIGHT_X = 3.7                     # centre of the right-hand column


def theta_of(phase):
    return PEND_AMP * np.cos(phase)


def bob_point(phase):
    th = theta_of(phase)
    return PIVOT + L_ROD * np.array([np.sin(th), -np.cos(th), 0.0])


def full_pendulum(phase):
    g = S3.pendulum(theta_of(phase))
    return VGroup(g, g.labels)


def graph_point(tau, phase):
    return G0 + np.array([K_T * tau, R * np.cos(phase), 0.0])


def other_curve(amp, phi):
    return ParametricFunction(
        lambda t: G0 + np.array([K_T * t, amp * np.cos(OMEGA * t + phi), 0.0]),
        t_range=[0, T_MAX, 0.05], color=DIM, stroke_width=3)


class Pendulum(NarratedScene):
    def construct(self):
        ph = ValueTracker(PHI0)          # pendulum phase
        tau = ValueTracker(0.0)          # graph time (s)
        state = {"run": False}

        def drive(m, dt):
            if state["run"]:
                tau.increment_value(dt)
                ph.set_value(PHI0 + OMEGA * tau.get_value())
        driver = VectorizedPoint(ORIGIN)
        driver.add_updater(drive)
        self.add(driver)

        # ============================================================ clip 1
        with self.say("c6.pend.1") as c:
            pend = S3.pendulum(PEND_AMP * 0.5)
            l_lbl, m_lbl, g_arrow, g_lbl = pend.labels
            self.play(*appear(pend, shift=None), run_time=min(1.2, c.until("weight")))
            c.wait_until("weight")
            self.play(*appear(m_lbl), run_time=0.8)
            c.wait_until("length")
            self.play(*appear(l_lbl), run_time=0.8)
            c.wait_until("gravity")
            self.play(GrowArrow(g_arrow), *appear(g_lbl), run_time=0.8)

            # one swing, there and back, starting and ending at rest at 10 degrees
            self.remove(pend, l_lbl, m_lbl, g_arrow, g_lbl)
            dyn = always_redraw(lambda: full_pendulum(ph.get_value()))
            self.add(dyn)
            swing_rt = max(2.5, min(3.6, c.until("angular displacement") - 0.1))
            self.play(ph.animate.set_value(PHI0 + TAU), run_time=swing_rt, rate_func=smooth)
            dyn.clear_updaters()
            self.remove(dyn)
            ph.set_value(PHI0)
            pend = S3.pendulum(PEND_AMP * 0.5)
            l_lbl, m_lbl, g_arrow, g_lbl = pend.labels
            self.add(pend, l_lbl, m_lbl, g_arrow, g_lbl)

            # {angle}: the arc between vertical and rod
            arc = Arc(radius=1.2, start_angle=-PI / 2, angle=PEND_AMP * 0.5, arc_center=PIVOT,
                      color=YELLOW, stroke_width=5)
            x_lbl = MathTex("x(t)", font_size=40, color=YELLOW).move_to(PIVOT + np.array([0.85, -1.05, 0]))
            words = T("angular displacement", 28, DIM).next_to(x_lbl, RIGHT, buff=0.3)
            words.align_to(x_lbl, DOWN)
            c.wait_until("angular displacement")
            self.play(Create(arc), *appear(x_lbl, words, lag=0.4), run_time=1.4)
            c.wait_until("vertical")
            self.play(*flash([pend.vertical], color=YELLOW, run_time=1.2, time_width=1.5), run_time=1.2)

            # {omega}
            omega = MathTex(r"\omega = \sqrt{g/l}", font_size=52).move_to([RIGHT_X, 3.15, 0])
            c.wait_until("omega")
            self.play(*appear(omega), run_time=1.0)
            c.wait_until("strength of gravity")
            self.play(FlashAround(g_lbl, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("length", nth=1)
            self.play(FlashAround(l_lbl, run_time=1.2, time_width=1.5), run_time=1.2)

            # {given}
            given = T("small swings  ·  physics next term", 28, DIM).next_to(omega, DOWN, buff=0.35)
            c.wait_until("given")
            self.play(*appear(given), run_time=1.0)

        # ============================================================ clip 2
        with self.say("c6.pend.2") as c:
            f = MathTex("x(t)", "=", "a", r"\cos", r"\omega t", "+", "b", r"\sin", r"\omega t",
                        font_size=48)
            num = T("(81)", 30, DIM)
            VGroup(f, num.next_to(f, RIGHT, buff=0.5)).move_to([RIGHT_X - 0.1, 0.9, 0])
            self.play(*appear(f, num, lag=0.4), run_time=1.2)  # early: (81) is the notes' line number

            # {cos} / {sin}
            ul_cos = underline(VGroup(f[2], f[3], f[4]), YELLOW)
            ul_sin = underline(VGroup(f[6], f[7], f[8]), YELLOW)
            c.wait_until("cos")
            self.play(GrowFromCenter(ul_cos), run_time=0.8)
            c.wait_until("sin")
            self.play(Transform(ul_cos, ul_sin), run_time=1.0)

            # {coeffs}
            tag_a = T("cosine coefficient", 28, BLUE)
            tag_a.move_to([f[2].get_x(), f.get_bottom()[1] - 0.6, 0])
            tag_b = T("sine coefficient", 28, BLUE)
            tag_b.move_to([f[6].get_x(), tag_a.get_y() - 0.6, 0])
            line_a = Line(f[2].get_bottom() + DOWN * 0.08, tag_a.get_top() + UP * 0.08,
                          color=BLUE, stroke_width=2)
            line_b = Line(f[6].get_bottom() + DOWN * 0.08, tag_b.get_top() + UP * 0.08,
                          color=BLUE, stroke_width=2)
            c.wait_until("coeffs")
            self.play(*disappear(ul_cos), *recolor(f[2], BLUE), *recolor(f[6], BLUE), run_time=1.0)
            c.wait_until(own_word=tag_a)
            self.play(GrowFromEdge(line_a, UP), *appear(tag_a), run_time=0.9)
            c.wait_until(own_word=tag_b)
            self.play(GrowFromEdge(line_b, UP), *appear(tag_b), run_time=0.9)

            # {shm}
            shm_t = T("simple harmonic motion", 36, YELLOW)
            shm_box = SurroundingRectangle(shm_t, color=YELLOW, buff=0.2, stroke_width=3)
            shm = VGroup(shm_box, shm_t).move_to([RIGHT_X - 0.1, tag_b.get_y() - 1.0, 0])
            c.wait_until("shm")
            self.play(GrowFromCenter(shm_box), *appear(shm_t, shift=None), run_time=1.2)

            # {graph}: the pendulum starts swinging and the pen starts plotting on the cue itself,
            # while the right column clears, the formula rises and the axes fade in under the pen
            graph = S3.x_graph()
            axes = graph.axes
            curve = graph.curve
            lab_op = ValueTracker(1.0)

            def pend_build():
                g = S3.pendulum(theta_of(ph.get_value()))
                op = lab_op.get_value()
                if op <= 0.01:
                    return VGroup(g)
                return VGroup(g, g.labels.set_opacity(op))
            pend_dyn = always_redraw(pend_build)
            drawn = always_redraw(lambda: curve.copy().pointwise_become_partial(
                curve, 0, max(min(tau.get_value() / T_MAX, 1.0), 1e-3)))

            def pen_op():
                return max(0.0, 1.0 - 2.0 * max(tau.get_value() - T_MAX, 0.0))

            def pen_build():
                t = min(tau.get_value(), T_MAX)
                p = graph_point(t, PHI0 + OMEGA * t)
                op = pen_op()
                tie = DashedLine(bob_point(ph.get_value()), p, color=DIM, stroke_width=2,
                                 dash_length=0.1).set_stroke(opacity=0.45 * op)
                dot = Dot(p, radius=0.08, color=BLUE).set_opacity(op)
                return VGroup(tie, dot)
            pen = always_redraw(pen_build)

            c.wait_until("graph")
            d_f = np.array([0, 3.35 - f.get_y(), 0])
            shm_target = shm.copy().scale(0.8).move_to([RIGHT_X - 0.1, 2.5, 0])
            self.remove(pend, l_lbl, m_lbl, g_arrow, g_lbl)
            self.add(pend_dyn, drawn, pen)
            state["run"] = True
            self.play(*during(disappear(omega, given), 0, 0.3),
                      *during(disappear(tag_a, tag_b, line_a, line_b, arc, x_lbl, words), 0, 0.45),
                      *during([lab_op.animate.set_value(0.0)], 0, 0.4),
                      *during([f.animate.shift(d_f), num.animate.shift(d_f),
                               Transform(shm, shm_target)], 0.1, 0.6),
                      *during(appear(axes, shift=None), 0.55, 1.0),
                      run_time=1.5)

        # ============================================================ clip 3
        with self.say("c6.pend.3") as c:
            # {omega_t}
            wt = [f[4], f[8]]
            ctr_lbl = MathTex(r"\omega t =", font_size=40, color=YELLOW)
            ctr = DecimalNumber(0, num_decimal_places=2, font_size=40, color=YELLOW)
            ctr_row = VGroup(ctr_lbl, ctr).arrange(RIGHT, buff=0.2)
            ctr_row.move_to([RIGHT_X - 1.5, 2.5, 0])
            ctr.set_value(OMEGA * tau.get_value() + 1.0 * OMEGA)
            ctr.next_to(ctr_lbl, RIGHT, buff=0.2)
            self.play(*swap(shm, ctr_row), *recolor(wt[0], YELLOW), *recolor(wt[1], YELLOW),
                      run_time=1.0)
            ctr.add_updater(lambda m: m.set_value(OMEGA * tau.get_value()))
            ctr.add_updater(lambda m: m.next_to(ctr_lbl, RIGHT, buff=0.2))

            # {grows}
            grows = T("+ ω every second", 30, DIM).next_to(ctr_row, RIGHT, buff=0.6)
            grows.align_to(ctr_lbl, DOWN)
            c.wait_until("grows")
            c.wait_until(own_word=grows)
            self.play(*appear(grows), run_time=1.0)

            # {repeat}: the first crest and the next one
            t1, t2 = (-PHI0) / OMEGA, (-PHI0 + TAU) / OMEGA
            p1, p2 = graph_point(t1, 0.0), graph_point(t2, 0.0)
            d1 = Dot(p1, radius=0.09, color=YELLOW)
            d2 = Dot(p2, radius=0.09, color=YELLOW)
            c.wait_until("repeat")
            self.play(FadeIn(d1, scale=0.5), FlashAround(d1, run_time=1.0, time_width=1.5, buff=0.12),
                      run_time=1.0)
            self.play(FadeIn(d2, scale=0.5), FlashAround(d2, run_time=1.0, time_width=1.5, buff=0.12),
                      run_time=1.0)

            # {period}
            brace = span_brace(p1, p2, direction=UP, color=TEAL)
            per = MathTex(r"2\pi/\omega", font_size=40, color=TEAL).next_to(brace, UP, buff=0.12)
            swing = T("one swing,\nthere and back", 28, TEAL, line_spacing=0.8)
            swing.next_to(per, RIGHT, buff=0.45)
            c.wait_until("period")
            ctr.clear_updaters()
            self.play(*during(disappear(ctr_row, grows), 0, 0.45),
                      *during([GrowFromCenter(brace)], 0.4, 1.0), run_time=1.4)
            self.play(*appear(swing, per, lag=0.5), run_time=1.4)

            # {fixed}: other starts, same period
            c2 = other_curve(1.1, 0.9)
            c3 = other_curve(1.55, 2.4)
            c.wait_until("fixed")
            self.play(Create(c2), Create(c3), run_time=min(1.8, c.until("but")))
            c.wait_until("stays the same")
            self.play(FlashAround(brace, color=TEAL, run_time=1.2, time_width=1.5), run_time=1.2)

        state["run"] = False
        for m in (pend_dyn, drawn, pen):
            m.clear_updaters()
        self.remove(pen)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not driver], run_time=1.0)
        self.remove(driver)
        self.wait(0.15)
