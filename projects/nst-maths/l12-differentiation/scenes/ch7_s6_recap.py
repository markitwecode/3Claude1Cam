"""Chapter 7, scene 6: recap of H1, H2, H4 and I1 in five panels, then next lecture. Clips c7.recap.1 – c7.recap.2.

Opens empty. {recap}: a row of five empty DIM panels along the top. Each recap sentence shows its
callback big in the centre with its short line under it (r1 ticked table + sin line, r2 variable
tags, r3 answers pair + squared equation, r4 e^y y' good / struck, r5 survivors shot); on the next
sentence it shrinks into its panel. {next}: everything shrinks away, "Next lecture: curve sketching
(§4.11)", ch6's labelled figure (no strip) small, s1's dim H3 / H5 minis slide back in. End card
held ~8 s after the last word, then a 1 s fade.
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
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch7_s1_intro")
S2 = load_scene("ch7_s2_basics")
S4 = load_scene("ch7_s4_h4_two")
S5 = load_scene("ch7_s5_i1")
V6 = load_scene("ch6_s2_vocab")

SLOT_W, SLOT_H, SLOT_GAP, SLOT_Y = 2.4, 1.4, 0.25, 3.05
HERO_C = np.array([0, -0.45, 0])
HERO_W, HERO_H = 10.5, 4.4
CAP_Y = -3.35


def slot(k):
    return np.array([(k - 2) * (SLOT_W + SLOT_GAP), SLOT_Y, 0])


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def hero(m, w=HERO_W, h=HERO_H):
    return fit(m, w, h).move_to(HERO_C)


def caption(text, **kw):
    return T(text, 38, **kw).move_to([0, CAP_Y, 0])


def frame(k):
    return RoundedRectangle(corner_radius=0.12, width=SLOT_W, height=SLOT_H).set_stroke(DIM, 2).move_to(slot(k))


class Ch7S6Recap(NarratedScene):
    def construct(self):
        self.frames = [frame(k) for k in range(5)]

        # ------------------------------------------------------------ c7.recap.1
        with self.say("c7.recap.1") as c:
            self.play(*appear(*self.frames, shift=None, lag=0.15), run_time=min(1.4, c.until("r1")))
            c.wait_until("r1")

            # ---- r1: the ticked table beside the sin line
            tbl = S2.ticked_table()
            sl = S2.sin_line(60)
            tbl.scale(5.9 / tbl.height)
            pic1 = VGroup(tbl, sl).arrange(RIGHT, buff=0.9)
            pic1.move_to([0, -0.65, 0])
            cap1 = T("trig and hyperbolic:\nfrom exponentials", 38, line_spacing=0.9)
            cap1.next_to(sl, DOWN, buff=0.7)
            self.play(*appear(tbl, sl, shift=None, lag=0.5),  # early: s2's table, shown whole as a callback
                      run_time=min(1.6, c.until("trig")))
            c.wait_until("trig")
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("exponentials")
            self.play(*flash([sl]), run_time=1.2)
            c.wait_until("r2")

            # ---- r2: the three variable tags
            self.shelve(0, pic1, c.until("variable"))
            tags = S2.variable_tags().scale(1.5).move_to(HERO_C)
            cap2 = caption("check the variable")
            self.play(*swap(cap1, cap2), *during(appear(*tags, lag=0.25), 0.3, 1),  # early: s2's tags, read as "the variable" the line names
                      run_time=1.4)
            c.wait_until("r3")

            # ---- r3: two boxed answers + the squared original equation
            self.shelve(1, tags, c.until("original equation"))
            pair = S4.answers_pair()
            sq = S4.squared_eq(48)
            pic3 = VGroup(pair, sq).arrange(DOWN, buff=0.5)
            hero(pic3, 11.0, 5.0)
            cap3 = caption("two routes, one answer")
            self.play(*appear(pair, shift=None), *swap(cap2, cap3), run_time=min(1.4, c.until("original equation")))
            c.wait_until("original equation")
            self.play(*appear(sq, shift=None), run_time=1.2)
            c.wait_until("r4")

            # ---- r4: e^y y' and the struck one
            self.shelve(2, pic3, c.until("every function"))
            good, bad = S4.ey_good(96), S4.ey_struck(96)
            ck = check_mark(GREEN).scale(1.3)
            xm = cross_mark(RED).scale(1.2)
            pic4 = VGroup(VGroup(good, ck).arrange(RIGHT, buff=0.4),
                          VGroup(bad, xm).arrange(RIGHT, buff=0.4)).arrange(RIGHT, buff=1.6)
            pic4.move_to(HERO_C)
            c.wait_until("every function")
            cap4 = caption("every function of y carries a y′", t2c={"y′": YELLOW})
            self.play(*appear(good, ck, shift=None, lag=0.3), *swap(cap3, cap4), run_time=1.2)
            self.play(*appear(bad, xm, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("r5")

            # ---- r5: the Leibniz card, the two survivors, the YELLOW (n + 1)
            self.shelve(3, pic4, c.until("leibniz"))
            shot = S5.survivors_shot()
            hero(shot)
            cap5 = caption("x runs out: two terms survive")
            self.play(*appear(shot.card, shot.row, shift=None, lag=0.4), run_time=min(1.6, c.until("leibniz")))
            c.wait_until("leibniz")
            self.play(*appear(shot.last, shot.before, shift=None, lag=0.4), run_time=1.4)
            c.wait_until("two terms")
            self.play(*swap(cap4, cap5), *flash([shot.before.n1]), run_time=1.2)  # early: its words are the line itself

        # ------------------------------------------------------------ c7.recap.2
        with self.say("c7.recap.2") as c:
            # r5 takes its place: the row of five, complete
            head = T("Next lecture: curve sketching (§4.11)", 48).move_to([0, 3.1, 0])
            lf = V6.labelled_figure()
            lf.remove(lf.strip)
            lf.scale_to_fit_width(9.4).move_to([-1.2, -0.75, 0])
            minis = VGroup(S1._mini("H3"), S1._mini("H5")).arrange(DOWN, buff=0.4)
            minis.move_to([5.55, -0.6, 0])
            grid = list(self.mobjects)
            self.play(*during([m.animate.scale(0.05, about_point=ORIGIN).set_opacity(0) for m in grid], 0, 0.5),
                      *during(appear(head), 0.5, 1),
                      run_time=min(2.0, c.until("stationary points")))
            self.remove(*grid)
            c.wait_until("stationary points")
            self.play(FadeIn(lf), run_time=min(1.5, c.until("h three")))  # early: last time's figure, shown whole
            c.wait_until("h three")
            minis.shift(4.5 * RIGHT)
            self.play(minis.animate.shift(4.5 * LEFT), run_time=1.3)
            c.wait_until("end")
            self.play(FlashAround(head, run_time=2, time_width=1.5))
        self.wait(7.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    def shelve(self, k, pic, rt):
        """The current hero shrinks into panel k of the top row; the panel lights."""
        pic.generate_target()
        fit(pic.target, SLOT_W - 0.2, SLOT_H - 0.2).move_to(slot(k))
        self.play(MoveToTarget(pic),
                  *during([restyle(self.frames[k], outline=BLUE, width=2)], 0.6, 1),
                  run_time=min(1.4, max(0.8, rt)))
