"""Chapter 8, scene 7: try these (Exercise 19, four questions with hints). Clips c8.try.1 – c8.try.4.

Exports for ch10 (`from lib.paths import load_scene; X = load_scene("ch8_s7_try")`), all static:
  X.ex19_card(i, size=40) -> VGroup(box, text) at ORIGIN, i = 1..4: the full exercise card, ch3 s8's
        ex_card look (DIM rounded box, stroke 2; text FG in CMU Serif, head "19.i." YELLOW), question
        verbatim from the exercise sheet. `.box .text .head` (head = the "19.i." glyphs). At size 40:
        19.1 11.7 x 3.2 (4 lines), 19.2 10.3 x 1.8, 19.3 9.5 x 1.7, 19.4 12.0 x 2.6 (3 lines).
        In this scene the hero sits at (0, 0.2); in the hint phase it is scaled 0.75 (text 30) to the top.
  X.ex19_row() -> VGroup(header, cards, tag), placed for the full frame as in this scene:
        `.header` T "Exercise 19" 52 at y 2.4; `.cards` VGroup of four mini cards (each 3.0 x 2.0, DIM
        box stroke 2, "19.i" T 44 DIM over a T 28 DIM subject) at y 0, x = ±1.625, ±4.875;
        `.tag` T "solutions: part 10" 30 DIM in a DIM pill at y -1.9. Overall 12.75 x 4.9.
  X.mini_card(i) -> one of those mini cards at ORIGIN (`.box .num .sub`).
  X.hint(i, size=28, width=None) -> T, DIM, the hint line ch10 quotes (width=w scales it down to fit w):
        1 "$.*[*] matches every element of every array at the top level of a document" (12.6 wide at 28:
        pass width), 2 "json_array_length", 3 "list_has_any(l1, l2)",
        4 "unnest, then AVG of the rating, cast to a number" (8.4 wide at 28); 2 and 3 ~3.3 wide.
  X.hints_line(size=28) -> T DIM "$.*[*] · json_array_length · list_has_any · unnest + AVG" (10.0 wide at 28).
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

# ══ exports ════════════════════════════════════════════════════════════════════

EX19 = {
    1: ["19.1. What are the IDs of all documents that",
        "needed to be updated when Lana Wachowski",
        "changed her name? Assume you know her",
        "person_id is nm0905154."],
    2: ["19.2. Who are the five people who have",
        "directed the most movies?"],
    3: ["19.3. In which movies did one of the",
        "directors also act?"],
    4: ["19.4. What is the average rating of the movies",
        "in each genre, for the five genres with the",
        "highest average rating?"],
}
SUBJECT = {1: "a new name", 2: "top directors", 3: "actor-directors", 4: "best genres"}
HINTS = {1: "$.*[*] matches every element of every array at the top level of a document",
         2: "json_array_length",
         3: "list_has_any(l1, l2)",
         4: "unnest, then AVG of the rating, cast to a number"}
HINTS_LINE = "$.*[*] · json_array_length · list_has_any · unnest + AVG"

HEADER_Y, ROW_Y, TAG_Y = 2.4, 0.0, -1.9
SLOT_X = (-4.875, -1.625, 1.625, 4.875)
MINI_W, MINI_H = 3.0, 2.0
HERO_Y = 0.2
TOP_SCALE, TOP_EDGE = 0.75, 3.75
GAP, BACK_RT = 1.55, 1.2   # after each clip's pause, its card shrinks back in the gap
PAUSE = 2.0          # the script's {pause=2} at the end of every clip


def ex19_card(i, size=40):
    lines = EX19[i]
    head = f"19.{i}."
    text = VGroup(*[T(s, size, t2c={head: YELLOW} if k == 0 else None) for k, s in enumerate(lines)])
    text.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.2, width=text.width + 0.8, height=text.height + 0.7)
    box.set_stroke(DIM, 2).set_fill(BG, 0)
    text.move_to(box)
    g = VGroup(box, text)
    g.box, g.text = box, text
    g.head = VGroup(*text[0][:len(head) - 0])  # "19.i." has no spaces: one glyph per character
    return g


def mini_card(i):
    num = T(f"19.{i}", 44, DIM)
    sub = T(SUBJECT[i], 28, DIM)
    VGroup(num, sub).arrange(DOWN, buff=0.28)
    box = RoundedRectangle(corner_radius=0.2, width=MINI_W, height=MINI_H).set_stroke(DIM, 2).set_fill(BG, 0)
    VGroup(num, sub).move_to(box)
    g = VGroup(box, num, sub)
    g.box, g.num, g.sub = box, num, sub
    g.text = VGroup(num, sub)
    return g


def ex19_row():
    header = T("Exercise 19", 52).move_to([0, HEADER_Y, 0])
    cards = VGroup(*[mini_card(i).move_to([SLOT_X[i - 1], ROW_Y, 0]) for i in range(1, 5)])
    lab = T("solutions: part 10", 30, DIM)
    pill = RoundedRectangle(corner_radius=0.18, width=lab.width + 0.5, height=lab.height + 0.36)
    pill.set_stroke(DIM, 1.5)
    tag = VGroup(pill, lab).move_to([0, TAG_Y, 0])
    lab.move_to(pill)
    g = VGroup(header, cards, tag)
    g.header, g.cards, g.tag = header, cards, tag
    return g


def hint(i, size=28, width=None):
    t = T(HINTS[i], size, DIM)
    if width is not None and t.width > width:
        t.scale(width / t.width)
    return t


def hints_line(size=28):
    return T(HINTS_LINE, size, DIM)


# ══ this scene's pieces ════════════════════════════════════════════════════════

ARRAYS = [("genres", 3), ("actors", 10), ("directors", 1), ("producers", 1), ("writers", 1),
          ("composers", 1), ("trivia_entries", 5)]


def kid_star_tree():
    """All 14 top-level keys of The Kid; genres open, the other arrays as stubs with their length."""
    kid = J.kid_value()
    tree = J.json_tree(kid, open=[("genres",)], counts=True, size=28, row_gap=0.4,
                       label_pad=0.32, trunk_gap=0.15)
    tree.orig = {}
    for p in tree.paths:
        if tree.kinds[p] in ("leaf", "more"):
            tree.orig[p] = tree.nodes[p].get_color()
        if p in tree.labels:
            tree.orig[("label",) + p] = tree.labels[p].get_color()
    tree.top = [p for p in tree.paths if len(p) == 1]
    return tree


def doc(src, size=26, outline=None):
    card = D.doc_card(src, size=size)
    for g in chars(card.code, "…"):
        g.set_color(DIM)
    if outline:
        card.frame.set_stroke(outline, 4)
    return card


def own_card():
    return doc('{\n  "person_id": "nm0905154",\n  "name": "Lana Wachowski",\n  …\n}', size=30, outline=YELLOW)


def chaplin_card():
    return doc('{\n  "name": "Charles Chaplin",\n  "directed": [ … ], …\n}', size=26)


def coogan_card():
    return doc('{\n  "name": "Jackie Coogan",\n  "acted_in": [ … ], …\n}', size=26)


def morris_card(pid):
    card = doc('{\n  "person_id": "' + pid + '",\n  "name": "John Morris", …\n}', size=26)
    card.code.find(f'"{pid}"').set_color(GREEN)
    card.code.find('"John Morris"').set_color(DIM)
    return card


def genre_bars_fallback():
    data = [("Drama", 1691), ("Comedy", 878), ("Action", 869), ("Adventure", 719), ("Crime", 621)]
    rows = VGroup()
    for k, (name, n) in enumerate(data):
        y = -0.5 * k
        lab = T(name, 28).move_to([0, y, 0], aligned_edge=RIGHT).shift(-2.9 * RIGHT)
        lab.align_to([-2.9, 0, 0], RIGHT)
        bar = Rectangle(width=4.2 * n / 1691, height=0.32).set_stroke(width=0).set_fill(BLUE, 0.75)
        bar.move_to([-2.7, y, 0], aligned_edge=LEFT)
        num = T(f"{n:,}", 28, GOLD).next_to(bar, RIGHT, buff=0.15)
        rows.add(VGroup(lab, bar, num))
    return rows.move_to(ORIGIN)


def genre_bars_small():
    try:
        g = load_scene("ch8_s3_group").genre_bars(size=28, max_len=3.6, pitch=0.5, header=False)
        return VGroup(*g.rows).move_to(ORIGIN), True
    except Exception:  # noqa: BLE001
        return genre_bars_fallback(), False


def pause_label():
    return T("pause and try it", 30, DIM).move_to([0, -3.35, 0]).align_to([6.6, 0, 0], RIGHT)


def to_top(card):
    """Where the hero card sits during its hint: scaled 0.75, centred, top edge at TOP_EDGE."""
    t = card.copy().scale(TOP_SCALE)
    t.move_to([0, TOP_EDGE - t.height / 2, 0])
    return t


class TryThese(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.back(self.cur, self.loose, run_time=1.2)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── the row's moves ────────────────────────────────────────────────────────
    def put_row(self, row):
        self.row = row
        self.add(row.header, *row.cards, row.tag)

    def grow(self, i, run_time):
        """Mini card i grows to the hero card; the rest of the row leaves."""
        row = self.row
        mini = row.cards[i - 1]
        others = [row.header, row.tag] + [c for k, c in enumerate(row.cards) if k != i - 1]
        self.remove(mini)
        self.add(mini.box, mini.num, mini.sub)
        hero = ex19_card(i).move_to([0, HERO_Y, 0])
        self.play(*during(disappear(*others, mini.num, mini.sub), 0, 0.42),  # early: the question card, read whole
                  *during([ReplacementTransform(mini.box, hero.box)], 0.1, 0.8),
                  *during(appear(hero.text, shift=None), 0.5, 1), run_time=run_time)
        self.remove(hero.box, hero.text)
        self.add(hero)
        return hero

    def back(self, cur, loose, run_time):
        """The current card (hero or badge) shrinks back into its slot; hint pictures leave; the row returns."""
        i = cur.idx
        row = ex19_row()
        mini = row.cards[i - 1]
        others = [row.header, row.tag] + [c for k, c in enumerate(row.cards) if k != i - 1]
        self.remove(cur)
        self.add(cur.box, cur.text)
        self.play(*during(disappear(*loose, cur.text), 0, 0.42),  # early: the exercise row returns, read whole before
                  *during([ReplacementTransform(cur.box, mini.box)], 0.15, 0.8),
                  *during(appear(*others, mini.num, mini.sub, shift=None, lag=0.1), 0.5, 1),
                  run_time=run_time)
        self.remove(mini.box, mini.num, mini.sub, *others)
        self.put_row(row)

    def lift(self, hero, run_time):
        tgt = to_top(hero)
        self.play(hero.animate.scale(TOP_SCALE).move_to(tgt), run_time=run_time)

    def pause_try(self, c):
        lab = pause_label()
        if c.remaining - PAUSE > 0.05:
            self.wait(c.remaining - PAUSE)
        self.play(*appear(lab, shift=None), run_time=0.6)  # early: the on-screen pause cue
        return lab

    # ── c8.try.1: the row, then 19.1 and its hint ──────────────────────────────
    def clip1(self):
        with self.say("c8.try.1", gap=GAP) as c:
            row = ex19_row()
            c.wait_until("four")
            self.play(*appear(row.header), run_time=1.0)
            self.add(row.header)
            c.wait_until("four questions")
            self.play(*appear(*row.cards, lag=0.3), run_time=min(1.8, c.until("for each")))  # early: the four cards, walked one by one later
            c.wait_until("sol")
            self.play(*appear(row.tag), run_time=1.0)
            self.remove(row.header, *row.cards, row.tag)
            self.put_row(row)

            c.wait_until("rename")
            hero = self.grow(1, run_time=min(1.6, c.until("when lana")))
            hero.idx = 1
            c.wait_until("hint")

            # the card shrinks to a badge; The Kid's tree arrives on the left
            badge_lab = T("19.1", 40, YELLOW)
            badge_box = RoundedRectangle(corner_radius=0.18, width=badge_lab.width + 0.7, height=0.95)
            badge_box.set_stroke(DIM, 2).set_fill(BG, 0)
            badge = VGroup(badge_box, badge_lab).move_to([0, 3.2, 0]).align_to([6.6, 0, 0], RIGHT)
            badge_lab.move_to(badge_box)
            badge.box, badge.text, badge.idx = badge_box, badge_lab, 1
            tree = kid_star_tree()
            if tree.height > 6.3:
                tree.scale(6.3 / tree.height)
            tree.move_to([0, -0.25, 0]).align_to([-6.5, 0, 0], LEFT)
            self.remove(hero)
            self.add(hero.box, hero.text)
            self.play(*during(disappear(hero.text), 0, 0.4),
                      *during([ReplacementTransform(hero.box, badge_box)], 0.1, 0.7),
                      *during(appear(badge_lab, shift=None), 0.55, 1),
                      *during(appear(tree, shift=None), 0.5, 1), run_time=min(1.6, c.until("the path")))
            self.remove(badge_box, badge_lab)
            self.add(badge)
            c.wait_until("the path")
            path = Mono("$.*[*]", 64).move_to([4.2, 1.7, 0])
            self.play(*appear(path), run_time=min(0.9, c.until("dollar")))
            c.wait_until("dollar")
            box = token_box(VGroup(*path[0:1]), path, height=path.height + 0.3)
            self.play(FadeIn(box), *P.light_step(tree, ()), run_time=min(0.9, c.until("star")))
            c.wait_until("star")
            self.play(Transform(box, token_box(VGroup(*path[1:3]), path, height=path.height + 0.3)),
                      *[a for p in tree.top for a in P.light_step(tree, p)],
                      run_time=min(1.2, c.until("square brackets")))
            c.wait_until("square brackets")

            # [*]: scalars fall away, the arrays' elements light, a GOLD counter adds them up
            scalars = [p for p in tree.top if tree.kinds[p] == "leaf"]
            counter = T("3", 80, GOLD).move_to([4.2, -0.3, 0])
            self.play(Transform(box, token_box(VGroup(*path[3:6]), path, height=path.height + 0.3)),
                      *[a for p in scalars for a in P.light_step(tree, p, on=False)],
                      *[a for k in range(3) for a in P.light_step(tree, ("genres", k))],
                      *during(appear(counter, shift=None), 0.5, 1), run_time=1.4)
            total = 3
            steps = [[("actors", 10)], [("directors", 1), ("producers", 1), ("writers", 1), ("composers", 1)],
                     [("trivia_entries", 5)]]
            for grp in steps:
                self.wait(0.25)
                total += sum(n for _, n in grp)
                new = T(str(total), 80, GOLD).move_to(counter)
                anims = []
                for key, _ in grp:
                    cnt = tree.nodes[(key,)][1]
                    anims += [cnt.animate.set_color(GOLD), FlashAround(cnt, color=GOLD, time_width=1.5)]
                self.play(*anims, *swap(counter, new), run_time=0.9)
                counter = new
            settle(self, tree)
            elems = T("elements", 32, DIM).next_to(counter, DOWN, buff=0.25)
            c.wait_until("kid")
            self.play(FlashAround(counter, color=GOLD, time_width=1.5), *appear(elems),
                      run_time=min(1.4, c.until("own")))
            c.wait_until("own")

            # her own document takes the tree's place
            own = own_card().move_to([-2.7, 0.5, 0])
            own_lab = T("her own document", 36, YELLOW).next_to(own, DOWN, buff=0.35)
            self.play(*during(disappear(tree), 0, 0.45), *during(appear(own, shift=None), 0.5, 1),
                      run_time=1.3)
            c.wait_until(own_word=own_lab)
            self.play(*appear(own_lab), run_time=0.9)
            lab = self.pause_try(c)
        self.back(badge, [path, box, counter, elems, own, own_lab, lab], run_time=BACK_RT)

    # ── c8.try.2: 19.2, json_array_length ───────────────────────────────────────
    def clip2(self):
        with self.say("c8.try.2", gap=GAP) as c:
            self.play(FlashAround(self.row.cards[1], time_width=1.5), run_time=min(1.0, c.until("who are")))
            c.wait_until("who are")
            hero = self.grow(2, run_time=1.5)
            hero.idx = 2
            c.wait_until("hint")
            code = Code("json_array_length(person, '$.directed')", size=36).move_to([0, 1.45, 0])
            self.lift(hero, run_time=1.0)
            self.play(*appear(code, shift=None), run_time=min(1.0, c.until("charles")))
            c.wait_until("charles")
            ch = chaplin_card().move_to([-3.35, 0, 0]).align_to([0, 0.85, 0], UP)
            a1 = Arrow(ch.get_bottom(), ch.get_bottom() + 0.7 * DOWN, buff=0.1, stroke_width=4).set_color(GOLD)
            five = T("5", 64, GOLD).next_to(a1, DOWN, buff=0.1)
            self.play(*appear(ch, shift=None), run_time=1.0)
            c.wait_until("five elements")
            self.play(GrowArrow(a1), *during(appear(five), 0.4, 1), run_time=min(1.2, c.until("never")))
            c.wait_until("never")
            co = coogan_card().move_to([3.35, 0, 0]).align_to([0, 0.85, 0], UP)
            a2 = Arrow(co.get_bottom(), co.get_bottom() + 0.7 * DOWN, buff=0.1, stroke_width=4).set_color(PINK)
            q = T("?", 64, PINK).next_to(a2, DOWN, buff=0.1)
            self.play(*appear(co, shift=None), run_time=1.0)
            c.wait_until("directed anything")
            self.play(GrowArrow(a2), *during(appear(q), 0.4, 1), run_time=1.0)
            lab = self.pause_try(c)
        self.back(hero, [code, ch, a1, five, co, a2, q, lab], run_time=BACK_RT)

    # ── c8.try.3: 19.3, list_has_any ────────────────────────────────────────────
    def clip3(self):
        with self.say("c8.try.3", gap=GAP) as c:
            self.play(FlashAround(self.row.cards[2], time_width=1.5), run_time=min(1.0, c.until("in which")))
            c.wait_until("in which")
            hero = self.grow(3, run_time=1.5)
            hero.idx = 3
            c.wait_until("hint")
            l1 = Code("list_has_any([1, 2], [2, 3])", size=34)
            l2 = Code("list_has_any([1, 2], [3])", size=34)
            l1.move_to([0, 1.5, 0]).align_to([-5.4, 0, 0], LEFT)
            l2.move_to([0, 0.6, 0]).align_to([-5.4, 0, 0], LEFT)
            ax = l1.get_right()[0] + 0.45
            ar1 = T("→", 40, DIM).move_to([ax + 0.25, l1.get_y(), 0])
            ar2 = T("→", 40, DIM).move_to([ax + 0.25, l2.get_y(), 0])
            r1 = Mono("true", 36, BLUE).next_to(ar1, RIGHT, buff=0.35)
            r2 = Mono("false", 36, BLUE).next_to(ar2, RIGHT, buff=0.35)
            r1.align_to(ar1.get_right() + 0.35 * RIGHT, LEFT)
            r2.align_to(r1, LEFT)
            self.lift(hero, run_time=1.0)
            self.play(*appear(l1, shift=None), run_time=0.9)
            c.wait_until("is true")
            self.play(*appear(ar1, r1, lag=0.3), run_time=min(1.0, c.until("at least")))
            c.wait_until("at least")
            twos = [l1.find("2", nth=0), l1.find("2", nth=1)]
            self.play(*[a for g in twos for a in recolor(g, YELLOW)],
                      *[FlashAround(g, color=YELLOW, time_width=1.5) for g in twos],
                      run_time=min(1.2, c.until("in common")))
            self.wait(0.3)
            self.play(*appear(l2, ar2, r2, lag=0.3, shift=None), run_time=min(1.2, max(0.6, c.until("kid") - 0.1)))
            c.wait_until("kid")

            # The Kid's two lists, Chaplin in both
            dirs = P.list_box(["Charles Chaplin"], size=28, serif=True)
            acts = P.list_box(["Charles Chaplin", "Edna Purviance", "Jackie Coogan", "…"], size=28, serif=True)
            dl = Mono("directors", 28, DIM)
            al = Mono("actors", 28, DIM)
            dirs.move_to([0, -1.3, 0]).align_to([-3.4, 0, 0], LEFT)
            acts.move_to([0, -2.4, 0]).align_to([-3.4, 0, 0], LEFT)
            dl.move_to(dirs).align_to([-3.75, 0, 0], RIGHT)
            al.move_to(acts).align_to([-3.75, 0, 0], RIGHT)
            lists = VGroup(dl, dirs, al, acts)
            lists.shift(-lists.get_center()[0] * RIGHT)
            self.play(*appear(dl, dirs, al, acts, lag=0.2, shift=None), run_time=1.2)
            c.wait_until("chaplin")
            chs = [dirs.items[0], acts.items[0]]
            self.play(*[a for g in chs for a in recolor(g, YELLOW)],
                      *[FlashAround(g, color=YELLOW, time_width=1.5) for g in chs],
                      run_time=min(1.2, c.until("ids")))
            settle(self, dirs)
            settle(self, acts)
            c.wait_until("ids")

            # same name, different IDs
            m1 = morris_card("nm0606657").move_to([-3.35, 0, 0]).align_to([0, 1.95, 0], UP)
            m2 = morris_card("nm0606658").move_to([3.35, 0, 0]).align_to([0, 1.95, 0], UP)
            self.play(*during(disappear(l1, l2, ar1, ar2, r1, r2), 0, 0.45),
                      *during(appear(m1, m2, lag=0.25, shift=None), 0.5, 1), run_time=1.6)
            lab = self.pause_try(c)
        self.back(hero, [dl, dirs, al, acts, m1, m2, lab], run_time=BACK_RT)

    # ── c8.try.4: 19.4, unnest + a cast ─────────────────────────────────────────
    def clip4(self):
        with self.say("c8.try.4") as c:
            self.play(FlashAround(self.row.cards[3], time_width=1.5), run_time=min(1.0, c.until("which five")))
            c.wait_until("which five")
            hero = self.grow(4, run_time=1.5)
            hero.idx = 4
            c.wait_until("hint")
            bars, self.s3_bars = genre_bars_small()
            bars.move_to([0, 0.35, 0])
            self.lift(hero, run_time=1.0)
            self.play(*appear(*bars, lag=0.15, shift=None), run_time=min(1.4, c.until("cast")))
            c.wait_until("cast")
            code = Code("movie->>'rating'", size=40)
            cast = Mono("::", 56, GOLD)
            VGroup(code, cast).arrange(RIGHT, buff=0.6).move_to([-0.6, -2.15, 0])
            cast.match_y(code)
            tag = T("a string", 30, RED).next_to(code, DOWN, buff=0.3)
            num = T("a number", 30, GOLD).next_to(cast, DOWN, buff=0.3)
            self.play(*appear(code, shift=None), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=0.9)
            c.wait_until("number")
            self.play(*appear(cast, shift=None), *appear(num), run_time=1.0)
            lab = self.pause_try(c)
        self.cur = hero
        self.loose = [*bars, code, cast, tag, num, lab]
