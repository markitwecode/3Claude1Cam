"""Chapter 1, scene 7: recap and the Part 2 preview (end card). Clips c1.recap.1 – c1.recap.3."""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch1_s1_hook")
S2 = load_scene("ch1_s2_define")
S3 = load_scene("ch1_s3_family")
S4 = load_scene("ch1_s4_cosix")
S6 = load_scene("ch1_s6_dictionary")

PANEL_X = (-4.75, 0.3, 4.95)
PIC_Y = 1.25            # centre of the panel pictures (1 and 3)
LINE_TOP = -1.75        # top of the panel lines
LINE_SZ = 28


def mx(src, color=FG):
    return MathTex(src, font_size=LINE_SZ * 1.3, color=color)


def row(*parts):
    g = VGroup(*parts).arrange(RIGHT, buff=0.12)
    for p in parts[1:]:
        if isinstance(p, MathTex):
            p.align_to(parts[0], DOWN)
    return g


def line_block(x, *rows, top=LINE_TOP):
    g = VGroup(*rows).arrange(DOWN, buff=0.16)
    g.move_to([x, 0, 0]).align_to([0, top, 0], UP)
    return g


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)           # end card: the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ------------------------------------------------------------ c1.recap.1
    def clip1(self):
        head = T("Recap", 44, DIM).move_to([0, 3.4, 0])
        self.head = head

        # panel 1: s2's averaging picture, built small with s2's builders (labels kept readable)
        ax = S2.graph_axes(x_length=2.8, y_length=3.5, ticks=False)
        ex, emx, ch, sh = S2.exp_curve(ax, 4), S2.emx_curve(ax, 4), S2.cosh_curve(ax, width=5), S2.sinh_curve(ax, width=5)
        lab = {k: S2.curve_label(ax, k, size=30) for k in ("exp", "emx", "cosh", "sinh")}
        marks = S2.x_marks(ax)
        for d in (marks.gold, marks.purple):
            d.scale(0.8)
        marks.mid.scale(0.85)
        p1 = VGroup(ax, ex, emx, ch, sh, marks, *lab.values())
        p1.move_to([PANEL_X[0], PIC_Y, 0]).align_to([-6.55, 0, 0], LEFT)
        assert p1.get_right()[0] < -2.8, p1.get_right()
        l1 = line_block(PANEL_X[0],
                        T("cosh, sinh: average", LINE_SZ),
                        T("and half-difference", LINE_SZ),
                        row(T("of", LINE_SZ), mx("e^{x}", GOLD), T("and", LINE_SZ), mx("e^{-x}", PURPLE)))

        # panel 2: s3's family card (no equation numbers), and the inverse card under it
        card = S3.family_card(size=27)
        for r, nm in zip(card.rows, card.nums):
            r.remove(nm)
        card.move_to([PANEL_X[1], 0, 0]).align_to([0, 2.85, 0], UP)
        inv = S3.inverse_card(size=28)
        inv.move_to([PANEL_X[1], card.get_bottom()[1] - 0.25 - inv.height / 2, 0])
        l2 = line_block(PANEL_X[1],
                        T("tanh = sinh / cosh,", LINE_SZ),
                        T("and three reciprocals", LINE_SZ))
        l2b = T("sech is not the inverse", LINE_SZ, RED).next_to(l2, DOWN, buff=0.16)

        self.p1, self.l1, self.p2, self.inv, self.l2, self.l2b = p1, l1, card, inv, l2, l2b
        self.card = card
        g = p1

        with self.say("c1.recap.1") as c:
            self.play(*appear(head, shift=None), run_time=1.0)  # early: section heading
            c.wait_until("r1")
            self.play(*appear(ax, ex, lab["exp"], emx, lab["emx"], shift=None, lag=0.2),
                      run_time=min(1.5, c.until("minus ex")))
            c.wait_until("minus ex")
            self.play(*appear(marks, ch, lab["cosh"], shift=None, lag=0.3),
                      run_time=min(1.5, c.until("half their")))
            c.wait_until("half their")
            self.play(*appear(sh, lab["sinh"], shift=None, lag=0.2), *appear(l1, lag=0.3),
                      run_time=min(1.5, c.until("r2")))
            settle(self, p1)

            c.wait_until("r2")
            self.play(*appear(card.rows[0], shift=None),
                      run_time=min(1.5, c.until("three reciprocals")))
            c.wait_until("three reciprocals")
            self.play(*appear(*card.rows[1:], shift=None, lag=0.3), *appear(l2, lag=0.3),
                      run_time=min(1.8, c.until("r2b")))
            settle(self, card)

            c.wait_until("r2b")
            sech = card.children[1]
            self.sech_box = SurroundingRectangle(sech, color=RED, buff=0.08).set_stroke(RED, 3)
            self.play(FadeIn(self.sech_box), run_time=0.8)
            c.wait_until("a different thing")
            self.play(*appear(inv, shift=None), *appear(l2b),
                      run_time=min(1.5, c.until(None)))

    # ------------------------------------------------------------ c1.recap.2
    def clip2(self):
        # s4/s6's dictionary card, rebuilt at a readable recap size (no equation numbers)
        rows = []
        for i, (src, pat, _n) in enumerate(S4.CARD_ROWS):
            tex = S4.at_glyph(S4.ctex(src, pat, size=32), S4.CARD_EQ, 0, -0.66 * i)
            r = VGroup(tex)
            r.tex = tex
            rows.append(r)
        left = min(r.tex.get_left()[0] for r in rows)
        header = S4.words_var("for every complex", "x", size=28, color=YELLOW)
        header.move_to([left, rows[0].tex.get_top()[1] + 0.3, 0], aligned_edge=DL)
        d = VGroup(header, *rows).move_to([PANEL_X[2], PIC_Y, 0])
        d.header, d.rows = header, rows
        l3 = line_block(PANEL_X[2],
                        S4.words_var("an", "i", "turns cosine", size=LINE_SZ, color=FG),
                        T("into cosh", LINE_SZ))
        l3[0][1].set_color(PINK)
        self.d, self.l3 = d, l3
        r1, r2, r3 = d.rows

        with self.say("c1.recap.2") as c:
            self.play(*appear(d.header, r1, r2, r3, shift=None, lag=0.3),  # early: card shown whole, header walked on r4
                      run_time=min(1.5, c.until("turns it")))
            c.wait_until("turns it")
            self.play(*appear(l3, lag=0.3), FlashAround(r1.tex[0][4], color=PINK, time_width=1.5),
                      run_time=min(1.2, c.until("extra")))
            c.wait_until("extra")
            pinks = [r2.tex[0][8], r3.tex[0][8]]
            self.play(*[FlashAround(p, color=PINK, time_width=1.5) for p in pinks],
                      *[p.animate.scale(1.3) for p in pinks], run_time=1.2)
            self.play(*[p.animate.scale(1 / 1.3) for p in pinks], run_time=0.6)
            c.wait_until("r4")
            self.play(FlashAround(d.header, run_time=2, time_width=1.5),
                      d.header.animate.scale(1.1), run_time=1.0)
            self.play(d.header.animate.scale(1 / 1.1), run_time=0.6)
            settle(self, d)

    # ------------------------------------------------------------ c1.recap.3
    def clip3(self):
        # the preview: circle + cos identity, hyperbola + cosh twin
        pair = S1.circle_hyperbola_pair(unit=0.5)
        for m in (pair.cdot, pair.hdot, pair.clabel, pair.hlabel):
            m.clear_updaters()
        circ = pair.circle_panel
        hyp = pair.hyper_panel
        circ.move_to([-4.4, 0.55, 0])
        hyp.move_to([-4.4, -2.0, 0])
        f1 = S6.part1_formula(size=52)
        f2 = S6.part2_formula(size=52)
        f1.shift(np.array([1.6, 0.3, 0]) - f1[0][11].get_center())      # '=' of f1 at x = 1.6
        f2.shift(np.array([1.6, -2.0, 0]) - f2[0][13].get_center())
        q = f2[0][6]
        eq_y = f2[0][13].get_y()
        box = Rectangle(width=0.36, height=0.48).set_stroke(YELLOW, 3).move_to([q.get_x(), eq_y, 0])
        q.set_opacity(0)
        minus = MathTex("-", font_size=52, color=YELLOW).move_to(box)
        part2 = T("Part 2 · Identities and the sign flip", 34)
        part2.move_to([0, 0, 0]).align_to([0, -3.45, 0], DOWN)
        # centre the end card's group in the space above the Part 2 line
        hero = VGroup(circ, hyp, f1, f2, box, minus)
        top, bot = 3.5, part2.get_top()[1] + 0.45
        hero.shift(UP * ((top + bot) / 2 - hero.get_center()[1]) + LEFT * hero.get_center()[0])
        part2.set_x(0)

        with self.say("c1.recap.3") as c:
            self.play(*disappear(self.head, self.p1, self.l1, self.p2, self.inv, self.sech_box,
                                 self.l2, self.l2b, self.d, self.l3), run_time=1.2)
            c.wait_until("cosine squared")
            self.play(*appear(f1, shift=None), *appear(circ, shift=None),
                      run_time=min(1.5, c.until("twin")))
            c.wait_until("twin")
            self.play(*appear(f2, box, shift=None, lag=0.3), run_time=min(1.4, c.until("minus")))
            c.wait_until("minus")
            self.play(FadeIn(minus, scale=0.6), FlashAround(box, time_width=1.5), run_time=1.2)
            c.wait_until("hyp")
            self.play(FadeOut(box), *appear(hyp, shift=None), run_time=1.5)
            self.play(*appear(part2), run_time=1.0)  # early: end-card line (the next part's title)
