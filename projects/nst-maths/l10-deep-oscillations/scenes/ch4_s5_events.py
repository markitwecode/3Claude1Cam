"""Chapter 4, scene 5: F19, where the arrow points (hint 2, M11, T4.4, the solution, the sweep). Clips c4.events.1 – c4.events.5.

Opens on ch4_s4_f19's handover shot. Exports (load_scene("ch4_s5_events")), for the recap (s7):
  MOVE_M11              the move card's text.
  events_picture(t, scale=1.0, center=ORIGIN, flags=True)
                        small F19 picture: DIM circle and axes, the GOLD arrow 25 e^{i(3t - delta)}, its
                        BLUE shadow dot, the hanging spring beside it with the weight at x(t) = 7 + Re;
                        t a ValueTracker (live) or a number (still). With flags: the four events at the
                        compass points (YELLOW "centre" top and bottom, FG "still" left and right).
                        .arrow .shadow .spring .circle .flags
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

kit = load_scene("ch1_s2_tools")
ak = load_scene("ch2_s3_velocity")
s1 = load_scene("ch4_s1_hook")
s4 = load_scene("ch4_s4_f19")

MOVE_M11 = "Ask where the arrow points: vertical means passing the centre; flat means still."

# ── F19 numbers (checked with cmath) ─────────────────────────────────────────────
DELTA = float(np.arctan2(7, 24))          # 0.28379
PERIOD = TAU / 3                          # 2.0944
T_TOP = DELTA / 3                         # 0.0946  flat right, x = 32
T_PASS1 = (PI / 2 + DELTA) / 3            # 0.6182  straight up
T_BOT = (PI + DELTA) / 3                  # 1.1418  flat left, x = -18
T_PASS2 = (3 * PI / 2 + DELTA) / 3        # 1.6654  straight down
T_END = (TAU + DELTA) / 3                 # 2.1890  flat right again
T_TURN = (1.4 + DELTA) / 3                # {turn}: the arrow at 1.4 rad (room for its angle label)


def zf(t):
    """X - its centre: 25 e^{i(3t - delta)}."""
    return 25 * complex(np.cos(3 * t - DELTA), np.sin(3 * t - DELTA))


def xf(t):
    return 7 + zf(t).real


def _v(x):
    return x.get_value() if hasattr(x, "get_value") else float(x)


# ── the re-framed plane ──────────────────────────────────────────────────────────
U2 = 0.07                                  # scene units per cm (s4: 0.2)
O2 = np.array([-0.95, 0.35, 0])            # the plane's origin = the centre, x = 7
CX = 1.4                                   # derivation column's left edge
ANG_R = 0.6                                # angle arc radius
LAB_R = 1.2                                # angle label's centre, at half the angle
INSET_POS = s4.INSET_POS
RULER_X = INSET_POS[0] + 0.45
W0, WS = -1.85, 0.72                       # wave: y at t = 0, scene units per second (downward)


def P(z):
    z = complex(z)
    return O2 + U2 * np.array([z.real, z.imag, 0.0])


def px(x):
    """Scene x of the position x (cm)."""
    return O2[0] + U2 * (x - 7)


def wy(t):
    return W0 - WS * t


def new_plane():
    r = 25 * U2 + 0.4
    re_ax = Line(O2 + r * LEFT, O2 + r * RIGHT)
    im_ax = Line(O2 + r * DOWN, O2 + r * UP)
    axes = VGroup(re_ax, im_ax).set_stroke(DIM, 2.5)
    circle = Circle(radius=25 * U2).move_to(O2).set_stroke(DIM, 2, opacity=0.8)
    im = T("Im", size=24, color=DIM).next_to(im_ax.get_end(), RIGHT, buff=0.1)
    im.align_to(O2 + (25 * U2 + 0.15) * UP, DOWN)          # clear above the circle's top
    g = VGroup(axes, circle, im)
    g.set_z_index(-4)
    g.axes, g.circle, g.im = axes, circle, im
    return g


def plane_ticks():
    """Ticks on the axis at x = -18, 0, 7, 32. −18 and 32 just outside the circle, 7 and "centre" left of
    the Im axis above, 0 and "origin" below (the arrow sits right of the Im axis in clip 1)."""
    y = O2[1]
    ticks, nums = VGroup(), VGroup()
    for x, col in ((-18, DIM), (0, DIM), (7, YELLOW), (32, DIM)):
        tk = Line([px(x), y - 0.09, 0], [px(x), y + 0.09, 0]).set_stroke(col, 3 if col == DIM else 4)
        ticks.add(tk)
        n = T(str(x).replace("-", "−"), size=24, color=YELLOW if x == 7 else DIM)
        n.move_to([px(x), y + 0.25, 0])
        if x == 32:
            n.move_to([px(x) + 0.08, y + 0.25, 0], aligned_edge=LEFT)
        if x == -18:
            n.move_to([px(x) - 0.08, y + 0.25, 0], aligned_edge=RIGHT)
        if x == 0:
            n.move_to([px(x), y - 0.25, 0])
        if x == 7:
            n.move_to([px(x) - 0.08, y + 0.25, 0], aligned_edge=RIGHT)
        nums.add(n)
    origin = T("origin", size=22, color=DIM).next_to(nums[1], DOWN, buff=0.08)
    centre = T("centre", size=22, color=YELLOW).next_to(nums[2], UP, buff=0.08)
    centre.align_to(nums[2], RIGHT)
    ticks.set_z_index(-3)
    g = VGroup(ticks, nums, origin, centre)
    g.ticks, g.nums, g.origin, g.centre = ticks, nums, origin, centre
    return g


def inset_ruler():
    def yy(x):
        return s1.weight_center(x, INSET_POS, s4.INSET_S)[1]
    line = Line([RULER_X, yy(-18) - 0.12, 0], [RULER_X, yy(32) + 0.12, 0]).set_stroke(DIM, 2)
    g = VGroup(line)
    for x in (-18, 0, 7, 32):
        col = YELLOW if x == 7 else DIM
        tk = Line([RULER_X - 0.08, yy(x), 0], [RULER_X + 0.08, yy(x), 0]).set_stroke(col, 3)
        n = T(str(x).replace("-", "−"), size=22, color=col).next_to(tk, RIGHT, buff=0.1)
        if x == 0:
            n.shift(0.05 * DOWN)
        if x == 7:
            n.shift(0.05 * UP)
        g.add(tk, n)
    return g


def arrow_at(t):
    return ak.arrow_between(O2, P(zf(_v(t))), GOLD, width=6)


def shadow_at(t):
    z = zf(_v(t))
    tip, foot = P(z), P(z.real)
    if np.linalg.norm(tip - foot) > 0.06:
        ln = DashedLine(tip, foot, dash_length=0.07).set_stroke(DIM, 2)
    else:
        ln = Line(tip, foot).set_stroke(DIM, 2, opacity=0)
    dot = Dot(foot, radius=0.09, color=BLUE).set_z_index(-1.7)
    return VGroup(ln, dot)


def angle_arc_at(t, color=YELLOW, radius=ANG_R):
    a = 3 * _v(t) - DELTA
    if abs(a) < 0.02:
        a = 0.02
    arc = Arc(radius=radius, start_angle=0, angle=a, arc_center=O2.copy())
    return arc.set_stroke(color, 4).set_z_index(-1.7)


# ── column helpers ───────────────────────────────────────────────────────────────
def mt(parts, cols=None, glyphs=None, size=32):
    m = MathTex(*parts, font_size=size)
    for k, c in (cols or {}).items():
        m[k].set_color(c)
    for (k, i), c in (glyphs or {}).items():
        m[k][i].set_color(c)
    return m


def at_row(mob, y):
    return mob.move_to([CX, y, 0], aligned_edge=LEFT)


def below(mob, prev, gap=0.42):
    """Put mob's top `gap` under prev's bottom, on the column; returns the gap's middle y."""
    mob.move_to([CX, 0, 0], aligned_edge=LEFT)
    mob.shift((prev.get_bottom()[1] - gap - mob.get_top()[1]) * UP)
    return prev.get_bottom()[1] - gap / 2


def step_at(text, y):
    s = kit.step_label(text, 0)
    s.shift([CX - kit.COL_LEFT, y - s[0].get_center()[1], 0])
    return s


# ── lines ────────────────────────────────────────────────────────────────────────
def line_polar():
    return mt(["24", "-", "7i", "=", "25", r"\,e^{-i\delta}"], {0: BLUE, 2: PINK, 4: GOLD, 5: GOLD},
              {(5, 3): YELLOW})


def line_tan():
    return mt([r"\tan", r"\delta", "=", r"\tfrac{7}{24}"], {1: YELLOW})


def line_delta():
    return mt([r"\delta", r"\approx 0.284\ \text{rad}\ \ (16.3^\circ)"], {0: YELLOW})


def line_sub():
    return mt(["X", "=", "25", r"\,e^{-i\delta}", r"\,e^{3it}"], {0: GOLD, 2: GOLD, 3: GOLD, 4: GOLD},
              {(3, 3): YELLOW})


def line_final():
    m = mt(["X", "=", "25", r"\,e^{i(3t - \delta)}"], {0: GOLD, 2: GOLD, 3: GOLD})
    for i in (3, 4, 5, 6):
        m[3][i].set_color(YELLOW)
    return m


def line_shadow():
    m = mt(["x - 7", "=", "25", r"\cos(3t - \delta)"], {2: GOLD}, {(0, 0): BLUE})
    for i in (4, 5, 6, 7):
        m[3][i].set_color(YELLOW)
    return m


def mapping_box():
    s = 24
    l1 = VGroup(T("the sheet's form", size=s, color=DIM),
                MathTex(r"A\,e^{i\phi}", font_size=s * 1.25, color=FG)).arrange(RIGHT, buff=0.15)
    a = MathTex("A", "=", "|", "24", "-", "7i", "|", "=", "25", font_size=s * 1.25)
    a[3].set_color(BLUE)
    a[5].set_color(PINK)
    a[8].set_color(GOLD)
    l2 = VGroup(T("its", size=s, color=DIM), a).arrange(RIGHT, buff=0.15)
    ph = MathTex(r"\phi", "=", r"3t - \delta", font_size=s * 1.25)
    ph[2].set_color(YELLOW)
    l3 = VGroup(T("its", size=s, color=DIM), ph, T(", the arrow's angle", size=s, color=DIM)).arrange(
        RIGHT, buff=0.12)
    for ln in (l1, l2, l3):
        kit._baseline_align(ln[0], 0)
    l1[1].align_to(l1[0], DOWN).shift(0.02 * DOWN)
    l2[1].align_to(l2[0], DOWN).shift(0.03 * DOWN)
    l3[1].align_to(l3[0], DOWN).shift(0.03 * DOWN)
    l3[2].align_to(l3[0], DOWN)
    body = VGroup(l1, l2, l3).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.1, width=body.width + 0.4, height=body.height + 0.34)
    box.set_stroke(DIM, 1.5).set_fill(kit.CARD_FILL, 1).move_to(body)
    g = VGroup(box, body)
    g.box, g.body = box, body
    return g


E_X = (r"x", BLUE, "position from 0")
E_W = s4.E_W
E_XX = s4.E_XX
E_D = (r"\delta", YELLOW, "tan δ = 7/24")
E_A = (r"3t - \delta", YELLOW, "the arrow's angle")


# ── recap export ─────────────────────────────────────────────────────────────────
def events_picture(t, scale=1.0, center=ORIGIN, flags=True):
    """F19's arrow at its four events, small: see the module docstring."""
    c = np.array(center, dtype=float)
    R = 1.1 * scale
    o = c + 0.55 * scale * RIGHT
    sp_pos = c + (0.55 * scale - R - 0.85 * scale) * RIGHT + 0.05 * scale * DOWN
    sp_s = 0.4 * scale
    k = R / 25

    def pt(z):
        return o + k * np.array([z.real, z.imag, 0.0])

    circle = Circle(radius=R).move_to(o).set_stroke(DIM, 2)
    axes = VGroup(Line(o + 1.12 * R * LEFT, o + 1.12 * R * RIGHT),
                  Line(o + 1.12 * R * DOWN, o + 1.12 * R * UP)).set_stroke(DIM, 2)
    base = VGroup(axes, circle).set_z_index(-4)

    def b_arrow():
        return ak.arrow_between(o, pt(zf(_v(t))), GOLD, width=max(3, 6 * scale))

    def b_shadow():
        z = zf(_v(t))
        tip, foot = pt(z), pt(complex(z.real, 0))
        ln = (DashedLine(tip, foot, dash_length=0.06).set_stroke(DIM, 1.5)
              if np.linalg.norm(tip - foot) > 0.05 else Line(tip, foot).set_stroke(DIM, 1.5, opacity=0))
        return VGroup(ln, Dot(foot, radius=0.07, color=BLUE).set_z_index(-1.7))

    def b_spring():
        return s1.hanging_spring(xf(_v(t)), pos=sp_pos, scale=sp_s)

    live = hasattr(t, "get_value")
    arrow = always_redraw(b_arrow) if live else b_arrow()
    sh = always_redraw(b_shadow) if live else b_shadow()
    spring = always_redraw(b_spring) if live else b_spring()
    g = VGroup(base, spring, arrow, sh)
    fl = VGroup()
    if flags:
        for d, word, col in ((UP, "centre", YELLOW), (DOWN, "centre", YELLOW),
                             (RIGHT, "still", FG), (LEFT, "still", FG)):
            p = o + R * d
            dot = Dot(p, radius=0.06, color=col)
            lab = T(word, size=22, color=col).next_to(dot, d, buff=0.12)
            fl.add(VGroup(dot, lab))
        g.add(fl)
    g.arrow, g.shadow, g.spring, g.circle, g.flags = arrow, sh, spring, circle, fl
    return g


class Events(NarratedScene):
    def construct(self):
        shot = s4.handover_shot()
        self.add(*shot)
        (self.oplane, self.ogold, self.oglab, self.oinset, self.xl, self.leg, self.pin,
         self.strip) = shot
        _check = events_picture(0.3, scale=0.6)   # build once: the export must not break s7
        del _check
        self.tt = ValueTracker(0.0)
        self.xin = ValueTracker(7.0)
        self.linked = False
        self.clip_polar()
        self.clip_move()
        self.clip_answer()
        self.clip_distances()
        self.clip_sweep()

    # ── live pieces ─────────────────────────────────────────────────────────────
    def inset_x(self):
        return xf(self.tt.get_value()) if self.linked else self.xin.get_value()

    # ── c4.events.1: hint 2, polar form ─────────────────────────────────────────
    def clip_polar(self):
        tt = self.tt
        hint = T("Hint 2", size=32, color=YELLOW).move_to([CX, 2.95, 0], aligned_edge=LEFT)
        self.hint = hint
        r0 = self.xl
        with self.say("c4.events.1", gap=0.3) as c:
            self.play(*appear(hint), run_time=1.0)
            # re-frame the plane: one smooth move
            k = U2 / s4.F19_U
            grid, axes, re, im = self.oplane
            gold2 = arrow_at(0.0)
            mid = (O2 + P(zf(0))) / 2
            nrm = np.array([-7.0, -24.0, 0]) / 25
            r0_target = r0.copy().move_to([CX, 2.3, 0], aligned_edge=LEFT)
            anims = [grid.animate.scale(k, about_point=s4.F19_O).shift(O2 - s4.F19_O),
                     axes.animate.scale(k, about_point=s4.F19_O).shift(O2 - s4.F19_O),
                     *disappear(re, im),
                     Transform(self.ogold, gold2),
                     self.oglab.animate.move_to(mid + 0.42 * nrm),
                     r0.animate.move_to(r0_target)]
            c.wait_until("first step")
            kit.legend_set(self, self.leg, [E_X, E_W, E_XX], *anims, run_time=2.0)
            # the new frame: whole circle of radius 25, ticks; old pieces hand over
            plane = new_plane()
            ticks = plane_ticks()
            self.remove(self.ogold)
            arrow = always_redraw(lambda: arrow_at(tt))
            self.add(arrow)
            c.wait_until("polar form")
            self.play(*during([FadeOut(grid), FadeOut(axes)], 0.3, 1.0),
                      *during([FadeIn(plane.axes), Create(plane.circle)], 0, 0.8),
                      *during([FadeIn(ticks.ticks), *appear(*ticks.nums, plane.im, lag=0.1)], 0.3, 1.0),
                      run_time=1.6)
            self.play(*appear(ticks.origin, ticks.centre, lag=0.3), run_time=1.0)
            # the weight follows the arrow's shadow
            self.remove(self.oinset)
            inset = always_redraw(lambda: s1.hanging_spring(self.inset_x(), pos=INSET_POS, scale=s4.INSET_S))
            self.add(inset)
            ruler = inset_ruler()
            shadow = always_redraw(lambda: shadow_at(tt))
            c.wait_until("where the weight is")
            self.play(FadeIn(shadow), *appear(ruler, shift=None), self.xin.animate.set_value(xf(0)),
                      run_time=1.6)
            self.linked = True
            self.plane, self.ticks, self.arrow, self.inset, self.ruler, self.shadow = (
                plane, ticks, arrow, inset, ruler, shadow)

            # {polar}: length 25, angle -delta
            r1 = line_polar()
            st1 = step_at("length 25, angle −δ", below(r1, r0_target))
            c.wait_until("polar")
            self.play(*appear(st1, r1, lag=0.3, shift=None),
                      VShowPassingFlash(arrow_at(0.0).set_stroke(YELLOW, 8), time_width=0.5), run_time=1.4)
            arc = always_redraw(lambda: angle_arc_at(tt))
            lab_d = MathTex(r"-\delta", font_size=32, color=YELLOW)
            lab_d.move_to(O2 + 0.95 * np.array([np.cos(-0.6), np.sin(-0.6), 0]))   # under the arrow: the wedge is thin
            c.wait_until("minus delta")
            self.play(*during(disappear(self.oglab), 0, 0.45),     # the angle label takes its spot
                      *during([Create(arc), *appear(lab_d, shift=None)], 0.4, 1.0), run_time=1.5)
            c.wait_until("delta is")
            kit.legend_add(self, self.leg, E_D, run_time=1.0)
            r2 = line_tan()
            below(r2, r1)
            r2b = line_delta()
            below(r2b, r2, gap=0.2)
            c.wait_until("tangent")
            self.play(*appear(r2, shift=None), run_time=1.0)
            c.wait_until("sixteen")
            self.play(*appear(r2b, shift=None), run_time=1.0)

            # {turn}: substitute, the angles add up
            r3 = line_sub()
            st3 = step_at("substitute", below(r3, r2b))
            c.wait_until("turn")
            self.play(*appear(st3, r3, lag=0.3, shift=None), run_time=1.2)
            lab_a = MathTex(r"3t - \delta", font_size=32, color=YELLOW)

            def place_a(m):
                a = 3 * tt.get_value() - DELTA
                m.move_to(O2 + LAB_R * np.array([np.cos(a / 2), np.sin(a / 2), 0]))
            lab_a.move_to(O2 + LAB_R * np.array([np.cos(0.7), np.sin(0.7), 0]))
            c.wait_until("angles add up")
            self.play(tt.animate.set_value(T_TURN), *swap(lab_d, lab_a),
                      run_time=1.8)
            lab_a.add_updater(place_a)
            r4 = line_final()
            st4 = step_at("the angles add up", below(r4, r3))
            c.wait_until("to the eye")
            derive(self, r3, r4, run_time=1.8)
            self.play(*appear(st4, shift=None), run_time=0.8)
            c.wait_until("three t minus delta")
            kit.legend_add(self, self.leg, E_A, run_time=1.0)
            # {sheetform}
            mbox = mapping_box()
            mbox.move_to([CX, 0, 0], aligned_edge=LEFT)
            mbox.shift((r4.get_bottom()[1] - 0.35 - mbox.get_top()[1]) * UP)
            c.wait_until("sheetform")
            self.play(FadeIn(mbox.box), *appear(*mbox.body, lag=0.3, shift=None),
                      run_time=min(1.4, c.until()))
        self.arc, self.lab_a, self.mbox = arc, lab_a, mbox

        # the polar lines leave; X = 25 e^{i(3t - delta)} goes to the top, its shadow under it
        y_top = 1.12
        dy = y_top - r4.get_center()[1]
        r5 = line_shadow()
        r5.move_to([CX, 0, 0], aligned_edge=LEFT)
        r5.shift((r4.get_bottom()[1] + dy - 0.42 - r5.get_top()[1]) * UP)
        st5 = step_at("take the shadow", (r4.get_bottom()[1] + dy + r5.get_top()[1]) / 2)
        mb_dy = (r5.get_bottom()[1] - 0.32) - mbox.get_top()[1]
        self.wait(0.6)
        self.play(*during(disappear(r0, st1, r1, r2, r2b, st3, r3, st4), 0, 0.45),
                  *during([r4.animate.shift(dy * UP), mbox.animate.shift(mb_dy * UP)], 0.35, 1.0),
                  run_time=1.6)
        self.play(*appear(st5, r5, lag=0.3, shift=None), run_time=1.1)   # early: the step's label, said as "its shadow" next
        self.wait(0.4)
        self.r4, self.r5, self.st5 = r4, r5, st5

    # ── c4.events.2: the move, the four directions, T4.4 ────────────────────────
    def clip_move(self):
        card = kit.move_card(MOVE_M11)
        g = 25 * U2
        up = ak.arrow_between(O2, O2 + g * UP, GOLD, width=5).set_opacity(0.5)
        dn = ak.arrow_between(O2, O2 + g * DOWN, GOLD, width=5).set_opacity(0.5)
        rt = ak.arrow_between(O2, O2 + g * RIGHT, GOLD, width=5).set_opacity(0.5)
        lf = ak.arrow_between(O2, O2 + g * LEFT, GOLD, width=5).set_opacity(0.5)
        c_dot = Dot(O2, radius=0.11, color=BLUE).set_z_index(-1.6)
        r_dot = Dot(P(25), radius=0.11, color=BLUE).set_z_index(-1.6)
        l_dot = Dot(P(-25), radius=0.11, color=BLUE).set_z_index(-1.6)
        tag_c = T("passing the centre", size=26, color=YELLOW)
        tag_c.move_to(O2 + [-0.15, 25 * U2 + 0.22, 0], aligned_edge=RIGHT)    # outside the circle, by the tip
        tag_s = T("still for an instant", size=26, color=FG).move_to(O2 + [-0.1, -25 * U2 - 0.35, 0])
        with self.say("c4.events.2") as c:
            self.play(*during(disappear(self.hint), 0, 0.45), *during(appear(card), 0.35, 1.0), run_time=1.4)   # early: the move card, shown whole, then walked
            c.wait_until("where the arrow points")
            self.play(FlashAround(card.body, run_time=1.5, time_width=1.5))
            c.wait_until("upright")
            self.play(GrowArrow(up), run_time=1.0)
            c.wait_until("straight down")
            self.play(GrowArrow(dn), run_time=1.0)
            c.wait_until("at the centre")
            self.play(FadeIn(c_dot, scale=0.5), FlashAround(self.ticks.nums[2], run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until(own_word=tag_c)
            self.play(*appear(tag_c), run_time=1.0)
            c.wait_until("flat")
            self.play(*set_alpha([up, dn, tag_c], 0.3), GrowArrow(rt), GrowArrow(lf), run_time=1.4)
            c.wait_until("as far out")
            self.play(FadeIn(r_dot, scale=0.5), FadeIn(l_dot, scale=0.5), run_time=1.0)
            c.wait_until(own_word=tag_s)
            self.play(*appear(tag_s), run_time=1.0)

            # T4.4
            think = kit.think_box("The weight passes the centre when\nthe arrow points straight up or down.\n"
                                  "When does it first point straight up?", size=30, pos=[3.45, -2.4, 0])
            ring = kit.think_ring()
            c.wait_until("t44")
            self.play(*during(disappear(self.mbox), 0, 0.45),
                      *during([FadeIn(think.box), *appear(think.question, shift=None), FadeIn(ring)], 0.4, 1.0),
                      run_time=1.5)   # early: the think stop's question, read at once
            c.wait_until("pause the video")
            self.play(*appear(think.hint), *disappear(up, dn, rt, lf, c_dot, r_dot, l_dot, tag_c, tag_s),
                      run_time=1.0)
            self.play(kit.drain(ring, c.until()))
        self.card, self.think, self.ring = card, think, ring

    # ── c4.events.3: the solution ───────────────────────────────────────────────
    def clip_answer(self):
        tt, r5 = self.tt, self.r5
        a1 = mt([r"3t - \delta", "=", r"\tfrac{\pi}{2}"], {0: YELLOW})
        y1 = below(a1, r5)
        st_a1 = step_at("first time straight up", y1)
        ref = kit.tag("reference").next_to(r5, RIGHT, buff=0.4)
        a2 = mt(["3t", "=", r"\tfrac{\pi}{2}", "+", r"\delta"], {4: YELLOW})
        st_a2 = step_at("add δ", below(a2, a1))
        a3 = mt(["t", "=", r"\dfrac{\pi/2 + \delta}{3}", r"\approx 0.618"], None, {(2, 4): YELLOW})
        st_a3 = step_at("divide by 3", below(a3, a2))
        with self.say("c4.events.3") as c:
            self.play(*disappear(self.think, self.ring), *set_alpha([self.r4], 0.4), run_time=0.9)
            c.wait_until("three t minus delta")
            self.play(*appear(st_a1, a1, ref, lag=0.3, shift=None), run_time=1.3)
            c.wait_until("reaches pi")
            self.play(tt.animate.set_value(T_PASS1), run_time=min(1.6, 0.9 * c.until("add")))
            c.wait_until("add")
            derive(self, a1, a2, run_time=1.8)
            self.play(*appear(st_a2, shift=None), run_time=0.7)
            c.wait_until("you find")
            derive(self, a2, a3, *set_alpha([a1, st_a1], 0.4), run_time=1.8)
            self.play(*appear(st_a3, shift=None), run_time=0.7)

            # {second}: the first passage is done; the second one under it
            # {second}: the first passage is done; the second one under it
            a3_dy = (a1.get_top()[1] + 0.05) - a3.get_top()[1]
            a3_t = a3.copy().shift(a3_dy * UP)
            st_a3b = step_at("first passage", y1)
            a4 = mt([r"3t - \delta", "=", r"\tfrac{3\pi}{2}"], {0: YELLOW})
            st_a4 = step_at("straight down", below(a4, a3_t))
            a5 = mt(["t", "=", r"\dfrac{3\pi/2 + \delta}{3}", r"\approx 1.665"], None, {(2, 5): YELLOW})
            st_a5 = step_at("same two steps", below(a5, a4))
            note = VGroup(T("half a turn later:", size=22, color=DIM),
                          MathTex(r"+\,\pi/3 \approx 1.047", font_size=28, color=DIM)).arrange(RIGHT, buff=0.12)
            note.next_to(a5, DOWN, buff=0.2, aligned_edge=LEFT).shift(0.35 * RIGHT)
            c.wait_until("half a turn")
            self.lab_a.clear_updaters()
            self.play(*disappear(self.arc, self.lab_a), run_time=0.6)
            self.play(tt.animate.set_value(T_PASS2),
                      *during(disappear(a1, st_a1, a2, st_a2, st_a3), 0, 0.4),
                      *during([a3.animate.shift(a3_dy * UP)], 0.3, 0.8),
                      *during(appear(st_a3b, shift=None), 0.75, 1.0),
                      run_time=max(1.0, min(2.0, 0.9 * c.until("straight down"))))
            c.wait_until("straight down")
            self.play(*appear(st_a4, a4, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("one point six seven")
            self.play(*appear(st_a5, a5, lag=0.3, shift=None), run_time=1.2)
            self.play(*appear(note, shift=None), run_time=0.8)

            # {still}: the arrow lies flat
            c.wait_until("lies flat")
            self.play(tt.animate.set_value(T_END), run_time=1.5)
            pas = mt(["t", r"\approx 0.618,\ \ 1.665"])
            at_row(pas, 0)
            pas.align_to(a3, UP)
            pas_tag = kit.tag("the two passages", pas)
            r7 = mt(["x - 7", "=", r"\pm 25"], {2: GOLD}, {(0, 0): BLUE})
            st7 = step_at("arrow flat", below(r7, pas))
            c.wait_until("so ex minus seven")
            self.play(*during(disappear(a3, st_a3b, a4, st_a4, a5, st_a5, note), 0, 0.45),
                      *during(appear(pas, pas_tag, lag=0.2, shift=None), 0.5, 1.0), run_time=1.3)
            self.play(*appear(st7, r7, lag=0.3, shift=None), run_time=min(1.2, max(0.5, c.until())))
        self.ref, self.pas, self.pas_tag, self.r7, self.st7 = ref, pas, pas_tag, r7, st7

    # ── c4.events.4: the tempting wrong answer ──────────────────────────────────
    def clip_distances(self):
        r7 = self.r7
        bot = O2[1] - 25 * U2 - 0.05
        p32, p18, p7, p0 = [np.array([px(x), bot, 0]) for x in (32, -18, 7, 0)]
        br_r = span_brace(p7, p32, color=FG)
        br_l = span_brace(p18, p7, color=FG)
        l_r = MathTex("25", font_size=30, color=GOLD).next_to(br_r, DOWN, buff=0.1)
        l_l = MathTex("25", font_size=30, color=GOLD).next_to(br_l, DOWN, buff=0.1)
        dist = T("distances: 25", size=28).next_to(r7, RIGHT, buff=0.5)
        strike = Line(dist.get_left() + 0.05 * LEFT, dist.get_right() + 0.05 * RIGHT).set_stroke(RED, 4)
        x_mark = cross_mark(RED).scale(0.8).next_to(dist, RIGHT, buff=0.2)
        from_c = kit.tag("from the centre").next_to(dist, DOWN, buff=0.14, aligned_edge=LEFT)
        o_line = DashedLine([px(0), self.ticks.origin.get_bottom()[1] - 0.08, 0], [px(0), bot + 0.02, 0],
                            dash_length=0.08).set_stroke(DIM, 2)
        br_r2 = span_brace(p0, p32, color=BLUE)
        br_l2 = span_brace(p18, p0, color=BLUE)
        l_r2 = MathTex("32", font_size=30, color=BLUE).next_to(br_r2, DOWN, buff=0.1)
        l_l2 = MathTex("18", font_size=30, color=BLUE).next_to(br_l2, DOWN, buff=0.1)
        r8 = mt(["x", "=", "32", r"\ \ \text{or}\ \ ", "x", "=", "-18"], {0: BLUE, 4: BLUE})
        st8 = step_at("add 7", below(r8, r7))
        fin = T("distances 32 and 18", size=30, color=YELLOW)
        fin_box = SurroundingRectangle(fin, color=YELLOW, buff=0.16, corner_radius=0.08).set_stroke(width=2.5)
        finale = VGroup(fin_box, fin)
        finale.move_to([CX, 0, 0], aligned_edge=LEFT)
        finale.shift((r8.get_bottom()[1] - 0.4 - finale.get_top()[1]) * UP)
        with self.say("c4.events.4", gap=1.5) as c:
            c.wait_until("tempted")
            self.play(GrowFromCenter(br_r), GrowFromCenter(br_l), *appear(l_r, l_l, shift=None), run_time=1.3)
            c.wait_until(own_word=dist)
            self.play(*appear(dist), run_time=1.0)
            c.wait_until("wrong")
            self.play(Create(strike), Create(x_mark), *recolor([dist], DIM), run_time=1.0)
            c.wait_until("from the centre")
            self.play(*appear(from_c), FlashAround(self.ticks.nums[2], run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until("from the origin")
            self.play(Create(o_line), FlashAround(self.ticks.nums[1], run_time=1.2, time_width=1.5),
                      run_time=1.2)
            c.wait_until("fix")
            self.play(*appear(st8, r8, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("minus eighteen")
            self.play(*during(disappear(br_r, br_l, l_r, l_l), 0, 0.45),
                      *during([GrowFromCenter(br_r2), GrowFromCenter(br_l2), *appear(l_r2, l_l2, shift=None)],
                              0.45, 1.0), run_time=1.4)
            c.wait_until("distances are")
            self.play(GrowFromCenter(fin_box), *appear(fin), run_time=min(1.1, c.until()))
        self.clip4 = [dist, strike, x_mark, from_c, o_line, br_r2, br_l2, l_r2, l_l2]
        self.r8, self.st8, self.finale = r8, st8, finale

    # ── c4.events.5: the sweep ──────────────────────────────────────────────────
    def clip_sweep(self):
        tt = self.tt
        t_axis = Line([px(7), W0 + 0.08, 0], [px(7), wy(T_END) - 0.05, 0]).set_stroke(DIM, 2)
        t_lab = MathTex("t", font_size=28, color=DIM).next_to(t_axis.get_end(), LEFT, buff=0.12).shift(0.12 * UP)
        t_axis.set_z_index(-3)

        def wave():
            s_end = tt.get_value()
            if s_end <= 0.004:
                return VMobject()
            n = max(3, int(220 * s_end / T_END) + 3)
            pts = [[px(xf(s)), wy(s), 0] for s in np.linspace(0, s_end, n)]
            return VMobject().set_points_as_corners(pts).set_stroke(BLUE, 4)

        def link_line():
            s = max(tt.get_value(), 0.0)
            top = np.array([px(xf(s)), O2[1], 0])
            bot = np.array([px(xf(s)), wy(s), 0])
            return Line(top, bot).set_stroke(DIM, 1.5, opacity=0.5).set_z_index(-3.5)

        rows_spec = [(r"t = 0", r"x = 31", "moving out", FG),
                     (r"t \approx 0.095", r"x = 32", "still", FG),
                     (r"t \approx 0.618", r"x = 7", "centre", YELLOW),
                     (r"t \approx 1.142", r"x = -18", "still", FG),
                     (r"t \approx 1.665", r"x = 7", "centre", YELLOW)]
        t_ev = [0.0, T_TOP, T_PASS1, T_BOT, T_PASS2]
        rows, dots = [], []
        y_row = self.r5.get_bottom()[1] - 0.55
        for i, (ts, xs, word, col) in enumerate(rows_spec):
            a = MathTex(ts, font_size=30)
            b = MathTex(xs, font_size=30)
            b[0][0].set_color(BLUE)
            w = T(word, size=26, color=col)
            y = y_row - 0.5 * i
            a.move_to([CX, y, 0], aligned_edge=LEFT)
            b.move_to([CX + 1.75, y, 0], aligned_edge=LEFT)
            w.move_to([CX + 3.35, y, 0], aligned_edge=LEFT)
            kit._baseline_align(w, a.get_bottom()[1] + 0.02)
            rows.append(VGroup(a, b, w))
            dots.append(Dot([px(xf(t_ev[i])), wy(t_ev[i]), 0], radius=0.07,
                            color=YELLOW if col == YELLOW else FG).set_z_index(-1))
        per = VGroup(T("one full turn: period", size=26, color=TEAL),
                     MathTex(r"2\pi/3 \approx 2.09", font_size=30, color=TEAL)).arrange(RIGHT, buff=0.15)
        per.move_to([CX, y_row - 0.5 * 5 - 0.12, 0], aligned_edge=LEFT)
        turn = Arc(radius=25 * U2, start_angle=0, angle=TAU * 0.999, arc_center=O2.copy()).set_stroke(TEAL, 4)
        turn.set_z_index(-1.6)

        with self.say("c4.events.5") as c:
            # one period back: the same arrow, the same weight (an invisible jump)
            tt.set_value(T_END - PERIOD)
            out = [self.ref, self.pas, self.pas_tag, self.r7, self.st7, *self.clip4]
            self.play(*during(disappear(*out), 0, 0.5),
                      *during([tt.animate.set_value(0.0)], 0.3, 1.0),
                      *during([Create(t_axis), *appear(t_lab, shift=None)], 0.5, 1.0), run_time=1.6)
            rd_specs = [(r"t =", lambda: tt.get_value(), FG, 3, 2.5),
                        (r"3t - \delta =", lambda: 3 * tt.get_value() - DELTA, YELLOW, 2, 1.95),
                        (r"x =", lambda: xf(tt.get_value()), BLUE, 1, 1.4)]
            labs, builders = [], []
            for tex, fn, col, places, y in rd_specs:
                lab = MathTex(tex, font_size=36, color=col).move_to([-5.15, y, 0], aligned_edge=LEFT)
                labs.append(lab)

                def build(fn=fn, col=col, places=places, lab=lab):
                    # one Text, not a DecimalNumber: its digits are separate texts, which the
                    # overlap audit sees crossing when the number's width changes
                    v = f"{fn():.{places}f}".replace("-", "−")
                    return T(v, size=27, color=col).next_to(lab, RIGHT, buff=0.15).align_to(lab, DOWN)
                builders.append(build)
            nums0 = [b() for b in builders]
            self.play(*appear(*[VGroup(lb, n) for lb, n in zip(labs, nums0)], lag=0.25, shift=None),
                      run_time=1.0)   # early: the sweep's readouts, read as it runs
            self.remove(*nums0)
            nums = [always_redraw(b) for b in builders]
            self.add(*nums)
            wv = always_redraw(wave)
            ln = always_redraw(link_line)
            self.add(ln, wv)

            c.wait_until("thirty-one")
            self.play(*during(disappear(self.r8, self.st8, self.finale), 0, 0.45),
                      *during([*appear(rows[0], shift=None), FadeIn(dots[0], scale=0.5)], 0.45, 1.0),
                      run_time=1.3)
            # the run: each stretch ends on its mark
            c.wait_until("moving out")
            lead = 1.4
            if c.until("top") - lead > 0.05:
                self.wait(c.until("top") - lead)
            self.play(tt.animate.set_value(T_TOP), rate_func=linear, run_time=max(0.3, c.until("top")))
            plan = [("pass1", T_PASS1, 1), ("bottom", T_BOT, 2), ("pass2", T_PASS2, 3)]
            for cue, tgt, i in plan:
                self.play(tt.animate.set_value(tgt), *during([*appear(rows[i], shift=None),
                                                              FadeIn(dots[i], scale=0.5)], 0, 0.4),
                          rate_func=linear, run_time=max(0.5, c.until(cue)))
            self.play(tt.animate.set_value(T_END), *during([*appear(rows[4], shift=None),
                                                            FadeIn(dots[4], scale=0.5)], 0, 0.3),
                      rate_func=linear, run_time=3.0)
            self.play(Create(turn), *appear(per, shift=None), run_time=1.4)

            # {same}: the weight you watched at the start
            c.wait_until("same")
            snap = s1.hanging_spring(xf(T_END), pos=INSET_POS, scale=s4.INSET_S)
            self.play(FlashAround(snap, run_time=2.0, time_width=1.5, color=BLUE),
                      FlashAround(self.arrow, run_time=2.0, time_width=1.5))
            if c.until() > 0.3:
                self.wait(c.until() - 0.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
