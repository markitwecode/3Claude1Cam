"""Chapter 1, scene 3: data that forms a graph, and the six-tile tour. Clips c1.shapes.1 – c1.shapes.4.

Exports `thumbnails()`: the 3x2 grid in its end-of-tour state (`.tiles` in order social, web, roads,
software, knowledge, ours; each tile `.drawing .caption .tag` (tag None for knowledge and ours)).
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


# ---------------------------------------------------------------- grid layout
COL_X = [-4.6, 0.0, 4.6]
ROW_Y = [2.05, -1.2]
TAG_DY, CAP_DY = 1.25, -1.25
R = 0.2            # thumbnail vertex radius
R_VERT = 0.5       # s2 tangle circle radius
OURS_S = 0.47      # the tangle shrunk into the last tile
CAPTIONS = ["social network", "the web", "road network", "software", "knowledge graph (Wikidata)", "our movies"]
TAGS = ["friends of friends", "links → search ranking", "shortest route",
        "all transitive dependencies", None, None]


def slot(i):
    return np.array([COL_X[i % 3], ROW_Y[i // 3], 0.0])


def caption(i):
    return T(CAPTIONS[i], 30, FG).move_to(slot(i) + CAP_DY * UP)


def tag(i):
    if TAGS[i] is None:
        return None
    t = T(TAGS[i], 30, YELLOW).move_to(slot(i) + TAG_DY * UP)
    if t.get_left()[0] < -6.55:
        t.shift((-6.55 - t.get_left()[0]) * RIGHT)
    return t


def P(i, x, y):
    return slot(i) + np.array([x, y, 0.0])


def vert(p, color, r=R):
    return Circle(radius=r).set_stroke(color, 3).set_fill(color, 0.2).move_to(p)


def line(a, b, r=R):
    return Line(a.get_center(), b.get_center(), buff=r).set_stroke(FG, 3)


def arrow(a, b, r=R, color=FG):
    return Arrow(a.get_center(), b.get_center(), buff=r + 0.03, stroke_width=3, color=color,
                 tip_length=0.16, max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)


def along(text, a, b, side=1, color=FG, size=28, off=0.32):
    """A label lying along the segment a-b, on its left (side=1) or right (side=-1) normal."""
    t = T(text, size, color)
    d = b - a
    ang = np.arctan2(d[1], d[0])
    if ang > PI / 2:
        ang -= PI
    elif ang < -PI / 2:
        ang += PI
    t.rotate(ang)
    n = np.array([-np.sin(ang), np.cos(ang), 0.0])
    t.move_to((a + b) / 2 + side * off * n)
    return t


def path_through(mobs, color=YELLOW, width=8):
    return VMobject().set_points_as_corners([m.get_center() for m in mobs]).set_stroke(color, width)


# ---------------------------------------------------------------- the six drawings (base state)
def social():
    pts = [(-1.6, 0), (-0.5, 0.62), (-0.5, -0.62), (0.6, 0), (1.7, 0.6), (1.7, -0.6)]
    vs = [vert(P(0, x, y), PINK) for x, y in pts]
    es = {e: line(vs[e[0]], vs[e[1]]) for e in [(0, 1), (0, 2), (1, 3), (2, 3), (3, 4), (3, 5), (4, 5)]}
    d = VGroup(*es.values(), *vs)
    d.vs, d.es = vs, es
    d.follow_line = es[(2, 3)]
    d.follow = arrow(vs[2], vs[3])
    d.follow_label = T("follows", 28, FG).move_to(P(0, 0.45, -0.7))
    d.lit = [es[(0, 1)], es[(1, 3)], vs[3]]
    d.chain = [vs[0], vs[1], vs[3]]
    return d


def web():
    pts = [(-1.6, 0.55), (-1.6, -0.55), (0.1, -0.05), (1.6, 0.6), (1.7, -0.55)]   # A B Hub D E
    vs = [vert(P(1, x, y), BLUE) for x, y in pts]
    es = {e: arrow(vs[e[0]], vs[e[1]]) for e in [(0, 2), (1, 2), (3, 2), (2, 4), (3, 4), (1, 0)]}
    d = VGroup(*es.values(), *vs)
    d.vs, d.es = vs, es
    d.lit = [vs[2]]
    d.chain_edges = [es[(1, 0)], es[(0, 2)], es[(2, 4)]]
    d.chain = [vs[1], vs[0], vs[2], vs[4]]
    return d


def roads():
    pts = [(-1.8, 0), (-0.6, 0.6), (-0.6, -0.6), (0.6, 0.6), (0.6, -0.6), (1.8, 0)]
    r = 0.14
    vs = [vert(P(2, x, y), FG, r) for x, y in pts]
    spec = [((0, 1), "2 km", 1), ((1, 3), "5 km", 1), ((3, 5), "2 km", 1),
            ((0, 2), "3 km", -1), ((2, 4), "2 km", -1), ((4, 5), "3 km", -1)]
    es = {e: line(vs[e[0]], vs[e[1]], r) for e, _, _ in spec}
    lens = [along(s, vs[e[0]].get_center(), vs[e[1]].get_center(), side=sd, color=GOLD) for e, s, sd in spec]
    d = VGroup(*es.values(), *vs)
    d.vs, d.es, d.lens = vs, es, lens
    d.lit = [es[(0, 2)], es[(2, 4)], es[(4, 5)], vs[0], vs[2], vs[4], vs[5]]
    d.chain = [vs[0], vs[2], vs[4], vs[5]]
    return d


def software():
    pts = [(-1.7, -0.05), (-0.55, 0.38), (-0.55, -0.5), (0.55, 0.55), (0.55, -0.02), (0.55, -0.6), (1.6, 0.25), (1.6, -0.5)]
    vs = [vert(P(3, x, y), PURPLE) for x, y in pts]
    names = [T("app", 28, FG).next_to(vs[0], UP, buff=0.1), T("lib", 28, FG).next_to(vs[1], UP, buff=0.1)]
    es = {e: arrow(vs[e[0]], vs[e[1]]) for e in
          [(0, 1), (0, 2), (1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (5, 7)]}
    first = [es[(0, 1)], es[(0, 2)], vs[0], vs[1], vs[2], *names]
    rest = [es[e] for e in [(1, 3), (1, 4), (2, 4), (2, 5), (3, 6), (4, 6), (5, 7)]] + vs[3:]
    d = VGroup(*es.values(), *vs, *names)
    d.vs, d.es, d.first, d.rest = vs, es, first, rest
    d.lit = list(es.values()) + vs[1:]
    d.chains = [[vs[0], vs[1], vs[3], vs[6]], [vs[0], vs[2], vs[5], vs[7]]]
    return d


def infobox(center):
    w, h = 1.1, 0.82
    box = RoundedRectangle(corner_radius=0.06, width=w, height=h).set_stroke(DIM, 2).set_fill(BG, 1)
    head = Line(LEFT * 0.28, RIGHT * 0.28).set_stroke(FG, 4).shift(UP * 0.28)
    img = Rectangle(width=0.5, height=0.16).set_stroke(width=0).set_fill(DIM, 0.6).shift(UP * 0.1)
    rows = VGroup()
    for k in range(3):
        y = -0.1 - 0.13 * k
        rows.add(Line([-0.42, y, 0], [-0.1, y, 0]).set_stroke(DIM, 3),
                 Line([0.0, y, 0], [0.42, y, 0]).set_stroke(FG if k == 0 else DIM, 3))
    return VGroup(box, head, img, rows).move_to(center)


def knowledge():
    kid = vert(P(4, -1.85, 0.0), BLUE)
    cc = vert(P(4, 0.0, 0.0), PINK)
    act = vert(P(4, 1.95, 0.0), FG)
    vs = [kid, cc, act]
    names = [T("The Kid", 28, FG).next_to(kid, DOWN, buff=0.1),
             VGroup(T("Charles", 28, FG), T("Chaplin", 28, FG)).arrange(DOWN, buff=0.08).next_to(cc, DOWN, buff=0.1),
             T("actor", 28, FG).next_to(act, DOWN, buff=0.1)]
    e1, e2 = arrow(kid, cc), arrow(cc, act)
    l1 = T("director", 28, DIM).next_to(e1, UP, buff=0.1)
    l2 = T("occupation", 28, DIM).next_to(e2, UP, buff=0.1)
    d = VGroup(e1, e2, *vs, *names, l1, l2)
    d.vs, d.names, d.edges, d.elabels = vs, names, [e1, e2], [l1, l2]
    d.card = infobox(P(4, 1.45, 0.95)).scale(0.75)
    d.chain = vs
    return d


def ours():
    t = load_scene("ch1_s2_lasttime").tangle()
    for v in t.v.values():
        v.remove(v.label)
    t.scale(OURS_S, about_point=ORIGIN).shift(slot(5))
    return t


def finalize(i, d):
    """The drawing's end-of-tour state (for thumbnails())."""
    if i == 0:
        d.remove(d.follow_line)
        d.add_to_back(d.follow)
        d.add(d.follow_label)
    if i == 2:
        d.add(*d.lens)
    if i == 4:
        d.add(d.card)
    for m in getattr(d, "lit", []):
        m.set_color(YELLOW)
    return d


BUILDERS = [social, web, roads, software, knowledge, ours]


def thumbnails():
    """The 3x2 grid of graphs, as at the end of c1.shapes.3. `.tiles` in order
    social, web, roads, software, knowledge, ours; each tile `.drawing .caption .tag`."""
    tiles = []
    for i, b in enumerate(BUILDERS):
        d = finalize(i, b())
        cap, tg = caption(i), tag(i)
        tile = VGroup(d, cap, *([tg] if tg is not None else []))
        tile.drawing, tile.caption, tile.tag = d, cap, tg
        tiles.append(tile)
    g = VGroup(*tiles)
    g.tiles = tiles
    return g


def card(title, sub, color, center):
    t1 = T(title, 36, color)
    t2 = T(sub, 32, color if color == DIM else FG)
    txt = VGroup(t1, t2).arrange(DOWN, buff=0.22)
    box = RoundedRectangle(corner_radius=0.15, width=6.2, height=1.75).set_stroke(color, 3).set_fill(BG, 0.96)
    g = VGroup(box, txt).move_to(center)
    g.box, g.title, g.sub = box, t1, t2
    return g


def edge_arrow(start, centre, r, color=YELLOW):
    u = (centre - start) / np.linalg.norm(centre - start)
    return Arrow(start, centre - u * (r + 0.1), buff=0, stroke_width=4, color=color,
                 max_tip_length_to_length_ratio=0.2)


class Shapes(NarratedScene):
    def construct(self):
        sh = load_scene("ch1_s2_lasttime").handover_shot()
        self.add(sh)
        self.sh = sh
        self.clip1(sh)
        self.clip2()
        self.clip3(sh)
        self.clip4(sh)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ the picture is a graph
    def clip1(self, sh):
        with self.say("c1.shapes.1") as c:
            word = T("graph", 48, YELLOW).move_to(UP * 3.3)
            c.wait_until(own_word=word)
            self.play(*appear(word), run_time=1.0)

            c.wait_until("vertices")
            vt1, vt2 = T("vertices", 36, YELLOW), T("(nodes)", 36, YELLOW)
            vtag = VGroup(vt1, vt2).arrange(DOWN, buff=0.12).move_to(LEFT * 5.0)
            va = [edge_arrow(vtag.get_right() + 0.15 * RIGHT + 0.25 * UP, sh.v["coogan"].circle.get_center(), R_VERT),
                  edge_arrow(vtag.get_right() + 0.15 * RIGHT + 0.25 * DOWN, sh.v["kid"].circle.get_center(), R_VERT)]
            self.play(*appear(vt1), *[GrowArrow(a) for a in va],
                      *flash([v.circle for v in sh.v.values()], run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until(own_word=vt2)
            self.play(*appear(vt2), run_time=1.0)

            c.wait_until("edges")
            etag = T("edges (links, arcs, relationships)", 36, YELLOW).move_to(DOWN * 3.3)
            ea = Arrow(etag.get_top() + 0.1 * UP, [0, -0.12, 0], buff=0, stroke_width=4, color=YELLOW,
                       max_tip_length_to_length_ratio=0.1)
            self.play(*appear(etag), GrowArrow(ea),
                      *[VShowPassingFlash(l.copy().set_stroke(YELLOW, 8), time_width=0.6, run_time=1.6)
                        for l in sh.lines],
                      run_time=1.6)

            c.wait_until("the shape")
            sh.generate_target()
            for i in range(3, 7):
                sh.target[i][1].set_opacity(0)
            sh.target.scale(OURS_S, about_point=ORIGIN).shift(slot(5))
            self.play(*during(disappear(word, vtag, etag, *va, ea), 0, 0.35),
                      *during([MoveToTarget(sh)], 0.35, 1), run_time=min(2.2, c.until()))
            for v in sh.v.values():
                v.remove(v.label)

    # ------------------------------------------------------------ social, web, roads
    def clip2(self):
        self.d = [b() for b in BUILDERS[:5]]
        self.caps = [caption(i) for i in range(6)]
        self.tags = [tag(i) for i in range(6)]
        soc, wb, rd = self.d[:3]
        with self.say("c1.shapes.2") as c:
            self.play(*appear(soc, self.caps[0], lag=0.3), run_time=min(1.6, c.until("follows")))

            c.wait_until("follows")
            self.play(ReplacementTransform(soc.follow_line, soc.follow), *appear(soc.follow_label),
                      run_time=1.5)

            c.wait_until("friends")
            self.play(*recolor(soc.lit, YELLOW), *appear(self.tags[0]), run_time=1.5)

            c.wait_until("web")
            self.play(*appear(wb, self.caps[1], lag=0.3), run_time=1.6)
            c.wait_until("search engines")
            self.play(*recolor(wb.lit, YELLOW), *flash(wb.lit, run_time=1.5), *appear(self.tags[1]),
                      run_time=1.5)

            c.wait_until("roads")
            self.play(*appear(rd, self.caps[2], lag=0.3), run_time=1.6)
            c.wait_until("labelled")
            self.play(*appear(*rd.lens, lag=0.15), run_time=1.5)

            c.wait_until("route")
            self.play(*recolor(rd.lit, YELLOW), *appear(self.tags[2]), run_time=1.5)

    # ------------------------------------------------------------ software, knowledge, ours
    def clip3(self, sh):
        sw, kn = self.d[3], self.d[4]
        with self.say("c1.shapes.3") as c:
            self.play(*appear(VGroup(*sw.first), self.caps[3], lag=0.3), run_time=1.5)
            c.wait_until("which depend")
            self.play(*appear(VGroup(*sw.rest)), run_time=1.5)

            c.wait_until("deps")
            self.play(*recolor(sw.lit, YELLOW), *appear(self.tags[3]), run_time=1.6)

            c.wait_until("knowledge")
            self.play(*appear(kn, self.caps[4], lag=0.3), run_time=1.6)
            c.wait_until("the box")
            self.play(FadeIn(kn.card, shift=0.15 * UP), run_time=1.2)

            c.wait_until("ours")
            self.play(*appear(self.caps[5]), FlashAround(sh, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("People")
            self.play(*flash([v.circle for v in sh.v.values()], run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("who worked")
            self.play(*[VShowPassingFlash(l.copy().set_stroke(YELLOW, 7), time_width=0.6) for l in sh.lines],
                      run_time=1.2)

    # ------------------------------------------------------------ the questions are chains
    def clip4(self, sh):
        soc, wb, rd, sw, kn = self.d
        qtags = [t for t in self.tags if t is not None]

        def run(mobs):
            return VShowPassingFlash(path_through(mobs), time_width=0.6)

        with self.say("c1.shapes.4") as c:
            self.play(*flash(qtags, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("Friends of friends")
            self.play(run(soc.chain), FlashAround(self.tags[0], run_time=1.2), run_time=1.2)
            c.wait_until("A route")
            self.play(run(rd.chain), FlashAround(self.tags[2], run_time=1.2), run_time=1.2)
            c.wait_until("Every dependency")
            self.play(*[run(ch) for ch in sw.chains], FlashAround(self.tags[3], run_time=1.2), run_time=1.2)

            more = wb.chain_edges + kn.edges + list(sh.lines)
            self.play(*recolor(more, YELLOW),
                      LaggedStart(run(wb.chain), run(kn.chain),
                                  run([sh.v[k].circle for k in ("coogan", "kid", "chaplin", "gold")]),
                                  lag_ratio=0.3),
                      run_time=min(1.5, c.until("unknown")))

            c.wait_until("unknown")
            q1 = T("questions follow chains of edges", 32, FG).move_to(DOWN * 3.3)
            self.play(*appear(q1), run_time=1.0)
            c.wait_until("often")
            q2 = T("questions follow chains of edges … often of unknown length", 32, FG,
                   t2c={"unknown length": GOLD}).move_to(DOWN * 3.3)
            qm = T("?", 48, GOLD).move_to(slot(5) + TAG_DY * UP)
            self.play(*edit(q1, q2), *appear(qm), run_time=1.5)

            c.wait_until("algos")
            c1 = card("graph algorithms", "the Algorithms course", DIM, LEFT * 3.35 + UP * 0.4)
            c2 = card("this course", "storing and querying graphs", YELLOW, RIGHT * 3.35 + UP * 0.4)
            texts = [m for top in self.mobjects for m in top.get_family()
                     if isinstance(m, Text) and m is not q2]
            others = [m for m in self.mobjects if m is not q2 and not isinstance(m, Text)]
            self.play(*set_alpha(others + [q2], DIMMED), run_time=1.2)
            self.play(*during([m.animate.set_opacity(0) for m in texts], 0, 0.45),
                      *during(appear(c1), 0.4, 1), run_time=1.5)

            c.wait_until("ours2")
            self.play(*appear(c2), run_time=1.0)
