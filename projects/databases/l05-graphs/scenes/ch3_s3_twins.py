"""Chapter 3, scene 3: Every pair twice. Clips c3.twins.1 – c3.twins.5.

Exports (shared with s2 / s4):
  open_shot()      this scene's first frame (s2 ends on it): one-line query + s2's result table.
  kid_ring()       The Kid and its ten actors (s2's run, s4 enlarges it).
  handover_shot()  = kid_ring(): this scene's last frame (s4 opens on it).
  costar_v(...)    the co-star V look: PINK person circles with the variable inside, BLUE movie
                   circle, ACTED_IN along each arrow, both arrows into m.
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
from lib.style import *  # noqa: E402,F403

MATCH_LINE = "MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]- (p2:Person)"
RETURN_LINE = "RETURN p1.name, p2.name, m.title"
WHERE_NEQ = "WHERE p1.person_id <> p2.person_id"
WHERE_LT = "WHERE p1.person_id < p2.person_id"

KID_CAST = ["Charles Chaplin", "Jackie Coogan", "Albert Austin", "Nellie Bly Baker", "Edward Biby",
            "Edna Purviance", "Carl Miller", "Beulah Bains", "Henry Bergman", "B.F. Blinn"]
ROWS_NEQ = [("Charles Chaplin", n, "The Kid") for n in KID_CAST[1:]] + \
           [("Jackie Coogan", "Charles Chaplin", "The Kid")]
ROWS_LT = ROWS_NEQ[:9] + [("Jackie Coogan", "Albert Austin", "The Kid")]
FOOTER_NEQ = "261476 rows (showing the first 40)"
FOOTER_LT = "130738 rows (showing the first 40)"
ID_CHAPLIN, ID_COOGAN = "nm0000122", "nm0001067"

TABLE_SIZE = 28
COL_X = (-5.22, -0.81, 3.60)      # left edges of the three columns
ROW_TOP = 1.40                    # y of row 1
ROW_PITCH = 0.44


# ---------------------------------------------------------------- shared look
def vnode(text, color, at, r, size=34):
    """A circle (PINK person / BLUE movie) with `text` (Mono) inside. .circ .lab"""
    circ = Circle(radius=r, color=color, stroke_width=4).set_fill(color, 0.12).move_to(at)
    lab = Mono(text, size=size).move_to(circ)
    v = VGroup(circ, lab)
    v.circ, v.lab = circ, lab
    return v


def into(a, b, size=28, color=FG, outer=False):
    """ACTED_IN arrow from node a into node b, its type along it (above the line, or below it
    with outer=True). -> (arrow, tag)"""
    s, e = a.circ.get_center(), b.circ.get_center()
    d = (e - s) / np.linalg.norm(e - s)
    ra, rb = a.circ.width / 2, b.circ.width / 2
    arr = Arrow(s + d * (ra + 0.04), e - d * (rb + 0.04), buff=0, stroke_width=4, color=color,
                max_tip_length_to_length_ratio=0.3, tip_length=0.24)
    ang = np.arctan2(d[1], d[0])
    if ang > PI / 2:
        ang -= PI
    if ang < -PI / 2:
        ang += PI
    nrm = np.array([-d[1], d[0], 0])
    if (nrm[1] < 0) != outer:
        nrm = -nrm
    tag = set_backstroke(T("ACTED_IN", size=size).rotate(ang))
    tag.move_to(arr.get_center() + 0.3 * nrm)
    return arr, tag


def costar_v(left_at, m_at, right_at, r=0.8, m_r=None, left="p1", right="p2", size=40, tag_size=28,
             outer=False):
    """The co-star V: PINK left/right person circles with their variable inside, BLUE m, both
    arrows into m. Parts: .left .right .m (each .circ .lab), .arrows [left, right], .tags."""
    lv = vnode(left, PINK, left_at, r, size)
    rv = vnode(right, PINK, right_at, r, size)
    mv = vnode("m", BLUE, m_at, m_r or r, size)
    a1, t1 = into(lv, mv, tag_size, outer=outer)
    a2, t2 = into(rv, mv, tag_size, outer=outer)
    g = VGroup(a1, a2, lv, rv, mv, t1, t2)
    g.left, g.right, g.m, g.arrows, g.tags = lv, rv, mv, [a1, a2], [t1, t2]
    return g


def big_v():
    """The V big in the centre: p1 (-3.4, 1.6), p2 (3.4, 1.6), m (0, -1.4), radius 0.8."""
    return costar_v([-3.4, 1.6, 0], [0, -1.4, 0], [3.4, 1.6, 0])


# ---------------------------------------------------------------- the table
def table_row(cells, y):
    row = VGroup(*[Mono(c, size=TABLE_SIZE) for c in cells])
    for t, x in zip(row, COL_X):
        t.move_to([x + t.width / 2, y, 0])
    return row


def result_table(rows, footer=None):
    """cypher-shell's table: header, rule, column rules, rows (ten), GOLD footer.
    Parts .header .rule .seps .rows[i] .footer (None if no footer)."""
    header = table_row(("p1.name", "p2.name", "m.title"), ROW_TOP + 0.58)
    header.set_color(DIM)
    rule = Line([-5.4, ROW_TOP + 0.30, 0], [5.4, ROW_TOP + 0.30, 0], color=DIM, stroke_width=2)
    body = [table_row(r, ROW_TOP - i * ROW_PITCH) for i, r in enumerate(rows)]
    bottom = ROW_TOP - (len(rows) - 1) * ROW_PITCH - 0.25
    seps = [Line([x - 0.33, ROW_TOP + 0.80, 0], [x - 0.33, bottom, 0], color=DIM, stroke_width=2)
            for x in COL_X[1:]]
    g = VGroup(header, rule, *seps, *body)
    footer_mob = None
    if footer:
        footer_mob = Mono(footer, size=TABLE_SIZE, color=GOLD)
        footer_mob.move_to([COL_X[0] + footer_mob.width / 2, ROW_TOP - 10 * ROW_PITCH - 0.24, 0])
        g.add(footer_mob)
    g.header, g.rule, g.seps, g.rows, g.footer = header, rule, seps, body, footer_mob
    return g


def query_code(where):
    code = Code("\n".join([MATCH_LINE, where, RETURN_LINE]), size=28)
    code.scale_to_fit_width(13.0)
    code.move_to([0, 3.6 - code.height / 2, 0])
    op = "<>" if "<>" in where else "<"
    code.find(op, line=1).set_color(YELLOW)
    return code


def open_shot():
    """Scene 3's first frame (s2 ends on it). Query at the top (13.0 wide, top at y 3.6, `<>`
    YELLOW), table below (header y 1.98, rows 1–10 at y 1.40 … -2.56, footer y -3.24).
    Parts: .query, .query_lines[i] (glyphs of line i), .table, .header, .rows[i], .footer."""
    q = query_code(WHERE_NEQ)
    tb = result_table(ROWS_NEQ, FOOTER_NEQ)
    g = VGroup(q, tb)
    g.query, g.query_lines = q, [q.line(i) for i in range(3)]
    g.table, g.header, g.rows, g.footer = tb, tb.header, tb.rows, tb.footer
    return g


# ---------------------------------------------------------------- The Kid's ring
RING_RX, RING_RY = 3.0, 2.45


def kid_ring():
    """The Kid (BLUE, r 0.8, at ORIGIN) with its ten actors on an ellipse (3.0 × 2.45): PINK
    circles r 0.3, Chaplin at 180°, then clockwise every 36° in KID_CAST order (Coogan 144°,
    Austin 108°, …, Blinn -144°), each name (T 30) just outside its circle, a DIM arrow from
    each actor into The Kid. Parts .movie (.circ .lab), .people[i], .names[i], .edges[i]."""
    circ = Circle(radius=0.8, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12)
    movie = VGroup(circ, T("The Kid", size=30).move_to(circ))
    movie.circ, movie.lab = circ, movie[1]
    people, names, edges = [], [], []
    for i, name in enumerate(KID_CAST):
        th = PI - i * TAU / 10
        u = np.array([np.cos(th), np.sin(th), 0])
        p = Circle(radius=0.3, color=PINK, stroke_width=4).set_fill(PINK, 0.12)
        p.move_to([RING_RX * u[0], RING_RY * u[1], 0])
        lab = T(name, size=30).next_to(p, u, buff=0.14)
        d = -p.get_center() / np.linalg.norm(p.get_center())
        e = Arrow(p.get_center() + d * 0.34, -d * 0.84, buff=0, stroke_width=2.5, color=DIM,
                  max_tip_length_to_length_ratio=0.2, tip_length=0.18)
        people.append(p)
        names.append(lab)
        edges.append(e)
    g = VGroup(*edges, movie, *people, *names)
    g.movie, g.people, g.names, g.edges = movie, people, names, edges
    return g


def handover_shot():
    """Last frame (s4 opens on it): The Kid's ring alone."""
    return kid_ring()


# ---------------------------------------------------------------- this scene's pieces
def placement(cx, left, right):
    """A small V placed on The Kid: Coogan's circle left, Chaplin's right, `left`/`right` the
    variables on them. .v (costar_v), .names [Coogan, Chaplin], .title, .ids (built, not shown)."""
    v = costar_v([cx - 2.2, 1.7, 0], [cx, -0.5, 0], [cx + 2.2, 1.7, 0], r=0.5, m_r=0.55, size=30,
                 left=left, right=right, outer=True)
    names = [T("Coogan", size=30).next_to(v.left.circ, UP, buff=0.18),
             T("Chaplin", size=30).next_to(v.right.circ, UP, buff=0.18)]
    title = T("The Kid", size=30).next_to(v.m.circ, DOWN, buff=0.18)
    ids = [Mono(ID_COOGAN, size=28, color=GOLD).next_to(names[0], UP, buff=0.16),
           Mono(ID_CHAPLIN, size=28, color=GOLD).next_to(names[1], UP, buff=0.16)]
    g = VGroup(v, *names, title)
    g.v, g.names, g.title, g.ids, g.cx = v, names, title, ids, cx
    return g


def tick_list(at):
    items = []
    for w in ("Person", "ACTED_IN", "into m"):
        tk = check_mark(GREEN).scale(0.6)
        items.append(VGroup(tk, T(w, size=28)).arrange(RIGHT, buff=0.12))
    g = VGroup(*items).arrange(RIGHT, buff=0.24)
    return g.move_to(at)


def row_box(row):
    return Rectangle(width=row.width + 0.34, height=0.46, stroke_color=YELLOW, stroke_width=2.5,
                     fill_color=YELLOW, fill_opacity=0.15).move_to(row).set_z_index(-1)


def compare(a, b, cx, y=-2.85):
    code = Code(f"'{a}' < '{b}'", size=28)
    code.find("<").set_color(YELLOW)
    return code.move_to([cx, y, 0])


class Twins(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.wait(0.6)       # handover: hold The Kid's ring (scene 4 opens on it)

    # ------------------------------------------------------------ why twice?
    def clip1(self):
        shot = open_shot()
        self.q, self.tb = shot.query, shot.table
        self.add(self.q, *self.tb.submobjects)
        rows = self.tb.rows
        with self.say("c3.twins.1") as c:
            self.play(*set_alpha([self.q], 0.4), run_time=1.0)
            c.wait_until("r1")
            self.box1 = row_box(rows[0])
            self.play(FadeIn(self.box1), *recolor(rows[0], YELLOW), run_time=1.0)
            c.wait_until("r10")
            self.box10 = row_box(rows[9])
            self.play(FadeIn(self.box10), *recolor(rows[9], YELLOW), run_time=1.0)
            c.wait_until("why")
            p1 = self.box1.get_right() + 0.12 * RIGHT
            p2 = self.box10.get_right() + 0.12 * RIGHT
            self.arc = ArcBetweenPoints(p1, p2, angle=-PI / 3, color=YELLOW, stroke_width=3)
            self.qmark = T("?", size=56, color=YELLOW).next_to(self.arc, RIGHT, buff=0.15)
            self.play(Create(self.arc), *appear(self.qmark, shift=None), run_time=1.2)

    # ------------------------------------------------------------ the mirror
    def clip2(self):
        tb, rows = self.tb, self.tb.rows
        with self.say("c3.twins.2") as c:
            # the rest of the table goes; the twin rows drop to the bottom of the frame
            leaving = [self.q, tb.header, tb.rule, *tb.seps, *rows[1:9], tb.footer, self.arc, self.qmark]
            d1 = np.array([0, -2.9 - rows[0].get_y(), 0])
            d10 = np.array([0, -3.45 - rows[9].get_y(), 0])
            moves = [rows[0].animate.shift(d1), self.box1.animate.shift(d1),
                     rows[9].animate.shift(d10), self.box10.animate.shift(d10)]
            self.play(*during(disappear(*leaving), 0, 0.4), *during(moves, 0.35, 1), run_time=1.5)
            v = big_v()
            self.play(*appear(*v.submobjects, shift=None, lag=0), run_time=1.0)
            c.wait_until("each with an arrow")
            self.play(*[VShowPassingFlash(a.copy().set_color(YELLOW).set_stroke(width=8), time_width=0.6)
                        for a in v.arrows], run_time=1.5)

            c.wait_until("flip")
            mirror = DashedLine([0, 2.7, 0], [0, -2.5, 0], dash_length=0.14, color=DIM, stroke_width=3)
            self.play(FadeIn(mirror), *disappear(*v.tags), run_time=0.8)
            shapes = [v.left.circ, v.right.circ, v.m.circ, *v.arrows]
            self.play(*[Rotate(s, PI, axis=UP, about_point=ORIGIN) for s in shapes],
                      v.left.lab.animate(path_arc=-PI / 2).move_to(v.right.circ),
                      v.right.lab.animate(path_arc=-PI / 2).move_to(v.left.circ),
                      run_time=2.6)
            self.play(*appear(*v.tags, shift=None), run_time=0.6)
            # now: left circle carries p2, right circle p1 (v.right / v.left trade sides)

            c.wait_until("swap")
            A = placement(-3.35, "p2", "p1")        # p1 on Chaplin, p2 on Coogan
            moves = [ReplacementTransform(v.right.circ, A.v.left.circ),
                     v.right.lab.animate.scale(30 / 40).move_to(A.v.left.lab),
                     ReplacementTransform(v.left.circ, A.v.right.circ),
                     v.left.lab.animate.scale(30 / 40).move_to(A.v.right.lab),
                     ReplacementTransform(v.m.circ, A.v.m.circ),
                     v.m.lab.animate.scale(30 / 40).move_to(A.v.m.lab),
                     ReplacementTransform(v.arrows[1], A.v.arrows[0]),
                     ReplacementTransform(v.arrows[0], A.v.arrows[1])]
            self.play(*disappear(*v.tags, mirror), run_time=0.6)
            self.play(*moves, run_time=1.6)
            self.remove(v.right.lab, v.left.lab, v.m.lab)
            self.add(A.v.left.lab, A.v.right.lab, A.v.m.lab)
            self.play(*appear(*A.v.tags, *A.names, A.title, lag=0.15), run_time=1.2)  # early: the placement's names come with it
            B = placement(3.35, "p1", "p2")         # p1 on Coogan, p2 on Chaplin
            self.play(*appear(B, shift=None), run_time=1.2)  # early: the mirrored placement, shown whole
            self.A, self.B = A, B
            c.wait_until("obeys every rule")
            self.lists = [tick_list([A.cx, -1.9, 0]), tick_list([B.cx, -1.9, 0])]
            self.play(*appear(*self.lists, lag=0.4), run_time=1.5)

            c.wait_until("both")
            self.ptrA = Arrow([-5.9, -2.1, 0], [-5.45, rows[0].get_top()[1] + 0.06, 0], buff=0,
                              color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.12)
            self.ptrB = Arrow([6.15, -2.1, 0], [self.box10.get_right()[0] + 0.05, rows[9].get_y(), 0],
                              buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.12)
            self.play(GrowArrow(self.ptrA), run_time=1.0)
            self.play(GrowArrow(self.ptrB), run_time=1.0)

    # ------------------------------------------------------------ every pair, every movie
    def clip3(self):
        A, B, rows = self.A, self.B, self.tb.rows
        with self.say("c3.twins.3") as c:
            self.play(*disappear(*self.lists, self.ptrA, self.ptrB, rows[0], rows[9],
                                 self.box1, self.box10), run_time=1.0)
            hp = [("Daniel Radcliffe", "Emma Watson"), ("Emma Watson", "Daniel Radcliffe")]
            title = "Harry Potter and the Sorcerer's Stone"
            hp_rows = []
            for i, (a, b) in enumerate(hp):
                r = VGroup(T(a, size=28), T(b, size=28), T(title, size=28))
                for t, x in zip(r, (-6.45, -3.4, -0.35)):
                    t.move_to([x + t.width / 2, -1.9 - 0.5 * i, 0])
                hp_rows.append(r)
            c.wait_until(own_word=hp_rows[0][0])
            self.play(*appear(*hp_rows, lag=0.5), run_time=1.5)  # early: cypher-shell rows, shown whole
            c.wait_until("on each harry potter film")
            films = []
            for i in range(8):
                f = Circle(radius=0.24, color=BLUE, stroke_width=4).set_fill(BLUE, 0.12)
                x2 = T("×2", size=30, color=GOLD).next_to(f, RIGHT, buff=0.1)
                films.append(VGroup(f, x2).move_to([-5.1 + 1.46 * i, -3.1, 0]))
            self.play(*appear(*films, lag=0.15), run_time=1.6)

            c.wait_until("double")
            self.play(*disappear(*films), run_time=0.8)
            num = Mono("261476", size=48, color=GOLD).move_to([0, -3.1, 0])
            self.play(*appear(num), run_time=1.0)
            c.wait_until("exactly twice")
            full = VGroup(num.copy(), Mono("= 2 × 130738", size=48, color=GOLD)).arrange(RIGHT, buff=0.3)
            full.move_to([0, -3.1, 0])
            rest = full[1]
            self.play(*during([num.animate.move_to(full[0])], 0, 0.5),
                      *during(appear(rest, shift=None), 0.5, 1), run_time=1.6)
            self.count = VGroup(num, rest)

            c.wait_until("neq")
            self.where = Code(WHERE_NEQ, size=36).move_to([0, -1.95, 0])
            self.where.find("<>").set_color(YELLOW)
            self.play(*disappear(*hp_rows), run_time=0.8)
            self.play(*appear(self.where), run_time=1.0)
            c.wait_until("in both twins")
            self.ticks = [check_mark(GREEN).move_to([P.cx + 1.05, -0.95, 0]) for P in (A, B)]
            self.play(FadeIn(self.ticks[0], scale=1.3), run_time=0.7)
            self.play(FadeIn(self.ticks[1], scale=1.3), run_time=0.7)
            c.wait_until("only")
            self.note = VGroup(Mono("<>", size=30, color=DIM), T("only rules out", size=30, color=DIM),
                               Mono("p1 = p2", size=30, color=DIM)).arrange(RIGHT, buff=0.18)
            self.note.move_to([0, -2.9, 0])
            self.play(*swap(self.count, self.note), run_time=1.2)

    # ------------------------------------------------------------ the fix
    def clip4(self):
        A, B = self.A, self.B
        with self.say("c3.twins.4") as c:
            self.play(FlashAround(self.where.find("<>"), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("replace")
            self.play(*disappear(self.note, *self.ticks), run_time=0.8)
            where_lt = Code(WHERE_LT, size=36)
            where_lt.find("<").set_color(YELLOW)
            where_lt.move_to(self.where, aligned_edge=LEFT)
            self.play(*edit(self.where, where_lt), run_time=1.5)
            self.where = where_lt

            c.wait_until("ids")
            self.play(*appear(*A.ids, *B.ids, lag=0.3), run_time=1.6)

            c.wait_until("pick")
            compA = compare(ID_CHAPLIN, ID_COOGAN, A.cx)
            tickA = check_mark(GREEN).move_to([A.cx + 1.05, -0.95, 0])
            self.play(*appear(compA, tickA, lag=0.4), run_time=1.3)
            compB = compare(ID_COOGAN, ID_CHAPLIN, B.cx)
            crossB = cross_mark(RED).move_to([B.cx + 1.05, -0.95, 0])
            self.play(*appear(compB, crossB, lag=0.4), run_time=1.3)
            self.play(*set_alpha([B, *B.ids, compB], DIMMED), run_time=0.9)

            c.wait_until("self")
            cx = B.cx
            me = Circle(radius=0.5, color=PINK, stroke_width=4).set_fill(PINK, 0.12).move_to([cx, 1.7, 0])
            labs = VGroup(Mono("p1", size=28), Mono("p2", size=28)).arrange(DOWN, buff=0.04).move_to(me)
            mm = vnode("m", BLUE, [cx, -0.5, 0], 0.55, 30)
            arr = Arrow(me.get_bottom() + 0.04 * DOWN, mm.circ.get_top() + 0.04 * UP, buff=0,
                        stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.4, tip_length=0.22)
            tag = T("ACTED_IN", size=28).next_to(arr, RIGHT, buff=0.15)
            nm = T("Chaplin", size=30).next_to(me, UP, buff=0.18)
            mid = Mono(ID_CHAPLIN, size=28, color=GOLD).next_to(nm, UP, buff=0.16)
            ttl = T("The Kid", size=30).next_to(mm.circ, DOWN, buff=0.18)
            mini = VGroup(arr, me, labs, mm, tag, nm, mid, ttl)
            self.play(*disappear(B, *B.ids, compB, crossB), run_time=0.8)
            self.play(*appear(mini, shift=None), run_time=1.2)
            compM = compare(ID_CHAPLIN, ID_CHAPLIN, cx)
            self.play(*appear(compM), run_time=1.0)
            c.wait_until("rules out")
            crossM = cross_mark(RED).move_to([cx + 1.05, -0.95, 0])
            note = T("nobody is less than themself", size=28, color=DIM).move_to([cx, -3.45, 0])
            self.play(FadeIn(crossM, scale=1.3), *appear(note), run_time=1.0)

    # ------------------------------------------------------------ once per movie
    def clip5(self):
        with self.say("c3.twins.5") as c:
            q = query_code(WHERE_LT)
            tb = result_table(ROWS_NEQ)
            sweep_clear(self, *during(appear(q, tb, lag=0.3), 0.5, 1), run_time=1.6)
            old = tb.rows[9]
            new = table_row(ROWS_LT[9], old.get_y())
            self.play(*set_alpha([old], DIMMED), run_time=0.6)
            self.play(*during([FadeOut(old, shift=2.5 * RIGHT)], 0, 0.5),
                      *during([FadeIn(new, shift=ROW_PITCH * UP)], 0.45, 1), run_time=1.5)
            self.remove(old)
            c.wait_until("result")
            footer = Mono(FOOTER_LT, size=TABLE_SIZE, color=GOLD)
            footer.move_to([COL_X[0] + footer.width / 2, ROW_TOP - 10 * ROW_PITCH - 0.24, 0])
            self.play(*appear(footer), run_time=1.0)
            c.wait_until("just picks one")
            ring = kid_ring()
            sweep_clear(self, *during(appear(ring, shift=None), 0.5, 1), run_time=1.6)
            self.play(*flash(ring.people[:2], color=YELLOW), run_time=1.5)
