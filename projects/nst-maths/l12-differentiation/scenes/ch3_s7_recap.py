"""Chapter 3, scene 7: recap, H4, next time, end card. Clips c3.recap.1 – c3.recap.3.

A "Recap" heading, then a row of three callbacks built on {r1} {r2} {r3}, each with its formula and a
short line under it: s3's circle (dashed x = 2.8, GREEN tangents) over 2y dy/dx = -2(x - 1); s5's
triangle over cos y = (+/-) 1/sqrt(1 + x^2), whose + turns GREEN and whose - drops RED and is struck on
"positive"; s6's swapped pair (readouts beside it) over dx/dy = 1/(dy/dx). On {h4} the lines go, the
row shrinks into a dim strip along the top and the H4 card arrives; the routes light in turn (TEAL box
on i, BLUE on ii), each gets its tag in a bottom row, and on {agree} two arrows meet at a YELLOW "=".
On {next} the board clears; ch4's opening question, then d^n/dx^n (fg) = ? under it. After the last
word the board clears into ch4's open_card(), held ~8 s, then fades.

Exports (the series' question-card style, STATUS.md ch3):
    question_card(label, lines, width=9.4, colors=None, size=30) -> VGroup centred at ORIGIN, parts
        .frame (RoundedRectangle r 0.2, DIM stroke 2, no fill, `width` wide), .label (T size 36 YELLOW,
        top left inside the frame, buff 0.35), .body (VGroup, one entry per item of `lines`; an item is
        a str (one Tex line) or a list of str (one part wrapped over lines: a VGroup of Tex lines, the
        continuation lines indented 0.55); white Tex size 40, left-aligned under the label; maths in
        $...$, `colors` = {tex substring: colour}, e.g. {"e^y": GOLD}).
    h4_card() -> question_card("H4", ...) with the sheet's text verbatim, e^y GOLD; parts as above plus
        .q (the question line, body[0]), .i and .ii (the two route parts, two lines each), .agree
        ("(Your answers should agree!)").  About 9.4 x 4.9.
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

COLS = [-4.4, 0.0, 4.4]
FIG_Y, FIG_W, FIG_H = 1.15, 4.0, 3.0
FORM_Y = -1.2
LINE_TOP = -2.0
STRIP_Y, STRIP_W, STRIP_H = 3.1, 2.6, 0.7
CARD_Y = 0.0
ROW_Y = -3.2


# ------------------------------------------------------------------ the question-card style (exported)

def question_card(label, lines, width=9.4, colors=None, size=40, indent=0.6):
    """A sheet question: DIM rounded frame, YELLOW label top left, the text verbatim in white Tex."""
    tmap = dict(colors or {})

    def tex(s):
        return Tex(s, font_size=size, color=FG, tex_to_color_map=tmap or None)

    entries = []
    for item in lines:
        if isinstance(item, (list, tuple)):
            rows = [tex(s) for s in item]
            part = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            for r in rows[1:]:
                r.shift(indent * RIGHT)
            entries.append(part)
        else:
            entries.append(tex(item))
    body = VGroup(*entries).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    pad = 0.35
    if body.width > width - 2 * pad:
        body.scale_to_fit_width(width - 2 * pad)
    lab = T(label, 36, YELLOW)
    content = VGroup(lab, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame = RoundedRectangle(corner_radius=0.2, width=width, height=content.height + 2 * pad)
    frame.set_stroke(DIM, 2).set_fill(opacity=0)
    content.move_to(frame.get_corner(UL) + np.array([pad, -pad, 0]), aligned_edge=UL)
    g = VGroup(frame, lab, body)
    g.move_to(ORIGIN)
    g.frame, g.label, g.body = frame, lab, body
    return g


def h4_card():
    """Examples sheet 1, H4, verbatim; e^y GOLD. Parts .frame .label .body .q .i .ii .agree."""
    g = question_card("H4", [
        r"Find $dy/dx$ if $y + e^y \sin y = 1/x$ by:",
        [r"i.\ \ expressing $x$ as a function of $y$", r"and then finding $dx/dy$; and"],
        [r"ii.\ differentiating the original expression", r"with respect to $x$."],
        r"(Your answers should agree!)",
    ], colors={"e^y": GOLD})
    g.q, g.i, g.ii, g.agree = g.body[0], g.body[1], g.body[2], g.body[3]
    return g


# ------------------------------------------------------------------ helpers

def fit(m, w, h, pos):
    s = min(w / m.width, h / m.height)
    m.scale(s).move_to(pos)
    return s


def resize(mob, size, orig, s):
    """Scale a label back to font `size` after its figure was scaled by s (it was built at `orig`)."""
    mob.scale(size / (orig * s))


def mt(*parts, size=36, color=FG):
    return MathTex(*parts, font_size=size, color=color)


def line_text(s):
    return T(s, 28, FG, line_spacing=0.9)


def route_box(part, color):
    return (Rectangle(width=part.width + 0.36, height=part.height + 0.24)
            .set_stroke(color, 2).set_fill(color, 0.16).set_z_index(-1).move_to(part))


def shrink(m, i, op=0.5):
    t = restyle(m, op).target_mobject
    fit(t, STRIP_W, STRIP_H, np.array([COLS[i], STRIP_Y, 0]))
    return Transform(m, t)


class Recap(NarratedScene):
    def construct(self):
        self.recap()
        self.h4()
        self.next_time()
        card = load_scene("ch4_s1_hook").open_card()
        sweep_clear(self, time_span(FadeIn(card), 0.6, 1.4), run_time=1.4)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- clip 1
    def recap(self):
        s3 = load_scene("ch3_s3_circle")
        s5 = load_scene("ch3_s5_sign")
        s6 = load_scene("ch3_s6_reciprocal")

        self.head = head = T("Recap", 44).move_to([0, 3.35, 0])

        # r1: the circle
        fig1 = s3.circle_figure(centre_dot=False, ticks=False, dashed=True, points=True, tangents=True)
        k = fit(fig1, FIG_W, FIG_H, [COLS[0], FIG_Y, 0])
        for lab in (fig1.xlab, fig1.ylab):
            resize(lab, 28, 34, k)
        F1 = mt("2y", r"\,\dfrac{dy}{dx}", "=", "-2(x - 1)").move_to([COLS[0], FORM_Y, 0])
        L1 = line_text("differentiate both sides;\nchain rule on y").move_to([COLS[0], LINE_TOP, 0], aligned_edge=UP)

        # r2: the triangle and the sign
        tri = s5.triangle()
        fit(tri, FIG_W, FIG_H, [COLS[1], FIG_Y, 0])
        F2 = mt(r"\cos y", "=", r"\pm", r"\dfrac{1}{\sqrt{1 + x^2}}")
        F2[2].set_color(YELLOW)
        plus, minus = s5.split_pm(F2[2])
        F2.move_to([COLS[1], FORM_Y, 0])
        L2 = line_text("pick the sign\nfrom the range:\ncos y > 0").move_to([COLS[1], LINE_TOP, 0], aligned_edge=UP)

        # r3: the swapped pair, readouts beside it
        pair = s6.swapped_pair()
        for pic in (pair.orig, pair.mirror):
            pic.remove(pic.run_lab, pic.rise_lab)
        pair.remove(pair.r3, pair.r13)
        r3, r13 = pair.r3, pair.r13
        VGroup(r3, r13).scale(30 / 44)
        k = fit(pair, FIG_W - 1.45, FIG_H, ORIGIN)
        for lab, orig in ((pair.xlab, 40), (pair.ylab, 40), (pair.diag_lab, 32)):
            resize(lab, 28, orig, k)
        pair.diag_lab.next_to(pair.diag.get_end(), RIGHT, buff=0.1)
        reads = VGroup(r3, r13).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        reads.next_to(pair, RIGHT, buff=0.25)
        VGroup(pair, reads).move_to([COLS[2], FIG_Y, 0])
        F3 = s6.tx([r"\dfrac{dx}{dy}", "=", r"\dfrac{1}{dy/dx}"], 36, iso=["dy/dx"], colors={"dy/dx": GREEN})
        F3.move_to([COLS[2], FORM_Y, 0])
        L3 = line_text("dx/dy = 1/(dy/dx),\nunless dy/dx = 0").move_to([COLS[2], LINE_TOP, 0], aligned_edge=UP)

        with self.say("c3.recap.1") as c:
            self.play(*appear(head), run_time=1.0)
            c.wait_until("r1")
            self.play(*appear(fig1, shift=None), run_time=1.5)
            c.wait_until("differentiate")
            self.play(*appear(F1), run_time=1.2)
            c.wait_until("chain rule")
            self.play(*appear(L1), FlashAround(F1[0], time_width=1.5), run_time=1.5)

            c.wait_until("r2")
            self.play(*appear(tri, shift=None), run_time=1.5)
            c.wait_until("both sides")
            self.play(*appear(F2), run_time=1.2)
            c.wait_until("pick the sign")
            self.play(*appear(L2), run_time=1.0)
            c.wait_until("positive")
            self.play(*recolor([plus], GREEN), FlashAround(plus, time_width=1.5), run_time=1.0)
            self.play(minus.animate.shift(0.2 * DOWN).set_color(RED), run_time=0.6)
            m = minus.get_center()
            strike = Line(m + np.array([-0.1, -0.06, 0]), m + np.array([0.1, 0.06, 0])).set_stroke(RED, 3)
            self.play(Create(strike), run_time=0.6)

            c.wait_until("r3")
            self.play(*appear(pair, shift=None), *appear(reads, lag=0.3), run_time=1.6)  # early: the callback picture, readouts part of it
            c.wait_until("one over")
            self.play(*appear(F3, L3, lag=0.4), run_time=1.4)  # early: the rule's line, read as the voice states it

        # the strip keeps only the pictures' shapes; every text goes with the lines
        fig1.remove(fig1.xlab, fig1.ylab)
        tri.remove(tri.one, tri.x, tri.hyp, tri.y)
        pair.remove(pair.xlab, pair.ylab, pair.diag_lab)
        self.add(fig1.xlab, fig1.ylab, tri.one, tri.x, tri.hyp, tri.y, pair.xlab, pair.ylab, pair.diag_lab)
        self.panels = [fig1, tri, pair]
        for p in self.panels:
            settle(self, p)
        self.lines = [L1, L2, L3, F1, F2, strike, F3, reads, fig1.xlab, fig1.ylab, tri.one, tri.x, tri.hyp,
                      tri.y, pair.xlab, pair.ylab, pair.diag_lab]

    # ---------------------------------------------------------------- clip 2
    def h4(self):
        card = h4_card().move_to([0, CARD_Y, 0])
        box_i = route_box(card.i, TEAL)
        box_ii = route_box(card.ii, BLUE)
        self.card = card

        tag_i = VGroup(T("reciprocal rule", 30, TEAL), T("(111)", 28, DIM)).arrange(RIGHT, buff=0.2)
        tag_ii = T("differentiate both sides", 30, BLUE)
        eq = MathTex("=", font_size=64, color=YELLOW).move_to([0, ROW_Y, 0])
        tag_i.move_to([-1.4, ROW_Y, 0], aligned_edge=RIGHT)
        tag_ii.move_to([1.4, ROW_Y, 0], aligned_edge=LEFT)
        ar_i = Arrow(tag_i.get_right(), eq.get_left(), buff=0.15, color=TEAL, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3)
        ar_ii = Arrow(tag_ii.get_left(), eq.get_right(), buff=0.15, color=BLUE, stroke_width=4,
                      max_tip_length_to_length_ratio=0.3)

        with self.say("c3.recap.2") as c:
            self.play(*during(disappear(self.head, *self.lines), 0, 0.4),
                      *during([shrink(p, i) for i, p in enumerate(self.panels)], 0.1, 0.65),
                      *during(appear(card, shift=None), 0.55, 1.0),  # early: the sheet question shown whole, then walked
                      run_time=2.2)
            c.wait_until("routes")
            self.play(FadeIn(box_i), run_time=0.8)
            c.wait_until("two routes")
            self.play(Transform(box_i, box_ii), run_time=0.9)
            box = box_i

            c.wait_until("first")
            self.play(Transform(box, route_box(card.i, TEAL)), run_time=0.9)
            c.wait_until("reciprocal rule")
            self.play(*appear(tag_i), run_time=1.0)

            c.wait_until("second")
            self.play(Transform(box, route_box(card.ii, BLUE)), run_time=0.9)
            c.wait_until("differentiates")
            self.play(*appear(tag_ii), run_time=1.0)  # early: the tag lands on "differentiates"

            c.wait_until("agree")
            self.play(FadeOut(box), GrowArrow(ar_i), GrowArrow(ar_ii),
                      *during(appear(eq, shift=None), 0.55, 1.0), run_time=1.5)
            c.wait_until("original equation")
            self.play(FlashUnder(card.q, color=YELLOW, time_width=1.5), run_time=min(1.5, c.until(floor=0.8)))

    # ---------------------------------------------------------------- clip 3
    def next_time(self):
        q = load_scene("ch4_s1_hook").question(size=60).move_to([0, 0.9, 0])
        nth = MathTex(r"\dfrac{d^{n}}{dx^{n}}", r"(", "f", "g", ")", r"=\;", "?", font_size=56)
        nth[2].set_color(BLUE)
        nth[3].set_color(PURPLE)
        nth[6].set_color(YELLOW)
        nth.move_to([0, -1.5, 0])
        nth.shift((q[5].get_x() - nth[5].get_x()) * RIGHT)

        with self.say("c3.recap.3") as c:
            c.wait_until("next")
            sweep_clear(self, time_span(FadeIn(q, shift=0.25 * DOWN), 0.8, 1.8), run_time=1.8)  # early: part four's question, posed as the voice says "next time"
            c.wait_until("nth")
            self.play(*appear(nth), run_time=1.2)
