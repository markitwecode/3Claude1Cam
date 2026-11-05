"""Chapter 3, scene 2: Divide and conquer. Clips c3.idea.1 – c3.idea.4.

Plan
- opens on ch3_s1_hook.handover_shot(): 5 → 3 → 9 → 4 → 7 → [] at (0, 2.6), scale 0.8.
- c3.idea.1: step column on the left ("1 choose" … lit YELLOW in turn, then DIM). {choose} the 5
  drops out YELLOW to (0, -1.3), "pivot a"; {divide} two dashed groups "≤ a" / "> a"; {tests} 3 9 4 7
  drop one by one with "≤ 5? yes/no"; {four} GOLD "comparisons: 4".
- c3.idea.2: {conquer} groups outline YELLOW, `quick` tags; {small} 3 → 4 stays, 9/7 swap, "+1"s;
  {combine} left part, pivot, right part slide back to the top row; {done} joined + GREEN tick;
  {six} counter edits to 6.
- c3.idea.3: {why} question; {because} YELLOW dashed line through the 5, braces "everything ≤ 5" /
  "everything > 5"; {nowork} counter flash + "combine: 0 comparisons".
- c3.idea.4: {dc} board clears to the sorted chain; steps gather into a row under a brace,
  "divide and conquer"; steps light as named; {merge} DIM "merge sort: Part 5".
split_icon(): module-level icon for the recap (s7).
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S = 0.8                     # cell scale (as the handover chain)
TOP_Y = 2.6                 # the chain row
GRP_Y = -1.3                # the two groups' row (and the pivot)
GRP_X = 2.5                 # group centres at ±GRP_X
PITCH = 2.3 * S             # chain pitch at scale S
STEP_X = -6.5               # left edge of the step column


def split_icon():
    """Recap icon: 5 → 3 → 9 → 4 → 7 → [] split round the YELLOW pivot into "≤ 5" and "> 5"."""
    top = ConsChain([5, 3, 9, 4, 7]).scale(0.5)
    L = ConsChain([3, 4], with_nil=False).scale(0.5)
    R = ConsChain([9, 7], with_nil=False).scale(0.5)
    piv = ConsCell(5, color=YELLOW).scale(0.5)
    piv.label.set_color(YELLOW)
    row = VGroup(L, piv, R).arrange(RIGHT, buff=0.6).next_to(top, DOWN, buff=0.9)
    le = T("≤ 5", 30, t2c={"5": YELLOW}).next_to(L, DOWN, buff=0.2)
    gt = T("> 5", 30, t2c={"5": YELLOW}).next_to(R, DOWN, buff=0.2)
    al = Arrow(top.get_bottom() + 0.6 * LEFT, L.get_top(), buff=0.12, stroke_width=3, color=DIM)
    ar = Arrow(top.get_bottom() + 0.6 * RIGHT, R.get_top(), buff=0.12, stroke_width=3, color=DIM)
    return VGroup(top, row, le, gt, al, ar).move_to(ORIGIN)


def _slot(side, k):
    """Centre of slot k (0, 1) in the left (-1) or right (+1) group."""
    return np.array([side * GRP_X + (k - 0.5) * PITCH, GRP_Y, 0])


class DivideAndConquer(NarratedScene):
    def construct(self):
        shot = load_scene("ch3_s1_hook").handover_shot()
        self.add(shot)
        self.cells = list(shot.cells)
        self.arrows = list(shot.arrows)
        self.nil = shot.nil
        self.steps = [T(f"{i + 1} {w}", 32, YELLOW) for i, w in
                      enumerate(("choose", "divide", "conquer", "combine"))]
        for i, s in enumerate(self.steps):
            s.move_to([0, 0.6 - 0.8 * i, 0]).align_to([STEP_X, 0, 0], LEFT)
        self.clip_divide()
        self.clip_conquer()
        self.clip_why()
        self.clip_dc()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def light(self, i, c, rt=1.0):
        """Step i appears YELLOW; the previous one goes DIM."""
        anims = appear(self.steps[i], shift=0.2 * RIGHT)
        if i > 0:
            anims.append(self.steps[i - 1].animate.set_color(DIM))
        self.play(*anims, run_time=rt)

    # ── c3.idea.1 ────────────────────────────────────────────────────────────────
    def clip_divide(self):
        cells, arrows = self.cells, self.arrows
        with self.say("c3.idea.1") as c:
            c.wait_until("choose")
            self.light(0, c)
            c.wait_until("pivot")
            piv = ConsCell(5, color=YELLOW).scale(S).move_to([0, GRP_Y, 0])
            piv.label.set_color(YELLOW)
            self.play(Transform(cells[0], piv), FadeOut(arrows[0]), run_time=1.6)
            self.pivot = cells[0]
            self.plab = T("pivot a", 34, t2c={"a": YELLOW}).next_to(piv, UP, buff=0.35)
            c.wait_until("call it")
            self.play(*appear(self.plab), run_time=1.0)
            c.wait_until("first item")
            self.play(FlashAround(self.pivot, color=YELLOW, time_width=1.5, run_time=1.5))

            c.wait_until("divide")
            boxes = [DashedVMobject(RoundedRectangle(corner_radius=0.2, width=3.44, height=1.4),
                                    num_dashes=48).set_stroke(DIM, 2).move_to([side * GRP_X, GRP_Y, 0])
                     for side in (-1, 1)]
            self.boxes = boxes
            self.play(*[FadeOut(a) for a in arrows[1:]], FadeOut(self.nil),
                      self.steps[0].animate.set_color(DIM),
                      *during(appear(self.steps[1], shift=0.2 * RIGHT), 0, 0.6),
                      *during([FadeIn(b) for b in boxes], 0.4, 1.0), run_time=1.5)
            self.le = T("≤ a", 36, t2c={"a": YELLOW}).next_to(boxes[0], UP, buff=0.2)
            self.gt = T("> a", 36, t2c={"a": YELLOW}).next_to(boxes[1], UP, buff=0.2)
            c.wait_until("at most")
            self.play(*appear(self.le), run_time=1.0)
            c.wait_until("bigger")
            self.play(*appear(self.gt), run_time=1.0)

            c.wait_until("tests")
            filled = {-1: 0, 1: 0}
            self.slot_cells = {-1: [], 1: []}
            tags = []
            for n, idx in enumerate((1, 2, 3, 4)):
                cell = cells[idx]
                yes = idx in (1, 3)                     # 3 and 4 are ≤ 5
                side = -1 if yes else 1
                tag = VGroup(T("≤ 5?", 30, GOLD),
                             T("yes" if yes else "no", 30, GREEN if yes else RED))
                tag.arrange(RIGHT, buff=0.15).next_to(cell, UP, buff=0.15)
                dst = _slot(side, filled[side])
                filled[side] += 1
                self.slot_cells[side].append(cell)
                tags.append(tag)
                rt = (1.4, 1.0, 0.85, 0.85)[n]
                self.play(*during(appear(tag, shift=None), 0, 0.35),
                          *during([cell.animate.move_to(dst)], 0.35, 1.0), run_time=rt)
                if n < 3:
                    self.wait(0.15)
            self.counter = T("comparisons: 4", 34, GOLD).move_to([0, -3.3, 0])
            c.wait_until(own_word=self.counter)
            self.play(*during(disappear(*tags), 0, 0.5),
                      *during(appear(self.counter), 0.3, 1.0), run_time=1.2)

    # ── c3.idea.2 ────────────────────────────────────────────────────────────────
    def clip_conquer(self):
        L, R = self.slot_cells[-1], self.slot_cells[1]
        with self.say("c3.idea.2") as c:
            self.play(self.steps[1].animate.set_color(DIM),
                      *appear(self.steps[2], shift=0.2 * RIGHT),
                      *[restyle(b, outline=YELLOW) for b in self.boxes], run_time=1.2)
            quicks = [Mono("quick", 30, YELLOW).next_to(b, DOWN, buff=0.2) for b in self.boxes]
            c.wait_until("quicksort itself")
            self.play(*appear(*quicks, lag=0.3), run_time=1.2)

            c.wait_until("small")
            la = link(L[0], L[1])
            p_l = T("+1", 34, GOLD).next_to(quicks[0], RIGHT, buff=0.25)
            self.play(GrowArrow(la), *during(appear(p_l), 0.3, 1.0), run_time=1.2)
            # the right part swaps: 9 bows over the top, 7 dips under
            c.wait_until("seven nine")
            self.play(R[0].animate(path_arc=-0.6 * PI).move_to(_slot(1, 1)),
                      R[1].animate(path_arc=-0.6 * PI).move_to(_slot(1, 0)), run_time=1.5)
            R = [R[1], R[0]]
            ra = link(R[0], R[1])
            p_r = T("+1", 34, GOLD).next_to(quicks[1], RIGHT, buff=0.25)
            self.play(GrowArrow(ra), *during(appear(p_r), 0.3, 1.0), run_time=1.0)

            c.wait_until("combine")
            self.play(self.steps[2].animate.set_color(DIM),
                      *appear(self.steps[3], shift=0.2 * RIGHT),
                      *disappear(*self.boxes, *quicks, self.le, self.gt, self.plab), run_time=1.2)
            # the two +1s wait beside the counter
            self.play(p_l.animate.next_to(self.counter, LEFT, buff=0.4),
                      p_r.animate.next_to(self.counter, RIGHT, buff=0.4), run_time=1.0)
            ref = ConsChain([3, 4, 5, 7, 9]).scale(S).move_to([0, TOP_Y, 0])
            home = [cl.get_center() for cl in ref.cells]
            c.wait_until("smaller part")
            d = home[0] - L[0].get_center()
            self.play(L[0].animate.shift(d), L[1].animate.shift(d), la.animate.shift(d), run_time=1.3)
            c.wait_until("then the pivot")
            self.play(self.pivot.animate.move_to(home[2]), run_time=1.1)
            c.wait_until("larger part")
            d = home[3] - R[0].get_center()
            self.play(R[0].animate.shift(d), R[1].animate.shift(d), ra.animate.shift(d), run_time=1.3)

            c.wait_until("done")
            new = [ref.arrows[1], ref.arrows[2], ref.arrows[4], ref.nil]
            self.tick = check_mark().move_to([5.5, TOP_Y, 0])
            self.play(*[GrowArrow(a) for a in new[:3]], FadeIn(new[3]), run_time=1.0)
            self.play(*appear(self.tick, shift=None), run_time=0.8)
            self.sorted = VGroup(L[0], L[1], self.pivot, R[0], R[1], la, ref.arrows[1],
                                 ref.arrows[2], ra, ref.arrows[4], ref.nil)
            settle(self, self.sorted)
            self.sorted_cells = [L[0], L[1], self.pivot, R[0], R[1]]

            c.wait_until("six")
            c6 = T("comparisons: 6", 34, GOLD).move_to(self.counter)
            self.play(*during(disappear(p_l, p_r), 0, 0.4),
                      *during(edit(self.counter, c6), 0.35, 1.0), run_time=1.6)
            self.counter = c6

    # ── c3.idea.3 ────────────────────────────────────────────────────────────────
    def clip_why(self):
        sc = self.sorted_cells
        with self.say("c3.idea.3") as c:
            q = T("But why is the result sorted?", 44).move_to([0.6, 0.2, 0])
            self.play(*appear(q), run_time=1.0)
            c.wait_until("because")
            x = self.pivot.box.get_x()
            line = DashedLine([x, 3.45, 0], [x, 0.6, 0], dash_length=0.12).set_stroke(YELLOW, 3)
            line.set_z_index(-2)
            self.play(GrowFromCenter(line), run_time=1.0)
            bl = span_brace(sc[0].get_corner(DL), sc[1].get_corner(DR))
            br = span_brace(sc[3].get_corner(DL), sc[4].get_corner(DR))
            el = T("everything ≤ 5", 34, t2c={"5": YELLOW}).next_to(bl, DOWN, buff=0.15)
            er = T("everything > 5", 34, t2c={"5": YELLOW}).next_to(br, DOWN, buff=0.15)
            self.play(GrowFromCenter(bl), *during(appear(el), 0.3, 1.0), run_time=1.2)
            c.wait_until("everything", nth=1)
            self.play(GrowFromCenter(br), *during(appear(er), 0.3, 1.0), run_time=1.2)
            c.wait_until("nothing needs")
            self.play(VShowPassingFlash(line.copy().set_stroke(YELLOW, 7), time_width=0.6),
                      *disappear(q), run_time=1.5)
            c.wait_until("nowork")
            zero = T("combine: 0 comparisons", 32, GOLD).next_to(self.counter, UP, buff=0.4)
            self.play(FlashAround(self.counter, color=GOLD, time_width=1.5),
                      *during(appear(zero), 0.3, 1.0), run_time=1.5)
            c.wait_until("all the comparing")
            self.play(self.steps[1].animate.set_color(YELLOW), run_time=1.0)
            self.play(FlashAround(self.steps[1], color=YELLOW, time_width=1.5), run_time=1.4)

    # ── c3.idea.4 ────────────────────────────────────────────────────────────────
    def clip_dc(self):
        steps = self.steps
        row = VGroup(*[s.copy().scale(36 / 32).set_color(FG) for s in steps])
        row.arrange(RIGHT, buff=0.7).move_to([0, 0.3, 0])
        for s, t in zip(steps, row):
            s.target = t
        brace = Brace(row, DOWN, buff=0.25, color=DIM)
        dc = T("divide and conquer", 48, YELLOW).next_to(brace, DOWN, buff=0.3)
        with self.say("c3.idea.4") as c:
            sweep_clear(self, *[MoveToTarget(s) for s in steps],
                        keep=[self.sorted, self.tick, *steps], run_time=1.6)
            self.play(GrowFromCenter(brace), *during(appear(dc), 0.3, 1.0), run_time=1.2)
            for i, cue in ((1, "split"), (2, "solve those"), (3, "combine their")):
                c.wait_until(cue)
                self.play(steps[i].animate.set_color(YELLOW), run_time=0.8)
            c.wait_until("merge")
            merge = T("merge sort: Part 5", 30, DIM).next_to(dc, DOWN, buff=0.4)
            self.play(*appear(merge), run_time=1.0)
        self.wait(0.8)
