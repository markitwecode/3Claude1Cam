"""Chapter 9, scene 1: spoiler warning, then the four exercises this part solves. Clips c9.intro.1 – c9.intro.2.

Opens on open_card() (ch8 s8's last frame, a reversed join: ch8 s8 ends on exactly this picture), holds it
~0.7 s, clears to the title card on {title}. Ends on an empty frame.

EXPORTS (static, no updaters; `load_scene("ch9_s1_intro").<name>()`):
- open_card(): ch9's first frame. `.part9` `.part10` small title cards (each `.head` T 48 "Part 9"/"Part 10",
  `.rule` DIM line 3.6 wide stroke 2, `.sub` T 32 two lines), centred at (-3.9, 1.55) / (-3.9, -1.75);
  `.tangle` ch6 s3's tangle() scaled 0.7, centred at (3.4, 0.35); `.caption` T 30 DIM
  "Lecture 5 · Graph databases", centred x 3.4, 0.45 under the tangle.
- spoiler_banner(): GOLD "SPOILERS AHEAD" (T 72 bold) in a GOLD rounded box (stroke 4, fill 0.08),
  centred at (0, 1.1). `.box .text`. (ch10 s1 reuses it.)
- pause_icon(height=1.6): two GOLD rounded bars ‖ at ORIGIN (bar 0.22·h wide, gap 0.26·h).
- ex_row(): the four try-these cards at their {cards} place, row centred y = 1.5, 4.1 tall, widths 3.55 (13) and 3.05,
  x = -4.8, -1.35, 1.825, 5.0 (gap 0.15). `.cards[13..16]`, each `.box` (DIM rounded rect, stroke 2) `.head`
  (T 32 YELLOW "Exercise n") `.title` (T 30, two lines) `.lines` (13 only: four DIM numbered lines T 28).
- big_card(n), n = 13..16: the enlarged card in ch3 s8's ex_card() look (notes' text for 13/14, script
  ch5 s7's for 15/16), max 12.6 wide; card + hint centred at (0, 0.55) (13 sits with its top at 3.5);
  members `.box .text`; `.hint` its hint(s) DIM T 30, 0.4 under it (not a member); `.pause` pause_icon(1.0) at (0, -3.0) (not a member).
  Suggested opening: self.add(row) then ReplacementTransform(row.cards[n].box.copy(), big.box) with
  appear(big.text) in the second half (text never morphs), then appear(big.hint, big.pause), hold.
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
from lib.titles import title_card  # noqa: E402

R8 = load_scene("ch3_s8_recap")
G6 = load_scene("ch6_s3_graph")

EX15 = ["Exercise 15. An index is a form of redundancy too.",
        "How is it similar to denormalisation, and how",
        "is it different?"]
EX16 = ["Exercise 16. One query over the relational tables →",
        "one JSON document per movie: ID, title, year,",
        "genres (array of strings), actors (array of",
        "{person_id, name}). How does your output differ",
        "from the JSON database?"]
EX_TEXT = {13: R8.EX13, 14: R8.EX14, 15: EX15, 16: EX16}
HINTS = {13: ["One row of r matching two rows of s? ON or WHERE?",
              "Annie Hall and the left join. A null in either y column?"],
         14: ["What does DISTINCT compare?"],
         15: ["Who keeps the copies consistent?",
              "What happens on reads? On writes?",
              "Does it change how queries are written, or what they return?"],
         16: ["Choose your actors' table with care."]}
SHORT_HINT = {13: "One row matching two?", 14: "What does DISTINCT compare?",
              15: "Who keeps the copies consistent?", 16: "Choose your actors' table with care."}
TITLES = {13: ["Four pairs", "of queries"], 14: ["Composers", "with a join"],
          15: ["An index is", "redundancy too"], 16: ["Documents", "from tables"]}
LINES13 = ["1  IN or JOIN", "2  ON or WHERE", "3  LEFT JOIN", "4  NOT IN"]
ROW_X = (-4.8, -1.35, 1.825, 5.0)
CARD_W = {13: 3.55, 14: 3.05, 15: 3.05, 16: 3.05}
ROW_Y, CARD_H = 1.5, 4.1


# ---------------------------------------------------------------- exports
def _mini_title(n, sub):
    head = T(f"Part {n}", 48)
    rule = Line(LEFT * 1.8, RIGHT * 1.8).set_stroke(DIM, 2)
    s = T(sub, 32, line_spacing=0.9)
    g = VGroup(head, rule, s).arrange(DOWN, buff=0.25)
    g.head, g.rule, g.sub = head, rule, s
    return g


def open_card():
    p9 = _mini_title(9, "Solutions: subqueries\nand redundancy").move_to([-3.9, 1.55, 0])
    p10 = _mini_title(10, "Solutions: modelling\nand JSON queries").move_to([-3.9, -1.75, 0])
    tg = G6.tangle().scale(0.7).move_to([3.4, 0.35, 0])
    cap = T("Lecture 5 · Graph databases", 30, DIM).next_to(tg, DOWN, buff=0.45)
    g = VGroup(p9, p10, tg, cap)
    g.part9, g.part10, g.tangle, g.caption = p9, p10, tg, cap
    return g


def spoiler_banner():
    text = T("SPOILERS AHEAD", 72, GOLD, weight=BOLD)
    box = RoundedRectangle(corner_radius=0.25, width=text.width + 1.2, height=text.height + 0.9)
    box.set_stroke(GOLD, 4).set_fill(GOLD, 0.08)
    g = VGroup(box, text).move_to([0, 1.1, 0])
    text.move_to(box)
    g.box, g.text = box, text
    return g


def pause_icon(height=1.6):
    w = 0.22 * height
    bars = [RoundedRectangle(corner_radius=w * 0.3, width=w, height=height).set_stroke(GOLD, 0).set_fill(GOLD, 1)
            for _ in range(2)]
    bars[0].move_to(LEFT * (0.13 * height + w / 2))
    bars[1].move_to(RIGHT * (0.13 * height + w / 2))
    return VGroup(*bars)


def row_card(n, x):
    box = RoundedRectangle(corner_radius=0.2, width=CARD_W[n], height=CARD_H).set_stroke(DIM, 2).set_fill(BG, 0)
    box.move_to([x, ROW_Y, 0])
    head = T(f"Exercise {n}", 32, YELLOW)
    title = VGroup(*[T(t, 30) for t in TITLES[n]]).arrange(DOWN, buff=0.14)
    parts = [head, title]
    lines = None
    if n == 13:
        lines = VGroup(*[T(s, 28, DIM) for s in LINES13]).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        parts.append(lines)
    body = VGroup(*parts).arrange(DOWN, buff=0.3)
    body.move_to(box).align_to(box, UP).shift(0.35 * DOWN)
    g = VGroup(box, *parts)
    g.box, g.head, g.title, g.lines = box, head, title, lines
    return g


def ex_row():
    row = VGroup()
    row.cards = {}
    for n, x in zip((13, 14, 15, 16), ROW_X):
        row.cards[n] = row_card(n, x)
        row.add(row.cards[n])
    return row


def big_card(n):
    size = 34 if n == 13 else 30
    card = R8.ex_card(EX_TEXT[n], size=size)
    if card.width > 12.6:
        card.scale(12.6 / card.width)
    card.move_to([0, 3.5 - card.height / 2, 0])
    hint = VGroup(*[T(s, 30, DIM) for s in HINTS[n]]).arrange(DOWN, buff=0.18)
    hint.next_to(card, DOWN, buff=0.4)
    both = VGroup(card, hint)
    both.move_to([0, 0.55, 0])
    if card.get_top()[1] > 3.5:
        both.shift((3.5 - card.get_top()[1]) * UP)
    card.hint = hint
    card.pause = pause_icon(1.0).move_to([0, -3.0, 0])
    return card


def result_card(x, y):
    box = Rectangle(width=1.7, height=1.6).set_stroke(FG, 2.5).set_fill(BG, 0)
    box.move_to([x, y, 0])
    head = Mono("x", 28).move_to([x, box.get_top()[1] - 0.27, 0])
    div = Line(box.get_left() + DOWN * 0, box.get_right()).set_stroke(FG, 1.5)
    div.move_to([x, box.get_top()[1] - 0.54, 0])
    return VGroup(box, head, div)


# ---------------------------------------------------------------- scene
class Ch9S1Intro(NarratedScene):
    def construct(self):
        self.oc = open_card()
        self.add(self.oc)
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def clip1(self):
        with self.say("c9.intro.1") as c:
            self.wait(0.7)
            tc = title_card("Part 9 · Solutions: subqueries and redundancy")
            if tc.title.width > 12:
                tc.title.scale_to_fit_width(12)
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.4),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.4), run_time=1.4)  # early: title card
            self.play(*appear(tc.course, tc.part, lag=0.4), run_time=1.0)  # early: title card
            c.wait_until("lasttime")

            # two DIM callbacks slide past: Part 3's exercises, then Part 5's
            cols = []
            for label, ns, x in (("Part 3", (13, 14), -3.55), ("Part 5", (15, 16), 3.55)):
                head = T(label, 36, FG)
                items = []
                for n in ns:
                    m = R8.mini_card(f"Exercise {n}")
                    h = T(SHORT_HINT[n], 28, DIM)
                    items.append(VGroup(m, h).arrange(DOWN, buff=0.22))
                col = VGroup(head, *items).arrange(DOWN, buff=0.6)
                col.move_to([x, 0, 0])
                for it in items:
                    it[0].box.set_stroke(DIM, 2, opacity=0.8)
                    it[0].label.set_color(DIM)
                    it[0].scale(1.25)
                cols.append(col)
            sweep_clear(self, time_span(FadeIn(cols[0], shift=1.2 * LEFT), 0.5, 1.6), run_time=1.6)  # early: a callback picture
            c.wait_until("five")
            self.play(FadeIn(cols[1], shift=1.2 * LEFT), run_time=min(1.4, c.until("this part")))  # early: a callback picture
            c.wait_until("warn")

            banner = spoiler_banner()
            sweep_clear(self, time_span(FadeIn(banner, scale=0.9), 0.6, 1.4), run_time=1.4)  # early: the banner
            pause = pause_icon(1.6).move_to([0, -1.6, 0])
            c.wait_until("pause now")
            self.play(FadeIn(pause, scale=0.8), run_time=min(1.0, c.until()))
            self.banner, self.pause = banner, pause

    def clip2(self):
        with self.say("c9.intro.2", gap=0.6) as c:
            row = ex_row()
            cards = row.cards
            for n in (14, 15, 16):
                cards[n].box.set_stroke(opacity=0.3)
                for part in cards[n][1:]:
                    part.set_opacity(0.3)
            sweep_clear(self, time_span(FadeIn(row), 0.5, 1.4), run_time=1.4)  # early: the four cards shown whole, then lit one by one
            for n, cue in ((14, "c14"), (15, "c15"), (16, "c16")):
                c.wait_until(cue)
                self.play(*set_alpha([cards[n]], 1), run_time=1.0)  # early: each card brightens on its number, its title read just after
            c.wait_until("ritual")

            # the ritual: empty r and s, two results, ≠?, DuckDB
            r = R8.table("r", -4.95, -1.0, scale=1.1)
            s = R8.table("s", -1.55, -1.0, scale=1.1)
            res1 = result_card(1.95, -1.8)
            res2 = result_card(5.05, -1.8)
            neq = T("≠?", 48, GOLD).move_to([3.5, -1.8, 0])
            arr = Arrow([0.45, -1.8, 0], [1.0, -1.8, 0], buff=0, stroke_width=4).set_color(DIM)
            tag = T("DuckDB v1.5.6", 30, DIM).move_to([3.5, -3.35, 0])
            self.play(*set_alpha([cards[14], cards[15], cards[16]], 0.4),
                      *appear(r, s, lag=0.3), run_time=min(1.5, c.until("tiny database")))
            c.wait_until("tells them apart")
            self.play(GrowArrow(arr), *appear(res1, res2, lag=0.3), run_time=min(1.5, c.until("run both")))
            self.play(*appear(neq), run_time=min(1.0, c.until("run both")))
            c.wait_until("duck d b")
            self.play(*appear(tag), run_time=min(1.0, c.until()))
        self.wait(2.5)
