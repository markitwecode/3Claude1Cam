"""Chapter 6, scene 5: amplitude and phase from the start (notes p. 28). Clips c6.ex.1 – c6.ex.5."""
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
PHI0 = S3.PHI0
ang = S3.ang

LX = -6.3                                  # left column edge
PC4, U4, EXT4 = np.array([3.6, 0.35, 0.0]), 1.5, 2.0     # clip 4: the triangle, zoomed in
PC5, U5, EXT5 = np.array([3.5, -0.1, 0.0]), 1.0, 2.9     # clip 5: the running plane (c = 1)
PEND_PIVOT = np.array([-3.2, 3.25, 0.0])
V_LEN = PI                                 # omega |A| with omega = pi/2, |A| = 2


def left_at(m, y, x=LX):
    m.move_to([0, y, 0])
    m.align_to(np.array([x, 0, 0]), LEFT)
    return m


def tex(*parts, size=44, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def moves(mobs, fn):
    """MoveToTarget for each on-screen piece, after fn arranges their targets as a group."""
    for m in mobs:
        m.generate_target()
    fn(VGroup(*[m.target for m in mobs]))
    return [MoveToTarget(m) for m in mobs]


# ---------------------------------------------------------------- clip-5 plane pieces (c = 1)
def gold_arrow(phase, op=1.0):
    a = Arrow(PC5, PC5 + 2 * U5 * ang(phase), buff=0, stroke_width=6, color=GOLD,
              tip_length=0.26, max_tip_length_to_length_ratio=0.3)
    return a.set_opacity(op).set_z_index(3)


def vel_arrow(phase, op=1.0):
    a = Arrow(PC5, PC5 + V_LEN * U5 * ang(phase + PI / 2), buff=0, stroke_width=6, color=PURPLE,
              tip_length=0.26, max_tip_length_to_length_ratio=0.3)
    return a.set_opacity(op).set_z_index(2)


def drop(tip, color, dot_color):
    foot = np.array([tip[0], PC5[1], 0.0])
    if abs(tip[1] - foot[1]) > 0.08:
        line = DashedLine(tip, foot, color=color, stroke_width=2.5, dash_length=0.08)
    else:
        line = Line(foot + UP * 0.001, foot, color=color, stroke_width=2.5)
    return VGroup(line, Dot(foot, radius=0.1, color=dot_color).set_z_index(4))


def x_shadow(phase, op=1.0):
    return drop(PC5 + 2 * U5 * ang(phase), DIM, BLUE).set_opacity(op)


def v_shadow(phase, op=1.0):
    return drop(PC5 + V_LEN * U5 * ang(phase + PI / 2), PURPLE, PURPLE).set_opacity(op)


def v_label(phase, op=1.0):
    x = PC5[0] + V_LEN * U5 * np.cos(phase + PI / 2)
    lbl = MathTex("v(t)", font_size=32, color=PURPLE).move_to([min(x, 5.75), PC5[1] + 0.8, 0])
    set_backstroke(lbl, width=5)
    return lbl.set_opacity(op)


class Example(NarratedScene):
    def dyn(self, build, op0=0.0):
        tr = ValueTracker(op0)
        mob = always_redraw(lambda: build(tr.get_value()))
        return mob, tr

    def construct(self):
        clock = S3.Clock()
        ticker = VectorizedPoint(ORIGIN)
        ticker.add_updater(lambda m, dt: clock.tick(dt))
        self.add(ticker)
        ph = clock.phase

        # ============================================================ clip 1: the start
        with self.say("c6.ex.1") as c:
            fact1 = tex("x(0)", "=", "c", size=52)
            fact1[2].set_color(GOLD)
            fact2 = tex("v(0)", r"\equiv", r"\dot{x}(0)", "=", r"\sqrt{3}\,c\,\omega", size=52)
            fact2[4].set_color(GOLD)
            VGroup(fact1, fact2).arrange(RIGHT, buff=1.3).move_to(UP * 0.9)
            brace = Brace(VGroup(fact1, fact2), DOWN, buff=0.25, color=DIM)
            start_lbl = T("the start", 38, DIM).next_to(brace, DOWN, buff=0.15)
            question = T("amplitude?     phase?", 44, YELLOW).move_to(DOWN * 1.9)

            c.wait_until("start")
            self.play(*appear(fact1), run_time=1.0)
            c.wait_until("velocity")
            self.play(*appear(fact2), run_time=1.2)

            c.wait_until("facts")
            self.play(GrowFromCenter(brace), *appear(start_lbl), run_time=1.2)

            c.wait_until("find")
            self.play(*appear(question), run_time=1.0)

        # ============================================================ clip 2: at t = 0
        with self.say("c6.ex.2") as c:
            top = [fact1, fact2, brace, start_lbl]
            self.play(*moves(top, lambda g: g.scale(0.77).to_corner(UL, buff=0.45)),
                      *moves([question], lambda g: g.scale(0.8).to_corner(UR, buff=0.5)),
                      run_time=1.5)
            zero = tex(r"e^{i\omega\cdot 0} = 1", size=36, color=DIM)
            zero.next_to(question, DOWN, buff=0.45)
            c.wait_until("just one")
            self.play(*appear(zero), run_time=1.0)

            line1 = tex("x(0)", "=", r"\mathrm{Re}(A)", "=", "c")
            line1[4].set_color(GOLD)
            left_at(line1, 1.0, LX + 0.3)
            c.wait_until("xzero")
            self.play(*appear(line1), run_time=1.2)
            self.play(FlashAround(line1[2], run_time=1.5, time_width=1.5), run_time=1.5)

            line2 = tex(r"\dot{x}(0)", "=", r"\mathrm{Re}(i\omega A)", "=", r"\sqrt{3}\,c\,\omega")
            line2[4].set_color(GOLD)
            left_at(line2, -0.15, LX + 0.3)
            c.wait_until("vzero")
            self.play(*appear(line2), run_time=1.2)
            self.play(FlashAround(line2[2], run_time=1.5, time_width=1.5), run_time=1.5)

        # ============================================================ clip 3: solve for A
        with self.say("c6.ex.3") as c:
            sweep_clear(self,
                        *moves([line1], lambda g: left_at(g, 3.15)),
                        *moves([line2], lambda g: left_at(g, 2.15)),
                        keep=[line1, line2, question, ticker], run_time=1.4)

            a_line = tex("A", "=", "c", "+", r"i\beta")
            a_line[2].set_color(BLUE)
            a_line[4].set_color(PINK)
            left_at(a_line, 0.95)
            c.wait_until("write")
            self.play(*appear(a_line), run_time=1.0)

            mult = tex(r"i\omega A", "=", r"i\omega", "c", r"-\omega\beta")
            mult[3].set_color(BLUE)
            mult[4].set_color(BLUE)
            left_at(mult, -0.1)
            c.wait_until("mult")
            self.play(*appear(mult), run_time=1.5)

            c.wait_until("real")
            ubrace = Brace(mult[4], DOWN, buff=0.12, color=BLUE)
            real_lbl = T("real part", 32, BLUE).next_to(ubrace, DOWN, buff=0.1)
            self.play(GrowFromCenter(ubrace), *appear(real_lbl), run_time=1.2)

            solve1 = tex(r"-\omega\beta", "=", r"\sqrt{3}\,c\,\omega")
            solve1[0].set_color(BLUE)
            solve1[2].set_color(GOLD)
            left_at(solve1, -2.0)
            solve2 = tex(r"\Rightarrow\;", r"\beta", "=", r"-\sqrt{3}\,c")
            solve2[3].set_color(PINK)
            solve2.next_to(solve1, RIGHT, buff=0.4)
            c.wait_until("solve")
            self.play(*appear(solve1), run_time=1.2)
            c.wait_until("beta is")
            self.play(*appear(solve2), run_time=1.2)

            result = tex("A", "=", r"c(1 - i\sqrt{3})")
            left_at(result, -3.1)
            c.wait_until("result")
            self.play(*appear(result), run_time=1.2)
            self.play(FlashAround(result, run_time=1.5, time_width=1.5), run_time=1.5)

        # ============================================================ clip 4: draw it
        with self.say("c6.ex.4") as c:
            plane4 = S3.argand_plane(PC4, U4, EXT4)
            sweep_clear(self,
                        *during(moves([result], lambda g: left_at(g, 2.5)), 0.5, 0.9),
                        *during(moves([question], lambda g: left_at(g.scale(1.1), -0.15)), 0.5, 0.85),
                        *during(appear(plane4, shift=None), 0.75, 1.0),  # early: the plane's axes
                        keep=[result, question, ticker], run_time=1.4)

            corner = PC4 + U4 * RIGHT
            tipA = PC4 + U4 * np.array([1, -np.sqrt(3), 0])
            leg_c = Line(PC4, corner, color=BLUE, stroke_width=7)
            leg_s = Line(corner, tipA, color=PINK, stroke_width=7)
            lbl_c = tex("c", size=40, color=BLUE).move_to(PC4 + 0.5 * U4 * RIGHT + 0.34 * UP)
            lbl_s = tex(r"\sqrt{3}\,c", size=40, color=PINK).next_to(leg_s, RIGHT, buff=0.15)
            c.wait_until("legs")
            self.play(Create(leg_c), *appear(lbl_c), run_time=1.0)
            c.wait_until("root three")
            self.play(Create(leg_s), *appear(lbl_s), run_time=1.2)

            hyp = Line(PC4, tipA, color=GOLD, stroke_width=7).set_z_index(1)
            nrm = np.array([-np.sqrt(3) / 2, -0.5, 0])
            lbl_2c = tex("2c", size=40, color=GOLD).move_to((PC4 + tipA) / 2 + 0.42 * nrm)
            pyth = tex("|A|", "=", r"\sqrt{c^2 + 3c^2}", "=", "2c")
            pyth[0].set_color(GOLD)
            pyth[4].set_color(GOLD)
            left_at(pyth, 1.2)
            c.wait_until("mod")
            self.play(Create(hyp), *appear(lbl_2c), run_time=1.3)
            c.wait_until("length")
            self.play(*appear(pyth), run_time=1.0)
            c.wait_until("one plus three")
            self.play(FlashAround(pyth[2], run_time=1.5, time_width=1.5), run_time=1.5)

            arc = Arc(radius=0.55, start_angle=0, angle=-PI / 3, arc_center=PC4,
                      color=YELLOW, stroke_width=4)
            spot = PC4 + 1.0 * ang(-PI / 6)
            lbl60 = tex(r"-60^\circ", size=34, color=YELLOW).move_to(spot)
            lblpi = tex(r"-\pi/3", size=34, color=YELLOW).move_to(spot)
            c.wait_until("angle")
            self.play(Create(arc), *appear(lbl60, shift=None), run_time=1.2)
            result_ext = tex("A", "=", r"c(1 - i\sqrt{3})", "=", r"2c\,e^{-i\pi/3}")
            left_at(result_ext, 2.5)
            c.wait_until("pi over three")
            self.play(*swap(lbl60, lblpi), *edit(result, result_ext), run_time=1.5)
            result = result_ext
            cpos = tex("c > 0", size=32, color=DIM).move_to(PC4 + np.array([-1.55, -1.1, 0]))
            c.wait_until("taking")
            self.play(*appear(cpos), run_time=0.8)

            answer = tex(r"\text{amplitude}\;\;", "|A| = 2c", r",\quad\text{phase}\;", r"-\pi/3",
                         size=40)
            answer[1].set_color(GOLD)
            answer[3].set_color(YELLOW)
            left_at(answer, -0.15)
            c.wait_until("answer")
            self.play(*swap(question, answer), run_time=1.2)

            xt = tex("x(t)", "=", r"2c\cos(", r"\omega t - \tfrac{1}{3}\pi", ")", size=46, color=YELLOW)
            left_at(xt, -1.6, LX + 0.15)
            box_x = SurroundingRectangle(xt, color=YELLOW, buff=0.18, stroke_width=3)
            box_a = SurroundingRectangle(result, color=YELLOW, buff=0.15, stroke_width=3)
            c.wait_until("displacement")
            self.play(*appear(xt), GrowFromCenter(box_x), GrowFromCenter(box_a), run_time=1.2)
            c.wait_until("arrow's angle")
            self.play(FlashAround(xt[3], run_time=1.5, time_width=1.5), run_time=1.5)

        # ============================================================ clip 5: let it run
        with self.say("c6.ex.5", gap=1.6) as c:
            plane5 = S3.argand_plane(PC5, U5, EXT5)
            circle = Circle(radius=2 * U5, color=DIM, stroke_width=2).move_to(PC5)
            arrow0 = gold_arrow(PHI0)
            self.play(*during([FadeOut(m) for m in (leg_c, leg_s, lbl_c, lbl_s, lbl_2c, arc, lblpi, cpos)],
                              0, 0.4),
                      ReplacementTransform(plane4, plane5),
                      ReplacementTransform(hyp, arrow0),
                      *during([FadeIn(circle)], 0.5, 1.0), run_time=1.2)
            self.remove(arrow0)
            arrow, ar_op = self.dyn(lambda op: gold_arrow(ph(), op), 1.0)
            self.add(arrow)                      # clock not started yet: held at t = 0 (phase -pi/3)

            # {half}: the t = 0 picture, held: the shadow starts at c
            c.wait_until("half")
            shd, shd_op = self.dyn(lambda op: x_shadow(ph(), op))
            self.add(shd)
            hbrace = span_brace(PC5, PC5 + U5 * RIGHT, DOWN, color=BLUE, buff=0.15)
            h_lbl = T("half the\namplitude", 30, BLUE, line_spacing=0.8)   # left of the Im axis, clear of the arrow
            h_lbl.move_to([0, hbrace.get_bottom()[1] - 0.05, 0]).align_to(PC5 + LEFT * 0.2, RIGHT)
            set_backstroke(h_lbl, width=6)
            self.play(shd_op.animate.set_value(1.0), GrowFromCenter(hbrace), *appear(h_lbl),  # early: said within 1 s
                      run_time=1.0)

            gx = PC5[0] + V_LEN * U5 * np.cos(PHI0 + PI / 2)
            g_tick = Line([gx, PC5[1] - 0.18, 0], [gx, PC5[1] + 0.18, 0], color=GREEN, stroke_width=5)
            g_lbl = tex(r"\sqrt{3}\,c\,\omega", size=30, color=GREEN)
            g_lbl.move_to([gx, PC5[1] - 0.45, 0]).align_to(np.array([6.55, 0, 0]), RIGHT)
            varrow, va_op = self.dyn(lambda op: vel_arrow(ph(), op))
            vshd, vs_op = self.dyn(lambda op: v_shadow(ph(), op))
            vlbl, vl_op = self.dyn(lambda op: v_label(ph(), op))
            self.add(varrow, vshd, vlbl)
            c.wait_until("outward")
            self.play(va_op.animate.set_value(1.0), vs_op.animate.set_value(1.0),
                      vl_op.animate.set_value(1.0), FadeIn(g_tick), *appear(g_lbl, shift=None),
                      run_time=1.2)


            # {same}: the pendulum of the whole chapter
            # the t = 0 picture is held through the sentence; released here, and its markers
            # (brace, sqrt3 c omega tick) leave the arrows' path as the clock starts
            c.wait_until("same")
            clock.start()
            self.play(*during(disappear(pyth, answer, hbrace, h_lbl, g_tick, g_lbl), 0, 0.4),
                      *during([result.animate.shift(DOWN * 4.25), box_a.animate.shift(DOWN * 4.25),
                               xt.animate.shift(DOWN * 1.35), box_x.animate.shift(DOWN * 1.35)], 0.35, 1.0),
                      run_time=1.4)
            pend, pend_op = self.dyn(lambda op: S3.pendulum(S3.PEND_AMP * np.cos(ph()), PEND_PIVOT,
                                                            S3.FULL_L, labels=False).set_opacity(op))
            self.add(pend)
            self.play(pend_op.animate.set_value(1.0), run_time=1.0)

            # {compare}: sines and cosines vs the complex amplitude
            hdr1 = T("sines and cosines", 36, DIM)
            left_at(hdr1, 3.2)
            ab = tex(r"a = c,\qquad b = \sqrt{3}\,c", size=40)
            left_at(ab, 2.3, LX + 0.3)
            ident = tex(r"c\cos\omega t + \sqrt{3}\,c\sin\omega t", r"\;\xrightarrow{\text{trig identity}}\;",
                        r"2c\cos(\omega t - \pi/3)", size=40)
            left_at(ident, 1.1, LX + 0.3)
            hdr2 = T("complex amplitude", 36, YELLOW)
            left_at(hdr2, -0.75)
            c.wait_until("compare")
            dyns = [(arrow, ar_op), (shd, shd_op), (varrow, va_op), (vshd, vs_op), (vlbl, vl_op), (pend, pend_op)]
            self.play(*during([tr.animate.set_value(0.0) for _, tr in dyns if tr is not None]
                              + [FadeOut(m) for m in (plane5, circle)], 0, 0.5),
                      run_time=1.2)
            for m, _ in dyns:
                self.remove(m)
            self.play(*appear(hdr1), run_time=0.8)
            c.wait_until("both coefficients")
            self.play(*appear(ab), run_time=1.0)
            c.wait_until("trig identity")
            self.play(*appear(ident), run_time=1.2)

            c.wait_until("two")
            self.play(*appear(hdr2), *set_alpha([hdr1, ab, ident], 0.4), run_time=1.0)
            self.play(FlashAround(box_a, run_time=1.6, time_width=1.5),
                      FlashAround(box_x, run_time=1.6, time_width=1.5), run_time=1.6)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
