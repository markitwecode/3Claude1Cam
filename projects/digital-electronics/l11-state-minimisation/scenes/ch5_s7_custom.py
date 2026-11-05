"""Chapter 5, scene 7: FPGA or custom chip? Clips c5.custom.1 – c5.custom.3.

Shared (s8 recap: load_scene("ch5_s7_custom")):
  cost_plot()  VGroup(axes, xlab, ylab, fpga, fpga_lab, custom, custom_lab, dash, dot) as it stands
               at the end of this scene (centred near (-0.3, -0.3), ~11.5 x 6.2); attributes of
               the same names, plus .left/.right (TEAL/PINK region tints, not in the group) and
               .left_lab/.right_lab ("FPGA", "custom chip" region labels, not in the group).
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

S41 = load_scene("ch4_s1_hook")


def _p(x, y):
    return np.array([x, y, 0.0])


def chip_pkg(label, color, w=3.0, h=1.7, n_pins=6, size=44):
    g = S41.package(label, w=w, h=h, n_pins=n_pins, size=size)
    g.shell.set_color(color)
    if g.lab is not None:
        g.lab.set_color(color)
    return g


def price_tag(s=0.4):
    body = Polygon(_p(-0.5, 0), _p(-0.25, 0.25), _p(0.5, 0.25), _p(0.5, -0.25), _p(-0.25, -0.25))
    body.set_stroke(GOLD, 2).set_fill(GOLD, 0.9)
    hole = Dot(_p(-0.22, 0), radius=0.06, color=BG)
    return VGroup(body, hole).scale(s).rotate(-PI / 8)


def product(x, y):
    box = RoundedRectangle(corner_radius=0.15, width=1.5, height=1.4).set_stroke(BLUE, 3)
    pkg = chip_pkg(None, TEAL, w=0.8, h=0.45, n_pins=3)
    g = VGroup(box, pkg).move_to(_p(x, y))
    g.box, g.pkg = box, pkg
    return g


def mask_and_wafer(c):
    wafer = Circle(radius=1.5).set_stroke(DIM, 3).set_fill(BLUE, 0.15).move_to(c)
    sq = Square(2.0).set_stroke(FG, 3).set_fill(FG, 0.3)
    paths = [
        [(-0.7, 0.6), (-0.1, 0.6), (-0.1, 0.1), (0.6, 0.1)],
        [(-0.7, -0.2), (-0.4, -0.2), (-0.4, -0.65), (0.3, -0.65)],
        [(0.3, 0.7), (0.3, 0.35), (0.7, 0.35)],
        [(0.6, -0.15), (0.6, -0.45)],
    ]
    cut = VGroup(*[VMobject().set_points_as_corners([_p(*q) for q in pth]).set_stroke(BG, 7)
                   for pth in paths])
    pads = VGroup(*[Square(0.16).set_stroke(width=0).set_fill(BG, 1).move_to(_p(*q))
                    for q in [(-0.7, 0.6), (0.6, 0.1), (-0.7, -0.2), (0.3, -0.65), (0.7, 0.35), (0.6, -0.45)]])
    mask = VGroup(sq, cut, pads).move_to(c)
    return wafer, mask


# ---------------------------------------------------------------- the cost plot (shared with s8)
XC = 4.2 / 0.9  # crossing in axis units: 0.3 + 1.2x = 4.5 + 0.3x


def _fpga_y(x):
    return 0.3 + 1.2 * x


def _custom_y(x):
    return 4.5 + 0.3 * x


def cost_plot():
    axes = Axes(x_range=[0, 10, 1], y_range=[0, 10, 1], x_length=8.4, y_length=5.2, tips=True,
                axis_config={"include_ticks": False, "color": DIM, "stroke_width": 3})
    axes.move_to(_p(-0.3, -0.3))
    xlab = T("number made", 32, DIM)
    xlab.next_to(axes.c2p(10, 0), DOWN, buff=0.3).align_to(axes.c2p(10, 0), RIGHT)
    ylab = T("total cost", 32, DIM).next_to(axes.c2p(0, 10), UP, buff=0.25)
    fpga = Line(axes.c2p(0, _fpga_y(0)), axes.c2p(7.4, _fpga_y(7.4))).set_stroke(TEAL, 6)
    fpga_lab = T("FPGA", 36, TEAL).next_to(fpga.get_end(), RIGHT, buff=0.2)
    custom = Line(axes.c2p(0, _custom_y(0)), axes.c2p(10, _custom_y(10))).set_stroke(PINK, 6)
    custom_lab = T("custom chip", 36, PINK).next_to(custom.get_end(), RIGHT, buff=0.2)
    cpt = axes.c2p(XC, _fpga_y(XC))
    dot = Dot(cpt, radius=0.12, color=YELLOW).set_z_index(2)
    dash = DashedLine(cpt, axes.c2p(XC, 0), dash_length=0.12).set_stroke(YELLOW, 3)
    g = VGroup(axes, xlab, ylab, fpga, fpga_lab, custom, custom_lab, dash, dot)
    g.axes, g.xlab, g.ylab, g.fpga, g.fpga_lab = axes, xlab, ylab, fpga, fpga_lab
    g.custom, g.custom_lab, g.dash, g.dot = custom, custom_lab, dash, dot
    lo, hi = axes.c2p(0, 0), axes.c2p(XC, 10)
    left = Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1]).set_stroke(width=0).set_fill(TEAL, 0.14)
    left.move_to((lo + hi) / 2).set_z_index(-1)
    lo2, hi2 = axes.c2p(XC, 0), axes.c2p(10, 10)
    right = Rectangle(width=hi2[0] - lo2[0], height=hi2[1] - lo2[1]).set_stroke(width=0).set_fill(PINK, 0.14)
    right.move_to((lo2 + hi2) / 2).set_z_index(-1)
    left_lab = T("FPGA", 40, TEAL).move_to(axes.c2p(XC * 0.64, 1.1))
    right_lab = T("custom chip", 40, PINK).move_to(axes.c2p((XC + 10) / 2, 1.1))
    g.left, g.right, g.left_lab, g.right_lab = left, right, left_lab, right_lab
    return g


def spread_from(region, edge):
    """Region tint grows sideways out of `edge` at its full height (no vertical scaling)."""
    region.save_state()
    region.stretch(0.002, 0, about_edge=edge)
    return Restore(region)


class FpgaOrCustom(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.clip3()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # -- clip 1: prototypes and small runs ---------------------------------------------
    def clip1(self):
        with self.say("c5.custom.1") as c:
            chip = chip_pkg("FPGA", TEAL, w=3.8, h=2.1, n_pins=7, size=52).move_to(_p(-1.0, 0.1))
            self.play(*appear(chip, shift=None), run_time=1.0)
            c.wait_until("proto")

            board = RoundedRectangle(corner_radius=0.2, width=5.6, height=3.6)
            board.set_stroke(GREEN, 3).set_fill(GREEN, 0.08).move_to(chip).set_z_index(-1)
            proto = T("prototype", 34, GREEN).next_to(board, DOWN, buff=0.3)
            self.play(FadeIn(board), run_time=0.8)
            c.wait_until(own_word=proto)
            self.play(*appear(proto), run_time=1.0)
            c.wait_until("if it fails")

            sx = 4.0
            cross = cross_mark().scale(2.0).move_to(_p(sx, 0.3))
            no_lab = T("doesn't work", 32, RED).next_to(cross, DOWN, buff=0.35)
            self.play(*appear(cross, no_lab, shift=None, lag=0.3), run_time=1.0)
            c.wait_until("you just reprogram")

            arc = Arc(radius=0.55, start_angle=PI / 2, angle=-1.7 * PI).set_stroke(GOLD, 6)
            arc.add_tip(tip_length=0.25, tip_width=0.25)
            arc.move_to(_p(sx, 0.3))
            rep_lab = T("reprogram", 32, GOLD).next_to(arc, DOWN, buff=0.35)
            self.play(*swap(VGroup(cross, no_lab), VGroup(arc, rep_lab)), run_time=1.0)
            stream = Line(_p(sx - 0.75, 0.1), chip.body.get_right() + 0.05 * RIGHT)
            self.play(*[time_span(VShowPassingFlash(stream.copy().set_stroke(GOLD, 8), time_width=0.4),
                                  0.3 * k, 0.3 * k + 0.8) for k in range(3)], run_time=1.4)
            c.wait_until("until it works")

            tick = check_mark().scale(2.2).move_to(_p(sx, 0.3))
            self.play(*swap(arc, tick), run_time=min(1.0, c.until("few", floor=0.5)))
            c.wait_until("few")

            # shrink the prototype to the left; a few products appear beside it
            bg = VGroup(board, chip)
            self.play(*disappear(tick, rep_lab),
                      bg.animate.scale(0.6).move_to(_p(-4.4, 0.3)),
                      proto.animate.move_to(_p(-4.4, -1.3)), run_time=1.0)
            self.prods = [product(x, 0.4) for x in (-1.6, 0.4, 2.4)]
            self.play(*appear(*self.prods, lag=0.3), run_time=min(1.4, c.until(floor=0.6)))
            self.board, self.chip, self.proto = board, chip, proto

    # -- clip 2: millions, the custom chip, masks ---------------------------------------
    def clip2(self):
        with self.say("c5.custom.2") as c:
            bg = VGroup(self.board, self.chip)
            more = [product(x, 0.4) for x in (4.4, 6.4, 8.4)]
            left = [product(x, 0.4) for x in (-3.6, -5.6, -7.6)]
            self.play(*during(disappear(bg, self.proto), 0, 0.45),
                      *during(appear(*more, *left, shift=None, lag=0.12), 0.35, 1), run_time=1.4)
            prods = self.prods + more + left
            mil = T("millions", 48, YELLOW).move_to(_p(0, 2.2))
            self.play(*appear(mil), run_time=1.0)
            tags = [price_tag(0.42).move_to(p.box.get_corner(UR) + _p(-0.1, -0.1)) for p in prods]
            self.play(*appear(*tags, shift=None, lag=0.08), run_time=1.0)
            c.wait_until("asic")

            cust = chip_pkg("custom chip", PINK, w=3.4, h=2.0, n_pins=7, size=40).move_to(_p(-4.0, 0.6))
            sweep_clear(self, FadeIn(cust), run_time=1.4)
            asic = T("ASIC: application-specific integrated circuit", 36, t2c={"ASIC": PINK})
            asic.move_to(_p(0, 3.1))
            c.wait_until(own_word=asic)
            self.play(*appear(asic), run_time=1.0)
            c.wait_until("masks")

            wafer, mask = mask_and_wafer(_p(1.3, 0.6))
            self.play(FadeIn(wafer), run_time=1.0)
            self.play(FadeIn(mask, shift=0.6 * DOWN), run_time=min(1.5, c.until("stencils", floor=0.8)))
            up = T("up-front cost:\ndesign + masks", 38, GOLD, line_spacing=0.9).move_to(_p(4.9, 0.6))
            c.wait_until("print")
            self.play(*appear(up), run_time=1.0)  # early: tag sums up the sentence, read as it lands
            c.wait_until("cheap")

            copies = [chip_pkg(None, PINK, w=1.0, h=0.55, n_pins=4).move_to(_p(x, -2.6))
                      for x in np.linspace(-5.6, 5.6, 8)]
            # each chip arrives already wearing its price tag, so every chip in the row has one
            ctags = [price_tag(0.26).move_to(cp.body.get_corner(UR) + _p(0.05, 0.05)) for cp in copies]
            tagged = [VGroup(cp, tg) for cp, tg in zip(copies, ctags)]
            self.play(LaggedStart(*[FadeIn(g, target_position=wafer.get_center(), scale=0.4)
                                    for g in tagged], lag_ratio=0.12),
                      run_time=min(1.8, c.until(floor=0.8)))

    # -- clip 3: the cost plot ---------------------------------------------------------
    def clip3(self):
        with self.say("c5.custom.3") as c:
            P = cost_plot()
            sweep_clear(self, FadeIn(P.axes), FadeIn(P.xlab), FadeIn(P.ylab),
                        run_time=min(2.2, c.until("fpga")))
            c.wait_until("fpga")

            self.play(Create(P.fpga), run_time=2.0, rate_func=linear)
            self.play(*appear(P.fpga_lab, shift=None), run_time=0.8)
            c.wait_until("custom")

            self.play(Create(P.custom), run_time=2.0, rate_func=linear)
            self.play(*appear(P.custom_lab, shift=None), run_time=0.8)
            c.wait_until("cross")

            self.play(GrowFromCenter(P.dot), run_time=0.8)
            self.play(Create(P.dash), FlashAround(P.dot, run_time=1.2, time_width=1.5), run_time=1.2)
            c.wait_until("left")

            self.play(spread_from(P.left, RIGHT), run_time=1.2)   # full height, spreads left from the dashed line
            self.play(*appear(P.left_lab), run_time=1.0)
            c.wait_until("right")

            self.play(spread_from(P.right, LEFT), run_time=1.2)   # full height, spreads right from the dashed line
            self.play(*appear(P.right_lab), run_time=1.0)
            c.wait_until("tradeoff")
            self.play(FlashAround(P.dash, run_time=1.2, time_width=1.5, color=YELLOW))
            c.wait_until("trade-off")
            cap = T("volume vs cost", 48, YELLOW).move_to(_p(0, 3.35))
            self.play(*appear(cap), run_time=1.0)
        self.wait(2.0)
