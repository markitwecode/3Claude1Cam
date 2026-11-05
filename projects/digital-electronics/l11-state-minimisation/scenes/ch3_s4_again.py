"""Chapter 3, scene 4: pass 2, pass 3, and the order of the passes. Clips c3.again.1 - c3.again.4.

Opens on ch3_s2_fill's home_shot("pass1") + pass_counter("pass 1: +7") (s3's last frame).
Ends (handover) on home_shot("pass2") at home: see handover_shot().
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

S2 = load_scene("ch3_s2_fill")
home_shot, cross_cell, pointer, pass_counter = S2.home_shot, S2.cross_cell, S2.pointer, S2.pass_counter
PASS1, PASS2 = S2.PASS1, S2.PASS2
WAVES = [["A-B", "B-D", "B-G"], ["A-G", "C-F", "D-G", "E-F", "F-H"], ["C-H", "E-H"], []]
SMALL = 0.68
LEFT_C, RIGHT_C = np.array([-3.5, 0.1, 0]), np.array([3.5, 0.1, 0])


def handover_shot():
    return home_shot("pass2")


def caption(lines):
    t = T(lines, 28, slant=ITALIC, line_spacing=0.8)
    return t.move_to(np.array([3.1 + t.width / 2, 3.0 - t.height / 2, 0]))


def set_arrow(arrow, color, op):
    arrow.set_stroke(color, opacity=op)
    arrow.get_tip().set_fill(color, op).set_stroke(color, opacity=op)
    return arrow


def brighten(arrow, color=YELLOW):
    c0 = ManimColor(arrow.get_stroke_color())
    o0 = arrow.get_stroke_opacity()

    def f(m, a):
        set_arrow(m, interpolate_color(c0, ManimColor(color), a), o0 + (1 - o0) * a)
    return UpdateFromAlphaFunc(arrow, f)


def outline(cell, on=True):
    cell.set_z_index(1)
    return cell.animate.set_stroke(YELLOW if on else FG, 5 if on else 2)


def thick_cross(shot, pair):
    anims = cross_cell(shot, pair, thick=True)
    shot.crosses[pair].set_z_index(2)
    return anims


def gold_glow(cell):
    sq = Square(cell.width + 0.02).move_to(cell).set_stroke(GOLD, 5).set_fill(opacity=0)
    halo = Square(cell.width + 0.08).move_to(cell).set_stroke(GOLD, 14, opacity=0.25).set_fill(opacity=0)
    return VGroup(halo, sq).set_z_index(3)


def split(shot):
    """Take the state table out of the shot: (tbl, staircase-and-everything-else)."""
    tbl = shot.tbl
    shot[0][0].remove(tbl)
    return tbl, shot


class Again(NarratedScene):
    def construct(self):
        self.shot = home_shot("pass1")
        self.counter = pass_counter("pass 1: +7")
        self.add(self.shot, self.counter)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.ending()

    def set_counter(self, text, rt, how="swap"):
        new = pass_counter(text)
        mv = swap if how == "swap" else edit
        self.play(*mv(self.counter, new), run_time=rt)  # early: the pass counter, updated as the passes go
        self.counter = new

    # ------------------------------------------------------------------ pass 1's crosses lean
    def clip1(self):
        shot = self.shot
        cells = shot.it.cells
        with self.say("c3.again.1") as c:
            self.play(*flash([cells[p] for p in PASS1], color=RED, time_width=1.5), run_time=1.6)
            c.wait_until("lean")
            self.play(*[outline(cells[p]) for p in PASS2], run_time=1.0)
            self.arrows = {}
            for pair, (owner, k), col, op, ang in [("B-D", ("A-G", 0), YELLOW, 0.45, -PI / 3),
                                                   ("D-G", ("C-H", 1), YELLOW, 0.45, -PI / 3),
                                                   ("A-G", ("E-H", 0), DIM, 0.6, PI / 4)]:
                arrow, _ = pointer(shot, shot.texts[owner][k], pair, angle=ang)
                self.arrows[owner] = set_arrow(arrow, col, op)
            self.play(*[Create(a) for a in self.arrows.values()], run_time=min(1.5, c.until("again")))
            c.wait_until("again")
            self.set_counter("pass 2", 1.0)
            self.cap = caption("“So, we must go\nthrough again to see\nif the added Xs make\n"
                               "any other pairs\nnon-equivalent”")
            self.play(*appear(self.cap, shift=None), run_time=min(1.2, max(0.3, c.remaining - 0.05)))  # early: the slide's sentence, read as a whole

    # ------------------------------------------------------------------ pass 2
    def clip2(self):
        shot = self.shot
        cells = shot.it.cells
        with self.say("c3.again.2") as c:
            self.play(FlashAround(self.counter, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("B and D")
            self.play(brighten(self.arrows["A-G"]), FlashAround(cells["B-D"], color=YELLOW, time_width=1.5),
                      run_time=1.5)
            c.wait_until("so cross it")
            self.play(*during([outline(cells["A-G"], False), *disappear(self.arrows["A-G"])], 0, 0.5),
                      *during(thick_cross(shot, "A-G"), 0.3, 1.0), run_time=1.5)

            c.wait_until("D and G")
            self.play(brighten(self.arrows["C-H"]), FlashAround(cells["D-G"], color=YELLOW, time_width=1.5),
                      run_time=1.5)
            c.wait_until("also crossed")
            self.play(*during([outline(cells["C-H"], False), *disappear(self.arrows["C-H"])], 0, 0.5),
                      *during(thick_cross(shot, "C-H"), 0.3, 1.0), run_time=min(1.5, c.until("eh")))

            c.wait_until("eh")
            self.play(brighten(self.arrows["E-H"]), run_time=1.2)
            c.wait_until("a moment ago")
            self.play(FlashAround(cells["A-G"], color=RED, time_width=1.5), run_time=1.2)
            c.wait_until("earlier in this pass")
            self.play(*during([outline(cells["E-H"], False), *disappear(self.arrows["E-H"])], 0, 0.5),
                      *during(thick_cross(shot, "E-H"), 0.3, 1.0), run_time=min(1.5, c.until("three")))

            c.wait_until("three")
            new = pass_counter("pass 2: +3")
            self.play(*swap(self.counter, new), run_time=1.0)  # early: the pass counter, updated as the passes go
            self.counter = new
            self.play(*flash([cells[p] for p in PASS2], color=RED, time_width=1.5),
                      run_time=min(1.4, max(0.3, c.remaining - 0.05)))

    # ------------------------------------------------------------------ pass 3: nothing changes
    def clip3(self):
        shot = self.shot
        cells = shot.it.cells
        with self.say("c3.again.3") as c:
            self.play(*disappear(self.cap), run_time=0.8)
            c.wait_until("for pass three")
            self.set_counter("pass 3", 1.0)
            c.wait_until("left")
            self.play(*[outline(cells[p]) for p in ("A-D", "C-E")], run_time=1.2)
            c.wait_until("lean2")
            a1, _ = pointer(shot, shot.texts["A-D"][1], "C-E", angle=-PI / 3)
            a2, _ = pointer(shot, shot.texts["C-E"][1], "A-D", angle=-PI / 3)
            self.loop = [a1, a2]
            self.play(Create(a1), *during([FlashAround(cells["C-E"], color=YELLOW, time_width=1.5)], 0.5, 1),
                      run_time=1.5)
            self.play(Create(a2), *during([FlashAround(cells["A-D"], color=YELLOW, time_width=1.5)], 0.5, 1),
                      run_time=min(1.5, c.until("stop")))
            c.wait_until("stop")
            self.set_counter("pass 3: +0", 1.2)
            self.cap = caption("“No more Xs are\nadded, so all cells\nwith non equivalent\n"
                               "states have now\nbeen Xed out”")
            self.play(*appear(self.cap, shift=None), run_time=1.2)  # early: the slide's bullet, read as a whole

    # ------------------------------------------------------------------ does the order matter?
    def clip4(self):
        cells = self.shot.it.cells
        with self.say("c3.again.4") as c:
            self.play(*disappear(self.counter, *self.loop),
                      *[outline(cells[p], False) for p in ("A-D", "C-E")], run_time=1.0)
            # invisible swap to a clean pass-2 shot, state table split off
            self.remove(*self.mobjects)
            self.tblA, self.A = split(home_shot("pass2"))
            self.add(self.tblA, self.A)
            self.A.save_state()
            ttlA = T("crosses used at once", 30, DIM)
            tallyA = T("+7, +3, +0", 34, GOLD)
            self.play(*during([FadeOut(self.tblA)], 0, 0.45),
                      *during([self.A.animate.scale(SMALL).move_to(LEFT_C)], 0.25, 1.0), run_time=1.8)
            ttlA.move_to([LEFT_C[0], 3.15, 0])
            tallyA.move_to([LEFT_C[0], self.A.get_bottom()[1] - 0.45, 0])
            self.play(*appear(ttlA, tallyA, lag=0.4), run_time=1.0)  # early: the left table's own record
            c.wait_until("Here's an example")

            _, B = split(home_shot("full"))
            B.scale(SMALL).move_to(RIGHT_C)
            self.B = B
            self.play(*during(disappear(self.cap), 0, 0.45), *during([FadeIn(B)], 0.35, 1.0), run_time=1.6)
            ttlB = T("only crosses from earlier passes", 30, YELLOW).move_to([RIGHT_C[0], 3.15, 0])
            c.wait_until(own_word=ttlB)
            self.play(*appear(ttlB), run_time=1.2)
            c.wait_until("waves")

            parts = [T(s, 34, GOLD) for s in ("+3,", "+5,", "+2,", "+0")]
            VGroup(*parts).arrange(RIGHT, buff=0.18).move_to([RIGHT_C[0], tallyA.get_y(), 0])
            for p in parts:
                p.align_to(tallyA, DOWN)
            rt = float(np.clip((c.until("why") - 0.4) / 4 - 0.3, 0.7, 1.2))
            for wave, part in zip(WAVES, parts):
                anims = [a for pair in wave for a in cross_cell(B, pair)]
                self.play(*anims, *appear(part, shift=None), run_time=rt)
                self.wait(0.25)
            c.wait_until("why")

            self.glows = [gold_glow(sh.it.cells[p]) for sh in (self.A, B) for p in ("A-D", "C-E")]
            self.play(*[FadeIn(g) for g in self.glows], run_time=1.5)
            cap = T("the order changes the passes, never the result", 32).move_to([0, -3.35, 0])
            self.play(*appear(cap), run_time=1.2)  # early: the scene's conclusion, said again at its end
            c.wait_until("never the result")
            self.play(FlashUnder(cap, color=GOLD, time_width=1.5), run_time=min(1.5, max(0.3, c.remaining - 0.05)))
            self.cap = cap
            self.extras = [ttlA, tallyA, ttlB, *parts, cap, *self.glows]

    # ------------------------------------------------------------------ back home for s5
    def ending(self):
        self.wait(1.5)
        cross_mobs = [m for m in self.mobjects if m not in (self.A, self.B, *self.extras)]
        # one continuous move: the left staircase starts home while the rest fades, the table
        # follows it in from the left as it clears the space
        self.play(*during([FadeOut(m) for m in [self.B, *self.extras, *cross_mobs]], 0, 0.4),
                  *during([Restore(self.A)], 0.08, 0.75),
                  *during([FadeIn(self.tblA, shift=0.6 * RIGHT)], 0.55, 1.0), run_time=3.0)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)
