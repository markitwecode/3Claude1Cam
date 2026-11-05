"""Chapter 4, scene 4: Chaplin as a document. Clips c4.person.1 – c4.person.4.

Exports (static, built at ORIGIN; `P = load_scene("ch4_s4_person")`):
    P.chaplin_doc(size=16) -> DocCard of CHAPLIN_DOC, slide 72's card (22 lines; ~8.2 x 7.3 at 16).
           P.CHAPLIN_LINES its lines: 0 "{", 1-4 id/name/years, 5-19 acted_in, 18 "/* 3 more */",
           20 the "also directed, ..." comment, 21 "}".
    P.hitch_doc(size=24) -> DocCard of HITCH_DOC, Hitchcock's five keys (~6.6 x 3.8 at 24).
    P.recap_thumb() -> VGroup(chaplin, hitch): Chaplin's long card (height 3.6) beside
           Hitchcock's short one, as in clip 2 ({r3} of the recap).
    P.directed_code(size=15.5) -> Chaplin's real directed array, one element per line (JSON colours).
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

CHAPLIN_LINES = [
    '{',
    '  "person_id": "nm0000122",',
    '  "name": "Charles Chaplin",',
    '  "birthyear": 1889,',
    '  "deathyear": 1977,',
    '  "acted_in": [',
    '    {',
    '      "movie_id": "tt0012349",',
    '      "title": "The Kid",',
    '      "year": 1921,',
    '      "roles": ["A Tramp"]',
    '    },',
    '    {',
    '      "movie_id": "tt0015864",',
    '      "title": "The Gold Rush",',
    '      "year": 1925,',
    '      "roles": ["The Lone Prospector"]',
    '    },',
    '    /* 3 more */',
    '  ],',
    '  /* also "directed", "produced", "wrote", "composed_for" */',
    '}',
]
CHAPLIN_DOC = "\n".join(CHAPLIN_LINES)

HITCH_LINES = [
    '{',
    '  "person_id": "nm0000033",',
    '  "name": "Alfred Hitchcock",',
    '  "birthyear": 1899,',
    '  "deathyear": 1980,',
    '  "directed": [/* 7 items */ ]',
    '}',
]
HITCH_DOC = "\n".join(HITCH_LINES)

# a person with no known birth year (movies.duckdb people row; movies-json.duckdb document)
ARAKAWA_DOC = "\n".join([
    '{',
    '  "person_id": "nm0032875",',
    '  "name": "Tarô Arakawa",',
    '',
    '  "deathyear": 2012,',
    '  "acted_in": [/* 1 item */ ]',
    '}',
])

DIRECTED_SRC = """"directed": [
  {"movie_id": "tt0012349", "title": "The Kid", "year": 1921, "job": "director"},
  {"movie_id": "tt0015864", "title": "The Gold Rush", "year": 1925},
  {"movie_id": "tt0021749", "title": "City Lights", "year": 1931},
  {"movie_id": "tt0027977", "title": "Modern Times", "year": 1936, "job": "director"},
  {"movie_id": "tt0032553", "title": "The Great Dictator", "year": 1940}
]"""
DIRECTED_JOBS = ["director", "NULL", "NULL", "director", "NULL"]

KEYS_SQL = """SELECT json_keys(person)
FROM people
WHERE person_id = 'nm0000033';"""
KEYS_REPLY = "[person_id, name, birthyear, deathyear, directed]"

ACTED_CHIPS = ["City Lights 1931", "Modern Times 1936", "The Great Dictator 1940"]
HITCH_CHIPS = [["Rebecca 1940", "Dial M for Murder 1954", "Rear Window 1954", "Vertigo 1958"],
               ["North by Northwest 1959", "Psycho 1960", "The Birds 1963"]]


def chaplin_doc(size=16):
    return D.doc_card(CHAPLIN_DOC, size=size)


def hitch_doc(size=24):
    return D.doc_card(HITCH_DOC, size=size)


def recap_thumb():
    ch = chaplin_doc()
    ch.scale(3.6 / ch.height)
    hi = hitch_doc()
    g = VGroup(ch, hi).arrange(RIGHT, buff=0.7, aligned_edge=UP)
    return g.move_to(ORIGIN)


def directed_code(size=15.5, line_spacing=2.0):
    """D.json_code's colours on a Code with wider line spacing (rows line up with a table)."""
    code = Code(DIRECTED_SRC, size=size, line_spacing=line_spacing, lang="json")
    glyphs = code.text.submobjects
    roles = D._roles(code.src)
    if len(roles) == len(glyphs):
        col = {"brace": TEAL, "comment": DIM, "null": PINK}
        for g, r in zip(glyphs, roles):
            if r:
                g.set_color(col[r])
    else:
        for ch in "{}[]":
            for g in chars(code, ch):
                g.set_color(TEAL)
    return code


def chip(text, size=28, color=DIM, pad=0.18):
    t = T(text, size, color)
    box = (RoundedRectangle(corner_radius=0.12, width=t.width + 2 * pad, height=t.height + 0.3)
           .set_stroke(DIM, 2).set_fill(BG, 0))
    box.move_to(t)
    return VGroup(box, t)


def lines_box(code, i, j, color=YELLOW, padx=0.14, pady=0.07):
    g = VGroup(*[code.line(k) for k in range(i, j + 1)])
    r = (Rectangle(width=g.width + 2 * padx, height=g.height + 2 * pady)
         .set_stroke(color, 2).set_fill(color, 0.12))
    return r.move_to(g).set_z_index(-1)


def stack_icon(label, color):
    frames = VGroup(*[RoundedRectangle(corner_radius=0.1, width=1.2, height=0.85)
                      .set_stroke(color, 2.5).set_fill(BG, 1).shift(i * 0.14 * (UP + RIGHT))
                      for i in range(3)][::-1])
    t = Mono(label, 28, color)
    t.next_to(frames, DOWN, buff=0.2)
    return VGroup(frames, t)


class Ch4S4Person(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1: Chaplin's document
    def clip1(self):
        card = chaplin_doc(16)
        card.move_to([-6.6 + card.width / 2, 0, 0])
        code = card.code
        self.card = card
        people = stack_icon("people", TEAL).move_to([3.3, 1.9, 0])
        movies = stack_icon("movies", DIM).move_to([5.5, 1.9, 0])
        with self.say("c4.person.1") as c:
            self.play(*appear(card, shift=None),  # early: the whole document first, then walked
                      run_time=min(1.5, c.until("stored")))
            c.wait_until("stored")
            self.play(*appear(people, movies, lag=0.3), run_time=min(1.2, c.until("top")))

            c.wait_until("top")
            box = lines_box(code, 1, 4)
            self.play(FadeIn(box), run_time=min(1.0, c.until("acted")))

            c.wait_until("acted")
            self.play(Transform(box, lines_box(code, 5, 19)), run_time=min(1.5, c.until("roles")))
            c.wait_until("roles")
            self.play(*flash([code.find('"roles"', nth=0), code.find('"roles"', nth=1)]),
                      run_time=min(1.5, c.until("five")))

            c.wait_until("five")
            com = code.line(18)
            self.play(Transform(box, lines_box(code, 18, 18)), run_time=min(1.0, c.until("from the kid")))
            chips = VGroup(*[chip(s) for s in ACTED_CHIPS]).arrange(DOWN, buff=0.28)
            chips.move_to([4.4, 0, 0])
            chips.shift(UP * (com.get_y() - chips[1].get_y()))
            self.play(FlashAround(com, run_time=1.2, time_width=1.5),
                      *during(appear(*chips, shift=0.3 * RIGHT, lag=0.35), 0.25, 1.0),
                      run_time=min(1.8, c.until("more")))

            c.wait_until("more")
            self.play(Transform(box, lines_box(code, 20, 20)), *recolor(code.line(20), YELLOW),
                      run_time=min(1.2, c.until("produced")))
            self.play(FlashAround(code.line(20), run_time=1.5, time_width=1.5))
        self.box, self.chips1, self.icons = box, chips, VGroup(people, movies)

    # ------------------------------------------------------------ c2: Hitchcock's five keys
    def clip2(self):
        card = self.card
        hcard = hitch_doc(24)
        hcard.move_to([2.0, 3.0 - hcard.height / 2, 0])
        hc = hcard.code
        target_w = 4.0
        sc = target_w / card.width
        ch_center = np.array([-4.0, 3.0 - card.height * sc / 2, 0])
        lab_c = T("Charles Chaplin", 30).move_to([ch_center[0], 3.45, 0])
        lab_h = T("Alfred Hitchcock", 30).move_to([hcard.get_x(), 3.45, 0])

        query = Code(KEYS_SQL, size=26)
        query.move_to([0, -2.05, 0])
        reply = Mono(KEYS_REPLY, 26)
        reply.move_to([0, -3.35, 0])

        with self.say("c4.person.2") as c:
            self.play(*during([FadeOut(self.box)] + disappear(self.chips1, self.icons), 0, 0.4),
                      *during([card.animate.scale(sc).move_to(ch_center)], 0.2, 0.75),
                      *during(appear(hcard, lab_c, lab_h, shift=None, lag=0.1), 0.6, 1.0),  # early: names of the two cards
                      run_time=min(2.0, c.until("keys")))

            c.wait_until("keys")
            self.play(*appear(query), run_time=min(1.0, c.until("just five")))
            c.wait_until("just five")
            self.play(*appear(reply), run_time=min(1.2, c.until("person ID")))

            keys = ["person_id", "name", "birthyear", "deathyear", "directed"]
            cues = ["person ID", "name", "birth year", "death year", "an array called directed"]
            c.wait_until("person ID")
            tb = token_box(select(reply, keys[0])[0], reply)
            self.play(FadeIn(tb), run_time=0.5)
            for k, cue in zip(keys[1:], cues[1:]):
                c.wait_until(cue)
                self.play(Transform(tb, token_box(select(reply, k)[0], reply)), run_time=0.5)

            c.wait_until("seven films")
            rows = [VGroup(*[chip(s) for s in r]).arrange(RIGHT, buff=0.15) for r in HITCH_CHIPS]
            chips = VGroup(*rows).arrange(DOWN, buff=0.22).move_to([0, -2.05, 0])
            self.play(*during(disappear(query), 0, 0.4),
                      *during(appear(*rows[0], *rows[1], shift=None, lag=0.12), 0.4, 1.0),
                      run_time=min(2.0, c.until("noacted")))

            # {noacted}: a ghost "acted_in" slot opens between deathyear and directed, then closes
            p = hc.line(3).get_y() - hc.line(4).get_y()
            tail = [g for k in (5, 6) for g in hc.line(k)]
            old_frame = hcard.frame.copy()
            tall = (RoundedRectangle(corner_radius=0.2, width=old_frame.width, height=old_frame.height + p)
                    .set_stroke(TEAL, 3).set_fill(TEAL, 0.06).move_to(old_frame, aligned_edge=UP))

            def slot_line(src):
                m = D.json_code(src, 24)
                m.set_color(DIM)
                m.move_to([0, hc.line(4).get_y() - p, 0]).align_to(hc.line(4), LEFT)
                return m

            c.wait_until("noacted")
            ghost = slot_line('"acted_in": [ … ],')
            self.play(Transform(hcard.frame, tall), *[g.animate.shift(DOWN * p) for g in tail],
                      FadeOut(tb), run_time=min(1.2, c.until("cameos")))
            self.play(*appear(ghost, shift=None), run_time=min(1.0, c.until("cameos")))
            c.wait_until("no acted in key")
            self.play(*flash([ghost], color=RED), run_time=min(1.2, c.until("rule")))

            c.wait_until("rule")
            rule = T("A key is there only if it applies.", 40, YELLOW).move_to([0, -2.5, 0])
            self.play(*during(disappear(ghost), 0, 0.35),
                      *during([Transform(hcard.frame, old_frame)] + [g.animate.shift(UP * p) for g in tail],
                              0.3, 0.75),
                      *swap(VGroup(chips, reply), rule), run_time=min(1.8, c.until("empty")))

            c.wait_until("empty")
            alt = slot_line('"acted_in": [],')
            fine = T("also fine", 30, GREEN)
            fine.move_to([0, alt.get_y(), 0]).align_to(hcard.frame, RIGHT).shift(LEFT * 0.4)
            self.play(*during([Transform(hcard.frame, tall)] + [g.animate.shift(DOWN * p) for g in tail],
                              0, 0.5),
                      *during(appear(alt, shift=None), 0.45, 0.8), *during(appear(fine), 0.65, 1.0),
                      run_time=min(1.6, c.until("leaves")))
        self.rule1 = rule

    # ------------------------------------------------------------ c3: unknown -> left out
    def clip3(self):
        cols = SCH.SCHEMA["people"][0]
        row = ["nm0032875", "Tarô Arakawa", "NULL", "2012"]
        colors = [[SCH._kid_color(cn, v) for cn, v in zip(cols, row)]]
        table = SCH.RowTable("people", cols, [row], colors, size=26, pitch=0.55)
        SCH.place(table, left=-6.0, top=3.45)
        null = table.cell(0, 2)

        doc = D.doc_card(ARAKAWA_DOC, size=24)
        SCH.place(doc, right=6.6, top=1.75)
        dc = doc.code
        name_k = dc.find('"name"')
        y_gap = (name_k.get_y() + dc.find('"deathyear"').get_y()) / 2
        gap = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=2.9, height=0.38)
                             .set_stroke(DIM, 2), num_dashes=28)
        gap.move_to([0, y_gap, 0]).align_to(name_k, LEFT).shift(LEFT * 0.06)

        n1 = T("8,775", 52, GOLD)
        c1 = T("people rows: birthyear NULL", 28, DIM)
        g1 = VGroup(n1, c1).arrange(DOWN, buff=0.15).move_to([-3.6, 0.85, 0])
        n2 = T("8,775", 52, GOLD)
        c2 = T("documents: no birthyear key", 28, DIM)
        g2 = VGroup(n2, c2).arrange(DOWN, buff=0.15).move_to([-3.6, -1.2, 0])

        x_n = null.get_x()
        corner = np.array([x_n, y_gap, 0])
        drop = Line([x_n, table.frame.get_bottom()[1] - 0.08, 0], corner).set_stroke(PINK, 4)
        into = Arrow(corner, gap.get_left() + LEFT * 0.05, buff=0, stroke_width=4,
                     max_tip_length_to_length_ratio=0.3).set_color(PINK)
        rule = T("NULL in a table  →  key left out", 40, t2c={"NULL": PINK}).move_to([0, -3.0, 0])

        with self.say("c4.person.3") as c:
            sweep_clear(self, *appear(table, shift=None), run_time=min(1.6, c.until("nobirth")))
            c.wait_until("nobirth")
            self.play(*flash([null], color=PINK), run_time=min(1.2, c.until("left out")))
            self.play(*appear(doc, shift=None), run_time=min(1.2, c.until("left out")))
            c.wait_until("left out")
            self.play(FadeIn(gap), run_time=min(1.0, c.until("instead")))

            c.wait_until("count")
            self.play(*appear(g1), run_time=min(1.0, c.until("people table")))
            c.wait_until("people table")
            self.play(*flash([null], color=PINK), run_time=min(1.2, c.until("documents")))
            c.wait_until("documents")
            self.play(*appear(g2), run_time=min(1.0, c.until("rule2")))

            c.wait_until("rule2")
            self.play(Create(drop), run_time=min(0.8, c.until("wherever")))
            self.play(GrowArrow(into), run_time=min(0.8, c.until("wherever")))
            c.wait_until("wherever")
            self.play(*appear(rule), run_time=min(1.2, c.until()))

    # ------------------------------------------------------------ c4: directed, job or no job
    def clip4(self):
        code = directed_code()
        p = code.line(0).get_y() - code.line(1).get_y()
        rows = [[j] for j in DIRECTED_JOBS]
        colors = [[PINK if j == "NULL" else YELLOW] for j in DIRECTED_JOBS]
        table = SCH.RowTable("has_position", ["job"], rows, colors, size=22, pitch=p)
        SCH.place(table, left=-6.5)
        code.move_to([0, 1.15, 0])
        SCH.place(code, left=table.frame.get_right()[0] + 0.45)
        box = table.frame[0]
        table.shift(UP * (code.line(0).get_y() + p / 2 - box.get_top()[1]))
        links = VGroup(*[Line([box.get_right()[0] + 0.06, code.line(i + 1).get_y(), 0],
                              [code.line(i + 1).get_left()[0] - 0.08, code.line(i + 1).get_y(), 0])
                         .set_stroke(DIM, 2) for i in range(5)])
        jobs = [code.find('"job": "director"', nth=k) for k in (0, 1)]
        short = [code.line(k) for k in (2, 3, 5)]
        nulls = [table.cell(i, 0) for i in (1, 2, 4)]

        n1 = T("731", 60, GOLD)
        t1 = T("with a job key", 32, DIM)
        g1 = VGroup(n1, t1).arrange(DOWN, buff=0.15).move_to([-3.0, -2.3, 0])
        n2 = T("2,435", 60, GOLD)
        t2 = T("without one", 32, DIM)
        g2 = VGroup(n2, t2).arrange(DOWN, buff=0.15).move_to([3.0, -2.3, 0])
        outlines = [SurroundingRectangle(code.line(k), buff=0.08, corner_radius=0.08)
                    .set_stroke(TEAL, 3) for k in range(1, 6)]

        with self.say("c4.person.4") as c:
            c.wait_until("directed")
            sweep_clear(self, *appear(code, table, shift=None, lag=0.3),
                        run_time=min(2.0, c.until("job")))
            self.play(*[Create(l) for l in links], run_time=min(0.8, c.until("job")))

            c.wait_until("job")
            self.play(*[r for j in jobs for r in recolor(j, YELLOW)],
                      *flash(jobs), run_time=min(1.5, c.until("nojob")))

            c.wait_until("nojob")
            self.play(*flash(short, color=PINK), *flash(nulls, color=PINK),
                      run_time=min(1.6, c.until("has position")))
            c.wait_until("has position")
            self.play(*flash(short, color=PINK), *flash(nulls, color=PINK),
                      run_time=min(1.6, c.until("count2")))

            c.wait_until("count2")
            self.play(*appear(g1), run_time=min(1.0, c.until("two thousand")))
            c.wait_until("two thousand")
            self.play(*appear(g2), run_time=min(1.0, c.until("free")))

            c.wait_until("free")
            self.play(*set_alpha([code], 0.4),
                      *appear(*outlines, shift=None, lag=0.2), run_time=min(1.8, c.until()))
