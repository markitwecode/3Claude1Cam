"""Chapter 1, scene 2: what sorting is for (five uses, then Knuth and Sedgewick). Clips c1.why.1 – c1.why.4.

Layout: a column of five slots down the left edge (header "Why sort?"), each filled with an icon
and a label on its mark; every use plays its example on the right (centred at RX) and then shrinks
into its slot. On {knuth} the column dims and the book covers take the right side.
Opens on scene 1's two YELLOW question lines (Q_* constants below) and clears them on {why}.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# Scene 1's closing shot, as scene 1 reported it: both T(..., 44, YELLOW), centred at x = 0.
Q_SIZE = 44
Q1_TEXT = "How many comparisons does sorting need?"
Q2_TEXT = "Could a cleverer method need fewer?"
Q1_POS = np.array([0.0, 0.45, 0.0])
Q2_POS = np.array([0.0, -0.40, 0.0])

RX = 2.4                                   # centre x of the example area
COL_X = -6.1                               # slot centre x
SLOT = 0.85                                # slot frame side
SLOT_Y = [2.2, 0.95, -0.3, -1.55, -2.8]
LABEL_X = -5.45                            # left edge of the slot labels
LABELS = ["search", "merging", "duplicates", "inverting tables", "graphics"]


# ---------------------------------------------------------------- icons (each fits in 0.65 x 0.65)
def magnifier(r=0.19, color=YELLOW, width=4, handle=0.22, hwidth=7):
    lens = Circle(radius=r).set_stroke(color, width)
    d = np.array([np.cos(-PI / 4), np.sin(-PI / 4), 0.0])
    bar = Line(r * d, (r + handle) * d).set_stroke(color, hwidth)
    return VGroup(lens, bar)


def icon_search():
    m = magnifier()
    return m.move_to(ORIGIN)


def icon_merge():
    def sq(x, y, op=1.0):
        return Square(0.12).set_stroke(width=0).set_fill(GOLD, op).move_to([x, y, 0])
    top = [sq(x, 0.16) for x in (-0.29, -0.14, 0.14, 0.29)]
    bot = [sq(x, -0.18) for x in (-0.225, -0.075, 0.075, 0.225)]
    return VGroup(*top, *bot)


def icon_dups():
    def tile(x):
        return (RoundedRectangle(corner_radius=0.05, width=0.24, height=0.36)
                .set_stroke(YELLOW, 3).set_fill(YELLOW, 0.35).move_to([x, 0, 0]))
    return VGroup(tile(-0.15), tile(0.15))


def icon_table():
    box = Rectangle(width=0.6, height=0.48).set_stroke(BLUE, 3)
    h1 = Line([-0.3, 0.08, 0], [0.3, 0.08, 0]).set_stroke(BLUE, 2)
    h2 = Line([-0.3, -0.08, 0], [0.3, -0.08, 0]).set_stroke(BLUE, 2)
    v = Line([-0.1, 0.24, 0], [-0.1, -0.24, 0]).set_stroke(BLUE, 2)
    return VGroup(box, h1, h2, v)


def icon_graphics():
    sq = Square(0.3).set_stroke(BG, 2).set_fill(BLUE, 1).move_to([-0.13, 0.11, 0])
    ci = Circle(radius=0.15).set_stroke(BG, 2).set_fill(TEAL, 1).move_to([0.02, -0.03, 0])
    tr = Triangle().scale(0.2).set_stroke(BG, 2).set_fill(YELLOW, 1).move_to([0.15, -0.1, 0])
    return VGroup(sq, ci, tr)


# ---------------------------------------------------------------- example pieces
def num_box(n, side=0.85, size=40):
    box = Square(side).set_stroke(BLUE, 3)
    lab = value_label(str(n), size, GOLD).move_to(box)
    return VGroup(box, lab)


def name_tile(s):
    box = (RoundedRectangle(corner_radius=0.14, width=1.35, height=0.8)
           .set_stroke(YELLOW, 3).set_fill(YELLOW, 0.12))
    lab = T(s, 34, YELLOW).move_to(box)
    return VGroup(box, lab)


def tag(text, color=FG, size=30):
    t = T(text, size, color)
    pill = SurroundingRectangle(t, buff=0.14, corner_radius=0.16).set_stroke(DIM, 2)
    return VGroup(pill, t)


def book(color, top_lines, author_lines, width=3.6, height=5.0):
    cover = (RoundedRectangle(corner_radius=0.1, width=width, height=height)
             .set_stroke(color, 3).set_fill(color, 0.12))
    spine = Line(cover.get_corner(UL) + 0.3 * RIGHT, cover.get_corner(DL) + 0.3 * RIGHT).set_stroke(color, 2)
    top = top_lines.move_to(cover.get_top() + 0.15 * RIGHT, aligned_edge=UP).shift(0.4 * DOWN)
    author = author_lines.move_to(cover.get_bottom() + 0.15 * RIGHT, aligned_edge=DOWN).shift(0.4 * UP)
    return VGroup(cover, spine, top, author)


def first_cue(c, *names):
    for n in names:
        try:
            c.at(n)
            return n
        except KeyError:
            pass
    return None


class WhySort(NarratedScene):
    def construct(self):
        # scene 1's closing shot
        self.q1 = T(Q1_TEXT, Q_SIZE, YELLOW).move_to(Q1_POS)
        self.q2 = T(Q2_TEXT, Q_SIZE, YELLOW).move_to(Q2_POS)
        self.play(FadeIn(self.q1), FadeIn(self.q2), run_time=0.5)
        self.wait(0.2)

        self.build_column()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()

        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------ column
    def build_column(self):
        self.title = T("Why sort?", 56)
        self.frames, self.nums, self.icons, self.labels = [], [], [], []
        makers = [icon_search, icon_merge, icon_dups, icon_table, icon_graphics]
        for i, y in enumerate(SLOT_Y):
            fr = RoundedRectangle(corner_radius=0.12, width=SLOT, height=SLOT).set_stroke(DIM, 2)
            fr.move_to([COL_X, y, 0])
            self.frames.append(fr)
            self.nums.append(T(str(i + 1), 30, DIM).move_to(fr))
            self.icons.append(makers[i]().move_to(fr))
            lab = T(LABELS[i], 30)
            lab.move_to([LABEL_X, y, 0], aligned_edge=LEFT)
            self.labels.append(lab)

    def slot_point(self, i):
        return self.frames[i].get_center()

    def fill_slot(self, i):
        return [FadeOut(self.nums[i], scale=0.5),
                FadeIn(self.icons[i], scale=0.5),
                FadeIn(self.labels[i], shift=0.2 * DOWN)]

    def shrink(self, parts, i, start=0.0, end=0.9):
        p = self.slot_point(i)
        return [time_span(FadeOut(m, target_position=p, scale=0.1), start, end) for m in parts]

    # ------------------------------------------------------------ clip 1: why, search, merging
    def clip1(self):
        title = self.title
        with self.say("c1.why.1") as c:
            self.play(time_span(FadeOut(self.q1, shift=0.4 * UP), 0.0, 0.8), time_span(FadeOut(self.q2, shift=0.4 * UP), 0.0, 0.8),
                      time_span(FadeIn(title, shift=0.3 * UP), 0.6, 1.4), run_time=1.4)
            c.wait_until("The notes list five uses")

            title.generate_target()
            title.target.scale(40 / 56)
            title.target.move_to([COL_X - SLOT / 2, 3.25, 0], aligned_edge=LEFT)
            anims = [MoveToTarget(title)]
            for i in range(5):
                s = 0.35 + 0.15 * i
                anims += [time_span(FadeIn(self.frames[i], shift=0.2 * RIGHT), s, s + 0.7),
                          time_span(FadeIn(self.nums[i], shift=0.2 * RIGHT), s, s + 0.7)]
            self.play(*anims, run_time=1.6)
            c.wait_until("search")

            # 1. search: a magnifier over a sorted row
            row = VGroup(*[num_box(n) for n in [3, 8, 12, 15, 21, 30, 34, 42]]).arrange(RIGHT, buff=0.1)
            row.move_to([RX, 0.3, 0])
            self.play(*self.fill_slot(0), time_span(FadeIn(row, lag_ratio=0.1), 0.3, 1.4), run_time=1.4)
            c.wait_until("Sorted data")

            mag = magnifier(r=0.55, width=6, handle=0.6, hwidth=12)
            mag.shift(row[3].get_center() - mag[0].get_center())
            self.play(FadeIn(mag, scale=1.3), run_time=0.9)
            c.wait_until("searched")
            self.play(mag.animate.shift(row[5].get_center() - row[3].get_center()),
                      time_span(row[5][0].animate.set_fill(YELLOW, 0.3), 0.6, 1.2), time_span(row[5][1].animate.set_color(YELLOW), 0.6, 1.2), run_time=1.2)
            c.wait_until("next scene")
            nxt = T("next scene", 30, DIM).move_to([RX, -1.45, 0])
            self.play(FadeIn(nxt, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("merge")

            # 2. merging: 2 7 8 and 3 5 9 interleave into one row
            self.play(*self.fill_slot(1), run_time=1.0)
            c.wait_until("Two sorted files")
            ra = VGroup(*[num_box(n) for n in [2, 7, 8]]).arrange(RIGHT, buff=0.15).move_to([RX - 2.1, 1.0, 0])
            rb = VGroup(*[num_box(n) for n in [3, 5, 9]]).arrange(RIGHT, buff=0.15).move_to([RX + 2.1, 1.0, 0])
            outs = VGroup(*[Square(0.85).set_stroke(DIM, 2) for _ in range(6)]).arrange(RIGHT, buff=0.15)
            outs.move_to([RX, -0.9, 0])
            self.play(*self.shrink([row, mag, nxt], 0),
                      time_span(FadeIn(ra, lag_ratio=0.15), 0.5, 1.3),
                      time_span(FadeIn(rb, lag_ratio=0.15), 0.6, 1.4),
                      time_span(FadeIn(outs, lag_ratio=0.1), 0.8, 1.6), run_time=1.6)

            moves = [(ra[0], 0), (rb[0], 1), (rb[1], 2), (ra[1], 3), (ra[2], 4), (rb[2], 5)]
            weights = [1.6, 1.2, 1.0, 1.0, 1.0, 1.0]
            hold = 0.12
            budget = c.until("part five", floor=3.0) - 0.15 - hold * len(moves)
            for (m, k), w in zip(moves, weights):
                rt = max(0.4, min(1.2, budget * w / sum(weights)))
                self.play(m.animate.move_to(outs[k]), run_time=rt)
                self.wait(hold)
            c.wait_until("part five")
            p5 = T("Part 5", 30, DIM).move_to([RX, -2.0, 0])
            self.play(FadeIn(p5, shift=0.2 * DOWN), run_time=0.8)
        self.merge_parts = [ra, rb, outs, p5]

    # ------------------------------------------------------------ clip 2: duplicates
    def clip2(self):
        with self.say("c1.why.2") as c:
            self.play(*self.fill_slot(2), run_time=1.0)
            c.wait_until("Here's a list of names")

            names = ["Cleo", "Amy", "Dee", "Bob", "Amy"]
            tiles = VGroup(*[name_tile(s) for s in names]).arrange(RIGHT, buff=0.2).move_to([RX, 0.3, 0])
            spots = [t.get_center() for t in tiles]
            self.play(*self.shrink(self.merge_parts, 1),
                      time_span(FadeIn(tiles, lag_ratio=0.2), 0.4, 1.7), run_time=1.7)
            c.wait_until("sorted")

            dest = [3, 0, 4, 2, 1]                       # Cleo Amy Dee Bob Amy -> Amy Amy Bob Cleo Dee
            arcs = [PI / 2, PI / 2, PI / 2, PI / 2, 0.75 * PI]
            self.play(*[tiles[i].animate(path_arc=arcs[i]).move_to(spots[dest[i]]) for i in range(5)],
                      run_time=1.8)
            c.wait_until("pass")

            order = [tiles[1], tiles[4], tiles[3], tiles[0], tiles[2]]

            def pair_brace(k):
                return span_brace(order[k].get_corner(DL), order[k + 1].get_corner(DR),
                                  direction=DOWN, color=FG)

            br = pair_brace(0)
            self.play(GrowFromCenter(br), run_time=0.7)
            self.play(*flash([VGroup(order[0], order[1])], color=GREEN, run_time=1.2, time_width=1.5),
                      order[0].animate.set_color(GREEN), order[1].animate.set_color(GREEN), run_time=1.2)
            self.wait(0.25)
            for k in (1, 2, 3):
                self.play(Transform(br, pair_brace(k)), run_time=0.5)
                self.wait(0.1)
        self.dup_parts = [tiles, br]

    # ------------------------------------------------------------ clip 3: inverting tables
    def clip3(self):
        with self.say("c1.why.3") as c:
            self.play(*self.fill_slot(3), run_time=1.0)
            c.wait_until("A telephone directory")

            entries = [("Ada", "52", "Mill Road"), ("Ben", "17", "Tenison Road"),
                       ("Cal", "38", "Hills Road"), ("Dee", "24", "Mill Road")]
            x0 = RX - 2.95
            cols = [x0, x0 + 1.4, x0 + 3.2]
            ys = [1.0 - 0.72 * k for k in range(4)]
            heads = VGroup(*[T(h, 30, DIM).move_to([cols[j], 1.8, 0], aligned_edge=LEFT)
                             for j, h in enumerate(["name", "number", "street"])])
            rows = []
            for k, (nm, no, st) in enumerate(entries):
                parts = [T(nm, 36, YELLOW), T(no, 36, GOLD), T(st, 36)]
                for j, p in enumerate(parts):
                    p.move_to([cols[j], ys[k], 0], aligned_edge=LEFT)
                rows.append(VGroup(*parts))
            table = VGroup(heads, *rows)
            ul = underline(heads[0], YELLOW)
            self.play(*self.shrink(self.dup_parts, 2),
                      time_span(FadeIn(table, lag_ratio=0.15), 0.4, 1.7),
                      time_span(Create(ul), 1.3, 1.9), run_time=1.9)
            c.wait_until("number")

            by_number = [3, 0, 2, 1]                     # Ben 17, Dee 24, Cal 38, Ada 52
            self.play(*[rows[i].animate.set_y(ys[by_number[i]]) for i in range(4)],
                      Transform(ul, underline(heads[1], YELLOW)), run_time=1.6)
            c.wait_until("police")
            police = tag("police").next_to(heads[1], UP, buff=0.3)
            self.play(FadeIn(police, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("street")

            by_street = [1, 3, 0, 2]                     # Cal Hills, Ada Mill, Dee Mill, Ben Tenison
            self.play(*[rows[i].animate.set_y(ys[by_street[i]]) for i in range(4)],
                      Transform(ul, underline(heads[2], YELLOW)), run_time=1.6)
            junk_cue = first_cue(c, "junk-mail firms", "junk mail firms", "firms")
            c.wait_until(junk_cue)
            junk = tag("junk mail").next_to(heads[2], UP, buff=0.3)
            self.play(ReplacementTransform(police, junk), run_time=1.0)
            c.wait_until("same")

            cap = T("same information, different applications", 30).move_to([RX, -2.1, 0])
            self.play(FadeIn(cap, shift=0.2 * UP), run_time=1.0)
        self.table_parts = [table, ul, junk, cap]

    # ------------------------------------------------------------ clip 4: graphics, then the books
    def clip4(self):
        with self.say("c1.why.4") as c:
            self.play(*self.fill_slot(4), run_time=1.0)
            c.wait_until("One example")
            self.play(*self.shrink(self.table_parts, 3, 0.0, 1.0), run_time=1.0)

            far = Square(1.9).set_stroke(BG, 6).set_fill(BLUE, 1).move_to([RX - 1.4, 0.8, 0])
            mid = Circle(radius=1.2).set_stroke(BG, 6).set_fill(TEAL, 1).move_to([RX - 0.2, 0.0, 0])
            near = (Triangle().scale(1.73).set_stroke(BG, 6).set_fill(YELLOW, 1)
                    .move_to([RX + 1.25, -0.45, 0]))
            c.wait_until("far shapes")
            self.play(FadeIn(far, scale=0.8), run_time=0.9)
            self.play(FadeIn(mid, scale=0.8), run_time=0.9)
            c.wait_until("near ones")
            self.play(FadeIn(near, scale=0.8), run_time=0.9)
            c.wait_until("knuth")

            column = [self.title, *self.frames, *self.icons, *self.labels]
            self.play(*self.shrink([far, mid, near], 4, 0.0, 1.1),
                      *set_alpha(column, DIMMED), run_time=1.2)

            k_top = VGroup(VGroup(T("The Art of", 32), T("Computer", 32), T("Programming", 32))
                           .arrange(DOWN, buff=0.12),
                           Line(0.9 * LEFT, 0.9 * RIGHT).set_stroke(DIM, 2),
                           T("Vol. 3", 30, GOLD),
                           VGroup(T("Sorting and", 30), T("Searching", 30)).arrange(DOWN, buff=0.1)
                           ).arrange(DOWN, buff=0.22)
            k_author = T("Donald Knuth", 30, YELLOW)
            knuth = book(BLUE, k_top, k_author).move_to([RX, 0.1, 0])
            self.play(FadeIn(knuth, shift=0.3 * UP), run_time=1.2)
            c.wait_until("Donald")
            self.play(FlashAround(k_author, run_time=1.5, time_width=1.5))
            c.wait_until("whole volume")
            self.play(FlashAround(VGroup(k_top[2], k_top[3]), run_time=1.6, time_width=1.5))
            c.wait_until("sedgewick")

            s_top = VGroup(T("Algorithms", 40), Line(0.9 * LEFT, 0.9 * RIGHT).set_stroke(DIM, 2)).arrange(DOWN, buff=0.3)
            s_author = VGroup(T("Robert", 30, YELLOW), T("Sedgewick", 30, YELLOW)).arrange(DOWN, buff=0.1)
            sedge = book(PURPLE, s_top, s_author).move_to([RX + 1.9, 0.1, 0])
            self.play(knuth.animate.move_to([RX - 1.9, 0.1, 0]),
                      time_span(FadeIn(sedge, shift=0.3 * LEFT), 0.3, 1.3), run_time=1.3)
