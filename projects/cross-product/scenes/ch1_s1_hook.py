"""Chapter 1, scene 1: hook. Two arrows, their parallelogram, a x b rising out of it; then the
formula students memorise, and the question of how the picture becomes the formula.
Clips c1.hook.1 – c1.hook.2.

Shared 3D frame, copied from ch1_s4_define.py (s4 owns it): W, P, Camera3D, the 3D
NarratedScene, flat3d, make_axes, floor_grid, vec3; phi = 70°, theta = -60°, zoom 1;
a = P(3,0,0) BLUE, b = P(1,2,0) YELLOW, a x b = P(0,0,6) TEAL; parallelogram TEAL 0.45, z -1.
Staging here: the camera drifts slowly in theta (-65° at {arrows}, -60° as clip 2 starts), and a
driver updater re-aims it every frame so the axes' origin O stays at the screen point (sx, sy):
clip 1 centres the picture, clip 2 moves it left for the formula.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene as NarratedScene2D  # noqa: E402
from lib.style import *  # noqa: E402,F403
from lib.titles import title_card  # noqa: E402

# ── shared 3D frame (verbatim from ch1_s4_define.py) ─────────────────────────────
U = 0.6                                       # scene units per axis step
W = np.array([-2.5981, -1.5, 0.0])            # where the axes' origin sits = -3·(cos30°, sin30°, 0)


def P(x, y, z=0.0):
    return W + np.array([x, y, z], dtype=float) * U


O = P(0, 0, 0)


class Camera3D(ThreeDCamera):
    """frame_center only re-aims the projection; the 2D frame itself never shifts."""

    @property
    def frame_center(self):
        return np.zeros(3)

    @frame_center.setter
    def frame_center(self, point):
        self._frame_center.move_to(point)

    def project_points(self, points):
        look = self._frame_center.points[0]
        d, zoom, rot = self.get_focal_distance(), self.get_zoom(), self.get_rotation_matrix()
        points = np.dot(points - look, rot.T)
        zs = points[:, 2]
        factor = d / (d - zs)
        factor[(d - zs) < 0] = 10**6
        for i in 0, 1:
            points[:, i] *= factor * zoom
        return points


class NarratedScene(NarratedScene2D, ThreeDScene):
    """NarratedScene with a 3D camera (engine/lib has no 3D variant, and vk finds the scene by
    the literal `class X(NarratedScene)`)."""

    def __init__(self, **kwargs):
        super().__init__(camera_class=Camera3D, **kwargs)


def flat3d(mob):
    """No Lambert shading: surfaces keep one flat colour and draw in scene/z_index order."""
    for m in mob.get_family():
        m.shade_in_3d = False
    return mob


def make_axes():
    ax = ThreeDAxes(
        x_range=[-2.5, 5.5, 1], y_range=[-1.5, 3.5, 1], z_range=[-6.5, 6.5, 1],
        x_length=8 * U, y_length=5 * U, z_length=13 * U, tips=False,
        axis_config={"color": FG, "stroke_width": 2, "tick_size": 0.05},
    )
    ax.shift(W - ax.c2p(0, 0, 0))
    return flat3d(ax)


def floor_grid():
    g = VGroup()
    for x in range(-2, 6):
        if x:
            g.add(Line(P(x, -1.5), P(x, 3.5)))
    for y in range(-1, 4):
        if y:
            g.add(Line(P(-2.5, y), P(5.5, y)))
    g.set_stroke(FG, 1.5, opacity=0.16)
    g.set_z_index(-2)
    return g


def vec3(end, color, start=None, thick=0.025, tip_h=0.27, tip_r=0.095):
    """A 3D vector: Line3D shaft (radius `thick`) + Cone tip (apex at `end`), flat colour."""
    start = O if start is None else np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    d = (end - start) / np.linalg.norm(end - start)
    shaft = Line3D(start, end - tip_h * d, thickness=thick, resolution=(1, 12))
    tip = Cone(direction=d, base_radius=tip_r, height=tip_h, resolution=(1, 16))
    tip.shift(end)
    v = VGroup(shaft, tip)
    v.set_fill(color, 1).set_stroke(color, 0.6)
    return flat3d(v)


# ── this scene ──────────────────────────────────────────────────────────────────
PHI = 70 * DEGREES
THETA_START = -65 * DEGREES
DRIFT = 0.006                      # rad/s, about 0.34°/s
HERO = (-1.3, -1.35, 1.35)         # clip 1: O on screen and zoom: close up, a x b just inside
LEFT_SPOT = (-5.0, 0.0, 1.0)       # clip 2: s4's zoom, picture on the left, formula on the right

FORMULA_SIZE = 40
FORMULA_Y = 1.0
FORMULA_PARTS = [r"\mathbf a", r"\times", r"\mathbf b", "=", "(",
                 "a_2", "b_3", "-", "a_3", "b_2", r",\ ",
                 "a_3", "b_1", "-", "a_1", "b_3", r",\ ",
                 "a_1", "b_2", "-", "a_2", "b_1", ")"]


def corner(u, v, s=0.3):
    """Right-angle mark at O between directions u and v."""
    u = np.array(u, dtype=float) / np.linalg.norm(u)
    v = np.array(v, dtype=float) / np.linalg.norm(v)
    return VMobject().set_points_as_corners([O + s * u, O + s * (u + v), O + s * v]).set_stroke(FG, 3).set_z_index(1)


class Hook(NarratedScene):
    def construct(self):
        self.build_camera()
        self.build_world()
        with self.say("c1.hook.1") as c:
            self.picture(c)
        with self.say("c1.hook.2") as c:
            self.formula(c)
        self.wait(1.0)
        self.finish()

    # ── camera ────────────────────────────────────────────────────────────────
    def build_camera(self):
        self.set_camera_orientation(phi=PHI, theta=THETA_START, zoom=HERO[2])
        self.sx, self.sy, self.zt = (ValueTracker(v) for v in HERO)
        self.drift = 0.0
        self.driver = Mobject().set_z_index(-100)   # first in the z-sorted family

        def drive(m, dt):
            cam = self.camera
            cam.theta_tracker.increment_value(self.drift * dt)
            cam.zoom_tracker.set_value(self.zt.get_value())
            R = cam.generate_rotation_matrix()
            s = np.array([self.sx.get_value(), self.sy.get_value(), 0.0]) / cam.get_zoom()
            cam.frame_center = O - R.T @ s          # O lands exactly on (sx, sy)

        self.driver.add_updater(drive)
        drive(self.driver, 0)
        self.add(self.driver)          # first moving mobject, so nothing is cached as static

    def hud(self, *mobs):
        """Fixed in frame (screen coordinates), drawn on top; not added yet."""
        self.camera.add_fixed_in_frame_mobjects(*mobs)
        for m in mobs:
            m.set_z_index(10)
        return mobs[0]

    def pin(self, mob, anchor, offset):
        """Fixed-orientation label drawn at screen(anchor) + offset; follows the camera."""
        anchor = np.array(anchor, dtype=float)
        mob.move_to(anchor + np.array([offset[0], offset[1], 0.0]))
        self.camera.add_fixed_orientation_mobjects(mob, center_func=lambda a=anchor: a)
        mob.set_z_index(2)
        return mob

    def scr(self, p):
        """Where a 3D point is drawn by the current camera."""
        self.camera.reset_rotation_matrix()
        q = self.camera.project_point(np.array(p, dtype=float))
        return np.array([q[0], q[1], 0.0])

    # ── the 3D picture ──────────────────────────────────────────────────────
    def build_world(self):
        self.axes = make_axes()
        self.grid = floor_grid()
        self.ax_labels = [
            self.pin(MathTex("x", font_size=36), P(5.5, 0, 0), (0.28, -0.12)),
            self.pin(MathTex("y", font_size=36), P(0, 3.5, 0), (-0.25, 0.22)),
            self.pin(MathTex("z", font_size=36), P(0, 0, 6.5), (-0.28, -0.1)),
        ]
        self.va = vec3(P(3, 0, 0), BLUE)
        self.vb = vec3(P(1, 2, 0), YELLOW)
        self.vc = vec3(P(0, 0, 6), TEAL, thick=0.035, tip_h=0.32, tip_r=0.12)
        self.la = self.pin(set_backstroke(MathTex(r"\mathbf a", font_size=48, color=BLUE)),
                           P(3, 0, 0), (0.05, -0.45))
        self.lb = self.pin(set_backstroke(MathTex(r"\mathbf b", font_size=48, color=YELLOW)),
                           P(1, 2, 0), (0.45, 0.3))
        self.lc = self.pin(set_backstroke(MathTex(r"\mathbf a\times\mathbf b", font_size=44, color=TEAL)),
                           P(0, 0, 6), (0.8, -0.05))

        self.para = Polygon(P(0, 0), P(3, 0), P(4, 2), P(1, 2))
        self.para.set_fill(TEAL, 0.45).set_stroke(TEAL, 2)
        self.para.set_z_index(-1)
        self.right_a = corner(OUT, RIGHT)
        self.right_b = corner(OUT, [1, 2, 0])

    def picture(self, c):
        card = title_card("From a picture to a formula")
        self.hud(card)
        self.play(FadeIn(card.title, shift=0.3 * DOWN), GrowFromCenter(card.rule),
                  time_span(FadeIn(card.course, shift=0.2 * DOWN), 0.1, 0.6),
                  time_span(FadeIn(card.part, shift=0.2 * DOWN), 0.1, 0.6), run_time=0.6)

        # {arrows}: card out, space in, then a and b grow from the same point
        c.wait_until("Take two vectors")
        self.drift = DRIFT
        self.play(*[FadeOut(m) for m in card],
                  time_span(FadeIn(self.axes), 0.4, 1.4),
                  time_span(FadeIn(self.grid), 0.4, 1.4),
                  *[time_span(FadeIn(m), 0.6, 1.4) for m in self.ax_labels],
                  run_time=1.4)
        c.wait_until("ay and bee")
        self.play(time_span(GrowFromPoint(self.va, O), 0, 1.5),
                  time_span(GrowFromPoint(self.vb, O), 0.4, 1.9),
                  time_span(FadeIn(self.la, shift=0.3 * DOWN), 1.0, 1.8),
                  time_span(FadeIn(self.lb, shift=0.3 * DOWN), 1.4, 2.2),
                  run_time=2.2)

        # {area}: the parallelogram they span
        c.wait_until("Together, they span")
        self.play(DrawBorderThenFill(self.para), run_time=min(1.8, 0.8 * c.until("Their cross product")))

        # {rise}: a x b grows straight up, then the right angles
        c.wait_until("Their cross product")
        self.play(time_span(GrowFromPoint(self.vc, O), 0, 1.8),
                  time_span(FadeIn(self.lc, shift=0.3 * DOWN), 1.2, 2.1),
                  run_time=2.1)
        c.wait_until("right angles")
        self.play(Create(self.right_a), Create(self.right_b), run_time=1.0)

    # ── the formula ─────────────────────────────────────────────────────────
    def make_formula(self):
        f = MathTex(*FORMULA_PARTS, font_size=FORMULA_SIZE)
        self.subs = []
        for part, g in zip(FORMULA_PARTS, f):
            if part == r"\mathbf a" or part.startswith("a_"):
                g.set_color(BLUE)
            elif part == r"\mathbf b" or part.startswith("b_"):
                g.set_color(YELLOW)
            if part[1:2] == "_":
                self.subs.append(g[1])
        f.to_edge(RIGHT, buff=0.6).set_y(FORMULA_Y)
        return f

    def formula(self, c):
        f = self.make_formula()
        self.hud(f)
        self.play(*[time_span(t.animate.set_value(v), 0, 1.2)
                    for t, v in zip((self.sx, self.sy, self.zt), LEFT_SPOT)],
                  time_span(Write(f), 1.0, 2.6), run_time=2.6)

        mem = T("memorise", size=44).move_to([f.get_x() - 1.8, f.get_bottom()[1] - 1.0, 0])
        der = T("derive", size=44, color=GREEN).move_to([f.get_x() + 1.8, mem.get_y(), 0])
        strike = Line(mem.get_left() + 0.12 * LEFT, mem.get_right() + 0.12 * RIGHT,
                      color=RED, stroke_width=6)
        self.hud(mem, der, strike)
        c.wait_until("handed to memorise")
        self.play(FadeIn(mem, shift=0.2 * DOWN), run_time=0.8)

        # {shuffle}: the subscripts flash in turn
        c.wait_until("It looks like")
        step = 0.17
        self.play(*[time_span(g.animate(rate_func=there_and_back).scale(1.5).set_color(FG),
                              step * k, step * k + 0.6)
                    for k, g in enumerate(self.subs)])

        # {why}: a question mark over it
        c.wait_until("So why would")
        q = T("?", size=110, color=YELLOW).next_to(f, UP, buff=0.4)
        self.hud(q)
        self.play(FadeIn(q, shift=0.3 * DOWN, scale=0.6), run_time=1.0)

        # {bridge}: picture -> formula, with a question mark on the way
        c.wait_until("And how does")
        p = self.scr(P(0, 0, 6)) + np.array([0.8, -0.05, 0])      # where the a x b label sits
        start = p + (self.lc.width / 2 + 0.18) * RIGHT + 0.05 * DOWN
        lhs_top = np.array([f[0].get_left()[0], f[0].get_top()[1], 0])
        end = lhs_top + 0.35 * RIGHT + 0.22 * UP
        bridge = CurvedArrow(start, end, angle=-PI / 2.4, color=YELLOW, stroke_width=4)
        d = normalize(end - start)
        bulge = np.array([-d[1], d[0], 0.0])                  # the side a clockwise arc bows to
        bq = T("?", size=56, color=YELLOW).move_to(bridge.point_from_proportion(0.5) + 0.4 * bulge)
        self.hud(bridge, bq)
        self.play(Create(bridge), time_span(FadeIn(bq, shift=0.2 * DOWN), 0.8, 1.6), run_time=1.6)

        # {derive}: derive it, instead of memorising it
        c.wait_until("By the end")
        self.play(FadeIn(der, shift=0.25 * DOWN), run_time=1.0)
        c.wait_until("instead of memorising")
        self.play(Create(strike), mem.animate.set_color(DIM), run_time=0.8)

    def finish(self):
        vis = [m for m in self.mobjects
               if m is not self.driver and not isinstance(m, ValueTracker)]
        self.play(*[FadeOut(m) for m in vis], run_time=1.0)
        self.remove(*self.mobjects)
        self.wait(0.15)
