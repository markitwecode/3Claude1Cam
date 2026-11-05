"""Chapter 8, scene 1: spoiler warning, the seven question cards and their Part tags. Clips c8.intro.1 – c8.intro.2.

Shared pieces for s2–s7 (import with load_scene("ch8_s1_intro")):
  card_row(lit=True)  VGroup of the seven small cards (F15 F16 F17 F12 F13 F18 F19), each a VGroup
                      with .box .label .icon .tag .qid; row centred at x 0, box centres y = ROW_Y.
  question_card(label, text_lines, size=36, width=None)  the enlarged question card, centred at ORIGIN.
  pause_icon(height=0.6, color=YELLOW)  the ‖ icon (two rounded bars).
  ritual_steps()      the "read → pause ‖ → work it out → compare" strip under the row (y = RITUAL_Y).
  handover_shot()     card_row() + ritual_steps(): this scene's last frame.
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
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

CARD_W, CARD_H = 1.7, 2.6
CARD_GAP = 0.18
ROW_Y = 0.9
RITUAL_Y = -2.5
UNLIT = 0.25

QUESTIONS = [("F15", "Part 1"), ("F16", "Part 1"), ("F17", "Parts 2–3"), ("F12", "Parts 2–3"),
             ("F13", "Parts 2–3"), ("F18", "Part 4"), ("F19", "Part 6")]


# ------------------------------------------------------------------ mini icons
def icon_ring():
    """ch1's ring of five: dashed GOLD circle, one GREEN root, the rest TEAL."""
    r = 0.4
    circ = DashedVMobject(Circle(radius=r, color=GOLD, stroke_width=2), num_dashes=20)
    dots = [Dot(r * np.array([np.cos(a), np.sin(a), 0]), radius=0.075,
                color=GREEN if k == 0 else TEAL)
            for k, a in enumerate(PI / 10 + 2 * PI * k / 5 for k in range(5))]
    return VGroup(circ, *dots)


def icon_chain():
    """ch3's tip-to-tail GOLD arrows, each turned a little further."""
    pts = [ORIGIN]
    for k in range(3):
        a = k * 0.6
        pts.append(pts[-1] + 0.42 * np.array([np.cos(a), np.sin(a), 0]))
    arrows = [Arrow(pts[k], pts[k + 1], buff=0, stroke_width=3.5, color=GOLD, tip_length=0.13,
                    max_tip_length_to_length_ratio=0.4) for k in range(3)]
    g = VGroup(*arrows)
    return g.move_to(ORIGIN)


def icon_ladder():
    """ch4's ladder: GOLD dashed line, TEAL rungs, one GREEN."""
    line = DashedLine(0.45 * DOWN, 0.45 * UP, dash_length=0.07, dashed_ratio=0.55, color=GOLD,
                      stroke_width=2)
    dots = [Dot([0, y, 0], radius=0.07, color=GREEN if k == 1 else TEAL)
            for k, y in enumerate((-0.33, -0.11, 0.11, 0.33))]
    return VGroup(line, *dots)


def icon_phasor():
    """ch6's GOLD arrow on its circle, with the dashed drop and the BLUE shadow dot."""
    r, a = 0.4, 0.9
    circ = Circle(radius=r, color=DIM, stroke_width=1.5)
    axis = Line(0.52 * LEFT, 0.52 * RIGHT, color=DIM, stroke_width=1.5)
    tip = r * np.array([np.cos(a), np.sin(a), 0])
    arr = Arrow(ORIGIN, tip, buff=0, stroke_width=3.5, color=GOLD, tip_length=0.13,
                max_tip_length_to_length_ratio=0.4)
    foot = np.array([tip[0], 0, 0])
    drop = DashedLine(tip, foot, color=DIM, stroke_width=1.5, dash_length=0.05)
    dot = Dot(foot, radius=0.065, color=BLUE)
    return VGroup(circ, axis, drop, arr, dot)


ICONS = {"Part 1": icon_ring, "Parts 2–3": icon_chain, "Part 4": icon_ladder, "Part 6": icon_phasor}


def _alpha(mob, op):
    for m in mob.family_members_with_points():
        if m.get_fill_opacity() > 0:
            m.set_fill(opacity=op)
        if m.get_stroke_width() > 0:
            m.set_stroke(opacity=op)
    return mob


# ------------------------------------------------------------------ shared pieces
def pause_icon(height=0.6, color=YELLOW):
    w = 0.3 * height
    bars = [RoundedRectangle(corner_radius=0.3 * w, width=w, height=height, stroke_width=0)
            .set_fill(color, 1) for _ in range(2)]
    return VGroup(*bars).arrange(RIGHT, buff=0.35 * height)


def small_card(qid, part, lit=True):
    box = RoundedRectangle(corner_radius=0.15, width=CARD_W, height=CARD_H,
                           stroke_color=BLUE if lit else DIM, stroke_width=3).set_fill(opacity=0)
    label = T(qid, size=46).move_to(box.get_top() + 0.6 * DOWN)
    icon = ICONS[part]().scale(1.35)
    icon.move_to(box.get_center() + 0.35 * DOWN)
    if not lit:
        _alpha(icon, UNLIT)
    tag = T(part, size=28, color=FG if lit else DIM).next_to(box, DOWN, buff=0.2)
    g = VGroup(box, label, icon, tag)
    g.box, g.label, g.icon, g.tag, g.qid = box, label, icon, tag, qid
    return g


def card_row(lit=True):
    """The seven cards in s1's final state (lit=True): BLUE boxes, FG tags, full-colour icons."""
    cards = [small_card(q, p, lit) for q, p in QUESTIONS]
    pitch = CARD_W + CARD_GAP
    for i, cd in enumerate(cards):
        cd.shift(np.array([(i - 3) * pitch, ROW_Y, 0]) - cd.box.get_center())
    row = VGroup(*cards)
    row.cards = cards
    return row


def question_card(label, text_lines, size=36, width=None):
    """The enlarged question card: BLUE rounded box centred at ORIGIN, the label (T 52, YELLOW) top
    left, the ‖ icon top right, the question below (str lines become T(size); Mobjects used as is),
    left-aligned. Parts: .box .label .icon .body."""
    lines = [T(s, size=size) if isinstance(s, str) else s for s in text_lines]
    body = VGroup(*lines).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
    lab = T(label, size=52, color=YELLOW)
    icon = pause_icon(0.6)
    w = width or max(10.0, body.width + 1.4, lab.width + icon.width + 2.0)
    h = lab.height + body.height + 1.6
    box = RoundedRectangle(corner_radius=0.25, width=w, height=h, stroke_color=BLUE,
                           stroke_width=4).set_fill(BG, 1)
    lab.move_to(box.get_corner(UL) + np.array([0.6 + lab.width / 2, -0.5 - lab.height / 2, 0]))
    icon.move_to(box.get_corner(UR) + np.array([-0.6 - icon.width / 2, 0, 0])).set_y(lab.get_y())
    body.next_to(lab, DOWN, buff=0.45).align_to(lab, LEFT)
    g = VGroup(box, lab, icon, body)
    g.box, g.label, g.icon, g.body = box, lab, icon, body
    return g


def ritual_steps():
    """read → pause ‖ → work it out → compare, under the row. Parts: .steps (4) .arrows (3)."""
    read = T("read", size=38)
    pause = VGroup(T("pause", size=38), pause_icon(0.36)).arrange(RIGHT, buff=0.2)
    solve = T("work it out", size=38)
    comp = T("compare", size=38)
    steps = [read, pause, solve, comp]
    VGroup(*steps).arrange(RIGHT, buff=1.2)
    xh = 0.0095 * 38 * 0.68   # x-height: align every word on the tops of its first (x-height) letter
    for s in steps:
        first = s[0][0] if s is pause else s[0]
        s.shift((RITUAL_Y + xh / 2 - first.get_top()[1]) * UP)
    pause[1].set_y(RITUAL_Y)
    arrows = [Arrow([steps[k].get_right()[0], RITUAL_Y, 0], [steps[k + 1].get_left()[0], RITUAL_Y, 0], buff=0.22, stroke_width=3,
                    color=DIM, tip_length=0.16, max_tip_length_to_length_ratio=0.3)
              for k in range(3)]
    for a in arrows:
        a.set_y(RITUAL_Y)
    g = VGroup(*steps, *arrows)
    g.steps, g.arrows = steps, arrows
    return g


def handover_shot():
    return VGroup(card_row(lit=True), ritual_steps())


def spoiler_banner():
    icon = pause_icon(1.3)
    word = T("SPOILERS AHEAD", size=64, color=YELLOW, weight=BOLD)
    inner = VGroup(icon, word).arrange(RIGHT, buff=0.7)
    frame = RoundedRectangle(corner_radius=0.3, width=inner.width + 1.4, height=inner.height + 1.0,
                             stroke_color=YELLOW, stroke_width=4).set_fill(opacity=0)
    g = VGroup(frame, inner).move_to(0.2 * UP)
    g.icon, g.word, g.frame = icon, word, frame
    return g


class Ch8S1Intro(NarratedScene):
    def construct(self):
        # ------------------------------------------------ clip 1: title and spoiler warning
        with self.say("c8.intro.1") as c:
            card = title_card("Part 8 · Solutions (bonus)")
            card.title.scale_to_fit_width(12.4)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      run_time=1.0)
            self.play(*appear(card.course, card.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("warn")

            banner = spoiler_banner()
            self.play(*disappear(card.title, card.rule, card.course, card.part, lag=0.1), run_time=1.0)
            self.play(FadeIn(banner.icon, scale=0.8), FadeIn(banner.frame),
                      *appear(banner.word, shift=None), run_time=1.0)  # early: the banner is the warning itself
            c.wait_until("pause now")
            self.play(FlashAround(banner.icon, color=YELLOW, run_time=1.5, time_width=1.5))
            c.wait_until()

        # ------------------------------------------------ clip 2: the cards and their tags
        with self.say("c8.intro.2", gap=0.35) as c:
            self.play(*disappear(banner), run_time=0.7)
            row = card_row(lit=False)
            lit = card_row(lit=True)
            self.play(*appear(*row.cards, lag=0.12), run_time=1.6)  # early: the row is shown whole, then walked
            c.wait_until("roots")

            def light(idx, cue):
                anims = []
                for i in idx:
                    cd, lc = row.cards[i], lit.cards[i]
                    anims += [cd.box.animate.set_stroke(BLUE),
                              cd.tag.animate.set_color(FG),
                              FadeOut(cd.icon), FadeIn(lc.icon),
                              FlashAround(cd.tag, color=YELLOW, time_width=1.5)]
                self.play(*anims, run_time=min(1.5, c.until(cue)))

            light([0, 1], "sums")
            c.wait_until("sums")
            light([2, 3, 4], "logs")
            c.wait_until("logs")
            light([5], "osc")
            c.wait_until("osc")
            light([6], "ritual")
            c.wait_until("ritual")

            rit = ritual_steps()
            for k, step in enumerate(rit.steps):
                word = step if k != 1 else step[0]
                c.wait_until(own_word=word)
                extra = [GrowArrow(rit.arrows[k - 1])] if k > 0 else []
                self.play(*appear(step, shift=0.15 * DOWN), *extra, run_time=0.6)
            c.wait_until()

        # end on the handover shot (exactly what handover_shot() draws)
        self.clear()
        self.add(handover_shot())
        self.wait(1.0)
