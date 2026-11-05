"""Chapter 10, scene 6: Exercise 19.4, the best-rated genres. Clips c10.genres.1 – c10.genres.4.

Clip 1: ch9 s9's next_card() row (no header), sub-card 19.4 bright; its box grows into ch8 s7's
ex19_card(4), hint(4) DIM under it, ch9 s1's pause icon on {stop}. Clip 2: The Kid's genres cell
unfolds into three rows (ch8 s2), each with its rating 8.2; the rows fall into genre buckets (ch8 s3's
bars) with GOLD averages; the cast `(movie->>'rating')::DOUBLE`; the full query and its result table.
Clip 3: no cast -> Binder Error; ::INTEGER -> rounded ratings, tied 8.0s; back to ::DOUBLE (or DECIMAL).
Clip 4: n_movies glows; Film-Noir and News open into movie chips; HAVING COUNT(*) >= 10; the
relational query's BLUE card returns the same five rows, linked GREEN. Ends on an empty frame.

The JSON query's first line (73 characters) is wrapped onto three lines to fit at a readable size.

EXPORTS (static): recap_r5() -> VGroup(.table (the {result} table, n_movies header GOLD),
  .double (Mono "::DOUBLE" GREEN), .integer (Mono "::INTEGER" RED), .strike (RED line through it)),
  centred at ORIGIN, about 11.3 wide x 3.0 tall.
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

R9 = load_scene("ch9_s9_recap")
T8 = load_scene("ch8_s7_try")
I9 = load_scene("ch9_s1_intro")
U = load_scene("ch8_s2_unnest")
D = load_scene("ch4_s3_movie")

# ══ data (verified on movies-json.duckdb / movies.duckdb) ══════════════════════
RESULT = [("Film-Noir", "8.27", "3"), ("News", "7.8", "1"), ("Documentary", "7.77", "39"),
          ("War", "7.69", "72"), ("Western", "7.58", "21")]
INT_RESULT = [("News", "8.0", "1"), ("Film-Noir", "8.0", "3"), ("Documentary", "7.82", "39"),
              ("War", "7.67", "72"), ("Western", "7.62", "21")]
HAV_RESULT = [("Documentary", "7.77", "39"), ("War", "7.69", "72"), ("Western", "7.58", "21"),
              ("Musical", "7.5", "29"), ("Biography", "7.43", "304")]
BUCKETS = [("Documentary", 7.77), ("War", 7.69), ("Comedy", 7.05), ("Drama", 7.35), ("Family", 7.11)]
KID_GENRES = ["Comedy", "Drama", "Family"]
NOIR = [("Double Indemnity", "8.3"), ("The Third Man", "8.1"), ("Sunset Boulevard", "8.4")]
NEWS = [("Food, Inc.", "7.8")]

CAST_LINE = {
    "double": "         ROUND(AVG((movie->>'rating')::DOUBLE), 2)",
    "none": "         ROUND(AVG(movie->>'rating'), 2)",
    "integer": "         ROUND(AVG((movie->>'rating')::INTEGER), 2)",
}
REL_SQL = """SELECT   g.name AS genre, ROUND(AVG(r.rating), 2) AS avg_rating,
         COUNT(*) AS n_movies
FROM     genres g
JOIN     has_genre hg ON hg.genre_id = g.genre_id
JOIN     ratings r ON r.movie_id = hg.movie_id
GROUP BY g.name
ORDER BY avg_rating DESC
LIMIT    5;"""
ERROR = ["Binder Error: No function matches the given",
         "name and argument types 'avg(VARCHAR)'. You",
         "might need to add explicit type casts."]

COLS = ["genre", "avg_rating", "n_movies"]
TSIZE, TPITCH = 28, 0.48
TABLE_LEFT, TABLE_TOP = -6.4, -0.45
Q_SIZE, Q_TOP = 25, 3.55


def json_sql(cast="double", having=False):
    lines = ["SELECT   genre,", CAST_LINE[cast], "         AS avg_rating,", "         COUNT(*) AS n_movies",
             "FROM     movies, unnest(movie->>'$.genres[*]') AS t(genre)", "GROUP BY genre"]
    if having:
        lines.append("HAVING   COUNT(*) >= 10")
    lines += ["ORDER BY avg_rating DESC", "LIMIT    5;"]
    return "\n".join(lines)


def json_query(cast="double", having=False):
    q = Code(json_sql(cast, having), size=Q_SIZE, line_spacing=0.72)
    if cast == "double":
        q.find("::DOUBLE").set_color(GREEN)
    elif cast == "integer":
        q.find("::INTEGER").set_color(RED)
    q.move_to([0, Q_TOP - q.height / 2, 0])
    return q


def _widths():
    allrows = RESULT + INT_RESULT + HAV_RESULT
    return [max([Mono(c, TSIZE, weight=BOLD).width] + [Mono(r[j], TSIZE).width for r in allrows]) + 0.32
            for j, c in enumerate(COLS)]


def result_table(rows, red=(), left=TABLE_LEFT, top=TABLE_TOP):
    """ch8's table look; header DIM, genres BLUE, numbers GOLD (cells in `red` RED)."""
    colors = [[BLUE, RED if (i, 1) in red else GOLD, GOLD] for i in range(len(rows))]
    t = U.table(COLS, [list(r) for r in rows], colors, size=TSIZE, pitch=TPITCH, widths=_widths())
    t.head.set_color(DIM)
    U.place(t, left, top)
    return t


def movie_chip(title, rating):
    lab = VGroup(T(title, 28, DIM), T(rating, 28, DIM)).arrange(RIGHT, buff=0.25)
    rect = RoundedRectangle(corner_radius=0.12, width=lab.width + 0.36, height=0.46)
    rect.set_stroke(DIM, 1.5).set_fill(BG, 1)
    lab.move_to(rect)
    g = VGroup(rect, lab)
    return g


def recap_r5():
    t = result_table(RESULT, left=0, top=0)
    t.head[2].set_color(GOLD)
    dbl = Mono("::DOUBLE", 36, GREEN)
    itg = Mono("::INTEGER", 36, RED)
    side = VGroup(dbl, itg).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
    strike = Line(itg.get_left() + 0.1 * LEFT, itg.get_right() + 0.1 * RIGHT).set_stroke(RED, 5)
    side.next_to(t, RIGHT, buff=0.9)
    strike.move_to(itg)
    g = VGroup(t, side, strike)
    g.table, g.double, g.integer, g.strike = t, dbl, itg, strike
    return g.move_to(ORIGIN)


def _row_y(i):
    return TABLE_TOP - TPITCH * (i + 1.5)


def _stream_dot(start, end, k, n, color=BLUE):
    d = Dot(start, radius=0.06, color=color).set_opacity(0)

    def upd(m, a):
        b = min(1.0, max(0.0, (a - 0.5 * k / n) / 0.5))
        p = start + (end - start) * smooth(b)
        m.move_to(p)
        m.set_opacity(0 if b <= 0 or b >= 1 else (1 if b < 0.8 else (1 - b) / 0.2))
    return d, UpdateFromAlphaFunc(d, upd)


class Ch10S6Genres(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c10.genres.1: card 19.4 grows out of the row; hint; pause icon
    def clip1(self):
        nc = R9.next_card()
        row = nc.row
        sub = nc.cards[19].subs[3]
        sub.box.set_stroke(FG, 2)
        sub.num.set_color(YELLOW)
        sub.sub.set_color(FG)
        big = T8.ex19_card(4)
        big.box.set_stroke(FG, 2)
        big.move_to([0, 1.15, 0])
        hnt = T8.hint(4).next_to(big, DOWN, buff=0.55)
        icon = I9.pause_icon(height=1.1).move_to([0, -2.45, 0])
        with self.say("c10.genres.1") as c:
            self.play(*appear(row, shift=None), run_time=0.7)   # early: the row the brief opens on
            self.play(*during(disappear(row), 0, 0.45),
                      *during([ReplacementTransform(sub.box.copy(), big.box)], 0.1, 0.75),
                      *during(appear(big.text, shift=None), 0.55, 1.0), run_time=1.6)
            c.wait_until("hint")
            self.play(*appear(hnt), run_time=1.0)
            c.wait_until("stop")
            self.play(*appear(icon, shift=None), run_time=0.8)
        self.big, self.hnt, self.icon = big, hnt, icon

    # c10.genres.2: unfold, group, cast, the query and its result
    def clip2(self):
        name = T("The Kid", 34)
        code = D.json_code('["Comedy", "Drama", "Family"]', 24)
        frame = D.fit_frame(code, size=24)
        cell = VGroup(frame, code).move_to([-3.6, 1.5, 0])
        name.next_to(cell, UP, buff=0.3).align_to(cell, LEFT)
        items = [code.find(g) for g in KID_GENRES]
        kt = U.table(["genre", "rating"], [[g, "8.2"] for g in KID_GENRES], [[BLUE, GOLD]] * 3,
                     size=28, pitch=0.5)
        U.place(kt, -5.7, 0.6)
        r_lab = T("rating", 28, DIM)
        r_val = Mono("8.2", 32, GOLD)
        r_src = VGroup(r_lab, r_val).arrange(DOWN, buff=0.15)
        r_src.move_to([kt.frame[0].get_right()[0] + 1.0, kt.rows[0].get_y() + 0.3, 0])
        r_val.set_y(kt.rows[0].get_y())
        r_lab.next_to(r_val, UP, buff=0.15)

        # buckets (ch8 s3's genre bars look): names right-aligned at NX, bars from NX + 0.25
        NX, BLEN, BP = 2.55, 3.0, 0.6
        b_y = [kt.rows[0].get_y() + 2 * BP, kt.rows[0].get_y() + BP] + [kt.rows[0].get_y() - BP * k for k in range(3)]
        names, bars, avgs = [], [], []
        for (g, a), y in zip(BUCKETS, b_y):
            n = T(g, 30).move_to([NX, y, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=BLEN * a / 7.77, height=0.4).set_stroke(BLUE, 2).set_fill(BLUE, 0.6)
            bar.move_to([NX + 0.25, y, 0], aligned_edge=LEFT)
            av = T(f"{a:.2f}", 30, GOLD).next_to(bar, RIGHT, buff=0.2)
            names.append(n)
            bars.append(bar)
            avgs.append(av)

        with self.say("c10.genres.2") as c:
            sweep_clear(self, FadeIn(name), FadeIn(cell), FadeIn(r_src), run_time=1.4)   # early: The Kid's row
            self.play(*appear(kt.frame, shift=None), run_time=0.8)
            c.wait_until("comedy")
            self.play(*U._drop_anims(items, kt), run_time=min(2.4, c.until("eight point two", floor=1.2)))
            c.wait_until("eight point two")
            flies = []
            for k in (2, 1, 0):
                j = 2 - k
                flies += during(fly(r_val, kt.cell(k, 1), arc=0), 0.25 * j, 0.5 + 0.25 * j)
            self.play(*flies, run_time=1.6)
            self.play(*appear(kt.head, shift=None), run_time=0.6)   # early: the columns' names
            settle(self, kt)

            c.wait_until("group")
            row_moves = []
            for k, g in enumerate(KID_GENRES):
                tgt = names[[b[0] for b in BUCKETS].index(g)]
                row_moves.append((kt.rows[k], tgt))
            anims = list(during(disappear(r_src), 0, 0.3))
            anims += during(appear(*names, lag=0.08, shift=None), 0.0, 0.45)
            for cp, tgt in row_moves:
                end = tgt.get_left() + LEFT * (cp.width / 2 + 0.15)
                anims += during([cp.animate.move_to(end).set_opacity(0)], 0.35, 1.0)
            dots = []
            n_dots = 16
            rng = np.random.default_rng(4)
            for k in range(n_dots):
                tgt = names[int(rng.integers(0, 5))]
                start = np.array([kt.frame[0].get_right()[0] + 0.25, kt.rows[0].get_y() - 1.0 * rng.random(), 0])
                d, a = _stream_dot(start, tgt.get_left() + 0.2 * LEFT, k, n_dots)
                dots.append(d)
                anims.append(during([a], 0.35, 1.0)[0])
            anims += during([GrowFromEdge(b, LEFT) for b in bars], 0.45, 1.0)
            self.play(*anims, run_time=min(2.2, c.until("average each")))   # early: the buckets the rows fall into
            self.remove(*dots)
            c.wait_until("average each")
            self.play(*appear(*avgs, lag=0.12, shift=None), run_time=1.0)

            # the cast
            c.wait_until("cast")
            expr = Code("(movie->>'rating')", 30)
            expr.move_to([-3.4, 0.5, 0])
            s_val = Mono("'8.2'", 36, BLUE).move_to([expr.get_x(), -0.7, 0])
            n_val = Mono("8.2", 36, GOLD).move_to(s_val)
            self.play(*during(disappear(name, cell, kt), 0, 0.45),
                      *set_alpha(bars + names + avgs, 0.5),
                      *during(appear(expr, s_val, lag=0.3, shift=None), 0.5, 1.0), run_time=1.4)
            c.wait_until("string")
            arrows = expr.find("->>")
            self.play(*recolor(arrows, YELLOW), FlashAround(arrows, time_width=1.5), run_time=1.0)
            c.wait_until("cast it")
            expr2 = Code("(movie->>'rating')::DOUBLE", 30)
            expr2.find("::DOUBLE").set_color(GREEN)
            expr2.move_to([-3.4, 0.5, 0])
            self.play(*edit(expr, expr2), *swap(s_val, n_val), run_time=min(1.4, c.until("result") - 0.1))

            # the whole query and its result
            c.wait_until("result")
            q = json_query("double")
            tbl = result_table(RESULT)
            sweep_clear(self, FadeIn(q), FadeIn(tbl.frame), FadeIn(tbl.head),
                        run_time=1.4)   # early: the query the line is about
            for k, word in enumerate(["film noir", "news"]):
                c.wait_until(word)
                self.play(*appear(tbl.rows[k], shift=None), run_time=0.8)
            c.wait_until("documentary")
            self.play(*appear(*tbl.rows[2:], lag=0.45, shift=None), run_time=1.6)
        self.q, self.tbl = q, tbl
        self.remove(*tbl.get_family())
        self.add(tbl.frame, tbl.head, *tbl.rows)

    # c10.genres.3: no cast, INTEGER, back to DOUBLE
    def clip3(self):
        q, tbl = self.q, self.tbl
        with self.say("c10.genres.3") as c:
            q_no = json_query("none")
            self.play(*edit(q, q_no), run_time=1.5)
            q = q_no
            c.wait_until("refuses")
            err = VGroup(*[Mono(s, 28, RED) for s in ERROR], Mono("…", 28, DIM))
            err.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0, -2.05, 0])
            self.play(*during(disappear(tbl.frame, tbl.head, *tbl.rows), 0, 0.45),
                      *during(appear(*err, lag=0.15, shift=None), 0.5, 1.0), run_time=1.4)

            c.wait_until("integer")
            q_int = json_query("integer")
            self.play(*edit(q, q_int), run_time=1.5)
            q = q_int
            c.wait_until("no error")
            it = result_table(INT_RESULT)
            self.play(*during(disappear(*err), 0, 0.45),
                      *during(appear(it.frame, it.head, *it.rows, lag=0.08, shift=None), 0.5, 1.0), run_time=1.4)

            c.wait_until("rounds")
            conv = VGroup()
            for s, v in (("'7.8'", "8"), ("'8.2'", "8")):
                lhs = Code(s + "::INTEGER", 28)
                lhs.find("::INTEGER").set_color(RED)
                ar = Arrow(LEFT * 0.35, RIGHT * 0.35, buff=0, stroke_width=3, color=DIM,
                           max_tip_length_to_length_ratio=0.3)
                rhs = Mono(v, 32, GOLD)
                conv.add(VGroup(lhs, ar, rhs).arrange(RIGHT, buff=0.25))
            conv.arrange(DOWN, buff=0.45, aligned_edge=LEFT)
            conv.move_to([4.15, _row_y(1) - 0.2, 0])
            self.play(*appear(*conv, lag=0.5, shift=None), run_time=1.4)
            c.wait_until("news ties")
            ties = [it.cell(0, 1), it.cell(1, 1)]
            self.play(*recolor(ties, RED), *flash(ties, color=RED, time_width=1.5), run_time=1.4)

            c.wait_until("double")
            q_dbl = json_query("double")
            dec = T("or DECIMAL", 28, DIM)
            dec.move_to([q_dbl.find("::DOUBLE").get_center()[0], q_dbl.line(2).get_y(), 0])
            self.play(*edit(q, q_dbl), *during(disappear(*conv), 0, 0.4), run_time=1.4)
            q = q_dbl
            tbl = result_table(RESULT)
            sw = [a for i in range(5) for a in swap(it.rows[i], tbl.rows[i])]
            self.play(*sw, *appear(dec), run_time=1.2)  # early: said with the cast
            self.remove(*it.frame.get_family(), *it.head.get_family())
            self.add(tbl.frame, tbl.head)
        self.q, self.tbl, self.dec = q, tbl, dec

    # c10.genres.4: n_movies, the few movies, HAVING, the relational version
    def clip4(self):
        q, tbl, dec = self.q, self.tbl, self.dec
        with self.say("c10.genres.4", gap=1.0) as c:
            col = [tbl.cell(i, 2) for i in range(5)]
            self.play(*recolor([tbl.head[2]], GOLD), *flash(col, color=GOLD, time_width=1.5),
                      FlashAround(tbl.head[2], color=GOLD, time_width=1.5), run_time=1.6)

            c.wait_until("few")
            x0 = tbl.frame[0].get_right()[0]
            noir = [movie_chip(*m) for m in NOIR]
            for k, ch in enumerate(noir):
                ch.move_to([0, _row_y(0) + 0.55 * (1 - k), 0]).align_to([x0 + 1.0, 0, 0], LEFT)
            news = movie_chip(*NEWS[0])
            news.move_to([0, _row_y(1) - 0.75, 0]).align_to([x0 + 1.0, 0, 0], LEFT)
            fan = [Line([x0 + 0.1, _row_y(0), 0], ch.get_left() + 0.08 * LEFT).set_stroke(DIM, 2) for ch in noir]
            nl = Line([x0 + 0.1, _row_y(1), 0], news.get_left() + 0.08 * LEFT).set_stroke(DIM, 2)
            self.play(*[Create(f) for f in fan], *appear(*noir, lag=0.2, shift=None), run_time=1.4)
            c.wait_until("news is just")
            self.play(Create(nl), *appear(news, shift=None), run_time=1.0)

            c.wait_until("trust only")
            q_h = json_query("double", having=True)
            self.play(*during(disappear(*noir, news, *fan, nl), 0, 0.35),
                      *edit(q, q_h), dec.animate.move_to([dec.get_x(), q_h.line(2).get_y(), 0]),
                      run_time=1.6)
            q = q_h
            hv = q.line(6)
            ht = result_table(HAV_RESULT)
            ht.head[2].set_color(GOLD)
            old = tbl.rows
            moves = [old[i].animate.move_to(ht.rows[i - 2]) for i in (2, 3, 4)]
            self.play(*during(disappear(old[0], old[1]), 0, 0.35), *during(moves, 0.25, 0.75),
                      *during(appear(ht.rows[3], ht.rows[4], lag=0.2, shift=None), 0.6, 1.0), run_time=1.8)
            c.wait_until("add having")
            self.play(FlashAround(hv, color=BLUE, time_width=1.5), run_time=1.2)
            c.wait_until("musical")
            self.play(*flash([ht.rows[3], ht.rows[4]], time_width=1.5), run_time=1.2)

            # the relational version
            c.wait_until("same")
            rq = Code(REL_SQL, size=22)
            card = RoundedRectangle(corner_radius=0.2, width=rq.width + 0.6, height=rq.height + 0.5)
            card.set_stroke(BLUE, 2.5).set_fill(BG, 0)
            rcard = VGroup(card, rq)
            rq.move_to(card)
            rcard.move_to([0, 3.75 - card.height / 2, 0])
            s = 0.8
            top = rcard.get_bottom()[1] - 0.35
            lt = result_table(RESULT, left=0, top=0).scale(s, about_point=ORIGIN)
            rt = result_table(RESULT, left=0, top=0).scale(s, about_point=ORIGIN)
            lt.shift([-6.5, top, 0])
            rt.shift([6.5 - rt.width, top, 0])
            sweep_clear(self, FadeIn(rcard), FadeIn(lt), run_time=1.4)
            self.play(*appear(rt, shift=None), run_time=1.0)
            links = []
            for i in range(5):
                y = lt.rows[i].get_y()
                links.append(Line([lt.frame[0].get_right()[0] + 0.06, y, 0],
                                  [rt.frame[0].get_left()[0] - 0.06, y, 0]).set_stroke(GREEN, 4))
            self.play(*[Create(l) for l in links], *flash([lt.cell(i, 1) for i in range(5)], color=GREEN),
                      *flash([rt.cell(i, 1) for i in range(5)], color=GREEN),
                      run_time=min(1.4, max(0.6, c.until() - 0.1)))
