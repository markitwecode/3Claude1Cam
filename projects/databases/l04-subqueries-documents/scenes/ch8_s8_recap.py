"""Chapter 8, scene 8: the chapter and lecture recap, then the end card. Clips c8.recap.1 – c8.recap.3.

c8.recap.1: a 3 x 2 grid of the chapter's thumbnails (s2 rows, s2 loop, s3 bars, s4 join, s5 Thacker,
s6 card), each with its short line, on {r1}..{r6}.
c8.recap.2: grid clears on {close}; "same movies, two shapes": ch1 s2's schema map (every table that
holds a piece of The Kid tinted YELLOW) beside ch4 s3's Kid document; on {fast} three question cards
(ch8 s1's look) slide under the shape that answers them more easily.
c8.recap.3: lands on exactly load_scene("ch9_s1_intro").open_card() (part 9 / part 10 cards on
{next}, the graph tangle and its caption on {graph}), held ~8 s; no fade (ch9 s1 opens on it).
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

U = load_scene("ch8_s2_unnest")
G = load_scene("ch8_s3_group")
J = load_scene("ch8_s4_join")
X = load_scene("ch8_s5_text")
S6 = load_scene("ch8_s6_summary")
SCH = load_scene("ch1_s2_schema")
D = load_scene("ch4_s3_movie")
N9 = load_scene("ch9_s1_intro")

# ---------------------------------------------------------------- recap grid
THUMB_W, THUMB_H = 4.25, 2.05
COL_X = [-4.45, 0.0, 4.45]
ROW_TOP = [3.0, -0.15]
LABELS = [
    "un-nest: one row\nper element",
    "once per movie, like a\ncorrelated subquery",
    "then all of SQL works",
    "unplanned questions\nneed joins",
    "crude patterns; search\nengines stem and rank",
    "the JSON toolkit",
]


def _thumb_sources():
    return [U.recap_thumb_rows(), U.recap_thumb_loop(), G.recap_thumb(), J.recap_thumb(),
            X.recap_thumb(), S6.recap_thumb(width=4.0)]


def thumbs():
    out = []
    for i, t in enumerate(_thumb_sources()):
        r, k = divmod(i, 3)
        t.scale(min(THUMB_W / t.width, THUMB_H / t.height))
        t.move_to([COL_X[k], ROW_TOP[r] - THUMB_H / 2, 0])
        out.append(t)
    return out


def labels():
    out = []
    for i, s in enumerate(LABELS):
        r, k = divmod(i, 3)
        lab = T(s, 30, line_spacing=0.7)
        lab.move_to([COL_X[k], ROW_TOP[r] - THUMB_H - 0.1 - lab.height / 2, 0])
        out.append(lab)
    return out


# ---------------------------------------------------------------- two shapes
MAP_X, DOC_X, SHAPE_Y = -3.5, 3.75, 0.6
QUESTIONS = ["Actors' ages?", "Movies per genre?", "Who's in The Kid?"]   # row order, left to right
Q_H, Q_Y, Q_Y2 = 0.74, -1.95, -2.75


def two_map():
    m = SCH.schema_map()
    m.remove(m.count_group)
    m.scale_to_fit_width(6.3)
    m.move_to([MAP_X, SHAPE_Y, 0])
    return m


def two_doc():
    d = D.kid_doc(18)
    d.scale_to_fit_height(3.6)
    d.move_to([DOC_X, SHAPE_Y, 0])
    return d


def q_card(q, w):
    """ch8 s1's question-card look: DIM rounded box, GOLD bold '?' on the left, T 28 text."""
    t = T(q, 28)
    box = RoundedRectangle(corner_radius=0.15, width=w, height=Q_H).set_stroke(DIM, 2).set_fill(BG, 0)
    mark = T("?", 40, GOLD, weight=BOLD).move_to([box.get_left()[0] + 0.4, 0, 0])
    t.move_to([mark.get_right()[0] + 0.25 + t.width / 2, 0, 0])
    g = VGroup(box, mark, t)
    g.box, g.mark, g.text = box, mark, t
    return g


def q_cards():
    w = max(T(q, 28).width for q in QUESTIONS) + 0.95
    cards = [q_card(q, w) for q in QUESTIONS]
    for c, x in zip(cards, (-4.45, 0.0, 4.45)):
        c.move_to([x, Q_Y, 0])
    return cards


class Recap(NarratedScene):
    def construct(self):
        self.grid()
        self.shapes()
        self.next()

    # ------------------------------------------------------------ c8.recap.1
    def grid(self):
        with self.say("c8.recap.1", gap=1.5) as c:
            title = T("Recap", 36).move_to([0, 3.32, 0])
            self.play(FadeIn(title), run_time=min(1.0, c.until("r1")))
            c.wait_until("r1")
            ts, ls = thumbs(), labels()
            cues = ["r1", "r2", "r3", "r4", "r5", "r6"]
            for i in range(6):
                c.wait_until(cues[i])
                nxt = cues[i + 1] if i < 5 else None
                self.play(*appear(ts[i], ls[i], lag=0.3, shift=None),  # early: each recap line lands on its {r} cue
                          run_time=min(1.4, 0.6 * c.until(nxt)))

    # ------------------------------------------------------------ c8.recap.2
    def shapes(self):
        with self.say("c8.recap.2") as c:
            cap = T("same movies, two shapes", 40).move_to([0, 3.3, 0])
            sweep_clear(self, run_time=min(1.2, c.until("two")))
            c.wait_until("two")
            self.play(*appear(cap), run_time=min(1.0, c.until("tables")))
            c.wait_until("tables")
            m = two_map()
            self.play(*appear(m, shift=None), run_time=min(1.2, c.until("each fact")))
            c.wait_until("each fact")
            anims = []
            for cd in m.cards.values():
                anims += [cd.box.animate.set_fill(YELLOW, 0.14), cd.title.animate.set_color(YELLOW)]
            self.play(*anims, run_time=min(1.2, c.until("documents")))
            settle(self, m)
            c.wait_until("documents")
            d = two_doc()
            self.play(*appear(d, shift=None), run_time=min(1.2, c.until("one piece")))
            c.wait_until("fast")
            ages, genre, who = q_cards()
            self.play(*appear(ages, genre, who, lag=0.3), run_time=min(1.3, c.until("so the")))  # early: the three questions, shown together, then sorted
            c.wait_until("so the")
            p0 = ages.get_center()
            path = VMobject().set_points_as_corners([p0, [p0[0], Q_Y2, 0], [MAP_X, Q_Y2, 0]])
            self.play(*during([MoveAlongPath(ages, path)], 0, 0.5),   # down first, then across: clear of the next card
                      *during([genre.animate.move_to([MAP_X, Q_Y, 0])], 0.5, 1),
                      *during([who.animate.move_to([DOC_X, Q_Y, 0])], 0.2, 0.8),
                      run_time=min(2.0, c.until()))

    # ------------------------------------------------------------ c8.recap.3
    def next(self):
        with self.say("c8.recap.3", gap=8.0) as c:
            oc = N9.open_card()
            sweep_clear(self, run_time=min(1.2, c.until("nine")))
            c.wait_until("nine")
            self.play(*appear(oc.part9), run_time=min(1.0, c.until("ten")))  # early: lands on "nine" (its word "parts" is said just before)
            c.wait_until("ten")
            self.play(*appear(oc.part10), run_time=min(1.0, c.until("graph")))  # early: lands on "ten"
            c.wait_until("graph")
            self.play(*appear(oc.caption), run_time=1.0)
            c.wait_until("tangle")
            self.play(*appear(oc.tangle, shift=None), run_time=min(1.5, c.until("the people")))
        # end card: hold exactly ch9 s1's open_card(); ch9 s1 opens on it (no fade)
