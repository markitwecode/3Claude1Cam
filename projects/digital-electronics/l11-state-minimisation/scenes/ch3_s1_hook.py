"""Chapter 3, scene 1: hook: back to the implication table; column A's promises; which can be kept?
Clips c3.hook.1 - c3.hook.2.

Opens on ch2_s8_recap's end_card(); ends on ch2_s7_columna's handover_shot() alone (ch3 s2 opens on it).
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

L6 = load_scene("ch2_s6_outputs")
L7 = load_scene("ch2_s7_columna")
R8 = load_scene("ch2_s8_recap")


def _p(x, y):
    return np.array([x, y, 0.0])


def handover_shot():
    return L7.handover_shot()


LINE_XY = _p(1.35, 2.8)


def promise_line():
    lhs = MathTex("A", r"\equiv", "B", font_size=40)
    lhs[0].set_color(YELLOW)
    lhs[2].set_color(YELLOW)
    c1 = MathTex(r"\text{if }", r"D \equiv F", font_size=40)
    c2 = MathTex(r"\text{and }", r"C \equiv H", font_size=40)
    g = VGroup(lhs, c1, c2).arrange(RIGHT, buff=0.32).move_to(LINE_XY, aligned_edge=LEFT)
    g.lhs, g.c1, g.c2 = lhs, c1, c2
    return g


def staircase(it):
    """The implication table's stepped outline (a flash round its bounding box runs through empty space)."""
    cols, rows = "ABCDEFG", "BCDEFGH"
    pts = [it.cell("A", "B").get_corner(UL)]
    for k, r in enumerate(rows):
        sq = it.cell(cols[k], r)
        pts += [sq.get_corner(UR), sq.get_corner(DR)]
    pts += [it.cell("A", "H").get_corner(DL), pts[0]]
    return VMobject().set_points_as_corners(pts)


def _pulse(cross):
    w0 = cross[0].get_stroke_width()

    def f(m, a):
        m.set_stroke(width=w0 * (1 + 1.4 * np.sin(PI * a)))
    return UpdateFromAlphaFunc(cross, f)


class Hook(NarratedScene):
    def construct(self):
        endc = R8.end_card()
        self.add(endc)
        self.wait(0.7)
        self.clip1(endc)
        self.clip2()
        self.wait(2.6)
        keep = self.shot
        self.play(*disappear(*[m for m in self.mobjects if m is not keep]), run_time=1.0)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)

    # ------------------------------------------------------------ c1: title, the table, crosses, column A
    def clip1(self, endc):
        with self.say("c3.hook.1") as c:
            card = title_card("Part 3 · Solving the implication table")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            nxt = endc.next
            rest = [m for m in endc if m is not nxt]
            # the two-line part line travels to the card's slot and re-wraps there (a cross-fade, no morph)
            self.play(*during([FadeOut(m) for m in rest], 0, 0.45),
                      *during([nxt.animate.scale(36 / 40).move_to(card.part).set_opacity(0)], 0.3, 0.72),
                      *during([FadeIn(card.part, shift=0.15 * UP)], 0.72, 1.0),
                      run_time=1.5)
            self.remove(nxt)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                      FadeIn(card.course, shift=0.25 * DOWN), run_time=1.1)

            # last time: the table and its staircase
            c.wait_until("table")
            shot = handover_shot()
            self.shot = shot
            tbl, it = shot[0][0], shot[0][1]
            self.tbl, self.it = tbl, it
            sweep_clear(self, FadeIn(shot), run_time=1.4)  # early: the home shot, shown whole
            c.wait_until("eight-state machine")
            self.play(FlashAround(tbl.col(0), time_width=1.5), run_time=min(1.6, c.until("with a cell")))
            c.wait_until("every pair")
            self.play(VShowPassingFlash(staircase(it).set_stroke(YELLOW, 5), time_width=0.5),
                      run_time=min(1.8, c.until("crosses")))

            # the 16 crosses pulse once
            c.wait_until("crosses")
            crosses = shot[0][3]
            n = len(crosses)
            self.play(*[a for k, x in enumerate(crosses) for a in during([_pulse(x)], 0.03 * k, 0.03 * k + 0.55)],
                      run_time=min(1.8, c.until("different outputs")))
            assert n == 16

            # column A's three open cells light in turn
            c.wait_until("columna")
            cells = [it.cell("A", r) for r in "BDG"]
            hl = cells[0].copy().set_fill(opacity=0).set_stroke(YELLOW, 5).set_z_index(3)
            self.hl = hl
            step = max(0.6, min(0.9, c.until() / 3.6))
            self.play(FadeIn(hl), *flash([VGroup(shot[1], shot[2])], time_width=1.5), run_time=step)
            for i, r in enumerate("DG", start=1):
                tgt = cells[i].copy().set_fill(opacity=0).set_stroke(YELLOW, 5).set_z_index(3)
                pairs = VGroup(shot[3], shot[4]) if r == "D" else VGroup(shot[5], shot[6])
                self.play(Transform(hl, tgt), *flash([pairs], time_width=1.5), run_time=step)

    # ------------------------------------------------------------ c2: the top promise; which can be kept?
    def clip2(self):
        shot, tbl, it, hl = self.shot, self.tbl, self.it, self.hl
        with self.say("c3.hook.2") as c:
            tgt = it.cell("A", "B").copy().set_fill(opacity=0).set_stroke(YELLOW, 5).set_z_index(3)
            self.play(Transform(hl, tgt), run_time=min(1.0, c.until("state a")))

            line = promise_line()
            c.wait_until("state a")
            self.play(*appear(line.lhs, shift=None), run_time=1.0)
            c.wait_until("if state d")
            self.play(*fly(shot[1], line.c1, arc=-PI / 2), run_time=min(1.5, c.until("and state c")))
            c.wait_until("and state c")
            self.play(*fly(shot[2], line.c2, arc=PI / 3), run_time=min(1.6, c.until("question") - 0.1))
            self.remove(line.lhs, line.c1, line.c2)
            self.add(line)

            # the question
            c.wait_until("question")
            q = T("?", 48, YELLOW).next_to(line, UP, buff=0.12)
            cap = T("which promises\ncan be kept?", 30, line_spacing=0.85).move_to(_p(4.3, 1.95))
            self.play(*appear(q, shift=None), *during(appear(cap), 0.3, 1.0), run_time=1.3)
            c.wait_until("will tell us")

            # the answer: the open cells, and what it will buy
            outlines = [it.cell(*p.split("-")).copy().set_fill(opacity=0).set_stroke(YELLOW, 3, opacity=0.45)
                        .set_z_index(2) for p in L6.OPEN12]
            self.play(*during(disappear(line, q, cap, hl), 0, 0.45),
                      *during(appear(*outlines, lag=0.05, shift=None), 0.4, 1.0),
                      run_time=min(1.8, c.until("two states smaller") - 0.1))
            c.wait_until("two states smaller")
            tag = T("8 states → ?", 32).move_to(_p(tbl.get_x(), -3.35))
            self.play(*appear(tag), run_time=1.0)
