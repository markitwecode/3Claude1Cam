"""Chapter 1, scene 4: the property graph model. Clips c1.prop.1 – c1.prop.4.

Exports the graph look for later scenes (load_scene("ch1_s4_propgraph")):
  vertex(name, kind="Person", at=ORIGIN, r=0.5)      VGroup(circle, label); .circle .label
  label_tag(text, color=FG)                          VGroup(box, text); .box .text  (":Person")
  tag_on(tag, v)                                     puts the tag just above v's circle
  prop_card(pairs, color=FG, slots=None)             VGroup(box, *rows); .box .rows
  card_under(card, v)                                puts the card under v's name
  slot_point(card, i)                                left-centre point of row slot i
  typed_edge(a, b, etype, color=FG, angle=0, side=UP, dashed=False)  VGroup(arrow, label); .arrow .label
  chaplin_kid()                                      the finished Chaplin -ACTED_IN-> The Kid picture
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
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- the graph look
KIND_COLOR = {"Person": PINK, "Movie": BLUE}
V_R = 0.5
NAME_SIZE = 30
TAG_SIZE = 30
CARD_SIZE = 28
PITCH = 0.5          # card row pitch
PADX, PADY = 0.25, 0.15
EDGE_SIZE = 28

CX, KX, VY = -3.7, 3.7, 0.6     # chaplin_kid() layout
NOTE_Y = -3.3


def vertex(name, kind="Person", at=ORIGIN, r=V_R):
    """Circle (stroke 4, fill 0.2 in the kind's colour) with its name under it."""
    col = KIND_COLOR.get(kind, kind)
    circle = Circle(radius=r).set_stroke(col, 4).set_fill(col, 0.2).move_to(at)
    label = T(name, size=NAME_SIZE).next_to(circle, DOWN, buff=0.18)
    g = VGroup(circle, label)
    g.circle, g.label, g.kind = circle, label, kind
    return g


def label_tag(text, color=FG):
    """A label like ':Person' in Mono, in a thin rounded box."""
    t = Mono(text, size=TAG_SIZE, color=color)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=0.5)
    box.set_stroke(color, 2).set_fill(color, 0).move_to(t)
    g = VGroup(box, t)
    g.box, g.text = box, t
    return g


def tag_on(tag, v):
    return tag.next_to(v.circle, UP, buff=0.15)


def prop_card(pairs, color=FG, slots=None):
    """Key-value card: rows 'key: value' in Mono 28, numbers GOLD; `slots` reserves empty rows."""
    n = max(len(pairs), slots or 0)
    rows = []
    for k, v in pairs:
        v = str(v)
        t2c = {v: GOLD} if v.isdigit() else {}
        rows.append(Mono(f"{k}: {v}", size=CARD_SIZE, t2c=t2c))
    w = max(r.width for r in rows) + 2 * PADX
    box = RoundedRectangle(corner_radius=0.12, width=w, height=n * PITCH + 2 * PADY)
    box.set_stroke(color, 2.5).set_fill(color, 0.08)
    top, left = box.get_top()[1], box.get_left()[0]
    for i, (r, (k, _)) in enumerate(zip(rows, pairs)):
        colon = r[len(k)]
        base = top - PADY - (i + 1) * PITCH + 0.15
        r.shift([left + PADX - r.get_left()[0], base - colon.get_bottom()[1], 0])
    g = VGroup(box, *rows)
    g.box, g.rows = box, rows
    return g


def card_under(card, v):
    return card.next_to(v.label, DOWN, buff=0.3)


def slot_point(card, i):
    top = card.box.get_top()[1]
    return np.array([card.box.get_left()[0] + PADX, top - PADY - (i + 0.5) * PITCH, 0])


def typed_edge(a, b, etype, color=FG, angle=0, side=UP, dashed=False):
    """Arrow rim to rim between two vertices, its type in Mono caps beside it.
    angle > 0 bends a left-to-right edge below the straight line (use side=DOWN)."""
    ca, cb = a.circle.get_center(), b.circle.get_center()
    ra, rb = a.circle.width / 2 + 0.06, b.circle.width / 2 + 0.06
    d = normalize(cb - ca)
    s = ca + rotate_vector(d, -angle / 2) * ra
    e = cb + rotate_vector(-d, angle / 2) * rb
    if angle:
        line = ArcBetweenPoints(s, e, angle=angle)
    elif dashed:
        line = DashedLine(s, e, dash_length=0.18, dashed_ratio=0.6)
    else:
        line = Line(s, e)
    line.set_stroke(color, 4)
    line.add_tip(tip_length=0.25, tip_width=0.25)
    line.tip.set_fill(color, 1).set_stroke(color, 1)
    label = Mono(etype, size=EDGE_SIZE, color=color).next_to(line, side, buff=0.12)
    g = VGroup(line, label)
    g.arrow, g.label, g.tail, g.head = line, label, s, e
    return g


def chaplin_kid():
    """(:Person Chaplin)-[:ACTED_IN {roles}]->(:Movie The Kid), tags and cards, full size."""
    ch = vertex("Charles Chaplin", "Person", at=[CX, VY, 0])
    kid = vertex("The Kid", "Movie", at=[KX, VY, 0])
    ctag = tag_on(label_tag(":Person"), ch)
    ktag = tag_on(label_tag(":Movie"), kid)
    ccard = card_under(prop_card([("name", "Charles Chaplin"), ("birthyear", "1889")]), ch)
    kcard = card_under(prop_card([("title", "The Kid"), ("year", "1921")]), kid)
    edge = typed_edge(ch, kid, "ACTED_IN")
    roles = prop_card([("roles", "['A Tramp']")], color=GOLD).next_to(edge.label, UP, buff=0.2)
    g = VGroup(ch, ctag, ccard, kid, ktag, kcard, edge, roles)
    g.chaplin, g.ctag, g.ccard, g.kid, g.ktag, g.kcard, g.edge, g.roles = \
        ch, ctag, ccard, kid, ktag, kcard, edge, roles
    return g


def grow_edge(line):
    """Grow a tipped edge from its tail (GrowArrow wants an Arrow)."""
    return GrowFromPoint(line, line.get_start())


def tiny_table():
    w, h, rows = 2.8, 2.0, 4
    frame = Rectangle(width=w, height=h).set_stroke(BLUE, 3)
    head = Rectangle(width=w, height=h / rows).set_stroke(BLUE, 0).set_fill(BLUE, 0.45)
    head.align_to(frame, UP)
    lines = VGroup(*[Line(frame.get_left(), frame.get_right()).set_stroke(BLUE, 2)
                     .shift(UP * (h / 2 - i * h / rows)) for i in range(1, rows)],
                   *[Line(frame.get_top(), frame.get_bottom()).set_stroke(BLUE, 2)
                     .shift(RIGHT * (j * w / 3 - w / 2)) for j in (1, 2)])
    return VGroup(head, lines, frame)


def tiny_graph():
    def dot(col, p):
        return Circle(radius=0.3).set_stroke(col, 3).set_fill(col, 0.2).move_to(p)
    a, b, c = dot(PINK, [-1.0, 0.6, 0]), dot(BLUE, [1.0, 0.6, 0]), dot(PINK, [0, -0.7, 0])

    def arr(x, y):
        d = normalize(y.get_center() - x.get_center())
        ln = Line(x.get_center() + d * 0.36, y.get_center() - d * 0.36).set_stroke(FG, 3)
        ln.add_tip(tip_length=0.18, tip_width=0.18)
        return ln
    return VGroup(a, b, c, arr(a, b), arr(c, b), arr(c, a))


# ---------------------------------------------------------------- the scene
class PropertyGraph(NarratedScene):
    def construct(self):
        pg = chaplin_kid()
        ch, ctag, ccard = pg.chaplin, pg.ctag, pg.ccard
        kid, ktag, kcard = pg.kid, pg.ktag, pg.kcard
        edge, roles = pg.edge, pg.roles
        ctag.set_color(YELLOW)
        ktag.set_color(YELLOW)
        heading = T("The property graph model", size=48).to_edge(UP, buff=0.45)

        # ---- c1: a vertex, its label, its properties
        with self.say("c1.prop.1") as c:
            c.wait_until("property graph")
            self.play(*appear(heading), run_time=1.0)
            c.wait_until("vertex")
            self.play(GrowFromCenter(ch.circle), run_time=1.2)
            c.wait_until(own_word=ctag.text)
            self.play(*appear(ctag), run_time=1.0)
            c.wait_until("which says")
            self.play(ctag.animate.set_color(FG), run_time=1.0)
            note1 = T("one or more labels", size=30, color=DIM).move_to([0, NOTE_Y, 0])
            c.wait_until("several labels")
            self.play(*appear(note1), run_time=1.0)
            c.wait_until("props")
            self.play(FadeIn(ccard.box), run_time=1.0)
            c.wait_until(own_word=ccard.rows[0])
            self.play(*appear(ccard.rows[0], ch.label, lag=0.4), run_time=1.4)
            c.wait_until("birth year")
            self.play(*appear(ccard.rows[1]), run_time=1.0)
            settle(self, ccard)

            json = Mono('{"name": "Charles Chaplin", "birthyear": 1889}', size=CARD_SIZE,
                        t2c={"{": TEAL, "}": TEAL, "1889": GOLD}).move_to([0, -2.55, 0])
            note2 = T("usually flat", size=30, color=DIM).move_to(note1)
            card_back = ccard
            c.wait_until("json")
            self.play(*appear(json), run_time=1.2)
            c.wait_until("usually flat")
            self.play(*swap(note1, note2), run_time=1.2)

        # ---- c2: a second vertex, the edge, its type, the role on the edge
        with self.say("c1.prop.2") as c:
            self.play(GrowFromCenter(kid.circle), *appear(ktag), run_time=1.0)
            self.play(ktag.animate.set_color(FG), run_time=0.6)
            c.wait_until("The Kid")
            self.play(*appear(kid.label, kcard, lag=0.4), run_time=1.3)
            c.wait_until("edge")
            self.play(grow_edge(edge.arrow), *disappear(json), run_time=1.6)
            c.wait_until("Chaplin")
            self.play(Flash(edge.tail, color=YELLOW, flash_radius=0.3, line_length=0.25), run_time=0.9)
            c.wait_until("ends at")
            self.play(Flash(edge.head, color=YELLOW, flash_radius=0.3, line_length=0.25), run_time=0.9)

            note3 = T("exactly one type · ALL_CAPS by convention", size=30, color=DIM).move_to(note2)
            c.wait_until(own_word=edge.label)
            self.play(*appear(edge.label), run_time=1.0)
            c.wait_until("by convention")
            self.play(*swap(note2, note3), run_time=1.2)

            final_roles = roles.get_center()
            roles.move_to([0, 2.45, 0])
            c.wait_until("his role")
            self.play(*appear(roles), run_time=1.0)

            ghost_c = T("The Lone\nProspector", size=28, color=DIM, slant=ITALIC)
            ghost_c.next_to(ch.circle, LEFT, buff=0.3)
            ghost_k = T("The Child", size=28, color=DIM, slant=ITALIC).next_to(kid.circle, RIGHT, buff=0.3)
            c.wait_until("notchaplin")
            self.play(roles.animate.move_to([-1.2, 2.45, 0]), *appear(ghost_c), run_time=0.9)
            c.wait_until("The Kid has")
            self.play(roles.animate.move_to([1.2, 2.45, 0]), *appear(ghost_k), run_time=0.9)
            c.wait_until("onedge")
            self.play(roles.animate.move_to([0, 2.45, 0]), run_time=0.8)
            self.play(roles.animate.move_to(final_roles), run_time=1.2)
            c.wait_until("property of the edge")
            self.play(FlashAround(roles, color=GOLD, time_width=1.5), *disappear(ghost_c, ghost_k), run_time=1.2)

        # ---- c3: very relaxed: any links, several edges, no schema, no edge rules
        with self.say("c1.prop.3") as c:
            c.wait_until("relaxed")
            self.play(*disappear(note3), run_time=0.8)

            def rim(v, p):
                d = normalize(np.array(p) - v.circle.get_center())
                return v.circle.get_center() + d * (V_R + 0.06)
            out = Line(rim(ch, [-7.6, 1.6, 0]), [-7.6, 1.6, 0]).set_stroke(DIM, 3)
            out.add_tip(tip_length=0.22, tip_width=0.22)
            back = Line([-7.6, -0.3, 0], rim(ch, [-7.6, -0.3, 0])).set_stroke(DIM, 3)
            back.add_tip(tip_length=0.22, tip_width=0.22)
            c.wait_until("any")
            self.play(grow_edge(out), time_span(grow_edge(back), 0.6, 1.4), run_time=1.4)
            self.play(FadeOut(out), FadeOut(back), run_time=1.0)

            directed = typed_edge(ch, kid, "DIRECTED", angle=0.9, side=DOWN)
            c.wait_until("several")
            self.play(grow_edge(directed.arrow), run_time=1.6)
            c.wait_until(own_word=directed.label)
            self.play(*appear(directed.label), run_time=1.0)

            # no schema: Chaplin moves up-left, his card goes beside him
            c.wait_until("no schema")
            sweep_clear(self, ch.animate.shift([-1.3, 1.3, 0]), ctag.animate.shift([-1.3, 1.3, 0]),
                        card_back.animate.shift(RIGHT * (-3.2 - card_back.get_left()[0])),
                        keep=[ch, ctag, card_back], run_time=1.8)
            self.play(card_back.animate.shift(UP * (2.65 - card_back.get_top()[1])), run_time=1.0)

            card3 = prop_card([("name", "Charles Chaplin"), ("birthyear", "1889"), ("deathyear", "1977")])
            card3.shift(card_back.box.get_corner(UL) - card3.box.get_corner(UL))
            c.wait_until("death year")
            self.play(ReplacementTransform(card_back.box, card3.box), *appear(card3.rows[2]), run_time=1.2)
            self.remove(*card_back.get_family())
            settle(self, card3)

            jl = vertex("Jennifer Lawrence", "Person", at=[-5.0, -1.4, 0])
            jtag = tag_on(label_tag(":Person"), jl)
            jcard = prop_card([("name", "Jennifer Lawrence"), ("birthyear", "1990")], slots=3)
            jcard.shift(np.array([-3.2, -0.65, 0]) - jcard.box.get_corner(UL))
            c.wait_until("Jennifer")
            self.play(GrowFromCenter(jl.circle), *appear(jtag, jl.label, lag=0.3), run_time=1.0)
            self.play(*appear(jcard), run_time=1.0)
            gap = slot_point(jcard, 2)
            ptr = Arrow([3.3, gap[1], 0], [0.3, gap[1], 0], buff=0, stroke_width=4,
                        tip_length=0.25, color=GOLD)
            ptr_label = T("no key at all", size=30, color=GOLD).next_to(ptr, RIGHT, buff=0.15)
            c.wait_until("no death year")
            self.play(GrowArrow(ptr), *appear(ptr_label), run_time=1.2)

            # nothing says what an edge type may join
            kid2 = vertex("The Kid", "Movie", at=[-3.0, 0.9, 0])
            gold = vertex("The Gold Rush", "Movie", at=[3.0, 0.9, 0])
            k2tag, gtag = tag_on(label_tag(":Movie"), kid2), tag_on(label_tag(":Movie"), gold)
            c.wait_until("edge type")
            sweep_clear(self, *appear(kid2, k2tag, gold, gtag, lag=0.2), run_time=2.0)
            bad = typed_edge(kid2, gold, "ACTED_IN", color=RED, dashed=True)
            c.wait_until("an acted in edge")
            self.play(grow_edge(bad.arrow), *appear(bad.label), run_time=1.5)
            caption = T("stored without complaint", size=34, color=RED).move_to([0, -1.0, 0])
            c.wait_until("stores it")
            self.play(*appear(caption), run_time=1.0)

        # ---- c4: about as expressive as tables; the language is the difference
        with self.say("c1.prop.4") as c:
            table = tiny_table().move_to([-3.4, 0.6, 0])
            approx = MathTex(r"\approx", font_size=120, color=GOLD).move_to([0, 0.6, 0])
            graph = tiny_graph().move_to([3.4, 0.6, 0])
            c.wait_until("than tables")
            sweep_clear(self, *appear(table, approx, graph, lag=0.3, shift=None), run_time=2.0)
            same = T("can express about the same", size=32, color=DIM).move_to([0, -1.3, 0])
            c.wait_until("express")
            self.play(*appear(same), run_time=1.0)
            lang = T("the difference: the query language", size=40, color=YELLOW).move_to([0, -2.5, 0])
            c.wait_until("query language")
            self.play(*appear(lang), run_time=1.0)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
