"""Chapter 2, scene 6: cosine and sine as exponentials, (77) and (78). Clips c2.expo.1 – c2.expo.4."""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared builders (recap reuses these)

TH0 = 50 * DEGREES
PIC = dict(cx=-2.0, cy=-0.1, u=1.45, ex=2.45, ey=2.3)       # the centre-stage plane (clips 3-4)
SIDE = dict(cx=-4.4, cy=-0.1, u=1.8, ex=1.35, ey=1.35)      # the plane beside the formulas (clips 1-2)


def to_pt(z, cx, cy, u):
    return np.array([cx + u * z.real, cy + u * z.imag, 0.0])


def build_plane(cx, cy, u, ex, ey, op=1.0):
    """Argand plane: faint integer grid, Re/Im axes, DIM unit circle (no labels)."""
    g = VGroup()
    for k in range(-int(ex), int(ex) + 1):
        if k:
            g.add(Line(to_pt(complex(k, -ey), cx, cy, u), to_pt(complex(k, ey), cx, cy, u),
                       stroke_width=1, stroke_color=DIM, stroke_opacity=0.35 * op))
    for k in range(-int(ey), int(ey) + 1):
        if k:
            g.add(Line(to_pt(complex(-ex, k), cx, cy, u), to_pt(complex(ex, k), cx, cy, u),
                       stroke_width=1, stroke_color=DIM, stroke_opacity=0.35 * op))
    g.add(Line(to_pt(complex(-ex, 0), cx, cy, u), to_pt(complex(ex, 0), cx, cy, u),
               stroke_width=2, stroke_color=FG, stroke_opacity=0.7 * op))
    g.add(Line(to_pt(complex(0, -ey), cx, cy, u), to_pt(complex(0, ey), cx, cy, u),
               stroke_width=2, stroke_color=FG, stroke_opacity=0.7 * op))
    g.add(Circle(radius=u, stroke_color=DIM, stroke_width=2, stroke_opacity=op).move_to([cx, cy, 0]))
    return g


def plane_labels(cx, cy, u, ex, ey):
    re = T("Re", 30, color=DIM).next_to(to_pt(complex(ex, 0), cx, cy, u), RIGHT, buff=0.15)
    im = T("Im", 30, color=DIM).next_to(to_pt(complex(0, ey), cx, cy, u), RIGHT, buff=0.15)
    return VGroup(re, im)


def arrow_between(a, b, color, op=1.0, width=6):
    if np.linalg.norm(b - a) < 0.06:
        return Dot(a, radius=0.03, color=color).set_opacity(op)
    return Arrow(a, b, buff=0, stroke_width=width, color=color,
                 max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=12
                 ).set_opacity(op)


def side_spot(a, b, label, normal_sign=1, turn=0.0):
    """Where a label sits beside the segment a→b: off its midpoint, on the left (+1) or right (−1)."""
    v = b - a
    n = np.linalg.norm(v)
    d = v / n if n > 1e-6 else RIGHT
    perp = normal_sign * np.array([-d[1], d[0], 0.0])
    if turn:
        perp = rotate_vector(perp, turn)
    r = 0.22 + 0.5 * max(label.width, label.height)
    return (a + b) / 2 + perp * r


def tip_spot(a, b, label):
    """Just beyond the tip of the arrow a→b, along its direction."""
    v = b - a
    n = np.linalg.norm(v)
    d = v / n if n > 1e-6 else RIGHT
    return b + d * (0.2 + 0.5 * max(label.width, label.height))


def cos_formula():
    f = MathTex(r"\cos\theta", "=", r"\frac{1}{2}", r"\Big(", r"e^{i\theta}", "+", r"e^{-i\theta}", r"\Big)",
                font_size=44)
    for i, col in enumerate([BLUE, FG, FG, FG, GOLD, FG, PURPLE, FG]):
        f[i].set_color(col)
    return f


def sin_formula():
    f = MathTex(r"\sin\theta", "=", r"\frac{1}{2i}", r"\Big(", r"e^{i\theta}", "-", r"e^{-i\theta}", r"\Big)",
                font_size=44)
    for i, col in enumerate([BLUE, FG, FG, FG, GOLD, FG, PURPLE, FG]):
        f[i].set_color(col)
    return f


def tagged_box(formula, tag, size=30):
    t = MathTex(tag, font_size=size, color=DIM).next_to(formula, RIGHT, buff=0.45)
    box = SurroundingRectangle(VGroup(formula, t), color=YELLOW, buff=0.22, stroke_width=3)
    return t, box


def recap_picture(theta=TH0):
    """The tip-to-tail sum at θ, ending at the BLUE dot 2cos θ, beside boxed (77) and (78)."""
    cx, cy, u, ex, ey = PIC["cx"], PIC["cy"], PIC["u"], PIC["ex"], PIC["ey"]
    e = np.exp(1j * theta)
    P = lambda z: to_pt(z, cx, cy, u)  # noqa: E731
    plane = build_plane(cx, cy, u, ex, ey)
    labels = plane_labels(cx, cy, u, ex, ey)
    gold = arrow_between(P(0), P(e), GOLD)
    purple = arrow_between(P(e), P(e + e.conjugate()), PURPLE)
    gl = MathTex(r"e^{i\theta}", font_size=44, color=GOLD)
    gl.move_to(side_spot(P(0), P(e), gl, +1))
    pl = MathTex(r"e^{-i\theta}", font_size=44, color=PURPLE)
    pl.move_to(side_spot(P(e), P(e + e.conjugate()), pl, +1))
    dot = Dot(P(2 * e.real), radius=0.09, color=BLUE)
    dl = MathTex(r"2\cos\theta", font_size=36, color=BLUE).next_to(dot, DOWN, buff=0.22)
    forms = boxed_pair()
    return VGroup(plane, labels, gold, purple, gl, pl, dot, dl, forms)


def boxed_pair():
    """(77) above (78), boxed YELLOW, at the right of the centre-stage plane."""
    cf, sf = cos_formula(), sin_formula()
    t77, b77 = tagged_box(cf, "(77)", 40)
    t78, b78 = tagged_box(sf, "(78)", 40)
    g77, g78 = VGroup(cf, t77, b77), VGroup(sf, t78, b78)
    for g in (g77, g78):
        g.scale(0.72)
    g77.move_to([4.55, 1.15, 0])
    g78.move_to([4.55, -1.15, 0])
    return VGroup(g77, g78)


# ---------------------------------------------------------------- scene

class CosSinExponentials(NarratedScene):
    def construct(self):
        self.setup_trackers()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    # -- live picture driven by trackers
    def setup_trackers(self):
        V = ValueTracker
        self.tr = {k: V(v) for k, v in SIDE.items()}
        for k, v in dict(th=TH0, m=0.0, s=0.0, f=0.0, plane=0.0, gold=0.0, purple=0.0, blue=0.0,
                         pink=0.0, pink2=0.0, arc=0.0, sum=0.0, dif=0.0).items():
            self.tr[k] = V(v)

    def g(self, k):
        return self.tr[k].get_value()

    def P(self, z):
        return to_pt(z, self.g("cx"), self.g("cy"), self.g("u"))

    def e(self):
        return np.exp(1j * self.g("th"))

    def purple_ends(self):
        e = self.e()
        m, s, f = self.g("m"), self.g("s"), self.g("f")
        v = complex(e.real, e.imag * (1 - 2 * m)) * (1 - 2 * f)
        start = s * e
        return self.P(start), self.P(start + v)

    def live(self, func):
        mob = always_redraw(func)
        self.add(mob)
        return mob

    def make_live(self):
        g = self.g
        self.plane = self.live(lambda: build_plane(g("cx"), g("cy"), g("u"), g("ex"), g("ey"), g("plane")))
        self.blue_seg = self.live(lambda: Line(self.P(0), self.P(complex(self.e().real, 0)), stroke_width=7,
                                               color=BLUE).set_opacity(g("blue")))
        self.pink_seg = self.live(lambda: DashedLine(self.P(complex(self.e().real, 0)), self.P(self.e()),
                                                     stroke_width=4, color=PINK, dash_length=0.1
                                                     ).set_opacity(g("pink")))
        self.pink_seg2 = self.live(lambda: DashedLine(self.P(complex(2 * self.e().real, self.e().imag)),
                                                      self.P(complex(2 * self.e().real, 0)),
                                                      stroke_width=4, color=PINK, dash_length=0.1
                                                      ).set_opacity(g("pink2")))
        self.arc = self.live(lambda: Arc(radius=0.45 * g("u"), start_angle=0, angle=g("th"),
                                         arc_center=self.P(0), stroke_width=3, color=FG
                                         ).set_opacity(g("arc")))
        self.purple = self.live(lambda: arrow_between(*self.purple_ends(),
                                                      interpolate_color(ManimColor(GOLD), ManimColor(PURPLE), g("m")), g("purple")))
        self.gold = self.live(lambda: arrow_between(self.P(0), self.P(self.e()), GOLD, g("gold")))
        self.sum_dot = self.live(lambda: Dot(self.P(2 * self.e().real), radius=0.09, color=BLUE
                                             ).set_opacity(g("sum")))
        self.dif_dot = self.live(lambda: Dot(self.P(complex(0, 2 * self.e().imag)), radius=0.09, color=PINK
                                             ).set_opacity(g("dif")))
        self.lives = [self.plane, self.blue_seg, self.pink_seg, self.pink_seg2, self.arc, self.purple,
                      self.gold, self.sum_dot, self.dif_dot]

        # labels: built once, follow by updater, enter/leave with appear/disappear
        self.re_im = plane_labels(g("cx"), g("cy"), g("u"), g("ex"), g("ey"))
        self.re_im.add_updater(lambda m: m.become(plane_labels(g("cx"), g("cy"), g("u"), g("ex"), g("ey"))))
        self.gl = MathTex(r"e^{i\theta}", font_size=44, color=GOLD)
        self.gl.add_updater(lambda m: m.move_to(side_spot(self.P(0), self.P(self.e()), m, +1)))
        self.pl = MathTex(r"e^{-i\theta}", font_size=44, color=PURPLE)
        self.pl.add_updater(lambda m: m.move_to(side_spot(*self.purple_ends(), m, -1, turn=PI * g("s"))))
        self.nl = MathTex(r"-e^{-i\theta}", font_size=44, color=PURPLE)
        self.nl.add_updater(lambda m: m.move_to(side_spot(*self.purple_ends(), m, -1)))
        self.thl = MathTex(r"\theta", font_size=34)
        self.thl.add_updater(lambda m: m.move_to(self.P(0) + 0.45 * g("u") * 1.0
                                                 * np.array([np.cos(g("th") / 2), np.sin(g("th") / 2), 0])
                                                 + 0.28 * np.array([np.cos(g("th") / 2), np.sin(g("th") / 2), 0])))
        self.sl = MathTex(r"2\cos\theta", font_size=36, color=BLUE)
        self.sl.add_updater(lambda m: m.next_to(self.P(2 * self.e().real), DOWN, buff=0.22))
        self.dl = MathTex(r"2i\sin\theta", font_size=36, color=PINK)
        self.dl.add_updater(lambda m: m.next_to(self.P(complex(0, 2 * self.e().imag)), LEFT, buff=0.2))
        for lab in (self.re_im, self.gl, self.pl, self.nl, self.thl, self.sl, self.dl):
            lab.update()

    def to(self, **vals):
        return [self.tr[k].animate.set_value(v) for k, v in vals.items()]

    # -- clip 1: Euler and its conjugate
    def clip1(self):
        self.make_live()
        X = 1.55                                  # x of the "=" column
        L1 = MathTex(r"e^{i\theta}", "=", r"\cos\theta", "+", r"i\sin\theta", font_size=46)
        L2 = MathTex(r"e^{-i\theta}", "=", r"\cos\theta", "-", r"i\sin\theta", font_size=46)
        for L, c0 in ((L1, GOLD), (L2, PURPLE)):
            for i, col in enumerate([c0, FG, BLUE, FG, PINK]):
                L[i].set_color(col)
        L1.shift([X - L1[1].get_x(), 2.85 - L1[1].get_y(), 0])
        L2.shift([X - L2[1].get_x(), 1.4 - L2[1].get_y(), 0])
        L2[3].match_x(L1[3])
        L2[2].match_x(L1[2])
        L2[4].match_x(L1[4])
        tag71 = MathTex("(71)", font_size=30, color=DIM).next_to(L1, RIGHT, buff=0.45)
        self.L1, self.L2, self.tag71 = L1, L2, tag71

        with self.say("c2.expo.1") as c:
            self.play(*self.to(plane=1.0), *appear(self.re_im, shift=None), run_time=1.2)
            c.wait_until("seventy")
            self.play(*appear(L1, tag71, lag=0.4), run_time=1.4)
            c.wait_until("E to the eye theta")
            self.play(*self.to(gold=1.0, arc=1.0), *appear(self.gl, self.thl, shift=None),
                      run_time=1.2)
            c.wait_until("cosine theta")
            self.play(*self.to(blue=1.0), FlashUnder(L1[2], color=BLUE), run_time=1.0)
            c.wait_until("plus eye sine theta")
            self.play(*self.to(pink=1.0), FlashUnder(L1[4], color=PINK), run_time=1.0)
            c.wait_until("conj")
            # the reflection: a gold copy squashes through the real axis into the PURPLE mirror
            self.tr["purple"].set_value(1.0)
            self.play(*self.to(m=1.0), run_time=1.8)
            c.wait_until(own_word=self.pl)
            self.play(*appear(self.pl, shift=None), run_time=0.8)
            c.wait_until("minus")
            # a fresh copy of (71) on the next row, then every "+ i" becomes "- i"
            L1c = L1.copy()
            L1c.shift([0, L2[1].get_y() - L1[1].get_y(), 0])
            self.play(*appear(L1c, shift=None), run_time=0.8)
            self.play(*edit(L1c, L2), run_time=1.5)
            self.play(FlashAround(L2[3], color=YELLOW, run_time=1.2, time_width=1.5))

    # -- clip 2: add, subtract
    def clip2(self):
        L1, L2 = self.L1, self.L2
        X = L1[1].get_x()
        plus = MathTex("+", font_size=46).next_to(L2, LEFT, buff=0.35)
        minus = MathTex("-", font_size=46).move_to(plus)
        rule = Line(LEFT, RIGHT, stroke_width=2, color=DIM)
        rule.put_start_and_end_on([plus.get_left()[0], 0.88, 0], [L1.get_right()[0], 0.88, 0])

        L3 = MathTex(r"e^{i\theta}", "+", r"e^{-i\theta}", "=", r"2\cos\theta", font_size=46)
        L3d = MathTex(r"e^{i\theta}", "-", r"e^{-i\theta}", "=", r"2i\sin\theta", font_size=46)
        for L, last in ((L3, BLUE), (L3d, PINK)):
            for i, col in enumerate([GOLD, FG, PURPLE, FG, last]):
                L[i].set_color(col)
            L.shift([X - L[3].get_x(), 0.25 - L[3].get_y(), 0])

        cf, sf = cos_formula(), sin_formula()
        cf.shift([X - cf[1].get_x(), -1.15 - cf[1].get_y(), 0])
        sf.shift([X - sf[1].get_x(), -2.75 - sf[1].get_y(), 0])
        t77, b77 = tagged_box(cf, "(77)")
        t78, b78 = tagged_box(sf, "(78)")

        def strike(m):
            return Line(m.get_corner(DL) + 0.05 * DL, m.get_corner(UR) + 0.05 * UR, stroke_width=4, color=RED)

        sp = [strike(L1[4]), strike(L2[4])]
        sb = [strike(L1[2]), strike(L2[2])]

        with self.say("c2.expo.2") as c:
            self.play(*appear(plus, shift=None), GrowFromCenter(rule), run_time=1.0)
            c.wait_until("cancel")
            self.play(*[Create(s) for s in sp], *set_alpha([L1[4], L2[4]], 0.4), run_time=1.0)
            self.play(*appear(L3), run_time=1.0)
            c.wait_until("cos")
            derive(self, L3, cf, run_time=2.0)
            c.wait_until("num77")
            self.play(*appear(t77, shift=None), FadeIn(b77), run_time=1.0)
            c.wait_until("sub")
            self.play(*swap(plus, minus), *[FadeOut(s) for s in sp], *set_alpha([L1[4], L2[4]], 1.0),
                      run_time=1.2)
            self.play(*[Create(s) for s in sb], *set_alpha([L1[2], L2[2]], 0.4), *swap(L3, L3d),
                      run_time=1.4)
            c.wait_until("sin")
            self.play(*appear(sf), run_time=1.2)
            c.wait_until("num78")
            self.play(*appear(t78, shift=None), FadeIn(b78), run_time=1.0)

        self.clip2_left = [L1, L2, self.tag71, minus, rule, L3d, *sb]
        self.g77 = VGroup(cf, t77, b77)
        self.g78 = VGroup(sf, t78, b78)

    # -- clip 3: the picture of the sum
    def clip3(self):
        target = boxed_pair()
        with self.say("c2.expo.3") as c:
            leave = [FadeOut(m) for m in self.clip2_left] + disappear(self.thl, self.pl) \
                + self.to(arc=0.0, blue=0.0, pink=0.0, purple=0.0)
            move = [Transform(self.g77, target[0]), Transform(self.g78, target[1])] \
                + self.to(**PIC)
            self.play(*during(leave, 0, 0.4), *during(move, 0.4, 1.0), run_time=min(2.2, c.until("gold")))
            self.tr["m"].set_value(1.0)
            # in the big picture the labels sit just beyond the arrow tips, outside the circle
            P, g = self.P, self.g
            self.gl.clear_updaters()
            self.gl.add_updater(lambda m: m.move_to(tip_spot(P(0), P(self.e()), m)))
            self.pl.clear_updaters()
            self.pl.add_updater(lambda m: m.move_to(tip_spot(*self.purple_ends(), m)))
            self.gl.update()
            self.pl.update()
            c.wait_until("gold")
            self.play(*self.to(th=130 * DEGREES), rate_func=linear, run_time=c.until("purple", floor=1.0) - 0.2)
            c.wait_until("purple")
            self.play(*self.to(purple=1.0), *appear(self.pl, shift=None), run_time=0.9)
            self.wait(0.5)
            # both labels have been read: they leave as the mirrors start to pass each other
            self.play(*self.to(th=(360 + 50) * DEGREES), *during(disappear(self.gl, self.pl), 0, 0.12),
                      rate_func=linear, run_time=c.until("tip", floor=1.0) - 0.2)
            c.wait_until("tip")
            self.play(*self.to(s=1.0), run_time=1.4)
            c.wait_until("real")
            self.play(*self.to(sum=1.0, pink=1.0, pink2=1.0), *appear(self.sl, shift=None), run_time=1.0)
            self.play(*self.to(th=(720 + 50) * DEGREES), rate_func=linear, run_time=c.until(floor=1.0) - 0.2)

    # -- clip 4: the difference, and the lecturer's verdict
    def clip4(self):
        div = MathTex(r"\div\,2i", font_size=40, color=YELLOW)
        sdot = Dot(radius=0.09, color=BLUE)
        slab = MathTex(r"\sin\theta", font_size=36, color=BLUE)
        quote = VGroup(
            T("“Working with exponentials", 38),
            T("is easier than working", 38),
            T("with cosines and sines.”", 38),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        who = T("the lecturer, 00:12:31", 30, color=DIM).next_to(quote, DOWN, buff=0.4, aligned_edge=RIGHT)
        card_txt = VGroup(quote, who)
        card = RoundedRectangle(corner_radius=0.2, width=card_txt.width + 0.9, height=card_txt.height + 0.8,
                                stroke_color=DIM, stroke_width=2).move_to(card_txt)
        VGroup(card, card_txt).move_to([-2.6, 0, 0])

        with self.say("c2.expo.4", gap=3.5) as c:
            # the sum's marks clear first, then the PURPLE arrow slides back to the origin
            self.play(*during(disappear(self.sl) + self.to(sum=0.0, pink=0.0, pink2=0.0), 0, 0.45),
                      *during(self.to(s=0.0), 0.35, 1.0), run_time=1.4)
            self.play(*self.to(f=1.0), run_time=min(1.3, c.until("The real parts")))
            c.wait_until("The real parts")
            self.play(*self.to(s=1.0), run_time=1.4)
            self.play(*appear(self.nl, shift=None), run_time=0.8)
            c.wait_until("imaginary axis")
            self.play(*self.to(dif=1.0), *appear(self.dl, shift=None), run_time=0.9)
            self.play(*self.to(th=(1080 + 50) * DEGREES), *during(disappear(self.nl), 0, 0.1), rate_func=linear,
                      run_time=c.until("divide", floor=1.0) - 0.2)
            # freeze the live picture at θ = 50°
            for m in (self.dl, self.re_im):
                m.clear_updaters()
            c.wait_until("divide")
            e = self.e()
            div.next_to(self.dl, UP, buff=0.25)
            sdot.move_to(self.P(e.imag))
            slab.next_to(sdot, DOWN, buff=0.22)
            self.play(*appear(div), run_time=0.8)
            src = Dot(self.P(complex(0, 2 * e.imag)), radius=0.09, color=PINK)
            self.add(src)
            self.play(*fly(src, sdot), *during(appear(slab, shift=None), 0.6, 1.0), run_time=1.5)
            self.remove(src)
            c.wait_until("working")
            leave = disappear(self.re_im, self.dl, div, sdot, slab) \
                + self.to(plane=0.0, gold=0.0, purple=0.0, dif=0.0)
            self.play(*during(leave, 0, 0.45),
                      *during([FadeIn(card)] + appear(*quote, who, lag=0.3), 0.45, 1.0), run_time=2.4)  # early: the quote card is shown whole, then read
        self.remove(*self.lives)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
