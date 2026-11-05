"""Chapter 4, scene 3: the worst case. Clips c4.worst.1 – c4.worst.4.

Plan: sorted chain across the top, its call tree (ch3's `call_tree`) grows below it, one call per
mark, every node with one RED empty side; it fades to the circle zigzag 3, 9, 4, 7, 5 (exported as
`worst_tree()`), 4 + 3 + 2 + 1 = 10 beside ch3's 8. Clip 3: the zigzag shrinks left, the recurrence,
Lecture 2's table, the rs counts. Clip 4: the almost-sorted row, ch2 s6's scale with quicksort's RED
tick, the shuffle into the running chain (`shuffled_chain()`, GREEN 158,058).
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from scenes.ch2_s6_bestworst import range_scale  # noqa: E402

CH_S = 0.7                 # chain scale in clip 4 (and the recap's builders)
TAB = 36                   # table font size
RX = 2.3                   # centre of the right-hand column in clip 3


def left_at(m, x, y):
    m.shift([x - m.get_left()[0], y - m.get_center()[1], 0])
    return m


def sorted_chain(scale=CH_S):
    """The sorted chain 3 -> 4 -> 5 -> 7 -> 9 -> [] with GREEN "sorted" on its left; chain centred at ORIGIN.
    Attributes .chain .label."""
    g = VGroup()
    g.chain = ConsChain([3, 4, 5, 7, 9]).scale(scale)
    for cell in g.chain.cells:
        cell.set_z_index(1)
    g.label = T("sorted", 40, GREEN).next_to(g.chain, LEFT, buff=0.4)
    g.add(g.label, g.chain)
    return g


def shuffled_chain(scale=CH_S):
    """The shuffled running chain 3 -> 5 -> 9 -> 4 -> 7 -> [] (chain centred at ORIGIN), "shuffled" on its
    left, GOLD "8 comparisons" under it and GREEN "random order, like rs: 158,058" under that.
    Attributes .chain .label .count .note."""
    g = VGroup()
    g.chain = ConsChain([3, 5, 9, 4, 7]).scale(scale)
    for cell in g.chain.cells:
        cell.set_z_index(1)
    g.label = T("shuffled", 40, FG).next_to(g.chain, LEFT, buff=0.4)
    g.count = VGroup(T("8", 60, GOLD), T("comparisons", 32, DIM)).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
    g.count.next_to(g.chain, DOWN, buff=0.55)
    g.note = T("random order, like rs: 158,058", 38, GREEN).next_to(g.count, DOWN, buff=0.4)
    g.add(g.label, g.chain, g.count, g.note)
    return g


SORTED = [3, 4, 5, 7, 9]


def worst_tree(form="lists", **kw):
    """The call tree of quick on the sorted list [3; 4; 5; 7; 9]: ch3's `call_tree` with every empty
    side RED and the leaf [5] not expanded (max_depth=4).
    form="lists": list nodes, pivots YELLOW, GOLD badges 4, 3, 2, 1, 0, empty calls RED "[]".
    form="circles": the zigzag of pivot circles 3, 9, 4, 7, 5 (ch3's BLUE rings, YELLOW digits), each with a RED stub toward its
    empty side. Other kwargs go to call_tree (size, pitch, gap, radius, badges, ...); place it with
    `.place(scale, point)` (point = the root's centre)."""
    kw.setdefault("max_depth", 4)
    tree = _ch3().call_tree(SORTED, form=form, **kw)
    if form == "circles":
        for nd in tree.nodes:          # YELLOW pivot digits; longer, bolder RED stubs toward the empty side
            nd.pivot_glyph.set_color(YELLOW)
            for side, st in nd.stubs.items():
                d = getattr(nd, side).point - nd.point
                d = d / np.linalg.norm(d)
                st.put_start_and_end_on(st.get_start(), st.get_start() + 0.75 * d * tree.root.body.width / 0.9)
                st.set_stroke(RED, 5)
    else:
        for nd in tree.nodes:
            if nd.is_empty:
                nd.body.set_color(RED)
    return tree


def _ch3():
    from lib.paths import load_scene
    return load_scene("ch3_s6_trace")


LT_ROOT = np.array([0.5, 2.0, 0])     # list tree root
CT_ROOT = np.array([-2.8, 2.0, 0])     # circle tree root
CHAIN_Y = 3.3


class TheWorstCase(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ---- clip 1 / 2: the tree of a sorted list ---------------------------------------------
    def grow(self, node, extra=(), run_time=1.2):
        """One child node appears under its parent (edge first, then the node)."""
        self.play(Create(node.edge), *during(appear(node.body), 0.3, 1.0), *extra, run_time=run_time)

    def clip1(self):
        lt = worst_tree("lists", gap=1.25).place(1.0, LT_ROOT)
        self.lt = lt
        n = {tuple(nd.values): nd for nd in lt.nodes}
        self.n = n
        sc = sorted_chain(scale=0.7)
        sc.shift([-sc.chain.get_center()[0] + 0.5, CHAIN_Y - sc.chain.get_center()[1], 0])
        self.sc = sc
        root = n[(3, 4, 5, 7, 9)]
        e0, r1 = root.left, root.right
        with self.say("c4.worst.1") as c:
            self.play(*appear(sc.chain), run_time=1.0)
            c.wait_until(own_word=sc.label)
            self.play(*appear(sc.label), run_time=0.8)
            c.wait_until("three, four")
            self.play(LaggedStart(*[FlashAround(cell, time_width=1.5) for cell in sc.chain.cells],
                                  lag_ratio=0.25), run_time=min(3.0, 0.8 * c.until("p1")))
            # {p1}: the root; pivot 3 the smallest
            c.wait_until("p1")
            self.play(*appear(root.body), run_time=1.0)
            c.wait_until("the smallest item")
            self.play(FlashAround(root.pivot_glyph, run_time=1.2, time_width=1.5))
            c.wait_until("goes right")
            self.grow(r1, run_time=1.5)
            c.wait_until("left part is empty")
            self.grow(e0, run_time=1.0)
            self.play(FlashAround(e0.body, color=RED, run_time=1.2, time_width=1.5))
            c.wait_until("four comparisons")
            self.play(GrowFromCenter(root.badge[0]), *appear(root.badge.num, shift=None), run_time=1.0)
            # {flip}: the right part comes out reversed
            c.wait_until("comes out as")
            ul = underline(r1.body, YELLOW, buff=0.1)
            tag = VGroup(T("part builds its parts", 30, DIM), T("backwards (Part 3)", 30, DIM)).arrange(
                DOWN, buff=0.15, aligned_edge=LEFT)
            tag.move_to([-4.5, -1.15, 0])
            self.play(GrowFromCenter(ul), *during(appear(tag), 0.3, 1.0), run_time=1.5)
            self.ul, self.tag = ul, tag

    def clip2(self):
        n = self.n
        r1, l2, e2 = n[(9, 7, 5, 4)], n[(4, 5, 7)], [nd for nd in self.lt.nodes if nd.is_empty]
        with self.say("c4.worst.2") as c:
            # {p2}: pivot 9, everything goes left
            self.play(FlashAround(r1.pivot_glyph, run_time=1.2, time_width=1.5))
            c.wait_until("goes left")
            self.grow(l2, [FadeOut(self.ul)], run_time=1.2)
            self.grow(r1.right, run_time=0.9)
            c.wait_until("Three comparisons")
            self.play(GrowFromCenter(r1.badge[0]), *appear(r1.badge.num, shift=None), run_time=1.0)
            # {p3}: 4 the smallest, then 7 the largest
            c.wait_until("p3")
            l3 = l2.right
            self.play(Create(l2.left.edge), Create(l3.edge),
                      *during(appear(l2.left.body, l3.body), 0.3, 1.0),
                      GrowFromCenter(l2.badge[0]), *appear(l2.badge.num, shift=None), run_time=1.2)
            c.wait_until("then seven")
            l4 = l3.left
            self.play(Create(l4.edge), Create(l3.right.edge),
                      *during(appear(l4.body, l3.right.body), 0.3, 1.0),
                      GrowFromCenter(l3.badge[0]), *appear(l3.badge.num, shift=None),
                      GrowFromCenter(l4.badge[0]), *appear(l4.badge.num, shift=None),
                      run_time=min(1.4, c.until("stick")))

            # {stick}: every pivot the smallest or the largest; then the lists fade to pivot circles
            c.wait_until("stick")
            self.play(LaggedStart(*[FlashAround(nd.pivot_glyph, time_width=1.5)
                                    for nd in self.lt.nodes if not nd.is_empty], lag_ratio=0.5),
                      run_time=min(3.0, 0.8 * c.until("one long branch")))
            c.wait_until("one long branch")
            ct = worst_tree("circles", size=36, radius=0.45, pitch=1.5, gap=1.25).place(1.0, CT_ROOT)
            cmap = {tuple(nd.values): nd for nd in ct.nodes}
            pivs, rest = [], []
            for nd in self.lt.nodes:
                self.remove(nd.body)
                if nd.is_empty:
                    rest.append(nd.body)
                    continue
                pg = nd.pivot_glyph.copy()
                others = VGroup(*[g.copy() for g in nd.body.submobjects if g is not nd.pivot_glyph[0]])
                rest.append(others)
                pivs.append((pg, cmap[tuple(nd.values)]))
            self.remove(*[m for x in list(self.lt.edges) + list(self.lt.badges) for m in x.get_family()])
            shown_badges = [nd.badge for nd in self.lt.nodes if not nd.is_empty]   # empty calls never got one
            loose = list(self.lt.edges) + shown_badges + rest + [self.tag]
            self.add(*loose, *[pg for pg, _ in pivs])
            anims = [*during([FadeOut(m) for m in loose], 0, 0.45)]
            anims += during([pg.animate.move_to(cn.pivot_glyph).set_height(cn.pivot_glyph.height).set_color(YELLOW)
                             for pg, cn in pivs], 0.2, 0.8)
            anims += during([GrowFromCenter(cn.body[0]) for cn in ct.nodes]
                            + [Create(e) for e in ct.edges + ct.stubs], 0.5, 1.0)
            self.play(*anims, run_time=2.0)
            for pg, _ in pivs:
                self.remove(pg)
            self.remove(*[cn.body[0] for cn in ct.nodes], *ct.edges, *ct.stubs)
            self.add(ct)
            cap = VGroup(T("every pivot the smallest", 36, FG), T("or the largest", 36, FG)).arrange(
                DOWN, buff=0.18)
            cap.move_to([3.9, 1.35, 0])
            self.play(*appear(cap), run_time=1.0)  # early: caption of the sentence being said
            c.wait_until("zigzags")
            self.play(LaggedStart(*[VShowPassingFlash(e.copy().set_stroke(YELLOW, 7), time_width=0.6)
                                    for e in ct.edges], lag_ratio=0.6), run_time=min(3.0, 0.8 * c.until("ten")))
            # {ten}: 4 + 3 + 2 + 1 = 10, beside ch3's 8
            c.wait_until("ten")
            sm = MathTex("4", "+", "3", "+", "2", "+", "1", "=", "10", font_size=60, color=GOLD)
            sm.move_to([3.9, -0.4, 0])
            self.play(*appear(*sm[:7], lag=0.3, shift=None), run_time=min(2.5, 0.9 * c.until("Ten comparisons")))
            c.wait_until("Ten comparisons")
            self.play(*appear(*sm[7:], shift=None), run_time=0.8)
            eight = VGroup(T("running list:", 34, FG), T("8", 60, GOLD)).arrange(RIGHT, buff=0.3)
            eight.next_to(sm, DOWN, buff=0.7)
            c.wait_until("only eight")
            self.play(*appear(eight), run_time=1.0)
            self.zig = ct
            self.pivots = [nd.body for nd in ct.nodes]
            self.cap, self.sm, self.eight = cap, sm, eight

    # ---- clip 3: the recurrence, the table, the rs counts -----------------------------------
    def clip3(self):
        zig = self.zig
        with self.say("c4.worst.3", gap=1.0) as c:
            # {eq}: the zigzag (and whatever sits beside it) shrinks to the left
            tgt_h = min(6.6, zig.height * 0.68)
            s = tgt_h / zig.height
            dst = zig.copy().scale(s)
            dst.shift([-6.6 - dst.get_left()[0], -0.2 - dst.get_center()[1], 0])
            self.play(zig.animate.scale(s).move_to(dst), *disappear(self.cap, self.sc), run_time=1.5)
            # each call sets aside only its pivot
            self.play(*flash(self.pivots, color=YELLOW, run_time=1.5, time_width=1.5),
                      run_time=min(1.6, c.until("So sorting")))
            c.wait_until("So sorting")
            eq = MathTex("T(n+1)", "=", "T(n)", "+", "n", font_size=60).move_to([RX, 0.6, 0])
            self.play(*during(disappear(self.sm, self.eight), 0, 0.45), *during(appear(eq), 0.5, 1.0),
                      run_time=1.6)
            c.wait_until("Tee of N plus one")
            self.play(FlashUnder(eq, color=YELLOW, run_time=2, time_width=1.5))

            # {table}: Lecture 2's table, eq becomes its second row
            c.wait_until("table")
            lhs = [MathTex(r"T(n+1) = T(n) + 1", font_size=TAB), None,
                   MathTex(r"T(n) = T(n/2) + 1", font_size=TAB), MathTex(r"T(n) = 2T(n/2) + n", font_size=TAB)]
            os_ = [MathTex(tx, font_size=TAB) for tx in ("O(n)", "O(n^2)", r"O(\log n)", r"O(n\log n)")]
            ty = [3.05, 2.3, 1.55, 0.8]
            eq_t = eq.copy().scale(TAB / 60)
            xl = RX - 2.5
            left_at(eq_t, xl, ty[1])
            xc2 = xl + max(eq_t.width, *[m.width for m in lhs if m is not None]) + 0.7
            for i in range(4):
                if lhs[i] is not None:
                    left_at(lhs[i], xl, ty[i])
                left_at(os_[i], xc2, ty[i])
            incoming = [m for m in lhs if m is not None] + os_
            t = min(1.6, 0.5 * c.until("big O"))
            self.play(time_span(eq.animate.scale(TAB / 60).move_to(eq_t), 0, 0.5 * t),
                      *[time_span(FadeIn(m, shift=0.3 * LEFT), 0.5 * t + 0.05 * t * i, 0.6 * t + 0.05 * t * i)
                        for i, m in enumerate(incoming)], run_time=t)
            tag = T("insertion sort's row (Part 2)", 30, DIM)
            tag.next_to(VGroup(*lhs[3:], os_[3]), DOWN, buff=0.4).align_to(lhs[3], LEFT)
            self.play(eq.animate.set_color(YELLOW), *appear(tag), run_time=1.0)
            c.wait_until("big O")
            self.play(os_[1].animate.set_color(RED), FlashAround(os_[1], color=RED, time_width=1.5),
                      run_time=1.5)

            # {rs}: sorted rs costs n(n-1)/2
            c.wait_until("rs")
            hx = RX - 1.0
            h1 = T("sorted rs:", 36, FG)
            h1.shift([hx - h1.get_right()[0], -1.2 - h1.get_center()[1], 0])
            v1 = T("49,995,000", 44, GOLD)
            left_at(v1, hx + 0.3, -1.2)
            f1 = MathTex(r"= \frac{n(n-1)}{2}", font_size=44)
            left_at(f1, v1.get_right()[0] + 0.3, -1.2)
            self.play(*appear(h1), run_time=1.0)  # early: "sorted" is never said; it labels "Sort our ten thousand numbers"
            c.wait_until("forty-nine million")
            self.play(*appear(v1), run_time=1.0)
            c.wait_until("exactly N times")
            self.play(*appear(f1), run_time=1.0)
            # {rev}
            c.wait_until("rev")
            h2 = T("reversed rs:", 36, FG)
            h2.shift([hx - h2.get_right()[0], -2.5 - h2.get_center()[1], 0])
            v2 = T("49,995,000", 44, GOLD)
            left_at(v2, hx + 0.3, -2.5)
            self.play(*appear(h2, v2, lag=0.3), run_time=1.2)
            c.wait_until("same")
            self.play(FlashAround(v2, run_time=1.5, time_width=1.5))

    # ---- clip 4: almost sorted, the irony, the shuffle --------------------------------------
    def clip4(self):
        with self.say("c4.worst.4") as c:
            # {almost}: a long sorted row, the first two of every ten swap
            cells = []
            n = 20
            for i in range(n):
                sq = Square(0.55, color=BLUE, stroke_width=3)
                lab = T(str(i + 1), 28, FG).move_to(sq)
                cells.append(VGroup(sq, lab))
            row = VGroup(*cells)
            for i, cell in enumerate(cells):
                cell.move_to([i * 0.62 + (0.45 if i >= 10 else 0), 0, 0])
            dots = T("…", 44, DIM).next_to(row, RIGHT, buff=0.3)
            full = VGroup(row, dots)
            full.move_to([0, 1.7, 0])
            cap = T("almost sorted: nearly as bad", 40, FG).move_to([0, -2.3, 0])
            sweep_clear(self, time_span(FadeIn(full), 0.6, 1.2), keep=[], run_time=1.2)
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("Swap one pair")
            t = min(2.0, 0.8 * c.until("forty-five million"))
            anims = []
            for b in (0, 10):
                a, d = cells[b], cells[b + 1]
                anims += [a.animate.move_to(d.get_center()).set_color(YELLOW),
                          d.animate.move_to(a.get_center()).set_color(YELLOW)]
            self.play(*anims, path_arc=PI / 2, run_time=t)
            big = T("44,996,000", 64, GOLD).move_to([0, 0.0, 0])
            c.wait_until("still makes")
            self.play(*appear(big), run_time=1.0)

            # {irony}: ch2 s6's scale, insertion sort's GREEN tick, quicksort's RED one
            c.wait_until("sorted input", nth=1)
            sc_ch = sorted_chain()
            sc_ch.shift([-sc_ch.chain.get_center()[0] + 0.3, 2.45 - sc_ch.chain.get_center()[1], 0])
            sc = range_scale().shift(0.75 * DOWN)
            names = [T("insertion sort", 30, GREEN).next_to(sc.ticks[0], DOWN, buff=0.2),
                     T("quicksort", 30, RED).next_to(sc.ticks[2], DOWN, buff=0.2)]
            names[0].shift(RIGHT * max(0, -6.6 - names[0].get_left()[0]))
            caption = T("comparisons for 10,000 sorted items", 30, DIM).move_to([0, -2.4, 0])
            sweep_clear(self, time_span(FadeIn(sc_ch), 0.6, 1.2), time_span(FadeIn(sc.line), 0.6, 1.2),
                        time_span(FadeIn(caption), 0.6, 1.2), keep=[], run_time=1.2)  # early: the scale's caption
            c.wait_until("favourite")
            self.play(GrowFromCenter(sc.ticks[0]), *appear(sc.values[0], names[0]), run_time=1.0)
            c.wait_until("nine thousand")
            self.play(FlashAround(sc.values[0], color=GREEN, run_time=1.5, time_width=1.5))
            c.wait_until("quicksort's worst")
            frame = SurroundingRectangle(sc_ch.chain, color=YELLOW, buff=0.2)
            tag = T("quicksort's worst case (Part 4)", 32, YELLOW).next_to(frame, UP, buff=0.2)
            self.play(GrowFromCenter(sc.ticks[2]), *appear(sc.values[2], names[1]),
                      FadeIn(frame), time_span(FadeIn(tag, shift=0.25 * DOWN), 0.5, 1.5), run_time=1.5)

            # {shuffle}: the chain's cells shuffle into the running chain's order (the scale stays)
            c.wait_until("shuffle")
            sh = shuffled_chain()
            sh.shift([-sh.chain.get_center()[0] + 0.3, 2.45 - sh.chain.get_center()[1], 0])
            old = sc_ch.chain
            order = [0, 2, 4, 1, 3]          # new slot i holds old cell order[i]: 3 5 9 4 7
            slots = [cell.get_center().copy() for cell in old.cells]
            t = min(2.0, 0.6 * c.until("Shuffled"))
            moves = [old.cells[j].animate(path_arc=PI / 2).move_to(slots[i])
                     for i, j in enumerate(order) if i != j]
            self.play(*[FadeOut(a) for a in old.arrows], *moves, run_time=t)
            # the moved cells are exactly sh's cells: hand over to sh
            self.remove(*old.get_family())
            self.add(*sh.chain.cells, sh.chain.nil)
            self.play(*[GrowArrow(a) for a in sh.chain.arrows], run_time=min(1.0, c.until("Shuffled")))
            settle(self, sh.chain)
            c.wait_until("Shuffled")
            gone = [sc.line, sc.ticks[0], sc.ticks[2], sc.values[0], sc.values[2], *names, caption, frame, tag]
            self.play(*disappear(*gone), *swap(sc_ch.label, sh.label), run_time=1.2)
            self.play(*appear(sh.count), run_time=1.0)
            c.wait_until("random order")
            self.play(*appear(sh.note), run_time=1.0)
            settle(self, sh)
            # {unlikely}
            c.wait_until("unlikely")
            cap2 = T("randomise the input: the worst case becomes highly unlikely", 32, YELLOW)
            cap2.move_to([0, -1.6, 0])
            self.play(*appear(cap2), run_time=1.0)
        self.wait(4.0)
