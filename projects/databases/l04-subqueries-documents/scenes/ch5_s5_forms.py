"""Chapter 5, scene 5: normal forms (1NF, the ladder, plays_role's title). Clips c5.forms.1 – c5.forms.4.

Exports (import with `F = load_scene("ch5_s5_forms")`), all static, built at ORIGIN:

    F.title_card(size=20, pitch=0.4) -> VGroup, the plays_role card with The Kid's 12 rows
        (ch1 kid_table look: label BLUE bold, IDs DIM, roles YELLOW) and the GOLD title column.
        .base       RowTable (ch1_s2_schema): .label .frame .head .rows[i] .cell(i, j), 3 columns
        .title_col  VGroup(.frame (BLUE outline: top/right/bottom + header line, open on the left,
                    meets .base's right edge), .head ("title"), .cells (12 GOLD "The Kid"))
        The whole card (base + column) is centred at ORIGIN; .base alone is therefore left of
        centre. Grow the column with e.g. appear(card.title_col) or GrowFromEdge(.., LEFT).
    F.list_cell(size=28) -> VGroup(.box BLUE, .value Mono "[Comedy, Drama, Family]",
        brackets TEAL, names YELLOW): DuckDB's list() result cell.
    F.recap_r4(size=24) -> VGroup(.rows (has_genre RowTable, The Kid's 3 rows),
        .array (json line '"genres": ["Comedy", "Drama", "Family"]')) side by side.
    F.genres_line(size=28) -> that json line on its own; F.PLAYS (the 12 rows, verified).
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
D = load_scene("ch4_s3_movie")

TT = "tt0012349"
PLAYS = [   # SELECT * FROM plays_role WHERE movie_id = 'tt0012349' ORDER BY ALL (12 rows)
    [TT, "nm0000122", "A Tramp"], [TT, "nm0001067", "The Child"],
    [TT, "nm0042317", "Car Thief"], [TT, "nm0042317", "Man in Shelter"],
    [TT, "nm0047800", "Bride"], [TT, "nm0048798", "Slum Nurse"],
    [TT, "nm0074788", "Night Shelter Keeper"], [TT, "nm0074788", "Professor Guido"],
    [TT, "nm0080930", "Orphan Asylum Driver"], [TT, "nm0088471", "His Assistant"],
    [TT, "nm0588033", "The Man"], [TT, "nm0701012", "The Woman"],
]
LIST_VAL = "[Comedy, Drama, Family]"
GENRES_JSON = '"genres": ["Comedy", "Drama", "Family"]'
SQL = """SELECT m.title, list(g.name) AS genres
FROM movies m
JOIN has_genre hg ON hg.movie_id = m.movie_id
JOIN genres g ON g.genre_id = hg.genre_id
WHERE m.movie_id = 'tt0012349'
GROUP BY m.title;"""


def row_table(name, size=24, pitch=0.5):
    cols = SCH.SCHEMA[name][0]
    rows = SCH.KID_ROWS[name]
    colors = [[SCH._kid_color(c, v) for c, v in zip(cols, r)] for r in rows]
    return SCH.RowTable(name, cols, rows, colors, size=size, pitch=pitch)


def _tint_list(val):
    for ch in "[]":
        for g in select(val, ch):
            g.set_color(TEAL)
    return val


def title_card(size=20, pitch=0.4):
    cols = SCH.SCHEMA["plays_role"][0]
    colors = [[SCH._kid_color(c, v) for c, v in zip(cols, r)] for r in PLAYS]
    base = SCH.RowTable("plays_role", cols, PLAYS, colors, size=size, pitch=pitch)
    box = base.frame[0]
    W, H = box.width, box.height
    x0, y0 = box.get_left()[0], box.get_top()[1]
    pad = 0.15
    w = max(Mono("title", size, weight=BOLD).width, Mono("The Kid", size).width) + 2 * pad
    outline = VMobject().set_points_as_corners([
        [x0 + W, y0, 0], [x0 + W + w, y0, 0], [x0 + W + w, y0 - H, 0], [x0 + W, y0 - H, 0]])
    outline.set_stroke(BLUE, 2)
    hline = Line([x0 + W, y0 - pitch, 0], [x0 + W + w, y0 - pitch, 0]).set_stroke(BLUE, 2)
    frame = VGroup(outline, hline)
    head = SCH._placed("title", size, FG, BOLD, y0 - pitch / 2, left=x0 + W + pad)[0]
    cells = VGroup(*[SCH._placed("The Kid", size, GOLD, NORMAL, y0 - pitch * (i + 1.5),
                                 left=x0 + W + pad)[0] for i in range(len(PLAYS))])
    col = VGroup(frame, head, cells)
    col.frame, col.head, col.cells = frame, head, cells
    card = VGroup(base, col)
    card.base, card.title_col = base, col
    card.move_to(ORIGIN)
    return card


def list_cell(size=28):
    val = _tint_list(Mono(LIST_VAL, size, YELLOW))
    box = Rectangle(width=val.width + 0.5, height=0.0095 * size * 3.2 + 0.2).set_stroke(BLUE, 2)
    box.move_to(val)
    g = VGroup(box, val)
    g.box, g.value = box, val
    return g.move_to(ORIGIN)


def genres_line(size=28):
    return D.json_code(GENRES_JSON, size=size)


def recap_r4(size=24):
    rows = row_table("has_genre", size=size)
    arr = genres_line(size + 2)
    g = VGroup(rows, arr).arrange(RIGHT, buff=0.8)
    g.rows, g.array = rows, arr
    return g.move_to(ORIGIN)


def movies_row():
    """The Kid's movies row with a dashed ghost column `genres` holding the list."""
    tab = row_table("movies", size=24, pitch=0.5)
    box = tab.frame[0]
    W, H, pitch, size, pad = box.width, box.height, 0.5, 24, 0.15
    x0, y0 = box.get_left()[0], box.get_top()[1]
    head = SCH._placed("genres", size, DIM, BOLD, y0 - pitch / 2, left=x0 + W + pad)[0]
    val = SCH._placed(LIST_VAL, size, YELLOW, NORMAL, y0 - pitch * 1.5, left=x0 + W + pad)[0]
    _tint_list(val)
    w = val.width + 2 * pad
    outline = VMobject().set_points_as_corners([
        [x0 + W, y0, 0], [x0 + W + w, y0, 0], [x0 + W + w, y0 - H, 0], [x0 + W, y0 - H, 0]])
    frame = VGroup(DashedVMobject(outline, num_dashes=40),
                   DashedLine([x0 + W, y0 - pitch, 0], [x0 + W + w, y0 - pitch, 0], dash_length=0.1))
    frame.set_stroke(DIM, 2)
    ghost = VGroup(frame, head, val)
    ghost.frame, ghost.head, ghost.val = frame, head, val
    g = VGroup(tab, ghost)
    g.tab, g.ghost = tab, ghost
    return g


def crack(val, a, b):
    """RED zigzag in the space between glyph groups a and b of the list value."""
    x = (a.get_right()[0] + b.get_left()[0]) / 2
    top, bot = val.get_top()[1] + 0.12, val.get_bottom()[1] - 0.12
    n = 5
    pts = [[x + (0.05 if k % 2 else -0.05), top + (bot - top) * k / n, 0] for k in range(n + 1)]
    return VMobject().set_points_as_corners(pts).set_stroke(RED, 4)


class Ch5S5Forms(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── 1NF: atomic values, has_genre ────────────────────────────────────────
    def clip1(self):
        with self.say("c5.forms.1") as c:
            title = T("Normal forms", 48).move_to([0, 3.35, 0])
            self.play(*appear(title), run_time=min(1.0, c.until("first")))  # early: the topic heading, shown as the line starts
            c.wait_until("first")

            t1 = T("First normal form (1NF)", 48, YELLOW).move_to([0, 3.35, 0])
            self.play(*swap(title, t1), run_time=min(1.2, c.until("Every value")))
            c.wait_until("Every value")

            sub = T("every value in a table is atomic", 36).move_to([0, 2.72, 0])
            self.play(*appear(sub), run_time=1.0)
            c.wait_until("meaning")
            note = T("(a single number or string, not a list or nested record)", 28, DIM)
            note.move_to([0, 2.2, 0])
            self.play(*appear(note), run_time=1.0)

            mv = movies_row()
            mv.move_to([0, 0, 0])
            place = mv.tab.frame[0].get_top()[1]
            mv.shift(UP * (1.3 - place))
            self.mv = mv
            c.wait_until("never a list")
            self.play(*appear(mv.tab), run_time=1.0)
            self.play(*appear(mv.ghost, shift=None), run_time=1.0)
            c.wait_until("genres")

            val = mv.ghost.val
            names = [select(val, n)[0] for n in ("Comedy", "Drama", "Family")]
            cracks = [crack(val, names[0], names[1]), crack(val, names[1], names[2])]
            self.play(*recolor(mv.ghost.frame, RED), mv.ghost.head.animate.set_color(RED),
                      *[Create(k) for k in cracks], run_time=1.5)
            c.wait_until("cannot sit")

            hg = row_table("has_genre")
            gn = row_table("genres")
            hg.move_to([-2.9, 0, 0])
            gn.move_to([3.2, 0, 0])
            for t in (hg, gn):
                t.shift(UP * (-0.8 - t.frame[0].get_top()[1]))
            self.hg, self.gn = hg, gn
            self.play(*appear(gn.label, gn.frame, *[gn.cell(i, 0) for i in range(3)], lag=0.1),
                      run_time=1.0)
            flights = []
            for k, i in enumerate((2, 1, 0)):   # bottom row first: no copy crosses a landed one
                flights += [time_span(a, 0.6 * k, 0.6 * k + 0.9) for a in fly(names[i], gn.cell(i, 1))]
            self.play(*flights, run_time=2.1)
            self.play(*disappear(mv.ghost, *cracks), *appear(gn.head, shift=None), run_time=0.8)
            settle(self, gn)
            c.wait_until("rows")

            arrows = []
            for i in range(3):
                y = hg.rows[i].get_y()
                arrows.append(Arrow([hg.frame[0].get_right()[0] + 0.08, y, 0],
                                    [gn.frame[0].get_left()[0] - 0.08, y, 0], buff=0,
                                    stroke_width=3, tip_length=0.16, color=FG))
            self.arrows = VGroup(*arrows)
            self.play(*appear(hg.label, hg.frame, hg.head, lag=0.1), run_time=0.8)
            self.play(*appear(*hg.rows, lag=0.4), *[time_span(GrowArrow(a), 0.5 + 0.4 * i, 1.3 + 0.4 * i)
                                                     for i, a in enumerate(arrows)],
                      run_time=min(2.1, c.until(None)))
            settle(self, hg)
            self.heading = VGroup(t1, sub, note)

    # ── documents break 1NF; DuckDB's list() ─────────────────────────────────
    def clip2(self):
        hg = self.hg
        with self.say("c5.forms.2") as c:
            doc = D.kid_doc(size=14).move_to([2.5, 0.75, 0])
            sweep_clear(self, hg.animate.move_to([-4.5, 0.75, 0]), keep=[hg], run_time=1.2)
            self.play(*appear(doc, shift=None), run_time=min(1.0, c.until("Its genres")))
            c.wait_until("Its genres")

            line = genres_line(28).move_to([0, -2.75, 0])
            keep6 = set(id(g) for g in doc.code.line(6))
            rest = [g for g in doc.code.text.submobjects if id(g) not in keep6]
            self.play(*[g.animate.set_opacity(0.2) for g in rest], run_time=0.8)
            self.play(*fly(doc.code.line(6), line), run_time=1.5)
            c.wait_until("violates")
            tag = T("violates 1NF, by design", 32, RED).move_to([0, -3.4, 0])
            self.play(*appear(tag), run_time=1.0)  # early: names what "break first normal form by design" says
            c.wait_until("list")

            code = Code(SQL, size=28)
            code.move_to(ORIGIN)
            code.shift(np.array([0, 3.3 - code.get_top()[1], 0]))   # centred across the frame
            self.play(*during(disappear(doc), 0, 0.4),
                      *during([hg.animate.move_to([4.6, -0.5 + hg.get_center()[1] - hg.frame[0].get_top()[1], 0])],
                             0.4, 1.0),
                      run_time=1.5)
            self.play(*appear(code, shift=None), run_time=1.0)
            c.wait_until("The list aggregate")

            box = token_box(code.find("list(g.name)"), code.line(0))
            res = SCH.RowTable(None, ["title", "genres"], [["The Kid", LIST_VAL]], [[FG, YELLOW]],
                               size=28, pitch=0.6)
            res.head.set_color(DIM)
            _tint_list(res.cell(0, 1))
            # left of has_genre (still on the right) while the rows fold in; centred afterwards
            res.shift(np.array([-1.3 - res.get_x(), -0.75 - res.get_top()[1], 0]))
            self.play(FadeIn(box), *during(disappear(line, tag), 0, 0.5),
                      *during(appear(res.frame, res.head, res.cell(0, 0), shift=None), 0.4, 1.0), run_time=1.3)
            tgt = res.cell(0, 1)
            # the table's frame clears first, so no row crosses its border; rows leave 0.35 s apart
            fold = [time_span(row.animate.move_to(tgt).scale(0.6).set_opacity(0), 0.45 + 0.35 * i, 1.25 + 0.35 * i)
                    for i, row in enumerate(hg.rows)]
            self.play(*fold, *during(appear(tgt, shift=None), 0.75, 1.0),
                      *during(disappear(hg.label, hg.frame, hg.head), 0, 0.22), run_time=2.0)
            self.remove(*hg.get_family())
            self.box, self.code, self.res = box, code, res
            c.wait_until("mean")
            self.play(*during([res.animate.set_x(0)], 0, 0.6), run_time=1.0)
            mean = T("many databases support JSON and list/array types", 30, DIM).move_to([0, -3.1, 0])
            self.play(*appear(mean), run_time=1.0)

    # ── the ladder; plays_role's title ───────────────────────────────────────
    def clip3(self):
        with self.say("c5.forms.3") as c:
            parts = ["1NF", "→", "2NF", "→", "3NF", "→", "BCNF", "→", "…"]
            lad = VGroup(*[T(p, 56, YELLOW if k == 0 else DIM) for k, p in enumerate(parts)])
            lad.arrange(RIGHT, buff=0.35).move_to([0, 0.3, 0])
            sweep_clear(self, *appear(lad[0]), run_time=min(1.4, c.until("second")))
            for k, cue in ((1, "second"), (3, "third"), (5, "Boyce-Codd"), (7, "and others")):
                c.wait_until(cue)
                self.play(*appear(lad[k], lad[k + 1], lag=0.2, shift=None), run_time=0.8)
            self.ladder = lad
            c.wait_until("example")

            card = title_card()
            card.shift(np.array([-6.5 - card.get_left()[0], 2.95 - card.get_top()[1], 0]))
            self.play(lad.animate.scale(0.6).move_to([0, 3.5, 0]), run_time=1.0)
            self.play(*appear(card, shift=None), run_time=1.0)
            c.wait_until("depends")

            base, col = card.base, card.title_col
            bot = base.frame[0].get_bottom()[1] - 0.08
            arr = CurvedArrow([base.head[0].get_x(), bot, 0], [col.head.get_x(), bot, 0], angle=0.5,
                              color=RED, stroke_width=4, tip_length=0.2)
            self.play(Create(arr), FlashAround(base.head[0], color=RED, run_time=1.5, time_width=1.5),
                      run_time=1.5)
            c.wait_until("only part")
            ul = [underline(base.head[j], YELLOW, buff=0.04).set_stroke(width=3) for j in range(3)]
            red = T("determined by\npart of the key", 32, RED)
            red.next_to(card, RIGHT, buff=0.4).align_to(card.base.frame[0], DOWN)
            self.play(*[GrowFromCenter(u) for u in ul], run_time=0.8)
            self.play(*appear(red), run_time=1.0)
            c.wait_until("That's the kind")
            self.play(FlashAround(col.cells, color=GOLD, time_width=1.5), run_time=1.5)
            self.card_stuff = [card, arr, red, *ul]

    # ── one fact, one place; break it on purpose ─────────────────────────────
    def clip4(self):
        with self.say("c5.forms.4") as c:
            self.play(*set_alpha([self.ladder], DIMMED), *disappear(*self.card_stuff),
                      run_time=min(1.2, c.until("The idea")))
            c.wait_until("The idea")
            idea = T("one fact, one place", 52, YELLOW).move_to([0, 0.9, 0])
            self.play(*appear(idea), run_time=1.0)
            c.wait_until("choice")
            line = genres_line(30).move_to([0, -1.0, 0])
            self.play(*appear(line, shift=None), run_time=1.0)
            tag = T("break it on purpose", 36, GREEN).move_to([0, -1.9, 0])
            self.play(*appear(tag), run_time=1.0)  # early: the tag sums up "breaking a normal form ... deliberate"
            c.wait_until("Just do it")
            self.play(FlashUnder(tag, color=GREEN, time_width=1.5), run_time=1.2)
