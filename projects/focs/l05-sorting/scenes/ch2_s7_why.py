"""Chapter 2, scene 7: Why bother, and recap. Clips c2.why.1 – c2.why.5.

Plan
- c2.why.1: YELLOW "why so slow?"; three candidate boxes (GOLD "O(n²) comparisons",
  GOLD "lots of copying", DIM "recursion"); the DIM one struck through, L3's maxim in DIM
  beneath; the GOLD pair flashes on "the comparisons and the copying".
- c2.why.2: RED "174 s" (insertion sort) and GOLD "1.4 s" (next-worst of the three), with
  proportional bars under them (11 units vs 0.09).
- c2.why.3: YELLOW "why learn it?", GREEN tags; `ins` at the root of a tree to merge sort /
  heapsort ("refinements"); `ins x ys` born from the root, rewritten to `merge (xs, ys)`, "Part 5".
- c2.why.4: recap in ch1_s8's layout ("Recap" T 52 at y 3.3, icon left, T 34 line right, block
  centred): cells icon, insort code + ticked chain, halved staircase, comparison scale.
- c2.why.5: rows sweep out, title becomes "Next: quicksort"; ch1's scoreboard (imported) with
  insertion sort's row filled and floor solid, quicksort's row lit YELLOW, its "?" pulsing;
  beneath it the chain 5 → 3 → 9 → 4 → 7 splits round the YELLOW pivot 5. End card ~8 s.
Every `ins` / `insort` in code is YELLOW (s2's ocode look).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

from scenes.ch1_s4_contest import make_scoreboard  # noqa: E402
from scenes.ch2_s6_bestworst import range_scale  # noqa: E402

# recap layout (ch1_s8_recap's look, four rows)
ICON_W, ICON_H = 2.8, 1.15
ROW_Y0, ROW_PITCH = 1.95, 1.5
TEXT_GAP = 0.45
TITLE_Y = 3.3


def fit(m, w=ICON_W, h=ICON_H):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


def ycode(src, size):
    """Code with every `ins` (and `insort`) YELLOW, as in s2."""
    c = Code(src, size=size)
    for key in ("ins", "insort"):
        k = 0
        while True:
            try:
                g = c.find(key, nth=k)
            except ValueError:
                break
            g.set_color(YELLOW)
            k += 1
    return c


def tag_box(text, color, size=36):
    t = T(text, size, color)
    box = RoundedRectangle(corner_radius=0.16, width=t.width + 0.7, height=0.95)
    box.set_stroke(color, 3).move_to(t)
    return VGroup(box, t)


# ── recap icons (built at full scale, then fitted; parts are animated one by one) ──────────
def cells_icon():
    old = ConsChain([3, 5, 9])
    new = [ConsCell(v, color=YELLOW) for v in (3, 4, 5)]
    xs = (old.cells[0].get_x() - 2.3, old.cells[0].get_x(), old.cells[1].get_x())
    for cell, x in zip(new, xs):
        cell.move_to([x, 1.9, 0])
    a1 = link(new[0], new[1], color=YELLOW)
    a2 = link(new[1], new[2], color=YELLOW)
    share = link(new[2], old.cells[2], color=YELLOW)
    teal9 = ConsCell(9, color=TEAL).move_to(old.cells[2])
    g = VGroup(old, *new, a1, a2, share, teal9)
    fit(g)
    g.old, g.new, g.new_arrows, g.share, g.teal9 = old, new, [a1, a2], share, teal9
    return g


INSORT_SRC = "let rec insort = function\n  | [] -> []\n  | x::xs -> ins x (insort xs)"


def insort_icon():
    code = ycode(INSORT_SRC, 28)
    chain = ConsChain([3, 4, 5, 7, 9]).scale(0.5)
    chain.next_to(code, DOWN, buff=0.4).align_to(code, LEFT)
    tick = check_mark(GREEN).scale(1.3).next_to(chain, RIGHT, buff=0.3)
    g = VGroup(code, chain, tick)
    fit(g)
    g.code, g.chain, g.tick = code, chain, tick
    return g


def stairs_icon(n=8, side=0.3, pitch=0.36):
    rows, full, halves = VGroup(), [], []
    for i in range(n):
        row = VGroup(*[Square(side).set_fill(GOLD, 0.9).set_stroke(width=0).move_to([j * pitch, -i * pitch, 0])
                       for j in range(i)])
        rows.add(row)
        keep = (i + 1) // 2
        full.extend(row[:keep])
        halves.extend(row[keep:])
    # row 0 is empty: keep its place, so the staircase starts with one block
    g = VGroup(*[r for r in rows if len(r)])
    fit(g)
    g.rows = [r for r in rows if len(r)]
    g.halves = halves
    return g


def scale_icon(w=2.6):
    """s6's range scale, line and ticks only (sorted GREEN, random, reversed RED)."""
    rs = range_scale(width=w)
    g = VGroup(rs.line, *rs.ticks)
    g.axis, (g.t_sorted, g.t_rand, g.t_rev) = rs.line, list(rs.ticks)
    return g


class WhyAndRecap(NarratedScene):
    def construct(self):
        self.why_slow()
        self.useless()
        self.worth()
        self.build_recap()
        self.recap()
        self.teaser()
        self.wait(7.2)                       # the end card; music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c2.why.1 ────────────────────────────────────────────────────────────────
    def why_slow(self):
        q = T("why so slow?", 56, YELLOW).move_to(UP * 1.65)
        b1 = tag_box("O(n²) comparisons", GOLD)
        b2 = tag_box("lots of copying", GOLD)
        b3 = tag_box("recursion", DIM)
        VGroup(b1, b2, b3).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.25)
        strike = Line(b3.get_left() + 0.12 * LEFT, b3.get_right() + 0.12 * RIGHT).set_stroke(RED, 5)
        maxim = T("“Never add an accumulator merely out of habit.”", 32, DIM, slant=ITALIC)
        maxim.move_to(DOWN * 1.9)

        with self.say("c2.why.1") as c:
            self.play(FadeIn(q, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("cause")
            self.play(FadeIn(b1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("copying")
            self.play(FadeIn(b2, shift=0.3 * DOWN),
                      time_span(FadeIn(b3, shift=0.3 * DOWN), 0.6, 1.6), run_time=1.6)
            c.wait_until("iter")
            self.play(Create(strike), time_span(FadeIn(maxim, shift=0.2 * DOWN), 0.6, 1.8), run_time=1.8)
            c.wait_until("comparisons and the copying")
            self.play(FlashAround(b1, color=GOLD, time_width=1.5),
                      FlashAround(b2, color=GOLD, time_width=1.5),
                      run_time=min(1.8, c.until()))

    # ── c2.why.2 ────────────────────────────────────────────────────────────────
    def useless(self):
        lab1 = T("insertion sort", 40).move_to([-3.4, 1.85, 0])
        big1 = T("174 s", 120, RED).move_to([-3.4, 0.65, 0])
        lab2 = T("next-worst of the three", 40).move_to([3.4, 1.85, 0])
        big2 = T("1.4 s", 120, GOLD).move_to([3.4, 0.65, 0])
        x0, full = -5.5, 11.0
        bar1 = Rectangle(width=full, height=0.42).set_fill(RED, 0.85).set_stroke(width=0)
        bar1.move_to([x0 + full / 2, -1.35, 0])
        w2 = full * 1.4 / 174
        bar2 = Rectangle(width=w2, height=0.42).set_fill(GOLD, 1).set_stroke(width=0)
        bar2.move_to([x0 + w2 / 2, -2.05, 0])

        with self.say("c2.why.2", gap=1.3) as c:
            sweep_clear(self, time_span(FadeIn(big1, scale=0.9), 0.5, 1.5),
                        time_span(FadeIn(lab1, shift=0.3 * DOWN), 0.8, 1.7), run_time=1.7)
            c.wait_until("times")
            self.play(GrowFromEdge(bar1, LEFT), rate_func=linear,
                      run_time=min(3.0, 0.9 * c.until("while")))
            c.wait_until("while the")
            self.play(FadeIn(lab2, shift=0.3 * DOWN), FadeIn(big2, scale=0.9), run_time=1.0)
            c.wait_until("one point four")
            self.play(GrowFromEdge(bar2, LEFT), run_time=0.4)
            self.play(FlashAround(big2, color=GOLD, time_width=1.5), run_time=min(1.5, c.until()))

    # ── c2.why.3 ────────────────────────────────────────────────────────────────
    def worth(self):
        q = T("why learn it?", 52, YELLOW).move_to(UP * 3.0)
        t1 = tag_box("easy to code", GREEN, 34)
        t2 = tag_box("shows the concepts", GREEN, 34)
        VGroup(t1, t2).arrange(RIGHT, buff=0.6).move_to(UP * 1.8)
        root = Mono("ins", 52, YELLOW).move_to(UP * 0.55)
        leaf_m = T("merge sort", 40).move_to([-3.2, -1.0, 0])
        leaf_h = T("heapsort", 40).move_to([3.2, -1.0, 0])
        ar_m = Arrow(root.get_bottom(), leaf_m.get_top(), buff=0.15, stroke_width=3).set_color(DIM)
        ar_h = Arrow(root.get_bottom(), leaf_h.get_top(), buff=0.15, stroke_width=3).set_color(DIM)
        refine = T("refinements", 32, DIM, slant=ITALIC).move_to(DOWN * 0.45)
        ins_c = ycode("ins x ys", 44).move_to([-3.2, -2.0, 0])
        mrg_c = ycode("merge (xs, ys)", 44).move_to([-3.2, -2.85, 0])
        part5 = T("Part 5", 32, DIM).next_to(leaf_m, LEFT, buff=0.45)

        with self.say("c2.why.3", gap=1.5) as c:
            sweep_clear(self, time_span(FadeIn(q, shift=0.3 * DOWN), 0.5, 1.5), run_time=1.5)
            c.wait_until("easy")
            self.play(FadeIn(t1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("shows")
            self.play(FadeIn(t2, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("refine")
            self.play(FadeIn(root, shift=0.2 * DOWN), run_time=0.9)
            c.wait_until("merge sort")
            self.play(LaggedStart(AnimationGroup(GrowArrow(ar_m), FadeIn(leaf_m, shift=0.3 * DOWN)),
                                  AnimationGroup(GrowArrow(ar_h), FadeIn(leaf_h, shift=0.3 * DOWN)),
                                  lag_ratio=0.5),
                      run_time=min(1.8, 0.9 * c.until("refinements")))
            c.wait_until("refinements")
            self.play(FadeIn(refine, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("In part five")
            self.play(*set_alpha([leaf_h, ar_h], DIMMED),
                      TransformFromCopy(root, ins_c.text),
                      time_span(FadeIn(part5, shift=0.2 * DOWN), 0.6, 1.5), run_time=1.6)
            c.wait_until("does what")
            self.play(TransformMatchingStrings(ins_c.text.copy(), mrg_c.text), run_time=1.5)
            c.wait_until("whole sorted list")
            self.play(FlashAround(mrg_c.find("xs"), color=YELLOW, time_width=1.5), run_time=1.0)
            c.wait_until("instead of")
            self.play(FlashAround(ins_c.find("x"), color=YELLOW, time_width=1.5),
                      run_time=min(1.0, c.until()))

    # ── c2.why.4: the recap ─────────────────────────────────────────────────────
    def build_recap(self):
        self.title = T("Recap", 52).move_to(UP * TITLE_Y)
        self.ic1, self.ic2, self.ic3, self.ic4 = cells_icon(), insort_icon(), stairs_icon(), scale_icon()
        self.l1 = T("ins copies up to its stop, shares the rest", 34,
                    t2c={"ins": YELLOW, "copies": YELLOW, "shares the rest": TEAL})
        self.l2 = T("insort: sorts the tail, inserts the head", 34, t2c={"insort": YELLOW})
        self.l3 = T("≈ n²/4 comparisons:  O(n²)", 34, t2c={"≈ n²/4": GOLD, "O(n²)": RED})
        self.l4 = T("sorted: n − 1   ·   reversed: n(n − 1)/2", 34,
                    t2c={"sorted:": GREEN, "reversed:": RED, "·": DIM})
        select(self.l4, "n − 1")[0].set_color(GOLD)
        select(self.l4, "n(n − 1)/2")[0].set_color(GOLD)
        icons = [self.ic1, self.ic2, self.ic3, self.ic4]
        texts = [self.l1, self.l2, self.l3, self.l4]
        x_text = ICON_W / 2 + TEXT_GAP
        for i, (icon, text) in enumerate(zip(icons, texts)):
            y = ROW_Y0 - i * ROW_PITCH
            icon.move_to([0, y, 0])
            text.move_to([0, y, 0])
            text.shift((x_text - text.get_left()[0]) * RIGHT)
        block = VGroup(*icons, *texts)
        block.shift(-block.get_center()[0] * RIGHT)

    def recap(self):
        ic1, ic2, ic3, ic4 = self.ic1, self.ic2, self.ic3, self.ic4
        l1a = select(self.l1, "ins copies up to its stop,")[0]
        l1b = select(self.l1, "shares the rest")[0]
        l3a = select(self.l3, "≈ n²/4 comparisons:")[0]
        l3b = select(self.l3, "O(n²)")[0]
        l4a = select(self.l4, "sorted: n − 1")[0]
        l4b = VGroup(*select(self.l4, "·")[0], *select(self.l4, "reversed: n(n − 1)/2")[0])
        old = ic1.old
        old_parts = [*old.cells, *old.arrows, old.nil]

        with self.say("c2.why.4", gap=1.2) as c:
            sweep_clear(self, time_span(FadeIn(self.title, shift=0.3 * DOWN), 0.5, 1.5), run_time=1.5)

            c.wait_until("r1")
            self.play(*[FadeIn(p) for p in old_parts],
                      time_span(FadeIn(l1a, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("It copies")
            self.play(LaggedStart(*[TransformFromCopy(o, n) for o, n in zip(old.cells, ic1.new)],
                                  lag_ratio=0.25),
                      time_span(LaggedStart(*[GrowArrow(a) for a in ic1.new_arrows], lag_ratio=0.4), 0.8, 1.6),
                      run_time=1.6)
            c.wait_until("shares the rest")
            self.play(GrowArrow(ic1.share),
                      Transform(old.cells[2], ic1.teal9),
                      old.arrows[2].animate.set_color(TEAL),
                      time_span(FadeIn(l1b, shift=0.2 * DOWN), 0.3, 1.2), run_time=1.2)

            c.wait_until("r2")
            self.play(FadeIn(ic2.code), FadeIn(ic2.chain),
                      time_span(FadeIn(self.l2, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("always in order")
            self.play(GrowFromCenter(ic2.tick), run_time=0.8)

            c.wait_until("r3")
            self.play(LaggedStart(*[FadeIn(r, shift=0.15 * RIGHT) for r in ic3.rows], lag_ratio=0.15),
                      run_time=1.4)
            c.wait_until("half as many")
            self.play(*set_alpha(ic3.halves, DIMMED), run_time=1.2)
            c.wait_until("N squared over four")
            self.play(FadeIn(l3a, shift=0.2 * DOWN), run_time=1.0)
            c.wait_until("Quadratic")
            self.play(FadeIn(l3b, shift=0.2 * DOWN), run_time=0.8)

            c.wait_until("r4")
            self.play(Create(ic4.axis), FadeIn(ic4.t_rand), GrowFromCenter(ic4.t_sorted),
                      time_span(FadeIn(l4a, shift=0.2 * DOWN), 0.4, 1.4), run_time=1.4)
            c.wait_until("reversed input")
            self.play(GrowFromCenter(ic4.t_rev), FadeIn(l4b, shift=0.2 * DOWN), run_time=1.0)

    # ── c2.why.5: next time, quicksort (the end card) ─────────────────────────────
    def teaser(self):
        nxt = T("Next: quicksort", 52, t2c={"quicksort": YELLOW}).move_to(UP * TITLE_Y)

        # the board as ch1 leaves it (solid floor), with insertion sort's row filled as in s5
        sb = make_scoreboard(bound="118,458")
        for col, val in enumerate(("25,146,194", "174 s")):
            v = T(val, 44, GOLD).move_to(sb.cells[0][col])
            sb.cells[0].submobjects[col] = v

        # end card: board on top, the split chain under it (chain 0.55, kept above y = -3.5)
        CH, yc, lift, drop = 0.55, -2.37, 0.4, 0.85
        top = 2.78
        avail = top - (yc + lift + CH / 2 + 0.15)
        s_big = min(5.75 / sb.height, 11.6 / sb.width)
        s_small = min(avail / sb.height, 12.0 / sb.width)
        sb.scale(s_big)
        sb.move_to([0, top - sb.height / 2, 0])

        qrow = VGroup(sb.row_labels[1], *sb.cells[1])
        lit = Rectangle(width=sb.width + 0.3, height=qrow.height + 0.3)
        lit.set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15).move_to([sb.get_x(), qrow.get_y(), 0])
        lit.set_z_index(-1)

        chain = ConsChain([5, 3, 9, 4, 7]).scale(CH).move_to([0, yc, 0])
        parts = [*chain.cells, *chain.arrows, chain.nil]
        pivot = ConsCell(5, color=YELLOW).scale(CH).move_to([0, yc + lift, 0])
        pivot.label.set_color(YELLOW)
        L = ConsChain([3, 4]).scale(CH).move_to([-3.4, yc - drop, 0])
        R = ConsChain([9, 7]).scale(CH).move_to([3.4, yc - drop, 0])
        le = T("≤ 5", 40, t2c={"5": YELLOW}).next_to(L, UP, buff=0.3)
        gt = T("> 5", 40, t2c={"5": YELLOW}).next_to(R, UP, buff=0.3)

        recap_parts = [m for m in self.mobjects if m is not self.title]
        with self.say("c2.why.5") as c:
            self.play(*set_alpha(recap_parts, DIMMED), FadeTransform(self.title, nxt), run_time=0.9)
            sweep_clear(self, time_span(FadeIn(sb), 0.5, 1.3), keep=[nxt], run_time=1.3)
            c.wait_until("quicksort")
            pulse = (lambda t: there_and_back((2 * t) % 1.0))
            self.play(FadeIn(lit),
                      *[q.animate(rate_func=pulse).scale(1.4) for q in sb.cells[1]],
                      run_time=1.2)
            settle(self, sb, add=[lit])
            c.wait_until("divide")
            sb.generate_target()
            sb.target.scale(s_small / s_big)
            sb.target.move_to([0, top - sb.target.height / 2, 0])
            self.play(MoveToTarget(sb),
                      time_span(LaggedStart(*[FadeIn(p) for p in parts], lag_ratio=0.08), 0.5, 1.3),
                      run_time=1.3)
            c.wait_until("one item")
            self.play(Transform(chain.cells[0], pivot), FadeOut(chain.arrows[0]), run_time=1.0)
            c.wait_until("smaller ones")
            self.play(*[FadeOut(a) for a in chain.arrows[1:]], FadeOut(chain.nil),
                      chain.cells[1].animate.move_to(L.cells[0]),
                      chain.cells[3].animate.move_to(L.cells[1]),
                      time_span(FadeIn(le, shift=0.2 * DOWN), 0.6, 1.3), run_time=1.3)
            c.wait_until("larger ones")
            self.play(chain.cells[2].animate.move_to(R.cells[0]),
                      chain.cells[4].animate.move_to(R.cells[1]),
                      time_span(FadeIn(gt, shift=0.2 * DOWN), 0.6, 1.3), run_time=1.3)
            c.wait_until("sorts each part")
            self.play(*[FadeIn(m) for m in (*L.arrows, L.nil, *R.arrows, R.nil)],
                      FlashAround(L.copy(), color=YELLOW, time_width=1.5),
                      FlashAround(R.copy(), color=YELLOW, time_width=1.5),
                      run_time=min(1.6, c.until()))
