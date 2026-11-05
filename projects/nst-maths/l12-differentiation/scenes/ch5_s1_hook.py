"""Chapter 5, scene 1: hook: from Leibniz's formula to Example 42's Hermite definition. Clips c5.hook.1 – c5.hook.3.

Exports: open_card() (ch4 s8 ends on it). Ends on load_scene("ch5_s2_define").open_shot().
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

PART = "Part 5 · Hermite polynomials"


# ====================== exported helpers ======================
def open_card():
    """The chapter's title card, bare and static, centred at ORIGIN (ch4 s8 ends on exactly this)."""
    return title_card(PART)


def handover_shot():
    """The last frame: s2's open_shot() (the definition line alone at the top)."""
    return load_scene("ch5_s2_define").open_shot()


# ====================== scene pieces ======================
_S2 = None


def s2():
    global _S2
    if _S2 is None:
        _S2 = load_scene("ch5_s2_define")
    return _S2


BIG = 60
DEF_Y = 0.75
DEF_PARTS = [r"H_n(x)", r"\equiv", r"(-1)^n", r"e^{x^2}", r"\frac{d^n}{dx^n}", r"\Big(",
             r"e^{-x^2}", r"\Big)"]
# inside out: gauss, then d^n/dx^n ( ... ), then e^{x^2}, then (-1)^n, then H_n(x) =
STAGES = [[6], [4, 5, 6, 7], [3, 4, 5, 6, 7], [2, 3, 4, 5, 6, 7], list(range(8))]


def big_def():
    m = s2().mtex(*DEF_PARTS, size=BIG)
    m.move_to([0, DEF_Y, 0])
    return m


def stage_centres(idx):
    """Centres of parts idx when only they are typeset, the group centred at (0, DEF_Y)."""
    tmp = s2().mtex(*[DEF_PARTS[i] for i in idx], size=BIG)
    full = s2().mtex(*DEF_PARTS, size=BIG).move_to([0, DEF_Y, 0])
    # keep the baseline: align the gauss part's vertical position with the full line's
    tmp.move_to([0, DEF_Y, 0])
    j = idx.index(6)
    tmp.shift(UP * (full[6].get_center()[1] - tmp[j].get_center()[1]))
    return {i: tmp[k].get_center() for k, i in enumerate(idx)}


def oscillator_plots():
    """Faint preview: four stacked oscillator states H_n(x) e^{-x^2/2}, n = 0..3 (bottom-up)."""
    hs = [lambda x: 1.0, lambda x: 2 * x, lambda x: 4 * x * x - 2, lambda x: 8 * x ** 3 - 12 * x]
    g = VGroup()
    sx = 0.9
    for n, h in enumerate(hs):
        xs = np.linspace(-4, 4, 400)
        amp = max(abs(h(x) * np.exp(-x * x / 2)) for x in xs)
        y0 = -2.2 + 1.35 * n
        base = Line([-4 * sx, y0, 0], [4 * sx, y0, 0], stroke_color=DIM, stroke_width=2)
        curve = FunctionGraph(lambda x, h=h, amp=amp, y0=y0: y0 + 0.55 * h(x / sx) * np.exp(-(x / sx) ** 2 / 2) / amp,
                              x_range=[-4 * sx, 4 * sx, 0.02], color=BLUE)
        curve.set_stroke(width=4)
        g.add(VGroup(base, curve))
    g.move_to([-0.8, -0.2, 0])
    g.set_opacity(0.45)
    return g


class Ch5S1Hook(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()

    # ------------------------------------------------------------ c1: title, then last time
    def clip1(self):
        with self.say("c5.hook.1") as c:
            card = open_card()
            self.play(time_span(FadeIn(card.title, shift=0.3 * DOWN), 0, 0.9),  # early: title card
                      time_span(GrowFromCenter(card.rule), 0, 0.9),
                      time_span(FadeIn(card.course), 0.3, 1.2),
                      time_span(FadeIn(card.part), 0.6, 1.5), run_time=1.5)
            self.remove(*card.get_family())
            self.add(card)
            c.wait_until("last")

            leib = load_scene("ch4_s4_formula").leibniz_card()
            leib.move_to([-1.7, 0.1, 0])
            tri = load_scene("ch4_s3_pattern").pascal_triangle(n_max=3, start=0)
            tri.move_to([4.7, 0.1, 0])
            self.leib, self.tri = leib, tri
            sweep_clear(self, *during(appear(leib, shift=None), 0.5, 1), run_time=1.6)
            c.wait_until("from pascals triangle")
            self.play(*appear(*tri.rows, lag=0.2, shift=0.15 * DOWN), run_time=1.4)
            c.wait_until("coefficients")
            self.play(FlashAround(leib.binom, run_time=1.5, time_width=1.5),
                      FlashAround(tri, run_time=1.5, time_width=1.5))

    # ------------------------------------------------------------ c2: why, then the definition
    def clip2(self):
        leib, tri = self.leib, self.tri
        with self.say("c5.hook.2") as c:
            # {when}: Leibniz card and triangle shrink into the top-right corner
            leib.generate_target()
            tri.generate_target()
            leib.target.scale(0.55)
            tri.target.scale(0.72)
            VGroup(leib.target, tri.target).arrange(RIGHT, buff=0.4).to_corner(UR, buff=0.45)
            self.play(MoveToTarget(leib), MoveToTarget(tri), run_time=min(1.8, c.until("quantum")))
            c.wait_until("quantum")

            plots = oscillator_plots()
            cap = T("quantum mechanics", size=40).set_opacity(0.85)
            cap.move_to([-0.8, -3.45, 0])
            self.play(FadeIn(plots, run_time=1.2), *appear(cap), run_time=1.2)
            c.wait_until("define")

            # {define}: the corner and the preview leave; the Example 42 card arrives
            header = T("Example 42: Hermite polynomials", size=42, color=GREEN)
            header.move_to([0, 2.15, 0])
            border = RoundedRectangle(corner_radius=0.15, width=12.6, height=5.5)
            border.set_stroke(GREEN, 3).set_fill(BG, 1).move_to([0, -0.05, 0]).set_z_index(-1)
            self.header, self.border = header, border
            self.play(*during(disappear(plots, cap, leib, tri), 0, 0.45),
                      *during([FadeIn(border)], 0.45, 0.85),
                      *during(appear(header), 0.55, 1), run_time=1.8)
            c.wait_until("gauss")

            full = big_def()
            self.full = full
            shown = []
            for k, (cue, rt) in enumerate([("gauss", 1.2), ("diff", 1.6), ("front", 1.2),
                                           ("sign", 1.2), ("hermeet polynomial", 1.4)]):
                c.wait_until(cue)
                pos = stage_centres(STAGES[k])
                new = [i for i in STAGES[k] if i not in shown]
                for i in new:
                    full[i].move_to(pos[i])
                moves = [full[i].animate.move_to(pos[i]) for i in shown]
                if k == 2:      # e^{x^2} slides in from the left
                    arrive = [FadeIn(full[3], shift=0.6 * RIGHT)]
                else:
                    arrive = appear(*[full[i] for i in new], shift=None if k in (1,) else 0.2 * DOWN)
                if moves:
                    anims = during(moves, 0, 0.55) + during(arrive, 0.45, 1)
                else:
                    anims = arrive
                self.play(*anims, run_time=min(rt, c.until(None)))
                shown += new
            settle(self, full)
            if c.remaining > 0.8:
                self.play(FlashUnder(full, time_width=1.5, color=YELLOW), run_time=min(1.5, c.until(None)))

    # ------------------------------------------------------------ c3: the claim and the question
    def clip3(self):
        full, header, border = self.full, self.header, self.border
        with self.say("c5.hook.3") as c:
            l1 = T("Show that the recursion relation", size=36)
            math = MathTex(r"H_{n+1} = 2xH_n - 2nH_{n-1}", font_size=48, color=FG)
            holds = T("holds.", size=36)
            l2 = VGroup(math, holds).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
            dn_x = full[4].get_x()
            l1.move_to([0, -0.95, 0]).align_to([dn_x - 0.45, 0, 0], RIGHT)
            l2.move_to([0, -2.0, 0])
            l2.shift(RIGHT * (dn_x - math.get_x()))
            self.play(*appear(l1, l2, lag=0.5), run_time=2.0)  # early: the notes' sentence, read whole
            c.wait_until("question")

            start = full[4].get_bottom() + 0.15 * DOWN
            end = math.get_top() + 0.12 * UP
            arrow = Arrow(start, end, buff=0, color=YELLOW, stroke_width=5)
            q = T("?", size=60, color=YELLOW).next_to(arrow, RIGHT, buff=0.25)
            self.play(GrowArrow(arrow), run_time=1.5)
            self.play(*appear(q), run_time=1.0)

        # after the question is asked, the card shrinks to the top edge: everything but the definition leaves, the line moves up
        target = s2().def_line()
        self.play(*during(disappear(border, header, l1, l2, arrow, q), 0, 0.45),
                  *during([full.animate.scale(44 / BIG).move_to(target)], 0.4, 1),
                  run_time=1.6)
        self.wait(0.8)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(0.3)
