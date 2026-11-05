"""Chapter 3, scene 2: why the D type won over J-K and T. Clips c3.family.1 – c3.family.2."""
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
from lib.style import *  # noqa: E402,F403

SEPIA = "#C8A47E"

# ---- ch2's flip-flop symbol (ch2_s6_symbols.make_ff / ch2_s7_recap.make_ff(ins=...)) ----------
BOX_W, BOX_H = 1.5, 2.6
PIN_Y = 0.6
WIRE = 0.85
EN_WIRE = 1.0


def _p(x, y):
    return np.array([x, y, 0.0])


def qbar(size=36, color=GREEN):
    q = T("Q", size, color)
    bar = Line(LEFT, RIGHT).set_stroke(color, 3).set_width(q.width * 1.05)
    bar.next_to(q, UP, buff=0.07)
    return VGroup(q, bar)


def make_ff(ins=(("D", PIN_Y),)):
    hb = BOX_H / 2
    box = Rectangle(width=BOX_W, height=BOX_H).set_stroke(FG, 4)
    q_w = Line([BOX_W / 2, PIN_Y, 0], [BOX_W / 2 + WIRE, PIN_Y, 0]).set_stroke(GREEN, 5)
    qb_w = Line([BOX_W / 2, -PIN_Y, 0], [BOX_W / 2 + WIRE, -PIN_Y, 0]).set_stroke(GREEN, 5)
    tri = Polygon(_p(-0.17, -hb), _p(0.17, -hb), _p(0, -hb + 0.26)).set_stroke(FG, 3).set_fill(BG, 1)
    clk_w = Line(_p(0, -hb - EN_WIRE), _p(0, -hb - 0.02)).set_stroke(YELLOW, 5)
    in_w = [Line([-BOX_W / 2 - WIRE, y, 0], [-BOX_W / 2, y, 0]).set_stroke(BLUE, 5) for _, y in ins]
    in_l = [T(s, 36, BLUE).move_to([-BOX_W / 2 + 0.3, y, 0]) for s, y in ins]
    q_l = T("Q", 36, GREEN).move_to([BOX_W / 2 - 0.3, PIN_Y, 0])
    qb_l = qbar().move_to([BOX_W / 2 - 0.3, -PIN_Y + 0.05, 0])
    g = VGroup(*in_w, q_w, qb_w, clk_w, box, tri, *in_l, q_l, qb_l)
    g.box, g.tri, g.clk_w, g.in_l = box, tri, clk_w, in_l
    return g


def place(g, scale, box_center):
    g.scale(scale)
    g.shift(_p(*box_center) - g.box.get_center())
    return g


# ---- layout ---------------------------------------------------------------------------------
SC = 0.85
ROW_Y = 0.9
XD, XJK, XT = -4.5, 0.0, 4.5
HALF_W = (BOX_W / 2 + WIRE) * SC          # symbol half width incl. wires
BAR_Y = -1.5
CHIP_Y = -2.85


def mini_d():
    box = Rectangle(width=0.3, height=0.4).set_stroke(FG, 2)
    tri = Polygon(_p(-0.06, -0.2), _p(0.06, -0.2), _p(0, -0.11)).set_stroke(FG, 1.5)
    d = Line(_p(-0.3, 0.08), _p(-0.15, 0.08)).set_stroke(BLUE, 2.5)
    q = Line(_p(0.15, 0.08), _p(0.3, 0.08)).set_stroke(GREEN, 2.5)
    c = Line(_p(0, -0.32), _p(0, -0.2)).set_stroke(YELLOW, 2.5)
    return VGroup(d, q, c, box, tri)


def chip(name, center):
    body = RoundedRectangle(corner_radius=0.12, width=3.6, height=1.25).set_stroke(DIM, 3)
    pins = VGroup(*[Line(_p(x, 0.625), _p(x, 0.74)) for x in np.linspace(-1.5, 1.5, 11)],
                  *[Line(_p(x, -0.625), _p(x, -0.74)) for x in np.linspace(-1.5, 1.5, 11)])
    pins.set_stroke(DIM, 3)
    lab = T(name, 30, FG).move_to(_p(-1.1, 0))
    minis = [mini_d().move_to(_p(0.2 + 0.6 * i, 0.27 - 0.55 * j)) for j in range(2) for i in range(3)]
    shell = VGroup(body, pins).shift(_p(*center))
    lab.shift(_p(*center))
    for m in minis:
        m.shift(_p(*center))
    return shell, lab, minis


def jk_sketch(center):
    cx, cy = center
    pts = [_p(cx + 1.75 * np.cos(a), cy - 0.1 + 1.35 * np.sin(a)) for a in (PI / 2, PI / 2 + 2 * PI / 3,
                                                                       PI / 2 + 4 * PI / 3)]
    circles = [Circle(radius=0.36).set_stroke(PURPLE, 4, opacity=0.6).set_fill(opacity=0).move_to(p)
               for p in pts]
    arrows = []
    for i in range(3):
        a, b = pts[i], pts[(i + 1) % 3]
        u = (b - a) / np.linalg.norm(b - a)
        arrows.append(CurvedArrow(a + 0.4 * u, b - 0.4 * u, angle=-PI / 5, color=PURPLE,
                                  stroke_width=3, tip_length=0.15))
    g = VGroup(*circles, *arrows)
    for ar in arrows:
        ar.set_stroke(PURPLE, 3, opacity=0.6).set_fill(opacity=0)
        ar.tip.set_fill(PURPLE, 0.6).set_stroke(width=0)
    g.set_z_index(-2)
    return g


def glow(scene, label, color=BLUE, peak=0.4, grow=1.3):
    """A soft disc behind an input label that swells and fades (no line near the letter: a bar
    above a letter reads as a complement here), plus a swell of the label itself."""
    disc = Circle(radius=0.75 * max(label.width, label.height) + 0.12).set_stroke(width=0)
    disc.set_fill(color, 0).move_to(label).set_z_index(-1)
    scene.add(disc)
    return [UpdateFromAlphaFunc(disc, lambda m, a: m.set_fill(color, peak * there_and_back(a))),
            label.animate(rate_func=there_and_back).scale(grow)], disc


def pulse(box, color=YELLOW, width=8):
    """The box's own outline brightens and returns: no extra frame around it."""
    return box.animate(rate_func=there_and_back).set_stroke(color, width)


class Family(NarratedScene):
    def construct(self):
        self.clip1()
        self.clip2()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    # ------------------------------------------------------------------ c3.family.1
    def clip1(self):
        with self.say("c3.family.1") as c:
            # {dtype}: the D flip-flop from part two, big, then its D label glows
            d = place(make_ff(), 1.15, (0, 0.4))
            self.play(*appear(d, shift=None), run_time=1.0)
            d_l = d.in_l[0]
            anims, disc = glow(self, d_l)
            self.play(*anims, run_time=1.8)
            self.remove(disc)

            # {three}: two other kinds join it; the heading
            c.wait_until("three")
            jk = place(make_ff(ins=(("J", PIN_Y), ("K", -PIN_Y))), SC, (XJK, ROW_Y))
            tf = place(make_ff(ins=(("T", PIN_Y),)), SC, (XT, ROW_Y))
            d.generate_target()
            place(d.target, SC / 1.15, (XD, ROW_Y))
            head = T("Other Types of Flip-Flops", 48, BLUE).move_to(_p(0, 3.25))
            self.play(*during([MoveToTarget(d)], 0, 0.5),
                      *during(appear(jk, tf, head, shift=None, lag=0.3), 0.4, 1),
                      run_time=2.2)
            self.d, self.jk, self.tf, self.head = d, jk, tf, head

            hist = T("historically important", 30, SEPIA, slant=ITALIC)
            hist.move_to(_p((XJK + XT) / 2, 2.5))
            # the heading sits at 3.45, boxes top ~2.0: the tag goes in between
            self.play(*appear(hist), run_time=1.0)
            self.hist = hist

            # {jk}: state machines, sketched faintly behind the J-K for a moment
            c.wait_until("jk")
            sk = jk_sketch((XJK, ROW_Y))
            self.play(FadeIn(sk), run_time=1.2)
            c.wait_until("t")
            # {t}: the T, a close relative, brightens briefly
            anims, disc = glow(self, tf.in_l[0], peak=0.3, grow=1.2)
            self.play(FadeOut(sk), pulse(tf.box), *anims, run_time=1.6)
            self.remove(disc)

            # {complex}: complexity to build, D short, J-K much longer
            c.wait_until("complex")
            x0d, x0j = XD - HALF_W, XJK - HALF_W
            bar_d = Rectangle(width=0.8, height=0.24).set_stroke(width=0).set_fill(GOLD, 1)
            bar_d.move_to(_p(x0d + 0.4, BAR_Y))
            bar_j = Rectangle(width=3.4, height=0.24).set_stroke(width=0).set_fill(GOLD, 1)
            bar_j.move_to(_p(x0j + 1.7, BAR_Y))
            blab = T("complexity to build", 30, GOLD).next_to(bar_d, DOWN, buff=0.2).align_to(bar_d, LEFT)
            self.play(GrowFromEdge(bar_d, LEFT), run_time=1.0)
            c.wait_until("lot more complex")
            self.play(GrowFromEdge(bar_j, LEFT), *appear(blab), run_time=2.0)
            self.bars = [bar_d, bar_j, blab]

            # {modern}: J-K and T fall out of favour; FPGA and VLSI chips are full of D types
            c.wait_until("modern")
            fpga, fpga_l, fpga_m = chip("FPGA", (-0.1, CHIP_Y))
            vlsi, vlsi_l, vlsi_m = chip("VLSI", (3.9, CHIP_Y))
            self.play(*set_alpha([jk, tf], 0.4), FadeIn(fpga), FadeIn(vlsi), run_time=1.2)
            self.play(*appear(fpga_l, vlsi_l, shift=None, lag=0.4), run_time=1.0)  # early: both chips named in this sentence
            self.play(*[FadeIn(m, scale=0.6) for m in fpga_m + vlsi_m], lag_ratio=0.1, run_time=1.6)
            self.chips = [fpga, fpga_l, *fpga_m, vlsi, vlsi_l, *vlsi_m]

    # ------------------------------------------------------------------ c3.family.2
    def clip2(self):
        d, jk, tf = self.d, self.jk, self.tf
        with self.say("c3.family.2", gap=2.3) as c:
            # {course}: the slide's line takes the bottom; a tick by the D
            course = VGroup(T("Consequently we will only consider synchronous", 32),
                            T("circuit design using D-type FFs", 32, t2c={"D-type FFs": BLUE}))
            course.arrange(DOWN, buff=0.18).move_to(_p(0, -2.65))
            self.play(*during([FadeOut(m) for m in self.bars + self.chips], 0, 0.45),
                      *during(appear(course, shift=None), 0.5, 1), run_time=1.8)
            tick = check_mark(GREEN).scale(1.3).move_to(_p(XD, 2.55))
            self.play(FadeIn(tick, scale=0.6), pulse(d.box, GREEN), run_time=1.2)

            # {complete}: J-K and T still get a brief look
            c.wait_until("for completeness")
            comp = T("for completeness", 30, DIM, slant=ITALIC).move_to(_p((XJK + XT) / 2, BAR_Y))
            self.play(*appear(comp), run_time=1.0)

            # {later}: both come back
            c.wait_until("later")
            self.play(*set_alpha([jk, tf], 1), *disappear(self.hist), run_time=1.4)

            # {ripple}: forward tag from the T
            c.wait_until("ripple")
            rip = T("Part 4: ripple counter", 28, YELLOW).move_to(_p(XT, 2.5))
            self.play(*appear(rip), pulse(tf.box), run_time=1.4)

            # {excite}: forward tag from the J-K
            c.wait_until("excite")
            exc = T("Part 5: excitation table", 28, YELLOW).move_to(_p(XJK - 0.2, 2.5))
            self.play(*appear(exc), pulse(jk.box), run_time=1.4)
