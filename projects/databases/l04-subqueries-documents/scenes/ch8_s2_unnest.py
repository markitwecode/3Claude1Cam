"""Chapter 8, scene 2: unnest, one row per element. Clips c8.unnest.1 – c8.unnest.5.

Opens on ch8 s1's handover_shot() (the ten lifted TEAL chips); parks the chips at the right edge
for {small}, lands them as the ten rows of `t` on {rows}. Ends on an empty frame.

Exports (import with `U = load_scene("ch8_s2_unnest")`; all static, no updaters):

    U.unfold(size=30) -> VGroup centred at ORIGIN, about 5.6 wide x 4.1 tall:
        .cell   The Kid's genres cell: json_code '["Comedy", "Drama", "Family"]' (TEAL brackets) in a
                ch4 s3 TEAL frame, on top; .cell.code, .cell.frame
        .items  [VGroup] the three quoted strings' glyphs inside .cell.code
        .table  the result table `t(genre)` under it (ch8 s3 pair_table look: BLUE frame, bold FG
                header, genres BLUE Mono, BLUE bold name label "t"); .table.frame .head .rows[i] .label
        Static: the cell shown, the table drawn complete. To animate the unfolding, add .cell, then
        U.play_unfold(scene, u, run_time=2.0): the table's frame/head/label appear, then the three
        strings fly down into the three rows (one after another).
    U.genre_table(size=32, pitch=0.6) -> just the 3-row `t(genre)` table, top-left corner at ORIGIN.
    U.recap_thumb_rows() -> VGroup(.list (Code `unnest(['Comedy', 'Drama', 'Family'])`, BLUE list),
        .arrow (DIM, down), .table (genre_table)), about 7.0 wide x 3.9 tall, centred at ORIGIN.
    U.recap_thumb_loop() -> VGroup(.loop (ch3 s2 outer_loop: movies left, BLUE `unnest(...)` card right,
        GOLD counter "10"), .cursor (YELLOW, on The Kid), .rows (The Kid's ten actor rows, TEAL)),
        full-frame layout (about 13.1 wide x 4.0 tall), centred at ORIGIN; scale it into a slot.
    U.table(cols, rows, colors, size, pitch, pad, widths, name): the table builder (ch8 s3's look).
    Data (verified on movies-json.duckdb / movies.duckdb): CAST_ROLES, SHERLOCK, JOIN_ROWS.

Colours as ch7: TEAL JSON value, BLUE SQL value / DuckDB list, PINK NULL, GOLD counts.
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

H = load_scene("ch8_s1_hook")
C2 = load_scene("ch3_s2_correlated")
K7 = load_scene("ch3_s7_toolkit")
SCH = load_scene("ch1_s2_schema")
D = load_scene("ch4_s3_movie")

# ══ data (verified) ═══════════════════════════════════════════════════════════
CAST_ROLES = [("Charles Chaplin", '["A Tramp"]'), ("Edna Purviance", '["The Woman"]'),
              ("Jackie Coogan", '["The Child"]'), ("Carl Miller", '["The Man"]'),
              ("Albert Austin", '["Car Thief","Man in Shelter"]'), ("Beulah Bains", '["Bride"]'),
              ("Nellie Bly Baker", '["Slum Nurse"]'),
              ("Henry Bergman", '["Professor Guido","Night Shelter Keeper"]'),
              ("Edward Biby", '["Orphan Asylum Driver"]'), ("B.F. Blinn", '["His Assistant"]')]
CAST = [n for n, _ in CAST_ROLES]
SHERLOCK = ["Buster Keaton", "Kathryn McGuire", "Joe Keaton", "Erwin Connelly", "Ward Crane",
            "Jane Connelly", "George Davis", "Doris Deane", "Christine Francis", "Betsy Ann Hisle"]
RESULT4 = [("Albert Austin", '["Car Thief","Man in Shelter"]'), ("B.F. Blinn", '["His Assistant"]'),
           ("Beulah Bains", '["Bride"]'), ("Carl Miller", '["The Man"]')]
JOIN4 = [("The Kid", "A Tramp", "Charles Chaplin"), ("The Kid", "Bride", "Beulah Bains"),
         ("The Kid", "Car Thief", "Albert Austin"), ("The Kid", "His Assistant", "B.F. Blinn")]
JOIN_ROWS = JOIN4 + [("The Kid", "Man in Shelter", "Albert Austin"),
                     ("The Kid", "Night Shelter Keeper", "Henry Bergman"),
                     ("The Kid", "Orphan Asylum Driver", "Edward Biby"),
                     ("The Kid", "Professor Guido", "Henry Bergman"),
                     ("The Kid", "Slum Nurse", "Nellie Bly Baker"),
                     ("The Kid", "The Child", "Jackie Coogan"), ("The Kid", "The Man", "Carl Miller"),
                     ("The Kid", "The Woman", "Edna Purviance")]
TWO_PARTS = ("Albert Austin", "Henry Bergman")

SMALL = """SELECT *
FROM   unnest(['Comedy', 'Drama', 'Family'])
       AS t(genre);"""
QUERY = """SELECT   a->>'name' AS name, a->'roles' AS roles
FROM     movies, unnest(movie->'$.actors[*]') AS t(a)
WHERE    (movie->>'title') = 'The Kid'
ORDER BY name
LIMIT    4;"""
WHERE_ID = "WHERE movie_id = 'tt0012349'"
WHERE_TITLE = "WHERE (movie->>'title') = 'The Kid'"
JOINQ = """SELECT   m.title, r.role, p.name
FROM     movies AS m
JOIN     plays_role AS r ON m.movie_id = r.movie_id
JOIN     people AS p ON r.person_id = p.person_id
WHERE    m.title = 'The Kid'
ORDER BY r.role
LIMIT    4;"""
UNNEST_CALL = "unnest(movie->'$.actors[*]')"
GENRES = ["Comedy", "Drama", "Family"]

# layout
Q_SIZE, Q_LEFT, Q_TOP = 22, -6.55, 3.6
PARK_S, PARK_X, PARK_Y0, PARK_PITCH = 0.55, -5.75, -0.6, 0.3
ROW_TOP, ROW_PITCH = 1.35, 0.4          # clip 2: t and the projection share these rows
T_LEFT, CHIP_S = 3.55, 0.9
LOOP_KW = dict(right_title=UNNEST_CALL, right_cols=("a",), dim_cols=(), lsize=24, rsize=20, title_size=20,
               lx=-6.5, ltop=0.55, lpitch=0.45, rx=6.6, ctop=0.8, hdr=0.42, pitch=0.3, count_y=-1.0,
               pad=0.2, cursor_pad=0.3)


def _obj_row(name):
    return '{"name": "%s", …}' % name


# ══ builders ═════════════════════════════════════════════════════════════════
def table(cols, rows, colors, size=28, pitch=0.5, pad=0.16, widths=None, name=None, serif=None):
    """ch8 s3's pair_table look: BLUE frame, BLUE header rule, DIM column rules, bold FG header,
    Mono cells on one baseline per row. Top-left corner at ORIGIN.
    serif = {column index: T size}: that column's cells in CMU Serif (plain names)."""
    serif = serif or {}

    def mk(v, j, color=FG):
        return T(v, serif[j], color) if j in serif else Mono(v, size, color=color)

    if widths is None:
        widths = [max([Mono(c, size, weight=BOLD).width] + [mk(r[j], j).width for r in rows]) + 2 * pad
                  for j, c in enumerate(cols)]
    xs = [sum(widths[:j]) for j in range(len(cols))]
    W, Ht = sum(widths), pitch * (1 + len(rows))
    box = Rectangle(width=W, height=Ht).set_stroke(BLUE, 2).set_fill(BG, 0)
    box.move_to([W / 2, -Ht / 2, 0])
    hline = Line([0, -pitch, 0], [W, -pitch, 0]).set_stroke(BLUE, 2)
    vlines = [Line([x, 0, 0], [x, -Ht, 0]).set_stroke(DIM, 1.5) for x in xs[1:]]
    frame = VGroup(box, hline, *vlines)
    head = VGroup(*[SCH._placed(c, size, FG, BOLD, -pitch / 2, left=xs[j] + pad)[0]
                    for j, c in enumerate(cols)])
    def cell(v, i, j):
        y = -pitch * (i + 1.5)
        if j in serif:
            t = mk(v, j, colors[i][j])
            base = SCH._placed("M", size, FG, NORMAL, y, left=0)[0].get_bottom()[1]
            t.move_to([0, y, 0]).align_to([xs[j] + pad, 0, 0], LEFT)
            t.shift(UP * (base - t[0].get_bottom()[1]))      # capital first letter on the row's baseline
            return t
        return SCH._placed(v, size, colors[i][j], NORMAL, y, left=xs[j] + pad)[0]

    rws = [VGroup(*[cell(v, i, j) for j, v in enumerate(r)]) for i, r in enumerate(rows)]
    g = VGroup(frame, head, *rws)
    g.label = None
    if name:
        g.label = Mono(name, size + 2, BLUE, weight=BOLD)
        g.label.next_to([0, 0, 0], UP, buff=0.12).align_to(box, LEFT)
        g.add(g.label)
    g.frame, g.head, g.rows, g.widths = frame, head, rws, widths
    g.cell = lambda i, j: rws[i][j]
    return g


def place(mob, left, top):
    """Shift a table so its frame's top-left corner sits at (left, top)."""
    box = mob.frame[0]
    mob.shift(RIGHT * (left - box.get_left()[0]) + UP * (top - box.get_top()[1]))
    return mob


def genre_table(size=32, pitch=0.6):
    return table(["genre"], [[g] for g in GENRES], [[BLUE]] * 3, size=size, pitch=pitch,
                 widths=[2.6 * size / 32], name="t")


def _drop_anims(items, tbl):
    """The items fly down into the table's rows, one after another (a list for play())."""
    out = []
    for k, (src, row) in enumerate(zip(items, tbl.rows)):
        j = len(tbl.rows) - 1 - k      # bottom row first: no item passes over a filled row
        out += during(fly(src, row[0], arc=0), 0.3 * j, 0.4 + 0.3 * j)
    return out


def unfold(size=30):
    code = D.json_code('["Comedy", "Drama", "Family"]', size)
    frame = D.fit_frame(code, size=size)
    cell = VGroup(frame, code)
    cell.code, cell.frame = code, frame
    items = [code.find(g) for g in GENRES]
    tbl = genre_table()
    tbl.next_to(cell, DOWN, buff=0.9)
    tbl.shift(RIGHT * (cell.get_center()[0] - tbl.frame.get_center()[0]))
    g = VGroup(cell, tbl).move_to(ORIGIN)
    g.cell, g.items, g.table = cell, items, tbl
    return g


def play_unfold(scene, u, run_time=2.0):
    t = u.table
    scene.play(*appear(t.frame, shift=None), run_time=min(0.8, run_time / 2))
    scene.play(*_drop_anims(u.items, t), run_time=run_time)
    scene.play(*appear(t.head, t.label, lag=0.15), run_time=0.8)


def recap_thumb_rows():
    lst = Code("unnest(['Comedy', 'Drama', 'Family'])", 30)
    tbl = genre_table()
    tbl.next_to(lst, DOWN, buff=1.0)
    tbl.shift(RIGHT * (lst.get_center()[0] - tbl.frame.get_center()[0]))
    arrow = Arrow(lst.get_bottom() + 0.05 * DOWN, tbl.label.get_top() + 0.05 * UP + RIGHT * 0.6,
                  buff=0.08, stroke_width=3, color=DIM)
    g = VGroup(lst, arrow, tbl).move_to(ORIGIN)
    g.list, g.arrow, g.table = lst, arrow, tbl
    return g


def _loop_rows(loop, names):
    card = loop.card
    x0 = card.heads[0].get_left()[0]
    rows = VGroup()
    for i, n in enumerate(names):
        y = card.y_first - i * loop.pitch
        t = Mono(_obj_row(n), LOOP_KW["rsize"], color=TEAL)
        t.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
        rows.add(t)
    return rows


def loop_picture():
    """The {loop} picture: ch3 s2's outer loop, card rows taken out (they drop in on {outer})."""
    loop = C2.outer_loop(left_rows=C2.MOVIE_ROWS, right_rows=[(_obj_row(n),) for n in SHERLOCK], **LOOP_KW)
    loop.card.remove(*loop.card.rows)
    loop.card.title.set_color(BLUE)
    return loop


def recap_thumb_loop():
    loop = loop_picture()
    rows = _loop_rows(loop, CAST)
    old = loop.counter
    new = Mono("10", 44, color=GOLD).move_to(old)
    loop.remove(old)
    loop.add(new)
    loop.counter = new
    cursor = loop.cursor_at(0)
    g = VGroup(cursor, loop, rows)
    g.loop, g.cursor, g.rows = loop, cursor, rows
    return g.move_to(ORIGIN)


def _t_table():
    """Clip 2's table t: column a, ten rows (empty frame; the chips land in it)."""
    w = H.CHIP_W * CHIP_S + 0.85
    n = len(CAST)
    Ht = ROW_PITCH * (n + 1)
    box = Rectangle(width=w, height=Ht).set_stroke(BLUE, 2).set_fill(BG, 0)
    box.move_to([T_LEFT + w / 2, ROW_TOP - Ht / 2, 0])
    hline = Line([T_LEFT, ROW_TOP - ROW_PITCH, 0], [T_LEFT + w, ROW_TOP - ROW_PITCH, 0]).set_stroke(BLUE, 2)
    frame = VGroup(box, hline)
    head = SCH._placed("a", Q_SIZE, FG, BOLD, ROW_TOP - ROW_PITCH / 2, left=T_LEFT + 0.16)[0]
    label = Mono("t", Q_SIZE + 2, BLUE, weight=BOLD)
    label.next_to([T_LEFT, ROW_TOP, 0], UP, buff=0.12).align_to(box, LEFT)
    g = VGroup(frame, head, label)
    g.frame, g.head, g.label = frame, head, label
    g.cx = T_LEFT + w / 2
    g.row_y = lambda i: ROW_TOP - ROW_PITCH * (i + 1.5)
    return g


def _curly(mob, side, w=0.13, buff=0.07, color=TEAL):
    """A drawn TEAL curly brace beside mob (a shape, so names can fly past it)."""
    top, bot = mob.get_top()[1], mob.get_bottom()[1]
    mid, h = (top + bot) / 2, top - bot
    if side is LEFT or np.allclose(side, LEFT):
        x0, s = mob.get_left()[0] - buff, -1
    else:
        x0, s = mob.get_right()[0] + buff, 1
    pts = [(0, top), (s * w * 0.5, top - h * 0.12), (s * w * 0.5, mid + h * 0.12), (s * w, mid),
           (s * w * 0.5, mid - h * 0.12), (s * w * 0.5, bot + h * 0.12), (0, bot)]
    v = VMobject().set_points_smoothly([np.array([x0 + x, y, 0]) for x, y in pts])
    return v.set_stroke(color, 2.5)


def _alpha(glyphs, op):
    return [restyle(g, op) for g in glyphs]


def _names_list(names, cx, top, size=26, pitch=0.36):
    col = VGroup()
    for i, n in enumerate(names):
        col.add(T(n, size).move_to([cx, top - i * pitch, 0]))
    return col


# ══ the scene ════════════════════════════════════════════════════════════════
class Unnest(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- c8.unnest.1
    def clip1(self):
        hs = H.handover_shot()
        self.add(hs)
        parts = [hs.table, hs.cell, hs.tag, hs.link, hs.doc, hs.slots]
        self.chips = chips = list(hs.chips)
        self.remove(hs)
        self.add(*parts, *chips)
        for i, ch in enumerate(chips):
            ch.generate_target()
            ch.target.scale(PARK_S).move_to([PARK_X, PARK_Y0 - i * PARK_PITCH, 0])
            ch.target.box.set_stroke(opacity=0.45).set_fill(opacity=0.05)
            ch.target.text.set_fill(opacity=0.45)

        code = Code(SMALL, 34)
        code.move_to([0, 0, 0]).align_to([0, 3.2, 0], UP)
        tbl = genre_table(size=36, pitch=0.66)
        place(tbl, 6.6 - tbl.frame[0].width, 0.7)

        with self.say("c8.unnest.1") as c:
            self.play(*during(disappear(*parts), 0, 0.45),
                      *during([MoveToTarget(ch) for ch in chips], 0.45, 1.0), run_time=1.6)
            self.play(*appear(code), run_time=min(1.0, c.until("list")))   # early: the query the line is about
            c.wait_until("list")
            lst = code.find("['Comedy', 'Drama', 'Family']")
            box = token_box(lst, code.line(1))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("three")
            self.play(*appear(tbl.frame, shift=None), run_time=0.8)
            self.play(*_drop_anims([code.find(g) for g in GENRES], tbl), FadeOut(box),

                      run_time=min(2.0, c.until("name")))
            self.play(*appear(tbl.head, tbl.label, lag=0.15), run_time=min(0.8, c.until("name")))
            c.wait_until("name")
            tg = code.find("t", line=2)
            gg = code.find("genre", line=2)
            b1 = Brace(tg, DOWN, buff=0.1, color=DIM)
            b2 = Brace(gg, DOWN, buff=0.1, color=DIM)
            l1 = T("table", 32).next_to(b1, DOWN, buff=0.15).align_to(b1, RIGHT)
            l2 = T("its one column", 32).next_to(b2, DOWN, buff=0.15)
            l2.align_to(b2, LEFT).shift(0.15 * RIGHT)
            c.wait_until(own_word=l1)
            self.play(GrowFromCenter(b1), *appear(l1), FlashAround(tbl.label, run_time=1.0, time_width=1.5),
                      run_time=1.0)
            c.wait_until(own_word=l2)
            rt = min(1.0, c.until(floor=0.6))
            self.play(GrowFromCenter(b2), *appear(l2), FlashAround(tbl.head, run_time=rt, time_width=1.5),
                      run_time=rt)

    # ---------------------------------------------------------------- c8.unnest.2
    def clip2(self):
        chips = self.chips
        q = Code(QUERY, Q_SIZE)
        q.move_to(ORIGIN).align_to([Q_LEFT, 0, 0], LEFT).align_to([0, Q_TOP, 0], UP)
        self.q = q
        t = _t_table()
        targets = []
        for i, (ch, n) in enumerate(zip(chips, CAST)):
            ch.target = H.chip(n).scale(CHIP_S).move_to([t.cx, t.row_y(i), 0])
            targets.append(ch.target)
        braces = [VGroup(_curly(tg, LEFT), _curly(tg, RIGHT)) for tg in targets]
        res = table(["name", "roles"], CAST_ROLES, [[FG, TEAL]] * 10, size=19, pitch=ROW_PITCH,
                    serif={0: H.CHIP_S * CHIP_S})
        place(res, Q_LEFT, ROW_TOP)
        call = q.find(UNNEST_CALL)

        with self.say("c8.unnest.2") as c:
            sweep_clear(self, *during(appear(q), 0.5, 1), keep=chips)
            c.wait_until("from")
            box = token_box(call, q.line(1))
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("single arrow")
            self.play(Transform(box, token_box(q.find("->", line=1), q.line(1))), run_time=0.8)
            c.wait_until("rows")
            self.play(*during(appear(t.frame, t.head, t.label, lag=0.1), 0, 0.5),
                      *during([MoveToTarget(ch) for ch in chips], 0.2, 1.0),
                      Transform(box, token_box(call, q.line(1))), run_time=1.8)
            self.play(*appear(*braces, shift=None, lag=0.08), run_time=1.0)
            c.wait_until("select")
            self.play(*appear(res.frame, res.head, lag=0.15),
                      Transform(box, token_box(q.find("a->>'name'"), q.line(0))), run_time=1.0)
            c.wait_until("double arrow")
            names = [res.rows[i][0] for i in range(10)]
            flies = []
            for k, (ch, dst) in enumerate(zip(chips, names)):
                flies += during(fly(ch.text, dst, arc=0), 0.04 * k, 0.64 + 0.04 * k)
            self.play(*flies, run_time=2.0)
            c.wait_until("single arrow", nth=1)
            self.play(Transform(box, token_box(q.find("a->'roles'"), q.line(0))),
                      *appear(*[res.rows[i][1] for i in range(10)], shift=0.15 * LEFT, lag=0.08),
                      run_time=min(1.6, c.until(floor=0.8)))
        self.box = box

    # ---------------------------------------------------------------- c8.unnest.3
    def clip3(self):
        q = self.q
        loop = loop_picture()
        cursor = loop.cursor
        kid = _loop_rows(loop, CAST)
        sher = _loop_rows(loop, SHERLOCK)
        comma = q.find(",", line=1)[0]
        mv = q.find("movie", line=1, nth=1)
        mv_cols = [g.get_color() for g in mv]
        row = K7.toolkit_card().rows[4].copy()
        row.move_to([-1.2, 1.2, 0])
        xm = Text("×", font=K7.GLYPH_FONT, font_size=30, color=DIM).move_to(comma.get_center() + 0.06 * UP)
        strike = Line(xm.get_corner(DL) + 0.06 * DL, xm.get_corner(UR) + 0.06 * UR).set_stroke(RED, 4)
        each = T("for each movie", 30, YELLOW).move_to([-4.4, 1.2, 0])

        with self.say("c8.unnest.3") as c:
            self.play(FlashAround(q.find(UNNEST_CALL), run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("comma")
            sweep_clear(self, *during(appear(loop.left, loop.card, loop.counter, loop.counter_label, lag=0.15)
                                      + [FadeIn(cursor)], 0.5, 1),
                        *during(FlashAround(comma, time_width=1.5, buff=0.08), 0.4, 1), keep=[q],
                        run_time=1.6)
            c.wait_until("comma", nth=1)
            self.play(*appear(row), run_time=1.0)
            self.play(*during(FadeIn(xm), 0.5, 1), *during(restyle(comma, 0), 0, 0.45),
                      FlashAround(row.glyph, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("depends")
            self.play(*recolor(mv, YELLOW), FlashUnder(mv, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("computed")
            self.play(Create(strike), run_time=0.6)
            self.play(*swap(row, each), *during(disappear(xm, strike), 0, 0.45),
                      *during(restyle(comma, 1), 0.5, 1), run_time=1.2)
            c.wait_until("outer")
            self.play(*appear(*kid, lag=0.08), run_time=1.6)
            C2.set_count(self, loop, 10, run_time=0.8)
            c.wait_until("just like")
            self.play(*C2.move_cursor(loop, 1), *swap(kid, sher), run_time=1.2)
            C2.set_count(self, loop, 20, run_time=0.6)
            res = table(["name", "roles"], RESULT4, [[FG, TEAL]] * 4, size=28, pitch=0.6)
            place(res, -res.frame[0].width / 2, 1.0)
            c.wait_until("result")
            sweep_clear(self, *during(appear(res.frame, res.head, lag=0.15), 0.5, 1),
                        *[g.animate.set_color(col) for g, col in zip(mv, mv_cols)], keep=[q])
            self.play(FlashUnder(q.line(3), run_time=1.2, time_width=1.5), run_time=1.0)
            for k, cue in enumerate(["Albert Austin", "F", "Beulah", "Carl Miller"]):
                c.wait_until(cue)
                self.play(*appear(res.rows[k], lag=0), run_time=0.8)
        self.res = res

    # ---------------------------------------------------------------- c8.unnest.4
    def clip4(self):
        q, res = self.q, self.res
        lx, rx = -3.2, 3.6
        h1 = Code(WHERE_TITLE, Q_SIZE).move_to([lx, 1.15, 0])
        h2 = Code(WHERE_ID, Q_SIZE).move_to([rx, 1.15, 0])
        left = _names_list(CAST, lx, 0.62)
        right = _names_list(CAST[::-1], rx, 0.62)
        cap = T("no ORDER BY, no order", 34, YELLOW).move_to([0, -3.1, 0])

        with self.say("c8.unnest.4") as c:
            self.play(*_alpha(list(q.line(3)) + list(q.line(4)), DIMMED), run_time=1.0)
            c.wait_until("title")
            self.play(*disappear(res), run_time=0.7)
            self.play(*appear(h1), FlashUnder(q.line(2), run_time=1.2, time_width=1.5), run_time=1.0)
            self.play(*appear(*left, lag=0.1), run_time=1.6)   # early: the run's whole result, then walked
            c.wait_until("Chaplin")
            self.play(left[0].animate.set_color(YELLOW), FlashAround(left[0], run_time=1.0), run_time=1.0)
            c.wait_until("id")
            self.play(*appear(h2), run_time=0.9)
            self.play(*appear(*right, lag=0.1), run_time=1.6)   # early: the run's whole result, then walked
            arrow = Arrow(left[0].get_right() + 0.1 * RIGHT, right[-1].get_left() + 0.1 * LEFT, buff=0.1,
                          stroke_width=4, color=YELLOW)
            self.play(GrowArrow(arrow), right[-1].animate.set_color(YELLOW), run_time=1.2)
            c.wait_until("never")
            self.play(*appear(cap), run_time=1.0)

    # ---------------------------------------------------------------- c8.unnest.5
    def clip5(self):
        un = Code(UNNEST_CALL, 20)
        un.move_to(ORIGIN).align_to([-6.35, 0, 0], LEFT).align_to([0, 3.35, 0], UP)
        un_f = D.fit_frame(un, pad=0.15)
        jq = Code(JOINQ, 18)
        jq.move_to(ORIGIN).align_to([6.55, 0, 0], RIGHT).align_to([0, 3.5, 0], UP)
        jq_f = SurroundingRectangle(jq, buff=0.12, corner_radius=0.15).set_stroke(BLUE, 2.5).set_fill(BLUE, 0.05)
        j4 = table(["title", "role", "name"], JOIN4, [[FG, FG, FG]] * 4, size=20, pitch=0.4)
        place(j4, 6.55 - j4.frame[0].width, 1.0)
        j12 = table(["title", "role", "name"], JOIN_ROWS, [[FG] * 3] * 12, size=18, pitch=0.33)
        place(j12, 6.55 - j12.frame[0].width, 1.0)
        g12 = T("12 rows", 36, GOLD).move_to([-2.4, -1.2, 0])
        # from {ten}: both results side by side, readable (serif cells, the join without `title`)
        TOP, GAP = 2.5, 0.3
        jb = table(["role", "name"], [r[1:] for r in JOIN_ROWS],
                   [[YELLOW if r[2] in TWO_PARTS else FG] * 2 for r in JOIN_ROWS],
                   size=20, pitch=0.4, pad=0.12, serif={0: 20, 1: 20})
        u10 = table(["name", "roles"], CAST_ROLES, [[FG, TEAL]] * 10, size=20, pitch=0.4,
                    pad=0.12, serif={0: 20, 1: 20})
        for r in u10.rows:     # roles: put the first capital (after `["`) on the name's baseline
            r[1].shift(UP * (r[0][0].get_bottom()[1] - r[1][2].get_bottom()[1]))
        wu, wj = u10.frame[0].width, jb.frame[0].width
        x0 = -(wu + GAP + wj) / 2
        place(u10, x0, TOP)
        place(jb, x0 + wu + GAP, TOP)
        g10 = T("10 rows", 36, GOLD).next_to(u10.frame, DOWN, buff=0.3).align_to(u10.frame, LEFT)
        tag_doc = T("documents", 30, TEAL).next_to(g10, RIGHT, buff=0.4)
        g12_to = T("12 rows", 36, GOLD).next_to(jb.frame, DOWN, buff=0.3).align_to(jb.frame, LEFT)
        tag_tab = T("tables", 30, BLUE).next_to(g12_to, RIGHT, buff=0.4)

        with self.say("c8.unnest.5") as c:
            sweep_clear(self, *during(appear(VGroup(un_f, un), VGroup(jq_f, jq), lag=0.3), 0.5, 1), keep=())
            self.play(*appear(j4, shift=None), run_time=1.0)
            c.wait_until("twelve")
            self.play(*_alpha(list(jq.line(6)), DIMMED), run_time=0.8)
            self.play(*swap(j4, j12), *appear(g12), run_time=1.4)
            c.wait_until("Albert Austin")
            ys = [i for i, r in enumerate(JOIN_ROWS) if r[2] in TWO_PARTS]
            self.play(*[cell.animate.set_color(YELLOW) for i in ys for cell in j12.rows[i]], run_time=1.0)
            c.wait_until("ten")
            self.play(*during(disappear(jq_f, jq, g12), 0, 0.45), *swap(j12, jb), run_time=1.4)
            g12 = g12_to
            self.play(*appear(u10, shift=None), *appear(g10, g12), run_time=1.2)
            two = [i for i, (n, _) in enumerate(CAST_ROLES) if n in TWO_PARTS]
            self.play(*[u10.rows[i][1].animate.set_color(YELLOW) for i in two],
                      *flash([u10.rows[i][1] for i in two]), run_time=1.2)
            c.wait_until("depends")
            self.play(*flash([g12, g10], color=GOLD), run_time=1.2)
            c.wait_until(own_word=tag_tab)
            self.play(*appear(tag_tab), run_time=0.9)
            c.wait_until(own_word=tag_doc)
            self.play(*appear(tag_doc), run_time=0.9)
