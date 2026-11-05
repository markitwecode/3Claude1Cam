"""Chapter 3, scene 8: recap in five panels, then what comes next. Clips c3.recap.1 – c3.recap.2."""
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

S2 = load_scene("ch3_s2_cube")
S3 = load_scene("ch3_s3_sum")
S4 = load_scene("ch3_s4_geometric")
S5 = load_scene("ch3_s5_conjugate")
S6 = load_scene("ch3_s6_result")
H4 = load_scene("ch4_s1_hook")

TOP_Y = 2.0       # centre of the top row's pictures
BOT_Y = -1.55      # centre of the bottom row's pictures
TOP_CAP = 0.15     # y of the top row's captions
BOT_CAP = -3.05    # y of the bottom row's captions
LIT, DIMMED_P = 1.0, 0.4


def fit(g, left, right):
    """Scale g down if wider than [left, right], then centre it there in x."""
    if g.width > right - left:
        g.scale_to_fit_width(right - left)
    g.set_x((left + right) / 2)
    return g


def caption_at(cap, x, y):
    return cap.move_to([x, y, 0])


# ---------------------------------------------------------------- the five panels
def panel_r1():
    c = np.array([-4.95, TOP_Y, 0])
    pic = S2.mirror_pairs(center=c, unit=0.72, extent=1.45)
    cap = MathTex(r"\cos^3\theta", "=", r"\tfrac14\cos 3\theta", "+", r"\tfrac34\cos\theta", font_size=30)
    for i in (0, 2, 4):
        cap[i].set_color(BLUE)
    caption_at(cap, -5.0, TOP_CAP)
    cap.shift((-6.5 - cap.get_left()[0]) * RIGHT)
    return pic, cap


def panel_r2(left):
    plane = S3.argand_plane(origin=ORIGIN, unit=0.56, xr=(-1.1, 3.3), yr=(-0.15, 4.3))
    chain = S3.unit_chain(S3.N6, S3.TH6, origin=ORIGIN, unit=0.56)
    shadow = S3.chain_shadow(S3.N6, S3.TH6, origin=ORIGIN, unit=0.56, row=0.11)
    cap = MathTex("S_N", "=", r"\mathrm{Re}", r"\Big[\sum e^{ik\theta}\Big]", font_size=30)
    cap[2].set_color(BLUE)
    caption_at(cap, 0, TOP_CAP)
    cap.shift((left + 0.45 - cap.get_left()[0]) * RIGHT)
    pic = VGroup(plane, chain, shadow).move_to([cap.get_x(), TOP_Y + 0.1, 0])
    return pic, cap, plane, chain, shadow


def panel_r3(left):
    lhs1 = S4.lhs(r"G=", S4.Y1)
    t1, p1 = S4.row([0, 1, 2, 3, 4], S4.Y1)
    lhs2 = S4.lhs(r"\lambda G=", S4.Y2, lam=0)
    t2, p2 = S4.row([1, 2, 3, 4, 5], S4.Y2)
    strikes = []
    for k in range(1, 5):
        for t in (t1[k], t2[k - 1]):
            strikes.append(Line(t.get_corner(DL) + 0.06 * DL, t.get_corner(UR) + 0.06 * UR).set_stroke(RED, 4))
    row1 = VGroup(lhs1, *t1, *p1)
    row2 = VGroup(lhs2, *t2, *p2)
    st = VGroup(*strikes)
    pic = VGroup(row1, row2, st)
    pic.scale(0.62)
    fit(pic, left + 0.35, 6.55).set_y(TOP_Y + 0.25)
    flag = S4.lam_flag()
    caption_at(flag, pic.get_x(), TOP_CAP + 0.25)
    return pic, flag, row1, row2, st


def panel_r4():
    B1, B2 = S5.conj_rows(size=30)
    pic = VGroup(B1, B2)
    fit(pic, -6.55, -1.15).set_y(BOT_Y + 0.15)
    line = S5.mt([("(1-", FG), (S5.EI, GOLD), (")(1-", FG), (S5.EMI, PURPLE), (")", FG), ("=", FG),
                  (r"2(1-\cos\theta)", BLUE)], 32)
    tag = T("real", 30, color=BLUE)
    cap = VGroup(line, tag)
    tag.next_to(line, RIGHT, buff=0.3).align_to(line, DOWN)
    fit(cap, -6.55, -1.15).set_y(BOT_CAP)
    return pic, cap, B1, B2, line, tag


def panel_r5():
    sc = S6.straight_chain(origin=ORIGIN, unit=0.34)
    box = S6.boxed_result(size=28)
    pic = VGroup(sc, box).arrange(RIGHT, buff=0.4)
    sc.shift((box.get_center()[1] - sc.chain.get_center()[1]) * UP + 0.2 * UP)
    fit(pic, -0.65, 6.55).set_y(BOT_Y)
    cap = MathTex(r"\theta=", r"2\pi m", r":\quad S_N=N", font_size=34)
    cap[1].set_color(TEAL)
    caption_at(cap, pic.get_x(), BOT_CAP)
    return pic, cap, sc, box


# ---------------------------------------------------------------- the end card
OE = np.array([2.4, -1.8, 0])   # end card's plane origin


def end_card():
    plane = H4.argand_plane().shift(OE - H4.O)
    z = OE + 2 * H4.U * UP
    dot = Dot(z, radius=0.12, color=YELLOW)
    zl = MathTex("2i", font_size=44, color=YELLOW).next_to(dot, DR, buff=0.1)
    wq = MathTex("w", "=", r"\mathord{?}", font_size=52).move_to([-3.6, z[1], 0])
    wq[2].set_color(YELLOW)
    arr = Arrow(wq.get_right() + 0.25 * RIGHT, dot.get_center() + 0.22 * LEFT, buff=0, color=GOLD,
                stroke_width=6, max_tip_length_to_length_ratio=0.07)
    el = MathTex("e^w", font_size=48, color=GOLD).next_to(arr, UP, buff=0.2)
    qx = wq[2].get_x()
    qs = VGroup()
    for k in (1, 2, 3):
        for s in (1, -1):
            q = MathTex(r"\mathord{?}", font_size=52, color=TEAL).move_to([qx, z[1] + s * 0.9 * k, 0])
            q.set_opacity([0.6, 0.42, 0.25][k - 1])
            qs.add(q)
    return plane, dot, zl, wq, arr, el, qs


class Recap(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.wait(8.0)   # end card; the music carries it
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    def clip1(self):
        with self.say("c3.recap.1") as c:
            # r1: mirror pairs, tip to tail onto the real axis
            c.wait_until("r1")
            pic, cap = panel_r1()
            self.play(FadeIn(pic.plane), run_time=0.8)
            c.wait_until("expand")
            g3, p3, d3 = pic.pair3
            self.play(GrowArrow(g3), run_time=0.8)
            self.play(GrowArrow(p3), FadeIn(d3, scale=0.5), run_time=0.8)
            c.wait_until("pair the mirror terms")
            g1, p1, d1 = pic.pair1
            self.play(GrowArrow(g1), GrowArrow(p1), FadeIn(d1, scale=0.5),
                      *appear(*pic.labels, lag=0.2), run_time=1.2)
            c.wait_until("back into cosines")
            self.play(*appear(cap, shift=None), run_time=min(1.0, c.until("r2")))   # no drop: it would brush the grid
            self.p1 = VGroup(pic, cap)
            settle(self, self.p1)

            # r2: the curling chain and its shadow
            c.wait_until("r2")
            pic, cap, plane, chain, shadow = panel_r2(self.p1[1].get_right()[0])
            self.play(*set_alpha([self.p1], DIMMED_P), FadeIn(plane), run_time=0.8)
            self.play(LaggedStart(*[GrowArrow(a) for a in chain], lag_ratio=0.5), run_time=1.6)
            c.wait_until("real part")
            self.play(LaggedStart(*[FadeIn(s) for s in shadow], lag_ratio=0.3), run_time=1.2)
            c.wait_until("geometric progression")
            self.play(*appear(cap), run_time=min(1.0, c.until("r3")))
            self.p2 = VGroup(pic, cap)
            settle(self, self.p2)

            # r3: shift and subtract, and the flag
            c.wait_until("r3")
            pic, flag, row1, row2, st = panel_r3(self.p2[0].get_right()[0])
            self.play(*set_alpha([self.p2], DIMMED_P), *appear(row1, row2, lag=0.3, shift=None), run_time=1.2)
            self.play(LaggedStart(*[Create(s) for s in st], lag_ratio=0.15), run_time=1.0)
            c.wait_until("lambda must")
            self.play(FadeIn(flag, scale=0.9), run_time=min(1.0, c.until("r4")))
            self.p3 = VGroup(pic, flag)
            settle(self, self.p3)

            # r4: the conjugate step makes the bottom real
            c.wait_until("r4")
            pic, cap, B1, B2, line, tag = panel_r4()
            self.play(*set_alpha([self.p3], DIMMED_P), *appear(B1, shift=None), run_time=1.0)
            c.wait_until("the bottom real")
            self.play(*appear(B2, shift=None), run_time=1.0)
            self.play(*appear(line, shift=None), run_time=0.9)
            c.wait_until("read off")
            self.play(*appear(tag), run_time=min(0.8, c.until("r5")))
            self.p4 = VGroup(pic, cap)
            settle(self, self.p4)

            # r5: the chain lies flat, the sum is N
            c.wait_until("r5")
            pic, cap, sc, box = panel_r5()
            self.play(*set_alpha([self.p4], DIMMED_P), FadeIn(box), run_time=1.0)
            c.wait_until("whole number of turns")
            self.play(LaggedStart(*[GrowArrow(a) for a in sc.chain], lag_ratio=0.3), run_time=1.2)
            self.play(*appear(cap, shift=None), run_time=1.0)
            c.wait_until("the sum is N")
            self.play(GrowFromCenter(sc.brace), *appear(sc.label), run_time=min(0.9, c.until(None)))
            self.p5 = VGroup(pic, cap)
            settle(self, self.p5)

    def clip2(self):
        heading = T("Next time", 44, color=DIM).move_to([0, 3.35, 0])
        plane, dot, zl, wq, arr, el, qs = end_card()
        with self.say("c3.recap.2") as c:
            c.wait_until("exponential")
            sweep_clear(self, *appear(heading, shift=None), FadeIn(plane), run_time=1.2)
            self.play(FadeIn(dot, scale=0.5), *appear(zl, wq, lag=0.2), run_time=0.8)
            self.play(GrowArrow(arr), *appear(el), run_time=0.9)
            c.wait_until("log")
            back = Line(dot.get_center() + 0.22 * LEFT, wq.get_right() + 0.25 * RIGHT)
            self.play(VShowPassingFlash(back.set_stroke(YELLOW, 8), time_width=0.5),
                      FlashAround(wq[2], run_time=1.5, time_width=1.5), run_time=1.5)
            c.wait_until("many")
            self.play(*appear(*qs, lag=0.2, shift=None), run_time=min(1.8, c.until(None)))
