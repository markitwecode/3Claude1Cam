"""Chapter 4, scene 7: recap in five panels, then 2^i and i^i next time. Clips c4.recap.1 – c4.recap.2."""
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

S2 = load_scene("ch4_s2_define")
S3 = load_scene("ch4_s3_map")
S4 = load_scene("ch4_s4_ln2i")
S5 = load_scene("ch4_s5_consequences")
S6 = load_scene("ch4_s6_principal")

TOP_Y = 2.0        # centre of the top row's pictures
BOT_Y = -1.3      # centre of the bottom row's pictures
BOT_CAP_Y = -3.05  # bottom row captions
CAP = 28


def strip_text(g):
    """Remove every Text / MathTex inside g (axis labels are unreadable at thumbnail size)."""
    for sub in list(g.submobjects):
        if isinstance(sub, (Text, MathTex, SingleStringMathTex)):
            g.remove(sub)
        else:
            strip_text(sub)
    return g


class Placer:
    """One scale + shift taking a picture built at its scene's coordinates into its panel."""

    def __init__(self, ref, scale, dst):
        self.c = ref.get_center().copy()
        self.s = scale
        self.d = np.asarray(dst, dtype=float)

    def __call__(self, *mobs):
        for m in mobs:
            m.scale(self.s, about_point=self.c).shift(self.d - self.c)
        return mobs[0] if len(mobs) == 1 else mobs

    def pt(self, p):
        return self.c + self.s * (np.asarray(p) - self.c) + (self.d - self.c)


def panel_r1():
    box = S2.result_box(size=60)
    box.scale(0.6).move_to([-3.45, TOP_Y, 0])
    cap = T("undo the exponential", CAP).next_to(box, DOWN, buff=0.35)
    return box, cap


def panel_r2():
    pair = S3.map_pair()
    wpl, zpl, arr, lab, line, circ = pair
    strip_text(wpl)
    strip_text(zpl)
    place = Placer(pair, 0.42, [3.6, TOP_Y, 0])
    coil = S3.coil()
    place(wpl, zpl, arr, line, circ, coil)
    new_lab = MathTex("e^w", font_size=32, color=GOLD).next_to(arr, UP, buff=0.1)
    base = VGroup(wpl, zpl, arr, new_lab)
    cap = T("lines wrap into circles", CAP).move_to([3.6, wpl.get_bottom()[1] - 0.3, 0])
    return base, line, coil, circ, cap


def panel_r3():
    wpl = strip_text(S4.w_plane(yr=(-9.5, 9.5)))
    L = S4.ladder(ns=(-1, 0, 1), n_fade=2, y_lo=-2.0, y_hi=2.0)
    dots = [L.dots[n] for n in (-1, 0, 1)]
    ref = VGroup(wpl, L.line, *dots, L.fade_top, L.fade_bot, L.brace)
    place = Placer(ref, 0.68, [-4.45, BOT_Y, 0])
    place(wpl, L.line, L.ln2[0], *dots, L.fade_top, L.fade_bot, L.brace)
    blab = MathTex(r"2\pi i", font_size=30, color=TEAL).next_to(L.brace, LEFT, buff=0.1)
    base = VGroup(wpl, L.line, L.ln2[0])
    rungs = [dots[0], dots[1], dots[2], L.fade_top, L.fade_bot]
    cap = T("a ladder, rungs 2πi apart", CAP).move_to([-4.45, BOT_CAP_Y, 0])
    return base, rungs, L.brace, blab, cap


def panel_r4():
    shot = S5.example_shot()
    plane, strip_g, _strip_lab, lad, brace, zdot, _zlab, _tag = shot
    strip_text(plane)
    ref = VGroup(plane, strip_g, lad, brace[0], zdot)
    place = Placer(ref, 0.38, [-0.5, BOT_Y, 0])
    place(plane, strip_g, lad, brace[0], zdot)
    zlab = MathTex("3 + 4i", font_size=28, color=YELLOW).next_to(zdot, RIGHT, buff=0.12)
    set_backstroke(zlab)
    base = VGroup(plane, strip_g, lad[0])
    rungs = [*lad[1], lad[2]]
    green = lad[1][0]
    cap = VGroup(MathTex(r"\ln e^z", font_size=32), T(": any rung", CAP))
    cap.arrange(RIGHT, buff=0.06, aligned_edge=DOWN).move_to([-0.5, BOT_CAP_Y, 0])
    return base, rungs, green, zdot, zlab, cap


def panel_r5():
    s = S6.pull_back_shot()
    strip_text(s.plane)
    parts = [s.plane, s.green, s.open_end, s.closed_end, s.spiral1, s.spiral2, s.arrow, s.red]
    ref = VGroup(*parts, s.red_label, s.angle_label)
    place = Placer(ref, 0.43, [3.95, BOT_Y, 0])
    rl, al = s.red_label.get_center(), s.angle_label.get_center()
    place(*parts)
    red_label = MathTex(r"-2\pi", font_size=30, color=RED).move_to(place.pt(rl))
    angle_label = MathTex("0", font_size=32, color=GREEN).move_to(place.pt(al))
    set_backstroke(red_label)
    set_backstroke(angle_label)
    base = VGroup(s.plane, s.green, s.open_end, s.closed_end, s.spiral1, s.spiral2, s.arrow)
    cap = T("principal values: off by a rung", CAP).move_to([3.95, BOT_CAP_Y, 0])
    return base, s.red, red_label, angle_label, cap


NX, NY = 4.4, 0.6      # the "next time" column
LIST_X, LIST_Y0, LIST_DY = -6.3, 1.9, 0.95   # the end card's recap list


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    def clip1(self):
        with self.say("c4.recap.1") as c:
            # r1: the boxed definition
            box, cap1 = panel_r1()
            f = box.formula
            self.play(FadeIn(box.rect), *appear(f, shift=None), run_time=1.0)
            c.wait_until(own_word=cap1)
            self.play(*appear(cap1), run_time=1.0)
            c.wait_until("ordinary log")
            self.play(FlashUnder(f[3], color=GOLD, run_time=1.2, time_width=1.5))
            c.wait_until("the argument")
            self.play(FlashUnder(f[7], color=YELLOW, run_time=1.2, time_width=1.5))
            c.wait_until("plus two pi N")
            self.play(FlashUnder(f[9], color=TEAL, run_time=1.2, time_width=1.5))
            p1 = VGroup(box)

            # r2: the line coils onto the circle
            c.wait_until("r2")
            base2, line, coil, circ, cap2 = panel_r2()
            self.play(FadeIn(base2), FadeIn(line), run_time=1.0)
            c.wait_until("wraps")
            moving = line.copy()
            self.play(ReplacementTransform(moving, coil), run_time=1.6)
            self.play(ReplacementTransform(coil, circ), run_time=0.8)
            c.wait_until("into circles")
            self.play(*appear(cap2), run_time=1.0)
            c.wait_until("whole column")
            self.play(VShowPassingFlash(line.copy().set_stroke(YELLOW, 7), time_width=0.6),
                      run_time=min(1.2, c.until("r3")))
            p2 = VGroup(base2, line, circ)

            # r3: the ladder of ln 2i
            c.wait_until("r3")
            base3, rungs3, brace3, blab3, cap3 = panel_r3()
            self.play(FadeIn(base3), run_time=0.8)
            c.wait_until(own_word=cap3)
            self.play(*appear(*rungs3, shift=None, lag=0.15), *appear(cap3), run_time=1.2)
            c.wait_until("two pi eye apart")
            self.play(GrowFromCenter(brace3), *appear(blab3), run_time=min(1.0, c.until("r4")))
            p3 = VGroup(base3, *rungs3, brace3, blab3)

            # r4: ln e^z lands on any rung of z's ladder
            c.wait_until("r4")
            base4, rungs4, green4, zdot4, zlab4, cap4 = panel_r4()
            self.play(FadeIn(base4), FadeIn(zdot4, scale=0.5), *appear(zlab4), run_time=1.0)
            c.wait_until("any rung")
            self.play(*appear(*rungs4, shift=None, lag=0.12), *appear(cap4), run_time=1.2)
            self.play(FlashAround(green4, color=GREEN, run_time=1.0, time_width=1.5),
                      run_time=min(1.0, c.until("r5")))
            p4 = VGroup(base4, *rungs4, zdot4, zlab4)

            # r5: pi + pi pulled back by a full turn
            c.wait_until("r5")
            base5, red5, rlab5, alab5, cap5 = panel_r5()
            self.play(FadeIn(base5), *appear(cap5), run_time=1.0)
            c.wait_until("break")
            self.play(Create(red5), *during(appear(rlab5, alab5, lag=0.3), 0.4, 1.0),
                      run_time=min(1.3, c.until(None)))
            p5 = VGroup(base5, red5, rlab5, alab5)

            self.pics = [p1, p2, p3, p4, p5]
            self.caps = [cap1, cap2, cap3, cap4, cap5]

    def clip2(self):
        heading = T("Next time", 40, color=DIM).move_to([NX, 3.3, 0])
        two_i = MathTex("2^i", font_size=80).move_to([NX, NY, 0])
        two_i[0][1].set_color(PINK)
        set_backstroke(two_i, width=8)
        offs = [0.8, 1.45, -0.8, -1.45]
        dots = [Dot([NX, NY + d, 0], radius=0.08, color=TEAL).set_z_index(-1) for d in offs]
        fades = [Dot([NX, NY + sg * d, 0], radius=r, color=TEAL).set_opacity(o).set_z_index(-1)
                 for sg in (1, -1) for d, r, o in ((1.95, 0.07, 0.55), (2.3, 0.06, 0.25))]
        ii = MathTex("i^i", "=", "?", font_size=64).move_to([NX, -2.55, 0])
        ii[0].set_color(PINK)
        ii[2].set_color(YELLOW)

        with self.say("c4.recap.2") as c:
            for p in self.pics:
                settle(self, p)
            # the pictures go; their five lines gather into the recap list on the left
            moves = []
            for k, cap in enumerate(self.caps):
                cap.generate_target()
                cap.target.scale(32 / CAP).move_to([0, LIST_Y0 - LIST_DY * k, 0]).align_to([LIST_X, 0, 0], LEFT)
                moves.append(MoveToTarget(cap))
            self.play(*during([FadeOut(p) for p in self.pics], 0, 0.4),
                      *during(moves, 0.4, 1.0), run_time=1.8)
            self.play(*appear(heading), run_time=0.8)
            c.wait_until("infinitely many")
            self.play(*appear(*dots, *fades, shift=None, lag=0.1), run_time=1.2)
            c.wait_until("two to the power eye")
            self.play(*appear(two_i), run_time=1.0)
            c.wait_until("ii")
            self.play(*appear(ii), run_time=1.0)
            c.wait_until("real number")
            self.play(FlashUnder(ii[2], run_time=1.5, time_width=1.5))
