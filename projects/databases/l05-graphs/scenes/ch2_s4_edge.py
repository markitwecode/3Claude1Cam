"""Chapter 2, scene 4: following an edge (55 rows from 35 movies). Clips c2.edge.1 – c2.edge.6."""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── the queries (wrapped as on Slide 103) ─────────────────────────────────────────
M0 = "MATCH (p:Person {name: 'Steven Spielberg'})"
Q1 = M0 + "\n      --> (m:Movie)\nRETURN m.title"
Q2 = M0 + "\n      --> (m:Movie)\nRETURN m.title, m.year\nORDER BY m.year\nLIMIT 6"
Q3 = M0 + "\n      -[:DIRECTED]-> (m:Movie)\nRETURN m.title"
Q4 = M0 + "\n      -[:DIRECTED]-> (m:Movie)\nRETURN m.title, m.year\nORDER BY m.year\nLIMIT 4;"

CE = "Close Encounters of the Third Kind"
ET = "E.T. the Extra-Terrestrial"
RAIDERS = "Raiders of the Lost Ark"
LIMIT6 = [("Jaws", 1975), (CE, 1977), (CE, 1977), (RAIDERS, 1981), (ET, 1982), (ET, 1982)]
LIMIT4 = [("Jaws", 1975), (CE, 1977), (RAIDERS, 1981), (ET, 1982)]
TABLE_TOP = -0.15
ROW_PITCH = 0.56


def query(src):
    c = Code(src, size=34)
    c.move_to(ORIGIN).to_edge(UP, buff=0.5)
    return c


def result_row(title, year, pad=34, size=30):
    return Mono(f"{title:<{pad}} │ {year}", size, t2c={"│": DIM, str(year): GOLD})


def table(entries):
    rows = VGroup(*[result_row(t, y) for t, y in entries])
    w = rows[0].width
    rows[0].move_to([0, TABLE_TOP, 0])
    bar_x = select(rows[0], "│")[0].get_x()
    for i, r in enumerate(rows):   # line the │ column up (ink widths differ row to row)
        r.set_y(TABLE_TOP - i * ROW_PITCH)
        r.shift((bar_x - select(r, "│")[0].get_x()) * RIGHT)
    return rows


def handover_shot():
    """Slide 103 and its four-row result: s5 opens from it."""
    return VGroup(query(Q4), table(LIMIT4))


# ── the fan of Spielberg's edges ──────────────────────────────────────────────────
SP = np.array([0.0, 0.85, 0.0])
R_S, R_M = 0.95, 0.3
ARCS = {1: [0.0], 2: [-0.35, 0.35], 3: [-0.45, 0.0, 0.45]}
EDGE = FG
MOVIES = [   # key, centre, label, label side, edge types (in arc order)
    ("CE", (-4.3, 2.35), "Close Encounters", UP, ["WROTE", "DIRECTED"]),
    ("Raiders", (-1.6, 2.75), "Raiders", UP, ["DIRECTED"]),
    ("JP", (1.6, 2.75), "Jurassic Park", UP, ["DIRECTED"]),
    ("Goonies", (4.3, 2.35), "The Goonies", UP, ["WROTE"]),
    ("Jaws", (-5.15, 0.75), "Jaws", LEFT, ["DIRECTED"]),
    ("Hook", (5.15, 0.75), "Hook", RIGHT, ["DIRECTED"]),
    ("Super8", (-4.5, -0.85), "Super 8", DOWN, ["PRODUCED"]),
    ("MR", (4.5, -0.85), "Minority Report", DOWN, ["DIRECTED"]),
    ("AI", (-2.3, -1.15), "A.I.", DOWN, ["WROTE", "PRODUCED", "DIRECTED"]),
    ("Spiel", (0.0, -1.35), "Spielberg (2017)", DOWN, ["ACTED_IN"]),
    ("ET", (2.3, -1.15), "E.T.", DOWN, ["PRODUCED", "DIRECTED"]),
]


def _edge_geom(m_pos, a, r_s=R_S, r_m=R_M, s_pos=SP):
    u = normalize(m_pos - s_pos)
    start = s_pos + r_s * rotate_vector(u, -a / 2)
    end = m_pos - r_m * rotate_vector(u, a / 2)
    return start, end


def edge_arrow(start, end, a, color=EDGE, width=3):
    return Arrow(start, end, buff=0, path_arc=a, stroke_width=width, color=color,
                 tip_length=0.2, max_tip_length_to_length_ratio=0.3)


def person_node(pos=SP):
    circ = Circle(radius=R_S, color=PINK, stroke_width=4).set_fill(BG, 1).move_to(pos)
    name = T("Steven\nSpielberg", 28).move_to(pos)
    return VGroup(circ, name)


def movie_node(pos, label, side=DOWN):
    circ = Circle(radius=R_M, color=BLUE, stroke_width=4).set_fill(BLUE, 0.2).move_to(pos)
    lab = T(label, 28).next_to(circ, side, buff=0.14)
    return VGroup(circ, lab)


class Fan(VGroup):
    def __init__(self):
        super().__init__()
        self.person = person_node()
        self.movies, self.arrows, self.paths, self.geom = {}, {}, {}, {}
        arrows, nodes = [], []
        for key, pos, label, side, types in MOVIES:
            p = np.array([pos[0], pos[1], 0.0])
            self.movies[key] = movie_node(p, label, side)
            nodes.append(self.movies[key])
            for typ, a in zip(types, ARCS[len(types)]):
                s, e = _edge_geom(p, a)
                self.geom[(key, typ)] = (s, e, a, p)
                self.arrows[(key, typ)] = edge_arrow(s, e, a)
                self.paths[(key, typ)] = Line(s, e, path_arc=a)
                arrows.append(self.arrows[(key, typ)])
        self.arrow_list = arrows
        self.node_list = nodes
        self.add(*arrows, *nodes, self.person)

    def path_flash(self, key, color=YELLOW, width=6, time_width=0.6):
        s, e = self.arrows[key].get_start(), self.arrows[key].get_end()   # wherever the fan now is
        p = Line(s, e, path_arc=self.geom[key][2]).set_stroke(color, width)
        return VShowPassingFlash(p, time_width=time_width)


def stencil_rest():
    c1 = Circle(radius=0.55, color=YELLOW, stroke_width=4).move_to([-1.4, -2.85, 0])
    c2 = Circle(radius=0.45, color=YELLOW, stroke_width=4).move_to([1.4, -2.85, 0])
    arr = Arrow(c1.get_right(), c2.get_left(), buff=0.1, stroke_width=5, color=YELLOW,
                tip_length=0.24, max_tip_length_to_length_ratio=0.3)
    return VGroup(c1, c2, arr)


def stencil_on(fan, key):
    s, e, a, p = fan.geom[key]
    c1 = Circle(radius=R_S + 0.15, color=YELLOW, stroke_width=4).move_to(SP)
    c2 = Circle(radius=R_M + 0.15, color=YELLOW, stroke_width=4).move_to(p)
    return VGroup(c1, c2, edge_arrow(s, e, a, color=YELLOW, width=5))


def tagged_rows(title, year, tags, ys, left):
    rows, tgs = [], []
    for tag, y in zip(tags, ys):
        r = result_row(title, year, pad=0)
        r.move_to([left + r.width / 2, y, 0])
        t = T(tag, 28, color=YELLOW).next_to(r, RIGHT, buff=0.45)
        rows.append(r)
        tgs.append(t)
    return rows, tgs


def et_pair():
    """For the recap: Spielberg -> E.T. along PRODUCED and DIRECTED, and the two identical rows."""
    s_pos, m_pos = np.array([-2.6, 0.9, 0]), np.array([2.6, 0.9, 0])
    person = person_node(s_pos)
    movie = VGroup(Circle(radius=0.45, color=BLUE, stroke_width=4).set_fill(BLUE, 0.2).move_to(m_pos))
    movie.add(T("E.T.", 32).next_to(movie[0], DOWN, buff=0.16))
    g = VGroup()
    for typ, a, side in (("PRODUCED", 0.5, DOWN), ("DIRECTED", -0.5, UP)):
        s, e = _edge_geom(m_pos, a, r_m=0.45, s_pos=s_pos)
        arr = edge_arrow(s, e, a, color=YELLOW, width=4)
        lab = T(typ, 28, color=YELLOW).next_to(arr, side, buff=0.1)
        g.add(arr, lab)
    rows = VGroup(*[result_row(ET, 1982, pad=0) for _ in range(2)])
    rows.arrange(DOWN, buff=0.22).move_to([0, -1.55, 0])
    return VGroup(g, person, movie, rows)


class FollowingAnEdge(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.clip6()
        self.wait(1.0)   # handover: hold Slide 103 and its result; s5 opens from it

    # c2.edge.1: build the query
    def clip1(self):
        self.q1 = q1 = query(Q1)
        line0 = q1.line(0).copy()
        dashes = q1.find("-->").copy()
        movie = q1.find("(m:Movie)").copy()
        ret = q1.line(2).copy()
        with self.say("c2.edge.1") as c:
            c.wait_until("person")
            self.play(*appear(line0), run_time=1.0)
            c.wait_until("curly braces")
            self.play(FlashAround(q1.find("{name: 'Steven Spielberg'}"), run_time=1.5, time_width=1.5))
            c.wait_until("arrow")
            self.play(*appear(dashes), run_time=1.0)
            c.wait_until("second circle")
            self.play(*appear(movie), run_time=1.0)
            c.wait_until("return")
            self.play(*appear(ret), run_time=1.0)
            self.remove(line0, dashes, movie, ret)
            self.add(q1)
            self.ask = T("how many rows?", 48, t2c={"?": GOLD}).move_to([0, -0.7, 0])
            c.wait_until("so how many")
            self.play(*appear(self.ask), run_time=1.0)

    # c2.edge.2: 55 rows, 35 movies; sorted, the repeats show
    def clip2(self):
        rows55 = T("55 rows", 48, color=GOLD).move_to([-4.0, -0.7, 0])
        movies35 = T("35 movies", 48, color=GOLD).move_to([0, -0.7, 0])
        extra = T("+20 ?", 48, color=GOLD).move_to([4.0, -0.7, 0])
        q2 = query(Q2)
        self.rows6 = rows = table(LIMIT6)
        with self.say("c2.edge.2") as c:
            self.play(*swap(self.ask, rows55), run_time=1.2)
            c.wait_until("thirty-five different")
            self.play(*appear(movies35), run_time=1.0)
            c.wait_until("extra twenty")
            self.play(*appear(extra), run_time=1.0)
            c.wait_until("look")
            self.play(*edit(self.q1, q2), run_time=1.5)
            self.play(*during(disappear(rows55, movies35, extra), 0, 0.3),
                      *during(appear(*rows, lag=0.15), 0.3, 1.0), run_time=1.6)
            c.wait_until("twice")
            self.play(*flash([rows[1], rows[2]], run_time=1.5, time_width=1.5),
                      *recolor([rows[1], rows[2]], YELLOW), run_time=1.5)
            c.wait_until("so does")
            self.play(*flash([rows[4], rows[5]], run_time=1.5, time_width=1.5),
                      *recolor([rows[4], rows[5]], YELLOW), run_time=1.5)

    # c2.edge.3: placements of a stencil with an arrow
    def clip3(self):
        self.fan = fan = Fan()
        st = stencil_rest()
        with self.say("c2.edge.3") as c:
            sweep_clear(self,
                        *during([FadeIn(fan.person)], 0.45, 0.7),
                        *during([FadeIn(n) for n in fan.node_list], 0.55, 0.85),
                        *during([GrowArrow(a) for a in fan.arrow_list], 0.7, 1.0),
                        run_time=2.0)
            c.wait_until("edge")
            self.play(FadeIn(st), run_time=1.0)
            c.wait_until("any")
            self.play(*[fan.path_flash(k, width=5, time_width=0.8) for k in fan.arrows],
                      run_time=2.0)
            c.wait_until("et")
            self.play(Transform(st, stencil_on(fan, ("ET", "DIRECTED"))), run_time=1.5)
            rows, tags = tagged_rows(ET, 1982, ["DIRECTED", "PRODUCED"], [-2.75, -3.25], -4.85)
            c.wait_until("directed it")
            self.play(*recolor([fan.arrows[("ET", "DIRECTED")]], YELLOW),
                      *appear(rows[0], shift=None), run_time=1.0)
            c.wait_until("produced it")
            self.play(*during([Transform(st, stencil_on(fan, ("ET", "PRODUCED")))], 0, 0.55),
                      *during(recolor([fan.arrows[("ET", "PRODUCED")]], YELLOW), 0.35, 0.7),
                      *during(appear(rows[1], shift=None), 0.5, 1.0), run_time=1.4)
            c.wait_until("two")
            self.play(*appear(*tags, lag=0.3),
                      fan.path_flash(("ET", "DIRECTED"), time_width=1.0),
                      fan.path_flash(("ET", "PRODUCED"), time_width=1.0), run_time=1.4)
        self.stencil, self.et_rows = st, rows + tags

    # c2.edge.4: A.I. three times; 55 = every edge out of him
    def clip4(self):
        fan = self.fan
        rows, tags = tagged_rows("A.I. Artificial Intelligence", 2001,
                                 ["DIRECTED", "PRODUCED", "WROTE"], [-2.48, -2.9, -3.32], -5.0)
        tally = T("DIRECTED 28 + PRODUCED 22 + WROTE 4 + ACTED_IN 1 = 55", 30,
                  t2c={"28": GOLD, "22": GOLD, " 4": GOLD, " 1": GOLD, "55": GOLD}).move_to([0, -2.95, 0])
        with self.say("c2.edge.4") as c:
            self.play(*disappear(self.stencil),
                      *recolor([fan.arrows[("ET", "DIRECTED")], fan.arrows[("ET", "PRODUCED")]], EDGE),
                      run_time=0.9)
            for typ, cue, i in (("DIRECTED", "directed", 0), ("PRODUCED", "produced", 1), ("WROTE", "wrote", 2)):
                c.wait_until(cue)
                extra = during(disappear(*self.et_rows), 0, 0.4) if i == 0 else []
                self.play(*extra, *recolor([fan.arrows[("AI", typ)]], YELLOW),
                          *during(appear(rows[i], tags[i], lag=0.2, shift=None), 0.4 if i == 0 else 0, 1.0),
                          run_time=1.2 if i == 0 else 1.0)
            c.wait_until("sum")
            self.play(*recolor([fan.arrows[("AI", t)] for t in ("DIRECTED", "PRODUCED", "WROTE")], EDGE),
                      *[fan.path_flash(k, width=5, time_width=0.8) for k in fan.arrows], run_time=1.8)
            c.wait_until("you get")
            self.play(*during(disappear(*rows, *tags), 0, 0.4),
                      *during(appear(tally), 0.5, 1.0), run_time=min(1.4, c.until("spiel")))
            c.wait_until("spiel")
            spiel = fan.movies["Spiel"]
            self.play(*recolor([fan.arrows[("Spiel", "ACTED_IN")]], YELLOW),
                      fan.path_flash(("Spiel", "ACTED_IN"), width=8, time_width=1.0),
                      FlashAround(spiel, run_time=2.0, time_width=1.5),
                      FlashUnder(select(tally, "ACTED_IN 1")[0], run_time=2.0, time_width=1.5),
                      run_time=2.0)
            c.wait_until("of course")
            self.play(FlashAround(spiel[1], run_time=1.5, time_width=1.5),
                      fan.path_flash(("Spiel", "ACTED_IN"), width=8, time_width=1.0), run_time=1.5)
        self.tally = tally

    # c2.edge.5: -[:DIRECTED]-> ; an edge type, not a directed graph
    def clip5(self):
        fan = self.fan
        q1 = query(Q1)
        q3 = query(Q3)
        fan.generate_target()
        fan.target.shift(1.35 * DOWN)
        for n in fan.target.node_list:
            n[1].set_opacity(0)
        idx = fan.arrow_list.index(fan.arrows[("Spiel", "ACTED_IN")])
        fan.target[idx].set_color(EDGE)
        directed = [a for (k, t), a in fan.arrows.items() if t == "DIRECTED"]
        others = [a for (k, t), a in fan.arrows.items() if t != "DIRECTED"]
        lonely = [fan.movies[k][0] for k in ("Goonies", "Super8", "Spiel")]
        rows28 = T("28 rows", 44, color=GOLD).move_to([4.4, 2.33, 0])
        with self.say("c2.edge.5") as c:
            self.play(*during(disappear(self.tally), 0, 0.35),
                      *during([MoveToTarget(fan)], 0.35, 0.8),
                      *during(appear(q1), 0.6, 1.0), run_time=2.0)
            c.wait_until("inside the arrow")
            self.play(*edit(q1, q3), run_time=1.8)
            c.wait_until("directed")
            self.play(*recolor(directed, YELLOW), *set_alpha(others + lonely, DIMMED), run_time=1.5)
            c.wait_until("we get")
            self.play(*appear(rows28), run_time=1.0)
            c.wait_until("careful")
            word = q3.find("DIRECTED")
            box = token_box(word, q3.line(1))
            self.play(*disappear(fan), FadeIn(box), run_time=1.0)
            big = Mono("DIRECTED", 56, color=YELLOW).move_to([-3.3, -0.2, 0])
            self.play(*appear(big), run_time=1.0)
            tag = T("edge type", 40, color=YELLOW).next_to(big, DOWN, buff=0.35)
            graph = T("directed graph", 44, color=DIM).move_to([3.3, -0.2, 0])
            strike = Line(graph.get_left() + 0.15 * LEFT, graph.get_right() + 0.15 * RIGHT,
                          color=RED, stroke_width=6)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("directed graph")
            self.play(*appear(graph), run_time=1.0)
            self.play(GrowFromEdge(strike, LEFT), run_time=0.8)
        self.q3, self.careful = q3, [box, big, tag, graph, strike, rows28]

    # c2.edge.6: Slide 103
    def clip6(self):
        q4, rows = handover_shot()
        with self.say("c2.edge.6", gap=0) as c:
            self.play(*disappear(*self.careful), run_time=0.8)
            self.play(*edit(self.q3, q4), run_time=min(1.6, c.until("list")))
            for i, cue in enumerate(("jaws", "close encounters", "raiders", "e t")):
                c.wait_until(cue)
                self.play(*appear(rows[i]), run_time=0.9)
