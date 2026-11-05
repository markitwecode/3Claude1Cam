"""Chapter 7, scene 3: four amplitudes and three rules. Clips c7.amp.1 – c7.amp.5.

Imports circuit() from ch7 s1 and amp_plane / amp_arrows from ch7 s5. Shadow dots copied
from ch6 s3's style (dashed DIM drop line + dot in the arrow's colour).

Module-level helpers a recap can reuse:
  turning_arrows(ph, ops=None, center, unit)   the four arrows at phase ph() (always_redraw)
  arrow_shadows(ph, ops=None, center, unit)    their four shadow dots + drop lines (always_redraw)
  law_lines(), form_lines(), rule_lines()      the laws, the four Re(...) forms, the three rules
Ends on an empty frame.
"""
# style: 2
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

_s1 = load_scene("ch7_s1_hook")
_s2 = load_scene("ch7_s2_circuit")
four_laws = _s2.four_laws
_s5 = load_scene("ch7_s5_impedance")
circuit = _s1.circuit
amp_plane = _s5.amp_plane
amp_arrows = _s5.amp_arrows
tx = _s5.tx

# ---------------------------------------------------------------- layout
CIRC_C = np.array([-4.8, 2.42, 0.0])
CIRC_S = 0.5
LAW_X = -2.75
P = np.array([4.0, -0.45, 0.0])        # plane origin
U = 0.54                               # screen units per amplitude unit (|I0| = 1, |V0| = 5)
EXT = 2.85
OMEGA = TAU / 10                       # one turn every 10 s
PHI0 = 25 * DEGREES                    # current's starting angle


def _dir(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


# ---------------------------------------------------------------- text
def law_lines():
    """s2's four laws (its four_laws), stacked tighter, left-aligned. VGroup(ohm row, store, rate, loop)."""
    g = four_laws(32)
    g[0][0].scale(30 / 36)
    g[0].arrange(RIGHT, buff=0.2)
    g.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
    g.move_to([0, CIRC_C[1], 0]).align_to([LAW_X, 0, 0], LEFT)
    return g


def _form(lhs, lcol, amp, size=44):
    return tx((lhs, lcol), "=", r"\mathrm{Re}(", (amp, lcol), r"e^{i\omega t}", ")", size=size)


def form_lines():
    """V = Re(V0 e^{iωt}) / I = ... / V_R = ... / V_C = ..., '=' aligned. Amplitude is [3]."""
    rows = [_form("V", FG, "V_0", 40), _form("I", GOLD, "I_0", 40),
            _form("V_R", BLUE, "V_{R0}", 40), _form("V_C", PINK, "V_{C0}", 40)]
    g = VGroup(*rows).arrange(DOWN, buff=0.16)
    for r in rows:
        r.shift((rows[0][1].get_x() - r[1].get_x()) * RIGHT)
    g.move_to([0, -0.12, 0]).align_to([-6.45, 0, 0], LEFT)
    return g


def rule_lines():
    """The lecturer's three bullets (scan p. 12), with DIM (83) beside the first and third."""
    r1 = VGroup(T("•", 34), tx(r"\mathrm{Re}", size=40), T("and", 34), tx(r"d/dt", size=40),
                T("commute", 34)).arrange(RIGHT, buff=0.16)
    r2 = VGroup(T("•", 34), tx(r"e^{i\omega t}", size=40), T("on two sides of eq", 34),
                tx(r"\rightarrow", size=40), T("cancel", 34)).arrange(RIGHT, buff=0.16)
    r3 = VGroup(T("•", 34), tx(r"(e^{i\omega t})'", "=", ("i", PINK), r"\omega", r"\,e^{i\omega t}", size=40)
                ).arrange(RIGHT, buff=0.16)
    for r in (r1, r2, r3):
        r[1:].align_to(r[0], DOWN).shift(0.02 * DOWN)
    g = VGroup(r1, r2, r3).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    g.move_to([0, -2.45, 0]).align_to([-6.45, 0, 0], LEFT)
    n1 = T("(83)", 30, DIM).next_to(r1, RIGHT, buff=0.4)
    n3 = T("(83)", 30, DIM).next_to(r3, RIGHT, buff=0.4)
    n3.align_to(n1, LEFT)
    g.n1, g.n3 = n1, n3
    return g


# ---------------------------------------------------------------- the turning picture
I_LEN = 2.0                            # I0 drawn 2 units long (as s4's resistor plane), so it clears V_R0's foot


def turning_arrows(ph, ops=None, center=P, unit=U, i_len=I_LEN):
    """always_redraw of amp_arrows at phase ph(); ops: dict vr/vc/v0/i0 -> ValueTracker opacity."""
    def build():
        g = amp_arrows(ph(), center=center, unit=unit, i_len=i_len)
        if ops:
            for k in ("vr", "vc", "v0", "i0"):
                getattr(g, k).set_opacity(ops[k].get_value())
        return g
    return always_redraw(build)


def _shadow(tip, color, center, op=1.0, ring=False):
    foot = np.array([tip[0], center[1], 0.0])
    if abs(tip[1] - foot[1]) > 0.08:
        line = DashedLine(tip, foot, color=DIM, stroke_width=2.5, dash_length=0.08)
    else:
        line = Line(foot + UP * 0.001, foot, color=DIM, stroke_width=2.5)
    line.set_opacity(0.7 * op)
    if ring:
        dot = Circle(radius=0.15, stroke_width=3).set_stroke(color, 3, opacity=op).set_fill(opacity=0).move_to(foot)
    else:
        dot = Dot(foot, radius=0.09, color=color).set_opacity(op)
    dot.set_z_index(5)
    return VGroup(line, dot)


def arrow_shadows(ph, ops=None, center=P, unit=U, i_len=I_LEN):
    """always_redraw of the four shadow dots on the real axis, each in its arrow's colour."""
    c = np.array(center, dtype=float)
    spec = [("v0", 5, -_s5.LAG, FG), ("vr", 4, 0.0, BLUE), ("vc", 3, -PI / 2, PINK), ("i0", i_len, 0.0, GOLD)]

    def build():
        g = VGroup()
        for k, r, off, col in spec:
            op = ops[k].get_value() if ops else 1.0
            g.add(_shadow(c + r * unit * _dir(ph() + off), col, c, op))
        return g
    return always_redraw(build)


# ---------------------------------------------------------------- the "why" pair
WHY_L = 2.4
WHY_A = 55 * DEGREES


def why_pair(a, center=P):
    c = np.array(center, dtype=float)
    d, n = _dir(a), _dir(a + PI / 2)
    tip = c + WHY_L * d
    solid = Arrow(c, tip, buff=0, stroke_width=6, color=FG, tip_length=0.26,
                  max_tip_length_to_length_ratio=0.3).set_z_index(2)
    w, tw, tl = 0.11, 0.24, 0.42
    pts = [c + n * w, tip - d * tl + n * w, tip - d * tl + n * tw, tip + d * 0.08,
           tip - d * tl - n * tw, tip - d * tl - n * w, c - n * w, c + n * w]
    outline = VMobject().set_points_as_corners(pts).set_stroke(YELLOW, 3)
    dashed = DashedVMobject(outline, num_dashes=34, dashed_ratio=0.55).set_z_index(3)
    return VGroup(solid, dashed)


def why_shadows(a, center=P):
    c = np.array(center, dtype=float)
    tip = c + WHY_L * _dir(a)
    s1 = _shadow(tip, FG, c)
    s2 = _shadow(tip, YELLOW, c, ring=True)
    return VGroup(s1, s2[1])


def _foot(a, center=P):
    return np.array([center[0] + WHY_L * np.cos(a), center[1], 0.0])


# ---------------------------------------------------------------- the scene
class Amplitudes(NarratedScene):
    def construct(self):
        ph = ValueTracker(PHI0)
        self.turning = False

        def tick(m, dt):
            if self.turning:
                m.increment_value(OMEGA * dt)
        ph.add_updater(tick)
        self.add(ph)
        ops = {k: ValueTracker(1.0) for k in ("vr", "vc", "v0", "i0")}

        circ = circuit(CIRC_C, CIRC_S)
        for lbl in (circ.V, circ.R, circ.C, circ.I):
            lbl.scale(1.5)
        circ.V.shift(0.08 * LEFT)
        circ.C.shift(0.08 * RIGHT)
        circ.source[1].scale(1.2)
        laws = law_lines()
        omega = tx(r"\omega", size=34)
        omega.next_to(circ.source, RIGHT, buff=0.18)

        # ------------------------------------------------ clip 1
        with self.say("c7.amp.1") as c:
            self.play(FadeIn(circ), *appear(*laws, lag=0.15), run_time=1.2)  # early: recap of s2's laws
            self.play(*appear(omega), run_time=1.0)
            self.play(FlashAround(omega, run_time=1.5, time_width=1.5))
            c.wait_until("linear")
            self.play(FlashAround(laws, run_time=1.8, time_width=1.5))

            tag_x = laws.get_right()[0] + 0.45
            tags = {}
            for name, rows in (("sum", [3]), ("constant multiple", [0, 1]), ("derivative", [2])):
                for i in rows:
                    t = T(name, 28, YELLOW)
                    t.move_to([0, laws[i].get_y(), 0]).align_to([tag_x, 0, 0], LEFT)
                    tags.setdefault(name, []).append(t)
            for name, cue in (("sum", "sum"), ("constant multiple", "constant multiple"),
                              ("derivative", "derivative")):
                c.wait_until(cue)
                rows = tags[name]
                idx = {"sum": [3], "constant multiple": [0, 1], "derivative": [2]}[name]
                self.play(*appear(*rows, shift=0.15 * LEFT, lag=0.2),
                          *[FlashAround(laws[i], time_width=1.5) for i in idx], run_time=1.2)
            c.wait_until("arrows")
            plane = amp_plane(P, U, EXT)
            all_tags = [t for v in tags.values() for t in v]
            self.play(*during(disappear(*all_tags), 0, 0.45), *during([FadeIn(plane)], 0.4, 1), run_time=1.4)
            arrows = turning_arrows(ph.get_value, ops)
            shads = arrow_shadows(ph.get_value, ops)
            grow = amp_arrows(PHI0, center=P, unit=U, i_len=I_LEN)
            self.play(*[GrowArrow(a) for a in grow], run_time=1.4)
            self.remove(*grow)
            self.add(shads, arrows)
            self.play(FadeIn(shads), run_time=0.6)
            self.turning = True

        # ------------------------------------------------ clip 2
        forms = form_lines()
        with self.say("c7.amp.2") as c:
            self.play(*appear(*forms, lag=0.5), run_time=min(3.0, c.until("vzero")))
            c.wait_until("vzero")
            self.play(FlashAround(forms[0][3], run_time=1.5, time_width=1.5),
                      *[ops[k].animate.set_value(DIMMED) for k in ("vr", "vc", "i0")], run_time=1.5)
            c.wait_until("izero")
            self.play(FlashAround(forms[1][3], run_time=1.5, time_width=1.5),
                      ops["i0"].animate.set_value(1.0), ops["v0"].animate.set_value(DIMMED), run_time=1.5)
            c.wait_until("others")
            self.play(FlashAround(forms[2][3], run_time=1.5, time_width=1.5),
                      FlashAround(forms[3][3], run_time=1.5, time_width=1.5),
                      ops["i0"].animate.set_value(DIMMED),
                      ops["vr"].animate.set_value(1.0), ops["vc"].animate.set_value(1.0), run_time=1.5)
            c.wait_until()

        # ------------------------------------------------ clip 3
        rules = rule_lines()
        with self.say("c7.amp.3") as c:
            self.play(*[ops[k].animate.set_value(1.0) for k in ops], run_time=1.0)
            c.wait_until("commute")
            self.play(*appear(rules[0], rules.n1, lag=0.3), run_time=1.2)
            c.wait_until("cancel")
            self.play(*appear(rules[1]), run_time=1.2)  # early: the lecturer's bullet, shown whole on its cue
            c.wait_until("deriv")
            self.play(*appear(rules[2], rules.n3, lag=0.3), run_time=1.2)
            c.wait_until()

        # ------------------------------------------------ clip 4
        with self.say("c7.amp.4") as c:
            self.turning = False
            self.play(FadeOut(arrows), FadeOut(shads), FlashAround(rules[1], time_width=1.5),
                      run_time=min(1.5, c.until("suppose")))
            c.wait_until("suppose")
            wa = ValueTracker(WHY_A - 1.5 * PI)
            pair = always_redraw(lambda: why_pair(wa.get_value()))
            wsh = always_redraw(lambda: why_shadows(wa.get_value()))
            self.play(FadeIn(pair), FadeIn(wsh), run_time=1.0)
            self.play(wa.animate.set_value(WHY_A), run_time=max(1.0, c.until("t0") - 0.1), rate_func=linear)
            c.wait_until("t0")
            f1 = _foot(WHY_A)
            lab1 = T("real parts equal", 30, FG)
            lab1.move_to([P[0], 3.5, 0])
            self.play(Flash(f1, color=YELLOW, line_length=0.2, flash_radius=0.3), run_time=1.0)
            self.play(*appear(lab1), run_time=1.0)
            c.wait_until("quarter")
            self.play(wa.animate.set_value(WHY_A + PI / 2), restyle(lab1, 0.4), run_time=1.8)
            f2 = _foot(WHY_A + PI / 2)
            lab2 = T("imaginary parts equal", 30, FG).next_to(lab1, DOWN, buff=0.2)
            self.play(Flash(f2, color=YELLOW, line_length=0.2, flash_radius=0.3),
                      *appear(lab2), run_time=1.2)
            c.wait_until("same")
            final = why_pair(WHY_A + PI / 2)
            fsh = why_shadows(WHY_A + PI / 2)
            self.remove(pair, wsh)
            self.add(final, fsh)
            merged = final[0].copy().set_color(YELLOW)
            self.play(FadeOut(final[1]), FadeOut(fsh[1]), Transform(final[0], merged), run_time=1.5)
            self.play(FlashAround(rules[1], run_time=1.5, time_width=1.5))
            c.wait_until()

        # ------------------------------------------------ clip 5
        goal = tx(r"\text{Find }", ("Z", YELLOW), r"\text{:}\quad", "V_0", "=", ("Z", YELLOW), ("I_0", GOLD), size=50)
        goal.move_to([3.8, 0.85, 0])
        box = SurroundingRectangle(goal, color=YELLOW, buff=0.25, stroke_width=3)
        small = tx("V", "=", ("R", BLUE), ("I", GOLD), size=44)
        small.move_to([goal[3:].get_x(), -0.75, 0])
        cap1 = T("Z: the complex impedance", 34, FG, t2c={"Z": YELLOW}).move_to([3.8, -2.05, 0])
        cap2 = T("(the notes: complex resistance)", 30, DIM).next_to(cap1, DOWN, buff=0.25)
        with self.say("c7.amp.5", gap=1.0) as c:
            keep = {id(f) for k in (circ, omega, laws, forms, rules, rules.n1, rules.n3, ph)
                    for f in k.get_family()}
            gone = [m for m in self.mobjects if id(m) not in keep]
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during([FadeIn(goal), FadeIn(box)], 0.5, 1), run_time=min(1.4, c.until("we want")))
            c.wait_until("we want")
            self.play(FlashAround(goal[3:], run_time=2.0, time_width=1.5))
            c.wait_until("ohm")
            self.play(*appear(small), run_time=1.0)
            maps = VGroup()
            for s, d in ((small[0], goal[3]), (small[2], goal[5]), (small[3], goal[6])):
                maps.add(Arrow(s.get_top(), d.get_bottom(), buff=0.15, color=DIM, stroke_width=3,
                               tip_length=0.18, max_tip_length_to_length_ratio=0.2))
            self.play(*[GrowArrow(m) for m in maps], run_time=1.5)
            self.play(*flash([goal[3], goal[5], goal[6]], run_time=1.5, time_width=1.5))
            c.wait_until("name")
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("notes call")
            self.play(*appear(cap2), run_time=1.0)
            c.wait_until()

        self.turning = False
        self.play(*[FadeOut(m) for m in self.mobjects if m is not ph], run_time=1.0)
        self.remove(ph)
        self.wait(0.15)
