"""Chapter 7, scene 1: spoilers ahead, and the four G cards. Clips c7.intro.1 – c7.intro.2.

Title card (+ GOLD "Bonus" tag); last time's circle / hyperbola pair; a GOLD "SPOILERS AHEAD"
banner with a big pause icon; the four question cards in a row, lit one by one; the ritual chips.
Ends on `handover_shot()`: the four lit cards alone (ch7_s2 opens on it and grows G1).

Shared with s2-s6 (import with load_scene("ch7_s1_intro")):
  pause_icon(height=1.0, color=GOLD)  two rounded bars, centred at ORIGIN
  g_card(k, lit=True)                 card k (1-4), CARD_W x CARD_H, centred at ORIGIN;
                                      .frame .tag ("G1".."G4") .body (its formula lines)
  card_row(lit=True)                  the four cards at x = ROW_X, y = ROW_Y
  handover_shot()                     card_row(lit=True)
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
from lib.titles import title_card  # noqa: E402

CARD_W, CARD_H = 3.0, 3.0
ROW_Y = 0.8
ROW_X = [-4.95, -1.65, 1.65, 4.95]
CHIP_Y = -1.95
BODY_DIM = 0.35


def pause_icon(height=1.0, color=GOLD):
    w = 0.24 * height
    bars = VGroup(*[RoundedRectangle(corner_radius=0.25 * w, width=w, height=height)
                    .set_stroke(width=0).set_fill(color, 1) for _ in range(2)])
    bars.arrange(RIGHT, buff=0.22 * height)
    return bars.move_to(ORIGIN)


def _fit(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def _body(k):
    if k == 1:
        lines = [MathTex(r"\tanh(x+y)", font_size=46),
                 T("in terms of", 30, color=DIM),
                 MathTex(r"\tanh x,\ \tanh y", font_size=38)]
    elif k == 2:
        lines = [MathTex(r"(a\cos\theta,\ b\sin\theta)", font_size=36, color=BLUE),
                 MathTex(r"(a\cosh\theta,\ b\sinh\theta)", font_size=36, color=TEAL),
                 T("locus? sketch it", 30, color=DIM)]
    elif k == 3:
        lines = [MathTex(r"e^x,\ \cosh x", font_size=38),
                 MathTex(r"\tanh x,\ \ln x", font_size=38),
                 MathTex(r"\sinh^{-1}x,\ \tanh^{-1}x", font_size=38)]
    else:
        lines = [MathTex(r"\tanh^{-1}x", font_size=46),
                 T("as a logarithm,", 30, color=DIM),
                 T("and differentiate", 30, color=DIM)]
    body = VGroup(*lines).arrange(DOWN, buff=0.28)
    for ln in lines:
        _fit(ln, CARD_W - 0.3)
    return body


def g_card(k, lit=True):
    frame = RoundedRectangle(corner_radius=0.15, width=CARD_W, height=CARD_H)
    frame.set_fill(BG, 1)
    tag = T(f"G{k}", 40, weight=BOLD)
    body = _body(k)
    tag.move_to(frame.get_top() + 0.45 * DOWN)
    body.move_to(frame.get_center() + 0.35 * DOWN)
    if lit:
        frame.set_stroke(BLUE, 3)
        tag.set_color(YELLOW)
    else:
        frame.set_stroke(DIM, 2)
        tag.set_color(DIM)
        body.set_opacity(BODY_DIM)
    card = VGroup(frame, tag, body)
    card.frame, card.tag, card.body = frame, tag, body
    return card


def card_row(lit=True):
    row = VGroup(*[g_card(k + 1, lit) for k in range(4)])
    for c, x in zip(row, ROW_X):
        c.move_to([x, ROW_Y, 0])
    return row


def handover_shot():
    return card_row(lit=True)


def _chip(parts, color):
    inner = VGroup(*parts).arrange(RIGHT, buff=0.2)
    box = RoundedRectangle(corner_radius=0.18, width=inner.width + 0.5, height=0.75)
    box.set_stroke(color, 2).set_fill(color, 0.12).move_to(inner)
    return VGroup(box, inner)


class Ch7S1Intro(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()

    def clip1(self):
        with self.say("c7.intro.1") as c:
            card = title_card("Part 7 · Solutions to Examples Sheet G")
            _fit(card.title, 12.6)
            bonus_t = T("Bonus", 30, color=GOLD)
            bonus_box = RoundedRectangle(corner_radius=0.15, width=bonus_t.width + 0.5, height=0.62)
            bonus_box.set_stroke(GOLD, 2).set_fill(GOLD, 0.12)
            bonus = VGroup(bonus_box, bonus_t)
            bonus.next_to(card.part, DOWN, buff=0.4)
            bonus_t.move_to(bonus_box)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(*appear(card.course), run_time=0.9)  # early: title card
            self.play(*appear(card.part), run_time=0.9)
            c.wait_until("bonus")
            self.play(*appear(bonus), run_time=0.8)
            self.play(FlashAround(bonus_box, color=GOLD, run_time=1.2))
            c.wait_until("last")

            # last time's pair: circle and hyperbola
            cx, R = -3.4, 1.6
            hx, U = 3.0, 0.95
            c_axes = VGroup(Line([cx - 2.2, 0, 0], [cx + 2.2, 0, 0]),
                            Line([cx, -2.2, 0], [cx, 2.2, 0])).set_stroke(DIM, 2)
            circ = Circle(radius=R).move_to([cx, 0, 0]).set_stroke(BLUE, 4)
            h_axes = VGroup(Line([hx - 2.6, 0, 0], [hx + 2.6, 0, 0]),
                            Line([hx, -2.3, 0], [hx, 2.3, 0])).set_stroke(DIM, 2)
            asym = VGroup(DashedLine([hx - 2.3, -2.3, 0], [hx + 2.3, 2.3, 0]),
                          DashedLine([hx - 2.3, 2.3, 0], [hx + 2.3, -2.3, 0])).set_stroke(DIM, 2)
            branches = VGroup(*[
                ParametricFunction(lambda t, s=s: np.array([hx + s * U * np.cosh(t), U * np.sinh(t), 0]),
                                   t_range=[-1.5, 1.5]).set_stroke(TEAL, 4)
                for s in (1, -1)])
            th = ValueTracker(0.35)
            cdot = always_redraw(lambda: Dot([cx + R * np.cos(th.get_value()), R * np.sin(th.get_value()), 0],
                                             radius=0.11, color=BLUE))
            hdot = always_redraw(lambda: Dot([hx + U * np.cosh(th.get_value()), U * np.sinh(th.get_value()), 0],
                                             radius=0.11, color=TEAL))
            c_lab = MathTex(r"(\cos\theta,\ \sin\theta)", font_size=38, color=BLUE).move_to([cx, 2.8, 0])
            h_lab = MathTex(r"(\cosh\theta,\ \sinh\theta)", font_size=38, color=TEAL).move_to([hx, 2.8, 0])
            c_eq = MathTex(r"x^2 + y^2 = 1", font_size=40, color=BLUE).move_to([cx, -2.85, 0])
            h_eq = MathTex(r"x^2 - y^2 = 1", font_size=40, color=TEAL).move_to([hx, -2.85, 0])
            pair = VGroup(c_axes, circ, h_axes, asym, branches, c_lab, h_lab, c_eq, h_eq)

            self.play(*during(disappear(*[m for m in self.mobjects]), 0, 0.45),
                      *during([FadeIn(VGroup(c_axes, h_axes, asym)), Create(circ), Create(branches[0]),
                               Create(branches[1])], 0.45, 1),
                      run_time=1.6)
            self.add(cdot, hdot)
            self.play(*appear(c_lab, h_lab, c_eq, h_eq, lag=0.15), FadeIn(cdot), FadeIn(hdot), run_time=1.1)
            self.play(th.animate.set_value(1.25), run_time=min(2.5, 0.8 * c.until("warn")), rate_func=smooth)
            c.wait_until("warn")

            # spoilers banner
            banner = T("SPOILERS AHEAD", 56, color=GOLD, weight=BOLD).move_to([0, 1.7, 0])
            icon = pause_icon(2.0, GOLD).move_to([0, -0.9, 0])
            cdot.clear_updaters()
            hdot.clear_updaters()
            self.play(*during(disappear(pair, cdot, hdot), 0, 0.45),
                      *during(appear(banner, icon, lag=0.3), 0.5, 1), run_time=1.6)
            c.wait_until("pause now")
            self.play(icon.animate.scale(1.15), rate_func=there_and_back, run_time=1.2)
            self.banner, self.icon = banner, icon

    def clip2(self):
        with self.say("c7.intro.2", gap=2.0) as c:
            row = card_row(lit=False)
            lit = card_row(lit=True)
            self.play(*during(disappear(self.banner, self.icon), 0, 0.45), *during(appear(*row, shift=None, lag=0.15), 0.4, 1), run_time=min(1.8, c.until("g1")))  # early: the four cards shown whole, then walked
            for i, cue in enumerate(["g1", "g2", "g3", "g4"]):
                c.wait_until(cue)
                rt = 1.2 if i == 0 else 1.0
                self.play(Transform(row[i], lit[i]), run_time=rt)
                self.play(row[i].animate.scale(1.08), rate_func=there_and_back, run_time=0.6)
            # row now shows exactly the lit row

            c.wait_until("pause")
            chips = [
                _chip([T("pause", 30), pause_icon(0.36, FG)], FG),
                _chip([T("solve", 30)], FG),
                _chip([cross_mark(RED).scale(0.8), T("the tempting mistake", 30, color=RED)], RED),
                _chip([check_mark(GREEN).scale(0.8), T("check", 30, color=GREEN)], GREEN),
            ]
            VGroup(*chips).arrange(RIGHT, buff=0.4).move_to([0, CHIP_Y, 0])
            self.play(*appear(chips[0]), run_time=0.9)
            c.wait_until("then the solution")
            self.play(*appear(chips[1]), run_time=0.9)
            c.wait_until("mistake")
            self.play(*appear(chips[2]), run_time=0.9)
            c.wait_until("check")
            self.play(*appear(chips[3]), run_time=0.9)
            self.chips = chips
        self.play(*disappear(*self.chips), run_time=0.9)
        self.wait(1.0)
