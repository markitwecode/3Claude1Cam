"""Chapter 2, scene 6: Example 33, tanh(A + B) through the dictionary. Clips c2.tanh.1 – c2.tanh.4.

Layout: ch2_s1's dictionary card docked top-right throughout. Clips 1–2: the Example 33 card docks
top-left with the "Recall" line under it; the chain runs below in three rows (scrolling up), each
line built from standalone MathTex pieces (positioned from one reference MathTex) so single i's
can be flashed, struck and swapped. Clip 3: the real fraction centred, ÷ labels, swaps into the
boxed answer; s5's prediction slides in below. Clip 4: s4's rows 3 and 1 fly into the ratio, the
same real fraction, the same box; then the G1 card.
"""
# style: 2
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
S5 = load_scene("ch2_s5_rule")
ctex, at_glyph, CARD_ROWS, CARD_EQ = S4.ctex, S4.at_glyph, S4.CARD_ROWS, S4.CARD_EQ

COL = dict(B=BLUE, T=TEAL, P=PINK, F=FG, Y=YELLOW, G=GOLD, D=DIM)
SZ = 40
EQX = -3.8
ROWY = [0.75, -0.95, -2.65]
PITCH = ROWY[0] - ROWY[1]


# ---------------------------------------------------------------- helpers
def dict_card():
    """ch2_s1's docked dictionary card: three rows, BLUE / TEAL / PINK i, rounded box, top-right."""
    rows = []
    for i, (src, pat, _n) in enumerate(CARD_ROWS):
        tex = ctex(src, pat, size=40)
        at_glyph(tex, CARD_EQ, 0, -i * 0.74)
        rows.append(tex)
    g = VGroup(*rows)
    box = RoundedRectangle(corner_radius=0.2, width=g.width + 0.55, height=g.height + 0.45,
                           stroke_color=DIM, stroke_width=2).move_to(g)
    card = VGroup(box, *rows)
    card.scale_to_fit_width(3.2).to_corner(UR, buff=0.25)
    card.rows = rows
    return card


def multi(parts, size=SZ):
    """One MathTex from (tex, colour-letter) parts, each part coloured."""
    m = MathTex(*[t for t, _ in parts], font_size=size)
    for k, (_, c) in enumerate(parts):
        m[k].set_color(COL[c])
    return m


def pieces_from(ref, parts, size):
    """Standalone MathTex per part, each sitting exactly where it sits in `ref`."""
    out = []
    for k, (t, c) in enumerate(parts):
        out.append(MathTex(t, font_size=size, color=COL[c]).move_to(ref[k]))
    return out


class Row:
    """[lhs] = num/den, as standalone pieces (never grouped on screen)."""

    def __init__(self, num, den, lhs=None, size=SZ, eqx=EQX, y=0.0, gap=0.3, eq=True):
        nref = MathTex(*[t for t, _ in num], font_size=size)
        dref = MathTex(*[t for t, _ in den], font_size=size)
        w = max(nref.width, dref.width) + 0.3
        self.eq = [MathTex("=", font_size=size).move_to([eqx, y, 0])] if eq else []
        left = (eqx + self.eq[0].width / 2 + gap) if eq else eqx
        bx = left + w / 2
        self.bar = Line([bx - w / 2, y, 0], [bx + w / 2, y, 0], stroke_width=3, color=FG)
        nref.next_to(self.bar, UP, buff=0.13)
        dref.next_to(self.bar, DOWN, buff=0.13)
        self.num = pieces_from(nref, num, size)
        self.den = pieces_from(dref, den, size)
        self.lhs = []
        if lhs:
            lref = MathTex(*[t for t, _ in lhs], font_size=size)
            lref.next_to(self.eq[0], LEFT, buff=gap)
            self.lhs = pieces_from(lref, lhs, size)
        self.extra = []

    def all(self):
        return self.lhs + self.eq + self.num + [self.bar] + self.den + self.extra

    def frac(self):
        return self.num + [self.bar] + self.den

    def shift(self, v):
        for p in self.all():
            p.shift(v)
        return self

    def center_x(self):
        return VGroup(*[p.copy() for p in self.all()]).get_center()[0]


def grp(ps):
    """A throwaway copy of on-screen pieces (for flashes/boxes; never added)."""
    return VGroup(*[p.copy() for p in ps])


def strike(m):
    return Line(m.get_corner(DL) + np.array([-0.06, -0.06, 0]),
                m.get_corner(UR) + np.array([0.06, 0.06, 0]), color=RED, stroke_width=5)


def moved(ps, v):
    return [p.animate.shift(v) for p in ps]


# the chain, as the notes print it (i PINK, circular BLUE, hyperbolic TEAL)
L1 = dict(lhs=[(r"\tanh(A+B)", "T")], num=[(r"\sinh(A+B)", "T")], den=[(r"\cosh(A+B)", "T")])
L2 = dict(num=[("i", "P"), (r"\sinh(A+B)", "T")], den=[("i", "P"), (r"\cosh(A+B)", "T")])
L3 = dict(num=[(r"\sin(", "B"), ("i", "P"), ("A+", "B"), ("i", "P"), ("B)", "B")],
          den=[("i", "P"), (r"\cos(", "B"), ("i", "P"), ("A+", "B"), ("i", "P"), ("B)", "B")])
L4 = dict(num=[(r"\sin(", "B"), ("i", "P"), (r"A)\cos(", "B"), ("i", "P"), ("B)", "B"), ("+", "F"),
               (r"\cos(", "B"), ("i", "P"), (r"A)\sin(", "B"), ("i", "P"), ("B)", "B")],
          den=[("i", "P"), ("[", "F"), (r"\cos(", "B"), ("i", "P"), (r"A)\cos(", "B"), ("i", "P"),
               ("B)", "B"), ("-", "F"), (r"\sin(", "B"), ("i", "P"), (r"A)\sin(", "B"), ("i", "P"),
               ("B)", "B"), ("]", "F")])
L5 = dict(num=[("i", "P"), (r"\sinh(A)\cosh(B)", "T"), ("+", "F"), (r"\cosh(A)", "T"), ("i", "P"),
               (r"\sinh(B)", "T")],
          den=[("i", "P"), ("[", "F"), (r"\cosh(A)\cosh(B)", "T"), ("+", "F"), ("(-i^2)", "P"),
               (r"\sinh(A)\sinh(B)", "T"), ("]", "F")])
REAL = dict(num=[(r"\sinh(A)\cosh(B)", "T"), ("+", "T"), (r"\cosh(A)\sinh(B)", "T")],
            den=[(r"\cosh(A)\cosh(B)", "T"), ("+", "T"), (r"\sinh(A)\sinh(B)", "T")])
ANS = dict(lhs=[(r"\tanh(A+B)", "T")],
           num=[(r"\tanh(A)", "T"), ("+", "T"), (r"\tanh(B)", "T")],
           den=[("1", "Y"), ("+", "T"), (r"\tanh(A)\tanh(B)", "T")])


def answer_row(size=48, y=0.6):
    r = Row(ANS["num"], ANS["den"], lhs=ANS["lhs"], size=size, eqx=0, y=y)
    r.den[0].set_color(TEAL)
    r.shift(LEFT * r.center_x())
    return r


def answer_box(row):
    return SurroundingRectangle(grp(row.all()), color=YELLOW, buff=0.3, stroke_width=3)


class Tanh(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c2.tanh.1
    def clip1(self):
        with self.say("c2.tanh.1") as c:
            self.card = card = dict_card()
            title = T("Example 33: Identity for hyperbolic tangent", 40, weight=BOLD)
            body = multi([(r"\text{Find an identity for }", "F"), (r"\tanh(A+B)", "T"), (".", "F")], 44)
            VGroup(title, body).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            VGroup(title, body).move_to([0, 0.3, 0]).align_to([-6.2, 0, 0], LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=title.width + 0.8,
                                   height=VGroup(title, body).height + 0.7,
                                   stroke_color=GREEN, stroke_width=3).move_to(VGroup(title, body))
            self.play(FadeIn(card), FadeIn(box), *appear(title), run_time=1.2)
            c.wait_until("find")
            self.play(*appear(body), run_time=1.0)
            ex = VGroup(box, title, body)
            settle(self, ex)
            self.ex = ex

            c.wait_until("start")
            self.play(ex.animate.scale(0.72, about_edge=LEFT), run_time=0.7)
            self.play(ex.animate.to_corner(UL, buff=0.25), run_time=0.8)
            r1 = Row(L1["num"], L1["den"], lhs=L1["lhs"], y=ROWY[0])
            self.play(*appear(*r1.lhs, *r1.eq, *r1.num, r1.bar, *r1.den, lag=0.15, shift=None),
                      run_time=min(1.5, c.until("times")))
            self.r1 = r1

            c.wait_until("times")
            r2 = Row(L2["num"], L2["den"], y=ROWY[1])
            rest = [r2.num[1], r2.bar, r2.den[1]]
            self.play(*appear(*r2.eq, *rest, lag=0.1, shift=None), run_time=1.0)
            self.play(*appear(r2.num[0], r2.den[0], lag=0, shift=0.4 * DOWN), run_time=1.0)
            self.r2 = r2

            c.wait_until("why")
            # the Recall line copies out of the dictionary card
            ref = MathTex(r"\text{Recall that }", r"\sin(iz) = i\sinh z", r"\text{ and }",
                          r"\cos(iz) = \cosh z", r"\text{.}", font_size=32)
            ref.move_to([-6.6, 1.95, 0], aligned_edge=LEFT)
            pre = MathTex(r"\text{Recall that }", font_size=32, color=DIM).move_to(ref[0])
            pa = multi([(r"\sin(", "B"), ("i", "P"), ("z)", "B"), ("=", "F"), ("i", "P"),
                        (r"\sinh z", "T")], 32).move_to(ref[1])
            andw = MathTex(r"\text{ and }", font_size=32, color=DIM).move_to(ref[2])
            pb = multi([(r"\cos(", "B"), ("i", "P"), ("z)", "B"), ("=", "F"), (r"\cosh z", "T"),
                        (r"\text{.}", "F")], 32)
            pb.move_to(VGroup(ref[3], ref[4]))
            # {why}: only the sine row (row 2) of the card, and its Recall half
            self.play(FlashAround(grp(r2.num), color=PINK, time_width=1.5),
                      FlashAround(card.rows[1], color=PINK, time_width=1.5),
                      *appear(pre, pa, lag=0.3), run_time=1.6)
            self.recall = [pre, pa, andw, pb]

            c.wait_until("top")
            r3 = Row(L3["num"], L3["den"], y=ROWY[2])
            self.play(*appear(*r3.eq, *r3.num, r3.bar, lag=0.1, shift=0.3 * DOWN),
                      run_time=min(1.5, c.until("bottom")))
            c.wait_until("bottom")
            # {bottom}: the cosine row (row 1) of the card, and the other Recall half
            self.play(FlashAround(card.rows[0], color=PINK, time_width=1.5),
                      *appear(andw, pb, lag=0.2), run_time=min(1.3, 0.4 * c.until()))
            self.play(*appear(*r3.den, lag=0.1, shift=0.3 * UP), run_time=min(1.5, 0.6 * c.until()))
            self.r3 = r3

    # ------------------------------------------------------------ c2.tanh.2
    def scroll(self, gone, stays, new, rt):
        """Top row fades, the others rise one row, the new row arrives in the bottom slot."""
        self.play(*during(disappear(*gone.all()), 0, 0.4),
                  *during([a for r in stays for a in moved(r.all(), UP * PITCH)], 0.2, 0.7),
                  *during(appear(*new, lag=0.05, shift=None), 0.6, 1.0), run_time=rt)

    def clip2(self):
        with self.say("c2.tanh.2") as c:
            r4 = Row(L4["num"], L4["den"], y=ROWY[2])
            self.scroll(self.r1, [self.r2, self.r3], r4.eq + r4.num + [r4.bar] + r4.den,
                        min(1.8, c.until("dict")))
            c.wait_until("dict")
            r5 = Row(L5["num"], L5["den"], y=ROWY[2])
            self.scroll(self.r2, [self.r3, r4], r5.eq + r5.num + [r5.bar] + r5.den,
                        min(1.8, c.until("numi")))
            c.wait_until("numi")
            ni = [r5.num[0], r5.num[4]]
            self.play(*flash(ni, color=PINK, time_width=1.5), run_time=1.5)

            c.wait_until("denom")
            mi = r5.den[4]
            self.play(FlashAround(mi, color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("plus one")
            one = MathTex("(+1)", font_size=SZ, color=YELLOW).move_to(mi)
            self.play(*swap(mi, one), run_time=1.2)
            r5.den[4] = one

            c.wait_until("cancel")
            self.play(*flash(ni, color=PINK, time_width=1.5), run_time=1.3)
            c.wait_until("so does the bottom")
            self.play(FlashAround(r5.den[0], color=PINK, time_width=1.5), run_time=1.3)
            c.wait_until("the eyes cancel")
            ss = [strike(m) for m in (r5.num[0], r5.num[4], r5.den[0])]
            self.play(*[GrowFromCenter(s) for s in ss], run_time=1.2)
            r5.extra += ss

            c.wait_until("real")
            r6 = Row(REAL["num"], REAL["den"], y=ROWY[2])
            self.scroll(self.r3, [r4, r5], r6.eq + r6.num + [r6.bar] + r6.den,
                        min(1.8, c.until("on top", nth=1)))
            self.r4, self.r5, self.r6 = r4, r5, r6
            c.wait_until("on top", nth=1)
            self.play(FlashUnder(grp(r6.num), color=TEAL, time_width=1.5), run_time=2)
            c.wait_until("underneath", nth=1)
            self.play(FlashUnder(grp(r6.den), color=TEAL, time_width=1.5), run_time=2)

    # ------------------------------------------------------------ c2.tanh.3
    def clip3(self):
        with self.say("c2.tanh.3") as c:
            r6 = self.r6
            big = Row(REAL["num"], REAL["den"], lhs=ANS["lhs"], size=48, eqx=0, y=0.4)
            big.shift(LEFT * big.center_x())
            moves = [ReplacementTransform(a, b) for a, b in zip(r6.eq + r6.frac(), big.eq + big.frac())]
            sweep_clear(self, *moves, *appear(*big.lhs, shift=None),
                        keep=[self.card] + r6.eq + r6.frac(), run_time=min(1.6, c.until("ratio")))
            cap = multi([(r"\text{Divide through by }", "F"), (r"\cosh(A)\cosh(B)", "T")], 36)
            cap.move_to([-1.8, 2.55, 0])
            divs = []
            for p, d in ((big.num[0], UP), (big.num[2], UP), (big.den[0], DOWN), (big.den[2], DOWN)):
                divs.append(MathTex(r"\div\cosh A\cosh B", font_size=30, color=GOLD).next_to(p, d, buff=0.18))
            self.play(*appear(cap, shift=None), *appear(*divs, lag=0.15, shift=None),
                      run_time=min(1.5, c.until("ratio")))

            c.wait_until("ratio")
            ans = Row(ANS["num"], ANS["den"], lhs=ANS["lhs"], size=48, eqx=0, y=0.4)
            ans.shift(RIGHT * (big.bar.get_center()[0] - ans.bar.get_center()[0]))
            self.play(*swap(big.num[0], ans.num[0]), *swap(big.num[2], ans.num[2]),
                      *swap(big.num[1], ans.num[1]), run_time=min(1.5, c.until("one")))
            c.wait_until("one")
            self.play(*swap(big.den[0], ans.den[0]), *swap(big.den[2], ans.den[2]),
                      *swap(big.den[1], ans.den[1]), *disappear(*divs),
                      ReplacementTransform(big.bar, ans.bar), run_time=min(1.5, c.until("answer")))

            c.wait_until("answer")
            fin = answer_row(48, 0.4)
            box = answer_box(fin)
            self.play(*disappear(cap),
                      *[a.animate.move_to(b) for a, b in zip(big.lhs + big.eq, fin.lhs + fin.eq)],
                      *[a.animate.move_to(b) for a, b in zip(ans.frac(), fin.frac()) if a is not ans.den[0]],
                      ans.den[0].animate.move_to(fin.den[0]).set_color(TEAL),
                      run_time=1.5)
            self.play(FadeIn(box), run_time=1.0)
            self.ans = big.lhs + big.eq + ans.frac()
            self.box = box

            pred, tag = S5.prediction_shot()      # s5's own prediction (hand-built fraction, YELLOW +)
            pred.scale(0.7)
            tag.next_to(pred, RIGHT, buff=0.5)
            VGroup(pred, tag).move_to([0, -2.55, 0])
            tick = check_mark(GREEN).move_to(tag.get_left() + RIGHT * 0.3)
            self.play(FadeIn(pred, shift=LEFT * 1.5), FadeIn(tag, shift=LEFT * 1.5),
                      run_time=1.2)
            c.wait_until("and underneath")
            self.play(FlashUnder(grp(ans.den), color=TEAL, time_width=1.5), run_time=2)
            c.wait_until("match")

            self.play(*swap(tag, tick), run_time=min(1.0, c.until()))
            self.pred = [pred, tick]

    # ------------------------------------------------------------ c2.tanh.4
    def clip4(self):
        with self.say("c2.tanh.4") as c:
            

            ratio = Row([(r"\sinh(A+B)", "T")], [(r"\cosh(A+B)", "T")], eq=False, eqx=0, y=0.0)
            real = Row(REAL["num"], REAL["den"], eqx=ratio.bar.get_right()[0] + 0.55, y=0.0)
            dx = -VGroup(*[p.copy() for p in ratio.all() + real.all()]).get_center()[0]
            ratio.shift(RIGHT * dx)
            real.shift(RIGHT * dx)

            def list_row(lhs, rhs, under, y):
                ref = MathTex(lhs, "=", rhs, font_size=SZ)
                ref.shift(np.array([under.get_center()[0], y, 0]) - ref[0].get_center())
                return pieces_from(ref, [(lhs, "T"), ("=", "F"), (rhs, "T")], SZ)

            row3 = list_row(r"\sinh(A+B)", r"\sinh A\cosh B + \cosh A\sinh B", ratio.num[0], 1.35)
            row1 = list_row(r"\cosh(A+B)", r"\cosh A\cosh B + \sinh A\sinh B", ratio.den[0], -1.35)
            c.wait_until("family")
            sweep_clear(self, *appear(*row3, lag=0.1, shift=None), keep=[self.card], run_time=1.6)
            self.play(*appear(*row1, lag=0.1, shift=None), run_time=1.0)

            c.wait_until("write")
            self.play(FlashAround(row3[0], color=TEAL, time_width=1.5),
                      FlashAround(row1[0], color=TEAL, time_width=1.5),
                      *appear(ratio.num[0], ratio.bar, ratio.den[0], lag=0, shift=None),
                      run_time=min(1.4, c.until("same")))
            c.wait_until("same")
            same = T("same", 32, GREEN).next_to(real.bar, RIGHT, buff=0.35)
            self.play(*appear(*real.eq, shift=None), *fly(row3[2], VGroup(*real.num)),
                      *fly(row1[2], VGroup(*real.den)), GrowFromCenter(real.bar), run_time=1.5)
            self.play(*appear(same), run_time=1.0)

            c.wait_until("again")
            fin = answer_row(40, -2.45)
            box = answer_box(fin)
            arrow = Arrow([real.bar.get_center()[0], -0.75, 0],
                          [real.bar.get_center()[0], box.get_top()[1] + 0.05, 0],
                          buff=0.05, stroke_width=4, color=GOLD)
            lab = MathTex(r"\div\cosh A\cosh B", font_size=30, color=GOLD).next_to(arrow, RIGHT, buff=0.2)
            self.play(*during(disappear(*row3, *row1), 0, 0.4),
                      *during([GrowArrow(arrow)], 0.35, 0.7),
                      *during(appear(lab, *fin.all(), box, lag=0, shift=None), 0.55, 1.0),
                      run_time=2.0)
            c.wait_until("as before")
            self.play(FlashAround(box, color=YELLOW, time_width=1.5), run_time=1.5)

            c.wait_until("sheet")
            g1 = multi([(r"\text{G1. Express }", "F"), (r"\tanh(x+y)", "T"), (r"\text{ in terms of }", "F"),
                        (r"\tanh x", "T"), (r"\text{ and }", "F"), (r"\tanh y", "T"), (r"\text{.}", "F")], 40)
            g1.move_to([0, 1.0, 0])
            gbox = RoundedRectangle(corner_radius=0.15, width=g1.width + 0.8, height=g1.height + 0.7,
                                    stroke_color=DIM, stroke_width=2).move_to(g1)
            sweep_clear(self, FadeIn(gbox), *appear(g1, shift=None), keep=[self.card, box] + fin.all(), run_time=1.6)
            c.wait_until("with ex")
            maps = MathTex(r"A \mapsto x,", r"\qquad B \mapsto y", font_size=44, color=GOLD)
            maps.move_to([0, -0.2, 0])
            self.play(*appear(maps), run_time=1.0)
            c.wait_until("part seven")
            p7 = T("part 7: a third route", 32, YELLOW).move_to([0, -1.05, 0])
            self.play(*appear(p7), run_time=1.0)
