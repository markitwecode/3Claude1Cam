"""Chapter 6, scene 7: the recap of the whole lecture (two pages of recap lines, each with a small
icon from its chapter), then the end card: next lecture (binary search, merge sort's take/drop
split) and the six exercises. Clips c6.recap.1 – c6.recap.3 (the lecture's last scene).

Layout follows ch4_s7_recap / ch5_s7_recap: title "Recap" at y 3.25, icon column centred at
x -5.05 (3.0 wide), text column from x -3.15 at size 34, a said line steps back to 0.5.
Seven recap rows don't fit one column at a readable size, so the recap has two pages, one per clip:
  page 1 (c6.recap.1, chapters 1-2): ch1's ConsChain([3,5,9,4,7]) with the GOLD cut (take / drop,
         O(i), O(1) space); the same chain with ch2's GOLD marker stepping (linear search, O(n));
         GREEN `=` beside a RED "functions" chip (polymorphic equality).
  page 2 (c6.recap.2, chapters 3-6): ch3's mirror (zip's and unzip's types, the shared
         ('a * 'b) list YELLOW-boxed in both); ch3's `let P = E` beside `let xs, ys = unzip pairs in`
         (one YELLOW box slides from the line onto the pattern); `change` and three numbered GOLD
         coin discs "greedy" (RED cross: stuck), "every way", "faster"; s4's three numbered steps
         born from the discs, "stepwise refinement", "start simple, add efficiency last".
c6.recap.3: header "Next lecture: Sorting" (T 48, "Next lecture:" DIM, "Sorting" YELLOW) at y 3.25.
{fast}: 8 sorted boxes, centred, a GOLD brace halving 8 -> 4 -> 2 -> 1 onto the 9, GOLD O(log n);
{merge}: the row slides left, ch1's chain comes in on the right, splits at the GOLD cut into take's
[3; 5] and drop's [9; 4; 7] (YELLOW mono labels), "merge sort". {bonus}: both pictures
step back to 0.5 (the split stays up through the next sentence) and s5's six_cards() comes in
below them: .cards scaled 0.85 (BigCards 3.49 x 1.23, columns x -3.66 / 0 / 3.66, rows y -0.71 /
-2.11, top -0.09), .note unscaled at y -3.2 on "the bonus chapter". End card = header + dimmed
pictures + six_cards(), held 8 s under the music, then faded. (s5's own layout, which ch7 opens
on: cards unscaled at rows y 1.35 / -0.30, note y -2.95.)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch6_s5_hints1 import six_cards  # noqa: E402  s5's six exercise cards + the solutions note

# ── layout (ch4/ch5 recap grid) ────────────────────────────────────────────────
TITLE_Y = 3.25
ICON_X, ICON_W = -5.05, 3.0
TEXT_X = -3.15
TEXT_SIZE = 34
CAP = 0.0095 * TEXT_SIZE            # cap height of a text line: y names the middle of the caps
COST_SIZE = 40
SAID = 0.5
END_CARD = 8.0
UP_S = 0.25 * UP                    # the shift things enter with

# page 1
P1_TD, P1_TD_ICON = (1.75, 1.15), 1.45
P1_S = -0.6
P1_EQ, P1_EQ_ICON = (-2.3, -2.9), -2.6
# page 2
P2_Z = (2.2, 1.6)
P2_P = 0.4
P2_C = -0.85
P2_R, P2_R_ICON = (-2.1, -2.7), -2.4
TYPE_SIZE, LET_SIZE = 30, 32
# end card
PIC_Y = 1.7
SORT_X, SORT_BOX, SORTED = -3.75, 0.66, [1, 3, 4, 5, 7, 9, 12, 15]
HALVES = [(4, 8), (4, 6), (5, 6)]   # the brace closes in on the 9
MERGE_X, MERGE_K = 3.34, 0.45
SPLIT_L, SPLIT_R = 0.45, 0.45       # how far take's half and drop's half move apart
PIC_LABEL_Y = 0.55
EX_K, EX_TOP, NOTE_Y = 0.85, -0.09, -3.2   # s5's six cards, scaled, under the pictures; its note

CHAIN = [3, 5, 9, 4, 7]             # ch1's running chain
CUT_X, CUT_H = -1.774, 1.05         # ch1's GOLD cut for that chain at ORIGIN (take 2)
ZIP_T = "'a list -> 'b list -> ('a * 'b) list"
UNZIP_T = "('a * 'b) list -> 'a list * 'b list"
MIRROR = "('a * 'b) list"
LET_SRC = "let xs, ys = unzip pairs in"
WAYS = ["greedy", "every way", "faster"]

FLAT = set("dfhiklmnrtuvwxzBDEFHIKLMNPRTUVWXZ1247")   # glyphs that sit exactly on the baseline


# ── helpers ─────────────────────────────────────────────────────────────────────
def baseline(m):
    """y of a text's baseline (a flat-bottomed glyph's bottom); MathTex: its first glyph's."""
    if isinstance(m, MathTex):
        return m[0][0].get_bottom()[1]
    if isinstance(m, Code):
        m = m.text
    s = getattr(m, "text", None)
    if isinstance(s, str):
        for i, ch in enumerate(s):
            if ch in FLAT and i < len(m):
                return m[i].get_bottom()[1]
    return m.get_bottom()[1]


def sit(m, y):
    """Shift m so its baseline is the baseline of a text line whose caps are centred on y."""
    return m.shift((y - CAP / 2 - baseline(m)) * UP)


def line_at(parts, y, x=TEXT_X, buff=0.22):
    """Parts in a row on one baseline, left edge at x, caps centred on y."""
    grp = VGroup(*parts).arrange(RIGHT, buff=buff)
    for p in parts:
        sit(p, y)
    grp.shift((x - grp.get_left()[0]) * RIGHT)
    return grp


def prose(text, **kw):
    """A text line; the function names take and drop in YELLOW mono."""
    names = [w for w in ("take", "drop") if w in text]
    t2c = {**{w: YELLOW for w in names}, **kw.pop("t2c", {})}
    return T(text, size=TEXT_SIZE, t2c=t2c, t2f={w: MONO for w in names}, **kw)


def cost(tex):
    return MathTex(tex, font_size=COST_SIZE, color=GOLD)


def multiply_opacity(mob, k):
    """Scale every part's opacity by k in place (keeps the dims inside an icon)."""
    for leaf in mob.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k, family=False)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k, family=False)
    return mob


def faded(mob, k):
    return multiply_opacity(mob.copy(), k)


def step_back(row):
    return Transform(row, faded(row, SAID))


def coin(v, r=0.42, size=34):
    """ch1's coin: GOLD disc (stroke 4, fill 0.15) with its label in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=size, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def tint(code):
    """ch3's type colours: 'a PINK, 'b PURPLE."""
    for k in range(code.src.count("'a")):
        code.find("'a", nth=k).set_color(PINK)
    for k in range(code.src.count("'b")):
        code.find("'b", nth=k).set_color(PURPLE)
    return code


def chain_icon(y, cut=False):
    """ch1's chain, icon size (3.0 wide), centred at (ICON_X, y); with ch1's GOLD cut if asked."""
    ch = ConsChain(CHAIN)
    k = ICON_W / ch.width
    ch.scale(k).move_to([ICON_X, y, 0])
    if not cut:
        return ch, k
    x = ICON_X + k * CUT_X
    line = DashedLine([x, y - k * CUT_H, 0], [x, y + k * CUT_H, 0], dash_length=0.06)
    return ch, line.set_stroke(GOLD, 4)


def part_box(cells):
    return SurroundingRectangle(VGroup(*cells), buff=0.06)


# ── s4's three numbered steps, small ────────────────────────────────────────────
def steps_icon(y):
    """s4's step cards, small: DIM-outlined cards (corner 0.18 -> 0.1, stroke 2.5), each with
    its GOLD number ring (stroke 2.5) and digit; the arrows between them YELLOW (as after {name})."""
    frames, rings, nums = [], [], []
    for i in range(3):
        f = RoundedRectangle(corner_radius=0.1, width=0.8, height=0.66).set_stroke(DIM, 2.5)
        ring = Circle(radius=0.22).set_stroke(GOLD, 2.5)
        num = T(str(i + 1), size=28, color=GOLD).move_to(ring)
        frames.append(f)
        rings.append(ring)
        nums.append(num)
    VGroup(*frames).arrange(RIGHT, buff=0.3).move_to([ICON_X, y, 0])
    for f, r, n in zip(frames, rings, nums):
        r.move_to(f)
        n.move_to(f)
    arrows = [Arrow(a.get_right(), b.get_left(), buff=0.04, stroke_width=3, color=YELLOW,
                    max_tip_length_to_length_ratio=0.5, tip_length=0.1)
              for a, b in zip(frames, frames[1:])]
    return frames, rings, nums, arrows


class LectureRecap(NarratedScene):
    def construct(self):
        self.page_one()
        self.page_two()
        self.next_time()
        # End card: next lecture, the six exercises, held under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── c6.recap.1: take / drop, linear search, equality ──────────────────────────
    def page_one(self):
        self.title = title = T("Recap", size=48).move_to([0, TITLE_Y, 0])

        # row 1: the chain with the cut; take copies, drop skips; O(i) time, drop O(1) space
        ch1, cut = chain_icon(P1_TD_ICON, cut=True)
        a1, a2 = prose("take copies,"), prose("drop skips")
        line_at([a1, a2], P1_TD[0])
        b1, b2, b3 = prose("both"), cost("O(i)"), prose("time;")
        b4, b5, b6 = prose("only drop"), cost("O(1)"), prose("space")
        line_at([b1, b2, b3, b4, b5, b6], P1_TD[1])
        b4.shift(0.15 * RIGHT)
        b5.shift(0.15 * RIGHT)
        b6.shift(0.15 * RIGHT)
        row1 = VGroup(ch1, cut, a1, a2, b1, b2, b3, b4, b5, b6)

        # row 2: the same chain, ch2's GOLD marker stepping along it; linear search: O(n)
        ch2, k = chain_icon(P1_S)
        ptr = marker(GOLD, scale=0.45 * k)
        ptr.move_to(ch2.cells[0].box.get_top() + UP * (0.38 * k + ptr.height / 2))
        s1, s2 = prose("linear search:"), cost("O(n)")
        line_at([s1, s2], P1_S)
        row2 = VGroup(ch2, ptr, s1, s2)

        # row 3: GREEN = beside a RED "functions" chip
        eq = Mono("=", size=56, color=GREEN)
        chip_t = T("functions", size=30, color=RED)
        chip_b = RoundedRectangle(corner_radius=0.2, width=chip_t.width + 0.36, height=0.52)
        chip_b.set_stroke(RED, 2.5).set_fill(RED, opacity=0.12)
        chip_t.move_to(chip_b)
        chip = VGroup(chip_b, chip_t)
        VGroup(eq, chip).arrange(RIGHT, buff=0.4).move_to([ICON_X, P1_EQ_ICON, 0])
        e1 = Mono("=", size=TEXT_SIZE, color=GREEN)
        e2 = prose("works on numbers, strings, lists, pairs")
        line_at([e1, e2], P1_EQ[0])
        e1.set_y(P1_EQ[0] - 0.03)                   # "=" floats on the maths axis
        e3 = prose("but functions raise an exception", t2c={"functions": RED, "exception": RED})
        line_at([e3], P1_EQ[1])
        self.row3 = row3 = VGroup(eq, chip, e1, e2, e3)

        with self.say("c6.recap.1") as c:
            # "That's the end of lecture four, so let's look back."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=1.0)

            # "Take copies the front of a list, ..."
            c.wait_until("takedrop")
            self.play(FadeIn(ch1, shift=UP_S), time_span(GrowFromCenter(cut), 0.5, 1.3),
                      FadeIn(a1, shift=UP_S), run_time=1.3)
            # "... and drop skips over it."
            c.wait_until("and drop")
            self.play(FadeIn(a2, shift=UP_S),
                      FlashAround(part_box([*ch1.cells[2:], ch1.nil]), color=YELLOW, time_width=1.5,
                                  buff=0.04), run_time=1.2)

            # "Both need time in proportion to how far they go, ..."
            c.wait_until("Both need time")
            self.play(*[FadeIn(m, shift=UP_S) for m in (b1, b2, b3)], run_time=1.0)
            # "... but only drop runs in constant space."
            c.wait_until("only drop")
            self.play(*[FadeIn(m, shift=UP_S) for m in (b4, b5, b6)], run_time=1.0)
            settle(self, row1)

            # "Searching a list means looking at one element at a time, ..."
            c.wait_until("search")
            self.play(step_back(row1), FadeIn(ch2, shift=UP_S), FadeIn(ptr, shift=UP_S),
                      FadeIn(s1, shift=UP_S), run_time=1.2)
            c.wait_until("one element")
            for i, rt in zip(range(1, 5), (0.6, 0.45, 0.4, 0.35)):
                self.play(ptr.animate.set_x(ch2.cells[i].box.get_x()), run_time=rt)
            # "... so it costs big O of en."
            c.wait_until("costs")
            self.play(FadeIn(s2, shift=UP_S), FlashUnder(s1, color=GOLD), run_time=1.0)
            settle(self, row2)

            # "Polymorphic equality works on numbers, strings, and lists or pairs of them, ..."
            c.wait_until("equal")
            self.play(step_back(row2), FadeIn(eq, shift=UP_S), FadeIn(e1, shift=UP_S),
                      FadeIn(e2, shift=UP_S), run_time=1.2)
            # "... but comparing functions raises an exception."
            c.wait_until("comparing functions")
            self.play(FadeIn(chip, shift=UP_S), FadeIn(e3, shift=UP_S), run_time=1.0)
            settle(self, row3)

    # ── c6.recap.2: zip and unzip, let patterns, three ways to make change ───────────
    def page_two(self):
        # row Z: ch3's mirror; the names in the icon column, the types beside them
        zt, ut = tint(Code(ZIP_T, size=TYPE_SIZE)), tint(Code(UNZIP_T, size=TYPE_SIZE))
        zn, un = Mono("zip", size=32, color=YELLOW), Mono("unzip", size=32, color=YELLOW)
        for name, typ, y in ((zn, zt, P2_Z[0]), (un, ut, P2_Z[1])):
            line_at([typ], y)
            name.move_to([ICON_X, 0, 0])
            name.shift((baseline(typ) - baseline(name)) * UP)
        zbox = token_box(zt.find(MIRROR), zt)
        ubox = token_box(ut.find(MIRROR), ut)
        rowZ = VGroup(zbox, ubox, zn, zt, un, ut)

        # row P: ch3's `let P = E`, beside unzip's let
        lpe = Code("let P = E", size=36)
        lpe.find("P").set_color(YELLOW)
        lpe.find("E").set_color(BLUE)
        lpe.move_to([ICON_X, 0, 0])
        let = Code(LET_SRC, size=LET_SIZE)
        let.find("unzip").set_color(YELLOW)
        line_at([let], P2_P)
        sit(lpe, P2_P)
        pbox = token_box(let.line(0), let)

        # row C: `change`; three numbered GOLD coin discs, labelled
        cname = Mono("change", size=34, color=YELLOW).move_to([ICON_X, 0, 0])
        sit(cname, P2_C)
        discs = [coin(i + 1, r=0.3, size=30) for i in range(3)]
        labels = [prose(w) for w in WAYS]
        pairs = [VGroup(d, lab).arrange(RIGHT, buff=0.18) for d, lab in zip(discs, labels)]
        VGroup(*pairs).arrange(RIGHT, buff=0.6).move_to([TEXT_X, P2_C, 0], aligned_edge=LEFT)
        for d, lab in zip(discs, labels):
            sit(lab, P2_C)
            d.move_to([d.get_x(), P2_C, 0])
        stuck = cross_mark(r=0.12).set_stroke(RED, 6).move_to(discs[0].get_corner(UR) + 0.02 * UR)

        # row R: s4's three numbered steps, born from the discs; stepwise refinement
        frames, rings, nums, arrows = steps_icon(P2_R_ICON)
        r1 = prose("stepwise refinement", color=YELLOW)
        line_at([r1], P2_R[0])
        r2 = prose("start simple, add efficiency last", t2c={"efficiency": GOLD})
        line_at([r2], P2_R[1])
        self.rowR = VGroup(*frames, *rings, *nums, *arrows, r1, r2)

        with self.say("c6.recap.2") as c:
            # "Zip pairs up two lists, ..."  (page 1 sweeps away; its last row lingers, dimmed)
            sweep_clear(self, step_back(self.row3),
                        time_span(FadeIn(zn, shift=UP_S), 0.5, 1.3), time_span(FadeIn(zt, shift=UP_S), 0.5, 1.3),
                        keep=[self.title, self.row3], run_time=1.3)
            # "... and unzip splits the pairs apart again."  The mirror: the shared ('a * 'b) list.
            c.wait_until("and unzip")
            self.play(FadeIn(un, shift=UP_S), FadeIn(ut, shift=UP_S),
                      time_span(FadeIn(zbox), 0.6, 1.4), time_span(FadeIn(ubox), 0.6, 1.4), run_time=1.4)
            settle(self, rowZ)

            # "A let can match a pattern, ..."
            c.wait_until("pattern")
            self.play(step_back(rowZ), FadeIn(lpe, shift=UP_S),
                      FadeIn(let, shift=UP_S), time_span(FadeIn(pbox), 0.5, 1.3), run_time=1.3)
            # "... and name every part of it at once."  The box slides onto the pattern.
            c.wait_until("name every part")
            xs, ys = let.find("xs"), let.find("ys")
            self.play(Transform(pbox, token_box(let.find("xs, ys"), let)), FadeOut(self.row3),
                      time_span(FlashUnder(VGroup(*xs), color=YELLOW), 0.5, 1.5),
                      time_span(FlashUnder(VGroup(*ys), color=YELLOW), 0.7, 1.7), run_time=1.7)
            rowP = VGroup(pbox, lpe, let)
            settle(self, rowP)

            # "We made change three ways."
            c.wait_until("change")
            self.play(step_back(rowP), FadeIn(cname, shift=UP_S), run_time=1.0)
            # "Greedy, which can get stuck."
            c.wait_until("Greedy")
            self.play(FadeIn(discs[0], scale=0.6), FadeIn(labels[0], shift=UP_S), run_time=1.0)
            c.wait_until("can get stuck")
            self.play(GrowFromCenter(stuck), run_time=0.7)
            # "Then every way."
            c.wait_until("Then every way")
            self.play(FadeIn(discs[1], scale=0.6), FadeIn(labels[1], shift=UP_S), run_time=1.0)
            # "Then every way, faster, with two accumulators."
            c.wait_until("Then every way", nth=1)
            self.play(FadeIn(discs[2], scale=0.6), FadeIn(labels[2], shift=UP_S), run_time=1.0)
            rowC = VGroup(cname, *discs, *labels, stuck)
            settle(self, rowC)

            # "And building it up like that is stepwise refinement."  The discs become s4's steps.
            c.wait_until("refine")
            self.play(*[TransformFromCopy(d[0], r) for d, r in zip(discs, rings)],
                      *[TransformFromCopy(d[1], n) for d, n in zip(discs, nums)],
                      *[time_span(Create(f), 0.5, 1.5) for f in frames],
                      *[time_span(GrowArrow(a), 1.0, 1.6) for a in arrows],
                      time_span(FadeIn(r1, shift=UP_S), 0.4, 1.4), time_span(step_back(rowC), 0.8, 1.8),
                      run_time=1.8)
            # "Start simple, and add efficiency last."
            c.wait_until("Start simple")
            self.play(FadeIn(r2, shift=UP_S), run_time=1.0)
            settle(self, self.rowR)

    # ── c6.recap.3: next lecture, then the exercises (the end card) ──────────────────
    def next_time(self):
        hd1, hd2 = T("Next lecture:", size=48, color=DIM), T("Sorting", size=48, color=YELLOW)
        head = VGroup(hd1, hd2).arrange(RIGHT, buff=0.25)
        hd2.shift((baseline(hd1) - baseline(hd2)) * UP)
        head.move_to([0, TITLE_Y, 0])
        self.head = head

        # left: a sorted row, a GOLD brace that halves, O(log n)
        boxes = VGroup(*[Square(SORT_BOX).set_stroke(BLUE, 3) for _ in SORTED]).arrange(RIGHT, buff=0)
        boxes.move_to([0, PIC_Y, 0])           # centred while it is the only picture
        vals = [Mono(str(v), size=28).move_to(b) for v, b in zip(SORTED, boxes)]

        def brace(lo, hi):
            return Brace(VGroup(*boxes[lo:hi]), DOWN, buff=0.12, color=GOLD)

        br = brace(0, len(SORTED))
        logn = MathTex(r"O(\log n)", font_size=48, color=GOLD).move_to([0, PIC_LABEL_Y, 0])

        # right: ch1's chain, the GOLD cut, the halves take and drop
        ch = ConsChain(CHAIN).scale(MERGE_K).move_to([MERGE_X, PIC_Y, 0])
        cx = MERGE_X + MERGE_K * CUT_X
        cut = DashedLine([cx, PIC_Y - MERGE_K * CUT_H, 0], [cx, PIC_Y + MERGE_K * CUT_H, 0],
                         dash_length=0.08).set_stroke(GOLD, 5)
        left = [ch.cells[0], ch.arrows[0], ch.cells[1]]
        right = [ch.cells[2], ch.arrows[2], ch.cells[3], ch.arrows[3], ch.cells[4], ch.arrows[4], ch.nil]
        new_nil = Nil().scale(MERGE_K)
        new_nil.move_to(ch.cells[2].box.get_left() + LEFT * SPLIT_L, aligned_edge=LEFT)
        new_nil.shift((ch.cells[1].box.get_y() - new_nil.get_y()) * UP)
        ghost_1 = ch.cells[1].copy().shift(LEFT * SPLIT_L)
        new_arrow = link(ghost_1, new_nil)
        take_l = Mono("take", size=32, color=YELLOW)
        drop_l = Mono("drop", size=32, color=YELLOW)
        top_y = ch.get_top()[1] + 0.42
        take_x = (ch.cells[0].get_left()[0] - SPLIT_L + new_nil.get_right()[0]) / 2
        drop_x = (ch.cells[2].get_left()[0] + ch.nil.get_right()[0]) / 2 + SPLIT_R
        take_l.move_to([take_x, top_y, 0])
        drop_l.move_to([drop_x, top_y, 0])
        msort = T("merge sort", size=36).move_to([(take_x + drop_x) / 2, PIC_LABEL_Y, 0])

        ex = six_cards()
        ex.cards.scale(EX_K)
        ex.cards.shift(UP * (EX_TOP - ex.cards.get_top()[1]))
        ex.note.set_y(NOTE_Y)

        with self.say("c6.recap.3") as c:
            # "Next lecture is about sorting."  The recap sweeps away; its last row leaves last.
            sweep_clear(self, time_span(FadeIn(head, shift=0.3 * DOWN), 0.4, 1.3), keep=[self.rowR],
                        run_time=1.3)

            # "A sorted collection can be searched in big O of log en."
            c.wait_until("fast")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.08),
                      LaggedStart(*[FadeIn(v) for v in vals], lag_ratio=0.08),
                      time_span(GrowFromCenter(br), 0.6, 1.1), run_time=1.1)
            c.wait_until("searched")
            for n, ((lo, hi), rt) in enumerate(zip(HALVES, (0.5, 0.4, 0.7))):
                out = [i for i in range(len(SORTED)) if not lo <= i < hi and boxes[i].get_stroke_opacity() > 0.5]
                extra = [time_span(FadeIn(logn, shift=UP_S), 0.1, 0.8)] if n == 2 else []
                if n == 0:
                    extra = [FadeOut(self.rowR)]
                self.play(Transform(br, brace(lo, hi)),
                          *[boxes[i].animate.set_stroke(opacity=DIMMED) for i in out],
                          *[vals[i].animate.set_opacity(DIMMED) for i in out], *extra, run_time=rt)

            # "And one way to sort, called merge sort, ..."
            # (the sorted row slides left to make room)
            c.wait_until("merge")
            self.play(*[m.animate.shift(SORT_X * RIGHT) for m in (*boxes, *vals, br, logn)],
                      time_span(FadeIn(ch, shift=UP_S), 0.4, 1.3), time_span(GrowFromCenter(cut), 0.9, 1.3),
                      run_time=1.3)
            c.wait_until("merge sort")
            self.play(FadeIn(msort, shift=UP_S), run_time=0.8)
            # "... splits its list in two ..."
            c.wait_until("splits")
            self.play(*[m.animate.shift(LEFT * SPLIT_L) for m in left],
                      *[m.animate.shift(RIGHT * SPLIT_R) for m in right],
                      FadeOut(ch.arrows[1]), time_span(FadeOut(cut), 0.6, 1.3),
                      time_span(FadeIn(new_nil), 0.6, 1.3), time_span(GrowArrow(new_arrow), 0.6, 1.3),
                      time_span(FadeIn(take_l, shift=0.2 * DOWN), 0.7, 1.4),
                      time_span(FadeIn(drop_l, shift=0.2 * DOWN), 0.7, 1.4), run_time=1.4)
            # "... with take and drop."
            c.wait_until("with take")
            self.play(FlashUnder(take_l, color=YELLOW), time_span(FlashUnder(drop_l, color=YELLOW), 0.3, 1.0),
                      run_time=1.0)

            pics = VGroup(boxes, *vals, br, logn, *left, new_arrow, new_nil, *right, take_l, drop_l, msort)
            settle(self, pics)

            # "But first, try the six exercises."  The pictures step back; the cards come in below.
            c.wait_until("bonus")
            self.play(step_back(pics), LaggedStart(*[FadeIn(k, shift=UP_S) for k in ex.cards], lag_ratio=0.2),
                      run_time=1.8)
            # "When you're ready, the bonus chapter walks through every solution."
            c.wait_until("the bonus chapter")
            self.play(FadeIn(ex.note, shift=UP_S), run_time=1.0)
            settle(self, ex)
            # "See you there."
