"""Chapter 4, scene 3: split z into x + iy. Clips c4.split.1 – c4.split.5.

Exports: `ex35_card(pos)` (the green Example 35 card; pos "centre" | "left" | "top"), `result_line()`
(cos z = cos x cosh y - i sin x sinh y, centred at Y_RES), `cosh_panel()` (the right-hand x = 0 check
panel: cosh curve TEAL over a y axis, YELLOW line at 2), `wave_panel()` (left-hand y = 0 panel).
Ends on `handover_shot()`: the card at the top + the result line; ch4_s4_cases opens on it.
"""
# style: 2
# handover: next
import math
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

S4 = load_scene("ch1_s4_cosix")
ctex, at_glyph, words_var, dictionary_card = S4.ctex, S4.at_glyph, S4.words_var, S4.dictionary_card

SZ = 60
XEQ = -3.2          # x of the working lines' "="
Y1, Y2 = 1.05, -0.4  # working lines
Y_ADD = -2.1        # the addition-formula card
Y_WORK = 0.3   # the result line while it is read (clips 3-4)
Y_RES = 1.55        # the result line (handover)
DOCK = 0.85         # card scale when docked

# ---------------------------------------------------------------- sources (tex, colour pattern)
SRC_Z = (r"z = x + iy, \quad x, y \in \mathbb{R}", "FFFFPFFFFFFF")
SRC_L1 = (r"\cos z = \cos(x + iy)", "BBBFF BBBFFFPFF")
SRC_L2 = (r"= \cos x \cos(iy) - \sin x \sin(iy)", "F BBBF BBBFPFF F BBBF BBBFPFF")
SRC_L2B = (r"= \cos x \cosh y - \sin x \sin(iy)", "F BBBF TTTTF F BBBF BBBFPFF")
SRC_L2C = (r"= \cos x \cosh y - \sin x \, i \sinh y", "F BBBF TTTTF F BBBF P TTTTF")
SRC_L2D = (r"= \cos x \cosh y - i \sin x \sinh y", "F BBBF TTTTF F P BBBF TTTTF")
SRC_RES = (r"\cos z = \cos x \cosh y - i \sin x \sinh y", "BBBF F BBBF TTTTF F P BBBF TTTTF")
SRC_ADD = (r"\cos(A + B) = \cos A \cos B - \sin A \sin B", "BBBFYFYF F BBBY BBBY F BBBY BBBY")
# result-line glyph ranges
R_COSX, R_COSHY, R_MINUS, R_I, R_SINX, R_SINHY = (5, 9), (9, 14), (14, 15), (15, 16), (16, 20), (20, 25)


def grp(m, a, b):
    """A fresh VGroup of glyphs a..b-1 (positions / flashes only, never animated itself)."""
    return VGroup(*m[0][a:b])


def glyphs(m, a, b):
    return list(m[0][a:b])


# ---------------------------------------------------------------- Example 35 card
def ex35_card(pos="top"):
    """The notes' green-bordered Example 35 box. pos: "centre" (full size, centre), "left"
    (docked top-left) or "top" (docked top-centre; the chapter's resting place)."""
    title = T("Example 35: Roots of complex cosine", 34, weight=BOLD)
    words = T("Find all the roots of", 40)
    eq = ctex(r"\cos z = 2", "BBBFFF", size=50)
    dot = T(".", 40)
    body = VGroup(words, eq, dot).arrange(RIGHT, buff=0.2)
    eq.align_to(words, DOWN).shift(0.02 * DOWN)
    dot.align_to(words, DOWN).shift(0.08 * LEFT)
    VGroup(title, body).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.15, width=title.width + 0.8,
                             height=VGroup(title, body).height + 0.6,
                             stroke_color=GREEN, stroke_width=3).move_to(VGroup(title, body))
    card = VGroup(frame, title, body)
    if pos == "centre":
        card.scale(1.25).move_to([0, 0.4, 0])
    else:
        card.scale(DOCK)
        if pos == "left":
            card.to_corner(UL, buff=0.35)
        else:
            card.move_to([0, 4 - 0.35 - card.height / 2, 0])
    card.frame, card.title, card.body = frame, title, body
    return card


def result_line(y=Y_RES):
    """The lecturer's line, centred: cos z = cos x cosh y - i sin x sinh y."""
    m = ctex(*SRC_RES, size=SZ)
    return m.move_to([0, y, 0])


def handover_shot():
    """Last frame / ch4_s4_cases' first: the Example 35 card at the top + the result line."""
    return VGroup(ex35_card("top"), result_line())


# ---------------------------------------------------------------- check panels
PANEL_W, PANEL_H, PANEL_TOP = 6.4, 3.95, 0.7


def _panel_frame(x):
    return RoundedRectangle(corner_radius=0.2, width=PANEL_W, height=PANEL_H, stroke_color=DIM,
                            stroke_width=2).move_to([x, PANEL_TOP - PANEL_H / 2, 0])


def _panel_text(frame, head_src, facts, eq):
    """Header (YELLOW) + facts on the first row, the reduced equation on the second."""
    head = MathTex(head_src, font_size=46, color=YELLOW)
    f = ctex(*facts, size=40)
    row = VGroup(head, f).arrange(RIGHT, buff=0.55)
    row.move_to(frame.get_top() + 0.45 * DOWN)
    e = ctex(*eq, size=50).move_to(frame.get_top() + 1.15 * DOWN)
    return head, f, e


def wave_panel(x=-3.45):
    """Left panel, y = 0: the hook's wave (BLUE cos x, dashed +-1 band) below the YELLOW line at 2."""
    frame = _panel_frame(x)
    head, facts, eq = _panel_text(frame, "y = 0", (r"\cosh 0 = 1,\ \sinh 0 = 0", "TTTTFFFF TTTTFFF"),
                                  (r"\cos z = \cos x", "BBBFF BBBF"))
    u, w = 0.45, 5.0
    cy = frame.get_bottom()[1] + 0.4 + u
    x0 = x - w / 2 + 0.25
    sx = w / (4 * PI)
    wave = ParametricFunction(lambda t: np.array([x0 + sx * t, cy + u * math.cos(t), 0]),
                              t_range=[0, 4 * PI], color=BLUE, stroke_width=4)
    top = DashedLine([x0 - 0.1, cy + u, 0], [x0 + w + 0.1, cy + u, 0], dash_length=0.1,
                     color=DIM, stroke_width=2)
    bot = DashedLine([x0 - 0.1, cy - u, 0], [x0 + w + 0.1, cy - u, 0], dash_length=0.1,
                     color=DIM, stroke_width=2)
    two = Line([x0 - 0.1, cy + 2 * u, 0], [x0 + w + 0.1, cy + 2 * u, 0], color=YELLOW, stroke_width=4)
    lab = MathTex("2", font_size=34, color=YELLOW).next_to(two, LEFT, buff=0.15)
    plot = VGroup(top, bot, wave, two, lab)
    g = VGroup(frame, head, facts, eq, plot)
    g.frame, g.head, g.facts, g.eq, g.plot = frame, head, facts, eq, plot
    return g


def cosh_panel(x=3.45):
    """Right panel, x = 0: cos(iy) = cosh y over the cosh curve (TEAL, horizontal axis y) with the
    YELLOW line at 2 it crosses twice. .axes .curve .two .lab .ylab .dots for reuse (ch4_s5)."""
    frame = _panel_frame(x)
    head, facts, eq = _panel_text(frame, "x = 0", (r"\cos 0 = 1,\ \sin 0 = 0", "BBBFFFF BBBFFF"),
                                  (r"\cos(iy) = \cosh y", "BBBFPFF F TTTTF"))
    lim = math.acosh(3.0)
    ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[0, 3.0, 1], x_length=4.6, y_length=1.9, tips=False,
              axis_config={"stroke_color": DIM, "stroke_width": 2, "include_ticks": False})
    ax.move_to([x - 0.1, frame.get_bottom()[1] + 0.25 + 1.9 / 2, 0])
    ylab = MathTex("y", font_size=36, color=DIM).next_to(ax.x_axis, RIGHT, buff=0.15)
    two = Line(ax.c2p(-2.2, 2), ax.c2p(2.2, 2), color=YELLOW, stroke_width=4)
    lab = MathTex("2", font_size=34, color=YELLOW).next_to(two, LEFT, buff=0.15)
    curve = ax.plot(math.cosh, x_range=[-lim, lim, 0.02], color=TEAL, stroke_width=5)
    r = math.acosh(2.0)
    dots = VGroup(*[Dot(ax.c2p(s * r, 2), radius=0.09, color=YELLOW) for s in (-1, 1)])
    plot = VGroup(ax, ylab, two, lab, curve, dots)
    g = VGroup(frame, head, facts, eq, plot)
    g.frame, g.head, g.facts, g.eq, g.plot = frame, head, facts, eq, plot
    g.axes, g.curve, g.two, g.lab, g.ylab, g.dots = ax, curve, two, lab, ylab, dots
    return g


class Split(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        # clear the check panels and braces: the card and the line remain (handover)
        res = self.res
        self.play(*disappear(self.left, self.right), *self.restore(res), run_time=1.0)
        self.wait(1.0)

    def restore(self, m):
        pat = SRC_RES[1].replace(" ", "")
        col = S4._COL
        return [g.animate.set_color(col[p]) for g, p in zip(m[0], pat)]

    # ------------------------------------------------------------ c4.split.1
    def clip1(self):
        with self.say("c4.split.1") as c:
            card = ex35_card("centre")
            self.play(FadeIn(card.frame), *appear(card.title), run_time=1.2)
            c.wait_until("find all")
            self.play(*appear(card.body), run_time=1.0)
            self.card = card

            c.wait_until("split")
            z = ctex(*SRC_Z, size=66).move_to([0, 0.2, 0])
            card.generate_target()
            card.target.become(ex35_card("left"))
            self.play(*during([MoveToTarget(card)], 0, 0.6), *during(appear(z), 0.5, 1), run_time=2.0)
            self.z = z

            c.wait_until("reason")
            tag = T("real functions", 34, color=GREEN)
            tag.next_to(grp(z, 7, 12), DOWN, buff=0.45)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            self.ztag = tag

    # ------------------------------------------------------------ c4.split.2
    def clip2(self):
        with self.say("c4.split.2") as c:
            l1 = at_glyph(ctex(*SRC_L1, size=SZ), 4, XEQ, Y1)
            self.play(*during(disappear(self.ztag), 0, 0.4), *during(edit(self.z, l1), 0.2, 1),
                      run_time=1.8)
            self.l1 = l1

            c.wait_until("formula")
            add = ctex(*SRC_ADD, size=44)
            add.move_to([0, Y_ADD, 0])
            frame = RoundedRectangle(corner_radius=0.2, width=add.width + 0.7, height=add.height + 0.55,
                                     stroke_color=DIM, stroke_width=2).move_to(add)
            self.play(FadeIn(frame), *appear(add, shift=None), run_time=1.2)
            self.play(FlashAround(VGroup(frame), color=YELLOW, run_time=1.5, time_width=1.5))
            self.add_card = VGroup(frame, add)
            settle(self, self.add_card)

            c.wait_until("cosine of ex")
            l2 = at_glyph(ctex(*SRC_L2, size=SZ), 0, XEQ, Y2)
            self.play(*appear(l2, shift=None),
                      FlashAround(grp(add, 9, 26), color=BLUE, run_time=1.8, time_width=1.5),
                      run_time=1.8)
            self.l2 = l2

            c.wait_until("valid")
            tag = words_var("valid for complex", "A, B", size=32, color=GREEN)
            tag.next_to(frame, DOWN, buff=0.22)
            self.play(*appear(tag), run_time=1.0)
            self.add_tag = tag

    # ------------------------------------------------------------ c4.split.3
    def pointer(self, row, target, angle=PI / 4, below=None):
        """TEAL arrow from a dictionary row's left edge to the top of `target`. With `below` (a lower
        row) it leaves to the left of the card, passes under `below` and arrives from above-left,
        so it crosses no text."""
        left = min(r.tex.get_left()[0] for r in self.dict.all_rows)
        start = np.array([left - 0.15, row.get_y(), 0])
        end = target.get_top() + 0.15 * UP
        if below is None:
            return CurvedArrow(start, end, angle=angle, color=TEAL, stroke_width=4)
        via = np.array([left - 0.45, below.get_bottom()[1] - 0.25, 0])
        arrow = Line(start, end, color=TEAL, stroke_width=4)
        arrow.set_points_smoothly([start, via, end])
        arrow.add_tip(tip_length=0.25)
        return arrow

    def clip3(self):
        with self.say("c4.split.3") as c:
            d = dictionary_card(rows=3)
            self.play(*appear(d, shift=0.4 * DL), *set_alpha([self.add_card, self.add_tag], 0.4),
                      run_time=1.2)
            self.dict = d

            c.wait_until("cosiy")
            l2 = self.l2
            arrow = self.pointer(d.rows[0].tex, grp(l2, 5, 12), angle=-PI / 3)
            self.play(Create(arrow),
                      FlashAround(d.rows[0].tex, color=TEAL, run_time=1.2, time_width=1.5),
                      run_time=1.2)
            l2b = at_glyph(ctex(*SRC_L2B, size=SZ), 0, XEQ, Y2)
            self.play(*edit(l2, l2b), run_time=1.5)
            self.arrow = arrow

            c.wait_until("siniy")
            arrow2 = self.pointer(d.rows[1].tex, grp(l2b, 15, 22), below=d.rows[2].tex)
            self.play(Transform(arrow, arrow2),
                      FlashAround(d.rows[1].tex, color=TEAL, run_time=1.2, time_width=1.5),
                      run_time=1.2)
            l2c = at_glyph(ctex(*SRC_L2C, size=SZ), 0, XEQ, Y2)
            self.play(*edit(l2b, l2c), run_time=1.5)

            c.wait_until("this time")
            l2d = at_glyph(ctex(*SRC_L2D, size=SZ), 0, XEQ, Y2)
            moves = []
            src = list(l2c[0])
            dst = list(l2d[0])
            order = list(range(11)) + [15, 11, 12, 13, 14] + list(range(16, 21))   # l2d slot -> l2c glyph
            for k, j in enumerate(order):
                if j == 15:
                    moves.append(src[j].animate(path_arc=-PI * 0.9).move_to(dst[k]))
                else:
                    moves.append(src[j].animate.move_to(dst[k]))
            self.play(*moves, run_time=1.6)
            self.remove(*l2c.get_family())
            self.add(l2d)
            self.play(FlashAround(l2d[0][11], color=PINK, run_time=1.2, time_width=1.5))
            self.l2 = l2d

            c.wait_until("result")
            res = result_line(Y_WORK)
            top = ex35_card("top")
            self.card.generate_target()
            self.card.target.become(top)
            self.play(*during(disappear(self.dict, self.arrow, self.add_card, self.add_tag, self.l1), 0, 0.4),
                      *during([MoveToTarget(self.card)], 0.15, 0.75),
                      *during(edit(l2d, res), 0.3, 1), run_time=2.2)
            self.res = res

    # ------------------------------------------------------------ c4.split.4
    def clip4(self):
        res = self.res
        with self.say("c4.split.4") as c:
            c.wait_until("real")
            b1 = Brace(grp(res, *R_COSX).add(*glyphs(res, *R_COSHY)), DOWN, buff=0.15, color=FG)
            t1 = T("real part", 32).next_to(b1, DOWN, buff=0.1)
            self.play(GrowFromCenter(b1), *appear(t1), run_time=1.2)

            c.wait_until("imag")
            b2 = Brace(grp(res, R_MINUS[0], R_SINHY[1]), DOWN, buff=0.15, color=PINK)
            t2 = T("imaginary part", 32, color=PINK).next_to(b2, DOWN, buff=0.1)
            c.wait_until(own_word=t2, )
            self.play(GrowFromCenter(b2), *appear(t2), run_time=1.2)
            self.braces = [b1, t1, b2, t2]

            c.wait_until("circular")
            self.play(FlashAround(grp(res, *R_COSX), color=BLUE, run_time=1.5, time_width=1.5),
                      FlashAround(grp(res, *R_SINX), color=BLUE, run_time=1.5, time_width=1.5))
            c.wait_until("hyperbolic")
            self.play(FlashAround(grp(res, *R_COSHY), color=TEAL, run_time=1.5, time_width=1.5),
                      FlashAround(grp(res, *R_SINHY), color=TEAL, run_time=1.5, time_width=1.5))

    # ------------------------------------------------------------ c4.split.5
    def clip5(self):
        res = self.res
        left, right = wave_panel(), cosh_panel()
        self.left, self.right = left, right
        with self.say("c4.split.5") as c:
            self.play(*during(disappear(*self.braces), 0, 0.45),
                      *during([res.animate.shift((Y_RES - Y_WORK) * UP)], 0.2, 0.8),
                      *during([FadeIn(left.frame), FadeIn(right.frame)], 0.6, 1), run_time=1.6)

            c.wait_until("yzero")
            self.play(*appear(left.head), run_time=0.9)
            c.wait_until("cosh of zero")
            hyper = glyphs(res, *R_COSHY) + glyphs(res, R_MINUS[0], R_SINHY[1])
            self.play(*appear(left.facts, shift=None), *recolor(hyper, DIM), run_time=1.4)
            c.wait_until("plain")
            self.play(*appear(left.eq), FadeIn(left.plot), run_time=1.4)

            c.wait_until("xzero")
            self.play(*self.restore(res), *appear(right.head), run_time=1.0)
            c.wait_until("imaginary axis")
            circ = glyphs(res, *R_COSX) + glyphs(res, R_MINUS[0], R_SINHY[1])
            self.play(*appear(right.facts, shift=None), *recolor(circ, DIM), run_time=1.4)

            c.wait_until("becomes")
            p = right
            self.play(*appear(p.eq), FadeIn(p.axes), FadeIn(p.ylab), FadeIn(p.two), FadeIn(p.lab),
                      run_time=1.2)
            c.wait_until("climb")
            self.play(Create(p.curve), run_time=2.0)
            self.play(*[GrowFromCenter(d) for d in p.dots], run_time=0.8)
