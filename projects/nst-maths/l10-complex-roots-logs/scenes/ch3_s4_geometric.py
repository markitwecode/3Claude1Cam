"""Chapter 3, scene 4: the geometric series, recalled: formula, the shift-and-subtract proof, the
lambda != 1 flag. Clips c3.geo.1 - c3.geo.3.

Shared: geo_formula() and lam_flag() are imported by ch3_s5_conjugate (top-right corner), s6, s7
and the recap. Keep their names and signatures."""
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


# ---------------------------------------------------------------- shared pieces
def geo_formula(size=48):
    """G = sum_{k=0}^{N-1} a lambda^k = a(1 - lambda^N)/(1 - lambda), every lambda GOLD.
    Parts: [0] G, [1] =, [2] the sigma with limits, [3] a lambda^k, [4] =, [5] the fraction.
    `.denom` = the glyphs of the denominator 1 - lambda (for a flash)."""
    f = MathTex(r"G", r"=", r"\sum_{k=0}^{N-1}", r"a\lambda^k", r"=",
                r"\frac{a(1-\lambda^N)}{1-\lambda}", font_size=size)
    f[3][1].set_color(GOLD)
    f[5][4].set_color(GOLD)
    f[5][10].set_color(GOLD)
    f.denom = VGroup(*f[5][8:11])
    return f


def lam_flag(text=r"\lambda \neq 1"):
    """The small RED flag: a condition in a thin red frame (ch2's tag style). VGroup(box, tex)."""
    tex = MathTex(text, font_size=36, color=RED)
    box = SurroundingRectangle(tex, color=RED, buff=0.16, corner_radius=0.1, stroke_width=2)
    return VGroup(box, tex)


# ---------------------------------------------------------------- this scene's layout
SIZE = 48
TOP_K = 0.6                       # the formula's scale while it sits above the proof
EQ_X = -3.8                       # every row's '=' sits here
COLS = [-3.0, -1.5, 0.0, 1.35, 3.05, 5.05]   # a, a lam, a lam^2, ..., a lam^{N-1}, a lam^N
Y0 = -0.5                         # the G row while the formula is first shown
Y1, Y2, Y3, Y4 = 1.6, 0.35, -0.95, -2.05   # G row, lambda G row, difference, factored
TERMS = [(r"a", None), (r"a\lambda", 1), (r"a\lambda^2", 1), (r"\cdots", None),
         (r"a\lambda^{N-1}", 1), (r"a\lambda^N", 1)]


def term(k, y):
    tex, lam = TERMS[k]
    m = MathTex(tex, font_size=SIZE)
    if lam is not None:
        m[0][lam].set_color(GOLD)
    m.shift(np.array([COLS[k], y, 0]) - (m.get_center() if k == 3 else
                                          np.array([m.get_center()[0], m[0][0].get_center()[1], 0])))
    return m


def plus(x, y):
    return MathTex("+", font_size=SIZE).move_to([x, y, 0])


def lhs(tex, y, lam=None):
    m = MathTex(tex, font_size=SIZE)
    if lam is not None:
        m[0][lam].set_color(GOLD)
    m.shift(np.array([EQ_X, y, 0]) - m[0][-1].get_center())
    return m


def row(ks, y):
    """Terms at columns ks with a '+' midway between neighbours."""
    ts = [term(k, y) for k in ks]
    ps = [plus((ts[i].get_right()[0] + ts[i + 1].get_left()[0]) / 2, y) for i in range(len(ts) - 1)]
    return ts, ps


def diff_line():
    """G - lambda G = a - a lambda^N, its '=' at EQ_X, on Y3. Parts: lhs, =, a, -, a lambda^N."""
    m = MathTex(r"G-\lambda G", r"=", r"a", r"-", r"a\lambda^N", font_size=SIZE)
    m[0][2].set_color(GOLD)
    m[4][1].set_color(GOLD)
    m.shift(np.array([EQ_X, Y3, 0]) - m[1].get_center())
    return m


def factored_line():
    m = MathTex(r"G(1-\lambda)=a(1-\lambda^N)", font_size=SIZE)
    m[0][4].set_color(GOLD)
    m[0][11].set_color(GOLD)
    m.shift(np.array([EQ_X, Y4, 0]) - m[0][6].get_center())
    return m


def _meet(a, b, pad=0.06):
    return not (a.get_right()[0] + pad < b.get_left()[0] or b.get_right()[0] + pad < a.get_left()[0]
                or a.get_top()[1] + pad < b.get_bottom()[1] or b.get_top()[1] + pad < a.get_bottom()[1])


class Slide(Animation):
    """A copy of `src` travels to `dst` (scaled to its height, along an arc): invisible while it still
    touches src, gone (fade 0.45-0.65) before dst fades in there. Pair with slid_in(dst)."""

    def __init__(self, src, dst, arc=0.0, y_clear=None, **kw):
        self.start_copy = src.copy()
        self.y_clear = src.get_bottom()[1] if y_clear is None else y_clear   # visible only below this
        self.p0, self.p1 = src.get_center(), dst.get_center()
        self.s1 = dst.height / max(src.height, 1e-6)
        self.path = path_along_arc(arc)
        kw.setdefault("run_time", 1.5)
        super().__init__(src.copy(), remover=True, introducer=True, **kw)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        m = self.mobject.become(self.start_copy)
        m.scale(1 + (self.s1 - 1) * a).move_to(self.path(np.array([self.p0]), np.array([self.p1]), a)[0])
        k = 0.0 if _meet(m, self.start_copy) or m.get_top()[1] > self.y_clear - 0.05 else 1.0
        k *= 1 - smooth(float(np.clip((alpha - 0.45) / 0.2, 0, 1)))
        m.set_opacity(k)


def slid_in(dst):
    return during([FadeIn(dst)], 0.7, 1.0)


class Ch3S4Geometric(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------- c3.geo.1: the progression, the formula
        with self.say("c3.geo.1") as c:
            lhs1 = lhs(r"G=", Y0)
            t1, p1 = row([0, 1, 2, 3, 4], Y0)
            items = [lhs1]
            for i, t in enumerate(t1):
                items.append(t)
                if i < len(p1):
                    items.append(p1[i])
            self.play(*appear(*items, lag=0.12, shift=None), run_time=min(1.8, c.until("setup")))
            c.wait_until("setup")

            brace = Brace(VGroup(*t1), UP, buff=0.15, color=DIM)
            n_lab = T("N terms", size=32, color=FG).next_to(brace, UP, buff=0.12)
            c.wait_until(own_word=n_lab)
            self.play(GrowFromCenter(brace), *appear(n_lab), run_time=0.9)
            first = T("first term", size=32, color=FG).next_to(t1[0], DOWN, buff=0.45)
            first.align_to(t1[0], RIGHT).shift(0.15 * RIGHT)
            c.wait_until(own_word=first)
            self.play(*appear(first), run_time=0.9)
            ratio = T("common ratio", size=32, color=GOLD).next_to(t1[1][0][1], DOWN, buff=0.45)
            ratio.align_to(t1[1][0][1], LEFT).shift(0.1 * LEFT)
            c.wait_until(own_word=ratio)
            self.play(*appear(ratio), run_time=0.9)
            c.wait_until("formula")

            formula = geo_formula(56).move_to([0, 2.45, 0])
            self.play(*appear(formula, shift=None), run_time=1.4)
            c.wait_until()

        # ---------------------------------------------------------- c3.geo.2: shift, subtract, divide
        with self.say("c3.geo.2") as c:
            up = (Y1 - Y0) * UP
            self.play(*during(disappear(brace, n_lab, first, ratio), 0, 0.4),
                      *during([formula.animate.scale(TOP_K).move_to([0, 2.95, 0]),
                               *[m.animate.shift(up) for m in items]], 0.3, 1),
                      run_time=min(1.8, c.until("shift")))
            c.wait_until("shift")

            lhs2 = lhs(r"\lambda G=", Y2, lam=0)
            t2, p2 = row([1, 2, 3, 4, 5], Y2)
            flies = []
            for k in range(5):
                flies.append(AnimationGroup(Slide(t1[k], t2[k], arc=0.0, y_clear=Y1 - 0.3), *slid_in(t2[k])))
            self.play(*appear(lhs2, shift=None), LaggedStart(*flies, lag_ratio=0.15),
                      run_time=min(2.2, c.until("subtract")))
            self.play(*appear(*p2, shift=None, lag=0.1), run_time=0.6)
            c.wait_until("subtract")

            minus = MathTex("-", font_size=SIZE).next_to(lhs2, LEFT, buff=0.35)
            rule = Line([-5.7, (Y2 + Y3) / 2 + 0.05, 0], [5.7, (Y2 + Y3) / 2 + 0.05, 0]).set_stroke(DIM, 3)
            self.play(*appear(minus, shift=None), Create(rule), run_time=0.8)
            strikes = []
            for k in range(1, 5):
                for t in (t1[k], t2[k - 1]):
                    strikes.append(Line(t.get_corner(DL) + 0.06 * (DL), t.get_corner(UR) + 0.06 * UR)
                                   .set_stroke(RED, 4))
            self.play(LaggedStart(*[Create(s) for s in strikes], lag_ratio=0.15),
                      run_time=min(1.8, c.until("only the first term")))
            c.wait_until("only the first term")

            struck = [t1[k] for k in range(1, 5)] + [t2[k] for k in range(4)] + p1 + p2 + strikes
            self.play(*set_alpha(struck, DIMMED), *flash([t1[0], t2[4]]), run_time=1.0)

            d = diff_line()
            dx = COLS[5] - d[4].get_x()
            d[3].shift(dx * RIGHT)
            d[4].shift(dx * RIGHT)
            self.play(Slide(t1[0], d[2]), *slid_in(d[2]), Slide(t2[4], d[4]), *slid_in(d[4]),
                      *appear(d[0], d[1], d[3], shift=None, lag=0), run_time=1.5)
            self.play(d[3].animate.shift(dx * LEFT), d[4].animate.shift(dx * LEFT), run_time=0.8)
            settle(self, d)
            c.wait_until("divide")

            f2 = factored_line()
            self.play(Slide(d, f2), *slid_in(f2), run_time=min(1.6, c.until("complex")))
            self.play(FlashAround(formula, run_time=1.2, time_width=1.5),
                      run_time=min(1.2, c.until("complex")))
            c.wait_until("complex")

            tag_t = T("λ can be complex: only + and × were used", size=32, color=YELLOW,
                      t2c={"λ": GOLD})
            tag_b = SurroundingRectangle(tag_t, color=YELLOW, buff=0.18, stroke_width=2, corner_radius=0.1)
            tag = VGroup(tag_b, tag_t)
            eg = MathTex(r"\lambda = e^{i\theta}", font_size=44, color=GOLD)
            VGroup(tag, eg).arrange(RIGHT, buff=0.6).move_to([0, -3.15, 0])
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("complex ratio")
            self.play(*appear(eg), run_time=1.0)
            c.wait_until()

        # ---------------------------------------------------------- c3.geo.3: the one condition
        with self.say("c3.geo.3") as c:
            self.play(FlashAround(formula.denom, run_time=1.6, time_width=1.5, color=YELLOW), run_time=1.6)
            c.wait_until("one")
            rest = [m for m in self.mobjects if m is not formula]
            self.play(*during([FadeOut(m) for m in rest], 0, 0.45),
                      *during([formula.animate.scale(1 / TOP_K).move_to([-0.85, 0.2, 0])], 0.45, 1),
                      run_time=1.0)

            flag = lam_flag().next_to(formula, RIGHT, buff=0.6)
            self.play(*appear(flag), run_time=0.8)
            c.wait_until("keep")

            f_t = formula.copy().scale(0.72).to_corner(UR, buff=0.5)
            fl_t = flag.copy().scale(0.86).next_to(f_t, DOWN, buff=0.25).align_to(f_t, RIGHT)
            self.play(formula.animate.become(f_t), flag.animate.become(fl_t),
                      run_time=min(1.5, c.until()))
            c.wait_until()

        self.wait(0.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
