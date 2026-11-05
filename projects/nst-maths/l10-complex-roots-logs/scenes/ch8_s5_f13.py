"""Chapter 8, scene 5: F13, three sums (half-angle trick, curling chain, conjugate). Clips c8.f13.1 – c8.f13.5.

Shared piece for the recap (ch8_s8_end):
  recap_panel()  VGroup(plane, chain, dashed, total): the θ = 0.4 curling chain of five GOLD unit
                 arrows on the Argand plane, its YELLOW total along the dashed 3θ line, as at {length}.
                 Parts: .plane .chain .dashed .total. Positioned as in this scene (origin at PO).
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

PO = np.array([-5.2, -2.0, 0.0])   # plane origin on screen
PU = 1.2                            # unit length
X_RANGE = (-1.1, 5.2)               # plane extent, in units
Y_RANGE = (-1.2, 4.6)
TH = 0.4                            # θ in radians
COL_X = 4.0                         # right-hand column centre
EQ_X = -1.0                         # x of the aligned "=" in the half-angle derivation


# ------------------------------------------------------------------ plane and chain
def plane():
    """ch2's argand_plane look (faint half-unit grid, Re/Im axes, DIM unit circle), asymmetric extent."""
    step = PU / 2
    grid = VGroup()
    x0, x1 = PO[0] + X_RANGE[0] * PU, PO[0] + X_RANGE[1] * PU
    y0, y1 = PO[1] + Y_RANGE[0] * PU, PO[1] + Y_RANGE[1] * PU
    for k in range(int(np.ceil(X_RANGE[0] * 2)), int(np.floor(X_RANGE[1] * 2)) + 1):
        if k:
            x = PO[0] + k * step
            grid.add(Line([x, y0, 0], [x, y1, 0]))
    for k in range(int(np.ceil(Y_RANGE[0] * 2)), int(np.floor(Y_RANGE[1] * 2)) + 1):
        if k:
            y = PO[1] + k * step
            grid.add(Line([x0, y, 0], [x1, y, 0]))
    grid.set_stroke(DIM, 1, opacity=0.3)
    ax_kw = dict(buff=0, stroke_width=2.5, tip_length=0.18, max_tip_length_to_length_ratio=0.1, color=FG)
    x_ax = Arrow([x0, PO[1], 0], [x1, PO[1], 0], **ax_kw).set_opacity(0.7)
    y_ax = Arrow([PO[0], y0, 0], [PO[0], y1, 0], **ax_kw).set_opacity(0.7)
    re = MathTex(r"\mathrm{Re}", font_size=34, color=DIM).next_to(x_ax.get_end(), DOWN, buff=0.15).shift(0.25 * LEFT)
    im = MathTex(r"\mathrm{Im}", font_size=34, color=DIM).next_to(y_ax.get_end(), RIGHT, buff=0.15).shift(0.2 * DOWN)
    circle = Circle(radius=PU, color=DIM, stroke_width=2.5).move_to(PO)
    g = VGroup(grid, x_ax, y_ax, circle, re, im)
    g.grid, g.axes, g.circle = grid, VGroup(x_ax, y_ax), circle
    return g


def chain_points(theta, r=1.0, n=5):
    pts, z = [PO.copy()], 0j
    for k in range(1, n + 1):
        z += (r * np.exp(1j * theta)) ** k
        pts.append(PO + PU * np.array([z.real, z.imag, 0]))
    return pts


def _arrow(a, b, color, width=6, tip=0.26):
    length = max(np.linalg.norm(b - a), 1e-3)
    return Arrow(a, b, buff=0, stroke_width=width, tip_length=min(tip, 0.45 * length),
                 max_tip_length_to_length_ratio=0.45, color=color)


def chain_arrows(theta, r=1.0):
    p = chain_points(theta, r)
    return VGroup(*[_arrow(p[k], p[k + 1], GOLD) for k in range(5)])


def total_arrow(theta, r=1.0):
    return _arrow(PO, chain_points(theta, r)[-1], YELLOW, width=7, tip=0.3).set_z_index(-1)


def dashed_3theta(theta=TH):
    d = np.array([np.cos(3 * theta), np.sin(3 * theta), 0])
    return DashedLine(PO, PO + 4.9 * PU * d, dash_length=0.12, color=FG, stroke_width=2.5).set_opacity(0.6)


def re_shadow(theta, r=1.0):
    x = chain_points(theta, r)[-1][0]
    return Line(PO, [max(x, PO[0] + 1e-3), PO[1], 0], color=BLUE, stroke_width=9).set_z_index(-2)


def im_shadow(theta, r=1.0):
    y = chain_points(theta, r)[-1][1]
    return Line(PO, [PO[0], max(y, PO[1] + 1e-3), 0], color=PINK, stroke_width=9).set_z_index(-2)


def recap_panel():
    """The θ = 0.4 curling chain with its YELLOW total along 3θ, on the plane (as at {length})."""
    pl, ch, da, to = plane(), chain_arrows(TH), dashed_3theta(), total_arrow(TH)
    g = VGroup(pl, da, to, ch)
    g.plane, g.chain, g.dashed, g.total = pl, ch, da, to
    return g


def boxed(mob, color=YELLOW, buff=0.2):
    return SurroundingRectangle(mob, color=color, buff=buff, stroke_width=3)


def strike(mob):
    return Line(mob.get_corner(DL) + 0.05 * DL, mob.get_corner(UR) + 0.05 * UR, color=RED, stroke_width=5)


class F13ThreeSums(NarratedScene):
    def construct(self):
        self.card()
        self.complex_sum()
        self.half_angle()
        self.picture()
        self.third_sum()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c8.f13.1
    def card(self):
        s1 = load_scene("ch8_s1_intro")
        with self.say("c8.f13.1") as c:
            row = s1.card_row()
            self.play(FadeIn(row), run_time=0.9)  # early: the chapter's question index, a reprise of s1
            f13 = row.cards[4]
            others = [cd for i, cd in enumerate(row.cards) if i != 4]
            intro = T("Evaluate the following sums:", size=36)
            sums = MathTex(r"\text{(a)}\ \sum_{n=1}^{5}\cos n\theta \qquad \text{(b)}\ \sum_{n=1}^{5}\sin n\theta"
                           r"\qquad \text{(c)}\ \sum_{n=1}^{5} r^n\cos n\theta", font_size=44)
            q = s1.question_card("F13", [intro, sums])
            self.play(*during(disappear(*others), 0, 0.35),
                      *during([FadeOut(f13.icon), FadeOut(f13.tag)], 0, 0.35),
                      *during(TransformFromCopy(f13.box, q.box), 0.3, 1),
                      *during(f13.label.animate.scale(52 / 46).move_to(q.label), 0.3, 1),
                      *during(FadeOut(f13.box), 0.6, 1),
                      run_time=1.6)
            self.remove(*f13.get_family())
            self.add(q.label)
            c.wait_until(own_word=intro)
            self.play(*appear(q.icon, intro, sums, lag=0.5), run_time=min(1.8, c.until("stop")))
            self.q = q
            c.wait_until("stop")
            self.play(FlashAround(q.icon, run_time=1.5, time_width=1.5, buff=0.15))

    # ------------------------------------------------------------------ c8.f13.2
    def complex_sum(self):
        with self.say("c8.f13.2") as c:
            A = MathTex(r"\sum_{n=1}^{5}\cos n\theta", r"+\,i", r"\sum_{n=1}^{5}\sin n\theta", "=",
                        r"\sum_{n=1}^{5} e^{in\theta}", font_size=48)
            A[0].set_color(BLUE)
            A[2].set_color(PINK)
            A.move_to(1.5 * UP)
            self.play(*during(disappear(self.q), 0, 0.45), *during(appear(A), 0.45, 1),
                      run_time=min(1.8, c.until("gp")))
            c.wait_until("gp")
            B = MathTex("=", r"e^{i\theta}", r"\,\frac{1-e^{5i\theta}}{1-e^{i\theta}}", font_size=44)
            B.shift(np.array([A[3].get_x() - B[0].get_x(), -0.6, 0]))
            self.play(*appear(B), run_time=1.2)
            frac = B[2]
            t_first = T("first term", size=30, color=YELLOW).next_to(B[1], DOWN, buff=0.45)
            t_first.shift(0.45 * LEFT)
            t_ratio = T("ratio", size=30, color=YELLOW).next_to(frac, DOWN, buff=0.25)
            t_ratio.set_x(frac.get_right()[0] - 0.45)
            t_five = T("5 terms", size=30, color=YELLOW).next_to(frac, UP, buff=0.2)
            t_five.set_x(frac.get_x() + 0.1)
            c.wait_until("e to the eye theta times")
            self.play(*appear(t_first), run_time=0.9)
            c.wait_until("five eye theta")
            self.play(*appear(t_five), run_time=0.9)
            c.wait_until("over one minus")
            self.play(*appear(t_ratio), run_time=0.9)
            self.A, self.B, self.tags = A, B, [t_first, t_five, t_ratio]

    # ------------------------------------------------------------------ c8.f13.3
    def half_angle(self):
        A, B = self.A, self.B
        with self.say("c8.f13.3") as c:
            PB = MathTex(r"\sum_{n=1}^{5} e^{in\theta}", font_size=44).next_to(B, LEFT, buff=0.15)
            trick = T("half-angle trick", size=34, color=YELLOW).move_to([4.9, 2.95, 0])
            self.play(*during(disappear(A), 0, 0.45), *during(appear(PB), 0.45, 1), run_time=1.2)
            c.wait_until("quicker route")
            self.play(*appear(trick), run_time=1.0)

            c.wait_until("factor")
            row_w = PB.width + 0.15 + B.width
            PB.generate_target()
            B.generate_target()
            PB.target.move_to([-1.0 - row_w / 2 + PB.width / 2, 2.95, 0])
            B.target.next_to(PB.target, RIGHT, buff=0.15)
            self.play(*during(disappear(*self.tags), 0, 0.45), *during([MoveToTarget(PB), MoveToTarget(B)], 0.2, 1),
                      run_time=1.2)
            F1 = MathTex(r"1-e^{5i\theta}", "=", r"e^{5i\theta/2}",
                         r"\left(e^{-5i\theta/2}-e^{5i\theta/2}\right)", font_size=40)
            F1.shift([EQ_X - F1[1].get_x(), 1.75 - F1.get_y(), 0])
            self.play(*appear(F1), run_time=1.5)
            c.wait_until("take out")
            self.play(*recolor(F1[3], YELLOW), FlashAround(F1[3], run_time=1.5, time_width=1.5), run_time=1.5)
            F1b = MathTex("=", r"-2i", r"\,e^{5i\theta/2}", r"\sin\tfrac{5\theta}{2}", font_size=40)
            F1b.shift([EQ_X - F1b[0].get_x(), 0.85 - F1b.get_y(), 0])
            F1b[1].set_color(YELLOW)
            F1b[3].set_color(YELLOW)
            n78 = MathTex("(78)", font_size=32, color=DIM).next_to(F1b, RIGHT, buff=0.6)
            c.wait_until("leaving")
            self.play(*appear(F1b, n78, lag=0.4), run_time=min(1.5, c.until("cancel")))

            c.wait_until("cancel")
            F2 = MathTex(r"1-e^{i\theta}", "=", r"-2i", r"\,e^{i\theta/2}", r"\sin\tfrac{\theta}{2}", font_size=40)
            F2.shift([EQ_X - F2[1].get_x(), -0.15 - F2.get_y(), 0])
            F2[2].set_color(YELLOW)
            F2[4].set_color(YELLOW)
            self.play(*appear(F2), run_time=1.2)
            c.wait_until("cancel")
            s1, s2 = strike(F1b[1]), strike(F2[2])
            self.play(Create(s1), Create(s2), run_time=0.9)

            c.wait_until("result")
            comb = MathTex(r"e^{i\theta}\cdot\frac{e^{5i\theta/2}}{e^{i\theta/2}}", "=", r"e^{3i\theta}", font_size=40)
            comb.shift([EQ_X - comb[1].get_x(), -1.3 - comb.get_y(), 0])
            comb[2].set_color(YELLOW)
            self.play(*appear(comb), run_time=1.2)
            res = MathTex(r"\sum_{n=1}^{5} e^{in\theta}", "=",
                          r"e^{3i\theta}\,\frac{\sin(5\theta/2)}{\sin(\theta/2)}", font_size=44)
            res.move_to([EQ_X + 0.4, -2.85, 0])
            box = boxed(res)
            c.wait_until("times the sine")
            self.play(*appear(res), time_span(FadeIn(box), 0.6, 1.4), run_time=1.4)
            self.res = VGroup(res, box)
            self.board = [PB, B, trick, F1, F1b, n78, F2, s1, s2, comb]

    # ------------------------------------------------------------------ c8.f13.4
    def picture(self):
        with self.say("c8.f13.4") as c:
            pl = plane()
            self.res.generate_target()
            self.res.target.scale(0.8).move_to([COL_X, 2.7, 0])
            sweep_clear(self, time_span(FadeIn(pl), 1.15, 1.8), time_span(MoveToTarget(self.res), 0.8, 1.4),
                        keep=[self.res], run_time=1.8)
            chain = chain_arrows(TH)
            self.play(*during([GrowArrow(a) for a in chain[:1]], 0, 0.36),
                      *during([GrowArrow(a) for a in chain[1:2]], 0.16, 0.52),
                      *during([GrowArrow(a) for a in chain[2:3]], 0.32, 0.68),
                      *during([GrowArrow(a) for a in chain[3:4]], 0.48, 0.84),
                      *during([GrowArrow(a) for a in chain[4:5]], 0.64, 1.0),
                      run_time=min(2.0, c.until("three theta")))
            dashed, total = dashed_3theta(), total_arrow(TH)
            c.wait_until("three theta")
            self.play(Create(dashed), GrowArrow(total), run_time=1.3)
            c.wait_until("the middle")
            self.play(FlashAround(chain[2], run_time=1.5, time_width=1.5, color=GOLD))

            c.wait_until("length")
            length = MathTex(r"|\Sigma| = \frac{\sin(5\theta/2)}{\sin(\theta/2)} \approx 4.24", font_size=38, color=GOLD)
            length.move_to([COL_X, 1.25, 0])
            self.play(*appear(length), run_time=1.2)

            c.wait_until("a_ans")
            sh_re = re_shadow(TH)
            v_re = MathTex(r"\approx 1.53", font_size=38, color=BLUE)
            v_re.move_to(PO + np.array([0.77 * PU, -0.45, 0]))
            v_re = VGroup(BackgroundRectangle(v_re, fill_opacity=0.92, buff=0.08), v_re)
            self.play(Create(sh_re), *appear(v_re), run_time=1.2)
            a_ans = MathTex(r"\text{(a)}\ \cos 3\theta\,\frac{\sin(5\theta/2)}{\sin(\theta/2)}", font_size=38, color=BLUE)
            a_ans.move_to([COL_X, -0.2, 0])
            a_box = boxed(a_ans, BLUE, 0.15)
            c.wait_until("cosine three theta")
            self.play(*appear(a_ans), time_span(FadeIn(a_box), 0.5, 1.2), run_time=1.2)

            c.wait_until("b_ans")
            sh_im = im_shadow(TH)
            v_im = MathTex(r"\approx 3.95", font_size=38, color=PINK)
            v_im.move_to(PO + np.array([-0.66, 2.0 * PU, 0]))
            v_im = VGroup(BackgroundRectangle(v_im, fill_opacity=0.92, buff=0.08), v_im)
            self.play(Create(sh_im), *appear(v_im), run_time=1.2)
            b_ans = MathTex(r"\text{(b)}\ \sin 3\theta\,\frac{\sin(5\theta/2)}{\sin(\theta/2)}", font_size=38, color=PINK)
            b_ans.move_to([COL_X, -1.7, 0])
            b_box = boxed(b_ans, PINK, 0.15)
            c.wait_until("sine three theta")
            self.play(*appear(b_ans), time_span(FadeIn(b_box), 0.5, 1.2), run_time=1.2)

            # {edge}: θ → a whole number of turns; the chain straightens along the real axis
            c.wait_until("edge")
            th, rr = ValueTracker(TH), ValueTracker(1.0)
            self.th, self.rr = th, rr
            ch_d = always_redraw(lambda: chain_arrows(th.get_value(), rr.get_value()))
            to_d = always_redraw(lambda: total_arrow(th.get_value(), rr.get_value()))
            re_d = always_redraw(lambda: re_shadow(th.get_value(), rr.get_value()))
            im_d = always_redraw(lambda: im_shadow(th.get_value(), rr.get_value()))
            self.remove(*chain, total, sh_re, sh_im)
            self.add(re_d, im_d, to_d, ch_d)
            self.play(*disappear(v_re, v_im, dashed), run_time=0.6)
            self.play(th.animate.set_value(0.0), run_time=min(1.8, c.until("five and zero")))
            edge = MathTex(r"\theta = 2\pi m:\quad \text{(a)} = 5,\ \ \text{(b)} = 0", font_size=40)
            edge[0][2:5].set_color(TEAL)
            edge.move_to([COL_X, -3.0, 0])
            c.wait_until("five and zero")
            self.play(*appear(edge), run_time=1.0)
            self.ch_d, self.to_d, self.re_d, self.im_d = ch_d, to_d, re_d, im_d
            self.edge = edge
            self.pl = pl

    # ------------------------------------------------------------------ c8.f13.5
    def third_sum(self):
        th, rr = self.th, self.rr
        with self.say("c8.f13.5", gap=3.0) as c:
            P1 = MathTex(r"\sum_{n=1}^{5} r^n\cos n\theta", font_size=38)
            E1 = MathTex("=", r"\mathrm{Re}\sum_{n=1}^{5}\left(re^{i\theta}\right)^n", font_size=38)
            L2 = MathTex("=", r"\mathrm{Re}\left[\frac{re^{i\theta}\left(1-r^5e^{5i\theta}\right)}{1-re^{i\theta}}\right]",
                         font_size=38)
            P1.move_to([1.6 + P1.width / 2, 2.7, 0])
            E1.shift([2.1 - E1[0].get_x(), 1.55 - E1.get_y(), 0])
            L2.shift([2.1 - L2[0].get_x(), 0.2 - L2.get_y(), 0])
            c.wait_until("ratio is")
            sweep_clear(self, *appear(P1, E1, L2, lag=0.5), keep=[self.pl, self.ch_d], run_time=2.2)
            c.wait_until("the arrows")
            self.play(rr.animate.set_value(0.8), run_time=min(1.5, c.until("or grow") + 0.3))   # shrink on "shrink"
            self.play(th.animate.set_value(TH), run_time=min(1.5, c.until("trick fails")))
            trick = T("half-angle trick", size=34, color=YELLOW).move_to([COL_X - 0.3, -1.4, 0])
            st = strike(trick)
            x = cross_mark().next_to(trick, RIGHT, buff=0.3)
            c.wait_until("trick fails")
            self.play(*appear(trick), run_time=0.8)
            self.play(Create(st), FadeIn(x, scale=0.6), run_time=0.8)

            # {conj}: the plane goes; the fraction moves up and takes the conjugate
            c.wait_until("one minus r times e")
            mult = MathTex(r"\times\frac{1-re^{-i\theta}}{1-re^{-i\theta}}", font_size=44, color=PURPLE)
            k = 44 / 38
            w = k * (P1.width + L2.width) + mult.width + 0.5
            P1.generate_target()
            L2.generate_target()
            P1.target.scale(k).move_to([-w / 2 + k * P1.width / 2, 2.55, 0])
            L2.target.scale(k).next_to(P1.target, RIGHT, buff=0.25)
            mult.next_to(L2.target, RIGHT, buff=0.25)
            sweep_clear(self, MoveToTarget(P1), MoveToTarget(L2), keep=[P1, L2], run_time=1.4)
            self.play(*appear(mult), run_time=1.0)

            c.wait_until("bottom")
            bot = MathTex(r"\text{bottom}", "=", r"1-2r\cos\theta+r^2", font_size=46)
            bot[2].set_color(BLUE)
            bot.move_to([0, 0.95, 0])
            self.play(*appear(bot), run_time=1.2)

            c.wait_until("top")
            top = MathTex(r"\text{top}", "=", r"re^{i\theta}", r"-r^2", r"-r^6e^{6i\theta}", r"+r^7e^{5i\theta}",
                          font_size=46)
            top.move_to([0, -0.25, 0])
            top.shift([bot[1].get_x() - top[1].get_x(), 0, 0])
            self.play(*appear(top), run_time=1.0)
            box = token_box(top[2], top)
            c.wait_until("r cosine theta")
            self.play(FadeIn(box), run_time=0.6)
            for k, cue in ((3, "minus r squared"), (4, "sixth"), (5, "seventh")):
                c.wait_until(cue)
                self.play(Transform(box, token_box(top[k], top)), run_time=0.6)

            c.wait_until("c_edge")
            ans = MathTex(r"\text{(c)} = \frac{r\cos\theta-r^2-r^6\cos 6\theta+r^7\cos 5\theta}{1-2r\cos\theta+r^2}",
                          font_size=46)
            ans.move_to([0, -1.95, 0])
            a_box = boxed(ans)
            self.play(FadeOut(box), *appear(ans), time_span(FadeIn(a_box), 0.6, 1.5), run_time=1.5)
            edge = MathTex(r"=5\ \ \text{if}\ \ re^{i\theta}=1", font_size=42)
            edge.next_to(a_box, DOWN, buff=0.3)
            c.wait_until("unless")
            self.play(*appear(edge), run_time=1.0)
