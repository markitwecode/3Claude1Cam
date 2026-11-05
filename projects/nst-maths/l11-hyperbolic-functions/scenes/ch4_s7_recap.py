"""Chapter 4, scene 7: recap in five panels, the cos z = -2 exercise, and the Part 5 preview.
Clips c4.recap.1 – c4.recap.3.

Panels (3 over 2, DIM rounded frames as in ch2's recap, "Recap" heading as in ch1's), each built
on its mark from the scene that taught it, with its short line inside the frame's foot:
r1 s1's wave under the YELLOW line at 2; r2 s2's peeling chain with its degree labels and GREEN
brace; r3 s3's result line with its real / imaginary (PINK) braces; r4 s4's case tree (RED ∅,
GREEN x = 2πm); r5 s6's lattice (GREEN crosses, BLUE 2π brace, TEAL height brace).
{try}: the other panels clear while the lattice grows; YELLOW cos z = -2 above it; "which n?"
swaps to "n odd" on {odd}; {slide}: every pair slides right by π (YELLOW odd tick labels).
{next}: "Next time", thin circle and ellipse (BLUE) and hyperbola (TEAL), "Part 5 · Circles and
ellipses". End card held ~8 s, then fade.
"""
# style: 2
import math
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

S1 = load_scene("ch4_s1_hook")
S2 = load_scene("ch4_s2_fta")
S3 = load_scene("ch4_s3_split")
S4 = load_scene("ch4_s4_cases")
S6 = load_scene("ch4_s6_lattice")

# panel geometry: top row three, bottom row two
TOP_Y, TOP_H = 1.55, 2.9
BOT_Y, BOT_H = -1.825, 3.25
PANELS = [(-5.05, TOP_Y, 3.4, TOP_H), (-0.675, TOP_Y, 4.95, TOP_H), (4.375, TOP_Y, 4.75, TOP_H),
          (-3.375, BOT_Y, 6.45, BOT_H), (3.375, BOT_Y, 6.45, BOT_H)]
LINE_SZ = 28
LAT_K = 1.0                     # the lattice's scale once it is the hero (clip 2)


def frame_at(k):
    x, y, w, h = PANELS[k]
    return RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(DIM, 2).move_to([x, y, 0])


def panel_line(k, *texts, **kw):
    """The panel's short line(s), in the frame's foot."""
    x, y, w, h = PANELS[k]
    g = VGroup(*[T(t, LINE_SZ, **kw) for t in texts]).arrange(DOWN, buff=0.1)
    g.move_to([x, 0, 0]).align_to([0, y - h / 2 + 0.2, 0], DOWN)
    return g


def fit(g, k, line, pad=0.25, gap=0.2):
    """Scale g to fill the panel above its line and centre it there."""
    x, y, w, h = PANELS[k]
    top = y + h / 2 - pad
    bot = line.get_top()[1] + gap
    s = min((w - 2 * pad) / g.width, (top - bot) / g.height)
    g.scale(s).move_to([x, (top + bot) / 2, 0])
    return g


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)           # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ------------------------------------------------------------ c4.recap.1: five panels
    def clip1(self):
        head = T("Recap", 44, DIM).move_to([0, 3.4, 0])
        with self.say("c4.recap.1") as c:
            self.play(*appear(head, shift=None), run_time=1.0)  # early: section heading

            # ---- r1: the wave under the line at 2
            c.wait_until("r1")
            f1 = frame_at(0)
            l1 = panel_line(0, "no real solution")
            ws = S1.wave_shot()
            band = VGroup(ws.band.fill, ws.band.dash_up, ws.band.dash_lo)
            p1 = fit(VGroup(ws.ax, band, ws.wave, ws.line), 0, l1)
            self.play(FadeIn(f1), FadeIn(ws.ax), FadeIn(band), Create(ws.wave),
                      run_time=min(1.5, c.until("reaches")))
            c.wait_until("reaches")
            self.play(Create(ws.line), *during(appear(l1), 0.3, 1), run_time=min(1.2, c.until("r2")))

            # ---- r2: the peeling chain
            c.wait_until("r2")
            f2 = frame_at(1)
            l2 = panel_line(1, "degree n: exactly n roots", t2s={" n": ITALIC})
            ch = S2.peel_chain()
            ch.arrange(DOWN, buff=0.3, aligned_edge=LEFT)       # tighter rows for the panel
            ch.dots.set_x(ch.lines[0][1].get_x())
            fit(ch, 1, l2)
            l1a, l2a, l3a = ch.lines
            self.play(FadeIn(f2), *appear(l1a, l2a, ch.dots, l3a, shift=None, lag=0.3),
                      run_time=min(1.8, c.until("exactly")))
            c.wait_until("exactly")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("peeled")
            self.play(*[FlashAround(l3a[i], color=GREEN, time_width=1.5) for i in (2, 3, 5)],
                      run_time=min(1.5, c.until("r3")))

            # ---- r3: the split line and its braces
            c.wait_until("r3")
            f3 = frame_at(2)
            l3 = panel_line(2, "split into real and", "imaginary parts")
            res = S3.result_line()
            x, y, w, h = PANELS[2]
            s = (w - 0.5) / res.width
            res.scale(s).move_to([x, l3.get_top()[1] + 1.45, 0])
            g = S3.grp
            b1 = Brace(g(res, *S3.R_COSX).add(*S3.glyphs(res, *S3.R_COSHY)), DOWN, buff=0.12, color=FG)
            t1 = T("real", LINE_SZ).next_to(b1, DOWN, buff=0.08)
            b2 = Brace(g(res, S3.R_MINUS[0], S3.R_SINHY[1]), DOWN, buff=0.12, color=PINK)
            t2 = T("imaginary", LINE_SZ, PINK).next_to(b2, DOWN, buff=0.08)
            self.play(FadeIn(f3), *appear(res, shift=None), run_time=min(1.2, c.until("real", nth=1)))
            c.wait_until(own_word=t1)
            self.play(GrowFromCenter(b1), *appear(t1), run_time=1.0)
            c.wait_until(own_word=t2)
            self.play(GrowFromCenter(b2), *appear(t2), run_time=1.0)
            self.play(*appear(*l3, lag=0.3), run_time=min(1.0, c.until("r4")))

            # ---- r4: the case tree
            c.wait_until("r4")
            f4 = frame_at(3)
            l4 = panel_line(3, "only x = 2πm survives", t2s={"x": ITALIC, "m": ITALIC})
            tree = S4.case_tree(right=r"x = 2\pi m", steps=False, center=ORIGIN)
            fit(tree, 3, l4, gap=0.4)
            either = T("either", LINE_SZ, DIM).move_to(tree.either).align_to(tree.either, RIGHT)
            orr = T("or", LINE_SZ, DIM).move_to(tree.orr).align_to(tree.orr, LEFT)
            self.play(FadeIn(f4), *appear(tree.root, shift=None),
                      Create(tree.edges[0]), Create(tree.edges[1]),
                      *appear(tree.lb, tree.rb, shift=None, lag=0.2),
                      *appear(either, orr, shift=None),
                      run_time=min(1.6, c.until("empty")))  # early: the case tree's branch words
            c.wait_until("empty")
            self.play(*appear(tree.empty), run_time=1.0)
            c.wait_until("even multiples")
            self.play(*appear(tree.rres), *during(appear(l4), 0.3, 1), run_time=1.2)

            # ---- r5: the lattice
            c.wait_until("r5")
            f5 = frame_at(4)
            l5 = panel_line(4, "infinitely many, 2π apart")
            lat = S6.lattice(center=ORIGIN, xs=0.3, ys=0.7, half_w=4.3, half_h=1.65, ms=range(-1, 2), size=42)
            lat.b2_lab.scale(1.25, about_edge=DOWN)            # 2π as big as the other labels
            lat.remove(lat.bh_lab)                             # the brace alone carries the height
            fit(lat, 4, l5)
            self.play(FadeIn(f5), FadeIn(lat.base), *[FadeIn(p) for p in lat.pairs],
                      GrowFromCenter(lat.bh),
                      run_time=min(1.5, c.until("two pi apart")))
            c.wait_until("two pi apart")
            self.play(GrowFromCenter(lat.b2), *appear(lat.b2_lab), *during(appear(l5), 0.3, 1), run_time=1.2)
            c.wait_until("infinitely")
            self.play(*appear(*lat.faded, *lat.dots, shift=None, lag=0.1), run_time=1.2)

        self.head = head
        self.lat = lat
        self.rest = [head, f1, ws.ax, band, ws.wave, ws.line, l1,
                     f2, ch, l2,
                     f3, res, b1, t1, b2, t2, l3,
                     f4, tree.root, *tree.edges, tree.lb, tree.rb, tree.empty, tree.rres, either, orr, l4, f5, l5]

    # ------------------------------------------------------------ c4.recap.2: try cos z = -2
    def clip2(self):
        lat = self.lat
        tgt = lat.copy().scale(LAT_K / (lat.base[1].get_length() / 8.6))
        tgt.move_to([0, -0.45, 0])
        title = MathTex(r"\cos z = -2", font_size=56, color=YELLOW).move_to([0, 3.05, 0])
        ask = T("which n?", 36, DIM, t2s={"n": ITALIC})
        odd = T("n odd", 36, GREEN, t2s={"n": ITALIC})
        for m in (ask, odd):
            m.next_to(title, RIGHT, buff=1.0).align_to(title, DOWN)
        with self.say("c4.recap.2", gap=2.0) as c:
            c.wait_until("find every")
            self.play(*during(disappear(*self.rest), 0, 0.45),
                      *during([lat.animate.scale(LAT_K / (lat.base[1].get_length() / 8.6))
                               .move_to(tgt.get_center())], 0.4, 1),
                      run_time=min(2.0, c.until("cosine is minus two")))
            c.wait_until("cosine is minus two")
            self.play(*appear(title), run_time=1.0)
            c.wait_until("same steps")
            self.play(*appear(ask), run_time=1.0)
            c.wait_until("odd")
            self.play(*swap(ask, odd), run_time=1.2)
            c.wait_until("slide")
            d = (lat.pair(1)[0].get_x() - lat.pair(0)[0].get_x()) / 2
            lab_y = lat.base[3][0].get_center()[1] - 0.34 * LAT_K
            odds = VGroup(*[MathTex(s, font_size=36, color=YELLOW).move_to([lat.pair(m)[0].get_x() + d, lab_y, 0])
                            for m, s in zip((-1, 0, 1), (r"-\pi", r"\pi", r"3\pi"))])
            self.play(*[p.animate.shift(d * RIGHT) for p in lat.pairs],
                      lat.b2.animate.shift(d * RIGHT), lat.b2_lab.animate.shift(d * RIGHT),
                      *during(disappear(lat.faded, lat.dots), 0, 0.35),
                      *during(appear(*odds, shift=None, lag=0.2), 0.6, 1),
                      run_time=min(2.0, c.until()))
        self.ex = [title, odd, lat, odds]

    # ------------------------------------------------------------ c4.recap.3: next time
    def clip3(self):
        nxt = T("Next time", 44, DIM).to_corner(UL, buff=0.6)
        circ = Circle(radius=1.3).set_stroke(BLUE, 3).move_to([-4.6, 0.3, 0])
        ell = Ellipse(width=4.0, height=2.2).set_stroke(BLUE, 3).move_to([0, 0.3, 0])
        a = 0.85
        hyp = VGroup(*[ParametricFunction(lambda t, s=s: np.array([s * a * math.cosh(t), a * math.sinh(t), 0]),
                                          t_range=[-1.4, 1.4]).set_stroke(TEAL, 3) for s in (1, -1)])
        hyp.move_to([4.6, 0.3, 0])
        part = T("Part 5 · Circles and ellipses", 34).move_to([0, -2.6, 0])
        with self.say("c4.recap.3") as c:
            sweep_clear(self, *appear(nxt), run_time=1.4)
            c.wait_until("circles")
            self.play(Create(circ), Create(ell), run_time=1.6)
            c.wait_until("hyperbolas")
            self.play(Create(hyp[0]), Create(hyp[1]), run_time=1.5)
            c.wait_until("tell them")
            self.play(*appear(part), run_time=1.0)  # early: end-card line (the next part's title)
