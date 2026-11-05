"""Chapter 3, scene 2: the other nine cells of the implication table, p. 152. Clips c3.fill.1 - c3.fill.4.

Opens on ch2_s7_columna's handover_shot() (p. 150 table, staircase, GREEN dots, 16 crosses, column A).
Shared drawings for ch3 (import with load_scene("ch3_s2_fill")):
- `FILL`: (col, row, line, a, b) for every pair this scene writes (line 0 = X=0, upper; 1 = X=1).
- `home_shot(stage="full")`: the table at home. "full" = this scene's last frame (12 cells of
  promises, 16 crosses); "pass1" = full + RED crosses on PASS1 (texts DIM under them); "pass2" =
  pass1 + thick crosses on PASS2; "survivors" = pass2, all 26 crosses dimmed a little, A-D and C-E
  glowing GOLD. Handles: `.tbl` (state table), `.it` (staircase), `.dots`,
  `.texts["A-B"]` (VGroup of that cell's pair groups; a struck pair is VGroup(pair, line)),
  `.crosses["A-B"]` (every cross on screen, by pair), `.glow["A-D"]` (survivors only).
  Animate texts per part (their Texts), never a `.texts[...]` VGroup as a whole.
- `handover_shot()` = home_shot("full").
- `cross_cell(shot, pair, thick=False)` -> list of anims: draws a RED cross on the cell and dims its
  text; the cross is registered in `shot.crosses[pair]` (a new top-level mobject once played).
- `pointer(shot, text_mob, pair, color=YELLOW, angle=-PI/3)` -> (arrow, anims): a curved arrow from
  an implied pair's text to the cell it names, and a flash on that cell in the second half.
- `pass_counter(text)` -> T 32 at the top-right corner (right edge x=6.6, y=3.3); "+n" in GOLD.
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

L6 = load_scene("ch2_s6_outputs")
L7 = load_scene("ch2_s7_columna")
pair_at, struck, write_pair, strike_pair = L7.pair_at, L7.struck, L7.write_pair, L7.strike_pair
_outline, _out_boxes, _Ferry, _via = L7._outline, L7._out_boxes, L7._Ferry, L7._via


def _p(x, y):
    return np.array([x, y, 0.0])


# ------------------------------------------------------------------ shared: the table at home
FILL = [("B", "D", 0, "A", "F"), ("B", "D", 1, "E", "H"), ("B", "G", 0, "B", "F"),
        ("C", "E", 0, "C", "E"), ("C", "E", 1, "A", "D"), ("C", "F", 0, "E", "F"), ("C", "F", 1, "B", "D"),
        ("C", "H", 0, "C", "E"), ("C", "H", 1, "D", "G"), ("D", "G", 0, "A", "B"), ("D", "G", 1, "E", "H"),
        ("E", "F", 0, "C", "F"), ("E", "F", 1, "A", "B"), ("E", "H", 1, "A", "G"),
        ("F", "H", 0, "C", "F"), ("F", "H", 1, "B", "G")]
PASS1 = ["A-B", "B-D", "B-G", "C-F", "D-G", "E-F", "F-H"]
PASS2 = ["A-G", "C-H", "E-H"]
THIN, THICK = 5, 11


def _texts_of(g):
    return [m for m in g.get_family() if isinstance(m, Text)]


def _dim_texts(shot, pair):
    for g in shot.texts.get(pair, []):
        for m in _texts_of(g):
            m.set_color(DIM)


def home_shot(stage="full"):
    base = L7.handover_shot()
    shot6 = base[0]
    tbl, it, dots, out_crosses = shot6
    texts = {}
    for i, (col, row, line, a, b) in enumerate(L7.COLUMN_A):
        texts.setdefault(f"{col}-{row}", []).append(base[1 + i])
    new = VGroup()
    for col, row, line, a, b in FILL:
        p = pair_at(it, col, row, line, a, b)
        if (col, row, line) == ("C", "E", 0):
            p, ln = struck(p)
            p = VGroup(p, ln)
        new.add(p)
        texts.setdefault(f"{col}-{row}", []).append(p)
    shot = VGroup(base, new)
    shot.tbl, shot.it, shot.dots = tbl, it, dots
    shot.texts = {k: VGroup(*v) for k, v in texts.items()}
    shot.crosses = dict(out_crosses.by)
    shot.glow = {}
    if stage in ("pass1", "pass2", "survivors"):
        g = VGroup()
        for p in PASS1 + (PASS2 if stage != "pass1" else []):
            cr = L6.cell_cross(it.cells[p]).set_stroke(width=THICK if p in PASS2 else THIN)
            _dim_texts(shot, p)
            shot.crosses[p] = cr
            g.add(cr)
        shot.add(g)
    if stage == "survivors":
        for cr in shot.crosses.values():
            cr.set_stroke(opacity=0.6)
        for p in ("A-D", "C-E"):
            sq = it.cells[p]
            sq.set_stroke(GOLD, 5).set_fill(GOLD, 0.12).set_z_index(1)
            glow = Square(sq.side_length + 0.06).move_to(sq).set_stroke(GOLD, 16, opacity=0.25)
            glow.set_fill(opacity=0).set_z_index(1)
            for m in shot.texts[p]:
                m.set_z_index(2)
            shot.glow[p] = glow
            shot.add(glow)
    elif stage not in ("full", "pass1", "pass2"):
        raise ValueError(stage)
    return shot


def handover_shot():
    return home_shot("full")


def cross_cell(shot, pair, thick=False):
    cr = L6.cell_cross(shot.it.cells[pair]).set_stroke(width=THICK if thick else THIN)
    shot.crosses[pair] = cr
    dims = [m.animate.set_color(DIM) for g in shot.texts.get(pair, []) for m in _texts_of(g)]
    return [Create(cr), *dims]


def pointer(shot, text_mob, pair, color=YELLOW, angle=-PI / 3):
    cell = shot.it.cells[pair]
    a, b = text_mob.get_center(), cell.get_center()
    u = (b - a) / max(np.linalg.norm(b - a), 1e-6)
    arrow = ArcBetweenPoints(a + 0.3 * u, b - 0.32 * u, angle=angle).set_stroke(color, 4)
    arrow.add_tip(tip_length=0.2, tip_width=0.2)
    arrow.get_tip().set_fill(color, 1).set_stroke(color, 1)
    return arrow, [Create(arrow), *during([FlashAround(cell, color=color, time_width=1.5)], 0.55, 1.0)]


def pass_counter(text):
    t2c = {text[text.index("+"):]: GOLD} if "+" in text else {}
    t = T(text, 32, t2c=t2c)
    return t.move_to(_p(6.6 - t.width / 2, 3.3))


# ------------------------------------------------------------------ this scene's own pieces
CAP_XY = _p(4.3, 2.25)


def _table_texts(tbl):
    return [m for r in tbl.rows for m in r.cells] + [tbl.h_ps, tbl.h_ns, tbl.h_out, *tbl.subs]


class _Lane(Animation):
    """A copy of dst starts on src, slants over the dimmed table to the grid line between rows
    (the cell's top edge for line 0, bottom for line 1), rides it shrunk (LANE_K) past the row
    letters and other cells' text, then drops into its slot. Invisible until it has cleared src."""

    def __init__(self, src, dst, it, col, row, line, **kw):
        cell = it.cell(col, row)
        yb = cell.get_y() + (0.45 if line == 0 else -0.45)
        pts = [src.get_center(), _p(LANE_X, yb), _p(dst.get_x(), yb), dst.get_center()]
        self.path = VMobject().set_points_as_corners(pts)
        lens = [np.linalg.norm(pts[i + 1] - pts[i]) for i in range(3)]
        tot = sum(lens)
        self.f1, self.f2 = lens[0] / tot, sum(lens[:2]) / tot
        self.p0 = pts[0]
        self.k0 = src.height / max(dst.height, 1e-6)
        self.base = dst.copy()
        self.clear = max(src.width, src.height) * 1.2
        super().__init__(dst.copy(), remover=True, introducer=True, **kw)

    def interpolate_mobject(self, alpha):
        a = self.rate_func(alpha)
        if a < self.f1:
            k = self.k0 + (LANE_K - self.k0) * min(1, a / self.f1 * 1.5)
        elif a < self.f2:
            k = LANE_K
        else:
            k = LANE_K + (1 - LANE_K) * (a - self.f2) / max(1 - self.f2, 1e-6)
        m = self.mobject.become(self.base)
        m.scale(k)
        pos = self.path.point_from_proportion(a)
        m.move_to(pos)
        d = np.linalg.norm(pos - self.p0)
        m.set_opacity(float(np.clip((d - self.clear) / 0.4, 0, 1)))


GAP_X = L7.GAP_X
LANE_K = 0.7
LANE_X = -2.2    # where the slanting first leg (over the dimmed table) meets the grid line


def _read(scene, tbl, it, col, row, line, rt, clear=(), restore=False):
    """Read the next states of col and row under X=line (BLUE boxes, the rest of the table at 0.2),
    carry the two letters along the grid into the cell's line (alphabetical), add the dash.
    restore=False keeps the table dimmed (for runs of quick cells; then _restore())."""
    ra, rb_ = tbl.row_of(col), tbl.row_of(row)
    sa, sb = tbl.cell(ra, 1 + line), tbl.cell(rb_, 1 + line)
    first, second = (sa, sb) if sa.text < sb.text else (sb, sa)
    pair = pair_at(it, col, row, line, first.text, second.text)
    boxes = [SurroundingRectangle(s, color=BLUE, buff=0.08).set_stroke(BLUE, 2.5) for s in (sa, sb)]
    keep = [sa, sb, tbl.cell(ra, 0), tbl.cell(rb_, 0), tbl.subs[line]]
    others = [m for m in _table_texts(tbl) if all(m is not k for k in keep)]
    scene.play(*(disappear(*clear) if clear else []), *[FadeIn(bx) for bx in boxes],  # early: the dimmed table coming back
               *set_alpha(others, 0.2), *set_alpha(keep, 1),
               *flash([tbl.subs[line]], color=BLUE, time_width=1.5), run_time=0.3 * rt)
    lanes = dict(it=it, col=col, row=row, line=line)
    scene.play(*during([_Lane(second, pair.b, **lanes)], 0.0, 0.78),  # early: the read pair landing
               *during([_Lane(first, pair.a, **lanes)], 0.22, 1.0),
               *during(appear(pair.dash, shift=None), 0.85, 1.0),
               *(during(_restore(tbl), 0.8, 1.0) if restore else []), run_time=0.7 * rt)  # early: the read pair landing
    settle(scene, pair)
    return pair, boxes


def _restore(tbl):
    return set_alpha(_table_texts(tbl), 1)


class _Merge(Animation):
    """A copy of src travels straight to `meet`; the absorbed one fades as it arrives, the other
    sits on the meeting point and fades out: the two equal letters become one, then nothing."""

    def __init__(self, src, meet, absorbed=False, **kw):
        self.p0, self.meet = src.get_center(), np.array(meet)
        self.base = src.copy()
        self.clear = max(src.width, src.height) * 1.2
        self.absorbed = absorbed
        super().__init__(src.copy(), remover=True, introducer=True, rate_func=linear, **kw)

    def interpolate_mobject(self, alpha):
        m = self.mobject.become(self.base)
        k = smooth(min(1.0, alpha / 0.7))
        pos = self.p0 + (self.meet - self.p0) * k
        m.move_to(pos)
        op = np.clip((np.linalg.norm(pos - self.p0) - self.clear) / 0.4, 0, 1)
        if self.absorbed:
            op *= np.clip((np.linalg.norm(pos - self.meet) - 0.35) / 0.4, 0, 1)
        else:
            op *= np.clip((1 - alpha) / 0.25, 0, 1)
        m.set_opacity(float(op))


def _merge(scene, tbl, it, col, row, line, rt, clear=()):
    """Both rows go to the same state under X=line: the two letters fly toward the cell, merge, fade."""
    ra, rb_ = tbl.row_of(col), tbl.row_of(row)
    sa, sb = tbl.cell(ra, 1 + line), tbl.cell(rb_, 1 + line)
    boxes = [SurroundingRectangle(s, color=BLUE, buff=0.08).set_stroke(BLUE, 2.5) for s in (sa, sb)]
    keep = [sa, sb, tbl.cell(ra, 0), tbl.cell(rb_, 0), tbl.subs[line]]
    others = [m for m in _table_texts(tbl) if all(m is not k for k in keep)]
    scene.play(*(disappear(*clear) if clear else []), *[FadeIn(bx) for bx in boxes],  # early: the dimmed table coming back
               *set_alpha(others, 0.2), *set_alpha(keep, 1),
               *flash([tbl.subs[line]], color=BLUE, time_width=1.5), run_time=0.3 * rt)
    meet = _via(it, col, row, line)
    scene.play(_Merge(sa, meet), _Merge(sb, meet, absorbed=True), run_time=0.7 * rt)
    return boxes


def _rows(tbl, it, col, row):
    return [tbl.row_box(tbl.row_of(col)), tbl.row_box(tbl.row_of(row))], _out_boxes(tbl, col, row)


class Fill(NarratedScene):
    def construct(self):
        base = L7.handover_shot()
        self.add(base)
        self.tbl, self.it = base[0][0], base[0][1]
        self.ad_struck = base[3]          # column A's struck "A-D"
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

    def switch(self, old_cell, new_cell, gone, rt, new_boxes=(), extra=()):
        """Old boxes out and old outline off, then new row/output boxes in and new outline on."""
        anims = [*during(disappear(*gone), 0, 0.45)] if gone else []
        if old_cell is not None:
            anims += during([_outline(old_cell, False)], 0.1, 0.6)
        ins = [FadeIn(b) for b in new_boxes] + ([_outline(new_cell)] if new_cell is not None else [])
        if ins:
            anims += during(ins, 0.45, 1.0)
        self.play(*anims, *extra, run_time=rt)

    # ------------------------------------------------------------------ B-D
    def clip1(self):
        tbl, it = self.tbl, self.it
        with self.say("c3.fill.1") as c:
            colb = it.col_letter("B")
            self.play(colb.animate.set_color(YELLOW), FlashAround(colb, color=YELLOW, time_width=1.5),
                      run_time=1.5)
            c.wait_until("bd")

            bd = it.cell("B", "D")
            rb, ob = _rows(tbl, it, "B", "D")
            self.play(*[FadeIn(b) for b in rb], _outline(bd), run_time=min(1.2, c.until("output zero")))
            c.wait_until("output zero")
            self.play(*[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("bd0")

            p1, bx1 = _read(self, tbl, it, "B", "D", 0, restore=True, rt=min(2.6, c.until("bd1") - 0.2))
            c.wait_until("bd1")
            p2, bx2 = _read(self, tbl, it, "B", "D", 1, restore=True, rt=min(2.6, c.until("bdcell") - 0.2),
                                 clear=bx1)
            c.wait_until("the pair A and F")
            self.play(*flash([p1], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("E and H")
            self.play(*flash([p2], color=YELLOW, time_width=1.5), run_time=1.2)
            self.cell, self.boxes = bd, rb + ob + bx2

    # ------------------------------------------------------------------ B-G: H and H
    def clip2(self):
        tbl, it = self.tbl, self.it
        with self.say("c3.fill.2") as c:
            bg = it.cell("B", "G")
            rb, ob = _rows(tbl, it, "B", "G")
            self.switch(self.cell, bg, self.boxes, min(1.6, c.until("output zero too")), rb)
            c.wait_until("output zero too")
            self.play(*[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("bg0")

            p1, bx1 = _read(self, tbl, it, "B", "G", 0, restore=True, rt=min(2.6, c.until("bg1") - 0.2))
            c.wait_until("bg1")
            bx2 = _merge(self, tbl, it, "B", "G", 1, rt=min(2.8, c.until("same") - 0.3), clear=bx1)
            self.play(*_restore(tbl), run_time=0.6)
            c.wait_until("same")

            cap = VGroup(MathTex(r"H \equiv H", font_size=52),
                         T("always true, not written", 30, DIM)).arrange(DOWN, buff=0.3).move_to(CAP_XY)
            self.play(*appear(*cap, lag=0.5), run_time=1.4)  # early: the caption the sentence explains
            c.wait_until("bgcell")
            self.play(*flash([p1], color=YELLOW, time_width=1.5), run_time=1.4)
            self.cell, self.boxes, self.cap = bg, rb + ob + bx2, cap

    # ------------------------------------------------------------------ C-E: self-implied
    def clip3(self):
        tbl, it = self.tbl, self.it
        with self.say("c3.fill.3") as c:
            ce = it.cell("C", "E")
            rb, ob = _rows(tbl, it, "C", "E")
            colb, colc = it.col_letter("B"), it.col_letter("C")
            self.switch(self.cell, ce, self.boxes + list(self.cap), min(1.6, c.until("both output one")), rb,
                        extra=[colb.animate.set_color(FG), colc.animate.set_color(YELLOW)])
            c.wait_until("both output one")
            self.play(*[FadeIn(b) for b in ob], run_time=1.0)
            c.wait_until("ce0")

            p1, bx1 = _read(self, tbl, it, "C", "E", 0, restore=True,
                            rt=min(2.6, c.until("That's the very pair") - 0.2))
            c.wait_until("That's the very pair")
            self.play(*flash([colc, it.row_letter("E")], color=YELLOW, time_width=1.5),
                      it.row_letter("E").animate.set_color(YELLOW), run_time=1.5)
            c.wait_until("strike it out")
            ln = strike_pair(self, p1, run_time=1.4)
            p1g = VGroup(p1, ln)
            settle(self, p1g)
            c.wait_until("just as we did")
            self.play(*flash([self.ad_struck], color=YELLOW, time_width=1.5),
                      it.row_letter("E").animate.set_color(FG), run_time=1.4)
            c.wait_until("ce1")

            p2, bx2 = _read(self, tbl, it, "C", "E", 1, restore=True, rt=min(2.6, c.until("cecell") - 0.2),
                                 clear=bx1)
            c.wait_until("A and D are")
            self.play(*flash([p2], color=YELLOW, time_width=1.5), run_time=min(1.4, max(0.3, c.remaining - 0.05)))
            self.cell, self.boxes = ce, rb + ob + bx2

    # ------------------------------------------------------------------ the rest
    def clip4(self):
        tbl, it = self.tbl, self.it
        with self.say("c3.fill.4") as c:
            colc = it.col_letter("C")
            self.switch(self.cell, None, self.boxes, 1.2, extra=[colc.animate.set_color(FG)])
            self.cell = None
            c.wait_until("you just have to keep")
            quote = T("“you just have to keep\ndoing these pairwise\ncomparisons”", 32,
                      slant=ITALIC, line_spacing=0.85).move_to(CAP_XY)

            # four quick cells, the table kept dimmed between them; the quote comes in with the first,
            # and all four are done before {eh} so rows E and H light on their own sentence
            quick = [("C", "F"), ("C", "H"), ("D", "G"), ("E", "F")]
            sw0, sw = 1.0, 0.45
            rt = float(np.clip((c.until("eh") - 0.3 - sw0 - 3 * sw) / 8, 0.5, 0.9))
            gone = []
            for i, (col, row) in enumerate(quick):
                cell = it.cell(col, row)
                rb, ob = _rows(tbl, it, col, row)
                self.switch(self.cell, cell, gone, sw0 if i == 0 else sw, rb + ob,
                            extra=appear(quote, shift=None) if i == 0 else ())  # early: the quote the sentence reads
                _, bx1 = _read(self, tbl, it, col, row, 0, rt)
                _, bx2 = _read(self, tbl, it, col, row, 1, rt, clear=bx1)
                self.cell, gone = cell, rb + ob + bx2

            # E-H: C twice
            eh = it.cell("E", "H")
            rb, ob = _rows(tbl, it, "E", "H")
            c.wait_until("eh")
            self.switch(self.cell, eh, gone, 1.0, rb + ob, extra=_restore(tbl))
            c.wait_until("input zero leads")
            bx1 = _merge(self, tbl, it, "E", "H", 0, rt=min(2.6, c.until("single") - 0.8))
            self.play(*_restore(tbl), run_time=0.6)
            c.wait_until("single")
            p2, bx2 = _read(self, tbl, it, "E", "H", 1, restore=True, rt=min(2.4, c.until("full") - 0.2),
                                 clear=bx1)
            c.wait_until("full")

            # F-H, then the table complete
            fh = it.cell("F", "H")
            eh_gone = rb + ob + bx2
            rb, ob = _rows(tbl, it, "F", "H")
            self.switch(eh, fh, eh_gone, 0.6, rb + ob)
            _, b1 = _read(self, tbl, it, "F", "H", 0, 0.9)
            _, b2 = _read(self, tbl, it, "F", "H", 1, 0.9, clear=b1)
            tally = VGroup(T("12 cells of promises", 36, t2c={"12": GOLD}),
                           T("16 crosses", 36, t2c={"16": GOLD})).arrange(DOWN, buff=0.25).move_to(CAP_XY)
            self.play(*during(disappear(*rb, *ob, *b2), 0, 0.5), *during([_outline(fh, False)], 0, 0.5),
                      *during(_restore(tbl), 0, 0.6), *swap(quote, tally), run_time=1.4)  # early: the tally the sentence reads
            c.wait_until("sixteen crosses")
            self.play(*flash([it.cells[p] for p in L6.CROSSED], color=RED, time_width=1.5),
                      run_time=min(1.4, max(0.3, c.remaining)))

        self.wait(4.0)
        self.play(*disappear(tally), run_time=1.0)
        for sq in it.squares:
            sq.set_z_index(0)
        self.wait(1.0)


