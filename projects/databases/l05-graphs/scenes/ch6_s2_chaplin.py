"""Chapter 6, scene 2: Exercise 20.1, directed and acted. Clips c6.chaplin.1 – c6.chaplin.4.

Exports (static, no updaters):
  recap_tile()  the fused pattern as this scene draws it: PINK hole p (:Person tag "Person"), BLUE hole m
                ("Movie"), joined by a lens of two YELLOW arrows p -> m, DIRECTED (upper arc) and ACTED_IN
                (lower arc), labels Mono 35 YELLOW. About 7.5 x 3.3, centred on ORIGIN.
                Attributes .p .m (holes: .ring .name_tag .label_tag), .arcs [directed, acted], .labels.
"""
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

EX = load_scene("ch5_s7_exercises")
MG = load_scene("ch1_s5_moviegraph")
MS = load_scene("ch2_s3_match")
INTRO = load_scene("ch6_s1_intro")


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- the pattern
PX, MX, PY = -2.7, 2.7, 1.1     # hole x's; the two unfused p holes sit at +-PY
LENS = 0.8                      # arc angle of the fused loop
HOLE_SCALE = 1.2
RING_R = 0.52 * HOLE_SCALE


def hole(name, label, color, side=LEFT):
    st = MS.stencil(label, name)
    st.scale(HOLE_SCALE, about_point=st.centre())
    st.ring.set_stroke(color)
    st.name_tag.set_fill(color)
    st.name_tag.next_to(st.ring, side, buff=0.15)
    if st.label_tag is not None:
        st.label_tag.set_fill(color)
        st.label_tag.next_to(st.ring, UP, buff=0.1)
    return st


def edge(a, b, r, angle, color=YELLOW, width=4):
    a, b = np.array(a), np.array(b)
    u = (b - a) / np.linalg.norm(b - a)
    s = a + r * rotate_vector(u, -angle / 2)
    e = b - r * rotate_vector(u, angle / 2)
    arc = ArcBetweenPoints(s, e, angle=angle).set_stroke(color, width)
    arc.add_tip(tip_length=0.24, tip_width=0.22)
    arc.tip.set_fill(color, 1).set_stroke(color, 0)
    return arc


def edge_label(text, arc, direction, color=YELLOW, size=35, buff=0.15):
    lab = set_backstroke(Mono(text, size, color))
    lab.next_to(arc.point_from_proportion(0.5), direction, buff=buff)
    return lab


def fused_parts():
    p = hole("p", "Person", PINK)
    m = hole("m", "Movie", BLUE, side=RIGHT)
    p.at(P(PX, 0))
    m.at(P(MX, 0))
    darc = edge(p.centre(), m.centre(), RING_R, -LENS)
    aarc = edge(p.centre(), m.centre(), RING_R, LENS)
    dlab = edge_label("DIRECTED", darc, UP)
    alab = edge_label("ACTED_IN", aarc, DOWN)
    return p, m, darc, aarc, dlab, alab


def recap_tile():
    p, m, darc, aarc, dlab, alab = fused_parts()
    g = VGroup(darc, aarc, p, m, dlab, alab)
    g.move_to(ORIGIN)
    g.p, g.m, g.arcs, g.labels = p, m, [darc, aarc], [dlab, alab]
    return g


# ---------------------------------------------------------------- code
Q1 = """MATCH (p:Person {name: 'Charles Chaplin'})
      -[:DIRECTED]-> (m:Movie) <-[:ACTED_IN]- (p)
RETURN m.title, m.year
ORDER BY m.year;"""
Q2 = """MATCH (p:Person {name: 'Charles Chaplin'})
      -[:DIRECTED]-> (m:Movie),
      (p) -[:ACTED_IN]-> (m)
RETURN m.title, m.year
ORDER BY m.year;"""
Q3 = """MATCH (p:Person {name: 'Charles Chaplin'})
      -[:DIRECTED]-> (m:Movie) <-[:ACTED_IN]- (q:Person)
RETURN m.title, q.name;"""
Q4 = """MATCH (p:Person {name: 'Clint Eastwood'})
      -[:DIRECTED]-> (m:Movie) <-[:ACTED_IN]- (p)
RETURN m.title, m.year
ORDER BY m.year;"""
CODE_UL = P(-6.4, 3.05)


def code(src):
    c = Code(src, size=28)
    c.align_to(CODE_UL, UL)
    return c


# ---------------------------------------------------------------- reply tables
def reply_table(cols, rows, x1, x2, y0, pitch=0.5, size=30, c2=GOLD):
    head = VGroup(Mono(cols[0], 28, DIM), Mono(cols[1], 28, DIM))
    head[0].move_to(P(0, y0)).align_to(P(x1, 0), LEFT)
    head[1].move_to(P(0, y0)).align_to(P(x2, 0), LEFT)
    out_rows = []
    for i, r in enumerate(rows):
        y = y0 - pitch * (i + 1)
        if r is None:
            row = VGroup(T("…", size, DIM).move_to(P(0, y)).align_to(P(x1, 0), LEFT))
        else:
            a = T(r[0], size).move_to(P(0, y)).align_to(P(x1, 0), LEFT)
            b = T(r[1], size, c2).move_to(P(0, y)).align_to(P(x2, 0), LEFT)
            row = VGroup(a, b)
        out_rows.append(row)
    right = max(m.get_right()[0] for m in [head[1]] + [r[-1] for r in out_rows])
    hline = Line(P(x1 - 0.15, y0 - pitch / 2), P(right + 0.15, y0 - pitch / 2)).set_stroke(DIM, 2)
    vline = Line(P(x2 - 0.3, y0 + 0.22), P(x2 - 0.3, y0 - pitch * len(rows) - 0.2)).set_stroke(DIM, 2)
    g = VGroup(hline, vline, head, *out_rows)
    g.head, g.rows, g.lines = head, out_rows, [hline, vline]
    return g


CHAPLIN_ROWS = [("The Kid", "1921"), ("The Gold Rush", "1925"), ("City Lights", "1931"),
                ("Modern Times", "1936"), ("The Great Dictator", "1940")]
TITLE_CUES = ["the kid", "the gold rush", "city lights", "modern times", "the great dictator"]
# the trap's reply as cypher-shell prints it (engine order): five film blocks, each the Chaplin row
# and one real co-cast row next to it in the printed order, then "⋮" for the film's other 8 rows
FIFTY_BLOCKS = [[("Modern Times", "Richard Alexander"), ("Modern Times", "Charles Chaplin")],
                [("The Kid", "Charles Chaplin"), ("The Kid", "Jackie Coogan")],
                [("The Gold Rush", "Charles Chaplin"), ("The Gold Rush", "Tom Murray")],
                [("The Great Dictator", "Charles Chaplin"), ("The Great Dictator", "Jack Oakie")],
                [("City Lights", "Charles Chaplin"), ("City Lights", "Florence Lee")]]


def fifty_table(x1=-0.3, x2=3.42, y0=1.45, pitch=0.35, gap=0.24, size=28):
    """m.title | q.name, five blocks of two rows + a DIM ⋮. .rows (all), .hits (the Chaplin rows), .dots."""
    head = VGroup(Mono("m.title", 28, DIM), Mono("q.name", 28, DIM))
    head[0].move_to(P(0, y0)).align_to(P(x1, 0), LEFT)
    head[1].move_to(P(0, y0)).align_to(P(x2, 0), LEFT)
    rows, hits, dots = [], [], []
    y = y0 - 0.48
    for block in FIFTY_BLOCKS:
        for title, name in block:
            a = T(title, size).move_to(P(0, y)).align_to(P(x1, 0), LEFT)
            b = T(name, size, RED).move_to(P(0, y)).align_to(P(x2, 0), LEFT)
            row = VGroup(a, b)
            rows.append(row)
            if name == "Charles Chaplin":
                hits.append(row)
            y -= pitch
        y -= gap
    for i in range(0, len(rows), 2):        # a vertical ellipsis under each block, in both columns
        top = min(rows[i + 1][0].get_bottom()[1], rows[i + 1][1].get_bottom()[1])
        nxt = rows[i + 2][0].get_top()[1] if i + 2 < len(rows) else top - 0.3
        cy = (top + nxt) / 2
        for x in (x1 + 0.5, x2 + 0.5):
            dots.append(VGroup(*[Dot(P(x, cy + 0.075 * k), radius=0.025, color=DIM) for k in (-1, 0, 1)]))
    bottom = dots[-1].get_bottom()[1]
    right = max(r[1].get_right()[0] for r in rows)
    hline = Line(P(x1 - 0.15, y0 - 0.24), P(right + 0.15, y0 - 0.24)).set_stroke(DIM, 2)
    vline = Line(P(x2 - 0.22, y0 + 0.22), P(x2 - 0.22, bottom)).set_stroke(DIM, 2)
    g = VGroup(hline, vline, head, *rows, *dots)
    g.head, g.rows, g.hits, g.dots, g.lines = head, rows, hits, dots, [hline, vline]
    return g


EASTWOOD_ROWS = [("Unforgiven", "1992"), ("A Perfect World", "1993"),
                 ("The Bridges of Madison County", "1995"), ("Million Dollar Baby", "2004"),
                 ("Gran Torino", "2008"), ("The Mule", "2018")]


def pause_icon(title):
    return INTRO.pause_icon().next_to(title, RIGHT, buff=0.45)


class Chaplin(NarratedScene):
    def construct(self):
        self.clip_card()
        self.clip_pattern()
        self.clip_run()
        self.clip_check()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c6.chaplin.1
    def clip_card(self):
        cards = EX.exercise_cards().scale(1.2).move_to(ORIGIN)
        panel = EX.exercise_panel("20.1")
        card = cards[0]
        with self.say("c6.chaplin.1") as c:
            self.play(*appear(*cards, shift=None, lag=0), run_time=0.4)  # early: the row of slots
            self.play(*during([ReplacementTransform(card.box.copy(), panel.frame),
                               *[FadeOut(k) for k in cards[1:]]], 0, 0.6),
                      *during([FadeOut(card)], 0.3, 0.7),
                      *during(appear(panel.title), 0.5, 1), run_time=1.2)
            c.wait_until(own_word=panel.question[0])
            self.play(*appear(panel.qgrp, shift=0.15 * DOWN), run_time=1.0)  # early: the question is shown whole
            c.wait_until("stop")
            icon = pause_icon(panel.title)
            self.play(*appear(icon, shift=None), run_time=0.6)
        self.panel, self.icon = panel, icon

    # ------------------------------------------------------------ c6.chaplin.2
    def build_fan(self):
        fn = MG.fan()
        lanes = VGroup(*fn.lanes)
        lanes.flip(UP, about_point=ORIGIN)               # Chaplin left, The Kid right
        kid, ch = fn.kid, fn.chaplin
        kid.shift(2 * MG.FAN_X * RIGHT)
        ch.shift(2 * MG.FAN_X * LEFT)
        for vv in (kid, ch):
            vv.label.set_x(vv.circle.get_x())
        if ch.label.get_left()[0] < -6.55:
            ch.label.shift((-6.55 - ch.label.get_left()[0]) * RIGHT)
        g = VGroup(ch, kid, *fn.lanes, *fn.label_bgs, *fn.labels)
        g.shift(1.75 * DOWN)
        return fn

    def clip_pattern(self):
        panel = self.panel
        fn = self.build_fan()
        tag = panel.title
        ACT, DIR = 0, 2

        p1 = hole("p", "Person", PINK).at(P(PX, PY))
        p2 = hole("p", None, PINK).at(P(PX, -PY))
        m = hole("m", "Movie", BLUE, side=RIGHT).at(P(MX, 0))
        darc = edge(p1.centre(), m.centre(), RING_R, -0.05)
        aarc = edge(p2.centre(), m.centre(), RING_R, 0.05)
        dlab = edge_label("DIRECTED", darc, UP, buff=0.4)
        alab = edge_label("ACTED_IN", aarc, DOWN, buff=0.4)
        pat = VGroup(darc, aarc, p1, p2, m, dlab, alab)
        pat.shift(0.2 * UP)

        q1 = code(Q1)
        q1_ps = [q1.find("(p", line=0)[1], q1.find("(p)", line=1)[1]]
        for g in q1_ps:
            g.set_color(YELLOW)

        with self.say("c6.chaplin.2") as c:
            self.play(*during(disappear(panel.frame, panel.qgrp, self.icon), 0, 0.45),
                      *during([tag.animate.scale(0.6).to_corner(UL, buff=0.5)], 0.2, 0.8), run_time=1.0)
            c.wait_until("chaplin")
            self.play(*appear(fn.chaplin, fn.kid, lag=0.3), run_time=1.0)  # early: the two vertices arrive together
            c.wait_until("five edges")
            self.play(LaggedStart(*[Succession(Create(ln.path, run_time=1.0), FadeIn(ln.tip, run_time=0.25))
                                    for ln in fn.lanes], lag_ratio=0.18),
                      *[FadeIn(b) for b in fn.label_bgs],
                      *appear(*fn.labels, shift=0.12 * DOWN, lag=0.15),  # early: the five types label the five edges
                      run_time=min(2.0, c.until("two")))
            c.wait_until("two")
            rest = [k for k in range(5) if k not in (ACT, DIR)]
            self.play(*set_alpha([fn.lanes[k] for k in rest] + [fn.labels[k] for k in rest], DIMMED),
                      run_time=1.0)
            for k, word in [(DIR, "directed"), (ACT, "acted in")]:
                c.wait_until(word)
                ln = fn.lanes[k]
                self.play(ln.path.animate.set_stroke(YELLOW), ln.tip.animate.set_fill(YELLOW).set_stroke(YELLOW),
                          *recolor([fn.labels[k]], YELLOW), run_time=0.8)

            c.wait_until("pattern")
            sweep_clear(self, *[time_span(a, 0.6, 1.3) for a in appear(m, p1, p2, lag=0.2)],
                        keep=[tag], run_time=1.4)
            self.play(GrowFromPoint(darc, darc.get_start()), GrowFromPoint(aarc, aarc.get_start()),
                      *appear(dlab, alab, shift=None, lag=0.2), run_time=min(1.4, c.until("same")))  # early: the two edge types
            settle(self, pat)

            c.wait_until("same")
            self.play(*during([pat.animate.shift(1.55 * DOWN)], 0, 0.6),
                      *during(appear(q1, shift=None), 0.45, 1), run_time=1.6)  # early: the query arrives whole
            c.wait_until("twice")
            self.play(*flash(q1_ps), *flash([p1.name_tag, p2.name_tag], color=PINK), run_time=1.2)

            c.wait_until("fuse")
            mid = (p1.centre() + p2.centre()) / 2
            mc = m.centre()
            darc2 = edge(mid, mc, RING_R, -LENS)
            aarc2 = edge(mid, mc, RING_R, LENS)
            dlab2 = edge_label("DIRECTED", darc2, UP)
            alab2 = edge_label("ACTED_IN", aarc2, DOWN)
            self.play(p1.animate.shift(mid - p1.centre()), p2.animate.shift(mid - p2.centre()),
                      *during([p2.name_tag.animate.set_opacity(0)], 0, 0.5),
                      Transform(darc, darc2), Transform(aarc, aarc2),
                      dlab.animate.move_to(dlab2), alab.animate.move_to(alab2), run_time=1.8)
            self.remove(*p2.get_family())
            settle(self, pat, drop=[p2])
            c.wait_until("loop")
            self.play(VShowPassingFlash(darc.copy().set_stroke(YELLOW, 9), time_width=0.5),
                      VShowPassingFlash(aarc.copy().set_stroke(YELLOW, 9), time_width=0.5),
                      FlashAround(p1.ring, color=PINK, time_width=1.5), run_time=1.5)
        self.pat, self.p, self.m, self.darc, self.aarc, self.dlab, self.alab = pat, p1, m, darc, aarc, dlab, alab
        self.q1, self.tag = q1, tag

    # ------------------------------------------------------------ c6.chaplin.3
    def clip_run(self):
        pat, q1 = self.pat, self.q1
        tbl = reply_table(["m.title", "m.year"], CHAPLIN_ROWS, 0.6, 4.6, -0.05)
        count5 = T("5 rows", 34, GOLD).move_to(P(0, -3.3)).align_to(P(0.6, 0), LEFT)

        q2 = code(Q2)
        for g in [q2.find("(p", line=0)[1], q2.find("(p)", line=2)[1]]:
            g.set_color(YELLOW)
        p_marks = [q2.find("(p", line=0)[1], q2.find("(p)", line=2)[1]]
        m_marks = [q2.find("(m", line=1)[1], q2.find("(m)", line=2)[1]]
        ul_p = [underline(g, YELLOW, buff=0.08) for g in p_marks]
        ul_m = [underline(g, YELLOW, buff=0.08) for g in m_marks]

        q3 = code(Q3)
        q3.find("(p", line=0)[1].set_color(YELLOW)
        q3.find("(q:Person)", line=1).set_color(RED)
        q3.find("q.name", line=2).set_color(RED)

        with self.say("c6.chaplin.3") as c:
            c.wait_until("run")
            self.play(*during([pat.animate.scale(0.8).move_to(P(-3.6, -1.7))], 0, 0.7),
                      *during(appear(*tbl.lines, tbl.head, shift=None), 0.5, 1),  # early: the reply's header
                      run_time=min(1.4, c.until("the kid")))
            settle(self, tbl, drop=tbl.rows)
            for i, cue in enumerate(TITLE_CUES):
                c.wait_until(cue)
                extra = appear(count5, shift=None) if i == 4 else []
                self.play(*appear(tbl.rows[i], shift=0.12 * DOWN),  # early: the row count lands with the last row
                          VShowPassingFlash(self.darc.copy().set_stroke(YELLOW, 8), time_width=0.6),
                          VShowPassingFlash(self.aarc.copy().set_stroke(YELLOW, 8), time_width=0.6),
                          *extra, run_time=0.8)
            settle(self, tbl, add=tbl.rows)

            c.wait_until("comma")
            self.play(*swap(q1, q2, shift=0.15 * UP), run_time=1.4)
            c.wait_until("person")
            self.play(*[GrowFromCenter(u) for u in ul_p], run_time=0.8)
            c.wait_until("movie")
            self.play(*[GrowFromCenter(u) for u in ul_m], run_time=0.8)
            c.wait_until("same query")
            self.play(FlashAround(count5, color=GOLD, time_width=1.5), run_time=1.5)

            # ---- the trap
            c.wait_until("trap")
            p, m = self.p, self.m
            pc, mc = p.centre(), m.centre()
            r = p.ring.width / 2
            dots = VGroup(*[Dot(P(-5.6 + 0.45 * k, -2.85), radius=0.1, color=PINK).set_opacity(0.7)
                            for k in range(10)])
            q = hole("q", None, RED)
            q.scale(0.8, about_point=q.centre()).at(pc)
            q.name_tag.next_to(q.ring, UP, buff=0.08).shift(0.35 * LEFT)
            bend = ValueTracker(LENS)
            qarc = always_redraw(lambda: edge(q.centre(), m.centre(), r, bend.get_value(), color=RED))
            self.remove(*self.aarc.get_family())
            self.add(qarc)
            self.play(*disappear(*ul_p, *ul_m), run_time=0.4)
            self.play(*swap(q2, q3, shift=0.15 * UP), run_time=1.4)
            self.play(*disappear(self.alab), FadeIn(q), run_time=0.6)
            self.play(q.animate.shift(dots[0].get_center() - pc), bend.animate.set_value(0.25),
                      *appear(*dots, shift=None, lag=0.05), run_time=1.3)
            c.wait_until("fifty")
            self.play(q.animate.shift(dots[7].get_center() - dots[0].get_center()), rate_func=linear,
                      run_time=min(2.2, c.until("giving")))

            tbl50 = fifty_table()
            count50 = T("50 rows", 36, GOLD).move_to(P(0, 0.95)).align_to(P(-6.4, 0), LEFT)
            why = T("= 5 films × 10 actors", 32).next_to(count50, DOWN, buff=0.22, aligned_edge=LEFT)
            c.wait_until("giving")
            self.play(*swap(VGroup(tbl, count5), VGroup(tbl50, count50)), run_time=1.2)  # early: the reply is printed whole
            c.wait_until("ten for each")
            self.play(*appear(why, shift=None), run_time=1.0)  # early: the count's reason, said as "ten for each film"

            c.wait_until("inside")
            hits = tbl50.hits
            rest = [r_ for r_ in tbl50.rows if r_ not in hits]
            self.play(*recolor([g for h in hits for g in h], YELLOW), *set_alpha(rest, DIMMED),
                      *flash(hits), run_time=1.5)

    # ------------------------------------------------------------ c6.chaplin.4
    def clip_check(self):
        tag = self.tag
        cl = Circle(radius=1.5).set_stroke(GOLD, 5).set_fill(GOLD, 0.08).move_to(P(-1.7, -0.2))
        cr = Circle(radius=1.5).set_stroke(GOLD, 5).set_fill(GOLD, 0.08).move_to(P(1.7, -0.2))
        ll = T("directed: 5", 36, GOLD).next_to(cl, LEFT, buff=0.3)
        lr = T("acted in: 5", 36, GOLD).next_to(cr, RIGHT, buff=0.3)
        name = T("Charles Chaplin", 44, PINK).move_to(P(0, 2.2))

        q4 = code(Q4)
        q4.find("(p", line=0)[1].set_color(YELLOW)
        q4.find("(p)", line=1)[1].set_color(YELLOW)
        ec = P(-4.6, -1.3)
        el = Circle(radius=1.25).set_stroke(GOLD, 5).set_fill(GOLD, 0.08).move_to(ec)
        er = Circle(radius=1.0).set_stroke(GOLD, 5).set_fill(GOLD, 0.08).move_to(ec + 1.2 * RIGHT)
        dl = T("directed 15", 30, GOLD).next_to(el, UP, buff=0.15).shift(0.4 * LEFT)
        al = T("acted in 10", 30, GOLD).next_to(er, DOWN, buff=0.2).shift(0.4 * RIGHT)
        six = T("6", 44, YELLOW).move_to(ec + 0.85 * RIGHT)
        etbl = reply_table(["m.title", "m.year"], EASTWOOD_ROWS, -0.9, 5.1, 0.45, pitch=0.45, size=28)
        count6 = T("6 rows", 34, GOLD).move_to(P(0, -3.05)).align_to(P(-0.9, 0), LEFT)

        with self.say("c6.chaplin.4") as c:
            sweep_clear(self, keep=[tag], run_time=1.2)
            c.wait_until("coincide")
            self.play(*appear(name, cl, cr, shift=None, lag=0.2), *appear(ll, lr, lag=0.2), run_time=1.2)  # early: both sets at once
            c.wait_until("exactly")
            self.play(cl.animate.move_to(P(0, -0.2)), cr.animate.move_to(P(0, -0.2)),
                      ll.animate.shift(1.7 * RIGHT), lr.animate.shift(1.7 * LEFT), run_time=1.8)
            c.wait_until("directing alone")
            self.play(FlashAround(ll, color=GOLD, time_width=1.5), run_time=1.5)

            c.wait_until("eastwood")
            self.play(*during(disappear(name, cl, cr, ll, lr), 0, 0.45),
                      *during(appear(q4, shift=None), 0.45, 1), run_time=1.4)  # early: the same query, his name
            self.play(*appear(el, er, shift=None, lag=0.2), FlashUnder(q4.find("'Clint Eastwood'")),
                      run_time=1.2)
            c.wait_until(own_word=dl)
            self.play(*appear(dl), run_time=0.8)
            c.wait_until("ten")
            self.play(*appear(al), run_time=0.8)
            c.wait_until("six")
            self.play(*appear(six, *etbl.lines, etbl.head, shift=None), run_time=0.8)  # early: overlap and header
            self.play(*appear(*etbl.rows, count6, shift=0.12 * DOWN, lag=0.15),  # early: the reply is printed whole
                      run_time=min(1.4, c.until("lesson")))
            c.wait_until("lesson")
            self.play(FlashAround(six, color=YELLOW, time_width=1.5), FlashAround(count6, color=GOLD, time_width=1.5),
                      run_time=1.5)
