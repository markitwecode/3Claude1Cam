"""Chapter 4, scene 7: recap, then the end card (ch5's opening card). Clips c4.recap.1 – c4.recap.2.

Plan
- c4.recap.1: "Recap" (T 52, y 3.3) and five rows in ch2 s7's layout (icon left, T 32 line right):
  r1 s2's recursion tree in miniature (sums "n", GOLD bracket log₂ n); r2 s3's `worst_tree()` circles
  zigzag; r3 s3's shuffled chain with GREEN "158,058"; r4 s5's `answer_row()` built from the right;
  r5 the scoreboard's quicksort row "158,058" / "0.53 s".
- c4.recap.2: title swaps to "Next: merge sort", the rows sweep out, the board comes in; merge sort's
  "?" cells pulse; L4's take/drop shot builds under it. Ends static on exactly
  `load_scene("ch5_s1_hook").open_card()` for ~8 s, then fades.
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

ICON_W, ICON_H = 3.7, 1.12
ROW_Y0, ROW_PITCH = 2.25, 1.28
TEXT_GAP = 0.5
TITLE_Y = 3.3
LINE = 30


def fit(m, w=ICON_W, h=ICON_H):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


def colour(text, sub, col, nth=0):
    select(text, sub)[nth].set_color(col)


# ── recap icons ─────────────────────────────────────────────────────────────────
def tree_icon():
    rt = load_scene("ch4_s2_average").recursion_tree(
        sums=("n", "n", "n"), width=5.6, leaves=8, pitch=0.6, box_h=0.5,
        with_sums=True, with_bracket=True)
    fit(rt)
    return rt


def worst_icon():
    wt = load_scene("ch4_s3_worst").worst_tree(form="circles", size=36, radius=0.45,
                                                pitch=1.3, gap=0.7, badges=False)
    wt.place(1.0, ORIGIN)
    fit(wt)
    return wt


def shuffled_icon():
    sc = load_scene("ch4_s3_worst").shuffled_chain()
    chain = sc.chain
    num = T("158,058", 48, GREEN).next_to(chain, DOWN, buff=0.3)
    g = VGroup(chain, num)
    fit(g)
    g.chain, g.num = chain, num
    return g


def answer_icon():
    ar = load_scene("ch4_s5_order").answer_row()
    fit(ar)
    return ar


def board_row_icon():
    lab = T("quicksort", 36, YELLOW)
    comps = T("158,058", 44, GOLD)
    secs = T("0.53 s", 44, GOLD)
    g = VGroup(lab, comps, secs).arrange(RIGHT, buff=0.7)
    comps.align_to(lab, DOWN)
    secs.align_to(lab, DOWN)
    fit(g)
    g.lab, g.comps, g.secs = lab, comps, secs
    return g


class Recap(NarratedScene):
    def construct(self):
        self.build_recap()
        self.recap()
        self.end_card()
        self.wait(7.3)                       # the end card; music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def build_recap(self):
        self.title = T("Recap", 52).move_to(UP * TITLE_Y)
        self.icons = [tree_icon(), worst_icon(), shuffled_icon(), answer_icon(), board_row_icon()]

        l1 = T("random pivots: log₂ n levels of n, O(n log n)", LINE)
        colour(l1, "log₂ n", GOLD)
        colour(l1, "O(n log n)", GREEN)
        l2 = T("sorted or reversed: every split lopsided, O(n²)", LINE)
        colour(l2, "lopsided", RED)
        colour(l2, "O(n²)", RED)
        l3 = T("randomise: worst case unlikely", LINE)
        colour(l3, "randomise", YELLOW)
        colour(l3, "unlikely", GREEN)
        l4 = T("quik: an accumulator, no @", LINE)
        colour(l4, "quik", YELLOW)
        colour(l4, "@", GOLD)
        l5 = T("same comparisons, less copying", LINE)
        colour(l5, "less copying", GREEN)
        self.lines = [l1, l2, l3, l4, l5]

        x_text = ICON_W / 2 + TEXT_GAP
        for i, (icon, text) in enumerate(zip(self.icons, self.lines)):
            y = ROW_Y0 - i * ROW_PITCH
            icon.move_to([0, y, 0])
            text.move_to([0, y, 0])
            text.shift((x_text - text.get_left()[0]) * RIGHT)
        block = VGroup(*self.icons, *self.lines)
        block.shift(-block.get_center()[0] * RIGHT)

    # ── c4.recap.1 ──────────────────────────────────────────────────────────────
    def recap(self):
        ic1, ic2, ic3, ic4, ic5 = self.icons
        l1, l2, l3, l4, l5 = self.lines
        l1a = select(l1, "random pivots:")[0]
        l1b = select(l1, "log₂ n levels of n,")[0]
        l1c = select(l1, "O(n log n)")[0]
        l2a = select(l2, "sorted or reversed: every split lopsided,")[0]
        l2b = select(l2, "O(n²)")[0]

        with self.say("c4.recap.1", gap=1.2) as c:
            self.play(*appear(self.title), run_time=1.0)  # early: the recap title
            c.wait_until("r1")
            self.play(*[FadeIn(r, shift=0.1 * DOWN) for r in ic1.rows], FadeIn(ic1.dots),
                      time_span(FadeIn(l1a, shift=0.2 * DOWN), 0.5, 1.5), run_time=1.5)
            c.wait_until("log base")
            self.play(GrowFromCenter(ic1.bracket.brace), FadeIn(ic1.bracket.label),
                      time_span(FadeIn(l1b, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("comparisons")
            self.play(*[FadeIn(s) for s in ic1.sums], run_time=1.0)
            c.wait_until("Big O")
            self.play(*appear(l1c), run_time=1.0)

            c.wait_until("r2")
            self.play(FadeIn(ic2, shift=0.1 * DOWN),
                      time_span(FadeIn(l2a, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("quadratic")
            self.play(*appear(l2b), run_time=1.0)

            c.wait_until("r3")
            self.play(FadeIn(ic3.chain, shift=0.1 * DOWN),
                      time_span(FadeIn(l3, shift=0.2 * DOWN), 0.3, 1.2), run_time=1.2)
            c.wait_until("highly")
            self.play(*appear(ic3.num), run_time=0.9)

            c.wait_until("r4")
            self.play(*appear(l4), run_time=1.0)
            c.wait_until("builds its answer")
            parts = [ic4.nil, *reversed(ic4.order)]
            self.play(LaggedStart(*[FadeIn(p, shift=0.15 * LEFT) for p in parts], lag_ratio=0.3),
                      time_span(GrowArrow(ic4.arrow), 0.6, 2.0), run_time=2.0)

            c.wait_until("r5")
            self.play(*appear(l5), run_time=1.0)
            c.wait_until("same comparisons")
            self.play(*appear(ic5.lab, ic5.comps, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("zero point five three")
            self.play(*appear(ic5.secs), run_time=1.0)
            self.play(FlashAround(ic5.secs, color=GOLD, time_width=1.5), run_time=min(1.4, c.until()))

    # ── c4.recap.2: next time, merge sort (the end card = ch5's opening card) ──────────
    def end_card(self):
        card = load_scene("ch5_s1_hook").open_card()
        nxt, sb, run, cut, L, R = card.nxt, card.board, card.run, card.cut, card.L, card.R

        with self.say("c4.recap.2", gap=0.2) as c:
            self.play(*swap(self.title, nxt), run_time=1.0)
            sweep_clear(self, time_span(FadeIn(sb), 0.6, 1.2), keep=[nxt], run_time=1.2)
            c.wait_until("never")
            pulse = (lambda t: there_and_back((2 * t) % 1.0))
            self.play(*[q.animate(rate_func=pulse).scale(1.4) for q in sb.cells[2]],
                      *flash(list(sb.cells[2]), GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("splits its list")
            self.play(FadeIn(run, shift=0.15 * UP), run_time=1.0)
            c.wait_until("counting")
            self.play(FadeIn(cut), run_time=0.8)
            c.wait_until("never lopsided")
            src_l = VGroup(*run.cells[:2])
            src_r = VGroup(*run.cells[2:])
            self.play(*fly(src_l, L), *fly(src_r, R), run_time=min(1.5, c.until(floor=0.8)))
