"""Chapter 3, scene 2: cos^3 theta via exponentials, mirror pairs, and its integral. Clips c3.cube.1 – c3.cube.5."""
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

THM = load_scene("ch2_s2_theorem")      # argand_plane()
EXPO = load_scene("ch2_s6_expo")        # arrow_between()
EXPAND = load_scene("ch2_s4_expand")    # pascal_rows()
HOOK = load_scene("ch3_s1_hook")        # toolbox()

FS = 42                                  # algebra font size
EQX = -4.9                               # x of the aligned "=" (clips 1-4)
EQX5 = -1.9                              # ... in clip 5 (column re-centred)
Y0, Y1, Y2, Y4 = 1.35, 0.0, -1.4, -2.8   # rows: cube, expansion, regrouped / cosines, boxed
Y5, YCHK = -1.35, -2.8                   # clip 5: integral, check
PASCAL_TOP = np.array([4.6, 2.75, 0])

# the Argand plane on the right (clip 3 on)
PC = np.array([4.3, -0.4, 0])
PU = 1.1
PEXT = 2.35
TH0 = 35 * DEGREES


def plane(center=PC, unit=PU, extent=PEXT):
    """ch2 s2's argand_plane, with Re lifted above the axis end (the 2cos θ label sits below)."""
    g = THM.argand_plane(center=center, unit=unit, extent=extent)
    re = g[4]
    re.next_to(g.axes[0].get_end(), UP, buff=0.12).shift(0.25 * LEFT)
    return g


# ---------------------------------------------------------------- helpers

def mt(parts, size=FS):
    """MathTex from (tex, colour) pairs; one submobject per pair."""
    m = MathTex(*[p for p, _ in parts], font_size=size)
    for sub, (_, col) in zip(m, parts):
        sub.set_color(col)
    return m


def place(m, eq_idx, y, eqx=EQX):
    """Shift m so its '=' (part eq_idx) sits at (eqx, y)."""
    e = m[eq_idx]
    m.shift([eqx - e.get_x(), y - e.get_y(), 0])
    return m


def P(z, center=PC, unit=PU):
    return np.array([center[0] + unit * z.real, center[1] + unit * z.imag, 0.0])


def pair(th, k, center=PC, unit=PU):
    """The mirror pair e^{ikθ} (GOLD, from 0) + e^{-ikθ} (PURPLE, tip to tail), and the BLUE dot 2cos kθ."""
    e = np.exp(1j * k * th)
    gold = EXPO.arrow_between(P(0, center, unit), P(e, center, unit), GOLD)
    purple = EXPO.arrow_between(P(e, center, unit), P(2 * e.real, center, unit), PURPLE)
    dot = Dot(P(2 * e.real, center, unit), radius=0.09, color=BLUE)
    return VGroup(gold, purple, dot)


def pair_label(k, dot, size=32):
    tex = r"2\cos 3\theta" if k == 3 else r"2\cos\theta"
    return MathTex(tex, font_size=size, color=BLUE).next_to(dot, DOWN, buff=0.22)


def mirror_pairs(theta=TH0, center=PC, unit=PU, extent=PEXT, with_plane=True, labels=True):
    """Shared picture (recap, s7's F12 hint): the ±3θ pair and the ±θ pair, each tip to tail,
    landing on the real axis at 2cos 3θ and 2cos θ (BLUE dots). VGroup(plane?, pair3, pair1, labels?);
    attributes .plane .pair3 .pair1 .labels (each pair: VGroup(gold, purple, dot))."""
    g = VGroup()
    pl = plane(center, unit, extent) if with_plane else None
    if pl is not None:
        g.add(pl)
    p3, p1 = pair(theta, 3, center, unit), pair(theta, 1, center, unit)
    g.add(p3, p1)
    labs = VGroup(pair_label(3, p3[2]), pair_label(1, p1[2])) if labels else None
    if labs is not None:
        g.add(labs)
    g.plane, g.pair3, g.pair1, g.labels = pl, p3, p1, labs
    return g


def cube_line():
    """cos³θ = [½(e^{iθ} + e^{−iθ})]³ ; parts 5-10 match (77)'s right-hand side."""
    L = mt([(r"\cos", BLUE), ("^3", RED), (r"\theta", BLUE), ("=", FG), (r"\Big[", FG),
            (r"\frac{1}{2}", FG), (r"\Big(", FG), (r"e^{i\theta}", GOLD), ("+", FG), (r"e^{-i\theta}", PURPLE),
            (r"\Big)", FG), (r"\Big]^3", FG)])
    return place(L, 3, Y0)


def expansion_line():
    L = mt([("=", FG), (r"\tfrac{1}{8}", FG), (r"\Big[", FG), (r"e^{3i\theta}", GOLD), ("+", FG),
            ("3", FG), (r"e^{2i\theta}", GOLD), (r"e^{-i\theta}", PURPLE), ("+", FG),
            ("3", FG), (r"e^{i\theta}", GOLD), (r"e^{-2i\theta}", PURPLE), ("+", FG),
            (r"e^{-3i\theta}", PURPLE), (r"\Big]", FG)])
    return place(L, 0, Y1)


def collapsed_line():
    L = mt([("=", FG), (r"\tfrac{1}{8}", FG), (r"\Big[", FG), (r"e^{3i\theta}", GOLD), ("+", FG),
            ("3", FG), (r"e^{i\theta}", GOLD), ("+", FG), ("3", FG), (r"e^{-i\theta}", PURPLE), ("+", FG),
            (r"e^{-3i\theta}", PURPLE), (r"\Big]", FG)])
    return place(L, 0, Y1)


def grouped_line():
    L = mt([("=", FG), (r"\tfrac{1}{8}", FG), (r"\Big[", FG), (r"e^{3i\theta}", GOLD), ("+", FG),
            (r"e^{-3i\theta}", PURPLE), (r"\Big]", FG), ("+", FG), (r"\tfrac{3}{8}", FG), (r"\Big[", FG),
            (r"e^{i\theta}", GOLD), ("+", FG), (r"e^{-i\theta}", PURPLE), (r"\Big]", FG)])
    return place(L, 0, Y2)


def cosine_line():
    L = mt([("=", FG), (r"\tfrac{1}{8}", FG), (r"\big(", FG), (r"2\cos 3\theta", BLUE), (r"\big)", FG),
            ("+", FG), (r"\tfrac{3}{8}", FG), (r"\big(", FG), (r"2\cos\theta", BLUE), (r"\big)", FG)])
    return place(L, 0, Y2)


def boxed_line():
    L = mt([("=", FG), (r"\tfrac{1}{4}", FG), (r"\cos 3\theta", BLUE), ("+", FG), (r"\tfrac{3}{4}", FG),
            (r"\cos\theta", BLUE)])
    return place(L, 0, Y4)


def integral_line():
    L = mt([(r"\int", FG), (r"\cos^3\theta", BLUE), (r"\,d\theta", FG), ("=", FG), (r"\tfrac{1}{12}", FG),
            (r"\sin 3\theta", BLUE), ("+", FG), (r"\tfrac{3}{4}", FG), (r"\sin\theta", BLUE), ("+", FG),
            ("C", FG)])
    return place(L, 3, Y5, EQX5)


def cube_ring(sup):
    """RED ring round the superscript ³, nudged up-right so it clears the "s" of cos."""
    h = sup.height                                   # same rule as ch3_s1_hook's ring
    return Circle(radius=0.68 * h, color=RED, stroke_width=3).move_to(
        sup.get_center() + 0.12 * h * RIGHT + 0.08 * h * UP)


# ---------------------------------------------------------------- scene

class CosineCubed(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(3.2)                                   # hold the check before clearing
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c3.cube.1: cos³θ = [½(e^{iθ}+e^{−iθ})]³, Pascal's row, ½ → ⅛
    def clip1(self):
        with self.say("c3.cube.1") as c:
            self.tb = HOOK.toolbox()
            L0 = self.L0 = cube_line()
            ring = self.ring = cube_ring(L0[1])
            head = VGroup(*L0[0:3])
            self.play(FadeIn(self.tb), *appear(head), GrowFromCenter(ring),  # early: the toolbox is a standing reference
                      run_time=min(1.2, c.until("swap")))
            c.wait_until("swap")

            # {swap}: the bracket is pulled out of the toolbox's (77)
            cf = self.tb[0][0]
            src = VGroup(*cf[2:8])
            dst = VGroup(*L0[5:11])
            rest = [self.tb[1], self.tb[0][1], cf[0], cf[1]]   # all but (77)'s right side dims while it's copied
            self.play(*set_alpha(rest, DIMMED), FlashAround(src, run_time=1.0), run_time=1.0)
            # the source dims as its copy leaves (the copy never sits bright on it)
            self.play(*during(set_alpha(list(src), DIMMED), 0, 0.15), *appear(L0[3], shift=None),
                      *fly(src, dst), run_time=min(1.8, c.until("cube it")))
            c.wait_until("cube it")
            self.play(*appear(L0[4], L0[11], shift=None, lag=0), FlashAround(L0[11], run_time=1.2),
                      *set_alpha(rest + list(src), 1), run_time=min(1.2, c.until("pascal")))
            settle(self, L0)
            c.wait_until("pascal")

            # {pascal}: rows 0-3, row 3 GOLD
            rows = EXPAND.pascal_rows(top=PASCAL_TOP, size=40, dx=0.8, dy=0.65)
            tri = self.tri = VGroup(*rows[:4])
            tri[3].set_color(GOLD)
            self.play(*appear(*tri, lag=0.25), run_time=min(1.4, c.until("one, three, three, one")))
            c.wait_until("one, three, three, one")
            self.play(FlashAround(tri[3], run_time=1.5, time_width=1.5, color=GOLD))
            c.wait_until("eighth")

            # {eighth}: ½ cubed is ⅛, the head of the expansion
            L1 = self.L1 = expansion_line()
            self.play(*flash([L0[5], L0[11]], color=YELLOW, run_time=1.2), run_time=1.2)
            self.play(*appear(L1[0], L1[1], L1[2], lag=0.15), run_time=min(1.2, c.until(floor=0.5)))

    # c3.cube.2: four terms, one per mark; the middle products collapse
    def clip2(self):
        L1, tri = self.L1, self.tri
        with self.say("c3.cube.2") as c:
            c.wait_until("t1")
            groups = [(L1[3:4], 0, "t2"), (L1[4:8], 1, "t3"), (L1[8:12], 2, "t4"), (L1[12:15], 3, "collapse")]
            for k, (parts, j, nxt) in enumerate(groups):
                self.play(*appear(*parts, lag=0.15), FlashAround(tri[3][j], color=GOLD, run_time=1.2),
                          run_time=min(1.2, c.until(nxt)))
                if k < 3:
                    c.wait_until(nxt)
            settle(self, L1, add=[])
            c.wait_until("collapse")

            # {collapse}: multiplying adds the angles
            n2 = MathTex(r"2\theta-\theta=\theta", font_size=32, color=YELLOW)
            n3 = MathTex(r"\theta-2\theta=-\theta", font_size=32, color=YELLOW)
            n2.next_to(VGroup(*L1[6:8]), DOWN, buff=0.35)
            n3.next_to(VGroup(*L1[10:12]), DOWN, buff=0.35)
            self.play(*appear(n2, n3, lag=0.4), run_time=min(1.4, c.until("mid")))
            self.play(*flash([n2, n3], color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until("mid")

            # {mid}: they shrink in place
            L1c = self.L1c = collapsed_line()
            self.notes = VGroup(n2, n3)
            self.play(*edit(L1, L1c), run_time=min(1.8, c.until()))

    # c3.cube.3: mirror pairs; the picture
    def clip3(self):
        L1c = self.L1c
        L2 = self.L2 = grouped_line()
        with self.say("c3.cube.3") as c:
            self.play(*disappear(self.tri, self.notes), run_time=min(1.0, c.until("p3")))
            c.wait_until("p3")

            # {p3}: e^{3iθ} with e^{-3iθ}
            a, d = L1c[3], L1c[11]
            arc3 = ArcBetweenPoints(a.get_top() + 0.22 * UP, d.get_top() + 0.22 * UP, angle=-PI / 5,
                                    color=YELLOW, stroke_width=3)
            self.play(FadeIn(arc3), run_time=min(1.0, c.until("p1")))
            self.play(*flash([a, d], color=YELLOW, run_time=1.4),
                      *appear(*L2[0:7], lag=0.08), run_time=min(1.6, c.until("p1")))
            c.wait_until("p1")

            # {p1}: e^{iθ} with e^{-iθ}
            b, e = VGroup(L1c[5], L1c[6]), VGroup(L1c[8], L1c[9])
            arc1 = ArcBetweenPoints(b.get_bottom() + 0.12 * DOWN, e.get_bottom() + 0.12 * DOWN, angle=PI / 3,
                                    color=YELLOW, stroke_width=3)
            self.arcs = VGroup(arc3, arc1)
            self.play(FadeIn(arc1), run_time=min(1.0, c.until("picture")))
            self.play(*flash([b, e], color=YELLOW, run_time=1.4),
                      *appear(*L2[7:14], lag=0.08), run_time=min(1.6, c.until("picture")))
            settle(self, L2)
            c.wait_until("picture")

            # {picture}: the plane on the right
            self.plane = plane()
            self.play(FadeIn(self.plane), run_time=min(1.2, c.until("arrows")))
            c.wait_until("arrows")

            # {arrows}: ±3θ tip to tail, then ±θ
            p3, p1 = pair(TH0, 3), pair(TH0, 1)
            for p, rt in ((p3, 1.8), (p1, 1.4)):
                self.play(LaggedStart(GrowArrow(p[0]), GrowArrow(p[1]), FadeIn(p[2], scale=0.5), lag_ratio=0.8),
                          run_time=rt)
                self.wait(0.3)

            # θ drifts: the arrows turn opposite ways, the tips stay on the real axis
            th = ValueTracker(TH0)
            live = always_redraw(lambda: VGroup(pair(th.get_value(), 3), pair(th.get_value(), 1)))
            self.remove(p3, p1)
            self.add(live)
            self.play(th.animate.set_value(TH0 + 9 * DEGREES), run_time=max(0.8, 0.5 * (c.until("twice") - 0.2)))
            self.play(th.animate.set_value(TH0), run_time=max(0.8, c.until("twice") - 0.1))
            live.clear_updaters()
            self.remove(live)
            self.p3, self.p1 = pair(TH0, 3), pair(TH0, 1)
            self.add(self.p3, self.p1)
            c.wait_until("twice")

            # {twice}: each pair is twice a cosine
            self.labs = VGroup(pair_label(3, self.p3[2]), pair_label(1, self.p1[2]))
            self.play(*appear(*self.labs, lag=0.3), run_time=min(1.2, c.until()))
            self.play(*flash([VGroup(*L2[2:7]), VGroup(*L2[9:14])], color=BLUE, run_time=1.2),
                      run_time=min(1.2, c.until()))

    # c3.cube.4: brackets become cosines; the boxed result; the power has gone
    def clip4(self):
        L2 = self.L2
        L3 = self.L3 = cosine_line()
        with self.say("c3.cube.4") as c:
            # {result}: the brackets go, the coefficients make room
            self.remove(L2)
            self.add(*L2)
            moves = [ReplacementTransform(L2[i], L3[j]) for i, j in ((0, 0), (1, 1), (7, 5), (8, 6))]
            self.play(*during(disappear(*L2[2:7], *L2[9:14]), 0, 0.45),
                      *during(moves, 0.2, 0.8),
                      *during(appear(L3[2], L3[4], L3[7], L3[9], shift=None, lag=0), 0.6, 1),
                      run_time=1.2)
            self.remove(*L2.get_family())
            c.wait_until("twice cosine three theta")
            self.play(FlashAround(self.labs[0], color=BLUE, run_time=1.2), *appear(L3[3]), run_time=1.2)
            c.wait_until("twice cosine theta")
            self.play(FlashAround(self.labs[1], color=BLUE, run_time=1.2), *appear(L3[8]),
                      run_time=min(1.2, c.until("box")))
            settle(self, L3)
            c.wait_until("box")

            # {box}: = ¼cos 3θ + ¾cos θ
            L4 = self.L4 = boxed_line()
            self.play(*appear(L4, shift=0.4 * DOWN), run_time=1.2)
            self.box = SurroundingRectangle(L4, color=YELLOW, buff=0.2, stroke_width=3)
            self.play(GrowFromCenter(self.box), run_time=0.8)
            c.wait_until("gone")

            # {gone}: the RED-circled power fades away
            self.play(FadeOut(self.ring, scale=0.6), self.L0[1].animate.set_color(BLUE), run_time=1.2)
            self.play(FlashAround(self.box, color=YELLOW, run_time=1.5, time_width=1.5))

    # c3.cube.5: integrate; check at θ = 0
    def clip5(self):
        L0, L4, box = self.L0, self.L4, self.box
        with self.say("c3.cube.5") as c:
            # {integrate}: clear the working, keep the question and the answer
            sweep_clear(self, keep=[self.tb, L0, L4, box], run_time=1.0)
            dx = EQX5 - EQX
            v_top = np.array([dx, 0, 0])
            v_box = np.array([dx, (Y0 - 1.3) - Y4, 0])
            self.play(L0.animate.shift(v_top), L4.animate.shift(v_box), box.animate.shift(v_box),
                      run_time=min(1.2, c.until("answer")))
            c.wait_until("answer")

            # {answer}: each term drops out of its cosine term
            L5 = integral_line()
            self.play(*appear(*L5[0:4], lag=0.1), run_time=min(1.0, c.until("one twelfth")))
            c.wait_until("one twelfth")
            self.play(FlashAround(VGroup(L4[1], L4[2]), color=BLUE, run_time=1.4),
                      *appear(L5[4], L5[5], shift=0.2 * DOWN, lag=0), run_time=1.4)
            c.wait_until("three quarters of sine")
            self.play(FlashAround(VGroup(L4[4], L4[5]), color=BLUE, run_time=1.4),
                      *appear(L5[6], L5[7], L5[8], shift=0.2 * DOWN, lag=0), run_time=1.4)
            c.wait_until("constant")
            self.play(*appear(L5[9], L5[10], lag=0.2), run_time=min(1.0, c.until("check")))
            settle(self, L5)
            c.wait_until("check")

            # {check}: θ = 0
            k0 = MathTex(r"\theta=0:", font_size=FS, color=YELLOW)
            k1 = mt([(r"\cos^3 0", BLUE), ("=", FG), ("1", FG)])
            k2 = mt([(r"\tfrac{1}{4}", FG), ("+", FG), (r"\tfrac{3}{4}", FG), ("=", FG), ("1", FG)])
            tick = check_mark()
            row = VGroup(k0, k1, k2, tick).arrange(RIGHT, buff=0.7)
            row.move_to([L5.get_center()[0], YCHK, 0])
            self.play(*appear(k0), run_time=min(1.0, c.until("lhs")))
            c.wait_until("lhs")
            self.play(*appear(k1), run_time=min(1.0, c.until("rhs")))
            c.wait_until("rhs")
            self.play(*appear(k2), run_time=1.0)
            self.play(GrowFromCenter(tick), run_time=min(0.8, c.until(floor=0.3)))
