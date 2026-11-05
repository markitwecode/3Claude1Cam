"""Chapter 7, scene 3: H4, route i (x as a function of y). Clips c7.h4one.1 – c7.h4one.4.

Opens from empty on s1's card_row(lit=True); H4 (row[2], ch3 s7's h4_card) grows to the hero; the
routes i / ii light under one sliding box, "(Your answers should agree!)" turns YELLOW, the GOLD
pause icon on {stop}. Clip 2: the card shrinks top right, "route i: x as a function of y" top left;
y + e^y sin y = 1/x (left side in a BLUE box) flips into x = 1/(BOX); tag "no x: a function of y
alone". Clip 3: x = 1/BOX moves left; template d/dy 1/□ = −□'/□² ("chain rule, part 2"); d/dy y = 1,
d/dy(e^y sin y) = e^y sin y + e^y cos y with a small (106) box, terms flashed in turn, a RED ✗ on a
lone e^y cos y; then the GREEN box row and dx/dy = −GREEN/(BLUE)². Clip 4: ch3 s6's swapped pair
small + (111); the fraction turns upside down into dy/dx = −(BLUE)²/GREEN, boxed YELLOW, "route i";
its y's flash; it shrinks to the upper left beside the small card = handover_shot().

Exports: handover_shot() -> VGroup(answer, card); .answer (VGroup box, formula, label "route i"),
    .card = small_card(): compact H4 card (frame, "H4", "(Your answers should agree!)" YELLOW, Tex 32) at
    the upper right; .answer.formula has .frac .num_tex (BLUE box's tex) .den_tex (GREEN box's tex).
"""
# style: 2
# handover: next
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

HERO = np.array([0.0, 0.45, 0])
CARD_POS = np.array([3.6, 3.0, 0])
ANS_W, ANS_UL = 5.6, np.array([-6.6, 3.5, 0])


# ------------------------------------------------------------------ pieces

def lhs_tex(size=56):
    m = MathTex("y", "+", "e^y", r"\sin y", font_size=size)
    m[2].set_color(GOLD)
    return m


def dp_tex(size=56):
    m = MathTex("1", "+", "e^y", r"(\sin y + \cos y)", font_size=size)
    m[2].set_color(GOLD)
    return m


def boxed(tex, color, buff=0.12):
    rect = SurroundingRectangle(tex, color=color, buff=buff, stroke_width=3)
    g = VGroup(rect, tex)
    g.rect, g.tex = rect, tex
    return g


def frac(num, den, pad=0.1, gap=0.12):
    bar = Line(LEFT, RIGHT, stroke_width=2.6, color=FG)
    bar.set_width(max(num.width, den.width) + 2 * pad)
    num.next_to(bar, UP, buff=gap)
    den.next_to(bar, DOWN, buff=gap)
    g = VGroup(num, bar, den)
    g.num, g.bar, g.den = num, bar, den
    return g


def line(items, axis, buff=0.2):
    """Items left to right; every item that isn't the fraction `axis` sits on its bar's height."""
    g = VGroup(*items).arrange(RIGHT, buff=buff)
    for m in items:
        if m is not axis:
            m.set_y(axis.bar.get_y())
    return g


def squared(inner, size):
    """(inner)^2 around a boxed group."""
    lp = MathTex("(", font_size=size * 1.15)
    rp = MathTex(")", font_size=size * 1.15)
    two = MathTex("2", font_size=size * 0.7)
    g = VGroup(lp, inner, rp).arrange(RIGHT, buff=0.06)
    two.next_to(rp, UR, buff=0.02).shift(0.18 * DOWN)
    g.add(two)
    g.inner = inner
    return g


def y_glyphs_lhs(t):
    return [t[0][0], t[2][1], t[3][-1]]


def y_glyphs_dp(t):
    return [t[2][1], t[3][4], t[3][9]]


def answer_formula(size=48):
    """dy/dx = −(BLUE)^2 / GREEN."""
    num = squared(boxed(lhs_tex(size), BLUE), size)
    den = boxed(dp_tex(size), GREEN)
    fr = frac(num, den)
    f = line([MathTex(r"\frac{dy}{dx}", font_size=size), MathTex("=", font_size=size),
              MathTex("-", font_size=size), fr], fr, buff=0.2)
    f.frac = fr
    f.num_tex, f.den_tex = num.inner.tex, den.tex
    return f


def answer_group(size=48):
    f = answer_formula(size)
    box = SurroundingRectangle(f, color=YELLOW, buff=0.28, stroke_width=3)
    lab = T("route i", 30, YELLOW)
    g = VGroup(box, f, lab)
    g.box, g.formula, g.label = box, f, lab
    return g


def small_card():
    """The compact H4 card: frame, label, and the agree line (YELLOW). Parts .frame .label .agree."""
    lab = T("H4", 36, YELLOW)
    agree = Tex("(Your answers should agree!)", font_size=32, color=YELLOW)
    row = VGroup(lab, agree).arrange(RIGHT, buff=0.4)
    frame = RoundedRectangle(corner_radius=0.2, width=row.width + 0.7, height=row.height + 0.5)
    frame.set_stroke(DIM, 2).set_fill(opacity=0).move_to(row)
    card = VGroup(frame, lab, agree).move_to(CARD_POS)
    card.frame, card.label, card.agree = frame, lab, agree
    return card


def handover_shot():
    ans = answer_group()
    bf = VGroup(ans.box, ans.formula)
    bf.scale_to_fit_width(ANS_W).move_to(ANS_UL, aligned_edge=UL)
    ans.label.next_to(ans.box, DOWN, buff=0.15).align_to(ans.box, LEFT)
    card = small_card()
    g = VGroup(ans, card)
    g.answer, g.card = ans, card
    return g


def hl(part, color=YELLOW):
    return (Rectangle(width=part.width + 0.36, height=part.height + 0.22)
            .set_stroke(color, 2).set_fill(color, 0.14).set_z_index(-1).move_to(part))


def sq(color, s=0.46):
    return Square(side_length=s).set_stroke(color, 3).set_fill(opacity=0)


# ------------------------------------------------------------------ scene

class H4RouteOne(NarratedScene):
    def construct(self):
        s1 = load_scene("ch7_s1_intro")
        self.s1 = s1
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)   # handover: s4 opens on this shot

    # ---------------------------------------------------------------- clip 1: the card
    def clip1(self):
        row = self.s1.card_row(lit=True)
        hero = load_scene("ch3_s7_recap").h4_card().move_to(HERO)
        card = row[2]
        self.card = card
        with self.say("c7.h4one.1") as c:
            self.play(*appear(row, shift=None), run_time=0.9)  # early: s1's row, shown whole
            self.play(*during(disappear(row[0], row[1], row[3]), 0, 0.4),
                      *during(Transform(card, hero), 0.15, 1.0), run_time=1.8)
            self.remove(row)
            self.add(card)
            c.wait_until("The equation is")
            self.play(FlashUnder(card.q, color=YELLOW, time_width=1.5), run_time=2.0)
            c.wait_until("first")
            box = hl(card.i)
            self.play(FadeIn(box), run_time=0.9)
            c.wait_until("second")
            self.play(Transform(box, hl(card.ii)), run_time=1.0)
            c.wait_until("agree")
            self.play(FadeOut(box), *recolor(card.agree[0], YELLOW), run_time=1.2)
            c.wait_until("stop")
            pause = self.s1.pause_icon(0.9).move_to([0, -2.95, 0])
            self.pause = pause
            self.play(FadeIn(pause, scale=0.8), run_time=0.8)

    # ---------------------------------------------------------------- clip 2: flip
    def clip2(self):
        card = self.card
        route = T("route i: x as a function of y", 32, t2c={"route i:": TEAL})
        route.move_to([-6.6, 3.2, 0], aligned_edge=LEFT)
        self.route = route

        S = 56
        lhs = boxed(lhs_tex(S), BLUE)
        rhs = frac(MathTex("1", font_size=S), MathTex("x", font_size=S))
        eqA = line([lhs, MathTex("=", font_size=S), rhs], rhs, buff=0.3).move_to([0, 0.55, 0])
        lhs.set_y(rhs.bar.get_y())

        bx = MathTex("x", font_size=S)
        beq = MathTex("=", font_size=S)
        den = boxed(lhs_tex(S), BLUE)
        fB = frac(MathTex("1", font_size=S), den)
        eqB = line([bx, beq, fB], fB, buff=0.3).move_to([0, -1.55, 0])
        tag = T("no x: a function of y alone", 32, t2c={"no x": BLUE})
        tag.next_to(den, DOWN, buff=0.3)
        self.eqA, self.eqB, self.den, self.tag = eqA, eqB, den, tag

        with self.say("c7.h4one.2") as c:
            mini = small_card()
            self.play(*during(disappear(self.pause, card.q, card.i, card.ii), 0, 0.4),
                      *during([Transform(card.frame, mini.frame), Transform(card.label, mini.label),
                               Transform(card.agree, mini.agree)], 0.15, 0.8),
                      *during(appear(route), 0.55, 1.0),  # early: the route's title
                      run_time=1.6)
            self.play(*appear(eqA, shift=None), run_time=1.0)
            c.wait_until("in one over ex")
            self.play(FlashAround(rhs.den, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("upside down")
            self.play(*during(fly(lhs, den), 0, 0.55),
                      *during(fly(rhs.den, bx), 0.4, 0.85),
                      *during(appear(beq, fB.num, fB.bar, shift=None), 0.6, 1.0), run_time=2.2)
            c.wait_until("Now ex is one over")
            self.play(*set_alpha([eqA], 0.4), FlashAround(bx, color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("alone")
            self.play(FlashAround(den, color=BLUE, time_width=1.5), run_time=1.5)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)

    # ---------------------------------------------------------------- clip 3: dx/dy
    def clip3(self):
        eqB, den = self.eqB, self.den
        S = 46
        # template d/dy 1/□ = −□'/□²
        prime = VGroup(sq(GREEN), MathTex("'", font_size=S))
        prime[1].next_to(prime[0], UR, buff=0.02).shift(0.15 * DOWN)
        sqr = VGroup(sq(BLUE), MathTex("2", font_size=S * 0.7))
        sqr[1].next_to(sqr[0], UR, buff=0.02).shift(0.12 * DOWN)
        f1 = frac(MathTex("1", font_size=S), sq(BLUE))
        f2 = frac(prime, sqr)
        tmpl = line([MathTex(r"\frac{d}{dy}", font_size=S), f1, MathTex("=", font_size=S),
                     MathTex("-", font_size=S), f2], f1, buff=0.22).move_to([1.6, 0.6, 0])
        ttag = T("chain rule, part 2", 30, DIM).next_to(tmpl, DOWN, buff=0.3)

        P1 = MathTex(r"\frac{d}{dy}\,y", "=", "1", font_size=44).move_to([-4.6, -1.35, 0])
        P2 = MathTex(r"\frac{d}{dy}", r"(e^y \sin y)", "=", "e^y", r"\sin y", "+", "e^y",
                     r"\cos y", font_size=44).move_to([2.0, -1.35, 0])
        P2[1][1:3].set_color(GOLD)
        P2[3].set_color(GOLD)
        P2[6].set_color(GOLD)
        term1, term2 = VGroup(P2[3], P2[4]), VGroup(P2[6], P2[7])

        pb = load_scene("ch2_s5_product").product_box(44)
        k = 0.75
        pb.scale(k)
        pb.tag.scale(1 / k)
        pb.num.scale(1 / k)
        VGroup(pb.tag, pb.num).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(pb.rect, RIGHT, buff=0.2)
        pb.move_to([-6.6, -2.75, 0], aligned_edge=LEFT)

        lone = MathTex("e^y", r"\cos y", font_size=40)
        lone[0].set_color(GOLD)
        xm = cross_mark().scale(0.8)
        lone_g = VGroup(xm, lone).arrange(RIGHT, buff=0.25)
        cap = T("the product rule gives two terms", 30, RED)
        xg = VGroup(lone_g, cap).arrange(DOWN, buff=0.2).move_to([3.7, -2.85, 0])

        G_lhs = MathTex(r"\frac{d}{dy}", r"(y + e^y \sin y)", "=", font_size=44)
        G_lhs[1][3:5].set_color(GOLD)
        G_rhs = boxed(dp_tex(44), GREEN)
        G = VGroup(G_lhs, G_rhs).arrange(RIGHT, buff=0.2).move_to([0, -1.35, 0])

        Ln = boxed(dp_tex(S), GREEN)
        Ld = squared(boxed(lhs_tex(S), BLUE), S)
        Lf = frac(Ln, Ld)
        Lpre = [MathTex(r"\frac{dx}{dy}", font_size=S), MathTex("=", font_size=S), MathTex("-", font_size=S)]
        L = line([*Lpre, Lf], Lf, buff=0.2).move_to([2.9, 0.6, 0])
        self.L = L
        self.G = G

        with self.say("c7.h4one.3") as c:
            tB = eqB.copy().scale(0.8).move_to([-4.4, 0.6, 0])
            tagpos = self.tag.copy().next_to(tB[2].den, DOWN, buff=0.25).get_center()
            self.play(*during(disappear(self.eqA), 0, 0.45),
                      *during([eqB.animate.scale(0.8).move_to([-4.4, 0.6, 0]),
                               self.tag.animate.move_to(tagpos)], 0.3, 1.0), run_time=1.6)
            c.wait_until("One over something")
            self.play(*appear(tmpl, shift=None), run_time=1.6)
            c.wait_until(own_word=ttag)
            self.play(*appear(ttag), run_time=1.0)

            c.wait_until("the why term gives one")
            self.play(*during(disappear(self.tag), 0, 0.4),
                      *during(appear(P1, shift=None), 0.45, 1.0), run_time=1.6)
            c.wait_until("needs the product rule")
            self.play(*appear(P2, shift=None), *during(appear(pb), 0.4, 1.0), run_time=1.8)
            c.wait_until("Both factors change")
            self.play(*appear(lone_g, cap, lag=0.4), run_time=1.4)  # early: the slip and its fix, read together
            c.wait_until("one with sine of why")
            self.play(FlashAround(term1, color=YELLOW, time_width=1.5),
                      FlashAround(pb.term1, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("one with cosine of why")
            self.play(FlashAround(term2, color=YELLOW, time_width=1.5),
                      FlashAround(pb.term2, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("dp")
            self.play(*during(disappear(tmpl, ttag, pb, xg), 0, 0.45),
                      *swap(VGroup(P1, P2), G), run_time=1.4)
            self.play(*during(appear(Lf.bar, shift=None), 0, 0.3),
                      *during(fly(G_rhs, Ln), 0, 0.5),
                      *during(fly(den, Ld.inner), 0.4, 0.85),
                      *during(appear(*Lpre, Ld[0], Ld[2], Ld[3], shift=None, lag=0.1), 0.8, 1.0),
                      run_time=min(2.2, c.until(floor=1.5)))

    # ---------------------------------------------------------------- clip 4: reciprocal
    def clip4(self):
        L, G, eqB, card = self.L, self.G, self.eqB, self.card
        pair = load_scene("ch3_s6_reciprocal").swapped_pair()
        pair.remove(pair.r3, pair.r13)
        for pic in (pair.orig, pair.mirror):
            pic.remove(pic.run_lab, pic.rise_lab)
        k = 2.5 / pair.height
        pair.scale(k)
        for lab in (pair.xlab, pair.ylab):
            lab.scale(0.75 / k)
        pair.diag_lab.scale(0.85 / k).next_to(pair.diag.get_end(), RIGHT, buff=0.1)
        pair.move_to([-4.6, 0.75, 0])

        r111 = MathTex(r"\frac{dx}{dy}", "=", r"\frac{1}{dy/dx}", font_size=40)
        n111 = T("(111)", 28, DIM)
        g111 = VGroup(r111, n111).arrange(RIGHT, buff=0.3).move_to([-4.4, -1.6, 0])

        ans = answer_group(46)
        ans.formula.move_to([2.6, -0.7, 0])
        ans.box.move_to(ans.formula)
        ans.label.next_to(ans.box, DOWN, buff=0.18).align_to(ans.box, LEFT)
        f = ans.formula
        ys = y_glyphs_lhs(f.num_tex) + y_glyphs_dp(f.den_tex)

        final = handover_shot()

        with self.say("c7.h4one.4") as c:
            self.play(*during(disappear(eqB, G), 0, 0.45),
                      *during(L.animate.move_to(f), 0.25, 0.85),
                      *during(appear(pair, shift=None), 0.55, 1.0), run_time=1.8)
            self.play(*appear(g111, shift=None), run_time=1.0)  # early: (111), named in this sentence
            c.wait_until("Turn the derivative")
            self.play(FlashAround(r111[2], color=YELLOW, time_width=1.5), run_time=1.3)
            self.play(*swap(L, f), run_time=1.6)
            c.wait_until("answer1")
            self.play(GrowFromCenter(ans.box), *during(appear(ans.label), 0.4, 1.0),  # early: the result's name
                      run_time=1.2)
            c.wait_until("only_y")
            self.play(*flash(ys, color=YELLOW, time_width=1.5), run_time=1.6)
            c.wait_until("Keep it in view")
            self.play(*during(disappear(pair, g111, self.route), 0, 0.4),
                      *during([Transform(ans.box, final.answer.box), Transform(f, final.answer.formula),
                               Transform(ans.label, final.answer.label)], 0.25, 1.0),
                      run_time=min(1.6, c.until(floor=1.0)))
            self.remove(*ans.box.get_family(), *f.get_family(), *ans.label.get_family(), *card.get_family())
            self.add(final)
