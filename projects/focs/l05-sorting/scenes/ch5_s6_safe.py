"""Chapter 5, scene 6: never a bad split: merge sort's n log n is a worst case; measured. Clips c5.safe.1 – c5.safe.4.

Exported for s7's recap: `level_tree()` -> the n = 10,000 recursion tree (ch4 s2's
`recursion_tree()` relabelled 10,000 / 5,000 / 2,500 / 1), with its GOLD "≤ n comparisons" tags
(.tags), the left brace (.brace) with "14 levels" / "log2 10,000 ≈ 13.3" (.blabel), and the bottom
row only partly filled (.empty: the faint leaves).  Built at full frame; scale/move it.
{why} uses ch4 s3's `worst_tree("circles")` under the sorted chain.
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
from lib.style import *  # noqa: E402,F403

from scenes.ch4_s2_average import recursion_tree  # noqa: E402
from scenes.ch4_s3_worst import worst_tree  # noqa: E402
from scenes.ch5_s1_hook import filled_board, pill  # noqa: E402
from scenes.ch5_s5_trace import PARENT, POS, split_tree, tree_edge  # noqa: E402

SORTED = (3, 4, 5, 7, 9)
RUNNING = (3, 5, 9, 4, 7)
REVERSED = (9, 7, 5, 4, 3)

# ── clip 1: the two small trees ─────────────────────────────────────────────────────────
TOP = 1.75          # top edge of both trees
NAME_Y = 2.7        # "quicksort" / "merge sort"
QT_S, MT_S, MT_SY = 0.6, 0.55, 0.85   # merge tree: rows scaled MT_S, levels spread MT_SY


def grow_text(g, size=29):
    """Bring every Text in a miniature back up to `size` (in place, about its own centre)."""
    for m in g.get_family():
        if isinstance(m, Text) and m.font_size < size - 0.5:
            m.scale(size / m.font_size)
    return g


def quick_tree():
    """ch4 s3's worst_tree() (circle zigzag 3, 9, 4, 7, 5, RED empty sides) under the sorted chain."""
    chain = grow_text(ConsChain(list(SORTED)).scale(0.43))
    chain.move_to([-6.6 + chain.width / 2, TOP - chain.height / 2, 0])
    wt = worst_tree("circles", size=26, radius=0.3, pitch=0.9, gap=0.66)
    wt.next_to(chain, DOWN, buff=0.3).set_x(chain.get_x())
    return VGroup(chain, wt)


def merge_tree(values):
    """s5's split tree of `values`, small, on the right; the same place for any values."""
    g, ref = _spread(split_tree(values)), _spread(split_tree(SORTED))
    g.shift([6.6 - ref.get_right()[0], TOP - ref.get_top()[1], 0])
    return grow_text(g)


def _spread(g):
    for k, r in g.rows.items():
        r.scale(MT_S).move_to([POS[k][0] * MT_S, POS[k][1] * MT_SY, 0])
    for k, p in PARENT.items():
        g.edges[k].become(tree_edge(g.rows[p], g.rows[k]))
    return g


def strip_labels(g):
    """Take the value labels out of the tree's cells: returns them as one VGroup."""
    labs = VGroup()
    for r in g.rows.values():
        for cell in r.cells:
            cell.remove(cell.label)
            labs.add(cell.label)
    return labs


# ── clip 2: the n = 10,000 tree ────────────────────────────────────────────────────────
TREE_W, TREE_X, PITCH = 5.4, 0.35, 1.15
N_FULL = 4          # of 16 leaves drawn solid: 1,808 of 8,192 slots on the 14th level ≈ 22%


def level_tree(partial=True):
    """ch4 s2's recursion tree for merge sort, n = 10,000, with "≤ n comparisons" tags and
    the 14-level brace. partial=False: every leaf drawn solid (the scene dims them on cue)."""
    tree = recursion_tree(labels=("10{,}000", "5{,}000", "2{,}500", "1"), width=TREE_W,
                          pitch=PITCH, box_h=0.7)
    tree.shift(RIGHT * TREE_X)
    xr = tree.get_right()[0] + 0.45
    tags = VGroup(*[T("≤ n comparisons", 30, GOLD).move_to([0, row.get_y(), 0]).align_to([xr, 0, 0], LEFT)
                    for row in tree.rows])
    brace = tree.bracket.brace
    lvl = T("14 levels", 34, GOLD)
    logl = MathTex(r"\log_2 10{,}000 \approx 13.3", font_size=36, color=GOLD)
    blabel = VGroup(lvl, logl).arrange(DOWN, buff=0.25)
    blabel.next_to(brace, LEFT, buff=0.2)
    empty = list(tree.rows[3])[N_FULL:]
    if partial:
        for node in empty:
            node.set_opacity(0.15)
    g = VGroup(tree, tags, brace, blabel)
    g.tree, g.tags, g.brace, g.blabel, g.lvl, g.logl, g.empty = tree, tags, brace, blabel, lvl, logl, empty
    return g


# ── clip 3: the number line of comparisons ─────────────────────────────────────────────
Y0 = 0.3
MAXV = 140_000


def xv(v):
    return -6.0 + 12.0 * v / MAXV


def vtick(v, y_from, y_to, color, dashed=False, width=5):
    a, b = [xv(v), y_from, 0], [xv(v), y_to, 0]
    if dashed:
        return DashedLine(a, b, dash_length=0.12, dashed_ratio=0.55).set_stroke(color, width)
    return Line(a, b).set_stroke(color, width)


def label_left(text, color, v, y, size=30):
    return T(text, size, color).move_to([0, y, 0]).align_to([xv(v) - 0.14, 0, 0], RIGHT)


def label_right(text, color, v, y, size=30):
    return T(text, size, color).move_to([0, y, 0]).align_to([xv(v) + 0.14, 0, 0], LEFT)


class Safe(NarratedScene):
    def construct(self):
        self.why()
        self.levels()
        self.measure()
        self.board()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # c5.safe.1: two trees; balanced halves; the shape ignores the values
    def why(self):
        qt = quick_tree()
        mt = merge_tree(SORTED)
        labs = strip_labels(mt)
        qname = T("quicksort", 40).move_to([qt.get_x(), NAME_Y, 0])
        mname = T("merge sort", 40).move_to([mt.get_x(), NAME_Y, 0])
        self.qt, self.mt, self.labs = qt, mt, labs

        splits = [("root", ("L", "R"), "2 + 3"), ("L", ("LL", "LR"), "1 + 1"), ("R", ("RL", "RR"), "1 + 2")]
        tags = []
        for p, (a, b), txt in splits:
            par = mt.rows[p]
            kid_top = max(mt.rows[a].get_top()[1], mt.rows[b].get_top()[1])
            y = (par.get_bottom()[1] + kid_top) / 2 - 0.06
            nudge = 0 if p == "root" else -0.2 * RIGHT + -0.1 * UP
            tags.append(T(txt, 28, GOLD).move_to([par.get_x(), y, 0]).shift(nudge))

        with self.say("c5.safe.1") as c:
            self.play(*appear(qt, qname), run_time=1.2)
            self.play(*appear(mt, labs, mname, lag=0.1), run_time=1.2)
            c.wait_until("halves")
            for k, ((p, (a, b), _), tg) in enumerate(zip(splits, tags)):
                anims = [mt.edges[a].animate.set_stroke(GOLD, 4), mt.edges[b].animate.set_stroke(GOLD, 4)]
                anims += appear(tg)
                if k == 0:
                    anims += set_alpha([qt, qname], 0.4)
                self.play(*anims, run_time=1.4 if k == 0 else 1.0)
                if k == 0:
                    self.wait(0.4)
            c.wait_until("shape")
            for vals, cue in ((RUNNING, None), (REVERSED, "the split"), (SORTED, "even when")):
                if cue:
                    c.wait_until(cue)
                new = strip_labels(merge_tree(vals))
                self.play(*swap(self.labs, new, shift=0.12 * UP), run_time=min(1.1, c.until(floor=0.3)))
                self.labs = new
                if cue is None:
                    self.wait(0.4)

    # c5.safe.2: the balanced tree for every input; ≤ n per level; 14 levels; the recurrence
    def levels(self):
        lt = level_tree(partial=False)
        tree, tags, brace = lt.tree, lt.tags, lt.brace
        log_n = MathTex(r"\log_2 n", font_size=40, color=GOLD).move_to(lt.logl, aligned_edge=RIGHT)
        eq = MathTex(r"T(n) = 2T(n/2) + n", font_size=48)
        always = T("always", 40, GREEN)
        VGroup(eq, always).arrange(RIGHT, buff=0.6).move_to([0, 3.2, 0])

        # Lecture 2's table
        TAB = 40
        lhs = [MathTex(s, font_size=TAB) for s in
               (r"T(n+1) = T(n) + 1", r"T(n+1) = T(n) + n", r"T(n) = T(n/2) + 1", r"T(n) = 2T(n/2) + n")]
        os_ = [MathTex(s, font_size=TAB) for s in ("O(n)", "O(n^2)", r"O(\log n)", r"O(n\log n)")]
        ty = [2.75, 1.95, 1.15, 0.35]
        lw = max(m.width for m in lhs)
        x0 = -(lw + 0.9 + max(m.width for m in os_)) / 2
        for m, o, y in zip(lhs, os_, ty):
            m.move_to([0, y, 0]).align_to([x0, 0, 0], LEFT)
            o.move_to([0, y, 0]).align_to([x0 + lw + 0.9, 0, 0], LEFT)
        eq_t = lhs[3]
        ms = T("merge sort: worst case", 40, GREEN).move_to([0, -0.85, 0])
        qs = T("quicksort: average case only", 32, DIM).move_to([0, -1.6, 0])
        ceil_ = MathTex(r"n \log_2 n \approx 133{,}000", font_size=48, color=GOLD)
        anyin = T("on any input", 34)
        VGroup(ceil_, anyin).arrange(RIGHT, buff=0.6).move_to([0, -2.85, 0])
        self.ceil_ = ceil_

        with self.say("c5.safe.2") as c:
            # each small tree leaves as one piece (its digits with its cells): left, then right
            olds = [m for m in self.mobjects if m.get_family() and any(x.has_points() for x in m.get_family())]
            self.remove(*[m for m in self.mobjects if m not in olds])
            left = [m for m in olds if m.get_x() < 0]
            right = [m for m in olds if m.get_x() >= 0]
            self.play(*[time_span(FadeOut(m), 0.0, 0.7) for m in left],
                      *[time_span(FadeOut(m), 0.2, 0.9) for m in right],
                      time_span(FadeIn(tree), 0.9, 1.8), run_time=1.8)
            c.wait_until("level")
            self.play(*flash(list(tree.rows[1])), run_time=1.5)
            c.wait_until(own_word=tags[0])
            self.play(*appear(*tags, lag=0.3), run_time=1.6)
            c.wait_until("levels")
            self.play(GrowFromCenter(brace), *appear(log_n), run_time=1.2)
            c.wait_until("thirteen point three")
            self.play(*swap(log_n, lt.logl), run_time=1.2)
            c.wait_until("fourteen levels")
            self.play(*appear(lt.lvl), run_time=1.0)
            c.wait_until("partly filled")
            self.play(*set_alpha(lt.empty, 0.15), run_time=min(1.2, c.until("recur", floor=0.6)))
            c.wait_until("recur")
            self.play(*appear(eq, always, lag=0.5), run_time=1.4)
            c.wait_until("table")
            sweep_clear(self, time_span(eq.animate.scale(TAB / 48).move_to(eq_t), 0.6, 1.3),
                        *[time_span(FadeIn(m, shift=0.4 * LEFT), 1.3 + 0.1 * i, 1.8 + 0.1 * i)
                          for i, m in enumerate(lhs[:3] + os_)],
                        keep=[eq], run_time=2.5)
            self.play(eq.animate.set_color(YELLOW), os_[3].animate.set_color(YELLOW), run_time=1.0)
            c.wait_until("worst")
            self.play(*appear(ms), run_time=1.0)
            c.wait_until("not just")
            self.play(*appear(qs), run_time=0.9)
            c.wait_until("ceiling")
            self.wait(1.0)
            self.play(*appear(ceil_), run_time=1.3)
            c.wait_until("come to")
            self.play(*appear(anyin), run_time=min(1.0, c.until(floor=0.3)))  # early: the ceiling's caption, read with it

    # c5.safe.3: measured on a 0 .. 140,000 line between floor and ceiling
    def measure(self):
        title = T("comparisons on 10,000 items", 36).move_to([0, 3.3, 0])
        line = Line([-6, Y0, 0], [6, Y0, 0]).set_stroke(GOLD, 6)
        zero = T("0", 28, DIM).move_to([-6, Y0 - 0.5, 0])
        top = T("140,000", 28, DIM).move_to([0, Y0 - 0.5, 0]).align_to([6.6, 0, 0], RIGHT)
        f_tick = vtick(118_458, Y0 - 0.15, Y0 + 1.15, GOLD, width=6)
        f_lab = label_left("lower bound ≈ 118,458", GOLD, 118_458, Y0 + 1.3)
        c_tick = vtick(133_000, Y0 - 0.15, Y0 + 2.0, GOLD, dashed=True, width=6)
        c_lab = T("≈ 133,000", 30, GOLD).move_to([xv(133_000), Y0 + 2.3, 0])
        r_tick = vtick(120_392, Y0, Y0 - 0.75, FG)
        r_lab = label_left("120,392 random", FG, 120_392, Y0 - 0.6)
        pct = label_left("+1.6%", GOLD, 118_458, Y0 + 0.62, size=34)
        s_tick = vtick(64_608, Y0, Y0 - 2.65, GREEN)
        s_lab = label_left("64,608 sorted", GREEN, 64_608, Y0 - 2.5)
        v_tick = vtick(69_008, Y0, Y0 - 2.65, GREEN)
        v_lab = label_right("69,008 reversed", GREEN, 69_008, Y0 - 2.5)
        w_tick = vtick(123_617, Y0, Y0 - 1.75, YELLOW)
        w_lab = label_left("123,617 worst input", YELLOW, 123_617, Y0 - 1.6)

        with self.say("c5.safe.3") as c:
            sweep_clear(self, *[time_span(a, 0.6, 1.4) for a in
                                [FadeIn(title), Create(line), FadeIn(zero), FadeIn(top)]], run_time=1.4)
            self.play(Create(f_tick), Create(c_tick), *appear(f_lab, c_lab), run_time=1.3)  # early: recap of the floor and the ceiling
            c.wait_until("random")
            self.play(Create(r_tick), *appear(r_lab), run_time=1.3)
            c.wait_until("floor")
            self.play(*appear(pct), FlashAround(f_tick, run_time=1.2, color=GOLD), run_time=1.2)
            c.wait_until("sorted")
            self.play(Create(s_tick), *appear(s_lab), run_time=1.2)
            c.wait_until("reversed input")
            self.play(Create(v_tick), *appear(v_lab), run_time=1.2)
            c.wait_until("worstin")
            self.play(Create(w_tick), *appear(w_lab), run_time=1.3)
            c.wait_until("Even that")
            self.play(*flash([w_lab, c_lab]), run_time=1.5)

    # c5.safe.4: the board; 1.4 s vs 0.53 s; safe but slower
    def board(self):
        sb = filled_board()
        sb.shift(UP * (3.55 - sb.get_top()[1]))
        q0, q1 = sb.cells[2][0], sb.cells[2][1]
        sb.cells[2].remove(q0, q1)
        v0 = T("120,392", 44, GOLD).move_to(q0)
        v1 = T("1.4 s", 44, GOLD).move_to(q1)
        ratio = MathTex(r"1.4 / 0.53 \approx 2.6", font_size=44, color=GOLD)
        ratio.move_to([q1.get_x(), sb.floor_label.get_y(), 0])
        cap = T("fewer comparisons, more time", 30, DIM).move_to([0, -3.25, 0])
        other = T("the rest of the work: List.length, take's copies", 30, DIM).move_to([0, -3.25, 0])
        p_ms = pill("merge sort: safe", GREEN, 32)
        p_qs = pill("quicksort: faster", GOLD, 32)
        VGroup(p_ms, p_qs).arrange(RIGHT, buff=1.0).move_to([0, -3.15, 0])

        with self.say("c5.safe.4") as c:
            sweep_clear(self, time_span(FadeIn(sb), 0.6, 1.3), time_span(FadeIn(q0), 0.6, 1.3), time_span(FadeIn(q1), 0.6, 1.3), run_time=1.3)  # early: the board is recalled whole
            self.play(*swap(q0, v0), run_time=min(1.2, c.until("secs", floor=0.6)))
            c.wait_until("secs")
            self.play(*swap(q1, v1), run_time=1.2)
            c.wait_until("compare")
            self.play(*flash([sb.cells[1][0], sb.cells[1][1], v0, v1]), run_time=1.5)
            c.wait_until("nearly three times")
            self.play(*appear(ratio, cap, lag=0.5), run_time=1.4)  # early: the ratio's caption, read with it
            c.wait_until("other")
            self.play(*swap(cap, other), run_time=1.2)
            c.wait_until("safe")
            self.play(*swap(other, VGroup(p_ms, p_qs)), run_time=1.4)
