"""Chapter 1, scene 6: a property graph in two relational tables (Slide 96). Clips c1.tables.1 – c1.tables.4.

Exports for later scenes (load_scene("ch1_s6_tables")):
  graph_tables()   VGroup(vcard, ecard, tails_tag, heads_tag): the `vertices` card above the `edges`
                   card, YELLOW edges_tails / edges_heads tags beside tail_vertex / head_vertex.
                   .vcard .ecard .tails_tag .heads_tag; cards have .box .title .rows (Mono 28).
                   About 6.3 x 5.2 at scale 1, centred on ORIGIN.
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

S4 = load_scene("ch1_s4_propgraph")
S5 = load_scene("ch1_s5_moviegraph")

CS = 21            # DDL / query code size (17 lines must fit the frame at once)

V_SRC = [
    "CREATE TABLE vertices(",
    "vertex_id  INT PRIMARY KEY,",
    "label      TEXT,    -- e.g. 'Movie' or 'Person'",
    'properties JSON     -- e.g. {"name": "Charles Chaplin"}',
    ");",
]
E_SRC = [
    "CREATE TABLE edges(",
    "edge_id     INT PRIMARY KEY,",
    "tail_vertex INT REFERENCES vertices(vertex_id),",
    "head_vertex INT REFERENCES vertices(vertex_id),",
    "type        TEXT,   -- e.g. 'ACTED_IN'",
    'properties JSON     -- e.g. {"roles": ["A Tramp"]}',
    ");",
]
I_SRC = ["CREATE INDEX edges_tails ON edges(tail_vertex);",
         "CREATE INDEX edges_heads ON edges(head_vertex);"]
DDL = "\n".join(V_SRC + [""] + E_SRC + [""] + I_SRC)

Q_SRC = """SELECT p.properties->>'name' AS name
FROM vertices AS m
JOIN edges AS e ON e.head_vertex = m.vertex_id
JOIN vertices AS p ON p.vertex_id = e.tail_vertex
WHERE m.properties->>'title' = 'The Kid'
AND e.type = 'ACTED_IN';"""

ACTORS = ["Charles Chaplin", "Jackie Coogan", "Albert Austin", "Beulah Bains", "Nellie Bly Baker",
          "Henry Bergman", "Edward Biby", "B.F. Blinn", "Carl Miller", "Edna Purviance"]


def sql(src):
    return Code(src, size=CS, lang="sql")


def partial(lines, n):
    """The skeleton with the first n column lines filled: header, n lines, ');'."""
    return "\n".join([lines[0]] + lines[1:1 + n] + [lines[-1]])


def anchor(code, i):
    return code.line(i)[0].get_center()


def put(block, point):
    """Shift a block so its first glyph (always the C of CREATE) sits at point."""
    return block.shift(point - anchor(block, 0))


# ---------------------------------------------------------------- export for s8
def _card(title, cols, color=BLUE):
    rows = VGroup(*[Mono(c, size=28) for c in cols]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    t = T(title, 32, color).next_to(rows, UP, buff=0.25).align_to(rows, LEFT)
    inner = VGroup(t, rows)
    box = RoundedRectangle(corner_radius=0.12, width=inner.width + 0.6, height=inner.height + 0.45)
    box.set_stroke(color, 3).set_fill(color, 0.06).move_to(inner)
    g = VGroup(box, t, rows)
    g.box, g.title, g.rows = box, t, rows
    return g


def graph_tables():
    vcard = _card("vertices", ["vertex_id", "label", "properties"])
    ecard = _card("edges", ["edge_id", "tail_vertex", "head_vertex", "type", "properties"])
    vcard.align_to(ecard, LEFT).next_to(ecard, UP, buff=0.35).align_to(ecard, LEFT)
    tails = S4.label_tag("edges_tails", YELLOW)
    heads = S4.label_tag("edges_heads", YELLOW)
    tails.next_to(ecard.box, RIGHT, buff=0.15).set_y(ecard.rows[1].get_y())
    heads.next_to(ecard.box, RIGHT, buff=0.15).set_y(ecard.rows[2].get_y())
    g = VGroup(vcard, ecard, tails, heads).move_to(ORIGIN)
    g.vcard, g.ecard, g.tails_tag, g.heads_tag = vcard, ecard, tails, heads
    return g


# ---------------------------------------------------------------- stand-ins / shared helpers
def lit(m, color=YELLOW):
    m.saved_look = m.copy()
    return m.animate.set_color(color)


def unlit(m):
    return Transform(m, m.saved_look)


def end_tag(text, point, side):
    d = Dot(point, radius=0.08, color=YELLOW)
    t = T(text, 30, YELLOW)
    t.move_to(point + 0.36 * UP)
    if side[0] < 0:
        t.align_to(point + 0.75 * RIGHT, LEFT)
    else:
        t.align_to(point + 0.75 * LEFT, RIGHT)
    g = VGroup(d, t)
    g.text = t
    return g


def edge_stack(n=22):
    bars = VGroup(*[Rectangle(width=2.3, height=0.15).set_stroke(GOLD, 1.5).set_fill(GOLD, 0.15)
                    for _ in range(n)]).arrange(DOWN, buff=0.1)
    return bars


def small_arrow(a, b, color=FG, width=3):
    ln = Line(a, b).set_stroke(color, width)
    ln.add_tip(tip_length=0.18, tip_width=0.18)
    ln.tip.set_fill(color, 1).set_stroke(color, 1)
    return ln


def tangle():
    """Coogan TL, Chaplin TR, The Kid BL, The Gold Rush BR (s5's layout), three s4 typed edges:
    Coogan -> The Kid, Chaplin -> The Kid, Chaplin -> The Gold Rush. Names on the outer side."""
    spec = [("coogan", "Jackie Coogan", "Person", (-2.4, 3.1), LEFT),
            ("chaplin", "Charles Chaplin", "Person", (2.4, 3.1), RIGHT),
            ("kid", "The Kid", "Movie", (-2.4, 1.3), LEFT),
            ("gold", "The Gold Rush", "Movie", (2.4, 1.3), RIGHT)]
    v = {}
    for key, name, kind, (x, y), side in spec:
        vv = S4.vertex(name, kind, at=[x, y, 0], r=0.38)
        vv.label.next_to(vv.circle, side, buff=0.2)
        v[key] = vv
    e = {k: S4.typed_edge(v[a], v[b], "ACTED_IN").arrow
         for k, a, b in [("coogan_kid", "coogan", "kid"), ("chaplin_kid", "chaplin", "kid"),
                         ("chaplin_gold", "chaplin", "gold")]}
    g = VGroup(*v.values(), *e.values())
    g.v, g.e = v, e
    g.base = {id(m): m.get_stroke_color() for m in [*[vv.circle for vv in v.values()], *e.values()]}
    return g


class GraphInTables(NarratedScene):
    def construct(self):
        # ---- layout A (c1.tables.1): s4's drawing on top at 0.72, the DDL at 24 below it
        dk = S4.chaplin_kid().scale(0.72)
        dk.shift([-dk.get_center()[0], 3.55 - dk.get_top()[1], 0])
        self.dk = dk
        f24 = Code(DDL, size=24, lang="sql")
        f24.shift([-5.5 - f24.get_left()[0], dk.get_bottom()[1] - 0.25 - f24.get_top()[1], 0])
        self.f24 = f24
        # ---- layout B (c1.tables.2): compact drawing (no vertex cards) at 0.7, the DDL at 21
        cx, kx = S4.CX, S4.KX
        S4.CX, S4.KX = -4.5, 4.5           # wider apart, so the roles card fits between the names
        dk2 = S4.chaplin_kid()
        S4.CX, S4.KX = cx, kx
        dk2.remove(dk2.ccard, dk2.kcard)
        dk2.roles.next_to(dk2.edge.arrow, DOWN, buff=0.25)      # under the arrow, between the names
        dk2.scale(0.72)
        dk2.shift([-dk2.get_center()[0], 3.6 - dk2.get_top()[1], 0])
        self.dk2 = dk2
        full = sql(DDL)
        full.shift([-6.6 - full.get_left()[0], 1.8 - full.get_top()[1], 0])
        self.full = full
        self.clip_vertices()
        self.clip_edges()
        self.clip_indexes()
        self.clip_query()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1.tables.1
    def clip_vertices(self):
        dk, f24 = self.dk, self.f24

        def s24(src):
            return Code(src, size=24, lang="sql")
        with self.say("c1.tables.1") as c:
            self.play(FadeIn(dk), run_time=1.0)  # early: the drawing is the subject, not a label
            c.wait_until("two tables")
            V = put(s24(partial(V_SRC, 0)), anchor(f24, 0))
            E = put(s24(partial(E_SRC, 0)), anchor(f24, 6))
            self.play(*appear(V, E, lag=0.4), run_time=1.4)
            c.wait_until("vneeds")

            V1 = put(s24(partial(V_SRC, 1)), anchor(f24, 0))
            box = token_box(V1.find("vertex_id"), V1.line(1))
            self.play(*edit(V, V1), FadeIn(box), lit(dk.chaplin.circle), lit(dk.kid.circle),
                      run_time=min(1.5, 0.7 * c.until("vlabel")))
            V = V1
            c.wait_until("vlabel")

            V2 = put(s24(partial(V_SRC, 2)), anchor(f24, 0))
            self.play(*edit(V, V2), Transform(box, token_box(V2.find("label"), V2.line(2))),
                      unlit(dk.chaplin.circle), unlit(dk.kid.circle), lit(dk.ctag), lit(dk.ktag),
                      run_time=c.until("vprops", floor=0.6))
            V = V2

            V3 = put(s24(partial(V_SRC, 3)), anchor(f24, 0))
            self.play(*edit(V, V3), Transform(box, token_box(V3.find("properties"), V3.line(3))),
                      unlit(dk.ctag), unlit(dk.ktag), lit(dk.ccard), lit(dk.kcard), run_time=1.5)
            V = V3
            c.wait_until("same type")
            self.play(FlashAround(V.find("JSON"), color=TEAL, time_width=1.5),
                      FlashAround(V.find('{"name": "Charles Chaplin"}'), color=TEAL, time_width=1.5),
                      run_time=1.6)
        self.V, self.E, self.box = V, E, box

    # ------------------------------------------------------------ c1.tables.2
    def clip_edges(self):
        dk, dk2, full, V, E, box = self.dk, self.dk2, self.full, self.V, self.E, self.box
        k = CS / 24
        low = full.copy().shift(0.6 * DOWN)      # while the fan is up, the DDL sits a little lower
        with self.say("c1.tables.2") as c:
            # the drawing leaves, the DDL settles at 21 on the left
            for b, i in ((V, 0), (E, 6)):
                b.generate_target()
                b.target.scale(k)
                put(b.target, anchor(low, i))
            self.play(*during(disappear(dk), 0, 0.45), FadeOut(box),
                      *during([MoveToTarget(V), MoveToTarget(E)], 0.2, 1), run_time=1.2)
            E1 = put(sql(partial(E_SRC, 1)), anchor(low, 6))
            box = token_box(E1.find("edge_id"), E1.line(1))
            self.play(*edit(E, E1), FadeIn(box), run_time=1.4)
            E = E1

            fan = S5.fan().scale(0.71)
            fan.shift([-fan.get_center()[0], 3.6 - fan.get_top()[1], 0])
            c.wait_until("five edges")
            self.play(*appear(fan, shift=None), run_time=1.2)  # early: the fan's types are seen, not read
            c.wait_until("same two ends")
            self.play(*flash([fan.chaplin.circle, fan.kid.circle]), run_time=1.2)
            c.wait_until("tail")

            E2 = put(sql(partial(E_SRC, 2)), anchor(full, 6))
            self.play(*edit(E, E2), Transform(box, token_box(E2.find("tail_vertex"), E2.line(2))),
                      *during(disappear(fan), 0, 0.45), *during([V.animate.shift(0.6 * UP)], 0.3, 0.8),
                      *during(appear(dk2, shift=None), 0.5, 1),
                      run_time=1.6)
            E = E2
            dk = dk2
            arrow = dk.edge.arrow
            ttag = end_tag("tail", arrow.get_start(), LEFT)
            c.wait_until(own_word=ttag.text)
            self.play(*appear(ttag), run_time=0.9)
            c.wait_until("head")

            E3 = put(sql(partial(E_SRC, 3)), anchor(full, 6))
            self.play(*edit(E, E3), Transform(box, token_box(E3.find("head_vertex"), E3.line(3))),
                      run_time=1.4)
            E = E3
            htag = end_tag("head", arrow.get_end(), RIGHT)
            c.wait_until(own_word=htag.text)
            self.play(*appear(htag), run_time=0.8)
            c.wait_until("etype")

            E4 = put(sql(partial(E_SRC, 4)), anchor(full, 6))
            self.play(*edit(E, E4), Transform(box, token_box(E4.find("type"), E4.line(4))),
                      lit(dk.edge.label), run_time=c.until("eprops", floor=0.6))
            E = E4

            E5 = put(sql(partial(E_SRC, 5)), anchor(full, 6))
            self.play(*edit(E, E5), Transform(box, token_box(E5.find("properties"), E5.line(5))),
                      unlit(dk.edge.label), lit(dk.roles), run_time=1.5)
            E = E5
            c.wait_until("again as json")
            self.play(FlashAround(E.find("JSON"), color=TEAL, time_width=1.5), run_time=1.2)
            c.wait_until("fk")

            refs = [E.find("REFERENCES vertices(vertex_id)", line=i) for i in (2, 3)]
            self.play(FadeOut(box), unlit(dk.roles), *disappear(ttag, htag), *recolor(refs[0], YELLOW),
                      *recolor(refs[1], YELLOW), *flash(refs), run_time=1.2)
            tgt = V.line(1).get_right() + 0.18 * RIGHT
            fks = VGroup()
            for j, (r, x) in enumerate(zip(refs, (3.15, 3.45))):
                y0 = E.line(2 + j).get_y()
                y1 = tgt[1] + (0.07 if j == 0 else -0.07)
                start = E.line(2 + j).get_right() + 0.15 * RIGHT
                path = VGroup(Line(start, [x, y0, 0]), Line([x, y0, 0], [x, y1, 0]),
                              Arrow([x, y1, 0], [tgt[0], y1, 0], buff=0, stroke_width=3,
                                    max_tip_length_to_length_ratio=0.06))
                path.set_color(YELLOW).set_stroke(width=3)
                fks.add(path)
            self.play(*[Create(p) for p in fks], run_time=1.6)
            self.play(FlashAround(V.find("vertex_id"), time_width=1.5), run_time=1.2)
            c.wait_until("onelabel")

            note = VGroup(T("one label each:", 28, DIM), T("a simplification", 28, DIM),
                          T("(a vertex may", 28, DIM), T("have several)", 28, DIM)
                          ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            note.align_to(V.line(0), UP).align_to([3.8, 0, 0], LEFT)
            self.play(*appear(note), FlashAround(V.find("label"), color=DIM), run_time=1.2)  # early: the note lands with its sentence
        self.E, self.fks, self.note, self.dk = E, fks, note, dk

    # ------------------------------------------------------------ c1.tables.3
    def relight(self, g, new):
        """YELLOW on the parts in `new`, base colour back on the lit parts not in it."""
        anims = [m.animate.set_color(g.base[id(m)]) for m in self.lit_now if m not in new]
        anims += [m.animate.set_color(YELLOW) for m in new if m not in self.lit_now]
        self.lit_now = list(new)
        return anims

    def clip_indexes(self):
        dk, full, V, E, fks, note = self.dk, self.full, self.V, self.E, self.fks, self.note
        up = np.array([0, 0.6 - E.get_top()[1], 0])
        g = tangle()
        v, e = g.v, g.e
        outs = [v["chaplin"].circle, e["chaplin_kid"], e["chaplin_gold"]]
        ins = [v["kid"].circle, e["coogan_kid"], e["chaplin_kid"]]
        self.lit_now = []

        def sweep(arrows):
            return [VShowPassingFlash(Line(a.get_start(), a.get_end()).set_stroke(YELLOW, 8),
                                      time_width=0.6) for a in arrows]
        with self.say("c1.tables.3") as c:
            q = T("?", 96, YELLOW).move_to([0, 3.0, 0])
            self.play(*during(disappear(V, *fks, dk, note), 0, 0.45),
                      *during([E.animate.shift(up)], 0.3, 0.8),
                      *during(appear(g, q, shift=None, lag=0.2), 0.5, 1), run_time=1.8)  # early: the ? stands for the question
            c.wait_until("out")

            self.play(*disappear(q), *self.relight(g, outs), *sweep(outs[1:]), run_time=1.4)
            c.wait_until("into")
            self.play(*self.relight(g, ins), *sweep(ins[1:]), FlashAround(v["kid"].circle), run_time=1.4)
            c.wait_until("one on the tail column")

            I1 = put(sql(I_SRC[0]), anchor(full, 14) + up)
            I2 = put(sql(I_SRC[1]), anchor(full, 15) + up)
            self.play(*appear(I1), *self.relight(g, outs), *sweep(outs[1:]), run_time=1.2)
            self.play(FlashAround(I1.find("tail_vertex"), time_width=1.5), run_time=1.0)
            c.wait_until("one on the head column")
            self.play(*appear(I2), *self.relight(g, ins), *sweep(ins[1:]), run_time=1.2)
            self.play(FlashAround(I2.find("head_vertex"), time_width=1.5), run_time=1.0)
            c.wait_until("either")

            # ---- layout C: the whole of Slide 96 on the left, the edges table as a stack on the right
            final = full.copy()
            final.shift([-6.5 - final.get_left()[0], -final.get_center()[1], 0])
            Vf = put(V.copy(), anchor(final, 0))
            self.play(*during(disappear(g), 0, 0.4),
                      *during([E.animate.shift(anchor(final, 6) - anchor(E, 0)),
                               I1.animate.shift(anchor(final, 14) - anchor(I1, 0)),
                               I2.animate.shift(anchor(final, 15) - anchor(I2, 0))], 0.1, 0.6),
                      *during(appear(Vf, shift=None), 0.6, 1), run_time=1.8)
            V = Vf

            bars = edge_stack().move_to([5.25, -0.35, 0])
            count = T("49,811 edges", 34, GOLD).next_to(bars, UP, buff=0.25)
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.04), *appear(count),
                      run_time=1.4)  # early: the count names the stack it labels
            c.wait_until("either direction")

            outs_b, ins_b = bars[6:11], bars[15:18]
            j1 = CurvedArrow(I1.get_right() + 0.15 * RIGHT, outs_b.get_left() + 0.1 * LEFT, angle=0.7,
                             color=YELLOW, stroke_width=3, tip_length=0.2)
            j2 = CurvedArrow(I2.get_right() + 0.15 * RIGHT, ins_b.get_left() + 0.1 * LEFT, angle=0.4,
                             color=YELLOW, stroke_width=3, tip_length=0.2)
            self.play(Create(j1), Create(j2), *[b.animate.set_fill(YELLOW, 0.7).set_stroke(YELLOW)
                                                  for b in [*outs_b, *ins_b]], run_time=1.6)
        self.V, self.E, self.I1, self.I2 = V, E, I1, I2
        self.stack = [bars, count, j1, j2]

    # ------------------------------------------------------------ c1.tables.4
    def clip_query(self):
        blocks = [self.V, self.E, self.I1, self.I2]
        P = VGroup(*[b.copy() for b in blocks]).get_corner(UL)
        k = 0.36
        Q0 = np.array([-6.5, 3.5, 0])
        with self.say("c1.tables.4") as c:
            Qc = sql(Q_SRC)
            Qc.shift([6.5 - Qc.get_right()[0], 3.5 - Qc.get_top()[1], 0])
            self.play(*during(disappear(*self.stack), 0, 0.35),
                      *during([b.animate.scale(k, about_point=P).shift(Q0 - P).set_opacity(0.6)
                               for b in blocks], 0.15, 0.6),
                      *during(appear(Qc), 0.6, 1), run_time=min(2.0, c.until("start")))
            c.wait_until("start")

            self.play(*recolor(Qc.line(1), BLUE), *recolor(Qc.find("m.properties->>'title' = 'The Kid'"), BLUE),
                      run_time=1.0)
            c.wait_until("e")
            self.play(*recolor(Qc.line(2), YELLOW), *recolor(Qc.find("e.type = 'ACTED_IN'"), YELLOW),
                      run_time=1.0)
            c.wait_until("p")
            self.play(*recolor(Qc.line(3), PINK), run_time=1.0)
            c.wait_until("rows")

            # ---- the ten rows, as a graph
            kid = Circle(radius=0.5).set_stroke(BLUE, 4).set_fill(BLUE, 0.2).move_to([0, -0.9, 0])
            kname = T("The Kid", 30).next_to(kid, DOWN, buff=0.15)
            etl = Mono("ACTED_IN", 28, DIM).next_to(kid, UP, buff=0.55)
            units = []
            for i, name in enumerate(ACTORS):
                side = LEFT if i < 5 else RIGHT
                y = 0.6 - 0.8 * (i % 5)
                p = Circle(radius=0.25).set_stroke(PINK, 4).set_fill(PINK, 0.2).move_to([3.3 * side[0], y, 0])
                lab = T(name, 28).next_to(p, side, buff=0.18)
                d = normalize(kid.get_center() - p.get_center())
                a = small_arrow(p.get_center() + d * 0.31, kid.get_center() - d * 0.58)
                units.append(VGroup(p, a, lab))
            self.play(*appear(kid, kname, etl, shift=None, lag=0.1), run_time=0.8)
            self.play(*appear(*units, shift=None, lag=0.12), run_time=1.8)  # early: the rows come out together
            rows = T("10 rows", 32, GOLD).next_to(kname, DOWN, buff=0.2)
            self.play(*appear(rows), run_time=0.8)
            c.wait_until("joins")

            jl = [Qc.line(2), Qc.line(3)]
            two = T("one edge = two joins", 36, GOLD).move_to([0, -3.35, 0])
            self.play(*flash(jl, color=GOLD, time_width=1.5), *during(appear(two), 0.3, 1), run_time=1.5)
            c.wait_until("generic")

            # ---- what we've gained
            gt = graph_tables().move_to([3.55, -0.6, 0])
            sweep_clear(self, *appear(gt, shift=None), run_time=1.6)
            c.wait_until("seven tables")
            seven = S5.seven_tables()
            seven.set_color(DIM)
            seven.scale_to_fit_width(min(5.6, seven.width))
            if seven.height > 5.4:
                seven.scale_to_fit_height(5.4)
            seven.move_to([-3.6, -0.6, 0])
            self.play(*appear(seven, shift=None), run_time=1.2)
            mfm = T("made for movies", 34, DIM).move_to([-3.6, 2.9, 0])
            c.wait_until(own_word=mfm)
            self.play(*appear(mfm), run_time=1.0)
            c.wait_until("these two")

            s3 = load_scene("ch1_s3_shapes") if _has("ch1_s3_shapes", "thumbnails") else None
            th = VGroup(*[t.drawing.copy() for t in s3.thumbnails().tiles]) if s3 else VGroup(*[S4.tiny_graph().scale(0.4) for _ in range(6)])
            for t in th:
                t.scale_to_fit_height(min(0.85, t.height))
                if t.width > 0.95:
                    t.scale_to_fit_width(0.95)
            th.arrange(RIGHT, buff=0.2).move_to([3.5, 2.9, 0])
            self.play(*appear(*th, lag=0.12), run_time=1.0)
            ag = T("any graph", 44, GOLD).move_to([3.5, 2.9, 0])
            c.wait_until("any graph")
            drops = [t.animate.scale(0.15).move_to(gt.vcard.box.get_top()).set_opacity(0) for t in th]
            self.play(LaggedStart(*drops, lag_ratio=0.1), *during(appear(ag), 0.65, 1),
                      *flash([gt.vcard.box, gt.ecard.box], color=GOLD), run_time=1.8)
            self.remove(*th)


def _has(stem, name):
    p = Path(__file__).resolve().parent / f"{stem}.py"
    return p.exists() and f"def {name}(" in p.read_text()
