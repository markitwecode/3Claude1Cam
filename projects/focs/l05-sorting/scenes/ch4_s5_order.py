"""Chapter 4, scene 5: quik builds its answer from the right. Clips c4.order.1 – c4.order.4.

Layout: c4.order.1 the combine line large (y 1.0) with its numbered boxes, a GOLD right-to-left
arrow and caption below. c4.order.2/3: the line small at the top, ch3's call tree (list nodes) in
the left two-thirds, the answer row `sorted` at the right (right-anchored at its []), the current
call in a bottom band. c4.order.4: the tree clears, the row grows to centre-left, "1 cons" over
each cell, "nothing appended", L3's card piles as a DIM inset at the right.
Exports `answer_row()` (GREEN cells 3 4 5 7 9, TEAL [], GOLD right-to-left arrow) for the recap.
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

COMBINE = "| l, r, [] -> quik (l, a :: quik (r, sorted))"
SIDE_ = 0.62          # answer-cell side (small row)
PITCH = 0.76          # answer-cell pitch


def combine_code(size=34):
    """The combine line of quik, styled as in scene 4 (quik YELLOW, [] :: TEAL)."""
    try:
        from lib.paths import load_scene
        return load_scene("ch4_s4_quik").ocode(COMBINE, size)
    except Exception:
        pass
    code = Code(COMBINE, size=size)
    for k in range(2):
        code.find("quik", nth=k).set_color(YELLOW)
    return code


def answer_row():
    """The finished answer row: GREEN cells 3 4 5 7 9, then a TEAL [], with a GOLD arrow under it
    pointing right to left (built from the largest end). Centred on ORIGIN.
    .cells: {value: cell} · .order: cells left to right · .nil · .arrow"""
    vals = [3, 4, 5, 7, 9]
    cells = []
    for i, v in enumerate(vals):
        box = Square(SIDE_, stroke_color=GREEN, stroke_width=3)
        cell = VGroup(box, Mono(str(v), 32).move_to(box)).move_to(RIGHT * PITCH * i)
        cells.append(cell)
    nil = Nil(size=34)
    nil.next_to(cells[-1], RIGHT, buff=0.18)
    row = VGroup(*cells, nil)
    arrow = Arrow(row.get_right() + DOWN * 0.62, row.get_left() + DOWN * 0.62, buff=0,
                  color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.08)
    g = VGroup(row, arrow).move_to(ORIGIN)
    g.cells = dict(zip(vals, cells))
    g.order = cells
    g.nil = nil
    g.arrow = arrow
    return g


# ── the call tree: ch3's call_tree(), list nodes ─────────────────────────────
KEYS = {"root": [3, 5, 9, 4, 7], "R": [7, 4, 9, 5], "RL": [5, 4], "RR": [9], "RLL": [4]}


def order_tree():
    """ch3 s6's call tree of the running list (list nodes, pivots YELLOW, no badges), without
    the empty calls under the one-item leaves. .n: {key: TreeNode}"""
    from lib.paths import load_scene
    tree = load_scene("ch3_s6_trace").call_tree(badges=False, size=34, gap=1.5)
    for nd in list(tree.nodes):
        if nd.is_empty and nd.parent is not None and len(nd.parent.values) == 1:
            tree.remove(nd.body, nd.edge)
    tree.n = {k: tree.node(v) for k, v in KEYS.items()}
    tree.n["L"] = tree.n["root"].left
    tree.n["RLR"] = tree.n["RL"].right
    tree.place(0.95, np.array([-2.4, 2.4, 0]))
    return tree


def tree_node(tree, key):
    return tree.n[key].body


def tree_digit(tree, key, v):
    nd = tree.n[key]
    return nd.item(nd.values.index(v))


def call_line(call, result=None):
    """The current call in the bottom band, optionally with ⇒ result (GREEN)."""
    parts = [Mono(call, 30)]
    if result is not None:
        parts += [MathTex(r"\Rightarrow", font_size=40), Mono(result, 30, color=GREEN)]
    g = VGroup(*parts).arrange(RIGHT, buff=0.3).move_to(DOWN * 3.3)
    return g


def cons_in(src_digit, cell, arc=-PI / 2):
    """The pivot digit flies from its tree node into its answer cell; the cell's box fades in."""
    return [*fly(src_digit, cell[1], arc=arc), *during([FadeIn(cell[0])], 0.6, 1)]


def over_top(scene, src, cell, run_time=1.5, lift=2.95):
    """The root's pivot climbs out of its node, crosses above the tree and drops into its cell
    (the straight or arced path would cross the other nodes). Plays it."""
    digit = cell[1]
    copy = src.copy()
    a, b = src.get_center(), digit.get_center()
    path = VMobject().set_points_smoothly([a, np.array([a[0], lift, 0]),
                                          np.array([(a[0] + b[0]) / 2, lift + 0.1, 0]),
                                          np.array([b[0], lift, 0]), b])
    c0, c1 = color_to_rgb(src.get_color()), color_to_rgb(digit.get_color())

    def step(m, t):
        m.move_to(path.point_from_proportion(t))
        m.set_color(rgb_to_color((1 - t) * c0 + t * c1))
        m.set_opacity(min(1.0, 4 * t))

    scene.play(UpdateFromAlphaFunc(copy, step, rate_func=smooth),
               *during([FadeIn(cell[0])], 0.6, 1), run_time=run_time)
    scene.remove(copy)
    scene.add(digit)


def node_box(m):
    return SurroundingRectangle(m, color=YELLOW, buff=0.14, stroke_width=2).set_fill(
        YELLOW, opacity=0.15).set_z_index(-1)


class Order(NarratedScene):
    def construct(self):
        self.combine()
        self.tree_walk()
        self.left_part()
        self.once()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── c4.order.1: the combine line, numbered ────────────────────────────────
    def combine(self):
        code = combine_code(34).move_to(UP * 1.0)
        self.code = code
        b1 = token_box(code.find("quik (r, sorted)"), code, height=0.62)
        b2 = token_box(code.find("a ::"), code, height=0.62)
        b3 = token_box(code.find("quik (l,"), code, height=0.62)
        nums = [T(str(k), 40, color=GOLD).next_to(b, DOWN, buff=0.2) for k, b in
                zip((1, 2, 3), (b1, b2, b3))]
        y = nums[0].get_bottom()[1] - 0.45
        arrow = Arrow(np.array([code.get_right()[0], y, 0]), np.array([code.get_left()[0], y, 0]),
                      buff=0, color=GOLD, stroke_width=5, max_tip_length_to_length_ratio=0.05)
        cap = T("built from the largest end", 36, color=GOLD).next_to(arrow, DOWN, buff=0.35)
        self.c1 = [b1, b2, b3, *nums, arrow, cap]
        with self.say("c4.order.1") as c:
            self.play(FadeIn(code, shift=0.2 * DOWN), run_time=1.0)
            for cue, b, n in (("first", b1, nums[0]), ("then", b2, nums[1]), ("last", b3, nums[2])):
                c.wait_until(cue)
                self.play(FadeIn(b), *appear(n), run_time=1.2)
            c.wait_until("right")
            self.play(GrowArrow(arrow), run_time=1.3)
            self.play(*appear(cap), run_time=1.0)  # early: names the arrow just drawn ("from the right")

    # ── c4.order.2: the tree, the right part first ────────────────────────────
    def tree_walk(self):
        code = self.code
        tree = order_tree()
        self.tree = tree
        row = answer_row()
        row.shift(RIGHT * (5.8 - row.nil.get_right()[0]) + UP * (0.3 - row.nil.get_y()))
        self.row = row
        lab = Mono("sorted", 30, color=FG).next_to(row[0], UP, buff=0.45)
        self.lab = lab
        N = lambda k: tree_node(tree, k)  # noqa: E731
        with self.say("c4.order.2") as c:
            c.wait_until("tree of calls")
            self.play(*during(disappear(*self.c1), 0, 0.45),
                      *during([code.animate.scale(0.82).move_to(UP * 3.45)], 0.2, 0.8),
                      *during([FadeIn(tree)], 0.5, 1), run_time=2.0)
            c.wait_until("root")
            box = node_box(N("root"))
            self.box = box
            self.play(FadeIn(box), *flash([tree_digit(tree, "root", 3)]), run_time=1.2)
            c.wait_until("sends everything right")
            self.play(FlashAround(N("L"), color=YELLOW), FlashAround(N("R"), color=YELLOW),
                      run_time=1.2)
            c.wait_until("first we sort")
            call = call_line("quik ([7; 4; 9; 5], [])")
            self.call = call
            self.play(Transform(box, node_box(N("R"))), *appear(call), run_time=1.3)
            c.wait_until("sorted empty")
            self.play(*appear(lab, row.nil), run_time=1.0)

            c.wait_until("seven")
            self.play(FlashAround(tree_digit(tree, "R", 7), color=YELLOW, run_time=1.2))
            c.wait_until("on the left")
            self.play(FlashAround(N("RL"), color=YELLOW), run_time=1.1)
            c.wait_until("on the right")
            self.play(FlashAround(N("RR"), color=YELLOW), run_time=1.1)

            c.wait_until("nine")
            new = call_line("quik ([9], [])")
            self.play(Transform(box, node_box(N("RR"))), *swap(call, new), run_time=1.3)
            call = new
            c.wait_until("consed onto")
            res = call_line("quik ([9], [])", "[9]")
            self.play(*cons_in(tree_digit(tree, "RR", 9), row.cells[9]),
                      *during(appear(*res[1:], shift=None), 0.5, 1), run_time=1.6)
            self.remove(call)
            self.add(res)
            call = res

            c.wait_until("cons7")
            self.play(Transform(box, node_box(N("R"))), *set_alpha([call], 0.35), run_time=1.0)
            over_top(self, tree_digit(tree, "R", 7), row.cells[7], run_time=1.5, lift=1.75)
            c.wait_until("seven nine")
            self.play(*flash([row.cells[7], row.cells[9]], color=GREEN), run_time=1.2)
            self.call = call

    # ── c4.order.3: the left part, then the root ──────────────────────────────
    def left_part(self):
        tree, row, box = self.tree, self.row, self.box
        N = lambda k: tree_node(tree, k)  # noqa: E731
        with self.say("c4.order.3") as c:
            new = call_line("quik ([5; 4], [7; 9])")
            self.play(Transform(box, node_box(N("RL"))), *swap(self.call, new), run_time=1.4)
            call = new
            c.wait_until("pivot5")
            self.play(FlashAround(tree_digit(tree, "RL", 5), color=YELLOW, run_time=1.2))
            c.wait_until("four on the left")
            self.play(FlashAround(N("RLL"), color=YELLOW), run_time=1.0)
            c.wait_until("nothing on the right")
            self.play(FlashAround(N("RLR"), color=YELLOW), run_time=1.0)

            c.wait_until("cons5")
            self.play(*cons_in(tree_digit(tree, "RL", 5), row.cells[5]), run_time=c.until("cons4", 0.6))
            c.wait_until("cons4")
            new = call_line("quik ([4], [5; 7; 9])", "[4; 5; 7; 9]")
            self.play(Transform(box, node_box(N("RLL"))), *swap(call, new[0]), run_time=0.9)
            call = new
            self.play(*cons_in(tree_digit(tree, "RLL", 4), row.cells[4]), run_time=1.2)
            c.wait_until("four five seven nine")
            self.play(*appear(*new[1:], shift=None), run_time=1.0)
            self.remove(new[0])
            self.add(new)

            c.wait_until("cons3")
            self.play(Transform(box, node_box(N("root"))), run_time=1.0)
            c.wait_until("three goes on")
            over_top(self, tree_digit(tree, "root", 3), row.cells[3], run_time=1.5)
            c.wait_until("left part is empty")
            new = call_line("quik ([], [3; 4; 5; 7; 9])", "[3; 4; 5; 7; 9]")
            self.play(Transform(box, node_box(N("L"))), *swap(call, new[0]), run_time=1.3)
            call = new
            c.wait_until("three four five")
            tick = check_mark().next_to(row[0], RIGHT, buff=0.3)
            self.tick = tick
            self.play(*appear(*new[1:], shift=None), *appear(tick, shift=None), run_time=1.0)
            self.remove(new[0])
            self.add(new)
            self.call = new
            settle(self, row[0], add=[tick])
            self.play(*flash([row[0]], color=GREEN), run_time=1.4)

    # ── c4.order.4: one cons each, nothing appended, the card piles ───────────
    def once(self):
        row, tick = self.row, self.tick
        with self.say("c4.order.4") as c:
            self.play(*during(disappear(self.tree, self.box, self.lab, self.call), 0, 0.45),
                      *during([row[0].animate.scale(1.7).move_to(LEFT * 2.3 + UP * 0.4)], 0.4, 1),
                      run_time=1.3)
            labs = {}
            for v, cue in ((9, None), (7, "seven"), (5, "five"), (4, "four"), (3, "three")):
                if cue:
                    c.wait_until(cue)
                cell = row.cells[v]
                labs[v] = T("1 cons", 28, color=GOLD).next_to(cell, UP, buff=0.25)
                self.play(FlashAround(cell, color=GREEN), *appear(labs[v]), run_time=0.8)  # early: the count names the cons just flashed
            arrow = row.arrow
            span = VGroup(*row.order, row.nil)
            arrow.become(Arrow(span.get_right() + DOWN * 1.0, span.get_left() + DOWN * 1.0,
                               buff=0, color=GOLD, stroke_width=5,
                               max_tip_length_to_length_ratio=0.06))
            c.wait_until("from the right")
            self.play(GrowArrow(arrow), run_time=1.2)
            c.wait_until("noapp")
            noapp = T("nothing appended", 36, color=GREEN).next_to(arrow, DOWN, buff=0.4)
            self.play(*appear(noapp), run_time=1.0)

            c.wait_until("cards")
            step = 0.65
            srcb = np.array([4.35, -1.6, 0])
            dstb = np.array([5.85, -1.6, 0])
            cards = {}
            for k, v in enumerate((3, 4, 5, 7, 9)):          # 9 on top of the old pile
                cards[v] = inset_card(v).move_to(srcb + UP * step * k)
            out = dim_outline().scale(0.7).move_to(dstb)
            title = Mono("rev_app", 28, color=DIM).next_to(VGroup(*cards.values(), out), UP, buff=0.35)
            frame = SurroundingRectangle(VGroup(title, *cards.values(), out), buff=0.3,
                                         corner_radius=0.2, color=DIM, stroke_width=2)
            inset = [frame, *cards.values(), out]
            self.play(*[FadeIn(m) for m in inset], *appear(title, shift=None), run_time=0.7)
            left = c.until(floor=1.5) - 0.05
            rts = [x * left / 5.4 for x in (1.4, 1, 1, 1, 1)]
            for k, v in enumerate((9, 7, 5, 4, 3)):
                anims = [cards[v].animate(path_arc=-PI / 2).move_to(dstb + UP * step * k)]
                if k == 0:
                    anims.append(FadeOut(out))
                self.play(*anims, run_time=rts[k])


# ── L3 ch4 s7's cards, DIM ────────────────────────────────────────────────────
CARD_W_, CARD_H_, SLOT_ = 1.4, 0.8, 0.92


def inset_card(v):
    """A card of scene 4's rev_app inset (L3 ch4 s7's cards, dimmed)."""
    try:
        from lib.paths import load_scene
        return load_scene("ch4_s4_quik")._card(v)
    except Exception:
        return dim_card(v).scale(0.7)


def dim_card(v):
    box = RoundedRectangle(width=CARD_W_, height=CARD_H_, corner_radius=0.12, stroke_color=DIM,
                           stroke_width=3, fill_color=BG, fill_opacity=1)
    return VGroup(box, value_label(v, color=DIM).move_to(box))


def dim_outline():
    return DashedVMobject(RoundedRectangle(width=CARD_W_, height=CARD_H_, corner_radius=0.12,
                                           stroke_color=DIM, stroke_width=3), num_dashes=22)
