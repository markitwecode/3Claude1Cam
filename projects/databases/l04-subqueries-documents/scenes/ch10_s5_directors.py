"""Chapter 10, scene 5: Exercise 19.2 and 19.3, directors. Clips c10.directors.1 – c10.directors.5.

Export for s7 (static): recap_r4() -> VGroup at ORIGIN: the five-director bars (Spielberg 28 on
top) beside The Kid's two ID lists, Chaplin's ID YELLOW in both. `.bars .lists`.
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
D = load_scene("ch4_s3_movie")

Q1 = """SELECT   person->>'name' AS name,
         json_array_length(person, '$.directed') AS n_directed
FROM     people
ORDER BY n_directed DESC, name
LIMIT    5;"""
Q1W = """SELECT   person->>'name' AS name,
         json_array_length(person, '$.directed') AS n_directed
FROM     people
WHERE    json_exists(person, '$.directed')
ORDER BY n_directed DESC, name
LIMIT    5;"""
Q2 = """SELECT   movie->>'title' AS title, movie->>'year' AS year
FROM     movies
WHERE    list_has_any(movie->>'$.directors[*].person_id',
                      movie->>'$.actors[*].person_id')
ORDER BY year, title;"""
Q1_SIZE, Q2_SIZE, Q_TOP = 26, 26, 3.6

TOP5 = [("Steven Spielberg", 28), ("Ridley Scott", 20), ("Tim Burton", 18),
        ("Clint Eastwood", 15), ("Martin Scorsese", 15)]
CHAPLIN_SRC = "\n".join([
    '{',
    '  "name": "Charles Chaplin",',
    '  "directed": [',
    '    {"title": "The Kid", …},',
    '    {"title": "The Gold Rush", …},',
    '    {"title": "City Lights", …},',
    '    {"title": "Modern Times", …},',
    '    {"title": "The Great Dictator", …}',
    '  ], …',
    '}'])
KID_SRC = "\n".join(['{', '  "title": "The Kid",', '  "directors": [ … ],', '  "actors": [ … ],', '  …', '}'])
DIRS = [("nm0000122", "Charles Chaplin")]
ACTORS = [("nm0000122", "Charles Chaplin"), ("nm0701012", "Edna Purviance"), ("nm0001067", "Jackie Coogan"),
          ("nm0588033", "Carl Miller"), ("nm0042317", "Albert Austin"), ("nm0047800", "Beulah Bains"),
          ("nm0048798", "Nellie Bly Baker"), ("nm0074788", "Henry Bergman"), ("nm0080930", "Edward Biby"),
          ("nm0088471", "B.F. Blinn")]
RES2 = [("The Kid", "1921", "Charles Chaplin"), ("Sherlock Jr.", "1924", "Buster Keaton"),
        ("The Gold Rush", "1925", "Charles Chaplin"), ("The General", "1926", "Buster Keaton")]

N_STRIPES, GOLD_AT = 48, (7, 22, 38)        # 1,458 / 23,179 of 48 stripes ≈ 3
COL_X, COL_TOP, COL_H, COL_W = 3.25, 0.3, 3.3, 0.8


# ══ pieces ═════════════════════════════════════════════════════════════════════
def director_bars(size=32, max_len=3.0, pitch=0.65, name_x=-2.3, top=0.0, header=True):
    names, bars, counts, rows = [], [], [], []
    for i, (nm, n) in enumerate(TOP5):
        y = top - pitch * i
        name = T(nm, size).move_to([name_x, y, 0], aligned_edge=RIGHT)
        bar = Rectangle(width=max_len * n / TOP5[0][1], height=0.0095 * size * 1.9)
        bar.set_stroke(BLUE, 2).set_fill(BLUE, 0.6).move_to([name_x + 0.25, y, 0], aligned_edge=LEFT)
        cnt = T(str(n), size, GOLD).next_to(bar, RIGHT, buff=0.2)
        names.append(name)
        bars.append(bar)
        counts.append(cnt)
        rows.append(VGroup(name, bar, cnt))
    head = VGroup()
    if header:
        hy = top + pitch * 0.95
        hn = Mono("name", 28, DIM).move_to([name_x, hy, 0], aligned_edge=RIGHT)
        hc = Mono("n_directed", 28, DIM).move_to([counts[0].get_right()[0], hy, 0], aligned_edge=LEFT)
        hc.align_to(hn, DOWN)
        hc.shift((counts[0].get_left()[0] - hc.get_left()[0]) * RIGHT)
        head.add(hn, hc)
    g = VGroup(head, *rows)
    g.rows, g.names, g.bars, g.counts, g.head = rows, names, bars, counts, head
    return g


def cards_row(i):
    """ch9 s9's next_card() cards (no header), all DIM but sub-card 19.i bright."""
    nc = R9.next_card()
    row = nc.row
    for m in row.get_family():
        if isinstance(m, Text):
            m.set_color(DIM)
    sub = nc.cards[19].subs[i - 1]
    sub.box.set_stroke(FG, 2.5)
    sub.num.set_color(FG)
    sub.sub.set_color(FG)
    return row, sub


def entry(pid, name):
    i = Mono(pid, 30, DIM)
    n = T(name, 28, DIM).next_to(i, DOWN, buff=0.12)
    g = VGroup(i, n)
    g.id, g.name = i, n
    return g


def list_frame(m):
    return SurroundingRectangle(m, buff=0.2, corner_radius=0.15).set_stroke(TEAL, 2).set_fill(TEAL, 0.04)


def person_icon(color=FG):
    head = Circle(radius=0.2).set_stroke(color, 3)
    body = Arc(radius=0.38, start_angle=0, angle=PI).set_stroke(color, 3)
    body.next_to(head, DOWN, buff=0.06).shift(0.2 * DOWN)
    return VGroup(head, body)


def recap_r4():
    bars = director_bars(name_x=0, top=0)
    d = Mono("[nm0000122]", 30, DIM)
    a = Mono("[nm0000122, nm0701012, …]", 30, DIM)
    for m in (d, a):
        m[1:10].set_color(YELLOW)
    dl, al = T("directors", 28, DIM), T("actors", 28, DIM)
    lists = VGroup(VGroup(dl, d).arrange(DOWN, buff=0.15, aligned_edge=LEFT),
                   VGroup(al, a).arrange(DOWN, buff=0.15, aligned_edge=LEFT)).arrange(DOWN, buff=0.45,
                                                                                       aligned_edge=LEFT)
    g = VGroup(bars, lists).arrange(RIGHT, buff=0.9).move_to(ORIGIN)
    g.bars, g.lists = bars, lists
    return g


def rt(c, cue, want, frac=0.85):
    return max(0.4, min(want, frac * c.until(cue)))


# ══ scene ══════════════════════════════════════════════════════════════════════
class Ch10S5Directors(NarratedScene):
    def construct(self):
        self.question(2, "c10.directors.1", "hint", "stop")
        self.clip2()
        self.clip3()
        self.question(3, "c10.directors.4", "hint2", "stop2")
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- 19.2 / 19.3 cards
    def question(self, i, cid, hint_cue, stop_cue):
        with self.say(cid) as c:
            row, sub = cards_row(i)
            if self.mobjects:
                sweep_clear(self, FadeIn(row), run_time=1.2)   # early: the cards row is the "question" shown whole
            else:
                self.play(FadeIn(row), run_time=0.8)   # early: the cards row is the "question" shown whole
            big = T8.ex19_card(i).move_to([0, 1.0, 0])
            self.play(*during(disappear(row), 0, 0.45),
                      *during([ReplacementTransform(sub.box.copy(), big.box)], 0.1, 0.85),
                      *during(appear(big.text, shift=None), 0.55, 1.0), run_time=1.6)   # early: the question is read now
            c.wait_until(hint_cue)
            hnt = T8.hint(i, size=32).move_to([0, -0.6, 0])
            self.play(*appear(hnt), run_time=1.0)   # early: the hint is spoken as words
            c.wait_until(stop_cue)
            icon = I9.pause_icon(1.2).move_to([0, -2.3, 0])
            self.play(FadeIn(icon, scale=0.8), run_time=0.8)

    # ---------------------------------------------------------------- 19.2 solution
    def clip2(self):
        with self.say("c10.directors.2") as c:
            card = T8.doc(CHAPLIN_SRC, size=26)
            card.move_to([0.4, Q_TOP - card.height / 2, 0])
            sweep_clear(self, *appear(card, shift=None), run_time=1.4)
            c.wait_until("five elements")
            nums = [T(str(k + 1), 32, GOLD).move_to([card.frame.get_left()[0] - 0.4,
                                                     card.code.line(3 + k).get_y(), 0]) for k in range(5)]
            self.play(*appear(*nums, shift=None, lag=0.5), run_time=2.2)
            c.wait_until("so its")
            expr = Code("json_array_length(person, '$.directed')", 30)
            expr.move_to([0, -2.85, 0])
            arr = Arrow(expr.get_right() + 0.3 * RIGHT, expr.get_right() + 1.1 * RIGHT, buff=0,
                        stroke_width=4, color=DIM, max_tip_length_to_length_ratio=0.3)
            five = T("5", 48, GOLD).next_to(arr, RIGHT, buff=0.3)
            VGroup(expr, arr, five).set_x(0)
            self.play(*appear(expr, shift=None), GrowArrow(arr), run_time=1.0)
            self.play(FlashAround(nums[4], color=GOLD, time_width=1.5), *appear(five, shift=None), run_time=rt(c, "query", 1.4))
            c.wait_until("query")

            q = Code(Q1, Q1_SIZE)
            q.move_to([0, Q_TOP - q.height / 2, 0])
            self.q = q
            sweep_clear(self, *appear(q, shift=None), run_time=1.5)
            c.wait_until("result")

            bars = director_bars()
            self.bars = bars
            cues = ["result", "ridley scott", "tim burton", "and clint eastwood"]
            groups = [[0], [1], [2], [3, 4]]
            for k, (cue, idx) in enumerate(zip(cues, groups)):
                c.wait_until(cue)
                anims = []
                if k == 0:
                    anims += appear(bars.head, shift=None)
                for j in idx:
                    anims += appear(bars.names[j], bars.counts[j], shift=None, lag=0.1)
                    anims.append(GrowFromEdge(bars.bars[j], LEFT))
                self.play(*anims, run_time=1.2 if k == 0 else 1.0)

            c.wait_until("tie")
            nm = q.find(", name", line=3)
            self.play(*recolor([bars.counts[3], bars.counts[4]], YELLOW),
                      *flash([bars.counts[3], bars.counts[4]]), run_time=1.4)
            c.wait_until("sorting by name")
            self.play(*recolor(nm, YELLOW), FlashUnder(nm, color=YELLOW, time_width=1.5), run_time=1.4)

            c.wait_until("spielberg")
            ct = T("part 7: movie side", 28, DIM)
            cc = Code("directors[*].name", 28)
            cn = T("28 movies", 40, t2c={"28": GOLD})
            body = VGroup(cn, cc, ct).arrange(DOWN, buff=0.22)
            frame = SurroundingRectangle(body, buff=0.25, corner_radius=0.15).set_stroke(DIM, 2)
            cb = VGroup(frame, body)
            cb.move_to([4.6, 0, 0]).shift((bars.counts[0].get_y() - cn.get_y()) * UP)
            link = Arrow(bars.counts[0].get_right() + 0.1 * RIGHT, [frame.get_left()[0] - 0.05, cn.get_y(), 0], buff=0,
                         stroke_width=4, color=YELLOW, max_tip_length_to_length_ratio=0.2)
            self.play(*recolor([bars.counts[3], bars.counts[4]], GOLD), *recolor(nm, FG),
                      FlashAround(bars.counts[0], color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("part seven")
            self.play(*appear(cb, shift=None), run_time=1.0)
            self.play(GrowArrow(link), FlashAround(cn[:2], color=YELLOW, time_width=1.5), run_time=rt(c, None, 1.2))
            self.cb, self.link = cb, link

    # ---------------------------------------------------------------- NULLs
    def clip3(self):
        q, bars = self.q, self.bars
        with self.say("c10.directors.3") as c:
            h = COL_H / N_STRIPES
            frame = Rectangle(width=COL_W + 0.12, height=COL_H + 0.12).set_stroke(DIM, 2)
            frame.move_to([COL_X, COL_TOP - COL_H / 2, 0])
            stripes = []
            for k in range(N_STRIPES):
                col = GOLD if k in GOLD_AT else PINK
                s = Rectangle(width=COL_W, height=h).set_stroke(col, 1, opacity=0.85).set_fill(col, 0.85)
                s.move_to([COL_X, COL_TOP - h * (k + 0.5), 0])
                s.gold = k in GOLD_AT
                stripes.append(s)
            lx = COL_X + COL_W / 2 + 0.35
            people = T("23,179 people", 28, DIM).move_to([lx, COL_TOP - COL_H / 2, 0], aligned_edge=LEFT)
            self.play(*during(disappear(self.cb, self.link), 0, 0.4),
                      *during([FadeIn(frame), *[FadeIn(s) for s in stripes], *appear(people, shift=None)],
                              0.4, 1.0), run_time=1.6)
            c.wait_until("twenty-one thousand")
            gold_lab = T("1,458 numbers", 28, GOLD).move_to([lx, COL_TOP - 0.15, 0], aligned_edge=LEFT)
            pink_lab = T("21,721 NULL", 28, PINK).move_to([lx, COL_TOP - COL_H * 0.5, 0], aligned_edge=LEFT)
            self.play(*swap(people, VGroup(gold_lab, pink_lab)), run_time=1.2)   # early: the counts are what "twenty-one thousand" says

            # DuckDB: numbers first, NULLs sink
            c.wait_until("last")
            order = [s for s in stripes if s.gold] + [s for s in stripes if not s.gold]
            duck = VGroup(T("DuckDB:", 28), T("NULLS LAST", 28, PINK)).arrange(DOWN, buff=0.12,
                                                                                 aligned_edge=LEFT)
            duck.move_to([lx, COL_TOP - COL_H + 0.35, 0], aligned_edge=LEFT)
            self.play(*[s.animate.move_to([COL_X, COL_TOP - h * (k + 0.5), 0]) for k, s in enumerate(order)],
                      *during(appear(duck), 0.55, 1.0), run_time=2.2)

            # Postgres: NULLs first
            c.wait_until("pg")
            order = [s for s in stripes if not s.gold] + [s for s in stripes if s.gold]
            pg = VGroup(T("Postgres:", 28, DIM, slant=ITALIC), T("DESC ⇒", 28, DIM, slant=ITALIC),
                        T("NULLS FIRST", 28, DIM, slant=ITALIC)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            pg.move_to([lx, COL_TOP - 0.55, 0], aligned_edge=LEFT)
            gold2 = T("1,458 numbers", 28, GOLD).move_to([lx, COL_TOP - COL_H + 0.1, 0], aligned_edge=LEFT)
            pink_to = pink_lab.copy().move_to([lx, COL_TOP - COL_H * 0.55, 0], aligned_edge=LEFT)
            self.play(*during(disappear(duck, gold_lab), 0, 0.35),
                      *during([pink_lab.animate.move_to(pink_to)], 0.2, 0.6),
                      *during([s.animate.move_to([COL_X, COL_TOP - h * (k + 0.5), 0])
                               for k, s in enumerate(order)], 0.25, 0.85),
                      *during(set_alpha(bars.rows, DIMMED), 0.3, 0.8),
                      *during(appear(pg, gold2, shift=None), 0.7, 1.0), run_time=2.4)
            c.wait_until("where json exists")
            q2 = Code(Q1W, Q1_SIZE)
            q2.move_to(q.get_corner(UL), aligned_edge=UL)
            self.play(*edit(q, q2), run_time=rt(c, None, 1.5, 0.5))
            ok = check_mark().next_to(q2.line(3), RIGHT, buff=0.4)
            self.play(*set_alpha(bars.rows, 1), FadeIn(ok, scale=0.8), run_time=1.0)

    # ---------------------------------------------------------------- 19.3 solution
    def clip5(self):
        with self.say("c10.directors.5") as c:
            card = T8.doc(KID_SRC, size=26)
            card.move_to([-4.1, 0.3, 0])
            sweep_clear(self, *appear(card, shift=None), run_time=1.2)

            c1, c2 = 0.7, 4.2
            dh = Code("movie->>'$.directors[*].person_id'", 26).move_to([0, 3.45, 0])
            dh.align_to(np.array([-0.95, 0, 0]), LEFT)
            de = entry(*DIRS[0]).move_to([c1, 2.6, 0])
            df = list_frame(de)
            ah = Code("movie->>'$.actors[*].person_id'", 26).move_to([0, 1.7, 0]).align_to(dh, LEFT)
            aes = [entry(*p) for p in ACTORS]
            for k, e in enumerate(aes):
                e.move_to([c1 if k < 5 else c2, 0.85 - 0.9 * (k % 5), 0])
            ag = VGroup(*aes)
            af = list_frame(ag)
            c.wait_until("the directors")
            pulls = []
            for k, (dst, frm) in enumerate([(df, None), (af, None)]):
                src = card.code.find("[ … ]", nth=k)
                pulls.append(Arrow(src.get_right() + 0.15 * RIGHT, dst.get_left() + 0.1 * LEFT, buff=0,
                                   stroke_width=3, color=TEAL, max_tip_length_to_length_ratio=0.12))
            for k, (src, hd, fr, body) in enumerate([(card.code.find("[ … ]"), dh, df, de),
                                                      (card.code.find("[ … ]", nth=1), ah, af, ag)]):
                if k:
                    c.wait_until("the actors")
                self.play(FlashAround(src, color=TEAL, time_width=1.5), GrowArrow(pulls[k]),
                          *during(appear(hd, fr, body, shift=None, lag=0.15), 0.35, 1.0), run_time=1.6)

            c.wait_until("share")
            true = Mono("TRUE", 40, GREEN).move_to([c2, de.get_y(), 0])
            ids = [de.id, aes[0].id]
            self.play(*recolor(ids, YELLOW), *flash(ids), run_time=1.4)
            c.wait_until("list has any")
            self.play(*appear(true), run_time=1.0)

            c.wait_until("byid")
            others = [e.id for e in aes[1:]]
            self.play(*recolor(others, FG), *flash(ids, color=GREEN), run_time=1.4)
            c.wait_until("names give")
            names = [de.name] + [e.name for e in aes]
            tag = T("names: also 165 today", 30, DIM).move_to([card.get_x(), -2.75, 0])
            self.play(*recolor(others + ids, DIM), *recolor(names[1:2] + names[0:1], YELLOW),
                      *recolor(names[2:], FG), *during(appear(tag), 0.4, 1.0), run_time=1.5)

            c.wait_until("only by luck")
            ntag_t = T("John Morris", 30, RED)
            ntag = VGroup(RoundedRectangle(corner_radius=0.15, width=ntag_t.width + 0.5,
                                           height=ntag_t.height + 0.35).set_stroke(RED, 2.5), ntag_t)
            ntag_t.move_to(ntag[0])
            ntag.move_to([card.get_x(), 1.5, 0])
            ppl = []
            for k, pid in enumerate(["nm0606657", "nm0606658"]):
                ic = person_icon()
                lab = Mono(pid, 28, DIM).next_to(ic, DOWN, buff=0.2)
                ppl.append(VGroup(ic, lab).move_to([card.get_x() + (k - 0.5) * 2.35, -0.3, 0]))
            ties = [Line(ntag.get_bottom(), p[0].get_top() + 0.08 * UP, stroke_width=3, color=RED) for p in ppl]
            self.play(*during(disappear(card, *pulls), 0, 0.4),
                      *during(appear(ntag, shift=None), 0.45, 0.75),
                      *during([Create(t) for t in ties] + appear(*ppl, shift=None, lag=0.3), 0.6, 1.0),
                      run_time=1.8)

            c.wait_until("query2")
            q = Code(Q2, Q2_SIZE)
            q.move_to([0, Q_TOP - q.height / 2, 0])
            sweep_clear(self, *appear(q, shift=None), run_time=1.2)

            # result rows
            tx, yx = -5.0, 0.4
            head = VGroup(Mono("title", 28, DIM).move_to([tx, 0.65, 0], aligned_edge=LEFT),
                          Mono("year", 28, DIM).move_to([yx, 0.65, 0], aligned_edge=LEFT))
            rows, tags = [], []
            for k, (ti, yr, who) in enumerate(RES2):
                y = 0.05 - 0.6 * k
                col = YELLOW if k == 0 else FG
                a = T(ti, 32, col).move_to([tx, y, 0], aligned_edge=LEFT)
                b = T(yr, 32, GOLD).move_to([yx, y, 0], aligned_edge=LEFT)
                rows.append(VGroup(a, b))
                tt = T(who, 28, DIM)
                pill = RoundedRectangle(corner_radius=0.12, width=tt.width + 0.36,
                                        height=0.46).set_stroke(DIM, 1.5).move_to(tt)
                tags.append(VGroup(pill, tt).move_to([2.2, y, 0], aligned_edge=LEFT))
            dots = T("…", 32, DIM).move_to([tx, 0.05 - 0.6 * 4, 0], aligned_edge=LEFT)
            n165 = T("165 rows", 36, GOLD).move_to([tx, -3.1, 0], aligned_edge=LEFT)
            c.wait_until("result2")
            self.play(*appear(head, shift=None), *appear(n165), run_time=1.0)
            c.wait_until("the first")
            self.play(*appear(*rows, dots, lag=0.3), run_time=1.8)   # early: rows read in the next lines
            c.wait_until("keaton")
            self.play(*appear(*tags, lag=0.4), run_time=2.2)   # early: tags are named as a pair at the end
