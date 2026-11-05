"""Chapter 6, scene 4: differentiating means multiplying by i omega. Clips c6.deriv.1 – c6.deriv.4.

Opens on ch6_s3_phasor's handover_shot(); the arrow keeps turning (s3's Clock, resumed at -pi/3).
Velocity arrow: PURPLE, i omega A e^{i omega t}, length omega|A| = pi plane units, 90 deg ahead;
its shadow is a PURPLE dot v(t). Acceleration arrow: FG, straight back (drawn 3.3 long: the true
omega^2|A| = 4.9 doesn't fit the plane).
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
P0, U, R, OMEGA, PHI0, A_MOD = S3.P0, S3.U, S3.R, S3.OMEGA, S3.PHI0, S3.A_MOD
ang = S3.ang
V_LEN = PI                      # omega |A| on screen (omega = pi/2, |A| = 2)
ACC_LEN = 3.3                   # acceleration arrow, not to scale
X = 3.1                         # right column centre
TAG_POS = np.array([4.2, 2.7, 0.0])


class PClock(S3.Clock):
    """s3's clock with hold/release: a held clock shows a fixed phase; release resumes from it."""

    def __init__(self):
        super().__init__()
        self.held = None

    def phase_at(self, s):
        if self.held is not None:
            return self.held
        return super().phase_at(s)

    def hold(self, target=None):
        """Freeze; with a target, at the turn of `target` nearest the current phase (the aimed warp
        lands on it, at most a frame ago)."""
        p = self.phase()
        self.held = p if target is None else target + TAU * round((p - target) / TAU)

    def release(self):
        h, self.held = self.held, None
        self.warps = []
        self.t0 = self.s - (h - PHI0) / OMEGA


def components(phase, op):
    tip = P0 + R * ang(phase)
    foot = np.array([tip[0], P0[1], 0.0])
    re = Line(P0, foot + RIGHT * 0.001, color=BLUE, stroke_width=7)
    im = Line(foot, tip + UP * 0.001, color=PINK, stroke_width=7)
    return VGroup(re, im).set_stroke(opacity=op)


def elbow(phase, op):
    u, v, s = ang(phase), ang(phase + PI / 2), 0.28
    return VMobject().set_points_as_corners([P0 + s * u, P0 + s * (u + v), P0 + s * v]).set_stroke(
        FG, 2.5, opacity=op)


def v_foot(phase):
    tip = P0 + V_LEN * U * ang(phase + PI / 2)
    return tip, np.array([tip[0], P0[1], 0.0])


def vshadow(phase, op):
    tip, foot = v_foot(phase)
    if abs(tip[1] - foot[1]) > 0.08:
        line = DashedLine(tip, foot, color=PURPLE, stroke_width=2.5, dash_length=0.08)
    else:
        line = Line(foot + UP * 0.001, foot, color=PURPLE, stroke_width=2.5)
    dot = Dot(foot, radius=0.1, color=PURPLE)
    return VGroup(line, dot).set_opacity(op)


def vlabel(phase, op):
    _, foot = v_foot(phase)
    lbl = S3._tex("v(t)", 32, PURPLE).move_to(foot + DOWN * 0.42 + RIGHT * 0.4)
    set_backstroke(lbl, width=5)
    return lbl.set_opacity(op)


def pull(phase, op):
    th = S3.PEND_AMP * np.cos(phase)
    bob = S3.INSET_PIVOT + S3.INSET_L * np.array([np.sin(th), -np.cos(th), 0.0])
    ln = 0.8 * np.cos(phase)
    if abs(ln) < 0.06 or op < 0.01:
        return VMobject()
    d = LEFT if ln > 0 else RIGHT
    start = bob + d * 0.17
    return Arrow(start, start + d * abs(ln), buff=0, stroke_width=4, color=FG, tip_length=0.14,
                 max_tip_length_to_length_ratio=0.5).set_opacity(op)


class Derivative(NarratedScene):
    def dyn(self, build, op0=0.0):
        tr = ValueTracker(op0)
        mob = always_redraw(lambda: build(tr.get_value()))
        return mob, tr

    def construct(self):
        clock = self.clock = PClock()
        ticker = VectorizedPoint(P0)
        ticker.add_updater(lambda m, dt: setattr(clock, "s", self.renderer.time))   # scene time, not summed dt
        self.add(ticker)
        ph = clock.phase

        # ---------------------------------------------------- s3's last shot, made live
        plane = S3.argand_plane()
        circle = S3.plane_circle()
        trail = S3.trail_arc(PHI0, PHI0 + TAU)
        shd = always_redraw(lambda: S3.shadow(ph()))
        comp, comp_op = self.dyn(lambda op: components(ph(), op))
        arrow = always_redraw(lambda: S3.phasor_arrow(ph()).set_z_index(3))
        omk, omk_op = self.dyn(lambda op: S3.omega_marker(ph(), op), 1.0)
        inset = always_redraw(lambda: S3.inset_pendulum(ph()))
        self.add(plane, circle, trail, comp, shd, arrow, omk, inset)
        clock.start()

        # ============================================================ clip 1
        def hero(*parts):
            m = MathTex(*parts, font_size=42).move_to([0, 1.0, 0])
            return m.shift(RIGHT * (0.35 - m.get_left()[0]))

        with self.say("c6.deriv.1") as c:
            LA = hero("v(t)", "=", r"\dfrac{dx}{dt}", "=", r"\dfrac{d}{dt}", r"\,\mathrm{Re}", r"\Big[",
                      r"A\,e^{i\omega t}", r"\Big]")
            self.play(*appear(LA, shift=None), run_time=1.2)

            # {swap}: Re and d/dt trade places
            c.wait_until("swap")
            LB = hero("v(t)", "=", r"\dfrac{dx}{dt}", "=", r"\mathrm{Re}", r"\Big[", r"\dfrac{d}{dt}",
                      r"\,A\,e^{i\omega t}", r"\Big]")
            self.play(*edit(LA, LB), run_time=min(1.8, c.until("because")))

            c.wait_until("because")
            aside = MathTex(r"\dfrac{d}{dt}\big(", "x", "+", "i", "y", r"\big)", "=",
                            r"\dfrac{d", "x", "}{dt}", "+", "i", r"\dfrac{d", "y", "}{dt}",
                            font_size=36)
            for k in (1, 8):
                aside[k].set_color(BLUE)
            for k in (4, 13):
                aside[k].set_color(PINK)
            aside.move_to([X, -0.45, 0])
            self.play(*appear(aside, shift=None), run_time=1.0)
            c.wait_until("real and imaginary")
            self.play(comp_op.animate.set_value(1.0),
                      *flash([aside[1], aside[4]], color=YELLOW, time_width=1.5), run_time=1.5)

            # {rule}
            c.wait_until("rule")
            LC = hero("v(t)", "=", r"\dfrac{dx}{dt}", "=", r"\mathrm{Re}", r"\Big[", "i", r"\omega",
                      r"\,A\,e^{i\omega t}", r"\Big]")
            eq83 = MathTex("(83)", font_size=30, color=DIM).next_to(LC, RIGHT, buff=0.35)
            self.play(*edit(LB, LC), run_time=1.6)
            self.play(*appear(eq83, shift=None), run_time=0.8)

            # {notes}
            c.wait_until("notes")
            lines = VGroup(
                MathTex(r"\text{to differentiate }e^{i\omega t}", font_size=32),
                MathTex(r"\text{we simply multiply by }i\omega", font_size=32),
                MathTex(r"\text{before taking the real part}", font_size=32),
            ).arrange(DOWN, buff=0.16)
            nbox = SurroundingRectangle(lines, color=YELLOW, buff=0.25, stroke_width=2.5)
            notes = VGroup(nbox, lines).move_to([X, -2.3, 0])
            self.play(*appear(notes, shift=None), comp_op.animate.set_value(0.0), run_time=1.2)  # early: the notes' sentence shown whole, then read
            c.wait_until("multiply by")
            self.play(*recolor(LC[6], PINK), *flash([LC[6], LC[7]], color=YELLOW, time_width=1.5),
                      run_time=1.5)

        # ============================================================ clip 2
        with self.say("c6.deriv.2") as c:
            clock.aim(c.remaining + 0.35, PI / 6)      # lands at pi/6 as clip 3 begins
            up = UP * 0.3
            self.play(*during(disappear(aside), 0, 0.45),
                      *during([LC.animate.shift(up), eq83.animate.shift(up)], 0.2, 0.8), run_time=1.2)
            C1 = MathTex(r"\dfrac{d}{dt}", r"\left(\cos\omega t + i\sin\omega t\right)",
                         font_size=42).move_to([X, 0.0, 0])
            self.play(*appear(C1, shift=None), run_time=1.0)

            c.wait_until("diff")
            C2 = MathTex("=", r"-\omega\sin\omega t", "+", r"i\omega", r"\cos\omega t",
                         font_size=42).move_to([X + 0.3, -1.05, 0])
            self.play(*during(disappear(notes), 0, 0.5), *during(appear(C2, shift=None), 0.3, 1.0),
                      run_time=1.4)

            c.wait_until("factor")
            C3 = MathTex("=", r"i\omega", r"\left(\cos\omega t + i\sin\omega t\right)", font_size=42)
            C3.shift([C2[0].get_x() - C3[0].get_x(), -2.0 - C3[0].get_y(), 0])
            self.play(*fly(C2[3], C3[1], arc=PI / 2), run_time=1.4)
            self.play(*appear(C3[0], C3[2], shift=None), run_time=0.8)
            settle(self, C3)
            self.play(*flash([C3[1]], color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("same")
            same = MathTex(r"\dfrac{d}{dt}\,e^{kt} = k\,e^{kt}", font_size=36, color=DIM)
            same.move_to([X, -3.0, 0])
            self.play(*appear(same, shift=None), run_time=1.0)

        # ============================================================ clip 3
        with self.say("c6.deriv.3") as c:
            clock.hold(PI / 6)
            phi = ph()
            self.play(omk_op.animate.set_value(0.0), run_time=0.8)

            # a copy turns a quarter turn ahead
            c.wait_until("Multiplying by eye")
            off, ln, col = ValueTracker(0.0), ValueTracker(A_MOD), ValueTracker(0.0)
            pop = ValueTracker(0.0)
            varrow = always_redraw(lambda: S3.phasor_arrow(
                ph() + off.get_value(), ln.get_value(),
                interpolate_color(ManimColor(GOLD), ManimColor(PURPLE), col.get_value()),
                pop.get_value()).set_z_index(2))
            self.add(varrow)
            self.play(*during([pop.animate.set_value(1.0)], 0, 0.25),
                      *during([off.animate.set_value(PI / 2)], 0.15, 1.0), run_time=1.6)
            el, el_op = self.dyn(lambda op: elbow(ph(), op))
            self.add(el)
            xi = MathTex(r"\times", "i", font_size=36).move_to(P0 + 0.85 * ang(phi + PI / 4))
            xi[1].set_color(PINK)
            set_backstroke(xi, width=5)
            self.play(el_op.animate.set_value(1.0), *appear(xi, shift=None), run_time=0.9)

            # {stretch}
            c.wait_until("stretch")
            xw = MathTex(r"\times\omega", font_size=36, color=YELLOW)
            xw.move_to(P0 + 2.0 * U * ang(phi + PI / 2) + 0.5 * ang(phi + PI))
            set_backstroke(xw, width=5)
            vtip = P0 + V_LEN * U * ang(phi + PI / 2)
            vlbl = MathTex(r"i\omega A\,e^{i\omega t}", font_size=36, color=PURPLE).move_to(vtip + UP * 0.45)
            set_backstroke(vlbl, width=5)
            self.play(ln.animate.set_value(V_LEN), col.animate.set_value(1.0),
                      *during(appear(xw, shift=None), 0.3, 0.7), *during(appear(vlbl), 0.6, 1.0),
                      run_time=1.8)
            self.play(*recolor(LC[7], PURPLE), *recolor(LC[8], PURPLE), run_time=1.0)

            # {lead}: both turn, the PURPLE shadow is v(t)
            c.wait_until("lead")
            self.play(*disappear(C1, C2, C3, same), run_time=1.0)
            c.wait_until("and its shadow")
            clock.release()
            clock.aim(c.until("ends", floor=0.5), 0.0)
            vsh, vsh_op = self.dyn(lambda op: vshadow(ph(), op))
            vtx, vtx_op = self.dyn(lambda op: vlabel(ph(), op))
            self.add(vsh, vtx)
            self.play(*disappear(xi, xw, vlbl), vsh_op.animate.set_value(1.0),
                      vtx_op.animate.set_value(1.0), run_time=1.2)

            # {ends}: freeze, GOLD along +Re
            c.wait_until("ends")
            clock.hold(0.0)
            c.wait_until("vertical")
            self.play(FlashAround(S3.phasor_arrow(ph() + PI / 2, V_LEN, PURPLE), color=PURPLE,
                                  time_width=1.5), run_time=min(1.5, c.until("shadow is zero")))
            c.wait_until("shadow is zero")
            _, foot = v_foot(ph())
            self.play(FlashAround(Dot(foot, radius=0.1), color=YELLOW, time_width=1.5),
                      run_time=min(1.2, c.until("still")))
            still = T("still", 36, YELLOW).move_to(TAG_POS)
            c.wait_until("For a moment")
            self.play(*appear(still), FlashAround(inset, color=YELLOW, time_width=1.5), run_time=1.2)

            # {bottom}: a quarter turn later
            c.wait_until("bottom")
            clock.release()
            clock.aim(c.until("passes the bottom", floor=0.8), PI / 2, lo=-PI / 2)
            self.play(*disappear(still), run_time=min(0.8, c.until("passes the bottom")))
            c.wait_until("passes the bottom")
            clock.hold(PI / 2)
            c.wait_until("furthest out")
            _, foot = v_foot(ph())
            self.play(FlashAround(Dot(foot, radius=0.1), color=YELLOW, time_width=1.5), run_time=1.2)
            fastest = T("fastest", 36, YELLOW).move_to(TAG_POS)
            c.wait_until("That.s where")
            self.play(*appear(fastest), run_time=min(1.0, c.until()))

        # ============================================================ clip 4
        with self.say("c6.deriv.4") as c:
            sq = MathTex(r"(", "i", r"\omega)^2", "=", r"-\omega^2", font_size=46)
            sq[1].set_color(PINK)
            sq.move_to([X, -0.7, 0])
            self.play(*appear(sq, shift=None), run_time=1.2)
            c.wait_until("minus omega squared")
            clock.release()
            clock.aim(c.until("back", floor=0.8), 0.0)
            self.play(*disappear(fastest), FlashAround(sq[4], color=YELLOW, time_width=1.5), run_time=1.3)

            # {back}: one more quarter turn on
            c.wait_until("back")
            clock.hold(0.0)
            off2, ln2, col2 = ValueTracker(PI / 2), ValueTracker(V_LEN), ValueTracker(0.0)
            aop = ValueTracker(0.0)
            aarrow = always_redraw(lambda: S3.phasor_arrow(
                ph() + off2.get_value(), ln2.get_value(),
                interpolate_color(ManimColor(PURPLE), ManimColor(FG), col2.get_value()),
                aop.get_value()).set_z_index(1))
            self.add(aarrow)
            acc = T("acceleration", 32, FG)
            atip = P0 + ACC_LEN * U * ang(ph() + PI)
            acc.next_to(atip, UP, buff=0.3).align_to(atip, LEFT)
            set_backstroke(acc, width=5)
            self.play(*during([aop.animate.set_value(1.0)], 0, 0.2),
                      *during([off2.animate.set_value(PI), ln2.animate.set_value(ACC_LEN),
                               col2.animate.set_value(1.0)], 0.1, 0.85),
                      *during(appear(acc), 0.6, 1.0), run_time=2.0)

            # {law}
            c.wait_until("law")
            law = MathTex(r"\ddot{x}", "=", r"-\omega^2", "x", font_size=50).move_to([X, -2.1, 0])
            law[0].set_color(FG)
            law[3].set_color(BLUE)
            pl, pl_op = self.dyn(lambda op: pull(ph(), op))
            self.add(pl)
            self.play(*appear(law, shift=None), pl_op.animate.set_value(1.0), run_time=1.2)

            c.wait_until("That's the equation")
            self.play(*disappear(acc), run_time=0.8)          # gone before the arrows turn again
            clock.release()
            self.play(FlashAround(law, color=YELLOW, time_width=1.5), run_time=1.5)

        clock.hold()
        for m in self.mobjects:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
