"""Chapter 1, scene 8: recap in one row of five panels, then ch2's opening card. Clips c1.recap.1 – c1.recap.2.

Layout: five DIM frames in one row appear on {recap}; each fills on its sentence with a shrunken copy
of the object that taught it (helpers from s2-s6), its line underneath.
{next}: the row dims and shrinks to a strip at the top; s4's Chaplin -> The Kid grows out of its panel
to the centre, then turns into ch2's Cypher line: circles shrink away where the round brackets come
in, the tag texts and ACTED_IN fly down into the code. The last ~8 s are exactly
load_scene("ch2_s1_hook").open_card() (reversed join; chapter end, no handover mark); the dimmed strip
fades in the first second of that hold.
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

# ── one row of five frames ─────────────────────────────────────────────────────────
PW, PH, PY = 2.5, 5.5, 0.45
CENTRES = [np.array([x, PY, 0]) for x in (-5.4, -2.7, 0.0, 2.7, 5.4)]
IW = 2.2                       # interior width for the drawings
LINES = ["a row per job,\ntwo copies", "chains of\nedges", "labels, types,\nproperties",
         "a row =\nan edge", "two tables"]
CAP = 28


def frame(i):
    return RoundedRectangle(corner_radius=0.2, width=PW, height=PH).set_stroke(DIM, 2, opacity=0.6) \
        .move_to(CENTRES[i])


def caption(i, fr):
    return T(LINES[i], CAP, FG, line_spacing=0.8).next_to(fr, DOWN, buff=0.2)


def fit(mob, w, h, centre):
    s = min(w / mob.width, h / mob.height)
    mob.scale(s).move_to(centre)
    return mob


def hp_card():
    """s2's has_position card in mini_table style: Chaplin's five rows."""
    t = T("has_position", 30, BLUE)
    rows = VGroup(*[Line(LEFT * 0.9, RIGHT * 0.9).set_stroke(DIM, 6) for _ in range(5)]).arrange(DOWN, buff=0.24)
    box = RoundedRectangle(corner_radius=0.1, width=2.5, height=rows.height + 0.5).set_stroke(BLUE, 3) \
        .set_fill(BLUE, 0.06)
    rows.move_to(box)
    t.next_to(box, UP, buff=0.15)
    return VGroup(box, t, rows)


def grid_drawings(s3):
    """s3's six drawings (end-of-tour state, no captions/tags), 2 columns x 3 rows; nothing lit yet.
    Returns (group, roads chain parts)."""
    ds = []
    for i, b in enumerate(s3.BUILDERS):
        d = b()
        if i == 0:
            d.remove(d.follow_line)
            d.add_to_back(d.follow)
            d.add(d.follow_label)
        if i == 4:
            d.add(d.card)
        ds.append(d)
    road_lit = ds[2].lit
    for k, d in enumerate(ds):              # one upright column, so each drawing is as wide as the panel
        d.move_to([0, 5.0 - 2.0 * k, 0])
    return VGroup(*ds), road_lit


def tall_chaplin_kid(s4):
    """s4's Chaplin -ACTED_IN-> The Kid, stood upright to fit a panel: tags right of the circles,
    the type and its roles card right of the edge."""
    ch = s4.vertex("Charles Chaplin", "Person", at=[0, 2.6, 0])
    kid = s4.vertex("The Kid", "Movie", at=[0, -2.6, 0])
    ch.label.next_to(ch.circle, UP, buff=0.18)
    ctag = s4.label_tag(":Person").next_to(ch.circle, RIGHT, buff=0.2)
    ktag = s4.label_tag(":Movie").next_to(kid.circle, RIGHT, buff=0.2)
    edge = s4.typed_edge(ch, kid, "ACTED_IN")
    # the edge's type and its roles card sit on the edge itself (the panel is too narrow beside it)
    edge.label.next_to(edge.arrow, RIGHT, buff=0.2).set_y(edge.arrow.get_center()[1] + 0.55)
    roles = s4.prop_card([("roles", "['A Tramp']")], color=GOLD).next_to(edge.label, DOWN, buff=0.2) \
        .set_x(edge.arrow.get_x())
    roles.add_to_back(BackgroundRectangle(roles, color=BG, fill_opacity=1, buff=0))
    roles.set_z_index(1)
    g = VGroup(ch, ctag, kid, ktag, edge, roles)
    g.chaplin, g.ctag, g.kid, g.ktag, g.edge, g.roles = ch, ctag, kid, ktag, edge, roles
    return g


def small_fan(s4, s5):
    """s5's fan, stood upright: Chaplin (top) to The Kid (bottom), five edges bulging right of the straight one."""
    ch = s4.vertex("Charles Chaplin", "Person", at=[0, 1.5, 0])
    kid = s4.vertex("The Kid", "Movie", at=[0, -1.5, 0])
    ch.label.next_to(ch.circle, UP, buff=0.18)
    kid.label.next_to(kid.circle, DOWN, buff=0.18)
    cc, kc, r = ch.circle.get_center(), kid.circle.get_center(), 0.56
    lanes = VGroup()
    for k in range(5):
        a = np.radians(18 * k)
        S = cc + r * np.array([np.sin(a), -np.cos(a), 0])
        E = kc + r * np.array([np.sin(a), np.cos(a), 0])
        path = Line(S, E) if k == 0 else ArcBetweenPoints(S, E, angle=-0.55 * k)
        pts = path.get_points()
        d = pts[-1] - pts[-2] if np.linalg.norm(pts[-1] - pts[-2]) > 1e-6 else E - S
        tip = s5.arrow_tip(E, d, FG)
        path.set_stroke(FG, 4)
        lanes.add(VGroup(path, tip))
    g = VGroup(kid, ch, lanes)
    g.kid, g.chaplin, g.lanes = kid, ch, lanes
    return g


class Recap(NarratedScene):
    def construct(self):
        s2 = load_scene("ch1_s2_lasttime")
        s3 = load_scene("ch1_s3_shapes")
        s4 = load_scene("ch1_s4_propgraph")
        s5 = load_scene("ch1_s5_moviegraph")
        s6 = load_scene("ch1_s6_tables")
        frames = [frame(i) for i in range(5)]
        caps = [caption(i, f) for i, f in enumerate(frames)]
        C = CENTRES

        with self.say("c1.recap.1") as c:
            # {recap}: the five empty frames
            self.play(*appear(*frames, shift=None, lag=0.15), run_time=min(1.2, c.until("r1")))
            c.wait_until("r1")

            # {r1}: the tangle under the has_position card, then the two document cards below
            hp = fit(hp_card(), 2.1, 1.7, C[0] + 1.55 * UP)
            tg = s2.tangle()
            for v in tg.v.values():
                v.remove(v.label)
            fit(tg, IW, 1.5, C[0] + 0.15 * DOWN)
            dk, dc = s2.mini_doc("The Kid"), s2.mini_doc("Chaplin")
            docs = VGroup(dk, dc).arrange(RIGHT, buff=0.25)
            fit(docs, IW, 1.4, C[0] + 1.75 * DOWN)
            self.play(*appear(tg, hp, lag=0.3), run_time=min(1.5, c.until("documents")))  # early: the join table the sentence names (its name is said in r4)
            c.wait_until("documents")
            self.play(*appear(dk, dc, lag=0.3), run_time=min(1.2, c.until("twice")))
            c.wait_until("twice")
            self.play(*appear(caps[0]), *flash([dk, dc], color=TEAL, run_time=1.4, time_width=1.5),
                      run_time=min(1.4, c.until("r2")))
            c.wait_until("r2")

            # {r2}: s3's grid of graphs; one chain turns YELLOW on "follow chains"
            grid, road_lit = grid_drawings(s3)
            fit(grid, IW, 5.0, C[1])
            self.play(*appear(grid, shift=None), run_time=min(1.2, c.until("follow chains")))
            c.wait_until("follow chains")
            self.play(*recolor(road_lit, YELLOW), *appear(caps[1]), run_time=min(1.2, c.until("your data")))
            c.wait_until("r3")

            # {r3}: Chaplin -> The Kid: vertices and edge, then the labels, then the property cards
            ck = fit(tall_chaplin_kid(s4), IW, 5.0, C[2])
            self.play(*appear(ck.chaplin, ck.kid, ck.edge, shift=None, lag=0.2),
                      run_time=min(1.2, c.until("labelled")))
            c.wait_until("labelled")
            self.play(*appear(ck.ctag, ck.ktag, lag=0.2), run_time=min(1.0, c.until("typed")))
            c.wait_until("typed")
            self.play(FlashUnder(ck.edge.label, color=YELLOW, time_width=1.5),
                      run_time=min(1.2, c.until("carrying")))
            c.wait_until("carrying")
            self.play(*appear(ck.roles, shift=None), *appear(caps[2]),
                      run_time=min(1.3, c.until("r4")))
            settle(self, ck)
            c.wait_until("r4")

            # {r4}: s5's fan of five edges; the GOLD row = edge count
            fn = fit(small_fan(s4, s5), IW, 3.7, C[3] + 0.55 * UP)
            note = T("49,811 rows\n= 49,811 edges", 28, GOLD, line_spacing=0.8)
            note.scale_to_fit_width(min(note.width, IW)).move_to(C[3] + 2.0 * DOWN)
            self.play(*appear(fn, shift=None), run_time=min(1.2, c.until("one edge")))
            c.wait_until("one edge")
            self.play(*appear(note, caps[3], lag=0.3), run_time=min(1.3, c.until("r5")))
            c.wait_until("r5")

            # {r5}: s6's two table cards with their index tags; GOLD 2 joins per edge
            gt = s6.graph_tables()
            VGroup(gt.tails_tag, gt.heads_tag).arrange(DOWN, buff=0.15).next_to(gt.ecard, DOWN, buff=0.25)
            fit(gt, IW, 3.9, C[4] + 0.5 * UP)
            two = T("2 joins\nper edge", 28, GOLD, line_spacing=0.8).move_to(C[4] + 2.05 * DOWN)
            self.play(*appear(gt.vcard, gt.ecard, caps[4], lag=0.25), run_time=min(1.2, c.until("two indexes")))
            c.wait_until("two indexes")
            self.play(*flash([gt.tails_tag, gt.heads_tag], run_time=1.3, time_width=1.5),
                      *appear(gt.tails_tag, gt.heads_tag, lag=0.2), run_time=min(1.3, c.until("two joins")))
            c.wait_until("two joins")
            self.play(*appear(two), run_time=min(1.0, c.until()))

        with self.say("c1.recap.2") as c:
            card = load_scene("ch2_s1_hook").open_card()
            code = card[0]
            g_person = code.find(":Person")
            g_acted = code.find("ACTED_IN")
            g_movie = code.find(":Movie")
            taken = {id(m) for g in (g_person, g_acted, g_movie) for m in g}
            rest = [m for m in code.text if id(m) not in taken]

            # the big drawing: circles where the round brackets will be, the arrow between them
            big = s4.chaplin_kid()
            pc, mc = code.find("(p:Person)").get_center(), code.find("(m:Movie)").get_center()
            d0 = big.kid.circle.get_center() - big.chaplin.circle.get_center()
            big.scale((mc[0] - pc[0]) / d0[0])
            big.shift(pc - big.chaplin.circle.get_center())
            gone = [big.chaplin.label, big.kid.label, big.ccard, big.kcard, big.roles]
            for m in gone:
                m.set_opacity(0)

            # {next}: the row dims and rises to a strip; Chaplin -> The Kid grows out of its panel
            strip = VGroup(*frames, *caps, hp, tg, dk, dc, grid, ck, fn, note, gt, two)
            settle(self, strip)
            dim = restyle(strip, op=DIMMED)
            dim.target_mobject.scale(0.36).move_to(UP * 2.35)
            seed = dim.target_mobject[len(frames) + len(caps) + 5].get_center()     # panel 3 in the strip
            keep = [big.chaplin.circle, big.kid.circle, big.ctag, big.ktag, big.edge]
            bc = VGroup(*keep).get_center()
            self.play(*during([dim], 0, 0.5),
                      *during([FadeIn(m, target_position=seed + 0.3 * (m.get_center() - bc), scale=0.3) for m in keep], 0.5, 1),
                      run_time=min(1.6, c.until("in a language")))
            c.wait_until("where the query")

            # the drawing becomes the query: brackets where the circles were, the arrow where the arrow was
            self.play(*during([big.chaplin.circle.animate.scale(0.4).set_opacity(0),
                               big.kid.circle.animate.scale(0.4).set_opacity(0),
                               FadeOut(big.edge.arrow), FadeOut(big.ctag.box), FadeOut(big.ktag.box)], 0, 0.45),
                      *during([Transform(big.ctag.text, g_person.copy()), Transform(big.ktag.text, g_movie.copy()),
                               Transform(big.edge.label, g_acted.copy())], 0.1, 0.75),
                      *during([FadeIn(m) for m in rest], 0.45, 1),
                      run_time=min(1.6, c.until(floor=1.0)))

        # end card: exactly ch2's opening card; the dimmed strip fades, then the card alone ~8 s
        self.remove(*[m for m in self.mobjects if m is not strip and isinstance(m, VMobject)])
        self.add(card)
        self.play(FadeOut(strip), run_time=1.0)
        self.wait(7.5)
