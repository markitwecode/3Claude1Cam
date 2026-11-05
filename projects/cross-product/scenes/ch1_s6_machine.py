"""Chapter 1, scene 6: Does it distribute? Crossing with a as a machine: split b, turn the view
so a points up, and read the machine as project -> rotate 90 deg -> scale by |a|.
Clips c1.mach.1 – c1.mach.5.

Opens on s4's end shot (its shared 3D frame is copied below: W, P, Camera3D, NarratedScene,
flat3d, make_axes, floor_grid, vec3, coord_label). Camera moves are true slerps (CamMove drives
Camera3D.R_override), so the turn to the "a up" view never passes through odd Euler angles.

HAND-OFF TO s7 (ch1_s7_linear opens on this scene's last shot), all in s4's frame:
  camera   A_UP: phi=60.5013°, theta=28.3408°, gamma=-132.3941°, zoom 1.3, focal distance 20,
           frame_center (-2.4992, -1.7525, 0.0581) (Camera3D: frame_center only re-aims the
           projection). That is s7's phi=40°, theta=50° after the cyclic swap (s4 x -> up,
           y -> x, z -> y); the origin P(0,0,0) lands at screen (-0.3, -0.2), a's tip at (-0.32, 1.40).
  a        vec3(P(3,0,0), BLUE) (radius 0.025, tip 0.27 x 0.095), label MathTex \\mathbf a 46 BLUE
           with backstroke, pinned at a's tip + (0.35, 0.0) on screen.
  floor    up_floor(): lines at whole y in [-3, 3] and whole z in [-2, 7] in the plane x = 0,
           FG, width 1.5, opacity 0.22, z_index -2 (no axes in this view).
  strip    Strip() (s7's class): three boxes 3.0 x 0.76, corner 0.14, buff 0.8, centred at y=3.3,
           stroke DIM 2.5, fill BG 0.9; labels T 32 (FG) 0.2 left of centre; DIM arrows; no ticks.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene as NarratedScene2D  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ── s4's shared 3D frame (copied from ch1_s4_define.py) ──────────────────────────────────
U = 0.6                                       # scene units per axis step
W = np.array([-2.5981, -1.5, 0.0])            # where the axes' origin sits


def P(x, y, z=0.0):
    return W + np.array([x, y, z], dtype=float) * U


O = P(0, 0, 0)
STD = dict(phi=70 * DEGREES, theta=-60 * DEGREES, gamma=0.0, zoom=1.0, frame_center=ORIGIN)
THETA = np.arctan2(2, 1)                      # the angle between a and b


class Camera3D(ThreeDCamera):
    """frame_center only re-aims the projection; the 2D frame itself never shifts.
    (s6 addition: R_override, set by CamMove while the camera slerps.)"""

    R_override = None

    @property
    def frame_center(self):
        return np.zeros(3)

    @frame_center.setter
    def frame_center(self, point):
        self._frame_center.move_to(point)

    def generate_rotation_matrix(self):
        if self.R_override is not None:
            return self.R_override
        return super().generate_rotation_matrix()

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
    """NarratedScene with a 3D camera (vk finds the scene by the literal `class X(NarratedScene)`)."""

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


def coord_label(name, coords, color, size=40):
    parts = [name, "=", "("]
    for i, c in enumerate(coords):
        parts += [str(c)] + ([","] if i < len(coords) - 1 else [])
    parts.append(")")
    lab = MathTex(*parts, font_size=size, color=FG)
    lab[0].set_color(color)
    for i, p in enumerate(parts):
        if p.isdigit():
            lab[i].set_color(GOLD)
    return lab


# ── s7's strip (copied from ch1_s7_linear.py so the hand-off matches exactly) ─────────────
class Strip(VGroup):
    """project -> rotate 90 deg -> scale by |a|, fixed at the top."""

    def __init__(self):
        super().__init__()
        self.boxes, self.labels, self.arrows = VGroup(), VGroup(), VGroup()
        names = [T("project", 32), T("rotate 90°", 32),
                 VGroup(T("scale by", 32), MathTex(r"|\mathbf a|", font_size=38)).arrange(RIGHT, buff=0.14)]
        for lab in names:
            box = RoundedRectangle(corner_radius=0.14, width=3.0, height=0.76)
            box.set_stroke(DIM, 2.5).set_fill(BG, 0.9)
            self.boxes.add(box)
            self.labels.add(lab)
        self.boxes.arrange(RIGHT, buff=0.8).move_to(3.3 * UP)
        for box, lab in zip(self.boxes, self.labels):
            lab.move_to(box.get_center() + 0.2 * LEFT)
        for b1, b2 in zip(self.boxes[:-1], self.boxes[1:]):
            self.arrows.add(Arrow(b1.get_right(), b2.get_left(), buff=0.1, color=DIM,
                                  stroke_width=3, max_tip_length_to_length_ratio=0.35))
        self.add(self.boxes, self.labels, self.arrows)

    def light(self, i, on=True):
        if on:
            return [self.boxes[i].animate.set_stroke(YELLOW, 3.5), self.labels[i].animate.set_color(YELLOW)]
        return [self.boxes[i].animate.set_stroke(DIM, 2.5), self.labels[i].animate.set_color(FG)]


# ── this scene's world (s4 coordinates) ──────────────────────────────────────────────────
A = np.array([3.0, 0, 0])
B = np.array([1.0, 2, 0])
BPAR = np.array([1.0, 0, 0])
BPERP = np.array([0, 2.0, 0])
AXB = np.array([0, 0, 6.0])


def _rz(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def _rx(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[1.0, 0, 0], [0, c, -s], [0, s, c]])


def cam_R(phi, theta, gamma=0.0):
    """ThreeDCamera's rotation matrix for these angles (radians)."""
    return _rz(gamma) @ _rx(-phi) @ _rz(-theta - PI / 2)


def view(phi, theta, gamma, zoom, origin_xy):
    """A camera dict whose frame_center puts the world origin O at screen `origin_xy`."""
    phi, theta, gamma = phi * DEGREES, theta * DEGREES, gamma * DEGREES
    R = cam_R(phi, theta, gamma)
    fc = O - R.T @ np.array([origin_xy[0] / zoom, origin_xy[1] / zoom, 0.0])
    return dict(phi=phi, theta=theta, gamma=gamma, zoom=zoom, frame_center=fc)


SPLIT = view(34, -74, 0, 1.9, (-0.5, -2.3))                  # the floor from higher up: split, shear
A_UP = view(60.5013, 28.3408, -132.3941, 1.3, (-0.3, -0.2))  # a vertical, floor = the plane x = 0


def up_floor():
    """The floor at right angles to a (the plane x = 0)."""
    g = VGroup(*[Line(P(0, y, -2), P(0, y, 7)) for y in range(-3, 4)],
               *[Line(P(0, -3, z), P(0, 3, z)) for z in range(-2, 8)])
    g.set_stroke(FG, 1.5, opacity=0.22)
    g.set_z_index(-2)
    return g


def arrow3(start, end, color, big=False):
    """vec3 that survives short lengths (smaller tip) and zero length (invisible), always with
    the same structure, so a live arrow can `become` it every frame."""
    start, end = np.asarray(start, float), np.asarray(end, float)
    L = np.linalg.norm(end - start)
    th, h, r = (0.035, 0.32, 0.12) if big else (0.025, 0.27, 0.095)
    if L < 0.03:
        d = (end - start) / L if L > 1e-9 else RIGHT
        v = vec3(start + 0.03 * d, color, start=start, thick=th, tip_h=0.01, tip_r=0.01)
        return v.set_opacity(0)
    k = min(1.0, L / (1.6 * h))
    return vec3(end, color, start=start, thick=th, tip_h=h * k, tip_r=r * k)


def corner(o, u, v, s=0.2, color=FG):
    o, u, v = (np.asarray(x, float) for x in (o, u, v))
    u, v = u / np.linalg.norm(u), v / np.linalg.norm(v)
    return VMobject().set_points_as_corners([o + s * u, o + s * u + s * v, o + s * v]).set_stroke(color, 3)


def plane_arc(o, e1, e2, r, t0, t1, color=FG, width=4, tip=0.17):
    """An arc arrow in the plane of e1, e2, turning from e1 toward e2 (t in radians)."""
    o, e1, e2 = (np.asarray(x, float) for x in (o, e1, e2))
    pts = [o + r * (np.cos(t) * e1 + np.sin(t) * e2) for t in np.linspace(t0, t1, 40)]
    arc = VMobject().set_points_smoothly(pts).set_stroke(color, width)
    tang = np.sign(t1 - t0) * (-np.sin(t1) * e1 + np.cos(t1) * e2)
    rad = np.cos(t1) * e1 + np.sin(t1) * e2
    end = pts[-1]
    head = Polygon(end + tip * tang, end + 0.5 * tip * rad, end - 0.5 * tip * rad)
    head.set_fill(color, 1).set_stroke(color, 1)
    return VGroup(arc, head)


def flash_line(p, q, color, width=10, run_time=1.2):
    return VShowPassingFlash(Line(p, q).set_stroke(color, width), time_width=0.6, run_time=run_time)


def lab(tex, color, size=46):
    return set_backstroke(MathTex(tex, color=color, font_size=size), width=6)


def hand_icon(color=FG):
    """Right-hand-rule glyph: thumb up, fingers curling counterclockwise seen from above."""
    thumb = Arrow(0.5 * DOWN, 0.55 * UP, buff=0, stroke_width=5, color=color,
                  max_tip_length_to_length_ratio=0.28)
    curl = Arc(radius=0.38, start_angle=150 * DEGREES, angle=235 * DEGREES)
    curl.stretch(0.4, 1).set_stroke(color, 4)
    curl.add_tip(tip_length=0.16, tip_width=0.16)
    curl.get_tip().set_fill(color, 1).set_stroke(color, 1)
    return VGroup(curl, thumb)


def light_icon():
    core = Circle(radius=0.12).set_fill(FG, 1).set_stroke(width=0)
    rays = VGroup(*[Line(0.19 * rotate_vector(RIGHT, k * TAU / 8), 0.31 * rotate_vector(RIGHT, k * TAU / 8))
                    for k in range(8)]).set_stroke(FG, 2.5)
    return VGroup(core, rays)


def _slerp(u, v, t):
    u, v = u / np.linalg.norm(u), v / np.linalg.norm(v)
    om = np.arccos(np.clip(np.dot(u, v), -1, 1))
    if om < 1e-6:
        return u
    return (np.sin((1 - t) * om) * u + np.sin(t * om) * v) / np.sin(om)


def _orbit(R0, R1, t):
    """Camera orientation part-way from R0 to R1: the viewing direction moves along a great
    circle while the screen's up direction turns with it (an orbit plus a roll)."""
    d = _slerp(R0[2], R1[2], t)
    up = _slerp(R0[1], R1[1], t)
    up = up - np.dot(up, d) * d
    up /= np.linalg.norm(up)
    return np.array([np.cross(up, d), up, d])


Q7 = np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0.0]])   # s4 -> s7 frame: x -> up, y -> x, z -> y


class CamMove(Animation):
    """Move the camera to `target` (a view dict); the origin's screen point moves in a line.
    Default path: _orbit. roll_first: first roll the picture until a points up, then orbit
    around a (azimuth and elevation measured from a, i.e. s7's phi/theta) into the target."""

    def __init__(self, scene, target, roll_first=False, split=0.45, **kw):
        self._sc = scene
        self._target = target
        self._roll_first, self._split = roll_first, split
        super().__init__(Mobject(), remover=True, **kw)

    def _state(self, R, zoom, look):
        v = R @ (O - look)
        f = self._d / (self._d - v[2])
        return v[:2] * zoom * f, v[2]

    def begin(self):
        cam = self._sc.renderer.camera
        self._d = cam.get_focal_distance()
        R0 = cam.R_override if cam.R_override is not None else cam_R(cam.get_phi(), cam.get_theta(), cam.get_gamma())
        z0, look0 = cam.get_zoom(), cam._frame_center.points[0].copy()
        t = self._target
        R1 = cam_R(t["phi"], t["theta"], t["gamma"])
        self._a = (R0, z0, *self._state(R0, z0, look0))
        self._b = (R1, t["zoom"], *self._state(R1, t["zoom"], np.array(t["frame_center"], float)))
        if self._roll_first:
            sa = R0 @ np.array([1.0, 0, 0])
            self._rho = PI / 2 - np.arctan2(sa[1], sa[0])
            Ma = _rz(self._rho) @ R0 @ Q7.T
            M1 = R1 @ Q7.T
            pa, ta = np.arccos(Ma[2, 2]), np.arctan2(Ma[2, 1], Ma[2, 0])
            p1, t1 = np.arccos(M1[2, 2]), np.arctan2(M1[2, 1], M1[2, 0])
            dt = (t1 - ta + PI) % TAU - PI
            self._orb = (pa, ta, p1 - pa, dt)
        super().begin()

    def interpolate_mobject(self, alpha):
        t = self.rate_func(alpha)
        cam = self._sc.renderer.camera
        R0, z0, s0, w0 = self._a
        R1, z1, s1, w1 = self._b
        if not self._roll_first:
            R = _orbit(R0, R1, t)
        elif alpha < self._split:
            R = _rz(self._rho * smooth(alpha / self._split)) @ R0
        else:
            u = smooth((alpha - self._split) / (1 - self._split))
            pa, ta, dp, dt = self._orb
            R = cam_R(pa + u * dp, ta + u * dt, 0.0) @ Q7
        zoom, s, w = z0 + (z1 - z0) * t, s0 + (s1 - s0) * t, w0 + (w1 - w0) * t
        f = self._d / (self._d - w)
        cam.R_override = R
        cam.zoom_tracker.set_value(zoom)
        cam._frame_center.move_to(O - R.T @ np.array([*(s / (zoom * f)), w]))

    def clean_up_from_scene(self, scene):
        super().clean_up_from_scene(scene)
        scene.renderer.camera.R_override = None
        scene.set_camera_orientation(**self._target)


class Machine(NarratedScene):
    # ── helpers ─────────────────────────────────────────────────────────────────────────
    def hud(self, *mobs):
        """Overlays: drawn in screen coordinates whatever the camera does."""
        for m in mobs:
            self.camera.add_fixed_in_frame_mobjects(m)
            m.set_z_index(3)
        return mobs[0] if len(mobs) == 1 else mobs

    def fx(self, anim):
        self.camera.add_fixed_in_frame_mobjects(anim.mobject)
        anim.mobject.set_z_index(3)
        return anim

    def pin(self, mob, anchor, offs, view="STD"):
        """A flat label drawn at screen(anchor) + offs[view]; follows camera moves."""
        mob.pin_fn = anchor if callable(anchor) else (lambda p=np.array(anchor, float): p)
        mob.offs = offs
        mob.pin_off = np.array([*offs[view], 0.0])
        mob.move_to(mob.pin_fn() + mob.pin_off)
        self.camera.add_fixed_orientation_mobjects(mob, center_func=lambda m=mob: m.pin_fn())
        mob.set_z_index(2)
        self.pins.append(mob)
        return mob

    def follow(self, mob, fn):
        mob.pin_fn = fn
        mob.add_updater(lambda m: m.move_to(m.pin_fn() + m.pin_off))

    def unfollow(self, mob):
        mob.clear_updaters()
        p = np.array(mob.pin_fn(), float)
        mob.pin_fn = lambda p=p: p

    def reoffset(self, view):
        anims = []
        for m in self.pins:
            if view in m.offs:
                new = np.array([*m.offs[view], 0.0])
                d = new - m.pin_off
                m.pin_off = new
                if np.linalg.norm(d) > 1e-6:
                    anims.append(m.animate.shift(d))
        return anims

    def live(self, fn):
        """An arrow redrawn every frame (same family throughout: CE draws the family it saw
        when a play() began, so swapping submobjects would leave stale copies on screen)."""
        m = fn()
        m.add_updater(lambda x: x.become(fn()))
        return m

    # ── build ───────────────────────────────────────────────────────────────────────────
    def build_world(self):
        self.pins = []
        # s4's end shot
        self.axes = make_axes()
        self.ax_labels = [
            self.pin(MathTex("x", font_size=36), P(5.5, 0, 0), {"STD": (0.28, -0.12)}),
            self.pin(MathTex("y", font_size=36), P(0, 3.5, 0), {"STD": (-0.25, 0.22)}),
            self.pin(MathTex("z", font_size=36), P(0, 0, 6.5), {"STD": (0.3, -0.15)}),
        ]
        self.grid = floor_grid()
        self.va = vec3(P(3, 0, 0), BLUE)
        self.vb = vec3(P(1, 2, 0), YELLOW)
        self.ab = vec3(P(0, 0, 6), TEAL, thick=0.035, tip_h=0.32, tip_r=0.12)
        self.la = self.pin(set_backstroke(coord_label(r"\mathbf a", (3, 0, 0), BLUE)), P(3, 0, 0), {"STD": (0.0, -0.62)})
        self.lb = self.pin(set_backstroke(coord_label(r"\mathbf b", (1, 2, 0), YELLOW)), P(1, 2, 0), {"STD": (1.4, 0.3)})
        self.para = Polygon(P(0, 0), P(3, 0), P(4, 2), P(1, 2)).set_fill(TEAL, 0.45).set_stroke(TEAL, 2)
        self.para.set_z_index(-1)
        self.lab_ab = self.hud(set_backstroke(MathTex(r"\mathbf a\times\mathbf b=(0,0,6)", font_size=44, color=TEAL))
                               .move_to([-1.30, 3.15, 0]))
        # this scene's short labels
        self.a_lab = self.pin(lab(r"\mathbf a", BLUE), P(*A), {"STD": (0.15, 0.32), "SPLIT": (0.15, 0.32), "UP": (0.35, 0.0)})
        self.b_lab = self.pin(lab(r"\mathbf b", YELLOW), P(*B), {"STD": (-0.25, 0.3), "SPLIT": (-0.25, 0.3), "UP": (-0.35, 0.1)})
        self.ab_lab = self.pin(lab(r"\mathbf a\times\mathbf b", TEAL, 44), P(*AXB),
                               {"STD": (0.8, -0.1), "SPLIT": (0.8, -0.1), "UP": (0.75, 0.15)})
        self.up_floor = up_floor()

    def build_hud(self):
        q = MathTex(r"\mathbf a", r"\times", r"(", r"\mathbf b", r"+", r"\mathbf c", r")", r"\overset{?}{=}",
                    r"\mathbf a", r"\times", r"\mathbf b", r"+", r"\mathbf a", r"\times", r"\mathbf c", font_size=56)
        for i, col in [(0, BLUE), (3, GREEN), (4, GREEN), (5, GREEN), (8, BLUE), (10, YELLOW), (12, BLUE), (14, PINK)]:
            q[i].set_color(col)
        max(q[7], key=lambda g: g.get_center()[1]).set_color(YELLOW)
        self.q = self.hud(q.move_to(3.25 * UP))
        self.matters = self.hud(MathTex(r"\text{multiply out brackets}\;\longrightarrow\;\text{components}",
                                        font_size=36, color=DIM).move_to(2.5 * UP))

        n1 = MathTex(r"|\mathbf b+\mathbf c|\;\ne\;|\mathbf b|+|\mathbf c|", color=RED, font_size=46)
        n2 = MathTex(r"\text{the angle to }\mathbf a\text{ changes}", color=RED, font_size=46)
        recipe = MathTex(r"|\mathbf a|\,|\mathbf b|\sin\theta", font_size=46)
        hand = hand_icon()
        plusq = MathTex(r"+\;?", color=RED, font_size=54)
        VGroup(recipe, hand, plusq).arrange(RIGHT, buff=0.4)
        VGroup(n1, n2, VGroup(recipe, hand, plusq)).arrange(DOWN, buff=0.65, aligned_edge=LEFT) \
            .to_edge(LEFT, buff=0.75).shift(0.1 * UP)
        self.notes = (n1, n2, recipe, hand, plusq)
        self.hud(*self.notes)

        mbox = RoundedRectangle(corner_radius=0.16, width=3.1, height=1.2).set_stroke(FG, 3).set_fill(BG, 0.9)
        mlabel = MathTex(r"\mathbf a", r"\times", r"(\quad\;\;)", font_size=58)
        mlabel[0].set_color(BLUE)
        self.machine = VGroup(mbox, mlabel).move_to([-4.2, 0.2, 0])
        mlabel.move_to(mbox)
        par = mlabel[2]
        slot = (par[0].get_right() + par[-1].get_left()) / 2
        self.b_in = MathTex(r"\mathbf b", color=YELLOW, font_size=58).move_to(slot).align_to(mlabel[0], DOWN)
        self.out_arrow = Arrow(mbox.get_bottom(), mbox.get_bottom() + 0.95 * DOWN, buff=0.08, color=TEAL,
                               stroke_width=5, max_tip_length_to_length_ratio=0.3)
        self.out_lab = MathTex(r"\mathbf a\times\mathbf b", color=TEAL, font_size=56).next_to(self.out_arrow, DOWN, buff=0.15)
        self.mbox, self.mlabel = mbox, mlabel
        self.hud(self.machine, self.b_in, self.out_arrow, self.out_lab)

        f1 = MathTex(r"|\mathbf b_\perp|", "=", r"|\mathbf b|", r"\sin\theta", font_size=50)
        f1[0].set_color(YELLOW)
        f1[2].set_color(YELLOW)
        f2 = MathTex(r"\mathbf a\times\mathbf b", "=", r"\mathbf a\times\mathbf b_\perp", font_size=50)
        f2[0].set_color(TEAL)
        f2[2].set_color(TEAL)
        VGroup(f1, f2).arrange(DOWN, buff=0.7, aligned_edge=LEFT).to_edge(LEFT, buff=0.8).shift(0.4 * UP)
        self.f1, self.f2 = self.hud(f1, f2)

        self.strip = self.hud(Strip())

        fm = MathTex(r"\mathbf a\times\mathbf b", "=", r"|\mathbf a|", r"\,R(", r"\mathbf b_\perp", r")", font_size=50)
        fm[0].set_color(TEAL)
        fm[2].set_color(BLUE)
        fm[4].set_color(YELLOW)
        self.formula = self.hud(fm.to_corner(DL, buff=0.7))

        vals = [MathTex(s, color=GOLD, font_size=42) for s in ("(1,2,0)", "(0,2,0)", "(0,0,2)", "(0,0,6)")]
        tos = [MathTex(r"\to", color=GOLD, font_size=42) for _ in range(3)]
        row = VGroup(vals[0], tos[0], vals[1], tos[1], vals[2], tos[2], vals[3]).arrange(RIGHT, buff=0.3)
        row.move_to(2.3 * UP)
        self.vals, self.tos = vals, tos
        self.hud(*vals, *tos)

    # ── scene ───────────────────────────────────────────────────────────────────────────
    def construct(self):
        self.set_camera_orientation(**STD)
        self.build_world()
        self.build_hud()
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.clip5()
        self.end_shot()

    def clip1(self):
        with self.say("c1.mach.1") as c:
            shot = [self.grid, self.axes, *self.ax_labels, self.para, self.va, self.vb, self.ab,
                    self.la, self.lb, self.lab_ab]
            self.play(*[FadeIn(m) for m in shot], run_time=1.0)
            c.wait_until("question")
            # make room: the picture moves right and down, seen from higher up
            short = (self.a_lab, self.b_lab, self.ab_lab)
            self.play(CamMove(self, SPLIT), *self.reoffset("SPLIT"),
                      *[time_span(FadeOut(m), 0, 0.6) for m in (self.la, self.lb, self.lab_ab, self.para, *self.ax_labels)],
                      *[time_span(FadeIn(m), 0.9, 1.6) for m in short],
                      run_time=max(1.0, min(1.8, c.until("Is ay") - 0.05)))
            c.wait_until("Is ay")
            self.play(Write(self.q[0:7]), run_time=1.6)
            c.wait_until("equal to")
            self.play(Write(self.q[7:]), run_time=min(2.4, c.until("matters") - 0.3))
            settle(self, self.q)
            c.wait_until("matters")
            self.play(FadeIn(self.matters, shift=0.2 * DOWN), run_time=1.0)

    def clip2(self):
        n1, n2, recipe, hand, plusq = self.notes
        with self.say("c1.mach.2") as c:
            self.play(self.fx(FlashAround(self.q[7], color=YELLOW, time_width=1.5, run_time=1.5)))
            c.wait_until("lengths")
            self.play(FadeIn(n1, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("angle")
            self.play(FadeIn(n2, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("sines")
            self.play(FadeIn(recipe, shift=0.3 * DOWN), FadeIn(hand, shift=0.3 * DOWN), run_time=1.2)
            c.wait_until("says nothing")
            self.play(FadeIn(plusq, scale=1.4), run_time=0.8)
            c.wait_until("Fix ay")
            # the notes give way to the machine
            self.play(LaggedStart(*[FadeOut(m) for m in (self.matters, n1, n2, recipe, hand, plusq)],
                                  lag_ratio=0.1, run_time=1.0),
                      time_span(FadeIn(self.mbox), 0.5, 1.8), time_span(Write(self.mlabel), 0.5, 1.8),
                      time_span(flash_line(O, P(*A), BLUE), 0.8, 2.0), run_time=2.0)
            c.wait_until("Bee goes in")
            self.play(FadeIn(self.b_in, shift=1.0 * DOWN), run_time=1.1)
            c.wait_until("and ay cross bee")
            self.play(GrowArrow(self.out_arrow), FadeIn(self.out_lab, shift=0.4 * DOWN),
                      run_time=max(0.5, min(1.1, c.until() - 0.05)))
            self.mach_all = VGroup(self.mbox, self.mlabel, self.b_in, self.out_arrow, self.out_lab)
            settle(self, self.mach_all)

    def clip3(self):
        bpar = vec3(P(*BPAR), DIM, thick=0.032)
        bperp = vec3(P(*B), YELLOW, start=P(*BPAR))
        self.bperp = bperp
        bpar_lab = self.pin(lab(r"\mathbf b_\parallel", DIM, 44), P(0.5, 0, 0), {"SPLIT": (0.05, -0.45)}, "SPLIT")
        bperp_lab = self.pin(lab(r"\mathbf b_\perp", YELLOW, 44), P(1, 1, 0),
                             {"SPLIT": (0.45, -0.05), "UP": (0.15, -0.42)}, "SPLIT")
        self.bperp_lab = bperp_lab
        ra = corner(P(*BPAR), LEFT, UP)
        theta_arc = Arc(radius=0.45 * U, start_angle=0, angle=THETA, arc_center=O).set_stroke(FG, 3)
        mid = 0.75 * np.array([np.cos(THETA / 2), np.sin(THETA / 2)])
        theta_lab = self.pin(set_backstroke(MathTex(r"\theta", font_size=40)), P(*mid), {"SPLIT": (0.05, 0.0)}, "SPLIT")
        para = self.para
        rect = Polygon(P(0, 0), P(3, 0), P(3, 2), P(0, 2)).set_fill(TEAL, 0.45).set_stroke(TEAL, 2)
        curl = plane_arc(O, RIGHT, UP, 0.95, 0.2, PI / 2 - 0.25, color=FG)
        self.c3 = dict(theta_arc=theta_arc, theta_lab=theta_lab)

        with self.say("c1.mach.3") as c:
            # the question has done its job; the machine waits in the corner
            self.play(FadeOut(self.q), self.mach_all.animate.scale(0.6).move_to([-5.35, 2.55, 0]), run_time=1.2)
            c.wait_until("par")
            self.play(GrowFromPoint(bpar, O), FadeIn(bpar_lab, shift=0.2 * DOWN),
                      run_time=max(0.6, min(1.0, c.until("perp") - 0.05)))
            c.wait_until("perp")
            self.play(GrowFromPoint(bperp, P(*BPAR)), FadeIn(bperp_lab, shift=0.2 * LEFT), run_time=1.1)
            self.play(Create(ra), run_time=0.6)
            c.wait_until("tri")
            self.play(Create(theta_arc), FadeIn(theta_lab), run_time=1.0)
            c.wait_until("opposite theta")
            self.play(flash_line(P(*BPAR), P(*B), YELLOW, run_time=1.2))
            c.wait_until("so its length")
            self.play(Write(self.f1), run_time=1.6)
            c.wait_until("same")
            # the parallelogram from s4 comes back: b-perp is its height
            self.play(FadeIn(para), flash_line(P(*BPAR), P(*B), YELLOW), run_time=1.2)
            c.wait_until("So crossing ay")
            self.follow(bperp_lab, lambda: bperp.get_center())
            self.play(Transform(para, rect), bperp.animate.shift(-U * BPAR), FadeOut(ra), run_time=2.0)
            self.unfollow(bperp_lab)
            c.wait_until("turning the same way")
            self.play(Create(curl), flash_line(O, P(*AXB), TEAL), run_time=1.3)
            c.wait_until("In other words")
            self.play(Write(self.f2), run_time=1.6)
            c.wait_until("drop")
            self.play(FadeOut(bpar), FadeOut(bpar_lab), FadeOut(curl), run_time=1.0)

    def clip4(self):
        bperp = self.bperp
        light = self.pin(light_icon(), P(3.6, 2, 0), {"UP": (0, 0)}, "UP")
        ray = DashedLine(P(3.35, 2, 0), P(0, 2, 0), dash_length=0.09).set_stroke(FG, 2.5, 0.7)
        ra_up = corner(O, U * A, U * AXB, s=0.24)
        ra_floor = corner(O, U * BPERP, U * AXB, s=0.24)
        len_lab = self.pin(lab(r"|\mathbf a|\,|\mathbf b_\perp|", TEAL, 44), P(0, 0, 3), {"UP": (-0.6, -0.55)}, "UP")
        self.c4 = dict(light=light, ray=ray, ra_up=ra_up, ra_floor=ra_floor, len_lab=len_lab)

        with self.say("c1.mach.4") as c:
            gone = [self.para, self.c3["theta_arc"], self.c3["theta_lab"], self.grid, self.axes,
                    self.b_in, self.out_arrow, self.out_lab]
            later = [time_span(FadeOut(self.f1), 0.3, 1.0), time_span(FadeOut(self.f2), 0.4, 1.1)]
            box = VGroup(self.mbox, self.mlabel)
            self.play(CamMove(self, A_UP, roll_first=True), *[time_span(FadeOut(m), 0, 0.9) for m in gone],
                      time_span(bperp.animate.set_opacity(0.3), 0, 1.0), *self.reoffset("UP"),
                      time_span(box.animate.move_to(3.3 * UP), 0.3, 1.5), *later,
                      run_time=max(1.5, min(3.0, c.until("plane") - 0.1)))
            settle(self, box)
            c.wait_until("plane")
            self.play(LaggedStart(*[Create(m) for m in self.up_floor], lag_ratio=0.06), run_time=1.8)
            c.wait_until("shadow")
            self.play(FadeIn(light, shift=0.3 * DOWN), Create(ray), run_time=1.0)
            t = ValueTracker(0)
            fall = self.live(lambda: arrow3(O, P(*(B - t.get_value() * BPAR)), YELLOW))
            self.add(fall)
            self.play(time_span(t.animate.set_value(1), 0, 1.6),
                      time_span(flash_line(O, P(*BPERP), YELLOW), 1.4, 2.4), run_time=2.4)
            fall.clear_updaters()
            self.remove(fall)
            bperp.set_opacity(1)
            c.wait_until("a light directly above")
            self.play(light.animate.scale(1.35), rate_func=there_and_back, run_time=0.8)
            c.wait_until("lies")
            self.play(flash_line(O, P(*AXB), TEAL, run_time=1.2))
            c.wait_until("meets ay")
            self.play(Create(ra_up), run_time=0.8)
            c.wait_until("at right angles to the shadow")
            self.play(Create(ra_floor), run_time=0.8)
            c.wait_until("long")
            self.play(Write(len_lab), run_time=1.4)

    def clip5(self):
        bperp, c4, strip = self.bperp, self.c4, self.strip
        floor_turn = plane_arc(O, UP, OUT, 0.75 * U * 2, 0.12, PI / 2 - 0.12, color=FG)
        ring = plane_arc(P(1.6, 0, 0), UP, OUT, 0.32, -0.6, 4.4, color=FG, width=3.5, tip=0.15)
        dot = flat3d(Dot3D(P(*B), radius=0.08, color=GOLD, resolution=(8, 8)))
        quarter = ParametricFunction(lambda s: P(0, 2 * np.cos(s), 2 * np.sin(s)), t_range=[0, PI / 2])
        zero = self.pin(lab(r"\mathbf 0", GOLD, 52), O, {"UP": (0.45, -0.35)}, "UP")

        with self.say("c1.mach.5") as c:
            # the machine opens into its three steps
            self.play(ReplacementTransform(self.mbox, strip.boxes), FadeOut(self.mlabel),
                      time_span(FadeIn(strip.labels), 0.6, 1.5), time_span(FadeIn(strip.arrows), 0.6, 1.5),
                      run_time=1.5)
            settle(self, strip)
            c.wait_until("project")
            t = ValueTracker(0)
            fall = self.live(lambda: arrow3(O, P(*(B - t.get_value() * BPAR)), YELLOW))
            self.add(fall)
            self.play(*strip.light(0), *[time_span(FadeOut(c4[k]), 0, 0.6) for k in ("ra_up", "ra_floor")],
                      time_span(t.animate.set_value(1), 0.2, 1.6), run_time=1.6)
            fall.clear_updaters()
            self.remove(fall)
            c.wait_until("rotate")
            ang = ValueTracker(0)
            turned = self.live(lambda: arrow3(O, P(0, 2 * np.cos(ang.get_value()), 2 * np.sin(ang.get_value())), YELLOW))
            self.add(turned)
            self.play(*strip.light(0, False), *strip.light(1), time_span(self.ab.animate.set_opacity(0.2), 0, 0.6),
                      time_span(FadeOut(c4["len_lab"]), 0, 0.6), ang.animate.set_value(PI / 2), Create(floor_turn),
                      run_time=2.0)
            turned.clear_updaters()
            c.wait_until("as the right hand says")
            self.play(Create(ring), run_time=1.0)
            c.wait_until("scale")
            self.remove(turned)
            k = ValueTracker(1)
            grown = self.live(lambda: arrow3(O, P(0, 0, 2 * k.get_value()), interpolate_color(
                ManimColor(YELLOW), ManimColor(TEAL), (k.get_value() - 1) / 2), big=k.get_value() > 2.0))
            self.add(grown)
            self.play(*strip.light(1, False), *strip.light(2), k.animate.set_value(3),
                      time_span(FadeOut(floor_turn), 0, 0.6), time_span(FadeOut(ring), 0, 0.6), run_time=2.0)
            grown.clear_updaters()
            self.remove(grown)
            self.ab.set_opacity(1)
            self.play(FadeIn(self.formula, shift=0.2 * UP), flash_line(O, P(*AXB), TEAL),
                      run_time=max(0.5, min(1.1, c.until("run") - 0.05)))
            c.wait_until("run")
            self.play(*strip.light(2, False), FadeIn(self.vals[0], shift=0.2 * DOWN), FadeIn(dot, scale=0.5), run_time=1.0)
            c.wait_until("p")
            self.play(*strip.light(0), TransformFromCopy(self.vals[0], self.vals[1]), FadeIn(self.tos[0]),
                      dot.animate.move_to(P(*BPERP)), run_time=1.5)
            c.wait_until("r")
            self.play(*strip.light(0, False), *strip.light(1), TransformFromCopy(self.vals[1], self.vals[2]),
                      FadeIn(self.tos[1]), MoveAlongPath(dot, quarter), run_time=1.5)
            c.wait_until("s")
            self.play(*strip.light(1, False), *strip.light(2), TransformFromCopy(self.vals[2], self.vals[3]),
                      FadeIn(self.tos[2]), dot.animate.move_to(P(*AXB)), run_time=1.5)
            c.wait_until("our arrow from before")
            self.play(*strip.light(2, False), flash_line(O, P(*AXB), TEAL),
                      self.fx(FlashAround(self.vals[3], color=TEAL, time_width=1.5)), run_time=1.3)

            # the one case the split skipped: b along a
            c.wait_until("point")
            sw = ValueTracker(0)
            L = np.sqrt(5)

            def bw():
                a = THETA * (1 - sw.get_value())
                return np.array([L * np.cos(a), L * np.sin(a), 0])

            b_live = self.live(lambda: arrow3(O, P(*bw()), YELLOW))
            sh_live = self.live(lambda: arrow3(O, P(0, bw()[1], 0), YELLOW))
            out_live = self.live(lambda: arrow3(O, P(0, 0, 3 * bw()[1]), TEAL, big=True))
            self.remove(self.vb, bperp, self.ab)
            self.add(b_live, sh_live, out_live)
            self.follow(self.b_lab, lambda: P(*bw()))
            dims = [m.animate.set_opacity(0.35) for m in (*self.vals, *self.tos)]
            self.play(*[time_span(d, 0, 0.8) for d in dims],
                      *[time_span(FadeOut(m), 0, 0.8) for m in (dot, c4["light"], c4["ray"], self.bperp_lab, self.ab_lab)],
                      time_span(sw.animate.set_value(1), 0.4, 3.0), run_time=3.0)
            for h in (b_live, sh_live, out_live):
                h.clear_updaters()
            self.unfollow(self.b_lab)
            c.wait_until("single point")
            shadow_dot = flat3d(Dot3D(O, radius=0.075, color=YELLOW, resolution=(8, 8)))
            self.play(FadeIn(shadow_dot, scale=2.0), run_time=0.6)
            c.wait_until("the machine gives zero")
            self.play(FadeIn(zero, scale=0.6), run_time=0.8)

    def end_shot(self):
        # s7 opens on this: a vertical, the floor at right angles to it, the strip with no ticks
        self.wait(1.0)
        keep = [self.up_floor, self.va, self.a_lab, self.strip]
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        gone = [m for m in list(self.mobjects) if id(m) not in keep_ids]
        self.play(LaggedStart(*[FadeOut(m) for m in gone], lag_ratio=0.08), run_time=1.2)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
        self.wait(0.15)
