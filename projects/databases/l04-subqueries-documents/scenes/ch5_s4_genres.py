"""Chapter 5, scene 4: losing a genre (deletion anomaly) and never gaining one (insertion anomaly).
Clips c5.genres.1 – c5.genres.4.

Layout: left zone the documents (clip 1-2) then the BLUE genres card (26 rows, two columns of 13);
right zone the TEAL grid "genres in the documents" (23 chips), rows aligned with the card's rows.
The top band (y > 2.3) carries the SQL, the mini rows, the anomaly names and the hovering chip.

Recap thumbnail for s7:
    mod = load_scene("ch5_s4_genres")
    r = mod.recap_r3()      # static VGroup at ORIGIN, ~11.5 x 5.4 (scale it to taste)
    r.blue                  # GenresCard: .box .header .title .rows[genre_id] (VGroup(id, name))
    r.teal                  # VGroup of the 23 TEAL chips (Chip: .rect .label), r.chips[name]
    r.gaps                  # VGroup of the three dashed RED gaps (Epic, Experimental, Gothic)
Data verified on movies.duckdb / movies-json.duckdb (DuckDB 1.5.6): GENRES, EMPTY, DOC_GENRES.
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

GENRES = [(1, "Action"), (2, "Adventure"), (3, "Animation"), (4, "Biography"), (5, "Comedy"),
          (6, "Crime"), (7, "Documentary"), (8, "Drama"), (9, "Epic"), (10, "Experimental"),
          (11, "Family"), (12, "Fantasy"), (13, "Film-Noir"), (14, "Gothic"), (15, "History"),
          (16, "Horror"), (17, "Music"), (18, "Musical"), (19, "Mystery"), (20, "News"),
          (21, "Romance"), (22, "Sci-Fi"), (23, "Sport"), (24, "Thriller"), (25, "War"),
          (26, "Western")]
EMPTY = ("Epic", "Experimental", "Gothic")          # 0 movies (LEFT JOIN has_genre)
DOC_GENRES = [n for _, n in GENRES if n not in EMPTY]   # the 23 distinct names in the documents

PITCH, TOP, HDR = 0.36, 2.2, 0.5
ROW_SIZE, CHIP_SIZE = 22, 24
CARD_L, COL1_L = -6.3, 1.05
CHIP_FILL = "#1B2E2D"          # TEAL at 0.15 over BG, opaque (tethers pass behind chips)


def row_y(r):
    return TOP - HDR - 0.06 - PITCH * (r + 0.5)


def slot(name):
    """(column, row) of a genre in the 26-row layout: column 0 holds ids 1-13, column 1 ids 14-26."""
    if name == "Superhero":
        return 1, 13
    i = [n for _, n in GENRES].index(name)
    return i // 13, i % 13


def placed(make, s, y):
    """Text whose baseline sits on row y (measured with a '|' spanning ascent + descent)."""
    ref = make(s + "|")
    ref.move_to([0, y, 0])
    body = VGroup(*ref[:-1])
    t = make(s)
    t.move_to(body.get_center())
    return t


def mono(size, color=FG, weight=NORMAL):
    return lambda s: Mono(s, size, color=color, weight=weight)


def serif(size, color=FG):
    return lambda s: T(s, size, color=color)


# ── the BLUE genres card (ch1 s2's schema-map look, with its 26 rows) ─────────────────
_ID_W = Mono("26", ROW_SIZE).width
_N1_W = max(Mono(n, ROW_SIZE).width for i, n in GENRES[:13])
_N2_W = max(Mono(n, ROW_SIZE).width for n in [n for _, n in GENRES[13:]] + ["Superhero"])
_CB_L = CARD_L + 0.22 + _ID_W + 0.18 + _N1_W + 0.45     # column B's left edge
CARD_W = (_CB_L - CARD_L) + _ID_W + 0.18 + _N2_W + 0.22
CARD_X = CARD_L + CARD_W / 2


def card_box(n_rows=13):
    h = HDR + 0.06 + n_rows * PITCH + 0.12
    return (Rectangle(width=CARD_W, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
            .move_to([CARD_X, TOP - h / 2, 0]))


def genre_row(gid, name, color=FG):
    col, r = slot(name)
    left = CARD_L + 0.22 if col == 0 else _CB_L
    y = row_y(r)
    i = placed(mono(ROW_SIZE, DIM), str(gid), y)
    i.shift(RIGHT * (left + _ID_W - i.get_right()[0]))
    n = placed(mono(ROW_SIZE, color), name, y)
    n.shift(RIGHT * (left + _ID_W + 0.18 - n.get_left()[0]))
    return VGroup(i, n)


class GenresCard(VGroup):
    def __init__(self):
        super().__init__()
        self.box = card_box(13)
        self.header = (Rectangle(width=CARD_W, height=HDR).set_stroke(BLUE, 0).set_fill(BLUE, 0.35)
                       .move_to([CARD_X, TOP - HDR / 2, 0]))
        self.divider = Line([CARD_L, TOP - HDR, 0], [CARD_L + CARD_W, TOP - HDR, 0]).set_stroke(BLUE, 2)
        self.title = placed(mono(26, FG, BOLD), "genres", TOP - HDR / 2)
        self.title.set_x(CARD_X)
        self.rows = {gid: genre_row(gid, n) for gid, n in GENRES}
        self.add(self.header, self.box, self.divider, self.title, *self.rows.values())


# ── the TEAL chips ─────────────────────────────────────────────────────────────────────
_W1 = max(T(n, CHIP_SIZE).width for _, n in GENRES[:13]) + 0.3
_W2 = max(T(n, CHIP_SIZE).width for _, n in GENRES[13:]) + 0.3
COL2_L = COL1_L + _W1 + 0.2
TEAL_X = (COL1_L + COL2_L + _W2) / 2


def slot_center(col, r):
    return np.array([COL1_L + _W1 / 2 if col == 0 else COL2_L + _W2 / 2, row_y(r), 0])


class Chip(VGroup):
    def __init__(self, name, width=None, color=TEAL):
        super().__init__()
        self.name = name
        self.label = placed(serif(CHIP_SIZE, color), name, 0)
        w = width or self.label.width + 0.3
        self.rect = (RoundedRectangle(corner_radius=0.1, width=w, height=0.3)
                     .set_stroke(color, 1.5).set_fill(CHIP_FILL, 1))
        self.rect.move_to([0, 0, 0])
        self.add(self.rect, self.label)


def chip_at(name, col, r):
    ch = Chip(name, _W1 if col == 0 else _W2)
    ch.move_to(slot_center(col, r))
    return ch


def doc_slots():
    """Initial TEAL layout: each column packed from the top (no visible holes)."""
    out = {}
    for col in (0, 1):
        names = [n for n in DOC_GENRES if slot(n)[0] == col]
        for r, n in enumerate(names):
            out[n] = (col, r)
    return out


def gap_box(name):
    col, r = slot(name)
    w = _W1 if col == 0 else _W2
    g = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=w, height=0.3), num_dashes=22)
    g.set_stroke(RED, 2)
    g.move_to(slot_center(col, r))
    return g


def recap_r3():
    """Static recap thumbnail: the BLUE 26-genre card, the TEAL 23-genre grid in the 26-row layout,
    the three dashed RED gaps. Centred on ORIGIN."""
    blue = GenresCard()
    chips = {n: chip_at(n, *slot(n)) for n in DOC_GENRES}
    teal = VGroup(*chips.values())
    gaps = VGroup(*[gap_box(n) for n in EMPTY])
    g = VGroup(blue, teal, gaps)
    g.shift(-g.get_center())
    g.blue, g.teal, g.gaps, g.chips = blue, teal, gaps, chips
    return g


# ── the documents ──────────────────────────────────────────────────────────────────────
def movie_doc(title, year, genres):
    arr = ", ".join(f'"{g}"' for g in genres)
    return "\n".join([f'{{"title": "{title}",', f' "year": {year},', f' "genres": [{arr}]}}'])


class GenresScene(NarratedScene):
    def construct(self):
        self.mod4 = load_scene("ch4_s3_movie")
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c5.genres.1: documents, chips tethered to the cards they came from; News → Food, Inc.
    def clip1(self):
        docs = [("Food, Inc.", 2008, ["Documentary", "News"]),
                ("Titanic", 1997, ["Drama", "Romance"]),
                ("Saving Private Ryan", 1998, ["Drama", "War"])]
        self.cards = []
        for k, (t, y, gs) in enumerate(docs):
            card = self.mod4.doc_card(movie_doc(t, y, gs), size=21)
            card.move_to([0, 2.1 - 2.1 * k, 0])
            card.shift(RIGHT * (-6.4 - card.get_left()[0]))
            self.cards.append(card)
        food, titanic, ryan = self.cards

        self.slots = doc_slots()
        self.chips = {n: chip_at(n, *self.slots[n]) for n in DOC_GENRES}
        self.tethers = {}            # (card index, genre) -> Line
        for k, (_, _, gs) in enumerate(docs):
            card = self.cards[k]
            start = np.array([card.frame.get_right()[0], card.code.line(2).get_y(), 0])
            for g in gs:
                ch = self.chips[g]
                ln = Line(start, ch.get_left()).set_stroke(TEAL, 2, opacity=0.7)
                ln.set_z_index(-1)
                self.tethers[(k, g)] = ln
        tethered = ["News", "Romance", "War", "Documentary", "Drama"]
        rest = [n for n in DOC_GENRES if n not in tethered]

        self.count = T("23", 30, color=GOLD, weight=BOLD)
        head_t = T("genres in the documents", 30, color=TEAL)
        self.head = VGroup(self.count, head_t).arrange(RIGHT, buff=0.16)
        self.head.move_to([TEAL_X, TOP - HDR / 2, 0])
        self.count.align_to(head_t, DOWN)

        with self.say("c5.genres.1") as c:
            self.play(*appear(*self.cards, lag=0.3), run_time=min(1.6, c.until("inside")))  # early: the documents are the scene's subject
            c.wait_until("inside")
            self.play(*[Create(t) for t in self.tethers.values()],  # early: the chips arrive as the sentence's "genre's name"
                      *during(appear(*[self.chips[n] for n in tethered], shift=None, lag=0.15), 0.45, 1.0),
                      run_time=2.0)
            self.play(*appear(*[self.chips[n] for n in rest], shift=None, lag=0.08),
                      *appear(self.head), run_time=1.2)  # early: the grid's heading arrives with its chips
            c.wait_until("news")
            news = self.chips["News"]
            others = [self.chips[n] for n in DOC_GENRES if n != "News"]
            other_t = [t for key, t in self.tethers.items() if key != (0, "News")]
            self.play(news.rect.animate.set_stroke(YELLOW, 2.5), *recolor([news.label], YELLOW),
                      self.tethers[(0, "News")].animate.set_stroke(YELLOW, 3, opacity=1),
                      *set_alpha(others + other_t + [titanic.code, ryan.code], DIMMED),
                      *[cd.frame.animate.set_stroke(opacity=DIMMED).set_fill(opacity=0.02)
                        for cd in (titanic, ryan)],
                      run_time=1.5)
            self.play(FlashAround(news, time_width=1.5, run_time=1.2))
            self.one = T("1 movie", 28, color=GOLD)
            self.one.next_to(news, RIGHT, buff=0.15)
            c.wait_until(own_word=self.one)
            self.play(*appear(self.one), FlashAround(food.frame, color=YELLOW, time_width=1.5),
                      run_time=1.2)

    # c5.genres.2: delete Food, Inc.; News vanishes. In the relational database it stays.
    def clip2(self):
        food, titanic, ryan = self.cards
        self.sql_del = Code("DELETE FROM movies\nWHERE movie_id = 'tt1286537';", size=28)
        self.sql_del.move_to([0, -0.3, 0])
        self.sql_del.shift(RIGHT * (-6.4 - self.sql_del.get_left()[0]))
        gone_t = [self.tethers[(k, g)] for (k, g) in self.tethers if k > 0]
        food_t = [self.tethers[(0, "News")], self.tethers[(0, "Documentary")]]
        news = self.chips["News"]
        with self.say("c5.genres.2") as c:
            self.play(*during(disappear(titanic, ryan, *gone_t), 0, 0.45),
                      *during(appear(self.sql_del), 0.5, 1.0), run_time=min(1.8, c.until("gone")))
            c.wait_until("gone")
            self.play(FadeOut(food, scale=0.85), *disappear(*food_t, self.one),
                      news.rect.animate.set_stroke(RED, 2.5), *recolor([news.label], RED),
                      run_time=1.5)
            new_count = T("22", 30, color=GOLD, weight=BOLD).move_to(self.count)
            others = [self.chips[n] for n in DOC_GENRES if n != "News"]
            self.play(FadeOut(news), *swap(self.count, new_count), *set_alpha(others, 1), run_time=1.3)
            self.count = new_count
            del self.chips["News"]
            self.del_label = T("Deletion anomaly", 48, color=YELLOW).move_to([-3.4, 2.1, 0])
            c.wait_until("anomaly")
            self.play(*appear(self.del_label), run_time=1.0)
            c.wait_until("relational")

            self.card = GenresCard()
            m = mono(ROW_SIZE)
            lines = [("movies", "tt1286537", "Food, Inc."),
                     ("has_genre", "tt1286537", " 7"), ("has_genre", "tt1286537", "20")]
            self.mini = VGroup()
            for k, (tab, mid, val) in enumerate(lines):
                y = 3.25 - 0.38 * k
                a = placed(mono(ROW_SIZE, DIM), tab, y)
                a.shift(RIGHT * (CARD_L - a.get_left()[0]))
                b = placed(mono(ROW_SIZE, DIM), mid, y)
                b.shift(RIGHT * (CARD_L + 2.1 - b.get_left()[0]))
                v = placed(m, val.strip(), y)
                if val.strip().isdigit():
                    v.shift(RIGHT * (CARD_L + 4.35 - v.get_right()[0]))
                else:
                    v.shift(RIGHT * (CARD_L + 4.0 - v.get_left()[0]))
                self.mini.add(VGroup(a, b, v))
            self.play(*during(disappear(self.sql_del, self.del_label), 0, 0.4),
                      *during(appear(self.card, shift=None), 0.35, 0.8),
                      *during(appear(*self.mini, lag=0.3), 0.6, 1.0),  # early: the rows of Food, Inc. come with the database
                      run_time=2.0)
            row = self.card.rows[20]
            c.wait_until("row of its own")
            self.play(*recolor(row, YELLOW), FlashAround(row, time_width=1.5), run_time=1.2)
            c.wait_until("delete the movie")
            self.play(*recolor(self.mini, RED), run_time=1.0)
            c.wait_until("and the genre")
            self.play(*disappear(*self.mini, lag=0.15), *recolor(row, GREEN),
                      FlashAround(row, color=GREEN, time_width=1.5), run_time=min(1.4, c.until(floor=0.8)))

    # c5.genres.3: INSERT Superhero: a row in the card; nowhere to go in the documents.
    def clip3(self):
        row20 = self.card.rows[20]
        self.sql_ins = Code("INSERT INTO genres (genre_id, name)\nVALUES (27, 'Superhero');", size=26)
        self.sql_ins.move_to([0, 2.95, 0])
        self.sql_ins.shift(RIGHT * (-6.4 - self.sql_ins.get_left()[0]))
        self.hero_row = genre_row(27, "Superhero", GREEN)
        self.hero_row[0].set_color(GREEN)
        with self.say("c5.genres.3") as c:
            self.play(row20[0].animate.set_color(DIM), row20[1].animate.set_color(FG), run_time=1.0)
            c.wait_until("superhero")
            self.play(*appear(self.sql_ins), run_time=1.0)
            c.wait_until("creates")
            self.play(Transform(self.card.box, card_box(14)),
                      *appear(self.hero_row, shift=0.25 * UP),
                      FlashUnder(self.sql_ins.find("(27, 'Superhero')"), color=GREEN, time_width=1.5),
                      run_time=1.6)
            c.wait_until("nowhere")
            self.hover = Chip("Superhero").move_to([TEAL_X - 0.3, 2.75, 0])
            self.qm = T("?", 44, color=RED).next_to(self.hover, RIGHT, buff=0.25)
            self.ins_label = T("Insertion anomaly", 36, color=YELLOW).move_to([TEAL_X + 0.4, 3.4, 0])
            self.play(*appear(self.hover, shift=0.25 * DOWN), run_time=1.2)
            self.play(*appear(self.qm, self.ins_label, lag=0.4), run_time=1.3)  # early: the anomaly is named as its picture lands
            c.wait_until("cause")
            self.del_label2 = T("Deletion anomaly", 36, color=YELLOW).move_to([CARD_X, 2.65, 0])
            self.play(*during(disappear(self.sql_ins), 0, 0.4),
                      *during([self.ins_label.animate.move_to([CARD_X, 3.25, 0])], 0.3, 0.8),
                      *during(appear(self.del_label2), 0.6, 1.0),  # early: both anomalies recalled as "both problems"
                      run_time=1.8)
            self.cause = T("a genre has no home of its own", 32, color=YELLOW).move_to([TEAL_X, 3.4, 0])
            c.wait_until(own_word=self.cause)
            self.play(*appear(self.cause), run_time=1.2)

    # c5.genres.4: the real databases: 26 vs 23; Epic, Experimental, Gothic have no movies.
    def clip4(self):
        news = chip_at("News", *self.slots["News"])
        self.chips["News"] = news
        with self.say("c5.genres.4") as c:
            self.play(*disappear(self.ins_label, self.del_label2, self.hover, self.qm),
                      run_time=1.0)
            new_count = T("23", 30, color=GOLD, weight=BOLD).move_to(self.count)
            self.play(*disappear(self.hero_row), Transform(self.card.box, card_box(13)),
                      *appear(news, shift=None), *swap(self.count, new_count),
                      *recolor(self.card.rows[20][1], FG), run_time=1.5)
            self.count = new_count
            c.wait_until("count")
            n26 = T("26 rows", 28, color=GOLD)
            n26.move_to(self.card.header).align_to(self.card.box, RIGHT).shift(LEFT * 0.2)
            self.play(*appear(n26, shift=None), FlashAround(n26, color=GOLD, time_width=1.5),
                      run_time=1.2)  # early: "twenty-six" is spoken as this lands
            c.wait_until("twenty-three")
            self.play(FlashAround(self.count, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("three")
            rows = [self.card.rows[gid] for gid in (9, 10, 14)]
            self.play(*[a for r in rows for a in recolor(r, YELLOW)],
                      *flash(rows), run_time=1.2)
            moves = []
            for n, ch in self.chips.items():
                col, r = slot(n)
                if (col, r) != self.slots[n]:
                    moves.append(ch.animate.move_to(slot_center(col, r)))
            gaps = [gap_box(n) for n in EMPTY]
            zeros = [T("0 movies", 24, color=GOLD).move_to(g) for g in gaps]
            self.play(*during(moves, 0, 0.55), *during([GrowFromCenter(g) for g in gaps], 0.5, 0.85),
                      *during(appear(*zeros, shift=None, lag=0.2), 0.6, 1.0),  # early: "no movies" follows the three names
                      run_time=2.0)
        self.wait(0.8)
