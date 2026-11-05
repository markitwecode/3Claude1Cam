"""Chapter 1, scene 1: Hook. Lawrence and Radcliffe, the Bacon query, two questions. Clips c1.hook.1 – c1.hook.3."""
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
from lib.titles import title_card  # noqa: E402

PAIR_Y = 0.3      # centre line of the two big vertices
PAIR_X = 4.8


def vertex(name=None, color=PINK, r=0.5, stroke=4, size=30):
    """Lecture-wide vertex: circle (stroke `color`, fill `color` at 0.2 over BG), name in FG under it."""
    c = Circle(radius=r).set_stroke(color, stroke).set_fill(interpolate_color(ManimColor(BG), ManimColor(color), 0.2), 1)
    g = VGroup(c)
    g.circle = c
    if name:
        lab = T(name, size)
        lab.next_to(c, DOWN, buff=0.2)
        g.add(lab)
        g.label = lab
    return g


def pair():
    """Jennifer Lawrence (left) and Daniel Radcliffe (right), PINK vertices, joined by a dashed arc of
    small alternating Movie/Person circles, with a YELLOW "?" over it.
    VGroup(lawrence, radcliffe, chain, q); lawrence/radcliffe = VGroup(circle, name); chain = VGroup(dashed, *dots)."""
    jl = vertex("Jennifer Lawrence")
    dr = vertex("Daniel Radcliffe")
    jl.circle.move_to([-PAIR_X, PAIR_Y, 0])
    jl.label.next_to(jl.circle, DOWN, buff=0.2)
    dr.circle.move_to([PAIR_X, PAIR_Y, 0])
    dr.label.next_to(dr.circle, DOWN, buff=0.2)
    arc = ArcBetweenPoints(jl.circle.get_right(), dr.circle.get_left(), angle=-0.6 * PI)
    dashed = DashedVMobject(arc, num_dashes=44, dashed_ratio=0.55).set_stroke(FG, 3)
    dots = []
    for k in range(1, 6):
        col = BLUE if k % 2 else PINK
        d = vertex(color=col, r=0.2, stroke=3)
        d.move_to(arc.point_from_proportion(k / 6))
        dots.append(d)
    chain = VGroup(dashed, *dots)
    q = T("?", 64, YELLOW).next_to(arc, UP, buff=0.25)
    return VGroup(jl, dr, chain, q)


def result_table():
    """The result, transposed to fit under the query: a bacon_number row over a people row."""
    nums = ["1", "2", "3", "4", "5", "6", "7", "8"]
    ppl = ["107", "3,519", "8,631", "1,676", "364", "212", "62", "9"]
    h1, h2 = T("bacon_number", 28), T("people", 28)
    h2.next_to(h1, DOWN, buff=0.3).align_to(h1, LEFT)
    head = VGroup(h1, h2)
    x0 = h1.get_right()[0] + 0.85
    body = VGroup()
    for i, (a, b) in enumerate(zip(nums, ppl)):
        x = x0 + 1.12 * i
        body.add(VGroup(T(a, 28, GOLD).move_to([x, h1.get_y(), 0]),
                        T(b, 28, GOLD).move_to([x, h2.get_y(), 0])))
    mid = (h1.get_bottom()[1] + h2.get_top()[1]) / 2
    rule = Line([h1.get_left()[0], mid, 0], [body.get_right()[0] + 0.1, mid, 0]).set_stroke(DIM, 2)
    t = VGroup(head, rule, body)
    t.head, t.rule, t.body = head, rule, body
    return t


QUERY = """MATCH path = allShortestPaths(
(kb:Person {name: 'Kevin Bacon'})
-[:ACTED_IN*]-
(p:Person))
WHERE p.person_id <> kb.person_id
RETURN length(path) / 2 AS bacon_number,
count(DISTINCT p.person_id) AS people
ORDER BY bacon_number;"""


class Hook(NarratedScene):
    def ripple(self, center, n=2, run_time=2.4):
        rings = [Circle(radius=0.7).set_stroke(PINK, 3, opacity=0.55).move_to(center) for _ in range(n)]
        self.add(*rings)
        self.play(LaggedStart(*[r.animate.scale(5).set_stroke(opacity=0) for r in rings], lag_ratio=0.45),
                  run_time=run_time, rate_func=linear)
        self.remove(*rings)

    def construct(self):
        P = pair()
        jl, dr, chain, q = P
        dashed, dots = chain[0], list(chain[1:])

        # ---- c1.hook.1: title, the pair, 0 films, the chain
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · From tables and trees to graphs")
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule), run_time=1.0)  # early: title card
            self.play(FadeIn(card.course, shift=0.2 * DOWN), run_time=0.9)  # early: title card
            self.play(FadeIn(card.part, shift=0.2 * DOWN), run_time=0.9)  # early: title card
            c.wait_until("two")
            sweep_clear(self, time_span(FadeIn(jl.circle, scale=0.6), 0.45, 1.05),
                        time_span(FadeIn(dr.circle, scale=0.6), 0.6, 1.2), run_time=1.2)
            c.wait_until("Jennifer Lawrence", own_word=jl.label)
            self.play(*appear(jl.label), run_time=0.8)
            c.wait_until("Daniel Radcliffe", own_word=dr.label)
            self.play(*appear(dr.label), run_time=0.8)

            zero = T("0 films together", 36, GOLD).move_to([0, PAIR_Y, 0])
            c.wait_until("never", own_word=zero)
            self.play(*appear(zero), run_time=1.0)

            c.wait_until("chain")
            self.play(Create(dashed), run_time=min(2.5, c.until("co-stars")))
            c.wait_until("co-stars")
            self.play(*appear(*dots, shift=None, lag=0.4), run_time=min(2.5, c.until("one link")))
            c.wait_until("how short")
            self.play(*appear(q), run_time=1.0)
        settle(self, P)

        # ---- c1.hook.2: Kevin Bacon, the query, its result
        with self.say("c1.hook.2") as c:
            P.save_state()
            kb = vertex("Kevin Bacon", size=36).scale(1.4).move_to(0.3 * UP)
            kb_label = kb.label
            self.play(*disappear(zero), *set_alpha([jl.label, dr.label, q], 0), run_time=0.6)
            self.play(P.animate.scale(0.35).to_corner(UL, buff=0.4),
                      FadeIn(kb.circle, scale=0.6), run_time=1.5)
            self.ripple(kb.circle.get_center(), n=2, run_time=min(2.2, c.until("kevin bacon")))
            c.wait_until("kevin bacon")
            self.play(*appear(kb_label), run_time=1.0)
            self.ripple(kb.circle.get_center(), n=2, run_time=min(2.2, max(0.5, c.until("query") - 0.1)))

            code = Code(QUERY, size=32, line_spacing=0.72)
            code.move_to(0.6 * DOWN)
            c.wait_until("query")
            self.play(kb.animate.scale(0.6).to_corner(UR, buff=0.5), run_time=1.2)
            self.play(*appear(code, shift=None), run_time=1.0)

            table = result_table()
            c.wait_until("result")
            code.generate_target()
            code.target.scale(0.875).move_to([0, 1.85 - code.height * 0.875 / 2, 0])
            table.next_to(code.target, DOWN, buff=0.45)
            self.play(MoveToTarget(code), run_time=1.2)
            self.play(*appear(table.head, table.rule, shift=None, lag=0.2), run_time=0.8)
            self.play(*appear(*table.body, shift=None, lag=0.3), run_time=1.4)

        # ---- c1.hook.3: the two questions
        with self.say("c1.hook.3") as c:
            sweep_clear(self, time_span(Restore(P), 0.5, 1.6), keep=[P], run_time=1.6)
            self.play(*set_alpha([jl.label, dr.label, q], 0.4), run_time=0.8)
            q1 = T("What shape is this data?", 44, YELLOW).move_to(1.8 * DOWN)
            q2 = T("What language fits that shape?", 44, YELLOW).next_to(q1, DOWN, buff=0.35)
            c.wait_until("q1")
            self.play(*appear(q1), run_time=1.0)
            c.wait_until("q2")
            self.play(*appear(q2), run_time=1.0)
        self.wait(3.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
