"""Chapter 3, scene 5: the two surviving cells, and why their promises hold. Clips c3.survive.1 - c3.survive.4.

Opens on ch3_s2_fill's home_shot("pass2") (s4's last frame); ends on home_shot("survivors") (s6 opens on it).
While the argument runs, p. 150's state table steps aside and the left half holds the caption, the
run, the pair graph and the two-lane callback; the table returns at the end.
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

F2 = load_scene("ch3_s2_fill")
D2 = load_scene("ch2_s2_definition")
H1 = load_scene("ch2_s1_hook")

LX = -3.8                  # centre of the free left half (where the state table sits at home)
NODE_Y = -0.9
NODE_X = {"A-D": -5.05, "C-E": -2.55}
NODE_R = 0.7


def _p(x, y):
    return np.array([x, y, 0.0])


def handover_shot():
    return F2.home_shot("survivors")


def _on_rim(name, deg):
    a = np.deg2rad(deg)
    return _p(NODE_X[name], NODE_Y) + NODE_R * np.array([np.cos(a), np.sin(a), 0.0])


def _arrow_of(path, color=FG):
    arr = path.copy().set_stroke(color, 3.5)
    arr.add_tip(tip_length=0.2, tip_width=0.2)
    arr.get_tip().set_fill(color, 1).set_stroke(color, 1)
    return arr


def pair_graph():
    """Two GOLD nodes A-D and C-E, outputs under each, input-0 self-loops on top, input-1 arcs between."""
    g = VGroup()
    g.node, g.outs, g.path, g.arrow, g.lab = {}, {}, {}, {}, {}
    for name, bits in (("A-D", "0, 0"), ("C-E", "1, 1")):
        c = Circle(radius=NODE_R).set_stroke(GOLD, 4).set_fill(GOLD, 0.12).move_to(_p(NODE_X[name], NODE_Y))
        lab = T(name, 36).move_to(c)
        node = VGroup(c, lab)
        outs = T(bits, 36, t2c={"1": GREEN}, t2w={"1": BOLD}).next_to(c, DOWN, buff=0.3)
        g.node[name], g.outs[name] = node, outs
    for name in ("A-D", "C-E"):
        loop = ArcBetweenPoints(_on_rim(name, 125), _on_rim(name, 55), angle=-1.45 * PI)
        g.path[(name, 0)] = loop
        g.arrow[(name, 0)] = _arrow_of(loop)
        g.lab[(name, 0)] = T("0", 36, BLUE).next_to(loop, UP, buff=0.12)
    up = ArcBetweenPoints(_on_rim("A-D", 22), _on_rim("C-E", 158), angle=-0.55)
    down = ArcBetweenPoints(_on_rim("C-E", 202), _on_rim("A-D", 338), angle=-0.55)
    g.path[("A-D", 1)], g.path[("C-E", 1)] = up, down
    g.arrow[("A-D", 1)], g.arrow[("C-E", 1)] = _arrow_of(up), _arrow_of(down)
    g.lab[("A-D", 1)] = T("1", 36, BLUE).next_to(up, UP, buff=0.1)
    g.lab[("C-E", 1)] = T("1", 36, BLUE).next_to(down, DOWN, buff=0.1)
    g.add(*g.node.values(), *g.outs.values(), *g.arrow.values(), *g.lab.values())
    return g


CARD_LINES = ["Two states, say p and q, can", "be considered equivalent,", "i.e., p ≡ q, if from each of",
              "these states, a finite state", "machine generates the same", "output sequence in response",
              "to any input bit sequence."]


def def_card(size=28):
    """ch2 s2's definition, reflowed to fit the left half (same words, same colours)."""
    pq = {"p": YELLOW, "q": YELLOW}
    t2c = [pq, {}, pq, {}, {"same": GREEN}, {"output sequence": GREEN}, {"any input bit sequence": BLUE}]
    lines = VGroup(*[T(l, size, t2c=c, disable_ligatures=True) for l, c in zip(CARD_LINES, t2c)])
    lines.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    frame = RoundedRectangle(corner_radius=0.2, width=lines.width + 0.6, height=lines.height + 0.5)
    frame.set_stroke(DIM, 2).move_to(lines)
    card = VGroup(frame, lines)
    card.same = [select(lines[4], "same")[0], select(lines[5], "output sequence")[0]]
    card.anyinput = select(lines[6], "any input bit sequence")[0]
    return card


NEXT = {("A-D", 0): "A-D", ("A-D", 1): "C-E", ("C-E", 0): "C-E", ("C-E", 1): "A-D"}


def _pulse_cross(cr):
    w0 = cr[0].get_stroke_width()

    def f(m, a):
        s = np.sin(PI * a)
        for ln in m:
            ln.set_stroke(RED, w0 + 8 * s, opacity=0.6 + 0.4 * s)
    return UpdateFromAlphaFunc(cr, f)


def _ring_flash(circle, color=GOLD):
    """A flash that travels once round the circle's own outline (FlashAround draws a square)."""
    ring = circle.copy().set_fill(opacity=0).set_stroke(color, 8)
    return VShowPassingFlash(ring, time_width=1.5)


def _shoot(dot, a, b):
    def f(m, t):
        m.move_to(a + (b - a) * smooth(t))
        m.set_opacity(min(1.0, 6 * t, 6 * (1 - t)))
    return UpdateFromAlphaFunc(dot, f)


class Survivors(NarratedScene):
    def construct(self):
        self.shot = F2.home_shot("pass2")
        self.add(self.shot)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.finish()

    # ------------------------------------------------------------------ c3.survive.1
    def clip1(self):
        s = self.shot
        it = s.it
        tgt = F2.home_shot("survivors")
        with self.say("c3.survive.1") as c:
            for p in ("A-D", "C-E"):
                it.cells[p].set_z_index(1)
                for m in s.texts[p]:
                    m.set_z_index(2)
            self.play(*[cr.animate.set_stroke(opacity=0.6) for cr in s.crosses.values()],
                      *[it.cells[p].animate.set_stroke(GOLD, 5).set_fill(GOLD, 0.12) for p in ("A-D", "C-E")],
                      *[FadeIn(tgt.glow[p]) for p in ("A-D", "C-E")],
                      run_time=min(1.2, c.until("cellad")))
            self.glows = [tgt.glow["A-D"], tgt.glow["C-E"]]
            c.wait_until("cellad")
            self.letters = [it.row_letters["D"], it.col_letters["A"], it.row_letters["E"], it.col_letters["C"]]
            self.letter_cols = [m.get_color() for m in self.letters]
            self.play(*[m.animate.set_color(YELLOW) for m in self.letters[:2]],
                      *flash(self.letters[:2], time_width=1.5), run_time=min(1.0, c.until("cellce")))
            c.wait_until("cellce")
            self.play(*[m.animate.set_color(YELLOW) for m in self.letters[2:]],
                      *flash(self.letters[2:], time_width=1.5), run_time=1.0)
            c.wait_until("coords")

            # the state table steps aside; p. 155's bullet takes the left half
            cap = VGroup(*[T(t, 30, slant=ITALIC) for t in (
                "The ‘coordinates’ of the",
                "remaining cells correspond",
                "to the equivalent state",
                "pairs, i.e., cell A-D and",
                "cell C-E so,")]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            cap.move_to(_p(LX, 1.75))
            self.cap = cap
            self.play(*during(disappear(s.tbl), 0, 0.45), *during(appear(cap), 0.5, 1.0), run_time=1.8)  # early: the bullet, shown whole
            c.wait_until("equivalent")
            res = T("A ≡ D and C ≡ E", 48, t2c={"A": YELLOW, "D": YELLOW, "C": YELLOW, "E": YELLOW})
            res.move_to(_p(LX, -0.4))
            self.res = res
            self.play(*appear(res), run_time=1.2)
            c.wait_until("doubt")

            # each promise leans on the other
            a1, an1 = F2.pointer(s, s.texts["A-D"][1], "C-E")
            self.play(*an1, run_time=1.5)
            a2, an2 = F2.pointer(s, s.texts["C-E"][1], "A-D")
            self.play(*an2, run_time=1.5)
            self.loop = [a1, a2]
            c.wait_until("Is that really enough")
            q = T("?", 56, YELLOW).move_to(_p(2.35, 1.98))
            self.q = q
            self.play(*appear(q), run_time=1.0)

    # ------------------------------------------------------------------ c3.survive.2
    def clip2(self):
        s = self.shot
        with self.say("c3.survive.2") as c:
            self.play(*during(disappear(self.cap), 0, 0.45),
                      *during([self.res.animate.move_to(_p(LX, 3.25))], 0.45, 1.0),
                      *[m.animate.set_color(col) for m, col in zip(self.letters, self.letter_cols)],
                      run_time=1.4)
            ab = s.crosses["A-B"]
            self.play(_pulse_cross(ab), FlashAround(s.it.cells["A-B"], color=RED, time_width=1.5),
                      run_time=1.6)
            c.wait_until("ab")
            arr, an = F2.pointer(s, s.texts["A-B"][0], "D-F", angle=-PI / 4)
            self.ab_ptr = arr
            self.play(*disappear(*self.loop, self.q), run_time=0.8)
            self.play(*an, run_time=2.0)
            c.wait_until("input")

            # the run: Moore style, each state with its output under it
            ya, yb, dy = 1.55, -0.75, 0.68
            xs, xe = LX - 1.6, LX + 1.6

            def st(n, x, y, out):
                lt = T(n, 50).move_to(_p(x, y))
                o = T(out, 38, GREEN, weight=BOLD) if out == "1" else T(out, 38)
                return lt, o.move_to(_p(x, y - dy))

            A, oA = st("A", xs, ya, "0")
            B, oB = st("B", xs, yb, "0")
            D, oD = st("D", xe, ya, "0")
            Fm, oF = st("F", xe, yb, "1")
            arrows, labs = [], []
            for y in (ya, yb):
                ar = Arrow(_p(xs + 0.4, y), _p(xe - 0.4, y), buff=0, stroke_width=4, color=FG,
                           tip_length=0.22, max_tip_length_to_length_ratio=0.2)
                arrows.append(ar)
                labs.append(T("0", 38, BLUE).next_to(ar, UP, buff=0.12))
            self.play(*appear(VGroup(A, oA), VGroup(B, oB), lag=0.3), run_time=1.0)
            self.play(*[GrowArrow(a) for a in arrows], *appear(*labs, lag=0.1), run_time=1.0)
            c.wait_until("State A goes to D")
            self.play(*appear(VGroup(D, oD)), run_time=1.0)
            c.wait_until("while state B")
            self.play(*appear(VGroup(Fm, oF)), run_time=1.0)
            c.wait_until("apart")
            neq = MathTex(r"A \not\equiv B", font_size=64, color=RED).move_to(_p(LX, -2.75))
            self.play(*flash([oD, oF], time_width=1.5), *during(appear(neq), 0.4, 1.0), run_time=1.6)
            self.run = [A, oA, B, oB, D, oD, Fm, oF, *arrows, *labs, neq]

    # ------------------------------------------------------------------ c3.survive.3
    def clip3(self):
        g = pair_graph()
        self.graph = g
        with self.say("c3.survive.3") as c:
            self.play(*during(disappear(*self.run, self.ab_ptr), 0, 0.45),
                      *during(appear(g.node["A-D"], g.node["C-E"], shift=None, lag=0.2), 0.5, 1.0),
                      run_time=1.8)
            self.play(*appear(g.outs["A-D"], g.outs["C-E"], lag=0.3), run_time=1.0)
            c.wait_until("fromad")
            for name, n0, n1 in (("A-D", 0, 0), ("C-E", 1, 1)):
                if name == "C-E":
                    c.wait_until("fromce")
                c.wait_until("input zero", nth=n0)
                self.play(Create(g.arrow[(name, 0)]), *appear(g.lab[(name, 0)]),
                          _ring_flash(g.node[name][0]), run_time=1.5)
                c.wait_until("input one", nth=n1)
                other = NEXT[(name, 1)]
                self.play(Create(g.arrow[(name, 1)]), *appear(g.lab[(name, 1)]),
                          *during([_ring_flash(g.node[other][0])], 0.4, 1.0),
                          run_time=1.5)
            settle(self, g)
            c.wait_until("closed")

            # a dot walks the graph on 1 0 1 1 0
            seq = VGroup(*[T(d, 42, BLUE) for d in "10110"]).arrange(RIGHT, buff=0.45).move_to(_p(LX, 1.75))
            box = SurroundingRectangle(seq[0], buff=0.12).set_stroke(YELLOW, 2).set_fill(YELLOW, 0.15)
            box.set_z_index(-1)
            dot = Dot(g.path[("A-D", 1)].get_start(), radius=0.12, color=YELLOW).set_z_index(3)
            self.play(*appear(seq, shift=None), FadeIn(box), FadeIn(dot, scale=0.5), run_time=1.0)
            here = "A-D"
            step_rt = max(0.8, (c.until("never") - 0.4) / 5)
            for i, d in enumerate("10110"):
                path = g.path[(here, int(d))]
                there = NEXT[(here, int(d))]
                anims = [Succession(dot.animate(run_time=0.2).move_to(path.get_start()),
                                    MoveAlongPath(dot, path, run_time=0.8)),
                         *during([FlashAround(g.outs[there], color=YELLOW, time_width=1.5)], 0.7, 1.0)]
                if i > 0:
                    anims.append(Transform(box, box.copy().move_to(seq[i])))
                self.play(*anims, run_time=step_rt)
                here = there
            c.wait_until("never")

            # the definition from part two comes back
            card = def_card().move_to(_p(LX, 0.55))
            self.card = card
            small = g.copy().scale(0.8).move_to(_p(4.85, 2.25))
            self.play(*during(disappear(seq, box, dot, self.res, g), 0, 0.45),  # early: recalled card
                      *during(appear(small, card, shift=None, lag=0.1), 0.5, 1.0), run_time=1.8)
            self.graph = small
            self.play(*[FlashAround(m, color=GREEN, time_width=1.5) for m in card.same],
                      FlashAround(card.anyinput, color=BLUE, time_width=1.5), run_time=1.8)

    # ------------------------------------------------------------------ c3.survive.4
    def clip4(self):
        g = self.graph
        lanes = H1.two_lanes()
        lanes.scale(0.9).move_to(_p(-3.75, 0.35))
        self.lanes = lanes
        with self.say("c3.survive.4") as c:
            self.play(*disappear(self.card), run_time=1.0)
            c.wait_until("One copy")
            self.play(*appear(lanes.labels[0], lanes.circles[0][0], lag=0.2), run_time=1.0)
            c.wait_until("the other in state D")
            self.play(*appear(lanes.labels[1], lanes.circles[1][0], lag=0.2), run_time=1.0)
            c.wait_until("both were fed")
            self.play(*appear(lanes.xlabel, *lanes.inputs, lag=0.15), run_time=1.0)
            self.play(*appear(*[lanes.step(i) for i in range(4)], shift=None, lag=0.5),
                      run_time=min(2.6, c.until("They visited")))
            c.wait_until("They visited")
            self.play(*appear(lanes.out_rows[0], lanes.out_rows[1], lag=0.3), run_time=1.0)
            c.wait_until("same outputs")
            self.play(*appear(lanes.out_boxes[0], lanes.out_boxes[1], lanes.eq, shift=None, lag=0.2),
                      run_time=1.0)
            settle(self, lanes)
            c.wait_until("pairs")

            cols = []
            for k in range(5):
                top, bot = lanes.circles[0][k], lanes.circles[1][k]
                h = top.get_top()[1] - bot.get_bottom()[1] + 0.2
                cols.append(RoundedRectangle(corner_radius=0.2, width=top.width + 0.22, height=h)
                            .set_stroke(GOLD, 3).move_to(_p(top.get_x(), (top.get_top()[1] + bot.get_bottom()[1]) / 2)))
            self.cols = cols
            self.play(LaggedStart(*[GrowFromCenter(b) for b in cols], lag_ratio=0.3), run_time=1.8)
            c.wait_until("lands")

            cells = ["A-D", "A-D", "C-E", "A-D", "A-D"]
            dots, shots = [], []
            for k, p in enumerate(cells):
                d = Dot(cols[k].get_bottom() + 0.05 * UP, radius=0.11, color=GOLD).set_opacity(0).set_z_index(3)
                dots.append(d)
                cell = self.shot.it.cells[p]
                shots.append(Succession(_shoot(d, cols[k].get_bottom() + 0.05 * UP, cell.get_center(), ),
                                        FlashAround(cell, color=GOLD, time_width=1.5)))
            self.add(*dots)
            self.play(LaggedStart(*shots, lag_ratio=0.3), run_time=min(3.0, c.until() - 0.1))
            self.dots = dots

    def finish(self):
        self.wait(0.8)
        self.play(*disappear(self.lanes, *self.cols, self.graph), run_time=1.0)
        fresh = handover_shot()
        self.remove(*self.mobjects)
        self.add(fresh)
        self.remove(fresh.tbl)
        self.play(*appear(fresh.tbl, shift=None), run_time=1.2)
        self.wait(1.0)
