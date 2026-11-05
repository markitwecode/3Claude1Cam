"""Chapter 3, scene 1: title card, then the hook: a program can't count a list at a glance,
it can only ask "empty, or a head on a tail?". Two answers are coming, one with a hidden cost.

Clips c3.hook.1 – c3.hook.3.

STATUS (paused): done: all three clips built, renders clean (480p15, ~55 s).
remaining: visual review of contact sheet / key frames (not yet looked at). Dwell: 0 flags
(after bumping the last gap to 1.6 s so "accumulator" can be read).
known issues: layout inside the "version" slots (cost label vs "accumulator") unchecked;
"length = ?" baseline alignment is approximate.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

S = 1.2                    # the chain is the hero: 5 -> 6 -> 7 -> [] spans ~8.8 units
DIM_TO = 0.25              # spotlight: everything else drops to this (PATTERNS P9)
CHAIN_Y, Q_Y = 0.35, -1.55  # chain and "length = ?" while the frame holds only them
DROP = 0.8                 # both move down this much when the fork arrives above
FORK_TOP, FORK_PAT = 3.05, 1.75   # the fork's "?" and its two patterns
SLOT_X, SLOT_W, SLOT_H = 3.35, 5.9, 4.3   # the two "version" slots
BOXES, BOX, BOX_GAP = 10, 0.42, 0.08       # the little list inside each slot


# ── helpers (local to this scene) ───────────────────────────────────────────────
def length_question():
    """`length = ?`, the "?" in GOLD (it briefly becomes a 3)."""
    q = VGroup(T("length", size=52), T("=", size=52), T("?", size=60, color=GOLD))
    q.arrange(RIGHT, buff=0.25)
    q[2].align_to(q[1], DOWN).shift(DOWN * 0.08)
    return q


def hl_box(mob, color=YELLOW, pad=0.12):
    """The sliding highlight (P8): thin stroke, faint fill, drawn behind the text."""
    return SurroundingRectangle(mob, buff=pad, stroke_width=2, color=color).set_fill(
        color, opacity=0.2).set_z_index(-1)


def fork():
    """The question pattern matching asks: [] on one branch, x :: xs on the other."""
    root = T("?", size=64, color=YELLOW).move_to(UP * FORK_TOP)
    nil = Code("[]", size=48).move_to([-2.0, FORK_PAT, 0])
    cons = Code("x :: xs", size=48).move_to([2.0, FORK_PAT, 0])
    lines = VGroup(*[Line(root.get_bottom() + DOWN * 0.12, p.get_top() + UP * 0.15,
                          stroke_width=3, color=DIM) for p in (nil, cons)])
    return root, lines, nil, cons


def slot(x, name):
    """A dashed, still-empty slot for one answer, with its name above."""
    frame = DashedVMobject(RoundedRectangle(corner_radius=0.22, width=SLOT_W, height=SLOT_H),
                           num_dashes=70).set_stroke(DIM, 2.5)
    frame.move_to([x, -0.55, 0])
    head = T(name, size=40).next_to(frame, UP, buff=0.3)
    return frame, head


def mini_list(frame):
    """Ten small element boxes, left-aligned inside a slot; only some are shown at a time."""
    boxes = VGroup(*[Square(BOX, stroke_color=BLUE, stroke_width=2.5) for _ in range(BOXES)])
    boxes.arrange(RIGHT, buff=BOX_GAP)
    boxes.move_to([frame.get_left()[0] + 0.48, frame.get_y() + 0.05, 0], aligned_edge=LEFT)
    return boxes


def span(boxes, n):
    """Width of the first n boxes."""
    return n * BOX + (n - 1) * BOX_GAP


def cost_bar(boxes, width):
    bar = Rectangle(width=width, height=0.3, stroke_width=0).set_fill(GOLD, 1)
    return bar.move_to(boxes[0].get_corner(DL) + DOWN * 0.55, aligned_edge=UL)


class Hook(NarratedScene):
    def construct(self):
        chain, labels, q = self.title()
        q = self.glance(chain, labels, q)
        self.twice(q)
        self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects)], lag_ratio=0.06),
                  run_time=1.2)
        self.wait(0.1)  # a truly empty last frame

    # hook.1: the title card; the word "Lists" becomes a list, and the question arrives
    def title(self):
        card = title_card("Part 3 · Length, recursion and accumulators")
        chain = ConsChain([5, 6, 7]).scale(S)
        labels = [c.label for c in chain.cells]   # the values arrive in hook.2, on the spoken numbers
        for c, lab in zip(chain.cells, labels):
            c.remove(lab)
        chain.move_to(card.title)
        q = length_question().move_to(UP * Q_Y)

        with self.say("c3.hook.1") as c:
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)
            c.wait_until("lecture")
            self.play(FadeIn(card.course, shift=0.25 * DOWN), run_time=0.9)
            c.wait_until("lists")
            self.play(FadeIn(card.part, shift=0.25 * DOWN), run_time=1.0)

            # "...the most basic question you can ask about a list": the word becomes a list (P5)
            c.wait_until("basic question")
            self.play(FadeTransform(card.title, chain), FadeOut(card.rule), run_time=1.6)

            # "How long is it?"  The subtitles make way; the question goes on screen (P23)
            c.wait_until("ask")
            self.play(LaggedStart(FadeOut(card.part), FadeOut(card.course), lag_ratio=0.2),
                      chain.animate.move_to(UP * CHAIN_Y),
                      time_span(FadeIn(q, shift=0.3 * DOWN), 0.6, 1.6), run_time=1.6)
        return chain, labels, q

    # hook.2: five, six, seven; you see three at a glance, a program can only ask the question
    def glance(self, chain, labels, q):
        cells = chain.cells
        three = T("3", size=60, color=GOLD).move_to(q[2])
        q_again = q[2].copy()
        root, lines, p_nil, p_cons = fork()
        the_fork = VGroup(root, lines, p_nil, p_cons)

        with self.say("c3.hook.2") as c:
            # "Take the list five, six, seven."  Each value lands on its spoken word.
            for lab, cell in zip(labels, cells):
                lab.move_to(cell.box)
            t0 = c.at("five")
            offs = [c.at(w) - t0 for w in ("five", "six", "seven")]
            c.wait_until("five")
            self.play(*[time_span(FadeIn(lab, shift=0.3 * DOWN), o, o + 0.7)
                        for lab, o in zip(labels, offs)], run_time=offs[-1] + 0.7)
            self.remove(*labels)
            for cell, lab in zip(cells, labels):
                cell.add(lab)            # the values belong to their cells from now on

            # "You can see at a glance": all three light up at once
            c.wait_until("glance")
            self.play(*[FlashAround(cell, color=YELLOW, time_width=1.5) for cell in cells],
                      *[lab.animate.set_color(YELLOW) for lab in labels], run_time=1.3)
            # "...that it has three elements."
            c.wait_until("three elements")
            self.play(FadeTransform(q[2], three), run_time=0.9)

            # "But a program can't see at a glance."  The 3 is gone again, and only the first
            # cell is visible to it.
            c.wait_until("cant")
            self.play(FadeTransform(three, q_again),
                      *[lab.animate.set_color(FG) for lab in labels],
                      *[m.animate.set_opacity(DIM_TO) for m in (*cells[1:], *chain.arrows, chain.nil)],
                      run_time=1.6)
            q = VGroup(q[0], q[1], q_again)

            # "All it can do is ask the question that pattern matching asks."
            c.wait_until("pattern matching")
            self.play(chain.animate.shift(DOWN * DROP), q.animate.shift(DOWN * DROP),
                      FadeIn(the_fork, shift=0.3 * DOWN), run_time=1.6)

            # "Is this list empty, or is it a head stuck onto a tail?"
            c.wait_until("is this list empty")
            hb = hl_box(p_nil)
            self.play(FadeIn(hb), run_time=0.8)
            c.wait_until("or is it")
            self.play(hb.animate.become(hl_box(p_cons)), run_time=0.8)
            c.wait_until("stuck onto")
            x_lab = Mono("x", size=44, color=YELLOW).next_to(cells[0].box, UP, buff=0.22)
            tail = VGroup(*cells[1:], chain.nil)
            brace = Brace(tail, UP, buff=0.12, color=TEAL)
            xs_lab = Mono("xs", size=44, color=TEAL).next_to(brace, UP, buff=0.1)
            x_lab.align_to(xs_lab, DOWN)
            self.play(TransformFromCopy(p_cons.find("x"), x_lab),
                      GrowFromCenter(brace),
                      TransformFromCopy(p_cons.find("xs"), xs_lab), run_time=1.5)

            # "So how do you count, using nothing but that question?"
            c.wait_until("count")
            self.play(FlashAround(q, color=GOLD, time_width=1.5), run_time=1.2)
            c.wait_until("that question")
            self.play(FlashAround(root, color=YELLOW, time_width=1.5), run_time=1.1)
        return q

    # hook.3: two answers; the first one's cost grows with the list, the second one's doesn't
    def twice(self, q):
        f1, h1 = slot(-SLOT_X, "version 1")
        f2, h2 = slot(SLOT_X, "version 2")
        cap1 = T("short and natural", size=34).move_to([f1.get_x(), f1.get_top()[1] - 0.6, 0])
        cap2 = T("same result", size=34).move_to([f2.get_x(), f2.get_top()[1] - 0.6, 0])
        l1, l2 = mini_list(f1), mini_list(f2)
        bar1, bar2 = cost_bar(l1, span(l1, 3)), cost_bar(l2, span(l2, 1.5))
        bar1_long = cost_bar(l1, span(l1, BOXES))
        c1 = T("cost", size=30, color=GOLD).next_to(bar1, DOWN, buff=0.18).align_to(bar1, LEFT)
        c2 = T("cost", size=30, color=GOLD).next_to(bar2, DOWN, buff=0.18).align_to(bar2, LEFT)
        acc = T("accumulator", size=42, color=YELLOW).move_to([f2.get_x(), f2.get_bottom()[1] + 0.6, 0])

        with self.say("c3.hook.3", gap=1.6) as c:   # a longer last hold: "accumulator" must be read
            # "We'll answer that twice in this chapter."  The question stays, at the top (P18).
            self.play(LaggedStart(*[FadeOut(m) for m in list(self.mobjects) if m not in q.get_family()
                                    and m is not q], lag_ratio=0.05),
                      q.animate.scale(0.85).move_to(UP * 3.2),
                      time_span(FadeIn(VGroup(f1, h1, f2, h2), shift=0.3 * DOWN, lag_ratio=0.15), 0.6, 1.8),
                      run_time=1.8)

            # "The first answer is short and natural,"
            c.wait_until("first")
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * DOWN) for b in l1[:3]], lag_ratio=0.25),
                      run_time=0.9)
            c.wait_until("short")
            self.play(FadeIn(cap1, shift=0.25 * DOWN), run_time=0.9)
            # "but it hides a cost that grows with the length of the list."
            c.wait_until("cost")
            self.play(GrowFromEdge(bar1, LEFT), FadeIn(c1, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("grows")
            self.play(LaggedStart(*[FadeIn(b) for b in l1[3:]], lag_ratio=1.0, rate_func=linear),
                      Transform(bar1, bar1_long, rate_func=linear),
                      run_time=c.until("second", floor=1.5) * 0.95)

            # "The second answer gives exactly the same result,"
            c.wait_until("second")
            self.play(LaggedStart(*[FadeIn(b, shift=0.2 * DOWN) for b in l2[:3]], lag_ratio=0.25),
                      FadeIn(cap2, shift=0.25 * DOWN),
                      time_span(GrowFromEdge(bar2, LEFT), 0.5, 1.3),
                      time_span(FadeIn(c2, shift=0.2 * DOWN), 0.5, 1.3), run_time=1.3)
            # "...without that cost."  Its list grows just as long; its bar doesn't move.
            c.wait_until("without")
            self.play(LaggedStart(*[FadeIn(b) for b in l2[3:]], lag_ratio=1.0, rate_func=linear),
                      run_time=1.6)

            # "It uses a trick called an accumulator, and you'll meet it again and again."
            c.wait_until("acc")
            self.play(FadeIn(acc, shift=0.3 * DOWN), run_time=0.9)
            c.wait_until("accumulator")
            self.play(FlashAround(acc, time_width=1.5), run_time=1.3)
