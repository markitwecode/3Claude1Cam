"""Chapter 6, scene 6: the whole lecture, then next lecture, then the end card. Clips c6.recap.1 – c6.recap.3.

Plan
- c6.recap.1: {recap} "Lecture 5: Sorting" (T 46, y 3.42) and a 3 x 2 grid of tile frames (4.3 x 3.0,
  DIM, "Part k" set into the top edge), filled on the marks: P1 ch1's tree_icon + YELLOW boxed
  2^{C(n)} >= n! + "≈ n log₂ n, worst case"; P2 ch2's cards, the 4 slides in between 3 and 5;
  P3 ch3's call_tree circles (root's empty left branch RED); P4 ch4's recursion_tree (GOLD line) and
  worst_tree (RED line), then `quik (xs, sorted)` YELLOW, "no append".
- c6.recap.2: P5 [3; 5] / [9; 4; 7] beside take / drop, the right half sorts, the zipper makes
  3 4 5 7 9 []; GREEN "never worse than n log n", "1.4 s vs 0.53 s". P6 ch6 s3's buckets (tiles 53,
  19, 51), radix lines; {best} buckets shrink left, board3() miniature right, lines swap to "match
  the algorithm / to the application".
- c6.recap.3: {next} grid dims, title swaps to "Next lecture: Datatypes and Trees"; {types} grid sweeps
  out, `type vehicle` reply; {exceptions} `exception Change` + GOLD coin; {trees} the 'a tree reply,
  the 1; 2, 3; 4, 5 tree, DIM "Lecture 7: binary search trees", faint halving bracket; {bonus} all but
  the title clear, ch7 s1's open_card() comes in (cards, then the note); {bye} the title goes.
  Ends static on exactly load_scene("ch7_s1_intro").open_card() for ~8 s (the reversed join: ch7 s1
  opens on it), so the last frame is not empty by design.

Exports for ch7's recap: vehicle_reply(size=30), exception_shot(size=30), tree_reply(size=30),
binary_tree(radius=0.3, dx=0.9, dy=0.8), halving_bracket(op=0.45).
"""
# style: 2
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

TITLE_Y = 3.2
COL_X = (-4.45, 0.0, 4.45)
ROW_TOP = (2.68, -0.62)
TILE_W, TILE_H = 4.3, 2.88
LINE = 28
LINE_PITCH = 0.38


# ------------------------------------------------------------------ next-lecture pictures (ch7 reuses them)
def vehicle_reply(size=30):
    """The reply to the notes' In [84]: `type vehicle = Bike | Motorbike | Car | Lorry`
    (type BLUE, constructors YELLOW). Mono, centred on ORIGIN."""
    return Mono("type vehicle = Bike | Motorbike | Car | Lorry", size,
                t2c={"type": BLUE, "Motorbike": YELLOW, "Bike": YELLOW, "Car": YELLOW, "Lorry": YELLOW})


def coin(v=20, r=0.42):
    """L4 ch4's coin (GOLD disc stroke 4, fill 0.15, value T 34 GOLD), built to its spec."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    return VGroup(disc, T(str(v), 34, GOLD).move_to(disc))


def exception_shot(size=30):
    """`exception Change` (the toplevel's reply; exception BLUE, Change YELLOW) with L4's GOLD
    coin 0.45 to its right. VGroup(code, coin), centred on ORIGIN; .code, .coin."""
    code = Mono("exception Change", size, t2c={"exception": BLUE, "Change": YELLOW})
    c = coin()
    g = VGroup(code, c).arrange(RIGHT, buff=0.45)
    g.code, g.coin = code, c
    return g


def tree_reply(size=30):
    """The reply to In [97]: `type 'a tree = Lf | Br of 'a * 'a tree * 'a tree` ('a PINK,
    type/of BLUE, Lf/Br YELLOW). Mono, centred on ORIGIN (Mono 30: ~11.9 wide)."""
    return Mono("type 'a tree = Lf | Br of 'a * 'a tree * 'a tree", size,
                t2c={"type": BLUE, " of ": BLUE, "'a": PINK, "Lf": YELLOW, "Br": YELLOW})


def binary_tree(radius=0.3, dx=0.9, dy=0.8, size=30):
    """The notes' In [98] tree: 1 on top, 2 and 3 under it, 4 and 5 under 2. BLUE rings, FG
    digits, DIM edges; root at ORIGIN. VGroup(edges, *nodes); .nodes {value: node}."""
    pos = {1: (0, 0), 2: (-dx, -dy), 3: (dx, -dy), 4: (-1.55 * dx, -2 * dy), 5: (-0.45 * dx, -2 * dy)}
    nodes = {}
    for v, (x, y) in pos.items():
        ring = Circle(radius=radius).set_stroke(BLUE, 3).set_fill(BG, 1).move_to([x, y, 0])
        nodes[v] = VGroup(ring, T(str(v), size).move_to(ring))
    edges = VGroup()
    for a, b in ((1, 2), (1, 3), (2, 4), (2, 5)):
        pa, pb = nodes[a][0].get_center(), nodes[b][0].get_center()
        d = (pb - pa) / np.linalg.norm(pb - pa)
        edges.add(Line(pa + radius * d, pb - radius * d).set_stroke(DIM, 3))
    g = VGroup(edges, *nodes.values())
    g.nodes, g.edges = nodes, edges
    return g


def halving_bracket(op=0.45, side=0.26):
    """A faint copy of ch1 s3's halving: 16 BLUE boxes and, under them, the GOLD span left after
    each probe (all 16, the right 8, then 4, then the one found, 41). Centred on ORIGIN."""
    boxes = VGroup(*[Square(side).set_stroke(BLUE, 2, opacity=op) for _ in range(16)]).arrange(RIGHT, buff=0)
    spans = VGroup()
    for k, (a, b) in enumerate(((0, 15), (8, 15), (12, 15), (12, 12))):
        y = boxes.get_bottom()[1] - 0.14 - 0.14 * k
        spans.add(Line([boxes[a].get_left()[0] + 0.03, y, 0], [boxes[b].get_right()[0] - 0.03, y, 0])
                  .set_stroke(GOLD, 3, opacity=op))
    g = VGroup(boxes, spans).move_to(ORIGIN)
    g.boxes, g.spans = boxes, spans
    return g


# ------------------------------------------------------------------ the recap grid
def fit(m, w, h):
    if m.width / w > m.height / h:
        m.scale_to_fit_width(w, scale_stroke=True)
    else:
        m.scale_to_fit_height(h, scale_stroke=True)
    return m


class Tile:
    """One tile: a DIM frame with "Part k" set into its top edge. .icon_c (icon centre),
    .line(i) (centre of text line i)."""

    def __init__(self, k, col, row):
        self.cx, self.top = COL_X[col], ROW_TOP[row]
        L, R = self.cx - TILE_W / 2, self.cx + TILE_W / 2
        B = self.top - TILE_H
        self.label = T(f"Part {k}", LINE, DIM).move_to([L + 0.3, self.top, 0], aligned_edge=LEFT)
        a = self.label.get_left()[0] - 0.12
        b = self.label.get_right()[0] + 0.12
        self.frame = VMobject().set_points_as_corners(
            [[b, self.top, 0], [R, self.top, 0], [R, B, 0], [L, B, 0], [L, self.top, 0], [a, self.top, 0]])
        self.frame.set_stroke(DIM, 1.5)

    def at(self, dy):
        return np.array([self.cx, self.top - dy, 0])

    def text(self, s, i, start=1.75, color=FG, **kw):
        return T(s, LINE, color, **kw).move_to(self.at(start + i * LINE_PITCH))


def tri_tree(t):
    """ch1's recap decision tree (root question, six GREEN leaves), 2.6 wide."""
    ic = load_scene("ch1_s8_recap").tree_icon()
    return fit(ic, 3.0, 1.25).move_to(t.at(0.8))


class Recap(NarratedScene):
    def construct(self):
        self.S2 = load_scene("ch2_s1_hook")
        self.tiles = [Tile(1, 0, 0), Tile(2, 1, 0), Tile(3, 2, 0), Tile(4, 0, 1), Tile(5, 1, 1), Tile(6, 2, 1)]
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(8.0)          # the end card: ch7 s1's open_card(), held still; ch7 s1 opens on it

    # ---------------------------------------------------------------- c6.recap.1
    def clip1(self):
        tl = self.tiles
        with self.say("c6.recap.1") as c:
            self.title = T("Lecture 5: Sorting", 42).move_to(UP * TITLE_Y)
            self.play(*appear(self.title), run_time=1.0)  # early: the recap's title
            parts = []
            for t in tl:
                parts += [t.frame, t.label]
            self.play(*appear(*parts, lag=0.12, shift=None), run_time=1.8)  # early: the grid's shape first, then filled

            # Part 1 {bound}
            t = tl[0]
            tree = tri_tree(t)
            c.wait_until("bound")
            self.play(*appear(tree, shift=None), run_time=1.2)
            bf = MathTex("2", "^{C(n)}", r"\ge", "n!", font_size=40, color=YELLOW).move_to(t.at(1.82))
            bbox = SurroundingRectangle(bf, color=YELLOW, buff=0.14, stroke_width=3)
            c.wait_until("needs about")
            self.play(FadeIn(bf, shift=0.2 * DOWN), GrowFromCenter(bbox), run_time=1.2)
            nl = t.text("≈ n log₂ n, worst case", 0, start=2.45)
            c.wait_until("worst case")
            self.play(*appear(nl, shift=None), run_time=1.0)

            # Part 2 {insertion}
            t = tl[1]
            S2 = self.S2
            K = 0.38
            H = t.at(1.12)
            base = np.array([S2.HAND_X, S2.CARD_Y, 0])

            def slot(n, i):
                p, a = S2.fan_slots(n)[i]
                return H + K * (p - base), a

            cards = {v: S2.make_card(v) for v in (3, 4, 5)}
            for v, (pos, ang) in ((3, slot(2, 0)), (5, slot(2, 1)), (4, (slot(3, 1)[0] + UP * 0.75, 0.0))):
                S2.apply_pose(cards[v], pos, ang, K)
            cards[3].set_z_index(1)
            cards[4].set_z_index(4)
            cards[5].set_z_index(3)
            l1 = t.text("insertion sort", 0, start=2.05)
            l2 = t.text("simple, O(n²)", 1, start=2.05, t2c={"O(n²)": GOLD})
            c.wait_until("insertion")
            self.play(*appear(cards[3], cards[5], cards[4], l1, lag=0.15, shift=None), run_time=1.2)
            c.wait_until("slides")
            moves = []
            for v, i in ((3, 0), (5, 2)):
                pos, ang = slot(3, i)
                moves.append(S2.card_move(cards[v], pos, ang, window=(0.0, 0.45), run_time=1.8))
            pos, ang = slot(3, 1)
            moves.append(S2.card_move(cards[4], pos, ang, window=(0.35, 1.0), z_end=2, run_time=1.8,
                                      stroke=S2.glow((0.0, 0.15), (0.85, 1.0))))
            self.play(*moves, run_time=1.8)
            c.wait_until("simple")
            self.play(*appear(l2, shift=None), run_time=1.0)

            # Part 3 {quick}
            t = tl[2]
            ct = load_scene("ch3_s6_trace").call_tree(form="circles", radius=0.42, gap=0.85, badges=False).place(1.0, ORIGIN)
            ct.root.stubs["left"].set_stroke(RED, 5)
            fit(ct, 3.7, 1.42).move_to(t.at(1.03) + RIGHT * 0.15)
            q1 = t.text("quicksort", 0, start=2.0)
            q2 = t.text("split around a pivot", 1, start=2.0)
            c.wait_until("quick")
            self.play(*appear(ct, q1, lag=0.3, shift=None), run_time=1.3)
            c.wait_until("pivot")
            self.play(*appear(q2, shift=None), run_time=1.0)

            # Part 4 {average} {worst} {quik}
            t = tl[3]
            rt = load_scene("ch4_s2_average").recursion_tree(width=5.6, leaves=8, pitch=0.6, box_h=0.5)
            fit(rt, 1.8, 0.75).move_to(t.at(0.58) + LEFT * 0.95)
            wt = load_scene("ch4_s3_worst").worst_tree(form="circles", size=36, radius=0.45,
                                                       pitch=1.3, gap=0.7, badges=False)
            wt.place(1.0, ORIGIN)
            fit(wt, 1.7, 0.8).move_to(t.at(0.58) + RIGHT * 1.05)
            a1 = t.text("n log n on average", 0, start=1.2, color=GOLD)
            a2 = t.text("O(n²) on sorted input", 1, start=1.2, color=RED)
            a3 = Mono("quik (xs, sorted)", LINE, YELLOW).move_to(t.at(1.2 + 2 * LINE_PITCH))
            a4 = t.text("no append", 3, start=1.2)
            c.wait_until("average")
            self.play(*appear(rt, a1, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("worst")
            self.play(*appear(wt, a2, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("quik")
            self.play(*appear(a3, shift=None), run_time=1.0)
            c.wait_until("removes its appends")
            self.play(*appear(a4, shift=None), run_time=1.0)

    # ---------------------------------------------------------------- c6.recap.2
    def clip2(self):
        tl = self.tiles
        with self.say("c6.recap.2") as c:
            # Part 5 {merge}
            t = tl[4]
            s = 0.3
            ic = t.at(0.75)

            def mini(vals):
                ch = ConsChain(list(vals)).scale(s)
                for m in [cl.label for cl in ch.cells] + [ch.nil.label]:
                    m.scale(1.6)
                return ch

            out = mini([3, 4, 5, 7, 9]).move_to(ic)
            xs = [cl.get_x() for cl in out.cells]
            yT, yB = ic[1] + 0.4, ic[1] - 0.4

            def at_cell(ch, i, x, y):
                return ch.shift(np.array([x, y, 0]) - ch.cells[i].get_center())

            Lh = at_cell(mini([3, 5]), 0, xs[0], yT)
            Rh = at_cell(mini([9, 4, 7]), 0, xs[2], yB)
            tk = Mono("take", LINE, YELLOW).next_to(Lh.nil, RIGHT, buff=0.3)
            dp = Mono("drop", LINE, YELLOW).next_to(Rh.cells[0], LEFT, buff=0.3)
            c.wait_until("merge")
            self.play(*appear(Lh, Rh, shift=None, lag=0.2), run_time=1.2)
            c.wait_until("take and drop")
            self.play(*appear(tk, dp, lag=0.3, shift=None), run_time=1.0)

            c.wait_until("merges")
            Rs = at_cell(mini([4, 7, 9]), 0, xs[2], yB)
            self.play(*swap(Rh, Rs), run_time=0.8)
            moves = [(Lh.cells[0], xs[0], (0.08, 0.4)), (Rs.cells[0], xs[1], (0.18, 0.52)),
                     (Lh.cells[1], xs[2], (0.3, 0.64)), (Rs.cells[1], xs[3], (0.42, 0.74)),
                     (Rs.cells[2], xs[4], (0.5, 0.82)), (Rs.nil, out.nil.get_x(), (0.55, 0.85))]
            anims = during([FadeOut(m) for m in (*Lh.arrows, Lh.nil, *Rs.arrows, tk, dp)], 0, 0.15)
            for m, x, (a, b) in moves:
                st = m.get_center()
                end = np.array([x, ic[1], 0])
                p = VMobject().set_points_as_corners([st, [x, st[1], 0], end])
                anims += during([MoveAlongPath(m, p)], a, b)
            anims += during([GrowArrow(ar) for ar in out.arrows], 0.8, 0.95)
            self.play(*anims, run_time=min(1.8, max(1.2, c.until("safe"))))
            self.remove(*Lh.get_family(), *Rs.get_family(), *out.arrows)
            self.add(out)

            m1 = t.text("never worse than", 0, start=1.6, color=GREEN)
            m2 = t.text("n log n", 1, start=1.6, color=GREEN)
            m3 = t.text("1.4 s vs 0.53 s", 2, start=1.6, t2c={"1.4 s": GOLD, "vs 0.53 s": DIM})
            c.wait_until("safe")
            self.play(*appear(m1, m2, lag=0.3, shift=None), run_time=1.0)
            c.wait_until("slower")
            self.play(*appear(m3, shift=None), run_time=1.0)

            # Part 6 {radix}
            t = tl[5]
            S1 = load_scene("ch6_s1_hook")
            row = S1.bucket_row(color=BLUE)
            tiles = VGroup()
            for n in (53, 19, 51):
                nt = S1.num_tile(n)
                S1.place_tile(nt, row, n % 10)
                tiles.add(nt)
            buckets = VGroup(row, tiles)
            fit(buckets, 3.8, 1.1).move_to(t.at(0.8))
            r1 = t.text("radix sort", 0, start=1.6)
            r2 = t.text("no comparisons; linear", 1, start=1.6, t2c={"no comparisons": GOLD})
            r3 = t.text("for small integers", 2, start=1.6)
            c.wait_until("radix")
            self.play(*appear(buckets, r1, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("never compares")
            self.play(*appear(r2, shift=None), run_time=1.0)
            c.wait_until("small integers")
            self.play(*appear(r3, shift=None), run_time=1.0)

            # {best}: the buckets and radix lines give way to the full scoreboard, then the moral
            board = load_scene("ch6_s2_summary").board3()
            fit(board, 3.95, 1.6).move_to(t.at(1.05))
            b1 = t.text("match the algorithm", 0, start=2.15)
            b2 = t.text("to the application", 1, start=2.15)
            c.wait_until("best")
            self.play(*during(disappear(buckets, r1, r2, r3), 0, 0.45),
                      *during(appear(board, shift=None), 0.5, 1.0), run_time=1.6)
            c.wait_until("matches")
            self.play(*appear(b1, b2, lag=0.25, shift=None), run_time=1.2)

    # ---------------------------------------------------------------- c6.recap.3
    def clip3(self):
        with self.say("c6.recap.3") as c:
            grid = [m for m in self.mobjects if m is not self.title]
            nt = T("Next lecture: Datatypes and Trees", 42, t2c={"Datatypes and Trees": YELLOW})
            nt.move_to(UP * TITLE_Y)
            self.play(*set_alpha(grid, DIMMED), *swap(self.title, nt), run_time=1.4)

            veh = vehicle_reply().move_to(UP * 2.15)
            c.wait_until("types")
            sweep_clear(self, *appear(veh, shift=None), keep=[nt], run_time=1.4)

            exc = exception_shot().move_to(UP * 0.95)
            c.wait_until("exceptions")
            self.play(*appear(exc.code), run_time=1.0)
            c.wait_until("make change")
            self.play(FadeIn(exc.coin, scale=0.6), run_time=0.9)

            tr = tree_reply().move_to(DOWN * 0.25)
            bt = binary_tree().move_to([-3.4, -2.05, 0])
            tag = T("Lecture 7: binary search trees", 32, DIM).move_to([2.6, -1.55, 0])
            hb = halving_bracket().move_to([2.6, -2.45, 0])
            c.wait_until("trees")
            self.play(*appear(tr, shift=None), run_time=1.0)
            c.wait_until("binary trees")
            self.play(*appear(bt.edges, *bt.nodes.values(), lag=0.15, shift=None), run_time=1.4)
            c.wait_until("which lead to")
            self.play(*appear(tag), run_time=1.0)
            c.wait_until("binary search", nth=1)
            self.play(FadeIn(hb), run_time=1.0)

            end = load_scene("ch7_s1_intro").open_card()
            c.wait_until("four exercises")
            sweep_clear(self, keep=[nt], run_time=1.0)
            self.play(*appear(*end.cards, lag=0.2, shift=None), run_time=1.4)  # early: the four cards whole, then named
            c.wait_until("bonus chapter")
            self.play(*appear(end.note), run_time=1.0)
            c.wait_until("bye")
            self.play(*disappear(nt), run_time=1.0)
            self.remove(*end.cards, end.note)
            self.add(end)
