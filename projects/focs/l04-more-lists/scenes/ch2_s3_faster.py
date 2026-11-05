"""Chapter 2, scene 3: faster ways to search (halving, hashing), and why linear search still
matters. Clips c2.fast.1 – c2.fast.4.

Plan
- c2.fast.1: s2's last shot (abstract chain x1 → … → xn → [] + GOLD "linear: O(n)") fades back in
  top-left; it grows into the cost ladder. {sorted} a 16-box row of sorted primes, "ordered";
  {middle} a YELLOW box + "find 41" on the middle box, the wrong half dims, GOLD "steps: 1";
  {halve} 8 → 4 → 2 → 1 live boxes; {power} DIM Lecture 2 tag; {log} "ordered: O(log n)" born from
  the step counter.
- c2.fast.2: O(log n) joins the ladder; two GOLD columns (up to 1,000,000 vs about 20, 2^20);
  YELLOW "exponentially better"; {binary} DIM caption; {lists} a small chain, YELLOW hops crawl
  head → middle, "needs arrays or trees, not lists".
- c2.fast.3: hash table: one YELLOW arrow lands straight on 41's slot; "indexed: O(1)", footnote,
  a search bar on "web search engines"; O(1) joins the ladder (O(n), O(log n), O(1)).
- c2.fast.4: ladder dims, "linear: O(n)" to centre, four GREEN tags one by one.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── s2's last shot: the ONE place its geometry lives (relayed by s2, final) ────────────────
# 5-slot chain x_1 → x_2 → x_3 → ⋯ → x_n → [] (ConsChain, FG MathTex labels at 60), scaled 0.4,
# to_corner(UL, buff=0.55): centre (-4.172, 3.250), 4.779 × 0.400.
# GOLD MathTex("\text{linear:}\ ", "O(n)", 96) scaled 0.4, next_to(chain, DOWN, 0.3, LEFT):
# centre (-5.546, 2.551), 2.030 × 0.399.
S2_SLOTS = ["x_1", "x_2", "x_3", r"\cdots", "x_n"]
S2_CHAIN_SCALE = 0.4
S2_CORNER_BUFF = 0.55
S2_LABEL_SCALE = 0.4         # cost labels are MathTex at 96 scaled; ladder rungs use 0.4 like s2
S2_LABEL_BUFF = 0.3
LADDER_PITCH = 0.6           # O(log n), O(1) stack under "linear: O(n)"

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53]
# (compared index, indices thrown away): 16 → 8 → 4 → 2 → 1, looking for 41
STEPS = [(7, range(0, 8)), (11, range(8, 12)), (13, range(14, 16)), (12, range(13, 14))]
BOX = 0.75
ROW_Y = 0.5
LOG_SCALE = 0.5              # "ordered: O(log n)" when it first lands (centre), then 0.4 in the ladder
IDX_SCALE = 0.46             # "indexed: O(1)" beside the hash table


def cost_label(word, big_o, scale):
    """GOLD 'word: O(..)' in s2's style (MathTex at 96, then scaled)."""
    return MathTex(rf"\text{{{word}:}}\ ", big_o, font_size=96, color=GOLD).scale(scale)


def s2_shot():
    chain = ConsChain(["x"] * len(S2_SLOTS))
    for cell, tex in zip(chain.cells, S2_SLOTS):
        cell.remove(cell.label)
        cell.label = MathTex(tex, font_size=60, color=FG).move_to(cell.box)
        cell.add(cell.label)
    chain.scale(S2_CHAIN_SCALE).to_corner(UL, buff=S2_CORNER_BUFF)
    lin = cost_label("linear", "O(n)", S2_LABEL_SCALE)
    lin.next_to(chain, DOWN, buff=S2_LABEL_BUFF, aligned_edge=LEFT)
    return VGroup(chain, lin), chain, lin


def ladder_slot(lin, i):
    """Left-centre point of ladder rung i (0 = "linear: O(n)")."""
    return lin.get_left() + DOWN * LADDER_PITCH * i


def make_row():
    row = VGroup()
    for p in PRIMES:
        sq = Square(BOX, stroke_color=BLUE, stroke_width=3, fill_color=BG, fill_opacity=1)
        row.add(VGroup(sq, T(str(p), 34, GOLD).move_to(sq)))
    return row.arrange(RIGHT, buff=0).move_to(UP * ROW_Y)


def search_bar():
    bar = RoundedRectangle(corner_radius=0.31, width=3.4, height=0.62).set_stroke(FG, 3)
    word = T("search", 30, DIM).move_to(bar).align_to(bar, LEFT).shift(RIGHT * 0.32)
    c = bar.get_right() + LEFT * 0.42 + UP * 0.04
    d = np.array([1, -1, 0]) / np.sqrt(2)
    glass = VGroup(Circle(radius=0.13).move_to(c),
                   Line(c + 0.13 * d, c + 0.3 * d)).set_stroke(FG, 3)
    return VGroup(bar, word, glass)


class FasterSearch(NarratedScene):
    def construct(self):
        shot, achain, lin = s2_shot()
        self.shot, self.achain, self.lin = shot, achain, lin
        self.clip_halving()
        self.clip_million()
        self.clip_hash()
        self.clip_why()
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c2.fast.1: ordered → halving → O(log n) ──────────────────────────────────────────
    def clip_halving(self):
        shot, lin = self.shot, self.lin
        with self.say("c2.fast.1") as c:
            self.play(FadeIn(shot), run_time=0.8)
            c.wait_until("slow")
            self.play(FlashUnder(lin, color=RED, run_time=min(1.5, c.until("sorted", floor=0.5))))
            c.wait_until("sorted")

            row = make_row()
            ordered = T("ordered", 34, FG).next_to(row, DOWN, buff=0.3).align_to(row, LEFT)
            self.play(LaggedStart(*[FadeIn(b, shift=0.15 * DOWN) for b in row], lag_ratio=0.08),
                      time_span(FadeIn(ordered, shift=0.2 * DOWN), 1.1, 1.8), run_time=1.8)
            settle(self, row)
            c.wait_until("middle")

            # compare with the middle item
            hl = Square(BOX + 0.14).set_stroke(YELLOW, 5).set_fill(opacity=0).move_to(row[7])
            token = VGroup(T("find", 32, DIM), T("41", 36, YELLOW)).arrange(
                RIGHT, buff=0.14, aligned_edge=DOWN).next_to(hl, UP, buff=0.14)
            self.play(Create(hl), FadeIn(token, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("throw away")
            lab = T("steps:", 34, GOLD)
            num = T("1", 38, GOLD).next_to(lab, RIGHT, buff=0.15)
            num.align_to(lab[0], DOWN)
            counter = VGroup(lab, num).next_to(row, DOWN, buff=0.3).align_to(row, RIGHT)
            self.play(*[row[i].animate.set_opacity(DIMMED) for i in STEPS[0][1]],
                      FadeIn(counter, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("halve")

            # halve what's left: first slow, then quicker
            avail = c.until("power", floor=2.4)
            for k, (mid, gone) in enumerate(STEPS[1:], start=2):
                shift = row[mid].get_center() - hl.get_center()
                slide = [hl.animate.shift(shift), token.animate.shift(shift)]
                drop = [*[row[i].animate.set_opacity(DIMMED) for i in gone],
                        Transform(num, T(str(k), 38, GOLD).move_to(num))]
                if k == 2:
                    d = 0.42 * avail
                    self.play(*slide, run_time=0.55 * d)
                    self.play(*drop, run_time=0.45 * d)
                else:
                    d = 0.29 * avail
                    self.play(*[time_span(a, 0, 0.5 * d) for a in slide],
                              *[time_span(a, 0.45 * d, d) for a in drop], run_time=d)
            c.wait_until("power")

            power = T("Lecture 2: power halves its exponent", 32, DIM).move_to(DOWN * 1.4)
            self.play(FadeIn(power, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("log")
            logl = cost_label("ordered", r"O(\log n)", LOG_SCALE).move_to(DOWN * 2.5)
            self.play(FadeTransform(counter.copy(), logl), run_time=1.5)

        self.row, self.ordered, self.hl, self.token = row, ordered, hl, token
        self.counter, self.power, self.logl = counter, power, logl

    # ── c2.fast.2: a million vs twenty; binary search needs arrays ───────────────────────
    def clip_million(self):
        lin, logl = self.lin, self.logl
        with self.say("c2.fast.2") as c:
            self.play(FadeOut(self.counter), run_time=1.0)
            c.wait_until("lin")

            col1 = VGroup(T("linear", 34, FG), T("up to 1,000,000", 42, GOLD),
                          T("comparisons", 34, GOLD)).arrange(DOWN, buff=0.22)
            col2 = VGroup(T("halving", 34, FG), T("about 20", 42, GOLD), T("steps", 34, GOLD),
                          MathTex(r"2^{20} = 1{,}048{,}576", font_size=36, color=GOLD)
                          ).arrange(DOWN, buff=0.22)
            col1.move_to(LEFT * 4.2)
            col2.move_to(RIGHT * 4.2)
            col1.shift(UP * (-0.85 - col1.get_top()[1]))
            col2.shift(UP * (-0.85 - col2.get_top()[1]))
            # the Lecture 2 tag and O(log n) hold through "Let's see what that means"; then the
            # tag goes first, so O(log n) can fly up into the ladder without crossing it
            self.play(time_span(FadeOut(self.power), 0, 0.5),
                      time_span(logl.animate.scale(S2_LABEL_SCALE / LOG_SCALE).move_to(
                          ladder_slot(lin, 1), aligned_edge=LEFT), 0.25, 1.35),
                      time_span(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in col1],
                                            lag_ratio=0.3), 0.6, 2.0),
                      run_time=2.0)
            c.wait_until("twenty")
            self.play(LaggedStart(*[FadeIn(m, shift=0.2 * DOWN) for m in col2], lag_ratio=0.3),
                      run_time=1.8)
            c.wait_until("exp")

            better = VGroup(T("exponentially", 40, YELLOW), T("better", 40, YELLOW)).arrange(
                DOWN, buff=0.12).move_to([0, col1[1].get_y() - 0.25, 0])
            self.play(FadeIn(better, scale=0.85), run_time=0.6)
            c.wait_until("binary")

            bincap = T("binary search: next lecture", 30, DIM).next_to(
                self.row, DOWN, buff=0.3).align_to(self.row, RIGHT)
            self.play(FadeIn(bincap, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("lists")

            # a list can only be walked from the head
            lchain = ConsChain([2, 3, 5, 7, 11, 13, 17]).scale(0.72).move_to(DOWN * 2.05)
            lcap = T("needs arrays or trees, not lists", 34, FG,
                     t2c={"not lists": RED}).move_to(DOWN * 3.25)
            sweep_clear(self, time_span(FadeIn(lcap, shift=0.2 * DOWN), 0.0, 0.8),
                        time_span(FadeIn(lchain), 0.5, 1.5),
                        keep=[self.shot, logl, self.row, self.ordered, self.hl, self.token,
                              bincap], run_time=1.6)
            c.wait_until("because a list")
            d = max(c.remaining - 0.3, 2.0)
            cells = lchain.cells
            for i, f in enumerate([0.3, 0.24, 0.2]):
                hop = CurvedArrow(cells[i].box.get_top() + UP * 0.06,
                                  cells[i + 1].box.get_top() + UP * 0.06, angle=-PI / 2,
                                  color=YELLOW, stroke_width=4, tip_length=0.2)
                self.play(Create(hop), run_time=f * d)
            self.play(cells[3].box.animate.set_stroke(YELLOW),
                      FlashAround(cells[3], run_time=0.24 * d))

    # ── c2.fast.3: index the data: hash table, O(1) ──────────────────────────────────────
    def clip_hash(self):
        lin, logl = self.lin, self.logl
        with self.say("c2.fast.3") as c:
            slots = VGroup(*[Rectangle(width=2.2, height=0.6).set_stroke(BLUE, 2.5)
                             for _ in range(7)]).arrange(DOWN, buff=0).move_to([0.4, -0.5, 0])
            vals = VGroup()
            for s, v in zip(slots, ["29", None, "13", None, "41", "3", None]):
                if v:
                    vals.add(T(v, 34, DIM).move_to(s))
            hit = vals[3]                                  # the 41 in slot 4
            box = RoundedRectangle(corner_radius=0.2, width=slots.width + 0.44,
                                   height=slots.height + 0.44).set_stroke(BLUE, 3).move_to(slots)
            tlabel = T("hash table", 36, FG).next_to(box, UP, buff=0.2)
            table = VGroup(box, slots, vals, tlabel)
            item = VGroup(RoundedRectangle(corner_radius=0.12, width=1.0, height=0.66
                                           ).set_stroke(YELLOW, 3),
                          T("41", 38, YELLOW)).move_to([-3.7, -0.5, 0])
            c.wait_until("index the data")
            sweep_clear(self, time_span(FadeIn(table), 0.4, 1.4), keep=[self.shot, logl],
                        run_time=1.4)
            c.wait_until("hash")
            self.play(FadeIn(item, shift=0.3 * RIGHT), run_time=0.7)
            c.wait_until("find an item")

            jump = Arrow(item.get_right(), slots[4].get_left(), buff=0.08, stroke_width=5,
                         color=YELLOW, max_tip_length_to_length_ratio=0.12)
            self.play(GrowArrow(jump), time_span(hit.animate.set_color(YELLOW), 0.8, 1.3),
                      time_span(FlashAround(slots[4]), 0.75, 1.45), run_time=1.45)
            c.wait_until("big O of one")
            idx = cost_label("indexed", "O(1)", IDX_SCALE).move_to([4.3, 0.5, 0])
            self.play(FadeIn(idx, shift=0.3 * DOWN), run_time=0.9)
            c.wait_until("limits")
            foot = T("(within machine limits)", 30, DIM).next_to(idx, DOWN, buff=0.3)
            self.play(FadeIn(foot, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("web")
            bar = search_bar().move_to([4.3, -1.4, 0])
            self.play(FadeIn(bar, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("They depend on it")
            self.play(FadeOut(foot),
                      idx.animate.scale(S2_LABEL_SCALE / IDX_SCALE).move_to(
                          ladder_slot(lin, 2), aligned_edge=LEFT),
                      run_time=min(1.5, c.remaining))
        self.idx = idx

    # ── c2.fast.4: why bother with linear search? ────────────────────────────────────────
    def clip_why(self):
        lin, logl, idx = self.lin, self.logl, self.idx
        with self.say("c2.fast.4") as c:
            hero = lin.copy()
            hero.generate_target()
            hero.target.scale(1.5).move_to(UP * 1.2)
            sweep_clear(self, MoveToTarget(hero),
                        *[m.animate.set_opacity(DIMMED) for m in (self.achain, lin, logl, idx)],
                        keep=[self.shot, logl, idx], run_time=1.6)

            texts = ["simple", "general", "fine for small collections",
                     "the starting point for better algorithms"]
            tags = VGroup()
            for s in texts:
                tags.add(VGroup(check_mark(GREEN).scale(0.8), T(s, 36, GREEN)).arrange(
                    RIGHT, buff=0.3))
            tags.arrange(DOWN, buff=0.38, aligned_edge=LEFT)
            tags.next_to(hero.target, DOWN, buff=0.6).set_x(0)
            gen = tags[1][1]
            more = T(": any order", 36, GREEN).next_to(gen, RIGHT, buff=0.04)
            more.shift(UP * (gen[1].get_bottom()[1] - more[1].get_bottom()[1]))
            VGroup(tags, more).set_x(0)

            def show(tag):
                self.play(Create(tag[0]), FadeIn(tag[1], shift=0.2 * DOWN), run_time=0.7)

            for cue, tag in zip(["simple", "general", "small", "start"], tags):
                c.wait_until(cue)
                show(tag)
                if cue == "general":
                    c.wait_until("any order")
                    self.play(FadeIn(more, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("write")
            self.play(FlashAround(hero, run_time=1.5, time_width=1.5))
