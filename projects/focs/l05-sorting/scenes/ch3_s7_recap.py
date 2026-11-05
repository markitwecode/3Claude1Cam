"""Chapter 3, scene 7: Recap. Clips c3.recap.1 – c3.recap.3.

Plan
- c3.recap.1: {board} the scoreboard returns (insertion sort's row filled, as in s1); {count}
  quicksort's comparisons cell becomes GOLD "158,058"; {floor} the floor row flashes, a GOLD arrow
  rises from the floor line to the count with "× 1.33"; {secs} the time cell becomes "0.74 s".
- c3.recap.2: {recap} board clears, "Recap" (ch2 s7's layout: icon left, line right); r1 split_icon
  (s2), r2 hoare_row + copies_icon (s3), r3 part_icon (s5), r4 the pivot tree with its RED empty
  left branch (s6), each line in two beats on its words.
- c3.recap.3: {next} recap dims, title swaps to "Next: how good is quicksort?"; {fast} the recap
  clears, the tree icon grows into the card's tree, the small board (quicksort lit) fades in;
  "?" on "slow"; {quik} the DIM append code, struck through on "never appends". The final frame
  is ch4_s1_hook.open_card(), held ~8 s, then a fade.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402

ICON_W, ICON_H = 4.2, 1.35
ROW_Y = (2.22, 0.74, -0.92, -2.78)   # row centres
ROW_H = (1.2, 1.2, 1.6, 1.6)         # icon heights (the trace and the tree get more room)
TEXT_GAP = 0.45
TITLE_Y = 3.3
TSIZE = 34


def fit(m, w=ICON_W, h=ICON_H):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


def board():
    sb = make_scoreboard(bound="118,458")
    for col, val in enumerate(("25,146,194", "174 s")):
        sb.cells[0].submobjects[col] = T(val, 44, GOLD).move_to(sb.cells[0][col])
    return sb


def two_lines(a, b):
    g = VGroup(a, b).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    return g


class QuickRecap(NarratedScene):
    def construct(self):
        self.ch4 = load_scene("ch4_s1_hook")
        self.clip_board()
        self.build_recap()
        self.clip_recap()
        self.clip_next()
        self.wait(8.0)                       # the end card; music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c3.recap.1 ───────────────────────────────────────────────────────────────
    def clip_board(self):
        sb = board()
        count = T("158,058", 44, GOLD).move_to(sb.cells[1][0])
        secs = T("0.74 s", 44, GOLD).move_to(sb.cells[1][1])
        a = np.array([1.95, sb.floor_line.get_y() + 0.12, 0])
        b = np.array([1.2, count.get_bottom()[1] - 0.1, 0])
        up = Arrow(a, b, buff=0, stroke_width=3, color=GOLD, max_tip_length_to_length_ratio=0.12)
        ratio = T("× 1.33", 32, GOLD).next_to(up.get_center(), RIGHT, buff=0.3)
        floor = VGroup(sb.floor_label, sb.floor_value)

        with self.say("c3.recap.1") as c:
            self.play(FadeIn(sb, shift=0.2 * UP), run_time=1.2)  # early: the scoreboard returns whole
            c.wait_until("a hundred and fifty-eight")
            self.play(*swap(sb.cells[1][0], count), run_time=1.2)
            c.wait_until("floor")
            self.play(FlashAround(floor.copy(), color=GOLD, time_width=1.5), run_time=1.5)
            self.play(GrowArrow(up), *appear(ratio), run_time=1.2)
            c.wait_until("zero point seven four")
            self.play(*swap(sb.cells[1][1], secs), run_time=min(1.2, c.until()))

    # ── c3.recap.2 ───────────────────────────────────────────────────────────────
    def build_recap(self):
        self.title = T("Recap", 52).move_to(UP * TITLE_Y)

        ic1 = fit(load_scene("ch3_s2_idea").split_icon(), h=ROW_H[0])
        hoare = load_scene("ch3_s3_hoare")
        h_row = fit(hoare.hoare_row(), 2.7, ROW_H[1])
        copies = fit(hoare.copies_icon(), 1.2, 1.0)
        ic2 = VGroup(h_row, copies).arrange(RIGHT, buff=0.3)
        ic3 = fit(load_scene("ch3_s5_part").part_icon(), h=ROW_H[2])
        tree = self.ch4.pivot_tree().ct          # pivots YELLOW, root's empty left stub RED
        ic4 = fit(tree, h=ROW_H[3])

        l1 = T("choose, divide, conquer, combine", TSIZE)
        l2a = T("Hoare: in place", TSIZE, t2c={"in place": BLUE})
        l2b = T("·  ours: lists", TSIZE, t2c={"·": DIM, "lists": TEAL})
        l2 = VGroup(l2a, l2b).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
        l3a = T("part: one pass, two accumulators,", TSIZE, t2c={"part": YELLOW})
        l3b = T("n − 1 comparisons", TSIZE, t2c={"n − 1": GOLD})
        l3 = two_lines(l3a, l3b)
        l4a = T("our list: 8 comparisons,", TSIZE, t2c={"8": GOLD})
        l4b = T("a lopsided first split", TSIZE, t2c={"lopsided": RED})
        l4 = two_lines(l4a, l4b)

        icons = [ic1, ic2, ic3, ic4]
        texts = [l1, l2, l3, l4]
        x_text = ICON_W / 2 + TEXT_GAP
        for i, (icon, text) in enumerate(zip(icons, texts)):
            y = ROW_Y[i]
            icon.move_to([0, y, 0])
            text.move_to([0, y, 0])
            text.shift((x_text - text.get_left()[0]) * RIGHT)
        block = VGroup(*icons, *texts)
        block.shift(-block.get_center()[0] * RIGHT)

        self.ic1, self.h_row, self.copies, self.ic3, self.tree = ic1, h_row, copies, ic3, tree
        self.l1, self.l2a, self.l2b, self.l3a, self.l3b, self.l4a, self.l4b = l1, l2a, l2b, l3a, l3b, l4a, l4b

    def clip_recap(self):
        ic1, tree = self.ic1, self.tree
        top, row, le, gt, al, ar = ic1
        ic3 = self.ic3
        lines, lr = ic3

        with self.say("c3.recap.2") as c:
            sweep_clear(self, time_span(FadeIn(self.title, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)

            c.wait_until("r1")
            self.play(FadeIn(top), *appear(self.l1), run_time=1.2)
            c.wait_until("divides")
            self.play(GrowArrow(al), GrowArrow(ar), *appear(row, le, gt, lag=0.2), run_time=1.5)
            c.wait_until("combines")
            self.play(FlashAround(self.l1.copy(), color=YELLOW, time_width=1.5),
                      run_time=min(1.4, c.until("r2")))

            c.wait_until("r2")
            self.play(*appear(self.h_row, self.l2a, lag=0.3), run_time=1.4)  # early: the line, read with its icon
            c.wait_until("Ours copies")
            self.play(*appear(self.copies, self.l2b, lag=0.3), run_time=1.4)

            c.wait_until("r3")
            self.play(*appear(*lines, lag=0.15), *appear(self.l3a), run_time=1.6)
            c.wait_until("so dividing")
            self.play(*appear(lr, shift=None), run_time=1.0)
            c.wait_until("N minus one")
            self.play(*appear(self.l3b), run_time=1.0)  # early: "n − 1" is its word

            c.wait_until("r4")
            self.play(FadeIn(tree), *appear(self.l4a), run_time=1.4)
            c.wait_until("lopsided")
            self.play(*appear(self.l4b),
                      VShowPassingFlash(tree.root.stubs["left"].copy().set_stroke(RED, 9), time_width=0.8),
                      run_time=min(1.4, c.until()))

    # ── c3.recap.3: next time (the end card) ─────────────────────────────────────
    def clip_next(self):
        card = self.ch4.open_card()
        tree = self.tree
        rows = [m for m in self.mobjects if m is not self.title]

        with self.say("c3.recap.3") as c:
            self.play(*set_alpha(rows, DIMMED), *swap(self.title, card.title), run_time=1.4)
            c.wait_until("fast")
            sweep_clear(self, time_span(ReplacementTransform(tree, card.tree.ct), 0.5, 1.25),
                        time_span(FadeIn(card.sb), 1.15, 1.8),
                        keep=[card.title, tree], run_time=1.8)
            c.wait_until("slow")
            self.play(*appear(card.tree.q),
                      VShowPassingFlash(card.tree.left_edge.copy().set_stroke(RED, 10), time_width=0.8), run_time=1.2)
            c.wait_until("quik")
            self.play(*appear(card.code.code), run_time=1.0)
            c.wait_until("never appends")
            self.play(Create(card.code.strike), run_time=min(1.0, c.until()))
