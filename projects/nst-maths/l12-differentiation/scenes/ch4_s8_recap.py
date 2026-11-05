"""Chapter 4, scene 8: recap, next time, end card. Clips c4.recap.1 – c4.recap.2.

A small "Recap" heading, then four panels in a 2x2 grid, built in place one per idea, each the
owner's own visual scaled down with a short line under it:
  r1 s2's chain_card() over power_contrast() (GREEN 6x, RED != (3x^2)^2 = 9x^4);
  r2 s3's board_lines() beside the YELLOW-framed pascal_triangle(3) ("Pascal's triangle" label on
     its word), r2b s4's leibniz_card() under them;
  r3 s5's row_last3() over answer_box(), the three lit entries flashed;
  r4 s7's linked_rows() over s6's dominoes(), fallen.
On {next} the heading goes and the grid shrinks into a dim strip at the top; the "Part 5 · Hermite
polynomials" line, s2's def_line() (ch5's GOLD/PURPLE) at the centre, then on {recursion}
H_{n+1} = 2xH_n - 2nH_{n-1} (ch5 s5's equation) under it with a YELLOW "?". After the clip's last
word the board clears into end_card(), held ~8 s, then fades.

end_card(): ch5's opening card, load_scene("ch5_s1_hook").open_card(), when that exists; else the
stand-in title_card("Part 5 · Hermite polynomials").
"""
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
from lib.titles import title_card  # noqa: E402

PART5 = "Part 5 · Hermite polynomials"

HEAD_Y = 3.25
COL_X = (-3.55, 3.55)
VIS_Y = (1.8, -1.5)     # visual centres, top / bottom row
CAP_DY = -1.6            # caption centre below the visual centre
VIS_W, VIS_H = 6.1, 2.2
CAP_SIZE = 28


def end_card():
    """ch5's opening card when ch5_s1_hook defines open_card(), else the stand-in title card."""
    if (Path(__file__).resolve().parent / "ch5_s1_hook.py").exists():
        mod = load_scene("ch5_s1_hook")
        if hasattr(mod, "open_card"):
            return mod.open_card()
    card = title_card(PART5)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


def slot(i):
    """(visual centre, caption centre) of panel i (0 TL, 1 TR, 2 BL, 3 BR)."""
    x, y = COL_X[i % 2], VIS_Y[i // 2]
    return np.array((x, y, 0.0)), np.array((x, y + CAP_DY, 0.0))


def fit(m, i, w=VIS_W, h=VIS_H):
    c, _ = slot(i)
    m.scale(min(w / m.width, h / m.height)).move_to(c)
    return m


def caption(text, i):
    _, c = slot(i)
    lines = [T(t, CAP_SIZE) for t in text.split("\n")]
    return VGroup(*lines).arrange(DOWN, buff=0.12).move_to(c)


def fallen(dom):
    """s6's dominoes after topple(): each tile tipped by dom.lean about its bottom-right corner."""
    for t in dom.tiles:
        t.rotate(-dom.lean, about_point=t.get_corner(DR))
    return dom


class Recap(NarratedScene):
    def construct(self):
        s2 = load_scene("ch4_s2_higher")
        s3 = load_scene("ch4_s3_pattern")
        s4 = load_scene("ch4_s4_formula")
        s5 = load_scene("ch4_s5_example")
        s6 = load_scene("ch4_s6_proof1")
        s7 = load_scene("ch4_s7_proof2")
        h2 = load_scene("ch5_s2_define")
        h5 = load_scene("ch5_s5_assemble")

        head = T("Recap", 44).move_to([0, HEAD_Y, 0])

        # panel 1: the x^3 chain, and the power that is not the derivative
        card = s2.chain_card()
        pc = s2.power_contrast()
        pc.next_to(card, DOWN, buff=0.45)
        p1 = fit(VGroup(card, pc), 0)
        cap1 = caption("nth derivative: differentiate n times,\nnot a power", 0)

        # panel 2: her three board lines, the framed triangle beside them, the sum card under both
        board = s3.board_lines(gap=0.5)
        tri = s3.pascal_triangle(n_max=3, start=0)
        tframe = SurroundingRectangle(tri, color=YELLOW, buff=0.3, stroke_width=4)
        plabel = T("Pascal's triangle", size=46, color=YELLOW).next_to(tframe, DOWN, buff=0.22)
        tgroup = VGroup(tri, tframe, plabel)
        lcard = s4.leibniz_card(size=44)
        lcard.next_to(board, DOWN, buff=0.35)
        left2 = VGroup(board, lcard)
        tgroup.next_to(left2, RIGHT, buff=0.8)
        p2 = fit(VGroup(left2, tgroup), 1)
        cap2 = caption("Leibniz: coefficients\nfrom Pascal's triangle", 1)

        # panel 3: row ten, last three lit, and the boxed answer
        row = s5.row_last3()
        ans = s5.answer_box()
        ans.next_to(row, DOWN, buff=0.55)
        p3 = fit(VGroup(row, ans), 2)
        cap3 = caption("a polynomial factor\ncuts the sum short", 2)

        # panel 4: the two shifted rows adding up, the dominoes fallen
        rows = s7.linked_rows(heads=False, y3=False)
        dom = fallen(s6.dominoes())
        dom.next_to(rows, RIGHT, buff=1.0)
        p4 = fit(VGroup(rows, dom), 3)
        cap4 = caption("proof: induction\nand Pascal's rule", 3)

        # ---------------------------------------------------------------- c4.recap.1
        with self.say("c4.recap.1") as c:
            self.play(*appear(head), run_time=1.0)
            c.wait_until("r1")
            self.play(*appear(card), run_time=1.2)
            c.wait_until("different")
            self.play(*appear(pc.six, pc.neq, pc.square, lag=0.3), run_time=1.6)
            c.wait_until(own_word=cap1[0])
            self.play(*appear(cap1), run_time=1.0)

            c.wait_until("r2")
            self.play(*appear(board, shift=None), run_time=1.4)
            self.play(*appear(tri, shift=None), GrowFromCenter(tframe), run_time=1.4)
            c.wait_until("r2b")
            self.play(*appear(lcard, cap2, shift=None, lag=0.3), run_time=1.4)
            c.wait_until(own_word=plabel)
            self.play(*appear(plabel), FlashAround(tframe, time_width=1.5), run_time=1.4)

            c.wait_until("r3")
            self.play(*appear(row, ans, lag=0.4), run_time=1.6)
            self.play(*flash(list(row)[-3:]), run_time=1.4)
            c.wait_until("survive")
            self.play(*appear(cap3), run_time=1.0)

            c.wait_until("r4")
            self.play(*appear(rows, dom, cap4, lag=0.35), run_time=1.8)

        # ---------------------------------------------------------------- c4.recap.2
        with self.say("c4.recap.2") as c:
            grid = [card, pc, cap1, board, tri, tframe, plabel, lcard, cap2, row, ans, cap3, rows, dom, cap4]
            about = np.array((0.0, 0.15, 0.0))
            s, shift = 0.3, np.array((0.0, 2.7, 0.0)) - about

            def to_strip(m):
                t = restyle(m, DIMMED).target_mobject
                t.scale(s, about_point=about).shift(shift)
                return Transform(m, t)

            self.play(*during(disappear(head), 0, 0.4), *[to_strip(m) for m in grid], run_time=2.0)

            dl = h2.def_line().scale(1.15).move_to([0, 0.75, 0])
            rec = h5.boxed_recursion()[0].move_to([0, -0.85, 0])
            q = MathTex("?", font_size=60, color=YELLOW).next_to(rec, RIGHT, buff=0.35)
            part = T(PART5, 34, DIM).move_to([0, -2.5, 0])
            c.wait_until("hermeet")
            self.play(*appear(dl, shift=None), run_time=1.5)
            c.wait_until("defined")
            self.play(*appear(part), run_time=1.0)
            c.wait_until("recursion")
            self.play(*appear(rec), run_time=1.5)
            c.wait_until("rule")
            self.play(*appear(q), run_time=1.0)

        ec = end_card()
        sweep_clear(self, time_span(FadeIn(ec), 0.6, 1.4), run_time=1.4)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
