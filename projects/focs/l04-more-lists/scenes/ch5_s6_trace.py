"""Chapter 5, scene 6: three ways to make four (the tree for change [2; 1] 4). Clips c5.trace.1 – c5.trace.4.

Tree (for `change [2; 1] 4`), node / edge / label constants matched to s3 (ch5_s3_choices):
  node    Mono 30 "amount, till" (amount GOLD, till TEAL) in a BLUE RoundedRectangle, corner 0.15,
          stroke 3, height 0.62, width text + 2 x 0.25. Collapsed node: an offset (0.13) BLUE L-shaped card edge.
  levels  (this scene's own) y 1.75 / -0.2 / -2.15. Root x 0.8; level 1 x -2.5 ("2, [2; 1]"), 4.6 ("4, [1]");
          level 2 x -4.8 ("0, [2; 1]"), 0.0 ("2, [1]").
  edges   FG stroke 4, parent bottom centre ±0.35 → child top centre; labels T 30 ("use 2" / "skip 2",
          coin GOLD), s3's rule: steep edges LEFT/RIGHT of the midpoint (buff 0.18, raised 0.1); shallow
          edges (|dx| > 1.5|dy|) at 0.65 of the way down, UL/UR buff 0.06.
  results Mono 30 GREEN, 0.8 under leaf / collapsed nodes; DIM T 28 "ones only: one way".
          Join beside "2, [2; 1]" (RIGHT, buff 0.25, as s3's results); the root's join in a top band centred (1.6, 3.2).
Solutions: coin(v) (ch1) scaled 0.6·s in TEAL boxes (corner 0.1, stroke 3, pad 0.12·s, buff 0.1·s);
  lists in a TEAL frame (corner 0.15, stroke 4, pad 0.2·s, buff 0.2·s).
  allc shot (s5's pair, s5's scale 1.2): left edge x -6.45, centre y 2.15; the hovering 2 disc
  (coin scaled 0.72) at (-1.15, 2.35); a copy lands on the front of each box in turn.
  final three boxes = s2's {example}: solutions([[2, 2], [2, 1, 1], [1, 1, 1, 1]]).scale(1.48) at (0, 0)
  (9.85 x 1.69), the answer line (GREEN Mono 32, same glyphs as Code 32) at (0, -1.55).
  c5.trace.4: the boxes rise to y 1.35, braces + "use 2"/"skip 2" above; the answer becomes the reply's
  second line in place, call + "- : int list list =" above it.
Replies are shown as OCaml 5.4.1 prints them with Format margin 40 (checked), so they fit at Code 32.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, FlashUnder, TransformMatchingStrings, select, set_backstroke, time_span  # noqa: E402,F401
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

COIN_R = 0.42                # ch1's coin
COIN_LABEL = 34
NODE = 30                    # node text
RES = 30                     # result text

CALL4 = "change [2; 1] 4"
PREFIX = "- : int list list ="
ANSWER = "[[2; 2]; [2; 1; 1]; [1; 1; 1; 1]]"
CALL5 = "change [5; 2; 1] 6"
REPLY5 = ("- : int list list =\n"
          "[[5; 1]; [2; 2; 2]; [2; 2; 1; 1];\n"
          " [2; 1; 1; 1; 1]; [1; 1; 1; 1; 1; 1]]")
SOLS5 = ["[5; 1]", "[2; 2; 2]", "[2; 2; 1; 1]", "[2; 1; 1; 1; 1]", "[1; 1; 1; 1; 1; 1]"]
GREEDY = "- : int list = [5; 1]"

BAND = (1.6, 3.2)            # the root's join
ALLC_S = 1.2                 # s5's scale for the pair
ALLC_LEFT, ALLC_Y = -6.45, 2.15
HOVER = (-1.15, 2.35)


# ── shared looks (copied from ch1_s1_hook / the ch5 spec) ─────────────────────────
def coin(v, r=COIN_R):
    """A coin: GOLD disc (stroke 4, fill 0.15) with its value in GOLD serif."""
    disc = Circle(radius=r).set_stroke(GOLD, 4).set_fill(GOLD, opacity=0.15)
    lab = T(str(v), size=COIN_LABEL, color=GOLD).move_to(disc)
    return VGroup(disc, lab)


def solution(vals, s=1.0):
    """One solution: coins in a row inside a TEAL box (empty: a coin-height square)."""
    d = 2 * COIN_R * 0.6 * s
    coins = VGroup(*[coin(v).scale(0.6 * s) for v in vals])
    if vals:
        coins.arrange(RIGHT, buff=0.1 * s)
    w = (coins.width if vals else d) + 0.24 * s
    rect = RoundedRectangle(corner_radius=0.1 * s, width=w, height=d + 0.24 * s).set_stroke(TEAL, 3)
    if vals:
        rect.move_to(coins)
    return VGroup(rect, coins)


def solutions(lists, s=1.0):
    """A list of solutions: solution boxes in a row inside a bigger TEAL box."""
    sols = VGroup(*[solution(v, s) for v in lists]).arrange(RIGHT, buff=0.2 * s)
    frame = RoundedRectangle(corner_radius=0.15 * s, width=sols.width + 0.4 * s,
                             height=sols.height + 0.4 * s).set_stroke(TEAL, 4).move_to(sols)
    return VGroup(frame, sols)


def allc_state(lists):
    return solutions(lists).scale(ALLC_S).move_to([0, ALLC_Y, 0]).align_to([ALLC_LEFT, 0, 0], LEFT)


def node(amt, till, at):
    txt = Mono(f"{amt}, {till}", NODE)
    n = len(str(amt))
    txt[:n].set_color(GOLD)
    txt[n + 1:].set_color(TEAL)
    box = RoundedRectangle(corner_radius=0.15, width=txt.width + 2 * 0.25, height=0.62).set_stroke(BLUE, 3)
    txt.move_to(box)
    return VGroup(box, txt).move_to(at)


def stack_mark(nd, d=0.13):
    """The edge of a second card behind a node: this node stands for a whole subtree."""
    b = nd[0]
    x0, x1 = b.get_left()[0], b.get_right()[0]
    y0, y1 = b.get_bottom()[1], b.get_top()[1]
    return VMobject().set_points_as_corners(
        [[x1 + d, y1 - 0.2, 0], [x1 + d, y0 - d, 0], [x0 + 0.2, y0 - d, 0]]).set_stroke(BLUE, 3, opacity=0.6)


def edge(parent, child, side):
    a = parent[0].get_bottom() + RIGHT * 0.35 * side      # s3's EDGE_OFF
    b = child[0].get_top()
    return Line(a, b).set_stroke(FG, 4)


def edge_label(e, word, v, side):
    """s3's placement: steep edges beside the midpoint, shallow ones near the child, outside."""
    lab = T(f"{word} {v}", 30)
    select(lab, str(v))[0].set_color(GOLD)
    d = e.get_end() - e.get_start()
    if abs(d[0]) > 1.5 * abs(d[1]):
        lab.next_to(e.point_from_proportion(0.65), UL if side < 0 else UR, buff=0.06)
    else:
        lab.next_to(e.point_from_proportion(0.5), LEFT if side < 0 else RIGHT, buff=0.18).shift(0.1 * UP)
    return lab


def result(s, nd, size=RES):
    return Mono(s, size, GREEN).move_to(nd.get_center() + DOWN * 0.8)


def row_parts(full_str, parts, colors, center, size=RES):
    """A row as one Mono, plus each part as its own Mono sitting exactly where it is in the row."""
    full = Mono(full_str, size).move_to([*center, 0])
    out, pos = [], 0
    for p, col in zip(parts, colors):
        i = full_str.index(p, pos)
        g0 = sum(not ch.isspace() for ch in full_str[:i])
        g1 = g0 + sum(not ch.isspace() for ch in p)
        full[g0:g1].set_color(col)
        out.append(Mono(p, size, col).move_to(full[g0:g1].get_center()))
        pos = i + len(p)
    return full, out


def mono_part(mono, s):
    return select(mono, s)[0]


class Trace(NarratedScene):
    def construct(self):
        self.build()
        self.root_and_split()   # c5.trace.1
        self.left_side()        # c5.trace.2
        self.join_up()          # c5.trace.3
        self.reply()            # c5.trace.4
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def build(self):
        self.R = node(4, "[2; 1]", [0.8, 1.75, 0])
        self.L = node(2, "[2; 1]", [-2.5, -0.2, 0])
        self.RT = node(4, "[1]", [4.6, -0.2, 0])
        self.LL = node(0, "[2; 1]", [-4.8, -2.15, 0])
        self.LR = node(2, "[1]", [0.0, -2.15, 0])
        self.eRL = edge(self.R, self.L, -1)
        self.lRL = edge_label(self.eRL, "use", 2, -1)
        self.eRR = edge(self.R, self.RT, 1)
        self.lRR = edge_label(self.eRR, "skip", 2, 1)
        self.eLL = edge(self.L, self.LL, -1)
        self.lLL = edge_label(self.eLL, "use", 2, -1)
        self.eLR = edge(self.L, self.LR, 1)
        self.lLR = edge_label(self.eLR, "skip", 2, 1)
        self.LL_RES = result("[[]]", self.LL)
        self.LR_RES = result("[[1; 1]]", self.LR)
        self.LR_NOTE = T("ones only: one way", 28, DIM).next_to(self.LR_RES, RIGHT, buff=0.45)
        self.RT_RES = result("[[1; 1; 1; 1]]", self.RT)
        self.RT_NOTE = T("ones only: one way", 28, DIM).next_to(self.RT_RES, DOWN, buff=0.22)
        self.LR_STACK = stack_mark(self.LR)
        self.RT_STACK = stack_mark(self.RT)

    # ── c5.trace.1: the root, and its two choices ─────────────────────────────────
    def root_and_split(self):
        R, L, RT = self.R, self.L, self.RT
        with self.say("c5.trace.1") as c:
            # "Now let's trace a case with more than one answer."
            call = Code(CALL4, 48).move_to(UP * 0.3)
            self.play(FadeIn(call, shift=0.3 * UP), run_time=1.0)
            # "Change for four, with twos and ones."
            c.wait_until("Change for four")
            off = min(c.until("with twos and ones"), 1.6)
            self.play(time_span(FlashUnder(call.find("4"), color=GOLD), 0, 1.1),
                      time_span(FlashUnder(call.find("[2; 1]"), color=TEAL), off, off + 1.1),
                      run_time=off + 1.1)
            # {root} "The two fits, so we can use it, or skip it."
            c.wait_until("root")
            self.play(TransformMatchingStrings(call, R[1]),
                      time_span(Create(R[0]), 0.5, 1.5), run_time=1.5)
            settle(self, R)
            c.wait_until("so we can use it")
            self.play(FlashAround(R[1][3], color=YELLOW, buff=0.08), run_time=1.2)
            # {use} "We can use the two, leaving two, still with twos and ones."
            c.wait_until("use")
            self.grow_child(R, L, self.eRL, self.lRL, 1.9)
            # {skip} "Or we can skip it, and make four from ones alone."
            c.wait_until("skip")
            self.grow_child(R, RT, self.eRR, self.lRR, 1.9)

    def grow_child(self, parent, child, e, lab, rt, extra=()):
        self.play(time_span(Create(e), 0, 0.8),
                  time_span(FadeIn(lab, shift=0.2 * DOWN), 0.4, 1.2),
                  time_span(ReplacementTransform(parent[0].copy(), child[0]), 0.5, rt),
                  time_span(TransformMatchingStrings(parent[1].copy(), child[1]), 0.5, rt),
                  *extra, run_time=rt)
        settle(self, child)

    def born(self, parent, child, rt, extra=()):
        self.play(ReplacementTransform(parent[0].copy(), child[0]),
                  TransformMatchingStrings(parent[1].copy(), child[1]), *extra, run_time=rt)
        settle(self, child)

    # ── c5.trace.2: the left side, all the way down and back ─────────────────────
    def left_side(self):
        L, LL, LR = self.L, self.LL, self.LR
        rowL, (p1, p2, p3) = row_parts("[[2]] @ [[1; 1]]", ["[[2]]", "@", "[[1; 1]]"],
                                       [GREEN, GOLD, GREEN], (0, 0))
        v = L.get_right() + RIGHT * 0.25 - rowL.get_left()   # beside "2, [2; 1]", as s3 writes results
        for m in (rowL, p1, p2, p3):
            m.shift(v[0] * RIGHT + (L.get_y() - rowL.get_y()) * UP)
        self.LRES = Mono("[[2]; [1; 1]]", RES, GREEN).next_to(L, RIGHT, buff=0.25)
        with self.say("c5.trace.2") as c:
            # {left} "Take the left side first."
            self.play(*[restyle(m, op=0.3) for m in (self.eRR, self.lRR, self.RT)],
                      FlashAround(L, color=YELLOW, buff=0.12), run_time=1.3)
            # "We owe two, with twos and ones still allowed, and it splits again."
            c.wait_until("We owe two")
            off = min(c.until("with twos and ones"), 1.8)
            self.play(time_span(FlashUnder(L[1][0], color=GOLD), 0, 1.0),
                      time_span(FlashUnder(L[1][2:], color=TEAL), off, off + 1.1),
                      run_time=off + 1.1)
            c.wait_until("splits again")
            rt = max(0.7, min(1.3, 0.95 * c.until("zero")))
            self.play(time_span(Create(self.eLL), 0, 0.7 * rt), time_span(Create(self.eLR), 0, 0.7 * rt),
                      time_span(FadeIn(self.lLL, shift=0.2 * DOWN), 0.35 * rt, rt),
                      time_span(FadeIn(self.lLR, shift=0.2 * DOWN), 0.35 * rt, rt), run_time=rt)
            # {zero} "Using a two reaches zero, which gives the list holding nil."
            c.wait_until("zero")
            self.born(L, LL, 1.5)
            c.wait_until("which gives the list holding nil")
            self.play(FadeIn(self.LL_RES, shift=0.25 * DOWN), run_time=1.0)
            # "All-see puts a two on that empty solution, so we get a single two."
            c.wait_until("puts a two")
            rising = self.LL_RES.copy()
            d2 = coin(2).scale(0.6).move_to(p1.get_center())
            start = mono_part(self.lLL, "2").get_center()
            self.play(rising.animate.move_to(p1),
                      FadeIn(d2, shift=d2.get_center() - start), run_time=1.6)
            c.wait_until("so we get a single two")
            self.play(Transform(rising[0], p1[0]), Transform(rising[1], p1[1]),
                      Transform(rising[2], p1[3]), Transform(rising[3], p1[4]),
                      FadeTransform(d2, p1[2]), run_time=1.0)
            self.remove(rising, p1[2])
            self.add(p1)
            # {ones} "Skipping the two means making two from ones, and that gives one plus one."
            c.wait_until("ones")
            self.born(L, LR, 1.5, extra=[time_span(Create(self.LR_STACK), 0.8, 1.5)])
            c.wait_until("that gives one plus one")
            self.play(FadeIn(self.LR_RES, shift=0.25 * DOWN),
                      time_span(FadeIn(self.LR_NOTE), 0.4, 1.1), run_time=1.1)
            # {joinleft} "Append them, and change for two has two solutions, ..."
            c.wait_until("joinleft")
            self.play(TransformFromCopy(self.LR_RES, p3),
                      time_span(FadeIn(p2, scale=0.5), 0.6, 1.5), run_time=1.5)
            c.wait_until("has two solutions")
            self.remove(p1, p2, p3)
            self.add(rowL)
            self.play(TransformMatchingStrings(rowL, self.LRES), run_time=1.4)
            # "... a single two, and one plus one."
            c.wait_until("a single two", nth=1)
            off = max(0.0, min(c.until("and one plus one"), 1.2))
            self.play(time_span(FlashUnder(mono_part(self.LRES, "[2]"), color=YELLOW), 0, 0.9),
                      time_span(FlashUnder(mono_part(self.LRES, "[1; 1]"), color=YELLOW), off, off + 0.9),
                      run_time=off + 0.9)

    # ── c5.trace.3: all-see on the top-left edge, the right side, the join ───────
    def join_up(self):
        RT = self.RT
        allc0 = allc_state([[2], [1, 1]])
        allc1 = allc_state([[2, 2], [1, 1]])
        allc2 = allc_state([[2, 2], [2, 1, 1]])
        hover = coin(2).scale(0.6 * ALLC_S).move_to([*HOVER, 0])
        band, (bl, bat, br) = row_parts("[[2; 2]; [2; 1; 1]] @ [[1; 1; 1; 1]]",
                                        ["[[2; 2]; [2; 1; 1]]", "@", "[[1; 1; 1; 1]]"],
                                        [GREEN, GOLD, GREEN], BAND)
        final = solutions([[2, 2], [2, 1, 1], [1, 1, 1, 1]]).scale(1.48).move_to(ORIGIN)   # s2's {example}
        ans = Mono(ANSWER, 32, GREEN).move_to([0, -1.55, 0])
        self.final, self.ans = final, ans
        lower_left = [self.eLL, self.lLL, self.LL, self.LL_RES, self.eLR, self.lLR, self.LR,
                      self.LR_STACK, self.LR_RES, self.LR_NOTE]
        with self.say("c5.trace.3") as c:
            # {allc} "That's exactly what we gave all-see a moment ago."
            self.play(FadeTransform(self.LRES.copy(), allc0),
                      time_span(FadeIn(hover, target_position=mono_part(self.lRL, "2"), scale=0.5), 0.6, 1.6),
                      *[restyle(m, op=0.35) for m in lower_left], run_time=1.8)
            # {front} "Back on the top-left edge, a two goes onto the front of each, ..."
            c.wait_until("front")
            self.coin_on_front(allc0, allc1, 0, hover, 1.6)
            c.wait_until("of each")
            self.coin_on_front(allc1, allc2, 1, hover, 1.3)
            # "... giving two plus two, and two plus one plus one."
            c.wait_until("giving two plus two")
            self.play(FadeTransform(allc2.copy(), bl), FadeOut(hover),
                      FlashAround(allc2[1][0], color=YELLOW), run_time=1.3)
            c.wait_until("and two plus one plus one")
            self.play(FlashAround(allc2[1][1], color=YELLOW),
                      FlashUnder(mono_part(bl, "[2; 1; 1]"), color=YELLOW), run_time=1.2)
            # {right} "On the right, four from ones alone has one way, four ones."
            c.wait_until("right")
            self.play(*[restyle(m, op=1) for m in (self.eRR, self.lRR, RT)],
                      time_span(Create(self.RT_STACK), 0.4, 1.1),
                      time_span(FadeIn(self.RT_NOTE), 0.7, 1.5), run_time=1.5)
            c.wait_until("has one way")
            self.play(FadeIn(self.RT_RES, shift=0.25 * DOWN), run_time=1.0)
            # {join} "The at sign appends the two sides."
            c.wait_until("join")
            self.play(TransformFromCopy(self.RT_RES, br, path_arc=PI / 4),
                      time_span(FadeIn(bat, scale=0.5), 0.6, 1.4),
                      time_span(FlashAround(bat, color=GOLD), 1.4, 2.3), run_time=2.3)
            # {answer} "Three ways."
            c.wait_until("answer")
            self.remove(bl, bat, br)
            self.add(band)
            keep = [band, allc2, self.RT_RES]
            gone = [m for m in self.mobjects if all(m is not k for k in keep)]
            alias = VGroup(final[0], VGroup(final[1][0], final[1][1]))
            self.play(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.04),
                      TransformMatchingStrings(band, ans),
                      ReplacementTransform(allc2, alias),
                      FadeTransform(self.RT_RES, final[1][2]), run_time=1.6)
            self.remove(alias, final[1][2])
            self.add(final)
            # "Two, two."  "Two, one, one."  "And one, one, one, one."
            for i, (cue, part) in enumerate([("Two, two", "[2; 2]"), ("Two, one, one", "[2; 1; 1]"),
                                             ("And one", "[1; 1; 1; 1]")]):
                c.wait_until(cue)
                self.play(FlashAround(final[1][i], color=YELLOW, buff=0.1),
                          FlashUnder(mono_part(ans, part), color=YELLOW), run_time=1.2)

    def coin_on_front(self, cur, nxt, recv, hover, rt):
        """The hovering 2 disc copies onto the front of solution `recv`; the boxes make room."""
        anims = [Transform(cur[0], nxt[0])]
        new_coin = None
        for i, (s0, s1) in enumerate(zip(cur[1], nxt[1])):
            anims.append(Transform(s0[0], s1[0]))
            targets = list(s1[1])
            if i == recv:
                new_coin, targets = targets[0], targets[1:]
            anims += [Transform(a, b) for a, b in zip(s0[1], targets)]
        anims.append(ReplacementTransform(hover.copy(), new_coin, path_arc=PI / 3))
        self.play(*anims, run_time=rt)
        self.remove(cur, new_coin)
        self.add(nxt)

    # ── c5.trace.4: OCaml agrees; the order; three coins ─────────────────────────
    def reply(self):
        final, ans = self.final, self.ans
        call4 = Code(CALL4, 32)
        rep4 = Code(PREFIX + "\n" + ANSWER, 32)
        VGroup(call4, rep4).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        rep4.shift(ans.get_center() - rep4.line(1).get_center())      # the answer stays put as line 2
        call4.align_to(rep4, LEFT).next_to(rep4, UP, buff=0.22, coor_mask=np.array([0, 1, 0]))
        pre4 = Code(PREFIX, 32).move_to(rep4.line(0))
        val4 = Code(ANSWER, 32).move_to(rep4.line(1))
        RISE = UP * 1.35
        top = final[0].get_top()[1] + RISE[1]
        s0, s1, s2 = final[1]
        br_use = span_brace(np.array([s0.get_left()[0], top, 0]), np.array([s1.get_right()[0], top, 0]),
                            direction=UP)
        br_skip = span_brace(np.array([s2.get_left()[0], top, 0]), np.array([s2.get_right()[0], top, 0]),
                             direction=UP)
        lab_use = T("use 2", 32).next_to(br_use, UP, buff=0.12)
        lab_skip = T("skip 2", 32).next_to(br_skip, UP, buff=0.12)
        for lab in (lab_use, lab_skip):
            select(lab, "2")[0].set_color(GOLD)

        call5 = Code(CALL5, 34)
        rep5 = Code(REPLY5, 32)
        blk5 = VGroup(call5, rep5).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        glab = T("greedy change:", 30, DIM)
        grep = Code(GREEDY, 32)
        grep.find("[5; 1]").set_color(YELLOW)
        grow = VGroup(glab, grep).arrange(RIGHT, buff=0.35)
        grow.next_to(blk5, DOWN, buff=0.75, aligned_edge=LEFT)
        VGroup(blk5, grow).move_to([0, 0.15, 0])
        ways = T("5 ways", 48, GOLD).move_to([3.5, call5.get_y(), 0])

        with self.say("c5.trace.4") as c:
            # {reply} "OCaml agrees."
            c.wait_until("reply")
            self.play(time_span(final.animate.shift(RISE), 0, 1.0),
                      time_span(ReplacementTransform(ans, val4), 0.2, 1.2),
                      time_span(FadeIn(call4, shift=0.2 * DOWN), 0.6, 1.5),
                      time_span(FadeIn(pre4), 0.7, 1.5), run_time=1.5)
            # {order} "Notice the order."
            c.wait_until("order")
            self.play(GrowFromCenter(br_use), GrowFromCenter(br_skip),
                      time_span(FadeIn(lab_use, shift=0.2 * DOWN), 0.4, 1.2),
                      time_span(FadeIn(lab_skip, shift=0.2 * DOWN), 0.4, 1.2), run_time=1.2)
            # "Solutions with larger coins come first, ..."
            c.wait_until("larger coins")
            self.play(FlashAround(s0[1][0], color=GOLD, buff=0.06),
                      FlashAround(s1[1][0], color=GOLD, buff=0.06), run_time=1.2)
            # "... because the use branch goes in front of the skip branch."
            c.wait_until("use branch")
            self.play(FlashAround(lab_use, color=YELLOW), run_time=1.0)
            c.wait_until("skip branch")
            self.play(FlashAround(lab_skip, color=YELLOW), run_time=0.9)
            # {five} "With all three coins, five, two and one, there are five ways to make six, ..."
            c.wait_until("five")
            sweep_clear(self, time_span(FadeIn(call5, shift=0.2 * UP), 0.6, 1.4), run_time=1.4)
            self.play(FadeIn(rep5, shift=0.2 * UP), run_time=1.2)
            c.wait_until("five ways")
            n = len(SOLS5)
            self.play(*[time_span(FlashUnder(rep5.find(s), color=GOLD), 0.3 * i, 0.3 * i + 0.9)
                        for i, s in enumerate(SOLS5)],
                      time_span(FadeIn(ways, shift=0.2 * DOWN), 0.3 * (n - 1), 0.3 * (n - 1) + 0.9),
                      run_time=0.3 * (n - 1) + 0.9)
            # "... from five plus one, down to six ones."
            c.wait_until("from five plus one")
            self.play(FlashAround(rep5.find(SOLS5[0]), color=YELLOW), run_time=1.0)
            c.wait_until("six ones")
            self.play(FlashAround(rep5.find(SOLS5[-1]), color=YELLOW), run_time=1.0)
            # {greedy} "Five plus one comes first, and that's exactly what greedy would have given."
            c.wait_until("greedy")
            self.play(*recolor(rep5.find(SOLS5[0]), YELLOW),
                      FlashAround(rep5.find(SOLS5[0]), color=YELLOW),
                      time_span(FadeIn(grow, shift=0.2 * UP), 0.4, 1.4), run_time=1.4)
            c.wait_until("exactly what greedy")
            self.play(FlashAround(rep5.find(SOLS5[0]), color=YELLOW),
                      FlashAround(grep.find("[5; 1]"), color=YELLOW), run_time=1.2)
        self.wait(1.9)   # the last reply stays a moment after the line ends
