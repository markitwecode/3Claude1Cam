"""Chapter 1, scene 5: copied or shared -- take copies its cells, drop shares the tail. Clips c1.cells.1 - c1.cells.4.

Layout: the running chain 3 -> 5 -> 9 -> 4 -> 7 -> [] (ConsChain, BLUE, TEAL nil) across y = 0.
take's new cells sit right above their originals (y = TAKE_Y), drop's one new 9 right below
the original 9 (y = NEW9_Y), its arrow reaching up into the original 4.

New-cell styling (for ch1_s6_cost): take's cells and drop's new 9 are ConsCell(v, color=YELLOW)
(YELLOW box + pointer outlines, FG value, BG fill); take's own nil is a plain Nil() (TEAL);
the shared 4 -> 7 -> [] gets TEAL box/pointer outlines and TEAL arrows.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, VShowPassingFlash, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TAKE_Y = 1.85       # take's new cells, above the original
NEW9_Y = -2.0       # drop's one new cell, below
SINK = 0.8          # how far the diagram drops to make room for the toplevel check
ROW_UP = 1.2        # the glued row sits at y = -SINK + ROW_UP
COL_X = 1.5         # left edge of the GOLD "new cells" counters
CODE_SIZE = 28      # the 53-character == line needs 28 to fit the frame

SESSION = [
    "let xs = [3; 5; 9; 4; 7]",
    "val xs : int list = [3; 5; 9; 4; 7]",
    "drop 2 xs == List.tl (List.tl xs)",
    "- : bool = false",
    "List.tl (drop 2 xs) == List.tl (List.tl (List.tl xs))",
    "- : bool = true",
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


class CellsCopiedOrShared(NarratedScene):
    def construct(self):
        self.build()
        self.clip_take()
        self.clip_drop()
        self.clip_check()
        self.clip_glue()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── pieces ────────────────────────────────────────────────────────────────
    def build(self):
        o = self.orig = ConsChain([3, 5, 9, 4, 7])
        tk = self.take = ConsChain([3, 5], color=YELLOW)
        tk.shift(o.cells[0].get_center() + UP * TAKE_Y - tk.cells[0].get_center())
        self.new9 = ConsCell(9, color=YELLOW).move_to(o.cells[2].get_center() + UP * NEW9_Y)
        self.arrow9 = pointer_arrow(self.new9.tail_start(),
                                    o.cells[3].box.get_bottom() + LEFT * 0.2)
        self.cut_x = (o.cells[1].get_right()[0] + o.cells[2].get_left()[0]) / 2

        self.xs_ptr = code_pointer("xs", o.cells[0].box, DOWN)
        self.take_ptr = code_pointer("take 2 xs", tk.cells[0].box, UP)
        self.drop_ptr = code_pointer("drop 2 xs", self.new9.box, LEFT)
        self.count2 = T("new cells: 2", size=36, color=GOLD).move_to(
            [COL_X, TAKE_Y, 0], aligned_edge=LEFT)
        self.count1 = T("new cells: 1", size=36, color=GOLD).move_to(
            [COL_X, NEW9_Y, 0], aligned_edge=LEFT)
        self.shared_lab = T("shared", size=34, color=TEAL).move_to(
            [(o.cells[4].get_center()[0] + o.nil.get_center()[0]) / 2, -1.0, 0])

    # ── c1.cells.1: take copies ───────────────────────────────────────────────
    def clip_take(self):
        o, tk = self.orig, self.take
        with self.say("c1.cells.1") as c:
            parts = []
            for i, cell in enumerate(o.cells):
                parts += [cell, o.arrows[i]]
            parts.append(o.nil)
            self.play(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.15),
                      run_time=min(2.0, 0.85 * c.until("xs")))
            settle(self, o)

            c.wait_until("xs")
            self.play(FadeIn(self.xs_ptr, shift=0.3 * UP), run_time=1.0)

            c.wait_until("copy")
            self.play(FadeIn(self.take_ptr, shift=0.3 * DOWN),
                      run_time=min(1.0, c.until("one for the three")))
            c.wait_until("one for the three")
            self.play(TransformFromCopy(o.cells[0], tk.cells[0]),
                      run_time=min(1.5, c.until("and one for the five")))
            c.wait_until("and one for the five")
            self.play(TransformFromCopy(o.cells[1], tk.cells[1]), GrowArrow(tk.arrows[0]),
                      run_time=min(1.5, c.until("ending in a nil")))
            c.wait_until("ending in a nil")
            self.play(GrowArrow(tk.arrows[1]), FadeIn(tk.nil, shift=0.2 * LEFT),
                      run_time=min(1.2, c.until("why")))
            settle(self, tk)

            c.wait_until("why")
            self.play(FadeIn(self.count2, shift=0.3 * DOWN), run_time=1.0)

            c.wait_until("the five points on")
            self.play(FlashAround(VGroup(o.cells[1], o.arrows[1], o.cells[2]), time_width=1.5),
                      flash_along(o.cells[1], o.cells[2], YELLOW), run_time=1.6)
            c.wait_until("but take's answer")
            self.play(FlashAround(VGroup(tk.cells[1], tk.arrows[1], tk.nil), color=TEAL,
                                  time_width=1.5),
                      flash_along(tk.cells[1], tk.nil, TEAL), run_time=1.6)
            c.wait_until()

    # ── c1.cells.2: drop shares ───────────────────────────────────────────────
    def clip_drop(self):
        o, tk = self.orig, self.take
        with self.say("c1.cells.2") as c:
            self.play(*set_alpha([tk, self.take_ptr, self.count2], 0.4), run_time=1.0)

            c.wait_until("nine, four, seven")
            self.play(FlashAround(VGroup(*o.cells[2:], o.nil), time_width=1.5), run_time=2.0)

            c.wait_until("skip")
            mk = marker(YELLOW).move_to(above(o.cells[0].box))
            self.play(Succession(FadeIn(mk, shift=0.2 * DOWN, run_time=0.5),
                                 mk.animate(run_time=0.8).move_to(above(o.cells[1].box)),
                                 mk.animate(run_time=0.8).move_to(above(o.cells[2].box))),
                      run_time=min(2.1, c.until("rebuild") - 0.1))

            c.wait_until("rebuild")
            frag = self.frag = Code("else x::xs", size=40)
            frag.move_to([self.new9.get_center()[0], -3.05, 0])
            self.play(FadeOut(mk), FadeIn(frag, shift=0.3 * UP), run_time=1.0)

            c.wait_until("the pattern took")
            self.play(FlashAround(o.cells[2], time_width=1.5), run_time=1.2)
            c.wait_until("into ex and exes")
            lx = Mono("x", size=34, color=YELLOW).next_to(o.cells[2].box, UP, buff=0.22)
            lxs = Mono("xs", size=34, color=YELLOW).move_to(
                [(o.cells[2].tail_start()[0] + o.cells[3].entry()[0]) / 2, lx.get_y(), 0])
            lxs.align_to(lx, DOWN)
            self.play(LaggedStart(FadeIn(lx, shift=0.25 * DOWN), FadeIn(lxs, shift=0.25 * DOWN),
                                  lag_ratio=0.5), run_time=1.0)
            c.wait_until("and ex consed")
            box = token_box(frag.find("x::xs"), frag)
            self.play(FadeIn(box), run_time=0.8)
            c.wait_until("builds a brand new cell")
            self.play(TransformFromCopy(o.cells[2], self.new9), run_time=1.8)

            c.wait_until("shared")
            self.play(GrowArrow(self.arrow9), FadeOut(lx, lxs, box), run_time=1.3)
            c.wait_until("at the four")
            teal = []
            for cell in (o.cells[3], o.cells[4]):
                teal += [cell.box.animate.set_stroke(TEAL), cell.ptr.animate.set_stroke(TEAL)]
            teal += [o.arrows[3].animate.set_color(TEAL), o.arrows[4].animate.set_color(TEAL)]
            self.play(*teal, FadeIn(self.shared_lab, shift=0.3 * UP), run_time=1.3)

            c.wait_until("one")
            self.play(FadeIn(self.count1, shift=0.3 * DOWN),
                      FadeIn(self.drop_ptr, shift=0.3 * RIGHT),
                      FlashAround(self.new9, color=GOLD, time_width=1.5), run_time=1.3)
            c.wait_until()

    # ── c1.cells.3: check it with == ──────────────────────────────────────────
    def clip_check(self):
        o = self.orig
        ref = Code("\n".join(SESSION), size=CODE_SIZE, line_spacing=0.8)
        ref.move_to(ORIGIN).shift(UP * (3.45 - ref.get_top()[1]))
        L = self.session = []
        for i, src in enumerate(SESSION):
            ln = Code(src, size=CODE_SIZE)
            ln.shift(ref.line(i)[0].get_center() - ln.text[0].get_center())
            ln.shift(DOWN * 0.1 * (i // 2))           # a little air between input/reply pairs
            L.append(ln)
        for g in L[4].find("=="):
            g.set_color(YELLOW)

        movers = [o, self.new9, self.arrow9, self.xs_ptr, self.drop_ptr, self.count1,
                  self.shared_lab]
        gone = [self.take, self.take_ptr, self.count2, self.frag]
        with self.say("c1.cells.3") as c:
            self.play(*[time_span(FadeOut(m), 0, 0.6) for m in gone],
                      *[time_span(m.animate.shift(DOWN * SINK), 0.3, 1.3) for m in movers],
                      run_time=1.3)
            self.play(LaggedStart(FadeIn(L[0]), FadeIn(L[1]), lag_ratio=0.5), run_time=1.0)

            c.wait_until("two equals signs")
            self.play(FadeIn(L[2]), run_time=0.9)
            eq = L[2].find("==")
            self.play(*recolor(eq, YELLOW), FlashUnder(eq, color=YELLOW), run_time=1.0)

            c.wait_until("nine")
            box = token_box(L[2].find("drop 2 xs"), L[2])
            self.play(FadeIn(box), FlashAround(self.new9, time_width=1.5), run_time=1.2)
            c.wait_until("the tail of the tail")
            self.play(Transform(box, token_box(L[2].find("List.tl (List.tl xs)"), L[2])),
                      FlashAround(o.cells[2], time_width=1.5), run_time=1.2)

            c.wait_until("false")
            self.play(FadeOut(box), FadeIn(L[3]), run_time=0.8)
            c.wait_until("the nine is a new cell")
            self.play(FlashAround(o.cells[2], time_width=1.5),
                      FlashAround(self.new9, time_width=1.5), run_time=1.5)

            c.wait_until("four")
            self.play(FadeIn(L[4]), run_time=1.0)
            c.wait_until("gives true")
            self.play(FadeIn(L[5]), pulse(self.arrow9), flash_along(o.cells[2], o.cells[3], TEAL),
                      FlashAround(o.cells[3], color=TEAL, time_width=1.5),
                      run_time=max(0.6, min(1.2, c.remaining - 0.05)))
            c.wait_until()

    # ── c1.cells.4: safe, and the pieces glue back ────────────────────────────
    def clip_glue(self):
        o, tk, L = self.orig, self.take, self.session
        with self.say("c1.cells.4") as c:
            self.play(FlashAround(VGroup(o.cells[3], o.cells[4], o.nil), color=TEAL,
                                  time_width=1.5), run_time=1.6)

            c.wait_until("because lists never change")
            cap = T("lists never change once they’re built", size=32, color=DIM).move_to(UP * 3.0)
            self.play(FadeOut(L[0]), FadeOut(L[1]), time_span(FadeIn(cap, shift=0.3 * DOWN), 0.5, 1.3),
                      run_time=1.3)

            c.wait_until("nobody can change")
            self.play(FlashAround(o.cells[3], color=TEAL, time_width=1.5), pulse(self.arrow9),
                      flash_along(o.cells[2], o.cells[3], TEAL), run_time=1.5)

            # the two pieces alone: take's cells come back above, the original front goes
            c.wait_until("glue")
            set_op_now(tk, 1)
            tk.shift(DOWN * SINK)
            front = [o.cells[0], o.cells[1], o.cells[2], o.arrows[0], o.arrows[1], o.arrows[2],
                     self.xs_ptr, self.drop_ptr, self.count1, self.shared_lab, *L[2:]]
            self.play(LaggedStart(*[FadeOut(m) for m in front], lag_ratio=0.04),
                      time_span(FadeIn(tk, shift=0.3 * DOWN), 0.4, 1.0), run_time=1.0)

            # ...and slide together into one row, under scene 1's GOLD cut
            row = o.cells[2].get_center() + UP * ROW_UP              # where drop's 9 lands
            dy_take = row[1] - tk.cells[0].get_center()[1]
            c5 = tk.cells[1].copy().shift(UP * dy_take)
            n9 = self.new9.copy().move_to(row)
            c4 = o.cells[3].copy().shift(UP * ROW_UP)
            tail = [o.cells[3], o.cells[4], o.arrows[3], o.arrows[4], o.nil]
            cut = DashedLine(UP * 1.05, DOWN * 1.05, dash_length=0.12, color=GOLD,
                             stroke_width=5).move_to([self.cut_x, row[1], 0])
            glue = Code("take 2 xs @ drop 2 xs", size=40)
            reply = Mono("- : int list = [3; 5; 9; 4; 7]", size=40, color=GREEN)
            VGroup(glue, reply).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 2.1)
            self.play(*[m.animate.shift(UP * dy_take) for m in (tk.cells[0], tk.cells[1], tk.arrows[0])],
                      Transform(tk.arrows[1], link(c5, n9)), FadeOut(tk.nil),
                      self.new9.animate.move_to(row), Transform(self.arrow9, link(n9, c4)),
                      *[m.animate.shift(UP * ROW_UP) for m in tail],
                      time_span(FadeIn(cut, shift=0.4 * DOWN), 1.1, 1.8),
                      time_span(FadeIn(glue, shift=0.2 * UP), 1.0, 1.8), run_time=1.8)

            c.wait_until("you get back the whole list")
            self.play(FadeIn(reply, shift=0.2 * UP), run_time=0.8)
            c.wait_until()
        self.wait(1.5)                      # let the final reply sit before the fade
