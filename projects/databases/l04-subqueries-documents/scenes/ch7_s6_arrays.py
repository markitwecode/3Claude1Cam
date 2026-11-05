"""Chapter 7, scene 6: Searching inside arrays. Clips c7.arrays.1 – c7.arrays.4.

Exports:
  recap_thumb()  for s8's r5: ch1 s4's Crime/Drama Venn (overlap filled, GOLD 397) over
      `list_contains` -> GOLD 72; static VGroup at ORIGIN, `.venn .row`.
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

S6 = load_scene("ch4_s6_store")
P = load_scene("ch7_s3_paths")
V = load_scene("ch1_s4_setops")

SQL = 28

COND1 = "(movie->>'year')::INTEGER >= 2021"
Q_CONTAINS = """SELECT COUNT(*) FROM movies
WHERE list_contains(movie->>'$.genres[*]', 'War');"""
Q_HASALL = """SELECT COUNT(*) FROM movies
WHERE list_has_all(movie->>'$.genres[*]',
                   ['Romance', 'Comedy']);"""
COND_CRIME = """list_has_all(movie->>'$.genres[*]',
             ['Crime', 'Drama'])"""
Q_SPIELBERG = """SELECT movie->>'title' AS title, movie->>'year' AS year
FROM   movies
WHERE list_contains(movie->>'$.directors[*].name',
                    'Steven Spielberg')
ORDER BY year
LIMIT 3;"""
RESULTS = [("Jaws", "1975"), ("Close Encounters of the Third Kind", "1977"),
           ("Raiders of the Lost Ark", "1981")]

SUMMARY = [
    ('{ year: { $gte: 2021 } }', "(movie->>'year')::INTEGER >= 2021"),
    ('{ genres: "War" }', "list_contains(movie->>'$.genres[*]', 'War')"),
    ('{ "directors.name": "Steven Spielberg" }',
     "list_contains(movie->>'$.directors[*].name',\n              'Steven Spielberg')"),
]


def count_tag(n, word="movies", size=40):
    return T(f"{n} {word}", size, t2c={n: GOLD})


def block_rect(m, color=YELLOW):
    r = SurroundingRectangle(m, buff=0.16, corner_radius=0.08)
    return r.set_stroke(color, 2).set_fill(color, 0.08).set_z_index(-1)


def recap_thumb():
    v = V.venn()
    v.both.set_fill(BLUE, V.FILL_OP)
    fn = Mono("list_contains", 36, BLUE)
    arrow = Arrow(LEFT, RIGHT, buff=0, stroke_width=4).set_color(DIM).scale(0.4)
    n = T("72", 44, GOLD)
    row = VGroup(fn, arrow, n).arrange(RIGHT, buff=0.3)
    g = VGroup(v, row).arrange(DOWN, buff=0.45).move_to(ORIGIN)
    g.venn, g.row = v, row
    return g


class ArraysScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c7.arrays.1: the three MongoDB questions; the first one's SQL ─────────
    def clip1(self):
        with self.say("c7.arrays.1") as c:
            mongo = S6.mongo_code(24).move_to(0.7 * UP)
            self.mongo = mongo
            self.play(*appear(*mongo, lag=0.3), run_time=1.6)  # early: the three questions, walked next
            box = block_rect(mongo[0])
            c.wait_until("twenty twenty-one")
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("War genre")
            self.play(Transform(box, block_rect(mongo[1])), run_time=0.8)
            c.wait_until("Steven Spielberg")
            self.play(Transform(box, block_rect(mongo[2])), run_time=0.8)

            c.wait_until("first")
            cond = Code(COND1, size=30)
            n383 = count_tag("383", size=36)
            VGroup(cond, n383).arrange(RIGHT, buff=0.5).next_to(mongo[0], DOWN, buff=0.45).set_x(0)
            drop = cond.height + 0.9
            self.play(mongo[1].animate.shift(drop * DOWN), mongo[2].animate.shift(drop * DOWN),
                      Transform(box, block_rect(mongo[0])), run_time=1.0)
            frag = mongo[0].find("{ year: { $gte: 2021 } }")
            self.play(FlashUnder(frag, color=YELLOW, time_width=1.5), *appear(cond), run_time=1.5)
            c.wait_until("three hundred")
            self.play(*appear(n383), run_time=1.0)

            c.wait_until("rest")
            keys = [mongo[1].find("genres"), mongo[2].find('"directors.name"')]
            self.play(*set_alpha([mongo[0], cond, n383], 0.4), FadeOut(box),
                      *[FlashUnder(k, color=YELLOW, run_time=1.5, time_width=1.5) for k in keys],
                      *[a for k in keys for a in recolor(k, YELLOW)], run_time=1.5)
            self.c1 = (cond, n383)

    # ── c7.arrays.2: a starred path gives a list; list_contains ─────────────
    def clip2(self):
        with self.say("c7.arrays.2") as c:
            path = Code("movie->>'$.genres[*]'", size=40).move_to(2.6 * UP)
            kid = P.list_box(P.GENRES, size=32)
            kid.move_to(0.6 * UP).align_to(np.array([-1.9, 0, 0]), LEFT)
            kid_lab = T("The Kid", 30, DIM).next_to(kid, LEFT, buff=0.4)
            arr = Arrow(path.get_bottom() + 0.1 * DOWN, [kid.get_center()[0], kid.get_top()[1] + 0.1, 0],
                        buff=0, stroke_width=3).set_color(BLUE)
            sweep_clear(self, time_span(FadeIn(path), 0.6, 1.2), run_time=1.2)
            self.play(GrowArrow(arr), *appear(kid, kid_lab), run_time=1.5)  # early: The Kid's genres, the list the path gives

            c.wait_until("contains")
            q = Code(Q_CONTAINS, size=SQL).move_to(2.75 * UP)
            spr = P.list_box(["Drama", "War"], size=32)
            spr.move_to(1.6 * DOWN).align_to(kid, LEFT)
            spr_lab = T("Saving Private Ryan", 30, DIM).next_to(spr, LEFT, buff=0.4)
            self.play(*swap(path, q), FadeOut(arr), run_time=1.4)
            self.play(*appear(spr, spr_lab), run_time=1.0)  # early: the second movie, probed on "seventy-two"

            c.wait_until("Is War among")
            probe = VGroup(T("War?", 30, YELLOW), marker(YELLOW)).arrange(DOWN, buff=0.08)
            probe.next_to(kid.items[0], UP, buff=0.22)
            self.play(FadeIn(probe, shift=0.15 * DOWN), run_time=0.6)
            for it in kid.items[1:]:
                self.play(probe.animate.next_to(it, UP, buff=0.22), run_time=0.55)
            no = cross_mark().next_to(kid, RIGHT, buff=0.35)
            self.play(probe.animate.set_color(RED), FadeIn(no, scale=0.6), run_time=0.6)

            c.wait_until("war")
            probe2 = VGroup(T("War?", 30, YELLOW), marker(YELLOW)).arrange(DOWN, buff=0.08)
            probe2.next_to(spr.items[1], UP, buff=0.22)
            self.play(FadeOut(probe), FadeIn(probe2, shift=0.15 * DOWN), run_time=0.7)
            yes = check_mark().next_to(spr, RIGHT, buff=0.35)
            self.play(spr.items[1].animate.set_color(GREEN), probe2.animate.set_color(GREEN),
                      FadeIn(yes, scale=0.6), run_time=0.8)
            n72 = count_tag("72").next_to(q.line(0), RIGHT, buff=0.7)
            self.play(*appear(n72), run_time=1.0)

            c.wait_until("any")
            m = Code('db.movies.find({ genres: "War" })', size=28, lang="javascript")
            m.move_to(3.1 * DOWN)
            m.set_opacity(0.6)
            y_q = q.line(1).get_center()[1]
            xm = -6.55
            link = VMobject().set_points_as_corners([
                m.get_left() + 0.15 * LEFT, [xm, m.get_center()[1], 0],
                [xm, y_q, 0], [q.get_left()[0] - 0.12, y_q, 0]]).set_stroke(DIM, 3)
            self.play(*appear(m), run_time=1.0)
            self.play(Create(link), run_time=1.2)
            self.c2 = dict(q=q, n72=n72, rest=[kid, kid_lab, spr, spr_lab, no, yes, probe2, m, link])

    # ── c7.arrays.3: list_has_all; the Venn comes back ───────────────────────
    def clip3(self):
        with self.say("c7.arrays.3", gap=0.9) as c:
            d = self.c2
            q2 = Code(Q_HASALL, size=SQL)
            q2.move_to(0.5 * UP)
            self.play(*during([FadeOut(m) for m in d["rest"] + [d["n72"]]], 0, 0.45),
                      *swap(d["q"], q2), run_time=1.4)
            lit = q2.find("['Romance', 'Comedy']")
            br = [q2.find("[", line=2)[0], q2.find("]", line=2)[0]]
            c.wait_until("second list")
            self.play(*recolor(br, BLUE), FlashUnder(lit, color=BLUE, time_width=1.5), run_time=1.5)

            c.wait_until("romcom")
            n174 = count_tag("174").next_to(q2.line(0), RIGHT, buff=0.7)
            c.wait_until("hundred and seventy-four")
            self.play(*appear(n174), run_time=1.0)

            c.wait_until("venn")
            v = V.venn().shift(1.0 * RIGHT + 0.45 * UP)
            sweep_clear(self, time_span(FadeIn(v), 0.6, 1.6), run_time=1.6)  # early: ch1's Venn returns whole
            card_t = Mono("INTERSECT", 32, BLUE)
            card = VGroup(RoundedRectangle(corner_radius=0.12, width=card_t.width + 0.5,
                                           height=card_t.height + 0.4)
                          .set_stroke(BLUE, 2.5).set_fill(BLUE, 0.08).move_to(card_t), card_t)
            card.move_to([-4.7, 0.9, 0])
            tag = VGroup(T("or a self-join:", 28, DIM), T("Exercise 10", 28, DIM)).arrange(DOWN, buff=0.12)
            tag.next_to(card, DOWN, buff=0.4)
            c.wait_until("intersect")
            self.play(*appear(card), run_time=1.0)
            c.wait_until("joined with itself")
            self.play(*appear(tag), run_time=1.0)  # early: one tag, "joined with itself" is its word

            c.wait_until("crime")
            cond = Mono(COND_CRIME, 28, TEAL, line_spacing=0.8).move_to([0.3, -2.6, 0])
            self.play(*appear(cond), run_time=0.8)
            res_arrow = Arrow(LEFT, RIGHT, buff=0, stroke_width=4).set_color(DIM).scale(0.35)
            res = T("397", 36, GOLD)
            res_g = VGroup(res_arrow, res).arrange(RIGHT, buff=0.25)
            res_g.next_to(cond, RIGHT, buff=0.35).align_to(cond, DOWN).shift(0.05 * UP)
            c.wait_until("three hundred")
            self.play(GrowArrow(res_arrow), *appear(res, shift=None), run_time=0.8)
            old = v.counts["both"]
            dst = T("397", 36, GOLD).move_to(old)
            c.wait_until("same overlap")
            self.play(*during([FadeOut(old)], 0, 0.4), *fly(res, dst, arc=-PI / 2), *V.fill(v, ["both"]),
                      run_time=1.1)
            self.play(FlashAround(dst, color=GOLD, time_width=1.5), run_time=c.until(floor=0.6))

    # ── c7.arrays.4: through an array of objects; Spielberg; the summary ─────
    def clip4(self):
        with self.say("c7.arrays.4", gap=2.6) as c:
            tree = P.walk_tree(keys=("movie_id", "genres", "actors", "directors"), open=[("directors", 0)])
            tree.move_to(0.45 * DOWN)
            sweep_clear(self, time_span(FadeIn(tree), 0.6, 1.6), run_time=1.6)

            c.wait_until("directors")
            path = Mono("$.directors[*].name", 40, TEAL).move_to(3.2 * UP)
            self.play(*appear(path), *P.light_step(tree, ()), run_time=1.0)
            steps = [("directors",), ("directors", 0), ("directors", 0, "name")]
            for p in steps:
                self.play(*P.light_step(tree, p), run_time=1.0)

            c.wait_until("spielberg")
            q = Code(Q_SPIELBERG, size=SQL).move_to(1.85 * UP)
            sweep_clear(self, time_span(FadeIn(q), 0.6, 1.4), run_time=1.4)
            n28 = count_tag("28").next_to(q.line(4), RIGHT, buff=1.6)
            c.wait_until("twenty-eight")
            self.play(*appear(n28), run_time=1.0)

            heads = VGroup(T("title", 28, DIM), T("year", 28, DIM))
            rows = []
            y0 = -0.6
            x_t, x_y = -5.4, 4.3
            heads[0].move_to([x_t, y0, 0], aligned_edge=LEFT)
            heads[1].move_to([x_y, y0, 0], aligned_edge=LEFT)
            rule = Line([x_t, y0 - 0.3, 0], [x_y + 1.0, y0 - 0.3, 0]).set_stroke(DIM, 2)
            for i, (t, y) in enumerate(RESULTS):
                tm = Mono(t, 30, BLUE).move_to([x_t, y0 - 0.85 - 0.62 * i, 0], aligned_edge=LEFT)
                ym = Mono(y, 30, BLUE).move_to([x_y, tm.get_center()[1], 0], aligned_edge=LEFT)
                rows.append((tm, ym))
            c.wait_until("three")
            self.play(*appear(VGroup(heads, rule), *[VGroup(*r) for r in rows], lag=0.15), run_time=1.2)  # early: the three rows shown whole, then walked
            prev = None
            for tm, ym in rows:
                c.wait_until(own_word=tm)
                anims = [*recolor([tm, ym], YELLOW)]
                if prev is not None:
                    anims += recolor(prev, BLUE)
                self.play(*anims, run_time=0.6)
                prev = [tm, ym]

            c.wait_until("answered")
            out = VGroup()
            ticks = []
            for js, sq in SUMMARY:
                mj = Code(js, size=28, lang="javascript")
                ms = Code(sq, size=28)
                ms.next_to(mj, DOWN, buff=0.22).align_to(mj, LEFT).shift(0.9 * RIGHT)
                ln = VMobject().set_points_as_corners([
                    mj.get_corner(DL) + np.array([0.25, -0.08, 0]),
                    [mj.get_left()[0] + 0.25, ms.line(0).get_center()[1], 0],
                    [ms.get_left()[0] - 0.12, ms.line(0).get_center()[1], 0]]).set_stroke(TEAL, 3)
                out.add(VGroup(mj, ln, ms))
            out.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to(0.45 * LEFT)
            for r in out:
                ticks.append(check_mark().move_to([out.get_right()[0] + 0.8, r.get_center()[1], 0]))
            sweep_clear(self, *[time_span(FadeIn(r, shift=0.2 * DOWN), 0.6 + 0.3 * i, 1.4 + 0.3 * i)
                                for i, r in enumerate(out)], run_time=2.0)
            self.play(*[FadeIn(t, scale=0.6) for t in ticks], run_time=0.8)
