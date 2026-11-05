"""Chapter 2, scene 7: column A of the implication table filled in, p. 152. Clips c2.column.1 - c2.column.3.

Opens on ch2_s6_outputs' handover_shot() (table, staircase, GREEN dots, 16 crosses).
Shared drawings (import with load_scene("ch2_s7_columna")):
- `pair_text(a, b, size=28, color=FG)`: an implied pair "a-b" as three Texts; `.a .dash .b`.
- `pair_slot(it, col, row, line)`: centre of line 0 (X=0, upper) or line 1 (X=1, lower) of a cell.
- `pair_at(it, col, row, line, a, b)`: pair_text placed in that slot (letters as given).
- `strike_line(pair)`: the DIM strike-through Line for a self-implied pair;
  `struck(pair)`: recolours the pair DIM and returns (pair, line) in the struck style (not added).
- `write_pair(scene, tbl, it, col, row, line, run_time=2.0, order="abc", clear=())`: reads the
  next states of col and row under X=line in the table (BLUE boxes), flies the two letters into
  the cell's line and adds the dash; alphabetical by default (`order="said"`: as read, col's
  first; then `alphabetise(scene, pair)` swaps them). `clear`: mobjects faded in the first part.
  Returns (pair, boxes); the boxes stay on screen. None if both next states are the same.
- `strike_pair(scene, pair, run_time=1.2)`: plays the strike-through + DIM; returns the line.
- `column_a_pairs(it)`: the six pair groups of this scene's final frame (struck A-D included).
- `handover_shot()`: s6's shot + column A filled (this scene's last frame; s8 and ch3 s1 open on it).
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

L5 = load_scene("ch2_s5_layout")
L6 = load_scene("ch2_s6_outputs")
L1 = load_scene("ch2_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ shared: implied pairs in cells
LINE_DY = 0.2


def pair_text(a, b, size=28, color=FG):
    la, dash, lb = T(a, size, color), T("-", size, color), T(b, size, color)
    g = VGroup(la, dash, lb).arrange(RIGHT, buff=0.05)
    g.a, g.dash, g.b = la, dash, lb
    return g


def pair_slot(it, col, row, line):
    return it.cell(col, row).get_center() + (LINE_DY if line == 0 else -LINE_DY) * UP


def pair_at(it, col, row, line, a, b, **kw):
    return pair_text(a, b, **kw).move_to(pair_slot(it, col, row, line))


def strike_line(pair):
    return Line(pair.get_left() + 0.06 * LEFT, pair.get_right() + 0.06 * RIGHT).set_stroke(DIM, 3.5)


def struck(pair):
    pair.set_color(DIM)
    return pair, strike_line(pair)


class _Ferry(Animation):
    """A copy of dst starts on src (at src's size) and travels through `via` into dst's place,
    invisible until it has cleared src, so it never sits doubled on its source."""

    def __init__(self, src, dst, via, **kw):
        self.p0 = src.get_center()
        self.k0 = src.height / max(dst.height, 1e-6)
        self.path = VMobject().set_points_smoothly([self.p0, np.array(via), dst.get_center()])
        self.base = dst.copy()
        self.clear = max(src.width, src.height) * 1.2
        super().__init__(dst.copy(), remover=True, introducer=True, **kw)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        m = self.mobject.become(self.base)
        m.scale(self.k0 + (1 - self.k0) * a)
        pos = self.path.point_from_proportion(a)
        m.move_to(pos)
        d = np.linalg.norm(pos - self.p0)
        m.set_opacity(float(np.clip((d - self.clear) / 0.4, 0, 1)))


GAP_X = -0.8     # the free strip between the state table and the staircase's row letters


def _via(it, col, row, line):
    """Where a carried letter crosses into the staircase: between two row letters, above (line 0)
    or below (line 1) the cell's own row letter."""
    return _p(GAP_X, it.cell(col, row).get_y() + (0.45 if line == 0 else -0.45))


def write_pair(scene, tbl, it, col, row, line, run_time=2.0, order="abc", clear=()):
    """Read the next states of col and row under X=line (BLUE boxes, the rest of the table dimmed),
    carry the two letters into the cell's line, add the dash, restore the table."""
    ra, rb_ = tbl.row_of(col), tbl.row_of(row)
    sa, sb = tbl.cell(ra, 1 + line), tbl.cell(rb_, 1 + line)
    a, b = sa.text, sb.text
    if a == b:
        return None
    first, second = (sa, sb) if (order == "said" or a < b) else (sb, sa)
    pair = pair_at(it, col, row, line, first.text, second.text)
    boxes = [SurroundingRectangle(s, color=BLUE, buff=0.08).set_stroke(BLUE, 2.5) for s in (sa, sb)]
    keep = {id(sa), id(sb), id(tbl.cell(ra, 0)), id(tbl.cell(rb_, 0)), id(tbl.subs[line])}
    others = [m for r in tbl.rows for m in r.cells if id(m) not in keep]
    others += [m for m in (tbl.h_ps, tbl.h_ns, tbl.h_out, *tbl.subs) if id(m) not in keep]
    scene.play(*(disappear(*clear) if clear else []), *[FadeIn(bx) for bx in boxes],  # early: the dimmed table coming back
               *set_alpha(others, 0.2),
               *flash([tbl.subs[line]], color=BLUE, time_width=1.5), run_time=0.3 * run_time)
    via = _via(it, col, row, line)
    # the right-hand letter lands first, so the left one never passes over it
    scene.play(*during([_Ferry(second, pair.b, via)], 0.0, 0.78),  # early: the dimmed table coming back
               *during([_Ferry(first, pair.a, via)], 0.22, 1.0),
               *during(appear(pair.dash, shift=None), 0.85, 1.0),
               *during(set_alpha(others, 1), 0.8, 1.0), run_time=0.7 * run_time)  # early: the dimmed table coming back
    settle(scene, pair)
    return pair, boxes


def alphabetise(scene, pair, run_time=1.2):
    """The two letters of a pair written as said swap places: alphabetical order."""
    tgt = pair_text(pair.b.text, pair.a.text).move_to(pair.get_center())   # exactly as pair_at builds it
    scene.play(pair.a.animate(path_arc=-PI).move_to(tgt.b), pair.b.animate(path_arc=-PI).move_to(tgt.a),
               pair.dash.animate.move_to(tgt.dash), run_time=run_time)
    pair.a, pair.b = pair.b, pair.a
    pair.submobjects = [pair.a, pair.dash, pair.b]
    settle(scene, pair)


def strike_pair(scene, pair, run_time=1.2):
    ln = strike_line(pair)
    scene.play(Create(ln), *[m.animate.set_color(DIM) for m in pair], run_time=run_time)
    return ln


COLUMN_A = [("A", "B", 0, "D", "F"), ("A", "B", 1, "C", "H"), ("A", "D", 0, "A", "D"),
            ("A", "D", 1, "C", "E"), ("A", "G", 0, "B", "D"), ("A", "G", 1, "C", "H")]


def column_a_pairs(it):
    out = []
    for col, row, line, a, b in COLUMN_A:
        p = pair_at(it, col, row, line, a, b)
        if (col, row, line) == ("A", "D", 0):
            p, ln = struck(p)
            p = VGroup(p, ln)
        out.append(p)
    return out


def handover_shot():
    shot = L6.handover_shot()
    return VGroup(shot, *column_a_pairs(shot[1]))


# ------------------------------------------------------------------ this scene's own pieces
def _outline(cell, on=True):
    cell.set_z_index(1)
    return cell.animate.set_stroke(YELLOW if on else FG, 5 if on else 2)


def _out_boxes(tbl, *letters):
    return [SurroundingRectangle(tbl.cell(tbl.row_of(l), 3), color=GOLD, buff=0.1).set_stroke(GOLD, 2.5)
            for l in letters]


def _pulse(mob, color=YELLOW, base=FG):
    def f(m, a):
        m.set_color(interpolate_color(ManimColor(base), ManimColor(color), np.sin(PI * a)))
    return UpdateFromAlphaFunc(mob, f)


def _small_lanes():
    """s1's two lanes, redrawn compact for the empty corner above the staircase's diagonal:
    "start in A/D" left of each lane, circles, the GOLD-boxed output rows facing each other, a GOLD "=" left of them."""
    pitch, x0 = 0.6, 4.14
    lane_y, out_y = (3.45, 1.95), (2.98, 2.42)
    g = VGroup()
    for l, seq in enumerate(L1.LANES):
        cs = [T(s, 30).move_to(_p(x0 + pitch * k, lane_y[l])) for k, s in enumerate(seq)]
        ars = [Arrow(cs[i].get_right(), cs[i + 1].get_left(), buff=0.07, stroke_width=2.5, color=DIM,
                     tip_length=0.12, max_tip_length_to_length_ratio=0.5) for i in range(4)]
        outs = [(T(L1.OUT[s], 28, GREEN, weight=BOLD) if L1.OUT[s] == "1" else T(L1.OUT[s], 28))
                .move_to(_p(x0 + pitch * k, out_y[l])) for k, s in enumerate(seq)]
        box = (Rectangle(width=4 * pitch + 0.5, height=0.4).move_to(_p(x0 + 2 * pitch, out_y[l]))
               .set_stroke(GOLD, 2).set_fill(GOLD, 0.15).set_z_index(-1))
        lab = T(f"start in {seq[0]}:", 28).next_to(cs[0], LEFT, buff=0.2)
        g.add(lab, *cs, *ars, box, *outs)
    eq = T("=", 48, GOLD).move_to(_p(x0 - 0.65, sum(out_y) / 2))
    g.add(eq)
    return g


CAP_XY = _p(4.9, 2.3)


class ColumnA(NarratedScene):
    def construct(self):
        shot = L6.handover_shot()
        self.add(shot)
        self.tbl, self.it = shot[0], shot[1]
        self.clip1()
        self.clip2()
        self.clip3()

    # ------------------------------------------------------------------ A-B
    def clip1(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.column.1") as c:
            ab = it.cell("A", "B")
            rb = [tbl.row_box(0), tbl.row_box(1)]
            self.play(*[FadeIn(b) for b in rb], _outline(ab), run_time=min(1.2, c.until("zeroout")))
            c.wait_until("zeroout")

            ob = _out_boxes(tbl, "A", "B")
            self.play(*[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("zero")

            p1, bx1 = write_pair(self, tbl, it, "A", "B", 0, run_time=min(2.6, c.until("one") - 0.2))
            c.wait_until("one")
            p2, bx2 = write_pair(self, tbl, it, "A", "B", 1, run_time=min(2.6, c.until("write") - 0.2),
                                 clear=bx1)
            c.wait_until("write")

            cap = VGroup(MathTex(r"A \equiv B", font_size=52),
                         MathTex(r"\text{if } D \equiv F", font_size=48),
                         MathTex(r"\text{and } C \equiv H.", font_size=48))
            cap.arrange(DOWN, buff=0.28).move_to(CAP_XY)
            self.play(*appear(*cap, lag=0.6), run_time=min(2.4, c.until("Those two implied pairs")))  # early: one sentence, lines read as it goes
            c.wait_until("Those two implied pairs")
            self.play(*flash([p1, p2], color=YELLOW, time_width=1.5), run_time=1.4)
            self.cap1 = cap
            self.boxes = rb + ob + bx2
            self.ab_pairs = (p1, p2)

    # ------------------------------------------------------------------ A-D: the self-implied pair
    def clip2(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.column.2") as c:
            ab, ad = it.cell("A", "B"), it.cell("A", "D")
            rb = [tbl.row_box(0), tbl.row_box(3)]
            self.play(*during(disappear(self.cap1, *self.boxes), 0, 0.45),
                      *during([_outline(ab, False)], 0.1, 0.6),
                      *during([FadeIn(b) for b in rb] + [_outline(ad)], 0.45, 1.0),
                      run_time=min(1.6, c.until("the pair we started with")))
            c.wait_until("the pair we started with")

            lanes = _small_lanes()
            self.play(FadeIn(lanes), run_time=1.0)  # early: a recap of s1's picture, its labels not read aloud
            c.wait_until("again both output zero")
            ob = _out_boxes(tbl, "A", "D")
            self.play(*[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("self")

            p1, bx1 = write_pair(self, tbl, it, "A", "D", 0,
                                 run_time=min(2.6, c.until("So the two are equivalent") - 0.2))
            c.wait_until("So the two are equivalent")
            cap = MathTex(r"A \equiv D", r"\text{ if }", r"A \equiv D", font_size=40).move_to(_p(5.0, 0.85))
            self.play(*appear(cap, shift=None), run_time=1.0)
            c.wait_until("strike")

            ln = strike_pair(self, p1, run_time=1.4)
            p1g = VGroup(p1, ln)
            settle(self, p1g)
            note = T("Note that ‘self implied’ pairs\nare removed from the table", 28, DIM,
                     slant=ITALIC, line_spacing=0.8).move_to(_p(-3.9, -3.2))
            self.play(*appear(note, shift=None), run_time=1.0)  # early: p. 152's note, not read aloud
            c.wait_until("ce")

            p2, bx2 = write_pair(self, tbl, it, "A", "D", 1, run_time=min(2.6, c.until("promise") - 0.2),
                                 clear=bx1)
            c.wait_until("promise")
            cap2 = MathTex(r"A \equiv D", r"\text{ if }", r"C \equiv E", font_size=42).move_to(cap)
            self.play(*swap(cap, cap2), *during(disappear(lanes), 0, 0.6), run_time=min(1.4, c.remaining))
            self.cap2, self.note = cap2, note
            self.boxes = rb + ob + bx2
            self.ad_pairs = (p1g, p2)

    # ------------------------------------------------------------------ A-G, the C-H twice, done
    def clip3(self):
        tbl, it = self.tbl, self.it
        with self.say("c2.column.3") as c:
            ad, ag = it.cell("A", "D"), it.cell("A", "G")
            rb = [tbl.row_box(0), tbl.row_box(6)]
            self.play(*during(disappear(*self.boxes), 0, 0.45),
                      *during([_outline(ad, False)], 0.1, 0.6),
                      *during([FadeIn(b) for b in rb] + [_outline(ag)], 0.45, 1.0),
                      run_time=min(1.6, c.until("also both output zero")))
            c.wait_until("also both output zero")
            ob = _out_boxes(tbl, "A", "G")
            self.play(*disappear(self.cap2, self.note), *[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("ag0")

            p1, bx1 = write_pair(self, tbl, it, "A", "G", 0, order="said",
                                 run_time=min(2.4, c.until("written in alphabetical order") - 0.2))
            c.wait_until("written in alphabetical order")
            alphabetise(self, p1, run_time=1.4)
            c.wait_until("ag1")

            p2, bx2 = write_pair(self, tbl, it, "A", "G", 1, run_time=min(2.4, c.until("twice") - 0.2),
                                 clear=bx1)
            c.wait_until("twice")

            ch1, ch2 = self.ab_pairs[1], p2
            arc = ArcBetweenPoints(ch1.get_right() + 0.1 * RIGHT, ch2.get_right() + 0.1 * RIGHT,
                                   angle=-PI / 3).set_stroke(YELLOW, 3, opacity=0.55)
            self.play(_pulse(ch1), _pulse(ch2), Create(arc), run_time=1.8)
            c.wait_until("If it ever fails")
            self.play(*flash([ch1, ch2], color=RED, time_width=1.5), run_time=1.4)
            self.play(FadeOut(arc), run_time=1.0)
            c.wait_until("done")

            filled = [it.cell("A", r) for r in "BDG"]
            cap = VGroup(T("column A:", 36),
                         T("3 cells of promises,", 36, t2c={"3": GOLD}),
                         T("4 crosses", 36, t2c={"4": GOLD}))
            cap.arrange(DOWN, buff=0.22).move_to(CAP_XY).set_x(4.3)
            self.play(*during(disappear(*rb, *ob, *bx2), 0, 0.5),  # early: one caption, read as the sentence goes
                      *[_outline(sq) for sq in filled],
                      *during(appear(*cap, shift=None, lag=0.4), 0.3, 1.0),
                      run_time=min(1.6, c.until("four crosses")))
            c.wait_until("four crosses")
            crossed = [it.cell("A", r) for r in "CEFH"]
            self.play(*flash(crossed, color=RED, time_width=1.5),
                      run_time=min(1.4, c.remaining))

        self.wait(2.8)
        self.play(*disappear(cap), *[_outline(sq, False) for sq in filled], run_time=1.0)
        for sq in [it.cell("A", r) for r in "BCDEFGH"]:
            sq.set_z_index(0)
        self.wait(1.0)
