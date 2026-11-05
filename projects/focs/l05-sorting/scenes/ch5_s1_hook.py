"""Chapter 5, scene 1: hook: quicksort's worst case, the board, merge sort's promise. Clips c5.hook.1 – c5.hook.3.

Opens on `open_card()` (ch4's last scene ends on exactly it), clears to the title card on {title}.
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
from lib.titles import title_card  # noqa: E402

from scenes.ch1_s2_why import num_box  # noqa: E402
from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402
from scenes.ch4_s3_worst import worst_tree  # noqa: E402

TITLE_Y = 3.3
RUN = [3, 5, 9, 4, 7]


# ── shared pieces ────────────────────────────────────────────────────────────────
def filled_board():
    """The scoreboard as ch4 leaves it: two rows filled, merge sort's row label YELLOW."""
    sb = make_scoreboard(bound="118,458")
    for r, row in enumerate((("25,146,194", "174 s"), ("158,058", "0.53 s"))):
        for col, val in enumerate(row):
            v = T(val, 44, GOLD).move_to(sb.cells[r][col])
            sb.cells[r].submobjects[col] = v
    sb.row_labels[0].set_color(FG)
    sb.row_labels[1].set_color(FG)
    return sb


def split_shot(s, yc, yl, gap):
    """L4 ch1 s7's take/drop shot, finished: the running chain at y=yc with the GOLD cut after
    cell 2, and [3; 5] and [9; 4; 7] lifted apart at y=yl.  Everything scaled by s."""
    run = ConsChain(RUN).scale(s).move_to([0, yc, 0])
    c = run.cells
    x_cut = (c[1].ptr.get_right()[0] + c[2].box.get_left()[0]) / 2
    half = 0.95 * s
    cut = DashedLine([x_cut, yc + half, 0], [x_cut, yc - half, 0], dash_length=0.12 * s / 0.75,
                     color=GOLD, stroke_width=5)
    L = ConsChain([3, 5]).scale(s)
    R = ConsChain([9, 4, 7]).scale(s)
    total = L.width + gap + R.width
    L.move_to([-total / 2 + L.width / 2, yl, 0])
    R.move_to([total / 2 - R.width / 2, yl, 0])
    return run, cut, L, R


def open_card():
    """ch5's first frame (= ch4's end card): "Next: merge sort" on top, the board, the split under it."""
    nxt = T("Next: merge sort", 52, t2c={"merge sort": YELLOW}).move_to(UP * TITLE_Y)
    sb = filled_board()
    top, floor = 2.78, -1.62
    sb.scale(min((top - floor) / sb.height, 12.0 / sb.width))
    sb.move_to([0, top - sb.height / 2, 0])
    run, cut, L, R = split_shot(0.5, -3.0, -2.05, gap=0.8)
    card = VGroup(nxt, sb, run, cut, L, R)
    card.nxt, card.board, card.run, card.cut, card.L, card.R = nxt, sb, run, cut, L, R
    return card


def pill(text, color, size=30):
    """L4's small outlined tag."""
    t = T(text, size=size, color=color)
    box = RoundedRectangle(corner_radius=0.22, width=t.width + 0.55, height=t.height + 0.36,
                           stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.10)
    box.move_to(t)
    return VGroup(box, t)


def hook_tree():
    """ch4 s3's worst_tree() (circle zigzag 3, 9, 4, 7, 5, BLUE rings, YELLOW digits, RED empty
    sides) at hero size under the sorted chain, styled as ch5 s6's quick_tree() scaled by 1.5.
    .chain, .levels (one VGroup per depth: edge in, node, its RED stubs), .empties (the stubs)."""
    wt = worst_tree("circles", size=39, radius=0.45, pitch=1.35, gap=1.0)
    wt.place(1.0, [-2.6, 1.55, 0])
    chain = ConsChain([3, 4, 5, 7, 9]).scale(0.72).move_to([-2.6, 2.8, 0])
    levels = []
    for nd in wt.nodes:
        parts = ([nd.edge] if nd.parent is not None else []) + [nd.body] + list(nd.stubs.values())
        levels.append(VGroup(*parts))
    tree = VGroup(chain, *levels)
    tree.chain, tree.levels, tree.empties, tree.wt = chain, levels, list(wt.stubs), wt
    return tree


class Hook(NarratedScene):
    def construct(self):
        card = open_card()
        self.add(*card)
        self.title_and_worst()
        self.board()
        self.promise()
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── c5.hook.1 ────────────────────────────────────────────────────────────────
    def title_and_worst(self):
        tc = title_card("Part 5 · Merging and merge sort")
        tree = hook_tree()
        count = T("sorted rs: 49,995,000", 40, GOLD).move_to([3.75, 0.35, 0])
        big = T("O(n²)", 64, RED).move_to([3.75, -1.0, 0])

        with self.say("c5.hook.1") as c:
            # {title}: the opening card clears to the title card
            sweep_clear(self, time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.6, 1.2),
                        time_span(GrowFromCenter(tc.rule), 0.6, 1.2), run_time=1.2)
            self.play(*appear(tc.course, tc.part, lag=0.3), run_time=1.0)   # early: title card

            # {last}: the card holds through "Last time", the worst case comes in on "weak spot"
            c.wait_until("weak spot")
            sweep_clear(self, time_span(FadeIn(tree.chain, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            c.wait_until("sorted input")
            self.play(*appear(*tree.levels, shift=None, lag=0.35),
                      run_time=min(2.6, 0.9 * c.until("lopsided") + 1.0))
            c.wait_until("lopsided")
            self.play(*flash(tree.empties, RED, time_width=1.5), run_time=1.5)
            c.wait_until("ten thousand")
            self.play(*appear(count), run_time=1.0)
            c.wait_until("fifty million")
            self.play(*appear(big), run_time=min(1.0, c.until()))

    # ── c5.hook.2 ────────────────────────────────────────────────────────────────
    def board(self):
        sb = filled_board()
        for m in (*sb.col_headers[0], sb.col_headers[1]):   # headers stay >= 28 after the 0.75 scale
            m.scale(38 / 30)
        c0 = sb.col_headers[0].get_center()
        sb.col_headers[0].arrange(DOWN, buff=0.12).move_to(c0)
        fl = VGroup(sb.floor_label, sb.floor_value)
        fl.scale(38 / 34, about_edge=LEFT)
        sb.floor_line.put_start_and_end_on(
            [sb.floor_value.get_right()[0] + 0.35, sb.floor_line.get_y(), 0], sb.floor_line.get_end())
        sb.tally_tag.scale(38 / 28).next_to(sb.col_headers[0], DOWN, buff=0.12)
        sb.col_headers[1].match_y(sb.col_headers[0][1]).shift(0.3 * RIGHT)
        sb.scale(0.75)
        sb.move_to([-6.6, 0.15, 0], aligned_edge=LEFT)
        row_r = max(sb.cells[r][1].get_right()[0] for r in range(2))
        tags = []
        for r, word in enumerate(("reversed", "sorted")):
            t = T(f"O(n²) on {word} input", 28, RED)
            t.move_to([row_r + 0.4, sb.cells[r][1].get_y(), 0], aligned_edge=LEFT)
            tags.append(t)
        q = T("O(n log n) on every input?", 44, YELLOW).move_to([0, 3.3, 0])
        pulse = (lambda t: there_and_back((2 * t) % 1.0))
        self.sb, self.q = sb, q
        _ = row_r

        with self.say("c5.hook.2") as c:
            # {board}
            sweep_clear(self, time_span(FadeIn(sb), 0.6, 1.4), run_time=1.4)   # early: the board returns whole
            c.wait_until("have inputs")
            self.play(*[m.animate(rate_func=pulse).scale(1.4) for m in sb.cells[2]],
                      *flash(list(sb.cells[2]), GOLD, time_width=1.5), run_time=1.4)
            # {quad}
            c.wait_until("reversed")
            self.play(*appear(tags[0], shift=0.25 * LEFT), run_time=1.0)
            c.wait_until("sorted input")
            self.play(*appear(tags[1], shift=0.25 * LEFT), run_time=1.0)
            # {guarantee}
            c.wait_until("guarantee")
            self.play(*appear(q), run_time=1.0)   # early: the question is on screen as it is asked

    # ── c5.hook.3 ────────────────────────────────────────────────────────────────
    def promise(self):
        run, cut, L, R = split_shot(0.75, -0.9, 1.25, gap=1.2)
        xs = label_pointer("xs", run.cells[0], direction=DOWN)
        lec = pill("Lecture 4: merge sort", DIM).move_to([0, 3.15, 0])

        RX = 3.4
        ra = VGroup(*[num_box(n) for n in [2, 7, 8]]).arrange(RIGHT, buff=0.15).move_to([RX - 1.75, 1.3, 0])
        rb = VGroup(*[num_box(n) for n in [3, 5, 9]]).arrange(RIGHT, buff=0.15).move_to([RX + 1.75, 1.3, 0])
        outs = VGroup(*[Square(0.85).set_stroke(DIM, 2) for _ in range(6)]).arrange(RIGHT, buff=0.15)
        outs.move_to([RX, -0.9, 0])
        p5 = T("Part 5", 30, DIM).move_to([RX, -2.1, 0])
        today = T("today", 34, YELLOW).move_to(p5)

        q1 = T("How do you merge two sorted lists?", 48, YELLOW).move_to([0, 0.8, 0])
        q2 = T("What does merge sort cost, at worst?", 48, YELLOW).move_to([0, -0.6, 0])

        with self.say("c5.hook.3") as c:
            # {promise}
            sweep_clear(self, time_span(FadeIn(run, shift=0.3 * UP), 0.6, 1.4),
                        time_span(FadeIn(xs, shift=0.2 * UP), 0.8, 1.4), keep=[self.q], run_time=1.4)
            c.wait_until("last lecture")
            self.play(*swap(self.q, lec), run_time=1.2)
            c.wait_until("cutting")
            self.play(Create(cut), run_time=min(1.2, c.until("take and drop")))
            c.wait_until("take and drop")
            rt = min(1.8, 0.9 * c.until("merging"))
            anims = []
            for i in range(2):
                anims += fly(run.cells[i], L.cells[i])
            for i in range(3):
                anims += fly(run.cells[i + 2], R.cells[i])
            anims += fly(run.nil, R.nil)
            anims += during([FadeIn(m) for m in (*L.arrows, L.nil, *R.arrows)], 0.75, 1)
            self.play(*anims, run_time=rt)
            settle(self, L)
            settle(self, R)

            # {merging}: the split shot shrinks to the left, merging comes in at the right
            c.wait_until("merging")
            moved = [L.animate.move_to([-6.6, 1.35, 0], aligned_edge=LEFT),
                     R.animate.move_to([-6.6, -0.35, 0], aligned_edge=LEFT)]
            self.play(*during([FadeOut(m) for m in (lec, run, xs, cut)], 0, 0.4),
                      *during(moved[:1], 0.15, 0.55), *during(moved[1:], 0.3, 0.7),
                      time_span(FadeIn(ra, lag_ratio=0.15), 0.8, 1.6),
                      time_span(FadeIn(rb, lag_ratio=0.15), 0.9, 1.7),
                      time_span(FadeIn(outs, lag_ratio=0.1), 1.0, 1.8), run_time=1.8)
            c.wait_until("part one listed")
            self.play(*appear(p5), run_time=0.8)   # early: ch1 s2's tag, read as "part one listed"

            c.wait_until("two sorted lists")
            moves = [(ra[0], 0), (rb[0], 1), (rb[1], 2), (ra[1], 3), (ra[2], 4), (rb[2], 5)]
            weights = [1.6, 1.2, 1.0, 1.0, 1.0, 1.0]
            hold = 0.1
            budget = c.until("into one", floor=3.0) - 0.15 - hold * len(moves)
            for (m, j), w in zip(moves, weights):
                self.play(m.animate.move_to(outs[j]), run_time=max(0.4, min(1.2, budget * w / sum(weights))))
                self.wait(hold)

            c.wait_until("into one")
            self.play(*swap(p5, today), run_time=1.2)
            # {questions}
            c.wait_until("how do you merge")
            sweep_clear(self, time_span(FadeIn(q1, shift=0.25 * DOWN), 0.6, 1.4), run_time=1.4)
            c.wait_until("what does merge sort")
            self.play(*appear(q2), run_time=1.0)
