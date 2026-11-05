"""Chapter 1, scene 2: state machines, briefly (definition, p. 123's diagram, p. 122's schematic,
Moore vs Mealy, counters, the design recipe). Clips c1.machines.1 – c1.machines.4.

Shared helpers (import with load_scene("ch1_s2_machines")):
- `moore_diagram(names=("A", "B", "C"), r=0.62)`: p. 123's Moore machine, codes hidden
  (ch5's hook redraws it with names).
- `recipe_row(with_dee=True, size=30)`: the four recipe chips + the YELLOW `D = Q'` tag (s6 shows it small).
"""
# style: 2
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


# ---------------------------------------------------------------- shared: p. 123's Moore diagram
def moore_diagram(names=("A", "B", "C"), r=0.62):
    """p. 123's Moore state diagram without its codes: A top left (-3, 1.9), B top right (3, 1.9),
    C below between them (0, -1.2); circles FG stroke 4, radius r; names T 44.
    Arcs FG stroke 3 with small tips, labels MathTex 40 BLUE, exactly as on the slide:
    A: loops \\overline{e}, e\\cdot r; A->B e\\cdot\\overline{r}; B: loop \\overline{r}; B->C r;
    C: loop \\overline{e}; C->A e\\cdot r; C->B e\\cdot\\overline{r}.
    Parts: .circles .names (lists of 3), .arcs .labels (lists of 8, same order as above),
    .by_state (3 lists of arc indices: A's 0-2, B's 3-4, C's 5-7). About 9.4 x 5.9, centre ~(0, 0)."""
    cen = [_p(-3, 1.9), _p(3, 1.9), _p(0, -1.2)]
    circles = [Circle(radius=r).set_stroke(FG, 4).move_to(c) for c in cen]
    nms = [T(n, 44).move_to(c) for n, c in zip(names, cen)]
    A, B, C = cen
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
    g = VGroup(*circles, *nms, *arcs, *labels)
    g.circles, g.names, g.arcs, g.labels = circles, nms, arcs, labels
    g.by_state = [[0, 1, 2], [3, 4], [5, 6, 7]]
    return g


# ---------------------------------------------------------------- shared: the design recipe row
RECIPE = ["state\ndiagram", "state transition\ntable", "next-state\nlogic", "output logic\n(if any)"]


def recipe_row(with_dee=True, size=30):
    """Four chips (RoundedRectangle BLUE stroke 3, BG fill, T `size` FG two-line text, 1.3 tall at
    size 30) joined by DIM arrows, row centred at ORIGIN, 12.3 wide at size 30.
    with_dee: YELLOW MathTex `D = Q'` (60) under chip 2 ("next-state logic"), hung from it by a
    short YELLOW line. Parts: .chips (each with .box .text), .arrows, .dee and .tie (or None)."""
    k = size / 30
    chips = []
    for s in RECIPE:
        t = T(s, size, line_spacing=0.8)
        box = RoundedRectangle(corner_radius=0.15 * k, width=t.width + 0.45 * k, height=1.3 * k)
        box.set_stroke(BLUE, 3).set_fill(BG, 1)
        chip = VGroup(box, t)
        t.move_to(box)
        chip.box, chip.text = box, t
        chips.append(chip)
    row = VGroup(*chips).arrange(RIGHT, buff=0.75 * k)
    arrows = [Arrow(a.get_right(), b.get_left(), buff=0.08 * k, stroke_width=3,
                    max_tip_length_to_length_ratio=0.35).set_color(DIM)
              for a, b in zip(chips, chips[1:])]
    g = VGroup(*chips, *arrows)
    g.chips, g.arrows, g.dee, g.tie = chips, arrows, None, None
    if with_dee:
        dee = MathTex("D", "=", "Q'", font_size=60 * k, color=YELLOW)
        dee.next_to(chips[2], DOWN, buff=0.75 * k)
        tie = Line(chips[2].get_bottom(), dee.get_top() + 0.1 * k * UP).set_stroke(YELLOW, 3)
        g.add(tie, dee)
        g.dee, g.tie = dee, tie
    return g


# ---------------------------------------------------------------- D flip-flop (L6's symbol, compact)
def qbar(size=32, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.06)
    return VGroup(q, bar)


def dff(center=ORIGIN, w=1.4, h=2.0, pin=0.45):
    """Box w x h (FG stroke 4), D (BLUE) / Q (GREEN) labels at `pin` above centre, Q-bar (GREEN)
    at `pin` below, clock triangle on the bottom edge. Parts .box .tri .d_l .q_l .qb_l."""
    box = Rectangle(width=w, height=h).set_stroke(FG, 4).set_fill(BG, 1)
    tri = Polygon(_p(-0.17, -h / 2), _p(0.17, -h / 2), _p(0, -h / 2 + 0.26)).set_stroke(FG, 3)
    d_l = T("D", 32, BLUE).move_to(_p(-w / 2 + 0.27, pin))
    q_l = T("Q", 32, GREEN).move_to(_p(w / 2 - 0.27, pin))
    qb_l = qbar().move_to(_p(w / 2 - 0.27, -pin + 0.05))
    g = VGroup(box, tri, d_l, q_l, qb_l)
    g.box, g.tri, g.d_l, g.q_l, g.qb_l = box, tri, d_l, q_l, qb_l
    g.shift(center)
    return g


def bus_slash(x, y, label, color):
    s = Line(_p(x - 0.12, y - 0.17), _p(x + 0.12, y + 0.17)).set_stroke(color, 3)
    t = T(label, 28, color).next_to(s, UP, buff=0.08)
    return s, t


def logic_box(text, x, w=2.6, h=2.0):
    box = Rectangle(width=w, height=h).set_stroke(FG, 4).move_to(_p(x, 0))
    t = T(text, 28, line_spacing=0.85).move_to(box)
    return box, t


class Machines(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------ c1: definition, diagram
    def clip1(self):
        with self.say("c1.machines.1") as c:
            head = T("Finite State Machine", 52).move_to(_p(0, 3.0))
            self.play(*appear(head), run_time=min(1.2, c.until("def")))
            c.wait_until("def")

            dfn = T("a deterministic machine (circuit)\nthat produces outputs which depend on\n"
                    "its internal state and external inputs", 38, line_spacing=0.9,
                    t2c={"internal state": GREEN, "external inputs": BLUE}).move_to(_p(0, 1.0))
            self.play(*appear(dfn, shift=None), run_time=1.2)  # early: the definition is read as a whole
            c.wait_until("memory")

            ff = dff(_p(0, -2.45), w=1.3, h=1.7, pin=0.38)
            src = select(dfn, "internal state")[0]
            dst = T("internal state", 34, GREEN).next_to(ff, UP, buff=0.22)
            self.play(*appear(ff, shift=None), run_time=0.6)
            self.play(*fly(src, dst), run_time=min(1.3, c.until("diagram")))
            c.wait_until("diagram")

            d = moore_diagram()
            self.d = d
            sweep_clear(self, *appear(*d.circles, *d.names, shift=None, lag=0.15), run_time=1.6)
            c.wait_until("circles")

            self.play(*[VShowPassingFlash(ci.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for ci in d.circles], run_time=1.4)
            c.wait_until("arcs")

            for idx in d.by_state:
                self.play(*[Create(d.arcs[i]) for i in idx],
                          *appear(*[d.labels[i] for i in idx], shift=None, lag=0.15),
                          run_time=1.3)
            c.wait_until("later")

            tag = T("Part 5", 34, YELLOW).move_to(_p(4.6, -2.5))
            self.play(*appear(tag), run_time=0.8)  # early: "Part five" is in this sentence
            self.wait(max(0.0, c.remaining - 1.3))
            grp = VGroup(*d.circles, *d.names, *d.arcs, *d.labels, tag)
            self.play(grp.animate.scale(0.3).to_corner(UR, buff=0.5).set_opacity(0),
                      run_time=max(0.6, min(1.2, c.remaining)))
            self.remove(*grp.get_family())

    # ------------------------------------------------------------ c2: the Moore schematic
    def clip2(self):
        with self.say("c1.machines.2") as c:
            inp = T("Inputs", 32, BLUE).move_to(_p(-6.15, 0))
            in_w = Arrow(_p(-5.48, 0), _p(-4.7, 0), buff=0, stroke_width=4,
                         max_tip_length_to_length_ratio=0.3).set_color(BLUE)
            in_s, in_n = bus_slash(-5.05, 0, "n", BLUE)
            b1, b1t = logic_box("Next state\ncombinational\nlogic", -3.4)
            d_w = Arrow(_p(-2.1, 0), _p(-0.7, 0), buff=0, stroke_width=4,
                        max_tip_length_to_length_ratio=0.2).set_color(BLUE)
            d_s, d_m = bus_slash(-1.4, 0, "m", BLUE)
            ff = dff(_p(0, -0.45))
            qb_w = Line(_p(0.7, -0.9), _p(1.0, -0.9)).set_stroke(GREEN, 3)
            q_w = Arrow(_p(0.7, 0), _p(1.75, 0), buff=0, stroke_width=4,
                        max_tip_length_to_length_ratio=0.25).set_color(GREEN)
            q_s, q_m = bus_slash(1.42, 0, "m", GREEN)
            b2, b2t = logic_box("Optional\ncombinational\nlogic", 3.05)
            out_w = Arrow(_p(4.35, 0), _p(5.05, 0), buff=0, stroke_width=4,
                          max_tip_length_to_length_ratio=0.3).set_color(GREEN)
            outp = T("Outputs", 32, GREEN).next_to(out_w, RIGHT, buff=0.12)
            tap = Dot(_p(1.05, 0), radius=0.07, color=GREEN)
            loop_up = VMobject().set_points_as_corners([_p(1.05, 0), _p(1.05, 1.9), _p(-3.4, 1.9)])
            loop_up.set_stroke(GREEN, 4)
            loop_dn = Arrow(_p(-3.4, 1.9), _p(-3.4, 1.0), buff=0, stroke_width=4,
                            max_tip_length_to_length_ratio=0.3).set_color(GREEN)
            cs = T("Current state", 30, GREEN).move_to(_p(-1.2, 2.3))
            clk_w = Line(_p(0, -2.05), _p(0, -1.47)).set_stroke(YELLOW, 4)
            clk = T("CLK", 30, YELLOW).next_to(clk_w.get_start(), LEFT, buff=0.12)
            self.parts = dict(inp=inp, in_w=in_w, in_s=in_s, in_n=in_n, b1=b1, b1t=b1t, d_w=d_w,
                              ff=ff, q_w=q_w, b2=b2, b2t=b2t, out_w=out_w, outp=outp, clk=clk,
                              clk_w=clk_w, loop_up=loop_up, loop_dn=loop_dn, cs=cs)

            shown = [inp, in_w, in_s, in_n, b1, b1t, d_w, d_s, d_m, ff, qb_w, q_w, q_s, q_m, tap,
                     b2, b2t, out_w, outp, loop_up, loop_dn, cs]
            sweep_clear(self, *appear(*shown, shift=None, lag=0.04),  # early: whole schematic first, then walked
                        run_time=min(2.0, c.until("logic")))
            c.wait_until("logic")

            path = VMobject().set_points_as_corners([_p(1.05, 0), _p(1.05, 1.9), _p(-3.4, 1.9), _p(-3.4, 1.0)])
            self.play(VShowPassingFlash(Line(_p(-5.48, 0), _p(-4.7, 0)).set_stroke(YELLOW, 9), time_width=0.6),
                      VShowPassingFlash(path.copy().set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(b1, run_time=1.8, time_width=1.5),
                      run_time=1.8)
            c.wait_until("ffs")

            self.play(VShowPassingFlash(Line(_p(-2.1, 0), _p(-0.7, 0)).set_stroke(YELLOW, 9), time_width=0.6),
                      FlashAround(ff.box, run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("clk")

            self.play(*appear(clk, shift=None), Create(clk_w), run_time=1.2)
            c.wait_until("loop")

            self.play(VShowPassingFlash(path.copy().set_stroke(GREEN, 11), time_width=0.5),
                      run_time=2.2, rate_func=linear)
            self.play(*recolor(cs, YELLOW), run_time=0.6)
            self.play(*recolor(cs, GREEN), run_time=0.6)
            c.wait_until("outlogic")

            self.play(FlashAround(b2, run_time=1.5, time_width=1.5), run_time=1.5)
            self.play(VShowPassingFlash(Line(_p(4.35, 0), _p(5.05, 0)).set_stroke(YELLOW, 9), time_width=0.8),
                      FlashAround(outp, run_time=1.2, time_width=1.5), run_time=min(1.2, c.remaining))

    # ------------------------------------------------------------ c3: Moore vs Mealy, counters
    def clip3(self):
        P = self.parts
        with self.say("c1.machines.3") as c:
            moore = T("Moore: outputs from\nthe state alone", 30, line_spacing=0.85,
                      t2c={"Moore:": GREEN})
            moore.align_to(_p(2.45, 0), LEFT).align_to(_p(0, -1.35), UP)
            self.play(*appear(moore), run_time=1.2)
            c.wait_until("every machine")

            every = T("every machine today", 30, YELLOW).next_to(moore, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(*appear(every), run_time=1.0)  # early: tags the line being said
            c.wait_until("mealy")

            mpath = VMobject().set_points_as_corners([_p(-5.3, 0), _p(-5.3, -2.6), _p(2.2, -2.6), _p(2.2, -1.0)])
            mealy_w = DashedVMobject(mpath.set_stroke(BLUE, 4), num_dashes=60)
            m_dot = Dot(_p(-5.3, 0), radius=0.07, color=BLUE)
            mealy = T("Mealy: outputs also from the inputs", 30, t2c={"Mealy:": BLUE}).move_to(_p(-1.6, -3.05))
            self.play(Create(mealy_w), FadeIn(m_dot), time_span(FadeIn(mealy, shift=0.25 * DOWN), 0.7, 1.5),
                      run_time=1.5)
            c.wait_until("noinputs")
            self.play(*disappear(mealy_w, m_dot, mealy), run_time=0.8)

            gone = [P["inp"], P["in_w"], P["in_n"], P["in_s"]]
            self.play(*[m.animate.set_color(DIM) for m in gone], run_time=0.6)
            self.play(*[m.animate.shift(1.2 * LEFT).set_opacity(0) for m in gone],
                      run_time=min(1.0, c.until("counter")))
            self.remove(*gone)
            c.wait_until("counter")

            cnt = T("a counter (Lecture 6)", 38, GREEN).move_to(_p(0, -2.55))
            quote = T("“synchronous state machines (of which counters are a subset)”", 30, DIM,
                      slant=ITALIC).move_to(_p(0, -3.1))
            self.play(*disappear(moore, every), run_time=0.7)
            self.play(*appear(cnt), run_time=1.0)
            self.play(*appear(quote, shift=None), run_time=1.0)  # early: p. 120's words under the tag
            self.cnt = [cnt, quote]

    # ------------------------------------------------------------ c4: the design recipe
    def clip4(self):
        with self.say("c1.machines.4") as c:
            row = recipe_row(size=31)
            row.shift(-row.get_center() + 0.2 * UP)
            for ch in row.chips:
                ch.set_opacity(0.3)
                ch.box.set_fill(BG, 1)
            for a in row.arrows:
                a.set_opacity(0.3)
            sweep_clear(self, *appear(*row.chips, *row.arrows, shift=None, lag=0.1),  # early: recipe shown whole, then walked
                        run_time=1.8)

            for i, cue in enumerate(["s1", "s2", "s3", "s4"]):
                c.wait_until(cue)
                anims = [restyle(row.chips[i].box, op=1, outline=YELLOW),
                         row.chips[i].text.animate.set_opacity(1)]
                if i > 0:
                    anims += [restyle(row.chips[i - 1].box, outline=BLUE),
                              row.arrows[i - 1].animate.set_opacity(1)]
                self.play(*anims, run_time=min(1.0, c.until()))
            c.wait_until("dee")

            self.play(restyle(row.chips[3].box, outline=BLUE), Create(row.tie), run_time=0.6)
            self.play(*appear(row.dee, shift=0.25 * UP), run_time=1.0)
            self.play(FlashAround(row.dee, run_time=1.5, time_width=1.5), run_time=1.5)
