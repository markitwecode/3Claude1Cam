"""Chapter 6, scene 7: Kirchhoff's current and voltage laws. Clips c6.laws.1 – c6.laws.6.

Opens on ch6_s6_resistance.handover_shot() (the running loop, 10 Ω resistor, 1.5 V / 0.15 A).
Owns two drawings kept for s8's recap and Lecture 12 (import with load_scene("ch6_s7_kirchhoff")):
  kcl_junction()  p. 170's node: two wires in from the left, one out to the right, GOLD current
                  arrows and I_1, I_2, I_3. .wires (in1, in2, out) .node .arrows .labels .paths
  kvl_loop()      p. 170's six-element loop, exactly as the slide draws it (clockwise current).
                  .wire .dot .bats (V_1, V_3, V_6) .res (R_a, R_b, R_c) .varrows (V_1..V_6, arrows
                  only) .vlabels .names (R_a, R_b, R_c) .current (GOLD arrow above V_1)
                  .through (small GOLD arrows through each resistor, not added) .corners (bl, tl, tr, br)
                  (built at full size; this scene itself shows it ×K_SCALE, shifted by K_SHIFT: see kp())
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

S2 = load_scene("ch6_s2_electrons")
WIRE_W = S2.WIRE_W

# ---------------------------------------------------------------------------------------------
# p. 170's junction (KCL)
# ---------------------------------------------------------------------------------------------
NODE = np.array([0.6, 0.0, 0.0])
J_X0, J_Y = -4.6, 1.5          # wires enter at x = J_X0, at y = ±J_Y


def kcl_junction():
    in1 = VMobject().set_points_as_corners([[J_X0, J_Y, 0], [-2.2, J_Y, 0], NODE])
    in2 = VMobject().set_points_as_corners([[J_X0, -J_Y, 0], [-2.2, -J_Y, 0], NODE])
    out = VMobject().set_points_as_corners([NODE, [4.6, 0, 0]])
    wires = VGroup(in1, in2, out).set_stroke(FG, WIRE_W)
    node = Dot(NODE, radius=0.13, color=FG)
    a1 = S2.current_arrow([-4.2, J_Y, 0], [-2.9, J_Y, 0])
    a2 = S2.current_arrow([-4.2, -J_Y, 0], [-2.9, -J_Y, 0])
    a3 = S2.current_arrow([2.0, 0, 0], [3.3, 0, 0])
    l1 = MathTex("I_1", font_size=44, color=GOLD).next_to(a1, DOWN, buff=0.2)
    l2 = MathTex("I_2", font_size=44, color=GOLD).next_to(a2, UP, buff=0.2)
    l3 = MathTex("I_3", font_size=44, color=GOLD).next_to(a3, DOWN, buff=0.2)
    arrows, labels = VGroup(a1, a2, a3), VGroup(l1, l2, l3)
    g = VGroup(wires, node, arrows, labels)
    g.wires, g.node, g.arrows, g.labels, g.paths = wires, node, arrows, labels, (in1, in2, out)
    return g


# ---------------------------------------------------------------------------------------------
# p. 170's loop (KVL)
# ---------------------------------------------------------------------------------------------
KL, KR, KT, KB = -4.2, 4.2, 2.4, -1.2      # the loop's sides
K_BAT_Y, K_RC_Y = 0.35, 0.6                  # V_1 on the left side, R_c on the right side
K_TOP_X = (-2.4, 0.0, 2.4)                  # R_a, V_3, R_b along the top
V_OFF, V_HALF = 0.45, 0.45                  # TEAL arrows: offset from the wire, half length


def _hbattery(center, signs_dir):
    """Horizontal cell, "+" (long plate) on the left; signs on the `signs_dir` side (UP/DOWN)."""
    b = S2.battery()
    VGroup(b.leads, b.plus_plate, b.minus_plate).rotate(PI / 2, about_point=ORIGIN)
    s = 1 if signs_dir[1] > 0 else -1
    b.plus_sign.move_to([-0.44, 0.32 * s, 0])     # beside the long plate, off the wire
    b.minus_sign.move_to([0.4, 0.3 * s, 0])
    return b.shift(center)


def _harrow_left(cx, y):
    return S2.voltage_arrow([cx + V_HALF, y, 0], [cx - V_HALF, y, 0])


def kvl_loop():
    L, R, Tp, B = KL, KR, KT, KB
    h = S2.BAT_H / 2
    rs = S2.SLOT_H / 2
    xa, x3, xb = K_TOP_X
    paths = [
        [[L, K_BAT_Y + h, 0], [L, Tp, 0], [xa - rs, Tp, 0]],
        [[xa + rs, Tp, 0], [x3 - h, Tp, 0]],
        [[x3 + h, Tp, 0], [xb - rs, Tp, 0]],
        [[xb + rs, Tp, 0], [R, Tp, 0], [R, K_RC_Y + rs, 0]],
        [[R, K_RC_Y - rs, 0], [R, B, 0], [h, B, 0]],
        [[-h, B, 0], [L, B, 0], [L, K_BAT_Y - h, 0]],
    ]
    wire = VGroup(*[VMobject().set_points_as_corners(p) for p in paths]).set_stroke(FG, WIRE_W)
    dot = Dot([L, B, 0], radius=0.11, color=FG)

    v1 = S2.battery().shift([L, K_BAT_Y, 0])
    v3 = _hbattery(np.array([x3, Tp, 0]), DOWN)
    v6 = _hbattery(np.array([0, B, 0]), UP)
    ra = S2.resistor(vertical=False).move_to([xa, Tp, 0])
    rb = S2.resistor(vertical=False).move_to([xb, Tp, 0])
    rc = S2.resistor().move_to([R, K_RC_Y, 0])

    ar1 = S2.voltage_arrow([L - V_OFF - 0.15, K_BAT_Y - V_HALF, 0], [L - V_OFF - 0.15, K_BAT_Y + V_HALF, 0])
    ar2 = _harrow_left(xa, Tp + V_OFF)
    ar3 = _harrow_left(x3, Tp + V_OFF)
    ar4 = _harrow_left(xb, Tp + V_OFF)
    ar5 = S2.voltage_arrow([R + V_OFF + 0.15, K_RC_Y - V_HALF, 0], [R + V_OFF + 0.15, K_RC_Y + V_HALF, 0])
    ar6 = _harrow_left(0, B - V_OFF)

    def lab(i):
        return MathTex(f"V_{i}", font_size=40, color=TEAL)
    l1 = lab(1).next_to(ar1, LEFT, buff=0.2)
    l2, l3, l4 = (lab(i).next_to(a, UP, buff=0.15) for i, a in ((2, ar2), (3, ar3), (4, ar4)))
    l5 = lab(5).next_to(ar5, RIGHT, buff=0.2)
    l6 = lab(6).next_to(ar6, LEFT, buff=0.2)

    na = MathTex("R_a", font_size=40).next_to(ra.body, DOWN, buff=0.32)
    nb = MathTex("R_b", font_size=40).next_to(rb.body, DOWN, buff=0.32)
    nc = MathTex("R_c", font_size=40).next_to(rc.body, LEFT, buff=0.3)

    cur = S2.current_arrow([L, K_BAT_Y + h + 0.3, 0], [L, K_BAT_Y + h + 1.1, 0])
    through = VGroup(*[Arrow(s, e, buff=0, stroke_width=4, color=GOLD, tip_length=0.2,
                             max_tip_length_to_length_ratio=0.3).set_z_index(3)
                       for s, e in (([xa - 0.42, Tp, 0], [xa + 0.42, Tp, 0]),
                                    ([xb - 0.42, Tp, 0], [xb + 0.42, Tp, 0]),
                                    ([R, K_RC_Y + 0.42, 0], [R, K_RC_Y - 0.42, 0]))])

    bats, res = VGroup(v1, v3, v6), VGroup(ra, rb, rc)
    varrows = VGroup(ar1, ar2, ar3, ar4, ar5, ar6)
    vlabels = VGroup(l1, l2, l3, l4, l5, l6)
    names = VGroup(na, nb, nc)
    g = VGroup(wire, dot, bats, res, varrows, vlabels, names, cur)
    g.wire, g.dot, g.bats, g.res, g.varrows, g.vlabels, g.names, g.current = \
        wire, dot, bats, res, varrows, vlabels, names, cur
    g.through = through
    g.corners = (np.array([L, B, 0]), np.array([L, Tp, 0]), np.array([R, Tp, 0]), np.array([R, B, 0]))
    return g


# ---------------------------------------------------------------------------------------------
# this scene's own pieces
# ---------------------------------------------------------------------------------------------
def _title(text):
    return T(text, 48).move_to([0, 3.3, 0])


# in this scene the six-element loop is drawn smaller and higher, leaving room for the equations
K_SCALE, K_SHIFT = 0.82, np.array([0.0, 0.1, 0.0])


def kp(p):
    """A point of kvl_loop()'s own coordinates, where this scene draws it."""
    return K_SCALE * np.array(p, dtype=float) + K_SHIFT


def _restore(mob):
    """Back to full opacity after set_alpha(mob, 0): set_alpha(mob, 1) can't, as it reads a fill
    already at 0 as an outline. Filled parts (text, signs) get their fill back, strokes theirs."""
    t = mob.copy()
    for leaf in t.family_members_with_points():
        if leaf.get_stroke_width() > 0:
            leaf.set_stroke(opacity=1)
        else:
            leaf.set_fill(opacity=1)
    return Transform(mob, t)


def _pipes(paths):
    return VGroup(*[p.copy().set_stroke(BLUE, 30, opacity=0.25) for p in paths]).set_z_index(-2)


class Water(VGroup):
    """Droplets streaming along the junction's paths: in through two, out through one (twice as dense)."""

    def __init__(self, paths, speed=1.1, gap=0.5):
        self.specs = []
        dots = []
        for k, p in enumerate(paths):
            ln = 0.0
            pts = p.get_anchors()
            for a, b in zip(pts[:-1], pts[1:]):
                ln += np.linalg.norm(b - a)
            g = gap / 2 if k == 2 else gap
            n = int(ln / g)
            for i in range(n):
                d = Dot(radius=0.07, color=BLUE).set_z_index(-1)
                dots.append(d)
                self.specs.append((p, ln, i * ln / n))
        super().__init__(*dots)
        self.speed, self.t = speed, 0.0
        self._place()

    def _place(self):
        for d, (p, ln, s0) in zip(self.submobjects, self.specs):
            s = (s0 + self.speed * self.t) % ln
            d.move_to(p.point_from_proportion(s / ln))

    def _step(self, m, dt):
        self.t += dt
        self._place()

    def start(self):
        self.add_updater(self._step)
        return self


class Kirchhoff(NarratedScene):
    def construct(self):
        self.shot = load_scene("ch6_s6_resistance").handover_shot()
        self.add(self.shot)
        self.kcl_intro()
        self.kcl_slide()
        self.kvl_intro()
        self.kvl_arrows()
        self.kvl_walk()
        self.kvl_numbers()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)

    # -- helper: start a move so that it lands on a cue
    def arrive(self, c, cue, anims, rt=1.3, nth=0):
        lead = c.until(cue, floor=0.0, nth=nth)
        if lead - rt > 0:
            self.wait(lead - rt)
        else:
            rt = max(0.6, lead)
        self.play(*anims, run_time=rt, rate_func=smooth)

    # ---------------------------------------------------------------- clip 1
    def kcl_intro(self):
        shot = self.shot
        self.shot_home = (shot.get_center().copy(), shot.width)
        with self.say("c6.laws.1") as c:
            self.shot_text = [shot[2], shot[4], shot[6], shot[8],
                              shot[0].battery.plus_sign, shot[0].battery.minus_sign]
            self.play(*set_alpha(self.shot_text, 0), run_time=0.8)
            shot.generate_target()
            shot.target.scale(0.26).move_to([5.2, 2.8, 0])
            self.play(MoveToTarget(shot), run_time=1.5)
            c.wait_until("kcl")
            self.title = _title("Kirchhoff's Current Law")
            self.play(*appear(self.title), run_time=1.0)
            c.wait_until("at a junction")
            J = self.J = kcl_junction()
            self.play(*[Create(w) for w in J.wires], GrowFromCenter(J.node), run_time=1.6)
            c.wait_until("node")
            self.play(FlashAround(J.node, run_time=1.2, time_width=1.5, buff=0.12))
            c.wait_until("signs")
            a1, a2, a3 = J.arrows
            self.tag1 = T("+ (in)", 32, GOLD).next_to(a1, UP, buff=0.2)
            self.tag2 = T("+ (in)", 32, GOLD).next_to(a2, DOWN, buff=0.2)
            self.tag3 = T("− (out)", 32, GOLD).next_to(a3, UP, buff=0.2)
            self.play(GrowArrow(a1.arrow), GrowArrow(a2.arrow), run_time=1.0)
            c.wait_until("positive")
            self.play(*appear(self.tag1, self.tag2, lag=0.2), run_time=1.0)
            c.wait_until("flowing out")
            self.play(GrowArrow(a3.arrow), *appear(self.tag3), run_time=min(1.0, c.until(floor=0.3)))

    # ---------------------------------------------------------------- clip 2
    def kcl_slide(self):
        J = self.J
        l1, l2, l3 = J.labels
        with self.say("c6.laws.2", gap=1.0) as c:
            for lab, cue in ((l1, "eye one"), (l2, "eye two"), (l3, "eye three")):
                c.wait_until(cue)
                self.play(*appear(lab), FlashAround(lab, buff=0.1), run_time=0.9)
            c.wait_until("eq")
            eq1 = MathTex("I_1+I_2-I_3=0", font_size=52)
            orr = T("or", 34, DIM)
            eq2 = MathTex("I_1+I_2=I_3", font_size=52)
            row = VGroup(eq1, orr, eq2).arrange(RIGHT, buff=0.7).move_to([0, -2.7, 0])
            self.eq1, self.eq_or, self.eq2 = eq1, orr, eq2
            self.play(*appear(eq1), run_time=1.2)
            c.wait_until("or eye one")
            self.play(*appear(orr, eq2, lag=0.3), run_time=1.2)
            c.wait_until("pipe")
            self.pipes = _pipes(J.paths)
            self.water = Water(J.paths)
            self.play(*disappear(self.tag1, self.tag2, self.tag3),
                      FadeIn(self.pipes), FadeIn(self.water), run_time=1.2)
            self.water.start()
            c.wait_until("example")
            a1, a2, a3 = J.arrows
            v1 = T("2 A", 34, GOLD).move_to(self.tag1)
            v2 = T("3 A", 34, GOLD).move_to(self.tag2)
            v3 = T("5 A", 34, GOLD).move_to(self.tag3)
            self.vals = (v1, v2, v3)
            c.wait_until("two amps")
            self.play(*appear(v1), run_time=0.9)
            c.wait_until("three amps")
            self.play(*appear(v2), run_time=0.9)
            c.wait_until("five amps")
            self.play(*appear(v3), run_time=0.9)
            c.wait_until("check")
            self.check = MathTex("2+3-5=0", font_size=46, color=GOLD).next_to(eq1, DOWN, buff=0.3)
            self.play(*appear(self.check), run_time=1.0)

    # ---------------------------------------------------------------- clip 3
    def kvl_intro(self):
        shot = self.shot
        with self.say("c6.laws.3") as c:
            new_title = _title("Kirchhoff's Voltage Law")
            c.wait_until("the voltage law")
            self.water.clear_updaters()
            sweep_clear(self, time_span(FadeIn(new_title, shift=0.2 * UP), 0.6, 1.2), keep=[shot])
            self.title = new_title
            c.wait_until("the voltages add up")
            self.quote = T("in any closed loop, the sum of all the voltages is zero", 28).move_to([0, -3.3, 0])
            self.play(*appear(self.quote), run_time=1.0)
            c.wait_until("ours")
            home, w = self.shot_home
            shot.generate_target()
            # back near s6's own size (labels read at 28)
            shot.target.scale(0.88 * w / shot.width).set_x(0)
            shot.target.shift(UP * (2.75 - shot.target.get_top()[1]))
            self.play(MoveToTarget(shot), run_time=1.5)
            self.play(*[_restore(m) for m in self.shot_text], run_time=0.8)
            ours = MathTex("+1.5", "-1.5", "=0", font_size=48).move_to([0, -2.7, 0])
            self.ours = ours
            c.wait_until("the battery gives")
            self.play(FlashAround(shot[4], buff=0.1), *appear(ours[0]), run_time=1.0)
            c.wait_until("the resistor takes")
            self.play(FlashAround(shot[6], buff=0.1), *appear(ours[1]), run_time=1.0)
            c.wait_until("so the total is zero")
            self.play(*appear(ours[2]), run_time=1.0)
            c.wait_until("grow")
            # the loop grows into p. 170's
            small = self.title.copy().scale(30 / 48).move_to([0, 3.3, 0])
            self.play(*disappear(self.quote, self.ours, shot[2], shot[4], shot[6], shot[8]),
                      *during([Transform(self.title, small)], 0.3, 1.0), run_time=1.1)
            K = self.K = kvl_loop()
            K.scale(K_SCALE, about_point=ORIGIN).shift(K_SHIFT)
            K.through.scale(K_SCALE, about_point=ORIGIN).shift(K_SHIFT)
            K.corners = tuple(kp(q) for q in K.corners)
            loop, r, va, vr, ca = shot[0], shot[1], shot[3], shot[5], shot[7]
            new_parts = [K.dot, K.bats[1], K.bats[2], K.res[0], K.res[1],
                         K.varrows[1], K.varrows[2], K.varrows[3], K.varrows[5]]
            # the sides stretch first (each half of the old wire onto the same-shaped half of the
            # new outline, so nothing crosses), then the new elements open their gaps in the wire
            h, rs = S2.BAT_H / 2, S2.SLOT_H / 2
            lower_t = VMobject().set_points_as_corners(
                [kp([KL, K_BAT_Y - h, 0]), kp([KL, KB, 0]), kp([KR, KB, 0]), kp([KR, K_RC_Y - rs, 0])])
            upper_t = VMobject().set_points_as_corners(
                [kp([KR, K_RC_Y + rs, 0]), kp([KR, KT, 0]), kp([KL, KT, 0]), kp([KL, K_BAT_Y + h, 0])])
            VGroup(lower_t, upper_t).set_stroke(FG, WIRE_W)
            self.play(ReplacementTransform(loop.lower, lower_t),
                      ReplacementTransform(loop.upper, upper_t),
                      ReplacementTransform(loop.battery, K.bats[0]),
                      ReplacementTransform(r, K.res[2]),
                      ReplacementTransform(va, K.varrows[0]),
                      ReplacementTransform(vr, K.varrows[4]),
                      ReplacementTransform(ca, K.current),
                      run_time=1.2)
            moved = [K.bats[0], K.res[2], K.varrows[0], K.varrows[4], K.current]
            self.remove(*shot.get_family())
            self.add(*moved)
            self.play(FadeOut(lower_t), FadeOut(upper_t), FadeIn(K.wire),
                      *[FadeIn(m, shift=0.25 * DOWN) for m in new_parts], run_time=1.0)
            settle(self, K, drop=[K.vlabels, K.names])

    # ---------------------------------------------------------------- clip 4
    def kvl_arrows(self):
        K = self.K
        with self.say("c6.laws.4") as c:
            self.play(*appear(*K.vlabels, lag=0.1), *flash(list(K.varrows), color=TEAL),
                      run_time=1.6)
            c.wait_until("batteries")
            b_ar = [K.varrows[0], K.varrows[2], K.varrows[5]]
            self.play(*[FlashAround(a.arrow.tip, buff=0.08) for a in b_ar],
                      *[FlashAround(b.plus_sign, buff=0.08) for b in K.bats], run_time=1.5)
            c.wait_until("choose")
            self.play(*appear(*K.names, lag=0.15), run_time=1.0)
            self.play(FlashAround(K.current, color=GOLD, time_width=1.5), run_time=1.5)
            c.wait_until("clockwise")
            self.tag = T("chosen: clockwise", 32, GOLD)
            self.tag.move_to(kp([KL + 1.2, K_BAT_Y + 0.65, 0]), aligned_edge=LEFT)
            self.play(*appear(self.tag), FlashAround(K.current, color=GOLD), run_time=1.2)
            c.wait_until("resistors")
            r_ar = [K.varrows[1], K.varrows[3], K.varrows[4]]
            self.play(*[GrowArrow(a) for a in K.through], run_time=1.2)
            self.play(*[FlashAround(a.arrow.tip, buff=0.08) for a in r_ar], run_time=1.3)

    # ---------------------------------------------------------------- clip 5
    def kvl_walk(self):
        K = self.K
        bl, tl, tr, br = K.corners
        walker = Dot(bl, radius=0.14, color=YELLOW).set_z_index(5)
        eq = self.eq = MathTex("V_1", "-V_2", "-V_3", "-V_4", "-V_5", "+V_6", "=0",
                               font_size=52, color=TEAL).move_to([0, -2.45, 0])
        eq[-1].set_color(FG)
        with self.say("c6.laws.5") as c:
            self.play(FadeIn(walker, scale=0.5), run_time=1.0)
            self.play(walker.animate.move_to(kp([KL, K_BAT_Y - 0.65, 0])), run_time=1.5)
            c.wait_until("rule")
            self.play(*disappear(self.tag), run_time=0.7)
            k1 = T("arrow with you:  +", 32)
            k2 = T("arrow against you:  −", 32)
            VGroup(k1, k2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, 0.4, 0])
            self.key = VGroup(k1, k2)
            c.wait_until("points the way")
            self.play(*appear(k1), run_time=1.0)
            c.wait_until("against you")
            self.play(*appear(k2), run_time=1.0)

            def step(cue, to, i, rt=1.3, nth=0):
                self.arrive(c, cue, [walker.animate.move_to(to)], rt=rt, nth=nth)
                self.play(*appear(eq[i], shift=0.25 * DOWN),
                          FlashAround(K.varrows[i], color=TEAL, buff=0.1), run_time=0.9)

            step("plus vee one", tl, 0, rt=1.6)
            step("minus vee two", kp([-1.3, KT, 0]), 1, rt=1.6)
            step("minus vee three", kp([1.15, KT, 0]), 2, rt=1.0)
            step("minus vee four", tr, 3, rt=1.0)
            step("minus vee five", br, 4, rt=1.4)
            step("plus vee six", kp([-1.0, KB, 0]), 5, rt=1.4)
            c.wait_until("zero")
            self.play(walker.animate.move_to(bl), *appear(eq[6]), run_time=1.2)
            self.play(FadeOut(walker), FlashAround(eq, buff=0.15), run_time=1.2)

    # ---------------------------------------------------------------- clip 6
    def kvl_numbers(self):
        K, eq = self.K, self.eq
        l1, l2, l3, l4, l5, l6 = K.vlabels
        na, nb, nc = K.names

        def val(text, color=TEAL):
            return T(text, 30, color)
        bv1 = val("= 5 V").next_to(l1, DOWN, buff=0.18)
        bv3 = val("= 1 V").next_to(l3, RIGHT, buff=0.12)
        bv6 = val("= 2 V").next_to(l6, DOWN, buff=0.18)
        ra = val("1 Ω", FG).next_to(na, DOWN, buff=0.15)
        rb = val("2 Ω", FG).next_to(nb, DOWN, buff=0.15)
        rc = val("3 Ω", FG).next_to(nc, DOWN, buff=0.15)
        amp = val("1 A", GOLD).next_to(K.current, LEFT, buff=0.2)
        v2 = val("= 1 V").next_to(l2, RIGHT, buff=0.12)
        v4 = val("= 2 V").next_to(l4, RIGHT, buff=0.12)
        v5 = val("= 3 V").next_to(l5, DOWN, buff=0.18)
        with self.say("c6.laws.6") as c:
            self.play(*disappear(self.key), run_time=0.8)
            c.wait_until("five")
            self.play(*appear(bv1, bv3, bv6, lag=0.5), run_time=1.8)
            c.wait_until("one", nth=1)
            self.play(*appear(ra, rb, rc, lag=0.5, shift=None), run_time=1.8)
            c.wait_until("one amp")
            self.play(*appear(amp), FlashAround(K.current, color=GOLD), run_time=1.0)
            c.wait_until("ohm")
            prod = T("1 A × 1 Ω", 30, GOLD).move_to([-1.25, 0.15, 0])
            eqv = T("1 V", 30, TEAL).next_to(prod, RIGHT, buff=0.4)
            self.play(*appear(prod, eqv, lag=0.3), run_time=0.8)
            c.wait_until("one two", nth=1)
            v2eq = T("=", 30, TEAL).move_to(v2[0])
            self.play(eqv.animate(path_arc=-PI / 2).move_to(v2[1:]), *during(appear(v2eq), 0.6, 1.0),
                      *during(disappear(prod), 0.5, 1.0), run_time=1.4)
            self.play(*appear(v4, v5, lag=0.4), run_time=1.2)
            c.wait_until("add")
            nums = VGroup(*[MathTex(s, font_size=46).move_to([eq[i].get_x(), -3.08, 0])
                            for i, s in enumerate(["5", "-1", "-1", "-2", "-3", "+2"])])
            rt = min(4.4, c.until("result"))
            self.play(*appear(*nums, lag=0.6, shift=0.15 * DOWN), run_time=rt)
            c.wait_until("result")
            res = MathTex("=0", font_size=46, color=GOLD).move_to([eq[6].get_x(), -3.08, 0])
            self.play(*appear(res), FlashAround(res, color=GOLD, buff=0.1), run_time=1.0)
            c.wait_until("negative")
            tag = VGroup(T("negative answer:", 32, GOLD), T("it flows the other way", 32, GOLD)
                         ).arrange(DOWN, buff=0.2).move_to([-0.1, 0.3, 0])
            ghost = K.current.copy().set_opacity(0.55)
            self.add(ghost)
            self.play(ghost.animate.shift(0.75 * RIGHT), run_time=0.8)
            c.wait_until(own_word=tag[0])
            self.play(*appear(*tag, lag=0.3), run_time=1.0)
            self.play(Rotate(ghost, PI), run_time=min(1.2, c.until(floor=0.5)))
        self.wait(3.5)
