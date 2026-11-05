"""Chapter 1, scene 7: recap, next time, end card. Clips c1.recap.1 – c1.recap.3.

A small "Recap" heading, then four panels, one per sentence, each shown big at the centre with its
line under it, then shrunk into a strip of four along the top as the next one arrives: s2's Figure 29 (chords converging onto the tangent), s3's derivation (step words light in
turn, the boxed 3x^2 flashes), s6's thumbs (RED corner dot, RED dashed jump flash), s6's diff box
((a), the left/right limits, "finite" light in turn). On {next} the last caption goes, the panels dim in
the strip (the diff box shrinks into it), s2's (103) box grows out of the first panel to the centre and three
rule labels come out of it (each label's YELLOW frame grows out of the box's bottom edge). On {same} three YELLOW
arrows rise from the labels to the box and its two lims flash; after the clip's last word the board
clears into end_card(), held ~8 s, then fades.

end_card(): ch2's opening card, load_scene("ch2_s1_hook").open_card(), when that exists; else the
stand-in title_card("Part 2 · The rules, from first principles"). Entered with one call:
    sweep_clear(self, time_span(FadeIn(card), 0.6, 1.4), run_time=1.4)
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

PART2 = "Part 2 · The rules, from first principles"

HERO = np.array((0.0, -0.3, 0.0))
HERO_W, HERO_H = 12.4, 4.3
CAP_Y = -3.05
STRIP = [np.array((x, 2.9, 0)) for x in (-5.1, -1.7, 1.7, 5.1)]
STRIP_W, STRIP_H = 2.9, 1.05


def end_card():
    """ch2's opening card when ch2_s1_hook defines open_card(), else the stand-in title card."""
    if (Path(__file__).resolve().parent / "ch2_s1_hook.py").exists():
        mod = load_scene("ch2_s1_hook")
        if hasattr(mod, "open_card"):
            return mod.open_card()
    card = title_card(PART2)
    if card.title.width > 12.6:
        card.title.scale_to_fit_width(12.6)
    return card


def fit(m, w, h, pos):
    m.scale(min(w / m.width, h / m.height)).move_to(pos)
    return m


def caption(text, t2c=None):
    return T(text, 32, t2c=t2c or {}).move_to([0, CAP_Y, 0])


def shrink(m, i, op=0.5):
    """Transform m into its strip slot (scaled to fit, opacity op)."""
    t = restyle(m, op).target_mobject
    fit(t, STRIP_W, STRIP_H, STRIP[i])
    return Transform(m, t)


class Recap(NarratedScene):
    def construct(self):
        s2 = load_scene("ch1_s2_chord")
        s3 = load_scene("ch1_s3_cube")
        s6 = load_scene("ch1_s6_differentiable")

        head = T("Recap", 44).move_to([0, 3.0, 0])

        # panel 1: Figure 29, chords converging onto the tangent
        fig = s2.figure29(dx=0.5, tangent=False, chord=True, braces=False, q_labels=False)
        for k in ("xlab", "ylab", "p_lab", "chord_lab"):
            fig.remove(getattr(fig, k))
        fit(fig, HERO_W, HERO_H, HERO)
        ax = fig.axes
        K = ax.get_x_axis().get_length() / 7.0     # figure29's x-axis is 7 units at full size
        P = ax.c2p(1.0, 1.0)

        def chord_at(d):
            return s2.chord_line(ax, d, 1.0).scale(K, about_point=P)

        tangent = s2.tangent_line(ax, 1.0).scale(K, about_point=P)
        ghosts = VGroup(*[chord_at(d).set_stroke(opacity=0.3) for d in (0.35, 0.2, 0.1)])
        cap1 = caption("derivative = limit of chord slopes", {"chord slopes": TEAL})

        # panel 2: s3's derivation
        der = s3.derivation()
        labels, column = der[0], der[1]
        fit(der, HERO_W, HERO_H + 0.3, HERO + 0.1 * UP)
        labels.scale(T("substitute", 30).height / labels[0].height)   # step words back to size 30
        labels.next_to(column, UP, buff=0.3)
        VGroup(labels, column).move_to(HERO + 0.1 * UP)
        words = [labels[i] for i in range(0, len(labels), 2)]
        res_box = column[4][1]
        cap2 = caption("first principles: substitute, expand, subtract, divide, limit")

        # panel 3: s6's thumbs
        th = fit(s6.thumbs(), HERO_W, HERO_H, HERO)
        v, step = th[0], th[1]
        cap3 = caption("a corner or a jump: no derivative", {"no derivative": RED})

        # panel 4: s6's diff box
        box = fit(s6.diff_box(), HERO_W, HERO_H, HERO)
        finite = select(box.b, "finite")[0]
        cap4 = caption("differentiable: continuous, both sides agree, finite")

        # ---------------- c1: heading, Figure 29, the derivation
        with self.say("c1.recap.1") as c:
            self.play(*appear(head), run_time=1.0)
            c.wait_until("r1")
            self.play(*appear(fig, cap1, lag=0.4), run_time=min(1.2, c.until("chord slopes")))

            def sweep(m, a):
                m.become(chord_at(0.5 - 0.48 * a))

            def qmove(m, a):
                d = 0.5 - 0.48 * a
                m.move_to(ax.c2p(1.0 + d, (1.0 + d) ** 3))

            self.play(UpdateFromAlphaFunc(fig.chord, sweep), UpdateFromAlphaFunc(fig.q_dot, qmove),
                      FadeIn(ghosts), run_time=min(2.2, c.until("r2") - 0.9), rate_func=linear)
            self.play(FadeIn(tangent), FadeOut(fig.chord), FadeOut(fig.q_dot),
                      run_time=min(0.8, c.until("r2")))
            fig.remove(fig.chord, fig.q_dot, fig.p_dot)
            fig.add(ghosts, tangent, fig.p_dot)
            self.remove(ghosts, tangent)
            self.add(fig)
            c.wait_until("r2")
            self.play(*during(disappear(head, cap1), 0, 0.4), *during([shrink(fig, 0)], 0.1, 0.65),  # early: the derivation shown whole, then walked
                      *during(appear(der, cap2, lag=0.2), 0.5, 1.0),
                      run_time=min(2.0, c.until("substitute")))
            for i, w in enumerate(words):
                cue = ["substitute", "expand", "subtract", "divide", "limit"][i]
                c.wait_until(cue)
                self.play(*recolor([w], YELLOW), run_time=min(0.5, c.until("three ex squared")))
            c.wait_until("three ex squared")
            self.play(FlashAround(res_box, color=GREEN, time_width=1.5), run_time=min(1.5, c.until()))

        # ---------------- c2: corner and jump, the diff box
        with self.say("c1.recap.2") as c:
            self.play(*during(disappear(cap2), 0, 0.4), *during([shrink(der, 1)], 0.1, 0.65),
                      *during(appear(th, cap3, lag=0.2), 0.5, 1.0),
                      run_time=min(1.6, c.until("jump")))
            self.play(FlashAround(v.corner, color=RED, time_width=1.5, buff=0.12), run_time=1.0)
            c.wait_until("jump")
            self.play(FlashAround(step.jump, color=RED, time_width=1.5, buff=0.12), run_time=1.0)
            c.wait_until("r4")
            self.play(*during(disappear(cap3), 0, 0.4), *during([shrink(th, 2)], 0.1, 0.65),
                      *during(appear(box, cap4, lag=0.2), 0.5, 1.0),
                      run_time=min(1.8, c.until("continuous")))
            c.wait_until("continuous")
            self.play(*recolor([box.a], YELLOW), FlashUnder(box.a, color=YELLOW), run_time=1.0)
            c.wait_until("left-hand")
            self.play(*recolor([box.then, box.eq], YELLOW),
                      FlashAround(box.eq, color=YELLOW, time_width=1.5), run_time=1.2)
            c.wait_until("finite")
            self.play(*recolor([finite], YELLOW), FlashUnder(finite, color=YELLOW), run_time=1.0)

        # ---------------- c3: next time, the three rules, end card
        with self.say("c1.recap.3") as c:
            defbox = s2.definition_box(size=44).move_to([0, 0.2, 0])
            self.play(*during(disappear(cap4), 0, 0.4),
                      *during([shrink(box, 3, DIMMED)], 0.1, 0.65),
                      *during(set_alpha([fig, der, th], DIMMED), 0.1, 0.65),
                      *during([FadeIn(defbox, target_position=STRIP[0], scale=0.3)], 0.45, 1.0),
                      run_time=min(2.0, c.until("chain rule")))
            names = ["chain rule", "product rule", "quotient rule"]
            rect = defbox.rect
            labs = []
            for name, x in zip(names, (-4.4, 0.0, 4.4)):
                lab = T(name, 40, YELLOW).move_to([x, -2.4, 0])
                frame = Rectangle(width=lab.width + 0.5, height=lab.height + 0.45,
                                  color=YELLOW, stroke_width=3).move_to(lab)
                # grows out of the box's bottom edge, below the formula
                src = np.array([np.clip(x, rect.get_left()[0] + 0.5, rect.get_right()[0] - 0.5),
                                rect.get_bottom()[1], 0])
                c.wait_until(name)
                self.play(GrowFromPoint(frame, src), *during(appear(lab, shift=None), 0.55, 1.0),
                          run_time=min(1.1, c.until("same")))
                labs.append(frame)
            c.wait_until("same")
            arrows = [Arrow(f.get_top(), [np.clip(f.get_x(), rect.get_left()[0] + 0.5,
                                                  rect.get_right()[0] - 0.5), rect.get_bottom()[1], 0],
                            buff=0.1, color=YELLOW, stroke_width=4) for f in labs]
            self.play(*[GrowArrow(a) for a in arrows], run_time=1.0)
            self.play(FlashAround(defbox.formula[2], color=YELLOW, time_width=1.5),
                      FlashAround(defbox.formula[5], color=YELLOW, time_width=1.5),
                      run_time=min(1.5, c.until()))

        card = end_card()
        sweep_clear(self, time_span(FadeIn(card), 0.6, 1.4), run_time=1.4)
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
