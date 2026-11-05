"""Chapter 6, scene 4: Exercise 20.3, both Wachowskis (28 rows, why, DISTINCT). Clips c6.wachowski.1 – c6.wachowski.4.

Exports (static, self-contained):
- edge_grid(row_types, col_types, row_title=None, col_title=None) -> EdgeGrid: the "one edge from each
  side, any pairing" grid. Rows = the left person's edge types (Mono 28 FG, right of an optional PINK
  T 30 row_title), columns = the right person's (Mono 28 FG, optional PINK col_title left of them on
  the header row). Each cell is a DIM box 2.1 x 0.85 holding one YELLOW placement glyph
  (-> ring <-, ch2 s3's stencil hole). GOLD T 44 count "a × b = n" right of the block (buff 0.6).
  Centred on ORIGIN as a whole. Parts: .block (VGroup of all boxes), .cells[i][j] (VGroup(box, glyph)),
  .boxes[i][j], .glyphs[i][j], .row_labels, .col_labels, .row_title, .col_title (None if not given),
  .count. To build it in steps: appear(block + labels), then the glyphs, then the count.
- recap_tile() -> VGroup: The Matrix's 2 x 2 grid, a DIM DISTINCT arrow, and the single row
  "The Matrix  1999": the grid folding into one row. About 9.6 x 2.6 at ORIGIN; scale it down.
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

# ── the edge grid (shared with s5 and the recap) ───────────────────────────────────
GRID_W, GRID_H = 2.1, 0.85


def placement_glyph(color=YELLOW):
    ring = Circle(radius=0.2).set_stroke(color, 4).set_fill(opacity=0)
    kw = dict(buff=0, stroke_width=3, color=color, tip_length=0.14, max_tip_length_to_length_ratio=0.5)
    a1 = Arrow([-0.75, 0, 0], [-0.22, 0, 0], **kw)
    a2 = Arrow([0.75, 0, 0], [0.22, 0, 0], **kw)
    return VGroup(a1, ring, a2)


class EdgeGrid(VGroup):
    """See module docstring."""

    def __init__(self, row_types, col_types, row_title=None, col_title=None):
        super().__init__()
        nr, nc = len(row_types), len(col_types)
        self.boxes, self.glyphs, self.cells = [], [], []
        self.block = VGroup()
        for i in range(nr):
            brow, grow, crow = [], [], []
            for j in range(nc):
                box = Rectangle(width=GRID_W, height=GRID_H).set_stroke(DIM, 2)
                box.move_to([(j - (nc - 1) / 2) * GRID_W, -i * GRID_H, 0])
                g = placement_glyph().move_to(box)
                brow.append(box)
                grow.append(g)
                crow.append(VGroup(box, g))
                self.block.add(box)
            self.boxes.append(brow)
            self.glyphs.append(grow)
            self.cells.append(crow)
        self.row_labels = VGroup(*[Mono(t, 28).next_to(self.boxes[i][0], LEFT, buff=0.25)
                                   for i, t in enumerate(row_types)])
        self.col_labels = VGroup(*[Mono(t, 28).next_to(self.boxes[0][j], UP, buff=0.2)
                                   for j, t in enumerate(col_types)])
        self.row_title = self.col_title = None
        self.count = T(f"{nr} × {nc} = {nr * nc}", 44, GOLD).next_to(self.block, RIGHT, buff=0.6)
        self.add(self.block, *[g for r in self.glyphs for g in r], self.row_labels, self.col_labels,
                 self.count)
        if row_title:
            self.row_title = T(row_title, 30, PINK).next_to(self.row_labels, LEFT, buff=0.35)
            self.add(self.row_title)
        if col_title:
            self.col_title = T(col_title, 30, PINK)
            self.col_title.move_to([self.row_labels.get_right()[0], self.col_labels.get_y(), 0], aligned_edge=RIGHT)
            self.add(self.col_title)
        self.move_to(ORIGIN)


def edge_grid(row_types, col_types, row_title=None, col_title=None):
    return EdgeGrid(row_types, col_types, row_title, col_title)


def recap_tile():
    g = edge_grid(["DIRECTED", "WROTE"], ["DIRECTED", "WROTE"], "Lana", "Lilly")
    arr = Arrow(LEFT * 0.9, RIGHT * 0.9, buff=0, stroke_width=4, color=DIM)
    arr.next_to(g, RIGHT, buff=0.4)
    lab = Mono("DISTINCT", 28, BLUE).next_to(arr, UP, buff=0.15)
    row = VGroup(T("The Matrix", 32), T("1999", 32)).arrange(RIGHT, buff=0.4)
    row.next_to(arr, RIGHT, buff=0.4)
    return VGroup(g, arr, lab, row).move_to(ORIGIN)


# ── this scene's pieces ───────────────────────────────────────────────────────────
CODE_ANY = ("MATCH (lana:Person {name: 'Lana Wachowski'})\n"
            "      --> (m:Movie) <--\n"
            "      (lilly:Person {name: 'Lilly Wachowski'})\n"
            "RETURN m.title;")
CODE_DISTINCT = ("MATCH (lana:Person {name: 'Lana Wachowski'})\n"
                 "      --> (m:Movie) <--\n"
                 "      (lilly:Person {name: 'Lilly Wachowski'})\n"
                 "RETURN DISTINCT m.title, m.year\n"
                 "ORDER BY m.year, m.title;")
CODE_TYPED = ("MATCH (lana:Person {name: 'Lana Wachowski'})\n"
              "      -[:DIRECTED]-> (m:Movie) <-[:DIRECTED]-\n"
              "      (lilly:Person {name: 'Lilly Wachowski'})\n"
              "RETURN m.title, m.year\n"
              "ORDER BY m.year, m.title;")
CODE_TOP = 3.0

REPLY = ["The Matrix", "The Matrix", "Bound", "Bound", "The Matrix Reloaded", "The Matrix Reloaded",
         "V for Vendetta", "Cloud Atlas", "Cloud Atlas", "The Matrix Revolutions",
         "The Matrix Revolutions", "The Matrix Resurrections", "Cloud Atlas", "Cloud Atlas",
         "The Matrix Revolutions", "The Matrix Revolutions", "V for Vendetta", "The Matrix Reloaded",
         "The Matrix Reloaded", "The Matrix", "The Matrix", "The Matrix Resurrections", "The Animatrix",
         "Cloud Atlas", "Cloud Atlas", "Bound", "Bound", "The Matrix Resurrections"]
REPLY_X = [-6.2, -1.6]

PER_MOVIE = [("Bound", "1996", "4"), ("The Matrix", "1999", "4"), ("The Matrix Reloaded", "2003", "4"),
             ("The Matrix Revolutions", "2003", "4"), ("The Animatrix", "2003", "1"),
             ("V for Vendetta", "2005", "2"), ("Cloud Atlas", "2012", "6"),
             ("The Matrix Resurrections", "2021", "3")]
TAB_X, YEAR_X, CNT_X = -4.6, 0.9, 2.4
TAB_Y0, TAB_P = 1.65, 0.42

G_Y = 1.25                      # the per-movie graph's row
LANA_C, MOVIE_C, LILLY_C = np.array([-4.6, G_Y, 0]), np.array([0, G_Y, 0]), np.array([4.6, G_Y, 0])
P_R, M_R = 0.55, 0.6
GRID_TOP = -0.6
COUNT_C = np.array([4.75, -1.25, 0])


def rot(v, a):
    c, s = np.cos(a), np.sin(a)
    return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1], 0])


def arc_edge(a, ra, b, rb, angle, color=FG, width=3):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    u = (b - a) / np.linalg.norm(b - a)
    s, e = a + rot(u, -angle / 2) * ra, b - rot(u, angle / 2) * rb
    line = Line(s, e) if abs(angle) < 1e-6 else ArcBetweenPoints(s, e, angle=angle)
    line.set_stroke(color, width)
    line.add_tip(tip_length=0.2, tip_width=0.18)
    line.tip.set_fill(color, 1).set_stroke(color, 0)
    return line


def tinted(r, color, center):
    return Circle(radius=r).set_stroke(color, 4).set_fill(
        interpolate_color(ManimColor(BG), ManimColor(color), 0.22), 1).move_to(center)


def person(name, center):
    return VGroup(tinted(P_R, PINK, center), T(name, 28).move_to(center))


ANGLES = {1: [0.0], 2: [0.9, -0.9], 3: [1.2, 0.0, -1.2]}


def fan(src, dst, types, flip):
    """Arcs src -> dst, one per type; returns (arcs, labels) ordered top to bottom."""
    arcs = [arc_edge(src, P_R, dst, M_R, (-a if flip else a)) for a in ANGLES[len(types)]]
    arcs.sort(key=lambda m: -m.point_from_proportion(0.5)[1])
    labels = []
    for a, t in zip(arcs, types):
        m = Mono(t, 28).move_to(a.point_from_proportion(0.5))
        labels.append(VGroup(BackgroundRectangle(m, color=BG, fill_opacity=1, buff=0.08), m))
    return arcs, labels


def movie_graph(title, lana_types, lilly_types):
    g = VGroup()
    g.lana, g.lilly = person("Lana", LANA_C), person("Lilly", LILLY_C)
    g.movie = tinted(M_R, BLUE, MOVIE_C)
    g.title = T(title, 34).move_to(MOVIE_C + UP * 1.4)
    g.arcs_l, g.labs_l = fan(LANA_C, MOVIE_C, lana_types, flip=True)
    g.arcs_r, g.labs_r = fan(LILLY_C, MOVIE_C, lilly_types, flip=False)
    g.add(*g.arcs_l, *g.arcs_r, g.lana, g.lilly, g.movie, g.title, *g.labs_l, *g.labs_r)
    return g


def placed_grid(lana_types, lilly_types):
    g = edge_grid(lana_types, lilly_types, "Lana", "Lilly")
    g.shift([-0.4 - g.block.get_x(), GRID_TOP - g.block.get_top()[1], 0])
    g.count.move_to(COUNT_C)
    return g


def pause_icon(next_to):
    return load_scene("ch6_s1_intro").pause_icon().next_to(next_to, RIGHT, buff=0.45)


def mini_doc():
    box = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.0).set_stroke(TEAL, 3).set_fill(TEAL, 0.05)
    box.move_to([-3.4, -2.85, 0])
    bars = VGroup(*[Line(ORIGIN, RIGHT * w).set_stroke(DIM, 6) for w in (1.2, 0.9, 1.0)])
    bars.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(box)
    title = T("Lecture 4", 28, TEAL).next_to(box, LEFT, buff=0.3)
    return VGroup(box, title), list(bars)


class Wachowski(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── clip 1: the card ─────────────────────────────────────────────────────────
    def clip1(self):
        ex = load_scene("ch5_s7_exercises")
        with self.say("c6.wachowski.1") as c:
            cards = ex.exercise_cards().scale(1.2).move_to(ORIGIN)
            self.play(*appear(cards, shift=None), run_time=0.4)  # early: the exercise row, shown whole
            panel = ex.exercise_panel("20.3")
            card = cards[2]
            self.play(*during([ReplacementTransform(card.box.copy(), panel.frame)], 0, 0.7),
                      *during([FadeOut(cards)], 0.15, 0.7),
                      *during(appear(panel.title), 0.6, 1.0), run_time=1.3)
            c.wait_until(own_word=panel.question[0])
            self.play(*appear(panel.qgrp, shift=0.15 * DOWN), run_time=1.0)  # early: the question, shown whole
            c.wait_until("stop")
            icon = pause_icon(panel.title)
            self.play(*appear(icon, shift=None), run_time=0.8)
        self.panel, self.icon = panel, icon

    # ── clip 2: the query, the drawing, 28 rows ─────────────────────────────────
    def clip2(self):
        panel = self.panel
        with self.say("c6.wachowski.2") as c:
            tag = panel.title
            tag.generate_target()
            tag.target.scale(0.6).to_corner(UL, buff=0.5)
            self.play(*during(disappear(panel.frame, panel.qgrp, self.icon), 0, 0.5),
                      *during([MoveToTarget(tag)], 0.25, 1.0), run_time=1.1)
            self.tag = tag
            code = Code(CODE_ANY, size=28)
            code.move_to([0, 0, 0]).align_to([0, CODE_TOP, 0], UP)
            self.play(*appear(code, shift=None), run_time=1.0)  # early: the query, shown whole
            c.wait_until("leave the type out")
            self.play(*flash([code.find("-->"), code.find("<--")], color=YELLOW, run_time=1.4,
                             time_width=1.5), run_time=1.4)

            c.wait_until("arrows")
            dy = -1.0
            lana = person("Lana", [-4.0, dy, 0])
            lilly = person("Lilly", [4.0, dy, 0])
            hole = Circle(radius=0.6).set_stroke(BLUE, 5).set_fill(opacity=0).move_to([0, dy, 0])
            hname = Mono("m", 32, BLUE).move_to(hole)
            a1 = Arrow(lana[0].get_right(), hole.get_left(), buff=0.12, stroke_width=4, color=FG,
                       max_tip_length_to_length_ratio=0.12)
            a2 = Arrow(lilly[0].get_left(), hole.get_right(), buff=0.12, stroke_width=4, color=FG,
                       max_tip_length_to_length_ratio=0.12)
            self.play(*appear(lana, lilly, hole, hname, shift=None, lag=0.15), run_time=1.0)
            self.play(GrowArrow(a1), GrowArrow(a2), run_time=1.4)
            drawing = [lana, lilly, hole, hname, a1, a2]

            c.wait_until("last lecture")
            doc, bars = mini_doc()
            self.play(*appear(doc, *bars, shift=None, lag=0.05), run_time=0.8)  # early: a tiny Lecture 4 card, gone at once
            new_bar = Line(ORIGIN, RIGHT * 0.7).set_stroke(YELLOW, 6).move_to(bars[0], aligned_edge=LEFT)
            c.wait_until("change of name")
            self.play(bars[0].animate.set_stroke(YELLOW), run_time=0.5)
            self.play(*swap(bars[0], new_bar, shift=None), run_time=0.9)
            self.play(*disappear(doc, new_bar, bars[1], bars[2]), run_time=0.7)

            c.wait_until("run")
            header = Mono("m.title", 28, DIM).move_to([0, 2.98, 0]).align_to([REPLY_X[0], 0, 0], LEFT)
            rows = []
            for k, t in enumerate(REPLY):
                col, i = divmod(k, 14)
                rows.append(T(t, 28).move_to([0, 2.45 - 0.38 * i, 0]).align_to([REPLY_X[col], 0, 0], LEFT))
            n28 = T("28 rows", 44, GOLD).move_to([4.9, 0.45, 0])
            sweep_clear(self, *appear(header, *rows, shift=None, lag=0.04), keep=[tag], run_time=2.2)  # early: the reply, printed whole
            c.wait_until(own_word=n28)
            self.play(*appear(n28), run_time=0.9)

            c.wait_until("the matrix appears")
            tm = [r for r, t in zip(rows, REPLY) if t == "The Matrix"]
            ca = [r for r, t in zip(rows, REPLY) if t == "Cloud Atlas"]
            self.play(*recolor(tm, YELLOW), *flash(tm, run_time=1.2), run_time=1.2)
            c.wait_until("cloud atlas")
            self.play(*recolor(ca, YELLOW), *flash(ca, run_time=1.2), run_time=1.2)
        self.rows, self.header, self.n28 = rows, header, n28

    # ── clip 3: why, the grids, the sum ─────────────────────────────────────────
    def clip3(self):
        rows, n28 = self.rows, self.n28
        with self.say("c6.wachowski.3") as c:
            why = T("why?", 44, GOLD).next_to(n28, DOWN, buff=0.45)
            self.play(*appear(why), run_time=0.8)

            c.wait_until("matrix")
            G = movie_graph("The Matrix", ["DIRECTED", "WROTE"], ["DIRECTED", "WROTE"])
            first = rows[0]
            others = [r for r in rows[1:]] + [self.header, n28, why]
            self.play(*disappear(*others), first.animate.set_color(FG), run_time=0.9)
            self.play(first.animate.scale(34 / 28).move_to(G.title), run_time=1.2)
            self.remove(first)
            self.add(G.title)
            self.play(*appear(G.lana, G.movie, G.lilly, shift=None, lag=0.15),  # early: the sisters' names on "each sister"
                      *[GrowFromPoint(a, a.get_start()) for a in G.arcs_l + G.arcs_r], run_time=1.4)
            c.wait_until("directed it")
            self.play(*appear(*G.labs_l, *G.labs_r, lag=0.1), run_time=1.0)

            c.wait_until("grid")
            g = placed_grid(["DIRECTED", "WROTE"], ["DIRECTED", "WROTE"])
            self.play(*appear(g.block, g.row_labels, g.col_labels, g.row_title, g.col_title,  # early: the empty grid, its headers
                              shift=None, lag=0.1), run_time=1.2)
            self.fill_grid(g, G, [1.4, 0.9, 0.8, 0.8])
            c.wait_until("times two")
            self.play(*appear(g.count), *flash([g.count], color=GOLD, run_time=1.2), run_time=1.2)
            c.wait_until("part four")
            rule = T("choices multiply", 36, YELLOW).move_to(COUNT_C + DOWN * 1.0)
            ptag = T("part 4", 28, DIM).next_to(rule, DOWN, buff=0.2)
            self.play(*appear(rule, ptag, lag=0.3), run_time=1.1)  # early: "part four" names the tag

            c.wait_until("cloud")
            G, g = self.change_movie(c, G, g, "Cloud Atlas", ["DIRECTED", "PRODUCED", "WROTE"],
                                     ["DIRECTED", "WROTE"], "three times two", 1.6)
            c.wait_until("animatrix")
            G, g = self.change_movie(c, G, g, "The Animatrix", ["WROTE"], ["WROTE"], "one times one", 1.3)

            c.wait_until("sum")
            tab = self.build_table()
            sweep_clear(self, *appear(*tab["all"], shift=None, lag=0.05), keep=[self.tag], run_time=1.3)  # early: the per-movie table, shown whole
            self.play(GrowFromCenter(tab["brace"]), *appear(tab["sum"], shift=None),
                      run_time=min(1.0, max(0.5, c.until(None) - 0.05)))
        self.tab = tab

    def fill_grid(self, g, G, times):
        k = 0
        for i in range(len(g.glyphs)):
            for j in range(len(g.glyphs[0])):
                rt = times[min(k, len(times) - 1)]
                fl = [VShowPassingFlash(a.copy().set_stroke(YELLOW, 7), time_width=0.6, run_time=rt)
                      for a in (G.arcs_l[i], G.arcs_r[j])]
                self.play(*appear(g.glyphs[i][j], shift=None), *fl, run_time=rt)
                k += 1

    def change_movie(self, c, G, g, title, lt, rt_types, count_cue, times):
        G2 = movie_graph(title, lt, rt_types)
        g2 = placed_grid(lt, rt_types)
        olds = [*G.arcs_l, *G.arcs_r, *G.labs_l, *G.labs_r, g.block, *[x for r in g.glyphs for x in r],
                g.row_labels, g.col_labels, g.row_title, g.col_title, g.count]
        self.play(*during(disappear(*olds), 0, 0.5),
                  *swap(G.title, G2.title), run_time=0.9)
        glyphs = [x for r in g2.glyphs for x in r]
        self.play(*during([GrowFromPoint(a, a.get_start()) for a in G2.arcs_l + G2.arcs_r], 0, 0.45),  # early: the new movie's edges and grid
                  *during(appear(*G2.labs_l, *G2.labs_r, g2.block, g2.row_labels, g2.col_labels,
                                 g2.row_title, g2.col_title, shift=None, lag=0.05), 0.2, 0.6),
                  *during(appear(*glyphs, shift=None, lag=0.15), 0.6, 1.0), run_time=times)
        c.wait_until(count_cue)
        self.play(*appear(g2.count), *flash([g2.count], color=GOLD, run_time=1.0), run_time=1.0)
        return G2, g2

    def build_table(self):
        hdr = VGroup(Mono("m.title", 28, DIM).move_to([0, TAB_Y0 + 0.55, 0]).align_to([TAB_X, 0, 0], LEFT),
                     Mono("m.year", 28, DIM).move_to([YEAR_X, TAB_Y0 + 0.55, 0]),
                     Mono("rows", 28, DIM).move_to([CNT_X, TAB_Y0 + 0.55, 0]))
        titles, years, counts = [], [], []
        for i, (t, y, n) in enumerate(PER_MOVIE):
            yy = TAB_Y0 - TAB_P * i
            titles.append(T(t, 30).move_to([0, yy, 0]).align_to([TAB_X, 0, 0], LEFT))
            years.append(T(y, 30).move_to([YEAR_X, yy, 0]))
            counts.append(T(n, 30, GOLD).move_to([CNT_X, yy, 0]))
        top = titles[0].get_top()[1] + 0.05
        bot = titles[-1].get_bottom()[1] - 0.05
        brace = Brace(Line([CNT_X, top, 0], [CNT_X, bot, 0]), direction=RIGHT, buff=0.45, color=GOLD)
        s = T("28", 48, GOLD).next_to(brace, RIGHT, buff=0.25)
        rowsg = [VGroup(a, b, d) for a, b, d in zip(titles, years, counts)]
        return {"hdr": hdr, "titles": titles, "years": years, "counts": counts, "brace": brace,
                "sum": s, "all": [hdr, *rowsg], "rows": rowsg}

    # ── clip 4: DISTINCT, and the typed trap ───────────────────────────────────
    def clip4(self):
        tab = self.tab
        with self.say("c6.wachowski.4") as c:
            # the table drops to make room for the query
            code = Code(CODE_ANY, size=28)
            code.move_to([0, 0, 0]).align_to([0, CODE_TOP, 0], UP)
            down = 1.55 * DOWN
            self.play(*during(disappear(tab["hdr"]), 0, 0.4),
                      *during([r.animate.shift(down) for r in tab["rows"]] +
                              [tab["brace"].animate.shift(down), tab["sum"].animate.shift(down)], 0.2, 0.75),
                      *during(appear(code, shift=None), 0.6, 1.0), run_time=1.4)
            for r in tab["rows"]:
                self.remove(*r.get_family())
            self.add(*tab["titles"], *tab["years"], *tab["counts"])
            code2 = Code(CODE_DISTINCT, size=28)
            code2.move_to([0, 0, 0]).align_to([0, CODE_TOP, 0], UP)
            self.play(*edit(code, code2), run_time=1.5)
            self.play(*flash([code2.find("DISTINCT")], color=YELLOW, run_time=1.0), run_time=1.0)

            # each grid folds to one row: the counts go, 28 -> 8 rows, The Animatrix takes its title order
            n8 = T("8 rows", 44, GOLD).move_to(tab["sum"], aligned_edge=LEFT)
            new_anim = VGroup(tab["titles"][4].copy(), tab["years"][4].copy()).shift(UP * 2 * TAB_P)
            self.play(*during(disappear(*tab["counts"], tab["brace"]), 0, 0.4),
                      *swap(tab["sum"], n8), run_time=1.2)
            self.play(*during([FadeOut(tab["titles"][4]), FadeOut(tab["years"][4])], 0, 0.35),
                      *during([m.animate.shift(DOWN * TAB_P) for k in (2, 3)
                               for m in (tab["titles"][k], tab["years"][k])], 0.3, 0.7),
                      *during([FadeIn(new_anim)], 0.7, 1.0), run_time=1.4)
            order = [0, 1, None, 2, 3, 5, 6, 7]
            lines = []
            for k in order:
                if k is None:
                    lines.append(new_anim)
                else:
                    lines.append(VGroup(tab["titles"][k], tab["years"][k]))

            c.wait_until("bound")
            self.play(*flash([lines[0]], run_time=1.0), run_time=1.0)
            c.wait_until("resurrections")
            self.play(*flash([lines[7]], run_time=1.0), run_time=1.0)

            c.wait_until("typed")
            code3 = Code(CODE_TYPED, size=28)
            code3.move_to([0, 0, 0]).align_to([0, CODE_TOP, 0], UP)
            self.play(*edit(code2, code3), run_time=1.6)
            c.wait_until("finds five")
            n5 = T("5 rows", 44, GOLD).move_to(n8, aligned_edge=LEFT)
            self.play(*swap(n8, n5), run_time=1.0)  # early: its word is "five"
            for cue, k, nth in (("vendetta", 5, 0), ("animatrix", 2, 0), ("resurrections", 7, 1)):
                c.wait_until(cue, nth=nth)
                self.play(*recolor(list(lines[k]), RED), run_time=0.8)

            c.wait_until("lesson")
            a = tinted(0.55, PINK, [-2.6, 0.5, 0])
            b = tinted(0.6, BLUE, [2.6, 0.5, 0])
            arcs = [arc_edge(a.get_center(), 0.55, b.get_center(), 0.6, ang) for ang in (1.0, 0.0, -1.0)]
            cap = T("several edges between two vertices", 40).move_to([0, -1.4, 0])
            cap2 = T("expect repeated rows", 40, YELLOW).move_to([0, -2.2, 0])
            sweep_clear(self, *appear(a, b, shift=None), *[GrowFromPoint(x, x.get_start()) for x in arcs],
                        run_time=1.4)
            self.play(*appear(cap, cap2, lag=0.4), run_time=1.2)  # early: the closing rule, read as one line
