"""Chapter 4, scene 2: chains of co-stars, alternating directions, and Slide 107's *4 query.
Clips c4.chains.1 – c4.chains.3.

Exports (reused by s3, s6 and the recap):
  chain_example(arrows=True) -> VGroup, nodes centred on y = 0, x = PITCH * (i - 2).
      .nodes[5] (Circle; PINK person / BLUE movie)  .names[5] (T 30, node colour, under the node)
      .edges[4] (Arrow, or plain Line when arrows=False; edge 0, 2 point right, 1, 3 point left)
      .types[4] (T 30 "ACTED_IN", DIM, above each edge)  .slot(i) -> point above edge i (counter row)
  slide107_code() -> Code (size 30) of Slide 107's query, centred on ORIGIN.
  handover_shot() -> the plain-line chain scaled 0.94, node row at y = TOP_Y (s3 opens on it).
"""
# style: 2
# handover: next
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

PITCH = 2.9          # node spacing along the chain
NODE_R = 0.4
CHAIN_Y = 0.4        # node row while the chain is the hero (clips 1-2)
TOP_Y = 2.3          # node row once shrunk to the top (clip 3, handover)
TOP_SCALE = 0.94
NAMES = [("Jennifer\nLawrence", PINK), ("The Hunger Games:\nCatching Fire", BLUE),
         ("Woody\nHarrelson", PINK), ("Now You See\nMe 2", BLUE), ("Daniel\nRadcliffe", PINK)]
# edge i joins nodes i and i+1; True = points right (person -> movie on its right)
RIGHTWARD = [True, False, True, False]
SLIDE107 = ("MATCH path = (a:Person {name: 'Jennifer Lawrence'})\n"
            "             -[:ACTED_IN*4]-\n"
            "             (b:Person {name: 'Daniel Radcliffe'})\n"
            "RETURN count(path);")
EDGE_PATTERN = "-[:ACTED_IN]->"
EITHER_PATTERN = "-[:ACTED_IN]-"


def chain_example(arrows=True):
    xs = [PITCH * (i - 2) for i in range(5)]
    nodes, names, edges, types = [], [], [], []
    for x, (name, col) in zip(xs, NAMES):
        c = Circle(radius=NODE_R, color=col, stroke_width=4).set_fill(col, 0.15).move_to([x, 0, 0])
        n = T(name, size=30, color=col, line_spacing=0.8).next_to(c, DOWN, buff=0.18)
        nodes.append(c)
        names.append(n)
    for i, right in enumerate(RIGHTWARD):
        a, b = xs[i] + NODE_R + 0.08, xs[i + 1] - NODE_R - 0.08
        s, e = (np.array([a, 0, 0]), np.array([b, 0, 0])) if right else \
            (np.array([b, 0, 0]), np.array([a, 0, 0]))
        if arrows:
            ed = Arrow(s, e, buff=0, stroke_width=4, color=FG, tip_length=0.24,
                       max_tip_length_to_length_ratio=0.2)
        else:
            ed = Line(s, e, stroke_width=4, color=FG)
        edges.append(ed)
        types.append(T("ACTED_IN", size=30, color=DIM).move_to([(xs[i] + xs[i + 1]) / 2, 0, 0])
                     .shift(0.62 * UP))
    g = VGroup(*nodes, *names, *edges, *types)
    g.nodes, g.names, g.edges, g.types = nodes, names, edges, types

    def slot(i):
        t = g.types[i]
        return t.get_center() + (t.height / 2 + 0.5) * UP * (g.nodes[0].width / (2 * NODE_R))
    g.slot = slot
    return g


def slide107_code():
    c = Code(SLIDE107, size=30)
    if c.width > 12.6:
        c.scale_to_fit_width(12.6)
    return c.move_to(ORIGIN)


def to_top(ch):
    """The chain (built at y = 0) shrunk to the top of the frame."""
    return ch.scale(TOP_SCALE, about_point=ORIGIN).shift(TOP_Y * UP)


def handover_shot():
    return to_top(chain_example(arrows=False))


def counter(s, at, size=40):
    return T(s, size=size, color=GOLD).move_to(at)


class Chains(NarratedScene):
    def construct(self):
        ch = chain_example(arrows=True).shift(CHAIN_Y * UP + PITCH * RIGHT)   # first three centred
        self.ch = ch
        extra = self.clip1(ch)
        self.clip2(ch, extra)
        self.clip3(ch)

    # ---------------------------------------------------------------- clip 1
    def clip1(self, ch):
        with self.say("c4.chains.1") as c:
            c.wait_until("Jennifer")
            self.play(*appear(ch.nodes[0], ch.names[0]), run_time=0.9)
            c.wait_until("Woody")
            self.play(*appear(ch.nodes[2], ch.names[2]), run_time=0.9)
            c.wait_until("Catching Fire")
            self.play(*appear(ch.nodes[1], ch.names[1]), *[GrowArrow(e) for e in ch.edges[:2]],
                      run_time=1.0)
            self.play(*appear(*ch.types[:2], lag=0.2), run_time=0.8)

            k = [counter(str(i + 1), ch.slot(i)) for i in range(4)]
            for i, cue in ((0, "from her"), (1, "two arrows")):
                c.wait_until(cue)
                e = ch.edges[i]
                self.play(*appear(k[i]),
                          VShowPassingFlash(Line(e.get_start(), e.get_end(), color=YELLOW,
                                                 stroke_width=7), time_width=0.6),
                          run_time=0.9)

            bot = min(n.get_bottom()[1] for n in ch.names[:3])
            b2 = span_brace(np.array([ch.nodes[0].get_left()[0], bot, 0]),
                            np.array([ch.nodes[2].get_right()[0], bot, 0]))
            l2 = T("length 2 = co-stars", size=32, t2c={"2": GOLD}).next_to(b2, DOWN, buff=0.15)
            c.wait_until("joined by a path")
            self.play(GrowFromCenter(b2), run_time=0.8)
            c.wait_until("length two")
            self.play(*appear(l2), run_time=0.9)

            # room on the right for the next two
            c.wait_until("three")
            present = [ch.nodes[0], ch.nodes[1], ch.nodes[2], ch.names[0], ch.names[1], ch.names[2],
                       *ch.edges[:2], *ch.types[:2], k[0], k[1], b2, l2]
            self.play(*[m.animate.shift(PITCH * LEFT) for m in present],
                      run_time=min(1.2, c.until("Daniel")))
            for m in [ch.nodes[3], ch.nodes[4], ch.names[3], ch.names[4], *ch.edges[2:], *ch.types[2:],
                      k[2], k[3]]:
                m.shift(PITCH * LEFT)
            c.wait_until("Daniel")
            self.play(*appear(ch.nodes[4], ch.names[4]), run_time=0.9)
            c.wait_until("Now You See")
            self.play(*appear(ch.nodes[3], ch.names[3]), *[GrowArrow(e) for e in ch.edges[2:]],
                      run_time=1.0)
            self.play(*appear(*ch.types[2:], lag=0.2), run_time=0.8)
            settle(self, ch)

            for i, cue in ((2, "to Radcliffe"), (3, "four arrows")):
                c.wait_until(cue)
                e = ch.edges[i]
                self.play(*appear(k[i]),
                          VShowPassingFlash(Line(e.get_start(), e.get_end(), color=YELLOW,
                                                 stroke_width=7), time_width=0.6),
                          run_time=0.8)

            b4 = span_brace(np.array([ch.nodes[0].get_left()[0], l2.get_bottom()[1], 0]),
                            np.array([ch.nodes[4].get_right()[0], l2.get_bottom()[1], 0]))
            l4 = T("length 4 = a co-star in common", size=32, t2c={"4": GOLD}).next_to(b4, DOWN, buff=0.15)
            c.wait_until("path of length", nth=1)
            self.play(GrowFromCenter(b4), run_time=0.7)
            c.wait_until("length four")
            self.play(*appear(l4), run_time=0.9)
        return dict(k=k, braces=[b2, l2, b4, l4])

    # ---------------------------------------------------------------- clip 2
    def clip2(self, ch, extra):
        k, braces = extra["k"], extra["braces"]
        with self.say("c4.chains.2") as c:
            c.wait_until("alt")
            self.play(*disappear(*k), *[FlashAround(e.tip, run_time=1.2, buff=0.08) for e in ch.edges],
                      run_time=1.2)
            tags = [Mono("→" if r else "←", size=40, color=YELLOW).move_to(ch.slot(i))
                    for i, r in enumerate(RIGHTWARD)]
            cues = [("forward", 0), ("backward", 0), ("forward", 1), ("backward", 1)]
            for i, (cue, nth) in enumerate(cues):
                c.wait_until(cue, nth=nth)
                anims = [*appear(tags[i]), ch.edges[i].animate.set_color(YELLOW)]
                if i:
                    anims.append(ch.edges[i - 1].animate.set_color(FG))
                self.play(*anims, run_time=0.6 if i else 0.8)

            # one fixed pattern, stamped along the chain
            hero = Code(EDGE_PATTERN, size=48).move_to([0, 3.05, 0])
            c.wait_until("edge pattern")
            self.play(*appear(hero), ch.edges[3].animate.set_color(FG), run_time=1.0)
            c.wait_until("If every step")
            self.play(*disappear(*tags, *braces), run_time=1.0)

            stamp = Code(EDGE_PATTERN, size=28).move_to(ch.slot(0))
            c.wait_until("first edge")
            self.play(*fly(hero, stamp), run_time=1.3)
            ok = check_mark().scale(0.8).next_to(stamp, UP, buff=0.12)
            c.wait_until("would fit")
            self.play(ch.edges[0].animate.set_color(GREEN), GrowFromCenter(ok), run_time=0.8)
            c.wait_until("second")
            self.play(stamp.animate.move_to(ch.slot(1)), run_time=1.0)
            bad = cross_mark().scale(0.8).next_to(stamp, UP, buff=0.12)
            c.wait_until("would fail")
            self.play(ch.edges[1].animate.set_color(RED), GrowFromCenter(bad), run_time=0.8)

            # the headless arrow of part two
            c.wait_until("drop")
            self.play(*disappear(stamp, ok, bad),
                      *[e.animate.set_color(FG) for e in ch.edges[:2]], run_time=0.9)
            hero2 = Code(EITHER_PATTERN, size=48)
            hero2.move_to(hero).align_to(hero, LEFT)
            c.wait_until("no heads")
            self.play(*edit(hero, hero2), run_time=1.5)
            c.wait_until("either direction")
            lines = chain_example(arrows=False).shift(CHAIN_Y * UP).edges
            self.play(*[Transform(e, l) for e, l in zip(ch.edges, lines)], run_time=1.4)
            c.wait_until("either")
            self.play(*[VShowPassingFlash(l.copy().set_color(TEAL).set_stroke(width=7), time_width=0.6)
                        for l in lines], FlashAround(hero2, run_time=1.6, time_width=1.5),
                      run_time=1.6)
        self.hero2 = hero2

    # ---------------------------------------------------------------- clip 3
    def clip3(self, ch):
        code = slide107_code()
        code.move_to([0, 0, 0]).align_to([0, 0.5, 0], UP)
        with self.say("c4.chains.3", gap=2.4) as c:
            self.play(*during(disappear(self.hero2), 0, 0.45),
                      *during([ch.animate.scale(TOP_SCALE, about_point=CHAIN_Y * UP)
                               .shift((TOP_Y - CHAIN_Y) * UP)], 0.1, 0.9),
                      run_time=1.2)
            self.play(*appear(code, shift=None), run_time=1.0)
            c.wait_until("path")
            self.play(*recolor(code.find("path ="), YELLOW), run_time=0.8)
            outline = SurroundingRectangle(ch, color=YELLOW, buff=0.15, corner_radius=0.15)
            c.wait_until("whole matched path")
            self.play(FadeIn(outline), run_time=1.0)

            for nm, i in (("'Jennifer Lawrence'", 0), ("'Daniel Radcliffe'", 4)):
                c.wait_until(nm.split()[1].strip("'"))
                self.play(FlashAround(code.find(nm), run_time=1.2, time_width=1.5),
                          FlashAround(VGroup(ch.nodes[i], ch.names[i]), run_time=1.2, time_width=1.5),
                          run_time=1.2)

            line1 = code.line(1)
            star = code.find("*4")
            c.wait_until("star four")
            box = token_box(star, line1)
            self.play(FadeIn(box), *recolor(star, GOLD), run_time=1.0)
            c.wait_until("inside the square")
            self.play(Transform(box, token_box(code.find("[:ACTED_IN*4]"), line1)), run_time=1.2)

            c.wait_until("meaning")
            self.play(FadeOut(box), ch.edges[0].animate.set_color(YELLOW), run_time=1.0)
            # the 4 counted out along the chain: one GOLD counter per edge (as in clip 1)
            tags = [counter(str(i + 1), ch.slot(i), size=36) for i in range(4)]
            c.wait_until("With them")
            self.play(FlashAround(star, run_time=1.0, time_width=1.5), run_time=1.0)
            self.play(*[time_span(FadeIn(tags[i], shift=0.15 * DOWN), 0.55 * i, 0.55 * i + 0.5)
                        for i in range(4)],
                      *[time_span(ch.edges[i].animate.set_color(YELLOW), 0.55 * i, 0.55 * i + 0.5)
                        for i in (1, 2, 3)],
                      run_time=2.15)

            hdr = Mono("count(path)", size=30, color=DIM)
            hdr.move_to([2.6, code.get_bottom()[1] - 0.4, 0])
            rule = Line(hdr.get_left() + 0.1 * LEFT, hdr.get_right() + 0.1 * RIGHT,
                        color=DIM, stroke_width=2).next_to(hdr, DOWN, buff=0.14)
            val = T("8", size=44, color=GOLD).next_to(rule, DOWN, buff=0.2)
            rows = T("1 row", size=28, color=DIM).next_to(val, DOWN, buff=0.15)
            c.wait_until("run")
            self.play(*appear(hdr, rule, shift=None), run_time=0.9)
            c.wait_until("eight")
            self.play(*appear(val), run_time=0.8)
            self.play(*appear(rows, shift=None), run_time=0.7)

        # hand over: only the plain chain stays, shrunk at the top
        self.play(*disappear(code, hdr, rule, val, rows, *tags, outline),
                  *[e.animate.set_color(FG) for e in ch.edges], run_time=1.0)
        self.remove(*ch.get_family())
        self.add(handover_shot())
        self.wait(1.0)
