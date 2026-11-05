"""Chapter 5, scene 6: Example 36, completing the square to find an ellipse's centre and semi-axes,
then sketching it. Clips c5.example.1 – c5.example.5.

Layout: clip 1 the Example 36 card across the top, the factored line below it. Clip 2 the
lecturer's completed-square line built piece by piece under it (the RED -1 slip, the x2 arrow,
the GREEN -2). Clip 3 the board scrolls: each new form derived from the line above. Clip 4 the
tucked form on top, the general form under it, the read-off lines below. Clip 5 the read-offs
compact on the left, the sketch (example36_sketch, shared with ch5_s8 and ch6_s5) on the right.
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
from lib.style import *  # noqa: E402,F403

EQ_TEX = r"2x^2+4x+y^2-6y+7=0"
FULL_TEX = r"2(x^2+2x+1)-2+(y^2-6y+9)-9+7=0"
DIV_TEX = r"\frac{(x+1)^2}{2}+\frac{(y-3)^2}{4}=1"
TUCK_TEX = r"\left(\frac{x+1}{\sqrt{2}}\right)^2+\left(\frac{y-3}{2}\right)^2=1"
GEN_TEX = r"\left(\frac{x-x_0}{a}\right)^2+\left(\frac{y-y_0}{b}\right)^2=1"
R2 = np.sqrt(2)


def example36_sketch(unit=1.05, center=ORIGIN):
    """The Example 36 sketch: axes, YELLOW centre (-1, 3) with dashes to the axes, GOLD arms +-2
    (y = 1 to 5), GREEN arms +-sqrt2, the tall BLUE ellipse, and its y-axis crossings.
    Parts: .ax .axis_labels .centre .centre_label .dashes .gold .gold_labels .green .green_labels
    .ellipse .cross_pts .poke_label. The axes are centred on `center`."""
    ax = Axes(x_range=[-3, 1.5, 1], y_range=[-0.5, 5.5, 1], x_length=4.5 * unit, y_length=6 * unit,
              tips=False, axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": True,
                                       "tick_size": 0.06})
    ax.move_to(center)
    xl = MathTex("x", font_size=36, color=DIM).next_to(ax.x_axis.get_right(), RIGHT, buff=0.15)
    yl = MathTex("y", font_size=36, color=DIM).next_to(ax.y_axis.get_top(), UP, buff=0.12)
    c = ax.c2p(-1, 3)
    centre = Dot(c, radius=0.09, color=YELLOW).set_z_index(3)
    centre_label = MathTex(r"(-1,\,3)", font_size=34, color=YELLOW)
    centre_label.next_to(c, DL, buff=0.12)
    dashes = VGroup(DashedLine(c, ax.c2p(-1, 0), dash_length=0.12).set_stroke(YELLOW, 2.5, opacity=0.7),
                    DashedLine(c, ax.c2p(0, 3), dash_length=0.12).set_stroke(YELLOW, 2.5, opacity=0.7))
    gold = VGroup(Line(ax.c2p(-1, 1), ax.c2p(-1, 5)).set_stroke(GOLD, 6),
                  Dot(ax.c2p(-1, 5), radius=0.08, color=GOLD), Dot(ax.c2p(-1, 1), radius=0.08, color=GOLD))
    gold.set_z_index(2)
    gold_labels = VGroup(MathTex("y=5", font_size=32, color=GOLD).next_to(ax.c2p(-1, 5), LEFT, buff=0.6),
                         MathTex("y=1", font_size=32, color=GOLD).next_to(ax.c2p(-1, 1), LEFT, buff=0.6))
    green = VGroup(Line(ax.c2p(-1 - R2, 3), ax.c2p(-1 + R2, 3)).set_stroke(GREEN, 6),
                   Dot(ax.c2p(-1 - R2, 3), radius=0.08, color=GREEN),
                   Dot(ax.c2p(-1 + R2, 3), radius=0.08, color=GREEN))
    green.set_z_index(2)
    green_labels = VGroup(
        MathTex(r"\sqrt{2}", font_size=32, color=GREEN).next_to(ax.c2p(-1 - R2 / 2, 3), UP, buff=0.12),
        MathTex(r"\sqrt{2}", font_size=32, color=GREEN).next_to(ax.c2p(-1 + R2 / 2 - 0.12, 3), UP, buff=0.12))
    for m in [*gold_labels, *green_labels, centre_label]:
        set_backstroke(m)
    ts = np.linspace(0, TAU, 200)
    ellipse = VMobject().set_points_smoothly([ax.c2p(-1 + R2 * np.cos(t), 3 + 2 * np.sin(t)) for t in ts])
    ellipse.set_stroke(BLUE, 5).set_fill(opacity=0)
    cross_pts = VGroup(Dot(ax.c2p(0, 3 - R2), radius=0.08, color=YELLOW),
                       Dot(ax.c2p(0, 3 + R2), radius=0.08, color=YELLOW)).set_z_index(3)
    poke_label = MathTex(r"x\approx 0.41", font_size=32, color=GREEN)
    poke_label.next_to(ax.c2p(-1 + R2, 3), RIGHT, buff=0.2)
    set_backstroke(poke_label)
    g = VGroup(ax, VGroup(xl, yl), dashes, ellipse, gold, green, centre, centre_label, gold_labels,
               green_labels, cross_pts, poke_label)
    g.ax, g.axis_labels, g.dashes, g.ellipse = ax, VGroup(xl, yl), dashes, ellipse
    g.gold, g.green, g.centre, g.centre_label = gold, green, centre, centre_label
    g.gold_labels, g.green_labels, g.cross_pts, g.poke_label = gold_labels, green_labels, cross_pts, poke_label
    return g


def glyphs(m, *idx):
    return [m[0][i] for i in idx]


def pulse(glyphs_, run_time, color=YELLOW):
    """A colour pulse: each glyph goes to `color` and back (one animation per glyph)."""
    return [g.animate(rate_func=there_and_back, run_time=run_time).set_color(color) for g in glyphs_]


class Example36(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c5.example.1
    def clip1(self):
        with self.say("c5.example.1") as c:
            eq = MathTex(EQ_TEX, font_size=56)
            self.play(*appear(eq, shift=None), run_time=1.0)
            c.wait_until("example thirty-six")

            title = T("Example 36: Properties of an ellipse", 38, weight=BOLD)
            body = T("Find the centre and the semi-axes of the ellipse given by", 30)
            title.move_to([-5.4, 3.3, 0], aligned_edge=LEFT)
            body.move_to([-5.4, 2.6, 0], aligned_edge=LEFT)
            eq.generate_target()
            eq.target.scale(48 / 56).move_to([0, 1.8, 0])
            box = RoundedRectangle(corner_radius=0.15, width=11.6, height=2.5,
                                   stroke_color=GREEN, stroke_width=3).move_to([0, 2.5, 0])
            self.play(FadeIn(box), *appear(title), MoveToTarget(eq), run_time=1.5)
            c.wait_until("task")
            self.play(*appear(body), run_time=1.0)
            c.wait_until("first")
            self.play(FlashAround(VGroup(*glyphs(eq, 0, 1, 2)), time_width=1.5),
                      *recolor(glyphs(eq, 0), YELLOW), run_time=1.5)
            c.wait_until("factor")
            self.play(*flash([VGroup(*glyphs(eq, 0, 1, 2)), VGroup(*glyphs(eq, 4, 5))], time_width=1.5),
                      run_time=1.5)
            c.wait_until("becomes")
            row1 = MathTex(r"2(x^2+2x)+y^2-6y+7=0", font_size=48).move_to([0, 0.35, 0])
            row1[0][0].set_color(YELLOW)
            derive(self, eq, row1, run_time=2.0)
            self.card = [box, title, body, eq]
            self.row1 = row1

    # ------------------------------------------------------------ c5.example.2
    def clip2(self):
        with self.say("c5.example.2") as c:
            full = MathTex(FULL_TEX, font_size=48).move_to([0, -1.25, 0])
            full[0][0].set_color(YELLOW)
            A = VGroup(*glyphs(full, *range(0, 10)))
            B = VGroup(*glyphs(full, 10, 11)).set_color(GREEN)
            C = VGroup(*glyphs(full, *range(12, 22)))
            D = VGroup(*glyphs(full, 22, 23))
            E = VGroup(*glyphs(full, 24, 25, 26, 27))
            self.play(*appear(A, shift=None), run_time=1.2)
            c.wait_until("add one")
            self.play(FlashAround(VGroup(*glyphs(full, 7, 8)), time_width=1.5), run_time=1.3)

            c.wait_until("slip")
            ghost = MathTex("-1", font_size=48, color=RED).move_to(B)
            self.play(*appear(ghost), run_time=1.0)

            c.wait_until("times")
            one, two = full[0][8], full[0][0]
            arrow = CurvedArrow(one.get_bottom() + 0.15 * DOWN, two.get_bottom() + 0.15 * DOWN,
                                angle=-1.1, color=YELLOW, stroke_width=4)
            times = MathTex(r"\times 2", font_size=40, color=YELLOW)
            times.next_to(arrow, DOWN, buff=0.12)
            self.play(*recolor(glyphs(full, 7, 8), YELLOW), Create(arrow), run_time=1.5)
            self.play(*appear(times), run_time=1.0)

            c.wait_until("sub")
            # FG strike over the RED ghost, so the -1 stays legible under it until the swap
            cross = Cross(ghost, stroke_color=FG, stroke_width=5, scale_factor=1.35).set_z_index(2)
            self.play(Create(cross), run_time=1.2)
            c.wait_until("not one")
            self.play(*swap(VGroup(ghost, cross), B), run_time=1.2)

            c.wait_until("yterms")
            self.play(*disappear(arrow, times), *recolor(glyphs(full, 7, 8), FG), run_time=1.0)
            c.wait_until("add its square")
            self.play(*appear(C, E, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("take nine away")
            self.play(*appear(D, shift=None), run_time=min(1.0, c.until(floor=0.5)))
            row2 = VGroup(A, B, C, D, E)
            settle(self, row2)
            self.row2 = row2
            self.full = full

    # ------------------------------------------------------------ c5.example.3
    def clip3(self):
        row2, full = self.row2, self.full
        with self.say("c5.example.3") as c:
            sweep_clear(self, row2.animate.move_to([0, 2.4, 0]), keep=[row2], run_time=1.2)
            loose = [*glyphs(full, 10, 11, 22, 23, 24, 25)]
            note = MathTex("-2", "-9", "+7", "=", "-4", font_size=48, color=GOLD).move_to([0, 1.0, 0])
            self.play(*recolor(loose, GOLD), *appear(note, shift=0.3 * DOWN), run_time=1.5)

            c.wait_until("move")
            row3 = MathTex("2(x+1)^2", "+", "(y-3)^2", "=", "4", font_size=48).move_to([0, -0.6, 0])
            self.play(*fly(note[4][1], row3[4]), *appear(row3[3], shift=None), run_time=1.5)
            c.wait_until("sq")
            self.play(*appear(row3[0], row3[1], row3[2], lag=0.3, shift=None), run_time=1.5)
            settle(self, row3)

            c.wait_until("div")
            sweep_clear(self, row3.animate.move_to([0, 2.4, 0]), keep=[row3], run_time=1.0)
            row4 = MathTex(DIV_TEX, font_size=48).move_to([0, 0.6, 0])
            derive(self, row3, row4, run_time=min(2.0, c.until("tuck", floor=1.2)))

            c.wait_until("tuck")
            row5 = MathTex(TUCK_TEX, font_size=48).move_to([0, -1.4, 0])
            derive(self, row4, row5, run_time=2.0)
            c.wait_until("root two squared")
            rt = min(1.4, c.until("four is two squared", floor=0.8))
            self.play(*pulse(glyphs(row5, 5, 6, 7), rt), run_time=rt)
            c.wait_until("four is two squared")
            rt = min(1.2, c.until())
            self.play(*pulse(glyphs(row5, 16), rt), run_time=rt)
            self.row5 = row5

    # ------------------------------------------------------------ c5.example.4
    def clip4(self):
        row5 = self.row5
        with self.say("c5.example.4", gap=1.4) as c:
            sweep_clear(self, row5.animate.move_to([0, 2.5, 0]), keep=[row5], run_time=1.2)
            gen = MathTex(GEN_TEX, font_size=48).move_to([0, 0.75, 0])
            self.play(*appear(gen, shift=0.4 * UP), run_time=1.2)

            def row(math, words, y):
                math.move_to([-5.6, y, 0], aligned_edge=LEFT)
                for w, x in zip(words, (-1.6, 2.0)):
                    w.move_to([x, y, 0], aligned_edge=LEFT)
                return math

            c.wait_until("centre")
            cl = MathTex(r"x_0=-1,\quad y_0=3", font_size=44, color=YELLOW)
            cw = T("(centre)", 34, YELLOW)
            row(cl, [cw], -0.8)
            self.play(*recolor(glyphs(row5, 2, 3, 13, 14) + glyphs(gen, 3, 4, 13, 14), YELLOW),
                      *appear(cl, cw, lag=0.4), run_time=1.5)

            c.wait_until("a")
            al = MathTex(r"a=\sqrt{2}\approx 1.41", font_size=44, color=GREEN)
            aw = [T("semi-minor axis", 34, GREEN), T("in x-direction", 34, GREEN)]
            row(al, aw, -1.85)
            self.play(*recolor(glyphs(row5, 5, 6, 7) + glyphs(gen, 6), GREEN), *appear(al), run_time=1.5)
            c.wait_until("minor", own_word=aw[0])
            self.play(*appear(*aw, lag=0.4), run_time=1.2)

            c.wait_until("b")
            bl = MathTex(r"b=2", font_size=44, color=GOLD)
            bw = [T("semi-major axis", 34, GOLD), T("in y-direction", 34, GOLD)]
            row(bl, bw, -2.9)
            self.play(*recolor(glyphs(row5, 16) + glyphs(gen, 16), GOLD),
                      *appear(bl, *bw, lag=0.2), run_time=1.0)
            self.read = dict(gen=gen, cl=cl, al=al, bl=bl, words=[cw, *aw, *bw])

    # ------------------------------------------------------------ c5.example.5
    def clip5(self):
        row5, r = self.row5, self.read
        with self.say("c5.example.5") as c:
            sk = example36_sketch(unit=1.05, center=[3.6, -0.2, 0])
            moves = [row5.animate.scale(0.8).move_to([-3.7, 2.2, 0])]
            for m, y in ((r["cl"], 0.7), (r["al"], -0.5), (r["bl"], -1.7)):
                moves.append(m.animate.move_to([-6.0, y, 0], aligned_edge=LEFT))
            self.play(*during(disappear(r["gen"], *r["words"]), 0, 0.45),
                      *during(moves, 0.2, 0.8),
                      *during([FadeIn(sk.ax), FadeIn(sk.axis_labels)], 0.5, 1), run_time=1.6)
            c.wait_until("mark the centre")
            self.play(GrowFromCenter(sk.centre), *[Create(d) for d in sk.dashes], run_time=1.2)
            c.wait_until("minus one three")
            self.play(*appear(sk.centre_label), run_time=1.0)

            c.wait_until("updown")
            self.play(GrowFromCenter(sk.gold[0]), *[GrowFromCenter(d) for d in sk.gold[1:]], run_time=1.5)
            c.wait_until("from why equals one")
            self.play(*appear(sk.gold_labels[1], sk.gold_labels[0], lag=0.5), run_time=1.5)

            c.wait_until("side")
            self.play(GrowFromCenter(sk.green[0]), *[GrowFromCenter(d) for d in sk.green[1:]],
                      *appear(*sk.green_labels, shift=None), run_time=1.5)

            c.wait_until("cross")
            self.play(Create(sk.ellipse), run_time=2.0)
            c.wait_until("pokes across")
            self.play(*[GrowFromCenter(d) for d in sk.cross_pts], *flash(list(sk.cross_pts), time_width=1.5),
                      run_time=1.5)
            c.wait_until("zero point four one")
            self.play(*appear(sk.poke_label), run_time=1.0)

            c.wait_until("tall")
            self.play(VShowPassingFlash(sk.ellipse.copy().set_stroke(YELLOW, 8), time_width=0.4),
                      run_time=2.0)
