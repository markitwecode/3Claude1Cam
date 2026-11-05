"""Chapter 2, scene 1: the crew returns, 850M tokens, three kinds, $633, three questions.
Clips c2.hook.1 - c2.hook.3.

Helpers shared in spirit with later scenes:
  crew_tree()      master shot (ch1 s2 layout, rebuilt from the brief)
  question_cards() the three question cards (s4 reuses card 2, s6 card 1)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402


def _agent(w, h, label=None, size=30, mono=False, outline=BLUE, fill_op=0.15, label_color=FG):
    back = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(width=0).set_fill(BG, 1)
    rect = RoundedRectangle(corner_radius=0.15, width=w, height=h).set_stroke(outline, 3).set_fill(BLUE, fill_op)
    g = VGroup(back, rect)
    if label:
        t = (Mono if mono else T)(label, size=size, color=label_color)
        if t.width > w - 0.3:
            t.scale_to_fit_width(w - 0.3)
        g.add(t)
    return g


def _conn(a, b):
    return Line(a.get_bottom(), b.get_top()).set_stroke(DIM, 2).set_z_index(-1)


def crew_tree():
    """Master shot, copied from ch1_s2_crew.py. Returns (tree VGroup of top-level pieces,
    agent rects for tokens, label mobjects).
    you T36 YELLOW (0,3.4); producer 3.2x0.8 (0,2.45) T32; row y=1.0, boxes 2.8x0.7, T26:
    series-planner x-5.1; script-writer x-1.7 (+2 copies +0.1/+0.2 up-right); `vk voice` x1.7 DIM;
    chapter-director x5.1 (front lit, 2 DIM copies +0.08/+0.16); 8 builders 0.75x0.45 y-0.5,
    centred x3.0 gap 0.15; DIM T28 'scene-builder x 6-8' (3.0,-1.05); DIM width-2 connectors;
    DIM T26 'xN' tags at y0.42 in the writer/director boxes. Boxes: BLUE stroke 3, BLUE fill 0.15."""
    ROW = 26.5
    you = T("you", size=36, color=YELLOW).move_to([0, 3.4, 0])
    producer = _agent(3.2, 0.8, "producer", 32).move_to([0, 2.45, 0])
    planner = _agent(2.8, 0.7, "series-planner", ROW).move_to([-5.1, 1.0, 0])
    writers = VGroup(*[_agent(2.8, 0.7, "script-writer" if k == 0 else None, ROW)
                       .move_to([-1.7 + 0.1 * k, 1.0 + 0.1 * k, 0]) for k in (2, 1, 0)])
    voice = _agent(2.8, 0.7, "vk voice", ROW, mono=True, outline=DIM, label_color=DIM).move_to([1.7, 1.0, 0])
    dir_back = VGroup(*[_agent(2.8, 0.7, None, 28, outline=DIM, fill_op=0.06)
                        .move_to([5.1 + 0.08 * k, 1.0 + 0.08 * k, 0]) for k in (2, 1)])
    dir_front = _agent(2.8, 0.7, "chapter-director", ROW).move_to([5.1, 1.0, 0])
    xs = [3.0 + (i - 3.5) * 0.9 for i in range(8)]
    builders = [RoundedRectangle(corner_radius=0.15, width=0.75, height=0.45).set_stroke(BLUE, 3)
                .set_fill(BLUE, 0.15).move_to([x, -0.5, 0]) for x in xs]
    brow = VGroup(*builders)
    blabel = T("scene-builder × 6–8", size=28, color=DIM).move_to([3.0, -1.05, 0])
    top_conns = VGroup(Line(you.get_bottom() + 0.05 * DOWN, producer.get_top()).set_stroke(DIM, 2).set_z_index(-1),
                       *[_conn(producer, b) for b in (planner, writers[-1], voice, dir_front)])
    bconn = VGroup(*[_conn(dir_front, b) for b in builders])
    wfront = writers[-1]
    w_n = T("×N", size=ROW, color=DIM).move_to([wfront.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    d_n = T("×N", size=ROW, color=DIM).move_to([dir_front.get_right()[0] - 0.1, 0.42, 0], aligned_edge=RIGHT)
    tree = VGroup(top_conns, bconn, you, producer, planner, writers, voice, dir_back, dir_front,
                  brow, blabel, w_n, d_n)
    agents = [producer[1], planner[1], wfront[1], dir_front[1]] + [b for b in builders]
    labels = [you, producer[2], planner[2], wfront[2], voice[2], dir_front[2], blabel, w_n, d_n]
    return tree, agents, labels


def token_mark(box_rect):
    d = VGroup(Circle(radius=0.15, color=GOLD, fill_color=GOLD, fill_opacity=1, stroke_width=2),
               Circle(radius=0.07, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0))
    d.move_to(box_rect.get_corner(UR))
    d.set_z_index(3)
    return d


# ---- question cards: box 11.6 x 1.7, rows y 2.4 / 0.1 / -2.2; text T34 left-aligned; unlit =
#      DIM outline + FG text, lit = YELLOW outline + YELLOW text, dimmed = restyle(DIMMED) ----
CARD_TEXT = [
    "Can any step run on Sonnet instead of Opus?",
    "Do we need so many scene-builders per chapter?\nStarting an agent costs money.",
    "How does scene building work?\nWhat does each agent do?",
]


def question_cards():
    cards = []
    for i, s in enumerate(CARD_TEXT):
        r = RoundedRectangle(corner_radius=0.2, width=11.6, height=1.7, stroke_color=DIM,
                             stroke_width=3, fill_color=BG, fill_opacity=1)
        t = T(s, size=34, line_spacing=0.9).move_to(r).align_to(r, LEFT).shift(0.5 * RIGHT)
        g = VGroup(r, t)
        g.box, g.text = r, t
        g.move_to([0, 2.4 - 2.3 * i, 0])
        cards.append(g)
    return cards


def card_lit(card):
    return [card.box.animate.set_stroke(YELLOW), card.text.animate.set_color(YELLOW)]


class Ch2S1Hook(NarratedScene):
    def construct(self):
        # ---- clip 1
        with self.say("c2.hook.1") as c:
            card = title_card("Part 2 · Where the tokens go")
            card.scale(0.8)
            self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                      time_span(FadeIn(card.course), 0.2, 0.6), time_span(FadeIn(card.part), 0.4, 0.8),
                      run_time=0.8)
            c.wait_until("crew")
            tree, agents, labs = crew_tree()
            self.play(FadeOut(card), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(p) for p in tree.submobjects], lag_ratio=0.18),
                      run_time=c.until("costs", floor=1.5))
            settle(self, tree)
            c.wait_until("costs")
            toks = [token_mark(a) for a in agents]
            self.play(LaggedStart(*[FadeIn(t, scale=2) for t in toks], lag_ratio=0.1), run_time=2.0)
            settle(self, tree, add=toks)
            c.wait_until("total")
            self.play(*[FadeOut(t) for t in labs], tree.animate.scale(0.38).move_to([-4.1, 2.6, 0]),
                      run_time=1.5)
            c1 = T("9 producer sessions", size=40, color=GOLD).move_to([2.4, 3.2, 0])
            c2 = T("175 sub-agent runs", size=40, color=GOLD).move_to([2.4, 2.4, 0])
            total = T("≈ 850 million tokens", size=60, color=GOLD).move_to([0, 0.4, 0])
            c.wait_until("nine producer sessions")
            self.play(FadeIn(c1, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("a hundred and seventy-five")
            self.play(FadeIn(c2, shift=0.3 * DOWN), run_time=0.8)
            c.wait_until("eight hundred and fifty million tokens")
            self.play(c1.animate.move_to(total).set_opacity(0),
                      c2.animate.move_to(total).set_opacity(0),
                      time_span(FadeIn(total), 0.5, 1.5), run_time=1.6)
            self.remove(c1, c2)
            c.wait_until("kinds")
            x0, s = -5.5, 11.0 / 794
            specs = [(794, GREEN, "794M cache reads", -1.0), (39.5, GOLD, "39.5M cache writes", -2.0),
                     (13.8, RED, "13.8M output", -3.0)]
            bars = []
            for v, col, lab, y in specs:
                b = Rectangle(width=v * s, height=0.6, stroke_width=0, fill_color=col, fill_opacity=1)
                b.move_to([x0 + v * s / 2, y, 0])
                if v > 100:
                    t = T(lab, size=32, color=BG).move_to(b)
                else:
                    t = T(lab, size=32, color=col).next_to(b, RIGHT, buff=0.25)
                bars.append((b, t))
            self.play(GrowFromEdge(bars[0][0], LEFT), FadeIn(bars[0][1]), run_time=1.0)
            self.play(*[GrowFromEdge(b, LEFT) for b, _ in bars[1:]],
                      *[FadeIn(t, shift=0.2 * RIGHT) for _, t in bars[1:]], run_time=0.7)

        # ---- clip 2
        with self.say("c2.hook.2") as c:
            dollars = T("≈ $633 at Opus list prices", size=44, color=GOLD).move_to([2.4, 3.1, 0])
            unit = T("subscription: a unit for comparing parts,\nnot money spent", size=28,
                     color=DIM, line_spacing=0.9).move_to([2.4, 2.2, 0])
            self.play(FadeIn(dollars, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("unit")
            self.play(FadeIn(unit, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("question")
            q = T("Where does it go?\nWhat can we cut without making the videos worse?",
                  size=40, color=YELLOW, line_spacing=1.0)
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
            self.play(FadeIn(q, shift=0.3 * UP), run_time=0.7)

        # ---- clip 3
        with self.say("c2.hook.3") as c:
            cards = question_cards()
            c.wait_until("three questions")
            self.play(FadeOut(q), LaggedStart(*[FadeIn(k, shift=0.3 * UP) for k in cards],
                                              lag_ratio=0.3), run_time=1.8)
            c.wait_until("sonnet")
            self.play(*card_lit(cards[0]), run_time=0.8)
            c.wait_until("many")
            self.play(*card_lit(cards[1]), run_time=0.8)
            c.wait_until("how")
            self.play(*card_lit(cards[2]), run_time=0.8)
            c.wait_until("third")
            tag = T("Part 1", size=30, color=GREEN).move_to(cards[2].box.get_right() + 1.1 * LEFT)
            self.play(restyle(cards[2], DIMMED), FadeIn(tag, shift=0.2 * DOWN), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
