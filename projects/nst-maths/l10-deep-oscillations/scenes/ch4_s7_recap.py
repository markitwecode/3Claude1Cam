"""Chapter 4, scene 7: recap (the part's three moves, then all four parts, then next). Clips c4.recap.1 – c4.recap.2.

Layout: three rows (r1 start, r2 events, r3 toolkit), each a small moving picture on the left and its
move card + line in a text column on the right; then four moving thumbnails (one per part); then
the circuit and "Next: the impedance video", held ~8 s as the end card (the pilot's last scene).
Every picture comes from its scene's export (start_picture, events_picture, the s6 panels,
circuit_small, ch1's spring drawing, the arrow kit), scaled down here; nothing is redrawn.
"""
# style: 2
import math
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
spr = load_scene("ch1_s3_spring")
hook = load_scene("ch4_s1_hook")
s2 = load_scene("ch4_s2_start")
s5 = load_scene("ch4_s5_events")
s6 = load_scene("ch4_s6_toolkit")

# ── layout ───────────────────────────────────────────────────────────────────────
ROW_Y = (1.95, -0.3, -2.55)       # row centres
PX = -4.45                        # picture centre x
TX = -1.3                         # text column left edge
LINE_SIZE = 34
FR_X = (-4.95, -1.65, 1.65, 4.95)  # thumbnail centres
FR_W, FR_H, FR_Y = 3.1, 2.6, 1.25
FORM_Y = 0.3                      # formulas inside the frames
CAP_Y = -0.42                     # captions under the frames
PIC_Y = 1.55                      # picture centres inside the frames


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


def clock(rate=0.0):
    """A tracker that advances by rate·dt every frame (set .rate to start or stop it)."""
    t = ValueTracker(0.0)
    t.rate = rate
    t.add_updater(lambda m, dt: m.increment_value(m.rate * dt))
    return t


def faded(build, op):
    """always_redraw of build() at opacity op (a tracker: fade a redrawn picture in or dim it)."""
    return always_redraw(lambda: s6._fade(build(), _v(op)))


def mini(build, k, src, dst, op=1.0):
    """always_redraw of build(), scaled by k about src and moved so src lands on dst."""
    src, dst = np.array(src, dtype=float), np.array(dst, dtype=float)

    def b():
        m = build()
        m.scale(k, about_point=src)
        m.shift(dst - src)
        return m
    return faded(b, op)


def freeze(*mobs):
    for m in mobs:
        for f in m.get_family():
            f.clear_updaters()


# ── r1 / p4: s2's frozen arrow, small ────────────────────────────────────────────
def start_mini(v0, k, dst, weight=True, push=True, op=1.0):
    """s2's start_picture (plane, legs, GOLD A, push arrow, weight) at scale k, with leg labels."""
    O = s2.O
    dst = np.array(dst, dtype=float)
    plane = s2.amp_plane(labels=False).scale(k, about_point=O).shift(dst - O)

    def build():
        p = s2.start_picture(_v(v0), weight=weight)
        if not push:
            p.remove(p.push)
        return p
    pic = mini(build, k, O, dst, op)
    u = s2.U * k
    xl = MathTex("x_0", font_size=26, color=BLUE)
    if weight:
        xl.move_to(dst + np.array([1.5 * u - 0.05, 0.27, 0]))
    else:
        xl.move_to(dst + np.array([1.5 * u, 0.2, 0]))
    vl = MathTex(r"-v_0/\omega", font_size=26, color=PINK)
    set_backstroke(vl)

    def place(m):
        b = -_v(v0) / 3.0
        m.next_to(dst + np.array([3 * u, 0.5 * b * u, 0]), RIGHT, buff=0.1)
    place(vl)
    vl.add_updater(place)
    g = VGroup(plane, pic, xl, vl)
    g.plane, g.pic, g.xl, g.vl = plane, pic, xl, vl
    return g


# ── r2: s5's events picture, with its flags glowing as the arrow reaches them ────
def glow_flags(pic, t):
    angles = (PI / 2, -PI / 2, 0.0, PI)
    for (dot_lab, ang) in zip(pic.flags, angles):
        dot = dot_lab[0]
        p = dot.get_center()
        col = dot.get_color()

        def up(m, p=p, col=col, ang=ang):
            a = 3 * _v(t) - s5.DELTA
            g = max(0.0, math.cos(a - ang)) ** 60
            m.become(Dot(p, radius=0.06 * (1 + 1.4 * g),
                         color=interpolate_color(ManimColor(col), ManimColor(WHITE), 0.6 * g)))
        dot.add_updater(up)


# ── p1: ch1's spring with its RED pull ───────────────────────────────────────────
def spring_mini(t, dst, op, k=0.4):
    src = np.array([-3.05, spr.SPRING_Y + 0.55, 0])

    def build():
        x = 2.5 * math.cos(2 * _v(t))
        return VGroup(spr.spring_drawing(x, zero=False), spr.pull_arrow(x))
    return mini(build, k, src, dst, op)


# ── p2: ch2's turning arrow, shadow, weight on its line ──────────────────────────
def arrow_mini(t, o, op, scale=0.42):
    def build():
        tv = _v(t)
        return VGroup(ak.spring_on_axis(tv, scale=scale, origin=o),
                      ak.turning_arrow(tv, scale=scale, origin=o, width=4),
                      ak.shadow(tv, scale=scale, origin=o))
    return faded(lambda: VGroup(ak.plane(scale, o, re_units=1.5, im_units=1.2, labels=False),
                                build()), op)


# ── p3: the turning arrow freezing into A (arrow kit: ride along with it) ───────
def freeze_mini(a, pa, o, op, scale=0.42):
    """a: the arrow's angle, pa: the plane's angle (both trackers). Riding along = pa turns back."""
    o = np.array(o, dtype=float)

    def bplane():
        pl = ak.plane(scale, o, re_units=1.2, im_units=1.2, labels=False)
        pl.grid.set_stroke(opacity=0)
        return pl.rotate(_v(pa), about_point=o)
    pl = faded(bplane, op)
    ar = faded(lambda: ak.arrow_between(
        o, o + ak.PLANE_R * scale * np.array([math.cos(_v(a)), math.sin(_v(a)), 0]), GOLD, 4), op)
    return VGroup(pl, ar)


def caption(k, words):
    g = VGroup(T(f"Part {k}", size=26, color=DIM), T(words, size=30, color=FG)).arrange(DOWN, buff=0.12)
    return g.move_to([FR_X[k - 1], CAP_Y - 0.12, 0])


class Recap(NarratedScene):
    def construct(self):
        self.clip_recap()
        self.clip_pilot()
        self.wait(8.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.15)

    # ── c4.recap.1: the part's three moves ──────────────────────────────────────
    def clip_recap(self):
        self.pin = hook.amp_pin()
        title = T("Recap", size=30, color=DIM).move_to(kit.TAG_TL, aligned_edge=UL)
        self.title = title

        # r1
        v0 = ValueTracker(12.0)
        r1 = start_mini(v0, 0.5, [-4.83, ROW_Y[0], 0])
        card1 = kit.move_card(s2.MOVE_M10, small=True).scale(1.1)
        card1.move_to([TX, ROW_Y[0] + 0.9, 0], aligned_edge=UL)
        line1 = MathTex(r"\text{set }", "t = 0", r":\quad ", "A", "=", "x_0", r"-\,i\,v_0/\omega",
                        font_size=LINE_SIZE)
        line1[3].set_color(GOLD)
        line1[5].set_color(BLUE)
        line1[6].set_color(PINK)
        line1.next_to(card1, DOWN, buff=0.22, aligned_edge=LEFT)

        # r2
        t2 = clock()
        t2.set_value(s5.T_TOP)
        self.add(t2)
        r2 = s5.events_picture(t2, scale=0.68, center=[-5.3, ROW_Y[1], 0])
        left = r2.flags[3]
        left[1].next_to(left[0], UR, buff=0.06)
        card2 = kit.move_card(s5.MOVE_M11, small=True).scale(1.1)
        card2.move_to([TX, ROW_Y[1] + 0.9, 0], aligned_edge=UL)
        l2a = T("vertical → passing the centre", size=30, t2c={"centre": YELLOW})
        l2s = T("·", size=30, color=DIM)
        l2b = T("flat → still", size=30)
        line2 = VGroup(l2a, l2s, l2b).arrange(RIGHT, buff=0.25)
        l2b.align_to(l2a[0], DOWN)                       # same baseline ("passing" has a descender)
        l2s.set_y(l2a[0].get_y())
        line2.next_to(card2, DOWN, buff=0.22, aligned_edge=LEFT)

        # r3
        t3 = clock()
        gap = ValueTracker(1.0)
        self.add(t3)
        xs = (-5.83, -4.13, -2.43)
        p_com = s6.panel_commute(t3, scale=0.34, origin=[xs[0], ROW_Y[2], 0])
        p_qua = s6.panel_quarter(t3, scale=0.34, origin=[xs[1], ROW_Y[2], 0], label=False)
        p_can = s6.panel_cancel(t3, gap, scale=0.34, origin=[xs[2], ROW_Y[2], 0])
        panels = (p_com, p_qua, p_can)
        l3a = MathTex(r"\text{frozen arrows}", font_size=LINE_SIZE)
        l3b = MathTex(r"\times\,", "i", r"\omega", r"\text{ differentiates}", font_size=LINE_SIZE)
        l3b[0].set_color(GREEN)
        l3b[1].set_color(PINK)
        l3b[2].set_color(GREEN)
        l3c = MathTex(r"\text{equal shadows}", r"\;\Rightarrow\;", r"\text{equal arrows}",
                      font_size=LINE_SIZE)
        l3c[2].set_color(GOLD)
        l3a.set_color(GOLD)
        line3 = VGroup(l3a, l3b, l3c).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        line3.move_to([TX, ROW_Y[2], 0], aligned_edge=LEFT)

        with self.say("c4.recap.1", gap=2.5) as c:
            self.play(*appear(title, shift=None), FadeIn(self.pin), run_time=1.2)  # early: the recap's heading and the chapter pin
            c.wait_until("r1")
            self.play(FadeIn(r1.plane), FadeIn(r1.pic), run_time=1.2)
            self.play(*appear(r1.xl, r1.vl, lag=0.3), run_time=0.9)
            c.wait_until("set")
            self.play(FadeIn(card1, shift=0.15 * DOWN), run_time=1.0)
            c.wait_until("The real part")
            self.play(*appear(line1), run_time=1.0)
            c.wait_until("where it starts")
            self.play(FlashAround(r1.xl, color=BLUE, time_width=1.5),
                      FlashAround(line1[5], color=BLUE, time_width=1.5), run_time=1.2)
            c.wait_until("how fast")
            self.play(v0.animate.set_value(18.0), run_time=1.6)
            self.play(v0.animate.set_value(-9.0), run_time=2.0)
            self.play(v0.animate.set_value(12.0), run_time=min(1.4, max(0.5, c.until("r2") - 0.1)))

            c.wait_until("r2")
            self.play(*set_alpha([card1, line1], 0.45), FadeIn(r2), run_time=1.2)  # early: s5's picture, its four event tags part of it
            t2.rate = 0.45
            glow_flags(r2, t2)
            c.wait_until("To time events")
            self.play(FadeIn(card2, shift=0.15 * DOWN), run_time=1.0)  # early: the move card, stated whole as the move is named
            c.wait_until("Straight up")
            self.play(*appear(l2a), run_time=1.0)
            c.wait_until("lying flat")
            self.play(*appear(l2s, l2b, lag=0.2), run_time=1.0)

            c.wait_until("r3")
            for p in panels:
                p.op.set_value(0.0)
                self.add(p.dynamic)
            self.play(*set_alpha([card2, line2], 0.45),
                      *[a for p in panels for a in s6.show(p)], run_time=1.2)
            t3.rate = 1.0
            t2.rate = 0.0
            c.wait_until("frozen arrows")
            self.play(*appear(l3a), run_time=0.9)
            c.wait_until("eye omega")
            self.play(*appear(l3b), FlashAround(p_qua.static, color=GREEN, time_width=1.5),
                      run_time=1.2)
            c.wait_until("equal shadows")
            self.play(*appear(l3c), gap.animate.set_value(0.0),
                      run_time=min(2.0, max(0.6, c.until() - 0.1)))

        self.rows = [VGroup(r1, card1, line1), VGroup(r2, card2, line2),
                     VGroup(*panels, line3)]
        self.trackers = (t2, t3)

    # ── c4.recap.2: the four parts, then next ───────────────────────────────────
    def clip_pilot(self):
        for t in self.trackers:
            t.rate = 0.0
        frames = [RoundedRectangle(corner_radius=0.15, width=FR_W, height=FR_H)
                  .set_stroke(DIM, 2).move_to([x, FR_Y, 0]) for x in FR_X]
        caps = [caption(1, "the rule"), caption(2, "the arrow"), caption(3, "the amplitude"),
                caption(4, "the start")]

        tk = clock()
        self.add(tk)
        ops = [ValueTracker(0.0) for _ in range(4)]
        p1 = spring_mini(tk, [FR_X[0], PIC_Y + 0.1, 0], ops[0])
        f1 = spr.rule_boxed().scale(0.9).move_to([FR_X[0], FORM_Y + 0.15, 0])
        o2 = np.array([FR_X[1] + 0.02, PIC_Y - 0.05, 0])
        p2 = arrow_mini(tk, o2, ops[1], scale=0.4)
        a3, pa3, fz = ValueTracker(0.4), ValueTracker(0.0), ValueTracker(0.0)
        a3.add_updater(lambda m, dt: m.increment_value(1.1 * (1 - fz.get_value()) * dt))
        pa3.add_updater(lambda m, dt: m.increment_value(-1.1 * fz.get_value() * dt))
        o3 = np.array([FR_X[2], PIC_Y, 0])
        p3 = freeze_mini(a3, pa3, o3, ops[2], scale=0.5)
        f3 = MathTex("x", "=", r"\mathrm{Re}", r"\left[", "A", r"\,e^{i\omega t}", r"\right]",
                     font_size=30)
        for i, col in ((0, BLUE), (2, BLUE), (4, GOLD), (5, GOLD)):
            f3[i].set_color(col)
        f3.move_to([FR_X[2], FORM_Y, 0])
        alab = MathTex("A", font_size=30, color=GOLD)
        set_backstroke(alab)
        v4 = ValueTracker(12.0)
        p4 = start_mini(v4, 0.42, [FR_X[3] - 0.4, PIC_Y - 0.05, 0], weight=False, push=False, op=ops[3])

        with self.say("c4.recap.2") as c:
            for r in self.rows:
                freeze(r)
            self.remove(*self.trackers)
            self.wait(min(1.2, c.until("p1") - 2.8))
            self.play(*[a for i, r in enumerate(self.rows) for a in during([FadeOut(r, scale=0.5)], 0.08 * i, 0.4 + 0.08 * i)], *during(disappear(self.title), 0, 0.4), *during([FadeIn(f) for f in frames], 0.5, 0.85), *during(appear(*caps, lag=0.15), 0.55, 1.0), run_time=2.4)  # early: the four parts shown whole, then walked

            c.wait_until("p1")
            self.add(p1)
            self.play(ops[0].animate.set_value(1.0), FadeIn(f1), run_time=1.2)
            tk.rate = 0.6
            c.wait_until("p2")
            self.add(p2)
            self.play(ops[1].animate.set_value(1.0), run_time=1.2)
            c.wait_until("p3")
            self.add(a3, pa3)
            self.add(p3)
            self.play(ops[2].animate.set_value(1.0), FadeIn(f3), run_time=0.9)
            self.play(fz.animate.set_value(1.0), run_time=min(1.0, max(0.4, c.until("p4") - 0.3)))
            tip = o3 + ak.PLANE_R * 0.5 * np.array([math.cos(a3.get_value()), math.sin(a3.get_value()), 0])
            alab.move_to(tip + 0.25 * np.array([math.cos(a3.get_value()), math.sin(a3.get_value()), 0]))
            c.wait_until("p4")
            self.add(p4.pic)
            self.play(FadeIn(alab), FadeIn(p4.plane), ops[3].animate.set_value(1.0),
                      *appear(p4.xl, p4.vl, shift=None), run_time=1.0)
            self.play(v4.animate.set_value(-9.0), run_time=min(2.0, max(0.5, c.until("next") - 0.1)))

            c.wait_until("next")
            tk.rate = 0.0
            fz.set_value(1.0)
            self.remove(a3, pa3)
            circ = s6.circuit_small(scale=0.7).move_to([-2.9, -2.3, 0])
            for lab in circ.labels:
                arr = lab[1]
                if lab is not circ.labels[3]:            # V_C's arrow sits by the capacitor already
                    arr.shift(0.24 * RIGHT)              # room to turn without sweeping its label
                arr.add_updater(lambda m, dt: m.rotate(1.3 * dt, about_point=m.get_start()))
            nxt = T("Next: the impedance video", size=34, color=FG).next_to(circ, RIGHT, buff=0.8)
            self.play(*[o.animate.set_value(0.4) for o in ops],
                      *set_alpha([*frames, *caps, f1, f3, alab, p4.plane, p4.xl, p4.vl], 0.4),
                      FadeIn(circ), run_time=1.2)
            c.wait_until(own_word=nxt)
            self.play(*appear(nxt), run_time=1.0)
