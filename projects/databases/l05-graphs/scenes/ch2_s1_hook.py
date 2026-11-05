"""Chapter 2, scene 1: Hook. Which movies did Spielberg direct? SQL, its diagram, and the
diagram as Cypher. Clips c2.hook.1 – c2.hook.3.

Exports: open_card() (ch1 s8 ends on it), sql_block() and join_diagram() (s6 brings them back).
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

OPEN_SRC = "(p:Person) -[:ACTED_IN]-> (m:Movie)"
SQL_SRC = """SELECT m.title, m.year
FROM   people AS p
JOIN   has_position AS hp ON hp.person_id = p.person_id
JOIN   movies AS m ON m.movie_id = hp.movie_id
WHERE p.name = 'Steven Spielberg'
  AND hp.position = 'director';"""
CYPHER_SRC = "(p:Person {name: 'Steven Spielberg'}) -[:DIRECTED]-> (m:Movie)"
R = 1.2          # vertex circle radius
MAX_W = 13.0      # widest a full-width line may be


def open_card():
    """ch2's first frame (ch1 s8's end card): the one Cypher line, centred, nothing else."""
    return VGroup(Code(OPEN_SRC, size=40).move_to(ORIGIN))


def sql_block():
    """Slide 105's SQL, verbatim, centred at ORIGIN (~13 wide)."""
    code = Code(SQL_SRC, size=28, lang="sql")
    if code.width > MAX_W:
        code.scale_to_fit_width(MAX_W)
    return code.move_to(ORIGIN)


def join_diagram():
    """people -> has_position -> movies, links labelled person_id / movie_id, centred at ORIGIN.
    Attributes: .boxes, .names, .links, .keys (lists, left to right)."""
    names = [Mono(n, size=28) for n in ("people", "has_position", "movies")]
    boxes = [RoundedRectangle(corner_radius=0.12, width=n.width + 0.5, height=0.8,
                              stroke_color=FG, stroke_width=3).move_to(n) for n in names]
    gap = 2.4
    x = 0.0
    for b, n in zip(boxes, names):
        b.move_to([x + b.width / 2, 0, 0])
        n.move_to(b)
        x += b.width + gap
    links = [Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.12, stroke_width=4,
                   color=TEAL, max_tip_length_to_length_ratio=0.15) for i in range(2)]
    keys = [Mono(k, size=28, color=TEAL).next_to(l, UP, buff=0.12) for k, l in zip(("person_id", "movie_id"), links)]
    g = VGroup(*boxes, *names, *links, *keys)
    g.shift(-g.get_center() * np.array([1, 0, 0]) - np.array([0, boxes[0].get_y(), 0]))
    g.boxes, g.names, g.links, g.keys = boxes, names, links, keys
    return g


def vertex(lines, color, at):
    circ = Circle(radius=R, color=color, stroke_width=4).set_fill(color, 0.12).move_to(at)
    lab = T(lines, size=30, line_spacing=0.8)
    if lab.width > 1.6 * R:
        lab.scale_to_fit_width(1.6 * R)
    lab.move_to(circ)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


def edge(a, b, text):
    """Arrow from vertex a to vertex b, its type in caps along it (above the line)."""
    s, e = a.circ.get_center(), b.circ.get_center()
    arr = Arrow(s, e, buff=R + 0.06, stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.12)
    d = (e - s) / np.linalg.norm(e - s)
    ang = np.arctan2(d[1], d[0])
    if ang > PI / 2:
        ang -= PI
    if ang < -PI / 2:
        ang += PI
    nrm = np.array([-d[1], d[0], 0])
    if nrm[1] < 0:
        nrm = -nrm
    lab = set_backstroke(T(text, size=30).rotate(ang))
    lab.move_to(arr.get_center() + 0.42 * nrm)
    return arr, lab


class Hook(NarratedScene):
    def construct(self):
        card = open_card()
        self.add(card)
        self.wait(0.6)
        self.clip1(card)
        self.clip2()
        self.clip3()
        self.wait(5.7)   # payoff line + footnote hold (dwell)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self, card):
        tc = title_card("Part 2 · Patterns: vertices, edges and arrows")
        with self.say("c2.hook.1") as c:
            self.play(*during(FadeOut(card), 0, 0.35),
                      *during([FadeIn(tc.title, shift=0.3 * DOWN), GrowFromCenter(tc.rule)], 0.35, 1),
                      run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.2)  # early: title card
            c.wait_until("graph")

            chaplin = vertex("Charles\nChaplin", PINK, [1.6, 1.8, 0])
            coogan = vertex("Jackie\nCoogan", PINK, [-5.0, 1.8, 0])
            kid = vertex("The Kid", BLUE, [-1.8, -2.0, 0])
            gold = vertex("The Gold\nRush", BLUE, [4.8, -2.0, 0])
            verts = [coogan, chaplin, kid, gold]
            edges = [edge(coogan, kid, "ACTED_IN"), edge(chaplin, kid, "ACTED_IN"),
                     edge(chaplin, gold, "DIRECTED")]
            sweep_clear(self, *appear(*verts, shift=None, lag=0.3), run_time=2.0)
            c.wait_until("edge")
            self.play(*[GrowArrow(a) for a, _ in edges], run_time=1.4)
            c.wait_until("an arrow")
            self.play(*appear(*[l for _, l in edges], lag=0.3), run_time=1.4)
            graph = VGroup(*verts, *[a for a, _ in edges], *[l for _, l in edges])
            self.add(graph)
            c.wait_until("ask")
            labels = [v.lab for v in verts] + [l for _, l in edges]
            self.play(*during([FadeOut(l) for l in labels], 0, 0.4),
                      *during(graph.animate.scale(0.5).to_corner(UR, buff=0.5), 0.3, 1), run_time=1.6)
            self.remove(*[m for l in labels for m in l.get_family()])
            q = T("Which movies did Steven Spielberg direct?", size=40, color=YELLOW).move_to(0.4 * DOWN)
            c.wait_until(own_word=q)
            self.play(*appear(q), run_time=1.2)
        self.graph, self.q = graph, q

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        graph, q = self.graph, self.q
        sql = sql_block().move_to(1.4 * UP)
        diag = join_diagram().move_to(2.0 * DOWN)
        with self.say("c2.hook.2") as c:
            self.play(*during(FadeOut(graph), 0, 0.35),
                      *during(q.animate.scale(0.8).move_to(3.45 * UP), 0.3, 0.75),
                      *during(FadeIn(sql), 0.6, 1),
                      run_time=2.0)
            c.wait_until("people")
            box = token_box(sql.find("people"), sql.line(1))
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("has position")
            self.play(Transform(box, token_box(sql.find("has_position"), sql.line(2))), run_time=0.6)
            c.wait_until("movies")
            self.play(Transform(box, token_box(sql.find("movies"), sql.line(3))), run_time=0.6)
            c.wait_until("joins")
            on1 = sql.find("ON hp.person_id = p.person_id")
            on2 = sql.find("ON m.movie_id = hp.movie_id")
            self.play(Transform(box, token_box(on1, sql.line(2))), run_time=1.0)
            c.wait_until("columns must match")
            self.play(Transform(box, token_box(on2, sql.line(3))), run_time=1.0)
            c.wait_until("draw")
            self.play(FadeOut(box), run_time=0.6)
            srcs = [sql.find("people"), sql.find("has_position"), sql.find("movies")]
            for i, (s, n, b) in enumerate(zip(srcs, diag.names, diag.boxes)):
                self.play(FlashAround(s, run_time=1.0, time_width=1.5),
                          *during(appear(b, n, lag=0), 0.3, 1), run_time=1.2 if i == 0 else 0.9)
            c.wait_until("linked")
            self.play(*[GrowArrow(l) for l in diag.links], run_time=1.2)
            self.play(*appear(*diag.keys, lag=0.4), run_time=1.2)
            self.add(diag)
        self.sql, self.diag = sql, diag

    # ------------------------------------------------------------------ clip 3
    def clip3(self):
        sql, diag = self.sql, self.diag
        y = diag.boxes[0].get_y()
        spiel = vertex("Steven\nSpielberg", PINK, [-4.6, y - 0.1, 0])
        movie = vertex("Movie", BLUE, [4.6, y - 0.1, 0])
        arr, dlab = edge(spiel, movie, "DIRECTED")
        cy = Code(CYPHER_SRC, size=28)
        if cy.width > MAX_W:
            cy.scale_to_fit_width(MAX_W)
        cy.move_to([0, y + 0.5, 0])
        note = T("Cypher docs: neo4j.com · Traverse: truespar.com", size=28, color=DIM).move_to(3.4 * DOWN)

        with self.say("c2.hook.3") as c:
            self.play(FlashAround(diag, run_time=2, time_width=1.5, buff=0.25))
            c.wait_until("morph")
            leave = [FadeOut(n) for n in diag.names] + [FadeOut(k) for k in diag.keys] \
                + [FadeOut(l) for l in diag.links]
            self.play(*during(leave, 0, 0.4),  # early: DIRECTED is part of the drawing, read next sentence
                      *during([ReplacementTransform(diag.boxes[0], spiel.circ),
                               ReplacementTransform(diag.boxes[1], arr),
                               ReplacementTransform(diag.boxes[2], movie.circ)], 0.2, 0.8),
                      *during([FadeIn(spiel.lab), FadeIn(movie.lab), FadeIn(dlab)], 0.6, 1),
                      run_time=2.2)
            self.remove(*diag.get_family())
            self.add(spiel, movie, arr, dlab)
            c.wait_until("person")
            self.play(FlashAround(spiel.circ, run_time=1.2, time_width=1.5, color=PINK))
            c.wait_until("arrow")
            self.play(FlashAround(VGroup(arr, dlab), run_time=1.2, time_width=1.5))
            c.wait_until("movie")
            self.play(FlashAround(movie.circ, run_time=1.2, time_width=1.5, color=BLUE))
            c.wait_until("ascii")

            p_part = cy.find("(p:Person {name: 'Steven Spielberg'})")
            m_part = cy.find("(m:Movie)")
            a_part = cy.find("-[:DIRECTED]->")
            h = cy.height + 0.35
            e1 = Ellipse(width=p_part.width + 0.2, height=h, color=PINK, stroke_width=4).move_to(p_part)
            e2 = Ellipse(width=m_part.width + 0.2, height=h, color=BLUE, stroke_width=4).move_to(m_part)
            a2 = Arrow(a_part.get_left(), a_part.get_right(), buff=0, stroke_width=4, color=FG,
                       max_tip_length_to_length_ratio=0.15)
            self.play(*set_alpha([sql], 0.3),
                      *during([FadeOut(spiel.lab), FadeOut(movie.lab), FadeOut(dlab)], 0, 0.35),
                      *during([ReplacementTransform(spiel.circ, e1), ReplacementTransform(movie.circ, e2),
                               ReplacementTransform(arr, a2)], 0.25, 1),
                      run_time=1.6)
            self.remove(*spiel.get_family(), *movie.get_family())
            self.play(*during([FadeOut(e1), FadeOut(e2), FadeOut(a2)], 0, 0.6),
                      *during(FadeIn(cy), 0.3, 1), run_time=1.1)
            self.play(*appear(note, shift=None), run_time=1.0)
            c.wait_until("arrowhead")
            self.play(FlashAround(a_part, run_time=1.4, time_width=1.5))
