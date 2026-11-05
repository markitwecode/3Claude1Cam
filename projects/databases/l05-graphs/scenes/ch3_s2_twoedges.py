"""Chapter 3, scene 2: Two actors, one movie. Clips c3.two.1 – c3.two.4.

Opens on ch3 s1's handover (the dimmed SQL diagram), which turns into the co-star V; the comma
form of the pattern, the merge of the two m's, the <> condition, the run on The Kid, the fold into
one line. Ends on ch3 s3's open_shot() (one-line query + result table).
"""
# style: 2
# handover: next
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch3_s1_hook")
S3 = load_scene("ch3_s3_twins")

R2 = 0.65                 # node radius once the drawing sits at the top
NS = 40 * R2 / 0.8        # node label size there (the big V's 40, scaled)
P_Y, M_Y, PX = 2.7, 0.8, 4.8
SPLIT_MX = 1.6
CODE_SIZE = 32
ROW_Y = (-0.8, -1.45, -2.1, -2.75)
L1_SRC = "MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie),"
L2_SRC = "(p2:Person) -[:ACTED_IN]-> (m:Movie)"
L2B_SRC = "(m:Movie) <-[:ACTED_IN]- (p2:Person)"
PREFIX = "MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie)"
SUFFIX = "<-[:ACTED_IN]- (p2:Person)"
Q_LOW = 4.2               # how far below its final place the one-line query first lands
FOLD_P_Y, FOLD_M_Y = 2.35, 0.45
RING_SHIFT = 0.3 * UP
CUR_ROW_Y = -3.35


def handover_shot():
    """Last frame = ch3 s3's first frame."""
    return S3.open_shot()


def code_line(src, left_x, y):
    """A Code line placed with its first 'p' glyph centred at height y, left edge at left_x."""
    c = Code(src, size=CODE_SIZE)
    c.move_to(ORIGIN)
    c.shift((left_x - c.get_left()[0]) * RIGHT)
    c.shift((y - c.find("p")[0].get_center()[1]) * UP)
    return c


def comma_code():
    l1 = Code(L1_SRC, size=CODE_SIZE).move_to(ORIGIN)
    l1.shift((ROW_Y[0] - l1.find("p")[0].get_center()[1]) * UP)
    indent = l1.find("(p1")[0].get_left()[0]
    l2 = code_line(L2_SRC, indent, ROW_Y[1])
    l3 = code_line(S3.WHERE_NEQ, l1.get_left()[0], ROW_Y[2])
    l3.find("<>").set_color(YELLOW)
    l4 = code_line(S3.RETURN_LINE, l1.get_left()[0], ROW_Y[3])
    return l1, l2, l3, l4


def node(text, color, at, r=R2, size=NS):
    return S3.vnode(text, color, at, r, size)


def top_v(p1x=-PX, mx=0.0, p2x=PX, py=P_Y, my=M_Y):
    return S3.costar_v([p1x, py, 0], [mx, my, 0], [p2x, py, 0], r=R2, size=NS)


class TwoEdges(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.wait(1.0)       # handover: hold s3's first frame

    # ------------------------------------------------------------ the picture, two patterns
    def clip1(self):
        d = S1.handover_shot()
        self.add(d)
        v = S3.big_v()
        with self.say("c3.two.1") as c:
            def lift(*parts):
                """Copies of the dimmed shapes (which then morph); the originals go blank so the
                first frame shows each shape once."""
                g = VGroup(*[p.copy() for p in parts])
                for p in parts:
                    p.set_stroke(opacity=0).set_fill(opacity=0)
                return g
            srcs = [lift(d.p1.hrect, d.p1.brect), lift(d.p2.hrect, d.p2.brect),
                    lift(d.h1.hrect, d.h1.brect), lift(d.h2.hrect, d.h2.brect), lift(d.links[1])]
            self.add(*srcs)
            self.bring_to_front(d)
            self.play(*during(FadeOut(d), 0, 0.5),
                      ReplacementTransform(srcs[0], v.left.circ),
                      ReplacementTransform(srcs[1], v.right.circ),
                      ReplacementTransform(srcs[2], v.arrows[0]),
                      ReplacementTransform(srcs[3], v.arrows[1]),
                      ReplacementTransform(srcs[4], v.m.circ),
                      *during(appear(v.left.lab, v.m.lab, v.right.lab, shift=None, lag=0.1), 0.6, 1),
                      run_time=2.0)  # early: the drawing's variable names
            self.add(v.left, v.right, v.m, *v.arrows)
            c.wait_until("acted-in")
            self.play(*appear(*v.tags, lag=0.3), run_time=1.0)  # early: named by "acted-in arrow"

            # the drawing moves to the top and splits into two one-edge drawings
            c.wait_until("comma")
            p1n, p2n, m1 = v.left, v.right, v.m
            m2 = m1.copy()
            self.add(m2)
            k = R2 / 0.8
            tp1, tp2 = node("p1", PINK, [-PX, P_Y, 0]), node("p2", PINK, [PX, P_Y, 0])
            tm1, tm2 = node("m", BLUE, [-SPLIT_MX, M_Y, 0]), node("m", BLUE, [SPLIT_MX, M_Y, 0])
            na1, nt1 = S3.into(tp1, tm1)
            na2, nt2 = S3.into(tp2, tm2)
            a1, a2 = v.arrows
            t1, t2 = v.tags
            l1, l2, l3, l4 = comma_code()
            self.play(p1n.animate.scale(k).move_to(tp1), p2n.animate.scale(k).move_to(tp2),  # early: the tags only move
                      m1.animate.scale(k).move_to(tm1), m2.animate.scale(k).move_to(tm2),
                      Transform(a1, na1), Transform(a2, na2),
                      *during(disappear(t1, t2), 0, 0.3), *during(appear(nt1, nt2, shift=None), 0.7, 1),
                      run_time=min(2.0, 0.5 * c.until("first says")))
            t1, t2 = nt1, nt2
            self.play(*appear(l1, l2, lag=0.4), run_time=1.2)  # early: the two patterns shown whole
            comma = l1.find(",")
            self.play(*flash([comma], color=YELLOW, run_time=1.2, time_width=1.5))

            left, right = [p1n, a1, t1, m1], [p2n, a2, t2, m2]
            c.wait_until("p1")
            box = token_box(l1.find("(p1:Person) -[:ACTED_IN]-> (m:Movie)"), l1)
            self.play(FadeIn(box), *flash([p1n.circ, m1.circ], color=YELLOW, time_width=1.5),
                      VShowPassingFlash(a1.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=1.2)
            c.wait_until("p2")
            self.play(Transform(box, token_box(l2.find(L2_SRC), l2)),
                      *flash([p2n.circ, m2.circ], color=YELLOW, time_width=1.5),
                      VShowPassingFlash(a2.copy().set_stroke(YELLOW, 7), time_width=0.6), run_time=1.2)
        self.v1 = dict(p1n=p1n, p2n=p2n, m1=m1, m2=m2, a1=a1, a2=a2, t1=t1, t2=t2, left=left)
        self.code = (l1, l2, l3, l4)
        self.box = box

        # ------------------------------------------------------------ same name, same vertex
    def clip2(self):
        g = self.v1
        l1, l2, l3, l4 = self.code
        with self.say("c3.two.2") as c:
            self.play(FadeOut(self.box), run_time=0.8)
            ms = [l1.find("m:Movie")[0], l2.find("m:Movie")[0]]
            self.play(*recolor(ms, YELLOW), *flash(ms, color=YELLOW, time_width=1.5),
                      *flash([g["m1"].circ, g["m2"].circ], color=YELLOW, time_width=1.5), run_time=1.4)

            c.wait_until("merge")
            tv = top_v()
            self.play(g["m1"].animate.move_to(tv.m), g["m2"].animate.move_to(tv.m),
                      Transform(g["a1"], tv.arrows[0]), Transform(g["a2"], tv.arrows[1]),
                      *during(disappear(g["t1"], g["t2"]), 0, 0.3),
                      *during(appear(*tv.tags, shift=None), 0.7, 1),
                      run_time=2.0)
            self.remove(g["m2"])

            c.wait_until("diff")
            self.play(*flash([g["p1n"].circ, g["p2n"].circ], color=PINK, time_width=1.5), run_time=1.4)
            q = T("?", size=48, color=DIM).move_to([0, P_Y, 0])
            c.wait_until("promise nothing")
            self.play(*appear(q), run_time=1.0)

            c.wait_until("where")
            neq = MathTex(r"\neq", color=YELLOW, font_size=64).move_to(q)
            self.play(*appear(l3), run_time=1.2)
            c.wait_until("not equal")
            self.play(*swap(q, neq), *flash([l3.find("<>")], color=YELLOW, time_width=1.5), run_time=1.4)
        self.neq = neq

    # ------------------------------------------------------------ the run on The Kid
    def clip3(self):
        l1, l2, l3, l4 = self.code
        ring = S3.kid_ring().shift(RING_SHIFT)
        K = ring.movie.get_center()

        def inward(i, dist=0.72):
            p = ring.people[i].get_center()
            u = (p - K) / np.linalg.norm(p - K)
            return p - dist * u

        def hole(i):
            return Circle(radius=0.45).set_stroke(YELLOW, 5).set_fill(opacity=0).move_to(ring.people[i])

        def cell(name):
            return S3.table_row(("Charles Chaplin", name, "The Kid"), CUR_ROW_Y)[1]

        with self.say("c3.two.3") as c:
            self.play(*appear(l4), run_time=1.0)

            c.wait_until("kid")
            sweep_clear(self, *appear(ring, shift=None), run_time=1.6)  # early: the cast shown whole

            m_ring = Circle(radius=0.98).set_stroke(YELLOW, 5).set_fill(opacity=0).move_to(K)
            m_tag = set_backstroke(Mono("m", 30, YELLOW)).move_to(K + np.array([0.95, 1.2, 0]))
            h1, h2 = hole(0), hole(1)
            p1_tag = set_backstroke(Mono("p1", 30, YELLOW)).move_to(inward(0))
            p2_tag = set_backstroke(Mono("p2", 30, YELLOW)).move_to(inward(1))
            c.wait_until("charles chaplin")
            self.play(GrowFromCenter(m_ring), GrowFromCenter(h1), *appear(m_tag, p1_tag, shift=None),
                      ring.edges[0].animate.set_color(YELLOW), run_time=1.2)
            c.wait_until("jackie coogan")
            self.play(GrowFromCenter(h2), *appear(p2_tag, shift=None),
                      ring.edges[1].animate.set_color(YELLOW), run_time=1.0)
            row = S3.table_row(("Charles Chaplin", "Jackie Coogan", "The Kid"), CUR_ROW_Y)
            self.play(*appear(row), run_time=1.0)

            # first hop slow
            c.wait_until("hop")
            cur = row[1]
            nxt = cell(S3.KID_CAST[2])
            self.play(Transform(h2, hole(2)), p2_tag.animate.move_to(inward(2)),
                      ring.edges[1].animate.set_color(DIM), ring.edges[2].animate.set_color(YELLOW),
                      *swap(cur, nxt, shift=None), run_time=1.2)
            self.wait(0.4)

            # the rest quick: one updater per moving thing, hops 2 -> 3 ... 8 -> 9
            idx = list(range(2, 10))
            n = len(idx) - 1
            cells = {2: nxt}
            for i in idx[1:]:
                cells[i] = cell(S3.KID_CAST[i]).set_opacity(0)
                self.add(cells[i])
            pts_h = [ring.people[i].get_center() for i in idx]
            pts_t = [inward(i) for i in idx]

            def phase(a):
                s = min(a * n, n - 1e-6)
                j = int(s)
                return j, s - j

            def mover(pts):
                def f(mob, a):
                    j, fr = phase(a)
                    t = smooth(min(fr / 0.6, 1.0))
                    mob.move_to(pts[j] + t * (pts[j + 1] - pts[j]))
                    if a >= 1:
                        mob.move_to(pts[-1])
                return f

            def edge_f(i):
                def f(mob, a):
                    j, fr = phase(a)
                    on = idx[j + 1] if fr > 0.3 else idx[j]
                    if a >= 1:
                        on = idx[-1]
                    mob.set_color(YELLOW if on == i else DIM)
                return f

            def cell_f(i):
                pos = idx.index(i)

                def f(mob, a):
                    j, fr = phase(a)
                    if a >= 1:
                        op = 1.0 if pos == n else 0.0
                    elif pos == j:            # leaving
                        op = 1 - smooth(min(fr / 0.3, 1.0))
                    elif pos == j + 1:        # arriving
                        op = smooth(min(max((fr - 0.35) / 0.3, 0.0), 1.0))
                    else:
                        op = 0.0
                    mob.set_opacity(op)
                return f

            hop_rt = max(1.5, c.until("rows") - 0.2)
            self.play(UpdateFromAlphaFunc(h2, mover(pts_h)), UpdateFromAlphaFunc(p2_tag, mover(pts_t)),
                      *[UpdateFromAlphaFunc(ring.edges[i], edge_f(i)) for i in idx],
                      *[UpdateFromAlphaFunc(cells[i], cell_f(i)) for i in idx],
                      run_time=hop_rt, rate_func=linear)
            for i in idx[:-1]:
                self.remove(cells[i])

            # every placement is one more row: the table
            c.wait_until("rows")
            tb = S3.result_table(S3.ROWS_NEQ, S3.FOOTER_NEQ)
            sweep_clear(self, *appear(tb.header, tb.rule, *tb.seps, *tb.rows, shift=None, lag=0.08),
                        run_time=2.2)
            c.wait_until(own_word=tb.footer, cue="quarter")
            self.play(*appear(tb.footer), run_time=1.0)
        self.tb3 = tb

    # ------------------------------------------------------------ the fold into one line
    def clip4(self):
        shot = S3.open_shot()
        q, tb = shot.query, shot.table
        q.shift(Q_LOW * DOWN)
        v = top_v()
        l1, l2, l3, l4 = comma_code()
        with self.say("c3.two.4") as c:
            c.wait_until("look at")
            sweep_clear(self, *appear(v, l1, l2, l3, l4, shift=None, lag=0.15), run_time=1.8)  # early: back to the code
            c.wait_until("written out")
            movies = [l1.find("(m:Movie)"), l2.find("(m:Movie)")]
            self.play(*flash(movies, color=YELLOW, time_width=1.5), *flash([v.m.circ], color=BLUE),
                      run_time=1.4)

            c.wait_until("rewrite")
            l2b = code_line(L2B_SRC, l2.get_left()[0], ROW_Y[1])
            self.play(*edit(l2, l2b), run_time=min(2.0, c.until("left")))

            c.wait_until("left")
            self.play(*flash([l2b.find("<-[:ACTED_IN]-")], color=YELLOW, time_width=1.5),
                      VShowPassingFlash(v.arrows[1].copy().set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=1.5)
            c.wait_until("from pee two")
            self.play(VShowPassingFlash(v.arrows[1].copy().set_stroke(YELLOW, 7), time_width=0.6),
                      *flash([v.right.circ, v.m.circ], color=YELLOW, time_width=1.5), run_time=1.5)

            # hang it onto the end of line 1: every glyph to its place in the one-line query
            c.wait_until("attach")
            assert len(l1.find(PREFIX)) == len(q.find(PREFIX, line=0))
            assert len(l3.line(0)) == len(q.line(1)) and len(l4.line(0)) == len(q.line(2))
            suffix = list(zip(l2b.find(SUFFIX), q.find(SUFFIX, line=0)))
            head = list(zip(l1.find(PREFIX), q.find(PREFIX, line=0)))
            tail = list(zip(l3.line(0), q.line(1))) + list(zip(l4.line(0), q.line(2)))
            dy = l2b.find(SUFFIX).get_center()[1] - q.find(SUFFIX, line=0).get_center()[1]
            for g, t in suffix:
                g.target = t.copy().shift(dy * UP)
            drop = [*l1.find(","), *l2b.find("(m:Movie)")]
            # 1: the comma and the second (m:Movie) fade, the edge slides right along its row
            self.play(*during([FadeOut(g) for g in drop], 0, 0.4),
                      *during([MoveToTarget(g) for g, _ in suffix], 0.2, 1), run_time=1.0)
            for g, t in suffix + head + tail:
                g.target = t.copy()
            xs = [q.find(s, line=0).get_center()[0] for s in ("(p1:Person)", "(m:Movie)", "(p2:Person)")]
            fv = top_v(xs[0], xs[1], xs[2], FOLD_P_Y, FOLD_M_Y)
            # 2: everything settles into the one-line query; the edge rises onto line 1
            self.play(*during([MoveToTarget(g) for g, _ in head], 0, 0.6),
                      *during([MoveToTarget(g) for g, _ in suffix], 0.55, 1),
                      *during([MoveToTarget(g) for g, _ in tail], 0.65, 1),
                      Transform(v, fv), run_time=1.6)
            self.remove(*l1.get_family(), *l2b.get_family(), *l2.get_family(),
                        *l3.get_family(), *l4.get_family())
            self.add(q)

            # a person, an arrow, a movie, an arrow, a person
            pieces = [q.find(s, line=0) for s in
                      ("(p1:Person)", "-[:ACTED_IN]->", "(m:Movie)", "<-[:ACTED_IN]-", "(p2:Person)")]
            parts = [v.left.circ, v.arrows[0], v.m.circ, v.arrows[1], v.right.circ]
            cues = [("a person", 0), ("an arrow", 0), ("a movie", 0), ("an arrow", 1), ("a person", 1)]
            box = None
            for k, (piece, part, (cue, nth)) in enumerate(zip(pieces, parts, cues)):
                c.wait_until(cue, nth=nth)
                lit = (VShowPassingFlash(part.copy().set_stroke(YELLOW, 7), time_width=0.6)
                       if k in (1, 3) else FlashAround(part, color=YELLOW, time_width=1.5))
                nb = token_box(piece, q.line(0))
                if box is None:
                    box = nb
                    self.play(FadeIn(box), lit, run_time=0.9)
                else:
                    self.play(Transform(box, nb), lit, run_time=0.9)

            # same rows: the query rises, the table returns
            c.wait_until("same2")
            self.play(*during([FadeOut(box), FadeOut(v)], 0, 0.4),
                      *during([q.animate.shift(Q_LOW * UP)], 0.25, 0.8),
                      *during(appear(*tb.submobjects, shift=None, lag=0.03), 0.8, 1),
                      run_time=2.4)
            c.wait_until("one person")
            self.play(*flash([q.find("(p1:Person)", line=0), q.find("(p2:Person)", line=0)],
                             color=PINK, time_width=1.5), run_time=1.4)
            self.play(*flash([q.find("(m:Movie)", line=0)], color=BLUE, time_width=1.5), run_time=1.2)
