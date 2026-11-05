"""Chapter 1, scene 5: twenty questions with n! answers (the comparison lower bound). Clips c1.bound.1 – c1.bound.5.

Plan: three cards a, b, c become the six orders (2 x 3 grid, 3! = 6); each order gets its
rearrangement diagram; the orders shrink to a row, a comparison card pair "a <= ? b" with yes/no
buttons asks the question; that question becomes the root of the decision tree, the orders drop
down its branches and become the six leaves (depth bracket "3 questions"). A cut at depth 2 gives
four answer boxes, two orders share a box, one comes out wrong, the third level grows back. The tree
shrinks to the corner and the general bound 2^{C(n)} >= n!, C(n) >= log2(n!) is derived.
Last shot: the boxed YELLOW bound and the log form under it, alone (scene 6 opens from them).
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403


PERMS = ["abc", "acb", "bac", "bca", "cab", "cba"]
GRID = {"abc": (-4.2, 2.6), "acb": (0.0, 2.6), "bac": (4.2, 2.6),
        "bca": (-4.2, -0.35), "cab": (0.0, -0.35), "cba": (4.2, -0.35)}

SC = 0.7                       # compact order scale (letters 64 -> 45)
TX = -0.25                     # tree x offset
Y0, Y1, Y2, Y3 = 2.15, 0.65, -0.7, -2.0
NODE_H = 0.78
LEAF_TOP = 0.49 * SC            # half-height of a compact order box
ROW_Y = 3.12
ROW_X = {"abc": TX - 4.7, "acb": TX - 3.1, "cab": TX - 1.5,
         "bac": TX + 1.5, "bca": TX + 3.1, "cba": TX + 4.7}
LEAF = {"abc": (TX - 4.7, Y2), "acb": (TX - 2.35, Y3), "cab": (TX - 0.65, Y3),
        "bac": (TX + 1.5, Y2), "bca": (TX + 3.85, Y3), "cba": (TX + 5.55, Y3)}
NODE = {"root": (TX, Y0, "a", "b"), "L1": (TX - 3.1, Y1, "b", "c"), "R1": (TX + 3.1, Y1, "a", "c"),
        "L2": (TX - 1.5, Y2, "a", "c"), "R2": (TX + 4.7, Y2, "b", "c")}
SLOT_X = [TX - 4.7, TX - 1.5, TX + 1.5, TX + 4.7]
BX = -6.35                     # depth bracket x


class Order(VGroup):
    """One arrangement of a, b, c: three YELLOW letters (baselines aligned) in a rounded box."""

    def __init__(self, perm, fs=64, pitch=0.62, stroke=BLUE, color=YELLOW):
        super().__init__()
        self.perm = perm
        self.letters = VGroup(*[MathTex(ch, font_size=fs, color=color) for ch in perm])
        for i, m in enumerate(self.letters):
            m.move_to(RIGHT * (i - 1) * pitch)
            m.align_to(ORIGIN, DOWN)
        xh = min(m.height for m in self.letters)
        self.letters.shift(DOWN * xh / 2)
        self.box = RoundedRectangle(corner_radius=0.14, width=2 * pitch + 0.8, height=0.98)
        self.box.set_stroke(stroke, 3).set_fill(BG, 1).move_to(UP * 0.06)
        self.add(self.box, self.letters)

    def letter(self, ch):
        return self.letters[self.perm.index(ch)]


class Node(VGroup):
    """A question node "p <= q ?"."""

    def __init__(self, p, q, fs=48):
        super().__init__()
        self.tex = MathTex(p, r"\le", q, "?", font_size=fs)
        self.tex[0].set_color(YELLOW)
        self.tex[2].set_color(YELLOW)
        self.box = RoundedRectangle(corner_radius=0.14, width=self.tex.width + 0.5, height=NODE_H)
        self.box.set_stroke(FG, 2.5).set_fill(BG, 1).move_to(self.tex)
        self.add(self.box, self.tex)


def apply_op(m, op):
    """Set the opacity of one of our pieces (Order, Node, or a stroke-only line) in place."""
    if isinstance(m, Order):
        m.box.set_stroke(opacity=op).set_fill(opacity=op)
        m.letters.set_fill(opacity=op)
    elif isinstance(m, Node):
        m.box.set_stroke(opacity=op).set_fill(opacity=op)
        m.tex.set_fill(opacity=op)
    else:
        m.set_stroke(opacity=op)
    return m


def fade_to(m, op, shift=None):
    m.generate_target()
    apply_op(m.target, op)
    if shift is not None:
        m.target.shift(shift)
    return MoveToTarget(m)


def edge(parent_xy, child_xy, child_is_node, color):
    start = np.array([parent_xy[0], parent_xy[1] - NODE_H / 2, 0])
    end = np.array([child_xy[0], child_xy[1] + (NODE_H / 2 if child_is_node else LEAF_TOP), 0])
    return Line(start, end, stroke_width=3, color=color)


def edge_label(e, word, color):
    lab = T(word, 30, color)
    s, t = e.get_start(), e.get_end()
    d = (t - s) / np.linalg.norm(t - s)
    n = np.array([-d[1], d[0], 0])
    if n[1] < 0:
        n = -n
    lab.move_to((s + t) / 2 + 0.34 * n)
    return set_backstroke(lab)


def bracket(top, bot, x=BX, color=GOLD):
    b = VMobject()
    b.set_points_as_corners([[x + 0.2, top, 0], [x, top, 0], [x, bot, 0], [x + 0.2, bot, 0]])
    return b.set_stroke(color, 4).set_fill(opacity=0)


def depth_label(n):
    lab = T(f"{n} questions", 32, GOLD)
    lab.move_to([0, 3.05, 0]).align_to([BX, 0, 0], LEFT)
    return lab


class Bound(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c1.bound.1
    def clip1(self):
        with self.say("c1.bound.1") as c:
            frames, letters = [], []
            for i, ch in enumerate("abc"):
                f = RoundedRectangle(corner_radius=0.18, width=1.5, height=2.0)
                f.set_stroke(BLUE, 4).set_fill(BG, 1).move_to([(i - 1) * 2.4, 0.4, 0])
                frames.append(f)
                letters.append(MathTex(ch, font_size=120, color=YELLOW))
            xh = letters[0].height
            for l, f in zip(letters, frames):
                l.move_to(f)
                l.align_to(f.get_center() + DOWN * xh / 2, DOWN)
            self.play(*[time_span(FadeIn(f, shift=0.3 * DOWN), 0.2 * i, 0.2 * i + 1.0)
                        for i, f in enumerate(frames)])
            for l, cue, nxt in zip(letters, ["ay", "bee", "see"], ["bee", "see", "six"]):
                c.wait_until(cue)
                self.play(FadeIn(l, scale=0.5), run_time=min(0.7, 0.8 * c.until(nxt)))

            # {six}: the cards become the first order
            c.wait_until("six")
            self.orders = O = {p: Order(p).move_to([*GRID[p], 0]) for p in PERMS}
            o0 = O["abc"]
            ghosts = [o0.box.copy() for _ in range(3)]
            self.play(*[ReplacementTransform(f, g) for f, g in zip(frames, ghosts)],
                      *[ReplacementTransform(l, o0.letters[i]) for i, l in enumerate(letters)],
                      run_time=1.1)
            self.remove(*ghosts)
            settle(self, o0)
            # ... and the other five, letters flying out of the first
            anims = []
            for k, p in enumerate(PERMS[1:]):
                o, s = O[p], 0.15 * k
                anims.append(time_span(FadeIn(o.box), s, s + 0.9))
                anims += [time_span(TransformFromCopy(o0.letter(ch), o.letters[j]), s, s + 1.0)
                          for j, ch in enumerate(p)]
            self.play(*anims)
            for p in PERMS[1:]:
                settle(self, O[p])

            # {list}: here are all six
            c.wait_until("list")
            self.play(*[time_span(FlashAround(O[p], time_width=1.5), 0.12 * k, 0.12 * k + 1.0)
                        for k, p in enumerate(PERMS)])

            # 3 x 2 x 1 = 6, built with the words
            self.f3 = f3 = MathTex("3!", "=", "3", r"\times", "2", r"\times", "1", "=", "6",
                                   font_size=60, color=GOLD).move_to([0, -3.1, 0])
            steps = [("three choices", [2]), ("two for the second", [3, 4]),
                     ("one for the last", [5, 6]), ("three factorial", [0, 1, 7, 8])]
            for k, (cue, idx) in enumerate(steps):
                c.wait_until(cue)
                nxt = steps[k + 1][0] if k + 1 < len(steps) else None
                self.play(*[FadeIn(f3[i], shift=0.2 * DOWN) for i in idx],
                          run_time=min(0.9, 0.7 * c.until(nxt)))
            settle(self, f3)

    # ------------------------------------------------------------------ c1.bound.2
    def clip2(self):
        O = self.orders
        with self.say("c1.bound.2") as c:
            # {must}: each order's own rearrangement into a b c
            diag, anims = [], []
            for k, p in enumerate(PERMS):
                o = O[p]
                tgt = Order("abc", stroke=DIM, color=DIM).scale(0.8).move_to(o.get_center() + DOWN * 1.65)
                arrows = []
                for j, ch in enumerate(p):
                    start = [o.letters[j].get_x(), o.box.get_bottom()[1] - 0.06, 0]
                    end = [tgt.letter(ch).get_x(), tgt.box.get_top()[1] + 0.06, 0]
                    arrows.append(Arrow(start, end, buff=0, stroke_width=3, tip_length=0.16,
                                        max_tip_length_to_length_ratio=0.35, color=FG))
                s = 0.22 * k
                anims.append(time_span(FadeIn(tgt), s, s + 0.9))
                anims += [time_span(GrowArrow(a), s + 0.3, s + 1.2) for a in arrows]
                diag += [tgt, *arrows]
            self.play(*anims)

            # {only}: the orders shrink to a row; the question
            c.wait_until("only")
            self.play(*[FadeOut(m) for m in diag], FadeOut(self.f3),
                      *[O[p].animate.scale(SC).move_to([ROW_X[p], ROW_Y, 0]) for p in PERMS],
                      run_time=1.5)
            self.qf = [RoundedRectangle(corner_radius=0.16, width=1.3, height=1.7)
                       .set_stroke(BLUE, 4).set_fill(BG, 1).move_to([x, 0.75, 0]) for x in (-2.1, 2.1)]
            self.ql = [MathTex(ch, font_size=100, color=YELLOW) for ch in "ab"]
            xh = self.ql[0].height
            for l, f in zip(self.ql, self.qf):
                l.move_to(f)
                l.align_to(f.get_center() + DOWN * xh / 2, DOWN)
            self.qle = MathTex(r"\le", "?", font_size=96).move_to([0, 0.75, 0])
            c.wait_until("is this item")
            self.play(*[FadeIn(f) for f in self.qf], *[FadeIn(l) for l in self.ql], Write(self.qle),
                      run_time=min(1.2, 0.8 * c.until("yesno")))

            # {yesno}: two buttons
            c.wait_until("yesno")
            self.btn = {}
            for word, col, x in (("yes", GREEN, -2.1), ("no", RED, 2.1)):
                fr = RoundedRectangle(corner_radius=0.2, width=1.9, height=0.85)
                fr.set_stroke(col, 3).set_fill(col, 0.15).move_to([x, -1.2, 0])
                self.btn[word] = (fr, T(word, 40, col).move_to(fr))
            self.play(*[time_span(FadeIn(m, shift=0.2 * UP), s, s + 0.8)
                        for s, w in ((0.0, "yes"), (0.4, "no")) for m in self.btn[w]])

            # {twenty}: twenty questions, a million things
            c.wait_until("twenty")
            self.cap = T("twenty questions: about a million things", 36).move_to([0, -2.45, 0])
            self.play(FadeIn(self.cap, shift=0.2 * UP), run_time=1.0)
            c.wait_until("about a million")
            self.p20 = MathTex(r"2^{20} = 1{,}048{,}576", font_size=52, color=GOLD).move_to([0, -3.2, 0])
            self.play(Write(self.p20), run_time=1.2)

    # ------------------------------------------------------------------ c1.bound.3
    def clip3(self):
        O = self.orders
        with self.say("c1.bound.3") as c:
            self.nodes = N = {k: Node(v[2], v[3]).move_to([v[0], v[1], 0]) for k, v in NODE.items()}
            root = N["root"]
            # {root}: the question becomes the root
            g = root.box.copy()
            self.play(ReplacementTransform(self.qf[0], root.box), ReplacementTransform(self.qf[1], g),
                      ReplacementTransform(self.ql[0], root.tex[0]), ReplacementTransform(self.ql[1], root.tex[2]),
                      ReplacementTransform(self.qle[0], root.tex[1]), ReplacementTransform(self.qle[1], root.tex[3]),
                      run_time=1.6)
            self.remove(g)
            self.remove(*self.qle.get_family())
            settle(self, root)

            xy = {k: v[:2] for k, v in NODE.items()}
            xy.update(LEAF)
            self.E = E = {
                ("root", "L1"): edge(xy["root"], xy["L1"], True, GREEN),
                ("root", "R1"): edge(xy["root"], xy["R1"], True, RED),
                ("L1", "abc"): edge(xy["L1"], xy["abc"], False, GREEN),
                ("L1", "L2"): edge(xy["L1"], xy["L2"], True, RED),
                ("L2", "acb"): edge(xy["L2"], xy["acb"], False, GREEN),
                ("L2", "cab"): edge(xy["L2"], xy["cab"], False, RED),
                ("R1", "bac"): edge(xy["R1"], xy["bac"], False, GREEN),
                ("R1", "R2"): edge(xy["R1"], xy["R2"], True, RED),
                ("R2", "bca"): edge(xy["R2"], xy["bca"], False, GREEN),
                ("R2", "cba"): edge(xy["R2"], xy["cba"], False, RED),
            }
            self.labs = {"yes": edge_label(E[("root", "L1")], "yes", GREEN),
                         "no": edge_label(E[("root", "R1")], "no", RED)}

            # {split}: yes -> three orders, no -> the other three
            for word, kid, group, cue, nxt in (("yes", "L1", ("abc", "acb", "cab"), "split", "and a no"),
                                               ("no", "R1", ("bac", "bca", "cba"), "and a no", "half")):
                c.wait_until(cue)
                fr, tx = self.btn[word]
                self.play(Create(E[("root", kid)]), ReplacementTransform(tx, self.labs[word]), FadeOut(fr),
                          *[O[p].animate.move_to([ROW_X[p], Y1, 0]) for p in group],
                          run_time=min(1.6, 0.75 * c.until(nxt)))

            # {half}
            c.wait_until("half")
            half = T("at best, each question rules out half", 36).move_to([0, -3.2, 0])
            self.play(FadeOut(self.cap), FadeOut(self.p20), FadeIn(half, shift=0.2 * UP), run_time=1.2)

            # {tree}: keep asking
            c.wait_until("tree")
            anims = [time_span(O[p].animate.move_to([*LEAF[p], 0]), 0, 1.3) for p in PERMS]
            anims += [time_span(FadeIn(N[k]), 0.5, 1.3) for k in ("L1", "R1")]
            anims += [time_span(Create(E[k]), 0.7, 1.5)
                      for k in (("L1", "abc"), ("L1", "L2"), ("R1", "bac"), ("R1", "R2"))]
            anims += [time_span(FadeIn(N[k]), 1.1, 1.8) for k in ("L2", "R2")]
            anims += [time_span(Create(E[k]), 1.3, 2.1)
                      for k in (("L2", "acb"), ("L2", "cab"), ("R2", "bca"), ("R2", "cba"))]
            self.play(*anims)

            # {leaves}: six leaves glow GREEN
            c.wait_until("leaves")
            anims = []
            for p in PERMS:
                o = O[p]
                o.generate_target()
                o.target.box.set_stroke(GREEN, 4)
                anims += [MoveToTarget(o), FlashAround(o, color=GREEN, time_width=1.5)]
            self.play(*anims, run_time=1.4)

            # {depth}: longest path, 3 questions
            c.wait_until("depth")
            self.br = bracket(Y0 + NODE_H / 2, Y3 - LEAF_TOP)
            self.brl = depth_label(3)
            self.play(Create(self.br), FadeIn(self.brl, shift=0.2 * DOWN), FadeOut(half), run_time=1.4)

    # ------------------------------------------------------------------ c1.bound.4
    def clip4(self):
        O, N, E = self.orders, self.nodes, self.E
        low_edges = [E[k] for k in (("L2", "acb"), ("L2", "cab"), ("R2", "bca"), ("R2", "cba"))]
        deep = ["acb", "cab", "bca", "cba"]
        with self.say("c1.bound.4") as c:
            # {two}: cut under depth 2
            cut = DashedLine([BX + 0.4, -1.375, 0], [6.4, -1.375, 0], dash_length=0.16).set_stroke(GOLD, 3)
            self.play(Create(cut), Transform(self.br, bracket(Y0 + NODE_H / 2, Y2 - NODE_H / 2)),
                      Transform(self.brl, depth_label(2)),
                      *[fade_to(m, DIMMED) for m in (N["L2"], N["R2"], *low_edges, *[O[p] for p in deep])],
                      run_time=1.6)

            # {four}: four answer patterns
            c.wait_until("four")
            p22 = MathTex("2^2", "=", "4", font_size=60, color=GOLD).move_to([2.4, 2.95, 0])
            self.play(FadeOut(cut), FadeOut(N["L2"]), FadeOut(N["R2"]), *[FadeOut(e) for e in low_edges],
                      *[fade_to(O[p], DIMMED, shift=0.5 * DOWN) for p in deep],
                      Write(p22), run_time=1.3)
            boxes, labs = [], []
            for x, words in zip(SLOT_X, ["yes yes", "yes no", "no yes", "no no"]):
                b = RoundedRectangle(corner_radius=0.16, width=1.75, height=0.92)
                b.set_stroke(GOLD, 3).set_fill(opacity=0).move_to([x, Y2, 0])
                boxes.append(b)
                labs.append(T(words, 30, t2c={"yes": GREEN, "no": RED}).next_to(b, DOWN, buff=0.2))
            c.wait_until("yes yes")
            offs = [c.until(q, floor=0) for q in ("yes yes", "yes no", "no yes", "and no no")]
            self.play(*[time_span(Create(b), o, o + 0.6) for b, o in zip(boxes, offs)],
                      *[time_span(FadeIn(l, shift=0.15 * DOWN), o, o + 0.6) for l, o in zip(labs, offs)])

            # {fewer}: 4 < 6, two orders share a box
            c.wait_until("fewer")
            lt = MathTex("4", "<", "6", font_size=60, color=GOLD).move_to([4.9, 2.95, 0])
            self.play(TransformFromCopy(p22[2], lt[0]), FadeIn(lt[1]), FadeIn(lt[2]), run_time=1.2)
            settle(self, lt)
            c.wait_until("at least two")
            anims = []
            for k, (p1, p2) in ((1, ("acb", "cab")), (3, ("bca", "cba"))):
                x = SLOT_X[k]
                wide = RoundedRectangle(corner_radius=0.16, width=3.3, height=0.92)
                wide.set_stroke(GOLD, 3).set_fill(opacity=0).move_to([x, Y2, 0])
                anims.append(Transform(boxes[k], wide))
                for p, dx in ((p1, -0.8), (p2, 0.8)):
                    anims.append(fade_to(O[p], 1.0, shift=np.array([x + dx, Y2, 0]) - O[p].get_center()))
            self.play(*anims, run_time=1.8)
            c.wait_until("treat them")
            self.play(FlashAround(boxes[1], time_width=1.5), FlashAround(boxes[3], time_width=1.5), run_time=1.6)

            # {wrong}: one of them comes out wrong
            c.wait_until("wrong")
            cab = O["cab"]
            cab.generate_target()
            cab.target.box.set_stroke(RED, 4)
            cab.target.letters.set_color(RED)
            cross = cross_mark().move_to(cab.get_corner(UR) + np.array([0.12, 0.14, 0]))
            self.play(MoveToTarget(cab), GrowFromCenter(cross), run_time=1.0)

            # {three}: the third question comes back
            c.wait_until("three")
            self.cap3 = T("some input needs a 3rd question", 36).move_to([0, -3.2, 0])
            for m in (N["L2"], N["R2"], *low_edges):
                apply_op(m, 1.0)
            anims = [FadeOut(m) for m in (*boxes, *labs, cross, p22, lt)]
            for p in deep:
                o = O[p]
                o.generate_target()
                o.target.move_to([*LEAF[p], 0])
                o.target.box.set_stroke(GREEN, 4)
                o.target.letters.set_color(YELLOW)
                anims.append(MoveToTarget(o))
            anims += [FadeIn(N["L2"]), FadeIn(N["R2"]), *[FadeIn(e) for e in low_edges]]
            anims += [Transform(self.br, bracket(Y0 + NODE_H / 2, Y3 - LEAF_TOP)),
                      Transform(self.brl, depth_label(3)), FadeIn(self.cap3, shift=0.2 * UP)]
            self.play(*anims, run_time=min(1.8, 0.7 * c.until()))

    # ------------------------------------------------------------------ c1.bound.5
    def clip5(self):
        O, N, E = self.orders, self.nodes, self.E
        with self.say("c1.bound.5") as c:
            # {general}: the tree shrinks to the corner
            skel = [*[n.box for n in N.values()], *[o.box for o in O.values()], *E.values()]
            texts = [*[n.tex for n in N.values()], *[o.letters for o in O.values()],
                     *self.labs.values(), self.br, self.brl]
            ref = VGroup(*skel).copy()
            s_ = 0.4
            c0 = ref.get_center()
            ref.scale(s_, about_point=c0)
            d = np.array([-6.6, 3.45, 0]) - ref.get_corner(UL)
            anims = [FadeOut(t) for t in texts]
            for m in skel:
                m.generate_target()
                m.target.scale(s_, about_point=c0).shift(d)
                m.target.set_stroke(width=2)
                anims.append(MoveToTarget(m))
            self.play(*anims, run_time=1.6)
            tree = VGroup(*skel)
            settle(self, tree)

            c.wait_until("a list of")
            nit = Tex("$n$", " items: ", "$n!$", " orders", font_size=48, color=GOLD).move_to([2.4, 2.5, 0])
            self.play(FadeIn(nit, shift=0.2 * DOWN), run_time=1.0)

            # {power}: each comparison at most doubles the answer patterns
            c.wait_until("power")
            pa = Tex("1", " comparison", ": at most ", "$2$", " answer patterns", font_size=44).move_to([0, 0.8, 0])
            pb = Tex("10", " comparisons", ": at most ", "$2^{10}$", " answer patterns", font_size=44).move_to([0, 0.8, 0])
            pc = Tex("$C$", " comparisons", ": at most ", "$2^{C}$", " answer patterns", font_size=44).move_to([0, 0.8, 0])
            for t in (pa, pb, pc):
                t[0].set_color(GOLD)
                t[3].set_color(GOLD)
            self.play(FadeOut(self.cap3), FadeIn(pa, shift=0.2 * UP), run_time=1.0)
            c.wait_until("so ten comparisons")
            self.play(*[ReplacementTransform(pa[i], pb[i]) for i in range(5)], run_time=1.5)
            settle(self, pb)

            # {bound}: 2^C(n) >= n!
            c.wait_until("bound")
            self.play(*[ReplacementTransform(pb[i], pc[i]) for i in range(5)], run_time=1.4)
            settle(self, pc)
            bf = MathTex("2", "^{C(n)}", r"\ge", "n!", font_size=60, color=YELLOW).move_to([0, -0.85, 0])
            bbox = SurroundingRectangle(bf, color=YELLOW, buff=0.25, stroke_width=4)
            c.wait_until("must be at least")
            self.play(TransformFromCopy(pc[3][0], bf[0]), TransformFromCopy(pc[3][1], bf[1]),
                      TransformFromCopy(nit[2], bf[3]), FadeIn(bf[2]),
                      time_span(Create(bbox), 0.8, 1.6), run_time=1.6)
            settle(self, bf)

            # {log}: C(n) >= log2(n!)
            c.wait_until("log")
            lf = MathTex("C(n)", r"\ge", r"\log_2", "(", "n!", ")", font_size=60).move_to([0, -2.3, 0])
            self.play(TransformFromCopy(bf[1], lf[0]), TransformFromCopy(bf[2], lf[1]),
                      TransformFromCopy(bf[0], lf[2]), TransformFromCopy(bf[3], lf[4]),
                      FadeIn(lf[3]), FadeIn(lf[5]), run_time=1.8)
            settle(self, lf)

            # {worst}: worst-case bound; the formulas move to their final place
            c.wait_until("worst")
            up = 1.7 * UP
            w1 = T("worst case:", 36, GOLD).move_to([0, -2.2, 0])
            w2 = T("whatever the method, some input needs this many", 34).move_to([0, -2.8, 0])
            self.play(FadeOut(tree), FadeOut(nit), FadeOut(pc),
                      bf.animate.shift(up), bbox.animate.shift(up), lf.animate.shift(up),
                      time_span(FadeIn(w1, shift=0.2 * UP), 0.8, 1.6),
                      time_span(FadeIn(w2, shift=0.2 * UP), 1.1, 1.9), run_time=1.9)

        # last shot: the two formulas alone (scene 6 opens from them)
        self.wait(1.5)
        self.play(FadeOut(w1), FadeOut(w2), run_time=0.9)
        self.wait(1.0)
