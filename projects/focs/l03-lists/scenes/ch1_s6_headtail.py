"""Chapter 1, scene 6: head and tail on the cell chain, tails of tails down to nil,
walking to the last element (O(n)), the answer to the opening question, the empty
list, and the chapter recap.

Clips c1.ht.1 - c1.ht.4, c1.recap.1 (the chapter's last scene).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, select, time_span  # noqa: E402
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S = 1.2                              # the chain is the hero: 3 cells + nil span ~63% of the width
STEP = (CELL + PTR_W + LINK) * S     # distance between neighbouring cells
ROW_Y = 0.0                          # height of the cell row (frame balanced vertically)
DIM_TO = 0.25                        # spotlight: everything else fades to this (PATTERNS P9)


# ── helpers (local to this scene) ───────────────────────────────────────────────
def slink(src, dst, color=FG):
    """lib.style.link at this scene's scale (tip scaled like the chain's own arrows)."""
    return Arrow(src.tail_start(), dst.entry(), buff=0, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16 * S)


def flash_along(src, dst, color=YELLOW, run_time=1.0):
    """A bright pulse travelling along one pointer arrow."""
    path = Line(src.tail_start(), dst.entry()).set_stroke(color, 8)
    return VShowPassingFlash(path, time_width=0.6, run_time=run_time)


def tail_row(arg, result):
    """`tail of [3; 5; 9]  =  [5; 9]`, as four parts so rows can be column-aligned."""
    return [T("tail of", size=38, t2c={"tail": YELLOW}), Code(arg, size=38),
            T("=", size=38), Code(result, size=38)]


def align_rows(rows, ys, gaps=(0.3, 0.45, 0.45)):
    """Lay out rows of parts in columns: col 0 right-aligned, the rest left-aligned."""
    widths = [max(r[i].width for r in rows) for i in range(len(rows[0]))]
    xs = [0.0]
    for i in range(1, len(widths)):
        xs.append(xs[-1] + widths[i - 1] + gaps[i - 1])
    total = xs[-1] + widths[-1]
    for row, y in zip(rows, ys):
        for i, part in enumerate(row):
            part.set_y(y)
            if i == 0:
                part.align_to(np.array([xs[0] + widths[0] - total / 2, 0, 0]), RIGHT)
            else:
                part.align_to(np.array([xs[i] - total / 2, 0, 0]), LEFT)
    return [VGroup(*r) for r in rows]


def opacity(mobs, value):
    # A list, to unpack into play(). An AnimationGroup would add a new Group of these
    # (already on screen) mobjects on top of the scene and change the drawing order.
    return [m.animate.set_opacity(value) for m in mobs]


class HeadAndTail(NarratedScene):
    def construct(self):
        chain = ConsChain([3, 5, 9]).scale(S).move_to(UP * ROW_Y)
        self.head_tail(chain)
        self.tails_of_tails(chain)
        self.walk_to_end(chain)
        self.empty_list()
        self.recap()

    # ht.1: head = the value in the first cell, tail = where its arrow points; both O(1)
    def head_tail(self, chain):
        cells = chain.cells
        head_eq = VGroup(T("head", size=42, color=YELLOW), T("=", size=42)).arrange(RIGHT, buff=0.2)
        head_val = value_label(3, size=46, color=YELLOW)
        head_lab = VGroup(head_eq, head_val).arrange(RIGHT, buff=0.2)
        head_lab.next_to(cells[0].box, UP, buff=0.45)
        tail_box = SurroundingRectangle(VGroup(cells[1], cells[2], chain.nil), color=YELLOW, buff=0.18)
        tail_lab = T("tail", size=42, color=YELLOW).next_to(tail_box, UP, buff=0.3)
        tail_lab.align_to(head_eq[0], DOWN)
        head_o = MathTex(r"O(1)", font_size=60, color=GOLD).next_to(tail_box, DOWN, buff=0.4)
        head_o.set_x(cells[0].box.get_x())
        tail_o = MathTex(r"O(1)", font_size=60, color=GOLD).next_to(tail_box, DOWN, buff=0.4)

        with self.say("c1.ht.1") as c:
            # "Taking a list apart is just as cheap as building one."
            self.play(FadeIn(chain, shift=0.3 * UP), run_time=1.5)

            # "The head of a list is the value in its first cell."  (the 3 comes out of the cell, P5)
            c.wait_until("head")
            self.play(FlashAround(cells[0].box, time_width=1.5), cells[0].box.animate.set_stroke(YELLOW),
                      FadeIn(head_eq, shift=0.25 * DOWN), run_time=1.2)
            self.play(TransformFromCopy(cells[0].label, head_val), run_time=1.5)

            # "The tail is wherever the first cell's arrow points."
            c.wait_until("tail")
            self.play(flash_along(cells[0], cells[1]), chain.arrows[0].animate.set_color(YELLOW), run_time=1.2)
            c.wait_until("points")
            self.play(Create(tail_box), FadeIn(tail_lab, shift=0.25 * DOWN), run_time=1.3)

            # "Each of these just follows one arrow, so both take constant time."
            c.wait_until("one arrow")
            self.play(FlashAround(cells[0].box, time_width=1.5), flash_along(cells[0], cells[1]), run_time=1.0)
            c.wait_until("constant time")
            self.play(FadeIn(head_o, shift=0.25 * UP), FadeIn(tail_o, shift=0.25 * UP), run_time=1.0)
        self.ht_bits = VGroup(head_lab, tail_box, tail_lab, head_o, tail_o)
        self.tail_lab = tail_lab

    # ht.2: the tail is not the last element; tails of tails down to nil
    def tails_of_tails(self, chain):
        cells = chain.cells
        red_box = SurroundingRectangle(cells[2], color=RED, buff=0.14)
        warn = MathTex(r"\text{tail} \neq \text{last element}", font_size=52, color=RED).move_to(UP * 2.75)

        boxes = [SurroundingRectangle(VGroup(*cells[i:], chain.nil), color=YELLOW, buff=0.18)
                 for i in (1, 2)] + [SurroundingRectangle(chain.nil, color=YELLOW, buff=0.18)]
        boxes[2].match_height(boxes[0])
        rows = align_rows([tail_row("[3; 5; 9]", "[5; 9]"),
                           tail_row("[5; 9]", "[9]"),
                           tail_row("[9]", "[]")],
                          ys=[-1.5, -2.3, -3.1])

        def spot(i):
            """peel cell i off: it and its arrow fade into the background"""
            return opacity([cells[i], chain.arrows[i]], DIM_TO)

        def next_row(i):
            """row i+1 comes out of row i: its argument IS the previous result (P5/P11)"""
            a, b = rows[i], rows[i + 1]
            return [TransformFromCopy(a[0], b[0]), TransformFromCopy(a[3], b[1])]

        with self.say("c1.ht.2") as c:
            # "But be careful with that word, tail."  (underline + a colour change that stays, P7)
            c.wait_until("tail")
            self.play(FlashUnder(self.tail_lab, color=RED, time_width=1.5),
                      self.tail_lab.animate.set_color(RED), run_time=1.2)
            # "It's easy to think the tail is the last element."  The head/tail picture and its
            # O(1)s stay up until the red box needs the chain.
            c.wait_until("last element")
            self.play(LaggedStart(*[FadeOut(m) for m in self.ht_bits], lag_ratio=0.1),
                      cells[0].box.animate.set_stroke(BLUE), chain.arrows[0].animate.set_color(FG),
                      Create(red_box), run_time=1.2)
            for m in (*cells, *chain.arrows, chain.nil):
                m.save_state()   # restored in ht.3, after the peeling
            # "It isn't."
            c.wait_until("it isn't")
            self.play(FadeIn(warn, shift=0.25 * DOWN), run_time=1.0)

            # "The tail of three, five, nine is the whole rest of the list: five, nine."
            c.wait_until("rest")
            self.play(FadeOut(red_box), FadeIn(VGroup(rows[0][0], rows[0][1]), shift=0.25 * DOWN), run_time=1.0)
            c.wait_until("whole rest")
            self.play(*spot(0), Create(boxes[0]), run_time=1.5)
            c.wait_until("five", nth=1)
            self.play(FadeIn(VGroup(rows[0][2], rows[0][3]), shift=0.25 * DOWN), run_time=1.0)

            # "And the tail of that is the list containing just nine."
            c.wait_until("tailtail")
            self.play(*next_row(0), run_time=1.5)
            c.wait_until("containing just nine")
            self.play(Transform(boxes[0], boxes[1]), *spot(1),
                      FadeIn(VGroup(rows[1][2], rows[1][3]), shift=0.25 * DOWN), run_time=1.3)

            # "And the tail of that is nil."
            c.wait_until("nil")
            self.play(*next_row(1), run_time=c.until("is nil", floor=0.8))
            self.play(Transform(boxes[0], boxes[2]), *spot(2),
                      FadeIn(VGroup(rows[2][2], rows[2][3]), shift=0.25 * DOWN), run_time=1.0)
        self.tt_box = boxes[0]
        self.tt_text = VGroup(warn, *rows)

    # ht.3: the last element means walking every arrow: O(n). Then the opening question.
    def walk_to_end(self, chain):
        cells, arrows, nil = chain.cells, chain.arrows, chain.nil
        everything = [*cells, *arrows, nil]
        last = label_pointer("last element", cells[2], direction=UP, color=FG, size=38)
        marker = SurroundingRectangle(cells[0], color=YELLOW, buff=0.14, stroke_width=5)
        steps = [T(str(i + 1), size=42, color=GOLD).next_to(cells[i], DOWN, buff=0.35) for i in range(3)]
        on = MathTex(r"O(n)", font_size=76, color=GOLD).move_to(DOWN * 2.45)
        per = T("one step per element", size=34, color=DIM).next_to(on, DOWN, buff=0.18)

        # the answer: room for a new cell on the front, then a walk along the whole list
        recentre = RIGHT * STEP / 2
        new = ConsCell(1, color=YELLOW).scale(S).move_to(cells[0].get_center() + LEFT * STEP + recentre)
        rows = align_rows([[T("front:", size=40), T("one step", size=40),
                            MathTex(r"O(1)", font_size=58, color=GOLD)],
                           [T("end:", size=40), T("walk the whole list", size=40),
                            MathTex(r"O(n)", font_size=58, color=GOLD)]],
                          ys=[-1.6, -2.7], gaps=(0.35, 0.8))

        with self.say("c1.ht.3") as c:
            # "So what if you really do want the last element?"  The chain comes back to full;
            # the tails derivation stays readable below it a little longer.
            c.wait_until("last element")
            self.play(FadeOut(self.tt_box), *[Restore(m) for m in everything],
                      FadeIn(last, shift=0.25 * DOWN), run_time=1.5)
            for m in everything:
                m.save_state()
            # "Then there's no shortcut."  The tails make way for the walk.
            c.wait_until("no shortcut")
            self.play(LaggedStart(*[FadeOut(m) for m in self.tt_text], lag_ratio=0.1), run_time=1.0)

            # "You have to start at the front, and follow the arrows, one by one, all the way to
            # the end."  A cursor walks the chain; everything else fades to 25% (PATTERNS §3).
            c.wait_until("start at the front")
            self.play(*opacity([*cells[1:], *arrows, nil], DIM_TO), Create(marker),
                      FadeIn(steps[0], shift=0.2 * DOWN), run_time=1.2)
            for i, cue in ((1, "follow the arrows"), (2, "by one")):
                c.wait_until(cue)
                self.play(cells[i - 1].animate.set_opacity(DIM_TO), arrows[i - 1].animate.set_opacity(1),
                          cells[i].animate.set_opacity(1),
                          marker.animate.move_to(cells[i]), FadeIn(steps[i], shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("to the end")
            self.play(*opacity([arrows[2], nil], 1), flash_along(cells[2], nil), run_time=0.9)

            # "For a list with a million elements, that's a million steps."
            c.wait_until("million")
            self.play(*[Restore(m) for m in everything], Write(on),
                      FadeIn(per, shift=0.25 * UP), run_time=1.6)

            # "And that's the answer to our opening question."  Keep the chain and the O(n) (P18):
            # the O(n) goes straight to its slot in the answer table.
            # The caption waits in row 2 too, and becomes "walk the whole list" below.
            c.wait_until("answer")
            per.generate_target()
            per.target.align_to(rows[1][1], LEFT).set_y(rows[1][1].get_y())
            self.play(LaggedStart(*[FadeOut(m) for m in (marker, *steps, last)], lag_ratio=0.1),
                      chain.animate.shift(recentre), ReplacementTransform(on, rows[1][2]),
                      MoveToTarget(per), run_time=1.5)
            new_arrow = slink(new, cells[0], color=YELLOW)

            # "Adding to the front is one step."
            c.wait_until("adding to the front")
            self.play(FadeIn(new, shift=0.4 * RIGHT), GrowArrow(new_arrow),
                      FadeIn(rows[0], shift=0.25 * DOWN), run_time=1.5)

            # "But anything at the end of a list means walking the whole length of it."
            c.wait_until("but anything")
            path = [new, *cells, nil]
            self.play(Succession(*[flash_along(a, b) for a, b in zip(path, path[1:])]),
                      FadeTransform(per, rows[1][1]), FadeIn(rows[1][0], shift=0.25 * DOWN), run_time=2.0)
        self.walk_bits = VGroup(chain, new, new_arrow)
        self.table = VGroup(*rows)

    # ht.4: the empty list has no head and no tail; then the question, left hanging (P23)
    def empty_list(self):
        nil = Nil(size=130).move_to(UP * 0.5)
        no_head = T("no head", size=44).move_to(LEFT * 2.3 + DOWN * 0.95)
        no_tail = T("no tail", size=44).move_to(RIGHT * 2.3 + DOWN * 0.95)
        question = VGroup(T("head", size=44, color=YELLOW), T("of", size=44), Code("[]", size=44),
                          T("=", size=44), T("?", size=84, color=GOLD)).arrange(RIGHT, buff=0.3)
        question.move_to(DOWN * 2.45)

        with self.say("c1.ht.4") as c:
            # "One last thing to notice."  The chain goes; the answer table (the chapter's payoff)
            # stays, smaller, at the top (P18).
            # (the chain is gone before the table slides up through its place)
            self.play(time_span(FadeOut(self.walk_bits), 0, 0.6),
                      time_span(self.table.animate.scale(0.75).move_to(UP * 2.75), 0.5, 1.6), run_time=1.6)
            # "The empty list has no first cell."
            c.wait_until("the empty list")
            self.play(FadeIn(nil, scale=0.8), run_time=1.2)
            # "So it has no head, and no tail."
            c.wait_until("no head")
            self.play(FadeIn(no_head, shift=0.25 * UP), run_time=1.0)
            c.wait_until("no tail")
            self.play(FadeIn(no_tail, shift=0.25 * UP), run_time=1.0)
            # "What should happen if you ask for one anyway?"  The question goes on screen and
            # stays: the answer is the next chapter.
            c.wait_until("ask")
            self.play(TransformFromCopy(select(no_head, "head")[0], question[0]),
                      FadeIn(question[1:], shift=0.25 * DOWN), run_time=1.1)
        self.empty_bits = VGroup(nil, no_head, no_tail, question)

    # recap.1: four lines, each built on its cue while the earlier ones step back; then the teaser
    def recap(self):
        title = T("Recap", size=52).to_edge(UP, buff=0.6)
        lines = [
            T("A list is a sequence of elements, all of one type", size=38),
            VGroup(T("Every list is", size=38), Code("[]", size=36), T("or", size=38),
                   Code("head :: tail", size=36)).arrange(RIGHT, buff=0.25),
            VGroup(T("Cons, head and tail are all", size=38), MathTex(r"O(1)", font_size=52, color=GOLD),
                   T("(one arrow each)", size=38, color=DIM)).arrange(RIGHT, buff=0.25),
            T("Lists never change, so they can share cells", size=38, t2c={"share cells": TEAL}),
        ]
        rows = VGroup(*[VGroup(Dot(radius=0.07, color=BLUE), ln).arrange(RIGHT, buff=0.3) for ln in lines])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to(UP * 0.35)
        nxt = VGroup(T("Next:", size=44, color=DIM), T("pattern matching", size=44, color=YELLOW))
        nxt.arrange(RIGHT, buff=0.25).move_to(DOWN * 2.85)

        with self.say("c1.recap.1") as c:
            # "Let's recap."
            self.play(LaggedStart(*[FadeOut(m) for m in (self.table, *self.empty_bits)], lag_ratio=0.1),
                      FadeIn(title, shift=0.3 * DOWN), run_time=c.until("r1", floor=0.8))
            for i, cue in enumerate(("r1", "r2", "r3", "r4")):
                c.wait_until(cue)
                anims = [FadeIn(rows[i], shift=0.25 * UP, lag_ratio=0.02)]
                if i:
                    anims.append(rows[i - 1].animate.set_opacity(0.5))
                self.play(*anims, run_time=1.5)
            # "Next time: taking lists apart properly, with pattern matching."  The whole recap
            # comes back to full brightness under the teaser.
            c.wait_until("next")
            self.play(*[r.animate.set_opacity(1) for r in rows[:3]], FadeIn(nxt, shift=0.25 * UP), run_time=1.2)

        # End card: the finished recap and the teaser hold, fully visible, under the music.
        self.wait(8.0)
        # the end of the chapter: a calm fade to an empty screen
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.3)
        self.wait(0.15)  # the last play() never renders its final (empty) frame
