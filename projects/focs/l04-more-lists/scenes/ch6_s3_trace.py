"""Chapter 6, scene 3: following the accumulators. The tree for change [2; 1] 4 [] [], walked in the order
it runs, a chg tag on every node and the solutions so far filling up. Clips c6.trace.1 – c6.trace.4.

Opening shot (s2's last): `change [2; 1] 4 [] []` alone, Code 32 at (0, 3.3), change YELLOW, both [] TEAL.
At {same} it slides left (left edge x -6.4, y 3.3); in c6.trace.4 it returns to (0, 3.3).

Tree (ch5's look, ch5_s3_choices): node Mono 30 "amount, till" (amount GOLD, till TEAL) in a BLUE RoundedRectangle
  (h 0.62, w text + 2 x 0.25, corner 0.15, stroke 3); edges parent bottom +-0.35 -> child top, stroke 4; edge labels
  T 30 (coin GOLD, ch5's placement) on the root's two edges only. Outline before the walk: boxes and edges DIM 2.5 at
  0.6, node labels at 0.45. Both ones chains expanded (16 nodes, 6 levels).
  levels   y 2.35 - 1.1 k, k = 0 ... 5
  x        root 0.2 | L1 -3.1, 3.45 | L2 -4.77 ("0, [2; 1]"), -1.464 ("2, [1]"), 3.1, 5.275 ("4, []")
           use side's chain steps 1.2 left (dead ends 0.975 right of the parent); skip side's chain steps 0.35 left
           (vertical use edges, dead ends 1.825 right of the parent)
  walk     a YELLOW cursor (box + 0.16, corner 0.22, stroke 4) slides node to node; walked edges YELLOW while on the
           current path, FG once done; dead ends light BLUE with a RED flash.
chg tags: ch5's solution box (coin x0.6 in TEAL, corner 0.1, stroke 3, pad 0.12) at scale 0.7, left of the node
  (buff 0.22; "0, [2; 1]"'s under it). A child's tag is its parent's, moved, with the till's head coin flown in front.
  Coin digits are T 46 before scaling (19 on screen; ch5's 34 would be 14 at this scale).
Solutions so far: ch5's list-of-solutions frame (corner 0.15, stroke 4, pad 0.2) at scale 0.7 as a row, newest at
  the front (left), right end x 6.55, centre y 2.62; DIM T 30 "solutions so far" above it (right-aligned, y 3.38).
c6.trace.4: replies Code 36 (OCaml's margin-40 layout, as ch5): now centred (0, 2.15); ch5's at opacity 0.4 at
  (0, 0.55) with DIM "last time"; GOLD MathTex 48 sum at y -0.8; L3's rev_app Code 28 at opacity 0.5 (left -5.8,
  centre y -2.5) with TEAL "consing reverses". Ends on an empty frame.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

COIN_R, COIN_LABEL = 0.42, 34                       # ch1's coin
SMALL_LABEL = 46                                    # digits of the 0.42-scale coins in tags and the row
NODE, NODE_H, NODE_PAD, NODE_CORNER = 30, 0.62, 0.25, 0.15
EDGE_OFF, EDGE_W = 0.35, 4
OUTLINE_W, OUTLINE_OP, LABEL_OP, ELABEL_OP = 2.5, 0.6, 0.45, 0.6
L0, DY = 2.35, 1.1
TS, TAG_BUFF = 0.7, 0.22                            # chg tags
RS, ROW_R, ROW_Y = 0.7, 6.55, 2.62                  # the solutions-so-far row

CALL = "change [2; 1] 4 [] []"
CALL_LEFT = -6.4
PREFIX = "- : int list list ="
NOW = "[[2; 2]; [1; 1; 2]; [1; 1; 1; 1]]"
OLD = "[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]"
REV_APP = ("let rec rev_app xs ys =\n"
           "  match xs, ys with\n"
           "  | [], ys    -> ys\n"
           "  | x::xs, ys -> rev_app xs (x::ys)")

# key: (level, x, amount, till, chg); chg None = a dead end (the till ran out)
NODES = {
    "R": (0, 0.2, 4, "[2; 1]", []),
    "U": (1, -3.1, 2, "[2; 1]", [2]),
    "S": (1, 3.45, 4, "[1]", []),
    "UU": (2, -4.77, 0, "[2; 1]", [2, 2]),
    "US": (2, -1.464, 2, "[1]", [2]),
    "S1": (2, 3.1, 3, "[1]", [1]),
    "Sx": (2, 5.275, 4, "[]", None),
    "US1": (3, -2.664, 1, "[1]", [1, 2]),
    "USx": (3, -0.489, 2, "[]", None),
    "S2": (3, 2.75, 2, "[1]", [1, 1]),
    "S1x": (3, 4.925, 3, "[]", None),
    "US2": (4, -3.864, 0, "[1]", [1, 1, 2]),
    "US1x": (4, -1.689, 1, "[]", None),
    "S3": (4, 2.4, 1, "[1]", [1, 1, 1]),
    "S2x": (4, 4.575, 2, "[]", None),
    "S4": (5, 2.05, 0, "[1]", [1, 1, 1, 1]),
    "S3x": (5, 4.225, 1, "[]", None),
}
EDGES = [("R", "U", -1), ("R", "S", 1), ("U", "UU", -1), ("U", "US", 1), ("S", "S1", -1), ("S", "Sx", 1),
         ("US", "US1", -1), ("US", "USx", 1), ("S1", "S2", -1), ("S1", "S1x", 1),
         ("US1", "US2", -1), ("US1", "US1x", 1), ("S2", "S3", -1), ("S2", "S2x", 1),
         ("S3", "S4", -1), ("S3", "S3x", 1)]
ELABELS = {("R", "U"): "use 2", ("R", "S"): "skip 2"}


# ── shared looks (ch5) ───────────────────────────────────────────────────────────
def coin(v, r=COIN_R, size=COIN_LABEL):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=size, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def solution(vals, s=1.0):
    """One solution: coins in a row inside a TEAL box (empty: a coin-height square)."""
    d = 2 * COIN_R * 0.6 * s
    coins = VGroup(*[coin(v, size=SMALL_LABEL).scale(0.6 * s) for v in vals])
    if vals:
        coins.arrange(RIGHT, buff=0.1 * s)
    w = (coins.width if vals else d) + 0.24 * s
    rect = RoundedRectangle(corner_radius=0.1 * s, width=w, height=d + 0.24 * s).set_stroke(TEAL, 3)
    if vals:
        rect.move_to(coins)
    return VGroup(rect, coins)


def row_layout(lists):
    """The solutions so far: boxes (newest first) in a TEAL frame whose right end is fixed at ROW_R."""
    boxes = [solution(v, RS) for v in lists]
    h = 2 * COIN_R * 0.6 * RS + 0.24 * RS
    if boxes:
        g = VGroup(*boxes).arrange(RIGHT, buff=0.2 * RS)
        w = g.width
    else:
        w = h
    frame = RoundedRectangle(corner_radius=0.15 * RS, width=w + 0.4 * RS,
                             height=h + 0.4 * RS).set_stroke(TEAL, 4)
    frame.move_to([ROW_R - frame.width / 2, ROW_Y, 0])
    if boxes:
        g.move_to(frame)
    return frame, boxes


def node_label(amount, till):
    lab = Mono(f"{amount}, {till}", size=NODE)
    n = len(str(amount))
    for i, g in enumerate(lab):
        g.set_color(GOLD if i < n else FG if i == n else TEAL)
    return lab


class Node:
    def __init__(self, key, level, x, amount, till, chg):
        self.key, self.level, self.chg = key, level, chg
        self.n = len(str(amount))
        pos = np.array([x, L0 - level * DY, 0.0])
        self.label = node_label(amount, till).move_to(pos).set_opacity(LABEL_OP)
        self.box = RoundedRectangle(corner_radius=NODE_CORNER, width=self.label.width + 2 * NODE_PAD,
                                    height=NODE_H).move_to(pos).set_stroke(DIM, OUTLINE_W, opacity=OUTLINE_OP)
        self.tag = None

    def head(self):
        """The till's first coin in the label ("4, [2; 1]" -> the 2)."""
        return self.label[self.n + 2]

    def tag_shape(self):
        t = solution(self.chg, TS)
        if self.key == "UU":
            return t.next_to(self.box, DOWN, buff=0.12).align_to(self.box, LEFT)
        return t.next_to(self.box, LEFT, buff=TAG_BUFF)


def edge_label(a, b, text, side):
    v = text.split()[1]
    lab = T(text, size=30, t2c={v: GOLD})
    line = Line(a, b)
    d = b - a
    if abs(d[0]) > 1.5 * abs(d[1]):
        lab.next_to(line.point_from_proportion(0.65), UL if side < 0 else UR, buff=0.06)
    else:
        lab.next_to(line.point_from_proportion(0.5), LEFT if side < 0 else RIGHT, buff=0.18).shift(0.1 * UP)
    return lab


class Edge:
    def __init__(self, p, c, side, text=None):
        self.a = p.box.get_bottom() + RIGHT * side * EDGE_OFF
        self.b = c.box.get_top()
        self.dim = Line(self.a, self.b).set_stroke(DIM, OUTLINE_W, opacity=OUTLINE_OP)
        self.label = edge_label(self.a, self.b, text, side).set_opacity(ELABEL_OP) if text else None
        self.yl = None

    def make(self, color):
        return Line(self.a, self.b).set_stroke(color, EDGE_W)


def cursor_for(node):
    return RoundedRectangle(corner_radius=0.22, width=node.box.width + 0.16,
                            height=NODE_H + 0.16).set_stroke(YELLOW, 4).move_to(node.box)


class AccTrace(NarratedScene):
    def construct(self):
        self.build()
        self.open_tree()
        self.skip_side()
        self.use_side()
        self.answer()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ── pieces ──────────────────────────────────────────────────────────────────
    def build(self):
        self.call = Code(CALL, size=32).move_to([0, 3.3, 0])
        self.call.find("change").set_color(YELLOW)
        for k in range(2):
            self.call.find("[]", nth=k).set_color(TEAL)
        self.N = {k: Node(k, *v) for k, v in NODES.items()}
        self.E, self.parent = {}, {}
        for p, ch, side in EDGES:
            self.E[(p, ch)] = Edge(self.N[p], self.N[ch], side, ELABELS.get((p, ch)))
            self.parent[ch] = p
        self.cursor = cursor_for(self.N["R"])
        self.sols = []
        self.frame, self.boxes = row_layout([])
        self._dims = []

    def walk(self, *anims, run_time):
        self.play(*anims, run_time=run_time)
        self.remove(*self._dims)          # the drawn edge now covers its DIM outline
        self._dims = []

    def step(self, pk, ck, coin=False, rt=1.2, draw_edge=True, extra=()):
        """The cursor goes down one edge; the child lights; its tag is the parent's, plus the head coin."""
        p, ch = self.N[pk], self.N[ck]
        e = self.E[(pk, ck)]
        anims = list(extra)
        if draw_edge:
            e.yl = e.make(YELLOW)
            self._dims.append(e.dim)
            anims.append(time_span(Create(e.yl), 0, 0.5 * rt))
            if e.label is not None:
                anims.append(time_span(e.label.animate.set_opacity(1), 0, 0.5 * rt))
        anims += [time_span(Transform(self.cursor, cursor_for(ch)), 0.15 * rt, 0.75 * rt),
                  time_span(ch.box.animate.set_stroke(BLUE, 3, opacity=1), 0.3 * rt, 0.8 * rt),
                  time_span(ch.label.animate.set_opacity(1), 0.3 * rt, 0.8 * rt)]
        ch.tag = ch.tag_shape()
        start = p.tag.copy()
        if coin:
            new = ch.tag[1][0].copy().scale(0.6).move_to(p.head())
            start = VGroup(start[0], VGroup(new, *start[1]))
        anims.append(time_span(ReplacementTransform(start, ch.tag), 0.3 * rt, rt))
        self.walk(*anims, run_time=rt)

    def light_dead(self, k, t0, t1, flash=True):
        n = self.N[k]
        e = self.E[(self.parent[k], k)]
        d = t1 - t0
        e.yl = e.make(FG)
        self._dims.append(e.dim)
        anims = [time_span(Create(e.yl), t0, t0 + 0.5 * d),
                 time_span(n.box.animate.set_stroke(BLUE, 3, opacity=1), t0 + 0.3 * d, t1),
                 time_span(n.label.animate.set_opacity(1), t0 + 0.3 * d, t1)]
        if flash:
            anims.append(time_span(FlashAround(n.box, color=RED, time_width=1.5, buff=0.08),
                                   t0 + 0.5 * d, t1 + 0.5))
        return anims

    def add_solution(self, k, rt):
        """The node's chg box flies onto the front of the solutions so far."""
        n = self.N[k]
        self.sols.insert(0, n.chg)
        frame, boxes = row_layout(self.sols)
        self.play(Transform(self.frame, frame), TransformFromCopy(n.tag, boxes[0]), run_time=rt)
        self.boxes.insert(0, boxes[0])

    def to_fg(self, pairs):
        return [self.E[p].yl.animate.set_stroke(FG) for p in pairs]

    # ── c6.trace.1: the same tree; the root starts with nothing ────────────────────
    def open_tree(self):
        call, N, E = self.call, self.N, self.E
        with self.say("c6.trace.1") as c:
            self.play(FadeIn(call), run_time=0.8)
            c.wait_until("making four")
            self.play(FlashAround(call.find("4"), color=GOLD, time_width=1.5), run_time=1.1)
            c.wait_until("twos and ones")
            self.play(FlashAround(call.find("[2; 1]"), color=TEAL, time_width=1.5), run_time=1.1)

            c.wait_until("same")
            call.generate_target()
            call.target.align_to([CALL_LEFT, 0, 0], LEFT)
            rt = max(1.2, min(2.0, c.until("start") - 0.1))
            lv = (rt - 0.6) / 5
            anims = [time_span(MoveToTarget(call), 0, min(1.0, rt))]
            for (p, ch), e in E.items():
                t0 = N[ch].level * lv
                anims.append(time_span(Create(e.dim), max(0, t0 - 0.15), t0 + 0.35))
                if e.label is not None:
                    anims.append(time_span(FadeIn(e.label), t0, t0 + 0.6))
            for n in N.values():
                t0 = n.level * lv
                anims += [time_span(FadeIn(n.box), t0, t0 + 0.6), time_span(FadeIn(n.label), t0, t0 + 0.6)]
            self.play(*anims, run_time=rt)

            c.wait_until("start")
            R = N["R"]
            self.play(R.box.animate.set_stroke(BLUE, 3, opacity=1), R.label.animate.set_opacity(1),
                      Create(self.cursor), run_time=1.0)
            c.wait_until("no coins chosen")
            R.tag = R.tag_shape()
            self.coins_lab = T("coins so far", 30, DIM).next_to(R.tag, LEFT, buff=0.22)
            self.play(TransformFromCopy(call.find("[]", nth=0), R.tag),
                      time_span(FadeIn(self.coins_lab, shift=0.2 * DOWN), 0.5, 1.2), run_time=1.2)
            c.wait_until("no solutions")
            self.sol_lab = T("solutions so far", 30, DIM).move_to([0, 3.38, 0]).align_to([ROW_R, 0, 0], RIGHT)
            rt = max(0.6, min(1.2, c.remaining - 0.05))
            self.play(TransformFromCopy(call.find("[]", nth=1), self.frame),
                      time_span(FadeIn(self.sol_lab, shift=0.2 * DOWN), 0.4 * rt, rt), run_time=rt)

    # ── c6.trace.2: the skip call runs first; four ones; the dead ends ────────────
    def skip_side(self):
        N, E = self.N, self.E
        eu, es = E[("R", "U")], E[("R", "S")]
        with self.say("c6.trace.2") as c:
            c.wait_until("its last argument")
            self.needs = T("needs its last argument", 30).move_to([0, 2.45, 0]).align_to([-2.2, 0, 0], RIGHT)
            self.play(FadeOut(self.coins_lab), FadeIn(self.needs, shift=0.2 * DOWN),
                      eu.label.animate.set_opacity(1), run_time=1.2)
            c.wait_until("that's the skip call")
            es.yl = es.make(YELLOW)
            self._dims.append(es.dim)
            self.walk(Create(es.yl), es.label.animate.set_opacity(1), run_time=1.3)

            c.wait_until("ones")
            self.step("R", "S", rt=1.5, draw_edge=False)
            c.wait_until("four from ones")
            self.play(FlashUnder(N["S"].label, color=YELLOW), run_time=1.0)

            c.wait_until("Each step down")
            self.step("S", "S1", coin=True, rt=1.4)
            self.step("S1", "S2", coin=True, rt=1.0)
            self.step("S2", "S3", coin=True, rt=0.9)
            c.wait_until("found")
            self.step("S3", "S4", coin=True, rt=1.2)
            c.wait_until("That's the first solution")
            self.add_solution("S4", rt=1.5)

            c.wait_until("dead")
            anims = []
            for i, k in enumerate(("Sx", "S1x", "S2x", "S3x")):
                anims += self.light_dead(k, 0.35 * i, 0.35 * i + 0.9)
            self.walk(*anims, run_time=2.45)
            c.wait_until("hand the solutions")
            self.play(FlashAround(self.frame, color=TEAL, time_width=1.5),
                      run_time=max(0.6, min(1.2, c.remaining - 0.05)))

    # ── c6.trace.3: the list goes up to the use call; use a two ────────────────────
    def use_side(self):
        N = self.N
        with self.say("c6.trace.3") as c:
            self.play(FlashAround(self.frame, color=TEAL, time_width=1.5), run_time=1.1)
            c.wait_until("goes back up")
            self.play(*self.to_fg([("R", "S"), ("S", "S1"), ("S1", "S2"), ("S2", "S3"), ("S3", "S4")]),
                      Transform(self.cursor, cursor_for(N["R"])), run_time=1.3)
            c.wait_until("and becomes")
            row = VGroup(self.frame, *self.boxes)
            self.handed = row.copy().scale(0.9).move_to([0, 2.5, 0]).align_to([-2.2, 0, 0], RIGHT)
            self.play(FadeOut(self.needs), TransformFromCopy(row, self.handed, path_arc=0.4), run_time=1.8)

            c.wait_until("usetwo")
            self.step("R", "U", coin=True, rt=1.6)
            c.wait_until("a single two")
            self.play(FlashAround(N["U"].tag, color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("two left to make")
            self.play(FlashAround(N["U"].label[0], color=GOLD, time_width=1.5, buff=0.06), run_time=1.1)

            c.wait_until("again")
            self.step("U", "US", rt=1.5)
            c.wait_until("The skip side runs first")
            self.step("US", "US1", coin=True, rt=1.0, extra=self.light_dead("USx", 0, 1.0, flash=False))
            self.step("US1", "US2", coin=True, rt=1.0, extra=self.light_dead("US1x", 0, 1.0, flash=False))
            c.wait_until("one, one, two")
            self.add_solution("US2", rt=1.3)

            c.wait_until("last")
            self.step("U", "UU", coin=True, rt=1.6,
                      extra=[time_span(a, 0, 1.0) for a in self.to_fg([("U", "US"), ("US", "US1"), ("US1", "US2")])])
            c.wait_until("record two, two")
            self.add_solution("UU", rt=max(0.6, min(1.3, c.remaining - 0.05)))

    # ── c6.trace.4: the reply, compared with last time's ───────────────────────────
    def answer(self):
        call = self.call
        with self.say("c6.trace.4") as c:
            row = VGroup(self.frame, *self.boxes)
            self.remove(self.frame, *self.boxes)
            self.add(row)
            now = Code(PREFIX + "\n" + NOW, size=36).move_to([0, 2.15, 0])
            call.generate_target()
            call.target.move_to([0, 3.3, 0])
            sweep_clear(self, time_span(MoveToTarget(call), 0.4, 1.6), time_span(FadeTransform(row, now), 0.5, 2.0),
                        keep=[call, row], run_time=2.0)

            c.wait_until("the same three as last time")
            old = Code(PREFIX + "\n" + OLD, size=36).move_to([0, 0.55, 0]).set_opacity(0.4)
            last = T("last time", 30, DIM).next_to(old.line(0), RIGHT, buff=0.6)
            self.play(FadeIn(old, shift=0.2 * DOWN), time_span(FadeIn(last, shift=0.2 * DOWN), 0.4, 1.2),
                      run_time=1.2)

            mid_now, mid_old = now.find("[1; 1; 2]"), old.find("[2; 1; 1]")
            c.wait_until("reversed")
            self.play(*recolor(mid_now, YELLOW), FlashAround(mid_now, color=YELLOW, time_width=1.5), run_time=1.3)
            c.wait_until("two, one, one")
            self.play(*[g.animate.set_color(YELLOW).set_opacity(1) for g in mid_old],
                      FlashAround(mid_old, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("and now it's")
            self.play(FlashAround(mid_now, color=YELLOW, time_width=1.5), run_time=1.1)

            c.wait_until("why")
            rev = Code(REV_APP, size=28).set_opacity(0.5)
            rev.move_to([0, -2.5, 0]).align_to([-5.8, 0, 0], LEFT)
            cons = T("consing reverses", 30, TEAL).next_to(rev, RIGHT, buff=0.5)
            self.play(FadeIn(rev, shift=0.2 * UP), time_span(FadeIn(cons, shift=0.2 * DOWN), 0.5, 1.3), run_time=1.3)
            c.wait_until("ends up last")
            self.play(FlashAround(now.find("2", line=1, nth=2), color=YELLOW, time_width=1.5), run_time=1.1)
            c.wait_until("as with rev-app")
            self.play(FlashAround(rev.find("(x::ys)"), color=TEAL, time_width=1.5), run_time=1.1)

            c.wait_until("fine")
            eq = MathTex("1 + 1 + 2", "=", "2 + 1 + 1", "=", "4", font_size=48).set_color(GOLD).move_to([0, -0.8, 0])
            self.play(TransformFromCopy(mid_now, eq[0]), TransformFromCopy(mid_old, eq[2]),
                      time_span(FadeIn(eq[1]), 0.8, 1.5), time_span(FadeIn(eq[3]), 1.2, 1.9),
                      time_span(FadeIn(eq[4], shift=0.2 * LEFT), 1.2, 1.9), run_time=1.9)
            c.wait_until("add up")
            self.play(FlashAround(eq[4], color=GOLD, time_width=1.5), run_time=1.1)
