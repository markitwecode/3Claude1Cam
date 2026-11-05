"""Chapter 5, scene 5: watching tmergesort [3; 5; 9; 4; 7] run. Clips c5.trace.1 – c5.trace.3.

Exported for scenes 6/7: split_tree(values=(3, 5, 9, 4, 7)) -> VGroup of the split tree
(rows .rows[key], edges .edges[key]; keys root L R LL LR RL RR RRL RRR), laid out as here
(ConsChain rows at scale ROW_S, full frame); scale/move it for a miniature.
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

VALS = (3, 5, 9, 4, 7)
ROW_S = 0.67
POS = {
    "root": (0.0, 2.5),
    "L": (-3.9, 1.2), "R": (2.9, 1.2),
    "LL": (-5.3, -0.1), "LR": (-2.9, -0.1), "RL": (0.3, -0.1), "RR": (4.1, -0.1),
    "RRL": (3.0, -1.4), "RRR": (5.2, -1.4),
}
PARENT = {"L": "root", "R": "root", "LL": "L", "LR": "L", "RL": "R", "RR": "R",
          "RRL": "RR", "RRR": "RR"}


def row(vals, key):
    return ConsChain(list(vals)).scale(ROW_S).move_to([*POS[key], 0])


def tree_edge(parent, child):
    dx = child.get_x() - parent.get_x()
    lim = parent.width * 0.3
    start = parent.get_bottom() + RIGHT * max(-lim, min(lim, dx)) + DOWN * 0.08
    end = child.get_top() + UP * 0.08
    return Line(start, end).set_stroke(DIM, 2)


def split_tree(values=VALS):
    """The split tree of a five-item list, as built in this scene (unsorted halves)."""
    v = list(values)
    parts = {"root": v, "L": v[:2], "R": v[2:], "LL": v[:1], "LR": v[1:2],
             "RL": v[2:3], "RR": v[3:], "RRL": v[3:4], "RRR": v[4:]}
    rows = {k: row(vals, k) for k, vals in parts.items()}
    edges = {k: tree_edge(rows[p], rows[k]) for k, p in PARENT.items()}
    g = VGroup(*rows.values(), *edges.values())
    g.rows, g.edges = rows, edges
    return g


class Trace(NarratedScene):
    # ---- helpers -------------------------------------------------------
    def split(self, parent, kids, edges, rt):
        anims, off = [], 0
        rest = []
        for kid in kids:
            for i, cell in enumerate(kid.cells):
                anims += fly(parent.cells[off + i], cell)
            off += len(kid.cells)
            rest += [*kid.arrows, kid.nil]
        anims += [Create(e) for e in edges]
        anims += during([FadeIn(m) for m in rest], 0.6, 1.0)
        self.play(*anims, run_time=rt)
        for kid in kids:
            settle(self, kid)

    def merge(self, parent, a, b, av, bv, key, budget, also_out=()):
        """Zip rows a, b into a new row at key; parent (old row there) fades first."""
        target = row(sorted(av + bv), key)
        picks, i, j = [], 0, 0
        while i < len(av) and j < len(bv):
            if av[i] <= bv[j]:
                picks.append(a.cells[i]); i += 1
            else:
                picks.append(b.cells[j]); j += 1
        left = a.cells[i:] if i < len(av) else b.cells[j:]
        n = len(picks) + 1
        fade_rt = min(0.8, 0.18 * budget)
        step = (budget - fade_rt) / n
        self.play(*disappear(parent, *also_out), run_time=fade_rt)
        k = 0
        for p in picks:
            self.play(*fly(p, target.cells[k]), run_time=0.8 * step)
            self.wait(0.2 * step)
            k += 1
        anims = []
        for cell in left:
            anims += fly(cell, target.cells[k]); k += 1
        anims += during([FadeIn(m) for m in [*target.arrows, target.nil]], 0.6, 1.0)
        anims += during(set_alpha([a, b], 0.4), 0.5, 1.0)
        self.play(*anims, run_time=0.85 * step)
        settle(self, target)
        return target

    # ---- scene ---------------------------------------------------------
    def construct(self):
        tree = split_tree()
        R_, E_ = tree.rows, tree.edges
        counts = []

        with self.say("c5.trace.1") as c:
            call = Code("tmergesort [3; 5; 9; 4; 7]", size=34).move_to([0, 3.35, 0])
            root = R_["root"]
            self.play(*appear(call, root, lag=0.4), run_time=min(1.6, c.until("split")))
            c.wait_until("split")
            cut_x = (root.cells[1].get_right()[0] + root.cells[2].get_left()[0]) / 2
            cut = DashedLine([cut_x, 2.95, 0], [cut_x, 1.95, 0], dash_length=0.1).set_stroke(GOLD, 4)
            self.play(GrowFromCenter(cut), run_time=0.8)
            self.wait(0.3)
            self.split(root, [R_["L"], R_["R"]], [E_["L"], E_["R"]], rt=min(2.0, c.until("leftfirst") - 0.5))
            c.wait_until("leftfirst")
            waits = T("waits", 30, DIM).next_to(R_["R"], DOWN, buff=0.35)
            self.play(*set_alpha([R_["R"], E_["R"]], 0.3), *appear(waits), run_time=1.0)
            c.wait_until("left")
            self.split(R_["L"], [R_["LL"], R_["LR"]], [E_["LL"], E_["LR"]], rt=1.6)
            c.wait_until("already sorted")
            s1 = T("sorted", 28, GREEN).next_to(R_["LL"], DOWN, buff=0.25)
            s2 = T("sorted", 28, GREEN).next_to(R_["LR"], DOWN, buff=0.25)
            self.play(*appear(s1, s2, lag=0.3), run_time=1.0)
            c.wait_until("m1")
            mL = self.merge(R_["L"], R_["LL"], R_["LR"], [3], [5], "L", budget=c.until() - 0.6)
            k1 = T("1", 44, GOLD).next_to(mL, LEFT, buff=0.35)
            self.play(*appear(k1), run_time=0.55)
            counts.append(k1)

        with self.say("c5.trace.2") as c:
            self.play(*set_alpha([R_["R"], E_["R"]], 1), *disappear(waits, s1, s2), run_time=1.0)
            c.wait_until("half of three")
            self.split(R_["R"], [R_["RL"], R_["RR"]], [E_["RL"], E_["RR"]], rt=1.8)
            c.wait_until("m2")
            self.split(R_["RR"], [R_["RRL"], R_["RRR"]], [E_["RRL"], E_["RRR"]], rt=1.4)
            self.wait(0.3)
            mRR = self.merge(R_["RR"], R_["RRL"], R_["RRR"], [4], [7], "RR",
                             budget=min(2.6, c.until("m3") - 0.7))
            k2 = T("1", 44, GOLD).next_to(mRR, RIGHT, buff=0.35)
            self.play(*appear(k2), run_time=0.5)
            counts.append(k2)
            c.wait_until("m3")
            mR = self.merge(R_["R"], R_["RL"], mRR, [9], [4, 7], "R",
                            budget=c.until("that's two comparisons") - 0.1)
            c.wait_until("that's two comparisons")
            k3 = T("2", 44, GOLD).next_to(mR, RIGHT, buff=0.35)
            self.play(*appear(k3), run_time=0.8)
            counts.append(k3)
            tag = T("an insert (scene 3)", 28, DIM).move_to([4.8, 1.85, 0])
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("sorted")
            self.play(FlashAround(mR, run_time=1.5, time_width=1.5))

        with self.say("c5.trace.3") as c:
            mroot = self.merge(root, mL, mR, [3, 5], [4, 7, 9], "root",
                               budget=min(5.0, c.until("in three comparisons") - 0.2), also_out=(cut, tag))
            c.wait_until("three comparisons")
            k4 = T("3", 44, GOLD).next_to(mroot, LEFT, buff=0.35)
            self.play(*appear(k4), run_time=0.8)
            counts.append(k4)
            c.wait_until("result")
            tick = check_mark(GREEN).scale(0.8).next_to(mroot, RIGHT, buff=0.35)
            reply = Code("- : int list = [3; 4; 5; 7; 9]", size=34).move_to(call)
            self.play(Create(tick), *swap(call, reply), run_time=1.3)
            c.wait_until("count")
            self.play(*[FlashAround(k, run_time=1.2, time_width=1.5) for k in counts], run_time=1.2)
            c.wait_until("one one two")
            lay = VGroup(*[T(ch, 44, GOLD if ch.isdigit() else FG) for ch in "1+1+2+3=7"])
            lay.arrange(RIGHT, buff=0.22).move_to([-2.8, -2.3, 0])
            lane = -2.95
            for n, k in enumerate(counts):
                dst = lay[2 * n].get_center()
                ex = 6.6 if k.get_x() > 0 else -6.6
                path = VMobject().set_points_as_corners([
                    k.get_center(), [ex, k.get_y(), 0], [ex, lane, 0], [dst[0], lane, 0], dst])
                extra = appear(lay[2 * n - 1], shift=None) if n else []
                self.play(MoveAlongPath(k, path), *extra, run_time=0.75, rate_func=smooth)
            eq_tail = [lay[7], lay[8]]
            self.play(*appear(*eq_tail, lag=0.3), run_time=0.8)
            seven = lay[8]
            c.wait_until("floor")
            f7 = T("7", 56, GOLD).move_to([3.6, -2.3, 0])
            flab = T("worst input, any comparison sort", 28, DIM).move_to([3.6, -2.95, 0])
            self.play(*appear(f7), run_time=1.0)
            self.play(*appear(flab), run_time=1.0)  # early: names the floor the voice is describing
            c.wait_until("exact")
            self.play(*recolor([seven, f7], GREEN), FlashAround(seven, run_time=1.5, time_width=1.5),
                      FlashAround(f7, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("others")
            t_ins = T("insertion sort: 6", 30, GOLD)
            t_qs = T("quicksort: 8", 30, GOLD)
            VGroup(t_ins, t_qs).arrange(RIGHT, buff=0.7).move_to([-2.8, -2.95, 0])
            c.wait_until(own_word=t_ins)
            self.play(*appear(t_ins), run_time=0.9)
            c.wait_until(own_word=t_qs)
            self.play(*appear(t_qs), run_time=0.9)
            c.wait_until("worst5")
            w5 = T("worst order of five: merge sort 8 · quicksort 10", 28, DIM).move_to([0, -3.5, 0])
            self.play(*appear(w5), run_time=1.0)
            c.wait_until()

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
