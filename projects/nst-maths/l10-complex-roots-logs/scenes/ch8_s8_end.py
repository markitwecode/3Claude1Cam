"""Chapter 8, scene 8: recap of the solutions, the two threads, next time. Clips c8.end.1 – c8.end.2.

Panels are imported from s3–s7 (recap_panel / recap_pascal / recap_triangle), scaled into slots.
Clip 1: s1's seven cards, then five panels in a row, each with its short line.
Clip 2: the panels sort into two framed rows (TEAL "the 2πn", GOLD "the turning arrow"), then
clear to the end card: the two threads on the left, "Next: Lecture 11", "Hyperbolic functions" and
cosh x = ½(e^x + e^{−x}) on the right. Held ~8 s, then fades. Last scene of the chapter.
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

S1 = load_scene("ch8_s1_intro")
S3 = load_scene("ch8_s3_f16")
S4 = load_scene("ch8_s4_f17_f12")
S5 = load_scene("ch8_s5_f13")
S6 = load_scene("ch8_s6_f18")
S7 = load_scene("ch8_s7_f19")


def P(x, y):
    return np.array([x, y, 0.0])


# ---------------------------------------------------------------- layout
# recap: r1 r2 r3 on top, r4 r5 below, each picture fitted into (w, h) at its centre
SLOT_H = 2.0
RECAP_SLOTS = [(2.0, -4.75, 1.95), (4.4, -0.75, 1.95), (3.5, 4.0, 1.95),
               (5.0, -1.6, -1.35), (2.0, 3.1, -1.35)]          # (width, x, y)
CAP_GAP = 0.25                   # picture bottom -> caption top
CAP = 28

# threads: TEAL row (r1, r4) and GOLD row (r2, r3, r5), as ch7 s6
ROW1_Y, ROW2_Y = 1.75, -1.95
H1_Y, H2_Y = 3.4, -0.3
THREAD_OF = [0, 1, 1, 0, 1]
THREAD_X = [-2.95, -3.5, 1.2, 1.45, 4.7]
FRAME_H = 2.4


def fit(m, w, h, center):
    s = min(w / m.width, h / m.height)
    return m.scale(s).move_to(center)


def caption(lines, center_top, t2c=None):
    g = VGroup(*[T(s, CAP, t2c=t2c or {}) for s in lines]).arrange(DOWN, buff=0.12)
    g.next_to(center_top, DOWN, buff=0)
    g.shift(LEFT * max(0.0, g.get_right()[0] - 6.55) + RIGHT * max(0.0, -6.55 - g.get_left()[0]))
    return g


# ---------------------------------------------------------------- panels
def panel_r1():
    p = S3.recap_panel()
    return VGroup(p.plane, p.circle, p.gold, p.purple)


def panel_r2():
    return S4.recap_pascal()


def panel_r3():
    p = S5.recap_panel()
    chain = VGroup(p.dashed, p.total, p.chain)
    tri = S4.recap_triangle()
    fit(chain, 0.85, SLOT_H, ORIGIN)
    fit(tri, 2.6, SLOT_H, ORIGIN)
    return VGroup(chain, tri).arrange(RIGHT, buff=0.15)


def panel_r4():
    return S6.recap_panel()


def panel_r5():
    return S7.recap_panel()


CAPTIONS = [
    (["keep the 2πn,", "then divide"], {"2πn": TEAL}),
    (["De Moivre and", "exponentials"], None),
    (["sums are", "geometric series"], None),
    (["the modulus,", "then every argument"], None),
    (["size and phase from", "one complex amplitude"], None),
]


def frame(m, color, h=FRAME_H):
    return (RoundedRectangle(corner_radius=0.15, width=m.width + 0.3, height=h)
            .set_stroke(color, 2).set_fill(BG, 1).move_to(m).set_z_index(-1))


class End(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(8.0)                                    # end card, music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # ============================================================ c8.end.1
    def clip1(self):
        builders = [panel_r1, panel_r2, panel_r3, panel_r4, panel_r5]
        self.pics, self.caps = [], []
        for k, b in enumerate(builders):
            w, x, y = RECAP_SLOTS[k]
            m = fit(b(), w, SLOT_H, P(x, y))
            lines, t2c = CAPTIONS[k]
            cap = caption(lines, P(x, y - SLOT_H / 2 - CAP_GAP), t2c)
            self.pics.append(m)
            self.caps.append(cap)

        title = T("Recap", 48).move_to(P(0, 3.25))
        cards = S1.card_row().move_to(P(0, 0.2))

        with self.say("c8.end.1") as c:
            self.play(*appear(title, shift=None), *appear(*cards.cards, lag=0.08), run_time=1.2)  # early: the title and the seven questions, named as a set
            c.wait_until("r1")
            self.play(*during(disappear(cards), 0, 0.45),
                      *during(appear(self.pics[0], shift=None), 0.5, 1), run_time=1.6)
            c.wait_until(own_word=self.caps[0][0], cue="keep")
            self.play(*appear(self.caps[0], lag=0.2), run_time=1.0)

            for k, cue, word in ((1, "r2", "Moivre"), (2, "r3", "sums"), (3, "r4", "modulus"), (4, "r5", "size")):
                c.wait_until(cue)
                self.play(*appear(self.pics[k], shift=None), run_time=1.0)
                c.wait_until(word)
                self.play(*appear(self.caps[k], lag=0.2), run_time=1.0)
        self.title = title

    # ============================================================ c8.end.2
    def clip2(self):
        targets = [P(THREAD_X[k], ROW1_Y if THREAD_OF[k] == 0 else ROW2_Y) for k in range(5)]
        slide = [0, 4]                                    # these slide; r2, r3, r4 would cross: they re-fade
        moved = {k: self.pics[k].copy().move_to(targets[k]) for k in (1, 2, 3)}
        frames = [frame(m.copy().move_to(t), TEAL if THREAD_OF[k] == 0 else GOLD)
                  for k, (m, t) in enumerate(zip(self.pics, targets))]
        th1 = Line(P(-6.6, ROW1_Y), P(6.6, ROW1_Y)).set_stroke(TEAL, 4, opacity=0.55).set_z_index(-2)
        th2 = Line(P(-6.6, ROW2_Y), P(6.6, ROW2_Y)).set_stroke(GOLD, 4, opacity=0.55).set_z_index(-2)
        h1 = T("the 2πn", 38, TEAL).move_to(P(0, H1_Y)).align_to(P(-6.3, 0), LEFT)
        tag1 = T("F15 · F16 · F18", 30, DIM).move_to(P(0, H1_Y)).align_to(P(6.3, 0), RIGHT)
        h2 = T("the turning arrow", 38, GOLD).move_to(P(0, H2_Y)).align_to(P(-6.3, 0), LEFT)
        tag2 = T("F17 · F12 · F13 · F19", 30, DIM).move_to(P(0, H2_Y)).align_to(P(6.3, 0), RIGHT)
        teal_frames = [f for k, f in enumerate(frames) if THREAD_OF[k] == 0]
        gold_frames = [f for k, f in enumerate(frames) if THREAD_OF[k] == 1]

        # end card
        LX = -6.2
        e_h1 = T("the 2πn", 38, TEAL).move_to(P(0, 1.55)).align_to(P(LX, 0), LEFT)
        e_t1 = T("F15 · F16 · F18", 30, DIM).move_to(P(0, 0.9)).align_to(P(LX, 0), LEFT)
        e_h2 = T("the turning arrow", 38, GOLD).move_to(P(0, -0.45)).align_to(P(LX, 0), LEFT)
        e_t2 = T("F17 · F12 · F13 · F19", 30, DIM).move_to(P(0, -1.1)).align_to(P(LX, 0), LEFT)
        RX = 3.1
        nxt = T("Next: Lecture 11", 48, t2c={"Next:": DIM}).move_to(P(RX, 1.75))
        hyp = T("Hyperbolic functions", 40).move_to(P(RX, 0.9))
        eq = MathTex(r"\cosh x", "=", r"\tfrac{1}{2}\big(", "e^{x}", "+", "e^{-x}", r"\big)", font_size=60)
        eq[3].set_color(GOLD)
        eq[5].set_color(PURPLE)
        eq.move_to(P(RX, -0.75))


        with self.say("c8.end.2", gap=0.0) as c:
            self.play(*during([FadeOut(m) for m in (*self.caps, self.title)], 0, 0.35),
                      *during([FadeOut(self.pics[k]) for k in moved], 0, 0.4),
                      *during([self.pics[k].animate.move_to(targets[k]) for k in slide], 0.3, 0.8),
                      *during([FadeIn(m) for m in moved.values()], 0.6, 1.0),
                      run_time=min(2.0, c.until("two pi N")))
            for k, m in moved.items():
                self.pics[k] = m
            c.wait_until("two pi N")
            self.play(*appear(h1), *[FadeIn(f) for f in teal_frames], FadeIn(th1), run_time=1.0)
            self.play(*appear(tag1), run_time=0.6)  # early: the question ids belong with their thread's name
            c.wait_until("turning arrow")
            self.play(*appear(h2), *[FadeIn(f) for f in gold_frames], FadeIn(th2), run_time=1.0)
            self.play(*appear(tag2), run_time=0.6)  # early: the question ids belong with their thread's name

            c.wait_until("next")
            d = c.until("lecture eleven", floor=0.9)     # rows clear, then "Next: Lecture 11" lands on its words
            rt = d + 0.9
            self.play(*during([FadeOut(m) for m in (*self.pics, *frames, th1, th2)], 0, 0.75 * d / rt),
                      *during([Transform(h1, e_h1), Transform(tag1, e_t1),
                               Transform(h2, e_h2), Transform(tag2, e_t2)], 0.6 * d / rt, 1.0),
                      *during(appear(nxt, shift=None), d / rt, 1.0), run_time=rt)
            c.wait_until(own_word=hyp, cue="hyperbolic functions")
            self.play(*appear(hyp), run_time=1.0)
            c.wait_until("hyperbolic cosine")
            self.play(*appear(eq), run_time=1.3)
            c.wait_until("end")
            self.play(FlashUnder(eq[0], run_time=1.5, time_width=1.5), *recolor(eq[0], YELLOW),
                      run_time=min(1.5, c.until(None)))
