"""Chapter 5, scene 5: cosine and sine draw circles and ellipses. Clips c5.param.1 – c5.param.4.

Visuals defined here (import with load_scene("ch5_s5_param")):
- circle_ellipse_pair(theta=0.7, eqs=True): left, the BLUE circle (YELLOW centre (x₀, y₀) with dashed
  drops to DIM axes, GOLD radius r at angle θ from a dashed horizontal); right, the BLUE ellipse
  (GOLD a, GREEN b); one θ dial between them drives both running points (`.theta`, a ValueTracker,
  not in the group). With eqs: x = x₀ + r cos θ, y = y₀ + r sin θ, 0 ≤ θ < 2π under the circle and
  x = x₀ + a cos θ, y = y₀ + b sin θ under the ellipse. The group can be moved/scaled freely.
- unit_hyperbola_shot(theta=0.6): the final shot: ch1 s1's circle_hyperbola_pair, the unit circle with
  (cos θ, sin θ), x = cos θ, y = sin θ and cos²θ + sin²θ = 1 under it, the hyperbola dimmed with
  (cosh θ, sinh θ), "Part 6" under it.
"""
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

S1 = load_scene("ch1_s1_hook")

UNIT = 1.45
EQ = 48


def _guard(mob, fn):
    """Updater acting on the on-screen original only (copies made by Transforms share the function)."""
    def u(m):
        if m is mob:
            fn(m)
    mob.add_updater(u)
    fn(mob)
    return mob


def _dir(t):
    return np.array([np.cos(t), np.sin(t), 0.0])


def _eq(parts, colors, size=EQ):
    m = MathTex(*parts, font_size=size)
    for i, col in colors.items():
        m[i].set_color(col)
    return m


# ---------------------------------------------------------------- (a) circle + ellipse + dial

def circle_ellipse_pair(theta=0.7, unit=UNIT, eqs=True):
    th = ValueTracker(theta)
    C = np.array([-3.4, 1.5, 0.0])
    E = np.array([3.4, 1.5, 0.0])
    O = np.array([-6.0, -0.4, 0.0])

    # ---- circle side
    axes = VGroup(Line(O, np.array([-1.3, O[1], 0])), Line(O, np.array([O[0], 3.3, 0]))).set_stroke(DIM, 2)
    circle = Circle(radius=unit).move_to(C).set_stroke(BLUE, 4)
    centre = Dot(C, radius=0.08, color=YELLOW).set_z_index(3)
    drop_x = DashedLine(C, np.array([C[0], O[1], 0]), dash_length=0.1).set_stroke(DIM, 2)
    drop_y = DashedLine(C, np.array([O[0], C[1], 0]), dash_length=0.1).set_stroke(DIM, 2)
    x0 = MathTex("x_0", font_size=34, color=YELLOW).next_to(np.array([C[0], O[1], 0]), DOWN, buff=0.15)
    y0 = MathTex("y_0", font_size=34, color=YELLOW).next_to(np.array([O[0], C[1], 0]), LEFT, buff=0.15)
    ref = DashedLine(C, C + (unit + 0.35) * RIGHT, dash_length=0.1).set_stroke(DIM, 2)

    def k():
        return circle.width / 2 / unit

    def cpt():
        return circle.get_center() + circle.width / 2 * _dir(th.get_value())

    radius = Line(C, cpt()).set_stroke(GOLD, 4)
    _guard(radius, lambda m: m.put_start_and_end_on(circle.get_center(), cpt()))
    r_lab = MathTex("r", font_size=36, color=GOLD)
    _guard(r_lab, lambda m: m.move_to(circle.get_center() + 0.5 * circle.width / 2 * _dir(th.get_value())
                                      + 0.3 * k() * _dir(th.get_value() + PI / 2)))

    def arc_fn(m):
        t = th.get_value() % TAU
        m.become(Arc(radius=0.4 * k(), start_angle=0, angle=max(t, 1e-3),
                     arc_center=circle.get_center()).set_stroke(GOLD, 3))
    t_arc = Arc(radius=0.4, angle=0.5)
    _guard(t_arc, arc_fn)
    t_lab = MathTex(r"\theta", font_size=32, color=GOLD)
    _guard(t_lab, lambda m: m.move_to(circle.get_center() + 0.68 * k() * _dir((th.get_value() % TAU) / 2)))
    cdot = Dot(cpt(), radius=0.09, color=FG).set_z_index(3)
    _guard(cdot, lambda m: m.move_to(cpt()))

    # ---- ellipse side (a = 2, b = 1 in the circle's units)
    ellipse = Ellipse(width=4 * unit, height=2 * unit).move_to(E).set_stroke(BLUE, 4)
    ecentre = Dot(E, radius=0.08, color=YELLOW).set_z_index(3)
    a_seg = Line(E, E + 2 * unit * RIGHT).set_stroke(GOLD, 4)
    b_seg = Line(E, E + unit * UP).set_stroke(GREEN, 4)
    a_lab = MathTex("a", font_size=36, color=GOLD).next_to(a_seg, DOWN, buff=0.12)
    b_lab = MathTex("b", font_size=36, color=GREEN).next_to(b_seg, LEFT, buff=0.12)

    def ept():
        t = th.get_value()
        return ellipse.get_center() + np.array([ellipse.width / 2 * np.cos(t), ellipse.height / 2 * np.sin(t), 0])

    edot = Dot(ept(), radius=0.09, color=FG).set_z_index(3)
    _guard(edot, lambda m: m.move_to(ept()))

    # ---- the dial
    D = np.array([0.0, -2.0, 0.0])
    ring = Circle(radius=0.5).move_to(D).set_stroke(DIM, 3)
    hub = Dot(D, radius=0.05, color=FG)
    needle = Line(D, D + 0.42 * RIGHT).set_stroke(FG, 4)
    _guard(needle, lambda m: m.put_start_and_end_on(ring.get_center(),
                                                     ring.get_center() + 0.84 * ring.width / 2 * _dir(th.get_value())))
    d_lab = MathTex(r"\theta", font_size=36, color=GOLD).next_to(ring, DOWN, buff=0.15)
    dial = VGroup(ring, needle, hub, d_lab)

    circle_panel = VGroup(axes, drop_x, drop_y, x0, y0, circle, ref, centre)
    circle_arm = VGroup(radius, r_lab, t_arc, t_lab)
    ellipse_panel = VGroup(ellipse, a_seg, b_seg, a_lab, b_lab, ecentre)
    g = VGroup(circle_panel, circle_arm, cdot, ellipse_panel, edot, dial)
    g.circle_panel, g.circle_arm, g.ellipse_panel, g.dial = circle_panel, circle_arm, ellipse_panel, dial
    g.axes, g.circle, g.centre, g.drops, g.x0, g.y0, g.ref = axes, circle, centre, VGroup(drop_x, drop_y), x0, y0, ref
    g.radius, g.r_lab, g.t_arc, g.t_lab, g.cdot = radius, r_lab, t_arc, t_lab, cdot
    g.ellipse, g.ecentre, g.ab, g.edot = ellipse, ecentre, VGroup(a_seg, b_seg, a_lab, b_lab), edot
    g.theta = th
    g.updated = [radius, r_lab, t_arc, t_lab, cdot, edot, needle]

    if eqs:
        cx = _eq(["x", "=", "x_0", "+", "r", r"\cos\theta"], {2: YELLOW, 4: GOLD})
        cy = _eq(["y", "=", "y_0", "+", "r", r"\sin\theta"], {2: YELLOW, 4: GOLD})
        ex = _eq(["x", "=", "x_0", "+", "a", r"\cos\theta"], {2: YELLOW, 4: GOLD})
        ey = _eq(["y", "=", "y_0", "+", "b", r"\sin\theta"], {2: YELLOW, 4: GREEN})
        for top, bot, x in ((cx, cy, C[0]), (ex, ey, E[0])):
            top.move_to(np.array([x, -1.55, 0]))
            bot.move_to(np.array([x, -2.45, 0]))
            bot.shift((top[1].get_x() - bot[1].get_x()) * RIGHT)
        rng = MathTex(r"0 \le \theta < 2\pi", font_size=40).move_to(np.array([C[0], -3.3, 0]))
        g.cx, g.cy, g.ex, g.ey, g.rng = cx, cy, ex, ey, rng
        g.add(cx, cy, rng, ex, ey)
    return g


# ---------------------------------------------------------------- (b) the closing shot

def unit_hyperbola_shot(theta=0.6):
    pair = S1.circle_hyperbola_pair(unit=1.4, theta=theta)
    pair.shift(0.4 * UP)
    cx = pair.circle.get_x()
    par = MathTex(r"x = \cos\theta,\quad y = \sin\theta", font_size=40).move_to(np.array([cx, -2.35, 0]))
    ident = MathTex(r"\cos^2\theta + \sin^2\theta = 1", font_size=40).move_to(np.array([cx, -3.1, 0]))
    hyper = pair.hyper_panel
    for m in (pair.h_axes, pair.right, pair.left):
        m.set_stroke(opacity=0.45)
    pair.h_eq.set_fill(opacity=0.45)
    pair.hdot.set_opacity(0.45)
    pair.hlabel.tex.set_fill(opacity=0.45)
    part6 = T("Part 6", size=32, color=DIM).move_to(np.array([pair.h_origin.get_x(), -2.6, 0]))
    shot = VGroup(pair, par, ident, part6)
    shot.pair, shot.par, shot.ident, shot.part6, shot.hyper = pair, par, ident, part6, hyper
    shot.theta = pair.theta
    return shot


# ---------------------------------------------------------------- parameter vs angle view

def _readout(val, color, left, size=42):
    """A degrees read-out 'ddd.d°' built from fixed digit slots (each slot holds the ten digits, one
    visible): glyphs never move or get rebuilt, so nothing slides across the label beside it."""
    tpl = MathTex("0", "0", "0", ".", "0", r"^\circ", font_size=size, color=color)
    tpl.move_to(left, aligned_edge=LEFT)
    slots = []
    for k in (0, 1, 2, 4):
        slots.append([MathTex(str(d), font_size=size, color=color).move_to(tpl[k]) for d in range(10)])
    fixed = VGroup(tpl[3].copy(), tpl[5].copy())
    g = VGroup(*[m for sl in slots for m in sl], fixed)

    def u(m):
        tenths = int(round(val() * 10)) % 3600
        ds = [tenths // 1000, tenths // 100 % 10, tenths // 10 % 10, tenths % 10]
        for i, (sl, d) in enumerate(zip(slots, ds)):
            lead = (i == 0 and tenths < 1000) or (i == 1 and tenths < 100)
            for j, mob in enumerate(sl):
                mob.set_fill(opacity=1.0 if (j == d and not lead) else 0.0)
    _guard(g, u)
    return g


def angle_view(theta=PI / 4, unit=1.45, centre=np.array([-1.6, 0.3, 0.0])):
    th = ValueTracker(theta)
    A, B = 2 * unit, unit
    aux = DashedVMobject(Circle(radius=A).move_to(centre), num_dashes=70).set_stroke(DIM, 2)
    ellipse = Ellipse(width=2 * A, height=2 * B).move_to(centre).set_stroke(BLUE, 4)
    cdot = Dot(centre, radius=0.08, color=YELLOW).set_z_index(3)
    ref = DashedLine(centre, centre + (A + 0.3) * RIGHT, dash_length=0.1).set_stroke(DIM, 2)

    def q():
        return centre + A * _dir(th.get_value())

    def p():
        t = th.get_value()
        return centre + np.array([A * np.cos(t), B * np.sin(t), 0])

    def phi():
        t = th.get_value()
        f = np.arctan2(B * np.sin(t), A * np.cos(t))
        return t + ((f - t + PI) % TAU - PI)

    rad = _guard(Line(centre, q()).set_stroke(GOLD, 4), lambda m: m.put_start_and_end_on(centre, q()))
    qdot = _guard(Dot(q(), radius=0.07, color=GOLD).set_z_index(3), lambda m: m.move_to(q()))
    t_arc = Arc(radius=1.1, angle=0.5)
    _guard(t_arc, lambda m: m.become(Arc(radius=1.1, angle=max(th.get_value() % TAU, 1e-3),
                                         arc_center=centre).set_stroke(GOLD, 3)))
    t_lab = MathTex(r"\theta", font_size=34, color=GOLD)
    _guard(t_lab, lambda m: m.move_to(centre + 1.42 * _dir((th.get_value() % TAU) / 2)))

    def drop_fn(m):
        a, b = q(), p()
        if np.linalg.norm(a - b) < 0.05:
            b = a + 0.001 * DOWN
        m.become(DashedLine(a, b, dash_length=0.08).set_stroke(FG, 2))
    drop = _guard(DashedLine(q(), p() + 0.01 * DOWN), drop_fn)
    pdot = _guard(Dot(p(), radius=0.09, color=FG).set_z_index(3), lambda m: m.move_to(p()))
    true = _guard(Line(centre, p()).set_stroke(YELLOW, 4), lambda m: m.put_start_and_end_on(centre, p()))
    f_arc = Arc(radius=0.6, angle=0.5)
    _guard(f_arc, lambda m: m.become(Arc(radius=0.6, angle=max(phi() % TAU, 1e-3),
                                         arc_center=centre).set_stroke(YELLOW, 3)))

    # read-outs (right)
    r1a = MathTex(r"\theta =", font_size=42, color=GOLD)
    r2a = T("angle =", size=38, color=YELLOW)
    r1a.move_to(np.array([3.35, 1.1, 0]), aligned_edge=RIGHT)
    r2a.move_to(np.array([3.35, 0.0, 0]), aligned_edge=RIGHT)
    r1b = _readout(lambda: np.degrees(th.get_value()), GOLD, np.array([3.6, r1a.get_y(), 0]))
    r2b = _readout(lambda: np.degrees(phi()), YELLOW, np.array([3.6, r2a.get_y(), 0]))
    row1 = VGroup(r1a, r1b)
    row2 = VGroup(r2a, r2b)
    cap = VGroup(MathTex(r"\theta", font_size=40), T("is a parameter, not the angle", size=36))
    cap.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to(np.array([0.0, -3.3, 0]))

    v = VGroup(aux, ellipse, ref, cdot)
    v.aux, v.ellipse, v.ref, v.cdot = aux, ellipse, ref, cdot
    v.param = VGroup(rad, t_arc, t_lab, qdot)
    v.stretch = VGroup(drop, pdot)
    v.true = VGroup(true, f_arc)
    v.row1, v.row2, v.cap = row1, row2, cap
    v.theta = th
    v.updated = [rad, qdot, t_arc, t_lab, drop, pdot, true, f_arc, r1b, r2b]
    return v


def _freeze(mobs):
    for m in mobs:
        m.clear_updaters()


# ---------------------------------------------------------------- the scene

class ParamScene(NarratedScene):
    def construct(self):
        g = circle_ellipse_pair()
        th = g.theta
        self.add(th)

        # ---- c5.param.1: the circle, its equations, the point goes round
        with self.say("c5.param.1") as c:
            self.play(*appear(g.axes, g.circle, lag=0.3, shift=None), run_time=1.4)
            self.play(*appear(g.centre, g.drops, g.x0, g.y0, lag=0.2), run_time=1.2)  # early: the centre's coordinates, named in the next line
            c.wait_until("fx")
            self.play(*appear(g.ref, g.radius, g.cdot, g.t_arc, g.r_lab, g.t_lab, lag=0.15, shift=None),
                      run_time=1.2)
            self.play(*appear(g.cx), run_time=1.0)
            c.wait_until("fy")
            self.play(*appear(g.cy), run_time=1.0)
            c.wait_until("run")
            self.play(*appear(g.rng), run_time=0.8)
            self.play(th.animate.set_value(0.7 + TAU), rate_func=linear,
                      run_time=min(4.0, c.until("polar", floor=1.0) - 0.1))
            th.set_value(0.7)
            c.wait_until("polar")
            self.play(*flash([g.radius, g.t_arc], color=GOLD, run_time=1.5, time_width=1.5))

        # ---- c5.param.2: the check, then the ellipse
        with self.say("c5.param.2") as c:
            lhs = _eq([r"(x-", "x_0", r")^2+(y-", "y_0", r")^2"], {1: YELLOW, 3: YELLOW}, size=48)
            l1 = _eq(["=", "r^2", r"\cos^2\theta", "+", "r^2", r"\sin^2\theta"], {1: GOLD, 4: GOLD}, size=48)
            l2 = _eq(["=", "r^2", "(", r"\cos^2\theta", "+", r"\sin^2\theta", ")"], {1: GOLD}, size=48)
            l2b = _eq(["=", "r^2", r"\cdot", "1"], {1: GOLD, 3: GREEN}, size=48)
            l3 = _eq(["=", "r^2"], {1: GOLD}, size=48)
            lhs.move_to(np.array([3.4, 2.4, 0]))
            x_eq = lhs.get_left()[0] + 0.5
            for m, y in ((l1, 1.45), (l2, 0.5), (l2b, 0.5), (l3, 0.5)):
                m.move_to(np.array([0, y, 0])).shift((x_eq - m.get_left()[0]) * RIGHT)

            self.play(*appear(lhs), run_time=1.2)
            c.wait_until("square and add")
            self.play(*appear(l1), run_time=1.2)
            c.wait_until("sum")
            derive(self, l1, l2)
            c.wait_until("one")
            bracket = VGroup(*l2[2:7])
            box = SurroundingRectangle(bracket, color=YELLOW, buff=0.1).set_z_index(-1)
            self.play(GrowFromCenter(box), run_time=0.8)
            c.wait_until("is one")
            box2 = SurroundingRectangle(l2b[3], color=YELLOW, buff=0.1).set_z_index(-1)
            self.play(*edit(l2, l2b), Transform(box, box2), run_time=1.2)
            c.wait_until("so you get")
            self.play(*edit(l2b, l3), FadeOut(box), run_time=1.2)
            self.play(FlashAround(l3, color=GREEN, run_time=1.2, time_width=1.5))

            c.wait_until("ell")
            # the finished check shrinks into the bottom-right corner (it stays readable until {efx})
            done = VGroup(lhs.copy(), l3.copy()).scale(0.65)
            done.arrange(RIGHT, buff=0.15, aligned_edge=DOWN).move_to(np.array([3.4, -3.3, 0]))
            lhs.generate_target()
            lhs.target.become(done[0])
            l3.generate_target()
            l3.target.become(done[1])
            self.play(*during(disappear(l1), 0, 0.35),
                      *during([MoveToTarget(lhs), MoveToTarget(l3)], 0.3, 0.75),
                      *during(appear(g.ellipse, g.ecentre, g.edot, shift=None, lag=0.2), 0.6, 1.0), run_time=2.2)
            self.play(*appear(g.ab, lag=0.2, shift=None), run_time=1.2)
            c.wait_until("efx")
            self.play(*during(disappear(lhs, l3), 0, 0.45), *during(appear(g.ex), 0.4, 1.0), run_time=1.4)
            c.wait_until("efy")
            self.play(*appear(g.ey), run_time=1.0)
            self.play(*appear(g.dial, shift=None), run_time=0.8)
            self.play(th.animate.set_value(0.7 + TAU), rate_func=linear, run_time=c.until(floor=1.0) - 0.1)
            th.set_value(0.7)

        # ---- c5.param.3: the ellipse check; parameter versus angle
        with self.say("c5.param.3") as c:
            echeck = _eq([r"\Big(\frac{x-", "x_0", "}{", "a", r"}\Big)^2+\Big(\frac{y-", "y_0", "}{", "b",
                          r"}\Big)^2=1"], {1: YELLOW, 3: GOLD, 5: YELLOW, 7: GREEN}, size=34)
            echeck.move_to(np.array([3.4, -3.25, 0]))
            self.play(*appear(echeck), run_time=1.2)
            c.wait_until("warn")

            v = angle_view()
            _freeze(g.updated)
            old = [m for m in self.mobjects if m not in (g.ellipse, g.ecentre, th, echeck)]
            echeck.generate_target()
            echeck.target.scale(0.85).move_to(np.array([4.5, 3.35, 0]))
            self.play(*during(disappear(*old), 0, 0.45),
                      *during([MoveToTarget(echeck)], 0.45, 1.0),
                      *during([ReplacementTransform(g.ellipse, v.ellipse),
                               ReplacementTransform(g.ecentre, v.cdot)], 0.2, 0.85),
                      *during(appear(v.aux, v.ref, shift=None), 0.6, 1.0), run_time=1.8)
            c.wait_until(own_word=v.cap[1])
            self.play(*appear(v.cap), run_time=1.0)
            c.wait_until("on the circle")
            self.play(*appear(v.param, v.row1, lag=0.2, shift=None), run_time=1.2)
            c.wait_until("stretch")
            self.play(*appear(v.stretch, lag=0.3, shift=None), run_time=1.0)
            c.wait_until("angle")
            self.play(*appear(v.true, v.row2, lag=0.3, shift=None), run_time=1.2)
            c.wait_until("drift")
            self.play(v.theta.animate.set_value(TAU), rate_func=linear, run_time=c.until(floor=1.0) - 0.1)

        # ---- c5.param.4: back to the unit circle, then the hyperbola beside it
        with self.say("c5.param.4", gap=0.6) as c:
            shot = unit_hyperbola_shot()
            pair = shot.pair
            uth = shot.theta
            self.add(uth)
            dx = -pair.circle.get_x()
            left_side = [pair.circle_panel, shot.par, shot.ident]
            for m in left_side:
                m.shift(dx * RIGHT)
            pair.clabel.update()
            pair.cdot.update()
            _freeze(v.updated)
            gone = [m for m in self.mobjects if m is not uth and isinstance(m, VMobject)]
            # the old view is fully gone before the unit circle arrives in the same place
            self.play(*during(disappear(*gone), 0, 0.4),
                      *during(appear(pair.circle_panel, pair.cdot, pair.clabel, lag=0.3, shift=None), 0.5, 1.0),
                      run_time=2.2)
            self.remove(*gone)
            c.wait_until("the point is")
            self.play(*appear(shot.par, shot.ident, lag=0.6), run_time=1.6)
            c.wait_until("draw")
            self.play(uth.animate.set_value(0.6 + TAU), rate_func=linear,
                      run_time=min(3.2, c.until("next", floor=1.0) - 0.1))
            uth.set_value(0.6)
            c.wait_until("next")
            self.play(*[m.animate.shift(dx * LEFT) for m in left_side],
                      *during(appear(pair.hyper_panel, pair.hdot, pair.hlabel, shift=None, lag=0.2), 0.45, 1.0),
                      run_time=1.8)
            c.wait_until(own_word=shot.part6)
            self.play(*appear(shot.part6), run_time=1.0)
            rest = c.until(floor=2.0) - 0.2
            self.play(uth.animate.set_value(1.1), run_time=0.35 * rest)
            self.play(uth.animate.set_value(-0.8), run_time=0.4 * rest)
            self.play(uth.animate.set_value(0.6), run_time=0.25 * rest)

        for m in (pair.cdot, pair.hdot, pair.clabel, pair.hlabel):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects if isinstance(m, VMobject)], run_time=1.0)
        self.remove(uth)
        self.wait(0.15)
