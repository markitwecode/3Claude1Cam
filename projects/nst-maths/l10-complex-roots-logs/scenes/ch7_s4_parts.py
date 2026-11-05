"""Chapter 7, scene 4: resistor and capacitor in amplitudes: V_R0 = R I0, V_C0 = I0/(iωC). Clips c7.parts.1 – c7.parts.4.

Two columns under the shrunken circuit (resistor BLUE left, capacitor PINK right), the three rules
small at the top right. Small planes under the columns; ch6 s4's pair (GOLD position, PURPLE
velocity, copied look) recoloured into this chapter's colours.
Shared helpers (for the recap): deriv_rule(size) "d/dt -> x iω", quarter_pair(center, unit, phase)
the PINK V_C0 arrow with the GOLD current a quarter turn ahead and a YELLOW right-angle mark.
Ends on ch7_s5_impedance.opening_shot() (handover).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch7_s1_hook")
S5 = load_scene("ch7_s5_impedance")
argand_plane = load_scene("ch2_s2_theorem").argand_plane
circuit = S1.circuit
tx, amp_plane, amp_arrows, opening_shot = S5.tx, S5.amp_plane, S5.amp_arrows, S5.opening_shot
res_r_tex, res_c_tex = S5.res_r_tex, S5.res_c_tex

XL, XR = -3.55, 3.55            # column centres
Y1, Y2 = 1.5, 0.35             # equation rows
EQ = 44                         # derivation size
RES = 48                        # result size
PY = -1.65                      # small planes' centre height
PEXT = 1.3
R_O, R_U = np.array([-3.55, PY, 0]), 0.3          # resistor plane
C_O, C_U = np.array([4.0, PY, 0]), 0.26            # capacitor plane
P_O, P_U = np.array([0.2, PY, 0]), 0.39          # ch6's pair, small copy
I_LEN_C = 1.5 * PI              # current arrow length on the capacitor plane (matches ch6's pair)
TH = PI / 6                     # direction of V_C0 / ch6's position arrow


def _dir(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


def _arrow(a, b, color, width=5, tip=0.2):
    return Arrow(a, b, buff=0, stroke_width=width, color=color, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3)


def elbow(center, a, s=0.2, color=YELLOW, width=3):
    c = np.array(center)
    u, v = _dir(a), _dir(a + PI / 2)
    return VMobject().set_points_as_corners([c + s * u, c + s * (u + v), c + s * v]).set_stroke(color, width)


# ---------------------------------------------------------------- shared helpers (recap)
def deriv_rule(size=48):
    """'d/dt  ->  x iω' (i PINK)."""
    m = MathTex(r"\frac{d}{dt}", r"\;\longrightarrow\;", r"\times", "i", r"\omega", font_size=size)
    m[3].set_color(PINK)
    return m


def quarter_pair(center=C_O, unit=C_U, phase=TH, i_len=I_LEN_C):
    """V_C0 PINK at `phase`, the current GOLD a quarter turn ahead, YELLOW right-angle mark."""
    c = np.array(center)
    vc = _arrow(c, c + 3 * unit * _dir(phase), PINK)
    i0 = _arrow(c, c + i_len * unit * _dir(phase + PI / 2), GOLD).set_z_index(2)
    g = VGroup(vc, i0, elbow(c, phase))
    g.vc, g.i0, g.mark = g[0], g[1], g[2]
    return g


def rules():
    r1 = MathTex(r"\bullet\ \mathrm{Re}\text{ and }\tfrac{d}{dt}\text{ commute}", font_size=28)
    r2 = MathTex(r"\bullet\ e^{i\omega t}\text{ on two sides of eq}\ \to\ \text{cancel}", font_size=28)
    r3 = MathTex(r"\bullet\ (e^{i\omega t})' = ", "i", r"\omega\, e^{i\omega t}", font_size=28)
    r3[1].set_color(PINK)
    g = VGroup(r1, r2, r3).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    g.to_corner(UR, buff=0.42)
    return g


def small_circuit(center=np.array([-0.2, 2.6, 0]), scale=0.44):
    """s1's circuit, shrunk; labels re-set at a readable size, the source's ∼ drawn as a wave."""
    circ = circuit(center=center, scale=scale)
    for lbl, s, col in ((circ.V, "V", FG), (circ.R, "R", BLUE), (circ.C, "C", PINK), (circ.I, "I", GOLD)):
        lbl.become(MathTex(s, font_size=30, color=col).move_to(lbl))
    ring, sim = circ.source
    r = ring.width / 2
    wave = FunctionGraph(lambda x: 0.28 * r * np.sin(PI * x / (0.55 * r)), x_range=[-0.55 * r, 0.55 * r],
                         color=FG, stroke_width=2.5).move_to(ring)
    sim.become(wave)
    return circ


def handover_shot():
    return opening_shot()


RE, EX = r"\mathrm{Re}(", r"e^{i\omega t})"


class Parts(NarratedScene):
    def dyn(self, build, op0=0.0):
        tr = ValueTracker(op0)
        mob = always_redraw(lambda: build(tr.get_value()))
        return mob, tr

    def construct(self):
        circ = small_circuit()
        rl = rules()
        self.circ, self.rl = circ, rl
        self.resistor()
        self.capacitor()
        self.solve()
        self.recap()

    def rule_flash(self, k, rt=1.2):
        self.play(FlashAround(self.rl[k], color=YELLOW, time_width=1.5),
                  self.rl[k].animate.set_color(YELLOW), run_time=rt)
        self.play(self.rl[k].animate.set_color(FG), run_time=0.4)
        if k == 2:
            self.rl[2][1].set_color(PINK)

    # ============================================================ clip 1: the resistor
    def resistor(self):
        circ, rl = self.circ, self.rl
        with self.say("c7.parts.1") as c:
            self.play(*appear(circ, shift=None), *appear(*rl, shift=None, lag=0.2),  # early: rules shown whole, used later
                      run_time=1.2)
            self.play(FlashAround(circ.resistor, color=BLUE, time_width=1.5),
                      run_time=min(1.2, c.until("law")))

            c.wait_until("law")
            law = tx(("V_R", BLUE), "=", ("R", BLUE), ("I", GOLD), size=EQ).move_to([XL, Y1, 0])
            self.play(*appear(law), run_time=1.0)

            c.wait_until("sub")
            sub = tx(RE, ("V_{R0}", BLUE), EX, "=", ("R", BLUE), r"\,\mathrm{Re}(", ("I_0", GOLD), EX,
                     size=EQ).move_to([XL, Y2, 0])
            self.play(*appear(sub), run_time=1.2)

            c.wait_until("R is a real")
            inside = tx(RE, ("V_{R0}", BLUE), EX, "=", RE, ("R", BLUE), ("I_0", GOLD), EX,
                        size=EQ).move_to([XL, Y2, 0])
            tag = T("R is real", 30, BLUE).move_to([XL, Y2 - 0.75, 0])
            self.play(*edit(sub, inside), *during(appear(tag), 0.4, 1.0), run_time=1.6)

            c.wait_until("drop")
            self.rule_flash(1, rt=1.0)
            res = res_r_tex(RES).move_to([XL, Y2, 0])
            self.play(*edit(inside, res), *during(disappear(tag), 0, 0.4), run_time=1.6)

            c.wait_until("result")
            self.play(FlashAround(res, color=YELLOW, time_width=1.5), run_time=1.4)
            plane = amp_plane(R_O, R_U, PEXT)
            rp = ValueTracker(0.5)
            arr = always_redraw(lambda: self.r_arrows(rp.get_value()))
            c.wait_until("amplitude", nth=1)
            self.play(*appear(plane, shift=None), FadeIn(arr), run_time=1.2)

            c.wait_until("along")
            sh, sh_op = self.dyn(lambda op: self.r_shadows(rp.get_value(), op))
            self.add(sh)
            self.play(sh_op.animate.set_value(1.0), run_time=0.8)
            self.play(rp.animate.set_value(0.5 + PI), rate_func=linear, run_time=c.until(floor=1.0))
            arr.clear_updaters()
            sh.clear_updaters()
            self.remove(rp, sh_op)   # trackers off the scene (check's flash audit trips on them)
        self.law_r, self.res_r = law, res
        self.r_plane, self.r_arr, self.r_sh = plane, arr, sh

    @staticmethod
    def r_arrows(ph):
        a = amp_arrows(ph, R_O, R_U, i_len=2.0, width=4, tip=0.2)
        a.i0.set_stroke(width=8).set_z_index(5)   # GOLD drawn on top of BLUE, thicker so it reads along it
        return VGroup(a.vr, a.i0)

    @staticmethod
    def r_shadows(ph, op):
        g = VGroup()
        for ln, col, r in ((4.0, BLUE, 0.085), (2.0, GOLD, 0.065)):
            tip = R_O + ln * R_U * _dir(ph)
            foot = np.array([tip[0], R_O[1], 0])
            if abs(tip[1] - foot[1]) > 0.08:
                g.add(DashedLine(tip, foot, color=col, stroke_width=2, dash_length=0.06))
            g.add(Dot(foot, radius=r, color=col).set_z_index(4))
        return g.set_opacity(op)

    # ============================================================ clip 2: the capacitor
    def capacitor(self):
        circ = self.circ
        with self.say("c7.parts.2") as c:
            self.play(FlashAround(circ.capacitor, color=PINK, time_width=1.5),
                      run_time=min(1.2, c.until("rate")))

            c.wait_until("rate")
            a = tx(("I", GOLD), "=", r"\frac{d", ("Q", PINK), "}{dt}", size=EQ).move_to([XR, Y1, 0])
            self.play(*appear(a), run_time=1.0)
            c.wait_until("and the charge")
            b = tx(("I", GOLD), "=", r"\frac{d", ("Q", PINK), "}{dt}", "=", r"\frac{d(", ("C", PINK),
                   ("V_C", PINK), ")}{dt}", size=EQ).move_to([XR, Y1, 0])
            self.play(*edit(a, b), run_time=1.5)

            c.wait_until("const")
            law = tx(("I", GOLD), "=", r"\frac{d", ("Q", PINK), "}{dt}", "=", ("C", PINK), r"\frac{d",
                     ("V_C", PINK), "}{dt}", size=EQ).move_to([XR, Y1, 0])
            tag = T("C is constant", 30, PINK).move_to([XR, Y1 - 0.95, 0])
            self.play(*edit(b, law), *during(appear(tag), 0.4, 1.0), run_time=1.7)

            c.wait_until("swap")
            s1 = tx(RE, ("I_0", GOLD), EX, "=", ("C", PINK), r"\frac{d}{dt}\mathrm{Re}(", ("V_{C0}", PINK), EX,
                    size=EQ).move_to([XR, Y2, 0])
            self.play(*disappear(tag), run_time=0.6)
            self.play(*appear(s1), run_time=1.0)
            c.wait_until("let the derivative")
            s2 = tx(RE, ("I_0", GOLD), EX, "=", RE, ("C", PINK), ("V_{C0}", PINK), r"\frac{d}{dt}" + EX,
                    size=EQ).move_to([XR, Y2, 0])
            self.play(*edit(s1, s2), FlashAround(self.rl[0], color=YELLOW, time_width=1.5), run_time=1.6)

            c.wait_until("iw")
            s3 = tx(RE, ("I_0", GOLD), EX, "=", RE, ("i", PINK), r"\omega", ("C", PINK), ("V_{C0}", PINK), EX,
                    size=EQ).move_to([XR, Y2, 0])
            self.play(FlashAround(self.rl[2], color=YELLOW, time_width=1.5), run_time=0.9)
            self.play(*edit(s2, s3), run_time=1.5)

            c.wait_until("drop")
            self.play(FlashAround(self.rl[1], color=YELLOW, time_width=1.5), run_time=0.9)
            r = tx(("I_0", GOLD), "=", ("i", PINK), r"\omega", ("C", PINK), ("V_{C0}", PINK),
                   size=RES).move_to([XR, Y2, 0])
            self.play(*edit(s3, r), run_time=1.5)
            c.wait_until("current amplitude")
            self.play(FlashAround(r, color=YELLOW, time_width=1.5), run_time=min(1.4, c.until(floor=0.6)))
        self.law_c, self.i_eq = law, r

    # ============================================================ clip 3: solve, quarter turn, pendulum
    def solve(self):
        with self.say("c7.parts.3", gap=1.0) as c:
            res = res_c_tex(RES).move_to([XR, Y2, 0])
            self.play(*edit(self.i_eq, res), run_time=1.6)
            self.play(FlashAround(res, color=YELLOW, time_width=1.5), run_time=1.3)

            c.wait_until("quarter")
            plane = amp_plane(C_O, C_U, PEXT)
            pair = quarter_pair()
            self.play(*set_alpha([self.r_plane, self.r_arr, self.r_sh], 0.4),
                      *appear(plane, pair.vc, shift=None, lag=0.2), run_time=1.2)
            # x i: a copy of the PINK V_C0 turns a quarter turn anticlockwise, growing and turning GOLD,
            # and lands as the current I0 (the original PINK arrow stays put).
            k = ValueTracker(0.0)

            def turning():
                t = k.get_value()
                ln = interpolate(3.0, I_LEN_C, t)
                col = interpolate_color(ManimColor(PINK), ManimColor(GOLD), min(1.0, 1.4 * t))
                return _arrow(C_O, C_O + ln * C_U * _dir(TH + t * PI / 2), col).set_z_index(2)
            turn = always_redraw(turning)
            sweep = Arc(radius=0.62, start_angle=TH + 0.12, angle=PI / 2 - 0.24, arc_center=C_O,
                        color=YELLOW, stroke_width=4).add_tip(tip_length=0.16)
            xi = MathTex(r"\times", "i", font_size=32).move_to(C_O + 1.0 * _dir(160 * DEGREES))
            xi[1].set_color(PINK)
            set_backstroke(xi, width=5)
            self.add(turn)
            self.play(*during([k.animate.set_value(1.0)], 0.1, 1.0),
                      *during([Create(sweep)], 0.1, 1.0),
                      *during(appear(xi, shift=None), 0.0, 0.35), run_time=2.0)
            turn.clear_updaters()
            self.remove(turn, k)
            self.add(pair.i0)

            c.wait_until("arrow runs")
            self.play(*disappear(sweep), *during(appear(pair.mark, shift=None), 0.3, 1.0), run_time=0.9)
            self.play(FlashAround(pair.i0, color=GOLD, time_width=1.5), run_time=1.3)

            c.wait_until("pendulum")
            p_plane = argand_plane(center=P_O, unit=P_U, extent=PEXT)
            pos = _arrow(P_O, P_O + 2.0 * P_U * _dir(TH), GOLD)
            vel = _arrow(P_O, P_O + PI * P_U * _dir(TH + PI / 2), PURPLE).set_z_index(2)
            p_el = elbow(P_O, TH, color=FG, width=2.5)
            self.play(*appear(p_plane, pos, vel, p_el, shift=None, lag=0.15), run_time=1.4)

            l1 = VGroup(T("position", 28, FG), MathTex(r"\to", font_size=30),
                        T("charge", 28, PINK), MathTex("Q", font_size=32, color=PINK)).arrange(RIGHT, buff=0.14)
            l2 = VGroup(T("velocity", 28, FG), MathTex(r"\to", font_size=30), T("current", 28, GOLD),
                        tx(("I", GOLD), "=", "d", ("Q", PINK), "/dt", size=30)).arrange(RIGHT, buff=0.14)
            labels = VGroup(l1, l2).arrange(RIGHT, buff=0.6).move_to([1.95, -3.25, 0])
            c.wait_until("position")
            self.play(*appear(l1), pos.animate.set_color(PINK), run_time=1.2)
            c.wait_until("velocity")
            self.play(*appear(l2), vel.animate.set_color(GOLD), run_time=1.2)
        self.c_res = res

    # ============================================================ clip 4: no calculus left
    def recap(self):
        res_r, res_c, law = self.res_r, self.c_res, self.law_c
        shot = opening_shot()
        frac = law[7:]
        with self.say("c7.parts.4", gap=1.0) as c:
            # {nocalc}: look at the capacitor's derivative
            self.play(*flash([VGroup(*frac)], color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("deriv")
            # the board clears; the results go to their s5 places (top-left)
            sweep_clear(self, *during([Transform(res_r, shot[0])], 0.5, 0.8),
                        *during([res_c.animate.move_to([shot[1].get_x(), Y2, 0]).scale(50 / RES)], 0.6, 1.0),
                        keep=[res_r, res_c, law], run_time=1.6)
            law.generate_target()
            law.target.scale(48 / EQ).move_to([-1.4, -0.9, 0])
            self.play(*during([Transform(res_c, shot[1])], 0, 0.7),
                      *during([MoveToTarget(law)], 0.2, 1.0), run_time=1.3)

            # the derivative becomes a multiplication
            rule = MathTex(r"\times", "i", r"\omega", font_size=56, color=YELLOW)
            rule[1].set_color(PINK)
            x0 = law.get_right()[0]
            arrow = Arrow([x0 + 0.3, -0.9, 0], [x0 + 1.6, -0.9, 0], buff=0, color=YELLOW,
                          stroke_width=5, tip_length=0.24)
            rule.next_to(arrow, RIGHT, buff=0.3)
            self.play(GrowArrow(arrow), *during(appear(rule, shift=None), 0.5, 1.0), run_time=1.5)

            c.wait_until("algebra")
            self.play(*flash([shot[0], shot[1]], color=YELLOW, time_width=1.5), run_time=1.4)
            cap = T("no calculus left", 40, YELLOW).move_to([0, -2.5, 0])
            self.play(*appear(cap), run_time=1.0)  # early: caption sums up the sentence it opens
            self.wait(max(0.0, c.until(floor=1.0) - 1.0))
            self.play(*disappear(law, arrow, rule, cap), run_time=min(1.0, c.until(floor=0.6)))
            self.remove(res_r, res_c)
            self.add(shot)
        self.wait(0.6)
