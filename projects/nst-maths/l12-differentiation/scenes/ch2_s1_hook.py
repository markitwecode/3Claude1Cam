"""Chapter 2, scene 1: hook: part 2's card, the definition and the x³ effort, ln x sin x, table + three rules, why? Clips c2.hook.1 – c2.hook.3.

Exports:
- open_card() -> part 2's opening card, title_card("Part 2 · The rules, from first principles"), static, at
  ORIGIN; parts `.title .rule .course .part` (ch1 s7 ends on it; this scene's first frame).
- handover_shot() -> load_scene("ch2_s2_table").open_shot() (s2 opens on it; the thumbnail grows into it).
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
from lib.titles import title_card  # noqa: E402

PART = "Part 2 · The rules, from first principles"

RX = 2.6                      # centre x of the right-hand region after the slide-left
THUMB_C = np.array([RX, 0.35, 0])
THUMB_H = 2.7
TILE_Y = -2.95
WHY_Y = -1.75


def open_card():
    """The chapter's title card exactly as it stands once settled (static VGroup at ORIGIN)."""
    card = title_card(PART)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


def handover_shot():
    return load_scene("ch2_s2_table").open_shot()


def fit(m, w, h, c):
    m.scale(min(w / m.width, h / m.height))
    m.move_to(c)
    return m


def shrunk(m, w, h, c, op=DIMMED):
    """Transform m into a fitted, dimmed copy."""
    t = restyle(m, op).target_mobject
    fit(t, w, h, c)
    return Transform(m, t)


def product_expr(size=56):
    m = MathTex(r"\frac{d}{dx}", r"\Big(", r"\ln x", r"\,", r"\sin x", r"\Big)", font_size=size, color=FG)
    m[2].set_color(BLUE)
    m[4].set_color(PURPLE)
    return m


def tile(text):
    frame = RoundedRectangle(corner_radius=0.12, width=2.75, height=0.9).set_stroke(DIM, 2).set_fill(opacity=0)
    lab = T(text, 30)
    g = VGroup(frame, lab)
    g.frame, g.lab = frame, lab
    return g


def thumb_card():
    t = load_scene("ch2_s2_table").table_card()
    t.scale(THUMB_H / t.height).move_to(THUMB_C)
    return t


class Hook(NarratedScene):
    def construct(self):
        self.s2 = load_scene("ch1_s2_chord")
        self.s3 = load_scene("ch1_s3_cube")
        self.card = open_card()
        self.add(self.card)                      # first frame: the card, fully drawn (ch1 s7 ends on it)
        self.clip1()
        self.clip2()
        self.clip3()

    # ---------------------------------------------------------------- c2.hook.1
    def clip1(self):
        s2, s3 = self.s2, self.s3
        fig = s2.figure29(dx=0.5, tangent=False, chord=True, braces=False, q_labels=False)
        for k in ("chord_lab", "p_lab"):
            fig.remove(getattr(fig, k))
        fit(fig, 5.4, 5.6, [-4.0, -0.3, 0])
        ax = fig.axes
        K = ax.get_x_axis().get_length() / 7.0
        P = ax.c2p(1.0, 1.0)

        def chord_at(d):
            return s2.chord_line(ax, d, 1.0).scale(K, about_point=P)

        tangent = s2.tangent_line(ax, 1.0).scale(K, about_point=P)
        box = s2.definition_box()
        fit(box, 7.4, 2.2, [2.9, 2.55, 0])
        column = s3.derivation()[1]
        fit(column, 7.4, 4.0, [2.9, -1.35, 0])
        self.fig, self.box, self.column = fig, box, column

        with self.say("c2.hook.1") as c:
            c.wait_until("last")
            self.play(*during(disappear(self.card), 0, 0.45), *during(appear(fig, shift=None), 0.5, 1),
                      run_time=min(1.6, c.until("defined the derivative")))
            c.wait_until("defined the derivative")
            self.play(*appear(box), run_time=min(1.0, 0.9 * c.until("chord slopes")))
            c.wait_until("chord slopes")

            def sweep(m, a):
                m.become(chord_at(0.5 * (0.03 / 0.5) ** a))

            def qmove(m, a):
                d = 0.5 * (0.03 / 0.5) ** a
                m.move_to(ax.c2p(1.0 + d, (1.0 + d) ** 3))

            self.play(UpdateFromAlphaFunc(fig.chord, sweep), UpdateFromAlphaFunc(fig.q_dot, qmove),
                      run_time=min(2.6, 0.6 * c.until("cube")))
            self.play(FadeIn(tangent), FadeOut(fig.chord), FadeOut(fig.q_dot),
                      run_time=min(1.0, 0.8 * c.until("cube")))
            settle(self, fig, add=[tangent], drop=[fig.chord, fig.q_dot])
            fig.tangent = tangent
            c.wait_until("cube")
            self.play(*appear(*column, shift=None, lag=0.6), run_time=max(1.5, 0.9 * c.until()))

    # ---------------------------------------------------------------- c2.hook.2
    def clip2(self):
        fig, box, column = self.fig, self.box, self.column
        prod = product_expr().move_to([RX - 0.35, 2.75, 0])
        q = T("?", 64, YELLOW).next_to(prod, RIGHT, buff=0.3)
        thumb = thumb_card()
        tiles = VGroup(tile("chain rule"), tile("product rule"), tile("quotient rule"))
        tiles.arrange(RIGHT, buff=0.2).move_to([2.05, TILE_Y, 0])
        self.prod, self.q, self.thumb, self.tiles = prod, q, thumb, tiles

        with self.say("c2.hook.2") as c:
            self.play(*during(shrunk(fig, 3.6, 2.8, [-4.7, 2.05, 0]), 0, 0.6),
                      *during(shrunk(column, 3.8, 1.9, [-4.75, -2.75, 0]), 0.25, 0.8),
                      *during(shrunk(box, 5.0, 1.8, [-4.2, -0.35, 0]), 0.45, 1),
                      run_time=min(2.2, 0.8 * c.until("log")))
            c.wait_until("log")
            self.play(*appear(prod), run_time=min(1.2, 0.9 * c.until("nobody")))
            c.wait_until("nobody")
            self.play(*appear(q), run_time=0.8)
            c.wait_until("table")
            self.play(*appear(thumb), run_time=min(1.2, 0.9 * c.until("rules")))
            c.wait_until("rules")
            self.play(*appear(*[t.frame for t in tiles], shift=None, lag=0.2),
                      run_time=min(0.8, 0.9 * c.until(own_word=tiles[0].lab)))
            for t in tiles:
                c.wait_until(own_word=t.lab)
                self.play(*appear(t.lab), t.frame.animate.set_stroke(BLUE, 3), run_time=0.7)

    # ---------------------------------------------------------------- c2.hook.3
    def clip3(self):
        box, tiles, thumb = self.box, self.tiles, self.thumb
        why = T("why?", 48, YELLOW, slant=ITALIC).move_to([RX, WHY_Y, 0])
        ends = [box.rect.get_corner(DR) + 0.3 * UP + k * 0.35 * UP for k in range(3)]
        arrows = [Arrow(t.frame.get_top() + 0.4 * LEFT, e, buff=0.08, stroke_width=2.5,
                        tip_length=0.18, color=YELLOW) for t, e in zip(tiles, ends)]

        # the thumbnail's target: s2's open shot, the rest of the card faded out
        s2t = load_scene("ch2_s2_table")
        target = s2t.table_card()
        keep = s2t._place_open(target)
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        for m in target.family_members_with_points():
            if id(m) not in keep_ids:
                m.set_opacity(0)

        with self.say("c2.hook.3", gap=1.0) as c:
            self.play(*appear(why), run_time=min(1.0, 0.9 * c.until("same")))
            c.wait_until("same")
            self.play(*during(disappear(why), 0, 0.3),
                      *during([GrowArrow(a) for a in arrows], 0.25, 0.85),
                      *during(set_alpha([box], 1), 0.5, 1),
                      run_time=min(2.4, 0.8 * c.until("first")))
            self.play(FlashAround(box.rect, time_width=1.5), run_time=min(1.5, 0.8 * c.until("first")))
            self.arrows = arrows
            c.wait_until("first")
            others = [m for m in self.mobjects if m is not thumb]
            self.play(*during([FadeOut(m) for m in others], 0, 0.45),
                      *during(Transform(thumb, target), 0.2, 1),
                      run_time=max(1.2, min(1.8, c.until())))
            self.remove(*thumb.get_family())
            self.add(handover_shot())
        self.wait(0.15)
