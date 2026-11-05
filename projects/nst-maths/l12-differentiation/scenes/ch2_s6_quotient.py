"""Chapter 2, scene 6: the quotient rule from the product and chain rules, Example 39, tan and tanh.
Clips c2.quot.1 – c2.quot.4.

Exports (for ch2 s7, the recap):
  quotient_box()  -> VGroup(rect, formula, num, tag) centred at ORIGIN, as s5's product_box(): (107)
                     boxed YELLOW, `\\frac{d}{dx}\\left(\\frac{u}{v}\\right) = \\frac{v\\,\\frac{du}{dx} -
                     u\\,\\frac{dv}{dx}}{v^2}` (MathTex 44, u BLUE, v PURPLE), .num "(107)" DIM 28 above its
                     top-right corner, .tag "quotient rule" (T 32, YELLOW) under it. .formula.parts[i] =
                     glyphs of element i of [d/dx(u/v), =, the fraction].
  split_line(size=56) -> MathTex `\\frac{u}{v} = u \\times \\left(\\frac{1}{v}\\right)` (u BLUE, v PURPLE),
                     .parts = [u/v, =, u, ×, (1/v)].
"""
# style: 2
import re
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

UV = {"u": BLUE, "v": PURPLE}
FG_ = {"f'": GREEN, "g'": GREEN, "f": BLUE, "g": PURPLE}
TQ = {r"\sin^2 x": BLUE, r"\cos^2 x": PURPLE, r"\sin x": BLUE, r"\cos x": PURPLE}
TH = {r"\sinh^2 x": BLUE, r"\cosh^2 x": PURPLE}


def _args(s, cmap):
    """Split tex `s` so every cmap key is its own arg; returns [(tex, colour)]."""
    if not cmap:
        return [(s, FG)]
    keys = sorted(cmap, key=len, reverse=True)
    tok = re.compile("|".join(re.escape(k) for k in keys) + r"|\\[A-Za-z]+|.", re.S)
    out, cur = [], ""
    for t in tok.findall(s):
        if t in cmap:
            if cur.strip():
                out.append((cur, FG))
            cur = ""
            out.append((t, cmap[t]))
        else:
            cur += t
    if cur.strip():
        out.append((cur, FG))
    return out


def M(elems, size=44, cmap=UV):
    """MathTex from elements (str, auto-coloured by cmap, or (tex, colour)); `.parts[i]` = element i."""
    args, spans = [], []
    for e in elems:
        a = [e] if isinstance(e, tuple) else _args(e, cmap)
        spans.append((len(args), len(args) + len(a)))
        args += a
    m = MathTex(*[a for a, _ in args], font_size=size)
    for i, (_, col) in enumerate(args):
        m[i].set_color(col)
    m.parts = [VGroup(*m[i:j]) for i, j in spans]
    return m


def glyphs(mob):
    return [g for g in mob.family_members_with_points()]


def frac(num, den, pad=0.08):
    bar = Line(LEFT, RIGHT, stroke_width=2.6, color=FG)
    bar.set_width(max(num.width, den.width) + 2 * pad)
    num.next_to(bar, UP, buff=0.12)
    den.next_to(bar, DOWN, buff=0.12)
    g = VGroup(num, bar, den)
    g.num, g.bar, g.den = num, bar, den
    return g


LHS = r"\frac{d}{dx}\left(\frac{u}{v}\right)"
QFRAC = r"\frac{v\,\frac{du}{dx} - u\,\frac{dv}{dx}}{v^2}"


def split_line(size=56):
    return M([r"\frac{u}{v}", "=", "u", r"\times", r"\left(\frac{1}{v}\right)"], size)


def quotient_box(size=44):
    f = M([LHS, "=", QFRAC], size)
    f.move_to(ORIGIN)
    pad = 0.38
    rect = Rectangle(width=f.width + 2 * pad, height=f.height + 2 * pad, color=YELLOW, stroke_width=3)
    rect.move_to(f)
    num = T("(107)", 28, DIM).next_to(rect.get_corner(UR), UP, buff=0.1).align_to(rect, RIGHT)
    tag = T("quotient rule", 32, YELLOW).next_to(rect, DOWN, buff=0.22)
    g = VGroup(rect, f, num, tag)
    g.rect, g.formula, g.num, g.tag = rect, f, num, tag
    g.shift(-rect.get_center())
    return g


def frac_pieces(part):
    """Glyphs of a fraction v du/dx - u dv/dx over v^2: (left term, right term, denominator)."""
    gs = glyphs(part)
    bar = max(gs, key=lambda g: g.width)
    y = bar.get_y()
    num = [g for g in gs if g is not bar and g.get_y() > y]
    den = [g for g in gs if g.get_y() < y]
    flats = sorted([g for g in num if g.height < 0.08], key=lambda g: g.get_x())
    mx = flats[len(flats) // 2].get_x()
    left = [g for g in num if g.get_x() < mx - 0.02]
    right = [g for g in num if g.get_x() > mx + 0.02]
    return left, right, den


def hl(gs, color=YELLOW):
    g = VGroup(*gs)
    return token_box(gs, g, color=color, height=g.height + 0.24)


def rt(c, want, nxt=None, frac_=0.9, nth=0):
    return max(0.3, min(want, frac_ * c.until(nxt, nth=nth)))


X0 = -6.3


class QuotientScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ setup, split, apply
    def clip1(self):
        F0 = M([r"\frac{u}{v}"], 110)
        nl = T("new limit?", 48, YELLOW)
        VGroup(F0, nl).arrange(RIGHT, buff=1.2).move_to(0.3 * UP + 0.6 * RIGHT)
        u, v = F0[1], F0[3]
        lab_t = T("top", 34, BLUE).next_to(F0, LEFT, buff=0.45).set_y(u.get_y())
        lab_b = T("bottom", 34, PURPLE).next_to(F0, LEFT, buff=0.45).set_y(v.get_y())
        strike = Line(nl.get_left() + 0.15 * LEFT, nl.get_right() + 0.15 * RIGHT).set_stroke(RED, 6)

        S = self.split = split_line()
        S.move_to([0, 2.6, 0]).align_to([X0, 0, 0], LEFT)

        with self.say("c2.quot.1") as c:
            self.play(*appear(F0, shift=None), run_time=1.0)
            c.wait_until(own_word=nl)
            self.play(*appear(nl), run_time=0.9)
            self.play(*appear(lab_t, lab_b, lag=0.4), run_time=rt(c, 1.0, "No"))  # early: the fraction's two parts, named in the next line
            c.wait_until("No")
            self.play(Create(strike), run_time=0.8)
            c.wait_until("times one over the bottom")
            k = S.parts[0].height / F0.height
            self.play(*during(disappear(nl, strike, lab_t, lab_b), 0, 0.45),
                      *during([F0.animate.scale(k).move_to(S.parts[0])], 0.2, 0.8),
                      *during(appear(*S.parts[1:], lag=0.15), 0.5, 1),
                      run_time=rt(c, 1.8, "apply"))
            self.remove(F0)
            self.remove(*S.get_family())
            self.add(S)

            c.wait_until("apply")
            PB = self.pb = load_scene("ch2_s5_product").product_box().scale(0.5).to_corner(UR, buff=0.45)
            self.play(*appear(PB, shift=None), run_time=0.8)
            self.play(FlashAround(PB.tag, run_time=1.5, time_width=1.5))

            D = self.d1 = M([LHS, "=", r"\frac{du}{dx}", r"\times", r"\left(\frac{1}{v}\right)",
                             "+", "u", r"\,\frac{d}{dx}\left(\frac{1}{v}\right)"], 50)
            D.move_to([0, 0.0, 0]).align_to([X0, 0, 0], LEFT)
            c.wait_until("derivative of the top")
            self.play(*appear(*D.parts[0:2], *D.parts[2:5], lag=0.3), run_time=rt(c, 1.6, "plus the top"))
            c.wait_until("plus the top")
            self.play(*appear(*D.parts[5:8], lag=0.3), run_time=rt(c, 1.5))
            self.remove(*D.get_family())
            self.add(D)

    # ------------------------------------------------------------------ chain aside, common, (107)
    def clip2(self):
        D, PB = self.d1, self.pb
        A = M([r"\frac{d}{dx}\left(\frac{1}{v}\right)", "=", r"\frac{d}{dv}\left(\frac{1}{v}\right)",
               r"\frac{dv}{dx}", "=", r"-\frac{1}{v^2}", r"\,\frac{dv}{dx}"], 46)
        A.move_to([0, -2.2, 0]).align_to([X0, 0, 0], LEFT)
        CB = load_scene("ch2_s3_chain").chain_box()
        CB.scale(PB.rect.width / CB.rect.width)
        CB.next_to(PB, DOWN, buff=0.3).align_to(PB, RIGHT)

        with self.say("c2.quot.2") as c:
            self.play(*fly(D.parts[7], A.parts[0], arc=1.4), run_time=rt(c, 1.6, "chain rule"))
            c.wait_until("chain rule")
            self.play(*appear(CB, shift=None), run_time=0.8)
            self.play(FlashAround(CB.tag, run_time=1.5, time_width=1.5))
            c.wait_until("outer function")
            self.play(*appear(*A.parts[1:3], lag=0.3), run_time=rt(c, 1.4, "minus one over"))
            c.wait_until("minus one over")
            self.play(*appear(*A.parts[4:6], lag=0.3), run_time=rt(c, 1.4, "inner"))
            c.wait_until("inner")
            self.play(*appear(A.parts[3], A.parts[6], lag=0.4), run_time=1.2)
            self.play(*flash([A.parts[3], A.parts[6]]), run_time=1.5)

            # the aside slots back into the line
            D2 = M([LHS, "=", r"\frac{du}{dx}", r"\times", r"\left(\frac{1}{v}\right)",
                    "+", "u", r"\left(", r"-\frac{1}{v^2}", r"\,\frac{dv}{dx}", r"\right)"], 50)
            D2.shift(D.parts[0].get_center() - D2.parts[0].get_center())
            r = 50 / 46
            moves = []
            for src, dst in ((A.parts[5], D2.parts[8]), (A.parts[6], D2.parts[9])):
                for g, h in zip(glyphs(src), glyphs(dst)):
                    moves.append(g.animate.scale(r).move_to(h))
            c.wait_until("common")
            self.play(*during(disappear(D.parts[7], *A.parts[0:5]), 0, 0.4),
                      *during(moves, 0.3, 0.85),
                      *during(appear(D2.parts[7], D2.parts[10], shift=None), 0.8, 1),
                      run_time=rt(c, 1.4, "the bottom squared"))
            self.remove(*D.get_family(), *D2.get_family(), *A.get_family())
            self.add(D2)

            # both terms over v^2: the line becomes the quotient rule
            Q = M([LHS, "=", QFRAC], 50)
            Q.shift(D2.parts[0].get_center() - Q.parts[0].get_center())
            c.wait_until("squared")
            self.play(*during(disappear(*D2.parts[2:11]), 0, 0.45),
                      *during(appear(Q.parts[2], shift=None), 0.5, 1), run_time=rt(c, 1.4, "result"))
            self.remove(*D2.get_family(), *Q.get_family())
            self.add(Q)

            c.wait_until("result")
            QB = quotient_box().scale(1.3).move_to(0.2 * UP)
            k = QB.formula.width / Q.width
            self.play(*disappear(PB, CB, self.split),
                      *during([Q.animate.scale(k).move_to(QB.formula)], 0.15, 0.7),
                      *during([GrowFromCenter(QB.rect)], 0.6, 1),
                      *during(appear(QB.num, QB.tag), 0.65, 1),
                      run_time=rt(c, 2.0, "the bottom, times"))
            self.remove(Q)
            self.remove(*QB.get_family())
            self.add(QB)
            left, right, den = frac_pieces(QB.formula.parts[2])
            c.wait_until("times the derivative of the top")
            box = hl(left)
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("minus the top")
            self.play(Transform(box, hl(right)), run_time=0.8)
            c.wait_until("all over")
            self.play(Transform(box, hl(den)), run_time=0.8)
            self.play(FadeOut(box), run_time=rt(c, 0.8))
            self.qb = QB

    # ------------------------------------------------------------------ Example 39
    def clip3(self):
        title = T("Example 39: Quotient rule", 44).to_corner(UL, buff=0.5)
        Y = M(["y", "=", r"\frac{", (r"\sin x", BLUE), "}{", ("x", PURPLE), "}"], 56)
        Y.move_to([0, 2.3, 0])
        tag = MathTex(r"x \neq 0", font_size=40, color=DIM).next_to(Y, RIGHT, buff=0.9)

        L1 = M([r"\frac{dy}{dx}", "=", r"\frac{f'g - fg'}{g^2}"], 40, FG_)
        L1.move_to([0, 0.75, 0]).align_to([-6.4, 0, 0], LEFT)
        L2 = M(["=", r"\frac{", (r"(\cos x)", GREEN), r"\,", ("x", PURPLE), "-", (r"(\sin x)", BLUE),
                ("(1)", GREEN), "}{", ("x^2", PURPLE), "}"], 40)
        L3 = M(["=", r"\frac{x\cos x - \sin x}{x^2}"], 40, {})
        for L, y in ((L2, -0.6), (L3, -1.95)):
            L.set_y(y)
            L.shift((L1.parts[1].get_x() - L.parts[0].get_x()) * RIGHT)

        R1 = M(["y", "=", (r"\sin x", BLUE), r"\cdot", (r"\frac{1}{x}", PURPLE)], 40)
        R1.move_to([0, 0.75, 0]).align_to([0.2, 0, 0], LEFT)
        R2 = M([r"\frac{dy}{dx}", "=", (r"(\cos x)", GREEN), (r"\left(\frac{1}{x}\right)", PURPLE), "+",
                (r"(\sin x)", BLUE), (r"\left(-\frac{1}{x^2}\right)", GREEN)], 40)
        R2.move_to([0, -0.6, 0]).align_to([0.2, 0, 0], LEFT)
        R3 = M([r"\frac{x\cos x - \sin x}{x^2}"], 40, {})
        R3.move_to([0, -1.95, 0])
        eq = MathTex("=", font_size=60, color=GREEN)

        with self.say("c2.quot.3") as c:
            sweep_clear(self, *appear(title, shift=None), run_time=1.4)  # early: card title
            self.play(*appear(Y, shift=None), run_time=rt(c, 1.0, "different from zero"))
            c.wait_until("different from zero")
            self.play(*appear(tag), run_time=1.0)

            c.wait_until("quot")
            self.play(*appear(L1, L2, lag=0.5), run_time=rt(c, 1.8, "ex times cosine"))
            c.wait_until("ex times cosine")
            self.play(*appear(L3), run_time=1.2)

            c.wait_until("prod")
            self.play(*appear(R1), run_time=1.2)
            c.wait_until("That gives")
            self.play(*appear(*R2.parts[0:4], lag=0.2), run_time=1.4)
            c.wait_until("minus sine")
            self.play(*appear(*R2.parts[4:7], lag=0.2), run_time=rt(c, 1.4, "same"))
            self.remove(*R2.get_family())
            self.add(R2)

            c.wait_until("same")
            R3.set_x(R2.parts[2].get_left()[0] + 0.5 * (R2.get_right()[0] - R2.parts[2].get_left()[0]))
            self.play(*appear(R3), run_time=rt(c, 1.4, "same answer"))
            eq.move_to([(L3.get_right()[0] + R3.get_left()[0]) / 2, L3.parts[0].get_y(), 0])
            c.wait_until("same answer")
            self.play(*appear(eq, shift=None), FlashAround(VGroup(L3.parts[1]), color=GREEN),
                      FlashAround(R3, color=GREEN), run_time=1.5)

            def tile(s, col):
                t = T(s, 30)
                r = RoundedRectangle(corner_radius=0.15, width=t.width + 0.5, height=0.65).set_stroke(col, 2.5)
                return VGroup(r.move_to(t), t)
            t1, t2, t3 = tile("product rule", YELLOW), tile("chain rule", YELLOW), tile("quotient rule", DIM)
            plus = MathTex("+", font_size=40)
            arr = MathTex(r"\Rightarrow", font_size=40)
            row = VGroup(t1, plus, t2, arr, t3).arrange(RIGHT, buff=0.3).move_to([0, -3.0, 0])
            c.wait_until("forget")
            self.play(*appear(t1, plus, t2, arr, t3, lag=0.35), run_time=rt(c, 2.0))  # early: rule tiles

    # ------------------------------------------------------------------ tan, tanh, constants
    def clip4(self):
        tb = load_scene("ch2_s2_table")
        card = tb.table_card()
        card.scale_to_fit_height(6.8).to_edge(RIGHT, buff=0.45).set_y(0)
        for b in card.blocks[:2]:
            b.set_opacity(0.4)

        Z = 42
        A = M([r"\frac{d}{dx}\tan x", "=", r"\frac{d}{dx}\frac{\sin x}{\cos x}"], Z, TQ)
        A.move_to([0, 2.75, 0]).align_to([-6.5, 0, 0], LEFT)
        ex = A.parts[1].get_x()
        B = M(["=", r"\frac{\cos x\cos x - \sin x(-\sin x)}{\cos^2 x}"], Z, TQ)
        B.set_y(1.25).shift((ex - B.parts[0].get_x()) * RIGHT)

        Ceq = MathTex("=", font_size=Z)
        Cf = frac(M([r"\cos^2 x + \sin^2 x"], Z, TQ), M([r"\cos^2 x"], Z, TQ))
        Ceq.next_to(Cf, LEFT, buff=0.2).set_y(Cf.bar.get_y())
        C = VGroup(Ceq, Cf)
        C.shift([ex - Ceq.get_x(), -0.25 - Cf.bar.get_y(), 0])

        one = M([("1", YELLOW)], Z)
        Cf2 = frac(one, Cf.den.copy())
        Cf2.next_to(Ceq, RIGHT, buff=0.2)
        Cf2.shift((Cf.bar.get_y() - Cf2.bar.get_y()) * UP)
        tail = M(["=", r"\sec^2 x"], Z, {}).next_to(Cf2, RIGHT, buff=0.2)
        tail.shift((Cf2.bar.get_y() - tail.parts[0].get_y()) * UP)

        Dt = M([r"\frac{d}{dx}\tanh x", "=", r"\frac{\cosh^2 x - \sinh^2 x}{\cosh^2 x}", "=",
                r"\mathrm{sech}^2 x"], Z, TH)
        Dt.move_to([0, -0.7, 0]).align_to([-6.5, 0, 0], LEFT)
        gs = glyphs(Dt.parts[2])
        bar = max(gs, key=lambda g: g.width)
        dnum = [g for g in gs if g.get_y() > bar.get_y() + 0.05]

        E = M([r"\frac{d}{dx}\tan(", ("a", YELLOW), "x)", "=", ("a", YELLOW), r"\sec^2(", ("a", YELLOW), "x)"],
              Z, {})
        E.move_to([0, -2.4, 0]).align_to([-6.5, 0, 0], LEFT)

        with self.say("c2.quot.4") as c:
            sweep_clear(self, FadeIn(card), run_time=rt(c, 1.6, "tanq"))
            c.wait_until("tanq")
            self.play(*appear(A, shift=None), run_time=1.2)
            c.wait_until("so the quotient rule")
            self.play(*appear(B, shift=None), run_time=rt(c, 1.2, "cosine squared"))
            c.wait_until("cosine squared")
            self.play(*appear(C, shift=None), run_time=1.2)

            c.wait_until("sec")
            self.play(*recolor(glyphs(Cf.num), YELLOW), run_time=1.0)
            c.wait_until("one over cosine squared")
            self.play(*during(disappear(Cf.num), 0, 0.45),
                      *during([Transform(Cf.bar, Cf2.bar), Cf.den.animate.move_to(Cf2.den)], 0.2, 0.8),
                      *during(appear(one, shift=None), 0.55, 1),
                      run_time=rt(c, 1.6, "secant squared"))
            c.wait_until("secant squared")
            self.play(*appear(tail, shift=None), run_time=1.0)

            c.wait_until("tanh")
            up = (B.parts[0].get_y() - Cf2.bar.get_y()) * UP
            self.play(*during(disappear(B), 0, 0.4),
                      *during([m.animate.shift(up) for m in (Ceq, Cf.bar, Cf.den, one, tail)], 0.4, 1),
                      run_time=1.2)
            self.play(*appear(*Dt.parts[0:3], lag=0.3), run_time=1.5)
            c.wait_until("also one")
            self.play(*recolor(dnum, YELLOW), run_time=1.0)
            c.wait_until("hyperbolic")
            self.play(*appear(*Dt.parts[3:5], lag=0.3), run_time=rt(c, 1.2, "const"))
            self.remove(*Dt.get_family())
            self.add(Dt)

            c.wait_until("const")
            self.play(*appear(E, shift=None), *during([FadeIn(tb.row_glow(card, 7)), FadeIn(tb.row_glow(card, 8))],
                                                      0.4, 1), run_time=rt(c, 1.6))
