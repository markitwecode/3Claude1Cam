"""Chapter 7, scene 5: I1, Leibniz on a Gaussian. Clips c7.i1.1 – c7.i1.6.

Plan: opens from empty on s1's card_row(lit=True); I1 (row[3]) grows to the hero (s3's pattern), the
equation's Z PURPLE, x BLUE, (n+1) YELLOW; pause icon on {stop}.
c2 g = e^{-x^2/2} + bell, Z_n = g^(n); key fact g' = -x g boxed; x's chain x -> 1 -> 0.
c3 key fact parks top-left; "how many times?" -> Z_n'' = g^(n+2) = (g')^(n+1) (prime ticked);
   d^{n+1} of both sides, edited to Z_n'' = -(xg)^(n+1).
c4 that line parks at the top; ch4's Leibniz card edits into the n+1 version; Pascal row 5 dim with
   the x-derivative under each entry; the first four die (RED 0), 5 and 1 lit; the two survivors.
c5 assembled, edited into the boxed equation, matched with the card's; (n+1) linked to its binomial;
   the RED slip (n times: the equation for Z_{n-1}).
c6 n = 0 check, GREEN tick; ch5 s4's step small on the right. Ends on an empty frame.

Shared (load_scene("ch7_s5_i1")), for the recap:
  leibniz_n1(size=52)    MathTex (xg)^{(n+1)} = sum_{m=0}^{n+1} binom(n+1,m) x^{(n+1-m)} g^{(m)} at ORIGIN;
                         parts .lhs .eq .sum .binom (YELLOW) .fpart (BLUE) .gpart (PURPLE)
  survivor_last(size=44)    binom(n+1,n+1) x g^(n+1) = x Z_n'      (MathTex)
  survivor_before(size=44)  binom(n+1,n) . 1 . g^(n) = (n+1) Z_n   (MathTex; .n1 the YELLOW (n+1), .binom)
  survivors_shot(size=44)   VGroup(.card, .row, .last, .before) at ORIGIN: the n+1 card, Pascal row 5 with
                            only its last two entries lit, then the two survivors; the (n+1) YELLOW
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

SZ = 44
HERO = np.array([0.0, 0.45, 0])
X = ("x", BLUE)
G0 = ("g", PURPLE)
ZPP, ZP, Z = ("Z_n''", PURPLE), ("Z_n'", PURPLE), ("Z_n", PURPLE)
N1 = ("(n+1)", YELLOW)
DN1 = r"\frac{d^{n+1}}{dx^{n+1}}"
ROW_DIM = 0.4


# ------------------------------------------------------------------ helpers
def M(parts, size=SZ):
    """MathTex with one part per entry; an entry is a tex string or (tex, colour)."""
    texs = [p if isinstance(p, str) else p[0] for p in parts]
    m = MathTex(*texs, font_size=size, color=FG)
    for i, p in enumerate(parts):
        if not isinstance(p, str):
            m[i].set_color(p[1])
    return m


def B(top, bot):
    return (rf"\binom{{{top}}}{{{bot}}}", YELLOW)


def Gk(k):
    return (f"g^{{({k})}}", PURPLE)


def leibniz_n1(size=52):
    m = M([r"(xg)^{(n+1)}", "=", r"\sum_{m=0}^{n+1}", B("n+1", "m"), (r"x^{(n+1-m)}", BLUE), Gk("m")], size)
    m[0][1].set_color(BLUE)
    m[0][2].set_color(PURPLE)
    m.move_to(ORIGIN)
    m.lhs, m.eq, m.sum, m.binom, m.fpart, m.gpart = m[0], m[1], m[2], m[3], m[4], m[5]
    return m


def survivor_last(size=SZ):
    m = M([B("n+1", "n+1"), X, Gk("n+1"), "=", X, ZP], size)
    m.binom = m[0]
    return m


def survivor_before(size=SZ):
    m = M([B("n+1", "n"), r"\cdot", ("1", BLUE), r"\cdot", Gk("n"), "=", N1, Z], size)
    m.binom, m.n1 = m[0], m[6]
    return m


def pascal5(size=SZ):
    return load_scene("ch4_s3_pattern").pascal_row(5, size=size, pitch=1.4)


def survivors_shot(size=SZ):
    card = leibniz_n1(size + 8)
    row = pascal5(size)
    for e in row[:4]:
        e.set_opacity(ROW_DIM)
    last, before = survivor_last(size), survivor_before(size)
    g = VGroup(card, row, last, before).arrange(DOWN, buff=0.45)
    g.move_to(ORIGIN)
    g.card, g.row, g.last, g.before = card, row, last, before
    return g


def split(m, *cuts):
    """Pieces of an (unshown) MathTex: parts [0, c1), [c1, c2), ... as VGroups."""
    edges = [0, *cuts, len(m)]
    return [VGroup(*m[a:b]) for a, b in zip(edges, edges[1:])]


def bell(width=3.4, height=1.5):
    xs = np.linspace(-3, 3, 61)
    pts = [[x * width / 6, height * np.exp(-x * x / 2), 0] for x in xs]
    curve = VMobject().set_points_smoothly(pts).set_stroke(PURPLE, 5)
    base = Line([-width / 2 - 0.15, 0, 0], [width / 2 + 0.15, 0, 0]).set_stroke(DIM, 2)
    return VGroup(base, curve)


def lit_eq(eq):
    """Colour the card's equation as the series: Z PURPLE, x BLUE, (n+1) YELLOW."""
    p = eq[0]
    out = []
    for i in (2, 3, 11, 12, 22, 23):
        out.append(p[i].animate.set_color(PURPLE))
    out.append(p[9].animate.set_color(BLUE))
    for i in range(17, 22):
        out.append(p[i].animate.set_color(YELLOW))
    return out


def color_eq(eq):
    p = eq[0]
    for i in (2, 3, 11, 12, 22, 23):
        p[i].set_color(PURPLE)
    p[9].set_color(BLUE)
    for i in range(17, 22):
        p[i].set_color(YELLOW)
    return eq


# ------------------------------------------------------------------ scene
class I1Leibniz(NarratedScene):
    def construct(self):
        self.s1 = load_scene("ch7_s1_intro")
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- 1: the card
    def clip1(self):
        s1 = self.s1
        row = s1.card_row(lit=True)
        hero = s1.i1_card().move_to(HERO)
        card = row[3]
        self.card = card
        with self.say("c7.i1.1") as c:
            self.play(*appear(row, shift=None), run_time=0.9)  # early: s1's row, shown whole
            self.play(*during(disappear(row[0], row[1], row[2]), 0, 0.4),
                      *during(Transform(card, hero), 0.15, 1.0), run_time=1.8)
            self.remove(row)
            self.add(card)
            zdef = card.body[1][0]
            self.play(FlashUnder(card.body[1], color=YELLOW, time_width=1.5),
                      *[zdef[i].animate.set_color(PURPLE) for i in (0, 1)], run_time=2.0)
            c.wait_until("double prime")
            self.play(FlashUnder(card.body[3], color=YELLOW, time_width=1.5), *lit_eq(card.body[3]),
                      run_time=2.0)
            c.wait_until("stop")
            pause = s1.pause_icon(0.9).move_to([0, -2.85, 0])
            self.pause = pause
            self.play(FadeIn(pause, scale=0.8), run_time=0.8)

    # ---------------------------------------------------------------- 2: g and the key fact
    def clip2(self):
        gdef = M([G0, "=", (r"e^{-x^2/2}", PURPLE)], 56).move_to([-2.7, 2.15, 0])
        curve = bell().move_to([2.9, 2.0, 0])
        zdef = M([Z, "=", Gk("n")], 56).next_to(gdef, DOWN, buff=0.6).align_to(gdef, LEFT)
        key = M([("g'", PURPLE), "=", "-", X, G0], 68).move_to([0, -1.1, 0])
        box = SurroundingRectangle(key, color=YELLOW, buff=0.3, corner_radius=0.1).set_stroke(YELLOW, 3)
        chain = M([X, r"\to", ("1", BLUE), r"\to", ("0", BLUE)], 44)
        chain.next_to(box, DOWN, buff=0.45)
        chain.shift((key[3].get_x() - chain[0].get_x()) * RIGHT)
        self.key = VGroup(key, box)
        with self.say("c7.i1.2") as c:
            self.play(*during(disappear(self.card, self.pause), 0, 0.45),
                      *during(appear(gdef, curve, shift=None), 0.5, 1.0), run_time=1.8)
            c.wait_until("so zed")
            self.play(*appear(zdef), run_time=1.0)
            c.wait_until("G prime")
            self.play(*appear(key), run_time=1.2)
            self.play(FadeIn(box), run_time=0.8)
            settle(self, self.key)
            c.wait_until("runs")
            self.play(FlashAround(key[3], color=BLUE, time_width=1.5), run_time=1.5)
            c.wait_until("it gives")
            self.play(*appear(chain), run_time=1.2)
        self.c2 = [gdef, curve, zdef, chain]

    # ---------------------------------------------------------------- 3: n + 1 times
    def clip3(self):
        q = T("how many times?", 44, YELLOW).move_to([0, 1.0, 0])
        l1 = M([ZPP, "=", Gk("n+2"), "=", (r"(g')^{(n+1)}", PURPLE)], 56).move_to([0.6, 1.0, 0])
        a1, b1 = split(l1, 3)
        tick = check_mark().scale(0.7).next_to(l1[4][2], UP, buff=0.12)
        l2a = M([DN1, ("g'", PURPLE), "=", "-", DN1, r"\big(", X, G0, r"\big)"], 56).move_to([0, -1.3, 0])
        l2b = M([ZPP, "=", "-", DN1, r"\big(", X, G0, r"\big)"], 56).move_to([0, -1.3, 0])
        l2c = M([ZPP, "=", "-", "(", X, G0, r")^{(n+1)}"], 56).move_to([0, -1.3, 0])
        with self.say("c7.i1.3") as c:
            sweep_clear(self, self.key.animate.scale(0.72).move_to([-4.7, 3.05, 0]),
                        time_span(FadeIn(q, shift=0.2 * DOWN), 0.7, 1.4), keep=[self.key], run_time=1.4)
            c.wait_until("double prime")
            self.play(*swap(q, a1), run_time=1.4)
            c.wait_until("already")
            self.play(*appear(b1), run_time=1.0)
            self.play(Create(tick), run_time=0.8)
            c.wait_until("left")
            self.play(*appear(l2a), FlashAround(self.key, color=YELLOW, time_width=1.5), run_time=1.6)
            c.wait_until("The left side")
            self.play(FlashAround(a1, color=PURPLE, time_width=1.5), run_time=1.2)
            self.play(*edit(l2a, l2b), run_time=1.6)
            c.wait_until("right")
            self.play(*edit(l2b, l2c), run_time=1.6)
        self.res = l2c

    # ---------------------------------------------------------------- 4: Leibniz, two survive
    def clip4(self):
        res = self.res
        c4 = load_scene("ch4_s4_formula").leibniz_card(52).move_to([0, 1.9, 0]).tex
        card = leibniz_n1(52).move_to([0, 1.9, 0])
        row = pascal5().move_to([0.9, 0.35, 0])
        for e in row:
            e.set_opacity(ROW_DIM)
        cap = MathTex(r"\text{row } n+1,\ n=4", font_size=32, color=DIM)
        cap.next_to(row, LEFT, buff=0.55)
        ders = ["x^{(5)}", "x^{(4)}", "x'''", "x''", "x'", "x"]
        tags = [MathTex(d, font_size=36, color=BLUE).move_to([e.get_x(), -0.35, 0]) for d, e in zip(ders, row)]
        zeros = [MathTex("0", font_size=36, color=RED).move_to(t) for t in tags[:4]]
        last = survivor_last().move_to([0, -1.45, 0])
        before = survivor_before().move_to([0, -2.75, 0])
        last.shift((before[5].get_x() - last[3].get_x()) * RIGHT)
        la, lb = split(last, 3)
        ba, bb = split(before, 5)
        with self.say("c7.i1.4") as c:
            sweep_clear(self, res.animate.scale(0.8).move_to([0, 3.3, 0]), keep=[res])
            self.play(*appear(c4, shift=None), run_time=1.0)
            c.wait_until("with ex")
            self.play(*edit(c4, card), run_time=1.6)
            c.wait_until("row")
            self.play(*appear(row, shift=None), *appear(cap), run_time=1.2)
            self.play(*appear(*tags, lag=0.15), run_time=1.4)
            c.wait_until("survive")
            c.wait_until("is zero")
            self.play(*[a for t, z in zip(tags[:4], zeros) for a in swap(t, z)],
                      *set_alpha(list(row[:4]), 0.2), run_time=1.4)
            c.wait_until("only the last two")
            self.play(*set_alpha(list(row[4:]), 1), *flash(list(row[4:])), run_time=1.4)
            c.wait_until("last")
            self.play(*appear(la), FlashAround(row[5], time_width=1.5), run_time=1.4)
            c.wait_until("times zed N prime")
            self.play(*appear(lb), run_time=1.0)
            c.wait_until("before")
            self.play(*appear(ba), FlashAround(row[4], time_width=1.5), run_time=1.4)
            c.wait_until("is N plus one")
            self.play(FlashAround(before[0], time_width=1.5), run_time=1.2)
            c.wait_until("That term is")
            self.play(*appear(bb), run_time=1.0)
        self.c4 = dict(card=card, row=row, cap=cap, tags=tags[4:], zeros=zeros, la=la, lb=lb, ba=ba, bb=bb,
                       before=before)

    # ---------------------------------------------------------------- 5: assemble
    def clip5(self):
        d = self.c4
        res = self.res
        asm = M([ZPP, "=", "-", X, ZP, "-", N1, Z], 56).move_to([0, 1.0, 0])
        fin = M([ZPP, "+", X, ZP, "+", N1, Z, "=", "0"], 56).move_to([0, 1.0, 0])
        fbox = SurroundingRectangle(fin, color=YELLOW, buff=0.25, corner_radius=0.1).set_stroke(YELLOW, 3)
        target = color_eq(self.s1.i1_card().body[3])
        lab = T("I1", 36, YELLOW)
        tg = VGroup(lab, target).arrange(RIGHT, buff=0.5).move_to([0, 2.85, 0])
        ba, bb, before = d["ba"], d["bb"], d["before"]
        shift_up = 1.45 * UP
        slip_cap = MathTex(r"\text{differentiate only } n \text{ times:}", font_size=36, color=RED)
        slip = MathTex(r"Z_{n-1}'' + x\,Z_{n-1}' + n\,Z_{n-1} = 0", font_size=48, color=RED)
        slip_tag = MathTex(r"\text{the equation for } Z_{n-1}", font_size=34, color=FG)
        VGroup(slip_cap, slip, slip_tag).arrange(DOWN, buff=0.35).move_to([0, -2.0, 0])
        with self.say("c7.i1.5", gap=1.6) as c:
            sweep_clear(self, res.animate.scale(1.25).move_to([0, 1.0, 0]),
                        keep=[res, d["la"], d["lb"], ba, bb])
            self.play(*edit(res, asm), run_time=1.6)
            c.wait_until("move")
            self.play(*during(disappear(d["la"], d["lb"]), 0, 0.4),
                      *during(edit(asm, fin), 0.1, 1.0),
                      *during([ba.animate.shift(shift_up), bb.animate.shift(shift_up)], 0.45, 1.0), run_time=2.0)
            c.wait_until("that's the equation")
            self.play(FadeIn(fbox), *appear(tg, shift=None), run_time=1.2)
            self.play(FlashAround(fin, time_width=1.5), FlashAround(target, time_width=1.5), run_time=1.6)
            c.wait_until("coef")
            bin_ = before[0]
            arrow = Arrow(bin_.get_top() + 0.05 * UP, fin[5].get_bottom() + 0.32 * DOWN, buff=0.05,
                          stroke_width=4, color=YELLOW)
            self.play(GrowArrow(arrow), FlashAround(fin[5], time_width=1.5), FlashAround(bin_, time_width=1.5),
                      run_time=1.6)
            c.wait_until("slip")
            self.play(*during(disappear(ba, bb, arrow), 0, 0.45),
                      *during(appear(slip_cap, slip, lag=0.3), 0.45, 1.0), run_time=1.8)
            c.wait_until("the right equation")
            self.play(*appear(slip_tag), run_time=1.0)
        self.fin = VGroup(fin, fbox)
        settle(self, self.fin)

    # ---------------------------------------------------------------- 6: n = 0
    def clip6(self):
        n0 = M([("n", FG), "=", ("0", GOLD)], 52).move_to([-4.5, 1.45, 0])
        z = [M([("Z_0", PURPLE), "=", G0], 48),
             M([("Z_0'", PURPLE), "=", "-", X, G0], 48),
             M([("Z_0''", PURPLE), "=", "(", ("x^2", BLUE), "-1)", G0], 48)]
        zg = VGroup(*z).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-3.7, -0.45, 0])
        for m in z[1:]:
            m.shift((z[0][1].get_x() - m[1].get_x()) * RIGHT)
        sm = M([r"\big[", "(", ("x^2", BLUE), "-1)", "-", ("x^2", BLUE), "+", "1", r"\big]", G0, "=", "0"], 52)
        sm.move_to([-0.6, -2.85, 0])
        sa, sb = split(sm, 10)
        tick = check_mark().scale(1.1).next_to(sm, RIGHT, buff=0.45)
        head = T("Part 5", 32, DIM)
        expr = M([r"\frac{d^n}{dx^n}", r"\Big(", X, (r"e^{-x^2}", PURPLE), r"\Big)"], 46)
        r4 = load_scene("ch4_s3_pattern").pascal_row(4, size=46, pitch=0.9)
        for e in r4[:3]:
            e.set_opacity(0.25)
        panel = VGroup(head, expr, r4).arrange(DOWN, buff=0.35).move_to([3.7, -0.3, 0])
        frame = SurroundingRectangle(panel, color=DIM, buff=0.3, corner_radius=0.15).set_stroke(DIM, 2)
        with self.say("c7.i1.6") as c:
            sweep_clear(self, self.fin.animate.scale(0.82).move_to([0, 2.95, 0]), keep=[self.fin])
            self.play(*appear(n0), run_time=1.0)
            c.wait_until("z0")
            self.play(*appear(z[0]), run_time=1.0)
            c.wait_until("its derivative")
            self.play(*appear(z[1]), run_time=1.0)
            c.wait_until("second derivative")
            self.play(*appear(z[2]), run_time=1.0)
            c.wait_until("sum")
            self.play(*appear(sa), run_time=1.4)
            c.wait_until("That's zero")
            self.play(*appear(sb), run_time=0.9)
            self.play(Create(tick), FlashAround(sm, color=GREEN, time_width=1.5), run_time=1.2)
            c.wait_until("same")
            self.play(FadeIn(frame), *appear(head, expr, r4, lag=0.2), run_time=1.4)
            self.play(*flash(list(r4[3:])), run_time=1.2)
        self.wait(3.5)
