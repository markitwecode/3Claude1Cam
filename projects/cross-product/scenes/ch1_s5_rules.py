"""Chapter 1, scene 5: what the picture gives for free. Clips c1.rules.1 – c1.rules.4.

Opens by fading in s4's end shot (ch1_s4_define's shared 3D frame: W, make_axes, floor_grid,
vec3, Camera3D, STD camera). b x a = -a x b (same parallelogram, thumb flips), a x a = 0 (s4's
FLOOR angles, zoomed out to fit b's slide), the i/j/k table (unit square at FLOOR angles, the
cyclic wheel, minus against it, zeros on the diagonal; parked top-right in clip 4 and reused by
s8), and the missing associativity.

2D objects are HUD objects (hud(): fixed in frame by a flag, so copies made by transforms stay
fixed); labels on 3D points are pinned like s4's. After the 3D picture leaves in clip 3 the camera
is reset flat, so the rest is plain 2D.

Table (for s8): MathTex font 52, FG bold i/j/k headers and entries, DIM corner "×", DIM 2-px rules
under the header row and right of the header column, cells 1.35 wide x 1.05 tall, minus signs RED,
diagonal zeros DIM. Full size centred (3.4, -0.5); parked = scaled 0.6, top-right corner with
0.5 margins (right edge x = 6.6, top y = 3.5).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))   # harmless; vk puts engine/ on the path

import numpy as np  # noqa: E402
from manim import *  # noqa: E402,F403

from lib.effects import (FlashAround, TransformMatchingStrings, VShowPassingFlash,  # noqa: E402
                         set_backstroke, time_span)
from lib.kit import *  # noqa: E402,F403
from lib.narration import NarratedScene as NarratedScene2D  # noqa: E402
from lib.style import *  # noqa: E402,F403

# ---- the chapter's shared 3D frame (copied from ch1_s4_define) ---------------------------
U = 0.6
W = np.array([-2.5981, -1.5, 0.0])


def P(x, y, z=0.0):
    return W + np.array([x, y, z], dtype=float) * U


O = P(0, 0, 0)
STD = dict(phi=70 * DEGREES, theta=-60 * DEGREES, zoom=1.0, frame_center=ORIGIN)
THETA = np.arctan2(2, 1)


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
    """NarratedScene with a 3D camera (vk finds the scene by the literal `class X(NarratedScene)`)."""

    def __init__(self, **kwargs):
        super().__init__(camera_class=Camera3D, **kwargs)


def flat3d(mob):
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
# ------------------------------------------------------------------------------------------


def vec(end, color, scale=1.0):
    """vec3 that survives short and zero lengths (b shrinking through the origin)."""
    end = np.array(end, dtype=float)
    L = np.linalg.norm(end - O)
    th, th_h, th_r = 0.025 * scale, 0.27 * scale, 0.095 * scale
    if L < 0.03:
        return vec3(O + 0.03 * RIGHT, color, thick=th, tip_h=0.015, tip_r=0.01).set_opacity(0)
    h = min(th_h, 0.5 * L)
    return vec3(end, color, thick=th, tip_h=h, tip_r=th_r * h / th_h)


FLOOR_ANG = dict(phi=45 * DEGREES, theta=-75 * DEGREES)   # s4's FLOOR angles
C2_ZOOM, C2_ORIGIN = 1.8, (-3.0, -0.7)                    # a x a and the parallel slide
C3_ZOOM, C3_ORIGIN = 5.0, (-5.2, -1.5)                    # i, j, k and the unit square
SWING = np.array([np.cos(-60 * DEGREES), np.sin(-60 * DEGREES), 0.0])  # STD's view axis: swing in the screen plane

RULE_SIZE = 52
RULE_POS = np.array([3.95, 2.95, 0])

TAB_SIZE, CW, RH = 52, 1.35, 1.05
TAB_CENTER = np.array([3.4, -0.5, 0])
PARK_SCALE = 0.6
SLOT_POS = np.array([3.4, 2.65, 0])
WHEEL_C, WHEEL_R = np.array([-3.4, -0.5, 0]), 1.5


class _HudSet(set):
    """Camera's fixed-in-frame set, by flag: copies of a HUD object stay HUD."""

    def __contains__(self, m):
        return getattr(m, "_hud", False) or set.__contains__(self, m)


def hud(m, z=2):
    for s in m.get_family():
        s._hud = True
    m.set_z_index(z)
    return m


def H(anim):
    hud(anim.mobject, z=3)
    return anim


def bold(letter, size=TAB_SIZE, color=FG):
    return MathTex(rf"\mathbf {letter}", font_size=size, color=color)


class Rules(NarratedScene):
    # ---------------------------------------------------------------- camera helpers
    def look_for(self, origin_xy, zoom, phi, theta):
        cam = self.camera
        old = cam.get_phi(), cam.get_theta()
        cam.set_phi(phi)
        cam.set_theta(theta)
        R = cam.generate_rotation_matrix()
        cam.set_phi(old[0])
        cam.set_theta(old[1])
        return O - (R.T @ np.array([origin_xy[0], origin_xy[1], 0.0])) / zoom

    def scr(self, p):
        self.camera.reset_rotation_matrix()
        q = self.camera.project_point(np.array(p, dtype=float))
        return np.array([q[0], q[1], 0.0])

    def cam_anims(self, phi=None, theta=None, zoom=None, look=None):
        cam, anims = self.camera, []
        for v, tr in ((phi, cam.phi_tracker), (theta, cam.theta_tracker), (zoom, cam.zoom_tracker)):
            if v is not None:
                anims.append(tr.animate.set_value(v))
        if look is not None:
            anims.append(cam._frame_center.animate.move_to(look))
        return anims

    def uncam(self):
        cam = self.camera
        self.remove(cam.phi_tracker, cam.theta_tracker, cam.zoom_tracker, cam._frame_center)

    def pin(self, mob, anchor, offset):
        anchor = np.array(anchor, dtype=float)
        mob.move_to(anchor + np.array([offset[0], offset[1], 0.0]))
        self.camera.add_fixed_orientation_mobjects(mob, center_func=lambda a=anchor: a)
        mob.set_z_index(2)
        return mob

    def set_b(self, v, color):
        B = P(*v)
        self.vb.become(vec(B, color))
        A = P(3, 0, 0)
        self.para.set_points_as_corners([O, A, A + B - O, B, O])
        flat = 1 - min(1.0, abs(3 * v[1]) / 6)       # 1 when the parallelogram has no area
        self.para.set_stroke(TEAL, 2 + 4 * flat)

    # ---------------------------------------------------------------- table and wheel
    def tab_xy(self, r, c):
        x0 = TAB_CENTER[0] - 2 * CW
        y0 = TAB_CENTER[1] + 2 * RH
        return np.array([x0 + CW * (c + 0.5), y0 - RH * (r + 0.5), 0])

    def build_table(self):
        x0, x1 = TAB_CENTER[0] - 2 * CW, TAB_CENTER[0] + 2 * CW
        y0, y1 = TAB_CENTER[1] + 2 * RH, TAB_CENTER[1] - 2 * RH
        corner = MathTex(r"\times", font_size=TAB_SIZE, color=DIM).move_to(self.tab_xy(0, 0))
        cols = [bold(n).move_to(self.tab_xy(0, c + 1)) for c, n in enumerate("ijk")]
        rows = [bold(n).move_to(self.tab_xy(r + 1, 0)) for r, n in enumerate("ijk")]
        hline = Line([x0 + 0.15, y0 - RH, 0], [x1, y0 - RH, 0]).set_stroke(DIM, 2)
        vline = Line([x0 + CW, y0 - 0.12, 0], [x0 + CW, y1, 0]).set_stroke(DIM, 2)
        self.table = hud(VGroup(corner, *cols, *rows, hline, vline))
        self.cells = {}

    def cell(self, r, c, letter, minus=False, color=FG):
        parts = (["-"] if minus else []) + [rf"\mathbf {letter}"]
        m = MathTex(*parts, font_size=TAB_SIZE, color=color)
        if minus:
            m[0].set_color(RED)
        m.move_to(self.tab_xy(r, c))
        self.cells[(r, c)] = m
        return hud(m)

    def slot_eq(self, x, y, z, minus=False):
        parts = [rf"\mathbf {x}", r"\times", rf"\mathbf {y}", "="] + (["-"] if minus else []) + [rf"\mathbf {z}"]
        m = MathTex(*parts, font_size=56, color=FG)
        if minus:
            m[4].set_color(RED)
        return hud(m.move_to(SLOT_POS))

    def build_wheel(self):
        ang = {"i": 90, "j": -30, "k": 210}
        self.wl = {n: hud(bold(n, 60).move_to(WHEEL_C + WHEEL_R * np.array(
            [np.cos(a * DEGREES), np.sin(a * DEGREES), 0]))) for n, a in ang.items()}
        d = 25
        self.arcs, self.rarcs = [], []
        for n in "ijk":
            a0 = ang[n]
            fw = Arc(radius=WHEEL_R, start_angle=(a0 - d) * DEGREES, angle=-(120 - 2 * d) * DEGREES,
                     arc_center=WHEEL_C).set_stroke(TEAL, 5)
            fw.add_tip(tip_length=0.26, tip_width=0.26)
            fw.set_color(TEAL)
            bw = Arc(radius=WHEEL_R, start_angle=(a0 - 120 + d) * DEGREES, angle=(120 - 2 * d) * DEGREES,
                     arc_center=WHEEL_C).set_stroke(RED, 5)
            bw.add_tip(tip_length=0.26, tip_width=0.26)
            bw.set_color(RED)
            self.arcs.append(hud(fw))
            self.rarcs.append(hud(bw))
        self.wheel = hud(VGroup(*self.wl.values(), *self.arcs))

    # ---------------------------------------------------------------- scene
    def construct(self):
        self.camera.fixed_in_frame_mobjects = _HudSet()
        self.set_camera_orientation(**STD)
        self.s4_end_shot()
        self.clip_swap()
        self.clip_self()
        self.clip_basis()
        self.clip_brackets()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)   # end on an empty frame
        self.wait(0.15)

    def s4_end_shot(self):
        self.axes = make_axes()
        self.ax_labels = [
            self.pin(MathTex("x", font_size=36), P(5.5, 0, 0), (0.28, -0.12)),
            self.pin(MathTex("y", font_size=36), P(0, 3.5, 0), (-0.2, 0.2)),
            self.pin(MathTex("z", font_size=36), P(0, 0, 6.5), (0.3, -0.15)),
        ]
        self.grid = floor_grid()
        self.para = Polygon(P(0, 0), P(3, 0), P(4, 2), P(1, 2))
        self.para.set_fill(TEAL, 0.45).set_stroke(TEAL, 2)
        self.para.set_z_index(-1)
        self.va = vec3(P(3, 0, 0), BLUE)
        self.vb = vec3(P(1, 2, 0), YELLOW)
        self.la = self.pin(set_backstroke(coord_label(r"\mathbf a", (3, 0, 0), BLUE)), P(3, 0, 0), (0.0, -0.62))
        self.lb = self.pin(set_backstroke(coord_label(r"\mathbf b", (1, 2, 0), YELLOW)), P(1, 2, 0), (1.4, 0.3))
        self.ab = vec3(P(0, 0, 6), TEAL, thick=0.035, tip_h=0.32, tip_r=0.12)
        lab = MathTex(r"\mathbf a\times\mathbf b=(0,0,6)", font_size=44, color=TEAL)
        lab.move_to([-1.30, 3.15, 0])
        set_backstroke(lab)
        self.lab = hud(lab)
        self.shot = [self.grid, self.axes, *self.ax_labels, self.para, self.va, self.vb, self.la, self.lb,
                     self.ab, self.lab]

    # c1.rules.1: b x a = -a x b
    def clip_swap(self):
        with self.say("c1.rules.1") as c:
            self.play(*[FadeIn(m) for m in self.shot], run_time=1.0)    # s4 faded this shot out
            c.wait_until("order")
            g = self.lab[0]
            pa, pb = g[0].get_center(), g[2].get_center()
            self.play(g[0].animate(path_arc=-0.8 * PI).move_to(pb), g[2].animate(path_arc=-0.8 * PI).move_to(pa),
                      *[FadeOut(x) for x in g[3:]], run_time=1.5)
            ba = MathTex(r"\mathbf b\times\mathbf a", font_size=44, color=TEAL)
            ba.shift(g[1].get_center() - ba[0][1].get_center())
            hud(set_backstroke(ba))
            self.remove(*self.lab.get_family())
            self.add(ba)
            self.lab = ba

            c.wait_until("same")
            edge = self.para.copy().set_fill(opacity=0).set_stroke(YELLOW, 7)
            self.play(VShowPassingFlash(edge, time_width=0.5),
                      self.para.animate(rate_func=there_and_back).set_fill(opacity=0.8), run_time=1.6)
            c.wait_until("so the length is the same")
            self.play(VShowPassingFlash(Line(O, P(0, 0, 6)).set_stroke(YELLOW, 9), time_width=0.6), run_time=1.2)

            c.wait_until("flip")
            cw = Arc(radius=1.5 * U, start_angle=THETA - 0.12, angle=-(THETA - 0.24), arc_center=O)
            cw.set_stroke(PURPLE, 6)
            cw.add_tip(tip_length=0.18, tip_width=0.18)
            cw.set_color(PURPLE)
            cw.set_z_index(1)
            self.cw = cw
            self.play(Create(cw), run_time=1.3)

            c.wait_until("and your thumb points down")
            tip = self.scr(P(0, 0, -6))
            full = MathTex(r"\mathbf b\times\mathbf a=(0,0,-6)", font_size=44, color=TEAL)
            full.move_to([tip[0] + 0.45 + full.width / 2, -3.05, 0])
            hud(set_backstroke(full))
            self.full = full
            down = MathTex(r"\mathbf b\times\mathbf a", font_size=44, color=TEAL)
            down.shift(full[0][1].get_center() - down[0][1].get_center())
            hud(set_backstroke(down))
            rt = min(1.8, c.until("neg") - 0.1)
            self.play(Rotate(self.ab, PI, axis=SWING, about_point=O),
                      time_span(FadeOut(self.lab), 0, 0.5),
                      time_span(FadeIn(down, shift=0.2 * DOWN), rt - 0.6, rt), run_time=rt)
            self.lab = down

            c.wait_until("neg")
            eq = MathTex(r"\mathbf b\times\mathbf a", "=", "-", r"\,\mathbf a\times\mathbf b", font_size=RULE_SIZE)
            eq[0].set_color(TEAL)
            eq[2].set_color(RED)
            eq[3].set_color(TEAL)
            eq.move_to(RULE_POS)
            self.rule_a = hud(eq)
            self.play(*[TransformFromCopy(down[0][i], eq[0][i]) for i in range(3)],
                      time_span(LaggedStart(*[FadeIn(eq[i]) for i in (1, 2, 3)], lag_ratio=0.25), 0.5, 1.6),
                      run_time=1.6)
            settle(self, eq)

            c.wait_until("ex")
            self.play(*[Write(full[0][i]) for i in range(3, len(full[0]))], run_time=1.2)
            self.remove(down)
            settle(self, full)
            self.lab = full

    # c1.rules.2: a x a = 0, parallel means zero
    def clip_self(self):
        with self.say("c1.rules.2") as c:
            fin = MathTex(r"\mathbf a\times\mathbf a", "=", r"\mathbf 0", font_size=RULE_SIZE)
            fin[0].set_color(TEAL)
            fin.next_to(self.rule_a, DOWN, buff=0.45, aligned_edge=LEFT)
            q = MathTex(r"\mathbf a\times\mathbf a", "=", "{?}", font_size=RULE_SIZE)
            q[0].set_color(TEAL)
            q.shift(fin[0].get_center() - q[0].get_center())
            hud(q)
            hud(fin)
            self.play(Write(q), run_time=1.0)

            c.wait_until("flat")
            look = self.look_for(C2_ORIGIN, C2_ZOOM, **FLOOR_ANG)
            r0, L0 = THETA, np.sqrt(5)

            def swing(m, t):
                ang, L = r0 * (1 - t), L0 + (3 - L0) * t
                col = interpolate_color(ManimColor(YELLOW), ManimColor(BLUE), np.clip((t - 0.6) / 0.4, 0, 1))
                self.set_b((L * np.cos(ang), L * np.sin(ang), 0), col)

            rt = min(2.4, 0.9 * c.until("its area is zero"))
            self.play(UpdateFromAlphaFunc(self.vb, swing),
                      *self.cam_anims(zoom=C2_ZOOM, look=look, **FLOOR_ANG),
                      *[time_span(FadeOut(m), 0, 0.6) for m in (self.ab, self.cw, self.lb)],
                      time_span(FadeOut(self.lab), rt - 0.9, rt - 0.1), run_time=rt)
            self.uncam()

            c.wait_until("its area is zero")
            area0 = T("area 0", 32, t2c={"0": GOLD})
            area0.move_to(self.scr(P(4.6, 0, 0)) + 0.5 * UP)
            self.area0 = hud(set_backstroke(area0))
            seg = Line(O, P(6, 0, 0)).set_stroke(YELLOW, 9)
            self.play(VShowPassingFlash(seg, time_width=0.6), FadeIn(area0, shift=0.2 * DOWN), run_time=1.3)

            c.wait_until("so ay cross ay")
            self.play(Transform(q[2], fin[2]), run_time=1.2)
            self.rule_b = q

            c.wait_until("par")

            def slide(m, t):
                col = interpolate_color(ManimColor(BLUE), ManimColor(YELLOW), np.clip(t / 0.3, 0, 1))
                self.set_b((3 - 5 * t, 0, 0), col)

            self.play(UpdateFromAlphaFunc(self.vb, slide), run_time=min(2.4, 0.9 * c.until("or one of them is zero")))

            c.wait_until("or one of them is zero")
            dot = hud(Dot(self.scr(O), radius=0.09, color=YELLOW))
            self.play(UpdateFromAlphaFunc(self.vb, lambda m, t: self.set_b((-2 * (1 - t), 0, 0), YELLOW)),
                      time_span(FadeIn(dot, scale=0.5), 0.8, 1.3),
                      H(FlashAround(self.area0, color=YELLOW, time_width=1.5)), run_time=1.3)

    # c1.rules.3: the i/j/k table
    def clip_basis(self):
        with self.say("c1.rules.3") as c:
            look = self.look_for(C3_ORIGIN, C3_ZOOM, **FLOOR_ANG)
            sweep_clear(self, *self.cam_anims(zoom=C3_ZOOM, look=look, **FLOOR_ANG), run_time=1.2)
            self.uncam()

            E = [np.array(e, dtype=float) for e in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
            sc = 1.5 / C3_ZOOM
            ijk = [vec(P(*e), FG, scale=sc) for e in E]
            mini = VGroup(*[Line(P(*(-0.45 * e)), P(*(1.6 * e))) for e in E]).set_stroke(DIM, 2)
            offs = [0.3 * DOWN + 0.25 * RIGHT, 0.32 * UP + 0.2 * RIGHT, 0.38 * UP]
            labs = [hud(set_backstroke(bold(n, 52).move_to(self.scr(P(*e)) + o))) for n, e, o in zip("ijk", E, offs)]
            self.build_table()
            self.play(Create(mini),
                      LaggedStart(*[GrowFromPoint(a, O) for a in ijk], lag_ratio=0.2),
                      LaggedStart(*[FadeIn(lb, shift=0.2 * DOWN) for lb in labs], lag_ratio=0.2),
                      time_span(FadeIn(self.table, lag_ratio=0.08), 0.8, 1.8), run_time=1.8)

            c.wait_until("square")
            I, J, K = (P(*e) for e in E)
            sq = Polygon(O, I, I + J - O, J).set_fill(TEAL, 0.5).set_stroke(TEAL, 2)
            sq.set_z_index(-1)
            area1 = T("area 1", 32, t2c={"1": GOLD}).move_to(self.scr((I + J) / 2) + 0.12 * DOWN)
            hud(set_backstroke(area1))
            self.play(FadeIn(sq), FadeIn(area1, shift=0.2 * DOWN), run_time=1.3)

            c.wait_until("and the right hand points up")
            curl = Arc(radius=0.55 * U, start_angle=0.15, angle=PI / 2 - 0.3, arc_center=O).set_stroke(PURPLE, 6)
            curl.add_tip(tip_length=0.09, tip_width=0.09)
            curl.set_color(PURPLE)
            curl.set_z_index(1)
            self.play(Create(curl), run_time=1.0)
            self.play(VShowPassingFlash(Line(O, K).set_stroke(YELLOW, 10), time_width=0.6),
                      ijk[2].animate(rate_func=there_and_back).set_color(TEAL), run_time=1.2)

            c.wait_until("so eye cross jay is kay")
            slot = self.slot_eq("i", "j", "k")
            self.play(Write(slot), run_time=1.0)

            # the wheel replaces the picture; the first fact lands in the table
            c.wait_until("wheel")
            self.build_wheel()
            picture = [mini, *ijk, *labs, sq, area1, curl]
            ck = self.cell(1, 2, "k")
            self.play(*[FadeOut(m) for m in picture],
                      time_span(FadeIn(self.wheel, lag_ratio=0.1), 0.5, 1.6),
                      time_span(TransformFromCopy(slot[4], ck), 0.5, 1.8), run_time=1.8)
            self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1, frame_center=ORIGIN)

            def fact(x, y, z, r, cc, arc, rt):
                nonlocal slot
                new = self.slot_eq(x, y, z)
                cl = self.cell(r, cc, z)
                self.play(TransformMatchingStrings(slot, new),
                          H(VShowPassingFlash(arc.copy().set_stroke(YELLOW, 9), time_width=0.6)),
                          time_span(TransformFromCopy(new[4], cl), 0.5 * rt, rt), run_time=rt)
                slot = new

            c.wait_until("jay cross kay")
            fact("j", "k", "i", 2, 3, self.arcs[1], 1.5)
            c.wait_until("kay cross eye")
            fact("k", "i", "j", 3, 1, self.arcs[2], 1.3)

            c.wait_until("against")
            new = self.slot_eq("j", "i", "k", minus=True)
            self.play(*[Transform(f, b) for f, b in zip(self.arcs, self.rarcs)],
                      TransformMatchingStrings(slot, new), run_time=1.1)
            slot = new
            neg = [self.cell(2, 1, "k", minus=True), self.cell(3, 2, "i", minus=True),
                   self.cell(1, 3, "j", minus=True)]
            self.play(TransformFromCopy(slot[4], neg[0][0]), TransformFromCopy(slot[5], neg[0][1]),
                      LaggedStart(FadeIn(neg[1], shift=0.2 * DOWN), FadeIn(neg[2], shift=0.2 * DOWN),
                                  lag_ratio=0.4), run_time=min(1.3, 0.95 * c.until("diag")))
            settle(self, neg[0])
            self.slot = slot

            c.wait_until("diag")
            zeros = [self.cell(k, k, "0", color=DIM) for k in (1, 2, 3)]
            self.play(LaggedStart(*[FadeIn(z, shift=0.2 * DOWN) for z in zeros], lag_ratio=0.3), run_time=1.3)

    # c1.rules.4: brackets matter
    def clip_brackets(self):
        with self.say("c1.rules.4") as c:
            settle(self, self.table, add=list(self.cells.values()))
            tab = self.table
            tab.generate_target()
            tab.target.scale(PARK_SCALE).to_edge(RIGHT, buff=0.5).to_edge(UP, buff=0.5)
            self.play(MoveToTarget(tab), FadeOut(self.wheel), FadeOut(self.slot), run_time=1.2)

            def look(r, cc):
                return H(FlashAround(self.cells[(r, cc)], color=YELLOW, buff=0.1, time_width=1.5))

            ib, jb, kb, x = r"\mathbf i", r"\mathbf j", r"\mathbf k", r"\times"
            l1 = MathTex("(", ib, x, ib, ")", x, jb, "=", r"\mathbf 0", x, jb, "=", r"\mathbf 0", font_size=56)
            l2 = MathTex(ib, x, "(", ib, x, jb, ")", "=", ib, x, kb, "=", "-", jb, font_size=56)
            l2[12].set_color(RED)
            l1.move_to([0, 1.5, 0])
            l2.move_to([0, 0.05, 0])
            l2.shift((l1[7].get_x() - l2[7].get_x()) * RIGHT)
            pair = VGroup(l1, l2)
            pair.shift((-1.6 - pair.get_center()[0]) * RIGHT)
            hud(l1)
            hud(l2)
            pl = MathTex("(", ib, x, ib, ")", x, jb, r"\neq", ib, x, "(", ib, x, jb, ")", font_size=56)
            pl[7].set_color(RED)
            pl.move_to([-1.6, -1.85, 0])
            hud(pl)
            r1, r2 = l1[12], VGroup(l2[12], l2[13])

            c.wait_until("left")
            self.play(LaggedStart(*[FadeIn(l1[i]) for i in range(7)], lag_ratio=0.12), run_time=1.2)
            c.wait_until("and you get zero")
            self.play(FadeIn(l1[7]), TransformFromCopy(VGroup(*l1[0:5]), l1[8]),
                      TransformFromCopy(l1[5], l1[9]), TransformFromCopy(l1[6], l1[10]),
                      look(1, 1), run_time=1.3)
            c.wait_until("still gives zero")
            self.play(FadeIn(l1[11]), TransformFromCopy(VGroup(*l1[8:11]), l1[12]), run_time=1.0)
            settle(self, l1)

            c.wait_until("right")
            self.play(LaggedStart(*[FadeIn(l2[i]) for i in range(7)], lag_ratio=0.12), run_time=1.2)
            c.wait_until("to get kay")
            self.play(FadeIn(l2[7]), TransformFromCopy(l2[0], l2[8]), TransformFromCopy(l2[1], l2[9]),
                      TransformFromCopy(VGroup(*l2[2:7]), l2[10]), look(1, 2), run_time=1.3)
            c.wait_until("then eye cross kay")
            self.play(FadeIn(l2[11]), TransformFromCopy(VGroup(*l2[8:11]), l2[12]),
                      TransformFromCopy(VGroup(*l2[8:11]), l2[13]), look(1, 3), run_time=1.2)
            settle(self, l2)

            c.wait_until("brackets")
            self.play(*[TransformFromCopy(l1[i], pl[i]) for i in range(7)],
                      *[TransformFromCopy(l2[i], pl[8 + i]) for i in range(7)],
                      time_span(GrowFromCenter(pl[7]), 0.8, 1.5),
                      H(FlashAround(r1, color=RED, buff=0.12, time_width=1.5)),
                      H(FlashAround(r2, color=RED, buff=0.12, time_width=1.5)), run_time=1.5)
            settle(self, pl)

            c.wait_until("the brackets matter")
            brackets = [l1[0], l1[4], l2[2], l2[6], pl[0], pl[4], pl[10], pl[14]]
            self.play(*recolor(brackets, YELLOW),
                      *[H(FlashAround(b, color=YELLOW, buff=0.06, time_width=1.5)) for b in brackets],
                      run_time=1.4)
            c.wait_until()
        self.wait(1.2)
