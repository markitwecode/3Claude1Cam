"""Chapter 6, scene 6: try F19, and recap. Clips c6.try.1, c6.try.2, c6.recap.1.

Reuses s3's shared builders (argand_plane, plane_circle, phasor_arrow, shadow, pendulum, x_graph),
built full size at s3's P0 and placed small (Place). Recap arrows turn on scene time
(phase = PHI0 + OMEGA t, one turn = 4 s), all in step. Last scene of the chapter: ends on the
end card (circuit + "d/dt -> x i omega", "calculus -> algebra") held ~8 s, then fades.
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
S4 = load_scene("ch6_s4_derivative")
P0, U, R, OMEGA, PHI0 = S3.P0, S3.U, S3.R, S3.OMEGA, S3.PHI0
ang = S3.ang

NL_Y = 0.2                      # F19 number line


def nl_x(v):                    # number line: value -> screen x  (-20..35 over 11 units)
    return -1.5 + 0.2 * v


class Place:
    """Scale + shift that maps a full-size reference build onto a small spot."""

    def __init__(self, ref, target, height=None, width=None):
        self.c0 = ref.get_center()
        scs = [x for x in (height and height / ref.height, width and width / ref.width) if x]
        self.sc = min(scs)
        self.d = np.array(target, dtype=float) - self.c0

    def __call__(self, m):
        return m.scale(self.sc, about_point=self.c0).shift(self.d)


def plane_axes(extent=2.4):
    p = S3.argand_plane(extent=extent)
    return VGroup(p.grid, p.re_axis, p.im_axis)


def tex(*parts, size=44, color=FG):
    return MathTex(*parts, font_size=size, color=color)


class Recap(NarratedScene):
    def dyn(self, build):
        """An always_redraw object whose opacity follows a tracker (starts hidden)."""
        tr = ValueTracker(0.0)
        mob = always_redraw(lambda: build().set_opacity(tr.get_value()))
        return mob, tr

    def construct(self):
        self.t_ref = 0.0
        self.ph = lambda: PHI0 + OMEGA * (self.renderer.time - self.t_ref)
        self.try_1()
        self.try_2()
        self.recap()
        self.wait(7.6)                                   # end card, music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ============================================================ c6.try.1
    def try_1(self):
        with self.say("c6.try.1") as c:
            title = T("Examples Sheet I  ·  F19", 44, t2c={"F19": YELLOW}).move_to([0, 3.35, 0])
            t_b = select(title, "F19")[0]
            rule = Line(LEFT * 3.4, RIGHT * 3.4, color=DIM, stroke_width=2).move_to([0, 2.95, 0])
            self.play(*appear(title, shift=None), GrowFromCenter(rule), run_time=1.0)  # early: the sheet's title card
            c.wait_until("nineteen")
            self.play(FlashAround(t_b, run_time=1.5, time_width=1.5), run_time=1.5)

            # {motion}
            eq = tex("x", "=", "7", "+", "24", r"\cos 3t", "+", "7", r"\sin 3t", size=56)
            eq.move_to([0, 2.15, 0])
            c.wait_until("motion")
            self.play(*appear(eq, shift=None), run_time=1.2)

            # {centre}: the number line, 7 marked
            line = NumberLine(x_range=[-20, 35, 5], length=11, color=DIM, include_tip=True,
                              tick_size=0.08, stroke_width=2.5).move_to([nl_x(7.5), NL_Y, 0])
            zero_lbl = tex("0", size=36, color=DIM).move_to([nl_x(0), NL_Y - 0.42, 0])
            x_lbl = tex("x", size=36, color=DIM).next_to(line.get_right(), UP, buff=0.12)
            seven_dot = Dot([nl_x(7), NL_Y, 0], radius=0.11, color=YELLOW).set_z_index(2)
            seven_lbl = tex("7", size=36, color=YELLOW).move_to([nl_x(7), NL_Y - 0.42, 0])
            centre_lbl = T("centre of motion", 30, YELLOW).move_to([nl_x(7), NL_Y - 0.95, 0])
            c.wait_until("centre")
            self.play(*appear(line, zero_lbl, x_lbl, shift=None, lag=0.15), run_time=1.0)
            self.play(eq[2].animate.set_color(YELLOW), FadeIn(seven_dot, scale=0.5),
                      *appear(seven_lbl), run_time=1.2)
            c.wait_until(own_word=centre_lbl, cue="seven")
            self.play(*appear(centre_lbl), run_time=0.9)

            # {match}: the rest is s3's SHM
            brace = Brace(VGroup(*eq[4:9]), DOWN, buff=0.12, color=DIM)
            brace_lbl = T("displacement from the centre", 30, DIM).next_to(brace, DOWN, buff=0.12)
            c.wait_until("match")
            self.play(GrowFromCenter(brace), *appear(brace_lbl), run_time=1.1)

            box_a = tex("A", "=", "a", "-ib", size=42)
            box_a[0].set_color(YELLOW)
            box_a[2].set_color(BLUE)
            box_a[3].set_color(PINK)
            box_r = SurroundingRectangle(box_a, color=YELLOW, buff=0.18, stroke_width=3)
            boxg = VGroup(box_a, box_r).move_to([-4.6, -1.65, 0])
            a_eq = tex("a", "=", "24", size=44, color=BLUE).move_to([-1.7, -1.65, 0])
            b_eq = tex("b", "=", "7", size=44, color=BLUE).move_to([0.7, -1.65, 0])
            w_eq = tex(r"\omega", "=", "3", size=44).move_to([3.1, -1.65, 0])
            for m in (a_eq, b_eq):
                m[1].set_color(FG)
            c.wait_until("simple harmonic")
            self.play(*appear(boxg), run_time=1.0)
            c.wait_until("cosine coefficient")
            self.play(*appear(a_eq), eq[4].animate.set_color(BLUE), run_time=1.0)
            c.wait_until("seven and omega")
            self.play(*appear(b_eq), eq[7].animate.set_color(BLUE), run_time=1.0)
            c.wait_until("equal to three")
            self.play(*appear(w_eq), run_time=1.0)

            # {hint}
            hint = tex("24", r"\cos 3t", "+", "7", r"\sin 3t", "=", r"\mathrm{Re}", r"\Big[",
                       "(", "24", "-", "7", "i", ")", r"\,e^{3it}", r"\Big]", size=46)
            for k in (0, 3, 9, 11):
                hint[k].set_color(BLUE)
            hint[12].set_color(PINK)
            hint.move_to([0, -2.95, 0])
            c.wait_until("hint")
            self.play(*appear(hint, shift=None), run_time=1.2)
            c.wait_until("twenty-four minus")
            self.play(FlashAround(VGroup(*hint[8:14]), run_time=1.5, time_width=1.5), run_time=1.5)

        self.p1 = dict(title=title, rule=rule, eq=eq, line=line, zero_lbl=zero_lbl, x_lbl=x_lbl,
                       seven_dot=seven_dot, seven_lbl=seven_lbl, centre_lbl=centre_lbl,
                       brace=brace, brace_lbl=brace_lbl, boxg=boxg, a_eq=a_eq, b_eq=b_eq,
                       w_eq=w_eq, hint=hint)

    # ============================================================ c6.try.2
    def try_2(self):
        p = self.p1
        with self.say("c6.try.2") as c:
            polar = tex("24", "-", "7", "i", "=", "|A|", r"\,e^{i\arg A}", size=50)
            polar[0].set_color(BLUE)
            polar[2].set_color(BLUE)
            polar[3].set_color(PINK)
            polar.move_to([-3.4, -2.0, 0])
            gone = [p["brace"], p["brace_lbl"], p["boxg"], p["a_eq"], p["b_eq"], p["w_eq"]]
            q1 = T("?", 40, YELLOW).next_to(polar[5], UP, buff=0.18)
            q2 = T("?", 40, YELLOW).next_to(polar[6], UP, buff=0.1)
            c.wait_until("polar form")
            self.play(*during(disappear(*gone), 0, 0.3), *during(edit(p["hint"], polar), 0.3, 0.8),
                      *during(appear(q1, q2, lag=0.3), 0.8, 1),
                      run_time=min(2.0, 0.95 * c.until("modulus is")))

            amp_lbl = T("amplitude", 30, GOLD).next_to(polar[5], DOWN, buff=0.28)
            c.wait_until("modulus is")
            self.play(polar[5].animate.set_color(GOLD), FlashAround(polar[5], run_time=1.2),
                      run_time=1.2)
            c.wait_until(own_word=amp_lbl)
            self.play(*appear(amp_lbl), run_time=0.9)

            # {crossing}: the tiny s3 arrow and its shadow
            pc = np.array([1.6, -2.2, 0])
            axes = plane_axes()
            place = Place(axes, pc, height=1.92)
            stat = place(VGroup(axes, S3.plane_circle()))
            tph = ValueTracker(PI / 2)
            moving, opm = self.dyn(lambda: place(VGroup(
                S3.shadow(tph.get_value()), S3.phasor_arrow(tph.get_value()))))
            tag = T("through the centre", 30, BLUE).move_to([2.95, -1.85, 0], aligned_edge=LEFT)
            c.wait_until("crossing")
            self.add(moving)
            self.play(*appear(stat, shift=None), opm.animate.set_value(1), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.9)

            # {still}
            tag2 = T("stationary", 30, BLUE).move_to([2.95, -2.6, 0], aligned_edge=LEFT)
            r_s = R * place.sc
            lo = tex("-|A|", size=30, color=GOLD).move_to(pc + LEFT * r_s + DOWN * 0.38)
            hi = tex("|A|", size=30, color=GOLD).move_to(pc + RIGHT * r_s + DOWN * 0.38)
            for m in (lo, hi):
                set_backstroke(m, width=5)
            c.wait_until("still")
            self.play(*appear(tag2), tph.animate.set_value(PI), run_time=1.4)
            self.play(*appear(lo, hi, shift=None, lag=0.3), run_time=0.9)
            self.play(tph.animate.set_value(TAU), run_time=min(1.8, c.until("careful")))

            # {origin}
            from_lbl = T("from the origin", 32, FG).move_to([-4.2, 1.05, 0])
            ul = underline(from_lbl, RED)
            plus = Arrow([nl_x(0), NL_Y + 0.42, 0], [nl_x(7), NL_Y + 0.42, 0], buff=0,
                         color=GOLD, stroke_width=4, tip_length=0.2,
                         max_tip_length_to_length_ratio=0.3)
            plus_lbl = tex("+\,7", size=36, color=GOLD).next_to(plus, UP, buff=0.12)
            c.wait_until(own_word=from_lbl, cue="origin")
            self.play(*appear(from_lbl), run_time=0.9)
            self.play(Create(ul), run_time=0.8)
            c.wait_until("add the seven")
            self.play(GrowArrow(plus), *appear(plus_lbl), run_time=1.2)
            self.play(FlashAround(p["eq"][2], run_time=1.2), run_time=1.2)

            # {part8}
            part8 = T("Full solutions: Part 8", 32, DIM).move_to([-3.4, -3.4, 0])
            c.wait_until(own_word=part8, cue="part8")
            self.play(*appear(part8), run_time=0.9)
        self.part8 = part8

    # ============================================================ c6.recap.1
    def recap(self):
        with self.say("c6.recap.1") as c:
            title = T("Recap", 48).move_to([0, 3.22, 0])
            self.play(*swap(self.p1["title"], title), *disappear(self.p1["rule"]), run_time=1.2)
            self.t_ref = self.renderer.time - (PI / 2 - PHI0) / OMEGA     # arrows start pointing up
            ph = self.ph

            # {r1}: s2's pendulum beside its wave
            def r1_build(theta):
                pend = S3.pendulum(theta, pivot=ORIGIN, length=3.6, labels=False)
                return pend

            gr = S3.x_graph(origin=np.array([1.7, -2.0, 0]), t_max=10)
            graph = VGroup(gr[0], gr[1], gr[4])
            ref = VGroup(r1_build(0.0), graph)
            pl1 = Place(ref, [-3.5, 1.65, 0], height=2.45, width=6.2)
            graph = pl1(graph)
            pend, op1 = self.dyn(lambda: pl1(r1_build(S3.PEND_AMP * np.cos(ph()))))
            cap1 = T("a cosine plus a sine, one ω", 30).move_to([-3.5, 0.0, 0])
            c.wait_until("r1")
            self.add(pend)
            sweep_clear(self, op1.animate.set_value(1), FadeIn(graph),
                        keep=[title, self.part8, pend], run_time=1.6)
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=1.0)

            # {r2}: s3's arrow on its circle, the shadow dot
            ax2 = plane_axes()
            pl2 = Place(ax2, [3.5, 1.65, 0], height=2.45)
            stat2 = pl2(VGroup(ax2, S3.plane_circle()))
            dyn2, op2 = self.dyn(lambda: pl2(VGroup(S3.shadow(ph()), S3.phasor_arrow(ph()))))
            cap2 = tex("x(t)", "=", r"\mathrm{Re}", r"\big[", r"A\,e^{i\omega t}", r"\big]", size=38)
            cap2[0].set_color(BLUE)
            cap2.move_to([3.5, 0.0, 0])
            c.wait_until("r2")
            self.add(dyn2)
            self.play(*appear(stat2, shift=None), op2.animate.set_value(1),
                      *disappear(self.part8), run_time=1.2)
            c.wait_until("complex amplitude")
            self.play(*appear(cap2), run_time=1.0)

            # {r3}: s4's arrows locked at 90 degrees
            ax3 = plane_axes(extent=3.4)
            pl3 = Place(ax3, [-3.5, -1.65, 0], height=2.55)
            stat3 = pl3(VGroup(ax3, S3.plane_circle()))
            dyn3, op3 = self.dyn(lambda: pl3(VGroup(
                S4.elbow(ph(), 1.0),
                S3.phasor_arrow(ph() + PI / 2, length=PI, color=PURPLE).set_z_index(2),
                S3.phasor_arrow(ph()).set_z_index(3))))
            cap3 = T("d/dt: multiply by iω", 30).move_to([-3.5, -3.3, 0])
            c.wait_until("r3")
            self.add(dyn3)
            self.play(*appear(stat3, shift=None), op3.animate.set_value(1), run_time=1.2)
            c.wait_until(own_word=cap3, cue="multiply")
            self.play(*appear(cap3), run_time=1.0)

            # {r4}: s5's picture: Re axis, the GOLD |A| = 2c arrow at -pi/3, the YELLOW arc
            o4, u4 = np.array([0.0, 0.0, 0]), 1.1
            tip4 = o4 + 2 * u4 * ang(-PI / 3)
            re4 = Line(o4 + LEFT * 0.8 * u4, o4 + RIGHT * 2.4 * u4, color=FG, stroke_width=2.5)
            re_lbl = tex(r"\mathrm{Re}", size=32, color=DIM).next_to(re4, RIGHT, buff=0.15)
            arr4 = Arrow(o4, tip4, buff=0, stroke_width=6, color=GOLD, tip_length=0.26,
                         max_tip_length_to_length_ratio=0.3)
            nrm = np.array([-np.sqrt(3) / 2, -0.5, 0])
            lbl_2c = tex("|A|", "=", "2c", size=38, color=GOLD)
            lbl_2c.move_to((o4 + tip4) / 2 + 1.05 * nrm)
            set_backstroke(lbl_2c, width=5)
            arc4 = Arc(radius=0.62, start_angle=0, angle=-PI / 3, arc_center=o4, color=YELLOW,
                       stroke_width=5)
            lbl_ph = tex(r"-\pi/3", size=36, color=YELLOW).move_to(o4 + 1.45 * ang(-PI / 6))
            r4 = VGroup(re4, re_lbl, arr4, lbl_2c, arc4, lbl_ph)
            r4.shift(np.array([3.5, -1.75, 0]) - r4.get_center())
            cap4 = T("modulus: size  ·  argument: phase", 30).move_to([3.5, -3.3, 0])
            c.wait_until("r4")
            self.play(*appear(re4, re_lbl, arr4, shift=None), FadeIn(arc4),
                      *appear(lbl_ph, shift=None), run_time=1.0)
            c.wait_until("modulus")
            self.play(*appear(lbl_2c, shift=None), *appear(cap4), run_time=1.0)
            c.wait_until("phase")
            self.play(FlashAround(VGroup(arc4, lbl_ph), run_time=1.2, time_width=1.5), run_time=1.2)

            # {next}: rows shrink away, the circuit arrives
            rows = [title, graph, cap1, stat2, cap2, stat3, cap3, r4, cap4]
            circuit = self.circuit()
            ac = np.array([4.1, -1.3, 0])
            arrows, op5 = self.dyn(lambda: self.four_arrows(ac, ph()))
            axis5 = Line(ac + LEFT * 1.7, ac + RIGHT * 1.7, color=DIM, stroke_width=2)
            nxt = T("Next: a series circuit", 36, DIM).move_to([0, 3.35, 0])
            c.wait_until("circuit")
            self.add(arrows)
            self.play(*during([FadeOut(m, scale=0.4) for m in rows], 0, 0.45),
                      *during([o.animate.set_value(0) for o in (op1, op2, op3)], 0, 0.45),
                      *during(appear(circuit, axis5, nxt, shift=None, lag=0.15), 0.5, 1),
                      *during([op5.animate.set_value(1)], 0.5, 1),
                      run_time=2.0)
            self.remove(pend, dyn2, dyn3)

            # {algebra}
            l1 = tex(r"\dfrac{d}{dt}", r"\;\longrightarrow\;", r"\times\, i\omega", size=50)
            l1[2].set_color(YELLOW)
            l1.move_to([0, 2.45, 0])
            l2 = tex(r"\text{calculus}", r"\;\longrightarrow\;", r"\text{algebra}", size=44)
            l2[2].set_color(YELLOW)
            l2.move_to([0, 1.45, 0])
            c.wait_until("derivative")
            self.play(*appear(l1), run_time=1.2)
            c.wait_until("calculus")
            self.play(*appear(l2), run_time=1.2)

    # ------------------------------------------------------------ end-card pieces
    def four_arrows(self, c, phase):
        g = VGroup()
        # ch7's colours: source V white (V_R + V_C), V_R BLUE in phase with I GOLD, V_C PINK lagging
        vr, vc = 1.45, 1.05
        v_len, v_off = np.hypot(vr, vc), -np.arctan2(vc, vr)
        for ln, off, col in ((v_len, v_off, FG), (vr, 0.0, BLUE), (vc, -PI / 2, PINK),
                             (0.85, 0.0, GOLD)):
            g.add(Arrow(c, c + ln * ang(phase + off), buff=0, stroke_width=5, color=col,
                        tip_length=0.2, max_tip_length_to_length_ratio=0.3))
        return g

    def circuit(self):
        L, Rx, top, bot = -5.0, 0.4, 0.15, -2.75
        cy = (top + bot) / 2
        w = dict(color=FG, stroke_width=3)
        src_c = Circle(radius=0.42, color=FG, stroke_width=3).move_to([L, cy, 0])
        sim = tex(r"\sim", size=48).move_to(src_c)
        v_lbl = tex("V", size=40).next_to(src_c, LEFT, buff=0.22)
        # resistor zigzag on the top wire
        z0, z1 = -3.3, -1.3
        zx = np.linspace(z0, z1, 9)
        zig = VMobject().set_points_as_corners(
            [[x, top + (0 if k in (0, 8) else (0.22 if k % 2 else -0.22)), 0]
             for k, x in enumerate(zx)]).set_stroke(FG, 3)
        r_lbl = tex("R", size=40).move_to([(z0 + z1) / 2, top + 0.6, 0])
        # capacitor on the right wire
        gap = 0.14
        p1 = Line([Rx - 0.45, cy + gap, 0], [Rx + 0.45, cy + gap, 0], color=FG, stroke_width=4)
        p2 = Line([Rx - 0.45, cy - gap, 0], [Rx + 0.45, cy - gap, 0], color=FG, stroke_width=4)
        c_lbl = tex("C", size=40).next_to(p1, RIGHT, buff=0.25).shift(DOWN * gap)
        wires = VGroup(
            Line([L, cy + 0.42, 0], [L, top, 0], **w), Line([L, top, 0], [z0, top, 0], **w),
            Line([z1, top, 0], [Rx, top, 0], **w), Line([Rx, top, 0], [Rx, cy + gap, 0], **w),
            Line([Rx, cy - gap, 0], [Rx, bot, 0], **w), Line([Rx, bot, 0], [L, bot, 0], **w),
            Line([L, bot, 0], [L, cy - 0.42, 0], **w))
        mid = (L + Rx) / 2
        i_arr = Arrow([mid + 0.5, bot, 0], [mid - 0.5, bot, 0], buff=0, color=GOLD,
                      stroke_width=4, tip_length=0.24, max_tip_length_to_length_ratio=0.4)
        i_lbl = tex("I", size=40, color=GOLD).next_to(i_arr, DOWN, buff=0.15)
        return VGroup(wires, src_c, sim, v_lbl, zig, r_lbl, p1, p2, c_lbl, i_arr, i_lbl)
