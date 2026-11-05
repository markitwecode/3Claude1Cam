"""Chapter 5, scene 7: bottom-up merge sort, runs, and the recap. Clips c5.bottom.1 – c5.bottom.4.

Plan
- c5.bottom.1: {top} s5's split tree in miniature, BLUE down arrow "split" left, YELLOW up arrow
  "merge" right, caption "top-down". {bottom} caption swaps to "bottom-up", the running chain;
  it falls apart into five one-cell lists; {pass1}..{pass3} each pass's lists are born on the
  row below (cells fly down in merged order), the row above dims; GREEN tick on the last.
- c5.bottom.2: {runs} the chain whole; {split} GOLD braces "increasing" over 3 5 9 and 4 7;
  the two runs pull apart into s2's Zipper rows, {once} one merge; {sortedrun} the sorted
  output centred with one GOLD brace "one run, nothing to merge".
- c5.bottom.3: recap in ch4 s7's five-row layout (ch2 s7's look): s2 zipper closing, s3's boxed
  bound + lopsided 5 over 1 2 3 4, s4's split_shot(), s6's level_tree(), merge sort's board row.
- c5.bottom.4: title swaps to ch6's card title, rows sweep out, board in; {nocompare} DIM
  buckets, 53/19/51 drop in, GOLD tag. Ends static on `load_scene("ch6_s1_hook").open_card()`
  held ~8 s, no fade (ch6 s1 opens on it).
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

S2 = load_scene("ch5_s2_merge")
S4 = load_scene("ch5_s4_code")
S5 = load_scene("ch5_s5_trace")
S6 = load_scene("ch5_s6_safe")
S6CH = load_scene("ch6_s1_hook")

RUN = (3, 5, 9, 4, 7)
CAP_Y = 3.3

# clip 1: the split tree miniature
TREE_S, TREE_SY, TREE_DY = 0.62, 0.95, -0.7
ARROW_X = 4.6
# clip 1: bottom-up passes
PS = 0.55
PASS_Y = [1.9, 0.55, -0.8, -2.15]
PASSES = [[(3,), (5,), (9,), (4,), (7,)],
          [(3, 5), (4, 9), (7,)],
          [(3, 4, 5, 9), (7,)],
          [(3, 4, 5, 7, 9)]]
# clip 2
RS = 0.8          # the runs chain
ZCY = 0.0         # zipper centre

# recap layout (ch4 s7's, ch2 s7's look)
ICON_W, ICON_H = 5.2, 1.12
ROW_Y0, ROW_PITCH = 2.25, 1.28
TEXT_GAP = 0.5
LINE = 30


def chain(vals, s):
    """ConsChain scaled by s, values (and []) kept readable (≥ size 31), as s2's Zipper does."""
    ch = ConsChain(list(vals)).scale(s)
    k = max(1.0, 31 / (42 * s))
    for m in [cl.label for cl in ch.cells] + [ch.nil.label]:
        m.scale(k)
    ch.vals = tuple(vals)
    return ch


def place_row(chains, y, gap=0.6):
    total = sum(c.width for c in chains) + gap * (len(chains) - 1)
    x = -total / 2
    for c in chains:
        c.move_to([x + c.width / 2, y, 0])
        x += c.width + gap
    return chains


def mini_tree():
    """s5's split tree, rows scaled TREE_S, levels spread TREE_SY, labels back to size 30."""
    g = S5.split_tree(RUN)
    for k, r in g.rows.items():
        x, y = S5.POS[k]
        r.scale(TREE_S).move_to([x * TREE_S, y * TREE_SY + TREE_DY, 0])
    for k, p in S5.PARENT.items():
        g.edges[k].become(S5.tree_edge(g.rows[p], g.rows[k]))
    S6.grow_text(g, 30)
    return g


def fit(m, w=ICON_W, h=ICON_H):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


def colour(text, sub, col, nth=0):
    select(text, sub)[nth].set_color(col)


def two_lines(a, b=None):
    lines = [T(a, LINE, disable_ligatures=True)] + ([T(b, LINE, disable_ligatures=True)] if b else [])
    g = VGroup(*lines).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    g.lines = lines
    return g


# ── recap icons ─────────────────────────────────────────────────────────────────
def zipper_icon():
    """s2's zipper: start (two GOLD-valued rows) and finished state, fitted by the same map."""
    z0 = S2.Zipper()
    z1 = S2.final_zipper(cy=S2.ZIP_Y)
    for z in (z0, z1):
        for ch in (z.top, z.bot):
            for cl in ch.cells:
                cl.label.set_color(GOLD)
    g0 = VGroup(z0.top, z0.bot, z0.slots)
    g1 = VGroup(z1.top, z1.bot, z1.links)
    f = min(ICON_W / g0.width, ICON_H / g0.height)
    anchor = g0.get_center()
    for g in (g0, g1):
        g.scale(f, scale_stroke=True, about_point=anchor)
    g0.z, g0.z1, g0.after = z0, z1, g1
    return g0


def bound_icon():
    form = MathTex(r"\le m + n - 1", font_size=34, color=GOLD)
    box = SurroundingRectangle(form, color=GOLD, buff=0.18)
    boxed = VGroup(form, box)
    top, bot = ConsChain([5]), ConsChain([1, 2, 3, 4])
    for ch in (top, bot):
        for cl in ch.cells:
            cl.label.set_color(GOLD)
    lop = VGroup(top, bot).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
    fit(lop, 1.9, 1.0)
    g = VGroup(lop, boxed).arrange(RIGHT, buff=0.3)
    g.boxed, g.lop = boxed, lop
    return g


def split_icon():
    g = S4.split_shot()
    fit(g)
    g.run, g.cut, g.halves = g[0], g[1], list(g[2:])
    return g


def tree_icon():
    g = S6.level_tree(partial=True)
    fit(g)
    return g


def board_row_icon():
    lab = T("merge sort", 30, YELLOW)
    comps = T("120,392", 34, GOLD)
    secs = T("1.4 s", 34, GOLD)
    nums = VGroup(comps, secs).arrange(RIGHT, buff=0.5)
    secs.align_to(comps, DOWN)
    g = VGroup(lab, nums).arrange(DOWN, buff=0.22)
    g.lab, g.comps, g.secs = lab, comps, secs
    return g


class BottomUp(NarratedScene):
    def construct(self):
        self.top_down()
        self.runs()
        self.build_recap()
        self.recap()
        self.end_card()
        self.wait(8.0)                       # ends ON ch6's opening card (cross-chapter join, no fade)

    # ── c5.bottom.1 ─────────────────────────────────────────────────────────────
    def top_down(self):
        with self.say("c5.bottom.1") as c:
            tree = mini_tree()
            cap = T("top-down", 48).move_to(UP * CAP_Y)
            c.wait_until("top")
            self.play(FadeIn(tree), *appear(cap), run_time=1.4)  # early: the caption names what is shown

            down = Arrow([-ARROW_X, 1.6, 0], [-ARROW_X, -2.0, 0], buff=0, color=BLUE, stroke_width=5)
            up = Arrow([ARROW_X, -2.0, 0], [ARROW_X, 1.6, 0], buff=0, color=YELLOW, stroke_width=5)
            l_split = T("split", 34, BLUE).next_to(down, LEFT, buff=0.2)
            l_merge = T("merge", 34, YELLOW).next_to(up, RIGHT, buff=0.2)
            c.wait_until("splits first")
            self.play(GrowArrow(down), *appear(l_split), run_time=1.2)
            c.wait_until("merges")
            self.play(GrowArrow(up), *appear(l_merge), run_time=1.2)  # early: spoken as "merges"

            # {bottom}: the running chain, then it falls apart
            cap2 = T("bottom-up", 48).move_to(UP * CAP_Y)
            run = chain(RUN, PS).move_to([0, PASS_Y[0], 0])
            c.wait_until("They start")
            root = tree.rows["root"]
            rest = [m for k, m in tree.rows.items() if k != "root"] + list(tree.edges.values())
            self.play(*[FadeOut(m) for m in (*rest, down, up, l_split, l_merge)],
                      Transform(root, run), *swap(cap, cap2), run_time=1.2)
            self.remove(*tree.get_family())
            self.add(run)

            c.wait_until("one-item lists")
            singles = place_row([chain(v, PS) for v in PASSES[0]], PASS_Y[0])
            moves = [run.cells[i].animate.move_to(singles[i].cells[0]) for i in range(5)]
            new = [m for s in singles for m in (*s.arrows, s.nil)]
            self.play(*moves, *during([FadeOut(m) for m in (*run.arrows, run.nil)], 0, 0.35),
                      *during([FadeIn(m) for m in new], 0.6, 1.0), run_time=1.6)
            self.remove(*run.get_family())
            for s in singles:
                settle(self, s)
            self.cap = cap2

            prev = singles
            for k, cue in enumerate(("pass1", "pass2", "pass3")):
                c.wait_until(cue)
                if k == 0:
                    rt = min(1.2, 0.92 * c.until("pass2"))
                elif k == 1:
                    rt = min(0.85, 0.95 * c.until("pass3"))
                else:
                    rt = 1.2
                nxt = place_row([chain(v, PS) for v in PASSES[k + 1]], PASS_Y[k + 1])
                self.play(*self.pass_anims(prev, nxt), *set_alpha(prev, 0.35), run_time=rt)
                for ch in nxt:
                    settle(self, ch)
                prev = nxt
            tick = check_mark(GREEN).next_to(prev[0], RIGHT, buff=0.4)
            self.play(GrowFromCenter(tick), run_time=0.6)

    def pass_anims(self, prev, nxt):
        src = {}
        for ch in prev:
            for v, cl in zip(self.vals(ch), ch.cells):
                src[v] = cl
        anims = []
        for ch in nxt:
            vals = self.vals(ch)
            n = len(vals)
            for j, (v, cl) in enumerate(zip(vals, ch.cells)):
                a = 0.6 * j / n
                anims += during(fly(src[v], cl), a, a + 0.4)
            anims += during([FadeIn(m) for m in (*ch.arrows, ch.nil)], 0.7, 1.0)
        return anims

    @staticmethod
    def vals(ch):
        return ch.vals

    # ── c5.bottom.2 ─────────────────────────────────────────────────────────────
    def runs(self):
        with self.say("c5.bottom.2", gap=1.0) as c:
            run = chain(RUN, RS).move_to([0, ZCY, 0])
            c.wait_until("order")
            sweep_clear(self, time_span(FadeIn(run), 0.6, 1.2), run_time=1.2)

            cl = run.cells
            b1 = span_brace(cl[0].get_corner(UL), cl[2].get_corner(UR), direction=UP, color=GOLD)
            b2 = span_brace(cl[3].get_corner(UL), cl[4].get_corner(UR), direction=UP, color=GOLD)
            t1 = T("increasing", 32, GOLD).next_to(b1, UP, buff=0.15)
            t2 = T("increasing", 32, GOLD).next_to(b2, UP, buff=0.15)
            c.wait_until("split")
            self.play(GrowFromCenter(b1), GrowFromCenter(b2), run_time=1.2)
            c.wait_until(own_word=t1)
            self.play(*appear(t1, t2, lag=0.3), run_time=1.0)

            c.wait_until("three five nine")
            self.play(FlashAround(VGroup(*cl[:3]), color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("four seven")
            self.play(FlashAround(VGroup(*cl[3:]), color=GOLD, time_width=1.5), run_time=1.2)

            # the two runs pull apart into the zipper's rows
            z = S2.Zipper(top=(3, 5, 9), bot=(4, 7), cy=ZCY, left=S2.ZIP_LEFT, scale=S2.ZS)
            ar = run.arrows
            top_parts = [cl[0], cl[1], cl[2], ar[0], ar[1]]
            bot_parts = [cl[3], cl[4], ar[3], ar[4], run.nil]
            self.play(*disappear(b1, b2, t1, t2), FadeOut(ar[2]),
                      *during([m.animate.shift(UP * S2.ROW_DY) for m in top_parts], 0.3, 1.0),
                      *during([m.animate.shift(DOWN * S2.ROW_DY) for m in bot_parts], 0.3, 1.0),
                      run_time=1.0)

            c.wait_until("once")
            pairs = list(zip(top_parts, [*z.top.cells, z.top.arrows[0], z.top.arrows[1]]))
            pairs += list(zip(bot_parts, [*z.bot.cells, *z.bot.arrows, z.bot.nil]))
            self.play(*[Transform(a, b.copy()) for a, b in pairs],
                      *during([FadeIn(z.top.arrows[2]), FadeIn(z.top.nil), FadeIn(z.slots)], 0.5, 1.0),
                      run_time=1.0)
            self.remove(*run.get_family(), z.top.arrows[2], z.top.nil)
            self.add(z.slots, z.top, z.bot)
            for w in ("top", "bot", "top", "bot"):
                self.play(*z.take(w), run_time=0.45)
            self.play(*z.rest("top"), run_time=0.5)

            # {sortedrun}: one run, nothing to merge
            c.wait_until("sortedrun")
            out = [*z.out, *z.links, *z.arr["top"], z.nil["top"]]
            d = -(z.out[0].get_left()[0] + z.nil["top"].get_right()[0]) / 2
            self.play(FadeOut(z.slots), FadeOut(z.nil["bot"]),
                      *[m.animate.shift(RIGHT * d + UP * 0.0) for m in out], run_time=1.0)
            b = span_brace(z.out[0].get_corner(UL), z.out[-1].get_corner(UR), direction=UP, color=GOLD)
            tag = T("one run, nothing to merge", 32, GOLD).next_to(b, UP, buff=0.15)
            c.wait_until("one long run")
            self.play(GrowFromCenter(b), *during(appear(tag), 0.3, 1.0), run_time=1.2)

    # ── c5.bottom.3: recap ──────────────────────────────────────────────────────
    def build_recap(self):
        self.title = T("Recap", 52).move_to(UP * CAP_Y)
        self.icons = [zipper_icon(), bound_icon(), split_icon(), tree_icon(), board_row_icon()]

        l1 = two_lines("merge: take the smaller head, repeat")
        colour(l1.lines[0], "merge:", YELLOW)
        l2 = two_lines("at most m + n − 1 comparisons,", "best when the lengths match")
        colour(l2.lines[0], "m + n − 1", GOLD)
        colour(l2.lines[1], "best", GREEN)
        l3 = two_lines("tmergesort: split by counting,", "sort both halves, merge")
        colour(l3.lines[0], "tmergesort:", YELLOW)
        l4 = two_lines("always halves: O(n log n),", "even at worst")
        colour(l4.lines[0], "O(n log n)", GREEN)
        l5 = two_lines("within 2% of the floor,", "still slower than quicksort")
        colour(l5.lines[0], "2%", GOLD)
        colour(l5.lines[1], "slower", RED)
        self.texts = [l1, l2, l3, l4, l5]

        x_text = ICON_W / 2 + TEXT_GAP
        for i, (icon, text) in enumerate(zip(self.icons, self.texts)):
            y = ROW_Y0 - i * ROW_PITCH
            d = np.array([0, y, 0]) - icon.get_center()
            icon.shift(d)
            if i == 0:
                icon.after.shift(d)
            text.move_to([0, y, 0])
            text.shift((x_text - text.get_left()[0]) * RIGHT)
        dx = -VGroup(*self.icons, *self.texts).get_center()[0]
        for m in [*self.icons, *self.texts, self.icons[0].after]:
            m.shift(dx * RIGHT)

    def recap(self):
        ic1, ic2, ic3, ic4, ic5 = self.icons
        l1, l2, l3, l4, l5 = self.texts
        with self.say("c5.bottom.3", gap=1.5) as c:
            sweep_clear(self, time_span(FadeIn(self.title, shift=0.3 * DOWN), 0.6, 1.5), run_time=1.5)

            # r1: the zipper closes
            c.wait_until("r1")
            z0, z1 = ic1.z, ic1.z1
            self.play(FadeIn(ic1), *during(appear(l1.lines[0]), 0.3, 1.0), run_time=1.4)
            c.wait_until("smaller head")
            v1 = {cl.value: cl for cl in [*z1.top.cells, *z1.bot.cells]}
            order = [3, 4, 5, 7, 9]
            cells0 = sorted([*z0.top.cells, *z0.bot.cells], key=lambda cl: order.index(cl.value))
            anims = []
            for j, cl in enumerate(cells0):
                a = 0.12 * min(j, 3)          # 7 and 9 go across together (the rest)
                anims += during([Transform(cl, v1[cl.value].copy())], a, a + 0.5)
            anims += [FadeOut(z0.top.nil), Transform(z0.bot.nil, z1.bot.nil.copy())]
            anims += during([FadeOut(a) for a in (*z0.top.arrows, *z0.bot.arrows)], 0, 0.3)
            anims += during([FadeOut(z0.slots)], 0, 0.5)
            new_ar = [*z1.arr["bot"], *z1.links]
            anims += during([FadeIn(a) for a in new_ar], 0.75, 1.0)
            self.play(*anims, run_time=2.0)
            self.remove(*ic1.get_family())
            z1.top.remove(z1.top.nil)       # the emptied top row's [] is left out of the icon
            settle(self, ic1.after)

            # r2: the bound, then the lopsided case
            c.wait_until("r2")
            self.play(FadeIn(ic2.boxed), *during(appear(l2.lines[0]), 0.3, 1.0), run_time=1.4)
            c.wait_until("works best")
            self.play(FadeIn(ic2.lop), *appear(l2.lines[1]), run_time=1.2)

            # r3: take/drop split
            c.wait_until("r3")
            self.play(FadeIn(ic3.run), *during(appear(l3.lines[0]), 0.3, 1.0), run_time=1.4)
            c.wait_until("counting")
            self.play(FadeIn(ic3.cut), run_time=0.8)
            c.wait_until("sorts both halves")
            self.play(*[FadeIn(h) for h in ic3.halves], *appear(l3.lines[1]), run_time=1.2)

            # r4: the balanced tree
            c.wait_until("r4")
            l4a = select(l4.lines[0], "always halves:")[0]
            l4b = select(l4.lines[0], "O(n log n),")[0]
            self.play(FadeIn(ic4.tree), FadeIn(l4a, shift=0.2 * DOWN), run_time=1.4)
            c.wait_until("big O")
            self.play(FadeIn(ic4.tags), GrowFromCenter(ic4.brace), FadeIn(ic4.blabel),
                      FadeIn(l4b, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("worst case")
            self.play(*appear(l4.lines[1]), run_time=1.0)
            self.remove(*l4.get_family())
            self.add(l4)

            # r5: the board row
            c.wait_until("r5")
            self.play(*appear(ic5.lab, ic5.comps, ic5.secs, shift=None, lag=0.3),  # early: the board row
                      *during(appear(l5.lines[0]), 0.4, 1.0), run_time=1.4)
            c.wait_until("still slower")
            self.play(*appear(l5.lines[1]), run_time=1.0)

    # ── c5.bottom.4: the end card = ch6's opening card ─────────────────────────────
    def end_card(self):
        card = S6CH.open_card()
        with self.say("c5.bottom.4", gap=0.2) as c:
            self.play(*swap(self.title, card.title), run_time=1.0)
            sweep_clear(self, time_span(FadeIn(card.board), 0.6, 1.2), keep=[card.title],  # early: the board, shown whole
                        run_time=1.2)

            c.wait_until("nocompare")
            self.play(FadeIn(card.buckets), run_time=1.0)
            self.play(*appear(*card.tiles, shift=0.9 * DOWN, lag=0.35), run_time=1.5)
            c.wait_until("never compares")
            self.play(*appear(card.tag), run_time=1.0)
