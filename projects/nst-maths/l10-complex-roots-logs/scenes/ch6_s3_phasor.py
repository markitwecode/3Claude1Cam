"""Chapter 6, scene 3: the turning arrow and its shadow. Clips c6.arrow.1 – c6.arrow.5.

Shared visuals for chapter 6 (import with load_scene("ch6_s3_phasor")):
  pendulum(theta, pivot, length, s, labels)  hatched ceiling, DIM dashed vertical, rod l, bob m, g
                                             (labels in `.labels`, not part of the group)
  inset_pendulum(phase)                      the small top-right pendulum, in step with `phase`
  argand_plane()                             Re/Im axes + DIM grid, centre P0, unit U
  phasor_arrow(phase), omega_marker(phase), shadow(phase), shadow_label(phase), trail_arc(a0, a1)
  x_graph()                                  s2's BLUE x(t) graph on t/x axes (origin G0, K_T per s)
  Clock                                      scene clock: phase = PHI0 + OMEGA t (+ smooth warps)
  handover_shot()                            this scene's last frame (arrow at PHI0)
"""
# style: 2
# handover: next
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, FlashUnder, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         select, set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---------------------------------------------------------------- running example and layout
OMEGA = PI / 2                 # one turn = one swing = 4 s
PHI0 = -PI / 3                 # arg A
A_MOD = 2.0                    # |A|  (A = 1 - i sqrt3, c = 1)
PEND_AMP = 20 * DEGREES        # pendulum angle = PEND_AMP cos(phase)
P0 = np.array([-3.3, -0.25, 0.0])   # Argand origin
U = 0.95                       # screen units per plane unit
EXT = 3.4                      # plane extent (fits s4's velocity arrow, length pi)
R = A_MOD * U                  # circle radius on screen
FULL_PIVOT = np.array([-3.4, 2.9, 0.0])
FULL_L = 3.6
INSET_PIVOT = np.array([5.55, 3.55, 0.0])
INSET_L = 1.45
INSET_S = 0.6
G0 = np.array([0.9, -0.6, 0.0])     # s2's graph origin
K_T = 0.4                      # graph: screen units per second of t
T_MAX = 12.0


def ang(t):
    return np.array([np.cos(t), np.sin(t), 0.0])


_TEX = {}


def _tex(src, size, color):
    key = (src, size, color)
    if key not in _TEX:
        _TEX[key] = MathTex(src, font_size=size, color=color)
    return _TEX[key].copy()


# ---------------------------------------------------------------- shared builders
def pendulum(theta=PEND_AMP * 0.5, pivot=FULL_PIVOT, length=FULL_L, s=1.0, labels=True):
    """The margin-sketch pendulum. Returns the geometry VGroup (ceiling, hatch, vertical, rod, bob);
    the l / m / g labels are in `.labels` (add them separately). theta > 0: bob to the right."""
    pivot = np.array(pivot, dtype=float)
    w = 0.85 * s
    ceiling = Line(pivot + LEFT * w, pivot + RIGHT * w, color=FG, stroke_width=3)
    hatch = VGroup(*[Line(pivot + RIGHT * x, pivot + RIGHT * (x + 0.2 * s) + UP * 0.2 * s,
                          color=DIM, stroke_width=2) for x in np.linspace(-w, w - 0.2 * s, 8)])
    vertical = DashedLine(pivot, pivot + DOWN * length * 1.08, color=DIM, stroke_width=2,
                          dash_length=0.12 * s)
    bob_pt = pivot + length * np.array([np.sin(theta), -np.cos(theta), 0.0])
    rod = Line(pivot, bob_pt, color=FG, stroke_width=4 if s >= 0.9 else 3)
    bob = Circle(radius=0.22 * s, color=FG, stroke_width=2).set_fill(FG, 1).move_to(bob_pt)
    g = VGroup(ceiling, hatch, vertical, rod, bob)
    g.ceiling, g.hatch, g.vertical, g.rod, g.bob = ceiling, hatch, vertical, rod, bob
    g.labels = VGroup()
    if labels:
        n = np.array([np.cos(theta), np.sin(theta), 0.0])        # right-hand normal to the rod
        l_lbl = MathTex("l", font_size=36, color=FG).move_to((pivot + bob_pt) / 2 + 0.32 * n)
        m_lbl = MathTex("m", font_size=36, color=FG).move_to(bob_pt + 0.55 * n)
        g_start = bob_pt + RIGHT * 1.15 + UP * 0.35
        g_arrow = Arrow(g_start, g_start + DOWN * 0.75, buff=0, stroke_width=3, color=FG,
                        tip_length=0.18, max_tip_length_to_length_ratio=0.3)
        g_lbl = MathTex("g", font_size=36, color=FG).next_to(g_arrow, RIGHT, buff=0.15)
        g.labels = VGroup(l_lbl, m_lbl, g_arrow, g_lbl)
    return g


def inset_pendulum(phase):
    return pendulum(PEND_AMP * np.cos(phase), INSET_PIVOT, INSET_L, s=INSET_S, labels=False)


def argand_plane(center=P0, unit=U, extent=EXT):
    c = np.array(center, dtype=float)
    e = extent * unit
    grid = VGroup()
    for k in range(-int(extent), int(extent) + 1):
        if k == 0:
            continue
        grid.add(Line(c + np.array([k * unit, -e, 0]), c + np.array([k * unit, e, 0])))
        grid.add(Line(c + np.array([-e, k * unit, 0]), c + np.array([e, k * unit, 0])))
    grid.set_stroke(DIM, 1, opacity=0.45)
    re_axis = Arrow(c + LEFT * e, c + RIGHT * (e + 0.15), buff=0, stroke_width=2.5, color=FG,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.05)
    im_axis = Arrow(c + DOWN * e, c + UP * (e + 0.15), buff=0, stroke_width=2.5, color=FG,
                    tip_length=0.18, max_tip_length_to_length_ratio=0.05)
    re_lbl = T("Re", 30, DIM).next_to(re_axis.get_end(), UP, buff=0.12).shift(LEFT * 0.25)
    im_lbl = T("Im", 30, DIM).next_to(im_axis.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.12)
    g = VGroup(grid, re_axis, im_axis, re_lbl, im_lbl)
    g.grid, g.re_axis, g.im_axis, g.re_lbl, g.im_lbl = grid, re_axis, im_axis, re_lbl, im_lbl
    return g


def phasor_arrow(phase, length=A_MOD, color=GOLD, opacity=1.0):
    a = Arrow(P0, P0 + length * U * ang(phase), buff=0, stroke_width=6, color=color,
              tip_length=0.26, max_tip_length_to_length_ratio=0.3)
    return a.set_opacity(opacity)


def omega_marker(phase, opacity=1.0):
    """Figure 24's small curved arrow, just ahead of the tip, with its omega."""
    arc = Arc(radius=R + 0.28, start_angle=phase + 0.12, angle=0.5, arc_center=P0,
              color=GOLD, stroke_width=3)
    arc.add_tip(tip_length=0.16, tip_width=0.16)
    lbl = _tex(r"\omega", 34, GOLD).move_to(P0 + (R + 0.62) * ang(phase + 0.37))
    return VGroup(arc, lbl).set_opacity(opacity)


def shadow(phase, opacity=1.0):
    """DIM dashed drop line from the tip to the real axis, and the BLUE shadow dot."""
    tip = P0 + R * ang(phase)
    foot = np.array([tip[0], P0[1], 0.0])
    if abs(tip[1] - foot[1]) > 0.08:
        line = DashedLine(tip, foot, color=DIM, stroke_width=2.5, dash_length=0.08)
    else:
        line = Line(foot + UP * 0.001, foot, color=DIM, stroke_width=2.5)
    dot = Dot(foot, radius=0.1, color=BLUE)
    return VGroup(line, dot).set_opacity(opacity)


def shadow_label(phase, opacity=1.0):
    foot = np.array([P0[0] + R * np.cos(phase), P0[1], 0.0])
    lbl = _tex("x(t)", 32, BLUE).move_to(foot + DOWN * 0.42)
    set_backstroke(lbl, width=5)
    return lbl.set_opacity(opacity)


def trail_arc(a0, a1, opacity=1.0):
    span = max(min(a1 - a0, TAU), 1e-3)
    return Arc(radius=R, start_angle=a0, angle=span, arc_center=P0, color=GOLD,
               stroke_width=3).set_stroke(opacity=0.45 * opacity)


def spiral_arc(a0, a1, r0, dr_turn, color=YELLOW, width=3, opacity=1.0, center=P0):
    if abs(a1 - a0) < 0.02:
        a1 = a0 + 0.02 * (1 if a1 >= a0 else -1)
    n = int(abs(a1 - a0) / 0.04) + 3
    ts = np.linspace(a0, a1, n)
    pts = [center + (r0 + dr_turn * abs(t - a0) / TAU) * ang(t) for t in ts]
    m = VMobject().set_points_smoothly(pts)
    return m.set_stroke(color, width, opacity=opacity)


def coil(a0, a1, r0, dr_turn, color=YELLOW, width=4, opacity=1.0, center=P0, keep=1.5 * TAU):
    """An angle arc that may wind past a full turn: a spiral of at most `keep` radians (the newest
    part), rings dr_turn apart, the part more than 3/4 turn behind the head fading out."""
    if a1 - a0 < 0.02:
        span = a1 - a0 if abs(a1 - a0) >= 0.02 else 0.02
        return VGroup(Arc(radius=r0, start_angle=a0, angle=span, arc_center=center)
                      .set_stroke(color, width, opacity=opacity))
    s = max(a0, a1 - keep)
    n = max(2, int((a1 - s) / 0.2) + 1)
    ts = np.linspace(s, a1, n + 1)
    g = VGroup()
    for i in range(n):
        sub = np.linspace(ts[i], ts[i + 1], 5)
        seg = VMobject().set_points_smoothly([center + (r0 + dr_turn * (t - s) / TAU) * ang(t) for t in sub])
        age = (a1 - 0.5 * (ts[i] + ts[i + 1])) / TAU
        op = 1.0 if age < 0.75 else max(0.12, 1.0 - 1.2 * (age - 0.75))
        g.add(seg.set_stroke(color, width, opacity=opacity * op))
    return g


def x_graph(origin=G0, k=K_T, t_max=T_MAX, curve_opacity=1.0):
    """s2's graph: t across, x up, BLUE x(t) = 2 cos(omega t - pi/3) (screen x-scale U)."""
    o = np.array(origin, dtype=float)
    t_axis = Arrow(o + LEFT * 0.1, o + RIGHT * (k * t_max + 0.35), buff=0, stroke_width=2.5,
                   color=DIM, tip_length=0.18, max_tip_length_to_length_ratio=0.05)
    x_axis = Arrow(o + DOWN * (R + 0.35), o + UP * (R + 0.4), buff=0, stroke_width=2.5,
                   color=DIM, tip_length=0.18, max_tip_length_to_length_ratio=0.08)
    t_lbl = MathTex("t", font_size=34, color=DIM).next_to(t_axis.get_end(), RIGHT, buff=0.12)
    x_lbl = MathTex("x", font_size=34, color=DIM).next_to(x_axis.get_end(), RIGHT, buff=0.12)
    curve = ParametricFunction(
        lambda t: o + np.array([k * t, R * np.cos(OMEGA * t + PHI0), 0.0]),
        t_range=[0, t_max, 0.05], color=BLUE, stroke_width=4).set_stroke(opacity=curve_opacity)
    g = VGroup(t_axis, x_axis, t_lbl, x_lbl, curve)
    g.axes, g.curve = VGroup(t_axis, x_axis, t_lbl, x_lbl), curve
    return g


def plane_circle():
    return Circle(radius=R, color=DIM, stroke_width=2).move_to(P0)


def handover_shot():
    """The last frame: plane, circle (with its full GOLD trail), the arrow at arg A with its
    shadow, and the inset pendulum at the matching angle (10 degrees, swinging outward)."""
    return VGroup(argand_plane(), plane_circle(), trail_arc(PHI0, PHI0 + TAU),
                  shadow(PHI0), phasor_arrow(PHI0).set_z_index(3), omega_marker(PHI0),
                  inset_pendulum(PHI0))


def swing_path(color):
    """The inset bob's path, there and back (one full swing), for a passing flash."""
    ts = np.concatenate([np.linspace(-PEND_AMP, PEND_AMP, 30), np.linspace(PEND_AMP, -PEND_AMP, 30)[1:]])
    pts = [INSET_PIVOT + INSET_L * np.array([np.sin(t), -np.cos(t), 0.0]) for t in ts]
    return VMobject().set_points_smoothly(pts).set_stroke(color, 7)


class Clock:
    """Scene clock for the phasor. phase = PHI0 + OMEGA (s - t0) plus smooth warps that land a
    chosen phase on a chosen cue (so cue-locked shots meet the arrow where they need it)."""

    def __init__(self):
        self.s, self.t0, self.warps = 0.0, None, []

    def tick(self, dt):
        self.s += dt

    def start(self):
        self.t0 = self.s

    def phase_at(self, s):
        if self.t0 is None:
            return PHI0
        ph = PHI0 + OMEGA * max(s - self.t0, 0.0)
        for a, b, d in self.warps:
            x = min(max((s - a) / (b - a), 0.0), 1.0)
            ph += d * x * x * (3 - 2 * x)
        return ph

    def phase(self):
        return self.phase_at(self.s)

    def aim(self, ahead, target=PHI0, lo=-PI):
        a = self.s
        b = a + max(ahead, 0.5)
        d = (target - self.phase_at(b) - lo) % TAU + lo
        self.warps.append((a, b, d))
        return d


# ---------------------------------------------------------------- the scene
class Phasor(NarratedScene):
    def dyn(self, build, op0=0.0):
        """An always_redraw object whose opacity follows a tracker."""
        tr = ValueTracker(op0)
        mob = always_redraw(lambda: build(tr.get_value()))
        return mob, tr

    def construct(self):
        clock = self.clock = Clock()
        ticker = VectorizedPoint(P0)
        ticker.add_updater(lambda m, dt: clock.tick(dt))
        self.add(ticker)
        ph = clock.phase

        plane = argand_plane()
        circle = plane_circle()
        self.keep = [ticker]

        # ============================================================ clip 1
        with self.say("c6.arrow.1", gap=2.4) as c:
            full = pendulum(PEND_AMP * 0.5, labels=False)
            self.play(*appear(full, shift=None), run_time=0.8)
            small = inset_pendulum(PHI0)
            self.play(*during([Transform(full, small)], 0.1, 0.9),
                      *during(appear(plane, shift=None), 0.4, 1.0), run_time=1.8)
            self.remove(full)
            inset, _ = self.dyn(lambda op: inset_pendulum(ph()), 1.0)
            self.add(inset)
            self.keep += [plane, inset]

            # {arrow}
            c.wait_until("arrow")
            grow = ValueTracker(0.05)
            arrow = always_redraw(lambda: phasor_arrow(ph(), A_MOD * grow.get_value()).set_z_index(3))
            omk, omk_op = self.dyn(lambda op: omega_marker(ph(), op))
            self.add(arrow, omk)
            self.play(grow.animate.set_value(1.0), omk_op.animate.set_value(1.0), run_time=1.2)
            clock.start()
            self.keep += [arrow, omk]

            # {circle}
            c.wait_until("circle")
            phc = ph()
            trail, trail_op = self.dyn(lambda op: trail_arc(phc, ph(), op))
            self.add(circle, trail)
            circle.set_stroke(opacity=0)
            self.play(circle.animate.set_stroke(opacity=1), trail_op.animate.set_value(1), run_time=1.0)
            self.keep += [circle, trail]

            # {shadow}
            c.wait_until("shadow")
            shd, shd_op = self.dyn(lambda op: shadow(ph(), op))
            slbl, slbl_op = self.dyn(lambda op: shadow_label(ph(), op))
            self.add(shd, slbl)
            self.play(shd_op.animate.set_value(1), slbl_op.animate.set_value(1), run_time=1.0)
            self.keep += [shd, slbl]

            # {swing}
            c.wait_until("swing")
            track = Line(P0 + LEFT * R, P0 + RIGHT * R, color=BLUE, stroke_width=8).set_stroke(opacity=0.35)
            self.play(FadeIn(track), VShowPassingFlash(swing_path(BLUE), time_width=0.6), run_time=1.5)

            # {trace}
            c.wait_until("trace")
            phn = ph()
            t_off = ((phn - PHI0) % TAU) / OMEGA
            down = ParametricFunction(
                lambda s: P0 + np.array([R * np.cos(phn + OMEGA * s), -K_T * s, 0.0]),
                t_range=[0, 8, 0.05], color=BLUE, stroke_width=4)
            graph = x_graph(curve_opacity=0.4)
            self.play(Create(down, rate_func=linear), *appear(graph, shift=None), run_time=1.5)
            base = down.copy()
            shift = G0 + RIGHT * K_T * t_off - P0

            def turn(m, a):
                m.become(base.copy().rotate(a * PI / 2, about_point=P0).shift(a * shift))

            self.play(UpdateFromAlphaFunc(down, turn), run_time=max(1.2, min(1.8, c.until())))

        # ============================================================ clip 2
        with self.say("c6.arrow.2", gap=2.0) as c:
            clock.aim(c.until("amp", floor=0.5), PHI0)
            f82 = MathTex("x(t)", "=", r"\mathrm{Re}\big[", "A", r"\,e^{i\omega t}", r"\big]",
                          font_size=46).move_to([2.6, 1.75, 0])
            eq82 = MathTex("(82)", font_size=30, color=DIM).next_to(f82, RIGHT, buff=0.45)
            self.play(*during(disappear(graph, down, track), 0, 0.45),
                      *during(appear(f82, eq82, lag=0.2), 0.5, 1.0), run_time=1.8)
            self.keep += [f82, eq82]

            # {amp}: a copy freezes at t = 0
            c.wait_until("amp")
            frozen = phasor_arrow(PHI0, opacity=0.6).set_z_index(2)
            self.add(frozen)
            d0 = ang(PHI0)
            a_lbl = MathTex("A", font_size=42, color=GOLD).move_to(P0 + 2.8 * d0)
            t0_lbl = MathTex("t = 0", font_size=30, color=DIM).next_to(a_lbl, RIGHT, buff=0.22)
            set_backstroke(a_lbl, width=5)
            set_backstroke(t0_lbl, width=5)
            self.play(*appear(a_lbl, t0_lbl, lag=0.3), run_time=1.2)
            self.keep += [frozen, a_lbl, t0_lbl]
            clock.aim(c.until("turns", floor=0.5), PHI0)

            c.wait_until("complex amplitude")
            ca = T("complex amplitude", 32, YELLOW)
            ca_box = SurroundingRectangle(ca, color=YELLOW, buff=0.15, stroke_width=2.5)
            cbox = VGroup(ca, ca_box).move_to([2.6, 0.9, 0])
            self.play(*recolor(f82[3], YELLOW), *appear(cbox), run_time=1.2)

            # {turns}
            c.wait_until("turns")
            pht = ph()
            wt_arc, wt_op = self.dyn(lambda op: coil(PHI0, PHI0 + ph() - pht, 0.55, 0.4, YELLOW, 4, op))
            self.add(wt_arc)
            self.play(wt_op.animate.set_value(1), *recolor(f82[4], GOLD),
                      FlashAround(f82[4], color=GOLD, time_width=1.5), run_time=1.5)
            wt_lbl = MathTex(r"\omega t", font_size=38, color=YELLOW).move_to(P0 + 1.5 * ang(2.45))
            set_backstroke(wt_lbl, width=5)
            self.play(*appear(wt_lbl), run_time=1.0)

            c.wait_until("keeps its length")
            ring = circle.copy().set_stroke(GOLD, 6, opacity=1)
            self.play(VShowPassingFlash(ring, time_width=0.6), run_time=2.0)

            # {two_angles}
            c.wait_until("two_angles")
            in_arc, in_op = self.dyn(lambda op: coil(-PI / 2, -PI / 2 + PEND_AMP * np.cos(ph()),
                                                     0.8, 0.0, YELLOW, 4, op, INSET_PIVOT))
            in_lbl = MathTex("x(t)", font_size=32, color=YELLOW).move_to(INSET_PIVOT + np.array([-0.55, -0.85, 0]))
            self.add(in_arc)
            self.play(in_op.animate.set_value(1), *appear(in_lbl), run_time=1.0)
            small_tag = T("stays small", 30, YELLOW).move_to([3.75, 2.3, 0])
            c.wait_until(own_word=small_tag)
            self.play(*appear(small_tag), run_time=1.0)
            grow_tag = T("keeps growing", 30, YELLOW).move_to(P0 + np.array([-1.95, 2.7, 0]))
            c.wait_until(own_word=grow_tag)
            self.play(*appear(grow_tag), FlashAround(wt_lbl, color=YELLOW), run_time=min(1.0, max(0.5, c.until())))

        # ============================================================ clip 3
        X = 3.4
        with self.say("c6.arrow.3") as c:
            q = T("why the same?", 36, YELLOW).move_to([X, 0.9, 0])
            self.play(*during(disappear(cbox, wt_lbl, in_lbl, small_tag, grow_tag), 0, 0.45),
                      *during([wt_op.animate.set_value(0), in_op.animate.set_value(0)], 0, 0.45),
                      *during(appear(q), 0.5, 1.0), run_time=1.8)   # early: the question is asked at "why"
            self.remove(wt_arc, in_arc)

            # {split}
            c.wait_until("split")
            row1 = MathTex("A", "=", r"\alpha", "+", r"i\beta", font_size=40).move_to([X, 0.05, 0])
            row1[0].set_color(YELLOW)
            row1[2].set_color(BLUE)
            row1[4].set_color(PINK)
            self.play(*appear(row1), run_time=1.0)
            row2 = MathTex(r"e^{i\omega t}", "=", r"\cos\omega t", "+", r"i\sin\omega t",
                           font_size=40).move_to([X, -0.7, 0])
            row2[0].set_color(GOLD)
            row2[4].set_color(PINK)
            c.wait_until("cosine plus")
            self.play(*appear(row2), run_time=1.0)

            # {multiply}
            c.wait_until("multiply")
            prod = MathTex("(", r"\alpha", "+", r"i\beta", ")(", r"\cos\omega t", "+",
                           r"i\sin\omega t", ")", font_size=40).move_to([X, -1.5, 0])
            prod[1].set_color(BLUE)
            prod[3].set_color(PINK)
            prod[7].set_color(PINK)
            self.play(*appear(prod), run_time=1.0)
            row_a = MathTex("=", r"\alpha\cos\omega t", "+", r"i\alpha\sin\omega t", font_size=40)
            row_a.next_to(prod, DOWN, buff=0.32).align_to(prod, LEFT).shift(RIGHT * 0.2)
            row_a[1].set_color(BLUE)
            row_a[3].set_color(PINK)
            row_b = MathTex("+", r"i\beta\cos\omega t", "+", "i^2", r"\beta\sin\omega t", font_size=40)
            row_b.next_to(row_a, DOWN, buff=0.3)
            row_b.shift(RIGHT * (row_a[1].get_left()[0] - row_b[1].get_left()[0]))
            row_b[1].set_color(PINK)
            row_b[3].set_color(PINK)
            row_b[4].set_color(PINK)
            self.play(*appear(row_a, row_b, lag=0.4), run_time=1.4)

            # {ii}
            c.wait_until("ii")
            self.play(FlashAround(row_b[3], color=YELLOW, time_width=1.5), run_time=1.2)
            row_b2 = MathTex("+", r"i\beta\cos\omega t", "-", r"\beta\sin\omega t", font_size=40)
            row_b2.align_to(row_b, LEFT).match_y(row_b)
            row_b2[1].set_color(PINK)
            row_b2[3].set_color(BLUE)
            c.wait_until("minus beta")
            self.play(*edit(row_b, row_b2), run_time=1.5)

            # {re}
            c.wait_until("re")
            self.play(*set_alpha([row_a[3], row_b2[1]], DIMMED), run_time=1.0)
            ans = MathTex(r"\mathrm{Re}\big[", "A", r"\,e^{i\omega t}", r"\big]", "=",
                          r"\alpha\cos\omega t", "-", r"\beta\sin\omega t", font_size=40).move_to([X, 0.9, 0])
            ans[5].set_color(BLUE)
            ans[7].set_color(BLUE)
            c.wait_until("alpha times")
            self.play(*swap(q, ans), run_time=1.2)

        # ============================================================ clip 4
        with self.say("c6.arrow.4") as c:
            sweep_clear(self, ans.animate.move_to([X, -0.4, 0]), keep=[*self.keep, ans])
            s2f = MathTex("x(t)", "=", "a", r"\cos\omega t", "+", "b", r"\sin\omega t",
                          font_size=40).move_to([X, 0.75, 0])
            s2f[2].set_color(BLUE)
            s2f[5].set_color(BLUE)
            s2f.shift(RIGHT * (ans[5].get_center()[0] - s2f[3].get_center()[0]) * 0.5)
            l_cos = Line(s2f[3].get_bottom() + DOWN * 0.1, ans[5].get_top() + UP * 0.1,
                         color=DIM, stroke_width=2)
            l_sin = Line(s2f[6].get_bottom() + DOWN * 0.1, ans[7].get_top() + UP * 0.1,
                         color=DIM, stroke_width=2)
            self.play(*appear(s2f, shift=0.5 * LEFT), *during([Create(l_cos), Create(l_sin)], 0.5, 1.0),
                      run_time=1.4)

            c.wait_until("alpha")
            alpha_eq = MathTex(r"\alpha", "=", "a", font_size=42).move_to([2.2, -1.45, 0])
            alpha_eq[0].set_color(BLUE)
            alpha_eq[2].set_color(BLUE)
            self.play(*appear(alpha_eq), FlashAround(l_cos, color=YELLOW), run_time=1.0)

            c.wait_until("beta")
            beta_eq = MathTex(r"\beta", "=", "-b", font_size=42).move_to([4.6, -1.45, 0])
            beta_eq[0].set_color(BLUE)
            beta_eq[2].set_color(BLUE)
            self.play(*appear(beta_eq), FlashAround(l_sin, color=YELLOW), run_time=1.0)

            c.wait_until("box")
            box_a = MathTex("A", "=", "a", "-ib", font_size=54).move_to([X, -2.6, 0])
            box_a[0].set_color(YELLOW)
            box_a[2].set_color(BLUE)
            box_a[3].set_color(PINK)
            box_r = SurroundingRectangle(box_a, color=YELLOW, buff=0.22, stroke_width=3)
            boxg = VGroup(box_a, box_r)
            self.play(*appear(boxg), run_time=1.2)

            c.wait_until("two real constants")
            self.play(*flash([box_a[2], box_a[3]], color=YELLOW, time_width=1.5), run_time=1.5)

        # ============================================================ clip 5
        with self.say("c6.arrow.5", gap=0.1) as c:
            clock.aim(c.until("cosform", floor=0.5), PHI0 + PI)
            sweep_clear(self, boxg.animate.move_to([X, 0.8, 0]), slbl_op.animate.set_value(0),
                        keep=[*self.keep, boxg])

            # {mod}
            c.wait_until("mod")
            mod_lbl = MathTex("|A|", font_size=36, color=GOLD).move_to(
                P0 + 1.5 * d0 + 0.42 * np.array([-0.866, -0.5, 0]))
            set_backstroke(mod_lbl, width=5)
            ring = circle.copy().set_stroke(GOLD, 6, opacity=1)
            self.play(*appear(mod_lbl), *during(disappear(t0_lbl), 0, 0.5), VShowPassingFlash(ring, time_width=0.6),
                      run_time=2.0)
            mod_row = MathTex("|A|", "=", r"\sqrt{a^2 + b^2}", font_size=42, color=GOLD).move_to([X, -0.3, 0])
            c.wait_until("pythagoras")
            self.play(*appear(mod_row), run_time=1.0)

            # {arg}
            c.wait_until("arg")
            arg_arc = Arc(radius=0.8, start_angle=0, angle=PHI0, arc_center=P0, color=YELLOW,
                          stroke_width=4)
            arg_lbl = MathTex(r"\arg A", font_size=34, color=YELLOW).move_to(P0 + np.array([1.25, -0.45, 0]))
            set_backstroke(arg_lbl, width=5)
            self.play(Create(arg_arc), *appear(arg_lbl), run_time=1.2)
            phase_tag = T("phase", 30, YELLOW).move_to(P0 + np.array([1.2, -0.86, 0]))
            set_backstroke(phase_tag, width=5)
            c.wait_until(own_word=phase_tag)
            self.play(*appear(phase_tag), run_time=1.0)

            # {cosform}
            c.wait_until("cosform")
            cos_row = MathTex("x(t)", "=", "|A|", r"\cos(", r"\omega t + \arg A", ")",
                              font_size=42).move_to([X, -1.45, 0])
            cos_row[2].set_color(GOLD)
            cos_row[4].set_color(YELLOW)
            phr = ph()
            full_arc, full_op = self.dyn(lambda op: coil(0, PHI0 + PI + ph() - phr, 0.3, 0.25, YELLOW, 4, op))
            self.add(full_arc)
            self.play(*appear(cos_row), full_op.animate.set_value(1), run_time=1.2)
            self.play(FlashAround(cos_row[4], color=YELLOW, time_width=1.5), run_time=1.5)

            # {fullturn}
            c.wait_until("fullturn")
            phf = ph()
            teal, teal_op = self.dyn(lambda op: Arc(
                radius=R, start_angle=phf, angle=max(min(ph() - phf, TAU), 1e-3), arc_center=P0,
                color=TEAL, stroke_width=6).set_stroke(opacity=op))
            two_pi = MathTex(r"2\pi", font_size=38, color=TEAL).move_to(P0 + 1.35 * ang(3 * PI / 4))
            set_backstroke(two_pi, width=5)
            self.add(teal)
            clock.aim(c.until() + 0.1 + 1.5 + 1.0 + 1.0, PHI0, lo=-PI / 2)
            self.play(full_op.animate.set_value(0), teal_op.animate.set_value(1), *appear(two_pi),
                      run_time=1.0)
            self.remove(full_arc)
            swing_row = VGroup(T("one turn = one swing:", 32, TEAL),
                               MathTex(r"\tfrac{2\pi}{\omega}", font_size=44, color=TEAL)).arrange(RIGHT, buff=0.2)
            swing_row.move_to([X, -2.6, 0])
            self.play(*appear(swing_row), run_time=1.0)
            c.wait_until("one full swing")
            self.play(VShowPassingFlash(swing_path(TEAL), time_width=0.6), run_time=min(1.5, max(0.5, c.until())))

        # ------------------------------------------------ handover: fade the extras, keep turning
        extras = [f82, eq82, boxg, mod_row, cos_row, swing_row, frozen, a_lbl, mod_lbl,
                  arg_arc, arg_lbl, phase_tag, two_pi]
        self.wait(1.5)
        self.play(*disappear(*extras), teal_op.animate.set_value(0), run_time=1.0)
        self.wait(1.0)
        self.remove(*self.mobjects)
        self.add(handover_shot())
        self.wait(0.1)
