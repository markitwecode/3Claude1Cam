"""Chapter 1, scene 3: the traffic light's ring, its clock, three flip-flops R A G and their codes;
eight patterns, four unused (don't cares); that choice was a state assignment. Clips c1.traffic.1 – c1.traffic.4.

Reuses s1's traffic_ring / make_ff / lamp_column (load_scene("ch1_s1_hook")) and s5's clock_wave.
"""
# style: 2
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402,F401
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.paths import load_scene  # noqa: E402
from lib.style import *  # noqa: E402,F403

S1 = load_scene("ch1_s1_hook")
clock_wave = load_scene("ch1_s5_divide5").clock_wave
traffic_ring, make_ff, lamp_column = S1.traffic_ring, S1.make_ff, S1.lamp_column
LAMP_COLS = (S1.LAMP_RED, S1.LAMP_AMBER, S1.LAMP_GREEN)
CODES = ["100", "110", "001", "010"]


def _p(x, y):
    return np.array([x, y, 0.0])


# ---- layout --------------------------------------------------------------------------------------
RING_S = 0.7
RING_C = _p(-3.05, 0.7)
FX = 3.2                       # flip-flop column x
FF_Y = [1.75, -0.15, -2.05]    # R, A, G
LX = 6.0                       # lamp column x
GX = 3.95                      # pattern grid centre x
GRID_Y = [1.0, -0.7]
GRID_PITCH = 1.35


def ff_unit(y):
    ff = make_ff(size=56).scale(0.5, about_point=ORIGIN).shift(_p(FX, y))
    return ff


def bit_at(ff, b):
    return T(b, 44, GREEN).next_to(ff.q_w, RIGHT, buff=0.14)


def ring_flash(circle):
    """A bright bump running once round a state's own circle (no bounding-box flash fragments)."""
    return VShowPassingFlash(circle.copy().set_stroke(YELLOW, 7), time_width=0.6, taper_width=0.1)


def chip_cross(chip):
    """A GOLD X just above an unused chip (where the used chips carry their lamp icon); the code stays clear."""
    return cross_mark(color=GOLD, r=0.16).set_stroke(width=6).next_to(chip, UP, buff=0.12)


def pattern_chip(code):
    box = RoundedRectangle(corner_radius=0.12, width=1.2, height=0.72).set_stroke(DIM, 2).set_fill(BG, 1)
    txt = Mono(code, 34, FG).move_to(box)
    g = VGroup(box, txt)
    g.box, g.txt, g.code = box, txt, code
    return g


class Traffic(NarratedScene):
    def construct(self):
        ring = traffic_ring(CODES, code_size=44).scale(RING_S).move_to(RING_C)
        codes = list(ring.codes)

        # ---------------------------------------------------------------- c1.traffic.1
        with self.say("c1.traffic.1") as c:
            self.play(*[FadeIn(a) for a in ring.arrows], *[FadeIn(s, scale=0.9) for s in ring.states],
                      run_time=min(1.5, c.until("order")))
            c.wait_until("red")
            dot = Dot(ring.inner(0), radius=0.11, color=YELLOW)
            self.play(FadeIn(dot, scale=0.5), ring_flash(ring.circles[0]), run_time=0.8)
            for i, (cue, nth) in enumerate([("red and amber", 0), ("green", 0), ("amber", 1), ("back to red", 0)]):
                c.wait_until(cue, nth=nth)
                nxt = (i + 1) % 4
                self.play(dot.animate.move_to(ring.inner(nxt)), ring_flash(ring.circles[nxt]),
                          run_time=0.8)
            c.wait_until("noinputs")

            clk = clock_wave(width=5.0, height=0.6, periods=4).move_to(_p(-2.8, -2.4))
            clk_l = T("CLK", 36, YELLOW).next_to(clk, LEFT, buff=0.3)
            self.play(*appear(clk_l, clk, shift=None, lag=0.2), run_time=1.0)

            # the dot steps once per rising edge as a cursor sweeps the wave
            x0, x1 = clk.get_left()[0], clk.get_right()[0]
            fr = [(clk.rising_x(k) - x0) / (x1 - x0) for k in range(4)]
            pts = [ring.inner(i) for i in range(4)]
            cursor = Line(_p(x0, -2.85), _p(x0, -1.95)).set_stroke(FG, 3)
            self.play(FadeIn(cursor), run_time=0.3)

            def move_cursor(m, a):
                m.set_x(x0 + a * (x1 - x0))

            def move_dot(m, a):
                done = [k for k in range(4) if a >= fr[k]]
                if not done:
                    m.move_to(pts[0])
                    return
                k = done[-1]
                t = smooth(min(1.0, (a - fr[k]) / 0.08))
                m.move_to(interpolate(pts[k], pts[(k + 1) % 4], t))

            self.play(UpdateFromAlphaFunc(cursor, move_cursor), UpdateFromAlphaFunc(dot, move_dot),
                      rate_func=linear, run_time=max(2.5, c.until("two") - 0.1))
            self.play(FadeOut(cursor), run_time=0.3)
            c.wait_until("two")

            two = VGroup(T("4 states:", 40, GOLD), T("2 flip-flops would do", 40, GOLD)).arrange(DOWN, buff=0.25)
            two.move_to(_p(3.8, 0.7))
            self.play(*appear(two, lag=0.4), run_time=1.2)

        # ---------------------------------------------------------------- c1.traffic.2
        with self.say("c1.traffic.2", gap=1.5) as c:
            ffs = [ff_unit(y) for y in FF_Y]
            two_t = T("4 states: 2 flip-flops would do", 32, GOLD).move_to(_p(3.5, 3.2))
            self.play(*during(swap(two, two_t, shift=None), 0, 0.5),
                      *during(appear(*ffs, shift=0.25 * LEFT, lag=0.2), 0.45, 1.0),
                      *during(set_alpha([clk, clk_l], 0.4), 0, 0.5),
                      run_time=min(1.8, c.until("names")))
            c.wait_until("names")

            names = [T(n, 48, col) for n, col in zip("RAG", LAMP_COLS)]
            for nm, ff in zip(names, ffs):
                nm.next_to(ff.d_w, LEFT, buff=0.2)
            for nm, cue in zip(names, ["red, amber", "amber and green", "and green"]):
                c.wait_until(cue)
                self.play(*appear(nm), run_time=0.7)
            c.wait_until("red")

            # {red}: the dot is on red; the flip-flops show 100 and the code appears
            bits = [bit_at(ff, b) for ff, b in zip(ffs, CODES[0])]
            self.play(*appear(*bits, shift=None, lag=0.15), ring_flash(ring.circles[0]),
                      run_time=1.0)
            self.play(*appear(codes[0], shift=0.2 * LEFT), run_time=0.9)

            for i, mark in [(1, "redamber"), (2, "green"), (3, "amber")]:
                c.wait_until(mark)
                anims = [dot.animate.move_to(ring.inner(i))]
                for k in range(3):
                    if CODES[i][k] != bits[k].text:
                        nb = bit_at(ffs[k], CODES[i][k])
                        anims += swap(bits[k], nb, shift=None)
                        bits[k] = nb
                self.play(*anims, run_time=min(0.9, 0.45 * c.until()))
                self.play(*appear(codes[i], shift=0.2 * (RIGHT if i == 3 else LEFT)), run_time=0.8)
            settle(self, ring)
            c.wait_until("lamps")

            # {lamps}: each Q wired straight to its lamp
            lamps = lamp_column((0, 1, 0), scale=2.2).move_to(_p(LX, FF_Y[1] + 0.3))
            wires = []
            for k, ff in enumerate(ffs):
                y = ff.q_w.get_y()
                xs = bits[k].get_right()[0] + 0.12
                ly = lamps.lamps[k].get_y()
                lx = lamps.lamps[k].get_left()[0] - 0.05
                w = VMobject().set_points_as_corners([_p(xs, y), _p(5.1, y), _p(5.1, ly), _p(lx, ly)])
                wires.append(w.set_stroke(GREEN, 4))
            self.play(FadeIn(lamps, shift=0.2 * LEFT), *[Create(w) for w in wires], run_time=1.5)
            cap = T("no output logic", 40, YELLOW).move_to(_p(4.5, 3.15))
            self.play(*swap(two_t, cap), run_time=1.2)  # early: the caption the next words say

        # ---------------------------------------------------------------- c1.traffic.3
        with self.say("c1.traffic.3", gap=0.7) as c:
            sweep_clear(self, keep=[ring, dot], run_time=1.0)
            chips = []
            for j in range(8):
                ch = pattern_chip(format(j, "03b"))
                ch.move_to(_p(GX + (j % 4 - 1.5) * GRID_PITCH, GRID_Y[j // 4]))
                chips.append(ch)
            self.play(*appear(*chips, shift=None, lag=0.1), run_time=min(1.4, c.until("only four")))
            c.wait_until("only four")

            used = [chips[int(code, 2)] for code in CODES]
            icons = [lamp_column(tuple(int(b) for b in code), scale=0.5).next_to(ch, UP, buff=0.08)
                     for code, ch in zip(CODES, used)]
            self.play(*[ch.box.animate.set_stroke(GREEN, 5) for ch in used], *[ch.txt.animate.set_color(GREEN) for ch in used],
                      *appear(*icons, shift=None, lag=0.1), run_time=1.2)
            c.wait_until("unused")

            unused = [chips[int(code, 2)] for code in ["000", "011", "101", "111"]]
            for ch, cue in zip(unused, ["zero zero zero", "zero one one", "one zero one", "and one one one"]):
                c.wait_until(cue)
                self.play(restyle(ch, op=0.35), run_time=0.6)
            c.wait_until("name")

            label = T("unused states", 40).move_to(_p(GX, -1.6))
            self.play(*appear(label), run_time=1.0)
            quote = VGroup(T("“Unused states,", 30, DIM), T("000, 011, 101 and 111.”", 30, DIM)).arrange(DOWN, buff=0.14).move_to(_p(GX, -3.0))
            self.play(*appear(quote, shift=None), run_time=1.0)
            c.wait_until("dontcare")

            crosses = [chip_cross(ch) for ch in unused]
            self.play(*appear(*crosses, shift=0.15 * DOWN, lag=0.2), run_time=1.4)
            tag = T("don’t care", 40, GOLD).move_to(_p(GX, -2.2))
            c.wait_until("don't care")
            self.play(*appear(tag), run_time=1.0)

        # ---------------------------------------------------------------- c1.traffic.4
        with self.say("c1.traffic.4") as c:
            sweep_clear(self, ring.animate.move_to(_p(0, 1.45)), keep=[ring], run_time=min(2.0, c.until("state assignment")))
            cap = T("a state assignment", 44, FG, t2c={"state assignment": YELLOW}).move_to(_p(0, -0.85))
            c.wait_until(own_word=cap)
            self.play(*appear(cap), run_time=1.0)
            c.wait_until("in general")

            lines = ["“In general, state assignment is a",
                     "difficult problem and the optimum",
                     "choice is not always obvious”"]
            hard = VGroup(*[T(s, 34, YELLOW) for s in lines]).arrange(DOWN, buff=0.2).move_to(_p(0, -2.3))
            self.play(*appear(*hard, shift=None, lag=0.6), run_time=2.0)
            later = T("→ Part 4", 34, BLUE).move_to(_p(5.4, -3.2))
            c.wait_until(own_word=later)
            self.play(*appear(later, shift=0.2 * LEFT), run_time=1.0)

        self.wait(2.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
