"""Chapter 8, scene 7: F19, a shifted oscillation. Clips c8.f19.1 – c8.f19.5.

Shared piece for the recap (ch8_s8_end):
  recap_panel()   the 24 − 7i GOLD arrow on its Argand plane with the 7-24-25 triangle (24 BLUE
                  along the real axis, 7 PINK down, 25 GOLD) and the BLUE shadow dot, as at {triangle}.
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

DELTA = float(np.arctan2(7, 24))          # 0.28379
T1 = (PI / 2 + DELTA) / 3                 # 0.61820
T2 = (3 * PI / 2 + DELTA) / 3             # 1.66539
T_MIN = (PI + DELTA) / 3                  # x = -18
T_FLAT = (TAU + DELTA) / 3                # x = 32 (arrow flat, pointing right)

# clip 3: the big triangle
P3 = np.array([-5.1, 0.8, 0.0])
R3 = 3.6
# clips 4-5: the turning arrow beside its wave
P4 = np.array([-4.5, -0.9, 0.0])
R4 = 1.8
G0 = np.array([-1.3, -0.9, 0.0])          # wave origin (t = 0 on the centre line x = 7)
K_T = 3.1                                 # screen units per unit of t
T_AX = 2.35

NL_Y = -0.9                               # clip 2 number line
NL_Y5 = 0.0                               # clip 5 number line


def nl_x(v):                              # ch6 s6's number line: -20..35 over 11 units
    return -1.5 + 0.2 * v


def ang(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


def tex(*parts, size=44, color=FG):
    return MathTex(*parts, font_size=size, color=color)


# ---------------------------------------------------------------- plane pieces (ch6 s3's look)
def plane(P, R, left=None, up=None, down=None):
    """Re/Im axes with a DIM grid every 5 (|24 - 7i| = 25 is R on screen); optional shorter
    left / up / down extents (screen units)."""
    P = np.array(P, dtype=float)
    u = R / 25
    e = 1.115 * R
    eL, eU, eD = left or e, up or e, down or e
    grid = VGroup()
    for k in range(-5, 6):
        if k == 0:
            continue
        if -eL - 1e-6 <= k * 5 * u <= e:
            grid.add(Line(P + np.array([k * 5 * u, -eD, 0]), P + np.array([k * 5 * u, eU, 0])))
        if -eD - 1e-6 <= k * 5 * u <= eU:
            grid.add(Line(P + np.array([-eL, k * 5 * u, 0]), P + np.array([e, k * 5 * u, 0])))
    grid.set_stroke(DIM, 1, opacity=0.35)
    re_axis = Arrow(P + LEFT * eL, P + RIGHT * (e + 0.15), buff=0, stroke_width=2.5, color=FG,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.05)
    im_axis = Arrow(P + DOWN * eD, P + UP * (eU + 0.15), buff=0, stroke_width=2.5, color=FG,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.05)
    re_lbl = T("Re", 30, DIM).next_to(re_axis.get_end(), UP, buff=0.12).shift(LEFT * 0.25)
    im_lbl = T("Im", 30, DIM).next_to(im_axis.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.12)
    return VGroup(grid, re_axis, im_axis, re_lbl, im_lbl)


def arrow_at(P, R, phase):
    return Arrow(P, P + R * ang(phase), buff=0, stroke_width=6, color=GOLD, tip_length=0.26,
                 max_tip_length_to_length_ratio=0.3).set_z_index(3)


def shadow_at(P, R, phase, opacity=1.0):
    tip = P + R * ang(phase)
    foot = np.array([tip[0], P[1], 0.0])
    if abs(tip[1] - foot[1]) > 0.08:
        line = DashedLine(tip, foot, color=DIM, stroke_width=2.5, dash_length=0.08)
    else:
        line = Line(foot + UP * 0.001, foot, color=DIM, stroke_width=2.5)
    dot = Dot(foot, radius=0.1, color=BLUE).set_z_index(4)
    line.set_stroke(opacity=opacity)
    return VGroup(line, dot)


def triangle_parts():
    """Clip 3's picture: plane, 24 / 7 legs, GOLD arrow, BLUE shadow dot, labels."""
    tip = P3 + R3 * ang(-DELTA)
    foot = np.array([tip[0], P3[1], 0.0])
    d = {}
    d["plane"] = plane(P3, R3, left=1.1, up=2.3, down=2.8)
    d["leg24"] = Line(P3, foot, color=BLUE, stroke_width=6)
    d["leg7"] = Line(foot, tip, color=PINK, stroke_width=6)
    d["arrow"] = arrow_at(P3, R3, -DELTA)
    d["dot"] = Dot(foot, radius=0.1, color=BLUE).set_z_index(4)
    d["l24"] = tex("24", size=38, color=BLUE).move_to((P3 + foot) / 2 + UP * 0.36)
    d["l7"] = tex("7", size=38, color=PINK).next_to(d["leg7"], RIGHT, buff=0.2)
    n = np.array([-7, -24, 0]) / 25.0
    d["l25"] = tex("25", size=38, color=GOLD).move_to((P3 + tip) / 2 + 0.42 * n)
    d["tip"] = tex("24-7i", size=38, color=GOLD).move_to(tip + np.array([0.15, -0.5, 0]))
    for k in ("l24", "l7", "l25", "tip"):
        set_backstroke(d[k], width=5)
    return d


def recap_panel():
    d = triangle_parts()
    return VGroup(d["plane"], d["leg24"], d["leg7"], d["arrow"], d["dot"],
                  d["l24"], d["l7"], d["l25"], d["tip"])


def wave(t_end):
    t_end = max(t_end, 0.01)
    return ParametricFunction(
        lambda t: G0 + np.array([K_T * t, R4 * np.cos(3 * t - DELTA), 0.0]),
        t_range=[0, t_end, 0.01], color=BLUE, stroke_width=4)


def wave_pt(t):
    return G0 + np.array([K_T * t, R4 * np.cos(3 * t - DELTA), 0.0])


class F19(NarratedScene):
    def construct(self):
        S1 = load_scene("ch8_s1_intro")
        self.clip1(S1)
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ============================================================ clip 1: the card
    def clip1(self, S1):
        with self.say("c8.f19.1") as c:
            row = S1.card_row()
            f19 = row.cards[6]
            others = row.cards[:6]
            kw = dict(font_size=40, color=FG)
            lines = [
                Tex(r"$x = 7 + 24\cos 3t + 7\sin 3t$. Show that the displacement from", **kw),
                Tex(r"the centre (at $x = 7$) is the real part of ", r"$X = (24-7i)e^{3it}$", r",", **kw),
                Tex(r"and obtain the amplitude. By writing $X$ in the form $Ae^{i\varphi}$", **kw),
                Tex(r"($A$, $\varphi$ real), find the time of the first two passages through", **kw),
                Tex(r"the centre after $t = 0$, and the distances of the stationary", **kw),
                Tex(r"points from the origin.", **kw),
            ]
            q = S1.question_card("F19", lines)
            self.q = q

            self.play(FadeIn(row), run_time=1.0)  # early: the chapter's card row, as in s1
            self.play(FlashAround(f19.box, time_width=1.5), run_time=1.2)
            self.play(*disappear(*others), run_time=0.8)
            rest = [f19.icon, f19.tag]
            self.play(TransformFromCopy(f19.box, q.box),
                      f19.label.animate.scale(q.label.height / f19.label.height).move_to(q.label),
                      *during(disappear(*rest, f19.box), 0.0, 0.5), run_time=1.5)
            self.remove(f19.label)
            self.add(q.label)
            self.play(*appear(*lines, q.icon, lag=0.2), run_time=1.6)  # early: the question card is shown whole, then read

            c.wait_until("show")
            self.play(*recolor(lines[1][1], GOLD), run_time=1.0)
            c.wait_until("stop")
            self.play(FlashAround(q.icon, run_time=1.5, time_width=1.5), run_time=1.5)

    # ============================================================ clip 2: the algebra
    def clip2(self):
        with self.say("c8.f19.2", gap=1.0) as c:
            eq = tex("x", "-", "7", "=", "24", r"\cos 3t", "+", "7", r"\sin 3t", size=56)
            eq.move_to([0, 2.8, 0])
            eq[2].set_color(YELLOW)
            self.play(*swap(self.q, eq), run_time=1.2)

            line = NumberLine(x_range=[-20, 35, 5], length=11, color=DIM, include_tip=True,
                              tick_size=0.08, stroke_width=2.5).move_to([nl_x(7.5), NL_Y, 0])
            zero_lbl = tex("0", size=36, color=DIM).move_to([nl_x(0), NL_Y - 0.42, 0])
            x_lbl = tex("x", size=36, color=DIM).next_to(line.get_right(), UP, buff=0.12)
            seven_dot = Dot([nl_x(7), NL_Y, 0], radius=0.11, color=YELLOW).set_z_index(2)
            seven_lbl = tex("7", size=36, color=YELLOW).move_to([nl_x(7), NL_Y - 0.42, 0])
            centre_lbl = T("centre", 30, YELLOW).move_to([nl_x(7), NL_Y - 0.95, 0])
            self.play(*appear(line, zero_lbl, x_lbl, shift=None, lag=0.15),
                      FadeIn(seven_dot, scale=0.5), run_time=1.0)
            self.play(*appear(seven_lbl, centre_lbl, lag=0.3), run_time=1.0)  # early: the centre, named in the line above
            nl = [line, zero_lbl, x_lbl, seven_dot, seven_lbl, centre_lbl]

            # {form}: matched to ch6's (81)
            f = tex("a", r"\cos", r"\omega t", "+", "b", r"\sin", r"\omega t", size=48)
            f[0].set_color(BLUE)
            f[4].set_color(BLUE)
            num = T("(81)", 30, DIM)
            VGroup(f, num.next_to(f, RIGHT, buff=0.5)).move_to([0, 1.7, 0])
            f.set_x(eq[4:].get_x())
            num.next_to(f, RIGHT, buff=0.5)
            a_eq = tex("a", "=", "24", size=44, color=BLUE).move_to([-2.6, 0.6, 0])
            b_eq = tex("b", "=", "7", size=44, color=BLUE).move_to([0.0, 0.6, 0])
            w_eq = tex(r"\omega", "=", "3", size=44).move_to([2.6, 0.6, 0])
            for m in (a_eq, b_eq):
                m[1].set_color(FG)
            c.wait_until("form")
            self.play(*appear(f, num, lag=0.3), run_time=1.2)
            self.play(*appear(a_eq, b_eq, w_eq, lag=0.3), *recolor(eq[4], BLUE),
                      *recolor(eq[7], BLUE), run_time=1.4)

            # {amp}: A = a - ib  =>  24 - 7i
            box_a = tex("A", "=", "a", "-ib", size=50)
            box_a[0].set_color(YELLOW)
            box_a[2].set_color(BLUE)
            box_a[3].set_color(PINK)
            box_r = SurroundingRectangle(box_a, color=YELLOW, buff=0.2, stroke_width=3)
            boxg = VGroup(box_a, box_r).move_to([-2.0, -0.6, 0])
            imp = tex(r"\Rightarrow", size=50).move_to([0.3, -0.6, 0])
            res = tex("24-7i", size=50, color=GOLD).next_to(imp, RIGHT, buff=0.4)
            set_backstroke(res, width=5)
            c.wait_until("amp")
            self.play(*during(disappear(*nl), 0.0, 0.45), *during(appear(boxg), 0.5, 1.0),
                      run_time=1.4)
            c.wait_until("so twenty-four minus")
            self.play(*appear(imp, res, lag=0.3), run_time=1.2)
            self.res = res

            # {expand}
            ex = tex(r"\mathrm{Re}\big[(24-7i)(\cos 3t+i\sin 3t)\big]", "=", r"24\cos 3t", "+",
                     r"7\sin 3t", size=44).move_to([0, -1.95, 0])
            prod = tex(r"-7i\cdot i\sin 3t", "=", r"+7\sin 3t", size=42, color=PINK)
            prod[1].set_color(FG)
            prod.move_to([0, -3.1, 0])
            c.wait_until("expand")
            self.play(*appear(ex), run_time=1.2)
            c.wait_until("since")
            self.play(*appear(prod), run_time=1.0)
            self.play(FlashAround(prod, time_width=1.5), FlashAround(ex[4], time_width=1.5),
                      run_time=1.5)

    # ============================================================ clip 3: the triangle and polar form
    def clip3(self):
        with self.say("c8.f19.3") as c:
            d = triangle_parts()
            self.d = d
            sweep_clear(self, *appear(d["plane"], shift=None), keep=[self.res])
            self.play(GrowArrow(d["arrow"]),
                      self.res.animate.scale(d["tip"].height / self.res.height).move_to(d["tip"]),
                      run_time=1.5)
            self.remove(self.res)
            self.add(d["tip"])
            c.wait_until("makes a seven")
            self.play(Create(d["leg24"]), Create(d["leg7"]), FadeIn(d["dot"], scale=0.5),
                      *appear(d["l7"], d["l24"], d["l25"], lag=0.35), run_time=1.6)

            X = 3.6
            mod = tex(r"|24-7i|", "=", r"\sqrt{576+49}", "=", "25", size=40).move_to([X, 2.9, 0])
            mod[4].set_color(GOLD)
            amp_t = VGroup(T("amplitude", 36), tex("25", size=46, color=GOLD)).arrange(RIGHT, buff=0.25)
            amp_t[1].align_to(amp_t[0], DOWN)
            amp_r = SurroundingRectangle(amp_t, color=GOLD, buff=0.2, stroke_width=3)
            amp = VGroup(amp_r, amp_t).move_to([X, 1.9, 0])
            self.play(*appear(mod), run_time=1.0)
            c.wait_until("is twenty-five")
            self.play(GrowFromCenter(amp_r), *appear(amp_t, shift=None), run_time=1.0)

            # {delta}
            arc = Arc(radius=0.4 * R3, start_angle=-DELTA, angle=DELTA, arc_center=P3, color=YELLOW,
                      stroke_width=4)
            dl = tex(r"\delta", size=38, color=YELLOW).move_to(P3 + 0.53 * R3 * ang(-DELTA / 2))
            set_backstroke(dl, width=5)
            c.wait_until("minus delta")
            self.play(Create(arc), *appear(dl), run_time=1.2)
            dline = tex(r"\delta", "=", r"\arctan\tfrac{7}{24}", r"\approx", r"0.284\,\mathrm{rad}",
                        r"\approx", r"16.3^\circ", size=36).move_to([X, 0.8, 0])
            dline[0].set_color(YELLOW)
            c.wait_until("tangent")
            self.play(*appear(dline), run_time=1.2)
            pol0 = tex("24-7i", "=", "25", r"e^{-i\delta}", size=44).move_to([X, -0.25, 0])
            pol0[0].set_color(GOLD)
            pol0[2].set_color(GOLD)
            c.wait_until("about sixteen")
            self.play(*appear(pol0), run_time=1.2)

            # {polar}
            Xl = tex("X", "=", "25", r"e^{i(3t-\delta)}", size=46).move_to([X, -1.4, 0])
            Xl[2].set_color(GOLD)
            xm = tex("x-7", "=", "25", r"\cos(3t-\delta)", size=46).move_to([X, -2.5, 0])
            xm[2].set_color(GOLD)
            note = Tex(r"sheet's $Ae^{i\varphi}$:\ its $A = |24-7i| = 25$,\ its $\varphi = 3t-\delta$",
                       font_size=32, color=DIM).move_to([0, -3.45, 0])
            c.wait_until("complex quantity")
            self.play(*appear(Xl), run_time=1.2)
            c.wait_until("and ex minus seven")
            self.play(*appear(xm), run_time=1.2)
            self.play(*appear(note), run_time=1.0)  # early: a side note mapping the sheet's letters
            self.xm = xm
            self.col = [mod, amp, dline, pol0, Xl, arc, dl]
            self.note = note

    # ============================================================ clip 4: passages through the centre
    def clip4(self):
        with self.say("c8.f19.4") as c:
            d = self.d
            xm = self.xm
            plane4 = plane(P4, R4)
            gone = self.col + [d["leg24"], d["leg7"], d["l24"], d["l7"], d["l25"], d["tip"]]
            self.play(*during(disappear(*gone), 0.0, 0.45),
                      *during([xm.animate.move_to([2.6, 3.2, 0])], 0.45, 1.0),
                      *during([FadeOut(d["plane"])], 0.0, 0.45),
                      *during([FadeIn(plane4)], 0.5, 1.0),
                      *during([Transform(d["arrow"], arrow_at(P4, R4, -DELTA)),
                               d["dot"].animate.move_to(P4 + R4 * np.cos(DELTA) * RIGHT)], 0.3, 1.0),
                      run_time=1.6)

            tt = ValueTracker(0.0)
            sop = ValueTracker(0.0)
            ph = lambda: 3 * tt.get_value() - DELTA  # noqa: E731
            arr = always_redraw(lambda: arrow_at(P4, R4, ph()))
            shd = always_redraw(lambda: shadow_at(P4, R4, ph(), sop.get_value()))
            self.remove(d["arrow"], d["dot"])
            self.add(shd, arr)

            # the wave axes: t along the centre line x = 7, x up
            t_axis = Arrow(G0 + LEFT * 0.1, G0 + RIGHT * (K_T * T_AX + 0.3), buff=0, stroke_width=2.5,
                           color=DIM, tip_length=0.18, max_tip_length_to_length_ratio=0.05)
            x_axis = Arrow(G0 + DOWN * (R4 + 0.35), G0 + UP * (R4 + 0.4), buff=0, stroke_width=2.5,
                           color=DIM, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
            t_lbl = tex("t", size=34, color=DIM).next_to(t_axis.get_end(), RIGHT, buff=0.12)
            x_lbl = tex("x", size=34, color=DIM).next_to(x_axis.get_end(), RIGHT, buff=0.12)
            ext = VGroup(*[DashedLine(G0 + s * R4 * UP, G0 + s * R4 * UP + RIGHT * K_T * T_AX,
                                      dash_length=0.1, color=DIM, stroke_width=1.5)
                           .set_stroke(opacity=0.6) for s in (1, -1)])
            l32 = tex("32", size=32, color=DIM).next_to(G0 + R4 * UP, LEFT, buff=0.2)
            l7 = tex("7", size=32, color=YELLOW).next_to(G0, LEFT, buff=0.2)
            lm18 = tex("-18", size=32, color=DIM).next_to(G0 + R4 * DOWN, LEFT, buff=0.2)
            circ = Circle(radius=R4, color=DIM, stroke_width=2).move_to(P4)
            axes = [t_axis, x_axis, t_lbl, x_lbl, ext, l32, l7, lm18]
            self.play(*appear(circ, *axes, shift=None, lag=0.08), sop.animate.set_value(1.0),
                      run_time=1.2)
            curve = always_redraw(lambda: wave(tt.get_value()))
            pen = always_redraw(lambda: Dot(wave_pt(tt.get_value()), radius=0.08, color=BLUE))
            self.add(curve, pen)
            self.l32, self.lm18 = l32, lm18

            # {t1}
            c.wait_until("t1")
            self.play(*disappear(self.note), run_time=0.6)
            self.play(tt.animate.set_value(T1), run_time=2.2, rate_func=linear)
            m1 = Dot(wave_pt(T1), radius=0.1, color=YELLOW).set_z_index(5)
            t1_lbl = tex("t_1", size=34, color=YELLOW).move_to(wave_pt(T1) + np.array([-0.4, -0.42, 0]))
            t1_eq = tex(r"3t-\delta=\tfrac{\pi}{2}", r"\Rightarrow", r"t_1=(\tfrac{\pi}{2}+\delta)/3",
                        r"\approx 0.618", size=40).move_to([2.6, 2.3, 0])
            t1_eq[2][0:2].set_color(YELLOW)
            self.play(FadeIn(m1, scale=0.5), *appear(t1_lbl, t1_eq, lag=0.4), run_time=1.5)

            # {t2}
            c.wait_until("t2")
            self.play(tt.animate.set_value(T2), run_time=2.0, rate_func=linear)
            m2 = Dot(wave_pt(T2), radius=0.1, color=YELLOW).set_z_index(5)
            t2_lbl = tex("t_2", size=34, color=YELLOW).move_to(wave_pt(T2) + np.array([0.4, -0.42, 0]))
            t2_eq = tex(r"t_2=(\tfrac{3\pi}{2}+\delta)/3", r"\approx 1.665", size=40)
            t2_eq.next_to(t1_eq, DOWN, buff=0.35).align_to(t1_eq[2], LEFT)
            t2_eq[0][0:2].set_color(YELLOW)
            self.play(FadeIn(m2, scale=0.5), *appear(t2_lbl, t2_eq, lag=0.4), run_time=1.5)
            half = DoubleArrow(wave_pt(T1) + UP * 0.45, wave_pt(T2) + UP * 0.45, buff=0, color=FG,
                               stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.1)
            half_lbl = Tex(r"half a turn later: $+\tfrac{\pi}{3}$", font_size=32, color=FG)
            half_lbl.next_to(half, UP, buff=0.15)
            self.play(GrowFromCenter(half), *appear(half_lbl), run_time=1.2)  # early: names the gap just said
            self.tt = tt

    # ============================================================ clip 5: the stationary points
    def clip5(self):
        with self.say("c8.f19.5", gap=2.0) as c:
            tt = self.tt
            self.play(tt.animate.set_value(T_FLAT), run_time=1.8, rate_func=linear)
            hi = Dot(wave_pt(T_FLAT), radius=0.11, color=GOLD).set_z_index(5)
            lo = Dot(wave_pt(T_MIN), radius=0.11, color=GOLD).set_z_index(5)
            c.wait_until("twenty-five either side")
            self.play(FadeIn(hi, scale=0.5), FadeIn(lo, scale=0.5), *recolor(self.l32, GOLD),
                      *recolor(self.lm18, GOLD), run_time=1.0)
            self.play(FlashAround(self.l32, time_width=1.5), FlashAround(self.lm18, time_width=1.5),
                      run_time=1.2)

            # {ends}: the number line again
            y = NL_Y5
            line = NumberLine(x_range=[-20, 35, 5], length=11, color=DIM, include_tip=True,
                              tick_size=0.08, stroke_width=2.5).move_to([nl_x(7.5), y, 0])
            x_lbl = tex("x", size=36, color=DIM).next_to(line.get_right(), UP, buff=0.12)
            z_dot = Dot([nl_x(0), y, 0], radius=0.09, color=FG).set_z_index(2)
            z_lbl = tex("0", size=36, color=FG).move_to([nl_x(0), y - 0.42, 0])
            s_dot = Dot([nl_x(7), y, 0], radius=0.11, color=YELLOW).set_z_index(2)
            s_lbl = tex("7", size=36, color=YELLOW).move_to([nl_x(7), y - 0.42, 0])
            c.wait_until("ends")
            sweep_clear(self, *appear(line, x_lbl, z_lbl, s_lbl, shift=None, lag=0.1),
                        FadeIn(z_dot), FadeIn(s_dot))
            p32 = Dot([nl_x(32), y, 0], radius=0.12, color=GOLD).set_z_index(2)
            p18 = Dot([nl_x(-18), y, 0], radius=0.12, color=GOLD).set_z_index(2)
            l32 = tex("32", size=36, color=GOLD).move_to([nl_x(32), y - 0.42, 0])
            l18 = tex("-18", size=36, color=GOLD).move_to([nl_x(-18), y - 0.42, 0])
            self.play(FadeIn(p32, scale=0.5), FadeIn(p18, scale=0.5), *appear(l32, l18, lag=0.3),
                      run_time=1.0)

            # {dist}: distances from the origin
            br32 = BraceBetweenPoints([nl_x(0), y + 0.2, 0], [nl_x(32), y + 0.2, 0], direction=UP,
                                      color=GOLD)
            d32 = tex("32", size=40, color=GOLD).next_to(br32, UP, buff=0.15)
            br18 = BraceBetweenPoints([nl_x(-18), y - 0.75, 0], [nl_x(0), y - 0.75, 0], direction=DOWN,
                                      color=GOLD)
            d18 = tex("18", size=40, color=GOLD).next_to(br18, DOWN, buff=0.15)
            tag = T("from the origin", 32, FG).move_to([0, 2.4, 0])
            ul = underline(tag, RED)
            c.wait_until("dist")
            self.play(GrowFromCenter(br32), GrowFromCenter(br18), *appear(d32, d18, lag=0.2),
                      run_time=1.2)
            self.play(*appear(VGroup(tag, ul)), run_time=1.0)  # early: the question's tag, said at the end of the line
