"""Chapter 9, scene 9: recap, then part ten's three exercise cards. Clips c9.recap.1 – c9.recap.2.

Clip 1: page one of the recap grid, r1 (s2's IN / JOIN cards) as a tall left column, r2 (ON = WHERE),
r3 (LEFT JOIN padded row) and r4 (NOT IN vs NOT EXISTS) stacked on the right; each appears on its
sentence with its short caption under it, the one before dims to 0.4. Clip 2: page one sweeps away;
r5 (DISTINCT) and r6 (index) on the top row, s7's 3 x 10 grid with s8's marks on the bottom row; the grid
splits into its two lists on "build each list". On {next} the page dims, clears, and next_card() builds:
header, then cards 17, 18, 19 on their phrases. The last frame is exactly next_card(), held ~8 s, no fade.

EXPORTS (static, no updaters; `load_scene("ch9_s9_recap").<name>()`):
- next_card(): ch9's end card = proposed ch10 opening frame. `.header` T 40 "Part 10 · Solutions: modelling
  and JSON queries" centred (0, 3.05); `.cards[17..19]` three DIM rounded cards (stroke 2, corner 0.2) in ch9 s1's
  row_card look, all CARD_H = 5.3 tall, centred y = -0.45, gap 0.15, the row 12.98 wide centred x = 0 (17: 3.54 wide
  at x -4.72; 18: 4.69 at x -0.46; 19: 4.45 at x 4.26); each `.box` `.head`
  (T 32 YELLOW "Exercise n") `.title` (T 30, two lines) `.lines` (17/18: five DIM T 28 numbered lines) or
  `.subs` (19: four sub-cards 19.1–19.4, each DIM box with `.num` T 30 DIM + `.sub` T 28 DIM in a row).
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

S2 = load_scene("ch9_s2_pairs")
S3 = load_scene("ch9_s3_left")
S4 = load_scene("ch9_s4_notin")
S5 = load_scene("ch9_s5_composers")
S6 = load_scene("ch9_s6_index")
S7 = load_scene("ch9_s7_build")
S8 = load_scene("ch9_s8_compare")
T8 = load_scene("ch8_s7_try")

# ---------------------------------------------------------------- end card
NEXT_HEADER = "Part 10 · Solutions: modelling and JSON queries"
TITLES = {17: ["Tables or", "documents?"], 18: ["What can a JSON", "Schema enforce?"],
          19: ["Four queries over", "the JSON database"]}
LINES = {17: ["1  blog", "2  bank", "3  event log", "4  shop catalogue", "5  app settings"],
         18: ["1  has a name", "2  deathyear ≥ birthyear", "3  unique person_id", "4  movie_ids exist",
              "5  titles match"]}
CARD_H, CARD_Y, CARD_GAP, HEADER_Y = 5.3, -0.45, 0.15, 3.05
SUB_W, SUB_H = 3.85, 0.62


def sub_card(i):
    num = T(f"19.{i}", 30, DIM)
    sub = T(T8.SUBJECT[i], 28, DIM)
    row = VGroup(num, sub).arrange(RIGHT, buff=0.3)
    box = RoundedRectangle(corner_radius=0.14, width=SUB_W, height=SUB_H).set_stroke(DIM, 2).set_fill(BG, 0)
    row.move_to(box).align_to(box, LEFT).shift(0.22 * RIGHT)
    g = VGroup(box, num, sub)
    g.box, g.num, g.sub = box, num, sub
    return g


def ex_card(n):
    head = T(f"Exercise {n}", 32, YELLOW)
    title = VGroup(*[T(t, 30) for t in TITLES[n]]).arrange(DOWN, buff=0.14)
    if n == 19:
        body = VGroup(*[sub_card(i) for i in range(1, 5)]).arrange(DOWN, buff=0.14)
    else:
        body = VGroup(*[T(s, 28, DIM) for s in LINES[n]]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
    inner = VGroup(head, title, body).arrange(DOWN, buff=0.3)
    box = RoundedRectangle(corner_radius=0.2, width=inner.width + 0.6, height=CARD_H)
    box.set_stroke(DIM, 2).set_fill(BG, 0)
    inner.move_to(box).align_to(box, UP).shift(0.35 * DOWN)
    g = VGroup(box, head, title, body)
    g.box, g.head, g.title = box, head, title
    g.lines = body if n != 19 else None
    g.subs = body if n == 19 else None
    return g


def next_card():
    header = T(NEXT_HEADER, 40).move_to([0, HEADER_Y, 0])
    cards = VGroup(*[ex_card(n) for n in (17, 18, 19)]).arrange(RIGHT, buff=CARD_GAP)
    cards.move_to([0, CARD_Y, 0])
    g = VGroup(header, cards)
    g.header = header
    g.cards = {17: cards[0], 18: cards[1], 19: cards[2]}
    g.row = cards
    return g


# ---------------------------------------------------------------- recap items
def item(vis, cap, w, h, t2c=None):
    vis.scale(min(w / vis.width, h / vis.height))
    lines = cap.split("\n")
    capt = VGroup(*[T(s, 30, t2c=t2c) for s in lines]).arrange(DOWN, buff=0.12)
    capt.next_to(vis, DOWN, buff=0.22)
    g = VGroup(vis, capt)
    g.vis, g.cap = vis, capt
    return g


def r4_fixed():
    """s4's recap_r4 with both labels under the taller NOT EXISTS card (the export's label overlaps its 3)."""
    r4 = S4.recap_r4()
    ni_l, ne_l = r4[3], r4[4]
    ne_l.next_to(r4[2], DOWN, buff=0.25)
    ni_l.set_y(ne_l.get_y())
    return r4


R7_SCALE = 0.46
R7_POS = np.array([-1.7, -1.55, 0])
MARKS_POS = np.array([4.45, -1.75, 0])


def page2_bottom():
    """s7's grid and its split r7, scaled identically; s8's marks to the right; caption under r7."""
    gr, r7 = S7.grid(), S7.recap_r7()
    off = R7_POS - r7.get_center() * R7_SCALE
    for m in (gr, r7):
        m.scale(R7_SCALE, about_point=ORIGIN).shift(off)
    cap = T("build each list on its own", 30).next_to(r7, DOWN, buff=0.22)
    marks = S8.recap_marks().scale(0.85).move_to(MARKS_POS)
    return gr, r7, cap, marks


class Ch9S9Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()

    def clip1(self):
        i1 = item(S2.recap_r1(), "a join repeats;\nIN asks once", 4.0, 4.6).move_to([-4.45, 0, 0])
        i2 = item(S2.recap_r2(), "inner join: ON = WHERE", 8.4, 1.35)
        i3 = item(S3.recap_r3(), "LEFT JOIN: ON matches, WHERE filters", 8.4, 0.85)
        i4 = item(r4_fixed(), "NOT IN breaks on NULLs", 7.0, 2.15, t2c={"NULLs": PINK})
        VGroup(i2, i3, i4).arrange(DOWN, buff=0.35).move_to([2.4, 0, 0])
        self.page1 = [i1, i2, i3, i4]
        with self.say("c9.recap.1", gap=1.5) as c:
            c.wait_until("r1")
            self.play(*appear(i1.vis, i1.cap, lag=0.3), run_time=min(1.5, c.until("r2")))
            prev = i1
            for cue, it in (("r2", i2), ("r3", i3), ("r4", i4)):
                c.wait_until(cue)
                self.play(*set_alpha([prev], 0.4), *appear(it.vis, it.cap, lag=0.3), run_time=1.5)
                prev = it

    def clip2(self):
        i5 = item(S5.recap_r5(), "DISTINCT: select the key", 5.2, 2.2).move_to([-3.85, 1.85, 0])
        i6 = item(S6.recap_r6(), "an index: redundancy the DBMS keeps", 6.6, 2.65).move_to([3.0, 1.8, 0])
        gr, r7, cap7, marks = page2_bottom()
        card = next_card()
        with self.say("c9.recap.2") as c:
            sweep_clear(self, *appear(i5.vis, i5.cap, lag=0.3), run_time=min(2.2, c.until("r6")))
            c.wait_until("r6")
            self.play(*set_alpha([i5], 0.4), *appear(i6.vis, i6.cap, lag=0.3), run_time=1.5)  # early: s6's callback shown whole
            c.wait_until("r7")
            self.play(*set_alpha([i6], 0.4), *appear(gr, marks, lag=0.4), run_time=1.5)
            c.wait_until("build each list")
            self.split(gr, r7, cap7)
            c.wait_until("document exercises")
            self.play(*set_alpha(list(self.mobjects), DIMMED), run_time=1.0)
            c.wait_until("which applications")
            sweep_clear(self, *appear(card.header, shift=None),  # early: the part's title card
                        *during(appear(card.cards[17], shift=0.5 * LEFT), 0.6, 1), run_time=2.0)
            for cue, n in (("what a json schema", 18), ("four queries", 19)):
                c.wait_until(cue)
                self.play(*appear(card.cards[n], shift=0.5 * LEFT), run_time=1.2)  # early: card shown as its exercise is named
        settle(self, card)
        self.wait(8.0)

    def split(self, gr, r7, cap7):
        anims = []
        for r in range(3):
            anims.append(ReplacementTransform(gr.cells[r][0], r7.genres[r][0]))
            anims.append(ReplacementTransform(gr.rows[r], r7.genres[r][1]))
        for c_ in range(10):
            src = gr.cells[0][c_] if c_ > 0 else gr.cells[0][0].copy()
            anims.append(ReplacementTransform(src, r7.actors[c_][0]))
            anims.append(ReplacementTransform(gr.heads[c_], r7.actors[c_][1]))
        rest = [gr.cells[r][c_] for r in (1, 2) for c_ in range(1, 10)]
        anims += during([FadeOut(m) for m in rest], 0, 0.45)
        anims += during(appear(r7.n3, r7.n10, cap7, lag=0.2), 0.55, 1)
        self.play(*anims, run_time=1.8)
        self.remove(*gr.get_family())
        settle(self, r7)
