"""Chapter 1, scene 4: length is area, direction is the right hand. Clips c1.def.1 – c1.def.4.

Owns the chapter's shared 3D frame (s1, s5, s6 and s8's inset copy it):
  world   W = (-2.5981, -1.5, 0): the axes' (0,0,0) sits there, so at the STD camera the origin
          is drawn at screen (-3, 0) and the right half of the frame is free for formulas
  axes    make_axes(): ThreeDAxes x[-2.5, 5.5] y[-1.5, 3.5] z[-6.5, 6.5] (step 1), 0.6 units
          per step, FG, stroke 2, tick_size 0.05, no tips; floor_grid() FG 1.5 at opacity 0.16
  camera  STD: phi=70°, theta=-60°, zoom 1, frame_center ORIGIN (stock ThreeDScene reproduces it)
  vectors vec3(): Line3D shaft + Cone tip, flat colour (no 3D shading)
Inside the scene the camera visits FLOOR (zoomed on the area) and TOP (looking down) and returns
to STD. Those two use frame_center, which CE's Cairo ThreeDCamera also applies a second time to
the whole 2D picture (fixed-in-frame text included), so this file uses Camera3D, which doesn't.
Labels on 3D points are pinned (fixed orientation) so they follow the camera.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

from manim import *  # noqa: E402,F403

from lib.effects import FlashAround, VShowPassingFlash, set_backstroke, time_span  # noqa: E402
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene as NarratedScene2D  # noqa: E402
from lib.style import *  # noqa: E402,F403

U = 0.6                                       # scene units per axis step
W = np.array([-2.5981, -1.5, 0.0])            # where the axes' origin sits = -3·(cos30°, sin30°, 0)


def P(x, y, z=0.0):
    return W + np.array([x, y, z], dtype=float) * U


O = P(0, 0, 0)
STD = dict(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=1.0, frame_center=ORIGIN)
FLOOR = dict(phi=45 * DEGREES, theta=-75 * DEGREES, zoom=2.3, frame_center=np.array([-1.3176, -0.5283, 0.3382]))
TOP = dict(phi=0.0, theta=-90 * DEGREES, zoom=1.8, frame_center=np.array([-0.0425, -0.7778, 0.0]))
THETA = np.arctan2(2, 1)                      # the angle between a and b


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


def make_hand():
    """A schematic right hand seen from the back: fingers point right, thumb on top."""
    skin = dict(fill_color=ManimColor(BG).interpolate(ManimColor(FG), 0.17), fill_opacity=1,
                stroke_color=FG, stroke_width=3)
    fingers, curled = [], []
    for w, y in zip((1.5, 1.65, 1.55, 1.25), (0.5, 0.17, -0.16, -0.48)):
        fingers.append(RoundedRectangle(width=w, height=0.3, corner_radius=0.15, **skin)
                       .move_to([-0.1 + w / 2, y, 0]))
        curled.append(RoundedRectangle(width=0.62, height=0.3, corner_radius=0.15, **skin)
                      .move_to([-0.1 + 0.31, y, 0]))
    palm = RoundedRectangle(width=1.5, height=1.45, corner_radius=0.45, **skin).move_to([-0.6, 0, 0])
    base = np.array([-1.05, 0.55, 0.0])
    thumb = RoundedRectangle(width=1.05, height=0.34, corner_radius=0.17, **skin)
    thumb.move_to(base + RIGHT * (1.05 / 2 - 0.17)).rotate(25 * DEGREES, about_point=base)
    a_arrow = Arrow([-0.25, -0.95, 0], [1.7, -0.95, 0], buff=0, color=BLUE, stroke_width=6)
    a_lab = MathTex(r"\mathbf a", font_size=44, color=BLUE).next_to(a_arrow, RIGHT, buff=0.15)
    curl = CurvedArrow(np.array([1.8, -0.1, 0]), np.array([0.5, 1.0, 0]), angle=PI / 2,
                       color=PURPLE, stroke_width=6)
    t_arrow = Arrow([-1.05, 1.78, 0], [-1.05, 2.75, 0], buff=0, color=TEAL, stroke_width=6)
    return dict(palm=palm, fingers=fingers, curled=curled, thumb=thumb, base=base,
                a_arrow=a_arrow, a_lab=a_lab, curl=curl, t_arrow=t_arrow)


class DefineCross(NarratedScene):
    # ── 3D helpers ──────────────────────────────────────────────────────────────
    def fixed(self, x):
        """Register a mobject (or an animation's mobject) as fixed in frame."""
        m = x.mobject if isinstance(x, Animation) else x
        self.camera.add_fixed_in_frame_mobjects(m)
        return x

    def pin(self, mob, anchor, offset):
        """Fixed-orientation label drawn at screen(anchor) + offset; follows camera moves."""
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

    def construct(self):
        self.set_camera_orientation(**STD)
        self.clip1()
        self.clip2()
        self.clip3()
        self.clip4()
        self.outro()

    # ── c1.def.1: axes, a, b, the floor, the length formula ─────────────────────
    def clip1(self):
        self.axes = make_axes()
        self.ax_labels = [
            self.pin(MathTex("x", font_size=36), P(5.5, 0, 0), (0.28, -0.12)),
            self.pin(MathTex("y", font_size=36), P(0, 3.5, 0), (-0.25, 0.22)),
            self.pin(MathTex("z", font_size=36), P(0, 0, 6.5), (0.3, -0.15)),
        ]
        self.va = vec3(P(3, 0, 0), BLUE)
        self.vb = vec3(P(1, 2, 0), YELLOW)
        self.la = self.pin(set_backstroke(coord_label(r"\mathbf a", (3, 0, 0), BLUE)), P(3, 0, 0), (0.0, -0.62))
        self.lb = self.pin(set_backstroke(coord_label(r"\mathbf b", (1, 2, 0), YELLOW)), P(1, 2, 0), (1.4, 0.3))
        self.grid = floor_grid()

        with self.say("c1.def.1") as c:
            self.play(Create(self.axes, lag_ratio=0.2), run_time=min(2.2, 0.7 * c.until("a")))
            self.play(*[FadeIn(m) for m in self.ax_labels], run_time=0.6)
            c.wait_until("a")

            self.play(GrowFromPoint(self.va, O),
                      time_span(FadeIn(self.la, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)
            c.wait_until("b")
            self.play(GrowFromPoint(self.vb, O),
                      time_span(FadeIn(self.lb, shift=0.3 * DOWN), 0.6, 1.4), run_time=1.4)
            c.wait_until("floor")

            # "Both lie flat in the floor": tilt down onto the floor as the grid appears
            self.move_camera(**FLOOR, run_time=min(2.2, c.until("len") - 0.2),
                             added_anims=[FadeIn(self.grid, lag_ratio=0.05)])
            c.wait_until("len")

            f = MathTex(r"|\mathbf a\times\mathbf b|", "=", r"|\mathbf a|", r"\,|\mathbf b|",
                        r"\sin\theta", font_size=52)
            f[0].set_color(TEAL)
            f[2].set_color(BLUE)
            f[3].set_color(YELLOW)
            f.move_to([3.95, 3.1, 0])
            self.fixed(f)
            self.formula = f
            self.play(Write(f[0]), run_time=1.2)
            c.wait_until("is the length of")
            self.play(*[Write(p) for p in f[1:]], run_time=1.8)
            settle(self, f)
            c.wait_until("where theta")

            self.theta_arc = Arc(radius=0.55 * U, start_angle=0, angle=THETA, arc_center=O).set_stroke(FG, 3)
            mid = 0.95 * np.array([np.cos(THETA / 2), np.sin(THETA / 2)])
            self.theta_lab = self.pin(set_backstroke(MathTex(r"\theta", font_size=36)), P(*mid), (0, 0))
            self.play(Create(self.theta_arc), FadeIn(self.theta_lab), run_time=1.2)

    # ── c1.def.2: theta's range, the height, the area ───────────────────────────
    def clip2(self):
        f = self.formula
        rng = MathTex(r"0^\circ", r"\le\theta\le", r"180^\circ", font_size=44)
        rng[0].set_color(GOLD)
        rng[2].set_color(GOLD)
        rng.move_to([3.95, 2.2, 0])
        sin = MathTex(r"\sin\theta\ge", "0", font_size=44)
        sin[1].set_color(GOLD)
        sin.move_to([3.95, 1.45, 0])
        self.fixed(rng)
        self.fixed(sin)
        self.rng, self.sin = rng, sin

        foot, btip = P(1, 0, 0), P(1, 2, 0)
        self.dashed = DashedLine(btip, foot, dash_length=0.05).set_stroke(FG, 3)
        s = 0.28
        self.rangle = VMobject().set_points_as_corners([P(1, s), P(1 + s, s), P(1 + s, 0)]).set_stroke(FG, 3)
        self.para = Polygon(P(0, 0), P(3, 0), P(4, 2), P(1, 2))
        self.para.set_fill(TEAL, 0.45).set_stroke(TEAL, 2)
        self.para.set_z_index(-1)

        with self.say("c1.def.2") as c:
            self.play(FadeIn(rng, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("so its sine")
            self.play(FadeIn(sin, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("and so is the length")
            self.play(self.fixed(FlashAround(f[0], color=YELLOW, time_width=1.5)), run_time=1.5)
            c.wait_until("height")

            self.play(Create(self.dashed), run_time=1.5)
            self.play(Create(self.rangle), run_time=0.6)
            c.wait_until("h")

            # the height label is born from the formula's |b| sin(theta)
            src = VGroup(f[3], f[4])
            hl = src.copy().scale(40 / 52)
            m = self.scr(P(1, 1.15, 0))
            hl.move_to(m + RIGHT * (0.3 + hl.width / 2) + DOWN * 0.05)
            set_backstroke(hl)
            fly = src.copy()
            self.fixed(fly)
            self.fixed(hl)
            self.hlab = hl
            self.play(ReplacementTransform(fly, hl), run_time=1.6)
            c.wait_until("area")

            c.wait_until("the base")
            base_path = Line(P(0, 0), P(3, 0)).set_stroke(YELLOW, 8)
            self.play(VShowPassingFlash(base_path, time_width=0.6), run_time=1.0)
            c.wait_until("the height")
            h_path = Line(btip, foot).set_stroke(YELLOW, 8)
            self.play(VShowPassingFlash(h_path, time_width=0.6), run_time=1.0)
            c.wait_until("the area of")
            self.play(DrawBorderThenFill(self.para), run_time=1.6)
            c.wait_until("base is three")

            def tag(text, num, pos):
                t = T(text, 32, t2c={num: GOLD})
                set_backstroke(t)
                return self.fixed(t.move_to(pos))

            b3 = tag("base 3", "3", self.scr(P(1.45, 0, 0)) + DOWN * 0.6)
            h2 = tag("height 2", "2", [0, 0, 0])
            h2.next_to(hl, DOWN, buff=0.2, aligned_edge=LEFT)
            a6 = tag("area 6", "6", self.scr(P(3.3, 0.55, 0)))
            self.six = [b3, h2, a6]
            self.play(FadeIn(b3, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("height is two")
            self.play(FadeIn(h2, shift=0.2 * DOWN), run_time=0.8)
            c.wait_until("area is six")
            self.play(FadeIn(a6, scale=0.8), run_time=0.8)

    # ── c1.def.3: the direction, the right hand, counterclockwise ───────────────
    def clip3(self):
        hand = make_hand()
        S, C = 1.1, np.array([3.95, -0.55, 0.0])         # the icon lives in the right half
        flat = ["palm", "thumb", "a_arrow", "a_lab", "curl", "t_arrow"]
        for m in [hand[k] for k in flat] + hand["fingers"] + hand["curled"]:
            m.scale(S, about_point=ORIGIN).shift(C)
            self.fixed(m)
            m.set_z_index(3)
        hand["base"] = hand["base"] * S + C
        hand["palm"].set_z_index(3.1)
        hand["thumb"].set_z_index(3.2)
        self.hand = hand

        up = vec3(P(0, 0, 1.6), DIM)
        down = vec3(P(0, 0, -1.6), DIM)
        self.cand_up = up
        ccw = Arc(radius=1.5 * U, start_angle=0.12, angle=THETA - 0.24, arc_center=O).set_stroke(PURPLE, 6)
        ccw.add_tip(tip_length=0.18, tip_width=0.18)
        ccw.set_z_index(1)
        self.ccw = ccw

        with self.say("c1.def.3") as c:
            # "Now the direction": the length formulas are done
            self.play(LaggedStart(*[FadeOut(m) for m in (self.formula, self.rng, self.sin)],
                                  lag_ratio=0.15), run_time=1.0)
            c.wait_until("two")
            self.play(GrowFromPoint(up, O), GrowFromPoint(down, O), run_time=1.2)
            c.wait_until("up or down")

            floor_stuff = [self.hlab, *self.six, self.dashed, self.rangle, self.theta_arc, self.theta_lab]
            self.move_camera(**STD, run_time=1.8,
                             added_anims=[time_span(FadeOut(m), 0, 0.7) for m in floor_stuff])
            c.wait_until("hand")

            parts = [*hand["fingers"], hand["palm"], hand["thumb"]]
            self.play(LaggedStart(*[FadeIn(m) for m in parts], lag_ratio=0.1), run_time=1.0)
            c.wait_until("fingers")

            self.play(GrowArrow(hand["a_arrow"]), FadeIn(hand["a_lab"], shift=0.2 * LEFT),
                      VShowPassingFlash(Line(O, P(3, 0, 0)).set_stroke(YELLOW, 8), time_width=0.6),
                      run_time=1.2)
            c.wait_until("curl")

            self.play(*[Transform(f, g) for f, g in zip(hand["fingers"], hand["curled"])],
                      Create(hand["curl"]),
                      VShowPassingFlash(Line(O, P(1, 2, 0)).set_stroke(YELLOW, 8), time_width=0.6),
                      run_time=1.0)
            self.play(Rotate(hand["thumb"], 65 * DEGREES, about_point=hand["base"]),
                      time_span(GrowArrow(hand["t_arrow"]), 0.6, 1.4),
                      FadeOut(down), up.animate.set_color(TEAL), run_time=1.4)
            c.wait_until("ccw")

            # seen from the tip of a x b: look straight down on the floor
            self.move_camera(**TOP, run_time=min(1.8, 0.5 * c.until("toward bee")))
            self.play(Create(ccw), run_time=1.5)

    # ── c1.def.4: the area becomes the arrow; a vector, not a number ────────────
    def clip4(self):
        ab = vec3(P(0, 0, 6), TEAL, thick=0.035, tip_h=0.32, tip_r=0.12)
        self.ab = ab
        rise_line = Line(O, P(0, 0, 6) - 0.32 * OUT).set_stroke(TEAL, 7)
        lab = MathTex(r"\mathbf a\times\mathbf b=(0,0,6)", font_size=44, color=TEAL)
        lab.move_to([-1.30, 3.15, 0])
        set_backstroke(lab)
        self.fixed(lab)
        lab.set_z_index(2)
        self.lab_ab = lab
        hand = self.hand

        with self.say("c1.def.4") as c:
            self.move_camera(**STD, run_time=1.4, added_anims=[FadeOut(self.ccw)])
            self.play(ReplacementTransform(self.para.copy(), rise_line),
                      time_span(FadeOut(self.cand_up), 0.0, 0.8),
                      time_span(FadeIn(ab[1]), 1.3, 1.9),
                      time_span(FadeIn(lab, shift=0.3 * DOWN), 1.2, 1.9),
                      run_time=1.9)
            self.remove(rise_line, ab[1])
            self.add(ab)
            c.wait_until("The area has become")

            outline = Polygon(P(0, 0), P(3, 0), P(4, 2), P(1, 2)).set_stroke(YELLOW, 7).set_fill(opacity=0)
            self.play(Succession(VShowPassingFlash(outline, time_width=0.5, run_time=1.2),
                                 VShowPassingFlash(Line(O, P(0, 0, 6)).set_stroke(YELLOW, 9),
                                                   time_width=0.6, run_time=0.9)))
            c.wait_until("conv")

            rh = T("right-handed", 30, DIM)
            rh.move_to([-5.0, -1.25, 0])
            self.fixed(rh)
            self.rh = rh
            hand_all = VGroup(hand["palm"], hand["thumb"], *hand["fingers"], hand["a_arrow"],
                              hand["a_lab"], hand["curl"], hand["t_arrow"])
            self.play(FadeIn(rh, shift=0.2 * DOWN),
                      self.fixed(FlashAround(hand_all, color=YELLOW, time_width=1.5, buff=0.2)),
                      run_time=1.5)
            c.wait_until("vec")

            dot = MathTex(r"\mathbf a\cdot\mathbf b=3", font_size=44, color=GOLD)
            dot.move_to([3.9, lab.get_y(), 0])
            num = T("a number", 30, GOLD).next_to(dot, DOWN, buff=0.3)
            vec = T("a vector", 30, TEAL).next_to(lab, DOWN, buff=0.3)
            for m in (dot, num, vec):
                self.fixed(m)
            self.compare = [dot, num, vec]
            self.play(*[FadeOut(m) for m in hand_all], FadeIn(dot, shift=0.3 * DOWN), run_time=1.0)
            c.wait_until("which is a number")
            self.play(FadeIn(num, shift=0.2 * DOWN), run_time=0.7)
            c.wait_until("ay cross bee", nth=1)
            self.play(FadeIn(vec, shift=0.2 * DOWN),
                      self.fixed(FlashAround(lab, color=TEAL, time_width=1.5)), run_time=1.2)

    # ── hand-off: the 3D shot alone, which s5 opens on ──────────────────────────
    def outro(self):
        self.wait(0.8)                     # + the clip's 0.35 s gap: ~1.5 s after "is a vector"
        self.play(*[FadeOut(m) for m in [*self.compare, self.rh]], run_time=0.6)
        self.wait(0.6)
        shown = [m for m in self.mobjects if isinstance(m, VMobject)]
        self.play(*[FadeOut(m) for m in shown], run_time=0.7)
        self.remove(*self.mobjects)
        self.wait(0.15)
