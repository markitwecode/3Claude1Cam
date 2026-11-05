"""Chapter 1, scene 6: matches that appear. K, M, N, P merge into H; L into J; then the new matches
D/G and E/F merge; fifteen states become seven; step 3 of the rule. Clips c1.cascade.1 – c1.cascade.4.

Opens on s5's handover_shot() and merges with s5's look (replace_entry, swing_arc, dim_state,
arc_geometry, state_counter); the batched variants below (several rows / circles / arcs in one
play) mirror s5's delete_row, merge_circle and swing_arc exactly.
Module-level helpers (load_scene("ch1_s6_cascade")):
  ROWS_AFTER_L: the 9-row table of p. 147's first slide; ROWS_FINAL: the 7-row table
  matched_table() -> VGroup(tbl, *boxes): the 9-row table (s5 layout) with rows D, G and E, F lit
    GOLD; .tbl, .boxes[letter]  (s8 recap r5)
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

S4 = load_scene("ch1_s4_tree")
S5 = load_scene("ch1_s5_hi")

ROWS_AFTER_L = [
    ("A", "B", "C", "0", "0"), ("B", "D", "E", "0", "0"), ("C", "F", "G", "0", "0"),
    ("D", "H", "H", "0", "0"), ("E", "J", "H", "0", "0"), ("F", "J", "H", "0", "0"),
    ("G", "H", "H", "0", "0"), ("H", "A", "A", "0", "0"), ("J", "A", "A", "0", "1"),
]
ROWS_FINAL = [
    ("A", "B", "C", "0", "0"), ("B", "D", "E", "0", "0"), ("C", "E", "D", "0", "0"),
    ("D", "H", "H", "0", "0"), ("E", "J", "H", "0", "0"), ("H", "A", "A", "0", "0"),
    ("J", "A", "A", "0", "1"),
]


def matched_table():
    """The 9-row table with rows D, G and E, F lit GOLD (s8's recap reuses it)."""
    tbl = S5.layout_table(ROWS_AFTER_L)
    boxes = {k: tbl.row_box(tbl.row_of(k), GOLD) for k in "DGEF"}
    g = VGroup(tbl, *boxes.values())
    g.tbl, g.boxes = tbl, boxes
    return g


# ---------------------------------------------------------------- layout of the right column
CNT_Y = -1.2          # the state counter, right corner under the diagram
TAG_Y = -1.8          # tags, left under the diagram
DIAG_DROP = 0.5       # the diagram moves down to make room for step 3


def counter(a, b):
    c = S5.state_counter(a, b).scale(0.75)
    return c.move_to([0, CNT_Y, 0]).align_to([6.55, 0, 0], RIGHT)


def tag(text, color=GOLD):
    return T(text, 30, color).move_to([0, TAG_Y, 0]).align_to([S5.RIGHT_X, 0, 0], LEFT)


Q_REPLACE4 = ["Similarly, rows K, M, N and P have", "the same next state and output as H",
              "and can be replaced by H"]
Q_DELETE4 = ["Similarly, there is now no way to", "get to states K, M, N and P and so",
             "we can remove these rows from the", "table"]
Q_REPLACEL = ["Also, the next state and outputs are", "identical for rows J and L, thus L",
              "can be replaced by J and row L", "eliminated from the table"]
Q_NEW = ["Now rows D and G are identical, as", "are rows E and F."]
Q_REPLACEGF = ["Consequently, G can be replaced", "by D, and row G eliminated. Also,",
               "F can be replaced by E and row F", "eliminated from the table"]


# ---------------------------------------------------------------- batched merges (s5's look)
def replace_entries(scene, tbl, items, run_time=1.5, color=GOLD):
    """s5's replace_entry for several cells at once: each flashes and swaps into its match."""
    anims, done = [], []
    for r, c, letter in items:
        old = tbl.cell(r, c)
        new = T(letter, S5.TABLE_SIZE, color).move_to(old)
        anims += [FlashAround(old, color=color, time_width=1.5), *swap(old, new)]
        done.append((r, c, old, new))
    scene.play(*anims, run_time=run_time)
    for r, c, old, new in done:
        row = tbl.rows[r]
        row.remove(old)
        row.cells[c] = new
        row.add(new)
    settle(scene, tbl)
    return [d[3] for d in done]


def swing_arcs(scene, d, items, run_time=1.5):
    """s5's swing_arc for several arcs at once; items (src, x, dst, bend or None)."""
    anims = []
    for src, x, dst, bend in items:
        arc, _ = S5.arc_geometry(d, src, x, dst, bend=bend)
        anims.append(Transform(d.arcs[(src, x)], arc))
    scene.play(*anims, run_time=run_time)
    settle(scene, d)


def delete_rows(scene, tbl, letters, extra=(), run_time=1.6):
    """s5's delete_row for several rows at once: they leave, the rows below close up."""
    idx = sorted(tbl.row_of(k) for k in letters)
    rows = [tbl.rows[i] for i in idx]
    ys = [rw.cells[0].get_y() for rw in rows]
    p = tbl.pitch
    moves = []
    for i, rw in enumerate(tbl.rows):
        n = sum(1 for j in idx if j < i)
        if i not in idx and n:
            moves.append(rw.animate.shift(n * p * UP))
    for m in tbl.rules[1:]:
        n = sum(1 for y in ys if y > m.get_y() + 0.01)
        if n:
            moves.append(m.animate.shift(n * p * UP))
    for sep in tbl.seps:
        moves.append(Transform(sep, Line(sep.get_start(), sep.get_end() + len(idx) * p * UP).set_stroke(DIM, 2)))
    scene.play(*during(disappear(*rows), 0, 0.4), *during(moves, 0.45, 1.0), *extra, run_time=run_time)
    for rw in rows:
        tbl.rows.remove(rw)
        tbl.remove(rw)
    S5._set_row_of(tbl)
    settle(scene, tbl)


def merge_circles(scene, d, pairs, extra=(), run_time=1.5):
    """s5's merge_circle for several states at once: each circle slides into its match (70%),
    then fades (30%)."""
    out, moves, gone_all = [], [], []
    for name, into in pairs:
        st = d.states[name]
        gone = [m for m in [d.stubs.get(name)] if m is not None]
        gone += [d.arcs[k] for k in list(d.arcs) if k[0] == name]
        out += disappear(st.letter, *gone)
        moves.append(st.circle.animate.set_stroke(DIM, opacity=1).move_to(d.states[into].get_center()))
        gone_all.append((name, st, gone))
    scene.play(*during(out, 0, 0.3), *during(moves, 0.15, 1.0), *extra, run_time=0.7 * run_time)
    scene.play(*[FadeOut(st.circle) for _, st, _ in gone_all], run_time=0.3 * run_time)
    for name, st, gone in gone_all:
        d.remove(st, *gone)
        d.states.pop(name)
        d.stubs.pop(name, None)
        for k in [k for k in list(d.arcs) if k[0] == name]:
            d.arcs.pop(k)
    settle(scene, d)


# ---------------------------------------------------------------- the scene
class Cascade(NarratedScene):
    def construct(self):
        shot = S5.handover_shot()
        self.tbl, self.d, self.cap, self.cnt = shot[0], shot[1], shot[2], shot[3]
        self.add(self.tbl, self.d, self.cap, self.cnt)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(2.0)          # step 3 stays up a moment after the voice
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def new_counter(self, a, b, extra=()):
        c = counter(a, b)
        anims = swap(self.cnt, c)
        self.cnt = c
        return anims

    def rows(self, letters):
        return [self.tbl.rows[self.tbl.row_of(k)] for k in letters]

    # ------------------------------------------------------------ c1: K, M, N, P match H
    def clip1(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.cascade.1") as c:
            upper = self.rows("ABCDEFG")
            target = counter(15, 14)
            self.play(self.cnt.animate.scale(0.75).move_to(target), *set_alpha(upper, 0.4),
                      run_time=min(1.3, c.until("kmnp")))
            c.wait_until("kmnp")
            grp = "HKMNP"
            self.boxes = [tbl.row_box(tbl.row_of(k), GOLD) for k in grp]
            self.play(*[FadeIn(b) for b in self.boxes],
                      *[restyle(d.states[k], outline=GOLD) for k in grp], run_time=1.5)
            settle(self, d)
            c.wait_until("each goes")
            nxt = [tbl.cell(tbl.row_of(k), j) for k in grp for j in (1, 2)]
            outs = [tbl.cell(tbl.row_of(k), j) for k in grp for j in (3, 4)]
            self.play(*recolor(nxt, YELLOW), run_time=1.0)
            c.wait_until("outputs")
            self.play(*recolor(outs, YELLOW), run_time=0.9)
            c.wait_until("start")
            self.tag = tag("identical from the start")
            self.play(*recolor(nxt + outs, FG), *appear(self.tag), run_time=1.2)  # early: names "matched from the very start"
            c.wait_until("replace4")
            self.quote = S5.quote(Q_REPLACE4)
            self.play(*appear(*self.quote, lag=0.15), *set_alpha(upper, 1),  # early: the slide's bullet, read whole
                      run_time=min(1.5, c.until("e1")))
            c.wait_until("e1")
            self.gold = []
            self.gold += replace_entries(self, tbl, [(tbl.row_of("E"), 2, "H")], run_time=1.2)
            swing_arcs(self, d, [("E", 1, "H", None)], run_time=min(1.2, c.until("f1")))
            c.wait_until("f1")
            self.gold += replace_entries(self, tbl, [(tbl.row_of("F"), 2, "H")], run_time=0.8)
            swing_arcs(self, d, [("F", 1, "H", None)], run_time=min(0.75, c.until("g")))
            c.wait_until("g")
            rg = tbl.row_of("G")
            self.gold += replace_entries(self, tbl, [(rg, 1, "H"), (rg, 2, "H")], run_time=0.9)
            swing_arcs(self, d, [("G", 0, "H", None), ("G", 1, "H", -0.8)], run_time=min(0.9, c.until("delete4")))
            c.wait_until("delete4")
            q2 = S5.quote(Q_DELETE4)
            dims = []
            for k in "KMNP":
                dims += S5.dim_state(tbl, d, k)
            self.play(*swap(self.quote, q2), *during(disappear(self.tag), 0, 0.45),
                      *[FadeOut(b) for b in self.boxes], *dims, *recolor(self.gold, FG), run_time=1.1)  # early: the slide's bullet
            self.quote = q2
            settle(self, d)
            settle(self, tbl)
            delete_rows(self, tbl, "KMNP", run_time=1.2)
            c.wait_until("ten states")
            merge_circles(self, d, [(k, "H") for k in "KMNP"],
                          extra=[bus_trim_after(d, "KMNP"), restyle(d.states["H"], outline=FG),
                                 *self.new_counter(14, 10)],
                          run_time=min(1.5, c.until(floor=0.5) - 0.2))

    # ------------------------------------------------------------ c2: J and L match each other
    def clip2(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.cascade.2") as c:
            self.boxes = [tbl.row_box(tbl.row_of(k), GOLD).set_fill(opacity=0).set_stroke(width=3) for k in "JL"]
            self.play(*[FadeIn(b) for b in self.boxes],
                      *[restyle(d.states[k], outline=GOLD) for k in "JL"], run_time=1.3)
            settle(self, d)
            c.wait_until("both go")
            nxt = [tbl.cell(tbl.row_of(k), j) for k in "JL" for j in (1, 2)]
            self.play(*recolor(nxt, YELLOW), *disappear(self.quote), run_time=1.0)
            c.wait_until("and one")
            ones = [tbl.cell(tbl.row_of(k), 4) for k in "JL"]
            self.play(*recolor(nxt, FG), *flash(ones, color=GREEN, time_width=1.5),
                      *[c1.animate(rate_func=there_and_back).scale(1.5) for c1 in ones], run_time=1.5)
            c.wait_until("noth")
            self.tag = tag("differs from H", FG)
            h0 = tbl.cell(tbl.row_of("H"), 4)
            j1 = tbl.cell(tbl.row_of("J"), 4)
            self.play(FlashAround(h0, color=YELLOW, time_width=1.5), FlashAround(j1, color=GREEN, time_width=1.5),
                      *recolor([h0], YELLOW), *during(appear(self.tag), 0.4, 1.0),  # early: sums up "sets them apart"
                      run_time=1.6)
            c.wait_until("replacel")
            self.quote = S5.quote(Q_REPLACEL)
            self.play(*during(disappear(self.tag), 0, 0.4), *recolor([h0], FG),  # early: the slide's bullet
                      *during(appear(*self.quote, lag=0.15), 0.3, 1.0), run_time=1.3)
            self.gold = replace_entries(self, tbl, [(tbl.row_of("F"), 1, "J")], run_time=1.3)
            swing_arcs(self, d, [("F", 0, "J", None)], run_time=min(1.2, c.until("deletel")))
            c.wait_until("deletel")
            self.play(*[FadeOut(b) for b in self.boxes], *S5.dim_state(tbl, d, "L"),
                      *recolor(self.gold, FG), run_time=0.8)
            settle(self, d)
            settle(self, tbl)
            delete_rows(self, tbl, "L", run_time=1.0)
            merge_circles(self, d, [("L", "J")],
                          extra=[bus_trim_after(d, "L"), restyle(d.states["J"], outline=FG),
                                 *self.new_counter(10, 9)],
                          run_time=min(1.3, c.until(floor=0.5)))

    # ------------------------------------------------------------ c3: new matches D/G and E/F
    def clip3(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.cascade.3") as c:
            p = tbl.pitch
            band = tbl.row_box(0, YELLOW)
            self.play(FadeIn(band), run_time=0.8)
            self.play(band.animate.shift((len(tbl.rows) - 1) * p * DOWN), rate_func=linear,
                      run_time=min(1.4, c.until("dg") - 0.6))
            self.play(FadeOut(band), *disappear(self.quote), run_time=0.6)
            c.wait_until("dg")
            self.boxes = {k: tbl.row_box(tbl.row_of(k), GOLD) for k in "DGEF"}
            self.play(*[FadeIn(self.boxes[k]) for k in "DG"],
                      *[restyle(d.states[k], outline=GOLD) for k in "DG"], run_time=1.5)
            settle(self, d)
            c.wait_until("ef")
            self.play(*[FadeIn(self.boxes[k]) for k in "EF"],
                      *[restyle(d.states[k], outline=GOLD) for k in "EF"], run_time=1.5)
            settle(self, d)
            c.wait_until("new")
            self.tag = tag("new matches", YELLOW)
            self.quote = S5.quote(Q_NEW)
            self.play(*appear(self.tag, *self.quote, lag=0.3), run_time=1.5)  # early: names the new matches; slide line
            c.wait_until("made")
            cells = [[(k, j)] for k, j in [("D", 2)]] + [[("G", 1), ("G", 2)], [("E", 2)], [("F", 1), ("F", 2)]]
            rt = min(2.6, c.until(floor=1.0))
            anims, made = [], []
            for i, group in enumerate(cells):
                a, b = i * rt / 5, i * rt / 5 + 2 * rt / 5
                for k, j in group:
                    cell = tbl.cell(tbl.row_of(k), j)
                    made.append(cell)
                    anims.append(time_span(FlashAround(cell, color=GOLD, time_width=1.5), a, b))
                    anims.append(time_span(cell.animate.set_color(GOLD), a, b))
            self.play(*anims, run_time=rt)
            self.made = made

    # ------------------------------------------------------------ c4: G into D, F into E; seven states
    def clip4(self):
        tbl, d = self.tbl, self.d
        with self.say("c1.cascade.4") as c:
            q = S5.quote(Q_REPLACEGF)
            c.wait_until("by state")
            self.play(*swap(self.quote, q), *during(disappear(self.tag), 0, 0.45),
                      *recolor(self.made, FG), run_time=1.3)  # early: the slide's bullet
            self.quote = q
            c.wait_until("rowc")
            rc = tbl.row_of("C")
            fg = [tbl.cell(rc, 1), tbl.cell(rc, 2)]
            self.play(*flash(fg, color=GOLD, time_width=1.5), *recolor(fg, YELLOW),
                      *[restyle(d.arcs[("C", x)], outline=YELLOW, fill=YELLOW) for x in (0, 1)], run_time=1.2)
            settle(self, d)
            c.wait_until("they become")
            self.gold = replace_entries(self, tbl, [(rc, 1, "E"), (rc, 2, "D")], run_time=1.4)
            swing_arcs(self, d, [("C", 0, "E", 0.0), ("C", 1, "D", 0.5)], run_time=1.4)
            c.wait_until("deletegf")
            dims = S5.dim_state(tbl, d, "G") + S5.dim_state(tbl, d, "F")
            self.play(*[FadeOut(b) for b in self.boxes.values()], *dims, *disappear(self.quote),
                      *recolor(self.gold, FG),
                      *[restyle(d.arcs[("C", x)], outline=FG, fill=FG) for x in (0, 1)], run_time=0.8)
            settle(self, d)
            settle(self, tbl)
            delete_rows(self, tbl, "GF", run_time=1.2)
            merge_circles(self, d, [("G", "D"), ("F", "E")],
                          extra=[restyle(d.states["D"], outline=FG), restyle(d.states["E"], outline=FG),
                                 *self.new_counter(9, 7)],
                          run_time=min(1.3, c.until("check", floor=0.8)))
            c.wait_until("check")
            band = tbl.row_box(0, YELLOW)
            self.play(FadeIn(band), run_time=0.4)
            self.play(band.animate.shift((len(tbl.rows) - 1) * tbl.pitch * DOWN), rate_func=linear,
                      run_time=min(1.6, c.until("nomatch")))
            c.wait_until("nomatch")
            self.play(FadeOut(band), run_time=0.8)
            c.wait_until("seven")
            self.play(*self.new_counter(15, 7), d.animate.shift(DIAG_DROP * DOWN),
                      FlashAround(tbl, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("keeps")
            aside = self.keeps_aside()
            self.play(*appear(*aside.rows, lag=0.3), run_time=1.0)
            c.wait_until("and it can")
            hs = [rw[1] for rw in aside.rows]
            news = [T("D", 30, GOLD).move_to(h) for h in hs]
            anims = []
            for h, n in zip(hs, news):
                anims += [*during([FlashAround(h, color=YELLOW, time_width=1.5)], 0, 0.45), *during(swap(h, n), 0.4, 1.0)]
            self.play(*anims, run_time=1.8)
            c.wait_until("make new")
            self.play(*appear(aside.cap), run_time=1.0)
            c.wait_until("rule")
            s3 = T("3. repeat until no rows match", 28, t2c={"3.": YELLOW})
            s3.move_to([0, S5.CAPTION_Y[1] - 0.5, 0]).align_to([S5.RIGHT_X, 0, 0], LEFT)
            loop = CurvedArrow(s3.get_left() + 0.12 * LEFT, self.cap.step1.get_left() + 0.12 * LEFT,
                               angle=-PI / 2, color=YELLOW, stroke_width=3, tip_length=0.16)
            self.play(*appear(s3), run_time=1.0)
            self.play(Create(loop), run_time=1.2)
            c.wait_until()

    def keeps_aside(self):
        tbl = self.tbl
        xs = [tbl.cell(0, j).get_x() for j in (1, 2, 3, 4)]
        rows = []
        for y in (-0.85, -1.35):
            rows.append(VGroup(*[T(s, 30, GOLD).move_to([x, y, 0]) for s, x in zip("JH00", xs)]))
        g = VGroup(*rows)
        cap = VGroup(T("replacing keeps matches,", 30), T("and can make new ones", 30)).arrange(DOWN, buff=0.15)
        cap.move_to([(xs[0] + xs[3]) / 2, -2.4, 0])
        g.rows, g.cap = rows, cap
        return g


def bus_trim_after(d, names):
    """bus_trim computed as if `names` had already left the bottom row."""
    path = d.bundle[0]
    left = [n for n in S4.LAYERS[3] if n in d.states and n not in names]
    x = max(d.states[n].get_x() for n in left)
    a = S4.POS["A"]
    corners = [[x, path.get_start()[1], 0],
               S5.to_screen([S4.BUS_X, S4.BUS_Y, 0]), S5.to_screen([S4.BUS_X, a[1], 0]),
               S5.to_screen([a[0] - S4.R - 0.7, a[1], 0])]
    new = path.copy()
    new.set_points_as_corners([np.array(c, dtype=float) for c in corners])
    return Transform(path, new)
