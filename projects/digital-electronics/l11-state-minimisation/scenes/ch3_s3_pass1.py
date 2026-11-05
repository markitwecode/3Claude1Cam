"""Chapter 3, scene 3: the first pass through the implication table (p. 152 -> p. 154). Clips c3.pass.1 - c3.pass.5.

Opens on ch3_s2_fill's handover_shot() (= home_shot("full")). Every check uses s2's pointer(),
cross_cell() and pass_counter(). Ends on home_shot("pass1") + pass_counter("pass 1: +7") (handover to s4).
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
L5 = load_scene("ch2_s5_layout")
L6 = load_scene("ch2_s6_outputs")
pointer, cross_cell, pass_counter, home_shot = S2.pointer, S2.cross_cell, S2.pass_counter, S2.home_shot
_outline, _out_boxes, _texts_of = S2._outline, S2._out_boxes, S2._texts_of


def _p(x, y):
    return np.array([x, y, 0.0])


def handover_shot():
    shot = home_shot("pass1")
    return VGroup(shot, pass_counter("pass 1: +7"))


CAP_XY = _p(4.85, 1.8)


def rule_card():
    lines = VGroup(T("If one of the pairs", 30),
                   T("in say cell i-j", 30, t2s={"i-j": ITALIC}),
                   T("is not equivalent,", 30),
                   VGroup(T("then", 30), MathTex(r"i \not\equiv j", font_size=36)).arrange(RIGHT, buff=0.18))
    return lines.arrange(DOWN, buff=0.2).move_to(CAP_XY)


def qmark(cell, texts=()):
    """An open cell, checked: a faint YELLOW tint and a "?" fully inside the cell.
    A cell with a free half (one pair) gets a bold "?" there; a full cell (two pairs) a large
    faint "?" behind its pairs, clear of the borders."""
    tint = Square(cell.side_length).move_to(cell).set_stroke(width=0).set_fill(YELLOW, 0.14).set_z_index(-1)
    side = cell.side_length
    if len(texts) == 1:
        t = texts[0]
        half = UP if t.get_center()[1] < cell.get_center()[1] else DOWN
        q = set_backstroke(T("?", 36, YELLOW, weight=BOLD), width=6)
        q.move_to(cell.get_center() + half * side / 4).set_z_index(3)
    else:
        # a drawn backdrop, not a label: a plain shape cut from the glyph, behind the pairs
        glyph = T("?", 40, YELLOW, weight=BOLD)
        q = VMobject().set_points(glyph[0].points).set_stroke(width=0).set_fill(YELLOW, 0.3)
        q.scale_to_fit_height(0.76 * side).move_to(cell).set_z_index(-1)
    return VGroup(tint, q)


def _pulse_cross(cr, peak=6):
    def f(m, a):
        m.set_stroke(width=S2.THIN + peak * np.sin(PI * a))
    return UpdateFromAlphaFunc(cr, f)


def inset_picture():
    """p. 154's slide, small: the staircase with its 23 crosses, frame and page label."""
    it = L5.implication_table()
    sq = it.squares
    crosses = VGroup(*[L6.cell_cross(it.cells[p]).set_stroke(width=3) for p in L6.CROSSED + S2.PASS1])
    pic = VGroup(sq.copy(), crosses)
    for m in pic[0]:
        m.set_stroke(FG, 1.5)
    bd_i = it.pairs.index("B-D")
    pic.scale(0.36).move_to(_p(5.25, 1.1))
    ring = SurroundingRectangle(pic[0][bd_i], color=YELLOW, buff=0.04).set_stroke(YELLOW, 4)
    frame = RoundedRectangle(corner_radius=0.12, width=pic.width + 0.3, height=pic.height + 0.3)
    frame.move_to(pic).set_stroke(DIM, 2)
    label = T("p. 154", 28, DIM)
    label.move_to(frame.get_corner(UR) + _p(-label.width / 2 - 0.2, -0.32))
    g = VGroup(frame, pic, label)
    g.frame, g.pic, g.label, g.ring = frame, pic, label, ring
    return g


class Pass1(NarratedScene):
    def construct(self):
        shot = S2.handover_shot()
        self.add(shot)
        self.shot, self.it, self.tbl = shot, shot.it, shot.tbl
        self.cur = None          # the outlined cell
        self.qs = {}             # "?" marks by cell
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()

    # ------------------------------------------------------------------ helpers
    def pair(self, cell, i):
        return self.shot.texts[cell][i]

    def go(self, key, rt, extra=()):
        """Move the YELLOW outline to cell `key`."""
        anims = list(extra)
        if self.cur is not None:
            anims += during([_outline(self.it.cells[self.cur], False)], 0, 0.6)
            anims += during([_outline(self.it.cells[key])], 0.4, 1.0)
        else:
            anims.append(_outline(self.it.cells[key]))
        self.cur = key
        self.play(*anims, run_time=rt)

    def point(self, srcs, rt):
        """Pointers from (cell, index) pair texts to the cells they name."""
        arrows, anims = [], []
        for cell, i, target in srcs:
            ar, an = pointer(self.shot, self.pair(cell, i), target)
            ar.set_z_index(4)
            arrows.append(ar)
            anims += an
        self.play(*anims, run_time=rt)
        return arrows

    def strike(self, key, srcs, arrows, rt):
        """The pointing pair turns RED, the arrow fades; then the RED cross over the checked cell."""
        reds = [a for cell, i in srcs for a in recolor(_texts_of(self.pair(cell, i)), RED)]
        self.play(*reds, *[FadeOut(a) for a in arrows], run_time=0.4 * rt)
        self.play(*cross_cell(self.shot, key), run_time=0.6 * rt)

    def leave_open(self, key, arrows, rt):
        q = qmark(self.it.cells[key], self.shot.texts[key])
        self.qs[key] = q
        self.play(*during([FadeOut(a) for a in arrows], 0, 0.5),
                  *during(appear(q, shift=0.15 * DOWN), 0.4, 1.0), run_time=rt)  # early: the open cell's mark

    # ------------------------------------------------------------------ A-B
    def clip1(self):
        it, tbl, shot = self.it, self.tbl, self.shot
        cola = it.col_letter("A")
        self.col_color = cola.get_color()
        with self.say("c3.pass.1") as c:
            self.cap = rule_card()
            self.counter = pass_counter("pass 1")
            self.play(cola.animate.set_color(YELLOW), FlashAround(cola, color=YELLOW, time_width=1.5),
                      *during(appear(self.counter, shift=None), 0.3, 1.0), run_time=1.4)  # early: the pass counter
            self.go("A-B", 1.0)
            self.play(*appear(*self.cap, lag=0.3), run_time=1.6)  # early: p. 153's rule, read before it is used
            c.wait_until("the pair D and F")
            self.play(*flash([self.pair("A-B", 0)], time_width=1.5), run_time=1.2)
            c.wait_until("pointer")
            arrows = self.point([("A-B", 0, "D-F")], rt=min(2.0, c.until("crossed") - 0.3))
            c.wait_until("crossed")
            boxes = _out_boxes(tbl, "D", "F")
            outs = [tbl.cell(tbl.row_of(l), 3) for l in "DF"]
            self.play(_pulse_cross(shot.crosses["D-F"]), *[FadeIn(b) for b in boxes],
                      *flash(outs, color=GOLD, time_width=1.5), run_time=1.6)
            c.wait_until("broken")
            self.strike("A-B", [("A-B", 0)], arrows, rt=min(2.6, c.until("cross their cell") + 0.6))
            c.wait_until("cross their cell")
            self.play(*disappear(*boxes), run_time=min(1.0, c.remaining))

    # ------------------------------------------------------------------ A-D, A-G
    def clip2(self):
        with self.say("c3.pass.2") as c:
            self.go("A-D", min(1.2, c.until("its one promise")))
            c.wait_until("its one promise")
            self.play(*flash([self.pair("A-D", 1)], time_width=1.5), run_time=1.2)
            c.wait_until("open")
            arrows = self.point([("A-D", 1, "C-E")], rt=1.6)
            self.leave_open("A-D", arrows, rt=min(1.4, c.until("ag")))
            c.wait_until("ag")
            self.go("A-G", 1.2)
            c.wait_until("neither")
            arrows = self.point([("A-G", 0, "B-D"), ("A-G", 1, "C-H")], rt=1.8)
            self.leave_open("A-G", arrows, rt=min(1.4, c.until("not yet") - 0.1))
            c.wait_until("not yet")
            self.yet = T("not yet", 40, YELLOW, slant=ITALIC).move_to(CAP_XY)
            self.play(*swap(self.cap, self.yet), run_time=min(1.2, c.remaining))

    # ------------------------------------------------------------------ columns B and C
    def clip3(self):
        it = self.it
        cola, colb, colc = (it.col_letter(l) for l in "ABC")
        with self.say("c3.pass.3") as c:
            self.play(cola.animate.set_color(self.col_color), colb.animate.set_color(YELLOW),
                      FlashAround(colb, color=YELLOW, time_width=1.5), run_time=min(1.4, c.until("bd")))
            c.wait_until("bd")
            self.go("B-D", 0.9)
            arrows = self.point([("B-D", 0, "A-F")], rt=1.3)
            self.strike("B-D", [("B-D", 0)], arrows, rt=min(2.0, c.until("bg") - 0.1))
            c.wait_until("bg")
            self.go("B-G", 0.8)
            arrows = self.point([("B-G", 0, "B-F")], rt=1.2)
            self.strike("B-G", [("B-G", 0)], arrows, rt=min(1.8, c.until("colc") - 0.1))
            c.wait_until("colc")
            self.play(colb.animate.set_color(self.col_color), colc.animate.set_color(YELLOW),
                      FlashAround(colc, color=YELLOW, time_width=1.5), run_time=1.4)
            c.wait_until("cf")
            self.go("C-F", 0.8)
            arrows = self.point([("C-F", 1, "B-D")], rt=min(1.6, c.until("fresh") - 0.1))
            c.wait_until("fresh")
            self.fresh = VGroup(T("use a cross", 32), T("as soon as it's made", 32)).arrange(DOWN, buff=0.2).move_to(CAP_XY)
            self.play(_pulse_cross(self.shot.crosses["B-D"]), run_time=1.2)
            c.wait_until("use a cross")
            self.play(*swap(self.yet, self.fresh), run_time=1.2)
            c.wait_until("so cross this one")
            self.strike("C-F", [("C-F", 1)], arrows, rt=min(2.0, c.until("ceh") - 0.1))
            c.wait_until("ceh")
            self.go("C-E", 0.8)
            arrows = self.point([("C-E", 1, "A-D")], rt=1.0)
            self.leave_open("C-E", arrows, rt=0.8)
            self.go("C-H", 0.7)
            arrows = self.point([("C-H", 0, "C-E"), ("C-H", 1, "D-G")], rt=1.0)
            self.leave_open("C-H", arrows, rt=min(0.8, c.remaining))

    # ------------------------------------------------------------------ the rest
    def clip4(self):
        colc = self.it.col_letter("C")
        with self.say("c3.pass.4") as c:
            self.go("D-G", 1.0, extra=[colc.animate.set_color(self.col_color)])
            c.wait_until("the first cell we crossed")
            arrows = self.point([("D-G", 0, "A-B")], rt=min(1.6, c.until("cross it") - 0.1))
            c.wait_until("cross it")
            self.strike("D-G", [("D-G", 0)], arrows, rt=min(1.8, c.until("ef") - 0.1))
            c.wait_until("ef")
            self.go("E-F", 0.8)
            arrows = self.point([("E-F", 1, "A-B")], rt=1.2)
            self.strike("E-F", [("E-F", 1)], arrows, rt=min(1.6, c.until("eh") - 0.1))
            c.wait_until("eh")
            self.go("E-H", 0.8)
            arrows = self.point([("E-H", 0, "A-G")], rt=1.2)
            self.leave_open("E-H", arrows, rt=min(1.0, c.until("fh") - 0.1))
            c.wait_until("fh")
            self.go("F-H", 0.8)
            arrows = self.point([("F-H", 1, "B-G")], rt=1.2)
            self.strike("F-H", [("F-H", 1)], arrows, rt=min(1.6, c.until("seven") - 0.1))
            c.wait_until("seven")
            new = [self.shot.crosses[p] for p in S2.PASS1]
            done = pass_counter("pass 1: +7")
            self.play(*during([_outline(self.it.cells[self.cur], False)], 0, 0.5),
                      *during(disappear(self.fresh), 0, 0.5),
                      *[_pulse_cross(cr) for cr in new], run_time=1.6)
            self.cur = None
            c.wait_until("seven new crosses")
            self.play(*swap(self.counter, done), run_time=min(1.2, c.remaining))
            self.counter = done

    # ------------------------------------------------------------------ the slide's picture
    def clip5(self):
        it, shot = self.it, self.shot
        ag = it.cells["A-G"]
        with self.say("c3.pass.5") as c:
            inset = inset_picture()
            self.play(*disappear(*self.qs.values()), run_time=0.8)
            self.play(*appear(inset.frame, inset.pic, inset.label, shift=None, lag=0.2), run_time=1.2)  # early: the slide's page
            c.wait_until("checks the cell for A and G")
            self.play(_outline(ag), GrowFromCenter(inset.ring), run_time=1.2)
            quote = T("“comes from later on”", 32, slant=ITALIC).move_to(_p(4.3, 2.72))
            c.wait_until("comes from later on")
            self.play(*appear(quote, shift=None), run_time=1.0)
            c.wait_until("firstpass")
            q = qmark(ag, shot.texts["A-G"])
            bd = shot.crosses["B-D"]
            self.play(*during(disappear(inset.frame, inset.pic, inset.label, inset.ring, quote), 0, 0.5),
                      *during([bd.animate.set_stroke(opacity=0.15)], 0.3, 0.8),
                      *during(appear(q, shift=0.15 * DOWN), 0.5, 1.0), run_time=1.6)  # early: the open cell's mark
        self.wait(2.0)
        self.play(*disappear(q), bd.animate.set_stroke(opacity=1), _outline(ag, False), run_time=1.0)
        for sq in it.squares:
            sq.set_z_index(0)
        self.wait(1.0)
