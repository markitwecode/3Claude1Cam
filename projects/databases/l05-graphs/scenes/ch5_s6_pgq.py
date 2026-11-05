"""Chapter 5, scene 6: graphs inside SQL (SQL/PGQ in DuckDB). Clips c5.pgq.1 – c5.pgq.4."""
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


PATTERN_SRC = "(p:people) -[r:plays_role]-> (m:movies)"


def pgq_pattern(size=36):
    """The GRAPH_TABLE match pattern as Cypher-highlighted code (the recap shows a shrunken copy)."""
    return Code(PATTERN_SRC, size=size)


def pattern_picture(r=0.35, length=1.8, labels=True):
    """PINK person circle -> BLUE movie circle, optionally labelled p, r, m."""
    p = Circle(radius=r).set_stroke(PINK, 4).set_fill(PINK, 0.15)
    m = Circle(radius=r).set_stroke(BLUE, 4).set_fill(BLUE, 0.15)
    m.move_to(p.get_center() + RIGHT * (2 * r + length))
    arr = Arrow(p.get_right(), m.get_left(), buff=0.08, stroke_width=4, color=FG)
    g = VGroup(p, arr, m)
    if labels:
        g.add(value_label("p", size=34).move_to(p), value_label("m", size=34).move_to(m),
              value_label("r", size=34).next_to(arr, UP, buff=0.1))
    return g.move_to(ORIGIN)


def table_card(name, cols, rows, color=BLUE, header_side=UP, col_gap=0.4, pitch=0.48, size=28):
    """A small table card: column names (DIM italic), rows, a rounded frame, the name outside it."""
    heads = [T(c, size, DIM, slant=ITALIC) for c in cols]
    body = [[T(v, size) for v in r] for r in rows]
    widths = [max([heads[j].width] + [r[j].width for r in body]) for j in range(len(cols))]
    x = 0.0
    for j, w in enumerate(widths):
        cx = x + w / 2
        heads[j].move_to([cx, 0, 0])
        for i, r in enumerate(body):
            r[j].move_to([cx, -(i + 1) * pitch, 0])
        x += w + col_gap
    hv = VGroup(*heads)
    rv = VGroup(*[VGroup(*r) for r in body])
    grid = VGroup(hv, rv)
    rule = Line([grid.get_left()[0] - 0.1, -pitch / 2, 0], [grid.get_right()[0] + 0.1, -pitch / 2, 0])
    rule.set_stroke(DIM, 1.5)
    frame = RoundedRectangle(corner_radius=0.12, width=grid.width + 0.5, height=grid.height + 0.4)
    frame.set_stroke(color, 2.5).move_to(grid)
    parts = [frame, rule, hv, rv]
    header = None
    if name:
        header = Mono(name, 28, color)
        header.next_to(frame, header_side, buff=0.12, aligned_edge=LEFT)
        parts.append(header)
    g = VGroup(*parts)
    g.frame, g.rule, g.heads, g.rows, g.header = frame, rule, hv, rv, header
    return g.move_to(ORIGIN)


def vertex(name, color, r=0.82):
    c = Circle(radius=r).set_stroke(color, 4).set_fill(color, 0.15)
    t = T(name, 28, line_spacing=0.8).move_to(c)
    g = VGroup(c, t)
    g.circle = c
    return g


def toward(v, p, pad=0.08):
    """The point on vertex v's circle facing point p."""
    c = v.circle.get_center()
    d = np.array(p) - c
    d = d / np.linalg.norm(d)
    return c + d * (v.circle.width / 2 + pad)


def colours_of(glyphs):
    return [g.get_color() for g in glyphs]


def restore(glyphs, cols):
    return [g.animate.set_color(c) for g, c in zip(glyphs, cols)]


def result_table():
    return table_card(None, ["title", "role", "name"],
                      [["The Kid", "A Tramp", "Charles Chaplin"],
                       ["The Kid", "Bride", "Beulah Bains"],
                       ["The Kid", "Car Thief", "Albert Austin"],
                       ["The Kid", "His Assistant", "B.F. Blinn"]], color=DIM, col_gap=0.35)


CREATE_SRC = """CREATE PROPERTY GRAPH movie_graph
VERTEX TABLES (movies, people)
EDGE TABLES (
  plays_role
    SOURCE KEY (person_id)
    REFERENCES people (person_id)
    DESTINATION KEY (movie_id)
    REFERENCES movies (movie_id)
);"""

QUERY_SRC = """SELECT   title, role, name
FROM     GRAPH_TABLE (movie_graph
            MATCH (p:people) -[r:plays_role]-> (m:movies)
            WHERE m.title = 'The Kid'
            COLUMNS (m.title, r.role, p.name))
ORDER BY role
LIMIT    4;"""

JOIN_SRC = """SELECT   m.title, r.role, p.name
FROM     movies AS m
JOIN     plays_role AS r ON m.movie_id = r.movie_id
JOIN     people AS p ON r.person_id = p.person_id
WHERE    m.title = 'The Kid'
ORDER BY r.role
LIMIT    4;"""


class PGQ(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c5.pgq.1
    def clip1(self):
        badge_t = T("not examinable", 28, DIM)
        badge_box = RoundedRectangle(corner_radius=0.12, width=badge_t.width + 0.4,
                                     height=badge_t.height + 0.3).set_stroke(DIM, 2)
        badge = VGroup(badge_box, badge_t).scale(1.5)
        self.badge = badge
        with self.say("c5.pgq.1") as c:
            self.play(*appear(badge), run_time=1.0)
            c.wait_until("But it closes a loop")
            self.play(badge.animate.scale(1 / 1.5).to_corner(UR, buff=0.4),
                      run_time=min(1.2, c.until("loop")))
            c.wait_until("loop")

            gt = load_scene("ch1_s6_tables").graph_tables()   # the part-one picture, tags dropped
            tables = VGroup(gt.vcard, gt.ecard)
            tables.scale_to_fit_height(3.9).move_to([-4.3, 1.15, 0]).align_to([-6.3, 0, 0], LEFT)
            vcard, ecard = gt.vcard, gt.ecard
            mini = pattern_picture(r=0.35, length=1.1, labels=False).move_to([4.9, 0.7, 0])
            arrow = Arrow([3.4, 0.7, 0], [tables.get_right()[0] + 0.15, 0.7, 0], buff=0,
                          stroke_width=5, color=YELLOW)
            lab = T("graph → tables", 30, YELLOW).next_to(arrow, UP, buff=0.2)
            self.play(*appear(vcard, ecard, mini, arrow, lab, lag=0.12),
                      run_time=min(1.4, c.until("flip")))
            c.wait_until("flip")
            lab2 = T("tables → graph", 30, YELLOW).move_to(lab)
            self.play(Rotate(arrow, PI), *swap(lab, lab2), run_time=min(1.5, c.until("duck")))
            c.wait_until("duck")

            inst = Code("INSTALL duckpgq FROM community;\nLOAD duckpgq;", size=36, lang="sql")
            inst.move_to([0, -1.7, 0])
            self.play(*appear(inst), run_time=1.0)
            c.wait_until("install")
            tag = T("DuckDB command line only, not the web version", 28, DIM)
            tag.next_to(inst, DOWN, buff=0.4)
            self.play(*appear(tag), run_time=1.0)  # early: a caption for the whole sentence

    # ------------------------------------------------------------------ c5.pgq.2
    def clip2(self):
        people = table_card("people", ["name"], [["Charles Chaplin"], ["Beulah Bains"]])
        movies = table_card("movies", ["title"], [["The Kid"], ["City Lights"]])
        people.move_to([-5.0, 1.5, 0])
        movies.move_to([-2.0, 1.5, 0]).align_to(people, UP)
        roles = table_card("plays_role", ["person_id", "movie_id", "role"],
                           [["Chaplin", "The Kid", "'A Tramp'"]], header_side=DOWN, col_gap=0.25)
        roles.move_to([-3.8, -2.3, 0])

        code = Code(CREATE_SRC, size=26, lang="sql")
        if code.width > 7.1:
            code.scale_to_fit_width(7.1)
        code.move_to([0, -0.3, 0]).align_to([-0.5, 0, 0], LEFT)

        with self.say("c5.pgq.2") as c:
            sweep_clear(self, *appear(people, movies, roles, code.line(0), lag=0.2),  # early: the tables shown whole, then walked
                        keep=[self.badge], run_time=min(2.4, c.until("vertices")))
            c.wait_until("vertices")
            l1 = code.line(1)
            l1_cols = colours_of(l1)
            self.play(*appear(l1), run_time=1.0)
            self.play(*recolor(l1, YELLOW), run_time=0.8)
            c.wait_until("Here every row")

            beulah = vertex("Beulah\nBains", PINK).move_to([-5.75, 2.0, 0])
            chap = vertex("Charles\nChaplin", PINK).move_to([-5.75, 0.15, 0])
            city = vertex("City\nLights", BLUE).move_to([-1.55, 2.0, 0])
            kid = vertex("The Kid", BLUE).move_to([-1.55, 0.15, 0])
            ptag = T(":people", 30, PINK).next_to(beulah, UP, buff=0.18)
            mtag = T(":movies", 30, BLUE).next_to(city, UP, buff=0.18)
            pv = VGroup(ptag, beulah, chap)
            mv = VGroup(mtag, city, kid)
            self.play(*swap(people, pv), *swap(movies, mv), run_time=min(1.8, c.until("edges")))  # early: the table names, said as the rows turn
            c.wait_until("edges")

            self.play(*appear(code.line(2), code.line(3), lag=0.3), run_time=1.0)
            top = roles.frame.get_top()[1] + 0.06
            ps = [roles.heads[0].get_x(), top, 0]
            ms = [roles.heads[1].get_x(), top, 0]
            a1 = Arrow(ps, toward(chap, ps), buff=0, stroke_width=4, color=YELLOW)
            a2 = Arrow(ms, toward(kid, ms), buff=0, stroke_width=4, color=YELLOW)
            row = roles.rows[0]
            self.play(GrowArrow(a1), GrowArrow(a2), *recolor([row[0], row[1]], YELLOW),
                      run_time=min(1.5, c.until("fk")))
            c.wait_until("fk")

            self.play(*appear(*[code.line(i) for i in range(4, 9)], lag=0.15), run_time=1.5)
            settle(self, code)
            fk_glyphs = [g for i in range(4, 8) for g in code.line(i)]
            self.play(*restore(l1, l1_cols), *recolor(fk_glyphs, YELLOW), run_time=1.0)
            c.wait_until("So the two foreign keys")

            edge = Arrow(chap.circle.get_right(), kid.circle.get_left(), buff=0.08,
                         stroke_width=5, color=FG)
            elab = Mono("plays_role", 28, FG).next_to(edge, UP, buff=0.12)
            prop = T("role: 'A Tramp'", 28, DIM).move_to(edge).shift(DOWN * 0.95)
            self.play(*during(disappear(roles, a1, a2), 0, 0.45),
                      *during([GrowArrow(edge)], 0.4, 0.75),
                      *during(appear(elab, prop, lag=0.2), 0.6, 1.0),
                      run_time=min(2.0, c.until("more")))
            c.wait_until("more")

            ghost_t = T("has_position: could be added", 28, DIM)
            ghost_box = DashedVMobject(RoundedRectangle(corner_radius=0.12, width=ghost_t.width + 0.5,
                                                        height=ghost_t.height + 0.5), num_dashes=40)
            ghost_box.set_stroke(DIM, 2)
            ghost = VGroup(ghost_box, ghost_t).move_to([-3.65, -2.1, 0])
            ghost_t.move_to(ghost_box)
            self.play(*appear(ghost), run_time=1.0)

    # ------------------------------------------------------------------ c5.pgq.3
    def clip3(self):
        q = Code(QUERY_SRC, size=26, lang="sql")
        if q.width > 12.6:
            q.scale_to_fit_width(12.6)
        q.move_to([0, -1.0, 0])

        with self.say("c5.pgq.3") as c:
            c.wait_until("pattern")
            sweep_clear(self, *appear(q, shift=None), keep=[self.badge],  # early: the whole query first, then walked
                        run_time=min(2.0, c.until("graphtable")))
            c.wait_until("graphtable")

            match = q.line(2)
            match_cols = colours_of(match)
            pat = pattern_picture().move_to([-3.4, 2.4, 0])
            self.play(*recolor(match, YELLOW), *appear(pat), run_time=min(1.5, c.until("columns")))
            c.wait_until("columns")

            cols = q.line(4)
            cols_cols = colours_of(cols)
            self.play(*restore(match, match_cols), *recolor(cols, YELLOW), run_time=0.8)
            row = VGroup(T("The Kid", 30, BLUE), T("A Tramp", 30, FG), T("Charles Chaplin", 30, PINK))
            row.arrange(RIGHT, buff=0.5).move_to([3.0, 2.4, 0])
            self.play(*fly(pat, row), run_time=min(1.5, c.until("outer")))  # early: one example placement, its names come with the result
            c.wait_until("outer")

            inner = list(q.find("GRAPH_TABLE (movie_graph")) + [g for i in (2, 3, 4) for g in q.line(i)]
            outer_kw = [q.find("SELECT"), q.find("ORDER", line=5), q.find("BY", line=5), q.find("LIMIT")]
            plain = T("plain SQL", 32, BLUE).next_to(q.line(5), RIGHT, buff=1.2)
            plain.match_y(VGroup(q.line(5), q.line(6)))
            self.play(*restore(cols, cols_cols), *set_alpha(inner, 0.35), run_time=1.0)
            self.play(*flash(outer_kw, color=BLUE), *appear(plain), run_time=1.2)  # early: the tag names what the sentence ends on
            c.wait_until("same")

            self.play(*disappear(pat, row, plain), *set_alpha(inner, 1), run_time=1.0)
            resA = result_table()
            resA.scale_to_fit_width(min(resA.width, 6.1)).move_to([-3.5, -2.2, 0])
            tagA = T("GRAPH_TABLE", 28, DIM).next_to(resA, UP, buff=0.15)
            self.play(*during([q.animate.move_to([0, 1.45, 0])], 0, 0.6), *during(appear(resA, tagA, shift=None, lag=0.1), 0.6, 1.0), run_time=min(2.0, c.until("A Tramp played")))  # early: the result shown whole, then read
            c.wait_until("A Tramp played")
            self.play(*flash([resA.rows[0]], color=YELLOW), run_time=1.5)
            c.wait_until("join")

            j = Code(JOIN_SRC, size=26, lang="sql").move_to(q).align_to(q, LEFT)
            resB = result_table()
            resB.scale_to_fit_width(min(resB.width, 6.1)).move_to([3.5, -2.2, 0])
            tagB = T("three-table join", 28, DIM).next_to(resB, UP, buff=0.15)
            eq = MathTex("=", font_size=96, color=GREEN).move_to([0, -2.2, 0])
            self.play(*swap(q, j), *during(appear(resB, tagB, eq, shift=None, lag=0.2), 0.5, 1.0),
                      run_time=min(1.8, c.until()))

    # ------------------------------------------------------------------ c5.pgq.4
    def clip4(self):
        box = RoundedRectangle(corner_radius=0.2, width=10.5, height=1.8).set_stroke(BLUE, 4)
        box.set_fill(BLUE, 0.08).move_to([0, -1.4, 0])
        sql = Mono("SQL", 48, BLUE).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.6)
        strip = VGroup(box, sql)
        braces = Mono("{ }", 56, TEAL).move_to([-0.6, -1.4, 0])
        json_tag = T("Lecture 4", 30, DIM).next_to(box, DOWN, buff=0.3).match_x(braces)
        edge = pattern_picture(r=0.32, length=1.0, labels=False).move_to([2.9, -1.4, 0])
        now_tag = T("now", 30, DIM).next_to(box, DOWN, buff=0.3).match_x(edge)
        pat = pgq_pattern(36).move_to([0, 1.1, 0])
        cy = T("from Cypher", 32, YELLOW).next_to(pat, UP, buff=0.4)

        with self.say("c5.pgq.4") as c:
            c.wait_until("json")
            sweep_clear(self, *appear(strip, shift=None), keep=[self.badge], run_time=1.4)
            self.play(FadeIn(braces, shift=LEFT * 2.5), run_time=1.2)
            self.play(*appear(json_tag), run_time=0.8)
            c.wait_until("graphs")
            self.play(FadeIn(edge, shift=LEFT * 2.5), run_time=1.2)
            self.play(*appear(now_tag), run_time=0.8)
            c.wait_until("origin")
            self.play(*fly(edge, pat), run_time=1.5)
            c.wait_until(own_word=cy)
            self.play(*appear(cy), run_time=1.0)
            c.wait_until("chains of connections")
            self.play(FlashAround(pat, run_time=2, time_width=1.5, color=YELLOW))
