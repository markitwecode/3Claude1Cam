"""Chapter 3, scene 6: merge D into A and E into C; p. 155's six-state table; still 3 flip-flops,
but two spare codes become don't cares. Clips c3.merge.1 – c3.merge.3.

Opens on ch3_s2_fill's home_shot("survivors") (ch3 s5's last frame). The merge is ch1 s5/s6's look
(flash GOLD + swap into the match; rows leave and the table closes up; GOLD state counter); the
ladder, brackets and code chips are ch1_s2_why's ladder(), ladder_bracket(), code_chips(); the
finished table is ch4_s1_hook's six_table(). Ends on an empty frame.
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

FILL = load_scene("ch3_s2_fill")
S6 = load_scene("ch1_s6_cascade")
WHY = load_scene("ch1_s2_why")
HOOK = load_scene("ch4_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


K = 1.05                    # the state table grows by this much
TBL_C = _p(-2.1, -0.4)      # ... and sits here
THUMB_K = 0.28              # implication table thumbnail, top right
STATE_X_BESIDE = 1.7        # where a compared row's state letter lands
LIT = 0.25


def _dim_family(mob, keep, k=LIT):
    keep_ids = {id(m) for g in keep for m in g.get_family()}
    for m in mob.family_members_with_points():
        if id(m) in keep_ids:
            continue
        m.set_stroke(opacity=m.get_stroke_opacity() * k)
        m.set_fill(opacity=m.get_fill_opacity() * k)


def row_glow(row, pitch):
    return (Rectangle(width=row.width + 0.4, height=pitch * 0.92).move_to(row)
            .set_stroke(GOLD, 2).set_fill(GOLD, 0.18).set_z_index(-1))


def replace_entries(scene, tbl, items, run_time=1.5):
    """ch1 s6's batched replace_entry, at this table's size: each letter flashes GOLD and swaps."""
    anims, done = [], []
    for r, c, letter in items:
        old = tbl.cell(r, c)
        new = T(letter, 32, GOLD).scale(K).move_to(old)
        anims += [FlashAround(old, color=GOLD, time_width=1.5), *swap(old, new)]
        done.append((r, c, old, new))
    scene.play(*anims, run_time=run_time)
    for r, c, old, new in done:
        row = tbl.rows[r]
        row.remove(old)
        row.cells[c] = new
        row.add(new)
    settle(scene, tbl)
    return [d[3] for d in done]


class Merge(NarratedScene):
    def construct(self):
        shot = FILL.home_shot("survivors")
        self.add(shot)
        tbl = shot.tbl
        shot6 = shot[0][0]
        imp = VGroup(*[m for m in shot6.submobjects if m is not tbl],
                     *shot[0].submobjects[1:], *shot.submobjects[1:])
        self.remove(shot)
        self.add(imp, tbl)          # same picture, now two top-level objects
        self.tbl, self.imp, self.shot = tbl, imp, shot
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(2.5)              # the slide's bullet stays up a moment after the voice
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1: replace D by A, E by C
    def clip1(self):
        tbl, imp, shot = self.tbl, self.imp, self.shot
        with self.say("c3.merge.1") as c:
            lit = [shot.it.cells["A-D"], shot.it.cells["C-E"], *shot.glow.values(),
                   shot.texts["A-D"], shot.texts["C-E"]]
            imp.save_state()
            _dim_family(imp, lit)
            imp.scale(THUMB_K)
            imp.move_to(_p(6.6 - imp.width / 2, 3.65 - imp.height / 2))
            imp.generate_target()
            imp.restore()
            tbl.generate_target()
            tbl.target.scale(K).move_to(TBL_C)
            tbl.pitch *= K
            self.play(*during([MoveToTarget(imp)], 0, 0.6), *during([MoveToTarget(tbl)], 0.3, 1.0),
                      run_time=min(2.2, c.until("We keep")))

            c.wait_until("keep states")
            keep = [tbl.cell(0, 0), tbl.cell(2, 0)]
            self.play(*recolor(keep, GOLD), *flash(keep, color=GOLD, time_width=1.5), run_time=1.2)

            c.wait_until("drop states")
            x0 = tbl.get_right()[0] + 0.45
            self.tags = []
            for r, letter in ((3, "A"), (4, "C")):
                t = T(f"→ {letter}", 32, t2c={letter: GOLD})
                t.move_to(_p(x0 + t.width / 2, tbl.cell(r, 0).get_y()))
                self.tags.append(t)
            self.play(*appear(*self.tags, lag=0.3), run_time=1.2)

            c.wait_until("replace")
            newA = replace_entries(self, tbl, [(0, 1, "A"), (2, 2, "A")], run_time=1.8)
            c.wait_until("row A's entry")
            self.play(FlashAround(newA[0], color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("row C's")
            self.play(FlashAround(newA[1], color=GOLD, time_width=1.5), run_time=1.0)

            c.wait_until("replacee")
            newC = replace_entries(self, tbl, [(2, 1, "C"), (3, 2, "C")], run_time=1.8)
            c.wait_until("row C's", nth=1)
            self.play(FlashAround(newC[0], color=GOLD, time_width=1.5), run_time=1.0)
            c.wait_until("row D's")
            self.play(FlashAround(newC[1], color=GOLD, time_width=1.5), run_time=1.0)

    # ------------------------------------------------------------ c2: rows D, E match A, C; delete
    def slide_beside(self, r_move, r_to, rt):
        tbl = self.tbl
        row = tbl.rows[r_move]
        dx = STATE_X_BESIDE - row.cells[0].get_x()
        c0 = row.get_center()
        c1 = c0 + dx * RIGHT
        c2 = _p(c1[0], tbl.rows[r_to].get_center()[1])
        path = VMobject().set_points_as_corners([c0, c1, c2])
        self.play(MoveAlongPath(row, path), run_time=rt)
        return row

    def clip2(self):
        tbl = self.tbl
        with self.say("c3.merge.2") as c:
            rowD, rowE = tbl.rows[3], tbl.rows[4]
            self.play(*disappear(*self.tags), *flash([rowD, rowE], color=YELLOW, time_width=1.5),
                      run_time=1.3)

            c.wait_until("Row D now")
            self.slide_beside(3, 0, rt=min(2.0, c.until("exactly like row A")))
            c.wait_until("exactly like row A")
            boxes = [row_glow(tbl.rows[0], tbl.pitch), row_glow(rowD, tbl.pitch)]
            self.play(*[FadeIn(b) for b in boxes], run_time=1.0)

            c.wait_until("Row E reads")
            self.slide_beside(4, 2, rt=min(2.0, c.until("exactly like row C")))
            c.wait_until("exactly like row C")
            boxes2 = [row_glow(tbl.rows[2], tbl.pitch), row_glow(rowE, tbl.pitch)]
            self.play(*[FadeIn(b) for b in boxes2], run_time=1.0)

            cap = T("identical rows", 36, GOLD).move_to(_p(3.95, -1.0))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)

            c.wait_until("delete")
            self.play(*set_alpha([rowD, rowE, boxes[1], boxes2[1]], DIMMED), run_time=1.0)

            c.wait_until("we delete")
            p = tbl.pitch
            moves = [rw.animate.shift(2 * p * UP) for rw in tbl.rows[5:]]
            for sep in tbl.seps:
                moves.append(Transform(sep, Line(sep.get_start(), sep.get_end() + 2 * p * UP).set_stroke(DIM, 2)))
            cnt = S6.counter(8, 6)
            cnt.move_to(_p(6.55 - cnt.width / 2, -3.05))
            self.cnt = cnt
            self.play(*during(disappear(rowD, rowE, *boxes, *boxes2, cap), 0, 0.4),
                      *during(moves, 0.45, 1.0), *during(appear(cnt), 0.5, 1.0),
                      run_time=min(1.8, c.until(floor=1.2)))
            for rw in (rowD, rowE):
                tbl.rows.remove(rw)
                tbl.remove(rw)
            settle(self, tbl)

    # ------------------------------------------------------------ c3: six states, still 3 FFs
    def clip3(self):
        tbl, imp = self.tbl, self.imp
        with self.say("c3.merge.3") as c:
            six = HOOK.six_table()
            anims = []
            for r in range(6):
                for col in range(4):
                    anims.append(Transform(tbl.rows[r].cells[col], six.rows[r].cells[col]))
            anims += [Transform(tbl.h_ps, six.head[0]), Transform(tbl.h_ns, six.head[1]),
                      Transform(tbl.subs[0], six.subs[0]), Transform(tbl.subs[1], six.subs[1]),
                      Transform(tbl.rules[0], six.rules[0]),
                      Transform(tbl.seps[0], six.seps[0]), Transform(tbl.seps[1], six.seps[1])]
            self.play(*anims, *swap(tbl.h_out, six.head[2]), *during(disappear(imp), 0, 0.5),
                      run_time=min(2.0, c.until("ladder")))
            self.remove(*tbl.get_family(), six.head[2])
            self.add(six)

            c.wait_until("ladder")
            lad = WHY.ladder()
            lad.move_to(ORIGIN)
            b8 = WHY.ladder_bracket(lad, 2, 8)
            b6 = WHY.ladder_bracket(lad, 2, 6, x=b8.get_right()[0] + 0.45)
            st3 = T("still 3", 32, YELLOW).next_to(b6.formula, DOWN, buff=0.2).align_to(b6.formula, LEFT)
            whole = VGroup(lad, b8, b6, st3)
            d = _p(0, -0.1) - whole.get_center()
            for m in (lad, b8, b6, st3):
                m.shift(d)
            c.wait_until("save a flip-flop")
            sweep_clear(self, FadeIn(lad), keep=[], run_time=min(1.6, c.until("no", floor=1.0)))   # early: the ladder returns whole, as in ch1 s2

            c.wait_until("no")
            self.play(GrowFromCenter(b8.brace), *during(appear(b8.tag, b8.formula, lag=0.3), 0.25, 1),
                      run_time=1.5)
            c.wait_until("so do six")
            self.play(GrowFromCenter(b6.brace), *during(appear(b6.tag, b6.formula, lag=0.3), 0.25, 1),
                      run_time=1.5)
            c.wait_until("so no")
            self.play(*appear(st3), run_time=0.9)

            c.wait_until("spare")
            grid = WHY.code_chips(unused=(), crossed=False)
            grid.move_to(_p(-1.9, -1.25))
            gone = [m for i, r in enumerate(lad.rows) for m in r if not (i == 2 and m is lad.pats[2])]
            dv = _p(grid.get_right()[0] + 0.45 - b8.brace.get_left()[0], grid.get_y() - b8.brace.get_y())
            src = lad.pats[2]
            src.generate_target()
            src.target.scale(1.3).move_to(grid)
            self.play(*during(disappear(*gone), 0, 0.35), *during([MoveToTarget(src)], 0.15, 0.55),
                      *during(swap(src, grid), 0.55, 1),
                      *during([m.animate.shift(dv) for m in (b8, b6, st3)], 0.35, 0.85), run_time=2.2)
            self.remove(*lad.get_family())
            c.wait_until("now unused")
            dead = [grid.chips[6], grid.chips[7]]
            self.play(*[ch.box.animate.set_stroke(DIM, 2) for ch in dead],
                      *[ch.txt.animate.set_color(DIM) for ch in dead], run_time=1.2)
            c.wait_until("don't cares")
            crosses = [WHY.chip_cross(ch) for ch in dead]
            dc = T("don’t care", 36, GOLD).next_to(VGroup(*dead), DOWN, buff=0.35)
            self.play(*appear(*crosses, shift=0.15 * DOWN, lag=0.2), *during(appear(dc), 0.4, 1), run_time=1.4)

            c.wait_until("may")
            b2 = VGroup(*[T(s, 30) for s in WHY.BULLET2]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
            dot = T("•", 30).next_to(b2[0], LEFT, buff=0.2)
            b2.add(dot)
            b2.move_to(_p(0, 1.75))
            self.play(*appear(*b2[:4], dot, lag=0.15), run_time=1.5)   # early: p. 144's bullet shown whole, then its two mays

            may0 = select(b2[0], "may")[0]
            may1 = select(b2[1], "may")[0]
            nh = T("not here", 28, RED).next_to(may0, UP, buff=0.14)
            c.wait_until("Here the count")
            self.play(*appear(nh), run_time=1.0)
            c.wait_until("may still")
            self.play(*recolor(may1, YELLOW), FlashAround(may1, color=YELLOW, time_width=1.5),
                      run_time=min(1.2, c.until(floor=0.8)))
