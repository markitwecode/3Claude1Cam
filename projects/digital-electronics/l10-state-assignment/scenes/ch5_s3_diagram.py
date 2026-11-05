"""Chapter 5, scene 3: reading the synchroniser's state diagram (p. 139). Clips c5.diagram.1 – c5.diagram.5.

Shared helpers (later scenes import them with load_scene("ch5_s3_diagram")):
- `sync_diagram(codes=None, unused=False, r=0.62)`: p. 139's diagram on ch1's moore_diagram
  positions: Sync (-3, 1.9), Hunt (3, 1.9), Sight (0, -1.2). Circles FG stroke 4, names T 32
  YELLOW, arcs FG stroke 3, labels MathTex 40 BLUE.
  Lists in order (Sync, Hunt, Sight): .circles .names; .arcs .labels (8, ch1's order):
    0 Sync loop ē (upper), 1 Sync loop e·r (lower), 2 Sync -> Hunt e·r̄ (top),
    3 Hunt loop r̄, 4 Hunt -> Sight r, 5 Sight loop ē, 6 Sight -> Sync e·r, 7 Sight -> Hunt e·r̄.
  Per state (name -> ...): .circle .name .by_state (arc indices leaving it) .code.
  codes: name -> string, e.g. {"Hunt": "00", "Sight": "01", "Sync": "10"} or one-hot
  {"Hunt": "001", ...}: GREEN Mono 32 "[00]" beside each circle (Sync, Hunt above; Sight left);
  .code[name] (None when not given; codes are part of the group when given).
  unused=True: .unused = VGroup(circle DIM, "[11]" DIM, "unused" DIM) at (4.6, -2.3)
  (.unused.circle .unused.code .unused.label); in the group. Otherwise .unused is None.
- `handover_shot()`: the bare finished diagram (sync_diagram()), this scene's last frame.
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
from lib.style import *  # noqa: E402,F403


def _p(x, y):
    return np.array([x, y, 0.0])


def _dir(deg):
    a = np.deg2rad(deg)
    return np.array([np.cos(a), np.sin(a), 0.0])


def _arc(s, e, angle, color=FG, width=3):
    a = ArcBetweenPoints(s, e, angle=angle).set_stroke(color, width)
    a.add_tip(tip_length=0.2, tip_width=0.2)
    a.get_tip().set_stroke(color, 1).set_fill(color, 1)
    return a


STATES = ("Sync", "Hunt", "Sight")
CENTRES = {"Sync": _p(-3, 1.9), "Hunt": _p(3, 1.9), "Sight": _p(0, -1.2)}
CODE_POS = {"Sync": _p(-3, 2.95), "Hunt": _p(3, 2.95), "Sight": _p(-1.5, -1.2)}


# ---------------------------------------------------------------- shared: p. 139's diagram
def sync_diagram(codes=None, unused=False, r=0.62):
    A, B, C = (CENTRES[n] for n in STATES)
    circles = [Circle(radius=r).set_stroke(FG, 4).move_to(CENTRES[n]) for n in STATES]
    names = [T(n, 32, YELLOW).move_to(CENTRES[n]) for n in STATES]
    E_BAR, E_R, E_RBAR, R_BAR, R = (r"\overline{e}", r"e\cdot r", r"e\cdot\overline{r}",
                                    r"\overline{r}", r"r")

    def loop(c, th):
        return _arc(c + r * _dir(th + 24), c + r * _dir(th - 24), -4.2), c + 1.78 * _dir(th)

    spec = [
        (*loop(A, 150), E_BAR),
        (*loop(A, 210), E_R),
        (_arc(A + r * _dir(15), B + r * _dir(165), -0.35), _p(0, 2.72), E_RBAR),
        (*loop(B, 30), R_BAR),
        (_arc(B + r * _dir(251), C + r * _dir(21), -0.5), _p(2.2, -0.3), R),
        (*loop(C, 270), E_BAR),
        (_arc(C + r * _dir(134), A + r * _dir(314), -0.5), _p(-2.1, -0.2), E_R),
        (_arc(C + r * _dir(71), B + r * _dir(201), -0.5), _p(0.62, 1.2), E_RBAR),
    ]
    arcs, labels = [], []
    for arc, pos, tex in spec:
        arcs.append(arc)
        labels.append(MathTex(tex, font_size=40, color=BLUE).move_to(pos))
    g = VGroup(*circles, *names, *arcs, *labels)
    g.circles, g.names, g.arcs, g.labels = circles, names, arcs, labels
    g.circle = dict(zip(STATES, circles))
    g.name = dict(zip(STATES, names))
    g.by_state = {"Sync": [0, 1, 2], "Hunt": [3, 4], "Sight": [5, 6, 7]}
    g.code = {n: None for n in STATES}
    if codes:
        for n, s in codes.items():
            t = Mono(f"[{s}]", 32, GREEN).move_to(CODE_POS[n])
            g.code[n] = t
            g.add(t)
    g.unused = None
    if unused:
        uc = Circle(radius=r).set_stroke(DIM, 4).move_to(_p(4.6, -2.3))
        ut = Mono("[11]", 32, DIM).move_to(uc)
        ul = T("unused", 30, DIM).next_to(uc, DOWN, buff=0.18)
        u = VGroup(uc, ut, ul)
        u.circle, u.code, u.label = uc, ut, ul
        g.unused = u
        g.add(u)
    return g


def handover_shot():
    return sync_diagram()


# ---------------------------------------------------------------- local: the (e, r) grids
CELL_S = 0.5
GRID_POS = {"Sync": _p(-5.4, -0.4), "Hunt": _p(5.2, 0.1), "Sight": _p(-2.6, -2.55)}
# arc index -> the (e, r) cells its label covers
COVERS = {3: [(0, 0), (1, 0)], 4: [(0, 1), (1, 1)],
          5: [(0, 0), (0, 1)], 6: [(1, 1)], 7: [(1, 0)],
          0: [(0, 0), (0, 1)], 1: [(1, 1)], 2: [(1, 0)]}


def input_grid(center, color=DIM, headers=True, s=CELL_S):
    """2 x 2 cells: rows e = 0, 1 (top to bottom), columns r = 0, 1. .cell[(e, r)]."""
    cell = {}
    for e in (0, 1):
        for rr in (0, 1):
            sq = Square(side_length=s).set_stroke(color, 2).set_fill(BG, 0)
            sq.move_to(center + _p((rr - 0.5) * s, (0.5 - e) * s))
            cell[(e, rr)] = sq
    g = VGroup(*cell.values())
    if headers:
        top, left = center[1] + s, center[0] - s
        for k in (0, 1):
            g.add(MathTex(str(k), font_size=30, color=BLUE).move_to(_p(center[0] + (k - 0.5) * s, top + 0.22)))
            g.add(MathTex(str(k), font_size=30, color=BLUE).move_to(_p(left - 0.22, center[1] + (0.5 - k) * s)))
        g.add(MathTex("r", font_size=30, color=BLUE).move_to(_p(center[0] + s + 0.24, top + 0.22)))
        g.add(MathTex("e", font_size=30, color=BLUE).move_to(_p(left - 0.22, center[1] - s - 0.26)))
    g.cell = cell
    return g


class ReadingTheDiagram(NarratedScene):
    def construct(self):
        d = sync_diagram()
        self.d = d
        self.clip1(d)
        self.clip2(d)
        self.clip3(d)
        self.clip4(d)
        self.clip5(d)
        self.wait(1.0)   # handover: hold the bare diagram; s4 opens on it

    # light one state, return the previous one to white
    def light(self, d, name, prev=None, rt=1.0):
        anims = [restyle(d.circle[name], outline=YELLOW, width=6)]
        if prev:
            anims.append(restyle(d.circle[prev], outline=FG, width=4))
        self.play(*anims, run_time=rt)

    def draw_arc(self, d, i, rt):
        self.play(Create(d.arcs[i]), *appear(d.labels[i], shift=None), run_time=rt)

    def clip1(self, d):
        with self.say("c5.diagram.1") as c:
            rt = min(1.5, c.until("hunt"))
            self.play(*appear(*d.circles, *d.names, shift=None, lag=0.12), run_time=rt)  # early: "its three states" shows all three at once
            c.wait_until("hunt")
            self.light(d, "Hunt", rt=min(1.0, c.until("stay")))
            c.wait_until("stay")
            self.draw_arc(d, 3, min(1.6, c.until("go")))
            c.wait_until("go")
            self.draw_arc(d, 4, min(1.6, c.until("either")))
            c.wait_until("either")
            self.either = T("e: either value", 30, DIM).move_to(_p(3.45, -0.85))
            self.play(*appear(self.either), run_time=min(1.0, c.until()))

    def clip2(self, d):
        with self.say("c5.diagram.2") as c:
            self.light(d, "Sight", "Hunt", rt=min(1.0, c.until("wait")))
            c.wait_until("wait")
            self.play(Create(d.arcs[5]), *appear(d.labels[5], shift=None),
                      *disappear(self.either), run_time=min(1.6, c.until("confirm")))
            c.wait_until("confirm")
            self.draw_arc(d, 6, min(1.6, c.until("ask")))
            c.wait_until("ask")
            q = T("?", 56, YELLOW).move_to(d.labels[7])
            self.play(*appear(q), run_time=min(1.0, c.until("fluke")))
            c.wait_until("fluke")
            self.play(*swap(q, d.labels[7]), *during([Create(d.arcs[7])], 0.3, 1.0),
                      run_time=min(1.6, c.until("the first sighting")))

    def clip3(self, d):
        with self.say("c5.diagram.3") as c:
            self.light(d, "Sync", "Sight", rt=min(1.0, c.until("between")))
            c.wait_until("between")
            self.draw_arc(d, 0, min(1.6, c.until("kept")))
            c.wait_until("kept")
            self.draw_arc(d, 1, min(1.6, c.until("lost")))
            c.wait_until("lost")
            # the near-flat Sync -> Hunt arc, drawn with Create, read as a straight stub poking
            # into empty space: it fades in whole, then a flash runs along it to show direction
            self.play(*appear(d.arcs[2], d.labels[2], shift=None, lag=0.1),
                      run_time=min(1.2, 0.5 * c.until("sync is lost")))
            path = d.arcs[2].copy()
            path.pop_tips()
            self.play(VShowPassingFlash(path.set_stroke(YELLOW, 6), time_width=0.5),
                      run_time=min(1.2, c.until("sync is lost")))

    def fill_arcs(self, d, grid, idxs, extra=(), rt=1.5, step=0.6):
        """Flash each arc in turn, its label goes YELLOW, its cells fill YELLOW."""
        anims = list(extra)
        dur = step * (len(idxs) - 1) + 0.9
        for k, i in enumerate(idxs):
            a, b = k * step, k * step + 0.9
            anims.append(time_span(VShowPassingFlash(d.arcs[i].copy().set_stroke(YELLOW, 8),
                                                     time_width=0.6), a, b))
            anims.append(time_span(d.labels[i].animate.set_color(YELLOW), a, b))
            for cell in COVERS[i]:
                anims.append(time_span(grid.cell[cell].animate.set_fill(YELLOW, 0.6), a, b))
        self.play(*anims, run_time=max(rt, dur))

    def settle_arcs(self, d, grid, idxs):
        out = []
        for i in idxs:
            out.append(d.labels[i].animate.set_color(BLUE))
            for cell in COVERS[i]:
                out.append(grid.cell[cell].animate.set_fill(BLUE, 0.45))
        return out

    def clip4(self, d):
        with self.say("c5.diagram.4") as c:
            self.play(restyle(d.circle["Sync"], outline=FG, width=4),
                      *[VShowPassingFlash(ci.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for ci in d.circles], run_time=min(1.4, c.until("grids")))
            c.wait_until("grids")
            grids = {n: input_grid(GRID_POS[n]) for n in STATES}
            self.grids = grids
            self.play(*appear(grids["Sync"], grids["Hunt"], grids["Sight"], shift=None, lag=0.35),
                      run_time=min(2.0, c.until("hunt2")))
            c.wait_until("hunt2")

            ticks = {n: check_mark() for n in STATES}
            ticks["Sync"].move_to(GRID_POS["Sync"] + _p(1.2, -0.95))
            ticks["Hunt"].move_to(GRID_POS["Hunt"] + _p(-1.4, -0.8))
            ticks["Sight"].move_to(GRID_POS["Sight"] + _p(1.45, 0.0))
            self.ticks = ticks

            self.fill_arcs(d, grids["Hunt"], [3], rt=min(1.3, c.until("the other two")))
            c.wait_until("the other two")
            self.fill_arcs(d, grids["Hunt"], [4], extra=self.settle_arcs(d, grids["Hunt"], [3]),
                           rt=min(1.3, c.until("others")))
            self.play(*self.settle_arcs(d, grids["Hunt"], [4]), *appear(ticks["Hunt"], shift=None),
                      run_time=min(0.9, c.until("others")))
            c.wait_until("others")

            self.fill_arcs(d, grids["Sight"], [5, 6, 7], step=0.55)
            self.wait(0.3)
            self.fill_arcs(d, grids["Sync"], [0, 1, 2], step=0.45,
                           extra=self.settle_arcs(d, grids["Sight"], [5, 6, 7])
                           + appear(ticks["Sight"], shift=None))
            self.play(*self.settle_arcs(d, grids["Sync"], [0, 1, 2]),
                      *appear(ticks["Sync"], shift=None), run_time=min(0.9, c.until("why2")))
            c.wait_until("why2")

            # two RED ghost grids: a cell missed, a cell covered twice
            g1 = input_grid(_p(2.6, -2.95), color=RED, headers=False)
            for cell in [(0, 0), (0, 1), (1, 1)]:
                g1.cell[cell].set_fill(RED, 0.35)
            cap1 = VGroup(T("nowhere", 28, RED), T("to go", 28, RED)).arrange(DOWN, buff=0.12).next_to(g1, UP, buff=0.2)
            c.wait_until(own_word=cap1[0])
            self.play(*appear(g1, shift=None), *appear(cap1), run_time=1.0)
            self.play(FlashAround(g1.cell[(1, 0)], color=RED, run_time=1.2, time_width=1.5))
            c.wait_until("cover one twice")
            g2 = input_grid(_p(5.3, -2.95), color=RED, headers=False)
            for cell in g2.cell.values():
                cell.set_fill(RED, 0.35)
            two = MathTex(r"\times 2", font_size=30, color=FG).move_to(g2.cell[(1, 1)])
            cap2 = VGroup(T("two places", 28, RED), T("to go", 28, RED)).arrange(DOWN, buff=0.12).next_to(g2, UP, buff=0.2)
            c.wait_until(own_word=cap2[0])
            self.play(*appear(g2, two, shift=None), *appear(cap2), run_time=1.0)
            self.ghosts = [g1, cap1, g2, two, cap2]

    def clip5(self, d):
        with self.say("c5.diagram.5") as c:
            c.wait_until("only in sync")
            tags = [MathTex("s = 1", font_size=36, color=GREEN).move_to(_p(-3, 3.1)),
                    MathTex("s = 0", font_size=36, color=DIM).move_to(_p(3, 3.1)),
                    MathTex("s = 0", font_size=36, color=DIM).move_to(_p(-1.25, -1.2))]
            self.play(*appear(*tags, shift=None, lag=0.2),
                      run_time=min(1.6, c.until("moore")))
            c.wait_until("moore")
            cap = VGroup(T("Moore:", 30, YELLOW),
                         T("output from the state alone", 30)).arrange(DOWN, buff=0.15)
            cap.move_to(_p(4.0, -2.85))
            self.play(*during(disappear(*self.ghosts), 0, 0.45), *during(appear(cap), 0.5, 1.0), run_time=min(1.6, c.until("design")))  # early: the caption reads the sentence "depends on the state alone"
            c.wait_until("design")
            self.play(*disappear(*self.grids.values(), *self.ticks.values()),
                      run_time=min(1.0, c.until("now we can")))
            c.wait_until("now we can")
            self.play(*disappear(*tags, cap), run_time=min(1.0, c.until()))
