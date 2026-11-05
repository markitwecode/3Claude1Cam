"""Chapter 1, scene 2: the movies database in one minute. Clips c1.schema.1 – c1.schema.4.

Owns the running visual *the schema map* (PLAN.md "Running visuals"), slide 23's layout.
Reuse it with `load_scene("ch1_s2_schema")`:

    mod = load_scene("ch1_s2_schema")
    m = mod.schema_map()            # SchemaMap (VGroup), full-frame size, static (no updaters)
    m.cards["movies"]               # TableCard: .box .header .divider .title
                                    #   .rows[col] (Mono 24 Text), .underlines[col] (primary-key Lines)
                                    #   .row_y(col), .entity (bool)
    m.card_group / m.arrow_group / m.count_group   # VGroups of the cards, FK arrows, GOLD counts
    m.arrows[("has_genre", "genres")]              # FK arrow (VGroup: polyline body + Arrow),
                                                   #   keys (src, dst): has_genre→movies/genres,
                                                   #   ratings→movies, has_position→movies/people,
                                                   #   plays_role→movies/people
    m.counts["movies"], m.counts["people"]         # GOLD "2,935 rows", "23,179 rows"
    m.light("movies")               # list of anims: card outline, title (and header fill) YELLOW
    card_alpha(card, a)             # one Transform: dim (a<1) / restore (a=1) a card, keeping its
                                    #   header's own fill opacity
    mod.kid_table("has_position")   # RowTable of The Kid's rows for that table (Mono 22, values
                                    #   YELLOW, tt/nm IDs DIM, NULL PINK): .label .frame .head
                                    #   .rows[i] (VGroup of cells) .cell(i, j); move with place()
    mod.KID_ROWS, mod.SCHEMA        # the data (verified on movies.duckdb)

To shrink the map into a corner: `m.generate_target(); m.target.scale(0.29)` then shift.
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
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- schema data (slide 23)
SCHEMA = {
    "genres": (["genre_id", "name"], ["genre_id"]),
    "ratings": (["movie_id", "rating", "votes"], ["movie_id"]),
    "people": (["person_id", "name", "birthyear", "deathyear"], ["person_id"]),
    "has_genre": (["movie_id", "genre_id"], ["movie_id", "genre_id"]),
    "movies": (["movie_id", "title", "year", "type", "minutes"], ["movie_id"]),
    "has_position": (["movie_id", "person_id", "position", "job"], ["movie_id", "person_id", "position"]),
    "plays_role": (["movie_id", "person_id", "role"], ["movie_id", "person_id", "role"]),
}
ENTITIES = ("movies", "people", "genres")
LINKS = ("ratings", "has_genre", "has_position", "plays_role")
ORDER = ("genres", "ratings", "people", "has_genre", "movies", "has_position", "plays_role")
LAYOUT = {   # card centre x, card top y
    "genres": (-4.6, 3.5), "ratings": (0.0, 3.5), "people": (4.6, 3.5),
    "has_genre": (-4.6, 0.85), "movies": (0.0, 0.85), "has_position": (4.6, 0.85),
    "plays_role": (4.6, -1.6),
}
TT, NM = "tt0012349", "nm0000122"
KID_ROWS = {
    "movies": [[TT, "The Kid", "1921", "movie", "68"]],
    "ratings": [[TT, "8.2", "142,991"]],
    "has_genre": [[TT, "5"], [TT, "8"], [TT, "11"]],
    "genres": [["5", "Comedy"], ["8", "Drama"], ["11", "Family"]],
    "people": [[NM, "Charles Chaplin", "1889", "1977"]],
    "has_position": [[TT, NM, "actor", "NULL"], [TT, NM, "composer", "composer"],
                     [TT, NM, "director", "director"], [TT, NM, "producer", "producer"],
                     [TT, NM, "writer", "written by"]],
    "plays_role": [[TT, NM, "A Tramp"]],
}
HDR, PITCH, PAD_B = 0.5, 0.36, 0.12
COL_SIZE, TITLE_SIZE = 24, 26


def _placed(s, size, color, weight, y, left=None, cx=None):
    """Mono text whose baseline sits on row y (measured with a '|' that spans ascent+descent).
    Returns (text, bottom of the row's descender line)."""
    ref = Mono(s + "|", size, weight=weight)
    ref.move_to([0, y, 0])
    body = VGroup(*ref[:-1])
    if left is not None:
        ref.shift(RIGHT * (left - body.get_left()[0]))
    else:
        ref.shift(RIGHT * (cx - body.get_center()[0]))
    t = Mono(s, size, color=color, weight=weight)
    t.move_to(body.get_center())
    return t, ref[-1].get_bottom()[1]


def _remember(mob):
    for p in mob.get_family():
        p._base = (p.get_fill_opacity(), p.get_stroke_opacity())


def card_alpha(card, a):
    """One Transform that sets every part of card to a × its own built opacity."""
    tgt = card.copy()
    for src, dst in zip(card.get_family(), tgt.get_family()):
        bf, bs = getattr(src, "_base", (src.get_fill_opacity(), src.get_stroke_opacity()))
        dst.set_fill(opacity=bf * a, family=False)
        dst.set_stroke(opacity=bs * a, family=False)
    return Transform(card, tgt)


class TableCard(VGroup):
    def __init__(self, name, x, top):
        super().__init__()
        cols, keys = SCHEMA[name]
        self.name = name
        self.entity = name in ENTITIES
        w = 3.2 if self.entity else 2.8
        h = HDR + len(cols) * PITCH + PAD_B
        self.top_y = top
        self.box = Rectangle(width=w, height=h).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.box.move_to([x, top - h / 2, 0])
        self.header = Rectangle(width=w, height=HDR).set_stroke(BLUE, 0)
        self.header.set_fill(BLUE, 0.35 if self.entity else 0)
        self.header.move_to([x, top - HDR / 2, 0])
        self.divider = Line([x - w / 2, top - HDR, 0], [x + w / 2, top - HDR, 0]).set_stroke(BLUE, 2)
        self.title, _ = _placed(name, TITLE_SIZE, FG, BOLD, top - HDR / 2, cx=x)
        self.rows, self.underlines = {}, {}
        for i, c in enumerate(cols):
            t, bot = _placed(c, COL_SIZE, FG, NORMAL, self.row_y(c, cols), left=x - w / 2 + 0.22)
            self.rows[c] = t
            if c in keys:
                self.underlines[c] = Line([t.get_left()[0], bot + 0.02, 0],
                                          [t.get_right()[0], bot + 0.02, 0]).set_stroke(FG, 2.5)
        self.add(self.header, self.box, self.divider, self.title,
                 *self.rows.values(), *self.underlines.values())
        _remember(self)

    def row_y(self, col, cols=None):
        cols = cols or SCHEMA[self.name][0]
        return self.top_y - HDR - PITCH * (cols.index(col) + 0.5) - 0.02


def _fk(points, color=FG):
    """Polyline through points, arrow tip on the last segment."""
    parts = []
    if len(points) > 2:
        parts.append(VMobject().set_points_as_corners([np.array(p) for p in points[:-1]])
                     .set_stroke(color, 3))
    parts.append(Arrow(np.array(points[-2]), np.array(points[-1]), buff=0, stroke_width=3,
                       tip_length=0.16, max_tip_length_to_length_ratio=0.7,
                       max_stroke_width_to_length_ratio=100, color=color))
    return VGroup(*parts)


class SchemaMap(VGroup):
    def __init__(self):
        super().__init__()
        self.cards = {n: TableCard(n, *LAYOUT[n]) for n in ORDER}
        cd = self.cards
        hg, mv, rt = cd["has_genre"], cd["movies"], cd["ratings"]
        hp, pp, pr, gn = cd["has_position"], cd["people"], cd["plays_role"], cd["genres"]
        y0 = mv.row_y("movie_id")
        self.arrows = {
            ("has_genre", "genres"): _fk([(hg.box.get_x(), hg.box.get_top()[1], 0),
                                         (gn.box.get_x(), gn.box.get_bottom()[1], 0)]),
            ("has_genre", "movies"): _fk([(hg.box.get_right()[0], y0, 0), (mv.box.get_left()[0], y0, 0)]),
            ("ratings", "movies"): _fk([(0, rt.box.get_bottom()[1], 0), (0, mv.box.get_top()[1], 0)]),
            ("has_position", "movies"): _fk([(hp.box.get_left()[0], y0, 0), (mv.box.get_right()[0], y0, 0)]),
            ("has_position", "people"): _fk([(5.4, hp.box.get_top()[1], 0), (5.4, pp.box.get_bottom()[1], 0)]),
            ("plays_role", "movies"): _fk([(pr.box.get_left()[0], pr.row_y("movie_id"), 0),
                                          (0.75, pr.row_y("movie_id"), 0),
                                          (0.75, mv.box.get_bottom()[1], 0)]),
            ("plays_role", "people"): _fk([(pr.box.get_right()[0], pr.row_y("person_id"), 0),
                                          (6.5, pr.row_y("person_id"), 0),
                                          (6.5, pp.row_y("person_id"), 0),
                                          (pp.box.get_right()[0], pp.row_y("person_id"), 0)]),
        }
        self.counts = {
            "movies": T("2,935 rows", 28, GOLD).move_to([-0.55, mv.box.get_bottom()[1] - 0.32, 0]),
            "people": T("23,179 rows", 28, GOLD).move_to(
                [3.9, (pp.box.get_bottom()[1] + hp.box.get_top()[1]) / 2, 0]),
        }
        self.card_group = VGroup(*cd.values())
        self.arrow_group = VGroup(*self.arrows.values())
        self.count_group = VGroup(*self.counts.values())
        self.add(self.arrow_group, self.card_group, self.count_group)

    def light(self, name, color=YELLOW):
        c = self.cards[name]
        anims = [c.box.animate.set_stroke(color), c.title.animate.set_color(color)]
        if c.entity:
            anims.append(c.header.animate.set_fill(color))
        return anims


def schema_map():
    return SchemaMap()


# ---------------------------------------------------------------- The Kid's rows as tables
def _kid_color(col, v):
    if v == "NULL":
        return PINK
    if col in ("movie_id", "person_id"):
        return DIM
    return YELLOW


class RowTable(VGroup):
    def __init__(self, name, cols, rows, colors=None, size=22, pad=0.15, pitch=0.46):
        super().__init__()
        colors = colors or [[YELLOW] * len(cols) for _ in rows]
        widths = []
        for j, c in enumerate(cols):
            ws = [Mono(c, size, weight=BOLD).width] + [Mono(r[j], size).width for r in rows]
            widths.append(max(ws) + 2 * pad)
        xs = [sum(widths[:j]) for j in range(len(cols))]
        W, H = sum(widths), pitch * (1 + len(rows))
        box = Rectangle(width=W, height=H).set_stroke(BLUE, 2).set_fill(BG, 0)
        box.move_to([W / 2, -H / 2, 0])
        hline = Line([0, -pitch, 0], [W, -pitch, 0]).set_stroke(BLUE, 2)
        vlines = [Line([x, 0, 0], [x, -H, 0]).set_stroke(DIM, 1.5) for x in xs[1:]]
        self.frame = VGroup(box, hline, *vlines)
        self.head = VGroup(*[_placed(c, size, FG, BOLD, -pitch / 2, left=xs[j] + pad)[0]
                             for j, c in enumerate(cols)])
        self.cells = [[_placed(v, size, colors[i][j], NORMAL, -pitch * (i + 1.5), left=xs[j] + pad)[0]
                       for j, v in enumerate(r)] for i, r in enumerate(rows)]
        self.rows = [VGroup(*r) for r in self.cells]
        parts = [self.frame, self.head, *self.rows]
        self.label = None
        if name:
            self.label = Mono(name, size + 2, BLUE, weight=BOLD)
            self.label.next_to([0, 0, 0], UP, buff=0.12).align_to(box, LEFT)
            parts.insert(0, self.label)
        self.add(*parts)

    def cell(self, i, j):
        return self.rows[i][j]


def kid_table(name, size=22):
    cols = SCHEMA[name][0]
    rows = KID_ROWS[name]
    colors = [[_kid_color(c, v) for c, v in zip(cols, r)] for r in rows]
    return RowTable(name, cols, rows, colors, size=size)


def place(mob, left=None, top=None, right=None):
    if left is not None:
        mob.shift(RIGHT * (left - mob.get_left()[0]))
    if right is not None:
        mob.shift(RIGHT * (right - mob.get_right()[0]))
    if top is not None:
        mob.shift(UP * (top - mob.get_top()[1]))
    return mob


SQL = """SELECT title, rating
FROM movies
JOIN ratings USING (movie_id)
WHERE title = 'The Kid';"""


class Ch1S2Schema(NarratedScene):
    def construct(self):
        m = schema_map()
        self.m = m
        cd = m.cards

        # ---------------------------------------------------------------- c1: seven tables
        with self.say("c1.schema.1") as c:
            self.play(*appear(*[cd[n] for n in ORDER], lag=0.12),  # early: the map is shown whole, then walked
                      run_time=min(2.5, c.until("almost")))
            settle(self, m, drop=[m.arrow_group, m.count_group])
            c.wait_until("three thousand movies")
            self.play(*appear(m.counts["movies"]), run_time=1.0)
            c.wait_until("thousand people")
            self.play(*appear(m.counts["people"]), run_time=1.0)
            settle(self, m, add=[m.count_group])

            c.wait_until("entities")
            self.play(*[card_alpha(cd[n], 0.3) for n in LINKS], run_time=1.0)
            c.wait_until("the world")
            self.play(LaggedStart(*[FlashAround(cd[n], time_width=1.5) for n in ("movies", "people", "genres")],
                                  lag_ratio=0.35), run_time=min(2.2, c.until("links")))
            c.wait_until("links")
            self.play(*[card_alpha(cd[n], 1) for n in LINKS],
                      *[card_alpha(cd[n], 0.4) for n in ENTITIES], run_time=1.2)
            c.wait_until("ratings")
            self.play(LaggedStart(*[FlashAround(cd[n], time_width=1.5) for n in LINKS], lag_ratio=0.3),
                      run_time=min(3.0, c.until()))

        # ---------------------------------------------------------------- c2: keys and arrows
        with self.say("c1.schema.2") as c:
            self.play(*[card_alpha(cd[n], 1) for n in ENTITIES], run_time=0.8)
            uls = [u for n in ORDER for u in cd[n].underlines.values()]
            self.play(*[VShowPassingFlash(u.copy().set_stroke(YELLOW, 7), time_width=0.8) for u in uls],
                      run_time=1.8)
            c.wait_until("arrows")
            self.play(LaggedStart(*[Create(a) for a in m.arrows.values()], lag_ratio=0.3),
                      run_time=min(3.5, c.until("a column")))
            settle(self, m, add=[m.arrow_group])
            c.wait_until("a column")
            a = m.arrows[("ratings", "movies")]
            self.play(VShowPassingFlash(a[-1].copy().set_stroke(YELLOW, 6), time_width=0.6),
                      FlashUnder(cd["ratings"].rows["movie_id"]), FlashUnder(cd["movies"].rows["movie_id"]),
                      run_time=1.5)

        # ---------------------------------------------------------------- c3: The Kid, card by card
        with self.say("c1.schema.3") as c:
            m.generate_target()
            m.target.scale(0.29)
            m.target.shift(RIGHT * (6.6 - m.target.get_right()[0]) + UP * (3.5 - m.target.get_top()[1]))
            self.play(MoveToTarget(m), run_time=min(2.0, c.until("the kid")))

            mv = place(kid_table("movies"), left=-6.1, top=3.45)
            head = T("The Kid (1921)", 52, YELLOW).move_to(mv)
            c.wait_until("the kid")
            self.play(*appear(head), run_time=1.0)
            c.wait_until("movie")
            self.play(*swap(head, mv), *m.light("movies"), run_time=min(1.5, c.until("minutes long")))
            c.wait_until("minutes long")
            self.play(FlashAround(mv.cell(0, 4), time_width=1.5), run_time=1.2)

            c.wait_until("rating")
            rt = place(kid_table("ratings"), left=-6.1, top=1.75)
            self.play(*appear(rt), *m.light("ratings"), run_time=1.2)

            c.wait_until("genres")
            hg = kid_table("has_genre")
            gt = kid_table("genres")
            hg.move_to([-2.7, 0, 0])
            place(hg, top=-0.5)
            gt.move_to([2.5, 0, 0])
            place(gt, top=-0.5)
            self.play(*appear(hg, gt, lag=0.3), *m.light("has_genre"), *m.light("genres"),  # early: both tables arrive together so the genre names hold the whole sentence
                      run_time=min(1.2, c.until("pointing at")))
            c.wait_until("pointing at")
            gx0, gx1 = hg.frame[0].get_right()[0], gt.frame[0].get_left()[0]
            lines = [Line([gx0, hg.cell(i, 1).get_y(), 0], [gx1, gt.cell(i, 0).get_y(), 0])
                     .set_stroke(YELLOW, 3) for i in range(3)]
            self.play(*[Create(ln) for ln in lines], run_time=min(1.5, c.until("chaplin")))

            c.wait_until("chaplin")
            pp = place(kid_table("people"), left=-6.1, top=3.45)
            self.play(*during(disappear(mv, rt, hg, gt, *lines), 0, 0.45),
                      *during(appear(pp), 0.5, 1), *during(m.light("people"), 0.5, 1), run_time=1.8)

            c.wait_until("jobs")
            hp = place(kid_table("has_position"), left=-6.1, top=1.75)
            self.play(*appear(hp.label, hp.frame, hp.head, lag=0.15), *m.light("has_position"),
                      run_time=1.2)
            for i, verb in enumerate(["acted", "composed", "directed", "produced", "wrote"]):
                c.wait_until(verb)
                self.play(*appear(hp.rows[i], shift=None), run_time=0.7)
            settle(self, hp)

            c.wait_until("role")
            pr = place(kid_table("plays_role"), right=6.4, top=-1.75)
            self.play(*appear(pr), *m.light("plays_role"), run_time=1.2)
            c.wait_until("a tramp")
            self.play(FlashAround(pr.cell(0, 2), time_width=1.5), run_time=1.2)

        # ---------------------------------------------------------------- c4: join on keys
        with self.say("c1.schema.4") as c:
            mv2 = place(kid_table("movies"), left=-6.1, top=3.45)
            rt2 = place(kid_table("ratings"), left=1.4, top=0.6)
            self.play(*during(disappear(pp, hp, pr), 0, 0.45),
                      *during(appear(mv2, rt2, lag=0.2), 0.5, 1), run_time=1.6)
            rt2.generate_target()
            place(rt2.target, left=-6.1, top=1.75)
            rt2.target.rows[0][0].set_color(YELLOW)
            a0 = mv2.cell(0, 0).get_left() + LEFT * 0.12
            a1 = rt2.target.rows[0][0].get_left() + LEFT * 0.12
            link = ArcBetweenPoints(a0, a1, angle=PI / 2).set_stroke(YELLOW, 4)
            self.play(MoveToTarget(rt2), mv2.cell(0, 0).animate.set_color(YELLOW),
                      *during([Create(link)], 0.7, 1), run_time=min(1.8, c.until("match")))

            c.wait_until("match")
            mt = MathTex(r"\text{movies} \bowtie_{\text{movie\_id}} \text{ratings}", font_size=48)
            place(mt.move_to([0, -1.45, 0]), right=6.5)
            self.play(*appear(mt), run_time=1.0)
            c.wait_until("on the movie")
            sql = Code(SQL, size=30)
            place(sql, left=-6.1, top=-1.0)
            self.play(*appear(sql), run_time=1.0)

            c.wait_until("title lands")
            res = RowTable(None, ["title", "rating"], [["The Kid", "8.2"]], size=30)
            res.move_to([4.2, 0.0, 0])
            others = [mv2.cell(0, j) for j in (2, 3, 4)] + [mv2.head[j] for j in (2, 3, 4)] \
                + [rt2.cell(0, 2), rt2.head[2]]
            self.play(*during(set_alpha(others, DIMMED), 0, 0.4),
                      *during(appear(res.frame), 0, 0.5),
                      *during(fly(mv2.cell(0, 1), res.cell(0, 0)) + fly(rt2.cell(0, 1), res.cell(0, 1)), 0.35, 1),
                      run_time=2.2)
            self.play(*appear(res.head, lag=0.1), run_time=0.8)

            c.wait_until("enough")
            self.play(FadeOut(m, scale=0.4, target_position=[6.3, 3.3, 0]), run_time=1.2)
            c.wait_until("everything else")
            self.play(*[FadeOut(x) for x in self.mobjects], run_time=1.0)
        if self.mobjects:
            self.play(*[FadeOut(x) for x in self.mobjects], run_time=1.0)
        self.wait(0.15)
