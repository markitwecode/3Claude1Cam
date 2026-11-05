"""Chapter 3, scene 8: recap of the implication table, then on to chip ch4. Clips c3.recap.1 – c3.recap.3.

Six thumbnails in a 3 x 2 grid, each built from the scene that taught it:
r1 ch3_s2_fill home_shot("full"); r2 the same + s2's pointer A-B "D-F" -> D-F and cross_cell(A-B);
r3 home_shot("pass1") + pass_counter steps and the thick pass-2 crosses; r4 home_shot("survivors")
+ the pointer loop; r5 ch4_s1_hook six_table() + ch1_s2_why ladder rung 3 with ladder_bracket 6;
r6 ch3_s7_method merged_diagram() / equiv_diagram(). Ends on ch4_s1_hook open_card(), held ~8 s,
then fades (chapter end, no handover).
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

F2 = load_scene("ch3_s2_fill")
HOOK = load_scene("ch4_s1_hook")
WHY = load_scene("ch1_s2_why")
MET = load_scene("ch3_s7_method")


def _p(x, y):
    return np.array([x, y, 0.0])


COL_X = (-4.7, 0.0, 4.7)
ROW_TOP = (2.7, -0.6)       # top of each row's picture
PIC_H = 2.12                  # picture height
CAP_Y = (0.15, -3.15)           # caption centres
STROKE_K = 0.6                # thumbnails: strokes thinned by this much


def _thin(mob, k=STROKE_K):
    for m in mob.get_family():
        if not m.has_points():          # a VGroup's own default width 4 would reach its texts
            continue
        w = m.get_stroke_width()
        if w and w > 3:
            m.set_stroke(width=w * k, family=False)
    return mob


def imp_thumb(stage, extra_fn=None, h=PIC_H):
    """The implication table at home without its state table, scaled into a panel."""
    s = F2.home_shot(stage)
    s[0][0].remove(s.tbl)
    extra = extra_fn(s) if extra_fn else []
    g = VGroup(s, *extra)
    g.scale(h / s.height)
    _thin(g)
    s.extra = extra
    s.k = h / 6.82
    return s


def place(mob, col, row):
    g = VGroup(mob, *getattr(mob, "extra", []))
    g.shift(_p(COL_X[col], ROW_TOP[row] - mob.height / 2) - mob.get_center())
    return mob


def caption(text, col, row, t2c=None):
    t = T(text, 28, t2c=t2c or {}, line_spacing=0.8)
    return t.move_to(_p(COL_X[col], CAP_Y[row]))


def _arrow_create(arrow, cell, color=YELLOW):
    return [Create(arrow), *during([FlashAround(cell, color=color, time_width=1.5, stroke_width=3)], 0.55, 1.0)]


def _counter(text, x_left, y):
    t = F2.pass_counter(text).scale(0.85)
    return t.move_to(_p(x_left + t.width / 2, y))


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ r1 – r3
    def clip1(self):
        with self.say("c3.recap.1") as c:
            head = T("Recap", 48).move_to(_p(0, 3.25))
            self.play(*appear(head), run_time=1.0)  # early: the heading
            self.head = head

            # r1: the filled table
            c.wait_until("r1")
            s1 = place(imp_thumb("full"), 0, 0)
            self.play(FadeIn(s1), run_time=1.2)
            c.wait_until("holds a promise")
            cap1 = caption("matching outputs:\nwrite the promises", 0, 0, t2c={"matching": GREEN})
            self.play(*appear(cap1, shift=None), run_time=1.0)  # early: the panel's summary line, paraphrasing this sentence

            # r2: a promise that leans on a crossed cell
            c.wait_until("r2")
            s2 = imp_thumb("full", lambda s: [F2.pointer(s, s.texts["A-B"][0], "D-F", angle=-PI / 4)[0]])
            place(s2, 1, 0)
            arrow = s2.extra[0]
            self.play(FadeIn(s2), run_time=1.0)
            c.wait_until("leans on")
            self.play(*_arrow_create(arrow, s2.it.cells["D-F"]), run_time=1.5)
            c.wait_until("gets crossed")
            anims = F2.cross_cell(s2, "A-B")
            s2.crosses["A-B"].set_stroke(width=F2.THIN * STROKE_K)
            self.play(*anims, run_time=1.0)
            cap2 = caption("a broken promise:\ncross the cell", 1, 0, t2c={"cross": RED})
            self.play(*appear(cap2, shift=None), run_time=min(1.0, c.until("r3")))

            # r3: again and again
            c.wait_until("r3")
            s3 = imp_thumb("pass1", h=2.1)
            place(s3, 2, 0).shift(1.05 * LEFT)
            ctr = _counter("+7", s3.get_right()[0] + 0.15, s3.get_y())
            self.play(FadeIn(s3), *appear(ctr), run_time=1.0)  # early: the pass counter
            c.wait_until("break more")
            new = _counter("+7, +3", ctr.get_left()[0], ctr.get_y())
            thick = []
            for p in F2.PASS2:
                thick += F2.cross_cell(s3, p, thick=True)
                s3.crosses[p].set_stroke(width=F2.THICK * STROKE_K).set_z_index(2)
            self.play(*edit(ctr, new), *thick, run_time=1.4)  # early: the pass counter, updated
            ctr = new
            c.wait_until("until a pass")
            new = _counter("+7, +3, +0", ctr.get_left()[0], ctr.get_y())
            self.play(*edit(ctr, new), run_time=1.0)  # early: the pass counter, updated
            ctr = new
            cap3 = caption("again, until\nnothing changes", 2, 0)
            self.play(*appear(cap3, shift=None), run_time=min(1.0, c.until(floor=0.5)))

    # ------------------------------------------------------------------ r4 – r6
    def clip2(self):
        with self.say("c3.recap.2", gap=2.0) as c:
            # r4: the survivors and their loop of promises
            def loop(s):
                return [F2.pointer(s, s.texts["A-D"][1], "C-E")[0],
                        F2.pointer(s, s.texts["C-E"][1], "A-D")[0]]
            s4 = place(imp_thumb("survivors", loop), 0, 1)
            a1, a2 = s4.extra
            self.play(FadeIn(s4), run_time=1.0)
            c.wait_until("survive")
            self.play(*_arrow_create(a1, s4.it.cells["C-E"]), run_time=1.2)
            self.play(*_arrow_create(a2, s4.it.cells["A-D"]), run_time=1.2)
            c.wait_until("state A with")
            cap4 = caption("the survivors:\nA ≡ D, C ≡ E", 0, 1, t2c={"A ≡ D, C ≡ E": GOLD})
            self.play(*appear(cap4, shift=None), run_time=1.0)

            # r5: six states, still three flip-flops
            c.wait_until("r5")
            six = HOOK.six_table()
            six.scale_to_fit_height(1.4).move_to(_p(COL_X[1], ROW_TOP[1] + 0.15 - 0.7))
            self.six = six
            self.play(FadeIn(six), run_time=1.2)
            c.wait_until("still three")
            lad = WHY.ladder()
            rung = lad.rows[2]
            lab, cnt, pat = lad.labs[2], lad.counts[2], lad.pats[2]
            VGroup(lab, cnt).arrange(RIGHT, buff=0.15).next_to(pat, LEFT, buff=0.3)
            br = WHY.ladder_bracket(lad, 2, 6)
            new_brace = Brace(pat, direction=RIGHT, buff=0.08, color=GOLD)
            br.remove(br.brace)
            br.brace = new_brace
            br.add(new_brace)
            VGroup(br.tag, br.formula).next_to(new_brace, RIGHT, buff=0.12)
            rg = VGroup(rung, br)
            cap5 = caption("6 states,\nstill 3 flip-flops", 1, 1, t2c={"6 states,": GOLD})
            room = six.get_bottom()[1] - 0.15 - (cap5.get_top()[1] + 0.15)
            rg.scale_to_fit_width(3.8)
            if rg.height > room:
                rg.scale_to_fit_height(room)
            rg.move_to(_p(COL_X[1], six.get_bottom()[1] - 0.15 - rg.height / 2))
            self.play(FadeIn(rung), GrowFromCenter(br.brace),
                      *during(appear(br.tag, br.formula, lag=0.3, shift=None), 0.3, 1.0), run_time=1.5)
            self.play(*appear(cap5, shift=None), run_time=1.0)

            # r6: equivalent, not just identical
            c.wait_until("row matching")
            xl, xr = COL_X[2] - 1.15, COL_X[2] + 1.15
            top = ROW_TOP[1]
            h_rm = T("row\nmatching", 28, DIM, line_spacing=0.8)
            h_it = T("implication\ntable", 28, DIM, line_spacing=0.8)
            h_rm.move_to(_p(xl, top - h_rm.height / 2))
            h_it.move_to(_p(xr, top - h_it.height / 2))
            dm = MET.merged_diagram().scale_to_fit_height(1.0)
            de = MET.equiv_diagram().scale_to_fit_height(1.0)
            dm.next_to(h_rm, DOWN, buff=0.1).set_x(xl)
            de.next_to(h_it, DOWN, buff=0.1).set_x(xr)
            de.align_to(dm, UP)
            w_id = T("identical", 28, GOLD).next_to(dm, DOWN, buff=0.1)
            w_eq = T("equivalent", 28, GOLD).next_to(de, DOWN, buff=0.1)
            w_eq.align_to(w_id, DOWN)
            cap6 = caption("equivalent,\nnot just identical", 2, 1, t2c={"equivalent,": GOLD})
            r6 = VGroup(h_rm, h_it, dm, de, w_id, w_eq)
            room = top - (cap6.get_top()[1] + 0.15)
            if r6.height > room:
                r6.scale(room / r6.height, about_point=_p(COL_X[2], top))
            self.play(*appear(h_rm, h_it, lag=0.3), FadeIn(dm), FadeIn(de), run_time=1.2)  # early: the two column heads
            self.play(*appear(w_id, shift=None), run_time=0.9)  # early: row matching's word, shown with its column
            c.wait_until("equivalent")
            self.play(*appear(w_eq, shift=None), *during(appear(cap6, shift=None), 0.2, 0.9), run_time=1.3)

    # ------------------------------------------------------------------ next: onto a chip
    def clip3(self):
        card = HOOK.open_card()
        six = self.six
        with self.say("c3.recap.3") as c:
            c.wait_until("how to build")    # r6's takeaway stays up until here
            sweep_clear(self, keep=[six], run_time=0.9)
            k = card.table.height / six.height
            self.play(*during([six.animate.scale(k).move_to(card.table)], 0, 0.75),
                      *during([FadeIn(card.chip, scale=1.08)], 0.45, 1.0),
                      run_time=min(1.6, c.until("chip", floor=1.2)))
            self.remove(six)
            self.add(card.table)
            self.play(*appear(card.part), run_time=0.8)
            c.wait_until("chip")
            self.play(*appear(card.cap), run_time=min(1.0, c.until(floor=0.6)))
