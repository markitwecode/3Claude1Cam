"""Chapter 6, scene 5: when reading-time schemas win, and what they cost. Clips c6.trade.1 – c6.trade.3.

Exports (import with `T5 = load_scene("ch6_s5_tradeoff")`; all static, built at ORIGIN):
    T5.mistake_docs(highlight=True)  # VGroup of the four {spell}/{string} documents (doc_card look,
                                     #   json size 28), stacked left-aligned: .docs[i] (DocCard
                                     #   .frame .code), .keys[i] (key glyphs, YELLOW if highlight),
                                     #   .quoted (glyphs of "1889" in docs[3]); ~11.2 x 3.6
    T5.recap_thumb()                 # the three product documents in their `products` table and the
                                     #   query result with the PINK NULL for birth_year; no caption
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

D = load_scene("ch4_s3_movie")
SCH = load_scene("ch1_s2_schema")
S4 = load_scene("ch6_s4_schema")

# ---------------------------------------------------------------- products
BOOK = '{"type": "book",\n "title": "My Autobiography",\n "author": "Charles Chaplin"}'
SHOE = '{"type": "shoe",\n "name": "Walking boot",\n "size": 42}'
TV = '{"type": "tv",\n "name": "Cinema 55",\n "resolution": "3840x2160"}'


def products_docs(size=28):
    docs = [D.doc_card(s, size=size, pad=0.2) for s in (BOOK, SHOE, TV)]
    col = VGroup(*docs).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.16, width=col.width + 0.6, height=col.height + 0.6)
    frame.set_stroke(TEAL, 2.5).set_fill(BG, 0).move_to(col)
    label = Mono("products", 30, TEAL, weight=BOLD)
    label.next_to(frame, UP, buff=0.15).align_to(frame, LEFT)
    g = VGroup(frame, label, *docs)
    g.frame, g.label, g.docs = frame, label, docs
    return g


class ProdCard(VGroup):
    """ch1 s2's TableCard look for a product table."""

    def __init__(self, name, cols, w=3.0, hdr=0.56, pitch=0.44, pad_b=0.14):
        super().__init__()
        h = hdr + len(cols) * pitch + pad_b
        top = h / 2
        self.box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.header = Rectangle(width=w, height=hdr).set_stroke(BLUE, 0).set_fill(BLUE, 0.35)
        self.header.move_to([0, top - hdr / 2, 0])
        self.divider = Line([-w / 2, top - hdr, 0], [w / 2, top - hdr, 0]).set_stroke(BLUE, 2)
        self.title, _ = SCH._placed(name, 30, FG, BOLD, top - hdr / 2, cx=0)
        self.rows = []
        ul = []
        for i, c in enumerate(cols):
            t, bot = SCH._placed(c, 28, FG, NORMAL, top - hdr - pitch * (i + 0.5) - 0.02, left=-w / 2 + 0.24)
            self.rows.append(t)
            if i == 0:
                ul.append(Line([t.get_left()[0], bot + 0.02, 0], [t.get_right()[0], bot + 0.02, 0])
                          .set_stroke(FG, 2.5))
        self.add(self.header, self.box, self.divider, self.title, *self.rows, *ul)


def type_cards():
    cards = [ProdCard("books", ["product_id", "title", "author"]),
             ProdCard("shoes", ["product_id", "name", "size"]),
             ProdCard("tvs", ["product_id", "name", "resolution"])]
    return VGroup(*cards).arrange(RIGHT, buff=0.4)


WIDE_COLS = ["product_id", "type", "title", "author", "name", "size", "resolution"]
WIDE_VALS = [["1", "book", "My Autobiography", "Charles Chaplin", "NULL", "NULL", "NULL"],
             ["2", "shoe", "NULL", "NULL", "Walking boot", "42", "NULL"],
             ["3", "tv", "NULL", "NULL", "Cinema 55", "NULL", "3840x2160"]]


class WideCard(VGroup):
    """The one wide products table as a schema card (columns listed down, ch1 s2 style), each
    product's row standing beside the column names; NULL PINK."""

    def __init__(self, hdr=0.56, pitch=0.44, pad_b=0.14, name_w=2.85, pad=0.2):
        super().__init__()
        n = len(WIDE_COLS)
        vw = [max(Mono(v, 28).width for v in r) + 2 * pad for r in WIDE_VALS]
        w = name_w + sum(vw)
        h = hdr + n * pitch + pad_b
        top, left = h / 2, -w / 2
        self.box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.header = Rectangle(width=w, height=hdr).set_stroke(BLUE, 0).set_fill(BLUE, 0.35)
        self.header.move_to([0, top - hdr / 2, 0])
        self.divider = Line([left, top - hdr, 0], [-left, top - hdr, 0]).set_stroke(BLUE, 2)
        self.title, _ = SCH._placed("products", 30, FG, BOLD, top - hdr / 2, left=left + 0.24)
        xs = [left + name_w + sum(vw[:j]) for j in range(len(vw))]
        self.vlines = [Line([x, top, 0], [x, -top, 0]).set_stroke(DIM if j else BLUE, 1.5 if j else 2)
                       for j, x in enumerate(xs)]
        self.names, self.vals, ul = [], [], []
        for i, c in enumerate(WIDE_COLS):
            y = top - hdr - pitch * (i + 0.5) - 0.02
            t, bot = SCH._placed(c, 28, FG, NORMAL, y, left=left + 0.24)
            self.names.append(t)
            if i == 0:
                ul.append(Line([t.get_left()[0], bot + 0.02, 0], [t.get_right()[0], bot + 0.02, 0])
                          .set_stroke(FG, 2.5))
        for j, r in enumerate(WIDE_VALS):
            col = []
            for i, v in enumerate(r):
                y = top - hdr - pitch * (i + 0.5) - 0.02
                t, _ = SCH._placed(v, 28, PINK if v == "NULL" else FG, NORMAL, y, left=xs[j] + pad)
                col.append(t)
            self.vals.append(col)
        self.add(self.header, self.box, self.divider, *self.vlines, self.title, *self.names, *ul,
                 *[t for col in self.vals for t in col])


def wide_table():
    return WideCard()


def ghost(key):
    k = Mono(key, 28, RED).set_opacity(0.45)
    q = Mono("?", 40, RED, weight=BOLD)
    return VGroup(k, q).arrange(RIGHT, buff=0.18)


# ---------------------------------------------------------------- people migration
PEOPLE_ROWS = [["nm0000002", "Lauren Bacall"], ["nm0000004", "John Belushi"],
               ["nm0000005", "Ingmar Bergman"], ["nm0000006", "Ingrid Bergman"],
               ["nm0000007", "Humphrey Bogart"]]
VDOTS = "⋮"


def people_tables():
    rows2 = [r for r in PEOPLE_ROWS] + [[VDOTS, VDOTS]]
    rows3 = [r + [r[1].split(" ")[0]] for r in PEOPLE_ROWS] + [[VDOTS, VDOTS, VDOTS]]
    c2 = [[DIM, FG] for _ in rows2]
    c3 = [[DIM, FG, YELLOW] for _ in rows3]
    narrow = SCH.RowTable("people", ["person_id", "name"], rows2, c2, size=28, pitch=0.54)
    wide = SCH.RowTable("people", ["person_id", "name", "first_name"], rows3, c3, size=28, pitch=0.54)
    shift = np.array([-wide.frame.get_center()[0], -0.62 - wide.frame.get_center()[1], 0])
    narrow.shift(shift)
    wide.shift(shift)
    return narrow, wide


ALTER = "ALTER TABLE people ADD COLUMN first_name TEXT;"
UPDATE = "UPDATE people\nSET first_name = split_part(name, ' ', 1);"

OLD_DOC = '{"person_id": "nm0000122",\n "name": "Charles Chaplin"}'
NEW_DOC = '{"person_id": "nm0001067",\n "first_name": "Jackie",\n "last_name": "Coogan"}'
READER = '''def first_name(person):
    if "first_name" in person:
        return person["first_name"]
    return person["name"].split(" ")[0]'''

# ---------------------------------------------------------------- mistakes
MISTAKES = ['{"name": "Charles Chaplin", "birthyear": 1889}',
            '{"name": "Jackie Coogan", "birthYear": 1914}',
            '{"name": "Edna Purviance", "birth_year": 1895}',
            '{"name": "Charles Chaplin", "birthyear": "1889"}']
KEYS = ['"birthyear"', '"birthYear"', '"birth_year"', '"birthyear"']


def mistake_docs(highlight=True):
    docs = [D.doc_card(s, size=28) for s in MISTAKES]
    g = VGroup(*docs).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(ORIGIN)
    keys = [d.code.find(k) for d, k in zip(docs, KEYS)]
    if highlight:
        for k in keys:
            k.set_color(YELLOW)
    g.docs, g.keys = docs, keys
    g.quoted = docs[3].code.find('"1889"')
    return g


QUERY = """SELECT person->>'name' AS name,
       person->>'birthyear' AS birthyear,
       person->>'birth_year' AS birth_year
FROM   people
WHERE  person_id = 'nm0000122';"""


def result_table():
    t = SCH.RowTable(None, ["name", "birthyear", "birth_year"], [["Charles Chaplin", "1889", "NULL"]],
                     [[FG, FG, PINK]], size=30, pitch=0.62)
    t.frame[0].set_stroke(TEAL)
    t.frame[1].set_stroke(TEAL)
    return t


def recap_thumb():
    p = products_docs()
    r = result_table().scale(1.1)
    r.next_to(p, RIGHT, buff=1.0)
    return VGroup(p, r).move_to(ORIGIN)


# ---------------------------------------------------------------- scene
class Ch6S5Tradeoff(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c6.trade.1") as c:
            q = T("When does checking on read win?", 44).move_to([0, 0.3, 0])
            self.play(*appear(q), run_time=1.0)
            c.wait_until("shop")
            P = products_docs()
            P.shift(np.array([-6.6 - P.frame.get_left()[0], 3.05 - P.frame.get_top()[1], 0]))
            book, shoe, tv = P.docs
            self.play(*during(disappear(q), 0, 0.3), *during([FadeIn(P.frame)], 0.3, 0.6),
                      *during(appear(P.label, book, shoe, tv, lag=0.45), 0.3, 1),
                      run_time=min(3.0, c.until("attrs") - 0.2))
            # a TV's resolution means nothing for a shoe
            c.wait_until("resolution")
            res = tv.code.find('"resolution"')
            self.play(*recolor(res, YELLOW), FlashAround(res, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("nothing")
            g1 = ghost('"resolution"').next_to(P.frame, RIGHT, buff=0.4).set_y(shoe.get_y())
            self.play(*appear(g1, shift=None), run_time=min(1.0, c.until("a shoe has")))
            c.wait_until("size")
            siz = shoe.code.find('"size"')
            self.play(*recolor(siz, YELLOW), FlashAround(siz, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("nothing", nth=1)
            g2 = ghost('"size"').next_to(P.frame, RIGHT, buff=0.4).set_y(tv.get_y())
            self.play(*appear(g2, shift=None), run_time=min(1.0, c.until("json")))
            # documents: one table, each with its own keys
            c.wait_until("json")
            self.play(FlashAround(P.frame, color=TEAL, run_time=1.6, time_width=1.5), run_time=1.6)
            # relationally: a table per type, or one wide table
            c.wait_until("tables")
            cards = type_cards()
            cards.move_to([0, 3.5 - cards.height / 2, 0])
            self.play(*during(disappear(P, g1, g2), 0, 0.4),
                      *during(appear(*cards, lag=0.3), 0.45, 1), run_time=min(2.0, c.until("or one wide")))
            c.wait_until("or one wide")
            w = wide_table()
            w.move_to([0, 1.0 - w.height / 2, 0])
            self.play(*appear(w), run_time=1.0)

    def clip2(self):
        with self.say("c6.trade.2") as c:
            narrow, wide = people_tables()
            parts = [narrow.label, narrow.frame, narrow.head, *narrow.rows]
            sweep_clear(self, *appear(*parts, lag=0.06))
            # first names on their own
            c.wait_until("first names")
            firsts = []
            for i, (_, name) in enumerate(PEOPLE_ROWS):
                n = len(name.split(" ")[0])
                firsts += list(narrow.cells[i][1][:n])
            self.play(*recolor(firsts, YELLOW), run_time=1.2)
            # the migration
            c.wait_until("alter")
            alter = Code(ALTER, size=28).move_to([0, 3.4, 0])
            upd = Code(UPDATE, size=28)
            upd.next_to(alter, DOWN, buff=0.14, aligned_edge=LEFT)
            self.play(*appear(alter), run_time=1.0)
            c.wait_until("add the column")
            self.play(ReplacementTransform(narrow.frame, wide.frame), *appear(wide.head[2]),
                      run_time=1.2)
            c.wait_until("then rewrite")
            self.play(*appear(upd), run_time=1.0)
            # sweep down every row
            lab_at = max(0.0, c.until("twenty-three thousand"))
            Tb = max(1.5, c.until("on a huge table") - 0.5)   # sweep done as "...of them" ends
            T_ = max(Tb + 0.5, lab_at + 1.0)
            pitch = 0.54
            y0 = wide.cells[0][0].get_y()
            bar = Rectangle(width=wide.frame.width - 0.06, height=pitch - 0.04).set_stroke(width=0)
            bar.set_fill(YELLOW, 0.18).set_z_index(-1)
            bar.move_to([wide.frame.get_center()[0], wide.rows[0].get_y(), 0])
            last_y = wide.rows[-1].get_y()
            self.add(bar)
            n = len(wide.rows)
            anims = [time_span(bar.animate(rate_func=linear).set_y(last_y), 0, Tb)]
            for i in range(n):
                t = Tb * i / (n - 1)
                anims.append(time_span(FadeIn(wide.cells[i][2]), t, t + 0.5))
            gold = T("23,179 rows rewritten", 40, GOLD)
            gold.next_to(wide.frame, DOWN, buff=0.35)
            anims.append(time_span(FadeIn(gold, shift=0.2 * DOWN), lab_at, lab_at + 1.0))
            self.play(*anims, run_time=T_)
            # documents: just write the new format
            c.wait_until("docs")
            old = D.doc_card(OLD_DOC, size=28, pad=0.15)
            new = D.doc_card(NEW_DOC, size=28, pad=0.15)
            old.move_to([0, 2.95 - old.height / 2, 0]).align_to([-6.62, 0, 0], LEFT)
            new.move_to([0, 2.95 - new.height / 2, 0]).align_to([6.62, 0, 0], RIGHT)
            sweep_clear(self, *appear(old))
            c.wait_until("new documents")
            tag_new = T("new", 30, DIM).next_to(new, UP, buff=0.2)
            self.play(*appear(new, tag_new, lag=0.3), run_time=1.2)
            c.wait_until("both")
            tag_old = T("old", 30, DIM).next_to(old, UP, buff=0.2)
            self.play(*appear(tag_old), run_time=0.8)
            c.wait_until("the code")
            rd = Code(READER, size=28, lang="python").move_to([0.4, -1.6, 0])
            self.play(*appear(rd), run_time=1.0)
            l2, l3 = rd.line(2), rd.line(3)
            a_new = Arrow(l2.get_right() + 0.15 * RIGHT, new.get_bottom() + 0.6 * RIGHT + 0.05 * DOWN,
                          buff=0.1, stroke_width=4, color=YELLOW)
            a_old = CurvedArrow(l3.get_left() + 0.15 * LEFT, old.get_bottom() + 1.6 * LEFT + 0.1 * DOWN,
                                angle=-PI / 3, color=YELLOW, stroke_width=4)
            self.play(GrowArrow(a_new), Create(a_old), run_time=min(1.2, c.until() - 0.1))

    def clip3(self):
        with self.say("c6.trade.3") as c:
            title = T("The price: mistakes are not caught", 44).move_to([0, 3.3, 0])
            c.wait_until("spell")   # documents + reader hold through {cost}
            sweep_clear(self, *appear(title))
            M = mistake_docs()
            M.move_to([-0.5, -0.35, 0])
            for d, cue in zip(M.docs[:3], ("one word", "camel case", "underscore")):
                c.wait_until(cue)
                self.play(*appear(d), run_time=0.9)
            c.wait_until("string")
            self.play(*appear(M.docs[3]), run_time=1.0)
            c.wait_until("in quotes")
            box = token_box(M.quoted, M.docs[3].code, color=GOLD)
            self.play(FadeIn(box), run_time=0.8)
            # accepted ... but wrong
            c.wait_until("accepted")
            ticks = [check_mark().move_to([M.get_right()[0] + 0.6, d.get_y(), 0]) for d in M.docs]
            self.play(*appear(*ticks, shift=None, lag=0.2), run_time=1.1)
            self.wait(0.3)
            rings = [Circle(radius=0.36).set_stroke(RED, 4).move_to(t) for t in ticks]
            self.play(*[GrowFromCenter(r) for r in rings], run_time=min(0.8, c.until("typo")))
            # reading a misspelt key: just NULL
            c.wait_until("typo")
            q = Code(QUERY, size=30).move_to([0, 1.55, 0])
            sweep_clear(self, *appear(q))
            c.wait_until("birth underscore year")
            kb = token_box(q.find("'birth_year'"), q.line(2))
            self.play(FadeIn(kb), run_time=0.8)
            c.wait_until("you just get")
            res = result_table().move_to([0, -1.3, 0])
            self.play(*appear(res), run_time=1.0)
            null = res.cell(0, 2)
            self.play(FlashAround(null, color=PINK, run_time=1.2, time_width=1.5), run_time=1.2)
            # contrast: the relational reply vs the silent NULL
            c.wait_until("contrast")
            rep = S4.birthyear_reply().move_to([0, -1.5, 0])
            tag_rel = T("relational", 30, BLUE).next_to(rep, UP, buff=0.25).align_to(rep, LEFT)
            res.generate_target()
            res.target.move_to([0, 1.6, 0])
            self.play(*during(disappear(q, kb), 0, 0.4), *during([MoveToTarget(res)], 0.4, 0.8),
                      *during(appear(tag_rel, rep, lag=0.2), 0.55, 1), run_time=min(1.8, c.until("the documents")))
            c.wait_until("the documents")
            tag_doc = T("documents", 30, TEAL).next_to(res, UP, buff=0.25).align_to(res, LEFT)
            self.play(*appear(tag_doc), FlashAround(res.cell(0, 2), color=PINK, run_time=1.4, time_width=1.5),
                      run_time=1.4)
