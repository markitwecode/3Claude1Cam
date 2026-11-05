"""Chapter 6, scene 3: radix sort, sorting without comparing. Clips c6.radix.1 – c6.radix.5.

Layout: top band = "radix sort" title (centre), GOLD O(n) (left), ch1 s5's boxed bound (right),
the "?" between them. Tiles in a row at y = 0.9 (y = 0 in clip 1), captions at y = 0 / -0.75,
ten BLUE buckets along the bottom (ch6 s1's bucket_row, taller so two tiles stack).
Tiles travel on vertical-tangent Bezier paths so they never slide across the row.
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
from lib.style import *  # noqa: E402,F403

from scenes.ch6_s1_hook import bucket_row, num_tile  # noqa: E402

NUMS = [53, 19, 51, 37, 12, 34]
ROW_Y = 0.9
PITCH = 1.4
STACK = 0.78          # tile pitch inside a bucket
TOP_Y = 2.55          # the top band's y


def row_pos(j, y=ROW_Y):
    return np.array([(j - 2.5) * PITCH, y, 0])


def bound_formulas():
    """ch1 s5's boxed 2^C(n) >= n! with C(n) >= log2(n!) under it, scaled 0.7, top right."""
    bf = MathTex("2", "^{C(n)}", r"\ge", "n!", font_size=60, color=YELLOW).move_to([0, -0.85, 0])
    bbox = SurroundingRectangle(bf, color=YELLOW, buff=0.25, stroke_width=4)
    lf = MathTex("C(n)", r"\ge", r"\log_2", "(", "n!", ")", font_size=60).move_to([0, -2.3, 0])
    g = VGroup(bf, bbox, lf).scale(0.7).move_to([4.45, TOP_Y, 0])
    g.bf, g.box, g.lf = bf, bbox, lf
    return g


class RadixScene(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ---------------------------------------------------------------- helpers
    def bucket_target(self, i, k):
        """Centre of a tile resting k-th (0 = floor) in bucket i."""
        return self.row.slot(i) + UP * (0.35 + STACK * k)

    def travel(self, tile, end, h=1.3):
        """Move a tile along a Bezier that leaves and arrives vertically."""
        p0 = tile.get_center()
        d = UP if end[1] > p0[1] else DOWN
        path = CubicBezier(p0, p0 + d * h, end - d * h, end)
        return MoveAlongPath(tile, path)

    # ---------------------------------------------------------------- clip 1
    def clip1(self):
        with self.say("c6.radix.1") as c:
            self.tiles = [num_tile(n) for n in NUMS]
            for j, t in enumerate(self.tiles):
                t.scale(1.4).move_to([(j - 2.5) * PITCH * 1.4, 0.0, 0])
            self.play(*appear(*self.tiles, lag=0.2), run_time=1.6)   # early: the example list, read in clip 2

            c.wait_until("radix")
            self.title = T("radix sort", 52, YELLOW).move_to([0, 3.4, 0])
            self.play(*appear(self.title), run_time=1.0)

            c.wait_until("big O of N")
            self.on = MathTex("O(n)", font_size=72, color=GOLD).move_to([-4.6, TOP_Y, 0])
            self.play(*appear(self.on), run_time=1.0)

            c.wait_until("contradict")
            self.bound = bound_formulas()
            self.play(FadeIn(self.bound.bf, shift=0.2 * DOWN), FadeIn(self.bound.box), run_time=1.2)
            self.play(FadeIn(self.bound.lf, shift=0.2 * DOWN), run_time=1.0)

            c.wait_until("So how can this be faster")
            self.q = MathTex("?", font_size=80, color=YELLOW).move_to([0, TOP_Y, 0])
            self.play(*appear(self.q), run_time=1.0)

    # ---------------------------------------------------------------- clip 2
    def clip2(self):
        tiles = self.tiles
        with self.say("c6.radix.2") as c:
            # {list}: pulse each tile as it is read
            c.wait_until("list")
            self.wait(min(1.0, c.until("buckets", floor=0.1) * 0.15))
            self.play(LaggedStart(*[FlashAround(t, run_time=1.2, time_width=1.5) for t in tiles],
                                  lag_ratio=0.55), run_time=min(5.0, 0.85 * c.until("buckets")))

            # {buckets}
            c.wait_until("buckets")
            row = bucket_row(color=BLUE, height=1.6)
            row.shift(UP * (-3.65 - row.get_bottom()[1]))
            self.row = row
            self.play(*[t.animate.scale(1 / 1.4).move_to(row_pos(j)) for j, t in enumerate(tiles)],
                      *[FadeIn(b) for b in row.buckets],
                      *appear(*row.labels, lag=0.05), run_time=1.8)

            # {units}: last digits YELLOW
            c.wait_until("units")
            self.play(*[t.ones.animate.set_color(YELLOW) for t in tiles], run_time=1.0)

            # deal: 53 and 19 slow, the rest quick
            c.wait_until("goes into bucket three")
            self.play(self.travel(tiles[0], self.bucket_target(3, 0)), run_time=1.4)
            c.wait_until("nineteen into bucket nine")
            self.play(self.travel(tiles[1], self.bucket_target(9, 0)), run_time=1.3)
            c.wait_until("and so on")
            self.play(LaggedStart(*[self.travel(tiles[j], self.bucket_target(NUMS[j] % 10, 0))
                                    for j in (2, 3, 4, 5)], lag_ratio=0.4),
                      run_time=min(2.4, 0.9 * c.until("collect")))

            # {collect}: buckets 0..9 empty into a new row
            c.wait_until("collect")
            order1 = sorted(range(6), key=lambda j: NUMS[j] % 10)          # 51 12 53 34 37 19
            self.play(LaggedStart(*[self.travel(tiles[j], row_pos(k)) for k, j in enumerate(order1)],
                                  lag_ratio=0.35), run_time=min(3.0, 0.9 * c.until("first")))
            self.tiles = tiles = [tiles[j] for j in order1]

            # {first}: the ones digits flash as the row is read
            c.wait_until("first")
            self.cap1 = T("sorted by last digit", 36).move_to([0, 0.0, 0])
            self.play(*appear(self.cap1), run_time=0.9)  # early: the brief puts it on {first}, as the row is read
            self.play(LaggedStart(*[FlashAround(t.ones, run_time=1.0, time_width=1.5) for t in tiles],
                                  lag_ratio=0.6), run_time=min(4.4, 0.9 * c.until("sorted by the last digit")))

    # ---------------------------------------------------------------- clip 3
    def clip3(self):
        tiles = self.tiles                       # 51 12 53 34 37 19
        with self.say("c6.radix.3") as c:
            c.wait_until("tens")
            self.play(*[t.ones.animate.set_color(GOLD) for t in tiles],
                      *[t.tens.animate.set_color(YELLOW) for t in tiles], run_time=1.0)
            # deal by tens, in row order; second of a bucket lands on top
            seen = {}
            moves = []
            for t in tiles:
                b = t.n // 10
                k = seen.get(b, 0)
                seen[b] = k + 1
                moves.append(self.travel(t, self.bucket_target(b, k)))
            self.play(*during(disappear(self.cap1), 0, 0.2),
                      *during([LaggedStart(*moves, lag_ratio=0.35)], 0.12, 1),
                      run_time=max(1.6, min(2.6, 0.95 * c.until("keep"))))

            # {keep}
            by_n = {t.n: t for t in tiles}
            self.tag = T("same bucket: arrival order kept", 34, TEAL).move_to([0, 0.1, 0])
            c.wait_until(own_word=self.tag, cue="keep")
            self.play(*appear(self.tag), run_time=1.0)
            c.wait_until("So twelve stays")
            self.play(*flash([by_n[12], by_n[19]], run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("fifty-one ahead")
            self.play(*flash([by_n[51], by_n[53]], run_time=1.5, time_width=1.5), run_time=1.5)

            # {sorted}: collect again; in each bucket the top tile leaves first
            c.wait_until("sorted")
            final = sorted(tiles, key=lambda t: t.n)
            pos = {t.n: k for k, t in enumerate(final)}
            order = [19, 12, 37, 34, 53, 51]
            self.play(*during(disappear(self.tag), 0, 0.2),
                      *during([LaggedStart(*[self.travel(by_n[n], row_pos(pos[n])) for n in order],
                                           lag_ratio=0.3)], 0.15, 1),
                      run_time=min(2.6, 0.85 * c.until("passes")))
            self.tiles = tiles = final
            self.tick = check_mark(GREEN).scale(0.8).next_to(tiles[-1], RIGHT, buff=0.35)
            self.play(Create(self.tick), run_time=0.8)

            # {passes}
            c.wait_until("Two-digit")
            self.cap2 = Tex(r"2 digits $\rightarrow$ 2 passes, each over all $n$ items: $O(n)$",
                            font_size=44, color=GOLD).move_to([0, 0.0, 0])
            self.play(*appear(self.cap2), run_time=1.0)

    # ---------------------------------------------------------------- clip 4
    def clip4(self):
        with self.say("c6.radix.4") as c:
            c.wait_until("never")
            le = Mono("<=", 48)
            lbox = SurroundingRectangle(le, color=BLUE, buff=0.22, stroke_width=4)
            zero = T("comparisons: 0", 38, GOLD)
            VGroup(VGroup(le, lbox), zero).arrange(RIGHT, buff=0.6).move_to([0, -0.8, 0])
            strike = Line(lbox.get_corner(DL), lbox.get_corner(UR)).set_stroke(RED, 7)
            self.play(FadeIn(lbox), *appear(le, shift=None), run_time=0.9)
            self.play(Create(strike), *appear(zero), run_time=1.0)  # early: the brief's tally on {never} ("compared")
            self.never = [le, lbox, strike, zero]

            # {bound}
            c.wait_until("bound")
            self.ctag = T("counts comparisons only", 30, YELLOW).move_to([0, 1.72, 0])
            self.play(FlashAround(VGroup(self.bound.box, self.bound.lf), run_time=1.6, time_width=1.5),
                      *appear(self.ctag), run_time=1.6)

            c.wait_until("There's no contradiction")
            self.noc = T("no contradiction", 38, GREEN).move_to([0, TOP_Y, 0])
            self.play(*swap(self.q, self.noc), run_time=1.2)

            # {catch}
            c.wait_until("catch")
            self.play(*set_alpha([*self.tiles, self.tick, self.row, *self.never], DIMMED), run_time=1.0)
            c.wait_until("The number of passes")
            self.catch1 = T("passes = digits of the largest number", 36).move_to([0, 0.0, 0])
            self.play(*swap(self.cap2, self.catch1), *disappear(*self.never), run_time=1.2)
            c.wait_until("linear only")
            self.catch2 = T("linear only if the largest number is fixed in advance", 36,
                            t2c={"fixed in advance": YELLOW}).move_to([0, -0.75, 0])
            self.play(*appear(self.catch2), run_time=1.0)

    # ---------------------------------------------------------------- clip 5
    def clip5(self):
        with self.say("c6.radix.5") as c:
            c.wait_until("equal")
            sweep_clear(self, time_span(self.catch1.animate.move_to([0, 3.4, 0]), 0.6, 1.4),
                        time_span(self.catch2.animate.move_to([0, 2.75, 0]), 0.6, 1.4),
                        keep=[self.catch1, self.catch2], run_time=1.4)

            # the pile: columns of 12s, 34s, 53s on the left
            cols = {12: -4.3, 34: -3.0, 53: -1.7}
            floor = -3.3
            pile = {n: [] for n in cols}

            def add_tiles(counts):
                new = []
                for n, cnt in counts.items():
                    for _ in range(cnt):
                        k = len(pile[n])
                        t = num_tile(n).move_to([cols[n], floor + 0.35 + STACK * k, 0])
                        pile[n].append(t)
                        new.append(t)
                return new

            first = add_tiles({12: 2, 34: 2, 53: 2})
            order = [first[i] for i in (0, 2, 4, 1, 3, 5)]
            self.play(*appear(*order, lag=0.25, shift=0.4 * DOWN), run_time=min(1.8, c.until("With numbers below")))

            self.lbl100 = T("numbers below 100: only 100 different values", 36).move_to([0, 1.9, 0])
            c.wait_until(own_word=self.lbl100, cue="With numbers below")
            self.play(*appear(self.lbl100), run_time=1.0)
            more = add_tiles({12: 3, 34: 2, 53: 3})
            more.sort(key=lambda t: t.get_y())
            self.play(*appear(*more, lag=0.18, shift=0.4 * DOWN), run_time=min(2.2, 0.9 * c.until("digits")))

            # {digits}
            c.wait_until("digits")
            d1 = Tex(r"$n$ different numbers need", font_size=54)
            d2 = Tex(r"about $\log_{10} n$ digits", font_size=54)
            dg = VGroup(d1, d2).arrange(DOWN, buff=0.25).move_to([3.0, 0.2, 0])
            self.play(*appear(d1, d2, lag=0.4), run_time=1.4)
            c.wait_until("brings back")
            nlog = Tex(r"$n \times \log n$ again", font_size=64, color=GOLD).move_to([3.0, -1.7, 0])
            self.play(*appear(nlog), run_time=1.0)

            # {special}
            c.wait_until("special")
            head = T("radix sort: a simple special case", 50, t2c={"radix sort:": YELLOW}).move_to([0, 1.7, 0])
            sweep_clear(self, FadeIn(head, shift=0.2 * DOWN), keep=[d1, d2, nlog], run_time=1.6)
            self.wait(0.1)

            # {others}: two DIM card outlines slide in together from the right edge
            c.wait_until("others")
            cards = VGroup()
            for name in ("selection sort", "bubble sort"):
                box = RoundedRectangle(corner_radius=0.2, width=4.6, height=2.2).set_stroke(DIM, 3)
                lab = T(name, 40, DIM).move_to(box)
                cards.add(VGroup(box, lab))
            cards.arrange(RIGHT, buff=1.2).move_to([0, -1.4, 0])
            cards.shift(RIGHT * 12)
            self.add(cards)
            self.play(*during(disappear(d1, d2, nlog), 0.1, 0.4),
                      *during([cards.animate.shift(LEFT * 12)], 0.35, 1), run_time=1.8)  # early: the exercises' two sorts, named next scene
