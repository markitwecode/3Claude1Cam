"""Chapter 1, scene 1: L10's end card, the title card, L10's teaser merge replayed, the 15-state
machine with look-alike states along the bottom, and the lecture's road. Clips c1.hook.1 – c1.hook.3.

Opens on L10 ch6_s8_recap's end_card() (loaded by path, with lib.paths.project pointed at L10 while
it loads, since that file loads its own L10 siblings). {last}/{teaser} replay that file's own
five_diagram() -> four_diagram() merge and ff_boxes 3 -> 2 (the merged circle GOLD here: GOLD = "the
same" in this lecture). {machine}: s4's tree_diagram(labelled=False). {road}: four chips on the right.
"""
# style: 2
import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

import lib.paths as _paths  # noqa: E402
from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

_LECTURES = Path(__file__).resolve().parents[2]


def _load_other(folder, stem):
    """A scene file of another lecture; its own load_scene() calls resolve inside that lecture."""
    proj = _LECTURES / folder
    orig = _paths.project
    _paths.project = lambda: proj
    try:
        spec = importlib.util.spec_from_file_location(f"_{folder[:3]}_{stem}", proj / "scenes" / f"{stem}.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        _paths.project = orig
    return mod


L10R = _load_other("l10-state-assignment", "ch6_s8_recap")
L8H = _load_other("l08-timing-metastability", "ch1_s1_hook")
TREE = load_scene("ch1_s4_tree")


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- the road ---------------------------------------------------------------------------------
ROW_YS = (2.45, 0.82, -0.82, -2.45)
ICON_X = -0.45
LABEL_X = 0.45


def icon_merge():
    a = Circle(radius=0.15).set_stroke(GOLD, 3).move_to(_p(-0.45, 0.2))
    b = Circle(radius=0.15).set_stroke(GOLD, 3).move_to(_p(-0.45, -0.2))
    arr = Arrow(_p(-0.22, 0), _p(0.18, 0), buff=0, stroke_width=3, color=DIM, tip_length=0.14,
                max_tip_length_to_length_ratio=0.4)
    m = Circle(radius=0.19).set_stroke(GOLD, 3).move_to(_p(0.45, 0))
    return VGroup(a, b, arr, m)


def icon_stairs(s=0.26):
    cells = VGroup()
    for r in range(3):
        for k in range(r + 1):
            cells.add(Square(side_length=s).set_stroke(FG, 2).move_to(_p(k * s, -r * s)))
    return cells.move_to(ORIGIN)


def icon_chip():
    ch = L8H.chip("x")
    ch.remove(ch.lab)
    return ch.scale(0.34)


def icon_lamp():
    L, Rx, top, bot = -0.5, 0.5, 0.36, -0.36
    wires = VGroup(
        Line(_p(L, 0.07), _p(L, top)), Line(_p(L, top), _p(Rx, top)), Line(_p(Rx, top), _p(Rx, 0.17)),
        Line(_p(Rx, -0.17), _p(Rx, bot)), Line(_p(Rx, bot), _p(L, bot)), Line(_p(L, bot), _p(L, -0.07)),
    ).set_stroke(FG, 3)
    plus = Line(_p(L - 0.17, 0.07), _p(L + 0.17, 0.07)).set_stroke(FG, 3)
    minus = Line(_p(L - 0.09, -0.07), _p(L + 0.09, -0.07)).set_stroke(FG, 5)
    bulb = Circle(radius=0.17).set_stroke(FG, 3).move_to(_p(Rx, 0))
    d = 0.17 / np.sqrt(2)
    xx = VGroup(Line(_p(Rx - d, -d), _p(Rx + d, d)), Line(_p(Rx - d, d), _p(Rx + d, -d))).set_stroke(FG, 2)
    glow = Circle(radius=0.3).set_stroke(width=0).set_fill(YELLOW, 0.35).move_to(_p(Rx, 0))
    glow.set_z_index(-1)
    g = VGroup(wires, plus, minus, bulb, xx)
    g.bulb, g.xx, g.glow = bulb, xx, glow
    return g


ROAD_TEXT = ("Part 1: matching rows", "Parts 2–3: a stronger test",
             "Parts 4–5: state machines\non programmable chips", "Part 6: electricity")


def road():
    icons = [icon_merge(), icon_stairs(), icon_chip(), icon_lamp()]
    labels = []
    for k, (ic, txt, y) in enumerate(zip(icons, ROAD_TEXT, ROW_YS)):
        ic.move_to(_p(ICON_X, y))
        lab = T(txt, 32, YELLOW if k == 0 else FG, line_spacing=0.8)
        lab.move_to(_p(0, y)).align_to(_p(LABEL_X, 0), LEFT)
        labels.append(lab)
    icons[3].glow.move_to(icons[3].bulb)
    arrows = [Arrow(_p(ICON_X, a - 0.5), _p(ICON_X, b + 0.5), buff=0, stroke_width=3, color=DIM,
                    tip_length=0.16, max_tip_length_to_length_ratio=0.35)
              for a, b in zip(ROW_YS, ROW_YS[1:])]
    return icons, labels, arrows


class Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- c1.hook.1: L10's end card, the title, the teaser --------------------------------------------
    def clip1(self):
        endc = L10R.end_card()
        self.add(endc)
        self.wait(0.7)
        with self.say("c1.hook.1") as c:
            card = title_card("Part 1 · Fewer states, same machine")
            if card.title.width > 12.0:
                card.title.scale_to_fit_width(12.0)
            self.play(*during([FadeOut(endc)], 0, 0.4),
                      *during([FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule)], 0.45, 1.0),  # early: title card
                      run_time=1.6)
            self.play(*appear(card.course, card.part, lag=0.35), run_time=1.2)  # early: title card read whole

            # L10's teaser, its own objects, centred
            d5 = L10R.five_diagram()
            ff3 = L10R.ff_boxes(L10R.FF_XS3)
            d4 = L10R.four_diagram()
            # the diagram above, the flip-flops below it, both scaled up (flip-flop letters >= 30)
            K = 1.35
            dc = d5.get_center()
            for m in (d5, d4):
                m.shift(-dc).scale(K, about_point=ORIGIN).shift(_p(0, 0.95))
            fc = ff3.get_center()
            ff3.shift(-fc).scale(K, about_point=ORIGIN).shift(_p(0, -2.45))
            d4.nodes["M"].set_stroke(GOLD)
            d4.arcs["MB"].set_color(GOLD)
            c.wait_until("and the lecture")
            sweep_clear(self, FadeIn(d5), FadeIn(ff3), run_time=min(1.6, c.until("teaser", floor=1.0)))  # early: the teaser picture

            c.wait_until("teaser")
            pair = [d5.nodes["D"], d5.nodes["E"]]
            twins = [d5.arcs["DB"], d5.arcs["EB"]]
            self.play(*[n.animate.set_stroke(GOLD, 6) for n in pair], *recolor(twins, GOLD),
                      *flash(pair, color=GOLD, time_width=1.5), run_time=min(1.2, c.until("than they")))
            c.wait_until("than they")
            moves = [ff3[k].animate.shift(K * (L10R.FF_XS2[k] - L10R.FF_XS3[k]) * RIGHT) for k in (0, 1)]
            self.play(ReplacementTransform(d5.nodes["D"], d4.nodes["M"]),
                      ReplacementTransform(d5.nodes["E"], d4.nodes["M"].copy()),
                      ReplacementTransform(d5.arcs["AD"], d4.arcs["AM"]),
                      ReplacementTransform(d5.arcs["CE"], d4.arcs["CM"]),
                      ReplacementTransform(d5.arcs["DB"], d4.arcs["MB"]),
                      ReplacementTransform(d5.arcs["EB"], d4.arcs["MB"].copy()),
                      *during(disappear(ff3[2]), 0, 0.45), *during(moves, 0.3, 1.0),
                      run_time=min(1.5, c.until(floor=0.9)))
            self.remove(*self.mobjects)
            ff2 = VGroup(ff3[0], ff3[1])
            self.add(d4, ff2)
            self.teaser = VGroup(d4, ff2)

    # -- c1.hook.2: the 15-state machine --------------------------------------------------------------
    def clip2(self):
        tree = self.tree = TREE.tree_diagram(labelled=False)
        tree.shift(-tree.get_center()[0] * RIGHT)
        S = tree.states
        with self.say("c1.hook.2") as c:
            self.play(*during([FadeOut(self.teaser, scale=0.3)], 0, 0.45),
                      *during([FadeIn(tree)], 0.45, 1.0), run_time=min(1.8, c.until("pairs")))
            c.wait_until("pairs")
            hi = [S["H"].circle, S["I"].circle]
            self.play(*[m.animate.set_stroke(GOLD, 5) for m in hi], *flash(hi, color=GOLD, time_width=1.5),
                      run_time=min(1.4, c.until("exactly")))
            c.wait_until("exactly")
            jl = [S["J"].circle, S["L"].circle]
            self.play(*[m.animate.set_stroke(GOLD, 5) for m in jl], *flash(jl, color=GOLD, time_width=1.5),
                      run_time=min(1.4, c.until("question")))

            c.wait_until("question")
            q = T("?", 48, YELLOW).move_to((S["H"].get_center() + S["I"].get_center()) / 2)
            self.q = q
            self.play(*appear(q), run_time=min(1.0, c.until("impossible")))
            cap = self.cap = T("impossible to tell apart?", 36).move_to(_p(0, -3.45))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=min(1.0, c.until("keep")))

            c.wait_until("keep")
            I = S["I"]
            self.play(I.animate(rate_func=there_and_back).shift(0.14 * LEFT).set_opacity(0.3),
                      run_time=min(1.6, c.until(floor=0.8)))

    # -- c1.hook.3: the lecture's road --------------------------------------------------------------
    def clip3(self):
        tree = self.tree
        icons, labels, arrows = road()
        with self.say("c1.hook.3") as c:
            c.wait_until("comes")
            letters = [st.letter for st in tree.states.values()]
            self.play(*disappear(self.q, self.cap, *letters), run_time=0.8)
            for st in tree.states.values():
                st.remove(st.letter)
            tree.generate_target()
            tree.target.scale(0.44)
            tree.target.move_to(_p(-6.55 + tree.target.width / 2, 0))
            self.play(MoveToTarget(tree), run_time=min(1.3, c.until("remove")))
            cues = ("remove", "stronger", "chips", "circuits")
            for k, cue in enumerate(cues):
                c.wait_until(cue)
                c.wait_until(own_word=labels[k])
                nxt = c.until(cues[k + 1]) if k < 3 else c.until(floor=0.8)
                extra = [GrowArrow(arrows[k - 1])] if k else []
                self.play(*extra, FadeIn(icons[k]), *appear(labels[k]), run_time=min(1.2, nxt))
                if k == 0:
                    c.wait_until("matching rows")
                    self.play(FlashUnder(labels[0], color=YELLOW, time_width=1.5),
                              run_time=min(1.2, c.until("stronger")))
            lamp = icons[3]
            self.play(FadeIn(lamp.glow), *recolor([lamp.bulb, *lamp.xx], YELLOW),
                      run_time=min(0.9, c.until(floor=0.5)))
