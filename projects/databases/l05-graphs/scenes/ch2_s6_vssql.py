"""Chapter 2, scene 6: Cypher next to SQL (Slide 105), piece by piece. Clips c2.sql.1 – c2.sql.5.

Layout: the two queries are stacked (Cypher on top, SQL below): side by side, the 13-unit SQL and
the 11-unit Cypher can't both be read at >= 28.

Exports: edge_join_panel() (for the recap's r5): the YELLOW `-[:DIRECTED]->` with a PINK tail dot and
a BLUE head dot, linked to `has_position AS hp` (YELLOW) and the two ON conditions (PINK / BLUE),
centred at ORIGIN, ~8.6 x 2.8. Parts: .arrow (Code), .tail, .head (Dots), .lines (3 Codes), .links.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch2_s1_hook")
S4 = load_scene("ch2_s4_edge")
C1S2 = load_scene("ch1_s2_lasttime")
C1S4 = load_scene("ch1_s4_propgraph")

CY_SRC = "MATCH (p:Person {name: 'Steven Spielberg'})\n      -[:DIRECTED]-> (m:Movie)\nRETURN m.title, m.year;"
CY_Y, SQL_Y = 2.72, -0.5
DOT_R = 0.09


def cypher():
    return Code(CY_SRC, size=30).move_to([0, CY_Y, 0])


def sql():
    return S1.sql_block().move_to([0, SQL_Y, 0])


def bot(m):
    return m.get_bottom() + 0.06 * DOWN


def top(m):
    return m.get_top() + 0.06 * UP


def connector(a, b, color):
    return Line(a, b, stroke_width=3, color=color).set_z_index(-2)


def route(points, color):
    """A right-angled connector through the given points (kept behind the text)."""
    pts = [np.array([x, y, 0.0]) for x, y in points]
    return VMobject().set_points_as_corners(pts).set_stroke(color, 3).set_z_index(-2)


def mid(a, b):
    return (a + b) / 2


def end_dots(arrow_glyphs):
    a, b = arrow_glyphs[0], arrow_glyphs[-1]
    tail = Dot([a.get_left()[0] - 0.16, a.get_y(), 0], radius=DOT_R, color=PINK)
    head = Dot([b.get_right()[0] + 0.16, b.get_y(), 0], radius=DOT_R, color=BLUE)
    return tail, head


def outline(piece, color):
    return RoundedRectangle(corner_radius=0.2, width=piece.width + 0.3, height=0.5) \
        .move_to(piece).set_stroke(color, 4)


def edge_join_panel():
    """The edge as a join: arrow + end dots over has_position AS hp and the two ON conditions."""
    arrow = Code("-[:DIRECTED]->", size=40)
    arrow.text.set_color(YELLOW)
    srcs = ["has_position AS hp", "ON hp.person_id = p.person_id", "ON m.movie_id = hp.movie_id"]
    lines = [Code(s, size=32, lang="sql") for s in srcs]
    for ln, col in zip(lines, (YELLOW, PINK, BLUE)):
        ln.text.set_color(col)
    block = VGroup(*lines).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    arrow.next_to(block, UP, buff=0.75)
    tail, head = end_dots(arrow.text)
    ya = arrow.get_y()
    xl, xr = block.get_left()[0] - 0.4, block.get_right()[0] + 0.4
    mid = Line(arrow.get_bottom() + 0.08 * DOWN, lines[0].get_top() + 0.08 * UP)
    tl = VMobject().set_points_as_corners([tail.get_center() + 0.1 * LEFT, [xl, ya, 0],
                                           [xl, lines[1].get_y(), 0],
                                           [lines[1].get_left()[0] - 0.12, lines[1].get_y(), 0]])
    hl = VMobject().set_points_as_corners([head.get_center() + 0.1 * RIGHT, [xr, ya, 0],
                                           [xr, lines[2].get_y(), 0],
                                           [lines[2].get_right()[0] + 0.12, lines[2].get_y(), 0]])
    for ln, col in ((mid, YELLOW), (tl, PINK), (hl, BLUE)):
        ln.set_stroke(col, 3)
    links = VGroup(mid, tl, hl)
    g = VGroup(links, arrow, tail, head, *lines)
    g.move_to(ORIGIN)
    g.arrow, g.tail, g.head, g.lines, g.links = arrow, tail, head, lines, links
    return g


def table_box(src):
    """ch1's table-card look: BLUE rounded box, stroke 3, faint BLUE fill."""
    c = Code(src, size=28, lang="sql")
    box = RoundedRectangle(corner_radius=0.12, width=c.width + 0.6, height=0.85)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.06).move_to(c)
    g = VGroup(box, c)
    g.box, g.code = box, c
    return g


def generic_schematic():
    cards = [table_box(s) for s in ("vertices AS p", "edges AS e", "vertices AS m")]
    row = VGroup(*cards).arrange(RIGHT, buff=1.2)
    links = [Line(cards[i].get_right(), cards[i + 1].get_left()).set_stroke(TEAL, 4) for i in range(2)]
    l0 = Code("ON e.tail_vertex = p.vertex_id", size=28, lang="sql").next_to(links[0], UP, buff=0.7)
    l1 = Code("ON m.vertex_id = e.head_vertex", size=28, lang="sql").next_to(links[1], DOWN, buff=0.7)
    g = VGroup(*cards, *links, l0, l1)
    g.cards, g.links, g.labels = cards, links, [l0, l1]
    return g


def results(tool, cy_):
    rows = VGroup(*[S4.result_row(t, y, size=28) for t, y in S4.LIMIT4])
    rows.arrange(DOWN, buff=0.2)
    bar_x = select(rows[0], "│")[0].get_x()
    for r in rows:
        r.shift((bar_x - select(r, "│")[0].get_x()) * RIGHT)
    rows.shift((-3.0 - rows.get_left()[0]) * RIGHT).set_y(cy_)
    lab = T(tool, 32)
    n = T("28 rows", 32, GOLD)
    labs = VGroup(lab, n).arrange(DOWN, buff=0.2).move_to([-5.0, cy_, 0])
    g = VGroup(lab, n, rows)
    g.lab, g.n, g.rows = lab, n, rows
    return g


def model_icons():
    t = C1S2.mini_table("tables")
    d = C1S2.mini_doc("trees")
    gr = C1S4.tiny_graph()
    gr.scale_to_fit_height(1.2)
    gt = T("graphs", 30, PINK)
    gt.next_to(gr, UP, buff=0.15)
    gi = VGroup(gt, gr)
    for ic, title in ((t, t[1]), (d, d[1]), (gi, gt)):
        body = VGroup(*[m for m in ic if m is not title])
        body.scale(0.7)
        title.next_to(body, UP, buff=0.12)
    row = VGroup(t, d, gi).arrange(RIGHT, buff=1.6, aligned_edge=UP)
    row.move_to([0, -2.85, 0])
    row.graph = gi
    return row


class CypherVsSql(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(4.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # spotlight: lit glyphs at full opacity (recoloured if a colour is given), the rest dimmed
    def spot(self, lit):
        want = {}
        for grp, col in lit:
            for g in grp:
                want[id(g)] = col
        anims = []
        for code in (self.cy, self.sql):
            for g in code.text:
                if id(g) in want:
                    col = want[id(g)]
                    anims.append(g.animate.set_fill(col, opacity=1) if col else g.animate.set_fill(opacity=1))
                elif g.get_fill_opacity() > DIMMED + 0.01:
                    anims.append(g.animate.set_fill(opacity=DIMMED))
        return anims

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        cy, sq = cypher(), sql()
        self.cy, self.sql = cy, sq
        ret, sel = cy.find("RETURN m.title, m.year"), sq.find("SELECT m.title, m.year")
        per, ppl, pname = (cy.find("(p:Person {name: 'Steven Spielberg'})"), sq.find("people AS p"),
                           sq.find("p.name = 'Steven Spielberg'"))
        mov, mvs = cy.find("(m:Movie)"), sq.find("movies AS m")
        self.lit1 = [(ret, GREEN), (sel, GREEN), (per, PINK), (ppl, PINK), (pname, PINK), (mov, BLUE), (mvs, BLUE)]
        k_ret = connector(bot(ret), top(sel), GREEN)
        k_p1 = connector(bot(per), top(ppl), PINK)
        k_p2 = connector(bot(per) + 0.6 * RIGHT, top(pname), PINK)
        # (m:Movie) -> movies AS m: down into the gap between the queries, through the word gap after
        # SELECT, then down the free column after FROM / JOIN to the left edge of `movies AS m`
        yb = mid(cy.line(2).get_bottom()[1], sq.line(0).get_top()[1])
        x_gap = mid(sq.find("SELECT").get_right()[0], sq.find("m.title", line=0).get_left()[0])
        y01 = mid(sq.find("SELECT").get_bottom()[1], sq.find("FROM").get_top()[1])
        xg = mid(sq.find("JOIN", line=3).get_right()[0], mvs.get_left()[0])
        k_m = route([(mov.get_x(), mov.get_bottom()[1] - 0.06), (mov.get_x(), yb), (x_gap, yb), (x_gap, y01),
                     (xg, y01), (xg, mvs.get_y()), (mvs.get_left()[0] - 0.06, mvs.get_y())], BLUE)

        with self.say("c2.sql.1") as c:
            self.play(*appear(cy, sq, shift=None, lag=0.5), run_time=1.6)  # early: both queries shown whole, then walked
            c.wait_until("return")
            self.play(*self.spot([(ret, GREEN), (sel, GREEN)]), Create(k_ret), run_time=1.4)
            c.wait_until("person")
            self.play(*self.spot([(per, PINK), (ppl, PINK), (pname, PINK)]), FadeOut(k_ret),
                      Create(k_p1), Create(k_p2), run_time=1.5)
            c.wait_until("movie")
            self.play(*self.spot([(mov, BLUE), (mvs, BLUE)]), FadeOut(k_p1), FadeOut(k_p2),
                      Create(k_m), run_time=1.4)
        self.k_m = k_m

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        cy, sq = self.cy, self.sql
        arr = cy.find("-[:DIRECTED]->")
        hp = sq.find("has_position AS hp")
        on1 = sq.find("ON hp.person_id = p.person_id")
        on2 = sq.find("ON m.movie_id = hp.movie_id")
        typ, pos = cy.find(":DIRECTED"), sq.find("hp.position = 'director'")
        q = T("?", 64, GOLD).move_to([3.8, 1.5, 0])
        tail, head = end_dots(arr)
        # lanes in the free space: yc between Cypher lines 1 and 2, yb between the queries,
        # xl / xr outside the SQL, yd under it; xc just left of the Cypher block
        yc = mid(cy.line(1).get_bottom()[1], cy.line(2).get_top()[1])
        yb = mid(cy.line(2).get_bottom()[1], sq.line(0).get_top()[1])
        xl, xr = sq.get_left()[0] - 0.28, sq.get_right()[0] + 0.28
        yd = sq.get_bottom()[1] - 0.3
        xc = cy.line(2).get_left()[0] - 0.35
        x_out = cy.line(2).get_right()[0] + 0.4
        x_hp = mid(sq.line(0).get_right()[0], hp.get_right()[0])
        y_on2 = on2.get_y()
        k_hp = route([(arr.get_x(), arr.get_bottom()[1] - 0.04), (arr.get_x(), yc), (x_out, yc), (x_out, yb),
                      (x_hp, yb), (x_hp, top(hp)[1])], YELLOW)
        k_tail = route([(tail.get_left()[0], tail.get_y()), (xc, tail.get_y()), (xc, yb),
                        (on1.get_x(), yb), (on1.get_x(), top(on1)[1])], PINK)
        k_head = route([(head.get_x(), head.get_bottom()[1]), (head.get_x(), yc), (xr, yc), (xr, y_on2),
                        (on2.get_right()[0] + 0.06, y_on2)], BLUE)
        k_typ = route([(typ.get_x(), typ.get_bottom()[1] - 0.04), (typ.get_x(), yc), (xl, yc), (xl, yd),
                       (pos.get_x(), yd), (pos.get_x(), bot(pos)[1])], YELLOW)
        lit = [(arr, YELLOW)]

        with self.say("c2.sql.2") as c:
            self.play(*self.spot(lit), FadeOut(self.k_m), *appear(q), run_time=1.4)
            c.wait_until("row")
            lit.append((hp, YELLOW))
            self.play(*self.spot(lit), Create(k_hp), run_time=1.5)
            c.wait_until("ends")
            self.play(*disappear(q), GrowFromCenter(tail), GrowFromCenter(head), run_time=1.0)
            self.play(FlashAround(tail, color=PINK, run_time=1.0), FlashAround(head, color=BLUE, run_time=1.0))
            c.wait_until("tail")
            lit.append((on1, PINK))
            self.play(*self.spot(lit), *during([FadeOut(k_hp)], 0, 0.45), *during([Create(k_tail)], 0.3, 1),
                      run_time=1.6)
            c.wait_until("head")
            lit.append((on2, BLUE))
            self.play(*self.spot(lit), Create(k_head), run_time=1.4)
            c.wait_until("type")
            self.play(*self.spot(lit + [(pos, YELLOW)]), Create(k_typ),
                      FlashAround(typ, run_time=1.5, time_width=1.5), run_time=1.5)
        self.edge_parts = (arr, hp, on1, on2)
        self.dots = (tail, head)
        self.ks = [k_tail, k_head, k_typ]

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        cy, sq = self.cy, self.sql
        arr, hp, on1, on2 = self.edge_parts
        tail, head = self.dots
        keep = {id(g) for grp in self.edge_parts for g in grp}
        panel = edge_join_panel().move_to([0, 1.45, 0])
        cap = T("An edge in a pattern ≈ a join with has_position", 36).move_to([0, 3.35, 0])
        sch = generic_schematic().move_to([0, -2.05, 0])

        with self.say("c2.sql.3") as c:
            gone = [g.animate.set_fill(opacity=0) for code in (cy, sq) for g in code.text if id(g) not in keep]
            self.play(*during(gone + [FadeOut(k) for k in self.ks], 0, 0.5),
                      *during(appear(cap), 0.5, 1), run_time=1.4)
            windows = [(0.0, 0.55), (0.15, 0.65), (0.3, 0.8), (0.45, 0.95)]
            moves = []
            for (a, b), src, dst in zip(windows, self.edge_parts, [panel.arrow, *panel.lines]):
                moves += during(fly(src, dst), a, b)
                moves += during([g.animate.set_fill(opacity=0) for g in src], a + 0.05, a + 0.3)
            moves += during([ReplacementTransform(tail, panel.tail), ReplacementTransform(head, panel.head)],
                            0.0, 0.55)
            moves += during(Create(panel.links), 0.8, 1.0)
            self.play(*moves, run_time=min(2.4, c.until("generic")))
            self.remove(*cy.get_family(), *sq.get_family())
            settle(self, panel)
            c.wait_until("generic")
            self.play(*appear(*sch.cards, shift=None, lag=0.3), run_time=1.3)  # early: schematic of the two tables
            self.play(*[Create(l) for l in sch.links], *appear(*sch.labels, lag=0.3), run_time=1.3)  # early: join conditions
            c.wait_until("edges")
            self.play(FlashAround(sch.cards[1], run_time=1.2, time_width=1.5))
            c.wait_until("then with vertices")
            self.play(FlashAround(sch.cards[0], run_time=1.0, time_width=1.5),
                      FlashAround(sch.cards[2], run_time=1.0, time_width=1.5))
            c.wait_until("same")
            top_r = results("cypher-shell", 1.65)
            bot_r = results("DuckDB", -1.75)
            sweep_clear(self, *appear(top_r, shift=None), run_time=1.6)  # early: result panel with its tool
            c.wait_until("Duck D B")
            self.play(*appear(bot_r, shift=None), run_time=1.2)  # early: result panel with its tool
            self.play(*flash([top_r.n, bot_r.n], color=GOLD, run_time=1.4, time_width=1.5))

    # ------------------------------------------------------------------ clip 4
    def clip4(self):
        cy, sq = cypher(), sql()
        self.cy, self.sql = cy, sq
        tabs = [sq.find("people AS p"), sq.find("has_position AS hp"), sq.find("movies AS m")]
        s_1 = CurvedArrow(tabs[0].get_right() + 0.15 * RIGHT, tabs[1].get_corner(UR) + [-0.4, 0.08, 0],
                          angle=-0.6 * PI, color=YELLOW, stroke_width=4, tip_length=0.18)
        s_2 = CurvedArrow(tabs[1].get_left() + 0.12 * LEFT, tabs[2].get_left() + 0.12 * LEFT,
                          angle=0.9 * PI, color=YELLOW, stroke_width=4, tip_length=0.18)
        diag = S1.join_diagram()
        diag.shift((-3.05 - diag.boxes[0].get_y()) * UP)
        targets = [outline(cy.find("(p:Person {name: 'Steven Spielberg'})"), PINK),
                   outline(cy.find("-[:DIRECTED]->"), YELLOW),
                   outline(cy.find("(m:Movie)"), BLUE)]
        cap = T("the query is the diagram", 40).move_to([0, -2.95, 0])

        with self.say("c2.sql.4") as c:
            c.wait_until("a matter of")
            sweep_clear(self, *appear(cy, sq, shift=None, lag=0.3), run_time=1.8)  # early: the two queries again
            c.wait_until("draw")
            self.play(Create(s_1), Create(s_2), lag_ratio=0.5, run_time=1.6)
            c.wait_until("carefully")
            self.play(*flash(tabs, run_time=1.4, time_width=1.5),
                      *during(appear(*[m for bn in zip(diag.boxes, diag.names) for m in bn], shift=None, lag=0.15),
                              0.2, 1), run_time=1.6)  # early: the sketch is built from the FROM/JOIN tables
            c.wait_until("joined to what")
            self.play(ReplacementTransform(s_1, diag.links[0]), ReplacementTransform(s_2, diag.links[1]),
                      *during(appear(*diag.keys, lag=0.3), 0.5, 1),
                      run_time=min(1.6, c.until("diagram")))  # early: link keys
            c.wait_until("diagram")
            leave = [FadeOut(m) for m in (*diag.names, *diag.keys, *diag.links)]
            self.play(*during(leave, 0, 0.35), *during(set_alpha([sq], 0.3), 0, 0.3),
                      *during([ReplacementTransform(b, t) for b, t in zip(diag.boxes, targets)], 0.25, 1),
                      run_time=2.2)
            self.remove(*diag.get_family())
            self.add(*targets)
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.2)
        self.targets, self.cap = targets, cap

    # ------------------------------------------------------------------ clip 5
    def clip5(self):
        cy, sq = self.cy, self.sql
        icons = model_icons()
        mv = self.targets[2]
        circ = Circle(radius=0.4).set_stroke(PINK, 4).set_fill(PINK, 0.2).move_to([5.3, mv.get_y(), 0])
        arrow2 = Arrow(circ.get_left(), mv.get_right(), buff=0.1, stroke_width=4, color=FG,
                       max_tip_length_to_length_ratio=0.15)
        raw = Code(S1.SQL_SRC, size=28, lang="sql")
        k = sq.width / raw.width
        pitch = sq.line(1).get_y() - sq.line(2).get_y()
        ghosts = [Code("JOIN   has_position …", size=28, lang="sql").scale(k),
                  Code("JOIN   people …", size=28, lang="sql").scale(k)]
        for i, gh in enumerate(ghosts):
            gh.align_to(sq, LEFT).set_y(sq.line(4).get_y() - i * pitch)
            gh.set_opacity(0.45)
        plus = T("+2 joins", 36, GOLD).move_to([1.6, sq.line(4).get_y() - 0.5 * pitch, 0])
        shift_lines = [g.animate.shift(2 * pitch * DOWN).set_fill(opacity=1) for i in (4, 5) for g in sq.line(i)]

        with self.say("c2.sql.5") as c:
            c.wait_until("The data model")
            self.play(*swap(self.cap, icons), run_time=1.4)  # early: the three data models
            c.wait_until("change")
            self.play(FlashAround(icons.graph, run_time=1.5, time_width=1.5, color=PINK))
            c.wait_until("cost")
            self.play(set_alpha([sq], 1)[0], *during([GrowFromCenter(circ), GrowArrow(arrow2)], 0.3, 1),
                      run_time=1.6)
            c.wait_until("two more")
            self.play(*during(disappear(icons), 0, 0.3), *during(shift_lines, 0.2, 0.6), *during(appear(*ghosts, shift=None, lag=0.2), 0.5, 0.85),
                      *during(appear(plus), 0.7, 1), run_time=min(1.8, c.until(None)))
