"""Chapter 2, scene 2: the hold constraint on the data-sheet diagram. Clips c2.hold.1 – c2.hold.4."""
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


# ============================================================================
# Data-sheet timing-diagram kit (copied from ch1_s5_datasheet.py; same geometry and styling)
# ============================================================================
WAVE_W = 4          # stroke of every trace
ROW_H = 0.8         # high-to-low height of a row
SLOPE = 0.35        # horizontal run of a sloped edge
GUIDE_W = 1.5       # thin grey guides
DIM_W = 3           # dimension arrows


def clock_wave(x0, x1, y, edges, h=ROW_H, slope=SLOPE, color=YELLOW, start_low=True):
    lo, hi = y - h / 2, y + h / 2
    level = lo if start_low else hi
    pts = [np.array([x0, level, 0])]
    for xc in edges:
        other = hi if level == lo else lo
        pts.append(np.array([xc - slope / 2, level, 0]))
        pts.append(np.array([xc + slope / 2, other, 0]))
        level = other
    pts.append(np.array([x1, level, 0]))
    wave = VMobject().set_points_as_corners(pts)
    wave.set_stroke(color, WAVE_W)
    return wave


def bus(x0, x1, y, crossings, h=ROW_H, color=BLUE):
    lo, hi = y - h / 2, y + h / 2
    g = VGroup()
    g.runs, g.xs = [], []
    cur = x0
    for a, b in list(crossings) + [(x1, x1)]:
        if a - cur > 1e-3:
            run = VGroup(Line([cur, hi, 0], [a, hi, 0]), Line([cur, lo, 0], [a, lo, 0]))
            run.set_stroke(color, WAVE_W)
            g.add(run)
            g.runs.append(run)
        if b - a > 1e-3:
            x = VGroup(Line([a, hi, 0], [b, lo, 0]), Line([a, lo, 0], [b, hi, 0]))
            x.set_stroke(color, WAVE_W)
            g.add(x)
            g.xs.append(x)
        cur = b
    return g


def hatch(a, b, n):
    w = (b - a) / n
    return [(a + i * w, a + (i + 1) * w) for i in range(n)]


def guide(x, y_top, y_bot):
    return Line([x, y_top, 0], [x, y_bot, 0]).set_stroke(DIM, GUIDE_W)


def dim_arrow(xa, xb, y, color, tex, label_dir=UP, size=44):
    arr = DoubleArrow([xa, y, 0], [xb, y, 0], buff=0, stroke_width=DIM_W, tip_length=0.16,
                      max_tip_length_to_length_ratio=0.4, color=color)
    lab = MathTex(tex, font_size=size, color=color).next_to(arr, label_dir, buff=0.15)
    return VGroup(arr, lab)
# ============================================================================


# ch1 s5/s6 coordinates (unscaled): one period = 7.0 from E1 to E2
YC, YQ, YD = 2.1, 0.4, -1.3
X0, X1 = -4.6, 6.3
E1, FALL, E2 = -2.8, 0.7, 4.2
PERIOD = E2 - E1
XQ = -1.6                 # Q0 crossover centre (~0.17 of a period)
HATCH_END = 2.7           # D1 settled (~0.8)
XSU = 3.5                 # D1's last X ends: the set-up deadline (0.9)
LAB_X = -5.9
Y_A = -2.4                # ch1's t_pc / t_pd / t_su row
Y_B = -3.3                # t_hold row
Y_C = -3.6                # the (t_pc + t_pd)_min bracket line
Y_GHOST = -4.68           # ghost D1 row / inequality slot
HOLD_END = 0.3            # hold time, in periods

K = 0.8                   # the whole diagram is drawn at 0.8 of ch1's size ...
SY = 0.62                 # ... and raised 0.62, so the rows below fit
SX_FOCUS = 0.7            # at {first} it eases 0.7 right (the first edge nearer the centre)


def ux(u):
    """Period units (0 = first rising edge, 1 = second) to unscaled x."""
    return E1 + u * PERIOD


def hold_diagram(hatch0=0.4, k=K, shift=(0.0, SY)):
    """ch1's data-sheet diagram (CLK YELLOW, Q0 GREEN, D1 BLUE; T_c, t_pc, t_pd, t_su arrows,
    guides) with D1's hatching starting at `hatch0` periods after the first edge (0.5 = ch1's
    'about halfway', 0.4 good, 0.2 the bad geometry). Built in ch1's coordinates, then scaled by
    `k` about ORIGIN and shifted by `shift`. Returns the diagram VGroup with parts as attributes;
    `.band` (GOLD hold band on D1's row, 0 to 0.3 periods) and `.thold` (GOLD t_hold arrow) are
    built and placed too but NOT in the group. Rows are split at D1's hatch end: `.left` and
    `.right` list the pieces on either side (traces, guides, arrows)."""
    xh = ux(hatch0)
    clk_l = clock_wave(X0, HATCH_END, YC, [E1, FALL], color=YELLOW)
    clk_r = clock_wave(HATCH_END, X1, YC, [E2], color=YELLOW)
    clk_lab = T("CLK", 40, YELLOW).move_to([LAB_X, YC, 0])
    g1, g2 = guide(E1, 3.25, -2.6), guide(E2, 3.25, -2.6)
    tc = dim_arrow(E1, E2, 3.05, YELLOW, "T_c")
    q0 = bus(X0, HATCH_END, YQ, [(XQ - 0.2, XQ + 0.2)], color=GREEN)
    q0_r = bus(HATCH_END, X1, YQ, [], color=GREEN)
    q0_lab = MathTex("Q_0", font_size=48, color=GREEN).move_to([LAB_X, YQ, 0])
    gq = guide(XQ, YQ + 0.6, -2.6)
    tpc = dim_arrow(E1, XQ, Y_A, PINK, "t_{pc}", label_dir=DOWN)
    d1 = bus(X0, HATCH_END, YD, hatch(xh, HATCH_END, 4), color=BLUE)
    d1_r = bus(HATCH_END, X1, YD, [(3.1, XSU)], color=BLUE)
    d1_lab = MathTex("D_1", font_size=48, color=BLUE).move_to([LAB_X, YD, 0])
    gsu = guide(XSU, YD + 0.4, -2.6)
    tpd = dim_arrow(XQ, XSU, Y_A, PURPLE, "t_{pd}", label_dir=DOWN)
    tsu = dim_arrow(XSU, E2, Y_A, GOLD, "t_{su}", label_dir=DOWN)

    dg = VGroup(g1, g2, gq, gsu, clk_l, clk_r, q0, q0_r, d1, d1_r,
                clk_lab, q0_lab, d1_lab, tc, tpc, tpd, tsu)
    band = Rectangle(width=ux(HOLD_END) - E1, height=ROW_H + 0.16)
    band.set_stroke(GOLD, 2).set_fill(GOLD, 0.22).move_to([(E1 + ux(HOLD_END)) / 2, YD, 0])
    band.set_z_index(-1)
    thold = dim_arrow(E1, ux(HOLD_END), Y_B, GOLD, r"t_{hold}", label_dir=LEFT)
    for m in (dg, band, thold):
        m.scale(k, about_point=ORIGIN).shift([shift[0], shift[1], 0])
    for name, m in dict(g1=g1, g2=g2, gq=gq, gsu=gsu, clk=clk_l, clk_r=clk_r, q0=q0, q0_r=q0_r,
                        d1=d1, d1_r=d1_r, clk_lab=clk_lab, q0_lab=q0_lab, d1_lab=d1_lab,
                        tc=tc, tpc=tpc, tpd=tpd, tsu=tsu).items():
        setattr(dg, name, m)
    dg.band, dg.thold = band, thold
    dg.right = [clk_r, q0_r, d1_r, g2, gsu, tc, tpd, tsu]
    return dg


def M(x, y, sx=SX_FOCUS):
    """Unscaled ch1 coordinates to the frame, after the {first} ease."""
    return np.array([K * x + sx, K * y + SY, 0])


class Hold(NarratedScene):
    def construct(self):
        # ----------------------------------------------------------- c2.hold.1
        with self.say("c2.hold.1") as c:
            dg = hold_diagram(0.5)                     # as ch1 s6 drew it
            good = hold_diagram(0.4)
            self.play(FadeIn(dg), run_time=1.0)
            self.play(Transform(dg.d1, good.d1), run_time=1.3)
            c.wait_until("clock signal")
            self.play(FlashAround(dg.clk_lab, color=YELLOW), run_time=0.9)
            c.wait_until("cue zero")
            self.play(FlashAround(dg.q0_lab, color=GREEN), run_time=0.9)
            c.wait_until("dee one")
            self.play(FlashAround(dg.d1_lab, color=BLUE), run_time=0.9)

            c.wait_until("first")
            sh = SX_FOCUS * RIGHT
            dimmed = dg.right + [dg.tpc]
            self.play(*[restyle(m, op=DIMMED if m in dimmed else None, shift=sh) for m in dg],
                      run_time=min(1.8, c.until("window")))
            band = dg.band.shift(sh)
            thold = dg.thold.shift(sh)

            c.wait_until("window")
            self.play(FadeIn(band), FlashAround(dg.g1, color=YELLOW), run_time=1.5)
            c.wait_until("hold time")
            self.play(GrowFromCenter(thold[0]), *appear(thold[1]), run_time=1.4)

            right_tag = set_backstroke(T("right side of the window", 30, GOLD))
            right_tag.move_to(M(ux(HOLD_END), -0.45), aligned_edge=RIGHT)
            c.wait_until("right")
            self.play(*appear(right_tag))

            c.wait_until("only")
            trace = band.copy().set_fill(opacity=0).set_stroke(GOLD, 7)
            self.play(VShowPassingFlash(trace, time_width=0.6), run_time=2.2)

            free = set_backstroke(T("free to change", 30, GREEN)).move_to(M(XQ, 1.25))
            c.wait_until(own_word=free)
            self.play(*appear(free), FlashAround(dg.q0.xs[0], color=GREEN), run_time=1.2)

        # ----------------------------------------------------------- c2.hold.2
        with self.say("c2.hold.2") as c:
            edge = Line(M(E1 - SLOPE / 2, YC - ROW_H / 2), M(E1 + SLOPE / 2, YC + ROW_H / 2))
            edge.set_stroke(YELLOW, 10)
            gpulse = dg.g1.copy().set_stroke(YELLOW, 5)
            self.play(VShowPassingFlash(edge, time_width=0.8), VShowPassingFlash(gpulse, time_width=0.5),
                      *disappear(right_tag), run_time=1.4)

            c.wait_until("q0")
            self.play(restyle(dg.tpc, op=1), FlashAround(dg.q0.xs[0], color=PINK), run_time=1.5)
            self.play(FlashUnder(dg.tpc[0], color=PINK), run_time=1.0)

            c.wait_until("hatch")
            xs = dg.d1.xs
            self.play(*disappear(free),
                      *[time_span(x.animate.set_color(YELLOW), 0.35 * i, 0.35 * i + 0.6)
                        for i, x in enumerate(xs)],
                      run_time=0.35 * (len(xs) - 1) + 0.6)
            xh = ux(0.4)
            gfirst = Line(M(xh, YD + 0.5), M(xh, Y_C - 0.45)).set_stroke(YELLOW, 2.5)
            c.wait_until("several times")
            self.play(Create(gfirst),
                      *[x.animate.set_color(BLUE) for x in xs[1:]], run_time=1.4)

            first_tag = set_backstroke(T("first change", 30, YELLOW))
            first_tag.move_to(M(xh, -0.45) + 0.15 * RIGHT, aligned_edge=LEFT)
            c.wait_until(own_word=first_tag)
            self.play(*appear(first_tag))
            tpd_new = dim_arrow(XQ, xh, Y_A, PURPLE, "t_{pd}", label_dir=DOWN)
            tpd_new.scale(K, about_point=ORIGIN).shift([SX_FOCUS, SY, 0])
            c.wait_until("logic's delay")
            self.play(restyle(dg.tpd, op=0), GrowFromCenter(tpd_new[0]), *appear(tpd_new[1]),
                      run_time=1.4)                     # ch1's long t_pd steps aside for the new one

            c.wait_until("earliest")
            brace = span_brace(M(E1, Y_C), M(xh, Y_C), color=FG)
            blab = MathTex("(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", font_size=40)
            blab[1].set_color(PINK)
            blab[3].set_color(PURPLE)
            blab.next_to(brace, RIGHT, buff=0.25)
            self.play(GrowFromCenter(brace), run_time=1.2)
            c.wait_until("plus the logic's")
            self.play(*appear(blab, shift=None))

        # ----------------------------------------------------------- c2.hold.3
        with self.say("c2.hold.3") as c:
            tick = check_mark(GREEN)
            fine = T("fine", 30, GREEN)
            fine_g = VGroup(tick, fine).arrange(RIGHT, buff=0.18)
            fine_g.next_to(first_tag, RIGHT, buff=0.4)
            self.play(xs[0].animate.set_color(BLUE), FlashAround(gfirst, color=YELLOW), run_time=1.2)
            c.wait_until(own_word=fine)
            self.play(*appear(fine_g, shift=None), run_time=1.0)

            bad_dg = hold_diagram(0.2)
            dy = K * (Y_GHOST - YD) * UP
            ghost = VGroup(bad_dg.d1, bad_dg.d1_lab).shift(dy + SX_FOCUS * RIGHT)
            ghost.set_stroke(opacity=0.6)
            ghost[1].set_opacity(0.6)
            gband = bad_dg.band.shift(dy + SX_FOCUS * RIGHT)
            c.wait_until("bad")
            self.play(*during(disappear(brace, blab), 0, 0.45),      # clear the row for the ghost
                      *during([FadeIn(ghost, shift=0.4 * UP), FadeIn(gband, shift=0.4 * UP)], 0.4, 1),
                      run_time=min(2.0, c.until("that's bad")))

            ov = Rectangle(width=K * (ux(HOLD_END) - ux(0.2)), height=K * (ROW_H + 0.16))
            ov.set_stroke(RED, 3).set_fill(RED, 0.45).move_to(M((ux(0.2) + ux(HOLD_END)) / 2, Y_GHOST))
            bad = VGroup(cross_mark(RED), T("bad", 32, RED)).arrange(RIGHT, buff=0.2)
            bad.move_to(M(HATCH_END, Y_GHOST) + 0.35 * RIGHT, aligned_edge=LEFT)
            c.wait_until("that's bad")
            self.play(FadeIn(ov), FlashAround(ov, color=RED), *appear(bad, shift=None), run_time=1.4)

            q = set_backstroke(T("?", 52, RED, weight=BOLD)).move_to(M((E1 + ux(0.2)) / 2, Y_GHOST))
            c.wait_until("wrong")
            self.play(*appear(q), run_time=1.0)

        # ----------------------------------------------------------- c2.hold.4
        with self.say("c2.hold.4") as c:
            ineq = MathTex("(", "t_{pc}", "+", "t_{pd}", ")", r"_{\min}", r"\ge", r"t_{hold}",
                           font_size=48)
            ineq[1].set_color(PINK)
            ineq[3].set_color(PURPLE)
            ineq[7].set_color(GOLD)
            ineq.move_to(M(-2.1, Y_GHOST))
            self.play(*during(disappear(ghost, gband, ov, bad, q, fine_g), 0, 0.45),
                      *during(appear(ineq, shift=None), 0.5, 1), run_time=2.0)

            c.wait_until("min")
            mn = ineq[5]
            join = Line(mn.get_top() + 0.08 * UP, gfirst.get_end()).set_stroke(YELLOW, 2)
            self.play(*recolor(mn, YELLOW), FlashAround(mn, color=YELLOW), Create(join),
                      run_time=1.5)

            su_tag = T("set-up:\narrive early enough", 30, GOLD)
            su_tag.move_to(M((XSU + E2) / 2, -4.2), aligned_edge=UP)
            c.wait_until("early")
            self.play(*set_alpha([dg.tsu, dg.gsu, dg.g2], 1), *appear(su_tag, shift=None), run_time=1.2)
            hd_tag = T("hold:\narrive late enough", 30, GOLD)
            hd_tag.next_to(thold[1], LEFT, buff=0.35)
            c.wait_until("Hold needs")
            self.play(*appear(hd_tag), FlashAround(thold, color=GOLD), run_time=1.2)

        self.wait(3.5)                                                  # let the two tags be read
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
