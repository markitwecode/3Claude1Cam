"""Chapter 8, scene 4: when the document doesn't have it, join. Clips c8.join.1 – c8.join.4.

Exports (import with `J = load_scene("ch8_s4_join")`; all static, no updaters):

    J.bergman() -> VGroup, clip 1's last picture (no slot, no question):
        .actor  Henry Bergman's actor object, TEAL doc card (ch4 s3 doc_card, Code 22, strings FG),
                left edge x -6.6, top y 0.0
        .person his person document card (1868 GOLD, /* 3 movies */ DIM), left x -0.3, top y 3.5
        .arrow  FG ID-reference arrow (ch4 s5 two_way style) from the actor's "nm0074788"
                to the person card's left edge at its person_id line
        .pid .year (glyph VGroups)
    J.recap_thumb() -> bergman() scaled to 6.0 wide, centred at ORIGIN (~6.0 x 2.6), for s8's {r4}.
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

D = load_scene("ch4_s3_movie")
S5 = load_scene("ch4_s5_shape")
H = load_scene("ch5_s1_hook")
P = load_scene("ch7_s5_parens")

ACTOR_SRC = "\n".join(['{', '  "person_id": "nm0074788",', '  "name": "Henry Bergman",',
                       '  "roles": ["Professor Guido", "Night Shelter Keeper"]', '}'])
PERSON_SRC = "\n".join(['{', '  "person_id": "nm0074788",', '  "name": "Henry Bergman",',
                        '  "birthyear": 1868,', '  "deathyear": 1946,',
                        '  "acted_in": [ /* 3 movies */ ]', '}'])
QUERY = ("SELECT   a->>'name' AS name,\n"
         "         (movie->>'year')::INTEGER\n"
         "            - (person->>'birthyear')::INTEGER AS age\n"
         "FROM     movies, unnest(movie->'$.actors[*]') AS t(a),\n"
         "         people\n"
         "WHERE    person_id = (a->>'person_id')\n"
         "  AND    (movie->>'title') = 'The Kid'\n"
         "ORDER BY age DESC, name\n"
         "LIMIT    4;")
ROWS = [("Henry Bergman", 53), ("B.F. Blinn", 49), ("Albert Austin", 39), ("Edward Biby", 35),
        ("Charles Chaplin", 32), ("Nellie Bly Baker", 28), ("Carl Miller", 27),
        ("Edna Purviance", 26), ("Beulah Bains", 16), ("Jackie Coogan", 7)]
CS = 22          # card code size
QS = 28          # query code size


def _card(src, size=CS):
    card = D.doc_card(src, size=size)
    S5._plain(card.code)
    return card


def bergman():
    g = VGroup()
    a, p = _card(ACTOR_SRC), _card(PERSON_SRC)
    a.move_to(ORIGIN, aligned_edge=UL).shift([-6.6, 0.0, 0])
    p.move_to(ORIGIN, aligned_edge=UL).shift([-0.3, 3.5, 0])
    g.year = p.code.find("1868").set_color(GOLD)
    p.code.find("1946").set_color(FG)
    g.pid = a.code.find('"nm0074788"')
    p1 = np.array([g.pid.get_right()[0] + 0.05, g.pid.get_y(), 0])
    p2 = np.array([p.frame.get_left()[0], p.code.line(1).get_y(), 0])
    g.arrow = Arrow(p1, p2, buff=0.04, stroke_width=3, color=FG, tip_length=0.18)
    g.actor, g.person = a, p
    g.add(a, p, g.arrow)
    return g


def recap_thumb():
    g = bergman()
    return g.scale(6.0 / g.width).move_to(ORIGIN)


def dashed_slot(w, h, color=RED):
    return DashedVMobject(Rectangle(width=w, height=h).set_stroke(color, 2.5), num_dashes=32)


def table_card(name):
    t = Mono(name, 28, BLUE)
    f = RoundedRectangle(corner_radius=0.12, width=2.3, height=0.55).set_stroke(BLUE, 2.5)
    f.set_fill(BLUE, 0.06)
    t.move_to(f)
    g = VGroup(f, t)
    g.frame, g.label = f, t
    return g


def result_table(size=30, pitch=0.52):
    h_n, h_a = Mono("name", size), Mono("age", size)
    names = [Mono(n, size, color=BLUE) for n, _ in ROWS]
    ages = [Mono(str(v), size, color=BLUE) for _, v in ROWS]
    x_age = max(n.width for n in names) + 0.6
    for i, (n, a) in enumerate(zip(names, ages)):
        yy = -(i + 1) * pitch - 0.12
        n.move_to([n.width / 2, yy, 0])
        a.move_to([x_age + 0.5 - a.width / 2, yy, 0])     # right-aligned numbers
    h_n.move_to([h_n.width / 2, 0, 0])
    h_a.move_to([x_age + 0.5 - h_a.width / 2, 0, 0])
    rule = Line([-0.1, -0.3, 0], [x_age + 0.6, -0.3, 0]).set_stroke(DIM, 2)
    rows = [VGroup(n, a) for n, a in zip(names, ages)]
    g = VGroup(h_n, h_a, rule, *rows)
    g.header, g.rule, g.rows, g.names, g.ages = VGroup(h_n, h_a), rule, rows, names, ages
    return g


class Join(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c8.join.1: the actor object has no birth year ─────────────────────────────
    def clip1(self):
        b = bergman()
        self.b = b
        actor, person = b.actor, b.person
        final_c = actor.get_center().copy()
        actor.scale(1.2).move_to([0, 0.3, 0])
        q = T("How old were The Kid's actors when it came out?", 36, YELLOW).move_to([0, 3.5, 0])
        self.q = q
        slot = dashed_slot(4.0, 0.48)
        slot_t = T("birthyear?", 30, RED)
        with self.say("c8.join.1") as c:
            c.wait_until(own_word=q)
            self.play(*appear(q), run_time=1.0)
            c.wait_until("look")
            self.play(*appear(actor, shift=None), run_time=1.2)
            # walk the three keys with one sliding box
            keys = [actor.code.find(k) for k in ('"person_id"', '"name"', '"roles"')]
            c.wait_until("person ID")
            box = token_box(keys[0], actor.code.line(1))
            self.play(FadeIn(box), run_time=0.6)
            c.wait_until("a name")
            self.play(Transform(box, token_box(keys[1], actor.code.line(2))), run_time=0.6)
            c.wait_until("list of roles")
            self.play(Transform(box, token_box(keys[2], actor.code.line(3))), run_time=0.6)
            c.wait_until("missing")
            self.play(FadeOut(box), actor.animate.scale(1 / 1.2).move_to(final_c), run_time=1.0)
            slot.next_to(actor, DOWN, buff=0.12).align_to(actor, LEFT).shift(0.3 * RIGHT)
            slot_t.move_to(slot)
            self.play(*appear(slot, slot_t, shift=None, lag=0.2), run_time=0.6)
            c.wait_until("where")
            self.play(*during([FadeOut(q)], 0, 0.45), *during(appear(person, shift=None), 0.45, 1),
                      run_time=1.2)
            self.play(GrowArrow(b.arrow), FlashAround(b.year, color=GOLD, time_width=1.5),
                      run_time=min(1.2, c.until(floor=0.5)))
        self.slot = VGroup(slot, slot_t)

    # ── c8.join.2: a product, then a selection ───────────────────────────────────
    def clip2(self):
        qc = Code(QUERY, size=QS)
        qc.move_to(ORIGIN, aligned_edge=UL).shift([-6.3, 3.5, 0])
        self.qc = qc
        cards = [table_card(n) for n in ("movies", "t(a)", "people")]
        VGroup(*cards).arrange(DOWN, buff=0.14).move_to([-5.0, -2.45, 0])
        # actor x person grid
        nr, nc, pitch, cell = 4, 7, 0.46, 0.36
        grid = VGroup(*[Square(cell).set_stroke(DIM, 2).set_fill(DIM, 0.15)
                        .move_to([(j - (nc - 1) / 2) * pitch, -(i - (nr - 1) / 2) * pitch, 0])
                        for i in range(nr) for j in range(nc)])
        grid.move_to([0.2, -2.6, 0])
        h_p = T("people", 28, DIM).next_to(grid, UP, buff=0.18)
        h_a = T("actors", 28, DIM).next_to(grid, LEFT, buff=0.25)
        match = {(0, 2), (1, 5), (2, 0), (3, 4)}
        hits = [grid[i * nc + j] for i, j in sorted(match)]
        rest = [grid[i * nc + j] for i in range(nr) for j in range(nc) if (i, j) not in match]
        cap = MathTex(r"\sigma \text{ over } \times \;=\; \bowtie", font_size=60)
        cap.move_to([4.7, -2.6, 0])
        comma = qc.find(",", line=3, nth=1)
        times = Mono("×", 28, YELLOW).move_to([comma.get_x(), qc.line(3).get_y(), 0])
        self.c2 = dict(cards=cards, grid=grid, h_p=h_p, h_a=h_a, cap=cap, comma=comma, times=times)

        with self.say("c8.join.2") as c:
            c.wait_until("from")
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45),
                      *during(appear(qc, shift=None), 0.5, 1), run_time=1.6)
            self.play(FlashAround(VGroup(qc.line(3), qc.line(4)), time_width=1.5), run_time=1.5)
            for card, cue in zip(cards, ("The movies", "un-nested actors", "people table")):
                c.wait_until(cue)
                self.play(*appear(card), run_time=0.8)
            c.wait_until("product")
            self.play(comma.animate.set_opacity(0), *during(appear(times, shift=None), 0.5, 1),
                      run_time=1.0)
            self.play(*appear(h_p, h_a, shift=None, lag=0.1),
                      LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.03), run_time=1.4)
            c.wait_until("every actor")
            self.play(LaggedStart(*[s.animate.set_fill(YELLOW, 0.6) for s in grid], lag_ratio=0.03),
                      run_time=1.2)
            self.play(*[s.animate.set_fill(DIM, 0.15) for s in grid], run_time=0.6)
            c.wait_until("select")
            wbox = token_box(qc.find("person_id = (a->>'person_id')"), qc.line(5), color=GREEN)
            self.wbox = wbox
            self.play(FadeIn(wbox), run_time=0.8)
            c.wait_until("primary key")
            self.play(*[s.animate.set_fill(GREEN, 0.8).set_stroke(GREEN) for s in hits],
                      *[s.animate.set_fill(DIM, 0.04).set_stroke(opacity=0.2) for s in rest],
                      run_time=1.5)
            c.wait_until("parentheses")
            pg = P.paren_glyphs(qc, 5)
            self.play(*recolor(pg, YELLOW), *flash(pg, time_width=1.5), run_time=1.2)
            c.wait_until("join")
            self.play(*appear(cap), run_time=1.0)

    # ── c8.join.3: subtract, and the ages ────────────────────────────────────────
    def clip3(self):
        qc, k = self.qc, self.c2
        n1 = Mono("1921", 48, GOLD)
        mi = Mono("−", 48)
        n2 = Mono("1868", 48, GOLD)
        eq = Mono("=", 48)
        r = Mono("53", 48, GOLD)
        eqn = VGroup(n1, mi, n2, eq, r).arrange(RIGHT, buff=0.3).move_to([-3.4, -2.2, 0])
        tab = result_table()
        tab.move_to(ORIGIN, aligned_edge=UL).shift([1.3, 3.1, 0])
        note = T("year − year: may be one too high", 28, DIM).move_to([-3.4, -3.15, 0])
        gone = [*k["cards"], k["grid"], k["h_p"], k["h_a"], k["times"], self.wbox]
        with self.say("c8.join.3") as c:
            self.play(*during([FadeOut(m) for m in gone], 0, 0.45),
                      *during([k["comma"].animate.set_opacity(1)], 0.5, 1), run_time=1.2)
            c.wait_until("movie's year")
            cast1 = qc.find("(movie->>'year')::INTEGER", line=1)
            self.play(FlashUnder(cast1, color=GOLD, time_width=1.5), *appear(n1), run_time=1.2)
            c.wait_until("birth year")
            cast2 = qc.find("(person->>'birthyear')::INTEGER", line=2)
            self.play(FlashUnder(cast2, color=GOLD, time_width=1.5), *appear(mi, n2, lag=0.3),
                      run_time=1.2)
            c.wait_until("top")
            tail = Code("ORDER BY age DESC, name\nLIMIT    4;", size=QS)
            tail.move_to(ORIGIN, aligned_edge=UL).shift([-6.3, 1.6, 0])
            self.play(*edit(qc, tail), FadeOut(k["cap"]), run_time=1.5)
            self.qc = qc = tail
            self.play(*appear(tab.header, tab.rule, shift=None), run_time=0.7)
            self.play(*appear(tab.names[0]), run_time=0.8)
            c.wait_until("fifty-three")
            self.play(*appear(eq, r, lag=0.3), run_time=0.8)
            self.play(*appear(tab.ages[0], shift=None), FlashAround(r, color=GOLD, time_width=1.5),
                      run_time=1.0)
            for i, cue in ((1, "Blinn"), (2, "Albert Austin"), (3, "Edward Biby")):
                c.wait_until(cue)
                self.play(*appear(tab.rows[i]), run_time=0.8)
            c.wait_until("all")
            limit = list(qc.line(1))
            self.play(*set_alpha(limit, DIMMED), run_time=0.8)
            self.play(*appear(*tab.rows[4:], lag=0.15), run_time=1.6)
            c.wait_until("Jackie Coogan")
            self.play(*recolor(list(tab.rows[9]), YELLOW), *flash([tab.rows[9]], time_width=1.5),
                      run_time=1.2)
            c.wait_until("approx")
            self.play(*appear(note), run_time=1.0)

    # ── c8.join.4: the lesson ────────────────────────────────────────────────────
    def clip4(self):
        tw = S5.two_way()
        parts = [tw.kid, tw.chap, tw.a1, tw.a2]
        q1 = T("Who's in this movie?", 32, FG).move_to([-3.6, 3.1, 0])
        tick = check_mark().next_to(q1, RIGHT, buff=0.3)
        one = T("one read", 28, GREEN).next_to(tick, RIGHT, buff=0.2)
        VGroup(q1, tick, one).move_to([-3.4, 3.1, 0])
        q2 = T("Their ages?", 32, RED)
        q2f = RoundedRectangle(corner_radius=0.15, width=q2.width + 0.5, height=0.7).set_stroke(RED, 2.5)
        q2f.set_fill(RED, 0.08)
        q2.move_to(q2f)
        q2c = VGroup(q2f, q2).move_to([2.6, 3.1, 0])
        jn = MathTex(r"\bowtie", font_size=60, color=BLUE).move_to([5.6, 3.1, 0])
        jarr = Arrow(q2c.get_right(), jn.get_left(), buff=0.15, stroke_width=3, color=RED,
                     tip_length=0.18)
        nine = tw.kid.code.find("/* 9 more */")
        plus = Mono("+1868", 28, GOLD).next_to(nine, RIGHT, buff=0.3)
        cnt = H.docs_side().counter     # ch5 s1's copy counter: same look (T 30 GOLD)
        cnt1 = T("1 copy of 1868", 30, cnt.get_color()).move_to([-3.4, 3.1, 0])
        cnt2 = T("2 copies of 1868", 30, cnt.get_color()).move_to(cnt1)
        quote = VGroup(T("“…maybe it should", 36), T("have been relational", 36),
                       T("in the first place.”", 36)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        who = T("— the lecturer", 28, DIM).next_to(quote, DOWN, buff=0.35, aligned_edge=RIGHT)
        qbody = VGroup(quote, who)
        qf = RoundedRectangle(corner_radius=0.2, width=qbody.width + 0.8, height=qbody.height + 0.7)
        qf.set_stroke(DIM, 2.5).set_fill(DIM, 0.06).move_to(qbody)
        qcard = VGroup(qf, qbody).move_to([3.5, 0.6, 0])
        code = tw.kid.code
        keys = [code.find(f'"{k}"') for k in ("movie_id", "title", "actors", "person_id", "name", "roles")]
        frames = [SurroundingRectangle(g, color=GREEN, buff=0.05).set_stroke(GREEN, 2) for g in keys]
        up = T("decided up front", 36, GREEN).next_to(qcard, DOWN, buff=0.6)

        with self.say("c8.join.4", gap=1.2) as c:
            self.play(*during([FadeOut(m) for m in self.mobjects], 0, 0.45),
                      *during(appear(*parts, shift=None, lag=0.1), 0.5, 1), run_time=1.6)
            c.wait_until(own_word=q1)
            self.play(*appear(q1), run_time=0.9)
            c.wait_until("single read")
            self.play(*appear(tick, one, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("other")
            self.play(*appear(q2c), run_time=0.9)
            c.wait_until("joins")
            self.play(GrowArrow(jarr), *during(appear(jn, shift=None), 0.4, 1), run_time=1.0)
            c.wait_until("copy")
            self.play(*during([FadeOut(m) for m in (q1, tick, one)], 0, 0.45),
                      *during(appear(cnt1), 0.5, 1), run_time=1.4)
            c.wait_until("more copies")
            self.play(FadeIn(plus, scale=1.6), *swap(cnt1, cnt2), run_time=1.2)
            c.wait_until("lecturer")
            self.play(  # early: the quote card is shown whole, then read
                      *during([FadeOut(m) for m in (tw.chap, tw.a1, tw.a2, q2c,
                                                    jarr, jn)], 0, 0.45),
                      *during(appear(qcard, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("upfront")
            self.play(*during([FadeOut(plus), FadeOut(cnt2)], 0, 0.4),
                      LaggedStart(*[FadeIn(f) for f in frames], lag_ratio=0.15),
                      *during(appear(up), 0.4, 1), run_time=1.5)
