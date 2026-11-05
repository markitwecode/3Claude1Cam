"""Chapter 3, scene 7: the method in four steps; more powerful than row matching; part 1's
7-state machine was already minimal. Clips c3.method.1 – c3.method.4.

Opens and ends on an empty frame.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

L5 = load_scene("ch2_s5_layout")
L6 = load_scene("ch2_s6_outputs")
L7 = load_scene("ch2_s7_columna")
F2 = load_scene("ch3_s2_fill")
OS = load_scene("ch2_s3_onestep")
LEFT7 = load_scene("ch1_s7_left")
CAS = load_scene("ch1_s6_cascade")
MEA = load_scene("ch1_s3_mealy")


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ step cards
CARD_Y = (2.8, 0.95, -0.9, -2.75)
NUM_X, ICON_X, TEXT_X = -6.2, -4.3, -2.5
TXT = 32


def _lines(*ss, t2c=None):
    g = VGroup(*[T(s, TXT, t2c=t2c or {}) for s in ss]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    return g


def _cell(side=0.95):
    return Square(side).set_stroke(FG, 2).set_fill(BG, 0)


def gold_cell(label, side=0.9):
    """ch3 s2's survivor look: GOLD outline, faint GOLD fill, soft glow, its pair inside."""
    sq = Square(side).set_stroke(GOLD, 5).set_fill(GOLD, 0.12)
    glow = Square(side + 0.06).set_stroke(GOLD, 16, opacity=0.25).set_fill(opacity=0)
    t = T(label, 28).move_to(sq)
    return VGroup(glow, sq, t)


# ------------------------------------------------------------------ ch2 s3's two diagrams
def merged_diagram():
    """ch2 s3's row-matching copy: p' and q' one GOLD circle."""
    d = OS.pq_diagram(marks=False)
    mid = (d.pp.get_center() + d.qp.get_center()) / 2
    arcs = [OS._arc(d.p.get_center(), mid), OS._arc(d.q.get_center(), mid)]
    d.pp.move_to(mid)
    d.pp.circle.set_stroke(GOLD, 4)
    d.labels[0].move_to(arcs[0].get_center() + 0.42 * UP + 0.1 * RIGHT)
    d.labels[1].move_to(arcs[1].get_center() + 0.42 * DOWN + 0.1 * RIGHT)
    return VGroup(d.p, d.q, d.pp, *arcs, *d.labels)


def equiv_diagram():
    d = OS.pq_diagram(marks=False)
    return VGroup(*d, d.eq_next)


def _cap(rel):
    m = MathTex(r"\text{%s: }" % ("row matching" if rel == "=" else "equivalence"), "p'",
                rel if rel == "=" else r"\equiv", "q'", font_size=38)
    m[1].set_color(YELLOW)
    m[2].set_color(GOLD)
    m[3].set_color(YELLOW)
    return m


# ------------------------------------------------------------------ part 1's machine, table, staircase
S7 = "ABCDEHJ"
WAVE_J = [f"{c}-J" for c in "ABCDEH"]
WAVE1 = ["A-E", "B-E", "B-H", "C-E", "C-H", "D-E", "E-H"]
WAVE2 = ["A-B", "A-C", "A-D", "A-H", "B-C", "B-D", "C-D", "D-H"]


def seven_table():
    return L5._pair_grid("ABCDEH", "BCDEHJ", lambda c, r: c < r, 0.8, 1.5, 3.0)


ROWS6 = [("A", "A", "C", "0"), ("B", "F", "H", "0"), ("C", "C", "A", "1"),
         ("F", "F", "B", "1"), ("G", "B", "H", "0"), ("H", "C", "G", "1")]


def six_table():
    """p. 150's table after the two merges (D -> A, C -> E), in p150_table's style."""
    keep = L5.P150
    L5.P150 = ROWS6
    try:
        tbl = L5.p150_table()
    finally:
        L5.P150 = keep
    for r, c in ((0, 1), (2, 1), (2, 2)):
        tbl.cell(r, c).set_color(GOLD)
    return tbl


class Method(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------- clip 1: four steps
        with self.say("c3.method.1") as c:
            nums = [T(str(i + 1), 48, YELLOW).move_to(_p(NUM_X, y)) for i, y in enumerate(CARD_Y)]
            self.play(*appear(*nums, lag=0.3), run_time=1.4)

            # step 1: compare every pair (the empty staircase)
            c.wait_until("step1")
            stair = L5.implication_table().squares.copy()
            stair.set_stroke(width=2).scale_to_fit_height(1.4).move_to(_p(ICON_X, CARD_Y[0]))
            t1 = _lines("Compare every pair of states")
            t1.move_to(_p(TEXT_X, CARD_Y[0]), aligned_edge=LEFT)
            self.play(FadeIn(stair, shift=0.2 * DOWN), *appear(t1), run_time=1.2)

            # step 2: cross / implied pairs
            c.wait_until("step2")
            y2 = CARD_Y[1]
            cx = _cell().move_to(_p(ICON_X - 0.6, y2))
            cross = L6.cell_cross(cx)
            cp = _cell().move_to(_p(ICON_X + 0.6, y2))
            pr0 = L7.pair_text("D", "F").move_to(cp.get_center() + 0.2 * UP)
            pr1 = L7.pair_text("C", "H").move_to(cp.get_center() + 0.2 * DOWN)
            t2a = T("Outputs differ: cross the cell.", TXT, t2c={"differ": RED})
            t2b = T("Outputs match: write the implied pairs", TXT, t2c={"match": GREEN})
            VGroup(t2a, t2b).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(_p(TEXT_X, y2), aligned_edge=LEFT)
            self.play(FadeIn(cx), Create(cross), *appear(t2a), run_time=1.4)
            c.wait_until("where they match")
            self.play(FadeIn(cp), *appear(pr0, pr1, t2b, lag=0.3), run_time=1.5)

            # step 3: again and again
            c.wait_until("step3")
            y3 = CARD_Y[2]
            t3 = _lines("Go through again and again,", "crossing every cell with a crossed pair,",
                        "until nothing changes")
            t3.move_to(_p(TEXT_X, y3), aligned_edge=LEFT)
            self.play(*appear(t3[0], t3[1], lag=0.5), run_time=1.6)
            c.wait_until("until")
            counter = F2.pass_counter("+7, +3, +0").scale(1.15).move_to(_p(ICON_X, y3))
            self.play(*appear(t3[2], counter, lag=0.4), run_time=1.2)

            # step 4: merge the survivors
            c.wait_until("step4")
            y4 = CARD_Y[3]
            g1 = gold_cell("A-D").move_to(_p(ICON_X - 0.95, y4))
            g2 = gold_cell("C-E").move_to(_p(ICON_X + 0.05, y4))
            dl = T("D", 44).move_to(_p(ICON_X + 1.05, y4))
            t4 = _lines("Merge the pairs that survive")
            t4.move_to(_p(TEXT_X, y4), aligned_edge=LEFT)
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(dl), *appear(t4), run_time=1.1)
            al = T("A", 44, GOLD).move_to(dl)
            self.play(*swap(dl, al), FlashAround(dl, color=GOLD, time_width=1.5),
                      run_time=min(1.3, c.until(floor=0.6)))

        # ---------------------------------------------------------- clip 2: more powerful
        with self.say("c3.method.2") as c:
            # numbers and icon shapes shrink into a column; the small texts inside the icons go
            shapes = [VGroup(stair), VGroup(cx, cross, cp), VGroup(counter), VGroup(g1[0], g1[1], g2[0], g2[1])]
            moves = []
            for i, (n, g) in enumerate(zip(nums, shapes)):
                y = 2.7 - 1.75 * i
                n.generate_target()
                n.target.scale(0.75).move_to(_p(-6.45, y))
                g.generate_target()
                g.target.scale(32 / 36.8 if i == 2 else 0.55)
                g.target.move_to(_p(-5.0, y))
                moves += [MoveToTarget(n), MoveToTarget(g)]
            gone = [t1, t2a, t2b, t3, t4, pr0, pr1, g1[2], g2[2], al]
            XL, XR = -1.4, 4.3
            h_rm = T("row matching", 40).move_to(_p(XL, 3.3))
            h_it = T("implication table", 40).move_to(_p(XR, 3.3))
            c.wait_until("than row matching")
            self.play(*during(disappear(*gone), 0, 0.4), *during(moves, 0.25, 0.8),
                      *during(appear(h_rm), 0.6, 1.0), run_time=1.8)

            c.wait_until("identical")
            s_rm = T("next states identical", TXT, t2c={"identical": GOLD}).move_to(_p(XL, 2.6))
            dm = merged_diagram().scale(0.75).move_to(_p(XL, 0.45))
            cap_rm = _cap("=").move_to(_p(XL, -1.85))
            self.play(*appear(s_rm), FadeIn(dm), run_time=1.3)
            self.play(*appear(cap_rm), FlashAround(dm[2], color=GOLD, time_width=1.5), run_time=1.2)

            c.wait_until("equivalent")
            s_it = T("next states equivalent", TXT, t2c={"equivalent": GOLD}).move_to(_p(XR, 2.6))
            de = equiv_diagram().scale(0.75).move_to(_p(XR, 0.45))
            cap_eq = _cap("≡").move_to(_p(XR, -1.85))
            self.play(*appear(h_it), run_time=0.9)
            self.play(*appear(s_it), FadeIn(de), run_time=1.2)
            self.play(*appear(cap_eq), FlashAround(de[-1], color=GOLD, time_width=1.5), run_time=1.2)

            c.wait_until("found nothing")
            sc_rm = T("no identical rows: 0 merges", 30, t2c={"0 merges": RED}).move_to(_p(XL, -2.95))
            self.play(*appear(sc_rm), run_time=1.0)
            c.wait_until("while the table")
            sc_it = T("2 merges: A ≡ D, C ≡ E", 30, GOLD).move_to(_p(XR, -2.95))
            self.play(*appear(sc_it), FlashAround(sc_it, color=GOLD, time_width=1.5),
                      run_time=min(1.2, c.until(floor=0.6)))

        # ---------------------------------------------------------- clip 3: part one's promise
        with self.say("c3.method.3") as c:
            d7 = LEFT7.seven_diagram()
            d7.one.set_color(GREEN)
            d7.returns["J"].set_stroke(GREEN)
            d7.returns["J"][1].set_fill(GREEN)
            d7.scale(0.48).move_to(_p(-3.5, 2.0))
            c.wait_until("row matching cut")
            sweep_clear(self, FadeIn(d7), run_time=1.6)

            c.wait_until("seven states")
            tbl = MEA.state_table(CAS.ROWS_FINAL, rules_after=("A", "C", "E"))
            tbl.move_to(_p(-3.45, -1.62))
            self.play(FadeIn(tbl, shift=0.2 * UP), run_time=1.3)

            c.wait_until("crossall")
            it = seven_table()
            self.play(FadeIn(it), run_time=1.2)

            c.wait_until("every single cell")
            j_out = tbl.cell(tbl.row_of("J"), 4)
            crosses = {}

            def wave(pairs, rt, *extra):
                anims = []
                for p in pairs:
                    crosses[p] = L6.cell_cross(it.cells[p])
                    anims.append(Create(crosses[p]))
                self.play(LaggedStart(*anims, lag_ratio=0.25), *extra, run_time=rt)

            wave(WAVE_J, 1.6, FlashAround(j_out, color=GREEN, time_width=1.5),
                 FlashAround(it.row_letter("J"), color=GREEN, time_width=1.5))
            self.wait(0.6)
            wave(WAVE1, 1.4)
            c.wait_until("so no two")
            wave(WAVE2, 1.4)

            c.wait_until("enough")
            # the 7-state machine grows into the space the tables leave (letters 18 -> ~25)
            d7.generate_target()
            d7.target.scale(1.38)
            d7.target.move_to(_p(-6.6, 3.6), aligned_edge=UL)
            cap7 = VGroup(T("already minimal:", 34, GREEN),
                          T("row matching was enough", 34)).arrange(DOWN, buff=0.18)
            cap7.next_to(d7.target, DOWN, buff=0.35)
            self.play(*during(disappear(tbl, it, *crosses.values()), 0, 0.4),
                      *during([MoveToTarget(d7)], 0.3, 0.75),
                      *during(appear(*cap7, lag=0.3), 0.7, 1.0), run_time=2.6)

            c.wait_until("this time")
            t6 = six_table().scale(0.88)
            cap6 = T("needed the implication table", 32, t2c={"implication table": YELLOW})
            x_free = d7.get_right()[0] + 0.45
            w_free = 6.6 - x_free
            if t6.width > w_free:
                t6.scale(w_free / t6.width)
            t6.move_to(_p(x_free + w_free / 2, 1.3))
            cap6.next_to(t6, DOWN, buff=0.35)
            self.play(FadeIn(t6, shift=0.2 * UP), *appear(cap6), run_time=min(1.4, c.until(floor=0.6)))

        # ---------------------------------------------------------- clip 4: have a go
        with self.say("c3.method.4") as c:
            q = VGroup(T("“the best way of … understanding this", 34, slant=ITALIC),
                       T("is just to have a go and do it”", 34, slant=ITALIC)).arrange(DOWN, buff=0.16)
            q.move_to(_p(0, -2.6))
            self.play(*set_alpha([d7, cap7, t6, cap6], 0.45), *appear(q), run_time=1.4)
            c.wait_until("there's an example")
            ex = T("an example in the examples paper", 30, DIM).move_to(_p(0, -3.32))
            self.play(*appear(ex), run_time=1.0)

        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
