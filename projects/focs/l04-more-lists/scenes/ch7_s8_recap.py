"""Chapter 7, scene 8: the recap of the six solutions (one row per exercise), then the end card:
next lecture, Sorting, with ch1's chain cut in two by take and drop. Clips c7.recap.1 – c7.recap.2
(the chapter's and the lecture's last scene).

Layout follows ch5_s7_recap / ch6_s7_recap: title "Recap" (T 48) at y 3.25, text at size 34, a said
row steps back to 0.5. Six rows at y 2.15 - 1.02 k; each row: the exercise number (T 34, from the
kit's EX_NUMS; all six appear DIM on {recap}, each turns FG when its row is said) at x -6.55, the
function name YELLOW (Mono 34) from x -5.65, the row's text from x -3.55:
  4.1 union   keeps what ys lacks, in O(m·n); shares ys (TEAL)
  4.2 bysign  a let, like unzip; 0 goes first (GREEN)
  4.3 zip     strict: Match_failure (RED)   old: drops the surplus
  4.4 change  coins > 0, distinct, descending; amt ≥ 0 (conditions GREEN, one per spoken word)
  4.5 ways    2 coins: O(n)   k coins: O(n^(k-1))  (the second cost born from the first)
  4.6 f, g    f (1, true) = (true, 1)   g 0 = [0; …; 0]  (results GREEN, born from the arguments:
              1 and true swap places, the 0 is copied into the list)
End card (c7.recap.2): the rows recede to their numbers and names (0.5), a column on the left (row
4.6's text lingers at 0.5 until "merge sort", so its results stay up long enough);
"Next lecture:" (DIM) "Sorting" (YELLOW) T 48 at (1.5, 3.25); ch1's ConsChain([3, 5, 9, 4, 7]) x0.7
centred at (1.5, 0.1), cut by ch1's GOLD dashed line, split as ch6_s7_recap splits it into take's
[3; 5] and drop's [9; 4; 7] (Mono 36 YELLOW labels above), "merge sort" (T 40) below. It holds 8 s
under the music, then fades to an empty frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch6_s5_hints1 import EX_NUMS  # noqa: E402

# ── layout (the recap grid of ch5/ch6, a number + name column instead of icons) ─────
TITLE_Y = 3.25
TEXT_SIZE = 34
CAP = 0.0095 * TEXT_SIZE            # cap height of a text line: y names the middle of the caps
COST_SIZE = 40
CODE_SIZE = 30
SAID = 0.5
END_CARD = 8.0
UP_S = 0.25 * UP                    # the shift things enter with
ROW_Y = [2.15 - 1.02 * k for k in range(6)]
NUM_X, NAME_X, TEXT_X = -6.55, -5.65, -3.55
GAP = 0.6                           # between the two halves of a row

# end card
TEASER_X, CH_Y, CH_K = 1.5, 0.1, 0.7
SPLIT = 0.55                        # how far take's half and drop's half move apart
CHAIN = [3, 5, 9, 4, 7]             # ch1's running chain
CUT_X, CUT_H = -1.774, 1.05         # ch1's GOLD cut for that chain at ORIGIN (take 2)

FLAT = set("dfhiklmnrtuvwxzBDEFHIKLMNPRTUVWXZ1247")   # glyphs that sit exactly on the baseline


# ── helpers ─────────────────────────────────────────────────────────────────────
def baseline(m):
    """y of a text's baseline (a flat-bottomed glyph's bottom); MathTex: its first glyph's."""
    if isinstance(m, MathTex):
        return m[0][0].get_bottom()[1]
    s = getattr(m, "text", None)
    if isinstance(s, str):
        glyphs = [ch for ch in s if not ch.isspace()]
        for i, ch in enumerate(glyphs):
            if ch in FLAT and i < len(m):
                return m[i].get_bottom()[1]
    return m.get_bottom()[1]


def sit(m, y):
    """Shift m so its baseline is the baseline of a text line whose caps are centred on y."""
    return m.shift((y - CAP / 2 - baseline(m)) * UP)


def line_at(parts, y, x=TEXT_X, buff=0.22, gaps=None):
    """Parts in a row on one baseline, left edge at x, caps centred on y; gaps: {i: extra}."""
    grp = VGroup(*parts).arrange(RIGHT, buff=buff)
    for i, extra in (gaps or {}).items():
        for p in parts[i:]:
            p.shift(extra * RIGHT)
    for p in parts:
        sit(p, y)
    grp.shift((x - grp.get_left()[0]) * RIGHT)
    return grp


def prose(text, mono=(), **kw):
    """A text line; the words in `mono` set in the code font."""
    return T(text, size=TEXT_SIZE, t2f={w: MONO for w in mono}, **kw)


def cost(tex, *more):
    m = MathTex(tex, *more, font_size=COST_SIZE)
    m[0].set_color(GOLD)
    return m


def split_mono(full, cut, size=CODE_SIZE, colors=({}, {})):
    """`full` as two Mono pieces (before / after character `cut`), each glyph exactly where it
    sits in the whole line (monospace), so a piece can arrive later or be born from the other."""
    whole = Mono(full, size=size)
    a_src, b_src = full[:cut].rstrip(), full[cut:].lstrip()
    a, b = Mono(a_src, size=size, t2c=colors[0]), Mono(b_src, size=size, t2c=colors[1])
    a.shift(whole[0].get_center() - a[0].get_center())
    n_a = len([ch for ch in a_src if not ch.isspace()])
    b.shift(whole[n_a].get_center() - b[0].get_center())
    return whole, a, b


def back(mobs):
    """Step a said row back to SAID."""
    return [restyle(m, SAID) for m in mobs]


class SolutionsRecap(NarratedScene):
    def construct(self):
        self.build()
        self.recap()
        self.next_time()
        # End card: the finished recap and the next lecture, held under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── the rows ────────────────────────────────────────────────────────────────────
    def build(self):
        self.title = T("Recap", size=48).move_to([0, TITLE_Y, 0])
        self.nums = []
        for k, y in enumerate(ROW_Y):
            n = T(EX_NUMS[k], size=TEXT_SIZE, color=DIM)
            n.shift((NUM_X - n.get_left()[0]) * RIGHT)
            self.nums.append(sit(n, y))
        names = [Mono("union", size=34, color=YELLOW), Mono("bysign", size=34, color=YELLOW),
                 Mono("zip", size=34, color=YELLOW), Mono("change", size=34, color=YELLOW),
                 T("ways", size=TEXT_SIZE, color=YELLOW), Mono("f, g", size=34, color=YELLOW)]
        for m, y in zip(names, ROW_Y):
            m.shift((NAME_X - m.get_left()[0]) * RIGHT)
            sit(m, y)
        self.names = names

        # 4.1: keeps what ys lacks, in O(m·n); shares ys
        a1 = prose("keeps what ys lacks, in", mono=("ys",))
        a2 = cost(r"O(m \cdot n)", ";")
        a3 = prose("shares ys", mono=("ys",), color=TEAL)
        line_at([a1, a2, a3], ROW_Y[0], gaps={2: 0.05})
        # 4.2: a let, like unzip; 0 goes first
        b1 = prose("a let, like unzip;", mono=("let", "unzip"), t2c={"let": BLUE, "unzip": YELLOW})
        b2 = prose("0 goes first", color=GREEN)
        line_at([b1, b2], ROW_Y[1])
        # 4.3: strict: Match_failure   old: drops the surplus
        c1 = prose("strict:")
        c2 = Mono("Match_failure", size=CODE_SIZE, color=RED)
        c3, c4 = prose("old:"), prose("drops the surplus")
        line_at([c1, c2, c3, c4], ROW_Y[2], gaps={2: GAP - 0.22})
        # 4.4: coins > 0, distinct, descending; amt ≥ 0
        d1 = prose("coins > 0,", t2c={">": GREEN, "0": GREEN})
        d2 = prose("distinct,", t2c={"distinct": GREEN})
        d3 = prose("descending;", t2c={"descending": GREEN})
        d4 = prose("amt ≥ 0", mono=("amt",), t2c={"≥": GREEN, "0": GREEN})
        line_at([d1, d2, d3, d4], ROW_Y[3])
        # 4.5: 2 coins: O(n)   k coins: O(n^(k-1))
        e1, e2 = prose("2 coins:"), cost("O(n)")
        e3, e4 = prose("k coins:", t2s={"k": ITALIC}), cost("O(n^{k-1})")
        line_at([e1, e2, e3, e4], ROW_Y[4], gaps={2: GAP - 0.22})
        # 4.6: f (1, true) = (true, 1)   g 0 = [0; …; 0]
        wf, f1, f2 = split_mono("f (1, true) = (true, 1)", 13,
                                colors=({"f": YELLOW, "1": GOLD}, {}))
        wg, g1, g2 = split_mono("g 0 = [0; …; 0]", 5, colors=({"g": YELLOW, "0": GOLD}, {}))
        f2.set_color(GREEN)
        g2.set_color(GREEN)
        sit(wf, ROW_Y[5])
        wf.shift((TEXT_X - wf.get_left()[0]) * RIGHT)
        wg.shift((wf[9].get_y() - wg[2].get_y()) * UP)              # the two "=" on one line
        wg.shift((wf.get_right()[0] + GAP - wg.get_left()[0]) * RIGHT)
        for whole, a, b in ((wf, f1, f2), (wg, g1, g2)):
            a.shift(whole[0].get_center() - a[0].get_center())
            n_a = len(a)
            b.shift(whole[n_a].get_center() - b[0].get_center())
        self.texts = [[a1, a2, a3], [b1, b2], [c1, c2, c3, c4], [d1, d2, d3, d4],
                      [e1, e2, e3, e4], [f1, f2, g1, g2]]

    def light(self, k, *more, run_time=1.2):
        """Row k comes up: the row before steps back, its number turns FG, its name drops in."""
        prev = [] if k == 0 else back([self.nums[k - 1], self.names[k - 1], *self.texts[k - 1]])
        self.play(*prev, self.nums[k].animate.set_color(FG),
                  FadeIn(self.names[k], shift=UP_S), *more, run_time=run_time)

    # ── c7.recap.1: the six rows ──────────────────────────────────────────────────────
    def recap(self):
        nums, (r1, r2, r3, r4, r5, r6) = self.nums, self.texts
        with self.say("c7.recap.1") as c:
            # "Let's recap."  The title, and the six exercise numbers: the whole shape.
            self.play(time_span(FadeIn(self.title, shift=0.3 * DOWN), 0, 1.0),
                      LaggedStart(*[FadeIn(n, shift=UP_S) for n in nums], lag_ratio=0.15),
                      run_time=min(1.5, c.until("r1") - 0.05))

            # "Union walks the first list and keeps what the second lacks, ..."
            c.wait_until("r1")
            self.light(0, time_span(FadeIn(r1[0], shift=UP_S), 0.4, 1.3), run_time=1.3)
            # "... in big O of em times en."
            c.wait_until("in big O")
            self.play(FadeIn(r1[1], shift=UP_S), time_span(FadeIn(r1[2], shift=UP_S), 0.6, 1.4),
                      run_time=1.4)

            # "Splitting by sign builds two results at once, ..."
            c.wait_until("r2")
            self.light(1)
            # "... with a let, like unzip."
            c.wait_until("with a let")
            self.play(FadeIn(r2[0], shift=UP_S), time_span(FadeIn(r2[1], shift=UP_S), 0.7, 1.5),
                      run_time=1.5)

            # "The stricter zip rejects unequal lengths, ..."
            c.wait_until("r3")
            self.light(2, time_span(FadeIn(r3[0], shift=UP_S), 0.4, 1.2),
                       time_span(FadeIn(r3[1], shift=UP_S), 0.6, 1.4), run_time=1.4)
            # "... where the old one drops the surplus."
            c.wait_until("where the old one")
            self.play(FadeIn(r3[2], shift=UP_S), time_span(FadeIn(r3[3], shift=UP_S), 0.3, 1.1),
                      run_time=1.1)

            # "The change functions trust the till to hold positive, distinct coins, in descending
            # order, and the amount to be zero or more."  One condition per spoken word.
            c.wait_until("r4")
            self.light(3)
            for piece, cue in zip(r4, ("positive", "distinct", "descending", "zero or more")):
                c.wait_until(cue)
                self.play(FadeIn(piece, shift=UP_S), run_time=min(0.8, c.until(None) - 0.1))

            # "With two coins, the ways grow as big O of en, ..."
            c.wait_until("r5")
            self.light(4, time_span(FadeIn(r5[0], shift=UP_S), 0.4, 1.2), run_time=1.2)
            c.wait_until("big O of en")
            self.play(FadeIn(r5[1], shift=UP_S), FlashUnder(r5[1], color=GOLD), run_time=1.0)
            # "... and each extra coin multiplies that by en."  The general cost, born from it.
            c.wait_until("each extra coin")
            self.play(FadeIn(r5[2], shift=UP_S), TransformFromCopy(r5[1], r5[3]), run_time=1.6)

            # "And the types force eff to swap, ..."  1 and true trade places.
            c.wait_until("r6")
            f1, f2, g1, g2 = r6
            self.light(5, time_span(FadeIn(f1, shift=UP_S), 0.4, 1.2), run_time=1.2)
            c.wait_until("swap")
            pairs = [(1, 0), (4, 1), (5, 2), (6, 3), (7, 4), (3, 5), (2, 6), (8, 7)]
            arcs = {2: -PI / 2, 4: PI / 3, 5: PI / 3, 6: PI / 3, 7: PI / 3}
            self.play(*[TransformFromCopy(f1[s], f2[d], path_arc=arcs.get(s, 0)) for s, d in pairs],
                      run_time=1.5)
            settle(self, f2)
            # "... and gee to return only copies of its argument."  The 0, copied.
            c.wait_until("and gee")
            self.play(FadeIn(g1, shift=UP_S), run_time=0.8)
            c.wait_until("to return")
            self.play(TransformFromCopy(g1[1], g2[1], path_arc=-PI / 3),
                      TransformFromCopy(g1[1], g2[5], path_arc=-PI / 3),
                      *[time_span(FadeIn(g2[i]), 0.3, 1.0) for i in (0, 2, 3, 4, 6)],
                      run_time=min(1.3, max(0.8, c.until(None) - 0.05)))
            settle(self, g2)

    # ── c7.recap.2: next lecture (the end card) ───────────────────────────────────────
    def next_time(self):
        hd1, hd2 = T("Next lecture:", size=48, color=DIM), T("Sorting", size=48, color=YELLOW)
        head = VGroup(hd1, hd2).arrange(RIGHT, buff=0.25)
        hd2.shift((baseline(hd1) - baseline(hd2)) * UP)
        head.move_to([TEASER_X, TITLE_Y, 0])

        # ch1's chain, the GOLD cut, the halves take and drop (as ch6_s7_recap draws them)
        ch = ConsChain(CHAIN).scale(CH_K).move_to([TEASER_X, CH_Y, 0])
        cx = TEASER_X + CH_K * CUT_X
        cut = DashedLine([cx, CH_Y - CH_K * CUT_H, 0], [cx, CH_Y + CH_K * CUT_H, 0],
                         dash_length=0.08).set_stroke(GOLD, 5)
        left = [ch.cells[0], ch.arrows[0], ch.cells[1]]
        right = [ch.cells[2], ch.arrows[2], ch.cells[3], ch.arrows[3], ch.cells[4], ch.arrows[4], ch.nil]
        new_nil = Nil().scale(CH_K)
        new_nil.move_to(ch.cells[2].box.get_left() + LEFT * SPLIT, aligned_edge=LEFT)
        new_nil.shift((ch.cells[1].box.get_y() - new_nil.get_y()) * UP)
        ghost_1 = ch.cells[1].copy().shift(LEFT * SPLIT)
        new_arrow = link(ghost_1, new_nil)
        take_l = Mono("take", size=36, color=YELLOW)
        drop_l = Mono("drop", size=36, color=YELLOW)
        top_y = ch.get_top()[1] + 0.5
        take_x = (ch.cells[0].get_left()[0] - SPLIT + new_nil.get_right()[0]) / 2
        drop_x = (ch.cells[2].get_left()[0] + ch.nil.get_right()[0]) / 2 + SPLIT
        take_l.move_to([take_x, top_y, 0])
        drop_l.move_to([drop_x, top_y, 0]).align_to(take_l, UP)       # one cap line ("p" descends)
        msort = T("merge sort", size=40).move_to([TEASER_X, ch.get_bottom()[1] - 0.75, 0])

        with self.say("c7.recap.2") as c:
            # "Next time, in lecture five, we turn to sorting."  The rows recede to their
            # numbers and names (the last row's text lingers, dimmed, until the chain is cut);
            # the title gives way to the next lecture.
            last = self.texts[5]
            sweep_clear(self, *back([self.nums[5], self.names[5], *last]),
                        time_span(FadeIn(head, shift=0.3 * DOWN), 0.5, 1.4),
                        keep=[*self.nums, *self.names, *last], run_time=1.4)
            c.wait_until("turn to sorting")
            self.play(FadeIn(ch, shift=UP_S), run_time=1.2)

            # "Sorted data can be searched fast, and merge sort ..."
            c.wait_until("merge sort")
            self.play(GrowFromCenter(cut), FadeIn(msort, shift=UP_S),
                      *[FadeOut(m) for m in last], run_time=1.0)
            # "... splits its lists ..."
            c.wait_until("splits")
            self.play(*[m.animate.shift(LEFT * SPLIT) for m in left],
                      *[m.animate.shift(RIGHT * SPLIT) for m in right],
                      FadeOut(ch.arrows[1]), time_span(FadeOut(cut), 0.6, 1.3),
                      time_span(FadeIn(new_nil), 0.6, 1.3), time_span(GrowArrow(new_arrow), 0.6, 1.3),
                      run_time=1.3)
            # "... with take and drop."
            c.wait_until("with take")
            self.play(FadeIn(take_l, shift=0.2 * DOWN), time_span(FadeIn(drop_l, shift=0.2 * DOWN), 0.3, 1.0),
                      run_time=1.0)
            pics = VGroup(*left, new_arrow, new_nil, *right, take_l, drop_l, msort)
            settle(self, pics, drop=[])
            # "Well done.  See you in the next lecture."  Hold.
