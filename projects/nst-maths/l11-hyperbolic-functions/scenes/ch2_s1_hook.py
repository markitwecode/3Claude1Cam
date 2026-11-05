"""Chapter 2, scene 1: hook: the dictionary returns, cos^2+sin^2 meets its twin, two routes. Clips c2.hook.1 – c2.hook.3.

`dictionary_card()` is the big centred card; `docked_card()` is its corner form (scaled to width
3.2, to_corner(UR, buff=0.25)), rebuilt identically by ch2_s3 and ch2_s6.
"""
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
from lib.titles import title_card  # noqa: E402

_COL = {"B": BLUE, "T": TEAL, "P": PINK, "G": GOLD, "U": PURPLE, "F": FG, "Y": YELLOW, "D": DIM}


def ctex(src, pattern, size=52):
    """MathTex coloured glyph by glyph: one letter of `pattern` per glyph (spaces ignored)."""
    m = MathTex(src, font_size=size)
    pat = pattern.replace(" ", "")
    assert len(m[0]) == len(pat), (src, len(m[0]), len(pat))
    for g, ch in zip(m[0], pat):
        g.set_color(_COL[ch])
    return m


CARD_ROWS = [
    (r"\cos(ix) = \cosh x", "BBBFPFFF TTTTF"),
    (r"\sin(ix) = i \sinh x", "BBBFPFFF P TTTTF"),
    (r"\tan(ix) = i \tanh x", "BBBFPFFF P TTTTF"),
]
CARD_EQ = 7  # glyph index of "=" in every row


def dictionary_card():
    """Big centred dictionary card: VGroup(box, rows); .box, .rows (each a MathTex)."""
    rows = VGroup()
    for i, (src, pat) in enumerate(CARD_ROWS):
        r = ctex(src, pat, size=68)
        r.shift(np.array([0, -i * 1.3, 0]) - r[0][CARD_EQ].get_center())
        rows.add(r)
    box = RoundedRectangle(corner_radius=0.3, width=rows.width + 1.0, height=rows.height + 0.9,
                           stroke_color=DIM, stroke_width=2).move_to(rows)
    card = VGroup(box, rows).move_to(ORIGIN)
    card.box, card.rows = box, rows
    return card


def docked_card():
    """The corner form, shared with ch2_s3 / ch2_s6."""
    return dictionary_card().scale_to_fit_width(3.2).to_corner(UR, buff=0.25)


def ident_trig(size=52):
    return ctex(r"\cos^2 x + \sin^2 x \equiv 1", "BBBBB B BBBBB BB", size=size)


def ident_hyp(size=52):
    m = ctex(r"\cosh^2 x - \sinh^2 x \equiv 1", "TTTTTT Y TTTTTT TT", size=size)
    return m


MINUS = 6   # glyph index of "-" in ident_hyp
EQUIV_T, EQUIV_H = 11, 13


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ title, dictionary returns
    def clip1(self):
        with self.say("c2.hook.1") as c:
            card_t = title_card("Part 2 · Identities and the sign flip")
            if card_t.title.width > 12:
                card_t.title.scale_to_fit_width(12)
            self.play(FadeIn(card_t.title, shift=0.3 * DOWN), GrowFromCenter(card_t.rule),  # early: title card
                      time_span(FadeIn(card_t.course), 0.3, 0.9),
                      time_span(FadeIn(card_t.part, shift=0.2 * DOWN), 0.5, 1.1),
                      run_time=1.1)
            c.wait_until("we found")

            card = dictionary_card()
            self.card = card
            sweep_clear(self, time_span(FadeIn(card.box), 0.7, 1.4),
                        *[time_span(FadeIn(r, shift=0.2 * DOWN), 0.8 + 0.25 * i, 1.6 + 0.25 * i)
                          for i, r in enumerate(card.rows)],
                        run_time=2.1)
            c.wait_until("putting an eye")
            self.play(*[FlashAround(card.rows[i][0][4], color=PINK, time_width=1.5) for i in range(3)],
                      run_time=1.5)
            c.wait_until("the cosine of eye ex")
            self.play(FlashAround(card.rows[0], time_width=1.5), run_time=1.6)
            c.wait_until("the sine of eye ex")
            self.play(FlashAround(card.rows[1], time_width=1.5), run_time=1.6)
            c.wait_until("times shine")
            self.play(card.animate.scale_to_fit_width(3.2).to_corner(UR, buff=0.25),
                      run_time=min(1.8, c.until()))

    # ------------------------------------------------------------ circle, identity, twin, doors
    def clip2(self):
        with self.say("c2.hook.2") as c:
            ctr = np.array([-4.6, 1.15, 0])
            r = 1.8
            th = 50 * DEGREES
            P = ctr + r * np.array([np.cos(th), np.sin(th), 0])
            foot = np.array([P[0], ctr[1], 0])
            circle = Circle(radius=r, color=BLUE, stroke_width=4).move_to(ctr)
            centre_dot = Dot(ctr, radius=0.05, color=FG)
            hyp = Line(ctr, P, color=FG, stroke_width=4)
            leg_c = Line(ctr, foot, color=BLUE, stroke_width=4)
            leg_s = Line(foot, P, color=BLUE, stroke_width=4)
            pdot = Dot(P, radius=0.08, color=YELLOW)
            arc = Arc(radius=0.45, start_angle=0, angle=th, arc_center=ctr, color=DIM, stroke_width=3)
            lab_th = MathTex(r"\theta", font_size=32, color=FG).move_to(
                ctr + 0.72 * np.array([np.cos(th / 2), np.sin(th / 2), 0]))
            lab_c = MathTex(r"\cos\theta", font_size=34, color=BLUE).next_to(leg_c, DOWN, buff=0.15)
            lab_s = set_backstroke(MathTex(r"\sin\theta", font_size=34, color=BLUE).next_to(leg_s, RIGHT, buff=0.12))
            lab_1 = MathTex("1", font_size=34, color=FG).move_to(
                (ctr + P) / 2 + 0.3 * np.array([-np.sin(th), np.cos(th), 0]))

            self.play(Create(circle), FadeIn(centre_dot), time_span(FadeIn(pdot, scale=0.5), 0.8, 1.2),
                      run_time=1.2)
            self.play(Succession(Create(leg_c), Create(leg_s), Create(hyp)),
                      time_span(FadeIn(arc), 0.9, 1.3), run_time=1.3)
            self.play(*appear(lab_c, lab_s, lab_1, lab_th, lag=0.2), run_time=1.1)  # early: diagram labels

            id1 = ident_trig()
            id1.shift(np.array([2.1, 1.4, 0]) - id1[0][EQUIV_T].get_center())
            c.wait_until("cosine squared")
            self.play(*appear(id1), run_time=1.3)
            c.wait_until("triangle")
            self.play(*[VShowPassingFlash(m.copy().set_stroke(YELLOW, 7), time_width=0.6)
                        for m in (leg_c, leg_s, hyp)], run_time=1.6)

            id2 = ident_hyp()
            id2.shift(np.array([2.1, -0.1, 0]) - id2[0][EQUIV_H].get_center())
            c.wait_until("twin")
            self.play(*appear(id2), run_time=min(1.4, c.until("with a minus")))
            c.wait_until("with a minus")
            self.play(FlashAround(id2[0][MINUS], time_width=1.5), run_time=1.4)

            q = T("?", size=60, color=YELLOW, weight=BOLD)
            q.move_to(id2[0][MINUS].get_center() + 0.7 * UP)
            c.wait_until("ask")
            self.play(*appear(q, shift=0.35 * DOWN), run_time=1.0)

            # the two doors
            panels = VGroup(*[RoundedRectangle(corner_radius=0.25, width=6.1, height=2.6,
                                               stroke_color=col, stroke_width=3)
                              for col in (GOLD, PINK)])
            panels[0].move_to([-3.45, -2.3, 0])
            panels[1].move_to([3.45, -2.3, 0])
            c.wait_until("doors")
            self.play(*[GrowFromCenter(p) for p in panels], run_time=1.3)

            lab_e = T("expand the definitions", size=32, color=GOLD)
            lab_e.move_to(panels[0].get_top() + 0.42 * DOWN)
            half = ctex(r"\tfrac{1}{2}(e^{x} + e^{-x})", "FFF F GG F UUU F", size=52)
            half.move_to(panels[0].get_center() + 0.32 * DOWN)
            c.wait_until(own_word=lab_e)
            self.play(*appear(lab_e), run_time=1.0)
            c.wait_until("in exponentials")
            self.play(*appear(half), run_time=1.2)

            lab_d = T("through the complex door", size=32, color=PINK)
            lab_d.move_to(panels[1].get_top() + 0.42 * DOWN)
            big_i = MathTex("i", font_size=84, color=PINK).move_to(
                panels[1].get_center() + np.array([-1.75, -0.32, 0]))
            thumb = dictionary_card().rows.arrange(DOWN, buff=0.3, aligned_edge=LEFT).scale_to_fit_width(2.7).move_to(
                panels[1].get_center() + np.array([1.1, -0.32, 0]))
            c.wait_until(own_word=lab_d)
            self.play(*appear(lab_d, big_i, lag=0.4), run_time=1.2)
            c.wait_until("with the dictionary")
            self.play(FlashAround(self.card, color=PINK, time_width=1.5),
                      FadeIn(thumb, shift=0.25 * DOWN), run_time=min(1.3, c.until()))

            self.diagram = VGroup(circle, centre_dot, hyp, leg_c, leg_s, pdot, arc,
                                  lab_th, lab_c, lab_s, lab_1)
            self.id1, self.id2, self.q = id1, id2, q
            self.panels = panels

    # ------------------------------------------------------------ both routes, one rule?
    def clip3(self):
        with self.say("c2.hook.3", gap=2.6) as c:
            self.play(*[FlashAround(p, color=p.get_stroke_color(), time_width=1.5) for p in self.panels],
                      run_time=1.8)
            c.wait_until("rule")

            blue = RoundedRectangle(corner_radius=0.3, width=4.8, height=2.2,
                                    stroke_color=BLUE, stroke_width=4).move_to([-3.7, -0.3, 0])
            teal = RoundedRectangle(corner_radius=0.3, width=4.8, height=2.2,
                                    stroke_color=TEAL, stroke_width=4).move_to([3.7, -0.3, 0])
            id1 = self.id1
            id1.generate_target()
            id1.target.scale(0.85).move_to(blue)
            sweep_clear(self, time_span(MoveToTarget(id1), 1.0, 2.0),
                        time_span(GrowFromCenter(blue), 1.0, 1.8),
                        time_span(GrowFromCenter(teal), 1.2, 2.0),
                        keep=[self.card, id1], run_time=2.0)

            arrow = Arrow(blue.get_right(), teal.get_left(), buff=0.2, color=YELLOW, stroke_width=6)
            one = T("one rule?", size=36, color=YELLOW).next_to(arrow, UP, buff=0.2)
            c.wait_until(own_word=one)
            self.play(GrowArrow(arrow), *appear(one), run_time=1.2)

            lab_b = T("trig identity", size=34, color=BLUE).next_to(blue, DOWN, buff=0.3)
            lab_t = T("hyperbolic twin", size=34, color=TEAL).next_to(teal, DOWN, buff=0.3)
            c.wait_until(own_word=lab_b)
            self.play(*appear(lab_b), run_time=1.0)
            c.wait_until(own_word=lab_t)
            self.play(*appear(lab_t), run_time=1.0)
