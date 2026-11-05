"""Chapter 5, scene 8: recap of the chapter in five panels, then the whole lecture in one picture. Clips c5.recap.1 – c5.recap.3.

Shared drawing (ch6 s1 opens on it, forward join):
  end_card() -> VGroup, the static last frame: .strip (five shrunken panels along the top), .copies (three
  tangle copies, left column), .tables .docs .graph (the three model rows), .teaser (DIM "Next: ...").
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

S2 = load_scene("ch5_s2_bfs")
S3 = load_scene("ch5_s3_unwrap")
S4 = load_scene("ch5_s4_bacon")
S5 = load_scene("ch5_s5_languages")
S6 = load_scene("ch5_s6_pgq")
L2 = load_scene("ch1_s2_lasttime")
PG = load_scene("ch1_s4_propgraph")
H2 = load_scene("ch2_s1_hook")

# ---------------------------------------------------------------- layout
PW = 2.5                    # panel frame width
PH = 3.0                    # panel frame height
PITCH = 2.65
PY = 0.5
PX = [(i - 2) * PITCH for i in range(5)]
STRIP_S = 0.42
STRIP_Y = 3.1
ROW_Y = [1.0, -0.8, -2.6]   # tables, documents, graph
CX = -5.8                   # the tangle copies (their row label sits under them)
MX = 0.75                   # centre of the model pictures
TANGLE_S = 0.88
COPY_S = 0.26
TEASER_Y = 2.05

CAPTIONS = ["ripples: each\nperson once", "one, or all\nof the shortest", "nodes + unwind\n→ rows",
            "length / 2,\ndistinct people", "GQL and\nSQL/PGQ"]


def pc(i):
    return np.array([PX[i], PY, 0])


def frame(i):
    return RoundedRectangle(corner_radius=0.15, width=PW, height=PH).set_stroke(DIM, 2).move_to(pc(i))


def caption(i):
    """Centred lines (a multi-line Text is left-aligned and would crowd its neighbour)."""
    t = VGroup(*[T(line, size=28) for line in CAPTIONS[i].split("\n")]).arrange(DOWN, buff=0.12)
    return t.next_to(frame(i), DOWN, buff=0.22)


# ---------------------------------------------------------------- panel contents (each in its final state)
def fit(m, w, h):
    """Scale m to fit inside w x h (its bounding box, whatever drawing it is)."""
    return m.scale(min(w / m.width, h / m.height))


def p_rings(final=True):
    rings = S2.ripple_rings(centre=pc(0), scale=0.5)
    route = S2.ripple_route(rings)
    if final:
        rings.target.set_color(YELLOW).scale(2.2)
    return rings, route


def p_paths():
    path = S2.lr_path(names=(None,) * 5, edge_color=YELLOW)
    path.scale_to_fit_width(2.1).move_to(pc(1) + 1.0 * UP)
    fan = S2.eight_fan()
    fan.remove(*fan.labels.values())     # names and film titles: at panel size a clean shape picture
    fit(fan, 2.2, 1.95).move_to(pc(1) + 0.3 * DOWN)
    return path, fan


LIST_COLS = [PINK, BLUE, PINK, BLUE, PINK]      # s3's five vertices of nodes(path)


def p_list(rows=True):
    """s3's list picture: five vertex circles in TEAL [ ], unrolled into rows numbered GOLD 0-4.
    rows=False: the list (circles in a row, brackets); rows=True: the column of rows with digits."""
    c = pc(2)
    g = VGroup()
    g.circles = [S2.vertex(col, r=0.15) for col in LIST_COLS]
    g.digits = [Mono(str(i), size=30, color=GOLD).move_to(c + (-0.45, 1.0 - 0.5 * i, 0)) for i in range(5)]
    g.lb = Mono("[", size=44, color=TEAL).move_to(c + (-1.0, 0.1, 0))
    g.rb = Mono("]", size=44, color=TEAL).move_to(c + (1.0, 0.1, 0))
    for i, circ in enumerate(g.circles):
        circ.move_to(c + ((0.3, 1.0 - 0.5 * i, 0) if rows else ((i - 2) * 0.4, 0.1, 0)))
    if rows:
        g.add(*g.circles, *g.digits)
    else:
        g.add(g.lb, g.rb, *g.circles)
    return g


def p_hist():
    h = S4.bacon_histogram(max_h=8.0, with_xlabel=False)
    h.remove(*h.values, *h.ticks)
    fit(h, 2.2, 2.4).move_to(pc(3))
    return h


def p_langs():
    pe = S5.plus_edge()
    pe.scale_to_fit_width(2.3).move_to(pc(4) + 0.75 * UP)
    pg = S6.pattern_picture()
    pg.scale_to_fit_width(2.0).move_to(pc(4) + 0.55 * DOWN)
    return pe, pg


def panel_contents(i):
    if i == 0:
        return list(p_rings())
    if i == 1:
        return list(p_paths())
    if i == 2:
        return [p_list()]
    if i == 3:
        return [p_hist()]
    return list(p_langs())


def to_strip(panel, i):
    return panel.scale(STRIP_S).move_to((PX[i] * STRIP_S, STRIP_Y, 0))


# ---------------------------------------------------------------- the lecture picture
def bare(t):
    """The tangle's lines and circles (no names), as one group."""
    return VGroup(*t.lines, *[t.v[k].circle for k in ("coogan", "chaplin", "kid", "gold")])


def copy_at(k, final=True):
    g = bare(L2.tangle()).scale(COPY_S).move_to((CX, ROW_Y[k] + 0.2, 0))
    if final and k == 0:
        g[1].set_color(YELLOW)          # Chaplin - The Kid: the edge being followed
    return g


ROW_NAMES = ["tables", "documents", "graph"]


def row_label(k):
    return T(ROW_NAMES[k], size=30, color=DIM).move_to((CX, ROW_Y[k] - 0.6, 0))


def tables_row():
    jd = H2.join_diagram()
    return jd.scale(0.95).move_to((MX, ROW_Y[0], 0))


def docs_row(final=True):
    dk = L2.mini_doc("The Kid").move_to((MX - 1.9, ROW_Y[1], 0))
    dc = L2.mini_doc("Chaplin").move_to((MX + 1.9, ROW_Y[1], 0))
    if final:
        for d in (dk, dc):
            d.copy_bar.set_color(YELLOW)
    g = VGroup(dk, dc)
    g.dk, g.dc = dk, dc
    return g


def graph_row(final=True):
    y = ROW_Y[2]
    ch = PG.vertex("Charles Chaplin", "Person", at=(-2.9, y, 0), r=0.35)
    kid = PG.vertex("The Kid", "Movie", at=(0.3, y, 0), r=0.35)
    edge = PG.typed_edge(ch, kid, "ACTED_IN")
    rings = VGroup(*[Circle(radius=0.47).set_stroke(YELLOW, 4).move_to(v.circle) for v in (ch, kid)])
    xs = [0.3 + 1.05 * k for k in range(1, 7)]
    ops = [1, 0.85, 0.7, 0.5, 0.35, 0.2]
    dots, links = [], []
    prev = kid.circle
    for k, (x, op) in enumerate(zip(xs, ops)):
        col = PINK if k % 2 == 0 else BLUE
        d = S2.vertex(col, r=0.14).move_to((x, y, 0)).set_opacity(op)
        a, b = prev.get_center(), d.get_center()
        links.append(Line(a, b, buff=prev.width / 2).set_stroke(FG, 3, opacity=op))
        dots.append(d)
        prev = d
    chain = VGroup(*links, *dots)
    anylen = T("any length", size=30, color=YELLOW).move_to((3.95, y - 0.55, 0))
    if final:
        edge.set_color(YELLOW)
    g = VGroup(edge, ch, kid, rings, chain, anylen)
    g.ch, g.kid, g.edge, g.rings, g.chain, g.anylen = ch, kid, edge, rings, chain, anylen
    g.links, g.dots = links, dots
    return g


def teaser():
    return T("Next: recursive queries and Datalog", size=36, color=DIM).move_to((0, TEASER_Y, 0))


def end_card():
    """The finished recap: strip, three copies, three model rows, the teaser. Static, no updaters."""
    strip = VGroup(*[to_strip(VGroup(frame(i), *panel_contents(i)), i) for i in range(5)])
    copies = VGroup(*[copy_at(k) for k in range(3)])
    labels = VGroup(*[row_label(k) for k in range(3)])
    g = VGroup(strip, copies, labels, tables_row(), docs_row(), graph_row(), teaser())
    g.strip, g.copies, g.labels, g.tables, g.docs, g.graph, g.teaser = g
    return g


class Recap(NarratedScene):
    def construct(self):
        frames = [frame(i) for i in range(5)]
        panels = [VGroup(f) for f in frames]
        caps = [caption(i) for i in range(5)]

        # ------------------------------------------------ clip 1: five panels
        with self.say("c5.recap.1") as c:
            self.play(*appear(*frames, shift=None, lag=0.15), run_time=min(1.3, c.until("r1")))
            c.wait_until("r1")

            rings, route = p_rings(final=False)
            self.play(LaggedStart(FadeIn(rings.centre_dot, scale=0.5), FadeIn(rings.films), FadeIn(rings.ring1),
                                  FadeIn(rings.ring2), lag_ratio=0.4), run_time=1.6)
            self.play(Create(route.line), FadeIn(route.via),
                      rings.target.animate.set_color(YELLOW).scale(2.2), run_time=1.2)
            self.play(*appear(caps[0]), run_time=1.0)
            settle(self, panels[0], add=[rings, route])
            c.wait_until("r2")

            path, fan = p_paths()
            self.play(*appear(path, shift=None), run_time=1.0)
            self.play(*appear(fan, shift=None), run_time=1.2)
            self.play(*appear(caps[1]), run_time=1.0)
            settle(self, panels[1], add=[path, fan])
            lst = p_list(rows=False)
            col = p_list(rows=True)
            self.play(*appear(lst.lb, lst.rb, *lst.circles, shift=None, lag=0.08), run_time=0.8)
            c.wait_until("r3")

            self.play(*during(disappear(lst.lb, lst.rb), 0, 0.35),
                      *during([circ.animate.move_to(tgt) for circ, tgt in zip(lst.circles, col.circles)], 0.2, 0.8),
                      *during(appear(*col.digits, shift=None, lag=0.1), 0.5, 1),
                      run_time=1.6)
            self.play(*appear(caps[2]), run_time=min(1.0, c.until("r4", floor=0.6)))
            self.remove(*lst.circles, *col.digits)
            settle(self, panels[2], add=[col])
            c.wait_until("r4")

            hist = p_hist()
            self.play(Create(hist.axis), run_time=0.5)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in hist.bars], lag_ratio=0.15), run_time=1.5)
            c.wait_until("half the length")
            self.play(*appear(caps[3]), run_time=1.0)
            settle(self, panels[3], add=[hist])
            c.wait_until("r5")

            pe, pg = p_langs()
            self.play(*appear(pe, shift=None), run_time=1.0)
            c.wait_until("sequel P G Q")
            self.play(*appear(pg, shift=None), *during(appear(caps[4]), 0.4, 1), run_time=1.4)
            settle(self, panels[4], add=[pe, pg])

        # ------------------------------------------------ clip 2: the whole lecture
        with self.say("c5.recap.2") as c:
            t = L2.tangle().scale(TANGLE_S).move_to((0, -0.75, 0))
            self.play(*during(disappear(*caps), 0, 0.35),
                      *during([panels[i].animate.scale(STRIP_S).move_to((PX[i] * STRIP_S, STRIP_Y, 0))
                               for i in range(5)], 0.1, 0.65),
                      *during(appear(t, shift=None), 0.45, 1),
                      run_time=1.6)
            self.wait(1.1)      # the one picture, names readable, before it splits

            b = bare(t)
            labels = [t.v[k].label for k in ("coogan", "chaplin", "kid", "gold")]
            self.remove(t)
            self.add(b, *labels)
            tg = [copy_at(k, final=False) for k in range(3)]
            self.play(*during(disappear(*labels), 0, 0.4),
                      *during([Transform(b, tg[0]), ReplacementTransform(b.copy(), tg[1]),
                               ReplacementTransform(b.copy(), tg[2])], 0.3, 1),
                      run_time=min(1.5, c.until("tables", floor=1.0)))
            copies = [b, tg[1], tg[2]]
            c.wait_until("tables")

            jd = tables_row()
            self.play(*appear(*jd.boxes, shift=None, lag=0.3), *appear(*jd.names, shift=None, lag=0.3),
                      *appear(row_label(0)), run_time=1.2)
            self.play(*[GrowArrow(l) for l in jd.links], *appear(*jd.keys), run_time=1.0)
            c.wait_until("is a join")
            self.play(b[1].animate.set_color(YELLOW),
                      *[VShowPassingFlash(Line(l.get_start(), l.get_end()).set_stroke(YELLOW, 6), time_width=0.6)
                        for l in jd.links], run_time=1.0)
            c.wait_until("trees")

            docs = docs_row(final=False)
            self.play(*appear(docs.dk, docs.dc, shift=None, lag=0.4), *appear(row_label(1)), run_time=1.2)
            c.wait_until("stored twice")
            self.play(*recolor(list(docs.dk.copy_bar) + list(docs.dc.copy_bar), YELLOW), run_time=0.8)
            self.play(*flash([docs.dk.copy_bar, docs.dc.copy_bar]), run_time=1.2)
            c.wait_until("graph")

            g = graph_row(final=False)
            self.play(*appear(g.ch, g.kid, shift=None, lag=0.3), *appear(row_label(2)), run_time=1.0)
            self.play(Create(g.edge.arrow), *appear(g.edge.label), run_time=0.9)
            c.wait_until("pattern")
            self.play(*[GrowFromCenter(r) for r in g.rings], *recolor([g.edge.arrow, g.edge.label], YELLOW),
                      run_time=1.0)
            c.wait_until("any length")
            self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(d)) for l, d in zip(g.links, g.dots)],
                                  lag_ratio=0.35),
                      *during(appear(g.anylen), 0.45, 1), run_time=min(1.8, c.until(floor=0.8)))

        # ------------------------------------------------ clip 3: next time
        with self.say("c5.recap.3") as c:
            tz = teaser()
            self.play(*appear(tz), run_time=1.2)
            c.wait_until("bye")

        # the end card: the same picture, rebuilt as one static object (ch6 s1 opens on it)
        self.clear()
        self.add(end_card())
        self.wait(8)
