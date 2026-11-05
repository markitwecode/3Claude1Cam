"""Chapter 8, scene 4: F17 (sums of roots of unity) and F12 (sin 3θ, sin⁵θ). Clips c8.duo.1 – c8.duo.5.

Shared pieces for the recap (ch8_s8_end):
  recap_pascal()    the signed Pascal row over the six terms of (e^{iθ} − e^{−iθ})⁵, mirror pairs bracketed
                    by PINK arcs (as at {pairs}); centred at ORIGIN.
  recap_triangle()  the Argand plane with the cube roots and the closed GOLD chain 1, ω, ω² (as at {tri}).
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

S1 = load_scene("ch8_s1_intro")

# F17's plane: origin, unit, ranges (in plane units)
O17 = np.array([-5.05, -0.75, 0.0])
U17 = 1.45
XR = (-1.15, 3.3)
YR = (-1.3, 1.75)
RCOL = 3.6           # centre x of the right-hand column
W3 = np.exp(2j * PI / 3)
W5 = np.exp(2j * PI / 5)


def P(z, o=O17, u=U17):
    return o + u * np.array([z.real, z.imag, 0.0])


def mt(parts, size=42):
    """MathTex from (tex, colour) pairs; one submobject per pair."""
    m = MathTex(*[p for p, _ in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        sub.set_color(col)
    return m


def plane17(o=O17, u=U17, xr=XR, yr=YR):
    """ch2's argand_plane look (faint half-unit grid, Re/Im arrows, DIM unit circle), asymmetric ranges."""
    grid = VGroup()
    step = 0.5
    for k in range(int(np.ceil(xr[0] / step)), int(np.floor(xr[1] / step)) + 1):
        if k:
            grid.add(Line(P(complex(k * step, yr[0]), o, u), P(complex(k * step, yr[1]), o, u)))
    for k in range(int(np.ceil(yr[0] / step)), int(np.floor(yr[1] / step)) + 1):
        if k:
            grid.add(Line(P(complex(xr[0], k * step), o, u), P(complex(xr[1], k * step), o, u)))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow(P(complex(xr[0], 0), o, u), P(complex(xr[1], 0), o, u), **ax_kw).set_opacity(0.7)
    y_ax = Arrow(P(complex(0, yr[0]), o, u), P(complex(0, yr[1]), o, u), **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=u, color=DIM, stroke_width=2.5).move_to(o)
    return VGroup(grid, x_ax, y_ax, circle, re, im)


def cube_roots():
    """Dots at 1, ω, ω² (ω YELLOW) with labels ω, ω²."""
    d1 = Dot(P(1), radius=0.09, color=FG)
    dw = Dot(P(W3), radius=0.1, color=YELLOW)
    dw2 = Dot(P(W3 ** 2), radius=0.09, color=FG)
    lw = MathTex(r"\omega", font_size=42, color=YELLOW).next_to(dw, UL, buff=0.1)
    lw2 = MathTex(r"\omega^2", font_size=42).next_to(dw2, DL, buff=0.1)
    g = VGroup(d1, dw, dw2, lw, lw2)
    g.dots, g.labels = VGroup(d1, dw, dw2), VGroup(lw, lw2)
    return g


def unit_arrow(a, b, color=GOLD):
    return Arrow(a, b, buff=0, stroke_width=6, color=color, tip_length=0.26,
                 max_tip_length_to_length_ratio=0.25)


def chain(steps):
    """Tip-to-tail arrows for the complex steps, starting at 0; returns (arrows, vertices)."""
    pts = [0j]
    for s in steps:
        pts.append(pts[-1] + s)
    return [unit_arrow(P(pts[k]), P(pts[k + 1])) for k in range(len(steps))], pts


def tri_parts():
    arrows, pts = chain([1, W3, W3 ** 2])
    cen = sum(pts[:3]) / 3
    labs = []
    for k, tex in enumerate(["1", r"\omega", r"\omega^2"]):
        mid = (pts[k] + pts[k + 1]) / 2
        out = (mid - cen) / abs(mid - cen)
        lab = MathTex(tex, font_size=38, color=GOLD)
        lab.move_to(P(mid) + (0.3 + 0.4 * max(lab.width, lab.height)) * np.array([out.real, out.imag, 0]))
        labs.append(lab)
    zero = MathTex("=0", font_size=42, color=GOLD).next_to(P(0), DL, buff=0.12)
    return arrows, labs, zero


def recap_triangle():
    arrows, labs, zero = tri_parts()
    return VGroup(plane17(), cube_roots(), *arrows, *labs, zero)


# ---------------------------------------------------------------- F12 (ii) pieces
TERM_Y = 1.0
ROW_Y = 1.95


def six_terms():
    t = MathTex(r"e^{5i\theta}", "-", r"5e^{3i\theta}", "+", r"10e^{i\theta}", "-", r"10e^{-i\theta}",
                "+", r"5e^{-3i\theta}", "-", r"e^{-5i\theta}", font_size=44)
    for i in range(11):
        t[i].set_color(FG if i % 2 else (GOLD if i < 5 else PURPLE))
    t.move_to([-1.0, TERM_Y, 0])
    return t


def signed_row(terms):
    row = VGroup()
    for k, (s, n) in enumerate(zip("+-+-+-", [1, 5, 10, 10, 5, 1])):
        m = MathTex(s, str(n), font_size=42)
        m[0].set_color(FG)
        m[1].set_color(GOLD)
        m.move_to([terms[2 * k].get_x(), ROW_Y, 0])
        row.add(m)
    return row


def pair_arcs(terms):
    arcs = VGroup()
    for (a, b), depth in zip([(0, 10), (2, 8), (4, 6)], [0.72, 0.48, 0.26]):
        p, q = terms[a].get_bottom() + 0.12 * DOWN, terms[b].get_bottom() + 0.12 * DOWN
        y = min(p[1], q[1])
        p[1] = q[1] = y
        L = q[0] - p[0]
        arcs.add(ArcBetweenPoints(p, q, angle=4 * np.arctan(2 * depth / L), color=PINK, stroke_width=3.5))
    return arcs


def recap_pascal():
    t = six_terms()
    g = VGroup(signed_row(t), t, pair_arcs(t))
    return g.move_to(ORIGIN)


def diff_picture():
    """ch2 s6's two opposite arrows: e^{ikθ} (GOLD) then −e^{−ikθ} (PURPLE), landing on Im at 2i sin kθ."""
    o, u = np.array([4.85, -1.25, 0.0]), 0.95
    axes = VGroup(Line(P(-1.25, o, u), P(1.35, o, u)), Line(P(-1.15j, o, u), P(1.55j, o, u)))
    axes.set_stroke(FG, 2, opacity=0.7)
    circ = Circle(radius=u, color=DIM, stroke_width=2).move_to(o)
    e = np.exp(1j * 40 * DEGREES)
    g = unit_arrow(P(0, o, u), P(e, o, u), GOLD)
    p = unit_arrow(P(e, o, u), P(2j * e.imag, o, u), PURPLE)
    dot = Dot(P(2j * e.imag, o, u), radius=0.09, color=PINK)
    gl = MathTex(r"e^{ik\theta}", font_size=34, color=GOLD).next_to(P(e, o, u), RIGHT, buff=0.15).shift(0.4 * DOWN)
    pl = MathTex(r"-e^{-ik\theta}", font_size=34, color=PURPLE).next_to(P(e, o, u), UP, buff=0.3).shift(0.35 * RIGHT)
    dl = MathTex(r"2i\sin k\theta", font_size=34, color=PINK).next_to(dot, LEFT, buff=0.15)
    return VGroup(axes, circ, g, p, dot, gl, pl, dl)


class F17F12(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.to_f12()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # bring question card q out of small card idx of row
    def emerge(self, row, idx, q, rt):
        small = row.cards[idx]
        others = [cd for i, cd in enumerate(row.cards) if i != idx]
        self.play(*during(disappear(*others, small.icon, small.tag), 0, 0.4),
                  *during([TransformFromCopy(small.box, q.box)], 0.25, 1),
                  *during(fly(small.label, q.label), 0.4, 1),
                  *during([FadeOut(small.label)], 0.4, 0.5),
                  *during([FadeOut(small.box)], 0.6, 1),
                  run_time=rt)
        self.remove(*row.get_family())

    # ------------------------------------------------------------ F17
    def clip1(self):
        lines = [MathTex(r"\text{If }\omega^3 = 1,\ \text{find all values of }1 + \omega + \omega^2.", font_size=40),
                 MathTex(r"\text{Generalise your result to the case }\omega^n = 1", font_size=40),
                 MathTex(r"\text{for }n\text{ a positive integer.}", font_size=40)]
        q = S1.question_card("F17", lines)
        self.q = q
        with self.say("c8.duo.1") as c:
            row = S1.card_row()
            self.play(FadeIn(row), run_time=0.8)
            self.emerge(row, 2, q, rt=max(1.0, min(1.4, c.until("If omega"))))
            c.wait_until("If omega")
            self.play(*appear(lines[0]), run_time=1.0)
            c.wait_until("generalise")
            self.play(*appear(lines[1], lines[2], lag=0.4), run_time=1.2)
            c.wait_until("stop")
            self.play(*appear(q.icon, shift=None), run_time=0.8)
            # the card holds, ‖ up, through the pause; the plane comes in at the start of c8.duo.2

    def clip2(self):
        q = self.q
        self.plane = plane17()
        self.roots = cube_roots()
        head = T("F17", size=44, color=YELLOW).to_corner(UL, buff=0.5)
        self.head = head
        with self.say("c8.duo.2") as c:
            self.play(*during(disappear(q.box, q.body, q.icon), 0, 0.45),
                      *during(swap(q.label, head), 0.1, 0.7),
                      *during([FadeIn(self.plane)], 0.45, 0.9),
                      *during(appear(*self.roots, lag=0.1, shift=None), 0.6, 1),
                      run_time=1.4)
            # ω = 1: a straight chain of three
            straight, _ = chain([1, 1, 1])
            A = mt([(r"\omega = 1:", FG), (r"\quad 1 + \omega + \omega^2", FG), ("=", FG), ("3", GOLD)])
            A.move_to([RCOL, 2.1, 0])
            three = Dot(P(3), radius=0.09, color=GOLD)
            self.play(*[GrowArrow(a) for a in straight], *appear(A), run_time=min(1.6, c.until("sum is three", floor=0.9)))
            self.play(FadeIn(three), *flash([A[3]], color=GOLD), run_time=1.0)
            c.wait_until("other")
            B = mt([(r"(\omega - 1)", FG), (r"(1 + \omega + \omega^2)", FG)])
            B.move_to([RCOL, 0.9, 0]).set_x(0.4, LEFT)
            self.play(*appear(B), *set_alpha(straight + [three], DIMMED), run_time=1.2)
            c.wait_until("Everything cancels")
            C = mt([("=", FG), (r"\omega", FG), ("+", FG), (r"\omega^2", FG), ("+", FG), (r"\omega^3", FG),
                    ("-", FG), ("1", FG), ("-", FG), (r"\omega", FG), ("-", FG), (r"\omega^2", FG)])
            C.next_to(B, DOWN, buff=0.45).align_to(B, LEFT).shift(0.3 * RIGHT)
            self.play(*appear(C), run_time=1.0)
            pairs = [(VGroup(C[1]), VGroup(C[8], C[9])), (VGroup(C[2], C[3]), VGroup(C[10], C[11]))]
            strikes = []
            for col, pr in zip((RED, RED), pairs):
                for g in pr:
                    strikes.append(Line(g.get_corner(DL) + 0.05 * LEFT, g.get_corner(UR) + 0.05 * RIGHT,
                                        color=col, stroke_width=4))
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.35), run_time=1.4)
            c.wait_until("which is zero")
            C2 = mt([("=", FG), (r"\omega^3", FG), ("-", FG), ("1", FG), ("=", FG), ("0", GOLD)])
            C2.align_to(C, LEFT).set_y(C.get_y())
            self.play(*during(disappear(*strikes), 0, 0.4), *edit(C, C2), run_time=1.3)
            c.wait_until("so the sum")
            D = mt([(r"\omega \neq 1", FG), (r"\;\Rightarrow\;", FG), (r"1 + \omega + \omega^2", FG), ("=", FG),
                    ("0", GOLD)])
            D.move_to([RCOL, -1.6, 0])
            self.play(*appear(D), run_time=1.1)
            # ω = e^{2πi/3}: the closed triangle
            c.wait_until("tri")
            arrows, labs, zero = tri_parts()
            self.play(*disappear(*straight, three), run_time=0.7)
            for k in range(3):
                self.play(GrowArrow(arrows[k]), *appear(labs[k], shift=None), run_time=0.9 if k == 0 else 0.75)
            c.wait_until("close up")
            self.play(*appear(zero), Flash(P(0), color=GOLD, line_length=0.25, flash_radius=0.3), run_time=1.0)
            self.right = [A, B, C2, D]
            self.tri, self.tri_labs, self.zero = arrows, labs, zero

    def clip3(self):
        with self.say("c8.duo.3", gap=0.2) as c:
            box_t = mt([(r"1 + \omega + \omega^2", FG), ("=", FG), (r"3\ \text{or}\ 0", GOLD)], 44)
            box_t.move_to([RCOL, 2.2, 0])
            box = SurroundingRectangle(box_t, color=YELLOW, buff=0.22, stroke_width=3)
            self.play(*during(disappear(*self.right), 0, 0.45), *during(appear(box_t, shift=None), 0.5, 1),
                      *during([GrowFromCenter(box)], 0.6, 1), run_time=1.4)   # early: the boxed F17 answer, then generalised
            G1 = mt([(r"\omega^n = 1:", FG), (r"\quad 1 + \omega + \dots + \omega^{n-1}", FG)])
            G1.move_to([RCOL, 0.95, 0]).set_x(0.3, LEFT)
            c.wait_until("the sum of")
            self.play(*appear(G1), run_time=1.1)
            G2 = mt([("=", FG), ("n", GOLD), (r"\quad\text{if }\omega = 1", FG)])
            G2.next_to(G1, DOWN, buff=0.45).align_to(G1, LEFT).shift(0.7 * RIGHT)
            c.wait_until("is N when")
            self.play(*appear(G2), run_time=1.0)
            c.wait_until("poly")
            G3 = mt([("=", FG), (r"\frac{1 - \omega^n}{1 - \omega}", FG)])
            G3.next_to(G2, DOWN, buff=0.45).align_to(G2, LEFT)
            self.play(*appear(G3), run_time=1.2)
            c.wait_until("which is zero")
            G3b = mt([("=", FG), ("0", GOLD), (r"\ \ \text{otherwise}", FG)]).next_to(G3, RIGHT, buff=0.25)
            G3b.shift((G3[0].get_y() - G3b[0].get_y()) * UP)
            self.play(*appear(G3b, shift=None), run_time=1.0)
            c.wait_until("closed")
            pent, _ = chain([W5 ** k for k in range(5)])
            self.play(*disappear(*self.tri_labs, *self.roots), run_time=0.6)
            self.play(*[ReplacementTransform(self.tri[k], pent[k]) for k in range(3)],
                      *[GrowArrow(pent[k]) for k in (3, 4)], run_time=min(1.6, c.until(floor=1.0)))

    def to_f12(self):
        row = S1.card_row()
        sweep_clear(self, FadeIn(row), run_time=1.4)   # early: s1's card row, shown whole as the way back to the questions
        self.row = row

    # ------------------------------------------------------------ F12
    def clip4(self):
        lines = [MathTex(r"\text{Express:}", font_size=40),
                 MathTex(r"\text{i.}\ \ \sin 3\theta\ \text{in terms of powers of}\ \sin\theta;", font_size=40),
                 MathTex(r"\text{ii.}\ \sin^5\theta\ \text{in terms of}\ \sin\theta,\ \sin 2\theta,\ \sin 3\theta\ \text{etc.}",
                         font_size=40)]
        q = S1.question_card("F12", lines)
        q.remove(q.icon)
        with self.say("c8.duo.4", gap=0.8) as c:
            self.emerge(self.row, 3, q, rt=1.3)
            self.play(*appear(*lines, lag=0.3), run_time=min(1.2, c.until("i", floor=0.8)))   # early: the card is read whole
            c.wait_until("i")
            head = T("F12", size=44, color=YELLOW).to_corner(UL, buff=0.5)
            self.play(*during(disappear(q.box, q.body), 0, 0.45),
                      *during(swap(q.label, head), 0.1, 0.8), run_time=1.2)
            I1 = mt([(r"\sin 3\theta", FG), ("=", FG), (r"\mathrm{Im}\,", PINK), (r"(\cos\theta", BLUE), ("+", FG),
                     (r"i\sin\theta", PINK), (r")^3", BLUE)], 50)
            I1.move_to([0, 1.15, 0])
            self.play(*appear(I1), run_time=1.0)
            c.wait_until("That's three")
            I2 = mt([("=", FG), ("3", FG), (r"\cos^2\theta", BLUE), (r"\,\sin\theta", FG), ("-", FG),
                     (r"\sin^3\theta", FG)], 50)
            I2.next_to(I1, DOWN, buff=0.5)
            I2.shift((I1[1].get_x() - I2[0].get_x()) * RIGHT)
            self.play(*appear(I2), run_time=1.3)
            c.wait_until("swap")
            I3 = mt([("=", FG), ("3", FG), (r"(1 - \sin^2\theta)", BLUE), (r"\,\sin\theta", FG), ("-", FG),
                     (r"\sin^3\theta", FG)], 50)
            I3.align_to(I2, LEFT).set_y(I2.get_y())
            self.play(*edit(I2, I3), run_time=1.5)
            c.wait_until("i_ans")
            R = mt([(r"\sin 3\theta", FG), ("=", FG), (r"3\sin\theta", BLUE), ("-", FG), (r"4\sin^3\theta", BLUE)], 52)
            R.move_to([0, -1.9, 0])
            rbox = SurroundingRectangle(R, color=YELLOW, buff=0.22, stroke_width=3)
            self.play(*during(appear(R, shift=None), 0, 0.6), *during([FadeIn(rbox)], 0.5, 1), run_time=1.4)

    def clip5(self):
        with self.say("c8.duo.5") as c:
            Tt = mt([(r"\sin^5\theta", FG), ("=", FG), (r"\frac{(e^{i\theta} - e^{-i\theta})^5}{(2i)^5}", FG)], 44)
            Tt.move_to([-1.0, 2.95, 0])
            Tt[2][1:4].set_color(GOLD)
            Tt[2][5:9].set_color(PURPLE)
            Tt[2][12:].set_color(PINK)
            c.wait_until("raise")
            sweep_clear(self, run_time=1.0)
            self.play(*appear(Tt), run_time=1.0)
            c.wait_until("pascal")
            terms = six_terms()
            row = signed_row(terms)
            self.play(*appear(*row, lag=0.3, shift=None), run_time=1.3)
            self.play(*appear(*terms, lag=0.12), run_time=min(1.5, c.until("pairs", floor=0.8)))
            c.wait_until("pairs")
            arcs = pair_arcs(terms)
            self.play(LaggedStart(*[Create(a) for a in arcs], lag_ratio=0.3), run_time=1.2)
            c.wait_until("each pair")
            Pl = mt([("=", FG), (r"2i\sin 5\theta", PINK), ("-", FG), (r"5\cdot 2i\sin 3\theta", PINK), ("+", FG),
                     (r"10\cdot 2i\sin\theta", PINK)], 42)
            Pl.move_to([-1.0, -0.55, 0])
            pic = diff_picture()
            self.play(*appear(Pl, shift=None), *appear(*pic, lag=0.08, shift=None), run_time=1.4)
            c.wait_until("ans")
            Q = mt([("(2i)^5", PINK), ("=", FG), ("32i", PINK)], 42).move_to([4.9, 2.95, 0])
            self.play(FlashAround(Tt[2][12:], color=PINK, run_time=1.4, time_width=1.5),
                      *during(appear(Q, shift=None), 0.35, 1), run_time=1.4)
            c.wait_until("gives sine")
            F = mt([(r"\sin^5\theta", FG), ("=", FG),
                    (r"\frac{\sin 5\theta - 5\sin 3\theta + 10\sin\theta}{16}", BLUE)], 46)
            F.move_to([-1.0, -1.9, 0])
            fbox = SurroundingRectangle(F, color=YELLOW, buff=0.22, stroke_width=3)
            self.play(*appear(F), run_time=1.4)
            self.play(GrowFromCenter(fbox), run_time=0.7)
            c.wait_until("check")
            K = mt([(r"\theta = \pi/2:", FG), (r"\quad (1 + 5 + 10)/16", FG), ("=", FG), ("1", GREEN)], 40)
            K.move_to([-1.0, -3.2, 0])
            self.play(*appear(K), run_time=1.2)
            c.wait_until("which is one")
            tick = check_mark().next_to(K, RIGHT, buff=0.35)
            self.play(FadeIn(tick, scale=0.6), run_time=0.6)
