"""Chapter 1, scene 3: binary search, as promised in Lecture 4. Clips c1.bin.1 – c1.bin.4.

Plan
- c1.bin.1: {row} L4 ch2 s3's 16 GOLD primes (make_row, imported) + YELLOW "find 41";
  {linear} a GOLD ▲ walks under the row 2 → 41 with a riding counter, "13 comparisons";
  {promise} pointer fades, "linear: 13" small bottom-left, DIM "Lecture 4: ..." tag at the top,
  which turns into the title "binary search" (TransformMatchingStrings) on "Here it is".
- c1.bin.2: four probes 19, 37, 43, 41 (YELLOW box, comparison under it, GOLD
  "comparisons: k" bottom-right); dead halves dim; 41 GREEN + "found".
- c1.bin.3: {four} counters regroup centred as "linear: 13" | "binary: 4"; {halves} two lines
  below (at least half / 1,000,000 → about 20); {logn} numbers become O(n) | O(log n), GOLD.
- c1.bin.4: {lists} row shrinks up, a prime chain (4 cells ⋯ 4 cells []) below; YELLOW ▼ drops
  straight onto the row's middle; {walk} a YELLOW ▼ crawls the chain head → ⋯, GOLD
  "about n/2 steps..."; {trees} "needs arrays or trees, not lists" + DIM Lecture 7 tag.
"""
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── Lecture 4 ch2 s3's prime row: imported, never copied ────────────────────────────────
_L4_PATH = (Path(__file__).resolve().parents[2] / "l04-more-lists" / "scenes"
            / "ch2_s3_faster.py")
_spec = importlib.util.spec_from_file_location("l04_ch2_s3_faster", _L4_PATH)
_l4 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_l4)
PRIMES, BOX, make_row = _l4.PRIMES, _l4.BOX, _l4.make_row

# L4's STEPS probe 19, 37, 43, 41 (indices 7, 11, 13, 12); here 43 is thrown away in step 3
PROBES = [(7, range(0, 8), ">"), (11, range(8, 12), ">"), (13, range(13, 16), "<"),
          (12, (), "=")]
TARGET = 12
ROW_Y = 0.2
FIND_Y = 2.0
TITLE_Y = 3.25
COUNT_Y = -1.8               # "linear: 13" (left) and "comparisons: k" (right)
PAIR_X = 2.7                 # c1.bin.3: the two counters side by side
HALF_Y = -2.7
MILLION_Y = -3.25
ROW2_SCALE = 0.85            # c1.bin.4: the row shrinks up (labels stay >= 28)
ROW2_Y = 1.85
CHAIN_Y = 0.4
STEPS_Y = -0.8
NEEDS_Y = -2.05
TAG7_Y = -2.95


def pair(word, num, wsize, nsize, wcol=FG, ncol=GOLD):
    """'word: n' with the number on the word's baseline (its first glyph's bottom)."""
    lab = T(word, wsize, wcol)
    n = T(num, nsize, ncol).next_to(lab, RIGHT, buff=0.18)
    n.align_to(lab[0], DOWN)
    return VGroup(lab, n)


def big_o(lab, tex, size=60):
    """GOLD MathTex O(..) after lab, its O sitting on lab's baseline."""
    o = MathTex(tex, font_size=size, color=GOLD).next_to(lab, RIGHT, buff=0.2)
    o.shift(UP * (lab[0].get_bottom()[1] - o[0][0].get_bottom()[1]))
    return o


class _Anchor:
    """A point that link() can start from or land on (the ⋯ in the chain)."""
    def __init__(self, p):
        self.p = np.array(p, dtype=float)

    def entry(self):
        return self.p

    def tail_start(self):
        return self.p


def prime_chain():
    """2 → 3 → 5 → 7 → ⋯ → 41 → 43 → 47 → 53 → [], values GOLD, nil TEAL; centred at ORIGIN."""
    vals = [2, 3, 5, 7, 41, 43, 47, 53]
    cells = []
    for v in vals:
        cell = ConsCell(v)
        cell.remove(cell.label)
        cell.label = value_label(v, 54, GOLD).move_to(cell.box)
        cell.add(cell.label)
        cells.append(cell)
    dots = MathTex(r"\cdots", font_size=72, color=FG)
    nil = Nil(size=54)
    x = 0.0
    for m in cells[:4] + [dots] + cells[4:] + [nil]:
        m.move_to([x + m.width / 2, 0, 0])
        x += m.width + LINK
    arrows = [link(cells[k], cells[k + 1]) for k in range(3)]
    arrows.append(link(cells[3], _Anchor(dots.get_left() + LEFT * 0.08)))
    arrows.append(link(_Anchor(dots.get_right() + RIGHT * 0.08), cells[4]))
    arrows += [link(cells[k], cells[k + 1]) for k in range(4, 7)]
    arrows.append(link(cells[7], nil))
    chain = VGroup(*cells, dots, nil, *arrows)
    return chain, cells, dots, arrows


class BinarySearch(NarratedScene):
    def construct(self):
        self.clip_linear()
        self.clip_probes()
        self.clip_compare()
        self.clip_lists()
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c1.bin.1: the row, the linear walk, the promise ───────────────────────────────────
    def clip_linear(self):
        with self.say("c1.bin.1") as c:
            row = make_row().move_to(UP * ROW_Y)
            find = T("find 41", 40, YELLOW).move_to(UP * FIND_Y)
            self.play(LaggedStart(*[FadeIn(b, shift=0.15 * DOWN) for b in row], lag_ratio=0.08),
                      run_time=1.8)
            settle(self, row)
            c.wait_until("forty-one")
            self.play(FadeIn(find, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("linear")

            # one box at a time from the left: a GOLD pointer with a riding counter
            xs = [b.get_x() for b in row]
            ptr = marker(GOLD).rotate(PI)
            ptr.move_to([xs[0], row.get_bottom()[1] - 0.15 - ptr.height / 2, 0])
            nums = [T(str(k), 40, GOLD) for k in range(1, TARGET + 2)]
            cnt = nums[0].copy().next_to(ptr, DOWN, buff=0.15)
            cnt_y = cnt.get_y()

            def phase(a):
                s = a * TARGET
                k = min(int(s), TARGET - 1)
                return k, smooth(min((s - k) / 0.55, 1.0))

            def move_ptr(m, a):
                k, f = phase(a)
                m.set_x(interpolate(xs[k], xs[k + 1], f))

            def move_cnt(m, a):
                k, f = phase(a)
                shown = k + 1 if f < 0.5 else k + 2
                m.become(nums[shown - 1].copy().move_to(
                    [interpolate(xs[k], xs[k + 1], f), cnt_y, 0]))

            self.play(FadeIn(ptr, shift=0.2 * UP), FadeIn(cnt, shift=0.2 * UP), run_time=0.5)
            walk = max(2.4, c.until("promise") - 1.0)
            self.play(UpdateFromAlphaFunc(ptr, move_ptr), UpdateFromAlphaFunc(cnt, move_cnt),
                      run_time=walk, rate_func=linear)
            comps = T("comparisons", 34, GOLD).next_to(cnt, RIGHT, buff=0.15)
            comps.shift(UP * (cnt.get_bottom()[1] - comps[0].get_bottom()[1]))
            self.play(FadeIn(comps, shift=0.2 * LEFT), run_time=min(0.6, c.until("promise")))
            c.wait_until("promise")

            # the pointer goes; the promise
            tag = T("Lecture 4: binary search, coming next lecture", 32, DIM).move_to(UP * TITLE_Y)
            self.play(FadeOut(ptr), FadeIn(tag, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("Here it is")

            # "linear: 13" stays small at the left; the tag becomes the title
            lin = pair("linear:", "13", 32, 40)
            lin.align_to(row, LEFT).set_y(COUNT_Y)
            lin_lab, lin_num = lin
            title = T("binary search", 52, FG).move_to(UP * TITLE_Y)
            d = min(1.6, c.until(floor=1.2))
            self.play(time_span(FadeOut(comps), 0, 0.5 * d),
                      time_span(ReplacementTransform(cnt, lin_num), 0, 0.75 * d),
                      time_span(FadeIn(lin_lab, shift=0.2 * RIGHT), 0.4 * d, 0.8 * d),
                      time_span(TransformMatchingStrings(tag, title), 0.15 * d, d), run_time=d)

        self.row, self.find, self.title = row, find, title
        self.lin_lab, self.lin_num = lin_lab, lin_num

    # ── c1.bin.2: four probes ─────────────────────────────────────────────────────────────
    def clip_probes(self):
        row = self.row

        def probe_box(i, color=YELLOW):
            return Square(BOX).set_stroke(color, 5).set_fill(opacity=0).move_to(row[i])

        def comparison(i, rel):
            m = MathTex("41", rel, str(PRIMES[i]), font_size=44, color=FG)
            m[0].set_color(YELLOW)
            return m.next_to(row[i], DOWN, buff=0.3)

        def bump(k):
            return Transform(self.ctr_num, T(str(k), 40, GOLD).move_to(self.ctr_num))

        def drop(i, gone, box):
            return [*[row[j].animate.set_opacity(DIMMED) for j in gone],
                    box.animate.set_stroke(opacity=DIMMED)]

        boxes = []
        with self.say("c1.bin.2") as c:
            # 1: the middle item, 19
            i, gone, rel = PROBES[0]
            box = probe_box(i)
            boxes.append(box)
            pos = T("position 8", 30, DIM).next_to(row[i], UP, buff=0.18)
            self.play(Create(box), row[i][1].animate.set_color(YELLOW),
                      FadeIn(pos, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("which is nineteen")
            ctr = pair("comparisons:", "1", 34, 40, wcol=GOLD)
            ctr.align_to(row, RIGHT).set_y(COUNT_Y)
            self.ctr_lab, self.ctr_num = ctr
            self.play(FadeIn(self.ctr_lab, shift=0.2 * DOWN), FadeIn(self.ctr_num, shift=0.2 * DOWN),
                      run_time=1.0)
            c.wait_until("left")
            cmp = comparison(i, rel)
            self.play(FadeIn(cmp, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("Throw the left half away")
            self.play(*drop(i, gone, box), FadeOut(pos), run_time=1.2)
            c.wait_until("second")

            # 2: 37, then 3: 43
            for (i, gone, rel), k, said, thrown in [
                    (PROBES[1], 2, "Bigger again", "throw away thirty-seven"),
                    (PROBES[2], 3, "This time", "throw away forty-three")]:
                box = probe_box(i)
                boxes.append(box)
                self.play(Create(box), row[i][1].animate.set_color(YELLOW), bump(k),
                          run_time=1.2)
                c.wait_until(said)
                old, cmp = cmp, comparison(i, rel)
                self.play(FadeOut(old), FadeIn(cmp, shift=0.2 * DOWN), run_time=0.9)
                c.wait_until(thrown)
                self.play(*drop(i, gone, box), run_time=1.2)
                c.wait_until("third" if k == 2 else "found")

            # 4: one item left, found
            i = PROBES[3][0]
            self.play(FlashAround(row[i], time_width=1.5, color=YELLOW), run_time=1.2)
            c.wait_until("the fourth comparison")
            box = probe_box(i, GREEN)
            boxes.append(box)
            found = T("found", 36, GREEN).next_to(row[i], DOWN, buff=0.3)
            self.play(Create(box), row[i][1].animate.set_color(GREEN), bump(4),
                      FadeOut(cmp), FadeIn(found, shift=0.2 * DOWN), run_time=1.2)
        self.boxes, self.found = boxes, found

    # ── c1.bin.3: 4 against 13; halving; O(log n) vs O(n) ─────────────────────────────────
    def clip_compare(self):
        with self.say("c1.bin.3") as c:
            L = pair("linear:", "13", 36, 60).move_to([-PAIR_X, COUNT_Y, 0])
            B = pair("binary:", "4", 36, 60).move_to([PAIR_X, COUNT_Y, 0])
            self.play(ReplacementTransform(self.lin_lab, L[0]),
                      ReplacementTransform(self.lin_num, L[1]),
                      FadeTransform(self.ctr_lab, B[0]),
                      ReplacementTransform(self.ctr_num, B[1]), run_time=1.5)
            c.wait_until("halves")
            half = T("each comparison throws away at least half", 34, FG).move_to(UP * HALF_Y)
            self.play(FadeIn(half, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("even a million")
            million = VGroup(T("1,000,000 items", 36, GOLD),
                             MathTex(r"\rightarrow", font_size=44, color=GOLD),
                             T("about 20", 36, GOLD)).arrange(RIGHT, buff=0.3)
            million.move_to(UP * MILLION_Y)
            self.play(FadeIn(million, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("logn")

            # the counts become the costs
            labs, os_ = [], []
            for (lab, num), tex, x in [(L, "O(n)", -PAIR_X), (B, r"O(\log n)", PAIR_X)]:
                new_lab = lab.copy().set_color(GOLD)
                o = big_o(new_lab, tex)
                VGroup(new_lab, o).move_to([x, COUNT_Y, 0])
                labs.append((lab, new_lab))
                os_.append((num, o))
            self.play(*[lab.animate.set_color(GOLD).move_to(new) for lab, new in labs],
                      *[ReplacementTransform(num, o) for num, o in os_], run_time=1.2)
        self.costs = [L[0], B[0], os_[0][1], os_[1][1]]

    # ── c1.bin.4: the catch: lists ────────────────────────────────────────────────────────
    def clip_lists(self):
        row, title = self.row, self.title
        with self.say("c1.bin.4") as c:
            row_t = make_row().scale(ROW2_SCALE).move_to(UP * ROW2_Y)
            chain, cells, dots, arrows = prime_chain()
            chain.scale(min(0.62, 12.6 / chain.width)).move_to(UP * CHAIN_Y)
            sweep_clear(self, Transform(row, row_t), time_span(FadeIn(chain), 0.7, 1.7),
                        keep=[row, title, *self.costs], run_time=1.7)
            c.wait_until("Binary search jumps")

            # an array: straight to the middle
            jump = marker(YELLOW).move_to(above(row[7], buff=0.12))
            self.play(FadeIn(jump, shift=0.6 * DOWN), row[7][1].animate.set_color(YELLOW),
                      time_span(FlashAround(row[7], time_width=1.5), 0.3, 1.3), run_time=1.3)
            c.wait_until("walk")

            # a list: from the head, one cell at a time
            def spot(k):
                m = cells[k].box if k < 4 else dots
                return [m.get_x(), above(cells[0].box, buff=0.12)[1], 0]

            crawl = marker(YELLOW).move_to(spot(0))
            self.play(FadeIn(crawl, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("walking half")
            total = max(2.4, c.until("that alone") - 0.15)
            for k, f in enumerate([0.31, 0.24, 0.23, 0.22]):
                a = arrows[k]
                trail = Line(a.get_start(), a.get_end()).set_stroke(YELLOW, 6)
                self.play(crawl.animate.move_to(spot(k + 1)),
                          VShowPassingFlash(trail, time_width=0.6), run_time=0.6 * f * total)
                self.wait(0.4 * f * total)
            c.wait_until("that alone")
            steps = T("about n/2 steps, just to reach the middle", 36, GOLD).move_to(UP * STEPS_Y)
            self.play(FadeIn(steps, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("trees")

            needs = T("needs arrays or trees, not lists", 40, FG, t2c={"not lists": RED})
            needs.move_to(UP * NEEDS_Y)
            self.play(*[FadeOut(m) for m in self.costs],
                      time_span(FadeIn(needs, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("we'll meet")
            tag7 = T("binary search trees: Lecture 7", 32, DIM).move_to(UP * TAG7_Y)
            self.play(FadeIn(tag7, shift=0.2 * DOWN), run_time=0.9)
