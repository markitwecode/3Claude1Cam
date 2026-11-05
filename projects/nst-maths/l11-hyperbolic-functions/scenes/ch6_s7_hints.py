"""Chapter 6, scene 7: Examples Sheet G, four hints (no solutions). Clips c6.hints.1 – c6.hints.5.

Clip 1: "Your turn" -> the sheet header; ch7_s1's four G cards, dim, in their row; "a hint each, not a
solution"; the GOLD "solutions: Part 7 (bonus)" note. Clips 2-5: the row shrinks to a strip at the
top; each card in turn travels (drop, then slide) to the hero spot on the left, lit, its hints build
on the right, a "pause and try it" label holds under it, and it travels back, dim.

Shared (load_scene("ch6_s7_hints")) for the recap:
  sheet_header()   T 44 "Examples Sheet I · G. Hyperbolic functions" at y = 3.1
  hints_row(lit)   ch7_s1's card_row(lit): the four cards at ROW_X, ROW_Y
  sheet_note()     GOLD "solutions: Part 7 (bonus)" at y = -2.55
"""
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

S1 = load_scene("ch7_s1_intro")
G3 = load_scene("ch7_s4_g3")

STRIP_Y = 2.9
STRIP_S = 0.5
STRIP_X = [x * STRIP_S for x in S1.ROW_X]
HERO = np.array([-4.5, -0.9, 0])
HERO_S = 1.25
HX = 2.35          # centre of the hint area (x in -1.9 .. 6.6)


def sheet_header():
    return T("Examples Sheet I · G. Hyperbolic functions", 44).move_to([0, 3.1, 0])


def hints_row(lit=False):
    return S1.card_row(lit)


def sheet_note():
    return T("solutions: Part 7 (bonus)", 32, color=GOLD).move_to([0, -2.55, 0])


def pause_label():
    g = VGroup(S1.pause_icon(0.42, GOLD), T("pause and try it", 30, color=GOLD)).arrange(RIGHT, buff=0.25)
    return g.move_to([HERO[0], -3.25, 0])


def strip_card(k):
    """The card at half size in the top strip: body hidden, tag at size 30."""
    card = S1.g_card(k, lit=False).scale(STRIP_S).move_to([STRIP_X[k - 1], STRIP_Y, 0])
    card.body.set_opacity(0)
    card.tag.scale(1.5)
    return card


def hero_card(k):
    return S1.g_card(k, lit=True).scale(HERO_S).move_to(HERO)


def travel(card, end, out=True, run_time=1.6):
    """Card to `end` (same card, other size/style): out = drop first, then slide; back = slide, then rise."""
    card.align_data(end)
    start = card.copy()
    c0, c1 = start.get_center(), end.get_center()

    def upd(m, a):
        a = smooth(a)
        early, late = 1 - (1 - a) ** 2, a ** 2
        ax, ay, aw = (late, early, late) if out else (early, late, early)
        for sm, s1, s2 in zip(m.get_family(), start.get_family(), end.get_family()):
            sm.interpolate(s1, s2, a)
        m.scale_to_fit_width(start.width + (end.width - start.width) * aw)
        m.move_to([c0[0] + (c1[0] - c0[0]) * ax, c0[1] + (c1[1] - c0[1]) * ay, 0])

    return UpdateFromAlphaFunc(card, upd, run_time=run_time)


def id_card(tex, color):
    eq = MathTex(tex, font_size=44, color=color)
    box = SurroundingRectangle(eq, color=color, buff=0.25, corner_radius=0.1).set_stroke(color, 3)
    return VGroup(box, eq)


def empty_mini(label_tex, center, mirror=True, inv_tex=None):
    """Empty mini-axes; the label sits under them: f, a vertical double arrow, f^-1 (a pair) or just f."""
    ax = G3.eq_axes(G3.MINI_X, G3.MINI_Y, G3.MINI_U * 0.85, ORIGIN, ticks=False)
    parts = [ax]
    if mirror:
        parts.append(G3.mirror_line(ax, -2.0, 2.5))
    sketch = VGroup(*parts).move_to(center)
    if inv_tex is None:
        lab = MathTex(label_tex, font_size=44).next_to(sketch, RIGHT, buff=0.3)
    else:
        lab = VGroup(MathTex(label_tex, font_size=44),
                     MathTex(r"\Updownarrow", font_size=44, color=TEAL),
                     MathTex(inv_tex, font_size=44)).arrange(DOWN, buff=0.1)
        lab.next_to(sketch, DOWN, buff=0.2)
    g = VGroup(sketch, lab)
    g.ax, g.sketch, g.lab = ax, sketch, lab
    return g


class Ch6S7Hints(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ helpers
    def go_hero(self, k, rt):
        self.play(travel(self.row[k - 1], hero_card(k), out=True, run_time=rt))

    def go_back(self, k, leaving, rt):
        card = self.row[k - 1]
        self.play(*during(disappear(*leaving), 0, 0.35),
                  *during([travel(card, strip_card(k), out=False)], 0.35, 1), run_time=rt)

    def pause_hold(self, c):
        c.wait_until("try")
        lab = pause_label()
        self.play(*appear(lab, shift=None), run_time=0.8)
        return lab

    # ------------------------------------------------------------ c6.hints.1
    def clip1(self):
        with self.say("c6.hints.1") as c:
            turn = T("Your turn", 56, color=YELLOW).move_to([0, -1.6, 0])
            self.play(*appear(turn), run_time=1.0)
            c.wait_until("sheet")
            head = sheet_header()
            self.play(*appear(head), run_time=1.0)
            c.wait_until("four questions")
            row = hints_row(lit=False)
            self.play(*appear(*row, shift=None, lag=0.2), run_time=1.6)  # early: the four cards shown whole, then walked
            c.wait_until("plan")
            plan = T("a hint for each, not a solution", 34).move_to([0, -1.6, 0])
            self.play(*swap(turn, plan), run_time=1.2)
            c.wait_until("worked solutions")
            note = sheet_note()
            self.play(*appear(note), run_time=1.0)
            self.head, self.row, self.plan, self.note = head, row, plan, note

    # ------------------------------------------------------------ c6.hints.2 (G1)
    def clip2(self):
        with self.say("c6.hints.2") as c:
            row = self.row
            c.wait_until("express")
            self.play(*during(disappear(self.head, self.plan), 0, 0.4),
                      *during([Transform(row[i], strip_card(i + 1)) for i in range(4)]
                              + [self.note.animate.scale(30 / 32).move_to([4.3, -3.35, 0])], 0.4, 1),
                      run_time=1.4)
            self.go_hero(1, 1.6)
            c.wait_until("hint1")

            title = T("Example 33 · Part 2", 32, weight=BOLD)
            q = [r"\text{Find an identity for }", r"\tanh(", "A", "+", "B", r")\text{.}"]
            body = MathTex(*q, font_size=40)
            VGroup(title, body).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
            box = RoundedRectangle(corner_radius=0.15, width=body.width + 0.8,
                                   height=VGroup(title, body).height + 0.7,
                                   stroke_color=GREEN, stroke_width=3)
            VGroup(title, body).move_to(box)
            ex = VGroup(box, title, body).move_to([HX, 0.6, 0])
            self.play(FadeIn(box), *appear(title, body, lag=0.3), run_time=1.3)
            c.wait_until("new letters")
            new = MathTex(*[s.replace("A", "x").replace("B", "y") if s in ("A", "B") else s for s in q],
                          font_size=40)
            new[2].set_color(YELLOW)
            new[4].set_color(YELLOW)
            new.move_to(body).align_to(body, LEFT)
            self.play(*edit(body, new), run_time=1.5)

            h1 = T("try exponentials too", 34, color=YELLOW).move_to([HX, -1.35, 0])
            c.wait_until(own_word=h1)
            self.play(*appear(h1), run_time=1.0)
            c.wait_until("check your answer")
            h2 = T("check: sign-flip rule", 34, t2c={"check:": GREEN}).move_to([HX, -2.25, 0])
            self.play(*appear(h2), run_time=1.0)
            lab = self.pause_hold(c)
            self.leaving = [box, title, new, h1, h2, lab]

    # ------------------------------------------------------------ c6.hints.3 (G2)
    def clip3(self):
        with self.say("c6.hints.3") as c:
            self.go_back(1, self.leaving, 1.8)
            self.go_hero(2, 1.6)
            card = self.row[1]
            body = card.body

            def hl(i, color):
                return SurroundingRectangle(body[i], color=color, buff=0.12, corner_radius=0.08) \
                    .set_stroke(color, 3)
            c.wait_until("first")
            box = hl(0, BLUE)
            self.play(FadeIn(box), *set_alpha([body[1], body[2]], 0.4), run_time=1.0)
            c.wait_until("second")
            self.play(Transform(box, hl(1, TEAL)), *set_alpha([body[1]], 1), *set_alpha([body[0]], 0.4),
                      run_time=1.2)
            c.wait_until("task")
            self.play(Transform(box, hl(2, YELLOW)), *set_alpha([body[2]], 1), *set_alpha([body[1]], 0.4),
                      run_time=1.2)
            c.wait_until("hint2")
            self.play(FadeOut(box), *set_alpha([body[0], body[1]], 1), run_time=0.8)

            c.wait_until("hint2")
            circ = id_card(r"\cos^2\theta + \sin^2\theta = 1", BLUE).move_to([HX, 0.95, 0])
            hyp = id_card(r"\cosh^2\theta - \sinh^2\theta = 1", TEAL).move_to([HX, -0.45, 0])
            self.play(*appear(circ, hyp, lag=0.5), run_time=1.6)
            c.wait_until("which")
            which = T("which part?", 34, color=GOLD).move_to([HX - 1.7, -2.0, 0])
            self.play(*appear(which), run_time=1.0)
            c.wait_until("remember")
            ge = MathTex(r"\cosh\theta \ge 1", font_size=44, color=GREEN).move_to([HX + 1.6, -2.0, 0])
            self.play(*appear(ge), run_time=1.0)
            lab = self.pause_hold(c)
            self.leaving = [circ, hyp, which, ge, lab]

    # ------------------------------------------------------------ c6.hints.4 (G3)
    def clip4(self):
        with self.say("c6.hints.4") as c:
            self.go_back(2, self.leaving, 1.6)
            self.go_hero(3, 1.5)
            c.wait_until("pairs")
            xs, top = [-0.55, 2.25, 5.05], 1.05
            pairs = [empty_mini(r"e^x", [xs[0], top, 0], inv_tex=r"\ln x"),
                     empty_mini(r"\sinh x", [xs[1], top, 0], inv_tex=r"\sinh^{-1}x"),
                     empty_mini(r"\tanh x", [xs[2], top, 0], inv_tex=r"\tanh^{-1}x")]
            self.play(*appear(*[p.sketch for p in pairs], shift=None, lag=0.3), run_time=1.5)
            for p, cue in zip(pairs, ["E to the ex", "shine with inverse", "tanch with inverse"]):
                c.wait_until(cue)
                self.play(*appear(p.lab), run_time=0.9)

            c.wait_until("reflected")
            beams = [Line(p.ax.c2p(-2.0, -2.0), p.ax.c2p(2.5, 2.5)).set_stroke(YELLOW, 5) for p in pairs]
            first = T("draw first", 30, color=YELLOW).next_to(pairs[1].lab, DOWN, buff=0.25)
            self.play(*[VShowPassingFlash(b, time_width=0.5) for b in beams], run_time=1.5)
            self.play(*appear(first), run_time=0.9)

            c.wait_until("cosh")
            lone = empty_mini(r"\cosh x", [xs[0], -2.6, 0], mirror=False)
            lone.sketch.scale(0.85, about_point=lone.sketch.get_bottom())
            lone.lab.next_to(lone.sketch, RIGHT, buff=0.3)
            self.play(*appear(lone.sketch, lone.lab, shift=None, lag=0.3), run_time=1.2)
            c.wait_until("mark")
            t1 = T("intercepts", 30, color=GOLD).move_to([xs[2], -1.95, 0])
            t2 = T("asymptotes", 30, color=GOLD).move_to([xs[2], -2.55, 0])
            c.wait_until("crosses")
            self.play(*appear(t1), run_time=0.9)
            c.wait_until("asymptotes")
            self.play(*appear(t2), run_time=0.9)
            lab = self.pause_hold(c)
            self.leaving = [*pairs, first, lone, t1, t2, lab]

    # ------------------------------------------------------------ c6.hints.5 (G4)
    def clip5(self):
        with self.say("c6.hints.5") as c:
            self.go_back(3, self.leaving, 1.6)
            self.go_hero(4, 1.5)
            c.wait_until("hint4")
            tag = T("Example 34 · Part 3", 30, color=DIM).move_to([HX, 1.45, 0])
            res = MathTex(r"\tanh^{-1}x = \tfrac{1}{2}", r"\ln\!\Big[\;\,", r"\frac{1+x}{1-x}", r"\;\,\Big]",
                          r",\quad |x|<1", font_size=46).move_to([HX, 0.3, 0])
            self.play(*appear(tag, res, lag=0.4), run_time=1.4)
            logq = VGroup(res[1], res[2], res[3])
            brace = Brace(logq, DOWN, buff=0.3, color=YELLOW)
            split = T("split first", 32, color=YELLOW).next_to(brace, DOWN, buff=0.15)
            c.wait_until(own_word=split)
            self.play(GrowFromCenter(brace), *appear(split), run_time=1.2)
            c.wait_until("chain")
            den = res[2][-3:]
            ring = Ellipse(width=den.width + 0.45, height=den.height + 0.16).move_to(den).shift(0.05 * DOWN)
            ring.set_stroke(YELLOW, 4)
            self.play(GrowFromCenter(ring), run_time=1.0)
            self.pause_hold(c)
