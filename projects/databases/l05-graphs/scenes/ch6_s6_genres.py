"""Chapter 6, scene 6: Exercise 22, genres as a list or as Genre vertices. Clips c6.genres.1 – c6.genres.5."""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

_ex = load_scene("ch5_s7_exercises")
exercise_cards, exercise_panel = _ex.exercise_cards, _ex.exercise_panel
node, edge_between = _ex.node, _ex.edge_between

# ---------------------------------------------------------------- layout
DY = 2.4                                   # the designs sit this much lower inside the clip-1 panel
L_M = np.array([-6.0, 1.85, 0])            # Annie Hall, list design
R_M = np.array([0.85, 1.5, 0])             # Annie Hall, vertex design
COM = np.array([3.75, 2.3, 0])
ROM = np.array([3.75, 0.68, 0])
RM, RG = 0.62, 0.78
L_RES = np.array([-0.85, 0.05, 0])
R_RES = np.array([0.85, 0.05, 0])
BAND = np.array([0, -2.0, 0])
ROWS = [-0.85, -1.85, -2.85]
LX, RX = -3.85, 3.95

Q_LIST = """MATCH (m:Movie)
WHERE 'Romance' IN m.genres AND 'Comedy' IN m.genres
RETURN count(m);"""
Q_VERT = """MATCH (:Genre {name: 'Romance'}) <-[:HAS_GENRE]- (m:Movie)
      -[:HAS_GENRE]-> (:Genre {name: 'Comedy'})
RETURN count(m);"""
Q_COPY1 = """MATCH (m:Movie) UNWIND m.genres AS g
WITH DISTINCT g
CREATE (:Genre {name: g});"""
Q_COPY2 = """MATCH (m:Movie) UNWIND m.genres AS g
MATCH (genre:Genre {name: g})
CREATE (m) -[:HAS_GENRE]-> (genre);"""
Q_EQ = """MATCH (m:Movie)
WHERE m.genres = ['Romance', 'Comedy']
RETURN count(m);"""
Q_ONE = """MATCH (m:Movie) -[:HAS_GENRE]-> (g:Genre)
WHERE g.name = 'Romance' AND g.name = 'Comedy'
RETURN count(m);"""
Q_REN_L = """MATCH (m:Movie)
WHERE 'Sci-Fi' IN m.genres
SET m.genres = [x IN m.genres |
  CASE WHEN x = 'Sci-Fi' THEN
  'Science Fiction' ELSE x END];"""
Q_REN_R = """MATCH (g:Genre
  {name: 'Sci-Fi'})
SET g.name =
  'Science Fiction';"""
Q_EPIC = """CREATE (:Genre
  {name: 'Epic'})"""


def glist(s, size=27, all_teal=False):
    """A list literal in Mono: TEAL brackets, GOLD strings (all TEAL if all_teal)."""
    t = Mono(s, size=size, color=TEAL if all_teal else FG)
    if not all_teal:
        for ch in ("[", "]"):
            for g in select(t, ch):
                g.set_color(TEAL)
        for word in ("'Comedy'", "'Romance'", "'Documentary'", "'News'"):
            if word in s:
                for g in select(t, word):
                    g.set_color(GOLD)
    return t


def prop_box(lst, key="genres:", size=27, center=ORIGIN):
    k = Mono(key, size=size, color=DIM)
    body = VGroup(k, lst).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.12, width=body.width + 0.4, height=body.height + 0.36)
    box.set_stroke(DIM, 2).set_fill(BG, 1)
    g = VGroup(box, body)
    g.move_to(center)
    g.box, g.key, g.lst = box, k, lst
    return g


def list_design():
    ma = node(L_M, RM, BLUE, ["Annie", "Hall"], size=27)
    lst = glist("['Comedy', 'Romance']")
    pb = prop_box(lst, center=[-2.68, L_M[1], 0])
    tie = Line(ma[0].get_right(), pb.box.get_left()).set_stroke(DIM, 2)
    g = VGroup(ma, tie, pb)
    g.node, g.tie, g.pb, g.lst = ma, tie, pb, lst
    return g


def edge_label(e, side):
    v = e.get_end() - e.get_start()
    ang = np.arctan2(v[1], v[0])
    lab = Mono("HAS_GENRE", size=20, color=DIM).rotate(ang)
    nrm = np.array([-np.sin(ang), np.cos(ang), 0]) * side
    lab.move_to((e.get_start() + e.get_end()) / 2 + 0.26 * nrm)
    return lab


def vertex_design():
    mb = node(R_M, RM, BLUE, ["Annie", "Hall"], size=27)
    com = node(COM, RG, PURPLE, ["Comedy"], size=27)
    rom = node(ROM, RG, PURPLE, ["Romance"], size=27)
    e1 = edge_between(R_M, RM, COM, RG)
    e2 = edge_between(R_M, RM, ROM, RG)
    l1, l2 = edge_label(e1, 1), edge_label(e2, -1)
    g = VGroup(e1, e2, mb, com, rom, l1, l2)
    g.node, g.com, g.rom, g.e1, g.e2, g.l1, g.l2 = mb, com, rom, e1, e2, l1, l2
    return g


def recap_tile():
    """Static tile for the recap: Annie Hall's TEAL list against its two PURPLE Genre circles (~7.4 x 2.2)."""
    lst = glist("['Comedy', 'Romance']", size=30, all_teal=True)
    vs = T("vs", size=30, color=DIM)
    com = node(ORIGIN, 0.62, PURPLE, ["Comedy"], size=24)
    rom = node(ORIGIN, 0.62, PURPLE, ["Romance"], size=24)
    circles = VGroup(com, rom).arrange(RIGHT, buff=0.4)
    tile = VGroup(lst, vs, circles).arrange(RIGHT, buff=0.5).move_to(ORIGIN)
    return tile


pause_icon = load_scene("ch6_s1_intro").pause_icon


def food_box(x, y):
    t = T("Food, Inc.", size=28, color=FG)
    box = RoundedRectangle(corner_radius=0.1, width=t.width + 0.3, height=0.52).set_stroke(BLUE, 3).set_fill(BG, 1)
    g = VGroup(box, t.move_to(box))
    g.move_to([x, y, 0])
    return g


def has_genre_card():
    hdr = [Mono("movie_id", size=27, color=DIM), Mono("genre_id", size=27, color=DIM)]
    rows = [[Mono("tt0012349", size=27), Mono(g, size=27, color=GOLD)] for g in ("5", "8", "11")]
    x0, x1, pitch = -1.05, 1.2, 0.38
    cells = VGroup()
    for i, (a, b) in enumerate([hdr] + rows):
        a.move_to([x0, -i * pitch, 0])
        b.move_to([x1, -i * pitch, 0])
        cells.add(a, b)
    rule = Line([-2.15, -0.19, 0], [2.15, -0.19, 0]).set_stroke(BLUE, 1.5)
    box = RoundedRectangle(corner_radius=0.12, width=4.7, height=1.78).set_stroke(BLUE, 3).set_fill(BLUE, 0.06)
    box.move_to(cells)
    title = T("has_genre", size=28, color=BLUE).next_to(box, UP, buff=0.1)
    return VGroup(box, rule, cells, title)


def doc_card():
    src = Mono('"genres": [\n  "Comedy", "Drama",\n  "Family"]', size=26, color=TEAL, line_spacing=0.9)
    box = RoundedRectangle(corner_radius=0.12, width=src.width + 0.5, height=src.height + 0.4)
    box.set_stroke(TEAL, 3).set_fill(TEAL, 0.05).move_to(src)
    return VGroup(box, src)


class Genres(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c6.genres.1
    def clip1(self):
        with self.say("c6.genres.1") as c:
            cards = exercise_cards().scale(1.2).move_to(ORIGIN)
            self.play(*appear(cards, shift=None), run_time=0.4)
            card = cards[4]
            panel = exercise_panel("22")
            others = [cards[i] for i in range(4)]
            self.play(*during([ReplacementTransform(card.box.copy(), panel.frame)], 0, 0.7),
                      *during(disappear(*others, card), 0, 0.5),
                      *during(appear(panel.title), 0.55, 1), run_time=1.2)
            self.play(*appear(panel.qgrp, shift=0.15 * DOWN), run_time=1.0)  # early: the card's question is shown whole
            self.panel = panel

            self.L = list_design().shift(DY * DOWN)
            self.R = vertex_design().shift(DY * DOWN)
            c.wait_until("a list")
            self.play(*appear(self.L.node, self.L.tie, self.L.pb, lag=0.3, shift=None),
                      run_time=min(1.4, c.until("alternative")))
            c.wait_until("genre vertex")
            R = self.R
            self.play(*appear(R.node, R.com, R.rom, lag=0.25, shift=None), run_time=1.2)  # early: design B's vertices, named in clip 2
            c.wait_until("edges")
            self.play(GrowFromPoint(R.e1, R.e1.get_start()), GrowFromPoint(R.e2, R.e2.get_start()),
                      *during(appear(R.l1, R.l2, lag=0.2, shift=None), 0.4, 1), run_time=1.3)
            c.wait_until("task")
            self.play(FlashAround(panel.question, run_time=2, time_width=1.5))
            c.wait_until("stop")
            icon = pause_icon().next_to(panel.title, RIGHT, buff=0.5)
            self.play(*appear(icon, shift=None), run_time=0.6)
            self.icon = icon

    # ------------------------------------------------------------ c6.genres.2
    def clip2(self):
        L, R, panel = self.L, self.R, self.panel
        with self.say("c6.genres.2") as c:
            tag_target = panel.title.copy().scale(0.6).to_corner(UL, buff=0.5)
            self.play(*during(disappear(panel.frame, panel.qgrp, self.icon), 0, 0.45),
                      *during([panel.title.animate.become(tag_target)], 0.2, 0.8),
                      *during([L.animate.shift(DY * UP), R.animate.shift(DY * UP)], 0.4, 1), run_time=1.5)
            self.tag = panel.title
            hl = T("list property", size=34, color=TEAL).move_to([-2.9, 3.3, 0])
            hr = T("Genre vertices", size=34, color=PURPLE).move_to([3.55, 3.3, 0])
            div = Line([0, 3.1, 0], [0, 0.5, 0]).set_stroke(DIM, 2)
            self.play(*appear(hl, hr, shift=None), FadeIn(div), run_time=0.8)  # early: column headers of the split
            self.heads = [hl, hr, div]

            q = Code(Q_LIST, size=26).move_to(BAND)
            self.play(*appear(q, shift=None), run_time=1.0)
            c.wait_until("romance must")
            l1 = q.line(1)
            box = token_box(q.find("'Romance' IN m.genres"), l1)
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("so must comedy")
            self.play(Transform(box, token_box(q.find("'Comedy' IN m.genres"), l1)), run_time=0.8)
            c.wait_until("that gives")
            r174 = T("174", size=44, color=GOLD).move_to(L_RES)
            self.play(FadeOut(box), FlashUnder(q.find("count(m)"), color=GOLD, run_time=1.2),
                      *appear(r174, shift=None), run_time=1.2)
            self.r174 = r174

            c.wait_until("vertexq")
            qv = Code(Q_VERT, size=28).move_to(BAND)
            self.play(*swap(q, qv), run_time=1.2)
            c.wait_until("a movie with")
            mlab = Mono("m", size=34, color=BLUE).move_to(R.node[0])
            self.play(*swap(R.node[1], mlab, shift=None),
                      R.e1.animate.set_color(YELLOW), R.e2.animate.set_color(YELLOW),
                      R.com[0].animate.set_stroke(YELLOW), R.rom[0].animate.set_stroke(YELLOW), run_time=1.5)
            self.mlab = mlab

            c.wait_until("copy")
            tagc = T("built on a scratch copy", size=28, color=DIM)
            k1 = Code(Q_COPY1, size=22)
            r1 = Mono("nodes created: 23, properties set: 23, labels added: 23", size=22, color=DIM,
                      t2c={"nodes created: 23": GOLD})
            k2 = Code(Q_COPY2, size=22)
            r2 = Mono("relationships created: 7826", size=22, color=DIM, t2c={"relationships created: 7826": GOLD})
            blk = VGroup(k1, r1, k2, r2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            blk[2].shift(0.08 * DOWN)
            blk[3].shift(0.08 * DOWN)
            blk.move_to(BAND + 0.12 * UP).to_edge(LEFT, buff=0.7)
            k1.set_opacity(0.6)
            k2.set_opacity(0.6)
            tagc.move_to([4.6, k1.get_top()[1] - 0.2, 0])
            self.play(*swap(qv, VGroup(k1, k2)), *during(appear(tagc, shift=None), 0.5, 1), run_time=1.3)
            c.wait_until("twenty-three")
            self.play(*appear(r1, shift=None), run_time=0.8)
            c.wait_until("seven thousand")
            self.play(*appear(r2, shift=None), run_time=0.8)

            c.wait_until("agree")
            qv2 = Code(Q_VERT, size=28).move_to(BAND)
            self.play(*during(disappear(k1, k2, r1, r2, tagc), 0, 0.45),
                      *during(appear(qv2, shift=None), 0.5, 1), run_time=1.2)
            r174b = T("174", size=44, color=GOLD).move_to(R_RES)
            tick = check_mark(GREEN).scale(0.7).move_to([0, 0.05, 0])
            self.play(FlashUnder(qv2.find("count(m)"), color=GOLD, run_time=1.2),
                      *appear(r174b, shift=None), *during(appear(tick, shift=None), 0.5, 1), run_time=1.2)
            self.qv, self.r174b, self.tick = qv2, r174b, tick

    # ------------------------------------------------------------ c6.genres.3
    def clip3(self):
        L, R = self.L, self.R
        with self.say("c6.genres.3") as c:
            alab = node(R_M, RM, BLUE, ["Annie", "Hall"], size=27)[1]
            self.play(*disappear(self.qv),  # early: Annie Hall's label returns to the design
                      *swap(self.mlab, alab, shift=None),
                      R.e1.animate.set_color(FG), R.e2.animate.set_color(FG),
                      R.com[0].animate.set_stroke(PURPLE), R.rom[0].animate.set_stroke(PURPLE), run_time=1.2)
            self.alab = alab

            c.wait_until("equal")
            q = Code(Q_EQ, size=30).move_to(BAND)
            self.play(*during(disappear(self.r174, self.r174b, self.tick), 0, 0.45),
                      *during(appear(q, shift=None), 0.45, 1), run_time=1.4)
            c.wait_until("that gives zero")
            z = Mono("0", size=40, color=RED).next_to(q.line(2), RIGHT, buff=0.6)
            self.play(FlashUnder(q.find("count(m)"), color=RED, run_time=1.0),
                      *appear(z, shift=None), run_time=1.0)

            c.wait_until("annie")
            self.play(FlashAround(L.lst, color=TEAL, run_time=1.2, time_width=1.5))
            lit = q.find("['Romance', 'Comedy']")
            cp = glist("['Romance', 'Comedy']")
            cp.next_to(L.pb.box, DOWN, buff=0.35).align_to(L.lst, LEFT)
            self.play(*fly(lit, cp, arc=-0.6), run_time=1.5)
            a_c, a_r = select(L.lst, "'Comedy'")[0], select(L.lst, "'Romance'")[0]
            b_r, b_c = select(cp, "'Romance'")[0], select(cp, "'Comedy'")[0]
            x1 = Line(a_c.get_bottom() + 0.06 * DOWN, b_c.get_top() + 0.06 * UP).set_stroke(RED, 3)
            x2 = Line(a_r.get_bottom() + 0.06 * DOWN, b_r.get_top() + 0.06 * UP).set_stroke(RED, 3)
            neq = MathTex(r"\neq", font_size=56, color=RED).next_to(cp, LEFT, buff=0.3)
            self.play(Create(x1), Create(x2), *during(appear(neq, shift=None), 0.4, 1), run_time=1.4)

            c.wait_until("one")
            q2 = Code(Q_ONE, size=28).move_to(BAND)
            self.play(*during(disappear(q, z, cp, x1, x2, neq), 0, 0.45),
                      *during(appear(q2, shift=None), 0.5, 1), run_time=1.4)
            c.wait_until("zero again")
            z2 = Mono("0", size=40, color=RED).next_to(q2.line(2), RIGHT, buff=0.6)
            self.play(FlashUnder(q2.find("count(m)"), color=RED, run_time=0.8),
                      *appear(z2, shift=None), run_time=0.8)

            c.wait_until("onevertex")
            mid = np.array([COM[0], 1.5, 0])
            one = node(mid, 0.8, PURPLE, ["Romance", "Comedy"], size=27)
            e0 = edge_between(R_M, RM, mid, 0.8)
            self.play(*during(disappear(R.e1, R.e2, R.com, R.rom, R.l1, R.l2), 0, 0.45),
                      *during([GrowFromPoint(e0, e0.get_start())], 0.45, 1),
                      *during(appear(one, shift=None), 0.5, 1), run_time=1.2)
            c.wait_until("one name")
            x = Cross(one[0], stroke_color=RED, stroke_width=6, scale_factor=0.8)
            self.play(Create(x), run_time=0.8)
            c.wait_until("two edges")
            self.play(*during(disappear(one, e0, x), 0, 0.45),
                      *during(appear(R.e1, R.e2, R.com, R.rom, R.l1, R.l2, shift=None), 0.45, 1), run_time=1.2)
            self.play(VShowPassingFlash(R.e1.copy().set_stroke(YELLOW, 6), time_width=0.5),
                      VShowPassingFlash(R.e2.copy().set_stroke(YELLOW, 6), time_width=0.5), run_time=1.0)
            self.q2, self.z2 = q2, z2

    # ------------------------------------------------------------ c6.genres.4
    def clip4(self):
        L, R = self.L, self.R
        with self.say("c6.genres.4") as c:
            rule = Line([-6.6, -0.3, 0], [6.6, -0.3, 0]).set_stroke(DIM, 1.5)
            self.play(*during(disappear(self.q2, self.z2), 0, 0.5),
                      *during([GrowFromCenter(rule)], 0.4, 1), run_time=1.2)
            self.rule = rule

            c.wait_until("rename")
            self.play(*flash([select(L.lst, "'Comedy'")[0], select(L.lst, "'Romance'")[0]], color=GOLD,
                             run_time=1.2, time_width=1.5))
            ql = Code(Q_REN_L, size=27, line_spacing=0.75)
            ql.move_to([0, -1.17, 0], aligned_edge=UP).to_edge(LEFT, buff=0.55)
            self.play(*appear(ql, shift=None), run_time=1.0)
            c.wait_until("renaming")
            qr = Code(Q_REN_R, size=27, line_spacing=0.75).move_to([RX, -1.17, 0], aligned_edge=UP)
            self.play(*appear(qr, shift=None), run_time=1.0)
            c.wait_until("two hundred")
            c1l = Mono("properties set: 273", size=27, color=RED).move_to([LX, ROWS[0], 0])
            self.play(*appear(c1l, shift=None), run_time=0.8)
            c.wait_until("against")
            c1r = Mono("properties set: 1", size=27, color=GREEN).move_to([RX, ROWS[0], 0])
            self.play(*appear(c1r, shift=None), run_time=0.8)

            c.wait_until("news appears")
            lab1 = T("rename", size=30, color=DIM).move_to([0, ROWS[0], 0])
            self.play(*during(disappear(ql, qr), 0, 0.45),
                      *during(appear(lab1, shift=None), 0.5, 1), run_time=1.0)
            fb_l = food_box(LX, ROWS[1] + 0.27)
            flst = glist("['Documentary', 'News']").move_to([LX, ROWS[1] - 0.26, 0])
            fb_r = food_box(2.75, ROWS[1])
            news = node([5.35, ROWS[1], 0], 0.48, PURPLE, ["News"], size=27)
            fe = edge_between(fb_r.get_right() + 0.02 * RIGHT, 0.0, news[0].get_center(), 0.48)
            self.play(*appear(fb_l, flst, fb_r, fe, news, lag=0.2, shift=None), run_time=min(1.5, c.until("deleting")))
            c.wait_until("deleting")
            nw = select(flst, "'News'")[0]
            self.play(*recolor(nw, RED), *flash([fb_l, fb_r], color=RED, run_time=1.0), run_time=1.0)
            rest = [g for g in flst if not any(g is h for h in nw)]
            strike = Line(nw.get_left() + 0.08 * LEFT, nw.get_right() + 0.08 * RIGHT).set_stroke(RED, 3)
            lab2 = T("delete", size=30, color=DIM).move_to([0, ROWS[1], 0])
            self.play(*disappear(fb_l, fb_r, fe), *[g.animate.set_opacity(0) for g in rest],
                      *[g.animate.set_opacity(0.5) for g in nw],
                      *during([Create(strike)], 0.4, 1), *during(appear(lab2, shift=None), 0.5, 1), run_time=1.3)

            c.wait_until("missing")
            m1 = T("SQL: 26 genres  ·  lists: 23", size=28, t2c={"26": GOLD, "23": GOLD}).move_to([LX, ROWS[2] + 0.24, 0])
            self.play(*appear(m1, shift=None), run_time=1.0)
            c.wait_until("epic")
            m2 = T("Epic   Experimental   Gothic", size=28, color="#A8473F").move_to([LX, ROWS[2] - 0.26, 0])
            self.play(*appear(m2, shift=None), run_time=1.0)
            c.wait_until("no trace")
            settle(self, flst)
            lab3 = T("insert", size=30, color=DIM).move_to([0, ROWS[2], 0])
            self.play(*appear(lab3, shift=None), run_time=0.8)

            c.wait_until("anomalies")
            new_labs = [VGroup(T(w, size=28, color=YELLOW), T("anomaly", size=28, color=YELLOW))
                        .arrange(DOWN, buff=0.08).move_to([0, y, 0])
                        for w, y in zip(("update", "deletion", "insertion"), ROWS)]
            self.play(*swap(lab1, new_labs[0], shift=None), run_time=0.9)
            self.play(*swap(lab2, new_labs[1], shift=None), run_time=0.8)
            self.play(*swap(lab3, new_labs[2], shift=None), run_time=0.8)
            self.table = [c1l, c1r, flst, strike, news, m1, m2] + new_labs

    # ------------------------------------------------------------ c6.genres.5
    def clip5(self):
        L, R = self.L, self.R
        with self.say("c6.genres.5") as c:
            epic = Code(Q_EPIC, size=26).move_to([RX, ROWS[2], 0])
            ticks = [check_mark(GREEN).scale(0.6).move_to([1.3, y, 0]) for y in ROWS]
            self.play(*appear(epic, shift=None), *during(appear(*ticks, lag=0.3, shift=None), 0.3, 1), run_time=1.5)
            c.wait_until("properties")
            kb = VGroup(Mono("name:", size=27, color=DIM), Mono("'Comedy'", size=27, color=GOLD),
                        Mono("...", size=27, color=DIM)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            kbox = RoundedRectangle(corner_radius=0.1, width=kb.width + 0.2, height=kb.height + 0.26).set_stroke(DIM, 2)
            kgrp = VGroup(kbox, kb.move_to(kbox))
            kgrp.next_to(R.com[0], RIGHT, buff=0.08)
            self.play(*appear(kgrp, shift=None), run_time=1.0)

            c.wait_until("one vertex")
            self.play(FlashAround(R.com[0], color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("follow")
            fan = VGroup()
            for a in np.linspace(-65, 28, 24) * DEGREES:
                d = np.array([np.cos(a), np.sin(a), 0])
                s, e = COM + 1.6 * d, COM + (RG + 0.03) * d
                fan.add(VGroup(Line(s, e).set_stroke(GOLD, 1.5, opacity=0.8), Dot(s, radius=0.04, color=BLUE)))
            n878 = T("878", size=36, color=GOLD).move_to(COM + np.array([1.5, -1.45, 0]))
            self.play(*during(disappear(kgrp), 0, 0.35),
                      *during([LaggedStart(*[GrowFromPoint(f, f[0].get_start()) for f in fan], lag_ratio=0.05)],
                              0.3, 1),
                      *during(appear(n878, shift=None), 0.6, 1), run_time=1.6)
            c.wait_until("instead")
            bars = VGroup(*[Line([x, 0.42, 0], [x, 0.8, 0]).set_stroke(DIM, 3) for x in np.linspace(-6.4, -0.8, 34)])
            n2935 = T("2,935 movies", size=28, color=GOLD).move_to([-3.6, 0.05, 0])
            self.play(*appear(bars, n2935, shift=None), run_time=0.6)
            sw = Rectangle(width=0.16, height=0.55).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.3).move_to([-6.5, 0.61, 0])
            self.add(sw)
            self.play(sw.animate.move_to([-0.7, 0.61, 0]), run_time=min(2.4, c.until("listpro", floor=0.8)),
                      rate_func=linear)

            pros = []
            for txt, y in (("genres come with the movie", -0.95), ("shorter query", -1.85), ("no extra edges", -2.75)):
                tk = check_mark(GREEN).scale(0.6)
                t = T(txt, size=30)
                pros.append(VGroup(tk, t).arrange(RIGHT, buff=0.3).move_to([0, y, 0]).to_edge(LEFT, buff=0.8))
            cost = VGroup(T("+23 vertices", size=36, color=GOLD), T("+7,826 edges", size=36, color=GOLD))
            cost.arrange(DOWN, buff=0.35).move_to([RX, -1.85, 0])
            c.wait_until("carries")
            keep = [self.tag, *self.heads, L, R, self.alab]
            sweep_clear(self, *appear(pros[0], shift=None), keep=keep, run_time=1.4)
            c.wait_until("shorter")
            self.play(*appear(pros[1], shift=None), run_time=0.9)
            c.wait_until("extra edges")
            self.play(*appear(pros[2], shift=None), *during(appear(cost, shift=None), 0.4, 1), run_time=1.2)

            c.wait_until("denormalised")
            dn = T("denormalised", size=36, color=TEAL)
            dc = doc_card()
            nm = T("normalised", size=36, color=BLUE)
            hg = has_genre_card()
            hcap = T("7,826 rows = 7,826 HAS_GENRE edges", size=27, t2c={"7,826": GOLD})
            VGroup(nm, hg, hcap).arrange(DOWN, buff=0.13).move_to([3.3, -0.4, 0], aligned_edge=UP)
            nm.set_x(3.3)
            hg.set_x(3.3)
            dn.move_to([-3.55, nm.get_y(), 0])
            dc.move_to([-3.55, hg[0].get_y(), 0])
            dcap = T("a document's genres (Lecture 4)", size=28, color=DIM).move_to([-3.55, hcap.get_y(), 0])
            self.play(*during(disappear(*pros, cost), 0, 0.35),
                      *during(appear(dn, dc, dcap, lag=0.35, shift=None), 0.35, 1), run_time=2.0)
            c.wait_until("vertices are")
            self.play(*appear(nm, hg, lag=0.35, shift=None), run_time=1.3)
            self.play(*appear(hcap, shift=None), run_time=0.9)
