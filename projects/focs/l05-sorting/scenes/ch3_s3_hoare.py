"""Chapter 3, scene 3: Hoare's idea. Clips c3.hoare.1 – c3.hoare.4.

Exports for the recap (s7): array_row(values), swap_arcs(row), hoare_row(), copies_icon().
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

BOX = 1.25          # array box side
ARC_Y = 0.12        # arcs start this far above the boxes' top


def array_row(values, pivot=5, side=BOX):
    """A row of touching BLUE square boxes (no pointers) holding values; the pivot YELLOW.
    Centred on ORIGIN. .boxes, .labels (VGroups, left to right)."""
    boxes = VGroup(*[Square(side_length=side).set_stroke(BLUE, 4).set_fill(BG, 0) for _ in values])
    boxes.arrange(RIGHT, buff=0)
    labels = VGroup(*[value_label(v, size=48 * side / BOX, color=YELLOW if v == pivot else FG)
                      .move_to(b) for v, b in zip(values, boxes)])
    row = VGroup(boxes, labels)
    row.boxes, row.labels = boxes, labels
    return row


def _arc(row, i, j, angle, color=YELLOW, inset=0.12):
    """A double-headed arc above the row from box i to box j (i < j)."""
    top = row.boxes[0].get_top()[1] + ARC_Y * row.boxes[0].height / BOX
    a = np.array([row.boxes[i].get_x() + inset, top, 0])
    b = np.array([row.boxes[j].get_x() - inset, top, 0])
    arc = ArcBetweenPoints(a, b, angle=angle).set_stroke(color, 3)
    tl = 0.18 * row.boxes[0].height / BOX
    arc.add_tip(tip_length=tl, tip_width=tl)
    arc.add_tip(tip_length=tl, tip_width=tl, at_start=True)
    return arc


def swap_arcs(row):
    """The two swaps of Hoare's partition on a 5-box row: boxes 2<->3 (9 and 4), then 0<->2 (pivot)."""
    return VGroup(_arc(row, 2, 3, -0.75 * PI), _arc(row, 0, 2, -0.5 * PI))


def hoare_row():
    """The finished picture: 4 3 5 9 7 with its two swap arcs."""
    row = array_row([4, 3, 5, 9, 7])
    return VGroup(row, swap_arcs(row))


def copies_icon():
    """A small chain of new YELLOW cells with a GOLD 'copies' tag above it."""
    chain = ConsChain([3, 4], color=YELLOW).scale(0.6)
    tag = T("copies", 32, GOLD).next_to(chain, UP, buff=0.25)
    return VGroup(chain, tag)


class HoareIdea(NarratedScene):
    def construct(self):
        self.card_intro()
        self.array_part()
        self.history()
        self.list_version()
        self.wait(2.5)   # let the finished split and "easier to follow" sit before the fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ c3.hoare.1
    def card_intro(self):
        name = T("Sir Tony Hoare", 60, YELLOW).move_to(UP * 1.0)
        dates = T("1934–2026", 40, GOLD).next_to(name, DOWN, buff=0.35)
        l1 = T("quicksort: Moscow State University, 1959", 34, DIM)
        l2 = T("later: Microsoft Research, Cambridge", 34, DIM)
        l3 = T("died 5 March 2026, aged 92", 34, DIM)
        VGroup(l1, l2, l3).arrange(DOWN, buff=0.35).next_to(dates, DOWN, buff=0.7)
        self.name, self.dates, self.lines = name, dates, (l1, l2, l3)
        with self.say("c3.hoare.1") as c:
            self.play(*appear(name, dates, lag=0.4), run_time=1.4)
            c.wait_until("moscow")
            self.play(*appear(l1), run_time=1.0)
            c.wait_until("msr")
            self.play(*appear(l2), run_time=1.0)
            c.wait_until("died")
            self.play(*appear(l3), run_time=1.0)

    # ------------------------------------------------------------------ c3.hoare.2
    def array_part(self):
        row = array_row([5, 3, 9, 4, 7]).move_to(RIGHT * 2.3)
        self.row = row
        slot = list(row.labels)                     # which label sits in box i
        lab = T("array", 32, DIM).next_to(row, DOWN, buff=0.35)
        inplace = T("in place", 38, GREEN).move_to([row.get_x(), 2.25, 0])
        arcs = swap_arcs(row)
        self.arcs = arcs

        def ptr(i):
            m = marker(BLUE).rotate(PI)
            return m.next_to(row.boxes[i], DOWN, buff=0.14)

        card = self.card = VGroup(self.name, self.dates)
        with self.say("c3.hoare.2") as c:
            self.play(*during(disappear(*self.lines), 0, 0.45),
                      card.animate.scale(0.7).move_to(LEFT * 4.7 + UP * 0.2),
                      run_time=1.4)
            self.play(*appear(*row.boxes, lag=0.12),
                      *during(appear(*row.labels, lag=0.12), 0.3, 1), run_time=1.4)
            self.play(*appear(lab), run_time=0.8)
            c.wait_until(own_word=inplace)
            self.play(*appear(inplace), run_time=1.0)

            c.wait_until("swap")
            pl, pr = ptr(1), ptr(4)
            self.play(*during(disappear(lab), 0, 0.45),
                      *during(appear(pl, pr, shift=0.2 * UP), 0.4, 1), run_time=1.2)
            c.wait_until("bigger than the pivot")
            self.play(pl.animate.move_to(ptr(2)), run_time=1.0)
            self.play(*flash([slot[2]], color=RED), run_time=1.0)
            c.wait_until("at most the pivot")
            self.play(pr.animate.move_to(ptr(3)), run_time=1.0)
            self.play(*flash([slot[3]], color=GREEN), run_time=1.0)
            c.wait_until("swaps them")
            a, b = slot[2], slot[3]
            self.play(*during([Create(arcs[0])], 0, 0.4),
                      *during([a.animate(path_arc=PI).move_to(row.boxes[3]),
                               b.animate(path_arc=PI).move_to(row.boxes[2])], 0.3, 1),
                      run_time=1.6)
            slot[2], slot[3] = b, a

            c.wait_until("middle")
            p, q = slot[0], slot[2]
            self.play(*during(disappear(pl, pr), 0, 0.3),
                      *during([Create(arcs[1])], 0.1, 0.45),
                      *during([p.animate(path_arc=-PI).move_to(row.boxes[2]),
                               q.animate(path_arc=-PI).move_to(row.boxes[0])], 0.35, 1),
                      run_time=1.8)
            slot[0], slot[2] = q, p

            c.wait_until("nonew")
            bl = span_brace(row.boxes[0].get_corner(DL), row.boxes[1].get_corner(DR), color=FG)
            br = span_brace(row.boxes[3].get_corner(DL), row.boxes[4].get_corner(DR), color=FG)
            tl = T("≤ 5", 36).next_to(bl, DOWN, buff=0.15)
            tr = T("> 5", 36).next_to(br, DOWN, buff=0.15)
            self.play(GrowFromCenter(bl), GrowFromCenter(br),
                      *during(appear(tl, tr, lag=0.2), 0.4, 1), run_time=1.2)
            nonew = T("no new cells", 38, GREEN).next_to(VGroup(tl, tr), DOWN, buff=0.45)
            nonew.set_x(row.get_x())
            c.wait_until("anything new")
            self.play(*appear(nonew), run_time=1.0)
        self.array_stuff = [row, arcs, bl, br, tl, tr, inplace, nonew]

    # ------------------------------------------------------------------ c3.hoare.3
    def history(self):
        tag = T("before recursion was well known", 32, DIM).move_to([self.row.get_x(), 3.2, 0])
        quote = T("“Tony, I don't care if\nthe program talks to itself,\n"
                  "as long as it doesn't do it\non company time.”",
                  38, slant=ITALIC, line_spacing=1.0).move_to([self.row.get_x(), 0.5, 0])
        attr = T("his manager at Elliott Brothers, 1960s\n(Computer History Museum)", 28, DIM,
                 line_spacing=0.9).next_to(quote, DOWN, buff=0.6)
        self.tag = tag
        with self.say("c3.hoare.3") as c:
            self.play(*set_alpha(self.array_stuff, DIMMED),
                      *during(appear(tag), 0.3, 1), run_time=1.4)
            c.wait_until("manager")
            sweep_clear(self, keep=[self.card, tag], run_time=1.0)
            c.wait_until("the reply was this")
            self.play(*appear(quote, attr, lag=0.3), run_time=1.4)  # early: the reply is read out right after
        self.quote = quote

    # ------------------------------------------------------------------ c3.hoare.4
    def list_version(self):
        chain = ConsChain([5, 3, 9, 4, 7]).scale(0.8).move_to(UP * 1.2)
        left = ConsChain([3, 4], color=YELLOW).scale(0.8).move_to([-4.0, -1.5, 0])
        right = ConsChain([9, 7], color=YELLOW).scale(0.8).move_to([4.0, -1.5, 0])
        piv = ConsCell(5, color=YELLOW).scale(0.8).move_to([0, -0.7, 0])
        piv.label.set_color(YELLOW)
        le = T("≤ 5", 36).next_to(left, DOWN, buff=0.3)
        gt = T("> 5", 36).next_to(right, DOWN, buff=0.3)
        copies = T("copies", 34, GOLD).move_to([0, le.get_y(), 0])
        easier = T("easier to follow", 38, GREEN).next_to(copies, DOWN, buff=0.35)
        card = self.card

        def rest(part):
            return [*part.arrows, part.nil]

        with self.say("c3.hoare.4") as c:
            sweep_clear(self, keep=[self.card], run_time=1.0)
            self.play(card.animate.to_corner(UL, buff=0.45), run_time=1.0)
            self.play(*appear(*chain.cells, *chain.arrows, chain.nil, lag=0.08, shift=None),
                      run_time=1.2)
            c.wait_until("copies")
            self.play(*fly(chain.cells[0], piv),
                      *during(fly(chain.cells[1], left.cells[0]), 0.1, 0.8),
                      *during(fly(chain.cells[3], left.cells[1]), 0.2, 0.9),
                      *during(appear(*rest(left), le, copies, lag=0.15), 0.6, 1),
                      run_time=1.7)
            self.play(*during(fly(chain.cells[2], right.cells[0]), 0, 0.7),
                      *during(fly(chain.cells[4], right.cells[1]), 0.1, 0.8),
                      *during(appear(*rest(right), gt, lag=0.15), 0.55, 1),
                      run_time=1.5)
            c.wait_until(own_word=easier)
            self.play(*appear(easier), run_time=1.0)
