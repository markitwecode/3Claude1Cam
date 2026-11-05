"""Chapter 7, scene 1: where the documents live, and the tree inside one cell. Clips c7.hook.1 – c7.hook.2.

Exports (import with `H = load_scene("ch7_s1_hook")`; all static, no updaters):

    H.movies_card() -> MoviesCard (VGroup), hero size, centred on ORIGIN (~12.3 x 3.5):
        .box .header (BLUE fill 0.35) .title (Mono 28 bold "movies") .count (T 28 GOLD "2,935 rows")
        .lines (dividers) .heads [movie_id, movie] (Mono 24 bold) .underline (movie_id, primary key)
        .tag (Mono 22 DIM "JSON" after `movie`) .ids[i] .cells[i] (Mono 24) .rows[i] VGroup(id, cell)
        .cell  = .cells[0], The Kid's `movie` cell (YELLOW, like its id); other cells DIM, cut off.
        .cell_right(i) -> the card's right edge at row i (where a link leaves the cell)
    H.place_card(card)  shrinks/moves a movies_card() to the open-card spot (scale CARD_S, top-left)
    H.kid_tree_open() -> JsonTree at ORIGIN (size 26): title, year, minutes, genres -> 3,
        actors -> 0 -> name; the rest folded DIM. String leaves TEAL, numbers GOLD.
    H.placed_tree()     kid_tree_open() scaled into the right half (top 3.3, right 6.6)
    H.tool_tags(tree) -> [`->`, `->>`, `$.actors[0].name`] TEAL tags (Mono 34 in TEAL boxes) under the tree
    H.open_card()     -> VGroup(.table .cell .link .tree .arrows): ch7's first frame (ch6 s7 ends on it)
    H.handover_shot() -> VGroup(.table .cell .link .tree .tags): this scene's last frame (ch7 s2 opens on it)
"""
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

J = load_scene("ch4_s2_json")
SCH = load_scene("ch1_s2_schema")
H6 = load_scene("ch6_s1_hook")

# ══ the movies table card (movies-json.duckdb, table order, DuckDB 1.5.6) ═════════

MOVIE_ROWS = [
    ("tt0012349", ('{"movie_id": "tt0012349",', '"title": "The Kid", …')),
    ("tt0015324", ('{"movie_id": "tt0015324",', '"title": "Sherlock Jr.", …')),
    ("tt0015864", ('{"movie_id": "tt0015864",', '"title": "The Gold Rush", …')),
    ("tt0017136", ('{"movie_id": "tt0017136",', '"title": "Metropolis", …')),
]
CS = 28
HDR_H, HEAD_H, ROW_H, PADX, LINE_D = 0.78, 0.66, 0.98, 0.28, 0.215


class MoviesCard(VGroup):
    def __init__(self):
        super().__init__()
        w_id = max(Mono(r[0], CS).width for r in MOVIE_ROWS) + 2 * PADX
        w_mv = max(Mono(ln, CS).width for r in MOVIE_ROWS for ln in r[1]) + 2 * PADX
        W, Hh = w_id + w_mv, HDR_H + HEAD_H + len(MOVIE_ROWS) * ROW_H
        x0, y0 = -W / 2, Hh / 2
        xm = x0 + w_id
        self.box = Rectangle(width=W, height=Hh).set_stroke(BLUE, 3).set_fill(BG, 0)
        self.header = Rectangle(width=W, height=HDR_H).set_stroke(BLUE, 0).set_fill(BLUE, 0.35)
        self.header.move_to([0, y0 - HDR_H / 2, 0])
        self.title, _ = SCH._placed("movies", 28, FG, BOLD, y0 - HDR_H / 2, left=x0 + PADX)
        self.count = T("2,935 rows", 28, GOLD)
        self.count.move_to([x0 + W - PADX - self.count.width / 2, y0 - HDR_H / 2, 0])
        yh = y0 - HDR_H - HEAD_H / 2
        h1, bot = SCH._placed("movie_id", CS, FG, BOLD, yh, left=x0 + PADX)
        h2, _ = SCH._placed("movie", CS, FG, BOLD, yh, left=xm + PADX)
        self.heads = VGroup(h1, h2)
        self.underline = Line([h1.get_left()[0], bot + 0.02, 0],
                              [h1.get_right()[0], bot + 0.02, 0]).set_stroke(FG, 2.5)
        self.tag = Mono("JSON", 26, DIM)
        self.tag.next_to(h2, RIGHT, buff=0.22).align_to(h2, DOWN)
        yb = y0 - HDR_H - HEAD_H
        lines = [Line([x0, y0 - HDR_H, 0], [x0 + W, y0 - HDR_H, 0]).set_stroke(BLUE, 2),
                 Line([x0, yb, 0], [x0 + W, yb, 0]).set_stroke(BLUE, 2),
                 Line([xm, y0 - HDR_H, 0], [xm, -y0, 0]).set_stroke(BLUE, 1.5)]
        for i in range(1, len(MOVIE_ROWS)):
            y = yb - i * ROW_H
            lines.append(Line([x0, y, 0], [x0 + W, y, 0]).set_stroke(DIM, 1, opacity=0.6))
        self.lines = VGroup(*lines)
        self.ids, self.cells, self.rows = [], [], []
        for i, (mid, doc) in enumerate(MOVIE_ROWS):
            y = yb - (i + 0.5) * ROW_H
            kid = i == 0
            a, _ = SCH._placed(mid, CS, YELLOW if kid else FG, NORMAL, y, left=x0 + PADX)
            b = VGroup(*[SCH._placed(ln, CS, YELLOW if kid else DIM, NORMAL, y + d, left=xm + PADX)[0]
                         for ln, d in zip(doc, (LINE_D, -LINE_D))])
            self.ids.append(a)
            self.cells.append(b)
            self.rows.append(VGroup(a, b))
        self.cell = self.cells[0]
        self.add(self.header, self.box, self.lines, self.title, self.count, self.heads,
                 self.underline, self.tag, *self.rows)

    def cell_right(self, i=0):
        return np.array([self.box.get_right()[0], self.rows[i].get_center()[1], 0])


def movies_card():
    return MoviesCard()


CARD_S = 0.4
CARD_LEFT, CARD_TOP = -6.0, 3.5


def place_card(card):
    card.scale(CARD_S)
    card.shift(RIGHT * (CARD_LEFT - card.get_left()[0]) + UP * (CARD_TOP - card.get_top()[1]))
    return card


# ══ The Kid's tree ═════════════════════════════════════════════════════════════

TREE_OPENS = [("title",), ("genres",), ("actors", 0, "name")]
TITLE_P, CHAPLIN_P = ("title",), ("actors", 0, "name")


def _get(v, path):
    for k in path:
        v = v[k]
    return v


def kid_tree_open():
    """The Kid with title, genres (all three) and actors -> 0 -> name open; every
    other key folded into DIM "+n more keys", actors 1-9 into "+9 more". Built under a
    throwaway wrapper object (json_tree folds keys only below the root), then cut off."""
    kv = J.kid_value()
    W = J.json_tree({"r": kv}, open=[("r",) + p for p in TREE_OPENS], elide_keys=True,
                    size=26, row_gap=0.38, label_pad=0.28, trunk_gap=0.15)
    W.remove(W.nodes[()], W.edges[("r",)], W.labels[("r",)])
    t = J.JsonTree()
    t.nodes = {p[1:]: m for p, m in W.nodes.items() if p}
    t.edges = {p[1:]: m for p, m in W.edges.items() if len(p) > 1}
    t.labels = {p[1:]: m for p, m in W.labels.items() if len(p) > 1}
    t.kinds = {p[1:]: k for p, k in W.kinds.items() if p}
    t.paths = [p[1:] for p in W.paths if p]
    t.add(*W.submobjects)
    t.root = t.nodes[()]
    for p, k in t.kinds.items():
        if k == "leaf" and isinstance(_get(kv, p), str):
            t.nodes[p].set_color(TEAL)
    t.move_to(ORIGIN)
    return t


TREE_TOP = 1.1      # the tree is never scaled: size 26, left edge on CARD_LEFT, below the card
LINK_X = CARD_LEFT - 0.35


def placed_tree():
    t = kid_tree_open()
    t.shift(RIGHT * (CARD_LEFT - t.get_left()[0]) + UP * (TREE_TOP - t.get_top()[1]))
    return t


def cell_box(card):
    """TEAL box round The Kid's `movie` cell (the opened cell)."""
    return SurroundingRectangle(card.cell, buff=0.06).set_stroke(TEAL, 2.5)


def kid_link(card, tree):
    """TEAL elbow from the card's left edge at The Kid's row, down the margin, into the root."""
    y0 = card.rows[0].get_center()[1]
    ry = tree.root.get_center()[1]
    return VMobject().set_points_as_corners([
        [card.get_left()[0], y0, 0], [LINK_X, y0, 0], [LINK_X, ry, 0], tree.root.get_left()
    ]).set_stroke(TEAL, 3)


def tool_tag(s):
    txt = Mono(s, 34, TEAL)
    box = RoundedRectangle(corner_radius=0.12, width=txt.width + 0.4, height=0.78)
    box.set_stroke(TEAL, 2).set_fill(TEAL, 0.12).move_to(txt)
    g = VGroup(box, txt)
    g.box, g.text = box, txt
    return g


TAG_Y = 2.45


def tool_tags(tree):
    tags = VGroup(*[tool_tag(s) for s in ("->", "->>", "$.actors[0].name")]).arrange(RIGHT, buff=0.4)
    tags.move_to([6.45 - tags.width / 2, TAG_Y, 0])
    return list(tags)


def _shot(n_tags):
    card = place_card(movies_card())
    tree = placed_tree()
    box = cell_box(card)
    link = kid_link(card, tree)
    tags = VGroup(*tool_tags(tree)[:n_tags])
    g = VGroup(card, box, link, tree, tags)
    g.table, g.cell, g.cell_box, g.link, g.tree = card, card.cell, box, link, tree
    return g, tags


def open_card():
    g, tags = _shot(2)
    g.arrows = tags
    return g


def handover_shot():
    g, tags = _shot(3)
    g.tags = tags
    return g


# ══ the scene ══════════════════════════════════════════════════════════════════

class Ch7S1Hook(NarratedScene):
    def construct(self):
        self.add(open_card())
        self.wait(0.7)
        self.clip1()
        self.clip2()
        self.wait(1.0)   # handover: ch7 s2 opens on handover_shot()

    def clip1(self):
        with self.say("c7.hook.1") as c:
            tc = title_card("Part 7 · Reaching inside a document")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("table")

            # where the documents live: the movies table
            card = movies_card().move_to([0, 0.1, 0])
            shell = [card.header, card.box, card.lines, card.title, card.heads, card.underline, card.tag]
            sweep_clear(self, *[time_span(FadeIn(p), 0.6, 1.5) for p in shell], run_time=1.5)
            self.play(*appear(*card.rows, lag=0.3), run_time=1.6)
            self.play(*appear(card.count, shift=None), run_time=0.8)  # early: the card's row count, not read aloud
            settle(self, card)
            c.wait_until("two columns")
            self.play(FlashUnder(card.heads[0], color=YELLOW, run_time=1.5, time_width=1.5),
                      FlashUnder(VGroup(card.heads[1], card.tag).copy(), color=YELLOW, run_time=1.5,
                                 time_width=1.5))
            c.wait_until("whole document")
            self.play(FlashAround(card.cell, color=TEAL, run_time=1.5, time_width=1.5))
            c.wait_until("open")

            # open The Kid's cell: a tree inside
            card.generate_target()
            place_card(card.target)
            self.play(MoveToTarget(card), run_time=min(1.4, c.until("but open")))
            tree = placed_tree()
            link = kid_link(card.target, tree)
            c.wait_until("but open")
            lift = cell_box(card)
            self.play(GrowFromCenter(lift), *during([Create(link)], 0.3, 0.75),
                      *during([FadeIn(tree.root, scale=0.6)], 0.6, 1.0),
                      run_time=min(1.4, c.until("entire tree")))
            rest = [p for p in tree.submobjects if p is not tree.root]
            c.wait_until("entire tree")
            self.play(*appear(*rest, shift=None, lag=0.02),
                      run_time=max(0.8, min(2.0, c.remaining - 0.1)))
            settle(self, tree)
            self.card, self.tree, self.link = card, tree, link

    def clip2(self):
        card, tree = self.card, self.tree
        title_leaf, chaplin = tree.nodes[TITLE_P], tree.nodes[CHAPLIN_P]
        with self.say("c7.hook.2") as c:
            # SQL thinks in flat rows
            strip = Rectangle(width=4.3, height=0.9).set_stroke(BLUE, 3).set_fill(BLUE, 0.12)
            strip.move_to([0.3, TAG_Y, 0])
            cond = Code("title = 'The Kid'", size=28).move_to(strip)
            q = T("?", 72, YELLOW).move_to([strip.get_right()[0] + 0.75, TAG_Y, 0])
            self.play(*appear(strip, shift=None), run_time=1.0)
            c.wait_until("where clause")
            self.play(*appear(cond), run_time=1.0)
            c.wait_until("ask")
            self.play(*appear(q, shift=None), run_time=1.0)
            c.wait_until("title")
            self.play(FlashAround(title_leaf, run_time=1.4, time_width=1.5), *recolor(title_leaf, YELLOW),
                      run_time=1.4)
            c.wait_until("first actor")
            self.play(FlashAround(chaplin, run_time=1.4, time_width=1.5), *recolor(chaplin, YELLOW),
                      run_time=1.4)
            c.wait_until("tools")

            # two arrows and a path language
            tags = tool_tags(tree)
            self.play(*disappear(strip, cond, q), *recolor(title_leaf, TEAL), *recolor(chaplin, TEAL),
                      run_time=1.0)
            c.wait_until("two arrows")
            self.play(*appear(tags[0], tags[1], lag=0.5), run_time=1.3)
            c.wait_until("small language")
            self.play(*appear(tags[2]), run_time=1.0)
            c.wait_until("traps")

            # traps ahead
            traps = [Mono("'99' > '321'", 30, GOLD), Mono("( )", 30, RED), Mono("NULL", 30, PINK)]
            for t, x in zip(traps, (1.9, 4.2, 5.6)):
                t.move_to([x, -3.15, 0])
            self.play(*appear(*traps, lag=0.4), run_time=1.5)
            c.wait_until("goes wrong")
            self.play(*flash(traps, run_time=1.3, time_width=1.5), run_time=1.3)
            self.play(*set_alpha(traps, 0.4), run_time=0.8)
            c.wait_until("without a word")
            self.play(*disappear(*traps), run_time=max(0.6, min(1.0, c.remaining - 0.05)))
