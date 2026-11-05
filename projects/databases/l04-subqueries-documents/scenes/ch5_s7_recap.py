"""Chapter 5, scene 7: try these (Exercises 15 and 16, with hints), then the recap. Clips c5.recap.1 – c5.recap.4.

Recap: ch3 s8's pattern, five DIM slots along the top; each callback big while its sentence plays
(its short line under it), then it shrinks into its slot. Ends non-empty by design (chapter's last
scene, like ch3 s8): the last frame is load_scene("ch6_s1_hook").open_card(), held ~8 s.

Exports (static): ex_card(n) -> the Exercise 15 / 16 card (ch3 s8 ex_card look), at ORIGIN.
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
R1 = load_scene("ch5_s1_hook")
R2 = load_scene("ch5_s3_update")
R3 = load_scene("ch5_s4_genres")
R4 = load_scene("ch5_s5_forms")
R5 = load_scene("ch5_s6_why")
END_CARD = lambda: load_scene("ch6_s1_hook").open_card()   # ch6's first frame

EX = {
    15: ["Exercise 15. An index is a form of redundancy too. How is it",
         "similar to denormalisation, and how is it different?"],
    16: ["Exercise 16. One query over the relational tables → one JSON",
         "document per movie: ID, title, year, genres (array of strings),",
         "actors (array of {person_id, name}). How does your output",
         "differ from the JSON database?"],
}
INDEX_SRC = """-- Make an index to efficiently find movies by year
CREATE INDEX movies_by_year ON movies (year);"""
OBJ_SRC = """SELECT json_object('title', title, 'year', year) AS doc
FROM movies
WHERE movie_id = 'tt0012349';"""
OBJ_OUT = '{"title":"The Kid","year":1921}'
HINTS = ["Who keeps the copies consistent?",
         "What happens on reads? On writes?",
         "Does it change how queries are written, or what they return?"]

SLOT_X = (-5.6, -2.8, 0.0, 2.8, 5.6)
SLOT_Y = 3.1
SLOT_W, SLOT_H = 2.55, 1.25
HERO_W, HERO_H, HERO_Y = 12.4, 4.9, -0.25
LINE_Y = -3.25
LINES = [("once, or 21 copies", {"21": GOLD}),
         ("update anomaly", {"update anomaly": RED}),
         ("deletion and insertion anomalies", {"anomalies": RED}),
         ("first normal form: atomic values", {"atomic": GREEN}),
         ("derive the copies", {"derive": GREEN})]
CARD_S = 28 / 24          # ch2 s3's schema cards


# ---------------------------------------------------------------- helpers
def ex_card(n, size=30):
    lines = EX[n]
    head = f"Exercise {n}."
    text = VGroup(*[T(s, size, t2c={head: YELLOW} if i == 0 else None) for i, s in enumerate(lines)])
    text.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.2, width=text.width + 0.8, height=text.height + 0.7)
    box.set_stroke(DIM, 2).set_fill(BG, 0)
    text.move_to(box)
    g = VGroup(box, text)
    g.box, g.text = box, text
    return g


def fit(mob, w, h, center, most=10.0):
    mob.scale(min(w / mob.width, h / mob.height, most))
    mob.move_to(center)
    return mob


def flow_row():
    """Flow (2024) as a small BLUE movie row with RED edges, 'movies' over it."""
    specs = [(Mono("tt4772188", 28), 2.3), (T("Flow", 30), 1.3), (T("2024", 30, GOLD), 1.2)]
    cells = VGroup()
    for mob, w in specs:
        r = Rectangle(width=w, height=0.62).set_stroke(RED, 3).set_fill(BLUE, 0.15)
        cells.add(VGroup(r, mob.move_to(r)))
    cells.arrange(RIGHT, buff=0)
    head = Mono("movies", 28, BLUE, weight=BOLD).next_to(cells, LEFT, buff=0.2)
    g = VGroup(head, cells)
    g.head, g.cells = head, cells
    return g


def count_tag(n, word):
    g = VGroup(T(n, 44, GOLD), T(word, 30, DIM)).arrange(RIGHT, buff=0.2)
    g[1].align_to(g[0], DOWN)
    return g


def to_slot(mob, i):
    k = min((SLOT_W - 0.25) / mob.width, (SLOT_H - 0.2) / mob.height)
    ctr, dst, s0 = mob.get_center(), np.array([SLOT_X[i], SLOT_Y, 0]), mob.copy()

    def upd(m, a):          # shrink in place (first 45%), then rise into the slot: passes no other slot
        a1 = smooth(min(1.0, a / 0.45))
        a2 = smooth(max(0.0, (a - 0.45) / 0.55))
        m.become(s0.copy().scale(1 + (k - 1) * a1, about_point=ctr).shift(a2 * (dst - ctr)))
    return UpdateFromAlphaFunc(mob, upd)


class Recap(NarratedScene):
    def construct(self):
        self.exercise15()
        self.exercise16()
        self.recap()
        self.next_time()

    # ------------------------------------------------------------ c5.recap.1
    def exercise15(self):
        with self.say("c5.recap.1", gap=1.5) as c:
            title = T("Try these", 48).move_to([0, 3.3, 0])
            self.play(*appear(title), run_time=min(1.0, c.until("ex15")))
            c.wait_until("ex15")
            card = ex_card(15, 32).move_to([0, 1.95, 0])
            self.play(*appear(card, shift=None), run_time=min(1.2, c.until("an index is")))  # early: the exercise card, read whole
            c.wait_until("index")
            code = Code(INDEX_SRC, 28).move_to([0, 0.2, 0])
            self.play(*appear(code, shift=None), run_time=min(1.4, c.until("how is an index")))
            hints = VGroup(*[T(h, 32, YELLOW) for h in HINTS]).arrange(DOWN, buff=0.38)
            hints.move_to([0, -1.85, 0])
            for i, cue in enumerate(["who", "rw", "queries"]):
                c.wait_until(cue)
                nxt = ["rw", "queries", None][i]
                self.play(*appear(hints[i]), run_time=min(1.0, 0.7 * c.until(nxt)))  # early: each hint lands on its {mark}

    # ------------------------------------------------------------ c5.recap.2
    def exercise16(self):
        with self.say("c5.recap.2", gap=2.5) as c:
            card = ex_card(16, 28)
            card.move_to([0, 3.7 - card.height / 2, 0])
            sweep_clear(self, time_span(FadeIn(card), 0.6, 1.3), run_time=min(1.3, c.until("write one query")))  # early: the exercise card, read whole

            c.wait_until("object")
            code = Code(OBJ_SRC, 26).move_to([0, 0.05, 0])
            out = Mono(OBJ_OUT, 28, t2c={"1921": GOLD, '"The Kid"': GOLD}).move_to([0, -1.2, 0])
            self.play(*appear(code, shift=None), run_time=min(1.4, 0.5 * c.until("list")))
            self.play(*appear(out), run_time=min(1.0, c.until("list")))
            c.wait_until("list")
            lst = R4.list_cell(28)
            lst.scale(0.8).move_to([0, -2.5, 0])
            self.play(*appear(lst), run_time=min(1.0, c.until("careful")))

            # careful: the card and the list leave, the query and its result move up
            c.wait_until("careful")
            code.generate_target().move_to([0, 2.85, 0])
            out.generate_target().move_to([0, 1.75, 0]).align_to([6.4, 0, 0], RIGHT)
            self.play(*during(disappear(card, lst), 0, 0.4),
                      *during([MoveToTarget(code), MoveToTarget(out)], 0.35, 1),
                      run_time=min(1.6, c.until("kaiva")))
            m = SCH.schema_map()
            hp = m.cards["has_position"].copy().scale(CARD_S)
            hp.move_to([-4.85, 0, 0]).align_to([0, 1.05, 0], UP)
            pr = m.cards["plays_role"].copy().scale(CARD_S)
            pr.move_to([-1.35, 0, 0]).align_to([0, 1.05, 0], UP)
            kaiva = T("Kaiva", 36, YELLOW).move_to([0, 1.65, 0]).align_to([-6.5, 0, 0], LEFT)
            ten = count_tag("10", "actors").move_to([hp.get_x(), -1.85, 0])
            zero = count_tag("0", "roles").move_to([pr.get_x(), -1.85, 0])
            c.wait_until("kaiva")
            self.play(*appear(kaiva), run_time=min(1.0, c.until("has position")))
            c.wait_until("has position")
            self.play(*appear(hp, ten, shift=None, lag=0.4), run_time=min(1.3, c.until("plays role")))
            c.wait_until("plays role")
            self.play(*appear(pr, zero, shift=None, lag=0.4), run_time=min(1.3, c.until("and flow")))
            c.wait_until("and flow")
            flow = flow_row()
            flow.move_to([0, -2.8, 0]).align_to([-6.5, 0, 0], LEFT)
            none = T("no actors anywhere", 32, RED).next_to(flow, RIGHT, buff=0.35)
            self.play(*appear(flow, none, shift=None, lag=0.5), run_time=min(1.4, c.until("compare")))  # early: Flow's row and its caption land on "and Flow has no actors"

            # compare: s6's derived-data stack comes in on the right, the result sends an arrow to it;
            # Kaiva / Flow stay up (the recap's sweep clears them), so the frame stays balanced
            c.wait_until("compare")
            stack = R5.derived_stack(with_label=False)
            stack.scale(1.75 / stack.height).move_to([4.6, -0.45, 0])
            slab = T("derived data,\nlike a cache", 30, TEAL, line_spacing=0.8).next_to(stack, DOWN, buff=0.25)
            arrow = Arrow([4.6, out.get_bottom()[1] - 0.05, 0], stack.get_top() + 0.05 * UP, buff=0.05,
                          stroke_width=5, color=YELLOW, max_tip_length_to_length_ratio=0.35)
            self.play(*appear(stack, slab, shift=None, lag=0.3), run_time=min(1.2, 0.45 * c.until()))  # early: s6's derived-data stack, a callback shown whole
            self.play(GrowArrow(arrow), run_time=min(1.0, c.until()))

    # ------------------------------------------------------------ c5.recap.3
    def recap(self):
        with self.say("c5.recap.3") as c:
            slots = [RoundedRectangle(corner_radius=0.12, width=SLOT_W, height=SLOT_H)
                     .set_stroke(DIM, 1.5, opacity=0.6).move_to([x, SLOT_Y, 0]) for x in SLOT_X]
            sweep_clear(self, *during(appear(*slots, shift=None, lag=0.15), 0.5, 1),
                        run_time=min(1.4, c.until("r1")))
            self.slots = slots
            raw = [R1.recap_r1(), R2.recap_r2(), R3.recap_r3(), R4.recap_r4(), R5.recap_r5()]
            # re-wrap: recap_r2's `.update` attribute shadows Mobject.update (play() would call it)
            heroes = [VGroup(*r.submobjects) for r in raw]
            heroes[0].copies, heroes[2].gaps = raw[0].copies, raw[2].gaps
            for h in heroes:
                fit(h, HERO_W, HERO_H, [0, HERO_Y, 0])
            lines = [T(s, 36, t2c=t2c).move_to([0, LINE_Y, 0]) for s, t2c in LINES]
            self.heroes, self.lines = heroes, lines

            # r1: one people row against 21 copies
            c.wait_until("r1")
            self.play(*appear(heroes[0], lines[0], shift=None, lag=0.3), run_time=min(1.4, c.until("r2")))  # early: a recap line lands on its {r} cue
            c.wait_until("twenty-one")
            self.play(*flash([heroes[0].copies], color=GOLD), run_time=min(1.5, c.until("r2")))

            # r2: r1 into its slot; the UPDATE row against its copies, one RED
            c.wait_until("r2")
            self.hero_step(c, 1, "r3")

            # r3: the 26 and 23 grids with three RED gaps
            c.wait_until("r3")
            self.hero_step(c, 2, "twenty-three")
            c.wait_until("twenty-three")
            self.play(*flash(list(heroes[2].gaps), color=RED), run_time=min(1.5, c.until()))

    def hero_step(self, c, i, nxt):
        """Hero i-1 (its line fading) into its slot, then hero i with its line in its place."""
        old, old_line = self.heroes[i - 1], self.lines[i - 1]
        anims = [*during(disappear(old_line), 0, 0.3), *during([to_slot(old, i - 1)], 0, 0.5),
                 *during(appear(self.heroes[i], self.lines[i], shift=None, lag=0.3), 0.5, 1)]
        self.play(*anims, run_time=min(1.2, c.until(nxt)))  # early: a recap callback and its line land on its {r} cue

    # ------------------------------------------------------------ c5.recap.4
    def next_time(self):
        end = END_CARD()
        with self.say("c5.recap.4") as c:
            self.hero_step(c, 3, "r5")
            c.wait_until("r5")
            self.hero_step(c, 4, "next")

            # next: r5 into its slot (the row complete), then the row clears to ch6's picture
            c.wait_until("next")
            self.play(*during(disappear(self.lines[4]), 0, 0.35), *during([to_slot(self.heroes[4], 4)], 0.1, 0.8),
                      run_time=min(1.4, c.until("right shape")))
            c.wait_until("right shape")
            sweep_clear(self, run_time=min(1.2, c.until("tree")))
            c.wait_until("tree")
            self.play(*appear(end.tree, shift=None), run_time=min(1.6, c.until("tangle")))
            c.wait_until("tangle")
            self.play(*appear(*end.others, shift=None, lag=0.15),
                      *[Create(l) for l in end.links], run_time=min(1.4, c.until("shape")))
            c.wait_until("shape")
            self.play(FadeIn(end.doc, scale=0.9), *during(appear(end.ask), 0.4, 1),
                      run_time=min(1.4, c.until()))
            for part in (end.tree, end.others, end.links, end.doc, end.ask):
                self.remove(*part.get_family())
            self.add(end)
        self.wait(7.7)      # the end card (= ch6's first frame), ~8 s after the last word; no fade (see docstring)
