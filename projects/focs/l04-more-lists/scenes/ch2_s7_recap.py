"""Chapter 2, scene 7: the recap of searching a list (five lines, each with a small icon from the
chapter on its left) and the end card with ch3's teaser (a phone book of pairs that splits into
two lists). Clips c2.recap.1 – c2.recap.2 (the chapter's last scene).

Icons are rebuilt small here (no imports from other scenes): s1's chain 3 5 9 4 7 with its GOLD
marker; s3's row of 16 ordered boxes halving, beside a column of hash-table slots; s4's member
code; s5's BLUE operators; s6's ring of four cells, the last pointer looping back under the row.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, select, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

MEMBER = ("let rec member x = function\n"
          "  | [] -> false\n"
          "  | y::l ->\n"
          "      if x = y then true\n"
          "      else member x l")
EXC = 'Invalid_argument "compare: functional value"'
BOOK = [("Amy", 21), ("Bob", 35), ("Cleo", 47)]

# ── layout ──────────────────────────────────────────────────────────────────────
TITLE_Y = 3.25
ICON_X, ICON_W = -5.05, 3.0         # icon column: centre and widest icon
TEXT_X = -3.15                      # left edge of every line's text
ROW_Y = (2.25, 1.25, -0.05, -1.2, -2.4)
R5_LINES = (-2.1, -2.7)             # row 5: the exception, then "may never finish"
TEXT_SIZE, COST_SIZE, EXC_SIZE = 34, 42, 26
SAID = 0.5                          # a line that has been said steps back to this
END_SCALE, END_TOP, END_OP = 0.7, 3.6, 0.45   # the recap on the end card
NEXT_Y, BOOK_Y, SPLIT_Y = -0.78, -1.82, -3.0     # teaser rows under it
BOOK_SIZE, BOOK_H, BOOK_LINK = 28, 0.8, 0.5
END_CARD = 8.0
HALVE_TARGET = 5                    # the box the halving icon closes in on


def multiply_opacity(mob, k):
    """Scale every part's opacity by k in place (keeps the dims inside an icon)."""
    for leaf in mob.family_members_with_points():
        leaf.set_fill(opacity=leaf.get_fill_opacity() * k, family=False)
        leaf.set_stroke(opacity=leaf.get_stroke_opacity() * k, family=False)
    return mob


def faded(mob, k):
    return multiply_opacity(mob.copy(), k)


def cost(tex, word=None, color=GOLD):
    o = MathTex(tex, font_size=COST_SIZE, color=color)
    if word is None:
        return VGroup(o)
    w = T(word, size=TEXT_SIZE, color=color)
    grp = VGroup(o, w).arrange(RIGHT, buff=0.18)
    w.align_to(o, DOWN).shift(UP * 0.06)
    return grp


def line_at(parts, y, gaps=None):
    """Parts in a row, left edge on the text column, centred on y."""
    grp = VGroup(*parts).arrange(RIGHT, buff=0.22)
    if gaps:
        for i, extra in gaps.items():
            for p in parts[i:]:
                p.shift(RIGHT * extra)
    grp.move_to([TEXT_X, y, 0], aligned_edge=LEFT)
    return grp


# ── icons ───────────────────────────────────────────────────────────────────────
def chain_icon():
    ch = ConsChain([3, 5, 9, 4, 7])
    ptr = marker(GOLD, scale=0.45).move_to(above(ch.cells[0].box))  # s1: 0.24, enlarged to read at icon size
    icon = VGroup(ch, ptr).scale(ICON_W / ch.width)
    icon.chain, icon.ptr = ch, ptr
    return icon


def search_icon():
    boxes = VGroup(*[Square(1.0, stroke_color=BLUE, stroke_width=2) for _ in range(16)])
    boxes.arrange(RIGHT, buff=0).scale_to_fit_width(2.2)
    slots = VGroup(*[Rectangle(width=0.5, height=0.15, stroke_color=BLUE, stroke_width=2)
                     for _ in range(5)]).arrange(DOWN, buff=0)
    slots.next_to(boxes, RIGHT, buff=0.3)
    icon = VGroup(boxes, slots)
    icon.boxes, icon.slots = boxes, slots
    return icon


def member_icon():
    code = Code(MEMBER, size=13)
    for k in range(2):
        for gl in code.find("member", nth=k):
            gl.set_color(YELLOW)
    return code


def corner(path, a, c, b):
    """Rounded corner from a (on the path's end) via corner point c to b."""
    path.add_cubic_bezier_curve_to(a + (c - a) * 0.55, b + (c - b) * 0.55, b)


def ring_icon():
    """s6's loop: the return pointer leaves cell 4's dot to the right, turns down, runs left
    under the row and goes up into the bottom of cell 1's box (link style: FG, stroke 3)."""
    ch = ConsChain([1, 2, 3, 4], with_nil=False)
    r = 0.25
    p0 = ch.cells[3].tail_start()
    x_r = ch.cells[3].ptr.get_right()[0] + 0.45
    x_1 = ch.cells[0].box.get_x()
    y_top, y_low = p0[1], ch.cells[0].box.get_bottom()[1] - 0.6
    pt = lambda x, y: np.array([x, y, 0.0])  # noqa: E731
    path = VMobject(stroke_color=FG, stroke_width=3)
    path.start_new_path(p0)
    path.add_line_to(pt(x_r - r, y_top))
    corner(path, pt(x_r - r, y_top), pt(x_r, y_top), pt(x_r, y_top - r))
    path.add_line_to(pt(x_r, y_low + r))
    corner(path, pt(x_r, y_low + r), pt(x_r, y_low), pt(x_r - r, y_low))
    path.add_line_to(pt(x_1 + r, y_low))
    corner(path, pt(x_1 + r, y_low), pt(x_1, y_low), pt(x_1, y_low + r))
    tip = Arrow(pt(x_1, y_low + r), ch.cells[0].box.get_bottom(), buff=0, stroke_width=3, color=FG,
                max_tip_length_to_length_ratio=0.6, tip_length=0.16)
    back = VGroup(path, tip)
    icon = VGroup(ch, back).scale(2.8 / VGroup(ch, back).width)
    icon.chain, icon.back, icon.path, icon.tip = ch, back, path, tip
    return icon


def loop_trace(icon):
    """The whole return pointer as one stroke, for a flash to run along."""
    trace = icon.path.copy()
    trace.add_line_to(icon.tip.get_end())
    return trace


# ── the teaser's phone book: cons cells that each hold a pair ───────────────────
def pair_label(name, num):
    return Mono(f'("{name}", {num})', size=BOOK_SIZE, t2c={f'"{name}"': YELLOW, str(num): GOLD})


def pair_cell(name, num, color=BLUE):
    label = pair_label(name, num)
    box = Rectangle(width=label.width + 0.34, height=BOOK_H, stroke_color=color, stroke_width=3,
                    fill_color=BG, fill_opacity=1)
    ptr = Rectangle(width=PTR_W, height=BOOK_H, stroke_color=color, stroke_width=3,
                    fill_color=BG, fill_opacity=1).next_to(box, RIGHT, buff=0)
    dot = Dot(ptr.get_center(), radius=0.07, color=FG)
    label.move_to(box)
    cell = VGroup(box, ptr, dot, label)
    cell.box, cell.ptr, cell.dot, cell.label = box, ptr, dot, label
    cell.tail_start = lambda: dot.get_center()
    cell.entry = lambda: box.get_left()
    cell.name, cell.num = name, num
    return cell


def book_chain():
    cells = [pair_cell(n, v) for n, v in BOOK]
    x = 0.0
    for c in cells:
        c.move_to(RIGHT * x, aligned_edge=LEFT)
        x += c.width + BOOK_LINK
    nil = Nil(size=36)
    nil.move_to(RIGHT * x, aligned_edge=LEFT)
    arrows = [link(a, b) for a, b in zip(cells, cells[1:] + [nil])]
    chain = VGroup(*cells, *arrows, nil).move_to([0, BOOK_Y, 0])
    chain.cells, chain.arrows, chain.nil = cells, arrows, nil
    return chain


class SearchRecap(NarratedScene):
    def construct(self):
        self.recap()
        self.teaser()
        # End card: the finished recap and the teaser hold, fully visible, under the music.
        self.wait(END_CARD)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.3)
        self.wait(0.15)

    # ── recap.1: five lines, one per mark ──────────────────────────────────────────
    def recap(self):
        self.title = title = T("Recap", size=48).move_to([0, TITLE_Y, 0])

        i1 = chain_icon().move_to([ICON_X, ROW_Y[0], 0])
        l1 = line_at([T("Linear search, one by one:", size=TEXT_SIZE), cost(r"O(n)", "time")], ROW_Y[0])
        row1 = VGroup(i1, *l1)

        i2 = search_icon().move_to([ICON_X, ROW_Y[1], 0])
        l2 = line_at([T("Data in order:", size=TEXT_SIZE), cost(r"O(\log n)"),
                      T("an index:", size=TEXT_SIZE), cost(r"O(1)")], ROW_Y[1], gaps={2: 0.35})
        row2 = VGroup(i2, *l2)

        i3 = member_icon().move_to([ICON_X, ROW_Y[2], 0])
        l3 = line_at([T("Simple and general;", size=TEXT_SIZE), T("iterative,", size=TEXT_SIZE),
                      cost(r"O(1)", "space")], ROW_Y[2])
        row3 = VGroup(i3, *l3)

        i4 = Mono("=  <  <=  >  >=", size=24, color=BLUE).move_to([ICON_X, ROW_Y[3], 0])
        l4 = line_at([T("Polymorphic equality compares", size=TEXT_SIZE),
                      T("by structure", size=TEXT_SIZE)], ROW_Y[3])
        row4 = VGroup(i4, *l4)

        i5 = ring_icon().move_to([ICON_X, ROW_Y[4], 0])
        exc = Mono(EXC, size=EXC_SIZE, color=RED).move_to([TEXT_X, R5_LINES[0], 0], aligned_edge=LEFT)
        never = T("may never finish", size=TEXT_SIZE).move_to([TEXT_X, R5_LINES[1], 0], aligned_edge=LEFT)
        row5 = VGroup(i5, exc, never)
        self.rows = [row1, row2, row3, row4, row5]

        up = 0.25 * UP
        with self.say("c2.recap.1") as c:
            # "Let's recap."
            self.play(FadeIn(title, shift=0.3 * DOWN), run_time=min(1.0, c.until("r1")))

            # "Linear search compares the item with each element in turn, so it takes big O of en time."
            c.wait_until("r1")
            self.play(FadeIn(i1, shift=up), FadeIn(l1[0], shift=up), run_time=1.2)
            c.wait_until("each element")
            xs = [cell.box.get_x() for cell in i1.chain.cells]

            def step(m, a):
                t = a * (len(xs) - 1)
                k = min(int(t), len(xs) - 2)
                f = smooth(float(np.clip((t - k) / 0.7, 0, 1)))
                m.set_x(xs[k] + (xs[k + 1] - xs[k]) * f)

            self.play(UpdateFromAlphaFunc(i1.ptr, step), rate_func=linear,
                      run_time=max(1.2, min(2.0, c.until("big O of en time") - 0.1)))
            c.wait_until("big O of en time")
            self.play(FadeIn(l1[1], shift=up), run_time=1.0)
            settle(self, row1)

            # "Data kept in order can be searched in big O of log en, and an index, like a hash table,
            # can reach big O of one."
            c.wait_until("r2")
            self.play(Transform(row1, faded(row1, SAID)), FadeIn(i2.boxes, lag_ratio=0.05),
                      FadeIn(l2[0], shift=up), run_time=1.2)
            c.wait_until("big O of log")
            lo, hi, halves = 0, 16, []
            while hi - lo > 1:
                mid = (lo + hi) // 2
                if HALVE_TARGET < mid:
                    halves.append(range(mid, hi))
                    hi = mid
                else:
                    halves.append(range(lo, mid))
                    lo = mid
            dims = [time_span(i2.boxes[j].animate.set_stroke(opacity=DIMMED), 0.3 * k, 0.3 * k + 0.3)
                    for k, rng in enumerate(halves) for j in rng]
            t_hit = 0.3 * len(halves)
            self.play(*dims, time_span(i2.boxes[HALVE_TARGET].animate.set_fill(YELLOW, 0.9), t_hit, t_hit + 0.3),
                      time_span(FadeIn(l2[1], shift=up), 0.3, 1.3), run_time=t_hit + 0.3)
            c.wait_until("an index")
            self.play(FadeIn(i2.slots, lag_ratio=0.15), FadeIn(l2[2], shift=up), run_time=1.1)
            c.wait_until("big O of one")
            self.play(i2.slots[2].animate.set_fill(GOLD, 0.9), FadeIn(l2[3], shift=up), run_time=1.0)
            settle(self, row2)

            # "Still, linear search is simple and general."
            c.wait_until("r3")
            self.play(Transform(row2, faded(row2, SAID)), FadeIn(i3, shift=up), FadeIn(l3[0], shift=up),
                      run_time=1.3)
            # "On lists, it's member, which is iterative, so it needs only constant space."
            c.wait_until("on lists")
            self.play(*flash([VGroup(*i3.find("member", nth=k)) for k in range(2)], YELLOW,
                             time_width=1.5), run_time=1.2)
            c.wait_until("iterative")
            self.play(FadeIn(l3[1], shift=up), run_time=1.0)
            c.wait_until("constant space")
            self.play(FadeIn(l3[2], shift=up), run_time=1.0)
            settle(self, row3)

            # "Member works at any type, thanks to polymorphic equality, which compares values by
            # their structure."
            c.wait_until("r4")
            self.play(Transform(row3, faded(row3, SAID)), FadeIn(i4, lag_ratio=0.2),
                      FadeIn(l4[0], shift=up), run_time=1.4)
            c.wait_until("by their structure")
            self.play(FadeIn(l4[1], shift=up), run_time=0.9)
            self.play(FlashUnder(l4[1], color=BLUE), run_time=1.0)
            settle(self, row4)

            # "But equality raises an exception on functions, and may never finish on a structure
            # that loops back on itself."
            c.wait_until("r5")
            self.play(Transform(row4, faded(row4, SAID)), FadeIn(exc, shift=up), run_time=1.3)
            c.wait_until("may never finish")
            self.play(FadeIn(i5.chain, lag_ratio=0.15), time_span(Create(i5.back), 0.6, 1.4),
                      FadeIn(never, shift=up), run_time=1.4)
            c.wait_until("loops back")
            self.play(VShowPassingFlash(loop_trace(i5).set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=1.2)
            settle(self, row5)

    # ── recap.2: the teaser, ch3's phone book ──────────────────────────────────────
    def teaser(self):
        recap = VGroup(*self.rows)
        settle(self, recap)
        target = recap.copy().scale(END_SCALE)
        target.move_to([0, END_TOP - target.height / 2, 0])
        for row, k in zip(target, [END_OP / SAID] * 4 + [END_OP]):
            multiply_opacity(row, k)

        nxt = VGroup(T("Next:", size=40, color=DIM), T("lists of pairs", size=40, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25).move_to([0, NEXT_Y, 0])
        book = book_chain()
        parts = [p for i, cell in enumerate(book.cells) for p in (cell, book.arrows[i])] + [book.nil]

        names = Mono('["Amy"; "Bob"; "Cleo"]', size=32, t2c={f'"{n}"': YELLOW for n, _ in BOOK})
        nums = Mono("[21; 35; 47]", size=32, t2c={str(v): GOLD for _, v in BOOK})
        VGroup(names, nums).arrange(RIGHT, buff=1.6).move_to([0, SPLIT_Y, 0])

        def name_of(cell):
            return select(cell.label, f'"{cell.name}"')[0]

        def num_of(cell):
            return select(cell.label, str(cell.num))[0]

        with self.say("c2.recap.2") as c:
            # "Next time, we'll look at lists of pairs."
            # The recap lands first (1.2 s); only then the header and the phone book come in.
            t = max(2.0, min(2.4, c.until("phone")))
            slide = [time_span(FadeIn(p, shift=0.6 * LEFT), 1.3 + 0.1 * i, min(t, 2.0 + 0.1 * i))
                     for i, p in enumerate(parts)]
            self.play(time_span(FadeOut(self.title, shift=0.3 * UP), 0, 0.8),
                      time_span(Transform(recap, target), 0, 1.2),
                      time_span(FadeIn(nxt, shift=0.3 * DOWN), 1.2, 1.9), *slide, run_time=t)
            settle(self, book)

            # "We'll pair up names with phone numbers, like a telephone directory,"
            c.wait_until("names")
            d = max(0.3, c.until("phone numbers"))
            self.play(*[time_span(FlashAround(name_of(cell), color=YELLOW, time_width=1.5), 0, 1.0)
                        for cell in book.cells],
                      *[time_span(FlashAround(num_of(cell), color=GOLD, time_width=1.5), d, d + 1.0)
                        for cell in book.cells], run_time=d + 1.0)

            # "and then split the pairs apart again."
            c.wait_until("split the pairs")
            movers, flights = [], []
            for cell in book.cells:
                for src, dst in ((name_of(cell), select(names, f'"{cell.name}"')[0]),
                                 (num_of(cell), select(nums, str(cell.num))[0])):
                    m = dst.copy()
                    movers.append(m)
                    flights.append(time_span(ReplacementTransform(src.copy(), m), 0, 1.4))
            self.play(*flights, time_span(FadeIn(names), 1.1, 1.8), time_span(FadeIn(nums), 1.1, 1.8),
                      run_time=1.8)
            self.remove(*movers)
