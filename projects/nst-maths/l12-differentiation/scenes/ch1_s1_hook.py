"""Chapter 1, scene 1: hook: title, last time, what this lecture is (and isn't), chord to tangent. Clips c1.hook.1 – c1.hook.3."""
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
from lib.titles import title_card  # noqa: E402

PART = "Part 1 · What is a derivative?"


def open_card():
    """The chapter's title card exactly as it stands once settled (static VGroup at ORIGIN)."""
    card = title_card(PART)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


# ---------- Lecture 11 thumbnails (all white: TEAL is reserved in L12)
def _thumb_cosh():
    ax = Line(LEFT * 1.5, RIGHT * 1.5, color=DIM, stroke_width=2).shift(DOWN * 0.9)
    ay = Line(DOWN * 0.9, UP * 1.2, color=DIM, stroke_width=2)
    curve = ParametricFunction(lambda t: np.array([t, 0.62 * (np.cosh(t) - 1) - 0.55, 0]),
                               t_range=[-1.45, 1.45], color=FG, stroke_width=4)
    return VGroup(ax, ay, curve)


def _thumb_conics():
    circ = Circle(radius=0.75, color=FG, stroke_width=4).shift(LEFT * 1.05)
    ell = Ellipse(width=1.7, height=1.0, color=FG, stroke_width=4).shift(RIGHT * 1.0)
    return VGroup(circ, ell)


def _thumb_hyperbola():
    k = 0.6
    asym = VGroup(Line(1.2 * (LEFT + DOWN), 1.2 * (RIGHT + UP), color=DIM, stroke_width=2),
                  Line(1.2 * (LEFT + UP), 1.2 * (RIGHT + DOWN), color=DIM, stroke_width=2))
    right = ParametricFunction(lambda t: np.array([k * np.cosh(t), k * np.sinh(t), 0]),
                               t_range=[-1.3, 1.3], color=FG, stroke_width=4)
    left = right.copy().flip(UP, about_point=ORIGIN)
    return VGroup(asym, right, left)


def _lines(text, size, color=FG):
    """Multi-line label with each line centred."""
    return VGroup(*[T(l, size=size, color=color) for l in text.split("\n")]).arrange(DOWN, buff=0.14)


def _corner_v():
    """A tiny hint of s5: BLUE |x| with a RED dot at the corner."""
    v = VMobject(color=BLUE, stroke_width=4).set_points_as_corners([UL * 0.4, ORIGIN, UR * 0.4])
    dot = Dot(ORIGIN, radius=0.07, color=RED)
    return VGroup(v, dot)


class HookScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---- c1.hook.1: title, last time, the review, the slow parts
    def clip1(self):
        with self.say("c1.hook.1", gap=2.4) as c:
            card = open_card()
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.6),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.6),
                      time_span(FadeIn(card.course), 0.15, 0.75),
                      time_span(FadeIn(card.part), 0.3, 0.9), run_time=0.9)
            thumbs = [_thumb_cosh(), _thumb_conics(), _thumb_hyperbola()]
            row = VGroup(*thumbs).arrange(RIGHT, buff=1.1).scale(1.05).move_to(ORIGIN)
            c.wait_until("hyperbolic")
            self.play(*during([FadeOut(card)], 0, 0.45),
                      *during([FadeIn(thumbs[0], shift=0.2 * DOWN)], 0.5, 1), run_time=1.6)
            c.wait_until("circles")
            self.play(FadeIn(thumbs[1], shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("hyperbolas")
            self.play(FadeIn(thumbs[2], shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("review")

            head = T("Chapter 4 of the notes", size=34, color=DIM).move_to(UP * 3.15)
            quote = T("“a review of what you had in A-level maths,\nnot even further maths”",
                      size=38, slant=ITALIC, line_spacing=1.0)
            quote.move_to(UP * 1.75)
            box = RoundedRectangle(corner_radius=0.2, width=quote.width + 0.9, height=quote.height + 0.7,
                                   stroke_color=DIM, stroke_width=2).move_to(quote)
            who = T("— the lecturer", size=28, color=DIM).next_to(box, DOWN, buff=0.15).align_to(box, RIGHT)
            self.play(FadeOut(row), run_time=0.8)
            c.wait_until(own_word=head)
            self.play(*appear(head), run_time=0.8)
            self.play(*appear(VGroup(box, quote), who, lag=0.4), run_time=1.4)
            c.wait_until("rebuild")

            fp = T("from first principles", size=48, color=YELLOW).move_to(DOWN * 0.45)
            c.wait_until("from the foundations", own_word=fp)
            self.play(*appear(fp), run_time=1.0)
            c.wait_until("half remember")

            specs = [("implicit\ndifferentiation", "Part 3", "implicit"),
                     ("Leibniz’s\nformula", "Parts 4–5", "formula"),
                     ("classifying\nstationary points", "Part 6", "classifying")]
            tags = []
            for name, part, _ in specs:
                t = _lines(name, 34)
                p = T(part, size=28, color=DIM).next_to(t, DOWN, buff=0.18)
                tags.append(VGroup(t, p))
            trow = VGroup(*tags).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to(DOWN * 2.55)
            for tag, (_, _, word) in zip(tags, specs):
                c.wait_until(word)
                self.play(*appear(tag[0], tag[1], lag=0.3, shift=0.25 * DOWN + 0.0 * RIGHT), run_time=1.0)
            self.board1 = VGroup(head, box, quote, who, fp, trow)

    # ---- c1.hook.2: one variable here, partials later
    def clip2(self):
        with self.say("c1.hook.2", gap=1.8) as c:
            yx = MathTex("y = y(x)", font_size=60)
            axis = Arrow(LEFT * 2.0, RIGHT * 2.0, buff=0, stroke_width=4, color=FG)
            xl = MathTex("x", font_size=44).next_to(axis, RIGHT, buff=0.15)
            tag = T("one variable: this lecture", size=34, color=GREEN)
            left = VGroup(yx, VGroup(axis, xl), tag).arrange(DOWN, buff=0.7).move_to(LEFT * 3.5 + UP * 0.3)

            sweep_clear(self, time_span(FadeIn(yx, shift=0.2 * DOWN), 0.6, 1.2))
            self.play(GrowArrow(axis), FadeIn(xl), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("partial")

            hxy = MathTex("h = h(x, y)", font_size=60, color=DIM)
            parts = VGroup(MathTex(r"\frac{\partial h}{\partial x}", font_size=56, color=DIM),
                           MathTex(r"\frac{\partial h}{\partial y}", font_size=56, color=DIM)).arrange(RIGHT, buff=1.2)
            pname = T("Partial differentiation", size=36, color=DIM)
            ptag = _lines("Chapter 7 of the notes,\nand next term", 30, DIM)
            right = VGroup(hxy, parts, pname, ptag).arrange(DOWN, buff=0.55).move_to(RIGHT * 3.6 + UP * 0.3)
            divider = DashedLine(UP * 2.6, DOWN * 2.6, color=DIM, stroke_width=2).move_to(UP * 0.3)

            self.play(Create(divider), FadeIn(hxy, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("different directions")
            self.play(*appear(parts[0], parts[1], lag=0.4), run_time=1.4)
            c.wait_until(own_word=pname)
            self.play(*appear(pname), run_time=1.0)
            c.wait_until("Chapter seven")
            self.play(*appear(ptag), run_time=1.0)

    # ---- c1.hook.3: chord swings to tangent; the two questions
    def clip3(self):
        with self.say("c1.hook.3", gap=2.4) as c:
            axes = Axes(x_range=[0, 1.8, 1], y_range=[0, 5, 1], x_length=5.4, y_length=3.6, tips=False,
                        axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
            axes.move_to(UP * 0.1)
            curve = axes.plot(lambda x: x ** 3, x_range=[0, 1.7], color=BLUE, stroke_width=5)
            b = ValueTracker(1.6)
            P = Dot(axes.c2p(1, 1), radius=0.09, color=FG)
            Q = always_redraw(lambda: Dot(axes.c2p(b.get_value(), b.get_value() ** 3), radius=0.09, color=FG))

            def chord_line(color=TEAL):
                bv = b.get_value()
                p = axes.c2p(1, 1)
                if abs(bv - 1) < 1e-4:
                    q = axes.c2p(1.1, 1 + 3 * 0.1)
                else:
                    q = axes.c2p(bv, bv ** 3)
                u = (q - p) / np.linalg.norm(q - p)
                mid = (p + axes.c2p(bv, bv ** 3)) / 2
                half = max(1.8, np.linalg.norm(axes.c2p(bv, bv ** 3) - p) / 2 + 0.6)
                return Line(mid - half * u, mid + half * u, color=color, stroke_width=4)

            chord = always_redraw(chord_line)
            fig = VGroup(axes, curve)

            sweep_clear(self, time_span(FadeIn(fig), 0.6, 1.4), run_time=1.4)
            c.wait_until("line through")
            self.play(FadeIn(chord), FadeIn(P), FadeIn(Q), run_time=1.2)
            c.wait_until("swing")

            self.play(b.animate.set_value(1.0), run_time=c.until("just touches", floor=2.5), rate_func=smooth)
            chord.clear_updaters()
            Q.clear_updaters()
            tangent = chord_line(GREEN)
            self.add(P)
            self.play(FadeIn(tangent), FadeOut(chord), FadeOut(Q), run_time=1.0)
            self.remove(Q)
            c.wait_until("What exactly")

            pic = VGroup(axes, curve, tangent, P)
            q1 = T("What exactly is a derivative?", size=40)
            q2 = T("When does it fail to exist?", size=40)
            VGroup(q1, q2).arrange(DOWN, buff=0.4).move_to(DOWN * 2.75)
            vhint = _corner_v().next_to(q2, RIGHT, buff=0.45)
            self.play(pic.animate.shift(UP * 0.9), run_time=0.9)
            self.play(*appear(q1), run_time=1.0)
            c.wait_until(own_word=q2)
            self.play(*appear(q2), run_time=1.0)
            self.play(FadeIn(vhint, shift=0.1 * UP), run_time=0.8)
