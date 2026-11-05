"""Chapter 3, scene 4: Predict the count. Clips c3.predict.1 – c3.predict.5.

Opens on s3's last frame (ch3_s3_twins.handover_shot() = kid_ring()), ends on an empty frame.

Recap helpers (module level):
  kid_chords() -> VGroup(.ring, .chords, .label)
      .ring:   kid_ring() without the names (.movie, .people[i], .edges[i]), at ORIGIN
      .chords: the 45 GOLD chords (flat list; chord_lists(ring)[i] = person i's chords to j > i)
      .label:  GOLD "10 choose 2 = 45" (T 36) under the ring
  big_star() -> VGroup(.v, .p3, .m, .arrows, .tags)
      .v: s3's costar_v (p1 (-3.4, 2.5), m (0, 0.4), p2 (3.4, 2.5), r 0.65)
      .p3: PINK vnode "p3" at (0, -1.85); .m = .v.m
      .arrows [p1→m, p2→m, p3→m], .tags [three ACTED_IN]
"""
# style: 2
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

S3 = load_scene("ch3_s3_twins")

MOVIE_FILL = "#18262D"     # BLUE at 0.12 over BG, made opaque (chords pass under it)
PERSON_FILL = "#29202C"    # PINK at 0.12 over BG, opaque

SQL_SRC = """SELECT sum(k * (k - 1) // 2) AS pairs,
       sum(k * (k - 1) * (k - 2) // 6) AS triples
FROM (SELECT movie_id, count(*) AS k
      FROM has_position
      WHERE position = 'actor'
      GROUP BY movie_id);"""
# DuckDB's reply, verbatim; reply_table() draws it (frame as lines, so a cell can fly out)
REPLY_SRC = """┌────────┬─────────┐
│ pairs  │ triples │
│ int128 │ int128  │
├────────┼─────────┤
│ 130738 │  347841 │
└────────┴─────────┘"""

# the trio query, verbatim tokens, wrapped to fit at size 28
L0A = "MATCH (p1:Person) -[:ACTED_IN]-> (m:Movie)"
L0B = "      <-[:ACTED_IN]- (p2:Person)"
L1 = "      (p3:Person) -[:ACTED_IN]-> (m:Movie)"
L2A = "WHERE p1.person_id < p2.person_id"
L2B = "  AND p2.person_id < p3.person_id"
L3 = "RETURN count(*);"

P1, M, P2, P3 = [-3.4, 2.6, 0], [0, 0.75, 0], [3.4, 2.6, 0], [0, -1.2, 0]
NODE_R = 0.6

GRID_COLS, N_MOVIES = 70, 2935
GRID_PITCH, TILE = 0.115, 0.085
GRID_C = np.array([-1.4, 0.95, 0])


# ---------------------------------------------------------------- recap helpers
def chord_lists(ring, color=GOLD, width=2.5):
    """Chords between the ring's people, edge to edge: lists[i] = lines from person i to j > i."""
    ps = ring.people
    out = []
    for i in range(len(ps)):
        row = []
        for j in range(i + 1, len(ps)):
            a, b = ps[i].get_center(), ps[j].get_center()
            d = (b - a) / np.linalg.norm(b - a)
            r = ps[i].width / 2
            row.append(Line(a + d * r, b - d * r, stroke_width=width, color=color).set_z_index(-1))
        out.append(row)
    return out


def opaque_ring(ring):
    """Make the ring's circles opaque (same look) and lift them over chords."""
    ring.movie.circ.set_fill(MOVIE_FILL, 1)
    ring.movie.set_z_index(2)
    for p in ring.people:
        p.set_fill(PERSON_FILL, 1).set_z_index(1)
    return ring


def kid_chords():
    ring = opaque_ring(S3.kid_ring())
    ring.remove(*ring.names)
    chords = [l for row in chord_lists(ring) for l in row]
    label = T("10 choose 2 = 45", size=36, color=GOLD).next_to(ring, DOWN, buff=0.35)
    g = VGroup(*chords, ring, label)
    g.ring, g.chords, g.label = ring, chords, label
    return g


def big_star():
    v = S3.costar_v(P1, M, P2, r=NODE_R)
    p3 = S3.vnode("p3", PINK, P3, NODE_R, 40)
    s, e = p3.circ.get_top() + 0.04 * UP, v.m.circ.get_bottom() + 0.04 * DOWN
    a3 = Arrow(s, e, buff=0, stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.35, tip_length=0.24)
    t3 = set_backstroke(T("ACTED_IN", size=28)).next_to(a3, RIGHT, buff=0.15)
    g = VGroup(v, a3, p3, t3)
    g.v, g.p3, g.m, g.arrows, g.tags = v, p3, v.m, [*v.arrows, a3], [*v.tags, t3]
    return g


# ---------------------------------------------------------------- this scene's pieces
def cypher_codes():
    """The trio query in three stages (2, 3, 6 lines), Code 28, bottom at -3.55, same left edge."""
    c4 = Code("\n".join([L0A, L0B + ",", L1, L2A, L2B, L3]), size=28)
    c2 = Code("\n".join([L0A, L0B + ",", L1]), size=28)
    c1 = Code("\n".join([L0A, L0B]), size=28)
    x0 = -c4.width / 2
    c2.shift([x0 - c2.get_left()[0], -3.55 - c2.get_bottom()[1], 0])
    c4.shift([x0 - c4.get_left()[0], -3.55 - c4.get_bottom()[1], 0])
    c1.shift(c2.line(0).get_left() - c1.line(0).get_left())
    return c1, c2, c4


def m_glyphs(code):
    out = [code.find("(m:", line=0)[1]]
    if len(code.src.split("\n")) > 2:
        out.append(code.find("(m:", line=2)[1])
    return out


def reply_table(at):
    """DuckDB's reply as drawn by the shell (frame as lines, cells Mono 36), centred at `at`,
    plus an opaque cover over the triples column. -> (table, cover); table.pairs, table.triples."""
    sz = 36
    cw = 0.0083 * sz
    w1, w2 = 8 * cw + 0.1, 9 * cw + 0.1
    k = sz / 28
    ys = [k * y for y in (0.82, 0.37, -0.08, -0.38, -0.68, -1.0)]   # top, row1, row2, rule, row3, bottom
    x0, xm, x1 = -(w1 + w2) / 2, -(w1 + w2) / 2 + w1, (w1 + w2) / 2
    st = dict(stroke_width=2, color=FG)
    frame = VGroup(Rectangle(width=w1 + w2, height=ys[0] - ys[5], **st).move_to([0, (ys[0] + ys[5]) / 2, 0]),
                   Line([xm, ys[0], 0], [xm, ys[5], 0], **st), Line([x0, ys[3], 0], [x1, ys[3], 0], **st))

    def cell(txt, x_left, y, right=None):
        m = Mono(txt, size=sz)
        if right is not None:
            m.move_to([right - m.width / 2, y, 0])
        else:
            m.move_to([x_left + m.width / 2, y, 0])
        return m

    pairs_h, trip_h = cell("pairs", x0 + cw, ys[1]), cell("triples", xm + cw, ys[1])
    t1, t2 = cell("int128", x0 + cw, ys[2]), cell("int128", xm + cw, ys[2])
    pv, tv = cell("130738", x0 + cw, ys[4]), cell("347841", None, ys[4], right=x1 - cw)
    g = VGroup(frame, pairs_h, trip_h, t1, t2, pv, tv)
    g.shift(np.array(at) - np.array([0, (ys[0] + ys[5]) / 2, 0]))
    g.pairs, g.triples = pv, tv
    cover = Rectangle(width=w2 - 0.12, height=ys[0] - ys[5] - 0.12, stroke_color=DIM, stroke_width=2)
    cover.set_fill(BG, 1).move_to([g.get_center()[0] + (xm + x1) / 2, g.get_center()[1], 0]).set_z_index(3)
    return g, cover


def ordering(perm, at):
    g = VGroup()
    for k, n in enumerate(perm):
        c = Circle(radius=0.24, color=PINK, stroke_width=4).set_fill(PINK, 0.12)
        c.move_to([at[0] + (k - 1) * 0.62, at[1], 0])
        g.add(VGroup(c, Mono(str(n), size=28).move_to(c)))
    return g


class Predict(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ can we predict 45?
    def clip1(self):
        ring = opaque_ring(S3.handover_shot())
        self.add(ring)
        self.ring = ring
        with self.say("c3.predict.1") as c:
            gone = ring.names[2:]
            self.play(*disappear(*gone), run_time=0.8)
            ring.remove(*gone)
            self.remove(*gone)
            self.play(ring.animate.scale(1.1, about_point=ORIGIN).shift([0.28, 0.3, 0]), run_time=1.3)
            rows = T("45 rows", size=48, color=GOLD).move_to([5.3, 1.5, 0])
            self.play(*appear(rows), run_time=1.0)
            self.rows = rows

            c.wait_until("guess")
            q = T("how many?", size=44, color=GOLD).move_to([5.3, 2.6, 0])
            self.play(*appear(q), run_time=1.0)  # early: the question asked on screen
            self.q = q

            c.wait_until("prominent")
            cap = T("at most 10 actors per movie: only the most prominent cast", size=30, color=DIM)
            cap.move_to([0, -3.45, 0])
            self.play(*appear(cap), run_time=1.0)  # early: caption for the sentence being said
            self.cap = cap
            c.wait_until("exactly ten")
            self.play(LaggedStart(*flash(ring.people, color=YELLOW), lag_ratio=0.12), run_time=2.0)

            # chords
            self.chords = chord_lists(ring)
            ppl = ring.people
            self.digits = [T(str(9 - i), size=30, color=GOLD).move_to(ppl[i]).set_z_index(4)
                           for i in range(9)]
            c.wait_until("chords")
            self.play(*set_alpha(ring.edges, 0.35), run_time=0.6)
            self.play(LaggedStart(*[Create(l) for l in self.chords[0]], lag_ratio=0.12),
                      *appear(self.digits[0], shift=None), run_time=1.8)
            c.wait_until("coogan")
            self.play(LaggedStart(*[Create(l) for l in self.chords[1]], lag_ratio=0.12),
                      *appear(self.digits[1], shift=None), run_time=1.6)
            c.wait_until("already counted")
            hl = self.chords[0][0].copy().set_stroke(YELLOW, 7)
            self.play(VShowPassingFlash(hl, time_width=0.6), run_time=1.0)

            c.wait_until("and so on")
            runs = [AnimationGroup(*[Create(l) for l in self.chords[i]], FadeIn(self.digits[i]))
                    for i in range(2, 9)]
            self.play(LaggedStart(*runs, lag_ratio=0.45), run_time=min(1.9, c.until(floor=0.8)))
            self.chordg = VGroup(*[l for row in self.chords for l in row])
            settle(self, self.chordg)
            self.digg = VGroup(*self.digits)
            settle(self, self.digg)

    # ------------------------------------------------------------ 9 + ... + 1 = 45, the ceiling
    def clip2(self):
        ring = self.ring
        with self.say("c3.predict.2") as c:
            names = ring.names[:2]
            self.play(*disappear(self.cap, self.q, *names), run_time=0.8)
            ring.remove(*names)
            self.remove(*names)
            d = [-0.88, 0, 0]
            self.play(ring.animate.shift(d), self.chordg.animate.shift(d), self.digg.animate.shift(d),
                      run_time=1.0)
            parts = []
            for i in range(9):
                parts.append(T(str(9 - i), size=44, color=GOLD))
                if i < 8:
                    parts.append(T("+", size=44, color=GOLD))
            eq = T("=", size=44, color=GOLD)
            tot = T("45", size=44, color=GOLD)
            row = VGroup(*parts, eq, tot).arrange(RIGHT, buff=0.2).move_to([-0.6, -3.3, 0])
            nums, plus = parts[0::2], parts[1::2]
            terms = [x for i in range(9) for x in ([nums[i], plus[i]] if i < 8 else [nums[i]])]
            self.play(*appear(*terms, shift=None, lag=0.12),
                      LaggedStart(*[FlashAround(d, color=GOLD) for d in self.digits], lag_ratio=0.25),
                      run_time=2.4)
            c.wait_until("makes")
            self.play(*appear(eq, tot, shift=None, lag=0.2), run_time=0.9)
            self.sum = VGroup(*parts, eq, tot)
            settle(self, self.sum)

            c.wait_until("ten times")
            frac = MathTex(r"\frac{10 \times 9}{2}", "=", "45", font_size=56, color=GOLD)
            frac.move_to([5.2, -0.3, 0])
            self.play(*appear(frac), run_time=1.2)
            lab = T("10 choose 2", size=32, color=GOLD).next_to(frac, DOWN, buff=0.35)
            c.wait_until("choose")
            self.play(*appear(lab), run_time=0.9)
            self.frac, self.lab = frac, lab

            # one movie becomes one tile of 2,935
            c.wait_until("ceiling")
            self.play(FlashAround(frac[2], run_time=1.4, time_width=1.5), run_time=1.4)
            tiles = []
            for k in range(N_MOVIES):
                rr, cc = divmod(k, GRID_COLS)
                p = GRID_C + np.array([(cc - (GRID_COLS - 1) / 2) * GRID_PITCH,
                                       ((41) / 2 - rr) * GRID_PITCH, 0])
                tiles.append(Square(TILE, stroke_width=0).set_fill(BLUE, 0.7).move_to(p))
            rng = np.random.default_rng(5)
            kid_k = int(np.argmin([np.linalg.norm(t.get_center() - ring.movie.get_center()) for t in tiles]))
            pool = [k for k in range(N_MOVIES) if k != kid_k]
            short_k = set(rng.choice(pool, size=57, replace=False).tolist())
            empty_k = sorted(short_k)[23]
            short_k.discard(empty_k)
            self.full = VGroup(*[t for k, t in enumerate(tiles) if k not in short_k and k != empty_k])
            self.short = VGroup(*[tiles[k] for k in sorted(short_k)])
            self.empty = tiles[empty_k]
            tgt = tiles[kid_k].get_center()
            o = ring.movie.get_center()
            k = TILE / ring.width
            shrink = [m.animate.scale(k, about_point=o).shift(tgt - o).set_opacity(0)
                      for m in (ring, self.chordg, self.digg)]
            c.wait_until("two thousand")
            self.play(*during(disappear(self.sum, self.rows), 0, 0.35), *during(shrink, 0, 0.75),
                      *during([FadeIn(self.full), FadeIn(self.short), FadeIn(self.empty)], 0.35, 1),
                      run_time=2.2)
            self.remove(ring, self.chordg, self.digg)

            ceil = MathTex("2935", r"\times", "45", "=", "132075", font_size=60, color=GOLD)
            ceil.move_to([-1.4, -2.45, 0])
            self.play(*appear(ceil[0], ceil[1], ceil[2], shift=None, lag=0.2), run_time=1.3)
            c.wait_until("about a hundred")
            self.play(*appear(ceil[3], ceil[4], shift=None, lag=0.2), run_time=1.0)
            self.remove(*ceil.get_family())
            self.add(ceil)
            self.ceil = ceil

            c.wait_until("most")

            def flicker(m, a):
                m.set_fill(opacity=0.22 + 0.48 * (1 - a) * abs(np.cos(a * 3 * PI)))

            self.empty.set_stroke(BLUE, 1)
            self.play(UpdateFromAlphaFunc(self.short, flicker),
                      UpdateFromAlphaFunc(self.empty, lambda m, a: m.set_fill(opacity=0.7 * (1 - a))),
                      run_time=1.6)
            below = T("the true count: just below", size=30, color=DIM).move_to([-1.4, -3.45, 0])
            self.play(*appear(below), run_time=1.0)

    # ------------------------------------------------------------ check it in SQL
    def clip3(self):
        with self.say("c3.predict.3") as c:
            card = Code(SQL_SRC, size=28, lang="sql").move_to([0, 3.5, 0], aligned_edge=UP)
            for g in card.line(1):
                g.set_opacity(0.4)
            cy_lab = T("Cypher", size=30, color=DIM).move_to([-4.8, -1.15, 0])
            cy = Mono("130738", size=44, color=GOLD).move_to([-4.8, -1.9, 0])
            sweep_clear(self, *during(appear(card, shift=None), 0.5, 1), run_time=1.6)  # early: the query card shown whole
            self.play(*appear(cy_lab, cy, lag=0.3), run_time=1.0)  # early: the number being checked

            c.wait_until("count each")
            box = token_box(card.find("count(*) AS k"), card.line(2))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("add up")
            self.play(Transform(box, token_box(card.find("sum(k * (k - 1) // 2)"), card.line(0))),
                      run_time=1.0)

            c.wait_until("match")
            rep, cover = reply_table([3.5, -1.95, 0])
            self.play(*appear(rep, shift=None), FadeIn(cover), run_time=1.0)
            pv = rep.pairs
            self.play(FlashAround(pv, run_time=1.5, time_width=1.5), run_time=1.5)

            c.wait_until("exactly")
            eq = Mono("=", size=44, color=FG).move_to([-3.2, -1.9, 0])
            dst = Mono("130738", size=44, color=GOLD).move_to([-1.6, -1.9, 0])
            self.play(*fly(pv, dst), *during(appear(eq, shift=None), 0.6, 1), run_time=1.5)
            self.play(*recolor([*cy, *dst, *pv], GREEN), run_time=0.8)
            self.box = box

    # ------------------------------------------------------------ three actors: a star
    def clip4(self):
        with self.say("c3.predict.4") as c:
            star = big_star()
            v, p3, a3, t3 = star.v, star.p3, star.arrows[2], star.tags[2]
            c1, c2, c4 = cypher_codes()
            self.codes = (c2, c4)
            sweep_clear(self, *during(appear(v, c1, shift=None, lag=0.3), 0.5, 1), run_time=1.8)  # early: the V and its query return

            p3.move_to([5.9, 2.5, 0])
            c.wait_until("ends")
            self.play(*appear(p3), run_time=1.0)
            c.wait_until("only once")
            self.play(p3.animate.shift(0.75 * LEFT), run_time=0.8)
            c.wait_until("arriving")
            self.play(*flash([v.left.circ, v.right.circ], color=RED, run_time=1.4, time_width=1.5),
                      p3.animate.shift(0.75 * RIGHT), run_time=1.4)

            c.wait_until("comma")
            self.play(*edit(c1, c2), run_time=1.5)
            self.play(p3.animate.move_to(P3), run_time=1.4)
            self.play(GrowArrow(a3), *appear(t3), run_time=1.0)
            c.wait_until("shares the movie")
            self.play(*recolor(m_glyphs(c2), YELLOW), *recolor([v.m.lab], YELLOW),
                      FlashAround(v.m.circ, run_time=1.4, time_width=1.5), run_time=1.4)

            c.wait_until("star")
            self.play(*[VShowPassingFlash(a.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for a in star.arrows], run_time=1.4)
            self.remove(v, p3, a3, t3)
            self.add(star)
            self.star = star

    # ------------------------------------------------------------ once per trio; the run
    def clip5(self):
        star = self.star
        c2, c4 = self.codes
        with self.say("c3.predict.5") as c:
            tags = star.tags
            self.play(*disappear(*tags), run_time=0.7)
            for t in tags[:2]:
                star.v.remove(t)
            star.remove(tags[2])
            self.remove(*tags)
            self.play(star.animate.scale(0.7).move_to([-3.9, 1.6, 0]), run_time=1.2)
            perms = [(1, 2, 3), (1, 3, 2), (2, 1, 3), (2, 3, 1), (3, 1, 2), (3, 2, 1)]
            ords = [ordering(p, [1.3 + 2.3 * (i % 3), 2.4 - 1.3 * (i // 3)]) for i, p in enumerate(perms)]
            self.play(*appear(*ords, lag=0.15), run_time=1.5)
            c.wait_until("increasing")
            good = ords[0]
            tick = check_mark(GREEN).next_to(good, UP, buff=0.15)
            self.play(*set_alpha(ords[1:], DIMMED),
                      *[g[0].animate.set_color(GREEN).set_fill(GREEN, 0.15) for g in good],
                      FadeIn(tick, scale=1.3), run_time=1.0)

            c.wait_until("chain")
            for g in m_glyphs(c4):
                g.set_color(YELLOW)
            self.play(*edit(c2, c4), run_time=1.5)
            line = c4.line(3)
            box = token_box(c4.find("p1.person_id < p2.person_id"), line)
            c.wait_until("below")
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("below", nth=1)
            self.play(Transform(box, token_box(c4.find("p2.person_id < p3.person_id"), c4.line(4))), run_time=1.0)

            c.wait_until("per")
            mini = S3.kid_ring()
            mini.remove(*mini.names)
            mini.movie.remove(mini.movie.lab)
            mini.scale(0.5).move_to([1.9, 1.75, 0])
            kid = T("The Kid", size=30).next_to(mini, DOWN, buff=0.2)
            pp = mini.people
            tri = Polygon(*[pp[i].get_center() for i in (0, 3, 7)], color=GOLD, stroke_width=3).set_z_index(-1)
            ch = VGroup(T("10 choose 3", size=36, color=GOLD), T("= 120", size=36, color=GOLD))
            ch.arrange(DOWN, buff=0.25).move_to([5.3, 1.6, 0])
            self.play(*swap(VGroup(*ords, tick), VGroup(mini, kid)), FadeOut(box), run_time=1.2)
            self.play(Create(tri), *appear(ch, lag=0.3), run_time=1.3)

            c.wait_until("dare")
            note = T("too slow to try?", size=44).move_to([-3.4, 1.4, 0])
            rep, cover = reply_table([3.5, 1.4, 0])
            self.play(*during(disappear(star), 0, 0.45), *during(appear(note, shift=None), 0.5, 1),
                      run_time=1.4)  # early: the lecturer's worry

            c.wait_until("result")
            strike = Line(note.get_left() + 0.15 * LEFT, note.get_right() + 0.15 * RIGHT,
                          color=RED, stroke_width=5)
            self.play(Create(strike), *swap(VGroup(mini, kid, tri, ch), VGroup(rep, cover)), run_time=1.2)
            ans = Mono("347841", size=56, color=GOLD).move_to(note)
            self.play(*swap(VGroup(note, strike), ans), run_time=1.2)
            secs = Mono("(1.7 s)", size=30, color=DIM).next_to(ans, DOWN, buff=0.3)
            c.wait_until("seconds")
            self.play(*appear(secs), run_time=0.9)

            c.wait_until("sum3")
            tv = rep.triples
            self.play(FadeOut(cover), run_time=0.9)
            self.play(*recolor([*ans, *tv], GREEN), FlashAround(tv, run_time=1.4, time_width=1.5),
                      run_time=1.4)
