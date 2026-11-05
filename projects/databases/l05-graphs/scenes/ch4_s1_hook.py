"""Chapter 4, scene 1: Hook. Lawrence and Radcliffe share no film, yet a chain links them; Six Degrees of Kevin Bacon. Clips c4.hook.1 – c4.hook.2."""
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
from lib.titles import title_card  # noqa: E402

PAIR_X = 4.8
PAIR_Y = -1.0
R_PAT = 0.6                  # vertex radius in the "last time" pattern

# Re-wrapped from the brief's 3 lines (68 chars is too wide for the frame); same tokens.
COSTAR = ("MATCH (a:Person {name: 'Jennifer Lawrence'})\n"
          "      -[:ACTED_IN]-> (m:Movie) <-[:ACTED_IN]-\n"
          "      (b:Person {name: 'Daniel Radcliffe'})\n"
          "RETURN m.title;")


# ---------------------------------------------------------------- shared drawing (ch1 s1's look)
def vertex(name=None, color=PINK, r=0.5, stroke=4, size=30):
    """Lecture-wide vertex: circle (stroke `color`, fill `color` at 0.2 over BG), name in FG under it."""
    c = Circle(radius=r).set_stroke(color, stroke).set_fill(
        interpolate_color(ManimColor(BG), ManimColor(color), 0.2), 1)
    g = VGroup(c)
    g.circle = c
    if name:
        lab = T(name, size)
        lab.next_to(c, DOWN, buff=0.2)
        g.add(lab)
        g.label = lab
    return g


def dashed_chain(p0, p1, n, angle=0.0, r=0.2):
    """A dashed path p0 -> p1 with n small circles on it, alternating Movie BLUE / Person PINK."""
    path = ArcBetweenPoints(p0, p1, angle=angle) if angle else Line(p0, p1)
    length = np.linalg.norm(np.array(p1) - np.array(p0)) * (1.3 if angle else 1.0)
    dashed = DashedVMobject(path, num_dashes=max(8, int(length / 0.2)), dashed_ratio=0.55).set_stroke(FG, 3)
    dots = []
    for k in range(1, n + 1):
        d = vertex(color=BLUE if k % 2 else PINK, r=r, stroke=3)
        d.move_to(path.point_from_proportion(k / (n + 1)))
        dots.append(d)
    g = VGroup(dashed, *dots)
    g.path = path
    return g


def pair():
    """VGroup(lawrence, radcliffe, chain, q), as ch1 s1 draws it."""
    jl = vertex("Jennifer Lawrence")
    dr = vertex("Daniel Radcliffe")
    jl.circle.move_to([-PAIR_X, PAIR_Y, 0])
    jl.label.next_to(jl.circle, DOWN, buff=0.2)
    dr.circle.move_to([PAIR_X, PAIR_Y, 0])
    dr.label.next_to(dr.circle, DOWN, buff=0.2)
    chain = dashed_chain(jl.circle.get_right(), dr.circle.get_left(), 5, angle=-0.45 * PI)
    q = T("?", 64, YELLOW).next_to(chain.path, UP, buff=0.25)
    g = VGroup(jl, dr, chain, q)
    g.jl, g.dr, g.chain, g.q = jl, dr, chain, q
    return g


def open_card():
    """This scene's first frame = ch3_s6_recap's last frame. Static, no updaters.
    VGroup(pair, line): pair = VGroup(lawrence, radcliffe, chain, q); line = YELLOW 'chains of any length'."""
    p = pair()
    line = T("chains of any length", 40, YELLOW).move_to([0, -3.0, 0])
    g = VGroup(p, line)
    g.pair, g.line = p, line
    return g


def pat_vertex(text, color, at):
    v = vertex(color=color, r=R_PAT).move_to(at)
    lab = T(text, 36, slant=ITALIC).move_to(v)
    g = VGroup(v, lab)
    g.circ = v.circle
    return g


def edge(a, b, text, size=30):
    s, e = a.circ.get_center(), b.circ.get_center()
    arr = Arrow(s, e, buff=R_PAT + 0.06, stroke_width=4, color=FG, max_tip_length_to_length_ratio=0.12)
    lab = set_backstroke(T(text, size=size)).next_to(arr, UP, buff=0.2)
    return arr, lab


def reply_table():
    head = Mono("m.title", 32)
    rule = Line(LEFT, RIGHT).set_stroke(DIM, 2).set_width(3.2).next_to(head, DOWN, buff=0.18)
    box = Rectangle(width=3.6, height=1.5).set_stroke(DIM, 2)
    box.move_to(VGroup(head, rule)).align_to(head, UP).shift(0.2 * UP)
    rows = T("0 rows", 36, t2c={"0": GOLD}).next_to(box, DOWN, buff=0.3)
    g = VGroup(box, head, rule, rows)
    g.rows = rows
    return g


class Hook(NarratedScene):
    def construct(self):
        card = open_card()
        self.add(card)
        self.wait(1.0)
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ------------------------------------------------------------------ clip 1
    def clip1(self):
        tc = title_card("Part 4 · Paths of any length")
        # Short lead-in: the ch3 card gives way to the title before "This is part four" begins.
        sweep_clear(self,  # early: title card
                    time_span(FadeIn(tc.title, shift=0.3 * DOWN), 0.35, 0.8),
                    time_span(GrowFromCenter(tc.rule), 0.35, 0.8),
                    time_span(FadeIn(tc.course), 0.45, 0.8),
                    time_span(FadeIn(tc.part), 0.5, 0.8),
                    run_time=0.8)
        with self.say("c4.hook.1") as c:
            c.wait_until("last")

            # Last time: the co-star pattern as a graph
            a = pat_vertex("a", PINK, [-4.2, 0.2, 0])
            m = pat_vertex("m", BLUE, [0, 0.2, 0])
            b = pat_vertex("b", PINK, [4.2, 0.2, 0])
            a1, l1 = edge(a, m, "ACTED_IN")
            a2, l2 = edge(b, m, "ACTED_IN")
            diagram = VGroup(a, m, b, a1, a2, l1, l2)
            sweep_clear(self, FadeIn(diagram), run_time=1.8)
            c.wait_until("counted")
            self.play(FlashAround(m.circ, color=GOLD, run_time=1.5, time_width=1.5))
            c.wait_until("costar")

            code = Code(COSTAR, size=30).move_to([0, 1.5, 0])
            self.code = code
            sweep_clear(self, FadeIn(code), run_time=min(1.8, c.until("none")))
            c.wait_until("none")

            table = reply_table().move_to([0, -1.9, 0])
            self.play(*appear(table[:3], table.rows, lag=0.4), run_time=1.2)
            c.wait_until("Zero rows")
            self.play(FlashAround(table.rows, color=GOLD, run_time=1.5, time_width=1.5))
            c.wait_until("Katniss")

            jl = code.find("'Jennifer Lawrence'")
            self.play(FlashUnder(jl, color=PINK, run_time=1.2), *recolor(jl, PINK), run_time=1.2)
            c.wait_until("Harry Potter")
            dr = code.find("'Daniel Radcliffe'")
            self.play(FlashUnder(dr, color=PINK, run_time=1.2), *recolor(dr, PINK), run_time=1.2)
            c.wait_until("chain")

            p = pair()
            self.pair = p
            self.play(*during(disappear(table), 0, 0.4),
                      *during([code.animate.scale(28 / 30).move_to([0, 2.65, 0])], 0.15, 0.7),
                      *during(appear(p.jl, p.dr, p.chain, p.q, lag=0.15), 0.45, 1),
                      run_time=c.until(floor=1.5))

    # ------------------------------------------------------------------ clip 2
    def clip2(self):
        p, code = self.pair, self.code
        with self.say("c4.hook.2", gap=2.5) as c:
            self.play(*disappear(code), run_time=0.8)
            names = [p.jl.label, p.dr.label]
            p.remove(p.jl, p.dr)
            p.add(p.jl.circle, p.dr.circle)
            self.remove(*p.jl.get_family(), *p.dr.get_family())
            self.add(p, *names)
            p.generate_target()
            p.target.scale(0.5).move_to([0, 2.9, 0])
            self.play(*during(disappear(*names), 0, 0.4), *during(MoveToTarget(p), 0.25, 1), run_time=1.8)

            bacon = vertex("Kevin Bacon", r=0.6, size=32).move_to([0, -0.6, 0])
            bacon.label.next_to(bacon.circle, DOWN, buff=0.2)
            c.wait_until(own_word=bacon.label)
            self.play(*appear(bacon), run_time=1.0)
            c.wait_until("rules")

            bc = bacon.circle.get_center()
            spokes = []
            for at, n in [((-3.4, 0.5), 1), ((-5.6, -1.9), 3), ((5.6, 0.8), 5), ((5.4, -2.2), 7)]:
                at = np.array([at[0], at[1], 0.0])
                actor = vertex(r=0.4).move_to(at)
                d = (at - bc) / np.linalg.norm(at - bc)
                ch = dashed_chain(bc + 0.6 * d, at - 0.4 * d, n, r=0.15)
                nrm = np.array([-d[1], d[0], 0])
                if nrm[1] < 0:
                    nrm = -nrm
                q = T("?", 48, GOLD).move_to(ch.path.get_center() + 0.5 * nrm)
                spokes.append((VGroup(ch, actor), q))
            self.play(*appear(*[s for s, _ in spokes], shift=None, lag=0.5),
                      run_time=min(3.5, 0.8 * c.until("unknown")))
            c.wait_until("unknown")
            self.play(*appear(*[q for _, q in spokes], lag=0.25), run_time=1.4)
            c.wait_until("question")

            ask = T("a chain of unknown length?", 40, YELLOW).move_to([0, -3.3, 0])
            self.play(*appear(ask), run_time=1.0)
