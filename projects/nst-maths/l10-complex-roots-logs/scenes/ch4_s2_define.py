"""Chapter 4, scene 2: from the definition e^w = z to ln z = ln|z| + i(arg z + 2πn). Clips c4.def.1 – c4.def.6."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

LEFT_X = -6.3                          # left edge of the derivation column
Y_Q, Y_D, Y_A, Y_B, Y_M, Y_V = 3.35, 2.4, 1.25, -0.05, -1.65, -3.0

# Argand inset (clip 4): copied from ch2_s1_hook.argand_plane, with its own origin and unit.
U = 1.3
O = np.array([4.95, -1.15, 0])
THETA = 50 * DEGREES


def P(x, y):
    return O + U * np.array([x, y, 0])


def argand_plane(xr=(-1.3, 1.05), yr=(-1.4, 1.4)):
    """Re/Im axes, faint grid, DIM unit circle (PLAN.md running visual)."""
    grid = VGroup()
    for x in range(int(np.ceil(xr[0])), int(np.floor(xr[1])) + 1):
        if x:
            grid.add(Line(P(x, yr[0]), P(x, yr[1]), stroke_width=1, color=DIM, stroke_opacity=0.3))
    for y in range(int(np.ceil(yr[0])), int(np.floor(yr[1])) + 1):
        if y:
            grid.add(Line(P(xr[0], y), P(xr[1], y), stroke_width=1, color=DIM, stroke_opacity=0.3))
    xax = Arrow(P(xr[0], 0), P(xr[1] + 0.2, 0), buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    yax = Arrow(P(0, yr[0]), P(0, yr[1] + 0.2), buff=0, stroke_width=2.5, color=FG,
                max_tip_length_to_length_ratio=0.04)
    re = T("Re", size=30).next_to(xax.get_end(), DOWN, buff=0.15)
    im = T("Im", size=30).next_to(yax.get_end(), RIGHT, buff=0.15)
    unit = Circle(radius=U, color=DIM, stroke_width=2).move_to(O)
    return VGroup(grid, xax, yax, re, im, unit)


def unit_arrow(angle, color):
    return Arrow(O, P(np.cos(angle), np.sin(angle)), buff=0, color=color, stroke_width=5,
                 max_tip_length_to_length_ratio=0.18)


# ---------------------------------------------------------------- maths text
def mt(parts, size=44):
    """MathTex from (tex, colour) pairs, one submobject per pair; colour may be a dict
    {glyph index: colour} over an FG part (e.g. e^{i\\theta}: {1: PINK, 2: YELLOW})."""
    m = MathTex(*[p for p, _ in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        if isinstance(col, dict):
            sub.set_color(FG)
            for k, cc in col.items():
                sub[k].set_color(cc)
        else:
            sub.set_color(col)
    return m


E_ITH = {1: PINK, 2: YELLOW}           # e^{i\theta}
E_IV = {1: PINK}                       # e^{iv}


def left_at(m, y):
    return m.move_to([0, y, 0]).align_to([LEFT_X, 0, 0], LEFT)


def result_box(size=60):
    """The YELLOW-boxed result ∴ ln z = ln|z| + i(arg z + 2πn); .formula .rect; centred at ORIGIN."""
    f = mt([(r"\therefore\quad", FG), (r"\ln z", FG), ("=", FG), (r"\ln|z|", GOLD), ("+", FG),
            ("i", PINK), (r"\big(", FG), (r"\arg z", YELLOW), ("+", FG), (r"2\pi n", TEAL),
            (r"\big)", FG)], size)
    rect = SurroundingRectangle(f, color=YELLOW, buff=0.32, stroke_width=4)
    g = VGroup(f, rect)
    g.formula, g.rect = f, rect
    return g


def exp_inset(o=np.array([5.25, -2.85, 0]), sx=0.85, sy=0.9, u0=-2.6, u1=1.45, show_level=True):
    """Graph of e^u: axes, BLUE curve, label; optional GOLD level |z| = 2 with drop to ln|z|."""
    def Q(u, y):
        return o + np.array([sx * u, sy * y, 0])
    ax_kw = dict(buff=0, stroke_width=2.5, color=FG, max_tip_length_to_length_ratio=0.05)
    xax = Arrow(Q(u0, 0), Q(u1 + 0.25, 0), **ax_kw)
    yax = Arrow(Q(0, -0.25), Q(0, np.exp(u1) + 0.3), **ax_kw)
    ulab = MathTex("u", font_size=34).next_to(xax.get_end(), DOWN, buff=0.12)
    curve = ParametricFunction(lambda t: Q(t, np.exp(t)), t_range=[u0, u1, 0.02], color=BLUE, stroke_width=5)
    clab = MathTex("e^u", font_size=40, color=BLUE).next_to(curve.get_end(), LEFT, buff=0.15)
    g = VGroup(xax, yax, ulab, curve, clab)
    g.axes, g.curve, g.clab, g.Q = VGroup(xax, yax, ulab), curve, clab, Q
    lv = 2.0
    ul = np.log(lv)
    g.level = Line(Q(u0, lv), Q(u1, lv), color=GOLD, stroke_width=3)
    g.zlab = MathTex("|z|", font_size=36, color=GOLD).next_to(g.level.get_start(), UP, buff=0.12)
    g.cross_pt = Q(ul, lv)
    g.foot = Q(ul, 0)
    g.drop = DashedLine(g.cross_pt, g.foot, color=GOLD, stroke_width=3)
    g.dot = Dot(g.cross_pt, radius=0.09, color=GOLD)
    g.lnlab = MathTex(r"\ln|z|", font_size=36, color=GOLD).next_to(g.foot, DOWN, buff=0.18)
    return g


def fly_lin(src, dst, arc=None):
    """fly() at constant speed, so the copy has left its source before it shows."""
    anims = fly(src, dst, arc=arc)
    for a in anims:
        a.rate_func = linear
    return anims


class Define(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the question, the definition
    def clip1(self):
        with self.say("c4.def.1") as c:
            q = mt([(r"\text{If }z = x + ", FG), ("i", PINK), (r"y = ", FG), ("|z|", GOLD),
                    (r"e^{i\theta}", E_ITH), (r"\text{ with }x, y, ", FG), (r"\theta", YELLOW),
                    (r"\in\mathbb{R}\text{, then what is }\ln z\,?", FG)], 46)
            q.move_to([0, Y_Q, 0])
            if q.width > 13:
                q.scale_to_fit_width(13)
            self.q = q
            self.play(*appear(q), run_time=1.2)  # early: the notes' question, read in full straight after
            c.wait_until("define")

            d = mt([(r"\text{For }z \neq 0,\ \text{define}\quad", RED), (r"w = \ln z", RED),
                    (r"\quad\text{if}\quad", RED), (r"e^w = z.", RED)], 54)
            d.move_to([0, Y_D, 0])
            self.d = d
            self.play(*appear(d), run_time=min(1.3, c.until("For any")))
            c.wait_until("same")
            self.play(*set_alpha([q], 0.35), run_time=1.0)
            self.play(FlashUnder(d[3], color=RED, run_time=1.6, time_width=1.5))

    # ------------------------------------------------------------ write w and z, expand
    def clip2(self):
        with self.say("c4.def.2") as c:
            self.play(FlashAround(self.d[3], color=YELLOW, run_time=min(1.6, c.until("w")), time_width=1.5))
            c.wait_until("w")

            A = mt([(r"\text{write}\quad", FG), (r"w = u + ", FG), ("i", PINK), ("v", FG),
                    (r"\quad\text{and}\quad", FG), ("z = ", FG), ("|z|", GOLD), (r"e^{i\theta}", E_ITH)], 52)
            left_at(A, Y_A)
            A1, A2 = VGroup(*A[0:4]), VGroup(*A[4:8])
            self.play(*appear(A1), run_time=1.2)
            c.wait_until("z")
            self.play(*appear(A2), run_time=1.2)
            c.wait_until("expand")

            B = mt([("e^w", FG), ("=", FG), ("e^u", GOLD), (r"\cdot", FG), (r"e^{iv}", E_IV),
                    ("=", FG), ("|z|", GOLD), (r"e^{i\theta}", E_ITH)], 66)
            left_at(B, Y_B)
            B1, B2 = VGroup(*B[0:5]), VGroup(*B[5:8])
            self.play(FlashUnder(VGroup(*A[1:4]), run_time=1.6, time_width=1.5),
                      *during(appear(B1, shift=0.4 * DOWN), 0.25, 1), run_time=min(1.8, 0.7 * c.until("equal")))
            c.wait_until("equal")
            self.play(FlashUnder(VGroup(*A[5:8]), run_time=1.6, time_width=1.5),
                      *during(appear(B2, shift=0.4 * DOWN), 0.25, 1), run_time=min(1.8, 0.8 * c.until()))
            self.A, self.B = A, B
            self.A_parts = [A1, A2]

    # ------------------------------------------------------------ lengths: u = ln|z|
    def clip3(self):
        A, B = self.A, self.B
        with self.say("c4.def.3") as c:
            self.play(*set_alpha(self.A_parts, 0.4), run_time=1.0)
            tag1 = T("length 1", 30, color=DIM).next_to(B[4], DOWN, buff=0.18)
            tag2 = T("length 1", 30, color=DIM).next_to(B[7], DOWN, buff=0.18)
            tag2.match_y(tag1).align_to(B[7], LEFT).shift(0.05 * RIGHT)
            c.wait_until(own_word=tag1)
            self.play(*appear(tag1, tag2, lag=0.3), run_time=1.2)
            c.wait_until("mod")

            M = mt([("e^u", GOLD), ("=", GOLD), ("|z|", GOLD), (r"\quad\text{(modulus)}", DIM)], 62)
            M.move_to([0, Y_M, 0])
            M.shift((B[6].get_x() - M[2].get_x()) * RIGHT)
            self.play(*fly_lin(B[2], M[0], arc=-PI / 2), *fly_lin(B[6], M[2]),
                      *during(appear(M[1], M[3], shift=None), 0.55, 1), run_time=1.8)
            settle(self, M)
            c.wait_until("its answer is")

            Uline = mt([("u", GOLD), ("=", GOLD), (r"\ln|z|", GOLD), (r"\quad\text{(modulus)}", DIM)], 62)
            Uline.move_to([0, Y_M, 0]).align_to(M, LEFT)
            self.play(*edit(M, Uline), run_time=1.6)
            self.Uline = Uline
            c.wait_until("once")

            ins = exp_inset()
            self.play(*appear(ins.axes, ins.curve, ins.clab, shift=None, lag=0.3), run_time=1.5)
            self.play(Create(ins.level), *appear(ins.zlab), run_time=1.2)
            self.play(FadeIn(ins.dot, scale=0.5), run_time=0.6)
            self.play(ins.dot.animate.move_to(ins.foot), Create(ins.drop), run_time=1.4)
            self.play(*appear(ins.lnlab), run_time=1.0)
            self.ins = VGroup(ins, ins.level, ins.zlab, ins.drop, ins.dot, ins.lnlab)

    # ------------------------------------------------------------ angles: v = θ + 2πn
    def clip4(self):
        with self.say("c4.def.4") as c:
            plane = argand_plane()
            self.wait(max(0.0, min(1.0, c.until("E to the eye V points") - 1.8)))
            self.play(*during(disappear(self.ins), 0, 0.45),
                      *during(appear(plane, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("E to the eye V points")

            av = unit_arrow(THETA, GOLD).set_stroke(width=10)
            av.tip.scale(1.3, about_point=av.get_end())
            lab_v = mt([(r"e^{iv}", {0: GOLD, 1: PINK, 2: GOLD})], 46)
            lab_v.next_to(av.get_end(), UP, buff=0.2).shift(0.35 * LEFT)
            self.play(GrowArrow(av), *during(appear(lab_v), 0.4, 1), run_time=1.4)
            c.wait_until("and E to the eye theta")

            at = unit_arrow(THETA, YELLOW).set_stroke(width=3.5)
            at.tip.set_fill(YELLOW)
            ang = Arc(radius=0.4, start_angle=0, angle=THETA, arc_center=O, color=YELLOW, stroke_width=3)
            th = MathTex(r"\theta", font_size=34, color=YELLOW).move_to(O + 0.62 * np.array([np.cos(THETA / 2), np.sin(THETA / 2), 0]))
            lab_t = mt([(r"e^{i\theta}", {0: YELLOW, 1: PINK, 2: YELLOW})], 46)
            lab_t.next_to(at.get_end(), RIGHT, buff=0.2)
            self.play(GrowArrow(at), Create(ang), *during(appear(th, lab_t), 0.4, 1), run_time=1.5)
            c.wait_until("any whole number")

            turn = Arc(radius=0.72 * U, start_angle=THETA, angle=TAU, arc_center=O, color=TEAL, stroke_width=5)

            def upd(m, alpha):
                m.become(unit_arrow(THETA + alpha * TAU, YELLOW).set_stroke(width=3.5))
                m.tip.set_fill(YELLOW)
            self.play(UpdateFromAlphaFunc(at, upd), Create(turn), run_time=min(3.0, c.until("v") - 0.2))
            c.wait_until("v")

            V = mt([("v", FG), ("=", FG), (r"\theta", YELLOW), ("+", FG), (r"2\pi n", TEAL),
                    (r"\quad\text{(argument)}\qquad", DIM), (r"n \in \mathbb{Z}", FG)], 58)
            left_at(V, Y_V)
            self.play(*appear(V, shift=None), run_time=1.3)
            self.V = V
            c.wait_until("thread")
            self.play(FlashAround(V[4], color=TEAL, run_time=2, time_width=1.5),
                      ShowPassingFlash(turn.copy().set_stroke(TEAL, 9), time_width=0.4, run_time=2))

    # ------------------------------------------------------------ the result
    def clip5(self):
        Uline, V = self.Uline, self.V
        with self.say("c4.def.5") as c:
            sweep_clear(self, keep=[Uline, V], run_time=1.0)
            k = 58 / 62
            gap = 0.9
            wu, wv = Uline.width * k, V.width
            s_all = min(1.0, 12.8 / (wu + wv + gap))
            x0 = -(wu + wv + gap) * s_all / 2
            self.play(Uline.animate.scale(k * s_all).move_to([x0 + wu * s_all / 2, 2.1, 0]),
                      time_span(V.animate.scale(s_all).move_to([x0 + (wu + gap + wv / 2) * s_all, 2.1, 0]), 0.5, 1.6),
                      run_time=1.6)
            self.ufont = 58 * s_all
            c.wait_until("formula")

            rb = result_box(66).move_to([0, -0.1, 0])
            F = rb.formula
            rest = [F[i] for i in (0, 1, 2, 4, 5, 6, 7, 8, 10)]
            self.play(*fly_lin(Uline[2], F[3]), *fly_lin(V[4], F[9]),
                      *during(appear(*rest, shift=None, lag=0.05), 0.5, 1), run_time=2.0)
            self.play(FadeIn(rb.rect), run_time=1.0)
            settle(self, rb)
            c.wait_until("values")
            self.play(FlashAround(F[9], color=TEAL, run_time=1.6, time_width=1.5))

            note = T("Infinitely many values spaced 2πi apart\non a vertical line in the complex plane.",
                     34, t2c={"2πi": TEAL}, line_spacing=1.1)
            note.next_to(rb, DOWN, buff=0.7)
            c.wait_until(own_word=note)
            self.play(*appear(note), run_time=1.2)
            self.rb, self.note = rb, note

    # ------------------------------------------------------------ why z ≠ 0
    def clip6(self):
        rb = self.rb
        with self.say("c4.def.6") as c:
            sweep_clear(self, keep=[rb, self.note], run_time=1.0)
            self.play(rb.animate.scale(0.75).move_to([0, 2.9, 0]),
                      self.note.animate.scale(0.85).move_to([0, 1.7, 0]), run_time=1.0)
            ins = exp_inset(o=np.array([4.6, -3.0, 0]), sx=1.0, u0=-3.6)
            self.play(*appear(ins.axes, ins.curve, ins.clab, shift=None, lag=0.2), run_time=min(1.2, c.until("never")))
            c.wait_until("never")

            Q = ins.Q
            dot = Dot(Q(1.2, np.exp(1.2)), radius=0.09, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), run_time=0.4)
            self.play(UpdateFromAlphaFunc(dot, lambda m, a: m.move_to(Q(1.2 - 4.8 * a, np.exp(1.2 - 4.8 * a)))),
                      run_time=min(3.0, c.until("always positive")), rate_func=smooth)

            pos = mt([(r"|e^w|", FG), ("=", FG), ("e^u", BLUE), ("> 0", GREEN)], 72)
            pos.move_to([-3.4, 0.1, 0])
            self.play(*appear(pos), run_time=1.0)
            c.wait_until("So E to the W can never")

            ln0 = MathTex(r"\ln 0", font_size=90, color=RED).move_to([-3.4, -1.9, 0])
            self.play(*appear(ln0), run_time=1.0)
            c.wait_until("no logarithm")
            x = Cross(ln0, stroke_color=RED, stroke_width=6, scale_factor=1.2)
            self.play(Create(x), run_time=0.8)
