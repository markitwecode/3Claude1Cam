"""Chapter 7, scene 1: spoilers ahead, and the four question cards. Clips c7.intro.1 – c7.intro.2.

Opens on open_card() fully drawn (ch6 s7 ends on it); the GOLD "Bonus" tag joins under .part on
"a bonus". {last}: ch6 s2's labelled figure (strip removed), small. {warn}: "SPOILERS AHEAD" + a big
pause icon. {cards}: H1, H2, H4, I1 in a row, dim, lit on {h12} {h4} {i1}; {later}: dim H3 / H5 with
"next lecture: curve sketching" slide off right; {ritual}/{mistake}: chips under the row. Ends on
handover_shot() (the lit row alone); ch7 s2 opens on it and grows H1.

Shared (load_scene("ch7_s1_intro")):
  open_card()            the bare title_card(PART7) at ORIGIN (ch6 s7's end card)
  h1_card(), h2_card()   full verbatim cards in ch3 s7's question_card style, centred at ORIGIN, ~9.4 wide;
                         parts .frame .label .body .intro (the instruction Tex lines) .parts (8 Tex, (a)..(h))
  h4_card()              ch3_s7_recap's
  i1_card()              ch5_s7_recap's once it defines one, else a stand-in to the same spec
  question_card          ch3_s7_recap's
  CARD_MAKERS            [h1_card, h2_card, h4_card, i1_card]
  card_row(lit=True)     the four cards, each a small copy of its full card (label enlarged to read at
                         480p), at x = ROW_X, y = ROW_Y; lit = bool or a set of indices (0..3). Unlit:
                         label DIM, body at 0.35. Grow card i to the hero with
                         Transform(row[i], h1_card().move_to(...)) (same glyphs; no TransformFromCopy).
  pause_icon(height=1.0, color=GOLD)   two rounded bars at ORIGIN
  handover_shot()        card_row(lit=True)
"""
# style: 2
# handover: next
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
from lib.titles import title_card  # noqa: E402

PART7 = "Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1"
_s37 = load_scene("ch3_s7_recap")
question_card = _s37.question_card
h4_card = _s37.h4_card

CARD_SLOT_W = 3.05
ROW_X = [-5.1, -1.7, 1.7, 5.1]
ROW_Y = 0.9
ROW_LABEL_SIZE = 32
BODY_DIM = 0.35
CHIP_Y = -2.45


# ------------------------------------------------------------------ shared helpers

def open_card():
    """ch7's opening card: the bare engine title card, static, at ORIGIN."""
    return title_card(PART7)


def pause_icon(height=1.0, color=GOLD):
    w = 0.24 * height
    bars = VGroup(*[RoundedRectangle(corner_radius=0.25 * w, width=w, height=height)
                    .set_stroke(width=0).set_fill(color, 1) for _ in range(2)])
    bars.arrange(RIGHT, buff=0.22 * height)
    return bars.move_to(ORIGIN)


def _grid_card(label, intro, parts, width=9.4, size=40):
    """question_card's style (DIM frame r 0.2, YELLOW T 36 label, white Tex 40), with the parts
    (a)..(h) laid out two per row."""
    intro_t = VGroup(*[Tex(s, font_size=size, color=FG) for s in intro]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    part_t = [Tex(s, font_size=size, color=FG) for s in parts]
    grid = VGroup(*part_t).arrange_in_grid(rows=len(parts) // 2, cols=2, buff=(0.7, 0.32),
                                           col_alignments="ll", flow_order="rd")
    body = VGroup(intro_t, grid).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    pad = 0.35
    if body.width > width - 2 * pad:
        body.scale_to_fit_width(width - 2 * pad)
    lab = T(label, 36, YELLOW)
    content = VGroup(lab, body).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame = RoundedRectangle(corner_radius=0.2, width=width, height=content.height + 2 * pad)
    frame.set_stroke(DIM, 2).set_fill(opacity=0)
    content.move_to(frame.get_corner(UL) + np.array([pad, -pad, 0]), aligned_edge=UL)
    g = VGroup(frame, lab, body)
    g.move_to(ORIGIN)
    g.frame, g.label, g.body, g.intro, g.parts = frame, lab, body, intro_t, part_t
    return g


def h1_card():
    """Examples sheet 1, H1, verbatim."""
    return _grid_card("H1", [r"Calculate the following derivatives:"], [
        r"(a) $\dfrac{d}{dx}(x^2+3)$",
        r"(b) $\dfrac{d}{dx}(x^4+2x+6)$",
        r"(c) $\dfrac{d}{dx}(ax^n+bx+c)$",
        r"(d) $\dfrac{d}{dx}e^x$",
        r"(e) $\dfrac{d}{dt}(at+bt^2\sin\theta)$",
        r"(f) $\dfrac{d}{dx}(1+x^{2/3})$",
        r"(g) $\dfrac{d}{dy}\dfrac{1}{1+y}$",
        r"(h) $\dfrac{d}{dx}\ln x$",
    ])


def h2_card():
    """Examples sheet 1, H2, verbatim."""
    return _grid_card("H2", [
        r"By writing the trigonometric and hyperbolic functions",
        r"in terms of exponentials, evaluate the following",
        r"derivatives:",
    ], [
        r"(a) $\dfrac{d}{dx}\sin x$",
        r"(b) $\dfrac{d}{d\theta}\cos\theta$",
        r"(c) $\dfrac{d}{dt}\tan t$",
        r"(d) $\dfrac{d}{d\omega}\sin(-i\omega t)$",
        r"(e) $\dfrac{d}{dx}\sinh x$",
        r"(f) $\dfrac{d}{dx}\cosh x$",
        r"(g) $\dfrac{d}{dx}\tanh x$",
        r"(h) $\dfrac{d}{dx}\tanh 2x$",
    ])


def i1_card():
    """ch5_s7_recap's I1 card once it exists; until then a stand-in to its brief (verbatim, e^{-x^2/2} PURPLE)."""
    if (Path(__file__).resolve().parent / "ch5_s7_recap.py").exists():
        mod = load_scene("ch5_s7_recap")
        if hasattr(mod, "i1_card"):
            return mod.i1_card()
    return question_card("I1", [
        r"Use Leibniz's formula to establish that",
        r"$Z_n \equiv \dfrac{d^n}{dx^n}\,e^{-x^2/2}$ is a solution of the",
        r"differential equation",
        r"$\dfrac{d^2Z_n}{dx^2} + x\,\dfrac{dZ_n}{dx} + (n+1)Z_n = 0$.",
    ], colors={"e^{-x^2/2}": PURPLE})


CARD_MAKERS = [h1_card, h2_card, h4_card, i1_card]


def _row_card(i, lit):
    """Card i small, for the row: whole card scaled to the slot, label enlarged (readable at 480p),
    body shifted under it, frame lengthened to match."""
    card = CARD_MAKERS[i]()
    card.scale_to_fit_width(CARD_SLOT_W)
    lab, body, frame = card.label, card.body, card.frame
    ul = lab.get_corner(UL)
    gap = lab.get_bottom()[1] - body.get_top()[1]
    lab.scale(T("H1", ROW_LABEL_SIZE).height / lab.height, about_point=ul)
    drop = (lab.get_bottom()[1] - gap) - body.get_top()[1]
    body.shift(drop * UP)
    top = frame.get_top()[1]
    frame.stretch_to_fit_height(frame.height - drop)
    frame.shift((top - frame.get_top()[1]) * UP)
    if not lit:
        lab.set_color(DIM)
        body.set_opacity(BODY_DIM)
    return card


def card_row(lit=True):
    lit_set = set(range(4)) if lit is True else (set() if not lit else set(lit))
    row = VGroup(*[_row_card(i, i in lit_set) for i in range(4)])
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


def _mini(label):
    frame = RoundedRectangle(corner_radius=0.15, width=1.7, height=1.1).set_stroke(DIM, 2)
    return VGroup(frame, T(label, 32, DIM).move_to(frame))


# ------------------------------------------------------------------ the scene

class Ch7S1Intro(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()

    def clip1(self):
        with self.say("c7.intro.1") as c:
            card = open_card()
            self.add(card)
            bonus_t = T("Bonus", 30, color=GOLD)
            bonus_box = RoundedRectangle(corner_radius=0.15, width=bonus_t.width + 0.5, height=0.62)
            bonus_box.set_stroke(GOLD, 2).set_fill(GOLD, 0.12)
            bonus = VGroup(bonus_box, bonus_t)
            bonus.next_to(card.part, DOWN, buff=0.4)
            bonus_t.move_to(bonus_box)
            c.wait_until("a bonus")
            self.play(*appear(bonus), run_time=0.9)
            self.play(FlashAround(bonus_box, color=GOLD, run_time=1.2))
            c.wait_until("last")

            # last time: part six's labelled figure, small
            lf = load_scene("ch6_s2_vocab").labelled_figure()
            lf.remove(lf.strip)
            lf.scale(0.88).move_to(ORIGIN)
            self.play(*during(disappear(card, bonus), 0, 0.45), *during([FadeIn(lf)], 0.45, 1), run_time=1.6)  # early: last time's figure, shown whole
            c.wait_until("warn")

            # spoilers banner
            banner = T("SPOILERS AHEAD", 56, color=GOLD, weight=BOLD).move_to([0, 1.7, 0])
            icon = pause_icon(2.0, GOLD).move_to([0, -0.9, 0])
            self.play(*during(disappear(lf), 0, 0.45),
                      *during(appear(banner, icon, lag=0.3), 0.5, 1), run_time=1.6)
            c.wait_until("pause now")
            self.play(icon.animate.scale(1.15), rate_func=there_and_back, run_time=1.2)
            self.banner, self.icon = banner, icon

    def clip2(self):
        with self.say("c7.intro.2", gap=4.6) as c:
            row = card_row(lit=False)
            lit = card_row(lit=True)
            self.play(*during(disappear(self.banner, self.icon), 0, 0.45),
                      *during(appear(*row, shift=None, lag=0.15), 0.4, 1), run_time=min(1.8, c.until("h12")))  # early: the four cards shown whole, then lit one by one

            c.wait_until("h12")
            self.play(Transform(row[0], lit[0]), Transform(row[1], lit[1]), run_time=1.2)
            self.play(FlashAround(row[0].frame, run_time=1.2), FlashAround(row[1].frame, run_time=1.2))
            for i, cue in ((2, "h4"), (3, "i1")):
                c.wait_until(cue)
                self.play(Transform(row[i], lit[i]), run_time=1.0)
                self.play(FlashAround(row[i].frame, run_time=1.2))

            # H3 and H5: next lecture
            c.wait_until("later")
            minis = VGroup(_mini("H3"), _mini("H5")).arrange(RIGHT, buff=0.4)
            tag = T("next lecture: curve sketching", 30, DIM)
            later = VGroup(minis, tag).arrange(DOWN, buff=0.3).move_to([0, -2.2, 0])
            self.play(*appear(*minis, shift=None, lag=0.2), *appear(tag), run_time=1.1)  # early: the tag names the two cards it sits under

            c.wait_until("ritual")
            self.play(later.animate.shift(9.5 * RIGHT), run_time=1.3, rate_func=rush_into)
            self.remove(later)

            chips = [
                _chip([T("pause", 30), pause_icon(0.36, FG)], FG),
                _chip([T("solution", 30)], FG),
                _chip([cross_mark(RED).scale(0.8), T("the tempting mistake", 30, color=RED)], RED),
            ]
            VGroup(*chips).arrange(RIGHT, buff=0.45).move_to([0, CHIP_Y, 0])
            c.wait_until(own_word=chips[0][1][0])
            self.play(*appear(chips[0]), run_time=0.9)
            c.wait_until(own_word=chips[1][1][0])
            self.play(*appear(chips[1]), run_time=0.9)
            c.wait_until("mistake")
            self.play(*appear(chips[2]), run_time=0.9)
            self.chips = chips
        self.play(*disappear(*self.chips), run_time=0.9)
        self.wait(1.0)
