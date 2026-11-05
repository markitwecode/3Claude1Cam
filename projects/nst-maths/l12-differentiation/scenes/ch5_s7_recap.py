"""Chapter 5, scene 7: recap, Examples Sheet I1, next time, end card. Clips c5.recap.1 – c5.recap.3.

Plan: opens empty (s6 ends empty). A small "Recap" heading, then four panels in a 2 x 2 grid, each the
owner's own objects scaled down, its line under it; each lights on its mark while the earlier ones dim:
  r1 s2's def_line() over table row n = 2: (4x^2-2) e^{-x^2} x e^{x^2}, the Gaussian pair dims, the
     polynomial flies to H_2 = 4x^2 - 2;
  r2 s3: d^{n+1}/dx^{n+1} = d^n/dx^n (d/dx ...), then H_{n+1} + s3's hero_line();
  r3 s4: the sum's first line struck RED (dimmed), the two survivors, ch4's pascal_row(4) with 4 1 lit;
  r4 s5's boxed_recursion() beside s2's ladder_card(5) (side by side: stacked it would be unreadable).
{sheet}: the grid clears, r3 shrinks to the bottom-right, the I1 card (i1_card(), owned here) lands at
the top; hints under it on {gdef}, {gprime}, {hint}; "two terms" tag arrows back at r3's survivors.
{next}: ch6 s1's notes_figure() (no dots), {shape}: YELLOW dots on its max and min. After the last
word the board sweeps into ch6 s1's open_card(), held ~8 s, then fades.

Exports: i1_card() = Examples Sheet I, question I1 (p. 11), verbatim, in ch3 s7's question_card style:
DIM rounded frame 9.4 wide, YELLOW "I1" top left, Tex 40 body, e^{-x^2/2} PURPLE; built at ORIGIN.
Parts .frame .label .body (VGroup of 4 Tex lines: .body[3] is the differential equation).
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

GAUSS2 = "e^{-x^2/2}"


def i1_card():
    """Examples Sheet I, I1 (p. 11), verbatim; e^{-x^2/2} PURPLE. Parts .frame .label .body."""
    q = load_scene("ch3_s7_recap").question_card
    return q("I1", [
        r"Use Leibniz's formula to establish that",
        r"$Z_n \equiv \dfrac{d^n}{dx^n}\, e^{-x^2/2}$ is a solution of the",
        r"differential equation",
        r"$\dfrac{d^2 Z_n}{dx^2} + x\,\dfrac{dZ_n}{dx} + (n+1)Z_n = 0$.",
    ], colors={GAUSS2: PURPLE})


# ---------------------------------------------------------------- grid layout
HEAD_Y = 3.45
COL_X = (-3.55, 3.55)
VIS_TOP = (3.05, -0.05)      # top edge of each row's visual
VIS_HS = (2.0, 2.9)          # the bottom row is taller: r4's ladder needs five rungs
VIS_W = 6.1
CAP_GAP = 0.2
CAP_SIZE = 28
DIM_K = 0.35
LAD_SIZE = 28
LAD_PITCH = 0.37


def fit(m, i, w=VIS_W):
    h = VIS_HS[i // 2]
    m.scale(min(w / m.width, h / m.height))
    x, top = COL_X[i % 2], VIS_TOP[i // 2]
    m.move_to([x, top - h / 2, 0])
    return m


def caption(text, i):
    lines = VGroup(*[T(t, CAP_SIZE) for t in text.split("\n")]).arrange(DOWN, buff=0.1)
    x, top = COL_X[i % 2], VIS_TOP[i // 2]
    lines.move_to([x, 0, 0]).align_to(np.array([0, top - VIS_HS[i // 2] - CAP_GAP, 0]), UP)
    return lines


def mini_ladder(S2):
    """s2's ladder card, compact: DIM rounded box, rungs H_0..H_4 bottom-up (YELLOW label, "=", FG
    value, DIM bar under each), size 28, no heading (too small to read in a quarter panel)."""
    rungs = VGroup()
    for j in range(5):
        lab = MathTex(f"H_{j}", "=", S2.RUNG_TEX[j], font_size=LAD_SIZE, color=FG)
        lab[0].set_color(YELLOW)
        rungs.add(lab)
    for j, r in enumerate(rungs):
        r.shift(np.array([-r[1].get_x(), LAD_PITCH * j - r[1].get_y(), 0]))
    w = max(r.get_right()[0] for r in rungs) - min(r.get_left()[0] for r in rungs) + 0.4
    left = min(r.get_left()[0] for r in rungs) - 0.2
    bars = VGroup(*[Line([left + 0.1, r[1].get_y() - LAD_PITCH / 2, 0],
                         [left + w - 0.1, r[1].get_y() - LAD_PITCH / 2, 0],
                         stroke_color=DIM, stroke_width=1.5).set_stroke(opacity=0.6)
                    for r in list(rungs)[1:]])
    box = RoundedRectangle(corner_radius=0.12, width=w, height=rungs.height + 0.3,
                           stroke_color=DIM, stroke_width=2).move_to(rungs)
    box.set_x(left + w / 2)
    g = VGroup(box, bars, rungs)
    g.box, g.bars, g.rungs = box, bars, rungs
    return g


def dimmed(m, k):
    """A copy of m with every part's opacity multiplied by k (keeps the parts' own dims)."""
    t = m.copy()
    for a, b in zip(m.family_members_with_points(), t.family_members_with_points()):
        b.set_fill(opacity=a.get_fill_opacity() * k)
        b.set_stroke(opacity=a.get_stroke_opacity() * k)
    return t


class Recap(NarratedScene):
    def construct(self):
        self.S2 = load_scene("ch5_s2_define")
        self.S3 = load_scene("ch5_s3_peel")
        self.S4 = load_scene("ch5_s4_leibniz")
        self.S5 = load_scene("ch5_s5_assemble")
        self.P4 = load_scene("ch4_s3_pattern")
        self.H6 = load_scene("ch6_s1_hook")
        self.build_panels()
        self.clip1()
        self.clip2()
        self.clip3()
        card = self.H6.open_card()
        sweep_clear(self, *appear(card, shift=None), run_time=1.6)
        self.wait(8.0)          # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ panels
    def build_panels(self):
        S2, S3, S4, S5, P4 = self.S2, self.S3, self.S4, self.S5, self.P4
        mt = S2.mtex

        # r1: def line over row n = 2
        dl = S2.def_line()
        d = mt(r"(4x^2-2)", r"\,e^{-x^2}", size=40)
        m = mt(r"\times", r"\,e^{x^2}", size=40)
        arr = MathTex(r"\to", font_size=40, color=DIM)
        h = MathTex(r"H_2", "=", r"4x^2-2", font_size=40, color=FG)
        h[0].set_color(YELLOW)
        row = VGroup(d, m, arr, h).arrange(RIGHT, buff=0.35)
        row.next_to(dl, DOWN, buff=0.6)
        self.v1 = fit(VGroup(dl, row), 0)
        self.p1 = dict(dl=dl, d=d, m=m, arr=arr, h=h)
        self.c1 = caption("polynomial × Gaussian,\nGaussian removed", 0)

        # r2: peel one derivative off, land on s3's hero line
        la = S3.M([r"\frac{d^{n+1}}{dx^{n+1}}", "=", S3.DN, S3.LP, r"\frac{d}{dx}", r"\,\cdots", S3.RP], 44)
        hero = S3.hero_line()
        hero.scale(44 / 56)
        hn = MathTex(r"H_{n+1}", font_size=44, color=YELLOW)
        lb = VGroup(hn, hero).arrange(RIGHT, buff=0.2)
        lb.next_to(la, DOWN, buff=0.55)
        la.shift(RIGHT * (lb[1][0].get_left()[0] - la[1].get_left()[0]))
        self.v2 = fit(VGroup(la, lb), 1)
        self.p2 = dict(la=la, lb=lb, hero=hero)
        self.c2 = caption("peel off one derivative", 1)

        # r3: the struck first line, the two survivors, Pascal's row 4 with 4 1 lit
        M, B, F, G = S4.M, S4.B, S4.F, S4.G
        l1 = M([B("n", 0), F("n"), G(0), "+", B("n", 1), F("n-1"), G(1), "+", r"\cdots", "+"], 40)
        l2 = M([B("n", "n-1"), F(1), G("n-1"), "+", B("n", "n"), F(0), G("n")], 40)
        l2.next_to(l1, DOWN, buff=0.4).align_to(l1, LEFT)
        prow = P4.pascal_row(4)
        prow.scale(40 / P4.PASCAL_SIZE)
        prow.next_to(l2, DOWN, buff=0.45).set_x(l1.get_x())
        groups = [VGroup(*l1[0:3]), VGroup(*l1[4:7]), l1[8]]
        strikes = VGroup(*[Line(g.get_left() + LEFT * 0.08, g.get_right() + RIGHT * 0.08,
                                color=RED, stroke_width=5) for g in groups])
        self.v3 = fit(VGroup(l1, strikes, l2, prow), 2)
        self.p3 = dict(l1=l1, l2=l2, strikes=strikes, prow=prow)
        self.c3 = caption("x runs out: two terms", 2)

        # r4: the boxed recursion over the full ladder (s5's box, s2's ladder, compact)
        rec0 = S5.boxed_recursion()
        eq = rec0[0].copy().scale(30 / 48)
        box = RoundedRectangle(corner_radius=0.12, width=eq.width + 0.45, height=eq.height + 0.32)
        box.set_stroke(YELLOW, 2.5).set_fill(opacity=0).move_to(eq)
        cap = MathTex(r"n \ge 1", font_size=28, color=FG).next_to(box, RIGHT, buff=0.25)
        rec = VGroup(eq, box, cap)
        lad = mini_ladder(S2)
        lad.next_to(rec, DOWN, buff=0.18)
        lad.shift(RIGHT * (box.get_x() - lad.get_x()))
        self.v4 = fit(VGroup(rec, lad), 3)
        self.p4 = dict(rec=rec, lad=lad)
        self.c4 = caption("the recursion builds the ladder", 3)

    def dim(self, *mobs):
        anims = []
        for m in mobs:
            m.save_state()
            anims.append(Transform(m, dimmed(m, DIM_K)))
        return anims

    # ------------------------------------------------------------------ c5.recap.1
    def clip1(self):
        p1, p2, p3, p4 = self.p1, self.p2, self.p3, self.p4
        head = T("Recap", 40).move_to([0, HEAD_Y, 0])
        self.head = head
        with self.say("c5.recap.1") as c:
            self.play(*appear(head), run_time=1.0)

            # r1
            c.wait_until("r1")
            self.play(*appear(p1["dl"], p1["d"], lag=0.4, shift=None), run_time=1.6)
            c.wait_until(own_word=self.c1[0])
            self.play(*appear(self.c1), run_time=1.0)
            c.wait_until("factor in front")
            self.play(*appear(p1["m"], shift=None), run_time=min(1.0, c.until("removes")))
            c.wait_until("removes")
            pair = [p1["d"][1], p1["m"][1]]
            self.play(*flash(pair), *set_alpha(pair, 0.3), run_time=1.0)
            self.play(*appear(p1["arr"], p1["h"], lag=0.3, shift=None),
                      run_time=max(0.8, min(1.4, c.until("r2") - 0.1)))
            settle(self, self.v1)

            # r2
            c.wait_until("r2")
            self.play(*self.dim(self.v1, self.c1), *appear(p2["la"], shift=None), run_time=1.5)
            c.wait_until(own_word=self.c2[0])
            self.play(*appear(self.c2), run_time=1.0)
            c.wait_until("left with")
            self.play(*appear(p2["lb"], shift=None), run_time=1.4)
            hero = p2["hero"]
            c.wait_until("times the gaussian")
            self.play(FlashAround(VGroup(hero[6], hero[7]), time_width=1.5),
                      run_time=min(1.4, c.until("r3")))
            settle(self, self.v2)

            # r3
            c.wait_until("r3")
            self.play(*self.dim(self.v2, self.c2),
                      *appear(p3["l1"], p3["l2"], self.c3, lag=0.3, shift=None), run_time=1.6)
            c.wait_until("after one derivative")
            self.play(restyle(p3["l1"], op=0.4), *[Create(s) for s in p3["strikes"]], run_time=1.2)
            c.wait_until("two terms")
            prow = p3["prow"]
            self.play(*appear(prow, shift=None), FlashAround(p3["l2"], time_width=1.5, buff=0.12),
                      run_time=1.2)
            self.play(*set_alpha([prow[0], prow[1], prow[2]], 0.3), *flash([prow[3], prow[4]]),
                      run_time=min(1.2, c.until("r4")))
            settle(self, self.v3)

            # r4
            c.wait_until("r4")
            self.play(*self.dim(self.v3, self.c3), *appear(p4["rec"], shift=None), run_time=1.5)
            c.wait_until(own_word=self.c4[0])
            self.play(*appear(self.c4), run_time=1.0)
            c.wait_until("recursion", nth=1)
            lad = p4["lad"]
            self.play(*appear(lad.box, lad.bars, shift=None),
                      *appear(*lad.rungs, lag=0.15, shift=0.15 * UP), run_time=1.5)
            settle(self, self.v4)
            c.wait_until("ladder")
            self.play(*[Restore(m) for m in (self.v1, self.c1, self.v2, self.c2, self.v3, self.c3)],
                      run_time=min(1.2, c.until(floor=0.6)))

    # ------------------------------------------------------------------ c5.recap.2
    def clip2(self):
        card = i1_card()
        card.scale(0.88)
        card.move_to([0, 3.55 - card.height / 2, 0])
        self.card = card
        v3 = self.v3
        v3.generate_target()
        v3.target.scale_to_fit_width(4.7)
        v3.target.move_to([4.2, -2.1, 0])

        X0 = -6.3
        h1 = MathTex("g", "=", GAUSS2, font_size=44, color=FG)
        h1[0].set_color(PURPLE)
        h1[2].set_color(PURPLE)
        h2 = MathTex("g'", "=", "-", "x", "g", font_size=44, color=FG)
        h2[0].set_color(PURPLE)
        h2[3].set_color(BLUE)
        h2[4].set_color(PURPLE)
        h3 = MathTex(r"\text{differentiate } n+1 \text{ times: Leibniz on }", "x", r"\,", "g",
                     font_size=38, color=FG)
        h3[1].set_color(BLUE)
        h3[3].set_color(PURPLE)
        h1.move_to([0, -0.75, 0]).align_to(np.array([X0, 0, 0]), LEFT)
        h2.move_to([0, -1.7, 0])
        h2.shift(RIGHT * (h1[1].get_x() - h2[1].get_x()))
        h3.move_to([0, -2.6, 0]).align_to(h1, LEFT)
        self.hints = (h1, h2, h3)

        with self.say("c5.recap.2") as c:
            gone = [self.head, self.v1, self.c1, self.v2, self.c2, self.c3, self.v4, self.c4]
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during([MoveToTarget(v3)], 0.4, 0.85),
                      *during(appear(card, shift=None), 0.5, 1.0),
                      run_time=max(1.8, min(2.6, c.until("gdef") - 0.2)))
            c.wait_until("gdef")
            self.play(*appear(h1), run_time=1.2)
            c.wait_until("gprime")
            self.play(*appear(h2), run_time=1.2)
            c.wait_until("hint")
            self.play(*appear(h3), run_time=1.4)

            # the "two terms" tag points back at r3's survivors
            l2 = self.p3["l2"]
            tag = T("two terms", 30, YELLOW)
            tag.next_to(h3, DOWN, buff=0.25).align_to(h3, RIGHT)
            arrow = Arrow(tag.get_right() + RIGHT * 0.1, l2.get_left() + LEFT * 0.08 + DOWN * 0.05,
                          buff=0.05, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.15)
            c.wait_until("two terms")
            self.play(*appear(tag), GrowArrow(arrow), FlashAround(l2, time_width=1.5, buff=0.12),
                      run_time=min(1.5, c.until(floor=0.8)))
            self.tag, self.arrow = tag, arrow

    # ------------------------------------------------------------------ c5.recap.3
    def clip3(self):
        fig = self.H6.notes_figure()
        fig.remove(fig.dots)
        with self.say("c5.recap.3") as c:
            sweep_clear(self, FadeIn(fig), run_time=max(1.2, min(1.6, c.until("shape") - 0.1)))
            c.wait_until("shape")
            self.play(*appear(fig.peak, fig.valley, lag=0.3, shift=0.2 * DOWN), run_time=1.2)
            settle(self, fig, add=[fig.peak, fig.valley])
