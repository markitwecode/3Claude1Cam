"""Chapter 2, scene 5: real and imaginary parts; cos 4θ in cos θ alone; sin 4θ factored; a check at π/4.
Clips c2.simp.1 – c2.simp.4."""
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

S4 = load_scene("ch2_s4_expand")
HAND = S4.HAND
mt = S4.mt

TOP_Y = 2.1          # the collected line, c2.simp.1
IM_Y = 0.45          # the Im line (it lands first under the top line, so nothing crosses it)
RE_Y = -0.95         # the Re line
LEFT_X = -5.15       # left edge of the Re / Im lines


def pieces(groups, size, eq=None, at=None):
    """One MathTex per group of (tex, colour) parts, each placed where a single MathTex of all the
    parts would put it (so they read as one line but move on their own). `eq`=(group, part) and
    `at`=(x, y): put that part (the '=') at that point."""
    flat = [p for g in groups for p in g]
    ref = mt(flat, size)
    if eq is not None:
        k = sum(len(g) for g in groups[:eq[0]]) + eq[1]
        ref.shift(np.array([at[0], at[1], 0]) - ref[k].get_center())
    out, k = [], 0
    for g in groups:
        m = mt(g, size)
        m.move_to(VGroup(*ref[k:k + len(g)]))
        out.append(m)
        k += len(g)
    return VGroup(*out)


B_ = BLUE
REAL_G = [(r"\cos^4\theta", B_), ("-", B_), ("6", B_), (r"\cos^2\theta\sin^2\theta", B_), ("+", B_),
          (r"\sin^4\theta", B_)]
TOP_G = [[(r"\cos", BLUE), ("4", GOLD), (r"\theta", BLUE)], [("+", FG)], [(r"i\sin", PINK), ("4", GOLD),
         (r"\theta", PINK)], [("=", FG)], REAL_G, [("+", FG)],
         [("4i", PINK), ("(", PINK), (r"\cos^3\theta\sin\theta", PINK), ("-", PINK),
          (r"\cos\theta\sin^3\theta", PINK), (")", PINK)]]
RE_G = [[(r"\cos", BLUE), ("4", GOLD), (r"\theta", BLUE)], [("=", FG)], REAL_G]
IM_G = [[(r"\sin", PINK), ("4", GOLD), (r"\theta", PINK)], [("=", FG)],
        [("4", PINK), ("(", PINK), (r"\cos^3\theta\sin\theta", PINK), ("-", PINK),
         (r"\cos\theta\sin^3\theta", PINK), (")", PINK)]]
RES_G = [[(r"\cos", BLUE), ("4", GOLD), (r"\theta", BLUE)], [("=", FG)], [(r"8\cos^4\theta", FG)],
         [(r"{}-8\cos^2\theta", FG)], [(r"{}+1", FG)]]


def top_line():
    """cos 4θ + i sin 4θ = (collected RHS), 7 pieces: cos 4θ, +, i sin 4θ, =, real group, +, imaginary group."""
    L = pieces(TOP_G, 42)
    if L.width > 13.0:
        L.scale_to_fit_width(13.0)
    return L.move_to([0, TOP_Y, 0])


def boxed_result():
    """cos 4θ = 8cos⁴θ − 8cos²θ + 1, boxed YELLOW: VGroup(eq, box); eq = VGroup of 5 MathTex
    (cos 4θ, =, 8cos⁴θ, −8cos²θ, +1), the '=' at ORIGIN."""
    eq = pieces(RES_G, 46, eq=(1, 0), at=(0, 0))
    box = SurroundingRectangle(eq, color=YELLOW, buff=0.25, stroke_width=3)
    return VGroup(eq, box)


def unit_dial(center, r=0.6):
    center = np.array(center, dtype=float)
    circ = Circle(radius=r, color=DIM, stroke_width=3).move_to(center)
    axes = VGroup(Line(center + LEFT * (r + 0.2), center + RIGHT * (r + 0.2)),
                  Line(center + DOWN * (r + 0.2), center + UP * (r + 0.2))).set_stroke(DIM, 2, opacity=0.6)
    dot = Dot(center + LEFT * r, radius=0.1, color=GOLD)
    return VGroup(axes, circ), dot


def _boxes_meet(a, b, pad=0.05):
    return not (a.get_right()[0] + pad < b.get_left()[0] or b.get_right()[0] + pad < a.get_left()[0]
                or a.get_top()[1] + pad < b.get_bottom()[1] or b.get_top()[1] + pad < a.get_bottom()[1])


class Merge(Animation):
    """A copy of `src` glides to `dst` (scaling to its height), invisible until clear of src, gone
    before it reaches dst (which fades in there: pair it with during(FadeIn(dst), 0.5, 0.9))."""

    def __init__(self, src, dst, **kw):
        self.src_m, self.start_copy = src, src.copy()
        self.p0, self.p1, self.s1 = src.get_center(), dst.get_center(), dst.height / max(src.height, 1e-6)
        kw.setdefault("run_time", 1.5)
        super().__init__(src.copy(), remover=True, introducer=True, **kw)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        m = self.mobject.become(self.start_copy)
        m.scale(1 + (self.s1 - 1) * a).move_to(self.p0 + (self.p1 - self.p0) * a)
        k = 0.0 if _boxes_meet(m, self.start_copy) else 1.0
        k *= 1 - smooth(float(np.clip((alpha - 0.38) / 0.1, 0, 1)))
        m.set_opacity(k * 0.85)


class Simplify(NarratedScene):
    def construct(self):
        shot = S4.handover_shot()
        self.add(shot)
        self.clip1(shot)
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c2.simp.1
    def clip1(self, shot):
        line1, S, C, br_r, lr, br_i, li = shot
        with self.say("c2.simp.1") as c:
            TOP = top_line()
            parts = [sub for p in TOP for sub in p]                 # the 21 parts, in line order
            self.play(*disappear(S, br_r, lr, br_i, li, *line1[7:]), run_time=0.8)
            moves = [ReplacementTransform(line1[i], parts[i]) for i in range(7)]
            moves += [ReplacementTransform(C[j], parts[7 + j]) for j in range(14)]
            self.play(*moves, run_time=min(1.6, c.until("their real parts")))
            self.remove(*shot.get_family())
            for p in TOP:
                settle(self, p)

            # the two tags: real above the line, imaginary below
            arc_re = ArcBetweenPoints(TOP[0].get_top() + 0.1 * UP, TOP[4].get_top() + 0.1 * UP,
                                      angle=-PI / 3, color=BLUE, stroke_width=3)
            tag_re = T("real = real", 30, BLUE).next_to(arc_re, UP, buff=0.08)
            arc_im = ArcBetweenPoints(TOP[2].get_bottom() + 0.1 * DOWN, TOP[6].get_bottom() + 0.1 * DOWN,
                                      angle=PI / 4, color=PINK, stroke_width=3)
            tag_im = T("imaginary = imaginary", 30, PINK).next_to(arc_im, DOWN, buff=0.08)
            c.wait_until("their real parts")
            self.play(Create(arc_re), *appear(tag_re), run_time=1.0)
            c.wait_until("imaginary parts")
            self.play(Create(arc_im), *appear(tag_im), run_time=1.0)

            # {re}: cos 4θ lifts out of the left side, then the BLUE group slides beside it
            R = pieces(RE_G, 42)
            R.move_to([0, RE_Y, 0]).align_to(LEFT_X * RIGHT, LEFT)
            c.wait_until("re")
            self.play(ReplacementTransform(TOP[0], R[0]), *during(appear(R[1], shift=None), 0.6, 1),
                      run_time=min(1.5, c.until("is the real part")))
            c.wait_until("is the real part")
            self.play(*during(disappear(arc_re, tag_re, arc_im, tag_im), 0, 0.35),
                      *during(ReplacementTransform(TOP[4], R[2]), 0.3, 1), run_time=2.0)
            re_m = Text("Re:", font=HAND, font_size=42, color=BLUE).next_to(R, LEFT, buff=0.6)
            self.play(*appear(re_m), run_time=0.8)

            # {im}: sin 4θ and its bracket come down, the i dropping away
            I = pieces(IM_G, 42)
            I.move_to([0, IM_Y, 0])
            I.shift((R[1].get_x() - I[1].get_x()) * RIGHT)
            c.wait_until("im")
            self.play(*during(disappear(TOP[1], TOP[3], TOP[5]), 0, 0.2), *edit(TOP[2], I[0]), *edit(TOP[6], I[2]),
                      *during(appear(I[1], shift=None), 0.6, 1), run_time=1.8)
            im_m = Text("Im:", font=HAND, font_size=42, color=PINK).next_to(I, LEFT, buff=0.6)
            im_m.align_to(re_m, RIGHT)
            self.play(*appear(im_m), run_time=0.8)

            # {met}
            task = S4.make_task().hand.copy().move_to([-0.6, -2.55, 0])
            chk = check_mark().next_to(task, RIGHT, buff=0.4)
            c.wait_until("met")
            self.play(*appear(task), run_time=1.0)
            self.play(*appear(chk, shift=None), run_time=0.8)
            self.R, self.I = R, I

    # ------------------------------------------------------------ c2.simp.2
    def clip2(self):
        R, I = self.R, self.I
        with self.say("c2.simp.2") as c:
            # {further}: Re line to the top, Im line aside
            R.generate_target()
            R.target.shift((2.75 - R.get_y()) * UP)
            sweep_clear(self, MoveToTarget(R), *during(FadeOut(I, shift=RIGHT), 0, 0.45), keep=[R, I], run_time=1.8)
            X, Y0 = R[1].get_x(), R[1].get_y()

            # {swap}
            tag = MathTex(r"\sin^2\theta=1-\cos^2\theta", font_size=38, color=YELLOW)
            tag_box = SurroundingRectangle(tag, color=YELLOW, buff=0.18, stroke_width=2, corner_radius=0.1)
            VGroup(tag, tag_box).to_edge(RIGHT, buff=0.5).set_y(R.get_y())
            c.wait_until("swap")
            self.play(*appear(tag, shift=None), FadeIn(tag_box), FlashAround(VGroup(*R[2][3][5:])), run_time=1.2)

            # {sixline}
            A = [("=", FG), (r"\cos^4\theta", FG), ("-", FG), (r"6\cos^2\theta", FG),
                 (r"(1-\cos^2\theta)", YELLOW)]
            PL = [("+", FG)]
            y1 = Y0 - 1.15
            L1 = pieces([A, PL, [(r"\sin^4\theta", FG)]], 42, eq=(0, 0), at=(X, y1))
            c.wait_until("sixline")
            self.play(*appear(L1, shift=0.4 * DOWN), run_time=1.5)

            # {square}: sin⁴θ → (sin²θ)² → (1 − cos²θ)²
            sq1 = pieces([A, PL, [(r"(\sin^2\theta)^2", FG)]], 42, eq=(0, 0), at=(X, y1))[2]
            sq2 = pieces([A, PL, [(r"(1-\cos^2\theta)^2", YELLOW)]], 42, eq=(0, 0), at=(X, y1))[2]
            c.wait_until("square")
            self.play(*edit(L1[2], sq1), run_time=1.2)
            self.wait(0.6)
            self.play(*edit(sq1, sq2), run_time=1.3)

            # {expand}
            y2 = y1 - 1.15
            L2 = mt([("=", FG), (r"\cos^4\theta", FG), (r"-6\cos^2\theta", FG), (r"+6\cos^4\theta", FG),
                     ("+1", FG), (r"-2\cos^2\theta", FG), (r"+\cos^4\theta", FG)], 42)
            L2.shift(np.array([X, y2, 0]) - L2[0].get_center())
            c.wait_until("expand")
            self.play(*appear(L2, shift=0.4 * DOWN), run_time=1.5)

            # {gather}: fourth powers → 8cos⁴θ
            res = boxed_result()
            res.shift(np.array([X, y2 - 1.2, 0]) - res[0][1].get_center())
            eq = res[0]
            fours = [L2[1], L2[3], L2[6]]
            c.wait_until("gather")
            self.play(*recolor(fours, GOLD), *flash(fours, color=GOLD), run_time=1.2)
            c.wait_until("eight in all")
            self.play(*[Merge(f, eq[2]) for f in fours],
                      *during(appear(eq[1], eq[2], shift=None, lag=0), 0.5, 0.9), run_time=1.6)
            # the squares → −8cos²θ
            twos = [L2[2], L2[5]]
            c.wait_until("the squares come")
            self.play(*recolor(fours, FG), *recolor(twos, GOLD), *flash(twos, color=GOLD), run_time=1.2)
            c.wait_until("minus eight in all")
            self.play(*[Merge(f, eq[3]) for f in twos], *during(appear(eq[3], shift=None), 0.5, 0.9), run_time=1.6)
            # {one}
            c.wait_until("one")
            self.play(*recolor(twos, FG), *recolor([L2[4]], GOLD), *flash([L2[4]], color=GOLD), run_time=1.0)
            self.play(Merge(L2[4], eq[4]), *during(appear(eq[4], shift=None), 0.5, 0.9), run_time=1.4)
            # {result}
            c.wait_until("result")
            self.play(*appear(eq[0], shift=None), GrowFromCenter(res[1]), run_time=1.2)
            self.res = res

    # ------------------------------------------------------------ c2.simp.3
    def clip3(self):
        res, I = self.res, self.I
        with self.say("c2.simp.3") as c:
            I = pieces(IM_G, 44)
            F = pieces([IM_G[0], IM_G[1], [(r"4\cos\theta\sin\theta", YELLOW), ("(", FG),
                                           (r"\cos^2\theta-\sin^2\theta", FG), (")", FG)]], 44)
            F.move_to([0.3, 1.25, 0])
            I.shift(F[1].get_center() - I[1].get_center())
            sweep_clear(self, *during(res.animate.move_to([0, 2.75, 0]), 0.45, 0.75),
                        *during(FadeIn(I, shift=LEFT), 0.75, 1), keep=[res], run_time=2.2)

            X = F[1].get_x()
            c.wait_until("common factor")
            self.play(*edit(I[2], F[2]), run_time=1.6)

            # {bracket}
            br = VGroup(*F[2][1:4])
            bbox = SurroundingRectangle(br, color=YELLOW, buff=0.06, stroke_width=3)
            bbox.stretch_to_fit_height(br.height + 0.24)
            c.wait_until("bracket")
            self.play(FadeIn(bbox), *recolor([F[2][2]], YELLOW), run_time=1.0)

            # {forms}: the margin note, then the first ending
            note = Text("cos²θ + sin²θ = 1", font=HAND, font_size=42, color=YELLOW)
            note.move_to([0, -2.75, 0])
            G1 = pieces([[("=", FG)], [(r"4\cos\theta\sin\theta", YELLOW)], [(r"(2\cos^2\theta-1)", FG)]], 44,
                        eq=(0, 0), at=(X, F[1].get_y() - 1.25))
            G2 = pieces([[("=", FG)], [(r"4\cos\theta\sin\theta", YELLOW)], [(r"(1-2\sin^2\theta)", FG)]], 44,
                        eq=(0, 0), at=(X, F[1].get_y() - 2.5))
            c.wait_until("forms")
            self.play(*appear(note), run_time=1.0)
            c.wait_until("two cosine squared")
            self.play(*appear(*G1, shift=None, lag=0.15), run_time=1.2)
            c.wait_until("or")
            self.play(*appear(*G2, shift=None, lag=0.15), run_time=1.2)

            # {hand}: the endings in her handwriting
            H1 = Text("(2cos²θ - 1)", font=HAND, font_size=44, color=YELLOW)
            H2 = Text("(1 - 2sin²θ)", font=HAND, font_size=44, color=YELLOW)
            H1.next_to(G1[1], RIGHT, buff=0.15)
            H2.next_to(G2[1], RIGHT, buff=0.15)
            c.wait_until("hand")
            self.play(*swap(G1[2], H1), *swap(G2[2], H2), run_time=1.4)

    # ------------------------------------------------------------ c2.simp.4
    def clip4(self):
        res = self.res
        with self.say("c2.simp.4") as c:
            sweep_clear(self, res.animate.move_to([-1.0, 2.6, 0]), keep=[res], run_time=1.6)
            eq = res[0]

            # {quarter}
            q = MathTex(r"\theta=\frac{\pi}{4}", font_size=46, color=YELLOW)
            q.next_to(res, RIGHT, buff=0.7)
            c.wait_until("quarter")
            self.play(*appear(q), run_time=1.0)

            # {left}: 4θ = π, the dial, cos π = −1 (on the total's row)
            lx = eq[0].get_x() - 0.2
            ROW = -2.45
            a1 = MathTex(r"4\theta=\pi", font_size=44).move_to([lx, 1.15, 0])
            dial, dot = unit_dial([lx, -0.55, 0], r=0.65)
            a2 = pieces([[(r"\cos\pi", BLUE)], [("=", FG)], [("-1", GOLD)]], 44, eq=(1, 0), at=(lx, ROW))
            c.wait_until("left")
            self.play(*appear(a1), run_time=1.0)
            c.wait_until("cosine of pi")
            self.play(FadeIn(dial), GrowFromCenter(dot), run_time=1.0)
            self.play(*appear(a2, shift=None), run_time=1.0)

            # {right}
            rx = 1.2
            b1 = MathTex(r"\cos^2(\pi/4)=\tfrac{1}{2}", font_size=44, color=GOLD).move_to([rx, 1.15, 0])
            b2 = MathTex(r"\cos^4(\pi/4)=\tfrac{1}{4}", font_size=44, color=GOLD).move_to([rx, 0.0, 0])
            c.wait_until("right")
            self.play(*appear(b1), run_time=1.0)
            c.wait_until("so cosine to the fourth")
            self.play(*appear(b2), run_time=1.0)

            # {sum}
            SG = [[(r"8\cdot\tfrac{1}{4}", GOLD), ("-", GOLD), (r"8\cdot\tfrac{1}{2}", GOLD), ("+", GOLD), ("1", GOLD)],
                  [("=", FG)], [("2-4+1", GOLD)]]
            s = pieces(SG, 44)
            s.move_to([0, -1.2, 0]).align_to(b2, LEFT).shift(0.3 * LEFT)
            ref = mt(SG[0], 44).move_to(s[0])
            c.wait_until("sum")
            self.play(*appear(s[0], shift=None), FlashAround(ref[0], color=GOLD), run_time=1.2)
            c.wait_until("eight halves")
            self.play(FlashAround(ref[2], color=GOLD), run_time=1.0)
            c.wait_until("so you get")
            self.play(*appear(s[1], s[2], shift=None, lag=0.2), run_time=1.2)

            # {total}: = −1 on the row of cos π = −1, joined by a GREEN line
            tot = pieces([[("=", FG)], [("-1", GOLD)]], 46, eq=(0, 0), at=(s[1].get_x(), ROW))
            chk = check_mark().next_to(tot, RIGHT, buff=0.4)
            join = Line(a2.get_right() + 0.25 * RIGHT, tot.get_left() + 0.25 * LEFT, color=GREEN, stroke_width=3)
            c.wait_until("total")
            self.play(*appear(tot, shift=None), run_time=1.0)
            self.play(GrowFromCenter(join), *appear(chk, shift=None), *recolor([a2[2], tot[1]], GREEN),
                      run_time=1.4)
