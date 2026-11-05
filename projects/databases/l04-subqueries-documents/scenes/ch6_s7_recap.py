"""Chapter 6, scene 7: exercises 17 and 18, then the chapter recap. Clips c6.try.1 – c6.recap.2.

Exports (static): exercise_card(17), exercise_card(18), hint_chip() ("one document at a time").
"""
# style: 2
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

H1 = load_scene("ch6_s1_hook")
S2 = load_scene("ch6_s2_tree")
S3 = load_scene("ch6_s3_graph")
S4 = load_scene("ch6_s4_schema")
S5 = load_scene("ch6_s5_tradeoff")
S6 = load_scene("ch6_s6_jsonschema")
N7 = load_scene("ch7_s1_hook")

EX = {
    17: ["Exercise 17. For each of the following applications, would you store the data in a relational "
         "schema or as documents? Justify your answers, and if you choose documents, say what each "
         "document would contain.",
         "1. A blogging platform, where each post has a title, a body text, some tags, and comments from readers.",
         "2. A bank, which stores customers, their accounts, and the transfers between accounts.",
         "3. An event log, which stores every time various functions were invoked, and what arguments "
         "were passed to the function invocation.",
         "4. An online shop's product catalogue, in which different types of product have different attributes.",
         "5. A system for storing the settings of a mobile app, such as the user's preferred language, "
         "notification preferences, and so on."],
    18: ["Exercise 18. Which of the following properties of the people documents in the example database "
         "can be enforced by a JSON Schema, and which cannot? Explain why.",
         "1. Every person has a name.",
         "2. A person's deathyear, if present, is not earlier than their birthyear.",
         "3. No two documents have the same person_id.",
         "4. Every movie_id in a person's acted_in array is the ID of a movie document.",
         "5. The title in each element of acted_in is the same as the title in the corresponding movie document."],
}
WRAP = 84


def exercise_card(n, size=28, max_w=12.8, max_h=None):
    """ch3 s8's ex_card look: DIM rounded box, YELLOW 'Exercise N.', paragraphs wrapped."""
    max_h = max_h or (5.3 if n == 17 else 4.5)
    head = f"Exercise {n}."
    paras = []
    for i, s in enumerate(EX[n]):
        lines = textwrap.wrap(s, WRAP if i == 0 else WRAP - 3)
        if i > 0:
            lines = [lines[0]] + ["    " + ln for ln in lines[1:]]
        paras.append(T("\n".join(lines), size, t2c={head: YELLOW} if i == 0 else None, line_spacing=0.9))
    text = VGroup(*paras).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.2, width=text.width + 0.8, height=text.height + 0.7)
    box.set_stroke(DIM, 2).set_fill(BG, 0)
    text.move_to(box)
    g = VGroup(box, text)
    g.box, g.text = box, text
    g.scale(min(1.0, max_w / g.width, max_h / g.height))
    return g


def chip(text, icons=(), color=YELLOW, size=28, icon_h=0.6):
    lab = T(text, size, color)
    parts = []
    if icons:
        ic = VGroup(*icons).arrange(RIGHT, buff=0.15)
        ic.scale_to_fit_height(icon_h)
        parts.append(ic)
    parts.append(lab)
    inner = VGroup(*parts).arrange(RIGHT, buff=0.25)
    box = RoundedRectangle(corner_radius=0.15, width=inner.width + 0.5, height=inner.height + 0.35)
    box.set_stroke(color, 2).set_fill(color, 0.08)
    inner.move_to(box)
    g = VGroup(box, inner)
    g.box, g.label = box, lab
    return g


def hint_chip():
    return chip("one document at a time")


def magnifier(r=0.32, color=YELLOW):
    ring = Circle(radius=r).set_stroke(color, 4)
    handle = Line(ring.point_at_angle(-PI / 4), ring.point_at_angle(-PI / 4) + 0.35 * (RIGHT + DOWN))
    handle.set_stroke(color, 6)
    return VGroup(ring, handle)


def hint18_icon():
    """s6's validator handed a single document, a magnifier over one value."""
    v = S6.validator()
    d = S6.doc(S6.CHAPLIN, size=22)
    d.next_to(v, UP, buff=0.25)
    arr = Arrow(d.get_bottom(), v.get_top(), buff=0.04, stroke_width=3, color=TEAL)
    mag = magnifier().move_to(d.get_right() + 0.55 * LEFT + 0.08 * DOWN)
    return VGroup(d, arr, v, mag)


THUMB_W, THUMB_H = 4.2, 2.0
COL_X = [[-4.5, 0.0, 4.5], [-2.25, 2.25]]
ROW_TOP = [2.75, -0.5]
LABELS = [
    "one owner: a tree,\nso nest it",
    "many-to-many: a graph,\nso copies or joins",
    "schema-on-write,\nschema-on-read",
    "flexible, and\nsilent about typos",
    "JSON Schema writes\nthe shape down",
]
SLOTS = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]


def thumbs():
    out = []
    for i, f in enumerate([S2, S3, S4, S5, S6]):
        r, k = SLOTS[i]
        t = f.recap_thumb()
        t.scale(min(THUMB_W / t.width, THUMB_H / t.height))
        t.move_to([COL_X[r][k], ROW_TOP[r] - THUMB_H / 2, 0])
        out.append(t)
    return out


def labels():
    out = []
    for i, s in enumerate(LABELS):
        r, k = SLOTS[i]
        lab = T(s, 30, line_spacing=0.9)
        lab.move_to([COL_X[r][k], ROW_TOP[r] - THUMB_H - 0.2 - lab.height / 2, 0])
        out.append(lab)
    return out


class Recap(NarratedScene):
    def construct(self):
        self.try17()
        self.try18()
        self.recap()
        self.next()

    # ------------------------------------------------------------ c6.try.1
    def try17(self):
        with self.say("c6.try.1", gap=1.5) as c:
            card = exercise_card(17)
            card.move_to([0, 3.6 - card.height / 2, 0])
            self.play(FadeIn(card), run_time=1.2)  # early: the exercise card, read whole
            c.wait_until("hint17")
            y = card.get_bottom()[1] - 0.6
            c1 = chip("tree or tangle?", [S2.tree_closed(), S3.tangle()])
            c2 = chip("what is updated,\nand how often?", [H1.two_way_copies()])
            c3 = chip("one structure\nor many?", [S5.products_docs()])
            row = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.4)
            row.scale(min(1.0, 12.8 / row.width))
            row.move_to([0, (card.get_bottom()[1] - 3.5) / 2, 0])
            c.wait_until(own_word=c1.label)
            self.play(*appear(c1), run_time=min(1.0, c.until("updates")))
            c.wait_until("updates")
            self.play(*appear(c2), run_time=min(1.0, c.until("shared")))
            c.wait_until("shared")
            self.play(*appear(c3), run_time=min(1.0, c.until()))  # early: chip lands on its cue, "share one structure"
            self.ex17 = [card, c1, c2, c3]

    # ------------------------------------------------------------ c6.try.2
    def try18(self):
        with self.say("c6.try.2", gap=2.5) as c:
            card = exercise_card(18)
            card.move_to([0, 3.6 - card.height / 2, 0])
            sweep_clear(self, time_span(FadeIn(card), 0.6, 1.3), run_time=1.3)  # early: the exercise card, read whole
            c.wait_until("hint18")
            icon = hint18_icon()
            room = card.get_bottom()[1] - 0.3 + 3.2
            icon.scale(room / icon.height)
            icon.move_to([-3.4, card.get_bottom()[1] - 0.3 - icon.height / 2, 0])
            hc = hint_chip().move_to([2.4, icon.get_top()[1] - 0.45, 0])
            self.play(*appear(icon), run_time=min(1.2, c.until("a validator")))
            c.wait_until(own_word=hc.label, cue="a validator")
            self.play(*appear(hc), run_time=min(1.0, c.until("and each keyword")))
            c.wait_until("ask")
            ask = T("what must it look at?", 34, YELLOW).next_to(hc, DOWN, buff=0.45)
            self.play(*appear(ask), run_time=min(1.0, c.until("answers")))  # early: the question lands on {ask}
            c.wait_until("answers")
            ans = T("worked answers: part 10", 30, DIM).next_to(ask, DOWN, buff=0.4)
            self.play(*appear(ans), run_time=min(1.0, c.until()))

    # ------------------------------------------------------------ c6.recap.1
    def recap(self):
        with self.say("c6.recap.1") as c:
            title = T("Recap", 44).move_to([0, 3.25, 0])
            sweep_clear(self, time_span(FadeIn(title), 0.6, 1.2), run_time=min(1.2, c.until("r1")))
            ts, ls = thumbs(), labels()
            cues = ["r1", "r2", "r3", "r4", "r5"]
            for i in range(5):
                c.wait_until(cues[i])
                nxt = cues[i + 1] if i < 4 else None
                if i != 3:
                    c.wait_until(own_word=ls[i], cue=cues[i])
                self.play(*appear(ts[i], ls[i], lag=0.3, shift=None), run_time=min(1.4, 0.6 * c.until(nxt)))  # early: each recap line lands on its {r} cue

    # ------------------------------------------------------------ c6.recap.2
    def next(self):
        with self.say("c6.recap.2", gap=8.0) as c:
            card = N7.open_card()
            sweep_clear(self, time_span(FadeIn(card), 0.7, 1.6), run_time=1.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
