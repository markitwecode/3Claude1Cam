"""Chapter 9, scene 6: Exercise 15, an index is redundancy too. Clips c9.index.1 – c9.index.5.

Exports (static, no updaters):
    recap_r6() -> VGroup at ORIGIN (~13.2 x 6.2): the logical/physical line (DIM) with its two labels,
        the BLUE movies card (title | year) above it and the index movies_by_year (sorted keys) beneath
        it. Parts: .line .logical .physical .table .index (.index.frames .index.keys .index.label).
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

SCH = load_scene("ch1_s2_schema")
TW = load_scene("ch4_s5_shape")
UPD = load_scene("ch5_s3_update")
S1 = load_scene("ch9_s1_intro")

# heap order in the table; the index keeps them sorted
ROWS = [["The General", "1926"], ["The Kid", "1921"], ["The Gold Rush", "1925"], ["Sherlock Jr.", "1924"]]
SORTED = ["1921", "1924", "1925", "1926"]
KID = 1
FS, PITCH, KEY_W = 28, 0.58, 1.3
TABLE_LEFT, TABLE_TOP = -4.4, 2.2
LINE_Y = -0.8

CREATE = "CREATE INDEX movies_by_year ON movies (year);"
DROP = "DROP INDEX movies_by_year;"
QUERY = "SELECT title FROM movies\nWHERE year = 1921;"
SQL_DIR = """SELECT p.name
FROM has_position AS hp
JOIN people AS p
  ON p.person_id = hp.person_id
WHERE hp.movie_id = 'tt0012349'
  AND hp.position = 'director';"""
DOC_DIR = """SELECT movie->>'$.directors[*].name'
FROM movies
WHERE movie_id = 'tt0012349';"""
INDEX_SRC = """-- Make an index to efficiently find movies by year
CREATE INDEX movies_by_year ON movies (year);"""
DRIFT_DOC = '{"directors": [{"name": "Charles Chaplin"}]}'


# ══ helpers ════════════════════════════════════════════════════════════════════

def movies_table():
    t = SCH.RowTable("movies", ["title", "year"], ROWS, [[FG, FG] for _ in ROWS], size=FS, pad=0.16, pitch=PITCH)
    box = t.frame[0]
    t.shift([TABLE_LEFT - box.get_left()[0], TABLE_TOP - box.get_top()[1], 0])
    return t


def index_mob(table):
    frames, keys = VGroup(), VGroup()
    for k, y in enumerate(SORTED):
        r = Rectangle(width=KEY_W, height=PITCH).set_stroke(BLUE, 2).set_fill(BLUE, 0.08)
        r.move_to([-6.6 + KEY_W / 2, table.rows[k].get_y(), 0])
        frames.add(r)
        keys.add(Mono(y, FS, FG).move_to(r))
    label = Mono("movies_by_year", FS, BLUE, weight=BOLD)
    label.next_to(frames, DOWN, buff=0.2).align_to(frames, LEFT)
    g = VGroup(frames, keys, label)
    g.frames, g.keys, g.label = frames, keys, label
    return g


def index_arrows(table, idx):
    out = VGroup()
    left = table.frame[0].get_left()[0]
    for k, y in enumerate(SORTED):
        r = next(i for i, row in enumerate(ROWS) if row[1] == y)
        a = Arrow(idx.frames[k].get_right(), [left, table.rows[r].get_y(), 0], buff=0.08,
                  stroke_width=3, color=BLUE, tip_length=0.16)
        out.add(a)
    return out


def index_below(idx, table):
    """Rearrange idx (in place) as a horizontal key row under the table, label above the keys."""
    cx = table.frame[0].get_x()
    for k in range(4):
        idx.frames[k].move_to([cx + (k - 1.5) * KEY_W, LINE_Y - 1.25, 0])
        idx.keys[k].move_to(idx.frames[k])
    idx.label.next_to(idx.frames, UP, buff=0.2)
    idx.label.set_x(cx)
    return idx


def level_labels():
    logical = T("logical: the data queries see", 30, t2c={"the data queries see": DIM})
    physical = T("physical: how the bytes are stored", 30, t2c={"how the bytes are stored": DIM})
    logical.next_to([6.6, LINE_Y, 0], UP, buff=0.2).align_to([6.6, 0, 0], RIGHT)
    physical.next_to([6.6, LINE_Y, 0], DOWN, buff=0.2).align_to([6.6, 0, 0], RIGHT)
    return logical, physical


def level_line():
    return Line([-6.6, LINE_Y, 0], [6.6, LINE_Y, 0]).set_stroke(DIM, 3)


TWB_SIZE = 18
KID_BIG = '{ "title": "The Kid",\n  "actors": [{\n    "name": "Charles Chaplin" }] }'
CHAP_BIG = '{ "name": "Charles Chaplin",\n  "acted_in": [{\n    "title": "The Kid",\n    "year": 1921 }] }'


def two_way_big():
    """ch4 s5's two copies (The Kid / Chaplin), cut to the copied facts and stacked to fit one column."""
    k = TW.D.doc_card(KID_BIG, size=TWB_SIZE)
    c = TW.D.doc_card(CHAP_BIG, size=TWB_SIZE)
    TW._plain(k.code)
    TW._plain(c.code)
    c.next_to(k, DOWN, buff=0.3)
    k.shift(LEFT * 0.35)
    c.shift(RIGHT * 0.35)
    g = VGroup(k, c)
    g.kid, g.chap = k, c
    g.name_k = k.code.find('"Charles Chaplin"')
    g.name_c = c.code.find('"Charles Chaplin"')
    g.title_c = c.code.find('"The Kid"')
    g.year_c = c.code.find("1921")
    return g


def stopwatch(r=0.3, color=GOLD):
    face = Circle(radius=r).set_stroke(color, 4)
    knob = Rectangle(width=0.16, height=0.1).set_fill(color, 1).set_stroke(width=0)
    knob.next_to(face, UP, buff=0.03)
    hand = Line(ORIGIN, UP * r * 0.72).set_stroke(color, 4)
    g = VGroup(face, knob, hand)
    g.face, g.hand = face, hand
    return g


def result_table(value):
    t = SCH.RowTable(None, ["title"], [[value]], [[FG]], size=FS, pad=0.2, pitch=PITCH)
    return t


def recap_r6():
    table = movies_table()
    table.shift(UP * 0.7)
    idx = index_below(index_mob(table), table)
    line = level_line()
    logical, physical = level_labels()
    g = VGroup(line, logical, physical, table, idx)
    g.line, g.logical, g.physical, g.table, g.index = line, logical, physical, table, idx
    g.move_to(ORIGIN)
    return g


# ══ scene ══════════════════════════════════════════════════════════════════════

class IndexRedundancy(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c9.index.1
    def clip1(self):
        with self.say("c9.index.1", gap=0.9) as c:
            row = S1.ex_row()
            self.play(FadeIn(row), run_time=0.5)  # early: s1's row of exercise cards, recalled whole
            card = S1.big_card(15)
            card.shift(UP * (3.5 - card.get_top()[1]))
            code = Code(INDEX_SRC, 28).next_to(card, DOWN, buff=0.4)
            hint = card.hint.next_to(code, DOWN, buff=0.45)
            pause = card.pause
            others = [row.cards[n] for n in (13, 14, 16)]
            src = row.cards[15]
            rt = min(1.8, c.until("an index is"))
            self.play(*during(disappear(*others, src.head, src.title), 0, 0.4), ReplacementTransform(src.box.copy(), card.box), *during(appear(card.text, shift=None), 0.55, 1.0), run_time=rt)  # early: the exercise card, read whole
            self.remove(*src.get_family())
            c.wait_until("values")
            self.play(*appear(code, shift=None), run_time=min(1.2, c.until("again")))
            c.wait_until("again in the index")
            self.play(FlashUnder(code.find("(year)"), color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("consider")
            self.play(*appear(hint, shift=None), run_time=min(1.0, c.until("consistency")))  # early: the hint list, walked next
            for cue, h, nxt in zip(["consistency", "reads", "queries"], hint, ["reads", "queries", "stop"]):
                c.wait_until(cue)
                self.play(*recolor(h, YELLOW), run_time=min(0.8, c.until(nxt)))
            c.wait_until("stop")
            self.play(FadeIn(pause, scale=0.8), run_time=0.8)

    # ------------------------------------------------------------ c9.index.2
    def clip2(self):
        with self.say("c9.index.2") as c:
            table = movies_table()
            idx = index_mob(table)
            arrows = index_arrows(table, idx)
            tw = two_way_big()
            tw.move_to([3.6, 0, 0]).shift(UP * (2.95 - tw.get_top()[1]))
            h_idx = T("index", 40, BLUE).move_to([-3.2, 3.35, 0])
            h_den = T("denormalised", 40, TEAL).move_to([3.6, 3.35, 0])
            self.table, self.idx, self.arrows, self.tw = table, idx, arrows, tw
            rt = min(2.0, c.until("copy"))
            sweep_clear(self, *during(appear(h_idx, table, shift=None), 0.5, 0.8),
                        *during(appear(idx, arrows, shift=None), 0.65, 0.9),
                        *during(appear(h_den, tw, shift=None), 0.75, 1.0), run_time=rt)  # early: the two columns, shown whole

            # {copy}
            cap_l = T("a second copy", 30, GOLD).move_to([-3.4, -1.65, 0])
            cap_r = T("a second copy", 30, GOLD).move_to([3.6, -1.65, 0])
            c.wait_until("copy")
            self.play(*recolor(idx.keys, GOLD), *recolor([tw.name_k, tw.title_c, tw.year_c], GOLD),
                      run_time=min(1.2, c.until("second")))
            c.wait_until(own_word=cap_l)
            self.play(*appear(cap_l, cap_r, lag=0), run_time=min(1.0, c.until("reads")))

            # {reads}
            c.wait_until("reads")
            kid_key = SORTED.index("1921")
            path = arrows[kid_key].copy().set_color(YELLOW)
            self.play(VShowPassingFlash(path, time_width=0.6), arrows[kid_key].animate.set_color(YELLOW),
                      *recolor(table.rows[KID], YELLOW), run_time=1.0)
            c.wait_until("document")
            self.play(FlashAround(tw.kid, color=TEAL, time_width=1.5), run_time=min(1.4, c.until("writes")))

            # {writes}
            c.wait_until("writes")
            kid_year = table.cell(KID, 1)
            targets = [kid_year, idx.keys[kid_key], tw.name_k, tw.name_c]
            dots = [Dot(t.get_center(), radius=0.11, color=YELLOW) for t in targets]
            starts = [[-1.9, 3.35, 0], [-1.9, 3.35, 0], [1.4, 2.6, 0], [1.4, 2.6, 0]]
            self.play(*[FadeIn(d, target_position=s) for d, s in zip(dots, starts)],
                      arrows[kid_key].animate.set_color(BLUE), *recolor(table.rows[KID], FG),
                      run_time=min(1.2, 0.4 * c.until("derived")))
            x2_l = T("×2", 44, GOLD).move_to(cap_l)
            x2_r = T("×2", 44, GOLD).move_to(cap_r)
            self.play(*[FadeOut(d, scale=2.5) for d in dots],
                      *swap(cap_l, x2_l), *swap(cap_r, x2_r), run_time=min(1.2, c.until("derived")))
            self.caps = [x2_l, x2_r]

            # {derived}
            create = Code(CREATE, 30).move_to([0, -3.25, 0])
            drop = Code(DROP, 30).next_to(create, UP, buff=0.25).align_to(create, LEFT)
            c.wait_until("drop the index")
            self.play(*disappear(idx, arrows), *appear(drop, shift=None),
                      run_time=min(1.2, c.until("rebuilds")))
            c.wait_until("rebuilds")
            years = VGroup(*[table.cell(i, 1) for i in range(4)])
            for k in idx.keys:
                k.set_color(GOLD)
            rt = min(2.0, c.until(None))
            self.play(*during(appear(create, shift=None), 0, 0.6), FlashAround(years, color=GOLD, time_width=1.5),
                      *during(appear(idx, arrows, shift=None, lag=0.1), 0.4, 1.0), run_time=rt)
            self.code = VGroup(drop, create)

    # ------------------------------------------------------------ c9.index.3
    def clip3(self):
        table, idx, arrows, tw = self.table, self.idx, self.arrows, self.tw
        drop_c, create_c = self.code
        with self.say("c9.index.3") as c:
            sweep_clear(self, *during([table.animate.shift(UP * 0.7), idx.animate.shift(UP * 0.7),
                                       tw.animate.shift(UP * 0.5)], 0.45, 1.0),
                        keep=[table, idx, tw, drop_c, create_c], run_time=min(1.8, c.until("one picture")))
            line = level_line()
            logical, physical = level_labels()
            c.wait_until("one picture")
            self.play(GrowFromCenter(line), run_time=min(1.2, c.until("logical")))
            c.wait_until(own_word=logical)
            self.play(*appear(logical), run_time=1.0)
            c.wait_until(own_word=physical)
            self.play(*appear(physical), run_time=1.0)
            term = T("data independence", 40, YELLOW).move_to([3.4, -2.6, 0])
            c.wait_until("data independence")
            self.play(*during(disappear(drop_c, create_c), 0, 0.45), *during(appear(term), 0.45, 1.0), run_time=1.4)
            self.play(FlashUnder(term, color=YELLOW, run_time=1.2, time_width=1.5))

            # {below}
            c.wait_until("below")
            tgt = index_below(idx.copy(), table)
            moves = [f.animate.move_to(t) for f, t in zip(idx.frames, tgt.frames)]
            moves += [k.animate.move_to(t) for k, t in zip(idx.keys, tgt.keys)]
            old_lab, new_lab = idx.label, tgt.label
            self.play(*during(FadeOut(old_lab), 0, 0.25), *during(moves, 0.25, 0.8),
                      *during(FadeIn(new_lab), 0.8, 1.0), run_time=min(1.8, c.until("above")))
            idx.remove(old_lab)
            idx.add(new_lab)
            idx.label = new_lab
            settle(self, idx)
            # {above}
            c.wait_until("above")
            self.play(FlashAround(tw.kid, color=TEAL, time_width=1.5),
                      FlashAround(tw.chap, color=TEAL, time_width=1.5), run_time=1.5)
            self.line, self.logical, self.physical, self.term = line, logical, physical, term

    # ------------------------------------------------------------ c9.index.4
    def clip4(self):
        table, idx, tw = self.table, self.idx, self.tw
        with self.say("c9.index.4") as c:
            q = T("Who keeps the copies consistent?", 32, YELLOW).move_to(self.term)
            self.play(*swap(self.term, q), run_time=min(1.2, c.until("dbms")))

            # {dbms}
            top = table.frame[0].get_top()[1]
            bot = idx.frames.get_bottom()[1]
            x = min(table.frame[0].get_left()[0], idx.frames.get_left()[0]) - 0.12
            brace = Brace(Line([x, top, 0], [x, bot, 0]), direction=LEFT, color=GREEN)
            one = T("one\nwrite", 32, GREEN).next_to(brace, LEFT, buff=0.15)
            kid_key = SORTED.index("1921")
            c.wait_until("same write")
            self.play(FlashAround(table.rows[KID], color=YELLOW, time_width=1.5),
                      FlashAround(idx.frames[kid_key], color=YELLOW, time_width=1.5),
                      GrowFromCenter(brace), run_time=1.4)
            self.play(*appear(one), run_time=min(1.0, c.until("app")))

            # {app}
            fan = UPD.recap_r2()
            del fan.update   # recap_r2 stores its UPDATE label as .update, shadowing Mobject.update
            fan.bad.set_stroke(TEAL, 2.5).set_fill(TEAL, 0.08)
            fan.scale(0.68)
            app_box = SurroundingRectangle(fan.left, buff=0.22, corner_radius=0.12).set_stroke(DIM, 2)
            app_lab = T("application", 28, DIM).next_to(app_box, UP, buff=0.12)
            fan_g = VGroup(fan, app_box, app_lab).move_to([3.6, 1.15, 0])
            c.wait_until("app")
            self.play(*swap(tw, fan_g), run_time=min(1.4, c.until("find every")))
            c.wait_until("find every")
            good = [cd for i, cd in enumerate(fan.copies) if i != 5]
            self.play(FlashAround(fan.row, color=YELLOW, time_width=1.5),
                      LaggedStart(*[FlashAround(cd, color=YELLOW, time_width=1.5) for cd in good],
                                  lag_ratio=0.25),
                      run_time=min(2.2, c.until("misses")))
            c.wait_until("misses")
            self.play(fan.bad.animate.set_stroke(RED, 2.5).set_fill(RED, 0.15), run_time=1.0)
            c.wait_until("drift")
            self.play(FlashAround(fan.bad, color=RED, time_width=1.5), run_time=min(1.2, c.until(None)))

    # ------------------------------------------------------------ c9.index.5
    def clip5(self):
        with self.say("c9.index.5", gap=1.8) as c:
            q_l = Code(QUERY, 28).move_to([-3.5, 0.45, 0])
            r_l = result_table("The Kid").move_to([-3.5, -1.6, 0])
            cap_l = T("without the index", 30, DIM).move_to([-3.5, 1.6, 0])
            sweep_clear(self, *during(appear(cap_l, q_l, r_l, shift=None, lag=0.2), 0.5, 1.0),
                        run_time=min(1.8, c.until("create")))  # early: the query panel, read whole

            # {create}
            create = Code(CREATE, 30).move_to([0, 2.95, 0])
            cap_r = T("with the index", 30, DIM).move_to([3.5, 1.6, 0])
            q_r = Code(QUERY, 28).move_to([3.5, 0.45, 0])
            r_r = result_table("The Kid").move_to([3.5, -1.6, 0])
            c.wait_until("create")
            self.play(*appear(create, cap_r, shift=None, lag=0.3), run_time=min(1.4, c.until("this query")))
            c.wait_until("this query")
            self.play(*fly(q_l, q_r), run_time=min(1.5, c.until("returns")))
            c.wait_until("returns")
            self.play(*fly(r_l, r_r), run_time=min(1.5, c.until("the kid")))
            eq = MathTex("=", font_size=96, color=GREEN).move_to([0, -0.55, 0])
            c.wait_until("the kid")
            self.play(GrowFromCenter(eq), *flash([r_l.rows[0], r_r.rows[0]], color=GREEN, time_width=1.5),
                      run_time=1.2)

            # {speed}
            sw = stopwatch().next_to(cap_r, RIGHT, buff=0.35)
            c.wait_until("speed")
            self.play(FadeIn(sw, scale=0.6), run_time=0.8)
            self.play(Rotate(sw.hand, angle=-2 * PI, about_point=sw.face.get_center()),
                      rate_func=linear, run_time=min(1.4, c.until("docs")))

            # {docs}
            sql = Code(SQL_DIR, 26)
            sql.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT).align_to([0, 3.55, 0], UP)
            sql_box = SurroundingRectangle(sql, buff=0.18, corner_radius=0.1).set_stroke(BLUE, 2.5)
            doc = Code(DOC_DIR, 26)
            doc.align_to([-6.3, 0, 0], LEFT).align_to([0, 0.12, 0], UP)
            doc_box = SurroundingRectangle(doc, buff=0.18, corner_radius=0.1).set_stroke(TEAL, 2.5)
            res_b = Mono("Charles Chaplin", 30).move_to([4.6, sql.get_y(), 0])
            res_t = Mono("[Charles Chaplin]", 30).move_to([4.6, doc.get_y(), 0])
            ar_b = Arrow([sql_box.get_right()[0] + 0.1, res_b.get_y(), 0], [res_b.get_left()[0] - 0.1, res_b.get_y(), 0],
                         buff=0, stroke_width=3, color=BLUE, tip_length=0.18)
            ar_t = Arrow([doc_box.get_right()[0] + 0.1, res_t.get_y(), 0], [res_t.get_left()[0] - 0.1, res_t.get_y(), 0],
                         buff=0, stroke_width=3, color=TEAL, tip_length=0.18)
            c.wait_until("docs")
            sweep_clear(self, *during(appear(sql_box, sql, shift=None, lag=0.1), 0.5, 0.85),
                        *during(appear(ar_b, res_b, shift=None), 0.75, 1.0), run_time=min(2.0, c.until("you read")))
            c.wait_until("you read")
            self.play(*appear(doc_box, doc, shift=None, lag=0.1), run_time=1.2)
            self.play(GrowArrow(ar_t), *appear(res_t, shift=None), run_time=min(1.0, c.until("drift")))
            eq2 = MathTex("=", font_size=72, color=GREEN).move_to([4.6, (res_b.get_y() + res_t.get_y()) / 2, 0])
            self.play(GrowFromCenter(eq2), run_time=min(0.8, c.until("drift")))

            # {drift}
            dcode = Code(DRIFT_DOC, 26, lang="json")
            dcard = SurroundingRectangle(dcode, buff=0.18, corner_radius=0.1).set_stroke(TEAL, 2.5)
            dg = VGroup(dcard, dcode).move_to([-0.6, -2.95, 0])
            dlab = T("if a copy drifted", 28, DIM).next_to(dg, UP, buff=0.15).align_to(dg, LEFT)
            neq = MathTex(r"\neq", font_size=72, color=RED).move_to(eq2)
            c.wait_until("drift")
            self.play(*appear(dlab, dcard, dcode, shift=None, lag=0.15), run_time=1.0)  # early: drift caption with its card
            name = dcode.find("Charles Chaplin")
            self.play(*recolor(name, RED), *recolor(res_t, RED), *swap(eq2, neq),
                      run_time=min(1.2, c.until(None)))
