"""Chapter 7, scene 5: V = V_R + V_C gives Z = R + 1/(iωC) = R − i/(ωC); what Z means. Clips c7.imp.1 – c7.imp.6.

Shared pieces (imported by ch7 s3 / s4):
  amp_plane(center, unit, extent)            ch2's Argand plane for the amplitude picture
  amp_arrows(phase, center, unit, ...)       I0 GOLD, V_R0 BLUE, V_C0 PINK, V0 FG in the 3-4-5 shape
  opening_shot()                             s4's two results top-left (s4 hands over into it)
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
from lib.style import *  # noqa: E402,F403
from lib.paths import load_scene  # noqa: E402

argand_plane = load_scene("ch2_s2_theorem").argand_plane

# ---------------------------------------------------------------- the amplitude picture (shared)
AMP_O = np.array([-2.7, -0.05, 0.0])   # origin of the plane
AMP_U = 0.72                            # screen units per amplitude unit (|I0| = 1, |V0| = 5)
AMP_EXT = 3.6
LAG = np.arctan2(3, 4)                  # 36.87°: V0 behind I0


def _dir(a):
    return np.array([np.cos(a), np.sin(a), 0.0])


def _arrow(a, b, color, width=6, tip=0.26):
    # ch6 s3's phasor arrow style
    return Arrow(a, b, buff=0, stroke_width=width, color=color, tip_length=tip,
                 max_tip_length_to_length_ratio=0.3)


def amp_plane(center=AMP_O, unit=AMP_U, extent=AMP_EXT):
    """ch2's Argand plane (grid, Re/Im axes, DIM unit circle) sized for the 3-4-5 arrows."""
    return argand_plane(center=center, unit=unit, extent=extent)


def amp_arrows(phase=0.0, center=AMP_O, unit=AMP_U, tip_to_tail=False, i_len=2.0, width=6, tip=0.26):
    """The four amplitude arrows, I0 at angle `phase` (radians).

    I0 GOLD (length i_len), V_R0 = R I0 BLUE along it (length 4), V_C0 PINK a quarter turn
    behind (length 3; from the origin, or from V_R0's tip if tip_to_tail), V0 FG (length 5,
    36.87° behind I0). Returns VGroup(vr, vc, v0, i0) with .i0 .vr .vc .v0.
    """
    c = np.array(center, dtype=float)
    vr = _arrow(c, c + 4 * unit * _dir(phase), BLUE, width, tip)
    base = vr.get_end() if tip_to_tail else c
    vc = _arrow(base, base + 3 * unit * _dir(phase - PI / 2), PINK, width, tip)
    v0 = _arrow(c, c + 5 * unit * _dir(phase - LAG), FG, width, tip)
    i0 = _arrow(c, c + i_len * unit * _dir(phase), GOLD, width, tip)
    vr.set_z_index(2)
    vc.set_z_index(2)
    v0.set_z_index(1)
    i0.set_z_index(3)
    g = VGroup(vr, vc, v0, i0)
    g.vr, g.vc, g.v0, g.i0 = vr, vc, v0, i0
    return g


# ---------------------------------------------------------------- maths helpers
def tx(*parts, size=48):
    """MathTex from (tex, colour) pairs (a bare string is FG)."""
    parts = [(p, FG) if isinstance(p, str) else p for p in parts]
    m = MathTex(*[p[0] for p in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        sub.set_color(col)
    return m


def res_r_tex(size=50):
    return tx(("V_{R0}", BLUE), "=", ("R", BLUE), ("I_0", GOLD), size=size)


def res_c_tex(size=50):
    return tx(("V_{C0}", PINK), "=", r"\frac{", ("I_0", GOLD), "}{", ("i", PINK), r"\omega",
              ("C", PINK), "}", size=size)


def opening_shot():
    """s4's two results, top-left, '=' signs aligned: VGroup(V_R0 = R I0, V_C0 = I0/(iωC))."""
    r = res_r_tex().move_to([0, 3.2, 0])
    r.shift((-6.4 - r.get_left()[0]) * RIGHT)
    cc = res_c_tex()
    cc.next_to(r, DOWN, buff=0.45)
    cc.shift((r[1].get_x() - cc[1].get_x()) * RIGHT)
    return VGroup(r, cc)


def right_angle(phase, center=AMP_O, unit=AMP_U, s=0.24):
    corner = np.array(center) + 4 * unit * _dir(phase)
    a, b = -_dir(phase) * s, _dir(phase - PI / 2) * s
    return VMobject().set_points_as_corners([corner + a, corner + a + b, corner + b]).set_stroke(FG, 2.5)


def lag_arc(phase, center=AMP_O, unit=AMP_U):
    return Arc(radius=1.7 * unit, start_angle=phase, angle=-LAG, arc_center=center,
               color=YELLOW, stroke_width=4)


def arg_label(phase, center=AMP_O, unit=AMP_U):
    lbl = MathTex(r"\arg Z < 0", font_size=32, color=YELLOW)
    return lbl.move_to(np.array(center) + 2.6 * unit * _dir(phase - 14 * DEGREES))


def leg_labels(phase, center=AMP_O, unit=AMP_U):
    c = np.array(center)
    lr = tx(("R", BLUE), (r"|I_0|", BLUE), size=36)
    lr.move_to(c + 2 * unit * _dir(phase) + 0.38 * _dir(phase + PI / 2))
    lc = tx((r"\frac{|I_0|}{\omega C}", PINK), size=36)
    mid = c + 4 * unit * _dir(phase) + 1.5 * unit * _dir(phase - PI / 2)
    lc.move_to(mid + 0.72 * _dir(phase))
    return VGroup(lr, lc)


def triangle(phase):
    arrows = amp_arrows(phase, tip_to_tail=True)
    return VGroup(arrows, right_angle(phase), lag_arc(phase), arg_label(phase))


# ---------------------------------------------------------------- the Z picture
W_LO, W_HI = 0.5, 40.0
SL_A, SL_B = np.array([2.3, -0.7, 0]), np.array([6.1, -0.7, 0])


def z_point(w):
    return AMP_O + AMP_U * np.array([4.0, -3.0 / w, 0])


def zpic(w):
    o = AMP_O
    zp = z_point(w)
    corner = o + 4 * AMP_U * RIGHT
    leg_r = Line(o, corner, color=BLUE, stroke_width=6)
    leg_c = Line(corner, zp + 0.001 * DOWN, color=PINK, stroke_width=6)
    zline = Line(o, zp, color=YELLOW, stroke_width=3).set_stroke(opacity=0.7)
    dot = Dot(zp, radius=0.12, color=YELLOW).set_z_index(3)
    zl = MathTex("Z", font_size=40, color=YELLOW).move_to(zp + 0.42 * (LEFT + DOWN))
    zl.set_y(max(zl.get_y(), -3.3))
    cl = tx((r"\frac{1}{\omega C}", PINK), size=36).move_to((corner + zp) / 2 + 0.75 * RIGHT)
    cl.set_opacity(float(np.clip((np.linalg.norm(zp - corner) - 0.45) / 0.6, 0, 1)))
    return VGroup(leg_r, leg_c, zline, dot, zl, cl)


def knob_x(w):
    f = (np.log(w) - np.log(W_LO)) / (np.log(W_HI) - np.log(W_LO))
    return SL_A + f * (SL_B - SL_A)


def coil(width=1.5, n=4, color=YELLOW):
    r = width / (2 * n)
    g = VGroup(*[Arc(radius=r, start_angle=PI, angle=-PI, arc_center=[-width / 2 + r * (2 * k + 1), 0, 0])
                 for k in range(n)])
    g.add(Line([-width / 2 - 0.35, 0, 0], [-width / 2, 0, 0]), Line([width / 2, 0, 0], [width / 2 + 0.35, 0, 0]))
    return g.set_stroke(color, 4)


class Impedance(NarratedScene):
    def construct(self):
        shot = opening_shot()
        self.add(shot)
        res_r, res_c = shot[0], shot[1]
        HERO_Y = 0.55

        # ------------------------------------------------------------ clip 1: V0 = (R + 1/(iωC)) I0
        e1 = tx(r"\text{Since }", "V", "=", ("V_R", BLUE), "+", ("V_C", PINK), r"\;\Rightarrow",
                size=50).move_to([0.6, HERO_Y, 0])
        e2 = tx("V_0", "=", ("V_{R0}", BLUE), "+", ("V_{C0}", PINK), size=50).move_to([0.6, HERO_Y, 0])
        e3 = tx("V_0", "=", ("R", BLUE), ("I_0", GOLD), "+", r"\frac{", ("I_0", GOLD), "}{", ("i", PINK),
                r"\omega", ("C", PINK), "}", size=50).move_to([0.6, HERO_Y, 0])
        e4 = tx("V_0", "=", r"\Big(", ("R", BLUE), "+", r"\frac{1}{", ("i", PINK), r"\omega", ("C", PINK),
                "}", r"\Big)", ("I_0", GOLD), size=50).move_to([0.6, HERO_Y, 0])
        rule2 = tx(r"\text{rule 2: } e^{i\omega t} \text{ cancels}", size=34)
        rule2.set_color(DIM).move_to([4.3, 3.0, 0])

        with self.say("c7.imp.1") as c:
            self.play(*appear(e1), run_time=min(1.2, c.until("The voltages add")))
            c.wait_until("amps")
            self.play(*appear(rule2), run_time=1.0)
            c.wait_until("drop the turning factor")
            self.play(FlashAround(rule2, run_time=1.2, time_width=1.5))
            c.wait_until("the amplitudes add up")
            self.play(*swap(e1, e2), run_time=min(1.4, c.until("fill")))
            c.wait_until("fill")
            e3.shift(e2[1].get_center() - e3[1].get_center())
            self.play(FadeOut(e2[2]), FadeOut(e2[4]), *during([e2[3].animate.move_to(e3[4])], 0.4, 1),
                      run_time=1.0)
            self.remove(*e2.get_family())
            self.add(e3[0], e3[1], e3[4])
            self.play(*fly(res_r[2:4], e3[2:4], arc=-0.5), *fly(res_c[2:9], e3[5:12], arc=-0.5),
                      run_time=min(1.8, c.until("factor")))
            self.remove(*e3.get_family())
            self.add(e3)
            c.wait_until("factor")
            self.play(*edit(e3, e4), run_time=min(1.6, c.until("z")))
            c.wait_until("z")
            self.play(FlashUnder(VGroup(*e4[2:11]), run_time=2, time_width=1.5))
            brace = Brace(VGroup(*e4[2:11]), DOWN, buff=0.15, color=FG)
            zlab_z = MathTex("Z", font_size=48)
            zlab_t = T("complex resistance", 30, color=DIM)
            zlab = VGroup(zlab_z, zlab_t).arrange(RIGHT, buff=0.3).next_to(brace, DOWN, buff=0.15)
            c.wait_until("That bracket")
            self.play(GrowFromCenter(brace), *appear(zlab, lag=0.3), run_time=1.2)  # early: names the bracket said here

        # ------------------------------------------------------------ clip 2: Z = R − i/(ωC), boxed
        inv = tx(r"\frac{1}{", ("i", PINK), "}", "=", "-", ("i", PINK), size=44).move_to([4.6, 2.85, 0])
        why = tx(("i", PINK), r"\cdot", "(-", ("i", PINK), ")", "=", "1", size=40)
        why.next_to(inv, DOWN, buff=0.35)
        zb = tx("Z", "=", ("R", BLUE), "-", r"\frac{", ("i", PINK), "}{", r"\omega", ("C", PINK), "}",
                size=52).move_to([-0.6, -2.45, 0])
        box = SurroundingRectangle(zb, color=YELLOW, buff=0.22, stroke_width=3)
        lab_re = T("real part:\nthe resistor", 30, color=BLUE).next_to(box, LEFT, buff=0.45)
        lab_im = T("imaginary part:\nthe capacitor, negative", 30, color=PINK).next_to(box, RIGHT, buff=0.45)

        with self.say("c7.imp.2") as c:
            # flash only the i: an underline under its own glyph (a ring round it would take in the ω)
            self.play(FlashUnder(e4[6], buff=0.08, run_time=1.5, time_width=1.5), *recolor(e4[6], YELLOW))
            c.wait_until("One over eye is minus eye")
            self.play(*swap(rule2, inv), run_time=1.2)
            c.wait_until("because")
            self.play(*appear(why), run_time=1.0)
            c.wait_until("box")
            self.play(*appear(zb), run_time=1.3)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("parts")
            self.play(FlashAround(zb[2], run_time=1.5, time_width=1.5), *appear(lab_re), run_time=1.5)
            c.wait_until("Its imaginary part")
            self.play(FlashAround(VGroup(*zb[3:10]), run_time=1.5, time_width=1.5), *appear(lab_im),
                      run_time=1.5)

        # ------------------------------------------------------------ clip 3: the triangle
        zg = VGroup(zb, box)
        self.remove(zb, box)
        self.add(zg)
        plane = amp_plane()
        A = amp_arrows(0.0)
        T0 = amp_arrows(0.0, tip_to_tail=True)
        ra = right_angle(0.0)
        legs = leg_labels(0.0)

        with self.say("c7.imp.3") as c:
            sweep_clear(self, zg.animate.scale(0.72).move_to([4.75, 2.9, 0]), FadeIn(plane), keep=[zg],
                        run_time=min(1.6, c.until("triangle")))
            c.wait_until("triangle")
            self.play(LaggedStart(GrowArrow(A.vr), GrowArrow(A.vc), GrowArrow(A.i0), lag_ratio=0.3),
                      run_time=1.6)
            c.wait_until("The resistor's lies along the current")
            self.play(VShowPassingFlash(Line(A.vr.get_start(), A.vr.get_end()).set_stroke(YELLOW, 10),
                                        time_width=0.5), run_time=1.2)
            c.wait_until("quarter turn behind")
            self.play(A.vc.animate.move_to(T0.vc), run_time=1.8)
            c.wait_until("right angle")
            self.play(FadeIn(ra), run_time=0.8)
            c.wait_until("sum")
            self.play(GrowArrow(T0.v0), run_time=1.5)
            c.wait_until("the long side")
            self.play(*appear(*legs, lag=0.4), run_time=min(1.4, c.until(floor=0.5)))  # early: the legs, named by the shape

        # ------------------------------------------------------------ clip 4: size and lag
        size_eq = tx("|", ("I_0", GOLD), "|", "=", r"\frac{|V_0|}{|Z|}", size=48).move_to([4.3, 0.35, 0])
        arc = lag_arc(0.0)
        alab = arg_label(0.0)
        lag_cap = T("the voltage lags\nthe current", 32).move_to([4.2, -2.4, 0])

        with self.say("c7.imp.4") as c:
            self.play(*appear(size_eq), run_time=1.2)
            c.wait_until("Divide the size")
            self.play(FlashAround(size_eq[4], run_time=1.5, time_width=1.5))
            c.wait_until("lag")
            self.play(Create(arc), *appear(alab), run_time=1.4)
            # swap the frozen pieces for a live triangle and turn it once, as a whole
            self.remove(*A.get_family(), *T0.get_family(), ra, arc, alab)
            ph = ValueTracker(0.0)
            live = always_redraw(lambda: triangle(ph.get_value()))
            self.add(live)
            rt = c.until(floor=2.0) - 0.1
            cap_t = max(1.0, min(rt - 1.0, c.until("voltage arrow trails", floor=0.0)))
            self.play(ph.animate.set_value(TAU), *[time_span(FadeOut(m), 0, 0.6) for m in legs],
                      time_span(FadeIn(lag_cap, shift=0.2 * DOWN), cap_t, cap_t + 1.0),
                      run_time=rt, rate_func=linear)
            live.clear_updaters()
            self.remove(live)
            S = triangle(0.0)
            self.add(S)

        # ------------------------------------------------------------ clip 5: Z on the plane, ω slides
        arrows, s_ra, s_arc, s_alab = S
        z0 = zpic(1.0)
        rlab = MathTex("R", font_size=40, color=BLUE).move_to(AMP_O + 2 * AMP_U * RIGHT + 0.38 * UP)
        track = Line(SL_A, SL_B, color=DIM, stroke_width=4)
        w_lab = MathTex(r"\omega", font_size=40).next_to(track, LEFT, buff=0.3)
        lo_t = T("low", 28, color=DIM).next_to(track.get_start(), DOWN, buff=0.25)
        hi_t = T("high", 28, color=DIM).next_to(track.get_end(), DOWN, buff=0.25)
        w = ValueTracker(1.0)
        knob = always_redraw(lambda: Dot(knob_x(w.get_value()), radius=0.13, color=FG))
        reline = DashedLine(AMP_O + 4 * AMP_U * RIGHT + AMP_EXT * UP, AMP_O + 4 * AMP_U * RIGHT + AMP_EXT * DOWN,
                            color=DIM, stroke_width=2, dash_length=0.1)
        cap_lo = T("low ω: |Z| huge,\nalmost no current", 32).move_to([4.2, -2.4, 0])
        cap_hi = T("high ω: Z ≈ R", 32).move_to([4.2, -2.4, 0])

        with self.say("c7.imp.5") as c:
            self.play(ReplacementTransform(arrows.vr, z0[0]), ReplacementTransform(arrows.vc, z0[1]),  # early: the slider's ends, shown whole before they are walked
                      ReplacementTransform(arrows.v0, z0[2]),
                      *during([FadeOut(m) for m in (arrows.i0, s_ra, s_arc, s_alab, size_eq)],
                              0, 0.45),
                      *during([FadeIn(z0[3]), FadeIn(z0[4]), FadeIn(z0[5]), FadeIn(rlab),
                               FadeIn(track), FadeIn(w_lab), FadeIn(lo_t), FadeIn(hi_t)], 0.5, 1),
                      run_time=1.5)
            self.remove(*z0.get_family())
            zdyn = always_redraw(lambda: zpic(w.get_value()))
            self.add(zdyn, knob)
            self.play(w.animate.set_value(0.68), FadeIn(reline), run_time=2.2)
            self.play(*swap(lag_cap, cap_lo), run_time=1.2)
            c.wait_until("high")
            self.play(w.animate.set_value(30.0), *during(swap(cap_lo, cap_hi), 0.45, 1), run_time=2.4)
            c.wait_until("sheet")
            zdyn.clear_updaters()
            knob.clear_updaters()
            expr = tx(r"\frac{e^{", ("i", PINK), r"\omega t}}{", ("R", BLUE), "+", ("i", PINK), r"\omega L",
                      "+", "(", ("i", PINK), r"\omega", ("C", PINK), ")^{-1}}", size=60).move_to([0, 0.9, 0])
            tag = T("Examples Sheet I, F1(h) and F3(d)", 32, color=DIM).move_to([0, 2.75, 0])
            # everything leaves together over 0.8 s (plane, Z picture, slider, captions), then the expression
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.5), *during(appear(expr), 0.55, 1),
                      run_time=1.6)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("inductor")
            iwl = [*expr[5], *expr[6]]
            self.play(*recolor(iwl, YELLOW), FlashAround(VGroup(expr[5], expr[6]), run_time=1.5, time_width=1.5),
                      run_time=1.5)
            cl = coil().move_to([VGroup(expr[5], expr[6]).get_x(), -0.75, 0])
            ind = T("inductor L", 30, color=YELLOW).next_to(cl, DOWN, buff=0.3)
            c.wait_until("a coil of wire")
            self.play(*appear(cl, ind, lag=0.3), run_time=1.0)
            ans = T("answers: end of the sheet", 30, color=DIM).move_to([0, -2.9, 0])
            c.wait_until(own_word=ans)
            self.play(*appear(ans), run_time=1.0)

        # ------------------------------------------------------------ clip 6: the lecturer's summary
        divider = Line([0, 2.6, 0], [0, -2.6, 0], color=DIM, stroke_width=2)
        xm = cross_mark().scale(1.3).move_to([-3.5, 1.9, 0])
        left = T("sines and cosines:\nequate, differentiate,\nequate again", 36, color=DIM)
        left.move_to([-3.5, 0.0, 0])
        tick = check_mark().scale(1.3).move_to([3.5, 1.9, 0])
        right = T("exponentials:\nequate amplitudes;", 36).move_to([3.5, 0.3, 0])
        rule = tx(r"\frac{d}{dt}", r"\;\to\;", r"\times\,", ("i", PINK), r"\omega", size=50)
        rule.next_to(right, DOWN, buff=0.45)

        with self.say("c7.imp.6") as c:
            sweep_clear(self, GrowFromCenter(divider), run_time=min(1.6, c.until("With sines")))
            c.wait_until(own_word=left)
            self.play(*appear(xm, left, lag=0.3), run_time=1.3)
            c.wait_until("exp")
            self.play(*appear(tick, right, rule, lag=0.4), run_time=1.6)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
