"""Chapter 2, scene 5: the product rule from first principles, its rectangle, Example 38.
Clips c2.prod.1 – c2.prod.5.

Exports (for ch2 s7 and the recap):
  product_box()      -> VGroup(rect, formula, num, tag) centred at ORIGIN: (106) boxed YELLOW,
                        `\\frac{d}{dx}(fg) = \\frac{df}{dx}\\,g + f\\,\\frac{dg}{dx}` (MathTex 44, f BLUE,
                        g PURPLE), .num "(106)" DIM 28 above its top-right corner, .tag "product rule"
                        (T 32, YELLOW, buff 0.22) under it, as s3's chain-rule tag. .formula.parts[i] = glyphs of element i of
                        [d/dx(fg), =, df/dx g, +, f dg/dx]; .term1 / .term2 = parts 2 / 4.
  framed_numerator() -> VGroup: the notes' second line `= lim_{h->0} (f(x+h)g(x+h) - f(x+h)g(x)
                        + f(x+h)g(x) - f(x)g(x)) / h`, the middle pair framed YELLOW (.frame), as
                        placed here (row centred, y = -0.1).
  strips_picture()   -> VGroup: the area-fg rectangle (BLUE base f, PURPLE side g), its TEAL δf / δg
                        edges and the two light TEAL strips with labels g δf, f δg (no corner), as
                        placed here (lower right).
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

SZ = 40                       # derivation rows
TOK = re.compile(r"\\delta [fg]|\\[A-Za-z]+|[fgh]'*|.", re.S)


def _args(s):
    out, cur = [], ""
    for t in TOK.findall(s):
        if re.fullmatch(r"\\delta [fg]|[fgh]'*", t):
            if cur.strip():
                out.append(cur)
            cur = ""
            out.append(t)
        else:
            cur += t
    if cur.strip():
        out.append(cur)
    return out


def _col(a):
    if a.startswith(r"\delta"):
        return TEAL
    if a[0] in "fgh" and a.endswith("'"):
        return GREEN
    return {"f": BLUE, "g": PURPLE, "h": TEAL}.get(a, FG)


def M(s, size=SZ):
    """MathTex with f BLUE, g PURPLE, h TEAL, f'/g' GREEN, δf/δg TEAL. A list: one element per part,
    `.parts[i]` = that element's glyphs."""
    elems = s if isinstance(s, (list, tuple)) else [s]
    args, spans = [], []
    for e in elems:
        a = _args(e)
        spans.append((len(args), len(args) + len(a)))
        args += a
    m = MathTex(*args, font_size=size)
    for i, a in enumerate(args):
        m[i].set_color(_col(a))
    m.parts = [VGroup(*m[i:j]) for i, j in spans]
    return m


def frac(num, den, pad=0.08):
    bar = Line(LEFT, RIGHT, stroke_width=2.6, color=FG)
    bar.set_width(max(num.width, den.width) + 2 * pad)
    num.next_to(bar, UP, buff=0.1)
    den.next_to(bar, DOWN, buff=0.1)
    g = VGroup(num, bar, den)
    g.num, g.bar, g.den = num, bar, den
    return g


def lay(items, y=0.0, x=None):
    """items: (mob, ref, gap_before). Left to right, each ref's centre on height y; centred on x."""
    cur = 0.0
    for i, (m, ref, gap) in enumerate(items):
        cur += gap if i else 0
        m.shift((cur - m.get_left()[0]) * RIGHT + (y - ref.get_center()[1]) * UP)
        cur = m.get_right()[0]
    g = VGroup(*[m for m, _, _ in items])
    if x is not None:
        g.shift((x - g.get_center()[0]) * RIGHT)
    return g


P, OP, EQ = 0.03, 0.12, 0.16   # gaps: product, binary operator, relation / lim


def _lim():
    m = M(r"\lim_{h \to 0}")
    return m, m[0]


# ---------- the derivation rows ----------

ROW1_Y, ROW2_Y, ROW3_Y = 2.0, -0.1, -2.3


def row1():
    a = M(r"\frac{dy}{dx} = \frac{d}{dx}(fg) =")
    lim, lref = _lim()
    nf, ng, nm, nf2, ng2 = M("f(x+h)"), M("g(x+h)"), M("-"), M("f(x)"), M("g(x)")
    num = lay([(nf, nf, 0), (ng, ng, P), (nm, nm, OP), (nf2, nf2, OP), (ng2, ng2, P)])
    fr = frac(num, M("h"))
    r = lay([(a, a, 0), (lim, lref, EQ), (fr, fr.bar, EQ)], ROW1_Y, 0)
    r.a, r.lim, r.fr = a, lim, fr
    r.nf, r.ng, r.nm, r.nf2, r.ng2 = nf, ng, nm, nf2, ng2
    return r


def row2():
    eq = M("=")
    lim, lref = _lim()
    at = [M("f(x+h)"), M("g(x+h)"), M("-"), M("f(x+h)"), M("g(x)"),
          M("+"), M("f(x+h)"), M("g(x)"), M("-"), M("f(x)"), M("g(x)")]
    gaps = [0, P, OP, OP, P, OP, OP, P, OP, OP, P]
    num = lay([(m, m, g) for m, g in zip(at, gaps)])
    fr = frac(num, M("h"))
    r = lay([(eq, eq, 0), (lim, lref, EQ), (fr, fr.bar, EQ)], ROW2_Y, 0)
    r.eq, r.lim, r.fr, r.at = eq, lim, fr, at
    r.T1, r.T2, r.T3, r.T4 = at[0:2], at[2:5], at[5:8], at[8:11]
    r.frame = SurroundingRectangle(VGroup(*at[2:8]), color=YELLOW, buff=0.07, stroke_width=3)
    return r


def row3():
    eq = M("=")
    lim, lref = _lim()
    lb, rb = MathTex(r"\Bigg[", font_size=SZ), MathTex(r"\Bigg]", font_size=SZ)
    F = M("f(x+h)")
    gn = lay([(m, m, g) for m, g in ((M("g(x+h)"), 0), (M("-"), OP), (M("g(x)"), OP))])
    gq = frac(gn, M("h"))
    plus = M("+")
    fn = lay([(m, m, g) for m, g in ((M("f(x+h)"), 0), (M("-"), OP), (M("f(x)"), OP))])
    fq = frac(fn, M("h"))
    G = M("g(x)")
    r = lay([(eq, eq, 0), (lim, lref, EQ), (lb, lb, 0.1), (F, F, 0.05), (gq, gq.bar, 0.1),
             (plus, plus, OP), (fq, fq.bar, OP), (G, G, 0.1), (rb, rb, 0.05)], ROW3_Y, 0)
    r.eq, r.lim, r.lb, r.rb, r.F, r.gq, r.plus, r.fq, r.G = eq, lim, lb, rb, F, gq, plus, fq, G
    return r


ROW3_UP = 2.6                  # row 3 once the board clears (c2.prod.3)
ROW4_Y = 0.4


R4 = 52


def row4():
    F = M("f(x)", R4)
    gp, plus, fp, G = M("g'(x)", R4), M("+", R4), M("f'(x)", R4), M("g(x)", R4)
    res = M(r"= f'g + fg'", R4)
    r = lay([(F, F, 0), (gp, gp, 0.06), (plus, plus, OP), (fp, fp, OP), (G, G, 0.06), (res, res, 0.25)],
            ROW4_Y, 0)
    Fa = M("f(x+h)", R4).move_to(F).align_to(F, RIGHT)
    r.F, r.gp, r.plus, r.fp, r.G, r.res, r.Fa = F, gp, plus, fp, G, res, Fa
    return r


def framed_numerator():
    r = row2()
    return VGroup(r, r.frame)


# ---------- (106) ----------

def product_box(size=44):
    f = M([r"\frac{d}{dx}(fg)", "=", r"\frac{df}{dx}\,g", "+", r"f\,\frac{dg}{dx}"], size)
    f.move_to(ORIGIN)
    pad = 0.38
    rect = Rectangle(width=f.width + 2 * pad, height=f.height + 2 * pad, color=YELLOW, stroke_width=3)
    rect.move_to(f)
    num = T("(106)", 28, DIM).next_to(rect.get_corner(UR), UP, buff=0.1).align_to(rect, RIGHT)
    tag = T("product rule", 32, YELLOW).next_to(rect, DOWN, buff=0.22)
    g = VGroup(rect, f, num, tag)
    g.rect, g.formula, g.num, g.tag = rect, f, num, tag
    g.term1, g.term2 = f.parts[2], f.parts[4]
    g.shift(-rect.get_center())
    return g


BOX_Y = -1.8                   # (106) under the derivation, scaled BOX_K1
BOX_K1 = 1.2
BOX_K = 1.1 / 1.2              # then to 1.1 beside the rectangle
BOX_L = np.array([3.65, 0.6, 0])

# ---------- the rectangle ----------

O = np.array([-5.5, -2.3, 0])  # lower-left corner
W, H, DF, DG = 3.4, 2.3, 0.9, 0.7


def _pt(x, y):
    return O + np.array([x, y, 0])


def rect_parts():
    p = VGroup()
    p.base = Rectangle(width=W, height=H, stroke_width=0, fill_color=FG, fill_opacity=0.08)
    p.base.move_to(_pt(W / 2, H / 2))
    p.top = Line(_pt(0, H), _pt(W, H), color=DIM, stroke_width=2)
    p.right = Line(_pt(W, 0), _pt(W, H), color=DIM, stroke_width=2)
    p.fside = Line(_pt(0, 0), _pt(W, 0), color=BLUE, stroke_width=6)
    p.gside = Line(_pt(0, 0), _pt(0, H), color=PURPLE, stroke_width=6)
    p.flab = M("f").next_to(p.fside, DOWN, buff=0.2)
    p.glab = M("g").next_to(p.gside, LEFT, buff=0.2)
    p.area = M(r"\text{area}\ fg", 40).move_to(p.base)
    p.df = Line(_pt(W, 0), _pt(W + DF, 0), color=TEAL, stroke_width=6)
    p.dg = Line(_pt(0, H), _pt(0, H + DG), color=TEAL, stroke_width=6)
    p.dflab = M(r"\delta f", 36).next_to(p.df, DOWN, buff=0.2)
    p.dglab = M(r"\delta g", 36).next_to(p.dg, LEFT, buff=0.2)
    p.rstrip = Rectangle(width=DF, height=H, stroke_color=TEAL, stroke_width=2,
                         fill_color=TEAL, fill_opacity=0.22).move_to(_pt(W + DF / 2, H / 2))
    p.tstrip = Rectangle(width=W, height=DG, stroke_color=TEAL, stroke_width=2,
                         fill_color=TEAL, fill_opacity=0.22).move_to(_pt(W / 2, H + DG / 2))
    p.rlab = M(r"g\,\delta f", 36).next_to(p.rstrip, RIGHT, buff=0.2)
    p.tlab = M(r"f\,\delta g", 36).next_to(p.tstrip, UP, buff=0.2)
    p.corner = Rectangle(width=DF, height=DG, stroke_color=GOLD, stroke_width=2,
                         fill_color=GOLD, fill_opacity=0.45).move_to(_pt(W + DF / 2, H + DG / 2))
    p.clab = M(r"\delta f\,\delta g", 36).next_to(p.corner, UP, buff=0.2)
    return p


def strips_picture():
    p = rect_parts()
    return VGroup(p.base, p.top, p.right, p.fside, p.gside, p.flab, p.glab, p.area, p.df, p.dg,
                  p.dflab, p.dglab, p.rstrip, p.tstrip, p.rlab, p.tlab)


def shrink_into(src, dst, a=0.0, b=1.0):
    """A copy of src (a whole fraction) leaves it, shrinking onto dst, visible only once clear of src
    and gone before dst fades in. -> (anims, copy)."""
    cp = src.copy().set_opacity(0)
    a0, k = src.get_center(), dst.height * 1.1 / src.height
    h0 = src.height

    def upd(m, t):
        u = smooth(min(1.0, t / 0.8))
        m.become(src.copy())
        m.scale(1 + (k - 1) * u).move_to(a0 + (dst.get_center() - a0) * u)
        op = float(np.clip((u - 0.35) / 0.15, 0, 1) * np.clip((0.95 - u) / 0.15, 0, 1))
        m.set_opacity(op)

    return [*during([UpdateFromAlphaFunc(cp, upd)], a, b), *during([FadeIn(dst)], a + 0.8 * (b - a), b)], cp


class ProductRule(NarratedScene):
    def construct(self):
        self.c1()
        self.c2()
        self.c3()
        self.c4()
        self.c5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c2.prod.1: the definition, for y = fg
    def c1(self):
        title = M(r"y(x) = f(x)\,g(x)", 48).move_to(3.35 * UP)
        r1 = self.r1 = row1()
        self.title = title
        for m in (title, r1):          # clip 1: big and central; they rise to their rows at {trick}
            m.generate_target()
        title.move_to(2.3 * UP)
        r1.scale(1.2).move_to(0.2 * UP)
        with self.say("c2.prod.1") as c:
            self.play(*appear(title), run_time=1.2)
            c.wait_until("def")
            self.play(*appear(r1.a, r1.lim, lag=0.4), run_time=min(1.5, c.until("top")))
            c.wait_until("top")
            self.play(*appear(r1.nf, r1.ng, lag=0.3), run_time=1.3)
            c.wait_until("minus F times G")
            self.play(*appear(r1.nm, r1.nf2, r1.ng2, lag=0.25), run_time=1.3)
            c.wait_until("over")
            self.play(GrowFromCenter(r1.fr.bar), *appear(r1.fr.den), run_time=min(1.2, c.until()))
        settle(self, r1)

    # c2.prod.2: subtract and add the mixed term, regroup
    def c2(self):
        r1, r2, r3 = self.r1, row2(), row3()
        self.r2, self.r3 = r2, r3
        zero = MathTex("=0", font_size=34, color=YELLOW).next_to(r2.frame, UP, buff=0.12)
        with self.say("c2.prod.2") as c:
            at = r2.at
            self.play(MoveToTarget(self.title), MoveToTarget(r1), run_time=1.0)
            self.play(*during([*fly(r1.lim, r2.lim), *appear(r2.eq)], 0, 0.45),
                      *during([*fly(r1.nf, at[0], arc=0.9), *fly(r1.ng, at[1], arc=0.9), *fly(r1.nm, at[8]), *fly(r1.nf2, at[9]),
                               *fly(r1.ng2, at[10]), ReplacementTransform(r1.fr.bar.copy(), r2.fr.bar),
                               *fly(r1.fr.den, r2.fr.den)], 0.4, 1.0), run_time=2.4)
            c.wait_until("Subtract a mixed term")
            self.play(*appear(*r2.T2, lag=0.2), run_time=1.3)
            c.wait_until("add it straight back")
            self.play(*appear(*r2.T3, lag=0.2), time_span(FadeIn(r2.frame), 1.0, 1.6), run_time=1.6)
            c.wait_until("nothing")
            self.play(*flash([r2.frame.copy()], run_time=1.5, time_width=1.5), *appear(zero), run_time=1.5)
            c.wait_until("regroup")
            self.play(*appear(r3.eq, r3.lim, lag=0.2), run_time=1.2)
            # first pair -> f(x+h) out in front, the g chord slope
            c.wait_until("first")
            self.play(*disappear(zero, r2.frame),
                      *flash([at[0].copy(), at[3].copy()], run_time=1.2, time_width=1.5), run_time=1.2)
            gq = r3.gq
            self.play(*fly(at[0], r3.F), *fly(at[1], gq.num[0]), *fly(at[2], gq.num[1]), *fly(at[4], gq.num[2]),
                      time_span(GrowFromCenter(gq.bar), 1.0, 1.8), time_span(FadeIn(gq.den), 1.1, 1.8),
                      run_time=1.8)
            c.wait_until("second")
            self.play(*flash([at[7].copy(), at[10].copy()], run_time=1.0, time_width=1.5), run_time=1.0)
            fq = r3.fq
            self.play(*during(fly(at[7], r3.G), 0, 0.5),
                      *during([*fly(at[5], r3.plus), *fly(at[6], fq.num[0]), *fly(at[8], fq.num[1]),
                               *fly(at[9], fq.num[2])], 0.4, 1.0),
                      time_span(GrowFromCenter(fq.bar), 1.6, 2.2), time_span(FadeIn(fq.den), 1.7, 2.2),
                      run_time=2.2)
            self.play(FadeIn(r3.lb), FadeIn(r3.rb), run_time=0.8)
        settle(self, r2, drop=[r2.frame])
        settle(self, r3)

    # c2.prod.3: the limit; continuity; the result and (106)
    def c3(self):
        r3, r4 = self.r3, row4()
        arrow = Arrow(UP * 1.65, UP * 1.05, buff=0, stroke_width=4, color=TEAL,
                      max_tip_length_to_length_ratio=0.35).set_x(r4.get_right()[0] + 0.5)
        hlab = M(r"h \to 0", 36).next_to(arrow, RIGHT, buff=0.2)
        db = load_scene("ch2_s3_chain").small_diff_box(lit=True)   # as s3 shows it (ch1's box, 0.45, DR)
        box = self.box = product_box().scale(BOX_K1).move_to(BOX_Y * UP)
        with self.say("c2.prod.3") as c:
            sweep_clear(self, r3.animate.scale(1.1).move_to(ROW3_UP * UP), keep=[r3])
            self.play(GrowArrow(arrow), *appear(hlab), run_time=1.0)
            c.wait_until("quot")
            ga, gcp = shrink_into(r3.gq, r4.gp, 0, 0.55)
            fa, fcp = shrink_into(r3.fq, r4.fp, 0, 0.55)
            self.play(*ga, *fa, *during([*fly(r3.F, r4.Fa), *fly(r3.plus, r4.plus), *fly(r3.G, r4.G)], 0.5, 1.0),
                      run_time=2.4)
            self.remove(gcp, fcp)
            c.wait_until("shift")
            fr = SurroundingRectangle(r4.Fa, color=YELLOW, buff=0.1, stroke_width=3)
            self.play(FadeIn(fr), run_time=0.8)
            c.wait_until("becomes F at ex")
            self.play(*swap(r4.Fa, r4.F), Transform(fr, SurroundingRectangle(r4.F, color=YELLOW, buff=0.1,
                                                                            stroke_width=3)), run_time=1.3)
            c.wait_until("careful")
            self.play(*appear(db, shift=None), run_time=1.0)  # early: the notes' box shown whole; (a) is lit
            c.wait_until("It needs F to be continuous")
            self.play(*flash([db.a.copy()], run_time=1.6, time_width=1.5), run_time=1.6)
            c.wait_until("result")
            self.play(*appear(r4.res), FadeOut(fr), run_time=1.0)
            c.wait_until("F prime times G")
            self.play(*disappear(db), time_span(FadeIn(box, shift=0.2 * UP), 0.4, 1.4), run_time=1.4)  # early: the boxed rule with its name
        self.rest3 = [r3, arrow, hlab, r4.F, r4.gp, r4.plus, r4.fp, r4.G, r4.res]

    # c2.prod.4: the rectangle picture
    def c4(self):
        box, p = self.box, rect_parts()
        with self.say("c2.prod.4", gap=0.8) as c:
            box.generate_target()
            tg = box.target
            tg.scale(BOX_K).move_to(BOX_L)
            sweep_clear(self, MoveToTarget(box), keep=[box])
            c.wait_until("Take a rectangle")
            self.play(FadeIn(p.base), Create(p.top), Create(p.right), Create(p.fside), Create(p.gside),
                      run_time=1.2)
            c.wait_until("sides F")
            self.play(*appear(p.flab, p.glab, lag=0.4), run_time=1.2)
            c.wait_until("so its area")
            self.play(*appear(p.area), run_time=1.0)
            c.wait_until("grow")
            self.play(GrowFromEdge(p.df, LEFT), GrowFromEdge(p.dg, DOWN), *appear(p.dflab, p.dglab),
                      run_time=1.5)
            c.wait_until("two thin strips")
            self.play(FadeIn(p.rstrip), FadeIn(p.tstrip), *appear(p.rlab, p.tlab, lag=0.3), run_time=1.5)
            c.wait_until("corner")
            self.play(FadeIn(p.corner), *appear(p.clab), run_time=1.2)
            c.wait_until("which vanishes")
            self.play(*flash([p.corner.copy()], run_time=1.0, color=GOLD), run_time=1.0)
            self.play(*disappear(p.corner, p.clab), run_time=0.9)
            c.wait_until("strips")
            t1, t2 = box.term1, box.term2
            a_right = Arrow(p.rlab.get_corner(UR) + 0.1 * RIGHT, t1.get_bottom() + 0.05 * UP,
                            buff=0.1, stroke_width=4, color=YELLOW)
            a_top = CurvedArrow(p.tlab.get_right() + 0.15 * RIGHT, t2.get_top() + 0.08 * UP, angle=-0.6,
                                stroke_width=4, color=YELLOW)
            self.play(GrowArrow(a_right), Create(a_top), *flash([t1.copy(), t2.copy()], run_time=1.5),
                      run_time=1.5)

    # c2.prod.5: Example 38
    def c5(self):
        title = T("Example 38: Product rule", 48, t2c={"Example 38": YELLOW}).move_to(3.3 * UP)
        yeq = MathTex("y =", r"\ln x", r"\sin x", font_size=60).move_to(2.1 * UP)
        yeq[1].set_color(BLUE)
        yeq[2].set_color(PURPLE)
        fdef = MathTex("f(x) =", r"\ln x", font_size=52, color=BLUE).move_to([-3.3, 0.7, 0])
        gdef = MathTex("g(x) =", r"\sin x", font_size=52, color=PURPLE).move_to([3.3, 0.7, 0])
        fp = MathTex("f' =", r"\frac{1}{x}", font_size=52, color=GREEN).move_to([-3.3, -0.75, 0])
        gp = MathTex("g' =", r"\cos x", font_size=52, color=GREEN).move_to([3.3, -0.75, 0])
        ans = MathTex(r"\frac{dy}{dx}", "=", "f'", "g", "+", "f", "g'", "=",
                      r"\frac{1}{x}", r"\sin x", "+", r"\ln x", r"\cos x", font_size=52)
        for i, col in ((2, GREEN), (3, PURPLE), (5, BLUE), (6, GREEN), (8, GREEN), (9, PURPLE),
                       (11, BLUE), (12, GREEN)):
            ans[i].set_color(col)
        ans.move_to([-0.85, -2.55, 0])
        abox = SurroundingRectangle(ans, color=YELLOW, buff=0.25, stroke_width=3)
        pos = MathTex("x > 0", font_size=40).next_to(abox, RIGHT, buff=0.4)
        with self.say("c2.prod.5") as c:
            sweep_clear(self, *appear(title))
            c.wait_until("the product from the start")
            self.play(*appear(yeq), run_time=1.0)
            c.wait_until("the log of ex")
            self.play(*appear(fdef), run_time=1.0)
            c.wait_until("times sine of ex")
            self.play(*appear(gdef), run_time=1.0)
            c.wait_until("f")
            self.play(*appear(fp), run_time=1.2)
            c.wait_until("g")
            self.play(*appear(gp), run_time=1.2)
            c.wait_until("answer")
            self.play(*appear(*ans[0:8], lag=0.08), run_time=1.0)
            c.wait_until("one over ex", nth=1)
            self.play(*fly(fp[1], ans[8], arc=1.0), *fly(gdef[1], ans[9], arc=-0.8), run_time=1.4)
            c.wait_until("plus the log of ex")
            self.play(*appear(ans[10]), *during(fly(fdef[1], ans[11], arc=0.5), 0, 0.6),
                      *during(fly(gp[1], ans[12]), 0.45, 1.0), run_time=1.8)
            self.play(GrowFromCenter(abox), run_time=0.8)
            c.wait_until("pos")
            self.play(*appear(pos), run_time=1.0)
        self.wait(1.6)
