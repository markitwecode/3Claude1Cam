"""Chapter 2, scene 5: naming the edge, its properties, and its direction. Clips c2.props.1 – c2.props.5.

Opens on ch2_s4_edge's handover_shot() (Slide 103 and its four rows).
Exports arrow_forms(): the three-row table of arrow forms (drawing + count each), for the recap.
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

G1 = load_scene("ch1_s4_propgraph")
S4 = load_scene("ch2_s4_edge")


# ── the arrow-forms table (exported) ───────────────────────────────────────────────
def _dot(col, letter, at):
    c = Circle(radius=0.3).set_stroke(col, 4).set_fill(col, 0.2).move_to(at)
    t = Mono(letter, 28).move_to(c)
    return VGroup(c, t)


def form_drawing(kind):
    """p (PINK) and m (BLUE), 2.0 apart, with the arrow form between them."""
    p, m = _dot(PINK, "p", LEFT * 1.0), _dot(BLUE, "m", RIGHT * 1.0)
    a, b = LEFT * 0.62, RIGHT * 0.62
    kw = dict(buff=0, stroke_width=3, color=FG, tip_length=0.16, max_tip_length_to_length_ratio=0.4)
    if kind == "fwd":
        lines = VGroup(Arrow(a, b, **kw))
    elif kind == "back":
        lines = VGroup(Arrow(b, a, **kw))
    elif kind == "both":
        lines = VGroup(Line(a, b).set_stroke(FG, 3))
    else:   # any type: several edges p -> m
        lines = VGroup(*[Arrow(a + UP * 0.1 * s, b + UP * 0.1 * s, path_arc=-0.9 * s, **kw)
                         for s in (-1, 0, 1)])
    g = VGroup(p, m, lines)
    g.p, g.m, g.lines = p, m, lines
    return g


def form_row(src, caption, count, color, kind):
    code = Code(src, size=36)
    cap = T(caption, 30, color=DIM)
    code.move_to(ORIGIN, aligned_edge=LEFT).shift(LEFT * 6.0 + UP * 0.25)
    cap.next_to(code, DOWN, buff=0.18, aligned_edge=LEFT)
    drawing = form_drawing(kind).move_to([2.3, 0, 0])
    cnt = T(count, 40, color=color).move_to([5.25, 0, 0])
    g = VGroup(code, cap, drawing, cnt)
    g.code, g.caption, g.drawing, g.count = code, cap, drawing, cnt
    return g


FORMS = [
    ("(p) <-[:DIRECTED]- (m)", "edge from m to p", "0 rows", RED, "back"),
    ("(p) -[:DIRECTED]- (m)", "edge in either direction", "28 rows", GOLD, "both"),
    ("(p) --> (m)", "edge of any type from p to m", "55 rows", GOLD, "any"),
]
FORM_PITCH = 1.6


def arrow_forms():
    """Slide 104's three arrow forms, each with a tiny drawing and its count for Spielberg
    (RED 0, GOLD 28, GOLD 55); rows 1.6 apart, centred at ORIGIN, ~12.3 wide x 4.2 tall.
    `.rows[i]` has `.code .caption .drawing (.p .m .lines) .count`."""
    rows = [form_row(*f).shift(UP * FORM_PITCH * (1 - i)) for i, f in enumerate(FORMS)]
    g = VGroup(*rows)
    g.rows = rows
    return g


# ── clip 1: (m:Movie) over -[r:ACTED_IN]-> ─────────────────────────────────────────
def _hub(col, at, r=0.3):
    c = Circle(radius=r).set_stroke(col, 4).set_fill(col, 0.2).move_to(at)
    g = VGroup(c)
    g.circle = c
    return g


# ── clip 2: The Kid's cast as a comb of ACTED_IN edges ─────────────────────────────
Q104 = ("MATCH (p:Person) -[r:ACTED_IN]->\n      (m:Movie {title: 'The Kid'})\n"
        "RETURN p.name, r.roles\nORDER BY p.name\nLIMIT 4;")
CAST = [   # name, card text (as drawn), cell text (as printed)
    ("Albert Austin", "['Car Thief',\n 'Man in Shelter']", "['Car Thief', 'Man in Shelter']"),
    ("B.F. Blinn", "['His Assistant']", "['His Assistant']"),
    ("Beulah Bains", "['Bride']", "['Bride']"),
    ("Carl Miller", "['The Man']", "['The Man']"),
    ("Charles Chaplin", "['A Tramp']", None),
    ("Jackie Coogan", "['The Child']", None),
]
CAST_Y = [0.5, -0.35, -1.05, -1.75, -2.45, -3.15]
CAST_X, CAST_R = -3.3, 0.22
CARD_L, TURN_X = -2.85, 3.6
KID = np.array([5.6, -1.3, 0.0])
KID_R = 0.75
CARD_FS, CELL_FS = 28, 28
CW = 0.0083 * CELL_FS * 1.0   # Mono advance at 28
ROW_L = -5.45
ROW_Y = [3.25, 2.7, 2.15, 1.6]
CORRIDOR_L = 2.3              # flying cells keep their left edge right of every card


def kid_graph():
    kid_c = Circle(radius=KID_R).set_stroke(BLUE, 4).set_fill(BLUE, 0.2).move_to(KID)
    kid_t = T("The Kid", 30).next_to(kid_c, DOWN, buff=0.18)   # under the circle, as ch1 names vertices
    kid = VGroup(kid_c, kid_t)
    kid.circle, kid.label = kid_c, kid_t
    cast = []
    for (name, card_txt, _), y in zip(CAST, CAST_Y):
        c = Circle(radius=CAST_R).set_stroke(PINK, 4).set_fill(PINK, 0.2).move_to([CAST_X, y, 0])
        lab = T(name, 28)
        lab.next_to(c, LEFT, buff=0.2)
        t = Mono(card_txt, CARD_FS)
        box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=t.height + 0.24)
        box.set_stroke(GOLD, 2.5).set_fill(BG, 1)
        box.move_to([CARD_L + box.width / 2, y, 0])
        t.move_to(box)
        card = VGroup(box, t)
        card.box, card.text = box, t
        corner = np.array([TURN_X, y, 0])
        seg1 = Line(c.get_center() + RIGHT * (CAST_R + 0.06), corner).set_stroke(FG, 3)
        seg1.set_z_index(-1)
        rim = KID + normalize(corner - KID) * (KID_R + 0.06)
        seg2 = Line(corner, rim).set_stroke(FG, 3)
        seg2.add_tip(tip_length=0.2, tip_width=0.2)
        seg2.tip.set_fill(FG, 1).set_stroke(FG, 1)
        edge = VGroup(seg1, seg2)
        v = VGroup(c, lab)
        v.circle, v.label = c, lab
        g = VGroup(v, edge, card)
        g.v, g.edge, g.card, g.name = v, edge, card, name
        cast.append(g)
    etype = Mono("ACTED_IN", 26, color=DIM).next_to([2.4, CAST_Y[4], 0], UP, buff=0.12)
    return kid, cast, etype


def result_row(name, roles, y):
    row = Mono(f"{name:<13} │ {roles}", CELL_FS, t2c={"│": DIM})
    row.move_to([0, y, 0], aligned_edge=LEFT).set_x(ROW_L + row.width / 2)
    n = len(name.replace(" ", ""))
    head = VGroup(*row[:n + 1])
    cell = VGroup(*row[n + 1:])
    return head, cell


def path_fly(src, dst, waypoints=(), scale=1.0):
    """A copy of src (same text as dst) travels the polyline src -> waypoints -> dst, growing by
    `scale`, faint until it has left src. Returns (copy, anim); after the play swap copy for dst."""
    base = src.copy()
    start = np.array(waypoints[0])   # it surfaces in the free corridor right of the cards, on its row
    copy = src.copy().move_to(start).set_opacity(0)
    pts = [start, *[np.array(w) for w in waypoints[1:]], dst.get_center()]
    seg = [np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])]
    total = sum(seg)

    def point(s):
        d = s * total
        for (a, b), L in zip(zip(pts, pts[1:]), seg):
            if d <= L or L == seg[-1]:
                return a + (b - a) * min(d / L, 1) if L > 0 else b
            d -= L
        return pts[-1]

    def upd(m, a):
        s = rush_from(a)
        m.become(base)
        m.scale(1 + (scale - 1) * s)
        m.move_to(point(s))
        m.set_opacity(min(1.0, a / 0.15))

    return copy, UpdateFromAlphaFunc(copy, upd)


# ── clip 4: Spielberg's star and the printed row ───────────────────────────────────
Q_WHOLE = ("MATCH (p:Person {name: 'Steven Spielberg'})\n      -[r:DIRECTED]-> (m:Movie)\n"
           "RETURN p, r, m")
STAR_C = np.array([0.0, -1.35, 0.0])
TXT_P = "(:Person {birthyear: 1946, name: 'Steven Spielberg',\n  person_id: 'nm0000229'})"
TXT_R = "[:DIRECTED {job: 'director'}]"
TXT_M = ("(:Movie {genres: ['Action', 'Adventure'],\n"
         "  minutes: 127, movie_id: 'tt0097576', rating: 8.2,\n"
         "  rating_votes: 847877,\n"
         "  title: 'Indiana Jones and the Last Crusade',\n"
         "  type: 'movie', year: 1989})")


def star():
    hub = Circle(radius=0.45).set_stroke(PINK, 4).set_fill(PINK, 0.2).move_to(STAR_C)
    ring, arrows = [], []
    for i in range(28):
        u = rotate_vector(RIGHT, PI / 2 - i * TAU / 28)
        c = Circle(radius=0.15).set_stroke(BLUE, 3).set_fill(BLUE, 0.2).move_to(STAR_C + u * 2.25)
        ring.append(c)
        arrows.append(Arrow(STAR_C + u * 0.5, STAR_C + u * 2.06, buff=0, stroke_width=2, color=FG,
                            tip_length=0.12, max_tip_length_to_length_ratio=0.2))
    return hub, ring, arrows


class Props(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- c2.props.1
    def clip1(self):
        shot = S4.handover_shot()
        code, table = shot[0], shot[1]
        self.add(code, table)
        with self.say("c2.props.1") as c:
            code.generate_target()
            code.target.scale(0.84).to_edge(UP, buff=0.4)
            self.play(*disappear(table), MoveToTarget(code), run_time=min(1.4, c.until("colon")))
            c.wait_until("colon")

            a = Code("(m:Movie)", size=48)
            b = Code("-[r:ACTED_IN]->", size=48)
            a.move_to([0, 0.35, 0])
            b.move_to([0, -0.55, 0])
            b.shift(RIGHT * (a.find(":").get_x() - b.find(":").get_x()))
            tx = max(a.get_right()[0], b.get_right()[0]) + 0.7
            ta = T("name : label", 32, color=DIM)
            tb = T("name : type", 32, color=DIM)
            ta.move_to([0, a.get_y(), 0], aligned_edge=LEFT).set_x(tx + ta.width / 2)
            tb.move_to([0, b.get_y(), 0], aligned_edge=LEFT).set_x(tx + tb.width / 2)
            pieces = VGroup(a, b, ta, tb)
            dx = -pieces.get_center()[0]
            pieces.shift(RIGHT * dx)
            self.play(*set_alpha([code], 0.35), *appear(a, ta, lag=0.4),
                      run_time=min(1.5, c.until("and the type")))
            c.wait_until("and the type")
            self.play(*appear(b, tb, lag=0.4), run_time=1.2)   # early: the second tag completes the pair just read
            c.wait_until("r")

            r = b.find("r")
            self.play(*recolor(r, YELLOW), FlashAround(r, color=YELLOW), run_time=1.0)
            pv = _hub(PINK, [-2.6, -2.05, 0])
            mv = _hub(BLUE, [2.6, -2.05, 0])
            edge = G1.typed_edge(pv, mv, "ACTED_IN")
            self.play(*appear(pv, mv, shift=None), G1.grow_edge(edge.arrow), run_time=1.4)
            self.play(*appear(edge.label), run_time=min(1.0, c.until("called")))
            c.wait_until("called")
            rtag = G1.label_tag("r", YELLOW).next_to(edge.label, LEFT, buff=0.25)
            self.play(*appear(rtag), FlashAround(r, color=YELLOW), run_time=1.2)
            c.wait_until("props")
            card = G1.prop_card([("roles", "[...]")], color=GOLD).next_to(edge.arrow, DOWN, buff=0.25)
            self.play(*appear(card), run_time=1.2)
            c.wait_until()

    # ---------------------------------------------------------------- c2.props.2
    def clip2(self):
        with self.say("c2.props.2") as c:
            code = Code(Q104, size=28)
            code.move_to(ORIGIN).to_edge(UP, buff=0.4)
            sweep_clear(self, *appear(code, shift=None), run_time=min(1.4, c.until("who acted")))
            c.wait_until("who acted")

            kid, cast, etype = kid_graph()
            self.kid, self.cast = kid, cast
            self.play(*appear(kid, shift=None),   # early: the whole cast is drawn first, then walked
                      *appear(*[g.v for g in cast], lag=0.12, shift=None), run_time=1.5)
            anims = []
            for g in cast:
                anims += [Create(g.edge[0]), G1.grow_edge(g.edge[1])]
            self.play(*anims, *appear(*[g.card for g in cast], lag=0.1, shift=None), *appear(etype, shift=None),
                      run_time=min(1.6, c.until("query")))   # early: the cards are read from {rows} on
            c.wait_until("query")

            box = token_box(code.find("(m:Movie {title: 'The Kid'})"), code.line(1))
            self.play(FadeIn(box), FlashAround(kid.circle, color=YELLOW), run_time=1.2)
            c.wait_until("we return")
            self.play(Transform(box, token_box(code.find("p.name, r.roles"), code.line(2))), run_time=1.2)
            c.wait_until("rows")

            heads, cells = [], []
            for i in range(4):
                name, _, roles = CAST[i]
                h, cl = result_row(name, roles, ROW_Y[i])
                heads.append(h)
                cells.append(cl)
            self.heads, self.cells = heads, cells
            sc = CELL_FS / CARD_FS
            cp0, an0 = path_fly(cells[0], cells[0], [cast[0].card.get_top() + UP * 0.3])
            self.play(*during(disappear(code, box), 0, 0.3),
                      *during(appear(heads[0], shift=None), 0.35, 0.8),
                      *during(an0, 0.35, 1.0),
                      run_time=1.9)
            self.remove(cp0)
            self.add(cells[0])
            anims, copies = [], []
            for i in (1, 2, 3):
                src = cast[i].card.text
                y0 = src.get_y()
                w = src.width * sc
                xr = CORRIDOR_L + w / 2
                way = [(xr, y0, 0), (xr, ROW_Y[i], 0)]
                a0 = (i - 1) * 0.32
                anims += during(appear(heads[i], shift=None), a0 + 0.1, a0 + 0.36)
                cp, an = path_fly(src, cells[i], way, scale=sc)
                copies.append(cp)
                anims += during(an, a0, a0 + 0.36)
            self.play(*anims, run_time=2.4)
            for cp, cl in zip(copies, cells[1:]):
                self.remove(cp)
                self.add(cl)
            c.wait_until("he played")
            self.play(FlashAround(cells[0], color=YELLOW), FlashAround(cast[0].card, color=YELLOW),
                      run_time=1.5)
            c.wait_until("chaplin")
            ch, co = cast[4], cast[5]
            self.play(*recolor([*ch.edge], YELLOW), ch.card.box.animate.set_stroke(YELLOW),
                      FlashAround(ch.card, color=YELLOW), run_time=1.3)
            c.wait_until("jackie coogan")
            self.play(*recolor([*co.edge], YELLOW), co.card.box.animate.set_stroke(YELLOW),
                      FlashAround(co.card, color=YELLOW), run_time=1.3)
            c.wait_until()

    # ---------------------------------------------------------------- c2.props.3
    def clip3(self):
        cells = self.cells
        with self.say("c2.props.3") as c:
            brackets = [g for cl in cells for g in (cl[0], cl[-1])]
            self.play(*[FlashAround(b, color=YELLOW, buff=0.06, time_width=1.5) for b in brackets],
                      run_time=min(1.6, c.until("several")))
            c.wait_until("several")
            self.play(*recolor(cells[0], YELLOW), FlashAround(cells[0], color=YELLOW, time_width=1.5),
                      run_time=1.6)
            c.wait_until("keanu")

            kr = G1.vertex("Keanu Reeves", "Person", at=[-2.7, 0, 0])
            mx = G1.vertex("The Matrix Resurrections", "Movie", at=[2.7, 0, 0])
            edge = G1.typed_edge(kr, mx, "ACTED_IN")
            card = G1.prop_card([("roles", "['Neo', 'Thomas Anderson']")], color=GOLD)
            card.next_to(edge.label, UP, buff=0.25)
            VGroup(kr, mx, edge, card).scale(1.3).move_to(ORIGIN)   # the pair is the hero: big, centred
            sweep_clear(self, *appear(kr, mx, lag=0.3, shift=None), run_time=1.2)
            self.play(G1.grow_edge(edge.arrow), *appear(edge.label), run_time=min(1.2, c.until("plays both")))
            c.wait_until("plays both")
            self.play(*appear(card), run_time=1.2)
            c.wait_until("edge")
            self.play(FlashAround(card, color=YELLOW, time_width=1.5),
                      VShowPassingFlash(edge.arrow.copy().set_stroke(YELLOW, 8), time_width=0.6),
                      run_time=1.6)
            c.wait_until("one actor")
            self.play(FlashAround(kr.circle, color=PINK), run_time=1.0)
            c.wait_until("one film")
            self.play(FlashAround(mx.circle, color=BLUE), run_time=min(1.0, c.until(floor=0.4)))
            c.wait_until()

    # ---------------------------------------------------------------- c2.props.4
    def clip4(self):
        with self.say("c2.props.4") as c:
            code = Code(Q_WHOLE, size=32)
            code.move_to(ORIGIN).to_edge(UP, buff=0.45)
            sweep_clear(self, *appear(code, shift=None), run_time=1.4)
            c.wait_until("star")

            hub, ring, arrows = star()
            self.play(FadeIn(hub), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(r)) for a, r in zip(arrows, ring)],
                                  lag_ratio=0.12), run_time=min(2.4, c.until("directed edges")))
            c.wait_until("directed edges")
            name = T("Steven Spielberg", 30).next_to(hub, LEFT, buff=0.15).set_x(-4.6)
            n28 = T("28", 60, color=GOLD).move_to([4.2, STAR_C[1], 0])
            self.play(*appear(name), run_time=1.0)   # early: names the hub as the voice says "Spielberg's"
            c.wait_until("twenty-eight")
            self.play(*appear(n28), run_time=1.0)
            c.wait_until("text")

            labs, blocks = [], []
            for key, src in (("p", TXT_P), ("r", TXT_R), ("m", TXT_M)):
                blocks.append(Code(src, size=28))
                labs.append(Mono(key, 28, color=DIM))
            col = VGroup(*blocks).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
            col.move_to([0.3, -1.05, 0])
            for lab, blk in zip(labs, blocks):
                lab.next_to(blk.line(0), LEFT, buff=0.35)
            sweep_clear(self, *appear(*[VGroup(l, b) for l, b in zip(labs, blocks)], lag=0.3, shift=None),
                        keep=[code], run_time=2.0)
            c.wait_until("round brackets")
            pb, rb, mb = blocks
            rnd = [pb.text[0], pb.text[-1], mb.text[0], mb.text[-1]]
            self.play(*[FadeIn(SurroundingRectangle(g, color=YELLOW, buff=0.07, stroke_width=3)) for g in rnd],
                      run_time=1.0)
            c.wait_until("square brackets")
            self.play(*[FadeIn(SurroundingRectangle(g, color=YELLOW, buff=0.07, stroke_width=3))
                        for g in (rb.text[0], rb.text[-1])], run_time=1.0)
            c.wait_until()

    # ---------------------------------------------------------------- c2.props.5
    def clip5(self):
        with self.say("c2.props.5") as c:
            ref = form_row("(p) -[:DIRECTED]-> (m)", "edge from p to m", "28 rows", GOLD, "fwd")
            ref.shift(UP * 2.65)
            rule = Line([-6.0, 1.75, 0], [6.3, 1.75, 0]).set_stroke(DIM, 2)
            forms = arrow_forms().shift(DOWN * 0.75)
            rows = forms.rows
            sweep_clear(self, *appear(ref, rule, lag=0.2, shift=None),   # early: the known form, as reference
                        run_time=min(1.6, c.until("back")))
            c.wait_until("back")

            r0 = rows[0]
            self.play(*appear(r0.code, r0.caption, r0.drawing, lag=0.3, shift=None),   # early: the form read with its gloss
                      run_time=1.5)
            c.wait_until("zero rows")
            self.play(*appear(r0.count), run_time=1.0)
            c.wait_until("why")
            self.play(VShowPassingFlash(ref.drawing.lines[0].copy().set_stroke(YELLOW, 8), time_width=0.6),
                      FlashAround(ref.drawing, color=YELLOW), run_time=1.5)
            c.wait_until("fits nowhere")
            self.play(*recolor([*r0.drawing.lines], RED), FlashAround(r0.drawing, color=RED), run_time=1.3)
            c.wait_until("both")

            r1 = rows[1]
            self.play(*appear(r1.code, r1.caption, r1.drawing, lag=0.3, shift=None),   # early: the form read with its gloss
                      run_time=1.5)
            c.wait_until("twenty-eight")
            self.play(*appear(r1.count), run_time=1.0)
            c.wait_until("any")

            r2 = rows[2]
            self.play(*appear(r2.code, r2.caption, r2.drawing, lag=0.3, shift=None),   # early: the form read with its gloss
                      run_time=1.4)
            self.play(*appear(r2.count), run_time=min(1.0, c.until(floor=0.5)))
            c.wait_until()
        self.wait(3.0)   # let "55 rows" land before the board clears
