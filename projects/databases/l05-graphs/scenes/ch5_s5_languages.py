"""Chapter 5, scene 5: a family of graph languages; Cypher's shortestPath vs GQL's SHORTEST 1. Clips c5.lang.1 – c5.lang.3."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


CYPHER_SRC = """MATCH path = shortestPath(
        (a:Person {name: 'Jennifer Lawrence'})
        -[:ACTED_IN*]-
        (b:Person {name: 'Daniel Radcliffe'}))
RETURN length(path);"""

GQL_SRC = """MATCH path = SHORTEST 1
        (a:Person {name: 'Jennifer Lawrence'})
        -[:ACTED_IN]-+
        (b:Person {name: 'Daniel Radcliffe'})
RETURN length(path);"""

CODE_SIZE = 28


def plus_edge(size=36):
    """The GQL edge pattern `-[:ACTED_IN]-+` as Code, its `+` YELLOW (for the chapter recap)."""
    code = Code("-[:ACTED_IN]-+", size=size)
    code.find("+").set_color(YELLOW)
    return code


def card(title, subs=(), color=BLUE, text=FG, width=None, tsize=40, ssize=28):
    """A rounded card: title over sub-lines. subs: list of (text, colour)."""
    t = T(title, tsize, color=text)
    ss = [T(s, ssize, color=c) for s, c in subs]
    col = VGroup(t, *ss).arrange(DOWN, buff=0.16)
    w = width or col.width + 0.6
    box = RoundedRectangle(corner_radius=0.15, width=w, height=col.height + 0.5)
    box.set_stroke(color, 3).set_fill(BG, 1).move_to(col)
    g = VGroup(box, t, *ss)
    g.box, g.title, g.subs = box, t, ss
    return g


class Languages(NarratedScene):
    def construct(self):
        # ---------- the family tree (full size) ----------
        cy = card("Cypher", [("Neo4j, ≈ 2011", DIM)], color=BLUE).move_to(2.25 * UP)
        root = cy.box.get_bottom()
        CW, CX, TOP = 3.9, 4.3, -0.3
        oc = card("openCypher", [("open specification", DIM)], width=CW)
        oc.move_to(CX * LEFT).align_to(TOP * UP, UP)
        gql = card("GQL", [("ISO/IEC 39075:2024", DIM), ("Traverse runs it too", GREEN)], width=CW)
        gql.move_to(ORIGIN).align_to(TOP * UP, UP)
        pgq = card("SQL/PGQ", [("SQL:2023 part 16", DIM), ("patterns inside SQL", FG)], width=CW)
        pgq.move_to(CX * RIGHT).align_to(TOP * UP, UP)
        pgq.box.stretch_to_fit_height(gql.box.height).align_to(gql.box, UP)
        oc.box.stretch_to_fit_height(gql.box.height).align_to(gql.box, UP)
        for c_ in (oc, pgq):   # re-centre text in the stretched boxes
            VGroup(*c_[1:]).move_to(c_.box)
        VGroup(*gql[1:]).move_to(gql.box)

        def edge(child):
            return Line(root, child.box.get_top(), stroke_width=3, color=BLUE)

        e_oc, e_gql, e_pgq = edge(oc), edge(gql), edge(pgq)
        for e in (e_oc, e_gql, e_pgq):
            e.set_z_index(-2)

        sparql = card("SPARQL", [("a different graph model,", DIM), ("RDF triple stores", DIM)],
                      color=DIM, text=DIM, tsize=36).move_to([-4.45, 2.25, 0])
        gremlin = card("Gremlin", color=DIM, text=DIM, tsize=36).move_to([4.45, 2.25, 0])

        frame = SurroundingRectangle(VGroup(gql.box, pgq.box), buff=0.22, corner_radius=0.2)
        frame.set_stroke(YELLOW, 2).set_fill(opacity=0).set_z_index(-3)
        iso = T("ISO", 36, color=YELLOW).next_to(frame, UP, buff=0.12).align_to(frame, RIGHT).shift(0.3 * LEFT)

        # ---------- clip 1: Cypher, openCypher, the others ----------
        with self.say("c5.lang.1") as c:
            self.play(*appear(cy), run_time=1.0)
            c.wait_until("open specification")
            self.play(Create(e_oc), *during(appear(oc), 0.3, 1), run_time=1.5)
            c.wait_until("sparql")
            self.play(*appear(sparql.box, sparql.title), run_time=1.0)
            c.wait_until(own_word=sparql.subs[0])
            self.play(*appear(sparql.subs[0]), run_time=1.0)
            c.wait_until(own_word=sparql.subs[1])
            self.play(*appear(sparql.subs[1]), run_time=1.0)
            c.wait_until("gremlin")
            self.play(*appear(gremlin), run_time=min(1.0, c.until()))

        # ---------- clip 2: ISO, GQL, SQL/PGQ ----------
        with self.say("c5.lang.2", gap=1.3) as c:
            self.play(FadeIn(frame), *appear(iso), run_time=1.2)
            c.wait_until("gql")
            self.play(Create(e_gql), *during(appear(gql.box, gql.title, gql.subs[0]), 0.3, 1),
                      run_time=1.5)
            c.wait_until(own_word=gql.subs[1])
            self.play(*appear(gql.subs[1]), run_time=1.0)
            c.wait_until("pgq")
            self.play(Create(e_pgq), *during(appear(pgq.box, pgq.title, pgq.subs[0]), 0.3, 1),
                      run_time=1.5)
            c.wait_until(own_word=pgq.subs[1])
            self.play(*appear(pgq.subs[1]), run_time=1.0)

        tree = VGroup(e_oc, e_gql, e_pgq, frame, iso, cy, oc, gql, pgq, sparql, gremlin)
        settle(self, tree)

        # ---------- clip 3: Cypher vs GQL ----------
        cyc = Code(CYPHER_SRC, size=CODE_SIZE)
        gqc = Code(GQL_SRC, size=CODE_SIZE)
        cyc.move_to([-0.25, 1.25, 0])
        gqc.next_to(cyc, DOWN, buff=0.55).align_to(cyc, LEFT)
        tag_cy = T("Cypher", 32, color=DIM).move_to(cyc.line(2)).align_to(cyc, RIGHT)
        tag_gq = T("GQL", 32, color=DIM).move_to(gqc.line(2)).align_to(gqc, RIGHT)

        with self.say("c5.lang.3") as c:
            # the tree clears; its Cypher and GQL titles become the code blocks' tags
            moves = []
            for title, tag in ((cy.title, tag_cy), (gql.title, tag_gq)):
                title.generate_target()
                title.target.scale_to_fit_height(tag.height).move_to(tag).set_color(DIM)
                moves.append(MoveToTarget(title))
            rest = [m for m in tree.get_family() if m not in (cy.title, gql.title)
                    and not m.submobjects]
            self.play(*during([FadeOut(m) for m in rest], 0, 0.45),
                      *during(moves, 0.15, 0.7),
                      *during(appear(cyc), 0.7, 1), run_time=2.0)
            tag_cy, tag_gq = cy.title, gql.title
            self.remove(*tree.get_family())
            self.add(tag_cy, tag_gq)
            self.play(*appear(gqc), run_time=1.0)

            # SHORTEST 1 vs shortestPath(
            c.wait_until("shortest")
            t1, t2 = cyc.find("shortestPath("), gqc.find("SHORTEST 1")
            o1 = [g.get_color() for g in t1]
            o2 = [g.get_color() for g in t2]
            xr = max(cyc.get_right()[0], gqc.get_right()[0]) + 0.4
            p1 = t1.get_right() + 0.15 * RIGHT
            p2 = t2.get_right() + 0.15 * RIGHT
            joiner = VMobject().set_points_as_corners(
                [p1, [xr, p1[1], 0], [xr, p2[1], 0], p2]).set_stroke(YELLOW, 3)
            self.play(*recolor(t1, YELLOW), *recolor(t2, YELLOW), Create(joiner), run_time=1.5)

            # the * and the +
            c.wait_until("plus")
            star, plus = cyc.find("*"), gqc.find("+")
            ed1 = [g for g in cyc.find("-[:ACTED_IN*]-") if g not in star]
            ed2 = [g for g in gqc.find("-[:ACTED_IN]-+") if g not in plus]
            self.play(*[g.animate.set_color(col) for g, col in zip(t1, o1)],
                      *[g.animate.set_color(col) for g, col in zip(t2, o2)],
                      FadeOut(joiner),
                      *[g.animate.set_color(YELLOW).set_opacity(0.55) for g in ed1 + ed2],
                      *recolor(star, YELLOW), *recolor(plus, YELLOW), run_time=1.5)
            c.wait_until("star")
            self.play(FlashAround(star, run_time=1.2, time_width=1.5))
            c.wait_until("plus sign")
            self.play(FlashAround(plus, run_time=1.2, time_width=1.5))

            # regex inset at the top
            c.wait_until("regex")
            rx = Mono("a+", 36, color=YELLOW)
            mt = T("matches", 30, color=DIM)
            ex = Mono('"a"   "aa"   "aaa"', 32)
            om = T("one or more", 30, color=YELLOW)
            row = VGroup(rx, mt, ex, om).arrange(RIGHT, buff=0.45)
            om.shift(0.25 * RIGHT)
            box = SurroundingRectangle(row, buff=0.2, corner_radius=0.15).set_stroke(DIM, 2)
            inset = VGroup(box, row).move_to(3.05 * UP)
            self.play(*appear(inset), run_time=1.2)

            # the same answer
            c.wait_until("four")
            r1 = VGroup(T("⇒", 36, color=DIM), Mono("4", 36, color=GOLD)).arrange(RIGHT, buff=0.3)
            r2 = r1.copy()
            r1.next_to(cyc.line(4), RIGHT, buff=0.7)
            r2.next_to(gqc.line(4), RIGHT, buff=0.7)
            self.play(*appear(r1, r2, lag=0.3), run_time=1.2)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
