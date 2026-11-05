"""Chapter 10, scene 4: Exercise 19.1, every copy of a name. Clips c10.rename.1 – c10.rename.3.

Clip 1: opens on ch9 s9's next_card() row (no header), 19.1 bright; 19.1's box grows into ch8 s7's
ex19_card(1), the DIM hint under it, ch9 s1's pause icon on {stop}. Clip 2: The Kid's 14 top-level
keys as a tree (ch4 s2's json_tree, arrays as counted stubs); the five person arrays glow on their
words; the path $ / .* / [*] / .person_id grows above the tree, one step per mark, GOLD counter
14 -> 22 -> 14, then the 14 person IDs as a column (Chaplin's YELLOW). Clip 3: the query (WHERE
wrapped as SQL usually is, to stay at size 28), UNION ALL box, the nine-row result, the five-OR
version, a ghost "cinematographers" array lit by $.*[*], her person document, 9 documents vs 1 row.

EXPORTS (static): recap_r3() -> VGroup at ORIGIN, ~7.6 x 5.4: the path `$.*[*].person_id` (Mono 40)
over a mini tree of The Kid's seven arrays (person arrays lit TEAL with ".person_id" tags, genres and
trivia dimmed), and GOLD "9 documents" against GOLD "1 row". `.path .tree .docs .rows`.
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

J = load_scene("ch4_s2_json")
D = load_scene("ch4_s3_movie")
P = load_scene("ch7_s3_paths")
U = load_scene("ch8_s2_unnest")
T8 = load_scene("ch8_s7_try")
S1 = load_scene("ch9_s1_intro")
R9 = load_scene("ch9_s9_recap")
SCH = load_scene("ch1_s2_schema")

PID = "nm0905154"
NAME = "Lana Wachowski"
PERSON_ARRAYS = ["actors", "directors", "producers", "writers", "composers"]
PATH = "$.*[*].person_id"
PIECES = [("$", 0, 1), (".*", 1, 3), ("[*]", 3, 6), (".person_id", 6, 16)]

QUERY = """SELECT movie_id AS id, movie->>'title' AS title
FROM   movies
WHERE  list_contains(movie->>'$.*[*].person_id',
                     'nm0905154')
UNION ALL
SELECT person_id, person->>'name'
FROM   people
WHERE  person_id = 'nm0905154'
ORDER BY id;"""

LONGER = "\n".join(
    [("WHERE  " if k == 0 else "   OR  ") + f"list_contains(movie->>'$.{a}[*].person_id',\n"
     + " " * 21 + "'nm0905154')" for k, a in enumerate(PERSON_ARRAYS)])

RESULT = [(PID, NAME), ("tt0115736", "Bound"), ("tt0133093", "The Matrix"),
          ("tt0234215", "The Matrix Reloaded"), ("tt0242653", "The Matrix Revolutions"),
          ("tt0328832", "The Animatrix"), ("tt0434409", "V for Vendetta"),
          ("tt10838180", "The Matrix Resurrections"), ("tt1371111", "Cloud Atlas")]

LANA_DOC = """{
  "person_id": "nm0905154",
  "name": "Lana Wachowski",
  "birthyear": 1965,
  "directed": [{"title": "Bound", …}, …],
  "produced": [{"title": "V for Vendetta", …}, …],
  "wrote": [{"title": "Bound", …}, …]
}"""

UPDATE_SQL = """UPDATE people
SET    name = 'Lana Wachowski'
WHERE person_id = 'nm0905154';"""


# ══ pieces ═════════════════════════════════════════════════════════════════════
def _with_orig(tree):
    tree.orig = {}
    for p in tree.paths:
        if tree.kinds[p] in ("leaf", "more"):
            tree.orig[p] = tree.nodes[p].get_color()
        if p in tree.labels:
            tree.orig[("label",) + p] = tree.labels[p].get_color()
    tree.top = [p for p in tree.paths if len(p) == 1]
    return tree


def kid_tree14():
    """The Kid: all 14 top-level keys, every array a counted stub (~7.3 x 5.8 at size 28)."""
    return _with_orig(J.json_tree(J.kid_value(), open=[], counts=True, size=28, row_gap=0.42,
                                  label_pad=0.32, trunk_gap=0.15))


def path_pieces(size=52):
    ref = Mono(PATH, size)
    out = []
    for s, a, b in PIECES:
        m = Mono(s, size)
        m.move_to(VGroup(*ref[a:b]).get_center())
        out.append(m)
    return ref, out


def id_column(size=28):
    kid = J.kid_value()
    ids = [e["person_id"] for a in PERSON_ARRAYS for e in kid[a]]
    lines = VGroup()
    for k, i in enumerate(ids):
        s = ("[" if k == 0 else "") + i + ("]" if k == len(ids) - 1 else ",")
        col = YELLOW if i == "nm0000122" else FG
        lines.add(Mono(s, size, color=col, t2c={"[": BLUE, "]": BLUE}))
    lines.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
    for k in range(1, len(lines)):
        lines[k].shift(RIGHT * 0.15)
    return lines


def pid_tags(tree, size=28):
    return [Mono(".person_id", size, color=TEAL).next_to(tree.nodes[(a,)], RIGHT, buff=0.3)
            for a in PERSON_ARRAYS]


def mini_people_tree(with_ghost=True, size=30):
    kid = J.kid_value()
    value = {a: kid[a] for a in PERSON_ARRAYS}
    if with_ghost:
        value["cinematographers"] = [{}]
    return _with_orig(J.json_tree(value, open=[], counts=False, size=size, row_gap=0.55,
                                  label_pad=0.32, trunk_gap=0.15))


def result_table():
    rows = [list(r) for r in RESULT]
    colors = [[DIM, FG] for _ in rows]
    t = U.table(["id", "title"], rows, colors, size=28, pitch=0.5, serif={1: 28})
    t.head.set_color(DIM)
    return t


def lana_card():
    card = T8.doc(LANA_DOC, size=28)
    code = card.code
    code.titles = [code.find('"Bound"', nth=0), code.find('"V for Vendetta"'), code.find('"Bound"', nth=1)]
    for g in code.titles:
        g.set_color(FG)
    code.find('"nm0905154"').set_color(FG)
    code.find('1965').set_color(FG)
    code.find('"Lana Wachowski"').set_color(YELLOW)
    return card


def doc_grid(scale=1.0):
    tiles = VGroup()
    for k in range(9):
        f = D._frame(0.8, 1.0)
        f.set_stroke(YELLOW if k == 8 else TEAL, 3)
        for j in range(3):
            ln = Line([-0.25, 0.22 - 0.2 * j, 0], [0.25 - 0.12 * (j == 2), 0.22 - 0.2 * j, 0])
            ln.set_stroke(YELLOW if k == 8 else TEAL, 2, opacity=0.6)
            f.add(ln)
        tiles.add(f)
    tiles.arrange_in_grid(3, 3, buff=0.25)
    return tiles.scale(scale)


def people_card(size=28):
    rows = [["…", "…", "…"], [PID, NAME, "…"], ["…", "…", "…"]]
    colors = [[DIM] * 3, [YELLOW, YELLOW, DIM], [DIM] * 3]
    t = SCH.RowTable("people", ["person_id", "name", "…"], rows, colors, size=size, pad=0.16, pitch=0.58)
    return t


def recap_r3():
    """Static: the path over a mini tree of The Kid's arrays, then 9 documents against 1 row."""
    kid = J.kid_value()
    keys = ["genres"] + PERSON_ARRAYS + ["trivia_entries"]
    tree = _with_orig(J.json_tree({k: kid[k] for k in keys}, open=[], counts=True, size=28,
                                  row_gap=0.46, label_pad=0.32, trunk_gap=0.15))
    P.light(tree, [(a,) for a in PERSON_ARRAYS])
    for a in ("genres", "trivia_entries"):
        for m in tree.branch(a):
            m.set_opacity(0.3)
    tags = VGroup(*pid_tags(tree, 26))
    tg = VGroup(tree, tags)
    path = Mono(PATH, 40).next_to(tg, UP, buff=0.4)
    docs = T("9 documents", 40, GOLD)
    vs = T("vs", 32, DIM)
    rows = T("1 row", 40, GOLD)
    bottom = VGroup(docs, vs, rows).arrange(RIGHT, buff=0.45).next_to(tg, DOWN, buff=0.45)
    g = VGroup(path, tg, bottom).move_to(ORIGIN)
    g.path, g.tree, g.docs, g.rows = path, tree, docs, rows
    return g


# ══ the scene ══════════════════════════════════════════════════════════════════
class RenameEverywhere(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c10.rename.1: the card and its hint ───────────────────────────────────
    def clip1(self):
        nc = R9.next_card()
        c17, c18, c19 = nc.cards[17], nc.cards[18], nc.cards[19]
        for c in (c17, c18, c19):
            c.head.set_color(DIM)
            c.title.set_color(DIM)
        s1 = c19.subs[0]
        s1.box.set_stroke(FG, 2.5)
        s1.num.set_color(YELLOW)
        s1.sub.set_color(FG)
        others = [c17, c18, c19.box, c19.head, c19.title, *c19.subs[1:]]
        self.add(*others, s1.box, s1.num, s1.sub)

        hero = T8.ex19_card(1).move_to([0, 1.35, 0])
        hint = T8.hint(1, size=28, width=12.4).move_to([0, -1.0, 0])
        pause = S1.pause_icon(height=1.2).move_to([0, -2.6, 0])

        with self.say("c10.rename.1") as c:
            self.wait(0.2)
            self.play(*during(disappear(*others, s1.num, s1.sub), 0, 0.42),  # early: the question card, read whole
                      *during([ReplacementTransform(s1.box, hero.box)], 0.1, 0.8),
                      *during(appear(hero.text, shift=None), 0.5, 1),
                      run_time=min(2.0, c.until("when lana")))
            self.remove(hero.box, hero.text)
            self.add(hero)
            c.wait_until("hint")
            self.play(*appear(hint), run_time=1.0)  # early: the hint line, read out over this sentence
            c.wait_until("then a star")
            self.play(FlashUnder(VGroup(*hint[:6]), color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("stop")
            self.play(FadeIn(pause, scale=0.8), run_time=0.8)
        self.hero, self.hint, self.pause = hero, hint, pause

    # ── c10.rename.2: the walk through The Kid ─────────────────────────────────
    def clip2(self):
        tree = kid_tree14()
        tree.move_to([-6.6 + tree.width / 2, -0.4, 0])
        ref, pieces = path_pieces(52)
        shift = np.array([-6.6 - ref.get_left()[0], 3.3 - ref.get_center()[1], 0])
        ref.shift(shift)
        for m in pieces:
            m.shift(shift)
        cpos = np.array([2.75, 0.6, 0])

        def counter(n, word):
            num = T(str(n), 88, GOLD).move_to(cpos)
            lab = T(word, 32, DIM).next_to(num, DOWN, buff=0.25)
            return num, lab

        with self.say("c10.rename.2") as c:
            sweep_clear(self, *appear(tree, shift=None), run_time=min(1.8, c.until("kinds")))
            c.wait_until("actors")
            for a in PERSON_ARRAYS:
                c.wait_until(a)
                lab = tree.labels[(a,)]
                self.play(lab.animate.set_color(TEAL), FlashAround(lab, color=TEAL, time_width=1.5),
                          run_time=0.7)
            settle(self, tree)

            c.wait_until("walk")
            self.play(*[tree.labels[(a,)].animate.set_color(FG) for a in PERSON_ARRAYS], run_time=0.8)

            # $ : the whole document
            c.wait_until("dollar")
            pieces[0].set_color(YELLOW)
            self.play(*appear(pieces[0]), *P.light_step(tree, ()), run_time=min(1.5, c.until("dotstar")))

            # .* : all fourteen top-level values
            c.wait_until("dotstar")
            pieces[1].set_color(YELLOW)
            self.play(*appear(pieces[1]), *recolor(pieces[0], FG),
                      *[a for p in tree.top for a in P.light_step(tree, p)], run_time=1.8)
            num, lab = counter(14, "values")
            c.wait_until("fourteen")
            self.play(*appear(num, lab, lag=0.3), run_time=1.0)

            # [*] : into the arrays, every element
            c.wait_until("brackstar")
            pieces[2].set_color(YELLOW)
            scalars = [p for p in tree.top if tree.kinds[p] == "leaf"]
            arrays = [p for p in tree.top if tree.kinds[p] == "stub"]
            self.play(*appear(pieces[2]), *recolor(pieces[1], FG),
                      *[a for p in scalars for a in P.light_step(tree, p, on=False)], run_time=1.6)
            c.wait_until("every element")
            self.play(*[tree.nodes[p].count.animate.set_color(GOLD) for p in arrays],
                      *[FlashAround(tree.nodes[p].count, color=GOLD, time_width=1.5) for p in arrays],
                      run_time=1.2)
            num2, lab2 = counter(22, "elements")
            c.wait_until("twenty-two")
            self.play(*swap(num, num2), *swap(lab, lab2), run_time=1.2)
            num, lab = num2, lab2

            # .person_id : only the person IDs
            c.wait_until("pid")
            pieces[3].set_color(YELLOW)
            tags = pid_tags(tree)
            self.play(*appear(pieces[3]), *recolor(pieces[2], FG), run_time=1.0)
            self.play(*appear(*tags, lag=0.15, shift=None), run_time=1.0)  # early: the five tags, named by "person IDs" just said
            c.wait_until("the genres")
            drop = [m for a in ("genres", "trivia_entries") for m in tree.branch(a)]
            num3, lab3 = counter(14, "person IDs")
            ids = id_column(28)
            ids.move_to([5.35, -0.25, 0])
            self.play(*set_alpha(drop, 0.3), *swap(num, num3), *swap(lab, lab3),
                      *during(appear(*ids, lag=0.05, shift=None), 0.35, 1),  # early: the list the path returns
                      run_time=max(0.8, min(1.8, c.until(None) - 0.1)))
            settle(self, tree)

    # ── c10.rename.3: the query, its answer, and why ───────────────────────────
    def clip3(self):
        q = Code(QUERY, size=28).move_to([0, 0.2, 0])
        with self.say("c10.rename.3") as c:
            sweep_clear(self, *appear(q, shift=None), run_time=min(1.8, c.until("that path")))
            c.wait_until("that path")
            self.play(FlashUnder(q.find("'$.*[*].person_id'"), color=TEAL, time_width=1.5), run_time=1.4)

            c.wait_until("union")
            block = VGroup(*[q.line(i) for i in range(4, 8)])
            box = RoundedRectangle(corner_radius=0.12, width=q.width + 0.4, height=block.height + 0.3)
            box.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.1).move_to([q.get_center()[0], block.get_center()[1], 0])
            box.set_z_index(-1)
            self.play(FadeIn(box), run_time=1.0)

            # the result: nine documents
            c.wait_until("result")
            tbl = result_table()
            U.place(tbl, -6.2, 2.5)
            nine = T("9", 110, GOLD)
            split = T("8 movies + 1 person", 36, GOLD)
            gold = VGroup(nine, split).arrange(DOWN, buff=0.3).move_to([4.3, 0.0, 0])
            sweep_clear(self, *appear(tbl, shift=None), run_time=1.6)  # early: the result table, read whole as the titles are named
            c.wait_until("eight movies")
            self.play(*appear(nine, split, lag=0.3), run_time=1.2)
            c.wait_until("plus her own")
            lana = tbl.rows[0]
            self.play(lana[1].animate.set_color(YELLOW), FlashAround(lana, time_width=1.5), run_time=1.2)

            # without the wildcard: five list_contains
            c.wait_until("longer")
            longer = Code(LONGER, size=27).move_to([0, 0.55, 0])
            also = T("also 8 movies", 36, GOLD).next_to(longer, DOWN, buff=0.45)
            sweep_clear(self, *appear(longer, shift=None), run_time=1.6)
            c.wait_until("five times")
            keys = [longer.find(a) for a in PERSON_ARRAYS]
            self.play(*[a for g in keys for a in recolor(g, TEAL)], *appear(also), run_time=1.2)

            # the wildcard also covers a sixth array
            c.wait_until("later")
            mt = mini_people_tree(with_ghost=True)
            mt.scale(1.3).move_to([0, -0.6, 0])
            mpath = Mono("$.*[*]", 56).move_to([0, 2.75, 0])
            ghost_path = ("cinematographers",)
            ghost = mt.branch(*ghost_path)
            for m in ghost:
                m.set_opacity(0)
            sweep_clear(self, *appear(mt, mpath, shift=None, lag=0.2), run_time=1.4)
            c.wait_until("added later")
            ghost_lab = mt.labels[ghost_path]
            ghost_lab.set_color(DIM)
            self.play(*[m.animate.set_opacity(0.55) for m in ghost], run_time=0.6)
            self.play(*[a for k in PERSON_ARRAYS for a in P.light_step(mt, (k,))],
                      mt.edges[ghost_path].animate.set_stroke(TEAL, 5, opacity=0.7),
                      ghost_lab.animate.set_color(TEAL).set_opacity(0.8),
                      mt.nodes[ghost_path].animate.set_opacity(0.8),
                      run_time=min(1.2, c.until("people") - 0.1))

            # her person document: titles, never names
            c.wait_until("people")
            card = lana_card().move_to([0, 0.2, 0])
            sweep_clear(self, *appear(card, shift=None), run_time=1.4)
            c.wait_until("titles")
            tg = card.code.titles
            self.play(*[a for g in tg for a in recolor(g, GOLD)],
                      *[FlashAround(g, color=GOLD, time_width=1.5) for g in tg], run_time=1.4)

            # 9 documents against 1 row
            c.wait_until("compare")
            grid = doc_grid().move_to([-3.9, 0.75, 0])
            docs = T("9 documents", 48, GOLD).next_to(grid, DOWN, buff=0.45)
            pc = people_card(28).move_to([3.0, 2.0, 0])
            sweep_clear(self, *during(appear(grid, docs, shift=None, lag=0.3), 0.55, 1), run_time=1.8)
            c.wait_until("against")
            self.play(*appear(pc, shift=None), run_time=1.0)
            c.wait_until("one row")
            row = pc.rows[1]
            rbox = SurroundingRectangle(row, color=YELLOW, buff=0.1).set_stroke(YELLOW, 3)
            one = T("1 row", 48, GOLD).next_to(pc, DOWN, buff=0.4)
            upd = Code(UPDATE_SQL, size=28).set_color(DIM).next_to(one, DOWN, buff=0.45)
            self.play(FadeIn(rbox), *appear(one), run_time=1.0)
            self.play(*appear(upd, shift=None), run_time=1.0)
        self.wait(1.2)
