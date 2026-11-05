"""Chapter 3, scene 7: recap in six panels, then a look ahead to cos z = 2 (end card).
Clips c3.recap.1 – c3.recap.3.

Panels (3 x 2, ch2_s7_recap's DIM rounded frames), each a miniature built with the builders of the
scene that taught it, on its mark, while the previous one dims: r1 s2's Figure 25(a); r2 s3/s4's
Figure 25(d) with the dashed GOLD/PURPLE tanh band; r3 s4's boxed quadratic in e^y; r4 s4's sinh /
sinh^-1 mirror pair + (96); r5 s5's Figure 26 + (97); r6 s6's tanh / tanh^-1 pair + Example 34.
r7: all restored, the three \\ln glow YELLOW. Then the board clears to cos_z2_shot(); end card ~8 s.

Shared (load_scene("ch3_s7_recap")):
  cos_z2_shot()  ch4 s1's opening shot: DIM axes over [-3pi, 3pi] (12 x 4, centred at (0, 0.9), as ch4_s1_hook.wave_shot()),
                 BLUE y = cos x with label, the faint BLUE +-1 band (DIM dashed edges, "1"/"-1"),
                 the solid YELLOW y = 2 line with label, and YELLOW \\cos z = 2 at (-3.6, -2.4).
                 Attributes .ax .wave .wave_label .band .line .line_label .eq.
"""
# style: 2
import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

C1 = load_scene("ch1_s2_define")
G3 = load_scene("ch7_s4_g3")
S2 = load_scene("ch3_s2_cosh")
S4 = load_scene("ch3_s4_arsinh")
S5 = load_scene("ch3_s5_arcosh")

SINH_C, TANH_C, INV_C = S4.SINH_C, S4.TANH_C, G3.INV_C
mt = S4.mt

# ---------------------------------------------------------------- the grid
PW, PH = 4.25, 3.15
XS = (-4.42, 0.0, 4.42)
YS = (2.1, -1.3)
CENTRES = [np.array([x, y, 0]) for y in YS for x in XS]
FADED = 0.4
LSZ = 34                                   # panel lines (MathTex)
TEXT_W = 3.8


def frame_at(k):
    return RoundedRectangle(corner_radius=0.15, width=PW, height=PH).set_stroke(DIM, 2).move_to(CENTRES[k])


def line(src, color=FG, size=LSZ):
    m = MathTex(src, font_size=size, color=color)
    if m.width > TEXT_W:
        m.scale_to_fit_width(TEXT_W)
    return m


def place(k, *parts, buff=0.2):
    g = VGroup(*parts).arrange(DOWN, buff=buff)
    g.move_to(CENTRES[k])
    return g


def tag_for(pic, text, size=28):
    """The result's tag ((96), (97), Example 34), left of the picture, level with its top."""
    t = T(text, size, DIM)
    t.next_to(pic, LEFT, buff=0.25, aligned_edge=UP)
    return t


def inv_formula(name, color, mid, rest, size=34):
    """s4-s6's boxed results, panel size: name coloured, \\ln isolated as part 2."""
    m = MathTex(name, mid, r"\ln", rest, font_size=size)
    m[0].set_color(color)
    if m.width > TEXT_W - 0.25:
        m.scale_to_fit_width(TEXT_W - 0.25)
    box = SurroundingRectangle(m, buff=0.12).set_stroke(YELLOW, 2.5)
    g = VGroup(m, box)
    g.tex, g.box, g.ln = m, box, m[2]
    return g


def small_axes(center, h=1.9):
    ax = S2.fig_axes()
    ax.scale(h / ax.height).move_to(center)
    return ax


def fig26_mini(center, u=0.19, width=4, gap=0.4):
    """s5's Figure 26 (fig26()) at unit u, no ticks, the two halves `gap` apart:
    cosh with the mirror, and its two-branch inverse."""
    lax = G3.eq_axes((-3, 3), (0, 10), u, ORIGIN, ticks=False)
    rax = G3.eq_axes((0, 10), (-3, 3), u, ORIGIN, ticks=False)
    lax.shift(-gap / 2 - lax.get_right()[0] * RIGHT)
    rax.shift(gap / 2 - rax.get_left()[0] * RIGHT)
    VGroup(lax, rax).move_to(center)
    a10 = S5.ACOSH10
    ch = G3.fcurve(lax, math.cosh, -a10, a10, TEAL, width)
    mirror = G3.mirror_line(lax, 0, 3)
    up = G3.pcurve(rax, math.cosh, lambda t: t, 0, a10, INV_C, width)
    lo = G3.pcurve(rax, math.cosh, lambda t: t, -a10, 0, PURPLE, width)
    dot = G3.kdot(rax, 1, 0, r=0.06)
    g = VGroup(lax, mirror, ch, rax, lo, up, dot)
    g.lax, g.rax, g.cosh, g.mirror, g.upper, g.lower, g.dot = lax, rax, ch, mirror, up, lo, dot
    return g


def branches_mini(center, u=0.2, width=4):
    """Just Figure 26's right half: the two branches of cosh^-1."""
    rax = G3.eq_axes((0, 10), (-3, 3), u, center)
    a10 = S5.ACOSH10
    up = G3.pcurve(rax, math.cosh, lambda t: t, 0, a10, INV_C, width)
    lo = G3.pcurve(rax, math.cosh, lambda t: t, -a10, 0, PURPLE, width)
    dot = G3.kdot(rax, 1, 0, r=0.06)
    g = VGroup(rax, lo, up, dot)
    g.ax, g.upper, g.lower, g.dot = rax, up, lo, dot
    return g


# ---------------------------------------------------------------- ch4 s1's opening shot
WAVE_C = np.array([0.0, 0.9, 0])           # ch4_s1_hook.WAVE_CENTER
EQ_POS = np.array([-3.3, -2.3, 0])


def cos_z2_shot():
    ax = Axes(x_range=[-3 * PI, 3 * PI, PI], y_range=[-1.5, 2.5, 1], x_length=12, y_length=4, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06})
    ax.move_to(WAVE_C)
    wave = ax.plot(math.cos, x_range=[-3 * PI, 3 * PI, 0.02], color=BLUE, stroke_width=5)
    wave_label = MathTex(r"y = \cos x", font_size=40, color=BLUE).move_to(ax.c2p(-PI, 0.45))
    x0, x1 = -3 * PI, 3 * PI
    fill = Rectangle(width=ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1])
    fill.set_stroke(width=0).set_fill(BLUE, 0.08).move_to(ax.c2p(0, 0)).set_z_index(-2)
    up = DashedLine(ax.c2p(x0, 1), ax.c2p(x1, 1), dash_length=0.12, color=DIM, stroke_width=2)
    lo = DashedLine(ax.c2p(x0, -1), ax.c2p(x1, -1), dash_length=0.12, color=DIM, stroke_width=2)
    one = MathTex("1", font_size=30, color=DIM).next_to(up, LEFT, buff=0.15)
    mone = MathTex("-1", font_size=30, color=DIM).next_to(lo, LEFT, buff=0.15)
    band = VGroup(fill, up, lo, one, mone)
    band.fill, band.up, band.lo, band.one, band.mone = fill, up, lo, one, mone
    ln = Line(ax.c2p(x0, 2), ax.c2p(x1, 2), color=YELLOW, stroke_width=5)
    ln_label = MathTex(r"y = 2", font_size=40, color=YELLOW).next_to(ax.c2p(x1, 2), UP, buff=0.15)
    ln_label.align_to(ln, RIGHT)
    eq = MathTex(r"\cos z = 2", font_size=60, color=YELLOW).move_to(EQ_POS)
    g = VGroup(ax, band, wave, wave_label, ln, ln_label, eq)
    g.ax, g.wave, g.wave_label, g.band, g.line, g.line_label, g.eq = ax, wave, wave_label, band, ln, ln_label, eq
    return g


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)                       # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ------------------------------------------------------------ c3.recap.1
    def clip1(self):
        frames = [frame_at(k) for k in range(6)]
        self.frames = frames
        with self.say("c3.recap.1") as c:
            # the whole shape first: six empty panels
            self.play(LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.15),
                      run_time=min(1.5, c.until("r1")))
            c.wait_until("r1")

            # ---- r1: Figure 25(a)
            ax = small_axes(ORIGIN)
            hexp, hemx = S2.half_exp_curve(ax, width=3), S2.half_emx_curve(ax, width=3)
            ch = S2.cosh_curve(ax, width=4)
            dot = Dot(ax.c2p(0, 1), radius=0.08, color=YELLOW).set_z_index(3)
            pic1 = VGroup(ax, hexp, hemx, ch, dot)
            ln1 = line(r"\cosh x \ge 1,\ \text{hugs } \tfrac12 e^{x}")
            for g in ln1[0][0:4]:
                g.set_color(TEAL)
            for g in ln1[0][-5:]:
                g.set_color(GOLD)
            place(0, pic1, ln1)
            self.play(FadeIn(ax), Create(ch), FadeIn(dot, scale=0.5), run_time=min(1.4, c.until("at least")))
            c.wait_until("at least")
            self.play(*appear(ln1), run_time=1.0)
            c.wait_until("hugging")
            self.play(FadeIn(hexp), FadeIn(hemx), FlashAround(ln1[0][-5:], time_width=1.5),
                      run_time=min(1.3, c.until("r2")))
            panel1 = VGroup(ax, hexp, hemx, ch, dot, ln1)
            settle(self, panel1)

            # ---- r2: Figure 25(d) and the tanh band
            c.wait_until("r2")
            ax2 = small_axes(ORIGIN)
            ch2 = S2.cosh_curve(ax2, width=4)
            sh2 = C1.sinh_curve(ax2, width=4)
            th2 = C1._plot(ax2, math.tanh, C1.X_LO, C1.X_HI, TANH_C, 4)
            bp = G3.dline(ax2, (-2.5, 1), (2.5, 1), GOLD, 2.5)
            bm = G3.dline(ax2, (-2.5, -1), (2.5, -1), PURPLE, 2.5)
            ln2a = line(r"\sinh,\ \tanh\ \text{odd, increasing}")
            for g in list(ln2a[0][0:4]) + list(ln2a[0][5:9]):
                g.set_color(TEAL)
            ln2b = line(r"-1 < \tanh x < 1")
            for g in ln2b[0][3:7]:
                g.set_color(TANH_C)
            for g in ln2b[0][0:2]:
                g.set_color(PURPLE)
            ln2b[0][-1].set_color(GOLD)
            pic2 = VGroup(ax2, ch2, sh2, th2, bp, bm)
            place(1, pic2, ln2a, ln2b, buff=0.14)
            self.play(*set_alpha([panel1], FADED), FadeIn(ax2), Create(ch2), Create(sh2), Create(th2),
                      run_time=min(1.4, c.until("odd")))
            c.wait_until("odd")
            self.play(*appear(ln2a), run_time=1.0)
            c.wait_until("trapped")
            self.play(Create(bp), Create(bm), *during(appear(ln2b, shift=None), 0.3, 1.0), run_time=min(1.4, c.until("r3")))
            panel2 = VGroup(ax2, ch2, sh2, th2, bp, bm, ln2a, ln2b)
            settle(self, panel2)

            # ---- r3: the quadratic in e^y
            c.wait_until("r3")
            tm = S4.times2(40)
            q = S4.l3q(40)
            if q.width > TEXT_W:
                q.scale_to_fit_width(TEXT_W)
            qlab = line(r"\text{a quadratic in } e^{y}", YELLOW, 36)
            place(2, tm, q, qlab, buff=0.4)
            boxes = [SurroundingRectangle(VGroup(*q[0][a:b]), buff=0.06).set_stroke(YELLOW, 2.5)
                     for a, b in ((0, 4), (8, 12))]
            self.play(*set_alpha([panel2], FADED), *appear(q), run_time=min(1.2, c.until("multiply")))
            c.wait_until("multiply")
            self.play(*appear(tm), run_time=1.0)
            c.wait_until("find")
            self.play(*[FadeIn(b) for b in boxes], *appear(qlab), run_time=1.2)
            panel3 = VGroup(tm, q, *boxes, qlab)
            settle(self, panel3)
        self.panels = [panel1, panel2, panel3]

    # ------------------------------------------------------------ c3.recap.2
    def clip2(self):
        with self.say("c3.recap.2") as c:
            # ---- r4: sinh and its mirror image
            ax = G3.eq_axes((-4, 4), (-4, 4), 0.23, ORIGIN, ticks=False)
            sh = G3.fcurve(ax, math.sinh, -S4.S4, S4.S4, TEAL, 4)
            mirror = G3.mirror_line(ax, -4, 4)
            ash = G3.pcurve(ax, math.sinh, lambda t: t, -S4.S4, S4.S4, INV_C, 4)
            f96 = inv_formula(r"\sinh^{-1}", SINH_C, r"x =", r"\left(x + \sqrt{x^2 + 1}\right)")
            pic4 = VGroup(ax, sh, mirror, ash)
            t96 = tag_for(pic4, "(96)")
            place(3, VGroup(t96, pic4), f96, buff=0.25)
            self.play(*set_alpha([self.panels[2]], FADED), FadeIn(ax), Create(sh), Create(mirror),
                      run_time=min(1.2, c.until("log of")))
            cp = sh.copy()
            self.play(G3.flip(cp, ax), run_time=1.3)
            self.remove(cp)
            self.add(ash)
            c.wait_until("log of")
            self.play(*appear(f96.tex), FadeIn(f96.box), *appear(t96), run_time=1.2)
            panel4 = VGroup(ax, sh, mirror, ash, f96, t96)
            settle(self, panel4)

            # ---- r5: Figure 26
            c.wait_until("r5")
            fig = fig26_mini(ORIGIN, u=0.14, gap=0.45)
            f97 = inv_formula(r"\cosh^{-1}", TEAL, r"x =", r"\left(x + \sqrt{x^2 - 1}\right)")
            ln5 = line(r"\text{keep the plus}", FG, 36)
            for g in ln5[0][-4:]:
                g.set_color(GREEN)
            pm_p = MathTex("+", font_size=40, color=GREEN)
            pm_m = MathTex("-", font_size=40, color=PURPLE)
            pm_p.next_to(fig.rax.c2p(10, 3), RIGHT, buff=0.12)
            pm_m.next_to(fig.rax.c2p(10, -3), RIGHT, buff=0.12)
            pic5 = VGroup(fig, pm_p, pm_m)
            t97 = tag_for(pic5, "(97)").shift(0.12 * LEFT + 0.3 * DOWN)   # clear of the U's left arm
            place(4, VGroup(t97, pic5), f97, ln5, buff=0.18)
            self.play(*set_alpha([panel4], FADED), FadeIn(fig.lax), Create(fig.cosh), Create(fig.mirror),
                      FadeIn(fig.rax), run_time=min(1.2, c.until("two branches")))
            c.wait_until("two branches")
            self.play(Create(fig.upper), Create(fig.lower), FadeIn(fig.dot), run_time=1.2)
            c.wait_until("plus or minus")
            self.play(*appear(pm_p, pm_m, lag=0.3, shift=None), run_time=0.8)
            self.play(*appear(f97.tex), FadeIn(f97.box), *appear(t97), run_time=1.0)
            c.wait_until("keep")
            self.play(*appear(ln5), VShowPassingFlash(fig.upper.copy().set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=min(1.2, c.until("r6")))
            panel5 = VGroup(fig, pm_p, pm_m, f97, t97, ln5)
            settle(self, panel5)

            # ---- r6: tanh and tanh^-1 with their asymptotes
            c.wait_until("r6")
            P = G3.tanh_panel(unit=0.3, center=ORIGIN)
            for m in (P.tanh, P.atanh):
                m.set_stroke(width=4)
            f34 = inv_formula(r"\tanh^{-1}", TANH_C, r"x = \tfrac12", r"\left[\dfrac{1 + x}{1 - x}\right]")
            t34 = VGroup(T("Example", 28, DIM), T("34", 28, DIM)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            t34.next_to(P, LEFT, buff=0.2, aligned_edge=UP)
            place(5, VGroup(t34, P), f34, buff=0.2)
            self.play(*set_alpha([panel5], FADED), FadeIn(P.ax), Create(P.mirror), Create(P.tanh),
                      Create(P.atanh), run_time=min(1.3, c.until("half the log")))
            c.wait_until("half the log")
            self.play(*appear(f34.tex), FadeIn(f34.box), *appear(t34), run_time=1.0)
            c.wait_until("between")
            self.play(Create(P.vp), Create(P.vm), run_time=1.2)
            panel6 = VGroup(P, f34, t34)
            settle(self, panel6)

            # ---- r7: all three are logs
            c.wait_until("r7")
            panels = self.panels + [panel4, panel5, panel6]
            self.panels = panels
            lns = [f96.ln, f97.ln, f34.ln]
            logs = T("all three inverses are logs", 36, YELLOW).move_to([0, -3.35, 0])
            self.play(*set_alpha(panels, 1), *appear(logs), run_time=1.0)
            self.play(*[FlashAround(l, time_width=1.5) for l in lns],
                      *[a for l in lns for a in recolor(list(l), YELLOW)], run_time=1.4)
            self.logs = logs

    # ------------------------------------------------------------ c3.recap.3: next time
    def clip3(self):
        W = cos_z2_shot()
        title = T("Next time", 44, DIM).to_corner(UL, buff=0.6)
        gap = DoubleArrow(W.ax.c2p(2 * PI, 1), W.ax.c2p(2 * PI, 2), buff=0.06, color=YELLOW, stroke_width=3,
                          tip_length=0.16, max_tip_length_to_length_ratio=0.5)
        arrow = Arrow(LEFT, RIGHT, buff=0, stroke_width=4, color=DIM).scale(0.45)
        sol = MathTex(r"\pm\cosh^{-1} 2", font_size=60, color=TEAL)
        mini = branches_mini(ORIGIN)
        arrow.next_to(W.eq, RIGHT, buff=0.35)
        sol.next_to(arrow, RIGHT, buff=0.35)
        mini.next_to(sol, RIGHT, buff=0.6)
        with self.say("c3.recap.3") as c:
            sweep_clear(self, FadeIn(W.ax), Create(W.wave), FadeIn(W.band), *appear(title),  # early: section title
                        run_time=1.6)
            self.play(*appear(W.wave_label, shift=None), run_time=0.8)
            c.wait_until("cosine is two")
            self.play(Create(W.line), *appear(W.line_label, W.eq, lag=0.3), run_time=1.2)
            c.wait_until("No real")
            self.play(FadeIn(gap), run_time=1.0)                     # whole: no lone tips
            c.wait_until("cosh2")
            self.play(GrowArrow(arrow), *during(appear(sol), 0.3, 1.0), run_time=1.2)
            c.wait_until("comes from")
            self.play(FadeIn(mini.ax), Create(mini.upper), Create(mini.lower), FadeIn(mini.dot), run_time=1.2)
            c.wait_until("both")
            self.play(VShowPassingFlash(mini.upper.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      VShowPassingFlash(mini.lower.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      FlashAround(sol, time_width=1.5), run_time=min(1.4, max(0.5, c.until())))
