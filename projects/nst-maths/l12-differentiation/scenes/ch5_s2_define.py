"""Chapter 5, scene 2: the definition at work (H_0, H_1, H_2 by hand). Clips c5.def.1 – c5.def.5.

Exports (chapter 5 chrome, see STATUS.md "Chapter 5"):
  def_line()        the definition along the top edge, as it sits in s2–s5.
  ladder_card(k)    the H_n ladder at the right edge, rungs bottom-up H_0..H_4, first k filled.
  rung_value(k)     rung k's polynomial, built and placed exactly as ladder_card puts it.
  open_shot()       s2's first frame: def line alone.
  handover_shot()   s2's last frame: def line + ladder_card(3).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- shared chrome (ch5)
DEF_SIZE = 44
DEF_CENTER = np.array([-0.8, 3.0, 0])      # top edge; the top-right corner (x > 3.1) stays free

LADDER_W, LADDER_H = 3.9, 5.45
LADDER_CENTER = np.array([4.65, -0.975, 0])  # box x 2.7..6.6, y -3.7..1.75
RUNG_Y0, RUNG_PITCH = -3.2, 0.98            # rung k sits at y = -3.2 + 0.98 k
RUNG_SIZE = 34
LABEL_X = 2.95                              # left edge of the H_k labels
VALUE_X = 3.95                              # left edge of the polynomials
VALUE_MAX_W = 6.4 - VALUE_X                 # polynomials wider than this are scaled to fit
EMPTY_LABEL_OP = 0.4
RUNG_TEX = ["1", "2x", "4x^2 - 2", "8x^3 - 12x", "16x^4 - 48x^2 + 12"]


def mtex(*parts, size=40, color=FG):
    """MathTex from parts; parts holding e^{x^2} GOLD, e^{-x^2} PURPLE."""
    m = MathTex(*parts, font_size=size, color=color)
    for i, p in enumerate(parts):
        if "e^{-x^2}" in p:
            m[i].set_color(PURPLE)
        elif "e^{x^2}" in p:
            m[i].set_color(GOLD)
    return m


def def_line():
    """H_n(x) ≡ (−1)^n e^{x²} dⁿ/dxⁿ ( e^{−x²} ), MathTex 44 at the top edge, centre (−0.8, 3.0).
    Parts (each a sub-mobject of the one MathTex): .lhs H_n(x), .equiv ≡, .sign (−1)^n,
    .front e^{x²} GOLD, .dn dⁿ/dxⁿ, .lpar (, .gauss e^{−x²} PURPLE, .rpar )."""
    m = mtex(r"H_n(x)", r"\equiv", r"(-1)^n", r"e^{x^2}", r"\frac{d^n}{dx^n}", r"\Big(",
             r"e^{-x^2}", r"\Big)", size=DEF_SIZE)
    m.move_to(DEF_CENTER)
    (m.lhs, m.equiv, m.sign, m.front, m.dn, m.lpar, m.gauss, m.rpar) = [m[i] for i in range(8)]
    return m


def rung_y(k):
    return RUNG_Y0 + RUNG_PITCH * k


def rung_value(k):
    """Rung k's polynomial (FG MathTex 34, scaled to fit if wide), placed as in ladder_card."""
    v = MathTex(RUNG_TEX[k], font_size=RUNG_SIZE, color=FG)
    if v.width > VALUE_MAX_W:
        v.scale_to_fit_width(VALUE_MAX_W)
    v.align_to(np.array([VALUE_X, 0, 0]), LEFT)
    v.align_to(np.array([0, rung_y(k) - 0.17, 0]), DOWN)
    return v


def ladder_card(k=3):
    """The H_n ladder, a narrow card at the right edge (box x 2.7..6.6, y −3.7..1.75; the
    top-right corner above y 1.75 stays free). Parts: .box (DIM rounded rect), .heading
    ("H_n ladder", H_n YELLOW), .rungs[0..4] bottom-up, each a VGroup with .bar (DIM line under
    it), .label (H_j, YELLOW; opacity 0.4 while empty), .eq ("="; opacity 0.4 while empty),
    .value (rung_value(j), None while empty), .slot (DIM dashed line, None once filled).
    Rung j is filled when j < k."""
    g = VGroup()
    g.box = RoundedRectangle(corner_radius=0.18, width=LADDER_W, height=LADDER_H,
                             stroke_color=DIM, stroke_width=2).move_to(LADDER_CENTER)
    g.heading = MathTex(r"H_n", r"\text{ ladder}", font_size=34, color=FG)
    g.heading[0].set_color(YELLOW)
    g.heading.move_to(np.array([LADDER_CENTER[0], 1.3, 0]))
    g.add(g.box, g.heading)
    g.rungs = []
    for j in range(5):
        y = rung_y(j)
        r = VGroup()
        r.bar = Line([2.9, y - 0.4, 0], [6.4, y - 0.4, 0], stroke_color=DIM, stroke_width=2)
        r.bar.set_stroke(opacity=0.6)
        r.label = MathTex(f"H_{j}", font_size=RUNG_SIZE, color=YELLOW)
        r.label.shift(np.array([LABEL_X, y - 0.17, 0]) - np.array([r.label.get_left()[0],
                                                                    r.label[0][0].get_bottom()[1], 0]))
        r.eq = MathTex("=", font_size=RUNG_SIZE, color=FG)
        r.eq.move_to(np.array([r.label.get_right()[0] + 0.12 + r.eq.width / 2, y - 0.05, 0]))
        r.add(r.bar, r.label, r.eq)
        if j < k:
            r.value = rung_value(j)
            r.slot = None
            r.add(r.value)
        else:
            r.value = None
            r.label.set_opacity(EMPTY_LABEL_OP)
            r.eq.set_opacity(EMPTY_LABEL_OP)
            r.slot = DashedLine([VALUE_X, y - 0.17, 0], [VALUE_X + 1.8, y - 0.17, 0],
                                dash_length=0.1, stroke_width=2, color=DIM)
            r.add(r.slot)
        g.rungs.append(r)
        g.add(r)
    return g


def open_shot():
    """s2's first frame: the definition line alone (ch5_s1 ends on it)."""
    return VGroup(def_line())


def handover_shot():
    """s2's last frame: def line + ladder_card(3) (ch5_s3 opens on it)."""
    return VGroup(def_line(), ladder_card(3))


# ---------------------------------------------------------------- the scene
COL_N, COL_D, COL_M, COL_H = -5.6, -2.7, 0.9, 4.3
HEAD_Y, RULE_Y = 1.6, 0.95
ROW_Y = [0.4, -0.7, -1.8]
STRIP_Y = -2.85


def low_path(a, b, dip=0.6):
    """Drop below the row, run along under it, rise into place (keeps clear of the row's text)."""
    y = min(a[1], b[1]) - dip
    return VMobject().set_points_smoothly([a, [a[0], a[1] - 0.4, 0], [a[0] + 0.6, y, 0],
                                           [b[0] - 0.6, y, 0], [b[0], b[1] - 0.4, 0], b])


def cell(m, x, row):
    return m.move_to(np.array([x, ROW_Y[row], 0]))


class Ch5S2Define(NarratedScene):
    def construct(self):
        dl = def_line()
        self.add(dl)
        self.gaussian(dl)
        self.rows01(dl)
        self.row2()
        self.pattern()
        self.check_and_ladder(dl)
        self.wait(0.6)          # handover: hold on handover_shot(); ch5_s3 opens on it

    # c5.def.1: the Gaussian and its inverse
    def gaussian(self, dl):
        with self.say("c5.def.1") as c:
            ax = Axes(x_range=[-2.6, 2.6, 1], y_range=[0, 1.2, 1], x_length=5.6, y_length=2.6,
                      tips=False, axis_config={"color": DIM, "stroke_width": 2, "include_ticks": False})
            ax.move_to([-3.2, 0.0, 0])
            curve = ax.plot(lambda x: np.exp(-x * x), x_range=[-2.6, 2.6], color=PURPLE, stroke_width=5)
            yl = mtex(r"y = ", r"e^{-x^2}", size=40)
            yl[0].set_color(PURPLE)
            yl.next_to(ax.c2p(0.7, 1.05), RIGHT, buff=0.15)
            gl = T("Gaussian", 34, PURPLE).next_to(ax.c2p(1.3, 0.3), UR, buff=0.08)
            self.play(Create(ax), run_time=1.0)
            self.play(Create(curve), *appear(yl), run_time=1.8)
            c.wait_until(own_word=gl)
            self.play(*appear(gl))

            id1 = mtex(r"e^{x^2}", r"\cdot", r"e^{-x^2}", r"= 1", size=48).move_to([3.4, 0.9, 0])
            id2 = mtex(r"e^{x^2}", r"\cdot\, p(x)\,", r"e^{-x^2}", r"= p(x)", size=48)
            id2.move_to([3.4, -0.6, 0])
            c.wait_until("inverse")
            self.play(FlashAround(dl.front, run_time=1.5, time_width=1.5))
            c.wait_until("is one over the gaussian")
            self.play(*appear(id1), run_time=1.2)
            c.wait_until("so whenever")
            self.play(*appear(id2), run_time=1.2)
            c.wait_until("strips")
            self.play(*flash([id2[0], id2[2]]), *set_alpha([id2[0], id2[2]], 0.3), run_time=1.4)
        self.fig = VGroup(ax, curve, yl, gl, id1, id2)

    # c5.def.2: rows n = 0 and n = 1
    def rows01(self, dl):
        self.hn = MathTex("n", font_size=40, color=DIM).move_to([COL_N, HEAD_Y, 0])
        self.hd = mtex(r"\frac{d^n}{dx^n}", r"\,e^{-x^2}").move_to([COL_D, HEAD_Y, 0])
        self.hm = mtex(r"\times(-1)^n", r"\,e^{x^2}").move_to([COL_M, HEAD_Y, 0])
        self.hh = MathTex("H_n", font_size=40, color=YELLOW).move_to([COL_H, HEAD_Y, 0])
        self.rule = Line([-6.1, RULE_Y, 0], [5.4, RULE_Y, 0], stroke_color=DIM, stroke_width=2)
        self.ns = [cell(MathTex(str(i), font_size=40, color=DIM), COL_N, i) for i in range(3)]
        self.d = [cell(mtex(r"e^{-x^2}"), COL_D, 0),
                  cell(mtex(r"-", r"2x", r"\,e^{-x^2}"), COL_D, 1),
                  cell(mtex(r"(4x^2-2)", r"\,e^{-x^2}"), COL_D, 2)]
        self.m = [cell(mtex(r"\times", r"\,e^{x^2}"), COL_M, 0),
                  cell(mtex(r"\times", r"(", r"-", r"1)", r"\,e^{x^2}"), COL_M, 1),
                  cell(mtex(r"\times", r"\,e^{x^2}"), COL_M, 2)]
        self.h = [cell(MathTex(t, font_size=40), COL_H, i) for i, t in enumerate(RUNG_TEX[:3])]
        d, m, h = self.d, self.m, self.h

        with self.say("c5.def.2") as c:
            sweep_clear(self, *appear(self.hn, self.hd, self.hm, self.hh, lag=0.15),
                        FadeIn(self.rule), keep=[dl], run_time=1.8)   # early: column heads, read with each row
            self.play(*appear(self.ns[0], d[0], lag=0.3), run_time=1.2)
            c.wait_until("with no derivatives")
            self.play(*appear(m[0]), run_time=1.0)
            c.wait_until("one0")
            self.play(*flash([d[0][0], m[0][1]]), *set_alpha([d[0][0], m[0][1]], 0.3), run_time=1.4)
            c.wait_until("h zero is one")
            self.play(*appear(h[0]), run_time=1.0)

            c.wait_until("first")
            self.play(*appear(self.ns[1], d[1], lag=0.3), run_time=1.4)
            self.tag = T("chain rule, part 2", 28, DIM).next_to(d[1], DOWN, buff=0.3)
            c.wait_until(own_word=self.tag)
            self.play(*appear(self.tag), run_time=1.0)
            c.wait_until("hone")
            self.play(*appear(m[1]), run_time=1.2)
            c.wait_until("the gaussian goes")
            self.play(*flash([d[1][2], m[1][4]]), *set_alpha([d[1][2], m[1][4]], 0.3),
                      *disappear(self.tag), run_time=min(1.2, c.until("the minus signs")))
            c.wait_until("the minus signs")
            self.play(*recolor([d[1][0], m[1][2]], YELLOW), *flash([d[1][0], m[1][2]]),
                      run_time=min(1.2, c.until("and h one is")))
            c.wait_until("and h one is")
            # one object travels: the row's own "2x" lifts out, a fresh one fades back in behind it
            mv = d[1][1].copy()
            self.remove(d[1])
            self.add(d[1][0], d[1][2], mv)  # row as separate parts while the "2x" leaves its slot
            self.play(*set_alpha([d[1][0], m[1][2]], 0.3),
                      MoveAlongPath(mv, low_path(mv.get_center(), h[1].get_center())),
                      *during([FadeIn(d[1][1])], 0.6, 1.0), run_time=min(1.5, c.until()))
            self.remove(mv)
            self.add(h[1])
            settle(self, d[1])

    # c5.def.3: row n = 2 via the product rule
    def row2(self):
        d, m, h = self.d, self.m, self.h
        s_l = mtex(r"\frac{d}{dx}\Big(-2x\,", r"e^{-x^2}", r"\Big)", size=36)
        s_r = mtex(r"= -2\,", r"e^{-x^2}", r"+ (-2x)(-2x)\,", r"e^{-x^2}", size=36)
        s_eq = MathTex("=", font_size=36)
        s_res = mtex(r"(4x^2-2)", r"\,e^{-x^2}", size=36)
        side = VGroup(s_l, s_r, s_eq, s_res).arrange(RIGHT, buff=0.22).move_to([-0.4, STRIP_Y, 0])
        with self.say("c5.def.3") as c:
            self.play(*appear(self.ns[2], s_l, lag=0.5), run_time=1.6)
            c.wait_until("four")
            self.play(*appear(s_r), run_time=1.5)
            c.wait_until("plus four ex squared")
            self.play(*appear(s_eq, s_res, lag=0.1), run_time=1.2)
            c.wait_until("times the gaussian", nth=2)
            self.play(*during(disappear(s_l, s_r), 0, 0.3), *fly(s_res, d[2], arc=-0.6),
                      run_time=min(1.6, c.until("htwo")))
            c.wait_until("htwo")
            self.play(*disappear(s_eq, s_res), *appear(m[2]), run_time=1.2)
            self.play(*flash([d[2][1], m[2][1]]), *set_alpha([d[2][1], m[2][1]], 0.3), run_time=1.2)
            c.wait_until("and h two is")
            self.play(FlashAround(d[2][0]), *appear(h[2]), run_time=min(1.4, c.until()))

    # c5.def.4: the pattern and the leading term
    def pattern(self):
        d, m = self.d, self.m
        pur = [d[0][0], d[1][2], d[2][1]]
        gold = [m[0][1], m[1][4], m[2][1]]
        L1 = MathTex("1", font_size=36)
        A1 = MathTex(r"\xrightarrow{\times(-2x)}", font_size=36)
        L2 = MathTex("-2x", font_size=36)
        A2 = MathTex(r"\xrightarrow{\times(-2x)}", font_size=36)
        L3 = MathTex("4x^2", font_size=36)
        IMP = MathTex(r"\Rightarrow\ (-2)^n x^n", font_size=36)
        MUL = MathTex(r"\times\,(-1)^n", font_size=36)
        RES = MathTex(r"=\ ", r"2^n x^n", font_size=36)
        RES[1].set_color(YELLOW)
        self.strip = [L1, A1, L2, A2, L3, IMP, MUL, RES]
        VGroup(*self.strip).arrange(RIGHT, buff=0.25).move_to([-0.4, STRIP_Y, 0])
        self.cap = MathTex(r"\text{degree } n", font_size=32, color=YELLOW).next_to(RES[1], DOWN, buff=0.15)
        with self.say("c5.def.4") as c:
            self.play(*set_alpha(pur, 1), *flash(pur), run_time=1.4)
            self.play(*set_alpha(gold, 1), *flash(gold, color=GOLD), *set_alpha(pur, 0.3),
                      run_time=min(1.4, c.until("lead")))
            c.wait_until("lead")
            self.play(*appear(L1, A1, L2, A2, L3, lag=0.35), run_time=min(2.6, c.until("flip")))
            c.wait_until("flip")
            self.play(*appear(IMP), run_time=1.0)
            c.wait_until("cancels")
            self.play(*appear(MUL), run_time=1.0)
            c.wait_until("all those minus signs")
            self.play(*appear(RES), run_time=1.0)
            c.wait_until(own_word=self.cap)
            self.play(*appear(self.cap), run_time=1.0)

    # c5.def.5: check the recursion at n = 1, then the ladder
    def check_and_ladder(self, dl):
        h = self.h
        inst = MathTex(r"H_2 = 2x\cdot H_1 - 2\cdot 1\cdot H_0", font_size=40)
        tail = MathTex(r"= 2x\cdot 2x - 2 = 4x^2 - 2", font_size=40)
        VGroup(inst, tail).arrange(RIGHT, buff=0.25).move_to([-0.4, STRIP_Y, 0])
        tick = check_mark().next_to(h[2], RIGHT, buff=0.35)
        card = ladder_card(3)
        with self.say("c5.def.5") as c:
            c.wait_until("it says")
            self.play(*during(disappear(*self.strip, self.cap), 0, 0.45),
                      *during(appear(inst), 0.5, 1), run_time=1.6)
            self.play(*[x.animate(rate_func=there_and_back).set_color(YELLOW) for x in (h[1], h[0])],
                      run_time=1.2)
            c.wait_until("four ex squared")
            self.play(*appear(tail), run_time=1.2)
            c.wait_until("tick")
            self.play(FadeIn(tick, scale=0.6), FlashAround(h[2], color=GREEN), run_time=1.0)

            c.wait_until("ladder")
            rest = [self.hn, self.hd, self.hm, self.hh, self.rule, *self.ns, *self.d, *self.m,
                    inst, tail, tick]
            r = card.rungs
            parts = [x for j in range(5) for x in (r[j].bar, r[j].label, r[j].eq, r[j].slot) if x is not None]
            # the H column slides left out of the card's way, the card opens, then the values
            # go in one at a time from H_0 up on straight paths that never cross
            self.play(*during(disappear(*rest), 0, 0.45),
                      *during([x.animate.shift(3.5 * LEFT) for x in h], 0.45, 0.9),
                      *during([FadeIn(card.box), FadeIn(card.heading)], 0.55, 1), run_time=1.3)
            k = RUNG_SIZE / 40
            self.play(*during(h[0].animate.scale(k).move_to(r[0].value), 0, 0.36),
                      *during(h[1].animate.scale(k).move_to(r[1].value), 0.3, 0.6),
                      *during(h[2].animate.scale(k).move_to(r[2].value), 0.56, 0.8),
                      *during(appear(*parts, shift=None, lag=0.02), 0.8, 1), run_time=2.3)
            self.remove(*h)
            self.add(*[r[j].value for j in range(3)])
            settle(self, card)
        self.handover = VGroup(dl, card)
