"""Chapter 6, scene 7: recap of stationary points, then part seven's preview. Clips c6.recap.1 – c6.recap.2.

Plan: a 3 + 2 grid of small callbacks (s2 labelled figure + flat tangents, s3 umbrellas, s4 chain
cards beside tiny x^3 / x^4 graphs, s5 power panels, s6 three graphs), each with its line under it,
built on its mark. Then the grid sweeps into part seven's question cards (H1 H2 H4 I1) and, beside
them, the notes' "4.11 Curve sketching" with H3 and H5. After the last word the board sweeps into
end_card(), held ~8 s, then fades (the chapter's last scene; no handover).
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

PART7 = "Part 7 · Solutions: Examples Sheet H1, H2, H4 and I1"

TOP_XS = (-4.65, -0.65, 4.1)
TOP_WS = (3.9, 3.7, 5.0)
TOP_Y, TOP_H = 2.4, 2.35
TOP_CAP = 1.05                       # top of the top row's captions
BOT_XS = (-3.45, 3.45)
BOT_Y, BOT_W, BOT_H = -1.4, 6.3, 2.0
BOT_CAP = -2.72
CAP_FS = 36


def end_card():
    """ch7's opening card when ch7_s1_intro defines open_card(), else the stand-in title card."""
    if (Path(__file__).resolve().parent / "ch7_s1_intro.py").exists():
        mod = load_scene("ch7_s1_intro")
        if hasattr(mod, "open_card"):
            return mod.open_card()
    card = title_card(PART7)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


def fit(m, w, h, pos):
    m.scale(min(w / m.width, h / m.height)).move_to(pos)
    return m


def caption(lines, x, top):
    """VGroup of MathTex lines (δx TEAL), centred on x, the first line's top at `top`."""
    g = VGroup(*[MathTex(s, font_size=CAP_FS, color=FG, substrings_to_isolate=[r"\delta x"])
                 for s in lines])
    for m in g:
        m.set_color_by_tex(r"\delta x", TEAL)
    g.arrange(DOWN, buff=0.16)
    g.move_to([x, top - g.height / 2, 0])
    return g


def q_card(label):
    """Sheet question card, label only: rounded rectangle, DIM border, YELLOW label top left."""
    frame = RoundedRectangle(corner_radius=0.15, width=2.5, height=1.55)
    frame.set_stroke(DIM, 2).set_fill(BG, 1)
    lab = T(label, 40, YELLOW)
    lab.move_to(frame.get_corner(UL) + np.array([0.22 + lab.width / 2, -0.2 - lab.height / 2, 0]))
    card = VGroup(frame, lab)
    card.frame, card.label = frame, lab
    return card


def thumb_r1():
    s2 = load_scene("ch6_s2_vocab")
    fig = s2.labelled_figure().fig
    fig.dots.remove(fig.bend1, fig.bend2)
    fig.remove(fig.dots)
    fig.add(fig.dots)
    tans = VGroup(*[s2._flat_tangent(d, half=1.05) for d in (fig.peak, fig.valley, fig.flat)])
    g = VGroup(fig, tans)
    fit(g, TOP_WS[0], TOP_H, [TOP_XS[0], TOP_Y, 0])
    g.fig, g.tans = fig, tans
    return g


def thumb_r2():
    u = load_scene("ch6_s3_second").umbrellas()
    u.remove(u.bowl_tex, u.bowl_lab, u.cap_tex, u.cap_lab)
    VGroup(u.cap, u.cap_rain).shift(1.3 * LEFT)
    return fit(u, TOP_WS[1], TOP_H, [TOP_XS[1], TOP_Y, 0])


def thumb_r3():
    s4 = load_scene("ch6_s4_higher")
    cards, fig = s4.chain_cards(), s4.figure30()
    cards.cube.move_to(ORIGIN)
    cards.quart.next_to(cards.cube, DOWN, buff=0.2).align_to(cards.cube, LEFT)
    rows = []
    for card, panel in ((cards.cube, fig.cube), (cards.quart, fig.quart)):
        panel.remove(panel.lab, panel.xlab, panel.ylab)
        panel.scale_to_fit_height(card.height * 0.95)
        panel.next_to(card, LEFT, buff=0.25)
        rows.append(VGroup(panel, card))
    g = VGroup(*rows)
    fit(g, TOP_WS[2], TOP_H, [TOP_XS[2], TOP_Y, 0])
    g.cards, g.fig = cards, fig
    return g


def thumb_r4():
    pp = load_scene("ch6_s5_why").power_panels()
    fit(pp, BOT_W, BOT_H, [BOT_XS[0], BOT_Y, 0])
    for p in pp.panels:                      # keep the titles and signs readable at thumbnail size
        p.title.scale(1.4)
        for sgn in p.signs:
            sgn.scale(1.35)
    return pp


def thumb_r5():
    tg = load_scene("ch6_s6_nonstat").three_graphs()
    for p in tg.panels:
        p.remove(p.info, p.down, p.up)
        p.word.next_to(p.axes, DOWN, buff=0.25)
    g = tg.panels
    fit(g, BOT_W, BOT_H, [BOT_XS[1], BOT_Y, 0])
    for p in tg.panels:                      # readable words and names at thumbnail size
        p.word.scale(28 / 17).next_to(p.axes, DOWN, buff=0.15)
        p.name.scale(1.4).next_to(p.axes, UP, buff=0.08)
    return g


class Recap(NarratedScene):
    def construct(self):
        # ---------------------------------------------------------- clip 1: the grid
        with self.say("c6.recap.1", gap=1.0) as c:
            c.wait_until("r1")
            r1 = thumb_r1()
            c1 = caption([r"\text{stationary: } y' = 0"], TOP_XS[0], TOP_CAP)
            self.play(FadeIn(r1.fig), *appear(c1), run_time=min(1.2, c.until("first derivative")))
            c.wait_until("first derivative")
            self.play(*[GrowFromCenter(t) for t in r1.tans], run_time=min(1.2, c.until("r2")))

            c.wait_until("r2")
            r2 = thumb_r2()
            c2 = caption([r"y'' > 0\text{: minimum}", r"y'' < 0\text{: maximum}"], TOP_XS[1], TOP_CAP)
            self.play(FadeIn(r2), run_time=min(1.2, c.until("positive")))
            c.wait_until("positive")
            self.play(*appear(c2[0]), run_time=min(1.0, c.until("negative")))
            c.wait_until("negative")
            self.play(*appear(c2[1]), run_time=min(1.0, c.until("r3")))

            c.wait_until("r3")
            r3 = thumb_r3()
            c3 = caption([r"\text{first non-zero derivative:}", r"\text{odd} \to \text{inflection}",
                          r"\text{even} \to \text{max or min}"], TOP_XS[2], TOP_CAP)
            self.play(FadeIn(r3), *appear(c3[0]), run_time=min(1.2, c.until("different from zero")))
            c.wait_until("different from zero")
            self.play(*flash([r3.cards.cube.ring, r3.cards.quart.ring], time_width=1.5),
                      run_time=min(1.5, c.until("odd order")))
            c.wait_until("odd order")
            self.play(*appear(c3[1]), run_time=min(1.0, c.until("even order")))
            c.wait_until("even order")
            self.play(*appear(c3[2]), run_time=min(1.0, c.until("r4")))

            c.wait_until("r4")
            r4 = thumb_r4()
            c4 = caption([r"\text{why: Taylor,}",
                          r"\text{the change} \approx (\delta x)^n\, y^{(n)}/n!"], BOT_XS[0], BOT_CAP)
            self.play(FadeIn(r4), *appear(c4[0]), run_time=min(1.2, c.until("the change")))
            c.wait_until("the change")
            self.play(*appear(c4[1]), run_time=min(1.0, c.until("delta ex")))
            c.wait_until("delta ex")
            self.play(*flash([p.signs for p in r4.panels], time_width=1.5),
                      run_time=min(1.5, c.until("r5")))

            c.wait_until("r5")
            r5 = thumb_r5()
            c5 = caption([r"\text{inflection: } y'' \text{ changes sign}"], BOT_XS[1], BOT_CAP)
            self.play(FadeIn(r5), *appear(c5), run_time=min(1.2, c.until("flat or not")))
            c.wait_until("flat or not")
            self.play(*[VShowPassingFlash(p.tan.copy().set_stroke(YELLOW, 8), time_width=0.6)
                        for p in r5], run_time=min(1.2, c.until("changes sign")))

        # ---------------------------------------------------------- clip 2: next time
        head7 = T("Part 7 · Solutions", 44).move_to([-3.4, 1.6, 0])
        cards7 = [q_card(s) for s in ("H1", "H2", "H4", "I1")]
        for i, k in enumerate(cards7):
            k.move_to([-4.85 + 2.9 * (i % 2), -0.05 - 1.9 * (i // 2), 0])
        head8 = T("4.11 Curve sketching", 44).move_to([3.7, 1.6, 0])
        cards8 = [q_card(s) for s in ("H3", "H5")]
        for i, k in enumerate(cards8):
            k.move_to([2.25 + 2.9 * i, -1.0, 0])

        with self.say("c6.recap.2") as c:
            sweep_clear(self, *appear(head7), run_time=min(1.6, c.until("worked solutions")))
            for k, cue in zip(cards7, ("H one", "H two", "H four", "eye one")):
                c.wait_until(cue)
                self.play(*appear(k), run_time=0.6)
            c.wait_until("Try them first")
            self.play(*flash([k.frame for k in cards7], time_width=1.5), run_time=min(1.5, c.until("lecture")))

            c.wait_until("lecture")
            self.play(*set_alpha(cards7 + [head7], 0.4), run_time=min(1.0, c.until("curve sketching")))
            c.wait_until(own_word=head8)
            self.play(*appear(head8), run_time=min(1.0, c.until("H three")))
            for k, cue in zip(cards8, ("H three", "H five")):
                c.wait_until(cue)
                self.play(*appear(k), run_time=min(0.8, c.until()))

        self.wait(0.6)                       # let H3 / H5 sit a moment before the sweep
        card = end_card()
        sweep_clear(self, time_span(FadeIn(card), 0.6, 1.4), run_time=1.4)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
