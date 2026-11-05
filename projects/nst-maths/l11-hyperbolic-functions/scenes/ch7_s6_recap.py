"""Chapter 7, scene 6: recap of Sheet G in a 2x2 grid, then next lecture + H2 card. Clips c7.recap.1 – c7.recap.2."""
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
S2 = load_scene("ch7_s2_g1")
S3 = load_scene("ch7_s3_g2")
S4 = load_scene("ch7_s4_g3")
S5 = load_scene("ch7_s5_g4")

PW, PH = 6.5, 3.4
CENTRES = [np.array([-3.4, 1.85, 0]), np.array([3.4, 1.85, 0]),
           np.array([-3.4, -1.85, 0]), np.array([3.4, -1.85, 0])]
REG_W, REG_H = 5.3, 2.3


def fit(m, w, h):
    m.scale(min(w / m.width, h / m.height))
    return m


def region(k):
    return CENTRES[k] + np.array([0.35, 0.22, 0])


def caption_pos(k):
    return CENTRES[k] + np.array([0, -PH / 2 + 0.4, 0])


def panel(k):
    """An unlit G-card frame (s1 styling) with its tag in the top-left corner."""
    frame = RoundedRectangle(corner_radius=0.15, width=PW, height=PH).set_fill(BG, 1).set_stroke(DIM, 2)
    frame.move_to(CENTRES[k])
    tag = T(f"G{k + 1}", 36, weight=BOLD, color=DIM)
    tag.move_to(frame.get_corner(UL) + np.array([0.5, -0.42, 0]))
    return frame, tag


def light(frame, tag):
    return [restyle(frame, outline=BLUE, width=3), tag.animate.set_color(YELLOW)]


def h2_card():
    frame = RoundedRectangle(corner_radius=0.15, width=7.6, height=3.9).set_fill(BG, 1).set_stroke(BLUE, 3)
    tag = T("H2", 40, weight=BOLD, color=YELLOW).move_to(frame.get_top() + 0.5 * DOWN)
    l1 = MathTex(r"\frac{d}{dx}\sinh x,\quad \frac{d}{dx}\cosh x,\quad \frac{d}{dx}\tanh x", font_size=46)
    if l1.width > 6.8:
        l1.scale_to_fit_width(6.8)
    l1.move_to(frame.get_center() + 0.15 * UP)
    words = T("from exponentials", 32, color=DIM)
    chip_p = S1._chip([MathTex(r"e^{x}", font_size=40, color=GOLD)], GOLD)
    chip_m = S1._chip([MathTex(r"e^{-x}", font_size=40, color=PURPLE)], PURPLE)
    row = VGroup(words, chip_p, chip_m).arrange(RIGHT, buff=0.3)
    row.move_to(frame.get_bottom() + 0.75 * UP)
    g = VGroup(frame, tag, l1, words, chip_p, chip_m)
    g.frame, g.tag, g.body, g.words, g.chip_p, g.chip_m = frame, tag, l1, words, chip_p, chip_m
    return g


class Ch7S6Recap(NarratedScene):
    def construct(self):
        panels = [panel(k) for k in range(4)]

        # ------------------------------------------------------------ c7.recap.1
        with self.say("c7.recap.1") as c:
            self.play(*appear(*[p[0] for p in panels], shift=None, lag=0.15),  # early: the grid shown whole, then walked
                      *appear(*[p[1] for p in panels], lag=0.15),               # early: card tags G1..G4
                      run_time=min(1.4, c.until("r1")))
            c.wait_until("r1")

            # ---- G1: tan formula (dimmed), boxed tanh(x+y) with the minus turning into a plus
            f1, t1 = panels[0]
            tan = S2.tan_sum_formula(44)
            ans = S2.boxed_answer(48)
            stack = VGroup(tan, ans).arrange(DOWN, buff=0.22)
            fit(stack, REG_W, REG_H).move_to(region(0))
            self.play(*light(f1, t1), *appear(tan, shift=None), run_time=min(1.2, c.until("divide through")))
            c.wait_until("divide through")
            self.play(*set_alpha([tan], 0.4), *appear(ans, shift=None),
                      run_time=min(1.6, c.until("plus underneath")))
            cap1 = MathTex(r"\text{divide by }\cosh x\,\cosh y", font_size=34).move_to(caption_pos(0))
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("plus underneath")
            # the tan formula's minus, then the plus that replaces it
            self.play(FlashAround(tan.minus, color=BLUE, run_time=1.0, time_width=1.5),
                      time_span(FlashAround(ans.plus, run_time=1.0, time_width=1.5), 0.9, 1.9),
                      run_time=1.9)
            c.wait_until("r2")

            # ---- G2: ellipse with a running point; hyperbola, one branch
            f2, t2 = panels[1]
            E = S3.ellipse_sketch()
            ell = VGroup(E.axes, E.curve, E.point)
            H = S3.hyperbola_sketch()
            hyp = VGroup(H.axes, H.left, H.right, H.cross)
            fit(ell, 2.6, 2.3)
            fit(hyp, 2.6, 2.3)
            ell.move_to(region(1) + 1.5 * LEFT)
            hyp.move_to(region(1) + 1.3 * RIGHT)
            ell_path = E.curve.copy()
            hyp_path = H.right.copy()
            self.play(*light(f2, t2), *appear(E.axes, E.curve, E.point, shift=None, lag=0.2),
                      run_time=min(1.2, c.until("trace the whole")))
            c.wait_until("trace the whole")
            self.play(MoveAlongPath(E.point, ell_path), run_time=min(2.5, c.until("shine and cosh")),
                      rate_func=linear)
            c.wait_until("shine and cosh")
            self.play(*appear(H.axes, H.right, H.left, shift=None, lag=0.2),
                      run_time=min(1.2, 0.55 * c.until("only one branch")))
            self.play(*appear(H.cross, shift=None), run_time=min(0.8, c.until("only one branch")))
            c.wait_until("only one branch")
            hdot = Dot(hyp_path.get_start(), radius=0.08, color=FG).set_stroke(TEAL, 2)
            cap2 = MathTex(r"\cosh\theta \ge 1:\ \text{one branch}", font_size=34).move_to(caption_pos(1))
            self.play(*appear(hdot, shift=None), *appear(cap2), run_time=0.8)
            self.play(MoveAlongPath(hdot, hyp_path), rate_func=linear, run_time=1.8)
            c.wait_until("r3")

            # ---- G3: tanh / tanh^-1 mirrored in y = x, asymptotes swinging
            f3, t3 = panels[2]
            P = S4.tanh_panel(False, unit=0.33, center=region(2) + 1.0 * LEFT + 0.12 * UP)
            ax = P.ax
            hp = S4.dline(ax, (-3, 1), (3, 1), GOLD)
            hm = S4.dline(ax, (-3, -1), (3, -1), PURPLE)
            lab_t = MathTex(r"\tanh x", font_size=38, color=TEAL)
            lab_i = MathTex(r"\tanh^{-1}x", font_size=38, color=S4.INV_C)
            labs = VGroup(lab_t, lab_i).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
            labs.next_to(ax, RIGHT, buff=0.6)
            self.play(*light(f3, t3), *appear(ax, P.mirror, hp, hm, P.tanh, shift=None, lag=0.1),
                      *appear(lab_t), run_time=min(1.4, c.until("mirrored")))
            c.wait_until("mirrored")
            inv = P.tanh.copy()
            self.add(inv)
            self.play(S4.flip(inv, ax), S4.flip(hp, ax), S4.flip(hm, ax),
                      run_time=min(1.8, c.until("why equals ex")))
            cap3 = MathTex(r"\text{inverse} = \text{mirror in } y = x", font_size=34).move_to(caption_pos(2))
            self.play(*recolor([inv], S4.INV_C), *appear(lab_i), *appear(cap3), run_time=1.0)
            c.wait_until("r4")

            # ---- G4: boxed derivative over its graph, (-1) chip
            f4, t4 = panels[3]
            A = S5.g4_answer(52)
            chip = S5.minus_one_chip(40)
            G = S5.deriv_graph(u=0.65)
            left = VGroup(A, chip).arrange(DOWN, buff=0.3)
            body = VGroup(left, G).arrange(RIGHT, buff=0.4)
            fit(body, REG_W, REG_H).move_to(region(3))
            chip.scale(1.25).next_to(A, DOWN, buff=0.25)
            self.play(*light(f4, t4), run_time=0.8)
            c.wait_until("derivative")
            self.play(*appear(A, shift=None), run_time=min(1.2, c.until("minus ex squared")))
            c.wait_until("minus ex squared")
            self.play(*appear(G.ax, G.curve, shift=None, lag=0.3), run_time=min(1.4, c.until("chain-rule")))
            c.wait_until("chain-rule")
            cap4 = MathTex(r"\text{mind the chain-rule minus}", font_size=34).move_to(caption_pos(3))
            self.play(*appear(chip), *appear(cap4), run_time=1.0)
            self.play(*flash([chip]), run_time=1.2)

        # ------------------------------------------------------------ c7.recap.2
        with self.say("c7.recap.2") as c:
            head = T("Next lecture: differentiation", 48)
            sub = T("(Chapter 4 of the notes)", 32, color=DIM)
            heading = VGroup(head, sub).arrange(DOWN, buff=0.2).move_to(np.array([0, 2.45, 0]))
            grid = list(self.mobjects)
            self.play(*during([m.animate.scale(0.05, about_point=ORIGIN).set_opacity(0) for m in grid], 0, 0.55),
                      *during(appear(head, sub, lag=0.3), 0.55, 1),
                      run_time=min(2.2, c.until("section h")))
            c.wait_until("section h")
            card = h2_card().move_to(np.array([0, -0.9, 0]))
            self.remove(*grid)
            self.play(*appear(card.frame, card.tag, card.body, shift=None, lag=0.25),
                      run_time=min(1.5, c.until("exponentials")))
            c.wait_until("exponentials")
            self.play(*appear(card.words, card.chip_p, card.chip_m, lag=0.3), run_time=1.0)
            c.wait_until("end")
            self.play(FlashAround(card.frame, run_time=2, time_width=1.5))
        self.wait(7.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
