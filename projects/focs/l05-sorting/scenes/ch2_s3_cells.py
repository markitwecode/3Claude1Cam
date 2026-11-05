"""Chapter 2, scene 3: what insert copies -- ins 4 [3; 5; 9] copies 3, 4, 5 and shares the 9. Clips c2.cells.1 - c2.cells.4.

Layout (as L4 ch1_s5_cells): the old list 3 -> 5 -> 9 -> [] (ConsChain, BLUE, TEAL nil) at y = OLD_Y,
YELLOW pointer `old` on its 3 from the left. The new cells of `fresh` sit one row up (y = NEW_Y),
shifted one pitch left so the new 5 is right above the old 5; the new 5's arrow reaches down into
the ORIGINAL 9. Whole picture centred on x = 0 (new 3 at x = -4.2, old nil's right edge at x = 4.95).

New-cell styling (for ch2_s7_why's recap): new cells are ConsCell(v, color=YELLOW) (YELLOW box +
pointer outlines, FG value, BG fill), FG arrows between them; the shared 9 gets TEAL box/pointer
outlines and a TEAL 9 -> [] arrow, TEAL "shared" (T 34) above it. GOLD counter "new cells: 3"
(T 36) top right. Bottom band (y < -1) holds code: the toplevel session, ins's last line, costs.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

NEW_Y = 1.75        # fresh's new cells
OLD_Y = -0.1        # the old list
CODE_SIZE = 28
SESSION_TOP = -0.95  # top of the toplevel session block
TOP_BAND_Y = 3.05   # pointer label `fresh` and the GOLD counter
COST_A, COST_B = -1.3, -1.95   # the two GOLD cost lines
END_TOP = -2.55     # top of the ins 10 block

SESSION = [
    "let old = [3; 5; 9]",
    "val old : int list = [3; 5; 9]",
    "let fresh = ins 4 old",
    "val fresh : int list = [3; 4; 5; 9]",
    "List.tl (List.tl fresh) == List.tl old",
    "- : bool = false",
    "List.tl (List.tl (List.tl fresh))",
    "  == List.tl (List.tl old)",
    "- : bool = true",
]
END_SESSION = [
    "ins 10 [3; 5; 9]",
    "- : int list = [3; 5; 9; 10]",
]


def code_pointer(text, target, direction=UP, color=YELLOW, size=32, length=0.55):
    """A code name (Mono) with a short arrow pointing at `target`."""
    lab = Mono(text, size=size, color=color)
    tip = target.get_edge_center(direction)
    lab.next_to(tip, direction, buff=length + 0.1)
    arr = Arrow(lab.get_edge_center(-direction), tip, buff=0.08, stroke_width=3, color=color,
                max_tip_length_to_length_ratio=0.35, tip_length=0.15)
    return VGroup(lab, arr)


def pointer_arrow(start, end, color=FG):
    """Same look as lib.style.link, between arbitrary points."""
    return Arrow(start, end, buff=0, stroke_width=3, color=color,
                 max_tip_length_to_length_ratio=0.3, tip_length=0.16)


def pulse(arrow, color=TEAL, run_time=1.2):
    """A bright pulse travelling along an arrow."""
    path = Line(arrow.get_start(), arrow.get_end()).set_stroke(color, 8)
    return VShowPassingFlash(path, time_width=0.6, run_time=run_time)


def set_op_now(mob, op):
    """restyle(mob, op) applied instantly."""
    for leaf in mob.family_members_with_points():
        if leaf.get_fill_opacity() > 0:
            leaf.set_opacity(op)
        else:
            leaf.set_stroke(opacity=op)


def code_lines(srcs, size, top_y):
    """One Code per line, laid out exactly like the multi-line block (centred, top at top_y)."""
    ref = Code("\n".join(srcs), size=size)
    ref.move_to(ORIGIN).shift(UP * (top_y - ref.get_top()[1]))
    lines = []
    for i, src in enumerate(srcs):
        ln = Code(src, size=size)
        ln.shift(ref.line(i)[0].get_center() - ln.text[0].get_center())
        lines.append(ln)
    return ref, lines


def drop_inset():
    """L4 ch1_s5's drop picture in miniature: the rebuilt 9 points into the original 4 -> 7 -> []."""
    d = ConsChain([3, 5, 9, 4, 7])
    n9 = ConsCell(9, color=YELLOW).move_to(d.cells[2].get_center() + DOWN * 2.0)
    a9 = pointer_arrow(n9.tail_start(), d.cells[3].box.get_bottom() + LEFT * 0.2)
    for cell in (d.cells[3], d.cells[4]):
        cell.box.set_stroke(TEAL)
        cell.ptr.set_stroke(TEAL)
    d.arrows[3].set_color(TEAL)
    d.arrows[4].set_color(TEAL)
    pic = VGroup(d, n9, a9).scale(0.67)
    sh = T("shared", size=28, color=TEAL)
    sh.move_to([(d.cells[4].get_x() + d.nil.get_x()) / 2, d.get_bottom()[1] - 0.32, 0])
    set_op_now(VGroup(pic, sh), 0.7)
    cap = T("drop, Lecture 4", size=28, color=DIM)
    cap.move_to([d.get_left()[0], n9.get_y(), 0], aligned_edge=LEFT)   # under the 3 and 5
    body = VGroup(cap, pic, sh)
    frame = SurroundingRectangle(body, color=DIM, buff=0.2, corner_radius=0.15).set_stroke(width=2)
    inset = VGroup(frame, body).move_to([0, -2.17, 0])
    return inset, n9, VGroup(d.cells[3], d.cells[4], d.nil)


class WhatInsertCopies(NarratedScene):
    def construct(self):
        self.build()
        self.clip_cells()
        self.clip_shared()
        self.clip_check()
        self.clip_cost()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── pieces ────────────────────────────────────────────────────────────────
    def build(self):
        o = self.orig = ConsChain([3, 5, 9])
        pitch = o.cells[1].get_x() - o.cells[0].get_x()
        left = o.cells[0].get_left()[0] - pitch
        right = o.nil.get_right()[0]
        o.shift(RIGHT * (-(left + right) / 2) + UP * OLD_Y)
        x0 = o.cells[0].get_x()
        self.arrow_col = o.arrows[2].get_color()

        self.n3 = ConsCell(3, color=YELLOW).move_to([x0 - pitch, NEW_Y, 0])
        self.n4 = ConsCell(4, color=YELLOW).move_to([x0, NEW_Y, 0])
        self.n5 = ConsCell(5, color=YELLOW).move_to([x0 + pitch, NEW_Y, 0])
        self.a34 = link(self.n3, self.n4)
        self.a45 = link(self.n4, self.n5)
        self.a59 = pointer_arrow(self.n5.tail_start(), o.cells[2].box.get_top() + LEFT * 0.2)

        self.old_ptr = code_pointer("old", o.cells[0].box, LEFT)
        self.fresh_ptr = code_pointer("fresh", self.n3.box, UP)
        self.shared_lab = T("shared", size=34, color=TEAL).move_to(
            [(o.cells[2].get_x() + o.nil.get_x()) / 2, OLD_Y + 0.85, 0])
        self.count = T("new cells: 3", size=36, color=GOLD).move_to(
            [o.nil.get_right()[0], TOP_BAND_Y, 0], aligned_edge=RIGHT)
        self.count4 = T("new cells: 4", size=36, color=GOLD).move_to(
            [o.nil.get_right()[0], TOP_BAND_Y, 0], aligned_edge=RIGHT)

        self.frag1 = Code("then x :: y :: ys", size=40).move_to([0, -2.0, 0])
        self.inset, self.inset_n9, self.inset_tail = drop_inset()

        self.ref, self.lines = code_lines(SESSION, CODE_SIZE, SESSION_TOP)
        for ln in (self.lines[4], self.lines[7]):
            for g in ln.find("=="):
                g.set_color(YELLOW)

        self.frag2 = Code("else y :: ins x ys", size=36).move_to([0, -1.35, 0])
        self.waits = label_pointer("waits", self.frag2.find("y ::"), DOWN, YELLOW, size=32, length=0.5)
        self.cost1 = T("1 comparison + 1 copied cell per step", size=34, color=GOLD).move_to([0, COST_A, 0])
        self.cost2 = T("O(steps) time and space", size=34, color=GOLD).move_to([0, COST_B, 0])
        _, self.end_lines = code_lines(END_SESSION, 30, END_TOP)

        m = self.m10 = ConsChain([3, 5, 9, 10], color=YELLOW)
        m.shift(self.n3.get_center() - m.cells[0].get_center())

    # ── c2.cells.1: ins builds new cells ──────────────────────────────────────
    def clip_cells(self):
        o = self.orig
        with self.say("c2.cells.1") as c:
            parts = [o.cells[0], o.arrows[0], o.cells[1], o.arrows[1], o.cells[2], o.arrows[2], o.nil]
            self.play(LaggedStart(*[FadeIn(p, shift=0.2 * DOWN) for p in parts], lag_ratio=0.2),
                      run_time=min(2.0, c.until("old")))
            settle(self, o)

            c.wait_until("old")
            self.play(LaggedStart(*[FlashAround(cl, time_width=1.5) for cl in o.cells], lag_ratio=0.4),
                      run_time=min(2.2, c.until("call it old")))
            c.wait_until("call it old")
            self.play(FadeIn(self.old_ptr, shift=0.3 * RIGHT), run_time=1.0)

            c.wait_until("three")
            self.play(FlashAround(o.cells[0], time_width=1.5), run_time=1.2)
            c.wait_until("new tail")
            self.play(flash_along(o.cells[0], o.cells[1], YELLOW), run_time=1.2)
            c.wait_until("builds a new cell")
            self.play(TransformFromCopy(o.cells[0], self.n3), run_time=min(1.8, c.until("four") - 0.1))

            c.wait_until("four")
            self.play(FadeIn(self.n4, shift=0.3 * DOWN), time_span(GrowArrow(self.a34), 0.6, 1.4),
                      run_time=1.4)

            c.wait_until("five")
            self.play(FadeIn(self.frag1, shift=0.3 * UP), run_time=1.0)
            c.wait_until("why consed onto whys")
            self.box1 = token_box(self.frag1.find("y :: ys"), self.frag1)
            self.play(FadeIn(self.box1), run_time=0.8)
            c.wait_until("brand new cell")
            self.play(TransformFromCopy(o.cells[1], self.n5), time_span(GrowArrow(self.a45), 1.2, 2.0),
                      run_time=2.0)
            c.wait_until()

    # ── c2.cells.2: the 9 is shared ───────────────────────────────────────────
    def clip_shared(self):
        o = self.orig
        with self.say("c2.cells.2") as c:
            self.play(GrowArrow(self.a59),
                      Transform(self.box1, token_box(self.frag1.find("ys"), self.frag1)), run_time=1.4)
            c.wait_until("at the nine")
            self.play(FlashAround(o.cells[2], time_width=1.5), pulse(self.a59, YELLOW), run_time=1.2)

            c.wait_until("shared")
            teal = [o.cells[2].box.animate.set_stroke(TEAL), o.cells[2].ptr.animate.set_stroke(TEAL),
                    o.arrows[2].animate.set_color(TEAL)]
            self.play(*teal, FadeIn(self.shared_lab, shift=0.3 * DOWN),
                      FlashAround(VGroup(o.cells[2], o.arrows[2], o.nil), color=TEAL, time_width=1.5),
                      run_time=1.4)

            c.wait_until("drop")
            self.play(FadeOut(self.frag1), FadeOut(self.box1),
                      time_span(FadeIn(self.inset, shift=0.3 * UP), 0.4, 1.4), run_time=1.4)
            c.wait_until("rebuilt a single cell")
            self.play(FlashAround(self.inset_n9, time_width=1.5), run_time=1.2)
            c.wait_until("shared the rest")
            self.play(FlashAround(self.inset_tail, color=TEAL, time_width=1.5), run_time=1.2)
            c.wait_until()

    # ── c2.cells.3: check it with == ──────────────────────────────────────────
    def clip_check(self):
        o, L, ref = self.orig, self.lines, self.ref
        dy = UP * (ref.line(0)[0].get_y() - ref.line(2)[0].get_y())   # scroll by two lines
        with self.say("c2.cells.3") as c:
            self.play(FadeOut(self.inset), time_span(FadeIn(L[0]), 0.4, 1.1),
                      time_span(FadeIn(L[1]), 0.8, 1.5), run_time=1.5)
            c.wait_until("call the answer fresh")
            self.play(FadeIn(L[2]), time_span(FadeIn(L[3]), 0.4, 1.2),
                      FadeIn(self.fresh_ptr, shift=0.3 * DOWN), run_time=1.2)

            c.wait_until("two equals signs")
            self.play(FadeIn(L[4]), run_time=0.9)
            c.wait_until("same cells in memory")
            self.play(FlashUnder(L[4].find("=="), color=YELLOW, time_width=1.5), run_time=1.2)

            c.wait_until("five2")
            for ln in L[5:]:
                ln.shift(dy)
            box = token_box(L[4].find("List.tl (List.tl fresh)"), L[4]).shift(dy)
            self.play(FadeOut(L[0]), FadeOut(L[1]), *[ln.animate.shift(dy) for ln in L[2:5]],
                      run_time=0.9)
            self.play(FadeIn(box), FlashAround(self.n5, time_width=1.5), run_time=1.2)
            c.wait_until("the five in old")
            self.play(Transform(box, token_box(L[4].find("List.tl old"), L[4])),
                      FlashAround(o.cells[1], time_width=1.5), run_time=1.2)

            c.wait_until("false")
            self.play(FadeOut(box), FadeIn(L[5]), FlashAround(self.n5, time_width=1.5),
                      FlashAround(o.cells[1], time_width=1.5), run_time=1.2)

            c.wait_until("nine")
            for ln in L[6:]:
                ln.shift(dy)
            self.play(FadeOut(L[2]), FadeOut(L[3]), *[ln.animate.shift(dy) for ln in L[4:6]],
                      time_span(FadeIn(L[6]), 0.5, 1.2), time_span(FadeIn(L[7]), 0.6, 1.3),
                      FlashAround(o.cells[2], color=TEAL, time_width=1.5), run_time=1.3)
            c.wait_until("so that one gives true")
            self.play(FadeIn(L[8]), pulse(self.a59), flash_along(o.cells[1], o.cells[2], TEAL),
                      FlashAround(o.cells[2], color=TEAL, time_width=1.5),
                      run_time=max(0.6, min(1.2, c.remaining - 0.05)))
            c.wait_until()

    # ── c2.cells.4: work waits, and the cost ──────────────────────────────────
    def clip_cost(self):
        o, L, E = self.orig, self.lines, self.end_lines
        with self.say("c2.cells.4") as c:
            self.play(*[time_span(FadeOut(ln), 0.6, 1.4) for ln in L[4:]],
                      time_span(FadeIn(self.frag2, shift=0.3 * UP), 1.0, 1.8), run_time=1.8)
            yc = self.frag2.find("y ::")
            self.play(*recolor(yc, YELLOW), FlashAround(yc, time_width=1.5),
                      FadeIn(self.waits, shift=0.3 * UP), run_time=1.2)

            c.wait_until("each item it walks past")
            self.play(FlashAround(o.cells[0], time_width=1.5), run_time=1.2)
            c.wait_until("consed onto the answer")
            self.play(FlashAround(self.n3, time_width=1.5), FlashAround(yc, time_width=1.5), run_time=1.3)

            c.wait_until("cost")
            self.play(FadeIn(self.count, shift=0.3 * DOWN),
                      *[FlashAround(m, color=GOLD, time_width=1.5) for m in (self.n3, self.n4, self.n5)],
                      run_time=1.4)

            c.wait_until("each step takes")
            self.play(FadeOut(self.frag2), FadeOut(self.waits),
                      time_span(FadeIn(self.cost1, shift=0.2 * UP), 0.4, 1.2), run_time=1.2)
            c.wait_until("time and space")
            self.play(FadeIn(self.cost2, shift=0.2 * UP), run_time=1.0)

            c.wait_until("end")
            gone = [self.n3, self.n4, self.n5, self.a34, self.a45, self.a59, self.fresh_ptr,
                    self.shared_lab]
            restore = [o.cells[2].box.animate.set_stroke(BLUE), o.cells[2].ptr.animate.set_stroke(BLUE),
                       o.arrows[2].animate.set_color(self.arrow_col)]
            self.play(*[FadeOut(m) for m in gone], *restore,
                      time_span(FadeIn(E[0], shift=0.2 * UP), 0.5, 1.2), run_time=1.2)
            m = self.m10
            self.play(LaggedStart(TransformFromCopy(o.cells[0], m.cells[0]),
                                  TransformFromCopy(o.cells[1], m.cells[1]),
                                  TransformFromCopy(o.cells[2], m.cells[2]),
                                  FadeIn(m.cells[3], shift=0.3 * DOWN), lag_ratio=0.3),
                      run_time=min(2.2, max(1.2, c.until("walks to the very end") - 0.05)))
            c.wait_until("walks to the very end")
            self.play(*[GrowArrow(a) for a in m.arrows], FadeIn(m.nil, shift=0.2 * LEFT),
                      FadeIn(E[1], shift=0.2 * UP), Transform(self.count, self.count4), run_time=1.3)
            c.wait_until("copying the whole list")
            self.play(FlashAround(VGroup(*m.cells, m.nil), color=GOLD, time_width=1.5),
                      FlashAround(self.count4, color=GOLD, time_width=1.5),
                      run_time=max(0.8, min(1.5, c.remaining - 0.1)))
            c.wait_until()
