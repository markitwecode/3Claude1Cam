"""Chapter 5, scene 3: use the largest coin or skip it; the tree for change [5; 2] 6, walked down
and folded back up. Clips c5.choices.1 – c5.choices.4.

TREE LAYOUT (shared: s6 reuses it for change [2; 1] 4, and ch6's trace too; constants below)
  NODE_SIZE 30     node label Mono "amount, till": amount GOLD, ", " FG, till TEAL
  NODE_H 0.62      box height; width = label width + 2 * NODE_PAD (0.25); corner 0.15; BLUE stroke 3
  LEVEL_Y0 2.95    root centre y;  LEVEL_DY 1.4 between levels (five levels: 2.95 ... -2.65)
  EDGE_OFF 0.35    an edge runs from the parent's bottom centre +- 0.35 (use left, skip right) to the
                   child's top centre; FG stroke EDGE_W 4
  edge labels      T size 30, the coin value GOLD, "(too big)" DIM. At the edge midpoint: steep edges
                   LEFT (use) / RIGHT (skip) with buff 0.18, lifted 0.1; shallow edges (|dx| > 1.5|dy|)
                   at 0.65 of the way down, UL / UR with buff 0.06
  results          Mono 30 beside the node, buff 0.25: GREEN answers, RED dead-end []; the skip-stub
                   dead ends are Mono 28 RED at opacity 0.6
  outline          before the walk every box and edge is DIM, stroke 2.5, opacity 0.6
  this tree's x    root -0.4 | L1 -4.0, 3.75 | L2 -3.4, 2.45, 4.75 | L3 -2.8, 1.15, 3.45 | L4 -0.15, 2.15
                   (use 2 steps 1.3 left, skip-2 stubs 1.0 right, the too-big skips 0.6 right)

Layout:
choices.1  amount 6 (GOLD 72) left, the till [5; 2] (till_chain x1.15) right, DIM labels under.
           The 5 lifts out of its cell with a YELLOW halo, "?" beside it. {two}: the coin rises to
           (0, 2.35) and the state splits into two panels (x -+3.5: amount 54 over a till x0.75 with
           an empty head); the "?" becomes the two arrows "use 5" / "skip 5". {use}: the right side
           dims, a copy of the 5 becomes the 5 of "6 − 5", another drops back into the left till.
           {skip}: the left dims, the right till's empty head cell leaves, amount still 6.
           {sources}: YELLOW brace under both panels, "two sources of solutions".
choices.2  sweep; the DIM outline of the whole tree grows top-down. Walked: root, left edge, the
           too-big chain to "1, []", RED [].
choices.3  the right spine to "0, [2]" and GREEN [[]]; the three skip-2 stubs, each a DIM RED [].
choices.4  the left [] hops up beside "1, [2]" and "1, [5; 2]"; GOLD 2 discs sit by the use-2
           edges and slide onto the front of each answer as it rises: [[2]], [[2; 2]], [[2; 2; 2]].
           {join}: [] @ [[2; 2; 2]] beside the root becomes GREEN [[2; 2; 2]]; {missed}: the left path
           goes RED, "greedy's path". Everything fades.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── tree layout (shared with s6 and ch6) ─────────────────────────────────────────
NODE_SIZE = 30
NODE_H = 0.62
NODE_PAD = 0.25
NODE_CORNER = 0.15
LEVEL_Y0, LEVEL_DY = 2.95, 1.4
EDGE_OFF = 0.35
EDGE_W = 4
LABEL_SIZE = 30
LABEL_BUFF, LABEL_LIFT, SHALLOW_BUFF, SHALLOW_AT = 0.18, 0.1, 0.06, 0.65
RESULT_BUFF = 0.25
STUB_SIZE, STUB_OP = 28, 0.6
OUTLINE_W, OUTLINE_OP = 2.5, 0.6

# key: (level, x, amount, till)
NODES = {
    "R": (0, -0.4, 6, "[5; 2]"),
    "A": (1, -4.0, 1, "[5; 2]"),
    "B": (1, 3.75, 6, "[2]"),
    "A1": (2, -3.4, 1, "[2]"),
    "B1": (2, 2.45, 4, "[2]"),
    "B6": (2, 4.75, 6, "[]"),
    "A2": (3, -2.8, 1, "[]"),
    "B2": (3, 1.15, 2, "[2]"),
    "B4": (3, 3.45, 4, "[]"),
    "B3": (4, -0.15, 0, "[2]"),
    "B5": (4, 2.15, 2, "[]"),
}
# (parent, child, side: -1 use / +1 skip, label)
EDGES = [
    ("R", "A", -1, "use 5"), ("R", "B", 1, "skip 5"),
    ("A", "A1", 1, "skip 5 (too big)"), ("A1", "A2", 1, "skip 2 (too big)"),
    ("B", "B1", -1, "use 2"), ("B1", "B2", -1, "use 2"), ("B2", "B3", -1, "use 2"),
    ("B", "B6", 1, "skip 2"), ("B1", "B4", 1, "skip 2"), ("B2", "B5", 1, "skip 2"),
]
SPINE = ("B3", "B2", "B1", "B")          # the right spine, bottom up
ANSWERS = {"B3": "[[]]", "B2": "[[2]]", "B1": "[[2; 2]]", "B": "[[2; 2; 2]]"}
DISC_R, DISC_LABEL = 0.28, 28            # the GOLD 2 discs by the use-2 edges

# ── clip 1: the choice ──────────────────────────────────────────────────────────
COIN_R = 0.42                # the coin disc of ch4-ch7 (copied from ch1_s1_hook)
COIN_LABEL = 34
STATE_Y, LAB_Y = 0.0, -1.0
AMT_X, TILL_X, TILL_S = -3.7, 1.1, 1.15
LIFT_Y, LIFT_S = 1.9, 1.25
TOP = np.array([0.0, 2.35, 0.0])
PANEL_X, PANEL_AMT_Y, PANEL_TILL_Y, PANEL_S = 3.5, -0.3, -1.5, 0.9
ARROW_END = (2.9, 0.25)
BRACE_Y, BRACE_X = -2.2, 5.7
GREEDY_AT = (-4.4, -2.55)


def coin(v, r=COIN_R, size=COIN_LABEL):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=size, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def till_chain(values, scale=1.0):
    """The till: ConsChain(values) scaled `scale`, a coin in each cell (as in ch4_s2_idea)."""
    chain = ConsChain(values).scale(scale)
    for cell in chain.cells:
        cell.remove(cell.label)
        cell.label = coin(cell.value, r=COIN_R * scale).move_to(cell.box)
        cell.add(cell.label)
    return chain


def empty_head(chain):
    chain.cells[0].remove(chain.cells[0].label)
    return chain


def ring_flash(mob, color=YELLOW, r=None):
    ring = Circle(radius=r or mob.width / 2 + 0.1).move_to(mob).set_stroke(color, 6)
    return VShowPassingFlash(ring, time_width=1.0)


def detach(root, part):
    """Take `part` out of whichever group in `root`'s family holds it."""
    for m in root.get_family():
        if part in m.submobjects:
            m.remove(part)
            return


def node_label(amount, till):
    lab = Mono(f"{amount}, {till}", size=NODE_SIZE)
    n = len(str(amount))
    for i, g in enumerate(lab):
        g.set_color(GOLD if i < n else FG if i == n else TEAL)
    return lab


class Node:
    def __init__(self, level, x, amount, till):
        self.level = level
        pos = np.array([x, LEVEL_Y0 - level * LEVEL_DY, 0.0])
        self.label = node_label(amount, till).move_to(pos)
        self.box = RoundedRectangle(corner_radius=NODE_CORNER, width=self.label.width + 2 * NODE_PAD,
                                    height=NODE_H).move_to(pos)
        self.box.set_stroke(DIM, OUTLINE_W, opacity=OUTLINE_OP)


def edge_label(line, text, side):
    t2c = {text.split()[1]: GOLD}
    if "(" in text:
        t2c["(too big)"] = DIM
    lab = T(text, size=LABEL_SIZE, t2c=t2c)
    mid = line.point_from_proportion(0.5)
    v = line.get_end() - line.get_start()
    if abs(v[0]) > 1.5 * abs(v[1]):
        lab.next_to(line.point_from_proportion(SHALLOW_AT), UL if side < 0 else UR, buff=SHALLOW_BUFF)
    else:
        lab.next_to(mid, LEFT if side < 0 else RIGHT, buff=LABEL_BUFF).shift(LABEL_LIFT * UP)
    return lab


class Edge:
    def __init__(self, p, c, side, text):
        a = p.box.get_bottom() + RIGHT * side * EDGE_OFF
        b = c.box.get_top()
        self.line = Line(a, b).set_stroke(FG, EDGE_W)
        self.dim = Line(a, b).set_stroke(DIM, OUTLINE_W, opacity=OUTLINE_OP)
        self.label = edge_label(self.line, text, side)
        self.side = side


def result(node, s, color, side, size=NODE_SIZE):
    r = Mono(s, size=size, color=color)
    return r.next_to(node.box, LEFT if side < 0 else RIGHT, buff=RESULT_BUFF)


def until(c, cue, cap, lo=0.5, frac=0.85):
    return max(lo, min(cap, frac * c.until(cue)))


class Choices(NarratedScene):
    def construct(self):
        self.build_tree()
        self.choice()
        self.walk_left()
        self.walk_right()
        self.fold_up()
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ── the tree's pieces (nothing on screen yet) ─────────────────────────────────
    def build_tree(self):
        self.N = {k: Node(*v) for k, v in NODES.items()}
        self.E = {(p, c): Edge(self.N[p], self.N[c], s, t) for p, c, s, t in EDGES}
        N = self.N
        self.res = {
            "A2": result(N["A2"], "[]", RED, -1),
            "A1": result(N["A1"], "[]", RED, -1),
            "A": result(N["A"], "[]", RED, -1),
            **{k: result(N[k], "[]", RED, 1, size=STUB_SIZE).set_opacity(STUB_OP) for k in ("B6", "B4", "B5")},
            **{k: result(N[k], s, GREEN, -1) for k, s in ANSWERS.items()},
        }
        self.discs = {}
        for p, c in (("B", "B1"), ("B1", "B2"), ("B2", "B3")):
            e = self.E[(p, c)].line
            self.discs[c] = coin(2, r=DISC_R, size=DISC_LABEL).move_to(
                e.point_from_proportion(0.5) + RIGHT * (LABEL_BUFF + DISC_R))
        self._dims = []

    def edge_in(self, p, c, t0, t1):
        e = self.E[(p, c)]
        self._dims.append(e.dim)
        return [time_span(Create(e.line), t0, t1),
                time_span(FadeIn(e.label, shift=0.15 * DOWN), t0 + 0.35 * (t1 - t0), t1)]

    def node_in(self, k, src, t0, t1):
        n = self.N[k]
        anims = [time_span(Transform(n.box, n.box.copy().set_stroke(BLUE, 3, opacity=1)), t0, t1)]
        if src is None:
            anims.append(time_span(FadeIn(n.label, shift=0.15 * DOWN), t0, t1))
        else:
            anims.append(time_span(TransformMatchingStrings(self.N[src].label.copy(), n.label), t0, t1))
        return anims

    def walk(self, *anims, run_time):
        self.play(*anims, run_time=run_time)
        self.remove(*self._dims)          # the FG edge now covers its DIM outline
        self._dims = []

    # ── c5.choices.1: use the coin, or leave it out ───────────────────────────────
    def choice(self):
        amt = T("6", size=72, color=GOLD).move_to([AMT_X, STATE_Y, 0])
        till = till_chain([5, 2], TILL_S).move_to([TILL_X, STATE_Y, 0])
        amt_lab = T("amount", size=30, color=DIM).move_to([AMT_X, LAB_Y, 0])
        till_lab = T("till", size=30, color=DIM).move_to([TILL_X, LAB_Y, 0])

        with self.say("c5.choices.1") as c:
            # "So how do we find every way?"
            self.play(FadeIn(amt, shift=0.3 * DOWN), FadeIn(till),
                      time_span(FadeIn(amt_lab), 0.5, 1.3), time_span(FadeIn(till_lab), 0.5, 1.3), run_time=1.4)

            # "Look at the largest coin in the till, ..." The 5 lifts out of its cell and glows.
            c.wait_until("largest coin")
            cell0 = till.cells[0]
            five = cell0.label
            cell0.remove(five)
            self.add(five)
            up = np.array([five.get_x(), LIFT_Y, 0])
            halo_r = COIN_R * TILL_S * LIFT_S + 0.13
            halo = Circle(radius=halo_r).set_stroke(YELLOW, 4, opacity=0.85).move_to(up)
            self.play(five.animate.scale(LIFT_S).move_to(up), time_span(FadeIn(halo, scale=1.4), 0.8, 1.5),
                      run_time=1.5)

            # "... and ask one question about it."
            c.wait_until("one question")
            q = T("?", size=64, color=YELLOW).next_to(halo, RIGHT, buff=0.3)
            self.play(FadeIn(q, shift=0.2 * DOWN), ring_flash(halo, r=halo_r + 0.08), run_time=1.1)

            # "Every solution either uses that coin, or leaves it out." The state splits in two
            # under the coin; the question becomes the two arrows.
            c.wait_until("two")
            amt_l, amt_r = [T("6", size=60, color=GOLD).move_to([s * PANEL_X, PANEL_AMT_Y, 0]) for s in (-1, 1)]
            till_l, till_r = [empty_head(till_chain([5, 2], PANEL_S)).move_to([s * PANEL_X, PANEL_TILL_Y, 0])
                              for s in (-1, 1)]
            q_at = TOP + RIGHT * (halo_r + 0.3 + q.width / 2)
            self.play(five.animate.move_to(TOP), halo.animate.move_to(TOP), q.animate.move_to(q_at),
                      FadeOut(amt_lab), FadeOut(till_lab),
                      TransformFromCopy(amt, amt_r), ReplacementTransform(amt, amt_l),
                      TransformFromCopy(till, till_r), ReplacementTransform(till, till_l), run_time=1.8)
            arrows, tags = [], []
            for s, word in ((-1, "use 5"), (1, "skip 5")):
                end = np.array([s * ARROW_END[0], ARROW_END[1], 0])
                d = (end - TOP) / np.linalg.norm(end - TOP)
                a = Arrow(TOP + d * (halo_r + 0.12), end, buff=0, stroke_width=5, color=FG,
                          max_tip_length_to_length_ratio=0.12)
                tag = T(word, size=36, t2c={"5": GOLD}).next_to(a.get_center(), UL if s < 0 else UR, buff=0.12)
                arrows.append(a)
                tags.append(tag)
            self.play(ReplacementTransform(q.copy(), arrows[0]), ReplacementTransform(q, arrows[1]),
                      *[time_span(FadeIn(t, shift=0.2 * DOWN), 0.6, 1.4) for t in tags], run_time=1.4)

            # "If it uses the coin, we hand that coin over, ..."
            c.wait_until("use")
            right = [arrows[1], tags[1], amt_r, till_r]
            for m in right:
                m.save_state()
            self.play(*[m.animate.fade(0.65) for m in right], run_time=1.0)
            c.wait_until("hand that coin over")
            pay = five.copy()
            self.play(Transform(pay, coin(5, r=COIN_R * PANEL_S).move_to([-PANEL_X + 1.1, PANEL_AMT_Y, 0])),
                      run_time=until(c, "amount minus", 1.4))

            # "... and still need change for the amount minus the coin."
            c.wait_until("amount minus")
            amt_l2 = T("6 − 5", size=60).move_to([-PANEL_X, PANEL_AMT_Y, 0])
            amt_l2[0].set_color(GOLD)
            amt_l2[2].set_color(GOLD)
            self.play(amt_l.animate.move_to(amt_l2[0]), FadeIn(amt_l2[1]), FadeTransform(pay, amt_l2[2]),
                      run_time=1.4)
            self.remove(amt_l, amt_l2[1], amt_l2[2])
            self.add(amt_l2)

            # "And the same coin may be used again." The 5 drops back into the left till.
            c.wait_until("same coin")
            slot = till_l.cells[0]
            back = five.copy()
            self.play(Transform(back, coin(5, r=COIN_R * PANEL_S).move_to(slot.box), path_arc=0.7), run_time=1.5)
            self.remove(back)
            slot.add(back)
            self.play(ring_flash(back), run_time=0.9)

            # "If it leaves the coin out, we need change for the whole amount, from the rest of the till."
            c.wait_until("skip")
            left = [arrows[0], tags[0], amt_l2, till_l]
            for m in left:
                m.save_state()
            self.play(*[Restore(m) for m in right], *[m.animate.fade(0.65) for m in left], run_time=1.0)
            head, ptr = till_r.cells[0], till_r.arrows[0]
            detach(till_r, head)
            detach(till_r, ptr)
            self.add(head, ptr)
            dx = PANEL_X - till_r.get_center()[0]
            self.play(FadeOut(head, shift=0.6 * DOWN), FadeOut(ptr, shift=0.6 * DOWN),
                      till_r.animate.shift(dx * RIGHT), run_time=until(c, "whole amount", 1.5))
            c.wait_until("whole amount")
            self.play(FlashAround(amt_r, color=YELLOW), run_time=until(c, "rest of the till", 1.2, frac=0.95))
            c.wait_until("rest of the till")
            self.play(FlashAround(till_r, color=YELLOW), run_time=until(c, "sources", 1.2, frac=0.95))

            # "So there are two sources of solutions, and we want them both."
            c.wait_until("sources")
            brace = span_brace(np.array([-BRACE_X, BRACE_Y, 0]), np.array([BRACE_X, BRACE_Y, 0]),
                               direction=DOWN, color=YELLOW)
            src = T("two sources of solutions", size=40, color=YELLOW).next_to(brace, DOWN, buff=0.2)
            self.play(*[Restore(m) for m in left], GrowFromCenter(brace),
                      time_span(FadeIn(src, shift=0.3 * DOWN), 0.5, 1.4), run_time=1.4)

    # ── c5.choices.2: the tree; down the left to a dead end ───────────────────────
    def walk_left(self):
        N = self.N
        with self.say("c5.choices.2") as c:
            # "Let's draw it as a tree, for six, with fives and twos." The board clears as the whole
            # shape grows in, top-down.
            c.wait_until("for six")
            t = max(1.4, min(2.0, c.until("root") - 0.95))
            step = t / 5.0
            anims = []
            for n in N.values():
                anims.append(time_span(Create(n.box), n.level * step, min(t, (n.level + 1.2) * step)))
            for (p, k), e in self.E.items():
                lv = N[k].level
                anims.append(time_span(Create(e.dim), (lv - 0.6) * step, lv * step))
            sweep_clear(self, run_time=0.9)
            self.play(*anims, run_time=t)

            # "Each node shows the amount still owed, and the coins still allowed."
            c.wait_until("root")
            self.walk(*self.node_in("R", None, 0, 1.2), run_time=1.2)
            c.wait_until("amount still owed")
            self.play(FlashAround(N["R"].label[0], color=GOLD), run_time=1.2)
            c.wait_until("coins still allowed")
            self.play(FlashAround(N["R"].label[2:], color=TEAL), run_time=1.2)

            # "On the left, we use the five. That leaves one, still with fives and twos."
            c.wait_until("usefive")
            self.walk(*self.edge_in("R", "A", 0, 1.2), run_time=1.2)
            c.wait_until("That leaves one")
            self.walk(*self.node_in("A", "R", 0, 1.5), run_time=1.5)

            # "Now the five is too big, so it must be skipped, and so must the two."
            c.wait_until("toobig")
            self.walk(*self.edge_in("A", "A1", 0, 1.0), *self.node_in("A1", "A", 0.7, 1.9), run_time=1.9)
            c.wait_until("so must the two")
            self.walk(*self.edge_in("A1", "A2", 0, 0.9), *self.node_in("A2", "A1", 0.6, 1.6), run_time=1.6)

            # "The till is empty, with one still owed. A dead end, with no solutions."
            c.wait_until("dead")
            self.play(FlashAround(N["A2"].label[2:], color=TEAL), run_time=until(c, "one still owed", 1.1))
            c.wait_until("one still owed")
            self.play(FlashAround(N["A2"].label[0], color=GOLD), run_time=until(c, "A dead end", 1.1))
            c.wait_until("A dead end")
            self.play(FadeIn(self.res["A2"], shift=0.3 * LEFT), run_time=1.0)

    # ── c5.choices.3: down the right, to zero; the skip stubs ─────────────────────
    def walk_right(self):
        N = self.N
        with self.say("c5.choices.3") as c:
            # "On the right, we skip the five, and need six from twos alone."
            self.walk(*self.edge_in("R", "B", 0, 1.2), run_time=1.2)
            c.wait_until("need six")
            self.walk(*self.node_in("B", "R", 0, 1.5), run_time=1.5)

            # "Use a two, leaving four. Use another, leaving two. Use a third, leaving zero."
            c.wait_until("chain")
            self.walk(*self.edge_in("B", "B1", 0, 1.0), *self.node_in("B1", "B", 0.6, 1.8), run_time=1.8)
            c.wait_until("Use another")
            self.walk(*self.edge_in("B1", "B2", 0, 0.8), *self.node_in("B2", "B1", 0.5, 1.4), run_time=1.4)
            c.wait_until("Use a third")
            self.walk(*self.edge_in("B2", "B3", 0, 0.7), *self.node_in("B3", "B2", 0.4, 1.2), run_time=1.2)

            # "Zero is success, one way, with no coins."
            c.wait_until("success")
            self.play(FlashAround(N["B3"].label[0], color=GOLD),
                      time_span(FadeIn(self.res["B3"], shift=0.3 * LEFT), 0.3, 1.2), run_time=1.2)
            c.wait_until("one way")
            self.play(FlashAround(self.res["B3"], color=GREEN), run_time=1.2)

            # "Along the way, each skip branch empties the till with money still owed, ..."
            c.wait_until("stubs")
            anims = []
            for i, (p, k) in enumerate((("B", "B6"), ("B1", "B4"), ("B2", "B5"))):
                t0 = 0.45 * i
                anims += self.edge_in(p, k, t0, t0 + 0.8) + self.node_in(k, p, t0 + 0.5, t0 + 1.3)
            self.walk(*anims, run_time=2.2)

            # "... so those are dead ends too."
            c.wait_until("dead ends")
            t = max(0.6, min(1.0, c.remaining - 0.15))
            self.play(*[time_span(FadeIn(self.res[k], shift=0.2 * RIGHT), 0.2 * i * t, (0.6 + 0.2 * i) * t)
                        for i, k in enumerate(("B6", "B4", "B5"))], run_time=t)

    # ── c5.choices.4: answers flow back up ────────────────────────────────────────
    def grow_answer(self, child, parent, run_time):
        """child's answer (beside its node) rises into parent's; the edge's disc becomes the new
        front 2 (and, after the first step, a new ';')."""
        kid, ans = self.res[child], self.res[parent]
        k = 1 if len(kid) == 4 else 2
        anims, temps = [], []
        for i, g in enumerate(kid):
            j = i if i < 2 else i + k
            cp = g.copy()
            temps.append(cp)
            anims.append(Transform(cp, ans[j].copy()))
        new = ans[2].copy()
        anims.append(FadeTransform(self.discs[child], new))
        extra = [ans[3].copy()] if k == 2 else []
        anims += [time_span(FadeIn(e), 0.5 * run_time, run_time) for e in extra]
        self.play(*anims, run_time=run_time)
        self.remove(*temps, new, *extra)
        self.add(ans)

    def fold_up(self):
        N, E, res = self.N, self.E, self.res
        with self.say("c5.choices.4") as c:
            # "Now the answers flow back up." The left side's [] climbs first.
            self.play(TransformFromCopy(res["A2"], res["A1"]), run_time=0.9)
            self.play(TransformFromCopy(res["A1"], res["A"]), run_time=0.9)

            # "On each edge where we used a two, a two goes onto the front of every solution coming up."
            c.wait_until("add")
            discs = [self.discs[k] for k in ("B1", "B2", "B3")]
            self.play(*[time_span(FadeIn(d, scale=0.5), 0.3 * i, 0.3 * i + 0.9) for i, d in enumerate(discs)],
                      *[time_span(FlashUnder(E[e].label, color=GOLD), 0.3 * i, 0.3 * i + 1.2)
                        for i, e in enumerate((("B", "B1"), ("B1", "B2"), ("B2", "B3")))], run_time=1.8)
            c.wait_until("front")
            self.play(FlashAround(res["B3"], color=GREEN), run_time=1.2)

            # "The empty solution becomes a single two, then a pair of twos, then three twos."
            c.wait_until("growing")
            self.grow_answer("B3", "B2", run_time=max(1.3, min(1.8, c.until("single two") + 0.4)))
            c.wait_until("pair of twos")
            self.grow_answer("B2", "B1", run_time=until(c, "three twos", 1.2, frac=0.95))
            c.wait_until("three twos")
            self.grow_answer("B1", "B", run_time=until(c, "join", 1.1, frac=0.95))

            # "At the top, the left side brings nothing, and the right side brings one solution."
            c.wait_until("join")
            join = Mono("[] @ [[2; 2; 2]]", size=NODE_SIZE, color=GREEN)
            join.next_to(N["R"].box, RIGHT, buff=RESULT_BUFF)
            join[0:2].set_color(RED)
            join[2].set_color(GOLD)
            self.play(FlashAround(N["R"].box, color=YELLOW), run_time=until(c, "left side", 1.0))
            c.wait_until("left side")
            lcp = res["A"].copy()
            self.play(Transform(lcp, join[0:2].copy(), path_arc=-1.4), run_time=until(c, "right side", 1.5))
            c.wait_until("right side")
            rcp = res["B"].copy()
            at = join[2].copy()
            self.play(Transform(rcp, join[3:].copy()), time_span(FadeIn(at, scale=0.6), 0.8, 1.5), run_time=1.5)
            self.remove(lcp, rcp, at)
            self.add(join)

            # "Joined together, that's a list holding one solution, two, two, two."
            c.wait_until("a list holding")
            final = Mono("[[2; 2; 2]]", size=NODE_SIZE, color=GREEN).next_to(N["R"].box, RIGHT, buff=RESULT_BUFF)
            self.play(TransformMatchingStrings(join, final, matched_keys=("[[2; 2; 2]]",)), run_time=1.6)

            # "That's the answer greedy missed, ..." The answer flashes; greedy's path goes RED.
            c.wait_until("missed")
            path = [E[e].line for e in (("R", "A"), ("A", "A1"), ("A1", "A2"))]
            greedy = T("greedy's path", size=34, color=RED).move_to([*GREEDY_AT, 0])
            self.play(FlashAround(final, color=GREEN, run_time=1.2),
                      *[time_span(ln.animate.set_stroke(RED, 5), 0.4 + 0.25 * i, 1.1 + 0.25 * i)
                        for i, ln in enumerate(path)],
                      time_span(FadeIn(greedy, shift=0.2 * UP), 0.9, 1.8), run_time=1.8)

            # "... because greedy only ever walked the left path."
            c.wait_until("left path")
            t = max(0.6, min(1.2, c.remaining - 0.1))
            self.play(*[time_span(VShowPassingFlash(ln.copy().set_stroke(YELLOW, 8), time_width=0.6),
                                  0.25 * i * t, (0.5 + 0.25 * i) * t) for i, ln in enumerate(path)], run_time=t)
