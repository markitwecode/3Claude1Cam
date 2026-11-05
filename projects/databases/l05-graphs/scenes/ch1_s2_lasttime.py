"""Chapter 1, scene 2: last time's tangle, stored as rows and as two trees. Clips c1.last.1 – c1.last.4."""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


# ---------------------------------------------------------------- the tangle (chapter anchor)
R_VERT = 0.5
TANGLE_POS = {
    "coogan": np.array([-2.4, 1.4, 0]),
    "chaplin": np.array([2.4, 1.4, 0]),
    "kid": np.array([-2.4, -1.4, 0]),
    "gold": np.array([2.4, -1.4, 0]),
}
TANGLE_NAMES = {"coogan": "Jackie Coogan", "chaplin": "Charles Chaplin",
                "kid": "The Kid", "gold": "The Gold Rush"}


def vertex(name, pos, color, label_side=DOWN):
    c = Circle(radius=R_VERT).set_stroke(color, 4).set_fill(color, 0.2).move_to(pos)
    lab = T(name, 32, FG).next_to(c, label_side, buff=0.14)
    v = VGroup(c, lab)
    v.circle, v.label = c, lab
    return v


def tangle():
    """Lecture 4's tangle: Coogan TL, Chaplin TR (PINK people), The Kid BL, The Gold Rush BR (BLUE movies).
    Lines Coogan–Kid, Chaplin–Kid, Chaplin–Gold Rush. Top names sit above their circles (so the
    lines leaving downward don't cross them), bottom names below. `.v[key]`, `.lines[i]`, `.people`,
    `.movies`."""
    v = {}
    for key in ("coogan", "chaplin"):
        v[key] = vertex(TANGLE_NAMES[key], TANGLE_POS[key], PINK, UP)
    for key in ("kid", "gold"):
        v[key] = vertex(TANGLE_NAMES[key], TANGLE_POS[key], BLUE, DOWN)
    pairs = [("coogan", "kid"), ("chaplin", "kid"), ("chaplin", "gold")]
    lines = [Line(TANGLE_POS[a], TANGLE_POS[b], buff=R_VERT).set_stroke(FG, 4) for a, b in pairs]
    g = VGroup(*lines, v["coogan"], v["chaplin"], v["kid"], v["gold"])
    g.v, g.lines = v, lines
    g.people, g.movies = [v["chaplin"], v["coogan"]], [v["kid"], v["gold"]]
    return g


def handover_shot():
    return tangle()


# ---------------------------------------------------------------- table cards
CELL_S = 28
COL_GAP = 0.45
ROW_PITCH = 0.43


def grid(rows, colors=None):
    """Rows of Mono cells in left-aligned columns. Returns VGroup of row VGroups (cells)."""
    cells = [[Mono(v, CELL_S, (colors[r][i] if colors else FG)) for i, v in enumerate(row)]
             for r, row in enumerate(rows)]
    ncol = max(len(r) for r in cells)
    widths = [max(row[i].width for row in cells if i < len(row)) for i in range(ncol)]
    xs = [sum(widths[:i]) + COL_GAP * i for i in range(ncol)]
    out = VGroup()
    for r, row in enumerate(cells):
        rg = VGroup()
        for i, cell in enumerate(row):
            cell.move_to([xs[i], -r * ROW_PITCH, 0], aligned_edge=LEFT)
            cell.set_y(-r * ROW_PITCH)
            rg.add(cell)
        out.add(rg)
    return out


def table_card(title, body, width):
    t = T(title, 32, BLUE)
    t.next_to(body, UP, buff=0.22).align_to(body, LEFT)
    inner = VGroup(t, body)
    box = RoundedRectangle(corner_radius=0.12, width=width, height=inner.height + 0.4)
    box.set_stroke(BLUE, 3).set_fill(BLUE, 0.06).move_to(inner)
    box.align_to(inner, LEFT).shift(0.3 * LEFT)
    card = VGroup(box, t, body)
    card.box, card.title, card.body = box, t, body
    return card


HP_ROWS = [
    ("person_id", "movie_id", "position", "job"),
    ("nm0000122", "tt0012349", "actor", "null"),
    ("nm0000122", "tt0012349", "composer", "composer"),
    ("nm0000122", "tt0012349", "director", "director"),
    ("nm0000122", "tt0012349", "producer", "producer"),
    ("nm0000122", "tt0012349", "writer", "written by"),
]


# ---------------------------------------------------------------- documents
KID_DOC = """{
"movie_id": "tt0012349",
"title": "The Kid",
"year": 1921,
"actors": [
{
"person_id": "nm0000122",
"name": "Charles Chaplin",
"roles": ["A Tramp"]
},
/* 9 more */
]
}"""

CHAPLIN_DOC = """{
"person_id": "nm0000122",
"name": "Charles Chaplin",
"acted_in": [
{
"movie_id": "tt0012349",
"title": "The Kid",
"year": 1921,
"roles": ["A Tramp"]
},
/* 4 more */
]
}"""


def doc_card(src, gold, comment):
    code = Code(src, size=28, lang="json")
    for sub in gold:
        code.find(sub).set_color(GOLD)
    code.find(comment).set_color(DIM)
    box = RoundedRectangle(corner_radius=0.12, width=code.width + 0.45, height=code.height + 0.4)
    box.set_stroke(TEAL, 3).set_fill(TEAL, 0.05).move_to(code)
    card = VGroup(box, code)
    card.box, card.code = box, code
    return card


def lines_box(code, i0, i1):
    grp = VGroup(*[code.line(i) for i in range(i0, i1 + 1)])
    r = SurroundingRectangle(grp, color=YELLOW, buff=0.1, corner_radius=0.08)
    r.set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12).set_z_index(-1)
    return r


# ---------------------------------------------------------------- mini icons (clip 4)
def mini_table(title):
    t = T(title, 30, BLUE)
    box = RoundedRectangle(corner_radius=0.1, width=2.2, height=1.2).set_stroke(BLUE, 3).set_fill(BLUE, 0.06)
    box.next_to(t, DOWN, buff=0.15)
    rows = VGroup(*[Line(LEFT * 0.8, RIGHT * 0.8).set_stroke(DIM, 6) for _ in range(3)])
    rows.arrange(DOWN, buff=0.28).move_to(box)
    g = VGroup(box, t, rows)
    g.rows = rows
    return g


def mini_doc(title):
    t = T(title, 30, TEAL)
    box = RoundedRectangle(corner_radius=0.1, width=2.2, height=1.2).set_stroke(TEAL, 3).set_fill(TEAL, 0.05)
    box.next_to(t, DOWN, buff=0.15)
    specs = [(1.4, 0), (1.1, 0.25), (1.1, 0.25), (1.2, 0)]
    bars = VGroup()
    for k, (w, ind) in enumerate(specs):
        bars.add(Line(ORIGIN, RIGHT * w).set_stroke(DIM, 6))
    bars.arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(box)
    for (w, ind), b in zip(specs, bars):
        b.shift(RIGHT * ind)
    g = VGroup(box, t, bars)
    g.bars = bars
    g.copy_bar = VGroup(bars[1], bars[2])
    return g


class LastTime(NarratedScene):
    def construct(self):
        self.clip_tangle()
        self.clip_tables()
        self.clip_docs()
        self.clip_neither()

    # ------------------------------------------------------------ c1.last.1
    def clip_tangle(self):
        tg = tangle()
        self.tg = tg
        cap = T("Last time: documents", 44, FG, t2c={"documents": TEAL})
        with self.say("c1.last.1") as c:
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("charles chaplin")
            self.play(*disappear(cap), *appear(tg.v["chaplin"]), run_time=min(1.0, c.until("jackie coogan")))
            c.wait_until("jackie coogan")
            self.play(*appear(tg.v["coogan"]), run_time=min(1.0, c.until("the kid")))
            c.wait_until("the kid")
            self.play(*appear(tg.v["kid"]), run_time=min(1.0, c.until("the gold rush")))
            c.wait_until("the gold rush")
            self.play(*appear(tg.v["gold"]), run_time=min(1.0, c.until("lines")))
            c.wait_until("lines")
            self.play(LaggedStart(*[Create(l) for l in tg.lines], lag_ratio=0.4),
                      run_time=min(2.0, 0.7 * c.until("mn")))
            settle(self, tg)
            c.wait_until("mn")
            tag = T("many-to-many", 34, YELLOW).move_to(DOWN * 3.15)
            self.tag = tag
            kid_lines = [tg.lines[0], tg.lines[1]]
            self.play(*[VShowPassingFlash(l.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for l in kid_lines], run_time=1.5)
            c.wait_until("a person works")
            self.play(*[VShowPassingFlash(l.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for l in (tg.lines[1], tg.lines[2])], run_time=1.5)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=min(1.0, c.until(None)))

    # ------------------------------------------------------------ c1.last.2
    def clip_tables(self):
        tg = self.tg
        self.tg_center = tg.get_center()
        line = tg.lines[1]   # Chaplin – The Kid

        hp_colors = [[DIM] * 4] + [[FG, FG, FG, DIM if r == 1 else FG] for r in range(1, 6)]
        hp_body = grid(HP_ROWS, hp_colors)
        ppl_body = grid([("nm0000122", "Charles Chaplin", "1889", "1977")], [[DIM] * 4])
        mov_body = grid([("tt0012349", "The Kid", "1921", "movie", "68")], [[DIM] * 5])
        width = hp_body.width + 0.6
        people = table_card("people", ppl_body, width)
        hp = table_card("has_position", hp_body, width)
        movies = table_card("movies", mov_body, width)
        stack = VGroup(people, hp, movies).arrange(DOWN, buff=0.55)
        stack.move_to([6.6 - width / 2, 0, 0])
        rows = list(hp_body[1:])

        with self.say("c1.last.2") as c:
            # the drawing shrinks to the top left, the three cards come in
            tg.generate_target()
            tg.target.scale(0.36).to_corner(UL, buff=0.5)
            for k in range(3, 7):
                tg.target[k][1].set_opacity(0)   # names fade: the mini drawing is circles and lines
            self.play(MoveToTarget(tg), self.tag.animate.scale(30 / 34).next_to(tg.target, DOWN, buff=1.1),
                      run_time=1.2)
            self.play(*appear(people.box, people.title, ppl_body, lag=0.1),  # early: the three tables shown whole, then walked
                      *appear(hp.box, hp.title, hp_body[0], lag=0.1),
                      *appear(movies.box, movies.title, mov_body, lag=0.1),
                      run_time=min(1.5, c.until("rows")))
            c.wait_until("rows")
            # the Chaplin–The Kid line flies into has_position as its first row
            self.play(line.animate.set_stroke(YELLOW, 4), *fly(line, rows[0], arc=PI / 2), run_time=min(1.6, c.until("five")))
            c.wait_until("five")
            self.play(*appear(*rows[1:], lag=0.3, shift=None), run_time=min(1.4, c.until("actor")))
            # walk the position column, one job per word
            box = token_box(rows[0][2], rows[0], height=0.44)
            c.wait_until("actor")
            self.play(FadeIn(box), run_time=0.4)
            for k, word in enumerate(["composer", "director", "producer", "writer"], start=1):
                c.wait_until(word)
                self.play(Transform(box, token_box(rows[k][2], rows[k], height=0.44)), run_time=0.4)
            c.wait_until("so his one line")
            rows_grp = VGroup(*rows)
            self.play(FadeOut(box), FlashAround(rows_grp, color=YELLOW, time_width=1.5),
                      VShowPassingFlash(line.copy().set_stroke(YELLOW, 8), time_width=0.6), run_time=1.6)
            # the join
            j1 = MathTex(r"\bowtie", font_size=60, color=YELLOW).move_to(
                (people.get_bottom() + hp.get_top()) / 2)
            j2 = MathTex(r"\bowtie", font_size=60, color=YELLOW).move_to(
                (hp.get_bottom() + movies.get_top()) / 2)
            c.wait_until("you join")
            self.play(*recolor(list(ppl_body[0]), YELLOW), *recolor([r[0] for r in rows], YELLOW),
                      GrowFromCenter(j1), run_time=1.0)
            self.play(*flash([ppl_body[0][0]] + [r[0] for r in rows]), run_time=1.0)
            c.wait_until("and has position")
            self.play(*recolor(list(mov_body[0]), YELLOW), *recolor([r[1] for r in rows], YELLOW),
                      GrowFromCenter(j2), run_time=min(1.0, c.until(None)))
            self.play(*flash([mov_body[0][0]] + [r[1] for r in rows]), run_time=1.0)
        self.cards = VGroup(people, hp, movies, j1, j2)
        settle(self, self.cards)

    # ------------------------------------------------------------ c1.last.3
    def clip_docs(self):
        tg = self.tg
        kid = doc_card(KID_DOC, ['"Charles Chaplin"'], "/* 9 more */")
        cha = doc_card(CHAPLIN_DOC, ['"The Kid"', "1921"], "/* 4 more */")
        kid.move_to([-3.35, 0, 0])
        cha.move_to([3.35, 0, 0])
        mid = (TANGLE_POS["kid"] + TANGLE_POS["chaplin"]) / 2
        d = TANGLE_POS["chaplin"] - TANGLE_POS["kid"]
        perp = np.array([-d[1], d[0], 0]) / np.linalg.norm(d)
        cut = DashedLine(mid - 1.4 * perp, mid + 1.4 * perp, dash_length=0.15).set_stroke(TEAL, 6)

        with self.say("c1.last.3") as c:
            tg.generate_target()
            tg.target.scale(1 / 0.36).move_to(self.tg_center)
            for k in range(3, 7):
                tg.target[k][1].set_opacity(1)
            sweep_clear(self, MoveToTarget(tg), keep=[tg], run_time=1.4)
            self.play(Create(cut), run_time=min(1.0, c.until("kid")))
            c.wait_until("kid")
            self.play(*during(disappear(tg, cut), 0, 0.45), *during(appear(kid), 0.5, 1.0), run_time=1.6)
            c.wait_until("with a copy")
            self.play(*flash([kid.code.find('"Charles Chaplin"')], color=GOLD), run_time=1.5)
            c.wait_until("chaplin")
            self.play(*appear(cha), run_time=1.0)
            c.wait_until("with a copy", nth=1)
            self.play(*flash([cha.code.find('"The Kid"'), cha.code.find("1921")], color=GOLD), run_time=1.5)
            c.wait_until("twice")
            b1, b2 = lines_box(kid.code, 5, 9), lines_box(cha.code, 4, 9)
            self.play(FadeIn(b1), FadeIn(b2), run_time=1.0)
            self.play(FlashAround(b1, color=YELLOW, time_width=1.5), FlashAround(b2, color=YELLOW, time_width=1.5),
                      run_time=1.5)
        self.docs = VGroup(kid, cha, b1, b2)

    # ------------------------------------------------------------ c1.last.4
    def clip_neither(self):
        tg = self.tg
        tg.lines[1].set_stroke(FG, 4)
        ppl = mini_table("people")
        hp = mini_table("has_position")
        left = VGroup(ppl, hp).arrange(DOWN, buff=0.6).move_to([-5.5, -0.1, 0])
        dk = mini_doc("The Kid")
        dc = mini_doc("Chaplin")
        right = VGroup(dk, dc).arrange(DOWN, buff=0.6).move_to([5.5, -0.1, 0])
        q = T("?", 80, GOLD).move_to([0, 1.55, 0])

        with self.say("c1.last.4") as c:
            self.play(*during(disappear(self.docs), 0, 0.45), *during(appear(tg, shift=None), 0.5, 1.0),
                      run_time=1.4)
            self.play(*appear(left, right, lag=0.3), run_time=min(1.2, c.until("asrow")))
            c.wait_until("asrow")
            self.play(*recolor([ppl.rows[1], hp.rows[1]], YELLOW), run_time=0.8)
            self.play(*flash([ppl.rows[1], hp.rows[1]]), run_time=1.5)
            c.wait_until("ascopies")
            self.play(*recolor(list(dk.copy_bar) + list(dc.copy_bar), YELLOW), run_time=0.8)
            self.play(*flash([dk.copy_bar, dc.copy_bar]), run_time=1.5)
            c.wait_until("neither one")
            dim = []
            for m in (ppl, hp, dk, dc):
                dim.append(m[0].animate.set_stroke(opacity=0.4))
                dim.append(m[1].animate.set_opacity(0.4))
                dim += [b.animate.set_stroke(opacity=0.4) for b in m[2]]
            self.play(*dim, run_time=1.0)
            c.wait_until("third")
            self.play(*recolor(tg.lines, YELLOW), *appear(q), run_time=1.2)
            self.play(*[VShowPassingFlash(l.copy().set_stroke(YELLOW, 10), time_width=0.6) for l in tg.lines],
                      run_time=min(1.5, c.until(None)))
        # handover: the drawing alone, plain, at centre
        self.play(*disappear(left, right, q), *recolor(tg.lines, FG), run_time=1.2)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(1.0)
