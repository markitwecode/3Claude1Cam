"""Chapter 4, scene 2: the average case: T(n) = 2T(n/2) + n, the recursion tree, n log2 n. Clips c4.avg.1 – c4.avg.5.

Exports `recursion_tree()` (for ch5 s6, ch6 and ch4's recap).
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


# ── exported: the recursion tree of perfect splits ──────────────────────────────────────
def recursion_tree(labels=("n", "n/2", "n/4", "1"),
                   sums=("n", r"2 \times n/2 = n", r"4 \times n/4 = n"),
                   levels_label=r"\log_2 n",
                   width=6.0, leaves=16, pitch=1.0, box_h=0.65, color=BLUE,
                   with_sums=False, with_bracket=False):
    """The recursion tree of quicksort with perfect splits: rows of 1, 2, 4 boxes, a ⋮, and a
    bottom row of `leaves` tiny boxes; every row is `width` wide. Rows centred on ORIGIN.

    labels: MathTex strings for the root, level 1, level 2 and the leaves (ch5 s6:
        ("10{,}000", "5{,}000", "2{,}500", "1")).
    sums: MathTex strings of the GOLD per-row sums of rows 0-2 (" = " splits off the last term).
    levels_label: MathTex of the bracket's label (above a T "levels").

    Returns a VGroup holding .rows and .dots (plus .sums / .bracket if with_sums / with_bracket).
    Parts (always built, positioned, whether in the group or not):
      .rows    list of 4 VGroups (root, level 1, level 2, leaves), each a VGroup of nodes;
               a node is VGroup(rect, label): node.rect, node.label
      .rects / .labels   list of 4 lists: each row's Rectangles / label MathTex
      .dots    the "⋮" between level 2 and the leaves
      .sums    VGroup of 3 GOLD MathTex at the right end of rows 0-2; sums[i][-1] is the final "n"
      .bracket VGroup(brace, label): GOLD Brace down the left side; .bracket.brace, .bracket.label
               (label = VGroup(MathTex levels_label, T "levels"))
    """
    gap = [0.0, 0.16, 0.14, 0.06]
    counts = [1, 2, 4, leaves]
    ys = [1.75 * pitch, 0.75 * pitch, -0.25 * pitch, -1.75 * pitch]
    sizes = [44, 40, 36, 28]
    tree = VGroup()
    tree.rows, tree.rects, tree.labels = [], [], []
    for r in range(4):
        k = counts[r]
        w = (width - gap[r] * (k - 1)) / k
        row = VGroup()
        rects, labs = [], []
        for j in range(k):
            x = -width / 2 + w / 2 + j * (w + gap[r])
            rect = Rectangle(width=w, height=box_h).set_stroke(color, 3).set_fill(color, 0.15)
            rect.move_to([x, ys[r], 0])
            lab = MathTex(labels[r], font_size=sizes[r]).move_to(rect)
            node = VGroup(rect, lab)
            node.rect, node.label = rect, lab
            row.add(node)
            rects.append(rect)
            labs.append(lab)
        tree.rows.append(row)
        tree.rects.append(rects)
        tree.labels.append(labs)
        tree.add(row)
    tree.dots = MathTex(r"\vdots", font_size=40).move_to([0, -1.0 * pitch, 0])
    tree.add(tree.dots)

    tree.sums = VGroup()
    for r, s in enumerate(sums):
        parts = s.split(" = ")
        tex = MathTex(*([parts[0], "=", parts[1]] if len(parts) == 2 else [s]), font_size=36, color=GOLD)
        tex.move_to([0, ys[r], 0]).align_to([width / 2 + 0.5, 0, 0], LEFT)
        tree.sums.add(tex)

    span = VGroup(*[tree.rows[0], tree.rows[3]])
    brace = Brace(span, direction=LEFT, buff=0.3, color=GOLD)
    blab = VGroup(MathTex(levels_label, font_size=40, color=GOLD), T("levels", size=30, color=GOLD))
    blab.arrange(DOWN, buff=0.15).next_to(brace, LEFT, buff=0.2)
    tree.bracket = VGroup(brace, blab)
    tree.bracket.brace, tree.bracket.label = brace, blab
    if with_sums:
        tree.add(tree.sums)
    if with_bracket:
        tree.add(tree.bracket)
    return tree


# ── layout ──────────────────────────────────────────────────────────────────────────────
BOX_W, BOX_H, SLOTS = 10.0, 0.7, 16
SLOT = BOX_W / SLOTS
TOP_Y = 1.6
TREE_SHIFT = np.array([0, -0.15, 0])      # the tree's rows: root at y 1.6, leaves at y -1.9


def call_tree_inset():
    """ch3's call tree, list-node form, small, for the {tree} beat."""
    try:
        from lib.paths import load_scene
        mod = load_scene("ch3_s6_trace")
        return mod.call_tree(form="lists", size=30, pitch=0.85, gap=0.95)
    except Exception:
        return None


class AverageCase(NarratedScene):
    def construct(self):
        self.split()
        self.recurrence()
        self.grow_tree()
        self.count_levels()
        self.ten_thousand()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c4.avg.1: n items, a pivot, n comparisons, two halves
    def split(self):
        x0 = -BOX_W / 2
        box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.15).move_to([0, TOP_Y, 0])
        piv = Square(SLOT - 0.08).set_stroke(width=0).set_fill(YELLOW, 0.9).move_to([x0 + SLOT / 2, TOP_Y, 0])
        piv_lbl = T("pivot", size=32, color=YELLOW).next_to(piv, UP, buff=0.25)
        items_lbl = T("n items", size=36, t2s={"n": ITALIC}).next_to(box, UP, buff=0.25).set_x(0.5)
        ticks = [Line(UP * 0.16, DOWN * 0.16).set_stroke(GOLD, 4).move_to([x0 + SLOT * (i + 0.5), TOP_Y - 0.62, 0])
                 for i in range(1, SLOTS)]
        cmp_lbl = T("about n comparisons", size=36, color=GOLD, t2s={"n": ITALIC}).move_to([0.3, TOP_Y - 1.2, 0])
        hy = TOP_Y - 2.4
        hw = (BOX_W - SLOT) / 2
        lbox = Rectangle(width=hw, height=BOX_H).set_stroke(BLUE, 3).set_fill(BLUE, 0.15).move_to([x0 + hw / 2, hy, 0])
        rbox = lbox.copy().move_to([-x0 - hw / 2, hy, 0])
        piv2 = piv.copy().move_to([0, hy, 0])
        lab_l = MathTex("n/2", font_size=48).move_to(lbox)
        lab_r = MathTex("n/2", font_size=48).move_to(rbox)

        with self.say("c4.avg.1") as c:
            self.play(FadeIn(box, shift=0.2 * DOWN), run_time=1.2)
            c.wait_until("pivots")
            self.play(FadeIn(piv, scale=0.6), run_time=1.0)
            c.wait_until(own_word=piv_lbl)
            self.play(*appear(piv_lbl), run_time=1.0)
            c.wait_until("compare")
            self.play(*appear(items_lbl), run_time=1.0)
            c.wait_until("compares every")
            self.play(LaggedStart(*[FadeIn(t, shift=0.12 * DOWN) for t in ticks], lag_ratio=0.35),
                      run_time=min(3.2, 0.9 * c.until("That's about")))
            c.wait_until("That's about")
            self.play(*appear(cmp_lbl), run_time=1.0)
            c.wait_until("halves")
            self.play(ReplacementTransform(box.copy(), lbox), ReplacementTransform(box.copy(), rbox),
                      TransformFromCopy(piv, piv2), run_time=min(2.0, 0.8 * c.until("so the two")))
            c.wait_until("so the two")
            self.play(*appear(lab_l, lab_r), run_time=1.0)
        self.top = [box, piv, piv_lbl, items_lbl, *ticks, cmp_lbl]
        self.halves = VGroup(lbox, rbox, piv2, lab_l, lab_r)
        self.lbox, self.rbox, self.piv2, self.lab_l, self.lab_r = lbox, rbox, piv2, lab_l, lab_r

    # c4.avg.2: T(n) = 2T(n/2) + n, T(1) = 1, Lecture 2's table
    def recurrence(self):
        hv = self.halves
        settle(self, hv)
        eq = MathTex("T(n)", "=", "2T(n/2)", "+", "n", font_size=48)
        base = MathTex("T(1) = 1", font_size=48)
        VGroup(eq, base).arrange(RIGHT, buff=0.8)
        base.align_to(eq, DOWN)
        VGroup(eq, base).to_edge(RIGHT, buff=0.55).set_y(3.2)
        br_h = Brace(eq[2], DOWN, buff=0.12, color=GOLD)
        br_s = Brace(eq[4], DOWN, buff=0.12, color=GOLD)
        lb_h = T("two halves", size=30, color=GOLD).next_to(br_h, DOWN, buff=0.12)
        lb_s = T("split", size=30, color=GOLD).next_to(br_s, DOWN, buff=0.12)

        TAB = 34
        lhs = [MathTex(tx, font_size=TAB) for tx in
               (r"T(n+1) = T(n) + 1", r"T(n+1) = T(n) + n", r"T(n) = T(n/2) + 1", r"T(n) = 2T(n/2) + n")]
        os_ = [MathTex(tx, font_size=TAB) for tx in ("O(n)", "O(n^2)", r"O(\log n)", r"O(n\log n)")]
        TX, TY0, TP = 0.7, 1.15, 0.72
        xc2 = TX + max(m.width for m in lhs) + 0.7
        for i in range(4):
            lhs[i].move_to([0, TY0 - TP * i, 0]).align_to([TX, 0, 0], LEFT)
            os_[i].move_to([0, TY0 - TP * i, 0]).align_to([xc2, 0, 0], LEFT)
        rows = [VGroup(lhs[i], os_[i]) for i in range(4)]
        tag = T("Lecture 2: listed, not derived", size=28, color=DIM)
        tag.move_to([0, TY0 - TP * 4 + 0.05, 0]).align_to([TX, 0, 0], LEFT)

        with self.say("c4.avg.2") as c:
            t = min(2.0, 0.85 * c.until("for the split"))
            self.play(*during([FadeOut(m) for m in self.top], 0, 0.45),
                      *during([hv.animate.scale(0.6).move_to([-0.6, -2.7, 0])], 0.2, 0.8),
                      *during([FadeIn(eq, shift=0.2 * DOWN)], 0.5, 1), run_time=t)
            c.wait_until(own_word=lb_s)
            self.play(GrowFromCenter(br_s), *appear(lb_s), run_time=1.0)
            c.wait_until(own_word=lb_h)
            self.play(GrowFromCenter(br_h), *appear(lb_h), run_time=1.0)
            c.wait_until("Tee of N equals")
            self.play(*flash([eq]), run_time=min(2.0, 0.6 * c.until("base")))
            c.wait_until("base")
            self.play(*appear(base), run_time=1.0)
            c.wait_until("table")
            self.play(*appear(*rows, shift=0.4 * LEFT, lag=0.15), run_time=1.6)
            self.play(*recolor([lhs[3], os_[3]], YELLOW), run_time=1.0)
            c.wait_until(own_word=tag)
            self.play(*appear(tag), run_time=1.0)
        self.eq, self.base = eq, base
        self.braces = [br_h, br_s, lb_h, lb_s]
        self.table = rows + [tag]

    # c4.avg.3: ch3's call tree; the recursion tree; the work on each row
    def grow_tree(self):
        tree = recursion_tree()
        tree.shift(TREE_SHIFT)
        tree.sums.shift(TREE_SHIFT)
        tree.bracket.shift(TREE_SHIFT)
        self.tree = tree
        hv = self.halves
        row1 = tree.rows[1]
        # halves scaled to sit on row 1 (pivot in the gap)
        tgt = VGroup(row1[0].rect, row1[1].rect)
        k = tgt.width / VGroup(self.lbox, self.rbox).width

        inset = call_tree_inset()
        if inset is None:
            inset = VGroup(T("call tree", size=30, color=DIM))
        if inset.width > 3.15:
            inset.scale_to_fit_width(3.15)
        if inset.height > 2.3:
            inset.scale_to_fit_height(2.3)
        inset.move_to([-4.95, 1.75, 0])
        inset_tag = T("Part 3:\nour five items", size=28, color=DIM, line_spacing=0.9).next_to(inset, DOWN, buff=0.3)
        inset_tag.set_x(inset.get_x())

        with self.say("c4.avg.3") as c:
            self.play(*appear(inset, inset_tag, lag=0.4), run_time=1.4)  # early: the inset's tag names it as it's shown
            c.wait_until("Now draw")
            t = min(2.0, 0.8 * c.until("root"))
            self.play(*during([FadeOut(m) for m in self.table + self.braces], 0, 0.45),
                      *during([hv.animate.scale(k).move_to([0, row1.get_y(), 0])], 0.45, 1), run_time=t)
            c.wait_until("root")
            root = tree.rows[0][0]
            self.play(ReplacementTransform(VGroup(self.lbox.copy(), self.piv2.copy(), self.rbox.copy()), root.rect),
                      run_time=1.5)
            self.play(*appear(root.label), run_time=0.8)
            c.wait_until("level1")
            self.play(ReplacementTransform(self.lbox, row1[0].rect), ReplacementTransform(self.rbox, row1[1].rect),
                      FadeOut(self.piv2, scale=0.5),
                      self.lab_l.animate.move_to(row1[0].label), self.lab_r.animate.move_to(row1[1].label),
                      run_time=1.6)
            self.remove(self.lab_l, self.lab_r)
            self.add(row1[0].label, row1[1].label)
            c.wait_until("level2")
            self.play(*during([ReplacementTransform(tree.rects[1][j // 2].copy(), tree.rects[2][j])
                               for j in range(4)], 0, 0.65),
                      *during([FadeIn(lab) for lab in tree.labels[2]], 0.55, 1), run_time=1.8)
            c.wait_until("so on")
            self.play(*during([ReplacementTransform(tree.rects[2][j // 4].copy(), tree.rects[3][j])
                               for j in range(16)], 0, 0.6),
                      *during([FadeIn(tree.dots, shift=0.15 * DOWN)], 0.2, 0.7),
                      *during([FadeIn(lab) for lab in tree.labels[3]], 0.55, 1), run_time=1.8)
            settle(self, tree)
            c.wait_until("work")
            self.play(*disappear(inset, inset_tag), run_time=1.0)
            for r, cue in enumerate(("row0", "row1", "row2")):
                c.wait_until(cue)
                self.play(*appear(tree.sums[r], shift=0.25 * LEFT), run_time=1.0)
            c.wait_until("every")
            self.play(*flash([s[-1] for s in tree.sums], color=GOLD, time_width=1.5),
                      *recolor([s[-1] for s in tree.sums], YELLOW), run_time=2.0)
            self.play(*recolor([s[-1] for s in tree.sums], GOLD), run_time=0.8)

    # c4.avg.4: log2 n levels, n log2 n
    def count_levels(self):
        tree = self.tree
        brace, blab = tree.bracket.brace, tree.bracket.label
        q = MathTex("?", font_size=56, color=GOLD).move_to(blab)
        total = MathTex(r"n \times \log_2 n", font_size=48)
        total.move_to([0, -3.0, 0])
        tbox = SurroundingRectangle(total, color=YELLOW, buff=0.18)
        big_o = MathTex(r"O(n\log n)", font_size=48, color=GREEN).next_to(tbox, RIGHT, buff=0.7)
        g = VGroup(total, tbox, big_o)
        dx = -g.get_center()[0]
        g.shift(RIGHT * dx)

        with self.say("c4.avg.4") as c:
            self.play(GrowFromCenter(brace), *appear(q), run_time=1.2)
            c.wait_until("halve")
            row_labs = [tree.labels[0], tree.labels[1], tree.labels[2], [tree.dots], tree.labels[3]]
            t = min(3.2, 0.9 * c.until("halvings"))
            self.play(*[time_span(lab.animate.set_color(YELLOW), 0.2 * t * i, 0.2 * t * i + 0.35 * t)
                        for i, labs in enumerate(row_labs) for lab in labs], run_time=t)
            c.wait_until("halvings")
            self.play(*swap(q, blab), run_time=1.2)
            self.play(*[lab.animate.set_color(FG) for labs in row_labs for lab in labs], run_time=0.8)
            c.wait_until("total")
            self.play(*appear(total), run_time=1.0)
            self.play(FadeIn(tbox), run_time=0.6)
            c.wait_until("in all")
            self.play(*flash([total], color=YELLOW, time_width=1.5), run_time=1.5)
            c.wait_until("Big O")
            self.play(*appear(big_o, shift=0.25 * LEFT), run_time=1.0)
        self.total = [total, tbox, big_o]

    # c4.avg.5: 10,000 items: 133,000 predicted, 158,058 counted; 235 times faster
    def ten_thousand(self):
        tree = self.tree
        full = VGroup(*tree.rows, tree.dots)
        settle(self, full)
        sc = 0.8
        small_c = np.array([-6.55 + sc * full.width / 2, 0.75, 0])
        RX = 2.75
        logl = MathTex(r"\log_2 10{,}000 \approx 13.3", font_size=48, color=GOLD).move_to([RX, 2.75, 0])
        cap1 = T("perfect splits: 14 levels,\nthe last only partly filled", size=28, color=DIM,
                 line_spacing=0.9).next_to(logl, DOWN, buff=0.3)
        prod = MathTex(r"10{,}000 \times 13.3 \approx 133{,}000", font_size=44, color=GOLD).move_to([RX, 0.5, 0])
        meas = MathTex(r"158{,}058", font_size=48, color=GOLD).move_to([RX, -0.6, 0])
        cap2 = T("counted by us: a tallying ≤", size=28, color=DIM).next_to(meas, DOWN, buff=0.25)
        aho = T("proof: Aho, p. 94", size=30, color=DIM).move_to([RX, -1.95, 0])

        with self.say("c4.avg.5", gap=3.8) as c:
            t = min(2.0, 0.6 * c.until("Thirteen halvings"))
            self.play(*during([FadeOut(m) for m in [self.eq, self.base, tree.sums, tree.bracket]], 0, 0.45),
                      *during([full.animate.scale(sc).move_to(small_c)], 0.2, 0.8),
                      *during([FadeIn(logl, shift=0.2 * DOWN)], 0.55, 1), run_time=t)
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("Ten thousand times")
            self.play(*appear(prod), run_time=1.2)
            c.wait_until("measured")
            self.play(*appear(meas), run_time=1.0)
            self.play(*appear(cap2), run_time=0.8)
            c.wait_until("imperfect")
            # uneven splits: one part wider than the other, by a different amount in each
            cap3 = T("random pivots:\nseldom exact halves", size=28, color=DIM, line_spacing=0.9)
            cap3.next_to(full, DOWN, buff=0.35).set_x(VGroup(*tree.rows).get_x())
            anims = []
            fr = {1: [0.36], 2: [0.6, 0.3]}
            l1 = tree.rects[1]
            x_l, x_r = l1[0].get_left()[0], l1[1].get_right()[0]
            g1 = l1[1].get_left()[0] - l1[0].get_right()[0]
            wid = x_r - x_l - g1
            w1 = [wid * fr[1][0], wid * (1 - fr[1][0])]
            edges1 = [(x_l, x_l + w1[0]), (x_l + w1[0] + g1, x_r)]
            l2 = tree.rects[2]
            g2 = l2[1].get_left()[0] - l2[0].get_right()[0]
            edges2 = []
            for p, (a, b) in enumerate(edges1):
                w = b - a - g2
                m = a + w * fr[2][p]
                edges2 += [(a, m), (m + g2, b)]
            for r, edges in ((1, edges1), (2, edges2)):
                for j, (a, b) in enumerate(edges):
                    rect = tree.rects[r][j]
                    new = rect.copy().stretch_to_fit_width(b - a).move_to([(a + b) / 2, rect.get_y(), 0])
                    anims.append(Transform(rect, new))
                    anims.append(tree.labels[r][j].animate.move_to(new))
            self.play(*anims, run_time=1.8)
            self.play(*appear(cap3), run_time=1.0)
            c.wait_until("aho")
            self.play(*appear(aho), run_time=1.0)  # early: the notes' reference, shown as their claim is read

            c.wait_until("ratio")
            slow = T("174 s", size=60, color=RED).move_to([-3.0, 0.7, 0])
            fast = T("0.74 s", size=60, color=GREEN).move_to([3.0, 0.7, 0])
            slow_l = T("insertion sort", size=32, color=DIM).next_to(slow, DOWN, buff=0.3)
            fast_l = T("quicksort", size=32, color=DIM).next_to(fast, DOWN, buff=0.3)
            ratio = T("≈ 235 × faster", size=52, color=GOLD).move_to([0, -1.7, 0])
            sweep_clear(self, *during(appear(slow, slow_l, fast, fast_l, lag=0.15), 0.6, 1), run_time=1.8)  # early: the two times are read as a pair
            c.wait_until("times faster")
            self.play(*appear(ratio), run_time=1.0)
