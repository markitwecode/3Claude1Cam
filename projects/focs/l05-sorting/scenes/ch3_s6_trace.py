"""Chapter 3, scene 6: watching quick run on [3; 5; 9; 4; 7]. Clips c3.trace.1 – c3.trace.5.

Exports `call_tree(values, form="lists"|"circles", ...)`: the call tree of `quick` (partition
builds both parts backwards, `x <= p` goes left), see its docstring. Also `list_text`,
`list_item`, `even_split()` (the small even split of [5; 3; 9; 4; 7]).
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

RUNNING = [3, 5, 9, 4, 7]


# ---------------------------------------------------------------- exported helpers
def list_text(values, size=32, color=FG):
    """OCaml list literal "[3; 5; 9]" in Mono; the empty list "[]" in TEAL."""
    if not values:
        return Mono("[]", size=size, color=TEAL)
    return Mono("[" + "; ".join(str(v) for v in values) + "]", size=size, color=color)


def list_item(text, values, i):
    """VGroup of the glyphs of item i in a list_text(values) (Text has no space glyphs)."""
    k = 1
    for v in values[:i]:
        k += len(str(v)) + 1
    return VGroup(*text.submobjects[k:k + len(str(values[i]))])


def _partition(p, xs):
    left, right = [], []
    for x in xs:
        if x <= p:
            left = [x] + left
        else:
            right = [x] + right
    return left, right


class TreeNode(VGroup):
    """One call of quick. .values .pivot (None if empty) .level .left .right .parent
    .comparisons .body (list text, or VGroup(circle, digit)) .badge (or None)
    .edge (Line from the parent, or None) .stubs {"left"/"right": Line} (circles form)
    .item(i) glyphs of value i (list form) .pivot_glyph .point (layout point, unscaled)."""

    def __init__(self, values, depth, rank_x, pivot_rank):
        super().__init__()
        self.values = list(values)
        self.pivot = values[0] if values else None
        self.level = depth
        self.rank_x = rank_x
        self.pivot_rank = pivot_rank
        self.left = self.right = self.parent = None
        self.comparisons = max(len(values) - 1, 0)
        self.body = self.badge = self.edge = None
        self.stubs = {}
        self.pivot_glyph = None

    def item(self, i):
        return list_item(self.body, self.values, i)

    @property
    def is_empty(self):
        return not self.values


class CallTree(VGroup):
    """VGroup(edges..., stubs..., bodies..., badges...). .root .nodes (preorder) .edges .stubs
    .badges .total (all comparisons) .node(values) .origin (layout origin, follows place())."""

    def node(self, values):
        for n in self.nodes:
            if n.values == list(values):
                return n
        raise KeyError(values)

    def place(self, scale=1.0, point=ORIGIN):
        """Scale about the layout origin, then move the origin (the root's row, rank centre) to point."""
        self.scale(scale, about_point=self.origin)
        self.shift(np.array(point, dtype=float) - self.origin)
        self.origin = np.array(point, dtype=float)
        return self


def call_tree(values=RUNNING, form="lists", size=32, pitch=1.6, gap=1.4, badges=True,
              pivot_color=YELLOW, empties=True, stubs=True, radius=0.38, color=BLUE,
              edge_color=DIM, max_depth=None, leaf_size=1):
    """The call tree of quick on `values`, built at the layout origin (root row y = 0, x = 0 at
    the centre of the sorted ranks); move it with `.place(scale, point)`.

    form="lists": each node is list_text(its list), pivot glyph in `pivot_color` (None: FG),
      x = centre of its rank span; empty calls are TEAL "[]" nodes (empties=False drops them);
      badges=True adds a GOLD ring with its comparison count (len - 1, leaves 0) right of it.
    form="circles": only the pivots, as BLUE-ringed digits (radius, color) at x = their rank
      (a binary search tree); stubs=True draws a short DIM line toward each empty child
      (node.stubs["left"/"right"]), e.g. the root's empty left branch for the sorted inputs.
    pitch: x units per rank; gap: y units per level; max_depth: cut the tree below that depth;
    leaf_size: lists this short are leaves (default 1: [4] has no [] children drawn).
    """
    values = list(values)
    n = len(values)
    nodes = []

    def build(xs, start, depth, parent):
        if not xs:
            node = TreeNode([], depth, start - 0.5, start - 0.5)
        else:
            left, right = _partition(xs[0], xs[1:])
            k = start + len(left)
            node = TreeNode(xs, depth, start + (len(xs) - 1) / 2, k)
        node.parent = parent
        nodes.append(node)
        if len(xs) > leaf_size and (max_depth is None or depth < max_depth):
            node.left = build(left, start, depth + 1, node)
            node.right = build(right, k + 1, depth + 1, node)
        return node

    root = build(values, 0, 0, None)
    centre = (n - 1) / 2

    def pos(node):
        x = node.rank_x if form == "lists" else node.pivot_rank
        return np.array([(x - centre) * pitch, -node.level * gap, 0.0])

    tree = CallTree()
    tree.root, tree.origin = root, np.array(ORIGIN, dtype=float)
    shown = [nd for nd in nodes if not (nd.is_empty and (form == "circles" or not empties))]
    tree.nodes = shown
    tree.total = sum(nd.comparisons for nd in nodes)
    for nd in nodes:
        nd.point = pos(nd)
    for nd in shown:
        if form == "lists":
            nd.body = list_text(nd.values, size=size).move_to(nd.point)
            if nd.values:
                nd.pivot_glyph = nd.item(0)
                if pivot_color is not None:
                    nd.pivot_glyph.set_color(pivot_color)
            if badges:
                ring = Circle(radius=0.27 * size / 32).set_stroke(GOLD, 2.5)
                num = T(str(nd.comparisons), size=34 * size / 32, color=GOLD).move_to(ring)
                nd.badge = VGroup(ring, num).next_to(nd.body, RIGHT, buff=0.15)
                nd.badge.num = num
        else:
            ring = Circle(radius=radius).set_stroke(color, 3).set_fill(BG, 1)
            digit = Mono(str(nd.pivot), size=size * 1.15).move_to(ring)
            nd.body = VGroup(ring, digit).move_to(nd.point)
            nd.pivot_glyph = digit
        nd.add(nd.body)
    tree.edges, tree.stubs, tree.badges = [], [], []
    for nd in shown:
        if nd.parent is None or nd.parent not in shown:
            continue
        p = nd.parent
        if form == "lists":
            a = p.body.get_bottom() + 0.1 * DOWN
            b = nd.body.get_top() + 0.1 * UP
            nd.edge = Line(a, b).set_stroke(edge_color, 2.5)
        else:
            nd.edge = Line(p.point, nd.point, buff=radius).set_stroke(edge_color, 3)
        tree.edges.append(nd.edge)
    if form == "circles" and stubs:
        for nd in shown:
            for side in ("left", "right"):
                ch = getattr(nd, side)
                if ch is not None and ch.is_empty:
                    d = ch.point - nd.point
                    end = nd.point + 0.55 * d
                    st = Line(nd.point, end, buff=0).set_stroke(edge_color, 3)
                    st.put_start_and_end_on(nd.point + radius * d / np.linalg.norm(d), end)
                    nd.stubs[side] = st
                    tree.stubs.append(st)
    tree.add(*tree.edges, *tree.stubs, *[nd.body for nd in shown])
    for nd in shown:
        if nd.badge is not None:
            tree.badges.append(nd.badge)
    tree.add(*tree.badges)
    return tree


def even_split(scale=0.67):
    """The even first split of [5; 3; 9; 4; 7]: YELLOW pivot cell 5 lifted, below it the row
    "≤ 5" 3 -> 4 -> [] and the row "> 5" 9 -> 7 -> [] (ConsChains). .pivot .left .right .lab_l .lab_r"""
    piv = ConsCell(5, color=YELLOW).scale(scale)
    left = ConsChain([3, 4]).scale(scale)
    right = ConsChain([9, 7]).scale(scale)
    lab_l = T("≤ 5", size=32)
    lab_r = T("> 5", size=32)
    rows = VGroup(VGroup(lab_l, left), VGroup(lab_r, right))
    for row in rows:
        row[0].next_to(row[1], LEFT, buff=0.35)
    rows.arrange(DOWN, buff=0.35, aligned_edge=RIGHT)
    piv.next_to(rows, UP, buff=0.4).align_to(left, LEFT)
    g = VGroup(piv, lab_l, lab_r, left, right)
    g.pivot, g.left, g.right, g.lab_l, g.lab_r = piv, left, right, lab_l, lab_r
    return g


# ---------------------------------------------------------------- scene helpers
def _travel(m, dst, color=None, a=0.1, b=0.7, fade_end=0.8):
    """m moves to dst's centre in [a, b] of the play (optionally recolouring), then fades out
    by fade_end; one animation, so the move and the fade don't fight over m."""
    start, end = m.get_center(), dst.get_center()
    src = m.copy()
    col = color

    def upd(mob, t):
        mob.become(src)
        p = smooth(min(max((t - a) / (b - a), 0), 1))
        mob.move_to(start + (end - start) * p)
        if col is not None:
            mob.set_color(interpolate_color(ManimColor(src.get_color()), ManimColor(col), p))
        if t > b:
            mob.set_opacity(max(0.0, 1 - (t - b) / (fade_end - b)))
    return UpdateFromAlphaFunc(m, upd, remover=True)


def step_line(lhs, rhs, size=28, two_lines=False):
    a = Code(lhs, size=size)
    arr = MathTex(r"\Rightarrow", font_size=44, color=DIM)
    b = Code(rhs, size=size)
    if not two_lines:
        g = VGroup(a, arr, b).arrange(RIGHT, buff=0.25)
    else:
        g = VGroup(a, VGroup(arr, b).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.22)
    g.rhs = b
    return g


ROOT0 = np.array([0.0, 2.15, 0.0])
STEP_Y = -3.05
CHAIN_Y = 3.2
ROOT1 = np.array([-2.7, 1.3, 0.0])     # clip 4: tree shrunk to the left
K1 = 0.88
ROOT2 = np.array([-2.7, 1.6, 0.0])     # clip 5: circles
COL_X = 3.95
COL_L = 1.5


class Ch3S6Trace(NarratedScene):
    def construct(self):
        self.tree = call_tree(RUNNING, pivot_color=None, gap=1.45).place(1.0, ROOT0)
        self.cur = {}
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # helpers
    def fly_item(self, src_node, val, dst_node, arc=None):
        g = src_node.item(src_node.values.index(val))[0]
        dst = dst_node.item(dst_node.values.index(val))[0].copy()
        return fly(g, dst, arc=arc), dst

    def complete(self, node, placed):
        """Swap the flown digit copies for the node's own text, then fade in its punctuation."""
        for d in placed:
            self.remove(d)
        digits = []
        for i in range(len(node.values)):
            digits += list(node.item(i))
        rest = [g for g in node.body if g not in digits]
        for g in rest:
            g.set_opacity(0)
        self.add(node.body)
        return [g.animate.set_opacity(1) for g in rest]

    def clip1(self):
        t = self.tree
        root = t.root
        rc = root.right
        with self.say("c3.trace.1") as c:
            self.chain = ConsChain(RUNNING).scale(0.7).move_to([0, CHAIN_Y, 0])
            self.play(FadeIn(self.chain), run_time=1.0)
            c.wait_until("three")
            self.play(*appear(root.body), run_time=1.0)
            c.wait_until("p1")
            self.play(*recolor(root.pivot_glyph, YELLOW), FlashAround(root.pivot_glyph, run_time=1.2),
                      run_time=1.2)
            c.wait_until("all")
            self.play(Create(rc.edge), run_time=0.8)
            anims, placed = [], []
            for i, v in enumerate([5, 9, 4, 7]):
                a, d = self.fly_item(root, v, rc)
                anims += during(a, 0.22 * i, 0.22 * i + 0.34)
                placed.append(d)
            self.play(*anims, run_time=min(3.0, c.until("first") - 0.1))
            c.wait_until("first")
            lc = root.left
            self.play(Create(lc.edge), *appear(lc.body), *self.complete(rc, placed), run_time=1.2)
            c.wait_until("built backwards")
            self.step = step_line("quick [3; 5; 9; 4; 7]", "(quick []) @ (3 :: quick [7; 4; 9; 5])",
                                   two_lines=True)
            self.step.move_to([0, STEP_Y - 0.05, 0])
            self.play(*appear(self.step), run_time=1.0)
            c.wait_until("c1")
            self.play(*appear(root.badge, shift=None), FlashAround(root.badge, color=GOLD), run_time=1.0)

    def clip2(self):
        t = self.tree
        root = t.root
        rc = root.right
        lc = root.left
        n54, n9 = rc.left, rc.right
        n4, ne = n54.left, n54.right
        with self.say("c3.trace.2") as c:
            self.eq_nil = Mono("= []", size=30, color=GREEN).next_to(lc.body, DOWN, buff=0.3)
            self.play(*recolor(lc.body, GREEN), FlashUnder(self.step.rhs.find("(quick [])")),
                      run_time=0.8)
            self.play(*appear(self.eq_nil, shift=None), run_time=0.8)
            c.wait_until("on the right")
            self.play(*recolor(rc.pivot_glyph, YELLOW), FlashAround(rc.pivot_glyph), run_time=1.0)
            c.wait_until("split2")
            a, d4 = self.fly_item(rc, 4, n54)
            self.play(Create(n54.edge), Create(n9.edge), run_time=0.6)
            self.play(*a, run_time=0.8)
            c.wait_until("nine goes right")
            a, d9 = self.fly_item(rc, 9, n9, arc=-0.9)
            self.play(*a, run_time=0.8)
            c.wait_until("five goes left")
            a, d5 = self.fly_item(rc, 5, n54, arc=1.2)
            self.play(*a, run_time=0.8)
            c.wait_until("c2")
            self.play(*self.complete(n54, [d4, d5]), *self.complete(n9, [d9]),
                      *appear(rc.badge, shift=None), run_time=1.0)
            c.wait_until("p3")
            self.play(*recolor(n54.pivot_glyph, YELLOW), FlashAround(n54.pivot_glyph), run_time=1.0)
            c.wait_until("and the four goes left")
            a, d4b = self.fly_item(n54, 4, n4)
            self.play(Create(n4.edge), Create(ne.edge), run_time=0.5)
            self.play(*a, run_time=0.8)
            c.wait_until("c3")
            self.play(*self.complete(n4, [d4b]), *appear(ne.body, shift=None),
                      *appear(n54.badge, shift=None), run_time=1.0)
            c.wait_until("leaves")
            leaves = [lc, n4, ne, n9]
            self.play(*appear(*[lf.badge for lf in leaves], shift=None, lag=0.2), run_time=1.2)
            self.tag = T("one item or none: no comparisons", size=32, color=DIM).move_to([0, STEP_Y, 0])
            c.wait_until(own_word=self.tag)
            self.play(*swap(self.step, self.tag), run_time=1.2)

    def assemble(self, node, left_m, right_m, result_vals):
        """node's body gives way to its GREEN result, born from the children's results + pivot."""
        res = list_text(result_vals, color=GREEN).move_to(node.body)
        old = self.cur.get(node, node.body)
        lc, pc, rc = left_m.copy(), node.pivot_glyph.copy(), right_m.copy()
        row = VGroup(lc.copy(), pc.copy(), rc.copy()).arrange(RIGHT, buff=0.12).move_to(res)
        anims = during([FadeOut(old)], 0, 0.3)
        anims += [_travel(lc, row[0]), _travel(pc, row[1], GREEN), _travel(rc, row[2])]
        anims += during([FadeIn(res)], 0.8, 1.0)
        self.add(lc, pc, rc)
        self.play(*anims, run_time=1.8)
        self.cur[node] = res
        return res

    def clip3(self):
        t = self.tree
        root = t.root
        rc, lc = root.right, root.left
        n54, n9 = rc.left, rc.right
        n4, ne = n54.left, n54.right
        with self.say("c3.trace.3") as c:
            c.wait_until("up")
            self.play(*recolor(n4.body, GREEN), *recolor(ne.body, GREEN), *recolor(n9.body, GREEN),
                      run_time=1.0)
            c.wait_until("a1")
            s1 = step_line("[4] @ (5 :: [])", "[4; 5]", size=32).move_to([0, STEP_Y, 0])
            self.play(*swap(self.tag, s1), run_time=1.2)
            r54 = self.assemble(n54, n4.body, ne.body, [4, 5])
            c.wait_until("a2")
            s2 = step_line("[4; 5] @ (7 :: [9])", "[4; 5; 7; 9]", size=32).move_to([0, STEP_Y, 0])
            self.play(*swap(s1, s2), run_time=1.2)
            r7 = self.assemble(rc, r54, n9.body, [4, 5, 7, 9])
            c.wait_until("a3")
            s3 = step_line("[] @ (3 :: [4; 5; 7; 9])", "[3; 4; 5; 7; 9]", size=32).move_to([0, STEP_Y, 0])
            self.play(*swap(s2, s3), run_time=1.2)
            rr = self.assemble(root, lc.body, r7, [3, 4, 5, 7, 9])
            c.wait_until("result")
            done = ConsChain([3, 4, 5, 7, 9]).scale(0.7).move_to([0, CHAIN_Y, 0])
            tick = check_mark(GREEN).scale(0.6).next_to(done, RIGHT, buff=0.2)
            self.done = VGroup(done, tick)
            self.reply = Code("- : int list = [3; 4; 5; 7; 9]", size=32).move_to([0, STEP_Y, 0])
            self.play(*swap(self.chain, self.done), FlashAround(rr, color=GREEN, run_time=1.6),
                      *during(swap(s3, self.reply), 0.3, 1.0), run_time=1.6)

    def clip4(self):
        t = self.tree
        root = t.root
        rc = root.right
        n54 = rc.left
        with self.say("c3.trace.4") as c:
            parts = list(t.edges) + [self.cur.get(nd, nd.body) for nd in t.nodes] + list(t.badges) + [self.eq_nil]
            self.G = VGroup(*parts)
            self.remove(*parts)
            self.add(self.G)
            self.play(*during(disappear(self.done, self.reply), 0, 0.25),
                      *during([self.G.animate.scale(K1, about_point=ROOT0).shift(ROOT1 - ROOT0)], 0.25, 1.0),
                      run_time=1.5)
            n4_, p1, n3_, p2, n1_, eq, n8 = [T(s, size=56, color=GOLD) for s in
                                             ("4", "+", "3", "+", "1", "=", "8")]
            self.sum = VGroup(n4_, p1, n3_, p2, n1_, eq, n8).arrange(RIGHT, buff=0.25)
            self.sum.move_to([COL_X, 2.6, 0]).align_to([COL_L, 0, 0], LEFT)
            c.wait_until("four plus three")
            b4, b3, b1 = root.badge.num, rc.badge.num, n54.badge.num
            anims = during(fly(b4, n4_, arc=-0.4), 0.0, 0.4)
            anims += during(appear(p1, shift=None), 0.3, 0.45)
            anims += during(fly(b3, n3_, arc=-0.4), 0.3, 0.7)
            anims += during(appear(p2, shift=None), 0.6, 0.75)
            anims += during(fly(b1, n1_, arc=-0.4), 0.6, 1.0)
            self.play(*anims, run_time=min(3.0, c.until("makes eight")))
            c.wait_until("makes eight")
            self.play(*appear(eq, n8, shift=None, lag=0.3), run_time=1.0)
            self.play(FlashAround(n8, color=GOLD), run_time=0.8)
            r7 = VGroup(T("7", size=48, color=GOLD), T("floor for five items", size=30))
            r7.arrange(RIGHT, buff=0.35).next_to(self.sum, DOWN, buff=0.55).align_to(self.sum, LEFT)
            r6 = VGroup(T("6", size=48, color=GOLD), T("insertion sort (Part 2)", size=30))
            r6.arrange(RIGHT, buff=0.35).next_to(r7, DOWN, buff=0.35).align_to(self.sum, LEFT)
            self.r7, self.r6 = r7, r6
            c.wait_until(own_word=r7[1])
            self.play(*appear(r7), run_time=1.0)
            c.wait_until(own_word=r6[1])
            self.play(*appear(r6), run_time=1.0)
            c.wait_until("even")
            ev = even_split().move_to([COL_X, -1.35, 0])
            six = T("6", size=48, color=GOLD).next_to(ev.pivot, RIGHT, buff=0.6)
            self.ev, self.six = ev, six
            self.play(FadeIn(ev), run_time=1.2)  # early: the split picture is shown whole
            self.play(*appear(six), run_time=0.8)

    def clip5(self):
        t = self.tree
        root = t.root
        ct = call_tree(RUNNING, form="circles", radius=0.42).place(1.0, ROOT2)
        self.ct = ct
        with self.say("c3.trace.5") as c:
            # break the shrunk tree into top-level pieces: pivots kept, the rest leaves
            self.remove(self.G)
            keep, rest = {}, []
            for nd in t.nodes:
                m = self.cur.get(nd, nd.body)
                if nd.is_empty:
                    rest.append(m)
                    continue
                vals = sorted(nd.values) if nd in self.cur else nd.values
                idx = vals.index(nd.pivot)
                k = 1 + sum(len(str(v)) + 1 for v in vals[:idx])
                pg = m.submobjects[k].copy()
                others = VGroup(*[g.copy() for j, g in enumerate(m.submobjects) if j != k])
                pg.set_z_index(3)
                keep[nd] = pg
                rest.append(others)
            loose = list(t.edges) + list(t.badges) + [self.eq_nil]
            self.add(*loose, *rest, *keep.values())
            gone = loose + rest + [self.sum, self.r7, self.r6, self.six]
            self.play(*disappear(*gone),
                      *during([self.ev.animate.move_to([COL_X + 0.4, -0.2, 0])], 0.4, 1.0),
                      run_time=1.2)
            c.wait_until("they form a tree")
            cmap = {tuple(n.values): n for n in ct.nodes}
            anims = []
            for nd, pg in keep.items():
                cn = cmap[tuple(nd.values)]
                anims.append(pg.animate.move_to(cn.pivot_glyph).set_height(cn.pivot_glyph.height)
                             .set_color(FG))
            anims += during([GrowFromCenter(cn.body[0]) for cn in ct.nodes]
                            + [Create(e) for e in ct.edges + ct.stubs], 0.5, 1.0)
            self.play(*anims, run_time=min(2.0, c.until("three at the top")))
            for nd, pg in keep.items():
                self.remove(pg)
            self.remove(*[cn.body[0] for cn in ct.nodes], *ct.edges, *ct.stubs)
            self.add(ct)
            byv = {cn.pivot: cn for cn in ct.nodes}
            for cue, vs in (("three at the top", [3]), ("then seven", [7]),
                            ("five and nine", [5, 9]), ("then four", [4])):
                c.wait_until(cue)
                self.play(*[FlashAround(byv[v].body) for v in vs], run_time=0.9)
            c.wait_until("lopsided")
            croot = ct.root
            self.play(FlashAround(croot.body, color=YELLOW, run_time=1.2), run_time=1.2)
            c.wait_until("nothing went left")
            stub = croot.stubs["left"]
            z = T("0", size=36, color=RED).next_to(stub.get_end(), DOWN + LEFT, buff=0.12)
            self.play(stub.animate.set_color(RED), VShowPassingFlash(stub.copy().set_stroke(RED, 8)),
                      *appear(z, shift=None), run_time=1.2)
            c.wait_until("as lopsided")
            seven = byv[7]
            f = T("4", size=36, color=FG).next_to(seven.edge.get_center(), UP + RIGHT, buff=0.1)
            self.play(*appear(f, shift=None), run_time=0.8)
            c.wait_until("evensplit")
            tt = T("2 and 2", size=36, color=GREEN).next_to(self.ev, DOWN, buff=0.35)
            self.play(FlashAround(self.ev, color=GREEN, run_time=1.5), *appear(tt), run_time=1.5)
            c.wait_until("hold")
            q = T("?", size=64, color=YELLOW).next_to(croot.body, UP, buff=0.2)
            self.play(*appear(q), run_time=0.8)
