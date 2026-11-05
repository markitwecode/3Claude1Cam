"""Chapter 8, scene 6: F18, five logarithms, each a ladder in its own small w-plane. Clips c8.f18.1 – c8.f18.5.

Shared piece for the recap (ch8_s8_end):
  recap_panel()  VGroup of the five mini-ladders as at the end of (e): each a VGroup(w-plane axes,
                 GOLD dashed line, TEAL rungs, GREEN principal value, fading TEAL dots), in their
                 in-scene positions (row across the frame, w origins at y = W_Y). .ladders = list.
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
C4D = load_scene("ch4_s2_define")
C4L = load_scene("ch4_s4_ln2i")
mt = C4D.mt

LN2 = float(np.log(2))
LN5 = float(np.log(5))
TH_D = float(np.arctan2(4, 3))       # arg(3 + 4i), the sample point for (d)
TH_E = 0.7                           # sample theta for (e), r = 2

# layout
CX = [-5.0, -2.45, 0.1, 2.65, 5.2]   # panel centres
W_Y = -0.35                          # w-plane origins' y
SX = 1.0
SY = 0.85 / (2 * PI)                 # 2 pi i -> 0.85 units
W_LO, W_HI = 1.45, 1.75              # w-plane extent below / above its origin (screen units)
A_Y = 2.6                            # tiny Argand planes' origin y
U_A = 0.5                            # tiny Argand unit
EQ_Y1, EQ_Y2 = -2.45, -3.2
EQ_SIZE = 42

# (Re w, principal Im w) per part
LADDERS = [(0.0, PI), (0.0, PI / 2), (LN2 / 2, PI / 4), (LN5, -TH_D), (LN2, TH_E + PI / 2)]


def w_origin(k):
    return np.array([CX[k] - 0.75, W_Y, 0])


def a_origin(k):
    return np.array([CX[k] + 0.1, A_Y, 0])


def apt(k, r, ang):
    return a_origin(k) + r * np.array([np.cos(ang), np.sin(ang), 0])


# ------------------------------------------------------------------ pieces
def mini_wplane(k):
    """ch4's w_plane, small: grid, Re and Im axes (labels split off as .re .im)."""
    wp = C4L.w_plane(origin=w_origin(k), sx=SX, sy=SY, xr=(-0.3, 1.85), yr=(-W_LO / SY, W_HI / SY))
    g = VGroup(wp[0], wp[1], wp[2])
    g.re, g.im = wp[3], wp[4]
    return g


def mini_ladder(k, re=None, im=None):
    """ch4's ladder() moved to Re w = re, principal Im w = im in panel k: .line .dots .fades .brace .brace_label."""
    x0, y0 = LADDERS[k]
    x0 = x0 if re is None else re
    y0 = y0 if im is None else im
    o = w_origin(k) + np.array([SX * (x0 - LN2), SY * (y0 - PI / 2), 0])
    L = C4L.ladder(origin=o, sx=SX, sy=SY, ns=(-1, 0, 1), n_fade=2, fade_step=0.17,
                   y_lo=W_Y - W_LO, y_hi=W_Y + W_HI)
    dots = [L.dots[n] for n in (-1, 0, 1)]
    g = VGroup(L.line, *dots, L.fade_bot, L.fade_top)
    g.line, g.dots, g.fades = L.line, dots, [L.fade_bot, L.fade_top]
    g.brace, g.brace_label = L.brace, L.brace_label
    g.point = L.point
    return g


def ladder_dots(L):
    """Every dot of a mini ladder (rungs and fading ones), one mobject each."""
    return list(L.dots) + [d for f in L.fades for d in f]


def tiny_argand(k):
    o = a_origin(k)
    kw = dict(buff=0, stroke_width=2, color=FG, tip_length=0.1, max_tip_length_to_length_ratio=0.2)
    xax = Arrow(o + 0.72 * LEFT, o + 0.8 * RIGHT, **kw)
    yax = Arrow(o + 0.55 * DOWN, o + 0.72 * UP, **kw)
    circ = Circle(radius=U_A, color=DIM, stroke_width=1.5).move_to(o)
    return VGroup(circ, xax, yax)


def zpoint(k, r, ang, color=FG):
    p = apt(k, r, ang)
    return VGroup(Line(a_origin(k), p, color=GOLD, stroke_width=3), Dot(p, radius=0.06, color=color))


def arg_arc(k, ang, start=0.0, radius=0.2):
    return Arc(radius=radius, start_angle=start, angle=ang, arc_center=a_origin(k), color=YELLOW,
               stroke_width=3)


def panel_label(k):
    return T(f"({'abcde'[k]})", size=36).move_to([CX[k] - 0.95, A_Y + 0.4, 0])


def eq(parts, y):
    return mt(parts, EQ_SIZE).move_to([0, y, 0])


def rule_box(size=50):
    """ch4 s2's boxed rule: z = |z| e^{i(θ+2πn)} ⇒ ln z = ln|z| + i(θ + 2πn)."""
    f = mt([("z =", FG), (r"|z|", GOLD),
            (r"\,e^{i(\theta+2\pi n)}", {1: PINK, 3: YELLOW, 4: TEAL, 5: TEAL, 6: TEAL, 7: TEAL}),
            (r"\quad\Rightarrow\quad", FG), (r"\ln z =", FG), (r"\ln|z|", GOLD), ("+", FG), ("i", PINK),
            (r"\big(", FG), (r"\theta", YELLOW), (r"+2\pi n", TEAL), (r"\big)", FG)], size)
    rect = SurroundingRectangle(f, color=YELLOW, buff=0.32, stroke_width=4)
    g = VGroup(f, rect)
    g.formula, g.rect = f, rect
    g.lhs, g.rhs = list(f[0:3]), list(f[3:])
    return g


def final_ladders():
    out = []
    for k in range(5):
        out.append(VGroup(mini_wplane(k), mini_ladder(k)))
    return out


def recap_panel():
    lads = final_ladders()
    g = VGroup(*lads)
    g.ladders = lads
    return g


# ------------------------------------------------------------------ scene
class F18(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -------------------------------------------------------------- card
    def clip1(self):
        with self.say("c8.f18.1") as c:
            row = S1.card_row(lit=True)
            self.play(FadeIn(row), run_time=1.0)  # early: the chapter's card row, as s1 left it
            line1 = T("Find the (natural) logarithms of the following:", size=36)
            items = VGroup(*[MathTex(r"\text{(%s)}\;\; %s" % (l, s), font_size=44)
                             for l, s in (("a", "-1"), ("b", "i"), ("c", "1+i"), ("d", "(x+iy)^*"),
                                          ("e", r"i\,r\,e^{i\theta}"))]).arrange(RIGHT, buff=0.75)
            q = S1.question_card("F18", [line1, items])
            card = row.cards[5]
            others = [cd for i, cd in enumerate(row.cards) if i != 5]
            c.wait_until("Find")
            lab = card.label
            k = q.label.height / lab.height
            self.play(*during([FadeOut(o) for o in others], 0, 0.45),
                      *during([TransformFromCopy(card.box, q.box)], 0.25, 1),
                      *during([lab.animate.scale(k).move_to(q.label).set_color(YELLOW)], 0.3, 1),
                      *during([FadeOut(card.icon), FadeOut(card.tag), FadeOut(card.box)], 0.3, 0.7),
                      run_time=1.6)
            self.remove(lab)
            self.add(q.label)
            self.play(*appear(line1), run_time=1.0)
            for cue, it in zip(("minus one", "eye", "one plus eye", "the conjugate", "eye times R"), items):
                c.wait_until(cue)
                self.play(*appear(it, shift=None), run_time=0.7)
            c.wait_until("stop")
            self.play(*appear(q.icon), run_time=0.8)
            self.play(FlashAround(q.icon, run_time=1.5, time_width=1.5))
            self.q = q

    # -------------------------------------------------------------- rule
    def clip2(self):
        with self.say("c8.f18.2") as c:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
            rule = rule_box(50).move_to(0.3 * UP)
            c.wait_until("Write the number")
            self.play(*appear(*rule.lhs, lag=0.3), run_time=1.4)
            c.wait_until("two pi N")
            self.play(FlashUnder(VGroup(*rule.formula[2][4:8]), color=TEAL, run_time=1.2))
            c.wait_until("Its log")
            self.play(*appear(*rule.rhs, lag=0.15), run_time=1.6)
            self.play(FadeIn(rule.rect, scale=1.04), run_time=0.8)   # not GrowFromCenter: it cut through the formula
            settle(self, rule)
            self.rule = rule

            self.labels = [panel_label(k) for k in range(5)]
            self.argands = [tiny_argand(k) for k in range(5)]
            self.wplanes = [mini_wplane(k) for k in range(5)]
            panels = [VGroup(self.labels[k], self.argands[k], self.wplanes[k]) for k in range(5)]
            c.wait_until("ladder")
            self.play(*during(disappear(rule), 0, 0.4),
                      *during(appear(*panels, lag=0.15), 0.35, 1), run_time=2.2)

    # -------------------------------------------------------------- helpers
    def activate(self, k):
        anims = recolor([self.labels[k]], YELLOW)
        if k:
            anims += recolor([self.labels[k - 1]], FG)
        return anims

    # -------------------------------------------------------------- (a) (b) (c)
    def clip3(self):
        with self.say("c8.f18.3") as c:
            # (a) -1
            pa = zpoint(0, U_A, PI)
            arc_a = arg_arc(0, PI)
            self.play(*self.activate(0), *appear(pa, arc_a, shift=None, lag=0.3), run_time=1.2)
            eq_a = mt([(r"\ln(-1) =", FG), ("i", PINK), (r"(", FG), (r"\pi", YELLOW),
                       (r"+2\pi n", TEAL), (r")", FG)], EQ_SIZE)
            eq_odd = mt([(r"=(2n+1)\pi", FG), ("i", PINK)], EQ_SIZE)
            VGroup(eq_a, eq_odd).arrange(RIGHT, buff=0.3).move_to([0, EQ_Y1, 0])
            eq_odd.match_y(eq_a)
            La = mini_ladder(0)
            c.wait_until("so its log")
            self.play(*appear(eq_a, shift=None), *appear(La.line, *ladder_dots(La), shift=None, lag=0.08),
                      run_time=1.6)
            tag = VGroup(T("principal", size=28, color=GREEN), T("value", size=28, color=GREEN)) \
                .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            tag.next_to(La.dots[1], RIGHT, buff=0.22).shift(0.27 * UP)
            self.play(*appear(tag, shift=None), run_time=0.9)  # early: legend for the GREEN dots, never read aloud
            rung_lab = []
            for n, d in zip((-1, 0, 1), La.dots):
                s = {-1: r"-\pi i", 0: r"\pi i", 1: r"3\pi i"}[n]
                m = MathTex(s, font_size=30, color=GREEN if n == 0 else TEAL)
                m.next_to(d, LEFT, buff=0.14)
                rung_lab.append(m)
            c.wait_until("a_odd")
            self.play(*appear(eq_odd, shift=None), *appear(*rung_lab, shift=None, lag=0.2), run_time=1.3)

            # (b) i
            pb = zpoint(1, U_A, PI / 2)
            arc_b = arg_arc(1, PI / 2)
            eq_b = eq([(r"\ln i =", FG), ("i", PINK), (r"(", FG), (r"\pi/2", YELLOW),
                       (r"+2\pi n", TEAL), (r")", FG)], EQ_Y2)
            c.wait_until("b")
            self.play(*self.activate(1), *appear(pb, arc_b, shift=None, lag=0.3), *appear(eq_b, shift=None),
                      run_time=1.2)
            Lb = mini_ladder(1)
            c.wait_until("pi over two")
            self.play(*appear(Lb.line, *ladder_dots(Lb), shift=None, lag=0.08), run_time=1.5)
            brace = Brace(Line(Lb.dots[1].get_center(), Lb.dots[2].get_center()), direction=RIGHT,
                          buff=0.15, color=TEAL)
            blab = MathTex(r"2\pi i", font_size=34, color=TEAL).next_to(brace, RIGHT, buff=0.1)
            self.play(GrowFromCenter(brace), *appear(blab, shift=None), run_time=1.0)

            # (c) 1 + i
            pc = zpoint(2, U_A * np.sqrt(2), PI / 4)
            arc_c = arg_arc(2, PI / 4, radius=0.25)
            eq_c1 = eq([(r"1+i =", FG), (r"\sqrt{2}", GOLD),
                        (r"\,e^{i(\pi/4+2\pi n)}", {1: PINK, 3: YELLOW, 4: YELLOW, 5: YELLOW,
                                                    6: TEAL, 7: TEAL, 8: TEAL, 9: TEAL})], EQ_Y1)
            c.wait_until("c")
            self.play(*during(disappear(eq_a, eq_odd), 0, 0.45), *self.activate(2),
                      *during(appear(pc, arc_c, shift=None, lag=0.3), 0.2, 0.8),
                      *during(appear(eq_c1, shift=None), 0.5, 1), run_time=1.8)
            eq_c2 = eq([(r"\ln(1+i) =", FG), (r"\tfrac{1}{2}\ln 2", GOLD), ("+", FG), ("i", PINK),
                        (r"(", FG), (r"\pi/4", YELLOW), (r"+2\pi n", TEAL), (r")", FG)], EQ_Y2)
            Lc = mini_ladder(2)
            c.wait_until("c_ans")
            self.play(*during(disappear(eq_b), 0, 0.45), *during(appear(eq_c2, shift=None), 0.5, 1),
                      run_time=1.3)
            self.play(*appear(Lc.line, *ladder_dots(Lc), shift=None, lag=0.08), run_time=1.4)
            self.eq_c1, self.eq_c2 = eq_c1, eq_c2

    # -------------------------------------------------------------- (d) conjugate
    def clip4(self):
        with self.say("c8.f18.4") as c:
            r = 0.62
            pz = zpoint(3, r, TH_D)
            pconj = zpoint(3, r, -TH_D, color=PURPLE)
            eq_d1 = mt([(r"(x+iy)^*", PURPLE), ("=", FG), (r"x-iy", PURPLE)], EQ_SIZE)
            eq_d1b = mt([(r"\theta", YELLOW), (r"=\arg(x+iy)", FG)], EQ_SIZE)
            VGroup(eq_d1, eq_d1b).arrange(RIGHT, buff=1.0).move_to([0, EQ_Y1, 0])
            eq_d1b.match_y(eq_d1)
            self.play(*during(disappear(self.eq_c1), 0, 0.45), *self.activate(3),
                      *during(appear(pz, shift=None), 0.2, 0.8),
                      *during(appear(eq_d1, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("same modulus")
            self.play(TransformFromCopy(pz, pconj), run_time=1.5)

            arc_z = arg_arc(3, TH_D, radius=0.25)
            arc_c = arg_arc(3, -TH_D, radius=0.25)
            c.wait_until("d_arg")
            self.play(*appear(eq_d1b, shift=None), Create(arc_z), run_time=1.2)
            c.wait_until("minus theta")
            self.play(TransformFromCopy(arc_z, arc_c), run_time=1.3)

            eq_d2 = eq([(r"\ln[", FG), (r"(x+iy)^*", PURPLE), (r"] =", FG),
                        (r"\tfrac{1}{2}\ln(x^2+y^2)", GOLD), ("+", FG), ("i", PINK), (r"(", FG),
                        (r"-\theta", YELLOW), (r"+2\pi n", TEAL), (r")", FG)], EQ_Y2)
            Ld = mini_ladder(3)
            ghost = mini_ladder(3, im=TH_D)
            for d in ladder_dots(Ld):
                d.set_color(PURPLE)
            for d in ladder_dots(ghost):
                d.set_color(DIM)
            c.wait_until("d_ans")
            self.play(*during(disappear(self.eq_c2), 0, 0.45), *during(appear(eq_d2, shift=None), 0.5, 1),
                      run_time=1.4)
            c.wait_until("plus eye times")
            self.play(*appear(Ld.line, *ladder_dots(ghost), shift=None, lag=0.06), run_time=1.2)
            c.wait_until("d_mirror")
            src = [d.copy() for d in ladder_dots(ghost)]
            # rung n of the ghost reflects onto rung -n; fading dots swap ends
            gd, ld = ladder_dots(ghost), ladder_dots(Ld)
            order = [2, 1, 0, 5, 6, 3, 4]      # ghost index i lands on Ld index order[i]
            self.play(*[ReplacementTransform(s, ld[order[i]]) for i, s in enumerate(src)], run_time=1.4)
            self.Ld, self.ghost = Ld, ghost
            self.eq_d1, self.eq_d1b, self.eq_d2 = eq_d1, eq_d1b, eq_d2
            self.dots_d = gd

    # -------------------------------------------------------------- (e) i r e^{iθ}
    def clip5(self):
        with self.say("c8.f18.5") as c:
            Ld = self.Ld
            o = a_origin(4)
            r = 0.62
            arrow = Arrow(o, apt(4, r, TH_E), buff=0, stroke_width=3, color=GOLD, tip_length=0.12,
                          max_tip_length_to_length_ratio=0.3)
            arc = arg_arc(4, TH_E, radius=0.24)
            self.play(*recolor(ladder_dots(Ld), TEAL), *recolor([Ld.dots[1]], GREEN),
                      *disappear(*ladder_dots(self.ghost)), *self.activate(4),
                      *appear(arrow, arc, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("quarter turn")
            self.play(Rotate(arrow, angle=PI / 2, about_point=o),
                      Transform(arc, arg_arc(4, TH_E + PI / 2, radius=0.24)), run_time=1.6)
            eq_e1 = eq([("i", PINK), (r"\,r\,", GOLD), (r"e^{i\theta}", {1: PINK, 2: YELLOW}), ("=", FG),
                        ("r", GOLD), (r"\,e^{i(\theta+\pi/2)}", {1: PINK, 3: YELLOW, 4: YELLOW, 5: YELLOW,
                                                                 6: YELLOW, 7: YELLOW})], EQ_Y1)
            c.wait_until("is R times")
            self.play(*during(disappear(self.eq_d1, self.eq_d1b), 0, 0.45),
                      *during(appear(eq_e1, shift=None), 0.5, 1), run_time=1.4)

            eq_e2 = eq([(r"\ln(i\,r\,e^{i\theta}) =", FG), (r"\ln r", GOLD), ("+", FG), ("i", PINK),
                        (r"(", FG), (r"\theta+\pi/2", YELLOW), (r"+2\pi n", TEAL), (r")", FG),
                        (r",\quad r>0", FG)], EQ_Y2)
            Le = mini_ladder(4)
            pre = mini_ladder(4, im=TH_E)
            for d in ladder_dots(pre):
                d.set_color(DIM)
            c.wait_until("e_ans")
            self.play(*during(disappear(self.eq_d2), 0, 0.45), *during(appear(eq_e2, shift=None), 0.5, 1),
                      run_time=1.4)
            c.wait_until("log R")
            self.play(*appear(Le.line, *ladder_dots(pre), shift=None, lag=0.06), run_time=1.0)
            c.wait_until("pi over two")
            self.play(*[ReplacementTransform(a, b) for a, b in zip(ladder_dots(pre), ladder_dots(Le))],
                      run_time=1.8)
