"""Chapter 5, scene 1: hook. ch4's end card -> title card -> 503 chains -> millions -> shortest? -> Bacon.
Clips c5.hook.1 - c5.hook.3.

open_card(): ch4's end card and this scene's first frame (ch4 s7 ends on it). Static VGroup:
Lawrence (PINK, left) and Radcliffe (PINK, right), a faint tangle of PINK/BLUE dot chains, one
four-edge chain in YELLOW arched above it, a GOLD "?" over that chain and a GOLD "503" at the top.
"""
# style: 2
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
from lib.titles import title_card  # noqa: E402

# ---------------------------------------------------------------- layout
L_POS = np.array([-5.2, -0.7, 0])       # Jennifer Lawrence
R_POS = np.array([5.2, -0.7, 0])        # Daniel Radcliffe
R_V = 0.7                               # vertex circle radius
FAN_OP = 0.55                           # fan chains while they pour in
TANGLE_OP = 0.2                         # fan once dimmed (as on the open card)
TOP_Y = 3.15                            # "503"
ASK_Y = 2.15                            # "?"
LIFT_Y = 1.25                           # the YELLOW chain's middle dots


def actor(name, pos, size=34, r=R_V):
    """A vertex in ch1's look (PINK stroke, fill PINK at 0.2 over BG), the name under it."""
    circ = Circle(radius=r).set_stroke(PINK, 4).set_fill(
        interpolate_color(ManimColor(BG), ManimColor(PINK), 0.2), 1).move_to(pos)
    label = T(name, size=size, color=FG, line_spacing=0.8).next_to(circ, DOWN, buff=0.2)
    g = VGroup(circ, label)
    g.circle, g.label = circ, label
    return g


def chain(points, line_color=DIM, line_w=2.0, r=0.07):
    """Points from Lawrence to Radcliffe; the inner ones become dots, alternately BLUE (film)
    and PINK (actor). Edges stop at the vertex circles. VGroup(lines, dots)."""
    pts = [np.array(p, dtype=float) for p in points]
    a, b = pts[0], pts[-1]
    pts[0] = a + R_V * (pts[1] - a) / np.linalg.norm(pts[1] - a)
    pts[-1] = b + R_V * (pts[-2] - b) / np.linalg.norm(pts[-2] - b)
    lines = VGroup(*[Line(pts[i], pts[i + 1]).set_stroke(line_color, line_w) for i in range(len(pts) - 1)])
    dots = VGroup(*[Dot(p, radius=r, color=BLUE if i % 2 == 0 else PINK) for i, p in enumerate(pts[1:-1])])
    return VGroup(lines, dots)


def chain_points(rng, edges):
    n = edges - 1
    h = rng.uniform(-1.6, 1.6)
    xs = np.linspace(L_POS[0], R_POS[0], edges + 1)
    pts = [L_POS]
    for i in range(1, n + 1):
        t = i / edges
        y = L_POS[1] + h * np.sin(PI * t) + rng.uniform(-0.45, 0.45)
        pts.append([xs[i] + rng.uniform(-0.25, 0.25), np.clip(y, -2.45, 0.85), 0])
    pts.append(R_POS)
    return pts


def fan_layers():
    """Four layers of chains, denser each time (fixed seed: identical every call)."""
    rng = np.random.default_rng(503)
    spec = [(8, (4, 6)), (12, (6, 8)), (20, (6, 8)), (30, (8, 8))]
    layers = []
    for count, (lo, hi) in spec:
        layer = VGroup()
        for k in range(count):
            edges = lo if k % 2 == 0 else hi
            layer.add(chain(chain_points(rng, edges)))
        layers.append(layer.set_opacity(FAN_OP))
    # layer 0, chain 0 is the four-edge chain that lifts out in YELLOW
    return layers


def lifted_chain():
    xs = [-2.6, 0.0, 2.6]
    pts = [L_POS] + [[x, LIFT_Y, 0] for x in xs] + [R_POS]
    return chain(pts, line_color=YELLOW, line_w=5, r=0.11)


def open_card():
    """ch4's end card = ch5's first frame. Static, no updaters."""
    law = actor("Jennifer\nLawrence", L_POS)
    rad = actor("Daniel\nRadcliffe", R_POS)
    tangle = VGroup(*fan_layers()).set_opacity(TANGLE_OP)
    yellow = lifted_chain()
    q = T("?", size=72, color=GOLD).move_to([0, ASK_Y, 0])
    total = Mono("503", size=48, color=GOLD).move_to([0, TOP_Y, 0])
    return VGroup(tangle, law, rad, yellow, q, total)


class Hook(NarratedScene):
    def construct(self):
        card0 = open_card()
        self.add(card0)
        self.wait(1.0)   # hold ch4's end card before the voice starts

        # ------------------------------------------------------------ c5.hook.1
        with self.say("c5.hook.1") as c:
            card = title_card("Part 5 · Shortest paths, Bacon numbers, and the graph languages")
            if card.part.width > 12.4:
                card.part.scale_to_fit_width(12.4)
            sweep_clear(self, FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),  # early: title card
                        run_time=1.8)
            self.play(*appear(card.course), run_time=1.0)   # early: title card
            self.play(*appear(card.part), run_time=1.0)     # early: title card
            c.wait_until("last")

            law = actor("Jennifer\nLawrence", L_POS)
            rad = actor("Daniel\nRadcliffe", R_POS)
            sweep_clear(self, GrowFromCenter(law.circle), GrowFromCenter(rad.circle),
                        run_time=min(1.6, c.until("Jennifer")))
            c.wait_until(own_word=law.label)
            self.play(*appear(law.label), run_time=0.9)
            c.wait_until(own_word=rad.label)
            self.play(*appear(rad.label), run_time=0.9)

            # count strip between them
            cols = []
            for x, k, n in [(-2.4, "*2", "0"), (0.0, "*4", "8"), (2.4, "*6", "495")]:
                key = Mono(k, size=36, color=FG).move_to([x, 0.75, 0])
                num = Mono(n, size=44, color=GOLD).move_to([x, 0.0, 0])
                cols.append((key, num))
            c.wait_until("count")
            self.play(*appear(*cols[0], lag=0.3), run_time=1.0)
            c.wait_until("eight")
            self.play(*appear(*cols[1], lag=0.3), run_time=1.0)
            c.wait_until("four hundred")
            self.play(*appear(*cols[2], lag=0.3), run_time=1.0)
            c.wait_until("five hundred")
            bar = Line([-3.2, -0.55, 0], [3.2, -0.55, 0]).set_stroke(GOLD, 3)
            total = Mono("503", size=52, color=GOLD).move_to([0.55, -1.3, 0])
            total_key = Mono("*2..6", size=36, color=FG).next_to(total, LEFT, buff=0.45)
            total_key.align_to(total, DOWN)
            self.play(GrowFromCenter(bar), run_time=0.6)
            self.play(*appear(total_key, total, lag=0.3), run_time=1.2)

        # ------------------------------------------------------------ c5.hook.2
        layers = fan_layers()
        with self.say("c5.hook.2") as c:
            strip = [m for col in cols for m in col] + [bar, total_key]
            self.play(*disappear(*strip),
                      *during(total.animate.scale(48 / 52).move_to([0, TOP_Y, 0]), 0.3, 1),
                      run_time=min(1.4, c.until("one of them")))
            c.wait_until("one of them")
            self.play(FadeIn(layers[0]), run_time=1.0)

            c.wait_until("more")
            lbl = T("paths from Lawrence", size=30, color=DIM)
            key4 = Mono("*4", size=32, color=FG)
            num4 = T("12,160", size=40, color=GOLD)
            row = VGroup(lbl, key4, num4).arrange(RIGHT, buff=0.4)
            row.move_to([0, -3.3, 0]).shift(LEFT * 0.9)
            for m in (key4, num4):
                m.align_to(lbl, DOWN)
            self.play(FadeIn(layers[1]), *appear(lbl, key4, num4, shift=None, lag=0.2), run_time=1.0)

            def step(old_k, old_n, k, n, layer, cue):
                new_k = Mono(k, size=32, color=FG).move_to(old_k)
                new_n = T(n, size=40, color=GOLD)
                new_n.align_to(old_n, LEFT).align_to(old_n, DOWN)
                c.wait_until(cue)
                self.play(*swap(old_k, new_k), *swap(old_n, new_n), FadeIn(layer),
                          run_time=min(1.0, c.until("ask")))
                return new_k, new_n

            k6, n6 = step(key4, num4, "*6", "700,512", layers[2], "explodes")
            k8, n8 = step(k6, n6, "*8", "≈ 39.6 million", layers[3], "millions")

            c.wait_until("ask")
            self.play(*[ly.animate.set_opacity(TANGLE_OP) for ly in layers], run_time=1.0)
            yellow = lifted_chain()
            self.play(ReplacementTransform(layers[0][0].copy(), yellow), run_time=1.5)
            q = T("?", size=72, color=GOLD).move_to([0, ASK_Y, 0])
            self.play(*appear(q), run_time=0.8)

        # ------------------------------------------------------------ c5.hook.3
        with self.say("c5.hook.3") as c:
            bacon = actor("Kevin Bacon", [3.2, 0.9, 0], size=40, r=0.85)
            bacon.label.next_to(bacon.circle, DOWN, buff=0.25)
            hook = T("every actor's distance?", size=44, color=YELLOW)
            hook.next_to(bacon.label, DOWN, buff=0.55)
            old = list(self.mobjects)
            self.play(*during([FadeOut(m, shift=3 * LEFT) for m in old], 0, 0.5),
                      *during(GrowFromCenter(bacon.circle), 0.5, 1),
                      run_time=min(2.2, c.until("every")))
            c.wait_until("every")
            self.play(*appear(hook), run_time=1.0)
            c.wait_until(own_word=bacon.label)
            self.play(*appear(bacon.label), run_time=0.9)

        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)
