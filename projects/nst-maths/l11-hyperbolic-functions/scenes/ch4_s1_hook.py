"""Chapter 4, scene 1: hook: cos x = 2 has no real solution, as x^2 + 1 = 0 had none. Clips c4.hook.1 – c4.hook.3.

Module-level builders (import with load_scene("ch4_s1_hook")):
- fig26(): ch3's Figure 26 inverse panel, built by ch3_s5_arcosh.fig26() (equal-unit axes x in [0, 10],
  y in [-3, 3], unit 0.6): upper branch INV_C, lower PURPLE, YELLOW dot at (1, 0), MathTex labels
  above / below. Centred at ORIGIN, 6 wide. Attributes .ax .upper .lower .dot .lab_up .lab_lo.
  F26_T is kept for ch4_s5_even (its label/dot heights).
- wave_shot(): the hook's wave: DIM axes over [-3pi, 3pi] (12 x 4, centred at (0, 0.9)), BLUE
  y = cos x with label, the dashed +-1 band (faint BLUE fill, DIM "1"/"-1"), the YELLOW y = 2 line
  with label, and a small YELLOW gap arrow between the crest at 2pi and the line.
  Attributes .ax .wave .wave_label .band (VGroup: fill, dash_up, dash_lo, one, mone) .line
  .line_label .gap (all in the group).
- handover_shot(): the last frame: YELLOW \\cos z = 2 over "z complex?"  "how many?", centred at ORIGIN.
"""
# style: 2
# handover: next
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
from lib.titles import title_card  # noqa: E402

AXIS_CFG = {"stroke_color": DIM, "stroke_width": 2, "include_ticks": True, "tick_size": 0.06}   # ch1_s2_define style
F26_T = math.acosh(4.0)                 # used by ch4_s5_even: the height of its labels at x = 4


def fig26():
    """ch3's Figure 26 right panel (ch3_s5_arcosh.fig26()), centred at ORIGIN."""
    full = load_scene("ch3_s5_arcosh").fig26()
    g = VGroup(full.rax, full.lower, full.upper, full.dot, full.ulab, full.llab)
    g.move_to(ORIGIN)
    g.ax, g.upper, g.lower, g.dot, g.lab_up, g.lab_lo = full.rax, full.upper, full.lower, full.dot, full.ulab, full.llab
    return g


WAVE_CENTER = np.array([0.0, 0.9, 0])


def wave_axes(x_range=(-3 * PI, 3 * PI, PI)):
    return Axes(x_range=list(x_range), y_range=[-1.5, 2.5, 1], x_length=12, y_length=4,
                tips=False, axis_config=AXIS_CFG).move_to(WAVE_CENTER)


def wave_shot():
    ax = wave_axes()
    wave = ax.plot(math.cos, x_range=[-3 * PI, 3 * PI, 0.02], color=BLUE, stroke_width=5)
    wave_label = MathTex(r"y = \cos x", font_size=40, color=BLUE)
    wave_label.move_to(ax.c2p(-PI, 0.45))
    x0, x1 = -3 * PI, 3 * PI
    fill = Rectangle(width=ax.c2p(x1, 0)[0] - ax.c2p(x0, 0)[0], height=ax.c2p(0, 1)[1] - ax.c2p(0, -1)[1])
    fill.set_stroke(width=0).set_fill(BLUE, 0.08).move_to(ax.c2p(0, 0)).set_z_index(-2)
    dash_up = DashedLine(ax.c2p(x0, 1), ax.c2p(x1, 1), dash_length=0.12, color=DIM, stroke_width=2)
    dash_lo = DashedLine(ax.c2p(x0, -1), ax.c2p(x1, -1), dash_length=0.12, color=DIM, stroke_width=2)
    one = MathTex("1", font_size=30, color=DIM).next_to(dash_up, LEFT, buff=0.15)
    mone = MathTex("-1", font_size=30, color=DIM).next_to(dash_lo, LEFT, buff=0.15)
    band = VGroup(fill, dash_up, dash_lo, one, mone)
    band.fill, band.dash_up, band.dash_lo, band.one, band.mone = fill, dash_up, dash_lo, one, mone
    line = Line(ax.c2p(x0, 2), ax.c2p(x1, 2), color=YELLOW, stroke_width=5)
    line_label = MathTex(r"y = 2", font_size=40, color=YELLOW).next_to(ax.c2p(x1, 2), UP, buff=0.15)
    line_label.align_to(line, RIGHT)
    gap = DoubleArrow(ax.c2p(2 * PI, 1), ax.c2p(2 * PI, 2), buff=0.06, color=YELLOW, stroke_width=3,
                      tip_length=0.16, max_tip_length_to_length_ratio=0.5)
    g = VGroup(ax, band, wave, wave_label, line, line_label, gap)
    g.ax, g.wave, g.wave_label, g.band, g.line, g.line_label, g.gap = ax, wave, wave_label, band, line, line_label, gap
    return g


def handover_shot():
    q = MathTex(r"\cos z = 2", font_size=72, color=YELLOW)
    sub = T("z complex?", 40, t2s={"z": ITALIC})
    many = T("how many?", 40)
    row = VGroup(sub, many).arrange(RIGHT, buff=1.0)
    g = VGroup(q, row).arrange(DOWN, buff=0.5).move_to(ORIGIN)
    g.q, g.sub, g.many = q, sub, many
    return g


BOTTOM_SCALE = 0.75
BOTTOM_POS = np.array([0, -2.55, 0])


class Hook(NarratedScene):
    def x_to_z(self, old, new):
        """cos x = 2 → cos z = 2: shared glyphs slide and recolour, x fades out while z fades in
        (overlapping, so the variable's slot is never empty)."""
        a, b = old[0], new[0]          # glyphs: c o s x = 2
        dz = b[3].get_center() - a[3].get_center()
        anims = [a[i].animate.move_to(b[i]).set_color(YELLOW) for i in (0, 1, 2, 4, 5)]
        anims.append(FadeOut(a[3], shift=dz))
        self.z_in = b[3].copy()
        anims.append(FadeIn(self.z_in, shift=dz))
        return anims

    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()

    # ---- c4.hook.1: title, then last time's sideways curve
    def clip1(self):
        with self.say("c4.hook.1") as c:
            card = title_card("Part 4 · Solving cos z = 2")
            if card.title.width > 12.6:
                card.title.scale_to_fit_width(12.6)
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.6),
                      time_span(FadeIn(card.course), 0.15, 0.75),
                      time_span(FadeIn(card.part), 0.3, 0.9), run_time=0.9)
            c.wait_until("last")

            fig = fig26().scale(1.2).move_to([0.3, -0.25, 0])
            last = T("Last time", 34, DIM).to_corner(UL, buff=0.6)
            self.fig, self.last = fig, last
            sweep_clear(self, *appear(last, fig.ax, lag=0.3), run_time=2.0)
            self.play(Create(fig.upper), Create(fig.lower), GrowFromCenter(fig.dot), run_time=1.5)
            self.play(*appear(fig.lab_up, fig.lab_lo, lag=0.3), run_time=1.2)
            c.wait_until("branches")
            self.play(VShowPassingFlash(fig.upper.copy().set_stroke(YELLOW, 10), time_width=0.6),
                      VShowPassingFlash(fig.lower.copy().set_stroke(YELLOW, 10), time_width=0.6),
                      *flash([fig.lab_up, fig.lab_lo], color=YELLOW, time_width=1.5), run_time=1.6)
            c.wait_until("You will need it")
            pic = VGroup(fig.ax, fig.upper, fig.lower, fig.dot)
            self.fig = pic
            self.play(*during(disappear(fig.lab_up, fig.lab_lo, last), 0, 0.5),
                      pic.animate.scale(0.3).to_corner(UL, buff=0.5).shift(0.6 * DOWN),
                      run_time=min(1.1, c.until()))

    # ---- c4.hook.2: the wave, its band, the line it never meets
    def clip2(self):
        W = self.W = wave_shot()
        with self.say("c4.hook.2") as c:
            self.play(FadeOut(self.fig), *appear(W.ax), run_time=0.8)
            self.play(Create(W.wave), run_time=min(1.5, c.until("band")))
            c.wait_until("band")
            self.play(FadeIn(W.band.fill), Create(W.band.dash_up), Create(W.band.dash_lo),
                      *appear(W.band.one, W.band.mone, W.wave_label, lag=0.2, shift=None),
                      run_time=min(1.6, c.until("line")))
            c.wait_until("line")
            start = UP * 2.2
            W.line.shift(start)
            W.line_label.shift(start)
            self.add(W.line, W.line_label)
            self.play(W.line.animate.shift(-start), W.line_label.animate.shift(-start),
                      run_time=1.8, rate_func=smooth)
            c.wait_until("never meets")
            self.play(GrowFromCenter(W.gap), run_time=1.0)

            self.ceq = MathTex(r"\cos x = 2", font_size=52, color=RED)
            self.cno = T("no real x", 36, t2s={"x": ITALIC})
            VGroup(self.ceq, self.cno).arrange(RIGHT, buff=0.5).move_to([0, -2.1, 0])
            self.cno.align_to(self.ceq, DOWN)
            c.wait_until("the equation")
            self.play(*appear(self.ceq), run_time=1.0)
            c.wait_until("no solution")
            self.play(*appear(self.cno), run_time=1.0)

    # ---- c4.hook.3: x^2 + 1 = 0, rescued by i; then the question
    def clip3(self):
        W = self.W
        ax2 = wave_axes((-3, 3, 1))
        r = math.sqrt(1.5)
        parab = ax2.plot(lambda x: x * x + 1, x_range=[-r, r, 0.01], color=FG, stroke_width=5)
        plab = MathTex(r"y = x^2 + 1", font_size=40, color=FG).next_to(ax2.c2p(r, 2.5), RIGHT, buff=0.3)
        plab.shift(0.25 * DOWN)
        left_block = VGroup(self.ceq, self.cno)

        sq = MathTex(r"x^2 + 1 = 0", font_size=52, color=RED)
        sqno = T("no real x", 36, t2s={"x": ITALIC})
        VGroup(sq, sqno).arrange(RIGHT, buff=0.5).move_to([3.4, -2.1, 0])
        sqno.align_to(sq, DOWN)
        roots = MathTex(r"x = \pm", r"i", font_size=52)
        roots[1].set_color(PINK)
        tick = check_mark(GREEN)
        VGroup(roots, tick).arrange(RIGHT, buff=0.4).next_to(sq, DOWN, buff=0.4).align_to(sq, LEFT)

        with self.say("c4.hook.3") as c:
            W.wave.save_state()
            W.ax.save_state()
            self.play(*during(disappear(W.band, W.line, W.line_label, W.gap, W.wave_label), 0, 0.4),
                      Transform(W.ax, ax2), Transform(W.wave, parab),
                      left_block.animate.shift(3.45 * LEFT).set_opacity(0.4),
                      *during(appear(plab), 0.6, 1.0),
                      run_time=min(1.8, c.until("sq")))
            c.wait_until("sq")
            self.play(*appear(sq), run_time=1.0)
            c.wait_until("real")
            self.play(*appear(sqno), run_time=1.0)
            c.wait_until("gave it")
            self.play(*appear(roots), run_time=1.2)
            self.play(Create(tick), run_time=0.8)

            # the question: the wave comes back under the line
            c.wait_until("ask")
            self.play(*during(disappear(plab), 0, 0.4),
                      Restore(W.ax), Restore(W.wave),
                      *during(appear(W.band, W.wave_label, shift=None), 0.5, 1.0),
                      *during(appear(W.line, W.line_label, shift=None), 0.5, 1.0),
                      left_block.animate.set_opacity(1),
                      run_time=1.3)
            q = self.q = handover_shot().scale(BOTTOM_SCALE).move_to(BOTTOM_POS)
            c.wait_until("zed")
            self.play(*during(disappear(self.cno, sq, sqno, roots, tick), 0, 0.35),
                      *during(self.x_to_z(self.ceq, q.q), 0.3, 1.0), run_time=1.5)
            self.remove(*self.ceq.get_family(), self.z_in)
            self.add(q.q)
            c.wait_until("complex solutions")
            self.play(*appear(q.sub), run_time=1.0)  # early: its word 'complex' is being said as it lands
            c.wait_until(own_word=q.many)
            self.play(*appear(q.many), run_time=1.0)
            c.wait_until()

        # closing pause: clear the wave and line, the question settles in the centre
        settle(self, q)
        self.play(*disappear(W.ax, W.wave, W.band, W.wave_label, W.line, W.line_label), run_time=0.9)
        self.play(q.animate.scale(1 / BOTTOM_SCALE).move_to(ORIGIN), run_time=1.2)
        self.wait(1.0)
